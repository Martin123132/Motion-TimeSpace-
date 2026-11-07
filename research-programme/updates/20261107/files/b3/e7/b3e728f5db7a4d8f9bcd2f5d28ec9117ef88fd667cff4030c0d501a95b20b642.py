from mixed_common import *
from mixed_wave_system import MixedSystem


class RelaxedSource:
    def __init__(self, system):
        folder = ROOT / 'backgrounds' / system.model
        packet = json.loads((folder / 'status.json').read_text())
        assert packet['all_checks_passed']
        self.inputs = [folder / 'status.json', folder / 'history.npz']
        with np.load(folder / 'history.npz') as saved:
            self.profile = interpolate.CubicSpline(saved['expansion'], saved['profiles'])
            self.temperature = interpolate.CubicSpline(saved['expansion'], saved['temperature'])
            self.integral = interpolate.CubicSpline(saved['expansion'], saved['temperature_integral'])
        self.system = system
        basis = system.basis
        vectors = np.column_stack([basis.chemical, basis.temperature])
        self.lift = vectors @ linalg.inv(np.vstack([basis.number, basis.energy]) @ vectors)

    def at(self, expansion):
        system = self.system
        heat = system.background(expansion)['heat']
        profile, derivative = self.profile(expansion), self.profile(expansion, 1)
        thermal, thermal_prime = float(self.temperature(expansion)), float(self.temperature(expansion, 1))
        energy = -heat * (thermal + float(self.integral(expansion)))
        energy_prime = -heat * (thermal + thermal_prime)
        profile += self.lift @ np.array([-system.basis.number @ profile, energy - system.basis.energy @ profile])
        derivative += self.lift @ np.array([-system.basis.number @ derivative, energy_prime - system.basis.energy @ derivative])
        return profile, derivative, thermal, thermal_prime

    def operator(self, expansion):
        system = self.system
        local = system.background(expansion)
        profile, derivative, thermal, thermal_prime = self.at(expansion)
        heat, hubble = local['heat'], local['hubble']
        weak = np.zeros((system.size, system.size), complex)
        first, dipole, second = system.mode_slice(0), system.mode_slice(1), system.mode_slice(2)
        source = system.basis.mass @ derivative
        redshift = system.mass_inverse @ system.redshift_weak @ profile
        weak[first] += np.outer(source, system.density_row)
        weak[dipole, 9] += system.boost_weak @ derivative / 3
        collision = system.ladder.at(local['theta'], 1)
        equilibrium = np.r_[redshift, np.zeros(system.count)]
        weak[system.slices[1], 9] -= local['opacity'] / hubble * collision @ equilibrium
        photon_heat = system.basis.energy @ system.mass_inverse @ weak[first]
        photon_momentum = system.basis.energy @ system.mass_inverse @ weak[dipole]
        weak[10] = -photon_heat + (system.basis.energy @ derivative) * system.density_row
        weak[9] = -photon_momentum
        redshift_weak = system.basis.mass @ redshift / hubble
        weak[first, 2] -= 2 * redshift_weak / 3
        weak[first, 3] -= redshift_weak / 3
        weak[second, 2] += 2 * redshift_weak / 15
        weak[second, 3] -= 2 * redshift_weak / 15
        compression = np.zeros(system.size, complex)
        compression[[2, 3, 9]] = [2., 1., 1j * system.momentum]
        weak[10] -= 2 * heat * thermal * compression / (3 * hubble)
        weak[9] -= 1j * system.momentum * 2 * heat * thermal * system.density_row / (3 * hubble)
        return sparse.csc_matrix(weak)
