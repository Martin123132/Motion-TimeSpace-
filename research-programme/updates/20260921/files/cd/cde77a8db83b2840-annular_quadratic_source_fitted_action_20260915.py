import numpy as np
from scipy.linalg import solve_banded
from scipy.sparse import coo_matrix, csr_matrix
from annular_source_fitted_action_20260915 import SourceFittedAction


class QuadraticSourceFittedAction(SourceFittedAction):
    def __init__(self, base_count=17, gram=True, order=10, background_mass=.7, anchor=6.03):
        linear = SourceFittedAction(base_count, gram, order, background_mass, anchor)
        self.base_count, self.base_radii = base_count, linear.radii.copy()
        self.anchor, self.background_mass, self.gram = anchor, background_mass, gram
        self.source_mass, self.stationary = linear.source_mass, False
        self.gram_spacing, self.spacing = linear.spacing, linear.spacing/2
        self.fractions, self.weights = linear.fractions, linear.weights
        self.edges = np.sort(np.append(self.base_radii, anchor))
        full_nodes = np.sort(np.concatenate([self.edges, (self.edges[:-1]+self.edges[1:])/2]))
        free = full_nodes != anchor
        self.radii, self.count = full_nodes[free], int(np.sum(free))
        full_to_free = np.full(len(full_nodes), -1, dtype=int)
        full_to_free[free] = np.arange(self.count)
        element_nodes = np.column_stack([np.arange(0, len(full_nodes)-2, 2), np.arange(1, len(full_nodes)-1, 2), np.arange(2, len(full_nodes), 2)])
        self.element_indices = full_to_free[element_nodes]
        lengths = np.diff(self.edges)
        self.reference_radius = (self.edges[:-1, None]+lengths[:, None]*self.fractions).ravel()
        self.reference_weight = (lengths[:, None]*self.weights).ravel()
        self.reference_indices, self.reference_shape, self.reference_radial = self.features_quadratic(self.reference_radius)
        vertex_indices = np.searchsorted(self.radii, self.base_radii)
        original = linear.original.tocoo()
        sampling = linear.sampling.tocoo()
        self.original = coo_matrix((original.data, (original.row, vertex_indices[original.col])), shape=(original.shape[0], self.count)).tocsr()
        self.sampling = coo_matrix((sampling.data, (sampling.row, vertex_indices[sampling.col])), shape=(sampling.shape[0], self.count)).tocsr()
        self.jump = np.zeros(self.count)
        source_edge = np.searchsorted(self.edges, anchor)
        for element, local, sign in [(source_edge-1, np.array([1., -4., 3.]), -1.), (source_edge, np.array([-3., 4., -1.]), 1.)]:
            indices = self.element_indices[element]
            valid = indices >= 0
            np.add.at(self.jump, indices[valid], sign*local[valid]/lengths[element])
        hinge = np.maximum(self.radii-anchor, 0.)
        self.lifted_hinge = self.original @ hinge
        self.lifted = self.original-csr_matrix(self.lifted_hinge[:, None]) @ csr_matrix(self.jump[None, :])
        cells, shapes, unused, unused2 = linear.features(self.radii, anchor)
        rows = np.repeat(np.arange(self.count), 2)
        columns = np.column_stack([cells, cells+1]).ravel()
        self.linear_embedding = coo_matrix((shapes.ravel(), (rows, columns)), shape=(self.count, base_count)).tocsr()

    def features_quadratic(self, reference):
        reference = np.asarray(reference)
        element = np.clip(np.searchsorted(self.edges, reference.real, side='right')-1, 0, len(self.edges)-2)
        length = self.edges[element+1]-self.edges[element]
        fraction = (reference-self.edges[element])/length
        shape = np.column_stack([(1-fraction)*(1-2*fraction), 4*fraction*(1-fraction), fraction*(2*fraction-1)])
        radial = np.column_stack([4*fraction-3, 4-8*fraction, 4*fraction-1])/length[:, None]
        indices = self.element_indices[element]
        valid = indices >= 0
        return np.maximum(indices, 0), shape*valid, radial*valid

    def assemble_quadratic(self, indices, values):
        result = np.zeros(self.count, dtype=values.dtype)
        np.add.at(result, indices.ravel(), values.ravel())
        return result

    def gram_data(self, position, scalar):
        if abs(position-self.anchor) > 1e-12:
            raise ValueError('The reference lift is anchored; physical b belongs only in the map.')
        return self.lifted @ scalar, self.lifted_hinge, self.jump

    def evaluate(self, time, coordinates, rates, pulled=None):
        if pulled is not None:
            raise ValueError('Live metric substitution requires a separately qualified coupled implementation.')
        dtype = np.result_type(time, coordinates, rates, float)
        coordinates, rates = np.asarray(coordinates, dtype=dtype), np.asarray(rates, dtype=dtype)
        scalar, position, velocity = coordinates[:-1], coordinates[-1], rates[-1]
        radius, jacobian, displacement = self.mapping(self.reference_radius, position)
        indices, shape, radial = self.reference_indices, self.reference_shape, self.reference_radial
        motion = -displacement[:, None]*radial/jacobian[:, None]
        field_motion = np.sum(motion*scalar[indices], axis=1)
        temporal = np.sum(shape*rates[:-1][indices], axis=1)+velocity*field_motion
        reference_gradient = np.sum(radial*scalar[indices], axis=1)
        gradient = reference_gradient/jacobian
        coefficient = self.coefficient(time, radius)
        temporal_weight = self.reference_weight*jacobian*radius**4/coefficient
        spatial_weight = self.reference_weight*coefficient/jacobian
        kinetic = np.dot(temporal_weight, temporal**2)/2
        factor = self.lifted @ scalar
        nodal_radius, nodal_jacobian, unused = self.mapping(self.radii, position)
        nodal = self.coefficient(time, nodal_radius)
        factor_coefficient = self.sampling @ (nodal/nodal_jacobian)
        potential = np.dot(spatial_weight, reference_gradient**2)/2+np.dot(factor_coefficient, factor**2)/(2*self.gram_spacing)
        lapse, root = self.metric(time, position)
        clock_squared = lapse**2-velocity**2/root**2
        if clock_squared.real <= 0:
            raise ValueError('Source left the timelike branch.')
        clock = np.sqrt(clock_squared)
        material_momentum = self.source_mass*velocity/(root**2*clock)
        field_momenta = self.assemble_quadratic(indices, shape*(temporal_weight*temporal)[:, None])
        source_field_momentum = np.dot(temporal_weight, temporal*field_motion)
        bands = np.zeros((5, self.count), dtype=dtype)
        for first in range(3):
            for second in range(3):
                selected = (shape[:, first] != 0) & (shape[:, second] != 0)
                row, column = indices[selected, first], indices[selected, second]
                values = temporal_weight[selected]*shape[selected, first]*shape[selected, second]
                np.add.at(bands, (2+row-column, column), values)
        cross = self.assemble_quadratic(indices, shape*(temporal_weight*field_motion)[:, None])
        source_inertia = np.dot(temporal_weight, field_motion**2)+self.source_mass*lapse**2/(root**2*clock**3)
        covector = self.assemble_quadratic(indices, velocity*motion*(temporal_weight*temporal)[:, None]-radial*(spatial_weight*reference_gradient)[:, None])
        covector -= self.lifted.T @ (factor_coefficient*factor/self.gram_spacing)
        return dict(action=kinetic-potential-self.source_mass*clock, wave_action=kinetic-potential,
            kinetic=kinetic, potential=potential, clock=clock, momenta=np.append(field_momenta, source_field_momentum+material_momentum),
            field_momenta=np.append(field_momenta, source_field_momentum), material_momentum=material_momentum,
            scalar_covector=covector, mass_bands=bands, cross=cross, source_inertia=source_inertia,
            radius=radius, weight=self.reference_weight*jacobian, coefficient=coefficient, nodal=nodal,
            field_time=temporal, field_radial=gradient, jacobian=jacobian,
            density_dual=-(radius**4*temporal**2/coefficient**2+gradient**2)/2,
            nodal_dual=-(self.sampling.T @ factor**2)/(2*self.gram_spacing*nodal_jacobian))

    def acceleration(self, time, coordinates, rates):
        data = self.evaluate(time, coordinates, rates)
        step = 1e-24
        moved = self.evaluate(time+1j*step, coordinates.astype(complex)+1j*step*rates, rates)
        force = np.append(data['scalar_covector'], self.source_covector(time, coordinates, rates))
        right_side = force-moved['momenta'].imag/step
        solved = solve_banded((2, 2), data['mass_bands'], np.column_stack([right_side[:-1], data['cross']]))
        schur = data['source_inertia']-data['cross'] @ solved[:, 1]
        if schur <= 0:
            raise ValueError('Nonpositive coupled velocity Schur complement.')
        source_acceleration = (right_side[-1]-data['cross'] @ solved[:, 0])/schur
        return np.append(solved[:, 0]-solved[:, 1]*source_acceleration, source_acceleration)

    def sample(self, reference, coordinates, rates):
        radius, jacobian, displacement = self.mapping(reference, coordinates[-1])
        indices, shape, radial = self.features_quadratic(reference)
        scalar = np.sum(shape*coordinates[:-1][indices], axis=1)
        gradient = np.sum(radial*coordinates[:-1][indices], axis=1)/jacobian
        temporal = np.sum(shape*rates[:-1][indices], axis=1)-displacement*rates[-1]*gradient
        return radius, scalar, temporal, gradient
