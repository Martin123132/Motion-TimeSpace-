from tail243 import *


def run_attribution(model):
    modest()
    frozen = read(ROOT / 'attribution-configuration.json')
    assert frozen['script_sha256'] == digest(__file__)
    assert digest(DATA / 'assessment/result.json') == frozen['assessment_sha256']
    inputs, checks = {}, []
    config, baseline, data, layout = loaded(model, inputs)
    fine_path = DATA / f'tails/{model}/time4.npz'
    force_path = DATA / f'tails/{model}/forcing.npz'
    fine, forces = packet(register(inputs, fine_path)), packet(register(inputs, force_path))
    assert np.array_equal(fine['expansion'], forces['expansion'])
    error = fine['state'][:, :, 1] - fine['state'][:, :, 2]
    magnitudes = np.linalg.norm(error, axis=1)
    peak_index = int(np.argmax(magnitudes))
    sizes, components, scale_rows = len(layout['frequency']), np.zeros((len(layout['frequency']), 3)), []
    peak_components = None
    forcing_error, sum_error, step_error = [], [], []
    forcing_peaks = np.zeros(3)
    maximum_components = np.zeros(3)
    with mp.workdps(80):
        for ordinal, coordinate in enumerate(fine['expansion'][1:], 1):
            local = operator(data, layout, coordinate)
            original = [[mp.mpf(float(high)) + mp.mpf(float(low)) for high, low in zip(
                forces['drive_high'][ordinal, column], forces['drive_low'][ordinal, column])] for column in (1, 2)]
            difference = [first - second for first, second in zip(original[0], original[1])]
            groups = [[mp.mpf(0)] * len(difference) for unused in range(3)]
            groups[0][0], groups[1][1] = difference[:2]
            groups[2][2:] = difference[2:]
            values = [forcing(local, layout, drive) for drive in groups]
            expected = [mp.mpf(float(forces['high'][ordinal, row, 1])) + mp.mpf(float(forces['low'][ordinal, row, 1]))
                - mp.mpf(float(forces['high'][ordinal, row, 2])) - mp.mpf(float(forces['low'][ordinal, row, 2])) for row in range(sizes)]
            combined = [mp.fsum(column[row] for column in values) for row in range(sizes)]
            denominator = max(prior.norm(mp.matrix(expected)), mp.mpf('1e-200'))
            forcing_error.append(float(prior.norm(mp.matrix(combined) - mp.matrix(expected)) / denominator))
            forcing_values = np.array([[float(value) for value in column] for column in values]).T
            forcing_peaks = np.maximum(forcing_peaks, np.linalg.norm(forcing_values, axis=0))
            step = float(coordinate - fine['expansion'][ordinal - 1])
            system = sparse.eye(sizes, format='csc') - step * local['generator']
            right = components + step * forcing_values
            components = splu(system).solve(right)
            step_error.append(float(np.max(abs(system @ components - right)) / max(np.max(abs(right)), 1e-300)))
            sum_error.append(norm(components.sum(axis=1) - error[ordinal]))
            maximum_components = np.maximum(maximum_components, np.linalg.norm(components, axis=0))
            scale_rows.append(np.linalg.norm(components, axis=0))
            if ordinal == peak_index:
                peak_components = components.copy()
            if ordinal % 400 == 0:
                print(dict(model=model, attribution=ordinal, steps=len(fine['expansion']) - 1), flush=True)
    check(checks, model + ':gas/beta/boundary force partition', max(forcing_error))
    check(checks, model + ':attribution BE residual', max(step_error))
    check(checks, model + ':evolved partition of history discrepancy', max(sum_error) / max(magnitudes.max(), 1e-300))
    target = fine['state'][-1, :, 2]
    peak_case = error[peak_index]
    worst_frequency_index = int(np.argmax(abs(peak_case)))
    report = dict(model=model, labels=['gas', 'hard-photon soft functional', 'upper boundary'], checks=checks,
        qualified=all(row['passed'] for row in checks), peak_coordinate=float(fine['expansion'][peak_index]),
        peak_fraction_of_interval=float((fine['expansion'][peak_index] - fine['expansion'][0]) /
            (fine['expansion'][-1] - fine['expansion'][0])),
        peak_discrepancy_l2=float(magnitudes[peak_index]), peak_component_l2=np.linalg.norm(peak_components, axis=0).tolist(),
        peak_most_affected_frequency=float(fine['frequency'][worst_frequency_index]),
        peak_pointwise_discrepancy=float(peak_case[worst_frequency_index]),
        target_discrepancy_relative=norm(error[-1]) / max(norm(target), 1e-300),
        target_discrepancy_l2=norm(error[-1]), target_component_l2=np.linalg.norm(components, axis=0).tolist(),
        maximum_component_l2=maximum_components.tolist(), maximum_forcing_l2=forcing_peaks.tolist(),
        peak_projection_on_net=[float(column @ peak_case / max(peak_case @ peak_case, 1e-300)) for column in peak_components.T],
        target_projection_on_net=[float(column @ error[-1] / max(error[-1] @ error[-1], 1e-300)) for column in components.T],
        original_failed_gates_remain=True, interpretation='Exact linear attribution within fixed discrete drive/tail choices; not a new fitted law',
        finished_at=now(), script_sha256=digest(__file__))
    modules(inputs)
    for path, checksum in inputs.items():
        assert digest(path) == checksum
    path = DATA / f'attribution/{model}.npz'
    save(path, coordinate=fine['expansion'][1:], component_norms=np.array(scale_rows), peak_components=peak_components,
        target_components=components, frequency=fine['frequency'])
    report.update(consumed_inputs=inputs, output_sha256=digest(path))
    write(path.with_suffix('.json'), report)
    print({key: value for key, value in report.items() if key not in ('consumed_inputs',)}, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('model', choices=['heavy', 'cold'])
    run_attribution(parser.parse_args().model)

