import numpy as np
from annular_gram_joint_action_20260909 import gram_matrices


class CurvedCutAction:
    def __init__(self, count=17, gram=True, order=8, stationary=False):
        self.radii = np.linspace(5.2, 6.8, count)
        self.count = count
        self.spacing = self.radii[1]-self.radii[0]
        self.source_mass = .03
        self.gram = gram
        self.stationary = stationary
        points, weights = np.polynomial.legendre.leggauss(order)
        self.fractions, self.weights = (points+1)/2, weights/2
        self.original, self.sampling = gram_matrices(count)
        if not gram:
            self.original = np.zeros((0, count))
            self.sampling = np.zeros((0, count))

    def metric(self, time, radius):
        effective_time = 0*time if self.stationary else time
        mass = .7+.002*(radius-6)+.001*effective_time
        lapse = .92+.015*(radius-6)+.003*effective_time+.002*effective_time**2
        root = np.sqrt(1-2*mass/radius)
        return lapse, root

    def coefficient(self, time, radius):
        lapse, root = self.metric(time, radius)
        return radius**2*lapse*root

    def mesh(self, position):
        cell = np.searchsorted(self.radii, position.real)-1
        if not 0 <= cell < self.count-1:
            raise ValueError('Source outside mesh.')
        endpoints = np.insert(self.radii.astype(np.result_type(position, float)), cell+1, position)
        lengths = np.diff(endpoints)
        radii = (endpoints[:-1, None]+lengths[:, None]*self.fractions).ravel()
        weights = (lengths[:, None]*self.weights).ravel()
        return radii, weights

    def basis(self, radius, position):
        radius = np.asarray(radius).reshape(-1)
        dtype = np.result_type(radius, position, float)
        cell = np.searchsorted(self.radii, radius.real, side='right')-1
        cell = np.clip(cell, 0, self.count-2)
        source_cell = np.searchsorted(self.radii, position.real)-1
        if not 0 <= source_cell < self.count-1:
            raise ValueError('Source outside mesh.')
        shape = np.zeros((len(radius), self.count), dtype=dtype)
        radial = np.zeros_like(shape)
        motion = np.zeros_like(shape)
        rows = np.arange(len(radius))
        fraction = (radius-self.radii[cell])/self.spacing
        shape[rows, cell], shape[rows, cell+1] = 1-fraction, fraction
        radial[rows, cell], radial[rows, cell+1] = -1/self.spacing, 1/self.spacing
        left = (cell == source_cell) & (radius.real < position.real)
        right = (cell == source_cell) & (~left)
        shape[left | right], radial[left | right] = 0, 0
        left_length = position-self.radii[source_cell]
        right_length = self.radii[source_cell+1]-position
        shape[left, source_cell] = (position-radius[left])/left_length
        radial[left, source_cell] = -1/left_length
        motion[left, source_cell] = (radius[left]-self.radii[source_cell])/left_length**2
        shape[right, source_cell+1] = (radius[right]-position)/right_length
        radial[right, source_cell+1] = 1/right_length
        motion[right, source_cell+1] = (radius[right]-self.radii[source_cell+1])/right_length**2
        return shape, radial, motion

    def lifted(self, position):
        cell = np.searchsorted(self.radii, position.real)-1
        jump = np.zeros(self.count, dtype=np.result_type(position, float))
        jump[cell] = 1/(position-self.radii[cell])
        jump[cell+1] = 1/(self.radii[cell+1]-position)
        hinge = np.where(self.radii > position.real, self.radii-position, 0.)
        return self.original-np.outer(self.original @ hinge, jump)

    def evaluate(self, time, coordinates, rates, pulled=None):
        scalar, position = coordinates[:-1], coordinates[-1]
        scalar_rate, velocity = rates[:-1], rates[-1]
        radius, weight = self.mesh(position)
        shape, radial, motion = self.basis(radius, position)
        if pulled is None:
            coefficient = self.coefficient(time, radius)
            nodal = self.coefficient(time, self.radii)
            lapse, root = self.metric(time, position)
            shift = 0.
        else:
            coefficient, nodal, lapse, root, shift = pulled
        field_motion = motion @ scalar
        field_time = shape @ scalar_rate+field_motion*velocity
        field_radial = radial @ scalar
        temporal_weight = weight*radius**4/coefficient
        kinetic = np.dot(temporal_weight, field_time**2)/2
        lifted = self.lifted(position)
        factor = lifted @ scalar
        factor_coefficient = self.sampling @ nodal
        stiffness = radial.T @ ((weight*coefficient)[:, None]*radial)
        stiffness += lifted.T @ (factor_coefficient[:, None]*lifted)/self.spacing
        potential = scalar @ stiffness @ scalar/2
        clock = np.sqrt(lapse**2-(velocity+shift)**2/root**2)
        if clock.real <= 0:
            raise ValueError('Source ceased to be timelike.')
        material_momentum = self.source_mass*(velocity+shift)/(root**2*clock)
        features = np.column_stack([shape, field_motion])
        field_momenta = features.T @ (temporal_weight*field_time)
        momenta = field_momenta.copy()
        momenta[-1] += material_momentum
        inertia = features.T @ (temporal_weight[:, None]*features)
        inertia[-1, -1] += self.source_mass*lapse**2/(root**2*clock**3)
        scalar_covector = velocity*(motion.T @ (temporal_weight*field_time))-stiffness @ scalar
        density_dual = -(radius**4*field_time**2/coefficient**2+field_radial**2)/2
        nodal_dual = -self.sampling.T @ (factor**2)/(2*self.spacing)
        return dict(action=kinetic-potential-self.source_mass*clock, wave_action=kinetic-potential,
                    kinetic=kinetic, potential=potential, clock=clock, momenta=momenta,
                    field_momenta=field_momenta, material_momentum=material_momentum,
                    inertia=inertia, scalar_covector=scalar_covector,
                    radius=radius, weight=weight, coefficient=coefficient, nodal=nodal,
                    density_dual=density_dual, nodal_dual=nodal_dual,
                    field_time=field_time, field_radial=field_radial)

    def density_dual_at(self, time, coordinates, rates, radius):
        shape, radial, motion = self.basis(radius, coordinates[-1])
        field_time = shape @ rates[:-1]+(motion @ coordinates[:-1])*rates[-1]
        field_radial = radial @ coordinates[:-1]
        coefficient = self.coefficient(time, radius)
        return -(radius**4*field_time**2/coefficient**2+field_radial**2)/2

    def source_covector(self, time, coordinates, rates, wave=False):
        step = 1e-24
        displaced = coordinates.astype(complex).copy()
        displaced[-1] += 1j*step
        return self.evaluate(time, displaced, rates)['wave_action' if wave else 'action'].imag/step

    def acceleration(self, time, coordinates, rates):
        data = self.evaluate(time, coordinates, rates)
        step = 1e-24
        moved = self.evaluate(time+1j*step, coordinates.astype(complex)+1j*step*rates, rates)
        force = np.concatenate([data['scalar_covector'], [self.source_covector(time, coordinates, rates)]])
        return np.linalg.solve(data['inertia'], force-moved['momenta'].imag/step)

    def rhs(self, time, state):
        coordinates, rates = np.split(state, 2)
        return np.concatenate([rates, self.acceleration(time, coordinates, rates)])


def history(time, radius):
    scalar = .02*(radius-6.03)+.004*np.sin(2*(radius-5))+.007*time*np.cos(radius)+.002*time**2*np.sin(radius)
    rate = .007*np.cos(radius)+.004*time*np.sin(radius)
    acceleration = .004*np.sin(radius)+0*time
    return scalar, rate, acceleration


def source_history(time):
    return 6.03+.03*time+.01*time**2, .03+.02*time, .02+0*time


def history_state(system, time):
    scalar, rate, acceleration = history(time, system.radii)
    position, velocity, source_acceleration = source_history(time)
    return np.append(scalar, position), np.append(rate, velocity), np.append(acceleration, source_acceleration)
