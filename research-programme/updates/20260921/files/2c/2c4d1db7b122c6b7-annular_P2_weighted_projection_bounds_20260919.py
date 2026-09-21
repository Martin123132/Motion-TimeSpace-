from derive_annular_source_gravity_20260914 import EvidenceRun
from scipy.linalg import solve_banded
import numpy as np


def uniform_constants(epsilon=.05):
    endpoint_square = 2/15
    midpoint_square = 8/15
    endpoint_absolute = np.sqrt(endpoint_square)
    midpoint_absolute = 2/3
    all_endpoint = 1.25*endpoint_absolute
    all_midpoint = 1.25*midpoint_absolute
    endpoint_margin = 1/30-epsilon*all_endpoint
    midpoint_margin = 2/5-epsilon*all_midpoint
    if min(endpoint_margin, midpoint_margin) <= 0:
        raise ValueError('The sufficient projection margin is not positive.')
    contraction = max((1/10+epsilon*(all_endpoint-endpoint_square))/((1-epsilon)*endpoint_square),
        (2/15+epsilon*(all_midpoint-midpoint_square))/((1-epsilon)*midpoint_square))
    stability = max((1+epsilon)*endpoint_absolute/endpoint_margin,
        (1+epsilon)*midpoint_absolute/midpoint_margin)
    return dict(epsilon=epsilon, endpoint_margin=endpoint_margin, midpoint_margin=midpoint_margin,
        contraction=contraction, nodal_projection_stability=stability,
        source_pair_l1_bound=4*contraction/(1-contraction)**2)


def band_action(bands, values):
    result = bands[2]*values
    count = len(values)
    for offset in [-2, -1, 1, 2]:
        columns = np.arange(max(0, -offset), min(count, count-offset))
        result[columns+offset] += bands[2+offset, columns]*values[columns]
    return result


def projection_data(layer, coordinates, rates):
    data = layer.evaluate(0., coordinates, rates)
    radius, jacobian, motion = layer.mapping(layer.reference_radius, coordinates[-1])
    kinetic = jacobian*radius**4/layer.coefficient(0., radius)
    quadrature_weight = layer.reference_weight*kinetic
    field_motion = -motion*data['field_radial']
    bands = data['mass_bands']
    offsum = np.zeros(layer.count)
    for offset in [-2, -1, 1, 2]:
        columns = np.arange(max(0, -offset), min(layer.count, layer.count-offset))
        offsum[columns+offset] += abs(bands[2+offset, columns])
    margins = bands[2]-offsum
    contraction = float(np.max(offsum/bands[2]))
    load_abs = layer.assemble_quadratic(layer.reference_indices,
        abs(layer.reference_shape)*quadrature_weight[:, None])
    stability = float(np.max(load_abs/margins)) if np.all(margins > 0) else None
    source = int(np.searchsorted(layer.edges, layer.anchor))
    order = len(layer.fractions)
    source_columns = np.zeros((layer.count, 2))
    missing_shapes = np.zeros((len(layer.reference_radius), 2))
    for side, element, local in [(0, source-1, 2), (1, source, 0)]:
        fraction = layer.fractions
        full = fraction*(2*fraction-1) if local == 2 else (1-fraction)*(1-2*fraction)
        selected = slice(element*order, (element+1)*order)
        missing_shapes[selected, side] = full
        source_columns[:, side] = layer.assemble_quadratic(layer.reference_indices,
            layer.reference_shape*(quadrature_weight*missing_shapes[:, side])[:, None])
    solved = solve_banded((2, 2), bands, np.column_stack([data['cross'], -source_columns]), check_finite=False)
    centres = (layer.edges[:-1]+layer.edges[1:])/2
    midpoint_radius, midpoint_jacobian, unused = layer.mapping(centres, coordinates[-1])
    midpoint_kinetic = midpoint_jacobian*midpoint_radius**4/layer.coefficient(0., midpoint_radius)
    relative = np.abs(kinetic.reshape(-1, order)/midpoint_kinetic[:, None]-1)
    return dict(data=data, kinetic=kinetic, quadrature_weight=quadrature_weight,
        field_motion=field_motion, projection=solved[:, 0], source_defects=solved[:, 1:],
        source_columns=source_columns, missing_shapes=missing_shapes, margins=margins,
        contraction=contraction, stability=stability, discrete_relative_variation=float(relative.max()),
        discrete_cell_variation=relative.max(axis=1), source=source,
        defect_pair_l1=float(np.sum(abs(solved[:, 1:]))))


