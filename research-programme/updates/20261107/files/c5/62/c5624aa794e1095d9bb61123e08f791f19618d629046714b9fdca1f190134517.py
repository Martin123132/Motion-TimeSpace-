from coupling238 import *
import argparse


def freeze():
    config = protocol()
    assert read(ROOT / 'results/hessian.json')['qualified']
    assert not (ROOT / 'port-configuration.json').exists()
    write(ROOT / 'port-configuration.json', dict(frozen_at=now(),
        files={name: digest(ROOT / name) for name in ('coupling238.py', 'ports238.py', 'algebra238.py')},
        configuration_sha256=digest(ROOT / 'configuration.json'), hessian_sha256=digest(ROOT / 'results/hessian.json'),
        identity_tolerance=config['identity_tolerance'], angular_response_gate=config['physical_response_tolerance'],
        negative_control_minimum=1e-7, wave_number=config['wave_number'],
        scope='Physical instantaneous source/stress/metric interface, not a closed full-bank spatial evolution'))


def local_context(system, history, theta, physical_gas):
    coordinate = float(np.log(system.theta[0] / theta))
    assert history['rows'][0, 0] <= coordinate <= history['rows'][-1, 0]
    columns = [float(np.interp(coordinate, history['rows'][:, 0], history['rows'][:, index])) for index in (12, 13, 14)]
    hubble = columns[0] * (1 + columns[1]) * (1 + columns[2])
    scale = system.background.start_scale * np.exp(coordinate)
    parent = system.background.parent
    reference = parent.photons / scale**4
    rest = parent.baryons / scale**3 / reference
    opacity = parent.opacity_constant / scale**2
    ratio = 1 + physical_gas
    eos = gravity.eos_at(system.mixture, theta, ratio)
    local = gravity.gas_coefficients(hubble, rest, system.heat, ratio, eos, 0.)
    return dict(local=local, scale=float(scale), reference=float(reference), opacity=float(opacity), coordinate=coordinate,
        background_transfer_reference='zero used only for the affine dQ derivative; no zero-transfer background evolution asserted',
        geometry_source='Interpolated retained Stage230 EOS H at matching theta; no on-shell claim for the frozen microscopic histories')


def background_derivative(local, checks, prefix):
    with mp.workdps(80):
        hubble, heat, capacity, capacity_R, ratio, energy, rest = [scalar(local[key]) for key in ('H', 'chi', 'C', 'C_R', 'R', 'A', 'rest')]
        density, temperature, velocity = map(mp.mpf, ('.3', '-.2', '.4'))
        scale = heat * hubble
        def primitive(argument):
            transfer = argument * scale
            ratio_prime = hubble * ratio - (2 * hubble * ratio + transfer / heat) / capacity
            capacity_prime = capacity_R * (ratio_prime - hubble * ratio)
            energy_prime = hubble * (energy - ratio * capacity) + capacity * ratio_prime
            inertia = rest + heat * (energy + 2 * ratio / 3)
            inertia_prime = hubble * rest + heat * (energy_prime + 2 * ratio_prime / 3)
            return ((hubble - 2 * hubble / capacity - capacity_prime / capacity) * temperature + transfer * density / (heat * capacity),
                    -inertia_prime * velocity / inertia)
        exact = [mp.diff(lambda argument: primitive(argument)[index], 0) for index in range(2)]
        result = background_transfer_tangent(local, float(scale), 0., 0., float(density), float(temperature), float(velocity))
        for name, measured, expected in [('temperature', result['temperature_rate'], exact[0]), ('velocity', result['velocity_rate'], exact[1])]:
            check(checks, prefix + ':independent dQ ' + name, abs(scalar(measured) / expected - 1))
        for name, measured, expected in [('energy', result['energy_defect'], float(scale * (density + capacity_R * temperature / capacity))),
                                       ('current', result['current_defect'], float(scale * (1 + 2 / (3 * capacity)) * velocity))]:
            check(checks, prefix + ':off-shell ' + name, normalization_error(measured, expected))


