import numpy as numerical

from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_parent_coefficient_box_20260910 import Box, Taylor, bilinear_box, concatenate
from annular_parent_root_residence_20260910 import action_enclosure, canonical_maps
from annular_implicit_parent_jets_20260910 import shift_jets
from annular_shift_source_schur_20260910 import matrix_solve
from annular_gram_joint_action_20260909 import gram_matrices


CHANNELS = ['mass_product_commutator', 'shift_test_commutator', 'scalar_gradient_commutator', 'scalar_time_commutator', 'inner_mass_reaction', 'outer_clock_port', 'Gram_scalar_pairing', 'Gram_lapse_variation', 'Gram_mass_pairing', 'Gram_shift_pairing']


def weak_product_source(system, packed, configuration, momenta, clock, mass_rate, lapse_rate, endpoint_acceleration, include_gram):
    basis, count = system.basis, system.node_count
    value_map, gradient_map = canonical_maps(basis)
    free_scalar = system.free_velocity_indices - system.slices[2].start
    values, gradients = Box(value_map[:, free_scalar]), Box(gradient_map[:, free_scalar])
    radius, weights = Box(basis.quadrature), Box(basis.quadrature_weights)
    face_values, face_gradients = Box(basis.face_value), Box(basis.face_gradient)
    eta, eta_gradient = Box(basis.node_value), Box(basis.node_gradient)
    mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
    mass_q, mass_gradient = face_values @ mass, face_gradients @ mass
    lapse_q, lapse_gradient = eta @ lapse, eta_gradient @ lapse
    speed, speed_gradient = face_values @ mass_rate, face_gradients @ mass_rate
    lapse_time = eta @ lapse_rate
    velocity = Box(value_map) @ packed[system.slices[2].start:]
    velocity_gradient = Box(gradient_map) @ packed[system.slices[2].start:]
    scalar_gradient = Box(gradient_map) @ configuration
    spatial_f = 1 - 2 * mass_q / radius
    if min(float(spatial_f.lo.min()), float(lapse_q.lo.min())) <= 0:
        raise ValueError('Weak product identity requires the positive canonical chart.')
    kappa = Box(1.) / 10
    kinetic_density = radius**2 / (lapse_q * spatial_f**.5)
    flux_density = radius**2 * lapse_q * spatial_f**.5
    theta = lapse_time / lapse_q - speed / (radius * spatial_f)
    acceleration_boundary = Box(value_map[:, [0, count - 1]]) @ Box(endpoint_acceleration)
    kinetic = bilinear_box(weights * kinetic_density, value_map[:, free_scalar], value_map[:, free_scalar])
    phi = (velocity / lapse_q)[:, None] * eta
    phi_gradient = (velocity_gradient / lapse_q - velocity * lapse_gradient / lapse_q**2)[:, None] * eta + (velocity / lapse_q)[:, None] * eta_gradient
    scalar_coefficients, scalar_diagnostic = matrix_solve(kinetic, values.T @ ((weights * kinetic_density)[:, None] * phi))
    phi_remainder = phi - values @ scalar_coefficients
    phi_gradient_remainder = phi_gradient - gradients @ scalar_coefficients
    orthogonality = values.T @ ((weights * kinetic_density)[:, None] * phi_remainder)
    scalar_gradient_source = -(phi_gradient_remainder.T @ (weights * flux_density * scalar_gradient))
    scalar_time_source = -(phi_remainder.T @ (weights * kinetic_density * (acceleration_boundary - theta * velocity)))
    mass_test = (speed / lapse_q)[:, None] * eta
    mass_test_gradient = (speed_gradient / lapse_q - speed * lapse_gradient / lapse_q**2)[:, None] * eta + (speed / lapse_q)[:, None] * eta_gradient
    node_at_face, unused_gradient = linear_value_gradient(basis.radii, basis.faces)
    lapse_at_face = Box(node_at_face) @ lapse
    mass_coefficients = (mass_rate / lapse_at_face)[:, None] * Box(node_at_face)
    mass_remainder = mass_test - face_values @ mass_coefficients
    mass_gradient_remainder = mass_test_gradient - face_gradients @ mass_coefficients
    lagrangian_mass = lapse_q * mass_gradient / (kappa * radius) * spatial_f**-1.5 + radius * velocity**2 / (2 * lapse_q) * spatial_f**-1.5 + radius * lapse_q * scalar_gradient**2 / 2 * spatial_f**-.5
    lagrangian_mass_gradient = lapse_q / kappa * spatial_f**-.5
    mass_source = mass_remainder.T @ (weights * lagrangian_mass) + mass_gradient_remainder.T @ (weights * lagrangian_mass_gradient)
    shift_pairing, shift_load = shift_jets(system, Taylor([packed]), Taylor([configuration]), include_gram, 0)
    shift_weight = weights / (kappa * lapse_q * spatial_f**1.5)
    zeta = (lapse_q * spatial_f)[:, None] * eta_gradient - (spatial_f * lapse_gradient)[:, None] * eta
    shift_coefficients, shift_diagnostic = matrix_solve(shift_pairing[0], face_values.T @ (shift_weight[:, None] * zeta))
    shift_remainder = zeta - face_values @ shift_coefficients
    scalar_flux = kappa * radius**2 * spatial_f * velocity * scalar_gradient
    shift_source = shift_remainder.T @ (shift_weight * (scalar_flux - speed))
    shift_equation_check = shift_pairing[0] @ mass_rate - shift_load[0]
    assembled = action_enclosure(system, packed, configuration, momenta, clock, include_gram)
    inner_reaction = mass_coefficients[0] * assembled['residual'][0]
    clock_port = mass_coefficients[-1] * clock / kappa
    root_remainder = mass_coefficients[1:].T @ assembled['residual'][1:system.face_count]
    zero = Box(numerical.zeros(count))
    gram_scalar, gram_lapse, gram_mass, gram_shift, gram_scalar_exact = zero, zero, zero, zero, zero
    if include_gram:
        factors, sampling = gram_matrices(count)
        embed = numerical.pad(factors, ((0, 0), (0, count)))
        nodes = Box(basis.radii)
        node_mass = Box(basis.face_to_node) @ mass
        node_speed = Box(basis.face_to_node) @ mass_rate
        node_f = 1 - 2 * node_mass / nodes
        leading = Box(factors) @ configuration[:count]
        leading_time = Box(factors) @ packed[system.slices[2]]
        density = (Box(sampling.T) @ leading**2) / (2 * basis.spacing)
        density_time = (Box(sampling.T) @ (leading * leading_time)) / basis.spacing
        coefficient = nodes**2 * lapse * node_f**.5
        scalar_gram_covector = Box(embed.T) @ ((Box(sampling) @ coefficient) * leading / basis.spacing)
        mass_gram_covector = Box(basis.face_to_node.T) @ (density * nodes * lapse * node_f**-.5)
        gram_scalar = scalar_coefficients.T @ scalar_gram_covector[free_scalar]
        gram_scalar_exact = packed[system.slices[2]] / lapse * scalar_gram_covector[:count]
        gram_lapse = -nodes**2 * density_time * node_f**.5 + nodes * density * node_speed * node_f**-.5
        gram_mass = -(mass_coefficients.T @ mass_gram_covector)
        unused_pairing, bulk_load = shift_jets(system, Taylor([packed]), Taylor([configuration]), False, 0)
        gram_shift = -(shift_coefficients.T @ (shift_load[0] - bulk_load[0]))
    channels = concatenate([part[:, None] for part in [mass_source, shift_source, scalar_gradient_source, scalar_time_source, inner_reaction, clock_port, gram_scalar, gram_lapse, gram_mass, gram_shift]], axis=1)
    ones = Box(numerical.ones(len(CHANNELS)))
    reconstructed = channels @ ones
    scalar_enriched_interior = (mass_source + shift_source + inner_reaction + clock_port + gram_scalar_exact + gram_lapse + gram_mass + gram_shift)[1:-1]
    face_at_node, unused_gradient = linear_value_gradient(basis.faces, basis.radii)
    node_field_f = 1 - 2 * (Box(face_at_node) @ mass) / basis.radii
    selected_neighbors = numerical.array([index + 1 if index + 1 < count - 1 else index - 1 for index in range(1, count - 1)])
    positive_jump = (node_field_f * lapse)[selected_neighbors] / basis.spacing
    acceleration_rhs = assembled['momentum_rate'][free_scalar] + values.T @ (weights * kinetic_density * (theta * velocity - acceleration_boundary))
    acceleration_free, acceleration_diagnostic = matrix_solve(kinetic, acceleration_rhs)
    acceleration_q = acceleration_boundary + values @ acceleration_free
    direct_density = speed_gradient / (kappa * spatial_f**.5) + mass_gradient * speed / (kappa * radius * spatial_f**1.5)
    direct_density = direct_density - radius**2 * velocity * acceleration_q / (lapse_q**2 * spatial_f**.5) + radius**2 * velocity**2 * lapse_time / (lapse_q**3 * spatial_f**.5)
    direct_density = direct_density - radius * velocity**2 * speed / (2 * lapse_q**2 * spatial_f**1.5) - radius**2 * scalar_gradient * velocity_gradient * spatial_f**.5 + radius * scalar_gradient**2 * speed / (2 * spatial_f**.5)
    direct_lapse_derivative = eta.T @ (weights * direct_density) + gram_lapse
    return {'channels': channels, 'reconstructed_obstruction': reconstructed, 'free_root_remainder': root_remainder, 'direct_lapse_derivative': direct_lapse_derivative, 'full_algebra_difference': reconstructed + root_remainder - direct_lapse_derivative, 'scalar_projection_orthogonality': orthogonality, 'shift_equation_check': shift_equation_check, 'scalar_projection_coefficients': scalar_coefficients, 'mass_test_coefficients': mass_coefficients, 'shift_projection_coefficients': shift_coefficients, 'scalar_product_remainder': phi_remainder, 'scalar_product_gradient_remainder': phi_gradient_remainder, 'mass_product_remainder': mass_remainder, 'mass_product_gradient_remainder': mass_gradient_remainder, 'shift_test_remainder': shift_remainder, 'scalar_acceleration_free': acceleration_free, 'Gram_combined': gram_scalar + gram_lapse + gram_mass + gram_shift if include_gram else zero, 'boundary_pair': inner_reaction + clock_port, 'node_at_face': Box(node_at_face), 'scalar_enriched_necessary_interior_obstruction': scalar_enriched_interior, 'scalar_enriched_Gram_pairing': gram_scalar_exact, 'shift_hat_neighbor_jump': positive_jump, 'diagnostics': {'scalar_product_projection': scalar_diagnostic, 'shift_test_projection': shift_diagnostic, 'scalar_acceleration': acceleration_diagnostic}}
