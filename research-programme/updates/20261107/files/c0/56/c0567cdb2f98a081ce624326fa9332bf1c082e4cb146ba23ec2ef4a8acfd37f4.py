from rectangular_common import *
from nonlocal_dc import gould
from resolved_redistribution import incoming_rule


def log_nodes(order, lower, upper):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    halfwidth = .5 * math.log(upper / lower)
    frequency = np.exp(.5 * math.log(upper * lower) + halfwidth * nodes)
    return frequency, halfwidth * weights * frequency


def overlap(spectra, tests, theta, seed_order, soft_order, floor=1e-6, seed_maximum=24., joined=True, inverse=False):
    result = np.zeros((spectra.basis.count + 2, 4))
    absolute = np.zeros_like(result)
    maximum_null = 0.
    physical_coefficients = np.repeat(np.column_stack([spectra.original['heavy'], spectra.original['cold']]), 2, axis=1)
    for anchor, seed_weight in incoming_rule(seed_order, 1e-5, seed_maximum):
        soft_upper = anchor if inverse else anchor / 2
        if soft_upper <= floor:
            continue
        boundaries = sorted({floor, soft_upper, *[value for value in [5e-5, 1e-4, 2e-4, .01, .1, 1.] if floor < value < soft_upper]})
        for lower, upper in zip(boundaries[:-1], boundaries[1:]):
            soft, soft_weights = log_nodes(soft_order, lower, upper)
            hard = np.full_like(soft, anchor) if inverse else anchor - soft
            seed = hard + soft if inverse else np.full_like(soft, anchor)
            left = tests.evaluate(soft) + tests.evaluate(hard) - tests.evaluate(seed)
            left[:, 0] = 0.
            left[:, 1] = 1 / spectra.basis.norms[0]
            left[:, 2] = -spectra.basis.mean / spectra.basis.norms[1]
            if joined:
                right = spectra.functions(soft)[:, 1:] + spectra.functions(hard)[:, 1:] - spectra.functions(seed)[:, 1:]
            else:
                right = left[:, 1:] @ physical_coefficients
            density = seed_weight * soft_weights * seed**4 * gould(soft / seed)
            density /= (np.expm1(seed) * (-np.expm1(-hard)) * (-np.expm1(-soft)) * soft)
            density *= 4 * weak.source.ALPHA * theta**2 / (3 * np.pi * I3)
            product = np.einsum('ni,nj->nij', left, right)
            result[:-1] -= np.einsum('n,nij->ij', density, product)
            absolute[:-1] += np.einsum('n,nij->ij', density, abs(product))
            maximum_null = max(maximum_null, float(np.max(abs(left[:, 1:] @ spectra.basis.temperature))))
    return result, dict(maximum_temperature_null=maximum_null, absolute_quadrature_sum=absolute.tolist())
