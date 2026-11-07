from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_candidate_Ward_source_20260921 import fields
from annular_radial_Ward_moments_20260921 import test_functions
from annular_decimal_transport_v2_20260919 import decimal_array
from decimal import Decimal, localcontext
from datetime import datetime
from time import perf_counter
import argparse
import contextlib
import csv
import hashlib
import json
import numpy as np
import sympy as sp


def archive(path):
    with np.load(path, allow_pickle=False) as data:
        return {key: data[key].copy() for key in data.files}


def symbolic_euler(evidence):
    time, reference = sp.symbols('t x', real=True)
    field = sp.Function('u')(time, reference)
    support = sp.Function('chi')(time, reference)
    jac, speed = sp.diff(support, reference), sp.diff(support, time)
    gradient = sp.diff(field, reference) / jac
    temporal = sp.diff(field, time) - speed * gradient
    alpha, beta = sp.Function('alpha')(time, support), sp.Function('beta')(time, support)
    density = jac * (alpha * temporal**2 - beta * gradient**2) / 2
    eulers = []
    for function in [field, support]:
        value = sp.diff(density, function)
        value -= sp.diff(sp.diff(density, sp.diff(function, time)), time)
        value -= sp.diff(sp.diff(density, sp.diff(function, reference)), reference)
        eulers.append(value)
    evidence.check('independent:explicit_Euler_wave_identity', sp.simplify(eulers[1] + gradient * eulers[0]) == 0)


def fresh_probe(action, vertices, label):
    cardinal = np.asarray(action.cardinal(label)).ravel()
    source = cardinal @ action.source
    quad = action.quadrature(label, source, 12)
    geometry = action.geometry(quad['reference'], source, label)
    point = fields(action, quad['reference'], quad['cells'], quad['local'], label)
    eta = test_functions(point['radius'])[0] - test_functions(source)[0][:, None] * geometry['displacement']
    actual = eta * point['gradient']
    local = quad['local']
    basis = np.stack([2 * local**2 - 3 * local + 1, 4 * local - 4 * local**2, 2 * local**2 - local], axis=1)
    basis *= np.asarray(action.mesh['elements'])[quad['cells']] >= 0
    coefficients = np.tensordot(vertices, cardinal, axes=(1, 0))
    projected = np.sum(coefficients[:, quad['indices']] * basis, axis=2)
    kinetic = geometry['jacobian'] * point['alpha']
    weight = quad['measure'] * kinetic
    node_geometry = action.geometry(action.knots, source, label)
    node_eta = test_functions(node_geometry['radius'])[0] - test_functions(source)[0][:, None] * node_geometry['displacement']
    node_strain = test_functions(node_geometry['radius'])[1] - test_functions(source)[0][:, None] * node_geometry['jacobian_source'] / node_geometry['jacobian']
    node_strain = (2 / node_geometry['radius'] + node_geometry['lapse_log_radial']
        + node_geometry['metric_radial'] / (2 * node_geometry['metric'])) * node_eta - node_strain
    with localcontext() as context:
        context.prec = 64
        projected_image = np.asarray(action.factor.apply(decimal_array(coefficients.T)), float)
    image = action.factor_values @ cardinal
    gamma = node_geometry['gradient']
    field_work = ((action.sampling @ gamma) * image) @ projected_image
    support_work = np.sum((action.sampling @ (gamma * node_strain).T) * (image**2 / 2)[:, None], axis=0)
    return dict(weight=weight, projected=projected, actual=actual, gradient=point['gradient'], eta=eta,
                kinetic=kinetic, forces=np.array([field_work, support_work, field_work + support_work]))


