from __future__ import annotations

import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PREVIOUS = BRANCH / 'whole-history-thermodynamic-stress-20261026'
sys.path.insert(0, str(PREVIOUS))
import run228 as prior
from eos228 import Mixture, particle_moments, radial_rule
from launch228 import windows_modest as modest
np, math, json, mp, sp = prior.np, prior.math, prior.json, prior.mp, prior.sp
read, write, digest, register, check, relative, now = prior.read, prior.write, prior.digest, prior.register, prior.check, prior.relative, prior.now
from scipy import linalg, interpolate
import time
from datetime import datetime
SEAL = 'c1fb57161bc2de99e1dc227bc1f75dad03286084d227d01e86ad70bb419758f3'
START = '2026-10-26T17:54:02+00:00'


def prepare():
    assert not (ROOT / 'configuration.json').exists()
    assert digest(PREVIOUS / 'results/stage-integrity.json') == SEAL
    seal = read(PREVIOUS / 'results/stage-integrity.json')
    assert seal['qualified']
    inputs = dict(seal['directly_consumed_inputs'])
    for name, expected in seal['file_hashes'].items():
        path = register(inputs, PREVIOUS / name)
        assert digest(path) == expected
    register(inputs, PREVIOUS / 'results/stage-integrity.json')
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=229, frozen_at=now(), turn_start=START,
        previous_goal_turn='progress', previous_seal=SEAL, models=['heavy', 'cold'], counts=[3200, 6400],
        chunk_steps=256, workers=2, numerical_threads=1, block_tolerance=1e-7,
        energy_tolerance=1e-8, refinement_tolerance=.01, prediction_tolerance=.01,
        heat_derivative_tolerance=1e-10, original_bank_changed=False, tolerances_changed=False,
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


def save_npz(path, **values):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    with temporary.open('wb') as handle:
        np.savez_compressed(handle, **values)
    temporary.replace(path)


class System:
    def __init__(self, model, count, inputs):
        sys.path.insert(0, str(BRANCH / 'infrared-source-domain-20261008'))
        import nonlocal_dc
        self.background, self.mixture = prior.load_background(model, inputs)
        self.ladder = nonlocal_dc.infrared_ladder.InfraredLadder(BRANCH / 'emitting-thermal-background-20261008/banks/infrared96-q700')
        self.basis = self.ladder.basis
        self.emission = nonlocal_dc.NonlocalEmission(self.basis, self.background, 'nonlocal-leading', BRANCH / 'infrared-source-domain-20261008/banks/s960-i256')
        self.model, self.count = model, count
        self.heat = self.background.chi
        self.step = self.background.end / count
        self.coordinates = np.arange(count + 1) * self.step
        self.theta = self.background.theta0 / self.background.start_scale * np.exp(-self.coordinates)
        self.eos = self.mixture.state(self.theta)
        for path in [*self.ladder.inputs, *self.emission.inputs]:
            register(inputs, path)
        add_modules(inputs)

    def operator(self, index):
        local = self.background.at(float(self.coordinates[index]))
        rate = local['coefficient'] / local['thermal_parameter']
        stiffness = self.ladder.at(local['thermal_parameter'], 0) - self.emission.at(local['thermal_parameter'], 'dcbr')
        return rate, stiffness


def advance(system, index, state, previous):
    step, heat, basis = system.step, system.heat, system.basis
    rate, stiffness = system.operator(index)
    if index == 1:
        alpha, histories = 1 / step, {key: value / step for key, value in state.items()}
    else:
        alpha, histories = 1.5 / step, {key: (2 * value - .5 * previous[key]) / step for key, value in state.items()}
    vector = histories['profiles']
    thermal = -rate * stiffness @ basis.temperature
    matrix = alpha * basis.mass - rate * stiffness
    solved = linalg.solve(matrix, np.column_stack([basis.mass @ vector, thermal]), assume_a='pos')
    free, response = solved[:, :2], solved[:, 2]
    free_energy_rate = basis.energy @ (alpha * free - vector)
    response_energy = float(basis.energy @ response)
    nr = (heat * histories['gas'][0] - 1 - free_energy_rate[0]) / (heat * (alpha + 1) + alpha * response_energy)
    excess = float(system.eos['delta_A'][index])
    capacity = float(system.eos['C'][index])
    capacity_delta = float(system.eos['delta_C'][index])
    forcing = excess + heat * capacity_delta * nr
    denominator = heat * capacity * (alpha - 1) + 2 * heat + alpha * response_energy
    delta = (histories['delta_heat'] - (alpha - 1) * forcing - free_energy_rate[1]) / denominator
    gas = np.array([nr, delta])
    profiles = free + response[:, None] * gas
    delta_heat = forcing + heat * capacity * delta
    work_sources = np.array([1 + heat * nr, 2 * heat * delta - delta_heat])
    work = (histories['work'] + work_sources) / alpha
    updated = dict(profiles=profiles, gas=gas, delta_heat=np.asarray(delta_heat), work=work)
    raw_equation = alpha * basis.mass @ profiles - basis.mass @ vector - rate * stiffness @ (profiles - basis.temperature[:, None] * gas)
    raw_scale = np.maximum(np.linalg.norm(rate * stiffness @ (profiles - basis.temperature[:, None] * gas), axis=0), 1e-30)
    diagnostics = dict(raw_relative=np.linalg.norm(raw_equation, axis=0) / raw_scale,
        alpha=alpha, histories=histories, matrix=matrix, thermal=thermal, forcing=forcing,
        nr=nr, denominator=denominator, free_energy_rate=free_energy_rate, response=response,
        capacity=capacity, vector=vector)
    return updated, diagnostics


def initial(system):
    return dict(profiles=np.zeros((system.basis.count, 2)), gas=np.zeros(2),
                delta_heat=np.asarray(system.eos['delta_A'][0]), work=np.zeros(2))


def packet_row(system, index, state):
    energy = system.basis.energy @ state['profiles']
    nr, delta = state['gas']
    heat = system.heat
    density = np.array([heat * (1 + energy[0] + heat * nr), heat * (energy[1] + state['delta_heat'])])
    pressure = np.array([heat * (energy[0] / 3 + 2 * (1 + heat * nr) / 3), heat * (energy[1] + 2 * heat * delta) / 3])
    return np.r_[system.coordinates[index], energy, nr, delta, state['delta_heat'], state['work'], density, pressure]
