from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def surface_momenta(mass, coupling, speed, radius, order):
    cosine, weights = np.polynomial.legendre.leggauss(order)
    azimuth = 2*np.pi*(np.arange(16)+.5)/16
    normal = np.stack([np.broadcast_to(cosine[:, None], (order, 16)),
                       np.sqrt(1-cosine[:, None]**2)*np.cos(azimuth)[None, :],
                       np.sqrt(1-cosine[:, None]**2)*np.sin(azimuth)[None, :]], axis=-1).reshape(-1, 3)
    solid_weights = np.repeat(weights*2*np.pi/16, 16)
    gamma = 1/np.sqrt(1-speed**2)
    boost = np.eye(4)
    boost[0, 0] = boost[1, 1] = gamma
    boost[0, 1] = boost[1, 0] = -gamma*speed
    positions = radius*normal
    rest_positions = positions@boost[1:, 1:].T
    rest_radius = np.linalg.norm(rest_positions, axis=1)
    radial_gradient = (rest_positions/rest_radius[:, None])@boost[1:, :]
    compact = coupling*mass/(2*rest_radius)
    lapse_rest = (1-compact)/(1+compact)
    spatial_factor = (1+compact)**4
    metric_diagonal = np.column_stack([-lapse_rest**2, spatial_factor, spatial_factor, spatial_factor])
    spatial_prime = -4*compact*(1+compact)**3/rest_radius
    lapse_metric_prime = -4*lapse_rest*compact/(rest_radius*(1+compact)**2)
    radial_diagonal = np.column_stack([lapse_metric_prime, spatial_prime, spatial_prime, spatial_prime])
    metric = np.einsum('ai,na,aj->nij', boost, metric_diagonal, boost)
    radial_metric = np.einsum('ai,na,aj->nij', boost, radial_diagonal, boost)
    derivative = radial_gradient[:, :, None, None]*radial_metric[:, None, :, :]
    spatial_metric = metric[:, 1:, 1:]
    spatial_inverse = np.linalg.inv(spatial_metric)
    lapse = 1/np.sqrt(-np.linalg.inv(metric)[:, 0, 0])
    shift_covector = metric[:, 0, 1:]
    connection = np.zeros((len(normal), 3, 3, 3))
    for upper in range(3):
        for first in range(3):
            for second in range(3):
                for contracted in range(3):
                    connection[:, upper, first, second] += .5*spatial_inverse[:, upper, contracted]*(
                        derivative[:, first+1, contracted+1, second+1]
                        +derivative[:, second+1, contracted+1, first+1]
                        -derivative[:, contracted+1, first+1, second+1])
    shift_derivative = derivative[:, 1:, 0, 1:]
    extrinsic = (shift_derivative+shift_derivative.transpose(0, 2, 1)
                 -2*np.einsum('nkij,nk->nij', connection, shift_covector)
                 -derivative[:, 0, 1:, 1:])/(2*lapse[:, None, None])
    trace_extrinsic = np.einsum('nij,nij->n', spatial_inverse, extrinsic)
    energy_vector = np.zeros_like(normal)
    for first in range(3):
        for second in range(3):
            energy_vector[:, first] += derivative[:, second+1, first+1, second+1]-derivative[:, first+1, second+1, second+1]
    energy = radius**2*np.sum(solid_weights*np.einsum('ni,ni->n', energy_vector, normal))/(16*np.pi*coupling)
    momentum_tensor = extrinsic-trace_extrinsic[:, None, None]*spatial_metric
    momentum = radius**2*np.einsum('n,nij,nj->i', solid_weights, momentum_tensor, normal)/(8*np.pi*coupling)
    return float(energy), momentum


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/adm-boost'
    output.mkdir(parents=True, exist_ok=False)
    source = BRANCH/'self-gravity-20261003/results/fine/status.json'
    row = next(row for row in json.loads(source.read_text(encoding='utf-8'))['rows']
               if row['base_radius'] == 20 and row['nominal_flat_compactness'] == .03)
    mass, coupling = row['adm_energy'], row['alpha']/(4*np.pi)
    report = {'state': 'running', 'script_sha256': digest(__file__), 'source_path': str(source),
              'source_sha256': digest(source), 'body_adm_energy': mass, 'alpha': row['alpha'],
              'matter_proper_energy': row['proper_matter_energy_without_tiny_tail'],
              'proper_matter_energy_is_not_used_as_inertial_mass': True,
              'scope': 'ADM surface integrals of the exactly boosted Schwarzschild exterior; finite-radius coordinate-sphere estimators are extrapolated, not called exact quasilocal masses.',
              'rows': [], 'extrapolations': []}
    try:
        for speed in [0., .2, .5, .8]:
            gamma = 1/np.sqrt(1-speed**2)
            samples = []
            for factor in [10., 30., 100., 300., 1000., 3000.]:
                energy, momentum = surface_momenta(mass, coupling, speed, factor*row['radius'], 32)
                item = {'speed': speed, 'radius_over_body_radius': factor, 'energy': energy, 'momentum': momentum.tolist(),
                        'relative_energy_error': abs(energy/(gamma*mass)-1),
                        'momentum_error_over_gamma_mass': float(np.linalg.norm(momentum-np.array([gamma*mass*speed, 0, 0]))/(gamma*mass))}
                report['rows'].append(item)
                samples.append(item)
            inverse_radius = np.array([1/item['radius_over_body_radius'] for item in samples[-3:]])
            energy_limit = np.polynomial.polynomial.polyfit(inverse_radius, [item['energy'] for item in samples[-3:]], 2)[0]
            momentum_limit = np.polynomial.polynomial.polyfit(inverse_radius, [item['momentum'][0] for item in samples[-3:]], 2)[0]
            refined_energy, refined_momentum = surface_momenta(mass, coupling, speed, 3000*row['radius'], 64)
            result = {'speed': speed, 'extrapolated_energy': float(energy_limit), 'extrapolated_axial_momentum': float(momentum_limit),
                      'relative_energy_lorentz_error': float(abs(energy_limit/(gamma*mass)-1)),
                      'momentum_error_over_gamma_mass': float(abs(momentum_limit-gamma*mass*speed)/(gamma*mass)),
                      'relative_mass_shell_error': float(abs((energy_limit**2-momentum_limit**2)/mass**2-1)),
                      'angular_refinement_energy_difference_over_mass': float(abs(refined_energy-samples[-1]['energy'])/mass),
                      'angular_refinement_momentum_difference_over_mass': float(np.linalg.norm(refined_momentum-samples[-1]['momentum'])/mass)}
            assert result['relative_energy_lorentz_error'] < 1e-8 and result['momentum_error_over_gamma_mass'] < 1e-8
            assert samples[-1]['relative_energy_error'] < samples[0]['relative_energy_error']
            report['extrapolations'].append(result)
            print(json.dumps(result), flush=True)
        report['state'] = 'complete'
    except Exception as error:
        report['state'] = 'failed'
        report['error'] = repr(error)
        raise
    finally:
        (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')


if __name__ == '__main__':
    main()
