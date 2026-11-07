from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_Legendre_current_20260921 import samples, wave_data
from annular_candidate_Ward_source_20260921 import fields
from annular_radial_Ward_moments_20260921 import KernelPrimitive
import numpy as np


RATE_TERMS = ['mesh_acceleration', 'field_velocity_slope', 'mesh_stretch', 'primitive_endpoints', 'primitive_metric', 'Euler_moment_rate']


class KernelTimeRate(KernelPrimitive):
    def __init__(self, action, tangent):
        self.tangent = tangent
        super().__init__(action, 24)

    def at(self, radius):
        values, unused = self.action.solver.values(self.action.solution, radius)
        metric = 1-2*values[0]/radius
        nu_rate, metric_rate = self.tangent.at(radius)
        return super().at(radius)*(-2*nu_rate[-1]-metric_rate[-1]/metric)


def endpoint_kinematics(action, acceleration, polynomial, label, reference, cells, local):
    cardinal = np.asarray(action.cardinal(label)).ravel()
    source, velocity, source_acceleration = cardinal@action.source, cardinal@action.velocity, cardinal@acceleration[:, -1]
    radius, jacobian, displacement, jacobian_source = action.mapping(reference, source, label)
    edges = np.array([float(value) for value in action.edges])
    anchored_left = (edges[cells+1]<=action.owner.model.anchor)&(reference==action.owner.model.anchor)
    span = action.owner.model.anchor-action.owner.model.radii[0]
    jacobian[anchored_left] = (source-action.owner.model.radii[0]-action.owner.width*label)/span
    jacobian_source[anchored_left] = 1/span
    widths = np.diff(edges)[cells]
    coefficients = np.einsum('cpl,l->cp', action.gradient, cardinal)[cells]
    slope = (coefficients[:, 0]+coefficients[:, 1]*local)/jacobian
    coefficients = np.einsum('cpl,l->cp', action.rate_polynomial, cardinal)[cells]
    velocity_slope = (coefficients[:, 1]+2*local*coefficients[:, 2])/widths/jacobian
    coefficients = np.einsum('cpl,l->cp', polynomial, cardinal)[cells]
    acceleration_slope = (coefficients[:, 1]+2*local*coefficients[:, 2])/widths/jacobian
    stretching = jacobian_source*velocity/jacobian
    slope_rate = velocity_slope-stretching*slope
    slope_second = acceleration_slope-2*stretching*slope_rate-jacobian_source*source_acceleration/jacobian*slope
    return dict(slope=slope, slope_rate=slope_rate, slope_second=slope_second,
        velocity_slope=velocity_slope, stretch_slope=stretching*slope,
        radius=radius, speed=displacement*velocity, speed_rate=displacement*source_acceleration)


