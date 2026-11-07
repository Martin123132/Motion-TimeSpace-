from collision_stage185 import *


def relative(predicted, measured):
    denominator = float(np.linalg.norm(measured))
    assert denominator > 0
    return float(np.linalg.norm(predicted - measured) / denominator)


def load_calculation():
    pending = [index for index in range(len(all_offsets())) if not (ROOT / 'targets' / f'target-{index}' / 'status.json').exists()]
    if pending:
        raise RuntimeError(f'Physical target evaluations must finish before analysis; pending targets: {pending}')
    with np.load(ROOT / 'results/frozen-tangent.npz') as packet:
        anchor, tangent = packet['block'].copy(), packet['derivative'].copy()
    targets = []
    for index in range(len(all_offsets())):
        folder = ROOT / 'targets' / f'target-{index}'
        status = read(folder / 'status.json')
        assert status['matrix_sha256'] == saved.digest(folder / 'matrices.npz')
        assert status['frozen_tangent_sha256'] == saved.digest(ROOT / 'results/frozen-tangent.npz')
        with np.load(folder / 'matrices.npz') as packet:
            targets.append(dict(status=status, **{key: packet[key].copy() for key in packet.files}))
    return anchor, tangent, targets


def matrices():
    anchor, tangent, targets = load_calculation()
    ladder, basis, theta = setup()
    checks = list(read(ROOT / 'results/frozen-tangent.json')['checks'])
    prediction_rows, derivative_rows, negatives, secants = [], [], [], []
    for target in targets:
        offset = float(target['offset'])
        for kind in ['block', 'fixed_mask']:
            delta = target[kind] - anchor
            error = relative(offset * tangent, delta)
            check(checks, f'{offset}:{kind}: frozen small-change matrix prediction', error, .01, 'prediction')
            prediction_rows.append(dict(offset=offset, kind=kind, change_norm=float(np.linalg.norm(delta)),
                prediction_relative_error=error, passed=error <= .01, tolerance=.01))
            zero_error = relative(np.zeros_like(delta), delta)
            assert zero_error > .01
            negatives.append(dict(offset=offset, kind=kind, test='zero temperature derivative', relative_error=zero_error, rejected=True))
        boundary_ratio = float(np.linalg.norm(target['boundary']) / np.linalg.norm(target['block'] - anchor))
        check(checks, f'{offset}: moving-mask contribution to small change', boundary_ratio, .01, 'domain')
        check(checks, f'{offset}: explicit boundary split',
            relative(target['fixed_mask'] + target['boundary'], target['block']))
        check(checks, f'{offset}: matrix symmetry', relative(target['block'].T, target['block']))
        check(checks, f'{offset}: number null', np.linalg.norm(target['block'] @ basis.chemical) / (np.linalg.norm(target['block']) * np.linalg.norm(basis.chemical)))
        largest = float(linear.eigh(target['block'], basis.mass, eigvals_only=True)[-1])
        check(checks, f'{offset}: nonpositive collision matrix', max(0., largest) / np.linalg.norm(target['block']))
        target['status']['boundary_over_small_change_norm'] = boundary_ratio
    for first_index in range(0, len(targets), 2):
        step = float(targets[first_index]['offset'])
        plus, minus = targets[first_index:first_index + 2]
        for kind in ['block', 'fixed_mask']:
            forward, backward = (plus[kind] - anchor) / step, (anchor - minus[kind]) / step
            centered = (plus[kind] - minus[kind]) / (2 * step)
            error = relative(tangent, centered)
            gap = relative(forward, backward)
            check(checks, f'{step}:{kind}: centered physical matrix derivative', error, .01, 'derivative')
            check(checks, f'{step}:{kind}: nearby one-sided derivative agreement', gap, .01, 'nearby_sides')
            derivative_rows.append(dict(step=step, kind=kind, derivative_error=error, one_sided_gap=gap,
                derivative_passed=error <= .01, sides_passed=gap <= .01))
    for label, numerator, denominator in [('cool', ladder.blocks[1] - ladder.blocks[0], ladder.temperatures[1] - ladder.temperatures[0]),
        ('warm', ladder.blocks[2] - ladder.blocks[1], ladder.temperatures[2] - ladder.temperatures[1])]:
        secant = theta * numerator / denominator
        error = relative(secant, tangent)
        check(checks, label + ': old bank secant versus physical tangent matrix', error, .01, 'old_secant')
        secants.append(dict(side=label, relative_error=error, passed=error <= .01, physical_tangent_norm=float(np.linalg.norm(tangent)), secant_norm=float(np.linalg.norm(secant))))
    write(ROOT / 'results/matrix-analysis.json', dict(predictions=prediction_rows, derivatives=derivative_rows,
        target_metadata=[target['status'] for target in targets], old_secants=secants, negative_controls=negatives, checks=checks))
    write(ROOT / 'progress.json', dict(state='matrix_analysis_complete'))
    print(json.dumps(dict(predictions=prediction_rows, derivatives=derivative_rows, secants=secants,
        crossings=[target['status']['crossings'] for target in targets], failed=[row for row in checks if not row['passed']])), flush=True)


