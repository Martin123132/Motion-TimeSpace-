from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
R10 = ROOT / "source-intake" / "r10"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
BRANCH_COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1500-Y5-R10-RAB-reviewed-R10-curve-promotion-gate-or-kernel-derivation-contract.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1499_validation": OUT / "P8_Y5_BRR545_1499_VALIDATION.csv",
    "1499_points": OUT / "P8_Y5_R10_1499_EOTWASH2020_ALPHA_LAMBDA_POINTS_NONCLAIM.csv",
    "1499_quality": OUT / "P8_Y5_R10_1499_POINT_QUALITY_LEDGER.csv",
    "1499_blockers": OUT / "P8_Y5_R10_1499_TARGET_PROMOTION_BLOCKERS.csv",
    "1499_next": OUT / "P8_Y5_R10_1499_NEXT_TARGET.csv",
}

VISUAL_POINTS = R10 / "derived" / "staging" / "R10_EotWash2020_alpha_lambda_VISUAL_NONCLAIM_1499.csv"
CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"
KERNEL_STUB = R10 / "derived" / "staging" / "R10_delta_w_kernel_contract_STUB_NONCLAIM_1500.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

PROMOTION_GATE = OUT / "P8_Y5_R10_1500_R10_CURVE_PROMOTION_GATE.csv"
KERNEL_CONTRACT = OUT / "P8_Y5_R10_1500_DELTA_W_TO_ALPHA_KERNEL_CONTRACT.csv"
KERNEL_STUB_LEDGER = OUT / "P8_Y5_R10_1500_KERNEL_STUB_LEDGER.csv"
EQUATION_REGISTER = OUT / "P8_Y5_R10_1500_R10_EQUATION_CONVENTION_REGISTER.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1500_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1500_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1500_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1500_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1500_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1500_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1500_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1500_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1500"
QUAR_PROMOTION = QUARANTINE / "R10_CURVE_PROMOTION_GATE_NONCLAIM.csv"
QUAR_KERNEL = QUARANTINE / "DELTA_W_TO_ALPHA_KERNEL_CONTRACT_NONCLAIM.csv"
QUAR_EQUATIONS = QUARANTINE / "R10_EQUATION_CONVENTION_REGISTER_NONCLAIM.csv"
QUAR_BLOCKERS = QUARANTINE / "TARGET_PROMOTION_BLOCKERS_NONCLAIM.csv"
BRANCH_PROMOTION = BRANCH_RESIDUALS / "r10_curve_promotion_gate_nonclaim_1500.csv"
BRANCH_KERNEL = BRANCH_RESIDUALS / "r10_delta_w_to_alpha_kernel_contract_nonclaim_1500.csv"
BRANCH_EQUATIONS = BRANCH_RESIDUALS / "r10_equation_convention_register_nonclaim_1500.csv"
BRANCH_BLOCKERS = BRANCH_RESIDUALS / "r10_target_promotion_blockers_nonclaim_1500.csv"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def promotion_gate_rows() -> list[dict[str, Any]]:
    checks = [
        ("PROM1500_0_source_curve", "source curve points are visual estimates, not reviewed digitization", False),
        ("PROM1500_1_machine_table", "no machine-readable primary R10 alpha(lambda) table found", False),
        ("PROM1500_2_axis_review", "axis calibration is visual/nonclaim and still requires review", False),
        ("PROM1500_3_curve_identity", "Eot-Wash 2020 curve identity is plausible but not independently reviewed", False),
        ("PROM1500_4_kernel", "delta_w-to-alpha projection kernel absent", False),
        ("PROM1500_5_live_target", "live R10 curve target must remain absent", False),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "promotion_check_id": check_id,
            "requirement": requirement,
            "requirement_satisfied": satisfied,
            "promotion_effect": "BLOCKS_LIVE_CURVE_PROMOTION",
            **flags(),
        }
        for check_id, requirement, satisfied in checks
    ]


def equation_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "equation_id": "EQ1500_0_R10_bound_convention",
            "equation": "V(r)=V_N(r)[1+alpha exp(-r/lambda)]",
            "meaning": "R10 constrains Yukawa strength alpha as a function of range lambda",
            "claim_status": "SOURCE_CONVENTION_NOT_MTS_PREDICTION",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "equation_id": "EQ1500_1_MTS_projection_target",
            "equation": "alpha_MTS(lambda)=sum_a C_a * tau_R10_a(lambda) * delta_w_a",
            "meaning": "minimal same-branch projection contract from MTS residual components into the R10 Yukawa alpha convention",
            "claim_status": "CONTRACT_ONLY_COEFFICIENTS_MISSING",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "equation_id": "EQ1500_2_R10_acceptance",
            "equation": "|alpha_MTS(lambda_i)| <= alpha_bound(lambda_i) for every reviewed curve row i",
            "meaning": "local R10 residual pass condition after curve and kernel are both validated",
            "claim_status": "NOT_EVALUABLE_YET",
            **flags(),
        },
    ]


