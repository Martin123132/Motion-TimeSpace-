import numpy as numerical
from scipy.linalg import solve

from annular_parent_coefficient_box_20260910 import Box, down, up, concatenate, bilinear_box, comparison_solve
from annular_gram_joint_action_20260909 import gram_matrices


def canonical_maps(basis):
    value = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)
    gradient = numerical.concatenate([basis.scalar_gradient, basis.lift_gradient / basis.spacing], axis=1)
    return value, gradient


def action_enclosure(system, packed, configuration, momenta, clock, include_gram, hessian=True):
    if system.kappa != .1 or any(system.constants[name] != 0 for name in ['Lambda', 'm_chi', 'b2', 'b3']):
        raise ValueError('Only the sourced canonical kappa=1/10 branch is covered.')
    basis, radius, weights = system.basis, system.basis.quadrature, system.basis.quadrature_weights
    radius = Box(radius)
    kappa = Box(1.) / 10
    value_map, gradient_map = canonical_maps(basis)
    mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
    mass_q, mass_r = Box(basis.face_value) @ mass, Box(basis.face_gradient) @ mass
    lapse_q = Box(basis.node_value) @ lapse
    velocity = Box(value_map) @ packed[system.slices[2].start:]
    gradient = Box(gradient_map) @ configuration
    field_f = 1 - 2 * mass_q / radius
    node_f = 1 - 2 * (Box(basis.face_to_node) @ mass) / basis.radii
    face_f = 1 - 2 * mass / basis.faces
    if min(float(face_f.lo.min()), float(field_f.lo.min()), float(node_f.lo.min()), float(lapse.lo.min()), float(lapse_q.lo.min())) <= 0:
        raise ValueError('Root neighborhood crosses the positive metric chart.')
    mass_density = lapse_q * mass_r / (kappa * radius) * field_f**-1.5 + radius * velocity**2 / (2 * lapse_q) * field_f**-1.5 + radius * lapse_q * gradient**2 / 2 * field_f**-.5
    lapse_density = mass_r / kappa * field_f**-.5 - radius**2 * velocity**2 / (2 * lapse_q**2) * field_f**-.5 - radius**2 * gradient**2 / 2 * field_f**.5
    momentum_density = radius**2 * velocity / lapse_q * field_f**-.5
    mass_row = Box(basis.face_value.T) @ (weights * mass_density) + Box(basis.face_gradient.T) @ (weights * lapse_q / kappa * field_f**-.5)
    lapse_row = Box(basis.node_value.T) @ (weights * lapse_density)
    velocity_row = Box(value_map.T) @ (weights * momentum_density) - momenta
    force = -(Box(gradient_map.T) @ (weights * radius**2 * lapse_q * field_f**.5 * gradient))
    factors, sampling = gram_matrices(system.node_count)
    embed = numerical.pad(factors, ((0, 0), (0, system.node_count)))
    density_gram = (Box(sampling.T) @ ((Box(factors) @ configuration[:system.node_count])**2)) / (2 * basis.spacing)
    coefficient = Box(basis.radii)**2 * lapse * node_f**.5
    if include_gram:
        mass_row = mass_row + Box(basis.face_to_node.T) @ (density_gram * basis.radii * lapse * node_f**-.5)
        lapse_row = lapse_row - density_gram * Box(basis.radii)**2 * node_f**.5
        force = force - Box(embed.T) @ ((Box(sampling) @ coefficient) * (Box(embed) @ configuration) / basis.spacing)
    boundary = numerical.zeros(system.face_count)
    boundary[-1] = 1.
    mass_row = mass_row - clock * boundary / kappa
    force_lower, force_upper = force.lo.copy(), force.hi.copy()
    force_lower[[0, system.node_count - 1]] = 0.
    force_upper[[0, system.node_count - 1]] = 0.
    result = {'residual': concatenate([mass_row, lapse_row, velocity_row]), 'momentum_rate': Box(force_lower, force_upper), 'minimum_F': float(min(face_f.lo.min(), field_f.lo.min(), node_f.lo.min())), 'minimum_N': float(min(lapse.lo.min(), lapse_q.lo.min()))}
    if not hessian:
        return result
    local = [[Box(numerical.zeros_like(basis.quadrature)) for other in range(4)] for first in range(4)]
    local[0][0] = 3 * lapse_q * mass_r / (kappa * radius**2) * field_f**-2.5 + 1.5 * velocity**2 / lapse_q * field_f**-2.5 + .5 * lapse_q * gradient**2 * field_f**-1.5
    local[0][1] = lapse_q / (kappa * radius) * field_f**-1.5
    local[0][2] = mass_r / (kappa * radius) * field_f**-1.5 - radius * velocity**2 / (2 * lapse_q**2) * field_f**-1.5 + radius * gradient**2 / 2 * field_f**-.5
    local[0][3] = radius * velocity / lapse_q * field_f**-1.5
    local[1][2] = field_f**-.5 / kappa
    local[2][2] = radius**2 * velocity**2 / lapse_q**3 * field_f**-.5
    local[2][3] = -radius**2 * velocity / lapse_q**2 * field_f**-.5
    local[3][3] = radius**2 / lapse_q * field_f**-.5
    maps = [mapping.copy() for mapping in system.maps]
    maps[3][:, system.slices[2].start:] = value_map
    jacobian = Box(numerical.zeros((system.count, system.count)))
    for first in range(4):
        for other in range(first, 4):
            if numerical.all(local[first][other].magnitude == 0):
                continue
            contribution = bilinear_box(weights * local[first][other], maps[first], maps[other])
            jacobian = jacobian + contribution
            if first != other:
                jacobian = jacobian + contribution.T
    if include_gram:
        jacobian = jacobian + bilinear_box(density_gram * lapse * node_f**-1.5, system.node_maps[0], system.node_maps[0])
        mixed = bilinear_box(density_gram * basis.radii * node_f**-.5, system.node_maps[0], system.node_maps[1])
        jacobian = jacobian + mixed + mixed.T
    result['jacobian'] = jacobian
    return result


