from common240 import *
import argparse
import virtual240
import state240


def freeze():
    config = protocol()
    assert not (ROOT / 'secondary-configuration.json').exists()
    inputs = {}
    mass_root = BRANCH / 'matched-mixed-state-20261026'
    for name in ('configuration.json', 'results/mass-coefficients.npz', 'results/mass.json', 'state235.py'):
        register(inputs, mass_root / name)
    assert digest(mass_root / 'results/mass-coefficients.npz') == read(mass_root / 'results/mass.json')['coefficient_sha256']
    for row in config['reused_event_zero']:
        for order in config['angular_orders']:
            register(inputs, REFERENCE / 'virtual' / f'angular{order}' / f'{row["label"]}-tensors.json')
            for join in config['joins']:
                path = REFERENCE / 'virtual' / f'angular{order}' / f'{row["label"]}-join{join}.npz'
                metadata = read(register(inputs, path.with_suffix('.json')))
                assert metadata['qualified']
                register(inputs, path, metadata['sha256'])
    reference = mass_root / 'runs' / config['reused_event_zero'][0]['label'] / 'state.npz'
    register(inputs, reference, read(reference.with_suffix('.json'))['sha256'])
    for join in config['joins']:
        register(inputs, virtual240.retained_virtual.VIRTUAL / 'radial' / f'join{join}-order6.npz')
    modules(inputs)
    write(ROOT / 'secondary-configuration.json', dict(frozen_at=now(), inputs=inputs,
        code={name: digest(ROOT / name) for name in ('virtual240.py', 'state240.py', 'secondary240.py')},
        original_tolerances_changed=False, dependencies='Reuse invariant scalar mass functional, recompute angle-dependent virtual and displaced-state sources'))


def control():
    modest()
    config = virtual240.secondary_protocol()
    assert not (ROOT / 'results/secondary-control.json').exists()
    virtual240.run(0, control=True)
    state240.run(0, control=True)
    reports = [read(path) for path in (ROOT / 'control').rglob('*.json')]
    checks = [entry for report in reports for entry in report['checks']]
    failures = [entry for entry in checks if not entry['passed']]
    assert len(reports) == 13
    write(ROOT / 'results/secondary-control.json', dict(qualified=not failures, checks=checks, failed=failures,
        packets=len(reports), finished_at=now(), scope='Generalized virtual maps/blocks and state derivative reproduce saved event0 before new kinematics'))
    print(json.dumps(dict(controls=len(checks), packets=len(reports), failures=failures[:3])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['freeze', 'control'])
    {'freeze': freeze, 'control': control}[parser.parse_args().mode]()
