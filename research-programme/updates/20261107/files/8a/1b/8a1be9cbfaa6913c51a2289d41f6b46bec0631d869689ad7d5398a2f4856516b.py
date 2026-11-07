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
PARENT = BRANCH / 'motion-bath-matching-20261006'
COSMO = BRANCH / 'cosmology-reconnection-20261006'
sys.dont_write_bytecode = True
sys.path.insert(0, str(COSMO))
import cosmology_common as old

C_KM_S = 299792.458
H0_KM_S_MPC = old.inherited.H0_KM_S_MPC
H0_SECOND = H0_KM_S_MPC * 1000 / old.inherited.MPC_METRES
HBAR_EV_SECOND = 6.582119569e-16
SCALE_MASS = 641967984.8120126
PARTICLE_FLOOR = 8.882479043701029e-23 / (HBAR_EV_SECOND * H0_SECOND)
LOCKED_PARTICLE = 1e-20 / (HBAR_EV_SECOND * H0_SECOND)
MASS_RATIOS = [1e6, 1e7, 1e8, SCALE_MASS, PARTICLE_FLOOR, LOCKED_PARTICLE]
WAVENUMBERS = [.02, .05, .1, .2, .5, 1., 2., 5., 10.]
FRACTIONS = [.1, .5, .8]
MODELS = ['LCDM', 'ParentScalar_Lambda_free', 'ParentScalar_Lambda_zero']
SOURCE_NAMES = [
    '5194-Y5-R2FR-parent-canonical-scalar-perturbation-growth-and-compressed-CMB-gate.md',
    '5195-Y5-R2FR-matched-joint-CMB-informed-parent-refit-and-physical-sound-horizon-gate.md',
    '5197-Y5-R2FR-universal-gap-cross-arena-compatibility-and-route-separation-theorem.md',
]
SOURCE_URLS = ['https://arxiv.org/abs/2201.10238',
              'https://doi.org/10.1103/PhysRevD.105.123529']


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
    paths = [Path(__file__), PARENT / 'results/stage-integrity.json',
             PARENT / 'results/replay/status.json', COSMO / 'results/comparison/status.json',
             COSMO / 'cosmology_common.py', Path(old.inherited.__file__),
             Path(old.inherited.closure_runner.__file__)]
    paths += [POST / name for name in SOURCE_NAMES]
    return {str(path): digest(path) for path in sorted(paths)}


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


class Background:
    def __init__(self, model, points=4001):
        fit = next(row for row in read_json(COSMO / 'results/comparison/status.json')['fits'] if row['model'] == model)
        self.model = model
        self.parameters = dict(fit['parameters'], **fit['fixed'])
        self.omega_m = self.parameters['Omega_m']
        redshift = np.expm1(np.linspace(0., 5., points))
        self.grid = -np.log1p(redshift)[::-1]
        if model == 'LCDM':
            expansion = old.inherited.baseline_e_grid(model, self.parameters, redshift)
            slope = (-1.5 * self.omega_m * (1 + redshift)**3 - 2 * old.inherited.OMEGA_R * (1 + redshift)**4) / expansion**2
            constraint = 0.
        else:
            profile = old.inherited.direct_scalar_profile(self.omega_m, self.parameters['log10_mu'], self.parameters['f_scalar'], -5., redshift)
            expansion, slope = profile['E'], profile['h']
            constraint = float(np.max(abs(profile['constraint_residual'])))
        self.log_e = interpolate.CubicSpline(self.grid, np.log(expansion[::-1]))
        self.h = interpolate.CubicSpline(self.grid, slope[::-1])
        interior = self.grid[2:-2]
        self.diagnostics = dict(model=model, parameters=self.parameters, present_E=float(expansion[0]),
            max_constraint_residual=constraint,
            max_dlogE_interpolation_difference=float(np.max(abs(self.log_e(interior, 1) - self.h(interior)))),
            archived_SN_BAO_chi2=fit['chi2_total'], no_new_background_fit=True,
            interpolation_nodes=points, supported_N=[-5., 0.])

    def values(self, efold):
        if efold < -5. - 1e-10 or efold > 1e-10:
            raise ValueError('No background extrapolation allowed')
        expansion2 = math.exp(2 * float(self.log_e(efold)))
        slope = float(self.h(efold))
        matter_fraction = self.omega_m * math.exp(-3 * efold) / expansion2
        return expansion2, slope, matter_fraction


