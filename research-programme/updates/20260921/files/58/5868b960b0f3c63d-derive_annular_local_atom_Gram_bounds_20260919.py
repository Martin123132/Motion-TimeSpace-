from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_frozen_Gram_refinement_20260919 import derivative_atoms
from annular_P2_graded_source_20260919 import GradedSourceAction
from derive_annular_spatial_Gram_defect_split_20260919 import state_pair
import contextlib
import json
import numpy as np


def local_expansion(target, source, field, jump, actual):
    atoms = derivative_atoms(source, field, jump)
    indices = source.element_indices
    nodes = field[np.maximum(indices, 0)]*(indices >= 0)
    lengths = np.diff(source.edges)
    curvature = nodes @ np.array([4.,-8.,4.])/lengths**2
    original = target.original.tocsr()
    gradient, second, polynomial, majorant = [np.zeros(len(actual)) for unused in range(4)]
    for row in range(len(actual)):
        start, stop = original.indptr[row:row+2]
        columns, coefficients = original.indices[start:stop], original.data[start:stop]
        selected = coefficients != 0.
        columns, coefficients = columns[selected], coefficients[selected]
        locations = target.radii[columns]
        lower, upper = float(min(locations)), float(max(locations))
        cell = int(np.clip(np.searchsorted(source.edges, lower, side='right')-1, 0, len(lengths)-1))
        fraction = (lower-source.edges[cell])/lengths[cell]
        shape = np.array([(1-fraction)*(1-2*fraction), 4*fraction*(1-fraction), fraction*(2*fraction-1)])
        radial = np.array([4*fraction-3,4-8*fraction,4*fraction-1])/lengths[cell]
        value = float(shape @ nodes[cell]-jump*max(lower-source.anchor, 0.))
        derivative = float(radial @ nodes[cell]-jump*(lower > source.anchor))
        displacement = locations-lower
        moment_terms = np.array([value*np.sum(coefficients), derivative*(coefficients @ displacement),
            .5*curvature[cell]*(coefficients @ displacement**2)])
        first_atom = np.searchsorted(atoms['locations'], lower, side='right')
        last_atom = np.searchsorted(atoms['locations'], upper, side='left')
        distances = np.maximum(locations[:,None]-atoms['locations'][None,first_atom:last_atom], 0.)
        first_terms = (coefficients @ distances)*atoms['gradient'][first_atom:last_atom]
        second_terms = (.5*coefficients @ distances**2)*atoms['curvature'][first_atom:last_atom]
        gradient[row], second[row], polynomial[row] = np.sum(first_terms), np.sum(second_terms), np.sum(moment_terms)
        majorant[row] = np.sum(abs(first_terms))+np.sum(abs(second_terms))+np.sum(abs(moment_terms))
    residual = actual-gradient-second-polynomial
    return dict(gradient=gradient, curvature=second, polynomial=polynomial, reconstruction_residual=residual,
        atom_majorant=majorant, bound=majorant+abs(residual))


def main():
    evidence = EvidenceRun('annular-local-atom-Gram-bounds-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, full_live_P2_force_convergence_proven=False,
            no_new_evolution=True, actual_coarse_piecewise_fields_retained=True, all_Gram_rows_retained=True,
            polynomial_moments_and_reconstruction_residual_retained=True,
            floating_residual_measured_not_interval_certified=True,
            fixed_field_consistency_not_uniform_evolving_family_convergence=True)
        path = evidence.output.parent/'annular-frozen-Gram-refinement-attempt01/status.json'
        previous = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('frozen_refinement_complete', previous['state'] == 'complete' and all(row['passed'] for row in previous['checks']))
        for branch in ['reference', 'MTS']:
            states = state_pair(evidence, branch, True)
            source = GradedSourceAction(257, branch == 'MTS', source_cap=2e-5)
            path = evidence.output.parent/'annular-live-weak-Gram-transfer-attempt01'/(branch+'_final-weak-Gram.npz')
            evidence.own(path)
            with np.load(path) as stored:
                test = stored['mass_adjoint']
            center = (states[0].shape[1]-1)//2
            fields = dict(trial=states[0][0, center, :-1], test=test)
            for count in [257, 513, 1025, 2049]:
                target = GradedSourceAction(count, branch == 'MTS', source_cap=2e-5)
                path = evidence.output.parent/'annular-frozen-Gram-refinement-attempt01'/(branch+'-bulk'+str(count)+'-frozen.npz')
                evidence.own(path)
                with np.load(path) as stored:
                    data = {name:stored[name] for name in stored.files}
                factors = {name:local_expansion(target, source, field, float(source.jump @ field), data[name]) for name,field in fields.items()}
                for name, result in factors.items():
                    tolerance = 2e-9*np.maximum(result['atom_majorant'], abs(data[name]))+2e-16
                    evidence.check(branch+'_'+str(count)+'_'+name+'_local_atom_reconstruction',
                        np.all(abs(result['reconstruction_residual']) <= tolerance),
                        dict(maximum_error=float(np.max(abs(result['reconstruction_residual']), initial=0.)),
                            maximum_tolerance=float(np.max(tolerance, initial=0.))))
                weighted = data['weights']
                bound = float(np.sum(weighted*factors['trial']['bound']*factors['test']['bound']))
                ideal_bound = float(np.sum(weighted*factors['trial']['atom_majorant']*factors['test']['atom_majorant']))
                work = float(np.sum(data['row_work']))
                evidence.check(branch+'_'+str(count)+'_local_row_bilinear_bound', abs(work) <= bound+1e-24)
                controls = {}
                names = ['gradient', 'curvature', 'polynomial', 'reconstruction_residual']
                for first in names:
                    for second in names:
                        controls[first+'__'+second] = float(np.sum(weighted*factors['trial'][first]*factors['test'][second]))
                error = abs(sum(controls.values())-work)
                evidence.check(branch+'_'+str(count)+'_sixteen_term_bilinear_identity', error < 1e-20)
                row = dict(branch=branch, base_count=count, work=work, local_atom_work_bound=bound,
                    local_atom_bound_without_arithmetic_residual=ideal_bound,
                    arithmetic_bound_allowance=bound-ideal_bound, row_absolute_bound=float(np.sum(abs(data['row_work']))),
                    bound_over_absolute_work=bound/abs(work) if work != 0. else None,
                    bilinear_identity_error=error, **controls, valid_for_claim=False)
                evidence.report['cases'].append(row)
                path = evidence.output/(branch+'-bulk'+str(count)+'-local-atoms.npz')
                np.savez_compressed(path, **{name+'_'+key:value for name,result in factors.items() for key,value in result.items()})
                evidence.own(path, 'outputs')
                evidence.save()
                print(json.dumps({key:value for key,value in row.items() if '__' not in key}), flush=True)
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
