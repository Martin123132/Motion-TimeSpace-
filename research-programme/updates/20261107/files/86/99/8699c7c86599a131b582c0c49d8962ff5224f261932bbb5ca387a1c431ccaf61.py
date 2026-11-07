from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_physical_native_kernel_20260928 import NativeKernel, maximum
from annular_common_weighted_moments_20260920 import decimal_fraction
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_nested_physical_refinement_v3_20260922 import adapt_owner
from annular_candidate_midpoint_20260921 import CommonLoads
from annular_candidate_coordinate_covectors_20260921 import CoordinateAction
from annular_candidate_radial_constraint_20260920 import CandidateRadialSolve
from annular_source_flat_native_20261002 import NativeFlatLoads
from annular_P2_indexed_live_geometry_20260919 import IndexedP2Material
from annular_candidate_full_inverse_20260920 import BandedSourceInverse
from scipy.linalg import cholesky_banded, cho_solve_banded, cho_factor
from scipy.sparse import csr_matrix, coo_matrix
from fractions import Fraction
from decimal import Decimal, localcontext
from bisect import bisect_right
from time import perf_counter
import numpy as np


ZERO = Decimal(0)


class PolynomialBasis:
    def __init__(self, degree):
        self.degree = degree
        self.nodes = [Fraction(index, degree) for index in range(degree + 1)]
        columns = []
        for index, point in enumerate(self.nodes):
            values = [Fraction(1)]
            for other, target in enumerate(self.nodes):
                if other == index:
                    continue
                updated = [Fraction(0)] * (len(values) + 1)
                for power, value in enumerate(values):
                    updated[power] -= target * value / (point - target)
                    updated[power + 1] += value / (point - target)
                values = updated
            columns.append(values)
        self.rational = np.array(columns, dtype=object).T
        self.exact = np.array([[decimal_fraction(value) for value in row] for row in self.rational], dtype=object)
        self.coefficients = np.asarray(self.exact, float)
        self.left_first = self.exact[1]
        self.right_first = np.sum(self.exact * np.arange(degree + 1)[:, None], axis=0)

    def values(self, coordinate, derivative=0):
        coefficients = np.polynomial.polynomial.polyder(self.coefficients, derivative, axis=0)
        return np.polynomial.polynomial.polyval(coordinate, coefficients).T

    def polynomial(self, indices, field):
        local = np.full(indices.shape + field.shape[1:], ZERO, dtype=object)
        selected = indices >= 0
        local[selected] = field[indices[selected]]
        if field.ndim == 1:
            return local @ self.exact.T
        return np.matmul(self.exact[None, :, :], local)


def high_mesh(support, anchor, degree=6, subdivide=1):
    edges = sorted(set(map(Fraction, support)) | {Fraction(anchor)})
    edges = sorted(set(edges + [lower + (upper - lower) * Fraction(index, subdivide)
        for lower, upper in zip(edges[:-1], edges[1:]) for index in range(1, subdivide)]))
    nodes = sorted({lower + (upper - lower) * Fraction(index, degree)
        for lower, upper in zip(edges[:-1], edges[1:]) for index in range(degree + 1)} - {Fraction(anchor)})
    lookup = {point: index for index, point in enumerate(nodes)}
    elements = [[lookup.get(lower + (upper - lower) * Fraction(index, degree), -1) for index in range(degree + 1)]
        for lower, upper in zip(edges[:-1], edges[1:])]
    return dict(edges=list(map(str, edges)), nodes=list(map(str, nodes)), elements=elements, anchor=str(Fraction(anchor)),
        count=len(nodes), degree=degree, gram_support=list(support), fixed_interaction_support=True)


