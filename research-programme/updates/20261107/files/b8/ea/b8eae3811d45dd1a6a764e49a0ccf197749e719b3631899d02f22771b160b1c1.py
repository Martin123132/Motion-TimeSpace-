from derive_annular_source_gravity_20260914 import EvidenceRun
from derive_annular_support_map_constraints_20260927 import restore_case, load_owned
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_moving_Legendre_current_20260921 import samples
from annular_directional_coupled_Euler_20260928 import interpolate_nodal
from annular_support_radial_response_20260928 import gravitational_moments
from annular_reacted_support_columns_20260929 import compatibility
from decimal import localcontext
from time import perf_counter
import argparse
import csv
import gc
import hashlib
import json
import numpy as np


def acceleration_channels_aligned(action, loads, directions, acceleration, metric_response, support_factor, order, deadline):
    points, weights = np.polynomial.legendre.leggauss(order)
    points, weights = points / 2, weights / 2
    weights *= 6 * (points + .5) * (.5 - points)
    result = np.zeros(4)
    reference_edges = np.array([float(value) for value in action.edges])
    for label, weight in zip(points, weights):
        if perf_counter() > deadline:
            raise RuntimeError('Safe acceleration sensitivity boundary')
        row = samples(action, label, 12)
        quad, geometry, cardinal = row['quadrature'], row['geometry'], row['cardinal']
        cells, local = quad['cells'], quad['local']
        indices = np.asarray(action.mesh['elements'])[cells]
        widths = np.diff(reference_edges)[cells] * geometry['jacobian']
        interpolate = lambda nodes: interpolate_nodal(nodes, indices, local, widths)[0]
        edge = cardinal @ directions['edge_vertices']
        eta = edge[cells] * (1 - local) + edge[cells + 1] * local
        field_test = interpolate(cardinal @ directions['field_vertices'])
        gradient = row['gradient'] / geometry['jacobian']
        radius, metric = geometry['radius'], geometry['metric']
        alpha = radius**2 / (geometry['lapse'] * np.sqrt(metric))
        temporal_acceleration = interpolate(cardinal @ acceleration[:, :-1])
        temporal_acceleration -= (geometry['displacement'] * (cardinal @ acceleration[:, -1]) + support_factor * eta) * row['gradient'] / geometry['jacobian']
        metric_change = metric_response.values(radius)
        fixed_density = alpha * temporal_acceleration
        metric_density = alpha * row['temporal'] * (metric_change[0] / (radius * metric) - metric_change[1])
        density = fixed_density + metric_density
        measure = quad['measure'] * geometry['jacobian']
        channels = [measure @ (density * (field_test - eta * gradient))]
        node_radius = action.geometry(action.knots, row['source'], label)['radius']
        node_rate = cardinal @ loads.rates[:, :-1]
        for power in range(3):
            integral = ((radius - 6)**(power + 1) - (row['source'] - 6)**(power + 1)) / (power + 1)
            node_integral = ((node_radius - 6)**(power + 1) - (row['source'] - 6)**(power + 1)) / (power + 1)
            weighted = interpolate(node_rate * node_integral)
            difference = row['temporal'] * integral - weighted
            channels.append(measure @ (fixed_density * difference) + measure @ (metric_density * difference))
        result += weight * np.array(channels)
    result[1:] += gravitational_moments(action, metric_response, 32)
    return result
