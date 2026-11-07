from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_boundary_integral_20260930 import quadratic
from annular_position_support_column_20260930 import coefficient_changes
from annular_support_shift_jet_20260928 import wave_terms
from annular_old_field_reaction_20260929 import coefficient_data
import numpy as np


def force_packet(evaluator, data, offsets):
    local,width=data['local'],data['width']
    radius=evaluator.anchor+offsets
    values,value_r,radial,radial_r=evaluator.metric.evaluate(offsets,evaluator.metric.cells(offsets))
    positions=[item.evaluate(offsets,item.cells(offsets)) for item in evaluator.responses]
    times=[item.evaluate(offsets,item.cells(offsets)) for item in evaluator.time_traces]
    time=sum(item[0] for item in times)
    mixed=sum(item.evaluate(offsets,item.cells(offsets))[0] for item in evaluator.mixed_traces)
    movement=data['movement_left']+(data['movement_right']-data['movement_left'])*local
    dilation=(data['movement_right']-data['movement_left'])/width
    displacement=data['displacement_left']+(data['displacement_right']-data['displacement_left'])*local
    displacement_r=(data['displacement_right']-data['displacement_left'])/width
    alpha,beta,alpha_r,beta_r=coefficient_data(radius,values,radial)
    rate,rate_r=quadratic(data['rate'],local,width)
    field,field_r=quadratic(data['test'],local,width)
    packet=dict(radius=radius,alpha=alpha,beta=beta,alpha_r=alpha_r,beta_r=beta_r,
        alpha_t=-alpha*(time[1]-time[0]/(radius*(1-2*values[0]/radius))),
        gradient=quadratic(data['field'],local,width)[1],rate=rate,rate_r=rate_r,
        acceleration=quadratic(data['acceleration'],local,width)[0],
        speed=displacement*data['source_velocity'],speed_r=displacement_r*data['source_velocity'],
        speed_rate=displacement*data['source_acceleration'],
        eta=data['eta_left']+(data['eta_right']-data['eta_left'])*local,
        eta_r=(data['eta_right']-data['eta_left'])/width,field=field,field_r=field_r)
    rate_change,rate_r_change=quadratic(data['rate_change'],local,width)
    direction=dict(movement=movement,movement_r=dilation,values=values,radial=radial,time=time,
        material_values=sum(item[0] for item in positions)+value_r*movement,
        material_radial=sum(item[2] for item in positions)+radial_r*movement,
        material_time=mixed+sum(item[1] for item in times)*movement,
        gradient=quadratic(data['field_change'],local,width)[1],rate=rate_change,rate_r=rate_r_change,
        acceleration=quadratic(data['acceleration_change'],local,width)[0],
        speed=displacement*data['source_rate_change'],speed_r=displacement_r*data['source_rate_change'],
        speed_rate=displacement*data['source_acceleration_change'])
    return packet,direction


def analytic_force(packet, direction):
    alpha, beta, gradient, speed, speed_r, temporal, gradient_rate, temporal_rate, alpha_dot, beta_dot, energy, energy_dot, momentum_rate, flux = wave_terms(packet)
    delta = coefficient_changes(packet, direction)
    dilation = direction['movement_r']
    for key in ['gradient', 'rate_r', 'speed_r']:
        delta[key] = direction[key] - dilation * packet[key]
    for key in ['rate', 'speed', 'speed_rate', 'acceleration']:
        delta[key] = direction[key]
    temporal_change = delta['rate'] - delta['speed'] * gradient - speed * delta['gradient']
    gradient_rate_change = delta['rate_r'] - delta['speed_r'] * gradient - speed_r * delta['gradient']
    temporal_rate_change = delta['acceleration'] - delta['speed_rate'] * gradient
    temporal_rate_change -= packet['speed_rate'] * delta['gradient'] + delta['speed'] * gradient_rate + speed * gradient_rate_change
    alpha_dot_change = delta['alpha_t'] + delta['speed'] * packet['alpha_r'] + speed * delta['alpha_r']
    beta_dot_change = -delta['beta'] * packet['alpha_t'] / alpha - beta * delta['alpha_t'] / alpha
    beta_dot_change += beta * packet['alpha_t'] * delta['alpha'] / alpha**2
    beta_dot_change += delta['speed'] * packet['beta_r'] + speed * delta['beta_r']
    momentum_change = (alpha_dot_change + delta['speed_r'] * alpha + speed_r * delta['alpha']) * temporal
    momentum_change += (alpha_dot + speed_r * alpha) * temporal_change
    momentum_change += delta['alpha'] * temporal_rate + alpha * temporal_rate_change
    flux_change = (delta['alpha'] * speed + alpha * delta['speed']) * temporal + alpha * speed * temporal_change
    flux_change += delta['beta'] * gradient + beta * delta['gradient']
    energy_change = (delta['alpha'] * temporal**2 + delta['beta'] * gradient**2) / 2
    energy_change += alpha * temporal * temporal_change + beta * gradient * delta['gradient']
    energy_dot_change = (alpha_dot_change * temporal**2 + beta_dot_change * gradient**2) / 2
    energy_dot_change += alpha_dot * temporal * temporal_change + beta_dot * gradient * delta['gradient']
    energy_dot_change += delta['alpha'] * temporal * temporal_rate + alpha * temporal_change * temporal_rate + alpha * temporal * temporal_rate_change
    energy_dot_change += delta['beta'] * gradient * gradient_rate + beta * delta['gradient'] * gradient_rate + beta * gradient * gradient_rate_change
    eta, eta_r, test, test_r = [packet[key] for key in ['eta', 'eta_r', 'field', 'field_r']]
    force_change = momentum_change * (test - gradient * eta) - momentum_rate * delta['gradient'] * eta
    force_change += (flux_change - dilation * flux) * test_r
    force_change -= (delta['alpha'] * temporal * gradient_rate + alpha * temporal_change * gradient_rate + alpha * temporal * gradient_rate_change) * eta
    potential_change = delta['alpha_r'] * temporal**2 + 2 * packet['alpha_r'] * temporal * temporal_change
    potential_change -= delta['beta_r'] * gradient**2 + 2 * packet['beta_r'] * gradient * delta['gradient']
    force_change -= potential_change * eta / 2
    mixed_change = (delta['alpha'] * speed + alpha * delta['speed']) * temporal * gradient
    mixed_change += alpha * speed * (temporal_change * gradient + temporal * delta['gradient'])
    force_change -= (energy_change + mixed_change - dilation * (energy + alpha * speed * temporal * gradient)) * eta_r
    force = momentum_rate*(test-gradient*eta)+flux*test_r-alpha*temporal*gradient_rate*eta
    force -= (packet['alpha_r']*temporal**2-packet['beta_r']*gradient**2)*eta/2
    force -= (energy+alpha*speed*temporal*gradient)*eta_r
    return force_change+dilation*force
