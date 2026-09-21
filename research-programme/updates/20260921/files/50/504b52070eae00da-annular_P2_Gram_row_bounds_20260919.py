from derive_annular_source_gravity_20260914 import EvidenceRun
from scipy.linalg import solve_banded
import numpy as np


def row_bounds(layer, coordinates, rates):
    data = layer.evaluate(0., coordinates, rates)
    projection = solve_banded((2, 2), data['mass_bands'], data['cross'], check_finite=False)
    nodes, jacobian, unused = layer.mapping(layer.radii, coordinates[-1])
    weights = np.asarray(layer.sampling @ (layer.coefficient(0., nodes)/jacobian))/layer.gram_spacing
    if np.any(weights <= 0):
        raise ValueError('Gram row bound needs positive row weights.')
    changed, changed_jacobian, unused = layer.mapping(layer.radii, complex(coordinates[-1], 1e-25))
    weight_derivative = (np.asarray(layer.sampling @ (layer.coefficient(0., changed)/changed_jacobian))
        /layer.gram_spacing).imag/1e-25
    factors, projected = layer.lifted @ coordinates[:-1], layer.lifted @ projection
    shape_rows = -.5*weight_derivative*factors**2
    products = weights*factors*projected
    absolute = abs(layer.original)
    left = np.asarray(absolute @ (layer.radii < layer.anchor)).ravel()
    right = np.asarray(absolute @ (layer.radii > layer.anchor)).ravel()
    source = (left > 0) & (right > 0)
    groups = []
    for name, selected in [('source_straddling', source), ('remaining', ~source)]:
        field_norm_squared = float(weights[selected] @ factors[selected]**2)
        direction_norm_squared = float(weights[selected] @ projected[selected]**2)
        bound = float(np.sqrt(field_norm_squared*direction_norm_squared))
        product_sum = float(np.sum(products[selected]))
        groups.append(dict(name=name, rows=int(np.sum(selected)),
            field_energy=field_norm_squared/2, direction_energy=direction_norm_squared/2,
            projected_sum=product_sum, projected_absolute_sum=float(np.sum(abs(products[selected]))),
            Cauchy_bound=bound, shape_sum=float(np.sum(shape_rows[selected])),
            shape_absolute_sum=float(np.sum(abs(shape_rows[selected]))),
            weighted_alignment=product_sum/bound if bound > 0 else 0.,
            hinge_weighted_norm_squared=float(weights[selected] @ layer.lifted_hinge[selected]**2)))
    global_bound = float(np.sqrt((weights @ factors**2)*(weights @ projected**2)))
    shape_absolute = float(np.sum(abs(shape_rows)))
    partitioned = sum(row['Cauchy_bound'] for row in groups)
    row_absolute = float(np.sum(abs(products)))
    band = data['mass_bands']
    offsum = np.zeros(layer.count)
    for offset in [-2, -1, 1, 2]:
        columns = np.arange(max(0, -offset), min(layer.count, layer.count-offset))
        rows = columns+offset
        offsum[rows] += abs(band[2+offset, columns])
    margins = band[2]-offsum
    bound_available = bool(np.all(margins > 0))
    maximum_projection_bound = float(np.max(abs(data['cross'])/margins)) if bound_available else None
    report = dict(groups=groups, row_count=len(weights), source_rows=int(np.sum(source)),
        all_rows_retained=True, no_small_hinge_tail_discarded=True,
        projected_drive=float(np.sum(products)), shape_force=float(np.sum(shape_rows)),
        explicit_drive=float(np.sum(products+shape_rows)),
        projected_absolute_row_bound=row_absolute, projected_partitioned_bound=partitioned,
        projected_global_bound=global_bound, shape_absolute_row_bound=shape_absolute,
        drive_absolute_row_bound=shape_absolute+row_absolute,
        drive_partitioned_bound=shape_absolute+partitioned,
        drive_global_same_shape_bound=shape_absolute+global_bound,
        projection_maximum=float(np.max(abs(projection))),
        minimum_mass_diagonal_margin=float(np.min(margins)),
        diagonal_margin_projection_bound_available=bound_available,
        diagonal_margin_projection_bound=maximum_projection_bound,
        source_cap=float(layer.source_cap), bulk_spacing=float(layer.gram_spacing))
    arrays = dict(weights=weights, field_factors=factors, direction_factors=projected,
        shape_rows=shape_rows, projected_rows=products, source_rows=source,
        projection=projection, coordinates=coordinates, rates=rates, margins=margins,
        kinetic_cross=data['cross'], hinge=layer.lifted_hinge)
    return report, arrays
