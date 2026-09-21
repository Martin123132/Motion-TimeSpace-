import numpy as np


def one_side_fields(system, geometry, label, side, coordinate):
    interpolation = geometry.material.interpolation([label])[0]
    fields = interpolation @ geometry.fields[:, side].reshape(system.layer_degree+1, -1)
    coefficients = fields.reshape(2, system.count) @ system.spatial_rule.inverse.T
    plus, minus = np.polynomial.chebyshev.chebval(2*np.asarray(coordinate)-1, coefficients.T)
    source = geometry.material.values([label])[0]
    lower, upper = (system.inner+system.width*label, source[0]) if side == 0 else (source[0], system.outer+system.width*label)
    radius = lower+(upper-lower)*np.asarray(coordinate)
    lapse, root = geometry.metric(radius)
    return np.array([lapse*root*(plus+minus)/2, (plus-minus)/2])


def sample_geometry_fast(system, geometry, radius, labels):
    radius, labels = np.broadcast_arrays(radius, labels)
    output = np.zeros((2, len(radius)))
    for label in np.unique(labels):
        source = geometry.material.values([label])[0]
        for side in [0, 1]:
            selected = (labels == label) & ((radius < source[0]) if side == 0 else (radius >= source[0]))
            lower, upper = (system.inner+system.width*label, source[0]) if side == 0 else (source[0], system.outer+system.width*label)
            coordinate = (radius[selected]-lower)/(upper-lower)
            output[:, selected] = one_side_fields(system, geometry, label, side, coordinate)
    return output[0], output[1]


def jump_aware_difference(first, first_states, second, second_states):
    points, weights = np.polynomial.legendre.leggauss(4)
    rows = []
    for coarse_state, fine_state in zip(first_states, second_states):
        coarse_geometry, fine_geometry = first.solve(coarse_state), second.solve(fine_state)
        aligned_error, relative_error, absolute_l2_error, maximum_gap = 0., 0., 0., 0.
        pointwise_gap_error = 0.
        for label in [-.25, 0., .25]:
            source_first = coarse_geometry.material.values([label])[0]
            source_second = fine_geometry.material.values([label])[0]
            coordinate = (1-np.cos(np.pi*np.arange(1537)/1536))/2
            endpoints = []
            for side in [0, 1]:
                field_first = one_side_fields(first, coarse_geometry, label, side, coordinate)
                field_second = one_side_fields(second, fine_geometry, label, side, coordinate)
                aligned_error = max(aligned_error, float(np.max(abs(field_first-field_second))))
                for system, source in [(first, source_first), (second, source_second)]:
                    lower, upper = (system.inner+system.width*label, source[0]) if side == 0 else (source[0], system.outer+system.width*label)
                    endpoints.extend(lower+(upper-lower)*system.coordinate)
            endpoints = np.unique(endpoints)
            lengths = np.diff(endpoints)
            radius = ((endpoints[:-1, None]+endpoints[1:, None])/2+lengths[:, None]*points/2).ravel()
            quadrature = (lengths[:, None]*weights/2).ravel()
            labels = np.full(len(radius), label)
            fields_first = np.array(sample_geometry_fast(first, coarse_geometry, radius, labels))
            fields_second = np.array(sample_geometry_fast(second, fine_geometry, radius, labels))
            lapse, root = fine_geometry.metric(radius)
            norms = np.stack([radius**2/(lapse*root), radius**2*lapse*root])
            error_squared = np.dot(quadrature, np.sum(norms*(fields_first-fields_second)**2, axis=0))
            target_squared = np.dot(quadrature, np.sum(norms*fields_second**2, axis=0))
            relative_error = max(relative_error, float(np.sqrt(error_squared/target_squared)))
            absolute_l2_error = max(absolute_l2_error, float(np.sqrt(np.dot(quadrature, np.sum((fields_first-fields_second)**2, axis=0)))))
            gap = abs(source_first[0]-source_second[0])
            maximum_gap = max(maximum_gap, gap)
            if gap > 2e-15:
                middle = np.array([(source_first[0]+source_second[0])/2])
                first_gap = np.array(sample_geometry_fast(first, coarse_geometry, middle, np.array([label])))
                second_gap = np.array(sample_geometry_fast(second, fine_geometry, middle, np.array([label])))
                pointwise_gap_error = max(pointwise_gap_error, float(np.max(abs(first_gap-second_gap))))
        rows.append(dict(aligned_field_error=aligned_error, physical_relative_L2_error=relative_error,
                         physical_absolute_L2_error=absolute_l2_error, maximum_source_gap=maximum_gap,
                         pointwise_error_inside_gap=pointwise_gap_error))
    return rows
