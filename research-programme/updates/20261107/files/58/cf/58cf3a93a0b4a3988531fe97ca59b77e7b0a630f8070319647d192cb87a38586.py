from cubic_inner_common import *


def main():
    modest()
    names=['coefficients','boundary-contract',*[f'replay-{model}-{variant}' for model in ['heavy','cold'] for variant in ['control','cubic']],
        'weak-m20','weak-m40',*[f'feedback-{model}-m{window}' for model in ['heavy','cold'] for window in [20,40]]]
    packets={name:local_packet(ROOT/'results'/name) for name in names}
    failures={name:[row['name'] for row in packet['checks'] if not row['passed']] for name,packet in packets.items()}
    failures={name:rows for name,rows in failures.items() if rows}
    count=sum(len(packet['checks']) for packet in packets.values())
    passed=sum(sum(row['passed'] for row in packet['checks']) for packet in packets.values())
    coefficient=packets['coefficients']['rows']
    weak=[row for name in ['weak-m20','weak-m40'] for row in packets[name]['rows']]
    budgets={}
    for model in ['heavy','cold']:
        replay=read_npz(ROOT/'results'/f'replay-{model}-cubic/prediction.npz')
        values=replay['budget']
        budgets[model]=dict(max_norm_balance_error=np.max(values[:,5],axis=0).tolist(),
            max_total_equation_error=np.max(values[:,6],axis=0).tolist(),
            cumulative_boundary_work=np.sum(values[:,4],axis=0).tolist(),
            cumulative_volume_work=np.sum(values[:,3],axis=0).tolist(),
            cumulative_generator_work=np.sum(values[:,2],axis=0).tolist(),
            endpoint_defect_relative=packets[f'replay-{model}-cubic']['endpoint_defect_relative'])
    responses={name:packet['variants'] for name,packet in packets.items() if name.startswith('feedback-')}
    next_target='Carry the corrected endpoint continuously into the next saved-epoch interval, deriving the next temperature coefficient/source bank from saved physical events; retain fixed frequency and response grids and paired baseline/MTS controls.'
    summary=dict(stage=132,scientific_checks=count,passing_scientific_checks=passed,retained_failed_checks=count-passed,
        failed_by_packet=failures,packet_names=names,all_frequency_symbol_upper=max(row['bound']['upper_bound'] for row in coefficient),
        worst_bulk_moment_error=max(row['moment_error'] for row in coefficient),
        max_negative_offdiagonals=max(row['negative_offdiagonal_coefficients'] for row in coefficient),
        max_negative_rate_fraction=max(row['negative_rate_l1_fraction'] for row in coefficient),
        max_weak_error=max(row['weak_relative'] for row in weak),
        max_remaining_original_weak_error=max(row['remaining_grid_error'] for row in weak),
        max_discrete_versus_continuum_taylor=max(row['discrete_versus_continuum_taylor_relative'] for row in weak),
        budgets=budgets,responses=responses,next_target=next_target,
        inner_steps_recomputed=2560,changed_inner_steps_per_background=640,later_history_carried=False,
        source_knots=139,changed_source_sites=33,frequency_nodes=5265,response_steps=2048)
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    lines=['# Stage132: derived correction installed in the inner evolution','',
        'Private/local. Earlier sealed work is unchanged. Baseline and both MTS columns receive identical numerical treatment.','',
        '## Construction and stability','',
        'Cubic interpolation in inverse Doppler ratio is the exact discrete variance-plus-skewness repair of the two-node deposition. Inner transport and weak source now share the same paired kernel; no fitted normalization is used.',
        f"Bulk moment residual <= {summary['worst_bulk_moment_error']:.9g}. The entire-band finite-principal-grid symbol bound is <= {summary['all_frequency_symbol_upper']:.9g} before positive clock scaling and DC/BR damping.",
        f"There are up to {summary['max_negative_offdiagonals']} negative off-diagonal coefficients (absolute-rate fraction <= {summary['max_negative_rate_fraction']:.9g}). Dissipativity does not imply positivity. The bound uses an analytic between-sample remainder and a conservative floating allowance, not formal interval arithmetic.",
        'Explicit ghost inflow, finite weighted adjoint and matching-window commutator tests pass. The recorded BDF norm budget is a stability diagnostic, not physical radiation energy. See PROJECTION-SCOPE.md.','',
        '## Paired restart result','',
        'Both 640-step controls reproduce Stage130 bitwise. Both corrected replays finish, with eight hashed restarts each containing both BDF time levels. The frequency grid, time spacing, outer histories and physical ghost prescriptions stay fixed.',
        'The new solver replaces the old mixed-stencil transport for the smooth driver as well as the defect. This is a combined consistency repair, not a source-only perturbation on unchanged states.','']
    for model,row in budgets.items():
        lines.append(f"- {model}: endpoint defect relative changes baseline/join1/join2 = {row['endpoint_defect_relative']}; maximum norm-budget residual = {max(row['max_norm_balance_error']):.9g}; total-field equation residual = {max(row['max_total_equation_error']):.9g}.")
    lines+=['','## Radiation and gas feedback','',
        f"Common cubic weak-source error <= {summary['max_weak_error']:.9g} relative to the saved matched-order physical event source. Remaining original weak error <= {summary['max_remaining_original_weak_error']:.9g}. Difference from Stage131 continuum Taylor correction <= {summary['max_discrete_versus_continuum_taylor']:.9g}.",
        'Feedback uses the inherited 139-knot local splice and 2048 response steps. Unchanged later forcing is retained. Independent difference-forcing solves separate the changed inner state from residual source discretization error. Fractions below refer to the small saved gas correction, not total gas temperature.','',
        '| Background/window | State-change endpoint fraction: baseline, MTS1, MTS2 | Source-discretization endpoint fraction: baseline, MTS1, MTS2 |',
        '|---|---|---|']
    for name,row in responses.items():
        left=', '.join(f'{value:.8g}' for value in row['state-change']['relative_endpoint'])
        right=', '.join(f'{value:.8g}' for value in row['discretization']['relative_endpoint'])
        lines.append(f'| {name} | {left} | {right} |')
    lines+=['','## Retained diagnostics','',f'{count} scientific checks: {passed} pass, {count-passed} retained failures. No acceptance thresholds changed.']
    for name,items in failures.items():
        lines.append(f'- {name}: '+ '; '.join(items))
    lines+=['','Raw full-response gas residuals and tiny-error subtraction tests are reported separately from direct difference-forcing results. Their failures are not erased by successful moment identities.','',
        '## Next','',next_target,'',
        'Corrected endpoints are saved but have not yet replaced the later inner trajectory. No observational MTS preference is inferred from this implementation experiment.']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(dict(science=count,passed=passed,failed=count-passed,weak_error=summary['max_weak_error'],
        responses={name:{label:row[label]['relative_endpoint'] for label in ['state-change','discretization']} for name,row in responses.items()})),flush=True)


if __name__=='__main__':
    main()
