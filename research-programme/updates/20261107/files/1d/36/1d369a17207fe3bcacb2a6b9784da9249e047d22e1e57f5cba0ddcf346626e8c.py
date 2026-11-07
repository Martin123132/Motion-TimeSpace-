from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_native_precision_context_20260929 import inherited_sources, restore_native
from annular_native_position_precision_20260929 import native_force_tangent
from decimal import Decimal, localcontext
from time import perf_counter
import csv
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-native-rounding-channels-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter() + 900
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False, valid_for_physics_claim=False,
            github_action=False, subagents_used=False, original_workbench_write=False,
            scope='Exact telescoping decomposition of legacy-to-Decimal geometry arithmetic',
            quadrature_convergence_tested=False)
        evidence.own(evidence.root / 'DERIVATION-20260929-native-force-directional-arithmetic.md')
        digests = inherited_sources(evidence)
        rows = []
        with localcontext() as context:
            context.prec = 70
            for level in ['fine', 'third']:
                setup = restore_native(evidence, digests, 'MTS-primary', level, deadline)
                engine, inverse = setup['precision'], setup['inverse']
                norm = lambda value: float(np.max(np.abs(inverse.solve(np.asarray(value, float).ravel()))))
                for label in [-.313, .017, .277]:
                    if perf_counter() > deadline:
                        raise RuntimeError('Safe rounding-channel boundary')
                    old = engine.packet(label, 'legacy')
                    new = engine.packet(label, 'decimal_geometry')
                    old_force = native_force_tangent(setup['native'], *old)[0]
                    new_force = native_force_tangent(setup['native'], *new)[0]
                    mixed_force = native_force_tangent(setup['native'], old[0], *new[1:])[0]
                    channels = {}
                    for channel, name in enumerate(['field_direction', 'edge_direction', 'beta_direction', 'beta_radial_direction'], start=1):
                        tangent = [np.full_like(array, Decimal(0)) for array in old[1:]]
                        tangent[channel - 1] = new[channel] - old[channel]
                        channels[name] = native_force_tangent(setup['native'], old[0], *tangent)[0]
                    channels['base_packet'] = new_force - mixed_force
                    total = new_force - old_force
                    error = total - sum(channels.values())
                    cardinal = old[0]['cardinal']
                    weighted_norm = lambda value: norm(np.outer(cardinal, value))
                    closure = weighted_norm(error)
                    evidence.check(level + ':' + str(label) + ':signed_channel_closure', closure <= 2e-11, closure)
                    row = dict(level=level, label=label, total_inverse=weighted_norm(total),
                        **{name + '_inverse': weighted_norm(value) for name, value in channels.items()},
                        closure_inverse=closure, seconds=perf_counter() - started, valid_for_claim=False)
                    path = evidence.output / (level + '-' + str(label) + '.npz')
                    np.savez_compressed(path, total=total.astype(str), cardinal=cardinal.astype(str),
                        **{name: value.astype(str) for name, value in channels.items()})
                    evidence.own(path, 'outputs')
                    evidence.report['cases'].append(row)
                    rows.append(row)
                    evidence.save()
                    print(json.dumps(row), flush=True)
        path = evidence.output / 'rounding-channels.csv'
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
