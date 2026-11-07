import numpy as np
from annular_covariant_cut_action_v2_20260915 import CurvedCutAction
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from annular_cut_initial_data_20260915 import compatible_initial_state
from verify_annular_cut_metric_and_inversion_20260915 import inverse_momenta


def material_weight(offset):
    return 6*(offset+.5)*(.5-offset)


class VacuumGeometry:
    def __init__(self, mass):
        self.mass = mass
        self.edges = np.array([])

    def metric(self, radius):
        root = np.sqrt(1-2*self.mass/np.asarray(radius))
        return root, root


class LiveLayerAction(CurvedCutAction):
    def __init__(self, owner, offset, geometry):
        super().__init__(owner.count, owner.gram, owner.action_order)
        self.radii = owner.base+owner.width*offset
        self.geometry = geometry
        self.source_mass = owner.source_mass

    def metric(self, time, radius):
        return self.geometry.metric(radius)

    def mesh(self, position):
        extra = self.geometry.edges
        extra = extra[(extra > self.radii[0]) & (extra < self.radii[-1])]
        extra = extra[abs(extra-position.real) > 1e-13]
        fixed = np.unique(np.concatenate([self.radii, extra]))
        fixed = fixed[abs(fixed-position.real) > 1e-13]
        endpoints = np.append(fixed.astype(np.result_type(position, float)), position)
        endpoints = endpoints[np.argsort(endpoints.real)]
        lengths = np.diff(endpoints)
        radius = (endpoints[:-1, None]+lengths[:, None]*self.fractions).ravel()
        weights = (lengths[:, None]*self.weights).ravel()
        return radius, weights


class MaterialState:
    def __init__(self, owner, coordinates):
        self.owner = owner
        self.coordinates = coordinates
        self.coefficients = owner.layer_rule.inverse @ coordinates
        self.source_derivative = 2*np.polynomial.chebyshev.chebder(self.coefficients[:, -1])
        probe = np.linspace(-.5, .5, 101)
        self.minimum_jacobian = float(np.min(self.source_jacobian(probe)))
        if self.minimum_jacobian <= 0:
            raise ValueError('Material layers are no longer ordered.')

    def interpolation(self, offsets):
        return np.polynomial.chebyshev.chebvander(2*np.asarray(offsets), self.owner.layer_degree) @ self.owner.layer_rule.inverse

    def values(self, offsets):
        return self.interpolation(offsets) @ self.coordinates

    def source_jacobian(self, offsets):
        return np.polynomial.chebyshev.chebval(2*np.asarray(offsets), self.source_derivative)

    def inverse_source(self, radius):
        bounds = self.coordinates[[0, -1], -1]
        offset = (np.asarray(radius)-bounds[0])/(bounds[1]-bounds[0])-.5
        for unused in range(8):
            value = np.polynomial.chebyshev.chebval(2*offset, self.coefficients[:, -1])
            offset -= (value-radius)/self.source_jacobian(offset)
        return offset

    def samples(self, radius, offsets):
        owner = self.owner
        radius, offsets = np.broadcast_arrays(radius, offsets)
        interpolation = self.interpolation(offsets)
        values = interpolation @ self.coordinates
        relative = radius-owner.width*offsets
        position = values[:, -1]
        local_position = position-owner.width*offsets
        cell = np.clip(np.searchsorted(owner.base, relative, side='right')-1, 0, owner.count-2)
        source_cell = np.searchsorted(owner.base, local_position)-1
        if np.any(source_cell < 0) or np.any(source_cell >= owner.count-1):
            raise ValueError('A source left the scalar mesh.')
        rows = np.arange(len(radius))
        shape = np.zeros((len(radius), owner.count))
        radial = np.zeros_like(shape)
        motion = np.zeros_like(shape)
        fraction = (relative-owner.base[cell])/owner.spacing
        shape[rows, cell], shape[rows, cell+1] = 1-fraction, fraction
        radial[rows, cell], radial[rows, cell+1] = -1/owner.spacing, 1/owner.spacing
        cut = cell == source_cell
        left = cut & (radius < position)
        right = cut & (~left)
        shape[cut], radial[cut] = 0., 0.
        left_length = local_position-owner.base[source_cell]
        right_length = owner.base[source_cell+1]-local_position
        shape[rows[left], source_cell[left]] = (position[left]-radius[left])/left_length[left]
        radial[rows[left], source_cell[left]] = -1/left_length[left]
        motion[rows[left], source_cell[left]] = (relative[left]-owner.base[source_cell[left]])/left_length[left]**2
        shape[rows[right], source_cell[right]+1] = (radius[right]-position[right])/right_length[right]
        radial[rows[right], source_cell[right]+1] = 1/right_length[right]
        motion[rows[right], source_cell[right]+1] = (relative[right]-owner.base[source_cell[right]+1])/right_length[right]**2
        outside = (relative < owner.base[0]) | (relative > owner.base[-1])
        shape[outside], radial[outside], motion[outside] = 0., 0., 0.
        gradient = np.sum(radial*values[:, :-1], axis=1)
        field_motion = np.sum(motion*values[:, :-1], axis=1)
        return interpolation, shape, gradient, field_motion

    def gram_load(self, offsets):
        owner = self.owner
        values = self.values(offsets)
        local_position = values[:, -1]-owner.width*np.asarray(offsets)
        cell = np.searchsorted(owner.base, local_position)-1
        rows = np.arange(len(offsets))
        jump = values[rows, cell]/(local_position-owner.base[cell])
        jump += values[rows, cell+1]/(owner.base[cell+1]-local_position)
        hinge = np.maximum(owner.base[None, :]-local_position[:, None], 0.)
        factors = values[:, :-1] @ owner.original.T-(hinge @ owner.original.T)*jump[:, None]
        return (factors**2) @ owner.sampling/(2*owner.spacing)


