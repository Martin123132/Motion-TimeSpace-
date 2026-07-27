from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_metric_shear_bound_runner_scaffold_source_locked_PPN_guardrails_prediction_not_scoreable_nonclaim"
CLAIM_CEILING = "metric_shear_bound_runner_scaffold_only_no_sigma_bound_no_PPN_score_no_R10_no_clock_no_orbital_no_local_GR_claim"
NEXT_TARGET = "693-Y5-R10-TF-shear-to-gamma-slip-coefficient-derivation-or-retained-bound.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "692-Y5-R10-metric-shear-bound-runner-from-PPN-slip-source-lock.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "347_doc": ROOT / "347-local-GR-parent-reduction-theorem-attempt.md",
    "352_doc": ROOT / "352-boundary-nohair-and-PPN-residual-vector-gate.md",
    "354_doc": ROOT / "354-official-local-bound-source-lock-or-nohair-proof-deepening.md",
    "357_doc": ROOT / "357-Ward-owned-local-nohair-or-retained-PPN-residual-map.md",
    "655_doc": ROOT / "655-Y5-R10-EH-operator-selection-under-WEP-closure-or-retained-R11-vector.md",
    "691_doc": ROOT / "691-Y5-R10-shear-channel-bound-source-pack-or-boundary-nohair-theorem.md",
    "549_validation": RESIDUALS / "P8_Y5_BRR545_549_VALIDATION.csv",
    "655_validation": RESIDUALS / "P8_Y5_BRR545_655_VALIDATION.csv",
    "678_validation": RESIDUALS / "P8_Y5_BRR545_678_VALIDATION.csv",
    "689_validation": RESIDUALS / "P8_Y5_BRR545_689_VALIDATION.csv",
    "690_validation": RESIDUALS / "P8_Y5_BRR545_690_VALIDATION.csv",
    "691_validation": RESIDUALS / "P8_Y5_BRR545_691_VALIDATION.csv",
    "691_source_pack": RESIDUALS / "P8_Y5_R10_691_SHEAR_CHANNEL_BOUND_SOURCE_PACK.csv",
    "691_observable_map": RESIDUALS / "P8_Y5_R10_691_OBSERVABLE_MAP.csv",
    "691_nohair_audit": RESIDUALS / "P8_Y5_R10_691_BOUNDARY_NOHAIR_THEOREM_AUDIT.csv",
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
        "347_doc": "local GR parent reduction maps trace-free residual to gamma/slip",
        "352_doc": "symbolic PPN residual vector with B_TF source terms",
        "354_doc": "source-locked internal gamma/beta/WEP/clock target scales",
        "357_doc": "retained PPN residual map and source-lock/quarantine status",
        "655_doc": "later observable impact table with R3-R11 guardrails",
        "691_doc": "immediate metric-shear source-pack predecessor",
        "549_validation": "549 validation gate",
        "655_validation": "655 validation gate",
        "678_validation": "678 validation gate",
        "689_validation": "689 validation gate",
        "690_validation": "690 validation gate",
        "691_validation": "691 validation gate",
        "691_source_pack": "metric shear source pack",
        "691_observable_map": "observable map for shear residual",
        "691_nohair_audit": "boundary no-hair theorem audit",
        "boundary_reference_status": "same-frame denominator status",
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


