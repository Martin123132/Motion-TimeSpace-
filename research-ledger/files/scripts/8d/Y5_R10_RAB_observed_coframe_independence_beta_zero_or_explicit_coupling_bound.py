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
DOC = ROOT / "1504-Y5-R10-RAB-observed-coframe-independence-beta-zero-or-explicit-coupling-bound.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1503_validation": OUT / "P8_Y5_BRR545_1503_VALIDATION.csv",
    "1503_beta_zero_route": OUT / "P8_Y5_R10_1503_BETA_ZERO_ROUTE_AUDIT.csv",
    "1503_formula": OUT / "P8_Y5_R10_1503_COUPLING_FORMULA_REGISTER.csv",
    "1503_bound_contract": OUT / "P8_Y5_R10_1503_COUPLING_CLOSURE_BOUND_ROW_CONTRACT.csv",
    "matter_action_contract": ROOT / "runs" / "20260601-191500-universal-matter-coupling-theorem-attempt" / "results" / "matter_action_contract.csv",
    "matter_action_candidates": ROOT / "runs" / "20260601-211000-representative-invariant-matter-action-for-lifted-C" / "results" / "matter_action_candidates.csv",
    "one_observed_coframe_contract": ROOT / "runs" / "20260601-233000-one-observed-coframe-parent-selector-or-WEP-closure" / "results" / "parent_action_contract.csv",
    "one_observed_coframe_no_go": ROOT / "runs" / "20260601-233000-one-observed-coframe-parent-selector-or-WEP-closure" / "results" / "no_go_steps.csv",
    "one_observed_coframe_gates": ROOT / "runs" / "20260601-233000-one-observed-coframe-parent-selector-or-WEP-closure" / "results" / "gate_results.csv",
    "pullback_theorem_attempt": ROOT / "runs" / "20260602-013500-observed-coframe-selector-pullback-cancellation-theorem" / "results" / "theorem_attempts.csv",
    "same_frame_allowed_forms": ROOT / "runs" / "20260602-113000-same-frame-matter-functor-zero-route" / "results" / "allowed_matter_action_forms.csv",
}

CURVE_TARGET = R10 / "derived" / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"
KERNEL_TARGET = R10 / "derived" / "R10_delta_w_kernel_lambda.csv"
C_PARENT_IMPORT = BRANCH_COEFF / "C_parent_WEP_slot_import.csv"

COFRAME_AUDIT = OUT / "P8_Y5_R10_1504_OBSERVED_COFRAME_INDEPENDENCE_AUDIT.csv"
BETA_ZERO_THEOREM = OUT / "P8_Y5_R10_1504_BETA_ZERO_THEOREM_OR_COUNTERMODEL.csv"
BETA_CLOSURE = OUT / "P8_Y5_R10_1504_BETA_CLOSURE_BOUND_INPUT_ROWS.csv"
VERTICALITY_CONTRACT = OUT / "P8_Y5_R10_1504_R10_RESIDUAL_VERTICALITY_CONTRACT.csv"
FORMULA_REGISTER = OUT / "P8_Y5_R10_1504_FORMULA_REGISTER.csv"
TARGET_BLOCKERS = OUT / "P8_Y5_R10_1504_TARGET_PROMOTION_BLOCKERS.csv"
SCORE_READINESS = OUT / "P8_Y5_R10_1504_DELTA_W_SCORE_READINESS.csv"
C_PARENT_REFUSAL = OUT / "P8_Y5_R10_1504_C_PARENT_IMPORT_REFUSAL.csv"
LOCAL_STATUS = OUT / "P8_Y5_R10_1504_LOCAL_GR_NEWTON_STATUS.csv"
REJECTION_LEDGER = OUT / "P8_Y5_R10_1504_REJECTION_LEDGER.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1504_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1504_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1504_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1504"
QUAR_AUDIT = QUARANTINE / "OBSERVED_COFRAME_INDEPENDENCE_AUDIT_NONCLAIM.csv"
QUAR_THEOREM = QUARANTINE / "BETA_ZERO_THEOREM_OR_COUNTERMODEL_NONCLAIM.csv"
QUAR_CLOSURE = QUARANTINE / "BETA_CLOSURE_BOUND_INPUT_ROWS_NONCLAIM.csv"
QUAR_VERTICALITY = QUARANTINE / "R10_RESIDUAL_VERTICALITY_CONTRACT_NONCLAIM.csv"
BRANCH_AUDIT = BRANCH_RESIDUALS / "r10_observed_coframe_independence_audit_nonclaim_1504.csv"
BRANCH_THEOREM = BRANCH_RESIDUALS / "r10_beta_zero_theorem_or_countermodel_nonclaim_1504.csv"
BRANCH_CLOSURE = BRANCH_RESIDUALS / "r10_beta_closure_bound_input_rows_nonclaim_1504.csv"
BRANCH_VERTICALITY = BRANCH_RESIDUALS / "r10_residual_verticality_contract_nonclaim_1504.csv"


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


