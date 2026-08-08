from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_epsilon_TF_numerator_denominator_contract_written_first_fill_row_unfilled_nonclaim"
CLAIM_CEILING = "epsilon_TF_contract_and_first_fill_row_only_no_epsilon_value_no_Cgamma_score_no_PPN_R10_no_local_GR_claim"
NEXT_TARGET = "695-Y5-R10-BTF-over-MH-theorem-zero-or-source-bound-acquisition.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "694-Y5-R10-epsilon-TF-numerator-denominator-contract-or-first-fill-row.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "234_doc": ROOT / "234-boundary-metric-variation-and-Bianchi-ledger.md",
    "352_doc": ROOT / "352-boundary-nohair-and-PPN-residual-vector-gate.md",
    "357_doc": ROOT / "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
    "549_doc": ROOT / "549-Y5-boundary-cohomology-nohair-certificate-or-boundary-flux-bound-fill.md",
    "678_doc": ROOT / "678-Y5-R10-boundary-class-nohair-projector-silence-or-BX-source-row.md",
    "691_doc": ROOT / "691-Y5-R10-shear-channel-bound-source-pack-or-boundary-nohair-theorem.md",
    "692_doc": ROOT / "692-Y5-R10-metric-shear-bound-runner-from-PPN-slip-source-lock.md",
    "693_doc": ROOT / "693-Y5-R10-TF-shear-to-gamma-slip-coefficient-derivation-or-retained-bound.md",
    "549_validation": RESIDUALS / "P8_Y5_BRR545_549_VALIDATION.csv",
    "678_validation": RESIDUALS / "P8_Y5_BRR545_678_VALIDATION.csv",
    "691_validation": RESIDUALS / "P8_Y5_BRR545_691_VALIDATION.csv",
    "692_validation": RESIDUALS / "P8_Y5_BRR545_692_VALIDATION.csv",
    "693_validation": RESIDUALS / "P8_Y5_BRR545_693_VALIDATION.csv",
    "691_source_pack": RESIDUALS / "P8_Y5_R10_691_SHEAR_CHANNEL_BOUND_SOURCE_PACK.csv",
    "691_observable_map": RESIDUALS / "P8_Y5_R10_691_OBSERVABLE_MAP.csv",
    "692_inputs": RESIDUALS / "P8_Y5_R10_692_METRIC_SHEAR_RUNNER_INPUTS.csv",
    "693_operator_contract": RESIDUALS / "P8_Y5_R10_693_OPERATOR_NORM_CONTRACT.csv",
    "693_retained_template": RESIDUALS / "P8_Y5_R10_693_RETAINED_BOUND_TEMPLATE.csv",
    "boundary_reference_status": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def source_list(*source_ids: str) -> str:
    return ";".join(str(SOURCE_PATHS[source_id]) for source_id in source_ids)


