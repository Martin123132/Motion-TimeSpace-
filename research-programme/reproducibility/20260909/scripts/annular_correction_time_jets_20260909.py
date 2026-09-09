import math

import numpy as numerical
from numpy.polynomial import Polynomial
from scipy.linalg import solve_banded

from annular_coordinate_evolution_operator_20260909 import coefficients, local_jacobians
from annular_noether_completion_20260909 import constraint_coefficients, derivative_band
from annular_noether_source_projection_20260909 import transpose_band
from sbp4_compatible_second_operator_20260909 import norm_weights, surface_derivative, gram_parts
from sbp4_derived_operator_20260909 import derivative


ORDER = 2


def constant(values):
    result = numerical.zeros((ORDER + 1,) + numerical.shape(values))
    result[0] = values
    return result


def multiply(first, second):
    return numerical.stack([sum(first[index] * second[degree - index] for index in range(degree + 1)) for degree in range(ORDER + 1)])


def divide(first, second):
    values = [first[0] / second[0]]
    for degree in range(1, ORDER + 1):
        values.append((first[degree] - sum(second[index] * values[degree - index] for index in range(1, degree + 1))) / second[0])
    return numerical.stack(values)


class CorrectionTimeJets:
    def __init__(self, evaluator, radii, initial, initial_radial, initial_second, time, side="left", strength=1 / 64):
        self.evaluator, self.radii, self.time = evaluator, radii, time
        self.initial, self.initial_radial, self.initial_second = initial, initial_radial, initial_second
        self.spacing = float(radii[1] - radii[0])
        self.norm = norm_weights(radii.size)
        self.strength = strength
        self.band = derivative_band(radii.size, self.spacing)
        self.outer = derivative(numerical.eye(radii.size), self.spacing).T[-1]
        coordinate = time * 640
        cell = int(round(coordinate)) - (1 if side == "left" else 0)
        self.first = max(0, min(187, cell - 2))
        self.nodes = numerical.arange(self.first, self.first + 6)
        times = self.nodes / 640
        snapshot = evaluator.evaluate(times[:, None], radii[None, :], 0.1)
        base, spatial, second = [snapshot[key][0] for key in ["state", "state_space", "state_second"]]
        matrices = local_jacobians(base, spatial, second, radii[None, :], evaluator.constants, evaluator.kappa, evaluator.sigma)
        self.samples = {key: numerical.moveaxis(matrix, 2, 0) for key, matrix in zip(["A", "B", "C"], matrices)}
        forcing = sum(numerical.einsum("ijtn,bjn->bitn", matrix, argument) for matrix, argument in zip(matrices, [initial, initial_radial, initial_second])) - snapshot["defect"]
        self.samples["forcing"] = numerical.moveaxis(forcing, 2, 0)
        self.samples["constraint"] = numerical.moveaxis(constraint_coefficients(base, spatial, radii[None, :], evaluator), 1, 0)
        data = coefficients(base, spatial, radii[None, :], evaluator.constants, evaluator.kappa, evaluator.sigma)
        acoustic = numerical.sqrt(data["b"]**2 - data["a"] * data["c"])
        self.samples["boundary"] = numerical.stack([evaluator.sigma - data["a"][:, 0] / (data["b"][:, 0] + acoustic[:, 0]), evaluator.sigma + (-data["b"][:, -1] - acoustic[:, -1]) / data["c"][:, -1]], axis=-1)
        varied_spatial = spatial.astype(complex)
        varied_spatial[0] += 1j * 1e-30 * second[0]
        radial_data = coefficients(base.astype(complex) + 1j * 1e-30 * spatial, varied_spatial, radii[None, :].astype(complex) + 1j * 1e-30, evaluator.constants, evaluator.kappa, evaluator.sigma)
        self.samples["flux_coefficient"] = data["c"]
        self.samples["flux_radial"] = radial_data["c"].imag / 1e-30
        self.samples["energy_time"] = -data["at"]
        self.polynomials = []
        for position, node in enumerate(self.nodes):
            polynomial = Polynomial([1.0])
            for other in self.nodes:
                if node != other:
                    polynomial *= Polynomial([coordinate - other, 640]) / (node - other)
            self.polynomials.append(polynomial)
        self.current = self.interpolate(0)
        if numerical.min(self.current["energy_time"][0]) <= 0 or numerical.min(self.current["flux_coefficient"][0]) <= 0:
            raise ValueError("Unqualified time-jet background")
        self.base_gram = gram_parts(radii.size, numerical.ones(radii.size))

    def interpolate(self, offset):
        weights = numerical.array([[polynomial.deriv(degree)(offset) / math.factorial(degree) for polynomial in self.polynomials] for degree in range(ORDER + 1)])
        result = {}
        for key, values in self.samples.items():
            interpolated = numerical.tensordot(weights, values - values[0], axes=(1, 0))
            interpolated[0] += values[0]
            result[key] = interpolated
        return result

    def signed_flux(self, values, coefficient):
        count, size = self.radii.size, self.radii.size - 3
        margins, adjacent, extras = self.base_gram
        centers = numerical.arange(size) + 1.5
        diagonal = margins * numerical.interp(centers, numerical.arange(count), coefficient)
        edge_values = numerical.interp(numerical.arange(size - 1) + 2.0, numerical.arange(count), coefficient)
        diagonal[:-1] += numerical.abs(adjacent) * edge_values
        diagonal[1:] += numerical.abs(adjacent) * edge_values
        off_diagonal = adjacent * edge_values
        difference = numerical.diff(values, n=3, axis=-1)
        weighted = diagonal * difference
        weighted[..., :-1] += off_diagonal * difference[..., 1:]
        weighted[..., 1:] += off_diagonal * difference[..., :-1]
        for first, second, weight in extras:
            sample = float(numerical.interp((first + second) / 2 + 1.5, numerical.arange(count), coefficient))
            weighted[..., first] += sample * (abs(weight) * difference[..., first] + weight * difference[..., second])
            weighted[..., second] += sample * (weight * difference[..., first] + abs(weight) * difference[..., second])
        remainder = numerical.zeros_like(values)
        for offset, coefficient_value in enumerate([-1, 3, -3, 1]):
            remainder[..., offset:offset + size] += coefficient_value * weighted
        gradient = derivative(values, self.spacing)
        result = derivative(coefficient * gradient, self.spacing) - remainder / (self.spacing**2 * self.norm)
        surface = surface_derivative(values, self.spacing) - gradient[..., [0, -1]]
        result[..., 0] -= coefficient[0] * surface[..., 0] / (self.spacing * self.norm[0])
        result[..., -1] += coefficient[-1] * surface[..., -1] / (self.spacing * self.norm[-1])
        return result

    def anchored_solve(self, gradient, forcing, transpose=False):
        matrix = self.band.copy()
        matrix[3] -= gradient[0, 2]
        matrix[3, -1] = 1
        if transpose:
            matrix = transpose_band(matrix)
        result = numerical.zeros_like(forcing)
        for degree in range(ORDER + 1):
            value = forcing[degree].copy()
            for index in range(1, degree + 1):
                diagonal = gradient[index, 2].copy()
                diagonal[-1] = 0
                value += diagonal * result[degree - index]
            result[degree] = solve_banded((3, 3), matrix, value.T, check_finite=False).T
        return result

    def rhs(self, current, values):
        radial = derivative(values, self.spacing)
        second = numerical.zeros_like(values)
        second[:, :, 0] = derivative(radial[:, :, 0], self.spacing)
        output = current["forcing"].copy()
        for degree in range(ORDER + 1):
            for index in range(degree + 1):
                for key, argument in zip(["A", "B", "C"], [values, radial, second]):
                    output[degree] += numerical.einsum("ijn,bjn->bin", current[key][index], argument[degree - index])
        selected = values[:, :, [1, 2, 3]]
        difference = numerical.diff(selected, n=3, axis=-1)
        adjoint = numerical.zeros_like(selected)
        for offset, coefficient in enumerate([-1, 3, -3, 1]):
            adjoint[..., offset:offset + difference.shape[-1]] += coefficient * difference
        sources = numerical.zeros_like(values)
        sources[:, :, [1, 2, 3]] = -self.strength * adjoint / (self.spacing * self.norm)
        sources[:, :, 1] = divide(sources[:, :, 1], current["energy_time"])
        flux = numerical.stack([sum(self.signed_flux(values[degree - index, :, 0], current["flux_coefficient"][index]) for index in range(degree + 1)) for degree in range(ORDER + 1)])
        replacement = flux - multiply(current["flux_coefficient"], second[:, :, 0]) - multiply(current["flux_radial"], radial[:, :, 0])
        sources[:, :, 1] += divide(replacement, current["energy_time"])
        surface = surface_derivative(values[:, :, 0], self.spacing)
        surface[0] += self.initial_radial[:, 0][:, [0, -1]]
        for endpoint, side, orientation in [(0, 0, 1), (-1, 1, -1)]:
            boundary = current["boundary"][:, side, None]
            residual = surface[:, :, endpoint] - multiply(boundary, values[:, :, 1, endpoint])
            sources[:, :, 1, endpoint] += orientation * multiply(current["C"][:, 1, 0, endpoint, None], residual) / (self.spacing * self.norm[endpoint])
        lapse = values[:, :, 3, -1].copy()
        lapse[0] += self.initial[:, 3, -1]
        sources[:, :, 3, -1] -= lapse / (self.evaluator.sigma * self.spacing * self.norm[-1])
        gradient = current["constraint"]
        normal_rhs = numerical.zeros((ORDER + 1, self.radii.size))
        normal_rhs[0] = self.outer
        normal_rhs[:, -1] -= gradient[:, 2, -1]
        normal = self.anchored_solve(gradient, normal_rhs, transpose=True)
        normal[:, -1] = 0
        normal[0, -1] = -1
        covector = multiply(normal, gradient[:, 1])
        covector[:, [0, -1]] = 0
        weight = current["energy_time"] * (self.spacing * self.norm)
        denominator = numerical.sum(divide(multiply(covector, covector), weight), axis=-1)
        if denominator[0] <= 0:
            raise ValueError("Time-jet projection crosses a singular restricted denominator")
        forcing = multiply(gradient[:, 1], sources[:, :, 1]) + multiply(gradient[:, 3], sources[:, :, 3])
        mismatch = numerical.sum(multiply(normal, forcing), axis=-1)
        amplitude = divide(mismatch, denominator[:, None])
        sources[:, :, 1] -= multiply(amplitude[:, :, None], divide(covector, weight))
        forcing = multiply(gradient[:, 1], sources[:, :, 1]) + multiply(gradient[:, 3], sources[:, :, 3])
        forcing[:, :, -1] = 0
        sources[:, :, 2] = self.anchored_solve(gradient, forcing)
        return output + sources, sources

    def time_derivatives(self, remainder):
        values = numerical.zeros((ORDER + 2,) + remainder.shape)
        values[0] = remainder
        for degree in range(ORDER + 1):
            rhs, unused_sources = self.rhs(self.current, values[:ORDER + 1])
            values[degree + 1] = rhs[degree] / (degree + 1)
        return numerical.stack([math.factorial(degree) * value for degree, value in enumerate(values)])

    def evaluate_rhs(self, offset, remainder):
        return self.rhs(self.interpolate(offset), constant(remainder))[0][0]
