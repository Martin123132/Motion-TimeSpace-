from __future__ import annotations

import json
import numpy as np
import sympy as sym

from radiation_common import *


def main():
    modest_process()
    checks = []

    def check(name, passed, value=None):
        checks.append(dict(name=name, passed=bool(passed), value=value))

    for path, expected in inputs().items():
        check('input:' + Path(path).name, Path(path).is_file() and len(expected) == 64)
    check('same native solver version as 5194', camb.__version__ == '1.6.6')
    table = np.loadtxt(BAO_MEAN, dtype=str)
    covariance = np.loadtxt(BAO_COV)
    check('DESI dimensions', table.shape == (13, 3) and covariance.shape == (13, 13))
    check('DESI covariance positive and symmetric', np.min(np.linalg.eigvalsh(covariance)) > 0 and np.max(abs(covariance - covariance.T)) < 1e-12)
    check('DESI observable labels', set(table[:, 2]) <= {'DM_over_rs', 'DH_over_rs', 'DV_over_rs'})
    check('DESI redshift and measured values positive', np.all(table[:, :2].astype(float) > 0))
    omega_m, slow_mass = inherited_parameters()
    species = StandardSpecies(omega_m, .5)
    check('positive cold density after explicit baryon and neutrino split', species.coefficients['cdm'] > 0)
    check('matter budget', abs(species.params.omegam + .5 * omega_m - omega_m) < 1e-13)
    sample = species.sample(np.array([START, -8., -4., 0.]))
    check('all five standard species present and positive', len(sample) == 5 and all(np.all(values > 0) for values in sample.values()))
    early_w = (1 - species.nu_log(START, 1)) / 3
    late_w = (1 - species.nu_log(0., 1)) / 3
    check('massive neutrino radiation and matter limits', abs(early_w - 1 / 3) < 1e-8 and 0 <= late_w < .001, [float(early_w), float(late_w)])
    perturbation, heavy_sound2 = sym.symbols('delta_rho cs_h2')
    pressure_at_zero_total_density = heavy_sound2 * perturbation - perturbation
    check('relative entropy forbids replacing two fields by one fixed-sound-speed fluid',
        sym.simplify(pressure_at_zero_total_density - (heavy_sound2 - 1) * perturbation) == 0
        and pressure_at_zero_total_density != 0)
    check('maximum switch inside exact background support', .00025 < EXACT_END)
    passed = all(row['passed'] for row in checks)
    save('preflight', __file__, dict(count=len(checks), checks=checks, all_checks_passed=passed,
        full_heavy_Boltzmann_supported_by_existing_binary=False,
        intended_native_heavy_use='Background and recombination only; no single-fluid heavy perturbation substitution.',
        standard_species_coefficients=species.coefficients, omega_m=omega_m, slow_mass_over_H0=slow_mass))
    print(json.dumps(dict(checks=len(checks), passed=passed, failed=[row for row in checks if not row['passed']])), flush=True)
    assert passed


if __name__ == '__main__':
    main()

