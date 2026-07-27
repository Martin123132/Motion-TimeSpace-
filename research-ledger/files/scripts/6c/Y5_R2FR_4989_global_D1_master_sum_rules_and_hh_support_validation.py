from __future__ import annotations

import csv
import hashlib
import json
import random
import sys
from pathlib import Path
from typing import Any

import mpmath as mp
import sympy as sp


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4989"
FACTOR_TWO = SOURCE / "master_factor_two_normalization.csv"
D1_KERNEL = SOURCE / "D1_ReF1_channel_kernel.csv"
D1_MOMENTS = SOURCE / "D1_legendre_moment_tower.csv"
SUM_RULES = SOURCE / "remaining_cut_sum_rules.csv"
HH_SUPPORT = SOURCE / "opposite_helicity_hh_support.csv"
AFFINE = SOURCE / "master_affine_invariant_coordinates.csv"
GATE = SOURCE / "global_master_completion_gate.csv"
RESULT = SOURCE / "global_D1_master_sum_rules_results.json"
VALIDATION = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_4989_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

MARKER = "MTS_4989_GLOBAL_D1_MASTER_SUM_RULES_HH_SUPPORT"
VALIDATION_MARKER = "P8_Y5_BRR545_4989_VALIDATION"

x, L = sp.symbols("x L", positive=True)
r0, r2 = sp.symbols("r0 r2")
PI = sp.pi
P2 = sp.expand(sp.legendre(2, 1 - 2 * x))


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
            "validation_id": f"VAL4989_{len(checks) + 1:04d}_{check_id}",
            "check": check_id,
            "passed": bool(passed),
            "evidence": evidence,
            "validation_marker": VALIDATION_MARKER,
        }
    )


def write_validation(rows: list[dict[str, Any]]) -> None:
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def parse(expression: str) -> sp.Expr:
    return sp.sympify(expression, locals={"x": x, "L": L, "r0": r0, "r2": r2, "pi": PI})


def polynomial_log_moment(spin: int, power: int) -> sp.Expr:
    polynomial = sp.Poly(sp.expand(sp.legendre(spin, 1 - 2 * x)), x)
    value = sp.S.Zero
    for monomial, coefficient in polynomial.terms():
        value -= coefficient / sp.Rational(monomial[0] + power + 1) ** 2
    return sp.factor(value)


def independent_g0_moment(spin: int) -> sp.Expr:
    a1 = polynomial_log_moment(spin, 1)
    a2 = polynomial_log_moment(spin, 2)
    a3 = polynomial_log_moment(spin, 3)
    return sp.factor(-sp.Rational(32, 1) / PI * (sp.Rational(46, 15) * a3 + sp.Rational(1, 15) * (a1 - a2)))


def independent_gL_moment(spin: int) -> sp.Expr:
    polynomial = sp.expand(sp.legendre(spin, 1 - 2 * x))
    return sp.factor(sp.integrate(polynomial * 144 * x * (1 - x) / PI, (x, 0, 1)))


