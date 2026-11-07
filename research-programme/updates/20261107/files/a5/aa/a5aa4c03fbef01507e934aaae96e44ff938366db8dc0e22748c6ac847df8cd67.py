from __future__ import annotations
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'angular-mixed-source-20261027'
sys.dont_write_bytecode = True
sys.path.insert(0, str(PARENT))
import common237 as saved
from common237 import np, mp, json, time, read, write, save, packet, digest, register, check, relative, modest, now, datetime
from common237 import scalar, precise, source, angular, statistics, geometry, projected
sys.path.insert(0, str(BRANCH / 'eos-spatial-source-20261026'))
import source231 as gravity
from scipy import linalg
SEAL = '11e63838ad6635dabc8e1a8ad63590bd7492d8b6068340109dfbb64136aedaf0'
START = '2026-10-27T05:00:54+00:00'


def setup(config):
    return saved.setup(config)


def modules(inputs):
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs, path)


def protocol():
    config = read(ROOT / 'configuration.json')
    for name, expected in config['protocol_hashes'].items():
        assert digest(ROOT / name) == expected, name
    return config


def physical_states(config):
    with mp.workdps(80):
        exact = [[scalar(config['heat']) * mp.mpf(value) for value in state['coefficients']] for state in config['states']]
        high = np.array([[float(value) for value in row] for row in exact]).T
        low = np.array([[float(value - scalar(float(value))) for value in row] for row in exact]).T
    return exact, high, low


def prepare():
    modest()
    assert not (ROOT / 'configuration.json').exists()
    assert digest(PARENT / 'results/stage-integrity.json') == SEAL
    seal = read(PARENT / 'results/stage-integrity.json')
    assert seal['qualified']
    payloads = {name.replace('\\', '/'): value for name, value in seal['file_hashes'].items()}
    inputs = {}
    register(inputs, PARENT / 'results/stage-integrity.json', SEAL)
    for name in ['configuration.json', 'results/completion.json'] + [f'results/{anchor}-assessment.{suffix}'
                for anchor in ('warm', 'middle', 'cold') for suffix in ('json', 'npz')]:
        register(inputs, PARENT / name, payloads[name])
    parent = read(PARENT / 'configuration.json')
    original, features, models = setup(parent)
    for path in original.inputs:
        register(inputs, path)
    for name in ('source231.py', 'DERIVATION.md', 'COLLISION-PORTS.md', 'results/stage-integrity.json'):
        register(inputs, BRANCH / 'eos-spatial-source-20261026' / name)
    for model in ('heavy', 'cold'):
        register(inputs, BRANCH / 'two-way-thermal-gravity-20261026' / 'runs' / (model + '-6400') / 'history.npz')
    modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=238, started_at=START, frozen_at=now(), previous_goal_turn='progress',
        parent_seal=SEAL, events=parent['events'], states=parent['states'], heat=parent['heat'],
        target_fraction=parent['target_fraction'], target_theta=parent['target_theta'], joins=[0, 1], multipoles=[0, 1, 2],
        angular_versions=['original', '6', '8'], components=['leading_control', 'MTS_correction', 'combined'],
        identity_tolerance=1e-10, physical_response_tolerance=.002, digits=80, wave_number=.1,
        source_scope='Mixed homogeneous-background derivative on three saved x14,event0 anchors; not a complete angular event bank',
        input_scope='98 photon input coordinates including two explicit saved-tail ports plus gas; no tail closure',
        units='Inherited c=8piG=1, conformal time, opacity=a ne sigmaT; stresses normalized to rho_star',
        baseline_scope='Inherited leading real-process control, separately on heavy and cold parent histories',
        original_bank_changed=False, original_tolerances_changed=False,
        bookmarks={str(path): digest(path) for path in (BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md')},
        protocol_hashes={path.name: digest(path) for path in ROOT.iterdir() if path.suffix in ('.py', '.md')}))
    save(ROOT / 'frozen/basis.npz', mass=features.basis.mass, energy=features.basis.energy,
        temperature=features.basis.temperature, number=features.basis.number)
    print(json.dumps(dict(prepared=True, inputs=len(inputs))), flush=True)


if __name__ == '__main__':
    prepare()
