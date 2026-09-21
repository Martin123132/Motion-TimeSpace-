from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_P2_unresolved_front_Gram_20260919 import front_profile
from derive_annular_P2_Gram_source_reaction_20260919 import graded_trace_coefficient
from annular_moving_collar_sparse_20260914 import sparse_factors
from scipy.linalg import solve_banded
import contextlib
import json
import numpy as np


def evaluate_front(spacing, phase=.6, speed=.77, velocity=.03, forcing=1., time=1., background=.01):
    left_speed, right_speed = speed+velocity, speed-velocity
    fronts = np.array([-left_speed*time, right_speed*time])
    half_count = int(round(32/spacing))
    base = (np.arange(2*half_count+1)-half_count-phase)*spacing
    edge_list = list(base)+[0., *fronts]
    edge_list.extend(np.linspace(base[half_count], 0., 9))
    edge_list.extend(np.linspace(0., base[half_count+1], 9))
    edges = np.unique(edge_list)
    nodes = np.sort(np.concatenate([edges, (edges[:-1]+edges[1:])/2]))
    free = nodes != 0.
    node_map = np.full(len(nodes), -1, dtype=int)
    node_map[free] = np.arange(np.sum(free))
    elements = node_map[np.column_stack([np.arange(0, len(nodes)-2, 2),
        np.arange(1, len(nodes)-1, 2), np.arange(2, len(nodes), 2)])]
    radii, lengths = nodes[free], np.diff(edges)
    source = int(np.searchsorted(edges, 0.))
    jump = np.zeros(len(radii))
    for element, derivative in [(source-1, -np.array([1., -4., 3.])),
            (source, np.array([-3., 4., -1.]))]:
        indices = elements[element]
        selected = indices >= 0
        jump[indices[selected]] += derivative[selected]/lengths[element]
    local_mass = np.array([[4., 2., -1.], [2., 16., 2.], [-1., 2., 4.]])/30
    bands = np.zeros((5, len(radii)))
    right_side = np.zeros(len(radii))
    constant_side = np.zeros(len(radii))
    for element, (indices, length) in enumerate(zip(elements, lengths)):
        positions = np.array([edges[element], np.mean(edges[element:element+2]), edges[element+1]])
        midpoint = positions[1]
        if fronts[0] < midpoint < 0:
            derivative = background-forcing*(time+positions/left_speed)/left_speed
        elif 0 < midpoint < fronts[1]:
            derivative = background+forcing*(time-positions/right_speed)/right_speed
        else:
            derivative = np.full(3, background)
        integrals = -length*local_mass @ derivative
        for first in range(3):
            row = indices[first]
            if row >= 0:
                right_side[row] += integrals[first]
                constant_side[row] -= length*np.sum(local_mass[first])
                for second in range(3):
                    column = indices[second]
                    if column >= 0:
                        bands[2+row-column, column] += length*local_mass[first, second]
    solved = solve_banded((2, 2), bands, np.column_stack([right_side, constant_side]), check_finite=False)
    projection, defect = solved[:, 0], 1+solved[:, 1]
    field = background*radii+front_profile(radii, time, speed, velocity, forcing)
    derivative = background+np.where(radii < 0,
        -forcing*np.maximum(time+radii/left_speed, 0)/left_speed,
        forcing*np.maximum(time-radii/right_speed, 0)/right_speed)
    left_trace, right_trace = background-forcing*time/left_speed, background+forcing*time/right_speed
    tail = np.where(radii < 0, left_trace, right_trace)*defect
    factors, unused = sparse_factors(len(base), True)
    original = factors[len(base)-1:].tocsr()
    vertices = np.searchsorted(radii, base)
    hinge = original @ np.maximum(base, 0.)
    field_factors = original @ field[vertices]-hinge*(jump @ field)
    projection_factors = original @ projection[vertices]-hinge*(jump @ projection)
    products = field_factors*projection_factors/spacing
    absolute = abs(original)
    source_rows = (np.asarray(absolute @ (base < 0)).ravel() > 0) & (np.asarray(absolute @ (base > 0)).ravel() > 0)
    support = np.asarray(abs(original[source_rows]).sum(axis=0)).ravel() > 0
    source_resolved = bool(np.all((base[support] > fronts[0]) & (base[support] < fronts[1])))
    curvature_jump = forcing*(left_speed**-2-right_speed**-2)
    coefficients = [graded_trace_coefficient(lengths[:source][::-1]), graded_trace_coefficient(lengths[source:])]
    trace_amplification = np.dot(coefficients, np.array([left_trace, right_trace])/lengths[source-1:source+1])
    quadratic = original @ np.maximum(base, 0.)**2
    step = original @ (base > 0).astype(float)
    tail_factor = original @ tail[vertices]
    predicted_source_factors = curvature_jump*quadratic[source_rows]/2
    predicted_projection_factors = (trace_amplification*hinge-(right_trace-left_trace)*step+tail_factor)[source_rows]
    source_prediction = float(predicted_source_factors @ predicted_projection_factors/spacing)
    source_actual = float(np.sum(products[source_rows]))
    return dict(spacing=spacing, phase=phase, count=len(radii),
        front_lengths=(-fronts[0], fronts[1]), minimum_front_cells=float(min(-fronts[0], fronts[1])/spacing),
        source_lengths=lengths[source-1:source+1].tolist(), source_rows=int(np.sum(source_rows)),
        source_stencil_front_resolved=source_resolved,
        source_support_interval=[float(min(base[support])), float(max(base[support]))],
        source_force=source_actual, source_local_prediction=source_prediction,
        source_prediction_error=abs(source_prediction-source_actual),
        total_projected_force=float(np.sum(products)), remaining_force=float(np.sum(products[~source_rows])),
        absolute_row_bound=float(np.sum(abs(products))),
        Gram_energy=float(field_factors @ field_factors/(2*spacing)),
        source_force_over_h=source_actual/spacing, remaining_force_over_h_squared=float(np.sum(products[~source_rows]))/spacing**2,
        energy_over_h_cubed=float(field_factors @ field_factors/(2*spacing**4)),
        projection_identity_error=float(np.max(abs(projection+derivative-tail))),
        source_jump_error=abs(float(jump @ field)-(right_trace-left_trace)),
        all_rows_retained=True, valid_for_claim=False)


