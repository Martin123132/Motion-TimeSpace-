import itertools
from outer_common import *
from batched_real import reduced, tensor_batch


def angular_basis(hard_direction, soft_direction):
    directions = np.array([[0., 0., 1.], hard_direction, soft_direction])
    frames = np.array([reduced.frame(direction) for direction in directions])
    vertices = np.array([[reduced.slash(polarization) for polarization in frame] for frame in frames])
    rays = np.array([reduced.slash(np.r_[1., direction]) for direction in directions])
    initial = reduced.spinors(np.array([1., 0., 0., 0.]))
    right = [.5 * rays[leg][None] @ vertices[leg] @ initial for leg in range(3)]
    labels = [(leg, other) for leg in range(3) for other in [-1, *[entry for entry in range(3) if entry != leg]]]
    basis = np.zeros((9, 2, 2, 2, 4, 2), dtype=complex)
    for first, middle, last in itertools.permutations(range(3)):
        ordering = [last, middle, first]
        transpose = [ordering.index(leg) for leg in range(3)] + [3, 4]
        left = .5 * vertices[last] @ rays[last]
        product = np.einsum('ade,bef,cfi->abcdi', left, vertices[middle], right[first])
        basis[labels.index((last, -1))] += product.transpose(transpose)
        for other in range(3):
            if other != last:
                scalar = frames[last, :, 1:] @ directions[other]
                product = np.einsum('a,bde,cei->abcdi', scalar, vertices[middle], right[first])
                basis[labels.index((last, other))] += product.transpose(transpose)
    operators = [reduced.GAMMA[0], *[reduced.GAMMA[0] @ matrix for matrix in reduced.GAMMA]]
    grams = np.array([np.einsum('iabcds,de,jabces->ij', basis.conj(), operator, basis).real / 4 for operator in operators])
    return dict(basis=basis, grams=grams, labels=labels, directions=directions)


def kinematics(energy, soft, hard_direction, soft_direction):
    soft = np.atleast_1d(np.asarray(soft, dtype=float))
    denominator = 1 + energy * (1 - hard_direction[2]) - soft * (1 - hard_direction @ soft_direction)
    hard = (energy - soft - energy * soft * (1 - soft_direction[2])) / denominator
    if np.any(hard <= 0) or np.any(denominator <= 0) or np.any(soft == 0):
        raise ValueError('Unphysical exact factorized event')
    photons = np.empty((len(soft), 3, 4))
    photons[:, 0] = np.array([energy, 0., 0., energy])
    photons[:, 1] = hard[:, None] * np.r_[1., hard_direction]
    photons[:, 2] = soft[:, None] * np.r_[1., soft_direction]
    recoil = photons[:, 0, 1:] - photons[:, 1, 1:] - photons[:, 2, 1:]
    final = np.column_stack([np.sqrt(1 + np.sum(recoil**2, axis=1)), recoil])
    transfers = np.column_stack([np.full(len(soft), energy), -hard, -soft])
    return photons, final, hard, denominator, transfers


def coefficients(final, transfers, angular):
    denominators = final[:, :1] - final[:, 1:] @ angular['directions'].T
    assert np.min(denominators) > 0
    return np.column_stack([1 / denominators[:, leg] if other == -1 else
        transfers[:, other] / (transfers[:, leg] * denominators[:, leg]) for leg, other in angular['labels']])


def factorized_intensity(energy, soft, hard_direction, soft_direction, angular):
    photons, final, hard, denominator, transfers = kinematics(energy, soft, hard_direction, soft_direction)
    factors = coefficients(final, transfers, angular)
    contractions = np.einsum('ni,pij,nj->np', factors, angular['grams'], factors)
    spin_weights = np.column_stack([np.ones(len(final)), final[:, 0], -final[:, 1:]])
    intensity = np.sum(contractions * spin_weights, axis=1)
    assert np.isfinite(intensity).all() and np.min(intensity) > 0
    return intensity, photons, final, hard, denominator


def factorized_tensor(energy, soft, hard_direction, soft_direction, angular):
    photons, final, hard, denominator, transfers = kinematics(energy, soft, hard_direction, soft_direction)
    factors = coefficients(final, transfers, angular)
    kernel = np.einsum('nq,qabcdi->nabcdi', factors, angular['basis'])
    final_left = np.array([reduced.spinors(momentum).conj().T @ reduced.GAMMA[0] for momentum in final])
    return np.einsum('nfd,nabcdi->nabcfi', final_left, kernel)
