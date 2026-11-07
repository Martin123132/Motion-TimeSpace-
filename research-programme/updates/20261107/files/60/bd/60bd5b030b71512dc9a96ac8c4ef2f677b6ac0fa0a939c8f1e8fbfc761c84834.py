from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import psutil
from scipy.interpolate import PPoly

from dynamic_system import BRANCH, DynamicProblem, Profile, ROOT, potential, potential_prime


sys.path.insert(0, str(BRANCH/'gravitating-tides-20261004'))
from test_curvature_v2 import background_jets


def general_curvature(metric, first, second):
    inverse = np.linalg.inv(metric)
    inverse_prime = np.array([-inverse@value@inverse for value in first])
    gamma = np.zeros((4, 4, 4))
    gamma_prime = np.zeros((4, 4, 4, 4))
    for upper in range(4):
        for left in range(4):
            for right in range(4):
                for contracted in range(4):
                    bracket = first[left, contracted, right]+first[right, contracted, left]-first[contracted, left, right]
                    gamma[upper, left, right] += inverse[upper, contracted]*bracket/2
                    for direction in range(4):
                        bracket_prime = second[direction, left, contracted, right]+second[direction, right, contracted, left]-second[direction, contracted, left, right]
                        gamma_prime[direction, upper, left, right] += (inverse_prime[direction, upper, contracted]*bracket+inverse[upper, contracted]*bracket_prime)/2
    ricci = np.zeros((4, 4))
    for left in range(4):
        for right in range(4):
            for contracted in range(4):
                ricci[left, right] += gamma_prime[contracted, contracted, left, right]-gamma_prime[right, contracted, left, contracted]
                for other in range(4):
                    ricci[left, right] += gamma[contracted, left, right]*gamma[other, contracted, other]-gamma[other, left, contracted]*gamma[contracted, right, other]
    return ricci, gamma, inverse


def product_jet(radial, angular, temporal):
    values = [temporal[0], radial[0], angular[0], 1.]
    first_values = [temporal[1], radial[1], angular[1], 0.]
    second_values = [temporal[2], radial[2], angular[2], 0.]
    value = np.prod(values)
    first, second = np.zeros(4), np.zeros((4, 4))
    for left in range(4):
        first[left] = first_values[left]*np.prod([values[index] for index in range(4) if index != left])
        second[left, left] = second_values[left]*np.prod([values[index] for index in range(4) if index != left])
        for right in range(4):
            if left != right:
                second[left, right] = first_values[left]*first_values[right]*np.prod([values[index] for index in range(4) if index not in [left, right]])
    return value, first, second


def multiply_jets(first, second):
    return np.array([first[0]*second[0], first[1]*second[0]+first[0]*second[1], first[2]*second[0]+2*first[1]*second[1]+first[0]*second[2]])


def local_jets(problem, spline, position):
    profile = problem.profile
    coordinate = position/profile.radius
    values = spline(coordinate)*problem.scales
    first = spline(coordinate, 1)*problem.scales/profile.radius
    second = spline(coordinate, 2)*problem.scales/profile.radius**2
    step = .0002*profile.radius
    positions = position+step*np.array([-2., -1., 0., 1., 2.])
    states = spline(positions/profile.radius)*problem.scales[:, None]
    time_values = problem.physical_evolution(positions, states)[1]
    time_value = time_values[2]
    time_first = (time_values[0]-8*time_values[1]+8*time_values[3]-time_values[4])/(12*step)
    time_second = (-time_values[0]+16*time_values[1]-30*time_values[2]+16*time_values[3]-time_values[4])/(12*step**2)
    return np.array([time_value, time_first, time_second]), np.array([values[0], first[0], second[0]]), np.array([values[1], first[1], second[1]]), np.array([values[2], first[2], second[2]]), np.array([values[4], first[4], second[4]])


