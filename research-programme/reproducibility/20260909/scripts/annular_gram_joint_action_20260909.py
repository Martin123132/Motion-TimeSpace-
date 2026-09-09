from functools import lru_cache

import numpy as numerical

from annular_compatible_current_restoring_20260909 import unit_gram_template


@lru_cache(maxsize=4)
def gram_matrices(count):
    margin, adjacent, extras = unit_gram_template(count)
    differences = numerical.diff(numerical.eye(count), n=3, axis=0)
    rows = [numerical.sqrt(margin)[:, None] * differences]
    rows.append(numerical.sqrt(numerical.abs(adjacent))[:, None] * (differences[:-1] + numerical.sign(adjacent)[:, None] * differences[1:]))
    locations = list(numerical.arange(count - 3) + 1.5)
    locations.extend(numerical.arange(count - 4) + 2.0)
    for first, second, weight in extras:
        rows.append((numerical.sqrt(abs(weight)) * (differences[first] + numerical.sign(weight) * differences[second]))[None, :])
        locations.append((first + second) / 2 + 1.5)
    factors = numerical.concatenate(rows)
    locations = numerical.array(locations)
    left = numerical.floor(locations).astype(int)
    fraction = locations - left
    sampling = numerical.zeros((locations.size, count))
    sampling[numerical.arange(locations.size), left] = 1 - fraction
    sampling[numerical.arange(locations.size), left + 1] = fraction
    factors.setflags(write=False)
    sampling.setflags(write=False)
    return factors, sampling


def remainder(values, coefficient, spacing):
    factors, sampling = gram_matrices(values.size)
    return factors.T @ ((sampling @ coefficient) * (factors @ values)) / spacing


def coefficient_pairing(first, second, spacing):
    factors, sampling = gram_matrices(first.size)
    return sampling.T @ ((factors @ first) * (factors @ second)) / spacing


def principal_coefficient(primitive, radii, constants, sigma):
    scalar, velocity, gradient, mass, shift, off_gauge = primitive
    exponential = numerical.exp(shift)
    lapse = 1 - 2 * mass / radii - constants["Lambda"] * radii**2 / 3
    determinant = 1 + lapse * off_gauge
    radial = gradient - sigma * velocity
    physical_time = velocity / exponential
    kinetic = (2 * physical_time * radial + lapse * radial**2 - off_gauge * physical_time**2) / determinant
    principal = 1 - 4 * constants["b2"] * kinetic - 6 * constants["b3"] * kinetic**2
    slope = -4 * constants["b2"] - 12 * constants["b3"] * kinetic
    raised = physical_time + lapse * radial
    coefficient = radii**2 * exponential * (lapse * principal / numerical.sqrt(determinant) + 2 * slope * raised**2 / determinant**1.5)
    return coefficient


@lru_cache(maxsize=1)
def coefficient_differentiator():
    import sympy as symbolic

    velocity, gradient, mass, shift, off_gauge, radius, sigma, quartic, sextic, cosmological = symbolic.symbols("q w mu delta beta r sigma b2 b3 Lambda", real=True)
    exponential = symbolic.exp(shift)
    lapse = 1 - 2 * mass / radius - cosmological * radius**2 / 3
    determinant = 1 + lapse * off_gauge
    radial = gradient - sigma * velocity
    physical_time = velocity / exponential
    kinetic = (2 * physical_time * radial + lapse * radial**2 - off_gauge * physical_time**2) / determinant
    principal = 1 - 4 * quartic * kinetic - 6 * sextic * kinetic**2
    slope = -4 * quartic - 12 * sextic * kinetic
    raised = physical_time + lapse * radial
    coefficient = radius**2 * exponential * (lapse * principal / symbolic.sqrt(determinant) + 2 * slope * raised**2 / determinant**symbolic.Rational(3, 2))
    variables = [velocity, gradient, mass, shift, off_gauge]
    expressions = [coefficient.subs(off_gauge, 0)]
    expressions.extend(symbolic.diff(coefficient, variable).subs(off_gauge, 0) for variable in variables)
    expressions.extend(symbolic.diff(coefficient, first, second).subs(off_gauge, 0) for first in variables for second in variables)
    evaluator = symbolic.lambdify(variables[:-1] + [radius, sigma, quartic, sextic, cosmological], expressions, modules="numpy", cse=True, docstring_limit=0)
    return evaluator


