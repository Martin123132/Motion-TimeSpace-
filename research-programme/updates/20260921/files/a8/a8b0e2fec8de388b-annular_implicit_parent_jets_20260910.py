import numpy as numerical

from annular_parent_coefficient_box_20260910 import Box, Taylor, down, up, concatenate, bilinear_box, comparison_solve
from annular_parent_root_residence_20260910 import canonical_maps, action_enclosure
from annular_gram_joint_action_20260909 import gram_matrices


def join_jets(jets):
    return Taylor([concatenate([jet.coefficients[order] for jet in jets]) for order in range(4)])


def set_coordinates(value, indices, replacement):
    replacement = Box.cast(replacement)
    lower, upper = value.lo.copy(), value.hi.copy()
    lower[indices], upper[indices] = replacement.lo, replacement.hi
    return Box(lower, upper)


def intersect(first, second):
    return Box(numerical.maximum(first.lo, second.lo), numerical.minimum(first.hi, second.hi))


def constraint_force_jets(system, packed, configuration, momenta, clock, include_gram):
    if system.kappa != .1 or any(system.constants[name] != 0 for name in ['Lambda', 'm_chi', 'b2', 'b3']):
        raise ValueError('Only the original canonical kappa=1/10 branch is supported.')
    basis, count = system.basis, system.node_count
    radius, nodes, weights, kappa = Box(basis.quadrature), Box(basis.radii), Box(basis.quadrature_weights), Box(1.) / 10
    value_map, gradient_map = canonical_maps(basis)
    mass, lapse = packed.selected(system.slices[0]), packed.selected(system.slices[1])
    mass_q, mass_r = mass.mapped(basis.face_value), mass.mapped(basis.face_gradient)
    lapse_q = lapse.mapped(basis.node_value)
    velocity = packed.selected(slice(system.slices[2].start, system.count)).mapped(value_map)
    gradient = configuration.mapped(gradient_map)
    field_f, node_f = 1 - 2 * mass_q / radius, 1 - 2 * mass.mapped(basis.face_to_node) / nodes
    if min(float(field_f.coefficients[0].lo.min()), float(node_f.coefficients[0].lo.min()), float(lapse_q.coefficients[0].lo.min()), float(lapse.coefficients[0].lo.min())) <= 0:
        raise ValueError('Constraint jets leave the positive chart.')
    mass_density = lapse_q * mass_r / (kappa * radius) * field_f**-1.5 + radius * velocity**2 / (2 * lapse_q) * field_f**-1.5 + radius * lapse_q * gradient**2 / 2 * field_f**-.5
    lapse_density = mass_r / kappa * field_f**-.5 - radius**2 * velocity**2 / (2 * lapse_q**2) * field_f**-.5 - radius**2 * gradient**2 / 2 * field_f**.5
    mass_row = (weights * mass_density).mapped(basis.face_value.T) + (weights * lapse_q / kappa * field_f**-.5).mapped(basis.face_gradient.T)
    lapse_row = (weights * lapse_density).mapped(basis.node_value.T)
    velocity_row = (weights * radius**2 * velocity / lapse_q * field_f**-.5).mapped(value_map.T) - momenta
    force = -(weights * radius**2 * lapse_q * field_f**.5 * gradient).mapped(gradient_map.T)
    if include_gram:
        factors, sampling = gram_matrices(count)
        embed = numerical.pad(factors, ((0, 0), (0, count)))
        density = (configuration.selected(slice(0, count)).mapped(factors)**2).mapped(sampling.T) / (2 * basis.spacing)
        coefficient = nodes**2 * lapse * node_f**.5
        mass_row = mass_row + (density * nodes * lapse * node_f**-.5).mapped(basis.face_to_node.T)
        lapse_row = lapse_row - density * nodes**2 * node_f**.5
        force = force - (coefficient.mapped(sampling) * configuration.mapped(embed) / basis.spacing).mapped(embed.T)
    boundary = numerical.zeros(system.face_count)
    boundary[-1] = 1.
    mass_row = mass_row - clock * boundary / kappa
    force = Taylor([set_coordinates(coefficient, [0, count - 1], Box(0.)) for coefficient in force.coefficients])
    return join_jets([mass_row, lapse_row, velocity_row]), force


