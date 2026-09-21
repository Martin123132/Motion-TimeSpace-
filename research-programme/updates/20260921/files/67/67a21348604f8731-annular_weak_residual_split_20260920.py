from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_mixed_weak_maps_20260920 import MixedMap, cell_coefficients
from annular_common_weighted_moments_20260920 import decimal_fraction
from annular_common_P2_overlay_20260919 import compose_rows
from decimal import Decimal
from fractions import Fraction


ZERO = Decimal(0)


def rows_of(mapping):
    rows = [{} for unused in range(mapping.shape[0])]
    for row, column, value in zip(mapping.rows, mapping.columns, mapping.values):
        rows[int(row)][int(column)] = value
    return rows


def transpose_map(mapping):
    rows = [{} for unused in range(mapping.shape[1])]
    for row, column, value in zip(mapping.rows, mapping.columns, mapping.values):
        rows[int(column)][int(row)] = value
    return MixedMap(rows, mapping.shape[0])


def combine(*terms):
    shape = terms[0][1].shape
    rows = [{} for unused in range(shape[0])]
    for coefficient, mapping in terms:
        if mapping.shape != shape:
            raise ValueError('Matrix shapes differ in split.')
        for row, column, value in zip(mapping.rows, mapping.columns, mapping.values):
            row, column = int(row), int(column)
            rows[row][column] = rows[row].get(column, ZERO)+coefficient*value
    return MixedMap(rows, shape[1])


def multiply(first, last):
    if first.shape[1] != last.shape[0]:
        raise ValueError('Matrix product shapes differ.')
    rows = [{} for unused in range(first.shape[0])]
    right = rows_of(last)
    for row, inner, value in zip(first.rows, first.columns, first.values):
        row, inner = int(row), int(inner)
        for column, coefficient in right[inner].items():
            rows[row][column] = rows[row].get(column, ZERO)+value*coefficient
    return MixedMap(rows, last.shape[1])


def rational_composition(first, last, columns):
    first = [{int(column): Fraction(value) for column, value in row.items()} for row in first]
    last = [{int(column): Fraction(value) for column, value in row.items()} for row in last]
    return MixedMap([{column: decimal_fraction(value) for column, value in row.items()}
        for row in compose_rows(first, last)], columns)


def native_factor(data, name):
    count = data['mass_bands'].shape[1]
    rows = [{} for unused in range(count)]
    pointers, columns = data[name+'_indptr'], data[name+'_indices']
    values = [Decimal.from_float(float(value)) for value in data[name+'_data']]
    for factor, weight in enumerate(data[name+'_weights']):
        weight = Decimal.from_float(float(weight))
        indices = range(pointers[factor], pointers[factor+1])
        for first in indices:
            row = int(columns[first])
            for last in indices:
                column = int(columns[last])
                rows[row][column] = rows[row].get(column, ZERO)+values[first]*weight*values[last]
    return MixedMap(rows, count)


def native_mass(action):
    rows = [{} for unused in range(action.count)]
    for row in range(action.count):
        rows[row][row] = action.bands[2, row]
        for offset in [1, 2]:
            if row+offset < action.count:
                rows[row+offset][row] = action.bands[2+offset, row]
                rows[row][row+offset] = action.bands[2+offset, row]
    return MixedMap(rows, action.count)


def weighted_forms(packet, moments, test_level):
    mesh = packet['overlay']
    rows_mass, rows_gradient = [[{} for unused in range(packet['native'][test_level]['count'])] for unused in range(2)]
    for cell, indices in enumerate(mesh['elements']):
        test = cell_coefficients(indices, packet['embeddings'][test_level])
        trial = cell_coefficients(indices, packet['embeddings'][0])
        width = decimal_fraction(Fraction(mesh['edges'][cell+1])-Fraction(mesh['edges'][cell]))
        for row, first in test.items():
            for column, last in trial.items():
                mass = sum((first[before]*last[after]*moments['coarse_mass'][cell, before+after]
                    for before in range(3) for after in range(3)), ZERO)
                gradient = sum((before*after*first[before]*last[after]*moments['coarse_gradient'][cell, before+after-2]/width**2
                    for before in [1, 2] for after in [1, 2]), ZERO)
                rows_mass[row][column] = rows_mass[row].get(column, ZERO)+mass
                rows_gradient[row][column] = rows_gradient[row].get(column, ZERO)+gradient
    return MixedMap(rows_mass, packet['native'][0]['count']), MixedMap(rows_gradient, packet['native'][0]['count'])


def build_split(packet, moments, coarse_action, coarse_data, fine_data, counter_weights, fine_maps):
    coarse_test = rational_composition(packet['left_inverses'][0], packet['embeddings'][1], packet['native'][1]['count'])
    coarse_test_transpose = transpose_map(coarse_test)
    canonical_trial = rational_composition(packet['left_inverses'][1], packet['embeddings'][0], packet['native'][0]['count'])
    mixed_mass, mixed_gradient = weighted_forms(packet, moments, 1)
    self_mass, self_gradient = weighted_forms(packet, moments, 0)
    original_mass = native_mass(coarse_action)
    original_gradient = native_factor(coarse_data, 'gradient')
    original_gram = native_factor(coarse_data, 'gram')
    counter_data = dict(fine_data, gram_weights=counter_weights)
    counter_gram = multiply(native_factor(counter_data, 'gram'), canonical_trial)
    coarse_gram = multiply(coarse_test_transpose, original_gram)
    projected_mass = multiply(coarse_test_transpose, self_mass)
    projected_gradient = multiply(coarse_test_transpose, self_gradient)
    zero = MixedMap([{} for unused in range(packet['native'][1]['count'])], packet['native'][0]['count'])
    channels = {
        'coarse_native_closure': (multiply(coarse_test_transpose, combine((1, self_mass), (-1, original_mass))),
            multiply(coarse_test_transpose, combine((1, self_gradient), (-1, original_gradient)))),
        'unresolved_finer_test': (combine((1, mixed_mass), (-1, projected_mass)),
            combine((1, mixed_gradient), (-1, projected_gradient))),
        'mass_gradient_geometry': (combine((1, fine_maps['mass']), (-1, mixed_mass)),
            combine((1, fine_maps['gradient']), (-1, mixed_gradient))),
        'Gram_geometry_weight': (zero, combine((1, fine_maps['gram']), (-1, counter_gram))),
        'Gram_same_geometry_stencil': (zero, combine((1, counter_gram), (-1, coarse_gram))),
    }
    return channels, dict(coarse_test=coarse_test, canonical_trial=canonical_trial, mixed_mass=mixed_mass,
        mixed_gradient=mixed_gradient, self_mass=self_mass, self_gradient=self_gradient,
        original_mass=original_mass, original_gradient=original_gradient, original_gram=original_gram)
