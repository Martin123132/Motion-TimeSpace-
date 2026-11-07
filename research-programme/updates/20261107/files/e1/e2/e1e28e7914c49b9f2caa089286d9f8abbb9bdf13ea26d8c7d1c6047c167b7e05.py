from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_weighted_moments_20260920 import decimal_fraction
from decimal import Decimal, localcontext
from fractions import Fraction
from bisect import bisect_left, bisect_right
import numpy as np


ZERO = Decimal(0)
ONE = Decimal(1)


def dec(values):
    return np.array([Decimal.from_float(float(value)) for value in np.asarray(values).ravel()], dtype=object).reshape(np.shape(values))


def apply_rows(rows, values):
    result = np.full((len(rows), values.shape[1]), ZERO, dtype=object)
    for index, row in enumerate(rows):
        for column, coefficient in row.items():
            result[index] += coefficient * values[column]
    return result


class ActualPullback:
    def __init__(self, mesh):
        self.edges = [decimal_fraction(Fraction(value)) for value in mesh['edges']]
        self.nodes = [decimal_fraction(Fraction(value)) for value in mesh['nodes']]
        self.elements = mesh['elements']
        self.anchor = decimal_fraction(Fraction(mesh['anchor']))
        self.widths = [upper - lower for lower, upper in zip(self.edges[:-1], self.edges[1:])]
        self.sides = []
        self.local_width = []
        for node in self.nodes:
            left = max(0, min(len(self.widths) - 1, bisect_left(self.edges, node) - 1))
            right = max(0, min(len(self.widths) - 1, bisect_right(self.edges, node) - 1))
            self.sides.append((left, right))
            self.local_width.append(min(self.widths[left], self.widths[right]))

    def row(self, position, cell, derivative=0):
        width = self.widths[cell]
        local = (position - self.edges[cell]) / width
        if derivative == 0:
            values = [(1 - local) * (1 - 2 * local), 4 * local * (1 - local), local * (2 * local - 1)]
        elif derivative == 1:
            values = [(4 * local - 3) / width, (4 - 8 * local) / width, (4 * local - 1) / width]
        else:
            values = [4 / width**2, -8 / width**2, 4 / width**2]
        return {column: value for column, value in zip(self.elements[cell], values) if column >= 0 and value}

    def rows(self, amount, speed):
        rows, derivatives = [], []
        for index, (node, velocity) in enumerate(zip(self.nodes, speed)):
            position = node + amount * velocity
            cell = max(0, min(len(self.widths) - 1, bisect_right(self.edges, position) - 1))
            if not self.edges[0] <= position <= self.edges[-1]:
                raise ValueError('Pullback left physical domain')
            if (node < self.anchor) != (position < self.anchor):
                raise ValueError('Pullback crossed pinned source')
            rows.append(self.row(position, cell))
            derivatives.append({column: velocity * value for column, value in self.row(position, cell, 1).items()})
            if any(abs(column - index) > 2 for column in rows[-1]):
                raise ValueError('Step crossed local band support')
        return rows, derivatives

    def generators(self, speed):
        output = []
        for sign in [1, -1]:
            rows, curvatures = [], []
            for index, (node, velocity) in enumerate(zip(self.nodes, speed)):
                cell = self.sides[index][1 if sign * velocity >= 0 else 0]
                rows.append({column: velocity * value for column, value in self.row(node, cell, 1).items()})
                curvatures.append({column: velocity**2 * value / 2 for column, value in self.row(node, cell, 2).items()})
            output.append((rows, curvatures))
        return output

    def safe_step(self, speed, eta_slope):
        bound = min((width / abs(value) for width, value in zip(self.local_width, speed) if value), default=ONE)
        strain = max(map(abs, eta_slope), default=ZERO)
        if strain:
            bound = min(bound, ONE / strain)
        return Decimal('0.02') * bound


class DecimalBandSolve:
    def __init__(self, rows):
        self.rows = [dict(row) for row in rows]
        self.margin = min(abs(row.get(index, ZERO)) - sum((abs(value) for column, value in row.items() if column != index), ZERO)
                          for index, row in enumerate(rows))
        if self.margin <= 0:
            raise ValueError('Pullback strict row diagonal dominance lost')
        for pivot, row in enumerate(self.rows):
            if row.get(pivot, ZERO) == 0:
                raise ValueError('Zero pullback pivot')
            for target in range(pivot + 1, min(len(rows), pivot + 3)):
                lower = self.rows[target].get(pivot, ZERO)
                if not lower:
                    continue
                multiplier = lower / row[pivot]
                self.rows[target][pivot] = multiplier
                for column, value in row.items():
                    if column > pivot:
                        self.rows[target][column] = self.rows[target].get(column, ZERO) - multiplier * value

    def solve(self, values):
        result = values.copy()
        for index, row in enumerate(self.rows):
            for column, coefficient in row.items():
                if column < index:
                    result[index] -= coefficient * result[column]
        for index in range(len(self.rows) - 1, -1, -1):
            for column, coefficient in self.rows[index].items():
                if column > index:
                    result[index] -= coefficient * result[column]
            result[index] /= self.rows[index][index]
        return result


def max_abs(values):
    return max(map(abs, np.asarray(values).ravel()), default=ZERO)


def quadratic(weight, image):
    return sum((coefficient * value**2 / 2 for coefficient, value in zip(weight, image)), ZERO)


def packed_rows(rows):
    indices = np.full((len(rows), 3), -1, dtype=int)
    values = np.full((len(rows), 3), '0', dtype='<U96')
    for index, row in enumerate(rows):
        for offset, (column, value) in enumerate(sorted(row.items())):
            indices[index, offset] = column
            values[index, offset] = str(value)
    return indices, values
