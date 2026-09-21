import numpy as numerical

from annular_parent_coefficient_box_20260910 import Box, concatenate
from annular_parent_root_residence_20260910 import canonical_maps
from annular_shift_source_schur_20260910 import matrix_solve
from annular_initial_shift_jet_20260911 import initial_gr_jet


def refine_initial_gr_jet(system, packed, configuration, clock, endpoint_acceleration):
    data = initial_gr_jet(system, packed, configuration, clock, endpoint_acceleration)
    basis, count = system.basis, system.node_count
    value, gradient = canonical_maps(basis)
    free = data['free_scalar']
    endpoints = numerical.array([0, count - 1])
    weights, radius, kappa = Box(basis.quadrature_weights), Box(basis.quadrature), Box(1.) / 10
    mass = Box(basis.face_value) @ packed[system.slices[0]]
    mass_r = Box(basis.face_gradient) @ packed[system.slices[0]]
    lapse = Box(basis.node_value) @ packed[system.slices[1]]
    velocity = Box(value) @ packed[system.slices[2].start:]
    velocity_r = Box(gradient) @ packed[system.slices[2].start:]
    scalar_gradient = Box(gradient) @ Box(configuration)
    spatial_f = 1 - 2 * mass / radius
    kinetic = radius**2 / (lapse * spatial_f**.5)
    spatial = radius**2 * lapse * spatial_f**.5
    projection_load = (velocity / lapse)[:, None] * Box(basis.node_value)
    projection, projection_diagnostic = matrix_solve(data['scalar_matrix'], data['lapse_mixing'])
    remainder = projection_load - Box(value[:, free]) @ projection
    schur = remainder.T @ ((weights * kinetic)[:, None] * remainder)
    source_scalar = -(Box(gradient[:, free].T) @ (weights * spatial * scalar_gradient))
    source_scalar -= Box(value[:, free].T) @ (weights * kinetic * velocity * data['mass_speed'] / (radius * spatial_f))
    source_scalar -= (Box(value[:, free].T) @ ((weights * kinetic)[:, None] * Box(value[:, endpoints]))) @ Box(endpoint_acceleration)
    source_lapse_density = data['mass_speed_gradient'] / (kappa * spatial_f**.5)
    source_lapse_density += (mass_r / (kappa * radius * spatial_f**1.5) - radius * velocity**2 / (2 * lapse**2 * spatial_f**1.5) + radius * scalar_gradient**2 / (2 * spatial_f**.5)) * data['mass_speed']
    source_lapse_density -= radius**2 * spatial_f**.5 * scalar_gradient * velocity_r
    source_lapse = -(Box(basis.node_value.T) @ (weights * source_lapse_density))
    source_lapse += (Box(basis.node_value.T) @ ((weights * kinetic * velocity / lapse)[:, None] * Box(value[:, endpoints]))) @ Box(endpoint_acceleration)
    shift_mixing = Box(value[:, free].T) @ ((weights * kinetic * scalar_gradient)[:, None] * Box(data['shift_map']))
    scalar_load = shift_mixing @ data['shift_rate'] + concatenate([source_scalar[:, None], Box(numerical.zeros((free.size, 1)))], axis=1)
    lapse_load = data['defect_mixing'] @ data['shift_rate'] + concatenate([source_lapse[:, None], Box(numerical.zeros((count, 1)))], axis=1)
    scalar_particular, particular_diagnostic = matrix_solve(data['scalar_matrix'], scalar_load)
    schur_load = lapse_load + data['lapse_mixing'].T @ scalar_particular
    lapse_rate, lapse_diagnostic = matrix_solve(schur, schur_load)
    free_acceleration = scalar_particular + projection @ lapse_rate
    refined = concatenate([free_acceleration, lapse_rate], axis=0)
    original = data['coupled_jet']
    lower = numerical.maximum(original.lo, refined.lo)
    upper = numerical.minimum(original.hi, refined.hi)
    if numerical.any(lower > upper):
        raise RuntimeError('Independent coupled/Schur enclosures disagree.')
    jet = Box(lower, upper)
    acceleration_lower, acceleration_upper = data['acceleration'].lo.copy(), data['acceleration'].hi.copy()
    acceleration_lower[free], acceleration_upper[free] = jet.lo[:free.size], jet.hi[:free.size]
    direct_schur = data['lapse_matrix'] - data['lapse_mixing'].T @ projection
    data['unrefined_coupled_jet'] = original
    data['coupled_jet'] = jet
    data['acceleration'] = Box(acceleration_lower, acceleration_upper)
    data['lapse_rate'] = jet[free.size:]
    data['scalar_residual'] = data['scalar_matrix'] @ jet[:free.size] - data['lapse_mixing'] @ data['lapse_rate'] - scalar_load
    data['lapse_residual'] = -data['lapse_mixing'].T @ jet[:free.size] + data['lapse_matrix'] @ data['lapse_rate'] - lapse_load
    data['schur'] = schur
    data['projection_remainder'] = remainder
    data['schur_identity_residual'] = schur - direct_schur
    data['diagnostics']['scalar_projection'] = projection_diagnostic
    data['diagnostics']['scalar_particular'] = particular_diagnostic
    data['diagnostics']['projection_Gram_lapse'] = lapse_diagnostic
    return data
