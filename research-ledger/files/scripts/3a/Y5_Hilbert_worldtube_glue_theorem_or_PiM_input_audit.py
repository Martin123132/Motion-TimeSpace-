from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_Hilbert_worldtube_glue_theorem_attempted_not_derived_PiM_input_audit_no_claim_inputs"
CLAIM_CEILING = "Hilbert_worldtube_glue_contract_and_input_audit_only_no_epsilon_charge_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "537-Y5-Hilbert-worldtube-parent-action-contract-or-PiM-input-fill.md"

DOC_PATH = Path("536-Y5-Hilbert-worldtube-glue-theorem-or-PiM-input-audit.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_SOURCE_REGISTER.csv")
THEOREM_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_THEOREM_ATTEMPT.csv")
PIM_INPUT_AUDIT_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_NUMERIC_INPUT_AUDIT.csv")
CERTIFICATE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE_UPDATE.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "535-Y5-PiM-commutator-bound-runner-or-Hilbert-worldtube-glue.md",
        "role": "immediate Pi_M runner and Hilbert-worldtube certificate target",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "EH-style worldtube/source-measure lesson and residual decomposition",
    },
    {
        "source_file": "504-parent-Hilbert-worldtube-glue-or-external-radial-input-plan.md",
        "role": "parent Noether mass-charge route and C-term leakage ledger",
    },
    {
        "source_file": "509-source-measure-Meff-flux-closure-after-kappa-gate.md",
        "role": "source-measure flux closure theorem target",
    },
    {
        "source_file": "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
        "role": "older Hilbert/topological equality attempt",
    },
    {
        "source_file": "500-topological-PiM-current-parent-clause-or-radial-bound-runner.md",
        "role": "topological Pi_M current parent-clause attempt",
    },
    {
        "source_file": "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
        "role": "Y5 Pi_M projector owner and radial-bound fork",
    },
    {
        "source_file": "533-Y5-epsilon-charge-first-row-runner-or-source-current-theorem.md",
        "role": "epsilon_charge first-row runner blocked by Pi_M/source-current identity",
    },
    {
        "source_file": "534-Y5-PiM-topological-equality-certificate-or-commutator-bound.md",
        "role": "Pi_M topological equality certificate and commutator bound template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv",
        "role": "535 explicit Hilbert-worldtube certificate rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv",
        "role": "worldtube source-measure clauses from parent route",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
        "role": "source-measure flux theorem rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "role": "source-measure residual map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_NUMERIC_INPUT_TEMPLATE.csv",
        "role": "current Pi_M commutator numeric input template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_EVALUATOR.csv",
        "role": "current Pi_M commutator evaluator",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
        "role": "Y5 Pi_M radial-bound input template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_NUMERIC_INPUTS_TEMPLATE.csv",
        "role": "broad radial runner numeric input template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_NUMERIC_INPUT_TEMPLATE.csv",
        "role": "epsilon_charge numeric input template",
    },
    {
        "source_file": "scripts/Y5_Hilbert_worldtube_glue_theorem_or_PiM_input_audit.py",
        "role": "this checkpoint generator",
    },
]


INPUT_AUDIT_FILES = [
    "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_NUMERIC_INPUT_TEMPLATE.csv",
    "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_EVALUATOR.csv",
    "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
    "source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_NUMERIC_INPUTS_TEMPLATE.csv",
    "source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_NUMERIC_INPUT_TEMPLATE.csv",
    "source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_EVALUATOR.csv",
]


