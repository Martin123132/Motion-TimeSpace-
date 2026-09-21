from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_weak_Gram_transfer_20260919 import adjoint_test, source_mask, TEMPLATE_BOUND
from annular_compatible_current_restoring_20260909 import unit_gram_template
from annular_wave_error_energy_20260919 import stiffness_weights
from annular_P2_indexed_live_geometry_20260919 import IndexedGradedP2System
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
import contextlib
import json
import numpy as np


def derivative_atoms(model, values, removed_jump):
    indices = model.element_indices
    nodes = values[np.maximum(indices, 0)]*(indices >= 0)
    lengths = np.diff(model.edges)
    first = nodes @ np.array([-3., 4., -1.])/lengths
    last = nodes @ np.array([1., -4., 3.])/lengths
    curvature = nodes @ np.array([4., -8., 4.])/lengths**2
    gradient_atoms = first[1:]-last[:-1]
    source_index = int(np.searchsorted(model.edges, model.anchor))-1
    gradient_atoms[source_index] -= removed_jump
    return dict(locations=model.edges[1:-1], gradient=gradient_atoms, curvature=np.diff(curvature),
        total_gradient_jump=float(np.sum(abs(gradient_atoms))), total_curvature_jump=float(np.sum(abs(np.diff(curvature)))))


def factor_bound(model, weights, sampled, fixed_jump, atoms):
    hinge = np.maximum(model.radii-model.anchor, 0.)
    detrended = sampled-fixed_jump*hinge
    direct = model.original @ sampled-model.lifted_hinge*fixed_jump
    base = detrended[np.searchsorted(model.radii, model.base_radii)]
    third = np.diff(base, n=3)
    margins, adjacent, extras = unit_gram_template(model.base_count)
    components = [np.sqrt(margins)*third, np.sqrt(abs(adjacent))*(third[:-1]+np.sign(adjacent)*third[1:]),
        np.array([np.sqrt(abs(weight))*(third[first]+np.sign(weight)*third[second]) for first, second, weight in extras])]
    reconstructed = np.concatenate(components) if len(weights) else np.zeros(0)
    arithmetic = float(np.sqrt(np.sum(weights*(direct-reconstructed)**2)))
    spacing = model.gram_spacing
    coefficient = float(np.max(weights*spacing, initial=0.))
    atom_bound = (np.sqrt(2*spacing)*atoms['total_gradient_jump']
        +np.sqrt(3*spacing**3)*atoms['total_curvature_jump'])
    third_bound = float(np.sqrt(TEMPLATE_BOUND*coefficient/spacing)*np.linalg.norm(third)+arithmetic)
    piecewise_bound = float(np.sqrt(TEMPLATE_BOUND*coefficient)*atom_bound+arithmetic)
    return dict(Gram_norm=float(np.sqrt(np.sum(weights*direct**2))), third_difference_bound=third_bound,
        fixed_P2_atom_bound=piecewise_bound, measured_third_seminorm=float(np.linalg.norm(third)/spacing**2.5),
        total_gradient_jump=atoms['total_gradient_jump'], total_curvature_jump=atoms['total_curvature_jump'],
        floating_factor_correction=arithmetic, coefficient_max=coefficient), direct


