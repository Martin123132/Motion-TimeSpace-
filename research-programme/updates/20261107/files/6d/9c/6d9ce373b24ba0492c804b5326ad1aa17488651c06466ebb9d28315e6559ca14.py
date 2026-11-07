import argparse
from population_common import *
from resolved_redistribution import incoming_rule


def main():
    modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('--name', required=True)
    parser.add_argument('--fraction', type=float, default=.5)
    parser.add_argument('--seed-order', type=int, default=1)
    parser.add_argument('--seed-maximum', type=float, default=24.)
    parser.add_argument('--hard-order', type=int, default=2)
    parser.add_argument('--gas-radial', type=int, default=1)
    parser.add_argument('--gas-polar', type=int, default=2)
    parser.add_argument('--gas-azimuth', type=int, default=2)
    parser.add_argument('--virtual-order', type=int, default=2)
    parser.add_argument('--soft-angular', type=int, default=2)
    parser.add_argument('--soft-order', type=int, default=16)
    parser.add_argument('--soft-floor', type=float, default=1e-6)
    arguments = parser.parse_args()
    folder = ROOT / 'runs' / arguments.name
    folder.mkdir(parents=True, exist_ok=True)
    if (folder / 'COMPLETE').exists():
        raise ValueError('Completed run is immutable')
    configuration = folder / 'configuration.json'
    identity = dict(arguments=vars(arguments), script_sha256=digest(__file__), common_sha256=digest(ROOT / 'population_common.py'))
    if configuration.exists():
        assert json.loads(configuration.read_text()) == identity
    else:
        write_json(configuration, identity)
    spectra = Spectra(arguments.fraction)
    weak.functions, weak.derivatives = spectra.functions, spectra.derivatives
    background = thermal_wave.thermal.ThermalBackground('heavy')
    theta = background.at(spectra.coordinate)['thermal_parameter']
    cosines, hard_weights = np.polynomial.legendre.leggauss(arguments.hard_order)
    electrons = []
    for meridian, weight in prior.inherited.inherited.gas_rule(theta, arguments.gas_radial, arguments.gas_polar):
        for azimuth in np.arange(arguments.gas_azimuth) * 2 * np.pi / arguments.gas_azimuth:
            electrons.append((np.array([meridian[0] * math.cos(azimuth), meridian[0] * math.sin(azimuth), meridian[2]]), weight / arguments.gas_azimuth))
    seeds = list(incoming_rule(arguments.seed_order, 1e-5, arguments.seed_maximum))
    total_nodes = len(electrons) * len(seeds) * len(cosines)
    parts = {key: np.zeros((6, 6)) for key in ['total', 'born', 'real', 'virtual', 'state']}
    node_paths, cache_paths, event_null, solved, maximum_seconds = [], set(), 0., 0, 0.
    started = time.monotonic()
    node_folder = folder / 'nodes'
    node_folder.mkdir(exist_ok=True)
    for velocity, electron_weight in electrons:
        for frequency, frequency_weight in seeds:
            for cosine, hard_weight in zip(cosines, hard_weights):
                node = solved
                path = node_folder / ('%05d.json' % node)
                parameters = weak.source.context(theta * frequency, float(cosine), velocity, theta)
                node_identity = dict(index=node, frequency=frequency, seed_weight=frequency_weight,
                                     cosine=float(cosine), hard_weight=float(hard_weight),
                                     velocity=velocity.tolist(), electron_weight=electron_weight)
                if path.exists():
                    row = json.loads(path.read_text())
                    assert row['identity'] == node_identity and row['complete']
                else:
                    tick = time.monotonic()
                    virtual, cache_path, computed = source_cache(parameters, arguments.virtual_order)
                    result = weak.matched(parameters, virtual, arguments.soft_angular, arguments.soft_order,
                                          lower_fraction=arguments.soft_floor)
                    pieces = dict(total=result['total'], born=result['born'], real=result['real']['total'],
                                  virtual=result['virtual'], state=result['state']['total'])
                    seed_measure = frequency_weight * frequency**2 / math.expm1(frequency) / I3
                    measure = electron_weight * seed_measure * 2 * np.pi * hard_weight * parameters['born_differential_over_thomson']
                    row = dict(identity=node_identity, complete=True, weight=float(measure),
                               parts={key: value.tolist() for key, value in pieces.items()},
                               cache_path=str(cache_path), virtual_scalar=virtual, loop_computed=computed,
                               event_energy_null=result['real']['maximum_event_energy_null_residual'],
                               seconds=time.monotonic() - tick)
                    temporary = path.with_suffix('.tmp')
                    write_json(temporary, row)
                    temporary.replace(path)
                for key in parts:
                    parts[key] += row['weight'] * np.asarray(row['parts'][key])
                maximum_seconds = max(maximum_seconds, row['seconds'])
                event_null = max(event_null, row['event_energy_null'])
                cache_paths.add(Path(row['cache_path']))
                node_paths.append(path)
                solved += 1
                elapsed = time.monotonic() - started
                progress = dict(state='running', completed_nodes=solved, total_nodes=total_nodes,
                                elapsed_seconds=elapsed, pid=os.getpid(), estimated_remaining_seconds=elapsed / solved * (total_nodes - solved),
                                current_parts={key: value.tolist() for key, value in parts.items()})
                write_json(folder / 'progress.json', progress)
                if solved % max(1, total_nodes // 8) == 0:
                    print(json.dumps({key: value for key, value in progress.items() if key != 'current_parts'}), flush=True)
    coefficients = spectra.coefficients()
    currents = {key: -value @ coefficients for key, value in parts.items()}
    null = np.array([1., 0., 0., 0., 0., 1.])
    relative_null = float(np.linalg.norm(parts['total'] @ null) / max(np.linalg.norm(parts['total']), 1e-300))
    checks = [
        dict(name='Electron quadrature has unit fixed-density normalization', value=float(sum(item[1] for item in electrons)), passed=abs(sum(item[1] for item in electrons) - 1) < 1e-13),
        dict(name='Matched population matrix finite', passed=bool(all(np.isfinite(value).all() for value in parts.values()))),
        dict(name='Event photon and gas energies cancel before quadrature', value=event_null, passed=event_null < 1e-10),
        dict(name='Common-temperature null of population projection', value=relative_null, passed=relative_null < 1e-6),
        dict(name='Actual spectral-source energy exchange paired', value=float(np.max(abs(currents['total'][0] + currents['total'][-1]))),
             passed=np.max(abs(currents['total'][0] + currents['total'][-1])) < 1e-6 * max(np.max(abs(currents['total'])), 1e-30)),
        dict(name='Every virtual scalar tied to exact evaluated node', passed=len(cache_paths) > 0 and all(path.is_file() for path in cache_paths)),
    ]
    np.savez(folder / 'projection.npz', **parts, coefficients=coefficients, **{'current_' + key: value for key, value in currents.items()})
    report = dict(checks=checks, configuration=vars(arguments), nodes=total_nodes, temperature=theta,
        gas_slopes=spectra.gas, spectral_order=['heavy-wide-join', 'heavy-narrow-join', 'cold-wide-join', 'cold-narrow-join'],
        photon_energy_sources_per_tau={key: value[0].tolist() for key, value in currents.items()},
        gas_energy_sources_per_tau={key: value[-1].tolist() for key, value in currents.items()},
        elapsed_seconds=time.monotonic() - started, maximum_node_seconds=maximum_seconds,
        spectral_frequency_domain=[1e-6, 60.], seed_frequency_domain=[1e-5, arguments.seed_maximum],
        quadrature_refinement_accepted=False, source_inserted_in_parent=False,
        scope='Actual population/seed/direction finite-domain projection; quadrature acceptance and omitted-domain control recorded separately.')
    finish(folder, report, __file__, [configuration, *spectra.inputs, *node_paths, *cache_paths,
                                    background.parent.source, background.native_constants])
    print(json.dumps(dict(name=arguments.name, checks=len(checks), failed=[item['name'] for item in checks if not item['passed']],
                         sources=report['photon_energy_sources_per_tau'], elapsed=report['elapsed_seconds'])), flush=True)


if __name__ == '__main__':
    main()
