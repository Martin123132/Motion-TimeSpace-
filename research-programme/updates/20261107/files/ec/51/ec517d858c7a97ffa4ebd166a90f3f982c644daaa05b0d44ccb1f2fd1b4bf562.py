from polar_nodes import *
from compare_source_vectors import dual_norm


def main():
    modest()
    locations = [ROOT / 'runs' / f'{part}-p3-shard{shard}' for part in ['expensive','control'] for shard in [0,1]]
    assert all((location/'COMPLETE').exists() and (location/'status.json').exists() for location in locations), 'Wait for all four completed packets.'
    folder = ROOT / 'results/node-audit'
    folder.mkdir(parents=True,exist_ok=False)
    rows, inputs, checks = [], [], []
    for location in locations:
        report = json.loads((location/'status.json').read_text())
        assert report['all_checks_passed']
        config = report['configuration']
        part, shard, theta = config['part'], config['shard'], config['temperature']
        keys = ['difference','virtual','state'] if part == 'expensive' else ['control']
        totals = {key:np.zeros((98,4)) for key in keys}
        nodes = [identity for identity in physical_nodes(theta,part) if identity['index'] % 2 == shard]
        maximum_weight, multiplicities = 0., set()
        for identity in nodes:
            index = identity['index']
            path = location / 'nodes' / f'{index//500:03d}' / f'{index:05d}.npz'
            saved = dict(np.load(path))
            assert json.loads(str(saved['identity'])) == identity
            parameters = weak.source.context(theta*identity['frequency'],identity['cosine'],np.array(identity['velocity']),theta)
            multiplicity = 1 if identity['azimuth_index'] in [0,4] else 2
            assert identity['reflection_multiplicity'] == multiplicity and identity['azimuth_index'] <= 4
            weight = identity['electron_weight'] * multiplicity * identity['seed_weight'] * identity['frequency']**2 / math.expm1(identity['frequency']) / I3
            weight *= 2*np.pi*identity['hard_weight']*parameters['born_differential_over_thomson']
            assert weight > 0
            maximum_weight=max(maximum_weight,float(abs(float(saved['weight'])/weight-1)))
            multiplicities.add(multiplicity)
            for key in keys:
                assert saved[key].shape == (98,4) and np.isfinite(saved[key]).all()
                totals[key] -= weight*saved[key]
            if part == 'expensive':
                loop_path=Path(str(saved['loop_path']))
                loop=json.loads(loop_path.read_text())
                assert loop_path.is_relative_to(ROOT/'virtual-cache')
                assert loop['identity'] == virtual_identity(parameters)
                assert loop['finite'] and np.isfinite(loop['scalar']) and loop['scalar'] == float(saved['loop_scalar'])
                inputs.append(loop_path)
            inputs.append(path)
        source=dict(np.load(location/'source.npz'))
        error=max(float(np.max(abs(totals[key]-source[key])))/max(float(np.max(abs(source[key]))),1e-300) for key in keys)
        assert len(nodes) == report['nodes'] == len(list((location/'nodes').rglob('*.npz')))
        checks.extend([dict(name='Actual identities/owned loops and complete shard:' + location.name,passed=True),
            dict(name='Positive original measure with proven reflection multiplicity:' + location.name,value=maximum_weight,passed=maximum_weight < 1e-13),
            dict(name='Node aggregate reconstructs original shard:' + location.name,value=error,passed=error < 1e-12)])
        rows.append(dict(part=part,shard=shard,nodes=len(nodes),multiplicities=sorted(multiplicities)))
        inputs.extend([location/'status.json',location/'source.npz'])
    parent_seal=json.loads((PARENT/'results/stage-integrity.json').read_text())
    parent_combined=dict(np.load(PARENT/'results/combined-source/source.npz'))
    denominator=dual_norm(parent_combined['remainder'][1:-1],parent_combined['mass'])
    replay={}
    for part in ['expensive','control']:
        parent_folder=PARENT/'runs'/f'{part}-h5-az8'
        keys=['difference','virtual','state'] if part=='expensive' else ['control']
        folded={key:np.zeros((98,4)) for key in keys}
        nodes=list(physical_nodes(theta,part,polar=2,folded=False))
        for identity in nodes:
            if identity['azimuth_index']>4:
                continue
            index=identity['index']
            path=parent_folder/'nodes'/f'{index//500:03d}'/f'{index:05d}.npz'
            assert digest(path)==parent_seal['file_hashes'][path.relative_to(PARENT).as_posix()]
            saved=dict(np.load(path))
            original=json.loads(str(saved['identity']))
            assert node_key(original)==node_key(identity)
            multiplicity=1 if identity['azimuth_index'] in [0,4] else 2
            for key in keys:
                folded[key]-=multiplicity*float(saved['weight'])*saved[key]
            inputs.append(path)
        original_source=dict(np.load(parent_folder/'source.npz'))
        for key in keys:
            difference=folded[key]-original_source[key]
            budget=dual_norm(difference[1:-1],parent_combined['mass'])/denominator
            replay[key]=budget.tolist()
            checks.append(dict(name='Folded replay of previously fully sampled parent:'+key,
                value=float(budget.max()),passed=bool(budget.max()<1e-6)))
        inputs.append(parent_folder/'source.npz')
    finish(folder,dict(checks=checks,rows=rows,every_source_node_verified=True,
        parent_fold_replay_relative_to_remainder=replay,
        parent_fold_replay_is_not_global_polar3_roundoff_bound=True,
        private_loop_files=len(list((ROOT/'virtual-cache').rglob('*.json')))),
        __file__,[*inputs,ROOT/'polar_nodes.py',PARENT/'results/combined-source/source.npz'])
    print(json.dumps(dict(checks=checks,rows=rows,replay=replay)),flush=True)


if __name__=='__main__':
    main()