def main():
    evidence = EvidenceRun('annular-frozen-Gram-refinement-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, frozen_actual_coarse_geometry=True, frozen_actual_coarse_trial_and_adjoint=True,
            fixed_original_source_jump_not_refitted_on_new_grid=True, bulk_refinement_not_a_new_trajectory=True,
            fixed_P2_consistency_not_uniform_evolving_family_convergence=True, no_fitted_couplings=True)
        evidence.report['controls'] = []
        for phase in [.13, .41, .79]:
            spacing = .03125
            nodes = spacing*np.arange(-4, 6)
            hinge = np.maximum(nodes-phase*spacing, 0.)
            first = np.diff(hinge, n=3)
            second = np.diff(.5*hinge**2, n=3)
            first_norm = float(np.linalg.norm(first)/np.sqrt(spacing))
            second_norm = float(np.linalg.norm(second)/np.sqrt(spacing))
            evidence.check(str(phase)+'_linear_hinge_third_difference_bound', first_norm <= np.sqrt(2*spacing)+1e-14)
            evidence.check(str(phase)+'_quadratic_hinge_third_difference_bound', second_norm <= np.sqrt(3*spacing**3)+1e-14)
            evidence.report['controls'].append(dict(phase=phase, first_norm=first_norm, first_bound=float(np.sqrt(2*spacing)),
                second_norm=second_norm, second_bound=float(np.sqrt(3*spacing**3)), valid_for_claim=False))
        path = evidence.output.parent/'annular-live-weak-Gram-transfer-attempt01/status.json'
        previous = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('actual_weak_pairing_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        for branch in ['reference', 'MTS']:
            states = state_pair(evidence, branch, True)
            coarse_system = IndexedGradedP2System(257, branch == 'MTS', 2e-5)
            fine_system = IndexedGradedP2System(513, branch == 'MTS', 1e-5)
            center = int(np.argmin(abs(coarse_system.labels)))
            coarse_rates, geometry = coarse_system.solve(*states[0])
            fine_rates, fine_geometry = fine_system.solve(*states[1])
            coarse = coarse_system.layer(coarse_system.labels[center], geometry)
            fine = fine_system.layer(fine_system.labels[center], fine_geometry)
            coarse_data = coarse.evaluate(0., states[0][0, center], coarse_rates[center])
            fine_data = fine.evaluate(0., states[1][0, center], fine_rates[center])
            indices, shape, unused = coarse.features_quadratic(fine.radii)
            test = fine_rates[center, :-1]-np.sum(shape*coarse_rates[center, :-1][indices], axis=1)
            adjoint, unused = adjoint_test(coarse_data['mass_bands'], fine_data['mass_bands'], test, indices, shape, coarse.count)
            fields = dict(trial=states[0][0, center, :-1], test=adjoint)
            jumps = {name:float(coarse.jump @ field) for name, field in fields.items()}
            atoms = {name:derivative_atoms(coarse, field, jumps[name]) for name, field in fields.items()}
            old = next(case for case in previous['cases'] if case['branch'] == branch and case['time'] == 4e-5)
            last_work = None
            for count in [257, 513, 1025, 2049]:
                system = coarse_system if count == 257 else IndexedGradedP2System(count, branch == 'MTS', 2e-5)
                layer = system.layer(coarse_system.labels[center], geometry)
                weights = stiffness_weights(layer, states[0][0, center, -1])['gram']
                indices, shape, unused = coarse.features_quadratic(layer.radii)
                sampled = {name:np.sum(shape*field[indices], axis=1) for name, field in fields.items()}
                results, factors = {}, {}
                for name in fields:
                    results[name], factors[name] = factor_bound(layer, weights, sampled[name], jumps[name], atoms[name])
                    value = results[name]
                    evidence.check(branch+'_'+str(count)+'_'+name+'_both_refinement_bounds',
                        value['Gram_norm'] <= value['third_difference_bound']+1e-15
                        and value['Gram_norm'] <= value['fixed_P2_atom_bound']+1e-15)
                row_work = weights*factors['trial']*factors['test']
                work = float(np.sum(row_work))
                source = source_mask(layer)
                atom_bound = results['trial']['fixed_P2_atom_bound']*results['test']['fixed_P2_atom_bound']
                third_bound = results['trial']['third_difference_bound']*results['test']['third_difference_bound']
                evidence.check(branch+'_'+str(count)+'_frozen_work_bounds', abs(work) <= atom_bound+1e-20 and abs(work) <= third_bound+1e-20)
                if count == 257:
                    evidence.check(branch+'_original_frozen_grid_matches_actual_work', abs(work-old['rows'][0]['coarse_work']) < 1e-18)
                row = dict(branch=branch, base_count=count, spacing=layer.gram_spacing, source_cap=2e-5, work=work,
                    source_work=float(np.sum(row_work[source])), remaining_work=float(np.sum(row_work[~source])),
                    row_absolute_bound=float(np.sum(abs(row_work))), fixed_P2_atom_work_bound=atom_bound,
                    discrete_third_work_bound=third_bound,
                    magnitude_ratio=abs(work/last_work) if last_work not in [None, 0.] else None,
                    observed_power=float(np.log2(abs(last_work/work))) if last_work not in [None, 0.] and work != 0. else None,
                    norms=results, valid_for_claim=False)
                evidence.report['cases'].append(row)
                path = evidence.output/(branch+'-bulk'+str(count)+'-frozen.npz')
                np.savez_compressed(path, weights=weights, trial=factors['trial'], test=factors['test'], row_work=row_work,
                    source_rows=source, trial_gradient_atoms=atoms['trial']['gradient'], trial_curvature_atoms=atoms['trial']['curvature'],
                    test_gradient_atoms=atoms['test']['gradient'], test_curvature_atoms=atoms['test']['curvature'])
                evidence.own(path, 'outputs')
                evidence.save()
                print(json.dumps({key:value for key,value in row.items() if key != 'norms'}), flush=True)
                last_work = work
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
