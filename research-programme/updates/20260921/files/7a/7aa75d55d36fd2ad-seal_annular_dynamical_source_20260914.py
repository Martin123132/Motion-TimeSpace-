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
    destination = intake/'annular-dynamical-source-final-integrity.json'
    snapshot = intake/'annular-dynamical-source-resume-snapshot.md'
    executed = intake/'annular-dynamical-source-executed-sealer.py'
    if any(path.exists() for path in [destination, snapshot, executed]):
        raise FileExistsError('Preserve all attempted or sealed evidence.')
    report = dict(state='running', checks=[], inputs={}, outputs={},
                  conditional_moving_source_action_and_response_derived=True,
                  fixed_source_loading_law_recovered=True,
                  flat_scalar_recoil_solved_and_direct_bulk_energy_checked=True,
                  causal_radially_stable_vacuum_material_example_tested=True,
                  original_rigid_source_failure_preserved=True,
                  complete_parent_source_action_derived=False,
                  material_coefficients_parent_derived=False,
                  perfect_reflection_parent_derived=False,
                  coupled_moving_GR_scalar_PDE_tested=False,
                  moving_finite_collar_MTS_boundary_derived=False,
                  nonspherical_stability_proven=False,
                  full_GR_limit_proven=False, valid_for_physics_claim=False,
                  github_action=False, subagents_used=False,
                  resource_policy='One own BelowNormal single-core numerical worker at a time in this turn; all numerical jobs completed.',
                  protected_scan_scope='mtime since2026-09-14T18:58:15Z, not pre-turn content hashes')

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
        previous = intake/'annular-source-collision-final-integrity.json'
        old = json.loads(previous.read_text())
        check('previous_collision_seal_complete', old['state'] == 'complete' and all(row['passed'] for row in old['checks']))
        inherit(old)
        own(previous)
        totals = {}
        statuses = {}
        for label, folder, count in [
            ('algebra', 'annular-dynamical-source-algebra-attempt02', 18),
            ('material_and_GR_shell', 'annular-dynamical-source-numerics-attempt01', 28),
            ('flat_recoil', 'annular-exact-flat-recoil-attempt02', 37),
            ('direct_bulk_energy', 'annular-flat-bulk-energy-attempt01', 37)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            check(label+'_complete', status['state'] == 'complete' and len(status['checks']) == count and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false', not status['full_GR_limit_proven'] and not status['valid_for_physics_claim'] and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            totals[label] = count
            statuses[label] = status
        for label, phrase in [
            ('annular-dynamical-source-algebra-attempt01', 'direct_time_dependent_interior_curvature'),
            ('annular-exact-flat-recoil-attempt01', 't_eval')]:
            path = intake/label/'status.json'
            status = json.loads(path.read_text())
            check(label+'_failed_attempt_preserved', status['state'] == 'failed' and phrase in status['error'])
            inherit(status)
            own(path)
        check('all_previous_and_current_hashes_match', True, len(report['inputs']))
        check('three_flat_amplitudes_and_fifteen_bulk_slices', len(statuses['flat_recoil']['cases']) == 3 and len(statuses['direct_bulk_energy']['cases']) == 15)
        check('current_GR_shell_test_not_old_wave_replay', statuses['material_and_GR_shell']['coupled_moving_GR_scalar_PDE_tested'] is False)
        report['maximum_direct_bulk_energy_defect'] = max(abs(row['energy_defect']) for row in statuses['direct_bulk_energy']['cases'])
        report['quiet_material'] = statuses['material_and_GR_shell']['quiet_material']
        report['flat_recoil_cases'] = statuses['flat_recoil']['cases']
        stems = ['annular_dynamical_source', 'derive_annular_dynamical_source', 'derive_annular_dynamical_source_v2',
                 'test_annular_dynamical_source', 'test_annular_exact_flat_recoil', 'test_annular_exact_flat_recoil_v2',
                 'verify_annular_flat_bulk_energy', 'seal_annular_dynamical_source']
        for stem in stems:
            path = root/'scripts'/(stem+'_20260914.py')
            compile(path.read_bytes(), str(path), 'exec')
            own(path)
        check('eight_sources_compile_without_bytecode', True)
        executed.write_bytes(Path(__file__).read_bytes())
        own(executed, 'outputs')
        note = root/'DERIVATION-20260914-action-consistent-moving-source.md'
        note_text = note.read_text(encoding='utf-8')
        cited = [root/value for value in re.findall(r'\x60([^\x60]+)\x60', note_text) if value.endswith(('.md', '.py', '.json', '.csv', '.npz'))]
        check('all_cited_local_sources_exist', bool(cited) and all(path.is_file() for path in cited), len(cited))
        for path in cited:
            own(path)
        provenance_path = intake/'annular-dynamical-source-provenance.json'
        provenance = json.loads(provenance_path.read_text())
        recorded = {source['url'] for source in provenance['sources']}
        recorded |= {'https://doi.org/'+source['doi'] for source in provenance['sources']}
        web_links = set(re.findall(r'\]\((https://[^)]+)\)', note_text))
        check('all_note_web_sources_recorded', bool(web_links) and web_links <= recorded, sorted(web_links))
        check('provenance_has_no_physics_pass', provenance['valid_for_physics_claim'] is False)
        own(provenance_path, 'outputs')
        own(note, 'outputs')
        protected = root.parent/'formalization-workbench'
        check('protected_workbench_exists', protected.is_dir())
        start = datetime.fromisoformat('2026-09-14T18:58:15+00:00').timestamp()
        changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start]
        check('protected_workbench_mtime_changed_count_zero', not changed, changed)
        check('no_script_bytecode_cache', not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot, 'outputs')
        report.update(state='complete', validation_counts=totals, total_completed_validation_checks=sum(totals.values()),
                      protected_changed_count=len(changed), completed_at=datetime.now(timezone.utc).isoformat())
        save()
        print(json.dumps(dict(state='complete', checks=len(report['checks']), validation_counts=totals,
                              maximum_direct_bulk_energy_defect=report['maximum_direct_bulk_energy_defect'],
                              protected_changed_count=len(changed), distinct_files=len(set(report['inputs']) | set(report['outputs'])))), flush=True)
    except Exception as error:
        report.update(state='failed', error=repr(error), traceback=traceback.format_exc())
        save()
        raise


if __name__ == '__main__':
    run()

