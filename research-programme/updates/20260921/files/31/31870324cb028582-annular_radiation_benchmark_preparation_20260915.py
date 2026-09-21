import numpy as np


def source_initial(mass=.7, source=.03, position=6.03, velocity=.03):
    metric = 1-2*mass/position
    metric_gradient = 2*mass/position**2
    clock = np.sqrt(metric-velocity**2/metric)
    momentum = source*velocity/(metric*clock)
    force = .5*position**2*metric*(1-velocity**2/metric**2)*(.012**2-.006**2)
    acceleration = -metric*metric_gradient/2+3*metric_gradient*velocity**2/(2*metric)+clock**3/source*force
    curvature_ratio = -(metric*(metric_gradient+2*metric/position)+acceleration)/(metric**2-velocity**2)
    return dict(position=position, velocity=velocity, momentum=momentum, clock=clock,
                acceleration=acceleration, curvature_ratio=curvature_ratio, force=force)


def initial_profile(radius, side=None, mass=.7):
    initial = source_initial(mass)
    offset = np.asarray(radius)-initial['position']
    left = offset < 0 if side is None else np.broadcast_to(side == 0, offset.shape)
    slope = np.where(left, .012, .006)
    curvature = slope*initial['curvature_ratio']
    width = .55
    inside = abs(offset) < width
    envelope, envelope_gradient = np.zeros_like(offset), np.zeros_like(offset)
    denominator = width**2-offset[inside]**2
    envelope[inside] = np.exp(-offset[inside]**2/denominator)
    envelope_gradient[inside] = envelope[inside]*(-2*offset[inside]*width**2/denominator**2)
    polynomial = slope*offset+curvature*offset**2/2
    scalar = polynomial*envelope
    gradient = (slope+curvature*offset)*envelope+polynomial*envelope_gradient
    temporal = -initial['velocity']*gradient
    return scalar, gradient, temporal
