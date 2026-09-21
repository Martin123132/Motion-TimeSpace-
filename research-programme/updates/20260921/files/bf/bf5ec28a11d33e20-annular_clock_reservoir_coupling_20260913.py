import numpy as np
from scipy.integrate import solve_ivp

from annular_finite_width_boundary_cut_20260913 import BoundaryCutBulk, CutPreparation
from annular_finite_width_bulk_current_20260913 import shape_weight


class ClockReservoirBulk(BoundaryCutBulk):
    def __init__(self, *arguments, reservoir_energy=.001, **keywords):
        self.reservoir_energy = reservoir_energy
        if reservoir_energy < 0:
            raise ValueError('Initial reservoir energy must be nonnegative.')
        super().__init__(*arguments, **keywords)
        state = [float(arguments[0]['mu'][0]), 0.]
        self.solutions, self.steps = [], 0
        for lower, upper in zip(self.edges[:-1], self.edges[1:]):
            span = upper - lower

            def equation(fraction, values):
                radius = lower + span * fraction
                mass = values[0]
                geometry = 1 - 2 * mass / radius
                if geometry <= .1:
                    raise ValueError('Positive chart lost.')
                density = self.energy_density(np.array([radius]))[0]
                reservoir = self.reservoir_density(np.array([radius]))[0]
                mass_gradient = self.coupling * (geometry * density + np.sqrt(geometry) * reservoir)
                transport_gradient = -self.slope + mass / (radius**2 * geometry) + self.coupling * density / radius
                return span * np.array([mass_gradient, transport_gradient])

            solution = solve_ivp(equation, (0., 1.), state, method='DOP853', rtol=2e-13, atol=2e-15, max_step=1 / 8, dense_output=True)
            if not solution.success:
                raise RuntimeError(solution.message)
            state = solution.y[:, -1]
            self.solutions.append(solution)
            self.steps += len(solution.t) - 1
        self.final_mass = float(state[0])

    def reservoir_density(self, radius):
        index, offsets, active = self.layer_coordinates(radius)
        selected = active & (index == len(self.radii) - 1)
        density = np.zeros(len(index))
        density[selected] = shape_weight(offsets[selected], self.shape) * self.reservoir_energy / self.width
        return density


class ClockReservoirPreparation(CutPreparation):
    def __init__(self, *arguments, reservoir_energy=.001, **keywords):
        self.reservoir_energy = reservoir_energy
        super().__init__(*arguments, **keywords)

    def build(self, coefficients, exterior_kick=0.):
        source = {key: value.copy() for key, value in self.source.items()}
        source['momentum'] += self.lifts @ coefficients
        arguments = (source, self.gram, self.width, self.shape, self.slope, 'linear')
        first = ClockReservoirBulk(*arguments, exterior_kick=exterior_kick, reservoir_energy=self.reservoir_energy)
        lower, target = first.edges[0], first.radii[0]
        points, weights = np.polynomial.legendre.leggauss(40)
        locations = (lower + target) / 2 + (target - lower) * points / 2
        exponent = (target - lower) / 2 * weights @ (2 * first.coupling * first.energy_density(locations) / locations)
        defect = self.source['mu'][0] - first.metric(np.array([target]))['mu'][0]
        source['mu'][0] += defect * np.exp(exponent)
        model = ClockReservoirBulk(source, self.gram, self.width, self.shape, self.slope, 'linear', exterior_kick=exterior_kick, reservoir_energy=self.reservoir_energy)
        model.configure_clock(self.outer_clock)
        return model


