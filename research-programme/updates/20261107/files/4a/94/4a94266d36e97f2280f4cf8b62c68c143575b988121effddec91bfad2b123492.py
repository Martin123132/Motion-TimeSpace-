from response_time_common import *


COLUMNS=['baseline','join1','join2']


def crossings(coordinate,values):
    indices=np.flatnonzero(values[:-1]*values[1:]<0)
    return [float(coordinate[index]-values[index]*(coordinate[index+1]-coordinate[index])/
        (values[index+1]-values[index])) for index in indices]


def main():
    modest()
    folder=ROOT/'results/response-comparison'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    stage119_path=PARENT/'results/time-comparison/status.json'
    local_packet(stage119_path.parent)
    inner_rows=json.loads(stage119_path.read_text())['rows']
    checks,rows,inputs,windows=[],[],[*ladder.inputs,stage119_path],[]
    responses={}
    for upper in [.04,.02]:
        for model in ['heavy','cold']:
            previous_path=PARENT/'results'/f'feedback-m{int(upper*1000)}-n10240'/(model+'-response.npz')
            current_path=ROOT/'results'/f'response-m{int(upper*1000)}-r4096'/(model+'-response.npz')
            for path in [previous_path,current_path]:
                local_packet(path.parent)
                inputs.extend([path,path.parent/'status.json'])
            previous,current=read_npz(previous_path),read_npz(current_path)
            assert np.array_equal(previous['coordinate'],current['coordinate'][::2])
            assert int(previous['integration_steps'])==2048 and int(current['integration_steps'])==4096
            for key in ['frequency','measure','replacement','unresolved_change','saved_potential','saved_residual']:
                assert np.array_equal(previous[key],current[key]),key
            checks.append(dict(name=f'{model}:m{int(upper*1000)}:Unchanged inner readout and common times',passed=True))
            old_gas,new_gas=previous['gas'][:,:3],current['gas'][:,:3]
            common=new_gas[::2]
            difference=common-old_gas
            peak=abs(new_gas).max(axis=0)
            late_peak=abs(new_gas[3072:]).max(axis=0)
            endpoint=abs(new_gas[-1])
            assert np.all(peak>0) and np.all(late_peak>0)
            peak_difference=abs(difference).max(axis=0)
            late_difference=abs(difference[1536:]).max(axis=0)
            endpoint_difference=abs(difference[-1])
            radiation=norm(current['physical_change']-previous['physical_change'],basis.measure)/norm(current['physical_change'],basis.measure)
            peak_relative=peak_difference/peak
            late_relative=late_difference/late_peak
            endpoint_relative=endpoint_difference/np.maximum(endpoint,1e-300)
            near_zero=endpoint<=1e-6*peak
            for name,value in [('Final radiation1percent',radiation),('Peak gas1percent',peak_relative),
                    ('Late gas1percent',late_relative),('Endpoint gas1percent',endpoint_relative)]:
                checks.extend(check(f'{model}:m{int(upper*1000)}:{name}:{column}',float(result),.01)
                    for column,result in zip(COLUMNS,value))
            checks.extend(dict(name=f'{model}:m{int(upper*1000)}:Endpoint denominator resolved:{column}',passed=not bool(flag))
                for column,flag in zip(COLUMNS,near_zero))
            inner=next(row for row in inner_rows if row['model']==model and row['upper']==upper)
            inner_endpoint=np.abs(np.array(inner['gas_endpoint_difference']))
            inner_peak=np.array(inner['gas_peak_absolute_difference'])
            common_endpoint=np.abs(np.array(inner['gas_new_endpoint']))
            assert np.array_equal(previous['gas'][-1,:3],np.array(inner['gas_new_endpoint']))
            rows.append(dict(model=model,upper=upper,columns=COLUMNS,
                radiation_relative_change=radiation.tolist(),gas_peak_relative_change=peak_relative.tolist(),
                gas_late_relative_change=late_relative.tolist(),gas_endpoint_relative_change=endpoint_relative.tolist(),
                gas_old_endpoint=old_gas[-1].tolist(),gas_new_endpoint=new_gas[-1].tolist(),
                gas_endpoint_difference=difference[-1].tolist(),gas_endpoint_near_zero=near_zero.tolist(),
                gas_full_peak_denominator=peak.tolist(),gas_late_peak_denominator=late_peak.tolist(),
                gas_endpoint_denominator=endpoint.tolist(),gas_peak_absolute_difference=peak_difference.tolist(),
                gas_late_absolute_difference=late_difference.tolist(),
                gas_peak_amplitude_change_over_refined_peak=((abs(new_gas).max(axis=0)-abs(old_gas).max(axis=0))/peak).tolist(),
                gas_peak_difference_coordinate=previous['coordinate'][np.argmax(abs(difference),axis=0)].tolist(),
                gas_late_difference_coordinate=previous['coordinate'][1536+np.argmax(abs(difference[1536:]),axis=0)].tolist(),
                gas_old_late_crossings=[crossings(previous['coordinate'][1536:],old_gas[1536:,index]) for index in range(3)],
                gas_new_late_crossings=[crossings(current['coordinate'][3072:],new_gas[3072:,index]) for index in range(3)],
                endpoint_sign_preserved=(np.sign(old_gas[-1])==np.sign(new_gas[-1])).tolist(),
                response_over_inner_endpoint_change=(endpoint_difference/np.maximum(inner_endpoint,1e-300)).tolist(),
                response_over_inner_peak_change=(peak_difference/np.maximum(inner_peak,1e-300)).tolist(),
                response_endpoint_change_over_stage119_endpoint=(endpoint_difference/np.maximum(common_endpoint,1e-300)).tolist(),
                inner_endpoint_change_over_stage119_endpoint=(inner_endpoint/np.maximum(common_endpoint,1e-300)).tolist(),
                compared_epochs=2049,refined_peak_epochs=4097,late_old_index=1536,late_new_index=3072,
                late_start_coordinate=float(current['coordinate'][3072]),final_coordinate=float(current['coordinate'][-1])))
            np.savez_compressed(folder/f'{model}-m{int(upper*1000)}-gas-difference.npz',
                coordinate=previous['coordinate'],gas_old=old_gas,gas_new_common=common,
                gas_difference=difference,refined_coordinate=current['coordinate'],gas_new_all=new_gas)
            responses[model,upper]=current
    for model in ['heavy','cold']:
        wide,narrow=responses[model,.04],responses[model,.02]
        windows.append(dict(model=model,radiation_window_difference_over_wide=(
            norm(narrow['physical_change']-wide['physical_change'],basis.measure)/norm(wide['physical_change'],basis.measure)).tolist(),
            gas_endpoint_narrow_over_wide=(narrow['gas'][-1,:3]/wide['gas'][-1,:3]).tolist()))
    finish(folder,dict(checks=checks,rows=rows,window_rows=windows,response_steps=[2048,4096],
        fixed_frequency_nodes=5265,fixed_inner_steps=10240,source_epochs=65,
        asymptotic_order_inferred=False,total_error_bound_claimed=False,
        compared_epochs=2049,refined_peak_epochs=4097,columns=COLUMNS),__file__,inputs)
    print(json.dumps(dict(rows=rows,windows=windows,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
