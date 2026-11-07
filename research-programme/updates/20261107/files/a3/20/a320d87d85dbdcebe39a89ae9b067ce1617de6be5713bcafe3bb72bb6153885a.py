from __future__ import annotations

import sympy as sp


class Jet:
    def __init__(self, constant=0, pn=0, tide=0, mixed=0):
        self.values = tuple(sp.sympify(value) for value in (constant, pn, tide, mixed))

    @staticmethod
    def cast(value):
        return value if isinstance(value, Jet) else Jet(value)

    def __add__(self, other):
        other = self.cast(other)
        return Jet(*(first+second for first, second in zip(self.values, other.values)))

    __radd__ = __add__

    def __neg__(self):
        return Jet(*(-value for value in self.values))

    def __sub__(self, other):
        return self+-self.cast(other)

    def __rsub__(self, other):
        return self.cast(other)+-self

    def __mul__(self, other):
        other = self.cast(other)
        constant, pn, tide, mixed = self.values
        other_constant, other_pn, other_tide, other_mixed = other.values
        return Jet(constant*other_constant, constant*other_pn+pn*other_constant,
                   constant*other_tide+tide*other_constant,
                   constant*other_mixed+mixed*other_constant+pn*other_tide+tide*other_pn)

    __rmul__ = __mul__

    def __pow__(self, power):
        constant, pn, tide, mixed = self.values
        return Jet(constant**power, power*constant**(power-1)*pn,
                   power*constant**(power-1)*tide,
                   power*constant**(power-1)*mixed+power*(power-1)*constant**(power-2)*pn*tide)

    def __truediv__(self, other):
        return self*self.cast(other)**-1

    def __rtruediv__(self, other):
        return self.cast(other)*self**-1

    def simplified(self):
        return Jet(*(sp.factor(value) for value in self.values))

    def substitute(self, replacements):
        return Jet(*(value.subs(replacements) for value in self.values)).simplified()

    def expression(self, pn_symbol, tide_symbol):
        return self.values[0]+self.values[1]*pn_symbol+self.values[2]*tide_symbol+self.values[3]*pn_symbol*tide_symbol


def gr_matching(central_fraction):
    companion_fraction = 1-central_fraction
    eta = central_fraction*companion_fraction
    return {
        'eta': eta, 'A': 3*companion_fraction/(2*central_fraction),
        'theta0': (1-3*eta)/8, 'theta1': (3+eta)/2, 'theta3': -sp.Rational(1, 2),
        'xi1': companion_fraction*(5+central_fraction)/2, 'xi3': -7+5*central_fraction,
        'tau1': sp.Rational(29, 42)*(1-3*eta), 'tau3': (8*eta-5)/7,
        'tau4': sp.Rational(11, 21)*(1-3*eta),
        'sigma1': 13*companion_fraction**2/(7*central_fraction),
        'sigma3': -3*companion_fraction*(8+23*central_fraction+13*central_fraction**2)/(14*central_fraction),
        'sigma4': 38*companion_fraction**2/(7*central_fraction)}


def circular_radius(central_fraction):
    coefficients = gr_matching(central_fraction)
    pn = Jet(0, 1)
    tide = Jet(0, 0, 1)
    radius_pn, radius_tide, radius_mixed = sp.symbols('radius_pn radius_tide radius_mixed')
    radius = Jet(1, radius_pn, radius_tide, radius_mixed)
    force = (radius-radius**-2-6*coefficients['A']*tide*radius**-7
             +pn*(4*coefficients['theta0']*radius**3+coefficients['theta1']-2*coefficients['theta3']*radius**-3
                    +coefficients['A']*tide*(-4*coefficients['xi1']*radius**-5-7*coefficients['xi3']*radius**-8)))
    solved = {}
    for index, symbol in [(1, radius_pn), (2, radius_tide), (3, radius_mixed)]:
        solved[symbol] = sp.factor(sp.solve(force.values[index].subs(solved), symbol)[0])
    return radius.substitute(solved), force.substitute(solved)


def derive_circular_model(central_fraction):
    coefficients = gr_matching(central_fraction)
    pn = Jet(0, 1)
    tide = Jet(0, 0, 1)
    radius, radial_residual = circular_radius(central_fraction)
    frequency_factor = sp.symbols('frequency_factor')
    action = (radius**2*frequency_factor**2/2+radius**-1+coefficients['A']*tide*radius**-6
              +pn*(coefficients['theta0']*radius**4*frequency_factor**4
                     +coefficients['theta1']*radius*frequency_factor**2+coefficients['theta3']*radius**-2
                     +coefficients['A']*tide*(coefficients['xi1']*frequency_factor**2*radius**-4+coefficients['xi3']*radius**-7)))
    energy = Jet(*(sp.diff(value, frequency_factor).subs(frequency_factor, 1)-value.subs(frequency_factor, 1) for value in action.values)).simplified()
    normal_moment = (radius**2+3*tide/(central_fraction*radius**3)
                     +pn*(coefficients['tau1']*radius**4+coefficients['tau3']*radius
                            +tide*(coefficients['sigma1']*radius**-1+coefficients['sigma3']*radius**-4)
                            +3*tide/(central_fraction*radius**3)*(2*radius**2-(6-central_fraction)/(2*radius))))
    tangent_moment = pn*(coefficients['tau4']*radius**4+coefficients['sigma4']*tide*radius**-1+3*tide/(central_fraction*radius))
    normal_moment, tangent_moment = normal_moment.simplified(), tangent_moment.simplified()
    octupole = ((1-2*central_fraction)*radius**3+9*(1-central_fraction)/central_fraction*tide*radius**-2).simplified()
    current = ((1-2*central_fraction)*radius**3+sp.Rational(9, 2)*(1-central_fraction)/central_fraction*tide*radius**-2).simplified()
    electric_flux = ((normal_moment-tangent_moment)**2).simplified()
    octupole_flux = (sp.Rational(1367, 1008)*pn*octupole**2).simplified()
    current_flux = (pn*current**2/36).simplified()
    flux = (electric_flux+octupole_flux+current_flux).simplified()
    energy_slope = Jet(*(-2*weight*value for weight, value in zip([1, 2, 6, 7], energy.values))).simplified()
    chirp = (flux/energy_slope).simplified()
    inverse_chirp = (1/chirp).simplified()
    phase_tide = -4*chirp.values[2]
    phase_mixed = sp.Rational(10, 7)*inverse_chirp.values[3]
    return {'radius': radius, 'radial_residual': radial_residual, 'energy': energy, 'normal_moment': normal_moment,
            'tangent_moment': tangent_moment, 'octupole': octupole, 'current': current,
            'electric_flux': electric_flux, 'octupole_flux': octupole_flux, 'current_flux': current_flux,
            'flux': flux, 'energy_slope': energy_slope, 'chirp': chirp, 'inverse_chirp': inverse_chirp,
            'fourier_phase_tide': sp.factor(phase_tide), 'fourier_phase_mixed': sp.factor(phase_mixed)}
