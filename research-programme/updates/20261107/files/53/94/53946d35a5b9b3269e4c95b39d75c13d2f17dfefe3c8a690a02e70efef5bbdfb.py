from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
import psutil
from scipy import linalg


ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent/'radial-gravity-stability-20261003'
sys.path.insert(0, str(PARENT))
from test_radial_energy import Profile, Quadrature, potential_prime


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def whiten(matrix, left_factor, right_factor=None):
    if right_factor is None:
        right_factor = left_factor
    left = linalg.solve_triangular(left_factor, matrix, lower=True, check_finite=False)
    return linalg.solve_triangular(right_factor, left.T, lower=True, check_finite=False).T


def orthogonal_complement(vector):
    unit = vector/linalg.norm(vector)
    reflector = unit.copy()
    reflector[-1] += 1 if unit[-1] >= 0 else -1
    reflection = np.eye(len(vector))-2*np.outer(reflector, reflector)/(reflector@reflector)
    basis = reflection[:, :-1]
    assert linalg.norm(basis.T@unit) < 1e-12
    return basis


def build(profile, cells, order):
    quadrature = Quadrature(profile.radius, cells, order)
    position, weights = quadrature.position, quadrature.weights
    field, gradient, mass, metric, xi, rotation = profile.values(position)
    coefficient = xi*metric
    basis = quadrature.basis
    gradient_basis = quadrature.derivative/position[:, None]-basis/position[:, None]**2
    value_basis = basis/position[:, None]
    nodes = np.polynomial.legendre.leggauss(order)[0]
    left, right = np.zeros(len(position)), np.zeros(len(position))
    left[:order], right[-order:] = (1-nodes)/2, (1+nodes)/2
    phase_basis = np.column_stack([left, basis, right])
    left_prime, right_prime = np.zeros(len(position)), np.zeros(len(position))
    left_prime[:order], right_prime[-order:] = -1/quadrature.width, 1/quadrature.width
    phase_derivative = np.column_stack([left_prime, quadrature.derivative, right_prime])
    phase_weight = position**2*field**2
    mass_amplitude = quadrature.form(basis, np.ones_like(position))
    mass_phase = quadrature.form(phase_basis, phase_weight)
    factor_amplitude = linalg.cholesky(mass_amplitude, lower=True, check_finite=False)
    factor_phase = linalg.cholesky(mass_phase, lower=True, check_finite=False)
    amplitude_size, phase_size = cells-1, cells+1
    force = potential_prime(field)
    potential_second = field**(-2/3)/6+1.5*field**2
    local_amplitude = quadrature.form(gradient_basis, coefficient*position**2)
    local_amplitude += quadrature.form(basis, xi*potential_second+3*profile.frequency**2/coefficient)
    local_density = quadrature.form(phase_basis, coefficient*phase_weight)
    local_mixed = -2*profile.frequency*quadrature.form(basis, position*field, phase_basis)
    kinetic_amplitude = 2*gradient[:, None]*gradient_basis-2*(profile.frequency**2*field/coefficient**2)[:, None]*value_basis
    kinetic_density = (2*profile.frequency*field**2/coefficient)[:, None]*phase_basis
    kinetic_variation = np.column_stack([kinetic_amplitude, kinetic_density])
    potential_variation = np.column_stack([force[:, None]*value_basis, np.zeros_like(phase_basis)])
    mass_source = xi[:, None]*position[:, None]**2*(metric[:, None]*kinetic_variation/2+potential_variation)
    mass_variation = quadrature.cumulative(mass_source)/xi[:, None]
    gravity_raw = -profile.alpha*kinetic_variation.T@((weights*xi*position)[:, None]*mass_variation)
    gravity = gravity_raw+gravity_raw.T
    even_amplitude = local_amplitude+gravity[:amplitude_size, :amplitude_size]
    even_density = local_density+gravity[amplitude_size:, amplitude_size:]
    even_mixed = local_mixed+gravity[:amplitude_size, amplitude_size:]
    even_amplitude = whiten(even_amplitude, factor_amplitude)
    even_density = whiten(even_density, factor_phase)
    even_mixed = whiten(even_mixed, factor_amplitude, factor_phase)
    phase_stiffness = quadrature.form(phase_derivative, coefficient*phase_weight)
    momentum_stiffness = quadrature.form(basis, coefficient)
    phase_white = whiten(phase_stiffness, factor_phase)
    momentum_white = whiten(momentum_stiffness, factor_amplitude)
    charge_vector = factor_phase.T@np.ones(phase_size)
    quotient = orthogonal_complement(charge_vector)
    density_reduced = quotient.T@even_density@quotient
    mixed_reduced = even_mixed@quotient
    even = np.block([[even_amplitude, mixed_reduced], [mixed_reduced.T, density_reduced]])
    even = (even+even.T)/2
    phase_reduced = quotient.T@phase_white@quotient
    phase_reduced = (phase_reduced+phase_reduced.T)/2
    momentum_white = (momentum_white+momentum_white.T)/2
    dynamic = linalg.block_diag(momentum_white, phase_reduced)
    dynamic_factor = linalg.block_diag(linalg.cholesky(momentum_white, lower=True, check_finite=False),
                                     linalg.cholesky(phase_reduced, lower=True, check_finite=False))
    pulsation = dynamic_factor.T@even@dynamic_factor
    pulsation = (pulsation+pulsation.T)/2
    zero_residual = linalg.norm(phase_white@charge_vector)/(linalg.norm(phase_white)*linalg.norm(charge_vector))
    return {'quadrature': quadrature, 'field': field, 'basis': basis, 'phase_basis': phase_basis,
            'mass_amplitude': mass_amplitude, 'mass_phase': mass_phase,
            'factor_amplitude': factor_amplitude, 'factor_phase': factor_phase,
            'phase_stiffness': phase_stiffness, 'phase_white': phase_white,
            'amplitude_gradient_form': quadrature.form(gradient_basis, position**2),
            'potential_second': potential_second, 'quotient': quotient, 'charge_vector': charge_vector,
            'even': even, 'dynamic': dynamic, 'dynamic_factor': dynamic_factor, 'pulsation': pulsation,
            'mass_variation': mass_variation, 'kinetic_variation': kinetic_variation,
            'phase_null_relative_residual': float(zero_residual)}


