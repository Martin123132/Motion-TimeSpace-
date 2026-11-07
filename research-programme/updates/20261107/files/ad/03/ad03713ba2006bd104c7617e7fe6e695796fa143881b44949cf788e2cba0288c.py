from operator212 import *


def main():
    config=protocol()
    manifest=verify_prediction(config)
    assert digest(config['reference_source_path'])==config['reference_source_sha256']
    reference=packet(config['reference_source_path'])
    original,unused=source.context(config['target_fraction'])
    factor=linear.cholesky(original.basis.mass,lower=True)
    measurements=[('photon',lambda values:metrics.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]
    checks=list(read(ROOT/'results/preparation.json')['checks'])
    for row in config['anchors']:
        values,report=verify_event(event_path('anchors',row))
        checks.extend(dict(entry,name=f"{row['frequency_index']}:{row['label']}:{row['event']}:"+entry['name']) for entry in report['checks'])
    nodes={}
    event_diagnostics=[]
    cumulative_actual=(reference['actual_high'],reference['actual_low'])
    cumulative_prediction=(reference['predicted_high'],reference['predicted_low'])
    scopes=[]
    for ordinal,frequency in enumerate(config['frequencies']):
        selected=[row for row in config['target'] if row['frequency']==frequency]
        frequency_index=selected[0]['frequency_index']
        direct=[]
        forecasts=[]
        for row in selected:
            values,report=verify_event(event_path('target',row))
            assert datetime.fromisoformat(report['started_at'])>datetime.fromisoformat(manifest['frozen_at'])
            assert report['coefficients_sha256']==digest(ROOT/'frozen/history-coefficients.npz')
            assert json.loads(str(values['node']))==row['node']
            assert float(values['theta'])==config['theta'] and float(values['weight'])==row['weight']
            checks.extend(dict(entry,name=f"target:{frequency_index}:{row['event']}:"+entry['name']) for entry in report['checks'])
            actual=(values['high'],values['low'])
            frozen=packet(ROOT/f"frozen/prediction/frequency-{frequency_index}/event-{row['event']:02d}.npz")
            predicted=(frozen['high'],frozen['low'])
            direct.append(actual)
            forecasts.append(predicted)
            difference=metrics.subtract(predicted,actual)
            for name,measure in measurements:
                relative=measure(difference[0][:2]+difference[1][:2])/np.maximum(measure(actual[0][:2]+actual[1][:2]),1e-300)
                event_diagnostics.append(dict(frequency=frequency,event=row['event'],measure=name,worst_relative=float(relative.max()),used_as_primary_gate=False))
        actual=metrics.primitives(direct)
        predicted=metrics.primitives(forecasts)
        nodes[frequency_index]=dict(actual=actual,predicted=predicted)
        cumulative_actual=metrics.primitives([cumulative_actual,actual])
        cumulative_prediction=metrics.primitives([cumulative_prediction,predicted])
        scopes.append((f'node-{frequency_index}',actual,predicted,f'predicted-node-{frequency_index}.npz',[frequency]))
        scopes.append((f'sum-{ordinal+5}',cumulative_actual,cumulative_prediction,f'predicted-sum-{ordinal+5}.npz',config['reference_frequencies']+config['frequencies'][:ordinal+1]))
    records=[]
    mesh_records=[]
    for scope,actual,predicted,frozen_name,frequencies in scopes:
        frozen=packet(ROOT/'frozen'/frozen_name)
        for index,name in enumerate(('high','low')):
            check(checks,scope+':frozen aggregate bitwise '+name,int(not np.array_equal(predicted[index],frozen[name])),0,'integrity')
        error=metrics.subtract(predicted,actual)
        for name,measure in measurements:
            relative=measure(error[0][:2]+error[1][:2])/np.maximum(measure(actual[0][:2]+actual[1][:2]),1e-300)
            for grid,component,column in np.ndindex(relative.shape):
                value=float(relative[grid,component,column])
                records.append(dict(scope=scope,grid=GRIDS[grid],component=COMPONENTS[component],model=('heavy','cold')[column//2],
                                    join=column%2,measure=name,relative=value))
                check(checks,f'{scope}:{grid}:{component}:{column}:{name}:forecast',value,.01,'prediction')
            for label,pair in [('actual',actual),('predicted',predicted)]:
                difference=metrics.subtract((pair[0][0],pair[1][0]),(pair[0][1],pair[1][1]))
                relative_mesh=measure(difference[0]+difference[1])/np.maximum(measure(pair[0][1]+pair[1][1]),1e-300)
                for component,column in np.ndindex(relative_mesh.shape):
                    value=float(relative_mesh[component,column])
                    mesh_records.append(dict(scope=scope,source=label,component=COMPONENTS[component],model=('heavy','cold')[column//2],
                                             join=column%2,measure=name,relative=value))
                    check(checks,f'{scope}:{label}:{component}:{column}:{name}:mesh',value,.01,'mesh')
        for label,pair in [('actual',actual),('predicted',predicted),('error',error)]:
            energy=pair[0][...,0,:]+pair[1][...,0,:]
            gas=pair[0][...,-1,:]+pair[1][...,-1,:]
            residual=abs(energy+gas)/np.maximum(np.maximum(abs(energy),abs(gas)),1e-300)
            check(checks,scope+':'+label+':energy exchange',residual.max(),1e-10,'identity')
            check(checks,scope+':'+label+':zero history',np.max(abs(pair[0][-1]))+np.max(abs(pair[1][-1])),0,'negative_control')
        save(ROOT/f'results/source-{scope}.npz',actual_high=actual[0],actual_low=actual[1],predicted_high=predicted[0],predicted_low=predicted[1],
             error_high=error[0],error_low=error[1],theta=config['theta'],frequencies=np.array(frequencies),components=np.array(COMPONENTS))
    for frequency_index,values in nodes.items():
        anchor_totals=[]
        for label in ('warm','middle','cold'):
            pairs=[]
            for event in range(36):
                packet_values=packet(ROOT/f'anchors/frequency-{frequency_index}/{label}/event-{event:02d}.npz')
                pairs.append((packet_values['high'],packet_values['low']))
            anchor_totals.append(metrics.primitives(pairs))
        regrouped=foundation.weighted_sum(anchor_totals,config['operator_weights'])
        error=metrics.subtract(regrouped,values['predicted'])
        for name,measure in measurements:
            relative=measure(error[0][:2]+error[1][:2])/np.maximum(measure(values['predicted'][0][:2]+values['predicted'][1][:2]),1e-300)
            check(checks,f'{frequency_index}:anchor-first/event-first regroup '+name,relative.max(),1e-10,'identity')
    cancellation=[]
    for label in ('actual','predicted'):
        leaves=[(reference[label+'_high'],reference[label+'_low'])]+[values[label] for values in nodes.values()]
        regrouped=metrics.primitives(leaves)
        aggregate=cumulative_actual if label=='actual' else cumulative_prediction
        error=metrics.subtract(regrouped,aggregate)
        for name,measure in measurements:
            relative=measure(error[0][:2]+error[1][:2])/np.maximum(measure(aggregate[0][:2]+aggregate[1][:2]),1e-300)
            check(checks,label+':six-frequency regroup '+name,relative.max(),1e-10,'identity')
            ratio=sum(measure(pair[0][:2]+pair[1][:2]) for pair in leaves)/np.maximum(measure(aggregate[0][:2]+aggregate[1][:2]),1e-300)
            cancellation.append(dict(source=label,measure=name,max_factor=float(ratio.max()),grouping='saved four-node source plus two nodes'))
    check(checks,'weights not reapplied or renormalized',int(config['frequency_weights_reapplied'] or config['partial_panel_normalized']),0,'integrity')
    failed=[entry for entry in checks if not entry['passed']]
    report=dict(stage=212,state='prediction_rejected' if failed else 'nodes_and_six_frequency_qualified',qualified=not failed,
                checks=checks,failed_checks=failed,records=records,mesh_records=mesh_records,event_diagnostics=event_diagnostics,
                cancellation=cancellation,frequencies=FREQUENCIES,coverage=config['coverage'],target_fraction=config['target_fraction'],
                anchor_events=216,direct_events=72,reused_target_events=144,permission_to_propagate=False,full_band=False,
                original_bank_changed=False,curve_changed=False,grids_changed=False,tolerances_changed=False)
    destination=ROOT/'results/assessment.json'
    assert not destination.exists()
    write(destination,report)
    write(ROOT/'progress.json',dict(state=report['state'],anchor_events_complete=216,target_events_complete=72,permission_to_propagate=False))
    summary={scope:{component:max(entry['relative'] for entry in records if entry['scope']==scope and entry['component']==component)
                    for component in ('baseline','MTS','total')} for scope,unused1,unused2,unused3,unused4 in scopes}
    print(json.dumps(dict(state=report['state'],checks=len(checks),failed=len(failed),summary=summary)),flush=True)


if __name__=='__main__':
    source.modest()
    main()

