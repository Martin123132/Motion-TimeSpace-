import mpmath as mp
from emission_angular_common import *


def differential_weight(energy, fraction, cosine_01, cosine_02, cosine_12):
    energy, fraction, cosine_01, cosine_02, cosine_12 = [mp.mpf(float(value)) for value in [energy, fraction, cosine_01, cosine_02, cosine_12]]
    emitted = energy * fraction
    angle_01, angle_02, angle_12 = 1 - cosine_01, 1 - cosine_02, 1 - cosine_12
    denominator = 1 + energy * angle_01 - emitted * angle_12
    companion = (energy - emitted - energy * emitted * angle_02) / denominator
    incoming = [-energy, companion, emitted]
    outgoing = [energy * (1 - companion * angle_01 - emitted * angle_02),
                -companion * denominator, -emitted * (1 + energy * angle_02 - companion * angle_12)]
    inverse_sum = sum(1 / value for value in incoming)
    reverse_sum = sum(1 / value for value in outgoing)
    inverse_pairs = sum(1 / (left * right) for left, right in zip(incoming, outgoing))
    energy_sum = sum(incoming)
    pair_sum = sum(left * right for left, right in zip(incoming, outgoing))
    product = mp.fprod(incoming)
    reverse_product = mp.fprod(outgoing)
    ratios = sum(left / right + right / left for left, right in zip(incoming, outgoing))
    difference = inverse_sum * reverse_sum - inverse_pairs
    squared = 2 * difference * ((inverse_sum + reverse_sum) * (2 + energy_sum) - difference - 8)
    squared -= 2 * energy_sum * (inverse_sum ** 2 + reverse_sum ** 2)
    squared -= 2 * (inverse_sum * reverse_sum + inverse_pairs * (1 - energy_sum)) * ratios + 8 * inverse_pairs
    bracket = (product + reverse_product) * (1 + energy_sum) + energy_sum ** 2 * (1 - pair_sum) + 2 * pair_sum
    bracket -= (inverse_sum * product + reverse_sum * reverse_product) * (2 + (1 - energy_sum) * pair_sum / energy_sum)
    squared += 4 * energy_sum / (product * reverse_product) * bracket
    electron_energy = 1 + energy - companion - emitted
    momentum_squared = energy ** 2 + companion ** 2 + emitted ** 2 - 2 * energy * companion * cosine_01 - 2 * energy * emitted * cosine_02 + 2 * companion * emitted * cosine_12
    shell = electron_energy ** 2 - momentum_squared - 1
    assert abs(shell) < mp.mpf('1e-50') and squared >= 0 and companion > 0
    return float(squared * companion / denominator)
