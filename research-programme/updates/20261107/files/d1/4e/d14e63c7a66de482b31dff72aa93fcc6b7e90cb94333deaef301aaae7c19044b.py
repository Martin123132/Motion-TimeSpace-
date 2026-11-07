from aligned_common import *


def main():
    modest()
    folder = ROOT / 'results/node-audit'
    folder.mkdir(parents=True, exist_ok=False)
    seal = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    checks, inputs, rows = [], [], []
    for order in [128, 160]:
        location = ROOT / 'runs' / f'compact{order}-h3-g2-2-4'
        report = json.loads((location / 'status.json').read_text())
        assert report['all_checks_passed']
        theta = report['configuration']['temperature']
        electrons = {}
        for identity in population_nodes(theta, 4):
            electrons[tuple(identity['velocity'])] = identity['electron_weight']
        hard_nodes, hard_weights = np.polynomial.legendre.leggauss(3)
        incoming = compact_rule(order, 1e-5, 24.)
        total, index, weight_error, reused = np.zeros((98, 4)), 0, 0., 0
        for velocity, electron_weight in electrons.items():
            for frequency, seed_weight in incoming:
                for cosine, hard_weight in zip(hard_nodes, hard_weights):
                    path = location / 'nodes' / f'{index // 500:03d}' / f'{index:05d}.npz'
                    saved = dict(np.load(path))
                    identity = dict(index=index, frequency=float(frequency), seed_weight=float(seed_weight),
                        cosine=float(cosine), hard_weight=float(hard_weight), velocity=list(velocity), electron_weight=electron_weight)
                    assert json.loads(str(saved['identity'])) == identity
                    parameters = weak.source.context(theta * frequency, cosine, np.array(velocity), theta)
                    weight = electron_weight * seed_weight * frequency**2 / math.expm1(frequency) / I3
                    weight *= 2 * np.pi * hard_weight * parameters['born_differential_over_thomson']
                    assert weight > 0 and np.isfinite(saved['control']).all() and saved['control'].shape == (98, 4)
                    weight_error = max(weight_error, float(abs(float(saved['weight']) / weight - 1)))
                    total -= weight * saved['control']
                    if str(saved['reuse_path']):
                        original = Path(str(saved['reuse_path']))
                        assert digest(original) == seal['file_hashes'][original.relative_to(PARENT).as_posix()]
                        old = dict(np.load(original))
                        assert node_key(json.loads(str(old['identity']))) == node_key(identity)
                        assert np.array_equal(old['control'], saved['control'])
                        reused += 1
                        inputs.append(original)
                    inputs.append(path)
                    index += 1
        source = dict(np.load(location / 'source.npz'))
        expected = dict(np.load(PARENT / 'runs/s4-h3-g2-2-4/source.npz'))
        assert index == report['nodes'] == len(list((location / 'nodes').rglob('*.npz')))
        reconstruction = float(np.max(abs(total - source['control']))) / float(np.max(abs(source['control'])))
        for key in ['difference', 'virtual', 'state', 'accurate_leading']:
            assert np.array_equal(source[key], expected[key])
        assert np.array_equal(source['kinematic_remainder'], source['control'] - source['sampled_leading'])
        assert np.array_equal(source['remainder'], source['kinematic_remainder'] + sum(source[key] for key in ['difference', 'virtual', 'state']))
        checks.extend([
            dict(name=f'All exact identities and pilot reuse hashes checked: compact{order}', passed=True, nodes=index, reused=reused),
            dict(name=f'Original positive population weights reproduced: compact{order}', value=weight_error, passed=weight_error < 1e-13),
            dict(name=f'Full control and whole mixed-source assembly independently checked: compact{order}',
                value=reconstruction, passed=reconstruction < 1e-12),
        ])
        rows.append(dict(order=order, nodes=index, reused=reused))
        inputs.extend([location / 'status.json', location / 'source.npz'])
    finish(folder, dict(checks=checks, rows=rows, every_control_node_verified=True,
        inherited_expensive_owner_unchanged=True), __file__, [*inputs, PARENT / 'runs/s4-h3-g2-2-4/source.npz'])
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