def coefficient_jets(primitive, radii, constants, sigma):
    if numerical.any(primitive[5] != 0):
        raise ValueError("Coefficient derivative evaluation is on beta=0 only")
    evaluated = coefficient_differentiator()(*primitive[1:5], radii, sigma, constants["b2"], constants["b3"], constants["Lambda"])
    evaluated = numerical.stack([numerical.broadcast_to(value, radii.shape) for value in evaluated])
    return evaluated[0], evaluated[1:6], evaluated[6:].reshape(5, 5, radii.size)


def potential(primitive, radii, constants, sigma, spacing):
    coefficient = principal_coefficient(primitive, radii, constants, sigma)
    factors, sampling = gram_matrices(radii.size)
    return numerical.sum((sampling @ coefficient) * (factors @ primitive[0])**2) / (2 * spacing)


def potential_gradient(primitive, radii, constants, sigma, spacing):
    coefficient, gradient, unused_hessian = coefficient_jets(primitive, radii, constants, sigma)
    dual = coefficient_pairing(primitive[0], primitive[0], spacing) / 2
    result = numerical.empty_like(primitive)
    result[0] = remainder(primitive[0], coefficient, spacing)
    result[1:] = gradient * dual
    return result


def potential_hessian_pair(primitive, first, second, radii, constants, sigma, spacing):
    coefficient, gradient, hessian = coefficient_jets(primitive, radii, constants, sigma)
    first_coefficient = numerical.sum(gradient * first[1:], axis=0)
    second_coefficient = numerical.sum(gradient * second[1:], axis=0)
    mixed_coefficient = numerical.einsum("ijn,in,jn->n", hessian, first[1:], second[1:])
    scalar = primitive[0]
    terms = numerical.array([
        numerical.dot(first[0], remainder(second[0], coefficient, spacing)),
        numerical.dot(first[0], remainder(scalar, second_coefficient, spacing)),
        numerical.dot(second[0], remainder(scalar, first_coefficient, spacing)),
        numerical.dot(scalar, remainder(scalar, mixed_coefficient, spacing)) / 2,
    ])
    return terms.sum(), terms


def matter_values(primitive, radii, constants, sigma):
    scalar, velocity, gradient, mass, shift, off_gauge = primitive
    exponential = numerical.exp(shift)
    lapse = 1 - 2 * mass / radii - constants["Lambda"] * radii**2 / 3
    determinant = 1 + lapse * off_gauge
    radial = gradient - sigma * velocity
    physical_time = velocity / exponential
    kinetic = (2 * physical_time * radial + lapse * radial**2 - off_gauge * physical_time**2) / determinant
    lagrangian = -kinetic / 2 - constants["m_chi"]**2 * scalar**2 / 2 + constants["b2"] * kinetic**2 + constants["b3"] * kinetic**3
    principal = 1 - 4 * constants["b2"] * kinetic - 6 * constants["b3"] * kinetic**2
    return exponential, lapse, determinant, radial, physical_time, kinetic, lagrangian, principal


def action(primitive, mass_time, shift_time, radii, constants, sigma, kappa, weights, derivative_matrix, integrability_defect, include_gram=True):
    fields = primitive.copy()
    fields[2] = derivative_matrix @ fields[0] + integrability_defect
    exponential, lapse, determinant, radial, physical_time, kinetic, lagrangian, principal = matter_values(fields, radii, constants, sigma)
    mass_radial = derivative_matrix @ fields[3] - sigma * mass_time
    exponential_radial = derivative_matrix @ exponential - sigma * exponential * shift_time
    gravity = exponential * mass_radial / kappa
    gravity += fields[5] * (-mass_time + exponential * lapse * mass_radial - radii * lapse**2 * exponential_radial) / (2 * kappa)
    matter = radii**2 * exponential * numerical.sqrt(determinant) * lagrangian
    result = numerical.sum(weights * (gravity + matter))
    if include_gram:
        result -= potential(fields, radii, constants, sigma, float(radii[1] - radii[0]))
    return result
