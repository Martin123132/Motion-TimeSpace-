import itertools
from remainder_common import *
from batched_real import reduced


def leading_tensor(fraction, hard_direction, soft_direction):
    fraction = np.atleast_1d(np.asarray(fraction, dtype=float))
    if np.any(fraction == 0) or np.any(fraction >= 1):
        raise ValueError('Signed fraction must be nonzero and leave positive hard energy')
    count = len(fraction)
    photons = np.empty((count, 3, 4))
    photons[:, 0] = np.array([1., 0., 0., 1.])
    photons[:, 1] = (1 - fraction[:, None]) * np.r_[1., hard_direction]
    photons[:, 2] = fraction[:, None] * np.r_[1., soft_direction]
    recoil = photons[:, 0, 1:] - photons[:, 1, 1:] - photons[:, 2, 1:]
    frames = np.array([reduced.frame(np.array([0., 0., 1.])),
                       reduced.frame(hard_direction), reduced.frame(soft_direction)])
    assert np.max(abs(frames[:, :, 0])) == 0
    vertices = np.array([[reduced.slash(polarization) for polarization in frame] for frame in frames])
    transfers = photons * np.array([1, -1, -1])[None, :, None]
    slashes = np.einsum('nla,aij->nlij', transfers * np.array([1, -1, -1, -1]), reduced.GAMMA)
    initial = reduced.spinors(np.array([1., 0., 0., 0.]))
    final_left = initial.conj().T @ reduced.GAMMA[0]
    left, right = [], []
    for leg in range(3):
        right.append((slashes[:, leg, None] @ vertices[leg][None] @ initial) /
                     (2 * transfers[:, leg, 0, None, None, None]))
        dot_pol = -recoil @ frames[leg, :, 1:].T
        numerator = 2 * dot_pol[:, :, None, None] * reduced.IDENTITY - vertices[leg][None] @ slashes[:, leg, None]
        left.append((final_left[None, None] @ numerator) /
                    (-2 * transfers[:, leg, 0, None, None, None]))
    result = np.zeros((count, 2, 2, 2, 2, 2), complex)
    for first, middle, last in itertools.permutations(range(3)):
        term = np.einsum('nafd,bde,ncei->nabcfi', left[last], vertices[middle], right[first])
        ordering = [last, middle, first]
        result += term.transpose([0] + [ordering.index(leg) + 1 for leg in range(3)] + [4, 5])
    return result


def leading_intensity(fraction, hard_direction, soft_direction):
    amplitude = leading_tensor(fraction, hard_direction, soft_direction)
    return np.sum(abs(amplitude)**2, axis=(1, 2, 3, 4, 5)) / 4
