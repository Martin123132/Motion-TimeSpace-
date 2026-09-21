from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_weighted_projection_bounds_20260919 import band_action
from scipy.linalg import solve_banded
import numpy as np


def stiffness_weights(layer, position):
    radius, jacobian, unused = layer.mapping(layer.reference_radius, position)
    gradient = layer.reference_weight*layer.coefficient(0., radius)/jacobian
    nodes, nodal_jacobian, unused = layer.mapping(layer.radii, position)
    gram = np.asarray(layer.sampling @ (layer.coefficient(0., nodes)/nodal_jacobian))/layer.gram_spacing
    return dict(gradient=gradient, gram=gram)


def stiffness_terms(layer, weights, values):
    gradient = np.sum(layer.reference_radial*values[layer.reference_indices], axis=1)
    factor = np.asarray(layer.lifted @ values).ravel()
    gradient_load = layer.assemble_quadratic(layer.reference_indices, layer.reference_radial*(weights['gradient']*gradient)[:, None])
    gram_load = np.asarray(layer.lifted.T @ (weights['gram']*factor)).ravel()
    return dict(gradient_load=gradient_load, gram_load=gram_load, load=gradient_load+gram_load,
        gradient_energy=.5*float(np.sum(weights['gradient']*gradient**2)),
        gram_energy=.5*float(np.sum(weights['gram']*factor**2)), gradient=gradient, factor=factor)


def source_kinetic_force(layer, values, rates, data):
    radius, jacobian, motion = layer.mapping(layer.reference_radius, values[-1])
    temporal_weight = layer.reference_weight*jacobian*radius**4/layer.coefficient(0., radius)
    derivative = -motion[:, None]*layer.reference_radial/jacobian[:, None]
    return layer.assemble_quadratic(layer.reference_indices,
        rates[-1]*derivative*(temporal_weight*data['field_time'])[:, None])


def wave_residual_channels(coarse, fine, coarse_weights, fine_weights, transfer):
    coarse_stiffness = stiffness_terms(coarse['layer'], coarse_weights, coarse['values'][:-1])
    transferred_stiffness = stiffness_terms(fine['layer'], fine_weights, transfer(coarse['values'][:-1]))

    def covector_transfer(load):
        velocity = solve_banded((2, 2), coarse['data']['mass_bands'], load, check_finite=False)
        return band_action(fine['data']['mass_bands'], transfer(velocity))

    def load_difference(coarse_load, fine_load):
        return fine_load-covector_transfer(coarse_load)

    channels = dict(gradient_stiffness_transfer=covector_transfer(coarse_stiffness['gradient_load'])-transferred_stiffness['gradient_load'],
        Gram_stiffness_transfer=covector_transfer(coarse_stiffness['gram_load'])-transferred_stiffness['gram_load'])
    local = []
    for item in [coarse, fine]:
        local.append(dict(source_kinetic=source_kinetic_force(item['layer'], item['values'], item['rates'], item['data']),
            cross_transport=-item['cross_rate']*item['rates'][-1],
            source_acceleration=-item['data']['cross']*item['source_acceleration'],
            mass_transport=-band_action(item['mass_rate'], item['rates'][:-1]),
            inverse_residual=-item['inverse_residual_rate']))
    for name in local[0]:
        channels[name] = load_difference(local[0][name], local[1][name])
    return channels


def wave_energy(layer, mass_bands, weights, displacement, velocity):
    stiffness = stiffness_terms(layer, weights, displacement)
    kinetic = .5*float(velocity @ band_action(mass_bands, velocity))
    return dict(kinetic=kinetic, gradient=stiffness['gradient_energy'], Gram=stiffness['gram_energy'],
        total=kinetic+stiffness['gradient_energy']+stiffness['gram_energy'])
