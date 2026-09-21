from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_decimal_transport_v2_20260919 import decimal_array
from bisect import bisect_right
from decimal import Decimal
from fractions import Fraction
import numpy as np


def decimal_fraction(value):
    rational = Fraction(value)
    return Decimal(rational.numerator)/Decimal(rational.denominator)


def apply_rational_rows(rows, values):
    answer = np.full((len(rows), values.shape[1]), Decimal(0), dtype=object)
    for index, row in enumerate(rows):
        for column, value in row.items():
            answer[index] += decimal_fraction(value)*values[int(column)]
    return answer


def polynomial_products(mesh, values):
    coefficients = np.full((len(mesh['elements']), 3, values.shape[1]), Decimal(0), dtype=object)
    lengths = []
    for element, indices in enumerate(mesh['elements']):
        local = [values[index] if index >= 0 else np.full(values.shape[1], Decimal(0), dtype=object) for index in indices]
        left, middle, right = local
        coefficients[element, 0] = left
        coefficients[element, 1] = -3*left+4*middle-right
        coefficients[element, 2] = 2*left-4*middle+2*right
        lengths.append(decimal_fraction(Fraction(mesh['edges'][element+1])-Fraction(mesh['edges'][element])))
    lengths = np.array(lengths, dtype=object)
    result = {}
    for name, first, last, factors in [('mass', 2, 3, coefficients),
            ('gradient', 0, 1, coefficients[:, 1:]*np.array([1, 2], dtype=object)[None, :, None]/lengths[:, None, None])]:
        products = np.full((len(lengths), 2*factors.shape[1]-1), Decimal(0), dtype=object)
        for before in range(factors.shape[1]):
            for after in range(factors.shape[1]):
                products[:, before+after] += factors[:, before, first]*factors[:, after, last]
        result[name] = products
    return result


def weighted_moments(mesh, cuts, quadrature):
    edges = list(map(Fraction, mesh['edges']))
    rational_cuts = [Fraction.from_float(float(value)) for value in cuts]
    parents, lengths, offsets, spans = [], [], [], []
    for lower, upper in zip(rational_cuts[:-1], rational_cuts[1:]):
        parent = bisect_right(edges, (lower+upper)/2)-1
        if parent < 0 or parent+1 >= len(edges) or lower < edges[parent] or upper > edges[parent+1]:
            raise ValueError('Integration segment crosses a preserved common edge.')
        width = edges[parent+1]-edges[parent]
        parents.append(parent)
        lengths.append(decimal_fraction(upper-lower))
        offsets.append(decimal_fraction((lower-edges[parent])/width))
        spans.append(decimal_fraction((upper-lower)/width))
    parents = np.asarray(parents)
    fractions = decimal_array(quadrature['fractions'])
    weights = decimal_array(quadrature['gauss_weights'])
    local = np.asarray(offsets, dtype=object)[:, None]+np.asarray(spans, dtype=object)[:, None]*fractions
    measure = np.asarray(lengths, dtype=object)[:, None]*weights
    result = {name:np.full((len(edges)-1, 5), Decimal(0), dtype=object) for name in
        ['unit', 'coarse_mass', 'fine_mass', 'coarse_gradient', 'fine_gradient']}
    densities = {name:decimal_array(quadrature[name+'_density']) for name in result if name != 'unit'}
    power = np.full(local.shape, Decimal(1), dtype=object)
    for degree in range(5):
        weighted = measure*power
        np.add.at(result['unit'][:, degree], parents, np.sum(weighted, axis=1))
        for name, values in densities.items():
            np.add.at(result[name][:, degree], parents, np.sum(weighted*values, axis=1))
        power *= local
    return result


def contract(moment, products):
    return np.sum(moment[:, :products.shape[1]]*products, axis=1)
