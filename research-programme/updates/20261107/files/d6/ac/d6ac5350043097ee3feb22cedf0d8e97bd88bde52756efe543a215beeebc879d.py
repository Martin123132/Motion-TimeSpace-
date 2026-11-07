from common import *
import numpy as np
import sympy as sp
import ctypes

SPECIES = ('cdm', 'baryon', 'photon', 'massless_neutrino', 'massive_neutrino', 'slow_scalar', 'heavy_scalar')
GROUPS = ('photon_baryon', 'massless_neutrino', 'massive_neutrino')


def symbolic():
    speed, hubble, wave, phi, psi, alpha, hubble_n = sp.symbols('v H k Phi Psi alpha H_N', positive=True)
    checks = dict(
        massive_weight_rate=sp.simplify(-(1 + speed**2) / 2 - (1 - speed**2) + (3 - speed**2) / 2),
        massive_dipole_source=sp.simplify(speed * (speed * wave * 4 * phi / (3 * hubble) + 4 * wave * psi / (3 * hubble * speed)) - 4 * wave * (speed**2 * phi + psi) / (3 * hubble)),
        massive_normal_dipole_alpha=sp.simplify(4 * speed * wave * alpha / 3 - 4 * wave * alpha / (3 * speed) + 4 * wave * (1 - speed**2) * alpha / (3 * speed)))
    degree = sp.symbols('ell', integer=True, positive=True)
    checks['streaming_pair'] = sp.simplify((2 * degree + 1) * (degree + 1) / (2 * degree + 1) - (2 * degree + 3) * (degree + 1) / (2 * degree + 3))
    gradient = sp.Matrix(sp.symbols('gx gy gz', real=True))
    tensor = gradient * gradient.T - sp.eye(3) * gradient.dot(gradient) / 3
    checks['scalar_shear_frobenius'] = sp.simplify(sp.trace(tensor.T * tensor) - sp.Rational(2, 3) * gradient.dot(gradient)**2)
    require(all(value == 0 for value in checks.values()), 'symbolic shear identities')
    return {name: str(value) for name, value in checks.items()}


