from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_energy_current_20260921 import richardson, gram_cut_current
from annular_candidate_Ward_source_20260921 import material_quadrature
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from copy import copy
from decimal import localcontext
from math import fsum
from time import perf_counter
from scipy.sparse import coo_matrix
import numpy as np


class MetricTangent:
    def __init__(self, probes, steps):
        self.probes, self.steps, self.prefixes = probes, steps, {}
        for key, action in probes.items():
            increments = np.polynomial.chebyshev.chebval(1., action.solution['primitives'][0].T)
            self.prefixes[key] = np.array([fsum(increments[:index]) for index in range(len(increments))])

    def at(self, radius):
        pairs = []
        for index in range(3):
            pair = []
            for sign in [-1, 1]:
                action = self.probes[index, sign]
                solver, solution = action.solver, action.solution
                selected = np.clip(np.searchsorted(solver.edges, radius, side='right')-1, 0, len(solver.edges)-2)
                mapped = 2*(radius-solver.centers[selected])/solver.lengths[selected]
                mass = self.prefixes[index, sign][selected]+np.polynomial.chebyshev.chebval(
                    mapped, solution['primitives'][0, selected].T, tensor=False)
                values, unused = solver.values(solution, radius)
                pair.append(np.array([mass, values[1]]))
            pairs.append(pair)
        unused, tangent = richardson(np.asarray(pairs), self.steps)
        return tangent[:, 1], -2*tangent[:, 0]/radius


def samples(action, label, order, targets=None):
    cardinal = np.asarray(action.cardinal(label)).ravel()
    source, velocity = cardinal @ action.source, cardinal @ action.velocity
    integration = action
    if targets is not None:
        integration = copy(action)
        integration.solver = copy(action.solver)
        integration.solver.edges = np.unique(np.r_[action.solver.edges, targets])
    quadrature = integration.quadrature(label, source, order)
    cells, local = quadrature['cells'], quadrature['local']
    geometry = action.geometry(quadrature['reference'], source, label)
    coefficients = np.einsum('cpl,l->cp', action.gradient, cardinal)[cells]
    gradient = coefficients[:, 0]+coefficients[:, 1]*local
    coefficients = np.einsum('cpl,l->cp', action.rate_polynomial, cardinal)[cells]
    rate = coefficients[:, 0]+local*(coefficients[:, 1]+local*coefficients[:, 2])
    widths = np.diff(np.array([float(value) for value in action.edges]))[cells]
    rate_gradient = (coefficients[:, 1]+2*local*coefficients[:, 2])/widths
    shape = np.column_stack([(1-local)*(1-2*local), 4*local*(1-local), local*(2*local-1)])
    shape *= np.array(action.mesh['elements'])[cells] >= 0
    motion = -geometry['displacement']*gradient/geometry['jacobian']
    motion_rate = -geometry['displacement']*rate_gradient/geometry['jacobian']
    motion_rate -= motion*geometry['jacobian_source']*velocity/geometry['jacobian']
    return dict(cardinal=cardinal, source=source, velocity=velocity, quadrature=quadrature, geometry=geometry,
        gradient=gradient, rate=rate, rate_gradient=rate_gradient, shape=shape, motion=motion,
        motion_rate=motion_rate, temporal=rate+velocity*motion)


def dust_data(action, source, velocity, tangent):
    values, derivatives = action.solver.values(action.solution, np.array([source]))
    lapse, metric = np.exp(values[1, 0]), 1-2*values[0, 0]/source
    metric_radial = -2*derivatives[0, 0]/source+2*values[0, 0]/source**2
    clock = np.sqrt(lapse**2-velocity**2/metric)
    nu_time, metric_time = tangent.at(np.array([source]))
    nu_time, metric_time = nu_time[:, 0], metric_time[:, 0]
    nu_total = nu_time+velocity*derivatives[1, 0]
    metric_total = metric_time+velocity*metric_radial
    clock_total = (lapse**2*nu_total+velocity**2*metric_total/(2*metric**2))/clock
    mass = action.owner.source_mass
    momentum, energy = mass*velocity/(metric*clock), mass*lapse**2/clock
    inertia = mass*lapse**2/(metric*clock**3)
    return dict(momentum=momentum, energy=energy, inertia=inertia,
        momentum_rate=momentum*(-metric_total/metric-clock_total/clock),
        energy_rate=energy*(2*nu_total-clock_total/clock),
        exchange=mass*(lapse**2*nu_time+velocity**2*metric_time/(2*metric**2))/clock,
        speed=abs(velocity)/(lapse*np.sqrt(metric)))


