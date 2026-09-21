from annular_P2_graded_source_20260919 import GradedP2System, GradedSourceAction, force_schur_identity, frequency_diagnostic
from bisect import bisect_right
from fractions import Fraction
from scipy.sparse import coo_matrix


def nested_embedding(coarse, fine):
    edges = [Fraction.from_float(float(value)) for value in fine.edges]
    coarse_edges = [Fraction.from_float(float(value)) for value in coarse.edges]
    anchor = Fraction.from_float(float(fine.anchor))
    nodes = sorted(edges+[(lower+upper)/2 for lower, upper in zip(edges[:-1], edges[1:])])
    nodes = [value for value in nodes if value != anchor]
    if len(nodes) != fine.count:
        raise ValueError('Analytic finite-element node count changed.')
    rows, columns, values = [], [], []
    for row, position in enumerate(nodes):
        element = min(max(0, bisect_right(coarse_edges, position)-1), len(coarse_edges)-2)
        fraction = (position-coarse_edges[element])/(coarse_edges[element+1]-coarse_edges[element])
        shape = [(1-fraction)*(1-2*fraction), 4*fraction*(1-fraction), fraction*(2*fraction-1)]
        for column, value in zip(coarse.element_indices[element], shape):
            if column >= 0:
                rows.append(row)
                columns.append(int(column))
                values.append(float(value))
    return coo_matrix((values, (rows, columns)), shape=(fine.count, coarse.count)).tocsr()
