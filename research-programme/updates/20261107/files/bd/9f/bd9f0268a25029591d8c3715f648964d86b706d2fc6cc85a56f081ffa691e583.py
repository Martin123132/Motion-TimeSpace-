from common243 import *
import argparse
from scipy import sparse
from scipy.sparse.linalg import splu


def norm(values):
    return float(np.linalg.norm(values))


def relative(values, reference):
    return norm(values) / max(norm(reference), 1e-300)


def split(values):
    high = np.array([float(value) for value in values])
    low = np.array([float(value - mp.mpf(float(part))) for value, part in zip(values, high)])
    return high, low


def scalar_rows(layout, state):
    profile, gas = state['profile'], state['gas']
    return [gas, mp.fsum(mp.mpf(float(weight)) * value for weight, value in zip(layout['beta'], profile))] + [
        mp.fsum(mp.mpf(float(weight)) * value for weight, value in zip(line, profile)) for line in layout['high_values']]


def interpolate(coordinates, values, coordinate):
    index = min(max(int(np.searchsorted(coordinates, coordinate)) - 1, 0), len(coordinates) - 2)
    fraction = (mp.mpf(float(coordinate)) - mp.mpf(float(coordinates[index]))) / (
        mp.mpf(float(coordinates[index + 1])) - mp.mpf(float(coordinates[index])))
    assert 0 <= fraction <= 1
    return [first + fraction * (second - first) for first, second in zip(values[index], values[index + 1])]


def operator(data, layout, coordinate):
    values = interp1d(data['coefficient_knots'], data['coefficient_bank'], axis=0, bounds_error=True)(float(coordinate))
    count, size, margin = len(layout['offsets']), len(layout['frequency']), layout['margin']
    coefficients = values[:count]
    eigenvalue, dc_coefficient, rate = values[count:count + 3]
    br = values[count + 3:]
    dc = dc_coefficient / layout['all_grid']**2
    gamma = dc + br
    internal, lower, upper = tail.owner.split_matrix(coefficients, layout['offsets'], size)
    generator = rate * (internal + sparse.diags(eigenvalue - gamma[margin:margin + size], format='csc'))
    return dict(generator=generator, lower=lower, upper=upper, dc=dc, br=br, gamma=gamma,
        rate=float(rate), eigenvalue=float(eigenvalue), coefficients=coefficients,
        row_damping=float(np.min(-generator @ np.ones(size))),
        offdiag_min=float(np.min(np.delete(coefficients, np.where(layout['offsets'] == 0)))))


def forcing(local, layout, drive):
    gas, beta = drive[:2]
    dc, br = [list(map(lambda value: mp.mpf(float(value)), local[name])) for name in ('dc', 'br')]
    gamma = list(map(lambda value: mp.mpf(float(value)), local['gamma']))
    margin, size = layout['margin'], len(layout['frequency'])
    source = [first * beta + second * gas for first, second in zip(dc, br)]
    exterior = [source[index] / gamma[index] for index in range(margin)] + [mp.mpf(0)] * size + drive[2:]
    result = []
    eigenvalue, rate = mp.mpf(local['eigenvalue']), mp.mpf(local['rate'])
    for index in range(size):
        position = margin + index
        boundary = mp.fsum(mp.mpf(float(weight)) * exterior[position + int(offset)]
            for weight, offset in zip(local['coefficients'], layout['offsets'])
            if not margin <= position + int(offset) < margin + size)
        result.append(rate * (source[position] - eigenvalue * gas + boundary))
    return result


def loaded(model, inputs):
    config = protocol()
    context, unused = connection.source.context(read(PARENT / 'configuration.json')['target_fraction'])
    index = ('heavy', 'cold').index(model)
    baseline_path, unused, tail_path = context.inputs[4 * index:4 * index + 3]
    baseline = packet(register(inputs, baseline_path))
    data = packet(register(inputs, tail_path))
    return config, baseline, data, tail.geometry(data, context.basis)


