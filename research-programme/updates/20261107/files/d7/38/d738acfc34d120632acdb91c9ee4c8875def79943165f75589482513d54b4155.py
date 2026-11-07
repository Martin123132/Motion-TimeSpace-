from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_position_reaction_20260929 import ResponseSum
from annular_position_force_compensated_20260929 import force_integrals
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from annular_candidate_energy_current_20260921 import reconstructed_solver
from scipy.sparse import load_npz
from decimal import localcontext
from time import perf_counter
import csv
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-position-force-compensated-diagnostic-attempt01', __file__)
    started, deadline = perf_counter(), perf_counter()+2800
    try:
        evidence.report.update(diagnostic_only=True, accepted_for_C0=False,
            numerical_acceptance_passed=False, branch='reference-reference', level='fine',
            scope='Independent weak field-force derivative, resolution, compensated summation',
            actual_flux_by_parts_implemented=False, full_live_reaction_recomputed=False,
            github_action=False, subagents_used=False, original_workbench_write=False)
        evidence.own(evidence.root/'DERIVATION-20260929-compensated-field-force-integration.md')
        parent_path = evidence.output.parent/'annular-position-reaction-diagnostic-attempt02/status.json'
        parent = json.loads(parent_path.read_text())
        evidence.own(parent_path)
        digests = dict(parent['inputs'], **parent['outputs'])
        read = lambda relative: load_owned(evidence, digests, evidence.root/relative)
        report = lambda name: read(str((evidence.output.parent/name/'status.json').relative_to(evidence.root)))
        branch, level = 'reference-reference', 'fine'
        match = lambda status: next(row for row in status['cases'] if row['branch'] == branch and row['level'] == level)
        loads, action, sources = restore_case(evidence, digests, branch, level, deadline)
        live = match(report('annular-live-support-acceleration-attempt01'))
        position_case = match(report('annular-compensated-position-attempt04'))
        jet_case = match(report('annular-position-metric-jet-validation-attempt01'))
        directions = read(live['direction_path'])
        correction = read(live['paths']['projection'])['correction']
        mode_rate = read(jet_case['paths']['completed_metric_time'])['mode_rate']

        def restore(archive):
            solver, solution = reconstructed_solver(archive)
            return MetricResponse(solver, solution, archive.get('forcing'), 0., [])

        position = ResponseSum(restore(read(position_case['paths']['response'])),
            restore(read(jet_case['paths']['transported_old_metric'])))
        baseline = read(match(parent)['paths']['material64'])
        old_force, old_base = baseline['force_wave'].copy(), baseline['base_force_wave'].copy()
        old_force[:, -1], old_base[:, -1] = 0., 0.
        label_path = evidence.output.parent/'annular-original-label-rule-diagnostic-attempt03/status.json'
        label_report = json.loads(label_path.read_text())
        evidence.own(label_path)
        evidence.check('high_label_baseline_complete', label_report['state'] == 'complete')
        label_baselines = {}
        for order in [1024, 2048]:
            row = next(item for item in label_report['cases'] if item['summary']['material_order'] == order)
            digests[row['path']] = label_report['outputs'][row['path']]
            label_baselines[order] = read(row['path'])['force'].copy()
            label_baselines[order][:, -1] = 0.
        owner = read(sources['parent'])
        centre = next(row for row in owner['centres'] if row.get('route') == 'resampled')
        matrix_path = evidence.root/centre['matrix_path']
        evidence.check('matrix_owned', str(matrix_path.relative_to(evidence.root)) in digests)
        inverse = BandedSourceInverse(load_npz(matrix_path), loads.rates.shape)
        invmax = lambda array: float(np.max(np.abs(inverse.solve(array.ravel()))))
        maximum = lambda array: float(np.max(np.abs(array)))

        def progress(stage):
            evidence.report['progress'] = dict(stage=stage, seconds=perf_counter()-started)
            evidence.save()
            print(json.dumps(evidence.report['progress']), flush=True)

        rows, previous = [], None
        with localcontext() as context:
            context.prec = 70
            for radial_order, label_order in [(32, 36), (40, 44), (48, 52)]:
                result = force_integrals(loads, action, directions, correction, mode_rate, position,
                    radial_order, label_order, deadline, progress)
                evidence.check('finite_force_'+str(radial_order),
                    all(np.all(np.isfinite(value)) for value in result.values()))
                oracle_error = invmax(result['compensated_oracle_difference'])
                evidence.check('independent_flux_derivative_'+str(radial_order), oracle_error <= 2e-11, oracle_error)
                ordinary, compensated = result['ordinary_position_force'], result['compensated_position_force']
                ordinary_error, compensated_error = invmax(ordinary-old_force), invmax(compensated-old_force)
                successive = None if previous is None else invmax(compensated-previous)
                row = dict(radial_order=radial_order, label_order=label_order,
                    ordinary_derivative_replay_inverse=ordinary_error,
                    compensated_derivative_replay_inverse=compensated_error,
                    ordinary_replay_within_2e11=ordinary_error <= 2e-11,
                    compensated_replay_within_2e11=compensated_error <= 2e-11,
                    summation_shift_inverse=invmax(compensated-ordinary),
                    derivative_oracle_inverse=oracle_error,
                    baseline_from_saved_ordinary=maximum(result['ordinary_base_force']-old_base),
                    baseline_from_saved_compensated=maximum(result['compensated_base_force']-old_base),
                    baseline_from_original1024=maximum(result['compensated_base_force']-label_baselines[1024]),
                    baseline_from_original2048=maximum(result['compensated_base_force']-label_baselines[2048]),
                    baseline_within_2e15=maximum(result['compensated_base_force']-label_baselines[2048]) <= 2e-15,
                    compensated_successive_inverse=successive,
                    successive_within_2e11=None if successive is None else successive <= 2e-11,
                    maximum_position_force=maximum(compensated), seconds=perf_counter()-started,
                    valid_for_claim=False)
                path = evidence.output/('field-force-'+str(radial_order)+'-'+str(label_order)+'.npz')
                np.savez_compressed(path, **result)
                evidence.own(path, 'outputs')
                evidence.report['cases'].append(dict(summary=row, path=str(path.relative_to(evidence.root))))
                evidence.save()
                print(json.dumps(row), flush=True)
                previous = compensated
                rows.append(row)
        path = evidence.output/'field-force-resolution.csv'
        with path.open('x', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        evidence.own(path, 'outputs')
        evidence.report['seconds'] = perf_counter()-started
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
