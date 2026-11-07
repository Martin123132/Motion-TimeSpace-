from pathlib import Path

import numpy as np
import sympy as sp

from interior_energy import Interior, dependencies, digest, save, modest_process


def main():
    modest_process()
    names = 'r F N Fp n h hp H K Kp J Jp u s sp spp alpha w W'
    symbols = sp.symbols(names, real=True)
    radius, metric, lapse, metric_prime, lapse_prime, field, gradient, time_metric, angular, angular_prime, shift, shift_prime, response, phase, phase_prime, phase_second, alpha, rotation, energy = symbols
    measure = radius**2/(lapse*sp.sqrt(metric))
    radial_rate = time_metric-2*metric*shift_prime-metric_prime*shift
    angular_rate = angular-2*metric*shift/radius
    mass_form = measure/(8*alpha)*(-4*radial_rate*angular_rate-2*angular_rate**2+12*metric*shift**2/radius**2)
    mass_form += measure*((response-metric*shift*gradient)**2
        +2*rotation*phase*(2*field*response+field**2*(time_metric+angular))
        +2*rotation*metric*shift*field**2*phase_prime
        -lapse**2*field**2*(metric*phase_prime**2+6*phase**2/radius**2))
    lagrangian = mass_form/2
    derivatives = {radius:1, metric:metric_prime, lapse:lapse*lapse_prime,
                   field:gradient, angular:angular_prime, shift:shift_prime,
                   phase:phase_prime, phase_prime:phase_second}

    def derivative(expression):
        return sum(sp.diff(expression, key)*value for key, value in derivatives.items())

    shift_euler = sp.diff(lagrangian, shift)-derivative(sp.diff(lagrangian, shift_prime))
    shift_normalization = sp.factor(sp.diff(shift_euler, angular_prime))
    shift_equation = sp.factor(shift_euler/shift_normalization)
    pressure = (metric*gradient**2+rotation**2*field**2/lapse**2)/2-energy
    substitutions = {metric_prime:(1-metric)/radius-alpha*radius*(metric*gradient**2+rotation**2*field**2/lapse**2+2*energy),
                     lapse_prime:((1-metric)/2+alpha*radius**2*pressure)/(radius*metric)}
    expected_angular = ((lapse_prime-1/radius)*angular+time_metric/radius
        +(3/radius**2-2*alpha*rotation**2*field**2/lapse**2)*shift
        +2*alpha*rotation*field**2*phase_prime-2*alpha*gradient*response)
    shift_residual = sp.factor((shift_equation-angular_prime+expected_angular).subs(substitutions))
    assert shift_residual == 0, shift_residual
    phase_euler = sp.diff(lagrangian, phase)-derivative(sp.diff(lagrangian, phase_prime))
    phase_normalization = sp.factor(sp.diff(phase_euler, phase_second))
    phase_equation = sp.factor(phase_euler/phase_normalization)
    first = 2/radius+lapse_prime+metric_prime/(2*metric)
    parent_shift_prime = (time_metric+angular-4*alpha*rotation*field**2*phase)/metric-(first-2/radius)*shift
    expected_phase_second = (-(first+2*gradient/field)*phase_prime
        +(6/radius**2-4*alpha*rotation**2*field**2/lapse**2)*phase/metric
        -2*rotation*response/(metric*lapse**2*field)
        +2*rotation/lapse**2*(1/radius-lapse_prime+gradient/field)*shift)
    phase_residual = sp.factor((phase_equation-phase_second+expected_phase_second).subs(shift_prime, parent_shift_prime))
    assert phase_residual == 0, phase_residual
    evaluator = sp.lambdify(symbols, [shift_equation, phase_equation], 'numpy', cse=True)
    interior = Interior('refined')
    random = np.random.default_rng(20261006)
    rows = []
    for fraction in [.1, .25, .5, .7, .85, .95]:
        position = np.array([fraction*interior.radius])
        baseline = interior.fields(position)[0]/interior.master_surface
        trial = baseline*(1+.2*random.normal(size=(6, 1)))
        flow, lapse_perturbation, _ = interior.problem.physical_evolution(position, trial)
        background = interior.problem.background(position)
        amplitude, amplitude_gradient, metric_value, lapse2, potential_value, _, _, _, lapse_log_derivative, background_first = [value[0] for value in background]
        metric_derivative = 2*metric_value*(background_first-2/position[0]-lapse_log_derivative)
        args = [position[0], metric_value, np.sqrt(lapse2), metric_derivative, lapse_log_derivative,
                amplitude, amplitude_gradient, lapse_perturbation[0], trial[0, 0], flow[0, 0],
                trial[1, 0], flow[1, 0], trial[2, 0], trial[4, 0], trial[5, 0], flow[5, 0],
                interior.alpha, interior.frequency, potential_value]
        values = evaluator(*args)
        scale = [1+abs(flow[0, 0])+abs(trial[0, 0]/position[0]),
                 1+abs(flow[5, 0])+abs(trial[5, 0]/position[0])]
        errors = [float(abs(value)/normalization) for value, normalization in zip(values, scale)]
        assert max(errors) < 1e-10, (fraction, errors)
        rows.append(dict(radius_fraction=fraction, scaled_momentum_constraint_error=errors[0],
                         scaled_phase_equation_error=errors[1]))
    inputs = dependencies()
    inputs[str(interior.archive_path)] = digest(interior.archive_path)
    inputs[str(interior.profile.path)] = digest(interior.profile.path)
    result = save('constraint-replay', Path(__file__), dict(input_hashes=inputs,
        exact_checks=[dict(name='Shift variation recovers parent angular/momentum equation', residual=str(shift_residual), passed=True),
                      dict(name='Phase variation recovers parent divided current equation', residual=str(phase_residual), passed=True)],
        rows=rows, numerical_checks=2*len(rows),
        shift_euler_equation=str(shift_equation), phase_euler_equation=str(phase_equation),
        scope='Leading-frequency stationary odd fields; coupled to the inherited static even fields and background equations.'))
    print(dict(state=result['state'], exact_checks=2, numerical_checks=result['numerical_checks'],
               maximum_error=max(max(row['scaled_momentum_constraint_error'], row['scaled_phase_equation_error']) for row in rows)), flush=True)


if __name__ == '__main__':
    main()

