from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_locally_refined_source_action_20260916 import LocallyRefinedSourceAction
from annular_source_fitted_action_20260915 import SourceFittedAction
from annular_repaired_live_geometry_20260915 import LiveGeometry, material_weight
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from annular_cut_initial_data_20260915 import compatible_initial_state
from scipy.linalg import solve_banded
from scipy.optimize import brentq
import numpy as np


def polynomial_extrema(coefficients):
    roots = np.polynomial.chebyshev.chebroots(np.polynomial.chebyshev.chebder(coefficients))
    roots = roots[(abs(roots.imag) < 1e-10) & (abs(roots.real) < 1)].real
    values = np.polynomial.chebyshev.chebval(np.concatenate([[-1., 1.], roots]), coefficients)
    return float(min(values)), float(max(values))


class LiveP2Layer(LocallyRefinedSourceAction):
    def __init__(self, owner, offset, geometry):
        self.__dict__.update(owner.model.__dict__)
        self.offset, self.width, self.geometry = offset, owner.width, geometry

    def mapping(self, reference, position):
        radius, jacobian, displacement = SourceFittedAction.mapping(self, reference, position-self.width*self.offset)
        return radius+self.width*self.offset, jacobian, displacement

    def metric(self, time, radius):
        return self.geometry.metric(radius)


def wave_kinematics(layer, coordinates):
    radius, jacobian, displacement = layer.mapping(layer.reference_radius, coordinates[-1])
    lapse, root = layer.metric(0., radius)
    shape, radial, indices = layer.reference_shape, layer.reference_radial, layer.reference_indices
    motion = -displacement*np.sum(radial*coordinates[:-1][indices], axis=1)/jacobian
    weight = layer.reference_weight*jacobian*radius**2/(lapse*root)
    return radius, shape, indices, motion, weight


def inverse_momenta(layer, coordinates, momenta):
    data = layer.evaluate(0., coordinates, np.zeros_like(coordinates))
    solved = solve_banded((2, 2), data['mass_bands'], np.column_stack([momenta[:-1], data['cross']]), check_finite=False)
    unused, shape, indices, motion, weight = wave_kinematics(layer, coordinates)
    projected = np.sum(shape*solved[:, 1][indices], axis=1)
    complement = float(np.real(np.dot(weight, (motion-projected)**2)))
    lapse, root = layer.metric(0., coordinates[-1])
    field_inertia = np.dot(weight, motion**2)
    raw_complement = field_inertia-data['cross'] @ solved[:, 1]
    target = momenta[-1]-data['cross'] @ solved[:, 0]
    limit = float(lapse*root)*(1-1e-12)

    def residual(velocity):
        clock = np.sqrt(lapse**2-velocity**2/root**2)
        return complement*velocity+layer.source_mass*velocity/(root**2*clock)-target

    velocity = brentq(residual, -limit, limit, xtol=2e-15, rtol=1e-14)
    rates = np.append(solved[:, 0]-solved[:, 1]*velocity, velocity)
    clock = np.sqrt(lapse**2-velocity**2/root**2)
    proper_inertia = layer.source_mass*lapse**2/(root**2*clock**3)
    return rates, dict(field_schur=complement, subtraction_schur=float(np.real(raw_complement)),
        schur_error=float(abs(raw_complement-complement)), proper_inertia=float(proper_inertia),
        total_schur=float(complement+proper_inertia), timelike_ratio=float(abs(velocity/(lapse*root))))


