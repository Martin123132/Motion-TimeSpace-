from derive_annular_source_gravity_20260914 import EvidenceRun
from decimal import Decimal, getcontext
from time import perf_counter
import numpy as np


ZERO = Decimal(0)
ONE = Decimal(1)


def decimal_array(values):
    values = np.asarray(values)
    return np.array([Decimal.from_float(float(value)) for value in values.flat], dtype=object).reshape(values.shape)


def zero_array(shape):
    return np.full(shape, ZERO, dtype=object)


def dot(first, last):
    return sum((first*last).flat, ZERO)


class DecimalMap:
    def __init__(self, matrix):
        source = matrix.tocsr()
        self.shape = source.shape
        self.rows = np.repeat(np.arange(source.shape[0]), np.diff(source.indptr))
        self.columns = source.indices.copy()
        self.values = decimal_array(source.data)

    def apply(self, values, transpose=False):
        rows, columns = (self.columns, self.rows) if transpose else (self.rows, self.columns)
        count = self.shape[1] if transpose else self.shape[0]
        result = zero_array((count, values.shape[1]))
        np.add.at(result, rows, self.values[:, None]*values[columns])
        return result


class DecimalAction:
    def __init__(self, data):
        self.count = data['mass_bands'].shape[1]
        self.bands = decimal_array(data['mass_bands'])
        self.diagonal = self.bands[2].copy()
        self.lower = zero_array((self.count, 2))
        for column in range(self.count):
            for offset in [1, 2]:
                row = column+offset
                if row < self.count and self.bands[2+offset, column] != self.bands[2-offset, row]:
                    raise ValueError('Saved mass is not exactly symmetric.')
        for row in range(self.count):
            for column in range(max(0, row-2), row):
                value = self.bands[2+row-column, column]
                for inner in range(max(0, row-2, column-2), column):
                    value -= self.lower[row, row-inner-1]*self.diagonal[inner]*self.lower[column, column-inner-1]
                self.lower[row, row-column-1] = value/self.diagonal[column]
            self.diagonal[row] -= sum((self.lower[row, row-column-1]**2*self.diagonal[column]
                for column in range(max(0, row-2), row)), ZERO)
            if self.diagonal[row] <= 0:
                raise ValueError('Positive mass LDL pivot required.')
        entries = [dict() for unused in range(self.count)]
        for name in ['gradient', 'gram']:
            indices, pointers = data[name+'_indices'], data[name+'_indptr']
            values, weights = decimal_array(data[name+'_data']), decimal_array(data[name+'_weights'])
            for factor_row, weight in enumerate(weights):
                for first in range(pointers[factor_row], pointers[factor_row+1]):
                    row = int(indices[first])
                    for last in range(pointers[factor_row], pointers[factor_row+1]):
                        column = int(indices[last])
                        entries[row][column] = entries[row].get(column, ZERO)+values[first]*weight*values[last]
        self.rows = np.array([row for row, entries_row in enumerate(entries) for column in sorted(entries_row)])
        self.columns = np.array([column for entries_row in entries for column in sorted(entries_row)])
        self.values = np.array([entries_row[column] for entries_row in entries for column in sorted(entries_row)], dtype=object)
        self.starts = np.flatnonzero(np.r_[True, np.diff(self.rows) != 0])
        self.active_rows = self.rows[self.starts]
        ratios, row_bounds = [], []
        for row, entries_row in enumerate(entries):
            diagonal = self.bands[2, row]
            offsum = sum((abs(self.bands[2+row-column, column])
                for column in range(max(0, row-2), min(self.count, row+3)) if column != row), ZERO)
            ratios.append(offsum/diagonal)
            row_bounds.append(sum(map(abs, entries_row.values()), ZERO)/diagonal)
        self.jacobi_ratio = max(ratios)
        if self.jacobi_ratio >= ONE:
            raise ValueError('Strict mass Jacobi contraction needed for scaling bound.')
        self.frequency_bound = (max(row_bounds)/(ONE-self.jacobi_ratio)).sqrt()
        self.calls = 0

    def solve(self, values):
        answer = values.copy()
        for row in range(self.count):
            for offset in [1, 2]:
                if row >= offset:
                    answer[row] -= self.lower[row, offset-1]*answer[row-offset]
        answer /= self.diagonal[:, None]
        for row in range(self.count-1, -1, -1):
            for offset in [1, 2]:
                if row+offset < self.count:
                    answer[row] -= self.lower[row+offset, offset-1]*answer[row+offset]
        return answer

    def stiffness(self, values):
        result = zero_array(values.shape)
        result[self.active_rows] = np.add.reduceat(self.values[:, None]*values[self.columns], self.starts, axis=0)
        return result

    def acceleration(self, values, transpose=False):
        self.calls += values.shape[1]
        return self.stiffness(self.solve(values)) if transpose else self.solve(self.stiffness(values))


def propagate(action, phase, duration, degree, transpose=False, increment=False, progress=None, deadline=None):
    scale = action.frequency_bound
    steps = max(1, int((abs(duration)*scale/Decimal(4)).to_integral_value(rounding='ROUND_CEILING')))
    step = duration/steps
    original = phase.copy()
    if transpose:
        original[0] /= scale
    else:
        original[0] *= scale

    def generator(values):
        result = zero_array(values.shape)
        if transpose:
            result[0] = -action.acceleration(values[1], True)/scale
            result[1] = scale*values[0]
        else:
            result[0] = scale*values[1]
            result[1] = -action.acceleration(values[0])/scale
        return result

    total = zero_array(phase.shape) if increment else original.copy()
    constant = generator(original) if increment else None
    maximum_last_term = ZERO
    for index in range(steps):
        if deadline is not None and perf_counter() > deadline:
            raise RuntimeError('Safe wall-time boundary; existing saved results retained.')
        term = step*(generator(total)+constant) if increment else step*generator(total)
        updated = total+term
        for order in range(2, degree+1):
            term = (step/Decimal(order))*generator(term)
            updated += term
        maximum_last_term = max(maximum_last_term, max(map(abs, term.flat)))
        total = updated
        if progress is not None and (index+1 == steps or (index+1) % 8 == 0):
            progress(index+1, steps)
    if transpose:
        total[0] *= scale
    else:
        total[0] /= scale
    return total, dict(substeps=steps, degree=degree, digits=getcontext().prec,
        maximum_scaled_last_term=str(maximum_last_term), scalar_action_products=action.calls)
