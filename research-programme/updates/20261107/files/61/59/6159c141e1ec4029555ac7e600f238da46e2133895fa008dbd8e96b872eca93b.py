from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_canonical_v2_20260918 import material_weight
from annular_P2_indexed_live_geometry_20260919 import indexed_label_values
import numpy as np


def complex_mixed_wave(engine, radius, amount):
    material, model, owner = engine.material, engine.owner.model, engine.owner
    coefficients = material.coefficients[:, -1] + amount * engine.source_direction_coefficients
    source = lambda labels: np.polynomial.chebyshev.chebval(2 * labels, coefficients)
    source_label = lambda labels: np.polynomial.chebyshev.chebval(2 * labels, 2 * np.polynomial.chebyshev.chebder(coefficients))
    velocity = lambda labels: np.polynomial.chebyshev.chebval(2 * labels,
        engine.source_rate_coefficients + amount * engine.source_velocity_direction_coefficients)

    def inverse(target, reference, initial):
        labels = initial.astype(complex)
        unused, unused2, displacement = model.mapping(reference, model.anchor)
        for unused in range(8):
            position = reference + displacement * (source(labels) - model.anchor) + (1 - displacement) * owner.width * labels
            jacobian = displacement * source_label(labels) + (1 - displacement) * owner.width
            labels -= (position - target) / jacobian
        return labels

    endpoints = np.array([material.node_geometry(model.edges, label)[0] for label in [-.5, .5]])
    rows, columns = np.nonzero((radius[:, None] > endpoints[0]) & (radius[:, None] < endpoints[1]))
    counts = np.bincount(rows, minlength=len(radius))
    starts = np.cumsum(counts) - counts
    positions = np.arange(len(rows)) - np.repeat(starts, counts)
    cuts = np.full((len(radius), int(max(counts)) + 2), np.nan, dtype=complex)
    cuts[:, :2] = [-.5, .5]
    initial = material.inverse_node(radius[rows], model.edges[columns])
    cuts[rows, positions + 2] = inverse(radius[rows], model.edges[columns], initial)
    cuts = np.take_along_axis(cuts, np.argsort(cuts.real, axis=1), axis=1)
    lengths = np.diff(cuts, axis=1)
    segment_rows, segment_columns = np.nonzero(np.isfinite(lengths) & (lengths.real > 1e-13))
    lower, upper = cuts[segment_rows, segment_columns], cuts[segment_rows, segment_columns + 1]
    points, weights = np.polynomial.legendre.leggauss(owner.label_order)
    labels = ((lower[:, None] + upper[:, None]) / 2 + (upper - lower)[:, None] * points / 2).ravel()
    measure = ((upper - lower)[:, None] * weights / 2).ravel() * material_weight(labels)
    rows = np.repeat(segment_rows, len(points))
    cardinal = material.interpolation(labels)
    inner, outer = model.radii[0] + owner.width * labels, model.radii[-1] + owner.width * labels
    left = radius[rows] < source(labels).real
    spatial = np.where(left, (source(labels) - inner) / (model.anchor - model.radii[0]),
        (outer - source(labels)) / (model.radii[-1] - model.anchor))
    reference = np.where(left, model.radii[0] + (radius[rows] - inner) / spatial,
        model.radii[-1] - (outer - radius[rows]) / spatial)
    cells = np.clip(np.searchsorted(model.edges, reference.real, side='right') - 1, 0, len(model.edges) - 2)
    local = (reference - model.edges[cells]) / np.diff(model.edges)[cells]
    indices = model.element_indices[cells]
    shape = np.column_stack([(1 - local) * (1 - 2 * local), 4 * local * (1 - local), local * (2 * local - 1)])
    shape *= indices >= 0
    gradient_coefficients = material.gradient_coefficients + amount * engine.direction_gradient
    gradient_values = np.einsum('ql,qpl->qp', cardinal, gradient_coefficients[cells], optimize=False)
    gradient = (gradient_values[:, 0] + gradient_values[:, 1] * local) / spatial
    displacement = np.where(left, (reference - model.radii[0]) / (model.anchor - model.radii[0]),
        (model.radii[-1] - reference) / (model.radii[-1] - model.anchor))
    field_rates = engine.loads.rates[:, :-1] + amount * engine.velocity_direction[:, :-1]
    temporal = np.sum(shape * indexed_label_values(cardinal, field_rates, indices), axis=1) - displacement * velocity(labels) * gradient
    field_direction = engine.field_direction + amount * engine.field_direction_rate
    field = np.sum(shape * indexed_label_values(cardinal, field_direction, indices), axis=1)
    edges = indexed_label_values(cardinal, engine.edges_direction, np.column_stack([cells, cells + 1]))
    movement = (1 - local) * edges[:, 0] + local * edges[:, 1] + displacement * (cardinal @ engine.source_direction)
    defect = field - movement * gradient
    outside = (radius[rows] < inner.real) | (radius[rows] > outer.real)
    temporal[outside], defect[outside] = 0., 0.
    result = np.zeros(len(radius), complex)
    np.add.at(result, rows, 2 * measure * temporal * defect)
    return result
