from __future__ import annotations

import sympy as sy

from eccentric_radiation import ROOT, BRANCH, digest, modest_process, save_json, report_header


def main():
    modest_process()
    checks = []

    def check(name, expression):
        residual = sy.factor(sy.cancel(sy.expand(expression)))
        checks.append({'name': name, 'passed': residual == 0, 'residual': str(residual)})
        assert residual == 0, (name, residual)

    frequency, azimuthal, amplitude2 = sy.symbols('omega m amplitude_squared', real=True)
    per_mode = sy.Rational(24, 64)/sy.pi
    check('MP_odd21_pair_factor', 2*per_mode-sy.Rational(3, 4)/sy.pi)
    angular_flux = 2*per_mode*sy.I*azimuthal*(-sy.I*frequency)*amplitude2
    energy_flux = 2*per_mode*frequency**2*amplitude2
    check('pair_energy_angular_relation', frequency*angular_flux-azimuthal*energy_flux)
    check('negative_frequency_energy_even', energy_flux.subs(frequency, -frequency)-energy_flux)
    check('negative_frequency_angular_odd_at_fixed_m', angular_flux.subs(frequency, -frequency)+angular_flux)
    check('negative_m_reality_pair_angular_equal', angular_flux.subs({frequency: -frequency, azimuthal: -azimuthal}, simultaneous=True)-angular_flux)
    check('zero_frequency_no_radiated_energy', energy_flux.subs(frequency, 0))
    check('zero_frequency_no_radiated_angular_momentum', angular_flux.subs(frequency, 0))
    phase, velocity, radial_value, radial_slope, metric_over_radius, jump = sy.symbols('phase u y yp f_over_r j', real=True)
    kernel = -jump*sy.exp(sy.I*phase)*((metric_over_radius+sy.I*frequency*velocity)*radial_value+radial_slope)
    mirror = kernel.subs({phase: -phase, velocity: -velocity}, simultaneous=True)
    check('full_orbit_reflection_conjugates_real_basis_kernel', sy.expand_complex(mirror-sy.conjugate(kernel)))
    half_kernel = -2*jump*((metric_over_radius*radial_value+radial_slope)*sy.cos(phase)-frequency*velocity*radial_value*sy.sin(phase))
    check('half_orbit_cosine_sine_integrand', sy.expand_complex(kernel+mirror)-half_kernel)
    time, duration = sy.symbols('t T', positive=True, real=True)
    check('distinct_radial_harmonics_average_to_zero', sy.integrate(sy.exp(6*sy.pi*sy.I*time/duration), (time, 0, duration)))
    alpha, displacement, beta_out, beta_horizon, integral_real, integral_dirichlet = sy.symbols('a d o h R Q', real=True)
    wronskian_horizon = alpha+sy.I*(beta_out-beta_horizon)
    wronskian_body = alpha-displacement+sy.I*beta_out
    wronskian_difference = -displacement+sy.I*beta_horizon
    source_out = integral_real+sy.I*beta_out*integral_dirichlet
    source_horizon = integral_real-alpha*integral_dirichlet+sy.I*beta_horizon*integral_dirichlet
    source_body = integral_real+(displacement-alpha)*integral_dirichlet
    reference = source_horizon/wronskian_horizon
    difference = -wronskian_difference*source_out/(wronskian_body*wronskian_horizon)
    check('stable_outgoing_amplitude_difference', source_body/wronskian_body-reference-difference)
    infinity_increment = beta_out*(sy.conjugate(reference)*difference+reference*sy.conjugate(difference)+difference*sy.conjugate(difference))
    horizon_power_signed = -beta_horizon*source_out*sy.conjugate(source_out)/(wronskian_horizon*sy.conjugate(wronskian_horizon))
    optical = -(difference*source_out-sy.conjugate(difference*source_out))/(2*sy.I)
    check('modal_optical_source_work_identity', optical-infinity_increment+horizon_power_signed)
    alternate_source_real, alternate_source_dirichlet = sy.symbols('R2 Q2', real=True)
    second_out = alternate_source_real+sy.I*beta_out*alternate_source_dirichlet
    check('reciprocal_response_kernel', difference*second_out-(-wronskian_difference*second_out/(wronskian_body*wronskian_horizon))*source_out)
    check('same_boundary_control', difference.subs({displacement: 0, beta_horizon: 0}))
    factor = sy.Rational(3, 4)/sy.pi
    retarded_imag = -factor/2*(difference*source_out-sy.conjugate(difference*source_out))/(2*sy.I)
    check('source_work_normalization', 2*frequency*retarded_imag-factor*frequency*optical)
    sources = [ROOT/'eccentric_radiation.py', BRANCH/'eccentric-source-20261005/30-conserved-eccentric-source-and-moving-jumps.md',
               BRANCH/'companion-source-20261004/sources/martel-poisson-2005.pdf',
               BRANCH/'axial-reciprocity-20261005/axial_action.py', BRANCH/'eccentric-source-20261005/results/stage-integrity.json']
    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=False)
    save_json(output/'status.json', {**report_header(__file__), 'checks': checks, 'exact_checks': len(checks),
              'input_hashes': {str(path): digest(path) for path in sources},
              'scope': 'Odd21 pair, m+1 sidebands at both signs plus m-1 reality partners, canonical pericentre time/azimuth.',
              'optical_identity': '2 omega Im F_ret = Delta P_infinity - P_horizon_BH',
              'retarded_overlap_phase_assumption': 'Projected radial Fourier source real in pericentre phase convention; other phase choices require dual conjugate source pairing.',
              'full_self_force_or_orbital_evolution_derived': False})
    print({'state': 'complete', 'exact_checks': len(checks)})


if __name__ == '__main__':
    main()
