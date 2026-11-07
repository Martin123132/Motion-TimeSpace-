from tail243 import *


def run_bounds():
    modest()
    results, checks, inputs = [], [], {}
    for model in ('heavy', 'cold'):
        report = read(register(inputs, DATA / f'relaxation/{model}.json'))
        config, baseline, data, layout = loaded(model, inputs)
        local = operator(data, layout, report['start'])
        with mp.workdps(80):
            unit = [mp.mpf(0)] * (2 + layout['margin'])
            unit[0] = 1
            response = forcing(local, layout, unit)
            gamma = mp.mpf(report['prediction']['gamma_start'])
            amplitude = abs(mp.mpf(report['prediction']['initial_fast_amplitude']))
            damping = mp.mpf(local['row_damping'])
            size = max(abs(value) for value in response)
            span = mp.mpf(config['target_coordinate']) - mp.mpf(report['start'])
            uniform = amplitude * size / gamma
            endpoint = amplitude * size * (mp.exp(-damping * span) - mp.exp(-gamma * span)) / (gamma - damping)
            check(checks, model + ':frozen positive tail damping', int(damping <= 0), 0)
            check(checks, model + ':frozen positive gas relaxation', int(gamma <= 0), 0)
            check(checks, model + ':endpoint below uniform frozen bound', int(endpoint < 0 or endpoint > uniform), 0)
        results.append(dict(model=model, gamma_gas_per_log_scale=float(gamma),
            tail_row_damping_per_log_scale=float(damping), gas_forcing_infinity_norm=float(size),
            initial_gas_amplitude=float(amplitude), uniform_frozen_tail_bound=float(uniform),
            target_frozen_tail_bound=float(endpoint),
            scope='Conditional constant-coefficient memory estimate, not variable-coefficient or total-source uncertainty bound'))
    modules(inputs)
    for path, checksum in inputs.items():
        assert digest(path) == checksum
    write(DATA / 'fast-memory-bounds.json', dict(checks=checks, qualified=all(row['passed'] for row in checks),
        records=results, script_sha256=digest(__file__), consumed_inputs=inputs, finished_at=now(),
        does_not_promote_failed_gates=True))
    print(dict(checks=checks, records=results), flush=True)


if __name__ == '__main__':
    run_bounds()

