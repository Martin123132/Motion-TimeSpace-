from annular_C0_boundary_integral_20260930 import quadratic
from annular_C0_decimal_transport_20260930 import precise_exp, precise_sqrt
import numpy as np


def compact_rows(data, radius, values, radial, time, precise=False):
    local, width = data['local'], data['width']
    gradient = quadratic(data['field'], local, width)[1]
    rate, rate_r = quadratic(data['rate'], local, width)
    acceleration = quadratic(data['acceleration'], local, width)[0]
    displacement = data['displacement_left']+(data['displacement_right']-data['displacement_left'])*local
    speed = displacement*data['source_velocity']
    speed_r = (data['displacement_right']-data['displacement_left'])*data['source_velocity']/width
    speed_rate = displacement*data['source_acceleration']
    test, test_r = quadratic(data['test'], local, width)
    eta = data['eta_left']+(data['eta_right']-data['eta_left'])*local
    eta_r = (data['eta_right']-data['eta_left'])/width
    metric = 1-2*values[0]/radius
    metric_r = -2*radial[0]/radius+2*values[0]/radius**2
    lapse = precise_exp(values[1]) if precise else np.exp(values[1])
    root = precise_sqrt(metric) if precise else np.sqrt(metric)
    alpha, beta = radius**2/(lapse*root), radius**2*lapse*root
    alpha_r = alpha*(2/radius-radial[1]-metric_r/(2*metric))
    beta_r = beta*(2/radius+radial[1]+metric_r/(2*metric))
    alpha_t = -alpha*(time[1]-time[0]/(radius*metric))
    temporal = rate-speed*gradient
    gradient_rate = rate_r-speed_r*gradient
    momentum_rate = (alpha_t+speed*alpha_r+speed_r*alpha)*temporal
    momentum_rate += alpha*(acceleration-speed_rate*gradient-speed*gradient_rate)
    flux = alpha*speed*temporal+beta*gradient
    energy = (alpha*temporal**2+beta*gradient**2)/2
    compact_energy = speed*(beta_r*gradient**2-alpha_r*temporal**2)/2+beta*gradient*rate_r-speed_r*energy
    force = momentum_rate*(test-gradient*eta)+flux*test_r-alpha*temporal*gradient_rate*eta
    force -= (alpha_r*temporal**2-beta_r*gradient**2)*eta/2
    force -= (energy+alpha*speed*temporal*gradient)*eta_r
    rows = [force]
    basis = [(1-local)*(1-2*local), 4*local*(1-local), local*(2*local-1)]
    basis_r = [(4*local-3)/width, (4-8*local)/width, (4*local-1)/width]
    node_width = data['node_right']-data['node_left']
    radius_offset, source_offset = radius-6, data['source']-6
    for power in range(3):
        integral = (radius-data['source'])*sum(radius_offset**(power-index)*source_offset**index for index in range(power+1))/(power+1)
        factor = -speed*gradient*integral
        weighted_r = np.zeros_like(rate)
        for fraction, shape, shape_r in zip([0., .5, 1.], basis, basis_r):
            node_radius = data['node_left']+fraction*node_width
            node_offset = node_radius-6
            node_rate = data['rate'][:, 0]+fraction*(data['rate'][:, 1]+fraction*data['rate'][:, 2])
            separation = (radius-data['node_left'])-fraction*node_width
            delta = separation*sum(radius_offset**(power-index)*node_offset**index for index in range(power+1))/(power+1)
            node_integral = (node_radius-data['source'])*sum(node_offset**(power-index)*source_offset**index for index in range(power+1))/(power+1)
            factor += shape*node_rate*delta
            weighted_r += shape_r*node_rate*node_integral
        rows.append(momentum_rate*factor-flux*weighted_r+compact_energy*integral+energy*speed*radius_offset**power)
    return np.array(rows)
