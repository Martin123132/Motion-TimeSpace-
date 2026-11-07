from corner_stage184 import *


def curvature(samples):
    return prior.prior.curvature(samples)


def relative_error(prediction, measured):
    return float(abs(prediction - measured) / max(abs(measured), 1e-300))


def sampling_errors(coordinate, targets, second):
    errors, cells = [], []
    for target, derivative in zip(targets, second):
        right_index = int(np.searchsorted(coordinate, target))
        if coordinate[right_index] == target:
            errors.append(0.)
            cells.append(dict(target=float(target), on_node=True, fraction=0., error=0.))
            continue
        left, right = coordinate[right_index - 1:right_index + 1]
        error = .5 * derivative * (target - left) * (right - target)
        errors.append(float(error))
        cells.append(dict(target=float(target), on_node=False, left=float(left), right=float(right),
            fraction=float((target - left) / (right - left)), error=float(error)))
    return np.array(errors), cells


def analyse():
    assert read(ROOT / 'progress.json')['state'] == 'counterfactual_complete'
    frozen = read(ROOT / 'results/frozen-predictions.json')
    frozen_hash = saved.digest(ROOT / 'results/frozen-predictions.json')
    assert read(ROOT / 'progress.json')['frozen_prediction_sha256'] == frozen_hash
    config = read(ROOT / 'configuration.json')
    checks = list(frozen['checks'])
    predictions = {row['model']: row for row in frozen['records'] if row['digits'] == 100}
    previous = {row['model']: row for row in read(HALF / 'results/history-comparison.json')}
    current = {row['model']: row for row in read(PARENT / 'results/history-comparison.json')}
    attribution, sampling, diagnostics = [], [], []
    amplitudes = np.empty((2, 3, 5))
    labels = ['original', 'reference', 'forced_difference', 'leading_corner_prediction', 'sampling_corrected_original']
    for model_index, model in enumerate(MODELS):
        probes = predictions[model]['probes']
        prediction = float(probes[0]['corner_width_prediction'])
        second = np.array([float(probe['gas_second']) for probe in probes])
        sampling_curves = []
        for grid_index, grid in enumerate(GRIDS):
            packet = history(model, grid)
            folder = ROOT / 'counterfactuals' / model / grid
            status = read(folder / 'status.json')
            assert status['state'] == 'complete' and status['frozen_prediction_sha256'] == frozen_hash
            with np.load(folder / 'history.npz') as counter:
                assert np.array_equal(counter['expansion'], packet['expansion'])
                assert np.array_equal(counter['coordinates'], packet['coordinates'])
                reference = np.interp(packet['coordinates'], packet['expansion'], counter['reference_gas'])
                forced = np.interp(packet['coordinates'], packet['expansion'], counter['forced_gas'])
                assert np.isfinite(counter['reference_profiles']).all() and np.isfinite(counter['forced_profiles']).all()
            original = np.interp(packet['coordinates'], packet['expansion'], packet['temperature_scaled'])
            original_curve, reference_curve, forced_curve = [curvature(values) for values in [original, reference, forced]]
            for field in ['forced_equation_relative', 'forced_gas_balance', 'reconstruction_gas_absolute', 'reconstruction_profile_relative']:
                maximum = max(abs(row[field]) for row in status['diagnostics'])
                check(checks, f'{model}:{grid}: {field}', maximum)
                diagnostics.append(dict(model=model, grid=grid, quantity=field, maximum=maximum))
            errors, cells = sampling_errors(packet['expansion'], packet['coordinates'], second)
            sampling_curve = curvature(errors)
            sampling_curves.append(sampling_curve)
            corrected = original_curve - sampling_curve
            for quantity_index, quantity in enumerate(QUANTITIES):
                direct_difference = original_curve[quantity_index] - reference_curve[quantity_index]
                forced_difference = forced_curve[quantity_index]
                check(checks, f'{model}:{grid}:{quantity}: direct/forced small contribution',
                    relative_error(forced_difference, direct_difference), .01, 'source')
            prediction_error = relative_error(prediction, original_curve[2])
            forced_error = relative_error(prediction, forced_curve[2])
            corrected_error = relative_error(prediction, corrected[2])
            check(checks, f'{model}:{grid}: leading corner/raw width', prediction_error, .01, 'raw_corner_prediction')
            check(checks, f'{model}:{grid}: leading corner/forced width', forced_error, .01, 'source')
            check(checks, f'{model}:{grid}: leading corner/sampling-corrected width', corrected_error, .01, 'sampling_corrected_prediction')
            amplitudes[model_index, grid_index] = [original_curve[2], reference_curve[2], forced_curve[2], prediction, corrected[2]]
            attribution.append(dict(model=model, grid=grid, original=original_curve.tolist(), reference=reference_curve.tolist(),
                forced=forced_curve.tolist(), leading_corner_prediction=prediction, raw_relative_error=prediction_error,
                forced_relative_error=forced_error, sampling_curve=sampling_curve.tolist(), sampling_corrected=corrected.tolist(),
                corrected_relative_error=corrected_error, signed_attributed_fraction=float(forced_curve[2] / original_curve[2]),
                cells=cells, updates=status['updates']))
        for grid_index, comparison in enumerate([previous[model], current[model]], 1):
            predicted_change = sampling_curves[grid_index] - sampling_curves[grid_index - 1]
            for quantity_index, quantity in enumerate(QUANTITIES):
                measured = comparison['comparison'][quantity_index]['interpolation_change']
                predicted = float(predicted_change[quantity_index])
                error = relative_error(predicted, measured)
                check(checks, f'{model}:{GRIDS[grid_index - 1]}/{GRIDS[grid_index]}:{quantity}: equation-based sampling change', error, .01, 'sampling_prediction')
                sampling.append(dict(model=model, transition=f'{GRIDS[grid_index - 1]}/{GRIDS[grid_index]}', quantity=quantity,
                    predicted=predicted, measured=measured, relative_error=error, tolerance=.01, passed=error <= .01))
    write(ROOT / 'results/corner-attribution.json', attribution)
    write(ROOT / 'results/sampling-prediction.json', sampling)
    write(ROOT / 'results/counterfactual-diagnostics.json', diagnostics)
    np.savez_compressed(ROOT / 'results/gas-amplitudes.npz', models=np.array(MODELS), grids=np.array(GRIDS),
        labels=np.array(labels), amplitudes=amplitudes)
    write(ROOT / 'results/analysis-checks.json', dict(checks=checks))
    write(ROOT / 'progress.json', dict(state='attribution_complete', frozen_prediction_sha256=frozen_hash))
    print(json.dumps(dict(attribution=[{key: row[key] for key in ['model', 'grid', 'raw_relative_error', 'forced_relative_error',
        'corrected_relative_error', 'signed_attributed_fraction']} for row in attribution], sampling=sampling,
        failed=[row for row in checks if not row['passed']])), flush=True)


