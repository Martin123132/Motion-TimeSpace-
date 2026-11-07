from gould_angles import *


def equilibrium_data(frequencies):
    occupations = 1 / np.expm1(frequencies)
    weights = occupations * (1 + occupations)
    forward = occupations[:, 0] * (1 + occupations[:, 1]) * (1 + occupations[:, 2])
    return occupations, weights, forward


def mixed_coefficients(frequencies, background):
    occupations, weights, forward = equilibrium_data(frequencies)
    shifts = weights * background
    return weights * np.column_stack([shifts[:, 1] + shifts[:, 2], shifts[:, 0] - shifts[:, 2],
                                     shifts[:, 0] - shifts[:, 1]]) / forward[:, None]


def event_rule(basis, total_order, fraction_order):
    total_nodes, total_weights = np.polynomial.legendre.leggauss(total_order)
    lower, upper = math.log(2 * basis.minimum), math.log(basis.maximum)
    totals = np.exp(.5 * (lower + upper) + .5 * (upper - lower) * total_nodes)
    total_weights = total_weights * .5 * (upper - lower) * totals
    fraction_nodes, fraction_weights = np.polynomial.legendre.leggauss(fraction_order)
    for total, total_weight in zip(totals, total_weights):
        lower, upper = math.log(basis.minimum / total), math.log(.5)
        fractions = np.exp(.5 * (lower + upper) + .5 * (upper - lower) * fraction_nodes)
        share_weights = fraction_weights * .5 * (upper - lower) * fractions
        frequencies = np.column_stack([np.full_like(fractions, total), total * (1 - fractions), total * fractions])
        product = fractions * (1 - fractions)
        gould = (1 - 3 * product + 1.5 * product ** 2 - product ** 3) / (1 - fractions)
        occupations, weights, forward = equilibrium_data(frequencies)
        measure = total_weight * share_weights * total ** 4 / (I3 * fractions) * gould * forward
        yield frequencies, fractions, measure, np.stack([basis.evaluate(frequencies[:, index]) for index in range(3)], axis=1)


def mixed_blocks(basis, profile, total_order=300, fraction_order=180, maximum=4):
    blocks = [np.zeros_like(basis.mass) for degree in range(maximum + 1)]
    signs = np.array([1., -1., -1.])
    for frequencies, fractions, measure, values in event_rule(basis, total_order, fraction_order):
        background = np.einsum('nik,k->ni', values, profile)
        coefficients = mixed_coefficients(frequencies, background)
        difference = values[:, 0] - values[:, 1] - values[:, 2]
        difference[:, 0] = -1 / basis.norms[0]
        difference[:, 1] = basis.mean / basis.norms[1]
        right = np.einsum('ni,nik->nk', coefficients, values)
        blocks[0] -= (difference.T * measure) @ right
        for degree in range(1, maximum + 1):
            hard, incoming, outgoing = correlations(fractions, degree)
            gram = np.broadcast_to(np.eye(3), (len(fractions), 3, 3)).copy()
            gram[:, 0, 1] = gram[:, 1, 0] = hard
            gram[:, 0, 2] = gram[:, 2, 0] = incoming
            gram[:, 1, 2] = gram[:, 2, 1] = outgoing
            for incident in range(3):
                coupled = np.einsum('ni,nik->nk', gram[:, incident] * coefficients, values)
                blocks[degree] -= (values[:, incident].T * (measure * signs[incident] / (2 * degree + 1))) @ coupled
    return blocks
