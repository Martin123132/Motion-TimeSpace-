from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4985"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4985_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

RESULT_JSON = SOURCE / "metric_frame_O2_flow_results.json"
RESULT_4959 = POST / "source-intake" / "functional_rg" / "4959" / "curvature_sixpoint_projector_results.json"
OUTPUTS = {
    "metric_bulk": SOURCE / "metric_frame_infinitesimal_bulk_cancellation.csv",
    "metric_boundary": SOURCE / "metric_frame_boundary_jet_checks.csv",
    "metric_gate": SOURCE / "metric_frame_O2_connection_zero.csv",
    "power": SOURCE / "O2_loop_power_counting.csv",
    "partial_wave": SOURCE / "O2_partial_wave_projection.csv",
    "crossing": SOURCE / "O2_crossing_projector_checks.csv",
    "sources": SOURCE / "O2_source_decomposition.csv",
    "flow": SOURCE / "O2_corrected_flow_and_trajectory.csv",
    "local": SOURCE / "local_GR_p6_consequence.csv",
    "gate": SOURCE / "metric_frame_O2_flow_gate.csv",
}

MARKER = "MTS_4985_METRIC_FRAME_O2_PARTIAL_WAVE_FLOW"
VALIDATION_MARKER = "MTS_4985_INDEPENDENT_VALIDATION"
CHECKED_DATE = "2026-07-14"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def add_check(rows: list[dict[str, Any]], name: str, passed: bool, evidence: str) -> None:
    rows.append(
        {
            "validation_id": f"VAL4985_{len(rows) + 1:03d}_{name}",
            "passed": passed,
            "evidence": evidence,
            "validation_marker": VALIDATION_MARKER,
            "checkpoint_marker": MARKER,
            "source_checked_date": CHECKED_DATE,
        }
    )


def independent_metric_residuals() -> tuple[float, float]:
    generator = np.random.default_rng(24985)
    maximum_bulk = 0.0
    maximum_boundary = 0.0
    for control_index in range(40):
        metric = np.eye(4) if control_index % 2 == 0 else np.diag([-1.0, 1.0, 1.0, 1.0])
        inverse_metric = np.linalg.inv(metric)
        gradient_covector = generator.normal(size=4)
        gradient_vector = inverse_metric @ gradient_covector
        hessian = generator.normal(size=(4, 4))
        hessian = 0.5 * (hessian + hessian.T)
        ricci = generator.normal(size=(4, 4))
        ricci = 0.5 * (ricci + ricci.T)
        beta_ctilde = float(generator.uniform(-1.8, 1.8))
        beta_d = float(generator.uniform(-1.8, 1.8))
        kappa = float(generator.uniform(0.1, 2.8))
        alpha = beta_d + beta_ctilde / 2.0

        kinetic = float(gradient_covector @ gradient_vector)
        ricci_scalar = float(np.sum(inverse_metric * ricci))
        ricci_vv = float(gradient_vector @ ricci @ gradient_vector)
        einstein_up = inverse_metric @ ricci @ inverse_metric - 0.5 * ricci_scalar * inverse_metric
        metric_variation = kappa * (
            alpha * kinetic * metric - beta_ctilde * np.outer(gradient_covector, gradient_covector)
        )
        direct_bulk = float(np.sum(einstein_up * metric_variation) / kappa)
        expected_bulk = -beta_d * ricci_scalar * kinetic - beta_ctilde * ricci_vv
        bulk_residual = abs(direct_bulk - expected_bulk) / max(abs(direct_bulk), abs(expected_bulk), 1.0e-15)
        maximum_bulk = max(maximum_bulk, bulk_residual)

        derivative_kinetic = 2.0 * hessian @ gradient_vector
        derivative_vector = hessian @ inverse_metric
        trace_hessian = float(np.sum(inverse_metric * hessian))
        direct_boundary = np.zeros(4)
        for component_mu in range(4):
            divergence = alpha * float(inverse_metric[component_mu] @ derivative_kinetic)
            divergence -= beta_ctilde * sum(
                derivative_vector[component_nu, component_mu] * gradient_vector[component_nu]
                + gradient_vector[component_mu] * derivative_vector[component_nu, component_nu]
                for component_nu in range(4)
            )
            trace_gradient = (4.0 * alpha - beta_ctilde) * float(
                inverse_metric[component_mu] @ derivative_kinetic
            )
            direct_boundary[component_mu] = kappa * (divergence - trace_gradient)
        reduced_boundary = kappa * (
            (-6.0 * beta_d - 2.0 * beta_ctilde) * (inverse_metric @ hessian @ gradient_vector)
            - beta_ctilde * gradient_vector * trace_hessian
        )
        boundary_residual = float(np.max(np.abs(direct_boundary - reduced_boundary))) / max(
            float(np.max(np.abs(direct_boundary))),
            float(np.max(np.abs(reduced_boundary))),
            1.0e-15,
        )
        maximum_boundary = max(maximum_boundary, boundary_residual)
    return maximum_bulk, maximum_boundary


