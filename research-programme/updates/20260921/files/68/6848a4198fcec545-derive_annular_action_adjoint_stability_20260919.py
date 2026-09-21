from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_action_test_energy_20260919 import dense_mass, dense_stiffness, transfer_constants
from annular_wave_error_energy_20260919 import stiffness_weights, stiffness_terms
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_moving_Gram_profile_20260919 import evaluate_pair, make_fields
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-action-adjoint-stability-attempt01',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,uniform_evolving_refinement_rate_proven=False,
            original_source_condition_retained=True,all_Gram_rows_retained=True,
            full_live_geometry_reconstructed=True,numerical_operator_bounds_not_interval_certified=True,
            all_fine_directions_tested_by_finite_matrix_not_only_actual_velocity=True)
        for branch in ['reference','MTS']:
            systems = [IndexedGradedP2System(257,branch == 'MTS',2e-5),IndexedGradedP2System(513,branch == 'MTS',1e-5)]
            indices,shape,unused = systems[0].model.features_quadratic(systems[1].model.radii)
            for final in [False,True]:
                tag = branch+('_final' if final else '_initial')
                states = state_pair(evidence,branch,final)
                pair = evaluate_pair(systems,states)
                fields,unused = make_fields(pair,indices,shape)
                weights = [stiffness_weights(item['layer'],item['values'][-1]) for item in pair]
                masses = [dense_mass(item['mass']) for item in pair]
                stiffness = [dense_stiffness(item['layer'],weight) for item,weight in zip(pair,weights)]
                for level,item in enumerate(pair):
                    action = stiffness_terms(item['layer'],weights[level],fields[2*level])
                    error = float(np.max(abs(stiffness[level] @ fields[2*level]-action['load'])))
                    tolerance = 2e-11*max(float(np.max(abs(action['load']))),1e-12)+1e-13
                    evidence.check(tag+'_'+str(level)+'_assembled_action_stiffness',error <= tolerance,dict(error=error,tolerance=tolerance))
                    scale = float(np.max(abs(stiffness[level])))
                    evidence.check(tag+'_'+str(level)+'_symmetric_mass_stiffness',np.max(abs(stiffness[level]-stiffness[level].T)) < 1e-13*scale
                        and np.max(abs(masses[level]-masses[level].T)) < 1e-13*float(np.max(abs(masses[level]))))
                result = transfer_constants(pair[0]['mass'],masses[1],stiffness[0],stiffness[1],indices,shape,
                    pair[0]['layer'].lifted,weights[0]['gram'])
                adjoint = result['adjoint'] @ fields[3]
                evidence.check(tag+'_matrix_adjoint_matches_banded_solve',np.max(abs(adjoint-fields[1])) < 1e-18+1e-10*float(np.max(abs(fields[1]))))
                for level,name in enumerate(['coarse','fine']):
                    lower = result[name+'_lower']
                    residual = float(np.max(abs(lower @ lower.T-stiffness[level])))
                    tolerance = 1e-12*float(np.max(abs(stiffness[level])))
                    evidence.check(tag+'_'+name+'_positive_cholesky_and_residual',np.all(np.diag(lower) > 0.) and residual <= tolerance,
                        dict(error=residual,tolerance=tolerance))
                for name in ['stiffness','gram']:
                    constant = result[name]
                    evidence.check(tag+'_'+name+'_operator_eigen_residual_and_upper_bound',
                        constant['eigen_residual'] <= 1e-10*max(constant['sharp_squared'],1.)
                        and constant['sharp_squared'] <= constant['row_sum_squared_bound']+1e-10)
                evidence.check(tag+'_Gram_dominated_by_full_stiffness',result['gram']['sharp_squared'] <= result['stiffness']['sharp_squared']+1e-8)
                maximizing = result['maximizer']
                projected = result['adjoint'] @ maximizing
                quotient = float(projected @ stiffness[0] @ projected/(maximizing @ stiffness[1] @ maximizing))
                evidence.check(tag+'_maximizing_direction_original_coordinate_check',abs(quotient-result['stiffness']['sharp_squared']) < 2e-6*max(quotient,1.),quotient)
                fine_form = float(fields[3] @ stiffness[1] @ fields[3])
                coarse_form = float(fields[1] @ stiffness[0] @ fields[1])
                factors = [pair[number//2]['layer'].lifted @ field for number,field in enumerate(fields)]
                norms = [float(np.sqrt(np.sum(weights[number//2]['gram']*factor**2))) for number,factor in enumerate(factors)]
                actual_gram_form = norms[1]**2
                full_upper = result['stiffness']['row_sum_squared_bound']
                gram_upper = result['gram']['row_sum_squared_bound']
                evidence.check(tag+'_actual_direction_energy_bounds',coarse_form <= full_upper*fine_form+1e-20
                    and actual_gram_form <= gram_upper*fine_form+1e-20 and norms[3]**2 <= fine_form+1e-20)
                work = float(np.sum(weights[0]['gram']*factors[0]*factors[1])-np.sum(weights[1]['gram']*factors[2]*factors[3]))
                prefactor = np.sqrt(gram_upper)*norms[0]+norms[2]
                work_bound = float(prefactor*np.sqrt(max(fine_form,0.)))
                evidence.check(tag+'_action_stiffness_weak_work_bound',abs(work) <= work_bound+1e-22)
                row = dict(branch=branch,time=4e-5 if final else 0.,
                    stiffness_sharp_squared=result['stiffness']['sharp_squared'],stiffness_squared_upper=full_upper,
                    Gram_sharp_squared=result['gram']['sharp_squared'],Gram_squared_upper=gram_upper,
                    worst_direction_quotient=quotient,fine_velocity_stiffness=fine_form,coarse_adjoint_stiffness=coarse_form,
                    actual_stiffness_ratio=coarse_form/fine_form if fine_form > 0. else 0.,
                    actual_Gram_ratio=actual_gram_form/fine_form if fine_form > 0. else 0.,
                    weak_work=work,work_prefactor=float(prefactor),action_stiffness_work_bound=work_bound,
                    coarse_trial_Gram_norm=norms[0],fine_trial_Gram_norm=norms[2],valid_for_claim=False)
                evidence.report['cases'].append(row)
                path = evidence.output/(tag+'-action-matrices.npz')
                arrays = dict(coarse_mass=masses[0],fine_mass=masses[1],coarse_stiffness=stiffness[0],fine_stiffness=stiffness[1],
                    adjoint_operator=result['adjoint'],interpolation=result['interpolation'],maximizing_direction=maximizing,
                    velocity_difference=fields[3],mass_adjoint=fields[1],
                    coarse_gradient_weights=weights[0]['gradient'],coarse_Gram_weights=weights[0]['gram'],
                    fine_gradient_weights=weights[1]['gradient'],fine_Gram_weights=weights[1]['gram'])
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
