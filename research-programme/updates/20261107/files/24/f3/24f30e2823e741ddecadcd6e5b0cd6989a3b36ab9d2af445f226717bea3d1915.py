from restart_stage182 import *
import time


def forbidden(*args,**kwargs):
    raise RuntimeError('Stage182 forbids new virtual-loop integration')


def event_path(node):
    return ROOT/'gas-events'/saved.angle_label(node['cosine'])/f"electron-{node['electron_index']:02d}.npz"


def evaluate(limit):
    config=read(ROOT/'configuration.json')
    paths=read(ROOT/'authenticated-inputs.json')
    anchor,theta=source.context(source.START)
    unit=previous.prior.ChannelHistory(anchor,'unit_gas')
    paired=source.PairedHistory(anchor,unit)
    evaluators=source.models(paired)
    source.physics.weak.source.virtual_map=forbidden
    consumed=set(anchor.inputs)
    for ordinal,node in enumerate(config['selected']):
        path=event_path(node)
        old=BANK/'events/anchor'/saved.angle_label(node['cosine'])/f"electron-{node['electron_index']:02d}.npz"
        with np.load(old) as packet:
            assert float(packet['theta'])==theta
            assert json.loads(str(packet['node']))==node
            expected_high,expected_low=packet['high'][0].copy(),packet['low'][0].copy()
            loop_path=Path(str(packet['loop_path']))
            expected_weight=float(packet['weight'])
        parameters,weight=source.physics.parameters_and_weight(theta,node)
        assert weight==expected_weight
        loop=read(loop_path)
        assert loop['finite'] and loop['identity']==source.physics.event_owner.inherited.virtual_identity(parameters)
        for owner in [old,loop_path]:
            assert str(owner) in paths and saved.digest(owner)==paths[str(owner)],str(owner)
        consumed.update([old,loop_path])
        if not path.exists():
            if limit<=0 or datetime.now(timezone.utc)>=datetime(2026,10,21,1,20,tzinfo=timezone.utc):
                write(ROOT/'response-progress.json',dict(state='safe_restart',next_event=ordinal,saved_events=len(list((ROOT/'gas-events').rglob('*.npz')))))
                return
            began=time.monotonic()
            mp.mp.dps=60
            high,low,diagnostics=source.evaluate(parameters,paired,evaluators,loop['scalar'])
            pair=(np.stack([high[...,:4],high[...,4:]]),np.stack([low[...,:4],low[...,4:]]))
            high,low=source.precise_combine([pair],[-weight])
            previous.prior.atomic_npz(path,high=high,low=low,theta=theta,weight=weight,
                node=json.dumps(node,sort_keys=True),diagnostics=json.dumps(diagnostics),
                original_path=str(old),original_sha256=saved.digest(old),loop_path=str(loop_path),loop_sha256=saved.digest(loop_path),
                seconds=time.monotonic()-began)
            limit-=1
            print(json.dumps(dict(event=ordinal+1,expected=36,seconds=time.monotonic()-began)),flush=True)
        with np.load(path) as packet:
            assert packet['high'].shape==packet['low'].shape==(2,6,98,4)
            assert np.isfinite(packet['high']).all() and np.isfinite(packet['low']).all()
            assert str(packet['original_sha256'])==saved.digest(old)
            assert str(packet['loop_sha256'])==saved.digest(loop_path)
        write(ROOT/'response-progress.json',dict(state='unit_gas_actions',saved_events=ordinal+1,expected=36,pid=os.getpid()))
    for module in list(sys.modules.values()):
        filename=getattr(module,'__file__',None)
        if filename and Path(filename).suffix=='.py' and Path(filename).is_relative_to(BRANCH) and not Path(filename).is_relative_to(ROOT):
            consumed.add(Path(filename))
    for owner in consumed:
        assert str(owner) in paths and saved.digest(owner)==paths[str(owner)],str(owner)
    write(ROOT/'response-inputs.json',{str(owner):saved.digest(owner) for owner in sorted(consumed)})
    write(ROOT/'response-progress.json',dict(state='unit_gas_complete',saved_events=36))


def precise_sum(pairs):
    shape=pairs[0][0].shape
    result=np.zeros(shape)
    with mp.workdps(80):
        for index in np.ndindex(shape):
            result[index]=float(mp.fsum(mp.mpf(float(high[index]))+mp.mpf(float(low[index])) for high,low in pairs))
    return result


