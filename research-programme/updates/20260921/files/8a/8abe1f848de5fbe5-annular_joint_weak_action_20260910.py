import numpy as numerical

from annular_adm_mixed_action_20260909 import linear_value_gradient
from annular_parent_coefficient_box_20260910 import Box, Taylor, concatenate
from annular_parent_root_residence_20260910 import canonical_maps
from annular_shift_source_schur_20260910 import matrix_solve
from annular_implicit_parent_jets_20260910 import shift_jets
from annular_gram_joint_action_20260909 import gram_matrices


def integrate_links(links, values):
    lower = numerical.zeros((links.node.size, values.lo.shape[1]))
    upper = lower.copy()
    from annular_parent_coefficient_box_20260910 import down, up
    for point, pair in enumerate(links.pairs):
        addition = values[point] * links.weights[point]
        lower[pair] = down(lower[pair] + addition.lo)
        upper[pair] = up(upper[pair] + addition.hi)
    return Box(lower, upper)


def bubble_maps(basis):
    knots = numerical.unique(numerical.concatenate([basis.radii, basis.faces]))
    segment = numerical.searchsorted(knots, basis.quadrature, side='right') - 1
    width = knots[segment + 1] - knots[segment]
    fraction = (basis.quadrature - knots[segment]) / width
    even = 4 * fraction * (1 - fraction)
    even_gradient = 4 * (1 - 2 * fraction) / width
    odd = even * (2 * fraction - 1)
    odd_gradient = even_gradient * (2 * fraction - 1) + 2 * even / width
    values = numerical.zeros((basis.quadrature.size, 2 * (knots.size - 1)))
    gradients = numerical.zeros_like(values)
    rows = numerical.arange(basis.quadrature.size)
    values[rows, 2 * segment], values[rows, 2 * segment + 1] = even, odd
    gradients[rows, 2 * segment], gradients[rows, 2 * segment + 1] = even_gradient, odd_gradient
    return values, gradients, segment, even, odd


