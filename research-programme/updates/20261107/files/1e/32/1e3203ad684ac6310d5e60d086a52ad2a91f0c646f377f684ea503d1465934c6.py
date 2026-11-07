from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import load_owned
from derive_annular_native_shape_stress_20260928 import physical_data, pinned_tests, nodal_transport
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import ProbeMetricRate, MetricResponse
from annular_joint_flow_derivative_20260922 import JointMetricTangent
from annular_moving_Legendre_current_20260921 import samples
from annular_physical_native_kernel_20260928 import decimals
from types import SimpleNamespace
from decimal import Decimal
import numpy as np
import sympy as sp


CHANNELS = ['wave_field', 'wave_mesh', 'wave_direct', 'wave_label_defect',
    'wave_spatial_defect', 'wave_faces', 'wave_identity', 'gram_field',
    'gram_mesh', 'gram_coefficient', 'gram_total', 'coupled_direct',
    'coupled_identity', 'solved_field_work', 'mesh_equation', 'kinetic_defect',
    'kinetic_label_defect', 'kinetic_spatial_defect', 'kinetic_cross',
    'wave_without_acceleration', 'wave_acceleration', 'label_profile_max_error']


def symbolic_checks(evidence):
    alpha, beta, alpha_r, beta_r, temporal, gradient, gradient_r, rate_r = sp.symbols('alpha beta alpha_R beta_R T g g_R qdot_R')
    speed, speed_r, eta, eta_r, field, field_r, momentum_rate = sp.symbols('W W_R eta eta_R z z_R A_dot')
    gradient_rate = rate_r - speed_r * gradient
    temporal_r = gradient_rate - speed * gradient_r
    density = (alpha * temporal**2 - beta * gradient**2) / 2
    density_r = (alpha_r * temporal**2 - beta_r * gradient**2) / 2 + alpha * temporal * temporal_r - beta * gradient * gradient_r
    flux = alpha * speed * temporal + beta * gradient
    direct = momentum_rate * (field - gradient * eta) + flux * field_r - alpha * temporal * gradient_rate * eta
    direct -= (alpha_r * temporal**2 - beta_r * gradient**2) * eta / 2
    direct -= (alpha * temporal**2 / 2 + beta * gradient**2 / 2 + alpha * speed * temporal * gradient) * eta_r
    defect = momentum_rate * (field - eta * gradient) + flux * (field_r - eta_r * gradient - eta * gradient_r)
    evidence.check('derived_wave_cell_boundary_identity', sp.expand(direct - defect + eta_r * density + eta * density_r) == 0)
    amount, width, width_r, q_s, qdot = sp.symbols('epsilon H eta_s q_s qdot', real=True)
    moved_width = width + amount * width_r
    moved_gradient = q_s / moved_width
    moved_alpha, moved_beta = alpha + amount * alpha_r * eta, beta + amount * beta_r * eta
    lagrangian = moved_width * (moved_alpha * (qdot - speed * moved_gradient)**2 - moved_beta * moved_gradient**2) / 2
    derivative = sp.diff(lagrangian, amount).subs(amount, 0).subs({q_s: width * gradient, qdot: temporal + speed * gradient, width_r: width * eta_r}) / width
    expected = (alpha_r * temporal**2 - beta_r * gradient**2) * eta / 2
    expected += (alpha * temporal**2 / 2 + beta * gradient**2 / 2 + alpha * speed * temporal * gradient) * eta_r
    evidence.check('finite_cell_position_action_derivative', sp.simplify(derivative - expected) == 0)


