import numpy as np
from scipy.linalg import solve, svd

from annular_canonical_rate_completion_20260911 import normalized_transform
from annular_cubic_lapse_reference_gravity_20260912 import evaluate_cubic_initial


def refresh(model):
    model.first = evaluate_cubic_initial(model.frames['mass'], model.frames['scalar'], model.data, model.basis, model.weights, model.links, model.gram, model.context.system.outer_clock, surface=model.surface, link_surface=model.link_surface)
    for surface in model.rates:
        mass, scalar = model.frames['mass'][surface], model.frames['scalar'][surface]
        model.rates[surface] = {'mu': mass['q'] @ model.first['mass_rate_coeff'], 'mu_r': mass['qr'] @ model.first['mass_rate_coeff'], 'P': mass['p'] @ model.first['P_rate_coeff'], 'pi': scalar['p'] @ model.first['pi_rate_coeff'], 'chi': scalar['q'] @ model.first['q_coeff'], 'w': scalar['qr'] @ model.first['q_coeff']}
    model.prepare_links()


def build_pair(model, include_drift=True):
    old = model.frames['scalar']
    kinetic = {surface: values['R']**2 / (values['N'] * np.sqrt(values['F'])) for surface, values in model.data.items()}
    weights = model.weights * kinetic['quad']
    transformation = normalized_transform(old['quad']['q'], weights)
    coordinate = {surface: {'q': maps['q'] @ transformation, 'qr': maps['qr'] @ transformation} for surface, maps in old.items()}
    family = {}
    for surface, values in model.data.items():
        radius, geometry, lapse = values['R'], values['F'], values['N']
        root_f = np.sqrt(geometry)
        rate, rate_r = model.rates[surface]['mu'], model.rates[surface]['mu_r']
        velocity = lapse * root_f * values['pi'] / radius**2
        velocity_r = (values['N_r'] * root_f * values['pi'] + lapse * values['F_r'] * values['pi'] / (2 * root_f) + lapse * root_f * values['pi_r']) / radius**2 - 2 * velocity / radius
        drift = -lapse * rate * values['pi'] / (radius**3 * root_f)
        drift_r = -(values['N_r'] * rate * values['pi'] + lapse * rate_r * values['pi'] + lapse * rate * values['pi_r']) / (radius**3 * root_f) - drift * (3 / radius + values['F_r'] / (2 * geometry))
        factor = root_f * values['pi'] / radius**2
        factor_r = (root_f * values['pi_r'] + values['F_r'] * values['pi'] / (2 * root_f)) / radius**2 - 2 * factor / radius
        family[surface] = {'q': np.column_stack([values['chi'], velocity]), 'qr': np.column_stack([values['w'], velocity_r])}
        if include_drift:
            family[surface]['q'] = np.column_stack([family[surface]['q'], drift, values['eta'] * factor[:, None]])
            family[surface]['qr'] = np.column_stack([family[surface]['qr'], drift_r, values['eta_r'] * factor[:, None] + values['eta'] * factor_r[:, None]])
    scale = np.maximum(np.sqrt(weights @ family['quad']['q']**2), 1e-30)
    projection = coordinate['quad']['q'].T @ (weights[:, None] * (family['quad']['q'] / scale))
    residual = family['quad']['q'] / scale - coordinate['quad']['q'] @ projection
    unused_left, singular, right = svd(np.sqrt(weights)[:, None] * residual, full_matrices=False)
    selected = singular > 1e-11
    extra_transform = right[selected].T / singular[selected]
    for surface, maps in coordinate.items():
        extra = (family[surface]['q'] / scale - maps['q'] @ projection) @ extra_transform
        extra_r = (family[surface]['qr'] / scale - maps['qr'] @ projection) @ extra_transform
        maps['q'] = np.column_stack([maps['q'], extra])
        maps['qr'] = np.column_stack([maps['qr'], extra_r])
    final_transform = normalized_transform(coordinate['quad']['q'], weights)
    frames = {surface: {'q': maps['q'] @ final_transform, 'qr': maps['qr'] @ final_transform, 'p': kinetic[surface][:, None] * (maps['q'] @ final_transform)} for surface, maps in coordinate.items()}
    pairing = frames['quad']['p'].T @ (model.weights[:, None] * frames['quad']['q'])
    coefficients = solve(pairing, frames['quad']['p'].T @ (model.weights[:, None] * family['quad']['q']))
    errors = {surface + '_' + kind: float(abs(frames[surface][kind] @ coefficients - family[surface][kind]).max()) for surface in frames for kind in ['q', 'qr']}
    retained_coeff = solve(pairing, frames['quad']['p'].T @ (model.weights[:, None] * old['quad']['q']))
    retained = {surface + '_' + kind: float(abs(frames[surface][kind] @ retained_coeff - old[surface][kind]).max()) / max(1., float(abs(old[surface][kind]).max())) for surface in frames for kind in ['q', 'qr']}
    kinetic_errors = {}
    for surface in frames:
        kinetic_image = frames[surface]['p'] / kinetic[surface][:, None]
        kinetic_errors[surface] = float(abs(kinetic_image - frames[surface]['q']).max())
    return frames, {'new_finite_scalar_momentum_space': True, 'old_momentum_space_not_claimed_retained': True, 'old_configuration_dimension': old['quad']['q'].shape[1], 'new_scalar_dimension': pairing.shape[0], 'continuous_family_dimension': family['quad']['q'].shape[1], 'new_family_directions': int(selected.sum()), 'family_singular_values': singular.tolist(), 'family_reconstruction_errors': errors, 'old_configuration_span_errors': retained, 'pointwise_kinetic_image_errors_all_surfaces': kinetic_errors, 'pair_identity_error': float(abs(pairing - np.eye(pairing.shape[0])).max()), 'pair_condition': float(np.linalg.cond(pairing)), 'coefficient_K0_is_frozen_not_a_moving_frame': True, 'broken_shift_drift_not_silently_added_to_continuous_space': True}


