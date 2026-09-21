from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_P2_canonical_v2_20260918 import LiveP2System, P2Material, P2Density
from annular_repaired_live_current_20260915 import TangentGeometry
from annular_repaired_live_geometry_20260915 import material_weight
import numpy as np


class EvolvingP2System(LiveP2System):
    def forces(self, coordinates, rates, geometry):
        return np.array([np.append(self.layer(label, geometry).evaluate(0., position, velocity)['scalar_covector'],
            self.layer(label, geometry).source_covector(0., position, velocity))
            for label, position, velocity in zip(self.labels, coordinates, rates)])

    def rhs(self, time, state):
        coordinates, momenta = state.reshape(2, len(self.labels), self.count+1)
        rates, geometry = self.solve(coordinates, momenta)
        return np.stack([rates, self.forces(coordinates, rates, geometry)]).ravel()


def physical_sample(layer, coordinates, rates, radius):
    radius = np.atleast_1d(radius)
    position = coordinates[-1]
    inner, outer = layer.radii[[0, -1]]+layer.width*layer.offset
    left = radius.real < position.real
    jacobian = np.where(left, (position-inner)/(layer.anchor-layer.radii[0]),
        (outer-position)/(layer.radii[-1]-layer.anchor))
    reference = np.where(left, layer.radii[0]+(radius-inner)/jacobian,
        layer.radii[-1]-(outer-radius)/jacobian)
    indices, shape, radial = layer.features_quadratic(reference)
    unused, unused2, displacement = layer.mapping(reference, position)
    gradient = np.sum(radial*coordinates[:-1][indices], axis=1)/jacobian
    temporal = np.sum(shape*rates[:-1][indices], axis=1)-displacement*rates[-1]*gradient
    return temporal, gradient


def regular_dual(layer, coordinates, rates, radius):
    temporal, gradient = physical_sample(layer, coordinates, rates, radius)
    coefficient = layer.coefficient(0., radius)
    return -.5*(np.asarray(radius)**4*temporal**2/coefficient**2+gradient**2)


def edge_duals(layer, coordinates, rates):
    positions, jacobian, displacement = layer.mapping(layer.edges, coordinates[-1])
    count = len(layer.edges)-1
    values = []
    for endpoint in [0., 1.]:
        shape = np.array([(1-endpoint)*(1-2*endpoint), 4*endpoint*(1-endpoint), endpoint*(2*endpoint-1)])
        radial = np.array([4*endpoint-3, 4-8*endpoint, 4*endpoint-1])[None, :]/np.diff(layer.edges)[:, None]
        indices = layer.element_indices
        mask = indices >= 0
        safe = np.maximum(indices, 0)
        reference = layer.edges[:-1] if endpoint == 0 else layer.edges[1:]
        radius, unused, motion = layer.mapping(reference, coordinates[-1])
        unused, local_jacobian, unused2 = layer.mapping((layer.edges[:-1]+layer.edges[1:])/2, coordinates[-1])
        gradient = np.sum(radial*mask*coordinates[:-1][safe], axis=1)/local_jacobian
        temporal = np.sum(shape*mask*rates[:-1][safe], axis=1)-motion*rates[-1]*gradient
        coefficient = layer.coefficient(0., radius)
        values.append(-.5*(radius**4*temporal**2/coefficient**2+gradient**2))
    jump = np.concatenate([[0.], values[1]])-np.concatenate([values[0], [0.]])
    return positions, displacement*rates[-1], jump


class LayerCurrent:
    def __init__(self, layer, tangent_layer, coordinates, rates, acceleration, step=1e-24):
        self.layer, self.tangent_layer = layer, tangent_layer
        self.coordinates, self.rates, self.acceleration, self.step = coordinates, rates, acceleration, step
        self.changed_coordinates = coordinates.astype(complex)+1j*step*rates
        self.changed_rates = rates.astype(complex)+1j*step*acceleration
        data = layer.evaluate(0., coordinates, rates)
        changed = tangent_layer.evaluate(0., self.changed_coordinates, self.changed_rates)
        self.data = data
        self.euler = changed['momenta'][:-1].imag/step-data['scalar_covector']
        self.source_euler = changed['momenta'][-1].imag/step-layer.source_covector(0., coordinates, rates)
        self.wave_source_euler = changed['field_momenta'][-1].imag/step-layer.source_covector(0., coordinates, rates, wave=True)
        self.nodes, unused, motion = layer.mapping(layer.radii, coordinates[-1])
        self.node_speed = motion*rates[-1]
        self.atom_dual = data['nodal_dual']
        self.atom_dual_dot = changed['nodal_dual'].imag/step
        coefficient_radial = layer.coefficient(0., self.nodes.astype(complex)+1j*step).imag/step
        self.atom_transport_work = coefficient_radial*self.atom_dual*self.node_speed
        self.atom_work = data['nodal']*self.atom_dual_dot+self.atom_transport_work
        self.edges, self.edge_speed, self.edge_jump = edge_duals(layer, coordinates, rates)
        self.edge_work = layer.coefficient(0., self.edges)*self.edge_speed*self.edge_jump

    def regular_work(self, radius):
        varied = regular_dual(self.tangent_layer, self.changed_coordinates, self.changed_rates, radius)
        return self.layer.coefficient(0., radius)*varied.imag/self.step

    def integrate(self, lower, upper):
        if upper <= lower:
            return 0.
        extra = np.concatenate([self.edges, self.layer.geometry.edges])
        extra = extra[(extra > lower) & (extra < upper)]
        endpoints = np.unique(np.concatenate([[lower], extra, [upper]]))
        lengths = np.diff(endpoints)
        radius = (endpoints[:-1, None]+lengths[:, None]*self.layer.fractions).ravel()
        weights = (lengths[:, None]*self.layer.weights).ravel()
        return float(weights @ self.regular_work(radius))

    def tail(self, target, retain_euler=True, moving_transport=True):
        left = target < self.coordinates[-1]
        lower, upper = (self.edges[0], min(target, self.edges[-1])) if left else (max(target, self.edges[0]), self.edges[-1])
        if upper <= lower:
            return 0.
        selected = self.nodes < target if left else self.nodes > target
        work = self.atom_work if moving_transport else self.data['nodal']*self.atom_dual_dot
        atoms = np.sum(work[selected])
        if retain_euler:
            atoms += np.sum((self.euler*self.rates[:-1])[selected])
        boundaries = self.edges < target if left else self.edges > target
        edge_work = np.sum(self.edge_work[boundaries]) if moving_transport else 0.
        total = self.integrate(lower, upper)+atoms+edge_work
        return float(total if left else -total)

    def noether(self):
        regular = self.integrate(self.edges[0], self.edges[-1])
        euler_work = self.euler @ self.rates[:-1]+self.rates[-1]*self.wave_source_euler
        total = euler_work+regular+sum(self.atom_work)+sum(self.edge_work)
        return dict(residual=float(abs(total)), without_moving_transport=float(abs(total-sum(self.atom_transport_work)-sum(self.edge_work))),
            moving_edge_work=float(sum(self.edge_work)), moving_atom_work=float(sum(self.atom_transport_work)),
            scalar_euler=float(max(abs(self.euler))), source_euler=float(abs(self.source_euler)))