def shift_enclosure(system, packed, configuration, include_gram):
    basis, links = system.basis, system.links
    value_map, gradient_map = canonical_maps(basis)
    mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
    lapse_q = Box(basis.node_value) @ lapse
    field_f = 1 - 2 * (Box(basis.face_value) @ mass) / basis.quadrature
    velocity_q = Box(value_map) @ packed[system.slices[2].start:]
    gradient_q = Box(gradient_map) @ configuration
    kappa = Box(1.) / 10
    pairing = bilinear_box(basis.quadrature_weights / (kappa * lapse_q * field_f**1.5), basis.face_value, basis.face_value)
    matter = -(Box(basis.face_value.T) @ (basis.quadrature_weights * Box(basis.quadrature)**2 * velocity_q * gradient_q / (lapse_q * field_f**.5)))
    gram = Box(numerical.zeros(system.face_count))
    if include_gram:
        factors, sampling = gram_matrices(system.node_count)
        coefficient = Box(basis.radii)**2 * lapse * (1 - 2 * (Box(basis.face_to_node) @ mass) / basis.radii)**.5
        leading = Box(factors) @ configuration[:system.node_count]
        leading_time = Box(factors) @ packed[system.slices[2]]
        sampled = Box(sampling) @ coefficient
        current = coefficient[links.node] * links.sweight * leading[links.factor] * leading_time[links.factor] / basis.spacing
        current = current - packed[system.slices[2]][links.node] * links.tweight * sampled[links.factor] * leading[links.factor] / basis.spacing
        link_lapse = Box(links.node_value) @ lapse
        link_f = 1 - 2 * (Box(links.face_value) @ mass) / links.points
        if min(float(link_lapse.lo.min()), float(link_f.lo.min())) <= 0:
            raise ValueError('Metric links leave the positive chart.')
        inverse = 1 / (link_lapse**2 * link_f)
        integrand = inverse[:, None] * links.face_value
        lower = numerical.zeros((links.node.size, system.face_count))
        upper = lower.copy()
        for point in range(links.points.size):
            addition = integrand[point] * links.weights[point]
            pair = links.pairs[point]
            lower[pair] = down(lower[pair] + addition.lo)
            upper[pair] = up(upper[pair] + addition.hi)
        gram = -(Box(lower, upper).T @ current)
    velocity, diagnostic = comparison_solve(pairing, gram - matter)
    return velocity, diagnostic


