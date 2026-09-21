import hashlib
import json
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path
from navier_stokes_source_audit_20260908 import limit_process


def main():
    limit_process()
    root=Path(__file__).resolve().parents[1]
    intake=root/'source-intake/navier-stokes/20260914'
    destination=intake/'annular-moving-collar-final-integrity.json'
    snapshot=intake/'annular-moving-collar-resume-snapshot.md'
    executed=intake/'annular-moving-collar-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Every previous attempt remains immutable.')
    report=dict(state='running',checks=[],inputs={},outputs={},
                source_Routh_reduction_on_constant_energy_branch=True,
                minimal_embedding_extension_assumed=True,
                curved_moving_factor_action_candidate_derived=True,
                curved_history_shape_variation_checked=True,
                zero_shift_matter_variation_derived=True,
                smooth_test_history_action_consistency_derived=True,
                moving_source_stability_or_solution_convergence_proven=False,
                minimal_extension_parent_uniqueness_proven=False,
                complete_parent_source_action_derived=False,
                coupled_curved_moving_finite_collar_evolution_completed=False,
                full_GR_limit_proven=False,valid_for_physics_claim=False,
                github_action=False,subagents_used=False,
                resource_policy='One principal BelowNormal single-core worker and at most one short validation worker; no unrelated process stopped.',
                protected_scan_scope='mtime since2026-09-14T21:11:54Z, not a pre-turn content hash baseline.')

    def save():
        destination.write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append(dict(name=name,passed=bool(passed),detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs','outputs']:
            for filename,expected in status[table].items():
                path=root/filename
                if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed evidence: '+filename)
                if filename in report['inputs'] and report['inputs'][filename]!=expected:
                    raise RuntimeError('Conflicting evidence hash: '+filename)
                report['inputs'][filename]=expected

    save()
    try:
        previous=intake/'annular-moving-GR-final-integrity.json'
        old=json.loads(previous.read_text())
        check('previous_moving_GR_control_seal_complete',old['state']=='complete' and all(row['passed'] for row in old['checks']))
        inherit(old)
        own(previous)
        statuses={}
        totals={}
        for label,folder,count in [
            ('flat_action_variation','annular-moving-collar-variation-attempt01',15),
            ('endpoint_links_and_clocks','annular-moving-link-clock-attempt01',13),
            ('material_pullback','annular-moving-material-pullback-attempt01',11),
            ('curved_factor_shape_variation','annular-moving-curved-factor-variation-attempt01',8),
            ('sparse_factor_equivalence','annular-moving-collar-sparse-equivalence-attempt01',16),
            ('smooth_action_consistency','annular-moving-action-consistency-attempt01',10),
            ('zero_shift_current','annular-moving-zero-shift-current-attempt01',8),
            ('flat_action_evolution','annular-moving-collar-flat-attempt03',28)]:
            path=intake/folder/'status.json'
            status=json.loads(path.read_text())
            check(label+'_complete',status['state']=='complete' and len(status['checks'])==count and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false',not status['full_GR_limit_proven'] and
                  not status['valid_for_physics_claim'] and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label]=status
            totals[label]=count
        for folder in ['annular-moving-collar-flat-attempt01','annular-moving-collar-flat-attempt02']:
            path=intake/folder/'status.json'
            failed=json.loads(path.read_text())
            check(folder+'_failure_preserved',failed['state']=='failed' and 'finest_original_accuracy_gates' in failed['error'])
            inherit(failed)
            own(path)
        curve=statuses['flat_action_evolution']
        check('original_waveform_gate_not_relaxed',curve['gates']==dict(max_wave_error=.005,max_position_error=.001,
                                                                      max_velocity_error=.001,max_relative_energy_error=1e-8))
        final={}
        for branch in ['reference','MTS']:
            rows=[row for row in curve['cases'] if row['branch']==branch and row.get('role')!='half_step_control']
            check(branch+'_nine_grids_and_original_finest_gates',len(rows)==9 and rows[-1]['count']==8193 and
                  all(rows[-1][key]<value for key,value in curve['gates'].items()))
            final[branch]=rows[-1]
        stems=['annular_moving_collar_action','derive_annular_moving_collar_action',
               'derive_annular_moving_link_clock','derive_annular_moving_material_pullback',
               'verify_annular_moving_curved_factor_variation','run_annular_moving_collar_flat',
               'run_annular_moving_collar_flat_v2','annular_moving_collar_sparse',
               'verify_annular_moving_collar_sparse','run_annular_moving_collar_flat_v3',
               'verify_annular_moving_action_consistency','seal_annular_moving_collar']
        stems.append('derive_annular_moving_zero_shift_current')
        for stem in stems:
            path=root/'scripts'/(stem+'_20260914.py')
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('thirteen_sources_compile_without_bytecode',True)
        executed.write_bytes(Path(__file__).read_bytes())
        own(executed,'outputs')
        note=root/'DERIVATION-20260914-moving-finite-collar-source-action.md'
        document=note.read_text(encoding='utf-8')
        cited=[root/value for value in re.findall(r'\x60([^\x60]+)\x60',document) if value.endswith(('.md','.py','.json','.csv','.npz'))]
        check('every_local_citation_exists',bool(cited) and all(path.is_file() for path in cited),len(cited))
        check('draft_result_marker_replaced','RESULTS_PENDING' not in document)
        for path in cited:
            own(path)
        own(note,'outputs')
        protected=root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        start=datetime.fromisoformat('2026-09-14T21:11:54+00:00').timestamp()
        changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>start]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        check('no_script_bytecode_cache',not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update(state='complete',validation_counts=totals,total_validation_checks=sum(totals.values()),
                      finest_flat_cases=final,manufactured_curved_variations=statuses['curved_factor_shape_variation']['cases'],
                      zero_shift_matter_current=statuses['zero_shift_current']['cases'],
                      sampled_action_consistency=statuses['smooth_action_consistency']['cases'][-2:],
                      numeric_warnings=curve['warnings'],protected_changed_count=len(changed),
                      completed_at=datetime.now(timezone.utc).isoformat())
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),validation_counts=totals,
                              distinct_files=len(set(report['inputs'])|set(report['outputs'])),
                              protected_changed_count=len(changed))),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
