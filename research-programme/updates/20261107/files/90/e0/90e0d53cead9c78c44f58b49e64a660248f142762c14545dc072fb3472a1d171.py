from stage163_common import *


def main():
    modest()
    source=verify_packet(ROOT/'results/sources')
    diagnosis=verify_packet(ROOT/'results/precision-diagnosis')
    baseline=verify_packet(ROOT/'results/baseline-check')
    compensated=verify_packet(ROOT/'results/compensated-probe')
    correlated=verify_packet(ROOT/'results/correlated-soft-probe')
    assert diagnosis['all_checks_passed'] and baseline['all_checks_passed']
    assert compensated['all_checks_passed'] and correlated['all_checks_passed']
    assert not source['all_checks_passed']
    assert not (ROOT/'results/response').exists()
    precision=source['summary']['precision']
    groups={}
    for group,selector in [('complete_sources',':source'),('repaired_order_steps',':step'),('legacy_saved4_updates',':update')]:
        values=[value for key,value in precision.items() if selector in key]
        groups[group]=dict(columns=len(values),
            pair_pass=sum(value['pair']<1e-10 for value in values),
            spectral_pass=sum(value['moment']<1e-10 for value in values),
            largest_pair=max(value['pair'] for value in values),largest_spectral=max(value['moment'] for value in values))
    improvements=[]
    zero_residuals=0
    for record in correlated['records'].values():
        for old,new in zip(record['old_pair'],record['new_pair']):
            if new==0:
                zero_residuals+=1
            else:
                improvements.append(old/new)
    summary=dict(**source['summary'],precision_groups=groups,
        paired_baseline_mts=dict(saved_readout_checks=baseline['count'],all_checks_passed=True,
            baseline_preserved=True,mts_preserved=True,inner_histories_rerun=False),
        compensated_summation_probe=dict(events=8,all_checks_passed=True,records=compensated['records'],
            resolves_remaining_defect=False),
        correlated_soft_probe=dict(events=8,all_checks_passed=True,full_source_computed=False,
            minimum_nonzero_improvement=min(improvements),maximum_nonzero_improvement=max(improvements),
            floating_zero_cases=zero_residuals,largest_pair=max(max(row['new_pair']) for row in correlated['records'].values()),
            records=correlated['records']),
        new_response_evolutions=0,
        accepted_scope='All7560 endpoint event primitive moments repaired with stable photon jumps and analytic low-test functions;all complete-source gates pass;four warm65 pair checks and legacy-reference update checks retained;independent correlated-soft follow-up derived and tested on eight worst events;paired saved baseline/MTS preserved.',
        next_target='Apply the independently tested correlated-soft/Born difference form to all7560 endpoint real-event moments,reusing the repaired virtual/state terms and higher spectral rows;rerun the identical1e-10 gates. Preserve the failed legacy saved4-update checks and explicitly reconcile the order4 arithmetic repair with the saved reference before any response propagation. No refit or cutoff change.')
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    print(json.dumps(dict(groups=groups,probe_min_improvement=min(improvements),probe_max_improvement=max(improvements),
        zero_cases=zero_residuals,propagation_allowed=False)),flush=True)


if __name__=='__main__':
    main()
