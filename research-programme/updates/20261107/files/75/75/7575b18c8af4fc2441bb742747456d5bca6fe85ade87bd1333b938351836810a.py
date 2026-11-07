from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import mpmath as mp
import psutil
import sympy as sym


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "results" / "off-shell-kernel"


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Refusing to overwrite executed evidence.")
    OUTPUT.mkdir(parents=True)
    exact = []
    numerator_variable, root_high, root_low, chemical, frequency, mass_squared = sym.symbols(
        "numerator_variable root_high root_low chemical frequency mass_squared"
    )

    def numerator(value):
        return sym.Matrix([[value, 2 * sym.I * chemical * frequency],
                           [-2 * sym.I * chemical * frequency, value - mass_squared]])

    reconstruction = (numerator(root_high) / (numerator_variable - root_high)
                      - numerator(root_low) / (numerator_variable - root_low)) / (root_high - root_low)
    target = numerator(numerator_variable) / ((numerator_variable - root_high) * (numerator_variable - root_low))
    for row in range(2):
        for column in range(2):
            residual = sym.simplify(reconstruction[row, column] - target[row, column])
            assert residual == 0
            exact.append({"name": f"matrix_partial_fraction_{row}_{column}", "passed": True})
    angle, argument = sym.symbols("angle argument")
    legendre = lambda value: (3 * value**2 - 1) / 2
    division = sym.simplify(legendre(angle) - legendre(argument) - sym.Rational(3, 2) * (angle - argument) * (angle + argument))
    assert division == 0
    exact.append({"name": "Q2_polynomial_division", "passed": True})
    reciprocal = numerator(numerator_variable).T - numerator(numerator_variable).subs(frequency, -frequency)
    for row in range(2):
        for column in range(2):
            assert sym.simplify(reciprocal[row, column]) == 0
            exact.append({"name": f"directed_frequency_transpose_{row}_{column}", "passed": True})

    mp.mp.dps = 100
    chemical_value = mp.mpf(1)
    mass_value = mp.mpf(10) / 9

    def Q2(value):
        return (3 * value**2 - 1) * mp.log((value + 1) / (value - 1)) / 4 - 3 * value / 2

    def projected_entry(first, second, imaginary_transfer, row, column):
        transfer = 1j * imaginary_transfer
        offset = transfer**2 - first**2 - second**2
        angular_scale = 2 * first * second

        def numerator_entry(root):
            return [[root, 2j * chemical_value * transfer],
                    [-2j * chemical_value * transfer, root - mass_value]][row][column]

        discriminant = mass_value**2 + 16 * chemical_value**2 * transfer**2
        radical = mp.sqrt(discriminant)
        if abs(discriminant) < mp.mpf("1e-90"):
            repeated_root = mass_value / 2
            function = lambda root: numerator_entry(root) * Q2((root - offset) / angular_scale)
            return -mp.diff(function, repeated_root) / angular_scale
        high = (mass_value + radical) / 2
        low = (mass_value - radical) / 2
        return -(numerator_entry(high) * Q2((high - offset) / angular_scale)
                 - numerator_entry(low) * Q2((low - offset) / angular_scale)) / (angular_scale * (high - low))

    samples = [
        (mp.mpf("0.3"), mp.mpf("0.8"), mp.mpf(0)),
        (mp.mpf("0.3"), mp.mpf("0.8"), mp.mpf("0.05")),
        (mp.mpf("0.7"), mp.mpf("0.7"), mp.mpf("0.2")),
        (mp.mpf("0.3"), mp.mpf("0.8"), mass_value / 4),
        (mp.mpf("0.3"), mp.mpf("0.8"), mp.mpf("0.5")),
        (mp.mpf("1.2"), mp.mpf("2.1"), mp.mpf(1)),
        (mp.mpf("0.04"), mp.mpf("0.08"), mp.mpf("0.03")),
    ]
    rows = []
    for first, second, imaginary_transfer in samples:
        transfer = 1j * imaginary_transfer
        for row in range(2):
            for column in range(2):
                def integrand(angle):
                    spatial_squared = first**2 + second**2 - 2 * first * second * angle
                    value = transfer**2 - spatial_squared
                    determinant = value * (value - mass_value) - 4 * chemical_value**2 * transfer**2
                    entry = [[value, 2j * chemical_value * transfer],
                             [-2j * chemical_value * transfer, value - mass_value]][row][column]
                    return (3 * angle**2 - 1) * entry / (4 * determinant)

                direct = mp.quad(integrand, [-1, -mp.mpf("0.5"), 0, mp.mpf("0.5"), 1])
                analytic = projected_entry(first, second, imaginary_transfer, row, column)
                error = abs(direct - analytic)
                budget = mp.mpf("1e-60") + mp.mpf("1e-50") * max(abs(direct), abs(analytic))
                assert error <= budget, (first, second, imaginary_transfer, row, column, error)
                rows.append({"first_momentum": str(first), "second_momentum": str(second),
                             "imaginary_transfer": str(imaginary_transfer), "row": row, "column": column,
                             "analytic": str(analytic), "independent_angular_integral": str(direct),
                             "absolute_error": str(error), "budget": str(budget), "passed": True})
    static_first, static_second = mp.mpf("0.3"), mp.mpf("0.8")
    static_scale = 2 * static_first * static_second
    static = []
    for index, internal_mass in enumerate([mass_value, mp.mpf(0)]):
        actual = projected_entry(static_first, static_second, mp.mpf(0), index, index)
        expected = -Q2((static_first**2 + static_second**2 + internal_mass) / static_scale) / static_scale
        assert abs(actual - expected) < mp.mpf("1e-80")
        static.append({"mode": "radial" if index == 0 else "phase", "passed": True, "value": str(actual)})
    report = {
        "state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
        "exact_checks": exact, "angular_checks": rows, "static_limit_checks": static,
        "counts": {"exact": len(exact), "high_precision_angular": len(rows), "static_limits": len(static)},
        "algebra_source_sha256": hashlib.sha256((ROOT / "results/algebra/status.json").read_bytes()).hexdigest(),
        "full_matrix_off_shell_l2_exchange_derived": True,
        "repeated_root_limit_tested": True,
        "imaginary_frequency_checks_are_not_a_pole_search": True,
        "static_phase_kernel_log_singularity_retained": True,
        "full_resummed_interacting_pole_test_performed": False,
        "scope": "Exact angular projection of the quadratic exchange propagator, usable with the action-derived cubic tensors in the tree l=2 two-body kernel; not a complete renormalized kernel."
    }
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", **report["counts"]}))


if __name__ == "__main__":
    main()
