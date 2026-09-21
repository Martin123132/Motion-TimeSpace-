import numpy as np
from scipy.optimize import root_scalar

from annular_clock_reservoir_coupling_20260913 import ClockReservoirBulk, ClockReservoirPreparation, ProperClockDrive
from annular_source_second_jet_20260913 import SourceSecondJet
from annular_finite_width_bulk_current_20260913 import shape_weight


class PiecewiseLayerFit:
    def __init__(self, evaluator, degree):
        self.parts = []
        points = np.cos(np.pi*(np.arange(degree+1)+.5)/(degree+1))
        for lower, upper in [(-.5, 0.), (0., .5)]:
            offsets = (lower+upper)/2+(upper-lower)*points/2
            coefficients = np.polynomial.chebyshev.chebfit(points, evaluator(offsets), degree)
            primitive = np.polynomial.chebyshev.chebint(coefficients, axis=0)*(upper-lower)/2
            self.parts.append((lower, upper, coefficients, primitive))

    def integral(self, lower, upper):
        result = np.zeros_like(lower)
        for start, end, coefficients, primitive in self.parts:
            mapped_lower = (2*np.clip(lower, start, end)-start-end)/(end-start)
            mapped_upper = (2*np.clip(upper, start, end)-start-end)/(end-start)
            result += np.polynomial.chebyshev.chebval(mapped_upper, primitive, tensor=False)-np.polynomial.chebyshev.chebval(mapped_lower, primitive, tensor=False)
        return result

    def density(self, offsets):
        result = np.zeros_like(offsets)
        for start, end, coefficients, primitive in self.parts:
            inside = (offsets >= start) & (offsets < end)
            mapped = (2*np.clip(offsets, start, end)-start-end)/(end-start)
            result += np.where(inside, np.polynomial.chebyshev.chebval(mapped, coefficients, tensor=False), 0.)
        return result


def pair_integrals(model, radius, fit):
    lower = (radius[:, None]-np.maximum(model.target_base, model.anchor_base))/model.width
    upper = (radius[:, None]-np.minimum(model.target_base, model.anchor_base))/model.width
    integral = fit.integral(lower, upper) @ model.orientation
    derivative = (fit.density(upper)-fit.density(lower)) @ model.orientation/model.width
    return integral, derivative


def exterior_modes(offsets):
    offsets = np.asarray(offsets).reshape(-1)
    active = (offsets > -.5) & (offsets < 0.)
    bump = np.where(active, 256**2 * offsets**4 * (offsets + .5)**4, 0.)
    return np.column_stack([bump, bump * (4 * offsets + 1)])


class ExteriorModeBulk(ClockReservoirBulk):
    def __init__(self, *arguments, exterior_amplitudes=(0., 0.), **keywords):
        self.exterior_amplitudes = np.asarray(exterior_amplitudes)
        super().__init__(*arguments, **keywords)

    def initial_scalar(self, offsets):
        data = super().initial_scalar(offsets)
        original = data['p'][:, 0].copy()
        data['p'][:, 0] += exterior_modes(offsets) @ self.exterior_amplitudes
        data['energy'][:, 0] += self.node_weights[0] * (data['p'][:, 0]**2 - original**2) / (2 * data['R'][:, 0]**2)
        return data

    def flux_fit(self, degree=40, drop_jacobian=False):
        return PiecewiseLayerFit(lambda offsets: shape_weight(offsets, self.shape)[:, None]*self.stencil(offsets, drop_jacobian)['global_I'], degree)

    def flux(self, radius, fit):
        radius = np.asarray(radius).reshape(-1)
        integral, derivative = pair_integrals(self, radius, fit)
        fields = self.metric(radius)
        kernel = np.exp(-2*fields['g'])*integral
        return kernel, -2*fields['g_r']*kernel+np.exp(-2*fields['g'])*derivative


class ExteriorModePreparation(ClockReservoirPreparation):
    def __init__(self, *arguments, base_coefficients, **keywords):
        self.base_coefficients = np.asarray(base_coefficients)
        super().__init__(*arguments, **keywords)

    def build(self, amplitudes):
        source = {key: value.copy() for key, value in self.source.items()}
        source['momentum'] += self.lifts @ self.base_coefficients
        arguments = (source, self.gram, self.width, self.shape, self.slope, 'linear')
        first = ExteriorModeBulk(*arguments, reservoir_energy=self.reservoir_energy, exterior_amplitudes=amplitudes)
        lower, target = first.edges[0], first.radii[0]
        points, weights = np.polynomial.legendre.leggauss(40)
        locations = (lower + target) / 2 + (target - lower) * points / 2
        exponent = (target-lower)/2 * weights @ (2*first.coupling*first.energy_density(locations)/locations)
        defect = self.source['mu'][0] - first.metric(np.array([target]))['mu'][0]
        source['mu'][0] += defect * np.exp(exponent)
        model = ExteriorModeBulk(source, self.gram, self.width, self.shape, self.slope, 'linear', reservoir_energy=self.reservoir_energy, exterior_amplitudes=amplitudes)
        model.configure_clock(self.outer_clock)
        return model


