from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_common_weighted_moments_20260920 import decimal_fraction
from annular_nonuniform_Gram_candidate_20260920 import template_rows
from derive_annular_nonuniform_Gram_atoms_20260920 import atom_responses
from decimal import Decimal
from fractions import Fraction
import numpy as np


ZERO = Decimal(0)


def add_scaled(target, source, scale):
    for column, value in source.items():
        target[column] = target.get(column, Fraction(0))+scale*value
    return {column:value for column, value in target.items() if value}


def atom_rows(mesh):
    edges = list(map(Fraction, mesh['edges']))
    slope_left, slope_right, curvature = [], [], []
    for cell, indices in enumerate(mesh['elements']):
        width = edges[cell+1]-edges[cell]
        rows = []
        for weights, denominator in [([-3, 4, -1], width), ([1, -4, 3], width), ([4, -8, 4], width**2)]:
            rows.append({column:Fraction(weight)/denominator for column, weight in zip(indices, weights) if column >= 0})
        slope_left.append(rows[0])
        slope_right.append(rows[1])
        curvature.append(rows[2])
    first, second = [], []
    for index, location in enumerate(edges[1:-1]):
        first.append({} if location == Fraction(mesh['anchor']) else add_scaled(dict(slope_left[index+1]), slope_right[index], -1))
        second.append(add_scaled(dict(curvature[index+1]), curvature[index], -1))
    return edges[1:-1], first, second


def gram_rows(mesh, knots, alternative=False):
    locations, slopes, curvatures = atom_rows(mesh)
    kernel = []
    for index in range(len(knots)-3):
        points = knots[index:index+4]
        width, responses = atom_responses(points, locations)
        row = {}
        for atom, first, second in responses:
            row = add_scaled(row, slopes[atom], first)
            row = add_scaled(row, curvatures[atom], second)
        scale = Decimal(1)/decimal_fraction(width).sqrt()
        if alternative:
            gaps = [last-first for first, last in zip(points, points[1:])]
            scale *= 1+decimal_fraction(sum((gap-width)**2 for gap in gaps)/sum(gap**2 for gap in gaps))
        kernel.append({column:decimal_fraction(value)*scale for column, value in row.items()})
    template, sampling = template_rows(len(knots))
    rows = []
    for index in range(template.shape[0]):
        row = {}
        for position in range(template.indptr[index], template.indptr[index+1]):
            scale = Decimal.from_float(float(template.data[position]))
            for column, value in kernel[template.indices[position]].items():
                row[column] = row.get(column, ZERO)+scale*value
        rows.append({column:value for column, value in row.items() if value})
    return rows, sampling


def gram_matrix(rows, weights, count):
    result = [{} for unused in range(count)]
    for row, weight in zip(rows, weights):
        for first, first_value in row.items():
            for last, last_value in row.items():
                result[first][last] = result[first].get(last, ZERO)+weight*(first_value*last_value)
    return result


def sum_rows(first, last):
    result = [dict(row) for row in first]
    for target, extra in zip(result, last):
        for column, value in extra.items():
            target[column] = target.get(column, ZERO)+value
    return result


def forms_from_moments(mesh, moments):
    names = ['mass', 'mass_X', 'gradient', 'gradient_X', 'transport', 'transport_X', 'inertia', 'inertia_X']
    result = {name:[{} for unused in range(mesh['count'])] for name in names}
    basis = [[1, -3, 2], [0, 4, -4], [0, -1, 2]]
    for cell, indices in enumerate(mesh['elements']):
        width = decimal_fraction(Fraction(mesh['edges'][cell+1])-Fraction(mesh['edges'][cell]))
        for first, row in enumerate(indices):
            if row < 0:
                continue
            for last, column in enumerate(indices):
                if column < 0:
                    continue
                for name in names:
                    first_degree = 0 if name.startswith(('mass', 'transport')) else 1
                    last_degree = 0 if name.startswith('mass') else 1
                    polynomial = [0]*5
                    for before in range(first_degree, 3):
                        for after in range(last_degree, 3):
                            coefficient = basis[first][before]*basis[last][after]
                            if first_degree:
                                coefficient *= before
                            if last_degree:
                                coefficient *= after
                            polynomial[before+after-first_degree-last_degree] += coefficient
                    value = sum((coefficient*moments[name][cell][degree]
                        for degree, coefficient in enumerate(polynomial)), ZERO)
                    value /= width**(first_degree+last_degree)
                    target = result[name][row]
                    target[column] = target.get(column, ZERO)+value
    return result


