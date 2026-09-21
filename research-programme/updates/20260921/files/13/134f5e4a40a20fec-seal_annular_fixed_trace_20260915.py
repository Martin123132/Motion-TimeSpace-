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
    intake = root / 'source-intake/navier-stokes/20260914'
    destination = intake / 'annular-fixed-trace-final-integrity.json'
    snapshot = intake / 'annular-fixed-trace-resume-snapshot.md'
    executed = intake / 'annular-fixed-trace-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Preserve every previous executed attempt.')
    report = dict(state='running', checks=[], inputs={}, outputs={},
                  paired_nonzero_scalar_source_live_gravity_evolved=True,
                  affine_candidate_local_current_gate_failed=True,
                  fixed_trace_local_conservation_qualified=True,
                  fixed_trace_accurate_boundary_force_qualified=False,
                  reference_static_cut_cell_pressure_derived=True,
                  reference_flat_cut_cell_kinetic_action_derived=True,
                  static_MTS_Gram_interface_lift_candidate_derived=True,
                  unique_parent_boundary_selection_proven=False,
                  full_MTS_Gram_boundary_completion_derived=False,
                  curved_cut_cell_current_derived=False,
                  source_cell_crossing_transfer_derived=False,
                  complete_parent_source_action_derived=False,
                  full_GR_limit_proven=False, valid_for_physics_claim=False,
                  github_action=False, subagents_used=False,
                  resource_policy='At most two BelowNormal single-core numerical workers; no unrelated process changed.',
                  protected_scan_scope='mtime since2026-09-14T23:36:22Z, not a pre-turn content hash baseline.')

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
                path = root / filename
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Missing or changed evidence: '+filename)
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Conflicting evidence hash: '+filename)
                report['inputs'][filename] = expected

    save()
    try:
        previous = intake / 'annular-source-gravity-final-integrity.json'
        old = json.loads(previous.read_text())
        check('previous_source_gravity_seal_complete', old['state'] == 'complete'
              and all(row['passed'] for row in old['checks']))
        inherit(old)
        own(previous)
        entries = [
            ('trace_qualification', 'annular-fixed-grid-moving-trace-qualification-attempt01', 6),
            ('added_action_clock', 'annular-fixed-trace-action-and-clock-attempt01', 12),
            ('independent_controls', 'annular-fixed-trace-independent-controls-attempt01', 15),
            ('affine_obstruction', 'annular-affine-moving-current-obstruction-attempt01', 9),
            ('stencil_evolution', 'annular-fixed-grid-moving-trace-evolution-attempt01', 50),
            ('smooth_evolution', 'annular-fixed-grid-moving-trace-smooth-evolution-attempt01', 50),
            ('evolution_comparison', 'annular-fixed-trace-evolution-comparison-attempt01', 12),
            ('static_force_audit', 'annular-trace-static-force-phase-audit-attempt01', 38),
            ('reference_cut_cell_kinetics', 'annular-reference-cut-cell-kinetics-attempt01', 16),
            ('MTS_static_interface_lift', 'annular-Gram-interface-lift-static-attempt01', 40)]
        statuses, counts = {}, {}
        for label, folder, count in entries:
            path = intake / folder / 'status.json'
            status = json.loads(path.read_text())
            check(label+'_complete', status['state'] == 'complete' and len(status['checks']) == count
                  and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false', not status['full_GR_limit_proven']
                  and not status['complete_parent_source_action_derived'] and not status['valid_for_physics_claim'])
            inherit(status)
            own(path)
            statuses[label], counts[label] = status, count
        failure_path = intake / 'annular-moving-live-gravity-qualification-attempt01/status.json'
        failure = json.loads(failure_path.read_text())
        check('failed_affine_local_current_preserved', failure['state'] == 'failed'
              and any(not row['passed'] for row in failure['checks']))
        inherit(failure)
        own(failure_path)
        verdict = statuses['static_force_audit']['verdict']
        check('both_interpolated_trace_force_failures_explicit', all(
            not verdict[branch+'_interpolated_trace']['passes_half_percent_pressure_gate']
            for branch in ['reference', 'MTS']))
        check('reference_cut_cell_static_repair_qualified',
              verdict['reference_cut_cell_reference_correction']['passes_half_percent_pressure_gate'])
        check('reference_repair_not_mislabeled_full_MTS_repair',
              not statuses['reference_cut_cell_kinetics']['full_MTS_Gram_boundary_completion_derived']
              and not statuses['reference_cut_cell_kinetics']['curved_time_link_and_metric_current_derived'])
        check('two_independent_initial_data_series_no_energy_projection', all(
            len(statuses[label]['cases']) == 8 and not statuses[label]['conservation_or_trace_position_projection']
            for label in ['stencil_evolution', 'smooth_evolution']))
        check('refinement_not_independent_continuum_accuracy',
              not statuses['evolution_comparison']['standalone_continuum_waveform_accuracy_qualified'])
        check('MTS_static_lift_not_parent_or_dynamic_completion',
              statuses['MTS_static_interface_lift']['original_boundary_action_changed_explicitly']
              and not statuses['MTS_static_interface_lift']['unique_parent_boundary_selection_proven']
              and not statuses['MTS_static_interface_lift']['arbitrary_dynamic_MTS_boundary_completion_derived'])
        scripts = [
            'annular_moving_live_gravity_20260914.py',
            'qualify_annular_moving_live_gravity_20260914.py',
            'annular_fixed_grid_moving_trace_20260914.py',
            'qualify_annular_fixed_grid_moving_trace_20260914.py',
            'run_annular_fixed_grid_moving_trace_20260914.py',
            'verify_annular_fixed_trace_action_20260914.py',
            'verify_annular_fixed_trace_controls_20260914.py',
            'diagnose_annular_affine_current_20260914.py',
            'annular_smooth_trace_preparation_20260914.py',
            'run_annular_fixed_trace_smooth_20260914.py',
            'compare_annular_fixed_trace_evolution_20260914.py',
            'audit_annular_trace_static_force_20260914.py',
            'derive_annular_reference_cut_cell_kinetics_20260915.py',
            'derive_annular_Gram_interface_lift_20260915.py',
            'seal_annular_fixed_trace_20260915.py']
        for filename in scripts:
            path = root / 'scripts' / filename
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('fifteen_sources_compile_without_bytecode', True)
        executed.write_bytes(Path(__file__).read_bytes())
        own(executed, 'outputs')
        note = root / 'DERIVATION-20260914-consistent-moving-trace-and-live-wave-gravity.md'
        document = note.read_text(encoding='utf-8')
        cited = [root/value for value in re.findall(r'\x60([^\x60]+)\x60', document)
                 if value.endswith(('.md', '.py', '.json', '.npz', '.csv'))]
        check('every_local_document_citation_exists', bool(cited) and all(path.is_file() for path in cited), len(cited))
        check('no_pending_result_marker', not re.search(r'[A-Z_]*RESULTS_PENDING', document))
        for path in cited:
            own(path)
        own(note, 'outputs')
        protected = root.parent / 'formalization-workbench'
        check('protected_workbench_exists', protected.is_dir())
        started = datetime.fromisoformat('2026-09-14T23:36:22+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        check('no_script_bytecode_cache', not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot, 'outputs')
        report.update(state='complete', validation_counts=counts, total_validation_checks=sum(counts.values()),
                      failure_passed_setup_checks=sum(row['passed'] for row in failure['checks']),
                      force_verdict=verdict,
                      finest_smooth_cases=[row for row in statuses['smooth_evolution']['cases'] if row['count'] == 129],
                      refinement=statuses['evolution_comparison']['refinements'],
                      protected_changed_count=len(changed), completed_at=datetime.now(timezone.utc).isoformat())
        save()
        print(json.dumps(dict(state=report['state'], integrity_checks=len(report['checks']),
                              validation_counts=counts, total_validation_checks=sum(counts.values()),
                              distinct_files=len(set(report['inputs']) | set(report['outputs'])),
                              protected_changed_count=len(changed))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
