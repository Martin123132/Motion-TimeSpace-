from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import json
import re
import traceback


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-P2-force-lift-final-integrity.json'
    snapshot = intake/'annular-P2-force-lift-resume-snapshot.md'
    executed = intake/'annular-P2-force-lift-executed-sealer.py'
    table = intake/'annular-P2-force-lift-initial-comparison.csv'
    if any(path.exists() for path in [destination, snapshot, executed, table]):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        full_GR_limit_proven=False, valid_for_physics_claim=False, full_live_P2_force_convergence_proven=False,
        independently_reviewed_proof=False, no_forward_evolution=True,
        protected_scan_scope='mtime since2026-09-18T21:32:06Z; not a pre-turn full hash baseline')
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

    def own(path, kind='inputs'):
        report[kind][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2, allow_nan=False)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(path):
        status = json.loads(path.read_text())
        for kind in ['inputs', 'outputs']:
            for name, expected in status[kind].items():
                source = (root/name).resolve()
                key = str(source.relative_to(root))
                if not source.is_file() or digest(source) != expected:
                    raise RuntimeError('Missing or changed sealed source: '+name)
                if key in report['inputs'] and report['inputs'][key] != expected:
                    raise RuntimeError('Conflicting sealed source: '+name)
                report['inputs'][key] = expected
        own(path)
        return status

    save()
    try:
        previous = inherit(intake/'annular-P2-continuum-bridge-final-integrity.json')
        check('previous_seal_complete_and_preserved', previous['state'] == 'complete'
            and all(row['passed'] for row in previous['checks']))
        check('prior_execution_and_force_failures_preserved', previous['inherited_failed_attempts_preserved'] == 33
            and previous['inherited_peak_force_failures_preserved'] == 4)
        prior_science = [row for cases in previous['scientific_results'].values() for row in cases]
        check('previous_six_scientific_accuracy_failures_retained', len(prior_science) == 6
            and all(not row['sampled_comparison_qualified'] for row in prior_science))
        names = ['annular-P2-saved-force-budget-reference-attempt01', 'annular-P2-saved-force-budget-MTS-attempt01',
            'annular-P2-conforming-force-lift-manufactured-attempt01', 'annular-P2-conforming-force-lift-saved-attempt01',
            'annular-P2-initial-force-refinement-source16-attempt01', 'annular-P2-initial-force-refinement-uniform129-attempt01']
        statuses = {}
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses[name] = status
            check(name+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            check(name+'_private_nonclaim', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['full_live_P2_force_convergence_proven'] and not status['github_action']
                and not status['subagents_used'] and status['no_forward_evolution'])
        for branch in ['reference', 'MTS']:
            status = statuses['annular-P2-saved-force-budget-'+branch+'-attempt01']
            check(branch+'_all_precision_controls', {row['configuration'] for row in status['cases']} ==
                {'baseline', 'action48', 'action64', 'label28', 'radial26', 'material18', 'material22', 'combined'})
            check(branch+'_tested_controls_small_not_certified', status['tested_held_state_controls_below_extraction_gate']
                and status['not_a_certified_numerical_error_bound'] and status['not_a_trajectory_time_refinement']
                and status['material_transfer_not_an_evolved_material_refinement'])
        manufactured = statuses['annular-P2-conforming-force-lift-manufactured-attempt01']
        live = statuses['annular-P2-conforming-force-lift-saved-attempt01']
        check('offshell_identities_both_branches_and_negative_controls', len(manufactured['cases']) == 4
            and len(manufactured['checks']) == 31 and all(row['identity_error'] < 2e-10 for row in manufactured['cases']))
        check('four_live_identity_cases', {(row['branch'], row['time']) for row in live['cases']} ==
            {('reference', 0.), ('reference', .004), ('MTS', .001), ('MTS', .004)}
            and all(row['identity_error'] < 2e-9 for row in live['cases']))
        comparison = inherit(intake/'annular-P2-continuum-comparison-65-attempt01/status.json')
        peak = comparison['independent_oracle']['force_peak_scale']
        absolute_gate = comparison['gates']['sampled_force_absolute']
        relative_gate = comparison['gates']['sampled_force_peak_relative']
        initial = []
        for configuration in ['source16', 'uniform129']:
            name = 'annular-P2-initial-force-refinement-'+configuration+'-attempt01'
            status = statuses[name]
            check(configuration+'_paired_initial_only', len(status['cases']) == 2
                and {row['branch'] for row in status['cases']} == {'reference', 'MTS'}
                and all(row['time'] == 0. for row in status['cases'])
                and status['only_initial_data_not_an_evolved_accuracy_test'])
            for row in status['cases']:
                error = abs(row['force_error_from_continuum'])
                initial.append(dict(branch=row['branch'], configuration=configuration, scalar_nodes=row['scalar_nodes'],
                    time=0., force_error=row['force_error_from_continuum'], error_ratio_to_old65=row['absolute_error_ratio'],
                    absolute_gate=absolute_gate, peak_scaled_gate=relative_gate*peak,
                    initial_absolute_gate_pass=error <= absolute_gate,
                    initial_combined_gate_pass=error <= absolute_gate and error <= relative_gate*peak,
                    evolved_accuracy_claim=False, valid_for_claim=False,
                    source_path=str((intake/name/'status.json').relative_to(root))))
        check('all_initial_combined_force_targets_still_fail', len(initial) == 4
            and all(not row['initial_combined_gate_pass'] for row in initial))
        with table.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(initial[0]))
            writer.writeheader()
            writer.writerows(initial)
        with table.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check('new_csv_parses_and_sources_exist', len(parsed) == 4 and all(None not in row
            and (root/row['source_path']).is_file() and row['valid_for_claim'] == 'False' for row in parsed))
        own(table, 'outputs')
        note = root/'DERIVATION-20260918-P2-conforming-force-lift-and-targeted-refinement.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('note_complete_and_limits_explicit', 'Pending' not in content and 'being finalized' not in content
            and 'not interval-certified' in content and 'old failed full-horizon force gates' in content
            and 'already known to miss' in content)
        own(note)
        for name in ['budget_annular_P2_saved_force_20260918.py', 'derive_annular_P2_conforming_force_lift_20260918.py',
                'probe_annular_P2_force_refinement_20260918.py', 'seal_annular_P2_conforming_force_lift_20260918.py']:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('new_sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 18, 21, 32, 6, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime >= start]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            successful_current_implementation_checks=sum(len(status['checks']) for status in statuses.values()),
            inherited_failed_attempts_preserved=33, inherited_peak_force_failures_preserved=4,
            inherited_short_horizon_scientific_failures_preserved=6, new_failed_attempts_preserved=[],
            initial_refinement_results=initial, new_initial_combined_force_failures=4,
            distinct_files_rehashed=len(cache))
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']),
            implementation_checks=report['successful_current_implementation_checks'], files_rehashed=len(cache),
            new_initial_combined_force_failures=4)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
