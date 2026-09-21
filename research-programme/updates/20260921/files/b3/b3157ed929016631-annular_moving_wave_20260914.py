import numpy as np
from scipy.integrate import cumulative_simpson
from annular_reflecting_boundary_20260914 import boundary_derivative, boundary_weights
from annular_dynamical_source_20260914 import DustSurface, outgoing_profile, shell_geometry, shell_acceleration


class MovingWave:
    def __init__(self, count, coupling=0., amplitude=.01, inner_radius=3., reduced_central_mass=8.,
                 material=None, initial_radius=6.):
        if count < 17 or count % 2 != 1:
            raise ValueError('Odd grid count at least17 required.')
        self.count = count
        self.coordinate = np.linspace(0., 1., count)
        self.spacing = 1/(count-1)
        self.weights = boundary_weights(count, self.spacing)
        self.coupling = coupling
        self.inner_radius = inner_radius
        self.inner_mass = coupling*reduced_central_mass
        self.material = material or DustSurface()
        self.amplitude = amplitude
        radii = inner_radius+(initial_radius-inner_radius)*self.coordinate
        profile, profile_rate = outgoing_profile(-radii, amplitude)
        radial_field = -profile_rate-profile/radii
        time_field = profile_rate
        self.initial_state = np.concatenate([time_field-radial_field, time_field+radial_field,
                                             [initial_radius, 0., 0., 0., 0.]])
        self.calls = 0
        self.initial_interior_mass = self.geometry(self.initial_state)['mass'][-1]

    def unpack(self, state):
        return state[:self.count], state[self.count:2*self.count], state[-5:]

    def primitive(self, values, radii):
        return cumulative_simpson(values, x=radii, initial=0.)

    def geometry(self, state):
        outgoing, incoming, source = self.unpack(state)
        radius, proper_rate, exterior_time, dissipation, mass_work = source
        length = radius-self.inner_radius
        if np.real(length) <= 0:
            raise ValueError('Shell crossed the inner boundary.')
        radii = self.inner_radius+length*self.coordinate
        density = (outgoing**2+incoming**2)/4
        if self.coupling == 0:
            mass = np.zeros_like(density)
        else:
            exponent = self.primitive(2*self.coupling*density/radii, radii)
            integrating = np.exp(exponent)
            mass = (self.inner_mass+self.primitive(self.coupling*density*integrating, radii))/integrating
        geometry = 1-2*mass/radii
        reservoir, pressure = self.material.stress(radius)
        shell = shell_geometry(radius, proper_rate, mass[-1], reservoir, self.coupling)
        if np.min(np.real(geometry)) <= .15:
            raise ValueError('Outside the declared horizon-free numerical chart.')
        log_primitive = self.primitive(2*mass/(radii**2*geometry), radii)
        speed = np.exp(np.log(shell['beta_minus'])+log_primitive-log_primitive[-1])
        speed_radial = 2*mass*speed/(radii**2*geometry)
        reflection = (shell['beta_minus']-proper_rate)/(shell['beta_minus']+proper_rate)
        normal_pressure = (shell['beta_minus']-proper_rate)**2*outgoing[-1]**2/(2*radius**2)
        return dict(radii=radii, length=length, density=density, mass=mass, F=geometry, L=speed,
                    L_radial=speed_radial, shell=shell, reservoir=reservoir, pressure=pressure,
                    reflection=reflection, normal_pressure=normal_pressure)

    def rhs(self, proper_time, state, frozen_reflection=False):
        self.calls += 1
        outgoing, incoming, source = self.unpack(state)
        radius, proper_rate, exterior_time, dissipation, mass_work = source
        data = self.geometry(state)
        length, speed, speed_radial = data['length'], data['L'], data['L_radial']
        outgoing_speed = (speed-self.coordinate*proper_rate)/length
        incoming_speed = (speed+self.coordinate*proper_rate)/length
        outgoing_rate = -(outgoing_speed*boundary_derivative(outgoing, self.spacing)+
                          boundary_derivative(outgoing_speed*outgoing, self.spacing))/2
        outgoing_rate -= (speed_radial+proper_rate/length)*outgoing/2
        outgoing_rate += speed*incoming/data['radii']
        incoming_rate = (incoming_speed*boundary_derivative(incoming, self.spacing)+
                         boundary_derivative(incoming_speed*incoming, self.spacing))/2
        incoming_rate += (speed_radial-proper_rate/length)*incoming/2
        incoming_rate -= speed*outgoing/data['radii']
        reflection = 1. if frozen_reflection else data['reflection']
        left_mismatch = outgoing[0]-incoming[0]
        right_mismatch = incoming[-1]+reflection*outgoing[-1]
        outgoing_rate[0] -= outgoing_speed[0]*left_mismatch/self.weights[0]
        incoming_rate[-1] -= incoming_speed[-1]*right_mismatch/self.weights[-1]
        acceleration = shell_acceleration(radius, proper_rate, data['mass'][-1], data['reservoir'],
                                          data['pressure'], data['normal_pressure'], self.coupling)
        outer_clock = data['shell']['beta_plus']/data['shell']['F_plus']
        dissipation_rate = speed[0]*left_mismatch**2/4+(speed[-1]+proper_rate)*right_mismatch**2/4
        mass_work_rate = -self.coupling*radius**2*data['normal_pressure']*proper_rate
        return np.concatenate([outgoing_rate, incoming_rate,
                               [proper_rate, acceleration, outer_clock, dissipation_rate, mass_work_rate]])

    def diagnostics(self, proper_time, state):
        outgoing, incoming, source = self.unpack(state)
        data = self.geometry(state)
        radius, proper_rate, exterior_time, dissipation, mass_work = source
        field_energy = data['length']*self.weights @ data['density']
        shell_energy_flat = data['reservoir']*np.sqrt(1+proper_rate**2)
        radial_field = (incoming-outgoing)/2
        time_field = (incoming+outgoing)/2
        primitive = self.primitive(radial_field/data['radii'], data['radii'])
        scalar = primitive-primitive[-1]
        return dict(radius=radius, proper_rate=proper_rate, exterior_time=exterior_time,
                    field_energy=field_energy, flat_energy_with_SAT=field_energy+shell_energy_flat+dissipation,
                    accumulated_SAT_loss=dissipation, mass_plus=data['shell']['mass_plus'],
                    mass_work_error=data['mass'][-1]-self.initial_interior_mass-mass_work,
                    left_boundary_mismatch=outgoing[0]-incoming[0],
                    right_boundary_mismatch=incoming[-1]+data['reflection']*outgoing[-1],
                    normal_pressure=data['normal_pressure'], minimum_F=data['F'].min(),
                    scalar=scalar, gradient=radial_field/data['radii'], momentum=data['radii']*time_field,
                    mass=data['mass'], L=data['L'], radii=data['radii'])

