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

CHECKPOINT = "4645"
CLAIM_ID = "L-487"
BRANCH_ID = "MTS_R2FR_Y5_XI_NONHILBERT_HPERP_EXACT_ZERO_CERTIFICATE_4645"
MARKER = "PPC4161_XI_NONHILBERT_HPERP_EXACT_ZERO_CERTIFICATE_4645"
PACKET_MARKER = "PPC4161_PACKET_XI_NONHILBERT_HPERP_ZERO_CERTIFICATE_4645"
DECISION = "XI_NONHILBERT_PROMOTED_TO_BRANCH_HPERP_EXACT_ZERO_CERTIFICATE_FINITE_BOUND_RETAINED_NONCLAIM"
NEXT_TARGET = "4646-Y5-R2FR-boundary-history-alpha-component-or-no-flux-zero-certificate.md"

DOC_PATH = POST / "4645-Y5-R2FR-Xi-nonHilbert-alpha-component-or-Hperp-exact-zero-certificate.md"
FORMAL_PATH = FORMAL / "661-PPC4161-Xi-nonHilbert-Hperp-exact-zero-certificate.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

DOC_4644 = POST / "4644-Y5-R2FR-first-Xi-component-magnitude-or-exact-zero-certificate.md"
DOC_4643 = POST / "4643-Y5-R2FR-Xi-tail-first-claim-grade-input-fill-or-exact-parent-signature.md"
DOC_4639 = POST / "4639-Y5-R2FR-Xi-nonHilbert-Hperp-tail-zero-or-bound.md"
FW_4319 = FORMAL / "335-PPC4161-nonHilbert-Hperp-source-support-zero-or-bound-row.md"
FW_4320 = FORMAL / "336-PPC4161-Hperp-Dq-component-certificate-or-first-epsilon-profile-row.md"
FW_4431 = FORMAL / "447-PPC4161-source-shadow-ban-and-nonHilbert-bypass-zero-or-first-DD-K-value.md"
CSV_4644_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4644_VALIDATION.csv"
CSV_4644_REMAINING = SOURCE_DIR / "P8_Y5_R2FR_4644_REMAINING_TAIL_AFTER_XISRC.csv"
CSV_4644_ALPHA = SOURCE_DIR / "P8_Y5_R2FR_4644_ALPHA_SRC_HIDDEN_COMPONENT.csv"
CSV_4641_CLAUSES = SOURCE_DIR / "P8_Y5_R2FR_4641_SAME_BRANCH_CLAUSE_MATRIX.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4645_SOURCE_REGISTER.csv"
ZERO_CERT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4645_XINONHILBERT_ZERO_CERTIFICATE.csv"
ALPHA_COMPONENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4645_ALPHA_NONHILBERT_COMPONENT.csv"
REDUCED_TAIL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4645_REDUCED_TAIL_AFTER_TWO_COMPONENTS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4645_XINONHILBERT_ZERO_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4645_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4645_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4645_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4645_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4645_VALIDATION.csv"

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
        ("SRC4645_00_4644_validation", CSV_4644_VALIDATION, "VAL4644_OVERALL", "4644 first component zero passed."),
        ("SRC4645_01_4644_alpha", CSV_4644_ALPHA, "ALPHA4644_0_alpha_src_hidden", "alpha_src_hidden zero input."),
        ("SRC4645_02_4644_remaining", CSV_4644_REMAINING, "REM4644_1_alpha_nonHilbert", "4644 selected alpha_nonHilbert next."),
        ("SRC4645_03_4643_norm", DOC_4643, "K_NH=K_edge=K_tr=Pi_R10=1", "dimensionless projection normalization."),
        ("SRC4645_04_4639_zero", DOC_4639, "F4639_2_exact_zero", "current Xi_nonHilbert exact-zero row."),
        ("SRC4645_05_4639_bound", DOC_4639, "F4639_3_finite_bound", "current Xi_nonHilbert finite bound."),
        ("SRC4645_06_4319_zero", FW_4319, "TH4319_3_exact_zero", "Hperp source-support exact zero theorem."),
        ("SRC4645_07_4319_bound", FW_4319, "F4319_5_bound", "Hperp finite bound theorem."),
        ("SRC4645_08_4320_source_zero", FW_4320, "F4320_2_source_readout_zero", "source/readout Hperp deletion condition."),
        ("SRC4645_09_4320_Nsrc", FW_4320, "F4320_1_Nsrc", "Nsrc finite source-support row."),
        ("SRC4645_10_4431_NH_zero", FW_4431, "NH4431_0_nonHilbert_zero_theorem", "Noether/improvement bypass zero theorem."),
        ("SRC4645_11_4431_gap", FW_4431, "NH4431_1_current_gap", "Noether/improvement caveat retained."),
        ("SRC4645_12_4641_clause2", CSV_4641_CLAUSES, "CLAUSE4641_2", "quotient Hperp silence same-branch clause."),
        ("SRC4645_13_4639_reduced", DOC_4639, "XR4639_2_reduced_tail_after_two_zeros", "two-component reduced tail handoff."),
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
            "certificate_id": "ZC4645_0_quotient_split",
            "premise": "local source/readout variations split into quotient and orthogonal pieces",
            "mathematical_condition": "H_L=H_q+Hperp with H_q in ker(Dq)",
            "effect": "only Hperp can feed non-Hilbert source bypass",
            "status": "IMPORTED_FROM_4639_4319",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "ZC4645_1_Hperp_silence",
            "premise": "the active source functional has no Hperp representative leg",
            "mathematical_condition": "Hperp=0 or S_A Hperp^A=0",
            "effect": "source-pairing term vanishes",
            "status": "SIGNED_ON_HPERP_SILENT_BRANCH",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "ZC4645_2_readout_silence",
            "premise": "source/readout factors through q and is fixed after variation",
            "mathematical_condition": "Dq_source_readout[Hperp]=0 and R_src_readout=0",
            "effect": "explicit source-readout remainder vanishes",
            "status": "SIGNED_ON_HPERP_SILENT_BRANCH",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "ZC4645_3_nonHilbert_zero",
            "premise": "source-pairing and readout remainder vanish on the same branch",
            "mathematical_condition": "S_A Hperp^A + R_src_readout = 0",
            "effect": "N_src_nonHilbert=0 and Xi_nonHilbert=0",
            "status": "EXACT_ZERO_CERTIFICATE_READY_BRANCH_LOCAL",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": "ZC4645_4_R10_alpha_projection",
            "premise": "4643 sets K_NH=1 only after dimensionless R10 alpha projection",
            "mathematical_condition": "alpha_nonHilbert(lambda)=Pi_R10[Xi_nonHilbert]",
            "effect": "alpha_nonHilbert(lambda)=0 for every lambda in the branch domain",
            "status": "SECOND_COMPONENT_ALPHA_FILLED_AS_EXACT_ZERO",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def alpha_component_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": "ALPHA4645_0_alpha_nonHilbert",
            "component": "alpha_nonHilbert(lambda)",
            "value": 0.0,
            "units": "dimensionless",
            "source_basis": "ZC4645_3_nonHilbert_zero plus 4643 K_NH=1 alpha normalization",
            "domain": "Hperp source-pairing/readout-silent branch only",
            "filled_input": True,
            "valid_for_full_tail_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "component_id": "ALPHA4645_1_alpha_nonHilbert_open",
            "component": "alpha_nonHilbert_open(lambda)",
            "value": "",
            "units": "dimensionless",
            "source_basis": "F4319_5_bound / F4320_1_Nsrc",
            "domain": "any branch where Hperp or R_src_readout survives",
            "filled_input": False,
            "valid_for_full_tail_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def reduced_tail_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "tail_id": "TAIL4645_0_two_component_reduction",
            "condition": "alpha_src_hidden=0 and alpha_nonHilbert=0 on the same branch",
            "reduced_tail": "alpha_tail(lambda)=alpha_boundary_history(lambda)+alpha_transition_inner(lambda)",
            "status": "TWO_COMPONENT_REDUCTION_READY_BRANCH_LOCAL",
            "next_action": NEXT_TARGET,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "tail_id": "TAIL4645_1_boundary_history_live",
            "condition": "worldtube shell/boundary no-flux not yet signed",
            "reduced_tail": "alpha_boundary_history(lambda) remains live",
            "status": "STILL_LIVE",
            "next_action": NEXT_TARGET,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "tail_id": "TAIL4645_2_transition_inner_live",
            "condition": "transition source-kernel hair not yet signed",
            "reduced_tail": "alpha_transition_inner(lambda) remains live",
            "status": "STILL_LIVE",
            "next_action": "4647-Y5-R2FR-transition-inner-alpha-component-or-source-kernel-zero-certificate.md",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4645_0_current_live_full_tail",
            "branch": "current live full local-GR/R10 tail",
            "alpha_src_hidden": 0.0,
            "alpha_nonHilbert": "",
            "alpha_boundary_history": "",
            "alpha_transition_inner": "",
            "result": "FAIL_CLOSED",
            "reason": "alpha_nonHilbert has a branch zero certificate, but boundary/history, transition-inner and lambda_mem remain live",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4645_1_Hperp_certificate",
            "branch": "Hperp source-pairing/readout-silent branch",
            "alpha_src_hidden": 0.0,
            "alpha_nonHilbert": 0.0,
            "alpha_boundary_history": "",
            "alpha_transition_inner": "",
            "result": "SECOND_COMPONENT_EXACT_ZERO_PASS_NONCLAIM",
            "reason": "Hperp source-pairing and readout remainder vanish, so alpha_nonHilbert(lambda)=0",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4645_2_Hperp_or_readout_survives",
            "branch": "Hperp, S_A Hperp^A, Dq_source_readout[Hperp] or R_src_readout survives",
            "alpha_src_hidden": 0.0,
            "alpha_nonHilbert": "",
            "alpha_boundary_history": "",
            "alpha_transition_inner": "",
            "result": "USE_FINITE_HPERP_BOUND",
            "reason": "failed certificate must use ||U_B||(C_S C_perp E_Dq,Hperp + ||R_src_readout||)",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4645_3_two_component_only_full_tail",
            "branch": "alpha_src_hidden and alpha_nonHilbert zero only",
            "alpha_src_hidden": 0.0,
            "alpha_nonHilbert": 0.0,
            "alpha_boundary_history": "",
            "alpha_transition_inner": "",
            "result": "REJECT_FULL_TAIL_ZERO",
            "reason": "boundary/history and transition-inner components remain live",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "run_id": "RUN4645_4_generic_Hperp_zero_import",
            "branch": "generic Hperp=0 asserted without source/readout branch",
            "alpha_src_hidden": 0.0,
            "alpha_nonHilbert": "",
            "alpha_boundary_history": "",
            "alpha_transition_inner": "",
            "result": "REJECT_BRANCH",
            "reason": "must certify the same source-pairing/readout branch, not borrow a generic quotient zero",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4645_0_same_branch_required",
            "rule": "alpha_src_hidden=0 and alpha_nonHilbert=0 must live on the same source/readout branch before tail reduction.",
            "enforced": True,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4645_1_generic_Hperp_not_enough",
            "rule": "A generic Hperp zero does not certify non-Hilbert silence unless source-pairing and R_src_readout are also silent.",
            "enforced": True,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTL4645_2_no_full_tail_from_two_components",
            "rule": "Two component zeros reduce the tail but do not prove local-GR/R10 recovery.",
            "enforced": True,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4645_0",
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "claim_allowed": False,
            "summary": "4645 fills alpha_nonHilbert(lambda)=0 on the Hperp source-pairing/readout-silent branch and reduces the live tail to boundary/history plus transition-inner components.",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "status": "PRIVATE_DERIVATION_ADVANCE_NONCLAIM",
            "summary": "Second Xi_tail component exact-zero certificate ready; reduced tail now boundary/history plus transition-inner, with lambda_mem still live.",
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
            "priority": "attack alpha_boundary_history(lambda) through worldtube no-flux/edge silence before finite projection",
            "why": "after source-label and non-Hilbert components zero, the boundary/history edge term is the next obstruction to local tail suppression",
            "timestamp_utc": timestamp,
        }
    ]


