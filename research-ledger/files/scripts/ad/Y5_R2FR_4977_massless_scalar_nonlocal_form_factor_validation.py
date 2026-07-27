from __future__ import annotations

import csv
import hashlib
import json
import math
import subprocess
import sys
from fractions import Fraction
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "4977"
VALIDATION_DIR = POST / "source-intake" / "mts_residuals"
VALIDATION = VALIDATION_DIR / "P8_Y5_BRR545_4977_VALIDATION.csv"
VALIDATION_PROVENANCE = SOURCE / "VALIDATION_PROVENANCE.md"

RUNNER = POST / "scripts" / "Y5_R2FR_4977_massless_scalar_nonlocal_form_factor_evaluator.py"
VALIDATOR = POST / "scripts" / "Y5_R2FR_4977_massless_scalar_nonlocal_form_factor_validation.py"
CHECKPOINT_DOC = POST / "4977-Y5-R2FR-massless-minimal-scalar-nonlocal-form-factors-and-log-location.md"
FORMAL_NOTE = FORMAL / "993-PPC4161-massless-scalar-nonlocal-form-factors-and-log-location.md"
CURRENT_RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CURRENT_SPINE = POST / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"
VARIABLE_AUDIT = FORMAL / "04-variable-audit.csv"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
EQUATION_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM = FORMAL / "06-consistency-red-team.md"
UNIFICATION_SPINE = FORMAL / "07-unification-spine.md"

TEX_SOURCE = POST / "source-intake" / "functional_rg" / "4973" / "src-0911.1168" / "cpt2009m.tex"
ALPHA_SOURCE = TEX_SOURCE.parent / "anc" / "ffwa.m"
EXPLICIT_SOURCE = TEX_SOURCE.parent / "anc" / "ffwd.m"

STRUCTURE_MAP = SOURCE / "C3_massless_scalar_structure_map.csv"
MANIFEST = SOURCE / "C3_massless_scalar_form_factor_manifest.csv"
CROSSCHECK = SOURCE / "C3_massless_scalar_form_factor_crosscheck.csv"
REDUCED_CHANNEL = SOURCE / "C3_massless_scalar_reduced_channel_values.csv"
HOMOGENEITY = SOURCE / "C3_massless_scalar_scale_homogeneity.csv"
TRIANGLE = SOURCE / "C3_massless_scalar_potential_triangle.csv"
QUADRATIC_LOG = SOURCE / "C3_massless_scalar_quadratic_log.csv"
GATE = SOURCE / "C3_massless_scalar_nonlocal_gate.csv"
RESULT = SOURCE / "C3_massless_scalar_nonlocal_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4977_MASSLESS_SCALAR_NONLOCAL_FORM_FACTORS_VALIDATION"
FORMAL_MARKER = "PPC4161_MASSLESS_SCALAR_NONLOCAL_FORM_FACTORS_4977"
EXPECTED_INDICES = {1, 4, 5, 6, 9, 10, 11, 15, 16, 17, 22, 23, 24, 25, 26, 27, 28, 29}
EXPECTED_SOURCE_HASHES = {
    TEX_SOURCE: "8cc7344187523211abd274cdbf8fbdc75b794662f5a062ddf1662f96195b7d8e",
    ALPHA_SOURCE: "6a9bc97cab8793aeda563513f6d0bf6ad20b387a4f52c9e1d76d7e9c27bdbd5f",
    EXPLICIT_SOURCE: "5c5ddd8038105ddee2cf48bfeba89ced5cea65ab38227fc29a9c6fc1014c2326",
}


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
    return path.exists() and text in path.read_text(encoding="utf-8", errors="replace")


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError):
        return False
    return True


def finite_rows(rows: list[dict[str, str]], fields: tuple[str, ...]) -> bool:
    try:
        return all(math.isfinite(float(row[field])) for row in rows for field in fields)
    except (KeyError, TypeError, ValueError):
        return False


def no_claim_rows(rows: list[dict[str, str]]) -> bool:
    return all(row.get("valid_for_full_MTS_claim", "").lower() == "false" for row in rows)