class HighKernel(NativeKernel):
    def __init__(self, mesh, support, enabled=True):
        super().__init__(mesh, support, enabled)
        self.basis = PolynomialBasis(mesh.get('degree', 2))
        self.native_indices = np.r_[self.indices[:, 0], self.indices[-1, -1]][self.native_edges]

    def atoms(self, edges, field):
        widths = np.diff(edges)
        if min(widths) <= 0:
            raise ValueError('Unordered physical cells')
        polynomial = self.basis.polynomial(self.indices, field)
        powers = np.arange(polynomial.shape[1])
        return dict(widths=widths, polynomial=polynomial, slope_left=polynomial[:, 1] / widths,
            slope_right=np.sum(polynomial * powers, axis=1) / widths,
            curvature_left=2 * polynomial[:, 2] / widths**2,
            curvature_right=np.sum(polynomial * powers * (powers - 1), axis=1) / widths**2)

    def evaluate(self, edges, field, beta, beta_radial=None):
        atom = self.atoms(edges, field)
        native, source = edges[self.native_edges], edges[self.anchor]
        jump = atom['slope_left'][self.anchor] - atom['slope_right'][self.anchor - 1]
        hinge = np.maximum(native - source, ZERO)
        values = field[self.native_indices] - jump * hinge
        kernels, coefficients, widths = [], [], []
        for index in range(len(native) - 3):
            width, row = self.stencil(native[index:index + 4])
            row = np.array(row, dtype=object) * int(self.enabled) / width.sqrt()
            kernels.append(sum(row * values[index:index + 4], ZERO))
            coefficients.append(row)
            widths.append(width)
        kernels = np.array(kernels, dtype=object)
        image = self.apply('template', kernels)
        weights = self.apply('sampling', beta)
        multiplier = self.apply('template', weights * image, True)
        load = self.apply('sampling', image**2 / 2, True)
        native_field = np.full(len(native), ZERO, dtype=object)
        native_shape = np.full(len(native), ZERO, dtype=object)
        for index, (row, width, weight) in enumerate(zip(coefficients, widths, multiplier)):
            points = native[index:index + 4]
            native_field[index:index + 4] += weight * row
            dilation = Decimal('2.5') * weight * kernels[index] / (3 * width)
            native_shape[index] -= dilation
            native_shape[index + 3] += dilation
            for first in range(4):
                product = weight * row[first] * values[index + first]
                for second in range(4):
                    if first != second:
                        changed = product / (points[first] - points[second])
                        native_shape[index + first] -= changed
                        native_shape[index + second] += changed
        native_shape -= jump * native_field * (native > source)
        if beta_radial is not None:
            native_shape += load * beta_radial
        field_gradient = np.full(self.count, ZERO, dtype=object)
        np.add.at(field_gradient, self.native_indices, native_field)
        edge_gradient = np.full(len(edges), ZERO, dtype=object)
        edge_gradient[self.native_edges] += native_shape
        jump_covector = -sum(native_field * hinge, ZERO)
        for cell, endpoint, sign in [(self.anchor - 1, self.basis.right_first, -1), (self.anchor, self.basis.left_first, 1)]:
            selected = self.indices[cell] >= 0
            np.add.at(field_gradient, self.indices[cell, selected], sign * jump_covector * endpoint[selected] / atom['widths'][cell])
        left_slope, right_slope = atom['slope_right'][self.anchor - 1], atom['slope_left'][self.anchor]
        edge_gradient[self.anchor - 1] -= jump_covector * left_slope / atom['widths'][self.anchor - 1]
        edge_gradient[self.anchor] += jump_covector * (left_slope / atom['widths'][self.anchor - 1] + right_slope / atom['widths'][self.anchor])
        edge_gradient[self.anchor + 1] -= jump_covector * right_slope / atom['widths'][self.anchor]
        edge_gradient[self.anchor] += jump * sum(native_field[native > source], ZERO)
        return dict(energy=sum(weights * image**2 / 2, ZERO), image=image, load=load, native_field=native_field,
            native_shape=native_shape, field_gradient=field_gradient, edge_gradient=edge_gradient, atoms=atom,
            source_jump=jump, jump_covector=jump_covector)


class HighMaterial(IndexedP2Material):
    def __init__(self, owner, coordinates, mesh, polynomial, basis):
        super().__init__(owner, np.asarray(coordinates, float))
        self.mesh, self.polynomial, self.basis = mesh, polynomial, basis
        self.gradient = polynomial[:, 1:] * np.arange(1, basis.degree + 1)[None, :, None]
        self.gradient /= np.diff(owner.model.edges)[:, None, None]

    def samples(self, radius, labels):
        model = self.owner.model
        interpolation = self.interpolation(labels)
        source = interpolation @ self.coordinates[:, -1]
        inner, outer = model.radii[0] + self.owner.width * labels, model.radii[-1] + self.owner.width * labels
        left = radius < source
        jacobian = np.where(left, (source - inner) / (model.anchor - model.radii[0]), (outer - source) / (model.radii[-1] - model.anchor))
        reference = np.where(left, model.radii[0] + (radius - inner) / jacobian, model.radii[-1] - (outer - radius) / jacobian)
        cells = np.clip(np.searchsorted(model.edges, reference, side='right') - 1, 0, len(model.edges) - 2)
        local = (reference - model.edges[cells]) / np.diff(model.edges)[cells]
        raw_indices = model.element_indices[cells]
        shape = self.basis.values(local) * (raw_indices >= 0)
        coefficients = np.einsum('ql,qpl->qp', interpolation, self.gradient[cells], optimize=False)
        gradient = np.polynomial.polynomial.polyval(local, coefficients.T, tensor=False) / jacobian
        unused, unused2, displacement = model.mapping(reference, model.anchor)
        outside = (radius < inner) | (radius > outer)
        shape[outside], gradient[outside] = 0., 0.
        return interpolation, np.maximum(raw_indices, 0), shape, gradient, -displacement * gradient


