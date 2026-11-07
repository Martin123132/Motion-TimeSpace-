import argparse
from panel_rule import *
import sampled_gould_control as leading


def run(order, width, angular):
    rule = PanelRule(width)
    spectra = Spectra(.5)
    model = SplitReal(spectra, 'control')
    origin = BRANCH / 'population-matched-source-20261008/runs/midpoint-real-refinement'
    original = json.loads((origin / 'status.json').read_text())
    origin_seal = json.loads((origin.parents[1] / 'results/stage-integrity.json').read_text())
    previous_path = PARENT / 'runs/midpoint-real-refinement-a4-r192/source.npz'
    previous = dict(np.load(previous_path))
    parent_seal = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    assert digest(previous_path) == parent_seal['file_hashes'][previous_path.relative_to(PARENT).as_posix()]
    name = f'a{angular}-p{order}-w{width:g}'
    folder = ROOT / 'runs' / name
    folder.mkdir(parents=True, exist_ok=True)
    assert not (folder / 'COMPLETE').exists()
    nodes_folder = folder / 'nodes'
    nodes_folder.mkdir(exist_ok=True)
    configuration = dict(angular=angular, panel_order=order, maximum_log_width=width,
        source_run=str(origin), parent_remainder=str(previous_path),
        fingerprints={str(path): digest(path) for path in [Path(__file__), ROOT / 'panel_rule.py',
            ROOT / 'control_common.py', previous_path, origin / 'status.json']})
    configuration_path = folder / 'configuration.json'
    if configuration_path.exists():
        assert json.loads(configuration_path.read_text()) == configuration
    else:
        write_json(configuration_path, configuration)
    source_paths = sorted((origin / 'nodes').glob('*.json'))
    total, maximum_null, started = np.zeros((98, 4)), 0., time.monotonic()
    inputs = [configuration_path, previous_path, previous_path.parent / 'status.json', origin / 'status.json']
    for index, path in enumerate(source_paths):
        fingerprint = digest(path)
        assert fingerprint == origin_seal['file_hashes'][path.relative_to(origin.parents[1]).as_posix()]
        source = json.loads(path.read_text())
        output = nodes_folder / (path.stem + '.npz')
        if output.exists():
            saved = dict(np.load(output))
            assert str(saved['source_sha256']) == fingerprint
        else:
            context = source['identity']
            parameters = weak.source.context(original['temperature'] * context['frequency'], context['cosine'],
                np.array(context['velocity']), original['temperature'])
            result = model.real(parameters, angular=angular, radial=order, rule=rule)
            saved = dict(control=result['total'], event_energy_null=result['event_energy_null'], source_sha256=fingerprint)
            temporary = output.with_suffix('.tmp')
            with temporary.open('wb') as handle:
                np.savez(handle, **saved)
            temporary.replace(output)
        total -= source['weight'] * saved['control']
        maximum_null = max(maximum_null, float(saved['event_energy_null']))
        inputs.extend([path, output])
        elapsed = time.monotonic() - started
        progress = dict(state='running', name=name, completed_nodes=index + 1, total_nodes=len(source_paths),
            pid=os.getpid(), elapsed_seconds=elapsed,
            estimated_remaining_seconds=elapsed / (index + 1) * (len(source_paths) - index - 1))
        write_json(folder / 'progress.json', progress)
        if (index + 1) % 168 == 0:
            print(json.dumps(progress), flush=True)
    original_rule = leading.logarithmic_rule
    leading.logarithmic_rule = rule
    try:
        sampled = leading.sampled(spectra, model.tests, original['temperature'], original['configuration']['seed_order'], order)
    finally:
        leading.logarithmic_rule = original_rule
    kinematic = total - sampled
    remainder = previous['difference'] + previous['virtual'] + previous['state'] + kinematic
    corrected = previous['accurate_leading'] + remainder
    scale = max(float(np.max(abs(corrected[0]))), 1e-30)
    pair = float(np.max(abs(corrected[0] + corrected[-1])))
    representation = float(np.max(abs(spectra.basis.temperature @ corrected[1:-1] - corrected[0])))
    checks = [
        dict(name='All96 source tests and four profiles retained and finite', passed=corrected.shape == (98, 4) and bool(np.isfinite(corrected).all())),
        dict(name='Exact event photon/gas exchange retained', value=maximum_null, passed=maximum_null < 1e-10),
        dict(name='Integrated photon/gas pair retained', value=pair, passed=pair < 1e-6 * scale),
        dict(name='Independent energy row agrees with original temperature test', value=representation, passed=representation < 1e-6 * scale),
        dict(name='Stationary leading term leaves energy and gas exactly zero', passed=bool(np.max(abs(sampled[[0, -1]])) == 0)),
    ]
    np.savez(folder / 'source.npz', total=corrected, remainder=remainder, control=total,
        sampled_leading=sampled, accurate_leading=previous['accurate_leading'], kinematic_remainder=kinematic,
        difference=previous['difference'], virtual=previous['virtual'], state=previous['state'],
        mass=spectra.basis.mass, temperature=spectra.basis.temperature, chemical=spectra.basis.chemical)
    finish(folder, dict(checks=checks, configuration=configuration, nodes=len(source_paths),
        elapsed_seconds=time.monotonic() - started, reused_amplitude_difference_angular_order=4,
        reused_amplitude_difference_radial_order=192, all_dimension_remainder_gate_closed=False,
        new_virtual_loop_evaluations=0, new_exact_six_diagram_evaluations=0,
        full_parent_feedback_applied=False, control_angular_only_test=angular != 4),
        __file__, [*inputs, *spectra.inputs])
    print(json.dumps(dict(name=name, checks=checks, elapsed_seconds=time.monotonic() - started)), flush=True)


if __name__ == '__main__':
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--orders', nargs='+', type=int, required=True)
    parser.add_argument('--width', type=float, default=.5)
    parser.add_argument('--angular', type=int, default=4)
    arguments = parser.parse_args()
    for order in arguments.orders:
        run(order, arguments.width, arguments.angular)
