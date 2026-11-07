from history_source_common import *


def main():
    modest()
    folder=ROOT/'results/history-proof'
    folder.mkdir(parents=True,exist_ok=False)
    ancestors=sealed_ancestors()
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    for name,expected in parent['file_hashes'].items():
        assert digest(PARENT/name)==expected,name
    bundle=EpochBundle()
    contexts=epoch_context(bundle)
    quarter,midpoint=contexts[0][0]['theta'],contexts[1][0]['theta']
    source=dict(np.load(MID/'source.npz'))
    inputs=[MID/'source.npz',MID/'status.json',OUTER/'source.npz',*bundle.inputs,ROOT/'DERIVATION.md']
    for path in inputs[:-1]:
        verify_reference(path,ancestors)
    for models in contexts:
        for model in models:
            for path in model['inputs']:
                inputs.append(Path(path))
    assert np.array_equal(bundle.basis.mass,source['mass'])
    assert np.array_equal(bundle.basis.temperature,source['temperature'])
    checks=[dict(name='Stage101 payloads and matched-grid source/history inputs unchanged',passed=True),
        dict(name='Temperature history follows theta_prime=-theta',value=quarter/midpoint,
            passed=abs(quarter/midpoint-math.exp(bundle.epochs[1].coordinate-bundle.epochs[0].coordinate))<1e-14),
        dict(name='Photon energy row equals mass times temperature direction',
            passed=bool(np.allclose(bundle.basis.energy,bundle.basis.mass@bundle.basis.temperature,rtol=1e-12,atol=1e-14)))]
    for part,location,count in [('expensive',OUTER,1008),('control',MID,4608)]:
        keys=['difference','virtual','state'] if part=='expensive' else ['control']
        totals={key:np.zeros((98,4)) for key in keys}
        index_map={}
        for path in (location/'nodes').rglob('*.npz'):
            with np.load(path) as archive:
                identity=json.loads(str(archive['identity']))
            index_map[node_key(identity)]=path
        identities=list(physical_nodes(midpoint,part))
        assert len(identities)==count
        for identity in identities:
            path=index_map[node_key(identity)]
            with np.load(path) as saved:
                parameters,weight=parameters_and_weight(midpoint,identity)
                assert abs(weight/(float(saved['weight'])*identity['reflection_multiplicity'])-1)<1e-14
                for key in keys:
                    totals[key]-=weight*saved[key]
            verify_reference(path,ancestors)
            inputs.append(path)
        denominator=dual_norm(source['remainder'][1:-1],source['mass'])
        error=max(float(np.max(dual_norm((totals[key]-source[key])[1:-1],source['mass'])/denominator)) for key in keys)
        checks.append(dict(name='Folded full midpoint source replay:'+part,value=error,passed=error<1e-9))
    sampled=sampled_leading(bundle,midpoint)
    sampled_error=float(np.max(abs(sampled[:,4:]-source['sampled_leading']))/max(np.max(abs(source['sampled_leading'])),1e-300))
    scaled=sampled_leading(bundle,quarter)
    leading_error=float(np.max(abs(scaled-(quarter/midpoint)**2*sampled))/max(np.max(abs(scaled)),1e-300))
    checks.extend([dict(name='Saved midpoint sampled-leading source replay',value=sampled_error,passed=sampled_error<1e-12),
        dict(name='Fixed-profile leading control has exact theta_squared scaling',value=leading_error,passed=leading_error<1e-12)])
    np.savez(folder/'sampled-leading.npz',quarter=scaled,midpoint=sampled)
    identities=list(physical_nodes(quarter,'expensive'))
    selected=min((node for node in identities if node['azimuth_index']==1),key=lambda node:abs(math.log(node['frequency']))+abs(node['cosine']))
    parameters,weight=parameters_and_weight(quarter,selected)
    packed=FastSplit(bundle,'difference')
    mixed=FastSplit(LinearEpochCombination(bundle,1.3,-.4),'difference')
    values,null,scalar,path=expensive_components(parameters,packed)
    combined,combined_null,combined_scalar,combined_path=expensive_components(parameters,mixed)
    for key in values:
        expected=1.3*values[key][:,:4]-.4*values[key][:,4:]
        error=float(np.max(abs(combined[key]-expected))/max(np.max(abs(expected)),1e-300))
        checks.append(dict(name='Actual event functional linear in profile and gas:'+key,value=error,passed=error<1e-7))
    reflected=dict(selected,velocity=[selected['velocity'][0],-selected['velocity'][1],selected['velocity'][2]])
    mirrored,unused=parameters_and_weight(quarter,reflected)
    reflected_values,reflected_null,reflected_scalar,reflected_path=expensive_components(mirrored,packed)
    for key in values:
        error=float(np.max(abs(values[key]-reflected_values[key]))/max(np.max(abs(values[key])),1e-300))
        checks.append(dict(name='Quarter-epoch scalar reflection:'+key,value=error,passed=error<1e-7))
    checks.append(dict(name='Quarter event energy pairing',value=max(null,combined_null,reflected_null),passed=max(null,combined_null,reflected_null)<1e-10))
    np.savez(folder/'event-check.npz',**values,**{'mixed_'+key:value for key,value in combined.items()})
    finish(folder,dict(checks=checks,quarter_theta=quarter,midpoint_theta=midpoint,epoch_contexts=contexts,
        prior_chain_entries=sum(len(packet['file_hashes']) for packet in ancestors.values()),
        full_ancestor_payload_rehashed=False,epoch_fraction=FRACTION,full_grid_gate_inherited_at_quarter=False,
        production_node_counts=dict(expensive=1008,control=4608)),__file__,[*inputs,path,reflected_path])
    print(json.dumps(dict(checks=len(checks),failed=[row for row in checks if not row['passed']],quarter_theta=quarter,midpoint_theta=midpoint)),flush=True)
    if not all(row['passed'] for row in checks):
        raise SystemExit(1)


if __name__=='__main__':
    main()
