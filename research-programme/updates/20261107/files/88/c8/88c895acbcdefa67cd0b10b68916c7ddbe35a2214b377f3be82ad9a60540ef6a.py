from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
import sys

import numpy as np
from scipy.integrate import solve_bvp
import sympy as sp


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'radial-pulsations-20261003'))
from solve_pulsations import Profile
from test_radial_energy import potential, potential_prime


@lru_cache(maxsize=1)
def h_coefficients():
    data = json.loads((ROOT/'results/reduction/status.json').read_text())
    symbols = sp.symbols(' '.join(data['coefficient_symbols']), real=True)
    environment = dict(zip(data['coefficient_symbols'], symbols))
    return sp.lambdify(symbols, [sp.sympify(value, locals=environment) for value in data['H_coefficients']], 'numpy', cse=True)


@lru_cache(maxsize=1)
def vacuum_functions():
    radius, mass, square = sp.symbols('radius mass square')
    metric = 1-2*mass/radius
    lapse_prime = mass/(radius**2*metric)
    numerator = 2*radius*(radius-2*mass)+mass*(radius-3*mass)-square*radius**4
    denominator = (radius-2*mass)*(2*radius+3*mass)
    time_row = sp.Matrix([[numerator/denominator, -(3*mass-square*radius**3)/(radius*(2*radius+3*mass))]])
    flow = sp.Matrix([[time_row[0]/radius+lapse_prime-1/radius, time_row[1]/radius+3/radius**2],
                      [(time_row[0]+1)/metric, time_row[1]/metric-2*lapse_prime]])
    second_flow = sp.diff(flow, radius)+flow*flow
    time_prime = sp.diff(time_row, radius)+time_row*flow
    time_second = sp.diff(time_prime, radius)+time_prime*flow
    return sp.lambdify((radius, mass, square), [time_row, flow, second_flow, time_prime, time_second], 'numpy', cse=True)


def vacuum_data(radius, mass, square):
    return [np.asarray(value) for value in vacuum_functions()(radius, mass, square)]


