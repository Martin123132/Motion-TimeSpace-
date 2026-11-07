from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_radial_constraint_20260920 import CandidateRadialSolve
from annular_candidate_canonical_response_20260920 import temporal_values, velocity_design, velocity_forcing, solve_tangent
from annular_P2_indexed_live_geometry_20260919 import IndexedP2Density, indexed_label_values
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from annular_joint_first_tangent_20260922 import MetricResponse
from annular_moving_Legendre_current_20260921 import samples
from annular_directional_coupled_Euler_20260928 import interpolate_nodal
from annular_support_shift_jet_20260928 import integrals
from scipy.sparse import csr_matrix, vstack
from time import perf_counter
from copy import copy
import numpy as np
import sympy as sp


def symbolic_checks(evidence):
    alpha, temporal, defect, metric_rate, integral, weighted = sp.symbols('alpha T d r I a')
    beta, gradient, speed, speed_r, alpha_r = sp.symbols('beta g W W_R alpha_R')
    alpha_t, gradient_rate, temporal_rate, weighted_r = sp.symbols('alpha_t gdot Tdot a_R')
    energy = (alpha * temporal**2 + beta * gradient**2) / 2
    energy_rate = ((alpha_t + speed * alpha_r) * temporal**2 - beta * alpha_t / alpha * gradient**2) / 2
    energy_rate += alpha * temporal * temporal_rate + beta * gradient * gradient_rate
    momentum_rate = (alpha_t + speed * alpha_r + speed_r * alpha) * temporal + alpha * temporal_rate
    current = -momentum_rate * weighted - (alpha * speed * temporal + beta * gradient) * weighted_r
    current += (energy_rate + speed_r * energy + alpha_t / alpha * energy) * integral
    changed = sp.diff(current, temporal_rate) * defect + sp.diff(current, alpha_t) * alpha * metric_rate
    expected = alpha * (defect + temporal * metric_rate) * (temporal * integral - weighted)
    evidence.check('current_acceleration_and_metric_time_block', sp.expand(changed - expected) == 0)
    amplitude, rate, coefficient = sp.symbols('amplitude rate coefficient')
    density = coefficient * (rate + amplitude * defect)**2 / 2
    evidence.check('direct_positive_acceleration_norm', sp.diff(density, amplitude, 2) == coefficient * defect**2)


def support_defect(density, loads, edge_vertices, field_vertices):
    material, model = loads.material, loads.owner.model
    radius, label = density.radius[density.indices], density.offsets
    source = density.interpolation @ loads.coordinates[:, -1].astype(float)
    inner, outer = model.radii[0] + loads.owner.width * label, model.radii[-1] + loads.owner.width * label
    left = radius < source
    jacobian = np.where(left, (source - inner) / (model.anchor - model.radii[0]),
        (outer - source) / (model.radii[-1] - model.anchor))
    reference = np.where(left, model.radii[0] + (radius - inner) / jacobian,
        model.radii[-1] - (outer - radius) / jacobian)
    cells = np.clip(np.searchsorted(model.edges, reference, side='right') - 1, 0, len(model.edges) - 2)
    local = (reference - model.edges[cells]) / np.diff(model.edges)[cells]
    edge_values = indexed_label_values(density.interpolation, edge_vertices, np.column_stack([cells, cells + 1]))
    movement = edge_values[:, 0] * (1 - local) + edge_values[:, 1] * local
    field = np.sum(density.shape * indexed_label_values(density.interpolation, field_vertices, density.scalar_indices), axis=1)
    gradient = material.samples(radius, label)[3]
    return field - movement * gradient


