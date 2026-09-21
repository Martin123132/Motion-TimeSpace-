import argparse
import hashlib
import json
import sys
import time
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    import sympy as sp
    from scipy.integrate import solve_ivp
    from annular_common_source_history_20260913 import ExteriorModePreparation, FixedInnerClockJet
    from annular_clock_reservoir_coupling_20260913 import ProperClockDrive
    from annular_horizontal_clock_evolution_20260913 import HorizontalEvolution

    parser = argparse.ArgumentParser()
    parser.add_argument('--stage', choices=['pilot','evolve'], required=True)
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260913'
    destination = intake/('annular-horizontal-clock-'+arguments.stage+'-attempt01')
    destination.mkdir(exist_ok=False)
    report = {'state':'running','stage':arguments.stage,'checks':[],'cases':[],'inputs':{},'outputs':{},
              'valid_for_physics_claim':False,'full_GR_limit_proven':False,'global_causal_wellposedness_proven':False,
              'original_prescribed_inner_mass_history_solved':False,'same_microscopic_exterior_state':False,
              'apparatus_support_stresses_derived':False,'unique_regulator_derived':False,
              'exterior_amplitudes_retuned':False,'closed_enlarged_support_is_declared_extension':True,
              'gauge_fixed_only_after_deriving_full_equations':True,'conditional_live_evolution_complete':False}

    def save():
        (destination/'status.json').write_text(json.dumps(report,indent=2)+'\n')

    def own(path, table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name, passed, detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    save()
    try:
        previous_path = intake/'annular-common-source-history-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_matched_two_jet_seal_complete',previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        for table in ['inputs','outputs']:
            for filename,expected in previous[table].items():
                if filename not in report['inputs']:
                    if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed inherited evidence: '+filename)
                    report['inputs'][filename]=expected
        own(previous_path)
        for path in [Path(__file__), root/'scripts/annular_horizontal_clock_evolution_20260913.py']:
            compile(path.read_bytes(),str(path),'exec')
            own(path)
            snapshot=destination/('executed-'+path.name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot,'outputs')
        geometry, lapse, momentum, coupling, scale, radius, mass = sp.symbols('F N P k a R m',positive=True)
        chart=1-coupling**2*geometry**2*momentum**2
        metric_tt=-lapse**2*chart
        metric_tr=coupling*lapse*sp.sqrt(geometry)*momentum
        connection=coupling*sp.sqrt(geometry)*momentum/(lapse*chart)
        check('horizontal_time_map_diagonalizes_metric',sp.simplify(metric_tr+metric_tt*connection)==0)
        check('diagonal_radial_geometry_is_F_times_d',sp.simplify(1/geometry+2*metric_tr*connection+metric_tt*connection**2-1/(geometry*chart))==0)
        check('diagonal_mass_includes_shift_square',sp.simplify((radius*(1-geometry*chart)/2-radius*(1-geometry)/2)-coupling**2*radius*geometry**3*momentum**2/2)==0)
        root_f, energy, reservoir, energy_rate, reservoir_rate, kernel = sp.symbols('U eps sigma eps1 sigma1 K')
        mass_gradient=coupling*(root_f**2*energy+root_f*reservoir)
        root_gradient=-mass_gradient/(radius*root_f)+mass/(radius**2*root_f)
        lapse_gradient=lapse*(mass/(radius**2*root_f**2)+coupling*energy/radius)
        kernel_gradient=-lapse*root_f*energy_rate-lapse*reservoir_rate
        flux=-coupling*root_f*kernel/lapse
        flux_gradient=-coupling*((root_gradient/lapse-root_f*lapse_gradient/lapse**2)*kernel+root_f*kernel_gradient/lapse)
        tangent_operator=coupling*(2*energy/radius+reservoir/(radius*root_f))
        check('Ward_identity_propagates_full_polar_mass_equation',sp.simplify(flux_gradient+tangent_operator*flux-coupling*(root_f**2*energy_rate+root_f*reservoir_rate))==0)
        prior=json.loads((intake/'annular-clock-reservoir-coupling-attempt01/status.json').read_text())
        baseline={row['label']:row for row in prior['cases']}
        matched=json.loads((intake/'annular-common-source-history-attempt01/status.json').read_text())
        for row in [entry for entry in matched['cases'] if entry['case']==0]:
            branch,label=row['branch'],row['label']
            source_path=root/'source-intake/navier-stokes/20260912/annular-interface-layer-clock-attempt03'/(branch+'_source_snapshot.npz')
            prepared_path=intake/'annular-finite-width-boundary-cut-attempt01'/(branch+'_0_prepared_collar.npz')
            history_path=root/'source-intake/navier-stokes/20260910/annular-parent-root-residence-attempt02'/('canonical_N16_'+branch+'_sample0.npz')
            with np.load(source_path,allow_pickle=False) as archive:
                source={key:archive[key].copy() for key in archive.files}
            with np.load(prepared_path,allow_pickle=False) as archive:
                prepared={key:archive[key].copy() for key in archive.files}
            with np.load(history_path,allow_pickle=False) as archive:
                clock=archive['affine_clock'].copy()
                outer_acceleration=float(archive['endpoint_acceleration'][-1])
            preparation=ExteriorModePreparation(source,branch!='GR',prepared['kinetic_seed'],float(prepared['outer_clock']),prepared['drive'],row['width'],row['shape'],reservoir_energy=row['reservoir_energy'],base_coefficients=baseline[label]['coefficients'])
            model=preparation.build(row['exterior_amplitudes'])
            driver=ProperClockDrive(model,float(clock[1]),outer_acceleration,degree=64)
            old_jet=FixedInnerClockJet(model,driver,degree=64,primitive_degree=44)
            cases=[(12,2e-8,2)] if arguments.stage=='pilot' else [(12,2e-8,2),(12,2e-11,4),(16,2e-11,4)]
            for degree,tolerance,steps in cases:
                name=branch+'_degree'+str(degree)+'_steps'+str(steps)
                report['active_case']=name
                save()
                system=HorizontalEvolution(model,driver,clock,degree=degree)
                started=time.monotonic()
                initial=system.evaluate(0.,system.initial_state)
                evaluation_seconds=time.monotonic()-started
                probe=np.unique(np.concatenate([model.radii,np.linspace(model.radii[0],model.radii[-1],37)]))
                original=old_jet.first_fields(probe)
                old_second=old_jet.current_second(probe)
                anchor_g=model.metric(np.array([model.radii[-1]]))['g'][0]
                time_scale=np.exp(original['g']-anchor_g)
                time_second=np.exp(original['g']-2*anchor_g)*(old_jet.primitive(probe)-old_jet.primitive(np.array([model.radii[-1]]))[0])
                new_metric=initial['geometry'].metric(probe)
                metric_error=float(max(abs(new_metric['mu']-original['mu']).max(),abs(new_metric['N']-time_scale*original['N']).max()))
                first_error=float(abs(system.mass_flux(initial,probe)-time_scale*original['mu1']).max())
                differential=system.differential_control(0.,system.initial_state,initial,probe)
                expected_second=time_scale**2*(old_second['mu2']+model.coupling**2*probe*original['U']**6*original['P1']**2)+time_second*original['mu1']
                second_error=float(abs(differential['mass_flux_rate']-expected_second).max())
                lapse_rate_error=float(abs(differential['metric_rate']['N']/new_metric['N']-(time_scale*original['L']+time_second/time_scale)).max())
                old_scalar=old_jet.transport_jet(system.grid.offsets)
                scalar_scale=np.exp(old_scalar['metric1']['g']-anchor_g)
                new_p_rate=initial['data']['Gchi']/system.node_weights
                new_p_rate[:,-1]=initial['source_p_rate']
                scalar_error=float(max(abs(initial['data']['q']-scalar_scale*old_scalar['q']).max(),abs(new_p_rate-scalar_scale*old_scalar['p1_driven']).max()))
                initial_report={'initial_metric_pullback_error':metric_error,'initial_mass_rate_pullback_error':first_error,
                                'initial_mass_acceleration_pullback_error':second_error,'initial_lapse_rate_pullback_error':lapse_rate_error,
                                'initial_scalar_rates_pullback_error':scalar_error,'initial_full_mass_equation_error':differential['mass_equation_error'],
                                'single_evaluation_seconds':evaluation_seconds,'initial_minimum_F':initial['geometry'].minimum_F,
                                'state_dimension':len(system.initial_state),'radial_degree':system.radial_rule.degree}
                result={'label':name,'branch':branch,'degree':degree,'temporal_tolerance':tolerance,'maximum_step_divisor':steps,
                        'exterior_amplitudes':row['exterior_amplitudes'],'initial':initial_report}
                report['cases'].append(result)
                save()
                print(json.dumps({'label':name,'initial':initial_report}),flush=True)
                check(name+'_saved_initial_geometry_and_flux_are_retained',max(metric_error,first_error)<1e-9)
                check(name+'_actual_first_and_second_equations_match_the_clock_pullback',max(scalar_error,second_error,lapse_rate_error,differential['mass_equation_error'])<1e-8)
                if arguments.stage=='pilot':
                    result['state']='pilot_complete'
                    save()
                    continue
                duration=.004
                completed=solve_ivp(system.rhs,(0.,duration),system.initial_state,method='DOP853',rtol=tolerance,atol=tolerance/100,max_step=duration/steps,dense_output=True)
                check(name+'_live_coupled_integration_completed',completed.success,completed.message)
                samples=np.array([0.,.0005,.001,.002,.004])
                states=completed.sol(samples)
                diagnostics=[]
                original_inner=model.metric(np.array([model.radii[0]]))
                proper_mass_rate=prepared['drive'][0]/original_inner['N'][0]
                initial_total_mass=initial['geometry'].metric(np.array([model.edges[-1]]))['mu'][0]
                for time_value,state in zip(samples,states.T):
                    evaluation=system.evaluate(time_value,state)
                    cut=evaluation['geometry'].metric(model.radii[[0,-1]])
                    inner_clock=system.unpack(state)[1]
                    inner_target=source['mu'][0]+proper_mass_rate*inner_clock
                    full_mass_error=None
                    if time_value in [0.,.002,.004]:
                        full_mass_error=system.differential_control(time_value,state,evaluation,probe)['mass_equation_error']
                    diagnostics.append({'time':float(time_value),'inner_proper_clock':float(inner_clock),'inner_mass':float(cut['mu'][0]),
                                        'inner_affine_proper_history_error':float(cut['mu'][0]-inner_target),
                                        'outer_total_mass_drift':float(evaluation['geometry'].metric(np.array([model.edges[-1]]))['mu'][0]-initial_total_mass),
                                        'minimum_F':evaluation['geometry'].minimum_F,'minimum_reservoir_energy':float(evaluation['data']['energy'].min()),
                                        'radial_collocation_defect':evaluation['geometry'].collocation_defect,'full_mass_equation_error':full_mass_error,
                                        'outer_clock_error':float(cut['N'][-1]/cut['U'][-1]-(clock[0]+clock[1]*time_value))})
                    save()
                works=[system.temporal_work(completed,duration,order=order) for order in [8,12]]
                result.update({'state':'evolved','duration':duration,'solver_steps':len(completed.t)-1,'rhs_calls':system.calls,
                               'elapsed_seconds':time.monotonic()-started,'diagnostics':diagnostics,'temporal_work':works,
                               'final_state_norm':float(np.linalg.norm(completed.y[:,-1]))})
                path=destination/(name+'_evolution.npz')
                np.savez_compressed(path,times=samples,states=states,solver_times=completed.t,solver_states=completed.y,
                                    offsets=system.grid.offsets,source_profile_left=system.source_profile[0],source_profile_right=system.source_profile[1],
                                    exterior_amplitudes=row['exterior_amplitudes'],initial_state=system.initial_state)
                own(path,'outputs')
                save()
                check(name+'_positive_chart_and_positive_source_energy',min(entry['minimum_F'] for entry in diagnostics)>.1 and min(entry['minimum_reservoir_energy'] for entry in diagnostics)>0)
                check(name+'_full_mass_equation_on_live_states',max(entry['full_mass_equation_error'] or 0 for entry in diagnostics)<1e-8)
                check(name+'_closed_outer_mass_and_clock_are_preserved',max(max(abs(entry['outer_total_mass_drift']),abs(entry['outer_clock_error'])) for entry in diagnostics)<1e-9)
                check(name+'_scalar_and_source_temporal_endpoint_work_retained',max(entry['error'] for entry in works)<1e-9 and min(entry['omitted_clock_work_error'] for entry in works)>1e-8)
                print(json.dumps({'label':name,'elapsed_seconds':result['elapsed_seconds'],'diagnostics':diagnostics,'temporal_work':works}),flush=True)
        for module in tuple(sys.modules.values()):
            filename=getattr(module,'__file__',None)
            if filename:
                path=Path(filename).resolve()
                if path.parent==root/'scripts' and path.suffix=='.py':
                    own(path)
        check('no_python_cache',not(root/'scripts/__pycache__').exists())
        report['conditional_live_evolution_complete']=arguments.stage=='evolve' and len(report['cases'])==6 and all(row.get('state')=='evolved' for row in report['cases'])
        report['state']='complete'
        save()
        print(json.dumps({'state':report['state'],'cases':len(report['cases']),'checks':len(report['checks']),'stage':arguments.stage}),flush=True)
    except Exception as error:
        report.update({'state':'failed','error':repr(error),'traceback':traceback.format_exc()})
        save()
        raise


if __name__=='__main__':
    run()