class DensityTable:
    def __init__(self, material, radius):
        self.material = material
        owner = material.owner
        self.radius = np.asarray(radius).reshape(-1)
        points, weights = np.polynomial.legendre.leggauss(owner.label_order)
        offsets, label_weights, indices = [], [], []
        source_low, source_high = material.coordinates[[0, -1], -1]
        for index, target in enumerate(self.radius):
            cuts = (target-owner.base)/owner.width
            cuts = cuts[(cuts > -.5) & (cuts < .5)]
            if source_low < target < source_high:
                cuts = np.append(cuts, material.inverse_source(target))
            cuts = np.unique(np.concatenate([[-.5], cuts, [.5]]))
            for lower, upper in zip(cuts[:-1], cuts[1:]):
                labels = (lower+upper)/2+(upper-lower)/2*points
                offsets.extend(labels)
                label_weights.extend((upper-lower)/2*weights*material_weight(labels))
                indices.extend([index]*len(points))
        self.offsets = np.array(offsets)
        self.label_weights = np.array(label_weights)
        self.indices = np.array(indices)
        radii = self.radius[self.indices]
        self.interpolation, self.shape, gradient, self.field_motion = material.samples(radii, self.offsets)
        self.gradient_square = np.bincount(self.indices, weights=self.label_weights*gradient**2, minlength=len(self.radius))
        self.gram = np.zeros(len(self.radius))
        for node, base in enumerate(owner.base):
            selected = abs(self.radius-base) < owner.width/2
            if np.any(selected):
                labels = (self.radius[selected]-base)/owner.width
                self.gram[selected] += material_weight(labels)*material.gram_load(labels)[:, node]/owner.width
        self.source_selected = (self.radius >= source_low) & (self.radius <= source_high)
        self.source_labels = material.inverse_source(self.radius[self.source_selected])
        self.source_interpolation = material.interpolation(self.source_labels)
        self.source_density = np.zeros(len(self.radius))
        self.source_density[self.source_selected] = material_weight(self.source_labels)/material.source_jacobian(self.source_labels)

    def update(self, rates):
        sample_rates = self.interpolation @ rates
        temporal = np.sum(self.shape*sample_rates[:, :-1], axis=1)+self.field_motion*sample_rates[:, -1]
        self.temporal_square = np.bincount(self.indices, weights=self.label_weights*temporal**2, minlength=len(self.radius))
        self.velocity = np.zeros(len(self.radius))
        self.velocity[self.source_selected] = self.source_interpolation @ rates[:, -1]

    def rhs(self, mass, log_lapse):
        owner = self.material.owner
        radius = self.radius
        root_square = 1-2*mass/radius
        lapse = np.exp(log_lapse)
        if np.min(root_square) <= 0:
            raise ValueError('The radial solver left the untrapped branch.')
        root = np.sqrt(root_square)
        clock_square = lapse**2-self.velocity**2/root_square
        if np.min(clock_square) <= 0:
            raise ValueError('The radial solver left the timelike source branch.')
        clock = np.sqrt(clock_square)
        dual = -.5*(self.temporal_square/(lapse**2*root_square)+self.gradient_square)-self.gram
        mass_rhs = -owner.coupling*radius**2*root_square*dual
        mass_rhs += owner.coupling*root*owner.source_mass*lapse/clock*self.source_density
        lapse_rhs = mass/(radius**2*root_square)-owner.coupling*radius*dual
        lapse_rhs += owner.coupling*owner.source_mass*self.velocity**2/(radius*lapse*root**3*clock)*self.source_density
        return mass_rhs, lapse_rhs