def restore_flow(evidence, digests, action, sources, level):
    read = lambda relative: load_owned(evidence, digests, evidence.root / relative)
    parent = read(sources['parent'])
    centre = next(row for row in parent['centres'] if row.get('route') == 'resampled') if level == 'fine' else parent['centres'][0]
    flow = read(centre['flow_path'])
    if level == 'fine':
        parent = read(str((evidence.output.parent / 'annular-matched-seed-flow-attempt01/status.json').relative_to(evidence.root)))
    probes = {}
    for index in range(3):
        for sign in [-1, 1]:
            suffix = '-inner' + str(index) + '-sign' + str(sign) + '.npz'
            archive = read(next(path for path in centre['probe_paths'] if path.endswith(suffix)))
            solver, solution = reconstructed_solver(archive)
            probes[index, sign] = SimpleNamespace(solver=solver, solution=solution)
    coordinate = ProbeMetricRate(probes, flow['inner_steps'])
    responses = []
    for estimate in range(2):
        final = max((row for row in parent['iterations'] if row['case'] == centre['case'] and row['estimate'] == estimate), key=lambda row: row['iteration'])
        saved = read(final['output'])
        evidence.check(centre['case'] + ':acceleration_replay:' + str(estimate), np.array_equal(saved['acceleration'], flow['accelerations'][estimate]))
        solution = {key: saved['metric_' + key] for key in ['state', 'rhs_coefficients', 'primitives', 'left']}
        responses.append(MetricResponse(action.solver, solution, saved['forcing'], final['radial_linear_residual'], []))
    tangent = JointMetricTangent(coordinate, responses)
    evidence.check(centre['case'] + ':metric_rate_replay', np.max(abs(tangent.values(flow['radius']) - flow['metric_rate'])) <= 2e-18)
    coordinate.cache.clear()
    return flow, tangent, centre


def trial_directions(engine, loads, action):
    labels = action.owner.layer_rule.points / 2
    edges, fields = [], []
    for label in labels:
        data = physical_data(engine, loads, action, label)
        edge = pinned_tests(data['edges'], data['source'])[1]
        edge[engine.anchor] = Decimal(0)
        atoms = engine.atoms(data['edges'], data['field'])
        field = nodal_transport(engine, dict(atoms=atoms), edge)
        edges.append(np.asarray(edge, float))
        fields.append(np.asarray(field, float))
    return np.array(edges), np.array(fields)


def interpolate_nodal(values, indices, local, widths):
    selected = indices >= 0
    nodes = values[np.maximum(indices, 0)] * selected
    left, middle, right = nodes.T
    value = left * (1 - local) * (1 - 2 * local) + middle * 4 * local * (1 - local) + right * local * (2 * local - 1)
    gradient = (left * (4 * local - 3) + middle * (4 - 8 * local) + right * (4 * local - 1)) / widths
    return value, gradient


def evaluate_wave(raw):
    measure, alpha, beta, alpha_r, beta_r, alpha_t, gradient, gradient_r, rate, rate_r, accel, speed, speed_r, speed_rate, eta, eta_r, field, field_r, star, star_r = [raw[key] for key in
        ['measure', 'alpha', 'beta', 'alpha_r', 'beta_r', 'alpha_t', 'gradient', 'gradient_r', 'rate', 'rate_r', 'acceleration', 'speed', 'speed_r', 'speed_rate', 'eta', 'eta_r', 'field', 'field_r', 'star', 'star_r']]
    temporal = rate - speed * gradient
    gradient_rate = rate_r - speed_r * gradient
    temporal_rate = accel - speed_rate * gradient - speed * gradient_rate
    momentum_rate = (alpha_t + speed * alpha_r + speed_r * alpha) * temporal + alpha * temporal_rate
    flux = alpha * speed * temporal + beta * gradient
    field_work = measure @ (momentum_rate * field + flux * field_r)
    mesh_work = measure @ (-momentum_rate * gradient * eta - alpha * temporal * gradient_rate * eta
        - (alpha_r * temporal**2 - beta_r * gradient**2) * eta / 2
        - (alpha * temporal**2 / 2 + beta * gradient**2 / 2 + alpha * speed * temporal * gradient) * eta_r)
    label, label_r = field - star, field_r - star_r
    spatial, spatial_r = star - eta * gradient, star_r - eta_r * gradient - eta * gradient_r
    label_work = measure @ (momentum_rate * label + flux * label_r)
    spatial_work = measure @ (momentum_rate * spatial + flux * spatial_r)
    face_work = -raw['face_eta'] @ raw['face_density_jump']
    defect = label + spatial
    acceleration_work = measure @ (alpha * (accel - speed_rate * gradient) * defect)
    return dict(wave_field=field_work, wave_mesh=mesh_work, wave_direct=field_work + mesh_work,
        wave_label_defect=label_work, wave_spatial_defect=spatial_work, wave_faces=face_work,
        wave_identity=label_work + spatial_work + face_work,
        kinetic_defect=measure @ (alpha * defect**2), kinetic_label_defect=measure @ (alpha * label**2),
        kinetic_spatial_defect=measure @ (alpha * spatial**2), kinetic_cross=2 * measure @ (alpha * spatial * label),
        wave_without_acceleration=label_work + spatial_work + face_work - acceleration_work,
        wave_acceleration=acceleration_work)


