from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import sys
import time

import numpy as np
import psutil
from scipy import integrate, interpolate, optimize, linalg

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
PARENT = BRANCH / 'heavy-interaction-and-condensate-bridge-20261007'
EARLY = BRANCH / 'early-adiabatic-matching-20261006'
COSMO = BRANCH / 'cosmology-reconnection-20261006'
CAMB_SITE = POST / '.venv-score/Lib/site-packages'
sys.path.append(str(CAMB_SITE))
import camb

C_LIGHT = 299792.458
H0 = 70.
OMBH2 = .02239
NEUTRINO_MASS = .06
AS = 2.1e-9
NS = .9653
START = math.log(1e-9)
EXACT_END = .0004
HEAVY_MASS = 641967984.8120126
BAO_ROOT = POST.parent / 'formalization-workbench/data/cosmology/desi_dr2_bao'
BAO_MEAN = BAO_ROOT / 'desi_gaussian_bao_ALL_GCcomb_mean.txt'
BAO_COV = BAO_ROOT / 'desi_gaussian_bao_ALL_GCcomb_cov.txt'
SOURCE_NAMES = [
    '5156-Y5-R2FR-FLRW-Hessian-Gaussian-state-single-clock-adiabatic-radiation-transfer-and-patch-collapse-gate.md',
    '5194-Y5-R2FR-parent-canonical-scalar-perturbation-growth-and-compressed-CMB-gate.md',
]
SOURCE_URLS = [
    'https://camb.readthedocs.io/en/latest/dark_energy.html',
    'https://camb.readthedocs.io/en/latest/results.html',
    'https://arxiv.org/abs/astro-ph/9506072',
    'https://arxiv.org/abs/2201.10238',
    'https://github.com/cmbant/CAMB/tree/1.6.6',
    'https://github.com/CobayaSampler/bao_data',
]


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
        EARLY / 'results/matching/status.json', EARLY / 'early_common.py',
        COSMO / 'results/comparison/status.json', BAO_MEAN, BAO_COV,
        POST / 'scripts/Y5_R2FR_5194_parent_scalar_perturbation_growth_CMB_gate.py']
    paths += [POST / name for name in SOURCE_NAMES]
    paths += list((CAMB_SITE / 'camb').glob('*.dll'))
    paths += [CAMB_SITE / 'camb' / name for name in ['__init__.py', 'results.py', 'dark_energy.py', 'model.py']]
    return {str(path): digest(path) for path in paths}


def save(label, script, report, extra=()):
    folder = ROOT / 'results' / label
    folder.mkdir(parents=True, exist_ok=False)
    hashes = inputs()
    hashes.update({str(path): digest(path) for path in extra})
    output = dict(state='complete', time_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script), input_hashes=hashes, source_urls=SOURCE_URLS,
        camb_version=camb.__version__, **report)
    write_json(folder / 'status.json', output)
    (folder / 'COMPLETE').write_text(output['time_utc'] + '\n', encoding='utf-8')


def inherited_parameters():
    fits = read_json(COSMO / 'results/comparison/status.json')['fits']
    row = next(row for row in fits if row['model'] == 'ParentScalar_Lambda_zero')
    parameters = dict(row['parameters'], **row['fixed'])
    return parameters['Omega_m'], 10**parameters['log10_mu']


def base_params(omega_m, fraction=0., accuracy=1.):
    params = camb.CAMBparams()
    params.set_cosmology(H0=H0, ombh2=OMBH2, omch2=.12, mnu=NEUTRINO_MASS,
        omk=0., tau=.0544, nnu=3.044, TCMB=2.7255)
    omega_cold_h2 = (1 - fraction) * omega_m * (H0 / 100)**2 - OMBH2 - params.omnuh2
    assert omega_cold_h2 > 0
    params.set_cosmology(H0=H0, ombh2=OMBH2, omch2=omega_cold_h2, mnu=NEUTRINO_MASS,
        omk=0., tau=.0544, nnu=3.044, TCMB=2.7255)
    params.InitPower.set_params(As=AS, ns=NS)
    params.set_accuracy(AccuracyBoost=accuracy, lAccuracyBoost=accuracy, lSampleBoost=accuracy)
    params.WantCls = False
    params.NonLinear = camb.model.NonLinear_none
    return params


