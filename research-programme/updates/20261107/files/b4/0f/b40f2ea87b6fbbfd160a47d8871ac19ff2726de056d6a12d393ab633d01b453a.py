from vacuum_virtual import *


def massive_soft_integral(energy, cosine, separator, photon_mass):
    first, second, rapidity = kinematics(energy, cosine)
    speed = mp.tanh(2 * rapidity)
    upper = mp.asinh(mp.mpf(str(separator)) / mp.mpf(str(photon_mass)))
    def integrand(position):
        radial = mp.tanh(position)
        product = speed * radial
        ratio = 1 if product == 0 else mp.atanh(product) / product
        angular = 4 * ratio - 2 - 2 * (1 - speed ** 2) / (1 - product ** 2)
        return radial ** 2 * angular * mp.mpf(str(ALPHA)) / (2 * mp.pi)
    return mp.quad(integrand, [0, 1, min(4, upper), upper])


def massive_soft_asymptotic(energy, cosine, separator, photon_mass):
    return cusp(energy, cosine) * mp.log(2 * mp.mpf(str(separator)) / mp.mpf(str(photon_mass))) + soft_constant(energy, cosine)


def virtual_with_mass(energy, cosine, photon_mass):
    return finite_virtual_ratio(energy, cosine) + cusp(energy, cosine) * mp.log(mp.mpf(str(photon_mass)))