def operator_constants(layer):
    original = layer.original.tocsr()
    spacing = layer.gram_spacing
    row_count = original.shape[0]
    row_norm, first_moment, second_moment = [], [], []
    for row in range(row_count):
        start, end = original.indptr[row:row+2]
        columns = original.indices[start:end]
        weights = abs(original.data[start:end])
        positions = layer.radii[columns]
        centre = (min(positions)+max(positions))/2
        distance = abs(positions-centre)/spacing
        row_norm.append(float(np.sum(weights)))
        first_moment.append(float(weights @ distance))
        second_moment.append(float(weights @ distance**2/2))
    absolute = abs(original)
    source_rows = (np.asarray(absolute @ (layer.radii < layer.anchor)).ravel() > 0)
    source_rows &= np.asarray(absolute @ (layer.radii > layer.anchor)).ravel() > 0
    hinge = layer.lifted_hinge
    maximum_hinge = float(np.max(abs(hinge), initial=0.)/spacing)
    maximum_second = max(second_moment, default=0.)
    return dict(row_count=row_count, source_rows=source_rows, source_count=int(np.sum(source_rows)),
        row_l1=max(row_norm, default=0.), column_l1=float(np.max(np.asarray(absolute.sum(axis=0)), initial=0.)),
        first_moment=max(first_moment, default=0.), second_moment=maximum_second,
        hinge_over_h=maximum_hinge, field_factor_constant=maximum_second+2*maximum_hinge,
        constant_annihilation=float(np.max(abs(original @ np.ones(layer.count)), initial=0.)),
        affine_annihilation=float(np.max(abs(original @ layer.radii), initial=0.)))


def consistency_bound(layer, coordinates, projection, operator, geometry_bounds, field_bounds, epsilon=.05):
    constants = uniform_constants(epsilon)
    spacing = layer.gram_spacing
    curvature, gradient = field_bounds['curvature'], field_bounds['gradient']
    maximum_map = geometry_bounds['maximum_transport_map']
    map_derivative = geometry_bounds['maximum_transport_map_derivative']
    lipschitz = map_derivative*gradient+maximum_map*curvature
    interpolation_remainder = 3*maximum_map*curvature+1.25*lipschitz
    velocity_bound = constants['nodal_projection_stability']*maximum_map*(gradient+3*spacing*curvature)
    source = int(np.searchsorted(layer.edges, layer.anchor))
    source_lengths = np.diff(layer.edges)[source-1:source+1]
    jump_bound = 5*np.sum(1/source_lengths)*velocity_bound
    coefficient_bound = geometry_bounds['maximum_Gram_coefficient']
    field_constant = operator['field_factor_constant']
    factor_bound = field_constant*curvature*spacing**2
    source_bound = coefficient_bound*operator['source_count']*factor_bound/spacing*(
        operator['row_l1']*velocity_bound+operator['hinge_over_h']*spacing*jump_bound)
    remaining = operator['row_count']-operator['source_count']
    far_sum_bound = remaining*spacing*(operator['first_moment']*lipschitz
        +operator['row_l1']*constants['nodal_projection_stability']*interpolation_remainder)
    far_sum_bound += maximum_map*gradient*operator['column_l1']*constants['source_pair_l1_bound']
    far_bound = coefficient_bound*factor_bound*far_sum_bound/spacing
    shape_bound = geometry_bounds['maximum_log_weight_derivative']*coefficient_bound*operator['row_count']*factor_bound**2/(2*spacing)
    values = coordinates[:-1]
    mapped, jacobian, unused = layer.mapping(layer.radii, coordinates[-1])
    weights = np.asarray(layer.sampling @ (layer.coefficient(0., mapped)/jacobian))/spacing
    factors = layer.lifted @ values
    tail = ~operator['source_rows']
    rounded_hinge = float(np.sum(weights[tail]*abs(factors[tail]*layer.lifted_hinge[tail]))*abs(layer.jump @ projection['projection']))
    return dict(source_bound=float(source_bound), remaining_bound=float(far_bound),
        shape_bound=float(shape_bound), numerical_hinge_tail=float(rounded_hinge),
        total_bound=float(source_bound+far_bound+shape_bound+rounded_hinge),
        field_factor_bound=float(factor_bound), field_factor_maximum=float(np.max(abs(factors), initial=0.)),
        transport_lipschitz=float(lipschitz), projected_velocity_bound=float(velocity_bound),
        projection_interpolation_remainder_bound=float(constants['nodal_projection_stability']*spacing*interpolation_remainder),
        source_lengths=source_lengths.tolist(), h_squared_over_minimum_source=float(spacing**2/min(source_lengths)),
        constants=constants)
