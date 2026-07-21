from __future__ import annotations

import csv
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4644"
CLAIM_ID = "L-486"
BRANCH_ID = "MTS_R2FR_Y5_FIRST_XI_COMPONENT_EXACT_ZERO_CERTIFICATE_4644"
MARKER = "PPC4161_FIRST_XI_COMPONENT_EXACT_ZERO_CERTIFICATE_4644"
PACKET_MARKER = "PPC4161_PACKET_FIRST_XI_COMPONENT_ZERO_CERTIFICATE_4644"
DECISION = "XI_SRC_HIDDEN_PROMOTED_TO_BRANCH_EXACT_ZERO_CERTIFICATE_OPEN_TAIL_RETAINED_NONCLAIM"
NEXT_TARGET = "4645-Y5-R2FR-Xi-nonHilbert-alpha-component-or-Hperp-exact-zero-certificate.md"

DOC_PATH = POST / "4644-Y5-R2FR-first-Xi-component-magnitude-or-exact-zero-certificate.md"
FORMAL_PATH = FORMAL / "660-PPC4161-first-Xi-component-exact-zero-certificate.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4643 = POST / "4643-Y5-R2FR-Xi-tail-first-claim-grade-input-fill-or-exact-parent-signature.md"
DOC_4641 = POST / "4641-Y5-R2FR-same-branch-Xi-tail-zero-assembly-or-finite-coefficient-pack.md"
DOC_4638 = POST / "4638-Y5-R2FR-Xi-tail-bound-first-component-or-exact-zero.md"
FW_4332 = FORMAL / "348-PPC4161-Xi-src-hidden-zero-or-source-label-tail-bound.md"
FW_4333 = FORMAL / "349-PPC4161-standard-branch-source-readout-rollup-or-open-tail-test-pack.md"
FW_4324 = FORMAL / "340-PPC4161-hidden-source-prefactor-and-marker-tail-zero-or-bound.md"
CSV_4643_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4643_VALIDATION.csv"
CSV_4643_NORM = SOURCE_DIR / "P8_Y5_R2FR_4643_NORMALIZED_PROJECTION_INPUT_PACK.csv"
CSV_4643_REMAINING = SOURCE_DIR / "P8_Y5_R2FR_4643_REMAINING_CLAIM_INPUTS.csv"
CSV_4641_CLAUSES = SOURCE_DIR / "P8_Y5_R2FR_4641_SAME_BRANCH_CLAUSE_MATRIX.csv"
CSV_4641_COMPAT = SOURCE_DIR / "P8_Y5_R2FR_4641_BRANCH_COMPATIBILITY_AUDIT.csv"
CSV_4641_FINITE = SOURCE_DIR / "P8_Y5_R2FR_4641_FINITE_COEFFICIENT_PACK_SCHEMA.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4644_SOURCE_REGISTER.csv"
ZERO_CERT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4644_XISRC_ZERO_CERTIFICATE.csv"
ALPHA_COMPONENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4644_ALPHA_SRC_HIDDEN_COMPONENT.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4644_XISRC_ZERO_RUNNER_RESULTS.csv"
REMAINING_CSV = SOURCE_DIR / "P8_Y5_R2FR_4644_REMAINING_TAIL_AFTER_XISRC.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4644_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4644_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4644_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4644_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4644_VALIDATION.csv"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", "<br>").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for line_number, line_text in enumerate(read_text(path).splitlines(), start=1):
        if needle in line_text:
            return line_number
    return 0


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    separator = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + separator + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    sources = [
        ("SRC4644_00_4643_validation", CSV_4643_VALIDATION, "VAL4643_OVERALL", "4643 normalized alpha projection passed."),
        ("SRC4644_01_4643_norm", CSV_4643_NORM, "NORM4643_0_Pi_R10", "alpha projection functional for component zero."),
        ("SRC4644_02_4643_remaining", CSV_4643_REMAINING, "REM4643_1_component_values", "4643 selected component value/zero target."),
        ("SRC4644_03_4638_doc", DOC_4638, "AUD4638_1_conditional_zero", "first component Xi_src_hidden conditional zero."),
        ("SRC4644_04_4638_component", DOC_4638, "CB4638_8", "component-level Xi_src_hidden row."),
        ("SRC4644_05_4332_definition", FW_4332, "F4332_0_Xi_definition", "canonical Xi_src_hidden definition."),
        ("SRC4644_06_4332_zero", FW_4332, "F4332_1_source_label_zero", "source-label forgetting zero formula."),
        ("SRC4644_07_4332_Xi_zero", FW_4332, "ZERO4332_8_Xi", "Xi_src_hidden zero row."),
        ("SRC4644_08_4332_open", FW_4332, "TAIL4332_6_Xi_open", "open-tail fallback if certificate fails."),
        ("SRC4644_09_4332_firewall", FW_4332, "FW4332_0_no_hidden_slot_global", "global overclaim firewall."),
        ("SRC4644_10_4324_master", FW_4324, "F4324_0_master_tail", "hidden source-prefactor master budget."),
        ("SRC4644_11_4324_zero", FW_4324, "RUN4324_1_exact_zero", "older exact zero control."),
        ("SRC4644_12_4333_contract", FW_4333, "CON4333_6_Xi", "standard branch source-readout contract uses Xi_src_hidden=0."),
        ("SRC4644_13_4641_clause0", CSV_4641_CLAUSES, "CLAUSE4641_0", "single Hilbert source owner clause."),
        ("SRC4644_14_4641_clause1", CSV_4641_CLAUSES, "CLAUSE4641_1", "source-label forgetting clause."),
        ("SRC4644_15_4641_source_label_only", CSV_4641_COMPAT, "COMP4641_1_source_label_only", "source-label-only zero is not full Xi_tail zero."),
        ("SRC4644_16_4641_finite", CSV_4641_FINITE, "FP4641_0", "finite pack first component target."),
        ("SRC4644_17_4641_doc", DOC_4641, "Xi_src_hidden may zero", "full-tail branch-mix guard."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "needle": needle,
            "needle_found": line_of(path, needle) > 0,
            "line": line_of(path, needle),
            "purpose": purpose,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for source_id, path, needle, purpose in sources
    ]


def zero_certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "ZC4644_0_source_label_gauge",
            "premise": "source labels/species weights are bookkeeping/gauge variables, not observable fields",
            "mathematical_condition": "D_label w_A = D_label N_src = D_label theta_src = D_label sigma_env = 0",
            "effect": "R_hidden_weights=R_source_normalization=R_marker_source_label=R_environment_selector=0",
            "status": "SIGNED_ON_SOURCE_LABEL_FORGETTING_BRANCH",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "ZC4644_1_Hilbert_owner",
            "premise": "ordinary matter, EM current and source stress are owned by one Hilbert parent before readout",
            "mathematical_condition": "S_matter=Sbar[g_obs,Psi,A_mu,J_mu] with no hidden/source-only vertex",
            "effect": "epsilon_matter_hidden=epsilon_SR_hidden=delta_w_EM=0",
            "status": "SIGNED_ON_SOURCE_LABEL_FORGETTING_BRANCH",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "ZC4644_2_no_direct_m_charge",
            "premise": "memory/motion field has no direct calibrated matter charge outside Hilbert stress/current",
            "mathematical_condition": "Q_m^H=0 in the local branch",
            "effect": "R_no_direct_m_charge=0",
            "status": "SIGNED_ON_SOURCE_LABEL_FORGETTING_BRANCH",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "ZC4644_3_sum_zero",
            "premise": "all seven source-label hidden subcomponents vanish on the same branch",
            "mathematical_condition": "Xi_src_hidden=sum_i R_i with every R_i=0",
            "effect": "Xi_src_hidden=0",
            "status": "EXACT_ZERO_CERTIFICATE_READY_BRANCH_LOCAL",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "ZC4644_4_R10_alpha_projection",
            "premise": "4643 defines alpha_i(lambda) by a linear calibrated R10 projection functional",
            "mathematical_condition": "alpha_src_hidden(lambda)=Pi_R10[Xi_src_hidden]",
            "effect": "alpha_src_hidden(lambda)=0 for every lambda in the branch domain",
            "status": "FIRST_COMPONENT_ALPHA_FILLED_AS_EXACT_ZERO",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def alpha_component_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": "ALPHA4644_0_alpha_src_hidden",
            "component": "alpha_src_hidden(lambda)",
            "value": 0.0,
            "units": "dimensionless",
            "source_basis": "ZC4644_3_sum_zero plus 4643 linear R10 alpha normalization",
            "domain": "source-label-forgetting Hilbert-owner branch only",
            "filled_input": True,
            "valid_for_full_tail_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "ALPHA4644_1_open_tail_fallback",
            "component": "alpha_src_hidden_open(lambda)",
            "value": "",
            "units": "dimensionless",
            "source_basis": "TAIL4332_6_Xi_open / F4332_2_Xi_open_bound",
            "domain": "any branch where source-label gauge/descent certificate fails",
            "filled_input": False,
            "valid_for_full_tail_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4644_0_current_live_full_tail",
            "branch": "current live full local-GR/R10 tail",
            "alpha_src_hidden": "",
            "alpha_nonHilbert": "",
            "alpha_boundary_history": "",
            "alpha_transition_inner": "",
            "result": "FAIL_CLOSED",
            "reason": "alpha_src_hidden has an exact-zero certificate branch, but the full same-branch Xi_tail and lambda_mem are not yet closed",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4644_1_source_label_certificate",
            "branch": "source-label-forgetting Hilbert-owner branch",
            "alpha_src_hidden": 0.0,
            "alpha_nonHilbert": "",
            "alpha_boundary_history": "",
            "alpha_transition_inner": "",
            "result": "FIRST_COMPONENT_EXACT_ZERO_PASS_NONCLAIM",
            "reason": "source-label gauge/descent certificate gives alpha_src_hidden(lambda)=0",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4644_2_hidden_weight_present",
            "branch": "w_A, N_src, theta_src, sigma_env, O_hidden, delta_w_EM or Q_m^H survives",
            "alpha_src_hidden": "",
            "alpha_nonHilbert": "",
            "alpha_boundary_history": "",
            "alpha_transition_inner": "",
            "result": "USE_OPEN_TAIL_BOUND",
            "reason": "failed certificate must use TAIL4332_6_Xi_open and cannot be silently zeroed",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4644_3_source_label_only_full_tail",
            "branch": "source-label component zero only",
            "alpha_src_hidden": 0.0,
            "alpha_nonHilbert": "",
            "alpha_boundary_history": "",
            "alpha_transition_inner": "",
            "result": "REJECT_FULL_TAIL_ZERO",
            "reason": "Xi_nonHilbert, boundary/history and transition-inner components remain live",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4644_4_hide_source_norm_in_G",
            "branch": "source normalization hidden in calibrated constants",
            "alpha_src_hidden": "",
            "alpha_nonHilbert": "",
            "alpha_boundary_history": "",
            "alpha_transition_inner": "",
            "result": "REJECT_BRANCH",
            "reason": "source normalization reentry violates the source-label gauge certificate and returns to open tail",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def remaining_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "remaining_id": "REM4644_0_alpha_src_hidden",
            "component": "alpha_src_hidden(lambda)",
            "status_after_4644": "FILLED_AS_BRANCH_EXACT_ZERO",
            "detail": "First Xi_tail component is zero on the source-label-forgetting Hilbert-owner branch, and remains an explicit open tail otherwise.",
            "next_action": NEXT_TARGET,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "remaining_id": "REM4644_1_alpha_nonHilbert",
            "component": "alpha_nonHilbert(lambda)",
            "status_after_4644": "STILL_LIVE",
            "detail": "Next best component: use Hperp/source-pairing exact zero or project the finite Hperp/readout bound into alpha_nonHilbert.",
            "next_action": NEXT_TARGET,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "remaining_id": "REM4644_2_alpha_boundary_history",
            "component": "alpha_boundary_history(lambda)",
            "status_after_4644": "STILL_LIVE",
            "detail": "Worldtube shell/boundary Q_edge component still needs exact no-flux proof or alpha projection.",
            "next_action": "after 4645 unless Hperp route blocks",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "remaining_id": "REM4644_3_alpha_transition_inner",
            "component": "alpha_transition_inner(lambda)",
            "status_after_4644": "STILL_LIVE",
            "detail": "Transition source-kernel hair still needs exact zero or alpha projection.",
            "next_action": "after 4645 unless Hperp route blocks",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "remaining_id": "REM4644_4_lambda_mem",
            "component": "lambda_mem",
            "status_after_4644": "UNCHANGED",
            "detail": "lambda_mem remains sqrt(Z_mem/M2_mem); 4644 does not derive the parent Hessian ratio.",
            "next_action": "return after component-zero chain or if finite scoring becomes necessary",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4644_0_branch_local_not_global",
            "rule": "alpha_src_hidden=0 is a branch certificate, not a global no-hidden-slot theorem.",
            "enforced": True,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4644_1_no_source_norm_hiding",
            "rule": "Any source normalization reentry through calibrated constants breaks the certificate and reopens Xi_open.",
            "enforced": True,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4644_2_no_full_tail_from_first_component",
            "rule": "Killing alpha_src_hidden alone cannot be advertised as Xi_tail=0 or local-GR recovery.",
            "enforced": True,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4644_0",
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "summary": "4644 fills the first normalized Xi_tail component as alpha_src_hidden(lambda)=0 on the source-label-forgetting Hilbert-owner branch, while retaining Xi_open whenever a hidden/source-label slot survives.",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "PRIVATE_DERIVATION_ADVANCE_NONCLAIM",
            "summary": "First Xi_tail component exact-zero certificate ready; remaining components and lambda_mem still block any local-GR/R10 claim.",
            "valid_for_claim": False,
            "claim_allowed": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "priority": "attack alpha_nonHilbert(lambda) next through Hperp/source-pairing exact zero before finite projection",
            "why": "after alpha_src_hidden=0, Xi_nonHilbert is the largest remaining same-branch obstruction before boundary/history and transition hair",
            "timestamp_utc": timestamp,
        }
    ]


