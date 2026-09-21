import numpy as np
from scipy.integrate import solve_ivp

from annular_covariant_scalar_action_20260912 import full_spatial_factors


def shape_weight(offset, shape):
    fraction = np.asarray(offset) + .5
    if shape == 'beta22':
        return 6 * fraction * (1 - fraction)
    if shape == 'beta23':
        return 12 * fraction * (1 - fraction)**2
    raise ValueError(shape)


class FiniteWidthBulk:
    def __init__(self, source, gram, width, shape='beta22', slope=.1, extension='linear', tolerance=2e-13):
        self.radii = source['radii'].copy()
        self.spacing = float(self.radii[1] - self.radii[0])
        if not 0 < width <= self.spacing / 2:
            raise ValueError('This pilot requires 0 < width <= h/2.')
        self.width, self.shape, self.slope = width, shape, slope
        self.coupling, self.lapse_origin = .1, .85
        self.scalar, self.momentum = source['scalar'].copy(), source['momentum'].copy()
        if extension not in ['flat', 'linear']:
            raise ValueError(extension)
        self.extension = extension
        self.scalar_slope = np.gradient(self.scalar, self.spacing, edge_order=2) if extension == 'linear' else np.zeros_like(self.scalar)
        self.momentum_slope = np.gradient(self.momentum, self.spacing, edge_order=2) if extension == 'linear' else np.zeros_like(self.momentum)
        self.factors, self.sampling = full_spatial_factors(len(self.radii), gram)
        self.factor, self.node = np.nonzero((self.factors != 0) | (self.sampling != 0))
        self.bpair = self.factors[self.factor, self.node]
        self.spair = self.sampling[self.factor, self.node]
        self.anchor_base = (self.sampling @ self.radii)[self.factor]
        self.target_base = self.radii[self.node]
        self.orientation = np.sign(self.target_base - self.anchor_base)
        self.node_weights = np.full(len(self.radii), self.spacing)
        self.node_weights[[0, -1]] /= 2
        self.edges = np.sort(np.concatenate([self.radii - width / 2, self.radii + width / 2]))
        self.solutions, self.steps = [], 0
        state = [float(source['mu'][0]), 0.]
        for lower, upper in zip(self.edges[:-1], self.edges[1:]):
            span = upper - lower

            def equation(fraction, values):
                radius = lower + span * fraction
                mass = values[0]
                geometry = 1 - 2 * mass / radius
                if geometry <= .1:
                    raise ValueError('Initial data leave the positive chart.')
                energy_density = self.energy_density(np.array([radius]))[0]
                generator = -self.slope + mass / (radius**2 * geometry) + self.coupling * energy_density / radius
                return span * np.array([self.coupling * geometry * energy_density, generator])

            solution = solve_ivp(equation, (0., 1.), state, method='DOP853', rtol=tolerance, atol=tolerance / 100, max_step=1 / 8, dense_output=True)
            if not solution.success:
                raise RuntimeError(solution.message)
            state = solution.y[:, -1]
            self.solutions.append(solution)
            self.steps += len(solution.t) - 1
        self.final_mass = float(state[0])

    def initial_scalar(self, offsets):
        offsets = np.asarray(offsets).reshape(-1)
        radii = self.radii[None, :] + self.width * offsets[:, None]
        scalar = self.scalar[None, :] + self.width * offsets[:, None] * self.scalar_slope
        momentum = self.momentum[None, :] + self.width * offsets[:, None] * self.momentum_slope
        amplitude = scalar @ self.factors.T
        nodal_d = amplitude**2 @ self.sampling / (2 * self.spacing)
        energy = self.node_weights * momentum**2 / (2 * radii**2) + radii**2 * nodal_d
        return {'R': radii, 'chi': scalar, 'p': momentum, 'A': amplitude, 'd': nodal_d, 'energy': energy}

    def layer_coordinates(self, radius):
        radius = np.asarray(radius).reshape(-1)
        index = np.clip(np.rint((radius - self.radii[0]) / self.spacing).astype(int), 0, len(self.radii) - 1)
        offsets = (radius - self.radii[index]) / self.width
        active = abs(offsets) < .5
        return index, offsets, active

    def energy_density(self, radius):
        index, offsets, active = self.layer_coordinates(radius)
        density = np.zeros(len(index))
        if active.any():
            data = self.initial_scalar(offsets[active])
            density[active] = shape_weight(offsets[active], self.shape) * data['energy'][np.arange(active.sum()), index[active]] / self.width
        return density

    def metric(self, radius):
        original_shape = np.shape(radius)
        radius = np.asarray(radius).reshape(-1)
        if radius.min() < self.edges[0] - 1e-12 or radius.max() > self.edges[-1] + 1e-12:
            raise ValueError('No unsourced extension beyond the enlarged pilot interval.')
        intervals = np.clip(np.searchsorted(self.edges, radius, side='right') - 1, 0, len(self.solutions) - 1)
        values = np.empty((2, len(radius)))
        for index in np.unique(intervals):
            mask = intervals == index
            fraction = (radius[mask] - self.edges[index]) / (self.edges[index + 1] - self.edges[index])
            values[:, mask] = self.solutions[index].sol(fraction)
        mass, primitive = values
        root = np.sqrt(1 - 2 * mass / radius)
        lapse = self.lapse_origin * np.exp(self.slope * (radius - self.radii[0]))
        density = self.energy_density(radius)
        generator = -self.slope + mass / (radius**2 * root**2) + self.coupling * density / radius
        result = {'mu': mass, 'g': primitive, 'U': root, 'N': lapse, 'epsilon': density, 'g_r': generator,
                  'P1': lapse * generator / (self.coupling * root)}
        return {key: value.reshape(original_shape) for key, value in result.items()}

    def stencil(self, offsets, drop_jacobian=False):
        offsets = np.asarray(offsets).reshape(-1)
        data = self.initial_scalar(offsets)
        fields = self.metric(data['R'])
        anchors = self.anchor_base[None, :] + self.width * offsets[:, None]
        anchor_g = self.metric(anchors)['g']
        endpoint_g = fields['g'][:, self.node]
        jacobian = np.exp(endpoint_g - anchor_g)
        if drop_jacobian:
            jacobian = np.ones_like(jacobian)
        coefficient = data['R']**2 * fields['N'] * fields['U']
        velocity = coefficient * data['p'] / data['R']**4
        density = np.stack([np.sum((self.spair * jacobian * coefficient[:, self.node])[:, self.factor == index], axis=1) for index in range(len(self.factors))], axis=1)
        amplitude_rate = np.stack([np.sum((self.bpair * jacobian * velocity[:, self.node])[:, self.factor == index], axis=1) for index in range(len(self.factors))], axis=1)
        current = data['A'][:, self.factor] * (self.spair * coefficient[:, self.node] * amplitude_rate[:, self.factor] - self.bpair * velocity[:, self.node] * density[:, self.factor]) / self.spacing
        force_pairs = -self.bpair * data['A'][:, self.factor] * density[:, self.factor] / (self.spacing * jacobian)
        d_rate_pairs = self.spair * data['A'][:, self.factor] * amplitude_rate[:, self.factor] / (self.spacing * jacobian)
        force = np.stack([force_pairs[:, self.node == index].sum(axis=1) for index in range(len(self.radii))], axis=1)
        d_rate = np.stack([d_rate_pairs[:, self.node == index].sum(axis=1) for index in range(len(self.radii))], axis=1)
        p_rate = force / self.node_weights
        energy_rate = self.node_weights * data['p'] * p_rate / data['R']**2 + data['R']**2 * d_rate
        power = velocity * force + coefficient * d_rate
        return dict(data, fields=fields, J=jacobian, C=coefficient, q=velocity, D=density, A_s=amplitude_rate,
                    I=current, global_I=current * np.exp(endpoint_g + anchor_g), Gchi=force, d1=d_rate,
                    p1=p_rate, energy1=energy_rate, power=power)

    def flux_fit(self, degree=32, drop_jacobian=False):
        points = np.cos(np.pi * (np.arange(degree + 1) + .5) / (degree + 1))
        values = self.stencil(points / 2, drop_jacobian)
        coefficients = np.polynomial.chebyshev.chebfit(points, shape_weight(points / 2, self.shape)[:, None] * values['global_I'], degree)
        return coefficients, np.polynomial.chebyshev.chebint(coefficients, axis=0)

    def flux(self, radius, fit):
        radius = np.asarray(radius).reshape(-1)
        coefficients, primitive = fit
        lower = 2 * (radius[:, None] - np.maximum(self.target_base, self.anchor_base)) / self.width
        upper = 2 * (radius[:, None] - np.minimum(self.target_base, self.anchor_base)) / self.width
        lower_clip, upper_clip = np.clip(lower, -1, 1), np.clip(upper, -1, 1)
        integrated = .5 * (np.polynomial.chebyshev.chebval(upper_clip, primitive, tensor=False) - np.polynomial.chebyshev.chebval(lower_clip, primitive, tensor=False))
        differentiated = (np.polynomial.chebyshev.chebval(upper_clip, coefficients, tensor=False) * (abs(upper) < 1) - np.polynomial.chebyshev.chebval(lower_clip, coefficients, tensor=False) * (abs(lower) < 1)) / self.width
        fields = self.metric(radius)
        kernel = np.exp(-2 * fields['g']) * (integrated @ self.orientation)
        kernel_r = -2 * fields['g_r'] * kernel + np.exp(-2 * fields['g']) * (differentiated @ self.orientation)
        return kernel, kernel_r

    def direct_flux(self, radius, order=32):
        cuts = np.concatenate([[-.5, .5], (radius - self.target_base) / self.width, (radius - self.anchor_base) / self.width])
        cuts = np.unique(cuts[(cuts >= -.5) & (cuts <= .5)])
        points, weights = np.polynomial.legendre.leggauss(order)
        total = 0.
        for lower, upper in zip(cuts[:-1], cuts[1:]):
            offsets = (lower + upper) / 2 + (upper - lower) * points / 2
            data = self.stencil(offsets)
            targets = self.target_base + self.width * offsets[:, None]
            anchors = self.anchor_base + self.width * offsets[:, None]
            hits = (radius > np.minimum(targets, anchors)) & (radius < np.maximum(targets, anchors))
            total += (upper - lower) / 2 * weights @ (shape_weight(offsets, self.shape) * np.sum(data['global_I'] * hits * self.orientation, axis=1))
        return float(total * np.exp(-2 * self.metric(np.array([radius]))['g'][0]))

    def live_density_rate(self, radius, drop_jacobian=False):
        index, offsets, active = self.layer_coordinates(radius)
        density_rate, power = np.zeros(len(index)), np.zeros(len(index))
        if active.any():
            data = self.stencil(offsets[active], drop_jacobian)
            weight = shape_weight(offsets[active], self.shape) / self.width
            density_rate[active] = weight * data['energy1'][np.arange(active.sum()), index[active]]
            power[active] = weight * data['power'][np.arange(active.sum()), index[active]]
        return density_rate, power

    def quadrature(self, order):
        points, weights = np.polynomial.legendre.leggauss(order)
        cuts = np.unique(np.concatenate([self.edges, self.radii[[2, 6, 10]], self.radii[[6, 10, 14]]]))
        lower, upper = cuts[:-1], cuts[1:]
        return ((lower[:, None] + upper[:, None]) / 2 + (upper - lower)[:, None] * points / 2).ravel(), ((upper - lower)[:, None] * weights / 2).ravel()

    def tests(self, radius):
        span = self.edges[-1] - self.edges[0]
        fraction = (radius - self.edges[0]) / span
        tests, derivatives = [], []
        for degree in range(4):
            tests.append(fraction**(degree + 2) * (1 - fraction)**2)
            derivatives.append(((degree + 2) * fraction**(degree + 1) * (1 - fraction)**2 - 2 * fraction**(degree + 2) * (1 - fraction)) / span)
        for node in [4, 8, 12]:
            half_span = 2 * self.spacing
            coordinate = (radius - self.radii[node]) / half_span
            inside = abs(coordinate) < 1
            tests.append(np.where(inside, (1 - coordinate**2)**4, 0.))
            derivatives.append(np.where(inside, -8 * coordinate * (1 - coordinate**2)**3 / half_span, 0.))
        return np.column_stack(tests), np.column_stack(derivatives)

    def compact_checks(self, degree=32, order=32):
        radius, weights = self.quadrature(order)
        fields = self.metric(radius)
        tests, derivatives = self.tests(radius)
        fit = self.flux_fit(degree)
        kernel, kernel_r = self.flux(radius, fit)
        root, lapse, mass, density = [fields[key] for key in ['U', 'N', 'mu', 'epsilon']]
        rate = -self.coupling * root * kernel / lapse
        density_rate, power = self.live_density_rate(radius)
        reference = np.sqrt(2 / 3)
        constraint = tests.T @ (weights * ((root + 1 / root - 2 * reference) / (2 * self.coupling) - root * density))
        constraint += derivatives.T @ (weights * radius * (root - reference) / self.coupling)
        mass_differential = tests.T @ (weights * mass * rate / (self.coupling * radius**2 * root**3))
        mass_differential -= derivatives.T @ (weights * rate / (self.coupling * root))
        mass_differential += tests.T @ (weights * density * rate / (radius * root))
        direct_rate = mass_differential - tests.T @ (weights * root * density_rate)
        transport_rate = -tests.T @ (weights * kernel * fields['g_r'] / lapse)
        constraint_rate = direct_rate + transport_rate
        local_ward = kernel_r + 2 * fields['g_r'] * kernel + power
        missing_transport = direct_rate.copy()
        wrong_fit = self.flux_fit(degree, drop_jacobian=True)
        wrong_kernel, unused_derivative = self.flux(radius, wrong_fit)
        wrong_rate = -self.coupling * root * wrong_kernel / lapse
        wrong_density_rate = self.live_density_rate(radius, drop_jacobian=True)[0]
        wrong_constraint_rate = tests.T @ (weights * (mass * wrong_rate / (self.coupling * radius**2 * root**3) + density * wrong_rate / (radius * root) - root * wrong_density_rate - wrong_kernel * fields['g_r'] / lapse))
        wrong_constraint_rate -= derivatives.T @ (weights * wrong_rate / (self.coupling * root))
        arrays = dict(R=radius, weights=weights, K=kernel, K_r=kernel_r, mu1=rate, epsilon1=density_rate, power=power, C0=constraint, C1=constraint_rate, missing_transport_C1=missing_transport, missing_J_C1=wrong_constraint_rate, ward=local_ward, **fields)
        return arrays, fit
