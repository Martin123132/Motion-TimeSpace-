from sharded_loop_cache import *
from compare_source_vectors import dual_norm


def main():
    modest()
    folder = ROOT / 'results/node-audit'
    folder.mkdir(parents=True, exist_ok=False)
    cache = ShardedLoopCache()
    checks, inputs, rows = [], [], []
    for seed_order in [2, 3, 4]:
        location = ROOT / 'runs' / f's{seed_order}-h3-g2-2-4'
        report = json.loads((location / 'status.json').read_text())
        assert report['all_checks_passed']
        theta = report['configuration']['temperature']
        identities = list(population_nodes(theta, seed_order))
        paths = sorted((location / 'nodes').rglob('*.npz'))
        assert len(paths) == len(identities) == report['nodes']
        maximum_weight = 0.
        reconstructed = {key: np.zeros((98, 4)) for key in ['difference', 'control', 'virtual', 'state']}
        for path, identity in zip(paths, identities):
            saved = dict(np.load(path))
            assert json.loads(str(saved['identity'])) == identity
            loop_path = Path(str(saved['loop_path']))
            loop = json.loads(loop_path.read_text())
            parameters = weak.source.context(theta * identity['frequency'], identity['cosine'], np.asarray(identity['velocity']), theta)
            expected = dict(lab_energy=parameters['lab_energy'], cosine=parameters['lab_cosine'],
                velocity=parameters['velocity'].tolist(), temperature=theta, order=2,
                script_sha256=digest(weak.source.__file__),
                stage88_sha256=digest(BRANCH / 'matched-weak-redistribution-20261008/results/stage-integrity.json'))
            assert loop['identity'] == expected and loop['finite'] and np.isfinite(loop['scalar']) and loop['scalar'] == float(saved['loop_scalar'])
            if loop_path.is_relative_to(cache.parent):
                assert digest(loop_path) == cache.seal['file_hashes'][loop_path.relative_to(cache.parent).as_posix()]
            else:
                assert loop_path.is_relative_to(ROOT / 'virtual-cache')
            weight = identity['electron_weight'] * identity['seed_weight'] * identity['frequency']**2 / math.expm1(identity['frequency']) / I3
            weight *= 2 * np.pi * identity['hard_weight'] * parameters['born_differential_over_thomson']
            maximum_weight = max(maximum_weight, abs(float(saved['weight']) / weight - 1))
            assert weight > 0
            for key in reconstructed:
                assert saved[key].shape == (98, 4) and np.isfinite(saved[key]).all()
                reconstructed[key] -= weight * saved[key]
            inputs.extend([path, loop_path])
        aggregate = dict(np.load(location / 'source.npz'))
        reconstruction_error = max(float(np.max(abs(reconstructed[key] - aggregate[key]))) /
            max(float(np.max(abs(aggregate[key]))), 1e-300) for key in reconstructed)
        assert np.array_equal(aggregate['kinematic_remainder'], aggregate['control'] - aggregate['sampled_leading'])
        assert np.array_equal(aggregate['remainder'], aggregate['difference'] + aggregate['virtual'] +
            aggregate['state'] + aggregate['kinematic_remainder'])
        assert np.array_equal(aggregate['total'], aggregate['accurate_leading'] + aggregate['remainder'])
        electrons = {tuple(item['velocity']): item['electron_weight'] for item in identities}
        seeds = {item['frequency']: item['seed_weight'] for item in identities}
        hard = {item['cosine']: item['hard_weight'] for item in identities}
        checks.extend([
            dict(name=f'Every exact source/loop identity and scalar checked independently: seed{seed_order}', passed=True, nodes=len(paths)),
            dict(name=f'Original positive physical measure reproduced: seed{seed_order}', value=maximum_weight, passed=maximum_weight < 1e-13),
            dict(name=f'All source components independently reassembled from weighted nodes: seed{seed_order}',
                value=reconstruction_error, passed=reconstruction_error < 1e-12),
            dict(name=f'Electron, seed and hard quadrature normalizations: seed{seed_order}',
                passed=abs(sum(electrons.values()) - 1) < 1e-13 and abs(sum(seeds.values()) - (24 - 1e-5)) < 1e-12 and abs(sum(hard.values()) - 2) < 1e-13),
        ])
        rows.append(dict(seed_order=seed_order, nodes=len(paths), electron_count=len(electrons), seed_count=len(seeds), hard_count=len(hard)))
        inputs.extend([location / 'status.json', location / 'source.npz'])
    reference_path = PARENT / 'angular/a4-p18-w0.5/source.npz'
    current_path = ROOT / 'runs/s2-h3-g2-2-4/source.npz'
    reference, current = [dict(np.load(path)) for path in [reference_path, current_path]]
    relative = dual_norm(current['remainder'][1:-1] - reference['remainder'][1:-1], reference['mass']) / dual_norm(reference['remainder'][1:-1], reference['mass'])
    checks.append(dict(name='Full baseline source replay against sealed Stage94 within1e-7 relative', value=float(relative.max()), passed=bool(relative.max() < 1e-7)))
    finish(folder, dict(checks=checks, rows=rows, every_node_loop_identity_verified=True,
        private_loop_files=len(list((ROOT / 'virtual-cache').rglob('*.json')))), __file__, [*inputs, reference_path])
    print(json.dumps(dict(checks=checks, rows=rows)), flush=True)


if __name__ == '__main__':
    main()
