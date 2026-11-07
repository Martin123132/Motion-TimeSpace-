from heavy40960_common import *


COLUMNS=['baseline','join1','join2']


def crossing_coordinates(coordinate,values):
    indices=np.flatnonzero(values[:-1]*values[1:]<0)
    return [float(coordinate[index]-values[index]*(coordinate[index+1]-coordinate[index])/
        (values[index+1]-values[index])) for index in indices]


def contraction_record(old_difference,new_difference,history_scale):
    resolved=old_difference>100*np.finfo(float).eps*np.maximum(history_scale,1e-300)
    ratios=[float(new/old) if flag else None for old,new,flag in zip(old_difference,new_difference,resolved)]
    orders=[float(-math.log2(value)) if value is not None and value>0 else None for value in ratios]
    return dict(old_absolute=old_difference.tolist(),new_absolute=new_difference.tolist(),
        denominator_resolved=resolved.tolist(),ratio=ratios,effective_order=orders,
        resolution_floor=(100*np.finfo(float).eps*np.maximum(history_scale,1e-300)).tolist())


def main():
    modest()
    folder=ROOT/'results/inner-contraction'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    checks,rows,inputs,windows=[],[],list(ladder.inputs),[]
    responses={}
    for upper in [.04,.02]:
        for model in ['heavy']:
            fields,inner_fields={},{}
            for name,owner,steps in [('coarse',COARSE_PARENT,10240),('previous',INNER_PARENT,20480),('refined',ROOT,40960)]:
                path=owner/'results'/f'feedback-m{int(upper*1000)}-n{steps}'/(model+'-response.npz')
                inner_path=owner/'results'/f'inner-{model}-n{steps}/prediction.npz'
                local_packet(path.parent)
                local_packet(inner_path.parent)
                inputs.extend([path,path.parent/'status.json',inner_path,inner_path.parent/'status.json'])
                fields[name]=read_npz(path)
                inner=read_npz(inner_path)
                assert len(inner['frequency'])==5265 and int(inner['steps'])==steps
                assert int(fields[name]['integration_steps'])==2048
                inner_fields[name]=np.stack([compact_defect(basis.nodes,inner['frequency'],values,upper) for values in inner['defect']])
            coarse,previous,refined=[fields[name] for name in ['coarse','previous','refined']]
            assert np.array_equal(coarse['coordinate'],previous['coordinate'])
            assert np.array_equal(previous['coordinate'],refined['coordinate'])
            assert len(refined['coordinate'])==2049
            coordinate=refined['coordinate']
            gas_coarse,gas_previous,gas_refined=[item['gas'][:,:3] for item in [coarse,previous,refined]]
            old_delta,new_delta=gas_previous-gas_coarse,gas_refined-gas_previous
            gas_norms=[abs(item).max(axis=0) for item in [gas_coarse,gas_previous,gas_refined]]
            late_norms=[abs(item[1536:]).max(axis=0) for item in [gas_coarse,gas_previous,gas_refined]]
            endpoint_norms=[abs(item[-1]) for item in [gas_coarse,gas_previous,gas_refined]]
            radiation_norms=[norm(item['physical_change'],basis.measure) for item in [coarse,previous,refined]]
            inner_norms=[norm(inner_fields[name],basis.measure).max(axis=0) for name in ['coarse','previous','refined']]
            old_differences={
                'radiation':norm(previous['physical_change']-coarse['physical_change'],basis.measure),
                'gas_peak':abs(old_delta).max(axis=0),'gas_late':abs(old_delta[1536:]).max(axis=0),
                'gas_endpoint':abs(old_delta[-1]),
                'inner':norm(inner_fields['previous']-inner_fields['coarse'],basis.measure).max(axis=0)}
            new_differences={
                'radiation':norm(refined['physical_change']-previous['physical_change'],basis.measure),
                'gas_peak':abs(new_delta).max(axis=0),'gas_late':abs(new_delta[1536:]).max(axis=0),
                'gas_endpoint':abs(new_delta[-1]),
                'inner':norm(inner_fields['refined']-inner_fields['previous'],basis.measure).max(axis=0)}
            all_norms=dict(radiation=radiation_norms,gas_peak=gas_norms,gas_late=late_norms,
                gas_endpoint=endpoint_norms,inner=inner_norms)
            relative,contractions={},{}
            for metric in old_differences:
                relative[metric]=(new_differences[metric]/np.maximum(all_norms[metric][-1],1e-300)).tolist()
                record=contraction_record(old_differences[metric],new_differences[metric],np.maximum.reduce(all_norms[metric]))
                contractions[metric]=record
                for index,column in enumerate(COLUMNS):
                    prefix=f'{model}:m{int(upper*1000)}:{metric}:{column}'
                    checks.append(check(prefix+':1percent',relative[metric][index],.01))
                    ratio=record['ratio'][index]
                    checks.append(dict(name=prefix+':Contraction',value=ratio,limit=1.,
                        passed=bool(record['denominator_resolved'][index] and ratio<=1.)))
                    checks.append(dict(name=prefix+':Resolved difference denominator',
                        passed=bool(record['denominator_resolved'][index])))
            near_zero=endpoint_norms[-1]<=1e-6*gas_norms[-1]
            checks.extend(dict(name=f'{model}:m{int(upper*1000)}:Endpoint denominator:{column}',passed=not bool(flag))
                for column,flag in zip(COLUMNS,near_zero))
            rows.append(dict(model=model,upper=upper,columns=COLUMNS,
                relative_change=relative,contractions=contractions,
                gas_coarse_endpoint=gas_coarse[-1].tolist(),gas_previous_endpoint=gas_previous[-1].tolist(),
                gas_refined_endpoint=gas_refined[-1].tolist(),gas_old_endpoint_increment=old_delta[-1].tolist(),
                gas_new_endpoint_increment=new_delta[-1].tolist(),
                endpoint_increment_direction_preserved=(np.sign(old_delta[-1])==np.sign(new_delta[-1])).tolist(),
                endpoint_response_sign_preserved=(np.sign(gas_previous[-1])==np.sign(gas_refined[-1])).tolist(),
                endpoint_near_zero=near_zero.tolist(),
                gas_full_peak_denominator=gas_norms[-1].tolist(),gas_late_peak_denominator=late_norms[-1].tolist(),
                gas_endpoint_denominator=endpoint_norms[-1].tolist(),
                gas_difference_maximum_coordinate=coordinate[np.argmax(abs(new_delta),axis=0)].tolist(),
                gas_late_difference_maximum_coordinate=coordinate[1536+np.argmax(abs(new_delta[1536:]),axis=0)].tolist(),
                gas_previous_late_crossings=[crossing_coordinates(coordinate[1536:],gas_previous[1536:,index]) for index in range(3)],
                gas_refined_late_crossings=[crossing_coordinates(coordinate[1536:],gas_refined[1536:,index]) for index in range(3)],
                compared_epochs=2049,late_start_index=1536,late_start_coordinate=float(coordinate[1536])))
            np.savez_compressed(folder/f'{model}-m{int(upper*1000)}-gas-differences.npz',coordinate=coordinate,
                gas_coarse=gas_coarse,gas_previous=gas_previous,gas_refined=gas_refined,
                old_difference=old_delta,new_difference=new_delta)
            responses[model,upper]=refined
    for model in ['heavy']:
        wide,narrow=responses[model,.04],responses[model,.02]
        windows.append(dict(model=model,radiation_window_difference_over_wide=(
            norm(narrow['physical_change']-wide['physical_change'],basis.measure)/norm(wide['physical_change'],basis.measure)).tolist(),
            gas_endpoint_narrow_over_wide=(narrow['gas'][-1,:3]/wide['gas'][-1,:3]).tolist()))
    finish(folder,dict(checks=checks,rows=rows,window_rows=windows,inner_steps=[10240,20480,40960],
        fixed_frequency_nodes=5265,response_steps=2048,source_epochs=65,
        effective_order_is_observed_only=True,asymptotic_order_proven=False,extrapolated_value_promoted=False,
        total_error_bound_claimed=False,columns=COLUMNS),__file__,inputs)
    print(json.dumps(dict(rows=rows,windows=windows,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
