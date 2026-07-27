from __future__ import annotations

import csv
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Any

import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4990"
CROSSING = SOURCE / "crossed_scalar_cut_identity.csv"
FLOWS = SOURCE / "flow_scheme_separation.csv"
SCHEME_ORBIT = SOURCE / "scheme_orbit_propagation_correction.csv"
CANCELLATION = SOURCE / "corrected_D1_cancellation.csv"
HH_SCOPE = SOURCE / "hh_crossing_support_scope.csv"
SUPERSESSION = SOURCE / "4989_supersession_matrix.csv"
GATES = SOURCE / "corrected_master_gate.csv"
RESULT = SOURCE / "crossed_cut_D1_scheme_bridge_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4990_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

MARKER = "MTS_4990_CROSSED_CUT_D1_SCHEME_BRIDGE_CORRECTION"
VALIDATION_MARKER = "P8_Y5_BRR545_4990_VALIDATION"

s, t, u = sp.symbols("s t u", nonzero=True)
x = sp.symbols("x", real=True)
L_A, L_B, Q_A, Q_B = sp.symbols("L_A L_B Q_A Q_B")
C_c, C_w, S_2L, rho_mix, r4, A_2, B_2 = sp.symbols("C_c C_w S_2L rho_mix r4 A_2 B_2")
alpha, beta = sp.symbols("alpha beta")
PI = sp.pi


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes"}


def add(checks: list[dict[str, Any]], check_id: str, passed: bool, evidence: str) -> None:
    checks.append(
        {
            "validation_id": f"VAL4990_{len(checks) + 1:04d}_{check_id}",
            "check": check_id,
            "passed": bool(passed),
            "evidence": evidence,
            "validation_marker": VALIDATION_MARKER,
        }
    )


def parse(expression: str) -> sp.Expr:
    return sp.sympify(
        expression,
        locals={
            "x": x,
            "pi": PI,
            "Q_A": Q_A,
            "Q_B": Q_B,
            "L_A": L_A,
            "L_B": L_B,
            "C_c": C_c,
            "C_w": C_w,
            "S_2L": S_2L,
            "rho_mix": rho_mix,
            "r4": r4,
            "A_2": A_2,
            "B_2": B_2,
            "alpha": alpha,
            "beta": beta,
        },
    )


