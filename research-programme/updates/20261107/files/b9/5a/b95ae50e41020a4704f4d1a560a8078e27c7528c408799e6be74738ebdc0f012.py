from stage163_common import *


def decimal_array(values):
    return np.asarray([Decimal.from_float(float(value)) for value in np.asarray(values).flat],dtype=object).reshape(np.asarray(values).shape)


def expand_moments(primitive,basis):
    photon,number,gas=np.moveaxis(primitive,-2,0)
    norm0,norm1=map(lambda value:Decimal.from_float(float(value)),basis.norms[:2])
    mean=Decimal.from_float(float(basis.mean))
    return np.stack([photon,number/norm0,(photon-mean*number)/norm1,gas],axis=-2)


def check_moments(checks,records,label,exact,rounded,temperature):
    moments=exact if exact.shape==(4,4) else exact[[0,1,2,97]]
    for column in range(4):
        photon,first,second,gas=moments[:,column]
        spectral=Decimal.from_float(float(temperature[0]))*first+Decimal.from_float(float(temperature[1]))*second
        scale=max(abs(photon),Decimal('1e-300'))
        pair=float(abs(photon+gas)/scale)
        moment=float(abs(spectral-photon)/scale)
        rounded_pair=float(abs(rounded[0,column]+rounded[-1,column])/max(abs(rounded[0,column]),1e-300))
        rounded_moment=float(abs(temperature@rounded[1:-1,column]-rounded[0,column])/max(abs(rounded[0,column]),1e-300))
        name=label+':'+str(column)
        test(checks,'60digit independent photon/gas:'+name,pair,1e-10)
        test(checks,'60digit unprojected spectral moment:'+name,moment,1e-10)
        test(checks,'Float independent photon/gas:'+name,rounded_pair,1e-10)
        test(checks,'Float unprojected spectral moment:'+name,rounded_moment,1e-10)
        records[name]=dict(pair=pair,moment=moment,rounded_pair=rounded_pair,rounded_moment=rounded_moment,
            photon=str(photon),gas=str(gas),number_condition=float((abs(first)+abs(second))/scale))


