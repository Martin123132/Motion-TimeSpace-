from __future__ import annotations

from datetime import datetime, timezone
import json
import math
from pathlib import Path
import time

import numpy as np
from scipy import integrate

import early_common as early
from early_common import ROOT, PARENT, MASS, FRACTION, AMPLITUDE, MODES, Environment, modest_process, read_json, digest, save, early_initial, exact_evolution, extract_match, fluid_evolution, cold_evolution
from run_early_match import summarize


def independent_onset(environment, displacement):
    initial = early_initial(environment, displacement, 1e-9, MODES)

    def equation(efold, state):
        field, velocity, phase = state[:3]
        scale, cold_density, radiation_density, _, expansion, slope = environment.exact_values(efold, field, velocity)
        frequency = MASS / expansion
        result = [frequency * velocity, -3 * velocity - frequency * field, frequency]
        for index, (wave, _) in enumerate(MODES):
            cold, cold_prime, radiation, radiation_velocity, delta_field, delta_velocity, eta = state[3 + 7 * index:10 + 7 * index]
            wave_ratio2 = (299792.458 * wave / 70. / (scale * expansion))**2
            delta_density = 2 * MASS**2 * (field * delta_field + velocity * delta_velocity)
            delta_pressure = 2 * MASS**2 * (velocity * delta_velocity - field * delta_field)
            momentum = 2 * MASS**2 * wave_ratio2 / frequency * velocity * delta_field
            result.extend([cold_prime,
                -(2 + slope) * cold_prime + 1.5 * (cold_density * cold + 2 * radiation_density * radiation + delta_density + 3 * delta_pressure) / expansion**2,
                4 / 3 * (cold_prime - radiation_velocity), -(1 + slope) * radiation_velocity + wave_ratio2 * radiation / 4,
                frequency * delta_velocity, -3 * delta_velocity - (frequency + wave_ratio2 / frequency) * delta_field + velocity * cold_prime,
                1.5 * (4 / 3 * radiation_density * radiation_velocity + momentum) / (expansion**2 * wave_ratio2)])
        return result

    solution = integrate.solve_ivp(equation, (math.log(1e-9), math.log(2e-5)), initial,
        method='Radau', rtol=1e-10, atol=1e-18, max_step=.02)
    assert solution.success
    return solution


