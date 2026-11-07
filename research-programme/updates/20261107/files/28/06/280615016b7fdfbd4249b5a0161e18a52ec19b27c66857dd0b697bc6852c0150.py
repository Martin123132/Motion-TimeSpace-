from __future__ import annotations

from eos228 import *
import argparse
import ast
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path
import mpmath as mp
import sympy as sp
from scipy import integrate, interpolate

ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
PREVIOUS = BRANCH / 'metric-kinetic-return-20261026'
SEAL = 'e543ab89f7a6a0f9c3ad43129ea0d0d0be83e26c42461dce4df6db3f3b8a4842'
START = '2026-10-26T17:25:49+00:00'


def now():
    return datetime.now(timezone.utc).isoformat()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, indent=2, allow_nan=False), encoding='utf-8')
    temporary.replace(path)


def digest(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def register(inputs, path):
    path = Path(path).resolve()
    actual = digest(path)
    if str(path) in inputs:
        assert actual == inputs[str(path)], str(path)
    inputs[str(path)] = actual
    return path


def modest():
    import ctypes
    assert ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x4000)


def check(checks, name, value, limit):
    value = float(value)
    checks.append(dict(name=name, value=value, limit=limit, passed=bool(np.isfinite(value) and abs(value) <= limit)))


def relative(actual, expected):
    actual, expected = np.asarray(actual), np.asarray(expected)
    return float(np.max(np.abs(actual - expected)) / max(float(np.max(np.abs(expected))), 1e-300))


def prepare():
    assert not (ROOT / 'configuration.json').exists()
    assert digest(PREVIOUS / 'results/stage-integrity.json') == SEAL
    seal = read(PREVIOUS / 'results/stage-integrity.json')
    assert seal['qualified'] and seal['state'] == 'complete'
    inputs = {}
    register(inputs, PREVIOUS / 'results/stage-integrity.json')
    for name, expected in seal['file_hashes'].items():
        path = register(inputs, PREVIOUS / name)
        assert inputs[str(path)] == expected
    sources = [
        'polarized-finite-shift-kernel-20261007/kernel_common.py',
        'kinetic-gain-loss-20261008/kinetic_common.py',
        'kinetic-gain-loss-20261008/mass_shell_population.py',
        'population-matched-source-20261008/population_common.py',
        'population-matched-source-20261008/project_population.py',
        'thermal-recoil-and-spectral-response-20261007/thermal_common.py',
        'thermal-recoil-and-spectral-response-20261007/flrw_thermal_response.py',
        'coupled-finite-wave-evolution-20261007/evolution_common.py',
        'expanding-thermal-gravity-20261007/DERIVATION.md',
        'native-heavy-matching-20261007/native/fortran/constants.f90',
        'infrared-source-domain-20261008/evolve_nonlocal_background.py',
        'emitting-thermal-background-20261008/evolve_emitting_background.py']
    for name in sources:
        register(inputs, BRANCH / name)
    for model in ('heavy', 'cold'):
        folder = BRANCH / f'infrared-source-domain-20261008/backgrounds/{model}-nonlocal-refined-6400'
        register(inputs, folder / 'history.npz')
        report = read(register(inputs, folder / 'status.json'))
        assert report['all_checks_passed'] and report['mode'] == 'nonlocal-leading'
        assert report['bank'] == 's960-i256' and report['steps'] == 6400
        register(inputs, BRANCH / f'thermal-recoil-and-spectral-response-20261007/results/flrw-response/{model}.npz')
    for folder in ('emitting-thermal-background-20261008/banks/infrared96-q700',
                   'infrared-source-domain-20261008/banks/s960-i256'):
        for path in (BRANCH / folder).rglob('*'):
            if path.is_file():
                register(inputs, path)
    write(ROOT / 'inputs.json', inputs)
    write(ROOT / 'configuration.json', dict(stage=228, state='frozen', frozen_at=now(), turn_start=START,
          previous_goal_turn='progress', previous_seal=SEAL, moment_orders=[32, 48],
          identity_tolerance=1e-10, refinement_tolerance=.01, inherited_balance_tolerance=1e-8,
          inherited_gravity_comparison_tolerance=5e-5, gravity_conservation_tolerance=1e-8,
          gravity_rtol=3e-11, gravity_atol=1e-27, gravity_max_step=.01,
          primary_species='Relativistic electrons and inherited NR ions',
          ion_extension='Conditional diagnostic with inherited atomic-mass convention',
          original_bank_changed=False, original_histories_changed=False, tolerances_changed=False,
          protocol_hashes={path.name: digest(path) for path in ROOT.iterdir()
                           if path.is_file() and path.suffix in ('.py', '.md')}))
    print(json.dumps(dict(prepared=True, inputs=len(inputs))), flush=True)


