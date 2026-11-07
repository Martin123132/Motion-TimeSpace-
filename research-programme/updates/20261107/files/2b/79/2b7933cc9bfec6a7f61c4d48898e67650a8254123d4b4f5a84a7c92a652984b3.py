from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_canonical_response_20260920 import common_material
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_nested_physical_refinement_v3_20260922 import adapt_owner, restore_refined
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import ProbeMetricRate, MetricResponse
from annular_joint_flow_derivative_20260922 import JointMetricTangent
from annular_joint_flow_derivative_v2_20260922 import DecimalSparseResidual
from annular_radial_Ward_moments_20260921 import test_functions, prepare
from annular_moving_Legendre_current_20260921 import samples, wave_data, dust_data
from annular_candidate_Ward_source_20260921 import fields
from annular_decimal_transport_v2_20260919 import decimal_array
from scipy.sparse import load_npz
from types import SimpleNamespace
from decimal import localcontext
from datetime import datetime
from time import perf_counter
import argparse
import contextlib
import csv
import hashlib
import json
import numpy as np
import sympy as sp


BRANCHES = ['reference-reference', 'MTS-primary']
CHANNELS = ['cell_original', 'face_original', 'dust_original', 'gram_original',
    'gram_field_work', 'gram_shape_space', 'shape_work', 'gram_advective_product',
    'gram_product_defect', 'gram_projection', 'cell_projection', 'face_projection',
    'source_material_projection', 'projected_work', 'source_identity', 'endpoint',
    'source_euler_contraction', 'source_shape_force', 'raw_eta_work']


def factor_apply(action, values):
    with localcontext() as context:
        context.prec = 64
        return np.asarray(action.factor.apply(decimal_array(values)), float)


def symbolic_checks(evidence):
    factor = sp.Matrix([[-1, 1, 0], [1, -2, 1]])
    sampling = sp.Matrix([[sp.Rational(1, 2), sp.Rational(1, 2), 0],
                          [sp.Rational(1, 4), sp.Rational(1, 2), sp.Rational(1, 4)]])
    field = sp.Matrix(sp.symbols('field0:3'))
    variation = sp.Matrix(sp.symbols('variation0:3'))
    gamma = sp.Matrix(sp.symbols('gamma0:3'))
    strain = sp.Matrix(sp.symbols('strain0:3'))
    amount = sp.symbols('epsilon')
    image = factor * (field + amount * variation)
    coefficient = sampling * (gamma + amount * sp.diag(*gamma) * strain)
    potential = sum(coefficient[index] * image[index]**2 / 2 for index in range(2))
    expected = sum((sampling * gamma)[index] * (factor * field)[index] * (factor * variation)[index]
                   for index in range(2))
    expected += sum((sampling * sp.diag(*gamma) * strain)[index] * (factor * field)[index]**2 / 2
                    for index in range(2))
    evidence.check('symbolic_potential_shape_derivative', sp.expand(sp.diff(potential, amount).subs(amount, 0) - expected) == 0)
    eta = sp.Matrix(sp.symbols('eta0:3'))
    gradient = sp.Matrix(sp.symbols('gradient0:3'))
    product = sp.diag(*eta) * gradient
    defect = factor * product - sp.diag(*(sampling * eta)) * factor * gradient
    split = sp.diag(*(sampling * eta)) * factor * gradient + defect + factor * (variation - product)
    evidence.check('symbolic_exact_rectangular_product_split', all(sp.expand(value) == 0 for value in split - factor * variation))
    radius = sp.symbols('radius')
    compact_piece = (radius - 1)**2 * (3 - radius)**2
    displacement = sp.Matrix([compact_piece.subs(radius, 1), compact_piece.subs(radius, 2)])
    slopes = sp.Matrix([sp.diff(compact_piece, radius).subs(radius, 1), sp.diff(compact_piece, radius).subs(radius, 2)])
    pair_factor, pair_field, pair_gradient = sp.Matrix([[-1, 1]]), sp.Matrix([1, 4]), sp.Matrix([2, 4])
    counterexample = ((pair_factor * pair_field).T * pair_factor * sp.diag(*displacement) * pair_gradient)[0]
    evidence.check('fixed_support_not_automatically_shape_invariant', slopes == sp.zeros(2, 1) and counterexample == 12,
                   'Compact piece on [1,3], zero outside; fixed two-node toy factor at radii 1,2, U=(u2-u1)^2/2.')
    evidence.report['exact_counterexample_shape_derivative'] = str(counterexample)


