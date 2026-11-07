from __future__ import annotations

import os
for variable in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS']:
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from pathlib import Path
from datetime import datetime, timezone
import argparse
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PARENT = BRANCH / 'local-quarter-step-gas-curvature-20261020'
PARENT_SHA = '12d622c87c03cf8426515d0c4a2e888bc669a1ed74998a21ad8c289854016fbd'
STARTED = '2026-10-20T22:26:15+00:00'
sys.path.insert(0, str(PARENT))
import quarter_step_stage183 as prior
source, saved, np, mp, native, linear = prior.source, prior.saved, prior.np, prior.mp, prior.native, prior.linear
read, write, check = prior.read, prior.write, prior.check
HALF = prior.PARENT
ENERGY = prior.prior.PARENT
MODELS = ['heavy', 'cold']
GRIDS = ['native', 'half', 'quarter']
QUANTITIES = ['coarse_curvature', 'fine_curvature', 'width_discrepancy']


def authenticate():
    seal_path = PARENT / 'results/stage-integrity.json'
    assert saved.digest(seal_path) == PARENT_SHA
    seal = read(seal_path)
    paths = dict(seal['consumed_and_immediate_rehashed'])
    paths.update({str(PARENT / name): checksum for name, checksum in seal['file_hashes'].items()})
    paths[str(seal_path)] = PARENT_SHA
    for filename, checksum in paths.items():
        assert saved.digest(filename) == checksum, filename
    return paths


def history(model, grid):
    owner = PARENT if grid == 'quarter' else HALF
    path = owner / 'histories' / model / grid / 'history.npz'
    with np.load(path) as packet:
        return {name: packet[name].copy() for name in packet.files}


class Operators:
    def __init__(self, model, ladder):
        self.ladder = ladder
        self.basis = ladder.basis
        self.background = native.thermal_wave.thermal.ThermalBackground(model)
        self.emission = native.NonlocalEmission(self.basis, self.background, 'nonlocal-leading', native.ROOT / 'banks/s960-i256')
        knot = read(ENERGY / 'results/bank-knot.json')
        self.index = knot['nearest_index']
        self.theta = float(ladder.temperatures[self.index])
        self.anchor = float(history(model, 'quarter')['coordinates'][0])
        self.low = (ladder.blocks[self.index] - ladder.blocks[self.index - 1]) / (ladder.temperatures[self.index] - ladder.temperatures[self.index - 1])
        self.high = (ladder.blocks[self.index + 1] - ladder.blocks[self.index]) / (ladder.temperatures[self.index + 1] - ladder.temperatures[self.index])
        self.inputs = set(ladder.inputs) | set(self.emission.inputs) | {self.background.parent.source, self.background.native_constants}
        assert self.background.at(self.anchor)['thermal_parameter'] == self.theta == knot['anchor_theta']
        relative = np.linalg.norm(self.high - self.low) / max(np.linalg.norm(self.low), np.linalg.norm(self.high))
        assert relative == knot['relative_matrix_slope_jump']

    def at(self, coordinate, side=None):
        local = self.background.at(coordinate)
        theta = local['thermal_parameter']
        rate = local['coefficient'] / theta
        scattering = self.ladder.at(theta, 0)
        damping = self.emission.at(theta, 'dcbr')
        current = rate * (scattering - damping)
        delta = rate * (theta - self.theta) * (self.low - self.high) if coordinate > self.anchor else np.zeros_like(current)
        return current, current - delta, delta

    def derivatives(self, coordinate, side=None):
        local = self.background.at(coordinate)
        theta = local['thermal_parameter']
        rate = local['coefficient'] / theta
        background = self.background.parent
        physical = background.at(local['moment'])
        scale = physical['scale']
        fields, prime = physical['fields'], physical['prime']
        radiation = physical['photon'] + physical['neutrino']
        matter = physical['baryon'] + physical['cold']
        kinetic = float(np.sum(prime**2 / scale**2))
        density = radiation + matter + .5 * (kinetic + float(np.sum(background.masses**2 * fields**2)))
        kinetic_prime = -6 * kinetic - 2 * float(np.sum(background.masses**2 * fields * prime)) / physical['hubble']
        slope = -(4 * radiation + 3 * matter + 3 * kinetic) / (2 * density)
        slope_prime = -(-16 * radiation - 9 * matter + 3 * kinetic_prime) / (2 * density) - 2 * slope**2
        rate_prime = rate * (-3 - slope)
        rate_second = rate * ((-3 - slope)**2 - slope_prime)
        bank = self.ladder.at(theta, 0)
        bank_slope = self.high if (side == 'warm' or (side is None and theta >= self.theta)) else self.low
        dc = native.integrated_dc.DC_CONSTANT * theta**2 * self.emission.nonlocal_matrix
        damping = dc + self.emission.interpolator(math.log(theta))
        damping_prime = -2 * dc - self.emission.interpolator(math.log(theta), 1)
        damping_second = 4 * dc + self.emission.interpolator(math.log(theta), 2)
        difference = bank - damping
        first = -theta * bank_slope - damping_prime
        second = theta * bank_slope - damping_second
        return rate * difference, rate_prime * difference + rate * first, rate_second * difference + 2 * rate_prime * first + rate * second