def finite_wave_derivatives(raw, step):
    measure, alpha, beta, alpha_r, beta_r, alpha_t, gradient, rate, accel, speed, speed_r, speed_rate, eta, eta_r, field, field_r = [raw[key] for key in
        ['measure', 'alpha', 'beta', 'alpha_r', 'beta_r', 'alpha_t', 'gradient', 'rate', 'acceleration', 'speed', 'speed_r', 'speed_rate', 'eta', 'eta_r', 'field', 'field_r']]
    amount = 1j * step
    span = 1 + amount * eta_r
    moved_gradient = (gradient + amount * field_r) / span
    moved_alpha, moved_beta = alpha + amount * alpha_r * eta, beta + amount * beta_r * eta
    lagrangian = measure @ (span * (moved_alpha * (rate - speed * moved_gradient)**2 - moved_beta * moved_gradient**2) / 2)
    span = 1 + amount * speed_r
    moved_gradient = (gradient + amount * raw['rate_r']) / span
    moved_alpha = alpha + amount * (alpha_t + speed * alpha_r)
    moved_temporal = rate + amount * accel - (speed + amount * speed_rate) * moved_gradient
    momentum = measure @ (span * moved_alpha * moved_temporal * (field - eta * moved_gradient))
    return np.array([lagrangian.imag / step, momentum.imag / step, (momentum.imag - lagrangian.imag) / step])


