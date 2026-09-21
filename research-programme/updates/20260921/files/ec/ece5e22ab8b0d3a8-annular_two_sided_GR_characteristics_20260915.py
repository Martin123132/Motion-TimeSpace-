import numpy as np
from annular_radiation_benchmark_preparation_20260915 import source_initial, initial_profile


class TwoSidedGRCharacteristics:
    def __init__(self, degree=96, mass=.7, source=.03):
        self.degree, self.count, self.mass, self.source = degree, degree+1, mass, source
        self.inner, self.outer = 5.2, 6.8
        self.coordinate = (1-np.cos(np.pi*np.arange(degree+1)/degree))/2
        barycentric = (-1.)**np.arange(degree+1)
        barycentric[[0, -1]] *= .5
        separation = self.coordinate[:, None]-self.coordinate[None, :]
        np.fill_diagonal(separation, 1.)
        derivative = barycentric[None, :]/barycentric[:, None]/separation
        np.fill_diagonal(derivative, 0.)
        np.fill_diagonal(derivative, -np.sum(derivative, axis=1))
        self.derivative = derivative
        vandermonde = np.polynomial.chebyshev.chebvander(2*self.coordinate-1, degree)
        self.inverse = np.linalg.inv(vandermonde)
        primitive = np.polynomial.chebyshev.chebint(self.inverse, axis=0)
        self.weights = (np.polynomial.chebyshev.chebval(1., primitive)-np.polynomial.chebyshev.chebval(-1., primitive))/2
        initial = source_initial(mass, source)
        radius, unused, unused2 = self.mesh(initial['position'], initial['velocity'])
        fields = []
        for side in [0, 1]:
            unused, gradient, temporal = initial_profile(radius[side], side, mass)
            metric = 1-2*mass/radius[side]
            fields.append(np.stack([temporal+metric*gradient, temporal-metric*gradient]))
        self.initial_state = self.pack(np.array(fields), np.array([initial['position'], initial['momentum'], 0.]))

    def pack(self, fields, source):
        return np.concatenate([fields[:, 0, :-1].ravel(), fields[:, 1, 1:].ravel(), source])

    def mesh(self, position, velocity):
        lengths = np.array([position-self.inner, self.outer-position])
        radii = np.stack([self.inner+lengths[0]*self.coordinate, position+lengths[1]*self.coordinate])
        speeds = np.stack([self.coordinate*velocity, (1-self.coordinate)*velocity])
        return radii, lengths, speeds

    def unpack(self, state):
        position, momentum, proper_time = state[-3:]
        metric = 1-2*self.mass/position
        energy = np.sqrt(self.source**2+metric*momentum**2)
        velocity = metric**1.5*momentum/energy
        fields = np.empty((2, 2, self.count), dtype=state.dtype)
        fields[:, 0, :-1] = state[:2*self.degree].reshape(2, self.degree)
        fields[:, 1, 1:] = state[2*self.degree:4*self.degree].reshape(2, self.degree)
        fields[0, 0, -1] = -(metric-velocity)/(metric+velocity)*fields[0, 1, -1]
        fields[0, 1, 0] = fields[0, 0, 0]
        fields[1, 0, -1] = fields[1, 1, -1]
        fields[1, 1, 0] = -(metric+velocity)/(metric-velocity)*fields[1, 0, 0]
        return fields, position, momentum, velocity

    def source_force(self, fields, position, velocity):
        metric = 1-2*self.mass/position
        gradient_left = (fields[0, 0, -1]-fields[0, 1, -1])/(2*metric)
        gradient_right = (fields[1, 0, 0]-fields[1, 1, 0])/(2*metric)
        pressure_jump = metric*(1-velocity**2/metric**2)*(gradient_left**2-gradient_right**2)/2
        return position**2*pressure_jump

    def rhs(self, time, state):
        fields, position, momentum, velocity = self.unpack(state)
        radii, lengths, speeds = self.mesh(position, velocity)
        metric = 1-2*self.mass/radii
        plus, minus = fields[:, 0], fields[:, 1]
        curvature = metric/radii*(plus-minus)
        plus_rate = (metric+speeds)/lengths[:, None]*(plus @ self.derivative.T)+curvature
        minus_rate = (speeds-metric)/lengths[:, None]*(minus @ self.derivative.T)+curvature
        source_metric = 1-2*self.mass/position
        metric_gradient = 2*self.mass/position**2
        clock = np.sqrt(source_metric-velocity**2/source_metric)
        gravity = -self.source*metric_gradient*(1+velocity**2/source_metric**2)/(2*clock)
        force = self.source_force(fields, position, velocity)
        return self.pack(np.stack([plus_rate, minus_rate], axis=1), np.array([velocity, gravity+force, clock]))

    def energy(self, state):
        fields, position, momentum, velocity = self.unpack(state)
        radii, lengths, unused = self.mesh(position, velocity)
        metric = 1-2*self.mass/radii
        field_energy = np.sum(lengths*(np.sum(fields**2, axis=1)*radii**2/(4*metric) @ self.weights))
        source_metric = 1-2*self.mass/position
        material_energy = np.sqrt(source_metric)*np.sqrt(self.source**2+source_metric*momentum**2)
        return field_energy+material_energy, field_energy

    def sample(self, state, radius):
        fields, position, momentum, velocity = self.unpack(state)
        radius = np.asarray(radius)
        result = np.zeros((2, len(radius)))
        for side in [0, 1]:
            selected = radius < position if side == 0 else radius >= position
            lower, upper = (self.inner, position) if side == 0 else (position, self.outer)
            mapped = 2*(radius[selected]-lower)/(upper-lower)-1
            coefficients = fields[side] @ self.inverse.T
            result[:, selected] = np.polynomial.chebyshev.chebval(mapped, coefficients.T)
        metric = 1-2*self.mass/radius
        return (result[0]+result[1])/2, (result[0]-result[1])/(2*metric)
