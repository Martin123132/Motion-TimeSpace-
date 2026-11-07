from source202 import *
from decimal import Decimal,localcontext


def observed_increment(absolute):
    pairs=[combine([(absolute[0][group],absolute[1][group]),(-absolute[0][0],-absolute[1][0])]) for group in (1,2)]
    return np.stack([pair[0] for pair in pairs]),np.stack([pair[1] for pair in pairs])


def records_for(scope,label,relative,rows,limit,category,extra=None):
    records=[]
    for index in np.ndindex(relative.shape):
        check(rows,f'{scope}:{label}:{index}',relative[index],limit,category)
        if len(index)==3:
            grid,component,column=index
            record=dict(grid=GRIDS[grid])
        else:
            component,column=index
            record={}
        record.update(scope=scope,component=COMPONENTS[component],model=('heavy','cold')[column//2],join=column%2,
            relative=float(relative[index]),test=label)
        if extra:record.update(extra)
        records.append(record)
    return records


def assess_scope(scope,predicted,absolute,parts,factor,rows):
    photon_norm=lambda values:metrics.norms(values,factor)
    measurements=[('photon',photon_norm),('gas',lambda values:abs(values[...,-1,:]))]
    observed=observed_increment(absolute)
    error=metrics.subtract(predicted,observed)
    records=[];mesh_records=[];decompositions=[]
    for name,measure in measurements:
        denominator=measure(observed[0]+observed[1])
        check(rows,scope+':'+name+':nonzero small corrections',int(not np.all(denominator>0)),0,'negative_control')
        relative=measure(error[0]+error[1])/np.maximum(denominator,1e-300)
        records.extend(records_for(scope,'frozen correction',relative,rows,.01,'prediction',dict(measure=name)))
        absolute_scale=np.maximum(measure(absolute[0][1:]+absolute[1][1:]),measure(absolute[0][0]+absolute[1][0]))
        reconstruction=measure(error[0]+error[1])/np.maximum(absolute_scale,1e-300)
        records_for(scope,'absolute reconstruction:'+name,reconstruction,rows,1e-10,'identity')
        increment_mesh=metrics.subtract((predicted[0][0],predicted[1][0]),(predicted[0][1],predicted[1][1]))
        direct_mesh=metrics.subtract((absolute[0][1],absolute[1][1]),(absolute[0][2],absolute[1][2]))
        for method,difference,scale in [('increment',increment_mesh,predicted[0][1]+predicted[1][1]),
                ('absolute_difference',direct_mesh,observed[0][1]+observed[1][1]),
                ('absolute_scale',direct_mesh,absolute[0][2]+absolute[1][2])]:
            relative=measure(difference[0]+difference[1])/np.maximum(measure(scale),1e-300)
            mesh_records.extend(records_for(scope,'mesh:'+method,relative,rows,.01,'mesh',dict(measure=name,method=method)))
    for grid_index,grid in enumerate(GRIDS):
        photon=(parts[0][2*grid_index],parts[1][2*grid_index])
        gas=(parts[0][2*grid_index+1],parts[1][2*grid_index+1])
        combined=combine([photon,gas])
        difference=metrics.subtract(combined,(predicted[0][grid_index],predicted[1][grid_index]))
        for name,measure in measurements:
            denominator=np.maximum(measure(combined[0]+combined[1]),1e-300)
            closure=measure(difference[0]+difference[1])/denominator
            records_for(scope,grid+':photon-gas closure:'+name,closure,rows,1e-10,'identity')
            first=measure(photon[0]+photon[1])/denominator
            second=measure(gas[0]+gas[1])/denominator
            for component,column in np.ndindex(denominator.shape):
                decompositions.append(dict(grid=grid,component=COMPONENTS[component],model=('heavy','cold')[column//2],
                    join=column%2,measure=name,omit_photon_error=float(first[component,column]),
                    omit_gas_error=float(second[component,column]),cancellation_factor=float(first[component,column]+second[component,column])))
    for label,pair in [('absolute',absolute),('predicted_delta',predicted),('observed_delta',observed),('split_parts',parts)]:
        values=pair[0]+pair[1]
        exchange=values[...,0,:]+values[...,-1,:]
        scale=np.maximum(np.maximum(abs(values[...,0,:]),abs(values[...,-1,:])),1e-300)
        for index in np.ndindex(scale.shape):
            check(rows,f'{scope}:{label}:{index}:energy exchange',exchange[index]/scale[index],1e-10,'identity')
        for component,members in [(4,[1,2,3]),(5,[0,1,2,3])]:
            expected=combine([(pair[0][:,member],pair[1][:,member]) for member in members])
            difference=metrics.subtract((pair[0][:,component],pair[1][:,component]),expected)
            for name,measure in measurements:
                relative=measure(difference[0]+difference[1])/np.maximum(measure(expected[0]+expected[1]),1e-300)
                check(rows,f'{scope}:{label}:{component}:{name}:component closure',relative.max(),1e-10,'identity')
    path=ROOT/f'results/{scope}-source.npz'
    save(path,prediction_high=predicted[0],prediction_low=predicted[1],absolute_high=absolute[0],absolute_low=absolute[1],
        delta_high=observed[0],delta_low=observed[1],discrepancy_high=error[0],discrepancy_low=error[1],
        split_high=parts[0],split_low=parts[1],frequencies=np.array([FREQUENCY] if scope=='neighbour' else [14.,FREQUENCY]),
        components=np.array(COMPONENTS),theta=protocol()['theta'])
    return dict(records=records,mesh_records=mesh_records,decompositions=decompositions,
        result_path=str(path),result_sha256=digest(path))


def decimal_samples(label,first,second,combined,rows):
    with localcontext() as context:
        context.prec=100
        for group in range(combined[0].shape[0]):
            for component,row,column in ((0,0,0),(1,48,2),(2,96,0),(3,97,3),(4,1,2),(5,97,0)):
                index=(group,component,row,column)
                expected=sum((Decimal.from_float(float(pair[side][index])) for pair in (first,second) for side in (0,1)),Decimal(0))
                actual=sum((Decimal.from_float(float(combined[side][index])) for side in (0,1)),Decimal(0))
                check(rows,f'{label}:{index}:independent Decimal sum',float(abs(actual-expected)/max(abs(expected),Decimal('1e-300'))),1e-10,'identity')


def main():
    config=protocol();manifest=verify_frozen()
    assert digest(REFERENCE/'results/x14-source.npz')==manifest['reference_prediction_sha256']
    original,theta=source.context(config['target_fraction'])
    factor=linear.cholesky(original.basis.mass,lower=True)
    rows=list(read(ROOT/'results/preparation.json')['checks'])
    prediction_events=[];absolute_events=[];part_events=[];event_diagnostics=[]
    frozen_time=datetime.fromisoformat(manifest['frozen_utc'])
    for index,node in enumerate(config['nodes']):
        for kind in ('prediction','actual'):
            path=ROOT/f'{kind}/event-{index:02d}.npz'
            record=read(path.with_suffix('.json'))
            assert digest(path)==record['sha256'] and not record['failed_checks']
            assert digest(record['loop_path'])==record['loop_sha256'] and record['new_virtual_integrals']==0
            rows.extend(dict(row,name=f'{kind}:{index}:'+row['name']) for row in record['checks'])
            values=packet(path)
            assert json.loads(str(values['node']))==node and float(values['theta'])==theta
            unused,weight=source.physics.parameters_and_weight(theta,node)
            check(rows,f'{kind}:{index}:original weight applied once',int(float(values['weight'])!=weight),0,'integrity')
            if kind=='actual':
                check(rows,f'{index}:all predictions frozen before actual start',int(datetime.fromisoformat(record['started_utc'])<=frozen_time),0,'integrity')
        prediction=packet(ROOT/f'frozen/event-{index:02d}-prediction.npz')
        actual=packet(ROOT/f'actual/event-{index:02d}.npz')
        parts=packet(ROOT/f'prediction/event-{index:02d}.npz')
        predicted=(prediction['high'],prediction['low'])
        absolute=(actual['high'],actual['low'])
        prediction_events.append(predicted);absolute_events.append(absolute)
        part_events.append((parts['high'][:4],parts['low'][:4]))
        observed=observed_increment(absolute)
        error=metrics.subtract(predicted,observed)
        photon_norm=lambda values:metrics.norms(values,factor)
        scale=np.maximum(photon_norm(actual['high'][1:]+actual['low'][1:]),photon_norm(actual['high'][0]+actual['low'][0]))
        records_for('event'+str(index),'absolute reconstruction',photon_norm(error[0]+error[1])/np.maximum(scale,1e-300),rows,1e-10,'identity')
        event_diagnostics.append(dict(event=index,maximum_photon_relative=float((photon_norm(error[0]+error[1])/np.maximum(photon_norm(observed[0]+observed[1]),1e-300)).max()),
            maximum_gas_relative=float((abs(error[0][...,-1,:]+error[1][...,-1,:])/np.maximum(abs(observed[0][...,-1,:]+observed[1][...,-1,:]),1e-300)).max()),aggregate_gate_applied_here=False))
    new=dict(prediction=metrics.primitives(prediction_events),absolute=metrics.primitives(absolute_events),split=metrics.primitives(part_events))
    reference_packet=packet(REFERENCE/'results/x14-source.npz')
    reference={label:(reference_packet[label+'_high'],reference_packet[label+'_low']) for label in ('prediction','absolute','split')}
    paired={label:metrics.primitives([reference[label],new[label]]) for label in new}
    for label in new:
        decimal_samples(label,reference[label],new[label],paired[label],rows)
    summaries={}
    for scope,collection in [('neighbour',new),('two-frequency',paired)]:
        frozen=packet(ROOT/f'frozen/{scope}-prediction.npz')
        for side,name in enumerate(('high','low')):
            check(rows,scope+':frozen aggregate '+name+' reproduced bitwise',int(not np.array_equal(collection['prediction'][side],frozen[name])),0,'integrity')
        summaries[scope]=assess_scope(scope,(frozen['high'],frozen['low']),collection['absolute'],collection['split'],factor,rows)
    cancellation=[]
    for name,measure in [('photon',lambda values:metrics.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]:
        first=reference['prediction'][0]+reference['prediction'][1]
        second=new['prediction'][0]+new['prediction'][1]
        combined=paired['prediction'][0]+paired['prediction'][1]
        ratios=(measure(first)+measure(second))/np.maximum(measure(combined),1e-300)
        for grid,component,column in np.ndindex(ratios.shape):
            cancellation.append(dict(grid=GRIDS[grid],component=COMPONENTS[component],model=('heavy','cold')[column//2],join=column%2,
                measure=name,cancellation_factor=float(ratios[grid,component,column])))
    check(rows,'frequency weights not reapplied or renormalized',int(config['frequency_weights_reapplied'] or config['partial_panel_normalized']),0,'integrity')
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/source-assessment.json',dict(checks=rows,failed_checks=failed,qualified=not failed,
        scopes=summaries,event_diagnostics=event_diagnostics,node_cancellation=cancellation,new_events=36,reused_reference_events=36,
        packets_already_frequency_weighted=True,frequency_weights_reapplied=False,partial_panel_normalized=False,
        full_frequency_panel_qualified=False,new_virtual_integrals=0,shared_evaluator=True,observational_prediction=False))
    write(ROOT/'progress.json',dict(state='qualified' if not failed else 'checks_failed',failed_checks=len(failed)))
    print(json.dumps(dict(checks=len(rows),failed=failed,summary={scope:dict(worst_prediction=max(row['relative'] for row in value['records']),
        worst_mesh=max(row['relative'] for row in value['mesh_records'])) for scope,value in summaries.items()})),flush=True)


if __name__=='__main__':
    source.modest()
    main()
