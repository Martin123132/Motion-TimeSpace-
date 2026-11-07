import argparse
from panel_rule import *


def run(angular):
    spectra = Spectra(.5)
    models = {mode: SplitReal(spectra, mode) for mode in ['difference', 'control']}
    rule = PanelRule(.5)
    origin = BRANCH / 'population-matched-source-20261008/runs/midpoint-real-refinement'
    original = json.loads((origin / 'status.json').read_text())
    origin_seal = json.loads((origin.parents[1] / 'results/stage-integrity.json').read_text())
    radial_folder = ROOT / 'runs/a4-p18-w0.5'
    radial_status = json.loads((radial_folder / 'status.json').read_text())
    assert radial_status['all_checks_passed']
    reference = dict(np.load(radial_folder / 'source.npz'))
    folder = ROOT / 'angular' / f'a{angular}-p18-w0.5'
    folder.mkdir(parents=True, exist_ok=True)
    assert not (folder / 'COMPLETE').exists()
    nodes = folder / 'nodes'
    nodes.mkdir(exist_ok=True)
    configuration = dict(angular=angular, panel_order=18, maximum_log_width=.5,
        fingerprints={str(path):digest(path) for path in [Path(__file__), ROOT / 'panel_rule.py',
            ROOT / 'control_common.py', radial_folder / 'status.json', radial_folder / 'source.npz', origin / 'status.json']})
    configuration_path = folder / 'configuration.json'
    if configuration_path.exists():
        assert json.loads(configuration_path.read_text()) == configuration
    else:
        write_json(configuration_path, configuration)
    totals = {key: np.zeros((98, 4)) for key in models}
    inputs = [configuration_path, origin / 'status.json', radial_folder / 'status.json', radial_folder / 'source.npz']
    source_paths = sorted((origin / 'nodes').glob('*.json'))
    started, maximum_null = time.monotonic(), 0.
    for index, path in enumerate(source_paths):
        fingerprint = digest(path)
        assert fingerprint == origin_seal['file_hashes'][path.relative_to(origin.parents[1]).as_posix()]
        source = json.loads(path.read_text())
        output = nodes / (path.stem + '.npz')
        control_path = radial_folder / 'nodes' / output.name
        if output.exists():
            saved = dict(np.load(output))
            assert str(saved['source_sha256']) == fingerprint
        else:
            context = source['identity']
            parameters = weak.source.context(original['temperature'] * context['frequency'], context['cosine'],
                np.array(context['velocity']), original['temperature'])
            result = models['difference'].real(parameters, angular=angular, radial=18, rule=rule)
            saved = dict(difference=result['total'], event_energy_null=result['event_energy_null'], source_sha256=fingerprint)
            if angular == 4:
                cached = dict(np.load(control_path))
                assert str(cached['source_sha256']) == fingerprint
                saved['control'] = cached['control']
                saved['event_energy_null'] = max(saved['event_energy_null'], float(cached['event_energy_null']))
            else:
                control = models['control'].real(parameters, angular=angular, radial=18, rule=rule)
                saved['control'] = control['total']
                saved['event_energy_null'] = max(saved['event_energy_null'], control['event_energy_null'])
            temporary = output.with_suffix('.tmp')
            with temporary.open('wb') as handle:
                np.savez(handle, **saved)
            temporary.replace(output)
        for key in models:
            totals[key] -= source['weight'] * saved[key]
        maximum_null = max(maximum_null, float(saved['event_energy_null']))
        inputs.extend([path, output])
        if angular == 4:
            inputs.append(control_path)
        elapsed = time.monotonic() - started
        progress = dict(state='running', angular=angular, completed_nodes=index + 1, total_nodes=len(source_paths),
            pid=os.getpid(), elapsed_seconds=elapsed,
            estimated_remaining_seconds=elapsed / (index + 1) * (len(source_paths) - index - 1))
        write_json(folder / 'progress.json', progress)
        if (index + 1) % 168 == 0:
            print(json.dumps(progress), flush=True)
    kinematic = totals['control'] - reference['sampled_leading']
    remainder = totals['difference'] + reference['virtual'] + reference['state'] + kinematic
    total = reference['accurate_leading'] + remainder
    scale = max(float(np.max(abs(total[0]))), 1e-30)
    pair = float(np.max(abs(total[0] + total[-1])))
    energy = float(np.max(abs(spectra.basis.temperature @ total[1:-1] - total[0])))
    checks = [
        dict(name='All96 tests and four profiles finite', passed=total.shape == (98, 4) and bool(np.isfinite(total).all())),
        dict(name='Exact event energy exchange retained', value=maximum_null, passed=maximum_null < 1e-10),
        dict(name='Integrated photon/gas energy exchange retained', value=pair, passed=pair < 1e-6 * scale),
        dict(name='Independent energy matches original temperature test', value=energy, passed=energy < 1e-6 * scale),
    ]
    np.savez(folder / 'source.npz', **totals, total=total, remainder=remainder, kinematic_remainder=kinematic,
        virtual=reference['virtual'], state=reference['state'], accurate_leading=reference['accurate_leading'],
        sampled_leading=reference['sampled_leading'], mass=spectra.basis.mass,
        temperature=spectra.basis.temperature, chemical=spectra.basis.chemical)
    finish(folder, dict(checks=checks, configuration=configuration, nodes=len(source_paths),
        elapsed_seconds=time.monotonic() - started, new_virtual_loop_evaluations=0,
        exact_amplitude_difference_recomputed_for_angular_resolution=True,
        full_parent_feedback_applied=False, all_dimension_remainder_gate_closed=False),
        __file__, [*inputs, *spectra.inputs])
    print(json.dumps(dict(angular=angular, checks=checks, elapsed_seconds=time.monotonic() - started)), flush=True)


if __name__ == '__main__':
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--angular', nargs='+', type=int, required=True)
    arguments = parser.parse_args()
    for angular in arguments.angular:
        run(angular)
