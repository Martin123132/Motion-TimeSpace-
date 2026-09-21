from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_Legendre_current_20260921 import MetricTangent, samples, wave_data, dust_data, acceleration_polynomials
from annular_candidate_Ward_source_20260921 import fields
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from decimal import localcontext, Decimal
from time import perf_counter
import numpy as np


class CachedTangent(MetricTangent):
    def at(self, radius):
        if radius is not getattr(self, 'last_radius', None):
            self.last_value = super().at(radius)
            self.last_radius = radius
        return self.last_value


def layer_current(action, loads, tangent, label, targets, accelerations, polynomials, order, gram_power, gram_source, image_rates):
    row = samples(action, label, order, targets)
    wave = wave_data(row, tangent)
    geometry, quadrature, cardinal = row['geometry'], row['quadrature'], row['cardinal']
    nu_time, metric_time = tangent.at(geometry['radius'])
    metric_log = (nu_time+metric_time/(2*geometry['metric']))[[0,1,0,1]]
    dust = dust_data(action, row['source'], row['velocity'], tangent)
    measure, local, cells = quadrature['measure'], quadrature['local'], quadrature['cells']
    source_acceleration = accelerations[:, :, -1] @ cardinal
    coefficients = np.einsum('ecpl,l->ecp', polynomials, cardinal)[:, cells]
    field_acceleration = coefficients[:, :, 0]+local*(coefficients[:, :, 1]+local*coefficients[:, :, 2])
    temporal_acceleration = field_acceleration+source_acceleration[:, None]*row['motion']
    kinetic, spatial, jacobian = geometry['kinetic'], geometry['gradient'], geometry['jacobian']
    temporal, gradient = row['temporal'], row['gradient']
    momentum_rate = wave['momentum_rate'][[0,1,0,1]]+kinetic*temporal_acceleration
    nodal = action.geometry(action.knots, row['source'], label)
    node_mask = nodal['radius'][:, None]<targets
    source_mask = row['source']<targets
    node_rate = cardinal @ loads.rates[:, :-1]
    masked_rate = node_rate[:, None]*node_mask
    local_rate = masked_rate[quadrature['indices']]
    test = np.einsum('qi,qik->qk', row['shape'], local_rate)
    test_gradient = np.einsum('qi,qik->qk', quadrature['radial'], local_rate)
    force_coefficient = -(kinetic*temporal*row['velocity']*geometry['displacement']/jacobian+spatial*gradient)
    field_work = (measure*force_coefficient) @ test_gradient-(momentum_rate*measure) @ test+gram_power @ node_mask
    source_wave_force = measure @ (geometry['kinetic_source']*temporal**2/2
        -kinetic*temporal*row['velocity']*row['motion']*geometry['jacobian_source']/jacobian
        -geometry['gradient_source']*gradient**2/2)
    source_wave_rate = (wave['momentum_rate'][[0,1,0,1]]*row['motion']
        +kinetic*temporal*row['motion_rate']+kinetic*row['motion']*temporal_acceleration) @ measure
    source_wave_work = row['velocity']*(source_wave_force-source_wave_rate)+np.sum(gram_source)
    unused, dust_force, unused2, unused3 = action.dust(row['source'], row['velocity'])
    source_dust_work = row['velocity']*(dust_force-dust['momentum_rate'][[0,1,0,1]]-dust['inertia']*source_acceleration)
    local_work = field_work+(source_wave_work+source_dust_work)[:, None]*source_mask
    widths = np.diff(np.array([float(value) for value in action.edges]))[cells]
    gradient_coefficients = np.einsum('cpl,l->cp', action.gradient, cardinal)[cells]
    second_gradient = gradient_coefficients[:, 1]/widths
    physical_gradient = gradient/jacobian
    mesh_velocity = geometry['displacement']*row['velocity']
    temporal_radial = (row['rate_gradient']-row['velocity']*(geometry['jacobian_source']*gradient
        +geometry['displacement']*second_gradient)/jacobian)/jacobian
    gradient_time = row['rate_gradient']/jacobian-physical_gradient*geometry['jacobian_source']*row['velocity']/jacobian
    gradient_time -= mesh_velocity*second_gradient/jacobian**2
    temporal_time = temporal_acceleration+row['velocity']*row['motion_rate']-mesh_velocity*temporal_radial
    coefficient = spatial*jacobian
    coefficient_work = -(kinetic/jacobian)*(temporal*temporal_time-temporal**2*metric_log)
    coefficient_work -= coefficient*physical_gradient*gradient_time
    regular = (coefficient_work*(measure*jacobian)) @ (geometry['radius'][:, None]<targets)
    edges = np.array([float(value) for value in action.edges])
    cell_indices = np.arange(len(edges)-1)
    left = fields(action,edges[:-1],cell_indices,np.zeros(len(cell_indices)),label)
    right = fields(action,edges[1:],cell_indices,np.ones(len(cell_indices)),label)
    face_radius = right['radius'][:-1]
    face_speed = (right['speed'][:-1]+left['speed'][1:])/2
    edge_power = face_speed*(left['energy'][1:]-right['energy'][:-1])
    edge_work = edge_power @ (face_radius[:, None]<targets)
    image, image_rate = action.factor_values @ cardinal, image_rates @ cardinal
    load_rate = np.asarray(action.sampling.T @ (image*image_rate)).ravel()
    atom_power = -nodal['gradient']*load_rate+gram_source
    atom_work = atom_power @ node_mask
    primitive = regular+edge_work+atom_work-field_work
    anchored = primitive-primitive[:, -1, None]*source_mask
    noether = primitive[:, -1]-source_wave_work
    return dict(horizontal_without_local_atom=anchored,regular=regular,edges=edge_work,atoms=atom_work,
        field_Euler_work=field_work,source_wave_work=source_wave_work,source_dust_work=source_dust_work,
        localized_Euler_work=local_work,whole_layer_Noether=noether,
        source=row['source'],velocity=row['velocity'])


