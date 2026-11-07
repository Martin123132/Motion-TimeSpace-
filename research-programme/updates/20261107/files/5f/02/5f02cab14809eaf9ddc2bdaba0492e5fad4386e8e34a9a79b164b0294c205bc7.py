from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_common_weighted_moments_20260920 import apply_rational_rows, decimal_fraction
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_nonuniform_Gram_candidate_20260920 import template_rows
from decimal import Decimal, localcontext
from fractions import Fraction
from bisect import bisect_right
from time import perf_counter
from scipy.sparse import csr_matrix
import numpy as np


ZERO = Decimal(0)


def local_polynomials(mesh, values):
    coefficients = np.full((len(mesh['elements']), 3, values.shape[1]), ZERO, dtype=object)
    widths = []
    for cell, indices in enumerate(mesh['elements']):
        left, middle, right = [values[index] if index >= 0 else np.full(values.shape[1], ZERO)
            for index in indices]
        coefficients[cell] = np.array([left, -3*left+4*middle-right, 2*left-4*middle+2*right])
        widths.append(decimal_fraction(Fraction(mesh['edges'][cell+1])-Fraction(mesh['edges'][cell])))
    gradient = coefficients[:, 1:]*np.array([1, 2], dtype=object)[None, :, None]/np.array(widths)[:, None, None]
    return np.asarray(coefficients, dtype=float), np.asarray(gradient, dtype=float)


def scaled_error(first, second, floor=1e-30):
    if first.size == 0 and second.size == 0:
        return 0.
    return float(np.max(abs(first-second))/max(float(np.max(abs(first))), float(np.max(abs(second))), floor))