def nodal_test(action, label):
    cardinal = np.asarray(action.cardinal(label)).ravel()
    source = float(cardinal @ action.source)
    edges = np.asarray(list(map(float, action.edges)))
    cells = np.arange(len(edges) - 1)
    endpoints = [fields(action, points, cells, np.full(len(cells), local), label)
                 for points, local in [(edges[:-1], 0.), ((edges[:-1] + edges[1:]) / 2, .5), (edges[1:], 1.)]]
    indices = np.array(action.mesh['elements'])
    selected = indices >= 0
    gradients = np.column_stack([point['gradient'] for point in endpoints])
    counts, totals = np.zeros(len(action.knots)), np.zeros(len(action.knots))
    np.add.at(counts, indices[selected], 1.)
    np.add.at(totals, indices[selected], gradients[selected])
    gradient = totals / counts
    geometry = action.geometry(action.knots, source, label)
    xi, xi_slope = test_functions(geometry['radius'])
    source_xi = test_functions(source)[0]
    eta = xi - source_xi[:, None] * geometry['displacement']
    eta_slope = xi_slope - source_xi[:, None] * geometry['jacobian_source'] / geometry['jacobian']
    return dict(cardinal=cardinal, source=source, geometry=geometry, gradient=gradient,
                eta=eta, eta_slope=eta_slope, values=eta * gradient, source_xi=source_xi, traces=endpoints)


def generator(action):
    labels = action.owner.layer_rule.points / 2
    rows = [nodal_test(action, label) for label in labels]
    vertices = np.array([row['values'] for row in rows]).transpose(1, 0, 2)
    source_vertices = np.array([row['source_xi'] for row in rows]).T
    packed = vertices.transpose(2, 0, 1).reshape(len(action.knots), -1)
    images = factor_apply(action, packed).reshape(action.factor.shape[0], 3, len(labels))
    cardinals = np.array([row['cardinal'] for row in rows])
    return vertices, source_vertices, images, float(np.max(abs(cardinals - np.eye(len(labels)))))


