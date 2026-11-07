from interpolation_common import *


def main():
    packets=[]
    failures={}
    inputs={}
    for path in sorted((ROOT/'results').glob('case-*/status.json')):
        packet=local_packet(path.parent)
        packets.append(packet)
        inputs[str(path)]=digest(path)
        names=[row['name'] for row in packet['checks'] if not row['passed']]
        if names:
            failures[path.parent.name]=names
    assert len(packets)==4
    count=sum(len(packet['checks']) for packet in packets)
    passing=sum(row['passed'] for packet in packets for row in packet['checks'])
    assert all(name.startswith('Response:') and name.endswith(':gas') for names in failures.values() for name in names)
    mts_residual=[value for packet in packets for value in packet['factored_operator_endpoint_residual_ratio'][1:]]
    baseline_residual=[packet['factored_operator_endpoint_residual_ratio'][0] for packet in packets]
    maxima=dict(factored_mts_endpoint=max(max(packet['candidate_comparisons']['factored']['gas_endpoint_relative'][1:]) for packet in packets),
        factored_baseline_endpoint=max(packet['candidate_comparisons']['factored']['gas_endpoint_relative'][0] for packet in packets),
        factored_radiation=max(max(packet['candidate_comparisons']['factored']['radiation_relative']) for packet in packets),
        closure=max(max(packet['closure'].values()) for packet in packets),
        raw_gas_residual=max(max(value['gas'] for value in packet['response_errors'].values()) for packet in packets),
        energy_moment_error=max(next(row['value'] for row in packet['checks'] if row['name']=='Exact candidate energy moment') for packet in packets),
        moment_curvature=max(max(abs(value) for value in packet['moment_curvature_relative']) for packet in packets))
    assert all(all(packet['operator_endpoint_resolved']) for packet in packets)
    prior=json.loads((PARENT/'ACCURACY-REVIEW.json').read_text())
    scope='Exact source-product and energy-moment decompositions at33 saved first-interval sites;two backgrounds/windows and baseline/MTS;fixed evolution and response grids;source-only factored interpolation.'
    conclusion=('The signed decomposition identifies curvature of the known Compton energy moment as the dominant '
        'operator-interpolation contribution. Factoring that moment leaves only0.03104–0.03112percent of the MTS '
        'operator-induced endpoint discrepancy,with opposing shape/mixed terms retained. The source-only factored '
        'candidate agrees with directly sampled source responses to0.1755percent of the MTS gas correction or better. '
        'This is a derived moment-preserving numerical representation,not a fitted physical coupling or a new history. '
        'All12 raw gas residual failures remain;the worst is1.677e-5. Refine the matching inner Compton coefficients next.')
    next_target=('Use the saved order6 Doppler events at the33 first-interval temperatures to rebuild the positive '
        'and high-order inner Compton stencils and their matched eigenvalue,retaining the5265 grid and40960 inner steps. '
        'Check constant/chemical and energy-moment contracts before evolution. Replay only the first640 steps from '
        'the original restart for both backgrounds,keeping initial matching,DC/BR,clock/outer drivers and other '
        'intervals fixed to isolate the Compton coefficient change. Recalculate the direct and moment-factored '
        'sources from those new states and propagate with2048 response steps. Treat this as a bounded Compton '
        'inner/source consistency test;separately track the remaining clock/emission coefficient interpolation and '
        'the need to carry changed endpoint state into subsequent intervals.')
    summary=dict(stage=128,scope=scope,checks=count,passes=passing,retained_failed_checks=count-passing,
        rows=[{key:value for key,value in packet.items() if key not in ['input_hashes','checks']} for packet in packets],
        maxima=maxima,mts_operator_residual_range=[min(mts_residual),max(mts_residual)],
        baseline_operator_residual_range=[min(baseline_residual),max(baseline_residual)],
        source_packet_hashes=inputs,new_inner_steps=0,new_temperature_integrals=0)
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    review=dict(stage=128,accepted_scope=scope,scientific_checks=count,passing_scientific_checks=passing,
        retained_failed_checks=count-passing,expected_failed_by_packet=failures,
        combined_original_response_failures=prior['combined_original_response_failures'],
        prior_stage_failed_checks_retained=prior['retained_failed_checks'],maxima=maxima,
        conclusion=conclusion,next_target=next_target,independent_validation_required=True,
        inner_source_consistency_established=False,physical_time_accuracy_certified=False,
        new_high_precision=False,fitted_normalization=False,goal_turn_classification='progress')
    write_json(ROOT/'ACCURACY-REVIEW.json',review)
    print(json.dumps(dict(checks=count,passes=passing,failures=count-passing,maxima=maxima,
        mts_residual=summary['mts_operator_residual_range'],baseline_residual=summary['baseline_operator_residual_range'],
        endpoints=[dict(model=packet['model'],upper=packet['upper'],endpoint=packet['endpoint'],
            peak_residual=packet['factored_operator_peak_residual_ratio']) for packet in packets])),flush=True)


if __name__=='__main__':
    main()
