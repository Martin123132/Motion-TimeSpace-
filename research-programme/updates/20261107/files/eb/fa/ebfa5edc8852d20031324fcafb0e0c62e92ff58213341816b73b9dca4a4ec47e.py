from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_P2_indexed_live_geometry_20260919 import IndexedP2Material, IndexedP2Density
from annular_live_P2_canonical_v2_20260918 import material_weight
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from annular_common_weighted_moments_20260920 import apply_rational_rows
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_nonuniform_Gram_candidate_20260920 import template_rows
from decimal import localcontext
from fractions import Fraction
from copy import copy
from time import perf_counter
from scipy.sparse import csr_matrix
import numpy as np


def radial_rhs(radius, mass, log_lapse, temporal_square, gradient_square, gram, source_density, velocity,
        coupling, source_mass, jacobian=False):
    metric = 1-2*mass/radius
    lapse = np.exp(log_lapse)
    clock_square = lapse**2-velocity**2/metric
    if min(np.min(metric.real), np.min(clock_square.real)) <= 0:
        raise ValueError('Outside untrapped/timelike polar chart.')
    root, clock = np.sqrt(metric), np.sqrt(clock_square)
    density = temporal_square/(2*lapse**2*metric)+gradient_square/2+gram
    dust_mass = coupling*source_mass*source_density*root*lapse/clock
    dust_lapse = coupling*source_mass*source_density*velocity**2/(radius*lapse*root**3*clock)
    mass_rhs = coupling*radius**2*metric*density+dust_mass
    lapse_rhs = mass/(radius**2*metric)+coupling*radius*density+dust_lapse
    result = np.stack([mass_rhs, lapse_rhs])
    if not jacobian:
        return result
    density_mass = temporal_square/(lapse**2*radius*metric**2)
    density_lapse = -temporal_square/(lapse**2*metric)
    clock_ratio = velocity**2/(radius*metric**2*clock_square)
    mass_mass = coupling*radius**2*(metric*density_mass-2*density/radius)
    mass_mass += dust_mass*(-1/(radius*metric)+clock_ratio)
    mass_lapse = coupling*radius**2*metric*density_lapse+dust_mass*(1-lapse**2/clock_square)
    lapse_mass = 1/(radius**2*metric)+2*mass/(radius**3*metric**2)+coupling*radius*density_mass
    lapse_mass += dust_lapse*(3/(radius*metric)+clock_ratio)
    lapse_lapse = coupling*radius*density_lapse+dust_lapse*(-1-lapse**2/clock_square)
    return result, np.array([[mass_mass, mass_lapse], [lapse_mass, lapse_lapse]])


class CandidateLoads:
    def __init__(self, owner, coordinates, rates, mesh_packet, action_packets):
        self.owner, self.coordinates, self.rates = owner, coordinates, rates
        self.deadline = perf_counter()+8100
        self.material = IndexedP2Material(owner, coordinates)
        self.knots = np.array([float(value) for value in map(Fraction, mesh_packet['overlay']['nodes'])])
        with localcontext() as context:
            context.prec = 64
            common = apply_rational_rows(mesh_packet['embeddings'][0], decimal_array(coordinates[:, :-1].T))
            self.factor_vertices = {}
            for extension, packet in action_packets.items():
                factor = MixedMap(packet['gram_factor']['rows'], packet['gram_factor']['columns'])
                self.factor_vertices[extension] = np.asarray(factor.apply(common).T, dtype=float)
        self.sampling = template_rows(len(self.knots))[1].tocsc()
        self.factor_coefficients = {name:owner.layer_rule.inverse @ values for name, values in self.factor_vertices.items()}

    def node_load(self, labels, index, extension):
        if extension == 'reference':
            return np.zeros_like(labels)
        start, end = self.sampling.indptr[index:index+2]
        factors = self.sampling.indices[start:end]
        weights = self.sampling.data[start:end]
        images = np.polynomial.chebyshev.chebval(2*labels, self.factor_coefficients[extension][:, factors])
        return np.sum(weights[:, None]*images**2, axis=0)/2

    def gram_density(self, radius, extension, omit_spatial_jacobian=False, omit_label_jacobian=False):
        answer = np.zeros_like(radius)
        if extension == 'reference':
            return answer
        for index, reference in enumerate(self.knots):
            lower, upper = self.material.node_geometry(reference, np.array([-.5, .5]))[0]
            selected = (radius >= lower) & (radius <= upper)
            if not np.any(selected):
                continue
            labels = self.material.inverse_node(radius[selected], reference)
            unused, spatial, label = self.material.node_geometry(reference, labels)
            measure = material_weight(labels)
            if not omit_spatial_jacobian:
                measure = measure/spatial
            if not omit_label_jacobian:
                measure = measure/label
            answer[selected] += measure*self.node_load(labels, index, extension)
        return answer

    def edges(self):
        references = np.unique(np.concatenate([self.owner.model.edges, self.knots]))
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

    def sample(self, radius, label_order, extensions, chunk_size=128):
        radius = np.asarray(radius).ravel()
        owner = copy(self.owner)
        owner.model = copy(self.owner.model)
        owner.model.sampling = csr_matrix((0, self.owner.model.count))
        owner.label_order = label_order
        material = IndexedP2Material(owner, self.coordinates)
        fields = {name:np.zeros_like(radius) for name in ['temporal_square', 'gradient_square', 'source_density', 'velocity']}
        for start in range(0, len(radius), chunk_size):
            if perf_counter() > self.deadline:
                raise RuntimeError('Safe density preparation wall boundary; saved outputs retained.')
            section = slice(start, start+chunk_size)
            density = IndexedP2Density(material, radius[section])
            density.update(self.rates)
            for name in fields:
                fields[name][section] = getattr(density, name)
        fields['gram'] = {extension:self.gram_density(radius, extension) for extension in extensions}
        return fields


