import numpy as numerical
from scipy.linalg import solve

from annular_canonical_trace_context_20260911 import load_archive
from annular_cubic_lapse_final_boundary_20260912 import CubicContext, GRAVITY_REFERENCE_ROOT
from annular_cubic_lapse_reference_gravity_20260912 import evaluate_cubic_initial
from annular_gram_joint_action_20260909 import gram_matrices
from annular_metric_flux_jets_20260909 import SecondJet


class FrozenSecondJet:
    def __init__(self, common, branch, higher=False):
        self.context = CubicContext(common, branch)
        self.branch = branch
        self.gram = branch != 'GR'
        self.surface = 'check' if higher else 'quad'
        self.link_surface = 'links_check' if higher else 'links'
        self.weights = self.context.check_weights if higher else self.context.weights
        self.links = self.context.check_links if higher else self.context.links
        self.basis = self.context.basis
        source = common.root / 'source-intake/navier-stokes/20260912/annular-cubic-lapse-boundary-attempt07'
        label = branch + '_corrected'
        raw_data = load_archive(source / (label + '_data.npz'))
        raw_frames = load_archive(source / (label + '_frames.npz'))
        self.data = {surface: {key.split('__', 1)[1]: value for key, value in raw_data.items() if key.startswith(surface + '__')} for surface in self.context.surfaces}
        self.frames = {phase: {surface: {kind: raw_frames[phase + '__' + surface + '__' + kind] for kind in ['q', 'qr', 'p']} for surface in self.context.surfaces} for phase in ['mass', 'scalar']}
        self.saved = load_archive(source / (label + '_initial_data.npz'))
        self.first = evaluate_cubic_initial(self.frames['mass'], self.frames['scalar'], self.data, self.basis, self.weights, self.links, self.gram, self.context.system.outer_clock, surface=self.surface, link_surface=self.link_surface)
        self.rates = {surface: {
            'mu': self.frames['mass'][surface]['q'] @ self.first['mass_rate_coeff'],
            'mu_r': self.frames['mass'][surface]['qr'] @ self.first['mass_rate_coeff'],
            'P': self.frames['mass'][surface]['p'] @ self.first['P_rate_coeff'],
            'chi': self.frames['scalar'][surface]['q'] @ self.first['q_coeff'],
            'w': self.frames['scalar'][surface]['qr'] @ self.first['q_coeff'],
            'pi': self.frames['scalar'][surface]['p'] @ self.first['pi_rate_coeff'],
        } for surface in self.context.surfaces}
        self.factors, self.sampling = gram_matrices(self.basis.radii.size)
        self.prepare_links()

    def prepare_links(self):
        nodes, values = self.data['nodes'], self.data[self.link_surface]
        links, rates = self.links, self.rates[self.link_surface]
        self.connection_factor = .1 * numerical.sqrt(values['F']) / values['N']
        self.jacobian = numerical.exp(links.integrate(self.connection_factor * rates['P']))
        self.partial_jacobian = numerical.exp(links.partial(self.connection_factor * rates['P']))
        self.coefficient = nodes['R']**2 * nodes['N'] * numerical.sqrt(nodes['F'])
        self.amplitude = self.factors @ nodes['chi']
        self.density = links.collect(links.sweight * self.jacobian * self.coefficient[links.node])
        self.amplitude_first = links.collect(links.tweight * self.jacobian * self.rates['nodes']['chi'][links.node])
        self.current = self.amplitude[links.factor] * (links.sweight * self.coefficient[links.node] * self.amplitude_first[links.factor] - links.tweight * self.rates['nodes']['chi'][links.node] * self.density[links.factor]) / self.basis.spacing
        self.nodal_density = self.sampling.T @ self.amplitude**2 / (2 * self.basis.spacing)
        self.nodal_density_first = numerical.zeros_like(nodes['R'])
        numerical.add.at(self.nodal_density_first, links.node, links.sweight * self.amplitude[links.factor] * self.amplitude_first[links.factor] / (self.basis.spacing * self.jacobian))

    def transport_load(self, test, multiplier, derivative=None):
        links = self.links
        if derivative is None:
            integral = links.integrate(test * (multiplier / self.partial_jacobian**2)[:, None])
            return integral.T @ (self.current * self.jacobian)
        current_first, endpoint_second, partial_second = derivative
        first_integral = links.integrate(test * (multiplier / self.partial_jacobian**3)[:, None])
        second_integral = links.integrate(test * (multiplier * partial_second / self.partial_jacobian**4)[:, None])
        return first_integral.T @ (current_first * self.jacobian + self.current * endpoint_second) - 2 * second_integral.T @ (self.current * self.jacobian)

    def candidate(self):
        nodes, rates = self.data['nodes'], self.rates['nodes']
        energy_first = nodes['pi'] * rates['pi'] / nodes['R']**2 + nodes['R']**2 * nodes['w'] * rates['w']
        desired = .1 * energy_first / nodes['R'] + rates['mu'] / (nodes['R']**2 * nodes['F']**2)
        scale = -rates['mu'][-1] / (nodes['R'][-1] * nodes['F'][-1])
        amplitude = (nodes['N'] * desired)[[0, -1]]
        values = scale * nodes['N'] + self.context.family.raw(nodes['R'])[0] @ amplitude
        coefficients = numerical.zeros(19)
        extra_raw = scale * self.saved['lapse_boundary_amplitudes'] + amplitude
        coefficients[-2:] = solve(self.context.family.transform, extra_raw)
        coefficients[:17] = values - self.data['nodes']['eta'][:, -2:] @ coefficients[-2:]
        return coefficients

    def evaluate(self, lapse_rate_coefficients):
        surface, link_surface = self.surface, self.link_surface
        values, nodes, link_values = self.data[surface], self.data['nodes'], self.data[link_surface]
        rates, node_rates, link_rates = self.rates[surface], self.rates['nodes'], self.rates[link_surface]
        mass, scalar = self.frames['mass'][surface], self.frames['scalar'][surface]
        mass_nodes, scalar_nodes = self.frames['mass']['nodes'], self.frames['scalar']['nodes']
        lapse_first = {name: data['eta'] @ lapse_rate_coefficients for name, data in self.data.items()}
        lapse_radial_first = {name: data['eta_r'] @ lapse_rate_coefficients for name, data in self.data.items()}
        radius, weights, links = values['R'], self.weights, self.links
        geometry = SecondJet(values['F'], -2 * rates['mu'] / radius)
        lapse = SecondJet(values['N'], lapse_first[surface])
        lapse_r = SecondJet(values['N_r'], lapse_radial_first[surface])
        mu = SecondJet(values['mu'], rates['mu'])
        momentum = SecondJet(values['pi'], rates['pi'])
        gradient = SecondJet(values['w'], rates['w'])
        energy = momentum * momentum / (2 * radius**2) + radius**2 * gradient * gradient / 2
        force = lapse * energy / (radius * geometry**.5) - lapse_r / (.1 * geometry**.5) + lapse * mu / (.1 * radius**2 * geometry**1.5)
        force_first = force.first + .3 * values['N'] * numerical.sqrt(values['F']) * rates['P'] * values['pi'] * values['w'] / radius
        mass_force_first = mass['q'].T @ (weights * force_first)
        clock_first = lapse_first['nodes'][-1] / numerical.sqrt(nodes['F'][-1]) + nodes['N'][-1] * node_rates['mu'][-1] / (nodes['R'][-1] * nodes['F'][-1]**1.5)
        mass_force_first += mass_nodes['q'][-1] * clock_first / .1
        if self.gram:
            nodal_mass_first = nodes['R'] * (self.nodal_density_first * nodes['N'] / numerical.sqrt(nodes['F']) + self.nodal_density * (lapse_first['nodes'] / numerical.sqrt(nodes['F']) + nodes['N'] * node_rates['mu'] / (nodes['R'] * nodes['F']**1.5)))
            mass_force_first += mass_nodes['q'].T @ nodal_mass_first
            mass_force_first += self.transport_load(self.frames['mass'][link_surface]['q'], -.1 * link_rates['P'] / (link_values['R'] * link_values['N'] * numerical.sqrt(link_values['F'])))
        P_second_coeff = solve(self.first['mass_pair'].T, mass_force_first)
        scalar_velocity = lapse * geometry**.5 * momentum / radius**2
        scalar_velocity_first = scalar_velocity.first + .1 * values['N'] * values['F']**1.5 * rates['P'] * values['w']
        chi_second_coeff = solve(self.first['scalar_pair'], scalar['p'].T @ (weights * scalar_velocity_first))
        P_second_links = self.frames['mass'][link_surface]['p'] @ P_second_coeff
        chi_second_nodes = scalar_nodes['q'] @ chi_second_coeff
        connection_second = self.connection_factor * (P_second_links - 2 * (link_rates['mu'] / (link_values['R'] * link_values['F']) + lapse_first[link_surface] / link_values['N']) * link_rates['P'])
        endpoint_second = self.jacobian * links.integrate(connection_second * self.partial_jacobian)
        partial_second = self.partial_jacobian * links.partial(connection_second * self.partial_jacobian)
        coefficient_first = nodes['R']**2 * (lapse_first['nodes'] * numerical.sqrt(nodes['F']) - nodes['N'] * node_rates['mu'] / (nodes['R'] * numerical.sqrt(nodes['F'])))
        density_first = links.collect(links.sweight * (endpoint_second * self.coefficient[links.node] + self.jacobian**2 * coefficient_first[links.node]))
        amplitude_second = links.collect(links.tweight * (endpoint_second * node_rates['chi'][links.node] + self.jacobian**2 * chi_second_nodes[links.node]))
        current_first = self.amplitude_first[links.factor] * (links.sweight * self.coefficient[links.node] * self.amplitude_first[links.factor] - links.tweight * node_rates['chi'][links.node] * self.density[links.factor]) / self.basis.spacing
        current_first = current_first + self.amplitude[links.factor] * (links.sweight * (self.jacobian * coefficient_first[links.node] * self.amplitude_first[links.factor] + self.coefficient[links.node] * amplitude_second[links.factor]) - links.tweight * (self.jacobian * chi_second_nodes[links.node] * self.density[links.factor] + node_rates['chi'][links.node] * density_first[links.factor])) / self.basis.spacing
        derivative = current_first, endpoint_second, partial_second
        gram_scalar_first = numerical.zeros(nodes['R'].shape, dtype=numerical.result_type(lapse_rate_coefficients))
        gram_density_second = numerical.zeros_like(gram_scalar_first)
        gram_P_first = numerical.zeros(mass['p'].shape[1], dtype=gram_scalar_first.dtype)
        if self.gram:
            scalar_load_first = -links.tweight / (self.basis.spacing * self.jacobian**2) * (self.amplitude_first[links.factor] * self.density[links.factor] + self.amplitude[links.factor] * density_first[links.factor] - self.amplitude[links.factor] * self.density[links.factor] * endpoint_second / self.jacobian)
            numerical.add.at(gram_scalar_first, links.node, scalar_load_first)
            density_load_second = links.sweight / self.basis.spacing * ((self.amplitude_first[links.factor]**2 + self.amplitude[links.factor] * amplitude_second[links.factor]) / self.jacobian**2 - self.amplitude[links.factor] * self.amplitude_first[links.factor] * endpoint_second / self.jacobian**3)
            numerical.add.at(gram_density_second, links.node, density_load_second)
            gram_P_first = self.transport_load(self.frames['mass'][link_surface]['p'], self.connection_factor, derivative)
            gram_P_first += self.transport_load(self.frames['mass'][link_surface]['p'], self.connection_factor * (-link_rates['mu'] / (link_values['R'] * link_values['F']) - lapse_first[link_surface] / link_values['N']))
            gram_P_first += mass_nodes['p'].T @ (2 * .1**2 * nodes['R']**2 * nodes['N'] * nodes['F']**2.5 * self.nodal_density * node_rates['P'])
        scalar_flux = lapse * geometry**.5 * radius**2 * gradient
        scalar_flux_first = scalar_flux.first + .1 * values['N'] * values['F']**1.5 * rates['P'] * values['pi']
        flux_nodes_first = nodes['R']**2 * (lapse_first['nodes'] * numerical.sqrt(nodes['F']) * nodes['w'] - nodes['N'] * node_rates['mu'] * nodes['w'] / (nodes['R'] * numerical.sqrt(nodes['F'])) + nodes['N'] * numerical.sqrt(nodes['F']) * node_rates['w'])
        flux_nodes_first += .1 * nodes['N'] * nodes['F']**1.5 * node_rates['P'] * nodes['pi']
        pi_force_first = -scalar['qr'].T @ (weights * scalar_flux_first) + scalar_nodes['q'].T @ gram_scalar_first
        pi_force_first += scalar_nodes['q'][0] * (-flux_nodes_first[0] - gram_scalar_first[0]) + scalar_nodes['q'][-1] * (flux_nodes_first[-1] - gram_scalar_first[-1])
        pi_second_coeff = solve(self.first['scalar_pair'].T, pi_force_first)
        mass_velocity = .1 * lapse * geometry**1.5 * momentum * gradient
        mass_velocity_first = mass_velocity.first + .1 * (radius * values['F']**2.5 * values['N_r'] + values['N'] * values['F']**1.5 * (values['mu_r'] - values['mu'] / radius)) * rates['P']
        mass_load_first = mass['p'].T @ (weights * mass_velocity_first) - gram_P_first
        radial_boundary_first = .1 * nodes['R'] * nodes['N'] * nodes['F']**2.5 * node_rates['P']
        mass_load_first += mass_nodes['p'][-1] * radial_boundary_first[-1] - mass_nodes['p'][0] * radial_boundary_first[0]
        mu_second_coeff = solve(self.first['mass_pair'], mass_load_first)
        second = {'mu': mu_second_coeff, 'P': P_second_coeff, 'chi': chi_second_coeff, 'pi': pi_second_coeff}
        constraint_jet = self.constraint_jet(second, gram_density_second, lapse_first, P_second_links, derivative)
        node_second = {'mu': mass_nodes['q'] @ mu_second_coeff, 'P': mass_nodes['p'] @ P_second_coeff, 'chi': chi_second_nodes, 'pi': scalar_nodes['p'] @ pi_second_coeff}
        residual = numerical.concatenate([constraint_jet.second, node_second['P'][[0, -1]], [clock_first]])
        return {'second': second, 'nodes': node_second, 'constraint': constraint_jet.value, 'constraint_first': constraint_jet.first, 'constraint_second': constraint_jet.second, 'compatibility': residual, 'inferred_drive_accelerations': numerical.array([node_second['mu'][0], node_second['chi'][-1]]), 'lapse_rate_coefficients': lapse_rate_coefficients, 'endpoint_J': self.jacobian, 'endpoint_Tss': endpoint_second, 'partial_Tss': partial_second, 'current_first': current_first, 'gram_scalar_first': gram_scalar_first, 'gram_density_second': gram_density_second, 'gram_P_first': gram_P_first, 'clock_first': clock_first, 'weighted_current_first_identity': links.collect(endpoint_second * self.current + self.jacobian * current_first), 'Cdot_replay_error': float(abs(constraint_jet.first - self.first['constraint_rate']).max())}

    def constraint_jet(self, second, density_second, lapse_first, P_second_links, derivative):
        values, nodes = self.data[self.surface], self.data['nodes']
        rates, node_rates = self.rates[self.surface], self.rates['nodes']
        mass, scalar = self.frames['mass'][self.surface], self.frames['scalar'][self.surface]
        mass_nodes = self.frames['mass']['nodes']
        radius, weights = values['R'], self.weights
        mu = SecondJet(values['mu'], rates['mu'], mass['q'] @ second['mu'])
        geometry = 1 - 2 * mu / radius
        root_f = geometry**.5
        mass_r = SecondJet(values['mu_r'], rates['mu_r'], mass['qr'] @ second['mu'])
        momentum = SecondJet(values['pi'], rates['pi'], scalar['p'] @ second['pi'])
        gradient = SecondJet(values['w'], rates['w'], scalar['qr'] @ second['chi'])
        shift = SecondJet(numerical.zeros_like(radius), rates['P'], mass['p'] @ second['P'])
        energy = momentum * momentum / (2 * radius**2) + radius**2 * gradient * gradient / 2
        density = (root_f + 1 / root_f - 2 * GRAVITY_REFERENCE_ROOT) / .2 - root_f * energy - .1 * geometry**1.5 * shift * momentum * gradient - .05 * geometry**1.5 * (mass_r - mu / radius) * shift * shift
        radial_density = radius * (root_f - GRAVITY_REFERENCE_ROOT) / .1 - .05 * radius * geometry**2.5 * shift * shift
        result = (density * weights).mapped(values['eta'].T) + (radial_density * weights).mapped(values['eta_r'].T)
        node_mu = SecondJet(nodes['mu'], node_rates['mu'], mass_nodes['q'] @ second['mu'])
        node_f = 1 - 2 * node_mu / nodes['R']
        node_shift = SecondJet(numerical.zeros_like(nodes['R']), node_rates['P'], mass_nodes['p'] @ second['P'])
        boundary = nodes['R'] * (node_f**.5 - GRAVITY_REFERENCE_ROOT) / .1 + .05 * nodes['R'] * node_f**2.5 * node_shift * node_shift
        result -= boundary.selected(-1) * nodes['eta'][-1] - boundary.selected(0) * nodes['eta'][0]
        if self.gram:
            density_jet = SecondJet(self.nodal_density, self.nodal_density_first, density_second)
            node_coefficient = nodes['R']**2 * node_f**.5 * (1 - .1**2 * node_f * node_f * node_shift * node_shift)
            result -= (density_jet * node_coefficient).mapped(nodes['eta'].T)
            link_values, link_rates = self.data[self.link_surface], self.rates[self.link_surface]
            first_multiplier = -self.connection_factor * link_rates['P'] / link_values['N']
            second_multiplier = -self.connection_factor / link_values['N'] * (P_second_links + 2 * (-link_rates['mu'] / (link_values['R'] * link_values['F']) - 2 * lapse_first[self.link_surface] / link_values['N']) * link_rates['P'])
            first = self.transport_load(link_values['eta'], first_multiplier)
            second_transport = self.transport_load(link_values['eta'], second_multiplier) + 2 * self.transport_load(link_values['eta'], first_multiplier, derivative)
            result += SecondJet(numerical.zeros(19), first, second_transport)
        return result