class SupportRadialResponse:
    def __init__(self, loads, action, extension, directions, deadline, progress):
        self.extension, self.deadline = extension, deadline
        solver = CandidateRadialSolve.__new__(CandidateRadialSolve)
        solver.loads, solver.owner = loads, loads.owner
        solver.rule, solver.label_order = ChebyshevRule(22), 28
        solver.edges = action.solver.edges.copy()
        solver.lengths = np.diff(solver.edges)
        solver.centers = (solver.edges[1:] + solver.edges[:-1]) / 2
        solver.nodes = solver.centers[:, None] + solver.lengths[:, None] * solver.rule.points / 2
        self.solver, self.state = solver, action.solution['state']
        radius, shape = solver.nodes.ravel(), loads.rates.shape
        loads.owner.label_order = solver.label_order
        fields = {name: np.zeros(len(radius)) for name in ['temporal_square', 'gradient_square', 'source_density', 'velocity']}
        support = np.zeros(len(radius))
        temporal_rows, velocity_rows = [], []
        stored_bytes = 0
        for start in range(0, len(radius), 32):
            if perf_counter() > deadline:
                raise RuntimeError('Safe radial-response preparation boundary')
            section = slice(start, min(start + 32, len(radius)))
            density = IndexedP2Density(loads.material, radius[section])
            density.update(loads.rates)
            for name in fields:
                fields[name][section] = getattr(density, name)
            temporal = temporal_values(density, loads.rates)
            defect = support_defect(density, loads, directions['edge_vertices'], directions['field_vertices'])
            support[section] = np.bincount(density.indices, weights=2 * density.label_weights * temporal * defect,
                minlength=len(density.radius))
            aggregation = csr_matrix((2 * density.label_weights * temporal,
                (density.indices, np.arange(len(temporal)))), shape=(len(density.radius), len(temporal)))
            reduced = (aggregation @ velocity_design(density, *shape)).tocsr()
            reduced.eliminate_zeros()
            selected = np.flatnonzero(density.source_selected)
            source_columns = np.arange(shape[0]) * shape[1] + shape[1] - 1
            velocity = csr_matrix((density.source_interpolation.ravel(),
                (np.repeat(selected, shape[0]), np.tile(source_columns, len(selected)))),
                shape=(len(density.radius), loads.rates.size))
            velocity.eliminate_zeros()
            temporal_rows.append(reduced)
            velocity_rows.append(velocity)
            stored_bytes += sum(array.nbytes for matrix in [reduced, velocity] for array in [matrix.data, matrix.indices, matrix.indptr])
            if stored_bytes > 1536 * 1024**2:
                raise RuntimeError('Sparse response exceeds 1.5 GiB storage gate')
            if start % 4096 == 0:
                progress('radial-response-' + str(start) + '-of-' + str(len(radius)))
        self.temporal = vstack(temporal_rows, format='csr')
        self.velocity = vstack(velocity_rows, format='csr')
        self.support, self.stored_bytes = support, stored_bytes
        fields['gram'] = {extension: loads.gram_density(radius, extension)}
        solver.fields = fields
        self.base_residual = float(np.max(abs(solver.residual(self.state, extension))))

    def apply(self, old_direction, support_scale=1.):
        if perf_counter() > self.deadline:
            raise RuntimeError('Safe metric-response solve boundary')
        temporal = support_scale * self.support + self.temporal @ old_direction.ravel()
        velocity = self.velocity @ old_direction.ravel()
        forcing = velocity_forcing(self.solver, self.state, temporal, velocity)
        tangent, residual, history = solve_tangent(self.solver, self.state, self.extension, forcing)
        unused, local = self.solver.rhs(self.state, self.extension, True)
        rhs = (np.einsum('abn,bn->an', local, tangent.reshape(2, -1)) + forcing).reshape(2, *self.solver.nodes.shape)
        coefficients = rhs @ self.solver.rule.inverse.T
        primitives = np.stack([np.polynomial.chebyshev.chebint(values.T).T * self.solver.lengths[:, None] / 2 for values in coefficients])
        for component in range(2):
            primitives[component, :, 0] -= np.polynomial.chebyshev.chebval(-1., primitives[component].T)
        increments = np.array([np.polynomial.chebyshev.chebval(1., values.T) for values in primitives])
        outer = -sum(increments[0]) / (self.solver.edges[-1] - 2 * self.state[0, -1, -1])
        left = np.array([np.r_[0., np.cumsum(increments[0, :-1])],
            outer - sum(increments[1]) + np.r_[0., np.cumsum(increments[1, :-1])]])
        result = MetricResponse(self.solver, dict(state=tangent, rhs_coefficients=coefficients,
            primitives=primitives, left=left), forcing, residual, history)
        result.temporal, result.velocity = temporal, velocity
        return result

    def complex_check(self, response, step=1e-20):
        altered = copy(self.solver)
        altered.fields = dict(self.solver.fields)
        altered.fields['temporal_square'] = self.solver.fields['temporal_square'] + 1j * step * response.temporal
        altered.fields['velocity'] = self.solver.fields['velocity'] + 1j * step * response.velocity
        state = self.state.astype(complex)
        for unused in range(32):
            rhs = altered.rhs(state, self.extension)
            mass = altered.owner.central_mass + altered.integrated(rhs[0])
            primitive = altered.integrated(rhs[1])
            lapse = .5 * np.log(1 - 2 * mass[-1, -1] / altered.edges[-1]) + primitive - primitive[-1, -1]
            state = np.stack([mass, lapse])
        return state.imag / step


