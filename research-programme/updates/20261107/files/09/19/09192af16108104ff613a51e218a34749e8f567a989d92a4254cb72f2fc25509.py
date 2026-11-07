from leading_angular import *


def angular_coefficients(hard_direction, soft_direction):
    directions = [np.array([0., 0., 1.]), hard_direction, soft_direction]
    frames = np.array([reduced.frame(direction) for direction in directions])
    assert np.max(abs(frames[:, :, 0])) == 0
    vertices = np.array([[reduced.slash(polarization) for polarization in frame] for frame in frames])
    rays = [reduced.slash(np.r_[1., direction]) for direction in directions]
    initial = reduced.spinors(np.array([1., 0., 0., 0.]))
    final_left = initial.conj().T @ reduced.GAMMA[0]
    recoil_constant = directions[0] - directions[1]
    recoil_linear = directions[1] - directions[2]
    left, right = [], []
    for leg in range(3):
        right.append(.5 * rays[leg][None] @ vertices[leg] @ initial)
        constant = frames[leg, :, 1:] @ recoil_constant
        linear = frames[leg, :, 1:] @ recoil_linear
        coefficients = np.zeros((4, 2, 2, 4), dtype=complex)
        coefficients[0] = .5 * final_left[None] @ vertices[leg] @ rays[leg]
        if leg == 0:
            coefficients[0] += constant[:, None, None] * final_left
            coefficients[1] = linear[:, None, None] * final_left
        elif leg == 1:
            coefficients[0] += linear[:, None, None] * final_left
            coefficients[3] = -(constant + linear)[:, None, None] * final_left
        else:
            coefficients[0] -= linear[:, None, None] * final_left
            coefficients[2] = -constant[:, None, None] * final_left
        left.append(coefficients)
    result = np.zeros((4, 2, 2, 2, 2, 2), dtype=complex)
    for first, middle, last in itertools.permutations(range(3)):
        term = np.einsum('qafd,bde,cei->qabcfi', left[last], vertices[middle], right[first])
        ordering = [last, middle, first]
        result += term.transpose([0] + [ordering.index(leg) + 1 for leg in range(3)] + [4, 5])
    return result


def angular_gram(hard_direction, soft_direction):
    coefficients = angular_coefficients(hard_direction, soft_direction).reshape(4, -1)
    return (coefficients.conj() @ coefficients.T).real / 4


def fast_intensity(fraction, gram):
    fraction = np.atleast_1d(np.asarray(fraction))
    if np.any(fraction == 0) or np.any(fraction >= 1):
        raise ValueError('Signed fraction outside leading domain')
    terms = np.column_stack([np.ones_like(fraction), fraction, 1 / fraction, 1 / (1 - fraction)])
    result = np.einsum('ni,ij,nj->n', terms, gram, terms)
    assert np.isfinite(result).all() and np.min(result) >= 0
    return result
