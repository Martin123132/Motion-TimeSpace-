import argparse
from rectangular_weak import *


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-run', required=True)
    parser.add_argument('--name', required=True)
    parser.add_argument('--angular', type=int)
    parser.add_argument('--radial', type=int)
    parser.add_argument('--density', type=int, default=48001)
    parser.add_argument('--limit', type=int)
    arguments = parser.parse_args()
    parent_folder = PARENT / 'runs' / arguments.source_run
    parent_status = json.loads((parent_folder / 'status.json').read_text())
    assert parent_status['state'] == 'complete' and parent_status['all_checks_passed']
    settings = parent_status['configuration']
    spectra = Spectra(settings['fraction'])
    model = Rectangular(spectra, arguments.density)
    angular = arguments.angular or settings['soft_angular']
    radial = arguments.radial or settings['soft_order']
    folder = ROOT / 'runs' / arguments.name
    folder.mkdir(parents=True, exist_ok=True)
    assert not (folder / 'COMPLETE').exists()
    scripts = [ROOT / name for name in ['rectangular_common.py', 'rectangular_weak.py', 'project_rectangular.py']]
    identity = dict(arguments=vars(arguments), source_sha256=digest(parent_folder / 'status.json'),
                    scripts={str(path): digest(path) for path in scripts})
    configuration = folder / 'configuration.json'
    if configuration.exists():
        assert json.loads(configuration.read_text()) == identity
    else:
        write_json(configuration, identity)
    node_folder = folder / 'nodes'
    node_folder.mkdir(exist_ok=True)
    source_paths = sorted((parent_folder / 'nodes').glob('*.json'))
    if arguments.limit:
        source_paths = source_paths[:arguments.limit]
    totals = {key: np.zeros((spectra.basis.count + 2, 4)) for key in ['total', 'born', 'real', 'virtual', 'state']}
    reference = {key: np.zeros((6, 4)) for key in totals}
    inputs, maximum_event, maximum_energy_comparison = [], 0., 0.
    parent_seal = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    started = time.monotonic()
    for index, source_path in enumerate(source_paths):
        assert digest(source_path) == parent_seal['file_hashes'][source_path.relative_to(PARENT).as_posix()]
        saved = json.loads(source_path.read_text())
        node_path = node_folder / source_path.name
        if node_path.exists():
            node = json.loads(node_path.read_text())
            assert node['complete'] and node['source_sha256'] == digest(source_path)
        else:
            context = saved['identity']
            parameters = weak.source.context(parent_status['temperature'] * context['frequency'], context['cosine'],
                                             np.array(context['velocity']), parent_status['temperature'])
            cache = Path(saved['cache_path'])
            assert digest(cache) == parent_seal['file_hashes'][cache.relative_to(PARENT).as_posix()]
            assert json.loads(cache.read_text())['scalar'] == saved['virtual_scalar']
            result = model.matched(parameters, saved['virtual_scalar'], angular, radial, settings['soft_floor'])
            node = dict(complete=True, source_sha256=digest(source_path), weight=saved['weight'],
                        event_energy_null=result.pop('event_energy_null'),
                        parts={key: value.tolist() for key, value in result.items()})
            temporary = node_path.with_suffix('.tmp')
            write_json(temporary, node)
            temporary.replace(node_path)
        for key in totals:
            totals[key] -= saved['weight'] * np.asarray(node['parts'][key])
            reference[key] -= saved['weight'] * np.asarray(saved['parts'][key]) @ spectra.coefficients()
        maximum_event = max(maximum_event, node['event_energy_null'])
        inputs.extend([source_path, node_path])
        elapsed = time.monotonic() - started
        progress = dict(state='running', completed_nodes=index + 1, total_nodes=len(source_paths),
                        pid=os.getpid(), elapsed_seconds=elapsed,
                        estimated_remaining_seconds=elapsed / (index + 1) * (len(source_paths) - index - 1))
        write_json(folder / 'progress.json', progress)
        if (index + 1) % max(1, len(source_paths) // 8) == 0:
            print(json.dumps(progress), flush=True)
    energy_error = float(np.max(abs(totals['total'][0] - reference['total'][0])))
    same_quadrature = angular == settings['soft_angular'] and radial == settings['soft_order']
    energy_scale = max(float(np.max(abs(reference['total'][0]))), 1e-30)
    energy_identity = float(np.max(abs(spectra.basis.temperature @ totals['total'][1:-1] - totals['total'][0])))
    paired = float(np.max(abs(totals['total'][0] + totals['total'][-1])))
    number = spectra.basis.chemical @ totals['total'][1:-1]
    checks = [
        dict(name='Full96-test finite rectangular source retained', passed=all(value.shape == (98, 4) and np.isfinite(value).all() for value in totals.values())),
        dict(name='Event energy exchange cancels independently', value=maximum_event, passed=maximum_event < 1e-10),
        dict(name='Source gas partner cancels photon energy', value=paired, passed=paired < 1e-6 * energy_scale),
        dict(name='Original temperature test reproduces independent energy row', value=energy_identity, passed=energy_identity < 1e-6 * energy_scale),
        dict(name='Saved Stage91 energy reproduced at identical quadrature or explicitly refined', value=energy_error,
             same_quadrature=same_quadrature, passed=not same_quadrature or energy_error < 1e-6 * energy_scale),
        dict(name='Physical photon number source not projected away', value=float(np.max(abs(number))), passed=bool(np.max(abs(number)) > 0)),
    ]
    np.savez(folder / 'source.npz', **totals, temperature=spectra.basis.temperature, chemical=spectra.basis.chemical,
             mass=spectra.basis.mass, number=number, reference_energy=reference['total'][0])
    finish(folder, dict(checks=checks, arguments=vars(arguments), epoch_fraction=settings['fraction'],
        temperature=parent_status['temperature'], nodes=len(source_paths), complete_outer_measure=arguments.limit is None,
        photon_energy=totals['total'][0].tolist(), gas_energy=totals['total'][-1].tolist(),
        photon_number=number.tolist(), energy_reference_relative_difference=energy_error / energy_scale,
        elapsed_seconds=time.monotonic() - started, new_virtual_loop_evaluations=0,
        full_parent_feedback_applied=False, vector_quadrature_accepted=False),
        __file__, [configuration, parent_folder / 'status.json', *spectra.inputs, *inputs])
    print(json.dumps(dict(name=arguments.name, checks=len(checks),
        failed=[item['name'] for item in checks if not item['passed']],
        energy=totals['total'][0].tolist(), number=number.tolist(),
        energy_comparison=energy_error / energy_scale, elapsed=time.monotonic() - started)), flush=True)


if __name__ == '__main__':
    main()