def edge_state(radius, mass, frequency, square, distance, amplitude, phase0, metric0):
    compactness = 2*mass/radius
    surface = 1-compactness
    constant = (12*surface)**(-1.5)
    background2 = (compactness+2)/(10*radius*surface)
    background3 = (9*compactness**2-6*compactness-5*frequency**2*radius**2+42)/(270*radius**2*surface**2)
    background4 = -(648*compactness**3-2142*compactness**2+405*compactness*frequency**2*radius**2+1806*compactness+110*frequency**2*radius**2-2436)/(18900*radius**3*surface**3)
    inverse1 = compactness/(radius*surface)
    inverse2 = compactness/(radius**2*surface)+inverse1**2
    inverse3 = compactness/(radius**3*surface)+2*compactness*inverse1/(radius**2*surface)+inverse1**3
    singular1 = 2*(inverse1-2*background2)
    singular2 = 2*(inverse2-2*background2*inverse1+3*background2**2-2*background3)
    singular3 = 2*(inverse3-2*background2*inverse2+(3*background2**2-2*background3)*inverse1-4*background2**3+6*background2*background3-2*background4)
    first0 = (1+1/surface)/radius
    first1 = (1+1/surface)/radius**2+inverse1/(surface*radius)
    first2 = (1+1/surface)/radius**3+inverse1/(surface*radius**2)+inverse2/(surface*radius)
    regular0 = 6/(radius**2*surface)-(frequency**2+square)/surface**2
    regular1 = 6*(2/radius+inverse1)/(radius**2*surface)-2*(frequency**2+square)*inverse1/surface**2
    time_row, flow, second_flow, time_prime, time_second = vacuum_data(radius, mass, square)
    tide = (time_row@metric0)[0]
    tide_prime = (time_prime@metric0)[0]
    tide_second = (time_second@metric0)[0]
    metric_d = -flow@metric0
    metric_d2 = second_flow@metric0/2
    drive1 = 1/(2*np.sqrt(12*surface))
    drive2 = drive1*background2+3*constant*compactness/radius
    drive3 = drive1*background3-2*frequency**2*constant/surface+3*constant*compactness*(4*background2+2/radius)/radius
    force1 = drive1*tide/surface
    force2 = (drive2*tide-drive1*tide_prime+inverse1*drive1*tide)/surface
    force3 = (drive3*tide-drive2*tide_prime+drive1*tide_second/2+inverse1*(drive2*tide-drive1*tide_prime)+inverse2*drive1*tide)/surface-2*frequency*constant*square*phase0/surface**2
    cubic = ((2*first0+singular1)*amplitude+force1)/4
    quartic = ((3*first0+singular1)*cubic+(2*first1+singular2+regular0)*amplitude+force2)/10
    quintic = ((4*first0+singular1)*quartic+(3*first1+singular2+regular0)*cubic+(2*first2+singular3+regular1)*amplitude+force3)/18
    phase1 = -frequency*amplitude/(3*constant*surface**2)-frequency*metric0[1]/surface
    phase_first0 = -first0+6*background2
    phase_first1 = -first1+12*background3-6*background2**2
    phase_regular0 = 6/(radius**2*surface)-square/surface**2
    phase_regular1 = 6*(2/radius+inverse1)/(radius**2*surface)-2*square*inverse1/surface**2
    source0 = 2*frequency/(constant*surface**2)*(cubic+amplitude*(2*inverse1-3*background2))
    source1 = 2*frequency/(constant*surface**2)*(quartic+cubic*(2*inverse1-3*background2)+amplitude*(inverse1**2+2*inverse2-6*inverse1*background2+6*background2**2-3*background3))
    lapse_prime = compactness/(2*radius*surface)
    lapse_prime_d = compactness*(2-compactness)/(2*radius**2*surface**2)
    shift_coefficient0 = 1/radius-lapse_prime-3*background2
    shift_coefficient1 = 1/radius**2-lapse_prime_d-6*background3+3*background2**2
    source0 += 6*frequency/surface*(metric_d[1]+inverse1*metric0[1])-2*frequency/surface*shift_coefficient0*metric0[1]
    source1 += 6*frequency/surface*(metric_d2[1]+inverse1*metric_d[1]+inverse2*metric0[1])-2*frequency/surface*(shift_coefficient0*metric_d[1]+(shift_coefficient1+inverse1*shift_coefficient0)*metric0[1])
    phase2 = -(phase_first0*phase1-phase_regular0*phase0+source0)/14
    phase3 = -(2*phase_first0*phase2+phase_first1*phase1-phase_regular0*phase1-phase_regular1*phase0+source1)/24
    value = amplitude*distance**2+cubic*distance**3+quartic*distance**4+quintic*distance**5
    derivative = -2*amplitude*distance-3*cubic*distance**2-4*quartic*distance**3-5*quintic*distance**4
    phase_value = phase0+phase1*distance+phase2*distance**2+phase3*distance**3
    phase_derivative = -phase1-2*phase2*distance-3*phase3*distance**2
    metric_value = metric0+metric_d*distance+metric_d2*distance**2
    return np.array([*metric_value, value, derivative, phase_value, phase_derivative])


