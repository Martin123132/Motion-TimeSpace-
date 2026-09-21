from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_wave_error_energy_20260919 import stiffness_weights, stiffness_terms, source_kinetic_force, wave_residual_channels, wave_energy
from annular_P2_weighted_projection_bounds_20260919 import band_action
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-live-wave-error-energy-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, full_geometry_reconstructed=True, all_scalar_modes_retained=True,
            original_source_condition_retained=True, all_Gram_rows_retained=True, no_fitted_couplings=True,
            rates_are_finite_difference_estimates=True, total_scalar_energy_not_total_gravity_Hamiltonian=True,
            nonnested_interpolation_not_exact_function_inclusion=True, full_nonlinear_stability_proven=False,
            displacement_tangent_formed_before_perturbing_to_reduce_subtraction_loss=True)
        for name in ['annular-wave-error-energy-algebra-attempt01', 'annular-live-compensated-rate-attempt01']:
            path = evidence.output.parent/name/'status.json'
            status = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(name+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        evidence.report['energy_snapshots'] = []
        for branch in ['reference', 'MTS']:
            systems = [IndexedGradedP2System(257, branch == 'MTS', 2e-5), IndexedGradedP2System(513, branch == 'MTS', 1e-5)]
            center = int(np.argmin(abs(systems[1].labels)))
            indices, shape, unused = systems[0].model.features_quadratic(systems[1].model.radii)

            def transfer(values):
                return np.sum(shape*values[indices], axis=1)

            def evaluate(system, state):
                rates, geometry = system.solve(*state)
                layer = system.layer(system.labels[center], geometry)
                values = state[0, center]
                data = layer.evaluate(0., values, rates[center])
                return dict(layer=layer, data=data, values=values, rates=rates[center],
                    all_rates=rates, weights=stiffness_weights(layer, values[-1]))

            for final in [False, True]:
                states = state_pair(evidence, branch, final)
                base = [evaluate(system, state) for system, state in zip(systems, states)]
                displacement = base[1]['values'][:-1]-transfer(base[0]['values'][:-1])
                velocity = base[1]['rates'][:-1]-transfer(base[0]['rates'][:-1])
                energies = wave_energy(base[1]['layer'], base[1]['data']['mass_bands'], base[1]['weights'], displacement, velocity)
                tag = branch+('_final' if final else '_initial')
                for level, item in enumerate(base):
                    weights = item['weights']
                    stiffness = stiffness_terms(item['layer'], weights, item['values'][:-1])
                    kinetic_force = source_kinetic_force(item['layer'], item['values'], item['rates'], item['data'])
                    force_error = float(max(abs(item['data']['scalar_covector']+stiffness['load']-kinetic_force)))
                    force_scale = float(max(np.max(abs(stiffness['load'])), np.max(abs(kinetic_force)), 1e-12))
                    potential_error = abs(item['data']['potential']-stiffness['gradient_energy']-stiffness['gram_energy'])
                    evidence.check(tag+'_'+str(level)+'_action_force_and_potential_match', force_error < 5e-13*force_scale+1e-15
                        and potential_error < 5e-13*max(abs(item['data']['potential']), 1e-15),
                        dict(force_error=force_error, potential_error=potential_error))
                    evidence.check(tag+'_'+str(level)+'_positive_stiffness_weights', np.all(weights['gradient'] > 0.)
                        and np.all(weights['gram'] > 0.))
                layer = base[1]['layer']
                radius, jacobian, unused = layer.mapping(layer.reference_radius, base[1]['values'][-1])
                temporal_density = jacobian*radius**4/layer.coefficient(0., radius)
                spatial_density = base[1]['weights']['gradient']/layer.reference_weight
                length = max(layer.anchor-layer.edges[0], layer.edges[-1]-layer.anchor)
                mass_by_stiffness_bound = .5*length**2*float(max(temporal_density)/min(spatial_density))
                for index, probe in enumerate([displacement, np.sin(layer.radii), np.cos(3*layer.radii)]):
                    stiffness = stiffness_terms(layer, base[1]['weights'], probe)
                    mass_form = float(probe @ band_action(base[1]['data']['mass_bands'], probe))
                    stiffness_form = 2*(stiffness['gradient_energy']+stiffness['gram_energy'])
                    evidence.check(tag+'_'+str(index)+'_anchored_discrete_coercivity_control',
                        mass_form <= mass_by_stiffness_bound*stiffness_form+1e-22)
                evidence.report['energy_snapshots'].append(dict(branch=branch, time=4e-5 if final else 0., **energies,
                    maximum_displacement=float(max(abs(displacement))), maximum_velocity_difference=float(max(abs(velocity))),
                    mass_by_stiffness_bound=mass_by_stiffness_bound, valid_for_claim=False))
                if not final:
                    continue
                base_stiffness = stiffness_terms(layer, base[1]['weights'], displacement)
                for step in [2e-7, 1e-7, 5e-8, 2.5e-8]:
                    path = evidence.output.parent/'annular-live-compensated-rate-attempt01'/(branch+'-'+str(step)+'-compensated-rate.npz')
                    evidence.own(path)
                    with np.load(path) as stored:
                        saved = {key:stored[key] for key in stored.files}
                    for level, item in enumerate(base):
                        prefix = str(level)+'_'
                        evidence.check(branch+'_'+str(step)+'_'+str(level)+'_same_saved_state_mass_and_canonical_direction',
                            np.array_equal(states[level], saved[prefix+'state'])
                            and np.max(abs(item['all_rates']-saved[prefix+'full_direction'][0])) < 1e-15
                            and np.max(abs(item['data']['scalar_covector']-saved[prefix+'full_direction'][1, center, :-1])) < 1e-15
                            and np.max(abs(item['data']['mass_bands']-saved[prefix+'mass_bands'])) < 1e-15)
                        item.update(mass_rate=saved[prefix+'mass_rate'], cross_rate=saved[prefix+'cross_rate'],
                            inverse_residual_rate=saved[prefix+'inverse_residual_rate'],
                            source_acceleration=float(saved[prefix+'direct_acceleration'][-1]))
                    before = evaluate(systems[1], states[1]-step*saved['1_full_direction'])
                    after = evaluate(systems[1], states[1]+step*saved['1_full_direction'])
                    evidence.check(branch+'_'+str(step)+'_same_reconstructed_tangent_velocities',
                        np.max(abs(before['rates']-saved['1_rates_before'])) < 1e-15
                        and np.max(abs(after['rates']-saved['1_rates_after'])) < 1e-15)
                    weight_rate = {name:(after['weights'][name]-before['weights'][name])/(2*step) for name in base[1]['weights']}
                    stiffness_rate = stiffness_terms(layer, weight_rate, displacement)
                    channels = wave_residual_channels(base[0], base[1], base[0]['weights'], base[1]['weights'], transfer)
                    acceleration = saved['acceleration_difference']
                    residual = band_action(base[1]['data']['mass_bands'], acceleration)+base_stiffness['load']
                    residual_split = sum(channels.values())
                    residual_error = float(max(abs(residual-residual_split)))
                    component_scale = sum(float(max(abs(value))) for value in channels.values())
                    evidence.check(branch+'_'+str(step)+'_seven_channel_wave_load_identity',
                        residual_error < 2e-10*max(component_scale, 1e-10)+5e-14,
                        dict(error=residual_error, component_scale=component_scale))
                    works = {name:float(velocity @ values) for name, values in channels.items()}
                    conservative_work = -float(velocity @ base_stiffness['load'])
                    mass_rate = .5*float(velocity @ band_action(base[1]['mass_rate'], velocity))
                    potential_rate_term = stiffness_rate['gradient_energy']+stiffness_rate['gram_energy']
                    kinetic_rate = float(velocity @ band_action(base[1]['data']['mass_bands'], acceleration))+mass_rate
                    exchange = -conservative_work
                    potential_rate = exchange+potential_rate_term
                    predicted = float(velocity @ residual)+mass_rate+potential_rate_term
                    velocity_before = saved['1_rates_before'][:-1]-transfer(saved['0_rates_before'][:-1])
                    velocity_after = saved['1_rates_after'][:-1]-transfer(saved['0_rates_after'][:-1])
                    first_energy = wave_energy(layer, before['data']['mass_bands'], before['weights'], displacement-step*velocity, velocity_before)
                    last_energy = wave_energy(layer, after['data']['mass_bands'], after['weights'], displacement+step*velocity, velocity_after)
                    direct = (last_energy['total']-first_energy['total'])/(2*step)
                    error = abs(direct-predicted)
                    tolerance = 2e-4*max(abs(direct), abs(predicted), abs(kinetic_rate), abs(potential_rate), 1e-30)+1e-23
                    bound = float(np.sum(abs(velocity*residual))+.5*np.sum(abs(velocity*band_action(base[1]['mass_rate'], velocity)))
                        +.5*np.sum(abs(weight_rate['gradient'])*base_stiffness['gradient']**2)
                        +.5*np.sum(abs(weight_rate['gram'])*base_stiffness['factor']**2))
                    evidence.check(branch+'_'+str(step)+'_wave_energy_rate_tangent_and_bound', error <= tolerance
                        and abs(predicted) <= bound+1e-24,
                        dict(error=error, numerical_control_tolerance=tolerance, bound=bound))
                    evidence.check(branch+'_'+str(step)+'_kinetic_potential_exchange_cancels',
                        abs(kinetic_rate+potential_rate-predicted) < 5e-14*max(abs(kinetic_rate), abs(potential_rate), 1e-18))
                    row = dict(branch=branch, tangent_step=step, **energies, **works,
                        conservative_kinetic_work=conservative_work, potential_exchange_rate=exchange,
                        kinetic_energy_rate=kinetic_rate, potential_energy_rate=potential_rate,
                        mass_geometry_rate=mass_rate, stiffness_geometry_rate=potential_rate_term,
                        full_wave_energy_rate=predicted, direct_directional_rate=direct, rate_comparison_error=error,
                        numerical_control_tolerance=tolerance, localized_rate_bound=bound, residual_load_reconstruction_error=residual_error,
                        residual_work=float(velocity @ residual), seven_channel_work_error=abs(sum(works.values())-float(velocity @ residual)),
                        valid_for_claim=False)
                    evidence.report['cases'].append(row)
                    output = evidence.output/(branch+'-'+str(step)+'-wave-energy.npz')
                    np.savez_compressed(output, displacement=displacement, velocity_difference=velocity,
                        acceleration_difference=acceleration, direct_wave_residual=residual, split_wave_residual=residual_split,
                        **channels, gradient_weight_rate=weight_rate['gradient'], Gram_weight_rate=weight_rate['gram'],
                        gradient_weights=base[1]['weights']['gradient'], Gram_weights=base[1]['weights']['gram'],
                        gradient_displacement=base_stiffness['gradient'], Gram_displacement=base_stiffness['factor'])
                    evidence.own(output, 'outputs')
                    evidence.save()
                    print(json.dumps(row), flush=True)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