def wave_data(row, tangent):
    geometry = row['geometry']
    nu_time, metric_time = tangent.at(geometry['radius'])
    metric_log = nu_time+metric_time/(2*geometry['metric'])
    kinetic, spatial = geometry['kinetic'], geometry['gradient']
    kinetic_rate = geometry['kinetic_source']*row['velocity']-kinetic*metric_log
    spatial_rate = geometry['gradient_source']*row['velocity']+spatial*metric_log
    temporal, gradient = row['temporal'], row['gradient']
    temporal_rate = row['velocity']*row['motion_rate']
    momentum_rate = kinetic_rate*temporal+kinetic*temporal_rate
    energy_rate = kinetic_rate*temporal**2/2+kinetic*temporal*temporal_rate
    energy_rate += spatial_rate*gradient**2/2+spatial*gradient*row['rate_gradient']
    exchange = metric_log*(kinetic*temporal**2+spatial*gradient**2)/2
    return dict(momentum_rate=momentum_rate, energy_rate=energy_rate, exchange=exchange,
        energy=(kinetic*temporal**2+spatial*gradient**2)/2)


def full_system(action, tangent, deadline, progress):
    node_count, label_count = len(action.knots), len(action.source)
    component_count = node_count+1
    cell_count = len(action.mesh['elements'])
    field_blocks = np.zeros((cell_count, 3, 3, label_count, label_count))
    cross_blocks = np.zeros((node_count, label_count, label_count))
    source_block = np.zeros((label_count, label_count))
    dust_block = np.zeros_like(source_block)
    momentum = np.zeros((label_count, component_count))
    convection = np.zeros((2, label_count, component_count))
    points, weights = np.polynomial.legendre.leggauss(48)
    points, weights = points/2, weights/2
    weights *= 6*(points+.5)*(.5-points)
    for index, (label, weight) in enumerate(zip(points, weights)):
        if perf_counter() > deadline:
            raise RuntimeError('Saved boundary during exact-clock Hessian assembly.')
        row = samples(action, label, 12)
        wave = wave_data(row, tangent)
        dust = dust_data(action, row['source'], row['velocity'], tangent)
        quadrature, geometry = row['quadrature'], row['geometry']
        measure, indices, shape = quadrature['measure'], quadrature['indices'], row['shape']
        kinetic, motion, temporal = geometry['kinetic'], row['motion'], row['temporal']
        cardinal = row['cardinal']
        outer = weight*np.outer(cardinal, cardinal)
        for first in range(3):
            for second in range(3):
                cell_values = np.bincount(quadrature['cells'],
                    weights=measure*kinetic*shape[:, first]*shape[:, second], minlength=cell_count)
                field_blocks[:, first, second] += cell_values[:, None, None]*outer
        cross_values = np.zeros(node_count)
        np.add.at(cross_values, indices.ravel(), (measure[:, None]*kinetic[:, None]*motion[:, None]*shape).ravel())
        cross_blocks += cross_values[:, None, None]*outer
        source_block += (measure @ (kinetic*motion**2)+dust['inertia'])*outer
        dust_block += dust['inertia']*outer
        field_values = np.zeros(node_count)
        np.add.at(field_values, indices.ravel(), (measure[:, None]*kinetic[:, None]*temporal[:, None]*shape).ravel())
        source_value = measure @ (kinetic*temporal*motion)+dust['momentum']
        momentum += weight*np.outer(cardinal, np.r_[field_values, source_value])
        for estimate in range(2):
            field_values = np.zeros(node_count)
            np.add.at(field_values, indices.ravel(),
                (measure[:, None]*wave['momentum_rate'][estimate, :, None]*shape).ravel())
            source_value = measure @ (wave['momentum_rate'][estimate]*motion+kinetic*temporal*row['motion_rate'])
            source_value += dust['momentum_rate'][estimate]
            convection[estimate] += weight*np.outer(cardinal, np.r_[field_values, source_value])
        if index%8 == 7:
            progress('Hessian-label-'+str(index+1))
    elements = np.asarray(action.mesh['elements'])
    row_nodes = np.broadcast_to(elements[:, :, None, None, None], field_blocks.shape)
    column_nodes = np.broadcast_to(elements[:, None, :, None, None], field_blocks.shape)
    label_rows = np.arange(label_count)[None, None, None, :, None]
    label_columns = np.arange(label_count)[None, None, None, None, :]
    field_rows = np.broadcast_to(row_nodes+component_count*label_rows, field_blocks.shape)
    field_columns = np.broadcast_to(column_nodes+component_count*label_columns, field_blocks.shape)
    selected = (row_nodes>=0)&(column_nodes>=0)
    cross_rows = np.broadcast_to(np.arange(node_count)[:, None, None]+component_count*np.arange(label_count)[None, :, None], cross_blocks.shape)
    cross_columns = np.broadcast_to(node_count+component_count*np.arange(label_count)[None, None, :], cross_blocks.shape)
    source_indices = node_count+component_count*np.arange(label_count)
    rows = np.r_[field_rows[selected], cross_rows.ravel(), cross_columns.ravel(), np.repeat(source_indices, label_count)]
    columns = np.r_[field_columns[selected], cross_columns.ravel(), cross_rows.ravel(), np.tile(source_indices, label_count)]
    values = np.r_[field_blocks[selected], cross_blocks.ravel(), cross_blocks.ravel(), source_block.ravel()]
    matrix = coo_matrix((values, (rows, columns)), shape=(label_count*component_count,)*2).tocsr()
    matrix.eliminate_zeros()
    inverse = BandedSourceInverse(matrix, (label_count, component_count))
    action_result = action.momentum_and_force(12, 48, deadline)
    forcing = action_result['force'][None]-convection
    acceleration = inverse.solve(forcing.reshape(2, -1).T).T.reshape(forcing.shape)
    return dict(matrix=matrix, inverse=inverse, momentum=momentum, convection=convection,
        force=action_result['force'], forcing=forcing, acceleration=acceleration, dust_block=dust_block,
        action_momentum=action_result['momentum'])