def validation_failures_for(source_id: str) -> list[dict[str, str]]:
    path = SOURCE_PATHS[source_id]
    if not path.exists():
        return [{"check_id": "MISSING_VALIDATION_FILE", "result": "fail", "detail": str(path)}]
    return [row for row in read_csv(path) if row.get("result") != "pass"]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    return sum(
        1
        for candidate_path in FORMALIZATION_WORKBENCH.rglob("*")
        if candidate_path.is_file()
        and datetime.fromtimestamp(candidate_path.stat().st_mtime) > FORMALIZATION_CUTOFF
    )


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    roles = {
        "234_doc": "Bianchi ledger: Pi_TF/projector stress must vanish or be retained",
        "352_doc": "boundary residual split with B_TF feeding gamma/slip",
        "357_doc": "retained PPN residual vector with epsilon_TF terms",
        "549_doc": "boundary cohomology/nohair failure and first boundary-flux row pattern",
        "678_doc": "boundary-class/projector/nohair silence stack failure",
        "691_doc": "metric shear source pack predecessor",
        "692_doc": "source-locked guardrail runner predecessor",
        "693_doc": "operator-norm coefficient contract predecessor",
        "549_validation": "549 validation gate",
        "678_validation": "678 validation gate",
        "691_validation": "691 validation gate",
        "692_validation": "692 validation gate",
        "693_validation": "693 validation gate",
        "691_source_pack": "metric shear source pack rows",
        "691_observable_map": "observable map rows",
        "692_inputs": "epsilon_TF input placeholders",
        "693_operator_contract": "operator norm contract rows",
        "693_retained_template": "retained bound template rows",
        "boundary_reference_status": "M_H_ref denominator status",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": bool_text(path.exists()),
            "role": roles[source_id],
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def epsilon_definition_contract_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "contract_id": "EDC694_0_definition",
            "clause": "epsilon_TF definition",
            "formula": "epsilon_TF := N_TF / D_TF",
            "required_inputs": "N_TF physical trace-free numerator;D_TF same-frame denominator",
            "current_status": "definition_written_not_filled",
            "valid_for_claim": "false",
            "source_paths": source_list("693_operator_contract", "692_inputs"),
            "generated_utc": now,
        },
        {
            "contract_id": "EDC694_1_numerator",
            "clause": "physical numerator only",
            "formula": "N_TF >= ||B_TF_obs|| + ||T_projector_TF|| + ||B_TF_profile|| + ||R11_TF||",
            "required_inputs": "B_TF boundary stress;projector TF stress;profile terms;retained operator terms",
            "current_status": "MISSING_NUMERATOR_COMPONENTS",
            "valid_for_claim": "false",
            "source_paths": source_list("234_doc", "352_doc", "691_source_pack"),
            "generated_utc": now,
        },
        {
            "contract_id": "EDC694_2_denominator",
            "clause": "same-frame denominator",
            "formula": "D_TF = M_H_ref or explicitly declared same-frame M_ref candidate",
            "required_inputs": "M_H_ref/source mass/reference convention/counterterm guard",
            "current_status": "MISSING_CLAIM_READY_DENOMINATOR",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "678_doc"),
            "generated_utc": now,
        },
        {
            "contract_id": "EDC694_3_no_projection_shortcut",
            "clause": "projected shear cannot fill numerator",
            "formula": "P_coh/J_C tracefree silence is excluded from N_TF unless lifted to observed metric shear theorem",
            "required_inputs": "metric shear theorem or source-backed metric residual",
            "current_status": "SCHEMA_ONLY_NONCLAIM_GUARD_ACTIVE",
            "valid_for_claim": "false",
            "source_paths": source_list("691_doc", "693_doc"),
            "generated_utc": now,
        },
        {
            "contract_id": "EDC694_4_theorem_zero_route",
            "clause": "epsilon_TF zero theorem",
            "formula": "epsilon_TF=0 only if all numerator components are theorem-zero and D_TF is fixed",
            "required_inputs": "boundary nohair;projector stress silence;R11/EH harmlessness;denominator",
            "current_status": "fail_current_corpus",
            "valid_for_claim": "false",
            "source_paths": source_list("691_doc", "549_doc", "678_doc"),
            "generated_utc": now,
        },
        {
            "contract_id": "EDC694_5_first_fill",
            "clause": "first executable fill row",
            "formula": "ETF694_0_epsilon_TF_first_fill carries missing numerator and denominator fields",
            "required_inputs": "source-backed value_or_theorem_zero for each numerator component plus D_TF",
            "current_status": "first_fill_row_written_unfilled",
            "valid_for_claim": "false",
            "source_paths": source_list("691_source_pack", "693_retained_template"),
            "generated_utc": now,
        },
    ]