def joint_prototype(system, packed, configuration, include_gram):
    basis, links, count = system.basis, system.links, system.node_count
    value_map, gradient_map = canonical_maps(basis)
    radius, weights = Box(basis.quadrature), Box(basis.quadrature_weights)
    face, face_gradient = Box(basis.face_value), Box(basis.face_gradient)
    eta, eta_gradient = Box(basis.node_value[:, 1:-1]), Box(basis.node_gradient[:, 1:-1])
    mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
    mass_q, mass_r = face @ mass, face_gradient @ mass
    lapse_q = Box(basis.node_value) @ lapse
    lapse_r = Box(basis.node_gradient) @ lapse
    velocity = Box(value_map) @ packed[system.slices[2].start:]
    gradient = Box(gradient_map) @ configuration
    spatial_f = 1 - 2 * mass_q / radius
    kappa = Box(1.) / 10
    rho = 1 / (kappa * lapse_q * spatial_f**1.5)
    scalar_flux = kappa * radius**2 * spatial_f * velocity * gradient
    zeta = (spatial_f * lapse_q)[:, None] * eta_gradient - (spatial_f * lapse_r)[:, None] * eta
    pairing, full_load = shift_jets(system, Taylor([packed]), Taylor([configuration]), include_gram, 0)
    old_rate, old_diagnostic = matrix_solve(pairing[0], full_load[0])
    old_speed = face @ old_rate
    shift_coefficients, project_diagnostic = matrix_solve(pairing[0], face.T @ ((weights * rho)[:, None] * zeta))
    remainder = zeta - face @ shift_coefficients
    zero = Box(numerical.zeros(count - 2))
    gram_old, gram_gauss, gram_exact = Box(numerical.zeros(system.face_count)), zero, zero
    gram_scalar, gram_lapse, gram_mass = zero, zero, zero
    current = Box(numerical.zeros(links.node.size))
    endpoint_kernel = Box(numerical.zeros((links.node.size, count - 2)))
    gauss_kernel = endpoint_kernel
    if include_gram:
        factors, sampling = gram_matrices(count)
        leading = Box(factors) @ configuration[:count]
        leading_time = Box(factors) @ packed[system.slices[2]]
        nodes = Box(basis.radii)
        node_f = 1 - 2 * (Box(basis.face_to_node) @ mass) / nodes
        coefficient = nodes**2 * lapse * node_f**.5
        factor_coefficient = Box(sampling) @ coefficient
        density = (Box(sampling.T) @ leading**2) / (2 * basis.spacing)
        density_time = (Box(sampling.T) @ (leading * leading_time)) / basis.spacing
        current = coefficient[links.node] * links.sweight * leading[links.factor] * leading_time[links.factor] / basis.spacing
        current = current - packed[system.slices[2]][links.node] * links.tweight * factor_coefficient[links.factor] * leading[links.factor] / basis.spacing
        anchor_map = Box(linear_value_gradient(basis.radii, links.anchors)[0])
        node_eta = Box(numerical.eye(count)[links.node, 1:-1])
        endpoint_kernel = node_eta / lapse[links.node, None] - anchor_map[:, 1:-1] / (anchor_map @ lapse)[:, None]
        link_eta, link_eta_r = linear_value_gradient(basis.radii, links.points)
        link_lapse = Box(link_eta) @ lapse
        link_lapse_r = Box(link_eta_r) @ lapse
        integrand = Box(link_eta_r[:, 1:-1]) / link_lapse[:, None] - Box(link_eta[:, 1:-1]) * (link_lapse_r / link_lapse**2)[:, None]
        gauss_kernel = integrate_links(links, integrand)
        gram_exact = -(endpoint_kernel.T @ current)
        gram_gauss = -(gauss_kernel.T @ current)
        unused_pairing, bulk_load = shift_jets(system, Taylor([packed]), Taylor([configuration]), False, 0)
        gram_old = full_load[0] - bulk_load[0]
        gram_scalar = (packed[system.slices[2]] / lapse * (Box(factors.T) @ (factor_coefficient * leading / basis.spacing)))[1:-1]
        node_speed = Box(basis.face_to_node) @ old_rate
        gram_lapse = (-nodes**2 * density_time * node_f**.5 + nodes * density * node_speed * node_f**-.5)[1:-1]
        gram_mass = (nodes * density * node_speed * node_f**-.5)[1:-1]
    gram_identity = gram_scalar + gram_lapse - gram_mass - gram_exact if include_gram else zero
    gram_quadrature_remainder = gram_exact - gram_gauss if include_gram else zero
    residual_old_zeta = zeta.T @ (weights * rho * (old_speed - scalar_flux)) - gram_gauss
    bubble_value, bubble_gradient, segment, even, odd = bubble_maps(basis)
    bubble = Box(bubble_value)
    moments = bubble.T @ ((weights * rho)[:, None] * remainder)
    cell_count = bubble_value.shape[1] // 2
    diagonal_even, mixed, diagonal_odd = [Box(numerical.zeros(cell_count)) for unused in range(3)]
    rows_even, rows_mixed, rows_odd = [], [], []
    for cell in range(cell_count):
        selected = numerical.flatnonzero(segment == cell)
        local_weight = (weights * rho)[selected]
        rows_even.append((Box(even[selected])**2) @ local_weight)
        rows_mixed.append((Box(even[selected]) * Box(odd[selected])) @ local_weight)
        rows_odd.append((Box(odd[selected])**2) @ local_weight)
    diagonal_even = concatenate([value[None] for value in rows_even])
    mixed = concatenate([value[None] for value in rows_mixed])
    diagonal_odd = concatenate([value[None] for value in rows_odd])
    determinant = diagonal_even * diagonal_odd - mixed**2
    if min(float(diagonal_even.lo.min()), float(determinant.lo.min())) <= 0:
        raise ValueError('Local bubble Gram positivity failed.')
    first = (diagonal_odd[:, None] * moments[0::2] - mixed[:, None] * moments[1::2]) / determinant[:, None]
    second = (diagonal_even[:, None] * moments[1::2] - mixed[:, None] * moments[0::2]) / determinant[:, None]
    lift_lower, lift_upper = numerical.zeros_like(moments.lo), numerical.zeros_like(moments.hi)
    lift_lower[0::2], lift_upper[0::2] = first.lo, first.hi
    lift_lower[1::2], lift_upper[1::2] = second.lo, second.hi
    lift = Box(lift_lower, lift_upper)
    mass_lift = bubble @ lift
    mass_lift_gradient = Box(bubble_gradient) @ lift
    enriched_pairing = moments.T @ lift
    projected_load = remainder.T @ (weights * rho * scalar_flux) + gram_gauss - shift_coefficients.T @ gram_old
    enrichment_rate, enrichment_diagnostic = matrix_solve(enriched_pairing, projected_load)
    induced_mass = mass_lift @ enrichment_rate
    base_rate, base_diagnostic = matrix_solve(pairing[0], full_load[0] - face.T @ (weights * rho * induced_mass))
    new_speed = face @ base_rate + induced_mass
    original_residual = face.T @ (weights * rho * new_speed) - full_load[0]
    enriched_residual = zeta.T @ (weights * rho * (new_speed - scalar_flux)) - gram_gauss
    mass_density = lapse_q * mass_r / (kappa * radius) * spatial_f**-1.5 + radius * velocity**2 / (2 * lapse_q) * spatial_f**-1.5 + radius * lapse_q * gradient**2 / 2 * spatial_f**-.5
    mass_gradient_density = lapse_q / kappa * spatial_f**-.5
    added_mass_equations = mass_lift.T @ (weights * mass_density) + mass_lift_gradient.T @ (weights * mass_gradient_density)
    orthogonality = face.T @ ((weights * rho)[:, None] * remainder)
    pairing_identity = remainder.T @ ((weights * rho)[:, None] * mass_lift) - enriched_pairing
    return {'zeta': zeta, 'shift_projection_coefficients': shift_coefficients, 'shift_test_remainder': remainder, 'pairing': pairing[0], 'original_mass_rate': old_rate, 'original_enriched_shift_residual': residual_old_zeta, 'Gram_endpoint_kernel': endpoint_kernel, 'Gram_gauss_kernel': gauss_kernel, 'Gram_link_current': current, 'Gram_scalar': gram_scalar, 'Gram_lapse_time': gram_lapse, 'Gram_mass_product': gram_mass, 'Gram_endpoint_shift': gram_exact, 'Gram_gauss_shift': gram_gauss, 'Gram_joint_cancellation': gram_identity, 'Gram_link_quadrature_remainder': gram_quadrature_remainder, 'bubble_value': bubble, 'bubble_gradient': Box(bubble_gradient), 'bubble_moments': moments, 'bubble_lift_coefficients': lift, 'local_bubble_determinant': determinant, 'mass_lift': mass_lift, 'mass_lift_gradient': mass_lift_gradient, 'enriched_pairing': enriched_pairing, 'enrichment_rate': enrichment_rate, 'base_mass_rate': base_rate, 'new_mass_speed': new_speed, 'new_mass_speed_gradient': face_gradient @ base_rate + mass_lift_gradient @ enrichment_rate, 'mass_speed_change': new_speed - old_speed, 'original_shift_residual_after_enrichment': original_residual, 'enriched_shift_residual_after_enrichment': enriched_residual, 'added_mass_equations': added_mass_equations, 'projected_shift_load': projected_load, 'shift_projection_orthogonality': orthogonality, 'enriched_pairing_identity': pairing_identity, 'diagnostics': {'original_shift': old_diagnostic, 'shift_projection': project_diagnostic, 'enriched_pairing': enrichment_diagnostic, 'base_mass_rate': base_diagnostic}}