def main() -> int:
    checks: list[dict[str, Any]] = []
    files = [FACTOR_TWO, D1_KERNEL, D1_MOMENTS, SUM_RULES, HH_SUPPORT, AFFINE, GATE, RESULT]
    for path in files:
        add(checks, f"file_exists_{path.stem}", path.exists(), str(path))
        add(checks, f"file_nonempty_{path.stem}", path.exists() and path.stat().st_size > 0, str(path.stat().st_size if path.exists() else 0))

    factor_rows = read_csv(FACTOR_TWO)
    kernel_rows = read_csv(D1_KERNEL)
    moment_rows = read_csv(D1_MOMENTS)
    sum_rows = read_csv(SUM_RULES)
    hh_rows = read_csv(HH_SUPPORT)
    affine_rows = read_csv(AFFINE)
    gate_rows = read_csv(GATE)
    result = json.loads(RESULT.read_text(encoding="utf-8"))

    tables = {
        "factor": factor_rows,
        "kernel": kernel_rows,
        "moments": moment_rows,
        "sum_rules": sum_rows,
        "hh_support": hh_rows,
        "affine": affine_rows,
        "gates": gate_rows,
    }
    expected_counts = {"factor": 4, "kernel": 8, "moments": 11, "sum_rules": 7, "hh_support": 6, "affine": 6, "gates": 17}
    for name, rows in tables.items():
        add(checks, f"row_count_{name}", len(rows) == expected_counts[name], str(len(rows)))
        add(checks, f"csv_shape_{name}", all(None not in row for row in rows), "no surplus columns")
        add(checks, f"marker_{name}", all(row["checkpoint_marker"] == MARKER for row in rows), MARKER)
        add(checks, f"full_MTS_false_{name}", all(not truth(row["valid_for_full_MTS_claim"]) for row in rows), "all rows guarded")

    add(checks, "result_marker", result["checkpoint_marker"] == MARKER, result["checkpoint_marker"])
    add(checks, "all_source_checks", all(result["source_checks"].values()), json.dumps(result["source_checks"], sort_keys=True))
    for source_path, expected_hash in result["source_hashes"].items():
        path = ROOT / source_path
        add(checks, f"source_exists_{len(checks)}", path.exists(), source_path)
        if path.exists():
            add(checks, f"source_hash_{len(checks)}", digest(path) == expected_hash, source_path)

    factor_by_id = {row["normalization_id"]: row for row in factor_rows}
    add(checks, "optical_theorem_equation", factor_by_id["NORM4989_01_optical_theorem"]["equation"] == "2 Im F = U", factor_by_id["NORM4989_01_optical_theorem"]["equation"])
    add(checks, "raw_cut_equation", factor_by_id["NORM4989_03_raw_cut_coordinate"]["equation"] == "D_phiphi=Disc_s/(-2pi i s^3)=-U_phiphi/(2pi s^3)", factor_by_id["NORM4989_03_raw_cut_coordinate"]["equation"])
    add(checks, "master_factor_two_equation", factor_by_id["NORM4989_04_real_master"]["equation"] == "R_master=-U_total/(pi s^3)-D1 ReF1=2 sum_i D_i-G", factor_by_id["NORM4989_04_real_master"]["equation"])

    kernel_by_quantity = {row["quantity"]: row for row in kernel_rows}
    add(checks, "D1_multiplier_sixteen", kernel_by_quantity["G=D1 ReF1"]["exact_expression"] == "16 ReF1", kernel_by_quantity["G=D1 ReF1"]["exact_expression"])
    expected_g0 = -sp.Rational(32, 1) / PI * (
        sp.Rational(23, 15) * (x**3 * sp.log(x) + (1 - x) ** 3 * sp.log(1 - x))
        + sp.Rational(1, 30) * x * (1 - x) * (sp.log(x) + sp.log(1 - x))
    )
    recorded_g0 = parse(kernel_by_quantity["G0(x)"]["exact_expression"])
    recorded_gL = parse(kernel_by_quantity["coefficient_L[G]"]["exact_expression"])
    recorded_disc = parse(kernel_by_quantity["Disc_s G/(-2pi i s^3)"]["exact_expression"])
    expected_gL = 144 * x * (1 - x) / PI
    expected_disc = 32 / PI * (sp.Rational(23, 15) - x * (1 - x) / 30)
    add(checks, "G0_symbolic", sp.simplify(recorded_g0 - expected_g0) == 0, str(sp.simplify(recorded_g0 - expected_g0)))
    add(checks, "GL_symbolic", sp.simplify(recorded_gL - expected_gL) == 0, str(sp.simplify(recorded_gL - expected_gL)))
    add(checks, "GL_legendre", sp.simplify(recorded_gL - 24 * (1 - P2) / PI) == 0, str(sp.simplify(recorded_gL - 24 * (1 - P2) / PI)))
    add(checks, "G_discontinuity_symbolic", sp.simplify(recorded_disc - expected_disc) == 0, str(sp.simplify(recorded_disc - expected_disc)))

    randomizer = random.Random(4989)
    mp.mp.dps = 70
    for index in range(20):
        numerator = randomizer.randint(1, 997)
        denominator = randomizer.randint(numerator + 1, 1200)
        value = sp.Rational(numerator, denominator)
        residual = sp.N((recorded_g0 - expected_g0).subs(x, value), 70)
        add(checks, f"G0_rational_event_{index:02d}", abs(residual) < sp.Float("1e-60"), str(residual))

    expected_coefficients = {
        0: sp.Rational(868, 135) / PI,
        2: -sp.Rational(3716, 675) / PI,
        4: -sp.Rational(6, 7) / PI,
        6: -sp.Rational(442, 10125) / PI,
        8: -sp.Rational(8296, 779625) / PI,
        10: -sp.Rational(68, 15015) / PI,
        12: -sp.Rational(331, 135135) / PI,
        14: -sp.Rational(29, 19305) / PI,
        16: -sp.Rational(10978, 11022375) / PI,
        18: -sp.Rational(175528, 251818875) / PI,
        20: -sp.Rational(3362, 6619239) / PI,
    }
    moments_by_spin = {int(row["spin_J"]): row for row in moment_rows}
    for spin in range(0, 22, 2):
        row = moments_by_spin[spin]
        recorded_moment = parse(row["G0_moment"])
        recorded_coefficient = parse(row["G0_legendre_coefficient"])
        recorded_scale_moment = parse(row["G_L_moment"])
        recorded_scale_coefficient = parse(row["G_L_legendre_coefficient"])
        independent_moment = independent_g0_moment(spin)
        independent_scale_moment = independent_gL_moment(spin)
        add(checks, f"moment_J{spin}", sp.simplify(recorded_moment - independent_moment) == 0, str(recorded_moment))
        add(checks, f"coefficient_J{spin}", sp.simplify(recorded_coefficient - (2 * spin + 1) * independent_moment) == 0, str(recorded_coefficient))
        add(checks, f"hardcoded_coefficient_J{spin}", sp.simplify(recorded_coefficient - expected_coefficients[spin]) == 0, str(recorded_coefficient))
        add(checks, f"scale_moment_J{spin}", sp.simplify(recorded_scale_moment - independent_scale_moment) == 0, str(recorded_scale_moment))
        add(checks, f"scale_coefficient_J{spin}", sp.simplify(recorded_scale_coefficient - (2 * spin + 1) * independent_scale_moment) == 0, str(recorded_scale_coefficient))
        if spin >= 4:
            recorded_required = parse(row["remaining_cut_required_L0_coefficient"])
            add(checks, f"higher_J_half_master_J{spin}", sp.simplify(recorded_required - expected_coefficients[spin] / 2) == 0, str(recorded_required))
            add(checks, f"higher_J_scale_zero_J{spin}", recorded_scale_coefficient == 0, str(recorded_scale_coefficient))

    sum_by_id = {row["rule_id"]: row for row in sum_rows}
    expected_sum_values = {
        "SUM4989_01_total_P0_scale": 12 / PI,
        "SUM4989_02_total_P2_scale": -12 / PI,
        "SUM4989_03_scalar_P0_scale": -sp.Rational(2233, 72) / PI,
        "SUM4989_04_scalar_P2_scale": -sp.Rational(203, 1800) / PI,
        "SUM4989_05_remaining_P0_scale": sp.Rational(3097, 72) / PI,
        "SUM4989_06_remaining_P2_scale": -sp.Rational(21397, 1800) / PI,
    }
    for rule_id, expected in expected_sum_values.items():
        recorded = parse(sum_by_id[rule_id]["exact_value"])
        add(checks, f"sum_rule_{rule_id}", sp.simplify(recorded - expected) == 0, str(recorded))
    scalar_d0 = parse(sum_by_id["SUM4989_03_scalar_P0_scale"]["exact_value"])
    scalar_d2 = parse(sum_by_id["SUM4989_04_scalar_P2_scale"]["exact_value"])
    remaining_d0 = parse(sum_by_id["SUM4989_05_remaining_P0_scale"]["exact_value"])
    remaining_d2 = parse(sum_by_id["SUM4989_06_remaining_P2_scale"]["exact_value"])
    add(checks, "P0_total_reassembly", sp.simplify(scalar_d0 + remaining_d0 - 12 / PI) == 0, str(sp.simplify(scalar_d0 + remaining_d0)))
    add(checks, "P2_total_reassembly", sp.simplify(scalar_d2 + remaining_d2 + 12 / PI) == 0, str(sp.simplify(scalar_d2 + remaining_d2)))
    add(checks, "low_spin_owned_by_three_particle", all(sum_by_id[row_id]["support_owner"] == "two three-particle cuts only" for row_id in ("SUM4989_05_remaining_P0_scale", "SUM4989_06_remaining_P2_scale")), "hh excluded from J0,J2")

    hh_by_id = {row["support_id"]: row for row in hh_rows}
    add(checks, "hh_internal_difference_four", hh_by_id["HH4989_02_internal_difference"]["exact_value"] == "abs(lambda_hh)=abs(2-(-2))=4", hh_by_id["HH4989_02_internal_difference"]["exact_value"])
    add(checks, "hh_wigner_minimum_J_four", hh_by_id["HH4989_03_wigner_selection"]["exact_value"] == "d^J_{0,4}=0 for J<4", hh_by_id["HH4989_03_wigner_selection"]["exact_value"])
    add(checks, "hh_same_helicity_zero", hh_by_id["HH4989_04_same_helicity_zero"]["exact_value"] == "M_tree(phi,+,+,phi)=0", hh_by_id["HH4989_04_same_helicity_zero"]["exact_value"])
    add(checks, "hh_low_J_claim_true", all(truth(row["valid_for_low_J_zero_claim"]) for row in hh_rows), "all six support rows")
    add(checks, "hh_numeric_claim_false", all(not truth(row["valid_for_numeric_hh_cut_claim"]) for row in hh_rows), "higher-J amplitude remains open")
    add(checks, "hh_result_minimum_J", result["hh_support"]["minimum_J"] == 4, str(result["hh_support"]["minimum_J"]))
    add(checks, "hh_result_J0_zero", result["hh_support"]["J0_zero"] is True, str(result["hh_support"]["J0_zero"]))
    add(checks, "hh_result_J2_zero", result["hh_support"]["J2_zero"] is True, str(result["hh_support"]["J2_zero"]))
    add(checks, "hh_direct_K_zero", result["hh_support"]["direct_K_mu_K_ang_contribution_zero"] is True, str(result["hh_support"]["direct_K_mu_K_ang_contribution_zero"]))

    affine_by_quantity = {row["quantity"]: row for row in affine_rows}
    d0_scalar = 143 * (120 * PI**2 + 1397) / (6480 * PI)
    d2_scalar = (-621877 + 103800 * PI**2) / (162000 * PI)
    g0_coefficient = 868 / (135 * PI)
    g2_coefficient = -3716 / (675 * PI)
    expected_R0 = sp.factor(2 * (d0_scalar + r0) - g0_coefficient)
    expected_R2 = sp.factor(2 * (d2_scalar + r2) - g2_coefficient)
    expected_Kmu = sp.factor(-6 * (expected_R0 - 5 * expected_R2))
    expected_Kang = sp.factor(expected_R0 + 7 * expected_R2)
    recorded_R0 = parse(affine_by_quantity["R0"]["exact_expression"])
    recorded_R2 = parse(affine_by_quantity["R2"]["exact_expression"])
    recorded_Kmu = parse(affine_by_quantity["K_mu"]["exact_expression"])
    recorded_Kang = parse(affine_by_quantity["K_ang"]["exact_expression"])
    add(checks, "affine_R0", sp.simplify(recorded_R0 - expected_R0) == 0, str(recorded_R0))
    add(checks, "affine_R2", sp.simplify(recorded_R2 - expected_R2) == 0, str(recorded_R2))
    add(checks, "affine_Kmu", sp.simplify(recorded_Kmu - expected_Kmu) == 0, str(recorded_Kmu))
    add(checks, "affine_Kang", sp.simplify(recorded_Kang - expected_Kang) == 0, str(recorded_Kang))
    add(checks, "Kmu_r0_slope", sp.diff(recorded_Kmu, r0) == -12, str(sp.diff(recorded_Kmu, r0)))
    add(checks, "Kmu_r2_slope", sp.diff(recorded_Kmu, r2) == 60, str(sp.diff(recorded_Kmu, r2)))
    add(checks, "Kang_r0_slope", sp.diff(recorded_Kang, r0) == 2, str(sp.diff(recorded_Kang, r0)))
    add(checks, "Kang_r2_slope", sp.diff(recorded_Kang, r2) == 14, str(sp.diff(recorded_Kang, r2)))
    expected_Kmu_known = (-89221 + 1500 * PI**2) / (225 * PI)
    expected_Kang_known = 2 * (67537 + 24075 * PI**2) / (3375 * PI)
    add(checks, "Kmu_known_intercept", sp.simplify(recorded_Kmu.subs({r0: 0, r2: 0}) - expected_Kmu_known) == 0, str(recorded_Kmu.subs({r0: 0, r2: 0})))
    add(checks, "Kang_known_intercept", sp.simplify(recorded_Kang.subs({r0: 0, r2: 0}) - expected_Kang_known) == 0, str(recorded_Kang.subs({r0: 0, r2: 0})))

    gates = {row["gate"]: truth(row["passed"]) for row in gate_rows}
    expected_open = {
        "hh_numeric_higher_J",
        "mixed_hhh_cut_numeric",
        "phiphih_cut_numeric",
        "numeric_full_K_mu",
        "numeric_full_K_ang",
        "finite_C_w",
        "exact_all_operator_local_GR",
        "full_MTS",
    }
    add(checks, "open_gate_set", {name for name, passed in gates.items() if not passed} == expected_open, json.dumps(sorted(name for name, passed in gates.items() if not passed)))
    add(checks, "nine_closed_gates", sum(gates.values()) == 9, str(sum(gates.values())))
    add(checks, "numeric_full_K_mu_false", result["numeric_full_K_mu"] is False, str(result["numeric_full_K_mu"]))
    add(checks, "numeric_full_K_ang_false", result["numeric_full_K_ang"] is False, str(result["numeric_full_K_ang"]))
    add(checks, "exact_local_GR_false", result["exact_all_operator_local_GR"] is False, str(result["exact_all_operator_local_GR"]))
    add(checks, "full_MTS_false", result["full_MTS"] is False, str(result["full_MTS"]))

    for table_name, rows in tables.items():
        for row_index, row in enumerate(rows):
            if row.get("source_path"):
                add(checks, f"row_source_exists_{table_name}_{row_index}", (ROOT / row["source_path"]).exists(), row["source_path"])
    for path in files[:-1]:
        text = path.read_text(encoding="utf-8")
        add(checks, f"no_missing_marker_{path.stem}", "MISSING_" not in text, path.name)

    write_validation(checks)
    passed = sum(bool(row["passed"]) for row in checks)
    VALIDATION_PROVENANCE.write_text(
        "\n".join(
            [
                "# 4989 independent validation provenance",
                "",
                f"Marker: `{VALIDATION_MARKER}`.",
                "",
                "The validator does not import the generator. It independently reconstructs the D1 channel kernel, checks twenty rational events, derives eleven exact Legendre moments from polynomial-log integrals, hard-codes the resulting J=0 through J=20 tower, reassembles both scale sum rules, proves the affine K-coordinate slopes, checks the helicity-support reduction, verifies every source hash and row source, and enforces all numeric-full-invariant nonclaim gates.",
                "",
                f"Passed: `{passed}/{len(checks)}`.",
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