def acceleration_polynomials(action, accelerations):
    result = []
    with localcontext() as context:
        context.prec = 64
        for acceleration in accelerations:
            polynomial, unused = local_polynomials(action.mesh, decimal_array(acceleration[:, :-1].T))
            result.append(polynomial)
    return np.asarray(result)


def wave_cut_advection(action, label, targets):
    from annular_candidate_Ward_source_20260921 import fields
    cardinal = np.asarray(action.cardinal(label)).ravel()
    source = cardinal @ action.source
    model = action.owner.model
    inner, outer = model.radii[[0, -1]]+action.owner.width*label
    selected = (targets>inner)&(targets<outer)
    result = np.zeros(len(targets))
    radius = targets[selected]
    jacobian = np.where(radius<source, (source-inner)/(model.anchor-model.radii[0]),
        (outer-source)/(model.radii[-1]-model.anchor))
    reference = np.where(radius<source, model.radii[0]+(radius-inner)/jacobian,
        model.radii[-1]-(outer-radius)/jacobian)
    edges = np.array([float(value) for value in action.edges])
    cells = np.clip(np.searchsorted(edges, reference, side='right')-1, 0, len(edges)-2)
    local = (reference-edges[cells])/(edges[cells+1]-edges[cells])
    values = fields(action, reference, cells, local, label)
    result[selected] = values['speed']*values['energy']
    return result