def source_locked_target_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        {
            "target_id": "SLT692_0_gamma",
            "observable": "gamma_minus_1",
            "bound_value": "2.3e-5",
            "bound_units": "dimensionless_abs",
            "source_lock_status": "source_locked_internal_guardrail",
            "score_allowed_now": "false",
            "why_not_scoreable": "MTS C_gamma_TF and epsilon_TF inputs are missing",
            "source_paths": source_list("354_doc", "357_doc", "655_doc"),
        },
        {
            "target_id": "SLT692_1_beta",
            "observable": "beta_minus_1",
            "bound_value": "7.8e-5",
            "bound_units": "dimensionless_abs",
            "source_lock_status": "source_locked_internal_guardrail",
            "score_allowed_now": "false",
            "why_not_scoreable": "shear contribution is not isolated from radial/nonlinear boundary terms",
            "source_paths": source_list("354_doc", "357_doc", "655_doc"),
        },
        {
            "target_id": "SLT692_2_xi",
            "observable": "xi_preferred_location_anisotropy",
            "bound_value": "4e-9",
            "bound_units": "dimensionless_abs",
            "source_lock_status": "candidate_guardrail_from_655_not_354_source_locked",
            "score_allowed_now": "false",
            "why_not_scoreable": "354 quarantines anisotropy; l>=2 shear profile and C_xi_TF are missing",
            "source_paths": source_list("354_doc", "357_doc", "655_doc"),
        },
        {
            "target_id": "SLT692_3_lensing_slip",
            "observable": "Phi_minus_Psi_or_lensing_slip",
            "bound_value": "MISSING_DIRECT_SOURCE_LOCK",
            "bound_units": "dimensionless_or_model_specific",
            "source_lock_status": "not_source_locked_in_current_corpus",
            "score_allowed_now": "false",
            "why_not_scoreable": "no direct slip target and no shear-to-slip coefficient",
            "source_paths": source_list("352_doc", "357_doc"),
        },
        {
            "target_id": "SLT692_4_R10",
            "observable": "R10_alpha_lambda_from_TF_operator",
            "bound_value": "MISSING_RANGE_DEPENDENT_TARGET_FOR_TF_OPERATOR",
            "bound_units": "alpha_lambda_curve",
            "source_lock_status": "not_ready_for_shear_channel",
            "score_allowed_now": "false",
            "why_not_scoreable": "no TF range kernel, alpha(lambda) map, or source normalization",
            "source_paths": source_list("655_doc", "691_observable_map"),
        },
    ]
    return [
        {
            **row,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for row in rows
    ]


def runner_input_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        (
            "SRI692_0_epsilon_TF",
            "epsilon_TF",
            "abs(B_TF_over_MH)+abs(T_projector_TF_over_MH)+profile_terms",
            "MISSING_EPSILON_TF_NUMERIC_OR_THEOREM_ZERO",
            "SB691_1_B_TF_boundary;SB691_2_Pi_TF_projector;SB691_6_same_frame_denominator",
            "dimensionless",
        ),
        (
            "SRI692_1_C_gamma_TF",
            "C_gamma_TF",
            "linearized coefficient mapping epsilon_TF into gamma_minus_1",
            "MISSING_C_GAMMA_TF_COEFFICIENT",
            "SB691_3_TF_to_PPN_coefficients",
            "dimensionless",
        ),
        (
            "SRI692_2_C_slip_TF",
            "C_slip_TF",
            "linearized coefficient mapping epsilon_TF into lensing slip/Phi-Psi",
            "MISSING_C_SLIP_TF_COEFFICIENT",
            "SB691_3_TF_to_PPN_coefficients",
            "dimensionless_or_model_specific",
        ),
        (
            "SRI692_3_C_xi_TF",
            "C_xi_TF",
            "linearized coefficient mapping l>=2 epsilon_TF into xi/preferred-location anisotropy",
            "MISSING_C_XI_TF_COEFFICIENT",
            "SB691_3_TF_to_PPN_coefficients",
            "dimensionless",
        ),
        (
            "SRI692_4_profile",
            "TF_profile",
            "time/radial/frame profile for the metric shear or boundary TF source",
            "MISSING_TF_PROFILE",
            "SB691_4_boundary_flux_profile",
            "profile_function",
        ),
        (
            "SRI692_5_denominator",
            "M_H_ref_or_M_ref_candidate",
            "same-frame denominator used by epsilon_TF",
            "MISSING_CLAIM_READY_M_REF_CANDIDATE",
            "SB691_6_same_frame_denominator",
            "mass_or_energy",
        ),
        (
            "SRI692_6_logic_guard",
            "projected_shear_nonimplication_guard",
            "reject P_coh/J_C projected shear silence as metric sigma_mu_nu zero",
            "SCHEMA_ONLY_NONCLAIM_GUARD_ACTIVE",
            "SB691_7_no_shortcut_guard",
            "logic",
        ),
    ]
    return [
        {
            "input_id": input_id,
            "input_symbol": symbol,
            "definition": definition,
            "current_status": status,
            "source_pack_rows": pack_rows,
            "units": units,
            "valid_for_claim": "false",
            "source_paths": source_list("691_source_pack", "691_observable_map"),
            "generated_utc": now,
        }
        for input_id, symbol, definition, status, pack_rows, units in rows
    ]


