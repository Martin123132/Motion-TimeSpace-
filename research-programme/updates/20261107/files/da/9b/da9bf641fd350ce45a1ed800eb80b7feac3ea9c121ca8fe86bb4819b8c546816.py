from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_Legendre_current_20260921 import samples, wave_data
from annular_candidate_Ward_source_20260921 import fields
from annular_radial_Ward_moments_20260921 import prepare
import numpy as np


def gram_pairs(action):
    factor = action.factor
    sampling = action.sampling.tocsr()
    bonds, atoms, nodes, coefficients = [], [], [], []
    for entry, bond in enumerate(factor.rows):
        for pointer in range(sampling.indptr[bond], sampling.indptr[bond + 1]):
            bonds.append(bond)
            atoms.append(sampling.indices[pointer])
            nodes.append(factor.columns[entry])
            coefficients.append(sampling.data[pointer] * float(factor.values[entry]))
    return tuple(np.array(value, dtype=float if index == 3 else int)
                 for index, value in enumerate([bonds, atoms, nodes, coefficients]))


def cell_channels(action, tangent, kernel, acceleration, polynomial, label, targets=None, levels=(1,)):
    row = samples(action, label, 12, targets=targets)
    quadrature, geometry, cardinal = row['quadrature'], row['geometry'], row['cardinal']
    cells, local, measure = quadrature['cells'], quadrature['local'], quadrature['measure']
    values = fields(action, quadrature['reference'], cells, local, label)
    coefficients = np.einsum('cpl,l->cp', polynomial, cardinal)[cells]
    field_acceleration = coefficients[:, 0] + local * (coefficients[:, 1] + local * coefficients[:, 2])
    source_acceleration = acceleration[:, -1] @ cardinal
    momentum_rate = wave_data(row, tangent)['momentum_rate'][-1]
    momentum_rate += geometry['kinetic'] * (field_acceleration + source_acceleration * row['motion'])
    euler = -momentum_rate - values['flux_x']
    primitive = kernel.anchored(geometry['radius'], row['source'])
    rate_coefficients = np.einsum('cpl,l->cp', action.rate_polynomial, cardinal)
    reference_rate = values['reference_rate']
    edges = np.array([float(value) for value in action.edges])
    interpolation, absolute_interpolation = [], []
    for level in levels:
        grid = np.arange(2 * level + 1) / (2 * level)
        references = edges[:-1, None] + np.diff(edges)[:, None] * grid
        physical_nodes = action.geometry(references.ravel(), row['source'], label)['radius']
        node_primitive = kernel.anchored(physical_nodes, row['source']).reshape(3, len(edges) - 1, -1)
        node_rate = rate_coefficients[:, 0, None] + grid * (rate_coefficients[:, 1, None] + grid * rate_coefficients[:, 2, None])
        product = node_primitive * node_rate
        subcell = np.minimum(np.floor(local * level).astype(int), level - 1)
        position = local * level - subcell
        shape = np.array([(1-position)*(1-2*position), 4*position*(1-position), position*(2*position-1)])
        projected = sum(product[:, cells, 2*subcell + vertex] * shape[vertex] for vertex in range(3))
        integrand = measure * euler * (projected - reference_rate * primitive)
        interpolation.append(np.sum(integrand, axis=1))
        absolute_interpolation.append(np.sum(abs(integrand), axis=1))
    transport_integrand = measure * euler * values['speed'] * values['gradient'] * primitive
    return row, dict(interpolation=np.array(interpolation), absolute_interpolation=np.array(absolute_interpolation),
        transport=np.sum(transport_integrand, axis=1), transport_absolute=np.sum(abs(transport_integrand), axis=1))


def layer_channels(action, loads, tangent, kernel, acceleration, polynomial, pairs, label):
    row, cell = cell_channels(action, tangent, kernel, acceleration, polynomial, label)
    edges = np.array([float(value) for value in action.edges])
    indices = np.arange(len(edges) - 1)
    left = fields(action, edges[:-1], indices, np.zeros(len(indices)), label)
    right = fields(action, edges[1:], indices, np.ones(len(indices)), label)
    speed = (right['speed'][:-1] + left['speed'][1:]) / 2
    average_gradient = (right['gradient'][:-1] + left['gradient'][1:]) / 2
    jump = left['gradient'][1:] - right['gradient'][:-1]
    face_euler = (left['beta'][1:] - left['alpha'][1:]*speed**2) * jump
    face_integrand = face_euler * speed * average_gradient * kernel.anchored(right['radius'][:-1], row['source'])
    face = np.sum(face_integrand, axis=1)
    endpoint = np.zeros(3)
    for sign, edge, index in [(-1, left, 0), (1, right, -1)]:
        primitive = kernel.anchored(np.array([edge['radius'][index]]), row['source'])[:, 0]
        force = -edge['alpha'][index]*edge['temporal'][index]*edge['speed'][index] - edge['beta'][index]*edge['gradient'][index]
        endpoint += sign * (force*edge['reference_rate'][index] - edge['physical_flux'][index]) * primitive
    nodal = action.geometry(action.knots, row['source'], label)
    node_primitive = kernel.anchored(nodal['radius'], row['source'])
    rate = row['cardinal'] @ loads.rates[:, :-1]
    image = action.factor_values @ row['cardinal']
    load = np.asarray(action.sampling.T @ (image**2 / 2))
    bonds, atoms, nodes, coefficients = pairs
    pair_values = image[bonds] * coefficients * nodal['gradient'][atoms] * rate[nodes]
    bond_integrand = pair_values * (node_primitive[:, atoms] - node_primitive[:, nodes])
    gram_bond = bond_integrand.sum(axis=1)
    gram_geometry = (node_primitive * row['velocity'] * nodal['gradient_source'] * load).sum(axis=1)
    gram_advection = (kernel.at(nodal['radius']) * nodal['displacement'] * row['velocity'] * nodal['gradient'] * load).sum(axis=1)
    components = np.array([cell['interpolation'][0], cell['transport'], face, endpoint, gram_bond, gram_geometry, gram_advection])
    return dict(components=components, predicted_wave=components[:4].sum(axis=0),
        predicted_gram=components[4:].sum(axis=0), predicted_total=components.sum(axis=0),
        interpolation_absolute=cell['absolute_interpolation'][0], transport_absolute=cell['transport_absolute'],
        face_absolute=np.sum(abs(face_integrand), axis=1), bond_absolute=np.sum(abs(bond_integrand), axis=1))


def refined_product(action, tangent, kernel, acceleration, polynomial, label):
    cardinal = np.asarray(action.cardinal(label)).ravel()
    source = cardinal @ action.source
    edges = np.array([float(value) for value in action.edges])
    references = edges[:-1, None] + np.diff(edges)[:, None] * np.arange(5)/4
    targets = action.geometry(references.ravel(), source, label)['radius']
    unused, values = cell_channels(action, tangent, kernel, acceleration, polynomial, label,
                                  targets=targets, levels=(1, 2, 4))
    return dict(interpolation=values['interpolation'], absolute_interpolation=values['absolute_interpolation'])
