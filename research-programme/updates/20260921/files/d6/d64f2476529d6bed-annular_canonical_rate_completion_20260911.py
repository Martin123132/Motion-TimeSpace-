import numpy as numerical
from scipy.linalg import solve, svd

from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_canonical_mesh_transfer_20260911 import scalar_maps, kinetic_weight
from annular_joint_weak_action_20260910 import joint_prototype
from annular_parent_coefficient_box_20260910 import Box
from annular_gram_joint_action_20260909 import gram_matrices


def bubbles(knots, points, modes):
    segment = numerical.clip(numerical.searchsorted(knots, points, side='right') - 1, 0, knots.size - 2)
    width = knots[segment + 1] - knots[segment]
    fraction = (points - knots[segment]) / width
    centered = 2 * fraction - 1
    base = 4 * fraction * (1 - fraction)
    base_r = (4 - 8 * fraction) / width
    values = numerical.zeros((points.size, modes * (knots.size - 1)))
    gradients = numerical.zeros_like(values)
    rows = numerical.arange(points.size)
    for mode in range(modes):
        values[rows, modes * segment + mode] = base * centered**mode
        gradients[rows, modes * segment + mode] = base_r * centered**mode
        if mode:
            gradients[rows, modes * segment + mode] += 2 * mode * base * centered**(mode - 1) / width
    return values, gradients


class OriginalFrames:
    def __init__(self, model):
        self.model = model
        self.knots = numerical.unique(numerical.concatenate([model.basis.radii, model.basis.faces]))
        prototype = joint_prototype(model.system, Box(model.packed), Box(model.configuration), False)
        self.lift = prototype['bubble_lift_coefficients'].midpoint

    def evaluate(self, points):
        model, basis = self.model, self.model.basis
        face, face_r = linear_value_gradient(basis.faces, points)
        node, node_r = linear_value_gradient(basis.radii, points)
        bubble, bubble_r = bubbles(self.knots, points, 2)
        mass_q = numerical.concatenate([face, bubble @ self.lift], axis=1)
        mass_qr = numerical.concatenate([face_r, bubble_r @ self.lift], axis=1)
        seed_f = 1 - 2 * (face @ model.packed[model.system.slices[0]]) / points
        seed_lapse, seed_lapse_r = node @ model.lapse_seed, node_r @ model.lapse_seed
        zeta = seed_f[:, None] * (seed_lapse[:, None] * node_r[:, 1:-1] - seed_lapse_r[:, None] * node[:, 1:-1])
        shift = numerical.concatenate([face, zeta - face @ model.maps['projection']], axis=1)
        mass_p = shift / (.1 * seed_lapse * seed_f**1.5)[:, None]
        scalar_q, scalar_qr = scalar_maps(basis, points)
        scalar_p = kinetic_weight(model, points)[0][:, None] * scalar_q
        return {'mass': {'q': mass_q, 'qr': mass_qr, 'p': mass_p}, 'scalar': {'q': scalar_q, 'qr': scalar_qr, 'p': scalar_p}}


def normalized_transform(values, weights):
    scale = numerical.sqrt(weights @ values**2)
    if numerical.any(scale == 0):
        raise ValueError('An original trial direction is zero; no mode is silently removed.')
    weighted = numerical.sqrt(weights)[:, None] * (values / scale)
    unused_orthogonal, triangular = numerical.linalg.qr(weighted, mode='reduced')
    if numerical.linalg.cond(triangular) > 1e12:
        raise ValueError('Original trial directions cannot be stably retained.')
    return solve(triangular, numerical.eye(triangular.shape[0])) / scale[:, None]


