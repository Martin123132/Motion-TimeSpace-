from common237 import *
import argparse


def freeze():
    config = protocol()
    path = ROOT / 'assessment-configuration.json'
    assert not path.exists()
    write(path, dict(frozen_at=now(), script_sha256=digest(__file__),
        configuration_sha256=digest(ROOT / 'configuration.json'),
        comparisons=[['original', '4'], ['4', '6'], ['6', '8'], ['original', '8']],
        components=['leading_control', 'real_correction', 'virtual', 'state', 'MTS_correction', 'combined'],
        angular_tolerance=config['angular_tolerance'], identity_tolerance=config['identity_tolerance'],
        final_accuracy_gate='6-to8 component and combined matrix/gas refinements; earlier differences retained separately',
        reference_accuracy_gate='original-to8 component and combined matrix/gas refinements',
        no_observational_claim=True))


def sum_real(anchor, order, config, inputs, checks):
    if order == 4:
        path = PARENT / 'results' / (anchor + '-assessment.npz')
        register(inputs, path)
        return {key.split(':', 1)[1]: value for key, value in packet(path).items() if key.startswith('order26:')}
    values, compensation = {}, {}
    count = len(list(angular.inherited.source.angular_nodes(order)))
    for index in range(count):
        path = ROOT / 'real' / anchor / f'angular{order}' / f'ray-{index:03d}.npz'
        report = read(path.with_suffix('.json'))
        assert report['anchor'] == anchor and report['angular_order'] == order and report['ray'] == index
        assert report['radial_order'] == config['radial_order']
        assert report['configuration_sha256'] == digest(ROOT / 'configuration.json')
        register(inputs, path, report['sha256'])
        register(inputs, path.with_suffix('.json'))
        check(checks, f'{anchor}:angular{order}:ray{index}:event four-force', report['maximum_independent_four_force_residual'])
        for name, value in packet(path).items():
            if name not in values:
                values[name] = np.zeros_like(value)
                compensation[name] = np.zeros_like(value)
            change = value - compensation[name]
            updated = values[name] + change
            compensation[name] = (updated - values[name]) - change
            values[name] = updated
    return values


def force_residual(matrix):
    return float(np.linalg.norm(matrix[0] + matrix[-1]) / max(np.linalg.norm(matrix[0]) + np.linalg.norm(matrix[-1]), 1e-300))


def comparison(first, second, degree):
    result = dict(matrix=relative(first, second), photon_shape=relative(first[1:-1], second[1:-1]),
        absolute_difference=float(np.linalg.norm(first - second)), reference_norm=float(np.linalg.norm(second)),
        maximum_entry_difference=float(np.max(abs(first - second))))
    if degree < 2:
        result['gas'] = relative(first[-1], second[-1])
    return result


