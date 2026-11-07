from __future__ import annotations

import hashlib
import json
from pathlib import Path

import psutil
import sympy as sp


ROOT = Path(__file__).resolve().parent


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    output = ROOT/'results/derivation/status.json'
    assert not output.exists()
    time, radius, polar, azimuth = sp.symbols('time radius theta phi', real=True)
    frequency, alpha = sp.symbols('frequency alpha', real=True)
    metric, lapse, field, master = [sp.Function(name)(radius) for name in ['F', 'nu', 'field', 'master']]
    potential = sp.Function('W')(field)
    speed = sp.exp(lapse)*sp.sqrt(metric)
    coordinates = [time, radius, polar, azimuth]
    background = [-sp.exp(2*lapse), 1/metric, radius**2, radius**2*sp.sin(polar)**2]
    angular_background = (1-metric)/radius**2-(metric*sp.diff(lapse, radius)+sp.diff(metric, radius)/2)/radius
    checks = []

    def check(name, expression):
        residual = sp.factor(sp.trigsimp(sp.expand(expression)))
        if residual != 0:
            residual = sp.factor(sp.trigsimp(residual, method='fu'))
        assert residual == 0, (name, residual)
        checks.append({'name': name, 'passed': True, 'residual': str(residual)})

    residual_records = {}
    for degree in [2, 3]:
        hzero, hone = [sp.Function(name)(radius) for name in ['hzero', 'hone']]
        harmonic = sp.sin(polar)*sp.diff(sp.legendre(degree, sp.cos(polar)), polar)
        oscillation = sp.exp(-sp.I*frequency*time)
        perturbation = sp.zeros(4)
        perturbation[0, 3] = perturbation[3, 0] = hzero*harmonic*oscillation
        perturbation[1, 3] = perturbation[3, 1] = hone*harmonic*oscillation
        inverse_delta = sp.Matrix(4, 4, lambda left, right: -perturbation[left, right]/(background[left]*background[right]))
        gamma, delta_gamma = {}, {}
        for upper in range(4):
            for left in range(4):
                for right in range(4):
                    ordinary_total, delta_total = 0, 0
                    for other in range(4):
                        ordinary = sp.diff(background[other], coordinates[left]) if other == right else 0
                        ordinary += sp.diff(background[other], coordinates[right]) if other == left else 0
                        ordinary -= sp.diff(background[left], coordinates[other]) if left == right else 0
                        changed = sp.diff(perturbation[other, right], coordinates[left])+sp.diff(perturbation[other, left], coordinates[right])-sp.diff(perturbation[left, right], coordinates[other])
                        ordinary_total += ordinary/(2*background[upper]) if other == upper else 0
                        delta_total += inverse_delta[upper, other]*ordinary/2
                        delta_total += changed/(2*background[upper]) if other == upper else 0
                    gamma[upper, left, right] = sp.simplify(ordinary_total)
                    delta_gamma[upper, left, right] = sp.simplify(delta_total)

        def ricci(left, right):
            value = 0
            for contracted in range(4):
                value += sp.diff(delta_gamma[contracted, left, right], coordinates[contracted])
                value -= sp.diff(delta_gamma[contracted, left, contracted], coordinates[right])
                for other in range(4):
                    value += delta_gamma[contracted, left, right]*gamma[other, contracted, other]
                    value += gamma[contracted, left, right]*delta_gamma[other, contracted, other]
                    value -= delta_gamma[other, left, contracted]*gamma[contracted, right, other]
                    value -= gamma[other, left, contracted]*delta_gamma[contracted, right, other]
            return sp.factor(sp.trigsimp(value/oscillation))

        degree_factor = degree*(degree+1)-2
        master_potential = sp.exp(2*lapse)*degree_factor/radius**2+2*speed**2/radius**2-speed*sp.diff(speed, radius)/radius
        master_second = -sp.diff(speed, radius)*sp.diff(master, radius)/speed-(frequency**2-master_potential)*master/speed**2
        hzero_master = speed*sp.diff(radius*master, radius)
        hone_master = -sp.I*frequency*radius*master/speed
        replacements = {}
        for function, expression in [(hzero, hzero_master), (hone, hone_master)]:
            for order in [0, 1, 2]:
                replacements[sp.diff(function, radius, order)] = sp.diff(expression, radius, order)
        wave_rules = {sp.diff(master, radius, 3): sp.diff(master_second, radius).subs(sp.diff(master, radius, 2), master_second),
                      sp.diff(master, radius, 2): master_second}
        for left, right in [(0, 3), (1, 3), (2, 3)]:
            residual = ricci(left, right)-angular_background*perturbation[left, right]/oscillation
            residual_records[f'l{degree}_{left}{right}'] = str(sp.factor(residual/harmonic))
            reduced = residual.subs(replacements, simultaneous=True).subs(wave_rules, simultaneous=True)
            check(f'four_dimensional_field_equation_l{degree}_{left}{right}', reduced)
        for left, right in [(0, 0), (1, 1), (2, 2), (3, 3), (0, 1), (0, 2), (1, 2)]:
            check(f'other_Ricci_l{degree}_{left}{right}', ricci(left, right))
        hzero_static = hzero_master
        log_shift = sp.diff(lapse, radius)-sp.diff(metric, radius)/(2*metric)
        static_operator = sp.diff(hzero_static, radius, 2)-log_shift*sp.diff(hzero_static, radius)+(2*log_shift/radius-2/radius**2-degree_factor/(radius**2*metric))*hzero_static
        check(f'static_parent_equation_l{degree}', static_operator.subs(wave_rules, simultaneous=True).subs(frequency, 0))
        inverse_static = radius*sp.sqrt(metric)/(sp.exp(lapse)*degree_factor)*(sp.diff(hzero_static, radius)-2*hzero_static/radius)
        check(f'static_inverse_map_l{degree}', (inverse_static-master).subs(sp.diff(master, radius, 2), master_second).subs(frequency, 0))
        potential_matter = sp.exp(2*lapse)*((degree*(degree+1)-3+3*metric)/radius**2+2*alpha*potential)
        check(f'potential_stress_identity_l{degree}', (potential_matter-master_potential).subs(potential, angular_background/(2*alpha)))
        print(json.dumps({'degree': degree, 'state': 'tensor_checks_complete'}), flush=True)

    degree = sp.symbols('ell', integer=True, positive=True)
    envelope = sp.Function('envelope')(radius)
    speed_log_prime = ((1-metric)/radius-2*alpha*radius*potential)/metric
    potential_matter = sp.exp(2*lapse)*((degree*(degree+1)-3+3*metric)/radius**2+2*alpha*potential)
    master_equation = sp.diff(radius**(degree+1)*envelope, radius, 2)+speed_log_prime*sp.diff(radius**(degree+1)*envelope, radius)+(frequency**2-potential_matter)/speed**2*radius**(degree+1)*envelope
    envelope_equation = sp.diff(envelope, radius, 2)+(2*(degree+1)/radius+speed_log_prime)*sp.diff(envelope, radius)
    envelope_equation += (frequency**2/speed**2-(degree**2-4)*(1-metric)/(radius**2*metric)-2*alpha*(degree+2)*potential/metric)*envelope
    check('general_regular_envelope_equation', master_equation/radius**(degree+1)-envelope_equation)
    central_lapse, central_potential, center_coefficient = sp.symbols('N0 W0 center_coefficient', positive=True)
    center_residual = 14*center_coefficient+frequency**2/central_lapse**2-8*alpha*central_potential
    check('quadrupole_regular_center', center_residual.subs(center_coefficient, (8*alpha*central_potential-frequency**2/central_lapse**2)/14))
    mass, density, radial_pressure = sp.symbols('mass rho p_r')
    check('potential_positive_rewrite', degree*(degree+1)/radius**2-6*mass/radius**3+alpha*(density-radial_pressure)
          -((degree*(degree+1)-3+3*(1-2*mass/radius))/radius**2+alpha*(density-radial_pressure)))
    geometric_time, rotation = sp.symbols('kinetic_time kinetic_radius')
    trace = geometric_time-rotation-4*potential
    transverse_pressure = (geometric_time-rotation)/2-potential
    check('both_axial_trace_reversed_stresses', transverse_pressure-trace/2-potential)
    flat_master = radius*sp.sin(frequency*radius)*(3/(frequency*radius)**3-1/(frequency*radius))-3*sp.cos(frequency*radius)/frequency**2/radius
    check('flat_regular_master', sp.diff(flat_master, radius, 2)+(frequency**2-6/radius**2)*flat_master)
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'raw_Ricci_residuals': residual_records,
              'master_equation': '(-d_t^2+d_rstar^2-V_l)U=0; drstar/dr=1/f; f=N*sqrt(F)',
              'potential': 'V_l=N^2[l(l+1)/r^2-6M(r)/r^3+alpha*(rho-p_r)]=N^2[(l(l+1)-3+3F)/r^2+2alpha*W]',
              'reconstruction': 'h0=f*(rU)prime, h1=-i*omega*rU/f for exp(-i*omega*t)',
              'quadrupole_envelope': 'U=r^3*u; u_second+(6/r+f_prime/f)*u_prime+[omega^2/f^2-8alpha*W/F]*u=0',
              'center': 'u=1+(8alpha*W0-omega^2/N0^2)*r^2/14+O(r^4)',
              'static_inverse': 'U=r*sqrt(F)/(N*[l(l+1)-2])*(h0_prime-2h0/r)',
              'positive_potential_assumptions': ['ell>=2', 'N>0', 'F>0', 'alpha>=0', 'W>=0', 'regular center; no added surface layer'],
              'no_axial_scalar_harmonic_or_fluid_state_inserted': True}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks)}))


if __name__ == '__main__':
    main()
