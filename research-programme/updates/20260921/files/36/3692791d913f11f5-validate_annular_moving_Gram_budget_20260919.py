from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_Gram_budget_20260919 import adjoint_rate, variation_rate, pairing_rate
from annular_weak_Gram_transfer_20260919 import adjoint_test
from annular_P2_graded_source_20260919 import GradedSourceAction
from derive_annular_frozen_Gram_refinement_20260919 import derivative_atoms
import contextlib
import json
import numpy as np


def bands(matrix):
    count = len(matrix)
    result = np.zeros((5, count))
    for row in range(count):
        for column in range(max(0, row-2), min(count, row+3)):
            result[2+row-column, column] = matrix[row, column]
    return result


def main():
    evidence = EvidenceRun('annular-moving-Gram-algebra-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            full_live_P2_force_convergence_proven=False, synthetic_controls_not_physical_evidence=True)
        random = np.random.default_rng(6272026)
        coarse_count, fine_count = 7, 11
        indices = random.integers(0, coarse_count, (fine_count, 3))
        shape = random.uniform(.2, 1., indices.shape)
        shape /= shape.sum(axis=1)[:, None]
        transfer = np.zeros((fine_count, coarse_count))
        for row in range(fine_count):
            np.add.at(transfer[row], indices[row], shape[row])
        masses, mass_rates = [], []
        for count in [coarse_count, fine_count]:
            diagonal = random.uniform(2., 3., count)
            off = random.uniform(-.2, .2, count-1)
            mass = np.diag(diagonal)+np.diag(off, 1)+np.diag(off, -1)
            rate = np.diag(random.normal(size=count))
            masses.append(mass)
            mass_rates.append(rate)
        test, test_rate = random.normal(size=(2, fine_count))
        adjoint = np.linalg.solve(masses[0], transfer.T @ masses[1] @ test)
        result = adjoint_rate(*[bands(value) for value in masses+mass_rates], test, test_rate, adjoint, indices, shape)
        expected = np.linalg.solve(masses[0], transfer.T @ (masses[1] @ test_rate+mass_rates[1] @ test)-mass_rates[0] @ adjoint)
        evidence.check('independent_dense_adjoint_derivative', np.max(abs(result['rate']-expected)) < 2e-14)
        for name, channel in result['channels'].items():
            evidence.check(name+'_omission_detected', np.max(abs(result['rate']-channel-expected)) > 1e-3)
        step = 1e-3
        first_masses = [mass-step*rate for mass, rate in zip(masses, mass_rates)]
        last_masses = [mass+step*rate for mass, rate in zip(masses, mass_rates)]
        first_test, last_test = test-step*test_rate, test+step*test_rate
        first, unused = adjoint_test(*map(bands, first_masses), first_test, indices, shape, coarse_count)
        last, unused = adjoint_test(*map(bands, last_masses), last_test, indices, shape, coarse_count)
        centered = adjoint_rate(*map(bands, masses+mass_rates), test, test_rate, (first+last)/2, indices, shape)
        evidence.check('exact_centered_secant_identity', np.max(abs(centered['rate']-(last-first)/(2*step))) < 1e-11)
        evidence.check('base_derivative_not_mislabeled_exact_secant', np.max(abs(result['rate']-(last-first)/(2*step))) > 1e-9)
        atoms, atom_rates = np.array([0., -2., 3.]), np.array([.4, .7, -.8])
        variation = variation_rate(atoms, atom_rates)
        measured = (np.sum(abs(atoms+1e-5*atom_rates))-np.sum(abs(atoms)))/1e-5
        evidence.check('variation_kink_one_sided_derivative', abs(measured-variation['upper_right_rate']) < 1e-9)
        evidence.check('variation_bound_not_signed_growth', variation['upper_right_rate'] < 0. < variation['absolute_rate_budget'])
        model = GradedSourceAction(65, True, source_cap=2e-5)
        values, rates = random.normal(size=(2, model.count))
        first_atoms = derivative_atoms(model, values, float(model.jump @ values))
        rate_atoms = derivative_atoms(model, rates, float(model.jump @ rates))
        last_atoms = derivative_atoms(model, values+.125*rates, float(model.jump @ (values+.125*rates)))
        for name in ['gradient', 'curvature']:
            error = float(np.max(abs(last_atoms[name]-first_atoms[name]-.125*rate_atoms[name])))
            scale = float(max(np.max(abs(last_atoms[name])), 1.))
            evidence.check(name+'_compensated_atoms_linear', error < 2e-12*scale, dict(error=error, scale=scale))
            evidence.check(name+'_finite_segment_variation_bound', np.sum(abs(last_atoms[name])) <=
                np.sum(abs(first_atoms[name]))+.125*np.sum(abs(rate_atoms[name]))+1e-10*scale)
        source_index = int(np.searchsorted(model.edges, model.anchor))-1
        evidence.check('source_atom_compensated_not_deleted_elsewhere',
            abs(first_atoms['gradient'][source_index]) < 1e-7 and len(first_atoms['gradient']) == len(model.edges)-2)
        weights = random.uniform(.3, 2., 19)
        weight_rate, trial, trial_rate, probe, probe_rate = random.normal(size=(5, 19))
        pair = pairing_rate(weights, weight_rate, trial, trial_rate, probe, probe_rate)
        direct = float(weight_rate @ (trial*probe)+weights @ (trial_rate*probe+trial*probe_rate))
        evidence.check('signed_pair_product_rule', abs(direct-pair['rate']) < 2e-14)
        evidence.check('pair_rate_absolute_bound', abs(pair['rate']) <= pair['row_absolute_rate_bound'])
        evidence.report['cases'] = [dict(adjoint_dense_error=float(np.max(abs(result['rate']-expected))),
            secant_error=float(np.max(abs(centered['rate']-(last-first)/(2*step)))),
            variation_right_rate=variation['upper_right_rate'], variation_absolute_budget=variation['absolute_rate_budget'],
            pairing_rate=pair['rate'], pairing_bound=pair['row_absolute_rate_bound'], valid_for_claim=False)]
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
