from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import psutil
from scipy import linalg

from sequence_tools import SequenceProfile, build, digest


ROOT = Path(__file__).resolve().parent


def supported_values(profile, positions):
    amplitude, density = np.zeros_like(positions), np.zeros_like(positions)
    inside = positions < profile.radius
    field, gradient, mass, metric, xi, rotation = profile.values(positions[inside])
    amplitude[inside] = field
    density[inside] = positions[inside]**2*field*rotation
    return amplitude, density


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--cells', type=int, nargs='+', default=[256, 512, 1024])
    args = parser.parse_args()
    source = ROOT/'results/tangent-window/status.json'
    report = json.loads(source.read_text(encoding='utf-8'))
    assert report['state'] == 'complete' and len(report['rows']) == 5
    profiles = [SequenceProfile(source.parent/row['archive'], row) for row in report['rows']]
    center = profiles[2]
    output = ROOT/'results'/args.label
    output.mkdir(exist_ok=False)
    result = {'state': 'running', 'source_sha256': digest(source), 'script_sha256': digest(Path(__file__)),
              'helper_sha256': digest(ROOT/'sequence_tools.py'), 'rows': []}
    try:
        for cells in args.cells:
            system = build(center, cells, 8)
            values, vectors = linalg.eigh(system['pulsation'], subset_by_index=[0, 3], check_finite=False)
            positions = system['quadrature'].position
            weights = system['quadrature'].weights
            pair_results = []
            for lower, upper in [(0, 4), (1, 3)]:
                step = (profiles[upper].row['control_value']-profiles[lower].row['control_value'])/2
                minus_field, minus_density = supported_values(profiles[lower], positions)
                plus_field, plus_density = supported_values(profiles[upper], positions)
                tangent_amplitude = (plus_field-minus_field)/(2*step)
                tangent_density = (plus_density-minus_density)/(2*step)
                amplitude_load = system['basis'].T@(weights*positions*tangent_amplitude)
                density_load = system['phase_basis'].T@(weights*tangent_density)
                amplitude_white = linalg.solve_triangular(system['factor_amplitude'], amplitude_load, lower=True)
                density_white = linalg.solve_triangular(system['factor_phase'], density_load, lower=True)
                reduced = np.concatenate([amplitude_white, system['quotient'].T@density_white])
                tangent = linalg.solve_triangular(system['dynamic_factor'], reduced, lower=True)
                tangent /= linalg.norm(tangent)
                action = system['pulsation']@tangent
                charge_prime = 4*np.pi*float(weights@tangent_density)
                absolute_charge_prime_scale = 4*np.pi*float(weights@abs(tangent_density))
                finite_charge_prime = (profiles[upper].row['charge']-profiles[lower].row['charge'])/(2*step)
                energy_prime = (profiles[upper].row['adm_energy']-profiles[lower].row['adm_energy'])/(2*step)
                data = {'step': step, 'overlap_with_lowest_mode': float(abs(vectors[:, 0]@tangent)),
                        'tangent_rayleigh_frequency_squared': float(tangent@action),
                        'pulsation_action_norm_on_unit_tangent': float(linalg.norm(action)),
                        'charge_derivative_by_field_integral': charge_prime,
                        'charge_derivative_by_backgrounds': finite_charge_prime,
                        'charge_tangency_error_over_absolute_density_variation': abs(charge_prime)/absolute_charge_prime_scale,
                        'charge_projection_fraction_in_whitened_density': float(abs(system['charge_vector']@density_white)/(linalg.norm(system['charge_vector'])*linalg.norm(density_white))),
                        'finite_step_first_law_absolute_residual': float(abs(energy_prime-center.frequency*finite_charge_prime)),
                        'fixed_physical_radius_used': True}
                pair_results.append(data)
                np.savez_compressed(output/f'tangent-N{cells}-step{step:.7f}.npz', tangent=tangent,
                                    fundamental_mode=vectors[:, 0], position=positions,
                                    amplitude_tangent=tangent_amplitude, canonical_density_tangent=tangent_density)
            modes = system['dynamic_factor']@vectors
            residual = linalg.norm(system['dynamic']@(system['even']@modes)-modes*values, axis=0)
            scaled = residual/(np.maximum(abs(values), 1e-7)*linalg.norm(modes, axis=0))
            row = {'cells': cells, 'central_target': center.row['control_value'], 'frequency_squared': values.tolist(),
                   'maximum_scaled_eigen_equation_residual': float(max(scaled)), 'tangent_checks': pair_results}
            result['rows'].append(row)
            (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
            print(json.dumps(row), flush=True)
        result['state'] = 'complete'
    except Exception as error:
        result['state'] = 'failed'
        result['error'] = repr(error)
        raise
    finally:
        (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
