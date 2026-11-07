from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil
from scipy.interpolate import PPoly

from companion_system import ROOT, BRANCH, CompanionProblem, determinant, static_master_basis, propagate, horizon_samples, horizon_coefficients, reference_wave, source_jumps, encode


def decode(value):
    return complex(value['real'], value['imaginary'])


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/controls'
    output.mkdir(exist_ok=False)
    problem = CompanionProblem()
    radius, mass = problem.radius, problem.mass
    horizon, normalization, _ = horizon_samples(mass, 0., [radius, 2*radius, 4*radius])
    static_controls = []
    surface_growing = static_master_basis(radius, mass, radius)[:, 0]
    for position, value in horizon.items():
        basis = static_master_basis(position, mass, radius)
        coefficients = np.linalg.solve(basis, value)
        static_controls.append({'radius_over_body_radius': position/radius,
                                'static_regular_shape_error': float(np.max(abs(value-basis[:, 0]/surface_growing[0])/(1+abs(value)))),
                                'static_decaying_over_growing_scaled': encode(coefficients[1]/coefficients[0])})
    extraction, basis_controls, source_work = [], [], []
    for separation in [2., 10., 40.]:
        orbit = separation*radius
        reference = reference_wave(orbit, mass, radius)
        sigma = reference['sigma']
        inside, solution, _ = problem.interior.interior(sigma)
        inside /= inside[0]
        black_hole, outgoing = reference['horizon'][radius], reference['outgoing'][radius]
        jump_value, jump_slope = source_jumps(orbit, mass)
        outgoing_overlap = jump_slope*reference['outgoing'][orbit][0]-jump_value*reference['outgoing'][orbit][1]
        horizon_overlap = jump_slope*reference['horizon'][orbit][0]-jump_value*reference['horizon'][orbit][1]
        original = -determinant(inside, black_hole)/determinant(inside, outgoing)*outgoing_overlap/horizon_overlap
        for fraction in [1.2, 1.5]:
            stacked = propagate(radius, fraction*radius, mass, sigma, np.column_stack([inside, black_hole, outgoing]))
            shifted = -determinant(stacked[:, 0], stacked[:, 1])/determinant(stacked[:, 0], stacked[:, 2])*outgoing_overlap/horizon_overlap
            extraction.append({'separation_over_radius': separation, 'extraction_over_radius': fraction,
                               'relative_excess_difference': abs(shifted/original-1)})
        for fraction in [2., 3., 4.]:
            basis = propagate(fraction*radius, radius, mass, sigma, static_master_basis(fraction*radius, mass, radius))
            coefficients = np.linalg.solve(basis, np.column_stack([inside, black_hole, outgoing]))
            rebuilt = -determinant(coefficients[:, 0], coefficients[:, 1])/determinant(coefficients[:, 0], coefficients[:, 2])*outgoing_overlap/horizon_overlap
            basis_controls.append({'separation_over_radius': separation, 'reference_buffer_over_radius': fraction,
                                   'relative_excess_difference': abs(rebuilt/original-1)})
        source_work.append({'separation_over_radius': separation,
                            'outgoing_source_overlap': encode(outgoing_overlap), 'horizon_source_overlap': encode(horizon_overlap)})
    unit_control = []
    for reference_mass in [.296546804477414, 2.3]:
        row = reference_wave(7.9456*reference_mass, reference_mass)
        unit_control.append({'mass': reference_mass, 'mass_squared_times_reference_flux': reference_mass**2*row['pair_power_infinity_per_geometric_particle_mass_squared']})
    coefficients_control = []
    for mass_frequency in [0., .00001, .003, .09]:
        order = 8
        coefficients = horizon_coefficients(.5, mass_frequency, order)
        second = np.array([0, 49, 154, 177, 88, 16], dtype=complex)
        first = np.array([49, 105, 72, 16, 0, 0], dtype=complex)-2j*mass_frequency*np.array([49, 203, 331, 265, 104, 16])
        zeroth = np.array([-189, -420, -336, -96], dtype=complex)
        first_derivative = np.arange(1, order+1)*coefficients[1:]
        second_derivative = np.arange(1, order)*first_derivative[1:]
        residual = np.polynomial.polynomial.polyadd(np.polynomial.polynomial.polymul(second, second_derivative),
                    np.polynomial.polynomial.polyadd(np.polynomial.polynomial.polymul(first, first_derivative), np.polynomial.polynomial.polymul(zeroth, coefficients)))
        coefficients_control.append({'scaled_frequency': mass_frequency, 'first_eight_residuals_maximum': float(max(abs(residual[:order])))})
    parent_residue = json.loads((BRANCH/'retarded-response-20261004/results/refined-residue/status.json').read_text())
    frequency = decode(parent_residue['corrected_pole']).real
    exterior_maximum = 2*np.sqrt(mass/radius**3)
    resonance_radius = (4*mass/frequency**2)**(1/3)
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'system_sha256': hashlib.sha256((ROOT/'companion_system.py').read_bytes()).hexdigest(),
              'static_horizon_controls': static_controls, 'fixed_source_extraction_controls': extraction,
              'matching_convention_controls': basis_controls, 'unit_scaling_controls': unit_control,
              'horizon_series_controls': coefficients_control, 'source_overlap_controls': source_work,
              'circular_resonance': {'mode_frequency': frequency, 'maximum_exterior_circular_m2_frequency': exterior_maximum,
                                      'maximum_drive_over_mode': exterior_maximum/frequency,
                                      'formal_resonance_radius': resonance_radius, 'formal_resonance_radius_over_body_radius': resonance_radius/radius,
                                      'external_circular_resonance_accessible': bool(resonance_radius >= radius)},
              'interior_evaluations': 3,
              'scope': 'Selected quadrupole and selected weak body; circular test companion only. Eccentric higher harmonics and other modes are not excluded by the circular resonance check.'}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