def kernel_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("KERN1500_0_curve", "reviewed alpha_bound(lambda) curve", rel(CURVE_TARGET), "empirical_bound", "MISSING_LIVE_TARGET"),
        ("KERN1500_1_delta_w_basis", "delta_w component basis and units", "source-intake/mts_residuals/P8_Y5_R10_delta_w_basis_contract.csv", "MTS_residual_basis", "MISSING"),
        ("KERN1500_2_coefficients", "component coupling coefficients C_a", rel(C_PARENT_IMPORT), "parent_action_or_explicit_residual", "MISSING_FORBIDDEN_IMPORT"),
        ("KERN1500_3_geometry", "R10 source/test geometry response tau_R10_a(lambda)", "source-intake/r10/derived/R10_geometry_response_kernel.csv", "experimental_projection", "MISSING"),
        ("KERN1500_4_range_law", "mapping between MTS local residual range and Yukawa lambda", "source-intake/r10/derived/R10_lambda_range_law.csv", "theory_projection", "MISSING"),
        ("KERN1500_5_sign", "absolute/plus/minus alpha convention", rel(EQUATION_REGISTER), "comparison_convention", "CONTRACT_WRITTEN_NEEDS_REVIEW"),
        ("KERN1500_6_output", "computed alpha_MTS(lambda) rows", rel(KERNEL_TARGET), "score_input", "MISSING"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "kernel_input_id": input_id,
            "required_input": required_input,
            "target_path": target_path,
            "owner": owner,
            "current_status": status,
            "failure_effect": "R10 score remains blocked",
            **flags(),
        }
        for input_id, required_input, target_path, owner, status in rows
    ]


def write_kernel_stub(points: list[dict[str, str]]) -> list[dict[str, Any]]:
    rows = []
    for row in points:
        rows.append(
            {
                "lambda_value": row["lambda_value"],
                "lambda_units": row["lambda_units"],
                "alpha_bound_abs_visual_nonclaim": row["alpha_bound_abs"],
                "delta_w_component_id": "MISSING_DELTA_W_COMPONENT",
                "C_a": "MISSING_PARENT_OR_RESIDUAL_COEFFICIENT",
                "tau_R10_a_lambda": "MISSING_GEOMETRY_KERNEL",
                "alpha_MTS_predicted": "MISSING",
                "pass_condition": "abs(alpha_MTS_predicted)<=alpha_bound_abs",
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    write_csv(KERNEL_STUB, rows)
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "stub_id": "STUB1500_0_kernel",
            "stub_path": rel(KERNEL_STUB),
            "stub_rows": len(rows),
            "stub_status": "NONCLAIM_KERNEL_STRUCTURE_WRITTEN_WITH_MISSING_INPUTS",
            "live_kernel_target": rel(KERNEL_TARGET),
            "live_kernel_target_exists": KERNEL_TARGET.exists(),
            **flags(),
        }
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1500_0_curve",
            "blocking_marker": "REVIEWED_R10_CURVE_MISSING",
            "reason": "1499 visual points cannot be promoted to live alpha(lambda) curve",
            "target_path": rel(CURVE_TARGET),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1500_1_kernel",
            "blocking_marker": "DELTA_W_TO_ALPHA_KERNEL_MISSING",
            "reason": "projection from MTS residuals into Yukawa alpha convention is not derived",
            "target_path": rel(KERNEL_TARGET),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1500_2_parent",
            "blocking_marker": "PARENT_COEFFICIENTS_MISSING",
            "reason": "C_a coefficients are not parent-action owned or source-backed",
            "target_path": rel(C_PARENT_IMPORT),
            **flags(),
        },
    ]


def simple_rows_from_blockers(blockers: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            f"{prefix}_id": f"{prefix.upper()}1500_{index}",
            "object": row["blocking_marker"],
            "path": row["target_path"],
            "status": "BLOCKED",
            "effect": row["reason"],
            **flags(),
        }
        for index, row in enumerate(blockers)
    ]


def c_parent_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "refusal_id": "CP1500_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "1500 writes a contract and refuses unsourced parent coefficients",
            "claim_effect": "R10/local-GR claim remains blocked",
            **flags(),
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1500_0_no_curve_promotion",
            "decision": "do not promote the visual 1499 points to the live R10 alpha(lambda) curve",
            "rationale": "they are useful for development but too weak for claim-grade bound rows",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1500_1_kernel_next",
            "decision": "prioritize the delta_w-to-alpha projection kernel over more cosmetic digitization",
            "rationale": "without the kernel even a perfect bound curve cannot test MTS",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1500_0_1501",
            "next_target": "1501-Y5-R10-RAB-delta-w-to-yukawa-alpha-kernel-derivation-attempt.md",
            "script": "scripts/Y5_R10_RAB_delta_w_to_yukawa_alpha_kernel_derivation_attempt.py",
            "objective": "attempt to derive the weak-field map from MTS local delta_w residuals to an effective Yukawa alpha(lambda); if derivation fails, retain explicit kernel closure variables",
            **flags(),
        }
    ]


