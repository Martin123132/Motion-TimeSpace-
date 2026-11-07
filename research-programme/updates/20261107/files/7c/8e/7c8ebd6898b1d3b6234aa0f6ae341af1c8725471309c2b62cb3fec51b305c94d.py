from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import psutil
from scipy.interpolate import PPoly


ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent/'radial-pulsations-20261003'))
from solve_pulsations import Profile
from solve_static_bvp import edge_values, integration_mesh


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def potential(field):
    return 3*np.abs(field)**(4/3)/8+field**4/8


def evaluate(row, cells):
    profile = Profile(round(row['radius']), 0.)
    archive = ROOT/'results/static-bvp'/row['archive']
    with np.load(archive) as stored:
        spline = PPoly.construct_fast(stored['spline_coefficients'], stored['spline_knots'], axis=1)
        scale = float(stored['scale'])
    position, radial_weights = integration_mesh(profile.radius, cells=cells)
    coordinate = position/profile.radius
    lower, upper = spline.x[0], spline.x[-1]
    sampled = spline(np.clip(coordinate, lower, upper))
    response, response_prime = scale*sampled[0], scale/profile.radius*sampled[1]
    center = coordinate < lower
    response[center] = scale*spline(lower)[0]*(coordinate[center]/lower)**2
    response_prime[center] = 2*response[center]/position[center]
    tail = coordinate > upper
    response[tail], distance_prime = edge_values(profile.radius-position[tail], profile.radius, profile.frequency, row['edge_amplitude'])
    response_prime[tail] = -distance_prime
    field, gradient = profile.values(position)[:2]
    angles, angular_weights = np.polynomial.legendre.leggauss(32)
    angular_weights *= 2*np.pi
    harmonic = np.sqrt(5/(16*np.pi))*(3*angles**2-1)
    assert abs(angular_weights@harmonic) < 1e-14
    assert abs(angular_weights@harmonic**2-1) < 1e-14
    moment3 = float(angular_weights@harmonic**3)
    norm0 = float(4*np.pi*np.dot(radial_weights, position**2*field**2))
    charge = profile.frequency*norm0
    norm2 = float(np.dot(radial_weights, position**2*(response**2-8*position**2*field*response)))
    norm3 = float(-4*moment3*np.dot(radial_weights, position**4*response**2))
    gradient2 = float(np.dot(radial_weights, position**2*response_prime**2+6*response**2))
    tests = []
    for displacement in [.1, .05, .025, .0125]:
        epsilon = displacement/abs(row['surface_displacement_per_unit_tide'])
        delta = epsilon*response[:, None]*harmonic[None, :]
        plus = potential(field[:, None]+delta)
        minus = potential(field[:, None]-delta)
        mean_difference = (plus+minus)/2-potential(field[:, None])
        mean_difference -= epsilon*position[:, None]**2*harmonic[None, :]*(plus-minus)
        potential_difference = float(np.dot(radial_weights*position**2, mean_difference@angular_weights))
        norm_deltas = [epsilon**2*norm2+sign*epsilon**3*norm3 for sign in [-1, 1]]
        assert all(norm0+change > 0 for change in norm_deltas)
        rotation_difference = float(np.mean([-.5*charge**2*change/(norm0*(norm0+change)) for change in norm_deltas]))
        energy_difference = rotation_difference+.5*epsilon**2*gradient2+potential_difference
        prediction = -.5*epsilon**2*row['susceptibility']
        tests.append({'edge_displacement_parameter': displacement, 'epsilon': epsilon,
                      'maximum_imposed_potential': epsilon*profile.radius**2*float(max(abs(harmonic))),
                      'symmetric_energy_difference': energy_difference, 'quadratic_prediction': prediction,
                      'relative_difference': abs(energy_difference/prediction-1),
                      'charge_relative_error': max(abs((charge/(norm0+change))*(norm0+change)/charge-1) for change in norm_deltas)})
    return {'radius': profile.radius, 'radial_cells': cells, 'angular_order': 32,
            'archive_path': str(archive), 'archive_sha256': digest(archive),
            'profile_path': str(profile.path), 'profile_sha256': digest(profile.path),
            'background_charge_relative_error': abs(charge/profile.row['charge']-1), 'tests': tests}


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/finite-energy'
    output.mkdir(exist_ok=False)
    source = ROOT/'results/static-bvp/status.json'
    report = json.loads(source.read_text(encoding='utf-8'))
    rows = []
    for row in report['rows']:
        if row['cutoff_distance'] == .005:
            for cells in [1024, 2048]:
                result = evaluate(row, cells)
                rows.append(result)
                print(json.dumps(result), flush=True)
    result = {'state': 'complete', 'script_sha256': digest(__file__), 'source_path': str(source),
              'source_sha256': digest(source), 'helper_sha256': digest(ROOT/'solve_static_bvp.py'), 'rows': rows,
              'scope': 'Finite fixed-Q test of the linearly prescribed weak-metric functional; not a second-order Einstein metric or full Love number.',
              'moving_edge_extension': 'First-order displacement is tested on fixed support; omitted displaced layer contributes beyond quadratic order.'}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