def prepare():
    assert not (ROOT / 'configuration.json').exists()
    paths = authenticate()
    config = read(PARENT / 'configuration.json')
    config.update(stage=184, started_utc=STARTED, parent_seal_sha256=PARENT_SHA,
        grids=GRIDS, finite_width=.01, anchor_state='saved quarter-step history',
        prediction_status='post-test equation-based diagnostic, no fitted coefficient or new independent holdout',
        counterfactual='warm-side secant continuation after anchor only; original bank unchanged',
        prior_bookmark_normalized_sha256={str(path): hashlib.sha256(path.read_text(encoding='utf-8').encode()).hexdigest()
            for path in [BRANCH / 'RESUME-CURRENT.md', BRANCH.parent / 'CURRENT_LOCAL_RESUME.md']})
    write(ROOT / 'configuration.json', config)
    write(ROOT / 'authenticated-inputs.json', paths)
    write(ROOT / 'progress.json', dict(state='prepared'))
    print(json.dumps(dict(authenticated_paths=len(paths))), flush=True)


def mp_matrix(array):
    return mp.matrix([[mp.mpf(float(value)) for value in row] for row in array])


def mp_vector(array):
    return mp.matrix([mp.mpf(float(value)) for value in array])


def predictions():
    assert not (ROOT / 'results/frozen-predictions.json').exists()
    ladder = native.infrared_ladder.InfraredLadder(native.BACKGROUND / 'banks/infrared96-q700')
    basis = ladder.basis
    checks, records, operators = [], [], {model: Operators(model, ladder) for model in MODELS}
    inputs = read(ROOT / 'authenticated-inputs.json')
    for operator in operators.values():
        for path in operator.inputs:
            assert inputs[str(path)] == saved.digest(path)
    for digits in [80, 100]:
        with mp.workdps(digits):
            mass = mp_matrix(basis.mass)
            decomposition, permutation = mp.mp.LU_decomp(mass)
            transpose_decomposition, transpose_permutation = mp.mp.LU_decomp(mass.T)
            def solve(right):
                return mp.mp.U_solve(decomposition, mp.mp.L_solve(decomposition, right, permutation))
            energy = mp_vector(basis.energy)
            dual = mp.mp.U_solve(transpose_decomposition, mp.mp.L_solve(transpose_decomposition, energy, transpose_permutation)).T
            template = mp_vector(basis.temperature)
            for model, operator in operators.items():
                packet = history(model, 'quarter')
                coordinate, profiles, gas = packet['expansion'], packet['profiles'], packet['temperature_scaled']
                targets = packet['coordinates']
                temperatures = ladder.temperatures
                index = operator.index
                low = (mp_matrix(ladder.blocks[index]) - mp_matrix(ladder.blocks[index - 1])) / (mp.mpf(float(temperatures[index])) - mp.mpf(float(temperatures[index - 1])))
                high = (mp_matrix(ladder.blocks[index + 1]) - mp_matrix(ladder.blocks[index])) / (mp.mpf(float(temperatures[index + 1])) - mp.mpf(float(temperatures[index])))
                probe_records = []
                for probe_index, target in enumerate(targets):
                    profile = mp_vector(np.array([np.interp(target, coordinate, profiles[:, column]) for column in range(96)]))
                    stored_gas = mp.mpf(float(np.interp(target, coordinate, gas)))
                    matrices = operator.derivatives(float(target))
                    direct, _, _ = operator.at(float(target))
                    check(checks, f'{model}:{digits}:{probe_index}: analytic emission reduction', np.linalg.norm(matrices[0] - direct) / np.linalg.norm(direct))
                    stiffness, first, second = [mp_matrix(matrix) for matrix in matrices]
                    heat = mp.mpf(operator.background.chi)
                    capacity = heat - (dual * stiffness * template)[0]
                    equilibrium = -(1 + (dual * stiffness * profile)[0]) / capacity
                    departure = profile - template * equilibrium
                    photon_first = solve(stiffness * departure)
                    gas_first = -(dual * (first * departure + stiffness * photon_first))[0] / capacity
                    departure_first = photon_first - template * gas_first
                    photon_second = solve(first * departure + stiffness * departure_first)
                    gas_second = -(dual * (second * departure + 2 * first * departure_first + stiffness * photon_second))[0] / capacity
                    row = dict(probe=probe_index, u=float(target), stored_gas=str(stored_gas), equilibrium_gas=str(equilibrium),
                        equilibrium_gap=str(equilibrium - stored_gas), effective_capacity=str(capacity), relaxation_width=str(heat / capacity),
                        gas_first=str(gas_first), gas_second=str(gas_second))
                    if probe_index == 0:
                        local = operator.background.at(float(target))
                        rate = mp.mpf(local['coefficient'] / local['thermal_parameter'])
                        jump = rate * mp.mpf(operator.theta) * (high - low)
                        photon_jump = solve(jump * (profile - template * stored_gas))
                        exact_gas_jump = -(energy.T * photon_jump)[0] / heat
                        slaved_jump = -(dual * jump * departure)[0] / capacity
                        finite_state_jump = -(dual * jump * (profile - template * stored_gas))[0] / capacity
                        width = mp.mpf('.01')
                        relaxation = heat / capacity
                        correction = slaved_jump * relaxation / width**2 * (3 + mp.exp(-width / relaxation) - 4 * mp.exp(-width / (2 * relaxation)))
                        check(checks, f'{model}:{digits}: exact corner energy exchange', (energy.T * photon_jump)[0] + heat * exact_gas_jump)
                        check(checks, f'{model}:{digits}: frozen relaxation/probe width', relaxation / (width / 2), .01, 'scale_separation')
                        check(checks, f'{model}:{digits}: slaved versus finite-state jump', (slaved_jump - finite_state_jump) / finite_state_jump, .01, 'source')
                        row.update(continuous_gas_curvature_jump=str(exact_gas_jump), slaved_slope_jump=str(slaved_jump),
                            corner_width_prediction=str(-slaved_jump / width), finite_capacity_scaling_correction=str(correction),
                            warm_gas_first=str(gas_first))
                        alternate_first = first + jump
                        cool_gas_first = -(dual * (alternate_first * departure + stiffness * photon_first))[0] / capacity
                        check(checks, f'{model}:{digits}: slope-jump algebra', (cool_gas_first - gas_first - slaved_jump) / slaved_jump)
                        row['cool_gas_first'] = str(cool_gas_first)
                    probe_records.append(row)
                record = dict(model=model, digits=digits, probes=probe_records)
                records.append(record)
                print(json.dumps(dict(model=model, digits=digits, jump=probe_records[0]['slaved_slope_jump'],
                    predicted_width=probe_records[0]['corner_width_prediction'], second=[float(row['gas_second']) for row in probe_records])), flush=True)
    for model in MODELS:
        lower = next(row for row in records if row['model'] == model and row['digits'] == 80)
        upper = next(row for row in records if row['model'] == model and row['digits'] == 100)
        with mp.workdps(100):
            for probe_index in range(5):
                for key in ['gas_first', 'gas_second', 'equilibrium_gas']:
                    first = mp.mpf(lower['probes'][probe_index][key])
                    second = mp.mpf(upper['probes'][probe_index][key])
                    check(checks, f'{model}:{probe_index}: 80/100 {key}', abs(first - second) / max(abs(second), mp.mpf('1e-300')))
    write(ROOT / 'results/frozen-predictions.json', dict(records=records, checks=checks,
        source_prediction_tolerance=.01, identity_tolerance=1e-10,
        new_fitted_parameters=0, original_history_replaced=False, independent_observational_holdout=False))
    np.savez_compressed(ROOT / 'results/saved-secants.npz', temperatures=ladder.temperatures,
        lower=operators['heavy'].low, upper=operators['heavy'].high)
    write(ROOT / 'bank-inputs.json', {str(path): saved.digest(path) for operator in operators.values() for path in operator.inputs})
    write(ROOT / 'progress.json', dict(state='predictions_frozen'))