def root_inclusion(center, residual, jacobian, widths):
    if not numerical.all(numerical.isfinite(widths)) or numerical.any(widths <= 0):
        raise ValueError('Root search radii must be finite and positive.')
    inverse = solve(jacobian.midpoint, numerical.eye(center.size), assume_a='gen')
    defect = Box(numerical.eye(center.size)) - Box(inverse) @ jacobian
    majorant = defect.magnitude
    contraction = float(max((Box(majorant) @ Box(numerical.ones(center.size))).hi))
    correction = -(Box(inverse) @ residual)
    image = (Box(correction.magnitude) + Box(majorant) @ Box(widths)).hi
    ratio = float(max((Box(image) / Box(widths)).hi))
    if contraction >= 1 or ratio >= 1:
        return {'gate': False, 'contraction': contraction, 'inclusion_ratio': ratio}
    delta, diagnostic = comparison_solve(jacobian, -residual)
    root = Box(center) + delta
    search = Box(center) + Box(-widths, widths)
    root = Box(numerical.maximum(root.lo, search.lo), numerical.minimum(root.hi, search.hi))
    return {'gate': True, 'contraction': contraction, 'inclusion_ratio': ratio, 'root': root, 'linear_diagnostic': diagnostic, 'maximum_correction': float(max(delta.magnitude)), 'maximum_enclosure_width': float(max(root.hi - root.lo)), 'preconditioner': inverse, 'majorant': majorant, 'search_radii': widths, 'image_bound': image, 'residual_box': residual}


def symmetric_box(center, relative_width):
    widths = up(relative_width * numerical.maximum(1., abs(center)))
    return Box(down(center - widths), up(center + widths))