def layer(action, loads, tangent, acceleration, polynomial, vertices, source_vertices, images, label, vary):
    row = samples(action, label, 12)
    cardinal, geometry, quadrature = row['cardinal'], row['geometry'], row['quadrature']
    cells, local, measure = quadrature['cells'], quadrature['local'], quadrature['measure']
    point = fields(action, quadrature['reference'], cells, local, label)
    coefficients = np.einsum('cpl,l->cp', polynomial, cardinal)[cells]
    acceleration_field = coefficients[:, 0] + local * (coefficients[:, 1] + local * coefficients[:, 2])
    acceleration_source = float(acceleration[:, -1] @ cardinal)
    momentum_rate = wave_data(row, tangent)['momentum_rate'][-1]
    momentum_rate += geometry['kinetic'] * (acceleration_field + acceleration_source * row['motion'])
    euler = -momentum_rate - point['flux_x']
    xi = test_functions(geometry['radius'])[0]
    source_xi = test_functions(row['source'])[0]
    eta = xi - source_xi[:, None] * geometry['displacement']
    actual = eta * point['gradient']
    nodal = nodal_test(action, label)
    projected_nodes = np.einsum('tln,l->tn', vertices, cardinal)
    source_projected = source_vertices @ cardinal
    projected_image = np.einsum('atl,l->at', images, cardinal)
    projected = np.einsum('tqv,qv->tq', projected_nodes[:, quadrature['indices']], row['shape'])
    left, middle, right = nodal['traces']
    face_radius = right['radius'][:-1]
    face_geometry = action.geometry(np.array(list(map(float, action.edges)))[1:-1], row['source'], label)
    face_speed = (right['speed'][:-1] + left['speed'][1:]) / 2
    face_force = (left['beta'][1:] - left['alpha'][1:] * face_speed**2) * (left['gradient'][1:] - right['gradient'][:-1])
    face_gradient = (left['gradient'][1:] + right['gradient'][:-1]) / 2
    face_xi = test_functions(face_radius)[0]
    face_eta = face_xi - source_xi[:, None] * face_geometry['displacement']
    face_indices = np.array(action.mesh['elements'])[:-1, 2]
    face_projected = projected_nodes[:, np.maximum(face_indices, 0)] * (face_indices >= 0)
    cell_original = np.sum(measure * euler * point['gradient'] * xi, axis=1)
    face_original = np.sum(face_force * face_gradient * face_xi, axis=1)
    raw_eta = np.sum(measure * euler * actual, axis=1) + np.sum(face_force * face_gradient * face_eta, axis=1)
    projected_wave = np.sum(measure * euler * projected, axis=1) + np.sum(face_force * face_projected, axis=1)
    cell_projection = np.sum(measure * euler * (actual - projected), axis=1)
    face_projection = np.sum(face_force * (face_eta * face_gradient - face_projected), axis=1)
    node_geometry = nodal['geometry']
    gamma = node_geometry['gradient']
    image = action.factor_values @ cardinal
    load = np.asarray(action.sampling.T @ (image**2 / 2)).ravel()
    coefficient = np.asarray(action.sampling @ gamma).ravel() * image
    gram_work = coefficient @ projected_image
    strain = 2 / node_geometry['radius'] + node_geometry['lapse_log_radial'] + node_geometry['metric_radial'] / (2 * node_geometry['metric'])
    gram_space = np.sum(gamma * load * (strain * test_functions(node_geometry['radius'])[0]
                        - test_functions(node_geometry['radius'])[1]), axis=1)
    shape_space = np.sum(gamma * load * (strain * nodal['eta'] - nodal['eta_slope']), axis=1)
    product_images = factor_apply(action, np.column_stack([nodal['gradient'], nodal['values'].T]))
    transport_image = (action.sampling @ nodal['eta'].T) * product_images[:, 0, None]
    product_defect = product_images[:, 1:] - transport_image
    projection_image = projected_image - product_images[:, 1:]
    advective = coefficient @ transport_image
    defect = coefficient @ product_defect
    projection = coefficient @ projection_image
    gram_source = -float(node_geometry['gradient_source'] @ load)
    source_test_work = np.sum(measure * euler * geometry['displacement'] * point['gradient'])
    source_test_work += np.sum(face_force * face_geometry['displacement'] * face_gradient)
    wave_source_force = geometry['kinetic_source'] * row['temporal']**2 / 2
    wave_source_force -= geometry['kinetic'] * row['temporal'] * row['velocity'] * row['motion'] * geometry['jacobian_source'] / geometry['jacobian']
    wave_source_force -= geometry['gradient_source'] * row['gradient']**2 / 2
    wave_source_euler = float(measure @ (wave_source_force - row['motion_rate'] * geometry['kinetic'] * row['temporal']
                                        - row['motion'] * momentum_rate))
    dust = dust_data(action, row['source'], row['velocity'], tangent)
    dust_euler = dust['momentum_rate'][-1] + dust['inertia'] * acceleration_source - action.dust(row['source'], row['velocity'])[1]
    source_euler = wave_source_euler + gram_source - dust_euler
    source_identity = source_xi * (wave_source_euler + source_test_work)
    endpoint = left['energy'][0] * test_functions(left['radius'][0])[0] - right['energy'][-1] * test_functions(right['radius'][-1])[0]
    values = np.array([cell_original, face_original, dust_euler * source_xi, gram_space,
        gram_work, shape_space, gram_work + shape_space, advective, defect, projection,
        cell_projection, face_projection, -(source_xi - source_projected) * source_euler,
        projected_wave - gram_work - source_projected * source_euler, source_identity, endpoint,
        -source_xi * source_euler, source_xi * gram_source, raw_eta])
    variations = []
    if vary:
        for test in range(3):
            for step in [1e-18, 1e-22]:
                moved_radius = node_geometry['radius'] + 1j * step * nodal['eta'][test]
                moved_jacobian = node_geometry['jacobian'] * (1 + 1j * step * nodal['eta_slope'][test])
                moved_values = action.solver.values(action.solution, moved_radius)[0]
                moved_gamma = moved_radius**2 * np.exp(moved_values[1]) * np.sqrt(1 - 2 * moved_values[0] / moved_radius) / moved_jacobian
                moved_image = image + 1j * step * projected_image[:, test]
                potential = (action.sampling @ moved_gamma) @ moved_image**2 / 2
                variations.append([test, step, potential.imag / step, values[6, test]])
    raw = dict(image=image, coefficient=coefficient, projected_image=projected_image,
               transport_image=transport_image, product_defect=product_defect, projection_image=projection_image,
               gram_atom_energy=gamma * load, shape_strain=strain * nodal['eta'] - nodal['eta_slope'])
    return values, np.array(variations).reshape(-1, 4), raw


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='annular-radial-shape-exchange-attempt01')
    parser.add_argument('--max-seconds', type=float, default=7200)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        intake = evidence.output.parent
        authorities, digests = {}, {}
        evidence.report.update(scientific_checks=[], new_nonlinear_solves=0, github_action=False, subagents_used=False,
            scope='Same-action fixed-support radial shape-work identity, tested on saved third-grid centres.',
            channels=CHANNELS, branches=BRANCHES, protected_since='2026-09-27T21:24:50+00:00')
        evidence.own(evidence.root / 'DERIVATION-20260927-fixed-support-radial-shape-work.md')
        for name in BRANCHES:
            short = 'reference' if name == 'reference-reference' else name
            for suffix in ['attempt02', 'validation-attempt02']:
                folder = 'annular-' + short + '-third-current-' + suffix
                path = intake / folder / 'status.json'
                status = json.loads(path.read_text())
                evidence.check(folder + ':complete', status['state'] == 'complete' and status['full_radial_comparison_completed']
                               and not status['pending_cases'] and all(row['passed'] for row in status['checks']))
                evidence.own(path)
                authorities[folder] = status
                for table in ['inputs', 'outputs']:
                    for relative, digest in status[table].items():
                        if relative in digests and digests[relative] != digest:
                            raise RuntimeError('Conflicting authority: ' + relative)
                        digests[relative] = digest
        for relative, digest in digests.items():
            path = evidence.root / relative
            evidence.check('hash:' + relative, path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest)
            evidence.own(path)

        def read(relative):
            path = evidence.root / relative
            if str(path.relative_to(evidence.root)) not in digests:
                raise RuntimeError('Unowned input: ' + str(relative))
            if path.suffix == '.json':
                return json.loads(path.read_text())
            with np.load(path, allow_pickle=False) as archive:
                return {key: archive[key].copy() for key in archive.files}

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe runtime boundary; completed branch data preserved')

        def science(name, error, tolerance):
            evidence.report['scientific_checks'].append(dict(name=name, error=float(error), tolerance=float(tolerance),
                passed=bool(np.isfinite(error) and error <= tolerance)))
            evidence.save()

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        symbolic_checks(evidence)
        comparisons = []
        for name in BRANCHES:
            progress(name + ':restore-centre')
            branch, extension = name.split('-')
            short = 'reference' if branch == 'reference' else name
            parent = authorities['annular-' + short + '-third-current-attempt02']
            row = parent['centres'][0]
            original = read(str((intake / 'annular-candidate-initial-metric-attempt02' / (branch + '-velocity-owned-inputs.npz')).relative_to(evidence.root)))
            overlay = read(str((intake / 'annular-transfer-kernel-overlay-attempt01' / (branch + '-exact-common-overlay.json')).relative_to(evidence.root)))
            packet = read(str((intake / 'annular-resampled-third-grid-preparation-attempt01' / (name + '-third-action.json')).relative_to(evidence.root)))
            native = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            base, unused, unused2 = common_material(native, original, overlay)
            owner = adapt_owner(base, packet['mesh'])
            state, flow = read(row['state_path']), read(row['flow_path'])
            loads, action = restore_refined(owner, state, packet['mesh'], packet, extension, deadline)
            probes = {}
            for index in range(3):
                for sign in [-1, 1]:
                    suffix = '-inner' + str(index) + '-sign' + str(sign) + '.npz'
                    archived = read(next(path for path in row['probe_paths'] if path.endswith(suffix)))
                    solver, solution = reconstructed_solver(archived)
                    probes[index, sign] = SimpleNamespace(solver=solver, solution=solution)
            coordinate = ProbeMetricRate(probes, flow['inner_steps'])
            responses = []
            for estimate in range(2):
                final = max((entry for entry in parent['iterations'] if entry['case'] == row['case'] and entry['estimate'] == estimate),
                            key=lambda entry: entry['iteration'])
                saved = read(final['output'])
                evidence.check(name + ':saved_acceleration:' + str(estimate), np.array_equal(saved['acceleration'], flow['accelerations'][estimate]))
                solution = {key: saved['metric_' + key] for key in ['state', 'rhs_coefficients', 'primitives', 'left']}
                responses.append(MetricResponse(action.solver, solution, saved['forcing'], final['radial_linear_residual'], []))
            tangent = JointMetricTangent(coordinate, responses)
            evidence.check(name + ':reconstructed_metric_jet', np.max(abs(tangent.values(flow['radius']) - flow['metric_rate'])) <= 2e-18)
            coordinate.cache.clear()
            polynomial, unused = prepare(action, loads, flow['accelerations'][-1])
            vertices, source_vertices, images, cardinal_error = generator(action)
            evidence.check(name + ':material_cardinals', cardinal_error <= 2e-12)
            matrix = load_npz(evidence.root / row['matrix_path'])
            rhs = flow['force'] - flow['coordinate_convection'] - flow['coordinate_momentum'][-1]
            residual = -DecimalSparseResidual(matrix).evaluate(flow['accelerations'][-1], flow['coupling'][-1], rhs)
            canonical_test = np.concatenate([vertices, -source_vertices[:, :, None]], axis=2)
            canonical_work = canonical_test.reshape(3, -1) @ residual.ravel()
            generator_path = save(name + '-generator', vertices=vertices, source_vertices=source_vertices,
                                  images=images, canonical_euler=residual, canonical_work=canonical_work)
            averages, paths, variations_all = [], [], []
            for order in [48, 64]:
                labels, weights = np.polynomial.legendre.leggauss(order)
                labels, weights = labels / 2, weights / 2
                weights *= 6 * (labels + .5) * (.5 - labels)
                values = []
                for index, label in enumerate(labels):
                    if index % 16 == 0:
                        progress(name + ':material' + str(order) + ':label' + str(index))
                    current, variations, raw = layer(action, loads, tangent, flow['accelerations'][-1], polynomial,
                        vertices, source_vertices, images, label, order == 64 and index in [0, 31, 63])
                    values.append(current)
                    coordinate.cache.clear()
                    science(name + ':product:' + str(order) + ':' + str(index), np.max(abs(current[4] - current[7:10].sum(axis=0))), 2e-16)
                    science(name + ':source_identity:' + str(order) + ':' + str(index), np.max(abs(current[14])), 2e-16)
                    if len(variations):
                        raw_path = save(name + '-variation-label' + str(index), **raw, variations=variations, label=np.array(label))
                        variations_all.append(raw_path)
                        for test, step, measured, expected in variations:
                            science(name + ':direct_potential_variation:' + str(index) + ':' + str(int(test)) + ':' + str(step),
                                    abs(measured - expected), 2e-18 + 2e-8 * abs(expected))
                values = np.array(values)
                average = np.tensordot(weights, values, axes=(0, 0))
                paths.append(save(name + '-material' + str(order), labels=labels, weights=weights, values=values,
                                  average=average, channels=np.array(CHANNELS)))
                averages.append(average)
            old = read(row['moment_paths'][1])
            for index, key in [(0, 'cell_source'), (1, 'face_source'), (2, 'dust_euler'), (3, 'gram_space'), (15, 'endpoint_source')]:
                science(name + ':saved_centre:' + key, np.max(abs(averages[1][index] - old['sum_' + key])), 2e-16)
            components = read(parent['summaries'][0]['component_path'])
            current_rate = components['components'][-1, 5:].sum(axis=0)
            weak_assembly = averages[0][13] - canonical_work
            material_change = averages[1][13] - averages[0][13]
            science(name + ':projected_weak_assembly', np.max(abs(weak_assembly)), 2e-16)
            predicted = (averages[1][6] + current_rate + averages[1][10:13].sum(axis=0) + canonical_work
                         + weak_assembly + material_change + averages[1][14] + averages[1][15])
            old_component_sum = components['components'][-1].sum(axis=0)
            science(name + ':old_component_sum', np.max(abs(predicted - old_component_sum)), 2e-16)
            if branch == 'reference':
                evidence.check('reference_Gram_shape_control_zero', np.max(abs(averages[1][4:10])) == 0.)
            for test in range(3):
                comparisons.append(dict(branch=name, test=test, direct=components['radial'][1, -1, test],
                    old_component_sum=old_component_sum[test], predicted=predicted[test], shape_work=averages[1][6, test],
                    gram_field_work=averages[1][4, test], gram_shape_space=averages[1][5, test],
                    gram_advective_product=averages[1][7, test], gram_product_defect=averages[1][8, test], gram_projection=averages[1][9, test],
                    full_current_correction_rate=current_rate[test], gram_bond_rate=components['components'][-1, 7, test],
                    cell_projection=averages[1][10, test], face_projection=averages[1][11, test],
                    source_material_projection=averages[1][12, test], canonical_euler_work=canonical_work[test],
                    weak_assembly=weak_assembly[test], material_work_change=material_change[test],
                    source_identity=averages[1][14, test], endpoint=averages[1][15, test],
                    predicted_minus_components=predicted[test] - old_component_sum[test],
                    direct_minus_predicted=components['radial'][1, -1, test] - predicted[test]))
            evidence.report['cases'].append(dict(branch=name, generator_path=generator_path, quadrature_paths=paths,
                variation_paths=variations_all, count=state['rates'].size, faces=len(action.edges) - 2,
                shape_work=averages[1][6].tolist(), canonical_work=canonical_work.tolist(), seconds=perf_counter() - started))
            evidence.save()
        table_path = evidence.output / 'radial-shape-balance.csv'
        with table_path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(comparisons[0]))
            writer.writeheader()
            writer.writerows(comparisons)
        evidence.own(table_path, 'outputs')
        threshold = datetime.fromisoformat(evidence.report['protected_since']).timestamp()
        changed = [str(path) for path in (evidence.root.parent / 'formalization-workbench').rglob('*')
                   if path.is_file() and path.stat().st_mtime >= threshold]
        evidence.check('protected_workbench_unchanged', not changed, changed)
        evidence.check('no_scripts_bytecode_cache', not (evidence.root / 'scripts/__pycache__').exists())
        evidence.report.update(seconds=perf_counter() - started, comparison=comparisons,
            science_passed=sum(row['passed'] for row in evidence.report['scientific_checks']),
            science_total=len(evidence.report['scientific_checks']), protected_workbench_changed_count=len(changed))
        with (evidence.output / 'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output / 'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', seconds=evidence.report['seconds'], checks=len(evidence.report['checks']),
                              science_passed=evidence.report['science_passed'], science_total=evidence.report['science_total'],
                              comparison=comparisons)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