def run():
    modest()
    config = protocol()
    frozen = read(ROOT / 'port-configuration.json')
    for name, expected in frozen['files'].items():
        assert digest(ROOT / name) == expected, name
    assert digest(ROOT / 'results/hessian.json') == frozen['hessian_sha256']
    assert not (ROOT / 'results/ports.json').exists()
    inputs = read(ROOT / 'inputs.json')
    original, features, models = setup(config)
    basis = features.basis
    stored_basis = packet(ROOT / 'frozen/basis.npz')
    assert np.array_equal(basis.mass, stored_basis['mass']) and np.array_equal(basis.energy, stored_basis['energy'])
    systems = {model: gravity.prior.System(model, 6400, inputs) for model in ('heavy', 'cold')}
    histories = {model: packet(BRANCH / 'two-way-thermal-gravity-20261026' / 'runs' / (model + '-6400') / 'history.npz') for model in systems}
    exact, high, low = physical_states(config)
    checks, records, refinements = [], [], []
    for event in config['events']:
        anchor = event['label']
        matrices = packet(PARENT / 'results' / (anchor + '-assessment.npz'))
        background = packet(ROOT / 'results' / (anchor + '-quadratic-background.npz'))
        output, context_records = {}, []
        for state_index, state in enumerate(config['states']):
            context = local_context(systems[state['model']], histories[state['model']], event['theta'], float(exact[state_index][-1]))
            local, opacity, reference, scale = context['local'], context['opacity'], context['reference'], context['scale']
            context_records.append(dict(model=state['model'], history=state['history'], **context))
            background_derivative(local, checks, f'{anchor}:{state["model"]}:{state["history"]}')
            for join in config['joins']:
                for component in config['components']:
                    sources = {}
                    for version in config['angular_versions']:
                        prefix = f'angular{version}:join{join}:{state["model"]}:{state["history"]}'
                        quadratic_key = prefix + ':quadratic_background:' + component
                        quadratic = background[quadratic_key]
                        density_photon = opacity * quadratic[0]
                        density_gas = opacity * quadratic[-1]
                        density_rate = (density_gas + density_photon) / (local['chi'] * local['C'])
                        scale_density = max(abs(density_gas) + abs(density_photon), 1e-300)
                        check(checks, prefix + ':' + component + ':one-electron density heating cancellation', abs(density_rate * local['chi'] * local['C']) / scale_density)
                        output[prefix + ':' + component + ':density_weak'] = opacity * quadratic
                        output[prefix + ':' + component + ':density_gas_temperature_rate'] = np.array(density_rate)
                        sources[version] = {}
                        for degree in config['multipoles']:
                            key = prefix + f':l{degree}:' + component
                            matrix = matrices[key]
                            port = lift(matrix, degree, basis, opacity, local['chi'], local['C'], local['B'])
                            metric = metric_response(port, degree, reference, scale, local['C'])
                            source_scale = max(np.linalg.norm(port['direct_moment']) + np.linalg.norm(port['gas_moment']), 1e-300)
                            check(checks, key + ':weak-to-physical photon moment', normalization_error(port['photon_moment'], port['direct_moment']))
                            if degree < 2:
                                pair_error = np.linalg.norm(port['photon_moment'] + port['gas_moment']) / source_scale
                                check(checks, key + ':independent gas exchange', pair_error)
                                divisor = local['chi'] * local['C'] if degree == 0 else local['B']
                                check(checks, key + ':EOS primitive conversion', normalization_error(port['gas_rate'] * divisor, port['gas_moment']))
                                wrong_missing_gas = np.linalg.norm(port['photon_moment']) / source_scale
                                check(checks, key + ':omitted gas rejected', int(wrong_missing_gas <= frozen['negative_control_minimum']), 0)
                                if degree == 1:
                                    wrong_factor = np.linalg.norm(port['photon_moment'] / 3 + port['gas_moment']) / source_scale
                                    check(checks, key + ':missing dipole mass factor rejected', int(wrong_factor <= frozen['negative_control_minimum']), 0)
                            else:
                                pair_error = 0.
                                check(checks, key + ':trace-free shear metric response',
                                    np.linalg.norm(2 * metric['sigma_transverse_second'] + metric['sigma_longitudinal_second']) /
                                    max(np.linalg.norm(metric['sigma_transverse_second']) + np.linalg.norm(metric['sigma_longitudinal_second']), 1e-300))
                            for name in ('photon', 'gas_rate', 'photon_moment', 'gas_moment'):
                                output[key + ':' + name] = port[name]
                            for name, value in metric.items():
                                output[key + ':' + name] = value
                            sources[version][degree] = dict(photon=port['photon'], gas_rate=port['gas_rate'],
                                metric_transverse=metric['sigma_transverse_second'], metric_longitudinal=metric['sigma_longitudinal_second'])
                            records.append(dict(anchor=anchor, version=version, join=join, model=state['model'], history=state['history'],
                                component=component, degree=degree, paired_exchange_residual=float(pair_error),
                                normalized_energy_transfer_norm=float(np.linalg.norm(port['photon_moment'])),
                                gas_primitive_rate_norm=float(np.linalg.norm(port['gas_rate'])),
                                metric_second_derivative_norm=float(np.linalg.norm(np.vstack([metric['sigma_transverse_second'], metric['sigma_longitudinal_second']]))),
                                quadratic_density_photon_transfer=float(density_photon), quadratic_density_gas_transfer=float(density_gas)))
                    for degree in config['multipoles']:
                        for name in sources['8'][degree]:
                            first, middle, last = [sources[version][degree][name] for version in config['angular_versions']]
                            error = relative(middle, last)
                            label = f'{anchor}:join{join}:{state["model"]}:{state["history"]}:l{degree}:{component}:{name}'
                            check(checks, label + ':angular6-to8 physical port refinement', error, config['physical_response_tolerance'])
                            output[label + ':candidate_minus_original'] = last - first
                            delta_norm = np.linalg.norm(last - first)
                            refinements.append(dict(anchor=anchor, join=join, model=state['model'], history=state['history'], degree=degree,
                                component=component, port=name, angular6_to8=error, original_to8=relative(first, last),
                                refinement_over_delta=float(np.linalg.norm(last - middle) / max(delta_norm, 1e-300))))
        save(ROOT / 'results' / (anchor + '-ports.npz'), **output)
        write(ROOT / 'results' / (anchor + '-contexts.json'), context_records)
        print(json.dumps(dict(anchor=anchor, checks=len(checks), failures=sum(not row['passed'] for row in checks))), flush=True)
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    failed = [row for row in checks if not row['passed']]
    write(ROOT / 'results/port-inputs.json', inputs)
    report = dict(stage=238, state='complete', qualified=not failed, checks=checks, failed=failed, records=records,
        refinements=refinements, finished_at=now(), script_sha256=digest(__file__),
        maximum_refinement=max(row['angular6_to8'] for row in refinements),
        maximum_exchange_residual=max(row['paired_exchange_residual'] for row in records),
        explicit_tail_input_ports=True, closed_wave_evolved=False, original_bank_changed=False,
        scope='Physical rectangular source lift, quadratic density source and EOS/metric derivatives on retained anchors, without a tail or full-bank closure')
    write(ROOT / 'results/ports.json', report)
    print(json.dumps(dict(checks=len(checks), failure_count=len(failed), first_failures=failed[:10],
        maximum_refinement=report['maximum_refinement'], maximum_exchange_residual=report['maximum_exchange_residual'])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'run'])
    {'freeze': freeze, 'run': run}[parser.parse_args().mode]()
