import hashlib
import json
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-constrained-mass-relative-energy-final-integrity.json'
    snapshot = intake/'annular-constrained-mass-relative-energy-resume-snapshot.md'
    executed = intake/'annular-constrained-mass-relative-energy-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Preserve sealed and attempted evidence.')
    report = {'state':'running','checks':[],'inputs':{},'outputs':{},
              'conditional_live_relative_energy_derived':True,
              'uniform_short_time_stability_while_solutions_exist_derived':True,
              'unconditional_uniform_convergence':False,'full_GR_limit_proven':False,
              'moving_source_extension_proven':False,'horizon_theorem_proven':False,
              'valid_for_physics_claim':False,'stationary_source_only':True,
              'github_action':False,'subagents_used':False,
              'protected_scan_scope':'mtime since2026-09-14T12:09:38Z,not pre-turn content hashes'}

    def save():
        destination.write_text(json.dumps(report,indent=2)+'\n')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    save()
    try:
        for label,directory,expected_cases in [
                ('main','annular-constrained-mass-relative-energy-attempt01',9),
                ('independent','annular-constrained-mass-relative-energy-independent-attempt01',3)]:
            status_path = intake/directory/'status.json'
            status = json.loads(status_path.read_text())
            check(label+'_complete',status['state']=='complete' and len(status['cases'])==expected_cases
                  and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_remain_false',not any(status[key] for key in
                  ['unconditional_uniform_convergence','full_GR_limit_proven','valid_for_physics_claim']))
            for table in ['inputs','outputs']:
                for filename,expected in status[table].items():
                    path = root/filename
                    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed evidence: '+filename)
                    report['inputs'][filename] = expected
            own(status_path)
            report[label+'_checks'] = len(status['checks'])
            if label=='main':
                constants = status['constants']
                report['constants'] = constants
                extra_domination = 2*constants['radius_upper']**2/constants['radius_lower']**2
                check('reference_Gram_domination_replayed',all(row['reference_Gram_rate_energy']<=
                      extra_domination*row['reference_rate_energy']+1e-10 for row in status['cases']))
                check('short_time_interval_not_full_duration',0<constants['uniform_tangent_comparison_time']<.06)
        check('all_current_and_inherited_hashes_match',True,len(report['inputs']))
        stems = ['annular_constrained_mass_relative_energy','derive_annular_constrained_mass_relative_energy',
                 'verify_annular_constrained_mass_relative_energy','seal_annular_constrained_mass_relative_energy']
        for stem in stems:
            source = root/'scripts'/(stem+'_20260914.py')
            compile(source.read_bytes(),str(source),'exec')
            own(source)
        check('four_new_sources_compile_without_bytecode',True)
        executed.write_bytes(Path(__file__).read_bytes())
        own(executed,'outputs')
        note = root/'DERIVATION-20260914-live-constrained-mass-relative-energy.md'
        for citation in re.findall(r'\x60([^\x60]+)\x60',note.read_text(encoding='utf-8')):
            if citation.endswith(('.py','.md','.json','.npz')):
                check('cited_source_exists_'+citation,(root/citation).is_file())
        own(note,'outputs')
        protected = root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        start = datetime.fromisoformat('2026-09-14T12:09:38+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>start]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        check('no_python_cache',not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update(state='complete',protected_changed_count=len(changed),completed_at=datetime.now(timezone.utc).isoformat())
        save()
        print(json.dumps({'state':'complete','checks':len(report['checks']),'main_checks':report['main_checks'],
                          'independent_checks':report['independent_checks'],'protected_changed_count':len(changed)}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()

