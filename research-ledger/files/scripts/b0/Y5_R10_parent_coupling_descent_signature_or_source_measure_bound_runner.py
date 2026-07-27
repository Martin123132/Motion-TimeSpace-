from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]
REPO_ROOT = POST_CHECKPOINT.parent
RESIDUALS = POST_CHECKPOINT / "source-intake" / "mts_residuals"
FORMALIZATION = REPO_ROOT / "formalization-workbench"

OUTPUT_DOC = POST_CHECKPOINT / "779-Y5-R10-parent-coupling-descent-signature-or-source-measure-bound-runner.md"
NEXT_TARGET = "780-Y5-R10-parent-action-coupling-signature-search-or-local-GR-branch-triage.md"
STATUS = "Y5_R10_779_parent_coupling_signature_runner_and_source_measure_bound_runner_built_both_blocked_by_missing_inputs_nonclaim"
CLAIM_CEILING = "signature_and_bound_runner_only_no_coupling_zero_no_numeric_source_measure_bound_no_physical_lock_rank_no_Newton_PPN_R10_R11_or_local_GR_claim"
FORMALIZATION_CUTOFF = datetime(2026, 5, 31, 14, 42, 0)

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_779_SOURCE_REGISTER.csv"
SIGNATURE_AUDIT_PATH = RESIDUALS / "P8_Y5_R10_779_PARENT_COUPLING_SIGNATURE_AUDIT.csv"
ZERO_DECISION_PATH = RESIDUALS / "P8_Y5_R10_779_ZERO_THEOREM_DECISION.csv"
BOUND_RUNNER_PATH = RESIDUALS / "P8_Y5_R10_779_SOURCE_MEASURE_BOUND_RUNNER.csv"
BOUND_COMPONENT_STATUS_PATH = RESIDUALS / "P8_Y5_R10_779_BOUND_COMPONENT_STATUS.csv"
DECISION_MATRIX_PATH = RESIDUALS / "P8_Y5_R10_779_DECISION_MATRIX.csv"
NONCLAIM_SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_779_NONCLAIM_SUMMARY.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_779_VALIDATION.csv"

COUPLING_DESCENT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_778_COUPLING_DESCENT_INPUT_CANDIDATE.csv"
CQMU_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_778_CQMU_COEFFICIENT_INPUT_CANDIDATE.csv"
SOURCE_FLUX_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_778_SOURCE_FLUX_VALUE_INPUT_CANDIDATE.csv"
READOUT_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_778_EM_CLOCK_ORBIT_READOUT_INPUT_CANDIDATE.csv"
PPN_COUPLING_CANDIDATE_PATH = RESIDUALS / "P8_Y5_R10_778_PPN_COUPLING_RESPONSE_INPUT_CANDIDATE.csv"

INPUT_ARTIFACTS = [
    COUPLING_DESCENT_CANDIDATE_PATH,
    CQMU_CANDIDATE_PATH,
    SOURCE_FLUX_CANDIDATE_PATH,
    READOUT_CANDIDATE_PATH,
    PPN_COUPLING_CANDIDATE_PATH,
]

CLAIM_ARTIFACTS = [
    RESIDUALS / "P8_Y5_R10_779_PARENT_COUPLING_DESCENT_ZERO_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_779_SOURCE_MEASURE_BOUND_CLAIM.csv",
    RESIDUALS / "P8_Y5_R10_779_PHYSICAL_LOCK_RANK_CERTIFICATE.csv",
    RESIDUALS / "P8_Y5_R10_779_LOCAL_GR_REENTRY_CANDIDATE.csv",
]

OUTPUT_PATHS = [
    OUTPUT_DOC,
    SOURCE_REGISTER_PATH,
    SIGNATURE_AUDIT_PATH,
    ZERO_DECISION_PATH,
    BOUND_RUNNER_PATH,
    BOUND_COMPONENT_STATUS_PATH,
    DECISION_MATRIX_PATH,
    NONCLAIM_SUMMARY_PATH,
    VALIDATION_PATH,
]

