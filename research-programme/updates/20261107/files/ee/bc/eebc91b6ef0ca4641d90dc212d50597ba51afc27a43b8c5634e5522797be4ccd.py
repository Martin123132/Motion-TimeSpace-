from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_acceleration_archive_checks_v2_20261001 import verify_report
from analyze_annular_source_flat_state_20261002 import read_archive
from decimal import Decimal, localcontext
from scipy.sparse import load_npz
from derive_annular_support_map_constraints_20260927 import restore_case
from annular_nested_physical_refinement_v3_20260922 import adapt_owner, restore_refined
from annular_quadratic_core_20261002 import source_geometry
from annular_moving_Legendre_current_20260921 import samples
from time import perf_counter
import csv
import ctypes
import json
import numpy as np


def main():
    kernel = ctypes.windll.kernel32
    kernel.GetCurrentProcess.restype = ctypes.c_void_p
    kernel.SetProcessAffinityMask.argtypes = [ctypes.c_void_p, ctypes.c_size_t]
    if not kernel.SetProcessAffinityMask(kernel.GetCurrentProcess(), 1 << 2):
        raise OSError('Affinity failed')
    evidence = EvidenceRun('annular-live-refinement-time-jet-analysis-attempt01', __file__)
    try:
        base = 'source-intake/navier-stokes/20260914/'
        evidence.own(evidence.root / 'DERIVATION-20261002-live-transmission-time-jet.md')
        evidence.own(evidence.root / 'DERIVATION-20261002-moving-native-transmission-and-third-jets.md')
        reports = {}
        for branch in ['primary', 'reference']:
            reports[branch] = verify_report(evidence, base + 'annular-live-native-transmission-fourth-' + branch + '-attempt03/status.json')
            evidence.check(branch + ':complete_refinement', reports[branch]['state'] == 'complete')
        algebra = verify_report(evidence, base + 'annular-moving-native-transmission-algebra-attempt01/status.json')
        evidence.check('complete_moving_algebra', algebra['state'] == 'complete')
        rows = []
        states = [read_archive(evidence.root / reports[branch]['state_path']) for branch in ['primary', 'reference']]
        evidence.check('matched_initial_data', np.array_equal(states[0]['coordinates'], states[1]['coordinates']) and np.array_equal(states[0]['rates'], states[1]['rates']))
        for branch, report in reports.items():
            for item in report['results']:
                saved = read_archive(evidence.root / item['path'])
                matrix = load_npz(evidence.root / item['matrix_path'])
                vector, force = saved['acceleration'].ravel(), saved['force'].ravel()
                residual = matrix @ vector - force
                relative = float(np.max(abs(residual)) / np.max(abs(force)))
                evidence.check(item['name'] + ':independent_full_Euler_replay', relative < 5e-11, relative)
                with localcontext() as context:
                    context.prec = 75
                    errors = []
                    for index in np.unique(np.linspace(0, len(vector) - 1, 31, dtype=int)):
                        start, end = matrix.indptr[index:index + 2]
                        exact = sum((Decimal.from_float(float(value)) * Decimal.from_float(float(vector[column]))
                            for column, value in zip(matrix.indices[start:end], matrix.data[start:end])), Decimal(0))
                        errors.append(abs(exact - Decimal.from_float(float(force[index]))))
                    error = float(max(errors))
                    evidence.check(item['name'] + ':75digit_selected_rows', error < 5e-11 * np.max(abs(force)), error)
                for name, actual in [('maximum_trace_residual', np.max(abs(saved['trace']))),
                    ('maximum_acceleration', np.max(abs(saved['acceleration']))),
                    ('maximum_shape_force', np.max(abs(saved['shape_layers']))),
                    ('maximum_point_residual', np.max(saved['point_errors'])), ('maximum_jump_residual', np.max(saved['jump_errors']))]:
                    evidence.check(item['name'] + ':' + name, float(actual) == item[name])
                energy = float(sum(float(weight) * float(value) for weight, value in zip(saved['weights'], saved['native_energy_layers'])))
                evidence.check(item['name'] + ':native_energy_sum', abs(energy - item['native_energy']) < 1e-24)
                evidence.check(item['name'] + ':complete_force_components', np.array_equal(saved['force'], saved['native_force'] + saved['wave_source_force']))
                if branch == 'reference':
                    evidence.check(item['name'] + ':zero_native_reference', not np.any(saved['native_force']) and item['relative_jump_residual'] is None
                        and item['relative_point_residual'] is None and item['native_energy'] == 0)
                row = dict(item)
                row.update(next(comparison for comparison in report['comparisons'] if comparison['material'] == item['material']))
                rows.append(row)
        table_path = evidence.output / 'refinement-comparison.csv'
        with table_path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(table_path, 'outputs')
        jets, jet_rows = {}, []
        for level in ['third', 'fourth']:
            report = verify_report(evidence, base + 'annular-live-transmission-time-jet-' + level + '-attempt01/status.json')
            evidence.check(level + ':completed_jet', report['state'] == 'complete' and report['includes_velocity_squared_radial_response'])
            baseline = read_archive(evidence.root / report['baseline_path'])
            levels = []
            for item in report['probes']:
                saved = read_archive(evidence.root / item['path'])
                amount = item['amount']
                geometry = (saved['forms'][:, :, 0, 0] - baseline['forms'][:, :, 0, 0]) / amount
                corrected = 2 * saved['forms'][:, :, 0, 1] + geometry
                evidence.check(level + ':' + str(amount) + ':geometry_replay', np.array_equal(geometry, saved['geometry']))
                evidence.check(level + ':' + str(amount) + ':corrected_replay', np.array_equal(corrected, saved['corrected']))
                evidence.check(level + ':' + str(amount) + ':field_at_zero', np.array_equal(2 * baseline['forms'][:, :, 0, 1], saved['field_at_zero']))
                jet_rows.append(dict(level=level, amount=amount, corrected_max=float(np.max(abs(corrected))),
                    geometry_max=float(np.max(abs(geometry))), field_max=float(np.max(abs(saved['field_at_zero']))),
                    raw_max=float(np.max(abs(saved['raw']))), quadratic_term_max=float(np.max(abs(saved['quadratic_term']))), valid_for_claim=False))
                levels.append(saved)
            last, previous = levels[-1], levels[-2]
            chosen = np.unravel_index(np.argmax(abs(last['corrected'])), last['corrected'].shape)
            spread = float(np.max(abs(last['corrected'] - previous['corrected'])))
            scale = float(np.max(abs(last['corrected'])))
            witness = dict(label=float(last['labels'][chosen[0]]), generator=int(chosen[1]),
                signed_second_jet=float(last['corrected'][chosen]), field=float(last['field_at_zero'][chosen]),
                geometry=float(last['geometry'][chosen]), step_spread_max=spread, maximum=scale,
                spread_to_signal=spread / scale if scale else None, sampled_resolved_nonzero=bool(scale > 100 * spread and scale > 0), valid_for_claim=False)
            jets[level] = dict(witness=witness, last=last, baseline=baseline)
        table_path = evidence.output / 'time-jet-comparison.csv'
        with table_path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(jet_rows[0]))
            writer.writeheader()
            writer.writerows(jet_rows)
        evidence.own(table_path, 'outputs')
        evidence.check('same_heldout_material_labels', np.array_equal(jets['third']['last']['labels'], jets['fourth']['last']['labels']))
        difference = float(np.max(abs(jets['fourth']['last']['corrected'] - jets['third']['last']['corrected'])))
        scale = max(jets['third']['witness']['maximum'], jets['fourth']['witness']['maximum'])
        refinement = dict(absolute_max=difference, relative_max=difference / scale if scale else None,
            continuum_certificate=False, finite_state_obstruction_only=True)
        curvature = verify_report(evidence, base + 'annular-native-curvature-repair-attempt02/status.json')
        evidence.check('completed_curvature_construction', curvature['state'] == 'complete')
        seal_path = evidence.output.parent / 'annular-quadratic-transmission-integrity-20261002.json'
        evidence.own(seal_path)
        digests = json.loads(seal_path.read_text())['hashes']
        deadline = perf_counter() + 1800
        with localcontext() as context:
            context.prec = 75
            unused, original, sources = restore_case(evidence, digests, 'MTS-primary', 'third', deadline)
        repair_rows = []
        for case in curvature['cases']:
            saved = read_archive(evidence.root / case['path'])
            authority = 'annular-live-native-transmission-third-attempt02' if case['level'] == 'third' else 'annular-live-native-transmission-fourth-primary-attempt03'
            parent = verify_report(evidence, base + authority + '/status.json')
            packet = json.loads((evidence.root / parent['packet_path']).read_text())
            state_path = next(row['path'] for row in parent['states'] if row['name'] == 'iteration0') if case['level'] == 'third' else parent['state_path']
            state = read_archive(evidence.root / state_path)
            high = next(row for row in parent['results'] if row['name'] == 'primary-16-64')
            acceleration = read_archive(evidence.root / high['path'])['acceleration']
            with localcontext() as context:
                context.prec = 75
                owner = adapt_owner(original.owner, packet['mesh'])
                loads, action = restore_refined(owner, state, packet['mesh'], packet, 'primary', deadline)
                source_traces, energy_ratios = [], []
                for label_index, label in enumerate(saved['labels']):
                    coefficients = np.array([[Decimal(value) for value in row] for row in saved['coefficients'][label_index]], dtype=object)
                    native = np.array([Decimal(value) for value in saved['native'][label_index]], dtype=object)
                    target = np.array([[Decimal(value) for value in row] for row in saved['target_jets'][label_index]], dtype=object)
                    width = np.diff(native)
                    degrees = np.arange(coefficients.shape[1])
                    values, before, after, second_before, second_after = target
                    maximum_error = max(float(np.max(abs(coefficients[:, 0] - values[:-1]))),
                        float(np.max(abs(np.sum(coefficients, axis=1) - values[1:]))),
                        float(np.max(abs(coefficients[:, 1] / width - after[:-1]))),
                        float(np.max(abs(np.sum(coefficients * degrees, axis=1) / width - before[1:]))),
                        float(np.max(abs(2 * coefficients[:, 2] / width**2 - second_after[:-1]))),
                        float(np.max(abs(np.sum(coefficients * degrees * (degrees - 1), axis=1) / width**2 - second_before[1:]))))
                    evidence.check(case['level'] + ':' + str(label) + ':independent_all_endpoint_jets', maximum_error < 1e-30, maximum_error)
                    cardinal, speed, drift = source_geometry(action, np.array([label]))
                    radius = Decimal.from_float(float(cardinal[0] @ action.source))
                    selected = int(np.searchsorted(native, radius, side='right') - 1)
                    local = (radius - native[selected]) / width[selected]
                    value = sum((coefficient * local**degree for degree, coefficient in enumerate(coefficients[selected])), Decimal(0))
                    first = sum((degree * coefficient * local**(degree - 1) for degree, coefficient in enumerate(coefficients[selected]) if degree), Decimal(0)) / width[selected]
                    second = sum((degree * (degree - 1) * coefficient * local**(degree - 2) for degree, coefficient in enumerate(coefficients[selected]) if degree > 1), Decimal(0)) / width[selected]**2
                    evidence.check(case['level'] + ':' + str(label) + ':independent_source_anchor', abs(value) < Decimal('1e-45'), str(value))
                    trace = speed[0] * float(second) + (drift[0] + cardinal[0] @ acceleration[:, -1]) * float(first)
                    source_traces.append(float(trace))
                    sample = samples(action, float(label), 20)
                    old_energy = float(sample['quadrature']['measure'] @ (sample['geometry']['gradient'] * sample['gradient']**2 / 2))
                    energy_ratios.append(float(saved['wave_energy'][label_index, 1] / old_energy))
            evidence.check(case['level'] + ':frozen_source_corner', np.max(abs(np.asarray(source_traces))) < 1e-9, float(np.max(abs(np.asarray(source_traces)))))
            row = dict(case, maximum_frozen_source_corner=float(np.max(abs(np.asarray(source_traces)))),
                minimum_wave_energy_ratio=min(energy_ratios), maximum_wave_energy_ratio=max(energy_ratios))
            repair_rows.append(row)
        evidence.report.update(refinement_rows=rows, time_jet_rows=jet_rows, time_jet_witnesses={key:value['witness'] for key, value in jets.items()},
            time_jet_grid_comparison=refinement, moving_transmission_law_verified=True, independent_third_jet_lift_verified=True,
            frozen_curvature_repair=repair_rows, repaired_higher_jet_state_constructed=True, live_repaired_state_solved=False,
            trajectory_computed=False, github_action=False, subagents_used=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
