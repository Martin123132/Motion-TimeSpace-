from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import psutil
from scipy.integrate import solve_bvp, solve_ivp
from scipy.special import hyp2f1
import sympy as sp


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'radial-pulsations-20261003'))
from solve_pulsations import Profile
from test_radial_energy import potential, potential_prime


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def exterior_basis(position, geometric_mass):
    ratio = 2*geometric_mass/position
    assert np.all(ratio < 1)
    growing = position**2*(1-ratio)
    growing_prime = 2*position-2*geometric_mass
    special = hyp2f1(3, 5, 6, ratio)
    special_prime = 2.5*hyp2f1(4, 6, 7, ratio)
    decaying = (1-ratio)*special/position**3
    decaying_prime = ((-3+4*ratio)*special-ratio*(1-ratio)*special_prime)/position**4
    return growing, growing_prime, decaying, decaying_prime


def exterior_coefficients(position, geometric_mass, value, derivative):
    growing, growing_prime, decaying, decaying_prime = exterior_basis(position, geometric_mass)
    wronskian = -5/growing
    return ((value*decaying_prime-derivative*decaying)/wronskian,
            (growing*derivative-growing_prime*value)/wronskian)


class TidalProblem:
    def __init__(self, profile, distance, tolerance):
        self.profile, self.distance, self.tolerance = profile, distance, tolerance
        self.radius = profile.radius
        self.mass = profile.alpha*profile.mass
        self.compactness = 2*self.mass/self.radius
        self.lower, self.upper = 1e-6, 1-distance/self.radius
        report = json.loads((ROOT/'results/edge-weak-v2/status.json').read_text(encoding='utf-8'))
        symbols = sp.symbols(' '.join(report['edge_symbols']), real=True)
        expressions = [sp.sympify(value, locals=dict(zip(report['edge_symbols'], symbols))) for value in report['edge_coefficients_orders_3_to_5']]
        self.coefficients = sp.lambdify(symbols, expressions, 'numpy')
        background = [sp.sympify(value, locals=dict(zip(report['edge_symbols'], symbols))) for value in report['background_coefficients_orders_2_to_4']]
        background_function = sp.lambdify(symbols[:3], background, 'numpy')
        self.background_coefficients = background_function(self.radius, self.compactness, profile.frequency**2)

    def radial_coefficients(self, position):
        profile = self.profile
        field, gradient, mass, metric, xi, canonical = profile.values(position)
        lapse_squared = xi**2*metric
        rotation = profile.frequency**2/lapse_squared
        density = (metric*gradient**2+rotation*field**2)/2+potential(field)
        pressure = density-2*potential(field)
        lapse_prime = profile.alpha*(mass+position**3*pressure)/(position**2*metric)
        first = (1+metric-2*profile.alpha*position**2*potential(field))/(position*metric)
        drive = potential_prime(field)-2*rotation*field-2*metric*lapse_prime*gradient
        metric_coefficient = (-4*profile.alpha*position**2*potential(field)-6
                              -(1-metric+2*profile.alpha*position**2*pressure)**2/metric
                              +8*profile.alpha*position**2*rotation*field**2)/(position**2*metric)
        field_coefficient = (6/position**2+field**(-2/3)/6+1.5*field**2-rotation+4*profile.alpha*metric*gradient**2)/metric
        return first, metric_coefficient, field_coefficient, drive/metric

    def equation(self, coordinate, state, parameters):
        first, metric_coefficient, field_coefficient, drive = self.radial_coefficients(self.radius*coordinate)
        return np.vstack([state[1],
                          -self.radius*first*state[1]-self.radius**2*metric_coefficient*state[0]+4*self.profile.alpha*self.radius**4*drive*state[2],
                          state[3], -self.radius*first*state[3]+self.radius**2*field_coefficient*state[2]+drive*state[0]])

    def surface_metric(self, right):
        scale = self.radius**2
        growing, decaying = exterior_coefficients(self.radius-self.distance, self.mass, scale*right[0], self.radius*right[1])
        basis = exterior_basis(self.radius, self.mass)
        return growing, decaying, growing*basis[0]+decaying*basis[2], growing*basis[1]+decaying*basis[3]

    def edge(self, distance, amplitude, surface_tide, surface_prime):
        coefficients = [amplitude, *self.coefficients(self.radius, self.compactness, self.profile.frequency**2, amplitude, surface_tide, surface_prime, *self.background_coefficients)]
        value = sum(coefficient*distance**order for order, coefficient in enumerate(coefficients, 2))
        derivative = sum(order*coefficient*distance**(order-1) for order, coefficient in enumerate(coefficients, 2))
        return value, derivative

    def boundary(self, left, right, parameters):
        growing, decaying, surface_tide, surface_prime = self.surface_metric(right)
        value, derivative = self.edge(self.distance, parameters[0]*self.radius**4, surface_tide, surface_prime)
        return np.array([left[1]-2*left[0]/self.lower, left[3]-2*left[2]/self.lower,
                         (right[2]-value/self.radius**4)/self.distance**2,
                         (right[3]+derivative/self.radius**3)/(self.radius*self.distance), growing+2])

    def solve(self):
        mesh = np.unique(np.r_[np.linspace(self.lower, self.upper, 350), np.linspace(max(self.lower, 1-12/self.radius), self.upper, 450)])
        guess = np.vstack([-2*mesh**2, -4*mesh, -.04*mesh**2*(1-mesh)**2, -.08*mesh*(1-mesh)*(1-2*mesh)])
        return solve_bvp(self.equation, self.boundary, mesh, guess, p=[-.04], tol=self.tolerance, bc_tol=self.tolerance/10, max_nodes=16000)


