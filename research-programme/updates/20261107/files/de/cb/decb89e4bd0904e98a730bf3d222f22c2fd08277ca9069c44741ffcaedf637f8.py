import mpmath as mp
import numpy as np

import integrate236 as retained
from precise_epoch_response import scalar


def array(values):
    values = np.asarray(values, dtype=object)
    return np.array([scalar(value) for value in values.flat], dtype=object).reshape(values.shape)


def contract(left, right):
    left, right = array(left), array(right)
    if left.ndim != 2 or right.ndim != 3 or left.shape[1] != right.shape[-1]:
        raise ValueError('Matching weak rows and full background/wave readouts required')
    product = left @ right.transpose(2, 0, 1).reshape(right.shape[-1], -1)
    return product.reshape(left.shape[0], right.shape[0], right.shape[1]).transpose(1, 0, 2)


def reference_components(response, frequency, join, degree):
    if mp.mp.dps < 60 or join not in (0, 1) or degree not in (0, 1, 2):
        raise ValueError('Retained source precision, join and multipole required')
    frequency = scalar(frequency)
    if not mp.isfinite(frequency) or frequency <= 0:
        raise ValueError('Finite positive soft frequency required')
    factors = response.factors
    basis = factors.features.evaluate(np.array([float(frequency)]), join)
    potential = response.contract(basis)[0]
    harmonic = factors.harmonics[degree][2]
    born = array(response.born(join, degree))
    if born.shape != (19, 18, (1, 3, 9)[degree]):
        raise ValueError('All eighteen physical/difference waves and nineteen backgrounds required')
    medium = np.empty_like(born)
    medium.fill(mp.mpf(0))
    for state in range(1, 19):
        density = response.born_coefficients[join][state]['density']
        for column in range(18):
            for axis in range(len(harmonic)):
                medium[state, column, axis] = mp.fsum([potential[state - 1] * born[0, column, axis],
                    density * potential[column] * scalar(harmonic[axis])])
    occupation = 1 / mp.expm1(frequency)
    coupling = 2 * occupation * (1 + occupation) / (1 + 2 * occupation)
    return dict(born=born, medium=medium, reference=born + coupling * medium,
        occupation=occupation, coupling=coupling)


def point(response, frequency, measure, densities, current, left_delta, mode, join, degree,
          event_weight, angular_weight, emission_allowed, absorption_allowed):
    if mp.mp.dps < 60 or mode not in ('control', 'difference') or join not in (0, 1) or degree not in (0, 1, 2):
        raise ValueError('Retained source precision and sectors required')
    if emission_allowed and not absorption_allowed:
        raise ValueError('No retained emission-only domain')
    values = tuple(map(scalar, (frequency, measure, event_weight, angular_weight)))
    if not all(mp.isfinite(value) and value > 0 for value in values):
        raise ValueError('Finite positive original node and quadrature weights required')
    frequency, measure, event_weight, angular_weight = values
    factors, owner = response.factors, response.factors.owner
    for sign, allowed in ((1, emission_allowed), (-1, absorption_allowed)):
        if allowed and (sign not in densities or sign not in current or sign not in left_delta or mode not in densities[sign]):
            raise ValueError('Physical branch data missing')
        if allowed and not mp.isfinite(densities[sign][mode]):
            raise ValueError('Nonfinite physical density')
    local_temperature = owner.temperature / owner.doppler
    soft = frequency * local_temperature
    pole = owner.pole[mode]
    reference = reference_components(response, frequency, join, degree)
    born, medium, normal = reference['born'], reference['medium'], reference['reference']
    population = reference['occupation']
    left = array(factors.left[degree])
    for sign, allowed in ((1, emission_allowed), (-1, absorption_allowed)):
        if allowed and (array(current[sign]['complete']).shape != born.shape
                or array(current[sign]['right_delta']).shape != born.shape or array(left_delta[sign]).shape != left.shape):
            raise ValueError('Incomplete physical source dimensions')
    if emission_allowed and absorption_allowed:
        positive = (1 + population) * densities[1][mode]
        negative = population * densities[-1][mode]
        density_sum, density_difference = positive + negative, positive - negative
        density_residual = density_sum - pole * (1 + 2 * population) / soft
        left_even = (array(left_delta[1]) + array(left_delta[-1])) / 2
        left_odd = (array(left_delta[1]) - array(left_delta[-1])) / 2
        right_even = (array(current[1]['right_delta']) + array(current[-1]['right_delta'])) / 2
        right_odd = (array(current[1]['right_delta']) - array(current[-1]['right_delta'])) / 2
        average = normal + right_even
        result = contract(left, density_residual * normal + density_sum * right_even + density_difference * right_odd)
        result += contract(left_even, density_sum * average + density_difference * right_odd)
        result += contract(left_odd, density_sum * right_odd + density_difference * average)
    else:
        thermal_reference = -2 * pole * population / soft * (born + (1 + population) * medium)
        result = contract(left, thermal_reference)
        if absorption_allowed:
            negative = population * densities[-1][mode]
            result += negative * contract(left + array(left_delta[-1]), array(current[-1]['complete']))
    scale = measure * local_temperature * event_weight * angular_weight / (2 * (2 * degree + 1))
    return scale * result


def logarithm(response, mode, join, degree, event_weight, angular_weight):
    if mp.mp.dps < 60 or mode not in ('control', 'difference') or join not in (0, 1) or degree not in (0, 1, 2):
        raise ValueError('Retained source precision and sectors required')
    weights = tuple(map(scalar, (event_weight, angular_weight)))
    if not all(mp.isfinite(value) and value > 0 for value in weights):
        raise ValueError('Finite positive original event/angular weights required')
    emission, unused_absorption, unused_temperature = retained.upper_limits(response.factors.owner)
    scale = weights[0] * weights[1] * response.factors.owner.pole[mode] * mp.log(2 * emission) / (2 * (2 * degree + 1))
    return scale * contract(response.factors.left[degree], response.born(join, degree))