def numerator_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        (
            "NUM694_0_B_TF_obs",
            "B_TF_obs_norm",
            "norm of physical observed boundary trace-free stress/shear source",
            "MISSING_B_TF_OVER_MH_VALUE_OR_THEOREM_ZERO",
            "dominant direct gamma/slip numerator candidate",
            "352_doc;691_source_pack",
        ),
        (
            "NUM694_1_projector_TF",
            "T_projector_TF_norm",
            "hidden/projector trace-free stress contribution after full metric variation",
            "MISSING_PROJECTOR_TF_STRESS_COEFFICIENT",
            "prevents dropping projector stress from Bianchi ledger",
            "234_doc;691_source_pack",
        ),
        (
            "NUM694_2_boundary_profile",
            "B_TF_profile_norm",
            "time/radial/frame profile of trace-free boundary term",
            "MISSING_SHEAR_BOUNDARY_PROFILE",
            "needed for beta/Gdot/frame leakage quarantine",
            "549_doc;691_source_pack",
        ),
        (
            "NUM694_3_R11_TF",
            "R11_TF_operator_norm",
            "retained non-EH trace-free operator contribution if EH/nohair branch fails",
            "MISSING_R11_TF_OPERATOR_MAP",
            "keeps non-EH fallback explicit",
            "693_retained_template;693_operator_contract",
        ),
        (
            "NUM694_4_cross_terms",
            "TF_cross_terms",
            "nonlinear or mixed radial/trace-free terms entering beta/gamma beyond linear shear",
            "MISSING_TF_CROSS_TERM_BOUND",
            "prevents false cancellation or undercounting",
            "357_doc;691_observable_map",
        ),
    ]
    return [
        {
            "numerator_id": numerator_id,
            "component": component,
            "definition": definition,
            "current_status": status,
            "why_needed": why_needed,
            "allowed_zero_route": "parent_theorem_zero_only_no_closure_credit",
            "valid_for_claim": "false",
            "source_paths": source_list(*source_ids_text.split(";")),
            "generated_utc": now,
        }
        for numerator_id, component, definition, status, why_needed, source_ids_text in rows
    ]


def denominator_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        (
            "DEN694_0_M_H_ref",
            "M_H_ref",
            "claim-ready Hamiltonian/source mass denominator in the observed frame",
            "MISSING_CLAIM_READY_M_H_REF",
            "preferred denominator for epsilon_TF",
        ),
        (
            "DEN694_1_M_ref_candidate",
            "M_ref_candidate",
            "fallback same-frame nonclaim denominator with explicit convention",
            "MISSING_SAME_FRAME_M_REF_CANDIDATE",
            "engineering fallback only if labelled nonclaim",
        ),
        (
            "DEN694_2_U_ref",
            "U_ref",
            "Newtonian/source potential normalization for gamma response",
            "MISSING_U_REF_OR_SOURCE_POTENTIAL",
            "needed to connect epsilon_TF to gamma coefficient",
        ),
        (
            "DEN694_3_counterterm_guard",
            "counterterm_reference_convention",
            "proof that boundary exact/counterterm choices do not subtract physical mass",
            "MISSING_COUNTERTERM_REFERENCE_GUARD",
            "prevents denominator/source subtraction trick",
        ),
        (
            "DEN694_4_same_frame_guard",
            "same_frame_guard",
            "source, clock, metric, boundary, and arena convention are identical",
            "MISSING_SAME_FRAME_CERTIFICATE",
            "prevents mixing numerator and denominator frames",
        ),
    ]
    return [
        {
            "denominator_id": denominator_id,
            "component": component,
            "definition": definition,
            "current_status": status,
            "why_needed": why_needed,
            "allowed_use_now": "nonclaim_template_only",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status", "678_doc", "693_retained_template"),
            "generated_utc": now,
        }
        for denominator_id, component, definition, status, why_needed in rows
    ]


def first_fill_row() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "fill_id": "ETF694_0_epsilon_TF_first_fill",
            "residual": "epsilon_TF",
            "formula": "N_TF/D_TF",
            "N_TF_components": "B_TF_obs_norm;T_projector_TF_norm;B_TF_profile_norm;R11_TF_operator_norm;TF_cross_terms",
            "D_TF_component": "M_H_ref_or_same_frame_M_ref_candidate",
            "B_TF_obs_norm": "MISSING_VALUE_OR_THEOREM_ZERO",
            "T_projector_TF_norm": "MISSING_VALUE_OR_THEOREM_ZERO",
            "B_TF_profile_norm": "MISSING_PROFILE_OR_THEOREM_ZERO",
            "R11_TF_operator_norm": "MISSING_OPERATOR_ROW_OR_THEOREM_ZERO",
            "TF_cross_terms": "MISSING_BOUND_OR_THEOREM_ZERO",
            "D_TF_value": "MISSING_CLAIM_READY_DENOMINATOR",
            "units": "dimensionless_after_denominator",
            "derivation_status": "unfilled_contract_row",
            "valid_for_claim": "false",
            "source_paths": source_list("691_source_pack", "693_operator_contract", "boundary_reference_status"),
            "generated_utc": now,
        }
    ]