def main():
    evidence = EvidenceRun('annular-P2-front-projected-Gram-attempt01', __file__)
    try:
        evidence.report.update(github_action=False, subagents_used=False,
            full_live_P2_force_convergence_proven=False, no_live_evolution=True,
            constant_weight_local_fixture_not_parent_solution=True,
            normalized_time_equals_one_by_similarity=True,
            source_and_two_fronts_fitted_in_scalar_mesh=True,
            wider_Gram_stencil_still_uses_uniform_base_vertices=True,
            no_fitted_force_or_parent_action_replacement=True,
            coefficient_source='same speed, velocity and forcing as prior unresolved-front fixture',
            actual_parent_front_resolution_not_yet_tested=True)
        for exponent in range(-2, 7):
            row = evaluate_front(2.**(-exponent))
            key = str(exponent)
            evidence.check(key+'_exact_profile_and_mass_projection', row['source_jump_error'] < 2e-11
                and row['projection_identity_error'] < 2e-11)
            evidence.check(key+'_all_row_split_and_bound',
                abs(row['total_projected_force']-row['source_force']-row['remaining_force']) < 2e-11
                and abs(row['total_projected_force']) <= row['absolute_row_bound']+2e-11)
            if row['source_stencil_front_resolved']:
                evidence.check(key+'_resolved_source_polynomial_law', row['source_prediction_error'] < 2e-10)
            evidence.report['cases'].append(row)
            evidence.save()
        resolved = [row for row in evidence.report['cases'] if row['source_stencil_front_resolved']]
        evidence.check('resolved_and_unresolved_stencils_both_exercised', len(resolved) >= 3
            and any(not row['source_stencil_front_resolved'] for row in evidence.report['cases']))
        evidence.check('unresolved_negative_control_rejects_local_polynomial_formula',
            evidence.report['cases'][0]['source_prediction_error'] > 1e-4)
        evidence.report.update(finest_to_previous_force_ratio=abs(resolved[-1]['total_projected_force']/resolved[-2]['total_projected_force']),
            finest_to_previous_energy_ratio=resolved[-1]['Gram_energy']/resolved[-2]['Gram_energy'],
            diagnostic_ratios_not_live_acceptance_gates=True)
        with (evidence.output/'completion.txt').open('w', encoding='utf-8') as stream, contextlib.redirect_stdout(stream):
            evidence.complete()
        evidence.own(evidence.output/'completion.txt', 'outputs')
        evidence.save()
        print(json.dumps(dict(state='complete', checks=len(evidence.report['checks']), cases=evidence.report['cases'])), flush=True)
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    main()
