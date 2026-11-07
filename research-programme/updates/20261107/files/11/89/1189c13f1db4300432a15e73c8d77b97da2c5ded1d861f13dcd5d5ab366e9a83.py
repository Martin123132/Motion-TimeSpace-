from wave_common import *
from emission_rates import ALPHA
from sourced_emission import GauntTable
from gaunt_gradient import gaunt_with_log_derivatives


def ambient_moments(frequency, basis, profile, order=96):
    nodes, weights = special.roots_laguerre(order)
    incident = 2 * frequency + nodes
    companion = incident - frequency
    fraction = frequency / incident
    product = fraction * (1 - fraction)
    polynomial = 1 - 3 * product + 1.5 * product ** 2 - product ** 3
    gould = polynomial / (1 - fraction)
    incident_planck = 1 / np.expm1(incident)
    companion_planck = 1 / np.expm1(companion)
    measure = weights * incident ** 4 * gould / ((-np.expm1(-incident)) * (-np.expm1(-companion)))
    normalization = np.sum(measure)
    incident_profile = basis.evaluate(np.clip(incident, basis.minimum, basis.maximum)) @ profile
    companion_profile = basis.evaluate(np.clip(companion, basis.minimum, basis.maximum)) @ profile
    incident_profile = np.where((incident >= basis.minimum) & (incident <= basis.maximum), incident_profile, 0.)
    companion_profile = np.where((companion >= basis.minimum) & (companion <= basis.maximum), companion_profile, 0.)
    background = np.sum(measure * ((1 + incident_planck) * incident_profile + companion_planck * companion_profile)) / normalization
    thermal = np.sum(measure * ((1 + incident_planck) * incident + companion_planck * companion)) / normalization
    gould_derivative = ((-3 + 3 * product - 3 * product ** 2) / polynomial * (1 - 2 * fraction) + 1 / (1 - fraction))
    slope = np.sum(measure * (8 * frequency / incident + gould_derivative * fraction * (1 - 2 * fraction)
                             - 2 * frequency * incident_planck - frequency * companion_planck)) / normalization
    return dict(normalization=normalization, background=background, thermal=thermal, log_slope=slope,
                incident=incident, companion=companion, measure=measure / normalization,
                incident_profile=incident_profile, companion_profile=companion_profile)


class EmissionResponse:
    def __init__(self, geometry):
        self.geometry = geometry
        self.tables = [GauntTable(PARENT / 'sources' / ('gauntff_merged_Z0' + str(charge) + '.dat'), charge) for charge in [1, 2]]
        self.inputs = [geometry.source, *[table.path for table in self.tables]]

    def at(self, expansion, frequency):
        geometry, basis = self.geometry, self.geometry.basis
        profile = geometry.profiles(expansion)
        gas = float(geometry.temperature(expansion))
        theta = geometry.at(expansion)['theta']
        planck = 1 / np.expm1(frequency)
        value = float(basis.evaluate(frequency) @ profile)
        slope = float(frequency * (basis.derivative(frequency) @ profile))
        departure = value - frequency * gas
        departure_slope = slope - frequency * gas
        ambient = ambient_moments(frequency, basis, profile)
        dc = 4 * ALPHA / (3 * math.pi) * theta ** 2 / (1 + 14.16 * theta)
        dc *= np.exp(-frequency) * (-np.expm1(-frequency)) / frequency ** 3 * ambient['normalization']
        dc_slope = -frequency + frequency * planck + ambient['log_slope'] - 3
        common_g = -14.16 * theta / (1 + 14.16 * theta)
        dc_thermal_frozen = dc * (frequency * (1 + planck) * value + gas * (frequency ** 2 * planck - 2 * frequency)
                                  - ambient['thermal'] * departure)
        dc_thermal = dc_thermal_frozen - dc * common_g * departure
        constants = geometry.thermal.constants
        helium = geometry.thermal.helium_fraction / (1 - geometry.thermal.helium_fraction) * constants['m_H'] / constants['m_He4']
        scale = geometry.thermal.theta0 / theta
        hydrogen = geometry.thermal.electron0 / scale ** 3 / (1 + 2 * helium)
        components = []
        for charge, density, table in zip([1, 2], [hydrogen, helium * hydrogen], self.tables):
            gaunt, gamma_derivative, frequency_derivative = gaunt_with_log_derivatives(table, charge ** 2 * ALPHA ** 2 / (2 * theta), frequency)
            components.append(np.array([gaunt, -.5 * gaunt - gamma_derivative - frequency_derivative, frequency_derivative]) * charge ** 2 * density)
        coefficient, thermal_derivative, frequency_derivative = np.sum(components, axis=0)
        compton = 6.62607015e-34 / (constants['m_e'] * constants['c'])
        br = ALPHA * compton ** 3 / (2 * math.pi * math.sqrt(6 * math.pi)) * theta ** (-3.5)
        br *= coefficient * (-np.expm1(-frequency)) / frequency ** 3
        br_thermal_log = thermal_derivative / coefficient
        br_slope = frequency_derivative / coefficient + frequency * planck - 3
        br_thermal = br * (frequency * planck * value + gas * (frequency ** 2 * (1 + planck) - 2 * frequency)
                          - br_thermal_log * departure)
        dc_source, br_source = -dc * departure, -br * departure
        source = dc_source + br_source
        source_slope = -dc * (dc_slope * departure + departure_slope) - br * (br_slope * departure + departure_slope)
        boost = (frequency * (1 + 2 * planck) - 1) * source - source_slope
        return dict(dc=dc, br=br, source=source, density_source=dc_source + 2 * br_source,
            dc_source=dc_source, br_source=br_source, dc_thermal=dc_thermal,
            dc_thermal_frozen=dc_thermal_frozen, br_thermal=br_thermal,
            br_thermal_log=br_thermal_log, common_g=common_g, boost=boost,
            theta=theta, gas=gas, value=value, ambient=ambient,
            dc_absorption_change_fixed_g=dc * (ambient['background'] - frequency * (1 + planck) * gas),
            br_absorption_change=br * (br_thermal_log - frequency * planck) * gas)
