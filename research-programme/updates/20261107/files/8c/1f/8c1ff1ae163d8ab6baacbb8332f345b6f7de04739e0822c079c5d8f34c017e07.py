from thermal_wave_common import *
from stable_spectral_basis import load_basis
sys.path.insert(0, str(THERMAL))
from flrw_thermal_response import state_at_scale


class ConservedThermalBackground:
    def __init__(self, model, name, amplitude=None):
        self.thermal = thermal.ThermalBackground(model)
        self.parent = self.thermal.parent
        self.source = ROOT / 'backgrounds' / name / 'history.npz'
        packet = json.loads((self.source.parent / 'status.json').read_text())
        assert packet['all_checks_passed']
        self.basis = load_basis(ROOT / 'banks' / ('stable' + str(packet['basis_count']) + '-late'))
        with np.load(self.source) as saved:
            self.expansion = saved['expansion']
            self.profiles = interpolate.CubicSpline(self.expansion, saved['profiles'])
            self.temperature = interpolate.CubicSpline(self.expansion, saved['temperature_scaled'])
            self.heat = float(saved['heat'])
            self.discrete_energy = saved['energy_scaled']
        self.work_integral = self.temperature.antiderivative()
        self.amplitude = self.heat if amplitude is None else amplitude
        self.initial = state_at_scale(self.thermal, self.thermal.start_scale)
        self.mass2 = self.parent.masses ** 2
        start = np.r_[self.initial['fields'], self.initial['prime'], 0., 0.]
        self.solution = integrate.solve_ivp(self.rhs, (0., self.thermal.end), start, method='DOP853',
                                            rtol=2e-12, atol=1e-28, max_step=.008, dense_output=True)
        assert self.solution.success

    def thermal_source(self, expansion):
        temperature = float(self.temperature(expansion))
        work = expansion + self.heat * float(self.work_integral(expansion) - self.work_integral(0.))
        energy = -work - self.heat * temperature
        energy_prime = -1 - self.heat * temperature - self.heat * float(self.temperature(expansion, 1))
        return energy, temperature, energy_prime

    def at(self, expansion, state=None):
        if state is None:
            state = self.solution.sol(expansion)
        scale = self.thermal.start_scale * math.exp(expansion)
        reference = self.parent.photons / scale ** 4
        energy, temperature, energy_prime = self.thermal_source(expansion)
        fields, prime = state[:2], state[2:4]
        gas_internal = self.amplitude * reference * (1 + self.heat * temperature)
        photons = reference * (1 + self.amplitude * energy)
        baryons, cold = self.parent.baryons / scale ** 3, self.parent.cold / scale ** 3
        neutrinos = self.parent.neutrinos / scale ** 4
        scalar_energy = np.sum(prime ** 2 / scale ** 2 + self.mass2 * fields ** 2) / 2
        scalar_pressure = np.sum(prime ** 2 / scale ** 2 - self.mass2 * fields ** 2) / 2
        density = baryons + cold + photons + neutrinos + gas_internal + scalar_energy
        pressure = (photons + neutrinos) / 3 + 2 * gas_internal / 3 + scalar_pressure
        hubble = scale * math.sqrt(density / 3)
        return dict(scale=scale, photon_reference=reference, photon=photons, baryon=baryons, cold=cold,
                    neutrino=neutrinos, internal=gas_internal, fields=fields, prime=prime, hubble=hubble,
                    density=density, pressure=pressure, opacity=self.parent.opacity_constant / scale ** 2,
                    theta=self.thermal.theta0 / scale, temperature_ratio=1 + self.heat * temperature,
                    ratio_prime=self.heat * float(self.temperature(expansion, 1)),
                    photon_energy_scaled=energy, photon_energy_prime=energy_prime,
                    heat=self.amplitude, physical_heat=self.heat,
                    inertia=(baryons + 5 * gas_internal / 3) / reference)

    def rhs(self, expansion, state):
        background = self.at(expansion, state)
        scale, hubble = background['scale'], background['hubble']
        return np.r_[state[2:4] / hubble, -2 * state[2:4] - scale ** 2 * self.mass2 * state[:2] / hubble,
                     1 / hubble, scale / hubble]
