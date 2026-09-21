import hashlib
import json
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path
from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    root=Path(__file__).resolve().parents[1]
    intake=root/'source-intake/navier-stokes/20260914'
    destination=intake/'annular-moving-GR-final-integrity.json'
    snapshot=intake/'annular-moving-GR-resume-snapshot.md'
    executed=intake/'annular-moving-GR-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('All earlier attempts are immutable.')
    report=dict(state='running',checks=[],inputs={},outputs={},
                coupled_moving_GR_scalar_PDE_tested=True,
                flat_exact_wave_and_source_accuracy_qualified=True,
                temporal_Einstein_and_scalar_constraints_checked=True,
                source_force_from_live_PDE=True,
                original_rigid_source_failure_preserved=True,
                mass_conservation_imposed_by_projection=False,
                numerical_boundary_loss_hidden_as_absorption=False,
                complete_parent_source_action_derived=False,
                material_coefficients_parent_derived=False,
                perfect_reflection_parent_derived=False,
                moving_finite_collar_MTS_boundary_derived=False,
                full_GR_limit_proven=False,valid_for_physics_claim=False,
                github_action=False,subagents_used=False,
                resource_policy='Main numerical jobs sequential, BelowNormal and one-core. At most two own Python processes including short diagnostics; no other task stopped.',
                protected_scan_scope='mtime since2026-09-14T20:03:06Z, not pre-turn content hashes')

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
                    raise RuntimeError('Conflicting source hash: '+filename)
                report['inputs'][filename]=expected

    save()
    try:
        previous=intake/'annular-dynamical-source-final-integrity.json'
        old=json.loads(previous.read_text())
        check('previous_source_action_seal_complete',old['state']=='complete' and all(row['passed'] for row in old['checks']))
        inherit(old)
        own(previous)
        totals={}
        statuses={}
        for label,folder,count in [
            ('moving_boundary_algebra','annular-moving-wave-algebra-attempt01',17),
            ('flat_coupled_PDE','annular-moving-flat-PDE-attempt03',37),
            ('GR_coupled_PDE','annular-moving-GR-PDE-attempt01',25),
            ('independent_GR_checks','annular-moving-GR-independent-attempt01',22),
            ('interpolation_warning','annular-moving-radial-interpolation-attempt01',13)]:
            path=intake/folder/'status.json'
            status=json.loads(path.read_text())
            check(label+'_complete',status['state']=='complete' and len(status['checks'])==count and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_false',not status['full_GR_limit_proven'] and not status['valid_for_physics_claim'] and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            totals[label]=count
            statuses[label]=status
        for folder,phrase in [
            ('annular-moving-flat-PDE-attempt01','at least one array'),
            ('annular-moving-flat-PDE-attempt02','finest_accuracy_gates')]:
            path=intake/folder/'status.json'
            failure=json.loads(path.read_text())
            check(folder+'_failure_preserved',failure['state']=='failed' and phrase in failure['error'])
            inherit(failure)
            own(path)
        check('inherited_and_current_files_unchanged',True,len(report['inputs']))
        for amplitude in [.01,.02]:
            cases=[row for row in statuses['flat_coupled_PDE']['cases'] if row['amplitude']==amplitude]
            check(str(amplitude)+'_original_flat_accuracy_gate_maintained',cases[-1]['relative_wave_error']<.005 and cases[-1]['count']==2049)
        curve=statuses['GR_coupled_PDE']
        check('GR_five_grids_with_recoil_and_no_prescribed_force',len(curve['cases'])==5 and curve['cases'][-1]['count']==4097 and not curve['external_force_history_prescribed'])
        report['finest_GR_case']=curve['cases'][-1]
        report['last_GR_refinement']=curve['refinement'][-1]
        report['independent_finest_residuals']=statuses['independent_GR_checks']['cases'][-1]
        report['interpolation_warnings']=statuses['interpolation_warning']['cases']
        stems=['annular_moving_wave','derive_annular_moving_wave','annular_exact_flat_wave','annular_exact_flat_wave_v2',
               'run_annular_moving_flat_PDE','run_annular_moving_flat_PDE_v2','run_annular_moving_flat_PDE_v3',
               'run_annular_moving_GR_PDE','verify_annular_moving_GR_PDE','audit_annular_moving_radial_interpolation',
               'seal_annular_moving_GR']
        for stem in stems:
            path=root/'scripts'/(stem+'_20260914.py')
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('eleven_sources_compile_without_bytecode',True)
        executed.write_bytes(Path(__file__).read_bytes())
        own(executed,'outputs')
        note=root/'DERIVATION-20260914-coupled-moving-source-GR-control.md'
        document=note.read_text(encoding='utf-8')
        cited=[root/value for value in re.findall(r'\x60([^\x60]+)\x60',document) if value.endswith(('.md','.py','.json','.csv','.npz'))]
        check('every_local_citation_exists',bool(cited) and all(path.is_file() for path in cited),len(cited))
        check('all_draft_results_replaced','RESULTS_PENDING' not in document and 'No pass should be inferred from this draft' not in document)
        for path in cited:
            own(path)
        own(note,'outputs')
        protected=root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        start=datetime.fromisoformat('2026-09-14T20:03:06+00:00').timestamp()
        changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>start]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        check('no_script_bytecode_cache',not (root/'scripts/__pycache__').exists())
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update(state='complete',validation_counts=totals,total_validation_checks=sum(totals.values()),
                      protected_changed_count=len(changed),completed_at=datetime.now(timezone.utc).isoformat())
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),validation_counts=totals,
                              distinct_files=len(set(report['inputs'])|set(report['outputs'])),
                              protected_changed_count=len(changed))),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()

