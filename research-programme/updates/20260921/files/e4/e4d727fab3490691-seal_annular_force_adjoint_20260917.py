from derive_annular_source_gravity_20260914 import EvidenceRun
from datetime import datetime,timezone
from pathlib import Path
import hashlib
import json
import re
import traceback


def main():
    root=Path(__file__).resolve().parents[1]
    intake=root/'source-intake/navier-stokes/20260914'
    destination=intake/'annular-force-adjoint-final-integrity.json'
    snapshot=intake/'annular-force-adjoint-resume-snapshot.md'
    executed=intake/'annular-force-adjoint-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Immutable evidence already exists.')
    report=dict(state='running',checks=[],inputs={},outputs={},full_GR_limit_proven=False,
        valid_for_physics_claim=False,continuum_limit_proven=False,uniform_time_bound=False,
        github_action=False,subagents_used=False,implementation_checks_not_physics_passes=True,
        original_action_unchanged=True,original_forward_trajectories_not_rerun=True,
        protected_scan_scope='mtime since turn start2026-09-17T14:22:07Z; not a pre-turn full hash baseline')
    cache={}

    def digest(path):
        path=path.resolve()
        if path not in cache:
            hasher=hashlib.sha256()
            with path.open('rb') as stream:
                while chunk:=stream.read(1024*1024):
                    hasher.update(chunk)
            cache[path]=hasher.hexdigest()
        return cache[path]

    def own(path,table='inputs'):
        report[table][str(path.resolve().relative_to(root))]=digest(path)

    def save():
        destination.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')

    def check(name,passed,detail=None):
        report['checks'].append(dict(name=name,passed=bool(passed),detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs','outputs']:
            for name,expected in status[table].items():
                path=(root/name).resolve()
                key=str(path.relative_to(root))
                if not path.is_file() or digest(path)!=expected:
                    raise RuntimeError('Missing or changed immutable file: '+name)
                if key in report['inputs'] and report['inputs'][key]!=expected:
                    raise RuntimeError('Conflicting immutable file: '+name)
                report['inputs'][key]=expected

    save()
    try:
        previous_path=intake/'annular-curvature-energy-final-integrity.json'
        previous=json.loads(previous_path.read_text())
        check('previous_seal_complete',previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        specifications=[('transpose','annular-matrix-free-adjoint-attempt01',73,12),
            ('inputs','annular-small-adjoint-inputs-attempt01',2,1),
            ('small','annular-force-adjoint-small-attempt01',12,2),
            ('small_tight','annular-force-adjoint-small-tight-attempt01',12,2),
            ('large','annular-force-adjoint-513-attempt01',10,2),
            ('large_tight','annular-force-adjoint-513-tight-attempt01',10,2),
            ('validation','annular-force-adjoint-validation-attempt01',26,4),
            ('relative','annular-relative-energy-attempt01',114,16),
            ('fronts','annular-curvature-fronts-attempt01',10,7),
            ('characteristic','annular-characteristic-source-attempt01',13,3),
            ('energy_gate','annular-characteristic-energy-gate-attempt01',8,1)]
        statuses,counts={},{}
        for name,label,count,cases in specifications:
            path=intake/label/'status.json'
            status=json.loads(path.read_text())
            json.dumps(status,allow_nan=False)
            check(name+'_complete',status['state']=='complete' and len(status['checks'])==count
                and len(status['cases'])==cases and all(row['passed'] for row in status['checks']))
            check(name+'_scope',not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['complete_parent_source_action_derived'] and status['original_action_unchanged']
                and not status['finite_future_trajectories_read'])
            inherit(status)
            own(path)
            statuses[name],counts[name]=status,count
        for name in ['small','small_tight','large','large_tight']:
            status=statuses[name]
            inputs={str(Path(path)) for path in status['inputs'] if Path(path).suffix.lower() in ['.npz','.npy']}
            check(name+'_isolated_inputs',not status['preexisting_forward_predictions_read']
                and inputs=={str(Path(path)) for path in status['npz_read_allowlist']} and len(inputs)==1
                and status['velocity_coordinate_adjoint_exactly_includes_off_solution_canonical_correction']
                and not status['full_GR_gate_upgraded'])
        validation=statuses['validation']
        check('all_full_horizon_terminal_dualities_pass',all(row['duality_error']<2e-9 for row in validation['cases'])
            and all(not row['physical_GR_claim'] for row in validation['cases'])
            and validation['only_terminal_04_force_not_entire_force_curve'])
        check('tighter_signed_term_controls_pass',len(validation['controls'])==4
            and all(row['total_change']<2e-10 and row['maximum_signed_term_change']<2e-10 for row in validation['controls']))
        check('freeze_before_forward_read',datetime.fromisoformat(validation['all_adjoint_outputs_verified_at'])
            <=datetime.fromisoformat(validation['forward_read_phase_started_at']))
        relative=statuses['relative']
        check('relative_energy_conditional_not_full_GR',relative['nonlinear_relative_energy_identity']
            and not relative['uniform_reference_regularities_established'] and not relative['nonlinear_full_GR_limit_proven']
            and relative['auxiliary_energy_shift_not_action_change'] and relative['finite_samples_only'])
        fronts=statuses['fronts']
        check('initial_corner_obstruction_and_front_hypothesis_explicit',fronts['initial_corner']['exact_defect']=='2/603'
            and not fronts['initial_corner']['C2_up_to_initial_source_corner_justified']
            and not fronts['finite_front_regularities_of_actual_solution_proven'])
        characteristic=statuses['characteristic']
        check('independent_characteristic_reference_failures_preserved',characteristic['prediction_frozen_before_spectral_comparison']
            and all(not row['force_comparison_within_previous_2e8_control'] for row in characteristic['cases'])
            and not characteristic['physical_GR_gate_upgraded'] and not characteristic['interval_certified_source_enclosure'])
        gate=statuses['energy_gate']
        check('analytic_energy_gate_not_numerical_interval_claim',gate['exact_rational_energy_gate']
            and gate['uses_continuum_energy_identity_not_sampled_speed_maximum']
            and not gate['interval_time_integration_performed'] and not gate['spectral_reference_regularity_certified'])
        check('earlier_failures_preserved',previous['inherited_failed_attempts_preserved']==25
            and previous['original_failed_cases_preserved'])
        note=root/'DERIVATION-20260917-time-dependent-force-adjoint-and-relative-energy.md'
        content=note.read_text(encoding='utf-8')
        cited=re.findall(r'`([^`\r\n]+\.(?:py|md|json))`',content)
        check('cited_note_paths_exist',all((root/name).is_file() for name in cited),cited)
        check('finished_note_scoped','PENDING' not in content and 'not the full GR limit' in content
            and '290 successful implementation checks' in content)
        own(note)
        names=['annular_matrix_free_adjoint_20260917.py','qualify_annular_matrix_free_adjoint_20260917.py',
            'prepare_annular_small_adjoint_20260917.py','run_annular_force_adjoint_20260917.py',
            'validate_annular_force_adjoint_20260917.py','annular_relative_hamiltonian_20260917.py',
            'qualify_annular_relative_energy_20260917.py','qualify_annular_curvature_fronts_20260917.py',
            'derive_annular_characteristic_source_20260917.py','derive_annular_characteristic_energy_gate_20260917.py',
            'seal_annular_force_adjoint_20260917.py']
        for name in names:
            path=root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_sources_compile',True,names)
        check('script_bytecode_cache_absent',not (root/'scripts/__pycache__').exists())
        protected=root.parent/'formalization-workbench'
        started=datetime(2026,9,17,14,22,7,tzinfo=timezone.utc).timestamp()
        changed=[str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime>=started]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('resume_and_executed_source_preserved',True)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),current_suite_checks=counts,
            total_successful_current_checks=sum(counts.values()),distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=25,new_failed_attempts_preserved=[],original_failed_cases_preserved=True,
            adjoint_results=validation['cases'],adjoint_controls=validation['controls'],relative_energy_results=relative['cases'],
            initial_corner_obstruction=fronts['initial_corner'],conditional_front_consistency_derived=True,
            characteristic_reference_comparisons=characteristic['cases'],analytic_source_energy_gate=gate['cases'],
            full_time_adjoint_terminal_output_qualified=True,conditional_nonlinear_relative_energy_derived=True,
            complete_force_curve_or_peak_qualified=False)
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),current_checks=sum(counts.values()),
            rehashed_files=len(cache),protected_changed=len(changed),failed_attempts_preserved=25)),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
