import numpy as np
from scipy.optimize import root

from annular_finite_width_bulk_current_20260913 import FiniteWidthBulk


class BoundaryCutBulk(FiniteWidthBulk):
    def __init__(self, *arguments, exterior_kick=0., **keywords):
        self.clock_adjustment = None
        self.exterior_kick = exterior_kick
        super().__init__(*arguments, **keywords)

    def initial_scalar(self, offsets):
        data = super().initial_scalar(offsets)
        offsets = np.asarray(offsets).reshape(-1)
        if self.exterior_kick:
            active = (offsets > -.5) & (offsets < 0)
            bump = np.where(active, 256**2 * offsets**4 * (offsets + .5)**4, 0.)
            old = data['p'][:, 0].copy()
            data['p'][:, 0] += self.exterior_kick * bump
            data['energy'][:, 0] += self.node_weights[0] * (data['p'][:, 0]**2 - old**2) / (2 * data['R'][:, 0]**2)
        return data

    def clock_shape(self, radius):
        span = self.radii[-1] - self.radii[0]
        fraction = (np.asarray(radius) - self.radii[0]) / span
        values = np.stack([span * fraction * (1 - fraction)**2, span * fraction**2 * (fraction - 1)])
        derivatives = np.stack([1 - 4 * fraction + 3 * fraction**2, 3 * fraction**2 - 2 * fraction])
        return values, derivatives

    def configure_clock(self, outer_clock):
        self.clock_adjustment = None
        endpoints = super().metric(self.radii[[0, -1]])
        target_log_slope = endpoints['mu'] / (self.radii[[0, -1]]**2 * endpoints['U']**2) + self.coupling * endpoints['epsilon'] / self.radii[[0, -1]]
        amplitudes = target_log_slope - self.slope
        normalization = outer_clock * endpoints['U'][-1] / endpoints['N'][-1]
        reference = amplitudes @ self.clock_shape(np.array([self.edges[0]]))[0][:, 0]
        self.clock_adjustment = (amplitudes, normalization, reference)

    def metric(self, radius):
        data = super().metric(radius)
        if self.clock_adjustment is not None:
            amplitudes, normalization, reference = self.clock_adjustment
            values, derivatives = self.clock_shape(radius)
            shift = np.einsum('i,i...->...', amplitudes, values)
            shift_r = np.einsum('i,i...->...', amplitudes, derivatives)
            data['N'] = data['N'] * normalization * np.exp(shift)
            data['g'] = data['g'] - shift + reference
            data['g_r'] = data['g_r'] - shift_r
            data['P1'] = data['N'] * data['g_r'] / (self.coupling * data['U'])
        return data

    def cut_quadrature(self, order=32):
        points, weights = np.polynomial.legendre.leggauss(order)
        cuts = np.unique(np.concatenate([self.edges, self.radii]))
        cuts = cuts[(cuts >= self.radii[0]) & (cuts <= self.radii[-1])]
        lower, upper = cuts[:-1], cuts[1:]
        return ((lower[:, None] + upper[:, None]) / 2 + (upper - lower)[:, None] * points / 2).ravel(), ((upper - lower)[:, None] * weights / 2).ravel()

    def unrestricted_checks(self, order=32, degree=40):
        radius, weights = self.cut_quadrature(order)
        fields = self.metric(radius)
        endpoints = self.metric(self.radii[[0, -1]])
        fraction = (radius - self.radii[0]) / (self.radii[-1] - self.radii[0])
        tests = np.column_stack([fraction**power for power in range(6)])
        derivatives = np.column_stack([np.zeros_like(fraction)] + [power * fraction**(power - 1) / (self.radii[-1] - self.radii[0]) for power in range(1, 6)])
        endpoint_tests = np.array([[1., 0., 0., 0., 0., 0.], [1., 1., 1., 1., 1., 1.]])
        fit = self.flux_fit(degree)
        current, current_r = self.flux(radius, fit)
        endpoint_current = self.flux(self.radii[[0, -1]], fit)[0]
        root_f, lapse, mass, energy = [fields[key] for key in ['U', 'N', 'mu', 'epsilon']]
        velocity = -self.coupling * root_f * current / lapse
        endpoint_velocity = -self.coupling * endpoints['U'] * endpoint_current / endpoints['N']
        energy_rate, power = self.live_density_rate(radius)
        reference, orientation = np.sqrt(2 / 3), np.array([-1., 1.])
        gravity_boundary = endpoint_tests.T @ (orientation * self.radii[[0, -1]] * (endpoints['U'] - reference) / self.coupling)
        constraint_no_boundary = tests.T @ (weights * ((root_f + 1 / root_f - 2 * reference) / (2 * self.coupling) - root_f * energy))
        constraint_no_boundary += derivatives.T @ (weights * radius * (root_f - reference) / self.coupling)
        constraint = constraint_no_boundary - gravity_boundary
        mass_rate = tests.T @ (weights * (mass * velocity / (self.coupling * radius**2 * root_f**3) + energy * velocity / (radius * root_f)))
        mass_rate -= derivatives.T @ (weights * velocity / (self.coupling * root_f))
        boundary_rate = endpoint_tests.T @ (orientation * endpoint_velocity / (self.coupling * endpoints['U']))
        direct_energy_rate = tests.T @ (weights * root_f * energy_rate)
        connection_rate = tests.T @ (weights * current * fields['g_r'] / lapse)
        constraint_rate = mass_rate + boundary_rate - direct_energy_rate - connection_rate
        return dict(R=radius, weights=weights, K=current, K_r=current_r, mu1=velocity, epsilon1=energy_rate, power=power,
                    C0=constraint, C1=constraint_rate, no_radial_boundary_C0=constraint_no_boundary,
                    no_radial_boundary_C1=constraint_rate - boundary_rate, no_connection_time_C1=constraint_rate + connection_rate,
                    endpoint_K=endpoint_current, endpoint_mu1=endpoint_velocity, endpoint_P1=endpoints['P1'],
                    endpoint_N=endpoints['N'], endpoint_U=endpoints['U'], endpoint_mu=endpoints['mu'],
                    boundary_power=-orientation * endpoint_current, **fields)


