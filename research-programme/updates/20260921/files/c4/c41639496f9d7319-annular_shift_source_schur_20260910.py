import numpy as numerical
from scipy.linalg import solve

from annular_parent_coefficient_box_20260910 import Box, Taylor, down, up, concatenate
from annular_parent_root_residence_20260910 import action_enclosure, canonical_maps
from annular_implicit_parent_jets_20260910 import constraint_force_jets, shift_jets, set_coordinates, intersect
from annular_gram_joint_action_20260909 import gram_matrices


CHANNELS = ['bulk_transport', 'Gram_link_current', 'Gram_action_variation', 'outer_clock_rate', 'left_endpoint_acceleration', 'right_endpoint_acceleration']


def matrix_solve(matrix, load):
    vector = load.lo.ndim == 1
    load = Box(load.lo[:, None], load.hi[:, None]) if vector else load
    size = matrix.lo.shape[0]
    inverse = solve(matrix.midpoint, numerical.eye(size), assume_a='gen')
    majorant = (Box(numerical.eye(size)) - Box(inverse) @ matrix).magnitude
    contraction = float((Box(majorant) @ Box(numerical.ones(size))).hi.max())
    if not numerical.isfinite(contraction) or contraction >= 1:
        raise ValueError('Matrix comparison inverse gate failed: ' + str(contraction))
    center = solve(matrix.midpoint, load.midpoint, assume_a='gen')
    residual = (Box(inverse) @ (load - matrix @ Box(center))).magnitude
    radius = numerical.maximum(0., solve(numerical.eye(size) - majorant, residual, assume_a='gen'))
    margin = max(0., float(((Box(majorant) @ Box(radius) + Box(residual)).hi - radius).max()))
    padding = up((margin + 1e-13 * (1 + float(radius.max()))) / down(1 - contraction))
    radius = up(radius + padding)
    if not numerical.all((Box(majorant) @ Box(radius) + Box(residual)).hi <= radius):
        raise RuntimeError('Matrix comparison radius inequality failed.')
    result = Box(down(center - radius), up(center + radius))
    return (result[:, 0] if vector else result), {'contraction': contraction, 'maximum_radius': float(radius.max()), 'componentwise_majorant_verified': True}


def gram_variation_source(system, packed, configuration, mass_velocity):
    basis, count = system.basis, system.node_count
    factors, sampling = gram_matrices(count)
    embed = numerical.pad(factors, ((0, 0), (0, count)))
    mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
    nodes = Box(basis.radii)
    field_f = 1 - 2 * (Box(basis.face_to_node) @ mass) / nodes
    mass_time = Box(basis.face_to_node) @ mass_velocity
    leading = Box(factors) @ configuration[:count]
    leading_time = Box(factors) @ packed[system.slices[2]]
    density = (Box(sampling.T) @ leading**2) / (2 * basis.spacing)
    density_time = (Box(sampling.T) @ (leading * leading_time)) / basis.spacing
    mass_rate = Box(basis.face_to_node.T) @ (nodes * lapse * density_time * field_f**-.5 + lapse * density * mass_time * field_f**-1.5)
    lapse_rate = -nodes**2 * density_time * field_f**.5 + nodes * density * mass_time * field_f**-.5
    coefficient = nodes**2 * lapse * field_f**.5
    force = -(Box(embed.T) @ ((Box(sampling) @ coefficient) * (Box(embed) @ configuration) / basis.spacing))
    force = set_coordinates(force, [0, count - 1], Box(0.))
    return concatenate([mass_rate, lapse_rate, -force])


