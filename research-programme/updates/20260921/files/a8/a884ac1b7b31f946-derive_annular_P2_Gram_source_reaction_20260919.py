from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_graded_source_20260919 import GradedSourceAction
from run_annular_P2_continuum_bridge_20260918 import checked_load
from scipy.linalg import solve_banded
import contextlib
import json
import numpy as np
import sympy as symbolic


def graded_trace_coefficient(lengths):
    lengths = np.asarray(lengths)
    tail = lengths[-1]/8
    for vertex in range(len(lengths)-1, 0, -1):
        tail = (lengths[vertex-1]+lengths[vertex])/8-(lengths[vertex]/24)**2/tail
    neighbour = lengths[0]/(24*tail)
    return float((7+3*neighbour)/2)


def constant_projection(model):
    bands = np.zeros((5, model.count))
    right_side = np.zeros(model.count)
    local_mass = np.array([[4., 2., -1.], [2., 16., 2.], [-1., 2., 4.]])/30
    integral = np.array([1., 4., 1.])/6
    for indices, length in zip(model.element_indices, np.diff(model.edges)):
        for first in range(3):
            row = indices[first]
            if row >= 0:
                right_side[row] -= length*integral[first]
                for second in range(3):
                    column = indices[second]
                    if column >= 0:
                        bands[2+row-column, column] += length*local_mass[first, second]
    return solve_banded((2, 2), bands, right_side, check_finite=False)


def main():
    evidence = EvidenceRun('annular-P2-Gram-source-reaction-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, no_new_evolution=True,
            no_new_fitted_coupling=True, no_Gram_terms_removed=True,
            rank_one_identity_not_closed_reaction_dynamics=True,
            constant_weight_trace_prediction_not_exact_live_theorem=True)
        decay = 3-2*symbolic.sqrt(2)
        coefficient = (7+3*decay)/2
        evidence.check('uniform_mass_projection_decay_root', symbolic.simplify(decay**2-6*decay+1) == 0)
        evidence.check('uniform_source_projection_trace_constant', symbolic.simplify(coefficient-(8-3*symbolic.sqrt(2))) == 0)
        fixtures = []
        for count in [65, 129, 257, 513]:
            for cap in [2e-5, 1e-5]:
                model = GradedSourceAction(count, True, source_cap=cap)
                source = int(np.searchsorted(model.edges, model.anchor))
                lengths = np.diff(model.edges)
                left, right = lengths[:source][::-1], lengths[source:]
                left_coefficient, right_coefficient = graded_trace_coefficient(left), graded_trace_coefficient(right)
                predicted = -left_coefficient/left[0]-right_coefficient/right[0]
                actual = float(model.jump @ constant_projection(model))
                key = str(count)+'_'+str(cap)
                evidence.check(key+'_graded_trace_bracket', 3.5 < left_coefficient <= 4 and 3.5 < right_coefficient <= 4)
                evidence.check(key+'_independent_constant_projection', abs(actual-predicted) < 2e-12*abs(predicted))
                fixtures.append(dict(base_count=count, source_cap=cap, left_trace=left_coefficient,
                    right_trace=right_coefficient, predicted_jump=predicted, actual_jump=actual))
        prior_path = evidence.output.parent/'annular-P2-local-Gram-bound-attempt01/status.json'
        prior = json.loads(prior_path.read_text())
        evidence.own(prior_path)
        evidence.check('localized_bound_checkpoint_complete', prior['state'] == 'complete')
        for count, cap in [(257, 2e-5), (513, 1e-5)]:
            saved = checked_load(evidence, 'annular-P2-local-Gram-bound-attempt01', 'MTS'+str(count)+'-row-data.npz')
            model = GradedSourceAction(count, True, source_cap=cap)
            source_mask = saved['source_rows']
            weights = saved['weights'][source_mask]
            hinge = saved['hinge'][source_mask]
            field = saved['field_factors'][source_mask]
            direction = saved['direction_factors'][source_mask]
            mu = float(weights @ hinge**2)
            multiplier = float(weights @ (hinge*field))
            gamma = float(weights @ (hinge*direction)/mu)
            alpha = multiplier/mu
            field_perpendicular = field-alpha*hinge
            direction_perpendicular = direction-gamma*hinge
            remainder = float(weights @ (field_perpendicular*direction_perpendicular))
            remainder_bound = float(np.sqrt((weights @ field_perpendicular**2)*(weights @ direction_perpendicular**2)))
            source_drive = float(weights @ (field*direction))
            reaction = multiplier*gamma
            values, projection = saved['coordinates'], saved['projection']
            preferred_jump = float(weights @ (hinge*(model.original @ values[:-1])[source_mask])/mu)
            jump = float(model.jump @ values[:-1])
            projected_jump = float(model.jump @ projection)
            projected_original = float(weights @ (hinge*(model.original @ projection)[source_mask])/mu)
            evidence.check(str(count)+'_exact_reaction_split', abs(source_drive-reaction-remainder) < 2e-20)
            evidence.check(str(count)+'_orthogonal_remainder_bound', abs(remainder) <= remainder_bound+2e-20
                and abs(weights @ (hinge*field_perpendicular)) < 2e-20
                and abs(weights @ (hinge*direction_perpendicular)) < 2e-12)
            evidence.check(str(count)+'_jump_defect_identity', abs(alpha-(preferred_jump-jump)) < 2e-13
                and abs(gamma-(projected_original-projected_jump)) < 2e-8)
            source = int(np.searchsorted(model.edges, model.anchor))
            lengths = np.diff(model.edges)
            coefficients = [graded_trace_coefficient(lengths[:source][::-1]), graded_trace_coefficient(lengths[source:])]
            traces = []
            for element, derivative in [(source-1, np.array([1., -4., 3.])), (source, np.array([-3., 4., -1.]))]:
                indices = model.element_indices[element]
                nodal = values[:-1][np.maximum(indices, 0)]*(indices >= 0)
                unused, jacobian, unused2 = model.mapping(np.mean(model.edges[element:element+2]), values[-1])
                traces.append(float(derivative @ nodal/lengths[element]/jacobian))
            predicted_gamma = coefficients[0]*traces[0]/lengths[source-1]+coefficients[1]*traces[1]/lengths[source]
            row = dict(base_count=count, source_cap=cap, mu=mu, multiplier=multiplier, gamma=gamma,
                preferred_jump=preferred_jump, actual_jump=jump, jump_defect=alpha,
                source_projected_drive=source_drive, rank_one_reaction=reaction,
                perpendicular_remainder=remainder, perpendicular_bound=remainder_bound,
                source_projection_jump=projected_jump, original_projection_hinge_coefficient=projected_original,
                constant_weight_trace_prediction=predicted_gamma,
                trace_prediction_relative_difference=abs(predicted_gamma-gamma)/abs(gamma),
                trace_coefficients=coefficients, physical_field_traces=traces,
                prediction_is_diagnostic_not_acceptance_gate=True, valid_for_claim=False)
            evidence.report['cases'].append(row)
            evidence.save()
            print(json.dumps(row), flush=True)
        evidence.report['constant_projection_fixtures'] = fixtures
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