def independent_flat_gyro(profile, system, count):
    quadrature = system['quadrature']
    basis, phase_basis, field = system['basis'], system['phase_basis'], system['field']
    flat_amplitude = system['amplitude_gradient_form']+quadrature.form(basis, system['potential_second']-profile.frequency**2)
    stiffness = linalg.block_diag(whiten(flat_amplitude, system['factor_amplitude']), system['phase_white'])
    overlap = quadrature.form(basis, quadrature.position*field, phase_basis)
    mixed = 2*profile.frequency*whiten(overlap, system['factor_amplitude'], system['factor_phase'])
    gyro = np.block([[np.zeros((mixed.shape[0], mixed.shape[0])), -mixed],
                     [mixed.T, np.zeros((mixed.shape[1], mixed.shape[1]))]])
    size = len(stiffness)
    generator = np.block([[np.zeros((size, size)), np.eye(size)], [-stiffness, -gyro]])
    spectrum = linalg.eigvals(generator, check_finite=False)
    physical = sorted([value.imag for value in spectrum if value.imag > 1e-5])
    return {'lowest_frequencies': physical[:count], 'maximum_absolute_real_part': float(np.max(abs(spectrum.real))),
            'near_zero_count': int(np.sum(abs(spectrum) < 1e-5)),
            'independent_form': 'second-order Cartesian gyro equations, phase-adapted finite element space'}


