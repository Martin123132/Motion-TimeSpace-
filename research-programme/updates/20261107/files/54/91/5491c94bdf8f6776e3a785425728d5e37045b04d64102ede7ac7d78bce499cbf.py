from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'spectral-medium-response-20261026'
sys.dont_write_bytecode = True
sys.path.insert(0, str(PARENT))
import common234 as previous
from common234 import np, mp, json, time, read, write, save, packet, digest, register, check, relative, modest, now, datetime
from common234 import source, cached, precise, angular, prior, scalar, statistics, raw_flux, projected, geometry
SEAL = '5b44b749423d2a21332ecc7167df6c714564adbaaa270be832a7d92256e3215c'
START = '2026-10-26T20:38:23+00:00'


def modules(inputs):
    for module in list(sys.modules.values()):
        name = getattr(module, '__file__', None)
        if name:
            path = Path(name).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs, path)


def setup(config):
    return previous.setup(config)


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
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=235, previous_goal_turn='progress', turn_start=START,
        frozen_at=now(), parent_seal=SEAL, events=config['events'], states=config['states'],
        target_fraction=config['target_fraction'], target_theta=config['target_theta'], heat=config['heat'],
        spectral_domain=config['spectral_domain'], multipoles=[0, 1, 2], joins=[0, 1],
        identity_tolerance=1e-10, refinement_tolerance=.002, canonical_steps=[.001, .0005],
        radial_orders=[4, 6], precision_digits=80, original_bank_changed=False, original_tolerances_changed=False,
        bookmarks={str(path): digest(path) for path in (BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md')},
        protocol_hashes={path.name: digest(path) for path in ROOT.iterdir() if path.suffix in ('.py', '.md')}))
    print(json.dumps(dict(prepared=True, inputs=len(inputs), stage=235)), flush=True)


if __name__ == '__main__':
    prepare()
