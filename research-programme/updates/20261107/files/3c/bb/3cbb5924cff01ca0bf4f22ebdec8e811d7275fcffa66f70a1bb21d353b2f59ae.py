from __future__ import annotations

from pathlib import Path
import sys

import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import hyp2f1


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'radial-gravity-stability-20261003'))
from test_radial_energy import Profile, Quadrature, potential


def basis(coordinate, compactness):
    ratio = compactness/coordinate
    special = hyp2f1(1, 4, 6, ratio)
    derivative = (2/3)*hyp2f1(2, 5, 7, ratio)
    return np.array([[coordinate**3*(1-ratio), coordinate**-2*special],
                     [coordinate**2*(3-2*ratio), coordinate**-3*(-2*special-ratio*derivative)]])


class AxialProblem:
    def __init__(self, nominal):
        self.profile = Profile(20., nominal)
        self.radius = self.profile.radius
        self.alpha = self.profile.alpha
        self.mass = self.alpha*self.profile.mass
        self.compactness = 2*self.mass/self.radius
        center = self.profile.row
        rotation = .5*self.profile.frequency**2*center['central_amplitude']**2/center['central_lapse']**2
        density = rotation+potential(center['central_amplitude'])
        pressure = rotation-potential(center['central_amplitude'])
        self.center_coefficient = (11*density/3+pressure)/14

    def background(self, coordinate):
        if coordinate >= 1:
            position = self.radius*coordinate
            return 0., 0., self.profile.mass, 1-2*self.mass/position
        position = np.array([self.radius*coordinate])
        field, gradient, mass, metric, xi, canonical = self.profile.values(position)
        rotation = self.profile.frequency**2*field**2/(xi**2*metric)
        density = .5*(metric*gradient**2+rotation)+potential(field)
        pressure = density-2*potential(field)
        return float(density[0]), float(pressure[0]), float(mass[0]), float(metric[0])

    def equation(self, coordinate, state):
        density, pressure, mass, metric = self.background(coordinate)
        radial = self.radius*coordinate
        shift = self.alpha*radial*(density+pressure)/metric
        source = ((density+pressure)+8*mass/radial**3)/metric
        return [state[1], -(6/coordinate-self.radius*shift)*state[1]+source*(1+self.alpha*self.radius**2*state[0])]

    def solve(self, tolerance, max_step, start):
        initial = [self.center_coefficient*start**2, 2*self.center_coefficient*start]
        solution = solve_ivp(self.equation, [start, 1.], initial, method='DOP853',
                             rtol=tolerance, atol=tolerance/20, max_step=max_step, dense_output=True)
        assert solution.success, solution.message
        return solution

    def match(self, coordinate, state):
        correction, slope = state
        amplitude = 1+self.alpha*self.radius**2*correction
        metric_value = coordinate**3*amplitude
        metric_prime = 3*coordinate**2*amplitude+self.alpha*self.radius**2*coordinate**3*slope
        vacuum = basis(coordinate, self.compactness)
        decaying_over_alpha = ((2*self.profile.mass/self.radius)*coordinate**4*amplitude
                               -(1-self.compactness/coordinate)*self.radius**2*coordinate**6*slope)/5
        decaying = self.alpha*decaying_over_alpha
        growing = (metric_value-decaying*vacuum[0, 1])/vacuum[0, 0]
        return {'growing': float(growing), 'decaying_scaled': float(decaying),
                'response': float(self.radius**5*decaying/growing),
                'response_over_alpha': float(self.radius**5*decaying_over_alpha/growing),
                'surface_log_derivative': float(coordinate*metric_prime/metric_value)}


def weak_integral(cells=240, order=12):
    profile = Profile(20., 0.)
    quadrature = Quadrature(profile.radius, cells, order)
    field = profile.values(quadrature.position)[0]
    return float((2/5)*quadrature.integrate(quadrature.position**6*potential(field)))