def protocol():
    config = read(ROOT / 'configuration.json')
    repair_path = ROOT / 'protocol-repair.json'
    repairs = read(repair_path) if repair_path.exists() else None
    if repairs:
        assert digest(ROOT / 'configuration.json') == repairs['configuration_sha256']
    for name, expected in config['protocol_hashes'].items():
        if repairs and name in repairs['replacements']:
            replacement = repairs['replacements'][name]
            assert expected == replacement['original']
            expected = replacement['corrected']
        assert digest(ROOT / name) == expected, name
    return config


def load_background(model, inputs):
    sys.path.insert(0, str(BRANCH / 'thermal-recoil-and-spectral-response-20261007'))
    from thermal_common import ThermalBackground
    background = ThermalBackground(model)
    register(inputs, background.parent.source)
    register(inputs, background.native_constants)
    helium_number = background.helium_fraction / (1 - background.helium_fraction) * background.constants['m_H'] / background.constants['m_He4']
    mixture = Mixture(helium_number, background.constants['m_e'] / background.constants['m_H'],
                      background.constants['m_e'] / background.constants['m_He4'])
    return background, mixture


def add_modules(inputs):
    for module in list(sys.modules.values()):
        filename = getattr(module, '__file__', None)
        if filename:
            path = Path(filename).resolve()
            if path.suffix == '.py' and path.is_relative_to(BRANCH) and not path.is_relative_to(ROOT):
                register(inputs, path)


def symbolic(checks):
    theta = sp.Symbol('theta', positive=True)
    def bessel_series(order):
        coefficients = [sp.Integer(1)]
        for index in range(1, 5):
            coefficients.append(coefficients[-1] * (4 * order**2 - (2 * index - 1)**2) / (8 * index))
        return sum(value * theta**index for index, value in enumerate(coefficients))
    heat_series = sp.series(bessel_series(1) / bessel_series(2) + 3 * theta - 1, theta, 0, 4).removeO()
    expected = 3 * theta / 2 + sp.Rational(15, 8) * theta**2 - sp.Rational(15, 8) * theta**3
    check(checks, 'Bessel expansion derives electron heat coefficients', int(sp.simplify(heat_series - expected) != 0), 0)
    expansion, heat, initial = sp.symbols('s chi D0', real=True)
    density = heat * initial * (2 - sp.exp(-expansion))
    pressure = 2 * heat * initial * (1 - sp.exp(-expansion)) / 3
    check(checks, 'Leading combined stress conservation', int(sp.simplify(sp.diff(density, expansion) - density + 3 * pressure) != 0), 0)
    check(checks, 'Initial excess heat retained', int(sp.simplify(density.subs(expansion, 0) - heat * initial) != 0), 0)
    check(checks, 'Initial excess photon energy and pressure zero', int(pressure.subs(expansion, 0) != 0), 0)
    ratio, ratio_s, capacity, A, E = sp.symbols('R R_s C A E')
    E_s = (capacity - 2) * ratio - capacity * ratio_s
    A_s = A + capacity * (ratio_s - ratio)
    continuity = E_s + A_s - (E + A) + E + 2 * ratio
    check(checks, 'Exact mixture homogeneous first law', int(sp.simplify(continuity) != 0), 0)
    hubble, ratio_prime, capacity_R, perturb, divergence, transfer, pert_transfer, delta_b, scale = sp.symbols('H Rp CR dr J Q dQ db scale')
    predicted = (hubble - 2 * hubble / capacity - capacity_R / capacity * (ratio_prime - hubble * ratio)) * perturb - 2 * ratio * divergence / (3 * capacity) - (pert_transfer - transfer * delta_b) / (scale * capacity)
    residual = capacity * (predicted - hubble * perturb) + capacity_R * (ratio_prime - hubble * ratio) * perturb + 2 * hubble * perturb + 2 * ratio * divergence / 3 + (pert_transfer - transfer * delta_b) / scale
    check(checks, 'Perturbed temperature equation from particle first law', int(sp.simplify(residual) != 0), 0)
    nr = -hubble * perturb - 2 * ratio * divergence / 3 - (pert_transfer - transfer * delta_b) / scale
    check(checks, 'Perturbed gas equation recovers Stage75', int(sp.simplify(predicted.subs({capacity: 1, capacity_R: 0}) - nr) != 0), 0)
    return dict(heat_series=str(heat_series), capacity_series=str(sp.diff(heat_series, theta)))


