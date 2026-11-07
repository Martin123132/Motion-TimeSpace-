from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_coordinate_covectors_20260921 import CoordinateAction, local_polynomials
from annular_candidate_radial_constraint_20260920 import CandidateLoads, CandidateRadialSolve
from annular_P2_indexed_live_geometry_20260919 import IndexedP2Material, IndexedP2Density
from annular_mixed_weak_maps_20260920 import MixedMap
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_nonuniform_Gram_candidate_20260920 import template_rows
from decimal import Decimal, localcontext
from fractions import Fraction
from time import perf_counter
from scipy.sparse import csr_matrix
import numpy as np


class StableCommonMaterial(IndexedP2Material):
    def __init__(self, owner, coordinates, gradient_coefficients):
        super().__init__(owner, np.asarray(coordinates, dtype=float))
        self.gradient_coefficients = gradient_coefficients

    def samples(self, radius, labels):
        model = self.owner.model
        interpolation = self.interpolation(labels)
        source = interpolation @ self.coordinates[:, -1]
        inner, outer = model.radii[0]+self.owner.width*labels, model.radii[-1]+self.owner.width*labels
        left = radius < source
        jacobian = np.where(left, (source-inner)/(model.anchor-model.radii[0]),
            (outer-source)/(model.radii[-1]-model.anchor))
        reference = np.where(left, model.radii[0]+(radius-inner)/jacobian, model.radii[-1]-(outer-radius)/jacobian)
        indices, shape, unused = model.features_quadratic(reference)
        cells = np.clip(np.searchsorted(model.edges, reference, side='right')-1, 0, len(model.edges)-2)
        local = (reference-model.edges[cells])/(model.edges[cells+1]-model.edges[cells])
        coefficients = np.einsum('ql,qpl->qp', interpolation, self.gradient_coefficients[cells], optimize=False)
        gradient = (coefficients[:, 0]+coefficients[:, 1]*local)/jacobian
        unused, unused2, displacement = model.mapping(reference, model.anchor)
        outside = (radius < inner) | (radius > outer)
        shape[outside], gradient[outside] = 0., 0.
        return interpolation, indices, shape, gradient, -displacement*gradient


class CommonLoads(CandidateLoads):
    def __init__(self, owner, coordinates, rates, mesh, packet, extension, precision, deadline):
        self.owner, self.coordinates, self.rates = owner, coordinates, rates
        self.deadline = deadline
        self.knots = np.array([float(Fraction(value)) for value in mesh['nodes']])
        self.factor = MixedMap(packet['gram_factor']['rows'], packet['gram_factor']['columns'])
        self.sampling = template_rows(len(self.knots))[1].tocsc()
        if self.factor.shape[0] == 0:
            self.sampling = csr_matrix((0, len(self.knots))).tocsc()
        with localcontext() as context:
            context.prec = precision
            self.polynomial, gradient = local_polynomials(mesh, coordinates[:, :-1].T)
            self.exact_factors = self.factor.apply(coordinates[:, :-1].T)
        self.material = StableCommonMaterial(owner, coordinates, gradient)
        self.factor_vertices = {extension:np.asarray(self.exact_factors.T, dtype=float)}
        self.factor_coefficients = {extension:owner.layer_rule.inverse @ self.factor_vertices[extension]}

    def sample(self, radius, label_order, extensions, chunk_size=128):
        radius = np.asarray(radius).ravel()
        self.owner.label_order = label_order
        fields = {name:np.zeros_like(radius) for name in ['temporal_square', 'gradient_square', 'source_density', 'velocity']}
        for start in range(0, len(radius), chunk_size):
            if perf_counter() > self.deadline:
                raise RuntimeError('Safe wall boundary during live common-state density preparation.')
            section = slice(start, start+chunk_size)
            density = IndexedP2Density(self.material, radius[section])
            density.update(self.rates)
            for name in fields:
                fields[name][section] = getattr(density, name)
        fields['gram'] = {extension:self.gram_density(radius, extension) for extension in extensions}
        return fields


