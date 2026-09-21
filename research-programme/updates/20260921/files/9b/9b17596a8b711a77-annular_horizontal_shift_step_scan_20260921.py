from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_Legendre_current_20260921 import samples
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from decimal import localcontext, Decimal
import numpy as np


def shift_spot_scan(action, loads, tangent, saved, acceleration, label, profile, steps):
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
    steps = np.asarray(steps,dtype=float)
    values = np.array([[finite(-step),finite(step)] for step in steps])
    centered = (values[:,1]-values[:,0])/(2*steps[:,None])
    derivative = (4*centered[1:]-centered[:-1])/3
    baseline = np.array([measure @ (kinetic*row['temporal']**2-spatial*row['gradient']**2)/2,
        -(action.sampling @ nodes['gradient']) @ base_factor**2/2,-action.owner.source_mass*source_clock])
    return dict(label=float(label),profile=int(profile),raw=raw,finite=derivative,
        error=abs(derivative-raw),steps=steps,values=values,zero=finite(0.),baseline=baseline,
        raw_wave_field=raw_wave_field,raw_wave_coefficient=raw_wave_coefficient,
        raw_gram_field=raw_gram_field,raw_gram_coefficient=raw_gram_coefficient,
        omitted_moving_clock=omitted_moving_clock,
        chart_minimum=float(min(metric)),maximum_source_speed=float(abs(source_velocity)/(lapse[-1]*np.sqrt(metric[-1]))))
