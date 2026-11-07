from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_C0_boundary_integral_20260930 import quadratic
import numpy as np


def stable_density_rows(data, radius, values, radial, time, amount=0., material=False):
    width = data['width'] + amount * (data['movement_right']-data['movement_left'])
    movement = data['movement_left']+(data['movement_right']-data['movement_left'])*data['local']
    local = data['local'] if material else data['local']-amount*movement/width
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
    lapse = np.exp(values[1])
    alpha, beta = radius**2/(lapse*np.sqrt(metric)), radius**2*lapse*np.sqrt(metric)
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
    baseline_node_width = data['node_right']-data['node_left']
    node_movement_width = data['movement_right']-data['movement_left']
    rate_nodes = data['rate']+amount*data['rate_change']
    radius_offset, source_offset = radius-6, source-6
    shapes = [(1-local)*(1-2*local), 4*local*(1-local), local*(2*local-1)]
    gradients = [(4*local-3)/width, (4-8*local)/width, (4*local-1)/width]
    remainder = -alpha*speed*temporal*rate_r
    remainder -= (speed*alpha_r+alpha*speed_r)*temporal**2/2
    remainder += (speed*beta_r-beta*speed_r)*gradient**2/2
    for power in range(3):
        integral = (radius-source)*sum(radius_offset**(power-index)*source_offset**index
            for index in range(power+1))/(power+1)
        difference, derivative_difference = np.zeros_like(rate), np.zeros_like(rate)
        for fraction, basis, basis_r in zip([0., .5, 1.], shapes, gradients):
            node_movement = data['movement_left']+fraction*node_movement_width
            node_offset = (data['node_left']-6)+fraction*baseline_node_width+amount*node_movement
            separation = (radius-data['node_left'])-fraction*baseline_node_width-amount*node_movement
            delta_integral = separation*sum(radius_offset**(power-index)*node_offset**index
                for index in range(power+1))/(power+1)
            node_rate = rate_nodes[:, 0]+fraction*(rate_nodes[:, 1]+fraction*rate_nodes[:, 2])
            difference = difference+basis*node_rate*delta_integral
            derivative_difference = derivative_difference+basis_r*node_rate*delta_integral
        current = momentum_rate*(difference-speed*gradient*integral)+flux*derivative_difference
        current += remainder*integral+energy*speed*radius_offset**power
        rows.append(current)
    return np.array(rows)
