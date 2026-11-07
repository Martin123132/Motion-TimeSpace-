from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import spherical_jn, spherical_yn


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'axial-tides-20261004'))
from axial_system import Profile, basis, potential


class WaveBody:
    def __init__(self, nominal=.03):
        self.profile = Profile(20., nominal)
        self.radius = self.profile.radius
        self.alpha = self.profile.alpha
        self.mass = self.alpha*self.profile.mass
        self.compactness = 2*self.mass/self.radius
        self.central_lapse = self.profile.row['central_lapse']
        self.central_potential = potential(self.profile.row['central_amplitude'])

    def coefficients(self, coordinate):
        radius = self.radius*coordinate
        if coordinate >= 1:
            metric = 1-self.compactness/coordinate
            return metric, self.compactness/(coordinate**2*metric), 0., metric, np.sqrt(metric)
        field, gradient, mass, metric, xi, canonical = self.profile.values(np.array([radius]))
        metric = float(metric[0])
        lapse = float(xi[0])*np.sqrt(metric)
        matter = float(potential(field[0]))
        speed = lapse*np.sqrt(metric)
        speed_log_prime = ((1-metric)/coordinate-2*self.alpha*self.radius**2*coordinate*matter)/metric
        return speed, speed_log_prime, 8*self.alpha*self.radius**2*matter/metric, metric, lapse

    def solve(self, frequency, tolerance=3e-12, max_step=1/240, start=1e-5, variations=False):
        central = (8*self.alpha*self.radius**2*self.central_potential-frequency**2/self.central_lapse**2)/14
        initial = [1+central*start**2, 2*central*start, start**7/(7*self.central_lapse)]
        if variations:
            assert frequency == 0
            initial.extend([-start**2/(14*self.central_lapse**2), -start/(7*self.central_lapse**2), 0., 0.])

        def equation(coordinate, state):
            speed, speed_log_prime, matter, metric, lapse = self.coefficients(coordinate)
            amplitude, derivative = state[:2]
            coefficient = matter-frequency**2/speed**2
            result = [derivative, -(6/coordinate+speed_log_prime)*derivative+coefficient*amplitude,
                      coordinate**6*amplitude**2/speed]
            if variations:
                first, first_prime, second, second_prime = state[3:]
                result.extend([first_prime, -(6/coordinate+speed_log_prime)*first_prime+matter*first-amplitude/speed**2,
                               second_prime, -(6/coordinate+speed_log_prime)*second_prime+matter*second-first/speed**2])
            return result

        solution = solve_ivp(equation, [start, 1.], initial, method='DOP853',
                             rtol=tolerance, atol=tolerance/30, max_step=max_step, dense_output=True)
        assert solution.success, solution.message
        amplitude, derivative, integral = solution.y[:3, -1]
        speed = 1-self.compactness
        result = {'Y': float(speed*(3+derivative/amplitude)), 'I_over_R': float(integral/amplitude**2),
                  'frequency_R': float(frequency), 'function_evaluations': solution.nfev}
        if variations:
            first, first_prime, second, second_prime = solution.y[3:, -1]
            result['Y_frequency_squared_coefficient'] = float(speed*(first_prime/amplitude-derivative*first/amplitude**2))
            result['Y_frequency_fourth_coefficient'] = float(speed*(second_prime/amplitude-first_prime*first/amplitude**2
                                                                    +derivative*first**2/amplitude**3-derivative*second/amplitude**2))
        return result, solution

    def recover_static(self, impedance):
        speed = 1-self.compactness
        metric_value = speed+impedance
        metric_prime = 2*metric_value+4
        growing, decaying = np.linalg.solve(basis(1., self.compactness), [metric_value, metric_prime])
        return float(self.radius**5*decaying/growing)


def static_outgoing(compactness):
    vacuum = basis(1., compactness)
    metric, derivative = vacuum[:, 1]
    master = (derivative-2*metric)/4
    return float(metric/master-(1-compactness))


def flat_impedance(frequency, outgoing=False):
    regular = spherical_jn(2, frequency)
    regular_prime = spherical_jn(2, frequency, derivative=True)
    if outgoing:
        regular += 1j*spherical_yn(2, frequency)
        regular_prime += 1j*spherical_yn(2, frequency, derivative=True)
    return 1+frequency*regular_prime/regular


def vacuum_impedance(compactness, frequency, outgoing, tolerance=3e-12, phase=60., order=12, horizon=1e-5):
    if frequency == 0:
        return complex(static_outgoing(compactness) if outgoing else 3*(1-compactness)), 0
    if compactness == 0 and not outgoing:
        return complex(flat_impedance(frequency)), 0
    if outgoing:
        coefficients = [1+0j]
        for index in range(order):
            previous = coefficients[index-1] if index else 0
            coefficients.append(((index*(index+1)-6)*coefficients[index]
                                 +compactness*frequency*(4-index**2)*previous)/(2j*(index+1)))
        coordinate = phase/frequency
        amplitude = sum(value/phase**index for index, value in enumerate(coefficients))
        derivative_phase = sum(-index*value/phase**(index+1) for index, value in enumerate(coefficients))
        speed = 1-compactness/coordinate
        initial = 1j*frequency*coordinate+coordinate*speed*frequency*derivative_phase/amplitude
    else:
        frequency_horizon = frequency*compactness
        coefficients = [1+0j]
        for index in range(1, order+1):
            residual = (2*(index-1)*(index-2)+(1-6j*frequency_horizon)*(index-1)-3)*coefficients[index-1]
            if index >= 2:
                residual += ((index-2)*(index-3)-6j*frequency_horizon*(index-2)-6)*coefficients[index-2]
            if index >= 3:
                residual += -2j*frequency_horizon*(index-3)*coefficients[index-3]
            coefficients.append(-residual/(index*(index-2j*frequency_horizon)))
        coordinate = compactness*(1+horizon)
        amplitude = sum(value*horizon**index for index, value in enumerate(coefficients))
        derivative = sum(index*value*horizon**(index-1) for index, value in enumerate(coefficients) if index)
        initial = -1j*frequency*coordinate+horizon*derivative/amplitude

    def equation(log_coordinate, state):
        coordinate = np.exp(log_coordinate)
        speed = 1-compactness/coordinate
        potential_value = speed*(6/coordinate**2-3*compactness/coordinate**3)
        impedance = state[0]
        return [impedance+(coordinate**2*(potential_value-frequency**2)-impedance**2)/speed]

    solution = solve_ivp(equation, [np.log(coordinate), 0.], [initial], method='DOP853',
                         rtol=tolerance, atol=tolerance/30, max_step=.04)
    assert solution.success, solution.message
    return complex(solution.y[0, -1]), solution.nfev
