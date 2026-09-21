import numpy as numerical
from scipy.linalg import eigh, eigvalsh, solve


def modal_system(mass, stiffness, endpoint_lift):
    eigenvalues, vectors = eigh(stiffness, mass)
    if numerical.min(eigenvalues) <= 0:
        raise ValueError('Positive restricted mass/stiffness pair required.')
    frequencies = numerical.sqrt(eigenvalues)
    modal_lift = vectors.T @ mass @ endpoint_lift
    return {'frequencies': frequencies, 'vectors': vectors, 'lift': modal_lift}


def constant_response(modal, endpoints, duration):
    frequencies = modal['frequencies']
    forcing = modal['lift'] @ endpoints
    phase = frequencies * duration
    first = numerical.sin(phase) * forcing
    second = -2 * numerical.sin(phase / 2)**2 * forcing
    return {'g': modal['vectors'] @ (first / frequencies), 'h': modal['vectors'] @ second, 'energy': .5 * float(first @ first + second @ second), 'modal_energy_vector': numerical.concatenate([first, second]), 'uniform_data_bound': 2 * float(forcing @ forcing)}


def affine_response(modal, initial, final, duration):
    if duration <= 0:
        raise ValueError('Positive duration required.')
    frequencies = modal['frequencies']
    start = modal['lift'] @ initial
    rate = modal['lift'] @ ((final - initial) / duration)
    phase = frequencies * duration
    sine_integral = 2 * numerical.sin(phase / 2)**2 / frequencies
    cosine_minus_one_integral = duration * (numerical.sinc(phase / numerical.pi) - 1)
    first = numerical.sin(phase) * start + sine_integral * rate
    second = -2 * numerical.sin(phase / 2)**2 * start + cosine_minus_one_integral * rate
    return {'g': modal['vectors'] @ (first / frequencies), 'h': modal['vectors'] @ second, 'energy': .5 * float(first @ first + second @ second), 'modal_energy_vector': numerical.concatenate([first, second])}


def input_gramian(modal, duration):
    frequencies = modal['frequencies']
    coupling = frequencies[:, None] * modal['lift']
    overlaps = coupling @ coupling.T
    frequency_sum = frequencies[:, None] + frequencies[None, :]
    frequency_difference = frequencies[:, None] - frequencies[None, :]

    def cosine_integral(frequency):
        return duration * numerical.sinc(frequency * duration / numerical.pi)

    def sine_integral(frequency):
        return .5 * frequency * duration**2 * numerical.sinc(frequency * duration / (2 * numerical.pi))**2

    cosine = .5 * overlaps * (cosine_integral(frequency_difference) + cosine_integral(frequency_sum))
    sine = .5 * overlaps * (cosine_integral(frequency_difference) - cosine_integral(frequency_sum))
    mixed = -.5 * overlaps * (sine_integral(frequency_sum) - sine_integral(frequency_difference))
    result = numerical.block([[cosine, mixed], [mixed.T, sine]])
    return (result + result.T) / 2


def gramian_quadrature(modal, duration, order):
    gauss, weights = numerical.polynomial.legendre.leggauss(order)
    times = duration * (gauss + 1) / 2
    weights = weights * duration / 2
    frequencies = modal['frequencies']
    coupling = frequencies[:, None] * modal['lift']
    phase = times[:, None] * frequencies
    kernels = numerical.concatenate([numerical.cos(phase)[:, :, None] * coupling, -numerical.sin(phase)[:, :, None] * coupling], axis=1)
    return numerical.einsum('t,tik,tjk->ij', weights, kernels, kernels, optimize=True)


def corrected_work(mass, stiffness, mass_time, stiffness_time, operators, graph, velocity, source, residual, endpoint_source, memory_graph, memory_velocity):
    operator = operators['L']
    graph_transport, velocity_transport = operators['configuration_transport'], operators['velocity_transport']
    graph_time = velocity + graph_transport @ graph + source
    velocity_time = -operator @ graph + velocity_transport @ velocity + residual
    memory_graph_time = memory_velocity + graph_transport @ memory_graph + endpoint_source
    memory_velocity_time = -operator @ memory_graph + velocity_transport @ memory_velocity
    corrected_graph, corrected_velocity = graph - memory_graph, velocity - memory_velocity
    corrected_graph_time, corrected_velocity_time = graph_time - memory_graph_time, velocity_time - memory_velocity_time
    regular_source = source - endpoint_source
    corrected_energy = .5 * (corrected_graph @ stiffness @ corrected_graph + corrected_velocity @ mass @ corrected_velocity)
    memory_energy = .5 * (memory_graph @ stiffness @ memory_graph + memory_velocity @ mass @ memory_velocity)
    original_energy = .5 * (graph @ stiffness @ graph + velocity @ mass @ velocity)
    direct_rate = corrected_graph @ stiffness @ corrected_graph_time + .5 * corrected_graph @ stiffness_time @ corrected_graph + corrected_velocity @ mass @ corrected_velocity_time + .5 * corrected_velocity @ mass_time @ corrected_velocity
    work = corrected_graph @ operators['configuration_form'] @ corrected_graph + corrected_velocity @ operators['velocity_form'] @ corrected_velocity + corrected_graph @ stiffness @ regular_source + corrected_velocity @ mass @ residual
    source_norm = numerical.sqrt(max(float(regular_source @ stiffness @ regular_source + residual @ mass @ residual), 0.))
    upper = operators['growth_rate'] * corrected_energy + numerical.sqrt(2 * corrected_energy) * source_norm
    memory_rate = memory_graph @ stiffness @ memory_graph_time + .5 * memory_graph @ stiffness_time @ memory_graph + memory_velocity @ mass @ memory_velocity_time + .5 * memory_velocity @ mass_time @ memory_velocity
    cross = graph @ stiffness @ memory_graph + velocity @ mass @ memory_velocity
    correction = memory_energy - cross
    return {'energy': float(corrected_energy), 'direct_rate': float(direct_rate), 'work_rate': float(work), 'rate_upper': float(upper), 'remaining_source_norm': float(source_norm), 'memory_energy': float(memory_energy), 'memory_rate': float(memory_rate), 'original_energy': float(original_energy), 'correction': float(correction), 'memory_graph_time': memory_graph_time, 'memory_velocity_time': memory_velocity_time, 'corrected_graph': corrected_graph, 'corrected_velocity': corrected_velocity, 'corrected_graph_time': corrected_graph_time, 'corrected_velocity_time': corrected_velocity_time, 'triangle_bound': float((numerical.sqrt(corrected_energy) + numerical.sqrt(memory_energy))**2)}


def input_sampling_bound(modal, duration, bin_width):
    if duration <= 0 or bin_width <= 0:
        raise ValueError('Positive time and bin width required.')
    frequencies = modal['frequencies']
    weights = numerical.sum((frequencies[:, None] * modal['lift'])**2, axis=1)
    bins = numerical.floor(frequencies / bin_width).astype(int)
    totals = numerical.bincount(bins, weights=weights)
    maximum = float(numerical.max(totals))
    bound = 4 * numerical.pi * maximum * (1 / bin_width + bin_width * duration**2)
    return {'maximum_band_weight': maximum, 'sufficient_gramian_bound': bound, 'bin_width': float(bin_width), 'maximum_bin': int(numerical.argmax(totals))}