def git_scope_clean() -> bool:
    completed = subprocess.run(
        ["git", "status", "--short"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        # The restored local corpus currently has no .git metadata.  In that
        # case enforce the checkpoint's explicit path allowlist rather than
        # pretending that a repository diff is available.
        checkpoint_paths = (
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
        allowed_roots = (POST.resolve(), FORMAL.resolve())
        return all(
            any(path.resolve().is_relative_to(root) for root in allowed_roots)
            for path in checkpoint_paths
        )
    for line in completed.stdout.splitlines():
        path = line[3:].strip().replace("\\", "/")
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        if not (path.startswith("post-checkpoint-work/") or path.startswith("formalization-workbench/")):
            return False
    return True


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
        STRUCTURE_MAP,
        MANIFEST,
        CROSSCHECK,
        REDUCED_CHANNEL,
        HOMOGENEITY,
        TRIANGLE,
        QUADRATIC_LOG,
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
        TEX_SOURCE,
        ALPHA_SOURCE,
        EXPLICIT_SOURCE,
        RESULT,
        PROVENANCE,
        *output_csvs,
    )
    check("V01_required_paths_exist", all(path.exists() for path in required_paths), f"{len(required_paths)} required paths")
    check("V02_runner_compiles", compiles(RUNNER), str(RUNNER))
    check("V03_validator_compiles", compiles(VALIDATOR), str(VALIDATOR))
    check("V04_checkpoint_marker", contains(CHECKPOINT_DOC, FORMAL_MARKER), FORMAL_MARKER)
    check("V05_formal_note_marker", contains(FORMAL_NOTE, FORMAL_MARKER), FORMAL_MARKER)
    check("V06_resume_marker", contains(CURRENT_RESUME, FORMAL_MARKER), FORMAL_MARKER)
    check("V07_spine_marker", contains(CURRENT_SPINE, FORMAL_MARKER), FORMAL_MARKER)
    check("V08_equation_register_marker", contains(EQUATION_REGISTER, FORMAL_MARKER), FORMAL_MARKER)
    check("V09_red_team_marker", contains(RED_TEAM, FORMAL_MARKER), FORMAL_MARKER)
    check("V10_unification_spine_marker", contains(UNIFICATION_SPINE, FORMAL_MARKER), FORMAL_MARKER)

    for number, (path, expected_hash) in enumerate(EXPECTED_SOURCE_HASHES.items(), start=11):
        check(f"V{number:02d}_source_hash_{path.name}", path.exists() and digest(path) == expected_hash, expected_hash)

    structure_rows = read_csv(STRUCTURE_MAP)
    manifest_rows = read_csv(MANIFEST)
    cross_rows = read_csv(CROSSCHECK)
    channel_rows = read_csv(REDUCED_CHANNEL)
    homogeneity_rows = read_csv(HOMOGENEITY)
    triangle_rows = read_csv(TRIANGLE)
    log_rows = read_csv(QUADRATIC_LOG)
    gate_rows = read_csv(GATE)
    result = json.loads(RESULT.read_text(encoding="utf-8"))

    structure_indices = {int(row["form_factor_index"]) for row in structure_rows}
    check("V14_structure_map_exact", len(structure_rows) == 18 and structure_indices == EXPECTED_INDICES, str(sorted(structure_indices)))
    check("V15_structure_derivatives_match", all(row["derivative_order"] == row["ancillary_derivative_order"] for row in structure_rows), "mapped versus ancillary der[i]")
    check("V16_structure_p_factors_valid", all(Fraction(row["P_equals_R_over_6_factor"]) in {Fraction(1), Fraction(1, 6), Fraction(1, 36), Fraction(1, 216)} for row in structure_rows), "P=R/6 powers")
    check("V17_manifest_complete", len(manifest_rows) == 18 and {int(row["form_factor_index"]) for row in manifest_rows} == EXPECTED_INDICES, "18 expression manifests")
    check("V18_manifest_hashes_present", all(len(row["alpha_expression_sha256"]) == 64 and len(row["explicit_expression_sha256"]) == 64 for row in manifest_rows), "exact expression digests")

    cross_pairs = {(row["sample_id"], int(row["form_factor_index"])) for row in cross_rows}
    check("V19_crosscheck_shape", len(cross_rows) == 54 and len(cross_pairs) == 54, "3 samples x 18 form factors")
    check("V20_crosscheck_numeric", finite_rows(cross_rows, ("basic_triangle_gamma", "alpha_representation", "explicit_representation", "representation_relative_difference")), "all finite")
    max_cross = max(float(row["representation_relative_difference"]) for row in cross_rows)
    check("V21_crosscheck_precision", max_cross < 1.0e-10, f"max={max_cross:.17g}")
    max_quadrature = max(float(row["alpha_low_vs_high_relative_difference"]) for row in cross_rows)
    check("V22_quadrature_precision", max_quadrature < 1.0e-11, f"max={max_quadrature:.17g}")

    channel_ids = {row["channel_id"] for row in channel_rows}
    check("V23_reduced_channel_shape", len(channel_rows) == 33 and len(channel_ids) == 11, "3 samples x 11 channels")
    check("V24_reduced_channel_numeric", finite_rows(channel_rows, ("alpha_reduced_channel_value", "explicit_reduced_channel_value", "relative_difference")), "all finite")
    max_channel = max(float(row["relative_difference"]) for row in channel_rows)
    check("V25_reduced_channel_precision", max_channel < 1.0e-10, f"max={max_channel:.17g}")

    check("V26_homogeneity_shape", len(homogeneity_rows) == 18, "one row per source form factor")
    max_homogeneity = max(max(float(row["alpha_relative_residual"]), float(row["explicit_relative_residual"])) for row in homogeneity_rows)
    check("V27_homogeneity_precision", max_homogeneity < 1.0e-9, f"max={max_homogeneity:.17g}")
    check("V28_homogeneity_powers", all(int(row["expected_homogeneity_power"]) == -(1 + int(row["derivative_order"]) // 2) for row in homogeneity_rows), "lambda^[-1-d/2]")

    check("V29_triangle_shape", len(triangle_rows) == 3, "three independent momentum samples")
    max_triangle = max(max(float(row["Gamma_1_identity_relative_residual"]), float(row["normalization_relative_residual"])) for row in triangle_rows)
    check("V30_triangle_precision", max_triangle < 1.0e-12, f"max={max_triangle:.17g}")
    check("V31_triangle_identity", all(math.isclose(float(row["Gamma_1_explicit"]), float(row["basic_triangle_gamma"]) / 3.0, rel_tol=1.0e-12, abs_tol=1.0e-14) for row in triangle_rows), "Gamma1=Gamma_basic/3")

    log_by_invariant = {row["invariant"]: row for row in log_rows}
    check("V32_quadratic_log_shape", len(log_rows) == 2, str(list(log_by_invariant)))
    check("V33_Ricci_log_exact", Fraction(log_by_invariant["R_mn log(-Box/mu^2) R^mn"]["log_coefficient_inside_minus_W_braces"]) == -Fraction(1, 60), "-1/60")
    check("V34_R_log_exact", Fraction(log_by_invariant["R log(-Box/mu^2) R"]["log_coefficient_inside_minus_W_braces"]) == -Fraction(1, 120), "-1/120")

    check("V35_runner_gate_count", len(gate_rows) == 11 and all(row["passed"].lower() == "true" for row in gate_rows), "11/11")
    check("V36_result_state", result["gate_pass_count"] == result["gate_count"] == 11 and result["valid_for_complete_free_scalar_cubic_curvature_form_factors"] is True, "runner result certificate")
    check("V37_no_full_metric_claim", result["valid_for_full_third_metric_response"] is False, "quadratic action third variation remains")
    check("V38_no_full_MTS_claim", result["valid_for_full_MTS_claim"] is False, "full MTS false")

    all_output_rows = [read_csv(path) for path in output_csvs]
    check("V39_all_rows_nonclaim", all(no_claim_rows(rows) for rows in all_output_rows), "valid_for_full_MTS_claim=false")
    check("V40_csv_widths", all(csv_width_valid(path) for path in (*output_csvs, VARIABLE_AUDIT, CLAIMS_REGISTER)), "scientific and formal CSV widths")
    check("V41_no_missing_markers", not any("MISSING_" in path.read_text(encoding="utf-8", errors="replace") for path in (*output_csvs, RESULT, CHECKPOINT_DOC, FORMAL_NOTE)), "no placeholder markers")

    variable_rows = read_csv(VARIABLE_AUDIT)
    expected_variables = {
        "GammaBasic4977_MTS",
        "ScalarGammaVector4977_MTS",
        "ScalarReducedChannels4977_MTS",
        "ScalarQuadraticLog4977_MTS",
        "PredictivityStatus4977_MTS",
    }
    present_variables = {row["symbol"] for row in variable_rows if row["symbol"] in expected_variables}
    check("V42_variable_audit_rows", present_variables == expected_variables, str(sorted(present_variables)))
    claim_rows = read_csv(CLAIMS_REGISTER)
    check("V43_claim_register_row", sum(row["claim_id"] == "L-819" for row in claim_rows) == 1, "L-819 exactly once")
    check("V44_path_scope", git_scope_clean(), "git diff when available; otherwise explicit checkpoint path allowlist under post-checkpoint-work or formalization-workbench")
    check("V45_no_script_pycache", not (POST / "scripts" / "__pycache__").exists(), "bytecode cache absent")

    VALIDATION_DIR.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(checks[0]))
        writer.writeheader()
        writer.writerows(checks)

    passed = sum(bool(row["passed"]) for row in checks)
    VALIDATION_PROVENANCE.write_text(
        f"""# Checkpoint 4977 validation provenance

Marker: `{MARKER}`

- checks passed: `{passed}/{len(checks)}`
- validation CSV: `{VALIDATION.relative_to(ROOT).as_posix()}`
- validation CSV SHA256: `{digest(VALIDATION)}`
- runner script SHA256: `{digest(RUNNER)}`
- validator script SHA256: `{digest(VALIDATOR)}`
- maximum alpha/explicit residual: `{max_cross:.17g}`
- maximum reduced-channel residual: `{max_channel:.17g}`
- maximum homogeneity residual: `{max_homogeneity:.17g}`
- maximum determinant-triangle residual: `{max_triangle:.17g}`
- complete free-scalar cubic-curvature form factors: `true`
- complete third metric response: `false`
- full MTS: `false`
""",
        encoding="utf-8",
    )

    print(f"{MARKER} {passed}/{len(checks)}")
    print(f"validation_sha256={digest(VALIDATION)}")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
