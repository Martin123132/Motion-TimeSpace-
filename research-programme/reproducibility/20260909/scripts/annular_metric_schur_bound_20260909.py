import numpy as numerical
import sympy as symbolic
from scipy.linalg import block_diag, eigvalsh, solve_triangular

from annular_uniform_energy_bounds_20260909 import metric_envelope
from sbp4_compatible_second_operator_20260909 import DATA


def exact_overlap_geometry():
    rational = symbolic.Rational
    count = 17
    edge = list(map(rational, DATA['norm_weights']))
    if edge != [rational(17, 48), rational(59, 48), rational(43, 48), rational(49, 48)]:
        raise ValueError('The derived face template changed; rederive the overlap constants.')
    widths = edge + [rational(1)] * (count - 8) + edge[::-1]
    faces = [rational(0)]
    for width in widths:
        faces.append(faces[-1] + width)
    overlap = symbolic.zeros(count)
    for cell in range(count):
        lower, upper = faces[cell:cell + 2]
        for node in range(count):
            for start, stop, slope, intercept in [(node - 1, node, 1, 1 - node), (node, node + 1, -1, node + 1)]:
                left = max(lower, rational(start), rational(0))
                right = min(upper, rational(stop), rational(count - 1))
                if right > left:
                    overlap[cell, node] += slope * (right**2 - left**2) / 2 + intercept * (right - left)
    row_sums = [sum(overlap[cell, node] for node in range(count)) for cell in range(count)]
    column_sums = [sum(overlap[cell, node] for cell in range(count)) for node in range(count)]
    row_gaps = [2 * overlap[index, index] - row_sums[index] for index in range(count)]
    column_gaps = [2 * overlap[index, index] - column_sums[index] for index in range(count)]
    interior = all(overlap[index, index - 1] == rational(1, 8) and overlap[index, index] == rational(3, 4) and overlap[index, index + 1] == rational(1, 8) for index in range(4, count - 4))
    reflected = all(overlap[first, second] == overlap[count - 1 - first, count - 1 - second] for first in range(count) for second in range(count))
    banded = all(overlap[first, second] == 0 for first in range(count) for second in range(count) if abs(first - second) > 1)
    positive = min(row_gaps) > 0 and min(column_gaps) > 0
    beta_squared = min(row_gaps) * min(column_gaps) / max(widths)
    return {'overlap': overlap, 'row_gap': min(row_gaps), 'column_gap': min(column_gaps), 'width_max': max(widths), 'beta_squared': beta_squared, 'beta': float(symbolic.sqrt(beta_squared)), 'template_proved': bool(interior and reflected and banded and positive and row_sums == widths and column_sums == [rational(1, 2)] + [rational(1)] * (count - 2) + [rational(1, 2)]), 'left_rows': [[str(overlap[row, column]) for column in range(5)] for row in range(4)], 'row_gaps_left': list(map(str, row_gaps[:5])), 'column_gaps_left': list(map(str, column_gaps[:5]))}


def whitened_form(matrix, row_metric, column_metric=None):
    if column_metric is None:
        column_metric = row_metric
    row_root = numerical.linalg.cholesky(row_metric)
    column_root = numerical.linalg.cholesky(column_metric)
    return solve_triangular(column_root, solve_triangular(row_root, matrix, lower=True).T, lower=True).T


