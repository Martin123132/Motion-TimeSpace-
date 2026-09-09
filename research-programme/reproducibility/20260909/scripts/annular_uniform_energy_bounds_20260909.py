import numpy as numerical
import sympy as symbolic

from annular_adm_mixed_action_20260909 import linear_value_gradient


INVERSE_CONSTANT = 16.0
RIGHT_VALUE_CONSTANT = 2.0
RIGHT_GRADIENT_CONSTANT = 13.0
HERMITE_ERROR_CONSTANT = 2.0
GRAM_ROW_BOUND = 1.0 / 8.0


def exact_certificates():
    coordinate = symbolic.Symbol('coordinate', real=True)
    monomials = symbolic.Matrix([[coordinate**degree for degree in range(4)]])
    right = symbolic.Matrix([[(3 * coordinate**2 - 2 * coordinate**3) + degree * (coordinate**3 - coordinate**2) for degree in range(4)]])
    gram = symbolic.integrate(monomials.T * monomials, (coordinate, 0, 1))
    derivative = symbolic.integrate(monomials.diff(coordinate).T * monomials.diff(coordinate), (coordinate, 0, 1))
    right_gram = symbolic.integrate(right.T * right, (coordinate, 0, 1))
    right_derivative = symbolic.integrate(right.diff(coordinate).T * right.diff(coordinate), (coordinate, 0, 1))
    certificates = {}
    for name, matrix in [('inverse_16', 256 * gram - derivative), ('right_2', 4 * gram - right_gram), ('right_gradient_13', 169 * gram - right_derivative)]:
        minors = [symbolic.factor(matrix[:size, :size].det()) for size in range(1, 5)]
        certificates[name] = {'positive': all(value > 0 for value in minors), 'leading_principal_minors': [str(value) for value in minors]}
    rational = symbolic.Rational
    diagonals = [rational(59097, 573104), rational(1825, 25284), rational(491, 7056), rational(5, 72)]
    off_rows = [rational(253, 50568) + rational(1, 392), rational(253, 50568) + rational(3, 392), rational(3, 392) + rational(1, 144) + rational(1, 392), rational(1, 72)]
    certificates['all_Gram_row_types'] = {'positive': all(diagonal - off > 0 and diagonal + off < rational(1, 8) for diagonal, off in zip(diagonals, off_rows)), 'diagonals': list(map(str, diagonals)), 'absolute_off_row_sums': list(map(str, off_rows)), 'scope': 'left three boundary rows, interior; right rows are reflections; disjoint for n>=17'}
    certificates['Hermite_H2_constant_2'] = {'positive': rational(7, 15)**2 - rational(16, 75) > 0, 'radical_inequality_margin': str(rational(7, 15)**2 - rational(16, 75)), 'statement': 'sqrt(2/5)+sqrt(2/15)<1, hence ||(Iu-u)prime||<=2h||u_second||'}
    return certificates


