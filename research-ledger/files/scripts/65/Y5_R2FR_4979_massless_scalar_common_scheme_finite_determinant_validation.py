from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4979"
VALIDATION_DIR = POST / "source-intake" / "mts_residuals"
VALIDATION = VALIDATION_DIR / "P8_Y5_BRR545_4979_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

RUNNER = POST / "scripts" / "Y5_R2FR_4979_massless_scalar_common_scheme_finite_determinant.py"
VALIDATOR = POST / "scripts" / "Y5_R2FR_4979_massless_scalar_common_scheme_finite_determinant_validation.py"
CHECKPOINT_DOC = POST / "4979-Y5-R2FR-massless-scalar-common-scheme-finite-determinant-and-TT-match.md"
FORMAL_NOTE = FORMAL / "995-PPC4161-massless-scalar-common-scheme-finite-TT-determinant.md"
CURRENT_RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CURRENT_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
VARIABLE_AUDIT = FORMAL / "04-variable-audit.csv"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
EQUATION_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION_SPINE = FORMAL / "07-unification-spine.md"

FORMULA = SOURCE / "massless_scalar_MSbar_shell_formulas.csv"
INTEGRAND = SOURCE / "massless_scalar_exact_integrand_crosscheck.csv"
TWO_POINT = SOURCE / "massless_scalar_two_point_scheme_map.csv"
TT_MATCH = SOURCE / "massless_scalar_TT_finite_determinant_match.csv"
TRACEFUL = SOURCE / "massless_scalar_traceful_continuation_audit.csv"
IDENTITIES = SOURCE / "massless_scalar_finite_determinant_identities.csv"
GATE = SOURCE / "massless_scalar_finite_determinant_gate.csv"
RESULT = SOURCE / "massless_scalar_finite_determinant_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
PREDECESSOR = POST / "source-intake" / "functional_rg" / "4978" / "scalar_TTT_assembly_results.json"

MARKER = "MTS_4979_MASSLESS_SCALAR_COMMON_SCHEME_FINITE_DETERMINANT_VALIDATION"
FORMAL_MARKER = "PPC4161_MASSLESS_SCALAR_COMMON_SCHEME_FINITE_TT_4979"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_width_valid(path: Path) -> bool:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.reader(handle))
    return bool(rows) and all(len(row) == len(rows[0]) for row in rows)


def contains(path: Path, text: str) -> bool:
    return path.exists() and text in path.read_text(
        encoding="utf-8", errors="replace"
    )


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError):
        return False
    return True


def finite_rows(rows: list[dict[str, str]], fields: tuple[str, ...]) -> bool:
    try:
        return all(
            math.isfinite(float(row[field])) for row in rows for field in fields
        )
    except (KeyError, TypeError, ValueError):
        return False


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-30)


def no_claim_rows(rows: list[dict[str, str]]) -> bool:
    return all(
        row.get("valid_for_full_MTS_claim", "").lower() == "false"
        for row in rows
    )


def path_scope_valid() -> bool:
    completed = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode == 0:
        for line in completed.stdout.splitlines():
            path = line[3:].strip().replace("\\", "/")
            if " -> " in path:
                path = path.split(" -> ", 1)[1]
            if not (
                path.startswith("post-checkpoint-work/")
                or path.startswith("formalization-workbench/")
            ):
                return False
        return True
    allowlisted = (
        RUNNER,
        VALIDATOR,
        CHECKPOINT_DOC,
        FORMAL_NOTE,
        CURRENT_RESUME,
        CURRENT_SPINE,
        VARIABLE_AUDIT,
        CLAIMS_REGISTER,
        EQUATION_REGISTER,
        RED_TEAM,
        UNIFICATION_SPINE,
        SOURCE,
        VALIDATION,
    )
    roots = (POST.resolve(), FORMAL.resolve())
    return all(
        any(path.resolve().is_relative_to(root) for root in roots)
        for path in allowlisted
    )


