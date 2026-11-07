from math import comb
import numpy as np


def weighted_polynomial(data, radius, rate, speed, gradient, power):
    local = data['local']
    length = data['node_right']-data['node_left']
    left_offset, source_offset = data['node_left']-6, data['source']-6
    radius_offset = radius-6
    primitive_coefficients = [(data['node_left']-data['source'])*sum(left_offset**(power-index)*source_offset**index
        for index in range(power+1))/(power+1)]
    primitive_coefficients += [comb(power+1, index)*left_offset**(power+1-index)*length**index/(power+1)
        for index in range(1, power+2)]
    product = [np.zeros_like(rate) for index in range(6)]
    for rate_index in range(3):
        for primitive_index, coefficient in enumerate(primitive_coefficients):
            product[rate_index+primitive_index] += data['rate'][:, rate_index]*coefficient
    derivative = sum(product[index]*((2.**(2-index)-1)+2*(2-2.**(2-index))*local) for index in range(1, 6))/data['width']
    interpolation_defect = local*(local-.5)*(local-1)*(product[3]+product[4]*(local+1.5)
        +product[5]*(local**2+1.5*local+1.75))
    mapped_offset = left_offset+local*length
    separation = (radius-data['node_left'])-local*length
    coordinate_defect = separation*sum(radius_offset**(power-index)*mapped_offset**index for index in range(power+1))/(power+1)
    integral = (radius-data['source'])*sum(radius_offset**(power-index)*source_offset**index for index in range(power+1))/(power+1)
    factor = rate*coordinate_defect+interpolation_defect-speed*gradient*integral
    return integral, derivative, factor
