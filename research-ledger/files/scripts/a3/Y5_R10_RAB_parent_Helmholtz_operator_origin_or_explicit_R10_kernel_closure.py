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
DOC = ROOT / "1502-Y5-R10-RAB-parent-Helmholtz-operator-origin-or-explicit-R10-kernel-closure.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1501_validation": OUT / "P8_Y5_BRR545_1501_VALIDATION.csv",
    "1501_theorem": OUT / "P8_Y5_R10_1501_CONDITIONAL_YUKAWA_KERNEL_THEOREM.csv",
    "1501_closure": OUT / "P8_Y5_R10_1501_KERNEL_CLOSURE_VARIABLES.csv",
    "1501_formula": OUT / "P8_Y5_R10_1501_KERNEL_FORMULA_REGISTER.csv",
    "1501_blockers": OUT / "P8_Y5_R10_1501_TARGET_PROMOTION_BLOCKERS.csv",
    "538_parent_action_tests": ROOT / "runs" / "20260605-041500-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion" / "results" / "P8_Y5_MINIMAL_PARENT_ACTION_TEST_CASES.csv",
    "557_positive_operator_attempt": ROOT / "runs" / "20260605-142500-Y5-Cextra-bulk-memory-range-positive-operator-zero-or-Yukawa-bound-fill" / "results" / "P8_Y5_CEXTRA_BULK_MEMORY_RANGE_POSITIVE_OPERATOR_ATTEMPT.csv",
    "558_no_range_attempt": ROOT / "runs" / "20260605-143500-Y5-R10-alpha-lambda-source-normalized-curve-data-or-no-range-theorem" / "results" / "P8_Y5_R10_NO_RANGE_THEOREM_ATTEMPT.csv",
}

CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

OPERATOR_AUDIT = OUT / "P8_Y5_R10_1502_OPERATOR_DERIVATION_AUDIT.csv"
HELMHOLTZ_THEOREM = OUT / "P8_Y5_R10_1502_CONDITIONAL_HELMHOLTZ_THEOREM.csv"
ACTION_REQUIREMENTS = OUT / "P8_Y5_R10_1502_PARENT_ACTION_CLAUSE_REQUIREMENTS.csv"
KERNEL_DEMOTION = OUT / "P8_Y5_R10_1502_R10_KERNEL_CLOSURE_DEMOTION.csv"
FORMULA_REGISTER = OUT / "P8_Y5_R10_1502_FORMULA_REGISTER.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1502_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1502_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1502_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1502_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1502_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1502_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1502_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1502_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1502"
QUAR_OPERATOR = QUARANTINE / "OPERATOR_DERIVATION_AUDIT_NONCLAIM.csv"
QUAR_THEOREM = QUARANTINE / "CONDITIONAL_HELMHOLTZ_THEOREM_NONCLAIM.csv"
QUAR_REQUIREMENTS = QUARANTINE / "PARENT_ACTION_CLAUSE_REQUIREMENTS_NONCLAIM.csv"
QUAR_DEMOTION = QUARANTINE / "R10_KERNEL_CLOSURE_DEMOTION_NONCLAIM.csv"
BRANCH_OPERATOR = BRANCH_RESIDUALS / "r10_operator_derivation_audit_nonclaim_1502.csv"
BRANCH_THEOREM = BRANCH_RESIDUALS / "r10_conditional_helmholtz_theorem_nonclaim_1502.csv"
BRANCH_REQUIREMENTS = BRANCH_RESIDUALS / "r10_parent_action_clause_requirements_nonclaim_1502.csv"
BRANCH_DEMOTION = BRANCH_RESIDUALS / "r10_kernel_closure_demotion_nonclaim_1502.csv"


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