SOURCES: dict[str, dict[str, Any]] = {
    "778_doc": {
        "path": POST_CHECKPOINT / "778-Y5-R10-coupling-descent-input-pack-or-physical-lock-rank-proof.md",
        "needles": ["CDT778_7_theorem_result", "D778_3_next_target"],
        "role": "immediate 779 handoff",
    },
    "778_validation": {
        "path": RESIDUALS / "P8_Y5_BRR545_778_VALIDATION.csv",
        "needles": ["V778_4_theorem_not_promoted", "V778_9_schema_inputs_created"],
        "role": "prior validation guard",
    },
    "778_theorem_gate": {
        "path": RESIDUALS / "P8_Y5_R10_778_COUPLING_DESCENT_THEOREM_GATE.csv",
        "needles": ["CDT778_2_matter_action_descent", "CDT778_7_theorem_result"],
        "role": "conditional coupling descent theorem",
    },
    "778_input_pack": {
        "path": RESIDUALS / "P8_Y5_R10_778_COUPLING_DESCENT_INPUT_PACK.csv",
        "needles": ["CIP778_0_coupling_descent_candidate", "CIP778_4_PPN_coupling_candidate"],
        "role": "candidate input-pack manifest",
    },
    "778_coupling_candidate": {
        "path": COUPLING_DESCENT_CANDIDATE_PATH,
        "needles": ["MISSING_COUPLING_DESCENT_SIGNATURE", "valid_for_claim"],
        "role": "coupling descent candidate rows",
    },
    "778_Cqmu_candidate": {
        "path": CQMU_CANDIDATE_PATH,
        "needles": ["MISSING_NUMERIC_OR_ZERO_THEOREM", "MISSING_MH_REFERENCE"],
        "role": "C_qmu coefficient candidate rows",
    },
    "778_flux_candidate": {
        "path": SOURCE_FLUX_CANDIDATE_PATH,
        "needles": ["MISSING_FLUX_VALUE_OR_NO_FLUX_THEOREM", "MISSING_BOUNDARY_AND_SOURCE_ASSUMPTIONS"],
        "role": "source flux candidate rows",
    },
    "778_ppn_candidate": {
        "path": PPN_COUPLING_CANDIDATE_PATH,
        "needles": ["MISSING_NUMERIC_OR_ZERO_THEOREM", "MISSING_GAUGE_CERTIFICATE"],
        "role": "PPN coupling response candidate rows",
    },
}


def utc_stamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def text_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_string(value: bool) -> str:
    return "true" if value else "false"


def markdown_cell(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    if not rows:
        return "_No rows._"
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def under_post_checkpoint(path: Path) -> bool:
    try:
        path.resolve().relative_to(POST_CHECKPOINT.resolve())
        return True
    except ValueError:
        return False


def formalization_changed_after_cutoff() -> int:
    if not FORMALIZATION.exists():
        return -1
    changed_count = 0
    for scanned_path in FORMALIZATION.rglob("*"):
        if scanned_path.is_file() and datetime.fromtimestamp(scanned_path.stat().st_mtime) > FORMALIZATION_CUTOFF:
            changed_count += 1
    return changed_count


def validation_clean(number: int) -> bool:
    path = RESIDUALS / f"P8_Y5_BRR545_{number}_VALIDATION.csv"
    rows = read_csv_rows(path)
    return path.exists() and bool(rows) and all(row.get("result") == "pass" for row in rows)


def source_register_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(source_spec["path"]),
            "exists": bool_string(Path(source_spec["path"]).exists()),
            "needle_check": bool_string(text_contains(Path(source_spec["path"]), source_spec["needles"])),
            "role": source_spec["role"],
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
        for source_id, source_spec in SOURCES.items()
    ]


def has_missing_marker(row: dict[str, Any]) -> bool:
    return "MISSING" in ",".join(str(value) for value in row.values())


def valid_false_or_true(row: dict[str, Any]) -> bool:
    return str(row.get("valid_for_claim", "")).lower() == "true"


def parse_number(value: Any) -> float | None:
    try:
        number = float(str(value))
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number):
        return None
    return number


def no_missing_and_claimed(rows: list[dict[str, Any]]) -> bool:
    return bool(rows) and all(valid_false_or_true(row) and not has_missing_marker(row) for row in rows)


