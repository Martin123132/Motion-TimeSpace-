from derive_annular_source_gravity_20260914 import EvidenceRun
import numpy as np


def metric_at_offset(solver, solution, radius_offset, anchor, second=False):
    offsets = np.asarray(radius_offset)
    edges = solver.edges-anchor
    indices = np.clip(np.searchsorted(edges, offsets.real, side='right')-1, 0, len(edges)-2)
    centers = solver.centers-anchor
    coordinate = 2*(offsets-centers[indices])/solver.lengths[indices]
    if second:
        return np.array([np.polynomial.chebyshev.chebval(coordinate,
            np.polynomial.chebyshev.chebder(values[indices].T, axis=0), tensor=False)
            *2/solver.lengths[indices] for values in solution['rhs_coefficients']])
    values = np.array([solution['left'][component, indices]+np.polynomial.chebyshev.chebval(coordinate,
        solution['primitives'][component, indices].T, tensor=False) for component in range(2)])
    radial = np.array([np.polynomial.chebyshev.chebval(coordinate,
        solution['rhs_coefficients'][component, indices].T, tensor=False) for component in range(2)])
    return values, radial


def response_at_offset(response, radius_offset, anchor):
    responses = getattr(response, 'responses', (response,))
    pairs = [metric_at_offset(item.solver, item.solution, radius_offset, anchor) for item in responses]
    return tuple(sum(pair[index] for pair in pairs) for index in range(2))
