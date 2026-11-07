from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_canonical_v2_20260918 import material_weight
from annular_P2_indexed_live_geometry_20260919 import indexed_label_values
import numpy as np


def complex_position(engine, radius, amount):
    radius = np.asarray(radius)
    material, model, owner = engine.material, engine.owner.model, engine.owner

    def source(labels):
        cardinal = material.interpolation(np.atleast_1d(labels))
        return cardinal @ (material.coordinates[:, -1] + amount * engine.direction[:, -1])

    def geometry(reference, labels):
        displacement = np.where(reference.real <= model.anchor, (reference - model.radii[0]) / (model.anchor - model.radii[0]), (model.radii[-1] - reference) / (model.radii[-1] - model.anchor))
        slope = np.where(reference.real <= model.anchor, 1 / (model.anchor - model.radii[0]), -1 / (model.radii[-1] - model.anchor))
        support, support_spatial, support_label = engine.support(reference, labels)
        moved_source = source(labels)
        source_label = np.polynomial.chebyshev.chebval(2 * labels, 2 * np.polynomial.chebyshev.chebder(material.coefficients[:, -1] + amount * engine.source_direction_coefficients))
        position = reference + displacement * (moved_source - model.anchor) + (1 - displacement) * owner.width * labels + amount * support
        spatial = 1 + slope * (moved_source - model.anchor - owner.width * labels) + amount * support_spatial
        label_jacobian = (1 - displacement) * owner.width + displacement * source_label + amount * support_label
        return position, spatial, label_jacobian, displacement

    def inverse(target, reference, initial):
        labels = initial.astype(complex)
        for unused in range(2):
            position, unused2, jacobian, unused3 = geometry(reference, labels)
            labels -= (position - target) / jacobian
        return labels

    endpoints = np.array([material.node_geometry(model.edges, label)[0] for label in [-.5, .5]])
    rows, columns = np.nonzero((radius[:, None] > endpoints[0]) & (radius[:, None] < endpoints[1]))
    counts = np.bincount(rows, minlength=len(radius))
    starts = np.cumsum(counts) - counts
    local = np.arange(len(rows)) - np.repeat(starts, counts)
    cuts = np.full((len(radius), int(max(counts)) + 2), np.nan, dtype=complex)
    cuts[:, :2] = [-.5, .5]
    initial = material.inverse_node(radius[rows], model.edges[columns])
    cuts[rows, local + 2] = inverse(radius[rows], model.edges[columns], initial)
    cuts = np.take_along_axis(cuts, np.argsort(cuts.real, axis=1), axis=1)
    lengths = np.diff(cuts, axis=1)
    segment_rows, segment_columns = np.nonzero(np.isfinite(lengths) & (lengths.real > 1e-13))
    lower, upper = cuts[segment_rows, segment_columns], cuts[segment_rows, segment_columns + 1]
    points, weights = np.polynomial.legendre.leggauss(owner.label_order)
    labels = ((lower[:, None] + upper[:, None]) / 2 + (upper - lower)[:, None] * points / 2).ravel()
    measure = ((upper - lower)[:, None] * weights / 2).ravel() * material_weight(labels)
    rows = np.repeat(segment_rows, len(points))
    inner, outer = model.radii[0] + owner.width * labels, model.radii[-1] + owner.width * labels
    moved_source = source(labels)
    left = radius[rows] < moved_source.real
    spatial = np.where(left, (moved_source - inner) / (model.anchor - model.radii[0]), (outer - moved_source) / (model.radii[-1] - model.anchor))
    reference = np.where(left, model.radii[0] + (radius[rows] - inner) / spatial, model.radii[-1] - (outer - radius[rows]) / spatial)
    for unused in range(2):
        position, spatial, unused2, unused3 = geometry(reference, labels)
        reference -= (position - radius[rows]) / spatial
    unused, spatial, unused2, displacement = geometry(reference, labels)
    cells = np.clip(np.searchsorted(model.edges, reference.real, side='right') - 1, 0, len(model.edges) - 2)
    local = (reference - model.edges[cells]) / np.diff(model.edges)[cells]
    shape = np.column_stack([(1 - local) * (1 - 2 * local), 4 * local * (1 - local), local * (2 * local - 1)])
    indices = model.element_indices[cells]
    shape *= indices >= 0
    cardinal = material.interpolation(labels)
    coefficients = np.einsum('ql,qpl->qp', cardinal, (material.gradient_coefficients + amount * engine.direction_gradient)[cells], optimize=False)
    gradient = (coefficients[:, 0] + coefficients[:, 1] * local) / spatial
    velocity = cardinal @ engine.loads.rates[:, -1]
    temporal = np.sum(shape * indexed_label_values(cardinal, engine.loads.rates[:, :-1], indices), axis=1) - displacement * velocity * gradient
    outside = (radius[rows] < inner.real) | (radius[rows] > outer.real)
    temporal[outside], gradient[outside] = 0., 0.
    answer = dict(temporal_square=np.zeros(len(radius), complex), gradient_square=np.zeros(len(radius), complex), source_density=np.zeros(len(radius), complex), velocity=np.zeros(len(radius), complex))
    np.add.at(answer['temporal_square'], rows, measure * temporal**2)
    np.add.at(answer['gradient_square'], rows, measure * gradient**2)
    selected = (radius >= material.coordinates[0, -1]) & (radius <= material.coordinates[-1, -1])
    labels = inverse(radius[selected], np.full(np.count_nonzero(selected), model.anchor), material.inverse_node(radius[selected], model.anchor))
    jacobian = geometry(np.full(len(labels), model.anchor), labels)[2]
    answer['source_density'][selected] = material_weight(labels) / jacobian
    answer['velocity'][selected] = material.interpolation(labels) @ engine.loads.rates[:, -1]
    return answer
