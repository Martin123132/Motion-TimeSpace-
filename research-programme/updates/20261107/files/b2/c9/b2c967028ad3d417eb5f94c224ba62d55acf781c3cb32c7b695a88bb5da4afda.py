from history_source_common import *


def main():
    modest()
    folder=ROOT/'results/anchor-source'
    folder.mkdir(parents=True,exist_ok=False)
    bundle=EpochBundle()
    theta=epoch_context(bundle)[0][0]['theta']
    proof_path=ROOT/'results/history-proof/status.json'
    proof=json.loads(proof_path.read_text())
    assert proof['all_checks_passed']
    totals={key:np.zeros((98,8)) for key in ['difference','virtual','state','control']}
    checks,inputs,rows=[],[proof_path],[]
    for part in ['expensive','control']:
        keys=['difference','virtual','state'] if part=='expensive' else ['control']
        for shard in [0,1]:
            location=ROOT/'runs'/f'{part}-quarter-shard{shard}'
            packet=json.loads((location/'status.json').read_text())
            assert (location/'COMPLETE').exists() and packet['all_checks_passed']
            for path,expected in packet['input_hashes'].items():
                assert digest(path)==expected,path
            aggregate=dict(np.load(location/'source.npz'))
            independent={key:np.zeros((98,8)) for key in keys}
            count=0
            for node in physical_nodes(theta,part):
                if node['index']%2!=shard:
                    continue
                path=location/'nodes'/f"{node['index']//500:03d}"/f"{node['index']:05d}.npz"
                with np.load(path) as archive:
                    saved={key:archive[key] for key in archive.files}
                assert json.loads(str(saved['identity']))==node
                parameters,weight=parameters_and_weight(theta,node)
                assert weight>0 and abs(weight/float(saved['weight'])-1)<1e-14
                for key in keys:
                    assert saved[key].shape==(98,8) and np.isfinite(saved[key]).all()
                    independent[key]-=weight*saved[key]
                if part=='expensive':
                    loop_path=Path(str(saved['loop_path']))
                    assert loop_path.is_relative_to(ROOT/'virtual-cache')
                    loop=json.loads(loop_path.read_text())
                    assert loop['identity']==inherited.virtual_identity(parameters) and loop['scalar']==float(saved['loop_scalar'])
                inputs.append(path)
                count+=1
            assert count==packet['nodes']==len(list((location/'nodes').rglob('*.npz')))
            error=max(float(np.max(abs(independent[key]-aggregate[key]))/max(np.max(abs(aggregate[key])),1e-300)) for key in keys)
            checks.append(dict(name=f'Actual identities,weights,loops and independent aggregate:{part}-{shard}',value=error,passed=error<1e-12))
            rows.append(dict(part=part,shard=shard,nodes=count))
            for key in keys:
                totals[key]+=aggregate[key]
            inputs.extend([location/'status.json',location/'source.npz'])
    sampled_path=ROOT/'results/history-proof/sampled-leading.npz'
    sampled=dict(np.load(sampled_path))['quarter']
    totals['sampled_leading']=sampled
    totals['kinematic_remainder']=totals['control']-sampled
    totals['remainder']=sum(totals[key] for key in ['kinematic_remainder','difference','virtual','state'])
    midpoint=dict(np.load(MID/'source.npz'))
    quarter=totals['remainder'][:,:4]
    temperature_only=totals['remainder'][:,4:]
    baseline=midpoint['remainder']
    delta_temperature=temperature_only-baseline
    delta_history=quarter-temperature_only
    delta_total=quarter-baseline
    denominator=dual_norm(quarter[1:-1],midpoint['mass'])
    assert np.min(denominator)>0
    def normalized(value):
        return dual_norm(value[1:-1],midpoint['mass'])/denominator
    split_error=normalized(delta_total-delta_temperature-delta_history)
    checks.append(dict(name='Exact temperature-first history increment split',value=float(split_error.max()),passed=bool(split_error.max()<1e-12)))
    for label,source in [('quarter',quarter),('fixed_midpoint_profiles',temperature_only),('temperature_increment',delta_temperature),('history_increment',delta_history)]:
        scale=max(float(np.max(abs(source[0]))),1e-30)
        pair=float(np.max(abs(source[0]+source[-1])))
        projection=float(np.max(abs(midpoint['temperature']@source[1:-1]-source[0])))
        checks.extend([dict(name='Independent photon/gas exchange:'+label,value=pair,passed=pair<1e-6*scale),
            dict(name='Temperature projection matches independent energy:'+label,value=projection,passed=projection<1e-6*scale)])
    quarter_theta=proof['quarter_theta']
    midpoint_theta=proof['midpoint_theta']
    naive=(quarter_theta/midpoint_theta)**2*baseline
    stats=dict(temperature_ratio=quarter_theta/midpoint_theta,
        coordinate_quarter=bundle.epochs[0].coordinate,coordinate_midpoint=bundle.epochs[1].coordinate,
        quarter_source_norm=denominator.tolist(),
        midpoint_source_norm=dual_norm(baseline[1:-1],midpoint['mass']).tolist(),
        relative_total_change=normalized(delta_total).tolist(),
        relative_temperature_change=normalized(delta_temperature).tolist(),
        relative_history_change=normalized(delta_history).tolist(),
        naive_theta_squared_error=normalized(quarter-naive).tolist(),
        frozen_profile_theta_squared_error=normalized(temperature_only-naive).tolist(),
        relative_component_sum=(normalized(delta_temperature)+normalized(delta_history)).tolist())
    np.savez(folder/'source.npz',**totals,quarter=quarter,temperature_only=temperature_only,midpoint=baseline,
        delta_temperature=delta_temperature,delta_history=delta_history,delta_total=delta_total,
        mass=midpoint['mass'],temperature=midpoint['temperature'],chemical=midpoint['chemical'])
    finish(folder,dict(checks=checks,rows=rows,**stats,every_source_node_verified=True,
        pilot_resolution=True,quarter_precision_gate_closed=False,new_parent_history=False,
        complete_finite_remainder_retained=True,leading_total_addback_newly_computed=False,
        physical_change_is_not_numerical_error=True),__file__,[*inputs,sampled_path,MID/'source.npz',*bundle.inputs])
    print(json.dumps(dict(**stats,failed=[row for row in checks if not row['passed']])),flush=True)


if __name__=='__main__':
    main()
