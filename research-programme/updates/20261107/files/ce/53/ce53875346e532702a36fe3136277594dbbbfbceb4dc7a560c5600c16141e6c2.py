from mixed_vertex233 import *
import argparse


def freeze():
    config = protocol()
    path = ROOT / 'run-configuration.json'
    assert not path.exists()
    write(path, dict(frozen_at=now(), configuration_sha256=digest(ROOT / 'configuration.json'),
        files={name: digest(ROOT / name) for name in ('run233.py', 'mixed_vertex233.py')},
        derivative_step='1e-20', mixed_background_step='1e-12', projection_order=6,
        exact_tolerance=config['identity_tolerance'], microscopic_inclusive_operator_qualified=False))
    print('Event geometry, histories, derivative tests and gates frozen.', flush=True)


def run_protocol():
    config = protocol()
    frozen = read(ROOT / 'run-configuration.json')
    assert digest(ROOT / 'configuration.json') == frozen['configuration_sha256']
    for name, value in frozen['files'].items():
        assert digest(ROOT / name) == value, name
    return config, frozen


def setup(config):
    original, theta = source.context(config['target_fraction'])
    assert theta == config['target_theta']
    features = cached.CachedFeatures(original)
    bundle = production.prior.lift.OperatorBundle(features, original.inputs)
    models = cached.models(bundle)
    return original, features, models


def replay():
    config, frozen = run_protocol()
    checks, comparisons = [], []
    coefficients = packet(config['coefficient_path'])
    factor = linear.cholesky(packet(PRODUCTION / 'frozen/basis-metric.npz')['mass'], lower=True)
    for event in config['events']:
        operator = packet(event['operator_path'])
        predicted = production.contract_histories((operator['high'], operator['low']), coefficients)
        save(ROOT / 'replay' / (event['label'] + '-frozen.npz'), high=predicted[0], low=predicted[1])
        frozen_at = now()
        actual = packet(event['source_path'])
        production.helpers.compare(event['label'], predicted, (actual['high'], actual['low']), factor, checks, comparisons)
        write(ROOT / 'replay' / (event['label'] + '-provenance.json'), dict(prediction_frozen_at=frozen_at,
            source_sha256=digest(event['source_path']), operator_sha256=digest(event['operator_path'])))
    report = dict(checks=checks, comparisons=comparisons, failed=[row for row in checks if not row['passed']],
        state='complete', scope='Existing production inclusive scalar operator on the frozen history repair; separate from the new mixed vertex',
        finished_at=now(), maximum_relative_error=max(row['relative'] for row in comparisons))
    write(ROOT / 'results/scalar-replay.json', report)
    print(json.dumps(dict(replay_checks=len(checks), failed=len(report['failed']), maximum=report['maximum_relative_error'])), flush=True)
    assert not report['failed'], report['failed']


def selected_events(parameters, config):
    yield 'born', geometry(parameters)
    directions = list(angular.inherited.source.angular_nodes(config['angular_rule']))
    for index in config['real_direction_indices']:
        direction, unused_weight = directions[index]
        doppler = angular.inherited.source.dot(parameters['bath'], np.r_[1., direction])
        for sign in (1, -1):
            upper = angular.inherited.source.bath_ordered_upper(parameters, direction) if sign == 1 else parameters['lab_energy'] / doppler
            for fraction in config['real_upper_fractions']:
                yield f'real-{index}-{sign}-{fraction}', geometry(parameters, sign * fraction * upper, direction)


def vector(coefficients):
    return list(coefficients['photon']) + [coefficients['gas']] + list(coefficients['velocity']) + [coefficients['density']]


def mp_relative(first, second):
    return float(mp.sqrt(mp.fsum((value - reference)**2 for value, reference in zip(first, second)))
                 / max(mp.sqrt(mp.fsum(value**2 for value in second)), mp.mpf('1e-300')))


def scalar_product(coefficients, photon_wave, gas_wave, velocity_wave, density_wave):
    return mp.fsum(value * wave for value, wave in zip(coefficients['photon'], photon_wave)) + coefficients['gas'] * gas_wave \
        + mp.fsum(value * wave for value, wave in zip(coefficients['velocity'], velocity_wave)) + coefficients['density'] * density_wave


