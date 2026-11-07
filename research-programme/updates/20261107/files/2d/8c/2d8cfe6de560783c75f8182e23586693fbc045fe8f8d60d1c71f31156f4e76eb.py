from operator209 import *


def main():
    config=protocol()
    manifest=verify_prediction(config)
    original,unused=source.context(config['target_fraction'])
    factor=linear.cholesky(original.basis.mass,lower=True)
    measurements=[('photon',lambda values:metrics.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]
    checks=list(read(ROOT/'results/preparation.json')['checks'])
    direct=[]
    forecasts=[]
    event_diagnostics=[]
    for row in config['anchors']:
        values,report=verify_event(event_path('anchors',row))
        checks.extend(dict(entry,name=f"{row['label']}:{row['event']}:"+entry['name']) for entry in report['checks'])
    for row in config['target']:
        values,report=verify_event(event_path('target',row))
        assert datetime.fromisoformat(report['started_at'])>datetime.fromisoformat(manifest['frozen_at'])
        assert report['coefficients_sha256']==digest(ROOT/'frozen/history-coefficients.npz')
        assert json.loads(str(values['node']))==row['node']
        assert float(values['theta'])==config['theta'] and float(values['weight'])==row['weight']
        checks.extend(dict(entry,name=f"target:{row['event']}:"+entry['name']) for entry in report['checks'])
        actual=(values['high'],values['low'])
        frozen=packet(ROOT/f"frozen/prediction/event-{row['event']:02d}.npz")
        predicted=(frozen['high'],frozen['low'])
        direct.append(actual)
        forecasts.append(predicted)
        difference=metrics.subtract(predicted,actual)
        for name,measure in measurements:
            relative=measure(difference[0][:2]+difference[1][:2])/np.maximum(measure(actual[0][:2]+actual[1][:2]),1e-300)
            event_diagnostics.append(dict(event=row['event'],measure=name,worst_relative=float(relative.max()),used_as_primary_gate=False))
    actual=metrics.primitives(direct)
    predicted=metrics.primitives(forecasts)
    frozen=packet(ROOT/'frozen/predicted-node.npz')
    for index,name in enumerate(('high','low')):
        check(checks,'frozen aggregate bitwise '+name,int(not np.array_equal(predicted[index],frozen[name])),0,'integrity')
    error=metrics.subtract(predicted,actual)
    records=[]
    mesh_records=[]
    for name,measure in measurements:
        relative=measure(error[0][:2]+error[1][:2])/np.maximum(measure(actual[0][:2]+actual[1][:2]),1e-300)
        for grid,component,column in np.ndindex(relative.shape):
            value=float(relative[grid,component,column])
            entry=dict(grid=GRIDS[grid],component=COMPONENTS[component],model=('heavy','cold')[column//2],
                       join=column%2,measure=name,relative=value)
            records.append(entry)
            check(checks,f'{grid}:{component}:{column}:{name}:forecast',value,.01,'prediction')
        for label,pair in [('actual',actual),('predicted',predicted)]:
            difference=metrics.subtract((pair[0][0],pair[1][0]),(pair[0][1],pair[1][1]))
            relative_mesh=measure(difference[0]+difference[1])/np.maximum(measure(pair[0][1]+pair[1][1]),1e-300)
            for component,column in np.ndindex(relative_mesh.shape):
                value=float(relative_mesh[component,column])
                mesh_records.append(dict(source=label,component=COMPONENTS[component],model=('heavy','cold')[column//2],
                                         join=column%2,measure=name,relative=value))
                check(checks,f'{label}:{component}:{column}:{name}:mesh',value,.01,'mesh')
    for label,pair in [('actual',actual),('predicted',predicted),('error',error)]:
        energy=pair[0][...,0,:]+pair[1][...,0,:]
        gas=pair[0][...,-1,:]+pair[1][...,-1,:]
        residual=abs(energy+gas)/np.maximum(np.maximum(abs(energy),abs(gas)),1e-300)
        check(checks,label+':energy exchange',residual.max(),1e-10,'identity')
        check(checks,label+':zero history',np.max(abs(pair[0][-1]))+np.max(abs(pair[1][-1])),0,'negative_control')
    anchor_totals=[]
    for label in ('warm','middle','cold'):
        pairs=[]
        for event in range(36):
            values=packet(ROOT/f'anchors/{label}/event-{event:02d}.npz')
            pairs.append((values['high'],values['low']))
        anchor_totals.append(metrics.primitives(pairs))
    regrouped=previous.weighted_sum(anchor_totals,config['operator_weights'])
    regroup_error=metrics.subtract(regrouped,predicted)
    for name,measure in measurements:
        relative=measure(regroup_error[0][:2]+regroup_error[1][:2])/np.maximum(measure(predicted[0][:2]+predicted[1][:2]),1e-300)
        check(checks,'anchor-first/event-first regroup '+name,relative.max(),1e-10,'identity')
    save(ROOT/'results/source-node.npz',actual_high=actual[0],actual_low=actual[1],
         predicted_high=predicted[0],predicted_low=predicted[1],error_high=error[0],error_low=error[1],
         theta=config['theta'],frequency=14.,components=np.array(COMPONENTS))
    failed=[entry for entry in checks if not entry['passed']]
    report=dict(stage=209,state='node_prediction_rejected' if failed else 'central_node_qualified',
                qualified=not failed,checks=checks,failed_checks=failed,records=records,mesh_records=mesh_records,
                event_diagnostics=event_diagnostics,frequency=14.,target_fraction=config['target_fraction'],
                anchor_events=108,direct_events=36,permission_to_propagate=False,full_band=False,
                original_bank_changed=False,curve_changed=False,grids_changed=False,tolerances_changed=False)
    destination=ROOT/'results/assessment.json'
    assert not destination.exists()
    write(destination,report)
    write(ROOT/'progress.json',dict(state=report['state'],anchor_events_complete=108,target_events_complete=36,
                                   permission_to_propagate=False))
    print(json.dumps(dict(state=report['state'],checks=len(checks),failed=len(failed),
        baseline=max(entry['relative'] for entry in records if entry['component']=='baseline'),
        MTS=max(entry['relative'] for entry in records if entry['component']=='MTS'),
        worst=max(entry['relative'] for entry in records))),flush=True)


if __name__=='__main__':
    source.modest()
    main()

