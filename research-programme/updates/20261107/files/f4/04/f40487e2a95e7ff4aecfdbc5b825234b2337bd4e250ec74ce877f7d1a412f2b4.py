from coefficient_common import *


def main():
    modest()
    folder=ROOT/'results/coefficients'
    folder.mkdir(parents=True,exist_ok=False)
    owner=refined_owner('heavy')/'results/inner-heavy-n40960'
    parent=read_npz(owner/'prediction.npz')
    status=local_packet(owner)
    spacing=float(status['spacing'])
    old_root=BRANCH/'direct-doppler-compton-feedback-20261012/results/bank-o6-q32-m40'
    old_paths=[old_root/f'epoch-{epoch:02d}.npz' for epoch in range(65)]
    old_events=[read_npz(path) for path in old_paths]
    fresh_paths=[SITES/'results/operator-m20'/f'event-{step:05d}.npz' for step in range(20,640,20)]
    events=[old_events[0],*[read_npz(path) for path in fresh_paths],old_events[1]]
    replay_path=SITES/'results/replay-heavy-s00000/prediction.npz'
    coordinate=read_npz(replay_path)['coordinate']
    margin=int(max(abs(parent['offsets'])))
    offsets,low,chemical,constant,minimum=positive_stencils(events,spacing,margin)
    high_offsets,high,high_chemical,high_constant=high_stencils(events,spacing,4,margin+4)
    old_offsets,old_low,unused_chemical,unused_constant,unused_minimum=positive_stencils(old_events,spacing,margin)
    old_high_offsets,old_high,unused_high_chemical,unused_high_constant=high_stencils(old_events,spacing,4,margin+4)
    assert np.array_equal(offsets,parent['offsets']) and np.array_equal(old_low,parent['coefficient_bank'][:,:len(offsets)])
    assert np.array_equal(low[[0,-1]],old_low[:2]) and np.array_equal(high[[0,-1]],old_high[:2])
    checks=[check('Positive right-chemical invariant',chemical,1e-9),check('Positive constant jump invariant',constant,1e-12),
        check('High right-chemical invariant',high_chemical,1e-9),check('High weight partition',high_constant,1e-12),
        dict(name='Nonnegative point-deposition weights',passed=minimum>=0),
        dict(name='Old stencil and endpoint arrays preserved',passed=True)]
    eigenvalues,moments,rows=[],[],[]
    for index,event in enumerate(events):
        ratio,rates=event['ratios'],event['rates']
        shift=np.log(ratio)
        eigen=float(rates@(-np.expm1(-shift)))
        moment=float(np.sum(rates*(ratio-1)**2*(ratio+1)/ratio**3))
        scale=max(abs(eigen),1e-300)
        balance_number=float(np.sum((rates/ratio)*np.expm1(-shift)))
        balance_energy=float(np.sum((rates/ratio)*np.expm1(-2*shift))-eigen)
        lower=np.floor(shift/spacing).astype(int)
        weight=-np.expm1(-(shift-lower*spacing))/(-np.expm1(-spacing))
        left=np.exp(-lower*spacing)
        right=np.exp(-(lower+1)*spacing)
        target=1/ratio
        variance=weight*(1-weight)*(left-right)**2
        predicted=np.array([np.sum(rates*variance),np.sum(rates*variance*(left+right+target))])
        direct=np.array([np.sum(rates*np.expm1(power*shift))+eigen for power in [-2,-3]])
        low_values=np.array([low[index]@np.expm1(power*offsets*spacing)+eigen for power in [-2,-3]])
        high_values=np.array([high[index]@np.expm1(power*high_offsets*spacing)+eigen for power in [-2,-3]])
        checks.extend([check(f'Detailed balance number:{index}',abs(balance_number)/scale,1e-8),
            check(f'Detailed balance energy:{index}',abs(balance_energy)/scale,1e-8),
            check(f'm=2lambda:{index}',abs(moment-2*eigen)/(2*scale),1e-8),
            check(f'Derived deposition bias:{index}',np.max(abs((low_values-direct)-predicted))/scale,1e-9),
            check(f'High exact moment:{index}',np.max(abs(high_values-direct))/scale,1e-9),
            check(f'Low exact moment:{index}',np.max(abs(low_values-direct))/scale,1e-9),
            dict(name='Positive saved kernel:'+str(index),passed=bool(np.all(rates>0) and np.all(ratio>0) and eigen>0))])
        rows.append(dict(index=index,coordinate=float(coordinate[index]),theta=float(event['theta']),
            eigenvalue=eigen,energy_moment=moment,low_bias=(low_values-direct).tolist(),
            predicted_bias=predicted.tolist(),low_bias_over_eigen=((low_values-direct)/scale).tolist(),
            high_bias_over_eigen=((high_values-direct)/scale).tolist()))
        eigenvalues.append(eigen)
        moments.append(moment)
    eigenvalues,moments=np.array(eigenvalues),np.array(moments)
    assert np.array_equal(eigenvalues[[0,-1]],parent['coefficient_bank'][:2,len(offsets)])
    assert all(row['passed'] for row in checks if not row['name'].startswith('Low exact moment:'))
    np.savez_compressed(folder/'bank.npz',coordinate=coordinate,temperature=np.array([event['theta'] for event in events]),
        offsets=offsets,low=low,high_offsets=high_offsets,high=high,eigenvalue=eigenvalues,moment=moments,
        old_coordinate=parent['coordinate'],old_low=old_low,old_high=old_high,spacing=spacing,
        original_coefficients=parent['coefficient_bank'])
    inputs=[owner/'prediction.npz',owner/'status.json',replay_path,replay_path.parent/'status.json',*old_paths,*fresh_paths]
    chain=ancestors()
    for path in inputs:
        verify_source(path,chain)
    finish(folder,dict(checks=checks,rows=rows,old_endpoints_bitwise=True,
        temporal_replay_permitted=True,continuum_energy_consistency=all(row['passed'] for row in checks),
        spatial_rule_unchanged=True,new_temperature_integrals=0),__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failures=sum(not row['passed'] for row in checks),
        low_number_bias_range=[min(row['low_bias_over_eigen'][0] for row in rows),max(row['low_bias_over_eigen'][0] for row in rows)],
        low_energy_bias_range=[min(row['low_bias_over_eigen'][1] for row in rows),max(row['low_bias_over_eigen'][1] for row in rows)],
        maximum_high_bias=max(max(abs(value) for value in row['high_bias_over_eigen']) for row in rows))),flush=True)


if __name__=='__main__':
    main()
