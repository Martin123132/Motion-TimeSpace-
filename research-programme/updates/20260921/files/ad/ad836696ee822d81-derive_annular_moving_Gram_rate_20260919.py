from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_moving_Gram_budget_20260919 import adjoint_rate, variation_rate, pairing_rate
from derive_annular_moving_Gram_profile_20260919 import evaluate_pair, make_fields
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from derive_annular_frozen_Gram_refinement_20260919 import derivative_atoms
from run_annular_P2_continuum_bridge_20260918 import checked_load
import contextlib
import json
import numpy as np


def work(pair, fields):
    factors = [pair[number//2]['layer'].lifted @ field for number,field in enumerate(fields)]
    value = float(np.sum(pair[0]['weights']*factors[0]*factors[1])-np.sum(pair[1]['weights']*factors[2]*factors[3]))
    return value, factors


def main():
    evidence = EvidenceRun('annular-moving-Gram-rate-attempt01', __file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,full_nonlinear_stability_proven=False,
            uniform_evolving_refinement_rate_proven=False,both_mass_transport_terms_retained=True,
            source_jump_rate_retained=True,inverse_residual_acceleration_retained=True,
            all_Gram_rows_retained=True,full_global_canonical_direction=True,
            rates_are_finite_difference_estimates=True,finite_probes_not_time_uniform_certificate=True)
        evidence.report['atom_rates'], evidence.report['adjoint_channel_atoms'] = [], []
        field_names = ['coarse_trial','coarse_test','fine_trial','fine_test']
        algebra_path = evidence.output.parent/'annular-moving-Gram-algebra-attempt01/status.json'
        algebra = json.loads(algebra_path.read_text())
        evidence.own(algebra_path)
        evidence.check('independent_algebra_complete',algebra['state'] == 'complete' and all(row['passed'] for row in algebra['checks']))
        for branch in ['reference','MTS']:
            systems = [IndexedGradedP2System(257,branch == 'MTS',2e-5),IndexedGradedP2System(513,branch == 'MTS',1e-5)]
            states = state_pair(evidence,branch,True)
            base = evaluate_pair(systems,states)
            indices,shape,unused = systems[0].model.features_quadratic(systems[1].model.radii)
            fields,unused = make_fields(base,indices,shape)
            base_work,base_factors = work(base,fields)
            for step in [2e-7,1e-7,5e-8,2.5e-8]:
                tag = branch+'-'+str(step)
                saved = checked_load(evidence,'annular-live-compensated-rate-attempt01',tag+'-compensated-rate.npz')
                flows = [saved[str(level)+'_full_direction'] for level in range(2)]
                evidence.check(tag+'_saved_base_states_and_masses_match', all(np.array_equal(state,saved[str(level)+'_state'])
                    and np.max(abs(base[level]['mass']-saved[str(level)+'_mass_bands'])) < 1e-14
                    for level,state in enumerate(states)))
                before = evaluate_pair(systems,[state-step*flow for state,flow in zip(states,flows)])
                after = evaluate_pair(systems,[state+step*flow for state,flow in zip(states,flows)])
                first_fields,unused = make_fields(before,indices,shape)
                last_fields,unused = make_fields(after,indices,shape)
                first_work,first_factors = work(before,first_fields)
                last_work,last_factors = work(after,last_fields)
                mass_rates = [saved[str(level)+'_mass_rate'] for level in range(2)]
                evidence.check(tag+'_saved_full_tangent_rates_reproduced',all(
                    np.max(abs(before[level]['rates']-saved[str(level)+'_rates_before'])) < 1e-13
                    and np.max(abs(after[level]['rates']-saved[str(level)+'_rates_after'])) < 1e-13
                    and np.max(abs((after[level]['mass']-before[level]['mass'])/(2*step)-mass_rates[level])) < 1e-12
                    for level in range(2)))
                delta_rate = saved['acceleration_difference']
                adjoint = adjoint_rate(base[0]['mass'],base[1]['mass'],*mass_rates,fields[3],delta_rate,fields[1],indices,shape)
                actual = (last_fields[1]-first_fields[1])/(2*step)
                error = float(max(abs(adjoint['rate']-actual)))
                tolerance = 2e-4*max(float(max(abs(actual))),float(max(abs(adjoint['rate']))),1e-8)+1e-8
                evidence.check(tag+'_differential_adjoint_control',error <= tolerance,dict(error=error,tolerance=tolerance))
                centered = adjoint_rate(*[(first['mass']+last['mass'])/2 for first,last in zip(before,after)],
                    *mass_rates,(first_fields[3]+last_fields[3])/2,(last_fields[3]-first_fields[3])/(2*step),
                    (first_fields[1]+last_fields[1])/2,indices,shape)
                exact_error = float(max(abs(centered['rate']-actual)))
                exact_tolerance = 1e-8*max(float(max(abs(actual))),1e-12)+1e-10
                evidence.check(tag+'_exact_secant_adjoint_control',exact_error <= exact_tolerance,dict(error=exact_error,tolerance=exact_tolerance))
                field_rates = [base[0]['rates'][:-1],adjoint['rate'],
                    np.sum(shape*base[0]['rates'][:-1][indices],axis=1),delta_rate]
                factor_rates = [base[number//2]['layer'].lifted @ field for number,field in enumerate(field_rates)]
                pair_results,secant_results = [],[]
                for level in range(2):
                    position = 2*level
                    weight_rate = (after[level]['weights']-before[level]['weights'])/(2*step)
                    result = pairing_rate(base[level]['weights'],weight_rate,base_factors[position],factor_rates[position],
                        base_factors[position+1],factor_rates[position+1])
                    pair_results.append(result)
                    mean_weight = (after[level]['weights']+before[level]['weights'])/2
                    mean_trial = (last_factors[position]+first_factors[position])/2
                    mean_test = (last_factors[position+1]+first_factors[position+1])/2
                    trial_secant = (last_factors[position]-first_factors[position])/(2*step)
                    test_secant = (last_factors[position+1]-first_factors[position+1])/(2*step)
                    exact = pairing_rate(mean_weight,weight_rate,mean_trial,trial_secant,mean_test,test_secant)
                    exact_mixed = float(step**2*np.sum(weight_rate*trial_secant*test_secant))
                    secant_results.append(exact['rate']+exact_mixed)
                    evidence.check(tag+'_'+str(level)+'_pair_rate_absolute_bound',abs(result['rate']) <= result['row_absolute_rate_bound']+1e-23)
                direct = (last_work-first_work)/(2*step)
                predicted = pair_results[0]['rate']-pair_results[1]['rate']
                work_error = abs(direct-predicted)
                work_tolerance = 2e-4*max(abs(direct),abs(predicted),1e-20)+1e-16
                evidence.check(tag+'_signed_work_differential_control',work_error <= work_tolerance,dict(error=work_error,tolerance=work_tolerance))
                work_secant_error = abs(direct-secant_results[0]+secant_results[1])
                evidence.check(tag+'_exact_triple_product_secant',work_secant_error <= 1e-16+1e-10*abs(direct),work_secant_error)
                arrays = dict(adjoint_rate=adjoint['rate'],direct_adjoint_rate=actual,compensated_test_rate=delta_rate)
                coarse_model = base[0]['layer']
                test_atoms = derivative_atoms(coarse_model,fields[1],float(coarse_model.jump @ fields[1]))
                for channel_name,channel_rate in adjoint['channels'].items():
                    channel_atoms = derivative_atoms(coarse_model,channel_rate,float(coarse_model.jump @ channel_rate))
                    arrays['adjoint_channel_'+channel_name] = channel_rate
                    for component in ['gradient','curvature']:
                        atom_values,atom_rates = test_atoms[component],channel_atoms[component]
                        evidence.report['adjoint_channel_atoms'].append(dict(branch=branch,tangent_step=step,
                            channel=channel_name,component=component,source_jump_rate=float(coarse_model.jump @ channel_rate),
                            absolute_atom_rate=float(np.sum(abs(atom_rates))),
                            signed_nonzero_atom_contribution=float(np.sum(np.sign(atom_values)*atom_rates)),
                            zero_atom_absolute_allowance=float(np.sum(abs(atom_rates[atom_values == 0.]))),valid_for_claim=False))
                for number,(name,field,rate) in enumerate(zip(field_names,fields,field_rates)):
                    model = base[number//2]['layer']
                    jump = float(model.jump @ field)
                    jump_rate = float(model.jump @ rate)
                    atoms = derivative_atoms(model,field,jump)
                    rates = derivative_atoms(model,rate,jump_rate)
                    arrays.update({name+'_gradient_atom_rate':rates['gradient'],name+'_curvature_atom_rate':rates['curvature']})
                    for component in ['gradient','curvature']:
                        budget = variation_rate(atoms[component],rates[component])
                        evidence.check(tag+'_'+name+'_'+component+'_variation_rate_bound',
                            abs(budget['upper_right_rate']) <= budget['absolute_rate_budget']+1e-10*max(budget['absolute_rate_budget'],1e-20))
                        evidence.report['atom_rates'].append(dict(branch=branch,tangent_step=step,field=name,component=component,
                            source_jump=jump,source_jump_rate=jump_rate,**budget,valid_for_claim=False))
                channels = {name:pair_results[0]['channels'][name]-pair_results[1]['channels'][name] for name in pair_results[0]['channels']}
                row = dict(branch=branch,tangent_step=step,base_work=base_work,
                    adjoint_rate_max=float(max(abs(adjoint['rate']))),adjoint_error=error,adjoint_tolerance=tolerance,
                    adjoint_exact_secant_error=exact_error,adjoint_exact_secant_tolerance=exact_tolerance,
                    test_acceleration_max=float(max(abs(adjoint['channels']['test_acceleration']))),
                    fine_mass_transport_max=float(max(abs(adjoint['channels']['fine_mass_transport']))),
                    coarse_mass_transport_max=float(max(abs(adjoint['channels']['coarse_mass_transport']))),
                    work_rate=predicted,direct_work_rate=direct,work_rate_error=work_error,work_rate_tolerance=work_tolerance,
                    work_exact_secant_error=work_secant_error,**channels,
                    work_absolute_rate_bound=pair_results[0]['row_absolute_rate_bound']+pair_results[1]['row_absolute_rate_bound'],valid_for_claim=False)
                evidence.report['cases'].append(row)
                path = evidence.output/(tag+'-moving-rate.npz')
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
