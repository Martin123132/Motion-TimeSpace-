from __future__ import annotations

from datetime import datetime, timezone
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path
import traceback

import mpmath as mp
import numpy as np
import psutil
from scipy.optimize import brentq, minimize_scalar


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / 'results' / 'full-spectrum-v2'


class TwoMode:
    def __init__(self, chemical, radial_mass_squared):
        self.chemical = float(chemical)
        self.mass_squared = float(radial_mass_squared)
        self.gap_squared = self.mass_squared + 4 * self.chemical**2
        self.gap = math.sqrt(self.gap_squared)
        self.sound_squared = self.mass_squared / self.gap_squared

    def energy(self, momentum, branch):
        squared = momentum * momentum
        radical = math.sqrt(self.gap_squared**2 / 4 + 4 * self.chemical**2 * squared)
        upper_squared = squared + self.gap_squared / 2 + radical
        value = upper_squared if branch else squared * (squared + self.mass_squared) / upper_squared
        return math.sqrt(value)

    def inverse_energy(self, energy, branch):
        if energy <= (self.gap if branch else 0):
            return 0.0
        squared = energy**2
        radical = math.sqrt(self.mass_squared**2 / 4 + 4 * self.chemical**2 * squared)
        lower_squared = squared * (1 + 4 * self.chemical**2 / (radical + self.mass_squared / 2))
        result = squared * (squared - self.gap_squared) / lower_squared if branch else lower_squared
        return math.sqrt(result)

    def velocity(self, momentum, branch):
        if momentum == 0:
            return 0.0 if branch else math.sqrt(self.sound_squared)
        radical = math.sqrt(self.gap_squared**2 / 4 + 4 * self.chemical**2 * momentum**2)
        coefficient = 1 + (1 if branch else -1) * 2 * self.chemical**2 / radical
        return momentum * coefficient / self.energy(momentum, branch)

    def momentum_over_velocity(self, momentum, branch):
        radical = math.sqrt(self.gap_squared**2 / 4 + 4 * self.chemical**2 * momentum**2)
        coefficient = 1 + (1 if branch else -1) * 2 * self.chemical**2 / radical
        return self.energy(momentum, branch) / coefficient

    def residue(self, momentum, branch):
        energy = self.energy(momentum, branch)
        if energy == 0:
            raise ValueError('The massless residue is singular at exactly zero momentum.')
        radical = math.sqrt(self.gap_squared**2 / 4 + 4 * self.chemical**2 * momentum**2)
        separation = 2 * radical
        if branch:
            radial_numerator = self.gap_squared / 2 + radical
            phase_numerator = radial_numerator - self.mass_squared
        else:
            radial_numerator = 4 * self.chemical**2 * momentum**2 / (radical + self.gap_squared / 2)
            phase_numerator = radial_numerator + self.mass_squared
        radial = radial_numerator / (2 * energy * separation)
        phase = phase_numerator / (2 * energy * separation)
        mixing = (1 if branch else -1) * self.chemical / separation
        return radial, phase, mixing

    def weight(self, first_momentum, first_branch, second_momentum, second_branch):
        first = self.residue(first_momentum, first_branch)
        second = self.residue(second_momentum, second_branch)
        sign_product = (1 if first_branch else -1) * (1 if second_branch else -1)
        return (math.sqrt(first[0] * second[0]) - sign_product * math.sqrt(first[1] * second[1]))**2

    def threshold(self, momentum, first_branch, second_branch):
        if momentum == 0:
            return (first_branch + second_branch) * self.gap
        function = lambda value: self.energy(value, first_branch) + self.energy(momentum - value, second_branch)
        candidate = minimize_scalar(function, bounds=(0, momentum), method='bounded', options={'xatol': 1e-13})
        return min(function(0), function(momentum), function(float(candidate.x)))

    def zero_momentum_channel(self, frequency, first_branch, second_branch):
        threshold = self.threshold(0, first_branch, second_branch)
        if frequency <= threshold:
            return 0.0
        function = lambda value: self.energy(value, first_branch) + self.energy(value, second_branch) - frequency
        upper = max(self.inverse_energy(frequency, first_branch), self.inverse_energy(frequency, second_branch))
        root = brentq(function, 0, upper, xtol=1e-15, rtol=2e-14)
        weight = self.weight(root, first_branch, root, second_branch)
        derivative = self.velocity(root, first_branch) + self.velocity(root, second_branch)
        return 2 * root**6 * weight / (15 * math.pi * derivative)

    def intervals(self, frequency, momentum, first_branch, second_branch, grid_count):
        if frequency <= self.threshold(momentum, first_branch, second_branch):
            return []
        maximum = self.inverse_energy(frequency - (self.gap if second_branch else 0), first_branch)
        if maximum == 0:
            return []
        lower_test = lambda value: self.energy(value, first_branch) + self.energy(abs(momentum - value), second_branch) - frequency
        upper_test = lambda value: self.energy(value, first_branch) + self.energy(momentum + value, second_branch) - frequency
        nodes = maximum * np.sin(np.linspace(0, math.pi / 2, grid_count))**2
        if 0 < momentum < maximum:
            nodes = np.unique(np.append(nodes, momentum))
        endpoints = [0.0, maximum]
        for function in [lower_test, upper_test]:
            values = [function(float(value)) for value in nodes]
            for index in range(len(nodes) - 1):
                left, right = float(nodes[index]), float(nodes[index + 1])
                if values[index] == 0:
                    endpoints.append(left)
                if values[index] * values[index + 1] < 0:
                    endpoints.append(brentq(function, left, right, xtol=1e-15, rtol=2e-14))
        endpoints = sorted(set(endpoints))
        return [(left, right) for left, right in zip(endpoints[:-1], endpoints[1:]) if lower_test((left + right) / 2) <= 0 and upper_test((left + right) / 2) >= 0]

    def channel(self, frequency, momentum, first_branch, second_branch, order=192, grid_count=513):
        if momentum == 0:
            return self.zero_momentum_channel(frequency, first_branch, second_branch)
        intervals = self.intervals(frequency, momentum, first_branch, second_branch, grid_count)
        nodes, weights = gauss_rule(order)
        total = 0.0
        for left, right in intervals:
            midpoint = (left + right) / 2
            half_width = (right - left) / 2
            terms = []
            for node, weight in zip(nodes, weights):
                first_momentum = midpoint + half_width * float(node)
                available = frequency - self.energy(first_momentum, first_branch)
                second_momentum = self.inverse_energy(available, second_branch)
                if second_momentum == 0 or first_momentum == 0:
                    terms.append(0.0)
                    continue
                angle = (first_momentum**2 + momentum**2 - second_momentum**2) / (2 * first_momentum * momentum)
                if abs(angle) > 1 + 1e-9:
                    raise AssertionError(('angular support escaped', angle))
                angular_factor = max(0.0, 1 - angle**2)**2
                pair_weight = self.weight(first_momentum, first_branch, second_momentum, second_branch)
                integrand = first_momentum**5 * self.momentum_over_velocity(second_momentum, second_branch) * angular_factor * pair_weight
                terms.append(float(weight) * integrand)
            total += half_width * math.fsum(terms)
        return total / (8 * math.pi * momentum)

    def spectrum(self, frequency, momentum, order=192, grid_count=513):
        return {(first, second): self.channel(frequency, momentum, first, second, order, grid_count) for first in range(2) for second in range(2)}