def complete_phase(frame, rates, reservoir, weights, tolerance=1e-12):
    original_count = frame['quad']['q'].shape[1]
    transformed = {}
    position_transform = normalized_transform(frame['quad']['q'], weights)
    momentum_transform = normalized_transform(frame['quad']['p'], weights)
    for surface, maps in frame.items():
        transformed[surface] = {'q': maps['q'] @ position_transform, 'qr': maps['qr'] @ position_transform, 'p': maps['p'] @ momentum_transform}

    def additions(kind):
        basis_values = transformed['quad'][kind]
        raw = rates['quad'][kind]
        scale = numerical.maximum(numerical.sqrt(weights @ raw**2), 1e-30)
        projection = basis_values.T @ ((weights / 1.)[:, None] * (raw / scale))
        residual = raw / scale - basis_values @ projection
        unused_left, singular, right = svd(numerical.sqrt(weights)[:, None] * residual, full_matrices=False)
        selected = singular > tolerance
        transformation = right[selected].T / singular[selected]
        added = {}
        for surface in frame:
            added[surface] = (rates[surface][kind] / scale - transformed[surface][kind] @ projection) @ transformation
            if kind == 'q':
                added[surface + '_gradient'] = (rates[surface]['qr'] / scale - transformed[surface]['qr'] @ projection) @ transformation
        return added, singular, int(selected.sum())

    added_q, position_singular, position_count = additions('q')
    for surface, maps in transformed.items():
        maps['q'] = numerical.concatenate([maps['q'], added_q[surface]], axis=1)
        maps['qr'] = numerical.concatenate([maps['qr'], added_q[surface + '_gradient']], axis=1)
        maps['p'] = numerical.concatenate([maps['p'], added_q[surface]], axis=1)
    momentum_transform = normalized_transform(transformed['quad']['p'], weights)
    for maps in transformed.values():
        maps['p'] = maps['p'] @ momentum_transform
    added_p, momentum_singular, momentum_count = additions('p')
    coordinate = transformed['quad']['q']
    momentum = transformed['quad']['p']
    pairing = momentum.T @ (weights[:, None] * coordinate)
    bubble_scale = numerical.sqrt(weights @ reservoir['quad']['q']**2)
    bubble_projection = solve(pairing, momentum.T @ (weights[:, None] * (reservoir['quad']['q'] / bubble_scale)))
    raw_lifts = {}
    for surface in frame:
        raw_lifts[surface] = reservoir[surface]['q'] / bubble_scale - transformed[surface]['q'] @ bubble_projection
        raw_lifts[surface + '_gradient'] = reservoir[surface]['qr'] / bubble_scale - transformed[surface]['qr'] @ bubble_projection
    moments = added_p['quad'].T @ (weights[:, None] * raw_lifts['quad'])
    if momentum_count:
        left, singular, right = svd(moments, full_matrices=False)
        if singular[-1] < 1e-10:
            raise ValueError('Continuous dual-bubble reservoir is insufficient; no momentum direction is deleted.')
        lift_coefficients = (right.T / singular) @ left.T
    else:
        singular = numerical.array([])
        lift_coefficients = numerical.empty((moments.shape[1], 0))
    for surface, maps in transformed.items():
        maps['q'] = numerical.concatenate([maps['q'], raw_lifts[surface] @ lift_coefficients], axis=1)
        maps['qr'] = numerical.concatenate([maps['qr'], raw_lifts[surface + '_gradient'] @ lift_coefficients], axis=1)
        maps['p'] = numerical.concatenate([maps['p'], added_p[surface]], axis=1)
    final_pair = transformed['quad']['p'].T @ (weights[:, None] * transformed['quad']['q'])
    expected_pair = numerical.block([[pairing, numerical.zeros((pairing.shape[0], momentum_count))], [added_p['quad'].T @ (weights[:, None] * coordinate), numerical.eye(momentum_count)]])
    reconstruction = {}
    for kind in ['q', 'p']:
        values = transformed['quad'][kind]
        coefficients = solve(values.T @ (weights[:, None] * values), values.T @ (weights[:, None] * rates['quad'][kind]))
        for surface in ['quad', 'check', 'nodes']:
            reconstruction[surface + '_' + kind] = float(abs(transformed[surface][kind] @ coefficients - rates[surface][kind]).max())
        if kind == 'q':
            reconstruction['check_qr'] = float(abs(transformed['check']['qr'] @ coefficients - rates['check']['qr']).max())
    return transformed, {'original_phase_dimension': original_count, 'position_rate_additions': position_count, 'momentum_rate_additions': momentum_count, 'completed_phase_dimension': final_pair.shape[0], 'position_singular_values': position_singular.tolist(), 'momentum_singular_values': momentum_singular.tolist(), 'dual_moment_singular_values': singular.tolist(), 'pairing_block_identity_error': float(abs(final_pair - expected_pair).max()), 'pairing_condition': float(numerical.linalg.cond(final_pair)), 'rate_reconstruction_errors': reconstruction, 'new_rate_rank_tolerance': tolerance, 'original_modes_removed': 0}