def csvs_parse(paths: list[Path]) -> bool:
    return all(parse_csv(path) for path in paths)


def generated_flags_false(paths: list[Path]) -> bool:
    for path in paths:
        for row in read_csv(path):
            for column in ["score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]:
                value = row.get(column)
                if value not in (None, "", "False", "false", False):
                    return False
    return True


def kernel_stub_false() -> bool:
    return all(row["valid_for_claim"] == "False" and row["claim_allowed"] == "False" for row in read_csv(KERNEL_STUB))


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (PROMOTION_GATE, QUAR_PROMOTION),
        (KERNEL_CONTRACT, QUAR_KERNEL),
        (EQUATION_REGISTER, QUAR_EQUATIONS),
        (TARGET_BLOCKERS, QUAR_BLOCKERS),
        (PROMOTION_GATE, BRANCH_PROMOTION),
        (KERNEL_CONTRACT, BRANCH_KERNEL),
        (EQUATION_REGISTER, BRANCH_EQUATIONS),
        (TARGET_BLOCKERS, BRANCH_BLOCKERS),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], promotion: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values()) and VISUAL_POINTS.exists()
    promotion_blocked = all(row["requirement_satisfied"] is False for row in promotion)
    stub_ok = KERNEL_STUB.exists() and kernel_stub_false()
    live_targets_absent = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = csvs_parse(generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_PROMOTION, QUAR_KERNEL, QUAR_EQUATIONS, QUAR_BLOCKERS, BRANCH_PROMOTION, BRANCH_KERNEL, BRANCH_EQUATIONS, BRANCH_BLOCKERS])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1500_0_local_sources", source_paths_exist, "all cited 1499/staged point paths exist"),
        ("VAL1500_1_promotion_blocked", promotion_blocked, "all curve-promotion requirements are unsatisfied"),
        ("VAL1500_2_kernel_stub", stub_ok, "kernel stub exists and remains nonclaim"),
        ("VAL1500_3_live_targets_absent", live_targets_absent, "live R10 curve/kernel targets remain absent"),
        ("VAL1500_4_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1500_5_csv_parse", csv_parse_ok, "all generated 1500 CSVs parse cleanly"),
        ("VAL1500_6_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1500_7_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1500_8_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1500_9_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1500_10_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1500 refused curve promotion and wrote the delta_w-to-alpha kernel contract"
            if overall
            else "1500 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(promotion: list[dict[str, Any]], equations: list[dict[str, Any]], kernel: list[dict[str, Any]], stub: list[dict[str, Any]], validation: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1500 - Reviewed R10 Curve Promotion Gate or Kernel Derivation Contract",
                "",
                "## Verdict",
                "- The 1499 visual R10 points are not promoted to the live curve file.",
                "- A concrete `delta_w -> alpha(lambda)` kernel contract is now written.",
                "- The next physics target is derivational: map MTS local residuals into the R10 Yukawa convention or retain explicit closure variables.",
                "",
                "## Curve Promotion Gate",
                md_table(promotion, ["promotion_check_id", "requirement", "requirement_satisfied", "promotion_effect"]),
                "",
                "## Equation Convention Register",
                md_table(equations, ["equation_id", "equation", "claim_status"]),
                "",
                "## Kernel Contract",
                md_table(kernel, ["kernel_input_id", "required_input", "owner", "current_status"]),
                "",
                "## Kernel Stub",
                md_table(stub, ["stub_id", "stub_path", "stub_rows", "stub_status"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    points = read_csv(VISUAL_POINTS)
    promotion = promotion_gate_rows()
    equations = equation_rows()
    kernel = kernel_contract_rows()
    stub = write_kernel_stub(points)
    blockers = blocker_rows()
    readiness = simple_rows_from_blockers(blockers, "ready")
    c_parent = c_parent_refusal_rows()
    local_rows = [
        {"same_parent_branch_id": BRANCH_ID, "local_status_id": "LRS1500_0", "object": "R10 kernel bridge", "status": "KERNEL_CONTRACT_WRITTEN_DERIVATION_OPEN", "effect": "moves from data plumbing to derivation target", **flags()}
    ]
    rejections = simple_rows_from_blockers(blockers, "rejection")
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(PROMOTION_GATE, promotion)
    write_csv(EQUATION_REGISTER, equations)
    write_csv(KERNEL_CONTRACT, kernel)
    write_csv(KERNEL_STUB_LEDGER, stub)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        PROMOTION_GATE,
        EQUATION_REGISTER,
        KERNEL_CONTRACT,
        KERNEL_STUB_LEDGER,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, promotion)
    write_csv(VALIDATION, validation)
    write_doc(promotion, equations, kernel, stub, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
