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
    destination = intake/'annular-reference-wave-decoupling-final-integrity.json'
    snapshot = intake/'annular-reference-wave-decoupling-resume-snapshot.md'
    executed = intake/'annular-reference-wave-decoupling-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Preserve sealed and attempted evidence.')
    report = {'state':'running','checks':[],'inputs':{},'outputs':{},
              'short_time_relative_decoupling_under_stated_existence_hypotheses_derived':True,
              'reference_forcing_vanishes_at_derived_weaker_rate':True,
              'continuum_GR_identified':False,'full_GR_limit_proven':False,'global_existence_proven':False,
              'moving_source_extension_proven':False,'valid_for_physics_claim':False,
              'github_action':False,'subagents_used':False,
              'protected_scan_scope':'mtime since2026-09-14T12:50:12Z,not pre-turn content hashes'}

    def save():
        destination.write_text(json.dumps(report,indent=2)+'\n')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs','outputs']:
            for filename,expected in status[table].items():
                path = root/filename
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed evidence: '+filename)
                report['inputs'][filename] = expected

    save()
    try:
        for label,directory,count in [
                ('main','annular-reference-wave-decoupling-attempt01',9),
                ('independent','annular-reference-wave-decoupling-independent-attempt02',3)]:
            path = intake/directory/'status.json'
            status = json.loads(path.read_text())
            check(label+'_complete',status['state']=='complete' and len(status['cases'])==count
                  and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false',not any(status[key] for key in
                  ['continuum_GR_identified','full_GR_limit_proven','valid_for_physics_claim']))
            inherit(status)
            own(path)
            report[label+'_checks'] = len(status['checks'])
            if label=='main':
                report['constants'] = status['constants']
                check('coarse_comparison_time_not_numerically_extended',0<status['constants']['uniform_tangent_comparison_time']<.06)
            else:
                report['boundary_orders'] = status['boundary_orders']
                check('root_split_quadrature_meets_original_gate',all(row['quadrature_error']<1e-7 for row in status['cases']))
        path = intake/'annular-higher-energy-exact-algebra-attempt01/status.json'
        algebra = json.loads(path.read_text())
        check('exact_changing_clock_algebra_complete',algebra['state']=='complete' and algebra['exact_residual']=='0'
              and all(row['passed'] for row in algebra['checks']))
        inherit(algebra)
        own(path)
        report['exact_algebra_checks'] = len(algebra['checks'])
        failed_path = intake/'annular-reference-wave-decoupling-independent-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        check('failed_coarse_quadrature_attempt_preserved',failed['state']=='failed' and
              'layer_quadrature_refinement' in failed['error'] and not failed['checks'][-1]['passed'])
        inherit(failed)
        own(failed_path)
        report['historical_failure'] = {'path':str(failed_path.relative_to(root)),'error':failed['error']}
        check('all_current_and_inherited_hashes_match',True,len(report['inputs']))
        for stem in ['annular_reference_wave_decoupling','derive_annular_reference_wave_decoupling',
                     'verify_annular_reference_wave_decoupling','verify_annular_reference_wave_decoupling_v2',
                     'annular_reference_wave_quadrature','check_annular_higher_energy_algebra',
                     'seal_annular_reference_wave_decoupling']:
            source = root/'scripts'/(stem+'_20260914.py')
            compile(source.read_bytes(),str(source),'exec')
            own(source)
        check('seven_sources_compile_without_bytecode',True)
        executed.write_bytes(Path(__file__).read_bytes())
        own(executed,'outputs')
        note = root/'DERIVATION-20260914-reference-wave-boundary-decoupling.md'
        for citation in re.findall(r'\x60([^\x60]+)\x60',note.read_text(encoding='utf-8')):
            if citation.endswith(('.py','.md','.json','.npz')):
                check('cited_source_exists_'+citation,(root/citation).is_file())
        own(note,'outputs')
        protected = root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        start = datetime.fromisoformat('2026-09-14T12:50:12+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>start]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        check('no_python_cache',not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update(state='complete',protected_changed_count=len(changed),completed_at=datetime.now(timezone.utc).isoformat())
        save()
        print(json.dumps({'state':'complete','checks':len(report['checks']),'main_checks':report['main_checks'],
                          'independent_checks':report['independent_checks'],'exact_algebra_checks':report['exact_algebra_checks'],
                          'protected_changed_count':len(changed)}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()

