from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_radial_constraint_20260920 import CandidateRadialSolve
from annular_candidate_canonical_response_20260920 import temporal_values, velocity_design, velocity_forcing, solve_tangent
from annular_candidate_midpoint_20260921 import CommonLoads, CommonCoordinateAction
from annular_P2_indexed_live_geometry_20260919 import IndexedP2Density
from annular_moving_Legendre_current_20260921 import samples
from annular_candidate_energy_current_20260921 import richardson, excess_mass
from annular_decimal_transport_v2_20260919 import decimal_array
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from scipy.sparse import csr_matrix, vstack
from decimal import Decimal, localcontext
from time import perf_counter
from math import fsum
import numpy as np


class ZeroTangent:
    def at(self, radius):
        return np.zeros((2, len(radius))), np.zeros((2, len(radius)))


def shifted_coordinates(coordinates, rates, duration):
    with localcontext() as context:
        context.prec = 64
        return coordinates + Decimal.from_float(float(duration)) * decimal_array(rates)


def live_metric(owner, coordinates, rates, mesh, packet, extension, deadline):
    loads = CommonLoads(owner, coordinates, rates, mesh, packet, extension, 64, deadline)
    solver = CandidateRadialSolve(loads, 22, 28, [extension])
    solution = solver.solve(extension)
    action = CommonCoordinateAction(owner, coordinates, rates, mesh, loads, solver, solution, 64)
    return loads, action


class ProbeMetricRate:
    def __init__(self, actions, steps):
        self.actions, self.steps = actions, steps
        self.prefixes, self.cache = {}, {}
        for key, action in actions.items():
            increments = np.polynomial.chebyshev.chebval(1., action.solution['primitives'][0].T)
            self.prefixes[key] = np.array([fsum(increments[:index]) for index in range(len(increments))])

    def values(self, radius):
        cached = self.cache.get(id(radius))
        if cached is not None and cached[0] is radius:
            return cached[1]
        values = []
        for index in range(len(self.steps)):
            pair = []
            for sign in [-1, 1]:
                action = self.actions[index, sign]
                evaluated = action.solver.values(action.solution, radius)[0]
                solver, solution = action.solver, action.solution
                selected = np.clip(np.searchsorted(solver.edges, radius, side='right') - 1, 0, len(solver.edges) - 2)
                mapped = 2 * (radius - solver.centers[selected]) / solver.lengths[selected]
                evaluated[0] = self.prefixes[index, sign][selected] + np.polynomial.chebyshev.chebval(
                    mapped, solution['primitives'][0, selected].T, tensor=False)
                pair.append(evaluated)
            values.append(pair)
        result = richardson(np.array(values), self.steps)[1]
        self.cache[id(radius)] = (radius, result)
        return result


class RadialResponse:
    def __init__(self, loads, base, extension, deadline, progress):
        self.extension, self.deadline = extension, deadline
        solver = CandidateRadialSolve.__new__(CandidateRadialSolve)
        solver.loads, solver.owner = loads, loads.owner
        solver.rule, solver.label_order = ChebyshevRule(22), 28
        solver.edges = base.solver.edges.copy()
        solver.lengths = np.diff(solver.edges)
        solver.centers = (solver.edges[1:] + solver.edges[:-1]) / 2
        solver.nodes = solver.centers[:, None] + solver.lengths[:, None] * solver.rule.points / 2
        self.solver, self.state = solver, base.solution['state']
        radius = solver.nodes.ravel()
        shape = loads.rates.shape
        loads.owner.label_order = 28
        fields = {name: np.zeros(len(radius)) for name in ['temporal_square', 'gradient_square', 'source_density', 'velocity']}
        temporal_rows, velocity_rows = [], []
        stored_bytes = 0
        for start in range(0, len(radius), 32):
            if perf_counter() > deadline:
                raise RuntimeError('Saved boundary during sparse radial velocity response')
            section = slice(start, min(start + 32, len(radius)))
            density = IndexedP2Density(loads.material, radius[section])
            density.update(loads.rates)
            for name in fields:
                fields[name][section] = getattr(density, name)
            temporal = temporal_values(density, loads.rates)
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
                raise RuntimeError('Sparse velocity-response storage exceeds declared 1.5 GiB budget')
            if start % 4096 == 0:
                progress('velocity-response-radius-' + str(start) + '-of-' + str(len(radius)))
        self.temporal = vstack(temporal_rows, format='csr')
        self.velocity = vstack(velocity_rows, format='csr')
        self.stored_bytes = stored_bytes
        fields['gram'] = {extension: loads.gram_density(radius, extension)}
        solver.fields = fields
        self.base_constraint_residual = float(np.max(abs(solver.residual(self.state, extension))))
        self.calls, self.residuals = 0, []

    def apply(self, acceleration):
        if perf_counter() > self.deadline:
            raise RuntimeError('Saved boundary during joint radial response')
        temporal = self.temporal @ acceleration.ravel()
        velocity = self.velocity @ acceleration.ravel()
        forcing = velocity_forcing(self.solver, self.state, temporal, velocity)
        tangent, residual, history = solve_tangent(self.solver, self.state, self.extension, forcing)
        self.calls += 1
        self.residuals.append(residual)
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
        return MetricResponse(self.solver, dict(state=tangent, rhs_coefficients=coefficients,
            primitives=primitives, left=left), forcing, residual, history)


