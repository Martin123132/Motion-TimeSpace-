import numpy as np
from scipy.linalg import cholesky, eigh, solve, solve_triangular
from annular_boundary_response_20260916 import field_matrices, matrix_derivatives, nested_coordinates


def maximum(values):
    return float(np.max(abs(np.asarray(values)), initial=0.))


def operator_norm(matrix):
    return float(np.linalg.norm(matrix, ord=2))


def energy_norm(position, velocity, stiffness, mass):
    value = np.einsum('...i,ij,...j->...', position, stiffness, position)
    value += np.einsum('...i,ij,...j->...', velocity, mass, velocity)
    return np.sqrt(np.maximum(value, 0.))


def modes(mass, stiffness):
    values, vectors = eigh(stiffness, mass)
    if values[0] <= 0:
        raise ValueError('This energy bound requires strictly positive finite mass and stiffness.')
    return np.sqrt(values), vectors


def evolution(mass, frequencies, vectors, initial_position, initial_velocity, times):
    position_amplitude = vectors.T @ mass @ initial_position
    velocity_amplitude = vectors.T @ mass @ initial_velocity
    phase = times[:, None]*frequencies
    position = np.cos(phase)*position_amplitude+np.sin(phase)*(velocity_amplitude/frequencies)
    velocity = -np.sin(phase)*(frequencies*position_amplitude)+np.cos(phase)*velocity_amplitude
    acceleration = -position*frequencies**2
    return position @ vectors.T, velocity @ vectors.T, acceleration @ vectors.T


def build_reduction(coarse, fine, retain_local=None):
    matrices = field_matrices(fine, fine.anchor)
    derivatives = matrix_derivatives(fine, fine.anchor)
    mass, stiffness, transport = [matrices[name].toarray() for name in ['mass', 'stiffness', 'transport']]
    embedding, bubbles, retained, new = nested_coordinates(coarse, fine)
    embedding, bubbles = embedding.toarray(), bubbles.toarray()
    local_mass = bubbles.T @ mass @ bubbles
    local_stiffness = bubbles.T @ stiffness @ bubbles
    coupling_stiffness = bubbles.T @ stiffness @ embedding
    static_map = embedding-bubbles @ solve(local_stiffness, coupling_stiffness, assume_a='pos')
    local_frequencies, local_vectors = modes(local_mass, local_stiffness)
    chosen = [] if retain_local is None else list(retain_local)
    trial = np.column_stack([static_map, bubbles @ local_vectors[:, chosen]]) if chosen else static_map
    reduced_mass = trial.T @ mass @ trial
    reduced_stiffness = trial.T @ stiffness @ trial
    full_frequencies, full_vectors = modes(mass, stiffness)
    reduced_frequencies, reduced_vectors = modes(reduced_mass, reduced_stiffness)
    residual_map = stiffness @ trial-mass @ trial @ solve(reduced_mass, reduced_stiffness, assume_a='pos')
    root_mass = cholesky(mass, lower=True)
    energy_basis = reduced_vectors/reduced_frequencies
    residual_operator = solve_triangular(root_mass, residual_map @ energy_basis, lower=True)
    current_operator = solve_triangular(root_mass, transport @ trial @ energy_basis, lower=True)
    inverse_transport = solve(mass, transport, assume_a='pos')
    position_load = -derivatives['stiffness'].toarray()+stiffness @ inverse_transport+inverse_transport.T @ stiffness
    velocity_load = derivatives['mass'].toarray()-transport-transport.T
    position_load = (position_load+position_load.T)/2
    velocity_load = (velocity_load+velocity_load.T)/2
    load_norm = max(maximum(eigh(position_load, stiffness, eigvals_only=True)), maximum(eigh(velocity_load, mass, eigvals_only=True)))
    return dict(mass=mass, stiffness=stiffness, transport=transport, mass_b=derivatives['mass'].toarray(),
        stiffness_b=derivatives['stiffness'].toarray(), embedding=embedding, bubbles=bubbles, static_map=static_map,
        trial=trial, reduced_mass=reduced_mass, reduced_stiffness=reduced_stiffness,
        full_frequencies=full_frequencies, full_vectors=full_vectors,
        reduced_frequencies=reduced_frequencies, reduced_vectors=reduced_vectors,
        local_frequencies=local_frequencies, retained_local_modes=chosen, local_count=len(new),
        residual_map=residual_map, root_mass=root_mass, residual_norm=operator_norm(residual_operator),
        current_norm=operator_norm(current_operator), load_norm=load_norm,
        position_load=position_load, velocity_load=velocity_load)


def initial_projection(data, position, velocity):
    trial = data['trial']
    reduced_position = solve(data['reduced_stiffness'], trial.T @ data['stiffness'] @ position, assume_a='pos')
    reduced_velocity = solve(data['reduced_mass'], trial.T @ data['mass'] @ velocity, assume_a='pos')
    return reduced_position, reduced_velocity


def source_load(data, position, velocity, acceleration):
    value = np.einsum('...i,ij,...j->...', velocity, data['mass_b']/2-data['transport'], velocity)
    value -= np.einsum('...i,ij,...j->...', position, data['stiffness_b']/2, position)
    value -= np.einsum('...i,ij,...j->...', acceleration, data['transport'], position)
    return value


def on_shell_load(data, position, velocity):
    return (np.einsum('...i,ij,...j->...', position, data['position_load'], position)
            +np.einsum('...i,ij,...j->...', velocity, data['velocity_load'], velocity))/2


def retarded_error(data, reduced_position, reduced_velocity, error_position, error_velocity, times):
    full_frequencies = data['full_frequencies'][:, None]
    reduced_frequencies = data['reduced_frequencies'][None, :]
    full_vectors, reduced_vectors = data['full_vectors'], data['reduced_vectors']
    amplitude = reduced_vectors.T @ data['reduced_mass'] @ reduced_position
    speed = reduced_vectors.T @ data['reduced_mass'] @ reduced_velocity
    forcing = -full_vectors.T @ data['residual_map'] @ reduced_vectors
    cosine_forcing = forcing*amplitude
    sine_forcing = forcing*(speed/data['reduced_frequencies'])
    homogeneous_position, homogeneous_velocity, unused = evolution(data['mass'], data['full_frequencies'], full_vectors,
        error_position, error_velocity, times)
    forced_positions, forced_velocities = [], []
    for instant in times:
        summed = full_frequencies+reduced_frequencies
        half_difference = (full_frequencies-reduced_frequencies)*instant/2
        averaged = summed*instant/2
        stable_sinc = np.sinc(half_difference/np.pi)
        cosine_response = instant*np.sin(averaged)*stable_sinc/summed
        sine_response = (-instant*np.cos(averaged)*stable_sinc+np.sin(full_frequencies*instant)/full_frequencies)/summed
        cosine_velocity = (full_frequencies*instant*np.cos(averaged)*stable_sinc+np.sin(reduced_frequencies*instant))/summed
        sine_velocity = reduced_frequencies*cosine_response
        forced_positions.append(full_vectors @ np.sum(cosine_forcing*cosine_response+sine_forcing*sine_response, axis=1))
        forced_velocities.append(full_vectors @ np.sum(cosine_forcing*cosine_velocity+sine_forcing*sine_velocity, axis=1))
    return (homogeneous_position+forced_positions, homogeneous_velocity+forced_velocities,
            homogeneous_position, homogeneous_velocity)
