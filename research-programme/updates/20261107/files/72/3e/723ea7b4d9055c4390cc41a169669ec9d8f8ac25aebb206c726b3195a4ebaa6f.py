from common234 import *
import radial234
import argparse


def compensated(values):
    high = np.array([complex(value) for value in values], dtype=complex)
    low = np.array([complex(value - mp.mpc(upper)) for value, upper in zip(values, high)], dtype=complex)
    return high, low


def response_tensor(config, row, report, radial, anchor, exterior=False):
    coordinates = 1 if exterior else 99
    rays = []
    for ray_index, ray in enumerate(report['rays']):
        matrix = []
        if exterior:
            constants = [radial234.thermal_exterior(*config['spectral_domain'])]
            pole_values = [[radial234.thermal_exterior(*config['spectral_domain'], radial['locations'][anchor, ray_index, pole_index])]
                for pole_index in range(2)]
        else:
            constants = [scalar(value) for value in radial['constant']]
            pole_values = [[mp.mpc(value) for value in radial['poles'][anchor, ray_index, pole_index]] for pole_index in range(2)]
        local_temperature = mp.mpf(str(row['theta'])) / mp.mpf(ray['doppler'])
        factor = mp.mpf(report['prefactor']) * scalar(ray['weight'])
        for index in range(coordinates):
            entry = []
            for polarization in ray['polarizations']:
                constant = matrix_value(polarization['constant'])
                poles = [matrix_value(pole['coefficient']) for pole in polarization['poles']]
                block = factor * (constant * local_temperature**2 * constants[index]
                    + sum((pole * values[index] for pole, values in zip(poles, pole_values)), mp.zeros(2)))
                entry.extend(list(block))
            matrix.append(entry)
        rays.append(matrix)
    features = np.column_stack([np.ones(8), np.array([ray['lab_direction'] for ray in report['rays']]),
        angular.angular_feature(np.array([ray['lab_direction'] for ray in report['rays']]), 2)])
    rest_features = np.column_stack([np.ones(8), np.array([[float(value) for value in ray['rest_direction']] for ray in report['rays']]),
        angular.angular_feature(np.array([[float(value) for value in ray['rest_direction']] for ray in report['rays']]), 2)])
    flat, wrong_frame = [], []
    for coordinate in range(coordinates):
        for feature in range(13):
            for entry in range(16):
                flat.append(mp.fsum(scalar(features[ray, feature]) * rays[ray][coordinate][entry] for ray in range(8)))
                wrong_frame.append(mp.fsum(scalar(rest_features[ray, feature]) * rays[ray][coordinate][entry] for ray in range(8)))
    high, low = compensated(flat)
    wrong_high, wrong_low = compensated(wrong_frame)
    shape = (coordinates, 13, 2, 2, 2, 2)
    return high.reshape(shape), low.reshape(shape), wrong_high.reshape(shape), wrong_low.reshape(shape)


def mueller_response(tree, high, low, parameters):
    normalization = angular.inherited.source.mueller(tree)[0, 0]
    rest = np.empty(high.shape[:2] + (4, 4))
    for index, feature in np.ndindex(high.shape[:2]):
        rest[index, feature] = (angular.inherited.source.interference(tree, high[index, feature])
            + angular.inherited.source.interference(tree, low[index, feature])) / normalization
    return np.einsum('ab,nkbc,dc->nkad', parameters['outgoing_stokes'], rest, parameters['incoming_stokes'])


def freeze():
    config = protocol()
    assert not (ROOT / 'assembly-configuration.json').exists()
    inputs = {}
    for path in (ROOT / 'radial').glob('*'):
        if path.suffix in ('.npz', '.json'):
            inputs[str(path)] = digest(path)
    for row in config['events']:
        for suffix in ('.json', '.npz'):
            path = ROOT / 'tensors' / (row['label'] + suffix)
            inputs[str(path)] = digest(path)
    assert read(ROOT / 'results/radial-assessment.json')['qualified']
    write(ROOT / 'assembly-configuration.json', dict(frozen_at=now(), inputs=inputs,
        script_sha256=digest(Path(__file__)), representation_tolerance=1e-10,
        refinement_tolerance=.002, full_spectral_domain=False, orders=config['radial_orders']))


