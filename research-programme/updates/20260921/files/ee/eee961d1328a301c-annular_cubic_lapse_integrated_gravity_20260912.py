import numpy as numerical
from scipy.linalg import solve

from annular_cubic_lapse_nodal_trace_20260912 import CubicContext
from annular_cubic_lapse_boundary_polynomial_20260912 import CubicPreparation as BasePreparation, CubicFields
from annular_canonical_trace_projection_stable_20260911 import kernel_family, trace_extension
from annular_gram_joint_action_20260909 import gram_matrices


class CubicPreparation(BasePreparation):
    def mass_equations(self, selected):
        context = self.context
        physical = CubicFields(context, selected)
        values, nodes = physical.evaluate(context.points), physical.evaluate(context.basis.radii)
        radius, weights, geometry = context.points, context.weights, values['F']
        if min(numerical.real(geometry).min(), numerical.real(nodes['F']).min()) <= .1:
            raise ValueError('Mass trial leaves the positive chart.')
        root_f, node_root = numerical.sqrt(geometry), numerical.sqrt(nodes['F'])
        energy = values['pi']**2 / (2 * radius**2) + radius**2 * values['w']**2 / 2
        eta_r = context.family.evaluate(context.points)[1]
        constraint = self.eta.T @ (weights * ((root_f + 1 / root_f - 2) / .2 - root_f * energy))
        constraint += eta_r.T @ (weights * radius * (root_f - 1) / .1)
        constraint -= self.eta_nodes[-1] * context.basis.radii[-1] * (node_root[-1] - 1) / .1
        constraint += self.eta_nodes[0] * context.basis.radii[0] * (node_root[0] - 1) / .1
        constraint -= self.eta_nodes.T @ (context.basis.radii**2 * node_root * self.gram_density)
        coefficient = values['mu'] / (.1 * radius**2 * geometry**1.5) + energy / (radius * root_f)
        derivative = self.eta.T @ (weights[:, None] * coefficient[:, None] * self.mass_map[:, 1:])
        derivative -= eta_r.T @ ((weights / (.1 * root_f))[:, None] * self.mass_map[:, 1:])
        derivative += numerical.outer(self.eta_nodes[-1], self.mass_nodes[-1, 1:]) / (.1 * node_root[-1])
        derivative -= numerical.outer(self.eta_nodes[0], self.mass_nodes[0, 1:]) / (.1 * node_root[0])
        derivative += self.eta_nodes.T @ ((context.basis.radii * self.gram_density / node_root)[:, None] * self.mass_nodes[:, 1:])
        return constraint, derivative

    def evaluate(self, amplitudes):
        self.calls += 1
        selected = self.candidate(amplitudes)
        history = self.project_mass(selected)
        context = self.context
        data, frames, completion = context.build(selected)
        baseline = evaluate_cubic_initial(frames['mass'], frames['scalar'], data, context.basis, context.weights, context.links, context.include_gram, context.system.outer_clock)
        family, unused_primitive, unused_carrier = kernel_family(context, data, frames['mass'], baseline['P_rate_coeff'])
        extended, diagnostics = trace_extension(context, frames['mass'], family)
        actual = evaluate_cubic_initial(extended, frames['scalar'], data, context.basis, context.weights, context.links, context.include_gram, context.system.outer_clock)
        nodes = data['nodes']
        parent_inner = .1 * nodes['N'][0] * nodes['F'][0]**1.5 * nodes['pi'][0] * nodes['w'][0]
        parent_inner += .1 * numerical.sqrt(nodes['F'][0]) * actual['q_nodes'][0] * actual['gram_scalar'][0] / nodes['N'][0]
        bulk_coefficient = .1 * nodes['R'][0]**2 * nodes['F'][0] * nodes['w'][0]
        residual = numerical.array([(parent_inner - selected['boundary_velocity'][0]) / bulk_coefficient, actual['q_nodes'][-1] - selected['boundary_velocity'][2]])
        count = context.basis.radii.size
        selected['state'][:count] = selected['mass_coefficients'][1:self.face_count]
        selected['state'][count:2 * count] = selected['pi_coefficients'][:count]
        selected['state'][-3:] = actual['reactions']
        return {'residual': residual, 'saved': selected, 'data': data, 'frames': {'mass': extended, 'scalar': frames['scalar']}, 'baseline': baseline, 'actual': actual, 'mass_history': history, 'completion': completion, 'extension': diagnostics, 'parent_inner_mass_rate': float(parent_inner)}