def current_comparison(action,loads,tangent,targets,accelerations,previous,ward,order,deadline,progress):
    labels, weights = previous['labels'], previous['weights']
    if not np.array_equal(labels,ward['labels']):
        raise ValueError('Saved label segmentation differs; cannot reuse Gram powers.')
    polynomials = acceleration_polynomials(action,accelerations)
    with localcontext() as context:
        context.prec = 64
        image_rates = np.asarray(loads.factor.apply(decimal_array(loads.rates[:, :-1].T)),float)
    rows = []
    for index,label in enumerate(labels):
        if perf_counter()>deadline:
            raise RuntimeError('Safe saved-work boundary during shift-current integration.')
        rows.append(layer_current(action,loads,tangent,label,targets,accelerations,polynomials,order,
            ward['label_node_field_power'][index],ward['label_node_source_power'][index],image_rates))
        if index%32==31 or index==len(labels)-1:
            progress('order'+str(order)+'-label'+str(index+1)+'of'+str(len(labels)))
    raw = {key:np.asarray([row[key] for row in rows]) for key in rows[0]}
    summed = {key:np.tensordot(weights,value,axes=(0,0)) for key,value in raw.items()}
    current = summed['horizontal_without_local_atom']+previous['gram_advection']
    expected = previous['exchange'][[0,1,0,1]]-previous['frozen'][[0,1,0,1]]-previous['inertia']
    expected -= summed['localized_Euler_work']
    return dict(labels=labels,weights=weights,targets=targets,current=current,expected=expected,
        **{'label_'+key:value for key,value in raw.items()},**{'sum_'+key:value for key,value in summed.items()})


