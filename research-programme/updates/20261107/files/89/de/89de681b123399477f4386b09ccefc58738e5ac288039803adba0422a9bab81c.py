from next_intervals_common import *
import time


def main():
    modest()
    started=time.monotonic()
    folder=ROOT/'results/coefficients'
    folder.mkdir(parents=True,exist_ok=False)
    parent_bank_path=PARENT/'results/coefficients/bank.npz'
    parent_bank=read_npz(parent_bank_path)
    old_path=refined_owner('heavy')/'results/inner-heavy-n40960/prediction.npz'
    old=read_npz(old_path)
    offsets,spacing=parent_bank['offsets'],float(parent_bank['spacing'])
    active=offsets!=0
    start,end=old['coordinate'][[0,-1]]
    coordinates=start+(end-start)*SOURCE_STEPS/40960
    backgrounds={model:thermal_wave.thermal.ThermalBackground(model) for model in ['heavy','cold']}
    checks,rows,stencils,raws,eigenvalues,temperatures=[],[],[],[],[],[]
    inputs=[parent_bank_path,parent_bank_path.parent/'status.json',old_path]
    for background in backgrounds.values():
        inputs.extend([background.parent.source,background.native_constants])
    for index,(step,coordinate) in enumerate(zip(SOURCE_STEPS,coordinates)):
        theta=backgrounds['heavy'].at(float(coordinate))['thermal_parameter']
        assert theta==backgrounds['cold'].at(float(coordinate))['thermal_parameter']
        path=event_path(int(step))
        if step%640==0:
            event=read_npz(path)
            ratios,rates=event['ratios'],event['rates']
            checks.append(check(f'Saved temperature:{step}',abs(theta-float(event['theta']))/theta,1e-12))
            inputs.append(path)
        else:
            ratios,rates=tail.jump_events(theta,6)
            np.savez_compressed(path,step=step,coordinate=coordinate,theta=theta,ratios=ratios,rates=rates)
        raw,weights,errors=deposit_cubic(ratios,rates,offsets,spacing)
        stencil=pair_cubic(raw,offsets,spacing)
        eigen=float(np.sum(rates*(ratios-1)**2*(ratios+1)/ratios**3)/2)
        moments=np.sum(stencil[active,None]*np.expm1(offsets[active,None]*spacing*np.array([-1.,-2.,-3.])),axis=0)+eigen
        moment_error=float(np.max(abs(moments-np.array([0.,0.,eigen])))/eigen)
        bound=symbol_bound(stencil,offsets,spacing,eigen)
        checks.extend([dict(name=f'Positive physical events:{step}',passed=bool(np.all(ratios>0) and np.all(rates>0))),
            check(f'Cubic monomials:{step}',max(errors),1e-12),check(f'Inner moments:{step}',moment_error,1e-9),
            dict(name=f'All-band finite-grid dissipativity:{step}',passed=bound['upper_bound']<0,value=bound['upper_bound'])])
        if index==0:
            checks.append(dict(name='Exact Stage135 endpoint coefficients',passed=np.array_equal(stencil,parent_bank['stencil'][-1]) and eigen==parent_bank['eigenvalue'][-1]))
        rows.append(dict(index=index,step=int(step),theta=theta,event_sha256=digest(path),event_path=str(path),
            moment_error=moment_error,bound=bound,reused=step%640==0))
        stencils.append(stencil)
        raws.append(raw)
        eigenvalues.append(eigen)
        temperatures.append(theta)
    assert all(row['passed'] for row in checks),[row for row in checks if not row['passed']]
    np.savez_compressed(folder/'bank.npz',steps=SOURCE_STEPS,coordinate=coordinates,temperature=np.array(temperatures),
        offsets=offsets,spacing=spacing,stencil=np.array(stencils),raw=np.array(raws),eigenvalue=np.array(eigenvalues))
    chain=ancestors()
    for path in inputs:
        verify_source(path,chain)
    finish(folder,dict(checks=checks,rows=rows,new_temperature_event_evaluations=int(np.count_nonzero(SOURCE_STEPS%640)),saved_endpoint_events_reused=int(np.count_nonzero(SOURCE_STEPS%640==0)),
        event_order=6,normalization_fitted=False,seconds=time.monotonic()-started),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),max_bound=max(row['bound']['upper_bound'] for row in rows),seconds=time.monotonic()-started)),flush=True)


if __name__=='__main__':
    main()
