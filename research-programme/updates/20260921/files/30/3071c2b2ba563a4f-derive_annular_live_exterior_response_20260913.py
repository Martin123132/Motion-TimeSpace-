import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_live_exterior_response_20260913 import LiveExteriorResponse, load_prepared_system, OUTPUT_NAMES, PROBE_NAMES

    root=Path(__file__).resolve().parents[1]
    intake=root/'source-intake/navier-stokes/20260913'
    destination=intake/'annular-live-exterior-response-attempt01'
    destination.mkdir(exist_ok=False)
    report={'state':'running','checks':[],'cases':[],'inputs':{},'outputs':{},'finite_probes':[],
            'valid_for_physics_claim':False,'full_GR_limit_proven':False,'trace_only_physical_port_derived':False,
            'global_causal_wellposedness_proven':False,'original_affine_inner_history_enforced':False,
            'new_forcing_added':False,'baseline_refitted':False,'apparatus_support_stresses_derived':False,
            'closed_enlarged_support_retained':True,'retained_input_is_full_state_history_not_just_a_trace':True,
            'nonlinear_exterior_replay_complete':False,'live_linear_memory_tested':False,
            'output_names':OUTPUT_NAMES,'probe_names':PROBE_NAMES,
            'perturbations_are_validation_initial_states_not_new_preparations':True}

    def save():
        (destination/'status.json').write_text(json.dumps(report,indent=2)+'\n')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))]=hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    save()
    try:
        previous_path=intake/'annular-horizontal-clock-final-integrity.json'
        previous=json.loads(previous_path.read_text())
        check('previous_live_evolution_seal_complete',previous['state']=='complete' and previous['conditional_live_evolution_complete'] and all(row['passed'] for row in previous['checks']))
        for table in ['inputs','outputs']:
            for filename,expected in previous[table].items():
                if filename not in report['inputs']:
                    if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed inherited source: '+filename)
                    report['inputs'][filename]=expected
        own(previous_path)
        for path in [Path(__file__),root/'scripts/annular_live_exterior_response_20260913.py']:
            compile(path.read_bytes(),str(path),'exec')
            own(path)
            snapshot=destination/('executed-'+path.name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot,'outputs')
        for branch in ['GR','metric_Gram']:
            report['active_branch']=branch
            report['phase']='baseline_and_full_tangents'
            save()
            system,matched=load_prepared_system(root,branch)
            response=LiveExteriorResponse(system)
            baseline=response.integrate()
            with np.load(intake/'annular-horizontal-clock-evolve-attempt01'/(branch+'_degree16_steps4_evolution.npz'),allow_pickle=False) as archive:
                recovery=float(abs(baseline.sol(archive['times'])-archive['states']).max())
                check(branch+'_baseline_state_not_refitted',np.array_equal(system.initial_state,archive['initial_state']) and recovery<1e-10,recovery)
            tangent=response.integrate_tangents(baseline)
            probes_times=np.linspace(0.,response.duration,9)
            replay,nonlinear_outputs=response.reduced_replay(baseline,probes_times)
            check(branch+'_nonlinear_exterior_elimination_replays_live_baseline',max(max(entry['exterior_error'],entry['output_error'],entry['retained_equation_discrepancy']) for entry in replay)<1e-8,replay)
            record={'branch':branch,'exterior_dimension':response.exterior_size,'retained_dimension':int(response.retained.sum()),
                    'exterior_amplitudes':matched['exterior_amplitudes'],'nonlinear_baseline_replay':replay}
            report['cases'].append(record)
            report['phase']='live_operator_sampling'

            def progress(completed,total):
                report['operator_nodes_completed']=completed
                report['operator_nodes_total']=total
                save()
                print(branch+' operator node '+str(completed)+'/'+str(total),flush=True)

            samples=response.sample_operator(baseline,tangent,progress=progress)
            fine=response.memory_replay(samples)
            coarse=response.memory_replay(samples,stride=2)
            frozen=response.memory_replay(samples,frozen=True)
            expected=samples['full_tangent_states'][:,response.exterior,:]
            exterior_error=float(abs(fine['exterior_tangents']-expected).max())
            output_error=float(abs(fine['predicted']-samples['full_output_tangent']).max())
            refinement=float(abs(fine['predicted']-coarse['predicted']).max())
            check(branch+'_live_memory_reconstructs_full_exterior_tangents',exterior_error<1e-8,exterior_error)
            check(branch+'_live_memory_reconstructs_full_observable_tangents',output_error<1e-8,output_error)
            check(branch+'_operator_time_refinement_without_retuning',refinement<1e-8,refinement)
            integral,transitions=response.terminal_duhamel(fine)
            values=fine['solution'].sol(response.duration).reshape(response.exterior_size,response.exterior_size+3)
            integral_error=float(abs(integral-values[:,response.exterior_size:]).max())
            check(branch+'_independent_Duhamel_quadrature_recovers_driven_state',integral_error<1e-8,integral_error)
            no_initial=float(abs(fine['initial_contribution'][:,0,0]).max())
            no_memory=float(abs(fine['memory_contribution'][:,0,1]).max())
            frozen_error=float(abs(frozen['predicted'][:,0,:]-samples['full_output_tangent'][:,0,:]).max())
            check(branch+'_initial_exterior_state_term_is_necessary',no_initial>1e-7,no_initial)
            check(branch+'_driven_memory_term_is_necessary',no_memory>1e-8,no_memory)
            check(branch+'_frozen_response_is_distinguishable_not_adopted',frozen_error>max(100*output_error,1e-10),frozen_error)
            balance=response.balances(baseline,tangent)
            tangent_balance=float(abs(np.asarray(balance['tangent_balance_errors'])).max())
            check(branch+'_live_nonlinear_mass_and_source_energy_balances',max(balance['mass_balance_error'],balance['source_energy_balance_error'],abs(balance['total_mass_change']))<1e-10,balance)
            check(branch+'_linearized_mass_and_source_energy_balances',tangent_balance<1e-10,tangent_balance)
            check(branch+'_metric_weight_must_not_be_frozen',max(abs(np.asarray(balance['omitted_metric_weight_contributions'])))>max(100*tangent_balance,1e-15),balance['omitted_metric_weight_contributions'])
            record.update({'exterior_tangent_error':exterior_error,'observable_tangent_error':output_error,'operator_refinement_error':refinement,
                           'Duhamel_error':integral_error,'omitted_initial_current_error':no_initial,'omitted_memory_current_error':no_memory,
                           'frozen_current_error':frozen_error,'balances':balance,'operator_time_change':float(abs(samples['Aee'][-1]-samples['Aee'][0]).max())})
            path=destination/(branch+'_live_operator.npz')
            np.savez_compressed(path,**samples,exterior_indices=response.exterior,retained_mask=response.retained,initial_directions=response.directions,
                                reference_states=baseline.sol(samples['times']),nonlinear_replay_times=probes_times,nonlinear_replay_outputs=nonlinear_outputs,
                                memory_prediction=fine['predicted'],memory_initial=fine['initial_contribution'],memory_driven=fine['memory_contribution'],
                                propagators=fine['propagators'],exterior_tangent_replay=fine['exterior_tangents'],
                                coarse_prediction=coarse['predicted'],frozen_prediction=frozen['predicted'],terminal_transitions=transitions)
            own(path,'outputs')
            save()
            report['phase']='nonlinear_finite_perturbation_controls'
            exact_tangent=tangent.sol(response.duration).reshape(response.directions.shape)
            exact_output=samples['full_output_tangent'][-1]
            for index,name in enumerate(PROBE_NAMES):
                for amplitude in [.001,.0005]:
                    solutions=[]
                    output_values=[]
                    energy_controls=[]
                    for sign in [-1.,1.]:
                        initial=system.initial_state+sign*amplitude*response.directions[:,index]
                        solution=response.integrate(initial)
                        solutions.append(solution)
                        output_values.append(response.outputs(system.evaluate(response.duration,solution.sol(response.duration))))
                        initial_outputs=response.outputs(system.evaluate(0.,initial))
                        trajectory=solution.sol(probes_times)
                        energy_controls.append({'sign':sign,'initial_total_mass_change_from_baseline':float(initial_outputs[6]-samples['baseline_outputs'][0,6]),
                                                'initial_source_energy_change_from_baseline':float(initial_outputs[4]-samples['baseline_outputs'][0,4]),
                                                'total_mass_drift':float(output_values[-1][6]-initial_outputs[6]),
                                                'minimum_source_energy':float(min(system.unpack(state)[0][:,-1].min() for state in trajectory.T))})
                        if name=='adjacent_interior_momentum' and amplitude==.001 and sign==1:
                            replay_rows,unused_outputs=response.reduced_replay(solution,probes_times)
                            check(branch+'_nonlinear_response_also_replays_perturbed_retained_history',max(max(entry['exterior_error'],entry['output_error'],entry['retained_equation_discrepancy']) for entry in replay_rows)<1e-8,replay_rows)
                            record['perturbed_nonlinear_replay']=replay_rows
                        saved=destination/(branch+'_'+name+'_'+str(amplitude)+'_'+('plus' if sign>0 else 'minus')+'.npz')
                        np.savez_compressed(saved,times=probes_times,states=solution.sol(probes_times),initial_state=initial,final_outputs=output_values[-1])
                        own(saved,'outputs')
                    derivative=(solutions[1].sol(response.duration)-solutions[0].sol(response.duration))/(2*amplitude)
                    output_derivative=(output_values[1]-output_values[0])/(2*amplitude)
                    state_error=float(abs(derivative-exact_tangent[:,index]).max())
                    observation_error=float(abs(output_derivative-exact_output[:,index]).max())
                    check(branch+'_'+name+'_'+str(amplitude)+'_nonlinear_trajectories_confirm_linear_response',max(state_error,observation_error)<1e-7,{'state':state_error,'outputs':observation_error})
                    check(branch+'_'+name+'_'+str(amplitude)+'_perturbation_energy_is_recorded_and_conserved',max(abs(entry['total_mass_drift']) for entry in energy_controls)<1e-10 and min(entry['minimum_source_energy'] for entry in energy_controls)>0,energy_controls)
                    report['finite_probes'].append({'branch':branch,'probe':name,'amplitude':amplitude,'state_derivative_error':state_error,'output_derivative_error':observation_error,'energy_controls':energy_controls})
                    save()
            record['state']='complete'
            save()
            print(json.dumps(record),flush=True)
        for module in tuple(sys.modules.values()):
            filename=getattr(module,'__file__',None)
            if filename:
                path=Path(filename).resolve()
                if path.parent==root/'scripts' and path.suffix=='.py':
                    own(path)
        check('no_python_cache',not(root/'scripts/__pycache__').exists())
        report.update({'state':'complete','nonlinear_exterior_replay_complete':True,'live_linear_memory_tested':True})
        save()
        print(json.dumps({'state':report['state'],'cases':len(report['cases']),'checks':len(report['checks'])}),flush=True)
    except Exception as error:
        report.update({'state':'failed','error':repr(error),'traceback':traceback.format_exc()})
        save()
        raise


if __name__=='__main__':
    run()
