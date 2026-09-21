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
    destination = intake/'annular-reference-continuum-shell-final-integrity.json'
    snapshot = intake/'annular-reference-continuum-shell-resume-snapshot.md'
    executed = intake/'annular-reference-continuum-shell-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Do not overwrite sealed or attempted evidence.')
    report = dict(state='running',checks=[],inputs={},outputs={},
                  conditional_spherical_bulk_equations_identified=True,
                  initial_constraint_consistency_derived=True,
                  source_shell_transfer_and_required_stress_derived=True,
                  evolving_reference_continuum_convergence_proven=False,
                  complete_parent_source_action_derived=False,
                  full_GR_limit_proven=False,global_existence_proven=False,
                  valid_for_physics_claim=False,github_action=False,subagents_used=False,
                  protected_scan_scope='mtime since2026-09-14T15:07:13Z,not pre-turn content hashes')

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
        previous = intake/'annular-reference-wave-decoupling-final-integrity.json'
        previous_status = json.loads(previous.read_text())
        check('previous_final_complete',previous_status['state']=='complete' and
              all(row['passed'] for row in previous_status['checks']))
        inherit(previous_status)
        own(previous)
        for label,directory,expected_count in [
                ('main','annular-reference-continuum-shell-attempt01',41),
                ('algebra','annular-reference-continuum-shell-algebra-attempt01',15),
                ('independent','annular-reference-continuum-shell-independent-attempt01',30)]:
            path = intake/directory/'status.json'
            status = json.loads(path.read_text())
            check(label+'_complete',status['state']=='complete' and len(status['checks'])==expected_count
                  and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_remain_false',not any(status[key] for key in
                  ['evolving_reference_continuum_convergence_proven','complete_parent_source_action_derived',
                   'full_GR_limit_proven','valid_for_physics_claim']))
            inherit(status)
            own(path)
            report[label+'_checks'] = len(status['checks'])
        check('all_inherited_and_current_hashes_match',True,len(report['inputs']))
        for stem in ['annular_reference_continuum_shell','derive_annular_reference_continuum_shell',
                     'check_annular_reference_continuum_shell','verify_annular_reference_continuum_shell',
                     'seal_annular_reference_continuum_shell']:
            path = root/'scripts'/(stem+'_20260914.py')
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('five_new_sources_compile_without_bytecode',True)
        executed.write_bytes(Path(__file__).read_bytes())
        own(executed,'outputs')
        note = root/'DERIVATION-20260914-reference-continuum-and-source-shell.md'
        note_text = note.read_text(encoding='utf-8')
        citations = re.findall(r'\x60([^\x60]+)\x60',note_text)
        paths = [root/citation for citation in citations if citation.endswith(('.py','.md','.json','.npz'))]
        check('all_cited_local_paths_exist',all(path.is_file() for path in paths),len(paths))
        for path in paths:
            own(path)
        own(note,'outputs')
        provenance = intake/'reference-continuum-shell-provenance.json'
        source_record = json.loads(provenance.read_text())
        check('primary_web_urls_recorded_and_cited',len(source_record['sources'])==2 and
              all(row['url'] in note_text and row['used'] and row['not_adopted'] for row in source_record['sources']))
        check('web_comparison_not_a_physics_claim',source_record['valid_for_physics_claim'] is False)
        own(provenance,'outputs')
        protected = root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        started = datetime.fromisoformat('2026-09-14T15:07:13+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>started]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        check('no_script_python_cache',not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),
                      protected_changed_count=len(changed))
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),
                              main=report['main_checks'],algebra=report['algebra_checks'],
                              independent=report['independent_checks'],hashed_files=len(report['inputs'])+len(report['outputs']),
                              protected_changed_count=len(changed))),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()

