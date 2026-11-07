from stage157_common import *
import argparse


def source_analysis(data,checks,folder,register):
    factor=np.linalg.cholesky(data['mass'])
    def norm(value):
        value=np.asarray(value)
        shape=value.shape
        whitened=np.linalg.solve(factor,np.moveaxis(value[...,1:-1,:],-2,0).reshape(96,-1))
        return np.linalg.norm(whitened,axis=0).reshape(shape[:-2]+(shape[-1],))
    scale=norm(data['actual'])
    bank_records={}
    banks={}
    consumed_nodes=set()
    consumed_loops=set()
    shared_count=0
    wrong_weight_bias=None
    for order in ORDERS:
        site_arrays=[]
        nodes_rule=list(incoming_rule(order,BOUNDARIES[0],BOUNDARIES[-1]))
        frequencies=np.asarray([row[0] for row in nodes_rule])
        seed_weights=np.asarray([row[1] for row in nodes_rule])
        panel_ids=np.repeat(np.arange(7),order)
        for site in SITES:
            location=bank_folder(site,order)
            config_path=location/'configuration.json'
            register(config_path)
            register(location/'status.json')
            config=json.loads(config_path.read_text())
            theta=config['temperature'] if order==4 else config['theta']
            nodes=list(integration_nodes(theta,order))
            if order==4:
                assert nodes==list(physical_nodes(theta,'expensive'))
            assert len(nodes)==7*order*36
            terms=[[] for frequency in frequencies]
            indices=[[] for frequency in frequencies]
            bad_terms=[]
            frequency_index={value:position for position,value in enumerate(frequencies)}
            rows=[0,1,2,97]
            with localcontext() as context:
                context.prec=60
                exact=[[[Decimal(0) for column in range(4)] for row in rows] for frequency in frequencies]
                for node in nodes:
                    path,original,reused=node_path(site,order,node,config,theta)
                    register(path)
                    saved=read_npz(path)
                    assert json.loads(str(saved['identity']))==original
                    assert event_signature(original)==event_signature(node)
                    parameters,weight=parameters_and_weight(theta,node)
                    original_parameters,original_weight=parameters_and_weight(theta,original)
                    assert weight>0 and float(saved['weight'])==original_weight
                    assert event_owner.inherited.virtual_identity(parameters)==event_owner.inherited.virtual_identity(original_parameters)
                    loop_path=Path(str(saved['loop_path']))
                    assert loop_path.is_relative_to(path.parents[4]/'virtual-cache')
                    register(loop_path)
                    loop=json.loads(loop_path.read_text())
                    assert loop['finite'] and loop['scalar']==float(saved['loop_scalar'])
                    assert loop['identity']==event_owner.inherited.virtual_identity(parameters)
                    value=saved['virtual']
                    assert value.shape==(98,4) and np.isfinite(value).all()
                    slot=frequency_index[node['frequency']]
                    assert node['seed_weight']==seed_weights[slot]
                    terms[slot].append(-weight*value)
                    indices[slot].append((node['electron_index'],node['cosine']))
                    for position,row in enumerate(rows):
                        for column in range(4):
                            exact[slot][position][column]+=Decimal.from_float(-weight)*Decimal.from_float(float(value[row,column]))
                    if reused:
                        shared_count+=1
                        bad_terms.append((weight-original_weight)*value)
                    consumed_nodes.add(str(path))
                    consumed_loops.add(str(loop_path))
                values=np.asarray([stable_sum(group) for group in terms])
                assert all(len(group)==36 and len(set(group))==36 for group in indices)
                assert all(group==indices[0] for group in indices)
                for slot in range(len(frequencies)):
                    values[slot,rows]=[[float(value) for value in row] for row in exact[slot]]
            total=stable_sum(values)
            expected=virtual_reference(data,site,order)
            test(checks,'Saved virtual total replay:'+site+':'+str(order),
                float(max(norm(total-expected)/scale)),1e-10)
            if bad_terms:
                wrong_weight_bias=(norm(stable_sum(bad_terms))/scale).tolist()
                assert min(wrong_weight_bias)>1e-8
                checks.append(dict(name='Old-order weights fail detectable shared-node control',passed=True))
            panels=np.asarray([stable_sum(values[panel_ids==panel]) for panel in range(7)])
            close(checks,'Panels sum to full virtual vector:'+site+':'+str(order),stable_sum(panels),total,1e-12)
            label=site+'-'+str(order)
            bank_records[label]=dict(theta=theta,nodes=len(nodes),frequency_count=len(frequencies),
                nodes_per_frequency=36,own_site_weights_retained=True,
                reference_replay_over_coldS4=(norm(total-expected)/scale).tolist(),
                virtual_norm_over_coldS4=(norm(total)/scale).tolist())
            site_arrays.append(values)
            print(json.dumps(dict(saved_virtual_bank=label,nodes=len(nodes))),flush=True)
        site_values=np.asarray(site_arrays)
        joint=site_values[0]+site_values[1]-1.5*site_values[2]
        panels=np.asarray([[stable_sum(values[panel_ids==panel]) for panel in range(7)] for values in site_values])
        joint_panels=panels[0]+panels[1]-1.5*panels[2]
        total=stable_sum(joint_panels)
        separated=np.sum(norm(site_values)*abs(COEFFICIENTS)[:,None,None],axis=0)
        joint_frequency_norm=norm(joint)
        separate_total=separated.sum(axis=0)
        joint_frequency_total=joint_frequency_norm.sum(axis=0)
        joint_panel_total=norm(joint_panels).sum(axis=0)
        coherent=norm(total)
        for first,second,label in [(joint_frequency_total,separate_total,'at_frequency'),
            (joint_panel_total,joint_frequency_total,'within_panel'),(coherent,joint_panel_total,'between_panels')]:
            test(checks,'Cancellation triangle:'+str(order)+':'+label,float(max(first/np.maximum(second,1e-300))),1+1e-12)
        panel_records=[]
        for panel in range(7):
            selected=panel_ids==panel
            panel_records.append(dict(panel=panel,bounds=BOUNDARIES[panel:panel+2].tolist(),
                separate_frequency_budget=(separated[selected].sum(axis=0)/scale).tolist(),
                joint_frequency_budget=(joint_frequency_norm[selected].sum(axis=0)/scale).tolist(),
                joint_panel_norm=(norm(joint_panels[panel])/scale).tolist(),
                frequency_coherence=(joint_frequency_norm[selected].sum(axis=0)/separated[selected].sum(axis=0)).tolist(),
                within_panel_coherence=(norm(joint_panels[panel])/joint_frequency_norm[selected].sum(axis=0)).tolist()))
        output=dict(frequencies=frequencies,seed_weights=seed_weights,panel_ids=panel_ids,
            sites=site_values,integrands=site_values/seed_weights[None,:,None,None],
            panels=panels,joint=joint,joint_panels=joint_panels,total=total,mass=data['mass'],scale=scale,
            separate_frequency_norm=separated,joint_frequency_norm=joint_frequency_norm)
        np.savez_compressed(folder/f'order{order}-frequency.npz',**output)
        banks[order]=output
        bank_records['order'+str(order)]=dict(
            separated_frequency_budget=(separate_total/scale).tolist(),
            joint_frequency_budget=(joint_frequency_total/scale).tolist(),
            joint_panel_budget=(joint_panel_total/scale).tolist(),coherent=(coherent/scale).tolist(),
            at_frequency_coherence=(joint_frequency_total/separate_total).tolist(),
            within_panel_coherence=(joint_panel_total/joint_frequency_total).tolist(),
            between_panel_coherence=(coherent/joint_panel_total).tolist(),panels=panel_records)
    steps={}
    previous_delta=None
    for order in [5,6]:
        previous=banks[order-1]
        current=banks[order]
        site_delta=current['panels']-previous['panels']
        joint_delta=site_delta[0]+site_delta[1]-1.5*site_delta[2]
        total=stable_sum(joint_delta)
        expected=sum(weight*(virtual_reference(data,site,order)-virtual_reference(data,site,order-1)) for weight,site in zip(COEFFICIENTS,SITES))
        close(checks,'Panel virtual refinement reproduces saved matched step:'+str(order),total,expected,1e-8)
        panel_norm=norm(joint_delta)
        independent_panel=np.sum(norm(site_delta)*abs(COEFFICIENTS)[:,None,None],axis=0)
        independent_global=sum(abs(weight)*norm(stable_sum(values)) for weight,values in zip(COEFFICIENTS,site_delta))
        panel_sum=panel_norm.sum(axis=0)
        coherent=norm(total)
        test(checks,'Step panel triangle:'+str(order),float(max(coherent/panel_sum)),1+1e-12)
        test(checks,'Step cross-temperature triangle:'+str(order),float(max(panel_sum/independent_panel.sum(axis=0))),1+1e-12)
        signed=np.asarray([np.sum(value[1:-1]*np.linalg.solve(data['mass'],total[1:-1]),axis=0)/coherent**2 for value in joint_delta])
        close(checks,'Panel signed projections sum to1:'+str(order),signed.sum(axis=0),np.ones(4),1e-10)
        share=panel_norm/panel_sum
        rankings=list(np.argsort(-share.mean(axis=1)).astype(int))
        rows=[]
        for panel in range(7):
            record=dict(panel=panel,bounds=BOUNDARIES[panel:panel+2].tolist(),
                joint_step_norm_over_coldS4=(panel_norm[panel]/scale).tolist(),
                independent_site_step_budget_over_coldS4=(independent_panel[panel]/scale).tolist(),
                cross_temperature_coherence=(panel_norm[panel]/np.maximum(independent_panel[panel],1e-300)).tolist(),
                share_of_joint_panel_budget=share[panel].tolist(),
                signed_projection_on_total=signed[panel].tolist())
            if previous_delta is not None:
                earlier=norm(previous_delta[panel])
                record['observed_step_ratio']=(panel_norm[panel]/np.maximum(earlier,1e-300)).tolist()
                record['ratio_resolved_above_roundoff']=(earlier>1e-12*norm(stable_sum(previous_delta))).tolist()
            rows.append(record)
        steps[str(order)]=dict(independent_global_budget=(independent_global/scale).tolist(),
            independent_panel_budget=(independent_panel.sum(axis=0)/scale).tolist(),
            joint_panel_budget=(panel_sum/scale).tolist(),coherent=(coherent/scale).tolist(),
            cross_temperature_coherence=(panel_sum/independent_panel.sum(axis=0)).tolist(),
            between_panel_coherence=(coherent/panel_sum).tolist(),panels=rows,
            ranking_by_mean_panel_norm_share=[int(value) for value in rankings])
        if previous_delta is not None:
            steps[str(order)]['coherent_step_ratio']=(coherent/norm(stable_sum(previous_delta))).tolist()
        np.savez_compressed(folder/f'step{order}-panels.npz',site_delta=site_delta,joint_delta=joint_delta,
            total=total,panel_norm=panel_norm,signed_projections=signed,scale=scale,mass=data['mass'])
        previous_delta=joint_delta
    assert shared_count==252 and len(consumed_nodes)==11340
    checks.append(dict(name='11340 existing event values;252cold5 shared values use correct new weights',passed=True))
    return dict(banks=bank_records,steps=steps,reused_event_files=len(consumed_nodes),
        reused_loop_files=len(consumed_loops),order3_shared_values=shared_count,
        wrong_shared_weights_bias_over_coldS4=wrong_weight_bias,
        common_incoming_coordinate=True,temperature_specific_weights_preserved=True,
        per_frequency_response_available=False,continuum_cancellation_bound_established=False)


