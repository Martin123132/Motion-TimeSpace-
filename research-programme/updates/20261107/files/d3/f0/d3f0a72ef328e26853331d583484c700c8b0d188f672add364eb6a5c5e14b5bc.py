from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys

import numpy as np
import psutil
from scipy import integrate, interpolate

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
PARENT = BRANCH / 'matter-growth-response-20261006'
sys.dont_write_bytecode = True
sys.path.insert(0, str(PARENT))
import growth_common as late

MASS = late.SCALE_MASS
FRACTION = .5
AMPLITUDE = 1e-5
MODES = [(.1, 'adiabatic'), (1., 'adiabatic'), (5., 'adiabatic'), (5., 'field_isocurvature')]
SOURCE_NAMES = [
    '5194-Y5-R2FR-parent-canonical-scalar-perturbation-growth-and-compressed-CMB-gate.md',
    '5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-clock-adiabatic-radiation-transfer-and-patch-collapse-gate.md',
]
SOURCE_URLS = ['https://arxiv.org/abs/astro-ph/9506072', 'https://arxiv.org/abs/astro-ph/9811156', 'https://arxiv.org/abs/2201.10238']


def modest_process():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write_json(path, value):
    with Path(path).open('x', encoding='utf-8') as handle:
        json.dump(value, handle, indent=2, allow_nan=False)


def inputs():
    paths = [Path(__file__), Path(late.__file__), PARENT / 'results/stage-integrity.json',
             PARENT / 'results/scan/status.json', late.COSMO / 'results/comparison/status.json',
             Path(late.old.inherited.__file__), late.COSMO / 'cosmology_common.py']
    paths += [POST / name for name in SOURCE_NAMES]
    return {str(path): digest(path) for path in paths}


def save(label, script, report, extra_paths=()):
    folder = ROOT / 'results' / label
    folder.mkdir(parents=True, exist_ok=False)
    hashes = inputs()
    hashes.update({str(path): digest(path) for path in extra_paths})
    output = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(),
                  script_sha256=digest(script), input_hashes=hashes, source_urls=SOURCE_URLS, **report)
    write_json(folder / 'status.json', output)
    (folder / 'COMPLETE').write_text(output['time_utc'] + '\n', encoding='utf-8')
    return output


class Environment:
    def __init__(self):
        self.late = late.Background('ParentScalar_Lambda_zero')
        self.matter = self.late.omega_m
        self.radiation = late.old.inherited.OMEGA_R
        expansion2, _, _ = self.late.values(-5.)
        self.frozen_dark = expansion2 - self.matter * math.exp(15) - self.radiation * math.exp(20)

    def exact_values(self, efold, field, velocity):
        scale = math.exp(efold)
        cold_density = (1 - FRACTION) * self.matter / scale**3
        radiation_density = self.radiation / scale**4
        scalar_density = MASS**2 * (field**2 + velocity**2)
        expansion2 = cold_density + radiation_density + scalar_density + self.frozen_dark
        slope = (-1.5 * cold_density - 2 * radiation_density - 3 * MASS**2 * velocity**2) / expansion2
        return scale, cold_density, radiation_density, scalar_density, math.sqrt(expansion2), slope

    def fluid_values(self, efold):
        scale = math.exp(efold)
        matter_density = self.matter / scale**3
        radiation_density = self.radiation / scale**4
        if efold < -5:
            expansion2 = matter_density + radiation_density + self.frozen_dark
            slope = (-1.5 * matter_density - 2 * radiation_density) / expansion2
        else:
            expansion2, slope, _ = self.late.values(efold)
        return scale, matter_density, radiation_density, math.sqrt(expansion2), slope


def background_solution(environment, displacement, start_a=1e-9, end_a=.0006, tolerance=2e-10):
    expansion = environment.exact_values(math.log(start_a), displacement, 0.)[4]
    initial = [displacement, -MASS * displacement / (5 * expansion), MASS * start_a**2 / (2 * math.sqrt(environment.radiation))]

    def equation(efold, state):
        expansion = environment.exact_values(efold, state[0], state[1])[4]
        frequency = MASS / expansion
        return [frequency * state[1], -3 * state[1] - frequency * state[0], frequency]

    solution = integrate.solve_ivp(equation, (math.log(start_a), math.log(end_a)), initial,
        method='DOP853', rtol=tolerance, atol=tolerance * 1e-3, max_step=.05)
    assert solution.success, solution.message
    field, velocity, phase = solution.y[:, -1]
    expansion = environment.exact_values(math.log(end_a), field, velocity)[4]
    invariant = MASS**2 * end_a**3 * (field**2 + (velocity + 1.5 * expansion / MASS * field)**2)
    return invariant, solution