def coframe_audit_rows() -> list[dict[str, Any]]:
    steps = [
        (
            "OC1504_0_single_coframe_contract",
            "single observed coframe",
            "S_matter=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A]",
            "conditional contract exists but was previously not parent-selected",
            "CONDITIONAL_CONTRACT",
            False,
        ),
        (
            "OC1504_1_fixed_coframe_variation",
            "fixed e_obs residual variation",
            "(delta S_matter/delta X_a)|e_obs,Psi = 0",
            "exact if X_a is absent from e_obs and no direct X_a matter vertex exists",
            "EXACT_CONDITIONAL_MATH",
            True,
        ),
        (
            "OC1504_2_vertical_pullback",
            "quotient vertical residual",
            "Dq[X_a]=0 and e_obs=e(q(Phi)) => partial_X e_obs=0",
            "would close beta_a=0 for R10-active X_a if the residual is mapped into ker(Dq)",
            "EXACT_CONDITIONAL_MATH",
            True,
        ),
        (
            "OC1504_3_universal_conformal_countermodel",
            "same coframe but X-visible",
            "e_obs=exp(beta_a X_a)e_0",
            "one universal coframe can still carry a fifth-force beta_a without species splitting",
            "COUNTERMODEL_SURVIVES",
            False,
        ),
        (
            "OC1504_4_common_class_metric",
            "representative-invariant common class metric",
            "e_obs=exp(F(C_D))e_0",
            "representative invariance alone allows F'(C_D) nonzero, so beta does not vanish unless a local extremum/selector theorem forces it",
            "UNDERSELECTED",
            False,
        ),
        (
            "OC1504_5_parent_selector",
            "parent selection of e_obs",
            "Euler/constraint equation forces e_obs independent of R10-active residuals",
            "not found in current parent-action evidence",
            "MISSING_PARENT_SELECTOR",
            False,
        ),
        (
            "OC1504_6_boundary_readout",
            "arena readout silence",
            "readout/boundary maps do not reintroduce beta_a after variation",
            "still open for R10 finite-source projection",
            "MISSING_ARENA_SILENCE",
            False,
        ),
        (
            "OC1504_7_verdict",
            "beta zero status",
            "beta_a=0",
            "proved only under quotient-vertical/coframe-independence premises; not parent-derived for the current R10 branch",
            "NOT_PARENT_DERIVED",
            False,
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "object": obj,
            "formula": formula,
            "status_detail": detail,
            "status": status,
            "mathematically_sufficient_if_parent_owned": sufficient,
            **flags(),
        }
        for audit_id, obj, formula, detail, status, sufficient in steps
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1504_0_vertical_pullback_beta_zero",
            "statement": "If e_obs factors through the quotient q(Phi), the R10-active residual direction X_a is vertical in ker(Dq), and there is no direct X_a matter vertex at fixed e_obs, then beta_a=partial ln e_obs/partial X_a=0.",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "proof_sketch": "By the chain rule, delta_X e_obs = De_obs[Dq[X_a]]. If Dq[X_a]=0, the matter action has no first-order X_a variation through e_obs; fixed-coframe direct vertices are excluded by premise.",
            "current_claim_status": "NOT_PARENT_SIGNED_FOR_R10_X",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1504_1_single_coframe_not_enough",
            "statement": "One observed coframe alone does not prove beta_a=0 because a universal X-dependent coframe e_obs=exp(beta_a X_a)e_0 is still a single coframe and can produce a composition-blind finite-range force.",
            "proof_status": "COUNTERMODEL_ACTIVE",
            "proof_sketch": "The matter action remains universal, but varying X_a changes e_obs and hence the test-body potential. This can evade species WEP while still failing R10/fifth-force bounds.",
            "current_claim_status": "BLOCKS_BETA_ZERO_FROM_ONE_COFRAME_ALONE",
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "theorem_id": "THM1504_2_current_branch_verdict",
            "statement": "The present branch has a useful beta-zero lemma but has not mapped every R10-active residual field into the quotient-vertical kernel or proved the selector equation that removes X_a from e_obs.",
            "proof_status": "DERIVED_AS_GATE_LOGIC",
            "proof_sketch": "Existing source files give one-coframe contracts and pullback-cancellation attempts, but also prior no-go rows saying parent selection is not derived.",
            "current_claim_status": "KEEP_BETA_A_CLOSURE_BOUND",
            **flags(),
        },
    ]


