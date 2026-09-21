from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_flat_preassembled_flow_20260916 import band_product
from derive_annular_characteristic_source_20260917 import rhs
from scipy.linalg import solve_banded
import numpy as np


def pullback_jets(system, reference, instant, coordinates):
    source = reference.source.sol(instant)
    position, velocity = source[:2]
    acceleration = rhs(instant, source)[1]
    radius, jacobian, displacement = system.mapping(coordinates, position)
    slope = np.where(coordinates < system.anchor, 1/(system.anchor-5.2), -1/(6.8-system.anchor))
    field = reference.sample(instant, radius)
    temporal = field['phi_t']+displacement*velocity*field['phi_r']
    spatial = jacobian*field['phi_r']
    mixed = jacobian*field['phi_tr']+slope*velocity*field['phi_r']+displacement*velocity*jacobian*field['phi_rr']
    second = field['phi_tt']+2*displacement*velocity*field['phi_tr']+(displacement*velocity)**2*field['phi_rr']
    second += displacement*acceleration*field['phi_r']
    return dict(value=field['phi'], temporal=temporal, spatial=spatial, mixed=mixed, second=second,
        radius=radius, jacobian=jacobian, displacement=displacement, slope=slope,
        position=position, velocity=velocity, acceleration=acceleration, clock=source[2], physical=field)


def nodal_reference(system, reference, instant):
    data = pullback_jets(system, reference, instant, system.radii)
    state = np.concatenate([data['value'], [data['position']], data['temporal'], [data['velocity'], data['clock']]])
    derivative = np.concatenate([data['temporal'], [data['velocity']], data['second'],
        [data['acceleration'], np.sqrt(1-data['velocity']**2)]])
    return state, derivative


def canonical_defect(model, state, derivative):
    count = model.count
    matrices = model.matrices(state[count])
    field = state[:count]
    cross = band_product(matrices['transport'], field)
    source_inertia = state[:count] @ band_product(matrices['square'], field)+model.system.source_mass/(1-state[-2]**2)**1.5
    discrepancy = model.evaluate(state)['flow']-derivative
    acceleration = discrepancy[count+1:-2]
    source_acceleration = discrepancy[-2]
    covector = np.append(band_product(matrices['mass'], acceleration)+cross*source_acceleration,
        cross @ acceleration+source_inertia*source_acceleration)
    factor = model.lifted @ field
    gram = np.append(-model.lifted_transpose @ (matrices['gram']*factor), -factor @ (matrices['gram_b']*factor)/2)
    return covector, gram, matrices, discrepancy


def mass_dual_norm(covector, matrices):
    field = covector[:-1]
    square = field @ solve_banded((2, 2), matrices['mass'], field, check_finite=False)+covector[-1]**2
    return float(np.sqrt(max(0., square)))


def weak_defects(system, reference, instant, state, derivative, order=10):
    count = system.count
    position, velocity, acceleration = state[count], state[-2], derivative[-2]
    physical_breaks = reference.breakpoints(instant)
    pulled_breaks = np.where(physical_breaks < position,
        5.2+(physical_breaks-5.2)*(system.anchor-5.2)/(position-5.2),
        6.8-(6.8-physical_breaks)*(6.8-system.anchor)/(6.8-position))
    edges = np.unique(np.concatenate([system.edges, pulled_breaks]))
    nodes, weights = np.polynomial.legendre.leggauss(order)
    coordinate = ((edges[:-1, None]+edges[1:, None])/2+np.diff(edges)[:, None]*nodes/2).ravel()
    measure = (np.diff(edges)[:, None]*weights/2).ravel()
    exact = pullback_jets(system, reference, instant, coordinate)
    indices, shape, radial = system.features_quadratic(coordinate)
    nodal_value = state[:count]
    nodal_rate = state[count+1:-2]
    nodal_second = derivative[count+1:-2]
    interpolated = dict(value=np.sum(shape*nodal_value[indices], axis=1),
        temporal=np.sum(shape*nodal_rate[indices], axis=1),
        spatial=np.sum(radial*nodal_value[indices], axis=1),
        mixed=np.sum(radial*nodal_rate[indices], axis=1),
        second=np.sum(shape*nodal_second[indices], axis=1))
    radius, jacobian, displacement, slope = [exact[name] for name in ['radius', 'jacobian', 'displacement', 'slope']]
    transport = velocity*displacement/jacobian
    transport_t = acceleration*displacement/jacobian-velocity**2*displacement*slope/jacobian**2
    transport_b = -velocity*displacement*slope/jacobian**2
    density = jacobian*radius**2
    density_b = slope*radius**2+2*jacobian*radius*displacement
    density_t = velocity*density_b
    stiffness = radius**2/jacobian
    stiffness_b = 2*radius*displacement/jacobian-radius**2*slope/jacobian**2
    loading = radius**2*displacement
    loading_t = 2*radius*displacement**2*velocity
    output = {}
    for label, data in [('exact', exact), ('interpolated', interpolated)]:
        gradient = data['spatial']
        temporal = data['temporal']-transport*gradient
        temporal_t = data['second']-transport_t*gradient-transport*data['mixed']
        momentum_t = density_t*temporal+density*temporal_t
        flux = stiffness*gradient+loading*velocity*temporal
        values = -measure[:, None]*(shape*momentum_t[:, None]+radial*flux[:, None])
        field_residual = system.assemble_quadratic(indices, values)
        source_density = density_b*temporal**2/2-density*transport_b*temporal*gradient-stiffness_b*gradient**2/2
        source_density += loading_t*temporal*gradient+loading*temporal_t*gradient+loading*temporal*data['mixed']
        source_residual = measure @ source_density-system.source_mass*acceleration/(1-velocity**2)**1.5
        output[label] = np.append(field_residual, source_residual)
    errors = {name: interpolated[name]-exact[name] for name in ['value', 'temporal', 'spatial', 'mixed', 'second']}
    output['error_norms'] = {name: float(np.sqrt(measure @ values**2)) for name, values in errors.items()}
    output['error_L1'] = {name: float(measure @ abs(values)) for name, values in errors.items()}
    error_transport = errors['temporal']-transport*errors['spatial']
    error_transport_t = errors['second']-transport_t*errors['spatial']-transport*errors['mixed']
    forcing = density_t*error_transport+density*error_transport_t
    flux_error = stiffness*errors['spatial']+loading*velocity*error_transport
    independent_field = system.assemble_quadratic(indices,
        -measure[:, None]*(shape*forcing[:, None]+radial*flux_error[:, None]))
    output['direct_error_field'] = independent_field
    output['reference_material_derivative_identity'] = float(max(abs(
        exact['second']-transport_t*exact['spatial']-transport*exact['mixed']
        -exact['physical']['phi_tt']-displacement*velocity*exact['physical']['phi_tr'])))
    output['quadrature_points'] = len(measure)
    return output