def calibrate(environment):
    displacement = .08
    target = FRACTION * environment.matter
    history = []
    for iteration in range(7):
        invariant, solution = background_solution(environment, displacement)
        residual = invariant / target - 1
        history.append(dict(iteration=iteration, displacement=displacement, late_action_density=invariant,
                            target=target, residual=residual, nfev=solution.nfev))
        print(dict(event='background_calibration', **history[-1]), flush=True)
        if abs(residual) < 2e-8:
            return displacement, history
        displacement *= math.sqrt(target / invariant)
    raise RuntimeError('Abundance normalization did not converge')


def early_initial(environment, displacement, start_a, modes):
    efold = math.log(start_a)
    _, cold_density, radiation_density, _, expansion, _ = environment.exact_values(efold, displacement, 0.)
    velocity = -MASS * displacement / (5 * expansion)
    phase = MASS * start_a**2 / (2 * math.sqrt(environment.radiation))
    field_ratio = (MASS / expansion)**2
    blocks = []
    for wave, preparation in modes:
        wave_ratio2 = (late.C_KM_S * wave / late.H0_KM_S_MPC / (start_a * expansion))**2
        if preparation == 'adiabatic':
            cold = AMPLITUDE * wave_ratio2
            cold_derivative = 2 * cold
            radiation = 4 * cold / 3
            radiation_velocity = AMPLITUDE * wave_ratio2**2 / 9
            field_delta = -displacement * field_ratio * cold / 105
            velocity_delta = 6 * field_delta * expansion / MASS
        else:
            field_delta = AMPLITUDE * displacement
            velocity_delta = (-wave_ratio2 / 3 - field_ratio / 5) * field_delta * expansion / MASS
            density_delta = 2 * MASS**2 * (displacement * field_delta + velocity * velocity_delta)
            cold = -density_delta / (4 * expansion**2)
            cold_derivative = 4 * cold
            radiation = 4 * cold / 3
            radiation_velocity = wave_ratio2 * radiation / 20
        density_delta = cold_density * cold + radiation_density * radiation + 2 * MASS**2 * (displacement * field_delta + velocity * velocity_delta)
        eta = -(cold_derivative + 1.5 * density_delta / expansion**2) / wave_ratio2
        block = np.array([cold, cold_derivative, radiation, radiation_velocity, field_delta, velocity_delta, eta])
        if preparation == 'adiabatic':
            block *= -4 * AMPLITUDE / eta
        blocks.extend(block.tolist())
    return np.array([displacement, velocity, phase] + blocks)


def exact_evolution(environment, displacement, start_a=1e-9, end_a=.0006, tolerance=2e-9, modes=MODES):
    wave_scales = np.array([(late.C_KM_S * wave / late.H0_KM_S_MPC)**2 for wave, _ in modes])

    def equation(efold, state):
        field, velocity, phase = state[:3]
        scale, cold_density, radiation_density, _, expansion, slope = environment.exact_values(efold, field, velocity)
        frequency = MASS / expansion
        blocks = state[3:].reshape(-1, 7)
        cold, cold_prime, radiation, radiation_velocity, delta_field, delta_velocity, eta = blocks.T
        wave_ratio2 = wave_scales / (scale * expansion)**2
        scalar_density_plus_pressure3 = 8 * MASS**2 * velocity * delta_velocity - 4 * MASS**2 * field * delta_field
        scalar_momentum = 2 * wave_scales * MASS * velocity * delta_field / (scale**2 * expansion)
        output = np.empty_like(blocks)
        output[:, 0] = cold_prime
        output[:, 1] = -(2 + slope) * cold_prime + 1.5 / expansion**2 * (cold_density * cold + 2 * radiation_density * radiation + scalar_density_plus_pressure3)
        output[:, 2] = 4 / 3 * (cold_prime - radiation_velocity)
        output[:, 3] = -(1 + slope) * radiation_velocity + wave_ratio2 * radiation / 4
        output[:, 4] = frequency * delta_velocity
        output[:, 5] = -3 * delta_velocity - (frequency + wave_ratio2 / frequency) * delta_field + velocity * cold_prime
        output[:, 6] = 1.5 / (expansion**2 * wave_ratio2) * (4 / 3 * radiation_density * radiation_velocity + scalar_momentum)
        return np.concatenate([[frequency * velocity, -3 * velocity - frequency * field, frequency], output.ravel()])

    solution = integrate.solve_ivp(equation, (math.log(start_a), math.log(end_a)), early_initial(environment, displacement, start_a, modes),
        method='DOP853', rtol=tolerance, atol=tolerance * 1e-6, max_step=.04, dense_output=True)
    assert solution.success, solution.message
    return solution