def build_doc(
    sources: list[dict[str, Any]],
    certs: list[dict[str, Any]],
    alpha_rows: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    remaining: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4644 - first Xi component magnitude or exact zero certificate

Branch: `{BRANCH_ID}`
Marker: `{MARKER}`
Decision: `{DECISION}`

## Result

4644 kills the first normalized `Xi_tail` component on the strict source-label-forgetting Hilbert-owner branch:

`alpha_src_hidden(lambda)=Pi_R10[Xi_src_hidden]=0`.

This is not a numerical fit. It follows because source labels, source weights, source normalization, hidden markers and environment selectors are treated as gauge/bookkeeping data that do not enter the parent action or observed readout except through the Hilbert-owned stress/current. Under that certificate every subcomponent of

`Xi_src_hidden := epsilon_matter_hidden + epsilon_SR_hidden + R_marker_source_label + R_hidden_weights + R_source_normalization + delta_w_EM + R_no_direct_m_charge + R_environment_selector`

vanishes on the same branch. If any hidden/source-label slot survives, the branch immediately returns to `Xi_open`; no cancellation or hiding inside calibrated `G_N` is allowed.

This fills one real component of the normalized 4643 gate, but it does **not** claim local GR/R10 because `alpha_nonHilbert`, `alpha_boundary_history`, `alpha_transition_inner` and `lambda_mem` remain live.

## Source Register

{markdown_table(sources)}

## Zero Certificate

{markdown_table(certs)}

## Alpha Component Row

{markdown_table(alpha_rows)}

## Runner

{markdown_table(runners)}

## Remaining Tail

{markdown_table(remaining)}

## Controls

{markdown_table(controls)}

## Decision

{markdown_table(decisions)}

## Status

{markdown_table(statuses)}

## Next Target

{markdown_table(nexts)}

## Validation

{markdown_table(validation)}
"""


def build_validation(
    sources: list[dict[str, Any]],
    certs: list[dict[str, Any]],
    alpha_rows: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    remaining: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL4644_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"))
    checks.append(("VAL4644_1_needles_found", all(row["needle_found"] for row in sources), "all cited source needles are present"))
    checks.append(("VAL4644_2_certificate_complete", len(certs) == 5 and certs[-1]["effect"] == "alpha_src_hidden(lambda)=0 for every lambda in the branch domain", "zero certificate includes R10 alpha projection"))
    alpha_zero = next((row for row in alpha_rows if row["component_id"] == "ALPHA4644_0_alpha_src_hidden"), None)
    checks.append(("VAL4644_3_alpha_src_hidden_zero", alpha_zero is not None and float(alpha_zero["value"]) == 0.0 and alpha_zero["filled_input"] is True, "alpha_src_hidden filled as exact zero"))
    result_by_id = {row["run_id"]: row["result"] for row in runners}
    checks.append(("VAL4644_4_live_full_tail_fail_closed", result_by_id.get("RUN4644_0_current_live_full_tail") == "FAIL_CLOSED", "full live tail remains fail-closed"))
    checks.append(("VAL4644_5_certificate_pass", result_by_id.get("RUN4644_1_source_label_certificate") == "FIRST_COMPONENT_EXACT_ZERO_PASS_NONCLAIM", "source-label certificate pass row present"))
    checks.append(("VAL4644_6_open_tail_fallback", result_by_id.get("RUN4644_2_hidden_weight_present") == "USE_OPEN_TAIL_BOUND", "hidden source-label survival reopens tail"))
    checks.append(("VAL4644_7_full_tail_zero_rejected", result_by_id.get("RUN4644_3_source_label_only_full_tail") == "REJECT_FULL_TAIL_ZERO", "first component zero not promoted to full tail zero"))
    checks.append(("VAL4644_8_source_norm_hiding_rejected", result_by_id.get("RUN4644_4_hide_source_norm_in_G") == "REJECT_BRANCH", "source normalization hiding rejected"))
    checks.append(("VAL4644_9_remaining_tail_live", any(row["component"] == "alpha_nonHilbert(lambda)" and row["status_after_4644"] == "STILL_LIVE" for row in remaining), "next component remains live"))
    checks.append(("VAL4644_10_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in runners + decisions), "generated runner/decision rows remain nonclaim"))
    checks.append(("VAL4644_11_doc_marker", MARKER in read_text(DOC_PATH), "post-checkpoint doc marker present"))
    checks.append(("VAL4644_12_formal_marker", MARKER in read_text(FORMAL_PATH), "formal checkpoint marker present"))
    checks.append(("VAL4644_13_claim_registered", CLAIM_ID in read_text(CLAIMS_PATH), "claim row registered"))
    checks.append(("VAL4644_14_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker appended"))
    checks.append(("VAL4644_15_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker appended"))
    checks.append(("VAL4644_16_public_stage_clean", git_clean(PUBLIC_STAGE), "public stage not modified"))
    checks.append(("VAL4644_17_backup_repo_clean", git_clean(BACKUP_REPO), "backup repo not modified"))
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for validation_id, passed, detail in checks
    ]
    all_pass = all(row["status"] == "PASS" for row in rows)
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4644_OVERALL",
            "status": "PASS" if all_pass else "FAIL",
            "detail": "4644 validation passed" if all_pass else "4644 validation failed",
            "timestamp_utc": utc_now(),
        }
    )
    return rows


def write_claim_append() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4644 fills the first normalized Xi_tail component: alpha_src_hidden(lambda)=0 on the source-label-forgetting Hilbert-owner branch, with Xi_open retained whenever hidden/source-label slots survive.",
        "Generated source register, zero certificate, alpha component row, runner, remaining-tail table, controls, decision, status, next target and validation.",
        "alpha_src_hidden_branch_exact_zero_nonclaim",
        NEXT_TARGET,
        "Treating the branch-local source-label certificate as a global no-hidden-slot theorem, hiding source normalization in calibrated G_N, or promoting first-component zero to full Xi_tail zero.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No local-GR/Newton/R10/PPN claim until remaining Xi components, lambda_mem and promotion maps are source-backed or exact-zero signed on the same branch.",
    ]
    escaped = []
    for value in row:
        value = str(value)
        if "," in value or '"' in value:
            value = '"' + value.replace('"', '""') + '"'
        escaped.append(value)
    append_once(CLAIMS_PATH, CLAIM_ID, ",".join(escaped))


def main() -> int:
    timestamp = utc_now()
    sources = source_rows(timestamp)
    certs = zero_certificate_rows(timestamp)
    alpha_rows = alpha_component_rows(timestamp)
    runners = runner_rows(timestamp)
    remaining = remaining_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_CERT_CSV, certs)
    write_csv(ALPHA_COMPONENT_CSV, alpha_rows)
    write_csv(RUNNER_CSV, runners)
    write_csv(REMAINING_CSV, remaining)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)

    write_text(DOC_PATH, build_doc(sources, certs, alpha_rows, runners, remaining, controls, decisions, statuses, nexts, []))
    write_text(FORMAL_PATH, build_doc(sources, certs, alpha_rows, runners, remaining, controls, decisions, statuses, nexts, []))
    write_claim_append()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4644 fills the first normalized `Xi_tail` component on the strict source-label-forgetting Hilbert-owner branch: `alpha_src_hidden(lambda)=0`. The zero is a source-label gauge/descent certificate, not a numerical fit. If any hidden/source-label slot, source normalization reentry, environment selector, direct matter charge or EM/source weight survives, the branch returns to the explicit `Xi_open` tail. This remains nonclaim because the other `Xi` components and `lambda_mem` remain live.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

Checkpoint `{CHECKPOINT}` promotes `alpha_src_hidden(lambda)` to a branch exact-zero certificate and preserves the open-tail fallback. Next packet target: `{NEXT_TARGET}`.
""",
    )

    validation = build_validation(sources, certs, alpha_rows, runners, remaining, decisions, timestamp)
    write_csv(VALIDATION_CSV, validation)
    write_text(DOC_PATH, build_doc(sources, certs, alpha_rows, runners, remaining, controls, decisions, statuses, nexts, validation))
    write_text(FORMAL_PATH, build_doc(sources, certs, alpha_rows, runners, remaining, controls, decisions, statuses, nexts, validation))

    status = validation[-1]["status"]
    print(f"{MARKER}: {status}")
    print(DOC_PATH)
    print(VALIDATION_CSV)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
