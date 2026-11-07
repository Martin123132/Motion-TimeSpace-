from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import psutil
import sympy as sym


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'results' / 'repair-independent-check'


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError('Executed evidence must not be overwritten.')
    OUTPUT.mkdir(parents=True)
    amplitude, coupling, quartic, chemical = sym.symbols('amplitude coupling quartic chemical', positive=True)
    epsilon, radial, phase, radial_rate, phase_rate, radial_gradient, phase_gradient = sym.symbols('epsilon radial phase radial_rate phase_rate radial_gradient phase_gradient', real=True)
    checks = []

    def verify(name, actual, expected=0):
        difference = sym.simplify(actual - expected)
        checks.append({'name': name, 'passed': difference == 0, 'difference': str(difference)})
        assert difference == 0, (name, difference)

    potential = 3 * coupling * amplitude**sym.Rational(4, 3) / 4 + quartic * amplitude**4 / 4
    frequency_squared = sym.diff(potential, amplitude) / amplitude
    stiffness = sym.diff(potential, amplitude, 2) - frequency_squared
    modulus_squared = (amplitude + epsilon * radial)**2 + epsilon**2 * phase**2
    potential_cartesian = 3 * coupling * modulus_squared**sym.Rational(2, 3) / 4 + quartic * modulus_squared**2 / 4
    cartesian_lagrangian = ((epsilon * radial_rate - chemical * epsilon * phase)**2
        + (epsilon * phase_rate + chemical * (amplitude + epsilon * radial))**2
        - epsilon**2 * (radial_gradient**2 + phase_gradient**2)) / 2 - potential_cartesian
    cartesian_quadratic = sym.diff(cartesian_lagrangian, epsilon, 2).subs(epsilon, 0) / 2
    expected_cartesian = ((radial_rate**2 + phase_rate**2 - radial_gradient**2 - phase_gradient**2) / 2
        - stiffness * radial**2 / 2 + chemical * (radial * phase_rate - phase * radial_rate))
    verify('independent_cartesian_quadratic', sym.expand(cartesian_quadratic - expected_cartesian).subs(chemical**2, frequency_squared))
    polar_quadratic = ((radial_rate**2 + phase_rate**2 - radial_gradient**2 - phase_gradient**2) / 2
        - stiffness * radial**2 / 2 + 2 * chemical * radial * phase_rate)
    verify('polar_cartesian_difference_is_total_derivative', polar_quadratic - expected_cartesian, chemical * (radial * phase_rate + phase * radial_rate))
    verify('amplitude_elimination_d_rho_d_X', (sym.diff(potential, amplitude, 2) - frequency_squared) * (2 * amplitude / stiffness), 2 * amplitude)
    verify('general_phase_P_XX', 2 * amplitude * (2 * amplitude / stiffness), 4 * amplitude**2 / stiffness)
    charge_density = sym.symbols('charge_density', real=True)
    fixed_charge_energy = charge_density**2 / (2 * amplitude**2) + potential
    verify('fixed_charge_amplitude_gap', sym.diff(fixed_charge_energy, amplitude, 2).subs(charge_density**2, frequency_squared * amplitude**4), stiffness + 4 * frequency_squared)
    compressibility = amplitude**2 + 2 * chemical * amplitude * (2 * chemical * amplitude / stiffness)
    verify('thermodynamic_compressibility', compressibility, amplitude**2 * (stiffness + 4 * chemical**2) / stiffness)

    samples = []
    repair_ratios = [sym.Rational(0), sym.Rational(1, 6), sym.Rational(1, 3), sym.Rational(1, 2), sym.Integer(1), sym.Integer(2), sym.Integer(10)]
    for ratio in repair_ratios:
        substitutions = {amplitude: 1, coupling: 1, quartic: ratio}
        frequency_value = sym.simplify(frequency_squared.subs(substitutions))
        stiffness_value = sym.simplify(stiffness.subs(substitutions))
        gap_value = stiffness_value + 4 * frequency_value
        speed = sym.factor(stiffness_value / gap_value)
        grand_potential = sym.simplify((potential - frequency_squared * amplitude**2 / 2).subs(substitutions))
        verify(f'ratio_{ratio}_sound', speed, (3 * ratio - 1) / (5 + 9 * ratio))
        verify(f'ratio_{ratio}_grand_potential', grand_potential, (1 - ratio) / 4)
        for momentum in [sym.Rational(1, 100000), sym.Rational(1, 100), sym.Rational(1, 10), sym.Integer(1), sym.Integer(10)]:
            lower = momentum**2 + gap_value / 2 - sym.sqrt(gap_value**2 / 4 + 4 * frequency_value * momentum**2)
            upper = momentum**2 + gap_value / 2 + sym.sqrt(gap_value**2 / 4 + 4 * frequency_value * momentum**2)
            verify(f'ratio_{ratio}_momentum_{momentum}_product', lower * upper, momentum**2 * (momentum**2 + stiffness_value))
            lower_number = lower.evalf(80)
            expected_unstable = momentum**2 + stiffness_value < 0
            assert bool(lower_number < 0) == bool(expected_unstable)
            assert upper.evalf(80) > 0
            samples.append({'ratio': str(ratio), 'momentum': str(momentum), 'sound_squared': str(speed), 'omega_lower_squared': str(lower_number), 'expected_instability_detected': bool(expected_unstable), 'locally_stable': bool(stiffness_value > 0), 'marginal': bool(stiffness_value == 0), 'preferred_to_empty_state_at_same_mu': bool(grand_potential < 0), 'grand_potential': str(grand_potential)})
    report = {'state': 'complete', 'created_at': datetime.now(timezone.utc).isoformat(), 'checks': checks, 'exact_identity_checks': len(checks), 'spectrum_samples': samples, 'sample_count': len(samples), 'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), 'first_run_sha256': hashlib.sha256((ROOT / 'results/first-candidate/status.json').read_bytes()).hexdigest(), 'scope': 'Independent rotating-Cartesian check of new complex extension, not a stability test of the original real-scalar MTS.', 'full_nonlinear_or_cosmological_stability_proven': False}
    (OUTPUT / 'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'exact_checks': len(checks), 'samples': len(samples), 'unstable_cases_preserved': sum(row['expected_instability_detected'] for row in samples)}))


if __name__ == '__main__':
    main()
