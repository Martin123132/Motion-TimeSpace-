from annular_P2_graded_source_20260919 import GradedP2System, GradedSourceAction, force_schur_identity, frequency_diagnostic
from scipy.sparse import coo_matrix
import numpy as np


def nested_embedding(coarse, fine):
    edges = np.asarray(fine.edges, dtype=np.longdouble)
    nodes = np.sort(np.concatenate([edges, (edges[:-1]+edges[1:])/2]))
    nodes = nodes[nodes != np.longdouble(fine.anchor)]
    if len(nodes) != fine.count:
        raise ValueError('Analytic finite-element node count changed.')
    indices, shape, unused = coarse.features_quadratic(nodes)
    return coo_matrix((np.asarray(shape, dtype=float).ravel(),
        (np.repeat(np.arange(fine.count), 3), indices.ravel())), shape=(fine.count, coarse.count)).tocsr()
