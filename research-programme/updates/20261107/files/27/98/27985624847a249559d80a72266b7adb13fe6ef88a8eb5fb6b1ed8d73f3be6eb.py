from annular_high_precision_current_20260928 import decimal_array
from annular_support_shift_jet_20260928 import wave_terms, perturb, interpolate, integrals
from decimal import Decimal, localcontext
import numpy as np


def stable_current(packet, direction, amplitude, ratio, power):
    changed = perturb(packet, direction, amplitude, True)
    changed['alpha_t'] = packet['alpha_t'] + amplitude * packet['alpha'] * ratio
    alpha, beta, gradient, speed, speed_r, temporal, gradient_rate, unused, alpha_dot, beta_dot, energy, unused_energy, unused_momentum, flux = wave_terms(changed)
    with localcontext() as context:
        context.prec = 70
        amount = Decimal.from_float(float(amplitude))
        gradient_exact = decimal_array(packet['gradient'])
        gradient_rate_exact = decimal_array(packet['rate_r']) - decimal_array(packet['speed_r']) * gradient_exact
        acceleration_exact = decimal_array(packet['acceleration']) + amount * decimal_array(direction['rate'])
        speed_rate_exact = decimal_array(packet['speed_rate']) + amount * decimal_array(direction['speed'])
        temporal_rate = np.asarray(acceleration_exact - speed_rate_exact * gradient_exact
            - decimal_array(packet['speed']) * gradient_rate_exact, float)
    energy_rate = (alpha_dot * temporal**2 + beta_dot * gradient**2) / 2
    energy_rate += alpha * temporal * temporal_rate + beta * gradient * gradient_rate
    momentum_rate = (alpha_dot + speed_r * alpha) * temporal + alpha * temporal_rate
    integral = integrals(packet['radius'], packet['source'], power)
    test = (packet['radius'] - 6)**power
    weighted, weighted_r = interpolate(packet, packet['node_rate'] * integrals(packet['node_radius'], packet['source'], power))
    beta_t = -beta * changed['alpha_t'] / alpha
    density = -momentum_rate * weighted - flux * weighted_r
    density += (energy_rate + speed_r * energy - beta_t * energy / beta) * integral + energy * speed * test
    return packet['measure'] @ density
