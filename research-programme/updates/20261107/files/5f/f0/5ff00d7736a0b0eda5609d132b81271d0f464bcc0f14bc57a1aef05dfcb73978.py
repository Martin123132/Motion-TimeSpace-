from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_canonical_v2_20260918 import P2Material, P2Density, inverse_momenta, material_weight
from annular_P2_primitive_geometry_20260918 import PrimitiveP2Geometry
from annular_P2_graded_source_20260919 import GradedP2System
import numpy as np


def indexed_label_values(interpolation, values, indices):
    result = np.empty(indices.shape, dtype=np.result_type(interpolation, values))
    for local in range(indices.shape[1]):
        result[:, local] = np.einsum('ql,lq->q', interpolation, values[:, indices[:, local]], optimize=False)
    return result


class IndexedP2Material(P2Material):
    def samples(self, radius, labels):
        model = self.owner.model
        interpolation = self.interpolation(labels)
        source = interpolation @ self.coordinates[:, -1]
        inner, outer = model.radii[0]+self.owner.width*labels, model.radii[-1]+self.owner.width*labels
        left = radius < source
        jacobian = np.where(left, (source-inner)/(model.anchor-model.radii[0]),
            (outer-source)/(model.radii[-1]-model.anchor))
        reference = np.where(left, model.radii[0]+(radius-inner)/jacobian,
            model.radii[-1]-(outer-radius)/jacobian)
        indices, shape, radial = model.features_quadratic(reference)
        unused, unused2, displacement = model.mapping(reference, model.anchor)
        values = indexed_label_values(interpolation, self.coordinates[:, :-1], indices)
        gradient = np.sum(radial*values, axis=1)/jacobian
        outside = (radius < inner) | (radius > outer)
        shape[outside], gradient[outside] = 0., 0.
        motion = -displacement*gradient
        return interpolation, indices, shape, gradient, motion


class IndexedP2Density(P2Density):
    def __init__(self, material, radius):
        self.material, self.radius = material, np.asarray(radius).ravel()
        owner, model = material.owner, material.owner.model
        points, weights = np.polynomial.legendre.leggauss(owner.label_order)
        endpoints = np.array([material.node_geometry(model.edges, label)[0] for label in [-.5, .5]])
        crossing_rows, crossing_columns = [], []
        for start in range(0, len(self.radius), 2048):
            target = self.radius[start:start+2048, None]
            selected = (target > endpoints[0]) & (target < endpoints[1])
            rows, columns = np.nonzero(selected)
            crossing_rows.append(rows+start)
            crossing_columns.append(columns)
        rows, columns = np.concatenate(crossing_rows), np.concatenate(crossing_columns)
        counts = np.bincount(rows, minlength=len(self.radius))
        starts = np.cumsum(counts)-counts
        local = np.arange(len(rows))-np.repeat(starts, counts)
        cuts = np.full((len(self.radius), int(max(counts))+2), np.nan)
        cuts[:, :2] = [-.5, .5]
        cuts[rows, local+2] = material.inverse_node(self.radius[rows], model.edges[columns])
        cuts.sort(axis=1)
        lengths = np.diff(cuts, axis=1)
        selected = np.isfinite(lengths) & (lengths > 1e-13)
        segment_rows, segment_columns = np.nonzero(selected)
        lower, upper = cuts[segment_rows, segment_columns], cuts[segment_rows, segment_columns+1]
        labels = (lower[:, None]+upper[:, None])/2+(upper-lower)[:, None]*points/2
        measures = (upper-lower)[:, None]*weights*material_weight(labels)/2
        self.offsets, self.label_weights = labels.ravel(), measures.ravel()
        self.indices = np.repeat(segment_rows, len(points))
        self.interpolation, self.scalar_indices, self.shape, gradient, self.motion = material.samples(
            self.radius[self.indices], self.offsets)
        self.gradient_square = np.bincount(self.indices, weights=self.label_weights*gradient**2,
            minlength=len(self.radius))
        self.gram = np.zeros(len(self.radius))
        selected_nodes = np.asarray(model.sampling.sum(axis=0)).ravel() != 0
        for index in np.flatnonzero(selected_nodes):
            reference = model.radii[index]
            lower, upper = material.node_geometry(reference, np.array([-.5, .5]))[0]
            selected = (self.radius >= lower) & (self.radius <= upper)
            if np.any(selected):
                labels = material.inverse_node(self.radius[selected], reference)
                unused, jacobian, label_jacobian = material.node_geometry(reference, labels)
                self.gram[selected] += material_weight(labels)*material.gram_load(labels)[:, index]/(jacobian*label_jacobian)
        lower, upper = material.coordinates[[0, -1], -1]
        self.source_selected = (self.radius >= lower) & (self.radius <= upper)
        labels = material.inverse_node(self.radius[self.source_selected], model.anchor)
        self.source_interpolation = material.interpolation(labels)
        self.source_density = np.zeros(len(self.radius))
        self.source_density[self.source_selected] = material_weight(labels)/material.source_jacobian(labels)

    def update(self, rates):
        sample = indexed_label_values(self.interpolation, rates[:, :-1], self.scalar_indices)
        temporal = np.sum(self.shape*sample, axis=1)
        temporal += self.motion*(self.interpolation @ rates[:, -1])
        self.temporal_square = np.bincount(self.indices, weights=self.label_weights*temporal**2,
            minlength=len(self.radius))
        self.velocity = np.zeros(len(self.radius))
        self.velocity[self.source_selected] = self.source_interpolation @ rates[:, -1]


