from thermal_wave_common import *
from kernel_ladder import KernelLadder
from background_geometry import ConservedThermalBackground
sys.path.insert(0, str(PARENT))
from cold_control import exact_cold
sys.path.insert(0, str(WAVES))
from coupled_system import CoupledSystem
from initial_state import initial_state


class ThermalWaveSystem:
    def __init__(self, model, count=16, maximum=8, control='physical'):
        self.ladder = KernelLadder(count)
        self.basis = self.ladder.basis
        self.count, self.maximum, self.control = count, maximum, control
        name = model + str(count) + ('-1600' if count == 16 else '-3200')
        self.geometry = ConservedThermalBackground(model, name, amplitude=0. if control == 'dust' else None)
        self.model = model
        self.momentum = .1
        self.slices, self.names = [], []
        index = 11
        for degree in range(maximum + 1):
            names = ['I', 'V'] if degree < 2 else ['I', 'E', 'B', 'V']
            self.names.append(names)
            self.slices.append(slice(index, index + count * len(names)))
            index += count * len(names)
        self.neutrino = slice(index, index + maximum + 1)
        self.size = self.neutrino.stop
        values = self.basis.values
        derivative = self.basis.derivative(self.basis.nodes)
        self.redshift_weak = ((3 * values + self.basis.nodes[:, None] * derivative).T * self.basis.measure) @ values
        self.boost_weak = ((2 * values + self.basis.nodes[:, None] * derivative).T * self.basis.measure) @ values
        self.mass_inverse = linalg.inv(self.basis.mass)
        self.density_row = np.zeros(self.size, complex)
        self.density_row[[0, 1, 8]] = [-1., -.5, 1.]

    def mode_slice(self, degree, name='I'):
        mode = self.names[degree].index(name)
        first = self.slices[degree].start + mode * self.count
        return slice(first, first + self.count)

    def background(self, expansion):
        state = self.geometry.at(expansion)
        if self.control == 'dust':
            state.update(temperature_ratio=1., ratio_prime=0., photon_energy_scaled=0., photon_energy_prime=0.)
        return state

    def spectral_background(self, expansion, local):
        if self.control == 'dust':
            return self.basis.temperature.copy(), np.zeros(self.count), np.zeros(self.count)
        coefficients = self.geometry.profiles(expansion)
        derivative = self.geometry.profiles(expansion, 1)
        vectors = np.column_stack([self.basis.chemical, self.basis.temperature])
        moments = np.vstack([self.basis.number, self.basis.energy])
        correction = linalg.solve(moments @ vectors,
                                  np.array([-self.basis.number @ coefficients,
                                            local['photon_energy_scaled'] - self.basis.energy @ coefficients]))
        coefficients = coefficients + vectors @ correction
        derivative_correction = linalg.solve(moments @ vectors,
                                             np.array([-self.basis.number @ derivative,
                                                       local['photon_energy_prime'] - self.basis.energy @ derivative]))
        derivative = derivative + vectors @ derivative_correction
        heat = local['heat']
        redshift = self.basis.temperature + heat * self.mass_inverse @ self.redshift_weak @ coefficients
        collision = heat * local['hubble'] * derivative
        boost = self.mass_inverse @ self.boost_weak @ collision
        return redshift, collision, boost

    def stress_rows(self, expansion):
        local = self.background(expansion)
        volume = np.zeros(self.size, complex)
        volume[[0, 1]] = [1., .5]
        thermal_density = local['temperature_ratio'] * self.density_row.copy()
        thermal_density[10] += 1.
        thermal_density *= local['heat'] * local['photon_reference']
        photon_energy = np.zeros(self.size, complex)
        photon_energy[self.mode_slice(0)] = self.basis.energy * local['photon_reference']
        photon_shear = np.zeros(self.size, complex)
        photon_shear[self.mode_slice(2)] = self.basis.energy * local['photon_reference'] / 15
        neutrino_energy = np.zeros(self.size, complex)
        neutrino_energy[self.neutrino.start] = local['neutrino']
        neutrino_shear = np.zeros(self.size, complex)
        neutrino_shear[self.neutrino.start + 2] = local['neutrino'] / 15
        kinetic, potential = np.zeros(self.size, complex), np.zeros(self.size, complex)
        kinetic[6:8] = local['prime'] / local['scale'] ** 2
        potential[4:6] = self.geometry.mass2 * local['fields']
        energy = (-local['cold'] * volume + local['baryon'] * self.density_row + thermal_density
                  + photon_energy + neutrino_energy + kinetic + potential)
        transverse = ((photon_energy + neutrino_energy) / 3 - photon_shear - neutrino_shear
                      + 2 * thermal_density / 3 + kinetic - potential)
        longitudinal = transverse + 3 * (photon_shear + neutrino_shear)
        current = np.zeros(self.size, complex)
        current[9] = local['photon_reference'] * local['inertia']
        current[self.mode_slice(1)] = local['photon_reference'] * self.basis.energy / 3
        current[self.neutrino.start + 1] = local['neutrino'] / 3
        current[4:6] = -1j * self.momentum * local['prime'] / local['scale'] ** 2
        return local, energy, current, transverse, longitudinal

    def matrices(self, expansion):
        local, energy, current, transverse, longitudinal = self.stress_rows(expansion)
        hubble, scale = local['hubble'], local['scale']
        heat, inertia, ratio = local['heat'], local['inertia'], local['temperature_ratio']
        redshift, background_collision, boost = self.spectral_background(expansion, local)
        operator = np.zeros((self.size, self.size), complex)
        mass = np.eye(self.size)
        for degree, section in enumerate(self.slices):
            angular_mass = self.basis.mass / (2 * degree + 1)
            modes = len(self.names[degree])
            if self.control == 'dust' or (self.control == 'matched-elastic' and degree > 0):
                stiffness = np.kron(exact_cold(degree), angular_mass)
            else:
                stiffness = self.ladder.at(local['theta'], degree)
            full_mass = linalg.block_diag(*([angular_mass] * modes))
            collision = local['opacity'] * linalg.solve(full_mass, stiffness, assume_a='pos')
            operator[section, section] = collision
            mass[section, section] = full_mass
            if degree in [0, 1]:
                equilibrium = np.r_[self.basis.temperature if degree == 0 else redshift, np.zeros((modes - 1) * self.count)]
                operator[section, 10 if degree == 0 else 9] -= collision @ equilibrium
        first, dipole = self.mode_slice(0), self.mode_slice(1)
        operator[first] += np.outer(background_collision, self.density_row)
        operator[dipole, 9] += boost
        photon_heat_source = self.basis.energy @ operator[first]
        photon_momentum_source = self.basis.energy @ operator[dipole] / 3
        compression = np.zeros(self.size, complex)
        compression[[2, 3, 9]] = [2., 1., 1j * self.momentum]
        if heat:
            operator[10] = -photon_heat_source / heat - (2 * ratio / 3) * compression
            operator[10, 10] -= hubble
            gas_background_heat = -self.basis.energy @ background_collision
            operator[10] -= gas_background_heat / heat * self.density_row
            mass[10, 10] = heat
        else:
            operator[10] = -(2 / 3) * compression
            operator[10, 10] -= hubble
        operator[9] = -photon_momentum_source / inertia
        inertia_prime = hubble * (local['baryon'] / local['photon_reference'] + 5 * heat * local['ratio_prime'] / 3)
        operator[9, 9] -= inertia_prime / inertia
        pressure = ratio * self.density_row.copy()
        pressure[10] += 1.
        operator[9] -= 1j * self.momentum * (2 * heat / (3 * inertia)) * pressure
        mass[9, 9] = inertia
        for degree, names in enumerate(self.names):
            for name in names:
                spin = 2 if name in ['E', 'B'] else 0
                section = self.mode_slice(degree, name)
                if degree > spin:
                    coupling = math.sqrt(degree ** 2 - spin ** 2) / (2 * degree - 1)
                    operator[section, self.mode_slice(degree - 1, name)] -= 1j * self.momentum * coupling * np.eye(self.count)
                if degree < self.maximum:
                    coupling = math.sqrt((degree + 1) ** 2 - spin ** 2) / (2 * degree + 3)
                    operator[section, self.mode_slice(degree + 1, name)] -= 1j * self.momentum * coupling * np.eye(self.count)
        operator[first, 2] -= 2 * redshift / 3
        operator[first, 3] -= redshift / 3
        operator[self.mode_slice(2), 2] += 2 * redshift / 3
        operator[self.mode_slice(2), 3] -= 2 * redshift / 3
        for degree in range(self.maximum + 1):
            index = self.neutrino.start + degree
            if degree:
                operator[index, index - 1] -= 1j * self.momentum * degree / (2 * degree - 1)
            if degree < self.maximum:
                operator[index, index + 1] -= 1j * self.momentum * (degree + 1) / (2 * degree + 3)
        operator[self.neutrino.start, [2, 3]] -= [8 / 3, 4 / 3]
        operator[self.neutrino.start + 2, [2, 3]] += [8 / 3, -8 / 3]
        operator[8, 9] = -1j * self.momentum
        operator[0, 2], operator[1, 3] = 2., 2.
        operator[2] += scale ** 2 * (energy - longitudinal) / 2
        operator[3] += scale ** 2 * (energy + longitudinal - 2 * transverse) / 2
        operator[2, [0, 2, 3]] += [-self.momentum ** 2 / 2, -4 * hubble, -hubble]
        operator[3, [0, 2, 3]] += [-self.momentum ** 2, -2 * hubble, -3 * hubble]
        for field in range(2):
            operator[4 + field, 6 + field] = 1.
            operator[6 + field, 4 + field] = -(self.momentum ** 2 + scale ** 2 * self.geometry.mass2[field])
            operator[6 + field, 6 + field] = -2 * hubble
            operator[6 + field, [2, 3]] -= local['prime'][field] * np.array([2., 1.])
        weighted = operator / hubble
        weighted[9] *= inertia
        if heat:
            weighted[10] *= heat
        for degree, section in enumerate(self.slices):
            full_mass = linalg.block_diag(*([self.basis.mass / (2 * degree + 1)] * len(self.names[degree])))
            weighted[section] = full_mass @ weighted[section]
        return sparse.csc_matrix(mass), sparse.csc_matrix(weighted), operator

    def constraints(self, expansion, state):
        local, energy, current, _, _ = self.stress_rows(expansion)
        hamiltonian = 2 * self.momentum ** 2 * state[0] + 4 * local['hubble'] * (2 * state[2] + state[3]) - 2 * local['scale'] ** 2 * (energy @ state)
        momentum = 2j * self.momentum * state[2] - local['scale'] ** 2 * (current @ state)
        scale = max(abs(2 * self.momentum ** 2 * state[0]), abs(2 * local['scale'] ** 2 * (energy @ state)), 1e-30)
        return np.array([hamiltonian, momentum]), scale

    def initial(self):
        inherited = CoupledSystem(self.geometry.parent, self.maximum)
        moment, states, provenance = initial_state(inherited, self.geometry.thermal.start_scale)
        source = inherited.unpack(states[0])
        state = np.zeros(self.size, complex)
        state[:4] = [source['metric'][1, 1], source['metric'][0, 0], source['rate'][1, 1], source['rate'][0, 0]]
        state[4:8] = np.r_[source['field'], source['prime']]
        state[8:10] = [source['number'], source['velocity'][0]]
        axis = np.array([1., 0., 0.])
        for degree in range(self.maximum + 1):
            tensors, names = prior.modal_tensors(inherited.directions, axis, degree)
            coefficients = (2 * degree + 1) / 4 * np.einsum('n,anij,nji->a', inherited.weights, tensors, source['photon'])
            for mode, name in enumerate(names):
                state[self.mode_slice(degree, name)] = coefficients[mode] * self.basis.temperature
            legendre = special.eval_legendre(degree, inherited.directions[:, 0])
            state[self.neutrino.start + degree] = (2 * degree + 1) * np.dot(inherited.weights * legendre, source['neutrino'])
        state[10] = self.basis.energy @ state[self.mode_slice(0)] / (self.basis.energy @ self.basis.temperature)
        local, energy, current, _, _ = self.stress_rows(0.)
        state[2] = local['scale'] ** 2 * (current @ state) / (2j * self.momentum)
        trace_rate = (local['scale'] ** 2 * (energy @ state) - self.momentum ** 2 * state[0]) / (2 * local['hubble'])
        state[3] = trace_rate - 2 * state[2]
        return state, dict(parent_initial_constraints=provenance, initial_only_rate_constraint_solve=True,
                           physical_thermal_initial_state=self.control != 'dust')

    def features(self, expansion, state):
        volume = state[0] + state[1] / 2
        energy = self.basis.energy
        return np.r_[-volume, state[8] - volume, energy @ state[self.mode_slice(0)],
                     state[self.neutrino.start], energy @ state[self.mode_slice(1)] / 3,
                     state[self.neutrino.start + 1] / 3, state[9], state[10], state[4:8]]
