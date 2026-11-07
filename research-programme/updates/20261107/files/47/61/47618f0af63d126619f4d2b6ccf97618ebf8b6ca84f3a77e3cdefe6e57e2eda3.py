import numpy as np


def compatible_initial_state(system, time):
    if time != 0:
        raise ValueError('This helper prepares initial data, not an exact evolving history.')
    position, velocity = 6.03, .03
    offset = system.radii-position
    distance = abs(offset)
    envelope = np.ones(system.count)
    envelope_gradient = np.zeros(system.count)
    outside = distance >= .55
    transition = (distance > .2) & (~outside)
    fraction = (distance[transition]-.2)/.35
    envelope[transition] = 1-10*fraction**3+15*fraction**4-6*fraction**5
    envelope_gradient[transition] = (-30*fraction**2+60*fraction**3-30*fraction**4)*np.sign(offset[transition])/.35
    envelope[outside] = 0.
    scalar = .01*offset*envelope
    gradient = .01*(envelope+offset*envelope_gradient)
    rates = -.01*velocity*(envelope+offset*envelope_gradient)
    return np.append(scalar, position), np.append(rates, velocity), np.zeros(system.count+1)