def metric_envelope(basis, mass, lapse, mass_rate, lapse_rate, mass_second=None, lapse_second=None):
    if not numerical.allclose(numerical.diff(basis.radii), basis.spacing, rtol=1e-12, atol=1e-14):
        raise ValueError('The theorem requires a uniform scalar grid.')
    knots = numerical.unique(numerical.concatenate([basis.radii, basis.faces]))
    face_map = linear_value_gradient(basis.faces, knots)[0]
    node_map = linear_value_gradient(basis.radii, knots)[0]
    mass_values, lapse_values = face_map @ mass, node_map @ lapse
    mass_rates, lapse_rates = face_map @ mass_rate, node_map @ lapse_rate
    denominator = knots - 2 * mass_values
    spatial_f = denominator / knots
    if knots[0] <= 0 or min(lapse_values) <= 0 or min(spatial_f) <= 0:
        raise ValueError('Positive-radius, positive-lapse, F>0 annulus required; no horizon extension.')
    radius_min, radius_max = float(knots[0]), float(knots[-1])
    lapse_min, lapse_max = float(min(lapse_values)), float(max(lapse_values))
    f_min, f_max = float(min(spatial_f)), float(max(spatial_f))
    cell_width = numerical.diff(knots)
    lapse_gradient = numerical.diff(lapse_values) / cell_width
    mass_gradient = numerical.diff(mass_values) / cell_width
    lapse_rate_gradient = numerical.diff(lapse_rates) / cell_width
    mass_rate_gradient = numerical.diff(mass_rates) / cell_width
    f_lipschitz = max(abs(2 * (mass_values[:-1] - mass_gradient * knots[:-1])) / knots[:-1]**2)
    lapse_lipschitz = max(abs(lapse_gradient))
    lapse_ratio = lapse_rates / lapse_values
    mass_ratio = mass_rates / denominator
    theta_lower = float(min(numerical.minimum(lapse_ratio[:-1], lapse_ratio[1:]) - numerical.maximum(mass_ratio[:-1], mass_ratio[1:])))
    theta_upper = float(max(numerical.maximum(lapse_ratio[:-1], lapse_ratio[1:]) - numerical.minimum(mass_ratio[:-1], mass_ratio[1:])))
    lapse_rate_numerator = lapse_rate_gradient * lapse_values[:-1] - lapse_rates[:-1] * lapse_gradient
    mass_rate_numerator = mass_rate_gradient * denominator[:-1] - mass_rates[:-1] * (1 - 2 * mass_gradient)
    theta_lipschitz = float(max(abs(lapse_rate_numerator) / numerical.minimum(lapse_values[:-1], lapse_values[1:])**2 + abs(mass_rate_numerator) / numerical.minimum(denominator[:-1], denominator[1:])**2))
    p_min = radius_min**2 * lapse_min * numerical.sqrt(f_min)
    p_max = radius_max**2 * lapse_max * numerical.sqrt(f_max)
    m_min = radius_min**2 / (lapse_max * numerical.sqrt(f_max))
    m_max = radius_max**2 / (lapse_min * numerical.sqrt(f_min))
    p_lipschitz = 2 * radius_max * lapse_max * numerical.sqrt(f_max) + radius_max**2 * lapse_lipschitz * numerical.sqrt(f_max) + radius_max**2 * lapse_max * f_lipschitz / (2 * numerical.sqrt(f_min))
    result = {'length': radius_max - radius_min, 'p_min': float(p_min), 'p_max': float(p_max), 'm_min': float(m_min), 'm_max': float(m_max), 'p_lipschitz': float(p_lipschitz), 'theta_min': theta_lower, 'theta_max': theta_upper, 'theta_lipschitz': theta_lipschitz, 'F_min': f_min, 'F_max': f_max, 'N_min': lapse_min, 'N_max': lapse_max, 'mass_rate_max': float(max(abs(mass_rates))), 'lapse_rate_max': float(max(abs(lapse_rates))), 'mass_rate_lipschitz': float(max(abs(mass_rate_gradient))), 'lapse_rate_lipschitz': float(max(abs(lapse_rate_gradient)))}
    if mass_second is not None and lapse_second is not None:
        mass_acceleration = float(max(abs(face_map @ mass_second)))
        lapse_acceleration = float(max(abs(node_map @ lapse_second)))
        theta_second_bound = lapse_acceleration / lapse_min + (result['lapse_rate_max'] / lapse_min)**2 + mass_acceleration / (radius_min * f_min) + 2 * (result['mass_rate_max'] / (radius_min * f_min))**2
        result.update(theta_time_max=theta_second_bound, mass_second_max=mass_acceleration, lapse_second_max=lapse_acceleration)
    return result