def shift_jets(system, packed, configuration, include_gram, order):
    if order not in [0, 1]:
        raise ValueError('Only zeroth/first shift coefficients are requested by this derivation.')
    basis, links = system.basis, system.links
    radius, nodes, weights, kappa = Box(basis.quadrature), Box(basis.radii), Box(basis.quadrature_weights), Box(1.) / 10
    value_map, gradient_map = canonical_maps(basis)
    mass, lapse = packed.selected(system.slices[0]), packed.selected(system.slices[1])
    lapse_q = lapse.mapped(basis.node_value)
    field_f = 1 - 2 * mass.mapped(basis.face_value) / radius
    velocity_q = packed.selected(slice(system.slices[2].start, system.count)).mapped(value_map)
    gradient_q = configuration.mapped(gradient_map)
    pairing_weight = weights / (kappa * lapse_q * field_f**1.5)
    pairing = [bilinear_box(value, basis.face_value, basis.face_value) for value in pairing_weight.coefficients[:order + 1]]
    matter = -(weights * radius**2 * velocity_q * gradient_q / (lapse_q * field_f**.5)).mapped(basis.face_value.T)
    gram = [Box(numerical.zeros(system.face_count)) for unused in range(order + 1)]
    if include_gram:
        factors, sampling = gram_matrices(system.node_count)
        coefficient = nodes**2 * lapse * (1 - 2 * mass.mapped(basis.face_to_node) / nodes)**.5
        leading = configuration.selected(slice(0, system.node_count)).mapped(factors)
        node_velocity = packed.selected(system.slices[2])
        leading_time = node_velocity.mapped(factors)
        sampled = coefficient.mapped(sampling)
        current = coefficient.selected(links.node) * links.sweight * leading.selected(links.factor) * leading_time.selected(links.factor) / basis.spacing
        current = current - node_velocity.selected(links.node) * links.tweight * sampled.selected(links.factor) * leading.selected(links.factor) / basis.spacing
        link_lapse, link_f = lapse.mapped(links.node_value), 1 - 2 * mass.mapped(links.face_value) / links.points
        if min(float(link_lapse.coefficients[0].lo.min()), float(link_f.coefficients[0].lo.min())) <= 0:
            raise ValueError('Metric-link jets leave the positive chart.')
        inverse = 1 / (link_lapse**2 * link_f)
        matrices = []
        for coefficient in inverse.coefficients[:order + 1]:
            integrand = coefficient[:, None] * links.face_value
            lower = numerical.zeros((links.node.size, system.face_count))
            upper = lower.copy()
            for point in range(links.points.size):
                addition = integrand[point] * links.weights[point]
                pair = links.pairs[point]
                lower[pair], upper[pair] = down(lower[pair] + addition.lo), up(upper[pair] + addition.hi)
            matrices.append(Box(lower, upper))
        for level in range(order + 1):
            gram[level] = -sum((matrices[previous].T @ current.coefficients[level - previous] for previous in range(level + 1)), Box(numerical.zeros(system.face_count)))
    return pairing, [gram[level] - matter.coefficients[level] for level in range(order + 1)]


def implicit_jet_enclosure(system, packed, configuration, momenta, clock, clock_rate, endpoint_acceleration, include_gram):
    static = action_enclosure(system, packed, configuration, momenta, clock, include_gram)
    jacobian = static['jacobian']
    selected = numerical.ix_(system.free, system.free)
    velocity_slice = slice(system.slices[2].start, system.count)
    velocity, force = packed[velocity_slice], static['momentum_rate']
    pairing_zero, load_zero = shift_jets(system, Taylor([packed]), Taylor([configuration]), include_gram, 0)
    shift_velocity, shift_diagnostic = comparison_solve(pairing_zero[0], load_zero[0])
    fixed_first = set_coordinates(Box(numerical.zeros(system.count)), system.fixed, concatenate([shift_velocity[:1], Box(endpoint_acceleration)]))
    clock_jet = Taylor([clock, Box(clock_rate)])
    configuration_first = Taylor([configuration, velocity])
    momentum_first = Taylor([momenta, force])
    residual_first, unused_force = constraint_force_jets(system, Taylor([packed, fixed_first]), configuration_first, momentum_first, clock_jet, include_gram)
    free_first, first_diagnostic = comparison_solve(jacobian[selected], -residual_first.coefficients[1][system.free])
    first = set_coordinates(fixed_first, system.free, free_first)
    residual_tangent, force_tangent = constraint_force_jets(system, Taylor([packed, first]), configuration_first, momentum_first, clock_jet, include_gram)
    pairing, load = shift_jets(system, Taylor([packed, first]), configuration_first, include_gram, 1)
    shift_acceleration, shift_first_diagnostic = comparison_solve(pairing[0], load[1] - pairing[1] @ shift_velocity)
    fixed_second = set_coordinates(Box(numerical.zeros(system.count)), [system.fixed[0]], shift_acceleration[:1])
    configuration_second = Taylor([configuration, velocity, first[velocity_slice] / 2])
    momentum_second = Taylor([momenta, force, force_tangent.coefficients[1] / 2])
    residual_second, unused_force = constraint_force_jets(system, Taylor([packed, first, fixed_second / 2]), configuration_second, momentum_second, clock_jet, include_gram)
    free_second, second_diagnostic = comparison_solve(jacobian[selected], -2 * residual_second.coefficients[2][system.free])
    second = set_coordinates(fixed_second, system.free, free_second)
    residual_acceleration, unused_force = constraint_force_jets(system, Taylor([packed, first, second / 2]), configuration_second, momentum_second, clock_jet, include_gram)
    velocity_mismatch = set_coordinates(first[system.slices[0]] - shift_velocity, [0], Box(0.))
    acceleration_mismatch = set_coordinates(second[system.slices[0]] - shift_acceleration, [0], Box(0.))
    defect = intersect(pairing[0] @ velocity_mismatch, pairing[0] @ first[system.slices[0]] - load[0])
    defect_time = intersect(pairing[1] @ velocity_mismatch + pairing[0] @ acceleration_mismatch, pairing[1] @ first[system.slices[0]] + pairing[0] @ second[system.slices[0]] - load[1])
    return {'first': first, 'second': second, 'jacobian': jacobian, 'shift_velocity': shift_velocity, 'shift_acceleration': shift_acceleration, 'shift_defect': defect, 'shift_defect_time': defect_time, 'mass_velocity_mismatch': velocity_mismatch, 'mass_acceleration_mismatch': acceleration_mismatch, 'force': force, 'force_time': force_tangent.coefficients[1], 'constraint_value': static['residual'][system.free], 'constraint_first': residual_tangent.coefficients[1][system.free], 'constraint_second': 2 * residual_acceleration.coefficients[2][system.free], 'pairing': pairing[0], 'pairing_time': pairing[1], 'shift_load': load[0], 'shift_load_time': load[1], 'first_known': residual_first.coefficients[1][system.free], 'second_known': 2 * residual_second.coefficients[2][system.free], 'diagnostics': {'shift': shift_diagnostic, 'parent_first': first_diagnostic, 'shift_first': shift_first_diagnostic, 'parent_second': second_diagnostic}, 'minimum_F': static['minimum_F'], 'minimum_N': static['minimum_N']}
