import numpy as np
from scipy.sparse import coo_matrix,csr_matrix
from annular_source_fitted_action_20260915 import SourceFittedAction
from annular_quadratic_source_fitted_action_20260915 import QuadraticSourceFittedAction


class LocallyRefinedSourceAction(QuadraticSourceFittedAction):
    def __init__(self, base_count=17, gram=True, order=10, background_mass=.7, anchor=6.03, source_splits=4):
        linear = SourceFittedAction(base_count, gram, order, background_mass, anchor)
        self.base_count, self.base_radii = base_count, linear.radii.copy()
        self.anchor, self.background_mass, self.gram = anchor, background_mass, gram
        self.source_mass, self.stationary = linear.source_mass, False
        self.gram_spacing, self.spacing = linear.spacing, linear.spacing/2
        self.fractions, self.weights = linear.fractions, linear.weights
        if not isinstance(source_splits,int) or source_splits < 1:
            raise ValueError('source_splits must be a positive integer.')
        self.source_splits = source_splits
        original_edges = np.sort(np.append(self.base_radii,anchor))
        source_index = np.searchsorted(original_edges,anchor)
        additions = np.concatenate([np.linspace(original_edges[source_index-1],anchor,source_splits+1),np.linspace(anchor,original_edges[source_index+1],source_splits+1)])
        self.edges = np.unique(np.concatenate([original_edges,additions]))
        full_nodes = np.sort(np.concatenate([self.edges, (self.edges[:-1]+self.edges[1:])/2]))
        free = full_nodes != anchor
        self.radii, self.count = full_nodes[free], int(np.sum(free))
        full_to_free = np.full(len(full_nodes), -1, dtype=int)
        full_to_free[free] = np.arange(self.count)
        element_nodes = np.column_stack([np.arange(0, len(full_nodes)-2, 2), np.arange(1, len(full_nodes)-1, 2), np.arange(2, len(full_nodes), 2)])
        self.element_indices = full_to_free[element_nodes]
        lengths = np.diff(self.edges)
        self.reference_radius = (self.edges[:-1, None]+lengths[:, None]*self.fractions).ravel()
        self.reference_weight = (lengths[:, None]*self.weights).ravel()
        self.reference_indices, self.reference_shape, self.reference_radial = self.features_quadratic(self.reference_radius)
        vertex_indices = np.searchsorted(self.radii, self.base_radii)
        original = linear.original.tocoo()
        sampling = linear.sampling.tocoo()
        self.original = coo_matrix((original.data, (original.row, vertex_indices[original.col])), shape=(original.shape[0], self.count)).tocsr()
        self.sampling = coo_matrix((sampling.data, (sampling.row, vertex_indices[sampling.col])), shape=(sampling.shape[0], self.count)).tocsr()
        self.jump = np.zeros(self.count)
        source_edge = np.searchsorted(self.edges, anchor)
        for element, local, sign in [(source_edge-1, np.array([1., -4., 3.]), -1.), (source_edge, np.array([-3., 4., -1.]), 1.)]:
            indices = self.element_indices[element]
            valid = indices >= 0
            np.add.at(self.jump, indices[valid], sign*local[valid]/lengths[element])
        hinge = np.maximum(self.radii-anchor, 0.)
        self.lifted_hinge = self.original @ hinge
        self.lifted = self.original-csr_matrix(self.lifted_hinge[:, None]) @ csr_matrix(self.jump[None, :])
        cells, shapes, unused, unused2 = linear.features(self.radii, anchor)
        rows = np.repeat(np.arange(self.count), 2)
        columns = np.column_stack([cells, cells+1]).ravel()
        self.linear_embedding = coo_matrix((shapes.ravel(), (rows, columns)), shape=(self.count, base_count)).tocsr()
