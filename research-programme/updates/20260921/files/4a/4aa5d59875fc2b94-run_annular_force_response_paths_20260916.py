from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_full_force_linearization_20260916 import FullForceLinearization
from annular_anchored_projector_chart_20260916 import AnchoredProjectorChart, material_terms
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from scipy.integrate import solve_ivp
import numpy as np
import json
import time


def main():
    evidence = EvidenceRun('annular-force-response-paths-attempt01',__file__)
    try:
        intake = evidence.root/'source-intake/navier-stokes/20260914'
        previous_folder = intake/'annular-anchored-moving-tight-attempt01'
        for path in [previous_folder/'status.json',intake/'annular-full-force-linearization-attempt01/status.json']:
            evidence.own(path)
            status = json.loads(path.read_text())
            evidence.check(path.parent.name+'_complete',status['state']=='complete' and all(row['passed'] for row in status['checks']))
        previous = json.loads((previous_folder/'status.json').read_text())
        evidence.report.update(configuration=dict(final_time=.005,node_count=321,rtol=2e-12,atol=2e-14,
            maximum_step_rule='same half-frequency cap as saved tight run',force_replay_tolerance=2e-10),
            original_action_unchanged=True,raw_initial_state_unchanged=True,full_prepared_counterfactual_not_physical_reinitialization=True,
            original_GR_gates_unchanged=True,continuum_limit=False)
        evidence.save()
        times = np.linspace(0.,.005,321)
        for gram in [False,True]:
            started = time.monotonic()
            branch = 'MTS' if gram else 'reference'
            path = previous_folder/(branch+'-accepted-8.npz')
            evidence.own(path)
            with np.load(path) as saved:
                old_times,old_full,old_reduced,retained = [saved[key].copy() for key in ['times','full_states','reduced_states','retained_indices']]
            diagnostic_path = previous_folder/(branch+'-diagnostics-8.json')
            evidence.own(diagnostic_path)
            old_diagnostics = json.loads(diagnostic_path.read_text())
            system = LocallyRefinedSourceAction(129,gram,background_mass=0.,source_splits=8)
            model = FullForceLinearization(system)
            chart = AnchoredProjectorChart(system,retained.tolist())
            evidence.check(branch+'_same_sealed_window_completed_mask',chart.retained==retained.tolist())
            step = next(row for row in previous['cases'] if row['branch']==branch)['maximum_step']
            reduced_initial = old_reduced[0,:-2]
            initial_coordinates,initial_rates = np.split(reduced_initial[:-1],2)
            physical,physical_rates = chart.lift(initial_coordinates,initial_rates)
            prepared_initial = np.concatenate([physical,physical_rates,[reduced_initial[-1]]])
            full_paths = {}
            for label,initial_state in [('raw',old_full[0]),('prepared',prepared_initial)]:
                result = solve_ivp(model.rhs,(0.,.005),initial_state,method='DOP853',t_eval=times,
                    rtol=2e-12,atol=2e-14,max_step=step,first_step=step/2)
                evidence.check(branch+'_'+label+'_full_replay_success',result.success)
                full_paths[label] = result.y.T
            reduced_core = [reduced_initial]
            for interval in range(8):
                interval_times = times[40*interval:40*interval+41]
                result = solve_ivp(chart.rhs,(interval_times[0],interval_times[-1]),reduced_core[-1],method='DOP853',
                    t_eval=interval_times,rtol=2e-12,atol=2e-14,max_step=step,first_step=step/2)
                if not result.success:
                    raise RuntimeError(result.message)
                reduced_core.extend(result.y.T[1:])
                path = evidence.output/(branch+'-reduced-replay-accepted-'+str(interval+1)+'.npz')
                np.savez_compressed(path,times=times[:len(reduced_core)],reduced_core=np.array(reduced_core))
                evidence.own(path,'outputs')
                evidence.report['progress'] = dict(branch=branch,accepted_time=float(interval_times[-1]),phase='reduced replay',seconds=time.monotonic()-started)
                evidence.save()
                print(evidence.report['progress'],flush=True)
                if time.monotonic()-started>3600:
                    raise RuntimeError('One-hour branch safe checkpoint; accepted replays preserved.')
            reduced_core = np.array(reduced_core)
            reduced_physical,reduced_derivatives,raw_derivatives,prepared_derivatives = [],[],[],[]
            raw_forces,prepared_forces,reduced_forces,same_state_forces,physical_defects = [],[],[],[],[]
            for index,instant in enumerate(times):
                coordinates,rates = np.split(reduced_core[index,:-1],2)
                dynamics = chart.dynamics(coordinates,rates)
                physical,physical_rates,physical_acceleration = chart.lift(coordinates,rates,dynamics['acceleration'])
                material = material_terms(system,coordinates[-1],rates[-1])
                physical_state = np.concatenate([physical,physical_rates,[reduced_core[index,-1]]])
                physical_flow = np.concatenate([physical_rates,physical_acceleration,[material['clock']]])
                data = model.evaluate(physical_state)
                raw_data = model.evaluate(full_paths['raw'][index])
                prepared_data = model.evaluate(full_paths['prepared'][index])
                reduced_force = material['inertia']*dynamics['acceleration'][-1]+material['momentum_b']*rates[-1]
                raw_forces.append(float(raw_data['force']))
                prepared_forces.append(float(prepared_data['force']))
                reduced_forces.append(float(reduced_force))
                same_state_forces.append(float(data['force']-reduced_force))
                physical_defects.append(data['flow']-physical_flow)
                reduced_physical.append(physical_state)
                reduced_derivatives.append(physical_flow)
                raw_derivatives.append(raw_data['flow'])
                prepared_derivatives.append(prepared_data['flow'])
            raw_forces,prepared_forces,reduced_forces,same_state_forces = map(np.array,[raw_forces,prepared_forces,reduced_forces,same_state_forces])
            initial_effect = raw_forces-prepared_forces
            moving_effect = prepared_forces-reduced_forces
            total_effect = raw_forces-reduced_forces
            old_raw_force = np.array([row['full_force'] for row in old_diagnostics])
            old_reduced_force = np.array([row['reduced_force'] for row in old_diagnostics])
            replay_error = max(float(np.max(abs(raw_forces[::8]-old_raw_force))),float(np.max(abs(reduced_forces[::8]-old_reduced_force))))
            evidence.check(branch+'_same_saved_observation_times',np.array_equal(times[::8],old_times))
            evidence.check(branch+'_independent_force_replay',replay_error<2e-10,replay_error)
            evidence.check(branch+'_counterfactual_algebra',float(np.max(abs(initial_effect+moving_effect-total_effect)))<2e-18)
            evidence.check(branch+'_omission_starts_with_zero_state_error',np.max(abs(prepared_initial-reduced_physical[0]))==0.)
            evidence.check(branch+'_actual_omission_is_acceleration_only',np.max(abs(np.array(physical_defects)[:,:system.count+1]))==0.
                and np.max(abs(np.array(physical_defects)[:,-1]))==0.)
            path = evidence.output/(branch+'-physical-paths.npz')
            np.savez_compressed(path,times=times,raw_states=full_paths['raw'],raw_derivatives=np.array(raw_derivatives),
                prepared_states=full_paths['prepared'],prepared_derivatives=np.array(prepared_derivatives),
                reduced_states=np.array(reduced_physical),reduced_derivatives=np.array(reduced_derivatives),
                physical_defects=np.array(physical_defects),raw_forces=raw_forces,prepared_forces=prepared_forces,
                reduced_forces=reduced_forces,same_state_forces=same_state_forces,initial_force_effect=initial_effect,
                moving_force_effect=moving_effect,total_force_effect=total_effect)
            evidence.own(path,'outputs')
            evidence.report['cases'].append(dict(branch=branch,full_dimension=system.count,retained_dimension=chart.count,
                node_count=len(times),maximum_force_replay_error=replay_error,
                endpoint_initial_preparation_effect=float(initial_effect[-1]),endpoint_accumulated_motion_effect=float(moving_effect[-1]),
                endpoint_same_state_omission=float(same_state_forces[-1]),endpoint_total_difference=float(total_effect[-1]),
                maximum_initial_preparation_effect=float(np.max(abs(initial_effect))),
                maximum_accumulated_motion_effect=float(np.max(abs(moving_effect))),
                maximum_total_difference=float(np.max(abs(total_effect))),
                finer_sample_budget_met=bool(np.max(abs(total_effect))<=2e-7),
                counterfactual_split_is_exact_algebra_but_order_dependent=True,
                nonlinear_evolution_not_linearized=True,seconds=time.monotonic()-started))
            evidence.save()
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__=='__main__':
    main()