def derivative_checks(event, potential, gas, stats, checks, prefix, frozen):
    photon_wave = [mp.mpf(index + 2) / 9 for index in range(len(potential))]
    gas_wave = mp.mpf('.03')
    velocity_wave = list(map(mp.mpf, ('.02', '-.01', '.015')))
    density_wave = mp.mpf('.04')
    step = mp.mpf(frozen['derivative_step'])
    background_step = mp.mpf(frozen['mixed_background_step'])
    def displaced(amplitude, wave):
        return raw_flux(event, [amplitude * value + wave * change for value, change in zip(potential, photon_wave)],
            amplitude * gas + wave * gas_wave, [wave * value for value in velocity_wave], wave * density_wave)
    numeric = (displaced(1, step) - displaced(1, -step)) / (2 * step)
    predicted = scalar_product(stats['exact'], photon_wave, gas_wave, velocity_wave, density_wave)
    check(checks, prefix + ':direct nonlinear derivative', abs(numeric - predicted) / max(abs(predicted), mp.mpf('1e-300')))
    mixed_numeric = (displaced(background_step, step) - displaced(background_step, -step)
        - displaced(-background_step, step) + displaced(-background_step, -step)) / (4 * step * background_step)
    mixed_predicted = scalar_product(stats['mixed'], photon_wave, gas_wave, velocity_wave, density_wave)
    check(checks, prefix + ':direct mixed nonlinear derivative', abs(mixed_numeric - mixed_predicted) / max(abs(mixed_predicted), mp.mpf('1e-300')))
    return float(abs(mixed_predicted / predicted))


def rotation_check(event, tests, features, coefficients, degree, frozen):
    block, density, left, right = projected(event, tests, features, coefficients, degree)
    directions = np.array(event['directions'])
    initial = np.array(event['electron_initial'])
    transfer = np.array(event['electron_transfer']) / event['temperature']
    integrated = np.zeros_like(block)
    axes, weights = np.polynomial.legendre.leggauss(frozen['projection_order'])
    for axis, weight in zip(axes, weights):
        for azimuth_index in range(2 * frozen['projection_order']):
            azimuth = np.pi * (azimuth_index + .5) / frozen['projection_order']
            axis_vector = np.array([np.sqrt(1 - axis**2) * np.cos(azimuth), np.sqrt(1 - axis**2) * np.sin(azimuth), axis])
            cosine = directions @ axis_vector
            legendre = np.ones(len(cosine)) if degree == 0 else cosine if degree == 1 else (3 * cosine**2 - 1) / 2
            output = (np.array(event['signs']) * legendre) @ tests
            input_values = (np.array(list(map(float, coefficients['photon']))) * legendre) @ features
            gas_left = transfer[0] if degree == 0 else transfer[1:] @ axis_vector if degree == 1 else 0.
            gas_right = float(coefficients['gas']) if degree == 0 else np.array(list(map(float, coefficients['velocity']))) @ axis_vector if degree == 1 else 0.
            integrated += weight / (4 * frozen['projection_order']) * np.outer(np.r_[output, gas_left], np.r_[input_values, gas_right])
    return relative(integrated, block)


