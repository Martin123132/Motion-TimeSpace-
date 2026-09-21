import numpy as numerical
from scipy.linalg import eigvalsh, solve

from annular_first_derivative_energy_20260909 import affine_lift_matrix, canonical_matrices
from annular_endpoint_commutator_bound_20260910 import endpoint_defect_bound
from annular_paired_variational_energy_20260910 import graph_operators, scalar_maps, symmetric
from annular_spatial_clock_energy_20260909 import linear_series, profile


def trace_feedback(system, packed, speed, include_gram):
    basis = system.basis
    count = basis.radii.size
    free = numerical.array([index for index in range(2 * count) if index not in [0, count - 1]])
    selection = numerical.ix_(free, free)
    matrices = canonical_matrices(system, packed, speed, include_gram)
    mass, stiffness, mass_time, stiffness_time = [matrices[name][selection] for name in ['M', 'K', 'M_dot', 'K_dot']]
    operators = graph_operators(mass, stiffness, mass_time, stiffness_time)
    potential = solve(stiffness, mass, assume_a='sym')

    def local_maps(points):
        data = profile(system, packed, speed, points)
        maps = scalar_maps(basis, points)[:, :, free]
        characteristic, characteristic_r = data['c'][:2]
        theta, theta_r = data['theta'][:2]
        ratio = 2 * characteristic**2 / points + characteristic * characteristic_r
        static = (-ratio[:, None] * maps[1] - characteristic[:, None]**2 * maps[2]) @ potential
        gradient = -(characteristic**2 * theta_r)[:, None] * (maps[1] @ potential)
        source = theta[:, None] * static + gradient
        return {'maps': maps, 'c': characteristic, 'theta': theta, 'theta_r': theta_r, 'ratio': ratio, 'static': static, 'gradient': gradient, 'source': source}

    volume = local_maps(basis.quadrature)
    endpoint = local_maps(basis.radii[[0, -1]])
    weights = basis.quadrature_weights * basis.quadrature**2 / volume['c']
    value = volume['maps'][0]
    projection = solve(mass, value.T * weights, assume_a='sym')
    lift = affine_lift_matrix(basis)
    endpoint_lift = solve(mass, (matrices['M'] @ lift)[free], assume_a='sym')
    gram = solve(mass, matrices['K_Gram_dot'][selection] @ potential, assume_a='sym')
    radial_weight = basis.quadrature_weights * basis.quadrature**2 * volume['c'] * volume['theta']
    quadrature_rhs = volume['maps'][1].T @ (radial_weight[:, None] * (volume['maps'][1] @ potential)) - value.T @ (weights[:, None] * volume['source'])
    quadrature = solve(mass, quadrature_rhs, assume_a='sym')
    trace = endpoint['source']
    zero_trace = projection @ (volume['source'] - scalar_maps(basis, basis.quadrature)[0] @ lift @ trace)
    reconstructed = endpoint_lift @ trace + zero_trace + gram + quadrature - operators['A']
    regular = operators['configuration_transport'] - endpoint_lift @ trace
    regular_form = symmetric(stiffness @ regular) + .5 * stiffness_time
    feedback_norm = numerical.sqrt(max(float(eigvalsh(trace @ solve(stiffness, trace.T, assume_a='sym'))[-1]), 0.))
    gradient_trace_norm = numerical.sqrt(max(float(eigvalsh(endpoint['gradient'] @ solve(stiffness, endpoint['gradient'].T, assume_a='sym'))[-1]), 0.))
    regular_rate = max(0., 2 * float(eigvalsh(regular_form, stiffness)[-1]), 2 * operators['velocity_rate'])
    slope_rows = numerical.array([int(numerical.flatnonzero(free == index)[0]) for index in [count, 2 * count - 1]])
    slope_balance = stiffness[slope_rows] @ potential - mass[slope_rows]
    gradient_regular = operators['configuration_transport'] - endpoint_lift @ endpoint['gradient']
    gradient_form = symmetric(stiffness @ gradient_regular) + .5 * stiffness_time
    gradient_regular_rate = max(0., 2 * float(eigvalsh(gradient_form, stiffness)[-1]), 2 * operators['velocity_rate'])
    return {'free': free, 'matrices': matrices, 'mass': mass, 'stiffness': stiffness, 'operators': operators, 'potential': potential, 'volume': volume, 'endpoint': endpoint, 'projection': projection, 'endpoint_lift': endpoint_lift, 'trace': trace, 'zero_trace': zero_trace, 'gram': gram, 'quadrature': quadrature, 'quadrature_rhs': quadrature_rhs, 'reconstructed': reconstructed, 'regular': regular, 'regular_form': regular_form, 'feedback_K_to_R2': float(feedback_norm), 'gradient_trace_K_to_R2': float(gradient_trace_norm), 'regular_growth': float(regular_rate), 'gradient_regular': gradient_regular, 'gradient_regular_form': gradient_form, 'gradient_regular_growth': float(gradient_regular_rate), 'slope_rows': slope_rows, 'slope_balance': slope_balance}


