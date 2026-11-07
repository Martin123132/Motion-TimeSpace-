from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import psutil
import sympy as sp

from check_limits import spline_for
from solve_tides import Profile, TidalProblem, potential, potential_prime


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_compact_constraint():
    radius = sp.symbols('radius', real=True)
    alpha, frequency = sp.symbols('alpha frequency', positive=True)
    metric, lapse, field, amplitude, angular, response = [sp.Function(name)(radius) for name in ['metric', 'lapse', 'field', 'amplitude', 'angular', 'response']]
    potential_function = sp.Function('potential')(field)
    pressure = (metric*sp.diff(field, radius)**2+frequency**2*sp.exp(-2*lapse)*field**2)/2-potential_function
    lapse_prime = ((1-metric)/2+alpha*radius**2*pressure)/(radius*metric)
    compact = ((3-metric)/2+radius**2*metric*lapse_prime**2+alpha*radius**2*(metric*sp.diff(field, radius)**2-frequency**2*sp.exp(-2*lapse)*field**2)/2)*amplitude
    compact += radius**2*metric*lapse_prime*sp.diff(amplitude, radius)/2-alpha*radius**2*metric*sp.diff(field, radius)*sp.diff(response, radius)
    compact += (alpha*radius**2*(sp.diff(potential_function, field)-frequency**2*sp.exp(-2*lapse)*field)-2*alpha*radius*metric*(1+radius*lapse_prime)*sp.diff(field, radius))*response
    report = json.loads((ROOT/'results/derivation/status.json').read_text(encoding='utf-8'))
    original = sp.sympify(report['expressions']['angular_constraint'], locals={'radius': radius, 'alpha': alpha, 'frequency': frequency, **{name: sp.Function(name) for name in ['metric', 'lapse', 'field', 'amplitude', 'response', 'potential']}})
    assert sp.factor(original-compact) == 0
    return str(compact)


def background_jets(profile, position):
    field, gradient, mass, metric, xi, canonical = [float(value[0]) for value in profile.values(np.array([position]))]
    lapse_squared = xi**2*metric
    rotation = profile.frequency**2/lapse_squared
    density = (metric*gradient**2+rotation*field**2)/2+potential(field)
    pressure = density-2*potential(field)
    metric_prime = (1-metric)/position-2*profile.alpha*position*density
    lapse_prime = profile.alpha*(mass+position**3*pressure)/(position**2*metric)
    second = (potential_prime(field)-rotation*field)/metric-(2/position+lapse_prime+metric_prime/(2*metric))*gradient
    density_prime = metric_prime*gradient**2/2+metric*gradient*second+rotation*field*gradient-lapse_prime*rotation*field**2+potential_prime(field)*gradient
    pressure_prime = density_prime-2*potential_prime(field)*gradient
    metric_second = -metric_prime/position-(1-metric)/position**2-2*profile.alpha*(density+position*density_prime)
    lapse_second = profile.alpha*((position**2*density+3*position**2*pressure+position**3*pressure_prime)/(position**2*metric)
                                  -(mass+position**3*pressure)*(2*position*metric+position**2*metric_prime)/(position**2*metric)**2)
    return field, gradient, second, metric, metric_prime, metric_second, lapse_squared, lapse_prime, lapse_second, rotation


def perturbation_jets(profile, spline, position):
    background = background_jets(profile, position)
    field, gradient, second, metric, metric_prime, metric_second, lapse_squared, lapse_prime, lapse_second, rotation = background
    coordinate = position/profile.radius
    values, derivatives, seconds = spline(coordinate), spline(coordinate, 1), spline(coordinate, 2)
    amplitude, amplitude_prime, amplitude_second = profile.radius**2*values[0], profile.radius*derivatives[0], seconds[0]
    response, response_prime, response_second = profile.radius**4*values[2], profile.radius**3*derivatives[2], profile.radius**2*seconds[2]
    angular = ((3-metric)/2+position**2*metric*lapse_prime**2+profile.alpha*position**2*(metric*gradient**2-rotation*field**2)/2)*amplitude
    angular += position**2*metric*lapse_prime*amplitude_prime/2-profile.alpha*position**2*metric*gradient*response_prime
    angular += (profile.alpha*position**2*(potential_prime(field)-rotation*field)-2*profile.alpha*position*metric*(1+position*lapse_prime)*gradient)*response
    angular_prime = amplitude_prime+2*lapse_prime*amplitude-4*profile.alpha*gradient*response
    angular_second = amplitude_second+2*lapse_second*amplitude+2*lapse_prime*amplitude_prime-4*profile.alpha*(second*response+gradient*response_prime)
    return background, (amplitude, amplitude_prime, amplitude_second, angular, angular_prime, angular_second, response, response_prime, response_second)


