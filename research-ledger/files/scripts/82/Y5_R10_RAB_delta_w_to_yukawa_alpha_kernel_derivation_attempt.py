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
DOC = ROOT / "1501-Y5-R10-RAB-delta-w-to-yukawa-alpha-kernel-derivation-attempt.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1500_validation": OUT / "P8_Y5_BRR545_1500_VALIDATION.csv",
    "1500_equations": OUT / "P8_Y5_R10_1500_R10_EQUATION_CONVENTION_REGISTER.csv",
    "1500_kernel_contract": OUT / "P8_Y5_R10_1500_DELTA_W_TO_ALPHA_KERNEL_CONTRACT.csv",
    "1500_kernel_stub": OUT / "P8_Y5_R10_1500_KERNEL_STUB_LEDGER.csv",
    "1500_next": OUT / "P8_Y5_R10_1500_NEXT_TARGET.csv",
}

CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

DERIVATION_STACK = OUT / "P8_Y5_R10_1501_WEAK_FIELD_DERIVATION_STACK.csv"
CONDITIONAL_THEOREM = OUT / "P8_Y5_R10_1501_CONDITIONAL_YUKAWA_KERNEL_THEOREM.csv"
CLOSURE_VARIABLES = OUT / "P8_Y5_R10_1501_KERNEL_CLOSURE_VARIABLES.csv"
KERNEL_FORMULA = OUT / "P8_Y5_R10_1501_KERNEL_FORMULA_REGISTER.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1501_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1501_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1501_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1501_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1501_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1501_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1501_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1501_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1501"
QUAR_DERIVATION = QUARANTINE / "WEAK_FIELD_DERIVATION_STACK_NONCLAIM.csv"
QUAR_THEOREM = QUARANTINE / "CONDITIONAL_YUKAWA_KERNEL_THEOREM_NONCLAIM.csv"
QUAR_CLOSURE = QUARANTINE / "KERNEL_CLOSURE_VARIABLES_NONCLAIM.csv"
QUAR_BLOCKERS = QUARANTINE / "TARGET_PROMOTION_BLOCKERS_NONCLAIM.csv"
BRANCH_DERIVATION = BRANCH_RESIDUALS / "r10_weak_field_derivation_stack_nonclaim_1501.csv"
BRANCH_THEOREM = BRANCH_RESIDUALS / "r10_conditional_yukawa_kernel_theorem_nonclaim_1501.csv"
BRANCH_CLOSURE = BRANCH_RESIDUALS / "r10_kernel_closure_variables_nonclaim_1501.csv"
BRANCH_BLOCKERS = BRANCH_RESIDUALS / "r10_target_promotion_blockers_nonclaim_1501.csv"


def flags() -> dict[str, bool]:
    return {"score_ready": False, "valid_prediction_row": False, "valid_for_claim": False, "claim_allowed": False}


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


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


def derivation_stack_rows() -> list[dict[str, Any]]:
    steps = [
        ("DER1501_0_GR_limit", "weak-field metric", "g_00=-(1+2 Phi/c^2)", "standard Newtonian limit form", True),
        ("DER1501_1_Newton", "Newton source law", "nabla^2 Phi_N=4 pi G rho", "GR/Newton side is known", True),
        ("DER1501_2_Yukawa", "R10 convention", "delta Phi/ Phi_N -> alpha exp(-r/lambda)", "bound convention known", True),
        ("DER1501_3_MTS_field", "MTS residual field equation", "(nabla^2-lambda^-2) X_a = source_a", "not parent-derived for delta_w", False),
        ("DER1501_4_coupling", "matter coupling", "delta S_matter ~ C_a X_a rho", "C_a not parent-owned", False),
        ("DER1501_5_kernel", "extended-body projection", "tau_R10_a(lambda)=geometry convolution of Yukawa response", "not computed", False),
        ("DER1501_6_prediction", "R10 prediction", "alpha_MTS(lambda)=sum_a C_a tau_R10_a(lambda) delta_w_a", "conditional only", False),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "derivation_step_id": step_id,
            "object": obj,
            "formula": formula,
            "status_detail": detail,
            "derived_or_available": ok,
            "derivation_effect": "supports conditional theorem" if ok else "blocks unconditional kernel derivation",
            **flags(),
        }
        for step_id, obj, formula, detail, ok in steps
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1501_0_conditional_kernel",
            "statement": "If each local MTS residual component delta_w_a is mediated by a parent-owned Helmholtz field X_a with range lambda, universal mass coupling C_a, and the R10 extended-body response tau_R10_a(lambda), then alpha_MTS(lambda)=sum_a C_a tau_R10_a(lambda) delta_w_a and the R10 pass condition is |alpha_MTS(lambda_i)|<=alpha_bound(lambda_i).",
            "proof_status": "CONDITIONAL_ONLY",
            "unclosed_premises": "parent Helmholtz operator; universal matter source; coefficient normalization; R10 geometry convolution; reviewed alpha(lambda) curve",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1501_1_no_unconditional_pass",
            "statement": "Without those premises, the visual R10 curve and the Yukawa convention do not imply an MTS R10 pass or local-GR/Newton closure.",
            "proof_status": "DERIVED_AS_BLOCKER_LOGIC",
            "unclosed_premises": "none for the blocker statement",
            **flags(),
        },
    ]