class CutPreparation:
    def __init__(self, source, gram, kinetic_seed, outer_clock, drive, width, shape='beta22'):
        self.source, self.gram = source, gram
        self.outer_clock, self.drive, self.width, self.shape = outer_clock, drive, width, shape
        radii = source['radii']
        fraction = (radii - radii[0]) / (radii[-1] - radii[0])
        self.lifts = kinetic_seed[:, None] * np.column_stack([1 - 3 * fraction**2 + 2 * fraction**3, 3 * fraction**2 - 2 * fraction**3])
        self.slope = float(np.log(source['lapse'][-1] / source['lapse'][0]) / (radii[-1] - radii[0]))
        self.calls = 0

    def build(self, coefficients, exterior_kick=0.):
        source = {key: value.copy() for key, value in self.source.items()}
        source['momentum'] += self.lifts @ coefficients
        arguments = (source, self.gram, self.width, self.shape, self.slope, 'linear')
        first = BoundaryCutBulk(*arguments, exterior_kick=exterior_kick)
        lower, target = first.edges[0], first.radii[0]
        points, weights = np.polynomial.legendre.leggauss(40)
        locations = (lower + target) / 2 + (target - lower) * points / 2
        exponent = (target - lower) / 2 * weights @ (2 * first.coupling * first.energy_density(locations) / locations)
        defect = self.source['mu'][0] - first.metric(np.array([target]))['mu'][0]
        source['mu'][0] += defect * np.exp(exponent)
        model = BoundaryCutBulk(source, self.gram, self.width, self.shape, self.slope, 'linear', exterior_kick=exterior_kick)
        model.configure_clock(self.outer_clock)
        return model

    def residual(self, coefficients):
        self.calls += 1
        model = self.build(coefficients)
        inner = model.metric(np.array([model.radii[0]]))
        current = model.direct_flux(model.radii[0], order=24)
        mass_rate = -model.coupling * inner['U'][0] * current / inner['N'][0]
        outer_velocity = model.stencil([0.])['q'][0, -1]
        return np.array([(mass_rate - self.drive[0]) / .001, (outer_velocity - self.drive[2]) / .02])

    def solve(self):
        solution = root(self.residual, np.zeros(2), method='hybr', options={'xtol': 1e-9, 'eps': 1e-10, 'maxfev': 60})
        residual = self.residual(solution.x)
        if not np.isfinite(solution.x).all() or abs(residual).max() > 1e-8:
            raise RuntimeError('Boundary initial preparation failed: ' + repr((solution.message, solution.x, residual)))
        return solution.x, self.build(solution.x), {'root_success': bool(solution.success), 'message': str(solution.message), 'calls': self.calls, 'scaled_residual': residual.tolist()}
