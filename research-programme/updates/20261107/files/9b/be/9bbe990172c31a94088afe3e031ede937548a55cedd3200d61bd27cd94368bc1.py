from __future__ import annotations
import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PREVIOUS = BRANCH / 'eos-coupled-photon-gas-20261026'
THERMO = BRANCH / 'whole-history-thermodynamic-stress-20261026'
sys.path.insert(0, str(PREVIOUS))
import common229 as prior
from common229 import np, math, json, mp, sp, read, write, digest, register, check, relative, now, modest, save_npz
from scipy import linalg, optimize, interpolate
from datetime import datetime
import time
sys.path.insert(0, str(THERMO))
from gravity228 import state_at_scale
SEAL = '1b852f8d80b4c19bf8f5eed800df7d86c5d253ce522d53074d9a902900713577'
START = '2026-10-26T18:14:27+00:00'


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
    write(ROOT / 'configuration.json', dict(stage=230, turn_start=START, frozen_at=now(), previous_goal_turn='progress',
        previous_seal=SEAL, models=['heavy', 'cold'], counts=[3200, 6400], chunk_steps=256,
        identity_tolerance=1e-7, root_tolerance=1e-10, budget_tolerance=1e-8, refinement_tolerance=.01,
        maximum_workers=2, numerical_threads=1, bank_changed=False, original_tolerances_changed=False,
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


class System(prior.System):
    def __init__(self, model, count, inputs):
        super().__init__(model, count, inputs)
        self.mass = self.background.parent.masses
        self.initial_parent = state_at_scale(self.background, self.background.start_scale)
        self.initial_D = float(self.eos['delta_A'][0])
        self.effective_mass = np.triu(self.basis.mass) + np.triu(self.basis.mass, 1).T

    def reference_density(self, scale):
        parent = self.background.parent
        return parent.radiation / scale**4 + (parent.baryons + parent.cold) / scale**3


def field_solve(alpha, omega, history):
    denominator = alpha * (alpha + 2) + omega**2
    return np.vstack([((alpha + 2) * history[0] + omega * history[1]) / denominator,
                      (alpha * history[1] - omega * history[0]) / denominator])


def field_pair(alpha, omega_base, base, delta_history, fraction):
    omega_new = omega_base / (1 + fraction)
    delta_omega = -omega_base * fraction / (1 + fraction)
    rhs = delta_history + np.vstack([delta_omega * base[1], -delta_omega * base[0]])
    return field_solve(alpha, omega_new, rhs)


def field_log_derivative(alpha, omega, fields):
    return field_solve(alpha, omega, np.vstack([-omega * fields[1], omega * fields[0]]))


class Step:
    def __init__(self, system, index, state, previous):
        self.system, self.index = system, index
        self.scale = system.background.start_scale * math.exp(float(system.coordinates[index]))
        self.alpha = (1. if index == 1 else 1.5) / system.step
        self.histories = {key: value / system.step if index == 1 else (2 * value - .5 * previous[key]) / system.step for key, value in state.items()}
        local = system.background.at(float(system.coordinates[index]))
        self.stiffness = system.ladder.at(local['thermal_parameter'], 0) - system.emission.at(local['thermal_parameter'], 'dcbr')
        self.effective_stiffness = np.triu(self.stiffness) + np.triu(self.stiffness, 1).T
        self.column = self.stiffness @ system.basis.temperature
        self.opacity = system.background.parent.opacity_constant / self.scale**2
        self.photon = system.background.parent.photons / self.scale**4
        self.base_density = system.reference_density(self.scale)
        self.field_history = np.stack([system.mass[:, None] * self.histories['fields'][0], self.histories['fields'][1] / self.scale])
        self.capacity = float(system.eos['C'][index])
        self.excess = float(system.eos['delta_A'][index])
        self.capacity_delta = float(system.eos['delta_C'][index])
        self.evaluations = 0

    def thermal(self, hubble, kind, nr=None, fraction=0.):
        system, alpha, heat = self.system, self.alpha, self.system.heat
        rate = self.opacity / hubble
        matrix = alpha * system.effective_mass - rate * self.effective_stiffness
        column = 0 if kind == 'NR' else 1
        vector = self.histories['profiles'][:, column]
        rhs = system.basis.mass @ vector
        if kind != 'NR':
            delta_rate = -nr['rate'] * fraction / (1 + fraction)
            rhs = rhs + delta_rate * (self.effective_stiffness @ nr['profile'] - self.column * nr['gas'])
        factor = linalg.cho_factor(matrix, lower=False)
        solved = linalg.cho_solve(factor, np.column_stack([rhs, -rate * self.column]))
        free, response = solved[:, 0], solved[:, 1]
        free_rate = float(system.basis.energy @ (alpha * free - vector))
        response_energy = float(system.basis.energy @ response)
        capacity = 1. if kind == 'NR' else self.capacity
        denominator = heat * capacity * (alpha - 1) + 2 * heat + alpha * response_energy
        if kind == 'NR':
            numerator = heat * self.histories['gas'][0] - 1 - free_rate
            forcing = 0.
        else:
            forcing = self.excess + heat * self.capacity_delta * nr['gas']
            numerator = self.histories['delta_heat'] - (alpha - 1) * forcing - free_rate
        gas = float(numerator / denominator)
        profile = free + response * gas
        thermal_heat = 1 + heat * gas if kind == 'NR' else forcing + heat * capacity * gas
        energy = float(system.basis.energy @ profile)
        total_profile = profile if kind == 'NR' else nr['profile'] + profile
        total_gas = gas if kind == 'NR' else nr['gas'] + gas
        force = -rate * (self.effective_stiffness @ total_profile - self.column * total_gas)
        free_log = linalg.cho_solve(factor, force)
        gas_log = -alpha * float(system.basis.energy @ free_log) / denominator
        q_log = heat**2 * (capacity - 2) * gas_log / alpha
        self.evaluations += 1
        return dict(profile=profile, gas=gas, U=thermal_heat, E=energy, q=heat * (energy + thermal_heat),
                    q_log=q_log, gas_log=gas_log, rate=rate, denominator=denominator, capacity=capacity)

    def no_heat(self):
        history = self.field_history[:, :, 0]
        maximum_field = float(np.sum(history**2) / (2 * self.alpha**2))
        lower = self.scale * math.sqrt(self.base_density / 3)
        upper = self.scale * math.sqrt((self.base_density + maximum_field) / 3)
        def equation(hubble):
            values = field_solve(self.alpha, self.scale * self.system.mass / hubble, history)
            return hubble**2 - self.scale**2 * (self.base_density + np.sum(values**2) / 2) / 3
        if upper == lower:
            hubble = lower
        else:
            hubble = optimize.brentq(equation, lower * (1 - 1e-14), upper * (1 + 1e-14), xtol=1e-300, rtol=1e-14)
        fields = field_solve(self.alpha, self.scale * self.system.mass / hubble, history)
        return hubble, fields, float(equation(hubble) / hubble**2)

    def paired_root(self, hubble_base, fields_base, kind, nr=None):
        system = self.system
        amplitude = system.heat if kind == 'NR' else system.heat * system.initial_D
        column = 1 if kind == 'NR' else 2
        history = self.field_history[:, :, column]
        omega_base = self.scale * system.mass / hubble_base
        cache = {}
        def evaluate(normalized):
            normalized = float(normalized)
            if normalized not in cache:
                fraction = amplitude * normalized
                if 1 + fraction <= 0:
                    raise ValueError('Nonpositive expansion branch')
                hubble = hubble_base * (1 + fraction)
                delta_fields = field_pair(self.alpha, omega_base, fields_base, history, fraction)
                total_fields = fields_base + delta_fields
                thermal = self.thermal(hubble, kind, nr, fraction)
                delta_density = float(np.sum(fields_base * delta_fields + .5 * delta_fields**2)) + self.photon * thermal['q']
                residual = normalized * (2 + fraction) - self.scale**2 * (delta_density / amplitude) / (3 * hubble_base**2)
                field_log = field_log_derivative(self.alpha, self.scale * system.mass / hubble, total_fields)
                density_log = float(np.sum(total_fields * field_log)) + self.photon * thermal['q_log']
                jacobian = 2 * (1 + fraction) - self.scale**2 * density_log / (3 * hubble_base**2 * (1 + fraction))
                cache[normalized] = dict(fraction=fraction, normalized=normalized, hubble=hubble, fields=delta_fields,
                    thermal=thermal, residual=float(residual), jacobian=float(jacobian), density_log=density_log)
            return cache[normalized]
        width = 2.
        for attempt in range(12):
            left, right = evaluate(-width), evaluate(width)
            if left['residual'] <= 0 <= right['residual']:
                break
            width *= 2
        else:
            raise RuntimeError('No bracket for the retained positive expansion branch')
        root = optimize.brentq(lambda value: evaluate(value)['residual'], -width, width, xtol=1e-13, rtol=1e-13)
        result = dict(evaluate(root))
        result['minimum_sampled_jacobian'] = min(item['jacobian'] for item in cache.values())
        result['maximum_sampled_fraction'] = max(abs(item['fraction']) for item in cache.values())
        result['bracket'] = [-width, width]
        result['evaluate'] = evaluate
        if result['minimum_sampled_jacobian'] <= 0 or abs(result['residual']) > 1e-10:
            raise RuntimeError('Unresolved shared-H branch or root residual')
        return result

    def advance(self):
        hubble0, fields0, residual0 = self.no_heat()
        nr = self.paired_root(hubble0, fields0, 'NR')
        eos = self.paired_root(nr['hubble'], fields0 + nr['fields'], 'EOS', nr['thermal'])
        energy_fields = np.stack([fields0, nr['fields'], eos['fields']], axis=2)
        fields = np.stack([energy_fields[0] / self.system.mass[:, None], energy_fields[1] * self.scale])
        profiles = np.column_stack([nr['thermal']['profile'], eos['thermal']['profile']])
        gas = np.array([nr['thermal']['gas'], eos['thermal']['gas']])
        delta_heat = np.asarray(eos['thermal']['U'])
        work_source = np.array([1 + self.system.heat * gas[0], 2 * self.system.heat * gas[1] - delta_heat])
        work = (self.histories['work'] + work_source) / self.alpha
        clock_source = np.array([1 / hubble0, -nr['fraction'] / (hubble0 * (1 + nr['fraction'])),
                                -eos['fraction'] / (nr['hubble'] * (1 + eos['fraction']))])
        clocks = (self.histories['clocks'] + np.vstack([clock_source, self.scale * clock_source])) / self.alpha
        state = dict(profiles=profiles, gas=gas, delta_heat=delta_heat, work=work, fields=fields, clocks=clocks)
        diagnostics = dict(hubble0=hubble0, fraction_NR=nr['fraction'], fraction_EOS=eos['fraction'],
            root_residual_NR=nr['residual'], root_residual_EOS=eos['residual'], root_residual0=residual0,
            minimum_jacobian=min(nr['minimum_sampled_jacobian'], eos['minimum_sampled_jacobian']), evaluations=self.evaluations,
            nr=nr, eos=eos)
        return state, diagnostics


def initial(system):
    state = prior.initial(system)
    fields = np.zeros((2, 2, 3))
    fields[0, :, 0] = system.initial_parent['fields']
    fields[1, :, 0] = system.initial_parent['prime']
    state.update(fields=fields, clocks=np.zeros((2, 3)))
    scale = system.background.start_scale
    density = system.reference_density(scale) + np.sum(fields[1, :, 0]**2 / scale**2 + system.mass**2 * fields[0, :, 0]**2) / 2
    photon = system.background.parent.photons / scale**4
    ratio_NR = system.heat * photon / density
    fraction_NR = ratio_NR / (math.sqrt(1 + ratio_NR) + 1)
    ratio_EOS = system.heat * system.initial_D * photon / (density + system.heat * photon)
    fraction_EOS = ratio_EOS / (math.sqrt(1 + ratio_EOS) + 1)
    diagnostics = dict(hubble0=scale * math.sqrt(density / 3), fraction_NR=fraction_NR, fraction_EOS=fraction_EOS,
        root_residual_NR=0., root_residual_EOS=0., root_residual0=0., minimum_jacobian=2., evaluations=0)
    return state, diagnostics


def packet_row(system, index, state, diagnostics):
    thermal = prior.packet_row(system, index, state)
    return np.r_[thermal, diagnostics['hubble0'], diagnostics['fraction_NR'], diagnostics['fraction_EOS'],
        diagnostics['root_residual0'], diagnostics['root_residual_NR'], diagnostics['root_residual_EOS'],
        diagnostics['minimum_jacobian']]