class P2Material:
    def __init__(self, owner, coordinates):
        self.owner, self.coordinates = owner, coordinates
        self.coefficients = owner.layer_rule.inverse @ coordinates
        self.source_derivative = 2*np.polynomial.chebyshev.chebder(self.coefficients[:, -1])
        self.minimum_jacobian = polynomial_extrema(self.source_derivative)[0]
        offset = self.coefficients[:, -1].copy()
        offset[0] -= owner.model.anchor
        offset[1] -= owner.width/2
        lower, upper = polynomial_extrema(offset)
        self.minimum_spatial_jacobian = min(1+lower/(owner.model.anchor-owner.model.radii[0]),
            1-upper/(owner.model.radii[-1]-owner.model.anchor))
        if min(self.minimum_jacobian, self.minimum_spatial_jacobian) <= 0:
            raise ValueError('Material or source-fitted spatial map lost ordering.')

    def interpolation(self, labels):
        return np.polynomial.chebyshev.chebvander(2*np.asarray(labels), self.owner.layer_degree) @ self.owner.layer_rule.inverse

    def values(self, labels):
        return self.interpolation(labels) @ self.coordinates

    def source_jacobian(self, labels):
        return np.polynomial.chebyshev.chebval(2*np.asarray(labels), self.source_derivative)

    def node_geometry(self, reference, labels):
        reference, labels = np.broadcast_arrays(reference, labels)
        model = self.owner.model
        unused, unused2, displacement = model.mapping(reference, model.anchor)
        source = np.polynomial.chebyshev.chebval(2*labels, self.coefficients[:, -1])
        slope = np.where(reference < model.anchor, 1/(model.anchor-model.radii[0]), -1/(model.radii[-1]-model.anchor))
        radius = reference+displacement*(source-model.anchor)+(1-displacement)*self.owner.width*labels
        jacobian = 1+slope*(source-model.anchor-self.owner.width*labels)
        label_jacobian = (1-displacement)*self.owner.width+displacement*self.source_jacobian(labels)
        return radius, jacobian, label_jacobian

    def inverse_node(self, radius, reference):
        radius = np.asarray(radius)
        lower = self.node_geometry(reference, -.5)[0]
        upper = self.node_geometry(reference, .5)[0]
        labels = (radius-lower)/(upper-lower)-.5
        for unused in range(8):
            physical, unused2, derivative = self.node_geometry(reference, labels)
            labels -= (physical-radius)/derivative
        return np.clip(labels, -.5, .5)

    def samples(self, radius, labels):
        model = self.owner.model
        interpolation = self.interpolation(labels)
        values = interpolation @ self.coordinates
        source = values[:, -1]
        inner, outer = model.radii[0]+self.owner.width*labels, model.radii[-1]+self.owner.width*labels
        left = radius < source
        jacobian = np.where(left, (source-inner)/(model.anchor-model.radii[0]), (outer-source)/(model.radii[-1]-model.anchor))
        reference = np.where(left, model.radii[0]+(radius-inner)/jacobian, model.radii[-1]-(outer-radius)/jacobian)
        indices, shape, radial = model.features_quadratic(reference)
        unused, unused2, displacement = model.mapping(reference, model.anchor)
        gradient = np.sum(radial*values[:, :-1][np.arange(len(radius))[:, None], indices], axis=1)/jacobian
        outside = (radius < inner) | (radius > outer)
        shape[outside], gradient[outside] = 0., 0.
        motion = -displacement*gradient
        return interpolation, indices, shape, gradient, motion

    def gram_load(self, labels):
        factors = self.values(labels)[:, :-1] @ self.owner.model.lifted.T
        return (factors**2) @ self.owner.model.sampling/(2*self.owner.model.gram_spacing)


