import numpy as np
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule


def weight(labels):
    return 6*(labels+.5)*(.5-labels)


def prepared_gradient(offset):
    distance = abs(offset)
    fraction = np.clip((distance-.2)/.35, 0., 1.)
    envelope = 1-10*fraction**3+15*fraction**4-6*fraction**5
    envelope_gradient = (-30*fraction**2+60*fraction**3-30*fraction**4)*np.sign(offset)/.35
    return .01*(envelope+offset*envelope_gradient)


class ContinuumMaterial:
    def __init__(self, owner, source):
        self.owner, self.source = owner, source
        self.coefficients = owner.layer_rule.inverse @ source
        self.jacobian_coefficients = 2*np.polynomial.chebyshev.chebder(self.coefficients[:, 0])
        self.minimum_jacobian = float(np.min(self.jacobian(np.linspace(-.5, .5, 101))))
        if self.minimum_jacobian <= 0:
            raise ValueError('Continuum material map lost ordering.')

    def interpolation(self, labels):
        return np.polynomial.chebyshev.chebvander(2*np.asarray(labels), self.owner.layer_degree) @ self.owner.layer_rule.inverse

    def values(self, labels):
        return self.interpolation(labels) @ self.source

    def jacobian(self, labels):
        return np.polynomial.chebyshev.chebval(2*np.asarray(labels), self.jacobian_coefficients)

    def inverse(self, radius):
        lower, upper = self.source[[0, -1], 0]
        labels = (np.asarray(radius)-lower)/(upper-lower)-.5
        for unused in range(8):
            labels -= (np.polynomial.chebyshev.chebval(2*labels, self.coefficients[:, 0])-radius)/self.jacobian(labels)
        return labels


class ContinuumDensity:
    def __init__(self, material, radius, order=None):
        self.material, self.radius = material, np.asarray(radius).reshape(-1)
        owner = material.owner
        points, weights = np.polynomial.legendre.leggauss(order or owner.label_order)
        labels, label_weights, indices = [], [], []
        source_low, source_high = material.source[[0, -1], 0]
        for index, target in enumerate(self.radius):
            cuts = np.array([(target-owner.inner)/owner.width, (target-owner.outer)/owner.width])
            cuts = cuts[(cuts > -.5) & (cuts < .5)]
            if source_low < target < source_high:
                cuts = np.append(cuts, material.inverse(target))
            cuts = np.unique(np.concatenate([[-.5], cuts, [.5]]))
            for lower, upper in zip(cuts[:-1], cuts[1:]):
                local = (lower+upper)/2+(upper-lower)*points/2
                labels.extend(local)
                label_weights.extend((upper-lower)*weights*weight(local)/2)
                indices.extend([index]*len(points))
        self.labels = np.asarray(labels)
        self.weights, self.indices = np.asarray(label_weights), np.asarray(indices)
        targets = self.radius[self.indices]
        sources = material.values(self.labels)[:, 0]
        inner, outer = owner.inner+owner.width*self.labels, owner.outer+owner.width*self.labels
        self.operators, self.selected = [], []
        for side in [0, 1]:
            selected = (targets >= inner) & (targets <= outer) & ((targets < sources) if side == 0 else (targets >= sources))
            lower, upper = (inner, sources) if side == 0 else (sources, outer)
            mapped = 2*(targets[selected]-lower[selected])/(upper[selected]-lower[selected])-1
            label_interpolation = material.interpolation(self.labels[selected])
            spatial_interpolation = np.polynomial.chebyshev.chebvander(mapped, owner.degree) @ owner.spatial_rule.inverse
            self.operators.append((label_interpolation[:, :, None]*spatial_interpolation[:, None, :]).reshape(np.sum(selected), -1))
            self.selected.append(selected)
        self.source_density, self.source_momentum = np.zeros(len(self.radius)), np.zeros(len(self.radius))
        selected = (self.radius >= source_low) & (self.radius <= source_high)
        labels = material.inverse(self.radius[selected])
        self.source_density[selected] = weight(labels)/material.jacobian(labels)
        self.source_momentum[selected] = material.values(labels)[:, 1]

    def update(self, fields):
        plus, minus = np.zeros(len(self.labels)), np.zeros(len(self.labels))
        for side in [0, 1]:
            plus[self.selected[side]] = self.operators[side] @ fields[:, side, 0].ravel()
            minus[self.selected[side]] = self.operators[side] @ fields[:, side, 1].ravel()
        self.square = np.bincount(self.indices, weights=self.weights*(plus**2+minus**2)/2, minlength=len(self.radius))
        self.cross = np.bincount(self.indices, weights=self.weights*(plus**2-minus**2)/4, minlength=len(self.radius))

    def radial(self, mass):
        owner, radius = self.material.owner, self.radius
        root_square = 1-2*mass/radius
        if np.min(root_square) <= 0:
            raise ValueError('Continuum oracle reached trapped polar coordinates.')
        root = np.sqrt(root_square)
        energy = np.sqrt(owner.source_mass**2+root_square*self.source_momentum**2)
        mass_radial = owner.coupling*(radius**2*root_square*self.square/2+root*energy*self.source_density)
        log_lapse_radial = mass/(radius**2*root_square)+owner.coupling*radius*self.square/2
        log_lapse_radial += owner.coupling*root*self.source_momentum**2*self.source_density/(radius*energy)
        return mass_radial, log_lapse_radial


