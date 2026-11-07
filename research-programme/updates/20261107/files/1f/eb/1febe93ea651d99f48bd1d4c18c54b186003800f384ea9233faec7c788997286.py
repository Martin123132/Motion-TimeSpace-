from fractions import Fraction
from itertools import combinations, product
import numpy as np


def determinant(rows):
    return (rows[0][0]*(rows[1][1]*rows[2][2]-rows[1][2]*rows[2][1])
        -rows[0][1]*(rows[1][0]*rows[2][2]-rows[1][2]*rows[2][0])
        +rows[0][2]*(rows[1][0]*rows[2][1]-rows[1][1]*rows[2][0]))


def envelope_search(baseline, columns, baseline_error, column_error):
    baseline, columns, baseline_error, column_error = [np.asarray(value, float) for value in
        [baseline, columns, baseline_error, column_error]]
    if baseline.shape!=(4,) or columns.shape!=(4, 3) or baseline_error.shape!=(4,) or column_error.shape!=(4, 3):
        raise ValueError('Expected four rows, three columns and matched errors')
    if not np.isfinite(np.r_[baseline, columns.ravel(), baseline_error, column_error.ravel()]).all():
        raise ValueError('Nonfinite exact feasibility input')
    if np.any(baseline_error<0) or np.any(column_error<0):
        raise ValueError('Negative exact feasibility error')
    rational = lambda value:Fraction.from_float(float(value))
    exact_baseline = [rational(value) for value in baseline]
    exact_columns = [[rational(value) for value in row] for row in columns]
    exact_base_error = [rational(value) for value in baseline_error]
    exact_error = [[rational(value) for value in row] for row in column_error]
    row_scale = [max(abs(value), error, Fraction(1, 10**300)) for value, error in zip(exact_baseline, exact_base_error)]
    objective_weights = [max([abs(exact_columns[row][column])/row_scale[row] for row in range(4)]+[Fraction(1, 10**300)])
        for column in range(3)]
    records, best_global, best_global_score = [], None, None
    for signs in product([-1, 1], repeat=3):
        constraints = []
        for side in [1, -1]:
            for row in range(4):
                values = [side*exact_columns[row][column]*signs[column]-exact_error[row][column] for column in range(3)]
                values.append(exact_base_error[row]-side*exact_baseline[row])
                denominator = max(value.denominator for value in values)
                constraints.append([value.numerator*(denominator//value.denominator) for value in values])
        constraints += [[-int(column==row) for column in range(3)]+[0] for row in range(3)]
        best, best_score, independent, feasible = None, None, 0, 0
        for selected in combinations(range(11), 3):
            matrix = [constraints[row][:3] for row in selected]
            denominator = determinant(matrix)
            if denominator==0:
                continue
            independent += 1
            target = [constraints[row][3] for row in selected]
            numerator = [determinant([[target[row] if column==replaced else matrix[row][column] for column in range(3)]
                for row in range(3)]) for replaced in range(3)]
            if denominator<0:
                denominator, numerator = -denominator, [-value for value in numerator]
            if any(sum(row[column]*numerator[column] for column in range(3))>row[3]*denominator for row in constraints):
                continue
            feasible += 1
            score = sum(objective_weights[column]*Fraction(numerator[column], denominator) for column in range(3))
            if best_score is not None and score>=best_score:
                continue
            best_score = score
            best = dict(numerator=[str(value) for value in numerator], denominator=str(denominator),
                active_constraints=list(selected), objective_numerator=str(score.numerator), objective_denominator=str(score.denominator))
        record = dict(signs=list(signs), solver_status=0 if best is not None else 2,
            message='Exact integer vertex enumeration', solver_success=best is not None,
            replay_passed=best is not None, independent_triples=independent, feasible_triples=feasible,
            enumerated_triples=165, exact_constraints=[[str(value) for value in row] for row in constraints],
            exact_witness=best, valid_for_claim=False)
        if best is not None:
            amplitudes = np.array([float(signs[column]*Fraction(int(best['numerator'][column]), int(best['denominator']))) for column in range(3)])
            residual = np.asarray(baseline, np.longdouble)+np.asarray(columns, np.longdouble)@np.asarray(amplitudes, np.longdouble)
            budget = np.asarray(baseline_error, np.longdouble)+np.asarray(column_error, np.longdouble)@abs(np.asarray(amplitudes, np.longdouble))
            arithmetic = 512*np.finfo(float).eps*(abs(baseline)+abs(columns)@abs(amplitudes))
            record.update(amplitudes=amplitudes.tolist(), residual=np.asarray(residual, float).tolist(),
                sampled_uncertainty=np.asarray(budget, float).tolist(), replay_arithmetic=arithmetic.tolist(),
                floating_rendering_replay_passed=bool(np.all(abs(residual)<=budget+arithmetic)), objective=float(best_score))
            if best_global_score is None or best_score<best_global_score:
                best_global, best_global_score = record, best_score
        records.append(record)
    return dict(orthants=records, any_replayed_witness=best_global is not None, minimum_scaled_witness=best_global,
        coefficient_perturbations_independent=True, correlated_parent_realizability_established=False,
        exact_infeasibility_proven=best_global is None, exact_input_contract='supplied_binary64_as_rational',
        error_arrays_proven_continuum_bounds=False, valid_for_claim=False)
