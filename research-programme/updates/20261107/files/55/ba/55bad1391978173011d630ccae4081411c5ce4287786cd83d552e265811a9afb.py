from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from derive_annular_radial_shape_exchange_20260927 import nodal_test as original_nodal_test
from annular_radial_Ward_moments_20260921 import test_functions
from annular_geometric_pullback_20260927 import ActualPullback, DecimalBandSolve, apply_rows, dec, max_abs, quadratic, packed_rows
from decimal import Decimal, localcontext
from time import perf_counter
from bisect import bisect_right
import argparse
import contextlib
import csv
import hashlib
import json
import numpy as np


ZERO = Decimal(0)
BRANCHES = ['reference-reference', 'MTS-primary']


def load_array(path):
    with np.load(path, allow_pickle=False) as data:
        return {key: data[key].copy() for key in data.files}


def pinned_profile(action, reference, source, label):
    geometry = action.geometry(reference, source, label)
    radius, displacement = geometry['radius'], geometry['displacement']
    derivative = geometry['jacobian_source'] / geometry['jacobian']
    boundary = action.geometry(np.array([float(action.edges[0]), float(action.edges[-1])]), source, label)['radius']
    endpoints = test_functions(boundary)[0]
    source_value = test_functions(source)[0]
    inner = radius < source
    endpoint_values = np.where(inner[None, :], endpoints[:, 0, None], endpoints[:, 1, None])
    xi, xi_slope = test_functions(radius)
    eta = xi - source_value[:, None] * displacement - endpoint_values * (1 - displacement)
    slope = xi_slope - source_value[:, None] * derivative + endpoint_values * derivative
    return eta, slope


def nodal_test(action, label):
    result = original_nodal_test(action, label)
    result['eta'], result['eta_slope'] = pinned_profile(action, action.knots, result['source'], label)
    result['values'] = result['eta'] * result['gradient']
    return result


def label_data(loads, action, pullback, label):
    nodal = nodal_test(action, label)
    geometry, cardinal = nodal['geometry'], nodal['cardinal']
    fields = np.column_stack([loads.coordinates[:, :-1].T @ dec(cardinal), dec(loads.rates[:, :-1].T) @ dec(cardinal)])
    image = action.factor.apply(fields)
    weights = dec(np.asarray(action.sampling @ geometry['gradient']).ravel())
    coefficient = 2 / geometry['radius'] + geometry['lapse_log_radial'] + geometry['metric_radial'] / (2 * geometry['metric'])
    response, directions = [], []
    for test in range(3):
        speed = dec(nodal['eta'][test] / geometry['jacobian'])
        weight_rate = dec(np.asarray(action.sampling @ (geometry['gradient'] *
            (coefficient * nodal['eta'][test] - nodal['eta_slope'][test]))).ravel())
        side_responses, side_directions = [], []
        for rows, curvatures in pullback.generators(speed):
            direction = apply_rows(rows, fields)
            curvature = apply_rows(curvatures, fields)
            factor_direction = action.factor.apply(direction)
            field_work = sum(weights * image[:, 0] * factor_direction[:, 0], ZERO)
            coefficient_work = sum(weight_rate * image[:, 0]**2 / 2, ZERO)
            changed_factor = -factor_direction[:, 0] - weight_rate * image[:, 0] / (2 * weights) if len(weights) else np.array([], dtype=object)
            operator_work = sum(weights * image[:, 0] * changed_factor, ZERO)
            net = field_work + coefficient_work + operator_work
            side_responses.append([field_work, coefficient_work, operator_work, net])
            side_directions.append((direction, curvature))
        response.append(side_responses)
        directions.append(side_directions)
    return dict(nodal=nodal, fields=fields, image=image, weights=weights, response=np.array(response, dtype=object), directions=directions)


