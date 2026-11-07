from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_radial_Ward_moments_20260921 import test_functions
from decimal import Decimal, localcontext
from fractions import Fraction
from bisect import bisect_right
from datetime import datetime
from time import perf_counter
import argparse
import contextlib
import csv
import hashlib
import json
import numpy as np
import sympy as sp


ZERO = Decimal(0)


def archive(path):
    with np.load(path, allow_pickle=False) as saved:
        return {key: saved[key].copy() for key in saved.files}


def decimal_values(values):
    return np.array([Decimal(str(value)) for value in np.asarray(values).ravel()], dtype=object).reshape(np.shape(values))


def maximum(values):
    return max(map(abs, np.asarray(values).ravel()), default=ZERO)


def packed_apply(indices, values, vector):
    answer = np.full((len(indices), vector.shape[1]), ZERO, dtype=object)
    for offset in range(3):
        mask = indices[:, offset] >= 0
        answer[mask] += values[mask, offset, None] * vector[indices[mask, offset]]
    return answer


def current_chain_proof(evidence):
    time = sp.symbols('t', real=True)
    beta = sp.Function('beta')(time)
    old = sp.Matrix([sp.Function('q1')(time), sp.Function('q2')(time)])
    new = sp.Matrix([sp.Function('Q1')(time), sp.Function('Q2')(time)])
    mass = sp.diag(2 + beta**2, 3 + beta**2)
    stiffness = sp.Matrix([[4 + beta**2, 1], [1, 5 + beta**2]])
    pullback = sp.Matrix([[1, beta], [0, 1]])
    inverse = pullback.inv()
    lagrangian = (old.diff(time).T * mass * old.diff(time) - old.T * stiffness * old)[0] / 2
    euler = sp.Matrix([sp.diff(lagrangian, field) - sp.diff(sp.diff(lagrangian, field.diff(time)), time) for field in old])
    original_current = sp.diff(lagrangian, beta)
    substituted = inverse * new
    replacements = {old[index].diff(time, order): substituted[index].diff(time, order)
                    for index in range(2) for order in [0, 1, 2]}
    transformed = lagrangian.subs(replacements, simultaneous=True)
    transformed_current = sp.diff(transformed, beta) - sp.diff(sp.diff(transformed, beta.diff(time)), time)
    change = -(inverse * pullback.diff(beta) * substituted)
    expected = original_current.subs(replacements, simultaneous=True) + (euler.subs(replacements, simultaneous=True).T * change)[0]
    evidence.check('symbolic:complete_metric_current_chain', sp.simplify(transformed_current - expected) == 0)
    connection = pullback.diff(time) * inverse
    evidence.check('symbolic:time_connection', sp.simplify(new.diff(time) - connection * new - pullback * substituted.diff(time)) == sp.zeros(2, 1))
    wrong_velocity = inverse * new.diff(time)
    wrong = (wrong_velocity.T * mass * wrong_velocity - substituted.T * stiffness * substituted)[0] / 2
    evidence.check('negative_control:omitted_connection_fails_chain', sp.simplify(sp.diff(wrong, beta) - expected) != 0)
    diagonal = sp.diag(*sp.symbols('w0:3', positive=True))
    derivative = sp.diag(*sp.symbols('dw0:3'))
    factor = sp.Matrix([[1, -2], [3, 1], [-1, 4]])
    generator = sp.Matrix(2, 2, sp.symbols('generator0:4'))
    factor_rate = -factor * generator - diagonal.inv() * derivative * factor / 2
    stiffness = factor.T * diagonal * factor
    actual_rate = factor_rate.T * diagonal * factor + factor.T * diagonal * factor_rate + factor.T * derivative * factor
    evidence.check('symbolic:weighted_factor_transport', sp.simplify(actual_rate + generator.T * stiffness + stiffness * generator) == sp.zeros(2, 2))
    evidence.report['chain_proof'] = dict(metric_parameter='arbitrary beta(t), noncommuting shear pullback',
        current='J_new=J_old-E^T P^-1 P_beta u', connection_required=True,
        validity='Differentiable pullback charts and retained temporal boundary terms; not a new shift completion.')


