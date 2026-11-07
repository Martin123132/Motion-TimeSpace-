from source_probe_common import *
from propagate_matched_feedback import solve_response


def main():
    modest()
    folder=ROOT/'results/source-attribution'
    folder.mkdir(parents=True,exist_ok=False)
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    basis=ladder.basis
    checks,rows,inputs=[],[],list(ladder.inputs)
    for model in ['heavy','cold']:
        background=thermal_wave.thermal.ThermalBackground(model)
        emission=NonlocalEmission(basis,background,'nonlocal-leading',BRANCH/'infrared-source-domain-20261008/banks/s960-i256')
        inputs.extend([*emission.inputs,background.parent.source,background.native_constants])
        for upper in [.04,.02]:
            probe=ROOT/'results'/f'probe-{model}-m{int(upper*1000)}'
            source={label:read_npz(probe/(label+'-source.npz')) for label in ['linear','assembled','direct']}
            response={label:read_npz(probe/(label+'-response.npz')) for label in source}
            inputs.extend([probe/(label+suffix) for label in source for suffix in ['-source.npz','-response.npz']])
            coordinate=source['direct']['coordinate']
            old_source_path=refined_owner(model)/'results'/f'feedback-m{int(upper*1000)}-n40960'/(model+'-source.npz')
            old_source=read_npz(old_source_path)
            inputs.append(old_source_path)
            difference=source['direct']['source']-source['linear']['source']
            first=difference.copy()
            first[coordinate>=old_source['coordinate'][1]]=0
            remaining=difference-first
            operator=source['direct']['source']-source['assembled']['source']
            assert not np.count_nonzero(operator[:,1:])
            deltas={}
            for label,forcing in [('first',first),('remaining',remaining),('operator',operator)]:
                packet=dict(coordinate=coordinate,source=forcing)
                solution,errors=solve_response(model,packet,2048,ladder,emission,background)
                np.savez_compressed(folder/f'{model}-m{int(upper*1000)}-{label}.npz',
                    coordinate=coordinate,source=forcing,response_coordinate=solution['coordinate'],
                    gas=solution['gas'],energy=solution['energy'],work=solution['work'],photon_final=solution['photon'][-1])
                checks.extend(check(f'Response:{model}:m{int(upper*1000)}:{label}:{name}',value,1. if name=='energy_spectrum' else 1e-7)
                    for name,value in errors.items())
                deltas[label]=solution
            closure=response['direct']['gas']-response['linear']['gas']-deltas['first']['gas']-deltas['remaining']['gas']
            scale=np.maximum((abs(response['direct']['gas'])+abs(response['linear']['gas'])+
                abs(deltas['first']['gas'])+abs(deltas['remaining']['gas'])).max(axis=0),1e-300)
            checks.append(check('Gas split closure:'+model+':'+str(upper),np.max(abs(closure)/scale),1e-7))
            operator_error=response['direct']['gas']-response['assembled']['gas']-deltas['operator']['gas']
            operator_scale=np.maximum((abs(response['direct']['gas'])+abs(response['assembled']['gas'])+
                abs(deltas['operator']['gas'])).max(axis=0),1e-300)
            checks.append(check('Gas operator increment closure:'+model+':'+str(upper),np.max(abs(operator_error)/operator_scale),1e-7))
            checks.append(dict(name='Unchanged DC and BR response columns:'+model+':'+str(upper),
                passed=np.array_equal(response['direct']['gas'][:,6:],response['assembled']['gas'][:,6:])))
            conditioning={}
            for label,values in response.items():
                parts=np.stack([values['gas'][-1,offset:offset+3] for offset in [3,6,9]])
                total=values['gas'][-1,:3]
                component_scale=abs(parts).sum(axis=0)
                error=abs(parts.sum(axis=0)-total)/np.maximum(component_scale,1e-300)
                checks.append(check('Gas component closure:'+model+':'+str(upper)+':'+label,np.max(error),1e-7))
                conditioning[label]=dict(endpoint=total.tolist(),component_endpoints=parts.tolist(),
                    absolute_component_sum=component_scale.tolist(),
                    cancellation_factor=(component_scale/np.maximum(abs(total),1e-300)).tolist(),
                    component_scaled_sum_error=error.tolist())
            rows.append(dict(model=model,upper=upper,conditioning=conditioning,
                first_interval_endpoint=deltas['first']['gas'][-1,:3].tolist(),
                remaining_intervals_endpoint=deltas['remaining']['gas'][-1,:3].tolist(),
                operator_increment_endpoint=deltas['operator']['gas'][-1,:3].tolist(),
                direct_minus_linear_endpoint=(response['direct']['gas'][-1,:3]-response['linear']['gas'][-1,:3]).tolist(),
                first_split_gas_closure=float(np.max(abs(closure)/scale)),
                operator_gas_closure=float(np.max(abs(operator_error)/operator_scale))))
    finish(folder,dict(checks=checks,rows=rows,diagnostic_added_after_source_probe=True,
        first_interval_index=0,remaining_sampled_intervals=PROBE_INTERVALS[1:],response_steps=2048,
        new_high_precision=False),__file__,[*inputs,ROOT/'FOLLOWUP.md'])
    print(json.dumps(dict(rows=rows,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
