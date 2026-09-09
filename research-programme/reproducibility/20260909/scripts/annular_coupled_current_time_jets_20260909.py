import math

import numpy as numerical
from numpy.polynomial import Polynomial
from scipy.linalg import solve_banded

from annular_correction_time_jets_20260909 import constant, divide, multiply
from annular_coupled_current_operator_20260909 import snapshot_coefficients
from annular_noether_completion_20260909 import derivative_band
from annular_noether_source_projection_20260909 import transpose_band
from sbp4_compatible_second_operator_20260909 import norm_weights
from sbp4_derived_operator_20260909 import derivative


def series_dot(coefficient, values):
    return numerical.sum(multiply(coefficient, values), axis=1)


def square_root(values):
    leading = numerical.sqrt(values[0])
    first = values[1] / (2 * leading)
    second = (values[2] - first**2) / (2 * leading)
    return numerical.stack([leading, first, second])


class CoupledCurrentTimeJets:
    def __init__(self, evaluator, radii, time, side="left"):
        if side not in {"left", "right"}:
            raise ValueError("Unknown interpolation side")
        self.evaluator, self.radii, self.time = evaluator, radii, time
        self.spacing = float(radii[1] - radii[0])
        self.weights = self.spacing * norm_weights(radii.size)
        self.band = derivative_band(radii.size, self.spacing)
        self.outer = derivative(numerical.eye(radii.size), self.spacing).T[-1]
        coordinate = time * 640
        if abs(coordinate - round(coordinate)) > 1e-10:
            raise ValueError("This replay requires an output cache node")
        cell = int(round(coordinate)) - (1 if side == "left" else 0)
        self.first = max(0, min(187, cell - 2))
        self.nodes = numerical.arange(self.first, self.first + 6)
        times = numerical.linspace(0, 0.3, 193)[self.nodes]
        snapshot = evaluator.evaluate(times[:, None], radii[None, :], 0.1)
        data = snapshot_coefficients(snapshot, radii[None, :], evaluator)
        data["defect"] = data["independent_defect"]
        data["J0"] = snapshot["initial_constraint"][0]
        keys = ["background", "defect", "J0", "old_gradient", "q_gradient", "flux_gradient", "C_gradient", "D_gradient", "V_gradient", "fmu_gradient", "constraint_gradient", "alpha", "B", "c", "P", "Q", "f_mu", "h_mu", "h_delta", "q0", "E"]
        self.samples = {key: numerical.moveaxis(data[key], -2, 0) for key in keys}
        self.polynomials = []
        for node in self.nodes:
            polynomial = Polynomial([1.0])
            for other in self.nodes:
                if node != other:
                    polynomial *= Polynomial([coordinate - other, 640]) / (node - other)
            self.polynomials.append(polynomial)
        self.current = self.interpolate(0)
        if min(numerical.min(self.current[key][0]) for key in ["alpha", "P", "Q"]) <= 0:
            raise ValueError("Unqualified current time-jet background")

    def interpolate(self, offset):
        weights = numerical.array([[polynomial.deriv(degree)(offset) / math.factorial(degree) for polynomial in self.polynomials] for degree in range(3)])
        result = {}
        for key, values in self.samples.items():
            result[key] = numerical.tensordot(weights, values - values[0], axes=(1, 0))
            result[key][0] += values[0]
        return result

    def anchored_solve(self, gradient, forcing, transpose=False):
        matrix = self.band.copy()
        matrix[3] -= gradient[0, 2]
        matrix[3, -1] = 1
        if transpose:
            matrix = transpose_band(matrix)
        result = numerical.zeros_like(forcing)
        for degree in range(3):
            value = forcing[degree].copy()
            for index in range(1, degree + 1):
                diagonal = gradient[index, 2].copy()
                diagonal[-1] = 0
                value += diagonal * result[degree - index]
            result[degree] = solve_banded((3, 3), matrix, value, check_finite=False)
        return result

    def numerical_source(self, current, values, velocity):
        fixed_velocity = velocity - multiply(current["q0"], values[:, 4])
        fixed_gradient = values[:, 1] - self.evaluator.sigma * multiply(current["q0"], values[:, 4])
        flux = multiply(current["B"], fixed_velocity) + multiply(current["c"], fixed_gradient)
        impedance = square_root(multiply(current["P"], current["Q"]))
        raw = numerical.zeros((3, 4, self.radii.size))
        for endpoint, orientation in [(0, 1), (-1, -1)]:
            raw[:, 1, endpoint] = divide(orientation * flux[:, endpoint] - multiply(impedance, fixed_velocity)[:, endpoint], current["alpha"][:, endpoint]) / self.weights[endpoint]
        raw[:, 3, -1] = -values[:, 4, -1] / (self.evaluator.sigma * self.weights[-1])
        gradient = current["old_gradient"]
        normal_rhs = numerical.zeros((3, self.radii.size))
        normal_rhs[0] = self.outer
        normal_rhs[:, -1] -= gradient[:, 2, -1]
        normal = self.anchored_solve(gradient, normal_rhs, transpose=True)
        normal[:, -1] = 0
        normal[0, -1] = -1
        covector = multiply(normal, gradient[:, 1])
        covector[:, [0, -1]] = 0
        weight = current["alpha"] * (self.weights * self.radii**2)
        denominator = numerical.sum(divide(multiply(covector, covector), weight), axis=-1)
        if denominator[0] <= 0 or not numerical.all(numerical.isfinite(denominator)):
            raise ValueError("Singular boundary-fixed projection in time-jet branch")
        forcing = multiply(gradient[:, 1], raw[:, 1]) + multiply(gradient[:, 3], raw[:, 3])
        mismatch = numerical.sum(multiply(normal, forcing), axis=-1)
        amplitude = divide(mismatch, denominator)
        complete = raw.copy()
        complete[:, 1] -= multiply(amplitude[:, None], divide(covector, weight))
        forcing = multiply(gradient[:, 1], complete[:, 1]) + multiply(gradient[:, 3], complete[:, 3])
        forcing[:, -1] = 0
        complete[:, 2] = self.anchored_solve(gradient, forcing)
        transformed = numerical.stack([complete[:, 0], numerical.zeros_like(velocity), multiply(current["alpha"], complete[:, 1]) + multiply(current["h_mu"], complete[:, 2]) + multiply(current["h_delta"], complete[:, 3]), complete[:, 2], complete[:, 3]], axis=1)
        return transformed, complete, raw

    def rhs(self, current, values):
        velocity = series_dot(current["q_gradient"], values)
        flux = series_dot(current["flux_gradient"], values)
        constraint = derivative(values[:, 3], self.spacing) - series_dot(current["constraint_gradient"], values)
        force = -multiply(current["f_mu"], constraint) - multiply(series_dot(current["fmu_gradient"], values), current["J0"])
        output = numerical.stack([velocity, derivative(velocity, self.spacing), derivative(self.radii**2 * flux, self.spacing) / self.radii**2 - series_dot(current["V_gradient"], values) + force, series_dot(current["C_gradient"], values), (derivative(values[:, 4], self.spacing) - series_dot(current["D_gradient"], values)) / self.evaluator.sigma], axis=1) - current["defect"]
        sources, coordinate, raw = self.numerical_source(current, values, velocity)
        return output + sources, sources, coordinate, raw

    def time_derivatives(self, correction):
        values = numerical.zeros((4,) + correction.shape)
        values[0] = correction
        for degree in range(3):
            output = self.rhs(self.current, values[:3])[0]
            values[degree + 1] = output[degree] / (degree + 1)
        return numerical.stack([math.factorial(degree) * value for degree, value in enumerate(values)])

    def evaluate_rhs(self, offset, correction):
        return self.rhs(self.interpolate(offset), constant(correction))[0][0]
