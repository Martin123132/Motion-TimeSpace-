from history242 import *
sys.path.insert(0, str(BRANCH / 'dynamical-infrared-tail-20261008'))
import tail_common as owner
from scipy.interpolate import interp1d


def geometry(data, basis):
    frequency = data['frequency']
    spacing = float(np.log(frequency[1] / frequency[0]))
    offsets = data['offsets'].astype(int)
    margin = max(-int(offsets[0]), int(offsets[-1]))
    lower = frequency[0] * np.exp(spacing * np.arange(-margin, 0))
    upper = frequency[-1] * np.exp(spacing * np.arange(1, margin + 1))
    assert upper.min() >= basis.minimum and upper.max() < basis.maximum
    return dict(frequency=frequency, offsets=offsets, margin=margin,
        all_grid=np.r_[lower, frequency, upper], high_values=basis.evaluate(upper) / upper[:, None],
        beta=owner.soft_slope_row(basis, 256))


def local_rhs(data, layout, coordinate, profile, gas, slope):
    values = interp1d(data['coefficient_knots'], data['coefficient_bank'], axis=0, bounds_error=True)(float(coordinate))
    count = len(layout['offsets'])
    coefficients = [mp.mpf(float(value)) for value in values[:count]]
    eigenvalue, dc_coefficient, rate = [mp.mpf(float(value)) for value in values[count:count + 3]]
    br = [mp.mpf(float(value)) for value in values[count + 3:]]
    dc = [dc_coefficient / mp.mpf(float(value))**2 for value in layout['all_grid']]
    gamma = [first + second for first, second in zip(dc, br)]
    beta = mp.fsum(mp.mpf(float(weight)) * value for weight, value in zip(layout['beta'], profile))
    source = [first * beta + second * gas for first, second in zip(dc, br)]
    margin, size = layout['margin'], len(layout['frequency'])
    lower = [source[index] / gamma[index] for index in range(margin)]
    upper = [mp.fsum(mp.mpf(float(weight)) * value for weight, value in zip(line, profile)) for line in layout['high_values']]
    extended = lower + list(slope) + upper
    result, margins, scales = [], [], []
    for index, value in enumerate(slope):
        position = margin + index
        jump = mp.fsum(weight * extended[position + int(offset)] for weight, offset in zip(coefficients, layout['offsets']))
        diagonal = (eigenvalue - gamma[position]) * value
        forcing = source[position] - eigenvalue * gas
        result.append(rate * (jump + diagonal + forcing))
        margins.append(rate * (gamma[position] - eigenvalue))
        scales.append(abs(rate) * (abs(jump) + abs(diagonal) + abs(forcing)))
    return mp.matrix(result), dict(minimum_damping=min(margins), maximum_damping=max(margins),
        coefficient_constant_defect=abs(mp.fsum(coefficients)) / max(mp.fsum(abs(value) for value in coefficients), mp.mpf('1e-300')),
        scale=mp.matrix(scales), beta=beta)


def run():
    modest()
    config = protocol()
    assert not (ROOT / 'results/tail-rhs.json').exists()
    history = read(ROOT / 'results/history.json')
    assert history['qualified']
    inputs = dict(history['consumed_inputs'])
    original, unused = connection.source.context(config['target_fraction'])
    checks, records, arrays = [], [], {}
    with mp.workdps(80):
        for model_index, model in enumerate(('heavy', 'cold')):
            tail_path = Path(original.inputs[4 * model_index + 2])
            data = packet(register(inputs, tail_path))
            status = read(register(inputs, tail_path.parent / 'status.json'))
            assert status['script_sha256'] == digest(register(inputs, owner.ROOT / 'evolve_tail.py'))
            assert status['all_checks_passed']
            layout = geometry(data, original.basis)
            current = mp.matrix([mp.mpf(float(value)) for value in original.epochs[0].tails[model][1]])
            interpolant = saved_slope(data, 'slope', config['coordinate'])
            for state in [row for row in config['states'] if row['model'] == model]:
                vector = list(map(mp.mpf, state['coefficients']))
                profile, gas = mp.matrix(vector[:96]), vector[-1]
                value, diagnostic = local_rhs(data, layout, config['coordinate'], profile, gas, current)
                with mp.workdps(100):
                    audited, unused = local_rhs(data, layout, config['coordinate'], profile, gas, current)
                name = model + ':' + state['history']
                check(checks, name + ':80/100 tail RHS', relative(value, audited))
                check(checks, name + ':positive damping margin', int(diagnostic['minimum_damping'] <= 0), 0)
                check(checks, name + ':constant jump identity', diagnostic['coefficient_constant_defect'])
                projection = mp.fsum(first * second for first, second in zip(value, current)) / mp.fsum(part * part for part in current)
                high = np.array(list(map(float, value)))
                low = np.array([float(exact - mp.mpf(float(part))) for exact, part in zip(value, high)])
                arrays[name + ':high'], arrays[name + ':low'] = high, low
                records.append(dict(model=model, history=state['history'],
                    slope_rhs=[mp.nstr(part, 85) for part in value],
                    interpolant_derivative_relative_defect=float(relative(interpolant, value)),
                    relative_rate=float(norm(value) / norm(current)),
                    nonproportional_fraction=float(norm(value - projection * current) / norm(value)),
                    minimum_damping_per_log_scale=float(diagnostic['minimum_damping']),
                    maximum_damping_per_log_scale=float(diagnostic['maximum_damping']),
                    scope='Retained soft-tail RHS on saved tail state with this photon/gas drive; no replacement history evolved'))
            baseline_path = Path(original.inputs[4 * model_index])
            baseline = packet(register(inputs, baseline_path))
            left, right = bracket(data, config['coordinate'])
            for index in (left, right):
                coordinate = float(data['expansion'][index])
                profile = interp1d(baseline['expansion'], baseline['profiles'], axis=0)(coordinate)
                gas = float(np.interp(coordinate, baseline['expansion'], baseline['temperature_scaled']))
                state = mp.matrix([mp.mpf(float(value)) for value in data['slope'][index]])
                before = mp.matrix([mp.mpf(float(value)) for value in data['slope'][index - 1]])
                result, diagnostic = local_rhs(data, layout, coordinate, list(map(lambda value: mp.mpf(float(value)), profile)), mp.mpf(gas), state)
                step = mp.mpf(float(data['expansion'][index])) - mp.mpf(float(data['expansion'][index - 1]))
                residual = state - before - step * result
                scale = max(norm(state) + norm(before) + step * norm(diagnostic['scale']), mp.mpf('1e-300'))
                check(checks, model + f':saved BE state identity:{index}', norm(residual) / scale, 1e-9)
            arrays[model + ':frequency'] = data['frequency']
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    path = ROOT / 'results/tail-rhs.npz'
    save(path, **arrays)
    failed = [row for row in checks if not row['passed']]
    write(ROOT / 'results/tail-rhs.json', dict(qualified=not failed, checks=checks, failed=failed,
        records=records, consumed_inputs=inputs, output_sha256=digest(path), script_sha256=digest(__file__),
        finished_at=now(), spectral_source_contraction_done=False, repaired_tail_history_evolved=False,
        limitation='Retained leading soft-tail equation and its fixed exterior rules, not all-frequency finite-recoil dynamics'))
    print(dict(tail_rhs_checks=len(checks), failed=failed), flush=True)


if __name__ == '__main__':
    run()
