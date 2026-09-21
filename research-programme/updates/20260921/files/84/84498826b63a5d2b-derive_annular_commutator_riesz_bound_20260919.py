from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_v2_20260919 import DecimalAction, DecimalMap, decimal_array
from derive_annular_transfer_kernel_and_common_overlay_20260919 import owned_json
from annular_P2_graded_source_20260919 import GradedSourceAction
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from scipy.linalg import cho_factor, cho_solve
from scipy.sparse import csr_matrix
from time import perf_counter
import contextlib
import json
import numpy as np


def refined_stiffness_solve(action, right_side):
    dense = np.zeros((action.count, action.count))
    dense[action.rows, action.columns] = np.asarray(action.values, dtype=float)
    scale = np.sqrt(np.diag(dense))
    factor = cho_factor(dense/scale[:, None]/scale[None, :], lower=True, check_finite=False)
    answer = np.full(right_side.shape, Decimal(0), dtype=object)
    denominator = max(Decimal(1), max(map(abs, right_side.flat)))
    history = []
    for iteration in range(80):
        residual = right_side-action.stiffness(answer)
        relative = max(map(abs, residual.flat))/denominator
        history.append(str(relative))
        if relative < Decimal('1e-42'):
            return answer, residual, history
        correction = cho_solve(factor, np.asarray(residual, dtype=float)/scale[:, None], check_finite=False)/scale[:, None]
        if not np.all(np.isfinite(correction)):
            raise RuntimeError('Nonfinite mixed-precision correction.')
        answer += decimal_array(correction)
    raise RuntimeError('High-precision stiffness residual failed refinement: '+history[-1])


def transpose_lower(action, values):
    answer = values.copy()
    for offset in [1, 2]:
        answer[:-offset] += action.lower[offset:, offset-1, None]*values[offset:]
    return answer


def mass_apply(action, values):
    result = action.bands[2, :, None]*values
    for offset in [1, 2]:
        result[offset:] += action.bands[2+offset, :-offset, None]*values[:-offset]
        result[:-offset] += action.bands[2+offset, :-offset, None]*values[offset:]
    return result