class P2Density:
    def __init__(self, material, radius):
        self.material, self.radius = material, np.asarray(radius).ravel()
        owner, model = material.owner, material.owner.model
        points, weights = np.polynomial.legendre.leggauss(owner.label_order)
        endpoints = np.array([material.node_geometry(model.edges, label)[0] for label in [-.5, .5]])
        offsets, measures, indices = [], [], []
        for index, target in enumerate(self.radius):
            selected = (target > endpoints[0]) & (target < endpoints[1])
            crosses = material.inverse_node(target, model.edges[selected])
            cuts = np.unique(np.concatenate([[-.5], crosses, [.5]]))
            for lower, upper in zip(cuts[:-1], cuts[1:]):
                if upper-lower < 1e-13:
                    continue
                labels = (lower+upper)/2+(upper-lower)*points/2
                offsets.extend(labels)
                measures.extend((upper-lower)*weights*material_weight(labels)/2)
                indices.extend([index]*len(points))
        self.offsets, self.label_weights, self.indices = np.asarray(offsets), np.asarray(measures), np.asarray(indices)
        self.interpolation, self.scalar_indices, self.shape, gradient, self.motion = material.samples(self.radius[self.indices], self.offsets)
        self.gradient_square = np.bincount(self.indices, weights=self.label_weights*gradient**2, minlength=len(self.radius))
        self.gram = np.zeros(len(self.radius))
        selected_nodes = np.asarray(model.sampling.sum(axis=0)).ravel() != 0
        for index in np.flatnonzero(selected_nodes):
            reference = model.radii[index]
            lower, upper = material.node_geometry(reference, np.array([-.5, .5]))[0]
            selected = (self.radius >= lower) & (self.radius <= upper)
            if np.any(selected):
                labels = material.inverse_node(self.radius[selected], reference)
                unused, jacobian, label_jacobian = material.node_geometry(reference, labels)
                self.gram[selected] += material_weight(labels)*material.gram_load(labels)[:, index]/(jacobian*label_jacobian)
        lower, upper = material.coordinates[[0, -1], -1]
        self.source_selected = (self.radius >= lower) & (self.radius <= upper)
        labels = material.inverse_node(self.radius[self.source_selected], model.anchor)
        self.source_interpolation = material.interpolation(labels)
        self.source_density = np.zeros(len(self.radius))
        self.source_density[self.source_selected] = material_weight(labels)/material.source_jacobian(labels)

    def update(self, rates):
        sample = self.interpolation @ rates
        temporal = np.sum(self.shape*sample[:, :-1][np.arange(len(sample))[:, None], self.scalar_indices], axis=1)
        temporal += self.motion*sample[:, -1]
        self.temporal_square = np.bincount(self.indices, weights=self.label_weights*temporal**2, minlength=len(self.radius))
        self.velocity = np.zeros(len(self.radius))
        self.velocity[self.source_selected] = self.source_interpolation @ rates[:, -1]

    def rhs(self, mass, log_lapse):
        owner, radius = self.material.owner, self.radius
        metric, lapse = 1-2*mass/radius, np.exp(log_lapse)
        if np.min(metric) <= 0:
            raise ValueError('P2 radial solve left the untrapped branch.')
        root = np.sqrt(metric)
        clock_square = lapse**2-self.velocity**2/metric
        if np.min(clock_square) <= 0:
            raise ValueError('P2 source left the timelike branch.')
        clock = np.sqrt(clock_square)
        density = .5*(self.temporal_square/(lapse**2*metric)+self.gradient_square)+self.gram
        mass_rhs = owner.coupling*(radius**2*metric*density+root*owner.source_mass*lapse/clock*self.source_density)
        lapse_rhs = mass/(radius**2*metric)+owner.coupling*radius*density
        lapse_rhs += owner.coupling*owner.source_mass*self.velocity**2/(radius*lapse*root**3*clock)*self.source_density
        return mass_rhs, lapse_rhs


