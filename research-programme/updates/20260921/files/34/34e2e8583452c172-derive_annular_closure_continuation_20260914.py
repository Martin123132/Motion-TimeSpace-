import hashlib
import json
import sys
import traceback
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as np
    from annular_live_exterior_response_20260913 import load_prepared_system,TimeFit
    from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
    from annular_joint_boundary_geometry_20260914 import ProtocolEvolution,JointSchurResponse
    from annular_closure_continuation_20260914 import PolynomialHistory,trajectory_diagnostics

    root = Path(__file__).resolve().parents[1]
    intake = root/'source-intake/navier-stokes/20260914'
    destination = intake/'annular-closure-continuation-attempt01'
    destination.mkdir(exist_ok=False)
    duration = .032
    report = {'state':'running','checks':[],'inputs':{},'outputs':{},'cases':[],'comparisons':[],'failures':[],
              'duration':duration,'layer_degrees':[12,16,20],'temporal_degrees':[16,32],'parameters':[-1.,0.,1.],
              'valid_for_physics_claim':False,'full_GR_limit_proven':False,'regulator_removed':False,
              'continuum_limit_proven':False,'global_stability_proven':False,'horizon_crossing_proven':False,
              'original_affine_inner_history_enforced':False,'baseline_refitted':False,
              'perturbed_metric_histories_supplied':False,'initial_amplitudes_retuned':False,
              'physical_spacing_and_width_fixed':True,'conditional_continuation_complete':False}

    def save():
        (destination/'status.json').write_text(json.dumps(report,indent=2)+'\n')

    def own(path,table='inputs'):
        report[table][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def check(name,passed,detail=None,fatal=True):
        report['checks'].append({'name':name,'passed':bool(passed),'detail':detail,'fatal':fatal})
        save()
        if not passed and fatal:
            raise RuntimeError(name+': '+repr(detail))

    def gate(name,passed,detail=None):
        check(name,passed,detail,fatal=False)

    def store_arrays(path,arrays):
        np.savez_compressed(path,**arrays)
        own(path,'outputs')
        save()

    def diagnostics_gate(name,values):
        gate(name,values['minimum_F_sampled']>.1 and values['minimum_N_sampled']>0
             and values['minimum_source_energy_sampled']>0
             and max(values['radial_constraint_defect'],values['live_mass_law_error'],values['total_mass_drift'],
                     values['inner_mass_balance_error'],values['source_energy_balance_error'])<1e-9,values)

    save()
    try:
        previous_path = intake/'annular-joint-boundary-geometry-final-integrity.json'
        previous = json.loads(previous_path.read_text())
        check('previous_joint_closure_sealed',previous['state']=='complete' and all(row['passed'] for row in previous['checks']))
        for table in ['inputs','outputs']:
            for filename,expected in previous[table].items():
                if filename not in report['inputs']:
                    if hashlib.sha256((root/filename).read_bytes()).hexdigest()!=expected:
                        raise RuntimeError('Changed inherited source: '+filename)
                    report['inputs'][filename] = expected
        own(previous_path)
        for path in [Path(__file__),root/'scripts/annular_closure_continuation_20260914.py']:
            compile(path.read_bytes(),str(path),'exec')
            own(path)
            snapshot = destination/('executed-'+path.name)
            snapshot.write_bytes(path.read_bytes())
            own(snapshot,'outputs')
        for branch in ['GR','metric_Gram']:
            for degree in [12,16,20]:
                label = branch+'_degree'+str(degree)
                report.update({'active_case':label,'phase':'unperturbed_longer_baseline'})
                save()
                record = {'branch':branch,'degree':degree,'label':label,'protocols':[],'state':'running'}
                report['cases'].append(record)
                try:
                    base,matched = load_prepared_system(root,branch,degree=degree)
                    system = ProtocolEvolution(base)
                    record.update({'state_dimension':len(system.initial_state),'radial_degree':system.radial_rule.degree,
                                   'current_degree':system.current_grid.degree,'spacing':system.spacing,'width':system.width,
                                   'shape':system.shape,'lower_mass_seed':system.lower_mass_seed,
                                   'source_profile_coefficients':[part.tolist() for part in system.source_profile],
                                   'exterior_amplitudes':matched['exterior_amplitudes'],
                                   'factor_hash':hashlib.sha256(system.factors.tobytes()+system.sampling.tobytes()).hexdigest()})
                    baseline = system.integrate_protocol(0.,duration,divisor=32)
                    baseline_diagnostics,baseline_arrays = trajectory_diagnostics(system,baseline,0.,duration)
                    diagnostics_gate(label+'_baseline_regularity_and_budget',baseline_diagnostics)
                    store_arrays(destination/(label+'_protocol_0.0_reference.npz'),baseline_arrays)
                    record['baseline_diagnostics'] = baseline_diagnostics
                    predictions = {}
                    if degree>=16:
                        report['phase'] = 'predict_longer_joint_response'
                        save()
                        times = duration*(ChebyshevRule(32).points+1)/2
                        samples = {'times':times,'reference_states':baseline.sol(times)}

                        def progress(completed,total):
                            report['nodes_completed'],report['nodes_total'] = completed,total
                            save()
                            if completed==1 or completed%4==0 or completed==total:
                                print(label+' Schur block '+str(completed)+'/'+str(total),flush=True)

                        fine = JointSchurResponse(system,samples,duration=duration,progress=progress)
                        tangent,linear_log = fine.linear_response()
                        coarse = JointSchurResponse(system,samples,duration=duration,stride=2,full_exterior_columns=fine.columns)
                        coarse_tangent,coarse_log = coarse.linear_response()
                        output_tangent = fine.output_tangent(tangent)
                        tangent_refinement = float(abs(tangent[::2]-coarse_tangent).max())
                        gate(label+'_longer_linear_time_refinement',tangent_refinement<1e-8 and linear_log['full_collocation_residual']<1e-9,
                             {'refinement':tangent_refinement,'solver':linear_log})
                        one_way,one_way_log = fine.linear_response(coupled=False)
                        one_way_outputs = fine.output_tangent(one_way)
                        record['linear_response'] = {'fine_solver':linear_log,'coarse_solver':coarse_log,
                                                     'time_refinement':tangent_refinement,
                                                     'one_way_state_difference':float(abs(one_way-tangent).max()),
                                                     'one_way_output_difference':float(abs(one_way_outputs-output_tangent).max()),
                                                     'one_way_current_difference':float(abs(one_way_outputs[:,0]-output_tangent[:,0]).max())}
                        store_arrays(destination/(label+'_linear_prediction.npz'),
                                     {'times':times,'baseline_states':fine.states,'source_forcing':fine.forcing,'exterior_columns':fine.columns,
                                      'integration':fine.integration,'exterior_indices':fine.exterior,'retained_mask':fine.retained,
                                      'tangent':tangent,'output_tangent':output_tangent,'coarse_tangent':coarse_tangent,
                                      'one_way_tangent':one_way,'one_way_outputs':one_way_outputs})
                        for parameter in [-1.,1.]:
                            report['phase'] = 'nonlinear_joint_prediction_'+str(parameter)
                            save()
                            states,history = fine.nonlinear_response(parameter,tangent,max_iterations=8)
                            coarse_states,coarse_history = coarse.nonlinear_response(parameter,coarse_tangent,max_iterations=8)
                            time_error = float(abs(PolynomialHistory(coarse.times,coarse_states).sol(times).T-states).max())
                            predicted_history = PolynomialHistory(times,states)
                            diagnostics,arrays = trajectory_diagnostics(system,predicted_history,parameter,duration)
                            diagnostics_gate(label+'_'+str(parameter)+'_joint_regularity_and_budget',diagnostics)
                            gate(label+'_'+str(parameter)+'_nonlinear_time_refinement',time_error<1e-8,
                                 {'error':time_error,'fine_history':history,'coarse_history':coarse_history})
                            arrays.update({'collocation_times':times,'collocation_states':states,'coarse_states':coarse_states})
                            key = str(parameter).replace('-','minus')
                            store_arrays(destination/(label+'_protocol_'+key+'_prediction.npz'),arrays)
                            predictions[parameter] = arrays
                            record['protocols'].append({'parameter':parameter,'joint_diagnostics':diagnostics,
                                                        'nonlinear_time_refinement':time_error,'fine_iterations':history,'coarse_iterations':coarse_history})
                        report['phase'] = 'fresh_perturbed_references_after_prediction'
                        save()
                    for parameter in [-1.,1.]:
                        reference = system.integrate_protocol(parameter,duration,divisor=32)
                        diagnostics,arrays = trajectory_diagnostics(system,reference,parameter,duration)
                        diagnostics_gate(label+'_'+str(parameter)+'_reference_regularity_and_budget',diagnostics)
                        key = str(parameter).replace('-','minus')
                        store_arrays(destination/(label+'_protocol_'+key+'_reference.npz'),arrays)
                        if degree>=16:
                            predicted = predictions[parameter]
                            errors = {'state':float(abs(predicted['states']-arrays['states']).max()),
                                      'outputs':float(abs(predicted['outputs']-arrays['outputs']).max()),
                                      'profiles':float(abs(predicted['profiles']-arrays['profiles']).max())}
                            gate(label+'_'+str(parameter)+'_closed_prediction_matches_fresh_reference',max(errors.values())<1e-8,errors)
                            item = next(row for row in record['protocols'] if row['parameter']==parameter)
                            item.update({'reference_diagnostics':diagnostics,'prediction_errors':errors})
                        else:
                            record['protocols'].append({'parameter':parameter,'reference_diagnostics':diagnostics})
                    if degree>=16:
                        full_times = fine.times
                        from scipy.integrate import solve_ivp

                        def variational_equation(time,direction):
                            return system.evaluate_protocol(time,baseline.sol(time)+1j*1e-20*direction,1j*1e-20)['rhs'].imag/1e-20

                        direct = solve_ivp(variational_equation,(0.,duration),np.zeros(len(system.initial_state)),method='DOP853',
                                           rtol=2e-12,atol=2e-14,max_step=duration/32,dense_output=True)
                        check(label+'_fresh_variational_integrator_succeeded',direct.success,direct.message)
                        direct_states = direct.sol(full_times).T
                        direct_outputs = np.stack([fine.response.outputs(system.evaluate_protocol(time,baseline.sol(time)+1j*1e-20*direction,1j*1e-20)).imag/1e-20
                                                   for time,direction in zip(full_times,direct_states)])
                        state_error = float(abs(direct_states-tangent).max())
                        output_error = float(abs(direct_outputs-output_tangent).max())
                        current_error = float(abs(direct_outputs[:,0]-output_tangent[:,0]).max())
                        gate(label+'_longer_joint_linear_prediction_matches_fresh_tangent',max(state_error,output_error)<1e-8,
                             {'state':state_error,'outputs':output_error,'current':current_error})
                        record['linear_response'].update({'fresh_state_error':state_error,'fresh_output_error':output_error,'fresh_current_error':current_error,
                            'one_way_output_effect_resolved':record['linear_response']['one_way_output_difference']>max(100*output_error,1e-13),
                            'one_way_current_effect_resolved':record['linear_response']['one_way_current_difference']>max(100*current_error,1e-13)})
                        store_arrays(destination/(label+'_linear_reference.npz'),{'times':full_times,'states':direct_states,'outputs':direct_outputs})
                    record['state'] = 'complete'
                    print(json.dumps({'label':label,'state':'complete','minimum_energy':min(row['reference_diagnostics']['minimum_source_energy_sampled'] for row in record['protocols']),
                                      'linear':record.get('linear_response')}),flush=True)
                except Exception as error:
                    record.update({'state':'failed','error':repr(error),'traceback':traceback.format_exc()})
                    report['failures'].append({'case':label,'error':repr(error)})
                    print(json.dumps({'label':label,'state':'failed','error':repr(error)}),flush=True)
                save()
            branch_cases = [row for row in report['cases'] if row['branch']==branch]
            gate(branch+'_all_three_resolutions_completed',all(row['state']=='complete' for row in branch_cases))
            if not all(row['state']=='complete' for row in branch_cases):
                continue
            check(branch+'_same_physical_regulator_and_preparation',
                  all(row['spacing']==branch_cases[0]['spacing'] and row['width']==branch_cases[0]['width']
                      and row['shape']==branch_cases[0]['shape'] and row['factor_hash']==branch_cases[0]['factor_hash']
                      and row['exterior_amplitudes']==branch_cases[0]['exterior_amplitudes']
                      and row['lower_mass_seed']==branch_cases[0]['lower_mass_seed'] for row in branch_cases))
            for parameter in [-1.,0.,1.]:
                key = str(parameter).replace('-','minus')
                comparisons = []
                archives = {}
                for degree in [12,16,20]:
                    with np.load(destination/(branch+'_degree'+str(degree)+'_protocol_'+key+'_reference.npz'),allow_pickle=False) as archive:
                        archives[degree] = {name:archive[name].copy() for name in archive.files}
                for low,high in [(12,16),(16,20)]:
                    first,second = archives[low],archives[high]
                    errors = {'low':low,'high':high,'initial_profile_error':float(abs(first['profiles'][0]-second['profiles'][0]).max()),
                              'profile_error':float(abs(first['profiles']-second['profiles']).max()),
                              'output_error':float(abs(first['outputs']-second['outputs']).max()),
                              'affine_history_defect_error':float(abs(first['inner_affine_defect']-second['inner_affine_defect']).max())}
                    comparisons.append(errors)
                    gate(branch+'_'+str(parameter)+'_resolution_'+str(low)+'_'+str(high),
                         max(errors['profile_error'],errors['output_error'],errors['affine_history_defect_error'])<1e-8
                         and errors['initial_profile_error']<1e-10,errors)
                report['comparisons'].append({'branch':branch,'parameter':parameter,'spatial_refinement':comparisons})
                save()
        for module in tuple(sys.modules.values()):
            filename = getattr(module,'__file__',None)
            if filename:
                path = Path(filename).resolve()
                if path.parent==root/'scripts' and path.suffix=='.py':
                    own(path)
        check('no_python_cache',not(root/'scripts/__pycache__').exists())
        failed = [row['name'] for row in report['checks'] if not row['passed']]
        report.update({'state':'complete' if not failed and not report['failures'] else 'complete_with_failed_gates',
                       'failed_gates':failed,'conditional_continuation_complete':not failed and not report['failures']})
        save()
        print(json.dumps({'state':report['state'],'cases':len(report['cases']),'checks':len(report['checks']),'failed_gates':failed,'failures':report['failures']}),flush=True)
    except Exception as error:
        report.update({'state':'failed','error':repr(error),'traceback':traceback.format_exc()})
        save()
        raise


if __name__=='__main__':
    run()