def parameter_root_tube(system, packed, relative_width, time_horizon, endpoint_acceleration, include_gram, unknown_radius=1e-6):
    if time_horizon <= 0 or relative_width <= 0 or unknown_radius <= 0:
        raise ValueError('Tube widths and horizon must be positive.')
    if not all(numerical.isfinite(value) for value in [time_horizon, relative_width, unknown_radius]):
        raise ValueError('Tube widths and horizon must be finite.')
    configuration = numerical.concatenate([system.scalar, system.slope])
    momenta = numerical.concatenate([system.momentum, system.slope_momentum])
    configuration_box = symmetric_box(configuration, relative_width)
    momentum_box = symmetric_box(momenta, relative_width)
    fixed_momenta = [0, system.node_count - 1]
    momentum_lower, momentum_upper = momentum_box.lo.copy(), momentum_box.hi.copy()
    momentum_lower[fixed_momenta], momentum_upper[fixed_momenta] = momenta[fixed_momenta], momenta[fixed_momenta]
    momentum_box = Box(momentum_lower, momentum_upper)
    inner_box = symmetric_box(numerical.array([packed[system.fixed[0]]]), relative_width)
    time_box = Box(0., time_horizon)
    if not hasattr(system, 'residence_clock_rate'):
        raise ValueError('Original affine clock rate must be supplied.')
    clock_box = Box(system.outer_clock) + time_box * system.residence_clock_rate
    width_free = up(unknown_radius * numerical.maximum(1., abs(packed[system.free])))
    packed_box = symmetric_box(packed, unknown_radius)
    lower, upper = packed_box.lo.copy(), packed_box.hi.copy()
    lower[system.fixed[0]], upper[system.fixed[0]] = inner_box.lo[0], inner_box.hi[0]
    prescribed_velocity = Box(packed[system.fixed[1:]]) + time_box * endpoint_acceleration
    lower[system.fixed[1:]], upper[system.fixed[1:]] = prescribed_velocity.lo, prescribed_velocity.hi
    packed_box = Box(lower, upper)
    assembled = action_enclosure(system, packed_box, configuration_box, momentum_box, clock_box, include_gram)
    center_lower, center_upper = packed_box.lo.copy(), packed_box.hi.copy()
    center_lower[system.free], center_upper[system.free] = packed[system.free], packed[system.free]
    parametric_residual = action_enclosure(system, Box(center_lower, center_upper), configuration_box, momentum_box, clock_box, include_gram, False)['residual'][system.free]
    selection = numerical.ix_(system.free, system.free)
    inclusion = root_inclusion(packed[system.free], parametric_residual, assembled['jacobian'][selection], width_free)
    if not inclusion['gate']:
        return {'gate': False, 'inclusion': inclusion, 'relative_width': relative_width}
    root_lower, root_upper = packed_box.lo.copy(), packed_box.hi.copy()
    root_lower[system.free], root_upper[system.free] = inclusion['root'].lo, inclusion['root'].hi
    root_box = Box(root_lower, root_upper)
    initial_residual = action_enclosure(system, Box(packed), Box(configuration), Box(momenta), Box(system.outer_clock), include_gram, False)['residual'][system.free]
    initial = root_inclusion(packed[system.free], initial_residual, assembled['jacobian'][selection], width_free)
    if not initial['gate']:
        raise RuntimeError('Initial root enclosure failed despite parameterized gate.')
    initial_lower, initial_upper = packed.copy(), packed.copy()
    initial_lower[system.free], initial_upper[system.free] = initial['root'].lo, initial['root'].hi
    field = action_enclosure(system, root_box, configuration_box, momentum_box, clock_box, include_gram, False)
    shift, shift_diagnostic = shift_enclosure(system, root_box, configuration_box, include_gram)
    dynamic_center = numerical.concatenate([configuration, momenta, [packed[system.fixed[0]]]])
    dynamic_box = concatenate([configuration_box, momentum_box, inner_box])
    vector_field = concatenate([root_box[system.slices[2].start:], field['momentum_rate'], shift[:1]])
    lower_distance = (Box(dynamic_center) - Box(dynamic_box.lo)).lo
    upper_distance = (Box(dynamic_box.hi) - Box(dynamic_center)).lo
    distance = numerical.maximum(0., numerical.minimum(lower_distance, upper_distance))
    speed_bound = vector_field.magnitude
    fixed = distance == 0
    if numerical.any(speed_bound[fixed] != 0):
        raise RuntimeError('A zero-width coordinate is not invariant.')
    active = (~fixed) & (speed_bound > 0)
    ratios = (Box(distance[active]) / Box(speed_bound[active])).lo
    limiting = float(min(ratios)) if ratios.size else time_horizon
    duration = float((Box(min(limiting, time_horizon)) / 2).lo)
    displacement = (Box(duration) * Box(speed_bound)).hi
    if not duration > 0 or not numerical.all(displacement[~fixed] < distance[~fixed]):
        raise RuntimeError('Strict residence inequality failed.')
    return {'gate': True, 'relative_width': relative_width, 'unknown_radius': unknown_radius, 'time_horizon': time_horizon, 'residence_time': duration, 'limiting_dynamic_index': int(numerical.flatnonzero(active)[numerical.argmin(ratios)]) if ratios.size else -1, 'inclusion': inclusion, 'initial': initial, 'initial_root_box': Box(initial_lower, initial_upper), 'initial_residual': initial_residual, 'root_box': root_box, 'configuration_box': configuration_box, 'momentum_box': momentum_box, 'dynamic_box': dynamic_box, 'vector_field': vector_field, 'distance_lower': distance, 'displacement_upper': displacement, 'constant_coordinate_indices': numerical.flatnonzero(fixed), 'shift_diagnostic': shift_diagnostic, 'minimum_F': assembled['minimum_F'], 'minimum_N': assembled['minimum_N'], 'jacobian_box': assembled['jacobian'], 'original_packed': packed}