def run(anchor):
    modest()
    config = protocol()
    frozen = read(ROOT / 'assessment-configuration.json')
    assert frozen['script_sha256'] == digest(__file__)
    assert frozen['configuration_sha256'] == digest(ROOT / 'configuration.json')
    target = ROOT / 'results' / (anchor + '-assessment.json')
    assert not target.exists()
    inputs, checks, records, output = {}, [], [], {}
    real = {order: sum_real(anchor, order, config, inputs, checks) for order in (4, 6, 8)}
    state_path = STATE / 'runs' / anchor / 'state.npz'
    register(inputs, state_path)
    state_blocks = packet(state_path)
    inherited = packet(PARENT / 'results' / (anchor + '-assessment.npz'))
    virtual = {}
    for order in (2, 4, 6, 8):
        for join in config['joins']:
            path = ROOT / 'virtual' / f'angular{order}' / f'{anchor}-join{join}.npz'
            metadata = read(path.with_suffix('.json'))
            assert metadata['qualified']
            assert metadata['script_sha256'] == digest(ROOT / 'virtual237.py')
            register(inputs, path, metadata['sha256'])
            register(inputs, path.with_suffix('.json'))
            virtual[order, join] = packet(path)
    for join in config['joins']:
        for degree in config['multipoles']:
            for state_index in range(7):
                if state_index == 0:
                    label, history = 'equilibrium', 'equilibrium'
                else:
                    state = config['states'][state_index - 1]
                    label, history = state['model'], state['history']
                matrices = {}
                for version in ('original', '4', '6', '8'):
                    real_order, virtual_order = (4, 2) if version == 'original' else (int(version), int(version))
                    leading = real[real_order][f'control:join{join}:l{degree}:total'][state_index]
                    correction = real[real_order][f'difference:join{join}:l{degree}:total'][state_index]
                    values = dict(leading_control=leading, real_correction=correction)
                    if state_index:
                        medium = virtual[virtual_order, join][f'state{state_index - 1}:l{degree}:total']
                        displaced = state_blocks[f'join{join}:state{state_index - 1}:l{degree}:step0.0005:total']
                        matched = correction + medium + displaced
                        values.update(virtual=medium, state=displaced, MTS_correction=matched, combined=leading + matched)
                        if version == 'original':
                            key = f'{anchor}:join{join}:{label}:{history}:l{degree}:finite_matched_fine'
                            check(checks, key + ':original combined replay', relative(matched, inherited[key]))
                    matrices[version] = values
                    for component, matrix in values.items():
                        key = f'angular{version}:join{join}:{label}:{history}:l{degree}:{component}'
                        output[key] = matrix
                        if degree < 2:
                            check(checks, key + ':integrated four-force', force_residual(matrix))
                for first, second in frozen['comparisons']:
                    for component in matrices[first]:
                        errors = comparison(matrices[first][component], matrices[second][component], degree)
                        record = dict(anchor=anchor, join=join, model=label, history=history, degree=degree,
                            component=component, comparison=first + '-to' + second, **errors)
                        record['passed'] = max(errors['matrix'], errors.get('gas', 0)) <= config['angular_tolerance']
                        records.append(record)
                if state_index:
                    for first, second in [('2', '4'), ('4', '6'), ('6', '8'), ('2', '8')]:
                        for part in ('statistical', 'background', 'wave'):
                            left = virtual[int(first), join][f'state{state_index - 1}:l{degree}:{part}']
                            right = virtual[int(second), join][f'state{state_index - 1}:l{degree}:{part}']
                            errors = comparison(left, right, degree)
                            records.append(dict(anchor=anchor, join=join, model=label, history=history, degree=degree,
                                component='virtual_' + part, comparison='virtual' + first + '-to' + second, **errors,
                                passed=max(errors['matrix'], errors.get('gas', 0)) <= config['angular_tolerance']))
    identities = all(entry['passed'] for entry in checks)
    final = [entry for entry in records if entry['comparison'] in ('6-to8', 'virtual6-to8')]
    original = [entry for entry in records if entry['comparison'] in ('original-to8', 'virtual2-to8')]
    final_pass = all(entry['passed'] for entry in final)
    original_pass = all(entry['passed'] for entry in original)
    save(target.with_suffix('.npz'), **output)
    result = dict(stage=237, state='complete', anchor=anchor, identities_pass=identities,
        final_angular_accuracy_pass=final_pass, original_angular_accuracy_pass=original_pass,
        qualified=identities and final_pass, checks=checks, failed_identities=[entry for entry in checks if not entry['passed']],
        records=records, final_accuracy_failures=[entry for entry in final if not entry['passed']],
        original_accuracy_failures=[entry for entry in original if not entry['passed']],
        maximum_final_change=max(max(entry['matrix'], entry.get('gas', 0)) for entry in final),
        maximum_original_change=max(max(entry['matrix'], entry.get('gas', 0)) for entry in original),
        directly_consumed_inputs=inputs, output_sha256=digest(target.with_suffix('.npz')),
        script_sha256=digest(__file__), finished_at=now(),
        scope='Same finite-domain x14/event0 collision source, three saved histories on each heavy/cold parent; l0/1/2. Equilibrium controls are real-sector only.',
        physical_exterior_supplied=False, polarized_soft_response_qualified=False, original_bank_changed=False)
    write(target, result)
    print(json.dumps({key: result[key] for key in ('anchor', 'identities_pass', 'final_angular_accuracy_pass',
        'original_angular_accuracy_pass', 'maximum_final_change', 'maximum_original_change')}), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'warm', 'middle', 'cold'])
    argument = parser.parse_args().mode
    freeze() if argument == 'freeze' else run(argument)