def weak_bulk_directional_control(system, packed, configuration, momenta, clock, data):
    basis, count = system.basis, system.node_count
    value_map, gradient_map = canonical_maps(basis)
    center = packed.midpoint
    mass, lapse = center[system.slices[0]], center[system.slices[1]]
    mass_q, mass_r = basis.face_value @ mass, basis.face_gradient @ mass
    lapse_q, lapse_r = basis.node_value @ lapse, basis.node_gradient @ lapse
    velocity = value_map @ center[system.slices[2].start:]
    velocity_r = gradient_map @ center[system.slices[2].start:]
    gradient = gradient_map @ configuration
    eta, eta_r = basis.node_value[:, 1], basis.node_gradient[:, 1]
    phi = eta * velocity / lapse_q
    phi_r = eta_r * velocity / lapse_q + eta * (velocity_r / lapse_q - velocity * lapse_r / lapse_q**2)
    mass_scale = max(1., float(abs(data['mass_lift'].midpoint[:, 0]).max()))
    shift_scale = max(1., float(abs(data['zeta'].midpoint[:, 0]).max()))
    change_mass = data['mass_lift'].midpoint[:, 0] / mass_scale
    change_mass_r = data['mass_lift_gradient'].midpoint[:, 0] / mass_scale
    change_shift = data['zeta'].midpoint[:, 0] / shift_scale
    endpoint_value, endpoint_gradient = linear_value_gradient(basis.radii, basis.radii[[0, -1]])
    endpoint_lapse = endpoint_value @ lapse
    endpoint_lapse_r = endpoint_gradient @ lapse
    endpoint_f = 1 - 2 * mass[[0, -1]] / basis.radii[[0, -1]]
    endpoint_shift = endpoint_f * (endpoint_lapse * endpoint_gradient[:, 1] - endpoint_value[:, 1] * endpoint_lapse_r) / shift_scale
    endpoint_eta = endpoint_value[:, 1]
    background = [mass_q, mass_r, data['new_mass_speed'].midpoint, lapse_q, lapse_r, velocity, gradient, numerical.zeros_like(velocity)]
    directions = [change_mass, change_mass_r, change_mass, eta, eta_r, phi, phi_r, change_shift]

    def density(values):
        local_mass, local_mass_r, local_speed, local_lapse, local_lapse_r, local_velocity, local_gradient, shift = values
        radius = basis.quadrature
        spatial_f = 1 - 2 * local_mass / radius
        scale = spatial_f**-.5
        scale_r = (local_mass_r / radius - local_mass / radius**2) * spatial_f**-1.5
        gravity = local_lapse * local_mass_r * scale / .1
        gravity = gravity + shift * local_speed / (.1 * local_lapse * spatial_f**1.5)
        gravity = gravity - radius * (scale_r * local_lapse + scale * local_lapse_r) * shift**2 / (.2 * local_lapse**2)
        matter = radius**2 * scale * (local_velocity - shift * local_gradient)**2 / (2 * local_lapse) - radius**2 * local_lapse * local_gradient**2 / (2 * scale)
        return gravity + matter

    def floating_action(amplitude):
        values = [value + amplitude * change for value, change in zip(background, directions)]
        endpoint_flux = basis.radii[[0, -1]] * endpoint_f**-.5 * (amplitude * endpoint_shift)**2 / (.2 * (endpoint_lapse + amplitude * endpoint_eta))
        return numerical.dot(basis.quadrature_weights, density(values)) - endpoint_flux[-1] + endpoint_flux[0] - clock * mass[-1] / .1

    series = density([Taylor([Box(value), Box(change)]) for value, change in zip(background, directions)])
    endpoint_flux = Box(basis.radii[[0, -1]] * endpoint_f**-.5) * Taylor([Box(numerical.zeros(2)), Box(endpoint_shift)])**2 / (.2 * Taylor([Box(endpoint_lapse), Box(endpoint_eta)]))
    coefficients = [Box(basis.quadrature_weights) @ coefficient - flux[1] + flux[0] for coefficient, flux in zip(series.coefficients, endpoint_flux.coefficients)]
    coefficients[0] = coefficients[0] - clock * mass[-1] / .1
    complex_first = float(numerical.imag(floating_action(1e-25j)) / 1e-25)
    step = 1e-3
    centered_second = float((floating_action(step) + floating_action(-step) - 2 * floating_action(0.)) / (2 * step**2))
    old_value = system.independent_action(center, False) + numerical.dot(momenta, center[system.slices[2].start:])
    return {'zero_shift_bulk_embedding_error': float(abs(floating_action(0.) - old_value)), 'first_variation_error': float(abs(complex_first - coefficients[1].midpoint)), 'second_coefficient_error': float(abs(centered_second - coefficients[2].midpoint)), 'second_coefficient': float(coefficients[2].midpoint), 'boundary_quadratic_flux': float(max(abs((basis.radii[[0, -1]] * endpoint_f**-.5 * endpoint_shift**2 / (.2 * endpoint_lapse))))), 'scope': 'Uncertified midpoint derivative controls for the nonlinear weak bulk action with retained physical boundary flux; Gram first variation is separately enclosed, not a full nonlinear Gram-interface implementation.'}