def residual(problem, spline, position, polar, time_phase, epsilon):
    profile = problem.profile
    field, gradient, field_second, metric, metric_prime, metric_second, lapse2, lapse_prime, lapse_second, rotation = background_jets(profile, position)
    tide, angular, shift, response, phase = local_jets(problem, spline, position)
    sigma = problem.sigma
    cosine = np.array([np.cos(time_phase), -sigma*np.sin(time_phase), -sigma**2*np.cos(time_phase)])
    sine = np.array([np.sin(time_phase), sigma*np.cos(time_phase), -sigma**2*np.sin(time_phase)])
    harmonic = np.sqrt(5/(16*np.pi))*np.array([3*np.cos(polar)**2-1, -6*np.cos(polar)*np.sin(polar), -6*np.cos(2*polar)])
    sphere = np.array([np.sin(polar)**2, np.sin(2*polar), 2*np.cos(2*polar)])
    unit = np.array([1., 0., 0.])
    radial_bases = [np.array([-lapse2, -2*lapse_prime*lapse2, -(2*lapse_second+4*lapse_prime**2)*lapse2]),
                    np.array([1/metric, -metric_prime/metric**2, 2*metric_prime**2/metric**3-metric_second/metric**2]),
                    np.array([position**2, 2*position, 2]), np.array([position**2, 2*position, 2])]
    values, first, second = np.zeros((4, 4)), np.zeros((4, 4, 4)), np.zeros((4, 4, 4, 4))
    for component, (base, factor) in enumerate(zip(radial_bases, [-tide, tide, angular, angular])):
        angular_base = sphere if component == 3 else unit
        background = product_jet(base, angular_base, unit)
        perturbation = product_jet(multiply_jets(base, factor), multiply_jets(angular_base, harmonic), cosine)
        values[component, component] = background[0]+epsilon*perturbation[0]
        first[:, component, component] = background[1]+epsilon*perturbation[1]
        second[:, :, component, component] = background[2]+epsilon*perturbation[2]
    offdiagonal = product_jet(-sigma*shift, harmonic, sine)
    values[0, 1] = values[1, 0] = epsilon*offdiagonal[0]
    first[:, 0, 1] = first[:, 1, 0] = epsilon*offdiagonal[1]
    second[:, :, 0, 1] = second[:, :, 1, 0] = epsilon*offdiagonal[2]
    scalar_perturbation = product_jet(response, harmonic, cosine)
    phase_perturbation = product_jet(sigma*phase, harmonic, sine)
    scalar = field+epsilon*scalar_perturbation[0]
    assert scalar > 0
    scalar_first = np.array([0., gradient, 0., 0.])+epsilon*scalar_perturbation[1]
    scalar_second = epsilon*scalar_perturbation[2]
    scalar_second[1, 1] += field_second
    phase_first = np.array([profile.frequency, 0., 0., 0.])+epsilon*phase_perturbation[1]
    phase_second = epsilon*phase_perturbation[2]
    curvature, gamma, inverse = general_curvature(values, first, second)
    source = 2*profile.alpha*(np.outer(scalar_first, scalar_first)+scalar**2*np.outer(phase_first, phase_first)+values*potential(scalar))
    scalar_box = np.sum(inverse*(scalar_second-np.einsum('abc,a->bc', gamma, scalar_first)))
    phase_box = np.sum(inverse*(phase_second-np.einsum('abc,a->bc', gamma, phase_first)))
    scalar_terms = np.array([scalar_box, -scalar*(phase_first@inverse@phase_first), -potential_prime(scalar)])
    phase_terms = np.array([scalar**2*phase_box, 2*scalar*(scalar_first@inverse@phase_first)])
    return curvature-source, curvature, source, scalar_terms, phase_terms


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/dynamic-curvature'
    output.mkdir(exist_ok=False)
    profile = Profile(20., .03)
    rows = []
    sources = []
    for sigma in [.01, .02]:
        source = ROOT/f'results/pilot/sigma{sigma:g}.npz'
        sources.append({'path': str(source), 'sha256': hashlib.sha256(source.read_bytes()).hexdigest()})
        archive = np.load(source)
        spline = PPoly.construct_fast(archive['spline_coefficients'], archive['spline_knots'], axis=1)
        problem = DynamicProblem(profile, sigma)
        for fraction in [.2, .5, .8, .9]:
            position = fraction*profile.radius
            tide, angular, shift, response, phase = local_jets(problem, spline, position)
            field = profile.values(np.array([position]))[0][0]
            scale = max(1., abs(tide[0]), abs(angular[0]), abs(response[0]/field), abs(sigma*phase[0]))
            for polar in [.7, 1.2]:
                for time_phase in [.4, 1.1]:
                    variations = []
                    for relative_step in [.002, .001, .0005]:
                        epsilon = relative_step/scale
                        plus = residual(problem, spline, position, polar, time_phase, epsilon)
                        minus = residual(problem, spline, position, polar, time_phase, -epsilon)
                        linear = [(positive-negative)/(2*epsilon) for positive, negative in zip(plus, minus)]
                        variations.append({'relative_step': relative_step,
                                           'einstein_residual': float(np.linalg.norm(linear[0])/(1+np.linalg.norm(linear[1])+np.linalg.norm(linear[2]))),
                                           'scalar_residual': float(abs(sum(linear[3]))/(1+sum(abs(linear[3])))),
                                           'current_residual': float(abs(sum(linear[4]))/(1+sum(abs(linear[4]))))})
                    rows.append({'sigma': sigma, 'radius_fraction': fraction, 'polar_angle': polar, 'time_phase': time_phase, 'variations': variations})
    result = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'input_sources': sources,
              'rows': rows, 'scope': 'Independent full non-diagonal nonlinear Ricci, scalar equation and phase current; centered finite perturbations; H jets by five-point differences, other perturbation jets directly from collocation spline.'}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'tests': len(rows)*3, **{key: max(row['variations'][-1][key] for row in rows) for key in ['einstein_residual', 'scalar_residual', 'current_residual']}}))


if __name__ == '__main__':
    main()
