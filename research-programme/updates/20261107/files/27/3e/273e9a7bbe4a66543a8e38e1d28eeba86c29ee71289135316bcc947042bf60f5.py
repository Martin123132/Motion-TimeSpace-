import mpmath as mp
import numpy as np

import integrate236 as retained


def reference_only(factors, frequency, degree, join):
    if degree not in (0, 1, 2) or join not in (0, 1):
        raise ValueError("Retained multipole and join required")
    frequency = np.asarray(frequency, dtype=float)
    if frequency.ndim != 1 or not len(frequency) or not np.isfinite(frequency).all() or np.any(frequency <= 0):
        raise ValueError("Finite positive one-dimensional frequencies required")
    basis = factors.features.evaluate(frequency, join)
    potential = retained.precise.stable_dot(basis, factors.high[join], factors.low[join])
    occupation = 1 / np.expm1(frequency)
    coupling = 2 * occupation * (1 + occupation) / (1 + 2 * occupation)
    harmonic = factors.harmonics[degree][2]
    wave = np.concatenate([basis[:, :, None] * harmonic, np.zeros((len(frequency), 1, len(harmonic)))], axis=1)
    result = np.broadcast_to(np.array(factors.right[join, degree]),
        (len(frequency), factors.state_count + 1, factors.spectral_count + 1, len(harmonic))).copy()
    for state in range(1, factors.state_count + 1):
        result[:, state] += (coupling * potential[:, state - 1])[:, None, None] * factors.right[join, degree][0]
        result[:, state] += (coupling * float(factors.coefficients[join][state]["density"]))[:, None, None] * wave
    return result


def panel_block(factors, frequency, measure, densities, factors_data, mode, join, degree,
                event_weight, angular_weight, emission_allowed, absorption_allowed):
    if mp.mp.dps < 60:
        raise ValueError("Subtracted source assembly requires at least60 decimal arithmetic digits")
    if mode not in ("control", "difference") or degree not in (0, 1, 2) or join not in (0, 1):
        raise ValueError("Retained source mode, multipole and join required")
    if emission_allowed and not absorption_allowed:
        raise ValueError("The retained domain has no emission-only region")
    frequency, measure = np.asarray(frequency, dtype=float), np.asarray(measure, dtype=float)
    if frequency.ndim != 1 or not len(frequency) or measure.shape != frequency.shape or not np.isfinite(frequency).all() or np.any(frequency <= 0) or not np.isfinite(measure).all():
        raise ValueError("Matching finite frequency and measure vectors required")
    if not np.isfinite(float(event_weight)) or not np.isfinite(float(angular_weight)):
        raise ValueError("Finite retained event and angular weights required")
    for sign, allowed in ((1, emission_allowed), (-1, absorption_allowed)):
        if allowed and (sign not in densities or sign not in factors_data or len(densities[sign]) != len(frequency)):
            raise ValueError("Missing physical events for an allowed branch")
    owner = factors.owner
    temperature = owner.temperature / owner.doppler
    soft = [retained.scalar(value) * temperature for value in frequency]
    occupation = [1 / mp.expm1(retained.scalar(value)) for value in frequency]
    pole, left_base = owner.pole[mode], factors.left[degree]
    if emission_allowed and absorption_allowed:
        sums = [(1 + population) * positive[mode] + population * negative[mode]
            for population, positive, negative in zip(occupation, densities[1], densities[-1])]
        differences = [(1 + population) * positive[mode] - population * negative[mode]
            for population, positive, negative in zip(occupation, densities[1], densities[-1])]
        residuals = [value - pole * (1 + 2 * population) / energy for value, population, energy in zip(sums, occupation, soft)]
        rho_sum, rho_diff, rho_residual = [measure * float(temperature) * np.array(list(map(float, values)))
            for values in (sums, differences, residuals)]
        result = retained.paired(left_base,
            (factors_data[1][degree, "left_delta"], factors_data[1][join, degree, "right_delta"]),
            (factors_data[-1][degree, "left_delta"], factors_data[-1][join, degree, "right_delta"]),
            factors_data[1][join, degree, "reference"], rho_sum, rho_diff, rho_residual)
    else:
        reference = factors_data[-1][join, degree, "reference"] if absorption_allowed else reference_only(factors, frequency, degree, join)
        subtracted = np.array([float(-pole * (1 + 2 * population) / energy) for population, energy in zip(occupation, soft)])
        reference_sum = np.einsum("n,nvbi->vbi", measure * float(temperature) * subtracted, reference)
        result = np.einsum("ai,vbi->vab", left_base, reference_sum, optimize=True)
        restore = float(pole) * np.sum(measure / frequency)
        result += restore * np.einsum("ai,vbi->vab", left_base, np.array(factors.right[join, degree]), optimize=True)
        if absorption_allowed:
            weighted_density = measure * float(temperature) * np.array([float(population * value[mode]) for population, value in zip(occupation, densities[-1])])
            left = left_base[None] + factors_data[-1][degree, "left_delta"]
            right = reference + factors_data[-1][join, degree, "right_delta"]
            result += retained.contract(left, weighted_density[:, None, None, None] * right)
    return result * (.5 * event_weight * angular_weight / (2 * degree + 1))


def separator_logarithm(factors, mode, join, degree, event_weight, angular_weight):
    if mp.mp.dps < 60:
        raise ValueError("Source logarithm requires at least60 decimal arithmetic digits")
    if mode not in ("control", "difference") or degree not in (0, 1, 2) or join not in (0, 1):
        raise ValueError("Retained source mode, multipole and join required")
    emission_upper, unused_absorption, unused_temperature = retained.upper_limits(factors.owner)
    scale = .5 * event_weight * angular_weight * float(factors.owner.pole[mode] * mp.log(2 * emission_upper)) / (2 * degree + 1)
    return scale * np.einsum("ai,vbi->vab", factors.left[degree], np.array(factors.right[join, degree]), optimize=True)