def run_anchor(label):
    modest()
    config, frozen = run_protocol()
    path = ROOT / 'runs' / label / 'status.json'
    assert not path.exists()
    began = time.monotonic()
    original, features, models = setup(config)
    row = next(row for row in config['events'] if row['label'] == label)
    parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
    assert weight == row['weight'] and digest(row['loop_path']) == row['loop_sha256']
    loop = read(row['loop_path'])
    assert loop['identity'] == source.physics.event_owner.inherited.virtual_identity(parameters)
    checks, records, arrays = [], [], {}
    tests_owner = models[0]['difference'].tests
    with mp.workdps(80):
        vacuum = angular.inherited.vacuum.finite_virtual_ratio(mp.mpf(str(parameters['energy'])), mp.mpf(str(parameters['cosine'])))
        vacuum += angular.inherited.vacuum.soft_constant(mp.mpf(str(parameters['energy'])), mp.mpf(str(parameters['cosine'])))
        virtual_coefficient = float((vacuum + scalar(loop['scalar'])) / 2)
        for event_index, (tag, event) in enumerate(selected_events(parameters, config)):
            frequencies = np.array(event['frequencies'])
            tests = tests_owner.evaluate(frequencies)
            photon_transfer = np.array(event['signs']) @ np.array(event['photons'])
            electron_transfer = np.array(event['electron_transfer'])
            check(checks, tag + ':independent four momentum', np.linalg.norm(photon_transfer + electron_transfer) / event['temperature'])
            for join in config['joins']:
                feature_values = features.evaluate(frequencies, join)
                feature_slopes = features.evaluate(frequencies, join, True)
                for state_index, state in enumerate(config['states']):
                    coefficients = list(map(mp.mpf, state['coefficients']))
                    heat = scalar(config['heat'])
                    potential = [heat * mp.fsum(scalar(value) * coefficient for value, coefficient in zip(values, coefficients[:98])) for values in feature_values]
                    derivative = [heat * mp.fsum(scalar(value) * coefficient for value, coefficient in zip(values, coefficients[:98])) for values in feature_slopes]
                    gas = heat * coefficients[98]
                    stats = statistics(event, potential, gas)
                    prefix = f'{tag}:{join}:{state["model"]}:{state["history"]}'
                    maximum_derivative = derivative_checks(event, potential, gas, stats, checks, prefix, frozen)
                    ratio = mp.sqrt(mp.fsum(value**2 for value in vector(stats['remainder']))) / max(mp.sqrt(mp.fsum(value**2 for value in vector(stats['mixed']))), mp.mpf('1e-300'))
                    photon_boost = [scalar(frequency) * (1 + (1 + 2 * occupation) * value - slope)
                        for frequency, occupation, value, slope in zip(frequencies, stats['occupations'], potential, derivative)]
                    boost_vector = [mp.fsum(coefficient * boost * scalar(direction[axis]) for coefficient, boost, direction in zip(stats['exact']['photon'], photon_boost, event['directions']))
                        + stats['exact']['velocity'][axis] for axis in range(3)]
                    for degree in config['multipoles']:
                        built = {}
                        for part in ('equilibrium', 'mixed', 'remainder'):
                            matrix, density, left, right = projected(event, tests, feature_values, stats[part], degree)
                            built[part] = matrix
                            arrays[f'event{event_index}-join{join}-state{state_index}-l{degree}-{part}'] = matrix
                            if degree == 0:
                                arrays[f'event{event_index}-join{join}-state{state_index}-density-{part}'] = density
                            if degree <= 1:
                                pairing = np.linalg.norm(matrix[0] + matrix[-1]) / max(np.linalg.norm(matrix[0]) + np.linalg.norm(matrix[-1]), 1e-300)
                                check(checks, prefix + f':l{degree}:{part}:independent gas pairing', pairing)
                            if state['history'] == 'quarter' and event_index in (0, 1, 4):
                                check(checks, prefix + f':l{degree}:{part}:sphere average', rotation_check(event, tests, feature_values, stats[part], degree, frozen))
                        if tag == 'born':
                            arrays[f'join{join}-state{state_index}-l{degree}-virtual-statistical-mixed'] = weight * virtual_coefficient * built['mixed']
                        if degree == 1:
                            common = np.r_[original.basis.mean * original.basis.norms[0], original.basis.norms[1], np.zeros(96), 1.]
                            check(checks, prefix + ':equilibrium common boost', np.linalg.norm(built['equilibrium'] @ common) / max(np.linalg.norm(built['equilibrium']), 1e-300))
                    records.append(dict(event=tag, join=join, model=state['model'], history=state['history'],
                        physical_gas_shift=float(gas), maximum_photon_potential=float(max(map(abs, potential))),
                        mixed_fraction_in_test_direction=maximum_derivative, nonlinear_remainder_over_mixed=float(ratio),
                        non_equilibrium_common_boost_norm=float(mp.sqrt(mp.fsum(value**2 for value in boost_vector))),
                        signed_normalized_flux=float(stats['exact']['density'])))
            if tag == 'born':
                legacy_left, legacy_right = models[0]['difference'].born_jumps(parameters)
                zero = statistics(event, [mp.mpf(0)] * 2, mp.mpf(0))
                for join in config['joins']:
                    matrix, unused, unused, unused = projected(event, tests, features.evaluate(frequencies, join), zero['exact'], 0)
                    retained = list(range(96)) + [98]
                    old = -np.outer(legacy_left, legacy_right[join::2][:-1])
                    check(checks, f'born:l0:join{join}:production equilibrium vertex', relative(matrix[:, retained], old))
            print(json.dumps(dict(anchor=label, event=tag, events_complete=event_index + 1, failed=sum(not row['passed'] for row in checks))), flush=True)
    save(ROOT / 'runs' / label / 'vertices.npz', **arrays)
    failed = [row for row in checks if not row['passed']]
    report = dict(stage=233, state='complete', label=label, checks=checks, failed=failed, qualified=not failed,
        records=records, elapsed_seconds=time.monotonic() - began, finished_at=now(),
        vertices_sha256=digest(ROOT / 'runs' / label / 'vertices.npz'), events=event_index + 1,
        virtual_scalar=loop['scalar'], virtual_factor_includes_event_weight=True, new_virtual_integrals=0,
        scope='Full finite-basis statistical vertex and its mixed derivative, not an integrated inclusive source')
    write(path, report)
    print(json.dumps(dict(label=label, checks=len(checks), failed=failed, elapsed=report['elapsed_seconds'])), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'replay', 'warm', 'middle', 'cold'])
    arguments = parser.parse_args()
    modest()
    if arguments.mode == 'freeze':
        freeze()
    elif arguments.mode == 'replay':
        replay()
    else:
        run_anchor(arguments.mode)
