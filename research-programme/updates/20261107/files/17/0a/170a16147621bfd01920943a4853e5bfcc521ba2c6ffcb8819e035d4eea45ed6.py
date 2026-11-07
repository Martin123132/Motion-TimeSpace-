from half_history_common import *


def main():
    modest()
    names=['coefficients','evolution-heavy-carry','evolution-cold-carry','weak-m20','weak-m40',
        *[f'feedback-{model}-m{window}' for model in ['heavy','cold'] for window in [20,40]]]
    packets={name:local_packet(ROOT/'results'/name) for name in names}
    failures={name:[row['name'] for row in packet['checks'] if not row['passed']] for name,packet in packets.items()}
    failures={name:items for name,items in failures.items() if items}
    count=sum(len(packet['checks']) for packet in packets.values())
    passed=sum(sum(row['passed'] for row in packet['checks']) for packet in packets.values())
    responses={name:packet['variants'] for name,packet in packets.items() if name.startswith('feedback-')}
    weak=max(row['weak_relative'] for name in ['weak-m20','weak-m40'] for row in packets[name]['rows'])
    evolution={}
    for model in ['heavy','cold']:
        values=read_npz(ROOT/'results'/f'evolution-{model}-carry/prediction.npz')
        evolution[model]=dict(saved_sites=len(values['coordinate']),maximum_budget_error=float(np.max(values['budget'][:,5])),
            maximum_total_equation_error=float(np.max(values['budget'][:,6])),minimum_generator_dissipation=float(np.min(values['budget'][:,2])),
            seconds=packets[f'evolution-{model}-carry']['seconds'])
    next_target='Continue the same corrected two-level trajectory from20480 to25600 in another eight-interval resumable block,using the verified cached common source and independent physical-event comparisons. Track cumulative gas/radiation response and source-error budget before interpreting a full-history physical amplitude.'
    summary=dict(stage=137,previous_goal_turn='progress',packet_names=names,scientific_checks=count,passing_scientific_checks=passed,
        retained_failed_checks=count-passed,failed_by_packet=failures,evolution=evolution,responses=responses,max_weak_error=weak,
        all_band_symbol_upper=max(row['bound']['upper_bound'] for row in packets['coefficients']['rows']),
        continuous_inner_start=0,continuous_inner_stop=LAST_STEP,new_corrected_steps_per_background=LAST_STEP-FIRST_STEP,
        replayed_inner_steps=2*(LAST_STEP-FIRST_STEP),original_saved_epochs_covered=LAST_STEP//640+1,continuous_source_sites=LAST_STEP//20+1,
        full_original_source_epochs=65,source_knots=sorted(set(packets[name]['source_knots'] for name in responses)),
        response_steps=2048,frequency_nodes=5265,source_restore_step=LAST_STEP+20,full_history_recomputed=False,
        physical_reference_sites_per_window=len(SOURCE_STEPS),new_temperature_event_evaluations=packets['coefficients']['new_temperature_event_evaluations'],next_target=next_target)
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    lines=['# Stage137: corrected source evolution through thirty-two original intervals','',
        'Private/local. Stage136 is preserved;both backgrounds now carry the corrected solution continuously through global step20480.','',
        '## Larger continuous extension','',
        'Each background advances5120 additional steps from the corrected15360 restart with both BDF and outer time levels. The accepted trajectory is never reset to the original history. Baseline and both MTS columns are evolved together.',
        'The original5265 frequency grid,40960 global inner spacing,2048 response steps,physical boundary prescription and external driver are unchanged. One hundred twenty-eight new hashed restarts retain both time levels.',
        'The new257-knot coefficient bank evaluates248missing physical temperatures and reuses9original coarse endpoints. Both backgrounds share the verified thermal parameter. No normalization or physical coefficient is fitted.',
        f"The entire-band finite-principal-grid symbol bound remains <= {summary['all_band_symbol_upper']:.9g}. It has an analytic between-sample remainder and a conservative floating allowance,not a formal interval-arithmetic certificate.",'']
    for model,row in evolution.items():
        lines.append(f"- {model}: weighted norm-budget residual{row['maximum_budget_error']:.9g};total-field boundary equation residual{row['maximum_total_equation_error']:.9g};{row['saved_sites']}new-block saved sites.")
    lines+=['','The norm budget is numerical stability accounting,not physical radiation-energy conservation. The inherited control/restart tests remain evidence;no new original-law trajectory is relabelled as a control.','',
        '## Full new-block source comparison','',
        'Stage133 unit-shift source matrices are reused exactly. Independent physical-event sources are evaluated at every257new-block knot in BOTH matching windows,not just at endpoints. Seventeen direct common-kernel checks per window also test the cache independently.',
        f"Maximum common-versus-physical weak relative error: {weak:.9g}.",
        'The continuous prefix has1025dense source sites over thirty-two original intervals (thirty-three of65original coarse saved epochs). Later forcing is restored at20500 for this bounded feedback comparison. The corrected20480 state remains saved for continuous extension.','',
        '## Gas-response changes','',
        'Fractions refer to the small saved gas correction,not total gas temperature. Extension increments and common/physical source differences are propagated separately to avoid relying on subtraction of nearly equal responses.','',
        '| Background/window | Extension endpoint fraction: baseline, MTS1, MTS2 | Source-discretization endpoint fraction: baseline, MTS1, MTS2 |',
        '|---|---|---|']
    for name,row in responses.items():
        left=', '.join(f'{value:.9g}' for value in row['continuation']['relative_endpoint'])
        right=', '.join(f'{value:.9g}' for value in row['discretization']['relative_endpoint'])
        lines.append(f'| {name} | {left} | {right} |')
    lines+=['','Stage133 attributed its earlier large MTS change predominantly to source reconstruction. This extension does not assume that earlier attribution quantitatively applies to all new intervals. Large sensitivity flags must remain visible.','',
        '## Retained diagnostics','',f'{count}scientific checks:{passed}pass,{count-passed}retained failures. No thresholds changed.']
    for name,items in failures.items():
        lines.append('- '+name+': '+'; '.join(items))
    lines+=['','All prior failed checks remain sealed separately. No parent output is overwritten. Coverage refers to the saved time-coordinate span,not necessarily elapsed physical time or response weight.','',
        '## Next','',next_target,'','This is a numerical extension of the existing framework,not an observational preference or completion of the remaining thermal history.']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(dict(science=count,passed=passed,failed=count-passed,max_weak_error=weak,evolution=evolution,
        responses={name:{label:row[label]['relative_endpoint'] for label in ['continuation','discretization']} for name,row in responses.items()})),flush=True)


if __name__=='__main__':
    main()
