from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'mixed-angular-vertex-20261026'
sys.path.insert(0, str(PARENT))
import run233 as prior
from common233 import np, mp, json, time, read, write, save, packet, digest, register, check, relative, modest, now, datetime
from mixed_vertex233 import scalar, statistics, raw_flux, projected, geometry
source, cached, precise, angular = prior.source, prior.cached, prior.precise, prior.angular
SEAL = 'b4054a2244ae712c7abd6eb4fca06d2f707389fe29af61667d2a94ea0fbe46b0'
START = '2026-10-26T20:15:31+00:00'


def modules(inputs):
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs, path)


def protocol():
    config = read(ROOT / 'configuration.json')
    for name, value in config['protocol_hashes'].items():
        assert digest(ROOT / name) == value, name
    return config


def prepare():
    assert not (ROOT / 'configuration.json').exists()
    assert digest(PARENT / 'results/stage-integrity.json') == SEAL
    seal = read(PARENT / 'results/stage-integrity.json')
    assert seal['qualified']
    inputs = dict(seal['directly_consumed_inputs'])
    register(inputs, PARENT / 'results/stage-integrity.json', SEAL)
    for name, expected in seal['file_hashes'].items():
        register(inputs, PARENT / name, expected)
    config = read(PARENT / 'configuration.json')
    original, features, models = prior.setup(config)
    for path in original.inputs:
        register(inputs, path)
    for row in config['events']:
        keys = set(read(row['loop_path']))
        assert {'identity', 'scalar', 'finite'} <= keys <= {'identity', 'scalar', 'finite', 'seconds'}
        row['cache_fields'] = sorted(keys)
    modules(inputs)
    for path, value in inputs.items():
        assert digest(path) == value, path
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=234, turn_start=START, previous_goal_turn='progress', frozen_at=now(),
        parent_seal=SEAL, events=config['events'], states=config['states'], target_fraction=config['target_fraction'],
        target_theta=config['target_theta'], heat=config['heat'], multipoles=[0, 1, 2], joins=[0, 1],
        spectral_domain=[float(features.frequency[0]), float(features.frequency[-1])],
        spline_grid_cells=len(features.splines[0].x) - 1, radial_orders=[4, 6], loop_angular_order=2,
        exact_identity_tolerance=1e-10, inherited_wave_refinement_tolerance=.002,
        representation='full98 photon coordinates plus unchanged gas; no assumed exterior spectrum',
        tensor_digits=80, maximum_workers=2, numerical_threads=1,
        original_bank_changed=False, original_tolerances_changed=False, new_virtual_cache_entries=0,
        bookmarks={str(path): digest(path) for path in (BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md')},
        protocol_hashes={path.name: digest(path) for path in ROOT.iterdir() if path.suffix in ('.py', '.md')}))
    print(json.dumps(dict(prepared=True, inputs=len(inputs), cells=len(features.splines[0].x) - 1)), flush=True)


def setup(config):
    return prior.setup(config)


def complex_text(value):
    return [mp.nstr(mp.re(value), 85), mp.nstr(mp.im(value), 85)]


def complex_value(value):
    return mp.mpc(*value)


def matrix_text(matrix):
    return [[complex_text(matrix[row, column]) for column in range(matrix.cols)] for row in range(matrix.rows)]


def matrix_value(values):
    return mp.matrix([[complex_value(value) for value in line] for line in values])


if __name__ == '__main__':
    modest()
    prepare()
