from __future__ import annotations

from pathlib import Path
import sys
import math
import numpy as np

PARENT = Path(__file__).resolve().parent.parent / "collective-operator-20261003"
sys.path.insert(0, str(PARENT))
from operator_core import Candidate


class WardCandidate:
    def __init__(self, scale=None):
        parent = Candidate()
        self.mass_squared = parent.mass_squared
        self.chemical = parent.chemical
        self.sound = parent.sound
        self.cubics = parent.cubics
        self.amplitude = 10.
        self.scale = scale
        self.radial_cubic = self.cubics[0, 0, 0]
        self.mixed_cubic = self.cubics[0, 1, 1]
        self.phase_quartic_matrix = np.diag([
            (self.radial_cubic - 2 * self.mixed_cubic) / self.amplitude,
            3 * self.mixed_cubic / self.amplitude])

    def regulator(self, squared):
        return np.zeros_like(squared) if self.scale is None else squared**3 / self.scale**4

    def derivative_factor(self, squared):
        return np.ones_like(squared) if self.scale is None else 1 + 3 * squared**2 / self.scale**4

    def propagator(self, frequency, spatial_squared):
        frequency, spatial_squared = np.broadcast_arrays(frequency, spatial_squared)
        squared = frequency**2 + spatial_squared
        shifted = squared + self.regulator(squared)
        determinant = shifted * (shifted + self.mass_squared) + 4 * self.chemical**2 * frequency**2
        output = np.empty(frequency.shape + (2, 2))
        output[..., 0, 0] = shifted / determinant
        output[..., 0, 1] = 2 * self.chemical * frequency / determinant
        output[..., 1, 0] = -output[..., 0, 1]
        output[..., 1, 1] = (shifted + self.mass_squared) / determinant
        return output

    def contract(self, first, second):
        return np.einsum("acd,bef,nce,ndf->nab", self.cubics, self.cubics, first, second, optimize=True)


def ward_slice(model, external_frequency, internal_frequency, momentum, cutoff, order):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    if math.isinf(cutoff):
        if model.scale is None:
            raise ValueError('Infinite slices require the ultraviolet regulator.')
        coordinate = (nodes + 1) / 2
        radial = model.scale * coordinate / (1 - coordinate)
        radial_weights = model.scale * weights / (2 * (1 - coordinate)**2)
    else:
        radial = cutoff * (nodes + 1) / 2
        radial_weights = cutoff * weights / 2
    radius, angle = np.meshgrid(radial, nodes, indexing="ij")
    integration = (radial_weights[:, None] * weights[None, :] * radius**2).ravel()
    radius, angle = radius.ravel(), angle.ravel()
    legendre = (3 * angle**2 - 1) / 2
    transfer_frequency = external_frequency - internal_frequency
    transfer_squared = momentum**2 + radius**2 - 2 * momentum * radius * angle
    first = model.propagator(internal_frequency, radius**2)
    second = model.propagator(transfer_frequency, transfer_squared)
    first_squared = first @ first
    second_squared = second @ second
    first_derivative = model.derivative_factor(internal_frequency**2 + radius**2)
    second_derivative = model.derivative_factor(transfer_frequency**2 + transfer_squared)
    first_shear = radius**2 * legendre
    second_shear = momentum**2 - 2 * momentum * radius * angle + radius**2 * legendre
    radial_derivative = momentum * (momentum - radius * angle)
    first_response = model.contract(first_squared, second)
    second_response = model.contract(first, second_squared)

    def integrate(values, coefficient):
        return np.einsum("n,n,nab->ab", integration, coefficient, values, optimize=True) / (8 * math.pi**3)

    first_half = integrate(first_response, first_shear * first_derivative / 2)
    second_half = integrate(second_response, second_shear * second_derivative / 2)
    direct_derivative = integrate(second_response, radial_derivative * second_derivative / 2)
    if math.isinf(cutoff):
        boundary = np.zeros((2, 2))
    else:
        surface_angle = nodes
        surface_transfer = momentum**2 + cutoff**2 - 2 * momentum * cutoff * surface_angle
        surface_first = model.propagator(np.full(order, internal_frequency), np.full(order, cutoff**2))
        surface_second = model.propagator(np.full(order, transfer_frequency), surface_transfer)
        boundary = (cutoff**3 / 4) * np.einsum("n,n,nab->ab", weights, (3 * nodes**2 - 1) / 2,
                                              model.contract(surface_first, surface_second), optimize=True) / (8 * math.pi**3)
    return {"first_leg_half": first_half, "second_leg_half": second_half,
            "direct_spatial_derivative": direct_derivative, "boundary": boundary,
            "completed_vertex": first_half + second_half + boundary,
            "collapsed_parent_vertex": 2 * first_half,
            "routing_correction": second_half - first_half}


def tadpole_integrals(model, order):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    coordinate = (nodes + 1) / 2
    scale = model.scale
    radius = scale * coordinate / (1 - coordinate)
    radial_weights = weights * scale / (2 * (1 - coordinate)**2)
    angle = (nodes + 1) * math.pi / 4
    angular_weights = weights * math.pi / 4
    radius_grid, angle_grid = np.meshgrid(radius, angle, indexing="ij")
    frequency = (radius_grid * np.cos(angle_grid)).ravel()
    momentum_squared = (radius_grid * np.sin(angle_grid)).ravel()**2
    measure = (radial_weights[:, None] * angular_weights[None, :] * radius_grid**3 * np.sin(angle_grid)**2).ravel() / (2 * math.pi**3)
    propagator = model.propagator(frequency, momentum_squared)
    radial_vertex = model.cubics[0]
    phase_vertex = model.cubics[1]
    tadpole = .5 * np.einsum("n,ab,nba->", measure, radial_vertex, propagator, optimize=True)
    phase_tadpole = .5 * np.einsum("n,ab,nba->", measure, model.phase_quartic_matrix, propagator, optimize=True)
    phase_bubble = -.5 * np.einsum("n,nab,bc,ncd,da->", measure, propagator, phase_vertex, propagator, phase_vertex, optimize=True)
    phase_self_energy = phase_tadpole + phase_bubble
    shift = -tadpole / model.mass_squared
    return {"tadpole": float(tadpole), "phase_quartic_tadpole": float(phase_tadpole),
            "phase_cubic_bubble": float(phase_bubble), "phase_self_energy": float(phase_self_energy),
            "tadpole_over_amplitude": float(tadpole / model.amplitude),
            "background_shift": float(shift), "relative_background_shift": float(shift / model.amplitude),
            "phase_mass_after_background_shift": float(phase_self_energy + model.mixed_cubic * shift)}