def response():
    assert read(ROOT / 'progress.json')['state'] == 'attribution_complete'
    paths = read(ROOT / 'authenticated-inputs.json')
    kernel_path = PARENT / 'results/gas-response.npz'
    assert saved.digest(kernel_path) == paths[str(kernel_path)]
    with np.load(kernel_path) as packet:
        kernels, components = packet['kernels'].copy(), list(packet['components'])
    with np.load(source.ROOT / 'results/preparation/basis.npz') as packet:
        factor = linear.cholesky(packet['mass'], lower=True)
    def norm(values):
        vectors = np.moveaxis(values[..., 1:97, :], -2, 0).reshape(96, -1)
        return np.linalg.norm(linear.solve_triangular(factor, vectors, lower=True), axis=0).reshape(values.shape[:-2] + (values.shape[-1],))
    with np.load(ROOT / 'results/gas-amplitudes.npz') as packet:
        amplitudes, labels = packet['amplitudes'].copy(), list(packet['labels'])
    checks, rows = [], []
    consumed = {str(kernel_path): saved.digest(kernel_path)}
    events = []
    for node in read(ROOT / 'configuration.json')['selected']:
        path = HALF / 'gas-events' / saved.angle_label(node['cosine']) / f"electron-{node['electron_index']:02d}.npz"
        assert saved.digest(path) == paths[str(path)]
        with np.load(path) as packet:
            assert json.loads(str(packet['node'])) == node
            events.append((packet['high'][1].copy(), packet['low'][1].copy()))
        consumed[str(path)] = saved.digest(path)
    reconstructed = np.empty_like(kernels)
    with mp.workdps(80):
        for index in np.ndindex(kernels.shape):
            reconstructed[index] = float(mp.fsum(mp.mpf(float(high[index])) + mp.mpf(float(low[index])) for high, low in events))
    assert np.array_equal(reconstructed, kernels)
    check(checks, '36 saved events reconstruct every gas kernel bitwise', 0)
    responses = np.empty((3, 5, 6, 98, 4))
    for grid_index, label_index, component, column in np.ndindex(3, 5, 6, 4):
        responses[grid_index, label_index, component, :, column] = kernels[component, :, column] * amplitudes[column // 2, grid_index, label_index]
    for grid_index, grid in enumerate(GRIDS):
        for component in [0, 4, 5]:
            values = responses[grid_index, :, component]
            norms = norm(values)
            raw_error = norm(values[3] - values[0]) / norms[0]
            forced_error = norm(values[3] - values[2]) / norms[2]
            corrected_error = norm(values[3] - values[4]) / norms[4]
            for column in range(4):
                amplitude = amplitudes[column // 2, grid_index]
                expected = relative_error(amplitude[3], amplitude[2])
                check(checks, f'{components[component]}:{column}:{grid}: source/gas corner fractional law',
                    abs(forced_error[column] - expected) / max(expected, 1e-300))
                check(checks, f'{components[component]}:{column}:{grid}: source corner/forced difference', forced_error[column], .01, 'source')
                rows.append(dict(component=components[component], column=column, model=MODELS[column // 2], grid=grid,
                    norm_by_label={label: float(norms[index, column]) for index, label in enumerate(labels)},
                    raw_relative_error=float(raw_error[column]), forced_relative_error=float(forced_error[column]),
                    corrected_relative_error=float(corrected_error[column]), tolerance=.01,
                    raw_passed=bool(raw_error[column] <= .01), forced_passed=bool(forced_error[column] <= .01),
                    corrected_passed=bool(corrected_error[column] <= .01)))
    for component in range(6):
        scale = np.maximum(np.maximum(abs(kernels[component, 0]), abs(kernels[component, -1])), 1e-300)
        check(checks, str(components[component]) + ': cached photon/gas energy cancellation',
            np.max(abs(kernels[component, 0] + kernels[component, -1]) / scale))
    check(checks, 'matched response kernel closure', np.max(norm(kernels[4] - kernels[1] - kernels[2] - kernels[3]) / norm(kernels[4])))
    check(checks, 'total response kernel closure', np.max(norm(kernels[5] - kernels[0] - kernels[4]) / norm(kernels[5])))
    np.savez_compressed(ROOT / 'results/gas-response.npz', kernels=kernels, responses=responses,
        grids=np.array(GRIDS), labels=np.array(labels), components=np.array(components))
    write(ROOT / 'results/gas-response-comparison.json', rows)
    write(ROOT / 'results/response-checks.json', dict(checks=checks, reused_gas_events=len(events), new_source_integrations=0))
    write(ROOT / 'response-inputs.json', consumed)
    write(ROOT / 'progress.json', dict(state='response_complete', frozen_prediction_sha256=saved.digest(ROOT / 'results/frozen-predictions.json')))
    print(json.dumps(dict(checks=len(checks), failed=[row for row in checks if not row['passed']],
        quarter=[row for row in rows if row['grid'] == 'quarter'])), flush=True)


if __name__ == '__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['analyse', 'response'])
    arguments = parser.parse_args()
    dict(analyse=analyse, response=response)[arguments.phase]()