THEOREM_ATTEMPT_ROWS = [
    {
        "step_id": "HWT536_0_parent_worldtube_fixed",
        "required_identity": "the compact source worldtube W_source is selected before orbital readout",
        "math_form": "W_source = supp(delta S_matter/delta e_obs) with linking spheres S enclosing the same W_source",
        "dependency": "WG510_0;WG510_1;HWG535_0",
        "current_status": "not_derived_for_current_MTS",
        "failure_if_missing": "mass charge can be chosen after the fit",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HWT536_1_observed_Hilbert_measure_owned",
        "required_identity": "the source measure is the Hilbert/Noether measure of the observed matter frame",
        "math_form": "J_H[tau] = delta S_matter/delta e_obs contracted with tau",
        "dependency": "SM509_0;SM509_1;HWG535_1",
        "current_status": "same_frame_source_measure_not_yet_locked",
        "failure_if_missing": "source mass and orbital mass may live in different frames",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HWT536_2_dressed_mass_charge_definition",
        "required_identity": "M_source is the dressed Hamiltonian/Noether source charge, not bare rest mass",
        "math_form": "M_source[W] := H_tau[S_outer] - H_tau[reference]",
        "dependency": "T510_1;WG510_7",
        "current_status": "definition_guardrail_adopted_but_not_MTS_derived",
        "failure_if_missing": "bare mass is falsely equated to measured gravitational mass",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HWT536_3_Hilbert_to_PiM_charge_map",
        "required_identity": "the Pi_M-projected Hilbert current is the same charge form used by the worldtube source",
        "math_form": "(4*pi*G_ref)^-1 int_S Pi_M J_H = H_tau[S] - H_tau[reference]",
        "dependency": "SM509_2;WG510_5;HWG535_2",
        "current_status": "not_derived",
        "failure_if_missing": "Pi_M may conserve a topological object that is not measured mass",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HWT536_4_topological_boundary_match",
        "required_identity": "the topological representative matches the boundary class of the same Hilbert worldtube",
        "math_form": "int_boundary(W_source) omega_M_top = 1 with no independent source label",
        "dependency": "HWG535_2;P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT",
        "current_status": "certificate_missing",
        "failure_if_missing": "closed topological current can be the wrong conserved object",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HWT536_5_exact_and_reference_terms_zero",
        "required_identity": "exact improvement and reference/boundary terms integrate to zero on linked surfaces",
        "math_form": "Pi_M J_H - J_M_top = dB_zero and int_boundary dB_zero = 0",
        "dependency": "WG510_6;HWG535_3",
        "current_status": "missing_certificate_or_bound",
        "failure_if_missing": "mass equality shifts by boundary bookkeeping",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HWT536_6_PiM_commutator_and_projector_stress_zero",
        "required_identity": "Pi_M is fixed/covariantly constant and carries no local metric/projector stress",
        "math_form": "[d,Pi_M]J_H = 0 and T_PiM_munu = 0 or below explicit local locks",
        "dependency": "HWG535_4;HWG535_5;MR510_3",
        "current_status": "missing_certificate_or_numeric_bound",
        "failure_if_missing": "projector hair remains a fifth-force/PPN source",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HWT536_7_extra_sector_charge_silence",
        "required_identity": "non-EH, memory, domain, motion, time, range, boundary, and frame channels carry no independent mass charge",
        "math_form": "Delta_nonEH = Delta_extra = Delta_symp = Delta_frame = 0 in compact local exterior",
        "dependency": "WG510_4;SMR509_2;SMR509_3;MR510_4;MR510_5",
        "current_status": "field_specific_silence_queue_open",
        "failure_if_missing": "M_eff can drift or receive hidden non-GR source charge",
        "valid_for_claim": "false",
    },
    {
        "step_id": "HWT536_8_weak_field_readout_after_charge_glue",
        "required_identity": "the same charge controls the 1/r metric coefficient and PPN residual vector",
        "math_form": "g_00=-1+2G_ref M_source/r+O(r^-2); Delta_PPN={gamma-1,beta-1,alpha_i,zeta_i,xi}",
        "dependency": "WG510_8;MR510_6;MR510_7",
        "current_status": "not_reached",
        "failure_if_missing": "Newton-looking leading order can pass while local GR still fails",
        "valid_for_claim": "false",
    },
]


