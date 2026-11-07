import numpy as np
from scipy.linalg import solve_banded
from scipy.sparse import csr_matrix
from annular_covariant_cut_action_v2_20260915 import CurvedCutAction
from annular_moving_collar_sparse_20260914 import sparse_factors


class SparseRepairedCut(CurvedCutAction):
    def __init__(self, count=17, gram=True, order=8, background_mass=None):
        self.radii = np.linspace(5.2, 6.8, count)
        self.count, self.gram = count, gram
        self.spacing = self.radii[1]-self.radii[0]
        self.source_mass, self.stationary = .03, False
        self.background_mass = background_mass
        points, weights = np.polynomial.legendre.leggauss(order)
        self.fractions, self.weights = (points+1)/2, weights/2
        if gram:
            factors, sampling = sparse_factors(count, True)
            self.original = factors[count-1:].tocsr()
            self.sampling = sampling[count-1:].tocsr()
        else:
            self.original = csr_matrix((0, count))
            self.sampling = csr_matrix((0, count))

    def metric(self, time, radius):
        if self.background_mass is None:
            return super().metric(time, radius)
        root = np.sqrt(1-2*self.background_mass/np.asarray(radius))
        return root, root

    def features(self, radius, position):
        radius = np.asarray(radius)
        cell = np.clip(np.searchsorted(self.radii, radius.real, side='right')-1, 0, self.count-2)
        source_cell = np.searchsorted(self.radii, position.real)-1
        dtype = np.result_type(radius, position, float)
        fraction = (radius-self.radii[cell])/self.spacing
        shape = np.column_stack([1-fraction, fraction]).astype(dtype)
        radial = np.tile([-1/self.spacing, 1/self.spacing], (len(radius), 1)).astype(dtype)
        motion = np.zeros_like(shape)
        cut = cell == source_cell
        left = cut & (radius.real < position.real)
        right = cut & (~left)
        shape[cut], radial[cut] = 0., 0.
        left_length = position-self.radii[source_cell]
        right_length = self.radii[source_cell+1]-position
        shape[left, 0] = (position-radius[left])/left_length
        radial[left, 0] = -1/left_length
        motion[left, 0] = (radius[left]-self.radii[source_cell])/left_length**2
        shape[right, 1] = (radius[right]-position)/right_length
        radial[right, 1] = 1/right_length
        motion[right, 1] = (radius[right]-self.radii[source_cell+1])/right_length**2
        return cell, shape, radial, motion

    def assemble(self, cell, values):
        result = np.zeros(self.count, dtype=values.dtype)
        np.add.at(result, cell, values[:, 0])
        np.add.at(result, cell+1, values[:, 1])
        return result

    def gram_data(self, position, scalar):
        cell = np.searchsorted(self.radii, position.real)-1
        jump = np.zeros(self.count, dtype=np.result_type(position, scalar, float))
        jump[cell] = 1/(position-self.radii[cell])
        jump[cell+1] = 1/(self.radii[cell+1]-position)
        hinge = np.where(self.radii > position.real, self.radii-position, 0.)
        lifted_hinge = self.original @ hinge
        factors = self.original @ scalar-lifted_hinge*(jump @ scalar)
        return factors, lifted_hinge, jump

    def evaluate(self, time, coordinates, rates, pulled=None):
        if pulled is not None:
            raise ValueError('Sparse qualification is P=0 with a supplied metric provider, not an arbitrary pulled shift.')
        dtype = np.result_type(time, coordinates, rates, float)
        coordinates, rates = np.asarray(coordinates, dtype=dtype), np.asarray(rates, dtype=dtype)
        scalar, position = coordinates[:-1], coordinates[-1]
        scalar_rate, velocity = rates[:-1], rates[-1]
        radius, weights = self.mesh(position)
        cell, shape, radial, motion = self.features(radius, position)
        values = np.column_stack([scalar[cell], scalar[cell+1]])
        velocities = np.column_stack([scalar_rate[cell], scalar_rate[cell+1]])
        field_motion = np.sum(motion*values, axis=1)
        temporal = np.sum(shape*velocities, axis=1)+velocity*field_motion
        gradient = np.sum(radial*values, axis=1)
        coefficient = self.coefficient(time, radius)
        temporal_weight = weights*radius**4/coefficient
        kinetic = np.dot(temporal_weight, temporal**2)/2
        potential = np.dot(weights*coefficient, gradient**2)/2
        factor, lifted_hinge, jump = self.gram_data(position, scalar)
        nodal = self.coefficient(time, self.radii)
        factor_coefficient = self.sampling @ nodal
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
        covector = self.assemble(cell, velocity*motion*(temporal_weight*temporal)[:, None]-radial*(weights*coefficient*gradient)[:, None])
        weighted_factor = factor_coefficient*factor/self.spacing
        covector -= self.original.T @ weighted_factor-jump*np.dot(lifted_hinge, weighted_factor)
        return dict(action=kinetic-potential-self.source_mass*clock, wave_action=kinetic-potential,
                    kinetic=kinetic, potential=potential, clock=clock, momenta=momenta,
                    field_momenta=np.append(field_momenta, source_field_momentum), material_momentum=material_momentum,
                    scalar_covector=covector, mass_bands=bands, cross=cross, source_inertia=source_inertia,
                    radius=radius, weight=weights, coefficient=coefficient, nodal=nodal,
                    field_time=temporal, field_radial=gradient,
                    density_dual=-(radius**4*temporal**2/coefficient**2+gradient**2)/2,
                    nodal_dual=-self.sampling.T @ factor**2/(2*self.spacing))

    def acceleration(self, time, coordinates, rates):
        data = self.evaluate(time, coordinates, rates)
        step = 1e-24
        moved = self.evaluate(time+1j*step, coordinates.astype(complex)+1j*step*rates, rates)
        force = np.append(data['scalar_covector'], self.source_covector(time, coordinates, rates))
        right_side = force-moved['momenta'].imag/step
        solved = solve_banded((1, 1), data['mass_bands'], np.column_stack([right_side[:-1], data['cross']]))
        schur = data['source_inertia']-data['cross'] @ solved[:, 1]
        if schur <= 0:
            raise ValueError('Nonpositive coupled velocity Schur complement.')
        source_acceleration = (right_side[-1]-data['cross'] @ solved[:, 0])/schur
        return np.append(solved[:, 0]-solved[:, 1]*source_acceleration, source_acceleration)
