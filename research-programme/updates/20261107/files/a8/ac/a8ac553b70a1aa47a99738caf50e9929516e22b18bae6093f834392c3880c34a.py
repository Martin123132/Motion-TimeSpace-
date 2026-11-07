from common230 import *
import argparse
from evolve229 import process_alive


def run(model, count, started):
    config = protocol()
    assert read(ROOT / 'results/preflight.json')['qualified']
    folder = ROOT / f'runs/{model}-{count}'
    folder.mkdir(parents=True, exist_ok=True)
    status_path = folder / 'status.json'
    if status_path.exists():
        status = read(status_path)
        if status['state'] == 'complete':
            return status['qualified']
        if status.get('pid') != os.getpid() and process_alive(status.get('pid', 0)):
            raise RuntimeError('Existing worker is alive; no duplicate allowed')
    inputs = read(ROOT / 'results/preflight-inputs.json')
    system = System(model, count, inputs)
    rows = np.zeros((count + 1, 19))
    profiles = np.zeros((count + 1, system.basis.count, 2))
    fields = np.zeros((count + 1, 2, 2, 3))
    clocks = np.zeros((count + 1, 2, 3))
    state, diagnostic = initial(system)
    previous, ignored = initial(system)
    rows[0] = packet_row(system, 0, state, diagnostic)
    fields[0], profiles[0], clocks[0] = state['fields'], state['profiles'], state['clocks']
    first = 1
    identity = dict(configuration_sha256=digest(ROOT / 'configuration.json'), model=model, count=count)
    restart = folder / 'restart.npz'
    if restart.exists():
        assert read(folder / 'restart-identity.json') == identity
        with np.load(restart) as saved:
            first = int(saved['index']) + 1
            rows[:first], profiles[:first], fields[:first], clocks[:first] = saved['rows'], saved['profiles'], saved['fields'], saved['clocks']
            state = {key: saved['state_' + key] for key in state}
            previous = {key: saved['previous_' + key] for key in previous}
    else:
        write(folder / 'restart-identity.json', identity)
    write(status_path, dict(state='running', pid=os.getpid(), model=model, count=count, index=first - 1, started_at=now()))
    for index in range(first, count + 1):
        step = Step(system, index, state, previous)
        updated, diagnostic = step.advance()
        previous, state = state, updated
        rows[index] = packet_row(system, index, state, diagnostic)
        profiles[index], fields[index], clocks[index] = state['profiles'], state['fields'], state['clocks']
        if index % config['chunk_steps'] == 0 or index == count:
            save_npz(restart, index=index, rows=rows[:index + 1], profiles=profiles[:index + 1], fields=fields[:index + 1], clocks=clocks[:index + 1],
                **{'state_' + key: value for key, value in state.items()},
                **{'previous_' + key: value for key, value in previous.items()})
            write(status_path, dict(state='running', pid=os.getpid(), model=model, count=count, index=index,
                updated_at=now(), elapsed_seconds=time.monotonic() - started, restart_sha256=digest(restart)))
            print(json.dumps(dict(model=model, count=count, saved=index, elapsed=round(time.monotonic() - started, 1))), flush=True)
            if time.monotonic() - started > 3 * 3600 and index < count:
                write(status_path, dict(state='saved_time_limit', pid=os.getpid(), model=model, count=count, index=index))
                return False
    heat = system.heat
    checks = []
    check(checks, 'NR thermal energy/work budget', np.max(abs(rows[:, 1] + heat * rows[:, 3] + rows[:, 6])), 1e-8)
    check(checks, 'EOS difference thermal energy/work budget',
        np.max(abs(rows[:, 2] + rows[:, 5] + rows[:, 7] - system.initial_D)) / np.max(abs(rows[:, 2] + rows[:, 5])), 1e-8)
    for column, label in ((15, 'no_heat'), (16, 'NR'), (17, 'EOS')):
        check(checks, label + ': scaled Friedmann residual', np.max(abs(rows[:, column])), 1e-10)
    check(checks, 'Positive sampled root Jacobian', int(np.min(rows[:, 18]) <= 0), 0)
    check(checks, 'Small gas temperature departures', heat * max(np.max(abs(rows[:, 3])), np.max(abs(rows[:, 3] + rows[:, 4]))), .002)
    check(checks, 'Positive heat capacity', int(np.min(system.eos['C']) <= 0), 0)
    selected = np.arange(0, count + 1, count // 100)
    samples = rows[selected, 0]
    reference = [state_at_scale(system.background, system.background.start_scale * math.exp(float(point))) for point in samples]
    reference_hubble = np.array([value['hubble'] for value in reference])
    check(checks, 'No-heat background versus independent retained parent', relative(rows[selected, 12], reference_hubble), .01)
    with np.load(register(inputs, THERMO / f'results/{model}-gravity.npz')) as saved:
        assert np.max(abs(saved['expansion'] - samples)) < 1e-14
        predicted = saved['physical_hubble_response']
        check(checks, 'NR heat H response versus Stage228', relative(rows[selected, 13], predicted[:, 0]), .01)
        check(checks, 'EOS H response versus Stage228', relative((1 + rows[selected, 13]) * rows[selected, 14], predicted[:, 1]), .01)
        for column, physical_column, label in ((1, 0, 'NR'), (2, 1, 'EOS')):
            amplitude = float(saved['amplitudes'][physical_column])
            check(checks, label + ': paired scalar fields versus Stage228', relative(fields[selected, :, :, column].reshape(-1, 4), saved['response'][:, :4, physical_column] * amplitude), .01)
            check(checks, label + ': paired clocks versus Stage228', relative(clocks[selected, :, column], saved['physical_clock_response'][:, :, physical_column]), .01)
    previous_count_path = PREVIOUS / f'runs/{model}-{count}/history.npz'
    with np.load(register(inputs, previous_count_path)) as saved:
        for column, label in ((9, 'density'), (11, 'pressure'), (4, 'gas')):
            check(checks, 'Kinetic EOS ' + label + ' versus Stage229', relative(rows[:, column], saved['rows'][:, column]), .01)
        check(checks, 'Kinetic EOS spectrum versus Stage229', relative(profiles[:, :, 1], saved['profiles'][:, :, 1]), .01)
    scale = system.background.start_scale * np.exp(rows[:, 0])
    reference_density = np.array([system.reference_density(float(value)) for value in scale])
    energy_fields = np.sum(fields[:, 1, :, 0]**2 / scale[:, None]**2 + system.mass[None, :]**2 * fields[:, 0, :, 0]**2, axis=1) / 2
    pressure_fields = np.sum(fields[:, 1, :, 0]**2 / scale[:, None]**2 - system.mass[None, :]**2 * fields[:, 0, :, 0]**2, axis=1) / 2
    density0 = reference_density + energy_fields
    pressure0 = system.background.parent.radiation / (3 * scale**4) + pressure_fields
    density_derivative = (1.5 * density0[2:] - 2 * density0[1:-1] + .5 * density0[:-2]) / system.step
    field_continuity_error = float(np.max(abs(density_derivative + 3 * (density0[2:] + pressure0[2:])) / (abs(density_derivative) + 3 * abs(density0[2:] + pressure0[2:]))))
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    save_npz(folder / 'history.npz', rows=rows, profiles=profiles, fields=fields, clocks=clocks, chi=heat,
        initial_D=system.initial_D, A0=system.eos['A'], C0=system.eos['C'])
    write(folder / 'inputs.json', inputs)
    report = dict(stage=230, state='complete', pid=os.getpid(), model=model, count=count, finished_at=now(),
        checks=checks, qualified=all(row['passed'] for row in checks), failed=[row for row in checks if not row['passed']],
        final_fraction_NR=float(rows[-1, 13]), final_fraction_EOS=float(rows[-1, 14]),
        final_EOS_fraction_relative_no_heat=float((1 + rows[-1, 13]) * rows[-1, 14]),
        minimum_root_J=float(np.min(rows[:, 18]) / 2), no_heat_discrete_continuity_diagnostic=field_continuity_error,
        elapsed_seconds=time.monotonic() - started, history_sha256=digest(folder / 'history.npz'))
    write(status_path, report)
    print(json.dumps(dict(model=model, count=count, qualified=report['qualified'], failed=report['failed'],
        final_NR=report['final_fraction_NR'], final_EOS=report['final_fraction_EOS'], elapsed=round(report['elapsed_seconds'], 1))), flush=True)
    return report['qualified']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', choices=['heavy', 'cold'], required=True)
    arguments = parser.parse_args()
    modest()
    started = time.monotonic()
    for count in protocol()['counts']:
        if not run(arguments.model, count, started):
            break