class CommonCoordinateAction(CoordinateAction):
    def __init__(self, owner, coordinates, rates, mesh, loads, solver, solution, precision):
        self.owner, self.mesh, self.solver, self.solution = owner, mesh, solver, solution
        self.edges, self.knots = list(map(Fraction, mesh['edges'])), loads.knots
        self.factor, self.sampling = loads.factor, loads.sampling.tocsr()
        self.source, self.velocity = np.asarray(coordinates[:, -1], float), rates[:, -1]
        self.precision = precision
        with localcontext() as context:
            context.prec = precision
            self.polynomial, self.gradient = local_polynomials(mesh, coordinates[:, :-1].T)
            self.rate_polynomial, unused = local_polynomials(mesh, decimal_array(rates[:, :-1].T))
        self.factor_values = np.asarray(loads.exact_factors, float)

    def momentum_and_force(self, reference_order, material_order, deadline):
        count, labels = len(self.knots), len(self.source)
        momentum, bulk, dust = [np.zeros((count+1, labels)) for unused in range(3)]
        gram_source = np.zeros(labels)
        moments = np.full((self.factor.shape[0], labels), Decimal(0), dtype=object)
        points, weights = np.polynomial.legendre.leggauss(material_order)
        points, weights = points/2, weights/2
        weights *= 6*(points+.5)*(.5-points)
        action, minimum_metric, maximum_speed = 0., 1., 0.
        for label, material_weight in zip(points, weights):
            if perf_counter() > deadline:
                raise RuntimeError('Safe wall boundary during common-state action evaluation.')
            cardinal = np.asarray(self.cardinal(label)).ravel()
            source, velocity = cardinal @ self.source, cardinal @ self.velocity
            quadrature = self.quadrature(label, source, reference_order)
            cells, local, measure = [quadrature[name] for name in ['cells', 'local', 'measure']]
            coefficients = np.einsum('cpl,l->cp', self.gradient, cardinal)[cells]
            gradient = coefficients[:, 0]+coefficients[:, 1]*local
            coefficients = np.einsum('cpl,l->cp', self.rate_polynomial, cardinal)[cells]
            rate = coefficients[:, 0]+local*(coefficients[:, 1]+local*coefficients[:, 2])
            geometry = self.geometry(quadrature['reference'], source, label)
            kinetic, spatial, jacobian, displacement, jacobian_source = [geometry[name]
                for name in ['kinetic', 'gradient', 'jacobian', 'displacement', 'jacobian_source']]
            motion = -displacement*gradient/jacobian
            temporal = rate+velocity*motion
            shape = np.column_stack([(1-local)*(1-2*local), 4*local*(1-local), local*(2*local-1)])
            indices = np.array(self.mesh['elements'])[cells]
            shape *= indices >= 0
            field_momentum, field_force = np.zeros(count), np.zeros(count)
            np.add.at(field_momentum, quadrature['indices'].ravel(),
                ((measure*kinetic*temporal)[:, None]*shape).ravel())
            weak = -measure*(kinetic*temporal*velocity*displacement/jacobian+spatial*gradient)
            np.add.at(field_force, quadrature['indices'].ravel(), (weak[:, None]*quadrature['radial']).ravel())
            source_force = measure @ (geometry['kinetic_source']*temporal**2/2-
                kinetic*temporal*velocity*motion*jacobian_source/jacobian-geometry['gradient_source']*gradient**2/2)
            bulk += material_weight*np.outer(np.r_[field_force, source_force], cardinal)
            nodal = self.geometry(self.knots, source, label)
            factors = self.factor_values @ cardinal
            sampled = self.sampling @ nodal['gradient']
            sampled_source = self.sampling @ nodal['gradient_source']
            gram_source -= material_weight*cardinal*(sampled_source @ factors**2)/2
            with localcontext() as context:
                context.prec = self.precision
                moments += decimal_array(material_weight*sampled*factors)[:, None]*decimal_array(cardinal)[None, :]
            dust_action, dust_force, source_metric, speed = self.dust(source, velocity)
            source_values, unused = self.solver.values(self.solution, np.array([source]))
            lapse = np.exp(source_values[1, 0])
            clock = np.sqrt(lapse**2-velocity**2/source_metric)
            source_momentum = measure @ (kinetic*temporal*motion)+self.owner.source_mass*velocity/(source_metric*clock)
            momentum += material_weight*np.outer(np.r_[field_momentum, source_momentum], cardinal)
            dust[-1] += material_weight*cardinal*dust_force
            action += material_weight*(measure @ (kinetic*temporal**2-spatial*gradient**2)/2-
                sampled @ factors**2/2+dust_action)
            minimum_metric = min(minimum_metric, float(np.min(geometry['metric'])), source_metric)
            maximum_speed = max(maximum_speed, speed)
        with localcontext() as context:
            context.prec = self.precision
            gram = np.vstack([-self.factor.apply(moments, transpose=True), decimal_array(gram_source)])
            force = decimal_array(bulk)+decimal_array(dust)+gram
        return dict(momentum=momentum.T, force=np.asarray(force.T, float), force_decimal=force.T,
            bulk=bulk.T, dust=dust.T, gram=np.asarray(gram.T, float), minimum_F=minimum_metric,
            maximum_speed_ratio=maximum_speed, matter_action=float(action))


