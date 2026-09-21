import hashlib
import json
import re
import traceback
from datetime import datetime,timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    root=Path(__file__).resolve().parents[1]
    intake=root/'source-intake/navier-stokes/20260914'
    destination=intake/'annular-compatible-h-evolution-final-integrity.json'
    snapshot=intake/'annular-compatible-h-evolution-resume-snapshot.md'
    executed=intake/'annular-compatible-h-evolution-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Preserve executed and attempted evidence.')
    report={'state':'running','checks':[],'inputs':{},'outputs':{},'historical_attempts':[],
            'full_GR_limit_proven':False,'uniform_H3_solution_bound_proven':False,
            'uniform_in_h_dynamical_energy_estimate_proven':False,'valid_for_physics_claim':False,
            'exact_energy_rate_and_local_product_identities_derived':True,
            'actual_data_energy_geometry_bound_derived':True,
            'stationary_source_only':True,'h_refined_dynamical_smoke_verified':False,
            'protected_scan_scope':'mtime since2026-09-14T01:19:42Z,not pre-turn content hashes',
            'github_action':False,'subagents_used':False}

    def save():
        destination.write_text(json.dumps(report,indent=2)+'\n')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    save()
    try:
        for label,directory in [('main','annular-compatible-h-evolution-main-attempt01'),
                                ('independent','annular-compatible-h-evolution-independent-attempt01')]:
            path=intake/directory/'status.json'
            status=json.loads(path.read_text())
            check(label+'_complete',status['state']=='complete' and len(status['cases'])==6 and all(row['passed'] for row in status['checks']))
            check(label+'_claim_gates_false',not any(status[key] for key in
                  ['full_GR_limit_proven','uniform_H3_solution_bound_proven','uniform_in_h_dynamical_energy_estimate_proven','valid_for_physics_claim']))
            for table in ['inputs','outputs']:
                for filename,expected in status[table].items():
                    source=root/filename
                    if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed source/evidence: '+filename)
                    report['inputs'][filename]=expected
            own(path)
            report[label+'_checks']=len(status['checks'])
            if label=='main':
                report['observed_orders']=status['orders']
        check('all_current_and_inherited_hashes_match',True)
        balance_path=intake/'annular-augmented-error-balance-attempt01/status.json'
        balance=json.loads(balance_path.read_text())
        check('augmented_error_balance_replay_complete',balance['state']=='complete' and len(balance['cases'])==9
              and all(row['passed'] for row in balance['checks']))
        check('augmented_replay_does_not_claim_uniform_estimate',not any(balance[key] for key in
              ['uniform_relative_energy_estimate_proven','full_GR_limit_proven','valid_for_physics_claim']))
        for table in ['inputs','outputs']:
            for filename,expected in balance[table].items():
                if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed augmented-balance evidence: '+filename)
                report['inputs'][filename]=expected
        own(balance_path)
        report['augmented_balance_checks']=len(balance['checks'])
        for suffix,expected_state in [('pilot-attempt01','failed'),('pilot-attempt02','failed'),('pilot-attempt03','complete')]:
            path=intake/('annular-compatible-h-evolution-'+suffix)/'status.json'
            status=json.loads(path.read_text())
            check(suffix+'_preserved_with_correct_status',status['state']==expected_state)
            report['historical_attempts'].append({'path':str(path.relative_to(root)),'state':status['state'],'error':status.get('error')})
            own(path)
            for table in ['inputs','outputs']:
                for filename,expected in status[table].items():
                    source=root/filename
                    if hashlib.sha256(source.read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed attempted evidence: '+filename)
                    report['inputs'][filename]=expected
        stems=['annular_compatible_h_evolution','annular_gram_velocity_commutator',
               'run_annular_compatible_h_evolution','run_annular_compatible_h_evolution_v2',
               'run_annular_compatible_h_evolution_v3','verify_annular_compatible_h_evolution',
               'seal_annular_compatible_h_evolution','replay_annular_augmented_error_balance']
        for stem in stems:
            path=root/'scripts'/(stem+'_20260914.py')
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('all_eight_new_and_attempted_scripts_compile_without_bytecode',True)
        executed.write_bytes(Path(__file__).read_bytes())
        own(executed,'outputs')
        note=root/'DERIVATION-20260914-boundary-compatible-h-evolution.md'
        for citation in re.findall(r'\x60([^\x60]+)\x60',note.read_text(encoding='utf-8')):
            if citation.endswith(('.py','.md','.json','.npz')):
                check('cited_source_exists_'+citation,(root/citation).is_file())
        own(note,'outputs')
        protected=root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        start=datetime.fromisoformat('2026-09-14T01:19:42+00:00').timestamp()
        changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>start]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        check('no_python_cache',not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update(state='complete',h_refined_dynamical_smoke_verified=True,
                      protected_changed_count=len(changed),completed_at=datetime.now(timezone.utc).isoformat())
        save()
        print(json.dumps({'state':report['state'],'checks':len(report['checks']),
                          'main_checks':report['main_checks'],'independent_checks':report['independent_checks'],
                          'protected_changed_count':len(changed)}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()
