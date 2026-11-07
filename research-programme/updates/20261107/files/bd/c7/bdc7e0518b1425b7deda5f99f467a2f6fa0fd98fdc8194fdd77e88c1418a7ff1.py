from history_frequency_common import *


def budgets(fine,deltas,mass,chemical):
    denominator=dual_norm(fine[1:-1],mass)
    assert np.min(denominator)>0
    components=np.asarray([dual_norm(delta[1:-1],mass) for delta in deltas])
    coherent=dual_norm(sum(deltas)[1:-1],mass)/denominator
    component_sum=components.sum(axis=0)/denominator
    rows=[]
    for column,label in enumerate(['heavy-join1','heavy-join2','cold-join1','cold-join2']):
        row=dict(profile=label,source_norm=float(denominator[column]),
            coherent_relative=float(coherent[column]),component_sum_relative=float(component_sum[column]),
            component_relative=(components[:,column]/denominator[column]).tolist(),moments={})
        for name,selector in [('photon_energy',lambda value:value[0]),
                ('gas_energy',lambda value:value[-1]),
                ('photon_number',lambda value:chemical@value[1:-1])]:
            central=float(selector(fine)[column])
            individual=np.array([selector(delta)[column] for delta in deltas])
            row['moments'][name]=dict(central=central,components=individual.tolist(),
                coherent_absolute=float(abs(individual.sum())),component_sum_absolute=float(abs(individual).sum()),
                coherent_relative=float(abs(individual.sum())/abs(central)) if central!=0 else None,
                component_sum_relative=float(abs(individual).sum()/abs(central)) if central!=0 else None,
                zero_denominator=central==0)
        rows.append(row)
    return rows


def main():
    modest()
    folder=ROOT/'results/frequency-sources'
    folder.mkdir(parents=True,exist_ok=False)
    proof_path=ROOT/'results/frequency-preflight/status.json'
    proof=json.loads(proof_path.read_text())
    assert proof['all_checks_passed']
    for path,expected in proof['input_hashes'].items():
        assert digest(path)==expected,path
    baseline_path=PARENT/'results/holdout-sources/source.npz'
    baseline=dict(np.load(baseline_path))
    assert digest(baseline_path)=='695037a1f7052d32d242457ab1b31b2a69becc544637c0ed77e0f2238eec8c3c'
    mass,temperature,chemical=[baseline[key] for key in ['mass','temperature','chemical']]
    checks,inputs,rows,arrays,metrics=[],[proof_path,baseline_path],[],{},{}
    keys=['difference','virtual','state']
    for epoch,fraction in FRACTIONS.items():
        bundle=EpochBundle(fraction)
        theta=epoch_context(bundle)[0][0]['theta']
        inputs+=bundle.inputs
        location=ROOT/'runs'/f'expensive-{epoch}'
        packet=json.loads((location/'status.json').read_text())
        assert (location/'COMPLETE').exists() and packet['all_checks_passed']
        for path,expected in packet['input_hashes'].items():
            assert digest(path)==expected,path
        aggregate=dict(np.load(location/'source.npz'))
        independent={key:np.zeros((98,4)) for key in keys}
        count=0
        for node in physical_nodes(theta,'expensive'):
            path=location/'nodes'/f"{node['index']//500:03d}"/f"{node['index']:05d}.npz"
            with np.load(path) as archive:
                saved={key:archive[key] for key in archive.files}
            assert json.loads(str(saved['identity']))==node
            parameters,weight=parameters_and_weight(theta,node)
            assert weight>0 and abs(weight/float(saved['weight'])-1)<1e-14
            for key in keys:
                assert saved[key].shape==(98,4) and np.isfinite(saved[key]).all()
                independent[key]-=weight*saved[key]
            loop_path=Path(str(saved['loop_path']))
            assert loop_path.is_relative_to(ROOT/'virtual-cache')
            loop=json.loads(loop_path.read_text())
            assert loop['identity']==inherited.virtual_identity(parameters)
            assert loop['scalar']==float(saved['loop_scalar']) and loop['finite']
            inputs.extend([path,loop_path])
            count+=1
        assert count==756==packet['nodes']==len(list((location/'nodes').rglob('*.npz')))
        error=max(float(np.max(abs(independent[key]-aggregate[key]))/max(np.max(abs(aggregate[key])),1e-300)) for key in keys)
        checks.append(dict(name='Actual positive nodes,owned loops and independent source reconstruction:'+epoch,value=error,passed=error<1e-12))
        rows.append(dict(epoch=epoch,theta=theta,new_seed3_nodes=count,reused_seed4_nodes=1008,reused_control_nodes=4608))
        inputs.extend([location/'status.json',location/'source.npz'])
        fine=baseline[epoch+'_actual']
        coarse=baseline[epoch+'_kinematic_remainder']+sum(aggregate[key] for key in keys)
        deltas=[baseline[epoch+'_'+key]-aggregate[key] for key in keys]
        error=float((dual_norm((fine-coarse-sum(deltas))[1:-1],mass)/dual_norm(fine[1:-1],mass)).max())
        checks.append(dict(name='R4 minus R3 equals all three component differences:'+epoch,value=error,passed=error<1e-12))
        for label,source in [('fine',fine),('coarse',coarse),*zip(keys,deltas)]:
            scale=max(float(np.max(abs(source[0]))),1e-30)
            pairing=float(np.max(abs(source[0]+source[-1])))
            projection=float(np.max(abs(temperature@source[1:-1]-source[0])))
            checks.extend([dict(name=f'Independent photon/gas pairing:{epoch}-{label}',value=pairing,passed=pairing<1e-6*scale),
                dict(name=f'Spectral projection equals independent energy:{epoch}-{label}',value=projection,passed=projection<1e-6*scale)])
        metrics[epoch]=budgets(fine,deltas,mass,chemical)
        triangle=max(row['coherent_relative']-row['component_sum_relative'] for row in metrics[epoch])
        checks.append(dict(name='Source triangle inequality without cancellation credit:'+epoch,value=triangle,passed=triangle<1e-12))
        arrays.update({epoch+'_fine':fine,epoch+'_coarse':coarse,epoch+'_delta_total':sum(deltas),
            epoch+'_defect':baseline[epoch+'_defect']})
        arrays.update({epoch+'_delta_'+key:value for key,value in zip(keys,deltas)})
        arrays.update({epoch+'_coarse_'+key:aggregate[key] for key in keys})
    structural_passed=all(bool(row['passed']) for row in checks)
    for epoch,measurements in metrics.items():
        for row in measurements:
            checks.append(dict(name=f"FREQUENCY_DIFFERENCE: source component-sum within1percent:{epoch}:{row['profile']}",
                value=row['component_sum_relative'],passed=row['component_sum_relative']<=.01))
    np.savez(folder/'source.npz',**arrays,anchors=baseline['anchors'],mass=mass,temperature=temperature,chemical=chemical)
    finish(folder,dict(checks=checks,rows=rows,profile_metrics=metrics,numerical_integrity_all_passed=structural_passed,
        every_source_node_verified=True,central_seed4_unchanged=True,controls_reused_without_recomputation=True,
        baseline_sha256=digest(baseline_path),source_frequency_continuum_error_bounded=False,
        new_epoch_precision_gate_closed=False,new_parent_history=False,complete_finite_remainder_retained=True),__file__,inputs)
    print(json.dumps(dict(profile_metrics=metrics,failed=[row['name'] for row in checks if not row['passed']])),flush=True)
    if not structural_passed:
        raise SystemExit(1)


if __name__=='__main__':
    main()
