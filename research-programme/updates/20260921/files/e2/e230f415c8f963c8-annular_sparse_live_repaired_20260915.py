import numpy as np
from scipy.linalg import solve_banded
from scipy.optimize import brentq
from annular_sparse_repaired_cut_20260915 import SparseRepairedCut
from annular_repaired_live_geometry_20260915 import (
    RepairedLiveSystem, LiveLayerAction, LiveGeometry, MaterialState,
    DensityTable, VacuumGeometry, material_weight,
)
from annular_horizontal_clock_evolution_20260913 import ChebyshevRule
from annular_cut_initial_data_20260915 import compatible_initial_state


def inverse_sparse(layer, coordinates, momenta):
    data = layer.evaluate(0., coordinates, np.zeros_like(coordinates))
    lapse, root = layer.metric(0., coordinates[-1])
    solved = solve_banded((1, 1), data['mass_bands'], np.column_stack([momenta[:-1], data['cross']]))
    free_velocity, cross_velocity = solved.T
    field_inertia = data['source_inertia']-layer.source_mass/(root**2*lapse)
    remainder = field_inertia-data['cross'] @ cross_velocity
    if remainder < -2e-12:
        raise ValueError('Negative field Schur complement beyond rounding tolerance.')
    target = momenta[-1]-data['cross'] @ free_velocity

    def residual(velocity):
        clock = np.sqrt(lapse**2-velocity**2/root**2)
        return layer.source_mass*velocity/(root**2*clock)+remainder*velocity-target

    limit = lapse*root*(1-1e-12)
    velocity = brentq(residual, -limit, limit, xtol=5e-15, rtol=2e-14)
    return np.append(free_velocity-cross_velocity*velocity, velocity), float(remainder)


class SparseLiveLayer(SparseRepairedCut):
    mesh = LiveLayerAction.mesh

    def __init__(self, owner, offset, geometry):
        self.radii = owner.base+owner.width*offset
        self.count, self.gram, self.spacing = owner.count, owner.gram, owner.spacing
        self.source_mass, self.stationary = owner.source_mass, False
        self.fractions, self.weights = owner.fractions, owner.action_weights
        self.original, self.sampling = owner.original, owner.sampling
        self.geometry = geometry

    def metric(self, time, radius):
        return self.geometry.metric(radius)


class SparseMaterial(MaterialState):
    def selected_values(self, interpolation, indices, array):
        return np.einsum('ij,ji->i', interpolation, array[:, indices])

    def samples(self, radius, offsets):
        owner = self.owner
        radius, offsets = np.broadcast_arrays(radius, offsets)
        interpolation = self.interpolation(offsets)
        position = interpolation @ self.coordinates[:, -1]
        relative = radius-owner.width*offsets
        local_position = position-owner.width*offsets
        cell = np.clip(np.searchsorted(owner.base, relative, side='right')-1, 0, owner.count-2)
        source_cell = np.searchsorted(owner.base, local_position)-1
        if np.any(source_cell < 0) or np.any(source_cell >= owner.count-1):
            raise ValueError('A source left the scalar mesh.')
        fraction = (relative-owner.base[cell])/owner.spacing
        shape = np.column_stack([1-fraction, fraction])
        radial = np.tile([-1/owner.spacing, 1/owner.spacing], (len(radius), 1))
        motion = np.zeros_like(shape)
        cut = cell == source_cell
        left, right = cut & (radius < position), cut & (radius >= position)
        shape[cut], radial[cut] = 0., 0.
        left_length = local_position-owner.base[source_cell]
        right_length = owner.base[source_cell+1]-local_position
        shape[left, 0] = (position[left]-radius[left])/left_length[left]
        radial[left, 0] = -1/left_length[left]
        motion[left, 0] = (relative[left]-owner.base[source_cell[left]])/left_length[left]**2
        shape[right, 1] = (radius[right]-position[right])/right_length[right]
        radial[right, 1] = 1/right_length[right]
        motion[right, 1] = (relative[right]-owner.base[source_cell[right]+1])/right_length[right]**2
        outside = (relative < owner.base[0]) | (relative > owner.base[-1])
        shape[outside], radial[outside], motion[outside] = 0., 0., 0.
        scalar = np.column_stack([self.selected_values(interpolation, cell+offset, self.coordinates) for offset in [0, 1]])
        return interpolation, cell, shape, np.sum(radial*scalar, axis=1), np.sum(motion*scalar, axis=1)

    def gram_at_node(self, offsets, node):
        owner = self.owner
        columns, factors, weights = owner.gram_stencils[node]
        if len(weights) == 0:
            return np.zeros(len(offsets))
        interpolation = self.interpolation(offsets)
        position = interpolation @ self.coordinates[:, -1]-owner.width*offsets
        cell = np.searchsorted(owner.base, position)-1
        jump = self.selected_values(interpolation, cell, self.coordinates)/(position-owner.base[cell])
        jump += self.selected_values(interpolation, cell+1, self.coordinates)/(owner.base[cell+1]-position)
        scalar = interpolation @ self.coordinates[:, columns]
        hinge = np.maximum(owner.base[columns][None, :]-position[:, None], 0.)
        lifted = scalar @ factors.T-(hinge @ factors.T)*jump[:, None]
        return lifted**2 @ weights/(2*owner.spacing)


