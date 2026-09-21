import numpy as np


def sample_geometry(system, geometry, radius, labels):
    radius, labels = np.broadcast_arrays(radius, labels)
    source = geometry.material.values(labels)
    inner, outer = system.inner+system.width*labels, system.outer+system.width*labels
    result = np.zeros((2, len(radius)))
    for side in [0, 1]:
        selected = radius < source[:, 0] if side == 0 else radius >= source[:, 0]
        lower, upper = (inner, source[:, 0]) if side == 0 else (source[:, 0], outer)
        mapped = 2*(radius[selected]-lower[selected])/(upper[selected]-lower[selected])-1
        label_interpolation = geometry.material.interpolation(labels[selected])
        spatial_interpolation = np.polynomial.chebyshev.chebvander(mapped, system.degree) @ system.spatial_rule.inverse
        for sign in [0, 1]:
            interpolated = label_interpolation @ geometry.fields[:, side, sign]
            result[sign, selected] = np.sum(interpolated*spatial_interpolation, axis=1)
    lapse, root = geometry.metric(radius)
    return lapse*root*(result[0]+result[1])/2, (result[0]-result[1])/2


def oracle_difference(first, first_states, second, second_states):
    differences = []
    for coarse_state, fine_state in zip(first_states, second_states):
        coarse_geometry, fine_geometry = first.solve(coarse_state), second.solve(fine_state)
        maximum_field, maximum_source, maximum_velocity, maximum_clock = 0., 0., 0., 0.
        for label in [-.25, 0., .25]:
            source_first = coarse_geometry.material.values([label])[0]
            source_second = fine_geometry.material.values([label])[0]
            radius = np.unique(np.concatenate([np.linspace(5.2, 6.8, 1001)+first.width*label,
                                               source_first[0]+np.linspace(-.03, .03, 401),
                                               source_second[0]+np.linspace(-.03, .03, 401)]))
            labels = np.full(len(radius), label)
            fields_first = np.array(sample_geometry(first, coarse_geometry, radius, labels))
            fields_second = np.array(sample_geometry(second, fine_geometry, radius, labels))
            maximum_field = max(maximum_field, float(np.max(abs(fields_first-fields_second))))
            maximum_source = max(maximum_source, abs(source_first[0]-source_second[0]))
            maximum_clock = max(maximum_clock, abs(source_first[2]-source_second[2]))
            velocities = []
            for system, geometry, source in [(first, coarse_geometry, source_first), (second, fine_geometry, source_second)]:
                lapse, root = geometry.metric(source[0])
                energy = np.sqrt(system.source_mass**2+root**2*source[1]**2)
                velocities.append(lapse*root**2*source[1]/energy)
            maximum_velocity = max(maximum_velocity, abs(velocities[0]-velocities[1]))
        differences.append([maximum_field, maximum_source, maximum_velocity, maximum_clock])
    return np.asarray(differences)
