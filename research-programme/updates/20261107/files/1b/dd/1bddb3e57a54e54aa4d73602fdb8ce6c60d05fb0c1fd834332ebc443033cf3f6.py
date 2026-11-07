from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_boundary_integral_20260930 import quadratic
from mpmath import mp
import numpy as np


def precise_exp(values):
    return np.array([mp.exp(value) for value in values.ravel()], dtype=object).reshape(values.shape)


def precise_sqrt(values):
    return np.array([mp.sqrt(value) for value in values.ravel()], dtype=object).reshape(values.shape)


def eulerian_density(data, radius, values, radial, time, amount=0.):
    width = data['width'] + amount * (data['movement_right']-data['movement_left'])
    local = (data['local']*data['width']-amount*data['movement_left'])/width
    source = data['source'] + amount*data['source_change']
    gradient = quadratic(data['field']+amount*data['field_change'], local, width)[1]
    rate, rate_r = quadratic(data['rate']+amount*data['rate_change'], local, width)
    acceleration = quadratic(data['acceleration']+amount*data['acceleration_change'], local, width)[0]
    displacement = data['displacement_left']+(data['displacement_right']-data['displacement_left'])*local
    source_velocity = data['source_velocity']+amount*data['source_rate_change']
    speed = displacement*source_velocity
    speed_r = (data['displacement_right']-data['displacement_left'])*source_velocity/width
    speed_rate = displacement*(data['source_acceleration']+amount*data['source_acceleration_change'])
    test, test_r = quadratic(data['test'], local, width)
    eta = data['eta_left']+(data['eta_right']-data['eta_left'])*local
    eta_r = (data['eta_right']-data['eta_left'])/width
    metric = 1-2*values[0]/radius
    metric_r = -2*radial[0]/radius+2*values[0]/radius**2
    lapse = precise_exp(values[1])
    alpha, beta = radius**2/(lapse*precise_sqrt(metric)), radius**2*lapse*precise_sqrt(metric)
    alpha_r = alpha*(2/radius-radial[1]-metric_r/(2*metric))
    beta_r = beta*(2/radius+radial[1]+metric_r/(2*metric))
    alpha_t = -alpha*(time[1]-time[0]/(radius*metric))
    temporal = rate-speed*gradient
    gradient_rate = rate_r-speed_r*gradient
    temporal_rate = acceleration-speed_rate*gradient-speed*gradient_rate
    alpha_dot = alpha_t+speed*alpha_r
    beta_dot = -beta*alpha_t/alpha+speed*beta_r
    momentum_rate = (alpha_dot+speed_r*alpha)*temporal+alpha*temporal_rate
    flux = alpha*speed*temporal+beta*gradient
    energy = (alpha*temporal**2+beta*gradient**2)/2
    energy_dot = (alpha_dot*temporal**2+beta_dot*gradient**2)/2
    energy_dot += alpha*temporal*temporal_rate+beta*gradient*gradient_rate
    force = momentum_rate*(test-gradient*eta)+flux*test_r-alpha*temporal*gradient_rate*eta
    force -= (alpha_r*temporal**2-beta_r*gradient**2)*eta/2
    force -= (energy+alpha*speed*temporal*gradient)*eta_r
    rows = [force]
    node_left = data['node_left']+amount*data['movement_left']
    node_right = data['node_right']+amount*data['movement_right']
    node_rates = data['rate']+amount*data['rate_change']
    for power in range(3):
        integral = ((radius-6)**(power+1)-(source-6)**(power+1))/(power+1)
        weighted_nodes = []
        for fraction in [0., .5, 1.]:
            node_radius = node_left+(node_right-node_left)*fraction
            node_rate = node_rates[:, 0]+fraction*(node_rates[:, 1]+fraction*node_rates[:, 2])
            weighted_nodes.append(node_rate*((node_radius-6)**(power+1)-(source-6)**(power+1))/(power+1))
        left, middle, right = weighted_nodes
        weighted = left*(1-local)*(1-2*local)+4*middle*local*(1-local)+right*local*(2*local-1)
        weighted_r = (left*(4*local-3)+middle*(4-8*local)+right*(4*local-1))/width
        current = -momentum_rate*weighted-flux*weighted_r
        current += (energy_dot+(speed_r+alpha_t/alpha)*energy)*integral+energy*speed*(radius-6)**power
        rows.append(current)
    return np.array(rows)