def freeze():
    config = protocol()
    validation = read(DATA / 'drives/validation.json')
    assert validation['qualified']
    inputs = dict(validation['consumed_inputs'])
    register(inputs, DATA / 'drives/validation.json')
    for case in validation['cases']:
        register(inputs, case['path'], case['sha256'])
    for model in ('heavy', 'cold'):
        loaded(model, inputs)
    register(inputs, tail.owner.ROOT / 'compare_tails.py')
    modules(inputs)
    assert not (ROOT / 'tail-configuration.json').exists()
    write(ROOT / 'tail-configuration.json', dict(frozen_at=now(), script_sha256=digest(__file__),
        method_sha256=digest(ROOT / 'TAIL-METHOD.md'), inputs=inputs, subdivisions=[1, 2, 4],
        dense_output='Piecewise linear80-digit projected drives on saved physical-state knots; no temperature fit',
        common_grid='Union of half/quarter history knots, original history/tail knots, coefficient knots and endpoints',
        initial_rule='Common saved tail at authenticated photon/gas start; differences zero only there',
        retained_gate_core_absolute=1e-4, retained_gate_moment_relative=.01,
        retained_gate_moment_envelope=1e-5, identity_tolerance=1e-10,
        history_mesh_tolerance=config['history_mesh_tolerance'], source_tolerance=config['source_tolerance'],
        no_source_contraction=True))


def tail_protocol():
    frozen = read(ROOT / 'tail-configuration.json')
    assert frozen['script_sha256'] == digest(__file__)
    assert frozen['method_sha256'] == digest(ROOT / 'TAIL-METHOD.md')
    for path, checksum in frozen['inputs'].items():
        assert digest(path) == checksum, path
    return frozen