def symbolic_evaluator_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        {
            "eval_id": "EV692_0_gamma",
            "observable": "gamma_minus_1",
            "formula": "abs(delta_gamma_TF)=abs(C_gamma_TF)*epsilon_TF",
            "target_id": "SLT692_0_gamma",
            "target_value": "2.3e-5",
            "required_inputs": "epsilon_TF;C_gamma_TF",
            "current_result": "not_evaluated_missing_epsilon_TF_and_C_gamma_TF",
            "claim_effect": "no PPN gamma score",
        },
        {
            "eval_id": "EV692_1_slip",
            "observable": "Phi_minus_Psi_or_lensing_slip",
            "formula": "abs(delta_slip_TF)=abs(C_slip_TF)*epsilon_TF",
            "target_id": "SLT692_3_lensing_slip",
            "target_value": "MISSING_DIRECT_SOURCE_LOCK",
            "required_inputs": "epsilon_TF;C_slip_TF;direct_slip_target_or_model_map",
            "current_result": "not_evaluated_missing_target_and_coefficient",
            "claim_effect": "no lensing/slip score",
        },
        {
            "eval_id": "EV692_2_xi",
            "observable": "xi_preferred_location_anisotropy",
            "formula": "abs(delta_xi_TF)=abs(C_xi_TF)*epsilon_TF_lge2",
            "target_id": "SLT692_2_xi",
            "target_value": "4e-9_candidate_not_source_locked_here",
            "required_inputs": "epsilon_TF_lge2;C_xi_TF;source_locked_xi_status",
            "current_result": "quarantined_missing_source_lock_and_lge2_profile",
            "claim_effect": "no xi score",
        },
        {
            "eval_id": "EV692_3_beta",
            "observable": "beta_minus_1",
            "formula": "abs(delta_beta_TF_profile)<=abs(C_boundary_nl)*epsilon_TF_profile + retained radial/nonlinear rows",
            "target_id": "SLT692_1_beta",
            "target_value": "7.8e-5",
            "required_inputs": "TF_profile;C_boundary_nl;radial/nonlinear separation",
            "current_result": "not_evaluated_missing_profile_and_coefficient",
            "claim_effect": "no beta score",
        },
        {
            "eval_id": "EV692_4_R10",
            "observable": "R10_alpha_lambda_from_TF_operator",
            "formula": "alpha_TF(lambda)=K_TF(lambda)*epsilon_TF/source_normalization",
            "target_id": "SLT692_4_R10",
            "target_value": "MISSING_RANGE_DEPENDENT_TARGET_FOR_TF_OPERATOR",
            "required_inputs": "lambda_TF;K_TF(lambda);epsilon_TF;source normalization",
            "current_result": "not_evaluated_missing_range_kernel_and_operator_row",
            "claim_effect": "no R10 score",
        },
    ]
    return [
        {
            **row,
            "score_allowed": "false",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "357_doc", "691_observable_map"),
            "generated_utc": now,
        }
        for row in rows
    ]


def unit_coefficient_smoke_rows() -> list[dict[str, str]]:
    now = generated_utc()
    rows = [
        {
            "smoke_id": "UCS692_0_gamma_unit_coeff",
            "assumption": "if C_gamma_TF=1 and all other residuals vanish",
            "target": "gamma_minus_1",
            "source_locked_bound": "2.3e-5",
            "implied_epsilon_limit": "epsilon_TF <= 2.3e-5",
            "use": "dry_run_sanity_only",
        },
        {
            "smoke_id": "UCS692_1_beta_unit_coeff",
            "assumption": "if shear-profile contribution enters beta with unit coefficient and no nonlinear/radial leakage",
            "target": "beta_minus_1",
            "source_locked_bound": "7.8e-5",
            "implied_epsilon_limit": "epsilon_TF_profile <= 7.8e-5",
            "use": "dry_run_sanity_only",
        },
        {
            "smoke_id": "UCS692_2_xi_candidate_unit_coeff",
            "assumption": "if C_xi_TF=1 and 655 candidate xi guardrail is accepted later",
            "target": "xi",
            "source_locked_bound": "4e-9_candidate",
            "implied_epsilon_limit": "epsilon_TF_lge2 <= 4e-9",
            "use": "quarantined_sanity_only",
        },
    ]
    return [
        {
            **row,
            "claim_status": "not_a_prediction_not_a_fit_not_a_pass",
            "valid_for_claim": "false",
            "source_paths": source_list("354_doc", "655_doc"),
            "generated_utc": now,
        }
        for row in rows
    ]


