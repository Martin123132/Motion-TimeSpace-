import argparse
from direction_common import *
import sampled_gould_control as leading


def physical_nodes(theta, part, hard_order):
    if part == 'expensive':
        yield from population_nodes(theta, 4, hard_order)
        return
    electrons = {}
    for identity in population_nodes(theta, 4):
        electrons[tuple(identity['velocity'])] = identity['electron_weight']
    hard_nodes, hard_weights = np.polynomial.legendre.leggauss(hard_order)
    index = 0
    for velocity, electron_weight in electrons.items():
        for frequency, seed_weight in compact_rule(128, 1e-5, 24.):
            for cosine, hard_weight in zip(hard_nodes, hard_weights):
                yield dict(index=index, frequency=float(frequency), seed_weight=float(seed_weight), cosine=float(cosine),
                    hard_weight=float(hard_weight), velocity=list(velocity), electron_weight=electron_weight)
                index += 1


def run(part, hard_order=5):
    spectra = Spectra(.5)
    owner = OUTER / 'runs/s4-h3-g2-2-4' if part == 'expensive' else PARENT / 'runs/compact128-h3-g2-2-4'
    owner_root = OUTER if part == 'expensive' else PARENT
    seal = json.loads((owner_root / 'results/stage-integrity.json').read_text())
    owner_report = json.loads((owner / 'status.json').read_text())
    assert owner_report['all_checks_passed']
    theta = owner_report['configuration']['temperature']
    cache = {}
    for path in sorted((owner / 'nodes').rglob('*.npz')):
        assert digest(path) == seal['file_hashes'][path.relative_to(owner_root).as_posix()]
        saved = dict(np.load(path))
        cache[node_key(json.loads(str(saved['identity'])))] = (path, saved)
    model = FastSplit(spectra, 'difference') if part == 'expensive' else SplitReal(spectra, 'control')
    keys = ['difference', 'virtual', 'state'] if part == 'expensive' else ['control']
    rule = PanelRule(.5)
    folder = ROOT / 'runs' / f'{part}-h{hard_order}'
    folder.mkdir(parents=True, exist_ok=True)
    assert not (folder / 'COMPLETE').exists()
    config = dict(part=part, hard_order=hard_order, incoming_rule='seed4' if part == 'expensive' else 'compact128',
        temperature=theta, electron_count=16, soft_angular=4, panel_order=18, panel_width=.5, virtual_order=2,
        fingerprints={str(path):digest(path) for path in [Path(__file__), ROOT / 'direction_common.py', ROOT / 'ACCEPTANCE.md',
            owner / 'source.npz', owner_root / 'results/stage-integrity.json']})
    config_path = folder / 'configuration.json'
    if config_path.exists():
        assert json.loads(config_path.read_text()) == config
    else:
        write_json(config_path, config)
    nodes = list(physical_nodes(theta, part, hard_order))
    totals = {key:np.zeros((98, 4)) for key in keys}
    inputs = [config_path, owner / 'status.json', owner / 'source.npz']
    started, maximum_null, reused = time.monotonic(), 0., 0
    for index, identity in enumerate(nodes):
        path = folder / 'nodes' / f'{index // 500:03d}' / f'{index:05d}.npz'
        parameters = weak.source.context(theta * identity['frequency'], identity['cosine'], np.array(identity['velocity']), theta)
        weight = identity['electron_weight'] * identity['seed_weight'] * identity['frequency']**2 / math.expm1(identity['frequency']) / I3
        weight *= 2 * np.pi * identity['hard_weight'] * parameters['born_differential_over_thomson']
        if path.exists():
            saved = dict(np.load(path))
            assert json.loads(str(saved['identity'])) == identity
            assert abs(float(saved['weight']) / weight - 1) < 1e-14
        else:
            referenced = cache.get(node_key(identity))
            if referenced is not None:
                old_path, old = referenced
                saved = {key:old[key] for key in keys}
                saved.update(event_energy_null=old['event_energy_null'], reuse_path=str(old_path))
                if part == 'expensive':
                    saved.update(loop_scalar=old['loop_scalar'], loop_path=old['loop_path'])
            else:
                result = model.real(parameters, angular=4, radial=18, rule=rule)
                saved = dict(event_energy_null=result['event_energy_null'], reuse_path='')
                if part == 'expensive':
                    scalar, loop_path = owned_loop(parameters)
                    weak.vacuum.mp.mp.dps = 60
                    vacuum = float(weak.vacuum.finite_virtual_ratio(parameters['energy'], parameters['cosine'])
                        + weak.vacuum.soft_constant(parameters['energy'], parameters['cosine']))
                    jump, product = model.born_data(parameters)
                    saved.update(difference=result['total'], virtual=.5 * (vacuum + scalar) * product,
                        state=model.state_correction(parameters)['total'], loop_scalar=scalar, loop_path=str(loop_path))
                else:
                    saved['control'] = result['total']
            saved.update(identity=json.dumps(identity, sort_keys=True), weight=weight)
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_suffix('.tmp')
            with temporary.open('wb') as handle:
                np.savez(handle, **saved)
            temporary.replace(path)
        for key in keys:
            assert saved[key].shape == (98, 4) and np.isfinite(saved[key]).all()
            totals[key] -= weight * saved[key]
        maximum_null = max(maximum_null, float(saved['event_energy_null']))
        inputs.append(path)
        if str(saved['reuse_path']):
            inputs.append(Path(str(saved['reuse_path'])))
            reused += 1
        if part == 'expensive':
            inputs.append(Path(str(saved['loop_path'])))
        elapsed = time.monotonic() - started
        progress = dict(state='running', part=part, completed_nodes=index + 1, total_nodes=len(nodes), pid=os.getpid(),
            elapsed_seconds=elapsed, estimated_remaining_seconds=elapsed / (index + 1) * (len(nodes) - index - 1))
        write_json(folder / 'progress.json', progress)
        if (index + 1) % max(1, len(nodes) // 4) == 0:
            print(json.dumps(progress), flush=True)
    checks = [dict(name='All96 source components and four profiles finite: ' + part, passed=True),
        dict(name='Exact event photon/gas exchange: ' + part, value=maximum_null, passed=maximum_null < 1e-10)]
    if part == 'control':
        old_rule, old_radial = leading.incoming_rule, leading.logarithmic_rule
        leading.incoming_rule, leading.logarithmic_rule = compact_rule, rule
        try:
            sampled = leading.sampled(spectra, model.tests, theta, 128, 18)
        finally:
            leading.incoming_rule, leading.logarithmic_rule = old_rule, old_radial
        reference = dict(np.load(owner / 'source.npz'))['sampled_leading']
        checks.append(dict(name='Hard-angle-independent matched leading subtraction unchanged', passed=bool(np.array_equal(sampled, reference))))
        totals.update(sampled_leading=sampled, kinematic_remainder=totals['control'] - sampled)
    np.savez(folder / 'source.npz', **totals, mass=spectra.basis.mass, temperature=spectra.basis.temperature, chemical=spectra.basis.chemical)
    finish(folder, dict(checks=checks, configuration=config, nodes=len(nodes), reused_nodes=reused,
        elapsed_seconds=time.monotonic() - started, hard_direction_gate_closed=False,
        full_parent_feedback_applied=False, new_parent_history=False), __file__, [*inputs, *spectra.inputs])
    print(json.dumps(dict(part=part, checks=checks, nodes=len(nodes), reused=reused)), flush=True)


if __name__ == '__main__':
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--parts', nargs='+', choices=['expensive', 'control'], required=True)
    parser.add_argument('--hard-order', type=int, default=5)
    arguments = parser.parse_args()
    for part in arguments.parts:
        run(part, arguments.hard_order)
