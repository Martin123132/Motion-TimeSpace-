from source_pair_common import *


def main():
    modest()
    packets={path.parent.name:json.loads(path.read_text()) for path in sorted((ROOT/'results').glob('*/status.json')) if path.parent.name!='validation'}
    assert len(packets)==14,list(packets)
    construction=packets['balanced-coefficients']
    summary=dict(stage=130,state='science complete',scientific_checks=sum(row['count'] for row in packets.values()),
        passing_scientific_checks=sum(sum(check_row['passed'] for check_row in row['checks']) for row in packets.values()),
        failed_by_packet={name:[item['name'] for item in row['checks'] if not item['passed']] for name,row in packets.items() if not row['all_checks_passed']},
        maximum_symbol_identity=max(row['adjoint_identity_residual'] for row in construction['rows']),
        maximum_symbol_errors={key:max(row['comparison'][key] for row in construction['rows']) for key in construction['rows'][0]['comparison']},
        maximum_pairing_rate_change=max(row['rate_change_from_total_relative'] for row in construction['rows']),
        moment_maximum=max(row['moment_error'] for row in construction['rows']),
        weak_actions={},feedback={},replays={},shape_attribution={},boundary=packets['finite-adjoint']['rows'],
        local_splice_only=True,later_state_carried=False,full_grid_energy_budget=False,empirical_fit=False,
        inherited_stage129_failed_checks=69,frequency_nodes=5265,response_steps=2048,inner_global_steps=40960,
        next_target='The source-derived pairing fixes the algebraic choice,but physical-versus-grid weak-shape error is amplified in the small gas correction. Use the independently evolved error response to set an accuracy budget. Derive/measure the leading spatial shape defect or carry both source treatments with that explicit uncertainty,then extend the corrected state continuously through later intervals with boundary/inflow accounting. Do not spend a full-history run pretending a bulk moment pass removes the measured shape error.')
    for label in ['source','total']:
        weak=[row['comparisons'][label] for name,packet in packets.items() if name.startswith('weak-') for row in packet['rows']]
        summary['weak_actions'][label]=dict(max_dual_operator_relative=max(row['weak_dual_frobenius_relative'] for row in weak),
            max_physical_state_relative={model:np.max(np.array([row['physical_state_action_relative'][model] for row in weak]),axis=0).tolist() for model in ['heavy','cold']})
    for name,packet in packets.items():
        if name.startswith('shape-error-'):
            summary['shape_attribution'][name]=dict(removed_weak_moment_relative=packet['removed_weak_moment_relative'],variants=packet['variants'])
        if name.startswith('feedback-'):
            summary['feedback'][name]={label:dict(comparison=row['comparison'],response_errors=row['response_errors']) for label,row in packet['variants'].items()}
        if name.startswith('replay-'):
            model=packet['model']
            old_path=PARENT/'results'/f'replay-{model}-balanced/prediction.npz'
            new_path=ROOT/'results'/name/'prediction.npz'
            old,new=map(read_npz,[old_path,new_path])
            delta=new['defect'][-1]-old['defect'][-1]
            summary['replays'][model]=dict(endpoint_relative_to_total=(np.max(abs(delta),axis=0)/np.maximum(np.max(abs(old['defect'][-1]),axis=0),1e-300)).tolist(),solve_errors=packet['solve_errors'])
    summary['retained_failed_checks']=summary['scientific_checks']-summary['passing_scientific_checks']
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    print(json.dumps({key:value for key,value in summary.items() if key not in ['boundary','feedback','failed_by_packet']}),flush=True)
    print(json.dumps(dict(feedback={name:{label:row['comparison']['gas_endpoint_relative'] for label,row in variants.items()} for name,variants in summary['feedback'].items()},failures=summary['failed_by_packet'])),flush=True)


if __name__=='__main__':
    main()
