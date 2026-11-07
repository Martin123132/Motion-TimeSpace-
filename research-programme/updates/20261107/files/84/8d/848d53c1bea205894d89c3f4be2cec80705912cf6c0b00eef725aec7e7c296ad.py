from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import numpy as np
import psutil

from axial_wave import ROOT, BRANCH, WaveBody, flat_impedance, static_outgoing, vacuum_impedance


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', choices=['coarse', 'fine'], required=True)
    arguments = parser.parse_args()
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results'/arguments.label
    output.mkdir(parents=True, exist_ok=False)
    fine = arguments.label == 'fine'
    settings = {'tolerance': 3e-12 if fine else 1e-10, 'max_step': 1/240 if fine else 1/100, 'start': 1e-5 if fine else 2e-5}
    exterior = {'tolerance': 3e-12 if fine else 1e-10, 'phase': 80. if fine else 50., 'order': 14 if fine else 10, 'horizon': 3e-6 if fine else 1e-5}
    parent_path = BRANCH/'axial-tides-20261004/results/fine-v2/status.json'
    parent = json.loads(parent_path.read_text(encoding='utf-8'))
    input_hashes = {str(parent_path): digest(parent_path)}
    static_rows = []
    for nominal in ([0., .0001, .003, .03] if fine else [.03]):
        body = WaveBody(nominal)
        static, solution = body.solve(0., variations=True, **settings)
        parent_row = next(row for row in parent['rows'] if row['nominal_flat_compactness'] == nominal)
        response = body.recover_static(static['Y'])
        static_rows.append({'nominal': nominal, 'radius': body.radius, 'mass': body.mass, **static,
                            'response_reconstructed': response, 'response_parent': parent_row['response'],
                            'response_relative_error': abs(response/parent_row['response']-1) if parent_row['response'] else abs(response),
                            'integral_variational_identity_error': abs(static['Y_frequency_squared_coefficient']+static['I_over_R'])})
        input_hashes[str(body.profile.path)] = digest(body.profile.path)
    body = WaveBody(.03)
    static, static_solution = body.solve(0., variations=True, **settings)
    static_out = static_outgoing(body.compactness)
    static_bh = 3*(1-body.compactness)
    kernel_zero = 1/(static['Y']-static_out)
    difference_zero = kernel_zero-1/(static_bh-static_out)
    spectral_floor = 3*body.central_lapse**2
    coordinates = np.linspace(1e-5, 1-1e-7, 8001)
    field, gradient, mass, metric, xi, canonical = body.profile.values(body.radius*coordinates)
    lapse = xi*np.sqrt(metric)
    rotation = body.profile.frequency**2*field**2/lapse**2
    from axial_wave import potential
    density = .5*(metric*gradient**2+rotation)+potential(field)
    pressure = density-2*potential(field)
    potential_dimensionless = lapse**2*((3+3*metric)/coordinates**2+2*body.alpha*body.radius**2*potential(field))
    background = {'central_lapse': body.central_lapse, 'minimum_sampled_lapse': float(np.min(lapse)),
                  'minimum_sampled_F': float(np.min(metric)), 'minimum_sampled_pr': float(np.min(pressure)),
                  'minimum_sampled_dimensionless_V': float(np.min(potential_dimensionless)),
                  'dimensionless_Dirichlet_spectral_floor': spectral_floor}
    sample_frequencies = []
    for ratio, separations in [(.01, [40., 20., 10., 5.]), (1., [5.])]:
        for separation in separations:
            frequency = np.sqrt(body.mass*(1+ratio)/(separation**3*body.radius))
            sample_frequencies.append((f'orbital_mu{ratio}_d{separation}', frequency, ratio, separation))
    sample_frequencies += [(f'frequency_control_{frequency}', frequency, None, None) for frequency in [.1, .3, 1.]]
    rows = []
    for label, frequency, ratio, separation in sample_frequencies:
        response, solution = body.solve(frequency, **settings)
        outgoing, outgoing_evaluations = vacuum_impedance(body.compactness, frequency, True, **exterior)
        black_hole, horizon_evaluations = vacuum_impedance(body.compactness, frequency, False, **exterior)
        squared = frequency**2
        taylor = static['Y']-squared*static['I_over_R']
        fourth_order = taylor+squared**2*static['Y_frequency_fourth_coefficient']
        remainder_bound = squared**2*static['I_over_R']/(spectral_floor-squared)
        kernel = 1/(response['Y']-outgoing)
        kernel_static_boundary = 1/(static['Y']-outgoing)
        kernel_taylor = 1/(taylor-outgoing)
        kernel_fourth = 1/(fourth_order-outgoing)
        kernel_bh = 1/(black_hole-outgoing)
        difference = kernel-kernel_bh
        denominator_margin = abs(taylor-outgoing)-remainder_bound
        assert denominator_margin > 0
        kernel_error_bound = remainder_bound/(abs(taylor-outgoing)*denominator_margin)
        row = {'label': label, 'frequency_R': frequency, 'companion_to_body_mass': ratio, 'd0_over_R': separation,
               **response, 'Y_taylor_quadratic': taylor, 'Y_taylor_quartic': fourth_order,
               'signed_remainder': taylor-response['Y'], 'quadratic_remainder_bound': remainder_bound,
               'Y_out_real': outgoing.real, 'Y_out_imag': outgoing.imag,
               'Y_BH_real': black_hole.real, 'Y_BH_imag': black_hole.imag,
               'surface_kernel_real': kernel.real, 'surface_kernel_imag': kernel.imag,
               'body_minus_BH_kernel_real': difference.real, 'body_minus_BH_kernel_imag': difference.imag,
               'body_minus_BH_kernel_ratio_to_static_real': (difference/difference_zero).real,
               'body_minus_BH_kernel_ratio_to_static_imag': (difference/difference_zero).imag,
               'surface_static_boundary_relative_error': abs(kernel_static_boundary/kernel-1),
               'surface_quadratic_boundary_relative_error': abs(kernel_taylor/kernel-1),
               'surface_quartic_boundary_relative_error': abs(kernel_fourth/kernel-1),
               'quadratic_kernel_absolute_error': abs(kernel_taylor-kernel),
               'quadratic_kernel_absolute_error_bound': kernel_error_bound,
               'quadratic_body_difference_relative_error': abs((kernel_taylor-kernel)/difference),
               'spectral_frequency_ratio': squared/spectral_floor,
               'retarded_denominator_abs': abs(response['Y']-outgoing),
               'outgoing_evaluations': outgoing_evaluations, 'horizon_evaluations': horizon_evaluations}
        rows.append(row)
        print(json.dumps({'label': label, 'frequency_R': frequency, 'quadratic_error': row['surface_quadratic_boundary_relative_error'],
                          'contrast_ratio': row['body_minus_BH_kernel_ratio_to_static_real']}), flush=True)
    flat_rows = []
    flat_body = WaveBody(0.)
    for frequency in [.001, .01, .1]:
        response, solution = flat_body.solve(frequency, **settings)
        outgoing, evaluations = vacuum_impedance(0., frequency, True, **exterior)
        exact_inner = flat_impedance(frequency)
        exact_outgoing = flat_impedance(frequency, outgoing=True)
        full = 1/(response['Y']-outgoing)
        exact = 1/(exact_inner-exact_outgoing)
        frozen = 1/(3-outgoing)
        flat_rows.append({'frequency_R': frequency, 'interior_error': abs(response['Y']-exact_inner),
                          'outgoing_error': abs(outgoing-exact_outgoing), 'full_kernel_error': abs(full-exact),
                          'spurious_contrast_when_freezing_full_Y': abs(frozen-exact)})
    with (output/'response.csv').open('x', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'system_sha256': digest(ROOT/'axial_wave.py'),
              'completed_at_utc': datetime.now(timezone.utc).isoformat(), 'settings': settings, 'exterior_settings': exterior,
              'input_hashes': input_hashes, 'body_radius': body.radius, 'body_mass': body.mass,
              'static_rows': static_rows, 'static_reference': static, 'background': background,
              'static_surface_kernel': kernel_zero, 'static_body_minus_BH_kernel': difference_zero,
              'rows': rows, 'flat_controls': flat_rows, 'csv_sha256': digest(output/'response.csv'),
              'response_definition': 'Dimensionless surface retarded resolvent K/R=1/(Y_regular-Y_out), Y=R*d_rstar U/U at R.',
              'contrast_definition': 'Same-mass body-minus-BH surface resolvent, not an extracted dynamical Love coefficient.',
              'orbital_frequencies': 'Omega*R=sqrt(M_body*(1+epsilon)/(R*(d0/R)^3)); leading axial l2,m1 forcing.',
              'spectral_bound_status': 'Analytic conditional bound using inherited numerical central lapse; no interval-arithmetic certification.',
              'static_freeze_warning': 'Freezing the full impedance is not the same as holding the material Love coefficient fixed; flat control exhibits the difference.'}
    with (output/'status.json').open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    print(json.dumps({'state': 'complete', 'label': arguments.label, 'rows': len(rows), 'static_rows': len(static_rows)}))


if __name__ == '__main__':
    main()
