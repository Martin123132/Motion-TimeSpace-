import hashlib
import json
import re
import traceback
from datetime import datetime
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from scipy.integrate import solve_ivp
    from annular_common_source_history_20260913 import ExteriorModePreparation
    from annular_clock_reservoir_coupling_20260913 import ProperClockDrive
    from annular_horizontal_clock_evolution_20260913 import HorizontalEvolution
    from annular_finite_width_bulk_current_20260913 import shape_weight

    root=Path(__file__).resolve().parents[1]
    intake=root/'source-intake/navier-stokes/20260913'
    destination=intake/'annular-horizontal-clock-final-integrity.json'
    snapshot=intake/'annular-horizontal-clock-resume-snapshot.md'
    if destination.exists() or snapshot.exists():
        raise FileExistsError('Executed evidence must not be overwritten.')
    report={'state':'running','checks':[],'inputs':{},'outputs':{},'independent_cases':[],
            'valid_for_physics_claim':False,'full_GR_limit_proven':False,'global_causal_wellposedness_proven':False,
            'original_prescribed_inner_mass_history_solved':False,'same_microscopic_exterior_state':False,
            'apparatus_support_stresses_derived':False,'unique_regulator_derived':False,'exterior_amplitudes_retuned':False,
            'closed_enlarged_support_is_declared_extension':True,'conditional_live_evolution_complete':False,
            'protected_scan_scope':'mtime since 2026-09-13T20:19:03Z; not pre-turn hashes'}

    def save():
        destination.write_text(json.dumps(report,indent=2)+'\n')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    save()
    try:
        for stage,count in [('pilot',2),('evolve',6)]:
            directory=intake/('annular-horizontal-clock-'+stage+'-attempt01')
            batch=json.loads((directory/'status.json').read_text())
            check(stage+'_completed_without_failed_checks',batch['state']=='complete' and len(batch['cases'])==count and all(row['passed'] for row in batch['checks']))
            for table in ['inputs','outputs']:
                for filename,expected in batch[table].items():
                    if filename not in report['inputs']:
                        if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                            raise RuntimeError('Changed source: '+filename)
                        report['inputs'][filename]=expected
            for path in directory.iterdir():
                if path.is_file():
                    own(path,'outputs')
                    if path.name.startswith('executed-'):
                        check(path.name+'_matches_source_'+stage,path.read_bytes()==(root/'scripts'/path.name.removeprefix('executed-')).read_bytes())
                    if path.suffix=='.npz':
                        with np.load(path,allow_pickle=False) as archive:
                            check(path.name+'_finite',all(np.isfinite(archive[key]).all() for key in archive.files))
            report[stage+'_checks']=len(batch['checks'])
        check('all_claim_limit_flags_remain_false',all(batch[key] is False for key,value in report.items() if value is False and key!='conditional_live_evolution_complete'))
        baseline={row['label']:row for row in json.loads((intake/'annular-clock-reservoir-coupling-attempt01/status.json').read_text())['cases']}
        matched={row['branch']:row for row in json.loads((intake/'annular-common-source-history-attempt01/status.json').read_text())['cases'] if row['case']==0}
        for branch in ['GR','metric_Gram']:
            row=matched[branch]
            with np.load(root/'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03'/(branch+'_source_snapshot.npz'),allow_pickle=False) as archive:
                source={key:archive[key].copy() for key in archive.files}
            with np.load(intake/'annular-finite-width-boundary-cut-attempt01'/(branch+'_0_prepared_collar.npz'),allow_pickle=False) as archive:
                prepared={key:archive[key].copy() for key in archive.files}
            with np.load(root/'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'/('canonical_N16_'+branch+'_sample0.npz'),allow_pickle=False) as archive:
                clock=archive['affine_clock'].copy()
                acceleration=float(archive['endpoint_acceleration'][-1])
            preparation=ExteriorModePreparation(source,branch!='GR',prepared['kinetic_seed'],float(prepared['outer_clock']),prepared['drive'],row['width'],row['shape'],reservoir_energy=row['reservoir_energy'],base_coefficients=baseline[row['label']]['coefficients'])
            model=preparation.build(row['exterior_amplitudes'])
            driver=ProperClockDrive(model,float(clock[1]),acceleration,degree=64)
            system=HorizontalEvolution(model,driver,clock,degree=16)
            directory=intake/'annular-horizontal-clock-evolve-attempt01'
            archives={}
            for suffix in ['degree12_steps2','degree12_steps4','degree16_steps4']:
                with np.load(directory/(branch+'_'+suffix+'_evolution.npz'),allow_pickle=False) as archive:
                    archives[suffix]={key:archive[key].copy() for key in archive.files}
            coarse,fine,spatial=[archives[key] for key in ['degree12_steps2','degree12_steps4','degree16_steps4']]
            temporal_change=float(abs(coarse['states']-fine['states']).max())
            coarse_system=HorizontalEvolution(model,driver,clock,degree=12)
            interpolated=[]
            for state in fine['states'].T:
                values,inner_clock=coarse_system.unpack(state)
                refined_values=coarse_system.grid.evaluate(coarse_system.grid.coefficients(values),system.grid.offsets)
                interpolated.append(system.pack(refined_values,inner_clock))
            spatial_change=float(abs(np.stack(interpolated,axis=1)-spatial['states']).max())
            check(branch+'_temporal_refinement_preserves_state',temporal_change<1e-9,temporal_change)
            check(branch+'_layer_refinement_preserves_state',spatial_change<1e-9,spatial_change)
            end_time=float(spatial['times'][-1])
            replay_rows=[]
            for step_count in [32,64]:
                state=system.initial_state.copy()
                step=end_time/step_count
                for index in range(step_count):
                    time=index*step
                    first=system.rhs(time,state)
                    second=system.rhs(time+step/2,state+step*first/2)
                    third=system.rhs(time+step/2,state+step*second/2)
                    fourth=system.rhs(time+step,state+step*third)
                    state += step*(first+2*second+2*third+fourth)/6
                difference=float(abs(state-spatial['states'][:,-1]).max())
                check(branch+'_independent_RK4_'+str(step_count)+'_agrees_with_DOP853',difference<1e-9,difference)
                evaluation=system.evaluate(end_time,state)
                inner_mass=evaluation['geometry'].metric(np.array([model.radii[0]]))['mu'][0]
                proper_rate=prepared['drive'][0]/model.metric(np.array([model.radii[0]]))['N'][0]
                affine_defect=float(inner_mass-source['mu'][0]-proper_rate*system.unpack(state)[1])
                replay_rows.append({'steps':step_count,'state_error':difference,'inner_affine_defect':affine_defect})
            check(branch+'_affine_history_defect_survives_independent_integration',all(abs(entry['inner_affine_defect'])>1e-9 for entry in replay_rows) and abs(replay_rows[0]['inner_affine_defect']-replay_rows[1]['inner_affine_defect'])<1e-11)
            final=system.evaluate(end_time,spatial['states'][:,-1])
            geometry=final['geometry']
            reference=[]
            values=np.array([system.lower_mass_seed,0.])
            for piece in geometry.pieces:
                lower,upper=piece['lower'],piece['upper']
                sample=np.linspace(lower,upper,7)
                if piece['gap']:
                    output=np.column_stack([np.full(len(sample),values[0]),values[1]+.5*np.log((1-2*values[0]/sample)/(1-2*values[0]/lower))])
                    values=output[-1].copy()
                else:
                    node=int(np.argmin(abs(model.radii-(lower+upper)/2)))

                    def equation(radius,state):
                        offset=(radius-model.radii[node])/model.width
                        scalar=geometry.scalar([offset])
                        weight=shape_weight(np.array([offset]),model.shape)[0]/model.width
                        root_f=np.sqrt(1-2*state[0]/radius)
                        if node==len(model.radii)-1:
                            momentum=radius**2*scalar['source_velocity'][0]/root_f
                            reservoir=weight*scalar['energy'][0]
                        else:
                            momentum=scalar['p'][0,node]
                            reservoir=0.
                        density=weight*(scalar['potential'][0,node]+model.node_weights[node]*momentum**2/(2*radius**2))
                        return np.array([model.coupling*(root_f**2*density+root_f*reservoir),state[0]/(radius**2*root_f**2)+model.coupling*density/radius])

                    radial=solve_ivp(equation,(lower,upper),values,method='DOP853',rtol=2e-13,atol=2e-15,max_step=(upper-lower)/4,dense_output=True)
                    if not radial.success:
                        raise RuntimeError(radial.message)
                    output=radial.sol(sample).T
                    values=output[-1].copy()
                reference.extend(zip(sample,output[:,0],output[:,1]))
            reference=np.array(reference)
            candidate=geometry.metric(reference[:,0])
            shift=candidate['log_N'][0]-reference[0,2]
            radial_error=float(max(abs(candidate['mu']-reference[:,1]).max(),abs(candidate['log_N']-reference[:,2]-shift).max()))
            check(branch+'_independent_adaptive_radial_equations_match_collocation',radial_error<1e-9,radial_error)
            initial_geometry=system.evaluate(0.,system.initial_state)['geometry'].metric(model.radii)
            final_geometry=geometry.metric(model.radii)
            inner=geometry.metric(np.array([model.radii[0]]))
            actual_current=final['current'].evaluate(np.array([model.radii[0]]))[0]
            required_current=-proper_rate*inner['N'][0]**2/(model.coupling*inner['U'][0])
            tracking_rate=system.mass_flux(final,np.array([model.radii[0]]))[0]-proper_rate*inner['N'][0]
            tracking_identity_error=float(abs(tracking_rate+model.coupling*inner['U'][0]*(actual_current-required_current)/inner['N'][0]))
            check(branch+'_affine_boundary_tracking_defect_owned_by_current',tracking_identity_error<1e-12)
            mass_change=float(abs(final_geometry['mu']-initial_geometry['mu']).max())
            lapse_change=float(abs(final_geometry['N']-initial_geometry['N']).max())
            check(branch+'_geometry_really_evolves_not_frozen',mass_change>1e-8 and lapse_change>1e-8,{'mass':mass_change,'lapse':lapse_change})
            rows=[entry for entry in batch['cases'] if entry['label']==branch+'_degree16_steps4'][0]['diagnostics']
            defects=np.array([entry['inner_affine_proper_history_error'] for entry in rows[1:]])
            orders=np.log2(abs(defects[1:]/defects[:-1]))
            check(branch+'_initial_two_jet_departure_is_resolved_near_cubic',np.all((orders>2.7)&(orders<3.2)),orders.tolist())
            report['independent_cases'].append({'branch':branch,'temporal_refinement_change':temporal_change,'spatial_refinement_change':spatial_change,
                                                'independent_RK4':replay_rows,'independent_radial_error':radial_error,'mass_change':mass_change,'lapse_change':lapse_change,
                                                'final_actual_inner_current':float(actual_current),'final_required_inner_current_for_affine_history':float(required_current),
                                                'final_inner_affine_tracking_rate':float(tracking_rate),'tracking_identity_error':tracking_identity_error,
                                                'observed_initial_departure_orders':orders.tolist(),'finite_interval_affine_history_does_not_hold':True})
            save()
        note=root/'DERIVATION-20260913-horizontal-clock-live-evolution-and-boundary-history.md'
        for citation in re.findall(r'`([^`]+)`',note.read_text(encoding='utf-8')):
            if citation.endswith(('.py','.md','.json','.npz')):
                check('cited_source_exists_'+citation,(root/citation).is_file())
        own(note,'outputs')
        for stem in ['annular_horizontal_clock_evolution','derive_annular_horizontal_clock_evolution','verify_annular_horizontal_clock_evolution']:
            path=root/'scripts'/(stem+'_20260913.py')
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        check('three_scripts_compile_without_bytecode',True)
        check('no_python_cache',not(root/'scripts/__pycache__').exists())
        protected=root.parent/'formalization-workbench'
        check('protected_workbench_exists',protected.is_dir())
        start=datetime.fromisoformat('2026-09-13T20:19:03+00:00').timestamp()
        changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>start]
        check('protected_workbench_mtime_changed_count_zero',not changed,changed)
        snapshot.write_bytes((root/'CURRENT_LOCAL_RESUME.md').read_bytes())
        own(snapshot,'outputs')
        report.update({'state':'complete','conditional_live_evolution_complete':True,'protected_changed_count':len(changed)})
        save()
        print(json.dumps({'state':report['state'],'checks':len(report['checks']),'pilot_checks':report['pilot_checks'],'evolve_checks':report['evolve_checks'],'protected_changed_count':len(changed)}),flush=True)
    except Exception as error:
        report.update({'state':'failed','error':repr(error),'traceback':traceback.format_exc()})
        save()
        raise


if __name__=='__main__':
    run()
