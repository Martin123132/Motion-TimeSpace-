from common229 import *
import argparse


def process_alive(pid):
    import ctypes
    from ctypes import wintypes
    kernel = ctypes.WinDLL('kernel32', use_last_error=True)
    kernel.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    kernel.OpenProcess.restype = wintypes.HANDLE
    kernel.GetExitCodeProcess.argtypes = [wintypes.HANDLE, ctypes.POINTER(wintypes.DWORD)]
    kernel.CloseHandle.argtypes = [wintypes.HANDLE]
    handle = kernel.OpenProcess(0x1000, False, pid)
    if not handle:
        return False
    code = wintypes.DWORD()
    ok = kernel.GetExitCodeProcess(handle, ctypes.byref(code))
    kernel.CloseHandle(handle)
    return bool(ok and code.value == 259)


def run(model, count, started):
    config = protocol()
    assert read(ROOT / 'results/preflight.json')['qualified']
    folder = ROOT / f'runs/{model}-{count}'
    folder.mkdir(parents=True, exist_ok=True)
    status_path = folder / 'status.json'
    if status_path.exists():
        previous_status = read(status_path)
        if previous_status['state'] == 'complete':
            return True
        if previous_status.get('pid') != os.getpid() and process_alive(previous_status.get('pid', 0)):
            raise RuntimeError('Saved worker still alive; refusing duplicate')
    identity = dict(configuration_sha256=digest(ROOT / 'configuration.json'), model=model, count=count)
    inputs = read(ROOT / 'results/preflight-inputs.json')
    system = System(model, count, inputs)
    rows = np.zeros((count + 1, 12))
    profiles = np.zeros((count + 1, system.basis.count, 2))
    raw = np.zeros((count + 1, 2))
    minimum_occupation, maximum_departure = np.ones(2), np.zeros(2)
    state = initial(system)
    previous = initial(system)
    rows[0], profiles[0] = packet_row(system, 0, state), state['profiles']
    first = 1
    restart = folder / 'restart.npz'
    if restart.exists():
        assert read(folder / 'restart-identity.json') == identity
        with np.load(restart) as saved:
            first = int(saved['index']) + 1
            rows[:first] = saved['rows']
            profiles[:first] = saved['profiles']
            raw[:first] = saved['raw']
            minimum_occupation = saved['minimum_occupation']
            maximum_departure = saved['maximum_departure']
            state = {key: saved['state_' + key] for key in state}
            previous = {key: saved['previous_' + key] for key in previous}
    else:
        write(folder / 'restart-identity.json', identity)
    write(status_path, dict(state='running', pid=os.getpid(), started_at=now(), index=first - 1, count=count, model=model))
    for index in range(first, count + 1):
        updated, diagnostics = advance(system, index, state, previous)
        previous, state = state, updated
        rows[index], profiles[index] = packet_row(system, index, state), state['profiles']
        raw[index] = diagnostics['raw_relative']
        if index % config['chunk_steps'] == 0 or index == count:
            physical_profiles = np.column_stack([state['profiles'][:, 0], state['profiles'][:, 0] + state['profiles'][:, 1]])
            occupation_departure = system.heat * (1 + 1 / np.expm1(system.emission.frequency))[:, None] * (system.emission.values @ physical_profiles)
            minimum_occupation = np.minimum(minimum_occupation, np.min(1 + occupation_departure, axis=0))
            maximum_departure = np.maximum(maximum_departure, np.max(abs(occupation_departure), axis=0))
            save_npz(restart, index=index, rows=rows[:index + 1], profiles=profiles[:index + 1], raw=raw[:index + 1],
                minimum_occupation=minimum_occupation, maximum_departure=maximum_departure,
                **{'state_' + key: value for key, value in state.items()},
                **{'previous_' + key: value for key, value in previous.items()})
            write(status_path, dict(state='running', pid=os.getpid(), updated_at=now(), model=model,
                count=count, index=index, elapsed_seconds=time.monotonic() - started, restart_sha256=digest(restart)))
            print(json.dumps(dict(model=model, count=count, saved=index, elapsed=round(time.monotonic() - started, 1))), flush=True)
            if time.monotonic() - started > 3 * 3600 and index < count:
                write(status_path, dict(state='saved_time_limit', pid=os.getpid(), index=index, count=count, model=model))
                return False
    heat = system.heat
    nr_balance = rows[:, 1] + heat * rows[:, 3] + rows[:, 6]
    difference_balance = rows[:, 2] + rows[:, 5] + rows[:, 7] - float(system.eos['delta_A'][0])
    checks = []
    check(checks, 'NR energy/work balance', np.max(abs(nr_balance)), 1e-8)
    check(checks, 'EOS difference energy/work balance', np.max(abs(difference_balance)) / np.max(abs(rows[:, 2] + rows[:, 5])), 1e-8)
    for column, label in enumerate(('NR', 'EOS_difference')):
        check(checks, label + ': raw kinetic equation throughout', np.max(raw[:, column]), 1e-7)
    physical_gas = np.column_stack([rows[:, 3], rows[:, 3] + rows[:, 4]])
    check(checks, 'Small temperature departure', np.max(abs(heat * physical_gas)), .002)
    check(checks, 'Positive gas temperature', int(np.min(1 + heat * physical_gas) <= 0), 0)
    check(checks, 'Positive heat capacity', int(np.min(system.eos['C']) <= 0), 0)
    check(checks, 'Sampled photon occupation positive', int(np.min(minimum_occupation) <= 0), 0)
    check(checks, 'Sampled photon departure remains small', np.max(maximum_departure), .002)
    if count == 6400:
        old_path = BRANCH / f'infrared-source-domain-20261008/backgrounds/{model}-nonlocal-refined-6400/history.npz'
        with np.load(register(inputs, old_path)) as old:
            check(checks, 'Original NR spectrum recovery', relative(profiles[:, :, 0], old['profiles']), 1e-7)
            check(checks, 'Original NR gas recovery', relative(rows[:, 3], old['temperature_scaled']), 1e-7)
            check(checks, 'Original NR energy recovery', relative(rows[:, 1], old['energy_scaled']), 1e-7)
            check(checks, 'Original NR work recovery', relative(rows[:, 6], old['expansion_work']), 1e-7)
    prediction_path = PREVIOUS / f'results/{model}-stress.npz'
    with np.load(register(inputs, prediction_path)) as prediction:
        target_q = np.interp(rows[:, 0], prediction['expansion'], prediction['delta_q'])
        target_p = np.interp(rows[:, 0], prediction['expansion'], prediction['delta_p'])
    check(checks, 'Frozen Stage228 density prediction', relative(rows[:, 9], target_q), .01)
    check(checks, 'Frozen Stage228 pressure prediction', relative(rows[:, 11], target_p), .01)
    check(checks, 'Initial excess density retained', rows[0, 9] / target_q[0] - 1, 1e-10)
    check(checks, 'Initial excess pressure zero', rows[0, 11], 0)
    negative = relative(rows[:, 9] - rows[0, 9], target_q)
    checks.append(dict(name='Missing-initial-heat negative control fails', value=negative, minimum=.01, passed=negative > .01))
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    save_npz(folder / 'history.npz', rows=rows, profiles=profiles, raw_residuals=raw,
        A0=system.eos['A'], C0=system.eos['C'], theta=system.theta, chi=heat,
        density_prediction=target_q, pressure_prediction=target_p)
    write(folder / 'inputs.json', inputs)
    report = dict(stage=229, state='complete', pid=os.getpid(), model=model, count=count, finished_at=now(),
        checks=checks, qualified=all(row['passed'] for row in checks), failed=[row for row in checks if not row['passed']],
        elapsed_seconds=time.monotonic() - started, final_delta_q=float(rows[-1, 9]), final_delta_p=float(rows[-1, 11]),
        final_delta_gas_temperature=float(heat * rows[-1, 4]), sampled_minimum_occupation=minimum_occupation.tolist(),
        sampled_maximum_occupation_departure=maximum_departure.tolist(), history_sha256=digest(folder / 'history.npz'))
    write(status_path, report)
    print(json.dumps(dict(model=model, count=count, qualified=report['qualified'], failed=report['failed'],
        final_delta_q=report['final_delta_q'], elapsed=round(report['elapsed_seconds'], 1))), flush=True)
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