def exterior_control(problem, value, derivative):
    def equation(position, state):
        metric = 1-2*problem.mass/position
        first = (1+metric)/(position*metric)
        second = -6/(position**2*metric)-(1-metric)**2/(position**2*metric**2)
        return [state[1], -first*state[1]-second*state[0]]

    start = problem.radius-problem.distance
    solution = solve_ivp(equation, (start, 3*problem.radius), [value, derivative], method='DOP853', rtol=2e-12, atol=2e-12,
                         t_eval=np.array([1, 1.5, 2, 3])*problem.radius)
    assert solution.success
    rows = []
    original = exterior_coefficients(start, problem.mass, value, derivative)
    for position, state in zip(solution.t, solution.y.T):
        coefficients = exterior_coefficients(position, problem.mass, state[0], state[1])
        rows.append({'radius_over_support': position/problem.radius, 'growing_coefficient': coefficients[0],
                     'decaying_coefficient': coefficients[1],
                     'growing_relative_change': abs(coefficients[0]/original[0]-1),
                     'decaying_change_over_maximum_of_absolute_coefficient_and_radius_fifth': abs(coefficients[1]-original[1])/max(abs(original[1]), problem.radius**5)})
    return rows


def evaluate(base_radius, nominal, args, output):
    profile = Profile(base_radius, nominal)
    problem = TidalProblem(profile, args.distance, args.tolerance)
    solution = problem.solve()
    archive_name = f'R{base_radius:g}-C{nominal:g}.npz'
    np.savez_compressed(output/archive_name, spline_coefficients=solution.sol.c, spline_knots=solution.sol.x,
                        parameters=solution.p, radius=profile.radius, mesh=solution.x, values=solution.y,
                        rms_residuals=solution.rms_residuals, cutoff_distance=args.distance, alpha=profile.alpha)
    assert solution.success, solution.message
    growing, decaying, surface_tide, surface_prime = problem.surface_metric(solution.y[:, -1])
    geometric_lambda = decaying/(3*growing)
    dimensionless = geometric_lambda/problem.mass**5 if problem.mass > 0 else None
    return {'base_radius': base_radius, 'nominal_flat_compactness': nominal, 'alpha': profile.alpha,
            'radius': profile.radius, 'geometric_mass': problem.mass, 'surface_compactness': problem.compactness,
            'profile_path': str(profile.path), 'profile_sha256': digest(profile.path), 'archive': archive_name,
            'nodes': len(solution.x), 'converged': bool(solution.success), 'iterations': solution.niter,
            'maximum_rms_residual': float(max(solution.rms_residuals)),
            'maximum_boundary_residual': float(max(abs(problem.boundary(solution.y[:, 0], solution.y[:, -1], solution.p)))),
            'growing_coefficient': float(growing), 'decaying_coefficient': float(decaying),
            'geometric_tidal_lambda': float(geometric_lambda), 'dimensionless_Lambda': dimensionless,
            'k2': float(1.5*geometric_lambda/profile.radius**5),
            'lambda_over_alpha': float(geometric_lambda/profile.alpha) if profile.alpha > 0 else None,
            'edge_amplitude': float(solution.p[0]*profile.radius**4), 'surface_metric_H': surface_tide,
            'surface_displacement_per_unit_tide': float(solution.p[0]*profile.radius**4/(3*(12*(1-problem.compactness))**(-1.5))),
            'exterior_controls': exterior_control(problem, profile.radius**2*solution.y[0, -1], profile.radius*solution.y[1, -1])}


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--radii', nargs='+', type=float, default=[20.])
    parser.add_argument('--nominals', nargs='+', type=float, default=[0., .00001, .0001, .001, .003, .01, .03])
    parser.add_argument('--distance', type=float, default=.01)
    parser.add_argument('--tolerance', type=float, default=2e-8)
    args = parser.parse_args()
    output = ROOT/'results'/args.label
    output.mkdir(exist_ok=False)
    report = {'state': 'running', 'script_sha256': digest(__file__), 'arguments': vars(args),
              'derivation_sha256': digest(ROOT/'results/derivation/status.json'),
              'edge_weak_sha256': digest(ROOT/'results/edge-weak-v2/status.json'),
              'parent_seal_sha256': digest(BRANCH/'quadrupole-response-20261004/results/stage-integrity.json'), 'rows': []}
    try:
        for radius in args.radii:
            for nominal in args.nominals:
                row = evaluate(radius, nominal, args, output)
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
