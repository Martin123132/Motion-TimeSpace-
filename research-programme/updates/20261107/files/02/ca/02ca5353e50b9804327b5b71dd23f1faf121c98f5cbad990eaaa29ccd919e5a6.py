from late_frequency_common import *


def ratio(numerator,denominator):
    return float(numerator/denominator) if denominator!=0 else None


def main():
    modest()
    folder=ROOT/'results/refinement-sources'
    folder.mkdir(parents=True,exist_ok=False)
    proof_path=ROOT/'results/refinement-preflight/status.json'
    proof=json.loads(proof_path.read_text())
    assert proof['all_checks_passed']
    for path,expected in proof['input_hashes'].items():
        assert digest(path)==expected,path
    plan_path=proof_path.parent/'reuse-plan.json'
    reuse=json.loads(plan_path.read_text())
    baseline_path=ANCHOR/'results/holdout-sources/source.npz'
    previous_path=PARENT/'results/frequency-sources/source.npz'
    baseline,previous=[dict(np.load(path)) for path in [baseline_path,previous_path]]
    assert digest(baseline_path)==proof['baseline_sha256']
    assert digest(previous_path)==proof['previous_comparison_sha256']
    mass,temperature,chemical=[baseline[key] for key in ['mass','temperature','chemical']]
    bundle=EpochBundle(.4375)
    theta=epoch_context(bundle)[0][0]['theta']
    location=ROOT/'runs/expensive-late'
    packet=json.loads((location/'status.json').read_text())
    assert (location/'COMPLETE').exists() and packet['all_checks_passed']
    for path,expected in packet['input_hashes'].items():
        assert digest(path)==expected,path
    keys=['difference','virtual','state']
    aggregate=dict(np.load(location/'source.npz'))
    independent={key:np.zeros((98,4)) for key in keys}
    inputs=[proof_path,plan_path,baseline_path,previous_path,location/'status.json',location/'source.npz',*bundle.inputs]
    count,reused_count=0,0
    for node in physical_nodes(theta,'expensive'):
        path=location/'nodes'/f"{node['index']//500:03d}"/f"{node['index']:05d}.npz"
        with np.load(path) as archive:
            saved={key:archive[key] for key in archive.files}
        assert json.loads(str(saved['identity']))==node
        parameters,weight=parameters_and_weight(theta,node)
        assert weight>0 and abs(weight/float(saved['weight'])-1)<1e-14
        record=reuse.get(str(node['index']))
        loop_path=Path(str(saved['loop_path']))
        if record is not None:
            assert str(saved['origin'])=='reused_seed3_event'
            origin=Path(str(saved['origin_path']))
            assert origin==Path(record['path']) and digest(origin)==record['sha256']==str(saved['origin_sha256'])
            with np.load(origin) as old:
                assert physical_key(json.loads(str(old['identity'])))==physical_key(node)
                assert all(np.array_equal(saved[key],old[key]) for key in keys)
            assert loop_path==Path(record['loop_path']) and digest(loop_path)==record['loop_sha256']
            inputs.append(origin)
            reused_count+=1
        else:
            assert str(saved['origin'])=='new_seed5_event' and loop_path.is_relative_to(ROOT/'virtual-cache')
        loop=json.loads(loop_path.read_text())
        assert loop['identity']==inherited.virtual_identity(parameters)
        assert loop['scalar']==float(saved['loop_scalar']) and loop['finite']
        for key in keys:
            assert saved[key].shape==(98,4) and np.isfinite(saved[key]).all()
            independent[key]-=weight*saved[key]
        inputs.extend([path,loop_path])
        count+=1
    assert count==1260==packet['nodes']==len(list((location/'nodes').rglob('*.npz')))
    assert reused_count==len(reuse)==packet['reused_physical_nodes']
    error=max(float(np.max(abs(independent[key]-aggregate[key]))/max(np.max(abs(aggregate[key])),1e-300)) for key in keys)
    checks=[dict(name='All weighted nodes,exact physical reuse,new weights and owned loops verified',value=error,passed=error<1e-12)]
    fine4=baseline['late_actual']
    candidate5=baseline['late_kinematic_remainder']+sum(aggregate[key] for key in keys)
    old_deltas=[previous['late_delta_'+key] for key in keys]
    new_deltas=[aggregate[key]-baseline['late_'+key] for key in keys]
    denominator=dual_norm(fine4[1:-1],mass)
    error=float((dual_norm((candidate5-fine4-sum(new_deltas))[1:-1],mass)/denominator).max())
    checks.append(dict(name='R5 minus R4 equals three new component differences',value=error,passed=error<1e-12))
    old_identity=float((dual_norm((fine4-previous['late_coarse']-sum(old_deltas))[1:-1],mass)/denominator).max())
    checks.append(dict(name='Saved R4 minus R3 and components unchanged',value=old_identity,passed=old_identity<1e-12))
    for label,source in [('fine4',fine4),('candidate5',candidate5),*zip(keys,new_deltas)]:
        scale=max(float(np.max(abs(source[0]))),1e-30)
        pairing=float(np.max(abs(source[0]+source[-1])))
        projection=float(np.max(abs(temperature@source[1:-1]-source[0])))
        checks.extend([dict(name='Independent photon/gas pairing:'+label,value=pairing,passed=pairing<1e-6*scale),
            dict(name='Spectral projection equals independent energy:'+label,value=projection,passed=projection<1e-6*scale)])
    old_norms=np.asarray([dual_norm(delta[1:-1],mass) for delta in old_deltas])
    new_norms=np.asarray([dual_norm(delta[1:-1],mass) for delta in new_deltas])
    old_sum,new_sum=old_norms.sum(axis=0)/denominator,new_norms.sum(axis=0)/denominator
    old_coherent=dual_norm(sum(old_deltas)[1:-1],mass)/denominator
    new_coherent=dual_norm(sum(new_deltas)[1:-1],mass)/denominator
    triangle=float(max((old_coherent-old_sum).max(),(new_coherent-new_sum).max()))
    checks.append(dict(name='Both component-sum budgets dominate coherent source changes',value=triangle,passed=triangle<1e-12))
    structural_passed=all(bool(row['passed']) for row in checks)
    metrics=[]
    for column,label in enumerate(['heavy-join1','heavy-join2','cold-join1','cold-join2']):
        row=dict(profile=label,central4_norm=float(denominator[column]),old43_component_sum=float(old_sum[column]),
            new54_component_sum=float(new_sum[column]),contraction=ratio(new_sum[column],old_sum[column]),
            old43_coherent=float(old_coherent[column]),new54_coherent=float(new_coherent[column]),
            components={},moments={})
        for offset,key in enumerate(keys):
            row['components'][key]=dict(old43=float(old_norms[offset,column]/denominator[column]),
                new54=float(new_norms[offset,column]/denominator[column]),
                contraction=ratio(new_norms[offset,column],old_norms[offset,column]))
        for name,selector in [('photon_energy',lambda value:value[0]),('gas_energy',lambda value:value[-1]),
                ('photon_number',lambda value:chemical@value[1:-1])]:
            central=float(selector(fine4)[column])
            old_values=np.array([selector(delta)[column] for delta in old_deltas])
            new_values=np.array([selector(delta)[column] for delta in new_deltas])
            row['moments'][name]=dict(central4=central,old43_components=old_values.tolist(),new54_components=new_values.tolist(),
                old43_component_sum=ratio(abs(old_values).sum(),abs(central)),
                new54_component_sum=ratio(abs(new_values).sum(),abs(central)),
                old43_coherent=ratio(abs(old_values.sum()),abs(central)),
                new54_coherent=ratio(abs(new_values.sum()),abs(central)),
                contraction=ratio(abs(new_values).sum(),abs(old_values).sum()),
                old43_absolute_sum=float(abs(old_values).sum()),new54_absolute_sum=float(abs(new_values).sum()),
                zero_central_denominator=central==0)
        checks.extend([
            dict(name='REFINEMENT_DIAGNOSTIC: source sum54 within1percent:'+label,value=row['new54_component_sum'],passed=row['new54_component_sum']<=.01),
            dict(name='REFINEMENT_DIAGNOSTIC: source component sum contracts:'+label,value=row['contraction'],passed=row['contraction'] is not None and row['contraction']<1)])
        for key,values in row['components'].items():
            value=values['contraction']
            checks.append(dict(name='REFINEMENT_DIAGNOSTIC: individual source component contracts:'+label+':'+key,
                value=value,passed=value<1 if value is not None else values['new54']==0))
        metrics.append(row)
    arrays={key:baseline[key] for key in ['anchors','early_defect','late_defect','mass','temperature','chemical']}
    arrays.update(late_fine4=fine4,late_candidate5=candidate5,late_old_delta=sum(old_deltas),late_new_delta=sum(new_deltas))
    arrays.update({'late_old_delta_'+key:value for key,value in zip(keys,old_deltas)})
    arrays.update({'late_new_delta_'+key:value for key,value in zip(keys,new_deltas)})
    arrays.update({'late_seed5_'+key:aggregate[key] for key in keys})
    np.savez(folder/'source.npz',**arrays)
    finish(folder,dict(checks=checks,profile_metrics=metrics,numerical_integrity_all_passed=structural_passed,
        every_source_node_verified=True,weighted_nodes=count,reused_physical_nodes=reused_count,new_physical_nodes=count-reused_count,
        central_seed4_unchanged=True,controls_reused_without_recomputation=True,baseline_sha256=digest(baseline_path),
        source_frequency_continuum_error_bounded=False,new_epoch_precision_gate_closed=False,new_parent_history=False),
        __file__,inputs)
    print(json.dumps(dict(profile_metrics=metrics,failed=[row['name'] for row in checks if not row['passed']])),flush=True)
    if not structural_passed:
        raise SystemExit(1)


if __name__=='__main__':
    main()
