from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_radial_constraint_20260920 import CandidateRadialSolve, radial_rhs
from annular_P2_indexed_live_geometry_20260919 import IndexedP2Material, IndexedP2Density, indexed_label_values
from annular_common_weighted_moments_20260920 import apply_rational_rows
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from copy import copy
from decimal import localcontext
from fractions import Fraction
from time import perf_counter
from scipy.sparse import coo_matrix, csr_matrix
import numpy as np


def common_material(owner, saved, packet):
    model = copy(owner.model)
    mesh = packet['overlay']
    model.edges = np.array([float(Fraction(value)) for value in mesh['edges']])
    model.radii = np.array([float(Fraction(value)) for value in mesh['nodes']])
    model.element_indices = np.array(mesh['elements'])
    model.count = mesh['count']
    model.sampling = csr_matrix((0, model.count))
    adapted = copy(owner)
    adapted.model, adapted.count = model, model.count
    with localcontext() as context:
        context.prec = 64
        fields = np.array(apply_rational_rows(packet['embeddings'][0],
            decimal_array(saved['coordinates'][:, :-1].T)).T, dtype=float)
        velocities = np.array(apply_rational_rows(packet['embeddings'][0],
            decimal_array(saved['fixed_rates'][:, :-1].T)).T, dtype=float)
    coordinates = np.column_stack([fields, saved['coordinates'][:, -1]])
    rates = np.column_stack([velocities, saved['fixed_rates'][:, -1]])
    return adapted, coordinates, rates


def probe_directions(owner, coordinates):
    radius = owner.model.radii
    fraction = (radius-radius[0])/(radius[-1]-radius[0])
    offset = (radius-owner.model.anchor)/(radius[-1]-radius[0])
    labels = owner.labels
    result = np.zeros((4, *coordinates.shape))
    result[0, :, :-1] = .1*(1+.2*labels[:, None])*np.sin(np.pi*fraction)*offset
    result[1, :, -1] = 1+.1*labels
    result[2, :, :-1] = .1*(1-.2*labels[:, None])*np.sin(np.pi*fraction)*(-1.)**np.arange(len(radius))
    result[3, :, :-1] = .05*(1+labels[:, None]+labels[:, None]**2)*np.sin(3*np.pi*fraction)*offset
    result[3, :, -1] = .2*(labels**2-1/12)
    return result


def density_chunks(owner, coordinates, radius, label_order, deadline):
    adapted = copy(owner)
    adapted.label_order = label_order
    material = IndexedP2Material(adapted, coordinates)
    for start in range(0, len(radius), 128):
        if perf_counter() > deadline:
            raise RuntimeError('Safe wall-clock boundary; completed evidence retained.')
        section = slice(start, start+128)
        yield section, IndexedP2Density(material, radius[section])


def temporal_values(density, rates):
    sample = indexed_label_values(density.interpolation, rates[:, :-1], density.scalar_indices)
    return np.sum(density.shape*sample, axis=1)+density.motion*(density.interpolation @ rates[:, -1])


def density_response(owner, coordinates, rates, directions, radius, label_order, deadline):
    count = len(radius)
    result = {name:np.zeros(count) for name in ['temporal_square', 'gradient_square', 'source_density', 'velocity']}
    result.update(delta_temporal=np.zeros((len(directions), count)),
        quadratic_temporal=np.zeros((len(directions), count)), delta_velocity=np.zeros((len(directions), count)))
    for section, density in density_chunks(owner, coordinates, radius, label_order, deadline):
        temporal = temporal_values(density, rates)
        result['temporal_square'][section] = np.bincount(density.indices,
            weights=density.label_weights*temporal**2, minlength=len(density.radius))
        result['gradient_square'][section] = density.gradient_square
        result['source_density'][section] = density.source_density
        selected = density.source_selected
        result['velocity'][section][selected] = density.source_interpolation @ rates[:, -1]
        for index, direction in enumerate(directions):
            variation = temporal_values(density, direction)
            result['delta_temporal'][index, section] = np.bincount(density.indices,
                weights=2*density.label_weights*temporal*variation, minlength=len(density.radius))
            result['quadratic_temporal'][index, section] = np.bincount(density.indices,
                weights=density.label_weights*variation**2, minlength=len(density.radius))
            result['delta_velocity'][index, section][selected] = density.source_interpolation @ direction[:, -1]
    return result


def restored_solver(owner, density, degree):
    solver = CandidateRadialSolve.__new__(CandidateRadialSolve)
    solver.owner = owner
    solver.rule = ChebyshevRule(degree)
    solver.edges, solver.nodes = density['edges'], density['nodes']
    solver.lengths, solver.centers = np.diff(solver.edges), (solver.edges[1:]+solver.edges[:-1])/2
    solver.fields = {name:density[name].copy() for name in ['temporal_square', 'gradient_square', 'source_density', 'velocity']}
    solver.fields['gram'] = {name[5:]:density[name] for name in density if name.startswith('gram_')}
    return solver


