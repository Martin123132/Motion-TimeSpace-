from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from numpy.polynomial import Polynomial

from sequence_tools import digest


ROOT = Path(__file__).resolve().parent


def main():
    source = ROOT/'results/turning-window/status.json'
    report = json.loads(source.read_text(encoding='utf-8'))
    assert report['state'] == 'complete'
    rows = report['rows']
    centers = np.array([row['control_value'] for row in rows])
    charges = np.array([row['charge'] for row in rows])
    energies = np.array([row['adm_energy'] for row in rows])
    frequencies = np.array([row['frequency_at_infinity'] for row in rows])
    middle = float(np.mean(centers))
    span = float(np.ptp(centers)/2)
    coordinate = (centers-middle)/span
    comparisons = []
    for degree in [3, 4, 5]:
        charge = Polynomial.fit(coordinate, charges-charges[0], degree).convert()
        energy = Polynomial.fit(coordinate, energies-energies[0], degree).convert()
        frequency = Polynomial.fit(coordinate, frequencies, degree).convert()
        charge_roots = [float(value.real) for value in charge.deriv().roots() if abs(value.imag) < 1e-9 and -1 < value.real < 1]
        energy_roots = [float(value.real) for value in energy.deriv().roots() if abs(value.imag) < 1e-9 and -1 < value.real < 1]
        assert len(charge_roots) == len(energy_roots) == 1
        charge_root, energy_root = charge_roots[0], energy_roots[0]
        law = energy.deriv()-frequency*charge.deriv()
        samples = np.linspace(-.8, .8, 81)
        derivative_scale = float(np.max(abs(frequency(samples)*charge.deriv()(samples)/span)))
        first_law_error = float(np.max(abs(law(samples)/span)))
        integrated_prediction = (frequency*charge.deriv()).integ()
        predicted_energy_change = float(integrated_prediction(1)-integrated_prediction(-1))
        comparisons.append({'degree': degree, 'charge_turning_center': middle+span*charge_root,
                            'mass_turning_center': middle+span*energy_root,
                            'charge_second_derivative': float(charge.deriv(2)(charge_root)/span**2),
                            'charge_at_turn': float(charge(charge_root)+charges[0]),
                            'energy_at_turn': float(energy(charge_root)+energies[0]),
                            'maximum_first_law_derivative_absolute_residual': first_law_error,
                            'maximum_first_law_residual_over_window_derivative_scale': first_law_error/derivative_scale,
                            'observed_energy_change': float(energies[-1]-energies[0]),
                            'integrated_first_law_energy_change': predicted_energy_change,
                            'integrated_first_law_absolute_difference': float(abs(predicted_energy_change-(energies[-1]-energies[0])))})
    output = ROOT/'results/turning-location'
    output.mkdir(exist_ok=False)
    result = {'state': 'complete', 'source_sha256': digest(source), 'script_sha256': digest(Path(__file__)),
              'center_window': [float(min(centers)), float(max(centers))], 'comparisons': comparisons,
              'selected_center': comparisons[-1]['charge_turning_center'],
              'polynomial_sensitivity_is_not_a_certified_error_bound': True}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
