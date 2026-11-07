from stage162_common import *


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    source_packet=verify_packet(ROOT/'results/sources')
    assert source_packet['all_checks_passed']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    checks,inputs,records=[],[*ladder.inputs,ROOT/'results/sources/status.json'],{}
    maximum_precision=maximum_svd=0.
    previous_owners=[SOURCE155,SOURCE158,SOURCE159,PARENT]
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            states={}
            for count in COUNTS:
                location=ROOT/'results/response'/f'{model}-{route}-{count}'
                proof=verify_packet(location)
                assert proof['all_checks_passed']
                current=read_npz(location/'response.npz')
                states[count]=current
                inputs.extend([location/'status.json',location/'response.npz'])
                old={}
                for owner in previous_owners:
                    path=owner/'results/response'/f'{model}-{route}-{count}/response.npz'
                    previous=read_npz(path)
                    assert np.array_equal(current['coordinate'],previous['coordinate'])
                    columns=slice(10,12) if owner==SOURCE155 else slice(2,4)
                    for key in ['photon','gas','energy','work','number','integrated_number_source']:
                        old[key]=old.get(key,0)+previous[key][...,columns]
                    inputs.append(path)
                label=f'{model}-{route}-{count}'
                state_metrics={}
                for quantity in ['photon','gas']:
                    measure=lambda value:state_norm(value,ladder.basis.mass) if quantity=='photon' else abs(value)
                    reference=measure(old[quantity]).max(axis=0)
                    first=measure(current[quantity][...,22:24])
                    last=measure(current[quantity][...,16:18])
                    total=measure(current[quantity][...,2:4])
                    state_metrics[quantity]=dict(
                        cumulative_history_over_saved_peak=(total.max(axis=0)/reference).tolist(),
                        cumulative_endpoint_over_saved_peak=(total[-1]/reference).tolist(),
                        last_over_first_history=(last.max(axis=0)/first.max(axis=0)).tolist(),
                        last_endpoint_over_saved_peak=(last[-1]/reference).tolist())
                energy=old['energy']+current['energy'][...,2:4]
                gas=old['gas']+current['gas'][...,2:4]
                work=old['work']+current['work'][...,2:4]
                balance=energy+proof['heat']*gas+work
                normalization=np.maximum(np.max(abs(energy)+abs(proof['heat']*gas)+abs(work),axis=0),1e-300)
                test(checks,'Counterfactual energy/work:'+label,float(max(np.max(abs(balance-balance[0]),axis=0)/normalization)),1e-7)
                readouts={}
                for match in [20,40]:
                    prior_path=PARENT/'results/comparison'/f'{label}-m{match}.npz'
                    prior=read_npz(prior_path)
                    inputs.append(prior_path)
                    baseline=prior['potential'][:,:1]
                    saved_mts=prior['potential'][:,3:5]
                    saved_energy=prior['energy'][3:5]
                    for step,columns,pieces in [
                        ('54',slice(22,24),[18,20]),('64',slice(2,4),[0,4]),('65',slice(16,18),[12,14])]:
                        first=reader.values@current['photon'][-1,:,22:24] if step=='65' else np.zeros_like(saved_mts)
                        first_energy=current['energy'][-1,22:24] if step=='65' else np.zeros_like(saved_energy)
                        before=saved_mts+first
                        before_energy=saved_energy+first_energy
                        increment=reader.values@current['photon'][-1,:,columns]
                        increment_energy=current['energy'][-1,columns]
                        after=before+increment
                        after_energy=before_energy+increment_energy
                        parts=[reader.values@current['photon'][-1,:,start:start+2] for start in pieces]
                        potential=np.column_stack([baseline,before,after,baseline+before,baseline+after,increment,*parts])
                        energy_read=np.r_[prior['energy'][:1],before_energy,after_energy,
                            prior['energy'][:1]+before_energy,prior['energy'][:1]+after_energy,
                            increment_energy,*[current['energy'][-1,start:start+2] for start in pieces]]
                        split=reader.split_values(potential,energy_read)
                        key=label+f'-m{match}-step{step}'
                        inherited.invariants(checks,reader,split,key)
                        assert np.array_equal(split['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                        assert np.array_equal(potential[:,:1],prior['potential'][:,:1])
                        if step!='65':
                            assert np.array_equal(potential[:,1:3],prior['potential'][:,3:5])
                        precise=precise_readout(dict(potential=potential,energy=energy_read),reader)
                        maximum_precision=max(maximum_precision,precise['same_baseline_cancellation'])
                        test(checks,'60digit paired baseline/MTS:'+key,precise['same_baseline_cancellation'],1e-8)
                        close(checks,'60digit direct increment amplitudes:'+key,precise['amplitudes'][:,3:5],split['amplitudes'][:,9:11],1e-8)
                        close(checks,'60digit direct increment residual:'+key,precise['residual'][:,3:5],split['residual'][:,9:11],1e-10)
                        alternate=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                            np.sqrt(reader.measure)[:,None]*split['distortion'],rcond=None)[0]
                        difference=np.linalg.norm(np.sqrt(reader.measure)[:,None]*(reader.templates@(alternate-split['amplitudes'])),axis=0)
                        normalization=np.maximum(np.linalg.norm(np.sqrt(reader.measure)[:,None]*split['distortion'],axis=0),1e-300)
                        maximum_svd=max(maximum_svd,float(max(difference/normalization)))
                        readouts[f'{match}-step{step}']=dict(
                            mu_increment=(proof['heat']*split['amplitudes'][0,9:11]).tolist(),
                            y_increment=(proof['heat']*split['amplitudes'][1,9:11]).tolist(),
                            mu_over_saved_mts=(abs(split['amplitudes'][0,9:11])/abs(prior['amplitudes'][0,3:5])).tolist(),
                            y_over_saved_mts=(abs(split['amplitudes'][1,9:11])/abs(prior['amplitudes'][1,3:5])).tolist(),
                            baseline_preserved=True,curve_adopted=False)
                        np.savez_compressed(folder/(key+'.npz'),**split,frequency=reader.frequency,measure=reader.measure,heat=proof['heat'])
                records[label]=dict(state=state_metrics,readouts=readouts)
            step_metrics={}
            for name,columns in [('start64',slice(0,2)),('total64',slice(2,4)),('end64',slice(4,6)),
                                 ('start65',slice(12,14)),('end65',slice(14,16)),('total65',slice(16,18)),
                                 ('start54',slice(18,20)),('end54',slice(20,22)),('total54',slice(22,24))]:
                step_metrics[name]={}
                for quantity in ['photon','gas']:
                    measure=lambda value:state_norm(value,ladder.basis.mass) if quantity=='photon' else abs(value)
                    fine=states[4096][quantity][...,columns]
                    coarse=states[2048][quantity][...,columns]
                    ratio=measure(fine[::2]-coarse).max(axis=0)/np.maximum(measure(fine).max(axis=0),1e-300)
                    step_metrics[name][quantity]=ratio.tolist()
                    test(checks,'CONVERGENCE:'+model+':'+route+':'+name+':'+quantity,float(max(ratio)),.01)
            records[model+'-'+route+'-steps']=step_metrics
    test(checks,'Independent weighted SVD',maximum_svd,1e-10)
    numerical=all(row['passed'] for row in checks if not row['name'].startswith('CONVERGENCE:'))
    summary=dict(**source_packet['summary'],
        response=dict(records=records,maximum_precision_cancellation=maximum_precision,maximum_independent_svd=maximum_svd,
            convergence_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:'))),
        numerical_integrity_passed=numerical,new_response_evolutions=8,
        baseline_preserved=True,diagnostic_only=True,earlier_window_history_fixed=True,
        next_target='Choose from the measured endpoint contraction and combined uncertainty;keep the adopted temperature curve fixed until numerical allowance is understood.')
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    finish(folder,dict(checks=checks,numerical_integrity_passed=numerical,records=records,
        maximum_precision_cancellation=maximum_precision,maximum_independent_svd=maximum_svd),__file__,
        [*inputs,ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
        max_precision=maximum_precision,max_svd=maximum_svd)),flush=True)
    assert numerical


if __name__=='__main__':
    main()
