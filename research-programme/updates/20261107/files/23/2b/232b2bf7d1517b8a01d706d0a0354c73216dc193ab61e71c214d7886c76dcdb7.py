from outer_inputs import *
from fast_source import FastSplit


def main():
    modest()
    folder = ROOT / 'results/outer-inputs'
    folder.mkdir(parents=True, exist_ok=False)
    spectra = Spectra(.5)
    origin = BRANCH / 'population-matched-source-20261008/runs/midpoint-real-refinement'
    status = json.loads((origin / 'status.json').read_text())
    theta = status['temperature']
    baseline = list(population_nodes(theta, 2))
    sources = sorted((origin / 'nodes').glob('*.json'))
    assert len(sources) == len(baseline) == 672
    mismatch = max(float(np.max(abs(np.asarray(node['velocity']) - np.asarray(json.loads(path.read_text())['identity']['velocity']))))
                   for node, path in zip(baseline, sources))
    for node, path in zip(baseline, sources):
        assert node == json.loads(path.read_text())['identity']
    cache = LoopCache()
    checks = [dict(name='Regenerated baseline exactly matches every saved population identity', passed=mismatch == 0)]
    rows, inputs = [], [origin / 'status.json', *sources]
    model = FastSplit(spectra, 'difference')
    rule = PanelRule(.5)
    for label, node in [('existing', baseline[25]), ('new-seed3', list(population_nodes(theta, 3))[25])]:
        parameters = weak.source.context(theta * node['frequency'], node['cosine'], np.asarray(node['velocity']), theta)
        started = time.monotonic()
        scalar, path, computed = cache.get(parameters)
        loop_seconds = time.monotonic() - started
        started = time.monotonic()
        result = model.real(parameters, angular=4, radial=18, rule=rule)
        real_seconds = time.monotonic() - started
        started = time.monotonic()
        state = model.state_correction(parameters)
        state_seconds = time.monotonic() - started
        rows.append(dict(label=label, loop_seconds=loop_seconds, real_seconds=real_seconds,
            state_seconds=state_seconds, computed=computed, loop_scalar=scalar, identity=node,
            event_energy_null=result['event_energy_null']))
        inputs.append(path)
        print(json.dumps(rows[-1]), flush=True)
    checks.extend([
        dict(name='Existing source-owned loop reused without rewriting parent', passed=not rows[0]['computed']),
        dict(name='New loop computed in current checkpoint', passed=rows[1]['computed']),
        dict(name='Actual new node finite with conserved event energy',
             passed=bool(np.isfinite(rows[1]['loop_scalar'])) and rows[1]['event_energy_null'] < 1e-10),
    ])
    finish(folder, dict(checks=checks, rows=rows, baseline_nodes=len(baseline), new_seed_order3_nodes=len(list(population_nodes(theta, 3)))), __file__, [*inputs, *spectra.inputs])
    print(json.dumps(dict(checks=checks)), flush=True)


if __name__ == '__main__':
    main()