def conditions(background, mass_ratio, wave, start_z):
    grid = np.linspace(-math.log1p(start_z), 0., 301)
    scale = np.exp(grid)
    expansion = np.exp(background.log_e(grid))
    wave_hubble = C_KM_S * wave / H0_KM_S_MPC
    values = dict(max_H_over_M=float(np.max(expansion / mass_ratio)),
                  max_k_over_aM=float(np.max(wave_hubble / (scale * mass_ratio))),
                  min_k_over_aH=float(np.min(wave_hubble / (scale * expansion))))
    values['accepted'] = values['max_H_over_M'] <= .01 and values['max_k_over_aM'] <= .05 and values['min_k_over_aH'] >= 10.
    return values


def initial_state(background, share, start_z, preparation='equal'):
    scale = 1 / (1 + start_z)
    equality_ratio = background.omega_m * scale / old.inherited.OMEGA_R
    slope = 1.5 * equality_ratio / (1 + 1.5 * equality_ratio)
    if preparation == 'equal':
        return np.array([1., slope, 1., slope])
    if preparation == 'heavy_unperturbed' and share < 1:
        return np.array([1., slope, 0., 0.]) / (1 - share)
    raise ValueError('Unsupported initial preparation')


def solve_response(background, mass_ratio, share, wave, start_z=99., preparation='equal', pressure=True,
                   method='DOP853', tolerance=2e-8, max_step=.06, dense=False):
    wave_hubble = C_KM_S * wave / H0_KM_S_MPC
    pressure_zero = wave_hubble**4 / (4 * mass_ratio**2) if pressure else 0.
    initial = initial_state(background, share, start_z, preparation)

    def equation(efold, state):
        expansion2, slope, matter_fraction = background.values(efold)
        friction = 2 + slope
        source = 1.5 * matter_fraction * ((1 - share) * state[0] + share * state[2])
        pressure_coefficient = pressure_zero * math.exp(-4 * efold) / expansion2
        return np.array([state[1], -friction * state[1] + source,
                         state[3], -friction * state[3] + source - pressure_coefficient * state[2]])

    solution = integrate.solve_ivp(equation, (-math.log1p(start_z), 0.), initial,
        method=method, rtol=tolerance, atol=tolerance / 100, max_step=max_step, dense_output=dense)
    if not solution.success or not np.all(np.isfinite(solution.y)):
        raise RuntimeError(solution.message)
    return solution


def summary(background, mass_ratio, share, wave, response, control, start_z=99., preparation='equal'):
    state, cold = response.y[:, -1], control.y[:, -1]
    total = (1 - share) * state[0] + share * state[2]
    total_derivative = (1 - share) * state[1] + share * state[3]
    cold_total = (1 - share) * cold[0] + share * cold[2]
    cold_derivative = (1 - share) * cold[1] + share * cold[3]
    return dict(model=background.model, mass_over_H0=mass_ratio, mass_eV=mass_ratio * H0_SECOND * HBAR_EV_SECOND,
        heavy_fraction=share, k_Mpc_inverse=wave, start_z=start_z, preparation=preparation,
        total_density_ratio=float(total / cold_total), cold_density_ratio=float(state[0] / cold[0]),
        total_density_derivative_ratio=float(total_derivative / cold_derivative),
        cold_velocity_divergence_ratio=float(state[1] / cold[1]), heavy_delta_today=float(state[2]),
        conditional_equal_initial_power_ratio=float((total / cold_total)**2),
        total_response_is_primordial_transfer_function=False, growth_likelihood_chi2=None,
        solver_nfev=response.nfev, **conditions(background, mass_ratio, wave, start_z))
