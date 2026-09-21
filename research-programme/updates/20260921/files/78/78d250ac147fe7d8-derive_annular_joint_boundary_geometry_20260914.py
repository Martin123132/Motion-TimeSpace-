import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from scipy.integrate import solve_ivp
    from annular_live_exterior_response_20260913 import load_prepared_system, TimeFit
    from annular_joint_boundary_geometry_20260914 import ProtocolEvolution, JointSchurResponse

    root = Path(__file__).resolve().parents[1]
    prior = root/'source-intake/navier-stokes/20260913'
    destination = root/'source-intake/navier-stokes/20260914/annular-joint-boundary-geometry-attempt01'
    destination.mkdir(parents=True,exist_ok=False)
    report = {'state':'running','checks':[],'inputs':{},'outputs':{},'cases':[],
              'valid_for_physics_claim':False,'full_GR_limit_proven':False,
              'one_point_boundary_action_derived':False,'continuum_wellposedness_proven':False,
              'apparatus_support_stresses_derived':False,'original_affine_inner_history_enforced':False,
              'new_parent_coefficient_fitted':False,'baseline_refitted':False,
              'parameter_is_declared_apparatus_history_probe':True,'perturbed_metric_histories_supplied':False,
              'conditional_joint_boundary_geometry_complete':False,'protocol':'D_eta(theta)=D0+V0*theta+aProper*theta^2/2+eta*theta^3/6',
              'parameters':[-1.,-.5,.5,1.]}

    def save():
        (destination/'status.json').write_text(json.dumps(report,indent=2)+'\n')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail})
        save()
        if not passed:
            raise RuntimeError(name+': '+repr(detail))

    def arrays(path,**values):
        np.savez_compressed(path,**values)
        own(path,'outputs')
        save()

    save()
    try:
        seal_path = prior/'annular-live-exterior-response-final-integrity.json'
        seal = json.loads(seal_path.read_text())
        check('previous_response_seal_complete',seal['state']=='complete' and all(row['passed'] for row in seal['checks']))
        for table in ['inputs','outputs']:
            for filename,expected in seal[table].items():
                if filename not in report['inputs']:
                    if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed inherited source: '+filename)
                    report['inputs'][filename] = expected
        own(seal_path)
        for path in [Path(__file__),root/'scripts/annular_joint_boundary_geometry_20260914.py']:
            compile(path.read_bytes(),str(path),'exec')
            own(path)
            copied = destination/('executed-'+path.name)
            copied.write_bytes(path.read_bytes())
            own(copied,'outputs')
        for branch in ['GR','metric_Gram']:
            report['active_branch'] = branch
            report['phase'] = 'build_live_Schur_blocks'
            save()
            base,matched = load_prepared_system(root,branch)
            system = ProtocolEvolution(base)
            with np.load(prior/'annular-live-exterior-response-attempt01'/(branch+'_live_operator.npz'),allow_pickle=False) as archive:
                samples = {key:archive[key].copy() for key in archive.files}
            baseline_error = max(float(abs(base.evaluate(time,state)['rhs']-system.evaluate(time,state)['rhs']).max())
                                 for time,state in zip(samples['times'],samples['reference_states'].T))
            initial = system.initial_state
            initial_error = max(float(abs(system.evaluate_protocol(0.,initial,parameter)['rhs']-system.evaluate(0.,initial)['rhs']).max()) for parameter in report['parameters'])
            check(branch+'_baseline_and_initial_state_not_changed',np.array_equal(initial,samples['reference_states'][:,0]) and max(baseline_error,initial_error)<1e-12,
                  {'baseline_rhs_error':baseline_error,'initial_protocol_rhs_error':initial_error})

            def progress(completed,total):
                report['nodes_completed'],report['nodes_total'] = completed,total
                save()
                print(branch+' Schur block '+str(completed)+'/'+str(total),flush=True)

            fine = JointSchurResponse(system,samples,progress=progress)
            report['phase'] = 'predict_unknown_coupled_response'
            save()
            tangent,linear_record = fine.linear_response()
            output_tangent = fine.output_tangent(tangent)
            check(branch+'_joint_Schur_linear_residual',max(linear_record['schur_residual'],linear_record['full_collocation_residual'])<1e-10,linear_record)
            coarse = JointSchurResponse(system,samples,stride=2,full_exterior_columns=fine.columns)
            coarse_tangent,coarse_record = coarse.linear_response()
            refinement = float(abs(coarse_tangent-tangent[::2]).max())
            check(branch+'_joint_temporal_refinement_without_retuning',refinement<1e-9,refinement)
            one_way,one_way_record = fine.linear_response(coupled=False)
            one_way_output = fine.output_tangent(one_way)
            check(branch+'_source_protocol_has_nonzero_predicted_response',float(abs(tangent).max())>1e-8,float(abs(tangent).max()))
            arrays(destination/(branch+'_predicted_response_before_reference.npz'),times=fine.times,baseline_states=fine.states,
                   source_forcing=fine.forcing,exterior_columns=fine.columns,integration=fine.integration,exterior_indices=fine.exterior,
                   retained_mask=fine.retained,joint_tangent=tangent,output_tangent=output_tangent,
                   coarse_tangent=coarse_tangent,one_way_tangent=one_way,one_way_output=one_way_output)
            record = {'branch':branch,'linear_solver':linear_record,'coarse_solver':coarse_record,
                      'temporal_refinement_error':refinement,'finite_protocols':[],
                      'one_way_tangent_difference':float(abs(one_way-tangent).max()),
                      'one_way_output_difference':float(abs(one_way_output-output_tangent).max())}
            report['cases'].append(record)
            report['phase'] = 'nonlinear_joint_closure_before_reference'
            save()
            for parameter in report['parameters']:
                states,history = fine.nonlinear_response(parameter,tangent)
                outputs = np.stack([fine.response.outputs(system.evaluate_protocol(time,state,parameter)) for time,state in zip(fine.times,states)])
                fit = TimeFit(states,fine.duration)
                derivative_coefficients = np.polynomial.chebyshev.chebder(fit.coefficients,axis=0)*2/fine.duration
                offnode = []
                for time in [.00071,.00213,.00369]:
                    derivative = np.polynomial.chebyshev.chebval(2*time/fine.duration-1,derivative_coefficients)
                    rhs = system.evaluate_protocol(time,fit(time),parameter)['rhs']
                    offnode.append(float((abs(derivative-rhs)/(1+abs(rhs))).max()))
                check(branch+'_'+str(parameter)+'_nonlinear_joint_closure',history[-1]['nonlinear_collocation_residual']<5e-13 and max(offnode)<2e-7,
                      {'history':history,'offnode_scaled_differential_residual':offnode})
                key = str(parameter).replace('-','minus')
                arrays(destination/(branch+'_joint_protocol_'+key+'.npz'),times=fine.times,states=states,outputs=outputs,parameter=np.array(parameter))
                record['finite_protocols'].append({'parameter':parameter,'joint_iterations':history,'offnode_scaled_residual':offnode})
            report['phase'] = 'independent_fresh_coupled_references'
            save()
            reference = system.integrate_protocol(0.)
            recovered = float(abs(reference.sol(fine.times).T-fine.states).max())
            check(branch+'_fresh_baseline_recovers_saved_baseline',recovered<1e-10,recovered)

            def tangent_equation(time,direction):
                return system.evaluate_protocol(time,reference.sol(time)+1j*1e-20*direction,1j*1e-20)['rhs'].imag/1e-20

            direct = solve_ivp(tangent_equation,(0.,fine.duration),np.zeros(fine.size),method='DOP853',
                               rtol=2e-12,atol=2e-14,max_step=fine.duration/8,dense_output=True)
            check(branch+'_fresh_full_tangent_integrator_converges',direct.success,direct.message)
            direct_states = direct.sol(fine.times).T
            direct_outputs = np.stack([fine.response.outputs(system.evaluate_protocol(time,reference.sol(time)+1j*1e-20*direction,1j*1e-20)).imag/1e-20
                                       for time,direction in zip(fine.times,direct_states)])
            tangent_error = float(abs(direct_states-tangent).max())
            observation_error = float(abs(direct_outputs-output_tangent).max())
            check(branch+'_predicted_joint_response_matches_fresh_full_tangent',max(tangent_error,observation_error)<1e-9,
                  {'state':tangent_error,'outputs':observation_error})
            record.update({'fresh_tangent_error':tangent_error,'fresh_output_tangent_error':observation_error,
                           'one_way_feedback_effect_resolved':record['one_way_output_difference']>max(100*observation_error,1e-14)})
            arrays(destination/(branch+'_fresh_tangent_reference.npz'),times=fine.times,states=direct_states,outputs=direct_outputs,baseline_states=reference.sol(fine.times).T)
            terminal = {}
            points,weights = np.polynomial.legendre.leggauss(16)
            for item in record['finite_protocols']:
                parameter = item['parameter']
                key = str(parameter).replace('-','minus')
                with np.load(destination/(branch+'_joint_protocol_'+key+'.npz'),allow_pickle=False) as archive:
                    predicted = archive['states'].copy()
                    predicted_outputs = archive['outputs'].copy()
                reference = system.integrate_protocol(parameter)
                states = reference.sol(fine.times).T
                outputs = np.stack([fine.response.outputs(system.evaluate_protocol(time,state,parameter)) for time,state in zip(fine.times,states)])
                mass_integral,energy_integral = 0.,0.
                for time,weight in zip(fine.duration*(points+1)/2,fine.duration*weights/2):
                    output = fine.response.outputs(system.evaluate_protocol(time,reference.sol(time),parameter))
                    mass_integral += weight*output[3]
                    energy_integral += weight*output[5]
                balances = {'inner_mass':float(abs(outputs[-1,1]-outputs[0,1]-mass_integral)),
                            'source_energy':float(abs(outputs[-1,4]-outputs[0,4]-energy_integral)),
                            'total_mass_drift':float(abs(outputs[:,6]-outputs[0,6]).max()),
                            'minimum_source_energy':float(min(system.unpack(state)[0][:,-1].min() for state in states))}
                state_error = float(abs(states-predicted).max())
                output_error = float(abs(outputs-predicted_outputs).max())
                check(branch+'_'+str(parameter)+'_nonlinear_joint_prediction_matches_fresh_evolution',max(state_error,output_error)<1e-9,
                      {'states':state_error,'outputs':output_error})
                check(branch+'_'+str(parameter)+'_source_and_mass_budget_retained',
                      max(balances['inner_mass'],balances['source_energy'],balances['total_mass_drift'])<1e-10 and balances['minimum_source_energy']>0,balances)
                arrays(destination/(branch+'_fresh_protocol_'+key+'.npz'),times=fine.times,states=states,outputs=outputs,initial_state=system.initial_state,parameter=np.array(parameter))
                item.update({'fresh_state_error':state_error,'fresh_output_error':output_error,'balances':balances})
                terminal[parameter] = states[-1],outputs[-1]
                save()
            finite_derivatives = []
            for amplitude in [1.,.5]:
                state_derivative = (terminal[amplitude][0]-terminal[-amplitude][0])/(2*amplitude)
                observable_derivative = (terminal[amplitude][1]-terminal[-amplitude][1])/(2*amplitude)
                errors = {'amplitude':amplitude,'state':float(abs(state_derivative-tangent[-1]).max()),
                          'outputs':float(abs(observable_derivative-output_tangent[-1]).max())}
                check(branch+'_'+str(amplitude)+'_finite_protocol_derivative_confirms_prediction',max(errors['state'],errors['outputs'])<1e-9,errors)
                finite_derivatives.append(errors)
            record.update({'state':'complete','finite_protocol_derivatives':finite_derivatives,'linear_solves':fine.linear_solves})
            print(json.dumps(record),flush=True)
            save()
        for module in tuple(sys.modules.values()):
            filename = getattr(module,'__file__',None)
            if filename:
                path = Path(filename).resolve()
                if path.parent==root/'scripts' and path.suffix=='.py':
                    own(path)
        check('no_python_cache',not(root/'scripts/__pycache__').exists())
        report.update({'state':'complete','conditional_joint_boundary_geometry_complete':True})
        save()
        print(json.dumps({'state':report['state'],'checks':len(report['checks']),'cases':len(report['cases'])}),flush=True)
    except Exception as error:
        report.update({'state':'failed','error':repr(error),'traceback':traceback.format_exc()})
        save()
        raise


if __name__=='__main__':
    run()

