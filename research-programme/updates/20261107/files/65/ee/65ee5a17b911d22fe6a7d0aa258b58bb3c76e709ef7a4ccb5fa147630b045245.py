from source205 import *


def save_scoped(path,**values):
    config=protocol()
    frequencies={
        ROOT/'results/neighbour-source.npz':[FREQUENCY],
        ROOT/'results/five-frequency-source.npz':[item['frequency'] for item in config['partial_panel']],
        ROOT/'results/adapter-replay-source.npz':[item['frequency'] for item in read(PARENT/'configuration.json')['partial_panel']],
    }
    assert Path(path) in frequencies,path
    assert np.array_equal(values['frequencies'],np.array([FREQUENCY] if Path(path).name=='neighbour-source.npz' else [14.,FREQUENCY]))
    values['frequencies']=np.array(frequencies[Path(path)])
    save(path,**values)


def configure_assessment():
    inherited_assessment.ROOT=ROOT
    inherited_assessment.FREQUENCY=FREQUENCY
    inherited_assessment.protocol=protocol
    inherited_assessment.save=save_scoped


def collection(path):
    values=packet(path)
    return {label:(values[label+'_high'],values[label+'_low']) for label in ('prediction','absolute','split')}


def adapter_test():
    config=protocol();configure_assessment()
    assert not (ROOT/'prediction').exists() and not (ROOT/'actual').exists()
    original,unused=source.context(config['target_fraction'])
    factor=linear.cholesky(original.basis.mass,lower=True)
    reference=collection(REFERENCE);rows=[]
    result=inherited_assessment.assess_scope('adapter-replay',reference['prediction'],reference['absolute'],reference['split'],factor,rows)
    replay=packet(result['result_path']);before=packet(REFERENCE)
    for name in before:
        check(rows,'saved four-frequency replay bitwise:'+name,int(not np.array_equal(replay[name],before[name])),0,'integrity')
    write(ROOT/'results/adapter-validation.json',dict(checks=rows,failed_checks=[row for row in rows if not row['passed']],
        reference_path=str(REFERENCE),reference_sha256=digest(REFERENCE),
        replay_sha256=result['result_sha256'],physics_evaluations=0,
        adapter_changes='Process-local output destination, frequency label and declared frequency metadata only'))
    print(json.dumps(dict(adapter_checks=len(rows),failed=[row for row in rows if not row['passed']])),flush=True)