def extract_match(environment, solution, scale, modes=MODES, half_width=8 * math.pi):
    efold = math.log(scale)
    central = solution.sol(efold)
    phase = central[2]
    offsets = np.linspace(-half_width, half_width, 801)
    inverse = interpolate.PchipInterpolator(solution.y[2], solution.t)
    efolds = inverse(phase + offsets)
    assert min(efolds) >= solution.t[0] and max(efolds) <= solution.t[-1]
    states = solution.sol(efolds)
    scaled_offsets = offsets / half_width
    basis = np.column_stack([scaled_offsets**degree for degree in range(5)] +
                            [scaled_offsets**degree * trig(2 * (phase + offsets)) for degree in range(3) for trig in [np.cos, np.sin]] +
                            [np.cos(4 * (phase + offsets)), np.sin(4 * (phase + offsets))])
    field, velocity = states[:2]
    scales = np.exp(efolds)
    expansion = np.array([environment.exact_values(efolds[index], field[index], velocity[index])[4] for index in range(len(efolds))])
    scalar_density = MASS**2 * (field**2 + velocity**2)

    def average(values):
        return float(np.linalg.lstsq(basis, np.asarray(values), rcond=None)[0][0])

    abundance = average(scales**3 * scalar_density)
    matches = []
    for index, (wave, preparation) in enumerate(modes):
        cold, cold_prime, radiation, radiation_velocity, delta_field, delta_velocity, eta = states[3 + 7 * index:10 + 7 * index]
        wave_scale2 = (late.C_KM_S * wave / late.H0_KM_S_MPC)**2
        density_delta = 2 * MASS**2 * (velocity * delta_velocity + field * delta_field)
        pressure_delta = 2 * MASS**2 * (velocity * delta_velocity - field * delta_field)
        momentum = 2 * wave_scale2 * MASS * velocity * delta_field / (scales**2 * expansion)
        heavy_delta = average(scales**3 * density_delta) / abundance
        heavy_velocity = average(scales**3 * momentum) / abundance
        heavy_pressure = average(scales**3 * pressure_delta) / abundance
        values = [average(cold), average(cold_prime), average(radiation), average(radiation_velocity), heavy_delta, heavy_velocity, average(eta)]
        matched_expansion = environment.fluid_values(efold)[3]
        wave_ratio2 = wave_scale2 / (scale * matched_expansion)**2
        kappa2 = wave_scale2 / (scale * MASS)**2
        sound2 = kappa2 / (math.sqrt(1 + kappa2) + 1)**2
        closure_pressure = sound2 * (heavy_delta + 3 * heavy_velocity / wave_ratio2)
        norm = max(abs(heavy_delta), abs(heavy_velocity) / max(1., math.sqrt(wave_ratio2 * sound2)), AMPLITUDE * 1e-4)
        full_density = ((1 - FRACTION) * environment.matter / scales**3 * cold + environment.radiation / scales**4 * radiation + density_delta)
        eta_constraint = -(cold_prime + 1.5 * full_density / expansion**2) / (wave_scale2 / (scales * expansion)**2)
        constraint_error = float(np.max(abs(eta_constraint - eta))) / AMPLITUDE
        matches.append(dict(wave=wave, preparation=preparation, state=values, heavy_pressure_from_field=heavy_pressure,
            closure_pressure=closure_pressure, pressure_mismatch_over_perturbation_norm=abs(heavy_pressure - closure_pressure) / norm,
            Einstein_constraint_error_over_seed=constraint_error, mass_over_H=MASS / matched_expansion,
            k_over_aM=math.sqrt(kappa2), sound_speed2=sound2))
    return dict(scale=scale, half_width_in_mass_time=half_width, phase_center=float(phase),
        recovered_abundance=abundance, target_abundance=FRACTION * environment.matter,
        relative_abundance_error=abundance / (FRACTION * environment.matter) - 1,
        matches=matches)


