from mixed_nodes import *


def main():
    modest()
    locations=[ROOT/'runs'/f'seed3-shard{shard}' for shard in [0,1]]
    assert all((location/'COMPLETE').exists() for location in locations)
    folder=ROOT/'results/node-audit-reverified'
    folder.mkdir(parents=True,exist_ok=False)
    checks,inputs,rows=[],[],[]
    for shard,location in enumerate(locations):
        report=json.loads((location/'status.json').read_text())
        assert report['all_checks_passed']
        theta=report['configuration']['temperature']
        nodes=[identity for identity in physical_nodes(theta,3) if identity['index']%2==shard]
        totals={key:np.zeros((98,4)) for key in ['difference','virtual','state']}
        maximum_weight=0.
        for identity in nodes:
            index=identity['index']
            path=location/'nodes'/f'{index//500:03d}'/f'{index:05d}.npz'
            with np.load(path) as packet:
                saved={key:packet[key] for key in packet.files}
            assert json.loads(str(saved['identity']))==identity
            parameters=weak.source.context(theta*identity['frequency'],identity['cosine'],np.array(identity['velocity']),theta)
            multiplicity=1 if identity['azimuth_index'] in [0,4] else 2
            assert identity['reflection_multiplicity']==multiplicity and identity['azimuth_index']<=4
            weight=identity['electron_weight']*multiplicity*identity['seed_weight']*identity['frequency']**2/math.expm1(identity['frequency'])/I3
            weight*=2*np.pi*identity['hard_weight']*parameters['born_differential_over_thomson']
            assert weight>0
            maximum_weight=max(maximum_weight,float(abs(float(saved['weight'])/weight-1)))
            for key in totals:
                assert saved[key].shape==(98,4) and np.isfinite(saved[key]).all()
                totals[key]-=weight*saved[key]
            loop_path=Path(str(saved['loop_path']))
            assert loop_path.is_relative_to(ROOT/'virtual-cache')
            loop=json.loads(loop_path.read_text())
            assert loop['identity']==virtual_identity(parameters) and loop['scalar']==float(saved['loop_scalar'])
            assert loop['finite'] and np.isfinite(loop['scalar'])
            inputs.extend([path,loop_path])
        aggregate=dict(np.load(location/'source.npz'))
        error=max(float(np.max(abs(totals[key]-aggregate[key])))/max(float(np.max(abs(aggregate[key]))),1e-300) for key in totals)
        assert len(nodes)==report['nodes']==len(list((location/'nodes').rglob('*.npz')))
        checks.extend([dict(name='Complete coarse shard identities and actual-node loops:'+str(shard),passed=True),
            dict(name='Positive original weights and inherited reflection multiplicity:'+str(shard),value=maximum_weight,passed=maximum_weight<1e-13),
            dict(name='Independent aggregate reconstruction:'+str(shard),value=error,passed=error<1e-12)])
        rows.append(dict(shard=shard,nodes=len(nodes)))
        inputs.extend([location/'status.json',location/'source.npz'])
    parent_seal=json.loads((PARENT/'results/stage-integrity.json').read_text())
    for relative in ['results/combined-source/source.npz','results/radial-budget/responses.npz']:
        assert digest(PARENT/relative)==parent_seal['file_hashes'][relative]
        inputs.append(PARENT/relative)
    checks.append(dict(name='Saved fine source and inherited ledger remain unchanged',passed=True))
    loops=len(list((ROOT/'virtual-cache').rglob('*.json')))
    assert loops==4725
    checks.append(dict(name='All4725 missing-corner points have actual owned loop records',passed=True))
    finish(folder,dict(checks=checks,rows=rows,every_source_node_verified=True,private_loop_files=loops,
        fine_source_recomputed=False,initial_audit_replayed=True),__file__,[*inputs,ROOT/'mixed_nodes.py',ROOT/'results/node-audit/status.json'])
    print(json.dumps(dict(checks=checks,rows=rows)),flush=True)


if __name__=='__main__':
    main()
