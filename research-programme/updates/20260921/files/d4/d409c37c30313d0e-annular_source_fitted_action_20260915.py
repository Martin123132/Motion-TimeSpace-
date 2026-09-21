import numpy as np
from annular_sparse_repaired_cut_20260915 import SparseRepairedCut


class SourceFittedAction(SparseRepairedCut):
    def __init__(self, count=17, gram=True, order=10, background_mass=.7, anchor=6.03):
        super().__init__(count, gram, order, background_mass)
        self.anchor = float(anchor)
        if not self.radii[0] < self.anchor < self.radii[-1]:
            raise ValueError('Reference source must be interior.')
        if np.min(abs(self.radii-self.anchor)) < 1e-12:
            raise ValueError('Reference anchor must lie strictly inside its reference cell.')
        self.reference_radius, self.reference_weight = super().mesh(self.anchor)
        self.reference_cell, self.reference_shape, self.reference_radial, unused = super().features(self.reference_radius, self.anchor)

    def mapping(self, reference, position):
        reference = np.asarray(reference)
        inner, outer = self.radii[[0, -1]]
        if not inner < np.real(position) < outer:
            raise ValueError('Source reached a physical endpoint; pullback no longer invertible.')
        left = reference.real < self.anchor
        jacobian = np.where(left, (position-inner)/(self.anchor-inner), (outer-position)/(outer-self.anchor))
        displacement = np.where(left, (reference-inner)/(self.anchor-inner), (outer-reference)/(outer-self.anchor))
        physical = reference+displacement*(position-self.anchor)
        return physical, jacobian, displacement

    def evaluate(self, time, coordinates, rates, pulled=None):
        if pulled is not None:
            raise ValueError('This qualification uses a prescribed metric, not an unvaried live-geometry substitution.')
        dtype = np.result_type(time, coordinates, rates, float)
        coordinates, rates = np.asarray(coordinates, dtype=dtype), np.asarray(rates, dtype=dtype)
        scalar, position = coordinates[:-1], coordinates[-1]
        scalar_rate, velocity = rates[:-1], rates[-1]
        radius, jacobian, displacement = self.mapping(self.reference_radius, position)
        weights = self.reference_weight
        cell, shape, radial = self.reference_cell, self.reference_shape, self.reference_radial
        motion = -displacement[:, None]*radial/jacobian[:, None]
        values = np.column_stack([scalar[cell], scalar[cell+1]])
        velocities = np.column_stack([scalar_rate[cell], scalar_rate[cell+1]])
        field_motion = np.sum(motion*values, axis=1)
        temporal = np.sum(shape*velocities, axis=1)+velocity*field_motion
        reference_gradient = np.sum(radial*values, axis=1)
        gradient = reference_gradient/jacobian
        coefficient = self.coefficient(time, radius)
        temporal_weight = weights*jacobian*radius**4/coefficient
        spatial_weight = weights*coefficient/jacobian
        kinetic = np.dot(temporal_weight, temporal**2)/2
        potential = np.dot(spatial_weight, reference_gradient**2)/2
        factor, lifted_hinge, jump = self.gram_data(self.anchor, scalar)
        nodal_radius, nodal_jacobian, unused = self.mapping(self.radii, position)
        nodal = self.coefficient(time, nodal_radius)
        factor_coefficient = self.sampling @ (nodal/nodal_jacobian)
        potential += np.dot(factor_coefficient, factor**2)/(2*self.spacing)
        lapse, root = self.metric(time, position)
        clock_squared = lapse**2-velocity**2/root**2
        if clock_squared.real <= 0:
            raise ValueError('Source left the timelike branch.')
        clock = np.sqrt(clock_squared)
        material_momentum = self.source_mass*velocity/(root**2*clock)
        field_momenta = self.assemble(cell, shape*(temporal_weight*temporal)[:, None])
        source_field_momentum = np.dot(temporal_weight, temporal*field_motion)
        momenta = np.append(field_momenta, source_field_momentum+material_momentum)
        diagonal = self.assemble(cell, temporal_weight[:, None]*shape**2)
        off_diagonal = np.zeros(self.count-1, dtype=diagonal.dtype)
        np.add.at(off_diagonal, cell, temporal_weight*shape[:, 0]*shape[:, 1])
        bands = np.zeros((3, self.count), dtype=diagonal.dtype)
        bands[1] = diagonal
        bands[0, 1:], bands[2, :-1] = off_diagonal, off_diagonal
        cross = self.assemble(cell, shape*(temporal_weight*field_motion)[:, None])
        source_inertia = np.dot(temporal_weight, field_motion**2)+self.source_mass*lapse**2/(root**2*clock**3)
        covector = self.assemble(cell, velocity*motion*(temporal_weight*temporal)[:, None]-radial*(spatial_weight*reference_gradient)[:, None])
        weighted_factor = factor_coefficient*factor/self.spacing
        covector -= self.original.T @ weighted_factor-jump*np.dot(lifted_hinge, weighted_factor)
        return dict(action=kinetic-potential-self.source_mass*clock, wave_action=kinetic-potential,
                    kinetic=kinetic, potential=potential, clock=clock, momenta=momenta,
                    field_momenta=np.append(field_momenta, source_field_momentum), material_momentum=material_momentum,
                    scalar_covector=covector, mass_bands=bands, cross=cross, source_inertia=source_inertia,
                    radius=radius, weight=weights*jacobian, coefficient=coefficient, nodal=nodal,
                    field_time=temporal, field_radial=gradient, jacobian=jacobian,
                    density_dual=-(radius**4*temporal**2/coefficient**2+gradient**2)/2,
                    nodal_dual=-(self.sampling.T @ factor**2)/(2*self.spacing*nodal_jacobian))

    def energy(self, time, coordinates, rates):
        data = self.evaluate(time, coordinates, rates)
        return np.dot(data['momenta'], rates)-data['action']

    def sample(self, reference, coordinates, rates):
        radius, jacobian, displacement = self.mapping(reference, coordinates[-1])
        cell, shape, radial, unused = super().features(np.asarray(reference), self.anchor)
        values = np.column_stack([coordinates[cell], coordinates[cell+1]])
        velocities = np.column_stack([rates[cell], rates[cell+1]])
        scalar = np.sum(shape*values, axis=1)
        gradient = np.sum(radial*values, axis=1)/jacobian
        temporal = np.sum(shape*velocities, axis=1)-displacement*rates[-1]*gradient
        return radius, scalar, temporal, gradient
