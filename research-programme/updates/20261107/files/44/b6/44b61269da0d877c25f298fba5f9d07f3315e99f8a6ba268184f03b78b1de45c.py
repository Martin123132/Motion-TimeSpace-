from common237 import *
import argparse


def run(order):
    modest()
    config = protocol()
    assert order in config['real_orders_to_evaluate']
    original, features, models = setup(config)
    local = dict(config, angular_order=order)
    for row in config['events']:
        rays = list(angular.inherited.source.angular_nodes(order))
        for ray in range(len(rays)):
            stem = ROOT / 'real' / row['label'] / f'angular{order}' / f'ray-{ray:03d}'
            if stem.with_suffix('.json').exists():
                saved = read(stem.with_suffix('.json'))
                assert saved['configuration_sha256'] == digest(ROOT / 'configuration.json')
                assert saved['sha256'] == digest(stem.with_suffix('.npz'))
                continue
            assert not stem.with_suffix('.npz').exists(), 'Unsealed packet: inspect before replacing'
            if time.time() >= config['deadline_timestamp'] or (ROOT / 'STOP-REQUESTED').exists():
                print(json.dumps(dict(safe_stop=True, anchor=row['label'], order=order, next_ray=ray)), flush=True)
                return
            with mp.workdps(config['digits']):
                arrays, metadata = retained.ray_integral(local, row, config['radial_order'], ray, original, features, models)
            assert all(np.all(np.isfinite(value)) for value in arrays.values())
            save(stem.with_suffix('.npz'), **arrays)
            write(stem.with_suffix('.json'), dict(anchor=row['label'], angular_order=order, radial_order=config['radial_order'],
                ray=ray, **metadata, configuration_sha256=digest(ROOT / 'configuration.json'),
                sha256=digest(stem.with_suffix('.npz')), finished_at=now()))
            print(json.dumps(dict(anchor=row['label'], angular_order=order, saved_ray=ray, total_rays=len(rays), seconds=metadata['seconds'])), flush=True)
    print(json.dumps(dict(angular_order=order, all_anchors_complete=True)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('order', type=int, choices=[6, 8])
    run(parser.parse_args().order)