def operator_audit_rows() -> list[dict[str, Any]]:
    steps = [
        (
            "OP1502_0_template_action",
            "candidate local quadratic residual clause",
            "L_X=-1/2 Z_a g^{mu nu} d_mu X_a d_nu X_a -1/2 M_a^2 X_a^2 + s_a X_a rho",
            "mathematically sufficient template, not shown to be in the current parent action",
            False,
            "template_only",
        ),
        (
            "OP1502_1_variation",
            "Euler-Lagrange variation of the template",
            "Z_a Box X_a - M_a^2 X_a = -s_a rho",
            "derivable if OP1502_0 is parent-owned",
            True,
            "conditional_derivation",
        ),
        (
            "OP1502_2_static_limit",
            "local weak-field static limit",
            "(nabla^2 - M_a^2/Z_a) X_a = -s_a rho/Z_a",
            "standard Helmholtz operator follows from the template",
            True,
            "conditional_derivation",
        ),
        (
            "OP1502_3_range_law",
            "range law",
            "lambda_a = sqrt(Z_a/M_a^2)",
            "requires Z_a>0 and M_a^2>0 from the parent action",
            False,
            "missing_parent_sign",
        ),
        (
            "OP1502_4_matter_coupling",
            "test-body readout",
            "delta Phi_test = beta_a c^2 X_a",
            "beta_a or equivalent matter-metric coupling is not parent-normalized",
            False,
            "missing_coupling",
        ),
        (
            "OP1502_5_alpha_normalization",
            "Yukawa alpha mapping",
            "alpha_a ~ beta_a s_a /(4 pi G Z_a), with unit factors fixed by the chosen X_a convention",
            "source/test units and sign convention are not locked",
            False,
            "missing_units",
        ),
        (
            "OP1502_6_R10_geometry",
            "finite-source R10 projection",
            "alpha_MTS(lambda_i)=sum_a C_a tau_R10_a(lambda_i) delta_w_a",
            "requires geometry convolution before comparison with the torsion-balance bound",
            False,
            "missing_arena_projection",
        ),
        (
            "OP1502_7_parent_ownership_verdict",
            "current parent-action status",
            "current files do not contain the signed Z_a,M_a^2,s_a,beta_a operator package",
            "operator origin not claimed; kernel remains closure-only",
            False,
            "not_parent_derived",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "operator_step_id": step_id,
            "object": obj,
            "formula": formula,
            "status_detail": detail,
            "derived_inside_template": template_ok,
            "parent_owned": parent_effect in {"conditional_derivation"} and step_id in {"OP1502_1_variation", "OP1502_2_static_limit"},
            "derivation_effect": parent_effect,
            **flags(),
        }
        for step_id, obj, formula, detail, template_ok, parent_effect in steps
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1502_0_conditional_helmholtz",
            "statement": "A Yukawa/Helmholtz residual follows if the parent action contains a local quadratic residual field X_a with positive kinetic coefficient Z_a, positive mass coefficient M_a^2, a universal source s_a rho, and a matter readout beta_a X_a.",
            "proof_status": "CONDITIONAL_PARENT_ACTION_TEMPLATE",
            "derived_equation": "(nabla^2-lambda_a^-2)X_a=-s_a rho/Z_a; lambda_a=sqrt(Z_a/M_a^2)",
            "unclosed_premises": "parent ownership of X_a; Z_a sign; M_a^2 sign; source normalization s_a; test-body coupling beta_a; R10 geometry response",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1502_1_closure_demotion",
            "statement": "If the signed quadratic residual clause is not parent-owned, the R10 kernel is an explicit closure and cannot be treated as a derived local-GR/Newton/R10 pass.",
            "proof_status": "DERIVED_AS_GATE_LOGIC",
            "derived_equation": "not_applicable",
            "unclosed_premises": "none for the demotion rule",
            **flags(),
        },
    ]


def action_requirement_rows() -> list[dict[str, Any]]:
    requirements = [
        ("REQ1502_0_field_owner", "X_a or delta_w_a", "define the residual variable as a real parent field or constrained auxiliary", "MISSING"),
        ("REQ1502_1_kinetic", "Z_a", "positive kinetic/operator coefficient in the local quadratic action", "MISSING"),
        ("REQ1502_2_mass_gap", "M_a^2", "positive mass/range coefficient giving lambda_a=sqrt(Z_a/M_a^2)", "MISSING"),
        ("REQ1502_3_source", "s_a rho", "universal source coupling to local mass density or Hamiltonian mass charge", "MISSING"),
        ("REQ1502_4_test_readout", "beta_a", "test-body matter-metric coupling/readout", "MISSING"),
        ("REQ1502_5_normalization", "G_measured", "same-frame Newton normalization so alpha is not double-counted into measured G", "MISSING"),
        ("REQ1502_6_geometry", "tau_R10_a(lambda)", "finite-source torsion-balance geometry response", "MISSING"),
        ("REQ1502_7_curve", "alpha_bound(lambda)", "reviewed source-backed R10 bound curve", "VISUAL_NONCLAIM_ONLY"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "requirement_id": requirement_id,
            "symbol": symbol,
            "requirement": requirement,
            "current_status": status,
            "required_before_score": True,
            **flags(),
        }
        for requirement_id, symbol, requirement, status in requirements
    ]


def demotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "demotion_id": "DEM1502_0_R10_kernel",
            "object": "R10_delta_w_kernel_lambda",
            "status": "DEMOTED_TO_EXPLICIT_CLOSURE",
            "reason": "the Helmholtz operator and alpha normalization are derivable only from an unsigned template, not the current parent action",
            "minimum_live_schema": "lambda_a;delta_w_a;Z_a;M_a2;s_a;beta_a;C_a;tau_R10_a;alpha_predicted;alpha_bound;source_paths;valid_for_claim",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "demotion_id": "DEM1502_1_local_GR_Newton",
            "object": "local_GR_Newton_R10_branch",
            "status": "NOT_PROMOTABLE",
            "reason": "a finite-range residual tail must either be parent-zeroed or source-bounded before local-GR/Newton closure can be claimed",
            "minimum_live_schema": "theorem_zero_certificate OR executable same-frame alpha(lambda) comparison",
            **flags(),
        },
    ]


def formula_rows() -> list[dict[str, Any]]:
    formulas = [
        ("FORM1502_0_parent_clause", "S_X=int sqrt(-g)[-1/2 Z_a(grad X_a)^2 -1/2 M_a^2 X_a^2 + s_a X_a rho]", "candidate clause, not parent-owned"),
        ("FORM1502_1_euler_lagrange", "Z_a Box X_a - M_a^2 X_a = -s_a rho", "conditional variation"),
        ("FORM1502_2_static_helmholtz", "(nabla^2-lambda_a^-2)X_a=-s_a rho/Z_a", "conditional local limit"),
        ("FORM1502_3_range", "lambda_a=sqrt(Z_a/M_a^2)", "requires positive Z_a and M_a^2"),
        ("FORM1502_4_alpha_contract", "alpha_a(lambda) ~ beta_a s_a/(4 pi G Z_a) after units/readout are fixed", "normalization not locked"),
        ("FORM1502_5_R10_kernel", "alpha_MTS(lambda_i)=sum_a C_a tau_R10_a(lambda_i) delta_w_a", "closure-only until parent-owned"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "formula_id": formula_id,
            "formula": formula,
            "status": status,
            **flags(),
        }
        for formula_id, formula, status in formulas
    ]


def blocker_rows() -> list[dict[str, Any]]:
    blockers = [
        ("BLK1502_0_parent_clause", "MISSING_PARENT_QUADRATIC_RESIDUAL_CLAUSE", "no parent-owned signed X_a action clause", "parent_action"),
        ("BLK1502_1_signs", "MISSING_POSITIVE_OPERATOR_AND_MASS_GAP", "Z_a>0 and M_a^2>0 are required for stable Yukawa range", "parent_action"),
        ("BLK1502_2_source", "MISSING_SOURCE_CHARGE_NORMALIZATION", "s_a rho or Hamiltonian charge source is unsourced", "parent_action"),
        ("BLK1502_3_coupling", "MISSING_TEST_BODY_COUPLING", "beta_a/C_a matter readout is not derived", rel(C_PARENT_IMPORT)),
        ("BLK1502_4_geometry", "MISSING_R10_GEOMETRY_RESPONSE", "tau_R10_a(lambda) has not been computed", rel(KERNEL_TARGET)),
        ("BLK1502_5_curve", "MISSING_REVIEWED_R10_BOUND_CURVE", "1499 curve points remain visual nonclaim", rel(CURVE_TARGET)),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "blocker_id": blocker_id,
            "blocking_marker": marker,
            "reason": reason,
            "target_path": target,
            **flags(),
        }
        for blocker_id, marker, reason, target in blockers
    ]


