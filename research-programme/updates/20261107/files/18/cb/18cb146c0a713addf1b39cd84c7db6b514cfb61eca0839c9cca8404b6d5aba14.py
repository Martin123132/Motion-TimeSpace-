from __future__ import annotations

import os
for variable in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ[variable] = '1'
import sys
sys.dont_write_bytecode = True
from functools import lru_cache
import numpy as np
from scipy import special


@lru_cache(maxsize=8)
def radial_rule(order):
    return special.roots_genlaguerre(order, .5)


def particle_moments(theta, order=32):
    theta = np.asarray(theta, dtype=float)
    if np.any(~np.isfinite(theta)) or np.any(theta <= 0):
        raise ValueError('Positive finite kBT/(mc^2) required')
    nodes, weights = radial_rule(order)
    scaled = theta[..., None] * nodes
    measure = weights * (1 + scaled) * np.sqrt(2 + scaled)
    measure = measure / measure.sum(axis=-1, keepdims=True)
    mean = np.sum(measure * nodes, axis=-1)
    variance = np.sum(measure * (nodes - mean[..., None])**2, axis=-1)
    pressure = np.sum(measure * nodes * (2 + scaled) / (3 * (1 + scaled)), axis=-1)
    return dict(energy_over_kBT=mean, cv_over_kB=variance, pressure_over_nkBT=pressure)


class Mixture:
    def __init__(self, helium_number, electron_to_hydrogen_mass, electron_to_helium_mass):
        if helium_number < 0 or min(electron_to_hydrogen_mass, electron_to_helium_mass) <= 0:
            raise ValueError('Invalid mixture')
        self.fractions = np.array([1 + 2 * helium_number, 1., helium_number]) / (2 + 3 * helium_number)
        self.mass_ratios = np.array([1., electron_to_hydrogen_mass, electron_to_helium_mass])

    def state(self, theta_star, ratio=1., order=32, relativistic_ions=False):
        theta_star, ratio = np.broadcast_arrays(np.asarray(theta_star), np.asarray(ratio))
        if np.any(ratio <= 0):
            raise ValueError('Positive gas temperature required')
        excess_energy = np.zeros_like(theta_star, dtype=float)
        excess_capacity = np.zeros_like(theta_star, dtype=float)
        active = range(3) if relativistic_ions else range(1)
        for species in active:
            moments = particle_moments(theta_star * ratio * self.mass_ratios[species], order)
            excess_energy += (2 / 3) * self.fractions[species] * (moments['energy_over_kBT'] - 1.5)
            excess_capacity += (2 / 3) * self.fractions[species] * (moments['cv_over_kB'] - 1.5)
        return dict(A=ratio * (1 + excess_energy), delta_A=ratio * excess_energy,
                    C=1 + excess_capacity, delta_C=excess_capacity, P=2 * ratio / 3)

    def leading_coefficient(self, theta_start, relativistic_ions=False):
        factor = np.dot(self.fractions, self.mass_ratios) if relativistic_ions else self.fractions[0]
        return 1.25 * factor * theta_start


def stress_from_energy_completion(coordinate, delta_A, chi):
    from scipy.interpolate import CubicSpline
    coordinate, delta_A = np.asarray(coordinate), np.asarray(delta_A)
    if coordinate[0] != 0 or np.any(np.diff(coordinate) <= 0):
        raise ValueError('Strictly increasing history starting at zero required')
    energy = CubicSpline(coordinate, delta_A, extrapolate=False)
    primitive = energy.antiderivative()
    density = chi * (delta_A[0] + primitive(coordinate) - primitive(0))
    photon = density - chi * delta_A
    return dict(delta_q=density, delta_p=photon / 3, photon_energy=photon,
                energy_spline=energy, integral_spline=primitive)


def finite_capacity_integral(gas, step):
    gas = np.asarray(gas)
    result = np.zeros_like(gas)
    result[1] = step * gas[1]
    for index in range(2, len(gas)):
        result[index] = (2 * result[index - 1] - .5 * result[index - 2] + step * gas[index]) / 1.5
    return result