class DynamicProblem:
    def __init__(self, profile, sigma, distance=.01, tolerance=2e-7):
        self.profile, self.sigma, self.distance, self.tolerance = profile, sigma, distance, tolerance
        self.radius, self.mass = profile.radius, profile.alpha*profile.mass
        self.square = sigma**2
        self.lower, self.upper = 1e-5, 1-distance/self.radius
        self.scales = np.array([self.radius**2, self.radius**3, self.radius**4, self.radius**3, self.radius**6, self.radius**5])
        self.parameter_scales = np.array([self.radius**4, self.radius**6, self.radius**2, self.radius**3])
        self.center_field = profile.values(np.array([self.lower*self.radius]))[0][0]

    def background(self, position):
        field, gradient, mass, metric, xi, canonical = self.profile.values(position)
        lapse2 = xi**2*metric
        energy = potential(field)
        energy_prime = potential_prime(field)
        energy_second = field**(-2/3)/6+1.5*field**2
        rotation = self.profile.frequency**2/lapse2
        pressure = (metric*gradient**2+rotation*field**2)/2-energy
        lapse_prime = self.profile.alpha*(mass+position**3*pressure)/(position**2*metric)
        first = (1+metric-2*self.profile.alpha*position**2*energy)/(position*metric)
        return field, gradient, metric, lapse2, energy, energy_prime, energy_second, rotation, lapse_prime, first

    def physical_evolution(self, position, state):
        field, gradient, metric, lapse2, energy, energy_prime, energy_second, rotation, lapse_prime, first = self.background(position)
        alpha, frequency = self.profile.alpha, self.profile.frequency
        angular, shift, response, response_prime, phase, phase_prime = state
        coefficients = h_coefficients()(position, metric, lapse2, field, gradient, energy, energy_prime, energy_second, alpha, frequency, self.square)
        amplitude = sum(coefficient*value for coefficient, value in zip(coefficients, state))
        angular_prime = (lapse_prime-1/position)*angular+amplitude/position+(3/position**2-2*alpha*rotation*field**2)*shift+2*alpha*frequency*field**2*phase_prime-2*alpha*gradient*response
        shift_prime = (amplitude+angular-4*alpha*frequency*field**2*phase)/metric-(first-2/position)*shift
        drive = energy_prime-2*rotation*field-2*metric*lapse_prime*gradient
        response_prime2 = -first*response_prime+(6/position**2+energy_second-rotation+4*alpha*metric*gradient**2-self.square/lapse2)*response/metric+drive*amplitude/metric-2*frequency*field*self.square*phase/(metric*lapse2)
        phase_prime2 = -(first+2*gradient/field)*phase_prime+(6/position**2-(self.square+4*alpha*frequency**2*field**2)/lapse2)*phase/metric-2*frequency*response/(metric*lapse2*field)+2*frequency/lapse2*(1/position-lapse_prime+gradient/field)*shift
        amplitude_prime = angular_prime-2*lapse_prime*amplitude+4*alpha*gradient*response-self.square*shift/lapse2
        return np.vstack([angular_prime, shift_prime, response_prime, response_prime2, phase_prime, phase_prime2]), amplitude, amplitude_prime

    def equation(self, coordinate, state, parameters):
        physical = state*self.scales[:, None]
        derivative, amplitude, amplitude_prime = self.physical_evolution(self.radius*coordinate, physical)
        return derivative*self.radius/self.scales[:, None]

    def boundary(self, left, right, parameters):
        amplitude, phase0, angular0, shift0 = parameters*self.parameter_scales
        expected = edge_state(self.radius, self.mass, self.profile.frequency, self.square, self.distance, amplitude, phase0, np.array([angular0, shift0]))/self.scales
        residual = right-expected
        residual[2] /= self.distance**2
        residual[3] /= self.radius*self.distance
        return np.r_[left[1]-self.lower*(2*left[0]-4*self.profile.alpha*self.profile.frequency*self.center_field**2*self.radius**4*left[4])/3,
                     left[3]-2*left[2]/self.lower, left[5]-2*left[4]/self.lower,
                     residual, parameters[2]+2]

    def solve(self, previous=None):
        mesh = np.unique(np.r_[np.linspace(self.lower, self.upper, 400), np.linspace(max(self.lower, 1-12/self.radius), self.upper, 500)])
        if previous is None:
            guess = np.vstack([-2*mesh**2, -4*mesh**3/3, -.04*mesh**2*(1-mesh)**2, -.08*mesh*(1-mesh)*(1-2*mesh), -.004*mesh**2, -.008*mesh])
            parameters = np.array([-.04, -.004, -2., -4/3])
        else:
            guess, parameters = previous.sol(mesh), previous.p
        if np.iscomplexobj(self.sigma):
            guess, parameters = guess.astype(complex), parameters.astype(complex)
        return solve_bvp(self.equation, self.boundary, mesh, guess, p=parameters, tol=self.tolerance, bc_tol=self.tolerance/10, max_nodes=18000)

    def surface(self, solution):
        amplitude, phase0, angular, shift = solution.p*self.parameter_scales
        time_row, flow, second_flow, time_prime, time_second = vacuum_data(self.radius, self.mass, self.square)
        pair = np.array([angular, shift])
        time_value, time_derivative = (time_row@pair)[0], (time_prime@pair)[0]
        radius, mass = self.radius, self.mass
        metric = 1-2*mass/radius
        first = (6*radius**2+6*mass*radius+6*mass**2)/(radius**2*(2*radius+3*mass))
        second = (2*radius**2-6*mass*radius-3*mass**2)/((radius-2*mass)*(2*radius+3*mass))
        master, master_prime = np.linalg.solve(np.array([[first, metric], [second, radius]]), pair)
        return time_value, time_derivative, master, metric*master_prime