class IndexedP2Geometry(PrimitiveP2Geometry):
    def __init__(self, owner, material, rates):
        self.owner, self.material, self.rule = owner, material, owner.radial_rule
        raw_edges = np.sort(np.concatenate([material.node_geometry(owner.model.edges, label)[0] for label in [-.5, .5]]))
        tolerance = 32*np.finfo(float).eps*max(1., float(max(abs(raw_edges))))
        clusters = [[raw_edges[0]]]
        for edge in raw_edges[1:]:
            if edge-clusters[-1][0] <= tolerance:
                clusters[-1].append(edge)
            else:
                clusters.append([edge])
        self.edges = np.array([np.mean(cluster) for cluster in clusters])
        self.edge_merges = [dict(count=len(cluster), spread=float(max(cluster)-min(cluster)),
            value=float(np.mean(cluster))) for cluster in clusters if len(cluster) > 1]
        self.edge_tolerance = tolerance
        self.lengths, self.centers = np.diff(self.edges), (self.edges[:-1]+self.edges[1:])/2
        self.nodes = self.centers[:, None]+self.lengths[:, None]*self.rule.points/2
        self.density = IndexedP2Density(material, self.nodes)
        self.density.update(rates)
        self.solve()

    def off_grid_residual(self, rates):
        points, unused = np.polynomial.legendre.leggauss(self.owner.radial_degree+3)
        radius = (self.centers[:, None]+self.lengths[:, None]*points/2).ravel()
        density = IndexedP2Density(self.material, radius)
        density.update(rates)
        mass, lapse, mass_radial, lapse_radial = self.values(radius)
        expected_mass, expected_lapse = density.rhs(mass, lapse)
        return float(max(abs(mass_radial-expected_mass))), float(max(abs(lapse_radial-expected_lapse)))


class IndexedGradedP2System(GradedP2System):
    def solve(self, coordinates, momenta):
        material = IndexedP2Material(self, coordinates)
        rates = np.zeros_like(coordinates)
        geometry = IndexedP2Geometry(self, material, rates)
        history = []
        for iteration in range(32):
            updated = np.array([inverse_momenta(self.layer(label, geometry), position, momentum)[0]
                for label, position, momentum in zip(self.labels, coordinates, momenta)])
            error = float(max(abs(updated-rates).ravel()))
            rates = updated
            geometry.density.update(rates)
            geometry.solve()
            history.append(error)
            if error < self.canonical_tolerance:
                break
        else:
            raise RuntimeError('Indexed P2 canonical/radial iteration failed to converge.')
        geometry.canonical_history = history
        return rates, geometry
