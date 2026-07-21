from __future__ import annotations

from functools import lru_cache

import sympy as sp


def truncate(expression: sp.Expr, velocity: sp.Symbol) -> sp.Expr:
    return sp.series(expression, velocity, 0, 5).removeO().expand()


@lru_cache(maxsize=1)
def surface_identity() -> dict[str, sp.Expr]:
    inverse_radius, theta, velocity = sp.symbols(
        "x theta v", positive=True, real=True
    )
    compactness, ratio = sp.symbols("C r", positive=True, real=True)
    radial_tail_1, angular_tail_1 = sp.symbols(
        "A1 B1", real=True
    )
    radial_tail_3, angular_tail_3 = sp.symbols(
        "A3 B3", real=True
    )
    sine, cosine = sp.sin(theta), sp.cos(theta)
    tail_1 = radial_tail_1 * cosine**2 + angular_tail_1 * sine**2
    tail_3 = radial_tail_3 * cosine**2 + angular_tail_3 * sine**2
    gamma_series = 1 + velocity**2 / 2 + 3 * velocity**4 / 8
    metric = (
        -1 + 2 * compactness * inverse_radius,
        1 + 2 * compactness * inverse_radius,
        inverse_radius**-2,
        sine**2 * inverse_radius**-2,
    )
    inverse_metric = (
        -1 - 2 * compactness * inverse_radius,
        1 - 2 * compactness * inverse_radius,
        inverse_radius**2,
        inverse_radius**2 / sine**2,
    )
    flow = (
        gamma_series
        + inverse_radius
        * (
            compactness * gamma_series
            + velocity**2 * tail_1
            + velocity**4 * (tail_1 / 2 + tail_3)
        ),
        velocity
        * (
            1
            + (radial_tail_1 - compactness) * inverse_radius
            + velocity**2
            * (
                sp.Rational(1, 2)
                + (
                    radial_tail_1 / 2
                    + radial_tail_3
                    - compactness / 2
                )
                * inverse_radius
            )
        )
        * cosine,
        -velocity
        * (
            inverse_radius
            + angular_tail_1 * inverse_radius**2
            + velocity**2
            * (
                inverse_radius / 2
                + (angular_tail_1 / 2 + angular_tail_3)
                * inverse_radius**2
            )
        )
        * sine,
        sp.Integer(0),
    )
    christoffel: dict[tuple[int, int, int], sp.Expr] = {}

    def symmetric(upper: int, first: int, second: int, value: sp.Expr) -> None:
        christoffel[(upper, first, second)] = value
        christoffel[(upper, second, first)] = value

    symmetric(0, 0, 1, compactness * inverse_radius**2)
    christoffel[(1, 0, 0)] = compactness * inverse_radius**2
    christoffel[(1, 1, 1)] = -compactness * inverse_radius**2
    christoffel[(1, 2, 2)] = -1 / inverse_radius + 2 * compactness
    christoffel[(1, 3, 3)] = (
        -1 / inverse_radius + 2 * compactness
    ) * sine**2
    symmetric(2, 1, 2, inverse_radius)
    christoffel[(2, 3, 3)] = -sine * cosine
    symmetric(3, 1, 3, inverse_radius)
    symmetric(3, 2, 3, cosine / sine)

    def coordinate_derivative(expression: sp.Expr, lower: int) -> sp.Expr:
        if lower == 1:
            return -inverse_radius**2 * sp.diff(expression, inverse_radius)
        if lower == 2:
            return sp.diff(expression, theta)
        return sp.Integer(0)

    derivative: list[list[sp.Expr]] = []
    for lower in range(4):
        row: list[sp.Expr] = []
        for upper in range(4):
            value = coordinate_derivative(flow[upper], lower)
            value += sum(
                christoffel.get((upper, lower, contracted), 0)
                * flow[contracted]
                for contracted in range(4)
            )
            row.append(truncate(value, velocity))
        derivative.append(row)
    divergence = truncate(
        sum(derivative[index][index] for index in range(4)), velocity
    )
    acceleration = tuple(
        truncate(
            sum(
                flow[lower] * derivative[lower][upper]
                for lower in range(4)
            ),
            velocity,
        )
        for upper in range(4)
    )
    c_1 = (1 + ratio) / 2
    c_3 = -c_1
    c_2 = sp.Rational(2, 3) / (1 + ratio)
    c_14 = 2 * ratio / (1 + ratio)
    c_4 = c_14 - c_1
    current: list[sp.Expr] = []
    for lower in range(4):
        value = (
            c_1
            * inverse_metric[1]
            * metric[lower]
            * derivative[1][lower]
            + c_3 * derivative[lower][1]
            - c_4
            * flow[1]
            * metric[lower]
            * acceleration[lower]
        )
        if lower == 1:
            value += c_2 * divergence
        current.append(truncate(value, velocity))
    integrand = truncate(
        sum(
            sp.diff(flow[index], velocity) * current[index]
            for index in range(4)
        ),
        velocity,
    )
    surface_density = sp.expand(integrand).coeff(inverse_radius, 2) * sine
    coefficient_density_1 = sp.expand(surface_density).coeff(velocity, 1)
    coefficient_density_3 = sp.expand(surface_density).coeff(velocity, 3)
    coefficient_1 = sp.factor(
        sp.integrate(
            sp.expand_trig(coefficient_density_1), (theta, 0, sp.pi)
        )
    )
    coefficient_3 = sp.factor(
        sp.integrate(
            sp.expand_trig(coefficient_density_3), (theta, 0, sp.pi)
        )
    )
    first_response = sp.factor(-coefficient_1 / (4 * compactness))
    quartic_response = sp.factor(coefficient_3 / (16 * compactness))
    return {
        "surface_coefficient_v": coefficient_1,
        "surface_coefficient_v3": coefficient_3,
        "f_surface": first_response,
        "kappa4_surface": quartic_response,
    }


def main() -> int:
    for key, value in surface_identity().items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
