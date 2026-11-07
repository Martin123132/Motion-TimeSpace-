import argparse
from sharded_loop_cache import *
from fast_source import FastSplit
import sampled_gould_control as leading


def run(seed_order, hard_order=3, gas_radial=2, gas_polar=2, gas_azimuth=4):
    spectra = Spectra(.5)
    models = {mode: FastSplit(spectra, mode) for mode in ['difference', 'control']}
    rule = PanelRule(.5)
    origin = BRANCH / 'population-matched-source-20261008/runs/midpoint-real-refinement'
    origin_status = json.loads((origin / 'status.json').read_text())
    theta = origin_status['temperature']
    cache = ShardedLoopCache()
    parent_seal = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    real_folder = PARENT / 'angular/a4-p18-w0.5'
    reference_path = real_folder / 'source.npz'
    reference = dict(np.load(reference_path))
    reference_map = {}
    for path in sorted((origin / 'nodes').glob('*.json')):
        assert digest(path) == cache.seal['file_hashes'][path.relative_to(cache.parent).as_posix()]
        saved = json.loads(path.read_text())
        reference_map[node_key(saved['identity'])] = (path, saved)
    name = f's{seed_order}-h{hard_order}-g{gas_radial}-{gas_polar}-{gas_azimuth}'
    folder = ROOT / 'runs' / name
    folder.mkdir(parents=True, exist_ok=True)
    assert not (folder / 'COMPLETE').exists()
    configuration = dict(seed_order=seed_order, hard_order=hard_order, gas_radial=gas_radial,
        gas_polar=gas_polar, gas_azimuth=gas_azimuth, soft_angular=4, panel_order=18, panel_width=.5,
        virtual_order=2, temperature=theta, fingerprints={str(path):digest(path) for path in
            [Path(__file__), ROOT / 'fast_source.py', ROOT / 'sharded_loop_cache.py',
             ROOT / 'outer_inputs.py', reference_path, origin / 'status.json', PARENT / 'results/stage-integrity.json']})
    config_path = folder / 'configuration.json'
    if config_path.exists():
        assert json.loads(config_path.read_text()) == configuration
    else:
        write_json(config_path, configuration)
    nodes = list(population_nodes(theta, seed_order, hard_order, gas_radial, gas_polar, gas_azimuth))
    totals = {key: np.zeros((98, 4)) for key in ['difference', 'control', 'virtual', 'state']}
    inputs = [config_path, reference_path, real_folder / 'status.json', origin / 'status.json']
    newly_computed_loops, reused_real_nodes, maximum_null = 0, 0, 0.
    started = time.monotonic()
    for index, node in enumerate(nodes):
        path = folder / 'nodes' / f'{index // 500:03d}' / f'{index:05d}.npz'
        path.parent.mkdir(parents=True, exist_ok=True)
        identity = json.dumps(node, sort_keys=True)
        referenced = reference_map.get(node_key(node))
        if path.exists():
            saved = dict(np.load(path))
            assert str(saved['identity']) == identity
        else:
            parameters = weak.source.context(theta * node['frequency'], node['cosine'], np.asarray(node['velocity']), theta)
            scalar, loop_path, computed = cache.get(parameters)
            newly_computed_loops += int(computed)
            if referenced is not None:
                source_path, original = referenced
                real_path = real_folder / 'nodes' / (source_path.stem + '.npz')
                assert digest(real_path) == parent_seal['file_hashes'][real_path.relative_to(PARENT).as_posix()]
                real = dict(np.load(real_path))
                assert str(real['source_sha256']) == digest(source_path)
                saved = dict(difference=real['difference'], control=real['control'], event_energy_null=real['event_energy_null'])
            else:
                result = {mode: model.real(parameters, angular=4, radial=18, rule=rule) for mode, model in models.items()}
                saved = {mode: value['total'] for mode, value in result.items()}
                saved['event_energy_null'] = max(value['event_energy_null'] for value in result.values())
            weak.vacuum.mp.mp.dps = 60
            vacuum = float(weak.vacuum.finite_virtual_ratio(parameters['energy'], parameters['cosine'])
                           + weak.vacuum.soft_constant(parameters['energy'], parameters['cosine']))
            jump, product = models['difference'].born_data(parameters)
            saved['virtual'] = .5 * (vacuum + scalar) * product
            saved['state'] = models['difference'].state_correction(parameters)['total']
            seed_weight = node['seed_weight'] * node['frequency']**2 / math.expm1(node['frequency']) / I3
            weight = node['electron_weight'] * seed_weight * 2 * np.pi * node['hard_weight'] * parameters['born_differential_over_thomson']
            saved.update(identity=identity, weight=weight, loop_scalar=scalar, loop_path=str(loop_path), real_reused=referenced is not None)
            temporary = path.with_suffix('.tmp')
            with temporary.open('wb') as handle:
                np.savez(handle, **saved)
            temporary.replace(path)
        for key in totals:
            totals[key] -= float(saved['weight']) * saved[key]
        maximum_null = max(maximum_null, float(saved['event_energy_null']))
        reused_real_nodes += int(saved['real_reused'])
        inputs.extend([path, Path(str(saved['loop_path']))])
        if referenced is not None:
            source_path, original = referenced
            inputs.extend([source_path, real_folder / 'nodes' / (source_path.stem + '.npz')])
        elapsed = time.monotonic() - started
        progress = dict(state='running', name=name, completed_nodes=index + 1, total_nodes=len(nodes), pid=os.getpid(),
            elapsed_seconds=elapsed, estimated_remaining_seconds=elapsed / (index + 1) * (len(nodes) - index - 1),
            new_loops_this_invocation=newly_computed_loops)
        write_json(folder / 'progress.json', progress)
        if (index + 1) % max(1, len(nodes) // 4) == 0:
            print(json.dumps(progress), flush=True)
    original_rule = leading.logarithmic_rule
    leading.logarithmic_rule = rule
    try:
        sampled = leading.sampled(spectra, models['control'].tests, theta, seed_order, 18)
    finally:
        leading.logarithmic_rule = original_rule
    kinematic = totals['control'] - sampled
    remainder = totals['difference'] + totals['virtual'] + totals['state'] + kinematic
    total = reference['accurate_leading'] + remainder
    scale = max(float(np.max(abs(total[0]))), 1e-30)
    pair = float(np.max(abs(total[0] + total[-1])))
    energy = float(np.max(abs(spectra.basis.temperature @ total[1:-1] - total[0])))
    checks = [
        dict(name='Complete all96-mode four-profile finite source', passed=total.shape == (98, 4) and bool(np.isfinite(total).all())),
        dict(name='Independent exact photon/gas event exchange', value=maximum_null, passed=maximum_null < 1e-10),
        dict(name='Integrated photon/gas exchange retained', value=pair, passed=pair < 1e-6 * scale),
        dict(name='Independent energy matches original temperature test', value=energy, passed=energy < 1e-6 * scale),
        dict(name='Every loop attached to its actual source node', passed=len(inputs) > 0 and all(Path(str(path)).is_file() for path in inputs)),
    ]
    np.savez(folder / 'source.npz', **totals, total=total, remainder=remainder, kinematic_remainder=kinematic,
        sampled_leading=sampled, accurate_leading=reference['accurate_leading'], mass=spectra.basis.mass,
        chemical=spectra.basis.chemical, temperature=spectra.basis.temperature)
    finish(folder, dict(checks=checks, configuration=configuration, nodes=len(nodes),
        elapsed_seconds=time.monotonic() - started, new_virtual_loops_this_invocation=newly_computed_loops,
        reused_exact_real_nodes=reused_real_nodes, all_dimension_remainder_gate_closed=False,
        full_parent_feedback_applied=False, seed_domain=[1e-5, 24.]), __file__, [*inputs, *spectra.inputs])
    print(json.dumps(dict(name=name, checks=checks, new_loops=newly_computed_loops,
        reused_real_nodes=reused_real_nodes, elapsed_seconds=time.monotonic() - started)), flush=True)


if __name__ == '__main__':
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--seeds', type=int, nargs='+', required=True)
    parser.add_argument('--hard-order', type=int, default=3)
    parser.add_argument('--gas-radial', type=int, default=2)
    parser.add_argument('--gas-polar', type=int, default=2)
    parser.add_argument('--gas-azimuth', type=int, default=4)
    arguments = parser.parse_args()
    for order in arguments.seeds:
        run(order, arguments.hard_order, arguments.gas_radial, arguments.gas_polar, arguments.gas_azimuth)
