import numpy as np
from annular_repaired_live_geometry_20260915 import MaterialState, material_weight


class TangentGeometry:
    def __init__(self, geometry, neighbors, step, amplitude):
        self.geometry, self.neighbors = geometry, neighbors
        self.step, self.amplitude, self.edges = step, amplitude, geometry.edges

    def derivative(self, radius, metric=True):
        getter = (lambda geometry: geometry.metric(radius)) if metric else (lambda geometry: geometry.values(radius)[:2])
        values = [getter(geometry) for geometry in self.neighbors]
        return tuple((values[0][index]-8*values[1][index]+8*values[2][index]-values[3][index])/(12*self.step)
                     for index in range(2))

    def metric(self, radius):
        lapse, root = self.geometry.metric(radius)
        lapse_dot, root_dot = self.derivative(np.asarray(radius).real)
        return lapse+self.amplitude*lapse_dot, root+self.amplitude*root_dot


class LiveTangent:
    def __init__(self, system, coordinates, momenta, difference_step=2e-5):
        self.system, self.coordinates, self.momenta = system, coordinates, momenta
        self.rates, self.geometry = system.solve(coordinates, momenta)
        self.forces = system.forces(coordinates, self.rates, self.geometry)
        self.material = MaterialState(system, coordinates)
        self.step = difference_step
        neighbors, rates = [], []
        for multiple in [-2, -1, 1, 2]:
            shifted_rates, shifted_geometry = system.solve(coordinates+multiple*difference_step*self.rates,
                                                          momenta+multiple*difference_step*self.forces)
            neighbors.append(shifted_geometry)
            rates.append(shifted_rates)
        self.acceleration = (rates[0]-8*rates[1]+8*rates[2]-rates[3])/(12*difference_step)
        self.tangent_geometry = TangentGeometry(self.geometry, neighbors, difference_step, 1j*1e-24)

    def layer_data(self, offset):
        interpolation = self.material.interpolation([offset])[0]
        coordinates = interpolation @ self.coordinates
        rates = interpolation @ self.rates
        acceleration = interpolation @ self.acceleration
        layer = self.system.layer(offset, self.geometry)
        tangent_layer = self.system.layer(offset, self.tangent_geometry)
        step = 1e-24
        data = layer.evaluate(0., coordinates, rates)
        varied = tangent_layer.evaluate(0., coordinates.astype(complex)+1j*step*rates,
                                        rates.astype(complex)+1j*step*acceleration)
        momenta_dot = varied['momenta'].imag/step
        euler = momenta_dot[:-1]-data['scalar_covector']
        source_euler = momenta_dot[-1]-layer.source_covector(0., coordinates, rates)
        wave_source_euler = varied['field_momenta'][-1].imag/step-layer.source_covector(0., coordinates, rates, wave=True)
        nodal_dot = varied['nodal_dual'].imag/step
        return layer, coordinates, rates, acceleration, data, euler, source_euler, wave_source_euler, nodal_dot

    def regular_dual_dot(self, layer, coordinates, rates, acceleration, radius):
        step = 1e-24
        shape, radial, motion = layer.basis(radius, coordinates[-1])
        temporal = shape @ rates[:-1]+(motion @ coordinates[:-1])*rates[-1]
        gradient = radial @ coordinates[:-1]
        moved_coordinates = coordinates.astype(complex)+1j*step*rates
        moved_rates = rates.astype(complex)+1j*step*acceleration
        moved_shape, moved_radial, moved_motion = layer.basis(radius, moved_coordinates[-1])
        moved_temporal = moved_shape @ moved_rates[:-1]+(moved_motion @ moved_coordinates[:-1])*moved_rates[-1]
        moved_gradient = moved_radial @ moved_coordinates[:-1]
        temporal_dot, gradient_dot = moved_temporal.imag/step, moved_gradient.imag/step
        lapse, root = self.geometry.metric(radius)
        lapse_dot, root_dot = self.tangent_geometry.derivative(radius)
        coefficient = radius**2*lapse*root
        coefficient_dot = radius**2*(lapse_dot*root+lapse*root_dot)
        dual_dot = -radius**4*temporal*temporal_dot/coefficient**2
        dual_dot += radius**4*temporal**2*coefficient_dot/coefficient**3-gradient*gradient_dot
        return coefficient*dual_dot

    def wave_current(self, offset, target, retain_euler=True):
        layer, coordinates, rates, acceleration, data, euler, unused, unused2, nodal_dot = self.layer_data(offset)
        position = coordinates[-1]
        lower, upper = (layer.radii[0], min(target, layer.radii[-1])) if target < position else (max(target, layer.radii[0]), layer.radii[-1])
        if upper <= lower:
            return 0.
        extra = np.concatenate([layer.radii, self.geometry.edges, [position]])
        extra = extra[(extra > lower) & (extra < upper)]
        endpoints = np.unique(np.concatenate([[lower], extra, [upper]]))
        lengths = np.diff(endpoints)
        radius = (endpoints[:-1, None]+lengths[:, None]*layer.fractions).ravel()
        weights = (lengths[:, None]*layer.weights).ravel()
        regular = weights @ self.regular_dual_dot(layer, coordinates, rates, acceleration, radius)
        selected = layer.radii < target if target < position else layer.radii > target
        atoms = data['nodal']*nodal_dot
        if retain_euler:
            atoms = atoms+euler*rates[:-1]
        result = regular+np.sum(atoms[selected])
        return float(result if target < position else -result)

    def noether(self, offset):
        layer, coordinates, rates, acceleration, data, euler, source_euler, wave_euler, nodal_dot = self.layer_data(offset)
        regular = data['weight'] @ self.regular_dual_dot(layer, coordinates, rates, acceleration, data['radius'])
        atom = data['nodal'] @ nodal_dot
        cell = np.searchsorted(layer.radii, coordinates[-1])-1
        left_gradient = -coordinates[cell]/(coordinates[-1]-layer.radii[cell])
        right_gradient = coordinates[cell+1]/(layer.radii[cell+1]-coordinates[-1])
        coefficient = layer.coefficient(0., coordinates[-1])
        multiplier = 1+coordinates[-1]**4*rates[-1]**2/coefficient**2
        jump = -.5*multiplier*(left_gradient**2-right_gradient**2)
        interface = rates[-1]*coefficient*jump
        residual = euler @ rates[:-1]+rates[-1]*wave_euler+regular+atom+interface
        return dict(noether=float(abs(residual)), omitted_interface=float(abs(residual-interface)),
                    scalar_euler=float(np.max(abs(euler))), source_euler=float(abs(source_euler)),
                    interface_term=float(interface))

    def mass_current(self, targets, label_order=10, retain_euler=True):
        system = self.system
        points, weights = np.polynomial.legendre.leggauss(label_order)
        currents, wave_currents, source_currents = [], [], []
        bounds = self.coordinates[[0, -1], -1]
        for target in targets:
            cuts = (target-system.base)/system.width
            cuts = cuts[(cuts > -.5) & (cuts < .5)]
            if bounds[0] < target < bounds[1]:
                cuts = np.append(cuts, self.material.inverse_source(target))
            cuts = np.unique(np.concatenate([[-.5], cuts, [.5]]))
            current = 0.
            for lower, upper in zip(cuts[:-1], cuts[1:]):
                offsets = (lower+upper)/2+(upper-lower)/2*points
                values = np.array([self.wave_current(offset, target, retain_euler) for offset in offsets])
                current += (upper-lower)/2*np.dot(weights*material_weight(offsets), values)
            lapse, root = self.geometry.metric(target)
            wave = -system.coupling*root/lapse*current
            source = 0.
            if bounds[0] < target < bounds[1]:
                offset = self.material.inverse_source(target)
                interpolation = self.material.interpolation([offset])[0]
                velocity = interpolation @ self.rates[:, -1]
                clock = np.sqrt(lapse**2-velocity**2/root**2)
                source_momentum = system.source_mass*velocity/(root**2*clock)
                source = -system.coupling*lapse*root**3*source_momentum*material_weight(offset)/self.material.source_jacobian(offset)
            currents.append(wave+source)
            wave_currents.append(wave)
            source_currents.append(source)
        return np.array(currents), np.array(wave_currents), np.array(source_currents)

    def compare(self, targets, label_order=10):
        radial_derivative = self.tangent_geometry.derivative(np.asarray(targets), metric=False)[0]
        full, wave, source = self.mass_current(targets, label_order, retain_euler=True)
        on_shell, unused, unused2 = self.mass_current(targets, label_order, retain_euler=False)
        return dict(targets=np.asarray(targets), radial_time_derivative=radial_derivative, current=full,
                    on_shell_current=on_shell, wave=wave, source=source,
                    error=float(np.max(abs(radial_derivative-full))),
                    on_shell_error=float(np.max(abs(radial_derivative-on_shell))),
                    current_euler_correction=float(np.max(abs(full-on_shell))))
