from common233 import *
from functools import lru_cache


def scalar(value):
    return mp.mpf(float(value)) if isinstance(value, (float, np.floating)) else mp.mpf(value)


@lru_cache(maxsize=64)
def thermodynamics(temperature_text, ratio_text):
    temperature, ratio = mp.mpf(temperature_text), mp.mpf(ratio_text)
    inverse = 1 / (temperature * ratio)
    scaled2 = mp.exp(inverse) * mp.besselk(2, inverse)
    ratio12 = mp.besselk(1, inverse) / mp.besselk(2, inverse)
    mean = ratio12 + 3 / inverse
    capacity = inverse**2 * (1 - ratio12**2) - 3 * inverse * ratio12 + 3
    return scaled2, mean, capacity


def electron_ratio(energy, temperature, ratio):
    zero, unused_mean, unused_capacity = thermodynamics(mp.nstr(temperature, 85), '1.0')
    scaled, mean, capacity = thermodynamics(mp.nstr(temperature, 85), mp.nstr(ratio, 85))
    logarithm = (energy - 1) * (ratio - 1) / (temperature * ratio) - mp.log(ratio) - mp.log(scaled / zero)
    return mp.exp(logarithm), (energy - mean) / (temperature * ratio**2), capacity


def statistics(event, potential, gas_shift):
    temperature = scalar(event['temperature'])
    frequencies = list(map(scalar, event['frequencies']))
    signs = event['signs']
    occupations = [1 / mp.expm1(value) for value in frequencies]
    potential = list(map(scalar, potential))
    ratio = 1 + scalar(gas_shift)
    initial = scalar(event['electron_initial'][0])
    final = initial + scalar(event['electron_transfer'][0])
    rate_forward, score_forward, unused = electron_ratio(initial, temperature, ratio)
    rate_reverse, score_reverse, unused = electron_ratio(final, temperature, ratio)
    forward_slopes = [value + int(sign < 0) for value, sign in zip(occupations, signs)]
    reverse_slopes = [value + int(sign > 0) for value, sign in zip(occupations, signs)]
    forward_factors = [1 + slope * value for slope, value in zip(forward_slopes, potential)]
    reverse_factors = [1 + slope * value for slope, value in zip(reverse_slopes, potential)]
    assert ratio > 0 and all(value > 0 for value in forward_factors + reverse_factors)
    forward = rate_forward * mp.fprod(forward_factors)
    reverse = rate_reverse * mp.fprod(reverse_factors)
    photon = [rate_forward * forward_slopes[index] * mp.fprod(forward_factors[:index] + forward_factors[index + 1:])
        - rate_reverse * reverse_slopes[index] * mp.fprod(reverse_factors[:index] + reverse_factors[index + 1:]) for index in range(len(signs))]
    gas = forward * score_forward - reverse * score_reverse
    momentum_initial = list(map(scalar, event['electron_initial'][1:]))
    transfer = list(map(scalar, event['electron_transfer'][1:]))
    momentum_final = [value + change for value, change in zip(momentum_initial, transfer)]
    velocity = [(forward * before - reverse * after) / (temperature * ratio) for before, after in zip(momentum_initial, momentum_final)]
    equilibrium = dict(photon=[mp.mpf(-sign) for sign in signs], gas=-scalar(event['electron_transfer'][0]) / temperature,
        velocity=[-value / temperature for value in transfer], density=mp.mpf(0))
    unused, mean, capacity = thermodynamics(mp.nstr(temperature, 85), '1.0')
    initial_score = (initial - mean) / temperature
    final_score = (final - mean) / temperature
    forward_change = initial_score * gas_shift + mp.fsum(slope * value for slope, value in zip(forward_slopes, potential))
    reverse_change = final_score * gas_shift + mp.fsum(slope * value for slope, value in zip(reverse_slopes, potential))
    mixed_photon = [forward_slopes[index] * (forward_change - forward_slopes[index] * potential[index])
        - reverse_slopes[index] * (reverse_change - reverse_slopes[index] * potential[index]) for index in range(len(signs))]
    mixed_gas = (initial_score**2 - final_score**2 - 2 * (initial_score - final_score)) * gas_shift
    mixed_gas += initial_score * mp.fsum(slope * value for slope, value in zip(forward_slopes, potential))
    mixed_gas -= final_score * mp.fsum(slope * value for slope, value in zip(reverse_slopes, potential))
    mixed_velocity = [(before * (forward_change - gas_shift) - after * (reverse_change - gas_shift)) / temperature
        for before, after in zip(momentum_initial, momentum_final)]
    mixed = dict(photon=mixed_photon, gas=mixed_gas, velocity=mixed_velocity, density=forward_change - reverse_change)
    exact = dict(photon=photon, gas=gas, velocity=velocity, density=forward - reverse)
    remainder = {name: [value - reference - change for value, reference, change in zip(exact[name], equilibrium[name], mixed[name])]
        if isinstance(exact[name], list) else exact[name] - equilibrium[name] - mixed[name] for name in exact}
    return dict(equilibrium=equilibrium, mixed=mixed, remainder=remainder, exact=exact, forward=forward, reverse=reverse,
        occupations=occupations, capacity=capacity, linear_source=forward_change - reverse_change)


