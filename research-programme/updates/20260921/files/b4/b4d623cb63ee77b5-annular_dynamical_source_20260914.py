from dataclasses import dataclass
import numpy as np


def shell_geometry(radius, proper_rate, interior_mass, reservoir, coupling=.1):
    interior_F = 1-2*interior_mass/radius
    beta_minus = np.sqrt(interior_F+proper_rate**2)
    beta_plus = beta_minus-coupling*reservoir/radius
    exterior_mass = interior_mass+coupling*reservoir*beta_minus-(coupling*reservoir)**2/(2*radius)
    exterior_F = 1-2*exterior_mass/radius
    if np.real(radius) <= 0 or np.real(reservoir) <= 0 or min(np.real(interior_F), np.real(exterior_F), np.real(beta_plus)) <= 0:
        raise ValueError('Outside this regular positive-mass, outward-normal shell chart.')
    return dict(F_minus=interior_F, F_plus=exterior_F, beta_minus=beta_minus,
                beta_plus=beta_plus, mass_plus=exterior_mass)


def shell_acceleration(radius, proper_rate, interior_mass, reservoir, surface_pressure, normal_pressure, coupling=.1):
    geometry = shell_geometry(radius, proper_rate, interior_mass, reservoir, coupling)
    beta_minus, beta_plus = geometry['beta_minus'], geometry['beta_plus']
    return (radius**2*normal_pressure*beta_plus/reservoir+
            2*radius*surface_pressure*beta_minus*beta_plus/reservoir-
            interior_mass/radius**2-coupling*reservoir*beta_minus/(2*radius**2))


def reflecting_trace(radius, proper_rate, interior_mass, field_gradient, interior_lapse):
    geometry = 1-2*interior_mass/radius
    beta = np.sqrt(geometry+proper_rate**2)
    speed = interior_lapse*np.sqrt(geometry)
    coordinate_rate = speed*proper_rate/beta
    momentum = -radius**2*proper_rate*field_gradient/beta
    normal_gradient = geometry*field_gradient/beta
    return dict(momentum=momentum, coordinate_rate=coordinate_rate,
                normal_gradient=normal_gradient, normal_pressure=normal_gradient**2/2,
                interior_clock_rate=beta/speed)


@dataclass(frozen=True)
class DustSurface:
    reservoir: float = .003

    def stress(self, radius):
        return self.reservoir, 0.*radius


@dataclass(frozen=True)
class CausalSurface:
    reference_radius: float
    reference_reservoir: float
    reference_pressure: float
    sound_speed_squared: float

    def __post_init__(self):
        density = self.reference_reservoir/self.reference_radius**2
        if not 0 <= self.sound_speed_squared <= 1 or density <= 0:
            raise ValueError('Positive density and causal surface sound speed required.')
        if self.sound_speed_squared*density < self.reference_pressure or density+self.reference_pressure <= 0:
            raise ValueError('This example requires nonnegative vacuum and positive particle contributions.')

    def stress(self, radius):
        density = self.reference_reservoir/self.reference_radius**2
        sound = self.sound_speed_squared
        vacuum = (sound*density-self.reference_pressure)/(1+sound)
        particles = (density+self.reference_pressure)/(1+sound)*(self.reference_radius/radius)**(2*(1+sound))
        return radius**2*(vacuum+particles), sound*particles-vacuum


def quiet_pressure(radius, interior_mass, reservoir, coupling=.1):
    geometry = shell_geometry(radius, 0., interior_mass, reservoir, coupling)
    return reservoir/(4*radius**2)*(1/(geometry['beta_minus']*geometry['beta_plus'])-1)


def vacuum_rhs(material, coupling=.1):
    def rhs(proper_time, state):
        radius, proper_rate, interior_mass = state
        reservoir, pressure = material.stress(radius)
        acceleration = shell_acceleration(radius, proper_rate, interior_mass, reservoir, pressure, 0., coupling)
        return np.array([proper_rate, acceleration, 0.])
    return rhs


def outgoing_profile(retarded_time, amplitude=.01, center=-5.5, width=.3):
    coordinate = (np.asarray(retarded_time)-center)/width
    selected = abs(coordinate) < 1
    value = np.zeros_like(coordinate, dtype=float)
    rate = np.zeros_like(coordinate, dtype=float)
    denominator = 1-coordinate[selected]**2
    value[selected] = amplitude*np.exp(1-1/denominator)
    rate[selected] = -2*coordinate[selected]*value[selected]/(width*denominator**2)
    return value, rate


def flat_mirror_rhs(reservoir, amplitude):
    def rhs(time, state):
        radius, rapidity, incident_energy, reflected_energy = state
        proper_rate = np.sinh(rapidity)
        gamma = np.cosh(rapidity)
        coordinate_rate = np.tanh(rapidity)
        profile, profile_rate = outgoing_profile(time-radius, amplitude)
        normal_gradient = -2*profile_rate/(radius*np.exp(rapidity))
        pressure = normal_gradient**2/2
        acceleration = shell_acceleration(radius, proper_rate, 0., reservoir, 0., pressure, coupling=0.)
        incident_rate = profile_rate**2*(1-coordinate_rate)
        reflected_rate = incident_rate*np.exp(-2*rapidity)
        return np.array([coordinate_rate, acceleration/gamma**2, incident_rate, reflected_rate])
    return rhs