class LiveP2Geometry(LiveGeometry):
    def __init__(self, owner, material, rates):
        self.owner, self.material, self.rule = owner, material, owner.radial_rule
        self.edges = np.unique(np.concatenate([material.node_geometry(owner.model.edges, label)[0] for label in [-.5, .5]]))
        self.lengths, self.centers = np.diff(self.edges), (self.edges[:-1]+self.edges[1:])/2
        self.nodes = self.centers[:, None]+self.lengths[:, None]*self.rule.points/2
        self.density = P2Density(material, self.nodes)
        self.density.update(rates)
        self.solve()

    def off_grid_residual(self, rates):
        points, unused = np.polynomial.legendre.leggauss(self.owner.radial_degree+3)
        radius = (self.centers[:, None]+self.lengths[:, None]*points/2).ravel()
        density = P2Density(self.material, radius)
        density.update(rates)
        mass, lapse, mass_radial, lapse_radial = self.values(radius)
        expected_mass, expected_lapse = density.rhs(mass, lapse)
        return float(max(abs(mass_radial-expected_mass))), float(max(abs(lapse_radial-expected_lapse)))


class LiveP2System:
    def __init__(self, base_count=17, gram=True, layer_degree=4, radial_degree=12, action_order=20, label_order=12, coupling=.1):
        self.model = LocallyRefinedSourceAction(base_count, gram, order=action_order, background_mass=.7, source_splits=8)
        self.count, self.gram, self.base_count = self.model.count, gram, base_count
        self.layer_degree, self.radial_degree, self.label_order = layer_degree, radial_degree, label_order
        self.layer_rule, self.radial_rule = ChebyshevRule(layer_degree), ChebyshevRule(radial_degree)
        self.labels = self.layer_rule.points/2
        self.width, self.central_mass, self.source_mass, self.coupling = .02, .7, .03, coupling
        self.radial_tolerance, self.canonical_tolerance = 4e-14, 4e-13

    def layer(self, label, geometry):
        return LiveP2Layer(self, label, geometry)

    def initial(self, wave=True, deformed=False):
        coordinates, rates, unused = compatible_initial_state(self.model, 0.)
        unused, unused2, displacement = self.model.mapping(self.model.radii, self.model.anchor)
        rates[:-1] *= 1-displacement
        if not wave:
            coordinates[:-1], rates[:-1] = 0., 0.
        coordinates, rates = np.tile(coordinates, (len(self.labels), 1)), np.tile(rates, (len(self.labels), 1))
        coordinates[:, -1] += self.width*self.labels
        if deformed:
            coordinates[:, -1] += .008+.002*self.labels+.004*self.labels**2
            coordinates[:, :-1] *= 1+.1*self.labels[:, None]
            rates[:, -1] = .04+.004*self.labels
            rates[:, :-1] *= 1+.15*self.labels[:, None]
        material = P2Material(self, coordinates)
        geometry = LiveP2Geometry(self, material, rates)
        momenta = np.array([self.layer(label, geometry).evaluate(0., position, velocity)['momenta']
            for label, position, velocity in zip(self.labels, coordinates, rates)])
        return coordinates, momenta, rates, geometry

    def solve(self, coordinates, momenta):
        material = P2Material(self, coordinates)
        rates = np.zeros_like(coordinates)
        geometry = LiveP2Geometry(self, material, rates)
        history = []
        for iteration in range(32):
            updated = np.array([inverse_momenta(self.layer(label, geometry), position, momentum)[0]
                for label, position, momentum in zip(self.labels, coordinates, momenta)])
            error = float(max(abs(updated-rates).ravel()))
            rates = updated
            geometry.density.update(rates)
            geometry.solve()
            history.append(error)
            if error < self.canonical_tolerance:
                break
        else:
            raise RuntimeError('Finite P2 canonical/radial iteration failed to converge.')
        geometry.canonical_history = history
        return rates, geometry

    def canonical_residual(self, coordinates, momenta, rates, geometry, off_grid=False):
        labels = (self.labels[:-1]+self.labels[1:])/2 if off_grid else self.labels
        interpolation = P2Material(self, coordinates).interpolation(labels)
        errors = [np.max(abs(self.layer(label, geometry).evaluate(0., position, velocity)['momenta']-target))
            for label, position, velocity, target in zip(labels, interpolation @ coordinates, interpolation @ rates, interpolation @ momenta)]
        return float(max(errors))