def raw_flux(event, potential, gas_shift, velocity=None, density=0):
    temperature = scalar(event['temperature'])
    ratio = 1 + scalar(gas_shift)
    occupations = [1 / mp.expm1(scalar(value)) for value in event['frequencies']]
    populations = [value + value * (1 + value) * shift for value, shift in zip(occupations, potential)]
    initial = list(map(scalar, event['electron_initial']))
    final = [value + scalar(change) for value, change in zip(initial, event['electron_transfer'])]
    velocity = [mp.mpf(0)] * 3 if velocity is None else velocity
    lorentz = 1 / mp.sqrt(1 - mp.fsum(value**2 for value in velocity))
    forward_energy = lorentz * (initial[0] - mp.fsum(value * speed for value, speed in zip(initial[1:], velocity)))
    reverse_energy = lorentz * (final[0] - mp.fsum(value * speed for value, speed in zip(final[1:], velocity)))
    zero, unused, unused = thermodynamics(mp.nstr(temperature, 85), '1.0')
    scaled, unused, unused = thermodynamics(mp.nstr(temperature, 85), mp.nstr(ratio, 85))
    forward = mp.exp((initial[0] - 1) / temperature - (forward_energy - 1) / (temperature * ratio)) * zero / (ratio * scaled)
    reverse = mp.exp((final[0] - 1) / temperature - (reverse_energy - 1) / (temperature * ratio)) * zero / (ratio * scaled)
    for sign, reference, value in zip(event['signs'], occupations, populations):
        forward *= value / reference if sign < 0 else (1 + value) / (1 + reference)
        reverse *= (1 + value) / (1 + reference) if sign < 0 else value / reference
    return (1 + density) * (forward - reverse)


def geometry(parameters, signed_soft=None, direction=None):
    temperature = parameters['temperature']
    energy = parameters['energy']
    transform = parameters['transform']
    incident = transform @ np.array([energy, 0., 0., energy])
    initial = transform @ np.array([1., 0., 0., 0.])
    if signed_soft is None:
        hard = parameters['hard']
        recoil = np.array([0., 0., energy]) - hard * parameters['hard_direction']
        photons = [incident, transform @ np.r_[hard, hard * parameters['hard_direction']]]
        signs = [-1, 1]
    else:
        incident_soft = 1 - direction[2]
        mixed = 1 - parameters['hard_direction'] @ direction
        hard = (energy - signed_soft - energy * signed_soft * incident_soft) / (1 + energy * (1 - parameters['cosine']) - signed_soft * mixed)
        assert hard > 0
        recoil = np.array([0., 0., energy]) - hard * parameters['hard_direction'] - signed_soft * direction
        photons = [incident, transform @ np.r_[hard, hard * parameters['hard_direction']], transform @ np.r_[abs(signed_soft), abs(signed_soft) * direction]]
        signs = [-1, 1, 1 if signed_soft > 0 else -1]
    recoil_energy = recoil @ recoil / (np.sqrt(1 + recoil @ recoil) + 1)
    transfer = transform @ np.r_[recoil_energy, recoil]
    photons = np.array(photons)
    directions = photons[:, 1:] / np.linalg.norm(photons[:, 1:], axis=1)[:, None]
    return dict(temperature=temperature, photons=photons.tolist(), frequencies=(photons[:, 0] / temperature).tolist(),
        directions=directions.tolist(), electron_initial=initial.tolist(), electron_transfer=transfer.tolist(), signs=signs)


def projected(event, tests, features, coefficients, degree):
    directions = np.array(event['directions'])
    harmonics = angular.angular_feature(directions, degree)
    left = np.einsum('n,na,ni->ai', event['signs'], tests, harmonics)
    transfer = np.array(event['electron_transfer']) / event['temperature']
    gas_left = transfer[:1] if degree == 0 else transfer[1:] if degree == 1 else np.zeros(harmonics.shape[1])
    left = np.vstack([left, gas_left])
    right = np.einsum('n,na,ni->ai', np.array(list(map(float, coefficients['photon']))), features, harmonics)
    gas_right = np.array([float(coefficients['gas'])]) if degree == 0 else np.array(list(map(float, coefficients['velocity']))) if degree == 1 else np.zeros(harmonics.shape[1])
    right = np.vstack([right, gas_right])
    block = left @ right.T / (2 * degree + 1)
    density = left[:, 0] * float(coefficients['density']) if degree == 0 else np.zeros(len(left))
    return block, density, left, right
