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
from scipy.interpolate import PPoly
import sympy as sp


ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent/'self-gravity-20261003'
sys.path.insert(0, str(PARENT))
from solve_self_gravity import BodySolver, potential, potential_prime


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Profile:
    def __init__(self, base_radius, nominal):
        report = json.loads((PARENT/'results/fine/status.json').read_text(encoding='utf-8'))
        self.row = next(row for row in report['rows'] if row['base_radius'] == base_radius and row['nominal_flat_compactness'] == nominal)
        self.path = PARENT/'results/fine'/self.row['archive']
        archive = np.load(self.path)
        self.spline = PPoly.construct_fast(archive['spline_coefficients'], archive['spline_knots'], axis=1)
        edge = json.loads((PARENT/'results/derivation/status.json').read_text(encoding='utf-8'))
        symbols = sp.symbols(' '.join(edge['edge_symbols']))
        expressions = [sp.sympify(value, locals=dict(zip(edge['edge_symbols'], symbols))) for value in edge['edge_u_coefficients_orders_2_to_5']]
        self.body = BodySolver(base_radius, float(archive['floor']), 2e-9, sp.lambdify(symbols, expressions, 'numpy'))
        self.alpha = self.body.alpha = float(archive['alpha'])
        self.parameters = archive['parameters']
        self.cut = self.body.endpoint(self.parameters)[0]
        self.radius = self.row['radius']
        self.frequency = self.row['frequency_at_infinity']
        self.mass = self.row['adm_energy']/(4*np.pi)

    def values(self, position):
        coordinate = np.clip(position/self.cut, 1e-6, 1.)
        amplitude, velocity, mass_fraction, log_lapse, charge_fraction = self.spline(coordinate)
        derivative = velocity/self.cut
        mass = self.body.mass_scale*mass_fraction
        metric = 1-2*self.alpha*mass/position
        lapse = np.exp(log_lapse)
        tail = position > self.cut
        if np.any(tail):
            amplitude[tail], derivative[tail] = self.body.tail_values(self.radius-position[tail], self.parameters)
            mass[tail] = self.mass
            metric[tail] = 1-2*self.alpha*self.mass/position[tail]
            lapse[tail] = np.sqrt(metric[tail])
        center = position/self.cut < 1e-6
        if np.any(center):
            central_amplitude = self.row['central_amplitude']
            central_lapse = self.row['central_lapse']
            force = potential_prime(central_amplitude)-self.frequency**2*central_amplitude/central_lapse**2
            amplitude[center] = central_amplitude+force*position[center]**2/6
            derivative[center] = force*position[center]/3
            central_density = .5*self.frequency**2*central_amplitude**2/central_lapse**2+potential(central_amplitude)
            mass[center] = central_density*position[center]**3/3
            metric[center] = 1-2*self.alpha*mass[center]/position[center]
            lapse[center] = central_lapse
        assert np.all(amplitude > 0) and np.all(metric > 0)
        xi = lapse/np.sqrt(metric)
        canonical_rotation = self.frequency*amplitude/(xi*metric)
        return amplitude, derivative, mass, metric, xi, canonical_rotation


class Quadrature:
    def __init__(self, radius, cells, order):
        nodes, weights = np.polynomial.legendre.leggauss(order)
        self.cells, self.order = cells, order
        self.width = radius/cells
        centers = self.width*(np.arange(cells)+.5)
        self.position = (centers[:, None]+self.width*nodes[None, :]/2).ravel()
        self.weights = np.tile(self.width*weights/2, cells)
        self.cell_weights = self.width*weights/2
        vandermonde = np.polynomial.legendre.legvander(nodes, order-1)
        antiderivatives = []
        for degree in range(order):
            coefficients = np.zeros(degree+1)
            coefficients[-1] = 1
            integral = np.polynomial.legendre.legint(coefficients)
            antiderivatives.append(np.polynomial.legendre.legval(nodes, integral)-np.polynomial.legendre.legval(-1., integral))
        self.partial_weights = self.width/2*np.array(antiderivatives).T@np.linalg.inv(vandermonde)
        basis = np.zeros((cells*order, cells+1))
        derivative = np.zeros_like(basis)
        for cell in range(cells):
            selection = slice(cell*order, (cell+1)*order)
            basis[selection, cell] = (1-nodes)/2
            basis[selection, cell+1] = (1+nodes)/2
            derivative[selection, cell] = -1/self.width
            derivative[selection, cell+1] = 1/self.width
        self.basis = basis[:, 1:-1]
        self.derivative = derivative[:, 1:-1]

    def integrate(self, values):
        return np.einsum('q,q...->...', self.weights, values)

    def cumulative(self, values):
        shaped = values.reshape((self.cells, self.order)+values.shape[1:])
        cell_integrals = np.einsum('q,cq...->c...', self.cell_weights, shaped)
        starts = np.concatenate([np.zeros_like(cell_integrals[:1]), np.cumsum(cell_integrals[:-1], axis=0)], axis=0)
        partial = np.einsum('pq,cq...->cp...', self.partial_weights, shaped)
        result = starts[:, None, ...]+partial
        return result.reshape(values.shape)

    def form(self, left, coefficient, right=None):
        if right is None:
            right = left
        return left.T@((self.weights*coefficient)[:, None]*right)