class LiveGeometry:
    def __init__(self, owner, material, rates):
        self.owner = owner
        self.material = material
        self.rule = owner.radial_rule
        bounds = material.coordinates[[0, -1], -1]
        self.edges = np.unique(np.concatenate([owner.base-owner.width/2, owner.base+owner.width/2, bounds]))
        self.lengths = np.diff(self.edges)
        self.centers = (self.edges[:-1]+self.edges[1:])/2
        self.nodes = self.centers[:, None]+self.lengths[:, None]/2*self.rule.points
        self.density = DensityTable(material, self.nodes.ravel())
        self.density.update(rates)
        self.solve()

    def integrated(self, density):
        density = density.reshape(self.nodes.shape)
        partial = (density @ self.rule.integration.T)*self.lengths[:, None]/2
        starts = np.concatenate([[0.], np.cumsum(partial[:-1, -1])])
        return partial+starts[:, None]

    def solve(self):
        mass = self.owner.central_mass+0*self.nodes
        log_lapse = np.log(np.sqrt(1-2*mass/self.nodes))
        for iteration in range(80):
            mass_rhs, lapse_rhs = self.density.rhs(mass.ravel(), log_lapse.ravel())
            new_mass = self.owner.central_mass+self.integrated(mass_rhs)
            primitive = self.integrated(lapse_rhs)
            outside = .5*np.log(1-2*new_mass[-1, -1]/self.edges[-1])
            new_lapse = outside+primitive-primitive[-1, -1]
            error = max(np.max(abs(new_mass-mass)), np.max(abs(new_lapse-log_lapse)))
            mass, log_lapse = new_mass, new_lapse
            if error < self.owner.radial_tolerance:
                break
        else:
            raise RuntimeError('Radial mass/lapse fixed point did not converge.')
        self.radial_iterations = iteration+1
        self.mass_nodes, self.log_lapse_nodes = mass, log_lapse
        self.mass_coefficients = mass @ self.rule.inverse.T
        self.lapse_coefficients = log_lapse @ self.rule.inverse.T
        self.fixed_point_error = float(error)
        self.mass_derivative = np.polynomial.chebyshev.chebder(self.mass_coefficients.T).T
        self.lapse_derivative = np.polynomial.chebyshev.chebder(self.lapse_coefficients.T).T

    def values(self, radius):
        radius = np.asarray(radius)
        indices = np.clip(np.searchsorted(self.edges, radius.real, side='right')-1, 0, len(self.lengths)-1)
        mapped = 2*(radius-self.centers[indices])/self.lengths[indices]
        mass = np.polynomial.chebyshev.chebval(mapped, self.mass_coefficients[indices].T, tensor=False)
        log_lapse = np.polynomial.chebyshev.chebval(mapped, self.lapse_coefficients[indices].T, tensor=False)
        mass_radial = 2/self.lengths[indices]*np.polynomial.chebyshev.chebval(mapped, self.mass_derivative[indices].T, tensor=False)
        lapse_radial = 2/self.lengths[indices]*np.polynomial.chebyshev.chebval(mapped, self.lapse_derivative[indices].T, tensor=False)
        return mass, log_lapse, mass_radial, lapse_radial

    def metric(self, radius):
        mass, log_lapse, unused, unused2 = self.values(radius)
        return np.exp(log_lapse), np.sqrt(1-2*mass/np.asarray(radius))

    def off_grid_residual(self, rates):
        points, unused = np.polynomial.legendre.leggauss(self.owner.radial_degree+3)
        radius = (self.centers[:, None]+self.lengths[:, None]/2*points).ravel()
        density = DensityTable(self.material, radius)
        density.update(rates)
        mass, log_lapse, mass_radial, lapse_radial = self.values(radius)
        exact_mass, exact_lapse = density.rhs(mass, log_lapse)
        return float(np.max(abs(mass_radial-exact_mass))), float(np.max(abs(lapse_radial-exact_lapse)))