def moment_tests(checks, theta_start):
    mp.mp.dps = 60
    source = BRANCH / 'polarized-finite-shift-kernel-20261007/kernel_common.py'
    tree = ast.parse(source.read_text(encoding='utf-8'))
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'juttner_rule')
    scope = dict(np=np, special=special)
    exec(compile(ast.Module(body=[function], type_ignores=[]), str(source), 'exec'), scope)
    rows = []
    for temperature in (theta_start / 10, theta_start / np.sqrt(10), theta_start, .03):
        theta = mp.mpf(float(temperature))
        def energy(parameter):
            return mp.besselk(1, 1 / parameter) / mp.besselk(2, 1 / parameter) + 3 * parameter - 1
        bessel_energy = energy(theta) / theta
        bessel_capacity = mp.diff(energy, theta)
        def measure(node):
            return mp.sqrt(node) * mp.exp(-node) * (1 + theta * node) * mp.sqrt(2 + theta * node)
        normal = mp.quad(measure, [0, 1, 8, 32, mp.inf])
        integral_mean = mp.quad(lambda node: node * measure(node), [0, 1, 8, 32, mp.inf]) / normal
        integral_capacity = mp.quad(lambda node: (node - integral_mean)**2 * measure(node), [0, 1, 8, 32, mp.inf]) / normal
        check(checks, f'Independent integral/Bessel excess heat theta={temperature}', float((integral_mean - bessel_energy) / (bessel_energy - mp.mpf('1.5'))), 1e-10)
        check(checks, f'Independent integral/Bessel capacity theta={temperature}', float(integral_capacity / bessel_capacity - 1), 1e-10)
        first = particle_moments(temperature, 32)
        second = particle_moments(temperature, 48)
        check(checks, f'Moments32/Bessel excess heat theta={temperature}', (float(first['energy_over_kBT']) - float(bessel_energy)) / float(bessel_energy - mp.mpf('1.5')), 1e-10)
        check(checks, f'Moments32/Bessel heat capacity theta={temperature}', float(first['cv_over_kB']) / float(bessel_capacity) - 1, 1e-10)
        check(checks, f'Radial order32/48 excess heat theta={temperature}', float(first['energy_over_kBT'] - second['energy_over_kBT']) / float(bessel_energy - mp.mpf('1.5')), 1e-10)
        check(checks, f'Pressure integration by parts theta={temperature}', float(first['pressure_over_nkBT']) - 1, 1e-10)
        speeds, weights = scope['juttner_rule'](temperature, 32)
        gamma = 1 / np.sqrt(1 - speeds**2)
        inherited_energy = np.dot(weights, speeds**2 * gamma**2 / (gamma + 1)) / temperature
        check(checks, f'Actual retained electron measure theta={temperature}', inherited_energy / float(first['energy_over_kBT']) - 1, 1e-10)
        rows.append(dict(theta=temperature, energy_over_kBT=float(bessel_energy), capacity_over_kB=float(bessel_capacity)))
    tiny = mp.mpf('1e-9')
    limit = (energy(tiny) - mp.mpf('1.5') * tiny) / tiny**2
    check(checks, 'Independent small-temperature coefficient 15/8', float(limit / mp.mpf('1.875') - 1), 1e-8)
    return rows


