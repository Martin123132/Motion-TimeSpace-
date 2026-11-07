from spatial_defect_common import *


def main():
    modest()
    packets={path.parent.name:json.loads(path.read_text()) for path in sorted((ROOT/'results').glob('*/status.json')) if path.parent.name!='validation'}
    assert len(packets)==9,list(packets)
    summary=dict(stage=131,state='science complete',scientific_checks=sum(row['count'] for row in packets.values()),
        passing_scientific_checks=sum(sum(item['passed'] for item in row['checks']) for row in packets.values()),
        failed_by_packet={name:[item['name'] for item in row['checks'] if not item['passed']] for name,row in packets.items() if not row['all_checks_passed']},
        operators={},feedback={},preflight=packets['preflight']['count'],inner_contract_checks=packets['inner-counterpart']['count'],
        inner_symbols={label:{band:max(row['variants'][label][band]['positive_growth_over_eigen'] for row in packets['inner-symbols']['rows']) for band in ['smooth','nyquist']} for label in ['physical','grid','second','third']},
        frequency_nodes=5265,response_steps=2048,inner_history_reused=True,new_inner_steps=0,
        local_splice_only=True,later_state_carried=False,corrected_inner_implemented=False,
        no_fit=True,no_measured_reference_difference_in_correction=True,inherited_stage130_failed_checks=17,
        next_target='Use the derived inner adjoint counterpart and finite-boundary/window terms to construct a controlled evolution correction. Test stability and chemical/number/energy identities before a paired restart run;do not assume a signed Taylor correction preserves positivity. Then carry corrected states continuously into later intervals with consistent sources and boundary accounting,retaining measured source-error uncertainty.')
    for label in ['corrected2','corrected3']:
        rows=[row for name,packet in packets.items() if name.startswith('operator-') for row in packet['rows']]
        summary['operators'][label]=dict(max_weak_relative=max(row['comparisons'][label]['weak_relative'] for row in rows),
            max_remaining_grid_error=max(row['comparisons'][label]['remaining_grid_error'] for row in rows),
            max_energy_defect=max(abs(row['comparisons'][label]['energy_defect_over_physical']) for row in rows))
    for name,packet in packets.items():
        if name.startswith('feedback-'):
            summary['feedback'][name]=packet['variants']
    summary['retained_failed_checks']=summary['scientific_checks']-summary['passing_scientific_checks']
    summary['raw_energy_evaluation_max']=max(row['diagnostics'][label+'_raw_energy_error'] for name,packet in packets.items()
        if name.startswith('operator-') for row in packet['rows'] for label in ['physical','second','third'])
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    print(json.dumps({key:value for key,value in summary.items() if key not in ['feedback','failed_by_packet']}),flush=True)
    print(json.dumps(dict(feedback={name:{label:{key:row.get(key) for key in ['direct_relative_endpoint','remaining_grid_error_peak','superposition_new_error']} for label,row in variants.items() if label!='matched'} for name,variants in summary['feedback'].items()},
        failures=summary['failed_by_packet'])),flush=True)


if __name__=='__main__':
    main()