class StressEnergy:
    def __init__(self, system, energy):
        self.system, self.energy = system, energy
        signature = system.context['signature_values']
        self.ufa = bool(signature[12])
        self.photon = np.array([energy.slot(int(signature[3]) + degree) for degree in range(int(signature[6]) + 1)])
        self.polar = np.array([energy.slot(int(signature[5]) + degree) for degree in range(2, int(signature[7]) + 1)])
        self.massless = np.array([energy.slot(int(signature[4]) + degree) for degree in range((2 if self.ufa else int(signature[8])) + 1)])
        self.baryon = energy.slot(4)
        self.massive = np.array([[energy.moment_slot(degree, node) for node in range(5)] for degree in range(3)])

    def background(self, scale):
        scale = np.atleast_1d(scale)
        density = self.energy.fluid_origin[None, :] * (self.energy.origin_scale / scale[:, None])**np.array([1., 1., 2., 2.])
        speeds = 1 / np.sqrt(1 + (scale[:, None] / self.energy.origin_scale)**2 * (1 / self.energy.speeds_origin**2 - 1))
        massive = np.array(self.energy.massive_origin)[None, :] * (self.energy.origin_scale / scale[:, None])**2 * self.energy.speeds_origin / speeds
        return density, speeds, massive

    def weights(self, density):
        photon_angles = 2 * np.arange(len(self.photon)) + 1.
        photon_angles[-1] = len(self.photon) - 1.
        radiation_angles = 2 * np.arange(len(self.massless)) + 1.
        radiation_angles[-1] = 2. if self.ufa else len(self.massless) - 1.
        degrees = np.arange(2, len(self.polar) + 2)
        polar_angles = (2 * degrees + 1.) * (degrees + 1) * (degrees + 2) / (degrees * (degrees - 1))
        degree = int(degrees[-1])
        polar_angles[-1] = ((2 * degree - 1) * degree * (degree + 1) / ((degree - 1) * (degree - 2))) * ((degree + 2) * (degree - 2) / (degree * (2 * degree - 1))) / (degree / (degree - 2))
        return (np.sqrt(density[:, 2, None] * photon_angles / 4),
                np.sqrt(density[:, 2, None] * polar_angles / 4),
                np.sqrt(density[:, 3, None] * radiation_angles / 4))

    def histories(self, reference):
        state, hubble, scale = reference['evolved_state'], reference['H'], reference['a']
        values = {name: reference['values'][:, index] for index, name in enumerate(reference['value_names'])}
        phi, psi = values['Phi'], values['Psi']
        alpha = state[:, self.system.alpha_slot]
        density, speeds, massive = self.background(scale)
        photon_weights, polar_weights, radiation_weights = self.weights(density)
        photon = state[:, self.photon].copy()
        photon[:, 0] -= 4 * hubble * alpha + 4 * phi
        photon[:, 1] += 4 * self.system.wave * alpha / 3
        photon *= photon_weights
        baryon = np.sqrt(density[:, 1]) * (state[:, self.baryon] + self.system.wave * alpha)
        polar = state[:, self.polar] * polar_weights
        radiation = state[:, self.massless].copy()
        radiation[:, 0] -= 4 * hubble * alpha + 4 * phi
        radiation[:, 1] += 4 * self.system.wave * alpha / 3
        if self.ufa:
            radiation[:, 2] += 4 * phi
        radiation *= radiation_weights
        massive_squared = np.zeros(len(scale))
        for degree in range(193):
            moments = state[:, self.massive[degree]].copy() if degree < 3 else state[:, self.energy.size + (degree - 3) * 5:self.energy.size + (degree - 2) * 5].copy()
            if degree == 0:
                moments -= 4 * (hubble * alpha + phi)[:, None]
            if degree == 1:
                moments += 4 * self.system.wave * alpha[:, None] / (3 * speeds)
            massive_squared += np.sum(massive * speeds**2 * (2 * degree + 1) * moments**2 / 4, axis=1)
        norms = np.column_stack((np.sqrt(baryon**2 + np.sum(photon**2, axis=1) + np.sum(polar**2, axis=1)),
                                 np.linalg.norm(radiation, axis=1), np.sqrt(massive_squared)))
        factors = np.column_stack((np.sqrt(4 * density[:, 2] / 5), np.sqrt((2 if self.ufa else 4 / 5) * density[:, 3]),
                                   np.sqrt(4 / 5 * np.sum(massive * speeds**2, axis=1))))
        endpoints = np.zeros_like(norms)
        if self.ufa:
            endpoints[:, 1] = 4 * density[:, 3] * abs(phi)
        pressure = reference['terms'][:, 1, 2] / density[:, 1]
        hubble_n = self.system.background_spline(reference['efold'], 1)[:, 0]
        source = np.zeros((len(scale), 3, 5))
        source[:, 0, 0] = np.sqrt(density[:, 1]) * self.system.wave / hubble * (psi + pressure)
        source[:, 0, 1] = 2 / np.sqrt(3) * np.sqrt(density[:, 2]) * self.system.wave / hubble * (phi + psi)
        source[:, 1, 0] = 2 / np.sqrt(3) * np.sqrt(density[:, 3]) * self.system.wave / hubble * ((3 if self.ufa else 1) * phi + psi)
        if self.ufa:
            source[:, 1, 1] = np.sqrt(density[:, 3] / 2) * (12 * phi / (hubble * reference['times']) - 4 * psi - 4 * (hubble_n - hubble) * alpha)
        source[:, 2] = 2 / np.sqrt(3) * np.sqrt(massive) * self.system.wave / hubble[:, None] * (speeds**2 * phi[:, None] + psi[:, None])
        return dict(norms=norms, factors=factors, endpoints=endpoints, source=source,
                    density=density, speeds=speeds, massive=massive)

    def qualification(self, efold, state):
        system, energy = self.system, self.energy
        derivative, values, rates, info, _, terms = system.evaluate(efold, state, 'gr')
        transform, _, logarithmic, _ = energy.blocks(efold)
        core = transform @ (state[:energy.size] / system.units[:energy.size])
        core_rate = transform @ (derivative[:energy.size] / system.units[:energy.size]) + logarithmic @ core
        density, speeds, massive = [value[0] for value in self.background([info['scale']])]
        photon_weights, polar_weights, radiation_weights = [value[0] for value in self.weights(density[None, :])]
        phi, psi, phi_n = values['Phi'], values['Psi'], rates['Phi'] / info['H']
        hubble, wave = info['H'], system.wave
        tau = system.context['point'](efold)[11]
        callback = system.context['lib'].mts_bridge_thermal_read
        pointer = ctypes.POINTER(ctypes.c_double)
        callback.argtypes, callback.restype = [ctypes.c_double, pointer], None
        thermal = np.zeros(6)
        callback(float(tau), thermal.ctypes.data_as(pointer))
        opacity = thermal[4] / hubble
        require(opacity >= 0, 'nonnegative Thomson opacity')
        photon = core[self.photon].copy()
        photon_rate = core_rate[self.photon].copy()
        photon[0] -= 4 * photon_weights[0] * phi
        photon_rate[0] -= 4 * photon_weights[0] * (phi_n - phi)
        group = np.r_[core[self.baryon], photon, core[self.polar]]
        group_rate = np.r_[core_rate[self.baryon], photon_rate, core_rate[self.polar]]
        weights = np.r_[np.sqrt(density[1]), photon_weights, polar_weights]
        matrix = -np.eye(len(group))
        matrix[0, 0] = -1.5 - 4 / 3 * density[2] / density[1] * opacity
        matrix[0, 2] = density[2] / density[1] * opacity
        matrix[2, 0] = 4 / 3 * opacity
        matrix[2, 2] -= opacity
        maximum = len(self.photon) - 1
        for degree in range(maximum + 1):
            slot = degree + 1
            if degree:
                matrix[slot, slot - 1] += wave / hubble * (1 if degree == maximum else degree / (2 * degree + 1))
            if degree < maximum:
                matrix[slot, slot + 1] -= wave / hubble * (degree + 1) / (2 * degree + 1)
            if degree >= 2:
                matrix[slot, slot] -= opacity
        matrix[maximum + 1, maximum + 1] -= (maximum + 1) / (hubble * tau)
        polar_start = len(self.photon) + 1
        maximum = len(self.polar) + 1
        for degree in range(2, maximum + 1):
            slot = polar_start + degree - 2
            matrix[slot, slot] -= opacity
            if degree > 2:
                matrix[slot, slot - 1] = wave / hubble * (degree / (degree - 2) if degree == maximum else degree / (2 * degree + 1))
            if degree < maximum:
                matrix[slot, slot + 1] = -wave / hubble * (degree + 3) * (degree - 1) / ((degree + 1) * (2 * degree + 1))
        matrix[-1, -1] -= (maximum + 3) / (hubble * tau)
        matrix[3, 3] += opacity / 10
        matrix[3, polar_start] += .6 * opacity
        matrix[polar_start, 3] += .1 * opacity
        matrix[polar_start, polar_start] += .6 * opacity
        matrix *= weights[:, None] / weights[None, :]
        force = np.zeros_like(group)
        force[0] = weights[0] * wave / hubble * (psi + terms[1, 2] / density[1])
        force[2] = 4 * photon_weights[1] * wave / (3 * hubble) * (phi + psi)
        photon_error = np.linalg.norm(group_rate - matrix @ group - force) / max(np.linalg.norm(group_rate), np.linalg.norm(matrix @ group), np.linalg.norm(force), 1e-80)
        eigen_bound = float(np.linalg.eigvalsh((matrix + matrix.T) / 2)[-1])
        radiation = core[self.massless].copy()
        radiation_rate = core_rate[self.massless].copy()
        radiation[0] -= 4 * radiation_weights[0] * phi
        radiation_rate[0] -= 4 * radiation_weights[0] * (phi_n - phi)
        matrix_r = -np.eye(len(radiation))
        maximum = len(radiation) - 1
        for degree in range(maximum + 1):
            if degree:
                matrix_r[degree, degree - 1] = wave / hubble * (1 if degree == maximum else degree / (2 * degree + 1))
            if degree < maximum:
                matrix_r[degree, degree + 1] = -wave / hubble * (degree + 1) / (2 * degree + 1)
        matrix_r[-1, -1] -= (maximum + 1) / (hubble * tau)
        matrix_r *= radiation_weights[:, None] / radiation_weights[None, :]
        force_r = np.zeros_like(radiation)
        force_r[1] = 4 * radiation_weights[1] * wave / (3 * hubble) * ((3 if self.ufa else 1) * phi + psi)
        if self.ufa:
            radiation[2] += 4 * radiation_weights[2] * phi
            radiation_rate[2] += 4 * radiation_weights[2] * (phi_n - phi)
            hubble_n = float(system.background_spline(efold, 1)[0])
            force_r[2] = radiation_weights[2] * (12 * phi / (hubble * tau) - 4 * psi - 4 * (hubble_n - hubble) * info['alpha'])
        radiation_error = np.linalg.norm(radiation_rate - matrix_r @ radiation - force_r) / max(np.linalg.norm(radiation_rate), np.linalg.norm(matrix_r @ radiation), np.linalg.norm(force_r), 1e-80)
        eigen_r = float(np.linalg.eigvalsh((matrix_r + matrix_r.T) / 2)[-1])
        moments = np.vstack((core[self.massive], energy.tail_weights * (state[energy.size:] / system.units[energy.size:]).reshape(190, 5)))
        moment_rates = np.vstack((core_rate[self.massive], energy.tail_weights * (derivative[energy.size:] / system.units[energy.size:]).reshape(190, 5) - (1 + speeds**2)[None, :] / 2 * moments[3:]))
        weight0 = np.sqrt(massive / 4)
        moments[0] -= 4 * weight0 * phi
        moment_rates[0] -= 4 * weight0 * (phi_n - (1 + speeds**2) / 2 * phi)
        moment_rates = speeds * (moment_rates - (1 - speeds**2) * moments)
        moments *= speeds
        expected = -(3 - speeds**2) / 2 * moments
        for degree in range(193):
            if degree:
                expected[degree] += wave / hubble * speeds * degree / np.sqrt((2 * degree - 1) * (2 * degree + 1)) * moments[degree - 1]
            if degree < 192:
                expected[degree] -= wave / hubble * speeds * (degree + 1) / np.sqrt((2 * degree + 1) * (2 * degree + 3)) * moments[degree + 1]
        massive_force = 2 / np.sqrt(3) * np.sqrt(massive) * wave / hubble * (speeds**2 * phi + psi)
        expected[1] += massive_force
        massive_error = np.linalg.norm(moment_rates - expected) / max(np.linalg.norm(moment_rates), np.linalg.norm(expected), 1e-80)
        return dict(photon_equation=photon_error, massless_equation=radiation_error, massive_equation=massive_error,
                    photon_symmetric_excess=max(0., eigen_bound + 1), massless_symmetric_excess=max(0., eigen_r + 1),
                    norms=np.array([np.linalg.norm(group), np.linalg.norm(radiation), np.linalg.norm(moments)]),
                    source_norms=np.array([np.linalg.norm(force), np.linalg.norm(force_r), np.linalg.norm(massive_force)]),
                    scalar_shear=float(np.max(abs(terms[[5, 6], 6]))))