class HighLoads(NativeFlatLoads):
    def __init__(self, owner, coordinates, rates, mesh, branch, deadline):
        self.owner, self.coordinates, self.rates, self.deadline = owner, coordinates, rates, deadline
        self.knots = owner.model.radii
        self.sampling = csr_matrix((0, mesh['count'])).tocsc()
        self.native_engine = HighKernel(mesh, mesh['gram_support'], branch == 'primary')
        self.basis = self.native_engine.basis
        self.native_references = np.array([float(self.native_engine.references[index]) for index in self.native_engine.native_edges])
        self.native_sampling = self.native_engine.sampling.tocsc()
        with localcontext() as context:
            context.prec = 64
            polynomial = self.basis.polynomial(np.array(mesh['elements']), coordinates[:, :-1].T)
            self.polynomial = np.asarray(polynomial, float)
            from annular_quadratic_core_20261002 import physical_edges
            factors = []
            for index, label in enumerate(owner.layer_rule.points / 2):
                edges = physical_edges(self.native_engine, coordinates[index, -1], label, owner.width)
                result = self.native_engine.evaluate(edges, coordinates[index, :-1], np.full(len(mesh['gram_support']), Decimal(1), dtype=object))
                factors.append(np.asarray(result['image'], float))
        self.native_factor_vertices = np.array(factors)
        self.native_factor_coefficients = owner.layer_rule.inverse @ self.native_factor_vertices
        self.material = HighMaterial(owner, coordinates, mesh, self.polynomial, self.basis)

    sample = CommonLoads.sample


class HighAction(CoordinateAction):
    def __init__(self, loads, mesh, solver, solution):
        self.owner, self.mesh, self.solver, self.solution = loads.owner, mesh, solver, solution
        self.loads, self.basis = loads, loads.basis
        self.edges = list(map(Fraction, mesh['edges']))
        self.knots = loads.knots
        self.source = np.asarray(loads.coordinates[:, -1], float)
        self.velocity = loads.rates[:, -1]
        self.polynomial = loads.polynomial
        self.gradient = loads.material.gradient
        with localcontext() as context:
            context.prec = 64
            self.rate_polynomial = np.asarray(self.basis.polynomial(np.array(mesh['elements']), decimal_array(loads.rates[:, :-1].T)), float)

    def quadrature(self, label, source, order):
        model = self.owner.model
        inner, outer = model.radii[[0, -1]] + self.owner.width * label
        selected = self.solver.edges[(self.solver.edges > inner) & (self.solver.edges < outer)]
        jacobian = np.where(selected < source, (source - inner) / (model.anchor - model.radii[0]), (outer - source) / (model.radii[-1] - model.anchor))
        pulled = np.where(selected < source, model.radii[0] + (selected - inner) / jacobian, model.radii[-1] - (outer - selected) / jacobian)
        cuts = sorted(set(self.edges + list(map(Fraction.from_float, pulled))))
        cuts = [value for value in cuts if self.edges[0] <= value <= self.edges[-1]]
        cells, offsets, spans, lengths = [], [], [], []
        for lower, upper in zip(cuts, cuts[1:]):
            cell = bisect_right(self.edges, (lower + upper) / 2) - 1
            width = self.edges[cell + 1] - self.edges[cell]
            cells.append(cell)
            offsets.append(float((lower - self.edges[cell]) / width))
            spans.append(float((upper - lower) / width))
            lengths.append(float(upper - lower))
        nodes, weights = np.polynomial.legendre.leggauss(order)
        local = (np.array(offsets)[:, None] + np.array(spans)[:, None] * (nodes + 1) / 2).ravel()
        measure = (np.array(lengths)[:, None] * weights / 2).ravel()
        cells = np.repeat(cells, order)
        widths = np.diff(model.edges)[cells]
        reference = model.edges[cells] + widths * local
        indices = np.array(self.mesh['elements'])[cells]
        shape = self.basis.values(local) * (indices >= 0)
        radial = self.basis.values(local, 1) / widths[:, None] * (indices >= 0)
        return dict(cells=cells, local=local, reference=reference, measure=measure, indices=np.maximum(indices, 0), shape=shape, radial=radial)

    def samples(self, label, order):
        cardinal = np.asarray(self.cardinal(label)).ravel()
        source, velocity = cardinal @ self.source, cardinal @ self.velocity
        quadrature = self.quadrature(label, source, order)
        cells, local = quadrature['cells'], quadrature['local']
        coefficients = np.einsum('cpl,l->cp', self.gradient, cardinal)[cells]
        gradient = np.polynomial.polynomial.polyval(local, coefficients.T, tensor=False)
        coefficients = np.einsum('cpl,l->cp', self.rate_polynomial, cardinal)[cells]
        rate = np.polynomial.polynomial.polyval(local, coefficients.T, tensor=False)
        geometry = self.geometry(quadrature['reference'], source, label)
        motion = -geometry['displacement'] * gradient / geometry['jacobian']
        return dict(cardinal=cardinal, source=source, velocity=velocity, quadrature=quadrature, gradient=gradient,
            temporal=rate + velocity * motion, geometry=geometry, motion=motion)