class SparseDensity(DensityTable):
    def __init__(self, material, radius):
        self.material = material
        owner = material.owner
        self.radius = np.asarray(radius).reshape(-1)
        points, weights = owner.label_points, owner.label_weights
        lower_source, upper_source = material.coordinates[[0, -1], -1]
        low = np.searchsorted(owner.base, self.radius-owner.width/2, side='right')
        high = np.searchsorted(owner.base, self.radius+owner.width/2, side='left')
        source_selected = (self.radius >= lower_source) & (self.radius <= upper_source)
        source_labels = material.inverse_source(self.radius[source_selected])
        inverse = np.zeros(len(self.radius))
        inverse[source_selected] = source_labels
        lower, upper, indices = [], [], []
        for index, target in enumerate(self.radius):
            cuts = (target-owner.base[low[index]:high[index]])/owner.width
            if lower_source < target < upper_source:
                cuts = np.append(cuts, inverse[index])
            cuts = np.unique(np.concatenate([[-.5], cuts, [.5]]))
            lower.extend(cuts[:-1])
            upper.extend(cuts[1:])
            indices.extend([index]*(len(cuts)-1))
        lower, upper = np.array(lower), np.array(upper)
        self.offsets = ((lower+upper)[:, None]/2+(upper-lower)[:, None]/2*points).ravel()
        self.label_weights = ((upper-lower)[:, None]/2*weights).ravel()*material_weight(self.offsets)
        self.indices = np.repeat(indices, len(points))
        radii = self.radius[self.indices]
        self.interpolation, self.cell, self.shape, gradient, self.field_motion = material.samples(radii, self.offsets)
        self.gradient_square = np.bincount(self.indices, weights=self.label_weights*gradient**2, minlength=len(self.radius))
        self.gram = np.zeros(len(self.radius))
        if owner.gram:
            for node, base in enumerate(owner.base):
                selected = abs(self.radius-base) < owner.width/2
                if np.any(selected):
                    labels = (self.radius[selected]-base)/owner.width
                    self.gram[selected] += material_weight(labels)*material.gram_at_node(labels, node)/owner.width
        self.source_selected, self.source_labels = source_selected, source_labels
        self.source_interpolation = material.interpolation(source_labels)
        self.source_density = np.zeros(len(self.radius))
        self.source_density[source_selected] = material_weight(source_labels)/material.source_jacobian(source_labels)

    def update(self, rates):
        temporal = self.field_motion*(self.interpolation @ rates[:, -1])
        for offset in [0, 1]:
            temporal += self.shape[:, offset]*self.material.selected_values(self.interpolation, self.cell+offset, rates)
        self.temporal_square = np.bincount(self.indices, weights=self.label_weights*temporal**2, minlength=len(self.radius))
        self.velocity = np.zeros(len(self.radius))
        self.velocity[self.source_selected] = self.source_interpolation @ rates[:, -1]