def protocol_assembly():
    config = protocol()
    frozen = read(ROOT / 'assembly-configuration.json')
    assert digest(Path(__file__)) == frozen['script_sha256']
    for path, expected in frozen['inputs'].items():
        assert digest(path) == expected, path
    return config, frozen


def build():
    modest()
    config, frozen = protocol_assembly()
    for anchor, row in enumerate(config['events']):
        report = read(ROOT / 'tensors' / (row['label'] + '.json'))
        saved = packet(ROOT / 'tensors' / (row['label'] + '.npz'))
        parameters, unused = source.physics.parameters_and_weight(row['theta'], row['node'])
        for join in config['joins']:
            for order in config['radial_orders']:
                output = ROOT / 'response' / f'{row["label"]}-join{join}-order{order}.npz'
                if output.exists():
                    previous = read(output.with_suffix('.json'))
                    assert previous['qualified'] and digest(output) == previous['sha256']
                    continue
                began = time.monotonic()
                checks = []
                radial = packet(ROOT / 'radial' / f'join{join}-order{order}.npz')
                with mp.workdps(80):
                    high, low, wrong_high, wrong_low = response_tensor(config, row, report, radial, anchor)
                    outside_high, outside_low, unused, unused = response_tensor(config, row, report, radial, anchor, exterior=True)
                response = mueller_response(saved['tree'], high, low, parameters)
                wrong = mueller_response(saved['tree'], wrong_high, wrong_low, parameters)
                thermal_replay = high[-1, 0] + low[-1, 0] + outside_high[0, 0] + outside_low[0, 0]
                check(checks, 'thermal tensor control including its known exterior', relative(thermal_replay, saved['planck_temperature_derivative']))
                for degree, section in [(1, slice(1, 4)), (2, slice(4, 13))]:
                    wrong_error = relative(wrong[:98, section], response[:98, section])
                    check(checks, f'l{degree}:wrong rest frame rejected', int(wrong_error <= 1e-10), 0)
                save(output, high=high, low=low, mueller=response, wrong_frame_mueller=wrong,
                    thermal_control_exterior_high=outside_high, thermal_control_exterior_low=outside_low,
                    original_frequency_domain=np.array(config['spectral_domain']))
                failed = [entry for entry in checks if not entry['passed']]
                result = dict(state='complete', qualified=not failed, checks=checks, failed=failed,
                    seconds=time.monotonic() - began, sha256=digest(output), finished_at=now(),
                    physical_history_exterior_assumed=False, thermal_control_exterior_not_a_history_model=True)
                write(output.with_suffix('.json'), result)
                print(json.dumps(dict(anchor=row['label'], join=join, order=order, failed=failed, seconds=result['seconds'])), flush=True)
                assert not failed, failed


def contract_mp(values, coefficients):
    return mp.fsum(scalar(value) * coefficient for value, coefficient in zip(values, coefficients))


