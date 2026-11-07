from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_moving_Legendre_current_20260921 import samples, wave_data
from annular_candidate_Ward_source_20260921 import fields
from annular_candidate_coordinate_covectors_20260921 import local_polynomials
from annular_decimal_transport_v2_20260919 import decimal_array
from decimal import localcontext
import numpy as np


CHANNELS = ['smooth_cell', 'trace_lift', 'material_cell', 'material_face', 'projected_cell', 'projected_face',
            'gram_work', 'boundary_work', 'raw_transport', 'raw_face', 'anchor_face', 'mode_metric_work', 'mode_mass_work']
TERMS = ['smooth_cell', 'trace_lift', 'material_cell', 'material_face', 'gram_work', 'negative_boundary',
         'full_Euler_work', 'mode_reaction', 'material_quadrature', 'weak_assembly_defect']


def traces(action, kernel, label):
    cardinal = np.asarray(action.cardinal(label)).ravel()
    source = cardinal@action.source
    edges = np.array([float(value) for value in action.edges])
    cells = np.arange(len(edges)-1)
    left = fields(action, edges[:-1], cells, np.zeros(len(cells)), label)
    middle = fields(action, (edges[:-1]+edges[1:])/2, cells, np.full(len(cells), .5), label)
    right = fields(action, edges[1:], cells, np.ones(len(cells)), label)
    own = np.stack([value['speed']*value['gradient']*kernel.anchored(value['radius'], source)
                    for value in [left, middle, right]], axis=-1)
    continuous = own.copy()
    average = (own[:, :-1, 2]+own[:, 1:, 0])/2
    continuous[:, :-1, 2] = average
    continuous[:, 1:, 0] = average
    elements = np.array(action.mesh['elements'])
    continuous[:, elements<0] = 0.
    speed = (right['speed'][:-1]+left['speed'][1:])/2
    jump = left['gradient'][1:]-right['gradient'][:-1]
    face_euler = (left['beta'][1:]-left['alpha'][1:]*speed**2)*jump
    anchor = edges[1:-1]==action.owner.model.anchor
    return dict(own=own, continuous=continuous, average=average, face_euler=face_euler,
                left=left, right=right, source=source, cardinal=cardinal, anchor=anchor)


def generator(action, loads, kernel):
    labels = action.owner.layer_rule.points/2
    count = len(action.knots)
    vertices = np.zeros((3, len(labels), count))
    elements = np.array(action.mesh['elements'])
    selected = elements>=0
    for index, label in enumerate(labels):
        trace = traces(action, kernel, label)
        vertices[:, index, elements[selected]] = trace['continuous'][:, selected]
    with localcontext() as context:
        context.prec = 64
        nodal = decimal_array(vertices.transpose(2, 0, 1).reshape(count, -1))
        polynomial, unused = local_polynomials(action.mesh, nodal)
        image = np.asarray(loads.factor.apply(nodal), float)
    polynomial = polynomial.reshape(len(elements), 3, 3, len(labels))
    image = image.reshape(loads.factor.shape[0], 3, len(labels))
    cardinal = np.array([np.asarray(action.cardinal(label)).ravel() for label in labels])
    return vertices, polynomial, image, float(np.max(abs(cardinal-np.eye(len(labels)))))