def released_slope_moments(system, packed, speed, result):
    basis = system.basis
    count = basis.radii.size
    endpoints = basis.radii[[0, -1]]
    endpoint_maps = scalar_maps(basis, endpoints)[:, :, result['free']]
    potential = result['potential']
    weights = basis.quadrature_weights
    coordinate = basis.quadrature
    data = result['volume']
    radial_density = coordinate**2 * data['c']
    mass_density = coordinate**2 / data['c']
    rows = []
    for side, direction in [(0, 1.), (1, -1.)]:
        distance = direction * (coordinate - endpoints[side])
        active = (distance > 0.) & (distance < basis.spacing)
        fraction = distance[active] / basis.spacing
        test = basis.spacing * fraction * (1 - fraction)**2
        test_r = direction * (1 - 4 * fraction + 3 * fraction**2)
        first = endpoint_maps[1, side] @ potential
        third = endpoint_maps[3, side] @ potential
        coefficient_first = numerical.dot(weights[active], radial_density[active] * test_r)
        coefficient_second = numerical.dot(weights[active], radial_density[active] * test_r * (coordinate[active] - endpoints[side]))
        coefficient_third = .5 * numerical.dot(weights[active], radial_density[active] * test_r * (coordinate[active] - endpoints[side])**2)
        forcing = (weights[active] * mass_density[active] * test) @ data['maps'][0, active]
        predicted_second = (forcing - coefficient_first * first - coefficient_third * third) / coefficient_second
        direct_second = endpoint_maps[2, side] @ potential
        rows.append({'coefficient_first': float(coefficient_first), 'coefficient_second': float(coefficient_second), 'coefficient_third': float(coefficient_third), 'forcing': forcing, 'predicted_second': predicted_second, 'direct_second': direct_second, 'third': third, 'first': first, 'test': test, 'direction': direction})
    return rows


def gradient_trace_map(system, packed, speed, include_gram):
    basis = system.basis
    count = basis.radii.size
    free = numerical.array([index for index in range(2 * count) if index not in [0, count - 1]])
    selection = numerical.ix_(free, free)
    matrices = canonical_matrices(system, packed, speed, include_gram)
    potential = solve(matrices['K'][selection], matrices['M'][selection], assume_a='sym')
    data = profile(system, packed, speed, basis.radii[[0, -1]])
    derivatives = scalar_maps(basis, basis.radii[[0, -1]])[1][:, free] @ potential
    return -(data['c'][0]**2 * data['theta'][1])[:, None] * derivatives


