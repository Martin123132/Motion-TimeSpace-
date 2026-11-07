from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PREVIOUS = BRANCH / 'two-way-thermal-gravity-20261026'
sys.path.insert(0, str(PREVIOUS))
import common230 as prior
from common230 import np, math, json, mp, sp, read, write, digest, register, check, relative, now, modest, save_npz
from scipy import linalg
from datetime import datetime
SEAL = '82c18a612c5848807e6c79149b80429aa943944ff0f4cb4a89291f362bd66c73'
START = '2026-10-26T18:57:01+00:00'


def prepare():
    assert not (ROOT / 'configuration.json').exists()
    assert digest(PREVIOUS / 'results/stage-integrity.json') == SEAL
    seal = read(PREVIOUS / 'results/stage-integrity.json')
    assert seal['qualified']
    inputs = dict(seal['directly_consumed_inputs'])
    register(inputs, PREVIOUS / 'results/stage-integrity.json')
    for name, expected in seal['file_hashes'].items():
        assert digest(register(inputs, PREVIOUS / name)) == expected
    for name in ('DERIVATION.md', 'thermal_wave_system.py', 'verify_thermal_identities.py', 'SOURCES.md'):
        register(inputs, BRANCH / 'expanding-thermal-gravity-20261007' / name)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=231, frozen_at=now(), previous_goal_turn='progress',
        turn_start=START, parent_seal=SEAL, models=['heavy', 'cold'], counts=[3200, 6400],
        sample_divisions=16, wave_number_Mpc_inverse=.1, numerical_threads=1, maximum_workers=2,
        algebra_tolerance=1e-9, thermodynamic_tolerance=1e-10, balance_tolerance=1e-8,
        refinement_tolerance=.01, negative_control_threshold=1e-7,
        original_bank_changed=False, original_tolerances_changed=False,
        protocol_hashes={path.name: digest(path) for path in ROOT.iterdir() if path.is_file() and path.suffix in ('.py', '.md')}))
    print(json.dumps(dict(prepared=True, inputs=len(inputs))), flush=True)


def protocol():
    config = read(ROOT / 'configuration.json')
    for name, expected in config['protocol_hashes'].items():
        assert digest(ROOT / name) == expected, name
    return config


def add_modules(inputs):
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs, path)


if __name__ == '__main__':
    prepare()