def blocks():
    modest()
    config, frozen = protocol_assembly()
    original, features, models = setup(config)
    checks, records, output = [], [], {}
    with mp.workdps(80):
        for row in config['events']:
            parameters, weight = source.physics.parameters_and_weight(row['theta'], row['node'])
            event = geometry(parameters)
            tests = models[0]['difference'].tests.evaluate(np.array(event['frequencies']))
            old = packet(PARENT / 'runs' / row['label'] / 'vertices.npz')
            for join in config['joins']:
                basis = features.evaluate(np.array(event['frequencies']), join)
                matrices = {order: packet(ROOT / 'response' / f'{row["label"]}-join{join}-order{order}.npz')['mueller'] for order in config['radial_orders']}
                for state_index, state in enumerate(config['states']):
                    coefficient = list(map(mp.mpf, state['coefficients']))
                    physical = [scalar(config['heat']) * value for value in coefficient]
                    potential = [contract_mp(line, physical[:98]) for line in basis]
                    stats = statistics(event, potential, physical[-1])
                    for degree, section in [(0, slice(0, 1)), (1, slice(1, 4)), (2, slice(4, 13))]:
                        reference, unused, left, unused = projected(event, tests, basis, stats['equilibrium'], degree)
                        statistical = old[f'join{join}-state{state_index}-l{degree}-virtual-statistical-mixed']
                        results = {}
                        for order, full in matrices.items():
                            scalar_map = full[:98, :, 0, 0]
                            background = float(contract_mp(scalar_map[:, 0], physical[:98]))
                            wave = np.vstack([scalar_map[:, section], np.zeros((1, scalar_map[:, section].shape[-1]))])
                            first = .5 * weight * background * reference
                            second = .5 * weight * float(stats['linear_source']) * (left @ wave.T) / (2 * degree + 1)
                            medium = first + second
                            total = statistical + medium
                            results[order] = (first, second, medium, total)
                            prefix = f'{row["label"]}:join{join}:{state["model"]}:{state["history"]}:l{degree}:order{order}'
                            if degree < 2:
                                for label, matrix in [('background_medium', first), ('wave_medium', second), ('virtual_mixed_sum', total)]:
                                    check(checks, prefix + ':' + label + ':independent gas force', np.linalg.norm(matrix[0] + matrix[-1]) / max(np.linalg.norm(matrix[0]) + np.linalg.norm(matrix[-1]), 1e-300))
                            for label, matrix in [('background', first), ('wave', second), ('medium', medium), ('total', total)]:
                                output[prefix + ':' + label] = matrix
                        for part, label in enumerate(('background', 'wave', 'medium', 'total')):
                            change = relative(results[4][part], results[6][part])
                            check(checks, prefix + ':' + label + ':4-to6 refinement', change, .002)
                        relative_wave = np.linalg.norm(results[6][1]) / max(np.linalg.norm(results[6][2]), 1e-300)
                        check(checks, prefix + ':omitted wave-medium term rejected', int(relative_wave <= 1e-10), 0)
                        check(checks, prefix + ':duplicate event weight rejected', int(abs(1 - weight) <= 1e-10), 0)
                        records.append(dict(anchor=row['label'], join=join, model=state['model'], history=state['history'], degree=degree,
                            background_delta_kappa=background, wave_term_over_medium=float(relative_wave),
                            medium_over_statistical=float(np.linalg.norm(results[6][2]) / max(np.linalg.norm(statistical), 1e-300)),
                            total_refinement=relative(results[4][3], results[6][3]),
                            maximum_medium_entry=float(np.max(abs(results[6][2])))))
    save(ROOT / 'results/virtual-mixed-blocks.npz', **output)
    failed = [entry for entry in checks if not entry['passed']]
    report = dict(state='complete', checks=checks, failed=failed, qualified=not failed, records=records,
        block_sha256=digest(ROOT / 'results/virtual-mixed-blocks.npz'), finished_at=now(),
        physical_exterior_terms='not supplied: explicit additional linear functionals', inclusive_source_complete=False,
        scope='Finite-domain photon-cut medium variation plus original statistical virtual variation; real/state assembly still separate')
    write(ROOT / 'results/virtual-mixed-assessment.json', report)
    print(json.dumps(dict(block_checks=len(checks), failed=failed, maximum_refinement=max(row['total_refinement'] for row in records),
        minimum_wave_fraction=min(row['wave_term_over_medium'] for row in records))), flush=True)
    assert not failed, failed


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'build', 'blocks'])
    args = parser.parse_args()
    modest()
    {'freeze': freeze, 'build': build, 'blocks': blocks}[args.mode]()
