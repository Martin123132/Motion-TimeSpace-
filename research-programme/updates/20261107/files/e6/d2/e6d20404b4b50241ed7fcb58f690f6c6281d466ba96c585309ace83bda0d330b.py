from __future__ import annotations

import json

import sympy as sp

from common import ROOT, configure_worker, contraction, digest, stf, write_new_json, zero_check


def derive():
    checks = []
    coordinates = sp.Matrix(sp.symbols('coord_x coord_y coord_z'))
    position = sp.Matrix(sp.symbols('pos_x pos_y pos_z'))
    velocity = sp.Matrix(sp.symbols('vel_x vel_y vel_z'))
    current_components = sp.symbols('S_xx S_yy S_xy S_xz S_yz')
    current_rates = sp.symbols('Sd_xx Sd_yy Sd_xy Sd_xz Sd_yz')

    def current_matrix(components):
        diagonal_x, diagonal_y, cross_xy, cross_xz, cross_yz = components
        return sp.Matrix([[diagonal_x, cross_xy, cross_xz],
                          [cross_xy, diagonal_y, cross_yz],
                          [cross_xz, cross_yz, -diagonal_x-diagonal_y]])

    current = current_matrix(current_components)
    current_dot = current_matrix(current_rates)
    epsilon = sp.LeviCivita
    identity = sp.eye(3)
    radius_squared = coordinates.dot(coordinates)
    evaluation = dict(zip(coordinates, position))
    density_coefficients = sp.Matrix(3, 3, lambda first, second: sp.Rational(4, 3)*sum(
        current[inner, first]*velocity[direction]*epsilon(second, direction, inner)
        for inner in range(3) for direction in range(3)))
    current_coefficients = [sp.Matrix(3, 3, lambda first, second: sp.Rational(1, 3)*sum(
        epsilon(component, inner, first)*current[inner, second] for inner in range(3)))
        for component in range(3)]

    def distribution_integral(polynomial, coefficients):
        return sp.expand(sum(coefficients[first, second]*sp.diff(
            polynomial, coordinates[first], coordinates[second])
            for first in range(3) for second in range(3))).subs(evaluation)

    def time_derivative(expression):
        return sum(sp.diff(expression, position[direction])*velocity[direction]
                   for direction in range(3))+sum(
                       sp.diff(expression, component)*rate
                       for component, rate in zip(current_components, current_rates))

    def third_stf(first, second, third):
        return (coordinates[first]*coordinates[second]*coordinates[third]
                -radius_squared*(identity[first, second]*coordinates[third]
                                 +identity[first, third]*coordinates[second]
                                 +identity[second, third]*coordinates[first])/5)

    quadratic = stf(coordinates*coordinates.T)
    density_moment = quadratic.applyfunc(lambda value: distribution_integral(value, density_coefficients))
    transport_moment = sp.Matrix(3, 3, lambda first, second: sum(
        distribution_integral(third_stf(first, second, component), current_coefficients[component])
        for component in range(3)))
    mass_correction = (density_moment-sp.Rational(20, 21)*transport_moment.applyfunc(time_derivative)).applyfunc(sp.factor)
    axial_moment = stf(sp.Matrix(3, 3, lambda first, second: sum(
        epsilon(inner, component, second)*distribution_integral(
            coordinates[first]*coordinates[inner], current_coefficients[component])
        for inner in range(3) for component in range(3))))
    benchmark = stf(sp.Matrix(3, 3, lambda first, second: sp.Rational(8, 9)*sum(
        epsilon(direction, inner, first)*(2*current[second, inner]*velocity[direction]
                                         -current_dot[second, inner]*position[direction])
        for direction in range(3) for inner in range(3))))
    for first in range(3):
        for second in range(3):
            zero_check(checks, f'generic_mass_source_{first}{second}', mass_correction[first, second]-benchmark[first, second])
            zero_check(checks, f'generic_current_source_{first}{second}', axial_moment[first, second]-current[first, second])
    zero_check(checks, 'generic_mass_trace', sp.trace(mass_correction))
    zero_check(checks, 'generic_current_trace', sp.trace(axial_moment))
    for direction in range(3):
        zero_check(checks, f'no_intrinsic_mass_dipole_{direction}', distribution_integral(coordinates[direction], density_coefficients))

    chi, total_mass, radius, omega, sigma_bar, angle = sp.symbols('chi MT radius Omega sigma_bar angle', real=True)
    companion = 1-chi
    reduced_mass = chi*companion*total_mass
    normal = sp.Matrix([sp.cos(angle), sp.sin(angle), 0])
    tangent = sp.diff(normal, angle)
    vertical = normal.cross(tangent)
    normal_stf = stf(normal*normal.T)
    tangent_stf = stf(tangent*tangent.T)
    axial_basis = stf(normal*vertical.T)
    tidal_raw = sp.Matrix(3, 3, lambda first, second: 6*companion*total_mass/radius**3*sum(
        radius*omega*tangent[direction]*epsilon(inner, direction, first)*normal[second]*normal[inner]
        for direction in range(3) for inner in range(3)))
    magnetic_tensor = stf(tidal_raw)
    induced_current = (sigma_bar*magnetic_tensor).applyfunc(sp.trigsimp)
    induced_rate = omega*sp.diff(induced_current, angle)
    replacements = dict(zip(position, companion*radius*normal))
    replacements.update(zip(velocity, companion*radius*omega*tangent))
    for symbol, entry in zip(current_components, [(0, 0), (1, 1), (0, 1), (0, 2), (1, 2)]):
        replacements[symbol] = induced_current[entry]
    for symbol, entry in zip(current_rates, [(0, 0), (1, 1), (0, 1), (0, 2), (1, 2)]):
        replacements[symbol] = induced_rate[entry]
    circular_mass = mass_correction.subs(replacements, simultaneous=True).applyfunc(sp.trigsimp)
    expected_mass = 8*total_mass*companion**2*omega**2*sigma_bar/(3*radius)*(5*normal_stf+4*tangent_stf)
    expected_current = 6*companion*total_mass*omega*sigma_bar/radius**2*axial_basis
    for first in range(3):
        for second in range(3):
            zero_check(checks, f'circular_mass_{first}{second}', circular_mass[first, second]-expected_mass[first, second])
            zero_check(checks, f'circular_current_{first}{second}', induced_current[first, second]-expected_current[first, second])
    zero_check(checks, 'tidal_invariant', contraction(magnetic_tensor, magnetic_tensor)-18*(companion*total_mass)**2*omega**2/radius**4)
    mass_derivative = omega**3*sp.diff(reduced_mass*radius**2*normal_stf, angle, 3)
    mass_correction_derivative = omega**3*sp.diff(circular_mass, angle, 3)
    point_current = (1-2*chi)*reduced_mass*radius**3*omega*axial_basis
    current_derivative = omega**3*sp.diff(point_current, angle, 3)
    induced_derivative = omega**3*sp.diff(induced_current, angle, 3)
    newton_flux = 32*reduced_mass**2*radius**4*omega**6/5
    intrinsic_mass_ratio = sp.factor(sp.trigsimp(2*contraction(mass_derivative, mass_correction_derivative)/(5*newton_flux)))
    intrinsic_current_ratio = sp.factor(sp.trigsimp(sp.Rational(32, 45)*contraction(current_derivative, induced_derivative)/newton_flux))
    zero_check(checks, 'mass_quadrupole_radiation_normalization', contraction(mass_derivative, mass_derivative)/5-newton_flux)
    zero_check(checks, 'intrinsic_mass_flux_ratio', intrinsic_mass_ratio-sp.Rational(16, 3)*companion*sigma_bar*omega**2/(chi*radius**3))
    zero_check(checks, 'intrinsic_current_flux_ratio', intrinsic_current_ratio-(1-2*chi)*sigma_bar*omega**2/(3*chi*radius**3))
    zero_check(checks, 'mass_basis_norm', contraction(sp.diff(normal_stf, angle, 3), sp.diff(normal_stf, angle, 3))-32)
    zero_check(checks, 'current_basis_norm', contraction(sp.diff(axial_basis, angle, 3), sp.diff(axial_basis, angle, 3))-sp.Rational(1, 2))

    pn, magnetic, radial_shift, frequency_factor, book = sp.symbols('x magnetic radial_shift frequency_factor book')
    trial_radius, trial_frequency = sp.symbols('trial_radius trial_frequency')
    action = trial_radius**2*trial_frequency**2/2+1/trial_radius+6*companion/chi*pn*magnetic*trial_frequency**2/trial_radius**4
    force = sp.diff(action, trial_radius)
    replacements_orbit = {trial_radius: 1+book*radial_shift, trial_frequency: 1, magnetic: book*magnetic}
    force_linear = sp.diff(force.subs(replacements_orbit, simultaneous=True), book).subs(book, 0)
    shift = sp.factor(sp.solve(force_linear, radial_shift)[0])
    circular_energy = trial_frequency*sp.diff(action, trial_frequency)-action
    energy_linear = sp.diff(circular_energy.subs(replacements_orbit, simultaneous=True), book).subs(book, 0).subs(radial_shift, shift)
    energy_coefficient = sp.factor(energy_linear/(pn*magnetic))
    radius_coefficient = sp.factor(shift/(pn*magnetic))
    intrinsic_mass_coefficient = sp.factor(intrinsic_mass_ratio.subs(omega**2, total_mass/radius**3)/(total_mass*sigma_bar/radius**6))
    intrinsic_current_coefficient = sp.factor(intrinsic_current_ratio.subs(omega**2, total_mass/radius**3)/(total_mass*sigma_bar/radius**6))
    orbital_flux_coefficient = 4*radius_coefficient
    flux_coefficient = sp.factor(orbital_flux_coefficient+intrinsic_mass_coefficient+intrinsic_current_coefficient)
    slope_coefficient = -14*energy_coefficient
    chirp_coefficient = sp.factor(flux_coefficient-slope_coefficient)
    fourier_coefficient = -sp.Rational(10, 7)*chirp_coefficient
    zero_check(checks, 'circular_force', force_linear.subs(radial_shift, shift))
    zero_check(checks, 'published_energy_barred_convention', energy_coefficient-22*companion/chi)
    zero_check(checks, 'published_flux_barred_convention', flux_coefficient-(114*companion-1)/(3*chi))
    zero_check(checks, 'published_phase_barred_convention', fourier_coefficient+10*(1038*companion-1)/(21*chi))
    coefficients = {'radius': radius_coefficient, 'energy': energy_coefficient,
                    'energy_slope': slope_coefficient, 'orbital_mass_flux': orbital_flux_coefficient,
                    'intrinsic_mass_flux': intrinsic_mass_coefficient,
                    'intrinsic_current_flux': intrinsic_current_coefficient,
                    'flux': flux_coefficient, 'chirp': chirp_coefficient,
                    'inverse_chirp': -chirp_coefficient, 'fourier_phase': sp.factor(fourier_coefficient)}
    return checks, coefficients, {
        'generic_mass_correction': [[str(value) for value in mass_correction.row(row)] for row in range(3)],
        'generic_current_correction': [[str(value) for value in axial_moment.row(row)] for row in range(3)],
        'intrinsic_mass_flux_before_Kepler': str(intrinsic_mass_ratio),
        'intrinsic_current_flux_before_Kepler': str(intrinsic_current_ratio),
        'action_over_reduced_mass_x': str(action), 'coefficient_basis': 'x * (geometric_sigma_bar / d0^5)'}


def main():
    configure_worker()
    checks, coefficients, details = derive()
    output = {'state': 'complete', 'script_sha256': digest(__file__), 'common_sha256': digest(ROOT/'common.py'),
              'source_provenance_sha256': digest(ROOT/'sources/provenance.json'), 'checks': checks,
              'coefficients': {name: str(value) for name, value in coefficients.items()}, **details,
              'source_formula_input': 'BV2020 Eqs22,23,45,48; final Eqs41,46,51,52,54 used only as checks.',
              'convention': 'G=c=1; Sij=sigma_bar Bij=2sigma_BV Bij; deformable body fraction chi=X1.'}
    write_new_json(ROOT/'results/derivation/status.json', output)
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks), 'coefficients': output['coefficients']}))


if __name__ == '__main__':
    main()
