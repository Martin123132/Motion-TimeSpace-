from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_directional_coupled_Euler_20260928 import CHANNELS, symbolic_checks, restore_flow, trial_directions, layer, finite_wave_derivatives
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_physical_native_kernel_20260928 import NativeKernel
from annular_radial_Ward_moments_20260921 import prepare
from decimal import localcontext
from time import perf_counter
import argparse
import contextlib
import csv
import hashlib
import json
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='annular-directional-coupled-Euler-attempt01')
    parser.add_argument('--max-seconds', type=float, default=7200)
    args = parser.parse_args()
    evidence = EvidenceRun(args.label, __file__)
    started, deadline = perf_counter(), perf_counter() + args.max_seconds
    try:
        evidence.report.update(channels=CHANNELS, test_index=1, new_nonlinear_solves=0, github_action=False,
            subagents_used=False, protected_since='2026-09-28T00:07:05+00:00',
            trial_space='15-cardinal material interpolation of pinned edge-affine direction and continuous averaged-trace P2 field direction',
            symbolic_scope='Finite candidate action directional Euler identity; archived coupled acceleration, not new evolution')
        evidence.own(evidence.root / 'DERIVATION-20260928-directional-coupled-Euler-test.md')
        seal_path = evidence.output.parent / 'annular-native-time-current-final-integrity-20260928.json'
        seal = json.loads(seal_path.read_text())
        evidence.own(seal_path)
        evidence.check('previous_final_seal_complete', seal['state'] == 'complete')
        digests, bad = {}, []
        for relative, digest in seal['hashes'].items():
            if relative == 'CURRENT_LOCAL_RESUME.md':
                continue
            path = evidence.root / relative
            if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != digest:
                bad.append(relative)
            else:
                digests[str(path.relative_to(evidence.root))] = digest
                evidence.own(path)
        evidence.check('all_prior_scientific_hashes', not bad, dict(count=len(digests), mismatches=bad))
        symbolic_checks(evidence)

        def save(name, **arrays):
            path = evidence.output / (name + '.npz')
            np.savez_compressed(path, **arrays)
            evidence.own(path, 'outputs')
            return str(path.relative_to(evidence.root))

        def check_close(name, error, tolerance):
            evidence.check(name, bool(np.isfinite(error) and abs(error) <= tolerance), dict(error=float(error), tolerance=float(tolerance)))

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter() - started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)
            if perf_counter() > deadline:
                raise RuntimeError('Safe completed-layer runtime boundary')

        summaries, finite_rows, quad_rows = [], [], []
        with localcontext() as context:
            context.prec = 80
            for branch in ['reference-reference', 'MTS-primary']:
                for level in ['fine', 'third']:
                    name = branch + '-' + level
                    progress(name + ':restore')
                    loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
                    packet = load_owned(evidence, digests, evidence.root / sources['packet'])
                    engine = NativeKernel(packet['mesh'], packet['gram_support'], branch == 'MTS-primary')
                    flow, tangent, centre = restore_flow(evidence, digests, action, sources, level)
                    acceleration = flow['accelerations'][-1]
                    polynomial, unused = prepare(action, loads, acceleration)
                    edge_vertices, field_vertices = trial_directions(engine, loads, action)
                    evidence.check(name + ':pinned_cardinal_directions', np.max(abs(edge_vertices[:, [0, engine.anchor, -1]])) == 0)
                    direction_path = save(name + '-directions', edge_vertices=edge_vertices, field_vertices=field_vertices)
                    paths, probes, means = [], [], []
                    maximum_identity = 0.
                    for order in [48, 64]:
                        labels, weights = np.polynomial.legendre.leggauss(order)
                        labels, weights = labels / 2, weights / 2
                        weights *= 6 * (labels + .5) * (.5 - labels)
                        rows = []
                        for index, label in enumerate(labels):
                            if index % 16 == 0:
                                progress(name + ':material' + str(order) + ':label' + str(index))
                            values, raw, pins = layer(engine, loads, action, tangent, acceleration, polynomial, edge_vertices, field_vertices, label, 12)
                            rows.append(values)
                            named = dict(zip(CHANNELS, values))
                            identity_error = abs(named['wave_direct'] - named['wave_identity'])
                            maximum_identity = max(maximum_identity, identity_error)
                            check_close(name + ':identity:' + str(order) + ':' + str(index), identity_error, 2e-16)
                            check_close(name + ':pins:' + str(order) + ':' + str(index), pins, 2e-15)
                            check_close(name + ':kinetic_split:' + str(order) + ':' + str(index),
                                named['kinetic_defect'] - named['kinetic_label_defect'] - named['kinetic_spatial_defect'] - named['kinetic_cross'],
                                1e-28 + 2e-10 * abs(named['kinetic_defect']))
                            if order == 64 and index in [0, 31, 63]:
                                probe_path = save(name + '-probe' + str(index), **raw, values=values)
                                probes.append(probe_path)
                                for step in [1e-20, 1e-24]:
                                    finite = finite_wave_derivatives(raw, step)
                                    error = finite[-1] - named['wave_direct']
                                    check_close(name + ':finite_action:' + str(index) + ':' + str(step), error, 2e-16)
                                    finite_rows.append(dict(branch=branch, level=level, material_label=float(label), step=step,
                                        position_derivative=finite[0], momentum_derivative=finite[1], direct_euler=finite[2], analytic_euler=named['wave_direct'], difference=error))
                                lower, unused_raw, unused_pins = layer(engine, loads, action, tangent, acceleration, polynomial, edge_vertices, field_vertices, label, 8)
                                error = np.max(abs(lower[:15] - values[:15]))
                                check_close(name + ':spatial_quadrature:' + str(index), error, 2e-16)
                                quad_rows.append(dict(branch=branch, level=level, material_label=float(label), max_channel_change=float(error)))
                        rows = np.array(rows)
                        average = weights @ rows
                        means.append(average)
                        paths.append(save(name + '-material' + str(order), labels=labels, weights=weights, values=rows, average=average, channels=np.array(CHANNELS)))
                        summaries.append(dict(branch=branch, level=level, material_order=order, **dict(zip(CHANNELS, map(float, average)))))
                    material_change = np.max(abs(means[1][:15] - means[0][:15]))
                    check_close(name + ':material_quadrature', material_change, 2e-16)
                    check_close(name + ':solved_field_equation', means[1][CHANNELS.index('solved_field_work')], 2e-16)
                    evidence.report['cases'].append(dict(branch=branch, level=level, sources=sources,
                        flow_path=centre['flow_path'], direction_path=direction_path, material_paths=paths, probe_paths=probes,
                        maximum_identity_error=maximum_identity, material_change=float(material_change)))
                    progress(name + ':saved')
        for filename, rows in [('directional-balance.csv', summaries), ('finite-action-checks.csv', finite_rows), ('spatial-quadrature-checks.csv', quad_rows)]:
            path = evidence.output / filename
            with path.open('w', newline='', encoding='utf-8') as stream:
                writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            evidence.own(path, 'outputs')
        evidence.report.update(seconds=perf_counter() - started, summaries=summaries)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    with contextlib.redirect_stderr(__import__('sys').stdout):
        main()