def fresh_rows(mesh, speed, amount):
    def rational(value):
        value = Fraction(value)
        return Decimal(value.numerator) / Decimal(value.denominator)
    edges, nodes = [list(map(rational, mesh[key])) for key in ['edges', 'nodes']]
    rows, derivatives = [], []
    for node, velocity in zip(nodes, speed):
        point = node + amount * velocity
        cell = max(0, min(len(edges) - 2, bisect_right(edges, point) - 1))
        width = edges[cell + 1] - edges[cell]
        local = (point - edges[cell]) / width
        coefficients = [2 * local**2 - 3 * local + 1, 4 * local - 4 * local**2, 2 * local**2 - local]
        gradients = [(4 * local - 3) * velocity / width, (4 - 8 * local) * velocity / width, (4 * local - 1) * velocity / width]
        rows.append({index: value for index, value in zip(mesh['elements'][cell], coefficients) if index >= 0})
        derivatives.append({index: value for index, value in zip(mesh['elements'][cell], gradients) if index >= 0})
    return rows, derivatives


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--run', default='annular-geometric-pullback-attempt02')
    parser.add_argument('--label', default='annular-geometric-pullback-validation-attempt01')
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + 3600
    try:
        parent_path = evidence.output.parent / args.run / 'status.json'
        parent = json.loads(parent_path.read_text())
        evidence.check('main_complete', parent['state'] == 'complete' and all(row['passed'] for row in parent['checks']))
        evidence.own(parent_path)
        digests = {}
        for category in ['inputs', 'outputs']:
            for path, digest in parent[category].items():
                if path in digests and digests[path] != digest:
                    raise RuntimeError('Hash conflict')
                digests[path] = digest
        for relative, digest in digests.items():
            path = evidence.root / relative
            evidence.check('hash:' + relative, path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() == digest)
            evidence.own(path)
        current_chain_proof(evidence)
        tables = {}
        for filename, count in [('one-sided-shape.csv', 12), ('finite-pullback.csv', 216)]:
            with (parent_path.parent / filename).open(newline='', encoding='utf-8') as handle:
                tables[filename] = list(csv.DictReader(handle))
            rows = tables[filename]
            evidence.check(filename + ':schema', len(rows) == count and all(None not in row and None not in row.values() for row in rows))
        replays, raw_replays = 0, 0
        errors = []
        with localcontext() as context:
            context.prec = 80
            for case in parent['cases']:
                name = case['branch'] + '-' + case['level']
                print(json.dumps(dict(stage=name, seconds=perf_counter() - started)), flush=True)
                for path in case['material_paths']:
                    saved = archive(evidence.root / path)
                    count = len(saved['labels'])
                    labels, weights = np.polynomial.legendre.leggauss(count)
                    labels, weights = labels / 2, weights / 2
                    weights *= 6 * (labels + .5) * (.5 - labels)
                    evidence.check(name + ':quadrature:' + str(count), np.array_equal(labels, saved['labels']) and np.array_equal(weights, saved['weights']))
                    average = np.einsum('l,ltsc->tsc', weights, saved['responses'])
                    evidence.check(name + ':mean:' + str(count), np.max(abs(average - saved['average'])) <= 2e-18)
                    evidence.check(name + ':cancellation:' + str(count), np.max(abs(saved['responses'][:, :, :, :3].sum(axis=3))) <= 2e-18)
                    replays += count
                for test in range(3):
                    row = next(row for row in tables['one-sided-shape.csv'] if row['branch'] == case['branch'] and row['level'] == case['level'] and int(row['test']) == test)
                    plus, minus = average[test, :, :2].sum(axis=1)
                    for key, value in [('shape_plus', plus), ('shape_minus', minus), ('centered_shape', (plus + minus) / 2), ('shape_jump', plus - minus)]:
                        evidence.check(name + ':CSV:' + str(test) + ':' + key, abs(float(row[key]) - value) <= 2e-18)
                loads, action, sources = restore_case(evidence, digests, case['branch'], case['level'], deadline)
                evidence.check(name + ':same_sources', sources == case['sources'])
                for path in case['finite_paths']:
                    raw = archive(evidence.root / path)
                    row = next(row for row in parent['finite_cases'] if row.get('raw_path') == path)
                    old, moved, recovered, speed = [decimal_values(raw[key]) for key in ['old_fields', 'moved_fields', 'recovered', 'speed']]
                    amount = Decimal(str(raw['step']))
                    entries, derivative_entries = decimal_values(raw['entries']), decimal_values(raw['derivative_entries'])
                    fresh, fresh_derivative = fresh_rows(action.mesh, speed, amount)
                    entry_error = ZERO
                    for key, indices, coefficients, expected_rows in [('value', raw['indices'], entries, fresh),
                                                                    ('derivative', raw['derivative_indices'], derivative_entries, fresh_derivative)]:
                        for index, expected in enumerate(expected_rows):
                            stored = {int(column): value for column, value in zip(indices[index], coefficients[index]) if column >= 0}
                            scale = max(maximum(list(expected.values())), Decimal(1))
                            local_error = max((abs(stored.get(column, ZERO) - expected.get(column, ZERO)) for column in set(stored) | set(expected)), default=ZERO)
                            entry_error = max(entry_error, local_error / scale)
                    field_scale = maximum(old)
                    matrix_error = maximum(packed_apply(raw['indices'], entries, old) - moved) / field_scale
                    residual_error = maximum(packed_apply(raw['indices'], entries, recovered) - moved) / field_scale
                    direction, curvature = decimal_values(raw['expected_direction']), decimal_values(raw['curvature'])
                    polynomial_error = maximum(moved - old - amount * direction - amount**2 * curvature) / field_scale
                    evidence.check(path + ':fresh_rows_and_residuals', max(entry_error, matrix_error, residual_error, polynomial_error) <= Decimal('1e-40'),
                                   float(max(entry_error, matrix_error, residual_error, polynomial_error)))
                    cardinal = np.asarray(action.cardinal(float(raw['label']))).ravel()
                    cardinal_decimal = np.array([Decimal.from_float(float(value)) for value in cardinal], dtype=object)
                    expected_old = np.column_stack([loads.coordinates[:, :-1].T @ cardinal_decimal,
                        np.array([[Decimal.from_float(float(value)) for value in column] for column in loads.rates[:, :-1].T], dtype=object) @ cardinal_decimal])
                    evidence.check(path + ':archived_fields', maximum(old - expected_old) <= Decimal('1e-40') * field_scale)
                    source = float(cardinal @ action.source)
                    geometry = action.geometry(action.knots, source, float(raw['label']))
                    test = row['test']
                    eta = test_functions(geometry['radius'])[0][test] - test_functions(source)[0][test] * geometry['displacement']
                    strain = test_functions(geometry['radius'])[1][test] - test_functions(source)[0][test] * geometry['jacobian_source'] / geometry['jacobian']
                    endpoints = action.geometry(np.array([float(action.edges[0]), float(action.edges[-1])]), source, float(raw['label']))['radius']
                    boundary_values = test_functions(endpoints)[0][test]
                    boundary_value = np.where(geometry['radius'] < source, boundary_values[0], boundary_values[1])
                    eta -= boundary_value * (1 - geometry['displacement'])
                    strain += boundary_value * geometry['jacobian_source'] / geometry['jacobian']
                    radius = geometry['radius'] + float(amount) * eta
                    values = action.solver.values(action.solution, radius)[0]
                    gamma = radius**2 * np.exp(values[1]) * np.sqrt(1 - 2 * values[0] / radius) / (geometry['jacobian'] * (1 + float(amount) * strain))
                    fresh_weights = np.asarray(action.sampling @ gamma).ravel()
                    weights, new_weights = decimal_values(raw['weights']), decimal_values(raw['new_weights'])
                    evidence.check(path + ':fresh_metric_weights', len(weights) == 0 or
                        np.max(abs(fresh_weights - np.asarray(new_weights, float))) <= 2e-13 * np.max(abs(fresh_weights)))
                    image = action.factor.apply(old)
                    transported = decimal_values(raw['transported_image'])
                    scales = np.array([(before / after).sqrt() for before, after in zip(weights, new_weights)], dtype=object)
                    expected_image = action.factor.apply(recovered) * scales[:, None]
                    image_scale = max(maximum(image), Decimal('1e-100'))
                    evidence.check(path + ':fresh_Gram_action', maximum(image - decimal_values(raw['old_image'])) <= Decimal('1e-40') * image_scale
                                   and maximum(expected_image - transported) <= Decimal('1e-40') * image_scale)
                    for field in range(2):
                        before = sum(weights * image[:, field]**2 / 2, ZERO)
                        after = sum(new_weights * transported[:, field]**2 / 2, ZERO)
                        error = abs(after - before) / max(abs(before), Decimal('1e-100'))
                        evidence.check(path + ':energy:' + str(field), error <= Decimal('1e-40'), float(error))
                        errors.append(float(error))
                    raw_replays += 1
                case_rows = [row for row in parent['finite_cases'] if row['branch'] == case['branch'] and row['level'] == case['level']]
                for label_index in [0, 31, 63]:
                    for test in range(3):
                        for sign in [-1, 1]:
                            group = sorted([row for row in case_rows if row['label_index'] == label_index and row['test'] == test and row['sign'] == sign], key=lambda row: row['resolution'])
                            evidence.check(name + ':steps:' + str(label_index) + ':' + str(test) + ':' + str(sign), len(group) == 3
                                and abs(group[0]['step'] / group[2]['step'] - 4) < 1e-14
                                and abs(group[0]['derivative_error'] / group[2]['derivative_error'] - 4) < 1e-9)
                evidence.report['cases'].append(dict(branch=case['branch'], level=case['level'], raw_replays=len(case['finite_paths'])))
                evidence.save()
        cutoff = datetime.fromisoformat(parent['protected_since']).timestamp()
        protected = evidence.root.parent / 'formalization-workbench'
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= cutoff]
        evidence.check('protected_workbench_mtime', not changed, changed)
        evidence.check('no_bytecode_cache', not (evidence.root / 'scripts/__pycache__').exists())
        for filename in ['annular_geometric_pullback_20260927.py', 'derive_annular_geometric_pullback_v2_20260927.py', 'validate_annular_geometric_pullback_20260927.py']:
            path = evidence.root / 'scripts' / filename
            compile(path.read_text(), str(path), 'exec')
            evidence.check('compile:' + filename, True)
        evidence.report.update(seconds=perf_counter() - started, material_replays=replays, raw_replays=raw_replays,
            maximum_energy_error=max(errors), current_chain_verified=True, current_physically_modified=False)
        completion = evidence.output / 'completion.txt'
        with completion.open('w', encoding='utf-8') as handle, contextlib.redirect_stdout(handle):
            evidence.complete()
        evidence.own(completion, 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=evidence.report['seconds'],
                             material_replays=replays, raw_replays=raw_replays, maximum_energy_error=max(errors))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