class ContinuumGeometry:
    def __init__(self, owner, material, free_fields):
        self.owner, self.material, self.rule = owner, material, owner.radial_rule
        outer_edges = np.array([owner.inner-owner.width/2, owner.inner+owner.width/2, owner.outer-owner.width/2, owner.outer+owner.width/2])
        fixed = np.arange(owner.inner+.05, owner.outer, owner.radial_spacing)
        self.edges = np.unique(np.concatenate([outer_edges, fixed, material.source[[0, -1], 0]]))
        self.lengths, self.centers = np.diff(self.edges), (self.edges[:-1]+self.edges[1:])/2
        self.nodes = self.centers[:, None]+self.lengths[:, None]*self.rule.points/2
        self.density = ContinuumDensity(material, self.nodes)
        mass = owner.central_mass+np.zeros_like(self.nodes)
        self.assign_mass(mass)
        for iteration in range(40):
            source_mass = self.evaluate(material.source[:, 0], self.mass_coefficients)
            fields = owner.boundaries(free_fields, material.source, source_mass)
            self.density.update(fields)
            mass_radial, unused = self.density.radial(mass.ravel())
            updated = owner.central_mass+self.integrated(mass_radial)
            error = float(np.max(abs(updated-mass)))
            mass = updated
            self.assign_mass(mass)
            if error < 2e-14:
                break
        else:
            raise RuntimeError('Independent continuum radial mass fixed point did not converge.')
        self.fields, self.iterations, self.fixed_point_error = fields, iteration+1, error
        unused, log_lapse_radial = self.density.radial(mass.ravel())
        primitive = self.integrated(log_lapse_radial)
        self.log_lapse_nodes = .5*np.log(1-2*mass[-1, -1]/self.edges[-1])+primitive-primitive[-1, -1]
        self.lapse_coefficients = self.log_lapse_nodes @ self.rule.inverse.T

    def integrated(self, values):
        partial = (values.reshape(self.nodes.shape) @ self.rule.integration.T)*self.lengths[:, None]/2
        starts = np.concatenate([[0.], np.cumsum(partial[:-1, -1])])
        return partial+starts[:, None]

    def assign_mass(self, mass):
        self.mass_nodes, self.mass_coefficients = mass, mass @ self.rule.inverse.T

    def evaluate(self, radius, coefficients, derivative=False):
        shape = np.asarray(radius).shape
        radius = np.asarray(radius).reshape(-1)
        indices = np.clip(np.searchsorted(self.edges, radius, side='right')-1, 0, len(self.lengths)-1)
        mapped = 2*(radius-self.centers[indices])/self.lengths[indices]
        if derivative:
            coefficients = np.polynomial.chebyshev.chebder(coefficients.T).T
        result = np.polynomial.chebyshev.chebval(mapped, coefficients[indices].T, tensor=False)
        result = result*2/self.lengths[indices] if derivative else result
        return result.reshape(shape)

    def metric(self, radius):
        mass = self.evaluate(radius, self.mass_coefficients)
        lapse = np.exp(self.evaluate(radius, self.lapse_coefficients))
        root = np.sqrt(1-2*mass/np.asarray(radius))
        return lapse, root

    def gradients(self, radius):
        return self.evaluate(radius, self.mass_coefficients, True), self.evaluate(radius, self.lapse_coefficients, True)

    def check_radial(self):
        points, unused = np.polynomial.legendre.leggauss(self.owner.radial_degree+3)
        targets = (self.centers[:, None]+self.lengths[:, None]*points/2).ravel()
        density = ContinuumDensity(self.material, targets, self.owner.label_order+4)
        density.update(self.fields)
        exact = density.radial(self.evaluate(targets, self.mass_coefficients))
        numerical = self.gradients(targets)
        return [float(np.max(abs(first-second))) for first, second in zip(exact, numerical)]


