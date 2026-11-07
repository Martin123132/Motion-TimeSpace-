import argparse
from aligned_common import *
import sampled_gould_control as leading


def run(order):
    spectra = Spectra(.5)
    assert spectra.basis.pivot == .1
    parent_seal = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    assert digest(PARENT / 'results/stage-integrity.json') == PARENT_SEAL
    owner = PARENT / 'runs/s4-h3-g2-2-4'
    owner_report = json.loads((owner / 'status.json').read_text())
    assert owner_report['all_checks_passed']
    theta = owner_report['configuration']['temperature']
    inherited_source = dict(np.load(owner / 'source.npz'))
    electron_map = {}
    for identity in population_nodes(theta, 4):
        electron_map[tuple(identity['velocity'])] = identity['electron_weight']
    assert len(electron_map) == 16 and abs(sum(electron_map.values()) - 1) < 1e-14
    hard_nodes, hard_weights = np.polynomial.legendre.leggauss(3)
    incoming = compact_rule(order, 1e-5, 24.)
    model, radial = SplitReal(spectra, 'control'), PanelRule(.5)
    folder = ROOT / 'runs' / f'compact{order}-h3-g2-2-4'
    folder.mkdir(parents=True, exist_ok=True)
    assert not (folder / 'COMPLETE').exists()
    configuration = dict(incoming_coordinate='z=(x-.1)/(x+.1)', incoming_order=order,
        electron_count=16, hard_order=3, soft_angular=4, panel_order=18, panel_width=.5,
        source_profile_count=4, spectral_count=96, temperature=theta, frequency_window=[1e-5, 24.],
        expensive_source_owner=str(owner), fingerprints={str(path):digest(path) for path in
            [Path(__file__), ROOT / 'aligned_common.py', ROOT / 'ACCEPTANCE.md',
             PARENT / 'pilot_compact_control.py', PARENT / 'results/stage-integrity.json', owner / 'source.npz']})
    config_path = folder / 'configuration.json'
    if config_path.exists():
        assert json.loads(config_path.read_text()) == configuration
    else:
        write_json(config_path, configuration)
    cache = {}
    for path in sorted((PARENT / 'runs/compact-control-pilot/nodes' / f'n{order}').rglob('*.npz')):
        assert digest(path) == parent_seal['file_hashes'][path.relative_to(PARENT).as_posix()]
        saved = dict(np.load(path))
        cache[node_key(json.loads(str(saved['identity'])))] = (path, saved)
    total, maximum_null, index, reused = np.zeros((98, 4)), 0., 0, 0
    inputs = [config_path, owner / 'status.json', owner / 'source.npz']
    started = time.monotonic()
    count = len(electron_map) * order * 3
    for velocity_key, electron_weight in electron_map.items():
        velocity = np.array(velocity_key)
        for frequency, seed_weight in incoming:
            for cosine, hard_weight in zip(hard_nodes, hard_weights):
                identity = dict(index=index, frequency=float(frequency), seed_weight=float(seed_weight),
                    cosine=float(cosine), hard_weight=float(hard_weight), velocity=velocity.tolist(), electron_weight=electron_weight)
                path = folder / 'nodes' / f'{index // 500:03d}' / f'{index:05d}.npz'
                parameters = weak.source.context(theta * frequency, cosine, velocity, theta)
                weight = electron_weight * seed_weight * frequency**2 / math.expm1(frequency) / I3
                weight *= 2 * np.pi * hard_weight * parameters['born_differential_over_thomson']
                if path.exists():
                    saved = dict(np.load(path))
                    assert json.loads(str(saved['identity'])) == identity
                    assert abs(float(saved['weight']) / weight - 1) < 1e-14
                else:
                    referenced = cache.get(node_key(identity))
                    if referenced is None:
                        result = model.real(parameters, angular=4, radial=18, rule=radial)
                        saved = dict(control=result['total'], event_energy_null=result['event_energy_null'], reuse_path='')
                    else:
                        old_path, old = referenced
                        saved = dict(control=old['control'], event_energy_null=old['event_energy_null'], reuse_path=str(old_path))
                    saved.update(identity=json.dumps(identity, sort_keys=True), weight=weight)
                    path.parent.mkdir(parents=True, exist_ok=True)
                    temporary = path.with_suffix('.tmp')
                    with temporary.open('wb') as handle:
                        np.savez(handle, **saved)
                    temporary.replace(path)
                assert np.isfinite(saved['control']).all() and weight > 0
                total -= weight * saved['control']
                maximum_null = max(maximum_null, float(saved['event_energy_null']))
                inputs.append(path)
                if str(saved['reuse_path']):
                    inputs.append(Path(str(saved['reuse_path'])))
                    reused += 1
                index += 1
                elapsed = time.monotonic() - started
                progress = dict(state='running', order=order, completed_nodes=index, total_nodes=count,
                    elapsed_seconds=elapsed, estimated_remaining_seconds=elapsed / index * (count - index), pid=os.getpid())
                write_json(folder / 'progress.json', progress)
                if index % 768 == 0:
                    print(json.dumps(progress), flush=True)
    original_incoming, original_radial = leading.incoming_rule, leading.logarithmic_rule
    leading.incoming_rule, leading.logarithmic_rule = compact_rule, radial
    try:
        sampled = leading.sampled(spectra, model.tests, theta, order, 18)
    finally:
        leading.incoming_rule, leading.logarithmic_rule = original_incoming, original_radial
    kinematic = total - sampled
    pieces = {key:inherited_source[key] for key in ['difference', 'virtual', 'state']}
    remainder = kinematic + sum(pieces.values())
    complete = inherited_source['accurate_leading'] + remainder
    scale = max(float(np.max(abs(complete[0]))), 1e-30)
    pair_error = float(np.max(abs(complete[0] + complete[-1])))
    energy_error = float(np.max(abs(spectra.basis.temperature @ complete[1:-1] - complete[0])))
    measure_error = abs(sum(weight for frequency, weight in incoming) / (24. - 1e-5) - 1)
    checks = [
        dict(name='Original normalized16-electron measure and positive compact frequency quadrature',
            value=float(measure_error), passed=bool(measure_error < 1e-7)),
        dict(name='Complete finite96-mode four-profile mixed source retained', passed=bool(np.isfinite(complete).all() and complete.shape == (98, 4))),
        dict(name='Exact event photon/gas exchange retained', value=maximum_null, passed=maximum_null < 1e-10),
        dict(name='Integrated photon/gas exchange retained', value=pair_error, passed=pair_error < 1e-6 * scale),
        dict(name='Original temperature test matches independent energy row', value=energy_error, passed=energy_error < 1e-6 * scale),
    ]
    np.savez(folder / 'source.npz', control=total, sampled_leading=sampled, kinematic_remainder=kinematic,
        **pieces, remainder=remainder, total=complete, accurate_leading=inherited_source['accurate_leading'],
        mass=spectra.basis.mass, temperature=spectra.basis.temperature, chemical=spectra.basis.chemical)
    finish(folder, dict(checks=checks, configuration=configuration, nodes=count,
        reused_pilot_nodes=reused, new_virtual_loop_evaluations=0, separate_resolution_identity_used=True,
        incoming_frequency_gate_closed=False, all_dimension_remainder_gate_closed=False,
        new_parent_history=False, full_parent_feedback_applied=False,
        elapsed_seconds=time.monotonic() - started), __file__, [*inputs, *spectra.inputs])
    print(json.dumps(dict(order=order, checks=checks, reused_pilot_nodes=reused, complete=True)), flush=True)


if __name__ == '__main__':
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--orders', type=int, nargs='+', required=True)
    arguments = parser.parse_args()
    for order in arguments.orders:
        run(order)
