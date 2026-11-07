from __future__ import annotations

from datetime import datetime, timezone
import json
import math
import time

import numpy as np

from early_common import ROOT, MASS, FRACTION, AMPLITUDE, MODES, Environment, modest_process, calibrate, exact_evolution, extract_match, fluid_evolution, cold_evolution, save


def summarize(environment, solution, control, match):
    rows = []
    for index, (wave, preparation) in enumerate(MODES):
        state = solution.y[:, -1].reshape(-1, 7)[index]
        cold_index = [.1, 1., 5.].index(wave)
        cold_control = control.y[:, -1].reshape(-1, 5)[cold_index, 0]
        expansion = environment.fluid_values(0.)[3]
        wave_ratio2 = (299792.458 * wave / 70. / expansion)**2
        total = (1 - FRACTION) * state[0] + FRACTION * state[4]
        comoving = total + 3 * FRACTION * state[5] / wave_ratio2
        rows.append(dict(k_Mpc_inverse=wave, preparation=preparation, matching_a=match['scale'],
            final_state=state.tolist(), cold_control_delta=float(cold_control), total_delta=float(total),
            comoving_matter_delta=float(comoving), density_ratio=float(total / cold_control),
            comoving_ratio=float(comoving / cold_control),
            ratio_interpretation='adiabatic transfer relative to same-curvature cold control' if preparation == 'adiabatic' else 'independent field seed response relative to adiabatic cold seed; not a prediction without covariance'))
    return rows


def main():
    modest_process()
    started = time.monotonic()
    folder = ROOT / 'runs/matching'
    folder.mkdir(parents=True, exist_ok=False)

    def log(event, **payload):
        record = dict(event=event, time_utc=datetime.now(timezone.utc).isoformat(), seconds=time.monotonic() - started, **payload)
        with (folder / 'log.txt').open('a', encoding='utf-8') as handle:
            handle.write(json.dumps(record, allow_nan=False) + '\n')
        print(record, flush=True)

    environment = Environment()
    log('started', mass_over_H0=MASS, heavy_dust_fraction=FRACTION, omega_m=environment.matter, omega_r=environment.radiation, frozen_early_dark=environment.frozen_dark)
    displacement, calibration = calibrate(environment)
    log('calibrated', displacement=displacement, calibration=calibration)
    exact = exact_evolution(environment, displacement)
    log('exact_onset_complete', nfev=exact.nfev, steps=len(exact.t))
    samples = np.linspace(exact.t[0], exact.t[-1], 800)
    np.savez_compressed(folder / 'exact-samples.npz', efolds=samples, states=exact.sol(samples))
    controls = cold_evolution(environment)
    log('cold_control_complete', nfev=controls.nfev)
    matches, outcomes = [], []
    for scale in [.0002, .0003, .00045]:
        match = extract_match(environment, exact, scale)
        matches.append(match)
        log('match_projected', match=match)
        fluid = fluid_evolution(environment, match)
        rows = summarize(environment, fluid, controls, match)
        outcomes.extend(rows)
        log('late_evolution_complete', matching_a=scale, nfev=fluid.nfev, rows=rows)
    projections = [extract_match(environment, exact, .0003, half_width=width * math.pi) for width in [4, 12]]
    save('matching', __file__, dict(displacement=displacement, calibration=calibration, mass_over_H0=MASS,
        heavy_dust_fraction=FRACTION, omega_m=environment.matter, omega_r=environment.radiation,
        frozen_early_dark=environment.frozen_dark, starting_a=1e-9, seed_amplitude=AMPLITUDE,
        matches=matches, window_sensitivity=projections, rows=outcomes,
        exact_nfev=exact.nfev, control_nfev=controls.nfev, elapsed_seconds=time.monotonic() - started,
        background_parameters_refitted=False, observations_fitted=False, full_Boltzmann_evolution=False,
        heavy_abundance_derived=False, primordial_covariance_derived=False), [folder / 'exact-samples.npz'])
    (folder / 'COMPLETE').write_text(datetime.now(timezone.utc).isoformat() + '\n', encoding='utf-8')
    log('complete', rows=len(outcomes))


if __name__ == '__main__':
    main()