def reduced_matrix(amplitude, mixed, momentum, charge_amplitude, charge_momentum):
    factor = linalg.cho_factor(momentum, lower=True, check_finite=False)
    inverse_mixed = linalg.cho_solve(factor, mixed.T, check_finite=False)
    inverse_charge = linalg.cho_solve(factor, charge_momentum, check_finite=False)
    unconstrained = amplitude-mixed@inverse_mixed
    effective_charge = charge_amplitude-mixed@inverse_charge
    denominator = float(charge_momentum@inverse_charge)
    assert denominator > 0
    constrained = unconstrained+np.outer(effective_charge, effective_charge)/denominator
    return (constrained+constrained.T)/2, (unconstrained+unconstrained.T)/2, factor, inverse_charge, effective_charge, denominator


def evaluate(profile, cells, order, output):
    started = time.monotonic()
    quadrature = Quadrature(profile.radius, cells, order)
    position, weights = quadrature.position, quadrature.weights
    amplitude, derivative, mass, metric, xi, rotation = profile.values(position)
    basis, basis_derivative = quadrature.basis, quadrature.derivative
    value_basis = basis/position[:, None]
    gradient_basis = basis_derivative/position[:, None]-basis/position[:, None]**2
    inertia = quadrature.form(basis, np.ones_like(position))
    force = potential_prime(amplitude)
    second = amplitude**(-2/3)/6+1.5*amplitude**2
    kinetic = derivative**2+rotation**2
    log_factor = quadrature.cumulative(profile.alpha*position*kinetic)
    total_log_factor = quadrature.integrate(profile.alpha*position*kinetic)
    xi_from_constraint = np.exp(log_factor-total_log_factor)
    mass_from_constraint = quadrature.cumulative(np.exp(log_factor)*position**2*(kinetic/2+potential(amplitude)))*np.exp(-log_factor)
    kinetic_variation = np.concatenate([2*derivative[:, None]*gradient_basis, 2*rotation[:, None]*value_basis], axis=1)
    potential_variation = np.concatenate([force[:, None]*value_basis, np.zeros_like(value_basis)], axis=1)
    source = xi[:, None]*position[:, None]**2*(metric[:, None]*kinetic_variation/2+potential_variation)
    mass_variation = quadrature.cumulative(source)/xi[:, None]
    gravity_unsymmetrized = -profile.alpha*kinetic_variation.T@((weights*xi*position)[:, None]*mass_variation)
    gravity = gravity_unsymmetrized+gravity_unsymmetrized.T
    size = cells-1
    local_amplitude = quadrature.form(gradient_basis, xi*position**2*metric)+quadrature.form(basis, xi*second)
    local_momentum = quadrature.form(basis, xi*metric)
    local_mixed = -profile.frequency*inertia
    amplitude_block = local_amplitude+gravity[:size, :size]
    momentum_block = local_momentum+gravity[size:, size:]
    mixed_block = local_mixed+gravity[:size, size:]
    charge_amplitude = value_basis.T@(weights*position**2*rotation)
    charge_momentum = value_basis.T@(weights*position**2*amplitude)
    fixed, free, factor, inverse_charge, effective_charge, denominator = reduced_matrix(
        amplitude_block, mixed_block, momentum_block, charge_amplitude, charge_momentum)
    frozen, frozen_free, _, _, _, _ = reduced_matrix(local_amplitude, local_mixed, local_momentum, charge_amplitude, charge_momentum)
    eigenvalues, eigenvectors = linalg.eigh(fixed, inertia, subset_by_index=[0, 2], check_finite=False)
    free_values = linalg.eigh(free, inertia, subset_by_index=[0, 1], eigvals_only=True, check_finite=False)
    frozen_values = linalg.eigh(frozen, inertia, subset_by_index=[0, 0], eigvals_only=True, check_finite=False)
    momentum_minimum = linalg.eigh(momentum_block, inertia, subset_by_index=[0, 0], eigvals_only=True, check_finite=False)[0]
    ground_amplitude = eigenvectors[:, 0]
    ground_momentum = -linalg.cho_solve(factor, mixed_block.T@ground_amplitude, check_finite=False)
    ground_momentum -= inverse_charge*(effective_charge@ground_amplitude)/denominator
    charge_error = abs(charge_amplitude@ground_amplitude+charge_momentum@ground_momentum)/max(1., abs(charge_amplitude@ground_amplitude), abs(charge_momentum@ground_momentum))
    ground_full = np.concatenate([ground_amplitude, ground_momentum])
    direct_energy = (ground_amplitude@amplitude_block@ground_amplitude+2*ground_amplitude@mixed_block@ground_momentum+ground_momentum@momentum_block@ground_momentum)
    rayleigh_error = abs(direct_energy-eigenvalues[0])/max(abs(eigenvalues[0]), 1e-15)
    phase_operator = quadrature.form(gradient_basis, xi*position**2*metric)+quadrature.form(basis, xi*force/amplitude-profile.frequency**2/(xi*metric))
    phase_values = linalg.eigh(phase_operator, inertia, subset_by_index=[0, 1], eigvals_only=True, check_finite=False)
    flat_error = None
    if profile.alpha == 0:
        overlap = basis.T@(weights*position*amplitude)
        radial_inertia = quadrature.integrate(position**2*amplitude**2)
        explicit_flat = quadrature.form(basis_derivative, np.ones_like(position))+quadrature.form(basis, second-profile.frequency**2)
        explicit_flat += 4*profile.frequency**2*np.outer(overlap, overlap)/radial_inertia
        flat_error = float(linalg.norm(fixed-explicit_flat)/linalg.norm(explicit_flat))
    name = f'R{profile.row["base_radius"]:g}-C{profile.row["nominal_flat_compactness"]:g}-N{cells}-G{order}'.replace('.', 'p')
    np.savez_compressed(output/f'{name}.npz', radius=profile.radius, alpha=profile.alpha,
                        nodal_position=np.linspace(0, profile.radius, cells+1), lowest_eigenvalues=eigenvalues,
                        amplitude_mode=np.concatenate([[0.], ground_amplitude, [0.]]),
                        momentum_mode=np.concatenate([[0.], ground_momentum, [0.]]),
                        quadrature_position=position, metric_mass_variation=mass_variation@ground_full,
                        canonical_kinetic_variation=kinetic_variation@ground_full)
    return {'base_radius': profile.row['base_radius'], 'nominal_compactness': profile.row['nominal_flat_compactness'],
            'alpha': profile.alpha, 'radius': profile.radius, 'cells': cells, 'quadrature_order': order,
            'lowest_fixed_charge_energy_eigenvalues': eigenvalues.tolist(),
            'lowest_unconstrained_energy_eigenvalues': free_values.tolist(),
            'lowest_frozen_metric_fixed_charge_energy_eigenvalue': float(frozen_values[0]),
            'momentum_block_minimum': float(momentum_minimum), 'phase_lowest_eigenvalues': phase_values.tolist(),
            'charge_tangent_relative_error': float(charge_error), 'schur_rayleigh_relative_error': float(rayleigh_error),
            'flat_explicit_operator_relative_error': flat_error,
            'lapse_constraint_max_absolute_error': float(np.max(abs(xi_from_constraint-xi))),
            'mass_constraint_max_relative_error': float(np.max(abs(mass_from_constraint-mass))/profile.mass),
            'profile_path': str(profile.path), 'profile_sha256': digest(profile.path), 'archive': f'{name}.npz',
            'seconds': time.monotonic()-started}


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
    arguments = parser.parse_args()
    output = ROOT/'results'/arguments.label
    output.mkdir(parents=True, exist_ok=False)
    report = {'state': 'running', 'arguments': vars(arguments), 'started': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(Path(__file__)), 'parent_seal_sha256': digest(PARENT/'results/stage-integrity.json'),
              'derivation_sha256': digest(ROOT/'results/derivation/status.json'), 'rows': [],
              'one_worker_one_core': True, 'spectrum_kind': 'fixed-charge energy Hessian, not oscillation frequency'}
    status = output/'status.json'
    try:
        for radius in arguments.radii:
            for nominal in arguments.nominal:
                profile = Profile(radius, nominal)
                for cells in arguments.cells:
                    row = evaluate(profile, cells, arguments.order, output)
                    report['rows'].append(row)
                    status.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
                    print(json.dumps(row), flush=True)
        report['state'] = 'complete'
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        raise
    finally:
        status.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