def live_high(owner, coordinates, rates, mesh, branch, deadline):
    loads = HighLoads(owner, coordinates, rates, mesh, branch, deadline)
    solver = CandidateRadialSolve(loads, 22, 28, [branch])
    solution = solver.solve(branch)
    return loads, HighAction(loads, mesh, solver, solution)


class HighInverse(BandedSourceInverse):
    def __init__(self, matrix, shape, degree):
        labels, components = shape
        self.shape, self.count = shape, labels * components
        self.field_count = labels * (components - 1)
        original = np.arange(self.count).reshape(shape)
        self.permutation = np.r_[original[:, :-1].T.ravel(), original[:, -1]]
        self.inverse_permutation = np.argsort(self.permutation)
        raw = matrix.tocsr()
        difference = raw - raw.T
        self.symmetry_error = float(max(abs(difference.data), default=0.) / max(abs(raw.data)))
        if self.symmetry_error > 2e-12:
            raise ValueError('High-order mass reciprocity failed')
        self.matrix = ((raw + raw.T) * .5).tocsr()
        ordered = self.matrix[self.permutation][:, self.permutation]
        diagonal = ordered.diagonal()
        if np.min(diagonal) <= 0:
            raise ValueError('Nonpositive canonical direction')
        self.scale = np.sqrt(diagonal)
        self.original_scale = self.scale[self.inverse_permutation]
        self.bandwidth = (degree + 1) * labels - 1
        field = ordered[:self.field_count, :self.field_count].tocoo()
        if np.max(abs(field.row - field.col)) > self.bandwidth:
            raise ValueError('Unexpected high-order bandwidth')
        self.bands = np.zeros((self.bandwidth + 1, self.field_count))
        selected = field.row >= field.col
        rows, columns = field.row[selected], field.col[selected]
        self.bands[rows - columns, columns] = field.data[selected] / (self.scale[rows] * self.scale[columns])
        self.factor = cholesky_banded(self.bands, lower=True, check_finite=False)
        cross = ordered[:self.field_count, self.field_count:].toarray()
        self.cross = cross / (self.scale[:self.field_count, None] * self.scale[None, self.field_count:])
        source = ordered[self.field_count:, self.field_count:].toarray()
        self.source = source / (self.scale[self.field_count:, None] * self.scale[None, self.field_count:])
        self.field_cross = cho_solve_banded((self.factor, True), self.cross, check_finite=False)
        self.schur = self.source - self.cross.T @ self.field_cross
        self.schur_symmetry_error = float(np.max(abs(self.schur - self.schur.T)))
        if self.schur_symmetry_error > 2e-12:
            raise ValueError('High-order source Schur reciprocity failed')
        self.schur = (self.schur + self.schur.T) / 2
        self.source_factor = cho_factor(self.schur, lower=True, check_finite=False)