def schur_blocks(system, packed, include_gram):
    jacobian = system.evaluate(packed, include_gram)[2]
    mass_indices = numerical.arange(1, system.face_count)
    lapse_indices = numerical.arange(system.slices[1].start, system.slices[1].stop)
    metric_indices = numerical.concatenate([mass_indices, lapse_indices])
    velocity_indices = system.free_velocity_indices
    raw_metric = jacobian[numerical.ix_(metric_indices, metric_indices)]
    coupling = jacobian[numerical.ix_(metric_indices, velocity_indices)]
    scalar_mass = jacobian[numerical.ix_(velocity_indices, velocity_indices)]
    schur = raw_metric - coupling @ numerical.linalg.solve(scalar_mass, coupling.T)
    count = mass_indices.size
    basis = system.basis
    mass_norm = basis.face_gradient[:, 1:].T @ (basis.quadrature_weights[:, None] * basis.face_gradient[:, 1:])
    lapse_norm = basis.spacing * numerical.eye(system.node_count)
    metric_norm = block_diag(mass_norm, lapse_norm)
    return {'jacobian': jacobian, 'metric_indices': metric_indices, 'velocity_indices': velocity_indices, 'scalar_mass': scalar_mass, 'coupling': coupling, 'raw_metric': raw_metric, 'schur': schur, 'A': schur[:count, :count], 'B': schur[:count, count:], 'D': schur[count:, count:], 'mass_norm': mass_norm, 'lapse_norm': lapse_norm, 'metric_norm': metric_norm}


def field_envelopes(system, packed):
    basis = system.basis
    q_values = packed[system.slices[2]]
    q_derivative = basis.derivative @ q_values + packed[system.slope_slice] / basis.spacing
    scalar_derivative = basis.derivative @ system.scalar + system.slope / basis.spacing
    q_controls = numerical.stack([q_values[:-1], q_values[:-1] + basis.spacing * q_derivative[:-1] / 3, q_values[1:] - basis.spacing * q_derivative[1:] / 3, q_values[1:]])
    w_controls = numerical.stack([scalar_derivative[:-1], 3 * numerical.diff(system.scalar) / basis.spacing - scalar_derivative[:-1] - scalar_derivative[1:], scalar_derivative[1:]])
    return {'q_max': float(numerical.max(abs(q_controls))), 'w_max': float(numerical.max(abs(w_controls))), 'q_Bernstein_controls': q_controls, 'w_Bernstein_controls': w_controls}


def analytic_schur_bound(system, packed, include_gram, geometry):
    if any(system.constants[name] != 0 for name in ['b2', 'b3', 'm_chi', 'Lambda']):
        raise ValueError('Canonical zero-mass/Lambda branch only.')
    basis = system.basis
    mass, lapse = packed[system.slices[0]], packed[system.slices[1]]
    envelope = metric_envelope(basis, mass, lapse, numerical.zeros_like(mass), numerical.zeros_like(lapse))
    fields = field_envelopes(system, packed)
    inner, length, kappa = basis.radii[0], envelope['length'], system.kappa
    f_min, f_max, n_min, n_max = [envelope[name] for name in ['F_min', 'F_max', 'N_min', 'N_max']]
    m_max, p_max = envelope['m_max'], envelope['p_max']
    q_max, w_max = fields['q_max'], fields['w_max']
    mass_gradient = float(numerical.max(abs(numerical.diff(mass) / numerical.diff(basis.faces))))
    denominator = inner * f_min
    nodal_poincare = numerical.sqrt(17 / 16) * length
    sigma_min, sigma_max = 1 / numerical.sqrt(f_max), 1 / numerical.sqrt(f_min)
    sigma_center, sigma_radius = (sigma_min + sigma_max) / 2, (sigma_max - sigma_min) / 2
    beta_reference = sigma_center / kappa * geometry['beta']
    perturbations = {'principal_variation': sigma_radius / kappa, 'gravity_lower_order': length * mass_gradient / (kappa * inner * f_min**1.5), 'kinetic': .5 * length * m_max * q_max**2 / (denominator * n_min), 'gradient': .5 * length * p_max * w_max**2 / (denominator * n_min), 'Gram': 2 * nodal_poincare * p_max * w_max**2 / (denominator * n_min) if include_gram else 0.0}
    beta_bound = beta_reference - sum(perturbations.values())
    a_terms = {'gravity_diagonal': 3 * n_max * mass_gradient * length**2 / (kappa * inner**2 * f_min**2.5), 'gravity_cross': 2 * n_max * length / (kappa * inner * f_min**1.5), 'kinetic': 1.5 * m_max * q_max**2 * length**2 / denominator**2, 'gradient': .5 * p_max * w_max**2 * length**2 / denominator**2, 'Gram': 2 * p_max * w_max**2 * nodal_poincare**2 / denominator**2 if include_gram else 0.0}
    a_bound = sum(a_terms.values())
    d_bound = m_max * q_max**2 / n_min**2
    valid = beta_bound > 0
    base_inverse = .5 * (a_bound / beta_bound**2 + numerical.sqrt((a_bound / beta_bound**2)**2 + 4 / beta_bound**2)) if valid else None
    feedback = base_inverse * d_bound if valid else None
    valid = bool(valid and feedback < 1)
    inverse = base_inverse / (1 - feedback) if valid else None
    return {'envelope': envelope, 'q_max': q_max, 'w_max': w_max, 'mass_R_max': mass_gradient, 'sigma_center': float(sigma_center), 'beta_reference_bound': float(beta_reference), 'B_perturbation_terms': {name: float(value) for name, value in perturbations.items()}, 'B_perturbation_bound': float(sum(perturbations.values())), 'beta_B_bound': float(beta_bound), 'A_terms': {name: float(value) for name, value in a_terms.items()}, 'A_bound': float(a_bound), 'D_bound': float(d_bound), 'reference_inverse_bound': None if base_inverse is None else float(base_inverse), 'Neumann_feedback': None if feedback is None else float(feedback), 'inverse_bound': None if inverse is None else float(inverse), 'sufficient_uniform_inverse_gate': valid, 'Gram_density_bound': float(2 * basis.spacing * w_max**2), 'q_Bernstein_controls': fields['q_Bernstein_controls'], 'w_Bernstein_controls': fields['w_Bernstein_controls']}