def closure_rows() -> list[dict[str, Any]]:
    closures = [
        ("CL1501_0_delta_w_basis", "delta_w_a", "dimensionless or units-specified residual component basis", "MISSING"),
        ("CL1501_1_range", "lambda_a", "range law/mass scale for each residual component", "MISSING"),
        ("CL1501_2_coupling", "C_a", "parent-owned universal matter coupling coefficient", "MISSING"),
        ("CL1501_3_geometry", "tau_R10_a(lambda)", "R10 source/test geometry convolution response", "MISSING"),
        ("CL1501_4_curve", "alpha_bound(lambda)", "reviewed R10 bound curve", "VISUAL_NONCLAIM_ONLY"),
        ("CL1501_5_sign", "alpha sign/absolute convention", "abs alpha or plus/minus branch selection", "CONTRACT_ONLY"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "closure_id": closure_id,
            "symbol": symbol,
            "definition": definition,
            "current_status": status,
            "required_before_score": True,
            **flags(),
        }
        for closure_id, symbol, definition, status in closures
    ]


def formula_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "formula_id": "FORM1501_0_point_mass_yukawa",
            "formula": "delta Phi(r) = -G M alpha exp(-r/lambda)/r",
            "usage": "links R10 alpha to potential-level correction",
            "status": "KNOWN_CONVENTION",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "formula_id": "FORM1501_1_force_response",
            "formula": "delta a/a_N = alpha (1+r/lambda) exp(-r/lambda) for point masses",
            "usage": "reminds that torque experiments require geometry convolution, not just potential amplitude",
            "status": "CONDITIONAL_GEOMETRY_REQUIRED",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "formula_id": "FORM1501_2_MTS_kernel",
            "formula": "alpha_MTS(lambda_i)=sum_a C_a tau_R10_a(lambda_i) delta_w_a",
            "usage": "minimal executable MTS/R10 score kernel once missing inputs are filled",
            "status": "CONTRACT_NOT_DERIVED",
            **flags(),
        },
    ]


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1501_0_parent_operator",
            "blocking_marker": "PARENT_HELMHOLTZ_OPERATOR_MISSING",
            "reason": "MTS delta_w residual has not been derived as a local Helmholtz/Yukawa mediator",
            "target_path": "parent_action",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1501_1_coupling",
            "blocking_marker": "UNIVERSAL_MATTER_COUPLING_MISSING",
            "reason": "C_a coefficients remain unsourced/underived",
            "target_path": rel(C_PARENT_IMPORT),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1501_2_geometry",
            "blocking_marker": "R10_GEOMETRY_CONVOLUTION_MISSING",
            "reason": "tau_R10_a(lambda) is needed because R10 measures torques of extended test bodies",
            "target_path": rel(KERNEL_TARGET),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": "BLK1501_3_curve",
            "blocking_marker": "REVIEWED_BOUND_CURVE_MISSING",
            "reason": "1499 curve is visual nonclaim only",
            "target_path": rel(CURVE_TARGET),
            **flags(),
        },
    ]