def kinetic_acceleration_control(model, result):
    values, rates = model.data[model.surface], model.rates[model.surface]
    maps = model.frames['scalar'][model.surface]
    radius, root_f = values['R'], np.sqrt(values['F'])
    lapse_first = values['eta'] @ result['lapse_rate_coefficients']
    kinetic_velocity = values['N'] * root_f / radius**2
    shift_drift = .1 * values['N'] * values['F']**1.5 * rates['P'] * values['w']
    continuous_drift = (lapse_first * root_f / radius**2 - values['N'] * rates['mu'] / (radius**3 * root_f)) * values['pi']
    physical = kinetic_velocity * rates['pi'] + continuous_drift + shift_drift
    projected = maps['q'] @ solve(model.first['scalar_pair'], maps['p'].T @ (model.weights * physical))
    actual = maps['q'] @ result['second']['chi']
    projected_kinetic = maps['q'] @ solve(model.first['scalar_pair'], maps['p'].T @ (model.weights * kinetic_velocity * rates['pi']))
    projected_continuous = maps['q'] @ solve(model.first['scalar_pair'], maps['p'].T @ (model.weights * continuous_drift))
    projected_shift = maps['q'] @ solve(model.first['scalar_pair'], maps['p'].T @ (model.weights * shift_drift))
    return {'scalar_acceleration_projector_identity_error': float(abs(projected - actual).max()), 'kinetic_rate_defect_max': float(abs(projected_kinetic - kinetic_velocity * rates['pi']).max()), 'continuous_drift_defect_max': float(abs(projected_continuous - continuous_drift).max()), 'shift_drift_defect_max': float(abs(projected_shift - shift_drift).max()), 'full_scalar_acceleration_defect_max': float(abs(actual - physical).max()), 'full_scalar_acceleration_defect_L2': float(np.sqrt(model.weights @ (actual - physical)**2))}
