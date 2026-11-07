from common237 import *
import argparse
import psutil


def freeze():
    config = protocol()
    assert not (ROOT / 'split-configuration.json').exists()
    for process in psutil.process_iter(['pid', 'cmdline']):
        command = process.info['cmdline'] or []
        assert not any(Path(value).name == 'real237.py' for value in command), process.info
    assert len(list((ROOT / 'real').glob('*/angular6/ray-*.json'))) == 216
    assignments = [[], []]
    index = 0
    for row in config['events']:
        for ray in range(128):
            path = ROOT / 'real' / row['label'] / 'angular8' / f'ray-{ray:03d}.npz'
            if path.with_suffix('.json').exists():
                report = read(path.with_suffix('.json'))
                assert report['configuration_sha256'] == digest(ROOT / 'configuration.json')
                assert digest(path) == report['sha256']
                continue
            assert not path.exists() and not path.with_suffix('.partial').exists(), str(path)
            assignments[index % 2].append(dict(anchor=row['label'], ray=ray))
            index += 1
    assert not (ROOT / 'STOP-REQUESTED').exists()
    write(ROOT / 'split-configuration.json', dict(frozen_at=now(), script_sha256=digest(__file__),
        configuration_sha256=digest(ROOT / 'configuration.json'), assignments=assignments,
        remaining_rays=index, deadline_timestamp=config['deadline_timestamp'],
        reason='After angular6 completes and the single angular8 worker saves/exits, use the two existing slots for disjoint remaining rays; no numerical changes'))
    print(json.dumps(dict(remaining=index, partitions=[len(part) for part in assignments])), flush=True)


def run(partition):
    modest()
    config = protocol()
    frozen = read(ROOT / 'split-configuration.json')
    assert frozen['script_sha256'] == digest(__file__)
    assert frozen['configuration_sha256'] == digest(ROOT / 'configuration.json')
    original, features, models = setup(config)
    local = dict(config, angular_order=8)
    for assignment in frozen['assignments'][partition]:
        row = next(row for row in config['events'] if row['label'] == assignment['anchor'])
        ray = assignment['ray']
        stem = ROOT / 'real' / row['label'] / 'angular8' / f'ray-{ray:03d}'
        if stem.with_suffix('.json').exists():
            report = read(stem.with_suffix('.json'))
            assert digest(stem.with_suffix('.npz')) == report['sha256']
            continue
        assert not stem.with_suffix('.npz').exists()
        if time.time() >= config['deadline_timestamp'] or (ROOT / 'STOP-REQUESTED').exists():
            print(json.dumps(dict(safe_stop=True, partition=partition, anchor=row['label'], next_ray=ray)), flush=True)
            return
        with mp.workdps(config['digits']):
            arrays, metadata = retained.ray_integral(local, row, config['radial_order'], ray, original, features, models)
        assert all(np.all(np.isfinite(value)) for value in arrays.values())
        save(stem.with_suffix('.npz'), **arrays)
        write(stem.with_suffix('.json'), dict(anchor=row['label'], angular_order=8, radial_order=config['radial_order'], ray=ray,
            **metadata, configuration_sha256=digest(ROOT / 'configuration.json'),
            scheduler_sha256=digest(ROOT / 'split-configuration.json'), partition=partition,
            sha256=digest(stem.with_suffix('.npz')), finished_at=now()))
        print(json.dumps(dict(partition=partition, anchor=row['label'], saved_ray=ray, seconds=metadata['seconds'])), flush=True)
    print(json.dumps(dict(partition=partition, complete=True)), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', '0', '1'])
    mode = parser.parse_args().mode
    freeze() if mode == 'freeze' else run(int(mode))
