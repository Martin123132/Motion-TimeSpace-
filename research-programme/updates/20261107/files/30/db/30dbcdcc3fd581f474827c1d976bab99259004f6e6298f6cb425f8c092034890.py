from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_candidate_canonical_response_20260920 import density_chunks, temporal_values, velocity_design, radial_weights
from time import perf_counter
from scipy.linalg import cholesky_banded, cho_solve_banded, cho_factor, cho_solve
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import LinearOperator, onenormest
import numpy as np


class QuadratureCache:
    def __init__(self, owner, coordinates, solver, deadline, budget=512*1024**2):
        self.owner, self.coordinates, self.solver, self.deadline = owner, coordinates, solver, deadline
        self.radius = solver.nodes.ravel()
        self.packets, self.bytes, self.prefix = [], 0, 0
        for section, density in density_chunks(owner, coordinates, self.radius, solver.label_order, deadline):
            size = sum(value.nbytes for value in density.__dict__.values() if isinstance(value, np.ndarray))
            if self.bytes+size > budget:
                break
            self.packets.append((section, density))
            self.bytes += size
            self.prefix = min(section.stop, len(self.radius))
        self.budget = budget

    def __iter__(self):
        for section, density in self.packets:
            if perf_counter() > self.deadline:
                raise RuntimeError('Safe canonical-inverse wall boundary reached.')
            yield section, density
        if self.prefix < len(self.radius):
            for section, density in density_chunks(self.owner, self.coordinates, self.radius[self.prefix:],
                    self.solver.label_order, self.deadline):
                yield slice(self.prefix+section.start, self.prefix+section.stop), density


class FullMomentumMap:
    def __init__(self, owner, coordinates, solver, cache):
        self.owner, self.coordinates, self.solver, self.cache = owner, coordinates, solver, cache
        self.shape = coordinates.shape
        self.count = coordinates.size
        self.source_indices = np.arange(self.shape[0])*self.shape[1]+self.shape[1]-1
        self.radius = solver.nodes.ravel()
        self.measure = radial_weights(solver)
        self.evaluations = 0

    def density(self, rates):
        temporal_square, velocity = np.zeros(len(self.radius)), np.zeros(len(self.radius))
        for section, density in self.cache:
            temporal = temporal_values(density, rates)
            temporal_square[section] = np.bincount(density.indices,
                weights=density.label_weights*temporal**2, minlength=len(density.radius))
            velocity[section][density.source_selected] = density.source_interpolation @ rates[:, -1]
        return temporal_square, velocity

    def fixed_momentum(self, rates, state, assemble=False):
        mass, log_lapse = state.reshape(2, -1)
        metric, lapse = 1-2*mass/self.radius, np.exp(log_lapse)
        coefficient = self.radius**2/(lapse*np.sqrt(metric))
        result = np.zeros(self.count, dtype=np.result_type(rates, state))
        normal = csr_matrix((self.count, self.count)) if assemble else None
        for section, density in self.cache:
            temporal = temporal_values(density, rates)
            measure = density.label_weights*self.measure[section][density.indices]*coefficient[section][density.indices]
            design = velocity_design(density, *self.shape)
            result += np.asarray(design.T @ (measure*temporal)).ravel()
            if assemble:
                normal = normal+design.T @ design.multiply(measure[:, None])
            selected = density.source_selected
            if np.any(selected):
                interpolation = density.source_interpolation
                velocity = interpolation @ rates[:, -1]
                local_metric, local_lapse = metric[section][selected], lapse[section][selected]
                clock_square = local_lapse**2-velocity**2/local_metric
                if np.min(clock_square.real) <= 0:
                    raise ValueError('Canonical trial left the timelike chart.')
                clock = np.sqrt(clock_square)
                measure = self.measure[section][selected]*density.source_density[selected]
                proper_momentum = self.owner.source_mass*velocity/(local_metric*clock)
                result[self.source_indices] += interpolation.T @ (measure*proper_momentum)
                if assemble:
                    inertia = measure*self.owner.source_mass*local_lapse**2/(local_metric*clock**3)
                    block = interpolation.T @ (inertia[:, None]*interpolation)
                    rows = np.repeat(self.source_indices, self.shape[0])
                    columns = np.tile(self.source_indices, self.shape[0])
                    normal += csr_matrix((block.ravel(), (rows, columns)), shape=(self.count, self.count))
        if assemble:
            normal.eliminate_zeros()
        return result.reshape(self.shape), normal

    def evaluate(self, rates, extension, assemble=False):
        self.evaluations += 1
        temporal, velocity = self.density(rates)
        self.solver.fields['temporal_square'], self.solver.fields['velocity'] = temporal, velocity
        solution = self.solver.solve(extension)
        momentum, normal = self.fixed_momentum(rates, solution['state'], assemble)
        minimum_metric = float(np.min(1-2*solution['state'][0]/self.solver.nodes))
        speed = abs(velocity)/(np.exp(solution['state'][1].ravel())*
            np.sqrt(1-2*solution['state'][0].ravel()/self.radius))
        return dict(momentum=momentum, solution=solution, normal=normal,
            minimum_F=minimum_metric, maximum_speed_ratio=float(max(speed)))


