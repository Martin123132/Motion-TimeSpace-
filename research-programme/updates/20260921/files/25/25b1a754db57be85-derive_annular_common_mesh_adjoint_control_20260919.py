from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_action_test_energy_20260919 import right_inverse_transpose,operator_bound
from annular_P2_graded_source_20260919 import GradedSourceAction
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from run_annular_P2_continuum_bridge_20260918 import checked_load
from scipy.linalg import cholesky,cho_solve
from scipy.sparse import csr_matrix
import contextlib
import json
import numpy as np


def features(model,radius):
    indices,shape,unused = model.features_quadratic(radius)
    return csr_matrix((shape.ravel(),(np.repeat(np.arange(len(radius)),3),indices.ravel())),shape=(len(radius),model.count))


def main():
    evidence = EvidenceRun('annular-common-mesh-adjoint-control-attempt01',__file__)
    try:
        evidence.report.update(github_action=False,subagents_used=False,no_new_evolution=True,
            full_live_P2_force_convergence_proven=False,uniform_evolving_refinement_rate_proven=False,
            counterfactual_diagnostic_not_replacement_action=True,original_transfer_and_force_results_unchanged=True,
            omitted_transfer_defect_not_allowed=True,projection_uses_fine_reference_mass_density=True,
            time_dependent_projection_not_inserted_in_original_energy_equations=True)
        for branch in ['reference','MTS']:
            coarse = GradedSourceAction(257,branch == 'MTS',source_cap=2e-5)
            fine_system = IndexedGradedP2System(513,branch == 'MTS',1e-5)
            states = state_pair(evidence,branch,True)
            center = int(np.argmin(abs(fine_system.labels)))
            rates,geometry = fine_system.solve(*states[1])
            fine = fine_system.layer(fine_system.labels[center],geometry)
            saved = checked_load(evidence,'annular-action-adjoint-stability-attempt01',branch+'_final-action-matrices.npz')
            coarse_lower = cholesky(saved['coarse_stiffness'],lower=True,check_finite=False)
            fine_lower = cholesky(saved['fine_stiffness'],lower=True,check_finite=False)
            mass_lower = cholesky(saved['coarse_mass'],lower=True,check_finite=False)
            fine_mass_lower = cholesky(saved['fine_mass'],lower=True,check_finite=False)
            edges = np.unique(np.concatenate([coarse.edges,fine.edges]))
            lengths = np.diff(edges)
            radius = (edges[:-1,None]+lengths[:,None]*fine.fractions).ravel()
            quadrature = (lengths[:,None]*fine.weights).ravel()
            physical,jacobian,unused = fine.mapping(radius,states[1][0,center,-1])
            density = jacobian*physical**4/fine.coefficient(0.,physical)
            fine_features,coarse_features = features(fine,radius),features(coarse,radius)
            weighted = fine_features.multiply((quadrature*density)[:,None])
            cross = (coarse_features.T @ weighted).toarray()
            common_fine_mass = (fine_features.T @ weighted).toarray()
            fine_error = float(np.max(abs(common_fine_mass-saved['fine_mass'])))
            fine_scale = float(np.max(abs(saved['fine_mass'])))
            evidence.check(branch+'_common_mesh_reproduces_fine_mass',fine_error < 1e-8*fine_scale,
                dict(error=fine_error,scale=fine_scale,not_exact_polynomial_quadrature=True))
            candidate = cho_solve((mass_lower,True),cross,check_finite=False)
            candidate_forward = cho_solve((fine_mass_lower,True),cross.T,check_finite=False)
            evidence.check(branch+'_candidate_exact_mass_duality',np.max(abs(saved['coarse_mass'] @ candidate
                -candidate_forward.T @ saved['fine_mass'])) < 1e-10*fine_scale)
            whitened = right_inverse_transpose(candidate,fine_lower)
            constant,unused = operator_bound(coarse_lower.T @ whitened)
            gram_constant,unused = operator_bound(np.sqrt(saved['coarse_Gram_weights'])[:,None]*(coarse.lifted @ whitened))
            nodal_cross = saved['interpolation'].T @ saved['fine_mass']
            alias = cho_solve((mass_lower,True),nodal_cross-cross,check_finite=False)
            defect_error = float(np.max(abs(saved['adjoint_operator']-candidate-alias)))
            evidence.check(branch+'_nodal_minus_common_cross_mass_defect',defect_error < 1e-9,defect_error)
            worst = saved['maximizing_direction']
            reference_projection = candidate @ worst
            defect_projection = alias @ worst
            original_projection = saved['adjoint_operator'] @ worst
            stiffness = saved['coarse_stiffness']
            original_energy = float(original_projection @ stiffness @ original_projection)
            common_energy = float(reference_projection @ stiffness @ reference_projection)
            defect_energy = float(defect_projection @ stiffness @ defect_projection)
            cross_energy = float(2*reference_projection @ stiffness @ defect_projection)
            evidence.check(branch+'_signed_worst_energy_split',abs(original_energy-common_energy-defect_energy-cross_energy) < 1e-8*max(original_energy,1.))
            test = saved['velocity_difference']
            actual_common = candidate @ test
            actual_defect = alias @ test
            trial = states[0][0,center,:-1]
            trial_factor = coarse.lifted @ trial
            original_coarse_work = float(np.sum(saved['coarse_Gram_weights']*trial_factor*(coarse.lifted @ saved['mass_adjoint'])))
            common_coarse_work = float(np.sum(saved['coarse_Gram_weights']*trial_factor*(coarse.lifted @ actual_common)))
            defect_coarse_work = float(np.sum(saved['coarse_Gram_weights']*trial_factor*(coarse.lifted @ actual_defect)))
            evidence.check(branch+'_original_work_common_plus_defect_retained',abs(original_coarse_work-common_coarse_work-defect_coarse_work) < 1e-19)
            evidence.check(branch+'_counterfactual_operator_upper_bounds',constant['sharp_squared'] <= constant['row_sum_squared_bound']+1e-10
                and gram_constant['sharp_squared'] <= gram_constant['row_sum_squared_bound']+1e-10
                and gram_constant['sharp_squared'] <= constant['sharp_squared']+1e-8)
            row = dict(branch=branch,common_mesh_cells=len(lengths),fine_mass_relative_error=fine_error/fine_scale,
                common_stiffness_sharp_squared=constant['sharp_squared'],common_stiffness_squared_upper=constant['row_sum_squared_bound'],
                common_Gram_sharp_squared=gram_constant['sharp_squared'],common_Gram_squared_upper=gram_constant['row_sum_squared_bound'],
                nodal_cross_mass_difference_max=float(np.max(abs(nodal_cross-cross))),
                worst_original_energy=original_energy,worst_common_projection_energy=common_energy,
                worst_defect_energy=defect_energy,worst_signed_cross_energy=cross_energy,
                actual_original_coarse_work=original_coarse_work,actual_common_coarse_work=common_coarse_work,
                actual_retained_defect_coarse_work=defect_coarse_work,valid_for_claim=False)
            evidence.report['cases'].append(row)
            path = evidence.output/(branch+'-common-mesh-control.npz')
            np.savez_compressed(path,cross_mass=cross,nodal_cross_mass=nodal_cross,candidate_adjoint=candidate,
                candidate_forward=candidate_forward,retained_alias_operator=alias,worst_common_projection=reference_projection,
                worst_defect_projection=defect_projection,actual_common_projection=actual_common,actual_defect_projection=actual_defect)
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