def measured_schur_norms(blocks, reference):
    singular = numerical.linalg.svd(whitened_form(blocks['B'], blocks['mass_norm'], blocks['lapse_norm']), compute_uv=False)
    perturbation = numerical.linalg.svd(whitened_form(blocks['B'] - reference, blocks['mass_norm'], blocks['lapse_norm']), compute_uv=False)[0]
    spectrum = eigvalsh(blocks['schur'], blocks['metric_norm'])
    d_spectrum = eigvalsh(blocks['D'], blocks['lapse_norm'])
    return {'beta_B': float(singular[-1]), 'B_perturbation_norm': float(perturbation), 'A_norm': float(max(abs(eigvalsh(blocks['A'], blocks['mass_norm'])))), 'D_norm': float(max(abs(d_spectrum))), 'D_minimum': float(d_spectrum[0]), 'inverse_norm': float(1 / min(abs(spectrum))), 'inertia_positive': int(numerical.sum(spectrum > 0)), 'inertia_negative': int(numerical.sum(spectrum < 0))}


def lapse_projection_residual(system, packed, blocks):
    basis = system.basis
    velocity = basis.scalar_value @ packed[system.slices[2]] + basis.lift_value @ packed[system.slope_slice] / basis.spacing
    lapse = basis.node_value @ packed[system.slices[1]]
    mass = basis.face_value @ packed[system.slices[0]]
    spatial_f = 1 - 2 * mass / basis.quadrature
    weighted_mass = basis.quadrature_weights * basis.quadrature**2 / (lapse * numerical.sqrt(spatial_f))
    fields = velocity[:, None] / lapse[:, None] * basis.node_value
    full_values = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)
    scalar_free = blocks['velocity_indices'] - system.slices[2].start
    free_values = full_values[:, scalar_free]
    projected = free_values @ numerical.linalg.solve(blocks['scalar_mass'], free_values.T @ (weighted_mass[:, None] * fields))
    residual = fields - projected
    return residual.T @ (weighted_mass[:, None] * residual)


