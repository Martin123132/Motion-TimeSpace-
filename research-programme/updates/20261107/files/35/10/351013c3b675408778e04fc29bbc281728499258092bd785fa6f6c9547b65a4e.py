from continue199 import *
NAMES=['original','candidate-half','candidate-quarter','candidate-half-delta','candidate-quarter-delta']
KINDS=['baseline','MTS','total']

def predict_versions(data):
    pairs=[]
    for indices in ([0],[0,3],[5],[3],[4]):
        pairs.append(saved.parts_sum(data['high'][indices],data['low'][indices]))
    return np.stack([pair[0] for pair in pairs]),np.stack([pair[1] for pair in pairs])

def main():
    config=checked_protocol();inputs=read(ROOT/'inputs.json');checks=[];records=[]
    for name,value in read(ROOT/'frozen/evaluation-protocol.json').items():
        assert digest(ROOT/name)==value,name
    assert digest(ROOT/'frozen/panel-prediction.npz')==config['prediction_hashes'][str(Path('frozen')/'panel-prediction.npz')]
    predictions=predict_versions(packet(ROOT/'frozen/panel-prediction.npz'))
    high=[];low=[];identities=[]
    for frequency_index in range(7):
        for node_index in range(36):
            path=ROOT/f'events/frequency-{frequency_index}/node-{node_index:02d}.npz'
            status=read(path.with_suffix('.json'));data=packet(path)
            assert digest(path)==status['sha256'] and not status['failed_checks']
            assert digest(status['loop_path'])==status['loop_sha256']
            assert abs(float(data['theta'])/(config['theta0']*math.exp(OFFSET))-1)<1e-12
            identities.extend(dict(row,name=f'{frequency_index}:{node_index}:'+row['name']) for row in status['checks'])
            high.append(data['high'][:,:4]);low.append(data['low'][:,:4])
    primitive=saved.parts_sum(np.stack(high),np.stack(low));absolute=[]
    for group in range(3):
        pairs=[]
        for members in ([0],[1,2,3],[0,1,2,3]):
            pairs.append(saved.parts_sum(primitive[0][group,members],primitive[1][group,members]))
        absolute.append((np.stack([pair[0] for pair in pairs]),np.stack([pair[1] for pair in pairs])))
    actual=list(absolute)
    for group in (1,2):
        actual.append(saved.parts_sum(np.stack([absolute[group][0],-absolute[0][0]]),np.stack([absolute[group][1],-absolute[0][1]])))
    actual_high=np.stack([pair[0] for pair in actual]);actual_low=np.stack([pair[1] for pair in actual])
    norm=microscopic.norm_setup()
    difference=saved.parts_sum(np.stack([predictions[0],-actual_high]),np.stack([predictions[1],-actual_low]))
    errors=norm(difference[0]+difference[1])/np.maximum(norm(actual_high+actual_low),1e-300)
    gas_errors=abs(difference[0][...,-1,:]+difference[1][...,-1,:])/np.maximum(abs(actual_high[...,-1,:]+actual_low[...,-1,:]),1e-300)
    for version,kind,column in np.ndindex(errors.shape):
        model=('heavy','cold')[column//2];join=column%2
        for measure,value in [('photon',errors[version,kind,column]),('gas',gas_errors[version,kind,column])]:
            name=f'{NAMES[version]}:{KINDS[kind]}:{model}:join{join}:{measure}:frozen prediction'
            check(checks,name,value,.01,'prediction')
            records.append(dict(version=NAMES[version],kind=KINDS[kind],model=model,join=join,measure=measure,relative=float(value)))
    step_diff=saved.parts_sum(np.stack([actual_high[1],-actual_high[2]]),np.stack([actual_low[1],-actual_low[2]]))
    for reference in (2,4):
        relative=norm(step_diff[0]+step_diff[1])/np.maximum(norm(actual_high[reference]+actual_low[reference]),1e-300)
        for kind,column in np.ndindex(relative.shape):
            check(checks,f'{KINDS[kind]}:{column}:history half/quarter relative to {NAMES[reference]}',relative[kind,column],.01,'history')
    source_pair=actual_high[...,0,:]+actual_low[...,0,:]+actual_high[...,-1,:]+actual_low[...,-1,:]
    scale=np.maximum(abs(actual_high[...,0,:]+actual_low[...,0,:]),1e-300)
    for version,kind,column in np.ndindex(scale.shape):
        check(identities,f'{NAMES[version]}:{KINDS[kind]}:{column}:energy pair',source_pair[version,kind,column]/scale[version,kind,column],1e-10,'identity')
    history_checks=[]
    for model in ('heavy','cold'):
        for grid in ('half','quarter'):
            status=read(ROOT/'histories'/model/grid/'complete.json')
            assert not status['failed_checks']
            history_checks.extend(dict(row,name=f'{model}:{grid}:'+row['name']) for row in status['checks'])
    checks.extend(identities);checks.extend(history_checks);checks.extend(read(ROOT/'collision/status.json')['checks'])
    save(ROOT/'results/target-panel.npz',high=actual_high,low=actual_low,prediction_high=predictions[0],prediction_low=predictions[1],
        difference_high=difference[0],difference_low=difference[1],offset=OFFSET,versions=np.array(NAMES),kinds=np.array(KINDS))
    for name,value in inputs.items():
        assert digest(name)==value,name
    failed=[row for row in checks if not row['passed']]
    report=dict(state='qualified' if not failed else 'forecast_rejected',stage=199,checks=checks,failed_checks=failed,
        records=records,events=252,inputs_rehashed=len(inputs),target_sha256=digest(ROOT/'results/target-panel.npz'),
        permission_to_propagate=not failed,prediction_adjusted_after_test=False)
    write(ROOT/'results/source-assessment.json',report)
    write(ROOT/'progress.json',dict(state=report['state'],checks=len(checks),failed_checks=len(failed),permission_to_propagate=not failed))
    print(json.dumps(dict(state=report['state'],checks=len(checks),failed_checks=failed,
        maxima={version:float(errors[index].max()) for index,version in enumerate(NAMES)})),flush=True)

if __name__=='__main__':main()
