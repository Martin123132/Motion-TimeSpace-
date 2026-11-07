from nonlocal_common import *


def main():
    modest()
    folder = ROOT / 'results/infrared-domain-corrected'
    folder.mkdir(parents=True, exist_ok=False)
    source = ROOT / 'results/infrared-domain/status.json'
    original = json.loads(source.read_text())
    rows, checks = [], []
    for row in original['rows']:
        background = thermal_wave.thermal.ThermalBackground(row['model'])
        constants = background.constants
        theta = row['temperature']
        scale = background.theta0 / theta
        electron_density = background.electron0 / scale**3
        reduced_wavelength = 6.62607015e-34 / (2 * np.pi * constants['m_e'] * constants['c'])
        corrected = math.sqrt(4 * np.pi * integrated_dc.ALPHA * electron_density * reduced_wavelength**3) / theta
        classical_radius = math.sqrt(3 * constants['sigma_thomson'] / (8 * np.pi))
        thomson_check = reduced_wavelength * math.sqrt(4 * np.pi * electron_density * classical_radius) / theta
        checks.append(check('Plasma scale independently reconstructed from native Thomson radius '
                            + row['model'] + row['source'] + str(row['history_fraction']),
                            abs(corrected / thomson_check - 1), 1e-7))
        revised = dict(row)
        revised['superseded_missing_pi_plasma_value'] = revised['plasma_frequency_over_temperature']
        revised['plasma_frequency_over_temperature'] = corrected
        revised['electron_density_SI'] = electron_density
        rows.append(revised)
    finish(folder, dict(checks=checks, count=len(checks),
           all_checks_passed=all(row['passed'] for row in checks), rows=rows,
           authoritative_for_plasma_scale=True, supersedes=str(source),
           correction='Restores pi in omega_p^2=4pi alpha n_e reduced_Compton_wavelength^3 in electron-rest-energy units. Original diagnostic is retained. This quantity was not used in any evolution or spectral kernel.',
           source_slope_and_spectral_results_unchanged=True, historical_evolutions_affected=False), __file__, [source])
    print(json.dumps(dict(failed=[row for row in checks if not row['passed']],
                         midpoint_plasma=rows[1]['plasma_frequency_over_temperature'])), flush=True)


if __name__ == '__main__':
    main()
