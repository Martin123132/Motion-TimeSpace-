from tail243 import *


def run_partition(model):
    modest()
    frozen = read(ROOT / 'corner-configuration.json')
    assert frozen['script_sha256'] == digest(__file__)
    assert frozen['attribution_hashes'][model] == digest(DATA / f'attribution/{model}.json')
    inputs, checks = {}, []
    config, baseline, data, layout = loaded(model, inputs)
    forces = packet(register(inputs, DATA / f'tails/{model}/forcing.npz'))
    attribution = read(register(inputs, DATA / f'attribution/{model}.json'))
    observed = packet(register(inputs, DATA / f'attribution/{model}.npz'))
    drive = read(register(inputs, DATA / f'drives/{model}-half.json'))
    coarse = np.array([point['coordinate'] for point in drive['points']])
    times = forces['expansion']
    lookup = np.searchsorted(times, coarse)
    assert np.array_equal(times[lookup], coarse)
    states = np.zeros((len(layout['frequency']), 2))
    peak = int(np.searchsorted(times, attribution['peak_coordinate']))
    errors = []
    with mp.workdps(80):
        gas = []
        for index in range(len(times)):
            rows = [mp.mpf(float(forces['drive_high'][index, column, 0])) +
                mp.mpf(float(forces['drive_low'][index, column, 0])) for column in range(3)]
            gas.append([rows[0] + rows[1], rows[0] + rows[2]])
        gas_fine_at_coarse = [[gas[index][1]] for index in lookup]
        nodal_errors = [[gas[index][0] - gas[index][1]] for index in lookup]
        maximum_nodal, maximum_interpolation = mp.mpf(0), mp.mpf(0)
        for ordinal, coordinate in enumerate(times[1:], 1):
            nodal = interpolate(coarse, nodal_errors, coordinate)[0]
            curvature = interpolate(coarse, gas_fine_at_coarse, coordinate)[0] - gas[ordinal][1]
            total = gas[ordinal][0] - gas[ordinal][1]
            errors.append(float(abs(nodal + curvature - total)))
            maximum_nodal = max(maximum_nodal, abs(nodal))
            maximum_interpolation = max(maximum_interpolation, abs(curvature))
            local = operator(data, layout, coordinate)
            unit = [mp.mpf(0)] * forces['drive_high'].shape[2]
            unit[0] = 1
            response = forcing(local, layout, unit)
            values = np.array([[float(value * multiplier) for multiplier in (nodal, curvature)] for value in response])
            step = float(coordinate - times[ordinal - 1])
            system = sparse.eye(len(layout['frequency']), format='csc') - step * local['generator']
            states = splu(system).solve(states + step * values)
            if ordinal == peak:
                peak_states = states.copy()
                peak_drives = dict(nodal=float(nodal), interpolation=float(curvature), total=float(total))
    expected_peak = observed['peak_components'][:, 0]
    expected_target = observed['target_components'][:, 0]
    check(checks, model + ':exact gas interpolation/nodal partition', max(errors))
    check(checks, model + ':peak propagated gas partition', relative(peak_states.sum(axis=1) - expected_peak, expected_peak))
    check(checks, model + ':target propagated gas partition', relative(states.sum(axis=1) - expected_target, expected_target))
    report = dict(model=model, qualified=all(row['passed'] for row in checks), checks=checks,
        labels=['saved-node discrepancy', 'piecewise-linear interpolation curvature'],
        peak_coordinate=attribution['peak_coordinate'], peak_drives=peak_drives,
        peak_component_norms=np.linalg.norm(peak_states, axis=0).tolist(),
        peak_projection_on_gas=[float(column @ expected_peak / (expected_peak @ expected_peak)) for column in peak_states.T],
        target_component_norms=np.linalg.norm(states, axis=0).tolist(),
        target_projection_on_gas=[float(column @ expected_target / (expected_target @ expected_target)) for column in states.T],
        max_nodal_drive_difference=float(maximum_nodal), max_interpolation_drive_difference=float(maximum_interpolation),
        status='Diagnostic only; frozen histories and failed gates unchanged', script_sha256=digest(__file__), finished_at=now())
    modules(inputs)
    for path, checksum in inputs.items():
        assert digest(path) == checksum
    path = DATA / f'corner/{model}.npz'
    save(path, peak_components=peak_states, target_components=states, frequency=layout['frequency'])
    report.update(consumed_inputs=inputs, output_sha256=digest(path))
    write(path.with_suffix('.json'), report)
    print({key: value for key, value in report.items() if key != 'consumed_inputs'}, flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('model', choices=['heavy', 'cold'])
    run_partition(parser.parse_args().model)