def write_validation(rows: list[dict[str, Any]]) -> None:
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    checks: list[dict[str, Any]] = []
    files = [CROSSING, FLOWS, SCHEME_ORBIT, CANCELLATION, HH_SCOPE, SUPERSESSION, GATES, RESULT, PROVENANCE]
    for path in files:
        add(checks, f"file_exists_{path.stem}", path.exists(), str(path))
        add(
            checks,
            f"file_nonempty_{path.stem}",
            path.exists() and path.stat().st_size > 0,
            str(path.stat().st_size if path.exists() else 0),
        )

    crossing_rows = read_csv(CROSSING)
    flow_rows = read_csv(FLOWS)
    scheme_rows = read_csv(SCHEME_ORBIT)
    cancellation_rows = read_csv(CANCELLATION)
    hh_rows = read_csv(HH_SCOPE)
    supersession_rows = read_csv(SUPERSESSION)
    gate_rows = read_csv(GATES)
    result = json.loads(RESULT.read_text(encoding="utf-8"))

    tables = {
        "crossing": crossing_rows,
        "flows": flow_rows,
        "scheme_orbit": scheme_rows,
        "cancellation": cancellation_rows,
        "hh_scope": hh_rows,
        "supersession": supersession_rows,
        "gates": gate_rows,
    }
    expected_counts = {
        "crossing": 6,
        "flows": 4,
        "scheme_orbit": 8,
        "cancellation": 8,
        "hh_scope": 5,
        "supersession": 5,
        "gates": 20,
    }
    for name, rows in tables.items():
        add(checks, f"row_count_{name}", len(rows) == expected_counts[name], str(len(rows)))
        add(checks, f"csv_shape_{name}", all(None not in row for row in rows), "no surplus columns")
        add(checks, f"marker_{name}", all(row["checkpoint_marker"] == MARKER for row in rows), MARKER)
        add(
            checks,
            f"full_MTS_false_{name}",
            all(not truth(row["valid_for_full_MTS_claim"]) for row in rows),
            "all rows remain guarded",
        )
        joined = "\n".join(str(value) for row in rows for value in row.values())
        add(checks, f"no_missing_marker_{name}", "MISSING_" not in joined, "no fabricated placeholder marker")

    add(checks, "result_marker", result["checkpoint_marker"] == MARKER, result["checkpoint_marker"])
    add(checks, "all_source_markers", all(result["source_checks"].values()), json.dumps(result["source_checks"], sort_keys=True))
    add(checks, "source_marker_count", len(result["source_checks"]) == 15, str(len(result["source_checks"])))
    for source_path, expected_hash in result["source_hashes"].items():
        path = ROOT / source_path
        add(checks, f"source_exists_{len(checks)}", path.exists(), source_path)
        if path.exists():
            add(checks, f"source_hash_{len(checks)}", digest(path) == expected_hash, source_path)

    for row in flow_rows:
        source_path = ROOT / row["source_path"]
        add(checks, f"flow_source_exists_{row['flow_id']}", source_path.exists(), row["source_path"])

    p2 = lambda value: sp.legendre(2, value)
    substitution = {u: -s - t}
    channel_identity = sp.factor((s**3 * p2((t - u) / s) - s**3 + 6 * s * t * u).subs(substitution))
    cube_identity = sp.factor((s**3 + t**3 + u**3 - 3 * s * t * u).subs(substitution))
    p2_sum_identity = sp.factor(
        (
            s**3 * p2((t - u) / s)
            + t**3 * p2((u - s) / t)
            + u**3 * p2((s - t) / u)
            + 15 * s * t * u
        ).subs(substitution)
    )
    mixed_identity = sp.factor(
        (
            s**3 * (-sp.Rational(55, 36) - p2((t - u) / s) / 180)
            + t**3 * (-sp.Rational(55, 36) - p2((u - s) / t) / 180)
            + u**3 * (-sp.Rational(55, 36) - p2((s - t) / u) / 180)
            + sp.Rational(9, 2) * s * t * u
        ).subs(substitution)
    )
    identities = {
        "single_channel_P2": channel_identity,
        "sum_cubes": cube_identity,
        "sum_P2": p2_sum_identity,
        "mixed_kernel": mixed_identity,
    }
    for name, residual in identities.items():
        add(checks, f"symbolic_{name}", residual == 0, str(residual))

    randomizer = random.Random(4990)
    for event in range(24):
        s_value = sp.Rational(randomizer.randint(1, 71), randomizer.randint(1, 29))
        t_value = -sp.Rational(randomizer.randint(1, 67), randomizer.randint(1, 31))
        if s_value + t_value == 0:
            t_value -= sp.Rational(1, 37)
        event_values = {s: s_value, t: t_value}
        for name, residual in identities.items():
            value = sp.simplify(residual.subs(event_values))
            add(checks, f"rational_{event:02d}_{name}", value == 0, str(value))

    crossing_by_id = {row["identity_id"]: row for row in crossing_rows}
    add(
        checks,
        "recorded_crossing_residuals",
        all(parse(row["exact_residual"]) == 0 for row in crossing_rows),
        ",".join(row["identity_id"] for row in crossing_rows),
    )
    add(
        checks,
        "recorded_crossed_log_statement",
        crossing_by_id["CROSS4990_06_crossed_scalar_log"]["statement"] == "Dphi_crossed,log=-(203/20)F1_log",
        crossing_by_id["CROSS4990_06_crossed_scalar_log"]["statement"],
    )

    p2_x = sp.expand(sp.legendre(2, 1 - 2 * x))
    d0_slope = -sp.Rational(2233, 72) / PI
    d2_slope = -sp.Rational(203, 1800) / PI
    mixed_kernel = -sp.Rational(55, 36) - p2_x / 180
    direct_slope = sp.factor(d0_slope + d2_slope * p2_x)
    add(
        checks,
        "scalar_slope_factorization",
        sp.simplify(direct_slope - sp.Rational(203, 10) / PI * mixed_kernel) == 0,
        str(direct_slope),
    )

    f1_log = sp.Rational(2, 1) / PI * (sp.Rational(23, 15) * L_A - sp.Rational(1, 30) * L_B)
    crossed_log = sp.factor((d0_slope + d2_slope) * L_A - 6 * d2_slope * L_B)
    d1_multiplier = -sp.Rational(203, 10)
    beta_smatrix = sp.Rational(203, 10)
    add(checks, "crossed_scalar_log", sp.simplify(crossed_log + sp.Rational(203, 20) * f1_log) == 0, str(crossed_log))
    add(checks, "master_D1_cancellation", sp.simplify(2 * crossed_log - d1_multiplier * f1_log) == 0, str(sp.simplify(2 * crossed_log - d1_multiplier * f1_log)))

    f2_double = sp.factor(beta_smatrix / (2 * PI) * (sp.Rational(23, 15) * Q_A - sp.Rational(1, 30) * Q_B))
    f2_derivative = sp.factor(f2_double.subs({Q_A: -4 * L_A, Q_B: -4 * L_B}))
    direct_double_log = sp.factor(-beta_smatrix / PI * (sp.Rational(23, 15) - x * (1 - x) / 30))
    add(checks, "double_log_RG", sp.simplify(f2_derivative + beta_smatrix * f1_log) == 0, str(f2_derivative))
    add(checks, "direct_double_log", sp.simplify(direct_double_log - direct_slope) == 0, str(direct_double_log))

    flow_by_id = {row["flow_id"]: row for row in flow_rows}
    add(checks, "FRG_coefficient", parse(flow_by_id["FLOW4990_01_FRG"]["flow_coefficient"]) == 16, flow_by_id["FLOW4990_01_FRG"]["flow_coefficient"])
    add(checks, "FRG_not_direct_D1", not truth(flow_by_id["FLOW4990_01_FRG"]["may_enter_on_shell_D1_directly"]), flow_by_id["FLOW4990_01_FRG"]["status"])
    add(checks, "Smatrix_coefficient", parse(flow_by_id["FLOW4990_02_Smatrix"]["flow_coefficient"]) == beta_smatrix, flow_by_id["FLOW4990_02_Smatrix"]["flow_coefficient"])
    add(checks, "Smatrix_direct_D1", truth(flow_by_id["FLOW4990_02_Smatrix"]["may_enter_on_shell_D1_directly"]), flow_by_id["FLOW4990_02_Smatrix"]["status"])
    add(checks, "D_operator_sign", parse(flow_by_id["FLOW4990_03_D_operator"]["flow_coefficient"]) == d1_multiplier, flow_by_id["FLOW4990_03_D_operator"]["flow_coefficient"])
    add(checks, "finite_bridge_open", flow_by_id["FLOW4990_04_bridge"]["flow_coefficient"] == "not derived", flow_by_id["FLOW4990_04_bridge"]["status"])
    add(checks, "scheme_coefficients_distinct", beta_smatrix != 16, f"16 != {beta_smatrix}")

    B_gc = -sp.Rational(6, 1) / PI
    f_A = sp.Rational(46, 15) / PI
    f_B = -sp.Rational(1, 15) / PI
    trajectory_double_log = sp.factor(B_gc * beta_smatrix / 2)
    S_prime = S_2L + beta_smatrix * alpha - B_gc * beta
    rho_prime = rho_mix + 3 * alpha
    r4_prime = r4 - beta
    I_fixed = sp.factor(3 * S_2L - beta_smatrix * rho_mix)
    I_fixed_prime = sp.factor(3 * S_prime - beta_smatrix * rho_prime)
    I_shift_residual = sp.factor(I_fixed_prime - I_fixed + 3 * B_gc * beta)
    K_mu = sp.factor(I_fixed - 3 * B_gc * r4)
    K_mu_prime = sp.factor(I_fixed_prime - 3 * B_gc * r4_prime)
    K_mu_residual = sp.factor(K_mu_prime - K_mu)
    A_prime = A_2 - beta * f_A
    B_prime = B_2 - beta * f_B
    K_ang = sp.factor(A_2 - B_2 - (f_A - f_B) * r4)
    K_ang_prime = sp.factor(A_prime - B_prime - (f_A - f_B) * r4_prime)
    K_ang_residual = sp.factor(K_ang_prime - K_ang)
    S_rf = sp.factor(S_2L - beta_smatrix * rho_mix / 3 - B_gc * r4)
    A_rf = sp.factor(A_2 - f_A * r4)
    B_rf = sp.factor(B_2 - f_B * r4)
    rf_mu_residual = sp.factor(3 * S_rf - K_mu)
    rf_ang_residual = sp.factor(A_rf - B_rf - K_ang)
    add(checks, "orbit_trajectory_double_log", trajectory_double_log == -sp.Rational(609, 10) / PI, str(trajectory_double_log))
    add(checks, "orbit_I_shift", I_shift_residual == 0, str(I_shift_residual))
    add(checks, "orbit_Kmu_invariant", K_mu_residual == 0, str(K_mu_residual))
    add(checks, "orbit_Kang_invariant", K_ang_residual == 0, str(K_ang_residual))
    add(checks, "orbit_rational_free_Kmu", rf_mu_residual == 0, str(rf_mu_residual))
    add(checks, "orbit_rational_free_Kang", rf_ang_residual == 0, str(rf_ang_residual))

    scheme_by_id = {row["correction_id"]: row for row in scheme_rows}
    add(checks, "recorded_orbit_residuals", all(parse(row["exact_residual"]) == 0 for row in scheme_rows), ",".join(scheme_by_id))
    add(checks, "recorded_trajectory_double_log", parse(scheme_by_id["ORBIT4990_03_W_double_log"]["corrected_expression"]) == trajectory_double_log, scheme_by_id["ORBIT4990_03_W_double_log"]["corrected_expression"])
    add(checks, "recorded_fixed_p4_I", sp.simplify(parse(scheme_by_id["ORBIT4990_05_fixed_p4_I"]["corrected_expression"]) - I_fixed) == 0, scheme_by_id["ORBIT4990_05_fixed_p4_I"]["corrected_expression"])
    add(checks, "recorded_full_Kmu", sp.simplify(parse(scheme_by_id["ORBIT4990_06_full_K_mu"]["corrected_expression"]) - K_mu) == 0, scheme_by_id["ORBIT4990_06_full_K_mu"]["corrected_expression"])
    add(checks, "recorded_full_Kang", sp.simplify(parse(scheme_by_id["ORBIT4990_07_full_K_ang"]["corrected_expression"]) - K_ang) == 0, scheme_by_id["ORBIT4990_07_full_K_ang"]["corrected_expression"])

    cancellation_by_id = {row["check_id"]: row for row in cancellation_rows}
    add(checks, "recorded_multiplier", cancellation_by_id["D1C4990_01_master_multiplier"]["exact_expression"] == "(-203/10) F1", cancellation_by_id["D1C4990_01_master_multiplier"]["exact_expression"])
    add(checks, "recorded_cancellation_zero", parse(cancellation_by_id["D1C4990_02_crossed_log_cancellation"]["exact_expression"]) == 0, cancellation_by_id["D1C4990_02_crossed_log_cancellation"]["exact_expression"])
    add(checks, "recorded_F2_double", sp.simplify(parse(cancellation_by_id["D1C4990_03_corrected_double_log"]["exact_expression"]) - f2_double) == 0, cancellation_by_id["D1C4990_03_corrected_double_log"]["exact_expression"])
    add(checks, "recorded_direct_double_log", sp.simplify(parse(cancellation_by_id["D1C4990_04_direct_channel_double_log"]["exact_expression"]) - direct_double_log) == 0, cancellation_by_id["D1C4990_04_direct_channel_double_log"]["exact_expression"])

    d0_constant = sp.Rational(143, 1) * (120 * PI**2 + 1397) / (6480 * PI)
    d2_constant = (-621877 + 103800 * PI**2) / (162000 * PI)
    delta_a = sp.factor(d0_constant + d2_constant)
    delta_b = sp.factor(-6 * d2_constant)
    delta_k_mu = sp.factor(-6 * (d0_constant - 5 * d2_constant))
    delta_k_ang = sp.factor(d0_constant + 7 * d2_constant)
    subtotal_expectations = {
        "D1C4990_05_scalar_A": delta_a,
        "D1C4990_06_scalar_B": delta_b,
        "D1C4990_07_scalar_Kmu": delta_k_mu,
        "D1C4990_08_scalar_Kang": delta_k_ang,
    }
    for row_id, expected in subtotal_expectations.items():
        recorded = parse(cancellation_by_id[row_id]["exact_expression"])
        add(checks, f"subtotal_{row_id}", sp.simplify(recorded - expected) == 0, str(recorded))
    add(checks, "Kmu_numeric", abs(float(delta_k_mu.evalf(30)) - float(cancellation_by_id["D1C4990_07_scalar_Kmu"]["numeric_value"])) < 1e-13, cancellation_by_id["D1C4990_07_scalar_Kmu"]["numeric_value"])
    add(checks, "Kang_numeric", abs(float(delta_k_ang.evalf(30)) - float(cancellation_by_id["D1C4990_08_scalar_Kang"]["numeric_value"])) < 1e-13, cancellation_by_id["D1C4990_08_scalar_Kang"]["numeric_value"])

    p4 = lambda value: sp.legendre(4, value)
    crossed_p4 = sp.factor(
        ((-x) ** 4 * p4(((x - 1) - 1) / (-x)) + (x - 1) ** 4 * p4((1 - (-x)) / (x - 1)))
    )
    expected_p4 = 2 * x**4 - 4 * x**3 + 126 * x**2 - 124 * x + 71
    p0_moment = sp.factor(sp.integrate(crossed_p4, (x, 0, 1)))
    p2_coefficient = sp.factor(5 * sp.integrate(crossed_p4 * p2_x, (x, 0, 1)))
    add(checks, "crossed_P4_polynomial", sp.simplify(crossed_p4 - expected_p4) == 0, str(crossed_p4))
    add(checks, "crossed_P4_P0", p0_moment == sp.Rational(252, 5), str(p0_moment))
    add(checks, "crossed_P4_P2", p2_coefficient == sp.Rational(144, 7), str(p2_coefficient))
    hh_by_id = {row["scope_id"]: row for row in hh_rows}
    add(checks, "recorded_hh_polynomial", sp.simplify(parse(hh_by_id["HHX4990_02_crossing_noninvariance"]["exact_value"]) - crossed_p4) == 0, hh_by_id["HHX4990_02_crossing_noninvariance"]["exact_value"])
    add(checks, "recorded_hh_P0", parse(hh_by_id["HHX4990_03_crossed_P0"]["exact_value"]) == p0_moment, hh_by_id["HHX4990_03_crossed_P0"]["exact_value"])
    add(checks, "recorded_hh_P2", parse(hh_by_id["HHX4990_04_crossed_P2"]["exact_value"]) == p2_coefficient, hh_by_id["HHX4990_04_crossed_P2"]["exact_value"])
    add(checks, "hh_global_zero_not_claimed", "unknown" in hh_by_id["HHX4990_05_correct_boundary"]["exact_value"], hh_by_id["HHX4990_05_correct_boundary"]["exact_value"])

    add(checks, "supersession_count", len(supersession_rows) == 5, str(len(supersession_rows)))
    add(checks, "supersession_decisions", {row["4990_decision"] for row in supersession_rows} == {"superseded", "rejected", "narrowed"}, ",".join(row["4990_decision"] for row in supersession_rows))
    add(checks, "supersession_corrected", all(row["status"] == "CORRECTED" for row in supersession_rows), ",".join(row["status"] for row in supersession_rows))

    gates_by_name = {row["gate"]: row for row in gate_rows}
    closed_gates = {
        "primary_source_lock",
        "crossed_channel_algebra",
        "scalar_slope_factorization",
        "smatrix_D1_multiplier",
        "crossed_log_cancellation",
        "corrected_double_log",
        "direct_double_log_match",
        "FRG_Smatrix_separated",
        "scalar_subtotals_restored",
        "hh_direct_support_only",
        "4989_affected_claims_superseded",
        "inherited_scheme_orbit_corrected",
    }
    open_gates = set(gates_by_name) - closed_gates
    add(checks, "closed_gate_count", len(closed_gates) == 12, str(len(closed_gates)))
    add(checks, "open_gate_count", len(open_gates) == 8, str(len(open_gates)))
    for gate in sorted(closed_gates):
        row = gates_by_name[gate]
        add(checks, f"closed_gate_{gate}", truth(row["passed"]) and truth(row["valid_for_checkpoint_claim"]), row["status"])
    for gate in sorted(open_gates):
        row = gates_by_name[gate]
        add(checks, f"open_gate_{gate}", not truth(row["passed"]) and not truth(row["valid_for_checkpoint_claim"]), row["status"])

    add(checks, "result_beta_Smatrix", parse(result["flow_separation"]["beta_C_Smatrix"]) == beta_smatrix, result["flow_separation"]["beta_C_Smatrix"])
    add(checks, "result_D_operator", parse(result["flow_separation"]["D_C_Smatrix"]) == d1_multiplier, result["flow_separation"]["D_C_Smatrix"])
    add(checks, "result_bridge_false", result["flow_separation"]["finite_bridge_derived"] is False, str(result["flow_separation"]["finite_bridge_derived"]))
    add(checks, "result_orbit_double_log", parse(result["scheme_orbit_correction"]["trajectory_double_log"]) == trajectory_double_log, result["scheme_orbit_correction"]["trajectory_double_log"])
    add(checks, "result_orbit_I", sp.simplify(parse(result["scheme_orbit_correction"]["I_fixed_p4"]) - I_fixed) == 0, result["scheme_orbit_correction"]["I_fixed_p4"])
    add(checks, "result_orbit_Kmu", sp.simplify(parse(result["scheme_orbit_correction"]["K_mu"]) - K_mu) == 0, result["scheme_orbit_correction"]["K_mu"])
    add(checks, "result_orbit_Kang", sp.simplify(parse(result["scheme_orbit_correction"]["K_ang"]) - K_ang) == 0, result["scheme_orbit_correction"]["K_ang"])
    add(checks, "result_orbit_residuals", all(parse(result["scheme_orbit_correction"][name]) == 0 for name in ("I_shift_residual", "K_mu_residual", "K_ang_residual", "rational_free_mu_residual", "rational_free_ang_residual")), json.dumps(result["scheme_orbit_correction"], sort_keys=True))
    add(checks, "result_master_zero", parse(result["corrected_D1"]["master_log_residual"]) == 0, result["corrected_D1"]["master_log_residual"])
    add(checks, "result_direct_zero", parse(result["corrected_D1"]["direct_channel_double_log_residual"]) == 0, result["corrected_D1"]["direct_channel_double_log_residual"])
    add(checks, "result_full_Kmu_false", result["numeric_full_K_mu"] is False, str(result["numeric_full_K_mu"]))
    add(checks, "result_full_Kang_false", result["numeric_full_K_ang"] is False, str(result["numeric_full_K_ang"]))
    add(checks, "result_local_GR_false", result["exact_all_operator_local_GR"] is False, str(result["exact_all_operator_local_GR"]))
    add(checks, "result_full_MTS_false", result["full_MTS"] is False, str(result["full_MTS"]))

    write_validation(checks)
    passed = sum(bool(row["passed"]) for row in checks)
    VALIDATION_PROVENANCE.write_text(
        "\n".join(
            [
                "# 4990 independent validation provenance",
                "",
                f"Marker: `{VALIDATION_MARKER}`.",
                "",
                "The validator does not import the generator. It independently proves the cyclic crossing identities, checks 24 exact rational kinematic events, reconstructs the scalar crossed-log and corrected double-log equations, propagates beta_C=203/10 through the 4985-4987 finite scheme orbit, separates the FRG and on-shell flow coordinates, restores the scalar invariant subtotals, constructs the crossed-P4 low-spin counterexample, verifies all source hashes and source paths, and enforces the eight explicit nonclaim gates.",
                "",
                f"Checks passed: `{passed}/{len(checks)}`.",
                f"Validation CSV: `{VALIDATION.relative_to(ROOT).as_posix()}`.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "validation_marker": VALIDATION_MARKER,
                "passed": passed,
                "total": len(checks),
                "output": str(VALIDATION),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