def claim_gate_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "gate_id": "CG692_0_targets",
            "gate": "source-locked target availability",
            "required_state": "target scale exists for scored observable",
            "observed_state": "gamma/beta are internal guardrails; xi/slip/R10 remain quarantined or missing",
            "result": "partial_pass_guardrails_only",
            "claim_effect": "targets alone do not create an MTS prediction",
            "valid_for_claim": "false",
            "source_paths": source_list("354_doc", "357_doc", "655_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG692_1_prediction_inputs",
            "gate": "MTS shear prediction readiness",
            "required_state": "epsilon_TF, coefficients, profiles, and denominator real or theorem-zero",
            "observed_state": "all physical prediction inputs missing or schema-only",
            "result": "fail_blocked",
            "claim_effect": "no PPN/slip/R10 score",
            "valid_for_claim": "false",
            "source_paths": source_list("691_source_pack"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG692_2_no_shortcut",
            "gate": "projected shear shortcut guard",
            "required_state": "P_coh/J_C channel silence not accepted as epsilon_TF=0",
            "observed_state": "guard active in SRI692_6",
            "result": "pass_guard_only",
            "claim_effect": "prevents fake local-GR pass",
            "valid_for_claim": "false",
            "source_paths": source_list("691_doc", "691_source_pack"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG692_3_unit_smoke",
            "gate": "unit-coefficient smoke interpretation",
            "required_state": "unit-coefficient rows are labelled dry-run only",
            "observed_state": "all smoke rows nonclaim and not predictions",
            "result": "pass_guard_only",
            "claim_effect": "sanity limits cannot be cited as evidence",
            "valid_for_claim": "false",
            "source_paths": source_list("354_doc", "655_doc"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG692_4_local_claims",
            "gate": "R10/PPN/clock/orbital/local-GR promotion",
            "required_state": "source-locked targets plus real MTS coefficients plus same-frame denominator",
            "observed_state": "coefficients, profiles, denominator, and R10 range kernel missing",
            "result": "fail_policy",
            "claim_effect": "no sigma bound, PPN score, R10, clock, orbital, or local-GR claim",
            "valid_for_claim": "false",
            "source_paths": source_list("691_observable_map", "boundary_reference_status"),
            "generated_utc": now,
        },
        {
            "gate_id": "CG692_5_next",
            "gate": "next target selection",
            "required_state": "choose highest-leverage missing prediction input",
            "observed_state": NEXT_TARGET,
            "result": "selected",
            "claim_effect": "derive C_gamma_TF/C_slip_TF or retain symbolic bound",
            "valid_for_claim": "false",
            "source_paths": source_list("352_doc", "357_doc"),
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D692_0_guardrails",
            "target": "PPN guardrails",
            "result": "partial_source_locked",
            "reason": "gamma and beta have internal source-locked scales; xi/slip/R10 are quarantined or missing in this shear channel",
            "next_action": "use gamma first because it is source-locked and directly tied to trace-free shear",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D692_1_runner",
            "target": "metric shear bound runner",
            "result": "scaffold_written_nonclaim",
            "reason": "the evaluator equations are written but every MTS prediction input remains missing or schema-only",
            "next_action": "do not score MTS yet",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D692_2_next",
            "target": "TF shear to gamma/slip coefficient",
            "result": "selected",
            "reason": "without C_gamma_TF and C_slip_TF, even source-locked gamma cannot test the physical shear residual",
            "next_action": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def nonclaim_summary_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "summary_id": "S692_0",
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "source-locked gamma/beta guardrails are loaded, but metric-shear prediction coefficients, epsilon_TF, profiles, and denominator are missing",
            "hardest_blocker": "C_gamma_TF/C_slip_TF derivation and same-frame epsilon_TF numerator/denominator",
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
    target_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
    evaluator_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    rows_by_name = {
        "targets": target_rows,
        "inputs": input_rows,
        "evaluator": evaluator_rows,
        "smoke": smoke_rows,
        "gates": gate_rows,
        "decision": decision_rows_,
        "summary": summary_rows,
    }
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_ids = ["549_validation", "655_validation", "678_validation", "689_validation", "690_validation", "691_validation"]
    prior_failure_counts = {source_id: len(validation_failures_for(source_id)) for source_id in prior_ids}
    targets_complete = len(target_rows) == 5 and all(row["valid_for_claim"] == "false" for row in target_rows)
    gamma_beta_loaded = any(row["observable"] == "gamma_minus_1" and row["bound_value"] == "2.3e-5" for row in target_rows) and any(
        row["observable"] == "beta_minus_1" and row["bound_value"] == "7.8e-5" for row in target_rows
    )
    quarantines_visible = any("not_source_locked" in row["source_lock_status"] for row in target_rows) and any(
        "candidate_guardrail" in row["source_lock_status"] for row in target_rows
    )
    input_complete = len(input_rows) == 7 and all(row["valid_for_claim"] == "false" for row in input_rows)
    missing_or_schema_retained = all(
        "MISSING_" in row["current_status"] or row["current_status"].startswith("SCHEMA_ONLY") for row in input_rows
    )
    evaluator_complete = len(evaluator_rows) == 5 and all(row["score_allowed"] == "false" for row in evaluator_rows)
    evaluator_blocks = all(row["current_result"].startswith(("not_evaluated", "quarantined")) for row in evaluator_rows)
    smoke_complete = len(smoke_rows) == 3 and all(row["claim_status"] == "not_a_prediction_not_a_fit_not_a_pass" for row in smoke_rows)
    gates_block = all(row["valid_for_claim"] == "false" for row in gate_rows) and any(row["result"].startswith("fail") for row in gate_rows)
    no_claim_rows = all_valid_for_claim_false(rows_by_name)
    next_selected = any(row["next_action"] == NEXT_TARGET for row in decision_rows_) and any(
        row["next_target"] == NEXT_TARGET for row in summary_rows
    )
    formalization_count = formalization_changed_count()
    output_paths = [
        DOC_PATH,
        RESIDUALS / "P8_Y5_R10_692_SOURCE_REGISTER.csv",
        RESIDUALS / "P8_Y5_R10_692_SOURCE_LOCKED_PPN_TARGETS.csv",
        RESIDUALS / "P8_Y5_R10_692_METRIC_SHEAR_RUNNER_INPUTS.csv",
        RESIDUALS / "P8_Y5_R10_692_SYMBOLIC_EVALUATOR.csv",
        RESIDUALS / "P8_Y5_R10_692_UNIT_COEFFICIENT_SMOKE.csv",
        RESIDUALS / "P8_Y5_R10_692_CLAIM_GATE_EVALUATION.csv",
        RESIDUALS / "P8_Y5_R10_692_DECISION.csv",
        RESIDUALS / "P8_Y5_R10_692_NONCLAIM_SUMMARY.csv",
        RESIDUALS / "P8_Y5_BRR545_692_VALIDATION.csv",
    ]
    scoped_outputs = all(str(path).startswith(str(ROOT)) for path in output_paths)
    checks = [
        ("V692_0_source_paths_exist", not missing_sources, "all cited source paths exist" if not missing_sources else "missing=" + ";".join(missing_sources)),
        ("V692_1_prior_validations_clean", all(count == 0 for count in prior_failure_counts.values()), ";".join(f"{key}={value}" for key, value in prior_failure_counts.items())),
        ("V692_2_targets_complete", targets_complete, f"target_rows={len(target_rows)}"),
        ("V692_3_gamma_beta_guardrails_loaded", gamma_beta_loaded, "gamma=2.3e-5;beta=7.8e-5"),
        ("V692_4_quarantines_visible", quarantines_visible, "xi/slip/R10 not silently scored"),
        ("V692_5_runner_inputs_complete", input_complete, f"input_rows={len(input_rows)}"),
        ("V692_6_missing_markers_retained", missing_or_schema_retained, "inputs retain MISSING or SCHEMA_ONLY status"),
        ("V692_7_evaluator_blocks_without_predictions", evaluator_complete and evaluator_blocks, "all evaluator rows non-scoreable"),
        ("V692_8_unit_smoke_nonclaim", smoke_complete, "unit-coefficient rows are dry-run sanity only"),
        ("V692_9_claim_gates_block", gates_block, "claim gates block scoring and local promotion"),
        ("V692_10_no_claim_rows_promoted", no_claim_rows, "all generated 692 rows remain valid_for_claim=false"),
        ("V692_11_next_target_selected", next_selected, NEXT_TARGET),
        ("V692_12_generated_outputs_scoped", scoped_outputs, "all 692 outputs target post-checkpoint-work"),
        ("V692_13_formalization_workbench_untouched", formalization_count == 0, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V692_14_status_nonclaim", "no_PPN_score" in CLAIM_CEILING and "no_local_GR_claim" in CLAIM_CEILING, CLAIM_CEILING),
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
    target_rows: list[dict[str, str]],
    input_rows: list[dict[str, str]],
    evaluator_rows: list[dict[str, str]],
    smoke_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision_rows_: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation_rows_: list[dict[str, str]],
) -> None:
    doc = f"""# 692 - Y5 R10 Metric Shear Bound Runner From PPN Slip Source Lock

## Verdict

692 turns the physical metric-shear problem into a test-shaped runner scaffold.

The useful progress is that `gamma - 1` and `beta - 1` already have internal source-locked guardrails. The hard stop is that MTS does not yet supply the prediction side:

```text
delta_gamma_TF = C_gamma_TF * epsilon_TF
delta_slip_TF  = C_slip_TF  * epsilon_TF
```

`epsilon_TF`, `C_gamma_TF`, `C_slip_TF`, the TF profile, and the same-frame denominator are still missing. So 692 loads the guardrails, writes the symbolic evaluator, performs only unit-coefficient smoke sanity rows, and keeps every scoring/promotion gate closed.

| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## Source Register

{markdown_table(source_rows, ["source_id", "path", "exists", "role"])}

## Source Locked PPN Targets

{markdown_table(target_rows, ["target_id", "observable", "bound_value", "source_lock_status", "score_allowed_now", "why_not_scoreable", "valid_for_claim"])}

## Metric Shear Runner Inputs

{markdown_table(input_rows, ["input_id", "input_symbol", "definition", "current_status", "units", "valid_for_claim"])}

## Symbolic Evaluator

{markdown_table(evaluator_rows, ["eval_id", "observable", "formula", "target_value", "current_result", "score_allowed", "claim_effect"])}

## Unit Coefficient Smoke

{markdown_table(smoke_rows, ["smoke_id", "assumption", "target", "source_locked_bound", "implied_epsilon_limit", "claim_status", "valid_for_claim"])}

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
    target_rows = source_locked_target_rows()
    input_rows = runner_input_rows()
    evaluator_rows = symbolic_evaluator_rows()
    smoke_rows = unit_coefficient_smoke_rows()
    gate_rows = claim_gate_rows()
    decision_rows_ = decision_rows()
    summary_rows = nonclaim_summary_rows()
    validation_rows_ = validation_rows(
        source_rows,
        target_rows,
        input_rows,
        evaluator_rows,
        smoke_rows,
        gate_rows,
        decision_rows_,
        summary_rows,
    )

    write_csv(RESIDUALS / "P8_Y5_R10_692_SOURCE_REGISTER.csv", source_rows, ["source_id", "path", "exists", "role", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_692_SOURCE_LOCKED_PPN_TARGETS.csv", target_rows, ["target_id", "observable", "bound_value", "bound_units", "source_lock_status", "score_allowed_now", "why_not_scoreable", "source_paths", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_692_METRIC_SHEAR_RUNNER_INPUTS.csv", input_rows, ["input_id", "input_symbol", "definition", "current_status", "source_pack_rows", "units", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_692_SYMBOLIC_EVALUATOR.csv", evaluator_rows, ["eval_id", "observable", "formula", "target_id", "target_value", "required_inputs", "current_result", "claim_effect", "score_allowed", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_692_UNIT_COEFFICIENT_SMOKE.csv", smoke_rows, ["smoke_id", "assumption", "target", "source_locked_bound", "implied_epsilon_limit", "use", "claim_status", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_692_CLAIM_GATE_EVALUATION.csv", gate_rows, ["gate_id", "gate", "required_state", "observed_state", "result", "claim_effect", "valid_for_claim", "source_paths", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_692_DECISION.csv", decision_rows_, ["decision_id", "target", "result", "reason", "next_action", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_R10_692_NONCLAIM_SUMMARY.csv", summary_rows, ["summary_id", "status", "claim_ceiling", "main_result", "hardest_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(RESIDUALS / "P8_Y5_BRR545_692_VALIDATION.csv", validation_rows_, ["check_id", "result", "detail", "generated_utc"])

    write_doc(source_rows, target_rows, input_rows, evaluator_rows, smoke_rows, gate_rows, decision_rows_, summary_rows, validation_rows_)

    failures = [row for row in validation_rows_ if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"target_rows={len(target_rows)}")
    print(f"input_rows={len(input_rows)}")
    print(f"evaluator_rows={len(evaluator_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")
        raise SystemExit(1)


if __name__ == "__main__":
    main()
