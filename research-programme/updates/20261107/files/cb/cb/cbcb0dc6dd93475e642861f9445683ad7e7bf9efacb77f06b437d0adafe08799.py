import sys
import math
from common import PREVIOUS
sys.path.append(str(PREVIOUS))
from canonical_math import Background, coefficients, generator, transform, JFULL, transpose, multiply, sup, norm, load, joint_extractor
import numpy as np


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for harmonic, value in polynomial.items():
            result[harmonic] = result.get(harmonic, 0) + value
    return result


def scale(polynomial, factor):
    return {harmonic: factor * value for harmonic, value in polynomial.items()}


def product(left, right):
    result = {}
    for first, left_value in left.items():
        for second, right_value in right.items():
            key = first + second
            result[key] = result.get(key, 0) + left_value @ right_value
    return result


def adjoint(polynomial):
    return {harmonic: transpose(value) for harmonic, value in polynomial.items()}


def evaluate(polynomial, phases):
    return sum(value * np.exp(1j * harmonic * np.asarray(phases))[:, None, None] for harmonic, value in polynomial.items())


def harmonic_parts(constant, cosine, sine):
    return {0: constant.astype(complex), 2: (cosine - 1j * sine) / 2, -2: (cosine + 1j * sine) / 2}


def phase_background(provider, points):
    original = provider.evaluate(points)
    values, rates = provider.dense(provider.packet, points)
    physical = values * provider.packet["units"]
    slow_field = provider.packet["initial_fields"][0] + physical[:, 0]
    scale_value, hubble = original["scale"], original["hubble"]
    amplitude, omega_h = original["background"], original["omega_h"]
    rest_rate = provider.other(points, 1)
    slow_density_rate = -4 * original["velocity_s"]**2 + original["omega_s"]**2 * slow_field**2
    heavy_mean_rate = -omega_h * abs(amplitude)**2 / (2 * scale_value**2)
    hlog_mean = (rest_rate + slow_density_rate + heavy_mean_rate) / (6 * hubble**2)
    hlog_cosine = omega_h * (amplitude**2).real / (4 * scale_value**2 * hubble**2)
    hlog_sine = omega_h * (amplitude**2).imag / (4 * scale_value**2 * hubble**2)
    slow_rate = -2 * original["velocity_s"] - original["omega_s"]**2 * slow_field / hubble
    mean = dict(original)
    mean.update(phi_s=slow_field, hlog=hlog_mean, velocity_s_rate=slow_rate,
                background_rate=1j * (original["mu"] - omega_h / hubble) * amplitude,
                mu_rate=(1 - hlog_mean) * original["mu"])
    cosine = dict(hlog=hlog_cosine, velocity_s_rate=np.zeros_like(slow_rate),
                  background_rate=1.5 * amplitude.conjugate(), mu_rate=-hlog_cosine * original["mu"])
    sine = dict(hlog=hlog_sine, velocity_s_rate=np.zeros_like(slow_rate),
                background_rate=1.5j * amplitude.conjugate(), mu_rate=-hlog_sine * original["mu"])
    return original, mean, cosine, sine


def phased(mean, cosine, sine, phases):
    result = dict(mean)
    result["phase"] = np.asarray(phases)
    for name in cosine:
        result[name] = mean[name] + np.cos(2 * phases) * cosine[name] + np.sin(2 * phases) * sine[name]
    return result