def material_density(data, radius, values, radial, time, amount=0.):
    width = data['width'] + amount * (data['movement_right']-data['movement_left'])
    local = data['local']
    source = data['source'] + amount*data['source_change']
    gradient = quadratic(data['field']+amount*data['field_change'], local, width)[1]
    rate, rate_r = quadratic(data['rate']+amount*data['rate_change'], local, width)
    acceleration = quadratic(data['acceleration']+amount*data['acceleration_change'], local, width)[0]
    displacement = data['displacement_left']+(data['displacement_right']-data['displacement_left'])*local
    source_velocity = data['source_velocity']+amount*data['source_rate_change']
    speed = displacement*source_velocity
    speed_r = (data['displacement_right']-data['displacement_left'])*source_velocity/width
    speed_rate = displacement*(data['source_acceleration']+amount*data['source_acceleration_change'])
    test, test_r = quadratic(data['test'], local, width)
    eta = data['eta_left']+(data['eta_right']-data['eta_left'])*local
    eta_r = (data['eta_right']-data['eta_left'])/width
    metric = 1-2*values[0]/radius
    metric_r = -2*radial[0]/radius+2*values[0]/radius**2
    lapse = precise_exp(values[1])
    alpha, beta = radius**2/(lapse*precise_sqrt(metric)), radius**2*lapse*precise_sqrt(metric)
    alpha_r = alpha*(2/radius-radial[1]-metric_r/(2*metric))
    beta_r = beta*(2/radius+radial[1]+metric_r/(2*metric))
    alpha_t = -alpha*(time[1]-time[0]/(radius*metric))
    temporal = rate-speed*gradient
    gradient_rate = rate_r-speed_r*gradient
    temporal_rate = acceleration-speed_rate*gradient-speed*gradient_rate
    alpha_dot = alpha_t+speed*alpha_r
    beta_dot = -beta*alpha_t/alpha+speed*beta_r
    momentum_rate = (alpha_dot+speed_r*alpha)*temporal+alpha*temporal_rate
    flux = alpha*speed*temporal+beta*gradient
    energy = (alpha*temporal**2+beta*gradient**2)/2
    energy_dot = (alpha_dot*temporal**2+beta_dot*gradient**2)/2
    energy_dot += alpha*temporal*temporal_rate+beta*gradient*gradient_rate
    force = momentum_rate*(test-gradient*eta)+flux*test_r-alpha*temporal*gradient_rate*eta
    force -= (alpha_r*temporal**2-beta_r*gradient**2)*eta/2
    force -= (energy+alpha*speed*temporal*gradient)*eta_r
    rows = [force]
    node_left = data['node_left']+amount*data['movement_left']
    node_right = data['node_right']+amount*data['movement_right']
    node_rates = data['rate']+amount*data['rate_change']
    for power in range(3):
        integral = ((radius-6)**(power+1)-(source-6)**(power+1))/(power+1)
        weighted_nodes = []
        for fraction in [0., .5, 1.]:
            node_radius = node_left+(node_right-node_left)*fraction
            node_rate = node_rates[:, 0]+fraction*(node_rates[:, 1]+fraction*node_rates[:, 2])
            weighted_nodes.append(node_rate*((node_radius-6)**(power+1)-(source-6)**(power+1))/(power+1))
        left, middle, right = weighted_nodes
        weighted = left*(1-local)*(1-2*local)+4*middle*local*(1-local)+right*local*(2*local-1)
        weighted_r = (left*(4*local-3)+middle*(4-8*local)+right*(4*local-1))/width
        current = -momentum_rate*weighted-flux*weighted_r
        current += (energy_dot+(speed_r+alpha_t/alpha)*energy)*integral+energy*speed*(radius-6)**power
        rows.append(current)
    return np.array(rows)