class StandardSpecies:
    def __init__(self, omega_m, fraction):
        self.params = base_params(omega_m, fraction)
        self.native = camb.get_background(self.params, no_thermo=True)
        self.efolds = np.linspace(START - .1, 0., 10001)
        scales = np.exp(self.efolds)
        values = self.native.get_background_densities(scales, vars=['cdm', 'baryon', 'photon', 'neutrino', 'nu'])
        normalization = 3 * (H0 / C_LIGHT)**2
        self.coefficients = {name: float(data[-1] / normalization) for name, data in values.items()}
        self.nu_log = interpolate.CubicSpline(self.efolds, np.log(values['nu'] / normalization))
        self.matter = self.coefficients['cdm'] + self.coefficients['baryon']
        self.radiation = self.coefficients['photon'] + self.coefficients['neutrino']

    def values(self, efold):
        scale = np.exp(efold)
        neutrino = np.exp(self.nu_log(efold) - 4 * efold)
        neutrino_w = (1 - self.nu_log(efold, 1)) / 3
        matter = self.matter / scale**3
        radiation = self.radiation / scale**4
        density = matter + radiation + neutrino
        pressure = radiation / 3 + neutrino_w * neutrino
        return density, pressure

    def sample(self, efolds):
        scales = np.exp(efolds)
        result = {name: coefficient / scales**(3 if name in ['cdm', 'baryon'] else 4)
            for name, coefficient in self.coefficients.items() if name != 'nu'}
        result['nu'] = np.exp(self.nu_log(efolds) - 4 * efolds)
        return result


def solve_slow(species, heavy_density, slow_mass):
    def evolve(displacement, dense=False):
        standard, _ = species.values(START)
        heavy, _ = heavy_density(START)
        expansion2 = standard + heavy + slow_mass**2 * displacement**2
        initial = [displacement, -slow_mass**2 * displacement / (5 * expansion2)]

        def equation(efold, state):
            field, velocity = state
            density, pressure = species.values(efold)
            heavy, heavy_derivative = heavy_density(efold)
            expansion2 = (density + heavy + slow_mass**2 * field**2) / (1 - velocity**2)
            slope = (-1.5 * (density + pressure) + .5 * heavy_derivative) / expansion2 - 3 * velocity**2
            return [velocity, -(3 + slope) * velocity - slow_mass**2 * field / expansion2]

        result = integrate.solve_ivp(equation, (START, 0.), initial, method='DOP853',
            rtol=3e-11, atol=1e-13, max_step=.04, dense_output=dense)
        assert result.success
        field, velocity = result.y[:, -1]
        expansion2 = (species.values(0.)[0] + heavy_density(0.)[0] + slow_mass**2 * field**2) / (1 - velocity**2)
        return expansion2, result

    root = optimize.brentq(lambda displacement: evolve(displacement)[0] - 1, .01, 3., xtol=5e-13)
    expansion2, result = evolve(root, True)
    return root, result, expansion2


def exact_heavy(species, target, frozen_slow, tolerance=1e-10):
    def evolve(displacement, dense=False):
        expansion = math.sqrt(species.values(START)[0] + HEAVY_MASS**2 * displacement**2 + frozen_slow)
        initial = [displacement, -HEAVY_MASS * displacement / (5 * expansion),
            HEAVY_MASS * math.exp(2 * START) / (2 * math.sqrt(species.radiation))]

        def equation(efold, state):
            field, velocity, phase = state
            expansion = math.sqrt(species.values(efold)[0] + HEAVY_MASS**2 * (field**2 + velocity**2) + frozen_slow)
            frequency = HEAVY_MASS / expansion
            return [frequency * velocity, -3 * velocity - frequency * field, frequency]

        result = integrate.solve_ivp(equation, (START, math.log(EXACT_END)), initial,
            method='DOP853', rtol=tolerance, atol=tolerance * 1e-4, dense_output=dense, max_step=.03)
        assert result.success
        field, velocity, phase = result.y[:, -1]
        expansion = math.sqrt(species.values(result.t[-1])[0] + HEAVY_MASS**2 * (field**2 + velocity**2) + frozen_slow)
        action = HEAVY_MASS**2 * EXACT_END**3 * (field**2 + (velocity + 1.5 * expansion / HEAVY_MASS * field)**2)
        return action, result

    displacement = read_json(EARLY / 'results/matching/status.json')['displacement']
    history = []
    for iteration in range(7):
        action, result = evolve(displacement)
        residual = action / target - 1
        history.append(dict(displacement=displacement, action=action, relative_error=residual, nfev=result.nfev))
        print(dict(event='heavy_calibration', iteration=iteration, **history[-1]), flush=True)
        if abs(residual) < 3e-8:
            _, result = evolve(displacement, True)
            return displacement, result, history
        displacement *= math.sqrt(target / action)
    raise RuntimeError('heavy calibration did not converge')


