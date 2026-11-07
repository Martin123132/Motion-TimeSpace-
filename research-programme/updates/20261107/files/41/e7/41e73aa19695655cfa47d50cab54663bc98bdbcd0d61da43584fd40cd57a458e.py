from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import psutil
from scipy import linalg


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'radial-pulsations-20261003'))
from solve_pulsations import Profile, whiten
from test_radial_energy import Quadrature, potential_prime


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def build(profile, cells, order, harmonic):
    quadrature = Quadrature(profile.radius, cells, order)
    position = quadrature.position
    field, gradient, mass, metric, xi, rotation = profile.values(position)
    assert profile.alpha == 0 and np.allclose(metric, 1.)
    basis = quadrature.basis
    value = basis/position[:, None]
    derivative = quadrature.derivative/position[:, None]-basis/position[:, None]**2
    angular = harmonic*(harmonic+1)
    second = field**(-2/3)/6+1.5*field**2
    amplitude_mass = quadrature.form(basis, np.ones_like(position))
    amplitude_factor = linalg.cholesky(amplitude_mass, lower=True)
    amplitude_raw = quadrature.form(derivative, position**2)+quadrature.form(value, angular+position**2*(second-profile.frequency**2))
    amplitude = whiten(amplitude_raw, amplitude_factor)
    nodes = np.polynomial.legendre.leggauss(order)[0]
    right, right_prime = np.zeros_like(position), np.zeros_like(position)
    right[-order:], right_prime[-order:] = (1+nodes)/2, 1/quadrature.width
    phase_basis = np.column_stack([basis, right])
    phase_derivative = np.column_stack([quadrature.derivative, right_prime])
    phase_mass = quadrature.form(phase_basis, position**2*field**2)
    phase_factor = linalg.cholesky(phase_mass, lower=True)
    phase_raw = quadrature.form(phase_derivative, position**2*field**2)+quadrature.form(phase_basis, angular*field**2)
    phase = whiten(phase_raw, phase_factor)
    overlap_raw = quadrature.form(basis, position*field, phase_basis)
    mixed = 2*profile.frequency*whiten(overlap_raw, amplitude_factor, phase_factor)
    even = np.block([[amplitude+mixed@mixed.T, -mixed], [-mixed.T, np.eye(phase.shape[0])]])
    dynamic_factor = linalg.block_diag(np.eye(amplitude.shape[0]), linalg.cholesky(phase, lower=True))
    pulsation = dynamic_factor.T@even@dynamic_factor
    pulsation = (pulsation+pulsation.T)/2
    source = 2*position**2*(potential_prime(field)-2*profile.frequency**2*field)
    source_load = basis.T@(quadrature.weights*position*source)
    source_white = linalg.solve_triangular(amplitude_factor, source_load, lower=True)
    return {'quadrature': quadrature, 'field': field, 'gradient': gradient, 'basis': basis,
            'amplitude': amplitude, 'phase': phase, 'amplitude_factor': amplitude_factor,
            'source': source, 'source_white': source_white, 'mixed': mixed, 'pulsation': pulsation}


