from __future__ import annotations

from pathlib import Path
import mpmath as mp
import numpy as np
import sympy as sp

from polar_energy import Background, even_form, modest_process, save, dependencies


def main():
    modest_process()
    radius, polar, azimuth = sp.symbols('r z phi', real=True)
    coordinates = [radius, polar, azimuth]
    metric = sp.Function('F')(radius)
    momentum_radial = sp.Function('p')(radius)
    momentum_angular = sp.Function('k')(radius)
    momentum_mixed = sp.Function('j')(radius)
    momentum_tensor = sp.Function('g')(radius)
    metric_covariant = sp.diag(1/metric, radius**2/(1-polar**2), radius**2*(1-polar**2))
    inverse = metric_covariant.inv()
    connection = [[[sp.simplify(sum(inverse[upper, contraction]*(sp.diff(metric_covariant[contraction, right], coordinates[left])+sp.diff(metric_covariant[contraction, left], coordinates[right])-sp.diff(metric_covariant[left, right], coordinates[contraction]))/2 for contraction in range(3))) for right in range(3)] for left in range(3)] for upper in range(3)]
    harmonic = (3*polar**2-1)/2
    tensor_covariant = sp.Matrix([[momentum_radial*harmonic/metric, momentum_mixed*sp.diff(harmonic, polar), 0], [momentum_mixed*sp.diff(harmonic, polar), radius**2*(momentum_angular*harmonic/(1-polar**2)+3*momentum_tensor/2), 0], [0, 0, radius**2*(momentum_angular*harmonic*(1-polar**2)-3*momentum_tensor*(1-polar**2)**2/2)]])
    tensor_mixed = inverse*tensor_covariant
    divergence = [sp.factor(sum(sp.diff(tensor_mixed[upper, lower], coordinates[upper])+sum(connection[upper][upper][middle]*tensor_mixed[middle, lower]-connection[middle][upper][lower]*tensor_mixed[upper, middle] for middle in range(3)) for upper in range(3))) for lower in range(3)]
    checks = []

    def check(name, residual):
        residual = sp.factor(residual)
        checks.append(dict(name=name, residual=str(residual), passed=residual == 0))
        assert residual == 0, (name, residual)

    check('independent radial tensor divergence', divergence[0]/harmonic-sp.diff(momentum_radial, radius)-2*(momentum_radial-momentum_angular)/radius+6*momentum_mixed/radius**2)
    check('independent angular tensor divergence', divergence[1]/sp.diff(harmonic, polar)-metric*sp.diff(momentum_mixed, radius)-(sp.diff(metric, radius)/2+2*metric/radius)*momentum_mixed-momentum_angular+2*momentum_tensor)
    check('azimuthal divergence', divergence[2])
    harmonic_norm = sp.integrate(harmonic**2, (polar, -1, 1))
    check('tensor trace', sp.trace(tensor_mixed)/harmonic-momentum_radial-2*momentum_angular)
    integrated_square = sp.integrate(sp.trace(tensor_mixed*tensor_mixed), (polar, -1, 1))/harmonic_norm
    check('tensor harmonic contraction', integrated_square-momentum_radial**2-2*momentum_angular**2-12*metric*momentum_mixed**2/radius**2-12*momentum_tensor**2)
    background = Background()
    nodes, weights = np.polynomial.legendre.leggauss(40)
    mp.mp.dps = 50
    angular_data = [(mp.mpf(str(node)), mp.mpf(str(weight))) for node, weight in zip(nodes, weights)]
    rows = []
    for fraction in [.2, .55, .9]:
        position = np.array([fraction*background.radius])
        values = background.values(position)
        field, gradient, metric_value, lapse, log_lapse_prime = [float(values[key][0]) for key in ['field', 'gradient', 'metric', 'lapse', 'log_lapse_prime']]
        radial, angular, angular_prime = .17, -.23, .037/background.radius
        amplitude, amplitude_prime = .13*field, -.17*gradient
        phase_momentum = .19*background.frequency*field/lapse
        singleton = lambda value: np.array([[value]])
        expected = float(even_form(background, position, np.ones(1), singleton(radial), singleton(angular), singleton(angular_prime), singleton(amplitude), singleton(amplitude_prime), singleton(phase_momentum))[0, 0]/2)
        mp_radius, mp_metric, mp_lapse, mp_log_prime, mp_field, mp_gradient, mp_frequency, mp_alpha = [mp.mpf(str(value)) for value in [position[0], metric_value, lapse, log_lapse_prime, field, gradient, background.frequency, background.alpha]]
        mp_radial, mp_angular, mp_angular_prime, mp_amplitude, mp_amplitude_prime, mp_phase_momentum = [mp.mpf(str(value)) for value in [radial, angular, angular_prime, amplitude, amplitude_prime, phase_momentum]]

        def nonlinear(epsilon):
            total = mp.mpf(0)
            for node, weight in angular_data:
                harmonic_value = mp.sqrt(5/(4*mp.pi))*(3*node**2-1)/2
                harmonic_gradient = mp.sqrt(5/(4*mp.pi))*3*node
                radial_factor = 1+epsilon*mp_radial*harmonic_value
                angular_factor = 1+epsilon*mp_angular*harmonic_value
                root_radial = mp.sqrt(radial_factor/mp_metric)
                root_angular = mp_radius*mp.sqrt(angular_factor)
                root_angular_prime = mp.sqrt(angular_factor)+mp_radius*epsilon*mp_angular_prime*harmonic_value/(2*mp.sqrt(angular_factor))
                angular_cross = (1-node**2)*epsilon**2*mp_radial*mp_angular*harmonic_gradient**2/(4*mp.sqrt(mp_metric*radial_factor)*angular_factor)
                curvature_bulk = 2*mp_lapse*root_radial+2*mp_lapse*angular_cross+2*mp_lapse*root_angular_prime**2/root_radial+4*mp_lapse*mp_log_prime*root_angular*root_angular_prime/root_radial
                current_field = mp_field+epsilon*mp_amplitude*harmonic_value
                current_gradient = mp_gradient+epsilon*mp_amplitude_prime*harmonic_value
                current_momentum = mp_frequency*mp_field**2/mp_lapse+epsilon*mp_field*mp_phase_momentum*harmonic_value
                volume_ratio = mp.sqrt(radial_factor)*angular_factor
                scalar = mp_lapse*mp_radius**2/mp.sqrt(mp_metric)*(current_momentum**2/(2*volume_ratio*current_field**2)+volume_ratio*(mp_metric*current_gradient**2/(2*radial_factor)+epsilon**2*mp_amplitude**2*(1-node**2)*harmonic_gradient**2/(2*root_angular**2)+3*current_field**(mp.mpf(4)/3)/8+current_field**4/8))
                total += 2*mp.pi*weight*(-curvature_bulk/(4*mp_alpha)+scalar)
            return total

        baseline = nonlinear(mp.mpf(0))
        errors = []
        for epsilon in [mp.mpf('.01'), mp.mpf('.005'), mp.mpf('.0025')]:
            measured = (nonlinear(epsilon)+nonlinear(-epsilon)-2*baseline)/(2*epsilon**2)
            error = float(abs(measured-mp.mpf(str(expected)))/max(abs(expected), 1))
            errors.append(error)
            rows.append(dict(radius_fraction=fraction, epsilon=float(epsilon), nonlinear_coefficient=float(measured), quadratic_form=expected, scaled_error=error))
        assert errors[-1] < 5e-6 and 3.8 < errors[-2]/errors[-1] < 4.2, errors
    save('independent', Path(__file__), dict(input_hashes=dependencies(background.profile), exact_checks=checks,
         nonlinear_rows=rows, arithmetic_digits=50, angular_gauss_order=40,
         largest_finest_error=max(row['scaled_error'] for row in rows if row['epsilon'] == .0025),
         scope='Independent covariant tensor divergence/contraction and finite nonlinear Hamiltonian bulk variations; no parent constraints substituted into variation test.'))
    print(dict(exact_checks=len(checks), nonlinear_checks=len(rows), maximum_finest_error=max(row['scaled_error'] for row in rows if row['epsilon'] == .0025)), flush=True)


if __name__ == '__main__':
    main()