def layer(engine, loads, action, tangent, acceleration, polynomial, edge_vertices, field_vertices, label, order):
    data = physical_data(engine, loads, action, label)
    cardinal = data['cardinal']
    edge_test, field_test = cardinal @ edge_vertices, cardinal @ field_vertices
    result = engine.evaluate(data['edges'], data['field'], data['beta'])
    star_nodes = np.asarray(nodal_transport(engine, result, decimals(edge_test)), float)
    row = samples(action, label, order)
    geometry, quad = row['geometry'], row['quadrature']
    cells, local = quad['cells'], quad['local']
    reference_edges = np.array([float(value) for value in action.edges])
    widths = np.diff(reference_edges)[cells] * geometry['jacobian']
    indices = engine.indices[cells]
    field, field_r = interpolate_nodal(field_test, indices, local, widths)
    star, star_r = interpolate_nodal(star_nodes, indices, local, widths)
    eta = edge_test[cells] * (1 - local) + edge_test[cells + 1] * local
    eta_r = (edge_test[cells + 1] - edge_test[cells]) / widths
    radius, metric = geometry['radius'], geometry['metric']
    alpha = radius**2 / (geometry['lapse'] * np.sqrt(metric))
    beta = radius**2 * geometry['lapse'] * np.sqrt(metric)
    alpha_r = alpha * (2 / radius - geometry['lapse_log_radial'] - geometry['metric_radial'] / (2 * metric))
    beta_r = beta * (2 / radius + geometry['lapse_log_radial'] + geometry['metric_radial'] / (2 * metric))
    nu_t, metric_t = tangent.at(radius)
    alpha_t = -alpha * (nu_t[-1] + metric_t[-1] / (2 * metric))
    gradient = row['gradient'] / geometry['jacobian']
    gradient_r = np.einsum('cpl,l->cp', action.gradient, cardinal)[cells, 1] / (widths * geometry['jacobian'])
    coefficients = np.einsum('cpl,l->cp', polynomial, cardinal)[cells]
    accel = coefficients[:, 0] + local * (coefficients[:, 1] + local * coefficients[:, 2])
    source_accel = float(acceleration[:, -1] @ cardinal)
    edge_rate = np.asarray(data['displacement'], float) * float(data['source_velocity'])
    face_radius = np.asarray(data['edges'][1:-1], float)
    values = action.solver.values(action.solution, face_radius)[0]
    face_metric = 1 - 2 * values[0] / face_radius
    face_alpha = face_radius**2 / (np.exp(values[1]) * np.sqrt(face_metric))
    face_beta = face_radius**2 * np.exp(values[1]) * np.sqrt(face_metric)
    rate_nodes = np.asarray(data['rate'], float)
    face_indices = engine.indices[:-1, 2]
    face_rate = rate_nodes[np.maximum(face_indices, 0)] * (face_indices >= 0)
    left_gradient = np.asarray(result['atoms']['slope_right'][:-1], float)
    right_gradient = np.asarray(result['atoms']['slope_left'][1:], float)
    face_speed = edge_rate[1:-1]
    left_time = face_rate - face_speed * left_gradient
    right_time = face_rate - face_speed * right_gradient
    density_jump = (left_gradient - right_gradient) * (-face_alpha * face_speed * (left_time + right_time) - face_beta * (left_gradient + right_gradient)) / 2
    raw = dict(measure=quad['measure'] * geometry['jacobian'], alpha=alpha, beta=beta, alpha_r=alpha_r, beta_r=beta_r,
        alpha_t=alpha_t, gradient=gradient, gradient_r=gradient_r, rate=row['rate'], rate_r=row['rate_gradient'] / geometry['jacobian'],
        acceleration=accel, speed=geometry['displacement'] * row['velocity'],
        speed_r=geometry['jacobian_source'] * row['velocity'] / geometry['jacobian'], speed_rate=geometry['displacement'] * source_accel,
        eta=eta, eta_r=eta_r, field=field, field_r=field_r, star=star, star_r=star_r,
        face_eta=edge_test[1:-1], face_density_jump=density_jump, label=np.array(label))
    wave = evaluate_wave(raw)
    gram_field = float(sum(result['field_gradient'] * decimals(field_test), Decimal(0)))
    gram_mesh = float(sum(result['edge_gradient'] * decimals(edge_test), Decimal(0)))
    gram_coefficient = float(sum(result['load'] * data['beta_radial'] * decimals(edge_test[engine.native_edges]), Decimal(0)))
    gram = gram_field + gram_mesh + gram_coefficient
    wave.update(gram_field=gram_field, gram_mesh=gram_mesh, gram_coefficient=gram_coefficient, gram_total=gram,
        coupled_direct=wave['wave_direct'] + gram, coupled_identity=wave['wave_identity'] + gram,
        solved_field_work=wave['wave_field'] + gram_field, mesh_equation=wave['wave_mesh'] + gram_mesh + gram_coefficient,
        label_profile_max_error=float(np.max(abs(edge_test - np.asarray(pinned_tests(data['edges'], data['source'])[1], float)))))
    pins = np.max(abs(edge_test[[0, engine.anchor, -1]]))
    tangent.coordinate_rate.cache.clear()
    return np.array([wave[key] for key in CHANNELS]), raw, float(pins)
