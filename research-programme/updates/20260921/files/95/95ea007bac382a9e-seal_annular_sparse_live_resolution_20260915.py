import hashlib
import json
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path
from navier_stokes_source_audit_20260908 import limit_process


def main():
    limit_process()
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-sparse-live-resolution-final-integrity.json'
    snapshot = intake/'annular-sparse-live-resolution-resume-snapshot.md'
    executed = intake/'annular-sparse-live-resolution-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Do not overwrite an existing seal or executed snapshot.')
    report = dict(state='running', checks=[], inputs={}, outputs={},
        full_GR_limit_proven=False, valid_for_physics_claim=False,
        parent_source_action_uniquely_derived=False,
        benchmark_is_not_observational_evidence=True, github_action=False, subagents_used=False,
        protected_scan_scope='mtime since2026-09-15T13:30:46Z, not a pre-turn hash baseline.')
    cache = {}

    def digest(path):
        path = path.resolve()
        if path not in cache:
            value = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(1024*1024):
                    value.update(chunk)
            cache[path] = value.hexdigest()
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
                path.relative_to(root)
                if not path.is_file() or digest(path) != expected:
                    raise RuntimeError('Missing or changed immutable source: '+name)
                if name in report['inputs'] and report['inputs'][name] != expected:
                    raise RuntimeError('Conflicting immutable source digest: '+name)
                report['inputs'][name] = expected

    save()
    try:
        prior_path = intake/'annular-independent-live-continuum-final-integrity.json'
        previous = json.loads(prior_path.read_text())
        check('previous_checkpoint_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(prior_path)
        statuses, counts = {}, {}
        for label, folder, count in [
            ('sparse_equivalence', 'annular-sparse-live-equivalence-attempt01', 44),
            ('initial_resolution_law', 'annular-initial-resolution-law-attempt01', 8),
            ('nonaffine_transport', 'annular-sparse-live-transport-controls-attempt01', 8),
            ('phase_refinement', 'annular-sparse-live-phase-refinement-attempt01', 62),
            ('initial_force_onset', 'annular-initial-force-onset-attempt01', 9),
            ('halfstep', 'annular-sparse-live-halfstep-controls-attempt01', 14),
            ('fine_refinement', 'annular-sparse-live-fine-refinement-attempt01', 26),
            ('precision_controls', 'annular-sparse-live-precision-controls-attempt01', 21)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status, allow_nan=False)
            check(label+'_complete', status['state'] == 'complete' and len(status['checks']) == count and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim'] and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label], counts[label] = status, count
        phase, fine = statuses['phase_refinement'], statuses['fine_refinement']
        cases = phase['cases']+fine['cases']
        check('same_branches_at_every_declared_grid', {(row['branch'], row['count']) for row in cases}
              == {(branch, count) for branch in ['reference', 'MTS'] for count in [119,129,139,149,253,513,1025]})
        check('no_changed_preparation_or_deleted_Gram_rows', all(status['same_original_preparation_width_domain_and_duration']
              and status['all_Gram_factors_retained'] and not status['energy_projection'] for status in [phase,fine]))
        check('same_unchanged_accuracy_gates', phase['prespecified_accuracy_gates'] == fine['prespecified_accuracy_gates']
              and fine['prespecified_accuracy_gates']['field_relative'] == .005 and fine['prespecified_accuracy_gates']['cell_margin'] == .15)
        check('all_force_gate_flags_recomputed', all(row['strict_force_gate'] == (row['force_absolute_error'] < 2e-7 and row['force_relative_error'] < .02) for row in cases))
        check('all_field_and_source_gate_flags_recomputed', all(row['strict_half_percent_waveform_gate'] == (row['maximum_field_error'] < .005)
            and row['source_clock_gate'] == (row['maximum_source_error'] < 5e-7 and row['maximum_velocity_error'] < 2e-5 and row['maximum_clock_error'] < 2e-7) for row in cases))
        check('phase_force_failures_not_hidden', any(not row['strict_force_gate'] for row in phase['cases']))
        check('source_momentum_transport_retained', all(status['moving_source_field_momentum_derivative_retained'] for status in [phase, fine]))
        check('initial_resolution_law_not_global_evolution_theorem', statuses['initial_resolution_law']['initial_H1_error_leading_coefficient_derived']
            and statuses['initial_resolution_law']['initial_accuracy_does_not_prove_evolving_accuracy']
            and not fine['uniform_phase_independent_convergence_proven'])
        check('force_onset_derived_not_fitted_or_new_physics_claim', statuses['initial_force_onset']['initial_force_onset_derived_from_wave_and_source_equations']
            and statuses['initial_force_onset']['second_trace_incompatibility_diagnosed_not_initial_data_replaced']
            and statuses['initial_force_onset']['result_explains_shared_benchmark_transient_not_MTS_observational_prediction'])
        check('prior_failed_attempts_remain_in_inherited_evidence', previous['preserved_failed_attempts'] == 5)
        note = root/'DERIVATION-20260915-sparse-live-resolution-and-phase-tests.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_cited_local_paths_exist', all((root/name).is_file() for name in cited), cited)
        check('main_note_complete_and_scope_explicit', 'RESULTS_PENDING' not in content and 'not an isolated fixed-spacing phase experiment' in content
            and 'not derived physical MTS coefficients' in content)
        own(note)
        scripts = [root/name for name in cited if name.startswith('scripts/') and name.endswith('.py')]
        scripts.append(Path(__file__))
        for path in scripts:
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_modules_compile_without_bytecode', len(scripts) >= 9, len(scripts))
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026,9,15,13,30,46,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= started]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('immutable_resume_and_executed_sealer_saved', snapshot.is_file() and executed.is_file())
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            current_suite_checks=counts, total_successful_current_checks=sum(counts.values()),
            distinct_files_rehashed=len(cache), inherited_failed_attempts_preserved=5,
            finest_cases=[row for row in cases if row['count'] == 1025],
            strict_finest_waveform_pass=all(row['strict_half_percent_waveform_gate'] for row in fine['cases'] if row['count'] == 1025),
            strict_finest_force_pass=all(row['strict_force_gate'] for row in fine['cases'] if row['count'] == 1025),
            implementation_checks_not_all_physical_accuracy_passes=True)
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), current_checks=sum(counts.values()), rehashed_files=len(cache), protected_changed=len(changed))),flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