def zero_system(action, spatial, material, deadline, progress):
    if np.any(action.velocity) or np.any(action.rate_polynomial):
        raise ValueError('Zero-rate Hessian requires time-symmetric data')
    labels, count = len(action.source), len(action.knots)
    degree, cells_count = action.basis.degree, len(action.mesh['elements'])
    field_blocks = np.zeros((cells_count, degree + 1, degree + 1, labels, labels))
    cross_blocks = np.zeros((count, labels, labels))
    source_block = np.zeros((labels, labels))
    wave_force, dust_force = np.zeros((labels, count + 1)), np.zeros((labels, count + 1))
    points, weights = np.polynomial.legendre.leggauss(material)
    points, weights = points / 2, weights / 2
    weights *= 6 * (points + .5) * (.5 - points)
    for index, (label, weight) in enumerate(zip(points, weights)):
        if perf_counter() > deadline:
            raise RuntimeError('Safe high-order Hessian boundary')
        row = action.samples(label, spatial)
        quad, geometry, cardinal = row['quadrature'], row['geometry'], row['cardinal']
        measure, shape = quad['measure'], quad['shape']
        kinetic, motion = geometry['kinetic'], row['motion']
        outer = weight * np.outer(cardinal, cardinal)
        for first in range(degree + 1):
            for second in range(degree + 1):
                integral = np.bincount(quad['cells'], weights=measure * kinetic * shape[:, first] * shape[:, second], minlength=cells_count)
                field_blocks[:, first, second] += integral[:, None, None] * outer
        cross_values = np.zeros(count)
        np.add.at(cross_values, quad['indices'].ravel(), (measure[:, None] * kinetic[:, None] * motion[:, None] * shape).ravel())
        cross_blocks += cross_values[:, None, None] * outer
        values, unused = action.solver.values(action.solution, np.array([row['source']]))
        lapse, metric = np.exp(values[1, 0]), 1 - 2 * values[0, 0] / row['source']
        source_block += (measure @ (kinetic * motion**2) + action.owner.source_mass / (metric * lapse)) * outer
        field_force = np.zeros(count)
        np.add.at(field_force, quad['indices'].ravel(), (-measure * geometry['gradient'] * row['gradient'])[:, None].repeat(degree + 1, axis=1).ravel() * quad['radial'].ravel())
        source_force = -measure @ (geometry['gradient_source'] * row['gradient']**2 / 2)
        wave_force += weight * np.outer(cardinal, np.r_[field_force, source_force])
        dust_force[:, -1] += weight * cardinal * action.dust(row['source'], 0.)[1]
        if index % 8 == 7:
            progress('Hessian material ' + str(index + 1))
    elements = np.array(action.mesh['elements'])
    component_count = count + 1
    row_nodes = np.broadcast_to(elements[:, :, None, None, None], field_blocks.shape)
    column_nodes = np.broadcast_to(elements[:, None, :, None, None], field_blocks.shape)
    field_rows = np.broadcast_to(row_nodes + component_count * np.arange(labels)[None, None, None, :, None], field_blocks.shape)
    field_columns = np.broadcast_to(column_nodes + component_count * np.arange(labels)[None, None, None, None, :], field_blocks.shape)
    selected = (row_nodes >= 0) & (column_nodes >= 0)
    cross_rows = np.broadcast_to(np.arange(count)[:, None, None] + component_count * np.arange(labels)[None, :, None], cross_blocks.shape)
    cross_columns = np.broadcast_to(count + component_count * np.arange(labels)[None, None, :], cross_blocks.shape)
    source_indices = count + component_count * np.arange(labels)
    rows = np.r_[field_rows[selected], cross_rows.ravel(), cross_columns.ravel(), np.repeat(source_indices, labels)]
    columns = np.r_[field_columns[selected], cross_columns.ravel(), cross_rows.ravel(), np.tile(source_indices, labels)]
    values = np.r_[field_blocks[selected], cross_blocks.ravel(), cross_blocks.ravel(), source_block.ravel()]
    matrix = coo_matrix((values, (rows, columns)), shape=(labels * component_count,) * 2).tocsr()
    matrix.eliminate_zeros()
    return dict(matrix=matrix, inverse=HighInverse(matrix, (labels, component_count), degree),
        force=wave_force + dust_force, wave_force=wave_force, dust_force=dust_force)
