from stage165_common import *
from assemble_repair import decimal_array,expand_moments,check_moments


def main():
    modest()
    folder=ROOT/'results/sources-refined'
    legacy_folder=ROOT/'results/legacy-update-refined'
    folder.mkdir(parents=True,exist_ok=False)
    legacy_folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    assert proof['all_checks_passed']
    parent_path=PARENT/'results/sources/source.npz'
    data=read_npz(parent_path)
    frozen=read_npz(SOURCE162/'results/preflight/frozen-reference.npz')
    inputs=[ROOT/'results/preflight/status.json',parent_path,SOURCE162/'results/preflight/frozen-reference.npz']
    checks,legacy_checks,records,legacy_records=[],[],{},{}
    panels,exacts,updates,fulls,deltas={},{},{},{},{}
    low_indices=[0,1,2,97]
    measure=SourceNorm(data['mass'])
    with localcontext() as context:
        context.prec=80
        for endpoint in ENDPOINTS:
            assert verify_packet(ROOT/'runs/refined'/endpoint)['all_checks_passed']
            inputs.append(ROOT/'runs/refined'/endpoint/'status.json')
            bundle=EpochBundle(ENDPOINTS[endpoint])
            inputs.extend(bundle.inputs)
            theta=proof['contexts'][endpoint][0]['theta']
            exacts[endpoint]={}
            for order in [4,5,6]:
                packet=ROOT/'runs'/endpoint/f'order{order}'
                assert verify_packet(packet)['all_checks_passed']
                inputs.append(packet/'status.json')
                primitive=np.empty((7,3,3,4),dtype=object)
                primitive.fill(Decimal(0))
                for node in integration_nodes(theta,order):
                    base_path=moment_path(endpoint,order,node['index'])
                    path=ROOT/'runs/refined'/endpoint/f'order{order}'/'nodes'/f'{node["index"]//500:03d}'/f'{node["index"]:05d}.npz'
                    base=read_npz(base_path)
                    required=bool(np.any(base['difference'][0]+base['difference'][-1]!=0))
                    assert path.exists()==required
                    if not required:
                        path=base_path
                    event=read_npz(path)
                    if required:
                        assert str(event['base_sha256'])==digest(base_path)
                        assert np.array_equal(event['virtual'],base['virtual']) and np.array_equal(event['state'],base['state'])
                    inputs.append(base_path)
                    old_path=parent164.moment_path(endpoint,order,node['index'])
                    old=read_npz(old_path)
                    parameters,weight=parameters_and_weight(theta,node)
                    assert float(event['weight'])==weight and json.loads(str(event['identity']))==node
                    assert str(event['parent_sha256'])==digest(old_path)
                    assert float(event['state_pair_exact'])<1e-10 and float(event['virtual_pair_exact'])<1e-10
                    panel=int(np.searchsorted(BOUNDARIES,node['frequency'])-1)
                    for component_index,component in enumerate(COMPONENTS):
                        primitive[panel,component_index]+=Decimal.from_float(-weight)*decimal_array(event[component])
                    inputs.extend([path,old_path])
                lower=expand_moments(primitive,bundle.basis)
                exacts[endpoint][order]=lower
                old_panel_path=SOURCE162/'results/sources'/f'{endpoint}-order{order}-panels.npz'
                previous=read_npz(old_panel_path)
                inputs.append(old_panel_path)
                repaired=previous['panels'].copy()
                repaired[:,:,low_indices,:]=np.asarray(lower,dtype=float)
                assert np.array_equal(repaired[:,:,3:97],previous['panels'][:,:,3:97])
                panels[(endpoint,order)]=repaired
                write_json(folder/f'{endpoint}-order{order}-moments.json',dict(shape=list(lower.shape),moments=low_indices,
                    decimal_precision=80,values=[str(value) for value in lower.flat],primitive_shape=list(primitive.shape),
                    primitive_values=[str(value) for value in primitive.flat]))
                np.savez_compressed(folder/f'{endpoint}-order{order}-panels.npz',panels=repaired,theta=theta)
                checks.append(dict(name=f'Precise virtual/state certified and higher spectral rows unchanged:{endpoint}:{order}',passed=True))
            old_exact_path=SOURCE162/'results/moment-repair'/f'{endpoint}-order4-moments.json'
            old_json=json.loads(old_exact_path.read_text())
            old_exact=np.array([Decimal(value) for value in old_json['values']],dtype=object).reshape(old_json['shape'])
            old_panels=read_npz(SOURCE162/'results/sources'/f'{endpoint}-order4-panels.npz')['panels']
            inputs.append(old_exact_path)
            update_exacts={}
            for order in [4,5,6]:
                update=stable_sum((panels[(endpoint,order)]-old_panels).reshape(-1,98,4))
                update_exact=(exacts[endpoint][order]-old_exact).sum(axis=(0,1))
                update[low_indices]=np.asarray(update_exact,dtype=float)
                full=frozen[endpoint]+update
                full_exact=decimal_array(frozen[endpoint][low_indices])+update_exact
                full[low_indices]=np.asarray(full_exact,dtype=float)
                updates[(endpoint,order)]=update
                fulls[(endpoint,order)]=full
                update_exacts[order]=update_exact
                data[f'soft_{endpoint}_source{order}']=full
                data[f'soft_{endpoint}_update{order}']=update
                check_moments(checks,records,f'{endpoint}:source{order}',full_exact,full,data['temperature'])
                if order in [5,6]:
                    check_moments(legacy_checks,legacy_records,f'{endpoint}:update{order}-saved4',update_exact,update,data['temperature'])
                write_json(folder/f'{endpoint}-source{order}-exact.json',dict(
                    low_shape=[4,4],full=[str(value) for value in full_exact.flat],
                    update=[str(value) for value in update_exact.flat],saved=[str(value) for value in decimal_array(frozen[endpoint][low_indices]).flat]))
            for step,high,low in [('54',5,4),('65',6,5),('64',6,4)]:
                delta=panels[(endpoint,high)]-panels[(endpoint,low)]
                delta_exact=exacts[endpoint][high]-exacts[endpoint][low]
                delta[:,:,low_indices,:]=np.asarray(delta_exact,dtype=float)
                total=stable_sum(delta.reshape(-1,98,4))
                total_exact=delta_exact.sum(axis=(0,1))
                total[low_indices]=np.asarray(total_exact,dtype=float)
                data[f'soft_{endpoint}_total{step}']=total
                deltas[(endpoint,step)]=delta
                check_moments(checks,records,f'{endpoint}:step{step}',total_exact,total,data['temperature'])
            close(checks,'Repaired physical order telescope:'+endpoint,
                data[f'soft_{endpoint}_total54']+data[f'soft_{endpoint}_total65'],data[f'soft_{endpoint}_total64'],1e-10)
            close(checks,'Reference arithmetic plus physical increment:'+endpoint,
                updates[(endpoint,4)]+data[f'soft_{endpoint}_total64'],updates[(endpoint,6)],1e-10)
            print(json.dumps(dict(endpoint=endpoint,failed=[row for row in checks if not row['passed']],legacy_failed=sum(not row['passed'] for row in legacy_checks))),flush=True)
    for order in [4,5,6]:
        data[f'soft_endpoint_panels{order}']=np.stack([panels[(endpoint,order)] for endpoint in ENDPOINTS],axis=1)
    for step in ['54','65','64']:
        data[f'soft_endpoint_delta{step}']=np.stack([deltas[(endpoint,step)] for endpoint in ENDPOINTS],axis=1)
    prediction_records={}
    for route in ['local','cubic']:
        prediction=old_prediction162(frozen,route)
        current=frozen['after_band820_full'][0]
        prediction_records[route]={}
        for order in [4,5,6]:
            correction=sum(endpoint_basis(.75,route,endpoint)*updates[(endpoint,order)] for endpoint in ENDPOINTS)
            error=current-prediction-correction
            data[f'soft_{route}_error{order}']=error
            prediction_records[route][str(order)]=(measure(error)/measure(current)).tolist()
    prior=read_npz(parent_path)
    assert all(np.array_equal(data[key],prior[key]) for key in prior if not key.startswith('soft_'))
    checks.append(dict(name='Every non-soft inherited source and improved-band array retained bitwise',passed=True))
    np.savez_compressed(folder/'source.npz',**data)
    summary=dict(stage=165,events=7560,source_precision=records,predictions=prediction_records,
        physical_source_checks_passed=all(row['passed'] for row in checks),
        legacy_raw_update_checks_passed=all(row['passed'] for row in legacy_checks),
        legacy_failed_checks=[row for row in legacy_checks if not row['passed']],
        adaptive_real_shift_repair=True,refined_real_events=474,temperature_curve_changed=False,improved_bands=[6,6,6,8,7,7,6],virtual_state_reused=False,expensive_virtual_coefficients_reused=True,
        response_propagation_allowed=False,reference_history_reconciled=False)
    write_json(ROOT/'SOURCE-SUMMARY-REFINED.json',summary)
    finish(folder,dict(checks=checks,summary=summary),__file__,[*inputs,folder/'source.npz',ROOT/'SOURCE-SUMMARY-REFINED.json'])
    finish(legacy_folder,dict(checks=legacy_checks,records=legacy_records,tolerance=1e-10,
        direct_update_from_unrepaired_history_allowed=all(row['passed'] for row in legacy_checks),
        original_failures_not_reclassified=True),__file__,[folder/'source.npz',folder/'status.json'])
    print(json.dumps(dict(source_checks=len(checks),failed=sum(not row['passed'] for row in checks),
        legacy_failed=sum(not row['passed'] for row in legacy_checks))),flush=True)


if __name__=='__main__':
    main()
