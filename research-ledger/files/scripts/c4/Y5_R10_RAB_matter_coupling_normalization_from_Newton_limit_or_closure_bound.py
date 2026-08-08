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
DOC = ROOT / "1503-Y5-R10-RAB-matter-coupling-normalization-from-Newton-limit-or-closure-bound.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1502_validation": OUT / "P8_Y5_BRR545_1502_VALIDATION.csv",
    "1502_operator": OUT / "P8_Y5_R10_1502_OPERATOR_DERIVATION_AUDIT.csv",
    "1502_requirements": OUT / "P8_Y5_R10_1502_PARENT_ACTION_CLAUSE_REQUIREMENTS.csv",
    "1502_demotion": OUT / "P8_Y5_R10_1502_R10_KERNEL_CLOSURE_DEMOTION.csv",
    "1473_double_zero": OUT / "P8_Y5_R10_1473_PARENT_COUPLING_DOUBLE_ZERO_THEOREM_ATTEMPT.csv",
    "1484_cparent_attempt": OUT / "P8_Y5_R10_1484_C_PARENT_COUPLING_DERIVATION_ATTEMPT.csv",
    "1229_source_contract": OUT / "P8_Y5_R10_1229_LOCAL_GR_SOURCE_COUPLING_THEOREM_CONTRACT.csv",
    "1229_source_audit": OUT / "P8_Y5_R10_1229_UNIVERSAL_SOURCE_COUPLING_CLAUSE_AUDIT.csv",
    "constant_sector_contract": OUT / "P8_constant_sector_universality_CONTRACT.csv",
    "matter_action_contract": ROOT / "runs" / "20260601-191500-universal-matter-coupling-theorem-attempt" / "results" / "matter_action_contract.csv",
    "matter_action_candidates": ROOT / "runs" / "20260601-211000-representative-invariant-matter-action-for-lifted-C" / "results" / "matter_action_candidates.csv",
    "same_frame_allowed_forms": ROOT / "runs" / "20260602-113000-same-frame-matter-functor-zero-route" / "results" / "allowed_matter_action_forms.csv",
    "radial_calibration_gates": ROOT / "runs" / "20260604-141500-source-normalization-radial-and-calibration-theorem-attempt" / "results" / "P8_RADIAL_CALIBRATION_COUPLING_GATES.csv",
}

CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

NEWTON_AUDIT = OUT / "P8_Y5_R10_1503_NEWTON_LIMIT_COUPLING_AUDIT.csv"
COUPLING_THEOREM = OUT / "P8_Y5_R10_1503_COUPLING_NORMALIZATION_THEOREM.csv"
FORMULA_REGISTER = OUT / "P8_Y5_R10_1503_COUPLING_FORMULA_REGISTER.csv"
BOUND_ROW_CONTRACT = OUT / "P8_Y5_R10_1503_COUPLING_CLOSURE_BOUND_ROW_CONTRACT.csv"
ZERO_ROUTE = OUT / "P8_Y5_R10_1503_BETA_ZERO_ROUTE_AUDIT.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1503_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1503_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1503_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1503_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1503_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1503_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1503_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1503_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1503"
QUAR_NEWTON = QUARANTINE / "NEWTON_LIMIT_COUPLING_AUDIT_NONCLAIM.csv"
QUAR_THEOREM = QUARANTINE / "COUPLING_NORMALIZATION_THEOREM_NONCLAIM.csv"
QUAR_FORMULA = QUARANTINE / "COUPLING_FORMULA_REGISTER_NONCLAIM.csv"
QUAR_BOUND = QUARANTINE / "COUPLING_CLOSURE_BOUND_ROW_CONTRACT_NONCLAIM.csv"
BRANCH_NEWTON = BRANCH_RESIDUALS / "r10_newton_limit_coupling_audit_nonclaim_1503.csv"
BRANCH_THEOREM = BRANCH_RESIDUALS / "r10_coupling_normalization_theorem_nonclaim_1503.csv"
BRANCH_FORMULA = BRANCH_RESIDUALS / "r10_coupling_formula_register_nonclaim_1503.csv"
BRANCH_BOUND = BRANCH_RESIDUALS / "r10_coupling_closure_bound_row_contract_nonclaim_1503.csv"


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