def gas_projection():
    assert read(ROOT / 'progress.json')['state'] == 'matrix_analysis_complete'
    anchor, tangent, targets = load_calculation()
    ladder, basis, theta = setup()
    checks, results = [], []
    scalars = np.empty((2, 3))
    with mp.workdps(80):
        mass = prior.mp_matrix(basis.mass)
        dual = mp.lu_solve(mass.T, prior.mp_vector(basis.energy)).T
        template = prior.mp_vector(basis.temperature)
        for model_index, model in enumerate(MODELS):
            operator = prior.Operators(model, ladder)
            history = prior.history(model, 'quarter')
            target = float(history['coordinates'][0])
            profile = prior.mp_vector(np.array([np.interp(target, history['expansion'], history['profiles'][:, index]) for index in range(96)]))
            stiffness = prior.mp_matrix(operator.at(target)[0])
            heat = mp.mpf(operator.background.chi)
            capacity = heat - (dual * stiffness * template)[0]
            equilibrium = -(1 + (dual * stiffness * profile)[0]) / capacity
            departure = profile - template * equilibrium
            local = operator.background.at(target)
            rate = mp.mpf(local['coefficient'] / local['thermal_parameter'])
            def project(matrix):
                return (rate * dual * prior.mp_matrix(matrix) * departure)[0] / capacity
            projection = project(tangent)
            old_cool, old_warm = project(theta * operator.low), project(theta * operator.high)
            scalars[model_index] = [float(projection), float(old_cool), float(old_warm)]
            old_frozen = read(PARENT / 'results/frozen-predictions.json')
            old_jump = mp.mpf(next(row for row in old_frozen['records'] if row['model'] == model and row['digits'] == 100)['probes'][0]['slaved_slope_jump'])
            check(checks, model + ': old secant projection reproduces Stage184 jump', (old_cool - old_warm - old_jump) / old_jump)
            rows = []
            for packet in targets:
                offset = float(packet['offset'])
                values = {}
                for kind in ['block', 'fixed_mask']:
                    actual = project(packet[kind] - anchor)
                    predicted = mp.mpf(offset) * projection
                    error = float(abs(predicted - actual) / abs(actual))
                    check(checks, f'{model}:{offset}:{kind}: gas small-change prediction', error, .01, 'gas_prediction')
                    values[kind] = dict(change=str(actual), predicted=str(predicted), relative_error=error, passed=error <= .01)
                boundary = project(packet['boundary'])
                rows.append(dict(offset=offset, values=values, boundary_projection=str(boundary), crossings=packet['status']['crossings']))
            centered = []
            for first_index in range(0, len(targets), 2):
                step = float(targets[first_index]['offset'])
                for kind in ['block', 'fixed_mask']:
                    observed = project((targets[first_index][kind] - targets[first_index + 1][kind]) / (2 * step))
                    error = float(abs(projection - observed) / abs(observed))
                    check(checks, f'{model}:{step}:{kind}: gas centered derivative', error, .01, 'gas_derivative')
                    centered.append(dict(step=step, kind=kind, observed=str(observed), error=error, passed=error <= .01))
            old_errors = {}
            for label, value in [('cool', old_cool), ('warm', old_warm)]:
                error = float(abs(value - projection) / abs(projection))
                old_errors[label] = error
                check(checks, model + ':' + label + ': old secant gas projection', error, .01, 'old_secant_gas')
            results.append(dict(model=model, physical_collision_gas_slope=str(projection), cool_secant=str(old_cool),
                warm_secant=str(old_warm), old_relative_errors=old_errors, capacity=str(capacity), equilibrium=str(equilibrium),
                predictions=rows, centered=centered))
    write(ROOT / 'results/gas-projection.json', dict(results=results, checks=checks,
        scope='Collision-temperature contribution to the local slaved gas u-slope, not its full derivative or curvature'))
    np.savez_compressed(ROOT / 'results/gas-slopes.npz', values=scalars, labels=np.array(['physical', 'cool_secant', 'warm_secant']), models=np.array(MODELS))
    write(ROOT / 'progress.json', dict(state='gas_projection_complete'))
    print(json.dumps(dict(results=results, failed=[row for row in checks if not row['passed']])), flush=True)