def finite_difference_curvatures(raw):
    directions = [np.array([1., 0., 0., 1., 0., 0.]), np.array([0., 1., 0., 0., 1., 0.]),
                  np.array([0., 0., 1., 0., 0., 1.]), np.array([1., -.5, .25, -.25, .5, 1.])]
    selected = np.linspace(0, len(raw['weight']) - 1, 31, dtype=int)
    results = []
    with localcontext() as context:
        context.prec = 64
        for direction in directions:
            for amount in [Decimal('0.01'), Decimal('0.003')]:
                measured, expected = Decimal(0), Decimal(0)
                for index in selected:
                    weight = Decimal(str(raw['weight'][index]))
                    rate = Decimal(str(raw['rate'][index]))
                    speed = Decimal(str(raw['speed'][index]))
                    gradient = Decimal(str(raw['gradient'][index]))
                    field_direction = sum(Decimal(str(direction[test])) * Decimal(str(raw['projected'][test, index])) for test in range(3))
                    map_direction = sum(Decimal(str(direction[test + 3])) * Decimal(str(raw['eta'][test, index])) for test in range(3))
                    original = rate - speed * gradient
                    plus = rate + amount * field_direction - (speed + amount * map_direction) * gradient
                    minus = rate - amount * field_direction - (speed - amount * map_direction) * gradient
                    measured += weight * (plus**2 / 2 + minus**2 / 2 - original**2) / amount**2
                    expected += weight * (field_direction - map_direction * gradient)**2
                results.append([float(amount), float(measured), float(expected), float(abs(measured - expected))])
    return np.array(results)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', default='annular-support-map-constraints-attempt01')
    parser.add_argument('--label', default='annular-support-map-constraints-validation-attempt01')
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + 3600
    try:
        report_path = evidence.output.parent / args.run / 'status.json'
        report = json.loads(report_path.read_text())
        evidence.check('main_complete', report['state'] == 'complete' and all(row['passed'] for row in report['checks']))
        evidence.own(report_path)
        digests = {}
        for table in ['inputs', 'outputs']:
            for relative, digest in report[table].items():
                if relative in digests and digests[relative] != digest:
                    raise RuntimeError('Conflicting main hash')
                digests[relative] = digest
        for relative, digest in digests.items():
            path = evidence.root / relative
            evidence.check('hash:' + relative, path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest)
            evidence.own(path)
        symbolic_euler(evidence)
        replay_count, finite_count, errors = 0, 0, []
        with (report_path.parent / 'support-map-profiles.csv').open(newline='', encoding='utf-8') as handle:
            table = list(csv.DictReader(handle))
        evidence.check('CSV_clean_12_rows', len(table) == 12 and all(None not in row and None not in row.values() for row in table))
        evidence.check('four_required_cases', {(case['branch'], case['level']) for case in report['cases']} ==
                       {(branch, level) for branch in ['reference-reference', 'MTS-primary'] for level in ['fine', 'third']})
        for case in report['cases']:
            name = case['branch'] + '-' + case['level']
            print(json.dumps(dict(stage=name, seconds=perf_counter() - started)), flush=True)
            averages = []
            for path in case['material_paths']:
                saved = archive(evidence.root / path)
                order = len(saved['labels'])
                labels, weights = np.polynomial.legendre.leggauss(order)
                labels, weights = labels / 2, weights / 2
                weights *= 6 * (labels + .5) * (.5 - labels)
                evidence.check(name + ':quadrature:' + str(order), np.array_equal(labels, saved['labels']) and np.array_equal(weights, saved['weights']))
                evidence.check(name + ':positive_weights:' + str(order), np.all(weights > 0) and abs(sum(weights) - 1) < 2e-14)
                average = np.einsum('l,labc->abc', weights, saved['blocks'])
                force = np.einsum('l,lab->ab', weights, saved['forces'])
                scale = np.max(abs(average[:3]))
                evidence.check(name + ':matrix_average:' + str(order), np.max(abs(average - saved['average'])) <= 2e-13 * scale)
                evidence.check(name + ':force_average:' + str(order), np.max(abs(force - saved['force_average'])) <= 2e-18)
                for index, blocks in enumerate(saved['blocks']):
                    field, cross, support, defect = blocks
                    local_scale = np.max(abs(blocks[:3]))
                    error = np.max(abs(defect - field + cross + cross.T - support))
                    hessian = np.block([[field, -cross], [-cross.T, support]])
                    evidence.check(name + ':layer:' + str(order) + ':' + str(index), error <= 2e-13 * local_scale
                        and np.linalg.eigvalsh(hessian)[0] >= -2e-13 * local_scale and np.linalg.eigvalsh(defect)[0] >= -2e-13 * local_scale)
                    replay_count += 1
                averages.append((average, force))
            for test in range(3):
                row = next(row for row in table if row['branch'] == case['branch'] and row['level'] == case['level'] and int(row['test']) == test)
                average, force = averages[-1]
                expected = dict(shape_work=force[2, test], field_work=force[0, test], support_work=force[1, test],
                    map_mass=average[2, test, test], projected_null_mass=average[3, test, test],
                    projected_null_fraction=average[3, test, test] / average[2, test, test],
                    mass_quadrature_change=average[3, test, test] - averages[0][0][3, test, test],
                    force_quadrature_change=force[2, test] - averages[0][1][2, test])
                for key, value in expected.items():
                    tolerance = 2e-18 if 'work' in key or key == 'force_quadrature_change' else max(2e-13 * abs(value), 2e-35)
                    if key == 'mass_quadrature_change':
                        tolerance = 2e-13 * average[3, test, test]
                    evidence.check(name + ':CSV:' + str(test) + ':' + key, abs(float(row[key]) - value) <= tolerance)
            loads, action, sources = restore_case(evidence, digests, case['branch'], case['level'], deadline)
            evidence.check(name + ':sources_match', sources == case['sources'])
            generator = archive(evidence.root / case['generator_path'])
            for index, path in enumerate(case['probe_paths']):
                raw = archive(evidence.root / path)
                fresh = fresh_probe(action, generator['vertices'], float(raw['label']))
                for key in ['weight', 'projected', 'actual', 'gradient', 'eta', 'kinetic']:
                    error = np.max(abs(fresh[key] - raw[key]))
                    scale = max(float(np.max(abs(raw[key]))), 1e-300)
                    evidence.check(name + ':fresh:' + str(index) + ':' + key, error <= 2e-13 * scale, float(error / scale))
                saved_force = np.array([raw['coefficient'] @ raw['projected_image'], np.sum(raw['atom'] * raw['strain'], axis=1)])
                saved_force = np.vstack([saved_force, saved_force.sum(axis=0)])
                evidence.check(name + ':fresh_force:' + str(index), np.max(abs(fresh['forces'] - saved_force)) <= 2e-18,
                               float(np.max(abs(fresh['forces'] - saved_force))))
                directions = np.array([[1., 0., 0.], [0., 1., 0.], [0., 0., 1.], [1., -.5, .25]])
                difference = fresh['projected'] - fresh['actual']
                gram = np.einsum('iq,jq,q->ij', difference, difference, fresh['weight'])
                for direction_index, direction in enumerate(directions):
                    direct = np.sum(fresh['weight'] * np.sum(direction[:, None] * difference, axis=0)**2)
                    expected = direction @ gram @ direction
                    evidence.check(name + ':positive_norm:' + str(index) + ':' + str(direction_index),
                                   abs(direct - expected) <= 2e-13 * max(abs(expected), 1e-300))
                variations = finite_difference_curvatures(raw)
                evidence.check(name + ':real_velocity_variations:' + str(index), np.max(variations[:, 3]) <= 1e-40)
                finite_count += len(variations)
                errors.append(float(np.max(variations[:, 3])))
                output = evidence.output / (name + '-probe' + str(index) + '-curvatures.npz')
                np.savez_compressed(output, variations=variations, defect_gram=gram, label=raw['label'])
                evidence.own(output, 'outputs')
            evidence.report['cases'].append(dict(branch=case['branch'], level=case['level'], fresh_probes=len(case['probe_paths'])))
            evidence.save()
        cutoff = datetime.fromisoformat(report['protected_since']).timestamp()
        protected = evidence.root.parent / 'formalization-workbench'
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= cutoff]
        evidence.check('protected_workbench_mtime_unchanged', not changed, changed)
        evidence.check('no_bytecode_cache', not (evidence.root / 'scripts/__pycache__').exists())
        for script in ['derive_annular_support_map_constraints_20260927.py', 'validate_annular_support_map_constraints_20260927.py']:
            path = evidence.root / 'scripts' / script
            compile(path.read_text(encoding='utf-8'), str(path), 'exec')
            evidence.check('compile:' + script, True)
        evidence.report.update(material_layer_replays=replay_count, real_velocity_variations=finite_count,
            maximum_decimal_curvature_error=max(errors), seconds=perf_counter() - started,
            new_nonlinear_solves=0, support_acceleration_solved=False, github_action=False,
            note='Fresh field traces, nodal Gram actions and real 64-digit velocity differences; shared immutable reconstruction helpers.')
        completion = evidence.output / 'completion.txt'
        with completion.open('w', encoding='utf-8') as handle, contextlib.redirect_stdout(handle):
            evidence.complete()
        evidence.own(completion, 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=evidence.report['seconds'],
                             real_velocity_variations=finite_count, maximum_error=max(errors))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