@lru_cache(maxsize=8)
def gauss_rule(order):
    return np.polynomial.legendre.leggauss(order)


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError('Refusing to overwrite executed evidence.')
    OUTPUT.mkdir(parents=True)
    checks = []

    def close(name, actual, expected, relative=1e-7, absolute=1e-25):
        error = abs(actual - expected)
        tolerance = absolute + relative * max(abs(expected), abs(actual))
        checks.append({'name': name, 'passed': error <= tolerance, 'actual': actual, 'expected': expected, 'error': error, 'tolerance': tolerance})
        if error > tolerance:
            raise AssertionError((name, actual, expected, error, tolerance))

    model = TwoMode(1, 10 / 9)
    for momentum in [1e-5, 0.03, 0.3, 1.0, 10.0, 100.0]:
        residues = []
        for branch in range(2):
            energy = model.energy(momentum, branch)
            conditioning_budget = 8 * np.finfo(float).eps * energy / model.velocity(momentum, branch)
            close(f'inverse_energy_{momentum}_{branch}', model.inverse_energy(energy, branch), momentum, relative=2e-8, absolute=conditioning_budget)
            mp.mp.dps = 70
            precise_momentum = mp.mpf(str(momentum))
            precise_mass = mp.mpf(model.mass_squared)
            precise_gap = precise_mass + 4
            precise_radical = mp.sqrt(precise_gap**2 / 4 + 4 * precise_momentum**2)
            precise_high = precise_momentum**2 + precise_gap / 2 + precise_radical
            precise_energy_squared = precise_high if branch else precise_momentum**2 * (precise_momentum**2 + precise_mass) / precise_high
            precise_inverse_radical = mp.sqrt(precise_mass**2 / 4 + 4 * precise_energy_squared)
            precise_low_inverse = precise_energy_squared * (1 + 4 / (precise_inverse_radical + precise_mass / 2))
            precise_inverse_squared = precise_energy_squared * (precise_energy_squared - precise_gap) / precise_low_inverse if branch else precise_low_inverse
            assert abs(mp.sqrt(precise_inverse_squared) / precise_momentum - 1) < mp.mpf('1e-50')
            radial, phase, mixing = model.residue(momentum, branch)
            assert radial >= 0 and phase >= 0
            close(f'residue_rank_{momentum}_{branch}', radial * phase, mixing**2, relative=2e-8)
            residues.append(np.array([[radial, 1j * mixing], [-1j * mixing, phase]]))
        commutator = residues[0] - residues[0].T + residues[1] - residues[1].T
        close(f'field_commutator_{momentum}', float(np.max(np.abs(commutator))), 0.0, absolute=1e-13)
        moment = sum(model.energy(momentum, branch) * (residues[branch] + residues[branch].T) for branch in range(2))
        close(f'momentum_commutator_{momentum}', float(np.max(np.abs(moment - np.eye(2)))), 0.0, absolute=3e-13)
        for first in range(2):
            for second in range(2):
                stable_weight = model.weight(momentum, first, momentum, second)
                direct_weight = float(np.trace(residues[first] @ residues[second].T).real)
                close(f'positive_pair_weight_{momentum}_{first}_{second}', stable_weight, direct_weight, relative=2e-7, absolute=2e-11)

    comparator = TwoMode(0, 1)
    free_rows = []
    for frequency, momentum in [(0.7, 0.1), (0.7, 1.0), (2.8, 0.5), (5.0, 1.0)]:
        channels = comparator.spectrum(frequency, momentum, order=192)
        invariant = frequency**2 - momentum**2
        expected = 0.0 if invariant <= 0 else invariant**2 / (960 * math.pi)
        if invariant > 4:
            expected += invariant**2 * (1 - 4 / invariant)**2.5 / (960 * math.pi)
        actual = math.fsum(channels.values())
        close(f'independent_free_scalar_spectrum_{frequency}_{momentum}', actual, expected, relative=2e-7)
        free_rows.append({'frequency': frequency, 'momentum': momentum, 'computed': actual, 'analytic_two_scalar': expected})

    infrared_rows = []
    for frequency, momentum in [(1e-4, 0), (2e-4, 1e-4), (4e-4, 5e-4)]:
        channels = model.spectrum(frequency, momentum, order=192)
        expected = (frequency**2 - model.sound_squared * momentum**2)**2 / (960 * math.pi * model.sound_squared**1.5)
        actual = math.fsum(channels.values())
        close(f'phonon_limit_{frequency}_{momentum}', actual, expected, relative=2e-6, absolute=1e-30)
        infrared_rows.append({'frequency': frequency, 'momentum': momentum, 'full_response': actual, 'phonon_EFT': expected, 'ratio': actual / expected})
    ultraviolet = math.fsum(model.spectrum(200, 0).values())
    ultraviolet_expected = 200**4 / (480 * math.pi)
    close('ultraviolet_two_scalar_normalization', ultraviolet, ultraviolet_expected, relative=3e-3)
    print(json.dumps({'stage': 'normalization_checks_complete', 'checks': len(checks)}), flush=True)

    spectrum_rows = []
    for momentum in [0.0, 0.25, 1.0]:
        for frequency in [0.2, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0]:
            coarse = model.spectrum(frequency, momentum, order=96, grid_count=257)
            fine = model.spectrum(frequency, momentum, order=192, grid_count=513)
            extra = model.spectrum(frequency, momentum, order=384, grid_count=1025)
            for key in fine:
                close(f'quadrature_{frequency}_{momentum}_{key}', fine[key], extra[key], relative=2e-6, absolute=1e-22)
            close(f'exchange_symmetry_{frequency}_{momentum}', extra[(0, 1)], extra[(1, 0)], relative=2e-6, absolute=1e-22)
            spectrum_rows.append({'frequency': frequency, 'momentum': momentum, 'channels': {str(key): value for key, value in extra.items()}, 'total': math.fsum(extra.values()), 'coarse_total': math.fsum(coarse.values()), 'fine_total': math.fsum(fine.values()), 'refinement_difference': abs(math.fsum(extra.values()) - math.fsum(fine.values())), 'thresholds': {str(key): model.threshold(momentum, *key) for key in extra}})
        print(json.dumps({'stage': 'full_two_mode_spectra', 'momentum': momentum, 'rows': len(spectrum_rows)}), flush=True)

    mp.mp.dps = 70
    partial_rows = []
    ratio = mp.mpf(2)
    amplitude = mp.mpf(10)
    chemical = mp.mpf(1)
    alpha = chemical**2 / (amplitude**2 * (1 + ratio))
    cubic_radial = amplitude * alpha * (6 * ratio - mp.mpf(2) / 9)
    cubic_mixed = amplitude * alpha * (2 * ratio - mp.mpf(2) / 3)
    mass_squared = chemical**2 * (2 * ratio - mp.mpf(2) / 3) / (1 + ratio)
    gap_squared = mass_squared + 4 * chemical**2
    for momentum_text in ['0.0001', '0.001', '0.03', '0.2', '1', '5', '20']:
        momentum = mp.mpf(momentum_text)
        radical = mp.sqrt(gap_squared**2 / 4 + 4 * chemical**2 * momentum**2)
        radial_weight = 4 * chemical**2 * momentum**2 / ((radical + gap_squared / 2) * 2 * radical)
        phase_weight = radial_weight + mass_squared / (2 * radical)
        current = cubic_radial * radial_weight + cubic_mixed * phase_weight
        argument = 1 + mass_squared / (2 * momentum**2)
        Q2 = (3 * argument**2 - 1) * mp.log((argument + 1) / (argument - 1)) / 4 - 3 * argument / 2
        analytic = current**2 * Q2 / momentum**2
        integrand = lambda angle: ((3 * angle**2 - 1) / 4) * current**2 * (1 / (mass_squared + 2 * momentum**2 * (1 - angle)) + 1 / (mass_squared + 2 * momentum**2 * (1 + angle)))
        direct = mp.quad(integrand, [-1, -0.5, 0, 0.5, 1])
        relative_error = abs(direct - analytic) / max(abs(direct), abs(analytic))
        assert relative_error < mp.mpf('1e-35'), relative_error
        assert 0 < analytic < 36 * chemical**2 / amplitude**2
        asymptotic_current = cubic_mixed * mass_squared / gap_squared
        asymptotic = 16 * asymptotic_current**2 * momentum**4 / (15 * mass_squared**3)
        partial_rows.append({'momentum': momentum_text, 'radial_source': str(current), 'l2_projection': str(analytic), 'direct_angular_integral': str(direct), 'relative_error': str(relative_error), 'infrared_k4_prediction': str(asymptotic), 'ratio_to_k4': str(analytic / asymptotic)})
    close('l2_low_momentum_k4_limit', float(mp.mpf(partial_rows[0]['ratio_to_k4'])), 1.0, relative=2e-6)

    report = {
        'state': 'complete', 'created_at': datetime.now(timezone.utc).isoformat(), 'checks': checks,
        'checks_passed': len(checks), 'free_scalar_comparators': free_rows,
        'infrared_matches': infrared_rows, 'ultraviolet_ratio': ultraviolet / ultraviolet_expected,
        'full_spectrum_rows': spectrum_rows, 'partial_wave_rows': partial_rows,
        'partial_wave_high_precision_checks': len(partial_rows),
        'parameters': {'mu': 1, 'y': 2, 'varrho0': 10, 'epsilon': 0.01, 'radial_mass_squared': 10 / 9, 'gap_squared': 46 / 9, 'sound_squared': 5 / 23, 'choice': 'dimensionless controlled example, not fitted or parent-predicted'},
        'algebra_sha256': hashlib.sha256((ROOT / 'results/algebra/status.json').read_bytes()).hexdigest(),
        'no_discrete_tensor_mode_in_computed_gaussian_response': True,
        'nonzero_tree_l2_interaction_derived': True,
        'full_resummed_interacting_collective_pole_test_performed': False,
        'quadrature_differences_are_not_interval_error_bounds': True,
        'inverse_energy_validation': 'Relative target retained; binary64 input conditioning allowance 8*eps*E/v added at threshold; all twelve inversions independently replayed at 70 digits to 1e-50 relative. Original failed run retained.',
    }
    (OUTPUT / 'status.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'spectrum_rows': len(spectrum_rows), 'partial_wave_rows': len(partial_rows)}))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        if OUTPUT.exists():
            (OUTPUT / 'FAILED.json').write_text(json.dumps({'state': 'failed', 'error': repr(error), 'traceback': traceback.format_exc()}, indent=2), encoding='utf-8')
        raise
