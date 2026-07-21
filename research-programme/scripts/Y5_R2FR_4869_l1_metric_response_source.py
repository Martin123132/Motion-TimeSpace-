from __future__ import annotations

from functools import lru_cache

import sympy as sp


Order = tuple[int, int]
Polynomial = dict[Order, sp.Expr]


def add(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = {}
    for polynomial in polynomials:
        for order, value in polynomial.items():
            result[order] = result.get(order, 0) + value
    return {order: value for order, value in result.items() if value != 0}


def scale(polynomial: Polynomial, coefficient: sp.Expr) -> Polynomial:
    return {
        order: coefficient * value
        for order, value in polynomial.items()
        if value != 0
    }


def multiply(*polynomials: Polynomial) -> Polynomial:
    result: Polynomial = {(0, 0): sp.Integer(1)}
    for polynomial in polynomials:
        product: Polynomial = {}
        for (left_shift, left_velocity), left_value in result.items():
            for (right_shift, right_velocity), right_value in polynomial.items():
                order = (left_shift + right_shift, left_velocity + right_velocity)
                if order[0] <= 1 and order[1] <= 1:
                    product[order] = product.get(order, 0) + left_value * right_value
        result = product
    return {order: value for order, value in result.items() if value != 0}


def differentiate(polynomial: Polynomial, variable: sp.Symbol) -> Polynomial:
    return {
        order: sp.diff(value, variable)
        for order, value in polynomial.items()
        if value != 0
    }


@lru_cache(maxsize=1)
def reduced_shift_flow_cross_lagrangian() -> tuple[sp.Expr, tuple[sp.Symbol, ...]]:
    time, radius, theta, phi = sp.symbols("t R theta phi", real=True)
    ratio = sp.symbols("r", positive=True, real=True)
    lapse = sp.Function("N")(radius)
    radial_metric = sp.Function("A")(radius)
    radial_flow = sp.Function("a")(radius)
    angular_flow = sp.Function("b")(radius)
    radial_shift = sp.Function("k")(radius)
    angular_shift = sp.Function("s")(radius)
    coordinates = (time, radius, theta, phi)
    sine = sp.sin(theta)
    cosine = sp.cos(theta)

    metric: list[list[Polynomial]] = [
        [dict() for _ in range(4)] for _ in range(4)
    ]
    inverse_metric: list[list[Polynomial]] = [
        [dict() for _ in range(4)] for _ in range(4)
    ]
    metric[0][0] = {(0, 0): -lapse**2}
    metric[1][1] = {(0, 0): radial_metric**2}
    metric[2][2] = {(0, 0): radius**2}
    metric[3][3] = {(0, 0): radius**2 * sine**2}
    metric[0][1] = metric[1][0] = {(1, 0): radial_shift * cosine}
    metric[0][2] = metric[2][0] = {
        (1, 0): -radius * angular_shift * sine
    }
    inverse_metric[0][0] = {(0, 0): -1 / lapse**2}
    inverse_metric[1][1] = {(0, 0): 1 / radial_metric**2}
    inverse_metric[2][2] = {(0, 0): 1 / radius**2}
    inverse_metric[3][3] = {(0, 0): 1 / (radius**2 * sine**2)}
    inverse_metric[0][1] = inverse_metric[1][0] = {
        (1, 0): radial_shift * cosine / (lapse**2 * radial_metric**2)
    }
    inverse_metric[0][2] = inverse_metric[2][0] = {
        (1, 0): -angular_shift * sine / (lapse**2 * radius)
    }

    christoffel: dict[tuple[int, int, int], Polynomial] = {}
    for upper in range(4):
        for first in range(4):
            for second in range(4):
                terms: list[Polynomial] = []
                for contracted in range(4):
                    derivative = add(
                        differentiate(metric[contracted][second], coordinates[first]),
                        differentiate(metric[contracted][first], coordinates[second]),
                        scale(
                            differentiate(metric[first][second], coordinates[contracted]),
                            -1,
                        ),
                    )
                    terms.append(
                        scale(
                            multiply(inverse_metric[upper][contracted], derivative),
                            sp.Rational(1, 2),
                        )
                    )
                value = add(*terms)
                if value:
                    christoffel[(upper, first, second)] = value

    contravariant_flow: list[Polynomial] = [
        {(0, 0): 1 / lapse},
        {
            (1, 0): -radial_shift * cosine / (lapse * radial_metric**2),
            (0, 1): radial_flow * cosine / radial_metric,
        },
        {
            (1, 0): angular_shift * sine / (lapse * radius),
            (0, 1): -angular_flow * sine / radius,
        },
        {},
    ]
    covariant_flow: list[Polynomial] = []
    for first in range(4):
        covariant_flow.append(
            add(
                *(
                    multiply(metric[first][second], contravariant_flow[second])
                    for second in range(4)
                )
            )
        )

    covariant_derivative: list[list[Polynomial]] = []
    for derivative_index in range(4):
        row: list[Polynomial] = []
        for vector_index in range(4):
            terms = [
                differentiate(
                    covariant_flow[vector_index], coordinates[derivative_index]
                )
            ]
            terms.extend(
                scale(
                    multiply(
                        christoffel[(contracted, derivative_index, vector_index)],
                        covariant_flow[contracted],
                    ),
                    -1,
                )
                for contracted in range(4)
                if (contracted, derivative_index, vector_index) in christoffel
            )
            row.append(add(*terms))
        covariant_derivative.append(row)

    invariant_1: Polynomial = {}
    invariant_3: Polynomial = {}
    for first in range(4):
        for second in range(4):
            for raised_first in range(4):
                for raised_second in range(4):
                    weight = multiply(
                        inverse_metric[first][raised_first],
                        inverse_metric[second][raised_second],
                    )
                    invariant_1 = add(
                        invariant_1,
                        multiply(
                            weight,
                            covariant_derivative[first][second],
                            covariant_derivative[raised_first][raised_second],
                        ),
                    )
                    invariant_3 = add(
                        invariant_3,
                        multiply(
                            weight,
                            covariant_derivative[first][second],
                            covariant_derivative[raised_second][raised_first],
                        ),
                    )

    expansion: Polynomial = {}
    for index in range(4):
        expansion = add(
            expansion,
            differentiate(contravariant_flow[index], coordinates[index]),
        )
        for contracted in range(4):
            if (index, index, contracted) in christoffel:
                expansion = add(
                    expansion,
                    multiply(
                        christoffel[(index, index, contracted)],
                        contravariant_flow[contracted],
                    ),
                )
    invariant_2 = multiply(expansion, expansion)

    acceleration: list[Polynomial] = []
    for vector_index in range(4):
        acceleration.append(
            add(
                *(
                    multiply(
                        contravariant_flow[derivative_index],
                        covariant_derivative[derivative_index][vector_index],
                    )
                    for derivative_index in range(4)
                )
            )
        )
    invariant_4: Polynomial = {}
    for first in range(4):
        for second in range(4):
            invariant_4 = add(
                invariant_4,
                multiply(
                    inverse_metric[first][second],
                    acceleration[first],
                    acceleration[second],
                ),
            )

    c_1 = (1 + ratio) / 2
    c_3 = -c_1
    c_2 = sp.Rational(2, 3) / (1 + ratio)
    c_14 = 2 * ratio / (1 + ratio)
    c_4 = c_14 - c_1
    kinetic = add(
        scale(invariant_1, c_1),
        scale(invariant_2, c_2),
        scale(invariant_3, c_3),
        scale(invariant_4, -c_4),
    )
    measure = 2 * sp.pi * lapse * radial_metric * radius**2 * sine
    cross_density = kinetic.get((1, 1), 0)
    lagrangian = sp.factor(
        sp.integrate(
            sp.expand_trig(sp.expand(measure * cross_density)),
            (theta, 0, sp.pi),
        )
    )
    lapse_value, radial_metric_value, lapse_prime, radial_metric_prime = sp.symbols(
        "N_value A_value N_prime A_prime", positive=True, real=True
    )
    values = sp.symbols("a_value b_value k_value s_value", real=True)
    derivatives = sp.symbols("a_prime b_prime k_prime s_prime", real=True)
    substitutions = [
        (sp.diff(lapse, radius), lapse_prime),
        (sp.diff(radial_metric, radius), radial_metric_prime),
        (sp.diff(radial_flow, radius), derivatives[0]),
        (sp.diff(angular_flow, radius), derivatives[1]),
        (sp.diff(radial_shift, radius), derivatives[2]),
        (sp.diff(angular_shift, radius), derivatives[3]),
        (lapse, lapse_value),
        (radial_metric, radial_metric_value),
        (radial_flow, values[0]),
        (angular_flow, values[1]),
        (radial_shift, values[2]),
        (angular_shift, values[3]),
    ]
    arguments = (
        radius,
        ratio,
        lapse_value,
        radial_metric_value,
        lapse_prime,
        radial_metric_prime,
        *values,
        *derivatives,
    )
    return sp.factor(lagrangian.subs(substitutions)), arguments


@lru_cache(maxsize=1)
def reduced_gr_matter_shift_lagrangian() -> tuple[
    sp.Expr, sp.Expr, tuple[sp.Symbol, ...]
]:
    radius, theta, phi = sp.symbols("R theta phi", positive=True, real=True)
    lapse = sp.Function("N")(radius)
    radial_metric = sp.Function("A")(radius)
    radial_shift = sp.Function("k")(radius)
    angular_shift = sp.Function("s")(radius)
    density = sp.Function("rho")(radius)
    pressure = sp.Function("P")(radius)
    coordinates = (radius, theta, phi)
    sine = sp.sin(theta)
    cosine = sp.cos(theta)
    spatial_metric = sp.diag(
        radial_metric**2,
        radius**2,
        radius**2 * sine**2,
    )
    inverse_spatial_metric = sp.diag(
        1 / radial_metric**2,
        1 / radius**2,
        1 / (radius**2 * sine**2),
    )
    shift = sp.Matrix(
        [radial_shift * cosine, -radius * angular_shift * sine, 0]
    )
    christoffel: dict[tuple[int, int, int], sp.Expr] = {}
    for upper in range(3):
        for first in range(3):
            for second in range(3):
                value = 0
                for contracted in range(3):
                    value += inverse_spatial_metric[upper, contracted] * (
                        sp.diff(spatial_metric[contracted, second], coordinates[first])
                        + sp.diff(spatial_metric[contracted, first], coordinates[second])
                        - sp.diff(spatial_metric[first, second], coordinates[contracted])
                    ) / 2
                if value != 0:
                    christoffel[(upper, first, second)] = value
    shift_derivative = sp.zeros(3)
    covariant_shift: list[list[sp.Expr]] = [[sp.Integer(0)] * 3 for _ in range(3)]
    for first in range(3):
        for second in range(3):
            covariant_shift[first][second] = sp.diff(
                shift[second], coordinates[first]
            ) - sum(
                christoffel.get((contracted, first, second), 0)
                * shift[contracted]
                for contracted in range(3)
            )
    extrinsic_curvature = sp.Matrix(
        3,
        3,
        lambda first, second: (
            covariant_shift[first][second]
            + covariant_shift[second][first]
        )
        / (2 * lapse),
    )
    trace = sum(
        inverse_spatial_metric[first, second]
        * extrinsic_curvature[first, second]
        for first in range(3)
        for second in range(3)
    )
    curvature_square = sum(
        inverse_spatial_metric[first, raised_first]
        * inverse_spatial_metric[second, raised_second]
        * extrinsic_curvature[first, second]
        * extrinsic_curvature[raised_first, raised_second]
        for first in range(3)
        for second in range(3)
        for raised_first in range(3)
        for raised_second in range(3)
    )
    measure = 2 * sp.pi * lapse * radial_metric * radius**2 * sine
    gr_lagrangian = sp.factor(
        sp.integrate(
            sp.expand_trig(sp.expand(measure * (curvature_square - trace**2))),
            (theta, 0, sp.pi),
        )
    )
    shift_square = sum(
        inverse_spatial_metric[first, second] * shift[first] * shift[second]
        for first in range(3)
        for second in range(3)
    )
    matter_measure = 2 * sp.pi * radial_metric * radius**2 * sine
    matter_lagrangian = sp.factor(
        sp.integrate(
            sp.expand_trig(
                sp.expand(
                    matter_measure
                    * (density + pressure)
                    * shift_square
                    / (2 * lapse)
                )
            ),
            (theta, 0, sp.pi),
        )
    )
    lapse_value, radial_metric_value, radial_metric_prime = sp.symbols(
        "N_value A_value A_prime", positive=True, real=True
    )
    density_value, pressure_value = sp.symbols(
        "rho_value P_value", real=True
    )
    values = sp.symbols("k_value s_value", real=True)
    derivatives = sp.symbols("k_prime s_prime", real=True)
    substitutions = [
        (sp.diff(radial_metric, radius), radial_metric_prime),
        (sp.diff(radial_shift, radius), derivatives[0]),
        (sp.diff(angular_shift, radius), derivatives[1]),
        (lapse, lapse_value),
        (radial_metric, radial_metric_value),
        (density, density_value),
        (pressure, pressure_value),
        (radial_shift, values[0]),
        (angular_shift, values[1]),
    ]
    arguments = (
        radius,
        lapse_value,
        radial_metric_value,
        radial_metric_prime,
        density_value,
        pressure_value,
        *values,
        *derivatives,
    )
    return (
        sp.factor(gr_lagrangian.subs(substitutions)),
        sp.factor(matter_lagrangian.subs(substitutions)),
        arguments,
    )


@lru_cache(maxsize=1)
def metric_shift_ward_identities() -> dict[str, sp.Expr]:
    gr_lagrangian, matter_lagrangian, arguments = (
        reduced_gr_matter_shift_lagrangian()
    )
    (
        radius,
        lapse,
        radial_metric,
        radial_metric_prime,
        density,
        pressure,
        radial_shift,
        angular_shift,
        radial_shift_prime,
        angular_shift_prime,
    ) = arguments
    lapse_prime, radial_shift_second, angular_shift_second = sp.symbols(
        "N_prime k_second s_second", real=True
    )

    def total_derivative(expression: sp.Expr) -> sp.Expr:
        return (
            sp.diff(expression, radius)
            + sp.diff(expression, lapse) * lapse_prime
            + sp.diff(expression, radial_metric) * radial_metric_prime
            + sp.diff(expression, radial_shift) * radial_shift_prime
            + sp.diff(expression, angular_shift) * angular_shift_prime
            + sp.diff(expression, radial_shift_prime) * radial_shift_second
            + sp.diff(expression, angular_shift_prime) * angular_shift_second
        )

    lagrangian = gr_lagrangian + 16 * sp.pi * matter_lagrangian
    radial_euler = sp.factor(
        total_derivative(sp.diff(lagrangian, radial_shift_prime))
        - sp.diff(lagrangian, radial_shift)
    )
    angular_euler = sp.factor(
        total_derivative(sp.diff(lagrangian, angular_shift_prime))
        - sp.diff(lagrangian, angular_shift)
    )
    lapse_gradient = (
        (radial_metric**2 - 1) / (2 * radius)
        + 4 * sp.pi * radius * radial_metric**2 * pressure
    )
    radial_metric_gradient = (
        4 * sp.pi * radius * radial_metric**2 * density
        - (radial_metric**2 - 1) / (2 * radius)
    )
    invariant_shift, invariant_shift_prime = sp.symbols(
        "Z Z_prime", real=True
    )
    angular_prime_from_invariant = (
        radial_shift
        - angular_shift
        + 2 * radius * lapse_gradient * angular_shift
        - invariant_shift
    ) / radius
    pressure_prime = -(density + pressure) * lapse_gradient
    lapse_gradient_prime = (
        sp.diff(lapse_gradient, radius)
        + sp.diff(lapse_gradient, radial_metric)
        * radial_metric
        * radial_metric_gradient
        + sp.diff(lapse_gradient, pressure) * pressure_prime
    )
    angular_second_from_invariant = (
        sp.diff(angular_prime_from_invariant, radius)
        + sp.diff(angular_prime_from_invariant, radial_metric)
        * radial_metric
        * radial_metric_gradient
        + sp.diff(angular_prime_from_invariant, pressure) * pressure_prime
        + sp.diff(angular_prime_from_invariant, radial_shift)
        * radial_shift_prime
        + sp.diff(angular_prime_from_invariant, angular_shift)
        * angular_prime_from_invariant
        + sp.diff(angular_prime_from_invariant, invariant_shift)
        * invariant_shift_prime
    )
    background = {
        lapse_prime: lapse * lapse_gradient,
        radial_metric_prime: radial_metric * radial_metric_gradient,
        angular_shift_prime: angular_prime_from_invariant,
        angular_shift_second: angular_second_from_invariant,
    }
    return {
        "radial_euler_invariant": sp.factor(radial_euler.subs(background)),
        "angular_euler_invariant": sp.factor(angular_euler.subs(background)),
        "invariant_definition": sp.factor(
            radial_shift
            - radius * angular_shift_prime
            - angular_shift
            + 2 * radius * lapse_gradient * angular_shift
        ),
        "lapse_gradient": lapse_gradient,
        "radial_metric_gradient": radial_metric_gradient,
    }


@lru_cache(maxsize=1)
def aether_radial_shift_source() -> tuple[sp.Expr, tuple[sp.Symbol, ...]]:
    lagrangian, arguments = reduced_shift_flow_cross_lagrangian()
    (
        radius,
        ratio,
        lapse,
        radial_metric,
        lapse_prime,
        radial_metric_prime,
        radial_flow,
        angular_flow,
        radial_shift,
        angular_shift,
        radial_flow_prime,
        angular_flow_prime,
        radial_shift_prime,
        angular_shift_prime,
    ) = arguments
    lapse_second, radial_metric_second = sp.symbols(
        "N_second A_second", real=True
    )
    radial_flow_second, angular_flow_second = sp.symbols(
        "a_second b_second", real=True
    )
    radial_shift_second, angular_shift_second = sp.symbols(
        "k_second s_second", real=True
    )

    def total_derivative(expression: sp.Expr) -> sp.Expr:
        return (
            sp.diff(expression, radius)
            + sp.diff(expression, lapse) * lapse_prime
            + sp.diff(expression, radial_metric) * radial_metric_prime
            + sp.diff(expression, lapse_prime) * lapse_second
            + sp.diff(expression, radial_metric_prime) * radial_metric_second
            + sp.diff(expression, radial_flow) * radial_flow_prime
            + sp.diff(expression, angular_flow) * angular_flow_prime
            + sp.diff(expression, radial_flow_prime) * radial_flow_second
            + sp.diff(expression, angular_flow_prime) * angular_flow_second
            + sp.diff(expression, radial_shift) * radial_shift_prime
            + sp.diff(expression, angular_shift) * angular_shift_prime
            + sp.diff(expression, radial_shift_prime) * radial_shift_second
            + sp.diff(expression, angular_shift_prime) * angular_shift_second
        )

    source = sp.factor(
        total_derivative(sp.diff(lagrangian, radial_shift_prime))
        - sp.diff(lagrangian, radial_shift)
    )
    source_arguments = (
        *arguments[:6],
        lapse_second,
        radial_metric_second,
        *arguments[6:12],
        radial_flow_second,
        angular_flow_second,
        *arguments[12:],
        radial_shift_second,
        angular_shift_second,
    )
    return source, source_arguments


@lru_cache(maxsize=1)
def asymptotic_response_identities() -> dict[str, sp.Expr]:
    source, arguments = aether_radial_shift_source()
    (
        radius,
        ratio,
        lapse,
        radial_metric,
        lapse_prime,
        radial_metric_prime,
        lapse_second,
        radial_metric_second,
        radial_flow,
        angular_flow,
        radial_shift,
        angular_shift,
        radial_flow_prime,
        angular_flow_prime,
        radial_flow_second,
        angular_flow_second,
        radial_shift_prime,
        angular_shift_prime,
        radial_shift_second,
        angular_shift_second,
    ) = arguments
    compactness, radial_tail, angular_tail = sp.symbols(
        "C A_infinity B_infinity", real=True
    )
    lapse_exterior = sp.sqrt(1 - 2 * compactness / radius)
    radial_metric_exterior = 1 / lapse_exterior
    radial_flow_exterior = 1 + radial_tail / radius
    angular_flow_exterior = 1 + angular_tail / radius
    substitutions = {
        lapse: lapse_exterior,
        radial_metric: radial_metric_exterior,
        lapse_prime: sp.diff(lapse_exterior, radius),
        radial_metric_prime: sp.diff(radial_metric_exterior, radius),
        lapse_second: sp.diff(lapse_exterior, radius, 2),
        radial_metric_second: sp.diff(radial_metric_exterior, radius, 2),
        radial_flow: radial_flow_exterior,
        angular_flow: angular_flow_exterior,
        radial_flow_prime: sp.diff(radial_flow_exterior, radius),
        angular_flow_prime: sp.diff(angular_flow_exterior, radius),
        radial_flow_second: sp.diff(radial_flow_exterior, radius, 2),
        angular_flow_second: sp.diff(angular_flow_exterior, radius, 2),
        radial_shift: 0,
        angular_shift: 0,
        radial_shift_prime: 0,
        angular_shift_prime: 0,
        radial_shift_second: 0,
        angular_shift_second: 0,
    }
    exterior_source = sp.simplify(source.subs(substitutions))
    invariant_shift = sp.factor(-3 * exterior_source / (8 * sp.pi))
    invariant_tail = sp.factor(
        sp.limit(radius * invariant_shift / compactness, radius, sp.oo)
    )
    c_14_bar = 2 * ratio / (1 + ratio)
    response_from_metric = sp.factor((invariant_tail + 2 * c_14_bar) / 4)
    response_from_bulk = sp.factor(
        (
            (3 * ratio**2 + 6 * ratio + 1) * radial_tail
            + 4 * angular_tail
            + compactness * (6 * ratio**2 + 18 * ratio + 8)
        )
        / (18 * compactness * (1 + ratio))
    )
    exterior_relation = sp.factor(
        (3 * ratio**2 + 6 * ratio + 7) * radial_tail
        - 8 * angular_tail
        + 2 * compactness * (3 * ratio**2 + 1)
    )
    return {
        "invariant_tail": invariant_tail,
        "response_from_metric": response_from_metric,
        "response_from_bulk": response_from_bulk,
        "response_difference": sp.factor(
            response_from_bulk - response_from_metric
        ),
        "exterior_relation": exterior_relation,
    }


def main() -> int:
    lagrangian, _ = reduced_shift_flow_cross_lagrangian()
    gr_lagrangian, matter_lagrangian, _ = reduced_gr_matter_shift_lagrangian()
    print(f"cross_operation_count={sp.count_ops(lagrangian)}")
    print(lagrangian)
    print(f"gr_operation_count={sp.count_ops(gr_lagrangian)}")
    print(gr_lagrangian)
    print(f"matter_operation_count={sp.count_ops(matter_lagrangian)}")
    print(matter_lagrangian)
    ward = metric_shift_ward_identities()
    print(f"radial_ward={ward['radial_euler_invariant']}")
    print(f"angular_ward={ward['angular_euler_invariant']}")
    asymptotic = asymptotic_response_identities()
    for key, value in asymptotic.items():
        print(f"{key}={value}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