def bdf_terms(current, previous, step, ordinal, divisor):
    if ordinal == 1 and divisor != 1:
        ratio = 1 / divisor
        alpha = (1 + 2 * ratio) / ((1 + ratio) * step)
        past = ((1 + ratio) * current - ratio**2 / (1 + ratio) * previous) / step
    else:
        alpha = 1.5 / step
        past = (2 * current - .5 * previous) / step
    return alpha, past


def counterfactual():
    assert read(ROOT / 'progress.json')['state'] == 'predictions_frozen'
    frozen_hash = saved.digest(ROOT / 'results/frozen-predictions.json')
    ladder = native.infrared_ladder.InfraredLadder(native.BACKGROUND / 'banks/infrared96-q700')
    basis = ladder.basis
    for model in MODELS:
        operator = Operators(model, ladder)
        heat = operator.background.chi
        for grid, divisor in zip(GRIDS, [1, 2, 4]):
            packet = history(model, grid)
            folder = ROOT / 'counterfactuals' / model / grid
            folder.mkdir(parents=True, exist_ok=False)
            step = float(packet['step'])
            profile, previous_profile = packet['initial_profile'].copy(), packet['initial_previous_profile'].copy()
            gas, previous_gas = float(packet['initial_gas']), float(packet['initial_previous_gas'])
            difference, previous_difference = np.zeros(96), np.zeros(96)
            gas_difference, previous_gas_difference = 0., 0.
            profiles, gases = [profile.copy()], [gas]
            differences, gas_differences = [difference.copy()], [0.]
            rows = []
            for ordinal, coordinate in enumerate(packet['expansion'][1:], 1):
                _, reference, jump = operator.at(float(coordinate))
                alpha, vector = bdf_terms(profile, previous_profile, step, ordinal, divisor)
                _, scalar = bdf_terms(gas, previous_gas, step, ordinal, divisor)
                _, difference_vector = bdf_terms(difference, previous_difference, step, ordinal, divisor)
                _, difference_scalar = bdf_terms(gas_difference, previous_gas_difference, step, ordinal, divisor)
                original_departure = packet['profiles'][ordinal] - basis.temperature * packet['temperature_scaled'][ordinal]
                forcing = jump @ original_departure
                thermal = -reference @ basis.temperature
                solution = linear.solve(alpha * basis.mass - reference,
                    np.column_stack([basis.mass @ vector, thermal, basis.mass @ difference_vector + forcing]), assume_a='pos')
                free, response, free_difference = solution[:, 0], solution[:, 1], solution[:, 2]
                denominator = heat * (alpha + 1) + alpha * (basis.energy @ response)
                new_gas = (heat * scalar - 1 - basis.energy @ (alpha * free - vector)) / denominator
                new_gas_difference = (heat * difference_scalar - basis.energy @ (alpha * free_difference - difference_vector)) / denominator
                new_profile = free + response * new_gas
                new_difference = free_difference + response * new_gas_difference
                residual = alpha * basis.mass @ new_difference - basis.mass @ difference_vector - reference @ (new_difference - basis.temperature * new_gas_difference) - forcing
                scale = max(np.linalg.norm(forcing), np.linalg.norm(reference @ (new_difference - basis.temperature * new_gas_difference)), 1e-300)
                rows.append(dict(u=float(coordinate), forced_equation_relative=float(np.linalg.norm(residual) / scale),
                    forced_gas_balance=float(basis.energy @ (alpha * new_difference - difference_vector) + heat * ((alpha + 1) * new_gas_difference - difference_scalar)),
                    reconstruction_gas_absolute=float(abs(new_gas + new_gas_difference - packet['temperature_scaled'][ordinal])),
                    reconstruction_profile_relative=float(np.linalg.norm(new_profile + new_difference - packet['profiles'][ordinal]) / np.linalg.norm(packet['profiles'][ordinal]))))
                previous_profile, profile = profile, new_profile
                previous_gas, gas = gas, float(new_gas)
                previous_difference, difference = difference, new_difference
                previous_gas_difference, gas_difference = gas_difference, float(new_gas_difference)
                profiles.append(profile.copy())
                gases.append(gas)
                differences.append(difference.copy())
                gas_differences.append(gas_difference)
            np.savez_compressed(folder / 'history.npz', expansion=packet['expansion'], coordinates=packet['coordinates'],
                reference_profiles=np.array(profiles), reference_gas=np.array(gases), forced_profiles=np.array(differences), forced_gas=np.array(gas_differences), step=step)
            write(folder / 'status.json', dict(state='complete', updates=len(rows), diagnostics=rows,
                original_bank_changed=False, frozen_prediction_sha256=frozen_hash))
            print(json.dumps(dict(model=model, grid=grid, updates=len(rows),
                reconstruction=max(row['reconstruction_gas_absolute'] for row in rows))), flush=True)
    assert saved.digest(ROOT / 'results/frozen-predictions.json') == frozen_hash
    write(ROOT / 'progress.json', dict(state='counterfactual_complete', frozen_prediction_sha256=frozen_hash))


if __name__ == '__main__':
    source.modest()
    parser = argparse.ArgumentParser()
    parser.add_argument('phase', choices=['prepare', 'predict', 'counterfactual'])
    arguments = parser.parse_args()
    dict(prepare=prepare, predict=predictions, counterfactual=counterfactual)[arguments.phase]()