def evaluator_readiness_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "eval_id": "ERE694_0_epsilon_TF",
            "target": "epsilon_TF",
            "required_state": "all numerator terms numeric/theorem-zero and D_TF valid",
            "observed_state": "first fill row contains missing numerator and denominator fields",
            "result": "not_evaluated",
            "claim_effect": "no epsilon_TF value",
            "valid_for_claim": "false",
            "source_paths": source_list("692_inputs", "693_operator_contract"),
            "generated_utc": now,
        },
        {
            "eval_id": "ERE694_1_gamma_runner",
            "target": "gamma/slip runner",
            "required_state": "epsilon_TF plus C_gamma_TF/C_slip_TF plus guardrail targets",
            "observed_state": "epsilon_TF and coefficients missing",
            "result": "blocked",
            "claim_effect": "no PPN score",
            "valid_for_claim": "false",
            "source_paths": source_list("692_doc", "693_doc"),
            "generated_utc": now,
        },
        {
            "eval_id": "ERE694_2_zero_route",
            "target": "epsilon_TF theorem-zero",
            "required_state": "all numerator components theorem-zero and denominator fixed",
            "observed_state": "boundary nohair/projector stress silence failed or conditional",
            "result": "fail_current_corpus",
            "claim_effect": "cannot set epsilon_TF=0",
            "valid_for_claim": "false",
            "source_paths": source_list("691_doc", "549_doc", "678_doc"),
            "generated_utc": now,
        },
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "CG694_0_definition",
            "gate": "epsilon_TF definition",
            "required_state": "physical numerator over same-frame denominator",
            "observed_state": "definition and first row written",
            "result": "pass_contract_only",
            "claim_effect": "contract exists but no value",
            "valid_for_claim": "false",
            "source_paths": source_list("693_operator_contract"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG694_1_numerator",
            "gate": "numerator readiness",
            "required_state": "every numerator term numeric/theorem-zero with source paths",
            "observed_state": "all numerator terms missing",
            "result": "fail_blocked",
            "claim_effect": "N_TF unavailable",
            "valid_for_claim": "false",
            "source_paths": source_list("691_source_pack"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG694_2_denominator",
            "gate": "denominator readiness",
            "required_state": "M_H_ref or same-frame M_ref valid",
            "observed_state": "boundary/reference status remains blocked",
            "result": "fail_blocked",
            "claim_effect": "D_TF unavailable",
            "valid_for_claim": "false",
            "source_paths": source_list("boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG694_3_no_shortcut",
            "gate": "projected shear shortcut guard",
            "required_state": "projected J_C silence excluded from physical numerator",
            "observed_state": "guard written in EDC694_3",
            "result": "pass_guard_only",
            "claim_effect": "prevents fake epsilon_TF zero",
            "valid_for_claim": "false",
            "source_paths": source_list("691_doc", "693_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG694_4_local_claims",
            "gate": "PPN/R10/local-GR promotion",
            "required_state": "epsilon_TF and coefficient runner scoreable",
            "observed_state": "epsilon_TF first row unfilled",
            "result": "fail_policy",
            "claim_effect": "no Cgamma score, PPN score, R10, or local-GR claim",
            "valid_for_claim": "false",
            "source_paths": source_list("692_doc", "693_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG694_5_next",
            "gate": "next target selection",
            "required_state": "choose first numerator/denominator fill target",
            "observed_state": NEXT_TARGET,
            "result": "selected",
            "claim_effect": "attempt B_TF_over_MH theorem-zero or source-bound acquisition",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "691_source_pack"),
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D694_0_contract",
            "target": "epsilon_TF contract",
            "result": "written_nonclaim",
            "reason": "physical numerator and same-frame denominator are now explicit, with projected-channel shortcuts excluded",
            "next_action": "use ETF694_0 as the first fill row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D694_1_value",
            "target": "epsilon_TF value",
            "result": "not_computed",
            "reason": "B_TF, projector TF, profile, R11, cross terms, and denominator are missing",
            "next_action": "do not score gamma/slip",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D694_2_next",
            "target": "B_TF_over_MH",
            "result": "selected",
            "reason": "direct physical boundary trace-free stress is the first and cleanest numerator component to derive or source",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S694_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "epsilon_TF numerator/denominator contract and first fill row are written, but all physical values remain missing",
            "hardest_blocker": "B_TF_over_MH plus same-frame M_H_ref",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
    ]


def all_valid_for_claim_false(rows_by_name: dict[str, list[dict[str, str]]]) -> bool:
    for rows in rows_by_name.values():
        for row in rows:
            if row.get("valid_for_claim") == "true":
                return False
    return True


def validation_rows(
    source_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    numerator_rows_: list[dict[str, str]],
    denominator_rows_: list[dict[str, str]],
    first_rows: list[dict[str, str]],
    evaluator_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows_by_name = {
        "contract": contract_rows,
        "numerator": numerator_rows_,
        "denominator": denominator_rows_,
        "first": first_rows,
        "evaluator": evaluator_rows,
        "gates": gate_rows,
        "decision": decision_rows_,
        "summary": summary_rows,
    }
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_ids = ["549_validation", "678_validation", "691_validation", "692_validation", "693_validation"]
    prior_failure_counts = {source_id: len(validation_failures_for(source_id)) for source_id in prior_ids}
    contract_complete = len(contract_rows) == 6 and all(row["valid_for_claim"] == "false" for row in contract_rows)
    numerator_complete = len(numerator_rows_) == 5 and all(row["valid_for_claim"] == "false" for row in numerator_rows_)
    denominator_complete = len(denominator_rows_) == 5 and all(row["valid_for_claim"] == "false" for row in denominator_rows_)
    first_complete = len(first_rows) == 1 and first_rows[0]["valid_for_claim"] == "false"
    first_missing = all("MISSING_" in value for key, value in first_rows[0].items() if key in {
        "B_TF_obs_norm",
        "T_projector_TF_norm",
        "B_TF_profile_norm",
        "R11_TF_operator_norm",
        "TF_cross_terms",
        "D_TF_value",
    })
    missing_markers_retained = all("MISSING_" in row["current_status"] for row in numerator_rows_ + denominator_rows_)
    evaluator_blocks = len(evaluator_rows) == 3 and all(row["valid_for_claim"] == "false" for row in evaluator_rows)
    no_shortcut_guard = any(row["contract_id"] == "EDC694_3_no_projection_shortcut" for row in contract_rows) and any(
        row["gate_id"] == "CG694_3_no_shortcut" and row["result"] == "pass_guard_only" for row in gate_rows
    )
    gates_block = all(row["valid_for_claim"] == "false" for row in gate_rows) and any(row["result"].startswith("fail") for row in gate_rows)
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision_rows_) and any(
        row["next_target"] == NEXT_TARGET for row in summary_rows
    )
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_694_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_694_EPSILON_TF_DEFINITION_CONTRACT.csv",
        RESIDUALS / "P8_Y5_R10_694_NUMERATOR_COMPONENTS.csv",
        RESIDUALS / "P8_Y5_R10_694_DENOMINATOR_COMPONENTS.csv",
        RESIDUALS / "P8_Y5_R10_694_FIRST_FILL_ROW.csv",
        RESIDUALS / "P8_Y5_R10_694_EVALUATOR_READINESS.csv",
        RESIDUALS / "P8_Y5_R10_694_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_694_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_694_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_694_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)
    checks = [
        ("V694_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V694_1_prior_validations_clean", all(count == 0 for count in prior_failure_counts.values()), ";".join(f"{key}={value}" for key, value in prior_failure_counts.items())),
        ("V694_2_definition_contract_complete", contract_complete, f"contract_rows={len(contract_rows)}"),
        ("V694_3_numerator_components_complete", numerator_complete, f"numerator_rows={len(numerator_rows_)}"),
        ("V694_4_denominator_components_complete", denominator_complete, f"denominator_rows={len(denominator_rows_)}"),
        ("V694_5_first_fill_row_complete", first_complete and first_missing, "first fill row written with all missing fields retained"),
        ("V694_6_missing_markers_retained", missing_markers_retained, "numerator/denominator rows retain MISSING status"),
        ("V694_7_evaluator_blocks", evaluator_blocks, "epsilon_TF and gamma runner not evaluated"),
        ("V694_8_no_projection_shortcut_guard", no_shortcut_guard, "projected shear cannot fill physical numerator"),
        ("V694_9_claim_gates_block", gates_block, "claim gates block epsilon value and local promotion"),
        ("V694_10_no_claim_rows_promoted", no_claim_rows, "all generated 694 rows remain valid_for_claim=false"),
        ("V694_11_next_target_selected", next_selected, NEXT_TARGET),
        ("V694_12_generated_outputs_scoped", scoped_outputs, "all 694 outputs target post-checkpoint-work"),
        ("V694_13_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V694_14_status_nonclaim", "no_epsilon_value" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now,
        }
        for check_id, passed, detail in checks
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._\n"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, divider, *body]) + "\n"


def write_doc(
    source_rows: list[dict[str, str]],
    contract_rows: list[dict[str, str]],
    numerator_rows_: list[dict[str, str]],
    denominator_rows_: list[dict[str, str]],
    first_rows: list[dict[str, str]],
    evaluator_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    doc = f"""# 694 - Y5 R10 Epsilon TF Numerator Denominator Contract Or First Fill Row

## Verdict

694 makes `epsilon_TF` executable as a contract:

```text
epsilon_TF := N_TF / D_TF
```

where `N_TF` must be the physical observed trace-free numerator, not projected/coherent-channel shear silence, and `D_TF` must be a same-frame denominator such as `M_H_ref`.

Current result: the contract and first fill row are written, but every physical numerator component and the denominator are still missing. No `epsilon_TF` value, no gamma/slip score, and no local-GR claim.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Epsilon TF Definition Contract

{markdown_table(contract_rows, ["contract_id", "clause", "formula", "current_status", "valid_for_claim"])}

## Numerator Components

{markdown_table(numerator_rows_, ["numerator_id", "component", "definition", "current_status", "why_needed", "valid_for_claim"])}

## Denominator Components

{markdown_table(denominator_rows_, ["denominator_id", "component", "definition", "current_status", "why_needed", "valid_for_claim"])}

## First Fill Row

{markdown_table(first_rows, ["fill_id", "residual", "formula", "N_TF_components", "D_TF_component", "derivation_status", "valid_for_claim"])}

## Evaluator Readiness

{markdown_table(evaluator_rows, ["eval_id", "target", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Claim Gate Evaluation

{markdown_table(gate_rows, ["gate_id", "gate", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Decision

{markdown_table(decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim"])}

## Validation

{markdown_table(validation_rows_, ["check_id", "result", "detail"])}
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    contract_rows = epsilon_definition_contract_rows()
    numerator_rows_ = numerator_rows()
    denominator_rows_ = denominator_rows()
    first_rows = first_fill_row()
    evaluator_rows = evaluator_readiness_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(
        source_rows,
        contract_rows,
        numerator_rows_,
        denominator_rows_,
        first_rows,
        evaluator_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
    )

    write_csv(RESIDUALS / "P8_Y5_R10_694_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_694_EPSILON_TF_DEFINITION_CONTRACT.csv", contract_rows, ["contract_id", "clause", "formula", "required_inputs", "current_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_694_NUMERATOR_COMPONENTS.csv", numerator_rows_, ["numerator_id", "component", "definition", "current_status", "why_needed", "allowed_zero_route", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_694_DENOMINATOR_COMPONENTS.csv", denominator_rows_, ["denominator_id", "component", "definition", "current_status", "why_needed", "allowed_use_now", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_694_FIRST_FILL_ROW.csv", first_rows, ["fill_id", "residual", "formula", "N_TF_components", "D_TF_component", "B_TF_obs_norm", "T_projector_TF_norm", "B_TF_profile_norm", "R11_TF_operator_norm", "TF_cross_terms", "D_TF_value", "units", "derivation_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_694_EVALUATOR_READINESS.csv", evaluator_rows, ["eval_id", "target", "required_state", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_694_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "required_state", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_694_DECISION.csv", decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_694_NONCLAIM_SUMMARY.csv", summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_694_VALIDATION.csv", validation_rows_, ["check_id", "result", "detail", "generated_utc"])

    write_doc(source_rows, contract_rows, numerator_rows_, denominator_rows_, first_rows, evaluator_rows, gate_rows, decision_rows_, summary_rows, validation_rows_)

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"contract_rows={len(contract_rows)}")
    print(f"numerator_rows={len(numerator_rows_)}")
    print(f"denominator_rows={len(denominator_rows_)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
