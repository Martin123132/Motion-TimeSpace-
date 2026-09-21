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
    destination = intake/'annular-P2-continuum-bridge-final-integrity.json'
    snapshot = intake/'annular-P2-continuum-bridge-resume-snapshot.md'
    executed = intake/'annular-P2-continuum-bridge-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        full_GR_limit_proven=False, valid_for_physics_claim=False, full_live_P2_force_convergence_proven=False,
        independently_reviewed_proof=False, proper_acceleration_comparison_claimed=False,
        protected_scan_scope='mtime since2026-09-18T18:42:59Z; not a pre-turn full hash baseline')
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
                    raise RuntimeError('Missing or modified sealed source: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed source: '+name)
                report['inputs'][key] = expected
        own(path)
        return status

    save()
    try:
        previous = inherit(intake/'annular-P2-tight-error-budget-final-integrity.json')
        check('previous_seal_complete_and_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']))
        check('all_previous_failed_attempts_preserved', previous['inherited_failed_attempts_preserved'] == 33
            and previous['inherited_peak_force_failures_preserved'] == 4)
        statuses = {}
        for pattern in ['annular-P2-continuum-bridge-*-attempt*/status.json',
                'annular-P2-continuum-comparison-*-attempt*/status.json', 'annular-P2-traction-gap-*-attempt*/status.json',
                'annular-P2-broken-traction-*-attempt*/status.json', 'annular-P2-frozen-frequencies-attempt*/status.json']:
            for path in sorted(intake.glob(pattern)):
                status = inherit(path)
                statuses[path.parent.name] = status
                check(path.parent.name+'_not_left_running', status['state'] in ['complete', 'failed'])
                check(path.parent.name+'_nonclaim_scope', not status['valid_for_physics_claim']
                    and not status['full_GR_limit_proven'] and not status.get('github_action', False)
                    and not status.get('subagents_used', False) and not status.get('full_live_P2_force_convergence_proven', False))
                if status['state'] == 'complete':
                    check(path.parent.name+'_implementation_checks_pass', all(row['passed'] for row in status['checks']))
        required = ['continuum-384', 'continuum-512', 'reference-33', 'MTS-33', 'reference-65', 'MTS-65']
        check('paired_independent_and_finite_trajectories_completed', all(
            statuses['annular-P2-continuum-bridge-'+key+'-attempt01']['state'] == 'complete' for key in required))
        comparisons = {name:status for name,status in statuses.items()
            if 'comparison-' in name and status['state'] == 'complete'}
        check('physical_comparison_completed', bool(comparisons))
        coverage = {(row['branch'],row['base_count']) for status in comparisons.values() for row in status['cases']}
        check('all_three_resolutions_both_branches_compared', coverage == {
            (branch,count) for branch in ['reference','MTS'] for count in [17,33,65]})
        for name, status in comparisons.items():
            cases = status['cases']
            check(name+'_matched_branch_coverage', all(
                {row['branch'] for row in cases if row['base_count'] == count} == {'reference', 'MTS'}
                for count in {row['base_count'] for row in cases}))
            check(name+'_scientific_failures_recorded', sorted(status['scientific_gate_failures']) == sorted(
                row['key'] for row in cases if not row['sampled_comparison_qualified']))
            check(name+'_force_and_gap_distinctions_preserved', status['force_is_reduced_not_raw_covector']
                and status['source_position_gap_included'] and status['compare_same_Eulerian_radii']
                and status['only_five_time_samples_not_a_continuous_time_peak_bound']
                and status['gates_are_new_short_horizon_checks_not_replacement_for_old_full_horizon_failures'])
        old = inherit(intake/'annular-initial-corner-response-final-integrity.json')
        identities = [status for status in statuses.values() if status.get('boundary_virtual_work_identity_not_convergence')]
        check('derived_traction_identity_all_resolutions_and_endpoints',
            {(row['branch'],row['base_count'],row['time']) for status in identities for row in status['cases']}
            == {(branch,count,time) for branch in ['reference','MTS'] for count in [17,33,65] for time in [0.,.004]}
            and all(status['state']=='complete' and all(row['identity_error']<2e-9 for row in status['cases']) for status in identities))
        offshell = statuses['annular-P2-broken-traction-offshell-attempt01']
        check('offshell_identity_and_negative_controls', offshell['state']=='complete' and len(offshell['checks'])==14
            and offshell['arbitrary_acceleration_not_using_equations_of_motion']
            and all(row['identity_error']<2e-10 for row in offshell['cases']))
        check('original_full_horizon_force_failures_still_fail', len(old['comparison_results']) == 4
            and all(not row['original_peak_force_gate_pass'] for row in old['comparison_results']))
        note = root/'DERIVATION-20260918-P2-independent-continuum-bridge.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('cited_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('note_final_and_scope_limited', 'In progress' not in content and 'Pending completion' not in content
            and 'not a certified infinite-resolution bound' in content and 'old failed full-horizon force gates' in content)
        own(note)
        names = ['run_annular_P2_continuum_bridge_20260918.py', 'compare_annular_P2_continuum_bridge_20260918.py',
            'diagnose_annular_P2_traction_gap_20260918.py', 'derive_annular_P2_broken_traction_identity_20260918.py',
            'verify_annular_P2_broken_traction_offshell_20260918.py',
            'diagnose_annular_P2_frozen_frequencies_20260918.py', 'seal_annular_P2_continuum_bridge_20260918.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('sources_compile_no_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 18, 18, 42, 59, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= start]
        check('protected_changed_file_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        checks = sum(len(status['checks']) for status in statuses.values() if status['state'] == 'complete')
        failed = [name for name,status in statuses.items() if status['state'] == 'failed']
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            successful_current_implementation_checks=checks, distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=33, inherited_peak_force_failures_preserved=4,
            new_failed_attempts_preserved=failed, scientific_results={name:status['cases'] for name,status in comparisons.items()},
            scientific_gate_failures={name:status['scientific_gate_failures'] for name,status in comparisons.items()})
        save()
        print(json.dumps(dict(state='complete', integrity_checks=len(report['checks']),
            implementation_checks=checks, files_rehashed=len(cache), failed_attempts=failed,
            scientific_gate_failures=report['scientific_gate_failures'])), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
