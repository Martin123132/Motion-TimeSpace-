from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedP2Material, IndexedP2Geometry
from annular_cut_initial_data_20260915 import compatible_initial_state
from scipy.linalg import solve
import numpy as np


def indexed_initial(system):
    coordinates, rates, unused = compatible_initial_state(system.model, 0.)
    unused, unused2, displacement = system.model.mapping(system.model.radii, system.model.anchor)
    rates[:-1] *= 1-displacement
    coordinates = np.tile(coordinates, (len(system.labels), 1))
    rates = np.tile(rates, (len(system.labels), 1))
    coordinates[:, -1] += system.width*system.labels
    geometry = IndexedP2Geometry(system, IndexedP2Material(system, coordinates), rates)
    momenta = np.array([system.layer(label, geometry).evaluate(0., position, velocity)['momenta']
        for label, position, velocity in zip(system.labels, coordinates, rates)])
    return coordinates, momenta, rates, geometry


def gram_jump_split(layer, values, mass):
    nodes, jacobian, unused = layer.mapping(layer.radii, values[-1])
    weights = np.asarray(layer.sampling @ (layer.coefficient(0., nodes)/jacobian))/layer.gram_spacing
    hinge = np.asarray(layer.lifted_hinge)
    jump = np.asarray(layer.jump)
    scalar = values[:-1]
    original_values = layer.original @ scalar
    jump_value = float(jump @ scalar)
    mixed = np.asarray(layer.original.T @ (weights*hinge))
    coefficient = float(weights @ hinge**2)
    direct_factor = layer.lifted @ scalar
    reconstructed_factor = original_values-hinge*jump_value
    direct_action = np.asarray(layer.lifted.T @ (weights*direct_factor))
    expanded_action = (layer.original.T @ (weights*original_values)
        -mixed*jump_value-jump*(mixed @ scalar)+coefficient*jump*jump_value)
    direct_energy = float(weights @ direct_factor**2/2)
    expanded_energy = float(weights @ original_values**2/2-jump_value*(mixed @ scalar)
        +coefficient*jump_value**2/2)
    inverse_jump = solve(mass, jump, assume_a='pos', check_finite=False)
    jump_dual_norm = float(jump @ inverse_jump)
    source_index = int(np.searchsorted(layer.edges, layer.anchor))
    source_lengths = np.diff(layer.edges)[source_index-1:source_index+1]
    return dict(gram_spacing=float(layer.gram_spacing), row_count=len(weights),
        source_lengths=source_lengths.tolist(), jump_value=jump_value,
        jump_penalty_coefficient=coefficient, jump_mass_dual_norm=jump_dual_norm,
        isolated_jump_dyad_frequency=float(np.sqrt(max(0., coefficient*jump_dual_norm))),
        isolated_dyad_not_full_spectral_bound=True,
        gram_energy=direct_energy, expanded_gram_energy=expanded_energy,
        factor_identity_error=float(np.max(abs(direct_factor-reconstructed_factor), initial=0.)),
        action_identity_error=float(np.max(abs(direct_action-expanded_action), initial=0.)),
        action_scale=float(np.max(abs(direct_action), initial=0.)),
        energy_identity_error=abs(direct_energy-expanded_energy),
        coefficient_over_bulk_spacing=coefficient/layer.gram_spacing)