def velocity_forcing(solver, state, delta_temporal, delta_velocity):
    radius = solver.nodes.ravel()
    mass, log_lapse = state.reshape(2, -1)
    metric, lapse = 1-2*mass/radius, np.exp(log_lapse)
    velocity = solver.fields['velocity']
    clock = np.sqrt(lapse**2-velocity**2/metric)
    density = solver.fields['source_density']
    coupling, source_mass = solver.owner.coupling, solver.owner.source_mass
    dust_mass = coupling*source_mass*density*np.sqrt(metric)*lapse/clock
    mass_forcing = coupling*radius**2*delta_temporal/(2*lapse**2)
    mass_forcing += dust_mass*velocity*delta_velocity/(metric*clock**2)
    lapse_forcing = coupling*radius*delta_temporal/(2*lapse**2*metric)
    lapse_forcing += coupling*source_mass*density/(radius*lapse*metric**1.5)*(
        2*velocity/clock+velocity**3/(metric*clock**3))*delta_velocity
    return np.array([mass_forcing, lapse_forcing])


def solve_tangent(solver, state, extension, forcing):
    unused, local = solver.rhs(state, extension, True)
    tangent = np.zeros_like(state)
    history = []
    outer_factor = solver.edges[-1]*(1-2*state[0, -1, -1]/solver.edges[-1])
    scale = max(np.max(abs(forcing)), 1e-30)
    for iteration in range(80):
        rhs = np.einsum('abn,bn->an', local, tangent.reshape(2, -1))+forcing
        mass = solver.integrated(rhs[0])
        primitive = solver.integrated(rhs[1])
        lapse = -mass[-1, -1]/outer_factor+primitive-primitive[-1, -1]
        updated = np.stack([mass, lapse])
        error = np.max(abs(updated-tangent))
        history.append(float(error))
        tangent = updated
        if error < 2e-14*scale:
            break
    else:
        raise RuntimeError('Metric velocity tangent iteration did not converge.')
    right_mass, right_lapse = [solver.integrated(values) for values in forcing]
    residual = solver.jacobian_product(state, tangent, extension)-np.stack([
        right_mass, right_lapse-right_lapse[-1, -1]])
    return tangent, float(np.max(abs(residual))), history


def solve_changed_velocity(solver, state, extension, response, direction, step, minimum_iterations=14):
    altered = copy(solver)
    altered.fields = dict(solver.fields)
    altered.fields['temporal_square'] = solver.fields['temporal_square']+step*response['delta_temporal'][direction]
    altered.fields['temporal_square'] += step**2*response['quadratic_temporal'][direction]
    altered.fields['velocity'] = solver.fields['velocity']+step*response['delta_velocity'][direction]
    current = state.astype(np.result_type(step, state))
    for iteration in range(80):
        rhs = altered.rhs(current, extension)
        mass = solver.owner.central_mass+solver.integrated(rhs[0])
        primitive = solver.integrated(rhs[1])
        lapse = .5*np.log(1-2*mass[-1, -1]/solver.edges[-1])+primitive-primitive[-1, -1]
        updated = np.stack([mass, lapse])
        error = float(np.max(abs(updated-current)))
        current = updated
        if iteration+1 >= minimum_iterations and error < 4e-14:
            break
    else:
        raise RuntimeError('Independent changed-velocity nonlinear radial solve failed.')
    return altered, current


def radial_weights(solver):
    return (solver.lengths[:, None]*solver.rule.integration[-1][None, :]/2).ravel()


def total_action(solver, state, extension):
    radius = solver.nodes.ravel()
    mass, log_lapse = state.reshape(2, -1)
    metric, lapse = 1-2*mass/radius, np.exp(log_lapse)
    root = np.sqrt(metric)
    clock = np.sqrt(lapse**2-solver.fields['velocity']**2/metric)
    rhs = solver.rhs(state, extension)
    wave = radius**2*solver.fields['temporal_square']/(2*lapse*root)
    wave -= lapse*root*radius**2*(solver.fields['gradient_square']/2+solver.fields['gram'][extension])
    dust = -solver.owner.source_mass*solver.fields['source_density']*clock
    gravity = lapse*rhs[0]/(solver.owner.coupling*root)
    return radial_weights(solver) @ (gravity+wave+dust)-mass[-1]/solver.owner.coupling


def velocity_design(density, label_count, component_count):
    samples = len(density.indices)
    scalar_columns = density.scalar_indices
    columns = np.concatenate([scalar_columns, np.full((samples, 1), component_count-1)], axis=1)
    shapes = np.column_stack([density.shape, density.motion])
    columns = np.arange(label_count)[:, None, None]*component_count+columns[None, :, :]
    rows = np.broadcast_to(np.arange(samples)[None, :, None], columns.shape)
    values = density.interpolation.T[:, :, None]*shapes[None, :, :]
    return coo_matrix((values.ravel(), (rows.ravel(), columns.ravel())),
        shape=(samples, label_count*component_count)).tocsr()