def main():
    config=protocol();configure_assessment();manifest=runner.verify_frozen()
    assert digest(REFERENCE)==manifest['reference_prediction_sha256']
    original,theta=source.context(config['target_fraction'])
    factor=linear.cholesky(original.basis.mass,lower=True)
    rows=list(read(ROOT/'results/preparation.json')['checks'])
    predictions=[];actuals=[];parts=[];event_diagnostics=[]
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
                check(rows,f'{index}:predictions frozen before actual start',int(datetime.fromisoformat(record['started_utc'])<=frozen_time),0,'integrity')
        predicted_packet=packet(ROOT/f'frozen/event-{index:02d}-prediction.npz')
        actual_packet=packet(ROOT/f'actual/event-{index:02d}.npz')
        part_packet=packet(ROOT/f'prediction/event-{index:02d}.npz')
        predicted=(predicted_packet['high'],predicted_packet['low'])
        absolute=(actual_packet['high'],actual_packet['low'])
        predictions.append(predicted);actuals.append(absolute)
        parts.append((part_packet['high'][:4],part_packet['low'][:4]))
        observed=inherited_assessment.observed_increment(absolute)
        error=metrics.subtract(predicted,observed)
        photon_norm=lambda values:metrics.norms(values,factor)
        scale=np.maximum(photon_norm(absolute[0][1:]+absolute[1][1:]),photon_norm(absolute[0][0]+absolute[1][0]))
        inherited_assessment.records_for('event'+str(index),'absolute reconstruction',photon_norm(error[0]+error[1])/np.maximum(scale,1e-300),rows,1e-10,'identity')
        event_diagnostics.append(dict(event=index,maximum_photon_relative=float((photon_norm(error[0]+error[1])/np.maximum(photon_norm(observed[0]+observed[1]),1e-300)).max()),
            maximum_gas_relative=float((abs(error[0][...,-1,:]+error[1][...,-1,:])/np.maximum(abs(observed[0][...,-1,:]+observed[1][...,-1,:]),1e-300)).max()),aggregate_gate_applied_here=False))
    new=dict(prediction=metrics.primitives(predictions),absolute=metrics.primitives(actuals),split=metrics.primitives(parts))
    reference=collection(REFERENCE)
    combined={label:metrics.primitives([reference[label],new[label]]) for label in new}
    leaves_by_node=[collection(path) for path in LEAVES]
    measurements=[('photon',lambda values:metrics.norms(values,factor)),('gas',lambda values:abs(values[...,-1,:]))]
    for label in new:
        inherited_assessment.decimal_samples(label,reference[label],new[label],combined[label],rows)
        leaves=metrics.primitives([*[item[label] for item in leaves_by_node],new[label]])
        difference=metrics.subtract(combined[label],leaves)
        for name,measure in measurements:
            error=measure(difference[0]+difference[1])/np.maximum(measure(leaves[0]+leaves[1]),1e-300)
            check(rows,label+':five-leaf grouping:'+name,error.max(),1e-10,'identity')
    summaries={}
    for scope,values in [('neighbour',new),('five-frequency',combined)]:
        frozen=packet(ROOT/f'frozen/{scope}-prediction.npz')
        for side,name in enumerate(('high','low')):
            check(rows,scope+':frozen aggregate bitwise:'+name,int(not np.array_equal(values['prediction'][side],frozen[name])),0,'integrity')
        summaries[scope]=inherited_assessment.assess_scope(scope,(frozen['high'],frozen['low']),values['absolute'],values['split'],factor,rows)
    cancellation=[]
    for label,pieces in [('saved-four-frequency plus new',[reference['prediction'],new['prediction']]),
                          ('five individual nodes',[*[item['prediction'] for item in leaves_by_node],new['prediction']])]:
        for name,measure in measurements:
            denominator=np.maximum(measure(combined['prediction'][0]+combined['prediction'][1]),1e-300)
            ratios=sum(measure(piece[0]+piece[1]) for piece in pieces)/denominator
            for grid,component,column in np.ndindex(ratios.shape):
                cancellation.append(dict(grouping=label,grid=GRIDS[grid],component=COMPONENTS[component],model=('heavy','cold')[column//2],
                    join=column%2,measure=name,cancellation_factor=float(ratios[grid,component,column])))
    check(rows,'weights not reapplied or renormalized',int(config['frequency_weights_reapplied'] or config['partial_panel_normalized']),0,'integrity')
    failed=[row for row in rows if not row['passed']]
    write(ROOT/'results/source-assessment.json',dict(checks=rows,failed_checks=failed,qualified=not failed,scopes=summaries,
        event_diagnostics=event_diagnostics,node_cancellation=cancellation,new_events=36,reused_reference_events=144,
        packets_already_frequency_weighted=True,frequency_weights_reapplied=False,partial_panel_normalized=False,
        full_frequency_panel_qualified=False,new_virtual_integrals=0,shared_evaluator=True,observational_prediction=False))
    write(ROOT/'progress.json',dict(state='qualified' if not failed else 'checks_failed',failed_checks=len(failed)))
    print(json.dumps(dict(checks=len(rows),failed=failed,summary={scope:dict(worst_prediction=max(row['relative'] for row in value['records']),
        worst_mesh=max(row['relative'] for row in value['mesh_records'])) for scope,value in summaries.items()})),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['adapter-test','assess'])
    args=parser.parse_args()
    if args.phase=='adapter-test':adapter_test()
    else:main()
