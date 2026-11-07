from stage147_step_common import *


def contraction_record(first,second,first_relative,second_relative):
    result=[]
    for older,newer,older_relative,newer_relative in zip(first,second,first_relative,second_relative):
        floor=bool(max(older_relative,newer_relative)<1e-10)
        ratio=float(newer/older) if older>0 else None
        order=float(np.log2(older/newer)) if older>0 and newer>0 else None
        result.append(dict(first_absolute=float(older),second_absolute=float(newer),
            contraction=ratio,observed_order=order,numerical_floor=floor,
            passed=bool(floor or newer<older)))
    return result


def state_difference(coarse,fine,selection,mass):
    stride=(len(fine['coordinate'])-1)//(len(coarse['coordinate'])-1)
    assert stride==2
    assert np.allclose(coarse['coordinate'],fine['coordinate'][::stride],rtol=0,atol=1e-14)
    fine_photon=fine['photon'][...,selection]
    difference=fine_photon[::stride]-coarse['photon'][...,selection]
    fine_norm=photon_norm(fine_photon,mass)
    difference_norm=photon_norm(difference,mass)
    fine_gas=fine['gas'][...,selection]
    gas_difference=abs(fine_gas[::stride]-coarse['gas'][...,selection])
    absolute=dict(photon_endpoint=difference_norm[-1],photon_trajectory=np.max(difference_norm,axis=0),
        gas_endpoint=gas_difference[-1],gas_trajectory=np.max(gas_difference,axis=0))
    scale=dict(photon_endpoint=fine_norm[-1],photon_trajectory=np.max(fine_norm,axis=0),
        gas_endpoint=np.max(abs(fine_gas),axis=0),gas_trajectory=np.max(abs(fine_gas),axis=0))
    return dict(absolute={key:value.tolist() for key,value in absolute.items()},
        relative={key:(value/np.maximum(scale[key],1e-300)).tolist() for key,value in absolute.items()},
        fine_scale={key:value.tolist() for key,value in scale.items()},
        gas_endpoint_signed_difference=(fine_gas[-1]-coarse['gas'][-1,selection]).tolist(),
        coordinate_max_difference=float(np.max(abs(coarse['coordinate']-fine['coordinate'][::stride]))))


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    parent_readout_path=PARENT/'results/spectral-readout/status.json'
    parent_readout=json.loads(parent_readout_path.read_text())
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    checks,inputs,states,readouts,rows=[],[parent_readout_path,*ladder.inputs],{},{},{}
    for model in ['heavy','cold']:
        heat=parent_readout['metadata'][model]['heat']
        states[model]={}
        for count in COUNTS:
            states[model][count]={}
            for phase in ['active','transfer']:
                location=response_folder(model,count,phase)
                assert verify_packet(location)['all_checks_passed']
                states[model][count][phase]=read_npz(location/'response.npz')
                inputs.extend([location/'status.json',location/'response.npz'])
            final=states[model][count]['transfer']
            original,revised,delta=[reader.values@final['photon'][-1,:,GROUPS[key]] for key in ['original','revised','increment']]
            original_e,revised_e,delta_e=[final['energy'][-1,GROUPS[key]] for key in ['original','revised','increment']]
            for match in [20,40]:
                key=f'{model}-m{match}'
                prior_path=PARENT/'results/spectral-readout'/(key+'-cubic.npz')
                prior=read_npz(prior_path)
                assert np.array_equal(prior['frequency'],reader.frequency)
                assert np.array_equal(prior['measure'],reader.measure)
                base,old=prior['potential'][:,:1],prior['potential'][:,1:3]
                base_e,old_e=prior['energy'][:1],prior['energy'][1:3]
                potential=np.column_stack([base,old,original,revised,old+original,old+revised,
                    base+old+original,base+old+revised,delta])
                energy=np.r_[base_e,old_e,original_e,revised_e,old_e+original_e,old_e+revised_e,
                    base_e+old_e+original_e,base_e+old_e+revised_e,delta_e]
                split=reader.split_values(potential,energy)
                label=key+'-'+str(count)
                inherited.invariants(checks,reader,split,label)
                assert np.array_equal(potential[:,:3],prior['potential'][:,:3])
                assert np.array_equal(split['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                if count==1024:
                    assert np.array_equal(potential,prior['potential'])
                    assert np.array_equal(energy,prior['energy'])
                checks.append(dict(name='Saved nonzero baseline and old window unchanged:'+label,passed=True))
                test(checks,'Direct revised response equals original plus isolated increment:'+label,
                    np.max(abs(revised-original-delta))/np.max(abs(revised)),1e-10)
                test(checks,'Identical baseline/MTS spectral projection:'+label,
                    np.max(abs(split['amplitudes'][:,13:15]-split['amplitudes'][:,:1]-split['amplitudes'][:,9:11]))/
                    max(float(np.max(abs(split['amplitudes'][:,9:11]))),1e-300),1e-8)
                metrics=inherited.metrics(reader,split,heat)
                readouts[label]=dict(metrics=metrics,correction_fraction={name:
                    (np.array(metrics[name])[15:17]/np.array(metrics[name])[7:9]).tolist() for name in ['mu','y']})
                np.savez_compressed(folder/(label+'.npz'),**split,frequency=reader.frequency,measure=reader.measure,heat=heat)
                inputs.append(prior_path)
        rows[model]={}
        for phase in ['active','transfer']:
            rows[model][phase]={}
            for group,selection in GROUPS.items():
                if group=='zero':
                    continue
                pairs=[state_difference(states[model][coarse][phase],states[model][fine][phase],selection,ladder.basis.mass)
                       for coarse,fine in zip(COUNTS[:-1],COUNTS[1:])]
                contractions={metric:contraction_record(pairs[0]['absolute'][metric],pairs[1]['absolute'][metric],
                    pairs[0]['relative'][metric],pairs[1]['relative'][metric]) for metric in pairs[0]['relative']}
                rows[model][phase][group]=dict(pairs=pairs,contractions=contractions)
                for metric,values in pairs[1]['relative'].items():
                    test(checks,'CONVERGENCE:finest state change:'+model+':'+phase+':'+group+':'+metric,max(values),.01)
                    if group=='increment':
                        checks.append(dict(name='CONVERGENCE:isolated state differences shrink:'+model+':'+phase+':'+metric,
                            passed=all(item['passed'] for item in contractions[metric])))
    spectral={}
    selections={'baseline':slice(0,1),'original':slice(3,5),'revised':slice(5,7),
                'combined':slice(9,11),'baseline_plus_mts':slice(13,15),'increment':slice(15,17)}
    for model in ['heavy','cold']:
        for match in [20,40]:
            key=f'{model}-m{match}'
            spectral[key]={}
            for name in ['mu','y']:
                spectral[key][name]={}
                values=[np.array(readouts[key+'-'+str(count)]['metrics'][name]) for count in COUNTS]
                for group,selection in selections.items():
                    amplitudes=[value[selection] for value in values]
                    signed=[fine-coarse for coarse,fine in zip(amplitudes[:-1],amplitudes[1:])]
                    relative=[abs(delta)/np.maximum(abs(fine),1e-300) for delta,fine in zip(signed,amplitudes[1:])]
                    contraction=contraction_record(abs(signed[0]),abs(signed[1]),relative[0],relative[1])
                    spectral[key][name][group]=dict(amplitudes=[value.tolist() for value in amplitudes],
                        signed_changes=[value.tolist() for value in signed],relative_changes=[value.tolist() for value in relative],
                        contractions=contraction)
                    if group=='baseline':
                        checks.append(dict(name='Exact saved baseline amplitude reuse:'+key+':'+name,
                            passed=bool(np.array_equal(amplitudes[0],amplitudes[1]) and np.array_equal(amplitudes[1],amplitudes[2]))))
                    else:
                        test(checks,'CONVERGENCE:finest spectral change:'+key+':'+name+':'+group,max(relative[1]),.01)
                    if group=='increment':
                        checks.append(dict(name='CONVERGENCE:isolated spectral differences shrink:'+key+':'+name,
                            passed=all(item['passed'] for item in contraction)))
    report=dict(checks=checks,state_comparisons=rows,spectral_comparisons=spectral,readouts=readouts,
        column_order=parent_readout['column_order'],metadata=parent_readout['metadata'],counts=COUNTS,modes=96,
        threshold=.01,source_unchanged=True,baseline_preserved=True,
        baseline_inner_history_refined=False,old_window_readout_preserved=True,
        active_and_transfer_both_refined=True,richardson_extrapolation_used=False,
        observed_trend_not_rigorous_error_bound=True,final_epoch=1e-5)
    finish(folder,report,__file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[item for item in checks if not item['passed']],
        increment_state={model:{phase:rows[model][phase]['increment'] for phase in ['active','transfer']} for model in rows},
        increment_spectral={key:{name:spectral[key][name]['increment'] for name in ['mu','y']} for key in spectral})),flush=True)


if __name__=='__main__':
    main()
