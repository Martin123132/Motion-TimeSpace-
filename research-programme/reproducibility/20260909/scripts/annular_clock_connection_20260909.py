import math

import numpy as numerical

from annular_gram_joint_action_20260909 import gram_matrices


def clock_offsets(coefficient, clock):
    factors, sampling = gram_matrices(coefficient.size)
    factor_coefficient = sampling @ coefficient
    if numerical.any(numerical.real(factor_coefficient) <= 0):
        raise ValueError("Positive leading Gram coefficient required")
    allocation = sampling * coefficient[None, :] / factor_coefficient[:, None]
    centers = allocation @ clock
    return clock[None, :] - centers[:, None], factor_coefficient, allocation


def quadratic_clock_potential(scalar, velocity, acceleration, coefficient, clock, spacing):
    factors, sampling = gram_matrices(scalar.size)
    offsets, factor_coefficient, allocation = clock_offsets(coefficient, clock)
    leading = factors @ scalar
    first = -numerical.sum(factors * offsets * velocity[None, :], axis=1)
    second = numerical.sum(factors * offsets**2 * acceleration[None, :], axis=1) / 2
    return numerical.sum(factor_coefficient * (leading**2 + 2 * leading * first + first**2 + 2 * leading * second)) / (2 * spacing)


def clock_hessian(scalar, velocity, acceleration, coefficient, first_clock, second_clock, spacing):
    factors, sampling = gram_matrices(scalar.size)
    first_offsets, factor_coefficient, allocation = clock_offsets(coefficient, first_clock)
    second_offsets, unused_coefficient, unused_allocation = clock_offsets(coefficient, second_clock)
    first = -numerical.sum(factors * first_offsets * velocity[None, :], axis=1)
    second = -numerical.sum(factors * second_offsets * velocity[None, :], axis=1)
    mixed = numerical.sum(factors * first_offsets * second_offsets * acceleration[None, :], axis=1)
    return numerical.sum(factor_coefficient * (first * second + (factors @ scalar) * mixed)) / spacing


def graph_flux(scalar, velocity, coefficient, spacing):
    factors, sampling = gram_matrices(scalar.size)
    directed = ((factors.T * ((factors @ scalar) / spacing)) @ sampling) * velocity[:, None] * coefficient[None, :]
    graph = directed - directed.T
    faces = numerical.array([0.] + [graph[:cut, cut:].sum() for cut in range(1, scalar.size)] + [0.])
    return graph, faces


def clock_from_connection(connection, edge_lengths):
    return numerical.concatenate((numerical.zeros(1, dtype=connection.dtype), numerical.cumsum(edge_lengths * connection)))


def exact_clock_potential(profile, time_value, radii, coefficient, clock, spacing):
    factors, sampling = gram_matrices(radii.size)
    offsets, factor_coefficient, allocation = clock_offsets(coefficient, clock)
    delayed = profile.evaluate(time_value - offsets, radii[None, :], 0)
    values = numerical.sum(factors * delayed, axis=1)
    return numerical.sum(factor_coefficient * values**2) / (2 * spacing)


def clock_remainder_bound(profile, time_value, radii, coefficient, clock, spacing):
    factors, sampling = gram_matrices(radii.size)
    offsets, factor_coefficient, allocation = clock_offsets(coefficient, clock)
    if numerical.iscomplexobj(offsets) or numerical.iscomplexobj(coefficient):
        raise ValueError("Real paths required for the analytic remainder bound")
    scalar, velocity, acceleration = [profile.evaluate(time_value, radii, order) for order in range(3)]
    support = factors != 0
    radii_offsets = numerical.max(numerical.abs(offsets) * support, axis=0)
    third_bound = profile.third_derivative_bound(time_value, radii, radii_offsets)
    leading = factors @ scalar
    first = -numerical.sum(factors * offsets * velocity[None, :], axis=1)
    second = numerical.sum(factors * offsets**2 * acceleration[None, :], axis=1) / 2
    remainder = numerical.sum(numerical.abs(factors) * numerical.abs(offsets)**3 * third_bound[None, :], axis=1) / 6
    bound = numerical.sum(factor_coefficient * (2 * numerical.abs(first * second) + second**2 + 2 * numerical.abs(leading + first + second) * remainder + remainder**2)) / (2 * spacing)
    absolute_roundoff_scale = numerical.sum(factor_coefficient * (numerical.sum(numerical.abs(factors) * (numerical.abs(scalar)[None, :] + numerical.abs(offsets * velocity[None, :]) + numerical.abs(offsets**2 * acceleration[None, :]) / 2), axis=1))**2) / (2 * spacing)
    return float(bound), float(absolute_roundoff_scale), float(numerical.max(radii_offsets))


class ScalarReferenceClockProfile:
    def __init__(self, case, epsilon=0.1, sigma=0.05):
        import sympy as symbolic

        advanced, radius = symbolic.symbols("v r", real=True)
        self.epsilon, self.sigma = epsilon, sigma
        self.domain = case["domain"]["v"]
        expression = symbolic.S.Zero
        self.bound_terms = []
        for order, harmonics in case["fields"]["scalar_ref"].items():
            for key, coefficient in harmonics.items():
                kind, mode = key[:3], int(key[3:])
                if kind not in {"cos", "sin"}:
                    raise ValueError("Unsupported reference harmonic")
                amplitude = symbolic.sympify(coefficient, locals={"v": advanced, "r": radius})
                phase = mode * advanced / symbolic.Rational(str(epsilon))
                trigonometric = symbolic.cos(phase) if kind == "cos" else symbolic.sin(phase)
                prefactor = symbolic.Rational(str(epsilon))**int(order)
                expression += prefactor * amplitude * trigonometric
                for differentiated in range(4):
                    polynomial = symbolic.Poly(symbolic.diff(prefactor * amplitude, advanced, differentiated), advanced)
                    factor = math.comb(3, differentiated) * (mode / epsilon)**(3 - differentiated)
                    for powers, value in polynomial.terms():
                        self.bound_terms.append((factor, powers[0], symbolic.lambdify(radius, value, "numpy", cse=True, docstring_limit=0)))
        self.functions = [symbolic.lambdify((advanced, radius), symbolic.diff(expression, advanced, order), "numpy", cse=True, docstring_limit=0) for order in range(4)]

    def evaluate(self, time_value, radii, order=0):
        advanced = time_value + self.sigma * (radii - 4)
        return self.functions[order](advanced, radii)

    def third_derivative_bound(self, time_value, radii, offsets):
        advanced = time_value + self.sigma * (radii - 4)
        if numerical.min(advanced - offsets) < self.domain[0] or numerical.max(advanced + offsets) > self.domain[1]:
            raise ValueError("Clock shifts leave the owned reference domain")
        maximum_time = numerical.abs(advanced) + offsets
        bound = numerical.zeros_like(radii)
        for factor, degree, evaluator in self.bound_terms:
            bound += factor * numerical.abs(evaluator(radii)) * maximum_time**degree
        return bound