def response_analysis(checks,folder,inputs):
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    inputs.extend(ladder.inputs)
    reader=ShapeReadout(ladder.basis,canonical=True)
    records={}
    maximum_precision=maximum_svd=0.
    quantities=['photon','gas','energy','work','number','integrated_number_source']
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            by_count={}
            for count in COUNTS:
                paths=[stage156_parent.location(stage,model,route,count)/'response.npz'
                    for stage in [STAGE150,STAGE151,SOURCE152,SOURCE154,SOURCE155]]
                original,cold5,cold6,anchor5,anchor6=[read_npz(path) for path in paths]
                metadata=verify_packet(stage156_parent.location(SOURCE155,model,route,count))
                heat=metadata['heat']
                previous={key:original[key][...,10:12] for key in quantities}
                accumulated={key:np.zeros_like(previous[key]) for key in quantities}
                for order,cold,anchor in [(5,cold5,anchor5),(6,cold6,anchor6)]:
                    virtual,rest,parts,without,current={},{},{},{},{}
                    for key in quantities:
                        parts[key]=[cold[key][...,14:16],anchor[key][...,14:16],anchor[key][...,20:22]]
                        virtual[key]=sum(parts[key])
                        rest[key]=sum(cold[key][...,start:start+2] for start in [12,16])+sum(anchor[key][...,start:start+2] for start in [12,16,18,22])
                        delta=cold[key][...,4:6]+anchor[key][...,4:6]
                        accumulated[key]+=delta
                        close(checks,'Virtual plus D/S equals full saved increment:'+model+':'+route+':'+str(count)+':'+str(order)+':'+key,virtual[key]+rest[key],delta,1e-8)
                        without[key]=previous[key]+rest[key]
                        current[key]=previous[key]+delta
                        expected=anchor5[key][...,10:12]-cold6[key][...,4:6] if order==5 else anchor6[key][...,10:12]
                        close(checks,'Exact matched history replay:'+model+':'+route+':'+str(count)+':'+str(order)+':'+key,current[key],expected,1e-10)
                    balance=virtual['energy']+heat*virtual['gas']+virtual['work']
                    denominator=np.maximum(np.max(abs(virtual['energy'])+abs(heat*virtual['gas'])+abs(virtual['work']),axis=0),1e-300)
                    test(checks,'Virtual-only energy/work:'+model+':'+route+':'+str(count)+':'+str(order),float(np.max(abs(balance-balance[0])/denominator)),1e-7)
                    state={}
                    for key in ['photon','gas']:
                        measure=lambda values:state_norm(values,ladder.basis.mass) if key=='photon' else abs(values)
                        reference=measure(original[key][...,10:12])
                        coherent=measure(virtual[key])
                        budget=sum(measure(value) for value in parts[key])
                        denominator=reference[-1] if key=='photon' else reference.max(axis=0)
                        state[key]=dict(coherent_endpoint_over_S4=(coherent[-1]/denominator).tolist(),
                            independent_endpoint_over_S4=(budget[-1]/denominator).tolist(),
                            endpoint_coherence=(coherent[-1]/np.maximum(budget[-1],1e-300)).tolist(),
                            coherent_history_over_S4_peak=(coherent.max(axis=0)/reference.max(axis=0)).tolist())
                        test(checks,'Virtual response triangle:'+model+':'+route+':'+str(count)+':'+str(order)+':'+key,float(max(coherent[-1]/np.maximum(budget[-1],1e-300))),1+1e-10)
                    by_count[count,order]={key:virtual[key] for key in ['photon','gas']}
                    label=f'{model}-{route}-{count}-order{order}'
                    readouts={}
                    for match in [20,40]:
                        old=read_npz(STAGE150/'results/comparison'/f'{model}-m{match}-{route}-{count}.npz')
                        last=read_npz(SOURCE155/'results/comparison'/f'{model}-m{match}-{route}-{count}.npz')
                        assert np.array_equal(old['potential'][:,:3],last['potential'][:,:3])
                        baseline=old['potential'][:,:1]
                        second=old['potential'][:,9:11]+reader.values@accumulated['photon'][-1]
                        delta=reader.values@virtual['photon'][-1]
                        first=second-delta
                        potential=np.column_stack([baseline,first,second,baseline+first,baseline+second,delta,
                            *[reader.values@value[-1] for value in parts['photon']]])
                        current_energy=old['energy'][9:11]+accumulated['energy'][-1]
                        without_energy=current_energy-virtual['energy'][-1]
                        energy=np.r_[old['energy'][:1],without_energy,current_energy,
                            old['energy'][:1]+without_energy,old['energy'][:1]+current_energy,
                            virtual['energy'][-1],*[value[-1] for value in parts['energy']]]
                        split=reader.split_values(potential,energy)
                        name=label+'-m'+str(match)
                        inherited.invariants(checks,reader,split,name)
                        assert np.array_equal(split['amplitudes'][:,:1],old['amplitudes'][:,:1])
                        if order==6:
                            close(checks,'Actual latest MTS readout replay:'+name,second,last['potential'][:,9:11],1e-10)
                            close(checks,'Actual latest energy readout replay:'+name,current_energy,last['energy'][9:11],1e-10)
                        precise=precise_readout(dict(potential=potential,energy=energy),reader)
                        maximum_precision=max(maximum_precision,precise['same_baseline_cancellation'])
                        test(checks,'60digit paired baseline/MTS virtual update:'+name,precise['same_baseline_cancellation'],1e-8)
                        close(checks,'60digit independent virtual amplitudes:'+name,precise['amplitudes'][:,3:5],split['amplitudes'][:,9:11],1e-8)
                        close(checks,'60digit independent baseline:'+name,precise['amplitudes'][:,:1],split['amplitudes'][:,:1],1e-10)
                        close(checks,'60digit independent virtual residual:'+name,precise['residual'][:,3:5],split['residual'][:,9:11],1e-10)
                        alternate=np.linalg.lstsq(np.sqrt(reader.measure)[:,None]*reader.templates,
                            np.sqrt(reader.measure)[:,None]*split['distortion'],rcond=None)[0]
                        numerator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*(reader.templates@(alternate-split['amplitudes'])),axis=0)
                        denominator=np.linalg.norm(np.sqrt(reader.measure)[:,None]*split['distortion'],axis=0)
                        maximum_svd=max(maximum_svd,float(max(numerator/np.maximum(denominator,1e-300))))
                        rows={}
                        for position,key in enumerate(['mu','y']):
                            amplitudes=split['amplitudes'][position]
                            denominator=abs(old['amplitudes'][position,9:11])
                            budget=sum(abs(amplitudes[start:start+2]) for start in [11,13,15])
                            coherent=abs(amplitudes[9:11])
                            rows[key]=dict(signed_amplitude=(heat*amplitudes[9:11]).tolist(),
                                coherent_over_S4=(coherent/denominator).tolist(),
                                independent_over_S4=(budget/denominator).tolist(),
                                coherence=(coherent/np.maximum(budget,1e-300)).tolist())
                        readouts[str(match)]=rows
                        np.savez_compressed(folder/(name+'-readout.npz'),**split,frequency=reader.frequency,measure=reader.measure,heat=heat)
                    records[label]=dict(state=state,readouts=readouts,
                        response_scope='Sum of saved bH/J_W/J_C virtual response slots;no second application of source-point coefficients',
                        readout_convention='Saved Stage150 accumulated readout plus matched saved increments;not direct projection of combined history',
                        frequency_resolved_response=False,baseline_inner_rerun=False)
                    previous=current
                print(json.dumps(dict(virtual_response_reused=model+'-'+route+'-'+str(count))),flush=True)
            for order in [5,6]:
                rows={}
                for key in ['photon','gas']:
                    measure=lambda value:state_norm(value,ladder.basis.mass) if key=='photon' else abs(value)
                    coarse=by_count[2048,order][key]
                    fine=by_count[4096,order][key]
                    relative=measure(fine[::2]-coarse).max(axis=0)/np.maximum(measure(fine).max(axis=0),1e-300)
                    rows[key]=relative.tolist()
                    test(checks,'CONVERGENCE:virtual response:'+model+':'+route+':'+str(order)+':'+key,float(max(relative)),.01)
                records[f'{model}-{route}-order{order}-steps']=rows
    test(checks,'Independent weightedSVD',maximum_svd,1e-10)
    return dict(records=records,maximum_precision_cancellation=maximum_precision,
        maximum_independent_svd=maximum_svd,baseline_preserved=True,baseline_inner_rerun=False,
        new_evolutions=0,frequency_resolved_response_available=False)