class FixedInnerClockJet(SourceSecondJet):
    def __init__(self, *arguments, gauge_shift=0., **keywords):
        self.gauge_shift = gauge_shift
        super().__init__(*arguments, **keywords)
        self.current_jet_fit = PiecewiseLayerFit(lambda offsets: shape_weight(offsets, self.model.shape)[:, None]*self.transport_jet(offsets)['global_current_jet'], self.degree)

    def integrated_pairs(self, radius, fit):
        if isinstance(fit, PiecewiseLayerFit):
            return pair_integrals(self.model, radius, fit)
        return super().integrated_pairs(radius, fit)

    def lapse_rate(self, radius):
        rate, derivative = super().lapse_rate(radius)
        span = self.model.radii[-1] - self.model.radii[0]
        fraction = (np.asarray(radius) - self.model.radii[0]) / span
        lift = 1 - 3*fraction**2 + 2*fraction**3
        lift_r = (-6*fraction + 6*fraction**2) / span
        amplitude = self.gauge_shift - self.driver.log_lapse_rate
        return rate + amplitude*lift, derivative + amplitude*lift_r


class CommonHistorySearch:
    def __init__(self, preparation, clock_rate, outer_acceleration, target_inner_acceleration=0.):
        self.preparation = preparation
        self.clock_rate, self.outer_acceleration = clock_rate, outer_acceleration
        self.target_inner_acceleration = target_inner_acceleration
        self.records = []
        self.cached_flux = {}
        self.cached_second = {}
        self.on_record = None

    def model_and_driver(self, amplitudes):
        model = self.preparation.build(amplitudes)
        driver = ProperClockDrive(model, self.clock_rate, self.outer_acceleration, degree=56)
        return model, driver

    def flux_error(self, amplitude0, amplitude1):
        key = (float(amplitude0), float(amplitude1))
        if key in self.cached_flux:
            return self.cached_flux[key]
        model, driver = self.model_and_driver(key)
        endpoint = model.metric(np.array([model.radii[0]]))
        current = model.flux(np.array([model.radii[0]]), driver.fit)[0][0]
        mass_rate = -model.coupling * endpoint['U'][0] * current / endpoint['N'][0]
        error = float(mass_rate - self.preparation.drive[0])
        self.cached_flux[key] = error
        return error

    def flux_matched_amplitude(self, amplitude1):
        probe = .05
        first = (self.flux_error(probe, 0.) - self.flux_error(-probe, 0.)) / (2*probe)
        second = (self.flux_error(0., probe) - self.flux_error(0., -probe)) / (2*probe)
        if abs(first) < 1e-9:
            raise ValueError('No resolved mean-flux response for the first exterior mode.')
        initial = -second/first*amplitude1
        result = root_scalar(lambda value: self.flux_error(value, amplitude1), x0=initial, x1=initial+.01, method='secant', xtol=2e-10, maxiter=15)
        if not result.converged or abs(self.flux_error(result.root, amplitude1)) > 2e-12:
            raise RuntimeError('First mass-drive matching failed.')
        return float(result.root)

    def acceleration_error(self, amplitude1):
        key = float(amplitude1)
        if key in self.cached_second:
            return self.cached_second[key]['error']
        amplitude0 = self.flux_matched_amplitude(amplitude1)
        model, driver = self.model_and_driver([amplitude0, amplitude1])
        jet = FixedInnerClockJet(model, driver, degree=56, primitive_degree=36)
        endpoints = jet.first_fields(model.radii[[0, -1]])
        second = jet.current_second(model.radii[[0, -1]])
        error = float(second['mu2'][0] - self.target_inner_acceleration)
        record = {'amplitudes': [amplitude0, float(amplitude1)], 'inner_mass_rate_error': self.flux_error(amplitude0, amplitude1),
                  'inner_mass_acceleration': float(second['mu2'][0]), 'target': self.target_inner_acceleration, 'error': error,
                  'proper_inner_mass_acceleration': float((second['mu2'][0]-endpoints['L'][0]*endpoints['mu1'][0])/endpoints['N'][0]**2),
                  'inner_log_lapse_rate': float(endpoints['L'][0]), 'primitive_fit_error': jet.primitive_max_fit_error}
        self.records.append(record)
        self.cached_second[key] = record
        print(str(record), flush=True)
        if self.on_record is not None:
            self.on_record()
        return error

    def solve(self, sign=1.):
        previous, previous_error = 0., self.acceleration_error(0.)
        bracket = None
        for scale in [.25, .5, 1., 2., 4., 8., 16.]:
            current = sign*scale
            error = self.acceleration_error(current)
            if error*previous_error <= 0:
                bracket = [previous, current]
                break
            previous, previous_error = current, error
        if bracket is None:
            return None, {'status': 'no_bracket_in_declared_range', 'sign': sign, 'range_limit': 16.}
        result = root_scalar(self.acceleration_error, bracket=sorted(bracket), method='brentq', xtol=2e-9, rtol=2e-12, maxiter=35)
        if not result.converged:
            return None, {'status': 'second_drive_root_failed', 'message': str(result)}
        error = self.acceleration_error(result.root)
        record = self.cached_second[float(result.root)]
        if abs(error) > 1e-10:
            return None, {'status': 'root_residual_above_gate', 'residual': error}
        return np.asarray(record['amplitudes']), {'status': 'converged', 'iterations': result.iterations, 'bracket': bracket, 'error': error}
