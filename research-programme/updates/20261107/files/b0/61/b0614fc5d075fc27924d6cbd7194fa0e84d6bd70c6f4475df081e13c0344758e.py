import itertools
import mpmath as mp
from soft_matching_common import *


def dot(left, right):
    return left[0] * right[0] - sum(left[index] * right[index] for index in range(1, 4))


def add(*vectors):
    return mp.matrix([sum(vector[index] for vector in vectors) for index in range(4)])


def gamma_matrices():
    imaginary = mp.j
    return [mp.diag([1, 1, -1, -1]),
        mp.matrix([[0, 0, 0, 1], [0, 0, 1, 0], [0, -1, 0, 0], [-1, 0, 0, 0]]),
        mp.matrix([[0, 0, 0, -imaginary], [0, 0, imaginary, 0], [0, imaginary, 0, 0], [-imaginary, 0, 0, 0]]),
        mp.matrix([[0, 0, 1, 0], [0, 0, 0, -1], [-1, 0, 0, 0], [0, 1, 0, 0]])]


def slash(vector):
    matrices = gamma_matrices()
    return matrices[0] * vector[0] - sum((matrices[index] * vector[index] for index in range(1, 4)), mp.zeros(4))


def propagator(momentum):
    return (slash(momentum) + mp.eye(4)) / (dot(momentum, momentum) - 1)


def spinors(momentum):
    energy, first, second, third = momentum
    lower = mp.matrix([[third, first - mp.j * second], [first + mp.j * second, -third]]) / (energy + 1)
    return mp.sqrt(energy + 1) * mp.matrix([[1, 0], [0, 1], [lower[0, 0], lower[0, 1]], [lower[1, 0], lower[1, 1]]])


def unit(vector):
    values = mp.matrix([mp.mpf(str(value)) for value in vector])
    return values / mp.sqrt(sum(value ** 2 for value in values))


def cross(left, right):
    return mp.matrix([left[1] * right[2] - left[2] * right[1], left[2] * right[0] - left[0] * right[2], left[0] * right[1] - left[1] * right[0]])


def frame(direction):
    reference = mp.matrix([0, 0, 1]) if abs(direction[2]) < mp.mpf('.8') else mp.matrix([1, 0, 0])
    transverse = cross(direction, reference)
    transverse /= mp.sqrt(sum(value ** 2 for value in transverse))
    second = cross(direction, transverse)
    return [mp.matrix([0, *transverse]), mp.matrix([0, *second])]


def photon(energy, direction):
    return mp.matrix([energy, *[energy * value for value in direction]])


def event(energy, fraction, hard_direction, soft_direction):
    energy, fraction = mp.mpf(str(energy)), mp.mpf(str(fraction))
    directions = [mp.matrix([0, 0, 1]), unit(hard_direction), unit(soft_direction)]
    angle01 = 1 - sum(directions[0][index] * directions[1][index] for index in range(3))
    angle02 = 1 - sum(directions[0][index] * directions[2][index] for index in range(3))
    angle12 = 1 - sum(directions[1][index] * directions[2][index] for index in range(3))
    soft = energy * fraction
    denominator = 1 + energy * angle01 - soft * angle12
    hard = (energy - soft - energy * soft * angle02) / denominator
    assert hard > 0
    photons = [photon(energy, directions[0]), photon(hard, directions[1]), photon(soft, directions[2])]
    initial = mp.matrix([1, 0, 0, 0])
    final = add(initial, photons[0], -photons[1], -photons[2])
    assert abs(dot(final, final) - 1) < mp.mpf('1e-50')
    return dict(initial=initial, final=final, photons=photons, directions=directions,
        frames=[frame(direction) for direction in directions], denominator=denominator)


def electron_amplitude(initial, transfers, polarizations, omit=None):
    final = add(initial, *transfers)
    total = mp.zeros(4)
    for ordering in itertools.permutations(range(len(transfers))):
        if ordering == omit:
            continue
        matrix = slash(polarizations[ordering[0]])
        momentum = add(initial, transfers[ordering[0]])
        for location in ordering[1:]:
            matrix = slash(polarizations[location]) * propagator(momentum) * matrix
            momentum = add(momentum, transfers[location])
        total += matrix
    return spinors(final).transpose_conj() * gamma_matrices()[0] * total * spinors(initial)


def tensor_for_event(sample, ward=None, omit=None):
    photons = sample['photons']
    transfers = [photons[0], -photons[1], -photons[2]]
    amplitudes = np.empty((2, 2, 2, 2, 2), dtype=complex)
    for incoming, hard, soft in itertools.product(range(2), repeat=3):
        polarizations = [sample['frames'][index][state] for index, state in enumerate([incoming, hard, soft])]
        if ward is not None:
            polarizations[ward] = photons[ward] / photons[ward][0]
        matrix = electron_amplitude(sample['initial'], transfers, polarizations, omit)
        for outgoing_spin, incoming_spin in itertools.product(range(2), repeat=2):
            amplitudes[incoming, hard, soft, outgoing_spin, incoming_spin] = complex(matrix[outgoing_spin, incoming_spin])
    return amplitudes


def single_tensor(energy, hard_direction):
    energy = mp.mpf(str(energy))
    initial = mp.matrix([1, 0, 0, 0])
    directions = [mp.matrix([0, 0, 1]), unit(hard_direction)]
    hard = energy / (1 + energy * (1 - directions[1][2]))
    photons = [photon(energy, directions[0]), photon(hard, directions[1])]
    frames = [frame(direction) for direction in directions]
    amplitudes = np.empty((2, 2, 2, 2), dtype=complex)
    for incoming, outgoing in itertools.product(range(2), repeat=2):
        matrix = electron_amplitude(initial, [photons[0], -photons[1]], [frames[0][incoming], frames[1][outgoing]])
        for final_spin, initial_spin in itertools.product(range(2), repeat=2):
            amplitudes[incoming, outgoing, final_spin, initial_spin] = complex(matrix[final_spin, initial_spin])
    return amplitudes, add(initial, photons[0], -photons[1])
