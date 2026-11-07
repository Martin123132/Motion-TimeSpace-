from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_native_precision_context_20260929 import inherited_sources, restore_native
from annular_native_tangent_precision_repair_20260929 import repair_engine
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
    parser.add_argument('--label', default='annular-native-tangent-precision-repair-attempt01')
    parser.add_argument('--max-seconds', type=float, default=3600)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False, valid_for_physics_claim=False,
            github_action=False, subagents_used=False, original_workbench_write=False,
            changed_terms=['field-direction interpolation arithmetic', 'edge-direction interpolation arithmetic', 'sum accumulation arithmetic'],
            background_packet_unchanged=True, cardinal_and_Gauss_rule_unchanged=True,
            native_pair_tolerance=2e-11, live_reaction_recomputed=False)
        evidence.own(evidence.root / 'DERIVATION-20260929-native-tangent-rounding-repair.md')
        channel_path = evidence.output.parent / 'annular-native-rounding-channels-attempt01/status.json'
        channel = json.loads(channel_path.read_text())
        evidence.own(channel_path)
        evidence.check('rounding_channels_complete', channel['state'] == 'complete' and len(channel['cases']) == 6)
        for relative, digest in channel['inputs'].items():
            if 'native_position_precision' in relative or 'native_precision_context' in relative:
                path = evidence.root / relative
                evidence.check('unchanged_derivative_source:' + relative, hashlib.sha256(path.read_bytes()).hexdigest() == digest)
                evidence.own(path)
        digests = inherited_sources(evidence)
        rows, pairs = [], []
        with localcontext() as context:
            context.prec = 70
            for level in ['fine', 'third']:
                reference = restore_native(evidence, digests, 'reference-reference', level, deadline)
                reference_engine = repair_engine(reference['precision'])
                for label in [-.313, .017, .277]:
                    force, base, unused = reference_engine.evaluate(label, 'decimal_tangents')
                    evidence.check('reference-' + level + '-' + str(label) + ':native_disabled', not np.any(force) and not np.any(base))
                del reference, reference_engine
                setup = restore_native(evidence, digests, 'MTS-primary', level, deadline)
                engine, inverse = repair_engine(setup['precision']), setup['inverse']
                norm = lambda value: float(np.max(np.abs(inverse.solve(np.asarray(value, float).ravel()))))
                previous, previous_decimal = None, None
                for order in [48, 64, 96]:
                    labels, weights = np.polynomial.legendre.leggauss(order)
                    labels, weights = labels / 2, weights / 2
                    weights *= 6 * (labels + .5) * (.5 - labels)
                    integral = np.full(setup['loads'].rates.shape, Decimal(0), dtype=object)
                    ordinary = np.zeros_like(setup['loads'].rates)
                    nodes, cardinals = [], []
                    for index, (label, weight) in enumerate(zip(labels, weights)):
                        if perf_counter() > deadline:
                            raise RuntimeError('Safe native tangent repair boundary')
                        force, unused, cardinal = engine.evaluate(label, 'decimal_tangents')
                        integral += Decimal.from_float(float(weight)) * np.outer(cardinal, force)
                        ordinary += weight * np.outer(np.asarray(cardinal, float), np.asarray(force, float))
                        nodes.append(force)
                        cardinals.append(cardinal)
                        if index % 16 == 15:
                            evidence.report['progress'] = dict(level=level, order=order, nodes=index + 1, seconds=perf_counter() - started)
                            evidence.save()
                            print(json.dumps(evidence.report['progress']), flush=True)
                    result = np.asarray(integral, float)
                    successive = None if previous is None else norm(result - previous)
                    evidence.check(level + '-' + str(order) + ':finite_integral', np.all(np.isfinite(result)))
                    row = dict(branch='MTS-primary', level=level, order=order,
                        maximum_force=float(np.max(np.abs(result))),
                        change_from_legacy64_inverse=norm(result - setup['original'][64]['force_native']),
                        successive_inverse=successive,
                        successive_decimal_inverse=None if previous is None else norm(integral - previous_decimal),
                        ordinary_accumulation_inverse=norm(ordinary - result),
                        native_pair_passed=None if previous is None else successive <= 2e-11,
                        seconds=perf_counter() - started, valid_for_claim=False)
                    if previous is not None:
                        pairs.append(dict(level=level, order=order, passed=successive <= 2e-11, error=successive))
                    path = evidence.output / (level + '-native-' + str(order) + '.npz')
                    np.savez_compressed(path, force_native=result, force_decimal=integral.astype(str), ordinary=ordinary,
                        labels=labels, weights=weights, node_forces=np.asarray(nodes).astype(str), cardinals=np.asarray(cardinals).astype(str))
                    evidence.own(path, 'outputs')
                    evidence.report['cases'].append(dict(summary=row, path=str(path.relative_to(evidence.root))))
                    rows.append(row)
                    evidence.save()
                    print(json.dumps(row), flush=True)
                    previous, previous_decimal = result, integral
        path = evidence.output / 'native-tangent-repair.csv'
        with path.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report.update(native_quadrature_checks=pairs,
            all_native_pairs_passed=len(pairs) == 4 and all(row['passed'] for row in pairs),
            seconds=perf_counter() - started, reference_zero_checks=6,
            unchanged_wave_force_gate_still_outstanding=True)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
