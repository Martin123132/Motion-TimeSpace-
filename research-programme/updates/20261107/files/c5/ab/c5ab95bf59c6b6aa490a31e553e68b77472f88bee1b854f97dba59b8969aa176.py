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
    output = ROOT/'results/far-action'
    output.mkdir(parents=True, exist_ok=False)
    radius, orbit, mass, particle, tidal_lambda, harmonic, sigma = sp.symbols('r D M mu lambda Ybar sigma', positive=True)
    azimuth = sp.symbols('m', real=True)
    metric = 1-2*mass/radius
    common = 8*sp.pi*particle*harmonic/sp.sqrt(1-3*mass/orbit)
    jump_a = common*(orbit-2*mass)/(3*(2*orbit+3*mass))
    jump_b = -common*(12*orbit**3-16*orbit**2*mass-24*orbit*mass**2-33*mass**3)/(6*orbit**2*(2*orbit+3*mass)**2)+common*mass*(azimuth**2-4)/(6*orbit**2)
    decaying = radius**-2+2*mass/(3*radius**3)+sigma**2/6
    overlap = (jump_b*decaying-jump_a*metric*sp.diff(decaying, radius)).subs(radius, orbit).subs(sigma**2, azimuth**2*mass/orbit**3)
    leading_overlap = -8*sp.pi*particle*harmonic/(6*orbit**3)
    ratio = sp.series(overlap/leading_overlap, mass, 0, 2).removeO().expand()
    checks = []

    def exact(name, expression):
        assert sp.factor(expression) == 0, (name, sp.factor(expression))
        checks.append({'name': name, 'passed': True})

    exact('source_overlap_first_PN_all_even_m', ratio-1-(7-azimuth**2)*mass/(2*orbit))
    square_ratio = sp.series(ratio**2, mass, 0, 2).removeO().expand()
    total_ratio = (square_ratio.subs(azimuth, 0)+3*square_ratio.subs(azimuth, 2))/4
    exact('action_first_PN_coefficient_four', total_ratio-1-4*mass/orbit)
    omega = sp.symbols('Omega', positive=True)
    circular_radius = (mass/omega**2)**sp.Rational(1, 3)
    leading_action = sp.Rational(3, 2)*tidal_lambda*particle**2/circular_radius**6
    action = leading_action*(1+4*mass/circular_radius)
    energy = omega*sp.diff(action, omega)-action
    momentum = sp.diff(action, omega)
    exact('energy_first_PN_coefficient_44_over_9', energy-3*leading_action*(1+sp.Rational(44, 9)*mass/circular_radius))
    exact('momentum_first_PN_coefficient_14_over_3', momentum-4*leading_action/omega*(1+sp.Rational(14, 3)*mass/circular_radius))
    exact('published_adiabatic_energy_test_mass_limit', sp.Rational(11, 4)*(3+2+3)/sp.Rational(9, 2)-sp.Rational(44, 9))
    report = {'state': 'complete', 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'checks': checks, 'overlap_ratio': str(ratio), 'action_ratio': str(total_ratio),
              'action': str(action), 'energy': str(sp.factor(energy)), 'angular_momentum': str(sp.factor(momentum)),
              'scope': 'First relative PN conservative electric quadrupole at leading nontrivial mass ratio, fixed body. Frequency-dependent interior terms begin beyond this far-orbit order. Not a complete first-PN flux or inspiral.'}
    (output/'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'action_ratio': str(total_ratio)}))


if __name__ == '__main__':
    main()