CERTIFICATE_UPDATE_ROWS = [
    {
        "previous_certificate_id": "HWG535_0_worldtube_fixed_before_readout",
        "mapped_536_step": "HWT536_0_parent_worldtube_fixed",
        "status_update": "still_missing_parent_selection_theorem",
        "needed_artifact": "parent action/source-support clause fixing W_source before readout",
        "valid_for_claim": "false",
    },
    {
        "previous_certificate_id": "HWG535_1_source_measure_owned",
        "mapped_536_step": "HWT536_1_observed_Hilbert_measure_owned",
        "status_update": "still_missing_same_frame_Hilbert_measure_ownership",
        "needed_artifact": "matter-coupling/source-current theorem for e_obs and tau",
        "valid_for_claim": "false",
    },
    {
        "previous_certificate_id": "HWG535_2_topological_representative_matches_worldtube_boundary",
        "mapped_536_step": "HWT536_3_Hilbert_to_PiM_charge_map;HWT536_4_topological_boundary_match",
        "status_update": "not_derived_topology_may_still_be_wrong_object",
        "needed_artifact": "boundary-class equality between Pi_M J_H and the Hilbert worldtube charge",
        "valid_for_claim": "false",
    },
    {
        "previous_certificate_id": "HWG535_3_exact_term_zero",
        "mapped_536_step": "HWT536_5_exact_and_reference_terms_zero",
        "status_update": "missing_zero_flux_certificate_or_bound",
        "needed_artifact": "reference-compatible exact-term integral proof or numeric bound",
        "valid_for_claim": "false",
    },
    {
        "previous_certificate_id": "HWG535_4_commutator_zero",
        "mapped_536_step": "HWT536_6_PiM_commutator_and_projector_stress_zero",
        "status_update": "missing_commutator_zero_or_sourced_numeric_integral",
        "needed_artifact": "Pi_M parent algebra theorem or I_commutator input row",
        "valid_for_claim": "false",
    },
    {
        "previous_certificate_id": "HWG535_5_no_projector_stress",
        "mapped_536_step": "HWT536_6_PiM_commutator_and_projector_stress_zero",
        "status_update": "missing_projector_stress_silence_or_residual_vector",
        "needed_artifact": "T_PiM_munu zero theorem or PPN/local-bound stress map",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D536_0_theorem_not_derived",
        "status": "Hilbert_worldtube_glue_not_derived_for_current_MTS",
        "meaning": "the exact contract is now explicit, but no current source closes all required doors",
        "claim_status": "no_local_GR_promotion",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D536_1_no_numeric_claim_inputs",
        "status": "PiM_input_audit_found_no_claim_valid_numeric_rows",
        "meaning": "existing templates/evaluators are placeholders, references, or not valid_for_claim",
        "claim_status": "epsilon_charge_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D536_2_best_route",
        "status": "parent_action_contract_or_source_backed_input_fill",
        "meaning": "either prove the worldtube charge map from the parent action or fill the Pi_M residual runner with sourced rows",
        "claim_status": "active_private_derivation",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D536_3_no_bare_mass_shortcut",
        "status": "bare_rest_mass_not_enough",
        "meaning": "M_source remains a dressed Hamiltonian/Noether charge until binding/reference/source-map terms are owned",
        "claim_status": "guardrail_retained",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D536_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "HILBERT_WORLDTUBE_GLUE",
        "previous_status": "certificate_written_as_next_theorem_target",
        "new_status": "exact_contract_written_but_not_derived",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "PIM_NUMERIC_INPUTS",
        "previous_status": "runner_written_no_numeric_inputs",
        "new_status": "audit_completed_no_claim_valid_numeric_rows",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SRC523_0_EPSILON_CHARGE",
        "previous_status": "blocked_by_PiM_equality_and_commutator_inputs",
        "new_status": "still_blocked_no_worldtube_glue_or_PiM_input",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "blocked_no_PiM_bound_or_worldtube_glue",
        "new_status": "still_blocked_dressed_source_charge_not_owned",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_first_source_current_row_unfilled",
        "new_status": "still_blocked_source_charge_PPN_readout_not_derived",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_exists(source_file: str) -> bool:
    if is_placeholder(source_file):
        return False
    return (ROOT / source_file).exists()


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def parse_float(value: Any) -> float | None:
    try:
        if str(value).strip() == "":
            return None
        return float(str(value))
    except (TypeError, ValueError):
        return None


def is_placeholder(value: Any) -> bool:
    text = str(value).strip().lower()
    if not text:
        return True
    markers = [
        "missing",
        "fill_",
        "not_applicable",
        "reference_not_current",
        "unfilled_template",
        "not_filled",
        "not_executable",
        "not_run",
        "placeholder",
    ]
    return any(marker in text for marker in markers)


def row_has_placeholder(row: dict[str, str]) -> bool:
    ignored = {"valid_for_claim"}
    return any(is_placeholder(value) for key, value in row.items() if key not in ignored)


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append({**item, "exists": full_path.exists()})
    return rows


def row_identifier(row: dict[str, str], index: int) -> str:
    for key in ["row_id", "input_id", "theorem_id", "clause_id", "residual_id", "model_id"]:
        value = row.get(key)
        if value:
            return value
    return f"row_{index}"


def row_quantity(row: dict[str, str]) -> str:
    for key in ["quantity", "channel", "branch_id", "normalization", "numeric_status", "current_status"]:
        value = row.get(key)
        if value:
            return value
    return "unspecified"


def numeric_field_summary(row: dict[str, str]) -> tuple[int, str]:
    numeric_items: list[str] = []
    for key, value in row.items():
        parsed = parse_float(value)
        if parsed is not None:
            numeric_items.append(f"{key}={parsed:g}")
    return len(numeric_items), ";".join(numeric_items[:6])


def input_audit_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_path in INPUT_AUDIT_FILES:
        csv_path = Path(source_path)
        candidate_rows = read_csv(csv_path)
        if not candidate_rows:
            rows.append(
                {
                    "audit_id": f"AUD536_{len(rows)}",
                    "candidate_file": source_path,
                    "candidate_row": "NO_ROWS",
                    "quantity": "none",
                    "declared_valid_for_claim": "false",
                    "source_file": "",
                    "source_file_exists": False,
                    "placeholder_detected": True,
                    "numeric_field_count": 0,
                    "numeric_field_examples": "",
                    "audit_status": "not_claimable",
                    "reason": "file_missing_or_empty",
                }
            )
            continue
        for index, row in enumerate(candidate_rows):
            source_file = row.get("source_file", "")
            declared_valid = is_true(row.get("valid_for_claim", "false"))
            placeholders = row_has_placeholder(row)
            numeric_count, numeric_examples = numeric_field_summary(row)
            exists = source_exists(source_file)
            claim_candidate = declared_valid and exists and not placeholders and numeric_count > 0
            reasons: list[str] = []
            if not declared_valid:
                reasons.append("declared_valid_for_claim_false")
            if not exists:
                reasons.append("source_file_missing_or_placeholder")
            if placeholders:
                reasons.append("placeholder_or_reference_terms_present")
            if numeric_count == 0:
                reasons.append("no_numeric_fields")
            rows.append(
                {
                    "audit_id": f"AUD536_{len(rows)}",
                    "candidate_file": source_path,
                    "candidate_row": row_identifier(row, index),
                    "quantity": row_quantity(row),
                    "declared_valid_for_claim": str(declared_valid).lower(),
                    "source_file": source_file,
                    "source_file_exists": exists,
                    "placeholder_detected": placeholders,
                    "numeric_field_count": numeric_count,
                    "numeric_field_examples": numeric_examples,
                    "audit_status": "claim_candidate" if claim_candidate else "not_claimable",
                    "reason": "claim_ready_candidate" if claim_candidate else ";".join(reasons),
                }
            )
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    prior_cert = read_csv(Path("source-intake/mts_residuals/P8_Y5_HILBERT_WORLDTUBE_GLUE_CERTIFICATE.csv"))
    worldtube_clauses = read_csv(Path("source-intake/mts_residuals/P8_PARENT_WORLDTUBE_GLUE_THEOREM_CLAUSES.csv"))
    source_flux = read_csv(Path("source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv"))
    input_files_missing = [path for path in INPUT_AUDIT_FILES if not (ROOT / path).exists()]
    claim_input_rows = [row for row in audit if row["audit_status"] == "claim_candidate"]
    claim_theorem_rows = [row for row in THEOREM_ATTEMPT_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V536_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V536_1_prior_certificate_loaded",
            "result": "pass" if len(prior_cert) == 6 else "fail",
            "detail": f"HWG535_rows={len(prior_cert)}",
        },
        {
            "check_id": "V536_2_worldtube_source_evidence_loaded",
            "result": "pass" if len(worldtube_clauses) >= 5 and len(source_flux) >= 3 else "fail",
            "detail": f"worldtube_clause_rows={len(worldtube_clauses)};source_flux_rows={len(source_flux)}",
        },
        {
            "check_id": "V536_3_theorem_attempt_complete",
            "result": "pass" if len(THEOREM_ATTEMPT_ROWS) == 9 else "fail",
            "detail": f"theorem_rows={len(THEOREM_ATTEMPT_ROWS)};claim_theorem_rows={len(claim_theorem_rows)}",
        },
        {
            "check_id": "V536_4_input_audit_files_present",
            "result": "pass" if not input_files_missing else "fail",
            "detail": f"input_files_missing={len(input_files_missing)};audit_rows={len(audit)}",
        },
        {
            "check_id": "V536_5_no_claim_numeric_rows",
            "result": "pass" if not claim_input_rows else "fail",
            "detail": f"claim_input_rows={len(claim_input_rows)}",
        },
        {
            "check_id": "V536_6_no_overclaim",
            "result": "pass" if not claim_input_rows and not claim_theorem_rows else "fail",
            "detail": "Hilbert_worldtube_glue_derived=false; PiM_bound_computed=false; epsilon_charge_filled=false; measured_GM=false; Newton=false; local_GR=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    claim_input_rows = [row for row in audit if row["audit_status"] == "claim_candidate"]
    return f"""# 536 - Y5 Hilbert Worldtube Glue Theorem or PiM Input Audit

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The Hilbert-worldtube route is sharper, but it is not yet derived for current MTS.

The exact target is:

```text
W_source fixed before readout
-> observed Hilbert source current J_H[tau]
-> dressed source charge M_source[W]
-> Pi_M J_H equals that charge form up to zero boundary/commutator/projector terms
-> the same charge controls the weak-field metric and PPN vector.
```

The audit also found no claim-valid Pi_M numeric input rows. So the branch stays alive, but no `epsilon_charge`, measured-GM, Newton, PPN, or local-GR promotion is allowed.

## 2. Exact Theorem Contract

The theorem would have to prove:

```text
M_source[W] = H_tau[S] - H_tau[reference]
            = (4*pi*G_ref)^-1 integral_S Pi_M J_H

Pi_M J_H - J_M_top = dB_zero + R_eq
[d,Pi_M]J_H = 0
T_PiM_munu = 0
Delta_extra = Delta_frame = Delta_nonEH = Delta_symp = 0
```

with `R_eq = 0` or explicitly bounded, and with the weak-field readout performed after the charge equality, not before it.

## 3. Theorem Attempt Rows

{markdown_table(THEOREM_ATTEMPT_ROWS)}

## 4. PiM Numeric Input Audit

Claim-ready input rows found: `{len(claim_input_rows)}`.

{markdown_table(audit)}

## 5. Certificate Update

{markdown_table(CERTIFICATE_UPDATE_ROWS)}

## 6. Decision

{markdown_table(DECISION_ROWS)}

## 7. Source Register

{markdown_table(sources)}

## 8. Validation

{markdown_table(validations)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
MTS has an exact Hilbert-worldtube glue contract.
MTS has audited the current Pi_M numeric-input files.
Current MTS has no claim-valid Pi_M equality/commutator/source-charge input.
```

Forbidden:

```text
MTS has filled epsilon_charge.
MTS has derived measured GM.
MTS has derived source-normalized Newton, beta, PPN, or local GR.
MTS may equate bare rest mass with the dressed gravitational source charge.
```

## 11. Practical Read

This is the right kind of pain. We did not kill the local-GR route; we pinned it to one hard contract. Either the parent action owns the Hilbert worldtube charge and the Pi_M projection, or the local branch becomes a residual/bound branch.

## 12. Next Target

`{NEXT_TARGET}`

Next: write the parent-action contract that could actually satisfy `HWT536_0` through `HWT536_8`, while leaving a parallel fill path for sourced Pi_M residual rows if the proof does not close.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-Hilbert-worldtube-glue-theorem-or-PiM-input-audit"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    audit = input_audit_rows()
    validations = validation_rows(sources, audit)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (THEOREM_ATTEMPT_PATH, THEOREM_ATTEMPT_ROWS),
        (PIM_INPUT_AUDIT_PATH, audit),
        (CERTIFICATE_UPDATE_PATH, CERTIFICATE_UPDATE_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, audit, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_input_rows = [row for row in audit if row["audit_status"] == "claim_candidate"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "theorem_attempt": str(ROOT / THEOREM_ATTEMPT_PATH),
        "pim_input_audit": str(ROOT / PIM_INPUT_AUDIT_PATH),
        "certificate_update": str(ROOT / CERTIFICATE_UPDATE_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "theorem_rows": len(THEOREM_ATTEMPT_ROWS),
        "input_audit_rows": len(audit),
        "claim_input_rows": len(claim_input_rows),
        "Hilbert_worldtube_glue_derived": False,
        "PiM_bound_computed": False,
        "PiM_input_claim_rows_found": False,
        "epsilon_charge_filled": False,
        "measured_GM_derived": False,
        "source_normalized_Newton_derived": False,
        "beta_equals_one_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        "done\nprivate_no_github\nno_epsilon_charge_measured_GM_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