def evaluate(profile, cells, order, output, direct=False):
    started = time.monotonic()
    system = build(profile, cells, order)
    values, vectors = linalg.eigh(system['pulsation'], subset_by_index=[0, 4], check_finite=False)
    even_values = linalg.eigh(system['even'], eigvals_only=True, subset_by_index=[0, 0], check_finite=False)
    assert values[0] > 0 and even_values[0] > 0
    frequencies = np.sqrt(values)
    modes = system['dynamic_factor']@vectors
    shape_count = cells-1
    amplitude_coefficients = linalg.solve_triangular(system['factor_amplitude'].T, modes[:shape_count], lower=False, check_finite=False)
    density_white = system['quotient']@modes[shape_count:]
    density_coefficients = linalg.solve_triangular(system['factor_phase'].T, density_white, lower=False, check_finite=False)
    original_coefficients = np.vstack([amplitude_coefficients, density_coefficients])
    source_modes = system['mass_variation']@original_coefficients
    charge_errors = abs(system['charge_vector']@density_white)/(linalg.norm(system['charge_vector'])*np.maximum(linalg.norm(density_white, axis=0), 1e-30))
    residuals = linalg.norm(system['dynamic']@(system['even']@modes)-modes*values, axis=0)/(np.maximum(values, 1e-30)*linalg.norm(modes, axis=0))
    direct_check = None
    if direct:
        size = len(system['even'])
        generator = np.block([[np.zeros((size, size)), system['dynamic']], [-system['even'], np.zeros((size, size))]])
        spectrum = linalg.eigvals(generator, check_finite=False)
        positive = sorted([value.imag for value in spectrum if value.imag > 1e-6])
        direct_check = {'maximum_absolute_real_part': float(np.max(abs(spectrum.real))),
                        'lowest_frequencies': positive[:5],
                        'relative_frequency_difference': float(np.max(abs(np.array(positive[:5])-frequencies)/frequencies))}
    flat_check = independent_flat_gyro(profile, system, 5) if direct and profile.alpha == 0 else None
    label = f'R{profile.row["base_radius"]:g}-C{profile.row["nominal_flat_compactness"]:g}-N{cells}-G{order}'.replace('.', 'p')
    np.savez_compressed(output/f'{label}.npz', frequency_squared=values, frequencies=frequencies,
                        nodal_position=np.linspace(0, profile.radius, cells+1),
                        amplitude_coefficients=amplitude_coefficients, density_coefficients=density_coefficients,
                        quadrature_position=system['quadrature'].position, mass_perturbation_modes=source_modes,
                        profile_radius=profile.radius, alpha=profile.alpha)
    return {'base_radius': profile.row['base_radius'], 'nominal_compactness': profile.row['nominal_flat_compactness'],
            'alpha': profile.alpha, 'radius': profile.radius, 'cells': cells, 'quadrature_order': order,
            'frequency_squared': values.tolist(), 'frequencies_at_infinity_in_mu_star_units': frequencies.tolist(),
            'fundamental_period_in_inverse_mu_star_units': float(2*np.pi/frequencies[0]),
            'fundamental_frequency_times_radius': float(frequencies[0]*profile.radius),
            'constrained_polar_energy_minimum': float(even_values[0]),
            'phase_null_relative_residual': system['phase_null_relative_residual'],
            'maximum_charge_tangent_relative_residual': float(np.max(charge_errors)),
            'maximum_second_order_relative_residual': float(np.max(residuals)),
            'direct_first_order_check': direct_check, 'independent_flat_gyro': flat_check,
            'profile_path': str(profile.path), 'profile_sha256': digest(profile.path),
            'archive': f'{label}.npz', 'seconds': time.monotonic()-started}


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--radii', nargs='+', type=float, default=[8., 20., 80.])
    parser.add_argument('--nominal', nargs='+', type=float, default=[0., .001, .03])
    parser.add_argument('--cells', nargs='+', type=int, default=[128, 256, 512])
    parser.add_argument('--order', type=int, default=8)
    parser.add_argument('--direct', action='store_true')
    arguments = parser.parse_args()
    output = ROOT/'results'/arguments.label
    output.mkdir(parents=True, exist_ok=False)
    report = {'state': 'running', 'arguments': vars(arguments), 'started': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(Path(__file__)), 'parent_seal_sha256': digest(PARENT/'results/stage-integrity.json'),
              'derivation_sha256': digest(ROOT/'results/derivation/status.json'),
              'one_worker_one_core': True, 'spectrum_kind': 'squared physical radial pulsation frequency in asymptotic dimensionless time', 'rows': []}
    try:
        for radius in arguments.radii:
            for nominal in arguments.nominal:
                profile = Profile(radius, nominal)
                for cells in arguments.cells:
                    row = evaluate(profile, cells, arguments.order, output, arguments.direct)
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
