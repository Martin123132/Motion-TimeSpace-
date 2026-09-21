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
    destination = intake/'annular-P2-joint-refinement-final-integrity.json'
    snapshot = intake/'annular-P2-joint-refinement-resume-snapshot.md'
    executed = intake/'annular-P2-joint-refinement-executed-sealer.py'
    table = intake/'annular-P2-joint-refinement-initial-results.csv'
    if any(path.exists() for path in [destination, snapshot, executed, table]):
        raise FileExistsError('Immutable seal destination already exists.')
    report = dict(state='running', checks=[], inputs={}, outputs={}, github_action=False, subagents_used=False,
        full_GR_limit_proven=False, valid_for_physics_claim=False, full_live_P2_force_convergence_proven=False,
        no_new_live_nonlinear_trajectory=True, frozen_solver_not_full_coupled_integrator=True,
        protected_scan_scope='mtime since2026-09-18T23:00:41Z; not a pre-turn full hash baseline')
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
        previous = inherit(intake/'annular-P2-force-lift-final-integrity.json')
        check('previous_complete_and_preserved', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        check('all_previous_failures_preserved', previous['inherited_failed_attempts_preserved'] == 33
            and previous['inherited_peak_force_failures_preserved'] == 4
            and previous['inherited_short_horizon_scientific_failures_preserved'] == 6
            and previous['new_initial_combined_force_failures'] == 4)
        failed = []
        for attempt in ['01', '02', '03']:
            name = 'annular-P2-graded-source-algebra-attempt'+attempt
            status = inherit(intake/name/'status.json')
            check(name+'_failure_retained', status['state'] == 'failed' and bool(status['error']))
            failed.append(name)
        names = ['annular-P2-graded-source-algebra-attempt04', 'annular-P2-source-corner-scale-attempt01',
            'annular-P2-joint-refinement-129-cap4e-05-attempt01', 'annular-P2-joint-refinement-257-cap4e-05-attempt01',
            'annular-P2-joint-refinement-257-cap2e-05-attempt01', 'annular-P2-frozen-modal-step-attempt01']
        statuses = {}
        for name in names:
            status = inherit(intake/name/'status.json')
            statuses[name] = status
            check(name+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            check(name+'_nonclaim_scope', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['full_live_P2_force_convergence_proven'] and not status['github_action'] and not status['subagents_used'])
        comparison = inherit(intake/'annular-P2-continuum-comparison-65-attempt01/status.json')
        peak = comparison['independent_oracle']['force_peak_scale']
        gate = min(comparison['gates']['sampled_force_absolute'], comparison['gates']['sampled_force_peak_relative']*peak)
        check('gate_scale_sourced_not_new_fit', peak == 5.401196245463084e-6)
        initial = []
        for name, status in statuses.items():
            if not name.startswith('annular-P2-joint-refinement-'):
                continue
            check(name+'_paired_and_no_evolution', len(status['cases']) == 2
                and {row['branch'] for row in status['cases']} == {'reference', 'MTS'} and status['no_forward_evolution'])
            for row in status['cases']:
                schur, law = row['schur'], row['mass_law']
                projection, inertia = schur['field_projection_inertia'], schur['dust_inertia']
                drive = law['local_corner_forcing']
                wave_drive = drive-schur['dust_drive']/inertia
                remainder = schur['free_wave_drive']+projection*wave_drive
                predicted = (-projection*drive+remainder)/(1+projection/inertia)
                bound = (projection*abs(drive)+abs(remainder))/(1+projection/inertia)
                bound += abs(row['force']-row['force_error_from_continuum'])
                check(name+'_'+row['branch']+'_Schur_remainder_decomposition', abs(predicted-row['force']) < 2e-10)
                initial.append(dict(branch=row['branch'], base_count=row['base_count'], source_cap=row['source_cap'],
                    scalar_nodes=row['scalar_nodes'], initial_force_error=row['force_error_from_continuum'],
                    combined_force_threshold=gate, initial_combined_gate_pass=row['initial_combined_gate_pass'],
                    source_inertia_drive=-projection*drive/(1+projection/inertia),
                    remaining_action_drive=remainder/(1+projection/inertia), no_cancellation_initial_bound=bound,
                    no_cancellation_initial_gate_pass=bound <= gate,
                    local_source_prediction=law['leading_source_force_prediction'], source_near_lift_work=row['source_near_work'],
                    omega_max=row['spectral']['maximum_angular_frequency'], measured_RHS_seconds=row['rhs_seconds'],
                    frozen_explicit_full_window_hours=row['spectral_cost']['0.004']['optimistic_RHS_seconds']/3600,
                    evolved_accuracy_claim=False, valid_for_claim=False,
                    source_path=str((intake/name/'status.json').relative_to(root))))
        selected = [row for row in initial if row['base_count'] == 257]
        check('both257_grids_qualify_initial_only_without_cancellation', len(selected) == 4
            and all(row['initial_combined_gate_pass'] and row['no_cancellation_initial_gate_pass'] for row in selected))
        coarse_mts = [row for row in initial if row['base_count'] == 129 and row['branch'] == 'MTS']
        check('coarse_MTS_failure_not_erased', len(coarse_mts) == 1 and not coarse_mts[0]['initial_combined_gate_pass'])
        modal = statuses['annular-P2-frozen-modal-step-attempt01']
        check('modal_control_is_not_live_evolution', modal['no_live_nonlinear_forward_evolution']
            and modal['source_velocity_set_zero_for_fixture'] and modal['not_the_actual_moving_source_trajectory']
            and modal['all_frozen_scalar_modes_retained'] and len(modal['cases']) == 2)
        reference = next(row for row in statuses['annular-P2-joint-refinement-257-cap4e-05-attempt01']['cases'] if row['branch'] == 'reference')
        slope = -2*6.03**2*.01**2*reference['mass_law']['local_corner_forcing']
        oracle = json.loads((intake/'annular-P2-continuum-comparison-65-attempt01/reference-65.json').read_text())
        own(intake/'annular-P2-continuum-comparison-65-attempt01/reference-65.json')
        corner = [dict(time=row['time'], leading_force=slope*row['time'], continuum_force=row['continuum_wave_force'],
            difference=slope*row['time']-row['continuum_wave_force']) for row in oracle['times']]
        report.update(curved_corner_slope=slope, curved_corner_saved_comparison=corner,
            initial_results=initial, modal_results=modal['cases'])
        with table.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(initial[0]))
            writer.writeheader()
            writer.writerows(initial)
        with table.open(encoding='utf-8', newline='') as stream:
            parsed = list(csv.DictReader(stream))
        check('CSV_parses_and_claim_scope_is_false', len(parsed) == 6 and all(None not in row
            and (root/row['source_path']).is_file() and row['valid_for_claim'] == 'False' for row in parsed))
        own(table, 'outputs')
        note = root/'DERIVATION-20260919-joint-source-refinement-and-inertial-force-scale.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json|csv))`', content)
        check('cited_local_paths_exist', bool(cited) and all((root/name).is_file() for name in cited), cited)
        check('final_note_preserves_limits', 'Pending' not in content and 'in progress' not in content
            and 'not an evolved force pass' in content and 'full-horizon force gates remain open' in content)
        own(note)
        sources = ['annular_P2_graded_source_20260919.py', 'annular_P2_graded_embedding_20260919.py',
            'annular_P2_graded_embedding_exact_20260919.py', 'verify_annular_P2_graded_source_20260919.py',
            'verify_annular_P2_graded_source_v2_20260919.py', 'verify_annular_P2_graded_source_v3_20260919.py',
            'verify_annular_P2_graded_source_v4_20260919.py', 'probe_annular_P2_joint_refinement_20260919.py',
            'derive_annular_P2_source_corner_scale_20260919.py', 'verify_annular_P2_frozen_modal_step_20260919.py',
            'seal_annular_P2_joint_refinement_20260919.py']
        for name in sources:
            path = root/'scripts'/name
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('all_sources_compile_without_bytecode', not (root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        start = datetime(2026, 9, 18, 23, 0, 41, tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime >= start]
        check('protected_mtime_changed_file_count_zero', not changed, changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot, 'outputs')
        own(executed, 'outputs')
        report.update(state='complete', completed_at=datetime.now(timezone.utc).isoformat(),
            successful_current_implementation_checks=sum(len(status['checks']) for status in statuses.values()),
            inherited_failed_attempts_preserved=33, new_failed_attempts_preserved=failed, total_failed_attempts_preserved=36,
            inherited_peak_force_failures_preserved=4, inherited_short_horizon_scientific_failures_preserved=6,
            inherited_initial_force_failures_preserved=4, new_initial_gate_failures=1,
            distinct_files_rehashed=len(cache))
        save()
        print(json.dumps(dict(state='complete', integrity_checks=len(report['checks']),
            implementation_checks=report['successful_current_implementation_checks'], files_rehashed=len(cache),
            retained_new_failed_attempts=len(failed), new_initial_gate_failures=1)), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    main()
