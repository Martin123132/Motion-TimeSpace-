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
    destination = intake/'annular-independent-continuum-final-integrity.json'
    snapshot = intake/'annular-independent-continuum-resume-snapshot.md'
    executed = intake/'annular-independent-continuum-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Preserve existing sealed or attempted evidence.')
    report = dict(state='running',checks=[],inputs={},outputs={},
                  independent_continuum_comparison_completed=True,
                  both_regulators_refine_toward_independent_target_in_tested_cases=True,
                  no_parameters_refitted=True,
                  physical_sampling_crosscheck_completed=True,
                  full_GR_limit_proven=False,longer_analytic_time_interval_proven=False,
                  genuine_wave_source_collision_tested=False,
                  parent_source_support_action_derived=False,
                  observational_claim=False,valid_for_physics_claim=False,
                  github_action=False,subagents_used=False,
                  protected_scan_scope='mtime since2026-09-14T16:47:41Z,not pre-turn content hashes')

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
        previous = intake/'annular-reference-layer-locking-final-integrity.json'
        old = json.loads(previous.read_text())
        check('predecessor_complete',old['state']=='complete' and all(row['passed'] for row in old['checks']))
        inherit(old)
        own(previous)
        for label,folder,expected in [
                ('continuum','annular-independent-continuum-attempt01',59),
                ('comparison','annular-continuum-regulator-comparison-attempt01',207),
                ('independent','annular-independent-continuum-verification-attempt01',16),
                ('physical_sampling','annular-continuum-physical-sampling-attempt01',40),
                ('figure','annular-continuum-comparison-figure-attempt02',10)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            check(label+'_passed',status['state']=='complete' and len(status['checks'])==expected
                  and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false',not status['full_GR_limit_proven'] and not status['valid_for_physics_claim'])
            inherit(status)
            own(path)
            report[label+'_checks'] = expected
        failed_path = intake/'annular-continuum-comparison-figure-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        check('failed_optional_renderer_preserved',failed['state']=='failed' and 'matplotlib' in failed['error'])
        inherit(failed)
        own(failed_path)
        report['preserved_render_failure'] = failed['error']
        check('current_and_inherited_hashes_match',True,len(report['inputs']))
        for stem in ['annular_independent_continuum','run_annular_independent_continuum',
                     'compare_annular_regulators_to_continuum','verify_annular_independent_continuum',
                     'check_annular_continuum_physical_sampling','plot_annular_continuum_comparison',
                     'plot_annular_continuum_comparison_v2','seal_annular_independent_continuum']:
            path = root/'scripts'/(stem+'_20260914.py')
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('eight_new_sources_compile_without_bytecode',True)
        executed.write_bytes(Path(__file__).read_bytes())
        own(executed,'outputs')
        note = root/'DERIVATION-20260914-independent-continuum-GR-comparison.md'
        paths = [root/value for value in re.findall(r'\x60([^\x60]+)\x60',note.read_text(encoding='utf-8'))
                 if value.endswith(('.md','.py','.json','.npz','.png','.svg'))]
        check('all_cited_local_paths_exist',all(path.is_file() for path in paths),len(paths))
        for path in paths:
            own(path)
        own(note,'outputs')
        visual = intake/'annular-continuum-comparison-visual-review.json'
        inspection = json.loads(visual.read_text())
        check('native_figure_visually_inspected',inspection['readable_labels'] and
              inspection['no_observed_clipping_or_overlap'] and (root/inspection['image']).is_file())
        own(visual,'outputs')
        protected = root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        started = datetime.fromisoformat('2026-09-14T16:47:41+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>started]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        check('no_script_python_cache',not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update(state='complete',protected_changed_count=len(changed),
                      completed_at=datetime.now(timezone.utc).isoformat())
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),
                              continuum=report['continuum_checks'],comparison=report['comparison_checks'],
                              independent=report['independent_checks'],physical_sampling=report['physical_sampling_checks'],
                              figure=report['figure_checks'],protected_changed_count=len(changed),
                              distinct_hashed_files=len(set(report['inputs'])|set(report['outputs'])))),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()

