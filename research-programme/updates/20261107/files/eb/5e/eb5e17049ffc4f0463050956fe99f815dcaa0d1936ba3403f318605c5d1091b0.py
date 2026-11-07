from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PREVIOUS = BRANCH / 'eos-spatial-source-20261026'
sys.path.insert(0, str(PREVIOUS))
import common231 as previous
from common231 import np, math, json, mp, sp, read, write, digest, register, check, relative, now, modest, save_npz
from scipy import special
from datetime import datetime
from contextlib import contextmanager
import time
sys.path.insert(0, str(BRANCH / 'matched-weak-redistribution-20261008'))
import matched_weak as inherited
SEAL = 'd9772a35a992bffc67e1c7744f3640bce1ca837b05730ed720ab5ddef2478245'
START = '2026-10-26T19:19:28+00:00'


def add_modules(inputs):
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs, path)


def prepare():
    assert not (ROOT / 'configuration.json').exists()
    assert digest(PREVIOUS / 'results/stage-integrity.json') == SEAL
    parent = read(PREVIOUS / 'results/stage-integrity.json')
    assert parent['qualified']
    inputs = dict(parent['directly_consumed_inputs'])
    register(inputs, PREVIOUS / 'results/stage-integrity.json')
    for name, expected in parent['file_hashes'].items():
        assert digest(register(inputs, PREVIOUS / name)) == expected
    probes = []
    for label, folder in [('initial', 'moving-a8-r56'), ('middle', 'midpoint-v6')]:
        path = BRANCH / 'matched-weak-redistribution-20261008/results' / folder
        report = read(register(inputs, path / 'status.json'))
        assert report['all_checks_passed']
        register(inputs, path / 'matrix.npz')
        virtual = report['thermal_virtual_ratio'] if label == 'initial' else report['thermal_virtual_scalar']
        probes.append(dict(label=label, temperature=report['temperature'], velocity=report['velocity'],
            virtual_scalar=virtual, source=str(path), lab_cosine=.1, incoming_frequency=1.))
    for name in ['angular-emission-kernel-20261008/DERIVATION.md', 'matched-weak-redistribution-20261008/DERIVATION.md',
                 'moving-polarized-thermal-20261008/moving_frame.py', 'finite-thermal-source-20261008/thermal_event_source.py']:
        register(inputs, BRANCH / name)
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=232, previous_goal_turn='progress', turn_start=START,
        frozen_at=now(), parent_seal=SEAL, probes=probes, degrees=[0, 1, 2],
        quadratures=[[6, 40], [8, 56]], profile_test=.2, separator_test=.2,
        algebra_tolerance=1e-10, event_conservation_tolerance=1e-12, matched_null_tolerance=2e-7,
        inherited_wave_refinement_tolerance=.002, same_discretization_replay_tolerance=1e-7,
        matched_scheme_tolerance=2e-7, soft_floors=[1e-3, 1e-4], maximum_workers=2, numerical_threads=1,
        new_virtual_amplitudes=False, original_bank_changed=False, original_tolerances_changed=False,
        protocol_hashes={path.name: digest(path) for path in ROOT.iterdir() if path.is_file() and path.suffix in ('.py', '.md')}))
    print(json.dumps(dict(prepared=True, inputs=len(inputs), probes=probes)), flush=True)


def protocol():
    config = read(ROOT / 'configuration.json')
    for name, expected in config['protocol_hashes'].items():
        assert digest(ROOT / name) == expected, name
    return config


if __name__ == '__main__':
    prepare()
