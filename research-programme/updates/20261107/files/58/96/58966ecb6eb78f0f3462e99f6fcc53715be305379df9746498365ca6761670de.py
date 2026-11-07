from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_boundary_integral_20260930 import quadratic
from annular_C0_decimal_transport_20260930 import eulerian_density, precise_exp, precise_sqrt
from probe_annular_C0_precise_transport_20260930 import converted
from mpmath import mp
import numpy as np


def channel_geometry(packet,radius,values,precise=False):
    local,width = packet['local'],packet['width']
    gradient = quadratic(packet['field'],local,width)[1]
    rate = quadratic(packet['rate'],local,width)[0]
    displacement = packet['displacement_left']+(packet['displacement_right']-packet['displacement_left'])*local
    speed = displacement*packet['source_velocity']
    temporal = rate-speed*gradient
    eta = packet['eta_left']+(packet['eta_right']-packet['eta_left'])*local
    test = quadratic(packet['test'],local,width)[0]
    metric = 1-2*values[0]/radius
    alpha = radius**2/((precise_exp(values[1]) if precise else np.exp(values[1]))
        *(precise_sqrt(metric) if precise else np.sqrt(metric)))
    factors = [test-eta*gradient]
    basis = [(1-local)*(1-2*local),4*local*(1-local),local*(2*local-1)]
    node_width = packet['node_right']-packet['node_left']
    radius_offset,source_offset = radius-6,packet['source']-6
    for power in range(3):
        integral = (radius-packet['source'])*sum(radius_offset**(power-index)*source_offset**index
            for index in range(power+1))/(power+1)
        difference = np.zeros_like(rate)
        for fraction,shape in zip([0.,.5,1.],basis):
            node_offset = packet['node_left']-6+fraction*node_width
            separation = (radius-packet['node_left'])-fraction*node_width
            delta = separation*sum(radius_offset**(power-index)*node_offset**index
                for index in range(power+1))/(power+1)
            node_rate = packet['rate'][:,0]+fraction*(packet['rate'][:,1]+fraction*packet['rate'][:,2])
            difference += shape*node_rate*delta
        factors.append(difference-speed*gradient*integral)
    factors = np.array(factors)
    return alpha,temporal,metric,gradient,factors


def density_from_geometry(radius,geometry,acceleration,map_acceleration,metric_time):
    alpha,temporal,metric,gradient,factors = geometry
    fixed = alpha*(acceleration-map_acceleration*gradient)
    induced = alpha*temporal*(metric_time[0]/(radius*metric)-metric_time[1])
    return np.array([fixed*factors,induced*factors])


def weights_and_density(packet,radius,values,acceleration,map_acceleration,metric_time,precise=False):
    return density_from_geometry(radius,channel_geometry(packet,radius,values,precise),
        acceleration,map_acceleration,metric_time)


def directions(packet,channel):
    local,width = packet['local'],packet['width']
    displacement = packet['displacement_left']+(packet['displacement_right']-packet['displacement_left'])*local
    if channel=='reaction':
        return quadratic(packet['acceleration_uncertainty'],local,width)[0],displacement*packet['source_uncertainty']
    if channel=='C2':
        eta = packet['eta_left']+(packet['eta_right']-packet['eta_left'])*local
        return quadratic(packet['field_change'],local,width)[0],eta+displacement*packet['source_change']
    raise ValueError(channel)


def precise_check(packet,radius,values,radial,time,metric_time,channel):
    mp.dps = 96
    data = {name:converted(value) for name,value in packet.items()}
    radius,values,radial,time,metric_time = [converted(value) for value in [radius,values,radial,time,metric_time]]
    acceleration,map_acceleration = directions(data,channel)
    gradient = quadratic(data['field'],data['local'],data['width'])[1]
    exact = weights_and_density(data,radius,values,acceleration,map_acceleration,metric_time,True).sum(axis=0)
    derivatives = []
    for step in [mp.mpf('1e-24'),mp.mpf('1e-28')]:
        pairs = []
        for sign in [-1,1]:
            moved = dict(data,acceleration=data['acceleration'].copy())
            moved['acceleration'][:,0] += sign*step*(acceleration-map_acceleration*gradient)
            pairs.append(eulerian_density(moved,radius,values,radial,time+sign*step*metric_time))
        derivatives.append((pairs[1]-pairs[0])/(2*step))
    scale = max(float(np.max(abs(exact))),1e-300)
    return dict(exact=np.asarray(exact,float),oracle=np.asarray(derivatives[-1],float),
        identity_relative=float(np.max(abs(exact-derivatives[-1])))/scale,
        step_relative=float(np.max(abs(derivatives[1]-derivatives[0])))/scale)