def main():
    modest()
    folder=ROOT/'results/sources'
    folder.mkdir(parents=True,exist_ok=False)
    proof=verify_packet(ROOT/'results/preflight')
    assert proof['all_checks_passed']
    source_path=PARENT/'results/sources/source.npz'
    data=read_npz(source_path)
    frozen=read_npz(PARENT/'results/preflight/frozen-reference.npz')
    inputs=[ROOT/'results/preflight/status.json',source_path,PARENT/'results/preflight/frozen-reference.npz']
    checks,records,panels,exacts,fulls,deltas,updates=[],{},{},{},{},{},{}
    mass=SourceNorm(data['mass'])
    low_indices=[0,1,2,97]
    diagnostics={}
    with localcontext() as context:
        context.prec=60
        for endpoint in ENDPOINTS:
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
                absolute=np.zeros((7,3,3,4))
                for node in integration_nodes(theta,order):
                    path=moment_path(endpoint,order,node['index'])
                    event=read_npz(path)
                    old,weight,old_path,loop_path=parent162.load_node162(endpoint,order,node,theta)
                    assert json.loads(str(event['identity']))==node and float(event['weight'])==weight
                    assert str(event['old_sha256'])==digest(old_path) and str(event['loop_sha256'])==digest(loop_path)
                    panel=int(np.searchsorted(BOUNDARIES,node['frequency'])-1)
                    factor=Decimal.from_float(-weight)
                    for component_index,component in enumerate(COMPONENTS):
                        primitive[panel,component_index]+=factor*decimal_array(event[component])
                        absolute[panel,component_index]+=weight*abs(event[component])
                    inputs.extend([path,old_path,loop_path])
                low=expand_moments(primitive,bundle.basis)
                exacts[endpoint][order]=low
                prior_panel_path=PARENT/'results/sources'/f'{endpoint}-order{order}-panels.npz'
                previous=read_npz(prior_panel_path)
                inputs.append(prior_panel_path)
                repaired=previous['panels'].copy()
                repaired[:,:,low_indices,:]=np.asarray(low,dtype=float)
                assert np.array_equal(repaired[:,:,3:97],previous['panels'][:,:,3:97])
                panels[(endpoint,order)]=repaired
                write_json(folder/f'{endpoint}-order{order}-moments.json',dict(shape=list(low.shape),moments=low_indices,
                    decimal_precision=60,values=[str(value) for value in low.flat],
                    primitive_shape=list(primitive.shape),primitive_values=[str(value) for value in primitive.flat]))
                np.savez_compressed(folder/f'{endpoint}-order{order}-panels.npz',panels=repaired,
                    primitive_absolute_terms=absolute,theta=theta)
                checks.append(dict(name=f'Bitwise inherited higher spectral panel rows:{endpoint}:{order}',passed=True))
            old_moment_path=PARENT/'results/moment-repair'/f'{endpoint}-order4-moments.json'
            old_moment_json=json.loads(old_moment_path.read_text())
            old_moments=np.array([Decimal(value) for value in old_moment_json['values']],dtype=object).reshape(old_moment_json['shape'])
            inputs.append(old_moment_path)
            old_panels=read_npz(PARENT/'results/sources'/f'{endpoint}-order4-panels.npz')['panels']
            for order in [4,5,6]:
                update=stable_sum((panels[(endpoint,order)]-old_panels).reshape(-1,98,4))
                update_exact=(exacts[endpoint][order]-old_moments).sum(axis=(0,1))
                update[low_indices]=np.asarray(update_exact,dtype=float)
                full=frozen[endpoint]+update
                full_exact=decimal_array(frozen[endpoint][low_indices])+update_exact
                full[low_indices]=np.asarray(full_exact,dtype=float)
                fulls[(endpoint,order)]=full
                updates[(endpoint,order)]=update
                check_moments(checks,records,f'{endpoint}:source{order}',full_exact,full,data['temperature'])
                if order in [5,6]:
                    check_moments(checks,records,f'{endpoint}:update{order}-saved4',update_exact,update,data['temperature'])
            for step,high,low in [('54',5,4),('65',6,5),('64',6,4)]:
                delta=panels[(endpoint,high)]-panels[(endpoint,low)]
                delta_exact=exacts[endpoint][high]-exacts[endpoint][low]
                delta[:,:,low_indices,:]=np.asarray(delta_exact,dtype=float)
                total=stable_sum(delta.reshape(-1,98,4))
                total_exact=delta_exact.sum(axis=(0,1))
                total[low_indices]=np.asarray(total_exact,dtype=float)
                deltas[(endpoint,step)]=delta
                check_moments(checks,records,f'{endpoint}:step{step}',total_exact,total,data['temperature'])
                data[f'repaired_{endpoint}_total{step}']=total
            close(checks,'Repaired endpoint step telescope:'+endpoint,
                data[f'repaired_{endpoint}_total54']+data[f'repaired_{endpoint}_total65'],data[f'repaired_{endpoint}_total64'],1e-10)
            close(checks,'Order4 repair included in full update:'+endpoint,
                updates[(endpoint,4)]+data[f'repaired_{endpoint}_total64'],updates[(endpoint,6)],1e-10)
            for order in [4,5,6]:
                data[f'repaired_{endpoint}_source{order}']=fulls[(endpoint,order)]
                data[f'repaired_{endpoint}_update{order}']=updates[(endpoint,order)]
            diagnostics[endpoint]=dict(theta=theta,source4_repair_over_saved=(mass(updates[(endpoint,4)])/mass(frozen[endpoint])).tolist(),
                source6_update_over_saved=(mass(updates[(endpoint,6)])/mass(frozen[endpoint])).tolist(),
                step65_over_step54=(mass(data[f'repaired_{endpoint}_total65'])/mass(data[f'repaired_{endpoint}_total54'])).tolist())
            print(json.dumps(dict(endpoint=endpoint,failed=[row for row in checks if not row['passed']])),flush=True)
    for order in [4,5,6]:
        data[f'repaired_endpoint_panels{order}']=np.stack([panels[(endpoint,order)] for endpoint in ENDPOINTS],axis=1)
    for step in ['54','65','64']:
        data[f'repaired_endpoint_delta{step}']=np.stack([deltas[(endpoint,step)] for endpoint in ENDPOINTS],axis=1)
    predictions={}
    for route in ['local','cubic']:
        prediction=old_prediction162(frozen,route)
        current=frozen['after_band820_full'][0]
        values={}
        for order in [4,5,6]:
            correction=sum(endpoint_basis(.75,route,endpoint)*updates[(endpoint,order)] for endpoint in ENDPOINTS)
            error=current-prediction-correction
            data[f'repaired_{route}_error{order}']=error
            values[str(order)]=(mass(error)/mass(current)).tolist()
        predictions[route]=values
    for key in frozen:
        assert np.array_equal(data[key],frozen[key]),key
    checks.append(dict(name='Every inherited frozen source array unchanged',passed=True))
    allowed=all(row['passed'] for row in checks)
    failures=[row for row in checks if not row['passed']]
    np.savez_compressed(folder/'source.npz',**data)
    summary=dict(stage=163,events=7560,new_virtual_coefficients=0,endpoint_orders=[4,5,6],
        interior_orders=[6,6,6,8,7,7,6],diagnostics=diagnostics,precision=records,predictions=predictions,
        source_readiness_passed=allowed,response_propagation_allowed=allowed,failed_checks=failures,
        gas_equals_minus_photon_enforced=False,temperature_curve_changed=False,lower_bands_changed=False,
        all_higher_spectral_rows_reused=True,arithmetic_repair4_included=True)
    write_json(ROOT/'SOURCE-SUMMARY.json',summary)
    finish(folder,dict(checks=checks,summary=summary,response_propagation_allowed=allowed),__file__,
        [*inputs,folder/'source.npz',ROOT/'SOURCE-SUMMARY.json'])
    print(json.dumps(dict(source_complete=True,checks=len(checks),failed=len(failures),propagation_allowed=allowed,
        max_pair=max(row['pair'] for row in records.values()),max_spectral=max(row['moment'] for row in records.values()))),flush=True)


if __name__=='__main__':
    main()