def prepare_forces(model, baseline, data, layout, config, checks):
    path = DATA / f'tails/{model}/forcing.npz'
    metadata_path = path.with_suffix('.json')
    if metadata_path.exists():
        metadata = read(metadata_path)
        assert metadata['script_sha256'] == digest(__file__) and digest(path) == metadata['sha256']
        checks.extend(metadata['checks'])
        return packet(path)
    start, stop = config['cases'][0]['start'], config['target_coordinate']
    sources = [read(DATA / f'drives/{model}-{grid}.json') for grid in ('half', 'quarter')]
    baseline_times = np.r_[start, baseline['expansion'][(baseline['expansion'] > start) & (baseline['expansion'] < stop)], stop]
    original_profiles = interp1d(baseline['expansion'], baseline['profiles'], axis=0)(baseline_times)
    original_gas = np.interp(baseline_times, baseline['expansion'], baseline['temperature_scaled'])
    coarse_times = np.unique(np.r_[baseline_times,
        data['expansion'][(data['expansion'] > start) & (data['expansion'] < stop)],
        data['coefficient_knots'][(data['coefficient_knots'] > start) & (data['coefficient_knots'] < stop)],
        *[[point['coordinate'] for point in source['points']] for source in sources]])
    assert coarse_times[0] == start and coarse_times[-1] == stop
    fine_times = np.unique(np.r_[np.concatenate([np.linspace(first, second, 5)[:-1] for first, second in zip(coarse_times[:-1], coarse_times[1:])]), stop])
    assert np.all(np.diff(fine_times) > 0)
    forcing_high, forcing_low, driving_high, driving_low = [], [], [], []
    local_checks = []
    with mp.workdps(80):
        original_values = [scalar_rows(layout, dict(profile=list(map(lambda value: mp.mpf(float(value)), profile)), gas=mp.mpf(float(gas))))
            for profile, gas in zip(original_profiles, original_gas)]
        projected = [(np.array([point['coordinate'] for point in source['points']]),
            [scalar_rows(layout, history.parse_state(point['state'])) for point in source['points']]) for source in sources]
        for grid, unused in enumerate(projected):
            check(local_checks, f'{model}:shared seed:{grid}',
                max(abs(first - second) for first, second in zip(original_values[0], projected[grid][1][0])))
        for ordinal, coordinate in enumerate(fine_times):
            original = interpolate(baseline_times, original_values, coordinate)
            repaired = [interpolate(coordinates, values, coordinate) for coordinates, values in projected]
            drives = [original] + [[value - before for value, before in zip(values, original)] for values in repaired]
            local = operator(data, layout, coordinate)
            values = [forcing(local, layout, drive) for drive in drives]
            if ordinal in (0, len(fine_times) // 2, len(fine_times) - 1):
                for grid in range(2):
                    direct = forcing(local, layout, repaired[grid])
                    check(local_checks, f'{model}:{ordinal}:{grid}:affine forcing',
                        prior.relative(mp.matrix(values[0]) + mp.matrix(values[grid + 1]), mp.matrix(direct)))
                with mp.workdps(100):
                    for column, drive in enumerate(drives):
                        audited = forcing(local, layout, drive)
                        check(local_checks, f'{model}:{ordinal}:{column}:80/100 forcing',
                            prior.relative(mp.matrix(values[column]), mp.matrix(audited)) if any(audited) else 0)
            pairs = [split(value) for value in values]
            forcing_high.append(np.array([pair[0] for pair in pairs]).T)
            forcing_low.append(np.array([pair[1] for pair in pairs]).T)
            drive_pairs = [split(value) for value in drives]
            driving_high.append(np.array([pair[0] for pair in drive_pairs]))
            driving_low.append(np.array([pair[1] for pair in drive_pairs]))
            if ordinal % 400 == 0:
                print(dict(model=model, phase='forcing', point=ordinal, total=len(fine_times)), flush=True)
    arrays = dict(expansion=fine_times, coarse_times=coarse_times, high=np.array(forcing_high), low=np.array(forcing_low),
        drive_high=np.array(driving_high), drive_low=np.array(driving_low), frequency=data['frequency'],
        initial=interp1d(data['expansion'], data['slope'], axis=0)(start))
    assert all(row['passed'] for row in local_checks), local_checks
    save(path, **arrays)
    write(metadata_path, dict(sha256=digest(path), script_sha256=digest(__file__), checks=local_checks,
        points=len(fine_times), finished_at=now(), forces_formed_before_rounding=True))
    checks.extend(local_checks)
    return arrays


def interval_margin(data, layout, start, stop):
    points = np.r_[start, data['coefficient_knots'][(data['coefficient_knots'] > start) & (data['coefficient_knots'] < stop)], stop]
    rate_min, margin_min, offdiag = float('inf'), float('inf'), float('inf')
    for coordinate in points:
        local = operator(data, layout, coordinate)
        rate_min = min(rate_min, local['rate'])
        margin_min = min(margin_min, float(np.min(local['gamma'] - local['eigenvalue'] - sum(local['coefficients']))))
        offdiag = min(offdiag, local['offdiag_min'])
    return rate_min * margin_min, offdiag


def evolve(model, subdivision, forces, data, layout, checks):
    path = DATA / f'tails/{model}/time{subdivision}.npz'
    metadata_path = path.with_suffix('.json')
    if metadata_path.exists():
        metadata = read(metadata_path)
        assert metadata['script_sha256'] == digest(__file__) and digest(path) == metadata['sha256']
        checks.extend(metadata['checks'])
        return
    selected_times = np.unique(np.r_[np.concatenate([np.linspace(first, second, subdivision + 1)[:-1]
        for first, second in zip(forces['coarse_times'][:-1], forces['coarse_times'][1:])]), forces['expansion'][-1]])
    indices = np.searchsorted(forces['expansion'], selected_times)
    assert np.array_equal(forces['expansion'][indices], selected_times)
    times = forces['expansion'][indices]
    size = len(layout['frequency'])
    state = np.zeros((size, 8))
    state[:, 0] = forces['initial']
    state[:, 3:5] = forces['initial'][:, None]
    state[:, 7] = 1
    states, residuals, affine, envelope_slack, min_envelopes = [state[:, :3].copy()], [], [], [], []
    for ordinal, selected in enumerate(indices[1:], 1):
        step = float(times[ordinal] - times[ordinal - 1])
        local = operator(data, layout, times[ordinal])
        generator = local['generator']
        system = sparse.eye(size, format='csc') - step * generator
        inverse = splu(system)
        force = forces['high'][selected] + forces['low'][selected]
        right = state.copy()
        right[:, :3] += step * force
        right[:, 3:5] += step * (force[:, :1] + force[:, 1:3])
        right[:, 5:7] += step * abs(force[:, 1:3])
        updated = inverse.solve(right)
        residuals.append(float(np.max(abs(system @ updated - right)) / max(np.max(abs(right)), 1e-300)))
        affine.append(float(np.max(abs(updated[:, 3:5] - updated[:, :1] - updated[:, 1:3])) /
            max(np.max(abs(updated)), 1e-300)))
        envelope_slack.append(float(np.max(abs(updated[:, 1:3]) - updated[:, 5:7])))
        min_envelopes.append(float(np.min(updated[:, 5:])))
        state = updated
        states.append(state[:, :3].copy())
    slopes = np.array(states)
    local_checks = []
    check(local_checks, f'{model}:time{subdivision}:BE residual', max(residuals))
    check(local_checks, f'{model}:time{subdivision}:full versus difference evolution', max(affine))
    check(local_checks, f'{model}:time{subdivision}:executed forcing envelope', max(0, max(envelope_slack)))
    check(local_checks, f'{model}:time{subdivision}:positive comparison solutions', max(0, -min(min_envelopes)))
    check(local_checks, f'{model}:time{subdivision}:finite arrays', int(not np.isfinite(slopes).all()), 0)
    final_local = operator(data, layout, times[-1])
    final_force = forces['high'][-1] + forces['low'][-1]
    derivative = final_local['generator'] @ slopes[-1] + final_force
    stationary = splu(-final_local['generator']).solve(final_force)
    original_stored = interp1d(data['expansion'], data['slope'], axis=0)(times)
    save(path, expansion=times, frequency=layout['frequency'], state=slopes, derivative=derivative,
        stationary_diagnostic=stationary, original_stored=original_stored,
        final_comparison_envelope=state[:, 5:7], initial_unit_response=state[:, 7])
    write(metadata_path, dict(qualified=all(row['passed'] for row in local_checks), checks=local_checks,
        sha256=digest(path), script_sha256=digest(__file__), steps=len(times) - 1, finished_at=now()))
    checks.extend(local_checks)
    print(dict(model=model, subdivision=subdivision, steps=len(times) - 1, checks=local_checks), flush=True)


def run(model):
    modest()
    frozen = tail_protocol()
    inputs, checks = dict(frozen['inputs']), []
    config, baseline, data, layout = loaded(model, inputs)
    status_path = DATA / f'workers/tail-{model}.json'
    write(status_path, dict(state='running', pid=os.getpid(), model=model, started_at=now()))
    margin, offdiag = interval_margin(data, layout, config['cases'][0]['start'], config['target_coordinate'])
    check(checks, model + ':whole coefficient interval positive damping', int(margin <= 0), 0)
    check(checks, model + ':whole coefficient interval Metzler', max(0, -offdiag), 0)
    forces = prepare_forces(model, baseline, data, layout, config, checks)
    for subdivision in frozen['subdivisions']:
        evolve(model, subdivision, forces, data, layout, checks)
    modules(inputs)
    for path, checksum in inputs.items():
        assert digest(path) == checksum, path
    write(DATA / f'tails/{model}/complete.json', dict(qualified=all(row['passed'] for row in checks),
        checks=checks, failed=[row for row in checks if not row['passed']], consumed_inputs=inputs,
        conservative_whole_interval_damping=margin, script_sha256=digest(__file__), finished_at=now()))
    write(status_path, dict(state='complete', pid=os.getpid(), model=model, finished_at=now()))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['freeze', 'heavy', 'cold'])
    arguments = parser.parse_args()
    if arguments.phase == 'freeze':
        freeze()
    else:
        run(arguments.phase)

