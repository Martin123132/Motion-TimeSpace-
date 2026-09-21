from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-full-interval-force-final-integrity.json'
    snapshot = intake/'annular-full-interval-force-resume-snapshot.md'
    executed = intake/'annular-full-interval-force-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable final evidence already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, original_action_unchanged=True,
        original_initial_data_unchanged=True, comparison_path_only=True, github_action=False,
        subagents_used=False, no_nonlinear_finite_trajectory_rerun=True,
        full_GR_limit_proven=False, valid_for_physics_claim=False,
        internal_flat_full_interval_force_argument_derived=True,
        independently_reviewed_proof=False, useful_h0_certified=False,
        time_integration_error_certified=False, implementation_checks_not_physics_passes=True,
        internal_bound='Uniform canonical energy O(h^(3/5)); material force O(h^(1/10)); exact prescribed-flat semidiscrete family only.',
        protected_scan_scope='mtime since recovered time check2026-09-18T00:26:48Z; not a pre-turn full hash baseline')
    cache = {}

    def digest(path):
        path = path.resolve()
        if path not in cache:
            hasher = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(1024*1024):
                    hasher.update(chunk)
            cache[path] = hasher.hexdigest()
        return cache[path]

    def own(path, table='inputs'):
        report[table][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs', 'outputs']:
            for name, expected in status[table].items():
                path = (root/name).resolve()
                key = str(path.relative_to(root))
                if not path.is_file() or digest(path) != expected:
                    raise RuntimeError('Missing or modified sealed input: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed hash: '+name)
                report['inputs'][key] = expected

    save()
    try:
        previous_path = intake/'annular-nonlinear-initial-force-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_seal_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        path = intake/'annular-smoothed-comparison-attempt02/status.json'
        status = json.loads(path.read_text())
        check('current_qualification_complete', status['state'] == 'complete' and len(status['checks']) == 327
            and all(row['passed'] for row in status['checks']))
        inherit(status)
        own(path)
        curvature_path = intake/'annular-source-curvature-comparison-attempt01/status.json'
        curvature = json.loads(curvature_path.read_text())
        check('independent_source_curvature_qualification_complete', curvature['state'] == 'complete'
            and len(curvature['checks']) == 16 and len(curvature['cases']) == 16
            and all(row['passed'] for row in curvature['checks']))
        inherit(curvature)
        own(curvature_path)
        check('independent_curvature_not_fitted_input', curvature['projection_amplitude_not_used_as_fitted_input']
            and curvature['original_action_unchanged'] and curvature['old_peak_force_gates_unchanged']
            and not curvature['finite_future_trajectories_read'] and not curvature['valid_for_physics_claim']
            and not curvature['full_GR_limit_proven'])
        check('same_action_and_data_no_future_fit', status['original_action_unchanged'] and status['original_initial_data_unchanged']
            and status['comparison_path_only'] and not status['finite_future_trajectories_read']
            and status['no_nonlinear_finite_trajectory_rerun'] and status['old_peak_force_gates_unchanged'])
        check('no_parent_or_GR_or_numeric_certification_upgrade', not status['complete_parent_source_action_derived']
            and not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
            and not status['useful_h0_certified'] and not status['independently_reviewed_proof']
            and not status['time_integration_error_certified'])
        expected = {(branch, count) for branch in ['reference', 'MTS'] for count in [129, 257, 513, 1025]}
        check('both_branches_all_four_phases', {(row['branch'], row['base_count']) for row in status['cases']} == expected)
        check('same_endpoint_and_envelope_times', all([point['time'] for point in row['probes']] == [0., .071, .195, .21, .4]
            for row in status['cases']))
        probes = [point for row in status['cases'] for point in row['probes']]
        check('independent_quadrature_and_endpoint_derivative', max(max(point['quadrature_control'].values()) for point in probes) < 2e-8
            and max(point['averaged_derivative_boundary_error'] for point in probes) < 2e-8)
        check('exact_cancellation_and_nonlinear_decomposition', max(point['linear_identity_error'] for point in probes) < 2e-10
            and max(point['decomposition_error'] for point in probes) < 2e-10
            and max(point['elliptic_relative_residual'] for point in probes) < 2e-9)
        check('stationary_corrector_retained_only_where_needed', all(row['max_scaled_corrector'] == 0 for row in status['cases'] if row['branch'] == 'reference')
            and all(row['max_scaled_corrector'] > 0 for row in status['cases'] if row['branch'] == 'MTS')
            and status['all_Gram_rows_retained'] and status['source_field_momentum_retained'])
        check('rate_balance_not_sample_fit', status['derived_exponents'] == dict(epsilon='4/5', accumulated_energy='3/5',
            linear_force='1/10', nonlinear_force='1/5', stationary_corrector='3/2')
            and status['uniform_bounds_not_inferred_from_samples'])
        failed_path = intake/'annular-smoothed-comparison-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        check('failed_six_row_checker_preserved', failed['state'] == 'failed'
            and [row['name'] for row in failed['checks'] if not row['passed']] == ['MTS129_stationary_kink_local_support']
            and status['supersedes_support_count_checker_failure'] == failed_path.parent.name)
        inherit(failed)
        own(failed_path)
        old_path = intake/'annular-initial-corner-response-final-integrity.json'
        old = json.loads(old_path.read_text())
        check('all_four_original_force_failures_still_fail', previous['inherited_peak_force_failures_preserved'] == 4
            and len(old['comparison_results']) == 4 and all(not row['original_peak_force_gate_pass'] for row in old['comparison_results']))
        check('retained_failure_chain_unchanged', previous['inherited_failed_attempts_preserved'] == 29)
        note = root/'DERIVATION-20260918-full-interval-force-comparison-path.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('completed_note_contains_scope_and_results', 'PENDING' not in content
            and '327 successful implementation checks' in content and '30 retained failed attempts' in content
            and 'NOT the full GR limit' in content and 'epsilon^2/h' in content
            and 'Qualification results and final integrity status are recorded after execution.' not in content)
        own(note)
        names = ['annular_smoothed_comparison_20260918.py', 'qualify_annular_source_curvature_20260918.py', 'qualify_annular_smoothed_comparison_20260918.py',
            'qualify_annular_smoothed_comparison_v2_20260918.py', 'seal_annular_full_interval_force_20260918.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_new_sources_compile', True, names)
        check('no_bytecode_cache_created', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        timestamp = datetime(2026, 9, 18, 0, 26, 48, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= timestamp]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('resume_snapshot_and_executed_sealer_saved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            total_successful_current_checks=len(status['checks'])+len(curvature['checks']), distinct_files_rehashed=len(cache),
            inherited_peak_force_failures_preserved=4, inherited_failed_attempts_preserved=30,
            prior_failed_attempts=29, new_failed_attempts_preserved=[str(failed_path.relative_to(root))],
            results=status['cases'], source_curvature_results=curvature['cases'])
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=len(status['checks'])+len(curvature['checks']),
            rehashed_files=len(cache), protected_changed=len(changed), failed_attempts_preserved=30)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