def newton_audit_rows() -> list[dict[str, Any]]:
    steps = [
        (
            "NL1503_0_standard_limit",
            "observed Newton limit",
            "a_N=-G_N M/r^2",
            "sets the measured common 1/r source strength in the observed frame",
            "DERIVED_STANDARD_INPUT",
            True,
        ),
        (
            "NL1503_1_common_rescaling",
            "universal massless rescaling",
            "G_parent -> G_N = G_parent(1+epsilon_common)",
            "a single composition-independent massless factor can be absorbed into measured G_N",
            "CALIBRATION_ONLY",
            True,
        ),
        (
            "NL1503_2_finite_range_residual",
            "finite-range residual force",
            "delta a/a_N = alpha_a(1+r/lambda_a)exp(-r/lambda_a)",
            "lambda-dependent force shape cannot be absorbed into a constant G_N calibration",
            "NOT_FIXED_BY_NEWTON_LIMIT",
            False,
        ),
        (
            "NL1503_3_composition_readout",
            "species/source readout",
            "epsilon_A, beta_A, s_A, or C_A",
            "composition-dependent factors are visible to WEP/PPN/clocks and are not removed by Newton calibration",
            "NOT_FIXED_BY_NEWTON_LIMIT",
            False,
        ),
        (
            "NL1503_4_same_frame_action",
            "single observed coframe matter action",
            "S_matter=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A]",
            "can kill direct matter vertices if parent proves e_obs is independent of residual X_a in the local branch",
            "CONDITIONAL_ZERO_ROUTE",
            False,
        ),
        (
            "NL1503_5_conformal_readout",
            "if e_obs depends on X_a",
            "e_obs -> exp(beta_a X_a)e_obs",
            "then beta_a is a new parent coefficient; Newton limit alone does not choose it",
            "CLOSURE_UNLESS_PARENT_DERIVED",
            False,
        ),
        (
            "NL1503_6_verdict",
            "coupling normalization verdict",
            "Newton limit fixes only the common zero-range/massless calibration, not finite alpha(lambda)",
            "R10 alpha needs beta_a*s_a/Z_a from parent action or an explicit bound row",
            "NO_UNIQUE_C_FROM_NEWTON_ALONE",
            False,
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": obj,
            "formula": formula,
            "result": result,
            "status": status,
            "derived_or_calibrated": ok,
            **flags(),
        }
        for audit_id, obj, formula, result, status, ok in steps
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1503_0_no_newton_unique_finite_coupling",
            "statement": "The same-frame Newton limit fixes one common inverse-square normalization G_N, but it does not determine a finite-range Yukawa amplitude alpha_a(lambda) because alpha_a multiplies a different radial kernel.",
            "proof_status": "DERIVED_AS_NO_GO_FOR_NEWTON_ONLY",
            "proof_sketch": "Compare a_N proportional to r^-2 with delta a proportional to r^-2(1+r/lambda)exp(-r/lambda). No constant G_N redefinition matches that kernel for all r unless alpha_a=0 or lambda is outside the active arena by theorem/bound.",
            "claim_effect": "C_a cannot be imported from Newton calibration alone",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1503_1_conditional_zero_by_same_frame_independence",
            "statement": "If the parent matter action depends only on one observed coframe and the local residual X_a is absent from that coframe to first order, then beta_a=partial ln e_obs/partial X_a=0 and the direct finite-range matter readout vanishes at first order.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM_NOT_PARENT_SIGNED",
            "proof_sketch": "Vary S_matter through e_obs. If delta_X e_obs=0 and no direct X_a matter vertex exists, the first variation with respect to X_a has no matter-source term.",
            "claim_effect": "would give alpha_a=0 for the direct matter readout, but parent coframe-independence is still open",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1503_2_conditional_finite_coupling_formula",
            "statement": "If e_obs contains exp(beta_a X_a), and X_a obeys the 1502 Helmholtz template with source s_a rho and kinetic coefficient Z_a, then the point-source Yukawa amplitude is alpha_a = - beta_a s_a c^2/(4 pi G_N Z_a), subject to units and sign convention.",
            "proof_status": "CONDITIONAL_TEMPLATE_FORMULA_ONLY",
            "proof_sketch": "Solve (nabla^2-lambda_a^-2)X_a=-s_a rho/Z_a for a point source and read delta Phi=beta_a c^2 X_a against delta Phi=-G_N M alpha exp(-r/lambda)/r.",
            "claim_effect": "gives exact closure variables, not a claim-grade value",
            **flags(),
        },
    ]


