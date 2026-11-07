from __future__ import annotations

import math
import time

import numpy as np
import sympy as sym
from scipy import integrate

from bridge_common import ROOT, PARENT, SOURCE_PATHS, modest_process, read_json, digest, save


def oscillator_check(quartic, derivative, amplitude):
    def equation(moment, state):
        field, velocity = state
        return [velocity, -(field + quartic * field**3 / 6) / (1 - 12 * derivative * velocity**2)]

    def crossing(moment, state):
        return state[0]

    crossing.direction = 1
    solution = integrate.solve_ivp(equation, (0., 100.), [amplitude, 0.],
        method='DOP853', rtol=2e-12, atol=2e-14, max_step=.025, events=crossing)
    assert solution.success and len(solution.t_events[0]) > 8
    periods = np.diff(solution.t_events[0][2:])
    measured = 2 * np.pi / np.mean(periods)
    expected = 1 + amplitude**2 * (quartic / 16 + 1.5 * derivative)
    energy = .5 * solution.y[1]**2 - 3 * derivative * solution.y[1]**4 + .5 * solution.y[0]**2 + quartic * solution.y[0]**4 / 24
    return dict(quartic=quartic, derivative_coefficient=derivative, amplitude=amplitude,
        measured_frequency=float(measured), leading_prediction=expected,
        error=abs(float(measured) - expected),
        energy_relative_drift=float(np.ptp(energy) / energy[0]),
        kinetic_min=float(np.min(1 - 12 * derivative * solution.y[1]**2)))