def beta_closure_rows() -> list[dict[str, Any]]:
    rows = [
        ("BETA1504_0_direct_readout", "beta_a", "partial ln e_obs / partial X_a", "MISSING_OR_DERIVED_ZERO_REQUIRED"),
        ("BETA1504_1_source_coupling", "s_a", "source coefficient in Helmholtz equation", "MISSING_OR_DERIVED_ZERO_REQUIRED"),
        ("BETA1504_2_kinetic_norm", "Z_a", "kinetic/operator normalization", "MISSING_OR_DERIVED_ZERO_REQUIRED"),
        ("BETA1504_3_product", "C_a", "-beta_a s_a c^2/(4 pi G_N Z_a)", "CLOSURE_PRODUCT_NONCLAIM"),
        ("BETA1504_4_alpha", "alpha_a(lambda)", "C_a times residual/geometric response convention", "NOT_SCORE_READY"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "closure_id": closure_id,
            "symbol": symbol,
            "definition": definition,
            "current_status": status,
            "source_path": "MISSING_SOURCE_FILE",
            **flags(),
        }
        for closure_id, symbol, definition, status in rows
    ]


def verticality_contract_rows() -> list[dict[str, Any]]:
    rows = [
        ("VC1504_0_define_q", "q: parent fields -> observed coframe/metric data", "explicit parent quotient map", "PARTIAL_PRIOR_CONTRACT"),
        ("VC1504_1_define_X", "X_a or delta_w_a", "R10-active residual field direction in parent tangent space", "MISSING_R10_FIELD_MAP"),
        ("VC1504_2_kernel_test", "Dq[X_a]=0", "verticality condition for beta-zero lemma", "MISSING"),
        ("VC1504_3_direct_vertex_test", "delta_X S_matter|e_obs=0", "no direct fixed-coframe matter vertex", "CONDITIONAL_POLICY_ONLY"),
        ("VC1504_4_readout_test", "delta_X R_R10=0 after variation", "arena projection does not reintroduce beta", "MISSING"),
        ("VC1504_5_acceptance", "beta_a=0", "allowed only if VC1504_0 through VC1504_4 close", "BLOCKED"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "symbol": symbol,
            "requirement": requirement,
            "current_status": status,
            **flags(),
        }
        for contract_id, symbol, requirement, status in rows
    ]