class LiveP2Tangent:
    def __init__(self, system, coordinates, momenta, difference_step=2e-5):
        self.system, self.coordinates, self.momenta = system, coordinates, momenta
        self.rates, self.geometry = system.solve(coordinates, momenta)
        self.forces = system.forces(coordinates, self.rates, self.geometry)
        self.material = P2Material(system, coordinates)
        self.step = difference_step
        neighbors, rates = [], []
        for multiple in [-2, -1, 1, 2]:
            changed_rates, geometry = system.solve(coordinates+multiple*difference_step*self.rates,
                momenta+multiple*difference_step*self.forces)
            neighbors.append(geometry)
            rates.append(changed_rates)
        self.acceleration = (rates[0]-8*rates[1]+8*rates[2]-rates[3])/(12*difference_step)
        self.tangent_geometry = TangentGeometry(self.geometry, neighbors, difference_step, 1j*1e-24)
        self.cache = {}

    def layer_data(self, label):
        if float(label) not in self.cache:
            interpolation = self.material.interpolation([label])[0]
            self.cache[float(label)] = LayerCurrent(self.system.layer(label, self.geometry),
                self.system.layer(label, self.tangent_geometry), interpolation @ self.coordinates,
                interpolation @ self.rates, interpolation @ self.acceleration)
        return self.cache[float(label)]

    def compare(self, targets, label_order=10):
        points, weights = np.polynomial.legendre.leggauss(label_order)
        rows = []
        model, system = self.system.model, self.system
        split_nodes = np.unique(np.concatenate([model.edges, model.radii]))
        endpoints = np.array([self.material.node_geometry(split_nodes, label)[0] for label in [-.5, .5]])
        for target in np.asarray(targets):
            selected = (target > endpoints[0]) & (target < endpoints[1])
            crosses = self.material.inverse_node(target, split_nodes[selected])
            cuts = np.unique(np.concatenate([[-.5], crosses, [.5]]))
            total = np.zeros(3)
            for lower, upper in zip(cuts[:-1], cuts[1:]):
                if upper-lower < 1e-13:
                    continue
                labels = (lower+upper)/2+(upper-lower)*points/2
                values = []
                for label in labels:
                    current = self.layer_data(label)
                    values.append([current.tail(target), current.tail(target, retain_euler=False),
                        current.tail(target, moving_transport=False)])
                total += (upper-lower)/2*(weights*material_weight(labels)) @ np.array(values)
            moving_atom = 0.
            active = np.flatnonzero(np.asarray(model.sampling.sum(axis=0)).ravel() != 0)
            for index in active:
                reference = model.radii[index]
                lower, upper = self.material.node_geometry(reference, np.array([-.5, .5]))[0]
                if lower < target < upper:
                    label = float(self.material.inverse_node(target, reference))
                    current = self.layer_data(label)
                    unused, unused2, label_jacobian = self.material.node_geometry(reference, label)
                    moving_atom -= current.data['nodal'][index]*current.atom_dual[index]*current.node_speed[index]*material_weight(label)/label_jacobian
            total[:2] += moving_atom
            lapse, root = self.geometry.metric(target)
            source = 0.
            lower, upper = self.coordinates[[0, -1], -1]
            if lower < target < upper:
                label = float(self.material.inverse_node(target, model.anchor))
                interpolation = self.material.interpolation([label])[0]
                velocity = interpolation @ self.rates[:, -1]
                clock = np.sqrt(lapse**2-velocity**2/root**2)
                source = -system.coupling*lapse*root**3*system.source_mass*velocity/(root**2*clock)*material_weight(label)/self.material.source_jacobian(label)
            currents = -system.coupling*root/lapse*total+source
            mass_dot = self.tangent_geometry.derivative(np.array([target]), metric=False)[0][0]
            rows.append(dict(radius=float(target), mass_derivative=float(mass_dot), current=float(currents[0]),
                on_shell_current=float(currents[1]), frozen_mesh_current=float(currents[2]),
                moving_atom_connection_current=float(moving_atom), source_current=float(source),
                error=float(abs(mass_dot-currents[0])), on_shell_error=float(abs(mass_dot-currents[1])),
                frozen_mesh_error=float(abs(mass_dot-currents[2]))))
        return rows