class CandidateRadialSolve:
    def __init__(self, loads, degree, label_order, extensions):
        self.loads, self.owner = loads, loads.owner
        self.rule = ChebyshevRule(degree)
        self.edges = loads.edges()
        self.lengths, self.centers = np.diff(self.edges), (self.edges[:-1]+self.edges[1:])/2
        self.nodes = self.centers[:, None]+self.lengths[:, None]*self.rule.points/2
        self.fields = loads.sample(self.nodes.ravel(), label_order, extensions)
        self.label_order = label_order

    def integrated(self, values):
        partial = values.reshape(self.nodes.shape) @ self.rule.integration.T*self.lengths[:, None]/2
        return partial+np.r_[0., np.cumsum(partial[:-1, -1])][:, None]

    def rhs(self, state, extension, jacobian=False):
        return radial_rhs(self.nodes.ravel(), state[0].ravel(), state[1].ravel(),
            self.fields['temporal_square'], self.fields['gradient_square'], self.fields['gram'][extension],
            self.fields['source_density'], self.fields['velocity'], self.owner.coupling, self.owner.source_mass, jacobian)

    def residual(self, state, extension):
        rhs = self.rhs(state, extension)
        mass_integral, lapse_integral = [self.integrated(values) for values in rhs]
        outer = .5*np.log(1-2*state[0, -1, -1]/self.edges[-1])
        return np.stack([state[0]-self.owner.central_mass-mass_integral,
            state[1]-outer-lapse_integral+lapse_integral[-1, -1]])

    def jacobian_product(self, state, direction, extension):
        unused, local = self.rhs(state, extension, True)
        tangent = np.einsum('abn,bn->an', local, direction.reshape(2, -1))
        mass_integral, lapse_integral = [self.integrated(values) for values in tangent]
        outer_metric = 1-2*state[0, -1, -1]/self.edges[-1]
        outer = direction[0, -1, -1]/(self.edges[-1]*outer_metric)
        return np.stack([direction[0]-mass_integral,
            direction[1]+outer-lapse_integral+lapse_integral[-1, -1]])

    def solve(self, extension, tolerance=4e-14):
        mass = np.full_like(self.nodes, self.owner.central_mass)
        lapse = .5*np.log(1-2*mass/self.nodes)
        history = []
        for iteration in range(80):
            rhs = self.rhs(np.stack([mass, lapse]), extension)
            updated = self.owner.central_mass+self.integrated(rhs[0])
            primitive = self.integrated(rhs[1])
            normalized = .5*np.log(1-2*updated[-1, -1]/self.edges[-1])+primitive-primitive[-1, -1]
            error = max(np.max(abs(updated-mass)), np.max(abs(normalized-lapse)))
            history.append(float(error))
            mass, lapse = updated, normalized
            if error < tolerance:
                break
        else:
            raise RuntimeError('Candidate radial iteration failed to converge.')
        state = np.stack([mass, lapse])
        rhs = self.rhs(state, extension).reshape(2, *self.nodes.shape)
        coefficients = rhs @ self.rule.inverse.T
        primitives = np.stack([np.polynomial.chebyshev.chebint(values.T).T*self.lengths[:, None]/2 for values in coefficients])
        for component in range(2):
            primitives[component, :, 0] -= np.polynomial.chebyshev.chebval(-1., primitives[component].T)
        increments = np.array([np.polynomial.chebyshev.chebval(1., values.T) for values in primitives])
        left = np.c_[self.owner.central_mass+np.r_[0., np.cumsum(increments[0, :-1])],
            .5*np.log(1-2*(self.owner.central_mass+sum(increments[0]))/self.edges[-1])
            -sum(increments[1])+np.r_[0., np.cumsum(increments[1, :-1])]].T
        return dict(state=state, rhs_coefficients=coefficients, primitives=primitives,
            left=left, history=history, maximum_residual=float(np.max(abs(self.residual(state, extension)))))

    def values(self, solution, radius):
        radius = np.asarray(radius)
        indices = np.clip(np.searchsorted(self.edges, radius.real, side='right')-1, 0, len(self.lengths)-1)
        coordinate = 2*(radius-self.centers[indices])/self.lengths[indices]
        values, derivatives = [], []
        for component in range(2):
            values.append(solution['left'][component, indices]+np.polynomial.chebyshev.chebval(
                coordinate, solution['primitives'][component, indices].T, tensor=False))
            derivatives.append(np.polynomial.chebyshev.chebval(
                coordinate, solution['rhs_coefficients'][component, indices].T, tensor=False))
        return np.array(values), np.array(derivatives)