def projected_response(loads, action, directions, correction, response, order):
    labels, weights = np.polynomial.legendre.leggauss(order)
    labels, weights = labels / 2, weights / 2
    weights *= 6 * (labels + .5) * (.5 - labels)
    reference_edges = np.array([float(value) for value in action.edges])
    totals, moments = [], []
    for label in labels:
        row = samples(action, label, 12)
        geometry, quad, cardinal = row['geometry'], row['quadrature'], row['cardinal']
        cells, local = quad['cells'], quad['local']
        indices = np.array(action.mesh['elements'])[cells]
        widths = np.diff(reference_edges)[cells] * geometry['jacobian']
        radius, metric = geometry['radius'], geometry['metric']
        alpha = radius**2 / (geometry['lapse'] * np.sqrt(metric))
        measure = quad['measure'] * geometry['jacobian']
        field_nodes = cardinal @ (directions['field_vertices'] - correction[:, :-1])
        source_direction = -float(cardinal @ correction[:, -1])
        field = interpolate_nodal(field_nodes, indices, local, widths)[0]
        edges = cardinal @ directions['edge_vertices']
        eta = edges[cells] * (1 - local) + edges[cells + 1] * local + geometry['displacement'] * source_direction
        defect = field - eta * row['gradient'] / geometry['jacobian']
        variation = response.values(radius)
        ratio = variation[0] / (radius * metric) - variation[1]
        norm = measure @ (alpha * defect**2)
        metric_work = measure @ (alpha * row['temporal'] * ratio * defect)
        source = row['source']
        source_radius = np.array([source])
        source_values = action.solver.values(action.solution, source_radius)[0][:, 0]
        source_metric, source_lapse = 1 - 2 * source_values[0] / source, np.exp(source_values[1])
        clock_square = source_lapse**2 - row['velocity']**2 / source_metric
        inertia = action.owner.source_mass * source_lapse**2 / (source_metric * clock_square**1.5)
        source_momentum = action.owner.source_mass * row['velocity'] / (source_metric * np.sqrt(clock_square))
        mass_partial = source_momentum * (2 / (source * source_metric) + row['velocity']**2 / (source * source_metric**2 * clock_square))
        lapse_partial = -source_momentum * source_lapse**2 / clock_square
        source_variation = response.values(source_radius)[:, 0]
        dust_norm = inertia * source_direction**2
        dust_metric = source_direction * (mass_partial * source_variation[0] + lapse_partial * source_variation[1])
        totals.append([norm, dust_norm, metric_work, dust_metric, norm + dust_norm + metric_work + dust_metric])
        node_radius = action.geometry(action.knots, source, label)['radius']
        node_rate = cardinal @ loads.rates[:, :-1]
        local_moments = []
        for power in range(3):
            integral = integrals(radius, source, power)
            weighted = interpolate_nodal(node_rate * integrals(node_radius, source, power), indices, local, widths)[0]
            difference = row['temporal'] * integral - weighted
            fixed_current = measure @ (alpha * defect * difference)
            metric_current = measure @ (alpha * row['temporal'] * ratio * difference)
            local_moments.append([fixed_current, metric_current, fixed_current + metric_current])
        moments.append(local_moments)
    totals, moments = np.array(totals), np.array(moments)
    return dict(labels=labels, weights=weights, totals=totals, moments=moments,
        average=np.tensordot(weights, totals, axes=(0, 0)), current=np.tensordot(weights, moments, axes=(0, 0)))


def gravitational_moments(action, response, order):
    solver = response.solver
    points, weights = np.polynomial.legendre.leggauss(order)
    radius = (solver.centers[:, None] + solver.lengths[:, None] * points / 2).ravel()
    measure = (solver.lengths[:, None] * weights / 2).ravel()
    values = action.solver.values(action.solution, radius)[0]
    metric = 1 - 2 * values[0] / radius
    coefficient = np.exp(values[1]) / (action.owner.coupling * np.sqrt(metric))
    mass_rate = response.values(radius)[0]
    return np.array([measure @ (coefficient * mass_rate * (radius - 6)**power) for power in range(3)])
