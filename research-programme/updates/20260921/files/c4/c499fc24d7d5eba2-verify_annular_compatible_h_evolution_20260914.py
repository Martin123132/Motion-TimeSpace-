import hashlib
import json
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    import sympy as symbolic
    from annular_compatible_h_evolution_20260914 import CompatibleEvolution,gram_energy_triplet,regular_chart_constants
    from annular_gram_velocity_commutator_20260914 import velocity_commutator,adaptive_energy_integral
    from annular_gram_geometry_bound_20260914 import propagation_bounds
    from annular_finite_width_bulk_current_20260913 import shape_weight
    from annular_covariant_scalar_action_20260912 import full_spatial_factors

    root=Path(__file__).resolve().parents[1]
    intake=root/'source-intake/navier-stokes/20260914'
    main_dir=intake/'annular-compatible-h-evolution-main-attempt01'
    output=intake/'annular-compatible-h-evolution-independent-attempt01'
    output.mkdir(exist_ok=False)
    report={'state':'running','checks':[],'inputs':{},'outputs':{},'cases':[],
            'full_GR_limit_proven':False,'uniform_H3_solution_bound_proven':False,
            'uniform_in_h_dynamical_energy_estimate_proven':False,'valid_for_physics_claim':False}

    def save():
        (output/'status.json').write_text(json.dumps(report,indent=2)+'\n')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def fields(system,time,state,radii,offsets):
        geometry=system.geometry(time,state)
        metric=geometry.metric(radii)
        data=geometry.layer(offsets)
        return np.stack([metric['mu'],metric['log_N']]),np.stack([data['chi'],data['p']])

    def rk4(system,duration,steps):
        state=system.initial_state.copy()
        step=duration/steps
        for index in range(steps):
            time=index*step
            first=system.rhs(time,state)
            second=system.rhs(time+step/2,state+step*first/2)
            third=system.rhs(time+step/2,state+step*second/2)
            fourth=system.rhs(time+step,state+step*third)
            state+=step*(first+2*second+2*third+fourth)/6
        return state

    def data_energy_bound(base_system,base_geometry,mts_geometry):
        points,weights=np.polynomial.legendre.leggauss(24)
        offsets=np.concatenate([-.25+.25*points,.25+.25*points])
        weights=np.concatenate([.25*weights,.25*weights])*shape_weight(offsets,base_system.shape)
        first=base_geometry.layer(offsets)
        second=mts_geometry.layer(offsets)
        factors,sampling=full_spatial_factors(len(base_system.radii),False)
        radius=first['R']
        def energy(scalar,momentum):
            potential=radius**2*((scalar @ factors.T)**2 @ sampling)/(2*base_system.spacing)
            kinetic=base_system.node_weights[None,:]*momentum**2/(2*radius**2)
            return float(weights @ (potential+kinetic).sum(axis=1))
        base_energy=energy(first['chi'],first['p'])
        mts_base_energy=energy(second['chi'],second['p'])
        error_energy=energy(second['chi']-first['chi'],second['p']-first['p'])
        extra=gram_energy_triplet(base_system,mts_geometry)[0]
        density_bound=extra+np.sqrt(error_energy)*(np.sqrt(base_energy)+np.sqrt(mts_base_energy))
        return {'base_energy':base_energy,'mts_base_energy':mts_base_energy,'state_error_energy':error_energy,
                'extra_energy':float(extra),'absolute_density_difference_bound':float(density_bound),
                **propagation_bounds(density_bound,0.)}

    save()
    try:
        main=json.loads((main_dir/'status.json').read_text())
        check('main_completed_six_trajectories',main['state']=='complete' and len(main['cases'])==6
              and len(main['comparisons'])==3 and all(row['passed'] for row in main['checks']))
        for table in ['inputs','outputs']:
            for filename,expected in main[table].items():
                if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                    raise RuntimeError('Changed evidence: '+filename)
                report['inputs'][filename]=expected
        own(main_dir/'status.json')
        check('main_and_predecessor_hashes_match',True)
        for path in [Path(__file__),root/'scripts/annular_compatible_h_evolution_20260914.py',
                     root/'scripts/annular_gram_velocity_commutator_20260914.py']:
            compile(path.read_bytes(),str(path),'exec')
            own(path)
        snapshot=output/('executed-'+Path(__file__).name)
        snapshot.write_bytes(Path(__file__).read_bytes())
        own(snapshot,'outputs')
        check('executed_helpers_and_verifier_compile',True)
        coefficient=symbolic.symbols('c0:4')
        momentum=symbolic.symbols('p0:4')
        def delta(values):
            return [second-first for first,second in zip(values[:-1],values[1:])]
        coefficient_first=delta(coefficient)
        coefficient_second=delta(coefficient_first)
        coefficient_third=delta(coefficient_second)
        momentum_first=delta(momentum)
        momentum_second=delta(momentum_first)
        momentum_third=delta(momentum_second)
        actual=delta(delta(delta([first*second for first,second in zip(coefficient,momentum)])))[0]
        expanded=coefficient[3]*momentum_third[0]+3*coefficient_first[2]*momentum_second[0]+3*coefficient_second[1]*momentum_first[0]+coefficient_third[0]*momentum[0]
        check('exact_discrete_third_product_identity',symbolic.expand(actual-expanded)==0)
        check('conditional_uniform_mass_barrier_remains_regular',regular_chart_constants()['F_lower_if_exact_mass_conserved']>.5,regular_chart_constants())
        mass_cap=regular_chart_constants()['full_support_mass_upper_bound']
        lapse_lower=np.sqrt(.5)*np.exp(-mass_cap*(1/4.9-1/6)/.5-(mass_cap-.8)/(4.9*.5))
        report['conditional_uniform_lapse_lower_bound']=float(lapse_lower)
        check('conditional_uniform_lapse_bound_positive',lapse_lower>0)
        for record in main['cases']:
            label=record['label']
            report['active_case']=label
            save()
            with np.load(main_dir/(label+'.npz'),allow_pickle=False) as archive:
                arrays={key:archive[key].copy() for key in archive.files}
            check(label+'_all_arrays_finite',all(np.isfinite(value).all() for value in arrays.values()))
            check(label+'_conditional_lapse_barrier_respected',arrays['minimums_and_defect'][:,1].min()>=lapse_lower)
            system=CompatibleEvolution(record['count'],record['gram'],degree=8)
            check(label+'_saved_initial_preparation_reproduced',np.array_equal(system.initial_state,arrays['states'][0]))
            case={'label':label,'commutators':[]}
            for index in [0,8,16]:
                time=arrays['times'][index]
                state=arrays['states'][index]
                geometry=system.geometry(time,state)
                diagnostic=velocity_commutator(system,geometry)
                check(label+'_local_product_bound_t'+str(index),
                      max(diagnostic['product_identity_error'],diagnostic['q_equals_coefficient_times_p_error'])<1e-12
                      and diagnostic['discrete_velocity_third_norm']<=diagnostic['local_product_bound']+1e-8
                      and diagnostic['rate_sqrt_over_h2']<=diagnostic['rate_sqrt_over_h2_bound']+1e-8,diagnostic)
                case['commutators'].append({'time':float(time),**diagnostic})
            time=record['duration']
            state=arrays['states'][-1]
            direction=system.rhs(time,state)
            step=1e-6
            plus=gram_energy_triplet(system,system.geometry(time,state+step*direction))[0]
            minus=gram_energy_triplet(system,system.geometry(time,state-step*direction))[0]
            expected=arrays['energies'][-1,2]
            derivative_error=abs((plus-minus)/(2*step)-expected)
            check(label+'_energy_rate_independent_directional_difference',
                  derivative_error<max(1e-10,abs(expected)*1e-6),float(derivative_error))
            case['energy_rate_difference_error']=float(derivative_error)
            check(label+'_source_boundary_work_zero_but_bulk_changes',record['max_scalar_and_momentum_change']>1e-5
                  and np.array_equal(system.unpack(state)[0][:,-1],system.unpack(system.initial_state)[0][:,-1]))
            if record['count'] in [33,129]:
                fine_system=CompatibleEvolution(record['count'],record['gram'],degree=12)
                fine_solution=fine_system.integrate(time,divisor=16,rtol=4e-12,atol=4e-14)
                fine_fields,fine_profiles=fields(fine_system,time,fine_solution.y[:,-1],arrays['radii'],arrays['offsets'])
                refinement={'fields':float(abs(fine_fields-arrays['fields'][-1]).max()),
                            'profiles':float(abs(fine_profiles-arrays['profiles'][-1]).max()),
                            'extra_energy':float(abs(gram_energy_triplet(fine_system,fine_system.geometry(time,fine_solution.y[:,-1]))[0]-arrays['energies'][-1,0]))}
                check(label+'_independent_layer_and_time_refinement',
                      refinement['fields']<2e-10 and refinement['profiles']<2e-7 and refinement['extra_energy']<1e-9,refinement)
                case['layer_time_refinement']=refinement
                archive_path=output/(label+'_degree12_refinement.npz')
                np.savez_compressed(archive_path,state=fine_solution.y[:,-1],fields=fine_fields,profiles=fine_profiles)
                own(archive_path,'outputs')
                if record['count']==33:
                    integral,error,evaluations=adaptive_energy_integral(fine_system,fine_solution,time,tolerance=1e-12)
                    initial_extra=gram_energy_triplet(fine_system,fine_system.geometry(0.,fine_system.initial_state))[0]
                    refined_bound=(np.sqrt(initial_extra)+integral[1])**2
                    change=abs(refined_bound-record['propagation_bound'])
                    check(label+'_energy_propagation_quadrature_refined_independently',error<1e-9 and change<1e-7,
                          {'error_estimate':error,'bound_change':float(change),'evaluations':evaluations})
                    case['refined_propagation_bound']=float(refined_bound)
            if record['count']==65:
                coarse=rk4(system,time,128)
                fine=rk4(system,time,256)
                independent_fields,independent_profiles=fields(system,time,fine,arrays['radii'],arrays['offsets'])
                errors={'state':float(abs(fine-state).max()),'time_refinement':float(abs(fine-coarse).max()),
                        'fields':float(abs(independent_fields-arrays['fields'][-1]).max()),
                        'profiles':float(abs(independent_profiles-arrays['profiles'][-1]).max())}
                check(label+'_independent_RK4',errors['state']<2e-7 and errors['time_refinement']<2e-6
                      and errors['fields']<2e-10 and errors['profiles']<2e-7,errors)
                case['RK4']=errors
                evaluation=system.evaluate(time,state)
                ward=system.differential_control(time,state,evaluation,system.radii)
                check(label+'_full_mass_evolution_Ward_identity',ward['mass_equation_error']<1e-9,float(ward['mass_equation_error']))
                case['mass_Ward_error']=float(ward['mass_equation_error'])
                archive_path=output/(label+'_RK4.npz')
                np.savez_compressed(archive_path,coarse=coarse,fine=fine,fields=independent_fields,profiles=independent_profiles)
                own(archive_path,'outputs')
            report['cases'].append(case)
            save()
            print(json.dumps(case),flush=True)
        for comparison in main['comparisons']:
            count=comparison['count']
            with np.load(main_dir/('comparison_count'+str(count)+'.npz'),allow_pickle=False) as archive:
                split_error=float(abs(archive['total']-archive['direct']-archive['feedback']).max())
                check('count'+str(count)+'_actual_trajectory_gap_retains_data_feedback',split_error<1e-13
                      and abs(archive['feedback']).max()>1e-10,
                      {'identity_error':split_error,'feedback_max':float(abs(archive['feedback']).max())})
            base_system=CompatibleEvolution(count,False)
            mts_system=CompatibleEvolution(count,True)
            with np.load(main_dir/('GR_control_count'+str(count)+'.npz'),allow_pickle=False) as archive:
                base_states=archive['states'].copy()
                times=archive['times'].copy()
                radii=archive['radii'].copy()
            with np.load(main_dir/('metric_Gram_count'+str(count)+'.npz'),allow_pickle=False) as archive:
                mts_states=archive['states'].copy()
            bounds=[]
            for index in [0,8,16]:
                base_geometry=base_system.geometry(times[index],base_states[index])
                mts_geometry=mts_system.geometry(times[index],mts_states[index])
                bound=data_energy_bound(base_system,base_geometry,mts_geometry)
                first=base_geometry.metric(radii)
                second=mts_geometry.metric(radii)
                mass_difference=float(abs(second['mu']-first['mu']).max())
                lapse_difference=float(abs(second['log_N']-first['log_N']).max())
                check('count'+str(count)+'_coupled_data_energy_geometry_bound_t'+str(index),
                      mass_difference<=bound['mass_difference_bound']+1e-11
                      and lapse_difference<=bound['log_lapse_difference_bound']+1e-11,
                      {'mass_difference':mass_difference,'log_lapse_difference':lapse_difference,**bound})
                bounds.append({'time':float(times[index]),**bound})
            report.setdefault('data_energy_bounds',[]).append({'count':count,'bounds':bounds})
        report['observed_orders']=main['orders']
        check('no_full_GR_or_uniform_dynamical_proof_promotion',not any(main[key] for key in
              ['full_GR_limit_proven','uniform_H3_solution_bound_proven','uniform_in_h_dynamical_energy_estimate_proven','valid_for_physics_claim']))
        check('no_python_cache',not (root/'scripts/__pycache__').exists())
        report['state']='complete'
        save()
        print(json.dumps({'state':report['state'],'checks':len(report['checks']),'cases':len(report['cases'])}),flush=True)
    except Exception as error:
        report.update(state='failed',error=repr(error),traceback=traceback.format_exc())
        save()
        raise


if __name__=='__main__':
    run()
