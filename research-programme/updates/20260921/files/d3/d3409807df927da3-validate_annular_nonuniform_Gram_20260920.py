from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_nonuniform_Gram_candidate_20260920 import gram_action, divided_rows, template_rows
from annular_moving_collar_sparse_20260914 import sparse_factors
from decimal import Decimal
from fractions import Fraction
from scipy.sparse import diags
from time import perf_counter
import contextlib
import json
import numpy as np


TEMPLATE_BOUND = float(Fraction(59097, 573104)+2*Fraction(3, 392)+Fraction(1, 392))


def main():
    evidence = EvidenceRun('annular-nonuniform-Gram-controls-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            original_live_action_unchanged=True, candidate_only=True, nonuniform_parent_uniqueness_proven=False,
            physical_force_mismatch_fixed=False, full_live_P2_force_convergence_proven=False,
            certified_continuous_time_bound=False, variation_qualified=False, uniform_recovery_qualified=False)
        evidence.report['uniform'], evidence.report['variations'], evidence.report['refinements'] = [], [], []
        evidence.own(evidence.root/'DERIVATION-20260919-weak-Gram-consistency-and-fixed-field-bound.md')
        for nodes in [[Fraction(index, 4) for index in range(4)],
                [Fraction(0), Fraction(1, 7), Fraction(2, 5), Fraction(1)]]:
            width = (nodes[-1]-nodes[0])/3
            weights = [6*width**3/np.prod([nodes[index]-nodes[other] for other in range(4) if other != index])
                for index in range(4)]
            for power in range(4):
                actual = sum((weight*node**power for weight, node in zip(weights, nodes)), Fraction(0))
                expected = 6*width**3 if power == 3 else Fraction(0)
                evidence.check('exact_rational_'+str(nodes[1])+'_moment_'+str(power), actual == expected)
            if nodes[1] == Fraction(1, 4):
                evidence.check('exact_uniform_normalized_third_difference', weights == [-1, 3, -3, 1])
        for count in [17, 33, 65, 257]:
            knots = np.linspace(5.2, 6.8, count)
            spacing = knots[1]-knots[0]
            values = .2*np.sin(1.3*np.arange(count))+.1*np.cos(.7*np.arange(count))
            coefficient = 1+.1*np.sin(knots)
            anchor, jump = 6.03, .17
            result = gram_action(knots, values, jump, anchor, coefficient)
            original, sampling = sparse_factors(count, True)
            original, sampling = original[count-1:], sampling[count-1:]
            hinge = np.maximum(knots-anchor, 0.)
            old_factor = original @ (values-jump*hinge)
            expected_energy = np.dot(sampling @ coefficient, old_factor**2)/(2*spacing)
            factor_error = float(np.max(abs((result['operator']*np.sqrt(spacing)-original).toarray()))/
                np.max(abs(original.data)))
            energy_error = float(abs(result['energy']-expected_energy)/max(1., abs(expected_energy)))
            evidence.check('uniform_'+str(count)+'_original_rule', max(factor_error, energy_error) < 3e-11,
                dict(factor_error=factor_error, energy_error=energy_error))
            evidence.check('uniform_'+str(count)+'_original_coefficient_sampling', (result['sampling']-sampling).nnz == 0)
            evidence.report['uniform'].append(dict(count=count, factor_relative_error=factor_error,
                energy_relative_error=energy_error, candidate_energy=float(result['energy']),
                original_energy=float(expected_energy), ideal_uniform_identity_exact=True, valid_for_claim=False))
        count = 33
        gaps = .8+.2*np.sin(np.arange(count-1)*1.3)
        knots = 5.2+1.6*np.concatenate([[0.], np.cumsum(gaps)])/sum(gaps)
        anchor, jump = 6.03, .17
        values = .2*np.sin(np.arange(count)*.73)+.1*np.cos(np.arange(count)*1.2)
        coefficient = 1+.1*np.cos(knots)
        direction = dict(knots=.01*np.sin(np.arange(count)*.39),
            values=.03*np.cos(np.arange(count)*.27), coefficient=.13*np.sin(np.arange(count)*.61),
            jump=.04, anchor=.017)
        baseline = gram_action(knots, values, jump, anchor, coefficient, direction)
        step = 1e-25
        moved = gram_action(knots+1j*step*direction['knots'], values+1j*step*direction['values'],
            jump+1j*step*direction['jump'], anchor+1j*step*direction['anchor'],
            coefficient+1j*step*direction['coefficient'])
        exact_direction = moved['energy'].imag/step
        error = abs(baseline['variation']-exact_direction)/max(1., abs(exact_direction))
        evidence.check('independent_complex_step_full_variation', error < 3e-11, float(error))
        for label in ['stencil_variation', 'coefficient_variation', 'trace_and_field_variation']:
            omitted_error = abs((baseline['variation']-baseline[label])-exact_direction)
            evidence.check('reject_omitted_'+label, omitted_error > 1e-8*max(1., abs(exact_direction)), float(omitted_error))
            evidence.report['variations'].append(dict(term=label, analytic=float(baseline[label]),
                omitted_error=float(omitted_error), full_variation=float(baseline['variation']),
                independent_variation=float(exact_direction), valid_for_claim=False))
        scaled = gram_action(anchor+2.3*(knots-anchor), values, jump/2.3, anchor, coefficient)
        evidence.check('inverse_length_energy_scaling', abs(2.3*scaled['energy']-baseline['energy']) < 3e-11*max(1., baseline['energy']))
        kernel, unused, widths = divided_rows(knots)
        for power in range(3):
            residual = kernel @ (knots-anchor)**power
            evidence.check('nonuniform_polynomial_'+str(power)+'_annihilated', np.max(abs(residual)) < 3e-10)
        hinge_values = .4*(knots-anchor)+.7*np.maximum(knots-anchor, 0.)
        hinge_result = gram_action(knots, hinge_values, .7, anchor, coefficient)
        evidence.check('compensated_linear_hinge_zero', hinge_result['energy'] < 1e-23, float(hinge_result['energy']))
        source_cell = np.searchsorted(knots, anchor)-1
        jump_row = np.zeros(count)
        jump_row[source_cell] = 1/(anchor-knots[source_cell])
        jump_row[source_cell+1] = 1/(knots[source_cell+1]-anchor)
        hinge = np.maximum(knots-anchor, 0.)
        field_map = np.eye(count)-np.outer(hinge, jump_row)
        lifted = baseline['operator'] @ field_map
        stiffness = lifted.T @ (baseline['row_weight'][:, None]*lifted)
        eigenvalues = np.linalg.eigvalsh(stiffness)
        evidence.check('positive_semidefinite_full_hessian', eigenvalues[0] >= -1e-12*eigenvalues[-1],
            dict(minimum=float(eigenvalues[0]), maximum=float(eigenvalues[-1])))
        field_jump = jump_row @ values
        field = gram_action(knots, values, field_jump, anchor, coefficient)
        predicted_covector = field['values_covector']+jump_row*field['jump_covector']
        field_moved = gram_action(knots, values+1j*step*direction['values'],
            field_jump+1j*step*(jump_row @ direction['values']), anchor, coefficient)
        field_error = abs(-predicted_covector @ direction['values']-field_moved['energy'].imag/step)
        evidence.check('source_trace_chain_rule_covector', field_error < 3e-11*max(1., abs(field_moved['energy'].imag/step)), float(field_error))
        reference = gram_action(knots, values, jump, anchor, coefficient, direction, include_gram=False)
        evidence.check('reference_identically_zero_energy_and_variation', reference['energy'] == 0 and reference['variation'] == 0
            and np.all(reference['values_covector'] == 0))
        template, sampling = template_rows(count)
        differences = np.diff(knots)
        windows = np.stack([differences[offset:count-3+offset] for offset in range(3)], axis=1)
        variance = np.sum((windows-widths[:, None])**2, axis=1)/np.sum(windows**2, axis=1)
        alternative = template @ diags(1+variance) @ kernel
        alternate_factor = alternative @ (values-jump*hinge)
        alternate_energy = float(np.dot(sampling @ coefficient, alternate_factor**2)/2)
        evidence.check('positive_nonuniform_extension_not_unique', abs(alternate_energy-baseline['energy']) > 1e-5*baseline['energy'])
        evidence.report['nonuniqueness'] = dict(primary_energy=float(baseline['energy']), alternative_energy=alternate_energy,
            alternative='multiply each divided-difference row by 1+local_gap_variance_over_square_sum',
            same_ideal_uniform_rule=True, both_positive=True, witness_not_a_fitted_physics_parameter=True, valid_for_claim=False)
        for count in [17, 33, 65, 129]:
            parameter = np.linspace(0., 1., count)
            knots = 5.2+1.6*(parameter+np.sin(2*np.pi*parameter)/(8*np.pi))
            coefficient = 1+.1*np.cos(knots)
            gap = np.diff(knots)
            maximum_gap = float(np.max(gap))
            windows = np.stack([gap[offset:count-3+offset] for offset in range(3)], axis=1)
            ratio = float(np.max(np.max(windows, axis=1)/np.min(windows, axis=1)))
            for profile in ['smooth', 'piecewise_quadratic']:
                if profile == 'smooth':
                    values = np.sin(2*(knots-5.2))+.17*np.maximum(knots-anchor, 0.)
                    bound = TEMPLATE_BOUND*np.max(coefficient)*1.6*maximum_gap**4*8**2/2
                else:
                    values = .02*(knots-anchor)**2+.3*np.maximum(knots-5.81, 0.)+.2*np.maximum(knots-6.23, 0.)**2/2
                    values += .17*np.maximum(knots-anchor, 0.)
                    bound = TEMPLATE_BOUND*np.max(coefficient)*3*ratio**6*(24*np.sqrt(maximum_gap)*.3
                        +36*maximum_gap**1.5*.2)**2/2
                result = gram_action(knots, values, .17, anchor, coefficient)
                evidence.check(profile+'_'+str(count)+'_derived_fixed_field_bound', 0 <= result['energy'] <= bound)
                evidence.report['refinements'].append(dict(profile=profile, count=count, maximum_gap=maximum_gap,
                    local_gap_ratio=ratio, energy=float(result['energy']), derived_energy_bound=float(bound),
                    fixed_field_not_live_solution=True, valid_for_claim=False))
        for label, invalid_knots in [('duplicate', np.array([0.]*17)), ('nonfinite', np.append(np.arange(16), np.nan))]:
            try:
                divided_rows(invalid_knots)
            except ValueError:
                caught = True
            else:
                caught = False
            evidence.check('reject_'+label+'_knots', caught)
        evidence.report.update(variation_qualified=True, uniform_recovery_qualified=True,
            seconds=perf_counter()-started)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), seconds=perf_counter()-started)), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()

