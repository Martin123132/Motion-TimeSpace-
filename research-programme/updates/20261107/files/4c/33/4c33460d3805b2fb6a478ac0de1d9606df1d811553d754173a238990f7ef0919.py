from math import fsum
from decimal import Decimal, localcontext
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
    precise = getattr(tangent, 'precise_probe_mass_rate', None)
    if precise is None:
        precise = PreciseProbeMassRate(tangent.coordinate_rate)
        tangent.precise_probe_mass_rate = precise
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
        mass_rate = precise.values(radius) + tangent.velocity_responses[-1].values(radius)[0]
        pieces.append([float(measure @ (coefficient * mass_rate * (radius - 6)**power)) for power in range(3)])
        tangent.coordinate_rate.cache.clear()
    result = np.array([fsum(piece[power] for piece in pieces) for power in range(3)])
    return result, edges


def decimal_values(values):
    array = np.asarray(values)
    return np.array([Decimal.from_float(float(value)) for value in array.ravel()], dtype=object).reshape(array.shape)


class PreciseProbeMassRate:
    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.tables = {}
        for index in [len(coordinate.steps) - 2, len(coordinate.steps) - 1]:
            for sign in [-1, 1]:
                action = coordinate.actions[index, sign]
                self.tables[index, sign] = dict(
                    centres=decimal_values(action.solver.centers),
                    lengths=decimal_values(action.solver.lengths),
                    prefixes=decimal_values(coordinate.prefixes[index, sign]),
                    primitives=decimal_values(action.solution['primitives'][0]))
        self.max_sample_float_difference = 0.
        self.precision_sample_difference = 0.
        self.sample_checked = False

    def evaluate(self, radius, precision):
        with localcontext() as context:
            context.prec = precision
            positions = decimal_values(radius)
            differences = []
            for index in [len(self.coordinate.steps) - 2, len(self.coordinate.steps) - 1]:
                pair = []
                for sign in [-1, 1]:
                    action, table = self.coordinate.actions[index, sign], self.tables[index, sign]
                    selected = np.clip(np.searchsorted(action.solver.edges, radius, side='right') - 1, 0, len(action.solver.edges) - 2)
                    mapped = 2 * (positions - table['centres'][selected]) / table['lengths'][selected]
                    value = table['prefixes'][selected] + np.polynomial.chebyshev.chebval(
                        mapped, table['primitives'][selected].T, tensor=False)
                    pair.append(value)
                step = Decimal.from_float(float(self.coordinate.steps[index]))
                differences.append((pair[1] - pair[0]) / (2 * step))
            result = (4 * differences[1] - differences[0]) / 3
            return np.asarray(result, float)

    def values(self, radius):
        result = self.evaluate(radius, 60)
        if not self.sample_checked:
            subset = radius[::max(1, len(radius) // 17)]
            accurate = self.evaluate(subset, 60)
            extra = self.evaluate(subset, 80)
            original = self.coordinate.values(subset)[-1, 0]
            self.max_sample_float_difference = float(np.max(abs(accurate - original)))
            self.precision_sample_difference = float(np.max(abs(accurate - extra)))
            self.coordinate.cache.clear()
            self.sample_checked = True
        return result