def shift_spot(action, loads, tangent, saved, acceleration, label, profile):
    row = samples(action,label,12)
    quadrature, geometry, cardinal = row['quadrature'],row['geometry'],row['cardinal']
    nodes = action.geometry(action.knots,row['source'],label)
    radii = np.r_[geometry['radius'],nodes['radius'],row['source']]
    values,unused = action.solver.values(action.solution,radii)
    lapse,metric = np.exp(values[1]),1-2*values[0]/radii
    nu_time,metric_time = tangent.at(radii)
    nu_time,metric_time = nu_time[-1],metric_time[-1]
    center = row['source']
    direction = (radii-center)**profile
    primitive = (radii-center)**(profile+1)/(profile+1)
    direction_source = direction[-1]
    clock_rate = -direction_source*row['velocity']
    regular_count,node_count = len(geometry['radius']),len(nodes['radius'])
    node_slice = slice(regular_count,regular_count+node_count)
    source_velocity = row['velocity']
    node_speed = nodes['displacement']*source_velocity
    with localcontext() as context:
        context.prec = 64
        card_decimal = decimal_array(cardinal)
        coordinates = decimals(saved['coordinates'])[:, :-1].T @ card_decimal
        velocities = decimal_array(loads.rates[:, :-1].T) @ card_decimal
        accelerations = decimal_array(acceleration[:, :-1].T) @ card_decimal
        delta_coordinate = velocities*decimal_array(primitive[node_slice])
        delta_velocity = accelerations*decimal_array(primitive[node_slice])
        delta_velocity += velocities*decimal_array(clock_rate+direction[node_slice]*node_speed)
        delta_polynomial,delta_gradient = local_polynomials(action.mesh,delta_coordinate[:,None])
        rate_polynomial,unused = local_polynomials(action.mesh,delta_velocity[:,None])
        delta_factor = np.asarray(loads.factor.apply(delta_coordinate[:,None])[:,0],float)
        base_factor = np.asarray(loads.factor.apply(coordinates[:,None])[:,0],float)
    cells,local,measure = quadrature['cells'],quadrature['local'],quadrature['measure']
    delta_gradient = delta_gradient[cells,0,0]+local*delta_gradient[cells,1,0]
    delta_rate = rate_polynomial[cells,0,0]+local*(rate_polynomial[cells,1,0]+local*rate_polynomial[cells,2,0])
    delta_temporal = delta_rate-geometry['displacement']*source_velocity*delta_gradient/geometry['jacobian']
    coefficient = radii**2*lapse*np.sqrt(metric)
    coefficient_time = coefficient*(nu_time+metric_time/(2*metric))
    delta_coefficient = coefficient_time*primitive+coefficient*clock_rate
    regular = slice(0,regular_count)
    kinetic,spatial = geometry['kinetic'],geometry['gradient']
    raw_wave_field = measure @ (kinetic*row['temporal']*delta_temporal-spatial*row['gradient']*delta_gradient)
    dual = -(kinetic*row['temporal']**2+spatial*row['gradient']**2)/(2*coefficient[regular])
    raw_wave_coefficient = measure @ (dual*delta_coefficient[regular])
    node_load = np.asarray(action.sampling.T @ (base_factor**2/2)).ravel()
    raw_gram_field = -(action.sampling @ nodes['gradient']*base_factor) @ delta_factor
    raw_gram_coefficient = -(node_load/nodes['jacobian']) @ delta_coefficient[node_slice]
    source_clock = np.sqrt(lapse[-1]**2-source_velocity**2/metric[-1])
    raw_dust = action.owner.source_mass*source_velocity*lapse[-1]**2*direction_source/source_clock
    raw = np.array([raw_wave_field+raw_wave_coefficient,raw_gram_field+raw_gram_coefficient,raw_dust])
    moving_only = np.asarray(velocities,float)*direction[node_slice]*node_speed
    with localcontext() as context:
        context.prec = 64
        moving_polynomial,unused = local_polynomials(action.mesh,decimal_array(moving_only[:,None]))
    moving_rate = moving_polynomial[cells,0,0]+local*(moving_polynomial[cells,1,0]+local*moving_polynomial[cells,2,0])
    omitted_moving_clock = float(measure @ (kinetic*row['temporal']*moving_rate))
    def finite(amplitude):
        times = amplitude*primitive
        time_jacobian = 1+amplitude*clock_rate
        timed_lapse = lapse*np.exp(nu_time*times)
        timed_metric = metric+metric_time*times
        connection = amplitude*direction
        shift = 2*connection*timed_lapse**2*timed_metric/(1+np.sqrt(1+4*connection**2*timed_lapse**2*timed_metric))
        changed_coefficient = time_jacobian*radii**2*(timed_lapse**2*timed_metric-shift**2)/(timed_lapse*np.sqrt(timed_metric))
        with localcontext() as context:
            context.prec = 64
            node_times = decimal_array(times[node_slice])
            transported = coordinates+node_times*velocities+node_times**2*accelerations/Decimal(2)
            transported_rate = (velocities+node_times*accelerations)*decimal_array(time_jacobian+connection[node_slice]*node_speed)
            polynomial,gradient = local_polynomials(action.mesh,transported[:,None])
            rate_polynomial,unused = local_polynomials(action.mesh,transported_rate[:,None])
            factor = np.asarray(loads.factor.apply(transported[:,None])[:,0],float)
        gradient = gradient[cells,0,0]+local*gradient[cells,1,0]
        rate = rate_polynomial[cells,0,0]+local*(rate_polynomial[cells,1,0]+local*rate_polynomial[cells,2,0])
        temporal = rate-geometry['displacement']*source_velocity*gradient/geometry['jacobian']
        wave_action = measure @ (geometry['jacobian']*radii[regular]**4*temporal**2/changed_coefficient[regular]
            -changed_coefficient[regular]*gradient**2/geometry['jacobian'])/2
        gram_action = -(action.sampling @ (changed_coefficient[node_slice]/nodes['jacobian'])) @ factor**2/2
        dust_action = -action.owner.source_mass*np.sqrt(lapse[-1]**2-(source_velocity+shift[-1])**2/metric[-1])
        return np.array([wave_action,gram_action,dust_action])
    steps = np.array([.001,.0005])
    values = np.array([[finite(-step),finite(step)] for step in steps])
    centered = (values[:,1]-values[:,0])/(2*steps[:,None])
    derivative = (4*centered[1]-centered[0])/3
    baseline = np.array([measure @ (kinetic*row['temporal']**2-spatial*row['gradient']**2)/2,
        -(action.sampling @ nodes['gradient']) @ base_factor**2/2,-action.owner.source_mass*source_clock])
    return dict(label=float(label),profile=int(profile),raw=raw,finite=derivative,
        error=abs(derivative-raw),steps=steps,values=values,zero=finite(0.),baseline=baseline,
        raw_wave_field=raw_wave_field,raw_wave_coefficient=raw_wave_coefficient,
        raw_gram_field=raw_gram_field,raw_gram_coefficient=raw_gram_coefficient,
        omitted_moving_clock=omitted_moving_clock,
        chart_minimum=float(min(metric)),maximum_source_speed=float(abs(source_velocity)/(lapse[-1]*np.sqrt(metric[-1]))))
