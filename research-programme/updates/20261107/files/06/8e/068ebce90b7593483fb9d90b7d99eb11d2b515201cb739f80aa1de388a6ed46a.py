from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'matched-mixed-state-20261026'
sys.dont_write_bytecode = True
sys.path.insert(0, str(PARENT))
import common235 as previous
import state235
import real235
from common235 import np, mp, json, time, read, write, save, packet, digest, register, check, relative, modest, now, datetime
from common235 import source, cached, precise, angular, prior, scalar, statistics, raw_flux, projected, geometry
import math
SEAL = '97332e34a3cd875256f4fefed8ff9990259406ada2df2984a2d661dbf5481429'
START = '2026-10-26T21:06:20+00:00'


def setup(config):
    return previous.setup(config)


def modules(inputs):
    for module in list(sys.modules.values()):
        name = getattr(module, '__file__', None)
        if name:
            path = Path(name).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs, path)


def protocol():
    config = read(ROOT / 'configuration.json')
    for name, expected in config['protocol_hashes'].items():
        assert digest(ROOT / name) == expected, name
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
    config = read(PARENT / 'configuration.json')
    original, features, models = setup(config)
    modules(inputs)
    for name, expected in inputs.items():
        assert digest(name) == expected, name
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=236, turn_start=START, previous_goal_turn='progress', frozen_at=now(),
        events=config['events'], states=config['states'], target_fraction=config['target_fraction'],
        target_theta=config['target_theta'], heat=config['heat'], joins=[0, 1], multipoles=[0, 1, 2],
        spectral_domain=config['spectral_domain'], angular_order=4, radial_orders=[18, 26], maximum_log_width=.5,
        identity_tolerance=1e-10, same_discretization_replay_tolerance=1e-7, refinement_tolerance=.002,
        arbitrary_precision_digits=60, precision_control_digits=80, original_bank_changed=False, original_tolerances_changed=False,
        bookmarks={str(path): digest(path) for path in (BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md')},
        protocol_hashes={path.name: digest(path) for path in ROOT.iterdir() if path.suffix in ('.py', '.md')}))
    print(json.dumps(dict(prepared=True, stage=236, inputs=len(inputs))), flush=True)


if __name__ == '__main__':
    prepare()
