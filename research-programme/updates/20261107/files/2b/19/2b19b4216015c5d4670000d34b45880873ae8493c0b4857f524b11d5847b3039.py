from common240 import *
import argparse


def run(hard_event):
    modest()
    config = protocol()
    assert read(ROOT / 'results/preflight.json')['qualified']
    original, features, models = setup(config)
    integrator = candidate_integrator()
    folder = ROOT / 'workers' / f'event{hard_event}'
    folder.mkdir(parents=True, exist_ok=True)
    inputs = read(ROOT / 'inputs.json')
    modules(inputs)
    status = dict(pid=os.getpid(), state='running', started_at=now(), hard_event=hard_event, completed_this_run=0)
    write(folder / 'status.json', status)
    for row in config['events']:
        if row['event'] != hard_event:
            continue
        for order in config['angular_orders']:
            rays = len(list(angular.inherited.source.angular_nodes(order)))
            for ray in range(rays):
                stem = ROOT / 'real' / event_key(row) / f'angular{order}' / f'ray-{ray:03d}'
                if stem.with_suffix('.json').exists():
                    record = read(stem.with_suffix('.json'))
                    assert record['configuration_sha256'] == digest(ROOT / 'configuration.json')
                    assert record['sha256'] == digest(stem.with_suffix('.npz'))
                    continue
                assert not stem.with_suffix('.npz').exists(), 'Unsealed output requires recovery before resuming'
                if time.time() >= config['deadline_timestamp'] or (ROOT / 'STOP-REQUESTED').exists():
                    status.update(state='safe_stop', next_event=event_key(row), next_order=order, next_ray=ray, saved_at=now())
                    write(folder / 'status.json', status)
                    print(json.dumps(status), flush=True)
                    return
                status.update(current_event=event_key(row), current_order=order, current_ray=ray, saved_at=now())
                write(folder / 'status.json', status)
                local = dict(config, angular_order=order)
                with mp.workdps(config['digits']):
                    arrays, metadata = integrator(local, row, config['radial_order'], ray, original, features, models)
                assert all(np.all(np.isfinite(value)) for value in arrays.values())
                assert metadata['maximum_independent_four_force_residual'] <= config['identity_tolerance']
                save(stem.with_suffix('.npz'), **arrays)
                record = dict(event_key=event_key(row), anchor=row['label'], event=row['event'], angular_order=order,
                    ray=ray, radial_order=config['radial_order'], **metadata, sha256=digest(stem.with_suffix('.npz')),
                    configuration_sha256=digest(ROOT / 'configuration.json'), finished_at=now())
                write(stem.with_suffix('.json'), record)
                with (folder / 'log.txt').open('a', encoding='utf-8') as handle:
                    handle.write(json.dumps(record) + '\n')
                status['completed_this_run'] += 1
                status.update(last_saved=str(stem), saved_at=now())
                write(folder / 'status.json', status)
                if ray % 16 == 15 or ray == rays - 1:
                    print(json.dumps(dict(event=event_key(row), order=order, rays_saved=ray + 1, total=rays,
                        seconds=metadata['seconds'])), flush=True)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(folder / 'inputs.json', inputs)
    status.update(state='complete', finished_at=now())
    write(folder / 'status.json', status)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
    print(json.dumps(status), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('event', type=int, choices=[1, 2])
    arguments = parser.parse_args()
    try:
        run(arguments.event)
    except Exception as error:
        write(ROOT / 'workers' / f'event{arguments.event}/failure.json', dict(pid=os.getpid(), state='failed',
            error=repr(error), failed_at=now(), source_sha256=digest(__file__)))
        raise