class LiveContinuumCharacteristics:
    def __init__(self, degree=48, layer_degree=4, radial_degree=10, radial_spacing=.1, label_order=8, coupling=.1, wave=True):
        self.degree, self.count, self.layer_degree, self.radial_degree = degree, degree+1, layer_degree, radial_degree
        self.spatial_rule, self.layer_rule, self.radial_rule = ChebyshevRule(degree), ChebyshevRule(layer_degree), ChebyshevRule(radial_degree)
        self.coordinate, self.labels = (1+self.spatial_rule.points)/2, self.layer_rule.points/2
        self.radial_spacing, self.label_order = radial_spacing, label_order
        self.width, self.inner, self.outer, self.central_mass, self.source_mass, self.coupling = .02, 5.2, 6.8, .7, .03, coupling
        self.wave = wave
        barycentric = (-1.)**np.arange(self.count)
        barycentric[[0, -1]] *= .5
        separation = self.coordinate[:, None]-self.coordinate[None, :]
        np.fill_diagonal(separation, 1.)
        self.derivative = barycentric[None, :]/barycentric[:, None]/separation
        np.fill_diagonal(self.derivative, 0.)
        np.fill_diagonal(self.derivative, -self.derivative.sum(axis=1))

    def mesh(self, source, velocity):
        position = source[:, 0]
        inner, outer = self.inner+self.width*self.labels, self.outer+self.width*self.labels
        lengths = np.stack([position-inner, outer-position], axis=1)
        radii = np.stack([inner, position], axis=1)[:, :, None]+lengths[:, :, None]*self.coordinate
        speed = np.stack([self.coordinate[None, :]*velocity[:, None], (1-self.coordinate)[None, :]*velocity[:, None]], axis=1)
        return radii, lengths, speed

    def pack(self, fields, source):
        return np.concatenate([fields[:, :, 0, :-1].ravel(), fields[:, :, 1, 1:].ravel(), source.ravel()])

    def unpack(self, state):
        part = (self.layer_degree+1)*2*self.degree
        fields = np.zeros((self.layer_degree+1, 2, 2, self.count))
        fields[:, :, 0, :-1] = state[:part].reshape(self.layer_degree+1, 2, self.degree)
        fields[:, :, 1, 1:] = state[part:2*part].reshape(self.layer_degree+1, 2, self.degree)
        return fields, state[2*part:].reshape(self.layer_degree+1, 3)

    def boundaries(self, free_fields, source, mass):
        fields = free_fields.copy()
        root = np.sqrt(1-2*mass/source[:, 0])
        energy = np.sqrt(self.source_mass**2+root**2*source[:, 1]**2)
        ratio = root*source[:, 1]/energy
        if np.max(abs(ratio)) >= 1:
            raise ValueError('Non-timelike continuum source.')
        fields[:, 0, 0, -1] = -(1-ratio)/(1+ratio)*fields[:, 0, 1, -1]
        fields[:, 0, 1, 0] = fields[:, 0, 0, 0]
        fields[:, 1, 0, -1] = fields[:, 1, 1, -1]
        fields[:, 1, 1, 0] = -(1+ratio)/(1-ratio)*fields[:, 1, 0, 0]
        return fields

    def solve(self, state):
        free, source = self.unpack(state)
        material = ContinuumMaterial(self, source)
        return ContinuumGeometry(self, material, free)

    def initial(self):
        source = np.stack([6.03+self.width*self.labels, np.zeros(len(self.labels)), np.zeros(len(self.labels))], axis=1)
        velocity = .03+np.zeros(len(self.labels))
        radii, unused, unused2 = self.mesh(source, velocity)
        gradient = prepared_gradient(radii-source[:, 0, None, None]) if self.wave else np.zeros_like(radii)
        temporal = -.03*gradient
        lapse, root = np.sqrt(1-2*self.central_mass/radii), np.sqrt(1-2*self.central_mass/radii)
        source_lapse, source_root = np.sqrt(1-2*self.central_mass/source[:, 0]), np.sqrt(1-2*self.central_mass/source[:, 0])
        previous = None
        for iteration in range(30):
            source[:, 1] = self.source_mass*velocity/(source_root**2*np.sqrt(source_lapse**2-velocity**2/source_root**2))
            scaled = temporal/(lapse*root)
            state = self.pack(np.stack([scaled+gradient, scaled-gradient], axis=2), source)
            geometry = self.solve(state)
            lapse, root = geometry.metric(radii)
            source_lapse, source_root = geometry.metric(source[:, 0])
            if previous is not None and np.max(abs(previous-state)) < 2e-14:
                return state, geometry
            previous = state.copy()
        raise RuntimeError('Independent velocity-prepared initial constraints failed.')

    def rhs_with_geometry(self, state):
        geometry = self.solve(state)
        fields, source = geometry.fields, geometry.material.source
        position, momentum = source[:, 0], source[:, 1]
        lapse_source, root_source = geometry.metric(position)
        energy = np.sqrt(self.source_mass**2+root_source**2*momentum**2)
        velocity, clock = lapse_source*root_source**2*momentum/energy, lapse_source*self.source_mass/energy
        radii, lengths, speeds = self.mesh(source, velocity)
        lapse, root = geometry.metric(radii)
        speed = lapse*root
        mass_radial, log_lapse_radial = geometry.gradients(radii)
        mass = geometry.evaluate(radii, geometry.mass_coefficients)
        speed_radial = speed*(log_lapse_radial+(mass/radii**2-mass_radial/radii)/root**2)
        plus, minus = fields[:, :, 0], fields[:, :, 1]
        curvature = speed/radii*(plus-minus)
        plus_rate = (speed+speeds)/lengths[:, :, None]*(plus @ self.derivative.T)+speed_radial*plus+curvature
        minus_rate = (speeds-speed)/lengths[:, :, None]*(minus @ self.derivative.T)-speed_radial*minus+curvature
        gradient_left = (fields[:, 0, 0, -1]-fields[:, 0, 1, -1])/2
        gradient_right = (fields[:, 1, 0, 0]-fields[:, 1, 1, 0])/2
        radiation = position**2*lapse_source*root_source*(1-(root_source*momentum/energy)**2)*(gradient_left**2-gradient_right**2)/2
        mass_radial_source, log_lapse_radial_source = geometry.gradients(position)
        mass_source = geometry.evaluate(position, geometry.mass_coefficients)
        gravity = -lapse_source*energy*log_lapse_radial_source
        gravity -= lapse_source*momentum**2/energy*(mass_source/position**2-mass_radial_source/position)
        source_rate = np.stack([velocity, gravity+radiation, clock], axis=1)
        flow = self.pack(np.stack([plus_rate, minus_rate], axis=2), source_rate)
        return flow, geometry, dict(velocity=velocity, clock=clock, radiation=radiation, gravity=gravity)

    def rhs(self, time, state):
        return self.rhs_with_geometry(state)[0]

    def sample(self, state, radius, labels):
        geometry = self.solve(state)
        source = geometry.material.values(labels)
        radius, labels = np.broadcast_arrays(radius, labels)
        inner, outer = self.inner+self.width*labels, self.outer+self.width*labels
        result = np.zeros((2, len(radius)))
        for side in [0, 1]:
            selected = radius < source[:, 0] if side == 0 else radius >= source[:, 0]
            lower, upper = (inner, source[:, 0]) if side == 0 else (source[:, 0], outer)
            mapped = 2*(radius[selected]-lower[selected])/(upper[selected]-lower[selected])-1
            label_interpolation = geometry.material.interpolation(labels[selected])
            spatial_interpolation = np.polynomial.chebyshev.chebvander(mapped, self.degree) @ self.spatial_rule.inverse
            for sign in [0, 1]:
                interpolated = label_interpolation @ geometry.fields[:, side, sign]
                result[sign, selected] = np.sum(interpolated*spatial_interpolation, axis=1)
        lapse, root = geometry.metric(radius)
        return lapse*root*(result[0]+result[1])/2, (result[0]-result[1])/2

    def current_test(self, state, step=2e-5):
        flow, geometry, unused = self.rhs_with_geometry(state)
        middle = geometry.material.source[self.layer_degree//2, 0]
        targets = np.array([5.53, 5.995, 6.005, middle-.007, middle, middle+.007, 6.095, 6.47])
        masses = []
        for multiple in [-2, -1, 1, 2]:
            adjacent = self.solve(state+multiple*step*flow)
            masses.append(adjacent.evaluate(targets, adjacent.mass_coefficients))
        derivative = (masses[0]-8*masses[1]+8*masses[2]-masses[3])/(12*step)
        density = ContinuumDensity(geometry.material, targets, self.label_order+4)
        density.update(geometry.fields)
        lapse, root = geometry.metric(targets)
        current = self.coupling*lapse*root**3*(targets**2*density.cross-density.source_momentum*density.source_density)
        return dict(targets=targets, derivative=derivative, current=current, error=float(np.max(abs(derivative-current))))
