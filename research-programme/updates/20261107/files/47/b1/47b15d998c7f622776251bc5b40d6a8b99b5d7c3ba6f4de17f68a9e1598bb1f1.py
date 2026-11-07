import mpmath as mp
from finite_matching_common import *
from emission_rates import ALPHA


def check(name, value, limit):
    value = float(value)
    return dict(name=name, value=value, limit=float(limit), passed=bool(np.isfinite(value) and value < limit))


def h_integral(rapidity):
    rapidity = mp.mpf(rapidity)
    if rapidity == 0:
        return mp.mpf(1)
    return mp.quad(lambda position: 1 if position == 0 else position / mp.tanh(position), [0, rapidity]) / rapidity


def h_closed(rapidity):
    rapidity = mp.mpf(rapidity)
    if rapidity == 0:
        return mp.mpf(1)
    decay = mp.exp(-2 * rapidity)
    return rapidity / 2 + mp.log(-mp.expm1(-2 * rapidity)) + (mp.pi ** 2 / 6 - mp.polylog(2, decay)) / (2 * rapidity)


def g_closed(invariant):
    invariant = mp.mpf(invariant)
    return 2 / invariant * (mp.pi ** 2 / 6 - mp.re(mp.polylog(2, 1 - invariant)))


def g_integral(invariant):
    invariant = mp.mpf(invariant)
    return -2 * mp.quad(lambda position: (mp.log(abs(invariant)) + mp.log(position)) / (1 - invariant * position), [0, 1])


def kinematics(energy, cosine):
    energy, cosine = mp.mpf(str(energy)), mp.mpf(str(cosine))
    if energy <= 0 or cosine < -1 or cosine >= 1:
        raise ValueError('Require positive energy and -1 <= cosine < 1; exact forward endpoint needs its analytic limit')
    outgoing = energy / (1 + energy * (1 - cosine))
    first, second = -energy, outgoing
    rapidity = mp.asinh(mp.sqrt(-(first + second) / 2))
    return first, second, rapidity


def compton(first, second):
    inverse = 1 / first + 1 / second
    return inverse ** 2 - 2 * inverse - first / second - second / first


def symmetric(first, second, rapidity, h_function=h_closed):
    inverse, ratio, product = 1 / first + 1 / second, first / second + second / first, first * second
    cusp = 2 * rapidity / mp.tanh(2 * rapidity)
    result = (mp.mpf(3) / 4 - cusp * (2 * h_function(rapidity) - h_function(2 * rapidity))) * compton(first, second)
    result += rapidity / mp.tanh(rapidity) * (4 + inverse + ratio) * h_function(rapidity)
    result -= 2 * rapidity * mp.tanh(rapidity) * (1 - inverse / 2)
    result += rapidity ** 2 * (2 - 1 / product + 3 * ratio / 2)
    result += inverse ** 2 / 4 * (1 - 2 * product * inverse)
    bracket = rapidity / mp.sinh(2 * rapidity) * (1 - 3 * inverse + ratio) + (1 + inverse - 2 / product) / 2
    bracket -= cusp * (1 + inverse / 2 + ratio - 1 / product)
    return result + mp.log(4 * abs(product)) * bracket


def asymmetric(first, second, rapidity, argument_scale=2):
    result = -(2 * first + second) / (2 * second * (1 - 2 * first))
    result += g_closed(argument_scale * first) * (2 * first ** 2 / second + second / (2 * first ** 2) + 2 * first + second + 1 / first - 3 / (2 * second) + first / second - 1)
    bracket = 2 * rapidity / mp.sinh(2 * rapidity) * ((2 / first + second) * (1 - second) / first - second)
    bracket += (3 + 2 * second) / first - (2 - second) / first ** 2
    bracket += (second ** 2 - first * (1 + second + 2 * second ** 2)) / (second * (1 - 2 * first) ** 2)
    return result + mp.log(2 * abs(first)) * bracket


