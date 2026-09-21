from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from annular_P2_weighted_projection_bounds_20260919 import band_action
from annular_weak_Gram_transfer_20260919 import adjoint_test, norm_bounds, source_mask
from annular_moving_Gram_budget_20260919 import adjoint_rate
from annular_wave_error_energy_20260919 import stiffness_weights
from derive_annular_frozen_Gram_refinement_20260919 import derivative_atoms, factor_bound
from derive_annular_local_atom_Gram_bounds_20260919 import local_expansion
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from run_annular_P2_continuum_bridge_20260918 import checked_load
import contextlib
import json
import numpy as np


def matched_states(evidence, branch, coarse_step):
    if coarse_step == 0:
        return state_pair(evidence, branch, False)
    coarse_folder = 'annular-P2-evolved-source-halving-'+branch+'-attempt'+('02' if branch == 'MTS' else '01')
    fine_folder = 'annular-P2-bulk513-MTS-time128-attempt01' if branch == 'MTS' else 'annular-P2-bulk513-evolution-reference-attempt01'
    fine_steps = 128 if branch == 'MTS' else 64
    fine_step = coarse_step*(fine_steps//32)
    coarse = checked_load(evidence, coarse_folder, 'steps32-accepted'+str(coarse_step).zfill(3)+'.npz')
    fine = checked_load(evidence, fine_folder, 'steps'+str(fine_steps)+'-accepted'+str(fine_step).zfill(3)+'.npz')
    target = 4e-5*coarse_step/32
    evidence.check(branch+'_'+str(coarse_step)+'_matched_stored_times',
        abs(float(coarse['time'])-target) < 1e-18 and abs(float(fine['time'])-target) < 1e-18)
    return [coarse['state'], fine['state']]


def evaluate_pair(systems, states):
    pair = []
    for system, state in zip(systems, states):
        center = int(np.argmin(abs(system.labels)))
        rates, geometry = system.solve(*state)
        layer = system.layer(system.labels[center], geometry)
        data = layer.evaluate(0., state[0, center], rates[center])
        pair.append(dict(layer=layer, rates=rates[center], all_rates=rates,
            values=state[0, center], mass=data['mass_bands'],
            weights=stiffness_weights(layer, state[0, center, -1])['gram']))
    return pair


def make_fields(pair, indices, shape):
    def transfer(values):
        return np.sum(shape*values[indices], axis=1)
    test = pair[1]['rates'][:-1]-transfer(pair[0]['rates'][:-1])
    adjoint, load = adjoint_test(pair[0]['mass'], pair[1]['mass'], test, indices, shape, pair[0]['layer'].count)
    fields = [pair[0]['values'][:-1], adjoint, transfer(pair[0]['values'][:-1]), test]
    return fields, load


def main():
    evidence = EvidenceRun('annular-moving-Gram-profile-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            full_live_P2_force_convergence_proven=False, full_nonlinear_stability_proven=False,
            full_live_geometry_reconstructed=True, matched_times_per_branch=9,
            uniform_evolving_refinement_rate_proven=False, sampled_path_not_continuous_solution_certificate=True,
            original_source_condition_retained=True, all_Gram_rows_retained=True,
            signed_gradient_curvature_cross_terms_retained=True)
        evidence.report['secants'], evidence.report['path_budgets'], evidence.report['bilinear_rows'] = [], [], []
        old_path = evidence.output.parent/'annular-live-weak-Gram-transfer-attempt01/status.json'
        previous = json.loads(old_path.read_text())
        evidence.own(old_path)
        evidence.check('previous_actual_weak_evidence_complete', previous['state'] == 'complete')
        field_names = ['coarse_trial', 'coarse_test', 'fine_trial', 'fine_test']
        for branch in ['reference', 'MTS']:
            systems = [IndexedGradedP2System(257, branch == 'MTS', 2e-5), IndexedGradedP2System(513, branch == 'MTS', 1e-5)]
            indices, shape, unused = systems[0].model.features_quadratic(systems[1].model.radii)
            stored = []
            for coarse_step in range(0, 33, 4):
                time = 4e-5*coarse_step/32
                tag = branch+'-'+str(coarse_step).zfill(3)
                states = matched_states(evidence, branch, coarse_step)
                pair = evaluate_pair(systems, states)
                fields, load = make_fields(pair, indices, shape)
                mass_error = float(max(abs(band_action(pair[0]['mass'], fields[1])-load)))
                evidence.check(tag+'_mass_adjoint_residual', mass_error < 1e-18+1e-10*float(max(abs(load))), mass_error)
                results, atoms_list, factors, expansions = [], [], [], []
                arrays = dict(coarse_mass=pair[0]['mass'], fine_mass=pair[1]['mass'])
                for number, (name, values) in enumerate(zip(field_names, fields)):
                    item = pair[number//2]
                    model, weights = item['layer'], item['weights']
                    jump = float(model.jump @ values)
                    atoms = derivative_atoms(model, values, jump)
                    bounds, factor = factor_bound(model, weights, values, jump, atoms)
                    norms = norm_bounds(model, weights, values)
                    evidence.check(tag+'_'+name+'_Gram_and_atom_bounds',
                        norms['Gram_norm'] <= bounds['fixed_P2_atom_bound']+1e-15
                        and abs(norms['Gram_norm']-bounds['Gram_norm']) < 1e-13)
                    expansion = local_expansion(model, model, values, jump, factor)
                    residual = float(np.max(abs(expansion['reconstruction_residual']), initial=0.))
                    allowance = float(2e-9*np.max(expansion['atom_majorant'], initial=0.)+2e-16)
                    evidence.check(tag+'_'+name+'_signed_atom_reconstruction', residual <= allowance,
                        dict(error=residual, tolerance=allowance))
                    results.append(dict(field=name, **norms, total_gradient_jump=atoms['total_gradient_jump'],
                        total_curvature_jump=atoms['total_curvature_jump'], fixed_P2_atom_bound=bounds['fixed_P2_atom_bound'],
                        reconstruction_error=residual, reconstruction_tolerance=allowance))
                    atoms_list.append(atoms)
                    factors.append(factor)
                    expansions.append(expansion)
                    arrays.update({name:values, name+'_factor':factor, name+'_gradient_atoms':atoms['gradient'],
                        name+'_curvature_atoms':atoms['curvature']})
                coarse_rows = pair[0]['weights']*factors[0]*factors[1]
                fine_rows = pair[1]['weights']*factors[2]*factors[3]
                work = float(np.sum(coarse_rows)-np.sum(fine_rows))
                source_work = float(np.sum(coarse_rows[source_mask(pair[0]['layer'])])-np.sum(fine_rows[source_mask(pair[1]['layer'])]))
                atom_bound = results[0]['fixed_P2_atom_bound']*results[1]['fixed_P2_atom_bound']+results[2]['fixed_P2_atom_bound']*results[3]['fixed_P2_atom_bound']
                evidence.check(tag+'_work_bounded', abs(work) <= atom_bound+1e-23)
                components = ['gradient', 'curvature', 'polynomial', 'reconstruction_residual']
                channels = []
                for first_name in components:
                    for second_name in components:
                        value = float(np.sum(pair[0]['weights']*expansions[0][first_name]*expansions[1][second_name])
                            -np.sum(pair[1]['weights']*expansions[2][first_name]*expansions[3][second_name]))
                        channels.append(value)
                        evidence.report['bilinear_rows'].append(dict(branch=branch,time=time,trial_component=first_name,
                            test_component=second_name,work=value,valid_for_claim=False))
                evidence.check(tag+'_all16_signed_bilinear_channels', abs(sum(channels)-work) < 1e-20+1e-10*sum(abs(value) for value in channels))
                if coarse_step in [0, 32]:
                    old = next(case for case in previous['cases'] if case['branch'] == branch and case['time'] == time)
                    evidence.check(tag+'_previous_endpoint_reproduced', abs(work-old['rows'][0]['weak_work']) < 1e-20)
                row = dict(branch=branch,time=time,coarse_step=coarse_step,weak_work=work,source_work=source_work,
                    remaining_work=work-source_work,row_absolute_bound=float(np.sum(abs(coarse_rows))+np.sum(abs(fine_rows))),
                    atom_work_bound=atom_bound,bilinear_absolute_sum=float(sum(abs(value) for value in channels)),
                    norms=results,valid_for_claim=False)
                evidence.report['cases'].append(row)
                arrays.update(coarse_weights=pair[0]['weights'],fine_weights=pair[1]['weights'],
                    coarse_trial_rate=pair[0]['rates'][:-1])
                path = evidence.output/(tag+'-profile.npz')
                np.savez_compressed(path, **arrays)
                evidence.own(path, 'outputs')
                stored.append(dict(time=time,masses=[item['mass'] for item in pair],fields=fields,atoms=atoms_list))
                evidence.save()
                print(json.dumps(dict(branch=branch,time=time,work=work,atom_bound=atom_bound,
                    test_A1=results[1]['total_gradient_jump'],test_A2=results[1]['total_curvature_jump'])),flush=True)
            variation_sums = np.zeros((4,2))
            for first, last in zip(stored[:-1], stored[1:]):
                duration = last['time']-first['time']
                mass_average = [(lower+upper)/2 for lower,upper in zip(first['masses'],last['masses'])]
                mass_rate = [(upper-lower)/duration for lower,upper in zip(first['masses'],last['masses'])]
                test_average = (first['fields'][3]+last['fields'][3])/2
                test_rate = (last['fields'][3]-first['fields'][3])/duration
                adjoint_average = (first['fields'][1]+last['fields'][1])/2
                result = adjoint_rate(*mass_average,*mass_rate,test_average,test_rate,adjoint_average,indices,shape)
                direct = (last['fields'][1]-first['fields'][1])/duration
                error = float(max(abs(result['rate']-direct)))
                tolerance = 1e-8*max(float(max(abs(direct))),1e-12)+1e-10
                evidence.check(branch+'_'+str(last['time'])+'_exact_mass_adjoint_secant',error <= tolerance,dict(error=error,tolerance=tolerance))
                for number,name in enumerate(field_names):
                    model = systems[number//2].model
                    rate = (last['fields'][number]-first['fields'][number])/duration
                    rate_atoms = derivative_atoms(model,rate,float(model.jump @ rate))
                    for order,component in enumerate(['gradient','curvature']):
                        before,after = first['atoms'][number][component],last['atoms'][number][component]
                        increment = after-before
                        residual = float(np.max(abs(increment-duration*rate_atoms[component]),initial=0.))
                        allowance = 2e-10*max(float(np.max(abs(before),initial=0.)),float(np.max(abs(after),initial=0.)),1e-10)+1e-14
                        evidence.check(branch+'_'+str(last['time'])+'_'+name+'_'+component+'_linear_atom_transport',residual <= allowance,
                            dict(error=residual,tolerance=allowance))
                        variation_sums[number,order] += np.sum(abs(increment))
                evidence.report['secants'].append(dict(branch=branch,start=first['time'],stop=last['time'],
                    direct_max=float(max(abs(direct))),comparison_error=error,numerical_tolerance=tolerance,
                    test_acceleration_max=float(max(abs(result['channels']['test_acceleration']))),
                    fine_mass_transport_max=float(max(abs(result['channels']['fine_mass_transport']))),
                    coarse_mass_transport_max=float(max(abs(result['channels']['coarse_mass_transport']))),valid_for_claim=False))
            for number,name in enumerate(field_names):
                for order,component in enumerate(['gradient','curvature']):
                    initial = float(np.sum(abs(stored[0]['atoms'][number][component])))
                    final = float(np.sum(abs(stored[-1]['atoms'][number][component])))
                    sampled_max = float(max(np.sum(abs(item['atoms'][number][component])) for item in stored))
                    bound = initial+float(variation_sums[number,order])
                    evidence.check(branch+'_'+name+'_'+component+'_sampled_path_budget',sampled_max <= bound+1e-10*max(bound,1e-20))
                    evidence.report['path_budgets'].append(dict(branch=branch,field=name,component=component,
                        initial=initial,final=final,sampled_max=sampled_max,total_sampled_atom_variation=float(variation_sums[number,order]),
                        interpolant_bound=bound,actual_continuous_time_bound=False,valid_for_claim=False))
        with (evidence.output/'completion.txt').open('w',encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt','outputs')
        evidence.save()
        print(json.dumps(dict(state='complete',checks=len(evidence.report['checks']))),flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
