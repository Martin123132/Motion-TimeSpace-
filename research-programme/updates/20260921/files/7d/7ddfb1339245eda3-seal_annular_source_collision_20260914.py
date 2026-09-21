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
    destination = intake/'annular-source-collision-final-integrity.json'
    snapshot = intake/'annular-source-collision-resume-snapshot.md'
    executed = intake/'annular-source-collision-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Preserve all attempted or sealed evidence.')
    report = dict(state='running', checks=[], inputs={}, outputs={},
                  actual_wave_source_collision_tested=True, boundary_operator_repaired=True,
                  source_loading_threshold_derived_conditionally=True,
                  current_rigid_classical_source_energy_condition_passed=False,
                  parent_source_support_action_derived=False, full_GR_limit_proven=False,
                  longer_uniform_analytic_interval_proven=False, valid_for_physics_claim=False,
                  github_action=False, subagents_used=False,
                  resource_policy='At most two own BelowNormal single-core numerical workers; no dense4097-node trajectory retained.',
                  protected_scan_scope='mtime since2026-09-14T17:22:26Z,not pre-turn content hashes')

    def save():
        destination.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append(dict(name=name, passed=bool(passed), detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs', 'outputs']:
            for filename, expected in status[table].items():
                path = root/filename
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
                    raise RuntimeError('Changed evidence: '+filename)
                if filename in report['inputs'] and report['inputs'][filename] != expected:
                    raise RuntimeError('Conflicting provenance: '+filename)
                report['inputs'][filename] = expected

    save()
    try:
        previous = intake/'annular-independent-continuum-final-integrity.json'
        old = json.loads(previous.read_text())
        check('previous_seal_complete', old['state'] == 'complete' and all(row['passed'] for row in old['checks']))
        inherit(old)
        own(previous)
        totals = {}
        for label, folder, count in [
            ('boundary', 'annular-reflecting-boundary-attempt01', 20),
            ('continuum', 'annular-source-collision-continuum-attempt01', 13),
            ('refined_target', 'annular-collision-refined-target-attempt01', 18),
            ('regulators', 'annular-source-collision-regulators-attempt01', 398),
            ('final_comparison', 'annular-source-collision-final-comparison-attempt01', 136)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            check(label+'_complete', status['state'] == 'complete' and len(status['checks']) == count and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim'])
            inherit(status)
            own(path)
            totals[label] = len(status['checks'])
            if label == 'final_comparison':
                report['both_branches_refine_all_declared_collision_norms'] = status['both_branches_refine_all_declared_collision_norms']
                report['nonmonotone_comparisons'] = [row for row in status['collision_refinement'] if not row['decreases']]
        failed_path = intake/'annular-collision-support-verification-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        check('failed_absolute_radial_audit_preserved', failed['state'] == 'failed' and 'radial_37_active_constraints' in failed['error'] and any(not row['passed'] for row in failed['checks']))
        inherit(failed)
        own(failed_path)
        report['preserved_audit_failure'] = failed['error']
        check('all_inherited_and_current_hashes_match', True, len(report['inputs']))
        stems = ['annular_reflecting_boundary', 'test_annular_reflecting_boundary', 'run_annular_source_collision_continuum',
                 'run_annular_source_collision_regulators', 'verify_annular_collision_and_support',
                 'refine_annular_collision_target', 'finalize_annular_source_collision', 'seal_annular_source_collision']
        for stem in stems:
            path = root/'scripts'/(stem+'_20260914.py')
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('eight_sources_compile_without_bytecode', True)
        executed.write_bytes(Path(__file__).read_bytes())
        own(executed, 'outputs')
        note = root/'DERIVATION-20260914-active-source-reflection-and-support-law.md'
        note_text = note.read_text(encoding='utf-8')
        cited = [root/value for value in re.findall(r'\x60([^\x60]+)\x60', note_text) if value.endswith(('.md', '.py', '.json', '.csv', '.npz'))]
        check('all_cited_local_sources_exist', all(path.is_file() for path in cited), len(cited))
        check('draft_status_replaced', 'Do not infer a pass from this draft status' not in note_text)
        for path in cited:
            own(path)
        own(note, 'outputs')
        protected = root.parent/'formalization-workbench'
        check('protected_workbench_exists', protected.is_dir())
        start = datetime.fromisoformat('2026-09-14T17:22:26+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        check('no_script_bytecode_cache', not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot, 'outputs')
        report.update(state='complete', validation_counts=totals, protected_changed_count=len(changed),
                      completed_at=datetime.now(timezone.utc).isoformat())
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), validation_counts=totals,
                              both_branches_refine=report['both_branches_refine_all_declared_collision_norms'],
                              protected_changed_count=len(changed), distinct_files=len(set(report['inputs']) | set(report['outputs'])))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    run()
