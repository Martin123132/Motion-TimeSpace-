from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import psutil
from scipy.integrate import solve_bvp


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'radial-pulsations-20261003'))
from solve_pulsations import Profile
from test_radial_energy import potential_prime


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def edge_values(distance, radius, frequency, amplitude):
    cubic = 4*amplitude/(5*radius)-np.sqrt(3)*radius**2/24
    quartic = -5*amplitude*frequency**2/54+62*amplitude/(45*radius**2)+np.sqrt(3)*radius/120
    quintic = -5*amplitude*frequency**2/(63*radius)+2188*amplitude/(1125*radius**3)+7*np.sqrt(3)*frequency**2*radius**2/1296-11*np.sqrt(3)/360
    value = amplitude*distance**2+cubic*distance**3+quartic*distance**4+quintic*distance**5
    derivative = 2*amplitude*distance+3*cubic*distance**2+4*quartic*distance**3+5*quintic*distance**4
    return value, derivative


def integration_mesh(radius, cells=2048, order=8):
    points, weights = np.polynomial.legendre.leggauss(order)
    edges = np.linspace(0, radius, cells+1)
    widths = np.diff(edges)
    centers = (edges[:-1]+edges[1:])/2
    return (centers[:, None]+widths[:, None]*points/2).ravel(), (widths[:, None]*weights/2).ravel()


def evaluate(profile, distance, tolerance, output):
    radius, frequency = profile.radius, profile.frequency
    scale = radius**4
    lower, upper = 1e-6, 1-distance/radius

    def equation(coordinate, state, parameters):
        position = radius*coordinate
        field = profile.values(position)[0]
        coefficient = 6/position**2+field**(-2/3)/6+1.5*field**2-frequency**2
        source = 2*position**2*(potential_prime(field)-2*frequency**2*field)
        return np.vstack([state[1], radius**2*(coefficient*state[0]-source/scale)-2*state[1]/coordinate])

    def boundary(left, right, parameters):
        value, derivative = edge_values(distance, radius, frequency, parameters[0]*scale)
        return np.array([left[1]-2*left[0]/lower,
                         (right[0]-value/scale)/distance**2,
                         (right[1]+radius*derivative/scale)/(radius*distance)])

    mesh = np.unique(np.r_[np.linspace(lower, upper, 300), np.linspace(max(lower, 1-12/radius), upper, 400)])
    guess = -.1*np.vstack([mesh**2*(1-mesh)**2, 2*mesh*(1-mesh)*(1-2*mesh)])
    solution = solve_bvp(equation, boundary, mesh, guess, p=[-.1], tol=tolerance, bc_tol=tolerance/10, max_nodes=30000)
    amplitude = float(solution.p[0]*scale)
    archive_name = f'R{radius:g}-d{distance:g}-t{tolerance:g}.npz'
    np.savez_compressed(output/archive_name, spline_coefficients=solution.sol.c, spline_knots=solution.sol.x,
                        parameters=solution.p, scale=scale, radius=radius, cutoff_distance=distance,
                        mesh=solution.x, values=solution.y, rms_residuals=solution.rms_residuals)
    assert solution.success, solution.message
    position, weights = integration_mesh(radius)
    coordinate = position/radius
    response = solution.sol(np.clip(coordinate, lower, upper))[0]*scale
    central = coordinate < lower
    response[central] = solution.y[0, 0]*scale*(coordinate[central]/lower)**2
    tail = coordinate > upper
    response[tail] = edge_values(radius-position[tail], radius, frequency, amplitude)[0]
    field = profile.values(position)[0]
    source = 2*position**2*(potential_prime(field)-2*frequency**2*field)
    susceptibility = float(np.dot(weights, position**2*source*response))
    return {'radius': radius, 'cutoff_distance': distance, 'tolerance': tolerance,
            'profile_path': str(profile.path), 'profile_sha256': digest(profile.path), 'archive': archive_name,
            'susceptibility': susceptibility, 'edge_amplitude': amplitude,
            'surface_displacement_per_unit_tide': amplitude/(3*12**(-1.5)),
            'nodes': len(solution.x), 'maximum_rms_residual': float(max(solution.rms_residuals)),
            'maximum_boundary_residual': float(max(abs(boundary(solution.y[:, 0], solution.y[:, -1], solution.p)))),
            'converged': bool(solution.success), 'iterations': solution.niter}


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', required=True)
    parser.add_argument('--radii', nargs='+', type=float, default=[8., 20., 80.])
    parser.add_argument('--distances', nargs='+', type=float, default=[.01, .005, .0025])
    parser.add_argument('--tolerance', type=float, default=2e-9)
    args = parser.parse_args()
    output = ROOT/'results'/args.label
    output.mkdir(exist_ok=False)
    report = {'state': 'running', 'script_sha256': digest(__file__), 'arguments': vars(args),
              'edge_derivation_sha256': digest(ROOT/'results/derivation/status.json'), 'rows': []}
    try:
        for radius in args.radii:
            profile = Profile(radius, 0.)
            for distance in args.distances:
                row = evaluate(profile, distance, args.tolerance, output)
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