class BandedSourceInverse:
    def __init__(self, matrix, shape):
        labels, components = shape
        self.shape, self.count = shape, labels*components
        self.field_count = labels*(components-1)
        original = np.arange(self.count).reshape(shape)
        self.permutation = np.r_[original[:, :-1].T.ravel(), original[:, -1]]
        self.inverse_permutation = np.argsort(self.permutation)
        raw = matrix.tocsr()
        difference = raw-raw.T
        self.symmetry_error = float(max(abs(difference.data), default=0.)/max(abs(raw.data)))
        if self.symmetry_error > 2e-12:
            raise ValueError('Fixed-metric mass assembly lost reciprocity.')
        self.matrix = ((raw+raw.T)*.5).tocsr()
        ordered = self.matrix[self.permutation][:, self.permutation]
        diagonal = ordered.diagonal()
        if np.min(diagonal) <= 0:
            raise ValueError('Unsampled or nonpositive canonical direction; no modes may be deleted.')
        self.scale = np.sqrt(diagonal)
        self.original_scale = self.scale[self.inverse_permutation]
        self.bandwidth = 3*labels-1
        field = ordered[:self.field_count, :self.field_count].tocoo()
        if np.max(abs(field.row-field.col)) > self.bandwidth:
            raise ValueError('Unexpected field/material mass bandwidth.')
        self.bands = np.zeros((self.bandwidth+1, self.field_count))
        selected = field.row >= field.col
        rows, columns = field.row[selected], field.col[selected]
        self.bands[rows-columns, columns] = field.data[selected]/(self.scale[rows]*self.scale[columns])
        self.factor = cholesky_banded(self.bands, lower=True, check_finite=False)
        cross = ordered[:self.field_count, self.field_count:].toarray()
        self.cross = cross/(self.scale[:self.field_count, None]*self.scale[None, self.field_count:])
        source = ordered[self.field_count:, self.field_count:].toarray()
        self.source = source/(self.scale[self.field_count:, None]*self.scale[None, self.field_count:])
        self.field_cross = cho_solve_banded((self.factor, True), self.cross, check_finite=False)
        self.schur = self.source-self.cross.T @ self.field_cross
        self.schur_symmetry_error = float(np.max(abs(self.schur-self.schur.T)))
        if self.schur_symmetry_error > 2e-12:
            raise ValueError('Source Schur reciprocity failed.')
        self.schur = (self.schur+self.schur.T)/2
        self.source_factor = cho_factor(self.schur, lower=True, check_finite=False)
        self.minimum_field_cholesky_pivot = float(min(self.factor[0]))
        self.minimum_schur_eigenvalue = float(min(np.linalg.eigvalsh(self.schur)))
        self.minimum_diagonal, self.maximum_diagonal = float(min(diagonal)), float(max(diagonal))

    def solve(self, values):
        values = np.asarray(values)
        was_vector = values.ndim == 1
        if was_vector:
            values = values[:, None]
        rhs = values[self.permutation]/self.scale[:, None]
        field = cho_solve_banded((self.factor, True), rhs[:self.field_count], check_finite=False)
        source = cho_solve(self.source_factor, rhs[self.field_count:]-self.cross.T @ field, check_finite=False)
        field -= self.field_cross @ source
        normalized = np.vstack([field, source])/self.scale[:, None]
        result = normalized[self.inverse_permutation]
        return result[:, 0] if was_vector else result

    def condition_estimates(self):
        matrix_norm = float(np.max(np.asarray(abs(self.matrix).sum(axis=0))))
        inverse = LinearOperator((self.count, self.count), matvec=self.solve, rmatvec=self.solve,
            matmat=self.solve, rmatmat=self.solve, dtype=float)
        raw = matrix_norm*float(onenormest(inverse))
        normalized = self.matrix.multiply(1/self.original_scale[:, None]).multiply(1/self.original_scale[None, :]).tocsr()

        def scaled_solve(values):
            if values.ndim == 1:
                return self.original_scale*self.solve(self.original_scale*values)
            return self.original_scale[:, None]*self.solve(self.original_scale[:, None]*values)

        inverse = LinearOperator((self.count, self.count), matvec=scaled_solve, rmatvec=scaled_solve,
            matmat=scaled_solve, rmatmat=scaled_solve, dtype=float)
        scaled = float(np.max(np.asarray(abs(normalized).sum(axis=0))))*float(onenormest(inverse))
        return raw, scaled

    def residual_norm(self, residual):
        return float(np.linalg.norm(np.asarray(residual).ravel()/self.original_scale))


def canonical_inverse(mapping, target, initial, extension, preconditioner, initial_evaluation=None, on_step=None):
    rates = initial.copy()
    current = initial_evaluation if initial_evaluation is not None else mapping.evaluate(rates, extension)
    history, rejected = [], []
    target_scale = max(preconditioner.residual_norm(target), 1e-30)
    for iteration in range(16):
        residual = current['momentum']-target
        norm = preconditioner.residual_norm(residual)
        step = preconditioner.solve(residual.ravel()).reshape(rates.shape)
        row = dict(iteration=iteration, momentum_relative_residual=norm/target_scale,
            momentum_maximum_residual=float(np.max(abs(residual))),
            maximum_preconditioned_correction=float(np.max(abs(step))),
            radial_residual=current['solution']['maximum_residual'],
            minimum_F=current['minimum_F'], maximum_speed_ratio=current['maximum_speed_ratio'])
        history.append(row)
        if on_step:
            on_step(row)
        if norm/target_scale < 2e-11 and np.max(abs(step)) < 2e-10:
            return rates, current, history, rejected
        damping = 1.
        for backtrack in range(9):
            trial = rates-damping*step
            try:
                evaluated = mapping.evaluate(trial, extension)
                trial_norm = preconditioner.residual_norm(evaluated['momentum']-target)
                accepted = trial_norm < norm
                reason = 'nondecreasing_residual'
            except ValueError as error:
                accepted = False
                reason = repr(error)
            if accepted:
                rates, current = trial, evaluated
                row['accepted_damping'] = damping
                break
            rejected.append(dict(iteration=iteration, damping=damping, reason=reason))
            damping /= 2
        else:
            raise RuntimeError('Full canonical inverse failed descent; saved iterate evidence retained.')
    raise RuntimeError('Full canonical inverse did not meet both unchanged stopping gates.')

