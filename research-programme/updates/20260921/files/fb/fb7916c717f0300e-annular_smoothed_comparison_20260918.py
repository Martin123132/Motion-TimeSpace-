from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_flat_preassembled_flow_20260916 import band_product
from annular_characteristic_galerkin_defect_20260917 import nodal_reference
from annular_instantaneous_force_bridge_20260917 import canonical_momentum
from scipy.linalg import solve_banded
from scipy.optimize import brentq
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import splu
import numpy as np


def canonical_state(model, state):
    return np.concatenate([state[:model.count+1], canonical_momentum(model, state)])


def canonical_flow(model, state):
    count = model.count
    field, position = state[:count], state[count]
    velocity, speed = state[count+1:-2], state[-2]
    matrices = model.matrices(position)
    factor = model.lifted @ field

    def stiffness(suffix):
        return band_product(matrices['bulk'+suffix], field)+model.lifted_transpose @ (matrices['gram'+suffix]*factor)

    field_gradient = speed*band_product(matrices['transport'], velocity, True)
    field_gradient += speed**2*band_product(matrices['square'], field)-stiffness('')
    source_gradient = velocity @ band_product(matrices['mass_b'], velocity)/2
    source_gradient += speed*velocity @ band_product(matrices['transport_b'], field)
    source_gradient += speed**2*field @ band_product(matrices['square_b'], field)/2-field @ stiffness('_b')/2
    return np.concatenate([velocity, [speed], field_gradient, [source_gradient]])


def inverse_legendre(model, canonical):
    count = model.count
    field, position = canonical[:count], canonical[count]
    matrices = model.matrices(position)
    cross = band_product(matrices['transport'], field)
    solved = solve_banded((2, 2), matrices['mass'], np.column_stack([canonical[count+1:-1], cross]), check_finite=False)
    complement = field @ band_product(matrices['square'], field)-cross @ solved[:, 1]
    loading = canonical[-1]-cross @ solved[:, 0]
    if complement < -1e-11:
        raise ValueError('Negative kinetic complement.')
    mass = model.system.source_mass
    speed = brentq(lambda value: complement*value+mass*value/np.sqrt(1-value**2)-loading,
        -1+1e-14, 1-1e-14, xtol=5e-16, rtol=1e-15)
    velocity = solved[:, 0]-speed*solved[:, 1]
    return np.concatenate([field, [position], velocity, [speed, 0.]])


def velocity_tangent(model, state, canonical_tangent):
    count = model.count
    field, position = state[:count], state[count]
    velocity, speed = state[count+1:-2], state[-2]
    matrices = model.matrices(position)
    field_rate, position_rate = canonical_tangent[:count], canonical_tangent[count]
    mixed_field = speed*band_product(matrices['transport'], field_rate)
    mixed_field += position_rate*(band_product(matrices['mass_b'], velocity)
        +speed*band_product(matrices['transport_b'], field))
    mixed_source = velocity @ band_product(matrices['transport'], field_rate)
    mixed_source += 2*speed*field_rate @ band_product(matrices['square'], field)
    mixed_source += position_rate*(velocity @ band_product(matrices['transport_b'], field)
        +speed*field @ band_product(matrices['square_b'], field))
    remaining = canonical_tangent[count+1:]-np.append(mixed_field, mixed_source)
    cross = band_product(matrices['transport'], field)
    solved = solve_banded((2, 2), matrices['mass'], np.column_stack([remaining[:-1], cross]), check_finite=False)
    schur = model.system.source_mass/(1-speed**2)**1.5+field @ band_product(matrices['square'], field)-cross @ solved[:, 1]
    speed_rate = (remaining[-1]-cross @ solved[:, 0])/schur
    velocity_rate = solved[:, 0]-speed_rate*solved[:, 1]
    return np.concatenate([field_rate, [position_rate], velocity_rate, [speed_rate, 0.]])


def energy_norm(model, vector):
    count = model.count
    matrices = model.matrices(model.system.anchor)
    square = vector[:count] @ band_product(matrices['bulk'], vector[:count])+vector[count]**2+vector[-1]**2
    square += vector[count+1:-1] @ solve_banded((2, 2), matrices['mass'], vector[count+1:-1], check_finite=False)
    return float(np.sqrt(max(0., square)))


def sparse_bands(bands):
    count = bands.shape[1]
    rows, columns, values = [], [], []
    for offset in range(-2, 3):
        indices = np.arange(max(0, -offset), min(count, count-offset))
        rows.extend(indices+offset)
        columns.extend(indices)
        values.extend(bands[2+offset, indices])
    return coo_matrix((values, (rows, columns)), shape=(count, count)).tocsc()


def source_curvature_jump(system, reference, instant):
    position = reference.source.sol(instant)[0]
    left = reference.sample(instant, [position], source_side='left')['phi_rr'][0]
    right = reference.sample(instant, [position], source_side='right')['phi_rr'][0]
    return ((6.8-position)/(6.8-system.anchor))**2*right-((position-5.2)/(system.anchor-5.2))**2*left