def source_decomposition(system, packed, configuration, momenta, clock, clock_rate, endpoint_acceleration, include_gram):
    if system.kappa != .1 or any(system.constants[name] != 0 for name in ['Lambda', 'm_chi', 'b2', 'b3']):
        raise ValueError('Only the canonical real-kappa=1/10 branch is supported.')
    basis, count = system.basis, system.node_count
    mass_all = numerical.arange(system.face_count)
    mass_free = numerical.intersect1d(system.free, mass_all)
    lapse_indices = numerical.arange(system.slices[1].start, system.slices[1].stop)
    velocity_free = numerical.intersect1d(system.free, numerical.arange(system.slices[2].start, system.count))
    if mass_free.size != lapse_indices.size:
        raise ValueError('The owned mixed mass/lapse dimensions are required.')
    total = action_enclosure(system, packed, configuration, momenta, clock, include_gram)
    bulk = action_enclosure(system, packed, configuration, momenta, clock, False)
    jacobian = total['jacobian']
    pairing, bulk_load = shift_jets(system, Taylor([packed]), Taylor([configuration]), False, 0)
    if include_gram:
        unused_pairing, full_load = shift_jets(system, Taylor([packed]), Taylor([configuration]), True, 0)
        gram_load = full_load[0] - bulk_load[0]
    else:
        full_load, gram_load = bulk_load, Box(numerical.zeros(system.face_count))
    split_load = concatenate([bulk_load[0][:, None], gram_load[:, None]], axis=1)
    mass_rates, shift_diagnostic = matrix_solve(pairing[0], split_load)
    if not include_gram:
        mass_rates = set_coordinates(mass_rates, (slice(None), 1), Box(0.))
    bulk_rate, gram_rate = mass_rates[:, 0], mass_rates[:, 1]
    full_rate = bulk_rate + gram_rate if include_gram else bulk_rate
    zero_packed = Box(numerical.zeros(system.count))
    bulk_path = set_coordinates(zero_packed, mass_all, bulk_rate)
    x_rate = packed[system.slices[2].start:]
    bulk_jet, unused_force = constraint_force_jets(system, Taylor([packed, bulk_path]), Taylor([configuration, x_rate]), Taylor([momenta, bulk['momentum_rate']]), Taylor([clock]), False)
    bulk_source = bulk_jet.coefficients[1]
    gram_current_source = bulk['jacobian'][:, mass_all] @ gram_rate if include_gram else zero_packed
    gram_action_source = gram_variation_source(system, packed, configuration, full_rate) if include_gram else zero_packed
    clock_source = set_coordinates(zero_packed, [system.face_count - 1], -Box(clock_rate) / (Box(1.) / 10))
    source_basis = concatenate([value[:, None] for value in [bulk_source, gram_current_source, gram_action_source, clock_source]] + [jacobian[:, system.fixed[1:]]], axis=1)
    channel_weights = Box(numerical.concatenate([numerical.ones(4), endpoint_acceleration]))
    sources = source_basis * channel_weights[None, :]
    absent = numerical.all(source_basis.magnitude == 0, axis=0)
    sources = set_coordinates(sources, (slice(None), absent), Box(0.))
    total_path = set_coordinates(zero_packed, mass_all, full_rate)
    total_path = set_coordinates(total_path, system.fixed[1:], Box(endpoint_acceleration))
    independent_jet, unused_force = constraint_force_jets(system, Taylor([packed, total_path]), Taylor([configuration, x_rate]), Taylor([momenta, total['momentum_rate']]), Taylor([clock, Box(clock_rate)]), include_gram)
    source_sum = sources @ Box(numerical.ones(len(CHANNELS)))
    assembly_difference = source_sum - independent_jet.coefficients[1]
    metric = numerical.concatenate([mass_free, lapse_indices])
    kinetic = jacobian[numerical.ix_(velocity_free, velocity_free)]
    kinetic_loads = concatenate([jacobian[numerical.ix_(velocity_free, metric)], source_basis[velocity_free]], axis=1)
    velocity_responses, kinetic_diagnostic = matrix_solve(kinetic, kinetic_loads)
    metric_response = velocity_responses[:, :metric.size]
    source_response = velocity_responses[:, metric.size:]
    schur = jacobian[numerical.ix_(metric, metric)] - jacobian[numerical.ix_(metric, velocity_free)] @ metric_response
    reduced_sources = source_basis[metric] - jacobian[numerical.ix_(metric, velocity_free)] @ source_response
    value_map, unused_gradient = canonical_maps(basis)
    velocity_map = value_map[:, velocity_free - system.slices[2].start]
    lapse_q = Box(basis.node_value) @ packed[system.slices[1]]
    field_f = 1 - 2 * (Box(basis.face_value) @ packed[system.slices[0]]) / basis.quadrature
    velocity_q = Box(value_map) @ packed[system.slices[2].start:]
    weight = Box(basis.quadrature_weights) * Box(basis.quadrature)**2 / (lapse_q * field_f**.5)
    lapse_product = (velocity_q / lapse_q)[:, None] * Box(basis.node_value)
    projected_remainder = lapse_product + Box(velocity_map) @ metric_response[:, count:]
    projection_gram = projected_remainder.T @ (weight[:, None] * projected_remainder)
    schur_nn = intersect(schur[count:, count:], projection_gram)
    schur_mm, schur_mn, schur_nm = schur[:count, :count], schur[:count, count:], schur[count:, :count]
    lapse_loads = concatenate([reduced_sources[:count], schur_mm], axis=1)
    lapse_responses, lapse_diagnostic = matrix_solve(schur_mn, -lapse_loads)
    trial_lapse = lapse_responses[:, :len(CHANNELS)]
    lapse_mass_response = lapse_responses[:, len(CHANNELS):]
    direct_source = reduced_sources[count:]
    projection_source = schur_nn @ trial_lapse
    obstruction_channels = direct_source + projection_source
    mass_operator = schur_nm + schur_nn @ lapse_mass_response
    mass_corrections, mass_diagnostic = matrix_solve(mass_operator, -obstruction_channels)
    shift_channels = pairing[0][:, mass_free] @ mass_corrections
    direct_shift, direct_diagnostic = matrix_solve(mass_operator, -direct_source)
    direct_shift = pairing[0][:, mass_free] @ direct_shift
    projection_shift, projection_diagnostic = matrix_solve(mass_operator, -projection_source)
    projection_shift = pairing[0][:, mass_free] @ projection_shift
    obstruction_basis = obstruction_channels
    boundary_rows = numerical.array([0, count - 1])
    boundary_columns = obstruction_basis[:, 4:]
    other_obstruction = obstruction_basis[:, :4] @ Box(numerical.ones(4))
    boundary_acceleration, boundary_diagnostic = matrix_solve(boundary_columns[boundary_rows], -other_obstruction[boundary_rows])
    boundary_obstruction = other_obstruction + boundary_columns @ boundary_acceleration
    boundary_forcing = set_coordinates(boundary_obstruction, boundary_rows, Box(0.))
    boundary_mass_response, boundary_response_diagnostic = matrix_solve(mass_operator, -boundary_forcing)
    boundary_shift_response = pairing[0][:, mass_free] @ boundary_mass_response
    reduced_sources = set_coordinates(reduced_sources * channel_weights[None, :], (slice(None), absent), Box(0.))
    trial_lapse = set_coordinates(trial_lapse * channel_weights[None, :], (slice(None), absent), Box(0.))
    direct_source = set_coordinates(direct_source * channel_weights[None, :], (slice(None), absent), Box(0.))
    projection_source = set_coordinates(projection_source * channel_weights[None, :], (slice(None), absent), Box(0.))
    obstruction_channels = set_coordinates(obstruction_channels * channel_weights[None, :], (slice(None), absent), Box(0.))
    mass_corrections = set_coordinates(mass_corrections * channel_weights[None, :], (slice(None), absent), Box(0.))
    shift_channels = set_coordinates(shift_channels * channel_weights[None, :], (slice(None), absent), Box(0.))
    direct_shift = set_coordinates(direct_shift * channel_weights[None, :], (slice(None), absent), Box(0.))
    projection_shift = set_coordinates(projection_shift * channel_weights[None, :], (slice(None), absent), Box(0.))
    mismatch_lower, mismatch_upper = numerical.zeros(system.face_count), numerical.zeros(system.face_count)
    mismatch = mass_corrections @ Box(numerical.ones(len(CHANNELS)))
    mismatch_lower[mass_free], mismatch_upper[mass_free] = mismatch.lo, mismatch.hi
    source_defect = shift_channels @ Box(numerical.ones(len(CHANNELS)))
    return {'sources': sources, 'summed_source': source_sum, 'independent_source': independent_jet.coefficients[1], 'assembly_difference': assembly_difference, 'kinetic': kinetic, 'schur_mm': schur_mm, 'schur_mn': schur_mn, 'schur_nm': schur_nm, 'schur_nn': schur_nn, 'projection_gram': projection_gram, 'projection_remainder': projected_remainder, 'reduced_sources': reduced_sources, 'direct_obstruction_channels': direct_source, 'projection_obstruction_channels': projection_source, 'obstruction_channels': obstruction_channels, 'trial_lapse_channels': trial_lapse, 'mass_operator': mass_operator, 'mass_correction_channels': mass_corrections, 'shift_channels': shift_channels, 'direct_shift_channels': direct_shift, 'projection_shift_channels': projection_shift, 'source_shift_defect': source_defect, 'source_mass_mismatch': Box(mismatch_lower, mismatch_upper), 'pairing': pairing[0], 'full_shift_rate': full_rate, 'bulk_shift_rate': bulk_rate, 'Gram_shift_rate': gram_rate, 'unit_boundary_obstruction': boundary_columns, 'non_boundary_obstruction': other_obstruction, 'required_boundary_acceleration': boundary_acceleration, 'boundary_repaired_obstruction': boundary_obstruction, 'boundary_repaired_shift': boundary_shift_response, 'diagnostics': {'shift': shift_diagnostic, 'kinetic': kinetic_diagnostic, 'lapse_trial': lapse_diagnostic, 'mass_response': mass_diagnostic, 'direct_response': direct_diagnostic, 'projection_response': projection_diagnostic, 'boundary_acceleration': boundary_diagnostic, 'boundary_shift_response': boundary_response_diagnostic}, 'minimum_F': total['minimum_F'], 'minimum_N': total['minimum_N']}
