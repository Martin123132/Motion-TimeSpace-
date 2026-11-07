from __future__ import annotations

from datetime import datetime, timezone
import sympy as sp

from common import ROOT, PARENT, digest, write_json, modest_process


def main():
    modest_process()
    checks = []

    def exact(name, expression):
        residual = sp.simplify(expression)
        assert residual == 0, (name, residual)
        checks.append(dict(name=name, passed=True, residual=str(residual)))

    semilatus, initial, mass, tidal, bookkeeping = sp.symbols('p pi M Lambda epsilon', positive=True)
    shrink = -sp.Rational(64, 5)/(mass**2*semilatus**3)
    damping = -sp.Rational(608, 15)/(mass**2*semilatus**4)
    orbital_frequency = 1/(mass*semilatus**sp.Rational(3, 2))
    exact('Newtonian logarithmic eccentricity-squared slope', damping/shrink-sp.Rational(19, 6)/semilatus)
    clock = sp.Rational(5, 256)*(initial**4-semilatus**4)
    phase = (initial**sp.Rational(5, 2)-semilatus**sp.Rational(5, 2))/32
    log_squared = sp.Rational(19, 6)*sp.log(semilatus/initial)
    exact('Newtonian mass-scaled elapsed time primitive', sp.diff(clock, semilatus)-1/(mass**2*shrink))
    exact('Newtonian mass-scaled orbital phase primitive', sp.diff(phase, semilatus)-orbital_frequency/(mass*shrink))
    exact('Newtonian eccentricity primitive', sp.diff(log_squared, semilatus)-damping/shrink)

    body_shrink = shrink*(1+bookkeeping*6*tidal/semilatus**5)
    hole_shrink = shrink*(1+bookkeeping/semilatus**4)
    body_damping = damping*(1+bookkeeping*sp.Rational(459, 19)*tidal/semilatus**5)
    hole_damping = damping*(1+bookkeeping*sp.Rational(54, 19)/semilatus**4)
    difference_clock = -sp.Rational(15, 32)*tidal/semilatus-sp.Rational(5, 64)*sp.log(semilatus)
    difference_phase = -sp.Rational(3, 16)*tidal/semilatus**sp.Rational(5, 2)+sp.Rational(5, 96)/semilatus**sp.Rational(3, 2)
    difference_log = -sp.Rational(23, 2)*tidal/semilatus**5+sp.Rational(35, 24)/semilatus**4
    clock_integrand = sp.diff((1/body_shrink-1/hole_shrink)/mass**2, bookkeeping).subs(bookkeeping, 0)
    phase_integrand = clock_integrand*mass*orbital_frequency
    log_integrand = sp.diff(body_damping/body_shrink-hole_damping/hole_shrink, bookkeeping).subs(bookkeeping, 0)
    exact('leading outgoing plus horizon time primitive', sp.diff(difference_clock, semilatus)-clock_integrand)
    exact('leading outgoing plus horizon phase primitive', sp.diff(difference_phase, semilatus)-phase_integrand)
    exact('leading outgoing plus horizon eccentricity primitive', sp.diff(difference_log, semilatus)-log_integrand)

    reference_shrink, increment_shrink, reference_damping, increment_damping = sp.symbols('P dP G dG', nonzero=True)
    exact('stable difference of reciprocal shrinkage', 1/(reference_shrink+increment_shrink)-1/reference_shrink
          +increment_shrink/(reference_shrink*(reference_shrink+increment_shrink)))
    exact('stable logarithmic-e difference', (reference_damping+increment_damping)/(reference_shrink+increment_shrink)-reference_damping/reference_shrink
          -(increment_damping*reference_shrink-reference_damping*increment_shrink)/(reference_shrink*(reference_shrink+increment_shrink)))
    delay, decay, residue = sp.symbols('s gamma A', positive=True)
    for order in [0, 1, 2]:
        moment = sp.integrate(residue*sp.exp(-decay*delay)*delay**order, (delay, 0, sp.oo))
        exact('absolute damped-pole kernel moment '+str(order), moment-residue*sp.factorial(order)/decay**(order+1))
    omega, phase_rate, time_shift, fixed_radius_difference = sp.symbols('omega phase_rate delta_t delta_phi')
    exact('first-order equal-time phase conversion', fixed_radius_difference+omega*(-time_shift)-(fixed_radius_difference-omega*time_shift))
    output = ROOT/'results/derivation'
    output.mkdir(parents=True, exist_ok=False)
    report = dict(state='complete', script_sha256=digest(__file__), time_utc=datetime.now(timezone.utc).isoformat(),
                  input_hashes={str(PARENT/'results/stage-integrity.json'): digest(PARENT/'results/stage-integrity.json')},
                  checks=checks, scaled_clock=str(clock), scaled_phase=str(phase), log_squared_evolution=str(log_squared),
                  tidal_parameter='Lambda=lambda/M^5',
                  leading_difference_primitives=dict(scaled_clock=str(difference_clock), scaled_phase=str(difference_phase), log_squared=str(difference_log)),
                  memory_bound='For causal q=K*f, |q-A exp(-i phi) chi(omega)| <= sup|A_dot| M1 + (sup|A|/2) sup|omega_dot| M2, provided those kernel moments exist and past derivative bounds hold.',
                  memory_scope='Pole moments are derived; full coupled response moments are not replaced by that pole. Adiabatically prepared histories and no independently excited free oscillation are assumptions.',
                  approximation='Leading test-mass, O(e^0) time/phase and linear e^2 transport; separated leading tidal/horizon terms, not a full PN expansion.')
    write_json(output/'status.json', report, exclusive=True)
    print(len(checks), 'exact identities passed', flush=True)


if __name__ == '__main__':
    main()