def signature_audit_rows(generated_utc: str) -> list[dict[str, Any]]:
    specs = [
        ("SIG779_0_coupling_descent", COUPLING_DESCENT_CANDIDATE_PATH, "all sectors descend through e_obs and q_parent with no hidden frame map"),
        ("SIG779_1_Cqmu_coefficients", CQMU_CANDIDATE_PATH, "all C_qmu coefficients are numeric or theorem-zero with source paths"),
        ("SIG779_2_source_flux", SOURCE_FLUX_CANDIDATE_PATH, "all source fluxes are numeric or no-flux theorem rows with M_H reference"),
        ("SIG779_3_readout_response", READOUT_CANDIDATE_PATH, "all EM/clock/orbit/source readouts are parent-owned or bounded"),
        ("SIG779_4_PPN_coupling_response", PPN_COUPLING_CANDIDATE_PATH, "all PPN coupling responses are numeric/theorem-zero with gauge and frame"),
    ]
    rows: list[dict[str, Any]] = []
    for audit_id, path, gate in specs:
        input_rows = read_csv_rows(path)
        missing_count = sum(1 for row in input_rows if has_missing_marker(row))
        valid_count = sum(1 for row in input_rows if valid_false_or_true(row))
        gate_pass = no_missing_and_claimed(input_rows)
        rows.append(
            {
                "audit_id": audit_id,
                "input_artifact": str(path),
                "gate": gate,
                "rows_seen": len(input_rows),
                "valid_rows": valid_count,
                "missing_rows": missing_count,
                "gate_result": "pass" if gate_pass else "fail_missing_or_nonclaim_inputs",
                "claim_effect": "can_support_claim" if gate_pass else "blocks_zero_and_bound_claim",
                "valid_for_claim": "false",
                "generated_utc": generated_utc,
            }
        )
    return rows