def diagonal_ricci(values, first, second):
    gamma = np.zeros((4, 4, 4))
    gamma_prime = np.zeros((4, 4, 4, 4))
    for upper in range(4):
        for left in range(4):
            for right in range(4):
                bracket = (first[left, upper] if upper == right else 0)+(first[right, upper] if upper == left else 0)-(first[upper, left] if left == right else 0)
                gamma[upper, left, right] = bracket/(2*values[upper])
                for direction in range(4):
                    derivative = (second[direction, left, upper] if upper == right else 0)+(second[direction, right, upper] if upper == left else 0)-(second[direction, upper, left] if left == right else 0)
                    gamma_prime[direction, upper, left, right] = derivative/(2*values[upper])-first[direction, upper]*bracket/(2*values[upper]**2)
    ricci = np.zeros((4, 4))
    for left in range(4):
        for right in range(4):
            for contracted in range(4):
                ricci[left, right] += gamma_prime[contracted, contracted, left, right]-gamma_prime[right, contracted, left, contracted]
                for other in range(4):
                    ricci[left, right] += gamma[contracted, left, right]*gamma[other, contracted, other]-gamma[other, left, contracted]*gamma[contracted, right, other]
    return ricci


def finite_residual(profile, spline, position, polar, epsilon):
    background, perturbation = perturbation_jets(profile, spline, position)
    field, gradient, second, metric, metric_prime, metric_second, lapse_squared, lapse_prime, lapse_second, rotation = background
    amplitude, amplitude_prime, amplitude_second, angular, angular_prime, angular_second, response, response_prime, response_second = perturbation
    normalization = np.sqrt(5/(16*np.pi))
    harmonic = normalization*(3*np.cos(polar)**2-1)
    harmonic_prime = -6*normalization*np.cos(polar)*np.sin(polar)
    harmonic_second = -6*normalization*np.cos(2*polar)
    radial_bases = [(-lapse_squared, -2*lapse_prime*lapse_squared, -(2*lapse_second+4*lapse_prime**2)*lapse_squared),
                    (1/metric, -metric_prime/metric**2, 2*metric_prime**2/metric**3-metric_second/metric**2),
                    (position**2, 2*position, 2), (position**2, 2*position, 2)]
    factors = [(-amplitude, -amplitude_prime, -amplitude_second), (amplitude, amplitude_prime, amplitude_second),
               (angular, angular_prime, angular_second), (angular, angular_prime, angular_second)]
    values, first, seconds = np.zeros(4), np.zeros((4, 4)), np.zeros((4, 4, 4))
    for component, (base, factor) in enumerate(zip(radial_bases, factors)):
        angular_base, angular_first, angular_second_base = (np.sin(polar)**2, np.sin(2*polar), 2*np.cos(2*polar)) if component == 3 else (1, 0, 0)
        modulation = 1+epsilon*factor[0]*harmonic
        values[component] = base[0]*angular_base*modulation
        first[1, component] = angular_base*(base[1]*modulation+base[0]*epsilon*factor[1]*harmonic)
        first[2, component] = base[0]*(angular_first*modulation+angular_base*epsilon*factor[0]*harmonic_prime)
        seconds[1, 1, component] = angular_base*(base[2]*modulation+2*base[1]*epsilon*factor[1]*harmonic+base[0]*epsilon*factor[2]*harmonic)
        seconds[1, 2, component] = base[1]*(angular_first*modulation+angular_base*epsilon*factor[0]*harmonic_prime)+base[0]*epsilon*factor[1]*(angular_first*harmonic+angular_base*harmonic_prime)
        seconds[2, 1, component] = seconds[1, 2, component]
        seconds[2, 2, component] = base[0]*(angular_second_base*modulation+2*angular_first*epsilon*factor[0]*harmonic_prime+angular_base*epsilon*factor[0]*harmonic_second)
    field_total = field+epsilon*response*harmonic
    assert field_total > 0
    field_gradient = np.array([0, gradient+epsilon*response_prime*harmonic, epsilon*response*harmonic_prime, 0])
    phase_gradient = np.array([profile.frequency, 0, 0, 0])
    source = 2*profile.alpha*(np.outer(field_gradient, field_gradient)+field_total**2*np.outer(phase_gradient, phase_gradient)+np.diag(values)*potential(field_total))
    curvature = diagonal_ricci(values, first, seconds)
    return curvature-source, curvature, source


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/curvature-v2'
    output.mkdir(exist_ok=False)
    compact_expression = verify_compact_constraint()
    source = ROOT/'results/fine/status.json'
    report = json.loads(source.read_text(encoding='utf-8'))
    checks = []
    for nominal in [0., .03]:
        row = next(value for value in report['rows'] if value['nominal_flat_compactness'] == nominal)
        profile = Profile(20., nominal)
        spline = spline_for(source.parent/row['archive'])
        problem = TidalProblem(profile, report['arguments']['distance'], report['arguments']['tolerance'])
        for fraction in [.2, .5, .8, .9]:
            position = fraction*profile.radius
            background, perturbation = perturbation_jets(profile, spline, position)
            amplitude, amplitude_prime, amplitude_second, angular, angular_prime, angular_second, response, response_prime, response_second = perturbation
            step = 1e-4*profile.radius
            shifted = [perturbation_jets(profile, spline, position+multiplier*step)[1][3] for multiplier in [-2, -1, 1, 2]]
            derivative = (shifted[0]-8*shifted[1]+8*shifted[2]-shifted[3])/(12*step)
            angular_constraint = abs(derivative-angular_prime)/(1+abs(derivative)+abs(angular_prime))
            first, metric_coefficient, field_coefficient, drive = [float(value[0]) for value in problem.radial_coefficients(np.array([position]))]
            scalar_residual = abs(response_second+first*response_prime-field_coefficient*response-drive*amplitude)/(1+abs(response_second)+abs(first*response_prime)+abs(field_coefficient*response)+abs(drive*amplitude))
            for polar in [.7, 1.2]:
                variations = []
                scale = max(1., abs(amplitude), abs(angular), abs(response/background[0]))
                for relative_step in [.002, .001, .0005]:
                    epsilon = relative_step/scale
                    positive, positive_curvature, positive_source = finite_residual(profile, spline, position, polar, epsilon)
                    negative, negative_curvature, negative_source = finite_residual(profile, spline, position, polar, -epsilon)
                    linear = (positive-negative)/(2*epsilon)
                    normalization = 1+np.linalg.norm((positive_curvature-negative_curvature)/(2*epsilon))+np.linalg.norm((positive_source-negative_source)/(2*epsilon))
                    variations.append({'relative_step': relative_step, 'epsilon': epsilon,
                                       'normalized_linearized_einstein_residual': float(np.linalg.norm(linear)/normalization)})
                checks.append({'nominal': nominal, 'radius_fraction': fraction, 'polar_angle': polar,
                               'angular_constraint_finite_difference_residual': angular_constraint,
                               'scalar_equation_spline_residual': scalar_residual, 'variations': variations})
    result = {'state': 'complete', 'script_sha256': digest(__file__), 'source_path': str(source), 'source_sha256': digest(source),
              'compact_angular_constraint_exactly_verified': True, 'compact_expression': compact_expression,
              'rows': checks, 'scope': 'Independent nonlinear diagonal-metric Ricci evaluator, centered finite perturbations, two angles; background jets from background equations and angular derivatives from reconstructed constraint.'}
    (output/'status.json').write_text(json.dumps(result, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'rows': len(checks),
                      'maximum_small_step_einstein_residual': max(row['variations'][-1]['normalized_linearized_einstein_residual'] for row in checks),
                      'maximum_scalar_residual': max(row['scalar_equation_spline_residual'] for row in checks),
                      'maximum_angular_derivative_residual': max(row['angular_constraint_finite_difference_residual'] for row in checks)}))


if __name__ == '__main__':
    main()
