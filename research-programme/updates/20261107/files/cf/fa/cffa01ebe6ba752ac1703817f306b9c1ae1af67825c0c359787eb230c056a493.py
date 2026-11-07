from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_P2_overlay_20260919 import evaluation_rows, serialize_mesh, serialize_rows
from annular_common_frozen_candidate_20260920 import gram_rows
from annular_common_weighted_moments_20260920 import apply_rational_rows
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_nonuniform_Gram_candidate_20260920 import template_rows
from annular_candidate_midpoint_20260921 import CommonLoads, CommonCoordinateAction
from annular_candidate_radial_constraint_20260920 import CandidateRadialSolve
from annular_candidate_energy_current_20260921 import reconstructed_solver
from annular_candidate_hamiltonian_20260921 import decimals
from annular_decimal_transport_v2_20260919 import decimal_array
from copy import copy
from decimal import Decimal, localcontext
from fractions import Fraction
from scipy.sparse import csr_matrix, coo_matrix, block_diag, kron, eye
import numpy as np


def rational_mesh(packet):
    return dict(packet, edges=list(map(Fraction, packet['edges'])), nodes=list(map(Fraction, packet['nodes'])),
                anchor=Fraction(packet['anchor']))


def bisected_mesh(packet):
    coarse = rational_mesh(packet)
    edges = sorted(coarse['edges']+[(lower+upper)/2 for lower, upper in zip(coarse['edges'][:-1], coarse['edges'][1:])])
    nodes = sorted([point for point in edges if point != coarse['anchor']]
                   +[(lower+upper)/2 for lower, upper in zip(edges[:-1], edges[1:])])
    lookup = {value: index for index, value in enumerate(nodes)}
    elements = [[lookup.get(lower, -1), lookup[(lower+upper)/2], lookup.get(upper, -1)]
                for lower, upper in zip(edges[:-1], edges[1:])]
    fine = dict(edges=edges, nodes=nodes, elements=elements, count=len(nodes), anchor=coarse['anchor'])
    prolongation = evaluation_rows(coarse, nodes)
    restriction = [lookup[value] for value in coarse['nodes']]
    return serialize_mesh(fine), serialize_rows(prolongation), restriction


def sparse_sampling(packet):
    rows, columns, values = [], [], []
    for index, row in enumerate(packet['gram_sampling']):
        for column, value in row.items():
            rows.append(index)
            columns.append(int(column))
            values.append(float(value))
    return coo_matrix((values, (rows, columns)), shape=(len(packet['gram_sampling']), packet['count'])).tocsr()


def refined_packet(coarse_mesh, fine_mesh, restriction, extension):
    count = fine_mesh['count']
    if extension == 'reference':
        return dict(count=count, extension=extension, gram_factor=dict(rows=[], columns=count), gram_sampling=[],
                    gram_support=coarse_mesh['nodes'], fixed_interaction_support=True)
    with localcontext() as context:
        context.prec = 64
        rows, sampling = gram_rows(fine_mesh, list(map(Fraction, coarse_mesh['nodes'])), extension == 'alternative')
        serial = MixedMap(rows, count).serialize()
    sampling = sampling.tocsr()
    sampled = [{str(restriction[int(sampling.indices[pointer])]): repr(float(sampling.data[pointer]))
                for pointer in range(sampling.indptr[index], sampling.indptr[index+1])}
               for index in range(sampling.shape[0])]
    return dict(count=count, extension=extension, gram_factor=serial, gram_sampling=sampled,
                gram_support=coarse_mesh['nodes'], fixed_interaction_support=True)


def adapt_owner(base, mesh):
    owner, model = copy(base), copy(base.model)
    model.edges = np.array([float(Fraction(value)) for value in mesh['edges']])
    model.radii = np.array([float(Fraction(value)) for value in mesh['nodes']])
    model.element_indices = np.array(mesh['elements'])
    model.count = mesh['count']
    model.sampling = csr_matrix((0, mesh['count']))
    owner.model, owner.count = model, mesh['count']
    return owner


def prolong_state(state, prolongation):
    with localcontext() as context:
        context.prec = 64
        position = apply_rational_rows(prolongation, decimals(state['coordinates'][:, :-1]).T).T
        rate = apply_rational_rows(prolongation, decimal_array(state['rates'][:, :-1].T)).T
        coordinates = np.column_stack([position, decimals(state['coordinates'])[:, -1]])
        rates = np.column_stack([np.asarray(rate, float), state['rates'][:, -1]])
    return coordinates, rates


def all_prolongation(rows, coarse_count, labels):
    first, last, values = [], [], []
    for index, row in enumerate(rows):
        for column, value in row.items():
            first.append(index)
            last.append(int(column))
            values.append(float(Fraction(value)))
    field = coo_matrix((values, (first, last)), shape=(len(rows), coarse_count)).tocsr()
    return kron(eye(labels, format='csr'), block_diag((field, csr_matrix([[1.]])), format='csr'), format='csr')


class RefinedLoads(CommonLoads):
    def __init__(self, owner, coordinates, rates, mesh, packet, extension, deadline):
        super().__init__(owner, coordinates, rates, mesh, packet, extension, 64, deadline)
        self.sampling = sparse_sampling(packet).tocsc()


    def edges(self):
        active = np.asarray(abs(self.sampling).sum(axis=0)).ravel() > 0
        references = np.unique(np.r_[self.owner.model.edges, self.knots[active]])
        raw = np.sort(np.concatenate([self.material.node_geometry(references, label)[0] for label in [-.5, .5]]))
        tolerance = 32*np.finfo(float).eps*max(1., max(abs(raw)))
        clusters = [[raw[0]]]
        for value in raw[1:]:
            if value-clusters[-1][0] <= tolerance:
                clusters[-1].append(value)
            else:
                clusters.append([value])
        self.edge_merge_spread = max(max(cluster)-min(cluster) for cluster in clusters)
        return np.array([np.mean(cluster) for cluster in clusters])


def live_refined(owner, coordinates, rates, mesh, packet, extension, deadline):
    loads = RefinedLoads(owner, coordinates, rates, mesh, packet, extension, deadline)
    solver = CandidateRadialSolve(loads, 22, 28, [extension])
    solution = solver.solve(extension)
    action = CommonCoordinateAction(owner, coordinates, rates, mesh, loads, solver, solution, 64)
    return loads, action


def restore_refined(owner, state, mesh, packet, extension, deadline):
    coordinates = decimals(state['coordinates'])
    loads = RefinedLoads(owner, coordinates, state['rates'], mesh, packet, extension, deadline)
    solver, solution = reconstructed_solver(state)
    action = CommonCoordinateAction(owner, coordinates, state['rates'], mesh, loads, solver, solution, 64)
    return loads, action