class SparseLiveGeometry(LiveGeometry):
    def __init__(self, owner, material, rates):
        self.owner, self.material, self.rule = owner, material, owner.radial_rule
        bounds = material.coordinates[[0, -1], -1]
        self.edges = np.unique(np.concatenate([owner.base-owner.width/2, owner.base+owner.width/2, bounds]))
        self.lengths = np.diff(self.edges)
        self.centers = (self.edges[:-1]+self.edges[1:])/2
        self.nodes = self.centers[:, None]+self.lengths[:, None]/2*self.rule.points
        self.density = SparseDensity(material, self.nodes.ravel())
        self.density.update(rates)
        self.solve()

    def off_grid_residual(self, rates):
        points, unused = np.polynomial.legendre.leggauss(self.owner.radial_degree+3)
        radius = (self.centers[:, None]+self.lengths[:, None]/2*points).ravel()
        density = SparseDensity(self.material, radius)
        density.update(rates)
        mass, log_lapse, mass_radial, lapse_radial = self.values(radius)
        exact_mass, exact_lapse = density.rhs(mass, log_lapse)
        return float(np.max(abs(mass_radial-exact_mass))), float(np.max(abs(lapse_radial-exact_lapse)))


class SparseRepairedLiveSystem(RepairedLiveSystem):
    def __init__(self, count=17, gram=True, layer_degree=4, radial_degree=8, width=.02,
                 action_order=8, label_order=8, central_mass=.7, coupling=.1):
        base_action = SparseRepairedCut(count, gram, action_order)
        self.count, self.gram = count, gram
        self.base, self.spacing = base_action.radii, base_action.spacing
        self.original, self.sampling = base_action.original, base_action.sampling
        self.fractions, self.action_weights = base_action.fractions, base_action.weights
        self.layer_degree, self.radial_degree = layer_degree, radial_degree
        self.layer_rule, self.radial_rule = ChebyshevRule(layer_degree), ChebyshevRule(radial_degree)
        self.labels = self.layer_rule.points/2
        self.width, self.action_order, self.label_order = width, action_order, label_order
        self.label_points, self.label_weights = np.polynomial.legendre.leggauss(label_order)
        self.central_mass, self.coupling, self.source_mass = central_mass, coupling, .03
        self.radial_tolerance, self.canonical_tolerance = 4e-14, 4e-13
        self.gram_stencils = []
        for node in range(count):
            column = self.sampling[:, node].tocoo()
            selected = column.data != 0
            rows, weights = column.row[selected], column.data[selected]
            factors = self.original[rows]
            columns = np.unique(factors.indices)
            self.gram_stencils.append((columns, factors[:, columns].toarray(), weights))

    def layer(self, offset, geometry):
        return SparseLiveLayer(self, offset, geometry)

    def initial(self, wave=True):
        base_action = self.layer(0., VacuumGeometry(self.central_mass))
        base_coordinates, base_rates, unused = compatible_initial_state(base_action, 0.)
        if not wave:
            base_coordinates[:-1], base_rates[:-1] = 0., 0.
        coordinates = np.tile(base_coordinates, (len(self.labels), 1))
        coordinates[:, -1] += self.width*self.labels
        rates = np.tile(base_rates, (len(self.labels), 1))
        geometry = SparseLiveGeometry(self, SparseMaterial(self, coordinates), rates)
        momenta = np.array([self.layer(offset, geometry).evaluate(0., position, velocity)['momenta']
                            for offset, position, velocity in zip(self.labels, coordinates, rates)])
        return coordinates, momenta, rates, geometry

    def solve(self, coordinates, momenta):
        material = SparseMaterial(self, coordinates)
        geometry = VacuumGeometry(self.central_mass)
        rates = np.zeros_like(coordinates)
        for iteration in range(32):
            updated = np.array([inverse_sparse(self.layer(offset, geometry), position, momentum)[0]
                                for offset, position, momentum in zip(self.labels, coordinates, momenta)])
            error = np.max(abs(updated-rates))
            rates = updated
            if iteration == 0:
                geometry = SparseLiveGeometry(self, material, rates)
            else:
                geometry.density.update(rates)
                geometry.solve()
            if error < self.canonical_tolerance:
                break
        else:
            raise RuntimeError('Coupled canonical/radial fixed point did not converge.')
        geometry.canonical_iterations = iteration+1
        geometry.canonical_fixed_point_error = float(error)
        return rates, geometry