class LiveCommonEvaluation:
    def __init__(self, owner, mesh, packet, extension, deadline, precision=64, reference_order=10, material_order=32):
        self.owner, self.mesh, self.packet, self.extension = owner, mesh, packet, extension
        self.deadline, self.precision = deadline, precision
        self.reference_order, self.material_order = reference_order, material_order
        self.evaluations = 0

    def evaluate(self, coordinates, rates):
        self.evaluations += 1
        loads = CommonLoads(self.owner, coordinates, rates, self.mesh, self.packet, self.extension, self.precision, self.deadline)
        solver = CandidateRadialSolve(loads, 22, 28, [self.extension])
        solution = solver.solve(self.extension)
        action = CommonCoordinateAction(self.owner, coordinates, rates, self.mesh, loads, solver, solution, self.precision)
        result = action.momentum_and_force(self.reference_order, self.material_order, self.deadline)
        result.update(solution=solution, solver=solver, radial_residual=solution['maximum_residual'],
            minimum_material_jacobian=loads.material.minimum_jacobian,
            minimum_spatial_jacobian=loads.material.minimum_spatial_jacobian)
        return result


def advance_coordinates(coordinates, rates, step, precision):
    with localcontext() as context:
        context.prec = precision
        return coordinates+Decimal.from_float(float(step))*decimal_array(rates)


def midpoint_step(evaluator, coordinates, momenta, seed, step, preconditioner, record):
    rates = seed.copy()
    scale = max(preconditioner.residual_norm(np.asarray(momenta, float)), 1e-30)
    history = []
    previous = None
    for iteration in range(20):
        midpoint = advance_coordinates(coordinates, rates, step/2, evaluator.precision)
        current = evaluator.evaluate(midpoint, rates)
        with localcontext() as context:
            context.prec = evaluator.precision
            residual_exact = (decimal_array(current['momentum'])-momenta-
                Decimal.from_float(float(step/2))*current['force_decimal'])
        residual = np.asarray(residual_exact, float)
        correction = preconditioner.solve(residual.ravel()).reshape(rates.shape)
        norm = preconditioner.residual_norm(residual)/scale
        maximum = float(np.max(abs(correction)))
        row = dict(iteration=iteration, relative_residual=norm, maximum_correction=maximum,
            radial_residual=current['radial_residual'], minimum_F=current['minimum_F'],
            maximum_speed_ratio=current['maximum_speed_ratio'],
            residual_ratio=None if previous is None else norm/previous)
        history.append(row)
        record(row, midpoint, rates, current, residual)
        if norm < 5e-12 and maximum < 2e-12:
            result = advance_coordinates(coordinates, rates, step, evaluator.precision)
            with localcontext() as context:
                context.prec = evaluator.precision
                updated = momenta+Decimal.from_float(float(step))*current['force_decimal']
            return result, updated, rates, current, history
        if previous is not None and norm > 1.25*previous:
            raise RuntimeError('Midpoint iteration is not contracting; no mode deletion or silent step change allowed.')
        previous = norm
        rates -= correction
    raise RuntimeError('Midpoint solver did not reach both declared stopping gates.')
