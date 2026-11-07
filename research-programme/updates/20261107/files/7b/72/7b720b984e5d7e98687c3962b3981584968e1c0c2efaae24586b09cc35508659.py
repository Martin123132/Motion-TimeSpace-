from __future__ import annotations

from datetime import datetime, timezone
import json

import mpmath as mp
import psutil
import sympy as sy

from acquire_source import ROOT, digest


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    checks = []

    def check(name, expression):
        residual = sy.simplify(sy.expand(expression))
        checks.append({'name': name, 'passed': residual == 0, 'residual': str(residual)})
        assert residual == 0, (name, residual)

    mass, omega, scale, laplace, exponent, x, particle, ratio = sy.symbols('M omega b s a x mu q', positive=True)
    constant = sy.symbols('kappa', real=True)
    transform = sy.diff(sy.gamma(exponent+1)*laplace**(-exponent-1), exponent).subs(exponent, 0)
    check('log_Laplace_derivative', transform-(-sy.EulerGamma-sy.log(laplace))/laplace)
    logarithm = sy.log(omega)-sy.I*sy.pi/2
    kernel = (-sy.EulerGamma-logarithm-sy.log(2*scale)+constant)/(-sy.I*omega)
    amplitude = sy.expand_complex(-2*mass*omega**2*kernel)
    check('tail_amplitude_real', sy.re(amplitude)-sy.pi*mass*omega)
    check('tail_amplitude_imaginary', sy.im(amplitude)-2*mass*omega*(sy.EulerGamma+sy.log(2*scale*omega)-constant))
    check('current_quadrupole_constant', amplitude.subs(constant, sy.Rational(7, 6))
          -(sy.pi*mass*omega+2*sy.I*mass*omega*(sy.EulerGamma+sy.log(2*scale*omega)-sy.Rational(7, 6))))
    check('log_scale_has_no_linear_power_effect', sy.diff(2*sy.re(amplitude), scale))
    check('kernel_constant_has_no_linear_power_effect', sy.diff(2*sy.re(amplitude), constant))
    flux_tail = 2*sy.re(amplitude)
    check('m1_current_tail_2pi', flux_tail.subs(omega, x**sy.Rational(3, 2)/mass)-2*sy.pi*x**sy.Rational(3, 2))
    check('m2_mass_tail_4pi', flux_tail.subs(omega, 2*x**sy.Rational(3, 2)/mass)-4*sy.pi*x**sy.Rational(3, 2))
    base_real, base_imag, delta_real, delta_imag, factor_real, factor_imag = sy.symbols('ar ai dr di tr ti', real=True)
    baseline = base_real+sy.I*base_imag
    delta = delta_real+sy.I*delta_imag
    factor = factor_real+sy.I*factor_imag
    norm = lambda value: sy.expand(value*sy.conjugate(value))
    check('shared_tail_multiplies_body_minus_reference_power', norm(factor*(baseline+delta))-norm(factor*baseline)
          -norm(factor)*(norm(baseline+delta)-norm(baseline)))
    check('shared_tail_cancels_in_amplitude_ratio', (factor*(baseline+delta))/(factor*baseline)-(baseline+delta)/baseline)
    check('shared_tail_zero_response_control', (norm(factor*(baseline+delta))-norm(factor*baseline)).subs({delta_real: 0, delta_imag: 0}))

    energy = (1-2*x)/sy.sqrt(1-3*x)-1
    slope = (1-6*x)/(1-3*x)**sy.Rational(3, 2)
    angular_momentum = particle*mass/sy.sqrt(x*(1-3*x))
    orbital_frequency = x**sy.Rational(3, 2)/mass
    check('geodesic_energy_derivative', -2*sy.diff(energy, x)-slope)
    check('circular_energy_angular_momentum_identity', particle*sy.diff(energy, x)-orbital_frequency*sy.diff(angular_momentum, x))
    check('energy_Newtonian_limit', sy.limit(energy/x, x, 0)+sy.Rational(1, 2))
    check('slope_first_PN', sy.series(slope, x, 0, 2).removeO()-(1-sy.Rational(3, 2)*x))
    check('inverse_slope_first_PN', sy.series(1/slope, x, 0, 2).removeO()-(1+sy.Rational(3, 2)*x))
    power = sy.symbols('P', positive=True)
    rate = 2*power/(particle*slope)
    check('orbital_energy_balance', particle*sy.diff(energy, x)*rate+power)
    check('orbital_angular_momentum_balance', sy.diff(angular_momentum, x)*rate+power/orbital_frequency)
    point_power = sy.Rational(32, 5)*(particle/mass)**2*x**5
    newton_rate = sy.Rational(64, 5)*particle/mass**2*x**5
    check('Newtonian_chirp_normalization', 2*point_power/particle-newton_rate)

    radius, distance, strength = sy.symbols('r D A', positive=True)
    growing_horizon = radius**3/(2*mass)**3
    outgoing = -3/(omega**2*radius**2)
    wronskian = growing_horizon*sy.diff(outgoing, radius)-sy.diff(growing_horizon, radius)*outgoing
    jump, jump_slope = strength*distance/2, -strength/2
    inward = (jump_slope*outgoing.subs(radius, distance)-jump*sy.diff(outgoing, radius).subs(radius, distance))/wronskian
    check('horizon_unit_normalized_amplitude', inward+strength*(2*mass)**3/(10*distance**2))
    projected_strength = 8*sy.pi/3*particle*omega*sy.sqrt(15/(8*sy.pi))
    horizon_power = sy.simplify(3*omega**2/(4*sy.pi)*inward.subs(strength, projected_strength)**2)
    horizon_power = sy.simplify(horizon_power.subs(omega**2, mass/distance**3).subs(distance, mass/x))
    check('derived_horizon_power_over_Newtonian_x5', horizon_power/point_power-x**5)
    bookkeeping = sy.symbols('epsilon', positive=True)
    metric = 1-2*bookkeeping*mass/radius
    decay = radius**-2*(1+bookkeeping*5*mass/(3*radius)+bookkeeping*omega**2*radius**2/6)
    growing = radius**3*(1-bookkeeping*omega**2*radius**2/14)
    source_numerator = -strength/2*(1-2*bookkeeping*mass/distance)*decay.subs(radius, distance)
    source_numerator -= strength*distance/2*(metric*sy.diff(decay, radius)).subs(radius, distance)
    numerator_ratio = sy.series(source_numerator/(strength/(2*distance**2)), bookkeeping, 0, 2).removeO()
    horizon_ratio = sy.series(numerator_ratio**2/(1-3*bookkeeping*mass/distance), bookkeeping, 0, 2).removeO()
    horizon_ratio = sy.expand(horizon_ratio.subs(omega**2, mass/distance**3).subs(mass, x*distance))
    check('horizon_power_first_PN_16over3', horizon_ratio-1-bookkeeping*sy.Rational(16, 3)*x)
    check('outgoing_normalization_cancels_horizon_amplitude', factor*source_numerator/(factor*wronskian)-source_numerator/wronskian)

    beta = sy.symbols('beta', real=True)
    velocity = sy.symbols('v', positive=True)
    magnetic_flux_ratio = 1+sy.Rational(173, 84)*velocity**2+2*sy.pi*velocity**3
    magnetic_chirp_ratio = sy.series(magnetic_flux_ratio/slope.subs(x, velocity**2), velocity, 0, 4).removeO()
    check('magnetic_chirp_relative_299over84', magnetic_chirp_ratio-1-sy.Rational(299, 84)*velocity**2-2*sy.pi*velocity**3)
    absorption_chirp = sy.series((1+sy.Rational(16, 3)*velocity**2)/slope.subs(x, velocity**2), velocity, 0, 4).removeO()
    check('removed_absorption_chirp_relative_41over6', absorption_chirp-1-sy.Rational(41, 6)*velocity**2)
    check('leading_total_axial_crossover', (-beta*x**6/3-x**5).subs(x, -3/beta))

    reference_flux = 1-sy.Rational(1247, 336)*velocity**2+4*sy.pi*velocity**3
    phase_prefactor = sy.series(slope.subs(x, velocity**2)/reference_flux**2, velocity, 0, 4).removeO()
    check('phase_prefactor_first_PN_and_tail', phase_prefactor-1-sy.Rational(995, 168)*velocity**2+8*sy.pi*velocity**3)
    magnetic_phase_ratio = sy.series(phase_prefactor*magnetic_flux_ratio, velocity, 0, 4).removeO()
    check('magnetic_phase_ratio_447over56_minus6pi', magnetic_phase_ratio-1-sy.Rational(447, 56)*velocity**2+6*sy.pi*velocity**3)
    absorption_phase_ratio = sy.series(phase_prefactor*(1+sy.Rational(16, 3)*velocity**2), velocity, 0, 4).removeO()
    check('absorption_phase_ratio_1891over168_minus8pi', absorption_phase_ratio-1-sy.Rational(1891, 168)*velocity**2+8*sy.pi*velocity**3)
    magnetic_density = sy.Rational(5, 96)*beta*x**sy.Rational(5, 2)*(1+sy.Rational(447, 56)*x-6*sy.pi*x**sy.Rational(3, 2))
    absorption_density = sy.Rational(5, 32)*x**sy.Rational(3, 2)*(1+sy.Rational(1891, 168)*x-8*sy.pi*x**sy.Rational(3, 2))
    magnetic_primitive = sy.Rational(5, 96)*beta*(sy.Rational(2, 7)*x**sy.Rational(7, 2)
                        +sy.Rational(149, 84)*x**sy.Rational(9, 2)-sy.Rational(6, 5)*sy.pi*x**5)
    absorption_primitive = sy.Rational(5, 32)*(sy.Rational(2, 5)*x**sy.Rational(5, 2)
                          +sy.Rational(1891, 588)*x**sy.Rational(7, 2)-2*sy.pi*x**4)
    check('magnetic_phase_primitive', sy.diff(magnetic_primitive, x)-magnetic_density)
    check('absorption_phase_primitive', sy.diff(absorption_primitive, x)-absorption_density)
    check('magnetic_phase_leading_stage23_limit', magnetic_primitive.coeff(beta).expand().coeff(x**sy.Rational(7, 2))-sy.Rational(5, 336))
    check('general_linear_phase_variation', sy.diff(2*orbital_frequency*(-particle*sy.diff(energy, x))/(power+bookkeeping), bookkeeping).subs(bookkeeping, 0)
          +2*orbital_frequency*(-particle*sy.diff(energy, x))/power**2)

    mp.mp.dps = 50
    damping_checks = []
    quadratures = []
    for omega_text, length_text in [('0.03', '2'), ('0.2', '0.7')]:
        frequency, length = mp.mpf(omega_text), mp.mpf(length_text)
        errors = []
        for damping in ['0.0001', '0.00001', '0.000001']:
            argument = frequency*(mp.mpf(damping)-1j)
            integral = (-mp.euler-mp.log(argument)-mp.log(2*length)+mp.mpf(7)/6)/argument
            correction = -2*frequency**2*integral
            errors.append(float(abs(mp.re(correction)/(mp.pi*frequency)-1)))
        assert errors[-1] < 1e-5 and all(first > second for first, second in zip(errors, errors[1:]))
        damping_checks.append({'frequency': omega_text, 'scale': length_text, 'relative_errors': errors})
        for damping in [mp.mpf('0.5'), mp.mpf('1')]:
            numerical = mp.quad(lambda variable: mp.exp(-(damping-1j)*variable)
                                *(mp.log(variable)-mp.log(2*length*frequency)+mp.mpf(7)/6),
                                [0, 1, 2, 4, 8, 16, 32, 64, 128, 256])/frequency
            argument = frequency*(damping-1j)
            exact = (-mp.euler-mp.log(argument)-mp.log(2*length)+mp.mpf(7)/6)/argument
            error = abs(numerical/exact-1)
            assert error < mp.mpf('1e-35'), error
            quadratures.append({'frequency': omega_text, 'scale': length_text, 'damping_over_frequency': str(damping),
                                'relative_error': str(error)})
    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=False)
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'checks': checks, 'exact_checks': len(checks),
              'tail_kernel_source': 'Blanchet-Qusailah-Will2005 Eq4c, PDFpage3; retained GR input',
              'amplitude_correction': str(amplitude.subs(constant, sy.Rational(7, 6))),
              'flux_tail_m1': '2*pi*x^(3/2)', 'flux_tail_m2': '4*pi*x^(3/2)',
              'infinity_magnetic_PN_coefficients': ['173/84', '2*pi'],
              'chirp_magnetic_PN_coefficients': ['299/84', '2*pi'],
              'phase_density_magnetic_PN_coefficients': ['447/56', '-6*pi'],
              'horizon_power_over_Newtonian': 'x^5*(1+16*x/3+O(x^2))',
              'phase_density_removed_absorption_coefficients': ['1891/168', '-8*pi'],
              'geodesic_slope': str(slope), 'phase_magnetic_primitive_times_q': str(magnetic_primitive),
              'phase_absorption_primitive_times_q': str(absorption_primitive),
              'damping_checks': damping_checks, 'direct_complex_integral_quadratures': quadratures,
              'new_body_fits': 0, 'finite_mass_ratio_claim': False,
              'phase_scope': 'Linear axial-channel contribution to Phi=2 orbital phase, leading q=mu/M, point reference through1.5PN; not full waveform.',
              'point_PN_reference_source': str(ROOT.parent/'pn-balance-20261004/21-electric-tidal-PN-radiation-and-balance.md')}
    (output/'status.json').write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks), 'direct_quadratures': len(quadratures)}))


if __name__ == '__main__':
    main()
