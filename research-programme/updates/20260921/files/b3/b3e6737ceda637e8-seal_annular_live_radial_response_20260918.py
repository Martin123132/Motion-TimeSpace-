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
    destination = intake/'annular-live-radial-response-final-integrity.json'
    snapshot = intake/'annular-live-radial-response-resume-snapshot.md'
    executed = intake/'annular-live-radial-response-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable final evidence already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, no_forward_evolution=True,
        original_action_unchanged=True, original_initial_data_unchanged=True, github_action=False,
        subagents_used=False, full_GR_limit_proven=False, valid_for_physics_claim=False,
        full_live_moving_source_force_convergence_proven=False, MTS_Gram_stress_derived=False,
        internal_scalar_metric_response_bound_derived=True, internal_fixed_position_Hessian_bound_derived=True,
        independently_reviewed_proof=False, implementation_checks_not_physics_passes=True,
        protected_scan_scope='mtime since2026-09-18T02:44:25Z; not a pre-turn full hash baseline')
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

    def inherit(path):
        status = json.loads(path.read_text())
        for table in ['inputs', 'outputs']:
            for name, expected in status[table].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Missing or modified sealed input: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed hash: '+name)
                report['inputs'][key] = expected
        own(path)
        return status

    save()
    try:
        previous = inherit(intake/'annular-full-interval-force-final-integrity.json')
        check('previous_seal_complete_and_all_hashes_retained', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']))
        check('prior_failed_attempt_and_force_counts', previous['inherited_failed_attempts_preserved'] == 30
            and previous['inherited_peak_force_failures_preserved'] == 4)
        failed_path = intake/'annular-live-radial-response-attempt01/status.json'
        failed = inherit(failed_path)
        check('new_failed_integration_control_preserved', failed['state'] == 'failed'
            and [row['name'] for row in failed['checks'] if not row['passed']]
                == ['wave_independent_mass_difference_matches_adjoint'])
        statuses = {}
        for name, count in [('annular-live-radial-response-attempt02', 46), ('annular-live-mass-hessian-attempt01', 11),
                ('annular-live-stress-response-attempt01', 12)]:
            status = inherit(intake/name/'status.json')
            statuses[name] = status
            check(name+'_complete', status['state'] == 'complete' and len(status['checks']) == count
                and all(row['passed'] for row in status['checks']))
            check(name+'_no_physics_upgrade_or_forward_evolution', not status['valid_for_physics_claim']
                and not status['full_GR_limit_proven'] and status['no_forward_evolution'] and not status['subagents_used'])
        radial = statuses['annular-live-radial-response-attempt02']
        hessian = statuses['annular-live-mass-hessian-attempt01']
        stress = statuses['annular-live-stress-response-attempt01']
        check('knot_alignment_changes_integrator_not_acceptance_or_input',
            radial['interpolation_knots_are_radial_integration_boundaries']
            and radial['supersedes_integration_control_failure'] == failed_path.parent.name
            and max(row['error'] for row in radial['cases'] if row['kind'] != 'localized_energy') < 2e-8)
        check('analytic_tube_and_response_constants_not_sample_fits', radial['uniform_bounds_derived_not_inferred_from_samples']
            and radial['analytic_constants']['derived_metric_floor'] > radial['analytic_constants']['metric_floor']
            and radial['physical_source_width_fixed'] == .02 and not radial['zero_width_limit_proven'])
        check('positive_Hessian_has_fixed_position_scope', hessian['analytic_lower_eigenvalue'] > 0
            and hessian['fixed_source_position_and_density'] and hessian['constrained_mass_Hessian_not_full_moving_canonical_chart']
            and hessian['no_uniform_third_source_momentum_variation_claim'])
        check('stress_counterexample_blocks_arbitrary_MTS_substitution', stress['counterexample_not_MTS_stress_identification']
            and stress['MTS_Gram_stress_not_replaced_with_scalar_stress']
            and stress['prescribed_radial_loading_test_not_full_conserved_potential_solution'])
        old = json.loads((intake/'annular-initial-corner-response-final-integrity.json').read_text())
        check('four_original_flat_force_failures_still_fail', len(old['comparison_results']) == 4
            and all(not row['original_peak_force_gate_pass'] for row in old['comparison_results']))
        note = root/'DERIVATION-20260918-live-metric-response-and-moving-mass-hessian.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('note_complete_with_correct_scope_and_failure_record', '69 successful implementation checks' in content
            and '31 retained failed attempts' in content and 'not a full GR/MTS limit claim' in content
            and 'PENDING' not in content and 'results and final integrity status are appended after execution' not in content)
        own(note)
        names = ['annular_live_radial_response_20260918.py', 'annular_live_radial_response_v2_20260918.py',
            'qualify_annular_live_radial_response_20260918.py', 'qualify_annular_live_radial_response_v2_20260918.py',
            'qualify_annular_live_mass_hessian_20260918.py', 'qualify_annular_live_stress_response_20260918.py',
            'seal_annular_live_radial_response_20260918.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_new_sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists(), names)
        protected = root.parent/'formalization-workbench'
        timestamp = datetime(2026, 9, 18, 2, 44, 25, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= timestamp]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('resume_and_executed_sealer_saved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            total_successful_current_checks=69, distinct_files_rehashed=len(cache),
            inherited_peak_force_failures_preserved=4, inherited_failed_attempts_preserved=31,
            prior_failed_attempts=30, new_failed_attempts_preserved=[str(failed_path.relative_to(root))],
            results={name: status['cases'] for name, status in statuses.items()},
            analytic_metric_constants=radial['analytic_constants'], analytic_Hessian_lower_matrix=hessian['analytic_lower_matrix'])
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=69,
            rehashed_files=len(cache), protected_changed=len(changed), failed_attempts_preserved=31)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
