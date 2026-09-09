import math

import numpy as numerical

from annular_curvature_timejet_transfer_20260909 import KEYS, TransferJet, spatial_derivatives
from annular_third_corner_initial_data_20260909 import initial_derivatives


def transform_mixed(mixed, radii, sigma):
    result = {}
    for name, component in [("scalar_ref", 0), ("mass_ref", 1), ("shift_ref", 2)]:
        data = numerical.zeros((len(KEYS), radii.size))
        for position, (direction, time_order, radius_order) in enumerate(KEYS):
            if direction == 0:
                data[position] = sum(math.comb(radius_order, index) * (-sigma)**index * mixed[time_order + index, radius_order - index][component] for index in range(radius_order + 1)) / (math.factorial(time_order) * math.factorial(radius_order))
        result[name] = TransferJet(data)
    return result


def error_fields(time_derivatives, payload, radii, sigma, method):
    if time_derivatives.shape != (4, 5, radii.size):
        raise ValueError("Expected actual current derivatives [order,chi,w,h,mu,delta] through third time order")
    spacing = float(radii[1] - radii[0])
    initial = initial_derivatives(payload, radii, maximum=3)[:, 0][:, [0, 2, 3]]
    mixed = {}
    for time_order in range(4):
        values = time_derivatives[time_order, [0, 3, 4]].copy()
        if time_order == 0:
            values -= initial[0]
        for radius_order, differentiated in enumerate(spatial_derivatives(values, spacing, 3 - time_order, method)):
            mixed[time_order, radius_order] = differentiated + (initial[radius_order] if time_order == 0 else 0)
    return transform_mixed(mixed, radii, sigma), mixed
