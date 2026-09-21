from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_weak_Gram_transfer_20260919 import adjoint_test, source_mask, norm_bounds, TEMPLATE_BOUND
from annular_wave_error_energy_20260919 import stiffness_weights
from annular_P2_weighted_projection_bounds_20260919 import band_action
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
from scipy.linalg import solve_banded
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-live-weak-Gram-transfer-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, both_initial_and_final_states=True, all_Gram_rows_retained=True,
            full_live_geometry_reconstructed=True, both_nonnested_jump_defects_retained=True,
            mass_adjoint_not_an_assumed_orthogonal_projection=True, original_source_condition_retained=True,
            no_uniform_actual_regularity_or_refinement_rate_claim=True, full_nonlinear_stability_proven=False)
        previous = {}
        for name in ['annular-weak-Gram-algebra-attempt01', 'annular-live-wave-error-energy-attempt01']:
            path = evidence.output.parent/name/'status.json'
            status = json.loads(path.read_text())
            evidence.own(path)
            evidence.check(name+'_complete', status['state'] == 'complete' and all(row['passed'] for row in status['checks']))
            previous[name] = status
        for branch in ['reference', 'MTS']:
            systems = [IndexedGradedP2System(257, branch == 'MTS', 2e-5), IndexedGradedP2System(513, branch == 'MTS', 1e-5)]
            center = int(np.argmin(abs(systems[1].labels)))
            indices, shape, unused = systems[0].model.features_quadratic(systems[1].model.radii)

            def transfer(values):
                return np.sum(shape*values[indices], axis=1)

            for final in [False, True]:
                states = state_pair(evidence, branch, final)
                layers, data, rates, weights = [], [], [], []
                for system, state in zip(systems, states):
                    velocity, geometry = system.solve(*state)
                    layer = system.layer(system.labels[center], geometry)
                    layers.append(layer)
                    rates.append(velocity[center])
                    data.append(layer.evaluate(0., state[0, center], velocity[center]))
                    weights.append(stiffness_weights(layer, state[0, center, -1])['gram'])
                coarse, fine = layers
                values = states[0][0, center, :-1]
                test = rates[1][:-1]-transfer(rates[0][:-1])
                adjoint, adjoint_load = adjoint_test(data[0]['mass_bands'], data[1]['mass_bands'], test, indices, shape, coarse.count)
                adjoint_error = float(max(abs(band_action(data[0]['mass_bands'], adjoint)-adjoint_load)))
                coarse_trial = coarse.lifted @ values
                coarse_test = coarse.lifted @ adjoint
                fine_trial = fine.lifted @ transfer(values)
                fine_test = fine.lifted @ test
                coarse_rows = weights[0]*coarse_trial*coarse_test
                fine_rows = weights[1]*fine_trial*fine_test
                coarse_force = np.asarray(coarse.lifted.T @ (weights[0]*coarse_trial)).ravel()
                fine_force = np.asarray(fine.lifted.T @ (weights[1]*fine_trial)).ravel()
                source = band_action(data[1]['mass_bands'], transfer(solve_banded((2,2), data[0]['mass_bands'], coarse_force, check_finite=False)))-fine_force
                direct = float(test @ source)
                extended_trial = fine.original @ transfer(values)-fine.lifted_hinge*(coarse.jump @ values)
                extended_test = fine.original @ transfer(adjoint)-fine.lifted_hinge*(coarse.jump @ adjoint)
                range_factor = fine.lifted @ (transfer(adjoint)-test)
                trial_jump = float(coarse.jump @ values-fine.jump @ transfer(values))
                test_jump = float(coarse.jump @ adjoint-fine.jump @ transfer(adjoint))
                rows = []
                tag = branch+('_final' if final else '_initial')
                evidence.check(tag+'_mass_adjoint_solve', adjoint_error < 1e-18+1e-10*float(max(abs(adjoint_load))), adjoint_error)
                arrays = dict(coarse_trial=coarse_trial, coarse_test=coarse_test, fine_trial=fine_trial, fine_test=fine_test,
                    coarse_weights=weights[0], fine_weights=weights[1], coarse_rows=coarse_rows, fine_rows=fine_rows,
                    mass_adjoint=adjoint, velocity_test=test, Gram_source=source,
                    extended_trial=extended_trial, extended_test=extended_test, range_factor=range_factor,
                    coarse_source_rows=source_mask(coarse), fine_source_rows=source_mask(fine))
                for partition in ['all_rows', 'source_straddling', 'remaining']:
                    coarse_mask, fine_mask = source_mask(coarse), source_mask(fine)
                    if partition == 'all_rows':
                        coarse_mask, fine_mask = np.ones(len(coarse_rows), dtype=bool), np.ones(len(fine_rows), dtype=bool)
                    elif partition == 'remaining':
                        coarse_mask, fine_mask = ~coarse_mask, ~fine_mask
                    coarse_work, fine_work = float(np.sum(coarse_rows[coarse_mask])), float(np.sum(fine_rows[fine_mask]))
                    weighted = fine_mask*weights[1]
                    operator_weight = coarse_work-float(np.sum(weighted*extended_trial*extended_test))
                    test_range = float(np.sum(weighted*extended_trial*range_factor))
                    test_jump_channel = -test_jump*float(np.sum(weighted*extended_trial*fine.lifted_hinge))
                    trial_jump_channel = -trial_jump*float(np.sum(weighted*fine_test*fine.lifted_hinge))
                    work = coarse_work-fine_work
                    bound = float(np.sum(abs(coarse_rows[coarse_mask]))+np.sum(abs(fine_rows[fine_mask])))
                    cauchy = float(np.sqrt(np.sum(weights[0][coarse_mask]*coarse_trial[coarse_mask]**2)
                        *np.sum(weights[0][coarse_mask]*coarse_test[coarse_mask]**2))
                        +np.sqrt(np.sum(weighted*fine_trial**2)*np.sum(weighted*fine_test**2)))
                    scale = abs(operator_weight)+abs(test_range)+abs(test_jump_channel)+abs(trial_jump_channel)
                    telescope_error = abs(work-operator_weight-test_range-test_jump_channel-trial_jump_channel)
                    tolerance = 2e-9*max(scale, abs(work), 1e-12)+1e-20
                    evidence.check(tag+'_'+partition+'_weak_telescope_and_bounds', telescope_error <= tolerance
                        and abs(work) <= bound+1e-23 and abs(work) <= cauchy+1e-23,
                        dict(error=telescope_error, tolerance=tolerance))
                    rows.append(dict(partition=partition, coarse_rows=int(sum(coarse_mask)), fine_rows=int(sum(fine_mask)),
                        coarse_work=coarse_work, fine_work=fine_work, weak_work=work, row_absolute_bound=bound,
                        partition_Cauchy_bound=cauchy, operator_weight=operator_weight, test_range=test_range,
                        test_jump=test_jump_channel, trial_jump=trial_jump_channel,
                        telescope_error=telescope_error, numerical_tolerance=tolerance, valid_for_claim=False))
                weak = rows[0]['weak_work']
                evidence.check(tag+'_weak_identity_matches_direct_load', abs(weak-direct) < 2e-9*max(abs(weak),abs(direct),1e-12)+1e-20,
                    dict(error=abs(weak-direct)))
                if final:
                    old = next(row for row in previous['annular-live-wave-error-energy-attempt01']['cases']
                        if row['branch'] == branch and row['tangent_step'] == 2.5e-8)
                    evidence.check(tag+'_matches_saved_Gram_work', abs(weak-old['Gram_stiffness_transfer']) < 1e-20)
                norms = []
                for name, model, weight, field in [('coarse_trial', coarse, weights[0], values),
                        ('coarse_test', coarse, weights[0], adjoint), ('fine_trial', fine, weights[1], transfer(values)),
                        ('fine_test', fine, weights[1], test)]:
                    result = norm_bounds(model, weight, field)
                    evidence.check(tag+'_'+name+'_uniform_template_and_both_norm_bounds',
                        result['template_row_bound'] <= TEMPLATE_BOUND and result['Gram_norm'] <= result['discrete_third_difference_bound']+1e-19
                        and result['Gram_norm'] <= result['lifted_H1_bound']+1e-19)
                    norms.append(dict(field=name, **result))
                mixed_bound = (norms[0]['discrete_third_difference_bound']*norms[1]['lifted_H1_bound']
                    +norms[2]['discrete_third_difference_bound']*norms[3]['lifted_H1_bound'])
                discrete_bound = (norms[0]['discrete_third_difference_bound']*norms[1]['discrete_third_difference_bound']
                    +norms[2]['discrete_third_difference_bound']*norms[3]['discrete_third_difference_bound'])
                evidence.check(tag+'_refinement_explicit_work_bounds', abs(weak) <= mixed_bound+1e-20 and abs(weak) <= discrete_bound+1e-20)
                evidence.report['cases'].append(dict(branch=branch, time=4e-5 if final else 0., rows=rows, norms=norms,
                    direct_load_work=direct, trial_jump_defect=trial_jump, test_jump_defect=test_jump,
                    adjoint_residual_error=adjoint_error, discrete_third_work_bound=discrete_bound,
                    mixed_third_H1_work_bound=mixed_bound, valid_for_claim=False))
                path = evidence.output/(tag+'-weak-Gram.npz')
                np.savez_compressed(path, **arrays)
                evidence.own(path, 'outputs')
                evidence.save()
                print(json.dumps(dict(case=tag, total=rows[0], source=rows[1], norms=norms,
                    mixed_bound=mixed_bound, discrete_bound=discrete_bound)), flush=True)
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