def main():
    evidence = EvidenceRun('annular-commutator-riesz-bound-attempt01', __file__)
    started = perf_counter()
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False,
            original_action_unchanged=True, original_nonnested_transfer_retained_for_this_bound=True,
            no_projected_mass_inverse=True, residual_terms_included=True,
            interval_arithmetic_certificate=False, uniform_continuum_bound=False)
        evidence.report['groups'], evidence.report['solves'] = [], []
        source_path = evidence.output.parent/'annular-transfer-kernel-overlay-attempt01/status.json'
        source = json.loads(source_path.read_text())
        evidence.own(source_path)
        evidence.check('rank_safe_overlay_complete', source['state'] == 'complete'
            and source['common_overlay_injectivity_proven'] and all(row['passed'] for row in source['checks']))
        with localcontext() as ctx:
            ctx.prec = 64
            for branch in ['reference', 'MTS']:
                data = checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-coarse-action.npz')
                action = DecimalAction(data)
                initial = checked_load(evidence, 'annular-moving-duhamel-trajectory-attempt01', branch+'-point032.npz')
                phase = decimal_array(np.stack([initial['0_position'], -initial['0_reverse_velocity']]))
                local = owned_json(evidence, 'annular-transfer-kernel-overlay-attempt01', branch+'-coarse-commutator-rows.json')
                original = np.array(local['dual_difference'], dtype=object)
                dual = np.array([Decimal(value) for value in original.flat], dtype=object).reshape(original.shape)
                position_representer, stiffness_residual, history = refined_stiffness_solve(action, dual[0])
                velocity_representer = action.solve(dual[1])
                mass_residual = dual[1]-mass_apply(action, velocity_representer)
                evidence.check(branch+'_stiffness_refinement_residual', Decimal(history[-1]) < Decimal('1e-42'), history)
                evidence.report['solves'].append(dict(branch=branch, correction_steps=len(history)-1,
                    relative_stiffness_residual=history[-1], residual_history=history,
                    maximum_mass_residual=str(max(map(abs, mass_residual.flat))), valid_for_claim=False))
                model = GradedSourceAction(257, branch == 'MTS', source_cap=2e-5)
                blocks = []
                for name in ['gradient', 'gram']:
                    matrix = csr_matrix((data[name+'_data'], data[name+'_indices'], data[name+'_indptr']),
                        shape=tuple(data[name+'_shape']))
                    mapping = DecimalMap(matrix)
                    vectors = np.column_stack([position_representer, phase[0]])
                    transformed = mapping.apply(vectors)
                    weights = decimal_array(data[name+'_weights'])
                    if name == 'gradient':
                        selected = abs(model.reference_radius-model.anchor) <= .001
                        label = 'within_reference_radius_0.001'
                    else:
                        original_support = abs(model.original)
                        selected = ((np.asarray(original_support @ (model.radii < model.anchor)).ravel() > 0)
                            & (np.asarray(original_support @ (model.radii > model.anchor)).ravel() > 0))
                        label = 'original_rows_straddling_source'
                    blocks.append((name, weights, transformed, selected, label))
                transformed = transpose_lower(action, np.column_stack([velocity_representer, phase[1]]))
                blocks.append(('kinetic', action.diagonal, transformed, abs(model.radii-model.anchor) <= .001,
                    'within_reference_radius_0.001'))
                for column, comparison in enumerate(['spatial32', 'spatial64']):
                    signed = Decimal(0)
                    dual_norm_squared, initial_norm_squared = Decimal(0), Decimal(0)
                    partition_bound = Decimal(0)
                    for name, weights, transformed, selected, label in blocks:
                        values = weights*transformed[:, column]*transformed[:, -1]
                        dual_squared = weights*transformed[:, column]**2
                        initial_squared = weights*transformed[:, -1]**2
                        signed += sum(values, Decimal(0))
                        dual_norm_squared += sum(dual_squared, Decimal(0))
                        initial_norm_squared += sum(initial_squared, Decimal(0))
                        for region, mask in [('source_selected', selected), ('remaining', ~selected)]:
                            value = sum(values[mask], Decimal(0))
                            first = sum(dual_squared[mask], Decimal(0))
                            last = sum(initial_squared[mask], Decimal(0))
                            bound = (first*last).sqrt()
                            partition_bound += bound
                            evidence.check(branch+'_'+comparison+'_'+name+'_'+region+'_weighted_Cauchy',
                                abs(value) <= bound+Decimal('1e-50'))
                            evidence.report['groups'].append(dict(branch=branch, comparison=comparison,
                                factor=name, region=region, partition_definition=label, rows=int(sum(mask)),
                                signed_value=str(value), Cauchy_bound=str(bound), dual_factor_norm_squared=str(first),
                                initial_factor_norm_squared=str(last), valid_for_claim=False))
                    residual = sum(stiffness_residual[:, column]*phase[0]+mass_residual[:, column]*phase[1], Decimal(0))
                    residual_bound = sum(abs(stiffness_residual[:, column]*phase[0])+abs(mass_residual[:, column]*phase[1]), Decimal(0))
                    reconstructed = signed+residual
                    expected = Decimal(next(row['frozen_operator_commutator'] for row in source['cases']
                        if row['branch'] == branch and row['comparison'] == comparison))
                    tolerance = Decimal('2e-10')*max(abs(expected), abs(reconstructed), Decimal('1e-9'))+Decimal('3e-16')
                    error = abs(reconstructed-expected)
                    evidence.check(branch+'_'+comparison+'_full_factored_force_reconstruction', error <= tolerance,
                        dict(error=str(error), unchanged_tolerance=str(tolerance)))
                    energy_bound = (dual_norm_squared*initial_norm_squared).sqrt()+residual_bound
                    bound = partition_bound+residual_bound
                    evidence.check(branch+'_'+comparison+'_residual_inclusive_force_bounds', abs(expected) <= bound
                        and bound <= energy_bound+Decimal('1e-45'))
                    old_bound = Decimal(next(row['finite_input_triangle_bound'] for row in source['cases']
                        if row['branch'] == branch and row['comparison'] == comparison))
                    evidence.report['cases'].append(dict(branch=branch, comparison=comparison,
                        original_commutator=str(expected), reconstructed=str(reconstructed), reconstruction_error=str(error),
                        unchanged_numerical_tolerance=str(tolerance), residual_pairing=str(residual), residual_absolute_bound=str(residual_bound),
                        action_energy_bound=str(energy_bound), partitioned_action_bound=str(bound), nodal_absolute_bound=str(old_bound),
                        improvement_over_nodal_bound=str(old_bound/bound), bound_to_signed_ratio=str(bound/abs(expected)),
                        certified_continuum_bound=False, valid_for_claim=False))
                output = evidence.output/(branch+'-riesz-representers.json')
                output.write_text(json.dumps(dict(position=position_representer.tolist(), velocity=velocity_representer.tolist(),
                    stiffness_residual=stiffness_residual.tolist(), mass_residual=mass_residual.tolist()), default=str)+'\n', encoding='utf-8')
                evidence.own(output, 'outputs')
                evidence.report['progress'] = dict(branch=branch, seconds=perf_counter()-started)
                evidence.save()
                print(json.dumps(evidence.report['progress']), flush=True)
        evidence.report['seconds'] = perf_counter()-started
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
