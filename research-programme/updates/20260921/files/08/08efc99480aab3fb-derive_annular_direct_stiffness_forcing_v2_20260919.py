from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_direct_stiffness_forcing_20260919 import transfer_rate,dual_norm,forcing_constant
from annular_action_test_energy_20260919 import dense_mass,dense_stiffness
from annular_wave_error_energy_20260919 import stiffness_weights,stiffness_terms
from annular_P2_weighted_projection_bounds_20260919 import band_action
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_moving_Gram_profile_20260919 import evaluate_pair
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from run_annular_P2_continuum_bridge_20260918 import checked_load
from scipy.linalg import cholesky,solve_banded
import contextlib
import json
import numpy as np


def sectors(layer,weights):
    gram = (layer.lifted.T @ layer.lifted.multiply(weights['gram'][:,None])).toarray()
    gradient = dense_stiffness(layer,dict(gradient=weights['gradient'],gram=np.zeros_like(weights['gram'])))
    return dict(gradient=gradient,gram=gram,total=gradient+gram)


def main():
    evidence = EvidenceRun('annular-direct-stiffness-forcing-attempt02',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,uniform_evolving_refinement_rate_proven=False,
            full_nonlinear_stability_proven=False,all_six_channels_retained=True,
            original_source_condition_retained=True,original_nonnested_interpolation_retained=True,
            new_jerk_not_computed=True,mass_and_stiffness_rates_are_finite_probe_estimates=True,
            operator_norm_bounds_not_interval_certified=True,coarse_background_energies_not_error_energies=True)
        evidence.report['channels'] = []
        evidence.report['factored_endpoint_loads_preserve_original_action_arithmetic'] = True
        failed_path = evidence.output.parent/'annular-direct-stiffness-forcing-attempt01/status.json'
        failed = json.loads(failed_path.read_text())
        evidence.own(failed_path)
        evidence.check('dense_secant_failed_attempt_preserved',failed['state'] == 'failed')
        old_path = evidence.output.parent/'annular-differentiated-action-energy-attempt01/status.json'
        previous = json.loads(old_path.read_text())
        evidence.own(old_path)
        evidence.check('nested_action_derivative_complete',previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        for branch in ['reference','MTS']:
            systems = [IndexedGradedP2System(257,branch == 'MTS',2e-5),IndexedGradedP2System(513,branch == 'MTS',1e-5)]
            states = state_pair(evidence,branch,True)
            base = evaluate_pair(systems,states)
            saved = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            interpolation = saved['interpolation']
            indices,shape,unused = systems[0].model.features_quadratic(systems[1].model.radii)

            def nodal_transfer(values):
                return np.sum(shape*values[indices],axis=1)
            coarse_stiffness = saved['coarse_stiffness']
            fine_mass = saved['fine_mass']
            mass_lower = cholesky(fine_mass,lower=True,check_finite=False)
            stiffness_lower = cholesky(coarse_stiffness,lower=True,check_finite=False)
            weights = [stiffness_weights(item['layer'],item['values'][-1]) for item in base]
            base_sectors = [sectors(item['layer'],weight) for item,weight in zip(base,weights)]
            values,velocity = base[0]['values'][:-1],base[0]['rates'][:-1]
            coarse_value_norm = float(np.sqrt(values @ coarse_stiffness @ values))
            coarse_velocity_norm = float(np.sqrt(velocity @ coarse_stiffness @ velocity))
            mismatch_constants = {}
            for step in [1e-7,5e-8]:
                tag = branch+'-'+str(step)
                canonical = checked_load(evidence,'annular-live-compensated-rate-attempt01',tag+'-compensated-rate.npz')
                old = checked_load(evidence,'annular-differentiated-action-energy-attempt01',tag+'-differentiated-energy.npz')
                flows = [canonical[str(level)+'_full_direction'] for level in range(2)]
                evidence.check(tag+'_same_saved_base_states_and_rates',all(np.array_equal(states[level],canonical[str(level)+'_state'])
                    and np.max(abs(base[level]['all_rates']-flows[level][0])) < 1e-15 for level in range(2)))
                before = evaluate_pair(systems,[state-step*flow for state,flow in zip(states,flows)])
                after = evaluate_pair(systems,[state+step*flow for state,flow in zip(states,flows)])
                first_weights = [stiffness_weights(item['layer'],item['values'][-1]) for item in before]
                last_weights = [stiffness_weights(item['layer'],item['values'][-1]) for item in after]
                weight_rates = [{name:(last[name]-first[name])/(2*step) for name in first} for first,last in zip(first_weights,last_weights)]
                matrix_rates = [sectors(item['layer'],rate) for item,rate in zip(base,weight_rates)]
                mass_rates = [dense_mass((last['mass']-first['mass'])/(2*step)) for first,last in zip(before,after)]
                evidence.check(tag+'_mass_rate_matches_previous_nested_evidence',np.max(abs(mass_rates[1]-old['mass_rate'])) < 1e-12)
                first_sectors = [sectors(item['layer'],weight) for item,weight in zip(before,first_weights)]
                last_sectors = [sectors(item['layer'],weight) for item,weight in zip(after,last_weights)]
                arrays = dict(coarse_values=values,coarse_velocity=velocity,mass_rate_coarse=mass_rates[0],mass_rate_fine=mass_rates[1])
                results = {}
                for sector in ['gradient','gram','total']:
                    result = transfer_rate(base[0]['mass'],fine_mass,*mass_rates,base_sectors[0][sector],base_sectors[1][sector],
                        matrix_rates[0][sector],matrix_rates[1][sector],interpolation,values,velocity)
                    endpoints = []
                    for pair,matrices in [(before,first_sectors),(after,last_sectors)]:
                        field = pair[0]['values'][:-1]
                        inverse_load = solve_banded((2,2),pair[0]['mass'],matrices[0][sector] @ field,check_finite=False)
                        endpoints.append(dense_mass(pair[1]['mass']) @ (interpolation @ inverse_load)-matrices[1][sector] @ (interpolation @ field))
                    dense_secant = (endpoints[1]-endpoints[0])/(2*step)
                    factored_endpoints = []
                    for pair,pair_weights in [(before,first_weights),(after,last_weights)]:
                        field = pair[0]['values'][:-1]
                        coarse_parts = stiffness_terms(pair[0]['layer'],pair_weights[0],field)
                        fine_parts = stiffness_terms(pair[1]['layer'],pair_weights[1],nodal_transfer(field))
                        load_name = {'gradient':'gradient_load','gram':'gram_load','total':'load'}[sector]
                        inverse_load = solve_banded((2,2),pair[0]['mass'],coarse_parts[load_name],check_finite=False)
                        factored_endpoints.append(band_action(pair[1]['mass'],nodal_transfer(inverse_load))-fine_parts[load_name])
                    secant = (factored_endpoints[1]-factored_endpoints[0])/(2*step)
                    derivative = result['derivative']
                    error = float(np.max(abs(derivative-secant)))
                    scale = max(float(np.max(abs(derivative))),float(np.max(abs(secant))),1e-10)
                    tolerance = 2e-4*scale+1e-9
                    evidence.check(tag+'_'+sector+'_direct_operator_derivative',error <= tolerance,dict(error=error,tolerance=tolerance))
                    channel_error = float(np.max(abs(derivative-sum(result['channels'].values()))))
                    channel_scale = sum(float(np.max(abs(value))) for value in result['channels'].values())
                    evidence.check(tag+'_'+sector+'_all_six_channels_and_paired_form',channel_error <= 2e-9*max(channel_scale,1e-10)+1e-11)
                    work = float(old['acceleration'] @ derivative)
                    secant_work = float(old['acceleration'] @ secant)
                    if sector != 'total':
                        name = 'Gram_stiffness_transfer' if sector == 'gram' else 'gradient_stiffness_transfer'
                        prior = next(row for row in previous['residual_channels'] if row['branch'] == branch and row['outer_step'] == step and row['channel'] == name)
                        evidence.check(tag+'_'+sector+'_matches_saved_nested_channel',abs(secant_work-prior['energy_work']) <= 1e-7*max(abs(prior['energy_work']),1e-10)+1e-10
                            and abs(float(np.max(abs(secant)))-prior['derivative_max']) <= 1e-7*max(prior['derivative_max'],1e-10)+1e-8,
                            dict(work_error=abs(secant_work-prior['energy_work']),maximum_error=abs(float(np.max(abs(secant)))-prior['derivative_max'])))
                    if sector not in mismatch_constants:
                        mismatch_constants[sector] = forcing_constant(result['mismatch'],mass_lower,stiffness_lower)
                    first_constant = mismatch_constants[sector]
                    second_constant = forcing_constant(result['mismatch_rate'],mass_lower,stiffness_lower)
                    bound = first_constant['upper']*coarse_velocity_norm+second_constant['upper']*coarse_value_norm
                    norm = dual_norm(mass_lower,derivative)
                    paired_bound = dual_norm(mass_lower,result['paired_velocity'])+dual_norm(mass_lower,result['paired_geometry'])
                    six_bound = sum(dual_norm(mass_lower,value) for value in result['channels'].values())
                    evidence.check(tag+'_'+sector+'_coarse_energy_and_paired_bounds',norm <= paired_bound+1e-10
                        and paired_bound <= six_bound+1e-10 and norm <= bound+1e-9)
                    row = dict(branch=branch,probe_step=step,sector=sector,derivative_max=float(np.max(abs(derivative))),
                        direct_secant_max=float(np.max(abs(secant))),comparison_error=error,numerical_tolerance=tolerance,
                        dense_vs_factored_secant_error=float(np.max(abs(dense_secant-secant))),
                        six_channel_reconstruction_error=channel_error,energy_work=work,direct_secant_work=secant_work,
                        forcing_dual_norm=norm,paired_velocity_dual_norm=dual_norm(mass_lower,result['paired_velocity']),
                        paired_geometry_dual_norm=dual_norm(mass_lower,result['paired_geometry']),
                        paired_norm_bound=paired_bound,six_channel_norm_bound=six_bound,
                        velocity_constant_sharp=first_constant['sharp'],velocity_constant_upper=first_constant['upper'],
                        geometry_constant_sharp=second_constant['sharp'],geometry_constant_upper=second_constant['upper'],
                        coarse_value_stiffness_norm=coarse_value_norm,coarse_velocity_stiffness_norm=coarse_velocity_norm,
                        coarse_energy_forcing_bound=float(bound),valid_for_claim=False)
                    evidence.report['cases'].append(row)
                    for name,load in result['channels'].items():
                        evidence.report['channels'].append(dict(branch=branch,probe_step=step,sector=sector,channel=name,
                            derivative_max=float(np.max(abs(load))),mass_dual_norm=dual_norm(mass_lower,load),
                            energy_work=float(old['acceleration'] @ load),valid_for_claim=False))
                    arrays.update({sector+'_derivative':derivative,sector+'_secant':secant,
                        sector+'_paired_velocity':result['paired_velocity'],sector+'_paired_geometry':result['paired_geometry'],
                        sector+'_mismatch':result['mismatch'],sector+'_mismatch_rate':result['mismatch_rate']})
                    results[sector] = result
                    print(json.dumps(row),flush=True)
                evidence.check(tag+'_gradient_plus_Gram_equals_total',np.max(abs(results['total']['derivative']-results['gradient']['derivative']-results['gram']['derivative']))
                    <= 1e-9*max(float(np.max(abs(results['total']['derivative']))),1e-8)+1e-10)
                path = evidence.output/(tag+'-direct-forcing.npz')
                np.savez_compressed(path,**arrays)
                evidence.own(path,'outputs')
                evidence.save()
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