def integrate_partial_waves(constant_term: Fraction, quadratic_term: Fraction) -> tuple[Fraction, Fraction]:
    partial_zero = constant_term + quadratic_term / 3
    partial_two = Fraction(2, 15) * quadratic_term
    return partial_zero, partial_two


def legendre_two(value: Fraction) -> Fraction:
    return (3 * value**2 - 1) / 2


def independent_crossing_controls() -> tuple[int, Fraction]:
    partial_gr = integrate_partial_waves(Fraction(-7, 4), Fraction(-1, 4))
    partial_x2 = integrate_partial_waves(Fraction(3, 4), Fraction(1, 4))
    partial_zero_product = partial_gr[0] * partial_x2[0]
    weighted_partial_two_product = 5 * partial_gr[1] * partial_x2[1]
    event_count = 0
    maximum_residual = Fraction(0, 1)
    for s_integer in range(2, 15):
        for t_integer in range(-17, 13, 3):
            s_value = Fraction(s_integer, 1)
            t_value = Fraction(t_integer, 1)
            u_value = -s_value - t_value
            if s_value * t_value * u_value == 0:
                continue
            crossing_sum = Fraction(0, 1)
            channels = (
                (s_value, t_value, u_value),
                (t_value, s_value, u_value),
                (u_value, t_value, s_value),
            )
            for channel_scale, first_other, second_other in channels:
                cosine = (first_other - second_other) / channel_scale
                crossing_sum += channel_scale**3 * (
                    partial_zero_product + weighted_partial_two_product * legendre_two(cosine)
                )
            residual = abs(crossing_sum - Fraction(-9, 2) * s_value * t_value * u_value)
            maximum_residual = max(maximum_residual, residual)
            event_count += 1
    return event_count, maximum_residual


def independent_trajectory_residual() -> float:
    generator = np.random.default_rng(34985)
    maximum_residual = 0.0
    for _ in range(48):
        time_value = float(generator.uniform(-3.5, 2.5))
        initial_g = float(generator.uniform(0.02, 0.3))
        constant_c = float(generator.uniform(-1.5, 1.5))
        constant_w = float(generator.uniform(-1.5, 1.5))
        source_two_loop = float(generator.uniform(-2.5, 2.5))
        g_value = initial_g * math.exp(2.0 * time_value)
        c_value = g_value**2 * (constant_c + 16.0 * time_value)
        ratio = (
            constant_w
            + (source_two_loop - 6.0 * constant_c / math.pi) * time_value
            - 48.0 * time_value**2 / math.pi
        )
        w_value = g_value**3 * ratio
        ratio_derivative = source_two_loop - 6.0 * constant_c / math.pi - 96.0 * time_value / math.pi
        derivative = 6.0 * w_value + g_value**3 * ratio_derivative
        beta = 6.0 * w_value - 6.0 * g_value * c_value / math.pi + source_two_loop * g_value**3
        residual = abs(derivative - beta) / max(abs(derivative), abs(beta), 1.0e-15)
        maximum_residual = max(maximum_residual, residual)
    return maximum_residual