class MetricResponse:
    def __init__(self, solver, solution, forcing, residual, history):
        self.solver, self.solution = solver, solution
        self.forcing, self.residual, self.history = forcing, residual, history

    def values(self, radius):
        return self.solver.values(self.solution, radius)[0]


class MomentumMetricResponse:
    def __init__(self, action, deadline, progress):
        self.action, self.shape, self.deadline = action, (len(action.source), len(action.knots) + 1), deadline
        self.rows = []
        points, weights = np.polynomial.legendre.leggauss(48)
        points, weights = points / 2, weights / 2
        weights *= 6 * (points + .5) * (.5 - points)
        for index, (label, weight) in enumerate(zip(points, weights)):
            if perf_counter() > deadline:
                raise RuntimeError('Saved boundary during momentum metric response cache')
            row = samples(action, label, 12)
            geometry, quadrature = row['geometry'], row['quadrature']
            source, velocity = row['source'], row['velocity']
            metric_values = action.solver.values(action.solution, np.array([source]))[0][:, 0]
            lapse, metric = np.exp(metric_values[1]), 1 - 2 * metric_values[0] / source
            clock_square = lapse**2 - velocity**2 / metric
            dust_momentum = action.owner.source_mass * velocity / (metric * np.sqrt(clock_square))
            self.rows.append(dict(radius=geometry['radius'], metric=geometry['metric'], lapse=geometry['lapse'],
                weighted_momentum=quadrature['measure'] * geometry['kinetic'] * row['temporal'],
                indices=quadrature['indices'], shape=row['shape'], motion=row['motion'], cardinal=row['cardinal'],
                source=source, source_radius=np.array([source]), velocity=velocity, source_lapse=lapse, source_metric=metric, weight=weight,
                dust_momentum=dust_momentum, dust_mass_partial=dust_momentum * (2 / (source * metric)
                    + velocity**2 / (source * metric**2 * clock_square)),
                dust_nu_partial=-dust_momentum * lapse**2 / clock_square))
            if index % 16 == 15:
                progress('momentum-response-label-' + str(index + 1))

    def accumulate(self, evaluator, complex_step=None):
        result = np.zeros(self.shape, dtype=complex if complex_step is not None else float)
        for row in self.rows:
            if perf_counter() > self.deadline:
                raise RuntimeError('Saved boundary in joint momentum response')
            variation = evaluator(row['radius'])
            source_variation = evaluator(row['source_radius'])[:, 0]
            if complex_step is None:
                wave = row['weighted_momentum'] * (variation[0] / (row['radius'] * row['metric']) - variation[1])
                dust = row['dust_mass_partial'] * source_variation[0] + row['dust_nu_partial'] * source_variation[1]
            else:
                amount = 1j * complex_step
                metric = row['metric'] - 2 * amount * variation[0] / row['radius']
                wave = row['weighted_momentum'] * np.exp(-amount * variation[1]) * np.sqrt(row['metric'] / metric)
                source_metric = row['source_metric'] - 2 * amount * source_variation[0] / row['source']
                source_lapse = row['source_lapse'] * np.exp(amount * source_variation[1])
                dust = self.action.owner.source_mass * row['velocity'] / (source_metric * np.sqrt(source_lapse**2 - row['velocity']**2 / source_metric))
            field = np.zeros(self.shape[1] - 1, dtype=result.dtype)
            np.add.at(field, row['indices'].ravel(), (wave[:, None] * row['shape']).ravel())
            source = wave @ row['motion'] + dust
            result += row['weight'] * np.outer(row['cardinal'], np.r_[field, source])
        return result if complex_step is None else result.imag / complex_step

    def base_momentum(self):
        result = np.zeros(self.shape)
        for row in self.rows:
            field = np.zeros(self.shape[1] - 1)
            np.add.at(field, row['indices'].ravel(), (row['weighted_momentum'][:, None] * row['shape']).ravel())
            source = row['weighted_momentum'] @ row['motion'] + row['dust_momentum']
            result += row['weight'] * np.outer(row['cardinal'], np.r_[field, source])
        return result


def joint_iteration(system, response, momentum_response, coordinate_momentum_rate, record):
    inverse, matrix = system['inverse'], system['matrix']
    rhs = system['force'] - system['convection'][-1] - coordinate_momentum_rate
    acceleration = inverse.solve(rhs.ravel()).reshape(rhs.shape)
    scale = max(inverse.residual_norm(rhs), 1e-30)
    history = []
    for index in range(24):
        metric_response = response.apply(acceleration)
        coupling = momentum_response.accumulate(metric_response.values)
        residual = (matrix @ acceleration.ravel()).reshape(rhs.shape) + coupling - rhs
        correction = inverse.solve(residual.ravel()).reshape(rhs.shape)
        row = dict(iteration=index, relative_residual=inverse.residual_norm(residual) / scale,
            maximum_residual=float(np.max(abs(residual))), maximum_correction=float(np.max(abs(correction))),
            radial_linear_residual=metric_response.residual)
        row['residual_ratio'] = None if not history else row['relative_residual'] / max(history[-1]['relative_residual'], 1e-300)
        history.append(row)
        record(row, acceleration, coupling, residual, metric_response)
        if row['relative_residual'] <= 2e-11 and row['maximum_correction'] <= 2e-12:
            return acceleration, metric_response, coupling, rhs, history
        if index >= 2 and row['relative_residual'] > 1.25 * history[-2]['relative_residual']:
            raise RuntimeError('Joint first tangent lost contraction; retain saved iterate')
        acceleration -= correction
    raise RuntimeError('Joint first tangent did not reach declared stopping gates')
