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
    destination = intake/'annular-P2-tight-error-budget-final-integrity.json'
    snapshot = intake/'annular-P2-tight-error-budget-resume-snapshot.md'
    executed = intake/'annular-P2-tight-error-budget-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Immutable evidence destination already exists.')
    report = dict(state='running',checks=[],inputs={},outputs={},
        primitive_radial_representation_qualified=True, physical_action_and_Gram_rows_unchanged=True,
        numerical_error_budget_not_new_physical_fit=True, short_coupled_evolution=True,
        full_live_P2_force_convergence_proven=False, full_GR_limit_proven=False,
        unique_parent_shift_extension_proven=False, valid_for_physics_claim=False,
        independently_reviewed_proof=False, no_GitHub_action=True, subagents_used=False,
        protected_scan_scope='mtime since2026-09-18T17:51:50Z; not a pre-turn full hash baseline')
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

    def inherit(path):
        status=json.loads(path.read_text())
        for table in ['inputs','outputs']:
            for name,expected in status[table].items():
                source=(root/name).resolve()
                key=str(source.relative_to(root))
                if not source.is_file() or digest(source)!=expected:
                    raise RuntimeError('Missing or modified sealed source: '+name)
                if key in report['inputs'] and report['inputs'][key]!=expected:
                    raise RuntimeError('Conflicting sealed hash: '+name)
                report['inputs'][key]=expected
        own(path)
        return status

    save()
    try:
        previous=inherit(intake/'annular-live-P2-current-final-integrity.json')
        check('previous_complete_seal_and_hash_chain',previous['state']=='complete'
            and all(row['passed'] for row in previous['checks']))
        check('all_inherited_failures_retained',previous['inherited_failed_attempts_preserved']==33
            and previous['inherited_peak_force_failures_preserved']==4)
        statuses={}
        for name,count in [('annular-P2-evolved-radial-budget-attempt01',35),
                ('annular-P2-tight-budget-reference-attempt01',21),('annular-P2-tight-budget-MTS-attempt01',21),
                ('annular-P2-readout-error-budget-attempt01',22)]:
            status=inherit(intake/name/'status.json')
            statuses[name]=status
            check(name+'_complete',status['state']=='complete' and len(status['checks'])==count
                and all(row['passed'] for row in status['checks']))
            check(name+'_private_nonclaim_scope',not status['valid_for_physics_claim'] and not status['full_GR_limit_proven']
                and not status['github_action'] and not status['subagents_used'] and not status['full_live_P2_force_convergence_proven'])
        radial=statuses['annular-P2-evolved-radial-budget-attempt01']
        expected={(branch,*config) for branch in ['reference','MTS'] for config in
            [('old',18,20,12),('old',24,20,12),('primitive',18,20,12),('primitive',24,20,12),('primitive',18,32,16)]}
        actual={(row['branch'],row['method'],row['radial_degree'],row['action_order'],row['label_order']) for row in radial['cases']}
        check('both_branches_all_five_same_state_configurations',actual==expected)
        check('derivative_is_actual_profile_derivative_not_an_ODE_substitute',
            radial['derivative_not_replaced_by_ODE_at_query_point'] and radial['saved_canonical_states_unchanged']
            and radial['equations_and_physical_action_unchanged']
            and all(row['derivative_is_derivative_of_reported_geometry']<2e-12 for row in radial['cases']))
        check('old_high_order_worsening_recorded',all(row['mass_error']>2e-7 for row in radial['cases']
            if row['method']=='old' and row['radial_degree']==24))
        check('tight_radial_primitive_and_original_collocation_solution',all(
            max(row['mass_error'],row['lapse_error'])<2e-9 and row['dense_output_node_change']<2e-13
            for row in radial['cases'] if row['method']=='primitive'))
        for branch in ['reference','MTS']:
            status=statuses['annular-P2-tight-budget-'+branch+'-attempt01']
            check(branch+'_matched_time_and_material_configs',
                {(row['mode'],row['layer_degree'],row['maximum_step']) for row in status['cases']}
                =={('principal',14,.0005),('half_step',14,.00025),('label_refined',18,.0005)}
                and all(row['radial_degree']==18 and row['action_order']==32 and row['label_order']==20
                    and row['duration']==.004 and row['rtol']==2e-12 and row['atol']==2e-14 for row in status['cases']))
            check(branch+'_full_short_interval_and_tight_gates',all(row['success'] and row['mass_drift']<2e-11
                and max(row['final_radial_residual'])<2e-9 for row in status['cases'])
                and all(max(row.values())<2e-9 for row in status['refinement_comparisons'].values()))
            check(branch+'_independent_current_retained',all(max(item['error'] for item in row['final_current'])<2e-9
                and max(item['on_shell_error'] for item in row['final_current'])<2e-9
                for row in status['cases'] if row['mode']=='principal'))
            check(branch+'_no_projection_or_physics_upgrade',status['no_mass_current_or_force_projection']
                and status['physical_action_and_Gram_rows_unchanged'] and not status['unique_parent_shift_extension_proven']
                and not status['continuum_accuracy_or_long_horizon_proven'])
        readout=statuses['annular-P2-readout-error-budget-attempt01']
        check('paired_saved_state_readout_budgets_not_continuum_upgrade',
            readout['same_saved_states_no_refitting'] and readout['canonical_source_force_not_proper_acceleration']
            and readout['readout_refinement_not_continuum_force_comparison']
            and {(row['branch'],row['mode']) for row in readout['cases']}
                =={(branch,mode) for branch in ['reference','MTS'] for mode in ['half_step','label_refined']}
            and all(max(row['canonical_source_force_difference'],row['total_radial_density_difference'],row['proper_clock_rate_difference'])<2e-8
                for row in readout['cases']))
        old=inherit(intake/'annular-initial-corner-response-final-integrity.json')
        check('four_original_force_gates_remain_failed',len(old['comparison_results'])==4
            and all(not row['original_peak_force_gate_pass'] for row in old['comparison_results']))
        note=root/'DERIVATION-20260918-P2-primitive-radial-repair-and-tight-error-budget.md'
        content=note.read_text(encoding='utf-8')
        cited=re.findall(r'`([^`\r\n]+\.(?:py|md|json))`',content)
        check('all_cited_local_paths_exist',bool(cited) and all((root/name).is_file() for name in cited),cited)
        check('note_complete_and_scope_explicit','99 successful implementation checks' in content
            and 'will be filled' not in content and 'PENDING' not in content
            and 'not an isolated estimate' in content and 'No additional physical interval is deleted' in content)
        own(note)
        names=['annular_P2_primitive_geometry_20260918.py','diagnose_annular_P2_evolved_radial_budget_20260918.py',
            'run_annular_P2_tight_error_budget_20260918.py','qualify_annular_P2_readout_error_budget_20260918.py',
            'seal_annular_P2_tight_error_budget_20260918.py']
        for name in names:
            path=root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_sources_compile_without_bytecode',not (root/'scripts/__pycache__').exists(),names)
        protected=root.parent/'formalization-workbench'
        timestamp=datetime(2026,9,18,17,51,50,tzinfo=timezone.utc).timestamp()
        changed=[str(path.relative_to(protected)) for path in protected.rglob('*')
            if path.is_file() and path.stat().st_mtime>=timestamp]
        check('protected_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('resume_and_executed_sealer_snapshots_saved',True)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),
            total_successful_current_checks=99,distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=33,inherited_peak_force_failures_preserved=4,
            new_failed_attempts_preserved=[],results={name:status['cases'] for name,status in statuses.items()})
        save()
        print(json.dumps(dict(state='complete',integrity_checks=len(report['checks']),current_checks=99,
            rehashed_files=len(cache),protected_changed=len(changed),failed_attempts_preserved=33)),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
