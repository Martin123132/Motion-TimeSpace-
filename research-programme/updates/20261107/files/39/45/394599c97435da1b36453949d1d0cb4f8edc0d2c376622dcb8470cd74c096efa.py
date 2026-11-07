from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'finite-real-mixed-source-20261026'
sys.dont_write_bytecode = True
sys.path.insert(0, str(PARENT))
import integrate236 as retained
from common236 import np, mp, json, time, read, write, save, packet, digest, register, check, relative, modest, now, datetime
from common236 import source, cached, precise, angular, prior, scalar, statistics, projected, geometry, state235
import common234
import radial234
SEAL = 'c012e7ec33665a991462bcf61ab054ab993d7077c4581883d95435db14319762'
START = '2026-10-27T01:21:20+00:00'
VIRTUAL = BRANCH / 'spectral-medium-response-20261026'
STATE = BRANCH / 'matched-mixed-state-20261026'


def setup(config):
    return retained.setup(config)


def protocol():
    config = read(ROOT / 'configuration.json')
    for name, expected in config['protocol_hashes'].items():
        assert digest(ROOT / name) == expected, name
    for name, expected in config['retained_code'].items():
        assert digest(name) == expected, name
    return config


def prepare():
    modest()
    assert not (ROOT / 'configuration.json').exists()
    assert digest(PARENT / 'results/stage-integrity.json') == SEAL
    seal = read(PARENT / 'results/stage-integrity.json')
    assert seal['qualified']
    inputs = dict(seal['directly_consumed_inputs'])
    register(inputs, PARENT / 'results/stage-integrity.json', SEAL)
    for name, expected in seal['file_hashes'].items():
        register(inputs, PARENT / name, expected)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    parent = read(PARENT / 'configuration.json')
    implementation = {str(PARENT / name): expected for name, expected in read(PARENT / 'integration-configuration.json')['files'].items()}
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=237, started_at=START, frozen_at=now(),
        deadline_timestamp=datetime.fromisoformat(START).timestamp() + 3.8 * 3600,
        events=parent['events'], states=parent['states'], heat=parent['heat'], target_fraction=parent['target_fraction'],
        target_theta=parent['target_theta'], spectral_domain=parent['spectral_domain'],
        reference_real_angular_order=4, reference_virtual_angular_order=2,
        candidate_angular_orders=[4, 6, 8], real_orders_to_evaluate=[6, 8], radial_order=26, virtual_radial_order=6,
        maximum_log_width=.5, digits=60, virtual_digits=80, joins=[0, 1], multipoles=[0, 1, 2],
        identity_tolerance=1e-10, angular_tolerance=.002, original_bank_changed=False, original_tolerances_changed=False,
        physical_scope='All three original x14,event0 anchors; both joins; equilibrium plus six histories; scalar-intensity l0/1/2',
        state_angular_handling='Reuse exact scalar mass angular identity and saved displaced-state matrices',
        retained_code=implementation, bookmarks={str(path): digest(path) for path in (BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md')},
        protocol_hashes={path.name: digest(path) for path in ROOT.iterdir() if path.suffix in ('.py', '.md')}))
    print(json.dumps(dict(prepared=True, verified_inputs=len(inputs), target_real_rays=600)), flush=True)


if __name__ == '__main__':
    prepare()