def coefficient_bounds(envelope, include_gram):
    length, p_min, p_max = [envelope[name] for name in ['length', 'p_min', 'p_max']]
    m_min, m_max, p_lipschitz = [envelope[name] for name in ['m_min', 'm_max', 'p_lipschitz']]
    theta_center = (envelope['theta_max'] + envelope['theta_min']) / 2
    theta_radius = (envelope['theta_max'] - envelope['theta_min']) / 2
    theta_max = max(abs(envelope['theta_min']), abs(envelope['theta_max']))
    theta_lipschitz = envelope['theta_lipschitz']
    gram_bound = 16 * GRAM_ROW_BOUND * p_max if include_gram else 0.0
    projection_constant = RIGHT_GRADIENT_CONSTANT + INVERSE_CONSTANT * numerical.sqrt(m_max / m_min) * (1 + RIGHT_VALUE_CONSTANT)
    alpha_a = abs(theta_center) + numerical.sqrt((p_max + gram_bound) / p_min) * (theta_radius + projection_constant * length * theta_lipschitz)
    elliptic_first = length / p_min
    elliptic_second = (1 + p_lipschitz * elliptic_first) / p_min
    interpolant_first = elliptic_first + HERMITE_ERROR_CONSTANT * length * elliptic_second
    consistency = HERMITE_ERROR_CONSTANT * p_max * elliptic_second + 2 * p_lipschitz * interpolant_first + gram_bound / numerical.sqrt(3) * elliptic_second
    elliptic_error = consistency / p_min
    residual_p_lipschitz = p_lipschitz * theta_radius + p_max * theta_lipschitz
    residual_consistency = HERMITE_ERROR_CONSTANT * p_max * theta_radius * elliptic_second + 2 * residual_p_lipschitz * interpolant_first + theta_radius * gram_bound / numerical.sqrt(3) * elliptic_second
    elliptic_transport = theta_radius + p_max * theta_lipschitz * elliptic_first + INVERSE_CONSTANT * (theta_radius * (p_max + gram_bound) * elliptic_error + residual_consistency)
    alpha_l = abs(theta_center) + m_max / m_min * elliptic_transport
    return {'alpha_M_bound': theta_max, 'alpha_K_bound': theta_max, 'alpha_A_bound': float(alpha_a), 'alpha_L_bound': float(alpha_l), 'beta_L_operator_bound': float(alpha_l), 'growth_bound': float(max(2 * alpha_a + theta_max, 2 * alpha_l + theta_max)), 'theta_center': theta_center, 'theta_radius': theta_radius, 'projection_constant': float(projection_constant), 'Gram_gradient_bound': float(gram_bound), 'elliptic_first': elliptic_first, 'elliptic_second': elliptic_second, 'interpolant_first': interpolant_first, 'elliptic_consistency': float(consistency), 'elliptic_error_constant': float(elliptic_error), 'elliptic_transport_L2_bound': float(elliptic_transport)}


def affine_norms(endpoint_values, length):
    first, second = map(float, endpoint_values)
    return numerical.sqrt(max(length * (first**2 + first * second + second**2) / 3, 0.0)), abs(second - first) / numerical.sqrt(length)


def boundary_bounds(envelope, bounds, endpoint_values, endpoint_rates, endpoint_accelerations):
    unused_lift_norm, lift_gradient = affine_norms(endpoint_values, envelope['length'])
    rate_norm, rate_gradient = affine_norms(endpoint_rates, envelope['length'])
    acceleration_norm, unused_acceleration_gradient = affine_norms(endpoint_accelerations, envelope['length'])
    m_max, m_min, p_max, p_lipschitz = [envelope[name] for name in ['m_max', 'm_min', 'p_max', 'p_lipschitz']]
    theta_max = bounds['alpha_M_bound']
    theta_lipschitz = envelope['theta_lipschitz']
    derivative_factor = 1 + 2 * INVERSE_CONSTANT
    force = (m_max * (acceleration_norm + theta_max * rate_norm) + derivative_factor * p_lipschitz * lift_gradient) / numerical.sqrt(m_min)
    force_time = (2 * m_max * theta_max * acceleration_norm + m_max * (theta_max**2 + envelope['theta_time_max']) * rate_norm + derivative_factor * ((p_lipschitz * theta_max + p_max * theta_lipschitz) * lift_gradient + p_lipschitz * rate_gradient)) / numerical.sqrt(m_min)
    return {'boundary_force_bound': float(force), 'boundary_force_time_bound': float(force_time), 'boundary_source_bound': float(bounds['beta_L_operator_bound'] * force + force_time), 'scope': 'same affine scalar-value lift; quadratic endpoint histories; every slope remains free; no Gram lift term because third differences of affine values vanish'}


def full_operator_norm(operator, metric):
    cholesky = numerical.linalg.cholesky(metric)
    whitened = numerical.linalg.solve(cholesky, (cholesky.T @ operator).T).T
    return float(numerical.linalg.svd(whitened, compute_uv=False)[0])


def projection_map(basis, theta_nodes):
    count = basis.radii.size
    diagonal = numerical.diag(theta_nodes)
    mapping = numerical.zeros((2 * count, 2 * count))
    mapping[:count, :count] = diagonal
    mapping[count:, :count] = basis.spacing * (diagonal @ basis.derivative - basis.derivative @ diagonal)
    mapping[count:, count:] = diagonal
    return mapping
