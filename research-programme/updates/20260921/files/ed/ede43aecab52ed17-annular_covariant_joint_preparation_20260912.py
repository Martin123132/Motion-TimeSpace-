from pathlib import Path

import numpy as np
from scipy.linalg import solve

from annular_canonical_trace_context_20260911 import load_archive
from annular_canonical_trace_projection_stable_20260911 import GlobalPrimitive
from annular_covariant_scalar_action_20260912 import full_spatial_factors
from annular_cubic_lapse_final_boundary_20260912 import CubicContext


class JointPreparation:
    def __init__(self, common, branch):
        self.root = Path(common.root)
        self.context = CubicContext(common, branch)
        self.branch = branch
        self.intake = self.root / 'source-intake/navier-stokes/20260912'
        source = self.intake / 'annular-cubic-lapse-boundary-attempt07'
        raw = load_archive(source / (branch + '_corrected_data.npz'))
        self.data = {surface: {key.split('__', 1)[1]: value for key, value in raw.items() if key.startswith(surface + '__')} for surface in self.context.surfaces}
        self.saved = load_archive(source / (branch + '_corrected_initial_data.npz'))
        source = self.intake / 'annular-acceleration-trace-completion-attempt02'
        raw = load_archive(source / (branch + '_extended_mass_frames.npz'))
        self.frame = {surface: {kind: raw[surface + '__' + kind] for kind in ['q', 'qr', 'p']} for surface in self.data}
        source = self.intake / 'annular-covariant-scalar-source-jet-attempt01'
        self.previous = load_archive(source / (branch + '_source_jet_and_C0_only_preparation.npz'))
        self.mass_map = {surface: self.previous[surface + '_mass_variation_map'] for surface in self.data}
        self.radii = self.data['nodes']['R']
        self.spacing = self.context.basis.spacing
        self.node_weights = np.full(self.radii.size, self.spacing)
        self.node_weights[[0, -1]] /= 2
        self.scalar = self.data['nodes']['chi'].copy()
        self.momentum_seed = self.data['nodes']['pi'].copy()
        fraction = (self.radii - self.radii[0]) / (self.radii[-1] - self.radii[0])
        self.momentum_lifts = common.kinetic(self.radii)[0][:, None] * np.column_stack([1 - 3 * fraction**2 + 2 * fraction**3, 3 * fraction**2 - 2 * fraction**3])
        self.factors, self.sampling = full_spatial_factors(self.radii.size, branch != 'GR')
        self.factor, self.node = np.nonzero((self.factors != 0) | (self.sampling != 0))
        self.bpair = self.factors[self.factor, self.node]
        self.spair = self.sampling[self.factor, self.node]
        self.anchors = (self.sampling @ self.radii)[self.factor]
        self.targets = self.radii[self.node]
        self.amplitude = self.factors @ self.scalar
        self.nodal_d = self.sampling.T @ self.amplitude**2 / (2 * self.spacing)
        self.lapse_lifts = {surface: self.context.family.raw(data['R']) for surface, data in self.data.items()}
        self.pairings = {surface: self.frame[surface]['p'].T @ (weights[:, None] * self.frame[surface]['q']) for surface, weights in [('quad', self.context.weights), ('check', self.context.check_weights)]}
        self.clock = self.context.system.outer_clock
        self.reference = np.sqrt(2 / 3)

    def collect(self, values):
        result = np.zeros(self.factors.shape[0], dtype=values.dtype)
        np.add.at(result, self.factor, values)
        return result

    def scatter(self, values):
        result = np.zeros(self.radii.size, dtype=values.dtype)
        np.add.at(result, self.node, values)
        return result

    def fields(self, coefficients):
        fields = {}
        for surface, original in self.data.items():
            mass = original['mu'] + self.mass_map[surface] @ coefficients[:19]
            geometry = 1 - 2 * mass / original['R']
            fields[surface] = dict(original, mu=mass, F=geometry)
        if min(item['F'].real.min() for item in fields.values()) <= .1:
            raise ValueError('Nonpositive geometry trial.')
        normalization = self.clock * np.sqrt(fields['nodes']['F'][-1]) / self.data['nodes']['N'][-1]
        for surface in fields:
            fields[surface]['N'] = self.data[surface]['N'] * normalization
            fields[surface]['N_r'] = self.data[surface]['N_r'] * normalization
        momentum = self.momentum_seed + self.momentum_lifts @ coefficients[19:]
        energy = self.node_weights * momentum**2 / (2 * self.radii**2) + self.radii**2 * self.nodal_d
        return fields, momentum, energy

    def constraint(self, fields, energy, surface='quad'):
        weights = self.context.weights if surface == 'quad' else self.context.check_weights
        values, nodes = fields[surface], fields['nodes']
        root_f, node_root = np.sqrt(values['F']), np.sqrt(nodes['F'])
        residual = values['eta'].T @ (weights * (root_f + 1 / root_f - 2 * self.reference) / .2)
        residual += values['eta_r'].T @ (weights * values['R'] * (root_f - self.reference) / .1)
        residual -= nodes['eta'][-1] * self.radii[-1] * (node_root[-1] - self.reference) / .1
        residual += nodes['eta'][0] * self.radii[0] * (node_root[0] - self.reference) / .1
        return residual - nodes['eta'].T @ (node_root * energy)

    def mass_differential(self, fields, energy, mass_rate, node_rate, surface='quad'):
        weights = self.context.weights if surface == 'quad' else self.context.check_weights
        values, nodes = fields[surface], fields['nodes']
        result = values['eta'].T @ (weights * values['mu'] * mass_rate / (.1 * values['R']**2 * values['F']**1.5))
        result -= values['eta_r'].T @ (weights * mass_rate / (.1 * np.sqrt(values['F'])))
        result += nodes['eta'][-1] * node_rate[-1] / (.1 * np.sqrt(nodes['F'][-1]))
        result -= nodes['eta'][0] * node_rate[0] / (.1 * np.sqrt(nodes['F'][0]))
        result += nodes['eta'].T @ (energy * node_rate / (self.radii * np.sqrt(nodes['F'])))
        return result

    def metric_momentum(self, fields, energy, surface='quad'):
        weights = self.context.weights if surface == 'quad' else self.context.check_weights
        values, nodes = fields[surface], fields['nodes']
        regular = -values['N_r'] / (.1 * np.sqrt(values['F'])) + values['N'] * values['mu'] / (.1 * values['R']**2 * values['F']**1.5)
        nodal = nodes['N'] * energy / (self.radii * np.sqrt(nodes['F']))
        force = self.frame[surface]['q'].T @ (weights * regular) + self.frame['nodes']['q'].T @ nodal
        outer_load = (nodes['N'][-1] / np.sqrt(nodes['F'][-1]) - self.clock) / .1
        force += self.frame['nodes']['q'][-1] * outer_load
        coefficients = solve(self.pairings[surface].T, force)
        return coefficients, force, regular, nodal

    def apply_lapse(self, fields, energy):
        initial = self.metric_momentum(fields, energy)[0]
        baseline_trace = self.frame['nodes']['p'][[0, -1]] @ initial
        columns = []
        for column in range(2):
            trial = {surface: dict(values, N=self.lapse_lifts[surface][0][:, column], N_r=self.lapse_lifts[surface][1][:, column]) for surface, values in fields.items()}
            values, nodes = trial['quad'], trial['nodes']
            regular = -values['N_r'] / (.1 * np.sqrt(values['F'])) + values['N'] * values['mu'] / (.1 * values['R']**2 * values['F']**1.5)
            nodal = nodes['N'] * energy / (self.radii * np.sqrt(nodes['F']))
            force = self.frame['quad']['q'].T @ (self.context.weights * regular) + self.frame['nodes']['q'].T @ nodal
            coefficients = solve(self.pairings['quad'].T, force)
            columns.append(self.frame['nodes']['p'][[0, -1]] @ coefficients)
        response = np.column_stack(columns)
        amplitudes = solve(response, -baseline_trace)
        for surface in fields:
            fields[surface]['N'] = fields[surface]['N'] + self.lapse_lifts[surface][0] @ amplitudes
            fields[surface]['N_r'] = fields[surface]['N_r'] + self.lapse_lifts[surface][1] @ amplitudes
        if min(item['N'].real.min() for item in fields.values()) <= .1:
            raise ValueError('Boundary lapse solve leaves the positive chart.')
        return amplitudes, response

    def current(self, fields, momentum, momentum_rate, surface='quad'):
        order = 12 if surface == 'quad' else 16
        values, nodes = fields[surface], fields['nodes']
        c_p = .1 * np.sqrt(values['F']) / values['N']
        generator = c_p * (self.frame[surface]['p'] @ momentum_rate)
        primitive = GlobalPrimitive(self.context.knots, generator, order)
        endpoint_g = primitive.evaluate(self.targets)
        anchor_g = primitive.evaluate(self.anchors)
        endpoint_J = np.exp(endpoint_g - anchor_g)
        if np.max(abs((endpoint_g - anchor_g).real)) > 30:
            raise ValueError('Unbounded time-link trial.')
        coefficient = self.radii**2 * nodes['N'] * np.sqrt(nodes['F'])
        velocity = coefficient * momentum / self.radii**4
        density = self.collect(self.spair * endpoint_J * coefficient[self.node])
        amplitude_first = self.collect(self.bpair * endpoint_J * velocity[self.node])
        current = self.amplitude[self.factor] * (self.spair * coefficient[self.node] * amplitude_first[self.factor] - self.bpair * velocity[self.node] * density[self.factor]) / self.spacing
        scalar_force = self.scatter(-self.bpair * self.amplitude[self.factor] * density[self.factor] / (self.spacing * endpoint_J))
        nodal_d_first = self.scatter(self.spair * self.amplitude[self.factor] * amplitude_first[self.factor] / (self.spacing * endpoint_J))
        global_current = current * np.exp(endpoint_g + anchor_g)

        def cell_coefficients(fraction):
            probes = self.radii[:-1] + fraction * np.diff(self.radii)
            hits = (probes[:, None] > np.minimum(self.targets, self.anchors)) & (probes[:, None] < np.maximum(self.targets, self.anchors))
            return hits @ (global_current * np.sign(self.targets - self.anchors))

        cell_current = cell_coefficients(.371)
        carriers, kernels = {}, {}
        for name, item in fields.items():
            cells = np.clip(np.searchsorted(self.radii, item['R'], side='right') - 1, 0, self.radii.size - 2)
            carrier = np.exp(-2 * primitive.evaluate(item['R']))
            kernels[name] = carrier * cell_current[cells]
            carriers[name] = .1 * np.sqrt(item['F']) / item['N'] * carrier
        return {'primitive': primitive, 'K': kernels, 'carriers': carriers, 'cell_current': cell_current, 'cell_anchor_error': abs(cell_current - cell_coefficients(.729)).max(), 'anchor_error': abs(self.collect(endpoint_J * current)).max(), 'J': endpoint_J, 'current': current, 'global_current': global_current, 'Gchi': scalar_force, 'd_first': nodal_d_first, 'q': velocity, 'generator': generator}

    def evaluate(self, coefficients, surface='quad', inferred_ports=True):
        fields, momentum, energy = self.fields(coefficients)
        lapse_amplitudes, lapse_response = self.apply_lapse(fields, energy)
        momentum_rate, force, regular, nodal = self.metric_momentum(fields, energy, surface)
        current = self.current(fields, momentum, momentum_rate, surface)
        weights = self.context.weights if surface == 'quad' else self.context.check_weights
        values, nodes = fields[surface], fields['nodes']
        raw_mu = -.1 * np.sqrt(values['F']) / values['N'] * current['K'][surface]
        raw_nodes = -.1 * np.sqrt(nodes['F']) / nodes['N'] * current['K']['nodes']
        mass_rate = solve(self.pairings[surface], self.frame[surface]['p'].T @ (weights * raw_mu))
        mu_first = self.frame[surface]['q'] @ mass_rate
        mu_nodes = self.frame['nodes']['q'] @ mass_rate
        p_first_free = current['Gchi'] / self.node_weights
        rate = self.mass_differential(fields, energy, mu_first, mu_nodes, surface)
        rate -= nodes['eta'].T @ (np.sqrt(nodes['F']) * (self.node_weights * momentum * p_first_free / self.radii**2 + self.radii**2 * current['d_first']))
        rate -= values['eta'].T @ (weights * current['K'][surface] * current['generator'] / values['N'])
        port_response = -nodes['eta'][[0, -1]].T * (current['q'][[0, -1]] / nodes['N'][[0, -1]])
        rho = np.zeros(self.radii.size, dtype=rate.dtype)
        if inferred_ports:
            rho[[0, -1]] = solve(port_response[[0, 16]], -rate[[0, 16]])
        else:
            rho = self.previous['prescribed_port_force'].copy()
        p_first = (current['Gchi'] + rho) / self.node_weights
        full_rate = rate + port_response @ rho[[0, -1]]
        projection_work = self.mass_differential(fields, energy, mu_first - raw_mu, mu_nodes - raw_nodes, surface)
        test = values['eta'] * (raw_mu / values['N'])[:, None]
        node_test = nodes['eta'] * (raw_nodes / nodes['N'])[:, None]
        metric_work = test.T @ (weights * (regular - self.frame[surface]['p'] @ momentum_rate)) + node_test.T @ nodal
        source_work = -nodes['eta'].T @ (rho * current['q'] / nodes['N'])
        boundary_K = np.array([-1., 1.]) * (self.radii[[0, -1]]**2 * nodes['N'][[0, -1]] * np.sqrt(nodes['F'][[0, -1]]) * current['d_first'][[0, -1]] + current['Gchi'][[0, -1]] * current['q'][[0, -1]])
        residual = np.concatenate([self.constraint(fields, energy, surface), [(raw_nodes[0] - self.saved['boundary_velocity'][0]) / .02, current['q'][-1] - self.saved['boundary_velocity'][2]]])
        return {'fields': fields, 'momentum': momentum, 'energy': energy, 'residual': residual, 'lapse_amplitudes': lapse_amplitudes, 'lapse_response': lapse_response, 'P_coeff': momentum_rate, 'P_force': force, 'P_nodes': self.frame['nodes']['p'] @ momentum_rate, 'mu_coeff': mass_rate, 'mu_first': mu_first, 'mu_nodes': mu_nodes, 'raw_mu': raw_mu, 'raw_nodes': raw_nodes, 'p_first': p_first, 'rho': rho, 'C1': full_rate, 'C1_no_ports': rate, 'current': current, 'projection_work': projection_work, 'metric_work': metric_work, 'source_work': source_work, 'Ward_error': full_rate - projection_work - metric_work - source_work, 'boundary_K_error': boundary_K - current['K']['nodes'][[0, -1]]}

    def solve(self):
        coefficients = np.concatenate([self.previous['mass_change_coefficients'], np.zeros(2)])
        history = []
        for iteration in range(14):
            result = self.evaluate(coefficients)
            merit = float(abs(result['residual']).max())
            history.append({'iteration': iteration, 'residual': merit, 'momentum_lifts': coefficients[19:].tolist()})
            if merit < 3e-12:
                return coefficients, result, history
            jacobian = np.column_stack([self.evaluate(coefficients + 1e-25j * direction)['residual'].imag / 1e-25 for direction in np.eye(21)])
            history[-1]['jacobian_condition'] = float(np.linalg.cond(jacobian))
            direction = solve(jacobian, -result['residual'])
            for exponent in range(16):
                trial = coefficients + direction * 2.**(-exponent)
                try:
                    error = abs(self.evaluate(trial)['residual']).max()
                except ValueError:
                    continue
                if error < merit:
                    coefficients = trial
                    break
            else:
                raise RuntimeError('Joint Newton line search failed: ' + repr(history))
        raise RuntimeError('Joint Newton iteration budget exhausted: ' + repr(history))