def evaluate_layer(action, loads, tangent, mode_response, kernel, acceleration, acceleration_polynomial,
                   mode, mode_polynomial, vertices, test_polynomial, test_image, label):
    row = samples(action, label, 12)
    quadrature, geometry, cardinal = row['quadrature'], row['geometry'], row['cardinal']
    cells, local, measure = [quadrature[key] for key in ['cells', 'local', 'measure']]
    field = fields(action, quadrature['reference'], cells, local, label)
    coefficients = np.einsum('cpl,l->cp', acceleration_polynomial, cardinal)[cells]
    field_acceleration = coefficients[:, 0]+local*(coefficients[:, 1]+local*coefficients[:, 2])
    source_acceleration = acceleration[:, -1]@cardinal
    momentum_rate = wave_data(row, tangent)['momentum_rate'][-1]
    momentum_rate += geometry['kinetic']*(field_acceleration+source_acceleration*row['motion'])
    full_euler = -momentum_rate-field['flux_x']
    coefficients = np.einsum('cpl,l->cp', mode_polynomial, cardinal)[cells]
    mode_field = coefficients[:, 0]+local*(coefficients[:, 1]+local*coefficients[:, 2])
    mode_source = mode[:, -1]@cardinal
    metric_change = mode_response.values(geometry['radius'])
    mode_metric = geometry['kinetic']*row['temporal']*(metric_change[0]/(geometry['radius']*geometry['metric'])-metric_change[1])
    mode_mass = geometry['kinetic']*(mode_field+mode_source*row['motion'])
    euler = np.array([full_euler, full_euler+mode_mass+mode_metric])
    trace = traces(action, kernel, label)
    shape = np.array([(1-local)*(1-2*local), 4*local*(1-local), local*(2*local-1)])
    own = np.sum(trace['own'][:, cells, :]*shape.T, axis=-1)
    continuous = np.sum(trace['continuous'][:, cells, :]*shape.T, axis=-1)
    primitive = kernel.anchored(geometry['radius'], row['source'])
    actual = field['speed']*field['gradient']*primitive
    coefficients = np.einsum('cptl,l->tcp', test_polynomial, cardinal)
    selected = coefficients[:, cells]
    projected = selected[:, :, 0]+local*(selected[:, :, 1]+local*selected[:, :, 2])
    projected_nodes = np.einsum('tln,l->tn', vertices, cardinal)
    elements = np.array(action.mesh['elements'])
    face_indices = elements[:-1, 2]
    projected_faces = projected_nodes[:, np.maximum(face_indices, 0)]*(face_indices>=0)
    face = trace['face_euler']
    face_projected = np.sum(face*projected_faces, axis=1)
    raw_face = np.sum(face*trace['average'], axis=1)
    material_face = np.sum(face*(trace['average']-projected_faces), axis=1)
    anchor_face = np.sum(face[trace['anchor']]*trace['average'][:, trace['anchor']], axis=1)
    boundary = np.zeros(3)
    for sign, edge, local_index, node_index in [(-1, trace['left'], 0, elements[0, 0]),
                                               (1, trace['right'], -1, elements[-1, 2])]:
        force = -edge['alpha'][local_index]*edge['temporal'][local_index]*edge['speed'][local_index]-edge['beta'][local_index]*edge['gradient'][local_index]
        if node_index>=0:
            boundary += sign*force*projected_nodes[:, node_index]
    nodal = action.geometry(action.knots, row['source'], label)
    image = action.factor_values@cardinal
    projected_image = np.einsum('atl,l->at', test_image, cardinal)
    gram = np.sum((image*(action.sampling@nodal['gradient']))[:, None]*projected_image, axis=0)
    values = np.zeros((2, len(CHANNELS), 3))
    for index, factor in [(0, actual-own), (1, own-continuous), (2, continuous-projected), (4, projected), (8, actual)]:
        values[:, index] = np.einsum('aq,tq,q->at', euler, factor, measure)
    for index, value in [(3, material_face), (5, face_projected), (6, gram), (7, boundary), (9, raw_face), (10, anchor_face),
                         (11, np.sum(measure*mode_metric*projected, axis=1)), (12, np.sum(measure*mode_mass*projected, axis=1))]:
        values[:, index] = value
    return values


def decomposition(averages48, averages64, full_residual, mode_reaction):
    projected48 = averages48[:, 4]+averages48[:, 5]
    projected64 = averages64[:, 4]+averages64[:, 5]
    reaction = np.array([np.zeros(3), mode_reaction])
    weak_defect = projected48-(full_residual+reaction+averages48[:, 6]-averages48[:, 7])
    terms = np.stack([averages64[:, 0], averages64[:, 1], averages64[:, 2], averages64[:, 3],
        averages48[:, 6], -averages48[:, 7], np.broadcast_to(full_residual, (2, 3)), reaction,
        projected64-projected48, weak_defect], axis=1)
    return terms, weak_defect
