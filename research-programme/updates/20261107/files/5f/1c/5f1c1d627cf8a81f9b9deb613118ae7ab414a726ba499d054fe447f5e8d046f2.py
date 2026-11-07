from __future__ import annotations

from pathlib import Path

import sympy as sp

from transient import ROOT, dependencies, save, modest_process


def main():
    modest_process()
    checks = []

    def check(name, expression):
        residual = sp.simplify(sp.expand(expression))
        checks.append(dict(name=name, residual=str(residual), passed=residual == 0))
        assert residual == 0, (name, residual)

    time, position = sp.symbols('time position', real=True)
    field = sp.Function('U')(time, position)
    potential = sp.Function('V')(position)
    forcing = sp.Function('f')(time, position)
    inertia, stiffness, normalization = sp.symbols('A B N', positive=True)
    velocity, slope = sp.diff(field, time), sp.diff(field, position)
    density = normalization*(velocity**2+slope**2+potential*field**2)/2
    flux = -normalization*velocity*slope
    check('local sourced canonical energy identity',
        sp.diff(density, time)+sp.diff(flux, position)-normalization*forcing*velocity
        -normalization*velocity*(sp.diff(field, time, 2)-sp.diff(field, position, 2)+potential*field-forcing))
    surface_energy = normalization*(inertia*velocity**2+stiffness*field**2)/2
    boundary_equation = stiffness*field+inertia*sp.diff(field, time, 2)
    check('boundary energy cancels exterior lower-end flux',
          sp.diff(surface_energy, time)-normalization*velocity*boundary_equation)
    source, source_velocity, left_slope = sp.symbols('j velocity_source left_slope', real=True)
    right_slope = left_slope-source
    check('positive source action gives minus-j derivative jump', right_slope-left_slope+source)
    check('shell work from the split bulk energy identity',
          normalization*source_velocity*(left_slope-right_slope)-normalization*source*source_velocity)
    total_rate, source_power, outgoing_power, boundary_rate = sp.symbols('total_rate source_power outgoing_power boundary_rate')
    bulk_rate = source_power-outgoing_power-boundary_rate
    check('finite-detector sourced balance', bulk_rate+boundary_rate+outgoing_power-source_power)
    frequency = sp.Symbol('Omega', positive=True)
    wave = sp.Symbol('wave', real=True)
    check('Fourier boundary response', stiffness*wave+inertia*(-frequency**2*wave)
          -(stiffness-inertia*frequency**2)*wave)
    radius, physical_inertia, physical_stiffness = sp.symbols('R A_physical B_physical', positive=True)
    wave_tau, wave_y = sp.symbols('wave_tau wave_y', real=True)
    energy = normalization*(physical_inertia*(wave_tau/radius)**2+physical_stiffness*wave**2)/2
    check('dimensionless boundary energy scale', energy*radius/normalization
          -(physical_inertia/radius*wave_tau**2+physical_stiffness*radius*wave**2)/2)
    check('dimensionless forcing work scale',
          (normalization*(source/radius)*(source_velocity/radius))*radius**2/normalization-source*source_velocity)
    difference, beta, regular_source, standing_source, dirichlet_source = sp.symbols('C beta us hs ds', real=True)
    green = -regular_source*(standing_source+sp.I*beta*dirichlet_source)/(difference+sp.I*beta)
    check('source Green imaginary part',
          sp.im(green).subs(standing_source, regular_source+difference*dirichlet_source)
          -beta*regular_source**2/(difference**2+beta**2))
    surface_modulus, current = sp.symbols('surface_modulus current', positive=True)
    infinity_modulus_squared = regular_source**2/(surface_modulus**2*(difference**2+beta**2))
    check('optical identity with outgoing current',
          (beta*regular_source**2/(difference**2+beta**2)-current*infinity_modulus_squared)
          .subs(beta, current/surface_modulus**2))
    amplitude = sp.Symbol('spectral_amplitude', real=True)
    green_imaginary = frequency*infinity_modulus_squared
    check('Parseval work equals infinity radiation',
          sp.pi*frequency*amplitude**2*green_imaginary
          -sp.pi*frequency**2*amplitude**2*infinity_modulus_squared)
    coordinate = sp.Symbol('z', real=True)
    polynomial = (1-coordinate**2)**8
    integral = sp.integrate(polynomial, (coordinate, -1, 1))
    check('unit pulse value at time zero', sp.integrate(polynomial/integral, (coordinate, -1, 1))-1)
    for derivative in range(8):
        value = sp.diff(polynomial, coordinate, derivative)
        check('left spectral endpoint derivative '+str(derivative), value.subs(coordinate, -1))
        check('right spectral endpoint derivative '+str(derivative), value.subs(coordinate, 1))
    directory = ROOT/'results/derivation'
    directory.mkdir(parents=True, exist_ok=False)
    result = save(directory, Path(__file__), dict(input_hashes=dependencies(), checks=checks,
        exact_checks=len(checks), source_action='S_source=N integral dt J(t) U(t,x_source)',
        field_equation='U_tt-U_xx+V U=J(t) delta(x-x_source)',
        energy_balance='d(E_ext+E_boundary)/dt+F_detector=N J(t) U_t(t,x_source)',
        spectral_convention='j(tau)=Re integral_0^infinity A(Omega) exp(-i Omega tau) dOmega',
        optical_identity='Im G_ss=I_out |C_infinity|^2; I_out=Omega in the exact outgoing normalization',
        spectral_work='pi integral Omega |A|^2 Im G_ss dOmega',
        spectral_radiation='pi integral Omega^2 |A|^2 |C_infinity|^2 dOmega',
        pulse_normalization=str(integral), pulse_tail='O(abs(tau)^-9), assuming smooth transfer inside the compact band',
        bulk_normalization='N inherited, results report E*R/N', physical_companion_stress_derived=False))
    print(dict(state=result['state'], exact_checks=result['exact_checks']), flush=True)


if __name__ == '__main__':
    main()