def formula_rows() -> list[dict[str, Any]]:
    formulas = [
        ("FORM1504_0_chain_rule", "delta_X e_obs = De_obs[Dq[X_a]]", "core beta-zero mechanism"),
        ("FORM1504_1_beta_definition", "beta_a = partial ln e_obs / partial X_a", "direct matter readout coefficient"),
        ("FORM1504_2_beta_zero", "Dq[X_a]=0 and no direct vertex => beta_a=0", "exact conditional theorem"),
        ("FORM1504_3_countermodel", "e_obs=exp(beta_a X_a)e_0 with beta_a != 0", "single coframe counterexample"),
        ("FORM1504_4_alpha_product", "alpha_a=-beta_a s_a c^2/(4 pi G_N Z_a)", "kept closure-only while beta_a open"),
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
        ("BLK1504_0_X_map", "MISSING_R10_ACTIVE_X_PARENT_FIELD_MAP", "R10-active residual has not been identified as a parent tangent/vector field", "parent_action"),
        ("BLK1504_1_verticality", "MISSING_DQ_X_ZERO_PROOF", "Dq[X_a]=0 is the exact beta-zero condition", "parent_action"),
        ("BLK1504_2_selector", "MISSING_OBSERVED_COFRAME_SELECTOR_EQUATION", "parent action has not forced e_obs independent of X_a", "parent_action"),
        ("BLK1504_3_direct_vertex", "MISSING_NO_DIRECT_X_VERTEX_PARENT_PROOF", "fixed-coframe direct matter vertices remain policy-only", "parent_action"),
        ("BLK1504_4_readout", "MISSING_R10_READOUT_SILENCE", "R10 projection could reintroduce beta-like response", rel(KERNEL_TARGET)),
        ("BLK1504_5_beta_bound", "MISSING_BETA_BOUND_INPUT", "if beta is finite it needs sourced numeric/derived-zero row", rel(C_PARENT_IMPORT)),
        ("BLK1504_6_curve", "MISSING_REVIEWED_R10_BOUND_CURVE", "R10 alpha(lambda) bound remains non-live", rel(CURVE_TARGET)),
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
            f"{prefix}_id": f"{prefix.upper()}1504_{index}",
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
            "refusal_id": "CP1504_0_no_import",
            "path": rel(C_PARENT_IMPORT),
            "path_exists": C_PARENT_IMPORT.exists(),
            "imported_now": False,
            "reason": "1504 proves only a conditional beta-zero lemma; no live beta/C coefficient is imported",
            "claim_effect": "R10/local-GR claim remains blocked",
            **flags(),
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    decisions = [
        ("DEC1504_0_exact_lemma_kept", "keep the vertical-pullback beta-zero lemma", "it is mathematically clean and gives the next derivation target"),
        ("DEC1504_1_no_one_coframe_shortcut", "do not infer beta_a=0 from one observed coframe alone", "universal conformal countermodel survives"),
        ("DEC1504_2_next", "map R10-active residual X_a into ker(Dq) or keep beta closure", "this is the least handwavy next proof obligation"),
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
            "next_id": "NEXT1504_0_1505",
            "next_target": "1505-Y5-R10-RAB-map-R10-residual-X-to-quotient-vertical-kernel-or-beta-bound.md",
            "script": "scripts/Y5_R10_RAB_map_R10_residual_X_to_quotient_vertical_kernel_or_beta_bound.py",
            "objective": "try to prove Dq[X_a]=0 for the R10-active residual; if not, keep beta_a as a sourced closure-bound coefficient",
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
        (COFRAME_AUDIT, QUAR_AUDIT),
        (BETA_ZERO_THEOREM, QUAR_THEOREM),
        (BETA_CLOSURE, QUAR_CLOSURE),
        (VERTICALITY_CONTRACT, QUAR_VERTICALITY),
        (COFRAME_AUDIT, BRANCH_AUDIT),
        (BETA_ZERO_THEOREM, BRANCH_THEOREM),
        (BETA_CLOSURE, BRANCH_CLOSURE),
        (VERTICALITY_CONTRACT, BRANCH_VERTICALITY),
    ]:
        shutil.copyfile(src, dst)


def validation_rows(generated_csvs: list[Path], theorem: list[dict[str, Any]], audit: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_paths_exist = all(path.exists() for path in SOURCE_FILES.values())
    exact_lemma = any(row["theorem_id"] == "THM1504_0_vertical_pullback_beta_zero" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem)
    countermodel = any(row["theorem_id"] == "THM1504_1_single_coframe_not_enough" and row["proof_status"] == "COUNTERMODEL_ACTIVE" for row in theorem)
    not_parent_derived = any(row["audit_id"] == "OC1504_7_verdict" and row["status"] == "NOT_PARENT_DERIVED" for row in audit)
    closure_rows = BETA_CLOSURE.exists() and len(read_csv(BETA_CLOSURE)) >= 5
    live_targets_absent = not CURVE_TARGET.exists() and not KERNEL_TARGET.exists()
    c_parent_refused = read_csv(C_PARENT_REFUSAL)[0]["imported_now"] == "False"
    csv_parse_ok = all(parse_csv(path) for path in generated_csvs)
    flags_false = generated_flags_false(generated_csvs)
    branch_copies = all(path.exists() for path in [QUAR_AUDIT, QUAR_THEOREM, QUAR_CLOSURE, QUAR_VERTICALITY, BRANCH_AUDIT, BRANCH_THEOREM, BRANCH_CLOSURE, BRANCH_VERTICALITY])
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    pycache_absent = not pycache.exists()
    formalization_modified = 0
    if FORMALIZATION.exists():
        formalization_modified = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime > START_TS)
    checks = [
        ("VAL1504_0_local_sources", source_paths_exist, "all cited coframe/coupling source paths exist"),
        ("VAL1504_1_exact_lemma", exact_lemma, "vertical-pullback beta-zero lemma recorded"),
        ("VAL1504_2_countermodel", countermodel, "one-coframe-alone countermodel recorded"),
        ("VAL1504_3_beta_not_parent_derived", not_parent_derived, "beta zero is not claimed for current R10 branch"),
        ("VAL1504_4_closure_rows", closure_rows, "beta closure-bound rows written"),
        ("VAL1504_5_live_targets_absent", live_targets_absent, "live R10 curve/kernel targets remain absent"),
        ("VAL1504_6_Cparent_refused", c_parent_refused, "C_parent import was not performed"),
        ("VAL1504_7_csv_parse", csv_parse_ok, "all generated 1504 CSVs parse cleanly"),
        ("VAL1504_8_branch_copies", branch_copies, "branch/quarantine nonclaim copies written"),
        ("VAL1504_9_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1504_10_formalization_untouched", formalization_modified == 0, f"formalization modified-file count since start={formalization_modified}"),
        ("VAL1504_11_claim_flags_false", flags_false, "all generated prediction/claim flags remain false"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {"same_parent_branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if result else "FAIL", "detail": detail}
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1504_12_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1504 proved the conditional beta-zero route but rejected one-coframe-alone as a parent proof"
            if overall
            else "1504 validation failed; inspect failed rows before continuing",
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
    verticality: list[dict[str, Any]],
    beta_closure: list[dict[str, Any]],
    formulas: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1504 - Observed Coframe Independence beta Zero or Explicit Coupling Bound",
                "",
                "## Verdict",
                "- beta_a=0 is exactly derivable if the R10 residual is quotient-vertical: Dq[X_a]=0 and matter has no direct fixed-coframe X_a vertex.",
                "- One observed coframe alone is not enough, because e_obs=exp(beta_a X_a)e_0 is still universal but produces a finite-range force.",
                "- Current MTS has the clean lemma but not the parent map Dq[X_a]=0, so beta_a remains closure-bound for now.",
                "",
                "## Coframe Independence Audit",
                md_table(audit, ["audit_id", "object", "formula", "status", "mathematically_sufficient_if_parent_owned"]),
                "",
                "## beta Zero Theorem or Countermodel",
                md_table(theorem, ["theorem_id", "proof_status", "current_claim_status"]),
                "",
                "## R10 Residual Verticality Contract",
                md_table(verticality, ["contract_id", "symbol", "requirement", "current_status"]),
                "",
                "## beta Closure Rows",
                md_table(beta_closure, ["closure_id", "symbol", "definition", "current_status"]),
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
    audit = coframe_audit_rows()
    theorem = theorem_rows()
    beta_closure = beta_closure_rows()
    verticality = verticality_contract_rows()
    formulas = formula_rows()
    blockers = blocker_rows()
    readiness = simple_rows_from_blockers(blockers, "ready")
    c_parent = c_parent_refusal_rows()
    local_rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "local_status_id": "LRS1504_0",
            "object": "R10 beta-zero/local coupling branch",
            "status": "VERTICALITY_PROOF_OR_BETA_BOUND_REQUIRED",
            "effect": "beta-zero lemma sharpened; no local-GR/Newton/R10 claim",
            **flags(),
        }
    ]
    rejections = simple_rows_from_blockers(blockers, "rejection")
    decisions = decision_rows()
    next_rows = next_target_rows()

    write_csv(COFRAME_AUDIT, audit)
    write_csv(BETA_ZERO_THEOREM, theorem)
    write_csv(BETA_CLOSURE, beta_closure)
    write_csv(VERTICALITY_CONTRACT, verticality)
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
        COFRAME_AUDIT,
        BETA_ZERO_THEOREM,
        BETA_CLOSURE,
        VERTICALITY_CONTRACT,
        FORMULA_REGISTER,
        TARGET_BLOCKERS,
        SCORE_READINESS,
        C_PARENT_REFUSAL,
        LOCAL_STATUS,
        REJECTION_LEDGER,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs, theorem, audit)
    write_csv(VALIDATION, validation)
    write_doc(audit, theorem, verticality, beta_closure, formulas, validation, next_rows)
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


if __name__ == "__main__":
    main()
