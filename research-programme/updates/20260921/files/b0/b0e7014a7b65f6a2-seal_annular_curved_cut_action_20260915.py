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
    destination = intake/'annular-curved-cut-action-final-integrity.json'
    snapshot = intake/'annular-curved-cut-action-resume-snapshot.md'
    executed = intake/'annular-curved-cut-action-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Preserve every previous executed attempt.')
    report = dict(state='running', checks=[], inputs={}, outputs={},
                  repaired_moving_curved_action_constructed=True,
                  physical_time_covariance_and_shift_variation_checked=True,
                  canonical_velocity_inversion_derived=True,
                  metric_covectors_checked_at_fixed_momenta=True,
                  moving_interface_Noether_term_required=True,
                  prescribed_background_evolution_completed=True,
                  live_repaired_gravity_evolution_completed=False,
                  conditional_bulk_mass_propagation_identity_derived=True,
                  source_cell_crossing_transfer_derived=False,
                  full_GR_limit_proven=False, valid_for_physics_claim=False,
                  unique_parent_boundary_selection_proven=False,
                  github_action=False, subagents_used=False,
                  resource_policy='At most two BelowNormal single-core numerical workers; no unrelated process changed.',
                  protected_scan_scope='mtime since2026-09-15T01:26:49Z, not a pre-turn content hash baseline.')

    def save():
        destination.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs', 'outputs']:
            for filename, expected in status[table].items():
                path = root/filename
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Missing or changed evidence: '+filename)
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Conflicting evidence hash: '+filename)
                report['inputs'][filename] = expected

    save()
    try:
        previous = intake/'annular-fixed-trace-final-integrity.json'
        old = json.loads(previous.read_text())
        check('previous_fixed_trace_seal_complete', old['state'] == 'complete'
              and all(row['passed'] for row in old['checks']))
        inherit(old)
        own(previous)
        statuses, counts = {}, {}
        for label, folder, count in [
            ('canonical_qualification', 'annular-covariant-cut-canonical-qualification-attempt02', 29),
            ('transport_current', 'annular-cut-transport-and-current-attempt01', 18),
            ('metric_inversion', 'annular-cut-metric-and-canonical-inversion-attempt01', 18),
            ('background_evolution', 'annular-cut-curved-background-evolution-attempt02', 46),
            ('interface_bound', 'annular-cut-interface-regular-limit-attempt01', 18)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            check(label+'_complete', status['state'] == 'complete' and len(status['checks']) == count
                  and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                  and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label], counts[label] = status, count
        warning_path = intake/'annular-covariant-cut-canonical-qualification-attempt01/status.json'
        warning = json.loads(warning_path.read_text())
        check('original_warning_run_preserved_separately', warning['state'] == 'complete' and len(warning['checks']) == 27)
        inherit(warning)
        own(warning_path)
        failure_path = intake/'annular-cut-curved-background-evolution-attempt01/status.json'
        failure = json.loads(failure_path.read_text())
        check('original_initial_data_failure_preserved', failure['state'] == 'failed'
              and any(not row['passed'] for row in failure['checks']))
        inherit(failure)
        own(failure_path)
        current = statuses['transport_current']
        check('nonzero_shift_and_moving_anchor_tested', current['finite_nonzero_shift_action_used']
              and current['moving_anchor_factor_retained'] and current['old_trace_multiplier_absent'])
        background = statuses['background_evolution']
        check('background_evolution_not_live_GR', len(background['cases']) == 10
              and not background['background_backreaction_evolved'] and not background['field_or_energy_projection']
              and not background['continuum_waveform_accuracy_qualified'])
        bound = statuses['interface_bound']
        check('interface_bound_not_crossing_theorem', bound['source_phase_margin'] == .2
              and not bound['uniform_near_cell_crossing_bound_proven'])
        scripts = [
            'annular_covariant_cut_action_20260915.py',
            'annular_covariant_cut_action_v2_20260915.py',
            'qualify_annular_covariant_cut_20260915.py',
            'qualify_annular_covariant_cut_v2_20260915.py',
            'verify_annular_cut_transport_current_20260915.py',
            'verify_annular_cut_metric_and_inversion_20260915.py',
            'run_annular_cut_curved_background_20260915.py',
            'annular_cut_initial_data_20260915.py',
            'run_annular_cut_curved_background_v2_20260915.py',
            'verify_annular_cut_interface_regular_limit_20260915.py',
            'seal_annular_curved_cut_action_20260915.py']
        for filename in scripts:
            path = root/'scripts'/filename
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('eleven_sources_compile_without_bytecode', True)
        executed.write_bytes(Path(__file__).read_bytes())
        own(executed, 'outputs')
        note = root/'DERIVATION-20260915-moving-curved-cut-action-and-canonical-current.md'
        document = note.read_text(encoding='utf-8')
        cited = [root/value for value in re.findall(r'\x60([^\x60]+)\x60', document)
                 if value.endswith(('.md', '.py', '.json', '.npz', '.csv'))]
        check('every_local_document_citation_exists', bool(cited) and all(path.is_file() for path in cited), len(cited))
        check('no_pending_result_marker', not re.search(r'[A-Z_]*RESULTS_PENDING', document))
        for path in cited:
            own(path)
        own(note, 'outputs')
        protected = root.parent/'formalization-workbench'
        check('protected_workbench_exists', protected.is_dir())
        started = datetime.fromisoformat('2026-09-15T01:26:49+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        check('no_script_bytecode_cache', not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot, 'outputs')
        report.update(state='complete', validation_counts=counts, total_current_validation_checks=sum(counts.values()),
                      historical_warning_checks_not_added_to_total=27,
                      failure_passed_setup_checks=sum(row['passed'] for row in failure['checks']),
                      finest_background_cases=[row for row in background['cases'] if row['count'] == 65],
                      interface_energy_order=bound['energy_order'], interface_force_order=bound['force_order'],
                      protected_changed_count=len(changed), completed_at=datetime.now(timezone.utc).isoformat())
        save()
        print(json.dumps(dict(state=report['state'], integrity_checks=len(report['checks']),
                              validation_counts=counts, total_current_validation_checks=sum(counts.values()),
                              distinct_files=len(set(report['inputs']) | set(report['outputs'])),
                              protected_changed_count=len(changed))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