def responses():
    assert read(ROOT / 'progress.json')['state'] == 'gas_projection_complete'
    config = read(prior.PARENT / 'configuration.json')
    paths = read(ROOT / 'authenticated-inputs.json')
    kernel_path = PARENT / 'results/gas-response.npz'
    with np.load(kernel_path) as packet:
        kernels, components = packet['kernels'].copy(), list(packet['components'])
    with np.load(source.ROOT / 'results/preparation/basis.npz') as packet:
        factor = linear.cholesky(packet['mass'], lower=True)
    def norm(values):
        reshaped = np.moveaxis(values[..., 1:97, :], -2, 0).reshape(96, -1)
        return np.linalg.norm(linear.solve_triangular(factor, reshaped, lower=True), axis=0).reshape(values.shape[:-2] + (values.shape[-1],))
    checks, event_pairs = [], []
    consumed = {str(kernel_path): saved.digest(kernel_path)}
    for node in config['selected']:
        path = prior.HALF / 'gas-events' / saved.angle_label(node['cosine']) / f"electron-{node['electron_index']:02d}.npz"
        assert paths[str(path)] == saved.digest(path)
        with np.load(path) as packet:
            assert json.loads(str(packet['node'])) == node
            event_pairs.append((packet['high'][1].copy(), packet['low'][1].copy()))
        consumed[str(path)] = saved.digest(path)
    reconstructed = np.empty_like(kernels)
    with mp.workdps(80):
        for index in np.ndindex(kernels.shape):
            reconstructed[index] = float(mp.fsum(mp.mpf(float(high[index])) + mp.mpf(float(low[index])) for high, low in event_pairs))
    assert np.array_equal(reconstructed, kernels)
    check(checks, '36 saved gas events reproduce previous summed kernels bitwise', 0)
    with np.load(ROOT / 'results/gas-slopes.npz') as packet:
        scalars = packet['values'].copy()
    response = np.empty((3, 6, 98, 4))
    for label, component, column in np.ndindex(3, 6, 4):
        response[label, component, :, column] = kernels[component, :, column] * scalars[column // 2, label]
    projection = read(ROOT / 'results/gas-projection.json')['results']
    rows = []
    for component in [0, 4, 5]:
        norms = norm(response[:, component])
        for column in range(4):
            model_index = column // 2
            for predicted in projection[model_index]['predictions']:
                for kind in ['block', 'fixed_mask']:
                    record = predicted['values'][kind]
                    actual = float(record['change']) * kernels[component, :, column]
                    test = float(record['predicted']) * kernels[component, :, column]
                    actual_norm = float(np.linalg.norm(linear.solve_triangular(factor, actual[1:97], lower=True)))
                    test_norm = float(np.linalg.norm(linear.solve_triangular(factor, test[1:97], lower=True)))
                    error = float(np.linalg.norm(linear.solve_triangular(factor, (actual - test)[1:97], lower=True)) / actual_norm)
                    check(checks, f'{components[component]}:{column}:{predicted["offset"]}:{kind}: source derivative prediction', error, .01, 'source_prediction')
                    check(checks, f'{components[component]}:{column}:{predicted["offset"]}:{kind}: gas/source fractional agreement', error - record['relative_error'])
                    rows.append(dict(component=components[component], column=column, model=MODELS[model_index], offset=predicted['offset'],
                        kind=kind, change_norm=actual_norm, prediction_norm=test_norm, relative_error=error, passed=error <= .01,
                        physical_tangent_response_norm=float(norms[0, column]), cool_secant_response_norm=float(norms[1, column]), warm_secant_response_norm=float(norms[2, column])))
    for component in range(6):
        scale = np.maximum(np.maximum(abs(kernels[component, 0]), abs(kernels[component, -1])), 1e-300)
        check(checks, str(components[component]) + ': cached energy cancellation', np.max(abs(kernels[component, 0] + kernels[component, -1]) / scale))
    check(checks, 'matched response closure', np.max(norm(kernels[4] - kernels[1] - kernels[2] - kernels[3]) / norm(kernels[4])))
    check(checks, 'total response closure', np.max(norm(kernels[5] - kernels[0] - kernels[4]) / norm(kernels[5])))
    write(ROOT / 'results/source-comparisons.json', dict(rows=rows, checks=checks, reused_events=36, new_source_events=0))
    write(ROOT / 'response-inputs.json', consumed)
    np.savez_compressed(ROOT / 'results/gas-responses.npz', kernels=kernels, response=response, components=np.array(components))
    write(ROOT / 'progress.json', dict(state='response_complete'))
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
        max_relative_error=max(row['relative_error'] for row in rows))), flush=True)


if __name__ == '__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['matrices', 'gas', 'responses'])
    arguments = parser.parse_args()
    dict(matrices=matrices, gas=gas_projection, responses=responses)[arguments.phase]()