def layer(action, tangent, mode_response, kernel, kernel_rate, acceleration, polynomial, mode, mode_polynomial, label):
    row = samples(action, label, 12)
    quadrature, geometry, cardinal = row['quadrature'], row['geometry'], row['cardinal']
    cells, local, measure = [quadrature[key] for key in ['cells', 'local', 'measure']]
    edges = np.array([float(value) for value in action.edges])
    count = len(edges)-1
    coefficients = np.einsum('cpl,l->cp', polynomial, cardinal)[cells]
    acceleration_value = coefficients[:, 0]+local*(coefficients[:, 1]+local*coefficients[:, 2])
    momentum_rate = wave_data(row, tangent)['momentum_rate'][-1]
    momentum_rate += geometry['kinetic']*(acceleration_value+(acceleration[:, -1]@cardinal)*row['motion'])
    coefficients = np.einsum('cpl,l->cp', mode_polynomial, cardinal)[cells]
    mode_value = coefficients[:, 0]+local*(coefficients[:, 1]+local*coefficients[:, 2])
    metric_change = mode_response.values(geometry['radius'])
    mode_rate = geometry['kinetic']*(mode_value+(mode[:, -1]@cardinal)*row['motion'])
    mode_rate += geometry['kinetic']*row['temporal']*(metric_change[0]/(geometry['radius']*geometry['metric'])-metric_change[1])
    field = fields(action, quadrature['reference'], cells, local, label)
    momentum_rates = np.array([momentum_rate, momentum_rate-mode_rate])
    euler = -momentum_rates-field['flux_x']
    flux = -field['alpha']*field['temporal']*field['speed']-field['beta']*field['gradient']
    moments, weak = np.zeros((2, count, 2)), np.zeros((2, count, 2))
    for endpoint, (shape, derivative) in enumerate([((1-local)*(1-2*local), 4*local-3), (local*(2*local-1), 4*local-1)]):
        for variant in range(2):
            moments[variant, :, endpoint] = np.bincount(cells, weights=measure*euler[variant]*shape, minlength=count)
            weak[variant, :, endpoint] = np.bincount(cells,
                weights=measure*(-momentum_rates[variant]*shape+flux*derivative/np.diff(edges)[cells]), minlength=count)
    indices = np.arange(count)
    left = fields(action, edges[:-1], indices, np.zeros(count), label)
    right = fields(action, edges[1:], indices, np.ones(count), label)
    weak[:, :, 0] += -left['alpha']*left['temporal']*left['speed']-left['beta']*left['gradient']
    weak[:, :, 1] -= -right['alpha']*right['temporal']*right['speed']-right['beta']*right['gradient']
    left_jet = endpoint_kinematics(action, acceleration, polynomial, label, edges[:-1], indices, np.zeros(count))
    right_jet = endpoint_kinematics(action, acceleration, polynomial, label, edges[1:], indices, np.ones(count))
    jump = {key: left_jet[key][1:]-right_jet[key][:-1] for key in ['slope', 'slope_rate', 'slope_second', 'velocity_slope', 'stretch_slope']}
    radius, speed, speed_rate = [left_jet[key][1:] for key in ['radius', 'speed', 'speed_rate']]
    primitive = kernel.anchored(radius, row['source'])
    psi = speed*primitive*jump['slope']
    endpoint_average = speed*primitive*(left_jet['slope'][1:]+right_jet['slope'][:-1])/2
    anchor = edges[1:-1]==action.owner.model.anchor
    difference = moments[:, 1:, 0]-moments[:, :-1, 1]
    weak_difference = weak[:, 1:, 0]-weak[:, :-1, 1]
    pin = np.einsum('tf,vf->vt', endpoint_average[:, anchor], (moments[:, 1:, 0]+moments[:, :-1, 1])[:, anchor])
    trace = np.einsum('tf,vf->vt', psi/2, difference)+pin
    weak_trace = np.einsum('tf,vf->vt', psi/2, weak_difference)
    weak_trace += np.einsum('tf,vf->vt', endpoint_average[:, anchor], (weak[:, 1:, 0]+weak[:, :-1, 1])[:, anchor])
    output = dict(moments=moments, weak_moments=weak, psi=psi, pin=pin, trace=trace, weak_trace=weak_trace,
        jump=jump['slope'], jump_rate=jump['slope_rate'], jump_second=jump['slope_second'],
        kinematic_replay=np.array([np.max(abs(left_jet['slope']-left['gradient'])), np.max(abs(right_jet['slope']-right['gradient']))]),
        continuity=np.array([np.max(abs(left_jet['radius'][1:]-right_jet['radius'][:-1])), np.max(abs(left_jet['speed'][1:]-right_jet['speed'][:-1]))]))
    if kernel_rate is not None:
        moving = kernel.at(radius)*speed-kernel.at(np.array([row['source']]))*row['velocity']
        metric = kernel_rate.anchored(radius, row['source'])
        output['psi_rate_terms'] = np.array([speed_rate*primitive*jump['slope'], speed*primitive*jump['velocity_slope'],
            -speed*primitive*jump['stretch_slope'], speed*jump['slope']*moving, speed*jump['slope']*metric])
        output['anchor_primitive_rate'] = (moving+metric)[:, anchor]
    return output
