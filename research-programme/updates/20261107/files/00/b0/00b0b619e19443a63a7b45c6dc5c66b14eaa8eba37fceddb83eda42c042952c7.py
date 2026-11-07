from stage162_common import *


def decimal_tensor(path):
    saved=json.loads(path.read_text())
    return np.array([Decimal(value) for value in saved['values']],dtype=object).reshape(saved['shape'])


def main():
    modest()
    folder=ROOT/'results/conditioning'
    folder.mkdir(parents=True,exist_ok=False)
    preflight=verify_packet(ROOT/'results/preflight')
    raw=verify_packet(ROOT/'results/sources')
    repaired=verify_packet(ROOT/'results/moment-repair')
    data=read_npz(ROOT/'results/sources/source.npz')
    inputs=[ROOT/'results/preflight/status.json',ROOT/'results/sources/status.json',
        ROOT/'results/moment-repair/status.json',ROOT/'results/sources/source.npz']
    checks,records,top_events=[],{},{}
    assert np.array_equal(np.flatnonzero(data['temperature']),[0,1])
    for endpoint in ENDPOINTS:
        theta=preflight['contexts'][endpoint][0]['theta']
        exacts={}
        event_rows={}
        for order in [4,5,6]:
            path=ROOT/'results/moment-repair'/f'{endpoint}-order{order}-moments.json'
            exacts[order]=decimal_tensor(path)
            inputs.append(path)
            event_rows[order]=[]
            with localcontext() as context:
                context.prec=60
                for node in integration_nodes(theta,order):
                    event,weight,path,loop_path=load_node162(endpoint,order,node,theta)
                    inputs.extend([path,loop_path])
                    for component in COMPONENTS:
                        photon=Decimal.from_float(-weight)*Decimal.from_float(float(event[component][0,0]))
                        gas=Decimal.from_float(-weight)*Decimal.from_float(float(event[component][-1,0]))
                        event_rows[order].append(dict(path=str(path),loop_path=str(loop_path),order=order,
                            index=node['index'],component=component,frequency=node['frequency'],cosine=node['cosine'],
                            electron_index=node['electron_index'],photon=str(photon),pair=str(photon+gas)))
        with localcontext() as context:
            context.prec=60
            for step,high,low in [('54',5,4),('65',6,5),('64',6,4)]:
                delta=exacts[high]-exacts[low]
                moments=delta.sum(axis=(0,1))
                pair=delta[:,:,0]+delta[:,:,-1]
                labelled=[dict(row,sign=sign,signed_pair=str(sign*Decimal(row['pair'])))
                    for order,sign in [(high,1),(low,-1)] for row in event_rows[order]]
                exact_pair=sum((Decimal(row['signed_pair']) for row in labelled),Decimal(0))
                test(checks,'Atomwise pair-defect replay:'+endpoint+':'+step,
                    float(abs(exact_pair-(moments[0,0]+moments[-1,0]))/max(abs(exact_pair),Decimal('1e-300'))),1e-10)
                absolute_input=sum((abs(Decimal(row['photon'])) for row in labelled),Decimal(0))
                condition=float(absolute_input/max(abs(moments[0,0]),Decimal('1e-300')))
                ranked=sorted(labelled,key=lambda row:abs(Decimal(row['signed_pair'])),reverse=True)
                selected=ranked[:12]
                top_events[endpoint+'-'+step]=selected
                component_pair=pair.sum(axis=0)
                panel_pair=pair.sum(axis=1)
                old=exacts[low].sum(axis=(0,1))
                new=exacts[high].sum(axis=(0,1))
                records[endpoint+'-'+step]=dict(
                    delta_photon=[str(value) for value in moments[0]],
                    independent_pair_absolute=[str(value) for value in moments[0]+moments[-1]],
                    component_pair_absolute=[[str(value) for value in row] for row in component_pair],
                    panel_pair_absolute=[[str(value) for value in row] for row in panel_pair],
                    atomic_weighted_photon_condition_heavy_join1=condition,
                    epsilon_times_condition_heavy_join1=float(np.finfo(float).eps)*condition,
                    old_full_DVS_pair_relative=[float(abs(old[0,index]+old[-1,index])/max(abs(old[0,index]),Decimal('1e-300'))) for index in range(4)],
                    new_full_DVS_pair_relative=[float(abs(new[0,index]+new[-1,index])/max(abs(new[0,index]),Decimal('1e-300'))) for index in range(4)],
                    interpretation='Exact defect of saved double event values;60digit resumming cannot remove it. Epsilon times condition is an arithmetic sensitivity indicator,not an input-error proof.')
        print(json.dumps(dict(endpoint=endpoint,condition=records[endpoint+'-65']['atomic_weighted_photon_condition_heavy_join1'])),flush=True)
    summary=dict(records=records,top_events=top_events,
        largest_atomic_pair_relative=max(row['pair'] for row in repaired['records'].values()),
        largest_atomic_moment_relative=max(row['moment'] for row in repaired['records'].values()),
        raw_failed_checks=[row for row in raw['checks'] if not row['passed']],
        atomic_failed_checks=[row for row in repaired['checks'] if not row['passed']],
        source_of_residual='Already present in stored event moment values;not solely final aggregation arithmetic.',
        response_propagation_allowed=False,source_tolerance_unchanged=1e-10,
        next_precision_target='Re-evaluate independent photon/electron moment jumps and soft-pole subtraction at the ranked events using a stable or higher-precision physical calculation;then rebuild scalar moments without projecting gas=-photon.')
    write_json(ROOT/'PRECISION-DIAGNOSIS.json',summary)
    finish(folder,dict(checks=checks,diagnosis=summary,precision_diagnostic_complete=True,
        response_propagation_allowed=False),__file__,[*inputs,ROOT/'PRECISION-DIAGNOSIS.json'])
    assert all(row['passed'] for row in checks)
    print(json.dumps(dict(checks=len(checks),complete=True,largest_pair=summary['largest_atomic_pair_relative'])),flush=True)


if __name__=='__main__':
    main()
