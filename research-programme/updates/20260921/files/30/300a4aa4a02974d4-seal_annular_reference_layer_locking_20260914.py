import hashlib
import json
import re
import traceback
from datetime import datetime,timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-reference-layer-locking-final-integrity.json'
    snapshot = intake/'annular-reference-layer-locking-resume-snapshot.md'
    executed = intake/'annular-reference-layer-locking-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Preserve sealed evidence.')
    report = dict(state='running',checks=[],inputs={},outputs={},
                  layer_locking_Oh_energy_derived=True,
                  restricted_short_time_reference_convergence_argument_derived=True,
                  restricted_MTS_limit_transferred_from_inherited_decoupling=True,
                  fixed_h_continuation_argument_derived=True,
                  proof_scope='Exact stationary-source regular annular regulators, inherited analytic bounds, T<tstar, paper-level argument.',
                  formally_machine_verified=False,
                  independent_continuum_evolution_comparator_run=False,
                  full_GR_limit_proven=False,global_spacetime_existence_proven=False,
                  complete_parent_source_action_derived=False,valid_for_physics_claim=False,
                  github_action=False,subagents_used=False,
                  protected_scan_scope='mtime since2026-09-14T15:58:04Z,not pre-turn content hashes')

    def save():
        destination.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append(dict(name=name,passed=bool(passed),detail=detail))
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
        previous = intake/'annular-reference-continuum-shell-final-integrity.json'
        status = json.loads(previous.read_text())
        check('predecessor_complete',status['state']=='complete' and all(row['passed'] for row in status['checks']))
        inherit(status)
        own(previous)
        for label,folder,expected_count in [
                ('main','annular-reference-layer-locking-attempt01',70),
                ('independent','annular-reference-layer-locking-independent-attempt01',9),
                ('active_source','annular-reference-layer-locking-active-source-attempt01',18)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            check(label+'_passed',status['state']=='complete' and len(status['checks'])==expected_count
                  and all(row['passed'] for row in status['checks']))
            check(label+'_broad_physics_guards_false',not status['full_GR_limit_proven'] and
                  not status['valid_for_physics_claim'] and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            report[label+'_checks'] = expected_count
            if label=='main':
                report['comparison_time'] = status['constants']['uniform_tangent_comparison_time']
                check('fresh_runs_inside_analytic_interval',max(row['time'] for row in status['cases'])<report['comparison_time'])
            if label=='active_source':
                check('active_source_controls_not_original_trajectories','manufactured' in status['scope'] and
                      'not the original compact preparation' in status['scope'])
        check('inherited_and_current_hashes_match',True,len(report['inputs']))
        for stem in ['annular_reference_layer_locking','derive_annular_reference_layer_locking',
                     'verify_annular_reference_layer_locking','check_annular_layer_locking_active_source',
                     'seal_annular_reference_layer_locking']:
            source = root/'scripts'/(stem+'_20260914.py')
            compile(source.read_bytes(),str(source),'exec')
            own(source)
        check('five_new_sources_compile_without_bytecode',True)
        executed.write_bytes(Path(__file__).read_bytes())
        own(executed,'outputs')
        note = root/'DERIVATION-20260914-layer-locking-and-restricted-evolving-GR-limit.md'
        paths = [root/value for value in re.findall(r'\x60([^\x60]+)\x60',note.read_text(encoding='utf-8'))
                 if value.endswith(('.py','.md','.json','.npz'))]
        check('all_cited_local_paths_exist',all(path.is_file() for path in paths),len(paths))
        for path in paths:
            own(path)
        own(note,'outputs')
        protected = root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        started = datetime.fromisoformat('2026-09-14T15:58:04+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>started]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        check('no_script_python_cache',not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update(state='complete',protected_changed_count=len(changed),
                      completed_at=datetime.now(timezone.utc).isoformat())
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),main=report['main_checks'],
                              independent=report['independent_checks'],active_source=report['active_source_checks'],
                              distinct_hashed_files=len(set(report['inputs'])|set(report['outputs'])),
                              protected_changed_count=len(changed))),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()

