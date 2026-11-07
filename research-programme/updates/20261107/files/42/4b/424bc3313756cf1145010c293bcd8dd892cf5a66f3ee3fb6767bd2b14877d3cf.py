from __future__ import annotations

from datetime import datetime, timezone
import json
import math
import os
from pathlib import Path
import sys

os.environ['OMP_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
sys.dont_write_bytecode = True

import numpy as np
import psutil
from scipy import interpolate

from acquire_native import ROOT, digest

PARENT = ROOT.parent / 'radiation-and-slow-field-transfer-20261007'
POST = ROOT.parent.parent
sys.path.insert(0, str(ROOT / 'native'))
sys.path.append(str(PARENT))
import camb
from camb.mts import MTSTwoField
import radiation_common as previous


def modest():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False), encoding='utf-8')


def finish(folder, report, script, extra=()):
    paths = [Path(script), ROOT / 'native_common.py', ROOT / 'native/camb/cambdll.dll',
        ROOT / 'native/camb/mts.py', ROOT / 'native/fortran/MTSTwoField.f90',
        PARENT / 'results/stage-integrity.json', PARENT / 'radiation_common.py'] + list(extra)
    report.update(state='complete', finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script), input_hashes={str(path): digest(path) for path in paths},
        local_camb_path=camb.__file__, camb_version=camb.__version__)
    write_json(folder / 'status.json', report)
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')


def custom_bridge(exact, target, frozen, species):
    start, end = math.log(.0003), math.log(.0004)

    def density(efold):
        nodes = np.asarray(efold)
        chosen = np.clip(nodes, previous.START, end)
        field, velocity, phase = exact.sol(chosen)
        rho = previous.HEAVY_MASS**2 * (field**2 + velocity**2)
        rho_n = -6 * previous.HEAVY_MASS**2 * velocity**2
        coordinate = np.clip((nodes - start) / (end - start), 0., 1.)
        weight = coordinate**3 * (10 - 15 * coordinate + 6 * coordinate**2)
        weight_n = 30 * coordinate**2 * (1 - coordinate)**2 / (end - start)
        log_dust = math.log(target) - 3 * nodes
        logrho = (1 - weight) * np.log(rho) + weight * log_dust
        slope = (1 - weight) * rho_n / rho - 3 * weight + weight_n * (log_dust - np.log(rho))
        value = np.exp(logrho)
        return value, value * slope

    return density


def load_model(table_path, seed_scale=1., initial_time_factor=1.):
    table = np.load(table_path)
    model = MTSTwoField()
    model.slow_mass_mpc = float(table['slow_mass_mpc'])
    model.heavy_mass_mpc = float(table['heavy_mass_mpc'])
    model.heavy_fraction = float(table['fraction'])
    model.heavy_exact_limit = .00028
    model.seed_scale = seed_scale
    model.initial_time_factor = initial_time_factor
    model.set_table('SetSlowTable', table['efold'], table['phi_s'], table['phidot_s'])
    if model.heavy_fraction:
        model.set_table('SetHeavyTable', table['heavy_efold'], table['phi_h'], table['phidot_h'])
        model.set_table('SetHeavyBackground', table['efold'], table['heavy_logrho_mpc'], table['heavy_w'])
    return model


def params_for(table_path, accuracy=1.5, seed_scale=1., initial_time_factor=1.):
    table = np.load(table_path)
    omega_m, slow_mass = previous.inherited_parameters()
    params = previous.base_params(omega_m, float(table['fraction']))
    params.DarkEnergy = load_model(table_path, seed_scale, initial_time_factor)
    params.set_accuracy(AccuracyBoost=accuracy)
    return params