def main():
    modest_process()
    started = time.monotonic()
    checks, identities = [], []

    def check(name, passed, value=None):
        checks.append(dict(name=name, passed=bool(passed), value=value))

    def identity(name, residual):
        result = sym.simplify(residual)
        identities.append(dict(name=name, residual=str(result)))
        check(name, result == 0)

    for path in SOURCE_PATHS:
        check('owner exists:' + path.name, path.is_file())
    sources = read_json(ROOT / 'results/sources/status.json')
    for row in sources['source_rows']:
        check('pinned external source:' + row['repository_path'], digest(row['local_path']) == row['sha256'])
    check('positive temperature not promoted to Lean verified', not sources['lean_independently_compiled'])

    heavy, light, overlap, cubic, quartic, coefficient = sym.symbols('h ell r U3 U4 C2', positive=True)
    mass, light_mass, number, phase, newton, momentum = sym.symbols('M mu n theta G q', positive=True)
    light_overlap = 1 - overlap
    motion = sym.sqrt(light_overlap) * light - sym.sqrt(overlap) * heavy
    potential = cubic * motion**3 / 6 + quartic * motion**4 / 24
    heavy_cubic = sym.diff(potential, heavy, 3).subs({heavy: 0, light: 0})
    light_heavy2 = sym.diff(potential, light, 1, heavy, 2).subs({heavy: 0, light: 0})
    heavy_light2 = sym.diff(potential, heavy, 1, light, 2).subs({heavy: 0, light: 0})
    heavy_quartic = sym.diff(potential, heavy, 4)
    heavy_light3 = sym.diff(potential, heavy, 1, light, 3)
    identity('rotated hhh coupling', heavy_cubic + cubic * overlap**sym.Rational(3, 2))
    identity('rotated ell hh coupling', light_heavy2 - cubic * sym.sqrt(light_overlap) * overlap)
    identity('rotated h ell ell coupling', heavy_light2 + cubic * sym.sqrt(overlap) * light_overlap)
    identity('rotated hhhh coupling', heavy_quartic - quartic * overlap**2)
    identity('rotated h ell ell ell coupling', heavy_light3 + quartic * sym.sqrt(overlap) * light_overlap**sym.Rational(3, 2))
    carrier = sym.sqrt(2 * number / mass) * sym.cos(phase)
    carrier_velocity = -sym.sqrt(2 * number * mass) * sym.sin(phase)
    mean_quartic = sym.integrate(carrier**4, (phase, 0, 2 * sym.pi)) / (2 * sym.pi)
    mean_derivative = sym.integrate(carrier_velocity**4, (phase, 0, 2 * sym.pi)) / (2 * sym.pi)
    contact = overlap**2 * (quartic / (8 * mass**2) + 3 * coefficient * mass**2)
    identity('quartic cycle average', mean_quartic - 3 * number**2 / (2 * mass**2))
    identity('derivative cycle average', mean_derivative - 3 * number**2 * mass**2 / 2)
    identity('contact from averaged action', heavy_quartic * mean_quartic / 24 + coefficient * overlap**2 * mean_derivative - contact * number**2 / 2)
    vertex_threshold = overlap**2 * (quartic + 8 * coefficient * (mass**4 + mass**4 + mass**4))
    identity('independent four-leg threshold vertex', vertex_threshold - 8 * mass**2 * contact)
    propagator_sum = 1 / (4 * mass**2 - mass**2) + 2 / (-mass**2)
    identity('heavy cubic exchange sum', propagator_sum + sym.Rational(5, 3) / mass**2)
    hard_contact = (vertex_threshold - 5 * heavy_cubic**2 / (3 * mass**2) + light_heavy2**2 / (4 * mass**2 - light_mass**2)) / (8 * mass**2)
    yukawa = -light_heavy2**2 / (4 * mass**2 * (momentum**2 + light_mass**2))
    threshold_all_local = (vertex_threshold + heavy_cubic**2 * propagator_sum + light_heavy2**2 * (1 / (4 * mass**2 - light_mass**2) - 2 / light_mass**2)) / (8 * mass**2)
    identity('soft exchange not double counted', hard_contact + yukawa.subs(momentum, 0) - threshold_all_local)
    gaussian_contact = hard_contact.subs({cubic: 0, quartic: 0, coefficient: 0})
    identity('Gaussian matter has zero short range contact', gaussian_contact)
    field_auxiliary, source_coupling, density, kernel = sym.symbols('ell gamma density kernel', real=True, nonzero=True)
    energy_auxiliary = kernel * field_auxiliary**2 / 2 + source_coupling * density * field_auxiliary / (2 * mass)
    minimized = energy_auxiliary.subs(field_auxiliary, -source_coupling * density / (2 * mass * kernel))
    identity('Yukawa sign from field elimination', minimized + source_coupling**2 * density**2 / (8 * mass**2 * kernel))
    gravity = -4 * sym.pi * newton * mass**2 / momentum**2
    dispersion = momentum**4 / (4 * mass**2) + number * momentum**2 * (hard_contact + yukawa + gravity) / mass
    identity('Gaussian returns Stage49 Jeans term', dispersion.subs({cubic: 0, quartic: 0, coefficient: 0}) - momentum**4 / (4 * mass**2) + 4 * sym.pi * newton * mass * number)
    scattering = mass * contact / (4 * sym.pi)
    identity('Born scattering length matches real scalar convention', scattering - vertex_threshold / (32 * sym.pi * mass))
    spectral, bath_frequency, coupling, bare = sym.symbols('s Omega coupling mb', real=True)
    schur = bare**2 - spectral - coupling**2 / (bath_frequency**2 - spectral)
    identity('Gaussian bath remains quadratic after elimination', sym.diff(schur * heavy**2 / 2, heavy, 4))

    invariant = sym.symbols('invariant', positive=True)
    phase3 = sym.integrate((1 - invariant / mass**2) / (128 * sym.pi**3), (invariant, 0, mass**2))
    identity('three-body massless phase space', phase3 - mass**2 / (256 * sym.pi**3))
    width3 = heavy_light3**2 * phase3 / (2 * mass * sym.factorial(3))
    identity('quartic induced heavy decay', width3 - quartic**2 * overlap * light_overlap**3 * mass / (3072 * sym.pi**3))
    pure_scattering = overlap**2 * quartic / (32 * sym.pi * mass)
    identity('elastic strength and decay share one coupling', width3 - light_overlap**3 * mass**3 * pure_scattering**2 / (3 * sym.pi * overlap**3))
    width2 = heavy_light2**2 / (32 * sym.pi * mass) * sym.sqrt(1 - 4 * light_mass**2 / mass**2)

    equations = dict(heavy_cubic=str(heavy_cubic), light_heavy2=str(light_heavy2), heavy_light2=str(heavy_light2),
        heavy_quartic=str(heavy_quartic), heavy_light3=str(heavy_light3),
        contact_without_cubic=str(contact), hard_contact=str(hard_contact), soft_yukawa=str(yukawa),
        full_zero_momentum_contact=str(threshold_all_local), newton_kernel=str(gravity),
        dispersion=str(dispersion), decay_to_two_light=str(width2), decay_to_three_light_massless=str(width3),
        exact_scope='Leading weak-coupling local stationary canonical germ; scalar derivative backgrounds set to zero. Contact matching is not a finite-range-potential or condensate-existence theorem.')

    oscillators = []
    for quartic_value, derivative_value in [(0.4, 0.), (0., .02), (0., -.02), (.4, -.01)]:
        pair = [oscillator_check(quartic_value, derivative_value, amplitude) for amplitude in [.08, .04]]
        for row in pair:
            check('oscillator energy:' + str(row['quartic']) + ':' + str(row['derivative_coefficient']) + ':' + str(row['amplitude']), row['energy_relative_drift'] < 1e-9, row['energy_relative_drift'])
            check('oscillator healthy kinetic coefficient', row['kinetic_min'] > .9, row['kinetic_min'])
        ratio = pair[1]['error'] / pair[0]['error']
        check('independent frequency remainder scales as amplitude fourth power:' + str((quartic_value, derivative_value)), .045 < ratio < .085, float(ratio))
        oscillators.extend(pair)

    random = np.random.default_rng(5207)
    unitary, _ = np.linalg.qr(random.normal(size=(8, 8)) + 1j * random.normal(size=(8, 8)))
    occupation = unitary @ np.diag([2., 1., .7, .4, .2, .1, .05, .01]) @ unitary.conj().T
    mean = random.normal(size=8) + 1j * random.normal(size=8)
    reference_mass = 2.3
    covariance_qq = (occupation.real + .5 * np.eye(8)) / reference_mass
    covariance_pp = reference_mass * (occupation.real + .5 * np.eye(8))
    covariance_qp = occupation.imag
    covariance_pq = -occupation.imag
    reconstructed = np.outer(mean.conj(), mean) + reference_mass * covariance_qq / 2 + covariance_pp / (2 * reference_mass) + .5j * (covariance_qp - covariance_pq) - .5 * np.eye(8)
    expected = np.outer(mean.conj(), mean) + occupation
    error = float(np.max(abs(reconstructed - expected)))
    check('field-momentum reconstruction including complex current covariance', error < 1e-13, error)
    vacuum = reference_mass * (np.eye(8) / (2 * reference_mass)) / 2 + reference_mass * np.eye(8) / (2 * 2 * reference_mass) - .5 * np.eye(8)
    check('canonical vacuum subtraction', float(np.max(abs(vacuum))) < 1e-14)
    check('one-particle matrix positive', float(np.linalg.eigvalsh(reconstructed)[0]) >= -1e-12)
    populations = []
    for count in [8, 32, 128]:
        total = 1000.
        coherent = np.zeros((count, count))
        coherent[0, 0] = total
        fragmented = total * np.eye(count) / count
        check('same total occupation does not fix coherence:' + str(count), abs(np.trace(coherent) - np.trace(fragmented)) < 1e-10 and np.linalg.eigvalsh(coherent)[-1] / total == 1 and abs(np.linalg.eigvalsh(fragmented)[-1] / total - 1 / count) < 1e-14)
        populations.append(dict(modes=count, total_number=total, coherent_fraction=1., fragmented_fraction=1 / count,
            exact_gradient_energy_matched=False, same_leading_rest_mass_density=True))
    coherent_mean = np.zeros(8, dtype=complex)
    coherent_mean[0] = np.sqrt(1000.)
    check('connected vacuum covariance alone misses coherent condensate', np.trace(np.outer(coherent_mean.conj(), coherent_mean)).real > 999 and np.max(abs(vacuum)) < 1e-14)

    inherited = read_json(PARENT / 'results/matching/status.json')
    mass_ratio = inherited['mass_over_H0']
    lifetimes = []
    for overlap_value in [1e-6, .01, .5]:
        rate_factor = overlap_value * (1 - overlap_value)**3 * mass_ratio / (3072 * math.pi**3)
        upper_quartic = 1 / math.sqrt(rate_factor)
        lifetimes.append(dict(motion_overlap=overlap_value, NOT_heavy_matter_fraction=inherited['heavy_dust_fraction'],
            width3_over_H0_per_U4_squared=rate_factor, U4_upper_for_width3_less_H0=upper_quartic,
            r_squared_times_U4_upper=overlap_value**2 * upper_quartic,
            status='Conditional pure-potential single-vertex vacuum-decay diagnostic; not a sourced U4 or total rate.', valid_for_observational_claim=False))
    check('lifetime coupling eliminated algebraically', abs(lifetimes[1]['width3_over_H0_per_U4_squared'] * lifetimes[1]['U4_upper_for_width3_less_H0']**2 - 1) < 1e-14)
    check('Stage51 parameters remain illustrative and unchanged', inherited['heavy_dust_fraction'] == .5 and not inherited['observations_fitted'])

    applicability = [
        dict(clause='Hamiltonian', paper='Specified hard-sphere repulsion in a static three-dimensional box', current='Gaussian fixed-metric normal modes have zero short-range contact; gravity is attractive and long range', automatic_transfer=False),
        dict(clause='state', paper='Ground state or specified canonical Gibbs ensemble', current='Classical homogeneous preparation and linear perturbation basis, not a specified many-body Gibbs state', automatic_transfer=False),
        dict(clause='number', paper='Fixed boson number for canonical theorem', current='Real-field particle number is an approximate slow-mode quantity; nonlinear cross-decays can be open', automatic_transfer=False),
        dict(clause='fraction', paper='Largest one-particle occupation divided by total particle number', current='F is heavy matter energy share; r is motion eigenvector overlap; neither equals f0', automatic_transfer=False),
        dict(clause='formal coverage', paper='Linked Lean scope covers ground-state hard-sphere result only', current='Positive-temperature manuscript not independently verified here', automatic_transfer=False),
    ]
    check('no theorem imported by relabeling', all(not row['automatic_transfer'] for row in applicability))
    check('all numerical rates remain diagnostics', all(not row['valid_for_observational_claim'] for row in lifetimes))
    passed = all(row['passed'] for row in checks)
    save('derivation', __file__, dict(checks=checks, count=len(checks), all_checks_passed=passed, exact_identities=identities,
        equations=equations, independent_oscillator_checks=oscillators, covariance_reconstruction_error=error,
        coherence_examples=populations, conditional_lifetime_rows=lifetimes, theorem_applicability=applicability,
        contact_numeric_parent_value_supplied=False, thermodynamic_BEC_proved=False,
        existing_coherent_wave_route_rejected=False, observations_changed=False, elapsed_seconds=time.monotonic() - started),
        [ROOT / 'results/sources/status.json'])
    print(dict(state='complete' if passed else 'failed', checks=len(checks), exact_identities=len(identities),
        failed=[row for row in checks if not row['passed']], elapsed_seconds=time.monotonic() - started), flush=True)
    assert passed


if __name__ == '__main__':
    main()