def formula_rows() -> list[dict[str, Any]]:
    formulas = [
        ("FORM1503_0_Newton_calibration", "Phi_N=-G_N M/r", "measured common calibration only"),
        ("FORM1503_1_finite_Yukawa_potential", "delta Phi_a=-G_N M alpha_a exp(-r/lambda_a)/r", "R10 convention"),
        ("FORM1503_2_finite_Yukawa_acceleration", "delta a/a_N=alpha_a(1+r/lambda_a)exp(-r/lambda_a)", "cannot be absorbed into constant G_N"),
        ("FORM1503_3_matter_readout", "delta Phi_a=beta_a c^2 X_a", "requires parent coframe/readout coefficient beta_a"),
        ("FORM1503_4_point_source_solution", "X_a(r)=s_a M exp(-r/lambda_a)/(4 pi Z_a r)", "conditional on 1502 Helmholtz template"),
        ("FORM1503_5_alpha_map", "alpha_a=-beta_a s_a c^2/(4 pi G_N Z_a)", "conditional and unit/sign dependent"),
        ("FORM1503_6_R10_comparison", "|sum_a alpha_a tau_R10_a(lambda_i) delta_w_a| <= alpha_bound(lambda_i)", "closure-bound comparison only"),
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


def bound_row_contract_rows() -> list[dict[str, Any]]:
    fields = [
        ("schema_version", "string", "R10_COUPLING_CLOSURE_BOUND_1503"),
        ("same_parent_branch_id", "string", BRANCH_ID),
        ("component_id", "string", "stable residual component id"),
        ("lambda_value", "positive_float", "range in declared units"),
        ("lambda_units", "string", "m or converted unit"),
        ("delta_w_a", "float_or_derived_zero", "residual amplitude"),
        ("Z_a", "float_or_derived_zero", "kinetic normalization"),
        ("s_a", "float_or_derived_zero", "source coupling"),
        ("beta_a", "float_or_derived_zero", "matter readout coefficient"),
        ("alpha_predicted", "float_or_derived_zero", "same-frame Yukawa amplitude"),
        ("tau_R10_a", "float_or_derived_zero", "finite-source geometry response"),
        ("alpha_bound", "positive_float", "reviewed R10 alpha(lambda) bound"),
        ("source_paths", "path_list", "local files/URLs/DOIs for every coefficient"),
        ("parent_status", "enum", "PARENT_DERIVED|DERIVED_ZERO|SOURCE_BACKED_NUMERIC|CLOSURE_NONCLAIM"),
        ("valid_for_claim", "boolean", "false unless all fields are real and sourced"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "field": field,
            "type": type_name,
            "required_value_or_policy": policy,
            "current_status": "SCHEMA_ONLY_NONCLAIM",
            **flags(),
        }
        for field, type_name, policy in fields
    ]


def zero_route_rows() -> list[dict[str, Any]]:
    clauses = [
        ("BZ1503_0_single_coframe", "all ordinary matter varies through one e_obs", "SUPPORTED_CONTRACT_NOT_PARENT_GLOBAL"),
        ("BZ1503_1_no_direct_X_vertex", "no X_a psi psi, X_a F^2, or source-only scalar matter vertex", "POLICY_ONLY_NOT_PARENT_SIGNED"),
        ("BZ1503_2_local_independence", "partial e_obs / partial X_a = 0 at compact local branch", "MISSING"),
        ("BZ1503_3_variation_before_readout", "vary parent matter action before arena readout/projection", "CONTRACT_ONLY"),
        ("BZ1503_4_boundary_projection_silence", "boundary/readout maps do not reintroduce beta_a", "MISSING"),
        ("BZ1503_5_beta_zero_verdict", "beta_a=0 for every R10-active residual component", "NOT_PARENT_DERIVED"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "zero_route_id": clause_id,
            "required_clause": clause,
            "current_status": status,
            "effect_if_closed": "direct matter Yukawa alpha is theorem-zero",
            "effect_if_open": "beta_a remains explicit closure coefficient",
            **flags(),
        }
        for clause_id, clause, status in clauses
    ]


def blocker_rows() -> list[dict[str, Any]]:
    blockers = [
        ("BLK1503_0_beta", "MISSING_BETA_A_PARENT_READOUT", "beta_a is not fixed by Newton limit", "parent_action"),
        ("BLK1503_1_source", "MISSING_S_A_SOURCE_COUPLING", "s_a rho source normalization remains parent-unsigned", "parent_action"),
        ("BLK1503_2_Z", "MISSING_Z_A_NORMALIZATION", "Z_a sets alpha normalization and is not sourced", "parent_action"),
        ("BLK1503_3_same_frame_zero", "MISSING_EOBS_INDEPENDENCE_PROOF", "beta_a=0 requires parent proof that e_obs has no local X_a dependence", "parent_action"),
        ("BLK1503_4_geometry", "MISSING_TAU_R10_GEOMETRY", "R10 extended-source response is not computed", rel(KERNEL_TARGET)),
        ("BLK1503_5_curve", "MISSING_REVIEWED_R10_BOUND_CURVE", "R10 curve is visual nonclaim only", rel(CURVE_TARGET)),
        ("BLK1503_6_import", "MISSING_C_PARENT_IMPORT", "no live coefficient row satisfies source/units/sign/basis requirements", rel(C_PARENT_IMPORT)),
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
            f"{prefix}_id": f"{prefix.upper()}1503_{index}",
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
            "refusal_id": "CP1503_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "1503 proves Newton calibration cannot define beta_a/C_a and does not fabricate a coefficient",
            "claim_effect": "R10/local-GR claim remains blocked",
            **flags(),
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        ("DEC1503_0_newton_no_go", "do not derive C_a from Newton calibration alone", "finite-range kernels are not constant G_N renormalizations"),
        ("DEC1503_1_zero_route_preferred", "attack beta_a=0 via observed-coframe independence", "a theorem-zero is cleaner than a fitted finite coupling"),
        ("DEC1503_2_closure_if_zero_fails", "retain beta_a*s_a/Z_a as explicit closure-bound row", "that is the honest empirical fallback"),
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
            "next_id": "NEXT1503_0_1504",
            "next_target": "1504-Y5-R10-RAB-observed-coframe-independence-beta-zero-or-explicit-coupling-bound.md",
            "script": "scripts/Y5_R10_RAB_observed_coframe_independence_beta_zero_or_explicit_coupling_bound.py",
            "objective": "try to prove partial e_obs / partial X_a = 0 in the compact local branch; if not, emit beta_a as an explicit closure-bound input",
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
        (NEWTON_AUDIT, QUAR_NEWTON),
        (COUPLING_THEOREM, QUAR_THEOREM),
        (FORMULA_REGISTER, QUAR_FORMULA),
        (BOUND_ROW_CONTRACT, QUAR_BOUND),
        (NEWTON_AUDIT, BRANCH_NEWTON),
        (COUPLING_THEOREM, BRANCH_THEOREM),
        (FORMULA_REGISTER, BRANCH_FORMULA),
        (BOUND_ROW_CONTRACT, BRANCH_BOUND),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], theorem: list[dict[str, Any]], zero_route: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    newton_no_go = any(row["theorem_id"] == "THM1503_0_no_newton_unique_finite_coupling" and row["proof_status"] == "DERIVED_AS_NO_GO_FOR_NEWTON_ONLY" for row in theorem)
    beta_zero_not_parent = any(row["zero_route_id"] == "BZ1503_5_beta_zero_verdict" and row["current_status"] == "NOT_PARENT_DERIVED" for row in zero_route)
    closure_contract = BOUND_ROW_CONTRACT.exists() and len(read_csv(BOUND_ROW_CONTRACT)) >= 12
    live_targets_absent = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = all(parse_csv(path) for path in generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_NEWTON, QUAR_THEOREM, QUAR_FORMULA, QUAR_BOUND, BRANCH_NEWTON, BRANCH_THEOREM, BRANCH_FORMULA, BRANCH_BOUND])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1503_0_local_sources", source_paths_exist, "all cited coupling/Newton source paths exist"),
        ("VAL1503_1_newton_no_go", newton_no_go, "Newton limit does not determine finite Yukawa coupling"),
        ("VAL1503_2_beta_zero_not_parent", beta_zero_not_parent, "beta zero route remains unclaimed"),
        ("VAL1503_3_closure_contract", closure_contract, "explicit coupling closure-bound schema written"),
        ("VAL1503_4_live_targets_absent", live_targets_absent, "live R10 curve/kernel targets remain absent"),
        ("VAL1503_5_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1503_6_csv_parse", csv_parse_ok, "all generated 1503 CSVs parse cleanly"),
        ("VAL1503_7_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1503_8_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1503_9_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1503_10_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1503_11_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1503 rejected Newton-only coupling derivation and converted beta/C into a precise zero-or-bound obligation"
            if overall
            else "1503 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join(output)


def write_doc(
    audit: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    formulas: list[dict[str, Any]],
    zero_route: list[dict[str, Any]],
    bound_contract: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1503 - Matter Coupling Normalization from Newton Limit or Closure Bound",
                "",
                "## Verdict",
                "- The Newton limit fixes the common measured inverse-square normalization, not a finite-range Yukawa amplitude.",
                "- A direct R10 matter coupling is zero only if the parent action proves observed-coframe independence from the residual field.",
                "- Otherwise beta_a s_a / Z_a remains an explicit closure-bound input; no C_parent import or R10/local-GR claim is made.",
                "",
                "## Newton Limit Coupling Audit",
                md_table(audit, ["audit_id", "object", "formula", "status", "derived_or_calibrated"]),
                "",
                "## Coupling Theorem",
                md_table(theorem, ["theorem_id", "proof_status", "claim_effect"]),
                "",
                "## Formula Register",
                md_table(formulas, ["formula_id", "formula", "status"]),
                "",
                "## Beta Zero Route",
                md_table(zero_route, ["zero_route_id", "required_clause", "current_status", "effect_if_open"]),
                "",
                "## Closure Bound Row Contract",
                md_table(bound_contract, ["field", "type", "required_value_or_policy", "current_status"]),
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
    audit = newton_audit_rows()
    theorem = theorem_rows()
    formulas = formula_rows()
    bound_contract = bound_row_contract_rows()
    zero_route = zero_route_rows()
    blockers = blocker_rows()
    readiness = simple_rows_from_blockers(blockers, "ready")
    c_parent = c_parent_refusal_rows()
    local_rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LRS1503_0",
            "object": "R10/local Newton coupling branch",
            "status": "BETA_ZERO_OR_CLOSURE_BOUND_REQUIRED",
            "effect": "Newton calibration alone rejected; no local-GR/Newton/R10 claim",
            **flags(),
        }
    ]
    rejections = simple_rows_from_blockers(blockers, "rejection")
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(NEWTON_AUDIT, audit)
    write_csv(COUPLING_THEOREM, theorem)
    write_csv(FORMULA_REGISTER, formulas)
    write_csv(BOUND_ROW_CONTRACT, bound_contract)
    write_csv(ZERO_ROUTE, zero_route)
    write_csv(TARGET_BLOCKERS, blockers)
    write_csv(SCORE_READINESS, readiness)
    write_csv(C_PARENT_REFUSAL, c_parent)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()

    generated_csvs = [
        NEWTON_AUDIT,
        COUPLING_THEOREM,
        FORMULA_REGISTER,
        BOUND_ROW_CONTRACT,
        ZERO_ROUTE,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, theorem, zero_route)
    write_csv(VALIDATION, validation)
    write_doc(audit, theorem, formulas, zero_route, bound_contract, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