class FrozenCandidate:
    def __init__(self, packet):
        self.count = packet['count']
        self.maps = {name:MixedMap(item['rows'], item['columns']) for name, item in packet['maps'].items()}
        rows = [{int(column):Decimal(value) for column, value in row.items()} for row in packet['maps']['mass']['rows']]
        self.mass_rows = rows
        self.diagonal = np.array([rows[index][index] for index in range(self.count)], dtype=object)
        self.lower = np.full((self.count, 2), ZERO, dtype=object)
        for row in range(self.count):
            for column, value in rows[row].items():
                if abs(row-column) > 2 and value:
                    raise ValueError('Common P2 mass bandwidth exceeded.')
                if value != rows[column].get(row, ZERO):
                    raise ValueError('Common mass must be exactly symmetric.')
            for column in range(max(0, row-2), row):
                value = rows[row].get(column, ZERO)
                for inner in range(max(0, row-2, column-2), column):
                    value -= self.lower[row, row-inner-1]*self.diagonal[inner]*self.lower[column, column-inner-1]
                self.lower[row, row-column-1] = value/self.diagonal[column]
            self.diagonal[row] -= sum((self.lower[row, row-column-1]**2*self.diagonal[column]
                for column in range(max(0, row-2), row)), ZERO)
            if self.diagonal[row] <= 0:
                raise ValueError('Nonpositive mass pivot.')
        stiffness = [{int(column):Decimal(value) for column, value in row.items()} for row in packet['maps']['stiffness']['rows']]
        ratio = max(sum((abs(value) for column, value in row.items() if column != index), ZERO)/row[index]
            for index, row in enumerate(rows))
        if ratio >= 1:
            raise ValueError('Mass row-dominance frequency bound unavailable.')
        bound = max(sum(map(abs, row.values()), ZERO)/rows[index][index] for index, row in enumerate(stiffness))
        self.frequency_bound = (bound/(1-ratio)).sqrt()
        self.mass_jacobi_ratio = ratio
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
        return self.maps['stiffness'].apply(values)

    def acceleration(self, values, transpose=False):
        self.calls += values.shape[1]
        return self.stiffness(self.solve(values)) if transpose else self.solve(self.stiffness(values))


def source_force(action, position, velocity, source_velocity, dust_inertia, dust_drive):
    maps = action.maps
    applied = {name:mapping.apply(position[:, None])[:, 0] for name, mapping in maps.items()
        if name in ['stiffness', 'stiffness_X', 'transport', 'transport_X', 'inertia', 'inertia_X']}
    cross = -applied['transport']
    scalar_drive = -applied['stiffness']+source_velocity*(maps['transport'].apply(velocity[:, None])[:, 0]
        -maps['transport'].apply(velocity[:, None], True)[:, 0]-maps['mass_X'].apply(velocity[:, None])[:, 0])
    scalar_drive += source_velocity**2*(applied['inertia']+applied['transport_X'])
    partial = sum(velocity*maps['mass_X'].apply(velocity[:, None])[:, 0], ZERO)/2
    partial -= sum(position*applied['stiffness_X'], ZERO)/2
    partial -= source_velocity*sum(velocity*applied['transport_X'], ZERO)
    partial += source_velocity**2*sum(position*applied['inertia_X'], ZERO)/2
    source_drive = sum(velocity*maps['mass_X'].apply(velocity[:, None])[:, 0], ZERO)/2
    source_drive += sum(velocity*maps['transport'].apply(velocity[:, None])[:, 0], ZERO)
    source_drive -= 2*source_velocity*sum(velocity*applied['inertia'], ZERO)
    source_drive -= source_velocity**2*sum(position*applied['inertia_X'], ZERO)/2
    source_drive -= sum(position*applied['stiffness_X'], ZERO)/2
    solved = action.solve(np.column_stack([cross, scalar_drive]))
    complement = sum(position*applied['inertia'], ZERO)-sum(cross*solved[:, 0], ZERO)
    free_drive = source_drive-sum(cross*solved[:, 1], ZERO)
    denominator = dust_inertia+complement
    if denominator <= 0:
        raise ValueError('Nonpositive total source Schur complement.')
    acceleration = (dust_drive+free_drive)/denominator
    reduced = (dust_inertia*free_drive-complement*dust_drive)/denominator
    return dict(partial_wave_covector=partial, wave_source_drive=source_drive,
        free_wave_drive=free_drive, field_inertia_complement=complement,
        total_inertia=denominator, source_acceleration=acceleration, reduced_wave_force=reduced)
