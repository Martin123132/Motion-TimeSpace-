from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_native_precision_context_20260929 import inherited_sources, restore_native
from annular_decimal_label_rule_20260929 import decimal_label_rule, exact_weighted_moment
from annular_physical_native_kernel_20260928 import decimals
from decimal import Decimal, localcontext
from time import perf_counter
import argparse
import csv
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--level', choices=['fine', 'third'], default='fine')
    parser.add_argument('--branch', choices=['MTS-primary', 'reference-reference'], default='MTS-primary')
    parser.add_argument('--modes', nargs='+', choices=['legacy', 'decimal_geometry', 'decimal_metric', 'decimal_all'], default=['legacy', 'decimal_geometry', 'decimal_all'])
    parser.add_argument('--rule', choices=['binary64', 'decimal'], default='binary64')
    parser.add_argument('--orders', nargs='+', type=int, default=[48, 64])
    parser.add_argument('--max-seconds', type=float, default=3600)
    args = parser.parse_args()
    if args.orders != sorted(set(args.orders)) or min(args.orders) < 8:
        parser.error('Use distinct increasing quadrature orders of at least eight')
    if args.rule == 'decimal' and args.modes != ['decimal_all']:
        parser.error('An extended-precision quadrature requires decimal_all evaluation')
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False, numerical_acceptance_passed=False,
            github_action=False, subagents_used=False, original_workbench_write=False,
            reaction_recomputed=False, action_coefficients_changed=False, configuration=vars(args),
            inverse_tolerance=2e-11, paired_rule_difference_is_rigorous_bound=False)
        evidence.own(evidence.root / 'DERIVATION-20260929-native-force-precision-integration.md')
        probe_path = evidence.output.parent / 'annular-native-position-arithmetic-probe-attempt01/status.json'
        probe = json.loads(probe_path.read_text())
        evidence.own(probe_path)
        evidence.check('independent_derivative_probe_complete', probe['state'] == 'complete' and all(row['passed'] for row in probe['checks']))
        for relative, digest in probe['inputs'].items():
            if relative.startswith('scripts') and ('precision' in relative or 'reaction_20260929' in relative):
                path = evidence.root / relative
                evidence.check('unchanged_probe_source:' + relative, hashlib.sha256(path.read_bytes()).hexdigest() == digest)
                evidence.own(path)
        digests = inherited_sources(evidence)
        rows, previous, previous_decimal = [], {}, {}
        with localcontext() as context:
            context.prec = 70
            setup = restore_native(evidence, digests, args.branch, args.level, deadline)
            engine, inverse = setup['precision'], setup['inverse']
            norm = lambda value: float(np.max(np.abs(inverse.solve(np.asarray(value, float).ravel()))))
            for order in args.orders:
                if args.rule == 'decimal':
                    labels, weights = decimal_label_rule(order)
                    for power in range(min(15, 2 * order - 2)):
                        error = abs(sum(weight * label ** power for label, weight in zip(labels, weights)) - exact_weighted_moment(power))
                        evidence.check('Gauss_moment_' + str(order) + '_' + str(power), error < Decimal('1e-55'), str(error))
                else:
                    labels, weights = np.polynomial.legendre.leggauss(order)
                    labels, weights = labels / 2, weights / 2
                    weights *= 6 * (labels + .5) * (.5 - labels)
                    labels, weights = decimals(labels), decimals(weights)
                for mode in args.modes:
                    integrated = np.full(setup['loads'].rates.shape, Decimal(0), dtype=object)
                    ordinary = np.zeros_like(setup['loads'].rates)
                    node_forces, cardinals = [], []
                    for index, (label, weight) in enumerate(zip(labels, weights)):
                        if perf_counter() > deadline:
                            raise RuntimeError('Safe native arithmetic integral boundary')
                        force, unused, cardinal = engine.evaluate(label, mode)
                        integrated += weight * np.outer(cardinal, force)
                        ordinary += float(weight) * np.outer(np.asarray(cardinal, float), np.asarray(force, float))
                        node_forces.append(force)
                        cardinals.append(cardinal)
                        if index % 16 == 15:
                            evidence.report['progress'] = dict(mode=mode, order=order, nodes=index + 1,
                                total=order, seconds=perf_counter() - started)
                            evidence.save()
                            print(json.dumps(evidence.report['progress']), flush=True)
                    rounded = np.asarray(integrated, float)
                    evidence.check(mode + '-' + str(order) + ':finite_integral', np.all(np.isfinite(rounded)))
                    if not setup['native'].enabled:
                        evidence.check(mode + '-' + str(order) + ':reference_native_zero', not np.any(rounded))
                    baseline = setup['original'][64]['force_native']
                    last = previous.get(mode)
                    delta_exact = None if last is None else norm(integrated - previous_decimal[mode])
                    successive = None if last is None else norm(rounded - last)
                    row = dict(branch=args.branch, level=args.level, mode=mode, rule=args.rule, order=order,
                        maximum_force=float(np.max(np.abs(rounded))), difference_from_original64=norm(rounded - baseline),
                        ordinary_accumulation_shift=norm(ordinary - rounded),
                        successive_inverse=successive, successive_decimal_difference_inverse=delta_exact,
                        final_rounding_inverse=norm(integrated - decimals(rounded)),
                        successive_within_gate=None if successive is None else successive <= 2e-11,
                        seconds=perf_counter() - started, valid_for_claim=False)
                    if mode == 'legacy' and order in setup['original']:
                        replay = norm(ordinary - setup['original'][order]['force_native'])
                        evidence.check('legacy_integral_replay_' + str(order), replay <= 2e-11, replay)
                        row['legacy_replay_inverse'] = replay
                    path = evidence.output / (mode + '-' + str(order) + '.npz')
                    np.savez_compressed(path, force_native=rounded, force_decimal=integrated.astype(str),
                        ordinary=ordinary, labels=labels.astype(str), weights=weights.astype(str),
                        node_forces=np.asarray(node_forces).astype(str), cardinals=np.asarray(cardinals).astype(str))
                    evidence.own(path, 'outputs')
                    evidence.report['cases'].append(dict(summary=row, path=str(path.relative_to(evidence.root))))
                    rows.append(row)
                    previous[mode], previous_decimal[mode] = rounded, integrated
                    evidence.save()
                    print(json.dumps(row), flush=True)
        fields = list(dict.fromkeys(key for row in rows for key in row))
        path = evidence.output / 'precision-integrals.csv'
        with path.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started,
            all_recorded_successive_rules_within_gate=all(row['successive_within_gate'] for row in rows if row['successive_within_gate'] is not None),
            candidate_only=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
