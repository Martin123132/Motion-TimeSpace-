import numpy as numerical
import sympy as symbolic

from annular_metric_schur_bound_20260909 import exact_overlap_geometry
from annular_uniform_energy_bounds_20260909 import affine_norms


def exact_gradient_geometry():
    overlap = exact_overlap_geometry()['overlap']
    count = overlap.rows
    widths = [sum(overlap[row, column] for column in range(count)) for row in range(count)]
    average = symbolic.diag(*[1 / width for width in widths]) * overlap
    gradient = symbolic.Matrix(count - 1, count - 1, lambda row, column: sum(average[row + 1, other] - average[row, other] for other in range(column + 1, count)))
    row_gap = min(2 * gradient[row, row] - sum(abs(gradient[row, column]) for column in range(count - 1)) for row in range(count - 1))
    column_gap = min(2 * gradient[column, column] - sum(abs(gradient[row, column]) for row in range(count - 1)) for column in range(count - 1))
    rational = symbolic.Rational
    reflected = all(gradient[row, column] == gradient[count - 2 - row, count - 2 - column] for row in range(count - 1) for column in range(count - 1))
    interior = all(gradient[row, row - 1] == rational(1, 8) and gradient[row, row] == rational(3, 4) and gradient[row, row + 1] == rational(1, 8) for row in range(4, count - 5))
    banded = all(gradient[row, column] == 0 for row in range(count - 1) for column in range(count - 1) if abs(row - column) > 1)
    infinity_margin = rational(123, 100) * row_gap - rational(1, 50) * rational(59, 48)
    l2_margin_lower = rational(123, 100) * rational(47, 100) - rational(1, 50) * rational(9, 8)
    proved = row_gap > 0 and column_gap > 0 and row_gap * column_gap >= rational(47, 100)**2 and rational(9, 8)**2 >= rational(59, 48)
    proved = proved and infinity_margin > rational(1, 2) and l2_margin_lower > rational(1, 2) and reflected and interior and banded
    return {'proved': bool(proved), 'row_gap': str(row_gap), 'column_gap': str(column_gap), 'infinity_margin': str(infinity_margin), 'l2_margin_lower': str(l2_margin_lower), 'left_rows': [[str(gradient[row, column]) for column in range(6)] for row in range(5)], 'inverse_gradient_majorant': 2.0, 'scope': 'four left gradient-row templates, repeated interior, reflected right; disjoint for n>=17'}


def row_data(system, packed, speed, include_gram, rho_time):
    basis = system.basis
    radius, weights = basis.quadrature, basis.quadrature_weights
    mass, mass_r = basis.face_value @ packed[system.slices[0]], basis.face_gradient @ packed[system.slices[0]]
    mass_t, mass_tr = basis.face_value @ speed[system.slices[0]], basis.face_gradient @ speed[system.slices[0]]
    lapse, lapse_t = basis.node_value @ packed[system.slices[1]], basis.node_value @ speed[system.slices[1]]
    reconstruction = numerical.concatenate([basis.scalar_value, basis.lift_value / basis.spacing], axis=1)
    radial = numerical.concatenate([basis.scalar_gradient, basis.lift_gradient / basis.spacing], axis=1)
    velocity = numerical.concatenate([packed[system.slices[2]], packed[system.slope_slice]])
    q_value, q_radial = reconstruction @ velocity, radial @ velocity
    acceleration = reconstruction @ numerical.concatenate([speed[system.slices[2]], speed[system.slope_slice]])
    scalar_gradient = radial @ numerical.concatenate([system.scalar, system.slope])
    spatial_f = 1 - 2 * mass / radius
    sigma = spatial_f**-.5
    sigma_time = mass_t / (radius * spatial_f**1.5)
    density = lapse * mass_r / (system.kappa * radius * spatial_f**1.5) + radius * q_value**2 / (2 * lapse * spatial_f**1.5) + radius * lapse * scalar_gradient**2 / (2 * numerical.sqrt(spatial_f))
    density_time = (lapse_t * mass_r + lapse * mass_tr) / (system.kappa * radius * spatial_f**1.5) + 3 * lapse * mass_r * mass_t / (system.kappa * radius**2 * spatial_f**2.5)
    density_time += radius * q_value * acceleration / (lapse * spatial_f**1.5) - radius * q_value**2 * lapse_t / (2 * lapse**2 * spatial_f**1.5) + 3 * q_value**2 * mass_t / (2 * lapse * spatial_f**2.5)
    density_time += radius * lapse_t * scalar_gradient**2 / (2 * numerical.sqrt(spatial_f)) + radius * lapse * scalar_gradient * q_radial / numerical.sqrt(spatial_f) + lapse * scalar_gradient**2 * mass_t / (2 * spatial_f**1.5)
    node_f = 1 - 2 * basis.face_to_node @ packed[system.slices[0]] / basis.radii
    node_lapse = packed[system.slices[1]]
    atoms = numerical.zeros(system.node_count)
    atoms_time = numerical.zeros_like(atoms)
    if include_gram:
        atoms = system.density * basis.radii * node_lapse / numerical.sqrt(node_f)
        atoms_time = rho_time * basis.radii * node_lapse / numerical.sqrt(node_f)
        atoms_time += system.density * (basis.radii * speed[system.slices[1]] / numerical.sqrt(node_f) + node_lapse * (basis.face_to_node @ speed[system.slices[0]]) / node_f**1.5)
    widths = numerical.diff(basis.faces)
    cells = numerical.clip(numerical.searchsorted(basis.faces, radius, side='right') - 1, 0, system.node_count - 1)
    averages = numerical.zeros((system.node_count, radius.size))
    averages[cells, numerical.arange(radius.size)] = weights / widths[cells]
    ramp = numerical.clip((radius[None, :] - basis.faces[:-1, None]) / widths[:, None], 0, 1)
    nodal_ramp = numerical.clip((basis.radii[None, :] - basis.faces[:-1, None]) / widths[:, None], 0, 1)
    hat = -numerical.diff(ramp, axis=0) / basis.spacing
    node_hat = -numerical.diff(nodal_ramp, axis=0) / basis.spacing
    average_nodes = averages @ basis.node_value
    gradient = numerical.cumsum(numerical.diff(average_nodes, axis=0)[:, ::-1], axis=1)[:, ::-1][:, 1:]
    return {'sigma': sigma, 'sigma_time': sigma_time, 'lapse': lapse, 'lapse_time': lapse_t, 'density': density, 'density_time': density_time, 'atoms': atoms, 'atoms_time': atoms_time, 'averages': averages, 'ramp': ramp, 'nodal_ramp': nodal_ramp, 'hat': hat, 'node_hat': node_hat, 'gradient_matrix': gradient, 'acceleration': acceleration, 'scalar_gradient': scalar_gradient, 'q_value': q_value}


