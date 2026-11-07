from history242 import *
import target242


def exact_vectors(config, records):
    high, low, states_high, states_low = [], [], [], []
    with mp.workdps(80):
        for state in config['states']:
            record = next(row for row in records if row['model'] == state['model'] and row.get('history') == state['history'] and 'rhs' in row)
            vector = [mp.mpf(config['heat']) * mp.mpf(value) for value in record['coefficient_tangent']]
            values = np.array(list(map(float, vector)))
            high.append(values)
            low.append(np.array([float(value - mp.mpf(float(part))) for value, part in zip(vector, values)]))
            original = [mp.mpf(config['heat']) * mp.mpf(value) for value in state['coefficients']]
            first = np.array(list(map(float, original)))
            states_high.append(first)
            states_low.append(np.array([float(value - mp.mpf(float(part))) for value, part in zip(original, first)]))
    return np.array(high).T, np.array(low).T, np.array(states_high).T, np.array(states_low).T


def contract(config, matrices, history):
    high, low, background_high, background_low = exact_vectors(config, history['records'])
    output = {}
    for order in (4, 6):
        for join in (0, 1):
            for index, state in enumerate(config['states']):
                stem = f'angular{order}:join{join}:{state["model"]}:{state["history"]}'
                for component in target242.assessment.COMPONENTS:
                    matrix = matrices[stem + ':l0:' + component]
                    output[stem + ':history_tangent:' + component] = precise.stable_dot(matrix, high[:, index:index + 1], low[:, index:index + 1])[:, 0]
                    output[stem + ':C2:' + component] = precise.stable_dot(matrix, background_high[:, index:index + 1], background_low[:, index:index + 1])[:, 0] / 2
    return output


def freeze():
    modest()
    config = protocol()
    assert not (ROOT / 'prediction/configuration.json').exists()
    history = read(ROOT / 'results/history.json')
    assert history['qualified']
    checks, inputs, fields = [], {}, []
    old = read(register(inputs, HISTORY / 'configuration.json'))
    weights = old['operator_weights']
    assert weights == [.375, .75, -.125]
    for anchor in ('warm', 'middle', 'cold'):
        path = SOURCE / 'results' / f'{anchor}-three-hard-angle-sum.npz'
        metadata = read(register(inputs, SOURCE / 'results' / f'{anchor}-assessment.json'))
        assert metadata['qualified']
        fields.append(contract(config, packet(register(inputs, path, metadata['output_sha256'])), history))
    prediction = {key: np.sum(np.stack([weight * field[key] for weight, field in zip(weights, fields)]), axis=0) for key in fields[0]}
    path = ROOT / 'prediction/target-prediction.npz'
    save(path, **prediction)
    write(ROOT / 'prediction/configuration.json', dict(frozen_at=now(), script_sha256=digest(__file__),
        source_prediction_tolerance=old['source_prediction_tolerance'], weights=weights,
        target_fraction=config['target_fraction'], output_sha256=digest(path), consumed_inputs=inputs,
        history_sha256=digest(ROOT / 'results/history.json'),
        method='Fixed earlier Stage209 quadratic operator weights, same actual target histories and RHS for every anchor',
        direct_target_outputs_read=False, prediction_is_not_an_operator_derivative=True))
    print(dict(frozen_predictor=True, fields=len(prediction)), flush=True)


def assess():
    modest()
    config = protocol()
    frozen = read(ROOT / 'prediction/configuration.json')
    assert frozen['script_sha256'] == digest(__file__)
    assert frozen['history_sha256'] == digest(ROOT / 'results/history.json')
    assert frozen['output_sha256'] == digest(ROOT / 'prediction/target-prediction.npz')
    report = read(ROOT / 'target/results/assessment.json')
    assert report['qualified']
    path = ROOT / 'target/results/three-hard-angle-sum.npz'
    assert digest(path) == report['output_sha256']
    history = read(ROOT / 'results/history.json')
    actual = contract(config, packet(path), history)
    predicted = packet(ROOT / 'prediction/target-prediction.npz')
    checks, records = [], []
    for key, value in actual.items():
        force_scale = max(abs(value[0]) + abs(value[-1]), 1e-300)
        check(checks, key + ':independent photon gas exchange', abs(value[0] + value[-1]) / force_scale)
        if key.startswith('angular4:'):
            better = actual[key.replace('angular4:', 'angular6:', 1)]
            for part, selection in [('all', slice(None)), ('shape', slice(1, -1)), ('gas', slice(-1, None))]:
                error = target242.retained.relative(value[selection], better[selection])
                check(checks, key + ':angular refinement:' + part, error, config['refinement_tolerance'])
        if ':half:' in key:
            quarter = actual[key.replace(':half:', ':quarter:')]
            for part, selection in [('all', slice(None)), ('shape', slice(1, -1)), ('gas', slice(-1, None))]:
                error = target242.retained.relative(value[selection], quarter[selection])
                check(checks, key + ':history mesh:' + part, error, config['history_mesh_tolerance'])
        prediction_error = target242.retained.relative(predicted[key], value)
        gas_error = abs(predicted[key][-1] - value[-1]) / max(abs(value[-1]), 1e-300)
        check(checks, key + ':frozen temperature prediction', prediction_error, frozen['source_prediction_tolerance'])
        check(checks, key + ':frozen gas prediction', gas_error, frozen['source_prediction_tolerance'])
        records.append(dict(name=key, vector_norm=float(np.linalg.norm(value)), photon_energy=float(value[0]),
            gas=float(value[-1]), prediction_error=prediction_error, gas_prediction_error=float(gas_error)))
    output = ROOT / 'results/target-history-source.npz'
    save(output, **actual)
    failures = [entry for entry in checks if not entry['passed']]
    write(ROOT / 'results/source-history.json', dict(qualified=not failures, checks=checks, failed=failures,
        records=records, output_sha256=digest(output), finished_at=now(),
        source_scope='Actual target-temperature C2 and J_B B_u on Stage240 three-angle x14 support',
        tail_shape_derivative_included=False, explicit_operator_derivative_included=False,
        full_time_derivative_claimed=False, fixed_gates=True))
    print(dict(source_history_checks=len(checks), failed=len(failures), first_failures=failures[:5]), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['freeze', 'assess'])
    arguments = parser.parse_args()
    freeze() if arguments.phase == 'freeze' else assess()
