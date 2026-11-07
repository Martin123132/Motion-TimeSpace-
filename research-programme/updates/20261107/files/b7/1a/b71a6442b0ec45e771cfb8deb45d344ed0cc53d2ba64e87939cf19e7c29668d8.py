from math import fsum
import numpy as np


def union_grid(action, tangent):
    arrays = [action.solver.edges]
    arrays.extend(probe.solver.edges for probe in tangent.coordinate_rate.actions.values())
    arrays.extend(response.solver.edges for response in tangent.velocity_responses)
    lower, upper = action.solver.edges[[0, -1]]
    combined = np.unique(np.concatenate(arrays))
    return combined[(combined >= lower) & (combined <= upper)]


def gravity_on_union(action, tangent, order):
    edges = union_grid(action, tangent)
    points, weights = np.polynomial.legendre.leggauss(order)
    pieces = []
    tangent.coordinate_rate.cache.clear()
    for start in range(0, len(edges) - 1, 128):
        section = edges[start:min(start + 128, len(edges) - 1) + 1]
        lengths = np.diff(section)
        centres = section[:-1] + lengths / 2
        radius = (centres[:, None] + lengths[:, None] * points / 2).ravel()
        measure = (lengths[:, None] * weights / 2).ravel()
        values = action.solver.values(action.solution, radius)[0]
        metric = 1 - 2 * values[0] / radius
        coefficient = np.exp(values[1]) / (action.owner.coupling * np.sqrt(metric))
        mass_rate = tangent.values(radius)[-1, 0]
        pieces.append([float(measure @ (coefficient * mass_rate * (radius - 6)**power)) for power in range(3)])
        tangent.coordinate_rate.cache.clear()
    result = np.array([fsum(piece[power] for piece in pieces) for power in range(3)])
    return result, edges
