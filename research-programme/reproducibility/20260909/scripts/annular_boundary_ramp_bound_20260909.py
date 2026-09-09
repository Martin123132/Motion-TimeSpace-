import numpy as numerical

from annular_adm_mixed_action_20260909 import linear_value_gradient, real_linear


def affine_link_bound(system, packed, pair_current):
    basis, links = system.basis, system.links
    mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
    cosmological = system.constants['Lambda']
    length = basis.radii[-1] - basis.radii[0]
    cell_bounds, relative_bounds, gamma_lowers, variations = [], [], [], []
    for cell, (left, right) in enumerate(zip(basis.faces[:-1], basis.faces[1:])):
        knots = numerical.concatenate([[left], basis.radii[(basis.radii > left) & (basis.radii < right)], [right]])
        mass_end = real_linear(linear_value_gradient(basis.faces, knots)[0], mass)
        lapse_end = real_linear(linear_value_gradient(basis.radii, knots)[0], lapse)
        mass_max = numerical.max(numerical.abs(mass_end))
        lapse_min = numerical.min(lapse_end)
        lower_f = 1 - 2 * mass_max / left - abs(cosmological) * right**2 / 3
        if left <= 0 or lapse_min <= 0 or lower_f <= 0:
            raise ValueError('The conservative positive-chart bound is not certified for this cell.')
        gamma_lower = lapse_min**2 * lower_f
        mass_slope = (mass[cell + 1] - mass[cell]) / (right - left)
        slopes = numerical.diff(lapse_end) / numerical.diff(knots)
        variation = 0.0
        for segment, (lower, upper) in enumerate(zip(knots[:-1], knots[1:])):
            local_mass_max = max(abs(mass_end[segment]), abs(mass_end[segment + 1]))
            local_lapse_max = max(abs(lapse_end[segment]), abs(lapse_end[segment + 1]))
            lapse_slope = slopes[segment]
            maximum_f = 1 + 2 * local_mass_max / lower + abs(cosmological) * upper**2 / 3
            maximum_first = 2 * abs(mass_slope) / lower + 2 * local_mass_max / lower**2 + 2 * abs(cosmological) * upper / 3
            maximum_second = 4 * abs(mass_slope) / lower**2 + 4 * local_mass_max / lower**3 + 2 * abs(cosmological) / 3
            gamma_second_bound = 2 * lapse_slope**2 * maximum_f + 4 * local_lapse_max * abs(lapse_slope) * maximum_first + local_lapse_max**2 * maximum_second
            variation += (upper - lower) * gamma_second_bound
        for node in range(1, knots.size - 1):
            spatial_f = 1 - 2 * mass_end[node] / knots[node] - cosmological * knots[node]**2 / 3
            variation += abs(2 * lapse_end[node] * spatial_f * (slopes[node] - slopes[node - 1]))
        interpolation_bound = (right - left) * variation / 4
        cell_bounds.append(interpolation_bound)
        relative_bounds.append(interpolation_bound / gamma_lower)
        gamma_lowers.append(gamma_lower)
        variations.append(variation)
    relative_bounds = numerical.asarray(relative_bounds)
    lower, upper = numerical.minimum(links.anchors, links.targets), numerical.maximum(links.anchors, links.targets)
    overlap = numerical.maximum(numerical.minimum(upper[:, None], basis.faces[None, 1:]) - numerical.maximum(lower[:, None], basis.faces[None, :-1]), 0)
    link_bound = real_linear(overlap, relative_bounds) / length
    gamma_face = real_linear(basis.node_to_face, lapse)**2 * (1 - 2 * mass / basis.faces - cosmological * basis.faces**2 / 3)
    generator = -gamma_face / length
    actual_error = real_linear(links.matrix(mass, lapse, system.constants), generator) + (links.targets - links.anchors) / length
    actual_remainder = -numerical.dot(pair_current, actual_error)
    bound = numerical.dot(numerical.abs(pair_current), link_bound)
    return {'link_error': actual_error, 'link_error_bound': link_bound, 'Gram_affine_link_remainder': numerical.asarray(actual_remainder), 'Gram_affine_link_remainder_bound': numerical.asarray(bound), 'cell_gamma_interpolation_bound': numerical.asarray(cell_bounds), 'cell_gamma_lower_bound': numerical.asarray(gamma_lowers), 'cell_gamma_derivative_variation_bound': numerical.asarray(variations), 'affine_shift_generator': generator}
