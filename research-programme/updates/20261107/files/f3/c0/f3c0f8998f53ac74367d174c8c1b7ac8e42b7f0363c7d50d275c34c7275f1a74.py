from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_compensation_complex_oracle_v2_20260928 import complex_mixed_wave
from copy import copy
from time import perf_counter
import numpy as np


def full_oracle(engine, solver, progress):
    radius = solver.nodes.ravel()
    result = np.zeros(len(radius))
    for start in range(0, len(radius), 32):
        if perf_counter() > engine.loads.deadline:
            raise RuntimeError('Safe full-grid independent derivative boundary')
        section = slice(start, start + 32)
        result[section] = complex_mixed_wave(engine, radius[section], 1j * 1e-25).imag / 1e-25
        if start % 8192 == 0:
            progress('independent-mixed-density-' + str(start) + '-of-' + str(len(radius)))
    return result


def resolved_control(engine, radius):
    control = copy(engine)
    nodes = engine.loads.knots
    offset = (nodes - nodes.min()) / (nodes.max() - nodes.min())
    labels = engine.owner.layer_rule.points / 2
    control.field_direction = .03 * (1 + .2 * labels[:, None]) * np.sin(2 * np.pi * offset)[None, :]
    control.field_direction_rate = .02 * (1 - .1 * labels[:, None]) * np.sin(np.pi * offset)[None, :]
    control.edges_direction = np.zeros_like(engine.edges_direction)
    control.source_direction = .01 * (1 + labels)
    unused, analytic = control.mixed_wave(radius)
    nonlinear = complex_mixed_wave(control, radius, 1j * 1e-25).imag / 1e-25
    return analytic, nonlinear