def evaluate():
    modest()
    protocol()
    assert not (ROOT / 'results/thermodynamics.json').exists()
    (ROOT / 'results').mkdir(exist_ok=True)
    inputs = read(ROOT / 'inputs.json')
    checks = []
    identities = symbolic(checks)
    models = []
    for model in ('heavy', 'cold'):
        background, mixture = load_background(model, inputs)
        path = BRANCH / f'infrared-source-domain-20261008/backgrounds/{model}-nonlocal-refined-6400/history.npz'
        with np.load(register(inputs, path)) as packet:
            saved = {key: packet[key] for key in packet.files}
        coordinate = saved['expansion']
        gas, heat = saved['temperature_scaled'], float(saved['heat'])
        assert heat == background.chi and len(coordinate) == 6401
        theta_start = background.theta0 / background.start_scale
        temperatures = theta_start * np.exp(-coordinate)
        if model == 'heavy':
            moments = moment_tests(checks, theta_start)
        ratio = 1 + heat * gas
        exact = mixture.state(temperatures)
        refined = mixture.state(temperatures, order=48)
        lagged = mixture.state(temperatures, ratio)
        ions = mixture.state(temperatures, relativistic_ions=True)
        completion = stress_from_energy_completion(coordinate, exact['delta_A'], heat)
        lag_completion = stress_from_energy_completion(coordinate, lagged['delta_A'], heat)
        ion_completion = stress_from_energy_completion(coordinate, ions['delta_A'], heat)
        coefficient = mixture.leading_coefficient(theta_start)
        leading_q = heat * coefficient * (2 - np.exp(-coordinate))
        leading_p = 2 * heat * coefficient * (1 - np.exp(-coordinate)) / 3
        step = float(coordinate[-1] / (len(coordinate) - 1))
        integral = finite_capacity_integral(gas, step)
        linear_integral = integrate.cumulative_trapezoid(gas, coordinate, initial=0.)
        capacity_q = -heat**2 * integral
        capacity_p = heat**2 * (gas - integral) / 3
        work_defect = saved['expansion_work'] - coordinate - heat * integral
        energy_defect = saved['energy_scaled'] + heat * gas + saved['expansion_work']
        check(checks, model + ': full history radial refinement excess energy', relative(exact['delta_A'], refined['delta_A']), 1e-10)
        check(checks, model + ': capacity positive', int(np.min(exact['C']) <= 0), 0)
        check(checks, model + ': pressure positive', int(np.min(exact['P']) <= 0), 0)
        check(checks, model + ': asymptotic density against exact electron EOS', relative(leading_q, completion['delta_q']), .01)
        check(checks, model + ': asymptotic pressure against exact electron EOS', relative(leading_p, completion['delta_p']), .01)
        check(checks, model + ': original work reconstructed from gas recurrence', np.max(abs(work_defect)), 1e-8)
        check(checks, model + ': original total energy balance', np.max(abs(energy_defect)), 1e-8)
        check(checks, model + ': capacity recurrence versus linear-history integral', relative(integral, linear_integral), .01)
        check(checks, model + ': derived completed stress continuity', np.max(abs(heat * exact['delta_A'] - completion['delta_q'] + 3 * completion['delta_p'])) / np.max(abs(completion['delta_q'])), 1e-10)
        capacity_spline = interpolate.CubicSpline(coordinate, exact['delta_C'])
        capacity_primitive = capacity_spline.antiderivative()
        independently_completed_photon = heat * (capacity_primitive(coordinate) - capacity_primitive(0))
        check(checks, model + ': independent capacity-source integral', relative(independently_completed_photon, completion['photon_energy']), 1e-10)
        left = exact['delta_A'][0]
        check(checks, model + ': initial excess heat in source', completion['delta_q'][0] / (heat * left) - 1, 1e-10)
        check(checks, model + ': initial photon correction zero', completion['photon_energy'][0], 0)
        np.savez_compressed(ROOT / f'results/{model}-stress.npz', expansion=coordinate, theta=temperatures,
              ratio=ratio, delta_A=exact['delta_A'], delta_C=exact['delta_C'], delta_q=completion['delta_q'],
              delta_p=completion['delta_p'], photon_energy=completion['photon_energy'],
              leading_delta_q=leading_q, leading_delta_p=leading_p, capacity_q=capacity_q,
              capacity_p=capacity_p, prescribed_lag_delta_q=lag_completion['delta_q'],
              ion_extended_delta_q=ion_completion['delta_q'], chi=heat, D0=coefficient)
        models.append(dict(model=model, heat=heat, theta_start=theta_start, theta_end=float(temperatures[-1]),
              electron_fraction=float(mixture.fractions[0]), particle_fractions=mixture.fractions.tolist(),
              constants=background.constants, T0=background.temperature0, YHe=background.helium_fraction,
              leading_D0=coefficient, exact_initial_D=float(left),
              final_density_correction=float(completion['delta_q'][-1]), final_pressure_correction=float(completion['delta_p'][-1]),
              initial_density_correction=float(completion['delta_q'][0]),
              final_photon_energy_correction=float(completion['photon_energy'][-1]),
              maximum_fractional_heat_capacity_change=float(np.max(exact['delta_C'])),
              maximum_capacity_density=float(np.max(abs(capacity_q))),
              eos_to_capacity_density_ratio=float(np.max(abs(completion['delta_q'])) / np.max(abs(capacity_q))),
              prescribed_lag_relative_change=relative(lag_completion['delta_q'], completion['delta_q']),
              conditional_ion_extension_relative_change=relative(ion_completion['delta_q'], completion['delta_q']),
              work_roundoff_density_allowance=float(heat * np.max(abs(work_defect))),
              energy_roundoff_density_allowance=float(heat * np.max(abs(energy_defect))),
              saved_lag_maximum=float(np.max(abs(heat * gas))),
              literal_frozen_photons_continuity_defect_scale=float(heat * np.max(abs(exact['delta_C'])))))
        print(json.dumps(dict(model=model, final_delta_q=models[-1]['final_density_correction'],
                         eos_to_capacity=models[-1]['eos_to_capacity_density_ratio'])), flush=True)
    add_modules(inputs)
    for path, expected in inputs.items():
        assert digest(path) == expected, path
    write(ROOT / 'results/thermodynamic-inputs.json', inputs)
    report = dict(stage=228, state='complete', finished_at=now(), symbolic=identities, moment_checks=moments,
                  models=models, checks=checks, failed=[row for row in checks if not row['passed']],
                  qualified=all(row['passed'] for row in checks), inputs_rehashed=len(inputs),
                  scope='Electron-derived EOS and conserved leading thermal source; saved-lag and ion variants are diagnostics')
    write(ROOT / 'results/thermodynamics.json', report)
    print(json.dumps(dict(checks=len(checks), failed=report['failed'], qualified=report['qualified'])), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['prepare', 'evaluate'])
    arguments = parser.parse_args()
    if arguments.action == 'prepare':
        prepare()
    else:
        evaluate()
