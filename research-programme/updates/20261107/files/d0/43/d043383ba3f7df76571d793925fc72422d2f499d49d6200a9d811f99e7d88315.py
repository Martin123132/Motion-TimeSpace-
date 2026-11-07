from __future__ import annotations

import hashlib
from pathlib import Path
import sys

import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy import sparse
from scipy.integrate import solve_ivp
from scipy.sparse.linalg import splu, spsolve
from scipy.special import wrightomega


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
sys.path.insert(0, str(BRANCH/'axial-companion-20261005'))
from axial_binary import WaveBody, outgoing_samples, horizon_samples


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def radial_coordinate(tortoise, compactness):
    auxiliary = wrightomega(np.log((1-compactness)/compactness)+(np.asarray(tortoise)+1-compactness)/compactness)
    radius = compactness*(1+auxiliary)
    metric = auxiliary/(1+auxiliary)
    return radius, metric


def wave_potential(tortoise, compactness):
    radius, metric = radial_coordinate(tortoise, compactness)
    return metric*(6/radius**2-3*compactness/radius**3)


def element_forms(edges, compactness):
    points, weights = leggauss(6)
    basis = np.array([points*(points-1)/2, 1-points**2, points*(points+1)/2]).T
    slopes = np.array([points-.5, -2*points, points+.5]).T
    mass_values, stiffness_values, row_indices, column_indices = [], [], [], []
    for index, (left, right) in enumerate(zip(edges[:-1], edges[1:])):
        jacobian = (right-left)/2
        locations = (right+left)/2+jacobian*points
        potential = wave_potential(locations, compactness)
        local_mass = np.einsum('q,qi,qj->ij', weights*jacobian, basis, basis)
        local_stiffness = np.einsum('q,qi,qj->ij', weights/jacobian, slopes, slopes)
        local_stiffness += np.einsum('q,qi,qj->ij', weights*jacobian*potential, basis, basis)
        local_indices = np.arange(2*index, 2*index+3)
        row_indices.extend(np.repeat(local_indices, 3))
        column_indices.extend(np.tile(local_indices, 3))
        mass_values.extend(local_mass.ravel())
        stiffness_values.extend(local_stiffness.ravel())
    size = 2*len(edges)-1
    inertia = sparse.coo_matrix((mass_values, (row_indices, column_indices)), shape=(size, size)).tocsr()
    stiffness = sparse.coo_matrix((stiffness_values, (row_indices, column_indices)), shape=(size, size)).tocsr()
    nodes = np.empty(size)
    nodes[::2], nodes[1::2] = edges, (edges[1:]+edges[:-1])/2
    return inertia, stiffness, nodes


def embed(matrix, offset, size):
    entries = matrix.tocoo()
    return sparse.coo_matrix((entries.data, (entries.row+offset, entries.col+offset)), shape=(size, size)).tocsr()


def build_network(kind, settings):
    body = WaveBody(.03)
    compactness = 2*body.mass/body.radius
    source_radius = 2.5
    source_tortoise = source_radius-1+compactness*np.log((source_radius-compactness)/(1-compactness))
    outer = settings['outer']
    first_edges = np.linspace(0., source_tortoise, int(np.ceil(source_tortoise/settings['exterior_step']))+1)
    second_edges = np.linspace(source_tortoise, outer, int(np.ceil((outer-source_tortoise)/settings['exterior_step']))+1)
    edges = np.r_[first_edges, second_edges[1:]]
    exterior_mass, exterior_stiffness, exterior_nodes = element_forms(edges, compactness)
    if kind == 'body':
        archive_path = BRANCH/'causal-axial-20261005/results/spectrum/body-256.npz'
        with np.load(archive_path, allow_pickle=False) as archive:
            count = settings['modes']
            eigenvalues, coupling = archive['eigenvalues'][:count], archive['coupling'][:count]
            interior_mass = sparse.diags(np.r_[np.ones(count), float(archive['norm'])], format='lil')
            interior_mass[:count, count] = coupling[:, None]
            interior_mass[count, :count] = coupling[None, :]
            interior_mass = interior_mass.tocsr()
            interior_stiffness = sparse.diags(np.r_[eigenvalues, float(archive['static_impedance'])], format='csr')
        interior_nodes = np.zeros(count+1)
    else:
        inner = settings['inner']
        inner_edges = np.linspace(inner, 0., int(np.ceil(-inner/settings['interior_step']))+1)
        interior_mass, interior_stiffness, interior_nodes = element_forms(inner_edges, compactness)
        archive_path = body.profile.path
    offset = interior_mass.shape[0]-1
    size = offset+exterior_mass.shape[0]
    inertia = embed(interior_mass, 0, size)+embed(exterior_mass, offset, size)
    stiffness = embed(interior_stiffness, 0, size)+embed(exterior_stiffness, offset, size)
    damping_values = np.zeros(size)
    damping_values[-1] = 1.
    if kind == 'BH':
        damping_values[0] = 1.
    damping = sparse.diags(damping_values, format='csr')
    source_index = offset+2*(len(first_edges)-1)
    force = np.zeros(size)
    force[source_index] = 1.
    return {'kind': kind, 'settings': settings, 'body': body, 'compactness': compactness,
            'mass': inertia, 'stiffness': stiffness, 'damping': damping, 'force': force,
            'interior_mass': interior_mass, 'interior_stiffness': interior_stiffness,
            'exterior_mass': exterior_mass, 'exterior_stiffness': exterior_stiffness,
            'exterior_nodes': exterior_nodes, 'interior_nodes': interior_nodes, 'interface_index': offset,
            'source_index': source_index, 'source_tortoise': source_tortoise,
            'source_radius': source_radius, 'archive_path': archive_path}