def evaluate_cubic_initial(frame_mass, frame_scalar, data, basis, weights, links, gram, clock, reactions=None, surface='quad', link_surface='links'):
    radius = data[surface]['R']
    values = data[surface]
    nodes = data['nodes']
    mass_maps, scalar_maps = frame_mass[surface], frame_scalar[surface]
    mass_nodes, scalar_nodes = frame_mass['nodes']['q'], frame_scalar['nodes']['q']
    mass_pair = mass_maps['p'].T @ (weights[:, None] * mass_maps['q'])
    scalar_pair = scalar_maps['p'].T @ (weights[:, None] * scalar_maps['q'])
    geometry, lapse = values['F'], values['N']
    energy = values['pi']**2 / (2 * radius**2) + radius**2 * values['w']**2 / 2
    mass_density = lapse * energy / (radius * numerical.sqrt(geometry)) - values['N_r'] / (.1 * numerical.sqrt(geometry)) + lapse * values['mu'] / (.1 * radius**2 * geometry**1.5)
    mass_force = mass_maps['q'].T @ (weights * mass_density) + (nodes['N'][-1] / numerical.sqrt(nodes['F'][-1]) - clock) / .1 * mass_nodes[-1] - nodes['N'][0] / (.1 * numerical.sqrt(nodes['F'][0])) * mass_nodes[0]
    factors, sampling = gram_matrices(basis.radii.size)
    amplitude = factors @ nodes['chi']
    gram_density = sampling.T @ amplitude**2 / (2 * basis.spacing)
    mass_reaction = nodes['N'][0] / (.1 * numerical.sqrt(nodes['F'][0])) if reactions is None else reactions[0]
    mass_force += mass_reaction * mass_nodes[0]
    if gram:
        mass_force += mass_nodes.T @ (basis.radii * nodes['N'] * gram_density / numerical.sqrt(nodes['F']))
    momentum_rate = solve(mass_pair.T, mass_force)
    q_coeff = solve(scalar_pair, scalar_maps['p'].T @ (weights * lapse * numerical.sqrt(geometry) * values['pi'] / radius**2))
    q_nodes = scalar_nodes @ q_coeff
    gram_p_force = numerical.zeros(frame_mass[surface]['p'].shape[1])
    gram_scalar = numerical.zeros(basis.radii.size)
    density_time = numerical.zeros(basis.radii.size)
    transport = numerical.zeros(data['nodes']['eta'].shape[1])
    endpoint_log = numerical.zeros(links.node.size)
    if gram:
        link_values = data[link_surface]
        momentum_link = frame_mass[link_surface]['p']
        momentum_time = momentum_link @ momentum_rate
        generator = .1 * numerical.sqrt(link_values['F']) * momentum_time / link_values['N']
        endpoint_log, partial_log = links.integrate(generator), links.partial(generator)
        if max(abs(endpoint_log).max(), abs(partial_log).max()) > 50:
            raise ValueError('Completed phase jet leaves the bounded time-link chart.')
        endpoint, partial = numerical.exp(endpoint_log), numerical.exp(partial_log)
        coefficient = basis.radii**2 * nodes['N'] * numerical.sqrt(nodes['F'])
        density = links.collect(links.sweight * endpoint * coefficient[links.node])
        amplitude_time = links.collect(links.tweight * endpoint * q_nodes[links.node])
        current = amplitude[links.factor] * (links.sweight * coefficient[links.node] * amplitude_time[links.factor] - links.tweight * q_nodes[links.node] * density[links.factor]) / basis.spacing
        weighted_current = current * endpoint
        kernel = links.integrate(momentum_link * (.1 * numerical.sqrt(link_values['F']) / (link_values['N'] * partial**2))[:, None])
        gram_p_force = kernel.T @ weighted_current
        numerical.add.at(gram_scalar, links.node, -links.tweight * amplitude[links.factor] * density[links.factor] / (basis.spacing * endpoint))
        numerical.add.at(density_time, links.node, links.sweight * amplitude[links.factor] * amplitude_time[links.factor] / (basis.spacing * endpoint))
        node_values = data[link_surface]['eta']
        kernel_time = links.integrate(node_values * (.1 * numerical.sqrt(link_values['F']) * momentum_time / (link_values['N']**2 * partial**2))[:, None])
        transport = -(kernel_time.T @ weighted_current)
    scalar_flux_endpoints = basis.radii[[0, -1]]**2 * nodes['N'][[0, -1]] * numerical.sqrt(nodes['F'][[0, -1]]) * nodes['w'][[0, -1]]
    actual_reactions = numerical.array([mass_reaction, -scalar_flux_endpoints[0] - gram_scalar[0], scalar_flux_endpoints[1] - gram_scalar[-1]]) if reactions is None else reactions
    scalar_force = -(scalar_maps['qr'].T @ (weights * lapse * numerical.sqrt(geometry) * radius**2 * values['w'])) + scalar_nodes.T @ gram_scalar
    scalar_force += scalar_nodes[0] * actual_reactions[1] + scalar_nodes[-1] * actual_reactions[2]
    pi_rate = solve(scalar_pair.T, scalar_force)
    mass_rate = solve(mass_pair, mass_maps['p'].T @ (weights * .1 * lapse * geometry**1.5 * values['pi'] * values['w']) - gram_p_force)
    physical_mass_rate, physical_mass_rate_r = mass_maps['q'] @ mass_rate, mass_maps['qr'] @ mass_rate
    physical_pi_rate, physical_momentum_rate = scalar_maps['p'] @ pi_rate, mass_maps['p'] @ momentum_rate
    physical_q, physical_q_r = scalar_maps['q'] @ q_coeff, scalar_maps['qr'] @ q_coeff
    coefficient = values['mu'] / (.1 * radius**2 * geometry**1.5) + energy / (radius * numerical.sqrt(geometry))
    density = coefficient * physical_mass_rate
    density -= numerical.sqrt(geometry) * values['pi'] * physical_pi_rate / radius**2 + radius**2 * numerical.sqrt(geometry) * values['w'] * physical_q_r + .1 * geometry**1.5 * values['pi'] * values['w'] * physical_momentum_rate
    lapse_tests = data[surface]['eta']
    gram_rate = data['nodes']['eta'].T @ (basis.radii * gram_density * (mass_nodes @ mass_rate) / numerical.sqrt(nodes['F']) - basis.radii**2 * numerical.sqrt(nodes['F']) * density_time) + transport if gram else numerical.zeros(data['nodes']['eta'].shape[1])
    constraint_rate = lapse_tests.T @ (weights * density) - values['eta_r'].T @ (weights * physical_mass_rate / (.1 * numerical.sqrt(geometry))) + gram_rate
    constraint_rate += data['nodes']['eta'][-1] * (mass_nodes[-1] @ mass_rate) / (.1 * numerical.sqrt(nodes['F'][-1]))
    constraint_rate -= data['nodes']['eta'][0] * (mass_nodes[0] @ mass_rate) / (.1 * numerical.sqrt(nodes['F'][0]))
    root_f, node_root = numerical.sqrt(geometry), numerical.sqrt(nodes['F'])
    constraint = lapse_tests.T @ (weights * ((root_f + 1 / root_f - 2) / .2 - root_f * energy))
    constraint += values['eta_r'].T @ (weights * radius * (root_f - 1) / .1)
    constraint -= data['nodes']['eta'][-1] * basis.radii[-1] * (node_root[-1] - 1) / .1
    constraint += data['nodes']['eta'][0] * basis.radii[0] * (node_root[0] - 1) / .1
    if gram:
        constraint -= data['nodes']['eta'].T @ (basis.radii**2 * numerical.sqrt(nodes['F']) * gram_density)
    return {'constraint': constraint, 'constraint_rate': constraint_rate, 'gram_constraint_rate': gram_rate, 'mu_t': physical_mass_rate, 'mu_tr': physical_mass_rate_r, 'P_t': physical_momentum_rate, 'pi_t': physical_pi_rate, 'q': physical_q, 'q_r': physical_q_r, 'mu_t_nodes': mass_nodes @ mass_rate, 'q_nodes': q_nodes, 'P_t_nodes': frame_mass['nodes']['p'] @ momentum_rate, 'gram_scalar': gram_scalar, 'endpoint_log': endpoint_log, 'reactions': actual_reactions, 'mass_pair': mass_pair, 'scalar_pair': scalar_pair, 'mass_rate_coeff': mass_rate, 'P_rate_coeff': momentum_rate, 'pi_rate_coeff': pi_rate, 'q_coeff': q_coeff}
