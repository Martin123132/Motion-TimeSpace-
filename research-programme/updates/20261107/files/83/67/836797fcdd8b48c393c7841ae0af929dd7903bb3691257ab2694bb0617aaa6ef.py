import argparse
from split_real import *
from sampled_gould_control import sampled


def run(radial, source_run='midpoint-real-refinement', angular=4):
    origin = BRANCH / 'population-matched-source-20261008/runs' / source_run
    origin_status = json.loads((origin / 'status.json').read_text())
    previous = PARENT / 'runs' / ('midpoint-log-pilot' if source_run == 'midpoint-pilot' else 'midpoint-log48')
    theta = origin_status['temperature']
    settings = origin_status['configuration']
    spectra = Spectra(settings['fraction'])
    models = {mode: SplitReal(spectra, mode) for mode in ['control', 'difference']}
    name = f'{source_run}-a{angular}-r{radial}'
    folder = ROOT / 'runs' / name
    folder.mkdir(parents=True, exist_ok=True)
    assert not (folder / 'COMPLETE').exists()
    nodes_folder = folder / 'nodes'
    nodes_folder.mkdir(exist_ok=True)
    configuration = dict(radial=radial, angular=angular, source_run=source_run,
        files={str(path): digest(path) for path in [Path(__file__), ROOT / 'split_real.py',
        ROOT / 'rational_leading.py', origin / 'status.json', previous / 'status.json']})
    configuration_path = folder / 'configuration.json'
    if configuration_path.exists():
        assert json.loads(configuration_path.read_text()) == configuration
    else:
        write_json(configuration_path, configuration)
    ancestor = json.loads((PARENT / 'results/stage-integrity.json').read_text())
    older = json.loads((origin.parents[1] / 'results/stage-integrity.json').read_text())
    totals = {key: np.zeros((98, 4)) for key in ['control', 'difference', 'virtual', 'state']}
    inputs = [configuration_path, origin / 'status.json', previous / 'status.json']
    source_paths = sorted((origin / 'nodes').glob('*.json'))
    started, maximum_null = time.monotonic(), 0.
    for index, source_path in enumerate(source_paths):
        source_digest = digest(source_path)
        assert source_digest == older['file_hashes'][source_path.relative_to(origin.parents[1]).as_posix()]
        saved = json.loads(source_path.read_text())
        reference_path = previous / 'nodes' / source_path.name
        assert digest(reference_path) == ancestor['file_hashes'][reference_path.relative_to(PARENT).as_posix()]
        reference = json.loads(reference_path.read_text())
        assert reference['source_sha256'] == source_digest
        output_path = nodes_folder / (source_path.stem + '.npz')
        if output_path.exists():
            values = dict(np.load(output_path))
            assert str(values['source_sha256']) == source_digest
        else:
            context = saved['identity']
            parameters = weak.source.context(theta * context['frequency'], context['cosine'],
                                             np.array(context['velocity']), theta)
            results = {mode: model.real(parameters, angular=angular, radial=radial) for mode, model in models.items()}
            values = {mode: result['total'] for mode, result in results.items()}
            values.update(event_energy_null=max(result['event_energy_null'] for result in results.values()),
                          source_sha256=source_digest)
            temporary = output_path.with_suffix('.tmp')
            with temporary.open('wb') as handle:
                np.savez(handle, **values)
            temporary.replace(output_path)
        for mode in models:
            totals[mode] -= saved['weight'] * values[mode]
        for component in ['virtual', 'state']:
            totals[component] -= saved['weight'] * np.asarray(reference['parts'][component])
        maximum_null = max(maximum_null, float(values['event_energy_null']))
        inputs.extend([source_path, reference_path, output_path])
        elapsed = time.monotonic() - started
        progress = dict(state='running', name=name, completed_nodes=index + 1, total_nodes=len(source_paths),
            elapsed_seconds=elapsed, estimated_remaining_seconds=elapsed / (index + 1) * (len(source_paths) - index - 1), pid=os.getpid())
        write_json(folder / 'progress.json', progress)
        if (index + 1) % max(1, len(source_paths) // 4) == 0:
            print(json.dumps(progress), flush=True)
    low = sampled(spectra, models['control'].tests, theta, settings['seed_order'], radial)
    leading_path = PARENT / 'overlaps/midpoint-gould48/overlap.npz'
    accurate = dict(np.load(leading_path))['joined_new_domain']
    full = sum(totals.values())
    remainder = totals['difference'] + totals['virtual'] + totals['state'] + (totals['control'] - low)
    corrected = accurate + remainder
    scale = max(float(np.max(abs(full[0]))), 1e-30)
    pair = float(np.max(abs(corrected[0] + corrected[-1])))
    energy_identity = float(np.max(abs(spectra.basis.temperature @ corrected[1:-1] - corrected[0])))
    checks = [
        dict(name='Full 96-mode source and four profiles remain finite', passed=corrected.shape == (98, 4) and bool(np.isfinite(corrected).all())),
        dict(name='Event photon/gas exchange retained', value=maximum_null, passed=maximum_null < 1e-10),
        dict(name='Integrated photon/gas exchange retained', value=pair, passed=pair < 1e-6 * scale),
        dict(name='Independent energy row reproduced by original basis temperature test', value=energy_identity, passed=energy_identity < 1e-6 * scale),
        dict(name='Split and leading addback agree algebraically',
             value=float(np.max(abs(corrected - (full - low + accurate)))),
             passed=bool(np.max(abs(corrected - (full - low + accurate))) < 1e-12 * np.max(abs(corrected)))),
    ]
    np.savez(folder / 'source.npz', **totals, total=corrected, raw=full, remainder=remainder,
        sampled_leading=low, accurate_leading=accurate, kinematic_remainder=totals['control'] - low,
        mass=spectra.basis.mass, temperature=spectra.basis.temperature, chemical=spectra.basis.chemical)
    finish(folder, dict(checks=checks, configuration=configuration, nodes=len(source_paths),
        elapsed_seconds=time.monotonic() - started, full_parent_feedback_applied=False,
        small_remainder_gate_waived=False, new_virtual_loop_evaluations=0,
        estimator='Exact-kinematics amplitude difference plus its control-minus-sampled-Gould addback, virtual and state terms; then independent accurate Gould.'),
        __file__, [*inputs, *spectra.inputs, leading_path])
    print(json.dumps(dict(name=name, checks=checks, elapsed_seconds=time.monotonic() - started)), flush=True)


if __name__ == '__main__':
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--orders', type=int, nargs='+', required=True)
    parser.add_argument('--source-run', default='midpoint-real-refinement')
    parser.add_argument('--angular', type=int, default=4)
    arguments = parser.parse_args()
    for order in arguments.orders:
        run(order, arguments.source_run, arguments.angular)
