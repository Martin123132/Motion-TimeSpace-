from connection208 import *


def main():
    config=protocol()
    manifest=read(ROOT/'frozen/prediction-manifest.json')
    assert digest(ROOT/'configuration.json')==manifest['configuration_sha256']
    original,unused=source.context(config['target_fraction'])
    factor=linear.cholesky(original.basis.mass,lower=True)
    measurements=[('photon',lambda values:metrics.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]
    completed={}
    checks=list(read(ROOT/'results/preparation.json')['checks'])
    all_direct=[]
    all_predictions={'quadratic':[],'linear':[]}
    event_count=0
    for frequency_index,item in enumerate(config['panel']):
        paths=[ROOT/f'events/frequency-{frequency_index}/event-{event:02d}.npz' for event in range(36)]
        if not all(path.exists() for path in paths):continue
        direct=[]
        predicted={'quadratic':[],'linear':[]}
        for event_index,path in enumerate(paths):
            record=read(path.with_suffix('.json'))
            assert digest(path)==record['sha256'] and not record['failed_checks']
            assert digest(record['loop_path'])==record['loop_sha256']
            assert datetime.fromisoformat(record['started_at'])>datetime.fromisoformat(manifest['frozen_at'])
            values=packet(path)
            assert float(values['theta'])==config['theta']
            expected=next(row for row in config['events'] if row['frequency_index']==frequency_index and row['event']==event_index)
            assert json.loads(str(values['node']))==expected['node']
            unused,weight=source.physics.parameters_and_weight(config['theta'],expected['node'])
            assert float(values['weight'])==weight
            direct.append((values['high'][:2],values['low'][:2]))
            frozen=packet(ROOT/f'frozen/frequency-{frequency_index}/event-{event_index:02d}.npz')
            for method in predicted:
                predicted[method].append((frozen[method+'_high'],frozen[method+'_low']))
            checks.extend(dict(row,name=f'{frequency_index}:{event_index}:'+row['name']) for row in record['checks'])
        event_count+=36
        all_direct.extend(direct)
        for method in predicted:all_predictions[method].extend(predicted[method])
        completed[str(frequency_index)]=dict(frequency=item['frequency'],actual=metrics.primitives(direct),
                                           predicted={method:metrics.primitives(pairs) for method,pairs in predicted.items()})
    assert completed,'No complete frequency node is ready for aggregate assessment'
    full=len(completed)==7
    if full:
        completed['full-seven']=dict(frequency=None,actual=metrics.primitives(all_direct),
                                     predicted={method:metrics.primitives(pairs) for method,pairs in all_predictions.items()})
    records=[]
    for scope,collection in completed.items():
        actual=collection['actual']
        for method,predicted in collection['predicted'].items():
            error=metrics.subtract(predicted,actual)
            for measure,operation in measurements:
                relative=operation(error[0]+error[1])/np.maximum(operation(actual[0]+actual[1]),1e-300)
                for grid,component,column in np.ndindex(relative.shape):
                    entry=dict(scope=scope,frequency=collection['frequency'],method=method,grid=GRIDS[grid],component=COMPONENTS[component],
                               model=('heavy','cold')[column//2],join=column%2,measure=measure,relative=float(relative[grid,component,column]))
                    records.append(entry)
                    if method=='quadratic':
                        check(checks,f'{scope}:{grid}:{component}:{column}:{measure}:primary forecast',relative[grid,component,column],.01,'prediction')
        difference=metrics.subtract((actual[0][0],actual[1][0]),(actual[0][1],actual[1][1]))
        for measure,operation in measurements:
            relative=operation(difference[0]+difference[1])/np.maximum(operation(actual[0][1]+actual[1][1]),1e-300)
            for component,column in np.ndindex(relative.shape):
                check(checks,f'{scope}:{component}:{column}:{measure}:history mesh',relative[component,column],.01,'mesh')
        energy=actual[0][...,0,:]+actual[1][...,0,:]
        gas=actual[0][...,-1,:]+actual[1][...,-1,:]
        relative=abs(energy+gas)/np.maximum(abs(energy),1e-300)
        check(checks,scope+':photon-gas energy exchange',relative.max(),1e-10,'identity')
        save(ROOT/f'results/source-{scope}.npz',high=actual[0],low=actual[1],frequencies=np.array([item['frequency'] for item in config['panel']] if scope=='full-seven' else [collection['frequency']]))
        if scope=='full-seven':
            for method,predicted in collection['predicted'].items():
                frozen=packet(ROOT/f'frozen/{method}-panel.npz')
                error=metrics.subtract(predicted,(frozen['high'],frozen['low']))
                check(checks,method+':full frozen sum regrouping',metrics.norms(error[0]+error[1],factor).max()/max(metrics.norms(predicted[0]+predicted[1],factor).max(),1e-300),1e-10,'identity')
    failed=[row for row in checks if not row['passed']]
    report=dict(stage=208,state='forecast_rejected' if failed else 'full_band_qualified' if full else 'partial_nodes_qualified',
                checks=checks,failed_checks=failed,records=records,completed_frequency_indices=[key for key in completed if key!='full-seven'],
                complete_band=full,completed_events=event_count,primary_prediction='quadratic',secondary_prediction='linear diagnostic',
                permission_to_propagate=full and not failed,source_prediction_tolerance=.01,identity_tolerance=1e-10,
                original_bank_changed=False,global_curve_changed=False,weights_reapplied=False)
    destination=ROOT/f'results/assessment-{event_count:03d}.json'
    assert not destination.exists()
    write(destination,report)
    write(ROOT/'progress.json',dict(state=report['state'],completed_events=event_count,total=252,assessment_path=str(destination),
                                   permission_to_propagate=report['permission_to_propagate']))
    print(json.dumps(dict(state=report['state'],events=event_count,checks=len(checks),failed=len(failed),
        worst_primary=max(row['relative'] for row in records if row['method']=='quadratic'),
        worst_linear=max(row['relative'] for row in records if row['method']=='linear'))),flush=True)


if __name__=='__main__':
    source.modest()
    main()
