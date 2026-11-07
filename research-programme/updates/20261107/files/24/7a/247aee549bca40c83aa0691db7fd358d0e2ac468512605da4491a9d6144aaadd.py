from stage154_anchor_common import *
from compare_steps import state_difference
from repair_readout_cancellation import precise_readout


def main():
    modest()
    folder=ROOT/'results/comparison'
    folder.mkdir(parents=True,exist_ok=False)
    allowed=verify_packet(ROOT/'results/readiness')['allowed_routes']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    checks,inputs,readouts,comparisons=[],[ROOT/'results/readiness/status.json',*ladder.inputs],{},{}
    groups={'central':slice(0,2),'revised':slice(2,4),'increment':slice(4,6)}
    components={anchor+'_'+key:slice(12+2*position,14+2*position)
        for position,(anchor,key) in enumerate((anchor,key) for anchor in ANCHORS for key in COMPONENTS)}
    maximum_precision=0.
    maximum_direct_projection=0.
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            if not allowed[route]:
                continue
            states={}
            for count in COUNTS:
                location=ROOT/'results/response'/f'{model}-{route}-{count}'
                packet=verify_packet(location)
                assert packet['all_checks_passed']
                heat=packet['heat']
                final=read_npz(location/'response.npz')
                states[count]=final
                original,revised,increment=[reader.values@final['photon'][-1,:,selection] for selection in groups.values()]
                original_energy,revised_energy,increment_energy=[final['energy'][-1,selection] for selection in groups.values()]
                for match in [20,40]:
                    prior_path=SOURCE152/'results/comparison'/f'{model}-m{match}-{route}-order6-4096.npz'
                    reference_path=STAGE150/'results/comparison'/f'{model}-m{match}-{route}-4096.npz'
                    prior=read_npz(prior_path)
                    reference=read_npz(reference_path)
                    baseline,older=prior['potential'][:,:1],prior['potential'][:,1:3]
                    baseline_energy,old_energy=prior['energy'][:1],prior['energy'][1:3]
                    potential=np.column_stack([baseline,older,original,revised,older+original,older+revised,
                        baseline+older+original,baseline+older+revised,increment,
                        *[reader.values@final['photon'][-1,:,selection] for selection in components.values()]])
                    energy=np.r_[baseline_energy,old_energy,original_energy,revised_energy,
                        old_energy+original_energy,old_energy+revised_energy,
                        baseline_energy+old_energy+original_energy,baseline_energy+old_energy+revised_energy,increment_energy,
                        *[final['energy'][-1,selection] for selection in components.values()]]
                    split=reader.split_values(potential,energy)
                    label=f'{model}-m{match}-{route}-{count}'
                    inherited.invariants(checks,reader,split,label)
                    assert np.array_equal(potential[:,:3],prior['potential'][:,:3])
                    assert np.array_equal(split['amplitudes'][:,:1],prior['amplitudes'][:,:1])
                    checks.append(dict(name='Exact saved baseline and older MTS:'+label,passed=True))
                    metrics=inherited.metrics(reader,split,heat)
                    fixed={name:abs(heat*reference['amplitudes'][position,9:11])
                        for position,name in enumerate(['mu','y'])}
                    component_budget={}
                    anchor_budget={}
                    for name in ['mu','y']:
                        values=np.asarray(metrics[name])
                        component_budget[name]=(sum(abs(values[position:position+2]) for position in range(17,29,2))/fixed[name]).tolist()
                        anchor_budget[name]={anchor:(sum(abs(values[position:position+2]) for position in range(start,start+6,2))/fixed[name]).tolist()
                            for anchor,start in [('warm',17),('centre',23)]}
                    rearranged=np.zeros((700,17))
                    rearranged_energy=np.zeros(17)
                    for destination,origin in [(slice(0,1),slice(0,1)),(slice(1,3),slice(7,9)),
                        (slice(3,5),slice(9,11)),(slice(5,7),slice(11,13)),
                        (slice(7,9),slice(13,15)),(slice(9,11),slice(15,17))]:
                        rearranged[:,destination]=potential[:,origin]
                        rearranged_energy[destination]=energy[origin]
                    high=precise_readout(dict(potential=rearranged,energy=rearranged_energy),reader)
                    maximum_precision=max(maximum_precision,high['same_baseline_cancellation'])
                    test(checks,'60digit identical baseline/MTS arithmetic:'+label,high['same_baseline_cancellation'],1e-8)
                    for position,name in enumerate(['mu','y']):
                        direct=high['amplitudes'][position,3:5]
                        saved=split['amplitudes'][position,15:17]
                        relative=float(max(abs(direct-saved)/np.maximum(abs(saved),1e-300)))
                        maximum_direct_projection=max(maximum_direct_projection,relative)
                        test(checks,'Independent60digit small '+name+' projection:'+label,relative,1e-8)
                    np.savez_compressed(folder/(label+'.npz'),**split,frequency=reader.frequency,measure=reader.measure,heat=heat)
                    readouts[label]=dict(metrics=metrics,component_budget=component_budget,
                        per_anchor_budget=anchor_budget,fixed_order4_denominator={name:value.tolist() for name,value in fixed.items()},
                        precision_cancellation=high['same_baseline_cancellation'])
                    inputs.extend([prior_path,reference_path])
                inputs.extend([location/'status.json',location/'response.npz'])
            key=model+'-'+route
            comparisons[key]=dict(state={},spectral={})
            fine=states[4096]
            reference_path=STAGE150/'results/response'/f'{model}-{route}-4096/response.npz'
            reference=read_npz(reference_path)
            inputs.append(reference_path)
            photon_reference=state_norm(reference['photon'][...,10:12],ladder.basis.mass)
            gas_reference=abs(reference['gas'][...,10:12])
            photon_sum=sum(state_norm(fine['photon'][...,selection],ladder.basis.mass) for selection in components.values())
            gas_sum=sum(abs(fine['gas'][...,selection]) for selection in components.values())
            sensitivity=dict(photon_endpoint=(photon_sum[-1]/photon_reference[-1]).tolist(),
                photon_history_over_peak=(photon_sum.max(axis=0)/photon_reference.max(axis=0)).tolist(),
                gas_endpoint_over_peak=(gas_sum[-1]/gas_reference.max(axis=0)).tolist(),
                gas_history_over_peak=(gas_sum.max(axis=0)/gas_reference.max(axis=0)).tolist())
            comparisons[key]['sensitivity']=sensitivity
            for name,values in sensitivity.items():
                test(checks,'RESPONSE_SENSITIVITY:'+key+':'+name,float(max(values)),.01)
            for group,selection in {**groups,**components}.items():
                record=state_difference(states[2048],states[4096],selection,ladder.basis.mass)
                comparisons[key]['state'][group]=record
                for name,values in record['relative'].items():
                    test(checks,'CONVERGENCE:'+key+':'+group+':'+name,float(max(values)),.01)
            for match in [20,40]:
                prefix=f'{model}-m{match}-{route}'
                records={}
                for name in ['mu','y']:
                    coarse=np.asarray(readouts[prefix+'-2048']['metrics'][name])
                    fine_values=np.asarray(readouts[prefix+'-4096']['metrics'][name])
                    assert np.array_equal(coarse[:3],fine_values[:3])
                    selections={'central':slice(3,5),'revised':slice(5,7),'increment':slice(15,17),
                        **{component:slice(17+2*position,19+2*position) for position,component in enumerate(components)}}
                    records[name]={}
                    for group,selection in selections.items():
                        change=abs(fine_values[selection]-coarse[selection])/np.maximum(abs(fine_values[selection]),1e-300)
                        records[name][group]=change.tolist()
                        test(checks,'CONVERGENCE:'+prefix+':'+name+':'+group,float(max(change)),.01)
                    test(checks,'RESPONSE_SENSITIVITY:'+prefix+':'+name,
                        max(readouts[prefix+'-4096']['component_budget'][name]),.01)
                comparisons[key]['spectral'][str(match)]=records
    finish(folder,dict(checks=checks,allowed_routes=allowed,comparisons=comparisons,readouts=readouts,
        maximum_precision_cancellation=maximum_precision,maximum_direct_projection=maximum_direct_projection,
        response_steps=COUNTS,modes=96,baseline_preserved=True,baseline_inner_history_refined=False,
        curve_adopted=False,cold_anchor_fixed=True,columns=29,
        convergence_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:'))),
        __file__,inputs)
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],
        precision_cancellation=maximum_precision,direct_projection=maximum_direct_projection)),flush=True)


if __name__=='__main__':
    main()