def fluid_evolution(environment, match, modes=MODES, tolerance=2e-8, end_N=0.):
    wave_scales = np.array([(late.C_KM_S * wave / late.H0_KM_S_MPC)**2 for wave, _ in modes])
    initial = np.array([row['state'] for row in match['matches']]).ravel()

    def equation(efold, state):
        scale, matter_density, radiation_density, expansion, slope = environment.fluid_values(efold)
        cold_density, heavy_density = (1 - FRACTION) * matter_density, FRACTION * matter_density
        cold, cold_prime, radiation, radiation_velocity, heavy, heavy_velocity, eta = state.reshape(-1, 7).T
        wave_ratio2 = wave_scales / (scale * expansion)**2
        kappa2 = wave_scales / (scale * MASS)**2
        sound2 = kappa2 / (np.sqrt(1 + kappa2) + 1)**2
        pressure = sound2 * (heavy + 3 * heavy_velocity / wave_ratio2)
        output = np.empty((len(modes), 7))
        output[:, 0] = cold_prime
        output[:, 1] = -(2 + slope) * cold_prime + 1.5 / expansion**2 * (cold_density * cold + 2 * radiation_density * radiation + heavy_density * (heavy + 3 * pressure))
        output[:, 2] = 4 / 3 * (cold_prime - radiation_velocity)
        output[:, 3] = -(1 + slope) * radiation_velocity + wave_ratio2 * radiation / 4
        output[:, 4] = cold_prime - heavy_velocity - 3 * pressure
        output[:, 5] = -(2 + slope) * heavy_velocity + wave_ratio2 * pressure
        output[:, 6] = 1.5 / (expansion**2 * wave_ratio2) * (4 / 3 * radiation_density * radiation_velocity + heavy_density * heavy_velocity)
        return output.ravel()

    solution = integrate.solve_ivp(equation, (math.log(match['scale']), end_N), initial, method='DOP853',
        rtol=tolerance, atol=tolerance * 1e-5, max_step=.05, dense_output=True)
    assert solution.success, solution.message
    return solution


def cold_evolution(environment, start_a=1e-9, waves=(.1, 1., 5.), tolerance=2e-8):
    wave_scales = np.array([(late.C_KM_S * wave / late.H0_KM_S_MPC)**2 for wave in waves])
    scale, matter, radiation_density, expansion, _ = environment.fluid_values(math.log(start_a))
    initial = []
    for wave_scale in wave_scales:
        wave_ratio2 = wave_scale / (scale * expansion)**2
        cold = AMPLITUDE * wave_ratio2
        eta = -(2 * cold + 1.5 * (matter * cold + radiation_density * 4 * cold / 3) / expansion**2) / wave_ratio2
        initial.extend((np.array([cold, 2 * cold, 4 * cold / 3, AMPLITUDE * wave_ratio2**2 / 9, eta]) * (-4 * AMPLITUDE / eta)).tolist())

    def equation(efold, state):
        scale, matter, radiation_density, expansion, slope = environment.fluid_values(efold)
        wave_ratio2 = wave_scales / (scale * expansion)**2
        cold, cold_prime, radiation, radiation_velocity, eta = state.reshape(-1, 5).T
        output = np.empty((len(waves), 5))
        output[:, 0] = cold_prime
        output[:, 1] = -(2 + slope) * cold_prime + 1.5 / expansion**2 * (matter * cold + 2 * radiation_density * radiation)
        output[:, 2] = 4 / 3 * (cold_prime - radiation_velocity)
        output[:, 3] = -(1 + slope) * radiation_velocity + wave_ratio2 * radiation / 4
        output[:, 4] = 2 * radiation_density * radiation_velocity / (expansion**2 * wave_ratio2)
        return output.ravel()

    solution = integrate.solve_ivp(equation, (math.log(start_a), 0.), initial, method='DOP853',
        rtol=tolerance, atol=tolerance * 1e-5, max_step=.05, dense_output=True)
    assert solution.success, solution.message
    return solution
