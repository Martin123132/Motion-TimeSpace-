from __future__ import annotations

import math
import numpy as np
from scipy import interpolate, optimize
from stage_common import *

camb, previous = native_imports()
from camb.mts import MTSTwoField

BACKGROUND = PARENT / 'runs/backgrounds/heavy.npz'
REFERENCE = PARENT / 'runs/final-bg8-start/heavy.npz'
MODES = np.array([.03, .1, 1., 5.])


def params_for(table_path, accuracy=2.5, background_boost=8., start_factor=.5, raw=False):
    table = np.load(table_path)
    omega_m, _ = previous.inherited_parameters()
    params = previous.base_params(omega_m, float(table['fraction']))
    model = MTSTwoField()
    model.slow_mass_mpc = float(table['slow_mass_mpc'])
    model.heavy_mass_mpc = float(table['heavy_mass_mpc'])
    model.heavy_fraction = float(table['fraction'])
    model.heavy_exact_limit = .00028
    model.initial_time_factor = start_factor
    model.set_table('SetSlowTable', table['efold'], table['phi_s'], table['phidot_s'])
    if model.heavy_fraction:
        model.set_table('SetHeavyTable', table['heavy_efold'], table['phi_h'], table['phidot_h'])
        model.set_table('SetHeavyBackground', table['efold'], table['heavy_logrho_mpc'], table['heavy_w'])
        if 'matching_scale' in table:
            model.matching_scale = float(table['matching_scale'])
            model.matching_density = float(table['matching_density'])
            model.matching_raw = float(raw)
            model.set_table('SetMatching', table['modes'], table['matching_delta'], table['matching_momentum'])
    params.DarkEnergy = model
    params.set_accuracy(AccuracyBoost=accuracy)
    params.Accuracy.BackgroundTimeStepBoost = background_boost
    return params


def native_hashes():
    return [ROOT / 'matching_common.py', ROOT / 'native/camb/cambdll.dll', ROOT / 'native/camb/mts.py',
        ROOT / 'native/camb/model.py', ROOT / 'native/fortran/MTSTwoField.f90',
        ROOT / 'native/fortran/equations.f90', ROOT / 'native/fortran/camb_python.f90',
        ROOT.parent / 'radiation-and-slow-field-transfer-20261007/radiation_common.py']