def simple_rows_from_blockers(blockers: list[dict[str, Any]], prefix: str) -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            f"{prefix}_id": f"{prefix.upper()}1502_{index}",
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
            "refusal_id": "CP1502_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "1502 derives the coupling contract but does not import or fabricate coefficients",
            "claim_effect": "R10/local-GR claim remains blocked",
            **flags(),
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        ("DEC1502_0_operator_contract", "accept the Helmholtz/Yukawa operator only as a conditional parent-action theorem", "variation works, ownership does not"),
        ("DEC1502_1_kernel_demotion", "demote the R10 kernel to explicit closure variables", "current parent action lacks signed Z/M/source/coupling package"),
        ("DEC1502_2_next", "attack matter-coupling normalization next", "without beta_a/C_a the field can be elegant and still not scoreable"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, rationale in decisions
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1502_0_1503",
            "next_target": "1503-Y5-R10-RAB-matter-coupling-normalization-from-Newton-limit-or-closure-bound.md",
            "script": "scripts/Y5_R10_RAB_matter_coupling_normalization_from_Newton_limit_or_closure_bound.py",
            "objective": "try to derive beta_a/C_a from the same-frame Newton limit and universal matter action; if not derivable, keep alpha(lambda) as a closure-bound row",
            **flags(),
        }
    ]


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
        (OPERATOR_AUDIT, QUAR_OPERATOR),
        (HELMHOLTZ_THEOREM, QUAR_THEOREM),
        (ACTION_REQUIREMENTS, QUAR_REQUIREMENTS),
        (KERNEL_DEMOTION, QUAR_DEMOTION),
        (OPERATOR_AUDIT, BRANCH_OPERATOR),
        (HELMHOLTZ_THEOREM, BRANCH_THEOREM),
        (ACTION_REQUIREMENTS, BRANCH_REQUIREMENTS),
        (KERNEL_DEMOTION, BRANCH_DEMOTION),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], audit: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    conditional_theorem = any(row["proof_status"] == "CONDITIONAL_PARENT_ACTION_TEMPLATE" for row in read_csv(HELMHOLTZ_THEOREM))
    parent_operator_missing = any(row["derivation_effect"] in {"template_only", "missing_parent_sign", "missing_coupling", "missing_units", "missing_arena_projection", "not_parent_derived"} for row in audit)
    demoted = any(row["status"] == "DEMOTED_TO_EXPLICIT_CLOSURE" for row in read_csv(KERNEL_DEMOTION))
    live_targets_absent = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = all(parse_csv(path) for path in generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_OPERATOR, QUAR_THEOREM, QUAR_REQUIREMENTS, QUAR_DEMOTION, BRANCH_OPERATOR, BRANCH_THEOREM, BRANCH_REQUIREMENTS, BRANCH_DEMOTION])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1502_0_local_sources", source_paths_exist, "all cited 1501/parent-action/R10 paths exist"),
        ("VAL1502_1_conditional_theorem", conditional_theorem, "Helmholtz derivation is conditional on a parent action template"),
        ("VAL1502_2_parent_operator_missing", parent_operator_missing, "parent-owned Z/M/source/coupling package remains unsigned"),
        ("VAL1502_3_kernel_demoted", demoted, "R10 kernel is explicitly closure-only"),
        ("VAL1502_4_live_targets_absent", live_targets_absent, "live R10 curve/kernel targets remain absent"),
        ("VAL1502_5_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1502_6_csv_parse", csv_parse_ok, "all generated 1502 CSVs parse cleanly"),
        ("VAL1502_7_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1502_8_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1502_9_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1502_10_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1502_11_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1502 derived the exact Helmholtz parent-action contract but demoted the current R10 kernel to closure-only"
            if overall
            else "1502 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(audit: list[dict[str, Any]], theorem: list[dict[str, Any]], requirements: list[dict[str, Any]], demotion: list[dict[str, Any]], formulas: list[dict[str, Any]], validation: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1502 - Parent Helmholtz Operator Origin or Explicit R10 Kernel Closure",
                "",
                "## Verdict",
                "- The Helmholtz/Yukawa operator is derivable from a precise quadratic local residual action.",
                "- The current parent-action evidence does not yet own that signed action clause, source normalization, or matter readout.",
                "- Therefore the R10 kernel is closure-only for now, but the missing contract is now exact rather than vague.",
                "",
                "## Operator Derivation Audit",
                md_table(audit, ["operator_step_id", "object", "formula", "derived_inside_template", "derivation_effect"]),
                "",
                "## Conditional Theorem",
                md_table(theorem, ["theorem_id", "proof_status", "derived_equation", "unclosed_premises"]),
                "",
                "## Parent Action Requirements",
                md_table(requirements, ["requirement_id", "symbol", "requirement", "current_status"]),
                "",
                "## R10 Kernel Demotion",
                md_table(demotion, ["demotion_id", "object", "status", "reason"]),
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
    audit = operator_audit_rows()
    theorem = theorem_rows()
    requirements = action_requirement_rows()
    demotion = demotion_rows()
    formulas = formula_rows()
    blockers = blocker_rows()
    readiness = simple_rows_from_blockers(blockers, "ready")
    c_parent = c_parent_refusal_rows()
    local_rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LRS1502_0",
            "object": "R10/local Newton branch",
            "status": "CLOSURE_ONLY_UNTIL_PARENT_OPERATOR_AND_COUPLING_CLOSE",
            "effect": "derivation contract sharpened; no local-GR/Newton/R10 claim",
            **flags(),
        }
    ]
    rejections = simple_rows_from_blockers(blockers, "rejection")
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(OPERATOR_AUDIT, audit)
    write_csv(HELMHOLTZ_THEOREM, theorem)
    write_csv(ACTION_REQUIREMENTS, requirements)
    write_csv(KERNEL_DEMOTION, demotion)
    write_csv(FORMULA_REGISTER, formulas)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        OPERATOR_AUDIT,
        HELMHOLTZ_THEOREM,
        ACTION_REQUIREMENTS,
        KERNEL_DEMOTION,
        FORMULA_REGISTER,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, audit)
    write_csv(VALIDATION, validation)
    write_doc(audit, theorem, requirements, demotion, formulas, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
