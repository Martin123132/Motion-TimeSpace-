from common240 import *
import argparse


def freeze():
    config = protocol()
    assert not (ROOT / 'radial-configuration.json').exists()
    write(ROOT / 'radial-configuration.json', dict(frozen_at=now(), script_sha256=digest(__file__),
        parent_configuration=digest(ROOT / 'configuration.json'), angular_order=6, coarse_radial_order=18,
        fine_radial_order=26, refinement_tolerance=config['refinement_tolerance'],
        purpose='Independent radial18-to26 check at the finer angular6 rule for all six new hard-angle rows',
        runtime_minutes_are_scheduling_only=True))


def run(hard_event, minutes):
    modest()
    config = protocol()
    frozen = read(ROOT / 'radial-configuration.json')
    assert frozen['script_sha256'] == digest(__file__)
    assert frozen['parent_configuration'] == digest(ROOT / 'configuration.json')
    assert read(ROOT / 'results/secondary-control.json')['qualified']
    original, features, models = setup(config)
    integrator = candidate_integrator()
    folder = ROOT / 'workers' / f'radial18-event{hard_event}'
    folder.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + min(minutes, 210.) * 60
    status = dict(pid=os.getpid(), state='running', started_at=now(), event=hard_event, completed_this_run=0, deadline=deadline)
    write(folder / 'status.json', status)
    for row in config['events']:
        if row['event'] != hard_event:
            continue
        for ray in range(72):
            stem = ROOT / 'radial18' / event_key(row) / f'ray-{ray:03d}'
            if stem.with_suffix('.json').exists():
                record = read(stem.with_suffix('.json'))
                assert record['configuration_sha256'] == digest(ROOT / 'radial-configuration.json')
                assert digest(stem.with_suffix('.npz')) == record['sha256']
                continue
            assert not stem.with_suffix('.npz').exists()
            if time.time() >= deadline or (ROOT / 'STOP-REQUESTED').exists():
                status.update(state='safe_stop', next_event=event_key(row), next_ray=ray, saved_at=now())
                write(folder / 'status.json', status)
                print(json.dumps(status), flush=True)
                return
            status.update(current_event=event_key(row), current_ray=ray, saved_at=now())
            write(folder / 'status.json', status)
            with mp.workdps(config['digits']):
                arrays, metadata = integrator(dict(config, angular_order=6), row, 18, ray, original, features, models)
            assert all(np.all(np.isfinite(value)) for value in arrays.values())
            assert metadata['maximum_independent_four_force_residual'] <= config['identity_tolerance']
            save(stem.with_suffix('.npz'), **arrays)
            record = dict(event_key=event_key(row), angular_order=6, radial_order=18, ray=ray, **metadata,
                sha256=digest(stem.with_suffix('.npz')), configuration_sha256=digest(ROOT / 'radial-configuration.json'), finished_at=now())
            write(stem.with_suffix('.json'), record)
            with (folder / 'log.txt').open('a', encoding='utf-8') as handle:
                handle.write(json.dumps(record) + '\n')
            status['completed_this_run'] += 1
            status.update(last_saved=str(stem), saved_at=now())
            write(folder / 'status.json', status)
            if ray % 16 == 15 or ray == 71:
                print(json.dumps(dict(radial18=event_key(row), rays_saved=ray + 1, total=72, seconds=metadata['seconds'])), flush=True)
    status.update(state='complete', finished_at=now())
    write(folder / 'status.json', status)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
    print(json.dumps(status), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'run'])
    parser.add_argument('--event', type=int, choices=[1, 2], default=1)
    parser.add_argument('--minutes', type=float, default=180.)
    arguments = parser.parse_args()
    freeze() if arguments.mode == 'freeze' else run(arguments.event, arguments.minutes)
