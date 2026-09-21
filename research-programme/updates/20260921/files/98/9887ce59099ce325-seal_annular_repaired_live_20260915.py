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
    destination = intake/'annular-repaired-live-final-integrity.json'
    snapshot = intake/'annular-repaired-live-resume-snapshot.md'
    executed = intake/'annular-repaired-live-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Do not overwrite an executed seal or snapshot.')
    report = dict(state='running', checks=[], inputs={}, outputs={},
                  repaired_live_canonical_spherical_evolution_completed=True,
                  continuous_width_density_before_metric_products=True,
                  independent_temporal_current_tested=True,
                  independent_GR_dust_and_prescribed_background_controls=True,
                  failed_method_attribution_preserved=True,
                  current_error_radial_refinement_diagnosed=True,
                  full_GR_limit_proven=False, valid_for_physics_claim=False,
                  evolving_continuum_waveform_accuracy_proven=False,
                  complete_parent_source_action_derived=False,
                  source_cell_crossing_transfer_derived=False,
                  exact_finite_label_Galerkin_closure_claimed=False,
                  github_action=False, subagents_used=False,
                  resource_policy='At most two BelowNormal single-core numerical workers; all numerical jobs finished before sealing.',
                  protected_scan_scope='mtime since2026-09-15T02:14:04Z; not a pre-turn content-hash baseline.')
    hash_cache = {}

    def digest(path):
        path = path.resolve()
        if path not in hash_cache:
            value = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(1024*1024):
                    value.update(chunk)
            hash_cache[path] = value.hexdigest()
        return hash_cache[path]

    def own(path, table='inputs'):
        report[table][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs', 'outputs']:
            for filename, expected in status[table].items():
                path = (root/filename).resolve()
                path.relative_to(root)
                if not path.is_file() or digest(path) != expected:
                    raise RuntimeError('Missing or changed executed evidence: '+filename)
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Conflicting inherited hashes: '+filename)
                report['inputs'][filename] = expected

    save()
    try:
        previous_path = intake/'annular-curved-cut-action-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_repaired_action_seal_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses, counts = {}, {}
        for label, folder, count in [
                ('snapshot', 'annular-repaired-live-geometry-attempt01', 15),
                ('initial_current', 'annular-repaired-live-current-attempt01', 8),
                ('evolution', 'annular-repaired-live-evolution-attempt01', 81),
                ('action_controls', 'annular-repaired-live-controls-attempt01', 20),
                ('radial_transport', 'annular-repaired-radial-transport-attempt01', 17)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            check(label+'_complete', status['state'] == 'complete' and len(status['checks']) == count and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                  and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label], counts[label] = status, count
        failed_path = intake/'annular-repaired-live-method-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        check('wrong_material_error_hypothesis_retained_failed', failed['state'] == 'failed'
              and failed['checks'][-1]['name'] == 'reference_deformed_material_current_refines'
              and not failed['checks'][-1]['passed'])
        inherit(failed)
        own(failed_path)
        check('sixteen_trajectories_no_projection_fixed_width', len(statuses['evolution']['cases']) == 16
              and not statuses['evolution']['energy_or_state_projection']
              and statuses['evolution']['finite_source_width_held_fixed']
              and not statuses['evolution']['continuum_waveform_accuracy_qualified'])
        check('independent_current_not_defined_from_radial_equation', statuses['initial_current']['live_repaired_canonical_tangent_tested']
              and not statuses['initial_current']['current_from_differentiated_radial_constraint']
              and not statuses['initial_current']['current_imposed_or_energy_projected'])
        check('nonaffine_overlap_and_interface_negative_controls', statuses['action_controls']['nonaffine_source_and_overlapping_supports_tested']
              and statuses['action_controls']['moving_interface_omission_negative_control'])
        check('error_diagnosis_did_not_change_equations', statuses['radial_transport']['matter_and_gravity_equations_unchanged']
              and statuses['radial_transport']['original_wrong_error_attribution_retained_as_failed'])
        check('finite_label_variational_claim_absent', statuses['initial_current']['material_label_collocation_not_exact_variational_truncation'])
        note = root/'DERIVATION-20260915-repaired-live-canonical-geometry-and-current.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`', content)
        check('all_note_source_paths_exist', all((root/name).is_file() for name in cited), cited)
        check('no_pending_numerical_results_in_note', 'RESULTS_PENDING' not in content)
        own(note)
        source_names = ['annular_repaired_live_geometry_20260915.py', 'annular_repaired_live_current_20260915.py',
                        'qualify_annular_repaired_live_geometry_20260915.py', 'qualify_annular_repaired_live_current_20260915.py',
                        'run_annular_repaired_live_evolution_20260915.py', 'verify_annular_repaired_live_controls_20260915.py',
                        'verify_annular_repaired_live_method_20260915.py', 'verify_annular_repaired_radial_transport_20260915.py',
                        'seal_annular_repaired_live_20260915.py']
        for name in source_names:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('nine_new_modules_compile_without_bytecode', True)
        check('script_bytecode_cache_absent', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026, 9, 15, 2, 14, 4, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= started]
        check('protected_workbench_mtime_changed_count_zero', len(changed) == 0, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        check('immutable_resume_and_executed_sealer_saved', snapshot.is_file() and executed.is_file())
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
                      successful_current_suite_checks=counts, total_successful_current_checks=sum(counts.values()),
                      failed_hypothesis_suite_count=1, distinct_files_rehashed=len(hash_cache),
                      next_target='Derive continuum moving-boundary radiation/source force, then independent nonzero-wave GR benchmark at fixed source width; no continuum force claim from conservation alone.')
        save()
        print(json.dumps(dict(state=report['state'], checks=len(report['checks']), current_checks=report['total_successful_current_checks'],
                              distinct_files_rehashed=report['distinct_files_rehashed'], protected_changed=len(changed))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