def analyse():
    assert read(ROOT/'response-progress.json')['state']=='unit_gas_complete'
    config=read(ROOT/'configuration.json')
    with np.load(source.ROOT/'results/preparation/basis.npz') as packet:
        mass=packet['mass'].copy()
    factor=linear.cholesky(mass,lower=True)
    def norm(values):
        reshaped=np.moveaxis(values[...,1:97,:],-2,0).reshape(96,-1)
        return np.linalg.norm(linear.solve_triangular(factor,reshaped,lower=True),axis=0).reshape(values.shape[:-2]+(values.shape[-1],))
    rows=[]
    pairs=[]
    native_pairs=[]
    original_pairs=[]
    for node in config['selected']:
        with np.load(event_path(node)) as packet:
            high,low=packet['high'].copy(),packet['low'].copy()
            pairs.append((high[1],low[1]))
            native_pairs.append((high[0],low[0]))
            original=Path(str(packet['original_path']))
            diagnostics=json.loads(str(packet['diagnostics']))
        with np.load(original) as packet:
            old_high,old_low=packet['high'][0].copy(),packet['low'][0].copy()
            original_pairs.append((old_high,old_low))
        label=saved.event_key(node)
        for name,value in diagnostics.items():
            check(rows,label+':'+name,value)
        comparison=norm((high[0]+low[0])-(old_high+old_low))/np.maximum(norm(old_high+old_low),1e-300)
        for component in range(6):
            check(rows,label+': native source replay '+source.COMPONENTS[component],np.max(comparison[component]))
        values=high[1]+low[1]
        for component in range(6):
            scale=np.maximum(np.maximum(abs(values[component,0]),abs(values[component,-1])),1e-300)
            check(rows,label+': unit gas exchange '+source.COMPONENTS[component],np.max(abs(values[component,0]+values[component,-1])/scale))
        check(rows,label+': unit columns identical',np.max(abs(values-values[...,:1]))/max(np.max(abs(values)),1e-300))
        check(rows,label+': unit matched closure',np.max(norm(values[4]-values[1]-values[2]-values[3])/np.maximum(norm(values[4]),1e-300)))
        check(rows,label+': unit total closure',np.max(norm(values[5]-values[0]-values[4])/np.maximum(norm(values[5]),1e-300)))
    kernels=precise_sum(pairs)
    native_values=precise_sum(native_pairs)
    old_values=precise_sum(original_pairs)
    independent_units=[]
    authenticated=read(ROOT/'authenticated-inputs.json')
    for node in config['selected']:
        path=SPLIT/'results/precision/events'/saved.angle_label(node['cosine'])/f"electron-{node['electron_index']:02d}.npz"
        assert str(path) in authenticated and saved.digest(path)==authenticated[str(path)]
        with np.load(path) as packet:
            independent_units.append((packet['unit_high'].copy(),packet['unit_low'].copy()))
    independent_virtual=precise_sum(independent_units)
    check(rows,'Independent Stage180 virtual unit-gas coefficient reproduced',np.max(norm(kernels[2]-independent_virtual)/np.maximum(norm(independent_virtual),1e-300)))
    for component in range(6):
        check(rows,'summed native '+source.COMPONENTS[component],np.max(norm(native_values[component]-old_values[component])/np.maximum(norm(old_values[component]),1e-300)))
    with np.load(ROOT/'results/history-curvature.npz') as packet:
        curves=packet['curves'].copy()
        branch_labels=list(packet['branches'])
    responses=np.zeros((4,3,6,98,4))
    for branch,order,component,column in np.ndindex(4,3,6,4):
        responses[branch,order,component,:,column]=kernels[component,:,column]*curves[column//2,branch,order]
    response_rows=[]
    for component in [0,4,5]:
        for column in range(4):
            for order,label in enumerate(['coarse_curvature','fine_curvature','width_discrepancy']):
                old=responses[0,order,component]
                refined=responses[1,order,component]
                relative=norm(refined-old)[column]/norm(refined)[column]
                expected=abs((curves[column//2,1,order]-curves[column//2,0,order])/curves[column//2,1,order])
                check(rows,f'{source.COMPONENTS[component]}:{column}:{label}: gas law relative',abs(relative-expected)/max(expected,1e-300))
                check(rows,f'{source.COMPONENTS[component]}:{column}:{label}: native/half',relative,.01,'step_comparison')
                response_rows.append(dict(component=source.COMPONENTS[component],column=column,quantity=label,
                    native_norm=float(norm(old)[column]),half_norm=float(norm(refined)[column]),
                    relative_change=float(relative),tolerance=.01,passed=bool(relative<=.01)))
    np.savez_compressed(ROOT/'results/gas-response.npz',kernels=kernels,responses=responses,
        branches=np.array(branch_labels),components=np.array(source.COMPONENTS),native_anchor_replay=native_values,original_anchor=old_values,
        independent_stage180_virtual_unit=independent_virtual)
    write(ROOT/'results/gas-response-comparison.json',response_rows)
    write(ROOT/'results/gas-response-checks.json',dict(checks=rows,count=len(rows),all_checks_passed=all(row['passed'] for row in rows),
        new_real_response_events=36,new_real_integrator_calls=144,new_virtual_loop_integrations=0,
        source_scope='isolated gas channel at original fixed anchor; not a full revised source history'))
    write(ROOT/'response-progress.json',dict(state='response_assessment_complete'))
    print(json.dumps(dict(checks=len(rows),failed=[row for row in rows if not row['passed']],
        maximum_native_source_replay_relative=float(np.max(norm(native_values-old_values)/np.maximum(norm(old_values),1e-300))))),flush=True)


if __name__=='__main__':
    source.modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('phase',choices=['evaluate','analyse'])
    parser.add_argument('--limit',type=int,default=36)
    args=parser.parse_args()
    evaluate(args.limit) if args.phase=='evaluate' else analyse()
