import os
for name in ['OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS']:
    os.environ[name] = '1'
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'
from navier_stokes_source_audit_20260908 import limit_process
limit_process()

from fractions import Fraction
from time import perf_counter
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from annular_reference_continuum_shell_20260914 import EvidenceRun
from annular_independent_continuum_20260914 import derivative
from annular_reflecting_boundary_20260914 import boundary_derivative, boundary_weights


def rational_identity():
    count = 17
    matrix = [[Fraction(0) for column in range(count)] for row in range(count)]
    rows = [['-24/17', '59/34', '-4/17', '-3/34'], ['-1/2', '0', '1/2'],
            ['4/43', '-59/86', '0', '59/86', '-4/43'],
            ['3/98', '0', '-59/98', '0', '32/49', '-4/49']]
    for row, coefficients in enumerate(rows):
        for column, value in enumerate(coefficients):
            matrix[row][column] = Fraction(value)
            matrix[-1-row][-1-column] = -Fraction(value)
    for row in range(4, count-4):
        for shift, value in [(-2, '1/12'), (-1, '-2/3'), (1, '2/3'), (2, '-1/12')]:
            matrix[row][row+shift] = Fraction(value)
    weights = [Fraction(1) for index in range(count)]
    for index, value in enumerate(['17/48', '59/48', '43/48', '49/48']):
        weights[index] = weights[-1-index] = Fraction(value)
    defects = []
    for row in range(count):
        for column in range(count):
            boundary = -int(row == column == 0)+int(row == column == count-1)
            defects.append(weights[row]*matrix[row][column]+weights[column]*matrix[column][row]-boundary)
    polynomial_errors = []
    for power in range(3):
        for row in range(count):
            exact = power*row**(power-1) if power else 0
            polynomial_errors.append(sum(matrix[row][column]*column**power for column in range(count))-exact)
    return matrix, weights, all(value == 0 for value in defects), all(value == 0 for value in polynomial_errors)


def mode(radius, time, wave_number):
    argument = wave_number*(6-radius)
    amplitude = .11
    scalar = amplitude*np.sin(argument)*np.cos(wave_number*time)/radius
    gradient = amplitude*(-wave_number*np.cos(argument)/radius-np.sin(argument)/radius**2)*np.cos(wave_number*time)
    momentum = -amplitude*wave_number*radius*np.sin(argument)*np.sin(wave_number*time)
    return np.concatenate([scalar, gradient, momentum])


