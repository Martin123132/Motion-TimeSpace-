from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_canonical_v2_20260918 import material_weight
from annular_P2_indexed_live_geometry_20260919 import indexed_label_values
import numpy as np


def complex_loads(engine, radius, radius_rate, amount):
    material, model, owner = engine.material, engine.owner.model, engine.owner
    radius = np.asarray(radius)
    moved_radius = radius + amount * radius_rate
    source_coefficients = material.coefficients[:, -1] + amount * engine.source_direction_coefficients
    source_derivative = 2 * np.polynomial.chebyshev.chebder(source_coefficients)
    source = lambda labels: np.polynomial.chebyshev.chebval(2 * labels, source_coefficients)
    source_label = lambda labels: np.polynomial.chebyshev.chebval(2 * labels, source_derivative)
    velocity_coefficients = engine.source_rate_coefficients + amount * engine.source_velocity_direction_coefficients
    velocity = lambda labels: np.polynomial.chebyshev.chebval(2 * labels, velocity_coefficients)

    def geometry(reference, labels):
        unused, unused2, displacement = model.mapping(reference, model.anchor)
        slope = np.where(reference < model.anchor, 1 / (model.anchor - model.radii[0]),
            -1 / (model.radii[-1] - model.anchor))
        position = reference + displacement * (source(labels) - model.anchor) + (1 - displacement) * owner.width * labels
        spatial = 1 + slope * (source(labels) - model.anchor - owner.width * labels)
        jacobian = displacement * source_label(labels) + (1 - displacement) * owner.width
        return position, spatial, jacobian

    def inverse(target, reference, initial):
        labels = initial.astype(complex)
        for unused in range(8):
            position, unused2, jacobian = geometry(reference, labels)
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
    cuts[rows, local + 2] = inverse(moved_radius[rows], model.edges[columns], initial)
    cuts = np.take_along_axis(cuts, np.argsort(cuts.real, axis=1), axis=1)
    lengths = np.diff(cuts, axis=1)
    segment_rows, segment_columns = np.nonzero(np.isfinite(lengths) & (lengths.real > 1e-13))
    lower, upper = cuts[segment_rows, segment_columns], cuts[segment_rows, segment_columns + 1]
    points, weights = np.polynomial.legendre.leggauss(owner.label_order)
    labels = ((lower[:, None] + upper[:, None]) / 2 + (upper - lower)[:, None] * points / 2).ravel()
    measure = ((upper - lower)[:, None] * weights / 2).ravel() * material_weight(labels)
    rows = np.repeat(segment_rows, len(points))
    interpolation = material.interpolation(labels)
    inner, outer = model.radii[0] + owner.width * labels, model.radii[-1] + owner.width * labels
    left = moved_radius[rows].real < source(labels).real
    spatial = np.where(left, (source(labels) - inner) / (model.anchor - model.radii[0]),
        (outer - source(labels)) / (model.radii[-1] - model.anchor))
    reference = np.where(left, model.radii[0] + (moved_radius[rows] - inner) / spatial,
        model.radii[-1] - (outer - moved_radius[rows]) / spatial)
    cells = np.clip(np.searchsorted(model.edges, reference.real, side='right') - 1, 0, len(model.edges) - 2)
    local = (reference - model.edges[cells]) / np.diff(model.edges)[cells]
    shape = np.column_stack([(1 - local) * (1 - 2 * local), 4 * local * (1 - local), local * (2 * local - 1)])
    indices = model.element_indices[cells]
    shape *= indices >= 0
    gradient_coefficients = material.gradient_coefficients + amount * engine.direction_gradient
    coefficients = np.einsum('ql,qpl->qp', interpolation, gradient_coefficients[cells], optimize=False)
    gradient = (coefficients[:, 0] + coefficients[:, 1] * local) / spatial
    displacement = np.where(left, (reference - model.radii[0]) / (model.anchor - model.radii[0]),
        (model.radii[-1] - reference) / (model.radii[-1] - model.anchor))
    field_rates = engine.loads.rates[:, :-1] + amount * engine.velocity_direction[:, :-1]
    temporal = np.sum(shape * indexed_label_values(interpolation, field_rates, indices), axis=1)
    temporal -= displacement * velocity(labels) * gradient
    outside = (moved_radius[rows].real < inner.real) | (moved_radius[rows].real > outer.real)
    temporal[outside], gradient[outside] = 0., 0.

    def aggregate(values):
        answer = np.zeros(len(radius), dtype=complex)
        np.add.at(answer, rows, values)
        return answer

    fields = dict(temporal_square=aggregate(measure * temporal**2), gradient_square=aggregate(measure * gradient**2),
        gram=np.zeros(len(radius), complex), source_density=np.zeros(len(radius), complex), velocity=np.zeros(len(radius), complex))
    if engine.extension != 'reference':
        factors = engine.loads.factor_coefficients[engine.extension] + amount * engine.factor_direction_coefficients
        for index, reference in enumerate(engine.loads.knots):
            start, end = engine.loads.sampling.indptr[index:index + 2]
            if start == end:
                continue
            lower, upper = material.node_geometry(reference, np.array([-.5, .5]))[0]
            selected = (radius >= lower) & (radius <= upper)
            if not np.any(selected):
                continue
            labels = inverse(moved_radius[selected], reference, material.inverse_node(radius[selected], reference))
            unused, spatial, jacobian = geometry(reference, labels)
            active, weights = engine.loads.sampling.indices[start:end], engine.loads.sampling.data[start:end]
            image = np.polynomial.chebyshev.chebval(2 * labels, factors[:, active])
            fields['gram'][selected] += material_weight(labels) * np.sum(weights[:, None] * image**2, axis=0) / (2 * spatial * jacobian)
    selected = (radius >= material.coordinates[0, -1]) & (radius <= material.coordinates[-1, -1])
    labels = inverse(moved_radius[selected], model.anchor, material.inverse_node(radius[selected], model.anchor))
    fields['source_density'][selected] = material_weight(labels) / source_label(labels)
    fields['velocity'][selected] = velocity(labels)
    return fields
