import numpy as np

from annular_finite_width_bulk_current_20260913 import shape_weight


class SourceSecondJet:
    def __init__(self, model, driver, correct_boundary_slopes=True, degree=48, primitive_degree=32):
        self.model, self.driver = model, driver
        self.degree = degree
        self.lapse_slopes = np.zeros(2)
        if correct_boundary_slopes:
            endpoints = self.first_fields(model.radii[[0, -1]])
            self.lapse_slopes = endpoints['mu1'] / (model.radii[[0, -1]]**2 * endpoints['U']**4) + model.coupling * endpoints['epsilon1'] / model.radii[[0, -1]]
        self.primitive_intervals = []
        self.primitive_max_fit_error = 0.
        samples = np.cos(np.pi * (np.arange(primitive_degree + 1) + .5) / (primitive_degree + 1))
        self.primitive_edges = np.unique(np.concatenate([model.edges, model.radii]))
        total = 0.
        for lower, upper in zip(self.primitive_edges[:-1], self.primitive_edges[1:]):
            locations = (lower + upper) / 2 + (upper - lower) * samples / 2
            fields = self.first_fields(locations)
            values = fields['c2'] * np.exp(fields['g'])
            coefficients = np.polynomial.chebyshev.chebfit(samples, values, primitive_degree)
            primitive = np.polynomial.chebyshev.chebint(coefficients) * (upper - lower) / 2
            primitive[0] += total - np.polynomial.chebyshev.chebval(-1., primitive)
            total = float(np.polynomial.chebyshev.chebval(1., primitive))
            self.primitive_intervals.append(primitive)
            check_locations = np.linspace(-.95, .95, 12)
            check_fields = self.first_fields((lower + upper) / 2 + (upper - lower) * check_locations / 2)
            error = abs(np.polynomial.chebyshev.chebval(check_locations, coefficients) - check_fields['c2'] * np.exp(check_fields['g'])).max()
            self.primitive_max_fit_error = max(self.primitive_max_fit_error, float(error))
        points = np.cos(np.pi * (np.arange(degree + 1) + .5) / (degree + 1))
        data = self.transport_jet(points / 2)
        coefficients = np.polynomial.chebyshev.chebfit(points, shape_weight(points / 2, model.shape)[:, None] * data['global_current_jet'], degree)
        self.current_jet_fit = (coefficients, np.polynomial.chebyshev.chebint(coefficients, axis=0))

    def lapse_rate(self, radius):
        values, derivatives = self.model.clock_shape(radius)
        return self.driver.log_lapse_rate + np.einsum('i,i...->...', self.lapse_slopes, values), np.einsum('i,i...->...', self.lapse_slopes, derivatives)

    def first_fields(self, radius):
        radius = np.asarray(radius)
        shape = radius.shape
        points = radius.reshape(-1)
        model = self.model
        fields = model.metric(points)
        kernel, kernel_r = model.flux(points, self.driver.fit)
        mass_rate = -model.coupling * fields['U'] * kernel / fields['N']
        epsilon_rate = model.live_density_rate(points)[0] + self.driver.density_rates(points)[0]
        lapse_rate, lapse_gradient = self.lapse_rate(points)
        connection_second = mass_rate / (points**2 * fields['U']**4) + model.coupling * epsilon_rate / points - lapse_gradient - lapse_rate * fields['g_r']
        momentum_second = fields['N'] * connection_second / (model.coupling * fields['U']) + 2 * (mass_rate / (points * fields['U']**2) + lapse_rate) * fields['P1']
        result = dict(fields, K=kernel, K_r=kernel_r, mu1=mass_rate, epsilon1=epsilon_rate, L=lapse_rate, L_r=lapse_gradient, c2=connection_second, P2=momentum_second)
        return {key: value.reshape(shape) for key, value in result.items()}

    def primitive(self, radius):
        radius = np.asarray(radius)
        shape = radius.shape
        points = radius.reshape(-1)
        indices = np.clip(np.searchsorted(self.primitive_edges, points, side='right') - 1, 0, len(self.primitive_intervals) - 1)
        result = np.empty(len(points))
        for index in np.unique(indices):
            selected = indices == index
            lower, upper = self.primitive_edges[index:index + 2]
            coordinate = (2 * points[selected] - upper - lower) / (upper - lower)
            result[selected] = np.polynomial.chebyshev.chebval(coordinate, self.primitive_intervals[index])
        return result.reshape(shape)

    def transport_jet(self, offsets):
        model = self.model
        offsets = np.asarray(offsets).reshape(-1)
        data = model.stencil(offsets)
        fields = self.first_fields(data['R'])
        p_rate = data['p1'].copy()
        p_rate[:, -1] += self.driver.layer(offsets)['rho'] / model.node_weights[-1]
        q_rate = (fields['L'] - fields['mu1'] / (data['R'] * fields['U']**2)) * data['q'] + fields['N'] * fields['U'] * p_rate / data['R']**2
        coefficient_rate = data['C'] * (fields['L'] - fields['mu1'] / (data['R'] * fields['U']**2))
        anchors = model.anchor_base[None, :] + model.width * offsets[:, None]
        anchor_g = model.metric(anchors)['g']
        endpoint_g = fields['g'][:, model.node]
        endpoint_primitive, anchor_primitive = self.primitive(data['R'])[:, model.node], self.primitive(anchors)
        second_map = np.exp(endpoint_g - 2 * anchor_g) * (endpoint_primitive - anchor_primitive)
        jacobian = data['J']

        def collect(pairs):
            return np.stack([pairs[:, model.factor == index].sum(axis=1) for index in range(len(model.factors))], axis=1)

        amplitude_second = collect(model.bpair * (second_map * data['q'][:, model.node] + jacobian**2 * q_rate[:, model.node]))
        density_first = collect(model.spair * (second_map * data['C'][:, model.node] + jacobian**2 * coefficient_rate[:, model.node]))
        amplitude, amplitude_first = data['A'][:, model.factor], data['A_s'][:, model.factor]
        density = data['D'][:, model.factor]
        force_rate_pairs = -model.bpair * (amplitude_first * density + amplitude * density_first[:, model.factor] - amplitude * density * second_map / jacobian) / (model.spacing * jacobian**2)
        potential_second_pairs = model.spair * ((amplitude_first**2 + amplitude * amplitude_second[:, model.factor]) / jacobian**2 - amplitude * amplitude_first * second_map / jacobian**3) / model.spacing
        force_rate = np.stack([force_rate_pairs[:, model.node == index].sum(axis=1) for index in range(len(model.radii))], axis=1)
        potential_second = np.stack([potential_second_pairs[:, model.node == index].sum(axis=1) for index in range(len(model.radii))], axis=1)
        bracket = model.spair * data['C'][:, model.node] * amplitude_first - model.bpair * data['q'][:, model.node] * density
        bracket_first = model.spair * (jacobian * coefficient_rate[:, model.node] * amplitude_first + data['C'][:, model.node] * amplitude_second[:, model.factor])
        bracket_first -= model.bpair * (jacobian * q_rate[:, model.node] * density + data['q'][:, model.node] * density_first[:, model.factor])
        current_anchor_rate = (amplitude_first * bracket + amplitude * bracket_first) / model.spacing
        global_current_jet = np.exp(endpoint_g + 2 * anchor_g) * current_anchor_rate + data['global_I'] * (endpoint_primitive + anchor_primitive)
        return dict(data, metric1=fields, p1_driven=p_rate, q1=q_rate, C1=coefficient_rate, T2=second_map,
                    A2=amplitude_second, D1=density_first, Gchi1=force_rate, d2=potential_second,
                    I_s=current_anchor_rate, global_current_jet=global_current_jet)

    def integrated_pairs(self, radius, fit):
        model = self.model
        coefficients, primitive = fit
        lower = 2 * (radius[:, None] - np.maximum(model.target_base, model.anchor_base)) / model.width
        upper = 2 * (radius[:, None] - np.minimum(model.target_base, model.anchor_base)) / model.width
        lower_clip, upper_clip = np.clip(lower, -1, 1), np.clip(upper, -1, 1)
        integral = .5 * (np.polynomial.chebyshev.chebval(upper_clip, primitive, tensor=False) - np.polynomial.chebyshev.chebval(lower_clip, primitive, tensor=False))
        derivative = (np.polynomial.chebyshev.chebval(upper_clip, coefficients, tensor=False) * (abs(upper) < 1) - np.polynomial.chebyshev.chebval(lower_clip, coefficients, tensor=False) * (abs(lower) < 1)) / model.width
        return integral @ model.orientation, derivative @ model.orientation

    def current_second(self, radius):
        radius = np.asarray(radius)
        shape = radius.shape
        points = radius.reshape(-1)
        fields = self.first_fields(points)
        initial, initial_r = self.integrated_pairs(points, self.driver.fit)
        first, first_r = self.integrated_pairs(points, self.current_jet_fit)
        primitive = self.primitive(points)
        kernel_rate = np.exp(-3 * fields['g']) * (first - 2 * primitive * initial)
        kernel_rate_r = -3 * fields['g_r'] * kernel_rate + np.exp(-3 * fields['g']) * (first_r - 2 * primitive * initial_r - 2 * fields['c2'] * np.exp(fields['g']) * initial)
        mass_rate = fields['mu1']
        mass_acceleration = -self.model.coupling * fields['U'] / fields['N'] * (kernel_rate - (fields['L'] + mass_rate / (points * fields['U']**2)) * fields['K'])
        mass_acceleration -= self.model.coupling**2 * points * fields['U']**6 * fields['P1']**2
        return {key: value.reshape(shape) for key, value in dict(K1=kernel_rate, K1_r=kernel_rate_r, mu2=mass_acceleration).items()}

    def completed_layer(self, offsets):
        model = self.model
        offsets = np.asarray(offsets).reshape(-1)
        data = self.transport_jet(offsets)
        radius, fields = data['R'], data['metric1']
        second = self.current_second(radius)
        p_second = data['Gchi1'] / model.node_weights
        mass_term = fields['mu1'] / (radius * fields['U']**2)
        mass_second_term = second['mu2'] / (radius * fields['U']**2) + fields['mu1']**2 / (radius**2 * fields['U']**4)
        source = self.driver.layer(offsets)
        forcing = 3 * self.driver.proper_acceleration * fields['N'][:, -1]**2 * fields['L'][:, -1]
        forcing += data['q'][:, -1] * (2 * fields['L'][:, -1] * mass_term[:, -1] + mass_second_term[:, -1] + model.coupling**2 * fields['U'][:, -1]**4 * fields['P1'][:, -1]**2)
        forcing -= 2 * (fields['L'][:, -1] - mass_term[:, -1]) * fields['N'][:, -1] * fields['U'][:, -1] * data['p1_driven'][:, -1] / radius[:, -1]**2
        p_second[:, -1] = radius[:, -1]**2 * forcing / (fields['N'][:, -1] * fields['U'][:, -1])
        force_rate = model.node_weights[-1] * p_second[:, -1] - data['Gchi1'][:, -1]
        multiplier_rate = (force_rate - fields['L'][:, -1] * source['rho']) / fields['N'][:, -1]
        reservoir_second = -multiplier_rate * data['q'][:, -1] - source['multiplier'] * data['q1'][:, -1]
        energy_second = model.node_weights * (data['p1_driven']**2 + data['p'] * p_second) / radius**2 + radius**2 * data['d2']
        return dict(data, **second, p2=p_second, energy2=energy_second, rho1=force_rate, lambda1=multiplier_rate, reservoir_E2=reservoir_second)

    def density_second(self, radius):
        model = self.model
        index, offsets, active = model.layer_coordinates(radius)
        energy_second, reservoir_second = np.zeros(len(index)), np.zeros(len(index))
        if active.any():
            selected = np.flatnonzero(active)
            for lower in range(0, len(selected), 24):
                chunk = selected[lower:lower + 24]
                data = self.completed_layer(offsets[chunk])
                weight = shape_weight(offsets[chunk], model.shape) / model.width
                energy_second[chunk] = weight * data['energy2'][np.arange(len(chunk)), index[chunk]]
                reservoir_second[chunk] = weight * data['reservoir_E2'] * (index[chunk] == len(model.radii) - 1)
        return energy_second, reservoir_second

    def check_second(self, order=24):
        model = self.model
        radius, weights = model.cut_quadrature(order)
        fields = self.first_fields(radius)
        second = self.current_second(radius)
        epsilon2, sigma2 = self.density_second(radius)
        sigma = model.reservoir_density(radius)
        sigma1 = self.driver.density_rates(radius)[1]
        root_f, lapse, energy = fields['U'], fields['N'], fields['epsilon']
        root_first = -fields['mu1'] / (radius * root_f)
        root_second = -second['mu2'] / (radius * root_f) - fields['mu1']**2 / (radius**2 * root_f**3)
        fraction = (radius - model.radii[0]) / (model.radii[-1] - model.radii[0])
        tests = np.column_stack([fraction**degree for degree in range(6)])
        test_derivatives = np.column_stack([np.zeros_like(radius)] + [degree * fraction**(degree - 1) / (model.radii[-1] - model.radii[0]) for degree in range(1, 6)])
        endpoint_tests = np.array([[1., 0., 0., 0., 0., 0.], [1., 1., 1., 1., 1., 1.]])
        orientation = np.array([-1., 1.])
        endpoints = self.first_fields(model.radii[[0, -1]])
        endpoint_second = self.current_second(model.radii[[0, -1]])
        endpoint_root2 = -endpoint_second['mu2'] / (model.radii[[0, -1]] * endpoints['U']) - endpoints['mu1']**2 / (model.radii[[0, -1]]**2 * endpoints['U']**3)
        metric_density = ((1 - root_f**-2) * root_second + 2 * root_f**-3 * root_first**2) / (2 * model.coupling)
        metric_row = tests.T @ (weights * metric_density) + test_derivatives.T @ (weights * radius * root_second / model.coupling)
        metric_boundary = endpoint_tests.T @ (orientation * model.radii[[0, -1]] * endpoint_root2 / model.coupling)
        metric_row -= metric_boundary
        mass_gradient = model.coupling * (root_f**2 * energy + root_f * sigma)
        gravity_p2_row = -tests.T @ (weights * model.coupling * root_f**3 * (mass_gradient - fields['mu'] / radius) * fields['P1']**2)
        gravity_p2_row -= test_derivatives.T @ (weights * model.coupling * radius * root_f**5 * fields['P1']**2)
        gravity_p2_boundary = -endpoint_tests.T @ (orientation * model.coupling * model.radii[[0, -1]] * endpoints['U']**5 * endpoints['P1']**2)
        gravity_p2_row += gravity_p2_boundary
        scalar_base = tests.T @ (weights * (-root_second * energy - 2 * root_first * fields['epsilon1'] - root_f * epsilon2))
        scalar_chart = tests.T @ (weights * 2 * model.coupling**2 * root_f**5 * energy * fields['P1']**2)
        reservoir = tests.T @ (weights * (-sigma2 + model.coupling**2 * root_f**4 * sigma * fields['P1']**2))
        connection = tests.T @ (weights * (-fields['K'] * fields['c2'] / lapse + 2 * fields['L'] * fields['K'] * fields['g_r'] / lapse - 2 * second['K1'] * fields['g_r'] / lapse))
        constraint_second = metric_row + gravity_p2_row + scalar_base + scalar_chart + reservoir + connection
        ward = second['K1_r'] + 3 * fields['g_r'] * second['K1'] + 2 * fields['c2'] * fields['K']
        ward += lapse * root_f * (fields['L'] - fields['mu1'] / (radius * root_f**2)) * fields['epsilon1'] + lapse * root_f * epsilon2 + lapse * fields['L'] * sigma1 + lapse * sigma2
        return dict(R=radius, weights=weights, **fields, **second, epsilon2=epsilon2, sigma=sigma, sigma1=sigma1, sigma2=sigma2,
                    C2=constraint_second, ward1=ward, metric_C2=metric_row, gravity_P2_C2=gravity_p2_row,
                    scalar_C2=scalar_base, scalar_chart_C2=scalar_chart, reservoir_C2=reservoir, connection_C2=connection,
                    no_source_C2=constraint_second-reservoir, no_connection_C2=constraint_second-connection,
                    no_P_squared_C2=constraint_second-gravity_p2_row-scalar_chart,
                    no_radial_C2=constraint_second+metric_boundary-gravity_p2_boundary,
                    endpoint_P2=endpoints['P2'], endpoint_mu2=endpoint_second['mu2'], lapse_rate_slopes=self.lapse_slopes)
