import numpy as np
from scipy.linalg import eigh, svd
from annular_boundary_response_20260916 import field_matrices, matrix_derivatives


def maximum(values):
    return float(np.max(abs(np.asarray(values)), initial=0.))


def spectral_clusters(values, relative_gap=1e-6):
    if relative_gap < 0:
        raise ValueError('Cluster tolerance must be nonnegative.')
    clusters = [[0]]
    for index in range(1, len(values)):
        scale = max(1., abs(values[index-1]), abs(values[index]))
        if values[index]-values[index-1] <= relative_gap*scale:
            clusters[-1].append(index)
        else:
            clusters.append([index])
    return clusters


def differentiated_frame(mass, stiffness, mass_b, stiffness_b, relative_gap=1e-6):
    values, vectors = eigh(stiffness, mass)
    if values[0] <= 0:
        raise ValueError('A positive field spectrum is required.')
    clusters = spectral_clusters(values, relative_gap)
    labels = np.empty(len(values), dtype=int)
    for label, cluster in enumerate(clusters):
        labels[cluster] = label
    modal_mass_b = vectors.T @ mass_b @ vectors
    modal_stiffness_b = vectors.T @ stiffness_b @ vectors
    within = labels[:, None]==labels[None, :]
    gaps = values[None, :]-values[:, None]
    connection = -modal_mass_b/2
    numerator = modal_stiffness_b-modal_mass_b*values[None, :]
    connection[~within] = numerator[~within]/gaps[~within]
    vectors_b = vectors @ connection
    block_stiffness_b = modal_stiffness_b+connection.T*values[None, :]+values[:, None]*connection
    return dict(values=values, vectors=vectors, vectors_b=vectors_b, connection=connection,
        block_stiffness_b=block_stiffness_b, clusters=clusters, labels=labels, within=within,
        minimum_external_gap=float(np.min(abs(gaps[~within]))) if np.any(~within) else None,
        mass_b_modal=modal_mass_b, stiffness_b_modal=modal_stiffness_b)


def system_frame(system, position, relative_gap=1e-6):
    matrices = field_matrices(system, position)
    derivatives = matrix_derivatives(system, position)
    matrices = {name: value.toarray() if hasattr(value, 'toarray') else value for name, value in matrices.items()}
    derivatives = {name: value.toarray() for name, value in derivatives.items()}
    frame = differentiated_frame(matrices['mass'], matrices['stiffness'], derivatives['mass'], derivatives['stiffness'], relative_gap)
    vectors, vectors_b = frame['vectors'], frame['vectors_b']
    mass, transport, square = [matrices[name] for name in ['mass', 'transport', 'transport_square']]
    modal_transport = vectors.T @ mass @ vectors_b+vectors.T @ transport @ vectors
    modal_square = vectors_b.T @ mass @ vectors_b+vectors_b.T @ transport @ vectors
    modal_square += vectors.T @ transport.T @ vectors_b+vectors.T @ square @ vectors
    frame.update(matrices=matrices, derivatives=derivatives, modal_transport=modal_transport, modal_square=modal_square)
    return frame


def aligned_frame(mass, stiffness, reference, reference_mass, clusters):
    values, vectors = eigh(stiffness, mass)
    for cluster in clusters:
        overlap = reference[:, cluster].T @ reference_mass @ vectors[:, cluster]
        left, singular, right_transpose = svd(overlap)
        if singular[-1] < .5:
            raise ValueError('Frame alignment lost its spectral cluster; reduce the step or enlarge the cluster.')
        vectors[:, cluster] = vectors[:, cluster] @ right_transpose.T @ left.T
    return vectors


def finite_frame_jet(system, position, frame, step):
    samples = []
    for multiplier in [-2, -1, 1, 2]:
        matrices = field_matrices(system, position+multiplier*step)
        aligned = aligned_frame(matrices['mass'].toarray(), matrices['stiffness'].toarray(),
            frame['vectors'], frame['matrices']['mass'], frame['clusters'])
        samples.append(aligned)
    first = (samples[0]-8*samples[1]+8*samples[2]-samples[3])/(12*step)
    second = (-samples[0]+16*samples[1]-30*frame['vectors']+16*samples[2]-samples[3])/(12*step**2)
    return first, second


def cluster_projector(vectors, mass, cluster):
    selected = vectors[:, cluster]
    return selected @ selected.T @ mass


def cluster_projector_derivative(frame, mass, mass_b, cluster):
    selected, selected_b = frame['vectors'][:, cluster], frame['vectors_b'][:, cluster]
    return selected_b @ selected.T @ mass+selected @ selected_b.T @ mass+selected @ selected.T @ mass_b


def close_selection_under_clusters(selected, clusters):
    selected = set(selected)
    return sorted({index for cluster in clusters if selected.intersection(cluster) for index in cluster})


def jet_pullback(system, base_position, frame, second, coordinates, rates):
    modal_position, position = coordinates[:-1], coordinates[-1]
    modal_rate, speed = rates[:-1], rates[-1]
    displacement = position-base_position
    vectors = frame['vectors']+displacement*frame['vectors_b']+displacement**2*second/2
    vectors_b = frame['vectors_b']+displacement*second
    physical_position = np.append(vectors @ modal_position, position)
    physical_rate = np.append(vectors @ modal_rate+speed*(vectors_b @ modal_position), speed)
    original = system.evaluate(0., physical_position, physical_rate)
    momenta = np.append(vectors.T @ original['momenta'][:-1],
        original['momenta'][-1]+original['momenta'][:-1] @ (vectors_b @ modal_position))
    return dict(original=original, momenta=momenta, action=original['action'],
        physical_coordinates=physical_position, physical_rates=physical_rate)