def main():
    modest_process()
    started = time.monotonic()
    folder = ROOT / 'runs/validation'
    folder.mkdir(parents=True, exist_ok=False)

    def log(event, **payload):
        record = dict(event=event, seconds=time.monotonic() - started, **payload)
        with (folder / 'log.txt').open('a', encoding='utf-8') as handle:
            handle.write(json.dumps(record, allow_nan=False) + '\n')
        print(record, flush=True)

    checks = []

    def check(name, condition, value=None, limit=None):
        entry = dict(name=name, passed=bool(condition), value=value, limit=limit)
        checks.append(entry)
        if not condition:
            log('failed_check', **entry)

    scan = read_json(ROOT / 'results/matching/status.json')
    for label, script in [('matching', 'run_early_match.py'), ('preflight', 'preflight_early.py')]:
        report = read_json(ROOT / 'results' / label / 'status.json')
        check(label + ' producer unchanged', report['script_sha256'] == digest(ROOT / script))
        for source, expected in report['input_hashes'].items():
            check(label + ' source unchanged: ' + Path(source).name, digest(source) == expected)
    check('12 rows and all modes accounted for', len(scan['rows']) == 12 and len(scan['matches']) == 3)
    check('no background re-fit', not scan['background_parameters_refitted'])
    check('no new observations or Boltzmann claim', not scan['observations_fitted'] and not scan['full_Boltzmann_evolution'])
    check('population and covariance remain explicit inputs', not scan['heavy_abundance_derived'] and not scan['primordial_covariance_derived'])
    for match in scan['matches']:
        error = abs(match['relative_abundance_error'])
        check('matched background abundance:' + str(match['scale']), error < 1e-5, error, 1e-5)
        for row in match['matches']:
            suffix = ':' + str(match['scale']) + ':' + str(row['wave']) + ':' + row['preparation']
            error = row['Einstein_constraint_error_over_seed']
            check('exact Einstein constraint' + suffix, error < 1e-5, error, 1e-5)
            error = row['pressure_mismatch_over_perturbation_norm']
            check('averaged pressure closure' + suffix, error < 1e-4, error, 1e-4)
    central = [row for row in scan['rows'] if row['matching_a'] == .0003]
    switching = []
    for wave, preparation in MODES:
        values = [row['comoving_ratio'] for row in scan['rows'] if row['k_Mpc_inverse'] == wave and row['preparation'] == preparation]
        spread = float(np.ptp(values) / max(abs(np.mean(values)), 1e-30))
        limit = 2e-5 if preparation == 'adiabatic' else .02
        check('matching epoch convergence:' + str(wave) + ':' + preparation, spread < limit, spread, limit)
        switching.append(dict(wave=wave, preparation=preparation, fractional_range=spread))

    environment = Environment()
    displacement = scan['displacement']
    refined_exact = exact_evolution(environment, displacement, tolerance=2e-10)
    log('refined_exact_complete', nfev=refined_exact.nfev)
    refined_control = cold_evolution(environment, tolerance=4e-9)
    log('refined_control_complete', nfev=refined_control.nfev)
    refined_match = extract_match(environment, refined_exact, .0003)
    refined_fluid = fluid_evolution(environment, refined_match, tolerance=4e-9)
    refined_rows = summarize(environment, refined_fluid, refined_control, refined_match)
    log('refined_fluid_complete', rows=refined_rows)
    sensitivities = []

    def compare(label, changed):
        entries = []
        for original, row in zip(central, changed):
            difference = abs(row['comoving_ratio'] - original['comoving_ratio'])
            relative = difference / max(abs(original['comoving_ratio']), 1e-30)
            limit = 3e-5 if row['preparation'] == 'adiabatic' else .02
            check(label + ':' + str(row['k_Mpc_inverse']) + ':' + row['preparation'], relative < limit, relative, limit)
            entries.append(dict(wave=row['k_Mpc_inverse'], preparation=row['preparation'], relative_change=relative, absolute_change=difference, changed_ratio=row['comoving_ratio']))
        sensitivities.append(dict(test=label, entries=entries))

    compare('ODE refinement', refined_rows)
    for match in scan['window_sensitivity']:
        changed_fluid = fluid_evolution(environment, match)
        changed = summarize(environment, changed_fluid, refined_control, match)
        compare('averaging width ' + str(match['half_width_in_mass_time']), changed)
        log('window_check_complete', width=match['half_width_in_mass_time'], rows=changed)

    earlier_exact = exact_evolution(environment, displacement, start_a=5e-10)
    earlier_match = extract_match(environment, earlier_exact, .0003)
    earlier_control = cold_evolution(environment, start_a=5e-10)
    earlier_fluid = fluid_evolution(environment, earlier_match)
    earlier_rows = summarize(environment, earlier_fluid, earlier_control, earlier_match)
    compare('start twice as early', earlier_rows)
    log('earlier_start_complete', rows=earlier_rows)

    independent = independent_onset(environment, displacement)
    reference = refined_exact.sol(math.log(2e-5))
    independent_errors = []
    for index, (_, preparation) in enumerate(MODES):
        block = slice(3 + 7 * index, 10 + 7 * index)
        difference = float(np.max(abs(independent.y[block, -1] - reference[block])) / max(AMPLITUDE, float(np.max(abs(reference[block])))))
        check('independent implicit onset integrator:' + str(index), difference < 1e-5, difference, 1e-5)
        independent_errors.append(difference)
    log('independent_onset_complete', errors=independent_errors, nfev=independent.nfev)
    try:
        early.FRACTION = 0.
        zero = exact_evolution(environment, 0., end_a=2e-5, tolerance=2e-10, modes=MODES[:3])
    finally:
        early.FRACTION = FRACTION
    cold_reference = refined_control.sol(math.log(2e-5)).reshape(-1, 5)
    zero_errors = []
    for index in range(3):
        block = zero.y[3 + 7 * index:10 + 7 * index, -1][[0, 1, 2, 3, 6]]
        difference = float(np.max(abs(block - cold_reference[index])) / max(AMPLITUDE, float(np.max(abs(cold_reference[index])))))
        check('zero heavy fraction recovers cold control:' + str(index), difference < 1e-5, difference, 1e-5)
        zero_errors.append(difference)

    parent_validation = read_json(PARENT / 'results/validation/status.json')
    handoffs = []
    state99 = refined_fluid.sol(-math.log(100)).reshape(-1, 7)
    for index, matrix in enumerate(parent_validation['finite_time_response_matrices']):
        wave = matrix['k_Mpc_inverse']
        cold, cold_prime, radiation, radiation_velocity, heavy, heavy_velocity, eta = state99[index]
        wave2 = (299792.458 * wave / 70. / (.01 * environment.fluid_values(-math.log(100))[3]))**2
        kappa2 = (299792.458 * wave / 70. / (.01 * MASS))**2
        pressure = kappa2 / (math.sqrt(1 + kappa2) + 1)**2 * (heavy + 3 * heavy_velocity / wave2)
        heavy_prime = cold_prime - heavy_velocity - 3 * pressure
        seed = [cold, cold_prime, heavy, heavy_prime]
        final = np.asarray(matrix['propagator']) @ seed
        value = (1 - FRACTION) * final[0] + FRACTION * final[2]
        full = refined_rows[index]['total_delta']
        error = abs(value / full - 1)
        check('actual early state joins existing stage50 propagator:' + str(wave), error < 1e-3, error, 1e-3)
        handoffs.append(dict(wave=wave, seed_at_z99=seed, parent_propagated_delta=float(value), radiation_retaining_delta=full, relative_difference=error))
    log('stage50_handoff_complete', rows=handoffs)
    check('no bytecode caches', not list(ROOT.rglob('__pycache__')))
    passed = all(row['passed'] for row in checks)
    save('validation', __file__, dict(checks=checks, count=len(checks), all_checks_passed=passed,
        switching=switching, sensitivity=sensitivities, refined_matching=refined_match, refined_rows=refined_rows,
        earlier_rows=earlier_rows, independent_implicit_errors=independent_errors,
        zero_fraction_errors=zero_errors, stage50_handoff=handoffs, elapsed_seconds=time.monotonic() - started,
        claim_scope='Shared regular adiabatic early transfer in perfect-radiation/cold/scalar subsystem; no likelihood or full Boltzmann accuracy claim.'),
        [ROOT / 'results/matching/status.json', ROOT / 'results/preflight/status.json', PARENT / 'results/validation/status.json', ROOT / 'run_early_match.py'])
    (folder / ('COMPLETE' if passed else 'FAILED')).write_text(datetime.now(timezone.utc).isoformat() + '\n', encoding='utf-8')
    log('complete' if passed else 'failed', checks=len(checks), failed=sum(not row['passed'] for row in checks))
    assert passed, 'Validation failures saved; do not seal as accepted.'


if __name__ == '__main__':
    main()
