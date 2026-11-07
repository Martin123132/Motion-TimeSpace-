from __future__ import annotations

from datetime import datetime, timezone
import sympy as sp

from carrier import ROOT, PRIOR, digest, write_json, modest_process


def main():
    modest_process()
    checks = []

    def exact(name, expression):
        result = sp.factor(expression)
        assert result == 0, (name, result)
        checks.append(dict(name=name, passed=True, residual=str(result)))

    tide = sp.symbols('k', real=True)
    carrier_quadrupole = 1+tide
    carrier_second = -sp.Rational(1, 2)-sp.Rational(11, 2)*tide
    carrier_power_second = 2*carrier_quadrupole*carrier_second-9*carrier_quadrupole**2
    angular_second = carrier_power_second+sp.Rational(3, 2)*carrier_quadrupole**2
    angular_second += sp.Rational(2, 3)*sp.Rational(729, 64)*(1+sp.Rational(7, 2)*tide)**2
    angular_second += 2*sp.Rational(9, 64)*(1+tide/6)**2
    exact('zero tide P2 normalization', angular_second.subs(tide,0)+sp.Rational(5,8))
    exact('electric tidal P2 coefficient in lambda/r5', 3*sp.diff(angular_second,tide).subs(tide,0)-sp.Rational(315,4))
    horizon_angular_second = -14+sp.Rational(3,2)+sp.Rational(2,3)*sp.Rational(441,16)+2*sp.Rational(1,16)
    exact('horizon P2 coefficient', horizon_angular_second-6)
    semilatus, initial, tidal = sp.symbols('p pi Lambda', positive=True)
    relative_tide = tidal/semilatus**5
    absorption = semilatus**-4
    log_shift = -sp.Rational(23,2)*tidal*(semilatus**-5-initial**-5)+sp.Rational(35,24)*(semilatus**-4-initial**-4)
    eccentricity_factor = (semilatus/initial)**sp.Rational(19,6)
    delta_ratio = sp.Rational(165,2)*relative_tide-sp.Rational(53,8)*absorption
    inverse_fraction = -6*relative_tide+absorption
    clock_bracket = delta_ratio-sp.Rational(5,8)*(inverse_fraction+log_shift)
    phase_bracket = -delta_ratio-sp.Rational(7,8)*(inverse_fraction+log_shift)
    exact('postcircular clock differential bracket', clock_bracket-(sp.Rational(345,4)*relative_tide-sp.Rational(29,4)*absorption-sp.Rational(5,8)*log_shift))
    exact('postcircular phase differential bracket', phase_bracket-(-sp.Rational(309,4)*relative_tide+sp.Rational(23,4)*absorption-sp.Rational(7,8)*log_shift))
    clock_integrand = sp.Rational(5,64)*semilatus**3*eccentricity_factor*clock_bracket
    phase_integrand = -sp.Rational(5,64)*semilatus**sp.Rational(3,2)*eccentricity_factor*phase_bracket
    clock_primitive = sp.integrate(sp.expand(clock_integrand), semilatus)
    phase_primitive = sp.integrate(sp.expand(phase_integrand), semilatus)
    exact('differential postcircular clock primitive', sp.diff(clock_primitive,semilatus)-clock_integrand)
    exact('differential postcircular phase primitive', sp.diff(phase_primitive,semilatus)-phase_integrand)
    directory = ROOT/'results/weak-field'
    directory.mkdir(parents=True,exist_ok=False)
    write_json(directory/'status.json',dict(state='complete', script_sha256=digest(__file__),
        time_utc=datetime.now(timezone.utc).isoformat(),input_hashes={str(PRIOR/'results/stage-integrity.json'):digest(PRIOR/'results/stage-integrity.json')},
        checks=checks, tidal_P2_coefficient='315/4', absorption_P2_coefficient='6',
        differential_clock_primitive=str(clock_primitive), differential_phase_primitive=str(phase_primitive),
        domain='Leading separate electric tidal and absorption terms; not a full PN expansion.'),exclusive=True)
    print(len(checks),'weak-field identities passed',flush=True)


if __name__ == '__main__':
    main()

