from overlap_common import *
import time


def planck_ratio(frequency,ratio):
    return (frequency/np.expm1(frequency))*(ratio*frequency/(-np.expm1(-ratio*frequency)))


def main():
    modest()
    folder=ROOT/'results/planck-remainder'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    inputs=[ROOT/'PLANCK-BOUND-SCOPE.md']
    checks,rows=[],[]
    edges=np.geomspace(.01,.04,257)
    for epoch in range(65):
        path=BRANCH/'direct-doppler-compton-feedback-20261012/results/bank-o8-q32-m40'/f'epoch-{epoch:02d}.npz'
        verify_source(path,chain)
        inputs.append(path)
        events=read_npz(path)
        lower=float(events['ratios'].min())
        upper=float(events['ratios'].max())
        low_bound=(edges[1:]/np.expm1(edges[1:]))*(lower*edges[:-1]/(-np.expm1(-lower*edges[:-1])))
        high_bound=(edges[:-1]/np.expm1(edges[:-1]))*(upper*edges[1:]/(-np.expm1(-upper*edges[1:])))
        epsilon=float(max(np.max(abs(low_bound-1)),np.max(abs(high_bound-1))))
        mid=np.sqrt(edges[1:]*edges[:-1])
        checks.extend([
            check(f'Monotone-box lower bound:e{epoch}',np.max(np.maximum(low_bound-planck_ratio(mid,lower),0)),1e-14),
            check(f'Monotone-box upper bound:e{epoch}',np.max(np.maximum(planck_ratio(mid,upper)-high_bound,0)),1e-14)])
        rows.append(dict(epoch=epoch,theta=float(events['theta']),ratio_range=[lower,upper],
            finite_event_band_planck_bound=epsilon,weak_norm_bound_not_net_relative=True))
    quadrature,weights=special.roots_legendre(96)
    half=math.log(4)/2
    frequency=np.exp(math.log(.01*.04)/2+half*quadrature)
    weights=weights*half*frequency/(2*I3)
    contrasts=[]
    for model in ['heavy','cold']:
        prediction,profiles,gas,dependencies=read_prediction(model,'fine')
        inputs.extend(dependencies)
        overlap_path=ROOT/'results'/f'{model}-fine-lo25-n5120/overlap.npz'
        candidate=read_npz(overlap_path)
        inputs.extend([overlap_path,overlap_path.parent/'status.json'])
        for epoch in [0,32,64]:
            started=time.monotonic()
            path=BRANCH/'direct-doppler-compton-feedback-20261012/results/bank-o8-q32-m40'/f'epoch-{epoch:02d}.npz'
            events=read_npz(path)
            ratios,rates=events['ratios'],events['rates']
            spline=interpolate.CubicSpline(np.log(candidate['frequency']),candidate['slope'][epoch],axis=0,extrapolate=False)
            initial=frequency[:,None]*(spline(np.log(frequency))-gas[epoch])
            soft=np.zeros(3)
            difference=np.zeros(3)
            dissipation=np.zeros(3)
            energy_dissipation=0.
            for begin in range(0,len(ratios),128):
                ratio=ratios[begin:begin+128,None]
                shifted=ratio*frequency
                shifted_phi=shifted[:,:,None]*(spline(np.log(shifted))-gas[epoch])
                delta_phi=shifted_phi-initial
                delta_test=shifted-frequency
                conductance=(rates[begin:begin+128,None]/ratio)*weights
                factor=planck_ratio(frequency,ratio)
                soft-=np.einsum('ef,ef,efk->k',conductance,delta_test,delta_phi)
                difference-=np.einsum('ef,ef,ef,efk->k',conductance,factor-1,delta_test,delta_phi)
                dissipation+=np.einsum('ef,efk,efk->k',conductance,delta_phi,delta_phi)
                energy_dissipation+=float(np.sum(conductance*delta_test**2))
            estimate=rows[epoch]['finite_event_band_planck_bound']*np.sqrt(energy_dissipation*dissipation)
            bound_ratio=abs(difference)/np.maximum(estimate,1e-300)
            checks.append(check(f'Dirichlet remainder bound:{model}:e{epoch}',np.max(bound_ratio),1+1e-10))
            checks.append(dict(name=f'Positive Dirichlet energies:{model}:e{epoch}',passed=bool((dissipation>=0).all() and energy_dissipation>=0)))
            contrasts.append(dict(model=model,epoch=epoch,soft_energy_functional=soft.tolist(),
                planck_change=difference.tolist(),opposite_gas_change=(-difference).tolist(),
                weak_bound=estimate.tolist(),bound_usage=bound_ratio.tolist(),
                planck_change_over_soft=(difference/np.where(soft!=0,soft,1e-300)).tolist(),
                source_domain='incident x in [0.01,0.04], including physical shifted endpoints',
                only_conductance_remainder=True,gas_history_not_evolved=True))
            print(json.dumps(dict(model=model,epoch=epoch,seconds=time.monotonic()-started)),flush=True)
    finish(folder,dict(checks=checks,rows=rows,contrasts=contrasts,
        maximum_finite_event_planck_bound=max(row['finite_event_band_planck_bound'] for row in rows),
        full_juttner_tail_certified=False,recoil_included=False,finite_emission_remainder_included=False,
        actual_doppler_shifts=True,new_thermal_events=0,net_force_relative_error_bound=False),__file__,inputs)
    print(json.dumps(dict(maximum_planck_bound=max(row['finite_event_band_planck_bound'] for row in rows),
        failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