class ProperClockDrive:
    def __init__(self, model, clock_rate, target_acceleration, degree=48):
        self.model = model
        self.fit = model.flux_fit(degree)
        self.clock_rate, self.target_acceleration = clock_rate, target_acceleration
        radius = model.radii[-1]
        data = model.stencil([0.])
        lapse, root_f = data['fields']['N'][0, -1], data['fields']['U'][0, -1]
        current = model.flux(np.array([radius]), self.fit)[0][0]
        mass_rate = -model.coupling * root_f * current / lapse
        self.clock = lapse / root_f
        self.log_lapse_rate = clock_rate / self.clock - mass_rate / (radius * root_f**2)
        self.proper_acceleration = (target_acceleration - self.log_lapse_rate * data['q'][0, -1]) / lapse**2

    def layer(self, offsets):
        model = self.model
        data = model.stencil(offsets)
        radius, lapse, root_f, speed, free_momentum_rate = [data[key][:, -1] if key in data else data['fields'][key][:, -1] for key in ['R', 'N', 'U', 'q', 'p1']]
        current = model.flux(radius, self.fit)[0]
        mass_rate = -model.coupling * root_f * current / lapse
        required_difference = lapse**2 * self.proper_acceleration + mass_rate * speed / (radius * root_f**2) - lapse * root_f * free_momentum_rate / radius**2
        force = model.node_weights[-1] * radius**2 * required_difference / (lapse * root_f)
        multiplier = force / lapse
        reservoir_rate = -multiplier * speed
        scalar_energy_rate_increment = data['p'][:, -1] * force / radius**2
        driven_momentum_rate = free_momentum_rate + force / model.node_weights[-1]
        free_acceleration = (self.log_lapse_rate - mass_rate / (radius * root_f**2)) * speed + lapse * root_f * free_momentum_rate / radius**2
        driven_acceleration = (self.log_lapse_rate - mass_rate / (radius * root_f**2)) * speed + lapse * root_f * driven_momentum_rate / radius**2
        prescribed_profile = self.log_lapse_rate * speed + lapse**2 * self.proper_acceleration
        return dict(R=radius, N=lapse, U=root_f, mu1=mass_rate, q=speed, p=data['p'][:, -1],
                    free_p1=free_momentum_rate, driven_p1=driven_momentum_rate, rho=force, multiplier=multiplier,
                    reservoir_E1=reservoir_rate, scalar_e1_increment=scalar_energy_rate_increment,
                    free_q1=free_acceleration, driven_q1=driven_acceleration, prescribed_q1=prescribed_profile,
                    clock_exchange_residual=root_f * scalar_energy_rate_increment + reservoir_rate)

    def density_rates(self, radius):
        model = self.model
        index, offsets, active = model.layer_coordinates(radius)
        selected = active & (index == len(model.radii) - 1)
        extra_scalar, reservoir_rate = np.zeros(len(index)), np.zeros(len(index))
        if selected.any():
            data = self.layer(offsets[selected])
            weight = shape_weight(offsets[selected], model.shape) / model.width
            extra_scalar[selected] = weight * data['scalar_e1_increment']
            reservoir_rate[selected] = weight * data['reservoir_E1']
        return extra_scalar, reservoir_rate

    def checks(self, order=32):
        model = self.model
        arrays = model.unrestricted_checks(order=order, degree=48)
        radius, weights = arrays['R'], arrays['weights']
        fraction = (radius - model.radii[0]) / (model.radii[-1] - model.radii[0])
        tests = np.column_stack([fraction**degree for degree in range(6)])
        sigma = model.reservoir_density(radius)
        extra_scalar, sigma_rate = self.density_rates(radius)
        extra_scalar_row = tests.T @ (weights * arrays['U'] * extra_scalar)
        reservoir_row = tests.T @ (weights * sigma_rate)
        constraint = arrays['C0'] - tests.T @ (weights * sigma)
        propagated = arrays['C1'] - extra_scalar_row - reservoir_row
        return dict(arrays, C0=constraint, C1=propagated, sigma=sigma, sigma1=sigma_rate,
                    extra_scalar_epsilon1=extra_scalar, omit_initial_reservoir_C0=arrays['C0'],
                    omit_reservoir_energy_rate_C1=arrays['C1'] - extra_scalar_row,
                    omit_scalar_force_C1=arrays['C1'] - reservoir_row,
                    source_exchange=arrays['U'] * extra_scalar + sigma_rate,
                    source_direct_mu2_term=-arrays['N'] * model.coupling**2 * arrays['U']**4 * sigma * arrays['P1'])


def clock_factor(radius, lapse, mass, momentum, coupling=.1):
    root_squared = 1 - 2 * mass / radius
    chart = 1 - coupling**2 * root_squared**2 * momentum**2
    return lapse * np.sqrt(chart)
