from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import traceback

import mpmath as mp
import numpy as np
import psutil
import sympy as sym

from operator_core import Candidate, q2, q2_derivative, rectangle_log_integral, BASIS, TRANSPOSE_PARITY


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "results" / "normalization"


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite evidence.")
    OUTPUT.mkdir(parents=True)
    exact = []
    numerical = []

    def exact_check(name, value):
        assert sym.simplify(value) == 0, (name, value)
        exact.append({"name": name, "passed": True})

    def check(name, actual, expected, tolerance=mp.mpf("1e-45")):
        error = abs(actual - expected)
        budget = tolerance * (1 + abs(expected))
        assert error < budget, (name, actual, expected, error, budget)
        numerical.append({"name": name, "actual": str(actual), "expected": str(expected),
                          "absolute_error": str(error), "budget": str(budget), "passed": True})

    angle = sym.symbols("angle", real=True)
    exact_check("Funk_Hecke_angular_measure", 2 * sym.pi * sym.integrate(((3 * angle**2 - 1) / 2)**2, (angle, -1, 1)) - 4 * sym.pi / 5)
    exact_check("four_dimensional_measure_after_projection", 4 * sym.pi / (2 * sym.pi)**4 - 1 / (4 * sym.pi**3))
    first, second, constant = sym.symbols("first second constant", positive=True)
    rectangle_quarter = first * second * sym.log(constant / (first**2 + second**2)) + 3 * first * second - first**2 * sym.atan(second / first) - second**2 * sym.atan(first / second)
    exact_check("rectangle_log_mixed_derivative", sym.diff(rectangle_quarter, first, second) - sym.log(constant / (first**2 + second**2)))
    exact_check("rectangle_zero_width", sym.limit(rectangle_quarter, first, 0))
    cubic = np.zeros((2, 2, 2), dtype=object)
    for indices in np.ndindex(2, 2, 2):
        cubic[indices] = sym.Rational(5, 3) if sum(indices) == 0 else sym.Rational(2, 7) if sum(indices) == 2 else sym.Rational(0)
    propagators = [sym.Matrix([[2, 0], [0, 3]]), sym.Matrix([[3, 1], [-1, 4]]), sym.Matrix([[3, -1], [1, 4]])]
    sources = [sym.Matrix([[2, 1], [1, 1]]), sym.Matrix([[1, 3], [2, 4]]), sym.Matrix([[1, 2], [3, 4]])]
    varied = [propagators[index] * sources[index] * propagators[index] for index in range(3)]
    for external in range(3):
        for left in range(2):
            for right in range(2):
                two_terms = sym.Rational(0)
                single_term = sym.Rational(0)
                for internal in range(3):
                    remainder = (external - internal) % 3
                    for first_index, second_index, third_index, fourth_index in np.ndindex(2, 2, 2, 2):
                        coefficient = cubic[left, first_index, second_index] * cubic[right, third_index, fourth_index]
                        leading = varied[internal][first_index, third_index] * propagators[remainder][second_index, fourth_index]
                        other = propagators[internal][first_index, third_index] * varied[remainder][second_index, fourth_index]
                        two_terms += coefficient * (leading + other) / 2
                        single_term += coefficient * leading
                exact_check(f"two_exchange_terms_cancel_identical_half_{external}_{left}_{right}", two_terms - single_term)

    mp.mp.dps = 70
    mass = mp.mpf(10) / 9
    chemical = mp.mpf(1)
    gap = mass + 4
    sound = mp.sqrt(mass / gap)

    def euclidean(frequency, momentum):
        squared = frequency**2 + momentum**2
        determinant = squared * (squared + mass) + 4 * frequency**2
        return mp.matrix([[squared, 2 * frequency], [-2 * frequency, squared + mass]]) / determinant

    def residues(momentum):
        radical = mp.sqrt(gap**2 / 4 + 4 * momentum**2)
        high_squared = momentum**2 + gap / 2 + radical
        low_squared = momentum**2 * (momentum**2 + mass) / high_squared
        result = []
        for squared, other in [(low_squared, high_squared), (high_squared, low_squared)]:
            energy = mp.sqrt(squared)
            numerator = mp.matrix([[squared - momentum**2, 2j * energy],
                                   [-2j * energy, squared - momentum**2 - mass]])
            result.append((energy, numerator / (2 * energy * (squared - other))))
        return result

    for momentum in [mp.mpf("0.3"), mp.mpf(2)]:
        spectral = residues(momentum)
        for frequency in [mp.mpf("0.1"), mp.mpf(1), mp.mpf(3)]:
            reconstructed = mp.zeros(2)
            for energy, residue in spectral:
                reconstructed += residue / (energy - 1j * frequency) + residue.T / (energy + 1j * frequency)
            for row, column in np.ndindex(2, 2):
                check(f"Euclidean_spectral_contour_{momentum}_{frequency}_{row}_{column}", reconstructed[row, column], euclidean(frequency, momentum)[row, column])
        for basis_index in range(4):
            source = mp.matrix([[0, 0], [0, 0]])
            source[basis_index // 2, basis_index % 2] = 1
            analytic = mp.zeros(2)
            for first_energy, first_residue in spectral:
                for second_energy, second_residue in spectral:
                    analytic += (first_residue * source * second_residue.T + first_residue.T * source * second_residue) / (first_energy + second_energy)
            for row, column in np.ndindex(2, 2):
                def integrand(frequency):
                    positive = euclidean(frequency, momentum)
                    negative = euclidean(-frequency, momentum)
                    return ((positive * source * positive)[row, column] + (negative * source * negative)[row, column]) / (2 * mp.pi)
                direct = mp.quad(integrand, [0, momentum, 1, 4, mp.inf])
                check(f"exact_frequency_integral_{momentum}_{basis_index}_{row}_{column}", direct, analytic[row, column])

    Q2 = lambda value: (3 * value**2 - 1) * mp.log((value + 1) / (value - 1)) / 4 - 3 * value / 2
    for value in [mp.mpf("1.0001"), mp.mpf(2), mp.mpf("3.0001"), mp.mpf(10), mp.mpf("1000000"), mp.mpc(1, 2), mp.mpc(3, 5)]:
        check(f"binary64_Q2_{value}", complex(q2(np.array([complex(value)]))[0]), Q2(value), mp.mpf("1e-11"))
        check(f"binary64_Q2_derivative_{value}", complex(q2_derivative(np.array([complex(value)]))[0]), mp.diff(Q2, value), mp.mpf("1e-10"))

    model = Candidate()
    for frequency, first_momentum, second_momentum in [
        (mp.mpf(0), mp.mpf("0.3"), mp.mpf("0.8")),
        (mass / 4, mp.mpf("0.3"), mp.mpf("0.8")),
        (mp.mpf("0.2"), mp.mpf("0.7"), mp.mpf("0.7")),
        (mp.mpf("0.5"), mp.mpf("0.3"), mp.mpf("0.8")),
        (mp.mpf(8), mp.mpf("0.01"), mp.mpf("0.03")),
    ]:
        actual = model.exchange_l2(np.array([float(frequency)]), np.array([float(first_momentum)]), np.array([float(second_momentum)]))[0]
        for row, column in np.ndindex(2, 2):
            def integrand(angle):
                internal = mp.sqrt(first_momentum**2 + second_momentum**2 - 2 * first_momentum * second_momentum * angle)
                return (3 * angle**2 - 1) * euclidean(frequency, internal)[row, column] / 4
            expected = mp.quad(integrand, [-1, 0, 1])
            check(f"binary64_angular_projection_{frequency}_{first_momentum}_{second_momentum}_{row}_{column}", actual[row, column], expected, mp.mpf("2e-10"))

    for radial_half, frequency_half, momentum in [(mp.mpf("0.1"), mp.mpf("0.2"), mp.mpf(1)),
                                                  (mp.mpf("0.01"), mp.mpf("0.5"), mp.mpf("0.02")),
                                                  (mp.mpf("0.3"), mp.mpf("0.02"), mp.mpf(2))]:
        scaled_half = frequency_half / sound
        function = lambda radial: scaled_half * mp.log(4 * momentum**2 / (radial**2 + scaled_half**2)) + 2 * scaled_half - 2 * radial * mp.atan(scaled_half / radial)
        direct = 4 * sound * mp.quad(function, [0, radial_half])
        analytic = 4 * sound * (radial_half * scaled_half * mp.log(4 * momentum**2 / (radial_half**2 + scaled_half**2)) + 3 * radial_half * scaled_half - radial_half**2 * mp.atan(scaled_half / radial_half) - scaled_half**2 * mp.atan(radial_half / scaled_half))
        check(f"exact_log_rectangle_{radial_half}_{frequency_half}", direct, analytic)
        check(f"binary64_log_rectangle_{radial_half}_{frequency_half}", rectangle_log_integral(float(radial_half), float(frequency_half), float(sound), float(momentum)), analytic, mp.mpf("1e-12"))

    for index in range(4):
        check(f"Bose_transpose_basis_{index}", float(np.max(np.abs(BASIS[index].T - TRANSPOSE_PARITY[index] * BASIS[index]))), 0)
    for first_index, second_index in np.ndindex(4, 4):
        check(f"pair_basis_normalization_{first_index}_{second_index}", float(np.sum(BASIS[first_index] * BASIS[second_index])), 1 if first_index == second_index else 0, mp.mpf("1e-14"))
    report = {"state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
              "exact_checks": exact, "numerical_checks": numerical,
              "counts": {"exact": len(exact), "numerical": len(numerical)},
              "core_sha256": hashlib.sha256((ROOT / "operator_core.py").read_bytes()).hexdigest(),
              "scope": "Zero-total-frequency normalization, full relative-frequency contour identity, Euclidean exchange and analytic product integration; not a finite-frequency pole search."}
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", **report["counts"]}))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        if OUTPUT.exists():
            (OUTPUT / "FAILED.json").write_text(json.dumps({"error": repr(error), "traceback": traceback.format_exc()}, indent=2), encoding="utf-8")
        raise
