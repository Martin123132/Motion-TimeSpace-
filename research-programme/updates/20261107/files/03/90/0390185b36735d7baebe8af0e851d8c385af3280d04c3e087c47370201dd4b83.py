from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path

import psutil
import sympy as sym


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "results/derivation"
PREVIOUS = ROOT.parent / "tensor-ward-20261003"


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    if OUTPUT.exists():
        raise RuntimeError("Executed evidence must not be overwritten.")
    OUTPUT.mkdir(parents=True)
    checks = []

    def check(name, expression):
        residual = sym.factor(expression)
        assert residual == 0, (name, residual)
        checks.append({"name": name, "passed": True})

    shifted, mass, mixing = sym.symbols("shifted mass mixing", positive=True)
    diagonal = shifted + mass
    schur = shifted + mixing**2 / diagonal
    lower = sym.Matrix([[1, 0], [mixing / diagonal, 1]])
    upper = sym.Matrix([[1, -mixing / diagonal], [0, 1]])
    propagator_inverse = sym.Matrix([[diagonal, -mixing], [mixing, shifted]])
    propagator = propagator_inverse.inv()
    factor_diagonal = sym.diag(diagonal, schur)
    entries = sym.symbols("response00 response01 response10 response11")
    response = sym.Matrix(2, 2, entries)
    transformed = lower.inv() * response * upper.inv()
    for first in range(2):
        for second in range(2):
            check(f"Schur_factorization_{first}_{second}",
                  (lower * factor_diagonal * upper - propagator_inverse)[first, second])
            check(f"arbitrary_response_sandwich_{first}_{second}",
                  (upper * propagator * response * propagator * lower
                   - factor_diagonal.inv() * transformed * factor_diagonal.inv())[first, second])
    soft_column = sym.Matrix([1, mixing / mass])
    soft_row = sym.Matrix([[1, -mixing / mass]])
    leakage = mixing * shifted / (mass * diagonal)
    expected = sym.Matrix([[1, -leakage], [leakage, -leakage**2]])
    for first in range(2):
        for second in range(2):
            check(f"exact_soft_vertex_in_Schur_basis_{first}_{second}",
                  (lower.inv() * soft_column * soft_row * upper.inv() - expected)[first, second])
    determinant = shifted * diagonal + mixing**2
    bounded_radial = (1 - shifted**2 / determinant) / mass
    bounded_phase = mixing * shifted / (mass * determinant)
    check("full_G_soft_radial_projection", (propagator * soft_column)[0] - bounded_radial)
    check("full_G_soft_phase_projection", (propagator * soft_column)[1] - bounded_phase)
    check("positive_radial_projection_numerator", determinant - shifted**2 - (mass * shifted + mixing**2))
    check("phase_projection_bound_certificate", determinant - 2 * mixing * shifted
          - ((shifted - mixing)**2 + mass * shifted))
    parameter = sym.symbols("parameter", real=True)
    check("rank_two_bubble_log_coefficient", sym.integrate(parameter**2, (parameter, 0, 1)) - sym.Rational(1, 3))

    amplitude, coupling, quartic = sym.symbols("amplitude coupling quartic", positive=True)
    potential = 3 * coupling * amplitude**sym.Rational(4, 3) / 4 + quartic * amplitude**4 / 4
    state_x = sym.diff(potential, amplitude) / (2 * amplitude)
    stiffness = sym.diff(potential, amplitude, 2) - sym.diff(potential, amplitude) / amplitude
    radial_cubic = sym.diff(potential, amplitude, 3)
    radial_quartic = sym.diff(potential, amplitude, 4)
    derivatives = [amplitude**2]
    for order in range(2, 5):
        derivatives.append(sym.factor(sym.diff(derivatives[-1], amplitude) / sym.diff(state_x, amplitude)))
    expected_p3 = 24 * amplitude**2 / stiffness**2 - 8 * amplitude**3 * radial_cubic / stiffness**3
    expected_p4 = (192 * amplitude**2 / stiffness**3 - 192 * amplitude**3 * radial_cubic / stiffness**4
                   + 48 * amplitude**4 * radial_cubic**2 / stiffness**5
                   - 16 * amplitude**4 * radial_quartic / stiffness**4)
    check("P_XX", derivatives[1] - 4 * amplitude**2 / stiffness)
    check("P_XXX", derivatives[2] - expected_p3)
    check("P_XXXX", derivatives[3] - expected_p4)

    chemical, time_derivative, spatial_squared, marker = sym.symbols("chemical time_derivative spatial_squared marker")
    pressure = sym.symbols("pressure1 pressure2 pressure3 pressure4")
    delta_x = chemical * marker * time_derivative + marker**2 * (time_derivative**2 - spatial_squared) / 2
    lagrangian = sum(pressure[index] * delta_x**(index + 1) / sym.factorial(index + 1) for index in range(4))
    cubic = (chemical * pressure[1] * time_derivative * (time_derivative**2 - spatial_squared) / 2
             + chemical**3 * pressure[2] * time_derivative**3 / 6)
    fourth = (pressure[1] * (time_derivative**2 - spatial_squared)**2 / 8
              + chemical**2 * pressure[2] * time_derivative**2 * (time_derivative**2 - spatial_squared) / 4
              + chemical**4 * pressure[3] * time_derivative**4 / 24)
    check("cubic_phase_Lagrangian", sym.expand(lagrangian).coeff(marker, 3) - cubic)
    check("quartic_phase_Lagrangian", sym.expand(lagrangian).coeff(marker, 4) - fourth)
    point_amplitude = sym.Integer(10)
    point_chemical = sym.Integer(1)
    point_ratio = sym.Integer(2)
    substitution = {
        amplitude: point_amplitude,
        coupling: point_chemical**2 * point_amplitude**sym.Rational(2, 3) / (1 + point_ratio),
        quartic: point_ratio * point_chemical**2 / (point_amplitude**2 * (1 + point_ratio)),
    }
    point_pressure = [sym.simplify(value.subs(substitution)) for value in derivatives]
    kinetic = point_pressure[0] + point_pressure[1]
    sound_squared = point_pressure[0] / kinetic
    check("canonical_sound_match", sound_squared - sym.Rational(5, 23))
    cubic_time = (point_pressure[1] / 2 + point_pressure[2] / 6) / kinetic**sym.Rational(3, 2)
    cubic_mixed = -point_pressure[1] / (2 * kinetic**sym.Rational(3, 2))
    quartic_time = (point_pressure[1] / 8 + point_pressure[2] / 4 + point_pressure[3] / 24) / kinetic**2
    quartic_mixed = -(point_pressure[1] + point_pressure[2]) / (4 * kinetic**2)
    quartic_spatial = point_pressure[1] / (8 * kinetic**2)
    sound = sym.sqrt(sound_squared)
    cubic_bound = 6 * (abs(cubic_time) * sound**3 + abs(cubic_mixed) * sound)
    quartic_bound = 24 * (abs(quartic_time) * sound**4 + abs(quartic_mixed) * sound_squared + abs(quartic_spatial))
    kernel_bound = sym.simplify(quartic_bound + 3 * cubic_bound**2 / sound_squared)
    norm_prefactor = sym.simplify(kernel_bound / (64 * sym.pi**2 * sound**3))
    infrared = sym.Rational(1, 9)**2 * sound / (32 * sym.pi**2)
    second_log = sym.simplify(sym.Rational(2, 3) * infrared**2 / sym.Rational(10, 9)**2)
    cutoffs = []
    for cutoff in [sym.Rational(1, 10), sym.Rational(1, 5), sym.Rational(3, 10)]:
        value = norm_prefactor * cutoff**4
        cutoffs.append({"acoustic_cutoff_over_mu": float(cutoff),
                        "radial_derivative_expansion_ratio": float(cutoff**2 / sym.Rational(10, 9)),
                        "leading_tree_EFT_continuum_norm_bound": float(value),
                        "below_one": bool(value < 1)})
    report = {
        "state": "complete", "created_at": datetime.now(timezone.utc).isoformat(),
        "checks": checks, "exact_check_count": len(checks),
        "P_derivatives_exact": [str(value) for value in point_pressure],
        "time_kinetic_coefficient": str(kinetic), "sound_squared": str(sound_squared),
        "canonical_coefficients": {
            "cubic_time": {"exact": str(cubic_time), "numeric": float(cubic_time)},
            "cubic_mixed": {"exact": str(cubic_mixed), "numeric": float(cubic_mixed)},
            "quartic_time": {"exact": str(quartic_time), "numeric": float(quartic_time)},
            "quartic_mixed": {"exact": str(quartic_mixed), "numeric": float(quartic_mixed)},
            "quartic_spatial": {"exact": str(quartic_spatial), "numeric": float(quartic_spatial)},
        },
        "vertex_bounds": {"C3": float(cubic_bound), "C4": float(quartic_bound),
                          "C_tree": float(kernel_bound), "norm_prefactor": float(norm_prefactor)},
        "cutoff_rows": cutoffs, "isolated_second_rung_phase_log_coefficient": float(second_log),
        "isolated_second_rung_scope": "One contribution of the bare Cartesian ladder, not a complete two-loop physical prediction.",
        "continuum_bound_scope": "Leading-derivative phase EFT, tree contact plus up to three phase-exchange channels, acoustic ball cutoff, zero total Euclidean momentum, derivative-weighted sup norm.",
        "full_microscopic_operator_excluded": False, "renormalized_loop_corrected_EFT_matched": False,
        "parent_seal_sha256": hashlib.sha256((PREVIOUS / "results/stage-integrity.json").read_bytes()).hexdigest(),
    }
    (OUTPUT / "status.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({"state": "complete", "exact_checks": len(checks),
                      "P_derivatives": report["P_derivatives_exact"],
                      "vertex_bounds": report["vertex_bounds"], "cutoffs": cutoffs,
                      "second_log_coefficient": float(second_log)}))


if __name__ == "__main__":
    main()

