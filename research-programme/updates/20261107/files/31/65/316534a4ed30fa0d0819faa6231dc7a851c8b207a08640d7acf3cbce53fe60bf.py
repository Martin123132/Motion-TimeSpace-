from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_weighted_moments_20260920 import decimal_fraction
from decimal import Decimal
from fractions import Fraction
import numpy as np


ZERO = Decimal(0)


class MixedMap:
    def __init__(self, rows, columns):
        entries = [(row, int(column), Decimal(value)) for row, values in enumerate(rows)
            for column, value in sorted(values.items(), key=lambda item: int(item[0])) if Decimal(value)]
        self.shape = (len(rows), columns)
        self.rows = np.array([item[0] for item in entries], dtype=int)
        self.columns = np.array([item[1] for item in entries], dtype=int)
        self.values = np.array([item[2] for item in entries], dtype=object)

    def apply(self, values, transpose=False):
        rows, columns = (self.columns, self.rows) if transpose else (self.rows, self.columns)
        answer = np.full((self.shape[1] if transpose else self.shape[0], values.shape[1]), ZERO, dtype=object)
        np.add.at(answer, rows, self.values[:, None]*values[columns])
        return answer

    def serialize(self):
        rows = [{} for unused in range(self.shape[0])]
        for row, column, value in zip(self.rows, self.columns, self.values):
            rows[int(row)][str(int(column))] = str(value)
        return dict(rows=rows, columns=self.shape[1])


def cell_coefficients(indices, embedding):
    nodal = [{int(column): Fraction(value) for column, value in embedding[index].items()}
        if index >= 0 else {} for index in indices]
    columns = sorted(set().union(*(row.keys() for row in nodal)))
    result = {}
    for column in columns:
        left, middle, right = [row.get(column, Fraction(0)) for row in nodal]
        result[column] = [decimal_fraction(value) for value in
            [left, -3*left+4*middle-right, 2*left-4*middle+2*right]]
    return result


def assemble_mixed(packet, moments, fine_data):
    mesh = packet['overlay']
    count = packet['native'][1]['count']
    mass, gradient, gram = [[{} for unused in range(count)] for unused in range(3)]
    for cell, indices in enumerate(mesh['elements']):
        coarse = cell_coefficients(indices, packet['embeddings'][0])
        fine = cell_coefficients(indices, packet['embeddings'][1])
        width = decimal_fraction(Fraction(mesh['edges'][cell+1])-Fraction(mesh['edges'][cell]))
        for row, test in fine.items():
            for column, trial in coarse.items():
                value = sum((test[first]*trial[last]*moments['fine_mass'][cell][first+last]
                    for first in range(3) for last in range(3)), ZERO)
                derivative = sum((first*last*test[first]*trial[last]*moments['fine_gradient'][cell][first+last-2]/width**2
                    for first in [1, 2] for last in [1, 2]), ZERO)
                mass[row][column] = mass[row].get(column, ZERO)+value
                gradient[row][column] = gradient[row].get(column, ZERO)+derivative
    from annular_common_P2_overlay_20260919 import compose_rows
    restrictions = [{int(column): Fraction(value) for column, value in row.items()} for row in packet['left_inverses'][1]]
    embeddings = [{int(column): Fraction(value) for column, value in row.items()} for row in packet['embeddings'][0]]
    canonical = compose_rows(restrictions, embeddings)
    pointers, columns = fine_data['gram_indptr'], fine_data['gram_indices']
    coefficients = [Decimal.from_float(float(value)) for value in fine_data['gram_data']]
    for factor, weight in enumerate(fine_data['gram_weights']):
        weight = Decimal.from_float(float(weight))
        test = {int(columns[index]): coefficients[index] for index in range(pointers[factor], pointers[factor+1])}
        trial = {}
        for inner, value in test.items():
            for column, rational in canonical[inner].items():
                trial[column] = trial.get(column, ZERO)+value*decimal_fraction(rational)
        for row, first in test.items():
            for column, last in trial.items():
                gram[row][column] = gram[row].get(column, ZERO)+weight*first*last
    return {name: MixedMap(rows, packet['native'][0]['count'])
        for name, rows in [('mass', mass), ('gradient', gradient), ('gram', gram)]}


def stiffness_apply(maps, values, transpose=False):
    return maps['gradient'].apply(values, transpose)+maps['gram'].apply(values, transpose)