class CoordinateAction:
    def __init__(self, owner, saved, packet, action_packet, solver, solution, directions, precision=64):
        self.owner, self.mesh, self.solver, self.solution = owner, packet['overlay'], solver, solution
        self.edges = list(map(Fraction, self.mesh['edges']))
        self.knots = np.array([float(Fraction(value)) for value in self.mesh['nodes']])
        self.sampling = template_rows(len(self.knots))[1].tocsr()
        self.factor = MixedMap(action_packet['gram_factor']['rows'], action_packet['gram_factor']['columns'])
        if self.factor.shape[0] == 0:
            self.sampling = csr_matrix((0, len(self.knots)))
        self.source = saved['coordinates'][:, -1].copy()
        self.velocity = saved['fixed_rates'][:, -1].copy()
        self.precision = precision
        with localcontext() as context:
            context.prec = precision
            self.exact_fields = apply_rational_rows(packet['embeddings'][0], decimal_array(saved['coordinates'][:, :-1].T))
            self.exact_rates = apply_rational_rows(packet['embeddings'][0], decimal_array(saved['fixed_rates'][:, :-1].T))
            self.polynomial, self.gradient = local_polynomials(self.mesh, self.exact_fields)
            self.rate_polynomial, unused = local_polynomials(self.mesh, self.exact_rates)
            self.factor_vertices = self.factor.apply(self.exact_fields)
            self.directions = [decimal_array(direction.T) for direction in directions]
            self.directions.append(np.vstack([self.exact_fields, np.full((1, len(self.source)), ZERO)]))
            self.direction_gradients = [local_polynomials(self.mesh, direction[:-1])[1] for direction in self.directions]
            self.direction_factors = [self.factor.apply(direction[:-1]) for direction in self.directions]
        self.factor_values = np.asarray(self.factor_vertices, dtype=float)
        self.direction_factor_values = [np.asarray(values, dtype=float) for values in self.direction_factors]
        self.direction_sources = np.array([direction[-1] for direction in self.directions], dtype=float)

    def cardinal(self, label):
        return np.polynomial.chebyshev.chebvander(2*label, self.owner.layer_degree) @ self.owner.layer_rule.inverse

    def mapping(self, reference, source, label):
        radius, jacobian, displacement = self.owner.model.mapping(reference, source-self.owner.width*label)
        derivative = np.where(reference < self.owner.model.anchor,
            1/(self.owner.model.anchor-self.owner.model.radii[0]),
            -1/(self.owner.model.radii[-1]-self.owner.model.anchor))
        return radius+self.owner.width*label, jacobian, displacement, derivative

    def quadrature(self, label, source, order):
        model = self.owner.model
        inner, outer = model.radii[[0, -1]]+self.owner.width*label
        selected = self.solver.edges[(self.solver.edges > inner) & (self.solver.edges < outer)]
        jacobian = np.where(selected < source, (source-inner)/(model.anchor-model.radii[0]),
            (outer-source)/(model.radii[-1]-model.anchor))
        pulled = np.where(selected < source, model.radii[0]+(selected-inner)/jacobian,
            model.radii[-1]-(outer-selected)/jacobian)
        cuts = sorted(set(self.edges+list(map(Fraction.from_float, pulled))))
        cuts = [value for value in cuts if self.edges[0] <= value <= self.edges[-1]]
        cells, offsets, spans, lengths = [], [], [], []
        for lower, upper in zip(cuts, cuts[1:]):
            cell = bisect_right(self.edges, (lower+upper)/2)-1
            width = self.edges[cell+1]-self.edges[cell]
            cells.append(cell)
            offsets.append(float((lower-self.edges[cell])/width))
            spans.append(float((upper-lower)/width))
            lengths.append(float(upper-lower))
        points, weights = np.polynomial.legendre.leggauss(order)
        local = (np.array(offsets)[:, None]+np.array(spans)[:, None]*(points+1)/2).ravel()
        measure = (np.array(lengths)[:, None]*weights/2).ravel()
        cells = np.repeat(np.array(cells), order)
        widths = np.array([float(last-first) for first, last in zip(self.edges, self.edges[1:])])[cells]
        reference = np.array([float(value) for value in self.edges[:-1]])[cells]+widths*local
        indices = np.array(self.mesh['elements'])[cells]
        radial = np.column_stack([4*local-3, 4-8*local, 4*local-1])/widths[:, None]
        radial *= indices >= 0
        return dict(cells=cells, local=local, reference=reference, measure=measure,
            indices=np.maximum(indices, 0), radial=radial)

    def geometry(self, reference, source, label):
        radius, jacobian, displacement, jacobian_source = self.mapping(reference, source, label)
        values, derivatives = self.solver.values(self.solution, radius)
        mass, log_lapse = values
        mass_radial, lapse_log_radial = derivatives
        metric = 1-2*mass/radius
        metric_radial = -2*mass_radial/radius+2*mass/radius**2
        lapse, root = np.exp(log_lapse), np.sqrt(metric)
        kinetic = jacobian*radius**2/(lapse*root)
        gradient = radius**2*lapse*root/jacobian
        kinetic_source = kinetic*(jacobian_source/jacobian+
            displacement*(2/radius-lapse_log_radial-metric_radial/(2*metric)))
        gradient_source = gradient*(displacement*(2/radius+lapse_log_radial+metric_radial/(2*metric))-
            jacobian_source/jacobian)
        return dict(radius=radius, jacobian=jacobian, displacement=displacement, jacobian_source=jacobian_source,
            metric=metric, lapse=lapse, kinetic=kinetic, gradient=gradient,
            kinetic_source=kinetic_source, gradient_source=gradient_source,
            metric_radial=metric_radial, lapse_log_radial=lapse_log_radial)

    def dust(self, source, velocity):
        values, derivatives = self.solver.values(self.solution, np.array([source]))
        mass, log_lapse = values[:, 0]
        mass_radial, lapse_log_radial = derivatives[:, 0]
        metric, lapse = 1-2*mass/source, np.exp(log_lapse)
        metric_radial = -2*mass_radial/source+2*mass/source**2
        clock = np.sqrt(lapse**2-velocity**2/metric)
        action = -self.owner.source_mass*clock
        force = -self.owner.source_mass*(lapse**2*lapse_log_radial+velocity**2*metric_radial/(2*metric**2))/clock
        return action, force, float(np.real(metric)), float(np.real(abs(velocity)/(lapse*np.sqrt(metric))))

    def evaluate(self, reference_order, material_order, deadline):
        count, labels = len(self.knots), len(self.source)
        bulk, dust = [np.zeros((count+1, labels)) for unused in range(2)]
        gram_source = np.zeros(labels)
        moments = np.full((self.factor.shape[0], labels), ZERO, dtype=object)
        derivatives = {name:np.zeros(len(self.directions)) for name in ['bulk', 'gram', 'dust']}
        actions = dict(bulk=0., gram=0., dust=0.)
        wrong_source = np.zeros(labels)
        points, weights = np.polynomial.legendre.leggauss(material_order)
        points, weights = points/2, weights/2
        weights *= 6*(points+.5)*(.5-points)
        minimum_metric, maximum_speed, sample_count = 1., 0., 0
        for label, material_weight in zip(points, weights):
            if perf_counter() > deadline:
                raise RuntimeError('Safe wall boundary: retain completed force evidence.')
            cardinal = np.asarray(self.cardinal(label)).ravel()
            source, velocity = cardinal @ self.source, cardinal @ self.velocity
            quadrature = self.quadrature(label, source, reference_order)
            cells, local, measure = [quadrature[name] for name in ['cells', 'local', 'measure']]
            sample_count += len(local)
            coefficients = np.einsum('cpl,l->cp', self.gradient, cardinal)[cells]
            gradient = coefficients[:, 0]+coefficients[:, 1]*local
            coefficients = np.einsum('cpl,l->cp', self.rate_polynomial, cardinal)[cells]
            rate = coefficients[:, 0]+local*(coefficients[:, 1]+local*coefficients[:, 2])
            geometry = self.geometry(quadrature['reference'], source, label)
            kinetic, spatial, jacobian, displacement, jacobian_source = [geometry[name]
                for name in ['kinetic', 'gradient', 'jacobian', 'displacement', 'jacobian_source']]
            motion = -displacement*gradient/jacobian
            temporal = rate+velocity*motion
            weak = -measure*(kinetic*temporal*velocity*displacement/jacobian+spatial*gradient)
            field = np.zeros(count)
            np.add.at(field, quadrature['indices'].ravel(), (weak[:, None]*quadrature['radial']).ravel())
            source_bulk = measure @ (geometry['kinetic_source']*temporal**2/2-
                kinetic*temporal*velocity*motion*jacobian_source/jacobian-geometry['gradient_source']*gradient**2/2)
            local_bulk = measure @ (kinetic*temporal**2-spatial*gradient**2)/2
            bulk += material_weight*np.outer(np.r_[field, source_bulk], cardinal)
            missing = kinetic*jacobian_source/jacobian
            wrong = measure @ (missing*temporal**2/2-kinetic*temporal*velocity*motion*jacobian_source/jacobian+
                spatial*jacobian_source/jacobian*gradient**2/2)
            wrong_source += material_weight*cardinal*wrong
            nodal_geometry = self.geometry(self.knots, source, label)
            factors = self.factor_values @ cardinal
            sampled = self.sampling @ nodal_geometry['gradient']
            sampled_source = self.sampling @ nodal_geometry['gradient_source']
            local_gram = -sampled @ factors**2/2
            gram_source -= material_weight*cardinal*(sampled_source @ factors**2)/2
            with localcontext() as context:
                context.prec = self.precision
                moments += decimal_array(material_weight*sampled*factors)[:, None]*decimal_array(cardinal)[None, :]
            local_dust, source_dust, dust_metric, speed = self.dust(source, velocity)
            dust[-1] += material_weight*cardinal*source_dust
            minimum_metric = min(minimum_metric, float(np.min(geometry['metric'])), dust_metric)
            maximum_speed = max(maximum_speed, speed)
            for name, value in [('bulk', local_bulk), ('gram', local_gram), ('dust', local_dust)]:
                actions[name] += material_weight*float(value)
            step = 1e-25
            for direction in range(len(self.directions)):
                delta_source = self.direction_sources[direction] @ cardinal
                coefficients = np.einsum('cpl,l->cp', self.direction_gradients[direction], cardinal)[cells]
                delta_gradient = coefficients[:, 0]+coefficients[:, 1]*local
                changed_source = source+1j*step*delta_source
                changed_gradient = gradient+1j*step*delta_gradient
                changed = self.geometry(quadrature['reference'], changed_source, label)
                changed_temporal = rate-velocity*changed['displacement']*changed_gradient/changed['jacobian']
                changed_bulk = measure @ (changed['kinetic']*changed_temporal**2-
                    changed['gradient']*changed_gradient**2)/2
                changed_nodal = self.geometry(self.knots, changed_source, label)
                changed_factors = factors+1j*step*(self.direction_factor_values[direction] @ cardinal)
                changed_gram = -(self.sampling @ changed_nodal['gradient']) @ changed_factors**2/2
                changed_dust = self.dust(changed_source, velocity)[0]
                for name, value in [('bulk', changed_bulk), ('gram', changed_gram), ('dust', changed_dust)]:
                    derivatives[name][direction] += material_weight*float(value.imag/step)
        with localcontext() as context:
            context.prec = self.precision
            gram = np.vstack([-self.factor.apply(moments, transpose=True), decimal_array(gram_source)])
            contractions = {name:np.array([float(np.sum(decimal_array(vector)*direction))
                for direction in self.directions]) for name, vector in [('bulk', bulk), ('dust', dust)]}
            contractions['gram'] = np.array([float(np.sum(gram*direction)) for direction in self.directions])
        return dict(bulk=bulk, gram=np.asarray(gram, dtype=float), dust=dust, gram_decimal=gram,
            gram_moments=moments, contractions=contractions, derivatives=derivatives, actions=actions,
            wrong_source=wrong_source, minimum_metric=minimum_metric, maximum_speed=maximum_speed,
            sample_count=sample_count, material_weight_sum=float(sum(weights)))
