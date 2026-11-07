from scaled_common import *


class ScaledSystem:
    def __init__(self, model, count=36, maximum=8):
        self.physical = ConsistentSystem(model, count, maximum)
        self.model, self.count, self.maximum = model, count, maximum
        self.basis, self.size = self.physical.basis, self.physical.size
        self.names, self.slices, self.neutrino = self.physical.names, self.physical.slices, self.physical.neutrino
        self.heat = self.physical.background(0.)['heat']
        assert self.heat > 0
        self.temperature = self.basis.temperature
        self.normalization = self.basis.number @ self.temperature
        self.number_row = self.basis.number / self.normalization
        self.complement = np.eye(count)[:, 1:]
        self.complement[0] -= self.basis.number[1:] / self.basis.number[0]
        self.projector = np.eye(count) - np.outer(self.temperature, self.number_row)
        self.shape_row = self.projector[1:]
        transform = np.eye(self.size)
        self.thermal_maps, self.shape_maps, self.inverse_masses = [], [], []
        for degree, names in enumerate(self.names):
            thermal = np.zeros((count, count))
            thermal[:, 0] = self.temperature
            shape = np.zeros((count, count))
            shape[:, 1:] = self.complement
            self.thermal_maps.append(linalg.block_diag(*([thermal] * len(names))))
            self.shape_maps.append(linalg.block_diag(*([shape] * len(names))))
            self.inverse_masses.append(linalg.block_diag(*([self.physical.mass_inverse * (2 * degree + 1)] * len(names))))
            for name in names:
                section = self.mode_slice(degree, name)
                transform[section, section] = thermal + self.heat * shape
        transform[10] = 0.
        transform[10, 10] = self.heat
        transform[10, self.mode_slice(0).start] = 1.
        self.transform = sparse.csc_matrix(transform)
        self.reference_readout = SpectralReadout(self.physical)
        self.inputs = [*self.physical.bank.inputs, *self.physical.ladder.inputs,
                       self.physical.geometry.source, self.physical.geometry.parent.source,
                       PARENT / 'consistent_system.py', PARENT / 'extended_system.py',
                       PARENT / 'consistent_spectral_basis.py', BATH_PARENT / 'mixed_wave_system.py',
                       THERMAL_PARENT / 'thermal_wave_system.py', THERMAL_PARENT / 'background_geometry.py']

    def mode_slice(self, degree, name='I'):
        return self.physical.mode_slice(degree, name)

    def physical_state(self, state):
        return self.transform @ state

    def initial(self):
        physical, provenance = self.physical.initial()
        state = physical.copy()
        for degree, names in enumerate(self.names):
            for name in names:
                section = self.mode_slice(degree, name)
                amplitude = physical[section.start] / self.temperature[0]
                state[section] = 0.
                state[section.start] = amplitude
        state[10] = 0.
        provenance.update(initial_shape_and_slip_zero_from_parent_thermal_initial_formula=True,
                          physical_reencoding_error=float(np.max(abs(self.physical_state(state) - physical))))
        return state, provenance

    def collision_parts(self, expansion, degree, local, background):
        physical, count, heat = self.physical, self.count, self.heat
        section = self.slices[degree]
        length = section.stop - section.start
        ratio = local['heat'] / heat
        redshift_change = ratio * physical.mass_inverse @ physical.redshift_weak @ background['profile']
        boost_change = ratio * physical.mass_inverse @ physical.boost_weak @ background['profile_prime']
        base = local['opacity'] / local['hubble'] * self.inverse_masses[degree] @ physical.ladder.at(local['theta'], degree)
        mixed = local['opacity'] / local['hubble'] * self.inverse_masses[degree] @ physical.bank.blocks[degree](expansion)
        thermal = self.thermal_maps[degree].copy()
        if degree == 0:
            thermal[:, 0] = 0.
        large, small, correction = [np.zeros((length, self.size), complex) for repeat in range(3)]
        large[:, section] = base @ thermal
        small[:, section] = base @ self.shape_maps[degree]
        correction[:, section] = mixed @ (self.thermal_maps[degree] + heat * self.shape_maps[degree])
        equilibrium = np.r_[self.temperature, np.zeros(length - count)]
        if degree == 0:
            small[:, 10] -= base @ equilibrium
            thermal_mixed = local['opacity'] / local['hubble'] * physical.mass_inverse @ physical.bank.temperature(expansion)
            correction[:count, self.mode_slice(0).start] += thermal_mixed
            correction[:count, 10] += heat * thermal_mixed
            assert np.max(abs(large[:count])) == 0.
        if degree == 1:
            change = np.r_[redshift_change, np.zeros(length - count)]
            large[:, 9] -= base @ equilibrium
            small[:, 9] -= base @ change
            small[:count, 9] += boost_change
            correction[:, 9] -= mixed @ (equilibrium + heat * change)
        return large, small, correction

    def matrices(self, expansion):
        physical, heat = self.physical, self.heat
        local, energy, current, transverse, longitudinal = physical.stress_rows(expansion)
        energy, current, transverse, longitudinal = [np.asarray(self.transform.T @ row).ravel() for row in [energy, current, transverse, longitudinal]]
        hubble, scale, inertia, ratio = local['hubble'], local['scale'], local['inertia'], local['temperature_ratio']
        background = self.reference_readout.background(expansion)
        heat_ratio = local['heat'] / heat
        redshift_change = heat_ratio * physical.mass_inverse @ physical.redshift_weak @ background['profile']
        derivative = heat_ratio * background['profile_prime']
        mass = np.eye(self.size)
        mass[9, 9] = inertia
        mass[10] = 0.
        mass[10, 10] = heat
        mass[10, self.mode_slice(0).start] = 1.
        operator, delta = [np.zeros((self.size, self.size), complex) for repeat in range(2)]
        collision = []
        for degree, names in enumerate(self.names):
            large, small, correction = self.collision_parts(expansion, degree, local, background)
            collision.append((large.copy(), small.copy(), correction.copy()))
            if degree == 0:
                small[:self.count] += np.outer(derivative, physical.density_row)
            for index, name in enumerate(names):
                target = self.mode_slice(degree, name)
                source = slice(index * self.count, (index + 1) * self.count)
                operator[target.start] += self.number_row @ large[source] + heat * (self.number_row @ small[source])
                operator[target.start + 1:target.stop] += (self.shape_row @ large[source]) / heat + self.shape_row @ small[source]
                delta[target.start] += heat * (self.number_row @ correction[source])
                delta[target.start + 1:target.stop] += self.shape_row @ correction[source]
        large, small, correction = collision[0]
        operator[10] -= self.basis.energy @ small[:self.count] / heat_ratio
        delta[10] -= self.basis.energy @ correction[:self.count] / heat_ratio
        compression = np.zeros(self.size, complex)
        compression[[2, 3, 9]] = [2 / hubble, 1 / hubble, 1j * physical.momentum / hubble]
        operator[10] -= 2 * ratio / 3 * compression
        operator[10, self.mode_slice(0).start] -= 1.
        operator[10, 10] -= heat
        large, small, correction = collision[1]
        operator[9] -= self.basis.energy @ (large[:self.count] + heat * small[:self.count]) / 3
        delta[9] -= heat * self.basis.energy @ correction[:self.count] / 3
        inertia_prime = local['baryon'] / local['photon_reference'] + 5 * local['heat'] * local['ratio_prime'] / 3
        operator[9, 9] -= inertia_prime
        pressure = ratio * physical.density_row.copy()
        pressure[self.mode_slice(0).start] += 1.
        pressure[10] += heat
        operator[9] -= 1j * physical.momentum / hubble * 2 * local['heat'] / 3 * pressure
        for degree, names in enumerate(self.names):
            for name in names:
                spin = 2 if name in ['E', 'B'] else 0
                section = self.mode_slice(degree, name)
                if degree > spin:
                    coupling = math.sqrt(degree ** 2 - spin ** 2) / (2 * degree - 1)
                    operator[section, self.mode_slice(degree - 1, name)] -= 1j * physical.momentum / hubble * coupling * np.eye(self.count)
                if degree < self.maximum:
                    coupling = math.sqrt((degree + 1) ** 2 - spin ** 2) / (2 * degree + 3)
                    operator[section, self.mode_slice(degree + 1, name)] -= 1j * physical.momentum / hubble * coupling * np.eye(self.count)
        for degree, rates in [(0, [-2 / 3, -1 / 3]), (2, [2 / 3, -2 / 3])]:
            section = self.mode_slice(degree)
            for column, coefficient in zip([2, 3], rates):
                operator[section.start, column] += coefficient / hubble * (1 + heat * self.number_row @ redshift_change)
                operator[section.start + 1:section.stop, column] += coefficient / hubble * (self.shape_row @ redshift_change)
        for degree in range(self.maximum + 1):
            index = self.neutrino.start + degree
            if degree:
                operator[index, index - 1] -= 1j * physical.momentum / hubble * degree / (2 * degree - 1)
            if degree < self.maximum:
                operator[index, index + 1] -= 1j * physical.momentum / hubble * (degree + 1) / (2 * degree + 3)
        operator[self.neutrino.start, [2, 3]] -= np.array([8 / 3, 4 / 3]) / hubble
        operator[self.neutrino.start + 2, [2, 3]] += np.array([8 / 3, -8 / 3]) / hubble
        operator[8, 9] = -1j * physical.momentum / hubble
        operator[0, 2], operator[1, 3] = 2 / hubble, 2 / hubble
        operator[2] += scale ** 2 * (energy - longitudinal) / (2 * hubble)
        operator[3] += scale ** 2 * (energy + longitudinal - 2 * transverse) / (2 * hubble)
        operator[2, [0, 2, 3]] += [-physical.momentum ** 2 / (2 * hubble), -4., -1.]
        operator[3, [0, 2, 3]] += [-physical.momentum ** 2 / hubble, -2., -3.]
        for field in range(2):
            operator[4 + field, 6 + field] = 1 / hubble
            operator[6 + field, 4 + field] = -(physical.momentum ** 2 + scale ** 2 * physical.geometry.mass2[field]) / hubble
            operator[6 + field, 6 + field] = -2.
            operator[6 + field, [2, 3]] -= local['prime'][field] * np.array([2., 1.]) / hubble
        return sparse.csc_matrix(mass), sparse.csc_matrix(operator), sparse.csc_matrix(delta)

    def readout(self, expansion, state):
        background = self.reference_readout.background(expansion)
        ratio = background['heat'] / self.heat
        dilation_change = ratio * background['dilation_change']
        projected_change = self.projector @ dilation_change
        density = self.physical.density_row @ state
        velocity = state[9]
        shapes, temperatures = [], []
        for degree, names in enumerate(self.names):
            for name in names:
                section = self.mode_slice(degree, name)
                amplitude = state[section.start]
                departure = self.complement @ state[section.start + 1:section.stop]
                if name == 'I' and degree == 0:
                    amplitude -= density / 3
                    departure += ratio * (background['profile_prime'] - background['dilation_change']) * density / 3
                if name == 'I' and degree == 1:
                    amplitude -= velocity
                    departure -= dilation_change * velocity
                temperature = (amplitude + self.heat * self.number_row @ departure) / (1 + self.heat * self.number_row @ dilation_change)
                shapes.append(self.heat * (self.projector @ departure - temperature * projected_change))
                temperatures.append(temperature)
        return dict(shapes=np.asarray(shapes), temperatures=np.asarray(temperatures), density=density, velocity=velocity)

    def constraints(self, expansion, state):
        return self.physical.constraints(expansion, self.physical_state(state))
