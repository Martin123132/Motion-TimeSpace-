from time_refinement_common import *


COLUMNS=['baseline','join1','join2']


def crossing_coordinates(coordinate,values):
    selected=np.flatnonzero(values[:-1]*values[1:]<0)
    return [float(coordinate[index]-values[index]*(coordinate[index+1]-coordinate[index])/
        (values[index+1]-values[index])) for index in selected]


def main():
    modest()
    folder=ROOT/'results/time-comparison'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    checks,rows,inputs,window_rows=[],[],list(ladder.inputs),[]
    responses={}
    for upper in [.04,.02]:
        for model in ['heavy','cold']:
            packet_name=f'feedback-m{int(upper*1000)}'
            old_path=PARENT/'results'/f'{packet_name}-n5120'/(model+'-response.npz')
            new_path=ROOT/'results'/f'{packet_name}-n10240'/(model+'-response.npz')
            for path in [old_path,new_path]:
                local_packet(path.parent)
                inputs.extend([path,path.parent/'status.json'])
            old,new=read_npz(old_path),read_npz(new_path)
            assert np.array_equal(old['coordinate'],new['coordinate'])
            assert len(new['coordinate'])==2049
            responses[model,upper]=new
            coordinate=new['coordinate']
            old_gas,new_gas=old['gas'][:,:3],new['gas'][:,:3]
            delta=new_gas-old_gas
            peak=np.max(abs(new_gas),axis=0)
            late_peak=np.max(abs(new_gas[1536:]),axis=0)
            endpoint=abs(new_gas[-1])
            assert np.all(peak>0) and np.all(late_peak>0)
            relative_radiation=norm(new['physical_change']-old['physical_change'],basis.measure)/norm(new['physical_change'],basis.measure)
            peak_change=np.max(abs(delta),axis=0)/peak
            late_change=np.max(abs(delta[1536:]),axis=0)/late_peak
            endpoint_change=abs(delta[-1])/np.maximum(endpoint,1e-300)
            near_zero=endpoint<=1e-6*peak
            inner_fields={}
            for name,owner,steps in [('old',PARENT,5120),('new',ROOT,10240)]:
                path=owner/'results'/f'inner-{model}-n{steps}/prediction.npz'
                local_packet(path.parent)
                saved=read_npz(path)
                inputs.extend([path,path.parent/'status.json'])
                inner_fields[name]=np.stack([compact_defect(basis.nodes,saved['frequency'],values,upper) for values in saved['defect']])
            inner_relative=norm(inner_fields['new']-inner_fields['old'],basis.measure).max(axis=0)/norm(inner_fields['new'],basis.measure).max(axis=0)
            for name,value in [('Final radiation1percent',relative_radiation),
                    ('Full-history peak gas1percent',peak_change),('Late-quarter peak gas1percent',late_change),
                    ('Endpoint gas1percent',endpoint_change),('Inner1percent',inner_relative)]:
                checks.extend(check(f'{model}:m{int(upper*1000)}:{name}:{column}',float(result),.01)
                    for column,result in zip(COLUMNS,value))
            checks.extend(dict(name=f'{model}:m{int(upper*1000)}:Endpoint denominator resolved:{column}',
                passed=not bool(flag)) for column,flag in zip(COLUMNS,near_zero))
            np.savez_compressed(folder/f'{model}-m{int(upper*1000)}-gas-difference.npz',
                coordinate=coordinate,gas_old=old_gas,gas_new=new_gas,gas_difference=delta,late_start_index=1536)
            rows.append(dict(model=model,upper=upper,columns=COLUMNS,
                final_radiation_relative_change=relative_radiation.tolist(),
                inner_peak_relative_change=inner_relative.tolist(),
                gas_peak_relative_change=peak_change.tolist(),gas_late_relative_change=late_change.tolist(),
                gas_endpoint_relative_change=endpoint_change.tolist(),gas_endpoint_near_zero=near_zero.tolist(),
                gas_old_endpoint=old_gas[-1].tolist(),gas_new_endpoint=new_gas[-1].tolist(),
                gas_endpoint_difference=delta[-1].tolist(),gas_full_peak_denominator=peak.tolist(),
                gas_late_peak_denominator=late_peak.tolist(),gas_endpoint_denominator=endpoint.tolist(),
                gas_peak_absolute_difference=abs(delta).max(axis=0).tolist(),
                gas_late_absolute_difference=abs(delta[1536:]).max(axis=0).tolist(),
                gas_maximum_difference_coordinate=coordinate[np.argmax(abs(delta),axis=0)].tolist(),
                gas_late_maximum_difference_coordinate=coordinate[1536+np.argmax(abs(delta[1536:]),axis=0)].tolist(),
                gas_old_late_crossings=[crossing_coordinates(coordinate[1536:],old_gas[1536:,column]) for column in range(3)],
                gas_new_late_crossings=[crossing_coordinates(coordinate[1536:],new_gas[1536:,column]) for column in range(3)],
                late_start_index=1536,late_start_coordinate=float(coordinate[1536]),
                final_coordinate=float(coordinate[-1]),all_response_states_compared=2049,
                endpoint_sign_preserved=(np.sign(new_gas[-1])==np.sign(old_gas[-1])).tolist()))
    for model in ['heavy','cold']:
        wide,narrow=responses[model,.04],responses[model,.02]
        window_rows.append(dict(model=model,
            radiation_window_difference_over_wide=(norm(narrow['physical_change']-wide['physical_change'],basis.measure)/norm(wide['physical_change'],basis.measure)).tolist(),
            gas_endpoint_narrow_over_wide=(narrow['gas'][-1,:3]/wide['gas'][-1,:3]).tolist(),
            gas_window_late_difference_over_wide_peak=(abs(narrow['gas'][1536:,:3]-wide['gas'][1536:,:3]).max(axis=0)/abs(wide['gas'][1536:,:3]).max(axis=0)).tolist()))
    finish(folder,dict(checks=checks,rows=rows,window_rows=window_rows,
        inner_steps=[5120,10240],fixed_frequency_nodes=5265,response_steps=2048,source_epochs=65,
        late_interval='last quarter of evolution coordinate; indices1536..2048 inclusive',
        columns=COLUMNS,physical_inputs_unchanged=True,extrapolated_value_promoted=False,
        asymptotic_order_inferred=False,response_step_error_isolated=False),__file__,inputs)
    print(json.dumps(dict(rows=rows,window_rows=window_rows,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