def polynomials(mean, cosine, sine, wave):
    values, rate_mean = coefficients(mean, wave)
    increments = []
    for direction in (cosine, sine):
        changed = dict(mean)
        changed.update({name: mean[name] + value for name, value in direction.items()})
        increments.append(coefficients(changed, wave)[1] - rate_mean)
    rate_parts = {harmonic: value for harmonic, value in harmonic_parts(rate_mean, increments[0], increments[1]).items()}
    slow_scale = mean["scale"] * (wave**2 + mean["omega_s"]**2)**.25
    metric_scale = mean["scale"] * np.sqrt(wave)
    units = np.column_stack([1 / slow_scale, slow_scale, np.ones(len(slow_scale)), np.ones(len(slow_scale)),
                             1 / metric_scale, metric_scale, 1 / metric_scale, metric_scale])
    hscale = units[:, :, None] * units[:, None, :]
    hessian = {0: values[:, 0] * hscale}
    generating = {}
    derivative = {}
    mu_log = harmonic_parts(mean["mu_rate"] / mean["mu"], cosine["mu_rate"] / mean["mu"], sine["mu_rate"] / mean["mu"])
    for harmonic, cosine_index, sine_index in ((2, 1, 2), (4, 3, 4)):
        for sign in (-1, 1):
            index = sign * harmonic
            coefficient = (values[:, cosine_index] - 1j * sign * values[:, sine_index]) / 2
            hessian[index] = coefficient * hscale
            generating[index] = hessian[index] / (1j * index * mean["mu"][:, None, None])
            derivative[index] = derivative.get(index, 0) + hessian[index]
            for background_harmonic, rates in rate_parts.items():
                rate = (rates[:, cosine_index] - 1j * sign * rates[:, sine_index]) / 2
                change = (rate - coefficient * mu_log[background_harmonic][:, None, None]) * hscale / (1j * index * mean["mu"][:, None, None])
                key = index + background_harmonic
                derivative[key] = derivative.get(key, 0) + change
    return hessian, {key: JFULL @ value for key, value in generating.items()}, {key: JFULL @ value for key, value in derivative.items()}, units


def action_orders(hessian, exponent, exponent_rate):
    count = len(next(iter(hessian.values())))
    identity = {0: np.broadcast_to(np.eye(8), (count, 8, 8)).copy().astype(complex)}
    hessian_term, connection_term, map_term = hessian, exponent_rate, identity
    hessian_sum, connection_sum, map_sum = {}, {}, {}
    results = []
    for order in range(4):
        if order:
            hessian_term = add(product(adjoint(exponent), hessian_term), product(hessian_term, exponent))
            connection_term = add(product(connection_term, exponent), scale(product(exponent, connection_term), -1))
            map_term = product(map_term, exponent)
        hessian_sum = add(hessian_sum, scale(hessian_term, 1 / math.factorial(order)))
        connection_sum = add(connection_sum, {key: JFULL @ value / math.factorial(order + 1) for key, value in connection_term.items()})
        map_sum = add(map_sum, scale(map_term, 1 / math.factorial(order)))
        action = add(hessian_sum, connection_sum)
        results.append(dict(hessian=action, source_map=adjoint(map_sum), coordinate_map=map_sum))
    return results


def constraint_polynomial(background, wave, units):
    count = len(units)
    scale_value, hubble = background["scale"], background["hubble"]
    amplitude = background["background"]
    source = np.zeros((count, 8))
    source[:, 0] = background["velocity_s"]
    source[:, 2], source[:, 3] = amplitude.imag / (2 * scale_value**2), -amplitude.real / (2 * scale_value**2)
    cosine, sine = np.zeros_like(source), np.zeros_like(source)
    cosine[:, 2], cosine[:, 3] = amplitude.imag / (2 * scale_value**2), amplitude.real / (2 * scale_value**2)
    sine[:, 2], sine[:, 3] = -amplitude.real / (2 * scale_value**2), amplitude.imag / (2 * scale_value**2)
    rows = np.zeros((count, 2, 8))
    rows[:, 0] = 1.5 * hubble[:, None] * source
    rows[:, 0, 0] += background["omega_s"]**2 * background["phi_s"] / 2
    rows[:, 0, 1] += background["velocity_s"] / (2 * scale_value**2)
    rows[:, 0, 2] += background["omega_h"] * amplitude.real / (2 * scale_value**2)
    rows[:, 0, 3] += background["omega_h"] * amplitude.imag / (2 * scale_value**2)
    rows[:, 0, 5] += 3 * hubble / scale_value**2
    rows[:, 0, 6] += wave**2
    rows[:, 0, 7] -= hubble / (2 * scale_value**2)
    rows[:, 1, 5] = 1 / scale_value**2
    cos_rows, sin_rows = np.zeros_like(rows), np.zeros_like(rows)
    cos_rows[:, 0] = 1.5 * hubble[:, None] * cosine
    sin_rows[:, 0] = 1.5 * hubble[:, None] * sine
    return harmonic_parts(rows * units[:, None], cos_rows * units[:, None], sin_rows * units[:, None])