def independent_schur_components(system, packed, blocks, include_gram):
    basis, radius, kappa = system.basis, system.basis.quadrature, system.kappa
    mass_value, mass_radial = basis.face_value[:, 1:], basis.face_gradient[:, 1:]
    lapse_value = basis.node_value
    mass = basis.face_value @ packed[system.slices[0]]
    mass_r = basis.face_gradient @ packed[system.slices[0]]
    lapse = lapse_value @ packed[system.slices[1]]
    value = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)
    radial = numerical.concatenate([basis.scalar_gradient, basis.lift_gradient / basis.spacing], axis=1)
    q_values = value @ numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice]])
    w_values = radial @ numerical.concatenate([system.scalar, system.slope])
    spatial_f = 1 - 2 * mass / radius
    denominator = radius * spatial_f
    mass_density = radius**2 / (lapse * numerical.sqrt(spatial_f))
    stiffness_density = radius**2 * lapse * numerical.sqrt(spatial_f)
    weights = basis.quadrature_weights
    free_value = value[:, blocks['velocity_indices'] - system.slices[2].start]
    e_mass = q_values[:, None] / denominator[:, None] * mass_value
    e_lapse = q_values[:, None] / lapse[:, None] * lapse_value

    def pair(first, density, second):
        return first.T @ ((weights * density)[:, None] * second)

    projected_mass = free_value @ numerical.linalg.solve(blocks['scalar_mass'], pair(free_value, mass_density, e_mass))
    projected_lapse = free_value @ numerical.linalg.solve(blocks['scalar_mass'], pair(free_value, mass_density, e_lapse))
    a_kinetic = .5 * pair(e_mass, mass_density, e_mass) + pair(e_mass - projected_mass, mass_density, e_mass - projected_mass)
    b_kinetic = -.5 * pair(e_mass, mass_density, e_lapse) + pair(projected_mass, mass_density, projected_lapse)
    a_gravity = pair(mass_value, 3 * lapse * mass_r / (kappa * radius**2 * spatial_f**2.5), mass_value)
    cross = pair(mass_value, lapse / (kappa * radius * spatial_f**1.5), mass_radial)
    a_gravity += cross + cross.T
    b_gravity = pair(mass_radial, 1 / (kappa * numerical.sqrt(spatial_f)), lapse_value) + pair(mass_value, mass_r / (kappa * radius * spatial_f**1.5), lapse_value)
    a_gradient = .5 * pair(mass_value, stiffness_density * w_values**2 / denominator**2, mass_value)
    b_gradient = .5 * pair(mass_value, stiffness_density * w_values**2 / (denominator * lapse), lapse_value)
    a_gram, b_gram = numerical.zeros_like(a_gravity), numerical.zeros_like(b_gravity)
    if include_gram:
        node_map = basis.face_to_node[:, 1:]
        node_lapse = packed[system.slices[1]]
        node_f = 1 - 2 * basis.face_to_node @ packed[system.slices[0]] / basis.radii
        node_p = basis.radii**2 * node_lapse * numerical.sqrt(node_f)
        a_gram = node_map.T @ ((system.density * node_p / (basis.radii * node_f)**2)[:, None] * node_map)
        b_gram = node_map.T * (system.density * node_p / (basis.radii * node_f * node_lapse))[None, :]
    return {'A_gravity': a_gravity, 'A_kinetic': a_kinetic, 'A_gradient': a_gradient, 'A_Gram': a_gram, 'B_gravity': b_gravity, 'B_kinetic': b_kinetic, 'B_gradient': b_gradient, 'B_Gram': b_gram, 'A_reconstructed': a_gravity + a_kinetic + a_gradient + a_gram, 'B_reconstructed': b_gravity + b_kinetic + b_gradient + b_gram, 'D_reconstructed': pair(e_lapse - projected_lapse, mass_density, e_lapse - projected_lapse)}
