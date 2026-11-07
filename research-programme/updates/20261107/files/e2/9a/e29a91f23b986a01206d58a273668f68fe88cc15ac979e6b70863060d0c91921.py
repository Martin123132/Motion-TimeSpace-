from stage157_common import *


def main():
    modest()
    folder=ROOT/'results/validation'
    folder.mkdir(parents=True,exist_ok=False)
    chain=ancestors()
    hashes={}
    def hashed(path):
        path=Path(path).resolve()
        if str(path) not in hashes:
            hashes[str(path)]=digest(path)
        return hashes[str(path)]
    for filename,sha in chain[PARENT/'results/stage-integrity.json']['file_hashes'].items():
        assert hashed(PARENT/filename)==sha
    analysis=json.loads((ROOT/'results/analysis/status.json').read_text())
    assert analysis['state']=='complete' and (ROOT/'results/analysis/COMPLETE').exists()
    assert analysis['numerical_integrity_passed']
    failures=[row for row in analysis['checks'] if not row['passed']]
    assert all(row['name'].startswith('CONVERGENCE:') for row in failures)
    for filename,sha in analysis['input_hashes'].items():
        path=Path(filename)
        assert hashed(path)==sha,path
        if not path.is_relative_to(ROOT):
            inherited.inherited.verify_source(path,chain)
    checks=[dict(name='Complete analysis and sourced input hashes verified',passed=True)]
    inputs=[ROOT/'results/analysis/status.json',ROOT/'NUMERICAL-SUMMARY.json']
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    data=read_npz(SOURCE155/'results/anchor-sources/source.npz')
    def norm(value):
        value=np.asarray(value)
        spectral=np.moveaxis(value[...,1:-1,:],-2,0).reshape(96,-1)
        solved=np.linalg.solve(data['mass'],spectral)
        return np.sqrt(np.maximum(np.sum(spectral*solved,axis=0),0)).reshape(value.shape[:-2]+(value.shape[-1],))
    scale=norm(data['actual'])
    arrays={}
    sampled_events=0
    sampled_reuses=0
    for order in ORDERS:
        path=ROOT/'results/analysis'/f'order{order}-frequency.npz'
        current=read_npz(path)
        arrays[order]=current
        inputs.append(path)
        rule=np.asarray(list(incoming_rule(order,BOUNDARIES[0],BOUNDARIES[-1])))
        assert np.array_equal(current['frequencies'],rule[:,0])
        assert np.array_equal(current['seed_weights'],rule[:,1])
        assert np.array_equal(current['panel_ids'],np.repeat(np.arange(7),order))
        close(checks,'Unweighted integrands reconstruct frequency contributions:'+str(order),
            current['integrands']*rule[:,1][None,:,None,None],current['sites'],1e-12)
        for site_index,site in enumerate(SITES):
            location=bank_folder(site,order)
            config=json.loads((location/'configuration.json').read_text())
            theta=config['temperature'] if order==4 else config['theta']
            nodes=list(integration_nodes(theta,order))
            wanted=[0,len(rule)//2,len(rule)-1]
            for frequency_index in wanted:
                frequency=rule[frequency_index,0]
                selected=[node for node in nodes if node['frequency']==frequency]
                assert len(selected)==36
                with localcontext() as context:
                    context.prec=60
                    exact=[Decimal(0) for position in range(392)]
                    for node in selected:
                        event_path,original,reused=node_path(site,order,node,config,theta)
                        saved=read_npz(event_path)
                        assert json.loads(str(saved['identity']))==original
                        parameters,weight=parameters_and_weight(theta,node)
                        stored_parameters,stored_weight=parameters_and_weight(theta,original)
                        assert float(saved['weight'])==stored_weight
                        assert event_signature(node)==event_signature(original)
                        for position,value in enumerate(saved['virtual'].flat):
                            exact[position]+=Decimal.from_float(-weight)*Decimal.from_float(float(value))
                        sampled_events+=1
                        sampled_reuses+=int(reused)
                    expected=np.asarray([float(value) for value in exact]).reshape(98,4)
                test(checks,'Independent60digit frequency reconstruction:'+site+':'+str(order)+':'+str(frequency_index),
                    float(max(norm(expected-current['sites'][site_index,frequency_index])/scale)),1e-10)
            reconstructed=np.asarray([np.sum(current['sites'][site_index,current['panel_ids']==panel],axis=0) for panel in range(7)])
            close(checks,'Independent panel partition:'+site+':'+str(order),reconstructed,current['panels'][site_index],1e-10)
            test(checks,'Independent saved virtual reference:'+site+':'+str(order),
                float(max(norm(np.sum(reconstructed,axis=0)-virtual_reference(data,site,order))/scale)),1e-10)
        joint=np.einsum('s,sfij->fij',COEFFICIENTS,current['sites'])
        close(checks,'Independent common-frequency combination:'+str(order),joint,current['joint'],1e-12)
        panels=np.asarray([np.sum(joint[current['panel_ids']==panel],axis=0) for panel in range(7)])
        close(checks,'Independent combined panel partition:'+str(order),panels,current['joint_panels'],1e-10)
        separated=np.sum(norm(current['sites'])*abs(COEFFICIENTS)[:,None,None],axis=0)
        source=summary['source']['banks']['order'+str(order)]
        measures={'separated_frequency_budget':separated.sum(axis=0),'joint_frequency_budget':norm(joint).sum(axis=0),
            'joint_panel_budget':norm(panels).sum(axis=0),'coherent':norm(np.sum(panels,axis=0))}
        for name,value in measures.items():
            close(checks,'Independent cancellation budget:'+str(order)+':'+name,value/scale,source[name],1e-10)
        for panel in range(7):
            assert source['panels'][panel]['bounds']==BOUNDARIES[panel:panel+2].tolist()
            selected=current['panel_ids']==panel
            close(checks,'Independent within-frequency panel coherence:'+str(order)+':'+str(panel),
                norm(joint[selected]).sum(axis=0)/separated[selected].sum(axis=0),
                source['panels'][panel]['frequency_coherence'],1e-10)
    assert sampled_events==972 and sampled_reuses==36
    checks.append(dict(name='972independent sampled event products include36shared cold5values with new weights',passed=True))
    previous_delta=None
    for order in [5,6]:
        path=ROOT/'results/analysis'/f'step{order}-panels.npz'
        step=read_npz(path)
        inputs.append(path)
        expected=arrays[order]['panels']-arrays[order-1]['panels']
        close(checks,'Independent site panel refinement:'+str(order),expected,step['site_delta'],1e-10)
        joint=np.einsum('s,spij->pij',COEFFICIENTS,expected)
        close(checks,'Independent joint panel refinement:'+str(order),joint,step['joint_delta'],1e-10)
        total=np.sum(joint,axis=0)
        close(checks,'Independent matched virtual aggregate:'+str(order),total,step['total'],1e-10)
        source=summary['source']['steps'][str(order)]
        panel_norm=norm(joint)
        share=panel_norm/panel_norm.sum(axis=0)
        ranking=list(np.argsort(-share.mean(axis=1)).astype(int))
        assert ranking==source['ranking_by_mean_panel_norm_share']
        for panel in range(7):
            row=source['panels'][panel]
            close(checks,'Independent panel importance:'+str(order)+':'+str(panel),
                share[panel],row['share_of_joint_panel_budget'],1e-10)
            if previous_delta is not None:
                close(checks,'Independent panel observed contraction:'+str(panel),
                    norm(joint[panel])/np.maximum(norm(previous_delta[panel]),1e-300),row['observed_step_ratio'],1e-10)
        previous_delta=joint
    assert summary['source']['reused_event_files']==11340 and summary['source']['order3_shared_values']==252
    assert min(summary['source']['wrong_shared_weights_bias_over_coldS4'])>1e-8
    assert not summary['source']['continuum_cancellation_bound_established']
    ladder=infrared_ladder.InfraredLadder(BRANCH/'emitting-thermal-background-20261008/banks/infrared96-q700')
    reader=ShapeReadout(ladder.basis,canonical=True)
    for model in ['heavy','cold']:
        for route in ['local','cubic']:
            for count in COUNTS:
                for order,cold_stage,anchor_stage in [(5,STAGE151,SOURCE154),(6,SOURCE152,SOURCE155)]:
                    cold=read_npz(stage156_parent.location(cold_stage,model,route,count)/'response.npz')
                    anchor=read_npz(stage156_parent.location(anchor_stage,model,route,count)/'response.npz')
                    pieces=[cold['photon'][-1,:,14:16],anchor['photon'][-1,:,14:16],anchor['photon'][-1,:,20:22]]
                    coherent=sum(pieces)
                    label=f'{model}-{route}-{count}-order{order}'
                    record=summary['response']['records'][label]
                    assert not record['frequency_resolved_response']
                    for match in [20,40]:
                        path=ROOT/'results/analysis'/(label+'-m'+str(match)+'-readout.npz')
                        result=read_npz(path)
                        old=read_npz(STAGE150/'results/comparison'/f'{model}-m{match}-{route}-{count}.npz')
                        assert result['potential'].shape==(700,17)
                        assert np.array_equal(result['potential'][:,:1],old['potential'][:,:1])
                        assert np.array_equal(result['amplitudes'][:,:1],old['amplitudes'][:,:1])
                        if order==6:
                            latest=read_npz(SOURCE155/'results/comparison'/f'{model}-m{match}-{route}-{count}.npz')
                            close(checks,'Independent actual saved MTS readout:'+label+':'+str(match),
                                result['potential'][:,3:5],latest['potential'][:,9:11],1e-10)
                            close(checks,'Independent actual saved energy readout:'+label+':'+str(match),
                                result['energy'][3:5],latest['energy'][9:11],1e-10)
                        close(checks,'Independent virtual response sum,no duplicated source weights:'+label+':'+str(match),
                            result['potential'][:,9:11],reader.values@coherent,1e-10)
                        for position,piece in enumerate(pieces):
                            assert np.array_equal(result['potential'][:,11+2*position:13+2*position],reader.values@piece)
                        for position,name in enumerate(['mu','y']):
                            values=result['amplitudes'][position]
                            budget=sum(abs(values[start:start+2]) for start in [11,13,15])
                            ratio=abs(values[9:11])/np.maximum(budget,1e-300)
                            close(checks,'Independent virtual '+name+' response coherence:'+label+':'+str(match),
                                ratio,record['readouts'][str(match)][name]['coherence'],1e-10)
                        inputs.append(path)
    assert summary['new_physical_events']==summary['new_virtual_coefficients']==summary['new_response_evolutions']==0
    assert not summary['temperature_curve_changed']
    scripts=sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_text(),str(path),'exec')
    assert len(scripts)==4 and not list(ROOT.rglob('__pycache__'))
    largest=max(len(files) for directory,directories,files in os.walk(ROOT))
    assert largest<1000
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    checks.append(dict(name='Four scripts compile;no bytecode;folder limits;protectedworkbench0;no newevents/evolutions',passed=True))
    consumed={path:sha for path,sha in hashes.items() if not Path(path).is_relative_to(ROOT)}
    finish(folder,dict(checks=checks,accepted_scope_verified=all(row['passed'] for row in checks),
        consumed_and_immediate_rehashed=consumed,rehashed_prior_files=len(consumed),
        scientific_checks=analysis['count'],passing_scientific_checks=analysis['count']-len(failures),
        retained_failure_names=[row['name'] for row in failures],compiled_scripts=len(scripts),
        largest_direct_file_count=largest,protected_workbench_recent_modified_file_count=0,
        independently_resummed_events=sampled_events,independently_checked_shared_nodes=sampled_reuses),
        __file__,inputs)
    print(json.dumps(dict(validation=len(checks),passed=all(row['passed'] for row in checks),
        scientific=analysis['count'],retained_failures=len(failures),prior_files=len(consumed))),flush=True)
    assert all(row['passed'] for row in checks)


if __name__=='__main__':
    main()