def spatial_bounds(system, scalar, static_residual, time_residual, inner_rate, clock_rate, endpoint_acceleration, include_gram, response_residual_dual=0.0, scalar_equation_residual_m=0.0):
    basis = system.basis
    inner, outer, length = 47 / 8, 49 / 8, 1 / 4
    f_min, f_max, n_min, n_max, q_max, w_max, mass_r = .65, .68, .8, .84, .02, .03, .002
    kappa, width_max, gram = .1, 59 / 48, float(include_gram)
    denominator = inner * f_min
    root_length = numerical.sqrt(length)
    node_length = 17 * length / 16
    node_root = numerical.sqrt(node_length)
    m_max, p_max = 60025 / 1024, 16807 / 640
    m_min, p_min = inner**2 / (n_max * numerical.sqrt(f_max)), inner**2 * n_min * numerical.sqrt(f_min)
    f_radial = (1 - f_min + 2 * mass_r) / inner
    sigma_radial = f_radial / (2 * f_min**1.5)
    static_defect = float(numerical.max(abs(static_residual[1:-1])) / basis.spacing)
    time_defect = float(numerical.linalg.norm(time_residual[1:-1]) / numerical.sqrt(basis.spacing))
    density_sup = n_max * mass_r / (kappa * inner * f_min**1.5) + outer * q_max**2 / (2 * n_min * f_min**1.5) + outer * n_max * w_max**2 / (2 * numerical.sqrt(f_min))
    atom_sup = gram * 2 * w_max**2 * p_max / denominator
    lapse_radial = 2 * (kappa * (width_max * density_sup + 3 * atom_sup + static_defect) + width_max * sigma_radial * n_max)
    p_radial = 2 * outer * n_max * numerical.sqrt(f_max) + outer**2 * lapse_radial * numerical.sqrt(f_max) + outer**2 * n_max * f_radial / (2 * numerical.sqrt(f_min))
    energy_root = numerical.sqrt(max(0.0, 2 * scalar['energy']))
    unused_norm, q_lift_radial = affine_norms(scalar['velocity'][:system.node_count][[0, -1]], length)
    unused_norm, chi_lift_radial = affine_norms(system.scalar[[0, -1]], length)
    eta_norm, unused_radial = affine_norms(endpoint_acceleration, length)
    q_radial = energy_root / numerical.sqrt(p_min) + q_lift_radial
    graph = energy_root + 33 * p_radial * chi_lift_radial / numerical.sqrt(m_min)
    drive = graph + numerical.sqrt(m_max) * eta_norm
    gravity_cross = n_max / (kappa * inner * f_min**1.5)
    a_density = 3 * n_max * mass_r / (kappa * inner**2 * f_min**2.5) + (3 * m_max * q_max**2 + p_max * w_max**2) / (2 * denominator**2)
    a_gram = gram * 2 * p_max * w_max**2 / denominator**2
    b_density = mass_r / (kappa * inner * f_min**1.5) + (m_max * q_max**2 + p_max * w_max**2) / (2 * denominator * n_min)
    b_gram = gram * 2 * p_max * w_max**2 / (denominator * n_min)
    poincare = numerical.sqrt(17 / 16) * length
    lift_mass = a_density * length * root_length + gravity_cross * root_length + a_gram * poincare * node_root
    lift_lapse = b_density * root_length + b_gram * node_root
    source_mass = p_max * w_max / denominator * (length + gram * numerical.sqrt(8) * poincare) * q_radial + root_length * abs(clock_rate) / kappa + numerical.sqrt(m_max) * q_max * length / denominator * drive + lift_mass * abs(inner_rate)
    source_lapse = p_max * w_max / n_min * (1 + gram * numerical.sqrt(8)) * q_radial + numerical.sqrt(m_max) * q_max / n_min * drive + lift_lapse * abs(inner_rate)
    response = 175 / 118 * (numerical.hypot(source_mass, source_lapse) + response_residual_dual)
    mass_sup = abs(inner_rate) + root_length * response
    direct_rows = width_max * (p_max * w_max / denominator * (root_length + gram * numerical.sqrt(8) * node_root) * q_radial + abs(clock_rate) / kappa + numerical.sqrt(m_max) * q_max * root_length / denominator * drive)
    mass_rows = width_max * (a_density * length * mass_sup + gravity_cross * (mass_sup + root_length * response) + a_gram * node_length * mass_sup)
    lapse_rows = width_max * (b_density * root_length + b_gram * node_root) * response
    lapse_sup = (direct_rows + mass_rows + lapse_rows) / ((1.23 * 527 / 2304 - .02 * width_max) / kappa)
    theta_sup = lapse_sup / n_min + mass_sup / denominator
    acceleration = (drive + numerical.sqrt(m_max) * q_max * root_length * theta_sup + scalar_equation_residual_m) / numerical.sqrt(m_min)
    density_rate_lapse = mass_r / (kappa * inner * f_min**1.5) + outer * q_max**2 / (2 * n_min**2 * f_min**1.5) + outer * w_max**2 / (2 * numerical.sqrt(f_min))
    density_rate_mass = 3 * n_max * mass_r / (kappa * inner**2 * f_min**2.5) + 3 * q_max**2 / (2 * n_min * f_min**2.5) + n_max * w_max**2 / (2 * f_min**1.5)
    density_time = (density_rate_lapse + n_max / (kappa * inner * f_min**1.5)) * response + density_rate_mass * root_length * mass_sup
    density_time += outer * q_max / (n_min * f_min**1.5) * acceleration + outer * n_max * w_max / numerical.sqrt(f_min) * q_radial
    rho_time = numerical.sqrt(8) * w_max * q_radial
    atom_time = gram * (p_max / denominator * rho_time + 2 * w_max**2 * (outer / numerical.sqrt(f_min) * response + n_max / f_min**1.5 * node_root * mass_sup))
    lambda_coefficient = n_max / (inner * f_min**1.5)
    lambda_radial_coefficient = lapse_radial / (inner * f_min**1.5) + n_max / (inner**2 * f_min**1.5) + 1.5 * n_max * f_radial / (inner * f_min**2.5)
    lambda_radial = lambda_coefficient * response + lambda_radial_coefficient * root_length * mass_sup
    lapse_time_radial = 2 * (kappa * (numerical.sqrt(width_max) * density_time + numerical.sqrt(3) * atom_time + time_defect) + numerical.sqrt(width_max) * (lambda_radial + sigma_radial * response))
    theta_radial = lapse_time_radial / n_min + lapse_sup * root_length * lapse_radial / n_min**2 + response / denominator + mass_sup * root_length * (1 + 2 * mass_r) / denominator**2
    paired = theta_radial + 2 * kappa * q_max * w_max * root_length / f_min
    return {name: float(value) for name, value in {'F_radial_sup_bound': f_radial, 'sigma_radial_sup_bound': sigma_radial, 'static_residual_density_sup': static_defect, 'time_residual_density_L2': time_defect, 'static_mass_density_sup_bound': density_sup, 'static_atom_density_sup_bound': atom_sup, 'lapse_radial_sup_bound': lapse_radial, 'p_radial_sup_bound': p_radial, 'energy': scalar['energy'], 'q_radial_L2_bound': q_radial, 'scalar_graph_force_bound': graph, 'metric_response_bound': response, 'mass_rate_sup_bound': mass_sup, 'lapse_rate_sup_bound': lapse_sup, 'theta_sup_bound': theta_sup, 'scalar_acceleration_L2_bound': acceleration, 'mass_density_time_L2_bound': density_time, 'atom_time_dual_L2_bound': atom_time, 'sigma_time_N_radial_L2_bound': lambda_radial, 'lapse_time_radial_L2_bound': lapse_time_radial, 'theta_radial_L2_bound': theta_radial, 'paired_flux_remainder_L2_bound': paired, 'inner_shift_trace_input': inner_rate}.items()}