def evaluate(profile, cells, order, output, direct):
    system = build(profile, cells, order, 2)
    stiffness, phase = system['amplitude'], system['phase']
    static_values = linalg.eigh(stiffness, subset_by_index=[0, 2], eigvals_only=True)
    phase_minimum = linalg.eigh(phase, subset_by_index=[0, 0], eigvals_only=True)[0]
    response = linalg.solve(stiffness, system['source_white'], assume_a='pos')
    susceptibility = float(response@system['source_white'])
    source_norm = float(system['quadrature'].integrate(system['quadrature'].position**2*system['source']**2))
    assert static_values[0] >= .9999*4/profile.radius**2
    assert phase_minimum >= .9999*6/profile.radius**2
    assert 0 < susceptibility < source_norm*profile.radius**2/4
    frequencies_squared = linalg.eigh(system['pulsation'], subset_by_index=[0, 3], eigvals_only=True)
    assert np.all(frequencies_squared > 0)
    lower_amplitude, lower_phase = 4/profile.radius**2, 6/profile.radius**2
    total = lower_amplitude+lower_phase+4*profile.frequency**2
    lower_frequency_squared = 2*lower_amplitude*lower_phase/(total+np.sqrt(total**2-4*lower_amplitude*lower_phase))
    assert frequencies_squared[0] >= .9999*lower_frequency_squared
    translation = build(profile, cells, order, 1)
    translation_values, translation_modes = linalg.eigh(translation['amplitude'], subset_by_index=[0, 0])
    quadrature = system['quadrature']
    translation_load = system['basis'].T@(quadrature.weights*quadrature.position*system['gradient'])
    translation_white = linalg.solve_triangular(system['amplitude_factor'], translation_load, lower=True)
    translation_overlap = abs(translation_modes[:, 0]@translation_white)/linalg.norm(translation_white)
    gyro_check = None
    if direct:
        mixed = system['mixed']
        gyro = np.block([[np.zeros_like(stiffness), -mixed], [mixed.T, np.zeros_like(phase)]])
        stiffness_pair = linalg.block_diag(stiffness, phase)
        size = len(stiffness_pair)
        generator = np.block([[np.zeros((size, size)), np.eye(size)], [-stiffness_pair, -gyro]])
        spectrum = linalg.eigvals(generator)
        positive = sorted(value.imag for value in spectrum if value.imag > 1e-6)
        gyro_check = {'maximum_absolute_real_part': float(max(abs(spectrum.real))),
                      'lowest_frequencies': positive[:4],
                      'maximum_relative_frequency_difference': float(max(abs(np.array(positive[:4])/np.sqrt(frequencies_squared)-1)))}
    coefficients = linalg.solve_triangular(system['amplitude_factor'].T, response, lower=False)
    archive = f'R{profile.radius:g}-N{cells}-G{order}.npz'
    np.savez_compressed(output/archive, nodal_position=np.linspace(0, profile.radius, cells+1),
                        amplitude_coefficients=coefficients, frequency_squared=frequencies_squared,
                        static_stiffness_eigenvalues=static_values)
    return {'radius': profile.radius, 'cells': cells, 'order': order, 'profile_path': str(profile.path),
            'profile_sha256': digest(profile.path), 'archive': archive, 'static_eigenvalues': static_values.tolist(),
            'phase_stiffness_minimum': float(phase_minimum), 'susceptibility': susceptibility,
            'susceptibility_upper_bound': source_norm*profile.radius**2/4,
            'linear_solve_relative_residual': float(linalg.norm(stiffness@response-system['source_white'])/linalg.norm(system['source_white'])),
            'frequency_squared': frequencies_squared.tolist(), 'frequencies': np.sqrt(frequencies_squared).tolist(),
            'analytic_frequency_lower_bound': float(np.sqrt(lower_frequency_squared)),
            'translation_static_eigenvalue': float(translation_values[0]),
            'translation_mode_overlap': float(translation_overlap), 'independent_gyro_check': gyro_check}


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--radii', type=float, nargs='+', default=[8., 20., 80.])
    parser.add_argument('--cells', type=int, nargs='+', default=[128, 256, 512])
    parser.add_argument('--order', type=int, default=8)
    parser.add_argument('--direct', action='store_true')
    args = parser.parse_args()
    output = ROOT/'results'/args.label
    output.mkdir(parents=True, exist_ok=False)
    report = {'state': 'running', 'arguments': vars(args), 'script_sha256': digest(__file__),
              'parent_seal_sha256': digest(BRANCH/'collective-motion-20261004/results/stage-integrity.json'), 'rows': []}
    try:
        for radius in args.radii:
            profile = Profile(radius, 0.)
            for cells in args.cells:
                row = evaluate(profile, cells, args.order, output, args.direct)
                report['rows'].append(row)
                (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
                print(json.dumps(row), flush=True)
        report['state'] = 'complete'
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        raise
    finally:
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
