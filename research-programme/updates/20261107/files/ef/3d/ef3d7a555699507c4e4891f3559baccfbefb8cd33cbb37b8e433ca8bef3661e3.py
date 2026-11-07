from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_native_precision_context_20260929 import inherited_sources, restore_native
from annular_native_position_precision_20260929 import Directional, chebyshev_value, chebyshev_derivative, metric_coefficients
from annular_position_reaction_20260929 import native_position_force
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import csv
import json
import mpmath as mp
import numpy as np


def algebra_checks(evidence):
    with localcontext() as context:
        context.prec = 70
        trial = Directional(Decimal('1.23'), Decimal('0.17'))
        test = ((trial ** 3 + 2) / trial.sqrt())
        expected = Decimal(3) * trial.value ** 2 * trial.tangent / trial.value.sqrt()
        expected -= (trial.value ** 3 + 2) * trial.tangent / (2 * trial.value ** Decimal('1.5'))
        evidence.check('dual_product_quotient_sqrt', abs(test.tangent - expected) < Decimal('1e-65'))
        coefficients = list(map(Decimal, ['0.1', '-0.7', '0.13', '0.002']))
        coordinate = Decimal('0.321')
        evaluated = chebyshev_value(coefficients, Directional(coordinate, Decimal(1)))
        differentiated = chebyshev_value(chebyshev_derivative(coefficients), coordinate)
        evidence.check('clenshaw_derivative_independent_dual', abs(evaluated.tangent - differentiated) < Decimal('1e-65'))
        with mp.workdps(65):
            radius, movement = mp.mpf('5.23'), mp.mpf('0.013')
            mass = lambda value: mp.mpf('0.8') + mp.mpf('.002') * value ** 2
            lapse = lambda value: mp.mpf('-.11') + mp.mpf('.003') * value ** 2
            mass_change = lambda value: mp.mpf('.004') + mp.mpf('.0002') * value
            lapse_change = lambda value: mp.mpf('-.002') + mp.mpf('.0003') * value
            beta = lambda value, amount: value ** 2 * mp.exp(lapse(value) + amount * lapse_change(value)) * mp.sqrt(1 - 2 * (mass(value) + amount * mass_change(value)) / value)
            beta_r = lambda value, amount: mp.diff(lambda point: beta(point, amount), value)
            expected = [beta(radius, 0), beta_r(radius, 0),
                mp.diff(lambda amount: beta(radius + amount * movement, amount), 0),
                mp.diff(lambda amount: beta_r(radius + amount * movement, amount), 0)]
            convert = lambda value: Decimal(str(value))
            observed = metric_coefficients(convert(radius), list(map(convert, [mass(radius), lapse(radius)])),
                list(map(convert, [mp.diff(mass, radius), mp.diff(lapse, radius)])),
                list(map(convert, [mp.diff(mass, radius, 2), mp.diff(lapse, radius, 2)])), convert(movement),
                list(map(convert, [mass_change(radius), lapse_change(radius)])),
                list(map(convert, [mp.diff(mass_change, radius), mp.diff(lapse_change, radius)])))
            for index in range(4):
                error = abs(observed[index] - convert(expected[index]))
                evidence.check('metric_chain_rule_' + str(index), error < Decimal('1e-55'), str(error))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='annular-native-position-arithmetic-probe-attempt01')
    parser.add_argument('--max-seconds', type=float, default=1800)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False, numerical_acceptance_passed=False,
            github_action=False, subagents_used=False, original_workbench_write=False,
            integral_convergence_tested=False, action_coefficients_changed=False)
        evidence.own(evidence.root / 'DERIVATION-20260929-native-force-directional-arithmetic.md')
        algebra_checks(evidence)
        digests = inherited_sources(evidence)
        rows = []
        with localcontext() as context:
            context.prec = 70
            for branch, level in [('reference-reference', 'fine'), ('MTS-primary', 'fine'), ('MTS-primary', 'third')]:
                setup = restore_native(evidence, digests, branch, level, deadline)
                engine, inverse = setup['precision'], setup['inverse']
                norm = lambda value: float(np.max(np.abs(inverse.solve(np.asarray(value, float).ravel()))))
                for label in [-.313, .017, .277]:
                    if perf_counter() > deadline:
                        raise RuntimeError('Safe arithmetic probe boundary')
                    old, halving, base = native_position_force(setup['native'], setup['loads'], setup['action'], label,
                        engine.field_direction, engine.source_direction, engine.edge_vertices, engine.position)
                    results = {mode: engine.evaluate(label, mode) for mode in ['legacy', 'decimal_geometry', 'decimal_metric', 'decimal_all']}
                    legacy, unused, cardinal = results['legacy']
                    replay = norm(np.outer(np.asarray(cardinal, float), np.asarray(legacy, float) - old))
                    evidence.check(branch + '-' + level + ':' + str(label) + ':dual_finite_difference_replay', replay <= 2e-11, replay)
                    if not setup['native'].enabled:
                        evidence.check('reference_native_zero:' + str(label), all(not np.any(result[0]) for result in results.values()))
                    for mode, (force, baseline, cardinal) in results.items():
                        represented = np.outer(cardinal, force)
                        previous = np.outer(results['legacy'][2], results['legacy'][0])
                        row = dict(branch=branch, level=level, label=label, mode=mode,
                            pointwise_inverse_shift=norm(represented - previous),
                            maximum_force_shift=float(np.max(np.abs(force - legacy))),
                            dual_replay_inverse=replay, seconds=perf_counter() - started, valid_for_claim=False)
                        rows.append(row)
                        path = evidence.output / (branch + '-' + level + '-' + str(label) + '-' + mode + '.npz')
                        np.savez_compressed(path, force=force.astype(str), base=baseline.astype(str), cardinal=cardinal.astype(str))
                        evidence.own(path, 'outputs')
                        evidence.report['cases'].append(row)
                    evidence.report['progress'] = dict(branch=branch, level=level, label=label, seconds=perf_counter() - started)
                    evidence.save()
                    print(json.dumps(evidence.report['progress']), flush=True)
        path = evidence.output / 'arithmetic-probes.csv'
        with path.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report['seconds'] = perf_counter() - started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