def evaluate_initial(frame_mass, frame_scalar, data, basis, weights, links, gram, clock, reactions=None, surface='quad', link_surface='links'):
    radius = data[surface]['R']
    values = data[surface]
    nodes = data['nodes']
    mass_maps, scalar_maps = frame_mass[surface], frame_scalar[surface]
    mass_nodes, scalar_nodes = frame_mass['nodes']['q'], frame_scalar['nodes']['q']
    mass_pair = mass_maps['p'].T @ (weights[:, None] * mass_maps['q'])
    scalar_pair = scalar_maps['p'].T @ (weights[:, None] * scalar_maps['q'])
    geometry, lapse = values['F'], values['N']
    energy = values['pi']**2 / (2 * radius**2) + radius**2 * values['w']**2 / 2
    mass_density = lapse * values['mu_r'] / (.1 * radius * geometry**1.5) + lapse * energy / (radius * numerical.sqrt(geometry))
    mass_force = mass_maps['q'].T @ (weights * mass_density) + mass_maps['qr'].T @ (weights * lapse / (.1 * numerical.sqrt(geometry))) - clock / .1 * mass_nodes[-1]
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
    transport = numerical.zeros(basis.radii.size)
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
        node_values = linear_value_gradient(basis.radii, links.points)[0]
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
    coefficient = values['mu_r'] / (.1 * radius * geometry**1.5) + energy / (radius * numerical.sqrt(geometry))
    density = physical_mass_rate_r / (.1 * numerical.sqrt(geometry)) + coefficient * physical_mass_rate
    density -= numerical.sqrt(geometry) * values['pi'] * physical_pi_rate / radius**2 + radius**2 * numerical.sqrt(geometry) * values['w'] * physical_q_r + .1 * geometry**1.5 * values['pi'] * values['w'] * physical_momentum_rate
    lapse_tests = data[surface]['eta']
    gram_rate = basis.radii * gram_density * (mass_nodes @ mass_rate) / numerical.sqrt(nodes['F']) - basis.radii**2 * numerical.sqrt(nodes['F']) * density_time + transport if gram else numerical.zeros(basis.radii.size)
    constraint_rate = lapse_tests.T @ (weights * density) + gram_rate
    constraint = lapse_tests.T @ (weights * (values['mu_r'] / (.1 * numerical.sqrt(geometry)) - numerical.sqrt(geometry) * energy))
    if gram:
        constraint -= basis.radii**2 * numerical.sqrt(nodes['F']) * gram_density
    return {'constraint': constraint, 'constraint_rate': constraint_rate, 'gram_constraint_rate': gram_rate, 'mu_t': physical_mass_rate, 'mu_tr': physical_mass_rate_r, 'P_t': physical_momentum_rate, 'pi_t': physical_pi_rate, 'q': physical_q, 'q_r': physical_q_r, 'mu_t_nodes': mass_nodes @ mass_rate, 'q_nodes': q_nodes, 'P_t_nodes': frame_mass['nodes']['p'] @ momentum_rate, 'gram_scalar': gram_scalar, 'endpoint_log': endpoint_log, 'reactions': actual_reactions, 'mass_pair': mass_pair, 'scalar_pair': scalar_pair, 'mass_rate_coeff': mass_rate, 'P_rate_coeff': momentum_rate, 'pi_rate_coeff': pi_rate, 'q_coeff': q_coeff}