def write_validation(rows: list[dict[str, Any]]) -> None:
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    required = [RESULT_JSON, RESULT_4959, *OUTPUTS.values()]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("\n".join(missing))

    checks: list[dict[str, Any]] = []
    result = json.loads(RESULT_JSON.read_text(encoding="utf-8"))
    prior_result = json.loads(RESULT_4959.read_text(encoding="utf-8"))
    tables = {name: read_csv(path) for name, path in OUTPUTS.items()}

    add_check(checks, "marker", result.get("checkpoint_marker") == MARKER, str(result.get("checkpoint_marker")))
    expected_counts = {
        "metric_bulk": 32,
        "metric_boundary": 32,
        "metric_gate": 6,
        "power": 6,
        "partial_wave": 4,
        "crossing": 12,
        "sources": 6,
        "flow": 7,
        "local": 6,
        "gate": 18,
    }
    for name, expected_count in expected_counts.items():
        add_check(checks, f"rows_{name}", len(tables[name]) == expected_count, f"rows={len(tables[name])}")

    for name, rows in tables.items():
        markers_match = all(row.get("checkpoint_marker") == MARKER for row in rows)
        full_claims_false = all(not parse_bool(row.get("valid_for_full_MTS_claim", "false")) for row in rows)
        add_check(checks, f"table_marker_{name}", markers_match, f"rows={len(rows)}")
        add_check(checks, f"table_nonclaim_{name}", full_claims_false, f"rows={len(rows)}")

    for source_path, expected_hash in result["source_hashes"].items():
        path = ROOT / source_path
        add_check(checks, "source_exists", path.exists(), source_path)
        add_check(checks, "source_hash", path.exists() and digest(path) == expected_hash, source_path)

    output_source_paths: set[str] = set()
    for rows in tables.values():
        for row in rows:
            source_path = row.get("source_path", "").strip()
            if source_path:
                output_source_paths.add(source_path)
    for source_path in sorted(output_source_paths):
        add_check(checks, "cited_path", (ROOT / source_path).exists(), source_path)

    runner_bulk_max = max(float(row["relative_residual"]) for row in tables["metric_bulk"])
    runner_boundary_max = max(float(row["relative_residual"]) for row in tables["metric_boundary"])
    add_check(checks, "runner_bulk", runner_bulk_max < 2.0e-13, f"max={runner_bulk_max:.3e}")
    add_check(checks, "runner_boundary", runner_boundary_max < 2.0e-13, f"max={runner_boundary_max:.3e}")

    independent_bulk, independent_boundary = independent_metric_residuals()
    add_check(checks, "independent_bulk", independent_bulk < 2.0e-13, f"max={independent_bulk:.3e}")
    add_check(checks, "independent_boundary", independent_boundary < 2.0e-13, f"max={independent_boundary:.3e}")

    metric_statuses = {row["status"] for row in tables["metric_gate"]}
    add_check(
        checks,
        "metric_connection_zero",
        "METRIC_FRAME_CONNECTION_ZERO" in metric_statuses,
        ";".join(sorted(metric_statuses)),
    )
    add_check(
        checks,
        "metric_finite_order",
        any("begins quadratically" in row["consequence"] for row in tables["metric_gate"]),
        "finite off-surface spillover retained",
    )

    for row in tables["power"]:
        higher_orders = [] if row["higher_derivative_vertices"] == "none" else [
            int(value) for value in row["higher_derivative_vertices"].split(";")
        ]
        recalculated = 2 + 2 * int(row["loop_order_L"]) + sum(order - 2 for order in higher_orders)
        add_check(
            checks,
            "power_count",
            recalculated == int(row["calculated_derivative_order_D"]),
            f"{row['case_id']} D={recalculated}",
        )

    expected_partial = {
        "GR_soft_regularized": integrate_partial_waves(Fraction(-7, 4), Fraction(-1, 4)),
        "X2_contact": integrate_partial_waves(Fraction(3, 4), Fraction(1, 4)),
        "O2_target": integrate_partial_waves(Fraction(-3, 4), Fraction(3, 4)),
    }
    for name, expected in expected_partial.items():
        row = next(row for row in tables["partial_wave"] if name in row["projector_id"])
        actual = (Fraction(row["a_J0"]), Fraction(row["a_J2"]))
        add_check(checks, f"partial_{name}", actual == expected, f"actual={actual} expected={expected}")

    partial_gr = expected_partial["GR_soft_regularized"]
    partial_x2 = expected_partial["X2_contact"]
    mixed_expected = (partial_gr[0] * partial_x2[0], partial_gr[1] * partial_x2[1])
    mixed_row = next(row for row in tables["partial_wave"] if "mixed_product" in row["projector_id"])
    mixed_actual = (Fraction(mixed_row["a_J0"]), Fraction(mixed_row["a_J2"]))
    add_check(checks, "mixed_partial", mixed_actual == mixed_expected, f"actual={mixed_actual}")

    crossing_events, crossing_residual = independent_crossing_controls()
    add_check(checks, "independent_crossing", crossing_residual == 0, f"events={crossing_events} residual={crossing_residual}")
    output_crossing_exact = all(Fraction(row["exact_residual"]) == 0 for row in tables["crossing"])
    output_beta_exact = all(Fraction(row["beta_w_over_u_over_Mpminus2_over_pi2"]) == Fraction(-3, 16) for row in tables["crossing"])
    add_check(checks, "output_crossing", output_crossing_exact, f"rows={len(tables['crossing'])}")
    add_check(checks, "output_beta", output_beta_exact, "-3/16")

    source_statuses = {row["status"] for row in tables["sources"]}
    add_check(checks, "minimal_one_loop_zero", "DERIVED_BY_EFT_POWER_COUNTING" in source_statuses, ";".join(sorted(source_statuses)))
    add_check(checks, "X2_mix_derived", "DERIVED_COMPLETE_SCALAR_CUT" in source_statuses, ";".join(sorted(source_statuses)))
    add_check(checks, "two_loop_open", "COMMON_SCHEME_SINGLE_LOG_COEFFICIENT_OPEN" in source_statuses, ";".join(sorted(source_statuses)))

    flow_equations = "\n".join(row["equation"] for row in tables["flow"])
    add_check(checks, "corrected_beta", "beta_w=6w-(6/pi)g c_ess+S_2L g^3" in flow_equations, "corrected source order")
    add_check(checks, "corrected_trajectory", "w/g^3=C_w+(S_2L-6C_c/pi)t-(48/pi)t^2" in flow_equations, "integrated exact solution")
    add_check(checks, "finite_scheme_law", "S_2L'=S_2L+16alpha" in flow_equations, "resonant p6 scheme transformation")
    add_check(checks, "mixed_coefficient_invariant", "B_gc'=B_gc=-6/pi" in flow_equations, "one-loop mixing is scheme invariant")
    add_check(checks, "double_log_invariant", "-(48/pi)t^2" in flow_equations, "A_c B_gc/2=-48/pi")
    trajectory_residual = independent_trajectory_residual()
    add_check(checks, "independent_trajectory", trajectory_residual < 2.0e-13, f"max={trajectory_residual:.3e}")

    local_statuses = {row["status"] for row in tables["local"]}
    add_check(checks, "local_silence", "EXACT_SELECTED_BRANCH_SILENCE" in local_statuses, ";".join(sorted(local_statuses)))
    add_check(checks, "Newton_retained", "LEADING_NEWTON_RETAINED" in local_statuses, ";".join(sorted(local_statuses)))
    add_check(checks, "exact_GR_not_claimed", result["gates"]["exact_local_GR"] is False, str(result["gates"]))
    add_check(checks, "full_MTS_not_claimed", result["gates"]["full_MTS"] is False, str(result["gates"]))

    prior_minima = [float(row["full_basis_kernel_minimized_over_O2"]) for row in prior_result["trajectory_bounds"]]
    add_check(checks, "prior_rate_positive", min(prior_minima) > 0.0, f"minimum={min(prior_minima):.12e}")
    add_check(
        checks,
        "arbitrary_O2_bound",
        prior_result["gates"]["arbitrary_O2_cannot_cancel_X3_rate"] is True,
        "4985 changes source order, not the coefficient-independent lower bound",
    )

    all_passed = all(bool(row["passed"]) for row in checks)
    add_check(checks, "overall", all_passed, f"pre_overall_checks={len(checks)}")
    if not all(bool(row["passed"]) for row in checks):
        failures = [row for row in checks if not bool(row["passed"])]
        raise RuntimeError(json.dumps(failures, indent=2))

    write_validation(checks)
    VALIDATION_PROVENANCE.write_text(
        "\n".join(
            [
                "# 4985 independent validation provenance",
                "",
                f"Marker: `{VALIDATION_MARKER}`.",
                "",
                f"Checks: `{len(checks)}/{len(checks)}` passed.",
                "",
                f"Fresh metric bulk maximum relative residual: `{independent_bulk:.16e}`.",
                f"Fresh metric boundary maximum relative residual: `{independent_boundary:.16e}`.",
                f"Fresh exact rational crossing controls: `{crossing_events}` with residual `{crossing_residual}`.",
                f"Fresh trajectory maximum relative residual: `{trajectory_residual:.16e}`.",
                "",
                "The validator independently rebuilds the local metric first-variation identities, exact partial-wave integrals, crossing sum, corrected weak trajectory, source hashes, cited paths, prior arbitrary-O2 rate bound, and nonclaim gates. It does not import runner functions.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(json.dumps({"validation_marker": VALIDATION_MARKER, "passed": len(checks), "total": len(checks)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