def normal_form(system, packed, speed, second, result):
    basis = system.basis
    endpoints = basis.radii[[0, -1]]
    mass_field, mass_r = linear_series(basis.faces, packed[system.slices[0]], endpoints, 'right')[:2]
    lapse, lapse_r = linear_series(basis.radii, packed[system.slices[1]], endpoints, 'right')[:2]
    mass_time, mass_time_r = linear_series(basis.faces, speed[system.slices[0]], endpoints, 'right')[:2]
    lapse_time, lapse_time_r = linear_series(basis.radii, speed[system.slices[1]], endpoints, 'right')[:2]
    mass_second, mass_second_r = linear_series(basis.faces, second[system.slices[0]], endpoints, 'right')[:2]
    lapse_second, lapse_second_r = linear_series(basis.radii, second[system.slices[1]], endpoints, 'right')[:2]
    denominator = endpoints - 2 * mass_field
    denominator_r = 1 - 2 * mass_r
    theta_time_r = lapse_second_r / lapse - lapse_second * lapse_r / lapse**2
    theta_time_r -= 2 * lapse_time / lapse * (lapse_time_r / lapse - lapse_time * lapse_r / lapse**2)
    theta_time_r -= mass_second_r / denominator - mass_second * denominator_r / denominator**2
    theta_time_r -= 4 * mass_time * mass_time_r / denominator**2 - 4 * mass_time**2 * denominator_r / denominator**3
    endpoint = result['endpoint']
    coefficient = endpoint['c']**2 * endpoint['theta_r']
    coefficient_time = endpoint['c']**2 * (2 * endpoint['theta'] * endpoint['theta_r'] + theta_time_r)
    endpoint_derivative = endpoint['maps'][1] @ result['potential']
    trace = -coefficient[:, None] * endpoint_derivative
    source = -coefficient_time[:, None] * endpoint_derivative
    operators, mass = result['operators'], result['mass']
    trace_time = source - trace @ operators['configuration_transport']
    lift = result['endpoint_lift']
    free = result['free']
    selection = numerical.ix_(free, free)
    lift_time = solve(mass, (result['matrices']['M_dot'] @ affine_lift_matrix(basis))[free] - result['matrices']['M_dot'][selection] @ lift, assume_a='sym')
    defect = lift_time - operators['velocity_transport'] @ lift
    coupling = defect @ trace + lift @ source - lift @ trace @ lift @ trace
    velocity_transport = operators['velocity_transport'] + lift @ trace
    velocity_form = symmetric(mass @ velocity_transport) + .5 * result['matrices']['M_dot'][selection]
    count_free = mass.shape[0]
    zero = numerical.zeros_like(mass)
    metric = numerical.block([[result['stiffness'], zero], [zero, mass]])
    cross = .5 * coupling.T @ mass
    work = numerical.block([[result['gradient_regular_form'], cross], [cross.T, velocity_form]])
    growth = max(0., 2 * float(eigvalsh(work, metric)[-1]))
    return {'trace': trace, 'source': source, 'trace_time': trace_time, 'coefficient': coefficient, 'coefficient_time': coefficient_time, 'theta_time_r': theta_time_r, 'lift_time': lift_time, 'endpoint_defect': defect, 'coupling': coupling, 'velocity_transport': velocity_transport, 'velocity_form': velocity_form, 'metric': metric, 'work': work, 'growth': growth, 'dimension': count_free}


def normal_form_bounds(system, packed, speed, include_gram, normal):
    inherited = endpoint_defect_bound(system, packed, speed, include_gram)
    envelope = inherited['envelope']
    derivative_sup = inherited['transport']['elliptic_derivative_sup_constant']
    trace_bound = derivative_sup * numerical.linalg.norm(normal['coefficient'])
    source_bound = derivative_sup * numerical.linalg.norm(normal['coefficient_time'])
    poincare = envelope['length'] * numerical.sqrt(envelope['m_max'] / envelope['p_min'])
    lift_bound = inherited['endpoint_lift_M_bound']
    defect_bound = inherited['endpoint_transport_M_bound']
    coupling_bound = defect_bound * trace_bound + lift_bound * source_bound + lift_bound**2 * trace_bound**2
    shear_bound = lift_bound * trace_bound * poincare
    added_growth = 2 * lift_bound * trace_bound + poincare * coupling_bound
    return {'trace_M_to_R2_upper': float(trace_bound), 'source_M_to_R2_upper': float(source_bound), 'poincare_M_over_K': float(poincare), 'lift_R2_to_M_upper': float(lift_bound), 'endpoint_defect_R2_to_M_upper': float(defect_bound), 'coupling_M_to_M_upper': float(coupling_bound), 'shear_K_to_M_upper': float(shear_bound), 'norm_equivalence_factor_upper': float(1 + shear_bound), 'added_growth_over_regular_upper': float(added_growth), 'clock_curvature_radius': inherited['curvature']['clock_curvature_radius'], 'scope': 'Analytic conditional coefficient bounds, not interval-certified and not a proof of regular-transport growth or parent propagation.'}