def stationary_residual(model, reference, instant, kink_factor):
    position = reference.source.sol(instant)[0]
    coefficient = source_curvature_jump(model.system, reference, instant)
    return -model.lifted_transpose @ (model.matrices(position)['gram']*kink_factor*coefficient)


def quadrature_breaks(system, reference, lower, upper):
    lines = [(6.03, -1.), (6.03, 1.), (5.2, 1.), (6.8, -1.)]
    for radius in [5.48, 5.83, 6.23, 6.58]:
        lines.extend([(radius, -1.), (radius, 1.), (10.4-radius, 1.), (13.6-radius, -1.)])
    extras = []
    for side, times in reference.transition_times.items():
        extras.extend(instant for instant in times if lower < instant < upper)
        for emitted in times:
            position = reference.source.sol(emitted)[0]
            lines.append((position+emitted, -1.) if side == 'left' else (position-emitted, 1.))
    low_radii = system.mapping(system.radii, reference.source.sol(lower)[0])[0]
    high_radii = system.mapping(system.radii, reference.source.sol(upper)[0])[0]
    points = [lower, upper]+extras
    for intercept, speed in lines:
        selected = (low_radii-intercept-speed*lower)*(high_radii-intercept-speed*upper) < 0.
        for coordinate in system.radii[selected]:
            def difference(instant):
                return float(system.mapping(coordinate, reference.source.sol(instant)[0])[0]-intercept-speed*instant)
            points.append(brentq(difference, lower, upper, xtol=5e-15))
    ordered = sorted(points)
    return np.array([ordered[0]]+[value for previous, value in zip(ordered[:-1], ordered[1:]) if value-previous > 1e-13])


def averaged_path(model, reference, instant, epsilon, order):
    count = model.count
    horizon = reference.horizon
    compression = 1-2*epsilon/horizon
    if not 0 < epsilon < horizon/4 or not 0 <= instant <= horizon:
        raise ValueError('Inward time-average domain failed.')
    center = epsilon+compression*instant
    lower, upper = center-epsilon/2, center+epsilon/2
    edges = quadrature_breaks(model.system, reference, lower, upper)
    nodes, weights = np.polynomial.legendre.leggauss(order)
    instants = ((edges[:-1, None]+edges[1:, None])/2+np.diff(edges)[:, None]*nodes/2).ravel()
    measure = (np.diff(edges)[:, None]*weights/(2*epsilon)).ravel()
    kink = np.maximum(model.system.radii-model.system.anchor, 0.)**2/2
    kink_factor = model.lifted @ kink
    state_sum, derivative_sum, flow_sum = [np.zeros(2*count+2) for unused in range(3)]
    stationary_sum = np.zeros(count)
    for sample, weight in zip(instants, measure):
        state, derivative = nodal_reference(model.system, reference, sample)
        canonical = canonical_state(model, state)
        canonical_derivative = np.concatenate([derivative[:count+1],
            canonical_momentum(model, state.astype(complex)+1e-25j*derivative).imag/1e-25])
        state_sum += weight*canonical
        derivative_sum += weight*canonical_derivative
        flow_sum += weight*canonical_flow(model, state)
        stationary_sum += weight*stationary_residual(model, reference, sample, kink_factor)
    stationary_rate = compression/epsilon*(stationary_residual(model, reference, upper, kink_factor)
        -stationary_residual(model, reference, lower, kink_factor))
    return dict(canonical=state_sum, derivative=compression*derivative_sum, mean_derivative=derivative_sum,
        mean_flow=flow_sum, stationary=stationary_sum, stationary_rate=stationary_rate,
        compression=compression, lower=lower, upper=upper, quadrature_nodes=len(instants),
        total_weight=float(sum(measure)), kink_factor=kink_factor)