def momentum_response(owner, coordinates, rates, directions, solver, state, tangents, complex_states, deadline):
    count = len(directions)
    shape = coordinates.shape
    radius = solver.nodes.ravel()
    measure = radial_weights(solver)
    metric, lapse = 1-2*state[0].ravel()/radius, np.exp(state[1].ravel())
    mass_tangent = tangents[:, 0].reshape(count, -1)
    log_tangent = tangents[:, 1].reshape(count, -1)
    coefficient = radius**2/(lapse*np.sqrt(metric))
    ratio = mass_tangent/(radius*metric)-log_tangent
    complex_coefficient = np.array([radius**2/(np.exp(values[1].ravel())*
        np.sqrt(1-2*values[0].ravel()/radius)) for values in complex_states])
    result = np.zeros((shape[0]*shape[1], 1+3*count))
    step = 1e-25
    for section, density in density_chunks(owner, coordinates, radius, solver.label_order, deadline):
        temporal = temporal_values(density, rates)
        variations = np.array([temporal_values(density, direction) for direction in directions])
        point = density.indices
        base_weight = density.label_weights*measure[section][point]
        kinetic_weight = coefficient[section][point]
        local_ratio = ratio[:, section][:, point]
        channels = np.column_stack([kinetic_weight*temporal,
            (kinetic_weight*variations).T,
            (kinetic_weight*(variations+temporal*local_ratio)).T,
            ((complex_coefficient[:, section][:, point]*(temporal+1j*step*variations)).imag/step).T])
        design = velocity_design(density, *shape)
        result += design.T @ (base_weight[:, None]*channels)
        selected = density.source_selected
        if np.any(selected):
            interpolation = density.source_interpolation
            velocity = interpolation @ rates[:, -1]
            changes = np.array([interpolation @ direction[:, -1] for direction in directions])
            local_metric, local_lapse = metric[section][selected], lapse[section][selected]
            clock = np.sqrt(local_lapse**2-velocity**2/local_metric)
            momentum = owner.source_mass*velocity/(local_metric*clock)
            direct = owner.source_mass*local_lapse**2/(local_metric*clock**3)*changes
            mass_partial = momentum*(2/(density.radius[selected]*local_metric)
                +velocity**2/(density.radius[selected]*local_metric**2*clock**2))
            lapse_partial = -momentum*local_lapse**2/clock**2
            total = direct+mass_partial*mass_tangent[:, section][:, selected]+lapse_partial*log_tangent[:, section][:, selected]
            checked = []
            for index, values in enumerate(complex_states):
                changed_metric = 1-2*values[0].ravel()[section][selected]/density.radius[selected]
                changed_lapse = np.exp(values[1].ravel()[section][selected])
                changed_velocity = velocity+1j*step*changes[index]
                checked.append((owner.source_mass*changed_velocity/(changed_metric*
                    np.sqrt(changed_lapse**2-changed_velocity**2/changed_metric))).imag/step)
            channels = np.column_stack([momentum, direct.T, total.T, np.array(checked).T])
            weights = measure[section][selected]*density.source_density[selected]
            source_indices = np.arange(shape[0])*shape[1]+shape[1]-1
            result[source_indices] += interpolation.T @ (weights[:, None]*channels)
    return dict(momentum=result[:, 0].reshape(shape),
        fixed_derivatives=result[:, 1:1+count].T.reshape(count, *shape),
        live_derivatives=result[:, 1+count:1+2*count].T.reshape(count, *shape),
        complex_derivatives=result[:, 1+2*count:].T.reshape(count, *shape))


def center_momentum(owner, coordinates, rates, solver, solution, order=28):
    center = int(np.argmin(abs(owner.labels)))
    scalar, velocity = coordinates[center, :-1], rates[center, -1]
    source = coordinates[center, -1]
    points, weights = np.polynomial.legendre.leggauss(order)
    edges = owner.model.edges
    reference = ((edges[1:, None]+edges[:-1, None])/2+np.diff(edges)[:, None]*points/2).ravel()
    measure = (np.diff(edges)[:, None]*weights/2).ravel()
    radius, spatial, displacement = owner.model.mapping(reference, source)
    indices, shapes, derivatives = owner.model.features_quadratic(reference)
    motion = -displacement*np.sum(derivatives*scalar[indices], axis=1)/spatial
    temporal = np.sum(shapes*rates[center, :-1][indices], axis=1)+velocity*motion
    values, unused = solver.values(solution, radius)
    coefficient = measure*spatial*radius**2/(np.exp(values[1])*np.sqrt(1-2*values[0]/radius))
    momentum = owner.model.assemble_quadratic(indices, shapes*(coefficient*temporal)[:, None])
    values, unused = solver.values(solution, np.array([source]))
    metric, lapse = 1-2*values[0, 0]/source, np.exp(values[1, 0])
    source_momentum = np.dot(coefficient, temporal*motion)+owner.source_mass*velocity/(
        metric*np.sqrt(lapse**2-velocity**2/metric))
    return np.r_[momentum, source_momentum]


def transpose_embedding(rows, values, count):
    result = np.zeros(count)
    for row, entries in enumerate(rows):
        for column, weight in entries.items():
            result[int(column)] += float(Fraction(weight))*values[row]
    return result