def zero_decision_rows(signature_audit: list[dict[str, Any]], generated_utc: str) -> list[dict[str, Any]]:
    signature_all_pass = all(row["gate_result"] == "pass" for row in signature_audit)
    return [
        {
            "decision_id": "ZTD779_0_signature_requirements",
            "requirement": "coupling descent, C_qmu zero/numeric rows, source flux silence, readout descent, and PPN coupling response all pass",
            "observed_state": "all_signature_gates_pass" if signature_all_pass else "one_or_more_signature_gates_fail",
            "result": "eligible_for_zero_certificate" if signature_all_pass else "zero_theorem_blocked",
            "claim_effect": "none" if not signature_all_pass else "would_allow_claim_review",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "ZTD779_1_current_verdict",
            "requirement": "do not set B_obs_source_measure=0 by assertion",
            "observed_state": "778 candidate rows contain MISSING markers and valid_for_claim=false",
            "result": "coupling_zero_not_claimed",
            "claim_effect": "local_GR_branch_stays_open_but_blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def numeric_rows_available(rows: list[dict[str, str]], numeric_fields: list[str]) -> bool:
    if not rows:
        return False
    for row in rows:
        if row.get("valid_for_claim") != "true" or has_missing_marker(row):
            return False
        for field in numeric_fields:
            if parse_number(row.get(field)) is None:
                return False
    return True


def bound_component_status_rows(generated_utc: str) -> list[dict[str, Any]]:
    coupling_rows = read_csv_rows(COUPLING_DESCENT_CANDIDATE_PATH)
    cqmu_rows = read_csv_rows(CQMU_CANDIDATE_PATH)
    flux_rows = read_csv_rows(SOURCE_FLUX_CANDIDATE_PATH)
    readout_rows = read_csv_rows(READOUT_CANDIDATE_PATH)
    ppn_rows = read_csv_rows(PPN_COUPLING_CANDIDATE_PATH)
    return [
        {
            "component_id": "BCS779_0_descent_switch",
            "component": "descent theorem switch",
            "input_rows": len(coupling_rows),
            "numeric_or_theorem_ready": bool_string(no_missing_and_claimed(coupling_rows)),
            "missing_count": sum(1 for row in coupling_rows if has_missing_marker(row)),
            "status": "ready" if no_missing_and_claimed(coupling_rows) else "blocked_missing_parent_signature",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "BCS779_1_Cqmu",
            "component": "C_qmu coefficients",
            "input_rows": len(cqmu_rows),
            "numeric_or_theorem_ready": bool_string(numeric_rows_available(cqmu_rows, ["C_qmu"])),
            "missing_count": sum(1 for row in cqmu_rows if has_missing_marker(row)),
            "status": "ready" if numeric_rows_available(cqmu_rows, ["C_qmu"]) else "blocked_missing_numeric_coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "BCS779_2_flux",
            "component": "source flux values",
            "input_rows": len(flux_rows),
            "numeric_or_theorem_ready": bool_string(numeric_rows_available(flux_rows, ["flux_value", "M_H_ref"])),
            "missing_count": sum(1 for row in flux_rows if has_missing_marker(row)),
            "status": "ready" if numeric_rows_available(flux_rows, ["flux_value", "M_H_ref"]) else "blocked_missing_flux_values",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "BCS779_3_readout",
            "component": "readout response coefficients",
            "input_rows": len(readout_rows),
            "numeric_or_theorem_ready": bool_string(numeric_rows_available(readout_rows, ["coefficient"])),
            "missing_count": sum(1 for row in readout_rows if has_missing_marker(row)),
            "status": "ready" if numeric_rows_available(readout_rows, ["coefficient"]) else "blocked_missing_readout_coefficients",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "component_id": "BCS779_4_PPN_response",
            "component": "PPN coupling responses",
            "input_rows": len(ppn_rows),
            "numeric_or_theorem_ready": bool_string(numeric_rows_available(ppn_rows, ["linear_response"])),
            "missing_count": sum(1 for row in ppn_rows if has_missing_marker(row)),
            "status": "ready" if numeric_rows_available(ppn_rows, ["linear_response"]) else "blocked_missing_PPN_response",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def bound_runner_rows(component_status: list[dict[str, Any]], generated_utc: str) -> list[dict[str, Any]]:
    all_ready = all(row["numeric_or_theorem_ready"] == "true" for row in component_status)
    return [
        {
            "runner_id": "SMR779_0_zero_route",
            "bound_expression": "If descent switch ready and all vertical matter/readout variations vanish, set B_SM/M_H = 0.",
            "required_inputs": "BCS779_0 ready plus parent boundary/source silence",
            "computed_status": "blocked_missing_inputs",
            "bound_value": "MISSING_PARENT_SIGNATURE",
            "claim_effect": "no_zero_claim",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "SMR779_1_no_cancellation_bound",
            "bound_expression": "|B_SM|/M_H <= sum_i |C_qmu_i| |F_i|/M_H + sum_A |r_A| |O_A| + sum_I |W_I| |DeltaPPN_I|",
            "required_inputs": "C_qmu rows, flux rows, readout coefficients, PPN responses, units, M_H references",
            "computed_status": "ready_to_compute" if all_ready else "blocked_missing_inputs",
            "bound_value": "MISSING_NUMERIC_INPUTS" if not all_ready else "COMPUTABLE_FROM_INPUT_ROWS",
            "claim_effect": "no_bound_claim" if not all_ready else "would_allow_bound_review",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "runner_id": "SMR779_2_local_branch_rule",
            "bound_expression": "Local-GR recovery cannot use the coupling block unless SMR779_0 proves zero or SMR779_1 computes a sourced finite bound.",
            "required_inputs": "zero certificate or numeric no-cancellation bound",
            "computed_status": "local_branch_blocked",
            "bound_value": "NOT_APPLICABLE",
            "claim_effect": "keeps_R10_PPN_Newton_R11_claims_blocked",
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def decision_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "D779_0_runner_built",
            "decision": "use a runner to decide zero-theorem versus no-cancellation numeric bound",
            "reason": "the coupling branch now has machine-checkable failure modes instead of prose-only blockers",
            "claim_status": "runner_only",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D779_1_zero_route_blocked",
            "decision": "do not claim B_obs_source_measure=0",
            "reason": "parent coupling signatures and no-hidden-map/readout clauses are missing",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D779_2_bound_route_blocked",
            "decision": "do not claim a finite source-measure bound",
            "reason": "C_qmu, flux, readout, and PPN response inputs are not numeric or sourced",
            "claim_status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
        {
            "decision_id": "D779_3_next_target",
            "decision": "search parent action for coupling signatures or triage the local-GR branch as empirical-residual first",
            "reason": "either we find the descent owner, or the local branch must carry a coupling residual into tests",
            "claim_status": "next_target_selected",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        },
    ]


def summary_rows(generated_utc: str) -> list[dict[str, Any]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "main_result": "779 runner proves the current input pack cannot claim coupling zero or a numeric source-measure bound yet",
            "hard_blocker": "all coupling/source-measure candidate routes remain MISSING/nonclaim",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "false",
            "generated_utc": generated_utc,
        }
    ]


def all_generated_rows(*row_groups: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for group in row_groups:
        rows.extend(group)
    return rows


def validation_rows(
    sources: list[dict[str, Any]],
    signature_audit: list[dict[str, Any]],
    zero_decision: list[dict[str, Any]],
    component_status: list[dict[str, Any]],
    bound_runner: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
) -> list[dict[str, str]]:
    source_paths_exist = all(row["exists"] == "true" for row in sources)
    source_needles_present = all(row["needle_check"] == "true" for row in sources)
    prior_665_778_clean = all(validation_clean(number) for number in range(665, 779))
    input_artifacts_exist = all(path.exists() for path in INPUT_ARTIFACTS)
    signature_audit_complete = len(signature_audit) == 5 and all(int(row["rows_seen"]) > 0 for row in signature_audit)
    signature_gates_fail_expected = all(row["gate_result"] == "fail_missing_or_nonclaim_inputs" for row in signature_audit)
    zero_blocked = any(row["decision_id"] == "ZTD779_1_current_verdict" and row["result"] == "coupling_zero_not_claimed" for row in zero_decision)
    component_status_complete = len(component_status) == 5
    component_status_blocked = all(str(row["status"]).startswith("blocked_") for row in component_status)
    bound_runner_complete = len(bound_runner) == 3
    bound_blocked = any(row["runner_id"] == "SMR779_1_no_cancellation_bound" and row["computed_status"] == "blocked_missing_inputs" for row in bound_runner)
    no_claim_rows_promoted = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for row in all_generated_rows(sources, signature_audit, zero_decision, component_status, bound_runner, decisions, summary)
    )
    claim_artifacts_absent = all(not path.exists() for path in CLAIM_ARTIFACTS)
    next_target_selected = summary[0]["next_target"] == NEXT_TARGET and any(row["decision_id"] == "D779_3_next_target" for row in decisions)
    output_scope_ok = all(under_post_checkpoint(path) for path in OUTPUT_PATHS)
    formalization_count = formalization_changed_after_cutoff()
    formalization_untouched = formalization_count == 0

    checks = [
        ("V779_0_source_paths_exist", source_paths_exist, f"source_rows={len(sources)}"),
        ("V779_1_source_needles_present", source_needles_present, "all local source needles present"),
        ("V779_2_prior_665_778_clean", prior_665_778_clean, "665-778 validation rows have no failures"),
        ("V779_3_input_artifacts_exist", input_artifacts_exist, "778 input artifacts present"),
        ("V779_4_signature_audit_complete", signature_audit_complete, "five signature gates audited"),
        ("V779_5_signature_gates_fail_expected", signature_gates_fail_expected, "all gates fail because rows are MISSING/nonclaim"),
        ("V779_6_zero_route_blocked", zero_blocked, "coupling zero not claimed"),
        ("V779_7_component_status_complete", component_status_complete, "five bound component groups checked"),
        ("V779_8_component_status_blocked", component_status_blocked, "all bound components blocked by missing inputs"),
        ("V779_9_bound_runner_complete", bound_runner_complete, "zero/bound/local-branch rules written"),
        ("V779_10_bound_route_blocked", bound_blocked, "numeric no-cancellation bound not claimable"),
        ("V779_11_no_claim_rows_promoted", no_claim_rows_promoted, "all generated rows valid_for_claim=false"),
        ("V779_12_claim_artifacts_absent", claim_artifacts_absent, "no zero/bound/rank/local-GR claim artifact fabricated"),
        ("V779_13_next_target_selected", next_target_selected, NEXT_TARGET),
        ("V779_14_outputs_scoped", output_scope_ok, "all outputs under post-checkpoint-work"),
        ("V779_15_formalization_workbench_untouched", formalization_untouched, f"formalization_changed_after_cutoff={formalization_count}"),
        ("V779_16_validation_rows_ready", True, "validation table constructed"),
    ]
    return [
        {"check_id": check_id, "result": "pass" if passed else "fail", "detail": detail}
        for check_id, passed, detail in checks
    ]


def build_doc(
    sources: list[dict[str, Any]],
    signature_audit: list[dict[str, Any]],
    zero_decision: list[dict[str, Any]],
    component_status: list[dict[str, Any]],
    bound_runner: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    validation: list[dict[str, str]],
) -> None:
    text = f"""# 779 - Y5 R10 Parent Coupling Descent Signature Or Source-Measure Bound Runner

Current result: **the runner is built and both routes are honestly blocked**. The zero route fails because the parent coupling descent signatures are missing. The numeric bound route fails because `C_qmu`, source fluxes, readout coefficients, and PPN coupling responses are missing or nonclaim. This is not a defeat; it is the trapdoor closing under handwaving. The local branch now has a strict rule: prove the parent coupling owner or carry a finite coupling residual into tests.

## Status

{markdown_table(summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim"])}

## Parent Coupling Signature Audit

{markdown_table(signature_audit, ["audit_id", "input_artifact", "gate", "rows_seen", "valid_rows", "missing_rows", "gate_result", "claim_effect", "valid_for_claim"])}

## Zero-Theorem Decision

{markdown_table(zero_decision, ["decision_id", "requirement", "observed_state", "result", "claim_effect", "valid_for_claim"])}

## Bound Component Status

{markdown_table(component_status, ["component_id", "component", "input_rows", "numeric_or_theorem_ready", "missing_count", "status", "valid_for_claim"])}

## Source-Measure Bound Runner

{markdown_table(bound_runner, ["runner_id", "bound_expression", "required_inputs", "computed_status", "bound_value", "claim_effect", "valid_for_claim"])}

## Decision Matrix

{markdown_table(decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim"])}

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Verdict

The next best move is not another broad derivation pass. It is a targeted parent-action search for exactly the signatures this runner asks for: quotient map, one observed coframe, quotient-invariant matter action, source current before measured-GM calibration, and no hidden readout map. If that search fails, the local branch should be triaged as empirical-residual first rather than local-GR-derived.

## Next Target

`{NEXT_TARGET}`
"""
    OUTPUT_DOC.write_text(text, encoding="utf-8")


def main() -> None:
    generated_utc = utc_stamp()
    sources = source_register_rows(generated_utc)
    signature_audit = signature_audit_rows(generated_utc)
    zero_decision = zero_decision_rows(signature_audit, generated_utc)
    component_status = bound_component_status_rows(generated_utc)
    bound_runner = bound_runner_rows(component_status, generated_utc)
    decisions = decision_rows(generated_utc)
    summary = summary_rows(generated_utc)
    validation = validation_rows(sources, signature_audit, zero_decision, component_status, bound_runner, decisions, summary)

    write_csv(SOURCE_REGISTER_PATH, sources, ["source_id", "path", "exists", "needle_check", "role", "valid_for_claim", "generated_utc"])
    write_csv(SIGNATURE_AUDIT_PATH, signature_audit, ["audit_id", "input_artifact", "gate", "rows_seen", "valid_rows", "missing_rows", "gate_result", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(ZERO_DECISION_PATH, zero_decision, ["decision_id", "requirement", "observed_state", "result", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(BOUND_COMPONENT_STATUS_PATH, component_status, ["component_id", "component", "input_rows", "numeric_or_theorem_ready", "missing_count", "status", "valid_for_claim", "generated_utc"])
    write_csv(BOUND_RUNNER_PATH, bound_runner, ["runner_id", "bound_expression", "required_inputs", "computed_status", "bound_value", "claim_effect", "valid_for_claim", "generated_utc"])
    write_csv(DECISION_MATRIX_PATH, decisions, ["decision_id", "decision", "reason", "claim_status", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(NONCLAIM_SUMMARY_PATH, summary, ["status", "claim_ceiling", "main_result", "hard_blocker", "next_target", "valid_for_claim", "generated_utc"])
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    build_doc(sources, signature_audit, zero_decision, component_status, bound_runner, decisions, summary, validation)

    failures = [row for row in validation if row["result"] != "pass"]
    if failures:
        failure_text = "; ".join(f"{row['check_id']}={row['detail']}" for row in failures)
        raise SystemExit(f"779 validation failed: {failure_text}")

    print(f"wrote {OUTPUT_DOC}")
    print(f"wrote {VALIDATION_PATH}")
    print(f"status={STATUS}")
    print(f"next={NEXT_TARGET}")


if __name__ == "__main__":
    main()
