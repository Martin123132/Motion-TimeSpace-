from derive_annular_source_gravity_20260914 import EvidenceRun
import hashlib
import json
import re
import traceback
from datetime import datetime, timezone
from pathlib import Path


def main():
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-anchored-moving-final-integrity.json'
    snapshot = intake/'annular-anchored-moving-resume-snapshot.md'
    executed = intake/'annular-anchored-moving-executed-sealer.py'
    if any(path.exists() for path in [destination,snapshot,executed]):
        raise FileExistsError('Sealed outputs are immutable.')
    report = dict(state='running',checks=[],inputs={},outputs={},full_GR_limit_proven=False,
        valid_for_physics_claim=False,live_metric_action_varied=False,rigorous_interval_certificate=False,
        github_action=False,subagents_used=False,
        protected_scan_scope='mtime since 2026-09-16T13:22:59Z, not a pre-turn full hash baseline')
    cache = {}

    def digest(path):
        path = path.resolve()
        if path not in cache:
            value = hashlib.sha256()
            with path.open('rb') as stream:
                while chunk := stream.read(1024*1024):
                    value.update(chunk)
            cache[path] = value.hexdigest()
        return cache[path]

    def own(path,table='inputs'):
        report[table][str(path.resolve().relative_to(root))] = digest(path)

    def save():
        destination.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n',encoding='utf-8')

    def check(name,passed,detail=None):
        report['checks'].append(dict(name=name,passed=bool(passed),detail=detail))
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def inherit(status):
        for table in ['inputs','outputs']:
            for name,expected in status[table].items():
                path = (root/name).resolve()
                key = str(path.relative_to(root))
                if not path.is_file() or digest(path)!=expected:
                    raise RuntimeError('Missing or changed immutable file: '+name)
                if key in report['inputs'] and report['inputs'][key]!=expected:
                    raise RuntimeError('Conflicting immutable digest: '+name)
                report['inputs'][key] = expected

    save()
    try:
        previous_path = intake/'annular-moving-spectral-final-integrity-v2.json'
        previous = json.loads(previous_path.read_text())
        check('previous_checkpoint_complete',previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        inherit(previous)
        own(previous_path)
        statuses,counts = {},{}
        for label,folder,count,cases in [('qualification','annular-anchored-chart-qualification-attempt03',141,12),
            ('gap','annular-chart-window-gap-attempt01',8,2),('smoke','annular-anchored-moving-smoke-attempt01',17,2),
            ('tight','annular-anchored-moving-tight-attempt01',17,2),('precision','annular-anchored-moving-precision-attempt01',16,2)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            json.dumps(status,allow_nan=False)
            check(label+'_complete',status['state']=='complete' and len(status['checks'])==count
                and len(status['cases'])==cases and all(row['passed'] for row in status['checks']))
            check(label+'_broad_claims_remain_false',not status['full_GR_limit_proven'] and not status['valid_for_physics_claim']
                and not status['complete_parent_source_action_derived'])
            inherit(status)
            own(path)
            statuses[label],counts[label] = status,count
        qualified = statuses['qualification']
        check('paired_flat_and_curved_qualification',
            {(row['branch'],row['base_count'],row['background_mass'],row['position']) for row in qualified['cases']}
            =={(branch,base_count,mass,position) for branch in ['reference','MTS'] for base_count,mass in [(33,0.),(33,.7),(129,0.)]
                for position in [6.03,6.0303]})
        check('chart_derivatives_independently_qualified',all(len(row['derivative_controls'])>=2 and
            all(control['first_error']<2e-4 and control['second_error']<3e-3 for control in row['derivative_controls'][-2:])
            for row in qualified['cases']))
        check('positive_whole_window_gap_margins_not_interval_claim',all(row['minimum_absolute_gap_margin']>0
            and row['maximum_enclosure_radius']<row['minimum_absolute_gap_margin']/10 and not row['rigorous_interval_certificate']
            for row in statuses['gap']['cases']) and not statuses['gap']['rigorous_interval_certificate'])
        for label in ['smoke','tight']:
            status = statuses[label]
            configuration = status['configuration']
            check(label+'_limited_scope_preserved',configuration['final_time']==.005 and configuration['sample_count']==41
                and configuration['same_sample_reduction_force_budget']==2e-7 and status['physical_GR_gates_unchanged']
                and not status['all_time_error_certificate'] and status['omitted_drive_integral_not_trajectory_error_bound'])
            for row in status['cases']:
                branch = row['branch']
                expected = 273 if branch=='reference' else 278
                check(label+'_'+branch+'_mask_and_preparation',row['retained_count']==expected and row['full_count']==286
                    and row['initial_preparation_energy_norm']>0 and row['freely_evolved_reduced_trajectory'])
                check(label+'_'+branch+'_evolution_complete',row['final_integrated_omitted_drive']>0
                    and row['final_integrated_kinetic_defect']>0 and row['chart_minimum_gap_all_evaluations']>1e-4
                    and row['chart_minimum_overlap_all_evaluations']>.25)
                folder = intake/('annular-anchored-moving-'+label+'-attempt01')
                diagnostics = json.loads((folder/(branch+'-diagnostics-8.json')).read_text())
                observed = max(abs(item['force_difference']) for item in diagnostics)
                check(label+'_'+branch+'_physical_flags_recomputed',len(diagnostics)==41 and diagnostics[-1]['time']==.005
                    and observed==row['maximum_sampled_force_error']
                    and row['sampled_reduction_force_budget_met']==(observed<=2e-7)
                    and row['failing_sample_count']==sum(abs(item['force_difference'])>2e-7 for item in diagnostics))
                check(label+'_'+branch+'_force_decomposition_and_direct_bound',all(
                    abs(item['force_difference']-item['same_state_force_difference']-item['trajectory_contribution'])<2e-15
                    and abs(item['same_state_force_difference'])<=item['same_state_force_bound']+2e-12 for item in diagnostics))
        check('tighter_control_is_independent_temporal_refinement',statuses['tight']['configuration']['tight']
            and statuses['tight']['configuration']['rtol']==statuses['smoke']['configuration']['rtol']/100
            and statuses['tight']['configuration']['atol']==statuses['smoke']['configuration']['atol']/100
            and all(row['all_sampled_force_flags_stable'] for row in statuses['precision']['cases']))
        failures = []
        for folder,expected_cases in [('annular-anchored-chart-qualification-attempt01',9),('annular-anchored-chart-qualification-attempt02',11)]:
            path = intake/folder/'status.json'
            status = json.loads(path.read_text())
            check(folder+'_preserved_failure',status['state']=='failed' and len(status['cases'])==expected_cases
                and 'lost overlap' in status['error'])
            inherit(status)
            own(path)
            failures.append(dict(folder=folder,error=status['error']))
        note = root/'DERIVATION-20260916-anchored-moving-reduction-and-gap-envelope.md'
        content = note.read_text(encoding='utf-8')
        cited = re.findall(r'`([^`\r\n]+\.(?:py|md|json))`',content)
        check('note_sources_exist',all((root/name).is_file() for name in cited),cited)
        check('note_finished_and_scoped', 'PENDING' not in content and 'a full GR limit' in content
            and '1/80' in content and 'NOT a rigorous trajectory-error bound' in content)
        own(note)
        names = ['annular_anchored_projector_chart_20260916.py','annular_windowed_projector_chart_20260916.py',
            'verify_annular_anchored_chart_20260916.py','verify_annular_anchored_chart_20260916_v2.py',
            'verify_annular_anchored_chart_20260916_v3.py','run_annular_anchored_moving_smoke_20260916.py',
            'derive_annular_chart_window_gap_20260916.py','verify_annular_anchored_moving_precision_20260916.py',
            'seal_annular_anchored_moving_20260916.py']
        for name in names:
            path = root/'scripts'/name
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('new_sources_compile_without_bytecode',True,names)
        check('script_bytecode_cache_absent',not(root/'scripts/__pycache__').exists())
        protected = root.parent/'formalization-workbench'
        started = datetime(2026,9,16,13,22,59,tzinfo=timezone.utc).timestamp()
        changed = [str(path.relative_to(protected)) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>=started]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        executed.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        own(executed,'outputs')
        check('resume_and_executed_sealer_saved',True)
        report.update(state='complete',completed_at=datetime.now(timezone.utc).isoformat(),current_suite_checks=counts,
            total_successful_current_checks=sum(counts.values()),distinct_files_rehashed=len(cache),
            inherited_failed_attempts_preserved=previous['inherited_failed_attempts_preserved']+len(failures),
            new_failed_attempts_preserved=failures,smoke_results=statuses['smoke']['cases'],
            tighter_results=statuses['tight']['cases'],precision_results=statuses['precision']['cases'],
            moving_reduced_trajectory_verified=True,short_finite_comparison_only=True,
            original_GR_failures_unchanged=True,implementation_checks_not_physics_passes=True)
        save()
        print(json.dumps(dict(state='complete',checks=len(report['checks']),current_checks=sum(counts.values()),
            rehashed_files=len(cache),protected_changed=len(changed),failed_attempts_preserved=report['inherited_failed_attempts_preserved'])),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    main()