class RepairedLiveSystem:
    def __init__(self, count=17, gram=True, layer_degree=4, radial_degree=8, width=.02,
                 action_order=8, label_order=8, central_mass=.7, coupling=.1):
        self.count, self.gram = count, gram
        self.base = np.linspace(5.2, 6.8, count)
        self.spacing = self.base[1]-self.base[0]
        self.layer_degree, self.radial_degree = layer_degree, radial_degree
        self.layer_rule, self.radial_rule = ChebyshevRule(layer_degree), ChebyshevRule(radial_degree)
        self.labels = self.layer_rule.points/2
        self.width, self.action_order, self.label_order = width, action_order, label_order
        self.central_mass, self.coupling, self.source_mass = central_mass, coupling, .03
        self.radial_tolerance, self.canonical_tolerance = 4e-14, 4e-13
        base_action = CurvedCutAction(count, gram)
        self.original, self.sampling = base_action.original, base_action.sampling

    def layer(self, offset, geometry):
        return LiveLayerAction(self, offset, geometry)

    def initial(self, wave=True):
        base_action = CurvedCutAction(self.count, self.gram)
        base_coordinates, base_rates, unused = compatible_initial_state(base_action, 0.)
        if not wave:
            base_coordinates[:-1], base_rates[:-1] = 0., 0.
        coordinates = np.tile(base_coordinates, (len(self.labels), 1))
        coordinates[:, -1] += self.width*self.labels
        rates = np.tile(base_rates, (len(self.labels), 1))
        material = MaterialState(self, coordinates)
        geometry = LiveGeometry(self, material, rates)
        momenta = np.array([self.layer(offset, geometry).evaluate(0., position, velocity)['momenta']
                            for offset, position, velocity in zip(self.labels, coordinates, rates)])
        return coordinates, momenta, rates, geometry

    def solve(self, coordinates, momenta):
        material = MaterialState(self, coordinates)
        geometry = VacuumGeometry(self.central_mass)
        rates = np.zeros_like(coordinates)
        for iteration in range(32):
            updated = np.array([inverse_momenta(self.layer(offset, geometry), 0., position, momentum)[0]
                                for offset, position, momentum in zip(self.labels, coordinates, momenta)])
            error = np.max(abs(updated-rates))
            rates = updated
            geometry = LiveGeometry(self, material, rates)
            if error < self.canonical_tolerance:
                break
        else:
            raise RuntimeError('Coupled canonical/radial fixed point did not converge.')
        geometry.canonical_iterations = iteration+1
        geometry.canonical_fixed_point_error = float(error)
        return rates, geometry

    def forces(self, coordinates, rates, geometry):
        forces = []
        for offset, position, velocity in zip(self.labels, coordinates, rates):
            layer = self.layer(offset, geometry)
            data = layer.evaluate(0., position, velocity)
            forces.append(np.append(data['scalar_covector'], layer.source_covector(0., position, velocity)))
        return np.array(forces)

    def rhs(self, time, state):
        coordinates, momenta = state.reshape(2, len(self.labels), self.count+1)
        rates, geometry = self.solve(coordinates, momenta)
        return np.stack([rates, self.forces(coordinates, rates, geometry)]).ravel()

    def canonical_residual(self, coordinates, momenta, rates, geometry, off_grid=False):
        labels = (self.labels[:-1]+self.labels[1:])/2 if off_grid else self.labels
        interpolation = MaterialState(self, coordinates).interpolation(labels)
        errors = []
        for offset, position, velocity, target in zip(labels, interpolation @ coordinates, interpolation @ rates, interpolation @ momenta):
            actual = self.layer(offset, geometry).evaluate(0., position, velocity)['momenta']
            errors.append(np.max(abs(actual-target)))
        return float(max(errors))
