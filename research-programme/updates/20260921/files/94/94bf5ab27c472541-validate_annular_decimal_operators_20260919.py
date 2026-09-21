from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_v2_20260919 import DecimalAction, DecimalMap, decimal_array, dot
from derive_annular_action_response_time_halving_20260919 import restore_action
from run_annular_P2_continuum_bridge_20260918 import checked_load
from decimal import Decimal, localcontext
from scipy.sparse import csr_matrix
import contextlib
import json
import numpy as np


def main():
    evidence = EvidenceRun('annular-decimal-operators-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False, no_new_evolution=True,
            full_live_P2_force_convergence_proven=False, certified_continuous_time_bound=False)
        path = evidence.output.parent/'annular-decimal-duality-attempt02/status.json'
        previous = json.loads(path.read_text())
        evidence.own(path)
        evidence.check('refined_primal_dual_transport_complete', previous['state'] == 'complete'
            and previous['original_strict_dual_gate_pass'] and all(row['passed'] for row in previous['checks']))
        random = np.random.default_rng(2026091922)
        with localcontext() as ctx:
            ctx.prec = 48
            for branch in ['reference', 'MTS']:
                for level in ['coarse', 'fine']:
                    data = checked_load(evidence, 'annular-action-exponential-response-attempt01', branch+'-'+level+'-action.npz')
                    action, old = DecimalAction(data), restore_action(data)
                    evidence.check(branch+'_'+level+'_positive_action_weights', bool(np.all(data['gradient_weights'] > 0)
                        and np.all(data['gram_weights'] >= 0)))
                    sample = decimal_array(random.normal(size=(action.count, 2)))
                    result = action.stiffness(sample)
                    factored = np.full(sample.shape, Decimal(0), dtype=object)
                    for name in ['gradient', 'gram']:
                        matrix = csr_matrix((data[name+'_data'], data[name+'_indices'], data[name+'_indptr']),
                            shape=tuple(data[name+'_shape']))
                        mapping = DecimalMap(matrix)
                        factored += mapping.apply(decimal_array(data[name+'_weights'])[:, None]*mapping.apply(sample), transpose=True)
                    scale = max(Decimal(1), max(map(abs, factored.flat)))
                    stiffness_error = max(map(abs, (result-factored).flat))/scale
                    evidence.check(branch+'_'+level+'_independent_factored_stiffness', stiffness_error < Decimal('1e-43'), str(stiffness_error))
                    solution = action.solve(sample)
                    reconstructed = action.bands[2, :, None]*solution
                    for offset in [1, 2]:
                        reconstructed[offset:] += action.bands[2+offset, :-offset, None]*solution[:-offset]
                        reconstructed[:-offset] += action.bands[2+offset, :-offset, None]*solution[offset:]
                    residual = max(map(abs, (reconstructed-sample).flat))/max(map(abs, sample.flat))
                    evidence.check(branch+'_'+level+'_original_lower_mass_equation', residual < Decimal('1e-43'), str(residual))
                    left, right = sample[:, 0:1], sample[:, 1:2]
                    primal = dot(left, action.acceleration(right))
                    dual = dot(action.acceleration(left, transpose=True), right)
                    transpose_error = abs(primal-dual)/max(abs(primal), abs(dual), Decimal(1))
                    evidence.check(branch+'_'+level+'_actual_operator_adjoint', transpose_error < Decimal('1e-42'), str(transpose_error))
                    wrong = dot(action.acceleration(left), right)
                    negative_control = abs(primal-wrong)/max(abs(primal), abs(wrong), Decimal(1))
                    evidence.check(branch+'_'+level+'_wrong_transpose_rejected', negative_control > Decimal('1e-8'), str(negative_control))
                    old_solution = old.solve_mass(np.asarray(sample, dtype=float))
                    relative = float(np.max(abs(np.asarray(solution, dtype=float)-old_solution))/max(1., np.max(abs(old_solution))))
                    evidence.check(branch+'_'+level+'_same_original_double_solve', relative < 2e-13, relative)
                    evidence.report['cases'].append(dict(branch=branch, level=level,
                        factored_stiffness_relative_error=str(stiffness_error), mass_relative_residual=str(residual),
                        transpose_relative_error=str(transpose_error), wrong_transpose_relative_error=str(negative_control),
                        original_double_solve_relative_error=relative, unused_upper_triangle_discrepancy=action.unused_upper_triangle_discrepancy,
                        jacobi_ratio=str(action.jacobi_ratio), frequency_scaling_bound=str(action.frequency_bound), valid_for_claim=False))
                    evidence.save()
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), cases=len(evidence.report['cases']))), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