def comparison_corrector(model, canonical, canonical_derivative, stationary, stationary_rate):
    count = model.count
    state = inverse_legendre(model, canonical)
    state_rate = velocity_tangent(model, state, canonical_derivative)
    field, position, velocity, speed = state[:count], state[count], state[count+1:-2], state[-2]
    field_rate, position_rate = state_rate[:count], state_rate[count]
    velocity_rate, speed_rate = state_rate[count+1:-2], state_rate[-2]
    matrices = model.matrices(position)
    stiffness = sparse_bands(matrices['bulk']-speed**2*matrices['square'])
    stiffness += model.lifted_transpose @ model.lifted.multiply(matrices['gram'][:, None])
    solver = splu(stiffness.tocsc())
    correction_field = solver.solve(stationary)
    changing_bands = position_rate*(matrices['bulk_b']-speed**2*matrices['square_b'])-2*speed*speed_rate*matrices['square']
    changing_product = band_product(changing_bands, correction_field)
    changing_product += model.lifted_transpose @ (position_rate*matrices['gram_b']*(model.lifted @ correction_field))
    correction_field_rate = solver.solve(stationary_rate-changing_product)
    row = band_product(matrices['transport'], velocity, True)+2*speed*band_product(matrices['square'], field)
    row_rate = position_rate*band_product(matrices['transport_b'], velocity, True)
    row_rate += band_product(matrices['transport'], velocity_rate, True)+2*speed_rate*band_product(matrices['square'], field)
    row_rate += 2*speed*(position_rate*band_product(matrices['square_b'], field)+band_product(matrices['square'], field_rate))
    correction_momentum = speed*band_product(matrices['transport'], correction_field)
    correction_momentum_rate = speed_rate*band_product(matrices['transport'], correction_field)
    correction_momentum_rate += speed*(position_rate*band_product(matrices['transport_b'], correction_field)
        +band_product(matrices['transport'], correction_field_rate))
    correction = np.concatenate([correction_field, [0.], correction_momentum, [row @ correction_field]])
    correction_rate = np.concatenate([correction_field_rate, [0.], correction_momentum_rate,
        [row_rate @ correction_field+row @ correction_field_rate]])
    source_row = speed*band_product(matrices['transport_b'], velocity, True)+speed**2*band_product(matrices['square_b'], field)
    source_row -= band_product(matrices['bulk_b'], field)+model.lifted_transpose @ (matrices['gram_b']*(model.lifted @ field))
    linear_flow = np.concatenate([np.zeros(count+1), -stiffness @ correction_field, [source_row @ correction_field]])
    velocity_correction = np.concatenate([correction_field, np.zeros(count+3)])
    independent = canonical_flow(model, state.astype(complex)+1e-25j*velocity_correction).imag/1e-25
    return dict(correction=correction, correction_rate=correction_rate, linear_flow=linear_flow,
        linear_identity_error=energy_norm(model, independent-linear_flow),
        elliptic_relative_residual=float(np.linalg.norm(stiffness @ correction_field-stationary)
            /max(1e-30, np.linalg.norm(stationary))), state=state, state_rate=state_rate)


def comparison_diagnostics(model, reference, instant, epsilon, order):
    data = averaged_path(model, reference, instant, epsilon, order)
    corrected = comparison_corrector(model, data['canonical'], data['derivative'], data['stationary'], data['stationary_rate'])
    base_flow = canonical_flow(model, corrected['state'])
    count = model.count
    singular = np.concatenate([np.zeros(count+1), data['stationary'], [0.]])
    averaged_residual = data['mean_flow']-data['mean_derivative']
    commutator = base_flow-data['mean_flow']
    compression_defect = (1-data['compression'])*data['mean_derivative']
    corrected_canonical = data['canonical']+corrected['correction']
    corrected_flow = canonical_flow(model, inverse_legendre(model, corrected_canonical))
    nonlinear_remainder = corrected_flow-base_flow-corrected['linear_flow']
    corrected_residual = corrected_flow-data['derivative']-corrected['correction_rate']
    decomposition = averaged_residual-singular+commutator+compression_defect
    decomposition += singular+corrected['linear_flow']-corrected['correction_rate']+nonlinear_remainder
    original, unused = nodal_reference(model.system, reference, instant)
    spacing = model.system.gram_spacing
    expected_scale = spacing/np.sqrt(epsilon)+epsilon**2/spacing+epsilon+spacing
    row = dict(time=instant, h=spacing, epsilon=epsilon, quadrature_order=order,
        quadrature_nodes=data['quadrature_nodes'], mean_residual_norm=energy_norm(model, averaged_residual),
        regular_residual_norm=energy_norm(model, averaged_residual-singular),
        stationary_residual_norm=energy_norm(model, singular), commutator_norm=energy_norm(model, commutator),
        correction_norm=energy_norm(model, corrected['correction']), correction_rate_norm=energy_norm(model, corrected['correction_rate']),
        source_remainder_norm=energy_norm(model, singular+corrected['linear_flow']),
        nonlinear_corrector_remainder_norm=energy_norm(model, nonlinear_remainder),
        corrected_residual_norm=energy_norm(model, corrected_residual), corrected_residual_scale=expected_scale,
        corrected_residual_ratio=energy_norm(model, corrected_residual)/expected_scale,
        comparison_displacement=energy_norm(model, corrected_canonical-canonical_state(model, original)),
        linear_identity_error=corrected['linear_identity_error'], decomposition_error=energy_norm(model, corrected_residual-decomposition),
        elliptic_relative_residual=corrected['elliptic_relative_residual'], total_weight=data['total_weight'],
        window_lower=data['lower'], window_upper=data['upper'])
    arrays = dict(canonical=data['canonical'], derivative=data['derivative'], correction=corrected['correction'],
        correction_rate=corrected['correction_rate'], averaged_residual=averaged_residual,
        regular_residual=averaged_residual-singular, corrected_residual=corrected_residual, commutator=commutator)
    return row, arrays