def main():
    modest()
    parser=argparse.ArgumentParser()
    parser.add_argument('--dry-run',action='store_true')
    parser.add_argument('--reuse-sources',type=Path)
    args=parser.parse_args()
    inputs=planned_inputs()
    assert all(path.is_file() for path in inputs)
    if args.dry_run:
        print(json.dumps(dict(inputs=len(inputs),all_exist=True,expected_event_reuses=11340,
            new_events=0,new_trajectories=0,outputs_written=False)))
        return
    folder=ROOT/'results/analysis'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    assert sum(len(packet['file_hashes']) for packet in chain.values())==INHERITED_PAYLOADS
    checked={}
    def register(path):
        path=Path(path).resolve()
        if str(path) in checked:
            return
        if path in chain:
            assert json.loads(path.read_text())==chain[path]
            checked[str(path)]=digest(path)
            inputs.append(path)
            return
        relative=path.relative_to(BRANCH)
        owner=BRANCH/relative.parts[0]
        seal=owner/'results/stage-integrity.json'
        expected=chain[seal]['file_hashes'][path.relative_to(owner).as_posix()]
        actual=digest(path)
        assert actual==expected,path
        checked[str(path)]=actual
        inputs.append(path)
    for filename in chain[PARENT/'results/stage-integrity.json']['file_hashes']:
        register(PARENT/filename)
    for path in list(inputs):
        register(path)
    checks=[dict(name='Immediate Stage156 and saved input provenance verified',passed=True)]
    data=read_npz(SOURCE155/'results/anchor-sources/source.npz')
    if args.reuse_sources:
        previous_folder=args.reuse_sources.resolve()
        assert previous_folder.is_relative_to(ROOT) and previous_folder!=folder
        prior=json.loads((previous_folder/'status.json').read_text())
        summary_path=previous_folder/'NUMERICAL-SUMMARY.json'
        assert digest(summary_path)==prior['input_hashes'][str(ROOT/'NUMERICAL-SUMMARY.json')]
        assert digest(previous_folder/'combine_virtual.initial.txt')==prior['script_sha256']
        for filename,sha in prior['input_hashes'].items():
            path=Path(filename)
            if not path.is_relative_to(ROOT):
                assert digest(path)==sha
                register(path)
        for name in ['order4-frequency.npz','order5-frequency.npz','order6-frequency.npz','step5-panels.npz','step6-panels.npz']:
            source_path=previous_folder/name
            assert digest(source_path)==prior['input_hashes'][str(folder/name)]
            (folder/name).write_bytes(source_path.read_bytes())
            inputs.append(source_path)
        first_response=next(position for position,row in enumerate(prior['checks']) if row['name'].startswith('Virtual plus D/S'))
        source_checks=prior['checks'][1:first_response]
        assert all(row['passed'] for row in source_checks)
        checks.extend(source_checks)
        sources=json.loads(summary_path.read_text())['source']
        inputs.extend([previous_folder/'status.json',summary_path,previous_folder/'combine_virtual.initial.txt'])
        checks.append(dict(name='Hashed completed source reconstruction reused;failed initial readout convention retained',passed=True))
    else:
        sources=source_analysis(data,checks,folder,register)
    response=response_analysis(checks,folder,inputs)
    numerical=all(row['passed'] for row in checks if not row['name'].startswith('CONVERGENCE:'))
    summary=dict(stage=157,source=sources,response=response,numerical_integrity_passed=numerical,
        all_time_step_checks_passed=all(row['passed'] for row in checks if row['name'].startswith('CONVERGENCE:')),
        new_physical_events=0,new_virtual_coefficients=0,new_response_evolutions=0,
        temperature_curve_changed=False,continuum_error_certified=False,
        next_target='Use the latest joint-panel virtual refinement ranking to target the dominant common-frequency contribution while keeping physical source weights and the temperature curve fixed.')
    write_json(ROOT/'NUMERICAL-SUMMARY.json',summary)
    finish(folder,dict(checks=checks,numerical_integrity_passed=numerical,new_events=0,new_trajectories=0,
        consumed_paths_verified=len(checked),baseline_preserved=True,temperature_curve_changed=False),
        __file__,[*inputs,*folder.glob('*.npz'),ROOT/'NUMERICAL-SUMMARY.json'])
    print(json.dumps(dict(checks=len(checks),numerical=numerical,failed=[row for row in checks if not row['passed']],
        dominant_panels=sources['steps']['6']['ranking_by_mean_panel_norm_share'])),flush=True)
    assert numerical


if __name__=='__main__':
    main()