def main() -> int:
    checks: list[dict[str, Any]] = []

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append(
            {
                "check": name,
                "passed": bool(passed),
                "detail": detail,
                "checkpoint_marker": MARKER,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": "2026-07-13",
            }
        )

    output_csvs = (
        FORMULA,
        INTEGRAND,
        TWO_POINT,
        TT_MATCH,
        TRACEFUL,
        IDENTITIES,
        GATE,
    )
    required_paths = (
        RUNNER,
        VALIDATOR,
        CHECKPOINT_DOC,
        FORMAL_NOTE,
        CURRENT_RESUME,
        CURRENT_SPINE,
        VARIABLE_AUDIT,
        CLAIMS_REGISTER,
        EQUATION_REGISTER,
        RED_TEAM,
        UNIFICATION_SPINE,
        RESULT,
        PROVENANCE,
        PREDECESSOR,
        *output_csvs,
    )
    check(
        "V01_required_paths_exist",
        all(path.exists() for path in required_paths),
        f"{len(required_paths)} paths",
    )
    check("V02_runner_compiles", compiles(RUNNER), str(RUNNER))
    check("V03_validator_compiles", compiles(VALIDATOR), str(VALIDATOR))
    check("V04_checkpoint_marker", contains(CHECKPOINT_DOC, FORMAL_MARKER), FORMAL_MARKER)
    check("V05_formal_note_marker", contains(FORMAL_NOTE, FORMAL_MARKER), FORMAL_MARKER)
    check("V06_resume_marker", contains(CURRENT_RESUME, FORMAL_MARKER), FORMAL_MARKER)
    check("V07_spine_marker", contains(CURRENT_SPINE, FORMAL_MARKER), FORMAL_MARKER)
    check("V08_equation_marker", contains(EQUATION_REGISTER, FORMAL_MARKER), FORMAL_MARKER)
    check("V09_red_team_marker", contains(RED_TEAM, FORMAL_MARKER), FORMAL_MARKER)
    check("V10_unification_marker", contains(UNIFICATION_SPINE, FORMAL_MARKER), FORMAL_MARKER)

    predecessor = json.loads(PREDECESSOR.read_text(encoding="utf-8"))
    check(
        "V11_predecessor_source_TTT",
        predecessor["valid_for_complete_free_scalar_source_metric_TTT"] is True,
        "4978 source response valid",
    )
    check(
        "V12_predecessor_UV_match",
        predecessor["valid_for_direct_determinant_UV_log_match"] is True,
        "4978 direct UV match valid",
    )
    check(
        "V13_predecessor_finite_open",
        predecessor["valid_for_independent_renormalized_determinant_match"] is False,
        "4979 starts from an open finite comparison",
    )

    formula_rows = read_csv(FORMULA)
    integrand_rows = read_csv(INTEGRAND)
    two_point_rows = read_csv(TWO_POINT)
    tt_rows = read_csv(TT_MATCH)
    traceful_rows = read_csv(TRACEFUL)
    identity_rows = read_csv(IDENTITIES)
    gate_rows = read_csv(GATE)
    result = json.loads(RESULT.read_text(encoding="utf-8"))

    check("V14_formula_shape", len(formula_rows) == 4, "k=0,1,2,3")
    check(
        "V15_formula_keys",
        {int(row["radial_power_k"]) for row in formula_rows} == {0, 1, 2, 3},
        "complete radial powers",
    )
    check(
        "V16_formula_poles",
        formula_rows[0]["one_over_epsilon_pole_without_1_over_4pi2"] == "0"
        and "E1/4" in formula_rows[1]["one_over_epsilon_pole_without_1_over_4pi2"]
        and "-E2 Delta/8" in formula_rows[2]["one_over_epsilon_pole_without_1_over_4pi2"]
        and "E3 Delta^2/32" in formula_rows[3]["one_over_epsilon_pole_without_1_over_4pi2"],
        "exact universal residues",
    )

    check("V17_integrand_shape", len(integrand_rows) == 2, "two external scales")
    check(
        "V18_integrand_numeric",
        finite_rows(
            integrand_rows,
            (
                "external_scale",
                "maximum_exact_integrand",
                "maximum_absolute_residual",
                "relative_residual",
                "inverse_propagator_residual",
            ),
        ),
        "all finite",
    )
    max_integrand = max(float(row["relative_residual"]) for row in integrand_rows)
    max_inverse = max(
        float(row["inverse_propagator_residual"]) for row in integrand_rows
    )
    check("V19_integrand_precision", max_integrand < 1.0e-12, f"max={max_integrand:.17g}")
    check("V20_inverse_precision", max_inverse < 1.0e-12, f"max={max_inverse:.17g}")

    check("V21_two_point_shape", len(two_point_rows) == 4, "four invariant coefficients")
    expected_two_point = {
        "Ricci_log_q2_over_mu2": 1.0 / 60.0,
        "Ricci_finite_local": -23.0 / 450.0,
        "R_log_q2_over_mu2": 1.0 / 120.0,
        "R_finite_local": -1.0 / 1800.0,
    }
    expected_source = {
        "Ricci_log_q2_over_mu2": -1.0 / 60.0,
        "Ricci_finite_local": 4.0 / 225.0,
        "R_log_q2_over_mu2": -1.0 / 120.0,
        "R_finite_local": -29.0 / 1800.0,
    }
    check(
        "V22_two_point_exact_coefficients",
        all(
            math.isclose(
                float(row["exact_covariant_W_MSbar"]),
                expected_two_point[row["coefficient"]],
                rel_tol=1.0e-14,
                abs_tol=1.0e-16,
            )
            for row in two_point_rows
        ),
        "exact rationals",
    )
    check(
        "V23_two_point_fitted_coefficients",
        all(
            relative_error(
                float(row["fitted_covariant_W_MSbar"]),
                expected_two_point[row["coefficient"]],
            )
            < 1.0e-8
            for row in two_point_rows
        ),
        "independent numerical projection",
    )
    check(
        "V24_source_coefficients_reconstructed",
        all(
            math.isclose(
                float(row["source_minus_W_coefficient"]),
                expected_source[row["coefficient"]],
                rel_tol=1.0e-14,
                abs_tol=1.0e-16,
            )
            for row in two_point_rows
        ),
        "source(-W)=shell-W",
    )
    check(
        "V25_scheme_identity_recorded",
        all(row["scheme_identity"] == "source(-W)=UV_shell-W_MSbar" for row in two_point_rows),
        "one common scheme",
    )

    check("V26_TT_shape", len(tt_rows) == 4, "four unseen TT geometries")
    check(
        "V27_TT_keys",
        {row["geometry_id"] for row in tt_rows} == {"TT00", "TT01", "TT02", "TT03"},
        "deterministic fresh controls",
    )
    check(
        "V28_TT_numeric",
        finite_rows(
            tt_rows,
            (
                "trace_residual",
                "transverse_residual",
                "source_minus_W_density",
                "source_UV_shell_density",
                "direct_W_MSbar_low",
                "direct_W_MSbar_high",
                "direct_target_shell_minus_source",
                "source_reconstructed_shell_minus_direct",
                "absolute_match_residual",
                "relative_match_residual",
                "quadrature_residual",
                "UV_shell_residual",
            ),
        ),
        "all finite",
    )
    max_projector = max(
        max(float(row["trace_residual"]), float(row["transverse_residual"]))
        for row in tt_rows
    )
    check("V29_TT_projectors", max_projector < 1.0e-12, f"max={max_projector:.17g}")
    check(
        "V30_TT_target_identity",
        all(
            math.isclose(
                float(row["direct_target_shell_minus_source"]),
                float(row["source_UV_shell_density"])
                - float(row["source_minus_W_density"]),
                rel_tol=1.0e-14,
                abs_tol=1.0e-17,
            )
            for row in tt_rows
        ),
        "target=shell-source",
    )
    check(
        "V31_TT_source_reconstruction",
        all(
            math.isclose(
                float(row["source_reconstructed_shell_minus_direct"]),
                float(row["source_UV_shell_density"])
                - float(row["direct_W_MSbar_high"]),
                rel_tol=1.0e-14,
                abs_tol=1.0e-17,
            )
            for row in tt_rows
        ),
        "source=shell-direct",
    )
    max_tt_absolute = max(float(row["absolute_match_residual"]) for row in tt_rows)
    max_tt_relative = max(float(row["relative_match_residual"]) for row in tt_rows)
    max_tt_quadrature = max(float(row["quadrature_residual"]) for row in tt_rows)
    max_tt_shell = max(float(row["UV_shell_residual"]) for row in tt_rows)
    check("V32_TT_absolute_match", max_tt_absolute < 5.0e-15, f"max={max_tt_absolute:.17g}")
    check("V33_TT_relative_match", max_tt_relative < 1.0e-8, f"max={max_tt_relative:.17g}")
    check("V34_TT_quadrature", max_tt_quadrature < 1.0e-7, f"max={max_tt_quadrature:.17g}")
    check("V35_TT_UV_shell", max_tt_shell < 1.0e-10, f"max={max_tt_shell:.17g}")
    check(
        "V36_TT_no_geometry_fit",
        all(row["status"] == "unfitted_common_scheme_TT_finite_match" for row in tt_rows),
        "one two-point-owned scheme",
    )

    check("V37_identity_shape", len(identity_rows) == 8, "four mu plus four scale")
    check(
        "V38_identity_groups",
        {row["identity"] for row in identity_rows}
        == {"mu_rescaling_W_MSbar", "common_momentum_mu_scaling"},
        "declared identities",
    )
    max_identity = max(float(row["relative_residual"]) for row in identity_rows)
    check("V39_identity_precision", max_identity < 1.0e-12, f"max={max_identity:.17g}")

    check("V40_traceful_shape", len(traceful_rows) == 2, "G03 and G04")
    check(
        "V41_traceful_keys",
        {row["geometry_id"] for row in traceful_rows} == {"G03", "G04"},
        "predeclared controls",
    )
    check(
        "V42_traceful_numeric",
        finite_rows(
            traceful_rows,
            (
                "source_minus_W_density",
                "source_UV_shell_density",
                "direct_target_shell_minus_source",
                "four_dimensional_W_MSbar",
                "product_continuation_W_MSbar",
                "product_triangle_evanescent",
                "product_pair_contact_evanescent",
                "continuation_difference",
                "absolute_product_target_mismatch",
                "relative_product_target_mismatch",
            ),
        ),
        "all finite",
    )
    min_continuation = min(float(row["continuation_difference"]) for row in traceful_rows)
    max_trace_mismatch = max(float(row["relative_product_target_mismatch"]) for row in traceful_rows)
    check("V43_continuation_active", min_continuation > 1.0e-8, f"min={min_continuation:.17g}")
    check("V44_trace_residual_nonzero", max_trace_mismatch > 1.0e-2, f"max={max_trace_mismatch:.17g}")
    check(
        "V45_traceful_claim_false",
        all(row["valid_for_complete_traceful_finite_match"].lower() == "false" for row in traceful_rows),
        "no complete traceful promotion",
    )
    check(
        "V46_pair_contacts_retained",
        all(abs(float(row["product_pair_contact_evanescent"])) > 1.0e-8 for row in traceful_rows),
        "evanescent determinant-volume contacts nonzero",
    )

    check(
        "V47_runner_gates",
        len(gate_rows) == 16 and all(row["passed"].lower() == "true" for row in gate_rows),
        "16/16",
    )
    check(
        "V48_result_counts",
        result["gate_pass_count"] == result["gate_count"] == 16
        and result["TT_geometry_count"] == 4,
        "production result",
    )
    check(
        "V49_integrand_flag",
        result["valid_for_exact_massless_triangle_integrand"] is True,
        "exact integrand promoted",
    )
    check(
        "V50_scheme_flag",
        result["valid_for_two_point_common_scheme_map"] is True,
        "two-point map promoted",
    )
    check(
        "V51_TT_flag",
        result["valid_for_TT_common_scheme_finite_determinant_match"] is True,
        "TT finite match promoted",
    )
    check(
        "V52_traceful_flag_false",
        result["valid_for_complete_traceful_common_scheme_finite_determinant_match"] is False,
        "generic trace contact open",
    )
    check(
        "V53_full_MTS_false",
        result["valid_for_full_MTS_claim"] is False,
        "full MTS false",
    )

    expected_variables = {
        "ExactScalarTriangle4979_MTS",
        "MSbarFiniteMoments4979_MTS",
        "ScalarSchemeMap4979_MTS",
        "ScalarTTFiniteMatch4979_MTS",
        "TraceContactResidual4979_MTS",
        "PredictivityStatus4979_MTS",
    }
    variable_rows = read_csv(VARIABLE_AUDIT)
    check(
        "V54_variable_rows",
        expected_variables.issubset({row["symbol"] for row in variable_rows}),
        "six 4979 variables",
    )
    claim_rows = read_csv(CLAIMS_REGISTER)
    claim = next((row for row in claim_rows if row["claim_id"] == "L-821"), None)
    check("V55_claim_row", claim is not None, "L-821")
    check(
        "V56_claim_nonclaim",
        claim is not None and "private_nonclaim" in claim["status"],
        "TT promotion with trace guard",
    )
    check(
        "V57_claim_trace_guard",
        claim is not None
        and "trace" in claim["key_risk"].lower()
        and "Gauss" in claim["next_test"],
        "trace/Gauss-Bonnet residual retained",
    )

    all_output_rows = [read_csv(path) for path in output_csvs]
    check(
        "V58_all_rows_nonclaim",
        all(no_claim_rows(rows) for rows in all_output_rows),
        "valid_for_full_MTS_claim=false",
    )
    check(
        "V59_csv_widths",
        all(
            csv_width_valid(path)
            for path in (*output_csvs, VARIABLE_AUDIT, CLAIMS_REGISTER)
        ),
        "all CSV rows parse",
    )
    check(
        "V60_no_missing_markers",
        not any(
            "MISSING_" in path.read_text(encoding="utf-8", errors="replace")
            for path in (*output_csvs, RESULT, CHECKPOINT_DOC, FORMAL_NOTE)
        ),
        "no placeholders",
    )
    check("V61_runner_hash", contains(PROVENANCE, digest(RUNNER)), digest(RUNNER))
    check("V62_path_scope", path_scope_valid(), "post-checkpoint-work and formalization-workbench only")
    check(
        "V63_no_pycache",
        not any((POST / "scripts").glob("__pycache__")),
        "scripts/__pycache__ absent",
    )

    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    fields = list(checks[0])
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(checks)
    passed = sum(bool(row["passed"]) for row in checks)
    VALIDATION_PROVENANCE.write_text(
        f"""# Checkpoint 4979 validation provenance

Marker: `{MARKER}`

- validator: `{VALIDATOR.relative_to(ROOT).as_posix()}`
- validator SHA256: `{digest(VALIDATOR)}`
- runner SHA256: `{digest(RUNNER)}`
- checks passed: `{passed}/{len(checks)}`
- exact triangle integrand: `{result['valid_for_exact_massless_triangle_integrand']}`
- common two-point scheme map: `{result['valid_for_two_point_common_scheme_map']}`
- TT finite determinant match: `{result['valid_for_TT_common_scheme_finite_determinant_match']}`
- complete traceful finite match: `{result['valid_for_complete_traceful_common_scheme_finite_determinant_match']}`
- full MTS: `{result['valid_for_full_MTS_claim']}`
""",
        encoding="utf-8",
    )
    print(f"4979 validation {passed}/{len(checks)}", flush=True)
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