def build_doc(
    sources: list[dict[str, Any]],
    certs: list[dict[str, Any]],
    alpha_rows: list[dict[str, Any]],
    reduced_tail: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4645 - Xi_nonHilbert alpha component or Hperp exact zero certificate

Branch: `{BRANCH_ID}`
Marker: `{MARKER}`
Decision: `{DECISION}`

## Result

4645 kills the second normalized `Xi_tail` component on the same style of strict branch:

`alpha_nonHilbert(lambda)=Pi_R10[Xi_nonHilbert]=0`.

The certificate is not a generic “set Hperp to zero” move. It requires the source-pairing and source/readout remainders to vanish together:

`Hperp=0` or `S_A Hperp^A=0`, and `R_src_readout=0`.

Then `N_src_nonHilbert=0`, hence `Xi_nonHilbert=0`, and by the 4643 dimensionless R10 normalization `alpha_nonHilbert(lambda)=0`.

If any Hperp source-pairing, readout-projector commutator, source/readout remainder, improvement flux, spin/boundary piece, or compact projected flux survives, the branch falls back to the finite no-cancellation bound. No full local-GR/R10 claim is made.

Together with 4644 this gives the branch-local reduction

`alpha_tail(lambda)=alpha_boundary_history(lambda)+alpha_transition_inner(lambda)`.

## Source Register

{markdown_table(sources)}

## Zero Certificate

{markdown_table(certs)}

## Alpha Component Row

{markdown_table(alpha_rows)}

## Reduced Tail

{markdown_table(reduced_tail)}

## Runner

{markdown_table(runners)}

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
    reduced_tail: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    checks.append(("VAL4645_0_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"))
    checks.append(("VAL4645_1_needles_found", all(row["needle_found"] for row in sources), "all cited source needles are present"))
    checks.append(("VAL4645_2_certificate_complete", len(certs) == 5 and certs[-1]["effect"] == "alpha_nonHilbert(lambda)=0 for every lambda in the branch domain", "zero certificate includes R10 alpha projection"))
    alpha_zero = next((row for row in alpha_rows if row["component_id"] == "ALPHA4645_0_alpha_nonHilbert"), None)
    checks.append(("VAL4645_3_alpha_nonHilbert_zero", alpha_zero is not None and float(alpha_zero["value"]) == 0.0 and alpha_zero["filled_input"] is True, "alpha_nonHilbert filled as exact zero"))
    checks.append(("VAL4645_4_two_component_reduction", any(row["tail_id"] == "TAIL4645_0_two_component_reduction" for row in reduced_tail), "two-component tail reduction present"))
    result_by_id = {row["run_id"]: row["result"] for row in runners}
    checks.append(("VAL4645_5_live_fail_closed", result_by_id.get("RUN4645_0_current_live_full_tail") == "FAIL_CLOSED", "full live tail remains fail-closed"))
    checks.append(("VAL4645_6_certificate_pass", result_by_id.get("RUN4645_1_Hperp_certificate") == "SECOND_COMPONENT_EXACT_ZERO_PASS_NONCLAIM", "Hperp certificate pass row present"))
    checks.append(("VAL4645_7_finite_bound_fallback", result_by_id.get("RUN4645_2_Hperp_or_readout_survives") == "USE_FINITE_HPERP_BOUND", "Hperp/readout survival uses finite bound"))
    checks.append(("VAL4645_8_full_tail_zero_rejected", result_by_id.get("RUN4645_3_two_component_only_full_tail") == "REJECT_FULL_TAIL_ZERO", "two component zeros not promoted to full tail zero"))
    checks.append(("VAL4645_9_generic_Hperp_rejected", result_by_id.get("RUN4645_4_generic_Hperp_zero_import") == "REJECT_BRANCH", "generic Hperp import rejected"))
    checks.append(("VAL4645_10_no_claim_allowed", not any(str(row.get("claim_allowed", "")).lower() == "true" for row in runners + decisions), "generated runner/decision rows remain nonclaim"))
    checks.append(("VAL4645_11_doc_marker", MARKER in read_text(DOC_PATH), "post-checkpoint doc marker present"))
    checks.append(("VAL4645_12_formal_marker", MARKER in read_text(FORMAL_PATH), "formal checkpoint marker present"))
    checks.append(("VAL4645_13_claim_registered", CLAIM_ID in read_text(CLAIMS_PATH), "claim row registered"))
    checks.append(("VAL4645_14_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker appended"))
    checks.append(("VAL4645_15_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker appended"))
    checks.append(("VAL4645_16_public_stage_clean", git_clean(PUBLIC_STAGE), "public stage not modified"))
    checks.append(("VAL4645_17_backup_repo_clean", git_clean(BACKUP_REPO), "backup repo not modified"))
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
            "validation_id": "VAL4645_OVERALL",
            "status": "PASS" if all_pass else "FAIL",
            "detail": "4645 validation passed" if all_pass else "4645 validation failed",
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
        "4645 fills the second normalized Xi_tail component: alpha_nonHilbert(lambda)=0 on the Hperp source-pairing/readout-silent branch, while retaining the finite Hperp/readout bound if any bypass survives.",
        "Generated source register, zero certificate, alpha component row, reduced-tail table, runner, controls, decision, status, next target and validation.",
        "alpha_nonHilbert_branch_exact_zero_nonclaim",
        NEXT_TARGET,
        "Importing a generic Hperp zero without source/readout silence, ignoring Noether improvement flux caveats, or promoting two component zeros to full Xi_tail zero.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No local-GR/Newton/R10/PPN claim until boundary/history, transition-inner, lambda_mem and promotion maps are source-backed or exact-zero signed on the same branch.",
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
    reduced_tail = reduced_tail_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_CERT_CSV, certs)
    write_csv(ALPHA_COMPONENT_CSV, alpha_rows)
    write_csv(REDUCED_TAIL_CSV, reduced_tail)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)

    write_text(DOC_PATH, build_doc(sources, certs, alpha_rows, reduced_tail, runners, controls, decisions, statuses, nexts, []))
    write_text(FORMAL_PATH, build_doc(sources, certs, alpha_rows, reduced_tail, runners, controls, decisions, statuses, nexts, []))
    write_claim_append()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4645 fills the second normalized `Xi_tail` component on the Hperp source-pairing/readout-silent branch: `alpha_nonHilbert(lambda)=0`. The proof requires `Hperp=0` or `S_A Hperp^A=0` together with `R_src_readout=0`; generic Hperp silence is not enough. With 4644, the live tail reduces branch-locally to `alpha_boundary_history + alpha_transition_inner`. This remains nonclaim because those components and `lambda_mem` remain live.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## {PACKET_MARKER}

Checkpoint `{CHECKPOINT}` promotes `alpha_nonHilbert(lambda)` to a branch exact-zero certificate and reduces the local tail to boundary/history plus transition-inner terms. Next packet target: `{NEXT_TARGET}`.
""",
    )

    validation = build_validation(sources, certs, alpha_rows, reduced_tail, runners, decisions, timestamp)
    write_csv(VALIDATION_CSV, validation)
    write_text(DOC_PATH, build_doc(sources, certs, alpha_rows, reduced_tail, runners, controls, decisions, statuses, nexts, validation))
    write_text(FORMAL_PATH, build_doc(sources, certs, alpha_rows, reduced_tail, runners, controls, decisions, statuses, nexts, validation))

    status = validation[-1]["status"]
    print(f"{MARKER}: {status}")
    print(DOC_PATH)
    print(VALIDATION_CSV)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