def localized(action, loads, tangent, targets, accelerations, order, deadline, progress):
    labels, weights, cuts = material_quadrature(loads, targets, order)
    polynomials = acceleration_polynomials(action, accelerations)
    channels = {name:[] for name in ['energy', 'frozen_wave', 'frozen_dust', 'frozen_gram',
        'exchange_wave', 'exchange_dust', 'exchange_gram', 'wave_advection', 'inertia_wave', 'inertia_dust']}
    with localcontext() as context:
        context.prec = 64
        image_rate_vertices = np.asarray(loads.factor.apply(decimal_array(loads.rates[:, :-1].T)), float)
    for index, label in enumerate(labels):
        if perf_counter() > deadline:
            raise RuntimeError('Saved boundary during localized Legendre integration.')
        row = samples(action, label, order, targets)
        wave, dust = wave_data(row, tangent), dust_data(action, row['source'], row['velocity'], tangent)
        quadrature, geometry, cardinal = row['quadrature'], row['geometry'], row['cardinal']
        measures = quadrature['measure'][:, None]*(geometry['radius'][:, None]<targets)
        source_mask = row['source']<targets
        coefficients = np.einsum('ecpl,l->ecp', polynomials, cardinal)[:, quadrature['cells']]
        local = quadrature['local']
        acceleration_field = coefficients[:, :, 0]+local*(coefficients[:, :, 1]+local*coefficients[:, :, 2])
        acceleration_source = accelerations[:, :, -1] @ cardinal
        acceleration_time = acceleration_field+acceleration_source[:, None]*row['motion']
        inertia_wave = (geometry['kinetic']*row['temporal']*acceleration_time) @ measures
        inertia_dust = (dust['inertia']*row['velocity']*acceleration_source)[:, None]*source_mask
        nodal = action.geometry(action.knots, row['source'], label)
        nu_time, metric_time = tangent.at(nodal['radius'])
        metric_log = nu_time+metric_time/(2*nodal['metric'])
        image, image_rate = action.factor_values @ cardinal, image_rate_vertices @ cardinal
        load = np.asarray(action.sampling.T @ (image**2/2)).ravel()
        load_rate = np.asarray(action.sampling.T @ (image*image_rate)).ravel()
        node_energy = nodal['gradient']*load
        masks = nodal['radius'][:, None]<targets
        gram_rate = (nodal['gradient_source']*row['velocity']+nodal['gradient']*metric_log)*load
        gram_rate += nodal['gradient']*load_rate
        channels['energy'].append(wave['energy'] @ measures+dust['energy']*source_mask+node_energy @ masks)
        channels['frozen_wave'].append(wave['energy_rate'] @ measures)
        channels['frozen_dust'].append(dust['energy_rate'][:, None]*source_mask)
        channels['frozen_gram'].append(gram_rate @ masks)
        channels['exchange_wave'].append(wave['exchange'] @ measures)
        channels['exchange_dust'].append(dust['exchange'][:, None]*source_mask)
        channels['exchange_gram'].append((node_energy*metric_log) @ masks)
        channels['wave_advection'].append(wave_cut_advection(action, label, targets))
        channels['inertia_wave'].append(inertia_wave)
        channels['inertia_dust'].append(inertia_dust)
        if index%32 == 31 or index==len(labels)-1:
            progress('local-order'+str(order)+'-label'+str(index+1)+'of'+str(len(labels)))
    packed = {key:np.asarray(value) for key, value in channels.items()}
    summed = {key:np.tensordot(weights, value, axes=(0, 0)) for key, value in packed.items()}
    old_gram, unused = gram_cut_current(loads, action, targets, 64)
    exchange = summed['exchange_wave']+summed['exchange_dust']+summed['exchange_gram']
    frozen = summed['frozen_wave']+summed['frozen_dust']+summed['frozen_gram']
    advection = summed['wave_advection']+old_gram['advection']
    frozen -= advection
    inertia = summed['inertia_wave']+summed['inertia_dust']
    current = exchange-frozen-inertia[:2]
    projection = inertia[:2]-inertia[2:]
    return dict(labels=labels, weights=weights, cuts=cuts, targets=targets, exchange=exchange,
        frozen=frozen, inertia=inertia, current=current, projection=projection,
        gram_advection=old_gram['advection'], gram_graph=old_gram['graph'],
        **{'label_'+key:value for key, value in packed.items()}, **{'sum_'+key:value for key, value in summed.items()})