def recast_finite(energy, cosine, argument_scale=2, h_function=h_closed):
    first, second, rapidity = kinematics(energy, cosine)
    if abs(1-2*second) < mp.mpf(10)**(-mp.mp.dps//4):
        return removable_limit(lambda shifted: recast_finite(shifted, cosine, argument_scale, h_function), mp.mpf(str(energy)))
    return 2 * symmetric(first, second, rapidity, h_function) + asymmetric(first, second, rapidity, argument_scale) + asymmetric(second, first, rapidity, argument_scale)


def removable_limit(function, center):
    step = max(1, abs(center)) * mp.mpf(10)**(-mp.mp.dps//6)
    wide = (function(center+step)+function(center-step))/2
    narrow = (function(center+step/2)+function(center-step/2))/2
    return (4*narrow-wide)/3


def brown_direct_part(first, second, rapidity):
    born = compton(first / 2, second / 2)
    result = -2 * rapidity / mp.tanh(2 * rapidity) * (2 * h_closed(rapidity) - h_closed(2 * rapidity)) * born
    result -= 4 * rapidity * mp.sinh(2 * rapidity) / (first * second) * (2 - mp.cosh(2 * rapidity)) * h_closed(rapidity)
    result += 2 * rapidity / mp.tanh(rapidity) * h_closed(rapidity)
    bracket = 4 * rapidity / mp.tanh(2 * rapidity) * (4 * mp.cosh(rapidity) ** 2 / (first * second)
        + (first - 6) / (2 * second * mp.cosh(2 * rapidity)) + 4 / first ** 2 - 1 / first - second / (2 * first) - first / second - 1)
    bracket += 3 * second / (2 * first ** 2) + 3 * second / (2 * first) + 3 / second + 1 - 7 / (first * second) + 8 / first - 8 / first ** 2
    bracket += (2 * first - second ** 2 - first ** 2 * second) / (2 * first ** 2 * second * (first - 1))
    bracket -= (2 * first ** 2 + second) / (2 * second * (first - 1) ** 2)
    result += mp.log(abs(first)) * bracket
    result += rapidity ** 2 / mp.sinh(rapidity) ** 2 * (2 / first - 7 * first / 4 - 3 * second ** 2 / (4 * first))
    result -= 4 * rapidity * mp.tanh(rapidity) * (mp.mpf(1) / 2 - 1 / first)
    result += 4 * (1 / first + 1 / second) ** 2 - 12 / first - 3 * first / (2 * second) - 2 * first / second ** 2
    result += (first / second + mp.mpf(1) / 2) / (first - 1)
    result += g_closed(first) * (first ** 2 / second + second / first ** 2 + first / second + first + second / 2 + 2 / first - 3 / second - 1)
    return result


def brown_finite(energy, cosine):
    first, second, rapidity = kinematics(energy, cosine)
    if abs(1-2*second) < mp.mpf(10)**(-mp.mp.dps//4):
        return removable_limit(lambda shifted: brown_finite(shifted, cosine), mp.mpf(str(energy)))
    return brown_direct_part(2 * first, 2 * second, rapidity) + brown_direct_part(2 * second, 2 * first, rapidity)


def cusp(energy, cosine):
    first, second, rapidity = kinematics(energy, cosine)
    return 2 * mp.mpf(str(ALPHA)) / mp.pi * (2 * rapidity / mp.tanh(2 * rapidity) - 1)


def finite_virtual_ratio(energy, cosine):
    first, second, rapidity = kinematics(energy, cosine)
    return -mp.mpf(str(ALPHA)) / mp.pi * recast_finite(energy, cosine) / compton(first, second)


def soft_constant(energy, cosine):
    first, second, rapidity = kinematics(energy, cosine)
    coefficient = 2 * rapidity / mp.tanh(2 * rapidity)
    return -cusp(energy, cosine) / 2 - 2 * mp.mpf(str(ALPHA)) / mp.pi * coefficient * (h_closed(2 * rapidity) - 1)


def matched_soft_ratio(energy, cosine, separator):
    return finite_virtual_ratio(energy, cosine) + soft_constant(energy, cosine) + cusp(energy, cosine) * mp.log(2 * mp.mpf(str(separator)))
