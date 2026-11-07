from observer_common import *


class SpectralReadout:
    def __init__(self, system):
        self.system, self.basis = system, system.basis
        self.inputs = [system.geometry.source, THERMAL_PARENT / 'stable_spectral_basis.py']

    def background(self, expansion, planck=False):
        system, basis = self.system, self.basis
        local = system.background(expansion)
        profile = system.geometry.profiles(expansion).copy()
        derivative = system.geometry.profiles(expansion, 1).copy()
        profile += system.moment_lift @ [-basis.number @ profile, local['photon_energy_scaled'] - basis.energy @ profile]
        derivative += system.moment_lift @ [-basis.number @ derivative, local['photon_energy_prime'] - basis.energy @ derivative]
        heat = 0. if planck else local['heat']
        frequency = basis.nodes
        planck_occupation = 1 / np.expm1(frequency)
        values = basis.values @ profile
        slopes = basis.derivative(frequency) @ profile
        boost_change_values = frequency * ((1 + 2 * planck_occupation) * values - slopes)
        boost_change = basis.project(boost_change_values)
        dilation = basis.temperature + heat * boost_change
        age = heat * derivative - dilation
        edges = np.array([basis.minimum, basis.maximum])
        edge_basis = basis.evaluate(edges)
        edge_planck = 1 / np.expm1(edges)
        edge_flux = edges ** 3 * edge_planck * (1 + edge_planck) * (edge_basis @ profile) / I3
        boundary = edge_flux[-1] * edge_basis[-1] - edge_flux[0] * edge_basis[0]
        weak_change = system.mass_inverse @ system.redshift_weak @ profile
        return dict(dilation=dilation, dilation_change=boost_change, age=age, profile=profile,
                    profile_prime=derivative, heat=heat, boundary=boundary, weak_change=weak_change)

    def split(self, coefficients, dilation):
        temperature = np.dot(self.basis.number, coefficients) / np.dot(self.basis.number, dilation)
        return temperature, coefficients - dilation * temperature

    def apply(self, expansion, state, planck=False):
        background = self.background(expansion, planck)
        dilation, age = background['dilation'], background['age']
        density = self.system.density_row @ state
        velocity = state[9]
        temperatures, shapes, relational = [], [], []
        for degree, names in enumerate(self.system.names):
            for name in names:
                coefficients = state[self.system.mode_slice(degree, name)].copy()
                if name == 'I' and degree == 0:
                    coefficients += age * density / 3
                if name == 'I' and degree == 1:
                    coefficients -= dilation * velocity
                temperature, shape = self.split(coefficients, dilation)
                temperatures.append(temperature)
                shapes.append(shape)
                relational.append(coefficients)
        return dict(temperatures=np.asarray(temperatures), shapes=np.asarray(shapes),
                    relational=np.asarray(relational), density=density, velocity=velocity,
                    dilation=dilation, age=age)

    def transform(self, expansion, state, clock_shift=0., frame_boost=0., planck=False):
        background = self.background(expansion, planck)
        result = state.copy()
        result[self.system.mode_slice(0)] -= background['age'] * clock_shift
        result[8] += 3 * clock_shift
        result[self.system.mode_slice(1)] -= background['dilation'] * frame_boost
        result[9] -= frame_boost
        return result

    def reconstruct(self, reading):
        coefficients = reading['shapes'] + reading['temperatures'][:, None] * reading['dilation']
        coefficients[0] -= reading['age'] * reading['density'] / 3
        coefficients[2] += reading['dilation'] * reading['velocity']
        return coefficients


def spectral_norm(values, mass):
    return np.sqrt(np.maximum(0., np.einsum('...i,ij,...j->...', values.conj(), mass, values).real))
