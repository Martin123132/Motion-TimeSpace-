from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_compensated_momentum_rate_20260919 import compensated_acceleration, inverse_residual, velocity_energy_rate
from annular_P2_weighted_projection_bounds_20260919 import band_action
from derive_annular_Gram_two_trace_force_law_20260919 import trace_force_data
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-live-compensated-rate-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, full_global_canonical_direction=True, all_Gram_rows_retained=True,
            both_inverse_residual_rates_retained=True, nonnested_jump_rate_retained=True,
            no_fitted_couplings=True, rates_are_finite_difference_estimates=True,
            centered_identity_not_independent_physics_validation=True, full_nonlinear_stability_proven=False,
            driver_rate_not_total_reduced_force_acceleration=True)
        for name in ['annular-compensated-rate-algebra-attempt01', 'annular-live-canonical-driver-attempt01']:
            path = evidence.output.parent/name/'status.json'
            status = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(name+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
        evidence.report['energy_rows'] = []
        for branch in ['reference', 'MTS']:
            systems = [IndexedGradedP2System(257, branch == 'MTS', 2e-5), IndexedGradedP2System(513, branch == 'MTS', 1e-5)]
            states = state_pair(evidence, branch, True)
            center = int(np.argmin(abs(systems[1].labels)))
            indices, shape, unused = systems[0].model.features_quadratic(systems[1].model.radii)

            def transfer(values):
                return np.sum(shape*values[indices], axis=1)

            def evaluate(system, state):
                rates, geometry = system.solve(*state)
                layer = system.layer(system.labels[center], geometry)
                data = layer.evaluate(0., state[0, center], rates[center])
                return dict(layer=layer, data=data, rates=rates[center], all_rates=rates, geometry=geometry,
                    coordinates=state[0, center], momenta=state[1, center, :-1],
                    inverse_residual=inverse_residual(data, rates[center], state[1, center, :-1]))

            def functionals(pair):
                coarse, fine = pair
                layer = fine['layer']
                values = fine['coordinates']
                actual = trace_force_data(layer, systems[1].model, values, values[-1])
                off_coarse = trace_force_data(layer, systems[0].model, coarse['coordinates'], values[-1])
                response = actual[1]['response']
                mean_trace = (actual[2]+off_coarse[2])/2
                targets = dict(left=response[:, 0], right=response[:, 1], trace_weighted=response @ mean_trace)
                delta = fine['rates'][:-1]-transfer(coarse['rates'][:-1])
                jump = float(systems[0].model.jump @ coarse['rates'][:-1]-layer.jump @ transfer(coarse['rates'][:-1]))
                result = {}
                for partition in ['all_rows', 'source_straddling', 'remaining']:
                    mask = np.ones(len(actual[0]['factor']), dtype=bool) if partition == 'all_rows' else actual[0]['source_rows']
                    if partition == 'remaining':
                        mask = ~mask
                    for name, target in targets.items():
                        row = mask*actual[0]['weights']*(layer.lifted @ target)
                        covector = np.asarray(layer.lifted.T @ row).ravel()
                        beta = float(row @ layer.lifted_hinge)
                        result[partition+'_'+name] = dict(covector=covector, beta=beta,
                            driver=float(covector @ delta+beta*jump), partition=partition, functional=name)
                return result, delta, jump

            base = [evaluate(system, state) for system, state in zip(systems, states)]
            flows = [np.stack([item['all_rates'], system.forces(state[0], item['all_rates'], item['geometry'])])
                for item, system, state in zip(base, systems, states)]
            evidence.check(branch+'_full_canonical_directions_finite', all(flow.shape == state.shape and np.all(np.isfinite(flow))
                for flow, state in zip(flows, states)))
            base_functionals, delta, jump = functionals(base)
            for step in [2e-7, 1e-7, 5e-8, 2.5e-8]:
                before = [evaluate(system, state-step*flow) for system, state, flow in zip(systems, states, flows)]
                after = [evaluate(system, state+step*flow) for system, state, flow in zip(systems, states, flows)]
                results, direct_accelerations, mass_rates, diagnostics = [], [], [], []
                arrays = {}
                for level, (item, first, last, flow, state) in enumerate(zip(base, before, after, flows, states)):
                    mass_rate = (last['data']['mass_bands']-first['data']['mass_bands'])/(2*step)
                    cross_rate = (last['data']['cross']-first['data']['cross'])/(2*step)
                    acceleration = (last['rates']-first['rates'])/(2*step)
                    residual_rate = (last['inverse_residual']-first['inverse_residual'])/(2*step)
                    result = compensated_acceleration(item['data'], item['rates'], flow[1, center, :-1],
                        mass_rate, cross_rate, acceleration[-1], residual_rate)
                    mean_data = dict(mass_bands=(last['data']['mass_bands']+first['data']['mass_bands'])/2,
                        cross=(last['data']['cross']+first['data']['cross'])/2)
                    exact_centered = compensated_acceleration(mean_data, (last['rates']+first['rates'])/2,
                        (last['momenta']-first['momenta'])/(2*step), mass_rate, cross_rate, acceleration[-1], residual_rate)
                    product_error = float(max(abs(result['acceleration']-acceleration[:-1])))
                    centered_error = float(max(abs(exact_centered['acceleration']-acceleration[:-1])))
                    scale = float(max(np.max(abs(acceleration[:-1])), np.max(abs(result['acceleration'])), 1e-8))
                    tolerance = 2e-4*scale+1e-8
                    tag = branch+'_'+str(step)+'_'+str(level)
                    evidence.check(tag+'_base_product_law_finite_tangent_control', product_error <= tolerance,
                        dict(error=product_error, tolerance=tolerance, not_a_derivative_certificate=True))
                    evidence.check(tag+'_centered_product_identity', centered_error <= 1e-7*scale+1e-8,
                        dict(error=centered_error, scale=scale))
                    diagnostics.append(dict(level=level, base_product_error=product_error, centered_product_error=centered_error,
                        acceleration_scale=scale, inverse_residual_rate_max=float(max(abs(residual_rate))),
                        source_acceleration=float(acceleration[-1])))
                    results.append(result)
                    direct_accelerations.append(acceleration)
                    mass_rates.append(mass_rate)
                    for name, value in dict(state=state, full_direction=flow, mass_rate=mass_rate, cross_rate=cross_rate,
                            inverse_residual_rate=residual_rate, direct_acceleration=acceleration,
                            compensated_acceleration=result['acceleration'], mass_bands=item['data']['mass_bands'],
                            inverse_residual_before=first['inverse_residual'], inverse_residual_after=last['inverse_residual'],
                            rates_before=first['rates'], rates_after=last['rates']).items():
                        arrays[str(level)+'_'+name] = value
                first_functionals, first_delta, unused = functionals(before)
                last_functionals, last_delta, unused = functionals(after)
                delta_acceleration = results[1]['acceleration']-transfer(results[0]['acceleration'])
                jump_rate = float(systems[0].model.jump @ results[0]['acceleration']
                    -systems[1].model.jump @ transfer(results[0]['acceleration']))
                rows = []
                for key, item in base_functionals.items():
                    first, last = first_functionals[key], last_functionals[key]
                    covector_rate = (last['covector']-first['covector'])/(2*step)
                    beta_rate = (last['beta']-first['beta'])/(2*step)
                    covector = item['covector']
                    channels = {name:float(covector @ (results[1]['channels'][name]-transfer(results[0]['channels'][name])))
                        for name in results[1]['channels']}
                    acceleration_channel = float(covector @ delta_acceleration)
                    functional_channel = float(covector_rate @ delta)
                    jump_channel = float(item['beta']*jump_rate+beta_rate*jump)
                    predicted = acceleration_channel+functional_channel+jump_channel
                    direct = (last['driver']-first['driver'])/(2*step)
                    absolute_bound = float(np.sum(abs(covector*delta_acceleration))+np.sum(abs(covector_rate*delta))
                        +abs(item['beta']*jump_rate)+abs(beta_rate*jump))
                    error = abs(predicted-direct)
                    tolerance = 2e-4*max(abs(direct), abs(predicted), 1e-8)+1e-5
                    evidence.check(branch+'_'+str(step)+'_'+key+'_driver_rate_control_and_bound', error <= tolerance
                        and abs(predicted) <= absolute_bound+1e-9,
                        dict(error=error, tolerance=tolerance, bound=absolute_bound))
                    rows.append(dict(branch=branch, tangent_step=step, partition=item['partition'], functional=item['functional'],
                        direct_directional_driver_rate=direct, compensated_driver_rate=predicted,
                        comparison_error=error, numerical_control_tolerance=tolerance, **channels,
                        combined_acceleration_channel=acceleration_channel, changing_functional_channel=functional_channel,
                        transfer_jump_rate_channel=jump_channel, localized_absolute_bound=absolute_bound,
                        split_reconstruction_error=abs(sum(channels.values())-acceleration_channel), valid_for_claim=False))
                energy = velocity_energy_rate(base[1]['data']['mass_bands'], mass_rates[1], delta, delta_acceleration)
                first_energy = .5*float(first_delta @ band_action(before[1]['data']['mass_bands'], first_delta))
                last_energy = .5*float(last_delta @ band_action(after[1]['data']['mass_bands'], last_delta))
                direct_energy_rate = (last_energy-first_energy)/(2*step)
                energy_error = abs(direct_energy_rate-energy['total_rate'])
                energy_tolerance = 2e-4*max(abs(direct_energy_rate), abs(energy['total_rate']), 1e-30)+1e-23
                evidence.check(branch+'_'+str(step)+'_velocity_energy_rate_control_and_bound', energy_error <= energy_tolerance
                    and abs(energy['total_rate']) <= energy['absolute_bound']+1e-25,
                    dict(error=energy_error, tolerance=energy_tolerance))
                evidence.report['energy_rows'].append(dict(branch=branch, tangent_step=step, **energy,
                    direct_energy_rate=direct_energy_rate, comparison_error=energy_error,
                    numerical_control_tolerance=energy_tolerance, valid_for_claim=False))
                evidence.report['cases'].append(dict(branch=branch, tangent_step=step, rows=rows, diagnostics=diagnostics))
                arrays.update(velocity_difference=delta, acceleration_difference=delta_acceleration)
                path = evidence.output/(branch+'-'+str(step)+'-compensated-rate.npz')
                np.savez_compressed(path, **arrays)
                evidence.own(path, 'outputs')
                evidence.save()
                print(json.dumps(dict(branch=branch, step=step, energy=energy,
                    total=[row for row in rows if row['partition'] == 'all_rows' and row['functional'] == 'trace_weighted'])), flush=True)
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