def density_bridge(exact, target, switch):
    lower = math.log(switch / 2)
    upper = math.log(switch)

    def evaluate(efold):
        values = np.asarray(efold)
        clipped = np.minimum(values, upper)
        field, velocity, _ = exact.sol(clipped)
        raw = HEAVY_MASS**2 * (field**2 + velocity**2)
        raw_slope = -6 * velocity**2 / (field**2 + velocity**2)
        dust_log = math.log(target) - 3 * values
        position = np.clip((values - lower) / (upper - lower), 0., 1.)
        weight = position**3 * (10 - 15 * position + 6 * position**2)
        weight_prime = 30 * position**2 * (1 - position)**2 / (upper - lower)
        log_raw = np.log(raw)
        log_density = (1 - weight) * log_raw + weight * dust_log
        slope = (1 - weight) * raw_slope - 3 * weight + weight_prime * (dust_log - log_raw)
        density = np.exp(log_density)
        return density, density * slope

    return evaluate


def full_table(species, slow_solution, slow_mass, heavy_density, exact, resolution=1):
    base_grid = np.linspace(START, 0., 7001 * resolution)
    if exact is not None:
        middle = (exact.t[1:] + exact.t[:-1]) / 2
        grid = np.unique(np.concatenate([base_grid, exact.t, middle]))
    else:
        grid = base_grid
    standard, standard_pressure = species.values(grid)
    heavy, heavy_prime = heavy_density(grid)
    field, velocity = slow_solution.sol(grid)
    expansion2 = (standard + heavy + slow_mass**2 * field**2) / (1 - velocity**2)
    slow_density = expansion2 * velocity**2 + slow_mass**2 * field**2
    slow_pressure = expansion2 * velocity**2 - slow_mass**2 * field**2
    dark_density = heavy + slow_density
    dark_pressure = -heavy - heavy_prime / 3 + slow_pressure
    table = dict(efold=grid, scale=np.exp(grid), dark_density=dark_density,
        dark_w=dark_pressure / dark_density, expansion2=expansion2,
        heavy_density=np.broadcast_to(heavy, grid.shape), slow_density=slow_density,
        slow_field=field, slow_velocity=velocity)
    return table


def native_background(species, table, accuracy=1.):
    params = species.params.copy()
    params.set_accuracy(AccuracyBoost=accuracy, lAccuracyBoost=accuracy, lSampleBoost=accuracy)
    params.set_dark_energy(use_tabulated_w=True, wde_a_array=table['scale'],
        wde_w_array=table['dark_w'], dark_energy_model='ppf')
    result = camb.get_background(params)
    return params, result


def bao_score(background):
    data = np.loadtxt(BAO_MEAN, dtype=str)
    redshift = data[:, 0].astype(float)
    observed = data[:, 1].astype(float)
    kinds = data[:, 2]
    covariance = np.loadtxt(BAO_COV)
    factor = linalg.cho_factor(covariance, lower=True)
    distances = background.comoving_radial_distance(redshift)
    radial = C_LIGHT / background.hubble_parameter(redshift)
    volume = (redshift * radial * distances**2)**(1 / 3)
    drag = background.get_derived_params()['rdrag']
    raw = np.array([{'DV_over_rs': volume[index], 'DM_over_rs': distances[index], 'DH_over_rs': radial[index]}[kind] for index, kind in enumerate(kinds)])
    prediction = raw / drag
    residual = prediction - observed
    inverse = linalg.cho_solve(factor, residual)
    scale = float(raw @ linalg.cho_solve(factor, observed) / (raw @ linalg.cho_solve(factor, raw)))
    shape_residual = scale * raw - observed
    shape_chi = float(shape_residual @ linalg.cho_solve(factor, shape_residual))
    return dict(chi2_fixed_physical_rd=float(residual @ inverse),
        chi2_profiled_rd_shape_only=shape_chi, profiled_rd_Mpc=1 / scale,
        physical_rd_Mpc=drag, parameter_fit=False, information_criteria_reported=False,
        rows=[dict(z=float(redshift[index]), observable=str(kinds[index]), measured=float(observed[index]),
            predicted=float(prediction[index]), residual=float(residual[index])) for index in range(len(kinds))])


def sound_horizon_quadrature(species, table, redshift):
    log_expansion = interpolate.CubicSpline(table['efold'], .5 * np.log(table['expansion2']))
    limit = -math.log1p(redshift)
    baryon_photon_ratio = 3 * species.coefficients['baryon'] / (4 * species.coefficients['photon'])
    efolds = np.unique(np.r_[table['efold'][table['efold'] < limit], limit])
    integrand = np.exp(-efolds - log_expansion(efolds)) / np.sqrt(3 * (1 + baryon_photon_ratio * np.exp(efolds)))
    tail = math.exp(START) / math.sqrt(3 * (species.radiation + math.exp(species.nu_log(START))))
    return C_LIGHT / H0 * (integrate.simpson(integrand, x=efolds) + tail)