def run():
    evidence = EvidenceRun('annular-reflecting-boundary-attempt01', __file__)
    try:
        evidence.report.update(test_scope='Flat radial scalar, exact Neumann-left/Dirichlet-right eigenmode; active boundary, not coupled gravity.',
                               new_boundary_formal_order='fourth interior, second boundary',
                               parent_source_support_action_derived=False)
        matrix, weights, exact_identity, exact_quadratic = rational_identity()
        evidence.check('exact_rational_summation_by_parts_identity', exact_identity)
        evidence.check('exact_boundary_quadratic_consistency', exact_quadratic)
        identity = np.eye(17)
        actual = np.column_stack([boundary_derivative(identity[:, column], 1.) for column in range(17)])
        evidence.check('implemented_operator_matches_exact_matrix', np.max(abs(actual-np.array(matrix, dtype=float))) < 2e-16)
        radius = np.linspace(5., 6., 17)
        random = np.random.default_rng(1417)
        gradient, momentum = random.normal(size=(2, 17))
        gradient[0], momentum[-1] = 0., 0.
        speed = .6+.1*(radius-5)
        rate = speed*momentum/radius**2
        force = radius**2*speed*gradient
        gradient_rate = boundary_derivative(rate, 1/16)
        momentum_rate = boundary_derivative(force, 1/16)
        gradient_rate[0], momentum_rate[-1] = 0., 0.
        energy_rate = boundary_weights(17, 1/16) @ (force*gradient_rate+rate*momentum_rate)
        evidence.check('arbitrary_positive_frozen_metric_energy_cancels', abs(energy_rate) < 1e-12, float(energy_rate))
        wrong_rate = boundary_weights(17, 1/16) @ (force*gradient_rate-rate*momentum_rate)
        evidence.check('wrong_flux_sign_negative_control_detected', abs(wrong_rate) > .01, float(wrong_rate))
        wave_number = brentq(lambda value: 5*value*np.cos(value)+np.sin(value), np.pi/2, np.pi, xtol=1e-14)
        evidence.check('analytic_left_neumann_condition', abs(5*wave_number*np.cos(wave_number)+np.sin(wave_number)) < 1e-13)
        evidence.report['wave_number'] = wave_number
        for label, operator in [('original_one_sided', derivative), ('energy_boundary', boundary_derivative)]:
            for count in [65, 129, 257]:
                started = perf_counter()
                radius = np.linspace(5., 6., count)
                spacing = 1/(count-1)
                initial = mode(radius, 0., wave_number)
                initial.reshape(3, count)[1, 0] = 0.
                weight = boundary_weights(count, spacing)

                def rhs(time, state):
                    scalar, gradient, momentum = state.reshape(3, count)
                    rate = momentum/radius**2
                    gradient_rate = operator(rate, spacing)
                    momentum_rate = operator(radius**2*gradient, spacing)
                    gradient_rate[0], momentum_rate[-1], rate[-1] = 0., 0., 0.
                    return np.concatenate([rate, gradient_rate, momentum_rate])

                times = np.linspace(0., 2., 81)
                solution = solve_ivp(rhs, (0., 2.), initial, method='DOP853', rtol=2e-11, atol=2e-13,
                                     max_step=spacing/4, t_eval=times)
                evidence.check(label+str(count)+'_solver_finished', solution.success)
                states = solution.y.T.reshape(-1, 3, count)
                energies = .5*np.sum(weight*(radius**2*states[:, 1]**2+states[:, 2]**2/radius**2), axis=1)
                exact = mode(radius, 2., wave_number).reshape(3, count)
                error = states[-1]-exact
                error_norm = np.sqrt(np.sum(weight*(radius**2*error[1]**2+error[2]**2/radius**2)))
                row = dict(branch=label, count=count, seconds=perf_counter()-started,
                           solution_energy_norm_error=float(error_norm),
                           relative_energy_drift=float(np.max(abs(energies-energies[0]))/energies[0]),
                           boundary_gradient_peak=float(np.max(abs(states[:, 1, -1]))),
                           finite=bool(np.isfinite(states).all()))
                evidence.report['cases'].append(row)
                output = evidence.output/(label+'_count'+str(count)+'.npz')
                np.savez_compressed(output, radii=radius, times=times, states=states, energies=energies)
                evidence.own(output, 'outputs')
                evidence.check(label+str(count)+'_finite_and_active', row['finite'] and row['boundary_gradient_peak'] > .02)
                evidence.save()
                print(row, flush=True)
        for label in ['original_one_sided', 'energy_boundary']:
            rows = [row for row in evidence.report['cases'] if row['branch'] == label]
            qualified = all(row['relative_energy_drift'] < 1e-5 for row in rows) and all(
                later['solution_energy_norm_error'] < earlier['solution_energy_norm_error']/3
                for earlier, later in zip(rows, rows[1:]))
            evidence.report[label+'_numerically_qualified_on_this_mode'] = qualified
        rows = [row for row in evidence.report['cases'] if row['branch'] == 'energy_boundary']
        evidence.check('new_boundary_exact_energy_test', max(row['relative_energy_drift'] for row in rows) < 1e-10)
        evidence.check('new_boundary_refinement_test', evidence.report['energy_boundary_numerically_qualified_on_this_mode'])
        evidence.complete()
    except Exception as error:
        evidence.fail(error)
        raise


if __name__ == '__main__':
    run()
