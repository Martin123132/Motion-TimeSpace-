from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import time

import numpy as np
import psutil
from scipy.integrate import solve_bvp, cumulative_simpson, simpson
from scipy.interpolate import PPoly
from scipy.optimize import brentq
import sympy as sp


ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent / 'finite-charge-20261003'


def potential(amplitude):
    absolute = np.abs(amplitude)
    return .375*absolute**(4/3)+.125*amplitude**4


def potential_prime(amplitude):
    return .5*np.cbrt(amplitude)+.5*amplitude**3


class BodySolver:
    def __init__(self, base_radius, floor, tolerance, coefficient_function):
        self.base_radius = base_radius
        self.floor = floor
        self.tolerance = tolerance
        self.coefficients = coefficient_function
        report = json.loads((PARENT/'results/regular-center-bodies/status.json').read_text(encoding='utf-8'))
        self.flat = next(row for row in report['rows'] if row['support_radius'] == base_radius)
        self.mass_scale = self.flat['energy']/(4*np.pi)
        self.charge_scale = self.flat['charge']/(4*np.pi)
        self.alpha = 0.0
        archive = np.load(PARENT/f'results/regular-center-bodies/profile-R{base_radius:g}.npz')
        self.flat_spline = PPoly.construct_fast(archive['spline_coefficients'], archive['spline_knots'], axis=1)
        self.flat_cut = float(archive['cut_radius'])
        self.nodes, self.weights = np.polynomial.legendre.leggauss(10)

    def tail_values(self, distance, parameters):
        frequency2, relative_radius, relative_mass = parameters
        radius = self.base_radius*relative_radius
        mass = self.mass_scale*relative_mass
        compactness = 2*self.alpha*mass/radius
        surface_metric = 1-compactness
        coefficient = (12*surface_metric)**(-1.5)
        values = [1., *self.coefficients(radius, compactness, frequency2)]
        variable = sum(value*distance**order for order, value in enumerate(values, 1))
        derivative = sum(order*value*distance**(order-1) for order, value in enumerate(values, 1))
        return coefficient*variable**3, -3*coefficient*variable**2*derivative

    def endpoint(self, parameters):
        frequency2, relative_radius, relative_mass = parameters
        radius = self.base_radius*relative_radius
        mass = self.mass_scale*relative_mass
        surface_metric = 1-2*self.alpha*mass/radius
        leading_distance = self.floor**(1/3)*np.sqrt(12*surface_metric)
        distance = brentq(lambda value: self.tail_values(value, parameters)[0]-self.floor,
                          .5*leading_distance, 1.5*leading_distance, xtol=1e-14)
        cut = radius-distance
        tail_distance = .5*distance*(1+self.nodes)
        weights = .5*distance*self.weights
        position = radius-tail_distance
        amplitude, derivative = self.tail_values(tail_distance, parameters)
        metric = 1-2*self.alpha*mass/position
        rho = .5*metric*derivative**2+.5*frequency2*amplitude**2/metric+potential(amplitude)
        tail_mass = float(np.dot(weights, position**2*rho))
        tail_charge = float(np.dot(weights, np.sqrt(frequency2)*position**2*amplitude**2/metric))
        slope = self.tail_values(distance, parameters)[1]
        lapse_at_cut = .5*np.log(1-2*self.alpha*mass/cut)
        return cut, slope, tail_mass, tail_charge, lapse_at_cut, distance

    def quantities(self, coordinate, fields, parameters):
        cut = self.endpoint(parameters)[0]
        position = cut*coordinate
        amplitude, velocity, mass_fraction, log_lapse, charge_fraction = fields
        mass = self.mass_scale*mass_fraction
        metric = 1-2*self.alpha*mass/position
        rotation = .5*parameters[0]*amplitude**2*np.exp(-2*log_lapse)
        gradient = .5*metric*(velocity/cut)**2
        value = potential(amplitude)
        density = gradient+rotation+value
        pressure = gradient+rotation-value
        lapse_prime = self.alpha*(mass+position**3*pressure)/(position**2*metric)
        metric_prime = 2*self.alpha*(mass/position**2-position*density)
        force = potential_prime(amplitude)-parameters[0]*amplitude*np.exp(-2*log_lapse)
        return cut, position, metric, density, pressure, rotation, gradient, lapse_prime, metric_prime, force

    def equation(self, coordinate, fields, parameters):
        cut, position, metric, density, pressure, rotation, gradient, lapse_prime, metric_prime, force = self.quantities(coordinate, fields, parameters)
        amplitude, velocity, mass_fraction, log_lapse, charge_fraction = fields
        return np.array([velocity,
                         cut**2*force/metric-(2/coordinate+cut*lapse_prime+cut*metric_prime/(2*metric))*velocity,
                         cut*position**2*density/self.mass_scale,
                         cut*lapse_prime,
                         cut*np.sqrt(parameters[0])*position**2*amplitude**2*np.exp(-log_lapse)/(np.sqrt(metric)*self.charge_scale)])

    def jacobian(self, coordinate, fields, parameters):
        cut, position, metric, density, pressure, rotation, gradient, lapse_prime, metric_prime, force = self.quantities(coordinate, fields, parameters)
        amplitude, velocity, mass_fraction, log_lapse, charge_fraction = fields
        count = len(coordinate)
        metric_jacobian = np.zeros((5, count))
        metric_jacobian[2] = -2*self.alpha*self.mass_scale/position
        density_jacobian = np.zeros((5, count))
        density_jacobian[0] = parameters[0]*amplitude*np.exp(-2*log_lapse)+potential_prime(amplitude)
        density_jacobian[1] = metric*velocity/cut**2
        density_jacobian[2] = .5*metric_jacobian[2]*(velocity/cut)**2
        density_jacobian[3] = -2*rotation
        pressure_jacobian = density_jacobian.copy()
        pressure_jacobian[0] -= 2*potential_prime(amplitude)
        mass_jacobian = np.zeros((5, count))
        mass_jacobian[2] = self.mass_scale
        lapse_jacobian = self.alpha*(mass_jacobian+position**3*pressure_jacobian)/(position**2*metric)-lapse_prime*metric_jacobian/metric
        metric_prime_jacobian = 2*self.alpha*(mass_jacobian/position**2-position*density_jacobian)
        force_jacobian = np.zeros((5, count))
        force_jacobian[0] = np.maximum(abs(amplitude), 1e-30)**(-2/3)/6+1.5*amplitude**2-parameters[0]*np.exp(-2*log_lapse)
        force_jacobian[3] = 2*parameters[0]*amplitude*np.exp(-2*log_lapse)
        jacobian = np.zeros((5, 5, count))
        jacobian[0, 1] = 1
        jacobian[1] = cut**2*(force_jacobian/metric-force*metric_jacobian/metric**2)
        jacobian[1] -= cut*(lapse_jacobian+metric_prime_jacobian/(2*metric)-metric_prime*metric_jacobian/(2*metric**2))*velocity
        jacobian[1, 1] -= 2/coordinate+cut*lapse_prime+cut*metric_prime/(2*metric)
        jacobian[2] = cut*position**2*density_jacobian/self.mass_scale
        jacobian[3] = cut*lapse_jacobian
        charge_factor = cut*np.sqrt(parameters[0])*position**2*np.exp(-log_lapse)/(np.sqrt(metric)*self.charge_scale)
        jacobian[4, 0] = 2*charge_factor*amplitude
        jacobian[4, 2] = -.5*charge_factor*amplitude**2*metric_jacobian[2]/metric
        jacobian[4, 3] = -charge_factor*amplitude**2
        parameter_jacobian = np.zeros((5, 3, count))
        for index in range(3):
            increment = 1e-5*max(1, abs(parameters[index]))
            plus, minus = parameters.copy(), parameters.copy()
            plus[index] += increment
            minus[index] -= increment
            parameter_jacobian[:, index] = (self.equation(coordinate, fields, plus)-self.equation(coordinate, fields, minus))/(2*increment)
        return jacobian, parameter_jacobian

    def boundary(self, left, right, parameters):
        cut, slope, tail_mass, tail_charge, lapse_at_cut, distance = self.endpoint(parameters)
        central_position = cut*1e-6
        amplitude, velocity, mass_fraction, log_lapse, charge_fraction = left
        central_rotation = .5*parameters[0]*amplitude**2*np.exp(-2*log_lapse)
        density = central_rotation+potential(amplitude)
        central_force = potential_prime(amplitude)-parameters[0]*amplitude*np.exp(-2*log_lapse)
        central_mass = central_position**3*density/(3*self.mass_scale)
        central_charge = np.sqrt(parameters[0])*np.exp(-log_lapse)*amplitude**2*central_position**3/(3*self.charge_scale)
        return np.array([velocity-cut*central_position*central_force/3,
                         mass_fraction-central_mass, charge_fraction-central_charge,
                         right[0]-self.floor, right[1]-cut*slope,
                         right[2]+tail_mass/self.mass_scale-parameters[2],
                         right[3]-lapse_at_cut, right[4]+tail_charge/self.charge_scale-1])

    def solve(self, nominal_compactness, previous=None):
        self.alpha = nominal_compactness*self.base_radius/(2*self.mass_scale)
        mesh = np.linspace(1e-6, 1, max(300, int(30*self.base_radius)))
        if previous is None:
            parameters = np.array([self.flat['frequency']**2, 1., 1.])
            cut = self.endpoint(parameters)[0]
            position = cut*mesh
            old_coordinate = np.clip(position/self.flat_cut, 0, 1)
            amplitude, derivative = self.flat_spline(old_coordinate)
            derivative /= self.flat_cut
            density = .5*derivative**2+.5*parameters[0]*amplitude**2+potential(amplitude)
            extended_position = np.concatenate([[0.], position])
            extended_mass_source = np.concatenate([[0.], position**2*density])
            extended_charge_source = np.concatenate([[0.], np.sqrt(parameters[0])*position**2*amplitude**2])
            mass = cumulative_simpson(extended_mass_source, x=extended_position, initial=0)[1:]
            charge = cumulative_simpson(extended_charge_source, x=extended_position, initial=0)[1:]
            initial = np.array([amplitude, cut*derivative, mass/self.mass_scale, np.zeros_like(mesh), charge/self.charge_scale])
            initial[0, -1] = self.floor
        else:
            parameters = previous.p.copy()
            initial = previous.sol(mesh)
        solution = solve_bvp(self.equation, self.boundary, mesh, initial, p=parameters,
                             fun_jac=self.jacobian, tol=self.tolerance, bc_tol=1e-11, max_nodes=50000)
        return solution

    def observables(self, solution):
        cut, slope, tail_mass, tail_charge, lapse_at_cut, distance = self.endpoint(solution.p)
        radius = self.base_radius*solution.p[1]
        mass = self.mass_scale*solution.p[2]
        mids = .5*(solution.x[1:]+solution.x[:-1])
        halves = .5*np.diff(solution.x)
        coordinate = (mids[:, None]+halves[:, None]*self.nodes).ravel()
        weights = (cut*halves[:, None]*self.weights).ravel()
        fields = solution.sol(coordinate)
        cut, position, metric, density, pressure, rotation, gradient, lapse_prime, metric_prime, force = self.quantities(coordinate, fields, solution.p)
        amplitude, velocity, mass_fraction, log_lapse, charge_fraction = fields
        tangential_pressure = rotation-gradient-potential(amplitude)
        charge_density = np.sqrt(solution.p[0])*amplitude**2*np.exp(-log_lapse)/np.sqrt(metric)
        quadrature_mass = np.dot(weights, position**2*density)+tail_mass
        quadrature_charge = np.dot(weights, position**2*charge_density)+tail_charge
        proper_energy = 4*np.pi*np.dot(weights, position**2*density/np.sqrt(metric))
        komar = np.dot(weights, position**2*np.exp(log_lapse)/np.sqrt(metric)*(density+pressure+2*tangential_pressure))
        field_derivatives = solution.sol(coordinate, 1)/cut
        field_seconds = solution.sol(coordinate, 2)/cut**2
        scalar_residual = field_seconds[0]+(2/position+field_derivatives[3]+metric_prime/(2*metric))*field_derivatives[0]-force/metric
        scalar_scale = max(np.max(np.abs(force/metric)), 1e-12)
        angular = metric*(field_seconds[3]+field_derivatives[3]**2+field_derivatives[3]/position)
        angular += .5*metric_prime*(field_derivatives[3]+1/position)-2*self.alpha*tangential_pressure
        angular_scale = max(2*self.alpha*np.max(density), 1e-12)
        sample = np.linspace(1e-6, 1, 10001)
        sample_fields = solution.sol(sample)
        sample_quantities = self.quantities(sample, sample_fields, solution.p)
        density_only_lapse_slope = self.alpha*self.mass_scale*mass_fraction/(position**2*metric)
        interior_pressure_lapse_fraction = float(np.max(np.abs(lapse_prime-density_only_lapse_slope))/max(np.max(np.abs(lapse_prime)), 1e-30))
        return {'base_radius': self.base_radius, 'alpha': self.alpha, 'radius': float(radius),
                'frequency_at_infinity': float(np.sqrt(solution.p[0])), 'charge': float(4*np.pi*quadrature_charge),
                'target_charge': self.flat['charge'], 'adm_energy': float(4*np.pi*mass),
                'flat_energy': self.flat['energy'], 'fixed_charge_energy_shift': float(4*np.pi*mass-self.flat['energy']),
                'proper_matter_energy_without_tiny_tail': float(proper_energy),
                'surface_compactness': float(2*self.alpha*mass/radius), 'minimum_F': float(np.min(sample_quantities[2])),
                'central_lapse': float(np.exp(solution.sol(1e-6)[3])),
                'central_amplitude': float(solution.sol(1e-6)[0]),
                'central_local_frequency': float(np.sqrt(solution.p[0])*np.exp(-solution.sol(1e-6)[3])),
                'mass_quadrature_relative_error': float(abs(quadrature_mass-mass)/mass),
                'charge_relative_error': float(abs(4*np.pi*quadrature_charge-self.flat['charge'])/self.flat['charge']),
                'komar_adm_relative_error_without_tiny_tail': float(abs(komar-mass)/mass),
                'scalar_collocation_relative_residual': float(np.max(abs(scalar_residual))/scalar_scale),
                'angular_Einstein_relative_residual': float(np.max(abs(angular))/angular_scale),
                'interior_pressure_fraction_of_lapse_gradient': interior_pressure_lapse_fraction,
                'boundary_max_residual': float(np.max(abs(self.boundary(solution.y[:, 0], solution.y[:, -1], solution.p)))),
                'min_amplitude_interior': float(np.min(sample_fields[0])),
                'maximum_field_increase': float(np.max(sample_fields[1]/cut)),
                'nodes': len(solution.x), 'max_rms_residual': float(np.max(solution.rms_residuals)),
                'endpoint_distance': float(distance), 'tail_mass': tail_mass, 'tail_charge': tail_charge,
                'converged': bool(solution.success), 'message': solution.message}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--radii', nargs='+', type=float, default=[8., 20., 80.])
    parser.add_argument('--nominal', nargs='+', type=float, default=[0., 1e-5, 1e-4, .001, .003, .01, .03])
    parser.add_argument('--floor', type=float, default=1e-8)
    parser.add_argument('--tol', type=float, default=2e-7)
    args = parser.parse_args()
    assert args.label.replace('-', '').isalnum()
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results'/args.label
    output.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    derivation = json.loads((ROOT/'results/derivation/status.json').read_text(encoding='utf-8'))
    symbols = sp.symbols('radius compactness frequency2')
    expressions = [sp.sympify(value, locals=dict(zip(derivation['edge_symbols'], symbols)))
                   for value in derivation['edge_u_coefficients_orders_2_to_5']]
    coefficients = sp.lambdify(symbols, expressions, 'numpy')
    rows = []
    try:
        for radius in args.radii:
            body = BodySolver(radius, args.floor, args.tol, coefficients)
            previous = None
            for nominal in args.nominal:
                solution = body.solve(nominal, previous)
                archive_name = f'R{radius:g}-C{nominal:g}'.replace('.', 'p')
                np.savez_compressed(output/f'{archive_name}.npz', spline_coefficients=solution.sol.c,
                                    spline_knots=solution.sol.x, parameters=solution.p,
                                    alpha=body.alpha, base_radius=radius, mass_scale=body.mass_scale,
                                    charge_scale=body.charge_scale, floor=body.floor)
                if not solution.success:
                    raise RuntimeError(f'{radius}, {nominal}: {solution.message}; residual {np.max(solution.rms_residuals)}')
                row = body.observables(solution)
                row['nominal_flat_compactness'] = nominal
                row['archive'] = archive_name+'.npz'
                rows.append(row)
                print(json.dumps({key: row[key] for key in ['base_radius', 'nominal_flat_compactness', 'radius', 'frequency_at_infinity',
                                                           'fixed_charge_energy_shift', 'surface_compactness', 'charge_relative_error',
                                                           'komar_adm_relative_error_without_tiny_tail', 'angular_Einstein_relative_residual', 'nodes']}), flush=True)
                (output/'progress.json').write_text(json.dumps(rows, indent=2, allow_nan=False), encoding='utf-8')
                previous = solution
        assert all(row['minimum_F'] > .5 and row['min_amplitude_interior'] > 0 for row in rows)
        assert all(row['charge_relative_error'] < 1e-7 and row['mass_quadrature_relative_error'] < 1e-7 for row in rows)
        assert all(row['komar_adm_relative_error_without_tiny_tail'] < 2e-6 for row in rows)
        report = {'state': 'complete', 'arguments': vars(args), 'rows': rows,
                  'elapsed_seconds': time.monotonic()-started, 'completed_at': datetime.now(timezone.utc).isoformat(),
                  'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  'derivation_sha256': hashlib.sha256((ROOT/'results/derivation/status.json').read_bytes()).hexdigest(),
                  'parent_seal_sha256': hashlib.sha256((PARENT/'results/stage-integrity.json').read_bytes()).hexdigest(),
                  'scope': 'Stationary minimal Einstein-complex-scalar continuation at fixed global charge; not gravitational dynamical stability.'}
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
        print(json.dumps({'state': 'complete', 'profiles': len(rows), 'elapsed_seconds': report['elapsed_seconds']}))
    except Exception as error:
        (output/'status.json').write_text(json.dumps({'state': 'failed', 'reason': repr(error), 'arguments': vars(args),
                                                     'completed_profiles': len(rows), 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}, indent=2), encoding='utf-8')
        raise


if __name__ == '__main__':
    main()
