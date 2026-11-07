from project_direction import physical_nodes
from direction_common import *


def main():
    modest()
    folder = ROOT / 'results/node-audit'
    folder.mkdir(parents=True, exist_ok=False)
    owner_seals = {owner:json.loads((owner / 'results/stage-integrity.json').read_text())
        for owner in [PARENT, OUTER, BRANCH / 'population-matched-source-20261008']}
    checks, inputs, rows = [], [], []
    for part in ['expensive', 'control']:
        location = ROOT / 'runs' / f'{part}-h5'
        report = json.loads((location / 'status.json').read_text())
        assert report['all_checks_passed']
        theta = report['configuration']['temperature']
        keys = ['difference', 'virtual', 'state'] if part == 'expensive' else ['control']
        totals = {key:np.zeros((98, 4)) for key in keys}
        nodes = list(physical_nodes(theta, part, 5))
        maximum_weight, reused = 0., 0
        for index, identity in enumerate(nodes):
            path = location / 'nodes' / f'{index // 500:03d}' / f'{index:05d}.npz'
            saved = dict(np.load(path))
            assert json.loads(str(saved['identity'])) == identity
            parameters = weak.source.context(theta * identity['frequency'], identity['cosine'], np.array(identity['velocity']), theta)
            weight = identity['electron_weight'] * identity['seed_weight'] * identity['frequency']**2 / math.expm1(identity['frequency']) / I3
            weight *= 2 * np.pi * identity['hard_weight'] * parameters['born_differential_over_thomson']
            assert weight > 0
            maximum_weight = max(maximum_weight, float(abs(float(saved['weight']) / weight - 1)))
            for key in keys:
                assert saved[key].shape == (98, 4) and np.isfinite(saved[key]).all()
                totals[key] -= weight * saved[key]
            if str(saved['reuse_path']):
                original = Path(str(saved['reuse_path']))
                owner = next(owner for owner in owner_seals if original.is_relative_to(owner))
                assert digest(original) == owner_seals[owner]['file_hashes'][original.relative_to(owner).as_posix()]
                old = dict(np.load(original))
                assert node_key(json.loads(str(old['identity']))) == node_key(identity)
                assert all(np.array_equal(old[key], saved[key]) for key in keys)
                inputs.append(original)
                reused += 1
            if part == 'expensive':
                loop_path = Path(str(saved['loop_path']))
                loop = json.loads(loop_path.read_text())
                assert loop['identity'] == virtual_identity(parameters)
                assert loop['finite'] and np.isfinite(loop['scalar']) and loop['scalar'] == float(saved['loop_scalar'])
                if not loop_path.is_relative_to(ROOT):
                    owner = next(owner for owner in owner_seals if loop_path.is_relative_to(owner))
                    assert digest(loop_path) == owner_seals[owner]['file_hashes'][loop_path.relative_to(owner).as_posix()]
                inputs.append(loop_path)
            inputs.append(path)
        aggregate = dict(np.load(location / 'source.npz'))
        error = max(float(np.max(abs(totals[key] - aggregate[key]))) / max(float(np.max(abs(aggregate[key]))), 1e-300) for key in keys)
        assert len(nodes) == report['nodes'] == len(list((location / 'nodes').rglob('*.npz')))
        checks.extend([
            dict(name='Every physical node/reused hash/loop identity checked: ' + part, passed=True),
            dict(name='Original positive weights reproduced: ' + part, value=maximum_weight, passed=maximum_weight < 1e-13),
            dict(name='Complete components reassembled from actual weighted nodes: ' + part, value=error, passed=error < 1e-12),
        ])
        rows.append(dict(part=part, nodes=len(nodes), reused=reused))
        inputs.extend([location / 'source.npz', location / 'status.json'])
    finish(folder, dict(checks=checks, rows=rows, every_source_node_verified=True,
        private_loop_files=len(list((ROOT / 'virtual-cache').rglob('*.json')))), __file__, inputs)
    print(json.dumps(dict(checks=checks, rows=rows)), flush=True)


if __name__ == '__main__':
    main()