def harmonic_response(network, frequency, wrong_surface_contact=False):
    stiffness = network['stiffness']
    if wrong_surface_contact:
        perturbation = np.zeros(stiffness.shape[0])
        perturbation[network['interface_index']] = 3*(1-network['compactness'])
        stiffness = stiffness-sparse.diags(perturbation, format='csr')
    operator = stiffness-frequency**2*network['mass']-1j*frequency*network['damping']
    field = spsolve(operator.tocsc(), network['force'])
    susceptibility = field[network['source_index']]
    outer_loss = frequency**2*abs(field[-1])**2/2
    horizon_loss = frequency**2*abs(field[0])**2/2 if network['kind'] == 'BH' else 0.
    work = frequency*susceptibility.imag/2
    return {'frequency_R': frequency, 'G_real': float(susceptibility.real), 'G_imag': float(susceptibility.imag),
            'source_work': float(work), 'outer_loss': float(outer_loss), 'horizon_loss': float(horizon_loss),
            'optical_identity_relative_error': float(abs(work-outer_loss-horizon_loss)/(outer_loss+horizon_loss))}


def continuum_response(network, frequency):
    compactness = network['compactness']
    source_tortoise = network['source_tortoise']
    settings = network['settings']

    def equation(position, state):
        return [state[1], (wave_potential(position, compactness)-frequency**2)*state[0]]

    def propagate(start, end, state):
        solution = solve_ivp(equation, (start, end), np.asarray(state, dtype=complex), method='DOP853', rtol=3e-12, atol=3e-14)
        assert solution.success
        return solution.y[:, -1]

    outgoing = propagate(settings['outer'], source_tortoise, [1., 1j*frequency])
    body = network['body']
    response, _ = body.solve(frequency, tolerance=8e-14, max_step=1/360, start=5e-6)
    body_state = propagate(0., source_tortoise, [1., response['Y']])
    if network['kind'] == 'body':
        inner_state = body_state
    else:
        inner_state = propagate(settings['inner'], source_tortoise, [1., -1j*frequency])
    finite = 1/(inner_state[1]/inner_state[0]-outgoing[1]/outgoing[0])
    physical_frequency = frequency/body.radius
    source_radius = network['source_radius']*body.radius
    outgoing_infinity, raw_out, _ = outgoing_samples(body.mass, physical_frequency, [source_radius], 65., 16, 8e-14)
    outgoing_slope = body.radius*complex(outgoing_infinity[source_radius][1].real, physical_frequency/abs(raw_out)**2)
    if network['kind'] == 'body':
        inner_slope = body_state[1]/body_state[0]
    else:
        ingoing, raw_horizon, _ = horizon_samples(body.mass, physical_frequency, [source_radius], 2e-6, 16, 8e-14)
        inner_slope = body.radius*complex(ingoing[source_radius][1].real, -physical_frequency/abs(raw_horizon)**2)
    infinite = 1/(inner_slope-outgoing_slope)
    return {'frequency_R': frequency, 'finite_G_real': float(finite.real), 'finite_G_imag': float(finite.imag),
            'infinite_G_real': float(infinite.real), 'infinite_G_imag': float(infinite.imag),
            'finite_to_infinite_complex_relative_difference': float(abs(finite-infinite)/abs(infinite))}