def simple_rows_from_blockers(blockers: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            f"{prefix}_id": f"{prefix.upper()}1501_{index}",
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
            "refusal_id": "CP1501_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "1501 does not import coefficients; it identifies them as derivation debt",
            "claim_effect": "R10/local-GR claim remains blocked",
            **flags(),
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1501_0_conditional_only",
            "decision": "accept the weak-field Yukawa map only as a conditional theorem",
            "rationale": "the field equation and coupling normalization are not parent-owned",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DEC1501_1_next",
            "decision": "attack the parent Helmholtz/operator origin before claiming R10",
            "rationale": "a geometry/data curve cannot replace a field-theoretic derivation",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1501_0_1502",
            "next_target": "1502-Y5-R10-RAB-parent-Helmholtz-operator-origin-or-explicit-R10-kernel-closure.md",
            "script": "scripts/Y5_R10_RAB_parent_Helmholtz_operator_origin_or_explicit_R10_kernel_closure.py",
            "objective": "try to derive the local Helmholtz/Yukawa operator for delta_w from the parent action; if not derivable, demote the R10 kernel to explicit closure variables",
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


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    BRANCH_RESIDUALS.mkdir(parents=True, exist_ok=True)
    for src, dst in [
        (DERIVATION_STACK, QUAR_DERIVATION),
        (CONDITIONAL_THEOREM, QUAR_THEOREM),
        (CLOSURE_VARIABLES, QUAR_CLOSURE),
        (TARGET_BLOCKERS, QUAR_BLOCKERS),
        (DERIVATION_STACK, BRANCH_DERIVATION),
        (CONDITIONAL_THEOREM, BRANCH_THEOREM),
        (CLOSURE_VARIABLES, BRANCH_CLOSURE),
        (TARGET_BLOCKERS, BRANCH_BLOCKERS),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], stack: list[dict[str, Any]], closures: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    conditional_only = any(row["proof_status"] == "CONDITIONAL_ONLY" for row in read_csv(CONDITIONAL_THEOREM))
    blockers_present = any(row["derived_or_available"] is False for row in stack) and len(closures) >= 6
    live_targets_absent = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = csvs_parse(generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_DERIVATION, QUAR_THEOREM, QUAR_CLOSURE, QUAR_BLOCKERS, BRANCH_DERIVATION, BRANCH_THEOREM, BRANCH_CLOSURE, BRANCH_BLOCKERS])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1501_0_local_sources", source_paths_exist, "all cited 1500 paths exist"),
        ("VAL1501_1_conditional_only", conditional_only, "kernel theorem remains conditional"),
        ("VAL1501_2_blockers", blockers_present, "unclosed premises and closure variables are explicit"),
        ("VAL1501_3_live_targets_absent", live_targets_absent, "live R10 curve/kernel targets remain absent"),
        ("VAL1501_4_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1501_5_csv_parse", csv_parse_ok, "all generated 1501 CSVs parse cleanly"),
        ("VAL1501_6_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1501_7_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1501_8_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1501_9_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1501_10_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1501 derived only a conditional Yukawa kernel theorem and retained explicit closure variables"
            if overall
            else "1501 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(stack: list[dict[str, Any]], theorem: list[dict[str, Any]], closures: list[dict[str, Any]], formulas: list[dict[str, Any]], validation: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1501 - delta_w to Yukawa alpha Kernel Derivation Attempt",
                "",
                "## Verdict",
                "- The weak-field Yukawa comparison map can be written, but only conditionally.",
                "- The parent Helmholtz operator, universal matter coupling, coefficient normalization, R10 geometry convolution, and reviewed curve remain unclosed.",
                "- Therefore R10 is now a well-posed derivation target, not a claim.",
                "",
                "## Derivation Stack",
                md_table(stack, ["derivation_step_id", "object", "formula", "derived_or_available", "derivation_effect"]),
                "",
                "## Conditional Theorem",
                md_table(theorem, ["theorem_id", "proof_status", "unclosed_premises"]),
                "",
                "## Closure Variables",
                md_table(closures, ["closure_id", "symbol", "definition", "current_status"]),
                "",
                "## Formula Register",
                md_table(formulas, ["formula_id", "formula", "status"]),
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
    stack = derivation_stack_rows()
    theorem = theorem_rows()
    closures = closure_rows()
    formulas = formula_rows()
    blockers = blocker_rows()
    readiness = simple_rows_from_blockers(blockers, "ready")
    c_parent = c_parent_refusal_rows()
    local_rows = [
        {"same_parent_branch_id": BRANCH_ID, "local_status_id": "LRS1501_0", "object": "R10 weak-field kernel", "status": "CONDITIONAL_ONLY_CLOSURE_REQUIRED", "effect": "derivation target sharpened, no score/local claim", **flags()}
    ]
    rejections = simple_rows_from_blockers(blockers, "rejection")
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(DERIVATION_STACK, stack)
    write_csv(CONDITIONAL_THEOREM, theorem)
    write_csv(CLOSURE_VARIABLES, closures)
    write_csv(KERNEL_FORMULA, formulas)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        DERIVATION_STACK,
        CONDITIONAL_THEOREM,
        CLOSURE_VARIABLES,
        KERNEL_FORMULA,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, stack, closures)
    write_csv(VALIDATION, validation)
    write_doc(stack, theorem, closures, formulas, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
