from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_action_test_energy_20260919 import dense_mass, dense_stiffness, differentiated_energy, energy_growth_bound
from annular_compensated_momentum_rate_20260919 import compensated_acceleration, inverse_residual
from annular_wave_error_energy_20260919 import stiffness_weights, stiffness_terms, wave_residual_channels, wave_energy
from annular_P2_weighted_projection_bounds_20260919 import band_action
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from run_annular_P2_continuum_bridge_20260918 import checked_load
from time import perf_counter
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-differentiated-action-energy-attempt01',__file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,uniform_evolving_refinement_rate_proven=False,
            full_nonlinear_stability_proven=False,all_Gram_rows_retained=True,original_source_condition_retained=True,
            inverse_residual_rates_retained=True,nested_actual_canonical_directions=True,
            frozen_direction_second_derivative_not_used=True,rates_are_finite_difference_estimates=True,
            energy_does_not_control_Gram_acceleration=True,energy_is_scalar_hierarchy_not_full_Hamiltonian=True)
        evidence.report['acceleration_controls'],evidence.report['residual_channels'] = [],[]
        stability_path = evidence.output.parent/'annular-action-adjoint-stability-attempt01/status.json'
        stability = json.loads(stability_path.read_text())
        evidence.own(stability_path)
        evidence.check('actual_stiffness_stability_complete',stability['state'] == 'complete' and all(row['passed'] for row in stability['checks']))
        example = 1.3
        full_second = 8*example**6
        frozen_second = 2*example**6
        missing_flow_derivative = 6*example**6
        evidence.check('nonzero_canonical_direction_change_control',abs(full_second-frozen_second-missing_flow_derivative) < 1e-12
            and abs(full_second-frozen_second) > 1.)
        for branch in ['reference','MTS']:
            systems = [IndexedGradedP2System(257,branch == 'MTS',2e-5),IndexedGradedP2System(513,branch == 'MTS',1e-5)]
            states = state_pair(evidence,branch,True)
            center = int(np.argmin(abs(systems[0].labels)))
            indices,shape,unused = systems[0].model.features_quadratic(systems[1].model.radii)

            def transfer(values):
                return np.sum(shape*values[indices],axis=1)

            def evaluate(system,state,with_flow):
                if perf_counter()-started > 10800:
                    raise RuntimeError('Three-hour calculation budget reached; completed evidence preserved.')
                rates,geometry = system.solve(*state)
                layer = system.layer(system.labels[center],geometry)
                values = state[0,center]
                data = layer.evaluate(0.,values,rates[center])
                item = dict(layer=layer,data=data,values=values,rates=rates[center],
                    weights=stiffness_weights(layer,values[-1]),
                    inverse_residual=inverse_residual(data,rates[center],state[1,center,:-1]))
                if with_flow:
                    item['flow'] = np.stack([rates,system.forces(state[0],rates,geometry)])
                return item

            def accelerate(system,state,item,inner_step,tag):
                first = evaluate(system,state-inner_step*item['flow'],False)
                last = evaluate(system,state+inner_step*item['flow'],False)
                mass_rate = (last['data']['mass_bands']-first['data']['mass_bands'])/(2*inner_step)
                cross_rate = (last['data']['cross']-first['data']['cross'])/(2*inner_step)
                residual_rate = (last['inverse_residual']-first['inverse_residual'])/(2*inner_step)
                direct = (last['rates']-first['rates'])/(2*inner_step)
                result = compensated_acceleration(item['data'],item['rates'],item['flow'][1,center,:-1],
                    mass_rate,cross_rate,direct[-1],residual_rate)
                error = float(np.max(abs(result['acceleration']-direct[:-1])))
                tolerance = 2e-4*max(float(np.max(abs(direct[:-1]))),1e-8)+1e-8
                evidence.check(tag+'_compensated_acceleration',error <= tolerance,dict(error=error,tolerance=tolerance))
                item.update(mass_rate=mass_rate,cross_rate=cross_rate,inverse_residual_rate=residual_rate,
                    source_acceleration=float(direct[-1]),acceleration=result['acceleration'])
                evidence.report['acceleration_controls'].append(dict(branch=branch,location=tag,inner_step=inner_step,
                    acceleration_error=error,numerical_tolerance=tolerance,
                    inverse_residual_rate_max=float(np.max(abs(residual_rate))),source_acceleration=float(direct[-1]),valid_for_claim=False))

            def pair_quantities(pair):
                displacement = pair[1]['values'][:-1]-transfer(pair[0]['values'][:-1])
                velocity = pair[1]['rates'][:-1]-transfer(pair[0]['rates'][:-1])
                acceleration = pair[1]['acceleration']-transfer(pair[0]['acceleration'])
                stiffness = stiffness_terms(pair[1]['layer'],pair[1]['weights'],displacement)
                direct_residual = band_action(pair[1]['data']['mass_bands'],acceleration)+stiffness['load']
                channels = wave_residual_channels(pair[0],pair[1],pair[0]['weights'],pair[1]['weights'],transfer)
                energy = wave_energy(pair[1]['layer'],pair[1]['data']['mass_bands'],pair[1]['weights'],velocity,acceleration)
                return dict(displacement=displacement,velocity=velocity,acceleration=acceleration,
                    residual=sum(channels.values()),direct_residual=direct_residual,channels=channels,energy=energy['total'])

            base = [evaluate(system,state,True) for system,state in zip(systems,states)]
            matrices = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            fine_mass,fine_stiffness = matrices['fine_mass'],matrices['fine_stiffness']
            upper = next(row for row in stability['cases'] if row['branch'] == branch and row['time'] == 4e-5)
            evidence.check(branch+'_same_action_matrices',np.max(abs(fine_mass-dense_mass(base[1]['data']['mass_bands']))) < 1e-13
                and np.max(abs(fine_stiffness-dense_stiffness(base[1]['layer'],base[1]['weights']))) < 1e-10)
            for step in [1e-7,5e-8]:
                inner_step = step/2
                tag = branch+'-'+str(step)
                evidence.report['progress'] = tag+' base and nested canonical probes'
                evidence.save()
                for level in range(2):
                    accelerate(systems[level],states[level],base[level],inner_step,tag+'-base-'+str(level))
                first_states = [state-step*item['flow'] for state,item in zip(states,base)]
                last_states = [state+step*item['flow'] for state,item in zip(states,base)]
                first = [evaluate(system,state,True) for system,state in zip(systems,first_states)]
                last = [evaluate(system,state,True) for system,state in zip(systems,last_states)]
                for label,pair,perturbed_states in [('before',first,first_states),('after',last,last_states)]:
                    for level in range(2):
                        accelerate(systems[level],perturbed_states[level],pair[level],inner_step,tag+'-'+label+'-'+str(level))
                current,lower,upper_state = [pair_quantities(pair) for pair in [base,first,last]]
                for label,result in [('base',current),('before',lower),('after',upper_state)]:
                    error = float(np.max(abs(result['direct_residual']-result['residual'])))
                    scale = sum(float(np.max(abs(value))) for value in result['channels'].values())
                    tolerance = 2e-10*max(scale,1e-10)+5e-14
                    evidence.check(tag+'_'+label+'_seven_action_channels_reconstruct_residual',error <= tolerance,dict(error=error,tolerance=tolerance))
                mass_rate = dense_mass((last[1]['data']['mass_bands']-first[1]['data']['mass_bands'])/(2*step))
                weight_rate = {name:(last[1]['weights'][name]-first[1]['weights'][name])/(2*step) for name in base[1]['weights']}
                stiffness_rate = dense_stiffness(base[1]['layer'],weight_rate)
                residual_rate = (upper_state['residual']-lower['residual'])/(2*step)
                result = differentiated_energy(fine_mass,fine_stiffness,mass_rate,stiffness_rate,
                    current['displacement'],current['velocity'],current['acceleration'],residual_rate)
                bound = energy_growth_bound(fine_mass,fine_stiffness,mass_rate,stiffness_rate,
                    current['displacement'],current['velocity'],current['acceleration'],residual_rate)
                direct = (upper_state['energy']-lower['energy'])/(2*step)
                rate_error = abs(direct-result['rate'])
                rate_tolerance = 2e-4*max(abs(direct),abs(result['rate']),sum(abs(value) for value in result['channels'].values()),1e-20)+1e-12
                evidence.check(tag+'_differentiated_energy_full_canonical_probe',rate_error <= rate_tolerance,dict(error=rate_error,tolerance=rate_tolerance))
                evidence.check(tag+'_conditional_Gronwall_rate_bound',abs(result['rate']) <= bound['energy_rate_upper_bound']+1e-16)
                fine_velocity_form = float(current['velocity'] @ fine_stiffness @ current['velocity'])
                work_bound = float(upper['work_prefactor']*np.sqrt(2*result['energy']))
                evidence.check(tag+'_E1_controls_test_energy_and_weak_work',fine_velocity_form <= 2*result['energy']+1e-20
                    and abs(upper['weak_work']) <= work_bound+1e-22)
                mean_mass = (dense_mass(last[1]['data']['mass_bands'])+dense_mass(first[1]['data']['mass_bands']))/2
                mean_weights = {name:(last[1]['weights'][name]+first[1]['weights'][name])/2 for name in base[1]['weights']}
                mean_stiffness = dense_stiffness(base[1]['layer'],mean_weights)
                average = {name:(upper_state[name]+lower[name])/2 for name in ['displacement','velocity','acceleration']}
                secant = {name:(upper_state[name]-lower[name])/(2*step) for name in average}
                exact_residual_rate = (upper_state['direct_residual']-lower['direct_residual'])/(2*step)
                exact = differentiated_energy(mean_mass,mean_stiffness,mass_rate,stiffness_rate,
                    average['displacement'],average['velocity'],average['acceleration'],exact_residual_rate)
                exchange = float(average['velocity'] @ mean_stiffness @ (secant['velocity']-average['acceleration'])
                    -average['acceleration'] @ mean_stiffness @ (secant['displacement']-average['velocity']))
                mixed = .5*step**2*float(secant['acceleration'] @ mass_rate @ secant['acceleration']
                    +secant['velocity'] @ stiffness_rate @ secant['velocity'])
                exact_error = abs(direct-exact['rate']-exchange-mixed)
                exact_tolerance = 2e-8*max(abs(direct),abs(exact['rate']),abs(exchange),1e-20)+1e-12
                evidence.check(tag+'_exact_centered_energy_with_kinematic_and_mixed_corrections',exact_error <= exact_tolerance,
                    dict(error=exact_error,tolerance=exact_tolerance))
                for name in current['channels']:
                    channel_rate = (upper_state['channels'][name]-lower['channels'][name])/(2*step)
                    evidence.report['residual_channels'].append(dict(branch=branch,outer_step=step,inner_step=inner_step,channel=name,
                        derivative_max=float(np.max(abs(channel_rate))),energy_work=float(current['acceleration'] @ channel_rate),valid_for_claim=False))
                row = dict(branch=branch,outer_step=step,inner_step=inner_step,energy=result['energy'],predicted_rate=result['rate'],
                    direct_rate=direct,rate_error=rate_error,numerical_tolerance=rate_tolerance,**result['channels'],**bound,
                    exact_secant_error=exact_error,exact_secant_tolerance=exact_tolerance,
                    finite_secant_kinematic_correction=exchange,finite_secant_mixed_correction=mixed,
                    weak_work=upper['weak_work'],E1_weak_work_bound=work_bound,valid_for_claim=False)
                evidence.report['cases'].append(row)
                arrays = dict(displacement=current['displacement'],velocity=current['velocity'],acceleration=current['acceleration'],
                    residual_rate=residual_rate,mass_rate=mass_rate,stiffness_rate=stiffness_rate,
                    first_residual=lower['residual'],last_residual=upper_state['residual'],
                    first_acceleration=lower['acceleration'],last_acceleration=upper_state['acceleration'])
                for level in range(2):
                    arrays[str(level)+'_before_flow'] = first[level]['flow']
                    arrays[str(level)+'_after_flow'] = last[level]['flow']
                path = evidence.output/(tag+'-differentiated-energy.npz')
                np.savez_compressed(path,**arrays)
                evidence.own(path,'outputs')
                evidence.save()
                print(json.dumps(row),flush=True)
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream,contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',checks=len(evidence.report['checks']))),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
