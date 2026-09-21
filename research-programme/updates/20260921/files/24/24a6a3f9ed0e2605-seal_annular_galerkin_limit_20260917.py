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
    destination = intake/'annular-galerkin-limit-final-integrity.json'
    snapshot = intake/'annular-galerkin-limit-resume-snapshot.md'
    executed = intake/'annular-galerkin-limit-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable evidence already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, full_GR_limit_proven=False,
        valid_for_physics_claim=False, original_action_unchanged=True, github_action=False, subagents_used=False,
        finite_future_trajectories_read=False, no_forward_trajectory_rerun=True,
        internal_flat_benchmark_analytic_derivation=True, independently_reviewed_proof=False,
        instantaneous_force_convergence_proven=False, useful_h0_certified=False,
        time_integrator_error_certified=False, implementation_checks_not_physics_passes=True,
        protected_scan_scope='mtime since turn start2026-09-17T17:58:00Z; not a pre-turn full hash baseline')
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
                    raise RuntimeError('Missing or changed immutable evidence: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting immutable evidence: '+name)
                report['inputs'][key] = expected

    save()
    try:
        path = intake/'annular-full-characteristic-final-integrity.json'
        previous = json.loads(path.read_text())
        check('previous_seal_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(path)
        statuses, counts = {}, {}
        for name, label, count, cases in [('defect', 'annular-coupled-galerkin-defect-attempt01', 296, 7),
                ('coercivity', 'annular-galerkin-coercivity-attempt02', 110, 18),
                ('flow', 'annular-reference-energy-flow-attempt01', 99, 7)]:
            path = intake/label/'status.json'
            status = json.loads(path.read_text())
            check(name+'_complete', status['state'] == 'complete' and len(status['checks']) == count
                and len(status['cases']) == cases and all(row['passed'] for row in status['checks']))
            check(name+'_scope', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['complete_parent_source_action_derived'] and status['original_action_unchanged']
                and not status['finite_future_trajectories_read'])
            inherit(status)
            own(path)
            statuses[name], counts[name] = status, count
        failed_path = intake/'annular-galerkin-coercivity-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        failures = [row['name'] for row in failed['checks'] if not row['passed']]
        check('incorrect_strict_sampling_test_preserved', failed['state'] == 'failed'
            and failures == ['MTS33_positive_Gram_sampling'])
        inherit(failed)
        own(failed_path)
        fixed = statuses['coercivity']
        check('sampling_correction_not_action_change', fixed['stored_zero_sampling_entries_are_allowed']
            and fixed['supersedes_failed_strict_sampling_check'] == failed_path.parent.name
            and sum('nonnegative_partition_Gram_sampling' in row['name'] for row in fixed['checks']) == 3)
        check('coercivity_samples_not_uniform_certificate', fixed['numerical_positivity_not_uniform_neighborhood_certificate']
            and all(row['sampled_beta_not_a_uniform_neighborhood_certificate'] for row in fixed['cases'])
            and not fixed['h0_numerically_certified'])
        defect = statuses['defect']
        check('source_momentum_and_weak_forms_retained', defect['source_field_momentum_retained']
            and not defect['force_fit'] and not defect['force_correction']
            and {row['base_count'] for row in defect['cases']} == {33, 65, 129, 257, 513, 1025, 2049})
        check('nonmonotone_residuals_not_hidden', defect['cases'][-1]['maximum_sampled_base_defect']
            > defect['cases'][-2]['maximum_sampled_base_defect']
            and defect['cases'][1]['maximum_sampled_Gram_defect'] > defect['cases'][0]['maximum_sampled_Gram_defect'])
        check('reference_flow_not_evolved_MTS_assumption', statuses['flow']['reference_norms_only_not_evolved_MTS_regularity']
            and statuses['flow']['finite_samples_not_uniform_certificate'] and statuses['flow']['canonical_flow_not_velocity_flow'])
        check('inherited_failures_and_old_force_gates_retained', previous['inherited_failed_attempts_preserved'] == 25
            and previous['original_failed_cases_preserved'] and previous['failed_current_peak_force_cases'] == 4)
        note = root/'DERIVATION-20260917-coupled-Galerkin-defect-and-flat-nonlinear-limit.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('cited_note_paths_exist', all((root/name).is_file() for name in cited), cited)
        check('completed_note_scope_and_failure', 'PENDING' not in content and 'not the full GR limit' in content
            and '505 implementation checks' in content and 'retained failed-attempt total to26' in content
            and 'exact semidiscrete ODEs' in content and 'first-exit argument' in content)
        own(note)
        names = ['annular_characteristic_galerkin_defect_20260917.py', 'qualify_annular_galerkin_defect_20260917.py',
            'qualify_annular_galerkin_coercivity_20260917.py', 'qualify_annular_galerkin_coercivity_v2_20260917.py',
            'qualify_annular_reference_energy_flow_20260917.py', 'seal_annular_galerkin_limit_20260917.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('new_sources_compile', True, names)
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026, 9, 17, 17, 58, 0, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= started]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('resume_and_executed_source_preserved', True)
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            current_suite_checks=counts, total_successful_current_checks=sum(counts.values()),
            distinct_files_rehashed=len(cache), inherited_failed_attempts_preserved=26,
            prior_failed_attempts=25, new_failed_attempts_preserved=[str(failed_path.relative_to(root))],
            original_failed_cases_preserved=True, inherited_peak_force_failures_preserved=4,
            flat_benchmark_convergence_proof_status='Internal analytic derivation; not external proof review, full GR or certified time integration.',
            residual_results=defect['cases'], coercivity_samples=fixed['cases'], reference_flow_samples=statuses['flow']['cases'])
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=sum(counts.values()),
            rehashed_files=len(cache), protected_changed=len(changed), failed_attempts_preserved=26)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