def closure_defect(action, pullback, nodal, old, moved, amount, test):
    points = np.array([float(lower + fraction * width) for lower, width in zip(pullback.edges[:-1], pullback.widths)
                       for fraction in [Decimal('.25'), Decimal('.75')]])
    geometry = action.geometry(points, nodal['source'], float(nodal['label']))
    eta = pinned_profile(action, points, nodal['source'], float(nodal['label']))[0][test]
    exact_points = [lower + fraction * width for lower, width in zip(pullback.edges[:-1], pullback.widths)
                    for fraction in [Decimal('.25'), Decimal('.75')]]
    interpolated, exact = [], []
    for index, (point, displacement) in enumerate(zip(exact_points, dec(eta / geometry['jacobian']))):
        target = point + amount * displacement
        cell = max(0, min(len(pullback.widths) - 1, bisect_right(pullback.edges, target) - 1))
        interpolated.append(sum((value * moved[column, 0] for column, value in pullback.row(point, index // 2).items()), ZERO))
        exact.append(sum((value * old[column, 0] for column, value in pullback.row(target, cell).items()), ZERO))
    return float(max_abs(np.array(interpolated, dtype=object) - np.array(exact, dtype=object)) / max_abs(old[:, 0]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='annular-geometric-pullback-attempt02')
    parser.add_argument('--max-seconds', type=float, default=7200)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(scope='Endpoint/source-pinned actual P2 pullback and same-functional Gram transport; passive, not a physical action replacement.',
            new_nonlinear_solves=0, physics_action_changed=False, current_repaired=False, subagents_used=False, github_action=False,
            protected_since='2026-09-27T22:22:41+00:00', finite_cases=[])
        evidence.own(evidence.root / 'DERIVATION-20260927-geometric-pullback-and-current-chain.md')
        evidence.own(evidence.root / 'DERIVATION-20260927-pullback-boundary-correction.md')
        evidence.own(evidence.output.parent / 'annular-geometric-pullback-attempt01/status.json')
        evidence.report['profile'] = 'xi minus piecewise affine interpolant through endpoints and source'
        authority_path = evidence.output.parent / 'annular-support-map-constraints-validation-attempt01/status.json'
        authority = json.loads(authority_path.read_text())
        evidence.check('source_complete', authority['state'] == 'complete' and all(row['passed'] for row in authority['checks']))
        evidence.own(authority_path)
        digests = {}
        for table in ['inputs', 'outputs']:
            for relative, digest in authority[table].items():
                if relative in digests and digests[relative] != digest:
                    raise ValueError('Hash conflict')
                digests[relative] = digest
        for relative, digest in digests.items():
            path = evidence.root / relative
            evidence.check('hash:' + relative, path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest)
            evidence.own(path)

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe runtime boundary; saved completed work retained')

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        table, finite_table = [], []
        with localcontext() as context:
            context.prec = 64
            for branch in BRANCHES:
                for level in ['fine', 'third']:
                    name = branch + '-' + level
                    progress(name + ':restore')
                    loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                    pullback = ActualPullback(action.mesh)
                    material_paths, finite_paths, averages = [], [], []
                    for order in [48, 64]:
                        labels, weights = np.polynomial.legendre.leggauss(order)
                        labels, weights = labels / 2, weights / 2
                        weights *= 6 * (labels + .5) * (.5 - labels)
                        responses, jump_norms, centered_errors = [], [], []
                        for label_index, label in enumerate(labels):
                            if label_index % 8 == 0:
                                progress(name + ':material' + str(order) + ':label' + str(label_index))
                            data = label_data(loads, action, pullback, label)
                            nodal, geometry = data['nodal'], data['nodal']['geometry']
                            nodal['label'] = label
                            pins = np.array([float(action.edges[0]), action.owner.model.anchor, float(action.edges[-1])])
                            pin_error = float(np.max(abs(pinned_profile(action, pins, nodal['source'], label)[0])))
                            evidence.check(name + ':pins:' + str(order) + ':' + str(label_index), pin_error <= 2e-14, pin_error)
                            responses.append(np.asarray(data['response'], float))
                            centers, jumps = [], []
                            for test, directions in enumerate(data['directions']):
                                centered = (directions[0][0][:, 0] + directions[1][0][:, 0]) / 2
                                centers.append(float(max_abs(centered - dec(nodal['values'][test])) / max(max_abs(centered), Decimal('1e-100'))))
                                jumps.append(float(max_abs(directions[0][0][:, 0] - directions[1][0][:, 0])))
                            centered_errors.append(centers)
                            jump_norms.append(jumps)
                            scale = max(max_abs(data['response'][:, :, :3]), Decimal('1e-100'))
                            evidence.check(name + ':transport:' + str(order) + ':' + str(label_index),
                                max_abs(data['response'][:, :, 3]) <= Decimal('1e-40') * scale)
                            evidence.check(name + ':centered_generator:' + str(order) + ':' + str(label_index), max(centers) <= 2e-12, max(centers))
                            if order != 64 or label_index not in [0, 31, 63]:
                                continue
                            for test in range(3):
                                speed = dec(nodal['eta'][test] / geometry['jacobian'])
                                strain = dec(nodal['eta_slope'][test])
                                step = pullback.safe_step(speed, strain)
                                old_energy = [quadratic(data['weights'], data['image'][:, field]) for field in range(2)]
                                for resolution in range(3):
                                    for sign in [-1, 1]:
                                        amount = sign * step / (2**resolution)
                                        rows, derivative_rows = pullback.rows(amount, speed)
                                        solver = DecimalBandSolve(rows)
                                        moved = apply_rows(rows, data['fields'])
                                        recovered = solver.solve(moved)
                                        field_scale = max_abs(data['fields'])
                                        inverse_error = max_abs(recovered - data['fields']) / field_scale
                                        derivative = apply_rows(derivative_rows, data['fields'])
                                        new_rate = moved[:, 1:2] + derivative[:, 0:1]
                                        connected = solver.solve(new_rate - apply_rows(derivative_rows, recovered[:, 0:1]))
                                        connection_error = max_abs(connected[:, 0] - data['fields'][:, 1]) / field_scale
                                        expected_direction, curvature = data['directions'][test][0 if sign == 1 else 1]
                                        polynomial_error = max_abs(moved - data['fields'] - amount * expected_direction - amount**2 * curvature) / field_scale
                                        radius = geometry['radius'] + float(amount) * nodal['eta'][test]
                                        jacobian = geometry['jacobian'] * (1 + float(amount) * nodal['eta_slope'][test])
                                        metric_values = action.solver.values(action.solution, radius)[0]
                                        gamma = radius**2 * np.exp(metric_values[1]) * np.sqrt(1 - 2 * metric_values[0] / radius) / jacobian
                                        new_weights = dec(np.asarray(action.sampling @ gamma).ravel())
                                        if len(new_weights) and min(new_weights) <= 0:
                                            raise ValueError('Nonpositive transported row weight')
                                        factor = action.factor.apply(recovered)
                                        row_scale = np.array([(old / new).sqrt() for old, new in zip(data['weights'], new_weights)], dtype=object)
                                        transported = factor * row_scale[:, None]
                                        invariant_energies = [quadratic(new_weights, transported[:, field]) for field in range(2)]
                                        energy_errors = [abs(new - old) / max(abs(old), Decimal('1e-100')) for new, old in zip(invariant_energies, old_energy)]
                                        untransported = action.factor.apply(moved)
                                        raw_energy = quadratic(new_weights, untransported[:, 0])
                                        derivative_estimate = (raw_energy - old_energy[0]) / amount
                                        predicted = sum(data['response'][test, 0 if sign == 1 else 1, :2], ZERO)
                                        derivative_error = max_abs((moved - data['fields']) / amount - expected_direction) / field_scale
                                        suffix = name + ':label' + str(label_index) + ':test' + str(test) + ':r' + str(resolution) + ':s' + str(sign)
                                        evidence.check(suffix + ':inverse', inverse_error <= Decimal('1e-45'), float(inverse_error))
                                        evidence.check(suffix + ':finite_action', max(energy_errors) <= Decimal('1e-40'), float(max(energy_errors)))
                                        evidence.check(suffix + ':connection', connection_error <= Decimal('1e-40'), float(connection_error))
                                        evidence.check(suffix + ':piecewise_quadratic', polynomial_error <= Decimal('1e-45'), float(polynomial_error))
                                        closure = closure_defect(action, pullback, nodal, data['fields'], moved, amount, test) if resolution == 2 else None
                                        finite = dict(branch=branch, level=level, label_index=label_index, label=float(label), test=test,
                                            resolution=resolution, sign=sign, step=float(amount), row_margin=float(solver.margin),
                                            inverse_error=float(inverse_error), connection_error=float(connection_error), energy_error=float(max(energy_errors)),
                                            derivative_error=float(derivative_error), shape_derivative=float(derivative_estimate),
                                            predicted_one_sided_shape=float(predicted), interpolation_defect=closure)
                                        if resolution == 2:
                                            indices, entries = packed_rows(rows)
                                            d_indices, d_entries = packed_rows(derivative_rows)
                                            path = save(name + '-label' + str(label_index) + '-test' + str(test) + '-sign' + str(sign),
                                                indices=indices, entries=entries, derivative_indices=d_indices, derivative_entries=d_entries,
                                                old_fields=data['fields'].astype(str), moved_fields=moved.astype(str), recovered=recovered.astype(str),
                                                weights=data['weights'].astype(str), new_weights=new_weights.astype(str),
                                                old_image=data['image'].astype(str), transported_image=transported.astype(str),
                                                speed=speed.astype(str), step=np.array(str(amount)), label=np.array(label),
                                                expected_direction=expected_direction.astype(str), curvature=curvature.astype(str))
                                            finite['raw_path'] = path
                                            finite_paths.append(path)
                                        finite_table.append(finite)
                            evidence.report['finite_cases'] = finite_table
                            evidence.save()
                        response = np.array(responses)
                        average = np.tensordot(weights, response, axes=(0, 0))
                        material_paths.append(save(name + '-material' + str(order), labels=labels, weights=weights, responses=response,
                            average=average, jump_norms=np.array(jump_norms), centered_errors=np.array(centered_errors)))
                        averages.append(average)
                    prior = load_array(evidence.output.parent / 'annular-support-map-constraints-attempt01' / (name + '-material64.npz'))
                    centered_force = averages[-1][:, :, :2].sum(axis=2).mean(axis=1)
                    replay_error = np.max(abs(centered_force - prior['force_average'][2]))
                    evidence.check(name + ':pinned_force_finite', np.all(np.isfinite(centered_force)))
                    for test in range(3):
                        plus, minus = averages[-1][test, :, :2].sum(axis=1)
                        table.append(dict(branch=branch, level=level, test=test, shape_plus=plus, shape_minus=minus,
                            centered_shape=centered_force[test], shape_jump=plus - minus,
                            previous_shape=prior['force_average'][2, test], profile_change=centered_force[test] - prior['force_average'][2, test]))
                    evidence.report['cases'].append(dict(branch=branch, level=level, sources=sources,
                        material_paths=material_paths, finite_paths=finite_paths, field_count=len(action.knots),
                        gram_rows=action.factor.shape[0], old_to_pinned_shape_difference=float(replay_error)))
                    evidence.save()
        for filename, rows in [('one-sided-shape.csv', table), ('finite-pullback.csv', finite_table)]:
            path = evidence.output / filename
            keys = list(dict.fromkeys(key for row in rows for key in row))
            with path.open('w', newline='', encoding='utf-8') as handle:
                writer = csv.DictWriter(handle, fieldnames=keys)
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, finite_tests=len(finite_table),
            passive_transport_constructed=True, physical_native_kernel_rebuild_derived=False,
            current_chain='delta_g S_new = delta_g S - E^T P^(-1)(delta_g P)u, with temporal boundary terms retained',
            metric_current_changed_on_shell=False,
            maximum_saved_projection_defect=max(row['interpolation_defect'] for row in finite_table if row['interpolation_defect'] is not None))
        completion = evidence.output / 'completion.txt'
        with completion.open('w', encoding='utf-8') as handle, contextlib.redirect_stdout(handle):
            evidence.complete()
        evidence.own(completion, 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=evidence.report['seconds'],
                             finite_tests=len(finite_table), shape_rows=table)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
