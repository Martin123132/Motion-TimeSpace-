from derive_annular_source_gravity_20260914 import EvidenceRun
from itertools import combinations
import numpy as np


def reduce_force(baseline,columns):
    baseline,columns = np.asarray(baseline,float),np.asarray(columns,float)
    if baseline.shape!=(4,) or columns.shape!=(4,3) or not np.isfinite(np.r_[baseline,columns.ravel()]).all():
        raise ValueError('Expected finite four-row baseline and4x3 columns')
    if columns[0,0]==0:
        raise ValueError('Cannot eliminate position with zero C0 force')
    ratio = columns[1:,0]/columns[0,0]
    return baseline[1:]-ratio*baseline[0],columns[1:,1:]-ratio[:,None]*columns[0,1:]


def diagnose(baseline,columns,baseline_error,column_error):
    baseline,columns = np.asarray(baseline,float),np.asarray(columns,float)
    baseline_error,column_error = np.asarray(baseline_error,float),np.asarray(column_error,float)
    reduced,operator = reduce_force(baseline,columns)
    if baseline_error.shape!=(4,) or column_error.shape!=(4,3) or not np.isfinite(np.r_[baseline_error,column_error.ravel()]).all():
        raise ValueError('Expected finite matched error arrays')
    if np.any(baseline_error<0) or np.any(column_error<0):
        raise ValueError('Negative sampled error')
    scales = np.max(abs(operator),axis=0)
    if np.any(scales==0):
        return dict(status='zero_reduced_column',rank_resolved=False,candidates=[],valid_for_claim=False)
    normalized = operator/scales
    target_scale = max(float(np.max(abs(reduced))),1e-300)
    singular = np.linalg.svd(normalized,compute_uv=False)
    numerical_rank = int(np.linalg.matrix_rank(normalized))
    ratio = columns[1:,0]/columns[0,0]
    denominator = abs(columns[0,0])-column_error[0,0]
    resolved_pivot = denominator>0
    reduced_error = None
    perturbation = None
    if resolved_pivot:
        ratio_error = (column_error[1:,0]+abs(ratio)*column_error[0,0])/denominator
        reduced_error = column_error[1:,1:]+abs(ratio[:,None])*column_error[0,1:]
        reduced_error += ratio_error[:,None]*(abs(columns[0,1:])+column_error[0,1:])
        perturbation = float(np.linalg.norm(reduced_error/scales,2))
    candidates = []

    def record(name,velocity_acceleration,solved_rows):
        position = -(baseline[0]+columns[0,1:]@velocity_acceleration)/columns[0,0]
        amplitudes = np.r_[position,velocity_acceleration]
        residual = baseline+columns@amplitudes
        error = baseline_error+column_error@abs(amplitudes)
        error += 64*np.finfo(float).eps*(abs(baseline)+abs(columns)@abs(amplitudes))
        candidates.append(dict(method=name,amplitudes=amplitudes.tolist(),residual=residual.tolist(),
            sampled_uncertainty=error.tolist(),within_sampled_uncertainty=bool(np.all(abs(residual)<=error)),
            solved_rows=solved_rows,omitted_rows=[row for row in range(4) if row not in solved_rows],
            valid_for_claim=False))

    for balanced in [False,True]:
        weights = np.maximum(np.max(abs(normalized),axis=1),1e-300) if balanced else np.ones(3)
        solution = np.linalg.lstsq(normalized/weights[:,None],-reduced/target_scale/weights,rcond=None)[0]
        record('row_balanced' if balanced else 'column_scaled',solution*target_scale/scales,[0])
    skipped = []
    for selected in combinations(range(3),2):
        block = normalized[list(selected)]
        if np.linalg.matrix_rank(block)<2:
            skipped.append(list(selected))
            continue
        solution = np.linalg.solve(block,-reduced[list(selected)]/target_scale)*target_scale/scales
        record('force_current_pair_'+''.join(str(value) for value in selected),solution,[0]+[value+1 for value in selected])
    null = np.cross(normalized[:,0],normalized[:,1])
    null_norm = float(np.linalg.norm(null))
    obstruction = None
    if numerical_rank==2 and null_norm>0:
        null /= null_norm
        obstruction = dict(left_null=null.tolist(),value=float(null@reduced),
            normalized_left_null_replay=float(np.max(abs(null@normalized))))
    return dict(status='provisional_position_enabled_diagnostic',reduced_baseline=reduced.tolist(),
        reduced_columns=operator.tolist(),singular_values=singular.tolist(),numerical_rank=numerical_rank,
        sampled_normalized_column_uncertainty=perturbation,position_pivot_resolved=bool(resolved_pivot),
        rank_resolved=bool(resolved_pivot and numerical_rank==2 and singular[-1]>5*perturbation),
        null_obstruction=obstruction,candidates=candidates,skipped_current_pairs=skipped,
        any_candidate_within_sampled_uncertainty=any(row['within_sampled_uncertainty'] for row in candidates),
        uncertainty_is_rigorous_bound=False,finite_history_established=False,valid_for_claim=False)
