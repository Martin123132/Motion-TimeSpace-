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
    destination = intake/'annular-gram-geometry-bound-final-integrity.json'
    snapshot = intake/'annular-gram-geometry-bound-resume-snapshot.md'
    script_snapshot = intake/'annular-gram-geometry-bound-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,script_snapshot]):
        raise FileExistsError('Do not overwrite sealed or attempted evidence.')
    report = {'state':'running','checks':[],'inputs':{},'outputs':{},
              'full_GR_limit_proven':False,'dynamical_h_family_evolved':False,
              'uniform_H3_solution_bound_proven':False,'valid_for_physics_claim':False,
              'conditional_matched_radial_geometry_bound_derived':True,
              'positive_extra_energy_disappearance_criterion_derived':True,
              'conditional_geometry_bound_numerically_verified':False,
              'protected_scan_scope':'mtime since 2026-09-14T00:55:45Z, not pre-turn content hashes',
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
        for label,directory,expected_checks in [
            ('main','annular-gram-geometry-bound-attempt01',61),
            ('independent','annular-gram-geometry-bound-independent-attempt01',88)]:
            status_path=intake/directory/'status.json'
            status=json.loads(status_path.read_text())
            check(label+'_complete',status['state']=='complete' and len(status['checks'])==expected_checks
                  and all(row['passed'] for row in status['checks']) and len(status['cases'])==8)
            check(label+'_claim_gates_remain_false',not any(status[key] for key in
                  ['full_GR_limit_proven','dynamical_h_family_evolved','uniform_H3_solution_bound_proven','valid_for_physics_claim']))
            for table in ['inputs','outputs']:
                for filename,expected in status[table].items():
                    path=root/filename
                    if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed or missing evidence: '+filename)
                    report['inputs'][filename]=expected
            own(status_path)
            report[label+'_checks']=expected_checks
        check('all_source_and_evidence_hashes_match',True)
        for stem in ['annular_gram_geometry_bound','derive_annular_gram_geometry_bound',
                     'verify_annular_gram_geometry_bound','seal_annular_gram_geometry_bound']:
            path=root/'scripts'/(stem+'_20260914.py')
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('four_new_scripts_compile_without_bytecode',True)
        script_snapshot.write_bytes(Path(__file__).read_bytes())
        own(script_snapshot,'outputs')
        note=root/'DERIVATION-20260914-Gram-bound-to-radial-geometry.md'
        for citation in re.findall(r'\x60([^\x60]+)\x60',note.read_text(encoding='utf-8')):
            if citation.endswith(('.py','.md','.json','.npz')):
                check('cited_path_exists_'+citation,(root/citation).is_file())
        own(note,'outputs')
        protected=root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        start=datetime.fromisoformat('2026-09-14T00:55:45+00:00').timestamp()
        changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>start]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        check('no_python_cache',not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update(state='complete',conditional_geometry_bound_numerically_verified=True,
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
