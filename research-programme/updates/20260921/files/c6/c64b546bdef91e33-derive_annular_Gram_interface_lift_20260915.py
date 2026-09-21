from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_gram_joint_action_20260909 import gram_matrices
from scipy.linalg import cho_factor, cho_solve
import json
import numpy as np


def assembly(count, position):
    radii = np.linspace(0., 1., count)
    spacing = radii[1]-radii[0]
    cell = int(position.real/spacing)
    left_length = position-radii[cell]
    right_length = radii[cell+1]-position
    dtype = np.result_type(position, float)
    base_factors = np.diff(np.eye(count), axis=0)
    cut_stiffness = base_factors.T @ base_factors/spacing
    cut_stiffness = cut_stiffness.astype(dtype)
    old_cell = base_factors[cell]
    cut_stiffness -= np.outer(old_cell, old_cell)/spacing
    cut_stiffness[cell, cell] += 1/left_length
    cut_stiffness[cell+1, cell+1] += 1/right_length
    jump = np.zeros(count, dtype=dtype)
    jump[cell], jump[cell+1] = 1/left_length, 1/right_length
    jump_derivative = np.zeros(count, dtype=dtype)
    jump_derivative[cell], jump_derivative[cell+1] = -1/left_length**2, 1/right_length**2
    right_mask = radii > position.real
    hinge = np.where(right_mask, radii-position, 0.)
    hinge_derivative = -right_mask.astype(float)
    original, unused_sampling = gram_matrices(count)
    hinge_factors = original @ hinge
    lifted = original-np.outer(hinge_factors, jump)
    lifted_derivative = -np.outer(original @ hinge_derivative, jump)-np.outer(hinge_factors, jump_derivative)
    stiffness = cut_stiffness+lifted.T @ lifted/spacing
    return dict(radii=radii, spacing=spacing, cell=cell, left_length=left_length,
                right_length=right_length, jump=jump, hinge=hinge, original=original,
                lifted=lifted, lifted_derivative=lifted_derivative, stiffness=stiffness)


def energy_force(data, profile):
    cell = data['cell']
    factors = data['lifted'] @ profile
    factor_derivative = data['lifted_derivative'] @ profile
    force = (profile[cell]**2/(2*data['left_length']**2)
             -profile[cell+1]**2/(2*data['right_length']**2)
             -factors @ factor_derivative/data['spacing'])
    return profile @ data['stiffness'] @ profile/2, force


def main():
    evidence = EvidenceRun('annular-Gram-interface-lift-static-attempt01', __file__)
    try:
        source = evidence.root/'source-intake/navier-stokes/20260914/annular-trace-static-force-phase-audit-attempt01/status.json'
        old = json.loads(source.read_text())
        evidence.check('unlifted_MTS_force_failure_preserved', old['state'] == 'complete'
                       and not old['verdict']['MTS_cut_cell_reference_correction']['passes_half_percent_pressure_gate'])
        evidence.own(source)
        random = np.random.default_rng(260915)
        for count in [33, 65, 129, 257]:
            spacing = 1/(count-1)
            for phase in [.2, .5, .8]:
                position = (int(.6/spacing)+phase)*spacing
                data = assembly(count, position)
                factorization = cho_factor(data['stiffness'][1:-1, 1:-1])
                for left_value, right_value in [(1., 0.), (.7, -.4)]:
                    right_hand = -data['stiffness'][1:-1, 0]*left_value-data['stiffness'][1:-1, -1]*right_value
                    profile = np.concatenate([[left_value], cho_solve(factorization, right_hand), [right_value]])
                    exact = np.where(data['radii'] < position, left_value*(position-data['radii'])/position,
                                     right_value*(data['radii']-position)/(1-position))
                    energy, force = energy_force(data, profile)
                    exact_energy = left_value**2/(2*position)+right_value**2/(2*(1-position))
                    exact_force = left_value**2/(2*position**2)-right_value**2/(2*(1-position)**2)
                    force_error = float(abs(force-exact_force)/max(abs(exact_force), 1e-15))
                    profile_error = float(np.max(abs(profile-exact)))
                    evidence.check(str(count)+str(phase)+str(left_value)+'_exact_static_energy_profile_and_force',
                                   abs(energy-exact_energy) < 2e-9 and profile_error < 2e-10 and force_error < 2e-8)
                    evidence.report['cases'].append(dict(count=count, phase=phase, left_value=left_value, right_value=right_value,
                                                         force_ratio=float(force/exact_force), relative_force_error=force_error,
                                                         profile_error=profile_error, energy_error=float(abs(energy-exact_energy))))
                continuous_slope = data['radii']-position
                evidence.check(str(count)+str(phase)+'_all_Gram_rows_retained_and_smooth_trace_recovered',
                               data['lifted'].shape == data['original'].shape
                               and np.max(abs(data['lifted'] @ continuous_slope-data['original'] @ continuous_slope)) < 2e-11
                               and np.max(abs(data['lifted'] @ exact)) < 2e-11)
                if count == 65:
                    probe = .03*random.normal(size=count)
                    step = spacing*1e-4
                    upper_two = energy_force(assembly(count, position+2*step), probe)[0]
                    upper = energy_force(assembly(count, position+step), probe)[0]
                    lower = energy_force(assembly(count, position-step), probe)[0]
                    lower_two = energy_force(assembly(count, position-2*step), probe)[0]
                    difference = -(-upper_two+8*upper-8*lower+lower_two)/(12*step)
                    exact_force = energy_force(data, probe)[1]
                    relative_error = float(abs(difference-exact_force)/max(1., abs(exact_force)))
                    evidence.check(str(phase)+'_independent_full_shape_derivative', relative_error < 2e-7, relative_error)
        evidence.report.update(scope='Static planar boundary-adapted Gram candidate: exact broken-slope lift, not the unchanged parent boundary action.',
                               boundary_rule='G_b = G(I-rho_b j_b^T); rho_b=(R-b)_+; j_b q=q_left/(b-R_left)+q_right/(R_right-b).',
                               interpretation='Remove the reflecting-interface derivative jump from the bulk third-difference penalty; retain every Gram factor with its original weight.',
                               positive_Gram_energy_by_factorization=True,
                               no_fitted_force_or_post_evolution_projection=True,
                               unchanged_bulk_action_away_from_interface=True,
                               original_boundary_action_changed_explicitly=True,
                               unique_parent_boundary_selection_proven=False,
                               arbitrary_dynamic_MTS_boundary_completion_derived=False,
                               second_derivative_jump_handling_complete=False,
                               curved_time_link_current_derived=False,
                               one_sided_decoupling_proven=False,
                               full_GR_limit_proven=False, valid_for_physics_claim=False)
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