def forcing(time, start=2., duration=12., carrier=.5):
    local = time-start
    return np.sin(np.pi*local/duration)**6*np.cos(carrier*local) if 0 < local < duration else 0.


def evolve(network, step, stop=90., record_every=10):
    inertia, stiffness, damping = network['mass'], network['stiffness'], network['damping']
    size = inertia.shape[0]
    factor = splu((inertia+step*damping/2+step**2*stiffness/4).tocsc(), permc_spec='NATURAL')
    right = inertia-step*damping/2-step**2*stiffness/4
    position, velocity = np.zeros(size), np.zeros(size)
    offset, source_index = network['interface_index'], network['source_index']
    boundary_mass = network['interior_mass'].getrow(offset)
    boundary_stiffness = network['interior_stiffness'].getrow(offset)
    work, outer_loss, horizon_loss, interface_work = 0., 0., 0., 0.
    rows = []

    def snapshot(time):
        inner_position, inner_velocity = position[:offset+1], velocity[:offset+1]
        outer_position, outer_velocity = position[offset:], velocity[offset:]
        interior_energy = .5*(inner_velocity@(network['interior_mass']@inner_velocity)
                              +inner_position@(network['interior_stiffness']@inner_position))
        exterior_energy = .5*(outer_velocity@(network['exterior_mass']@outer_velocity)
                              +outer_position@(network['exterior_stiffness']@outer_position))
        return [time, work, outer_loss, horizon_loss, interior_energy, exterior_energy, interface_work,
                position[offset], position[source_index], position[-1], velocity[-1], velocity[0] if network['kind'] == 'BH' else 0.]

    rows.append(snapshot(0.))
    steps = int(round(stop/step))
    for index in range(steps):
        time = index*step
        force = forcing(time+step/2)
        updated_velocity = factor.solve(right@velocity-step*(stiffness@position)+step*force*network['force'])
        midpoint_velocity = (updated_velocity+velocity)/2
        updated_position = position+step*midpoint_velocity
        midpoint_position = (position+updated_position)/2
        acceleration = (updated_velocity-velocity)/step
        traction = float((boundary_mass@acceleration[:offset+1]+boundary_stiffness@midpoint_position[:offset+1])[0])
        work += step*force*midpoint_velocity[source_index]
        outer_loss += step*midpoint_velocity[-1]**2
        horizon_loss += step*midpoint_velocity[0]**2 if network['kind'] == 'BH' else 0.
        interface_work += step*midpoint_velocity[offset]*traction
        position, velocity = updated_position, updated_velocity
        if (index+1) % record_every == 0 or index+1 == steps:
            rows.append(snapshot((index+1)*step))
    fields = ['time', 'work', 'outer_loss', 'horizon_loss', 'interior_energy', 'exterior_energy',
              'interface_work', 'interface_field', 'source_field', 'outer_field', 'outer_velocity', 'horizon_velocity']
    arrays = dict(zip(fields, np.asarray(rows).T))
    peak = float(np.max(np.abs(arrays['work'])))
    total_residual = arrays['work']-arrays['interior_energy']-arrays['exterior_energy']-arrays['outer_loss']-arrays['horizon_loss']
    interior_residual = arrays['interface_work']-arrays['interior_energy']-arrays['horizon_loss']
    exterior_residual = arrays['work']-arrays['interface_work']-arrays['exterior_energy']-arrays['outer_loss']
    return arrays, {'time_step': step, 'stop': stop, 'unknowns': size,
                    'total_balance_error_over_peak_work': float(np.max(np.abs(total_residual))/peak),
                    'interior_balance_error_over_peak_work': float(np.max(np.abs(interior_residual))/peak),
                    'exterior_balance_error_over_peak_work': float(np.max(np.abs(exterior_residual))/peak),
                    'pre_forcing_field_maximum': float(np.max(np.abs(arrays['source_field'][arrays['time'] <= 2.]))),
                    'minimum_stored_energy': float(min(np.min(arrays['interior_energy']), np.min(arrays['exterior_energy']))),
                    'final_work': float(arrays['work'][-1]), 'final_outer_loss': float(arrays['outer_loss'][-1]),
                    'final_horizon_loss': float(arrays['horizon_loss'][-1]),
                    'final_stored_energy': float(arrays['interior_energy'][-1]+arrays['exterior_energy'][-1])}
