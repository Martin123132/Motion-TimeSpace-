from carry_common import *


def main():
    modest()
    names=['coefficients',*[f'evolution-{model}-{variant}' for model in ['heavy','cold'] for variant in ['control','reset','carry']],
        'memory-contract','weak-m20','weak-m40','linear-source-cache',
        *[f'feedback-{model}-m{window}' for model in ['heavy','cold'] for window in [20,40]],
        *[f'attribution-{model}-m{window}' for model in ['heavy','cold'] for window in [20,40]]]
    packets={name:local_packet(ROOT/'results'/name) for name in names}
    failures={name:[row['name'] for row in packet['checks'] if not row['passed']] for name,packet in packets.items()}
    failures={name:items for name,items in failures.items() if items}
    count=sum(len(packet['checks']) for packet in packets.values())
    passed=sum(sum(row['passed'] for row in packet['checks']) for packet in packets.values())
    responses={name:packet['variants'] for name,packet in packets.items() if name.startswith('feedback-')}
    memory=packets['memory-contract']['models']
    weak=max(row['weak_relative'] for name in ['weak-m20','weak-m40'] for row in packets[name]['rows'])
    attribution={name:packet['contributions'] for name,packet in packets.items() if name.startswith('attribution-')}
    cache=packets['linear-source-cache']['windows']
    next_target='Extend the continuously corrected and response-collocated source history in a larger resumable chunk toward step5120. Reuse the now verified fixed-shift unit-source cache rather than recomputing basis shifts at every temperature; keep independent physical-event spot checks, paired baseline/MTS, fixed grids and the four-hour check-in.'
    summary=dict(stage=133,previous_goal_turn='progress',packet_names=names,scientific_checks=count,passing_scientific_checks=passed,
        retained_failed_checks=count-passed,failed_by_packet=failures,memory=memory,responses=responses,attribution=attribution,linear_source_cache=cache,max_weak_error=weak,
        all_band_symbol_upper=max(row['bound']['upper_bound'] for row in packets['coefficients']['rows']),
        continuous_inner_start=0,continuous_inner_stop=1280,new_corrected_steps_per_background=640,
        replayed_inner_steps=3840,original_saved_epochs_covered=3,continuous_source_sites=65,
        full_original_source_epochs=65,source_knots=sorted(set(packets[name]['source_knots'] for name in responses)),
        response_steps=2048,frequency_nodes=5265,source_restore_step=1300,full_history_recomputed=False,next_target=next_target)
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    lines=['# Stage133: the corrected state now carries through the next interval','',
        'Private/local. This is a continuous extension of Stage132, not a new independent trajectory or a replacement theory.','',
        '## Continuity and controls','',
        'Both backgrounds carry global steps641--1280 from the corrected640 restart with both BDF levels. No first-order restart and no reset to the original history. The completed0--640 prefix is unchanged.',
        'Both original-equation controls reproduce original saved epoch2 bitwise. A separately labelled reset diagnostic uses the same corrected operator but starts from the original state, exposing the inherited-memory contribution.',
        'Baseline and both MTS columns share the same frequency5265 grid, global40960 inner spacing and2048 response steps. Forty-eight hashed continuation restart records preserve both time levels.',
        f"The new33-knot bank reuses two endpoint events and evaluates31 intermediate temperatures from the existing order6 physical kernel. Entire-band finite-grid symbol upper bound <= {summary['all_band_symbol_upper']:.9g}; no fitted normalization.",'',
        '## Carried memory','',
        'Carry-minus-reset solves the homogeneous difference equation. Its BDF G-norm is a numerical stability quantity, not physical radiation energy.']
    for model,row in memory.items():
        lines.append(f"- {model}: final/initial G-norm-squared = {row['initial_to_final_ratio']}; endpoint carry/reset difference relative to the corrected defect = {row['endpoint_memory_relative']}.")
    lines+=['','## Radiation and gas','',
        f"The common cubic source differs from the matched physical-event source by <= {weak:.9g} in the recorded weak-operator norm over the new interval.",
        'The source now resolves65 sites over the first TWO original intervals, not all65 original epochs. Feedback preserves the inherited later forcing from step1300 onward. The corrected inner endpoint is saved independently for further continuous carry.',
        'Independent difference-forcing solves separate the extension effect from cumulative cubic-source discretization. Fractions below refer to the small saved gas correction, not total gas temperature.','',
        '| Background/window | Extension endpoint fraction: baseline, MTS1, MTS2 | Source-discretization endpoint fraction: baseline, MTS1, MTS2 |',
        '|---|---|---|']
    for name,row in responses.items():
        left=', '.join(f'{value:.9g}' for value in row['continuation']['relative_endpoint'])
        right=', '.join(f'{value:.9g}' for value in row['discretization']['relative_endpoint'])
        lines.append(f'| {name} | {left} | {right} |')
    lines+=['','The extension comparison includes replacing the previously interpolated second-interval source with the newly evolved and directly evaluated source; it is not a pure memory-only observable. The separate reset diagnostic isolates memory in the inner solver.','',
        '## Source attribution','',
        'The large MTS change requires diagnosis before promoting the earlier small correction. An exact source telescoping identity and independent response solves separate reference reconstruction, operator update and inherited memory. Reference reconstruction includes sampling and matched-order reevaluation; it is not a pure temperature-interpolation claim.','',
        '| Background/window | Reference reconstruction signed fraction | Operator update signed fraction | Carried memory signed fraction |',
        '|---|---|---|---|']
    for name,parts in attribution.items():
        entries=[' / '.join(f'{value:.8g}' for value in parts[label]['signed_endpoint_fraction_of_extension'])
            for label in ['reference-reconstruction','operator-update','carried-memory']]
        lines.append('| '+name+' | '+' | '.join(entries)+' |')
    lines+=['','Each cell lists baseline/MTS1/MTS2. Fractions are signed and can exceed1 when contributions cancel. Only the carry history is accepted; control/reset source histories are bookkeeping counterfactuals. See ATTRIBUTION.md.','',
        '## Exact source reuse','',
        'The source is linear in its fixed-grid shift rates. Unit-shift weak matrices are now cached and tested against all65 prefix sites and coefficient midpoints, without a temperature fit or replacement of independent physical references.']
    for window,row in cache.items():
        lines.append(f"- Window{window}: maximum saved-source relative reproduction error{row['max_saved_relative']:.9g};65-matrix assembly{row['assemble65_seconds']:.6g}s after one-time unit construction{row['unit_construction_seconds']:.6g}s.")
    lines+=['',
        '## Retained diagnostics','',f'{count} scientific checks: {passed} pass and {count-passed} retained failures. No thresholds changed.']
    for name,items in failures.items():
        lines.append('- '+name+': '+'; '.join(items))
    lines+=['','Raw gas residuals and subtraction of tiny differences remain distinct diagnostics from independent difference-forcing solves. Earlier failures remain in their sealed stages.','',
        '## Next','',next_target,'','No new physical coupling, cutoff, parent-action assumption, or observational preference is inferred from these numerical tests.']
    (ROOT/'RESULTS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(json.dumps(dict(science=count,passed=passed,failed=count-passed,max_weak_error=weak,memory=memory,
        responses={name:{label:row[label]['relative_endpoint'] for label in ['continuation','discretization']} for name,row in responses.items()})),flush=True)


if __name__=='__main__':
    main()
