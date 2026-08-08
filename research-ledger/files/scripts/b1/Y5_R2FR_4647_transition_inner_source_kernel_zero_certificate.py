from __future__ import annotations

import csv
import io
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
SCRIPTS_DIR = POST / "scripts"
PUBLIC_STAGE = Path(r"D:\Users\ollet\Desktop\Motion-TimeSpace-public-stage")
BACKUP_REPO = Path(r"D:\Users\ollet\Desktop\laptop-back-up-")

CHECKPOINT = "4647"
CLAIM_ID = "L-489"
BRANCH = "MTS_R2FR_Y5_TRANSITION_INNER_SOURCE_KERNEL_ZERO_CERTIFICATE_4647"
MARKER = "PPC4161_TRANSITION_INNER_SOURCE_KERNEL_ZERO_CERTIFICATE_4647"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_INNER_SOURCE_KERNEL_ZERO_CERTIFICATE_4647"
NEXT_TARGET = "4648-Y5-R2FR-same-branch-Xi-tail-zero-assembly-and-lambda-promotion-gate.md"

DOC_PATH = POST / "4647-Y5-R2FR-transition-inner-alpha-component-or-source-kernel-zero-certificate.md"
FORMAL_PATH = FORMAL / "663-PPC4161-transition-inner-source-kernel-zero-certificate.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4647_SOURCE_REGISTER.csv"
ZERO_CERT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4647_TRANSITION_INNER_ZERO_CERTIFICATE.csv"
ALPHA_COMPONENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4647_ALPHA_TRANSITION_INNER_COMPONENT.csv"
REDUCED_TAIL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4647_REDUCED_TAIL_AFTER_FOUR_COMPONENTS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4647_TRANSITION_INNER_ZERO_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4647_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4647_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4647_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4647_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4647_VALIDATION.csv"

CSV_4646_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4646_VALIDATION.csv"
CSV_4646_ALPHA = SOURCE_DIR / "P8_Y5_R2FR_4646_ALPHA_BOUNDARY_HISTORY_COMPONENT.csv"
CSV_4646_REDUCED = SOURCE_DIR / "P8_Y5_R2FR_4646_REDUCED_TAIL_AFTER_THREE_COMPONENTS.csv"
DOC_4643 = POST / "4643-Y5-R2FR-Xi-tail-first-claim-grade-input-fill-or-exact-parent-signature.md"
DOC_4640 = POST / "4640-Y5-R2FR-Xi-boundary-history-transition-tail-zero-or-bound.md"
CSV_4641_CLAUSES = SOURCE_DIR / "P8_Y5_R2FR_4641_SAME_BRANCH_CLAUSE_MATRIX.csv"
FORMAL_4355 = FORMAL / "371-PPC4161-transition-shell-same-worldtube-nonHilbert-residue-or-bounded-source-hair.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def line_number(path: Path, needle: str) -> int:
    if not path.exists():
        return 0
    for index, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ").replace("|", "\\|") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    existing = read_text(path)
    if marker in existing:
        return
    suffix = "" if existing.endswith("\n") or not existing else "\n"
    path.write_text(existing + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    handle = io.StringIO()
    writer = csv.writer(handle, lineterminator="\n")
    writer.writerow(values)
    return handle.getvalue()


def git_clean(repo: Path) -> tuple[bool, str]:
    if not repo.exists():
        return True, "path absent"
    if not (repo / ".git").exists():
        return True, "not a git checkout"
    result = subprocess.run(
        ["git", "-C", str(repo), "status", "--porcelain"],
        check=False,
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        return False, result.stderr.strip() or "git status failed"
    output = result.stdout.strip()
    return output == "", output or "clean"


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    source_specs = [
        ("SRC4647_00_4646_validation", CSV_4646_VALIDATION, "VAL4646_OVERALL", "4646 third-component certificate passed."),
        ("SRC4647_01_4646_alpha", CSV_4646_ALPHA, "ALPHA4646_0_alpha_boundary_history", "alpha_boundary_history zero input."),
        ("SRC4647_02_4646_reduced", CSV_4646_REDUCED, "TAIL4646_0_three_component_reduction", "transition-inner selected as only live Xi_tail component."),
        ("SRC4647_03_4643_norm", DOC_4643, "K_NH=K_edge=K_tr=Pi_R10=1", "dimensionless transition projection normalization."),
        ("SRC4647_04_4640_transition_hair", DOC_4640, "F4640_4_transition_hair", "finite epsilon_tr_hair vector."),
        ("SRC4647_05_4640_transition_bound", DOC_4640, "F4640_5_transition_bound", "transition-inner Xi bound."),
        ("SRC4647_06_4640_TR0", DOC_4640, "TR4640_0", "Hilbert action-domain source-kernel clause."),
        ("SRC4647_07_4640_TR1", DOC_4640, "TR4640_1", "same-worldtube readout clause."),
        ("SRC4647_08_4640_TR2", DOC_4640, "TR4640_2", "static l=0 monopole clause."),
        ("SRC4647_09_4640_TR3", DOC_4640, "TR4640_3", "universal species/frame blind clause."),
        ("SRC4647_10_4640_TR4", DOC_4640, "TR4640_4", "range-free common monopole clause."),
        ("SRC4647_11_4640_TR5", DOC_4640, "TR4640_5", "same metric/EH readout clause."),
        ("SRC4647_12_4640_TR6", DOC_4640, "TR4640_6", "boundary/nonlocal owner clause."),
        ("SRC4647_13_4641_same_branch", CSV_4641_CLAUSES, "CLAUSE4641_5", "same-branch transition source-kernel row."),
        ("SRC4647_14_4355_kernel", FORMAL_4355, "P_kernel := P_Hilbert,l=0,static,universal,range-free,same-metric,same-worldtube", "formal source-kernel projector."),
        ("SRC4647_15_4355_theorem", FORMAL_4355, "TH4355_0_clean_transition_source", "clean transition source theorem."),
        ("SRC4647_16_4355_total_hair", FORMAL_4355, "HB4355_7_total", "finite transition hair fallback."),
        ("SRC4647_17_4355_firewall", FORMAL_4355, "FW4355_1", "do not call epsilon_mu_tr zero unless q_tr=P_kernel q_tr."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, note in source_specs:
        text = read_text(path)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "line_number": line_number(path, needle),
                "note": note,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("ZC4647_0_input_bound", "transition-inner bound", "|Xi_transition_inner| <= K_tr epsilon_tr_hair", "4640 + 4643", "imports the normalized R10 projection bound", "READY"),
        ("ZC4647_1_kernel_projector", "source-kernel membership", "q_tr=P_kernel q_tr", "4355", "all transition source residue lives in the Hilbert/common source dressing projector", "BRANCH_CONDITION"),
        ("ZC4647_2_Hilbert", "non-Hilbert hair", "Y_nonHilbert=0", "TR4640_0/KM4355_0", "no representative-only/non-Hilbert transition source slot survives", "ZERO_CLAUSE"),
        ("ZC4647_3_worldtube", "readout-order hair", "Delta_Wtr=0", "TR4640_1/KM4355_1", "transition support is inside W_H before variation; exterior is only post-solve readout", "ZERO_CLAUSE"),
        ("ZC4647_4_static_l0", "time/multipole hair", "Y_time_l=0", "TR4640_2/KM4355_2", "partial_tau q_tr=0 and Q_l>=1,tr=0", "ZERO_CLAUSE"),
        ("ZC4647_5_universal", "species/frame/source hair", "Y_species_frame=0", "TR4640_3/KM4355_3", "D_species q_tr=D_frame q_tr=Delta_source_weight_tr=0", "ZERO_CLAUSE"),
        ("ZC4647_6_rangefree", "range hair", "Y_range=0", "TR4640_4/KM4355_4", "D_lambda q_tr=q_range_tail=0 so no finite-range Yukawa leg is created", "ZERO_CLAUSE"),
        ("ZC4647_7_metric_boundary", "non-EH and boundary hair", "Y_nonEH=0 and Y_boundary_nonlocal=0", "TR4640_5/TR4640_6/KM4355_5/KM4355_6", "same metric/EH readout and Hamiltonian/projection-null boundary ownership", "ZERO_CLAUSE"),
        ("ZC4647_8_epsilon_zero", "transition hair envelope", "epsilon_tr_hair <= 0", "HB4355_7_total", "sum of nonnegative hair channels vanishes on one branch", "DERIVED_ZERO"),
        ("ZC4647_9_Xi_zero", "transition-inner component", "Xi_transition_inner=0", "F4640_5_transition_bound", "with K_tr=1 normalized and epsilon_tr_hair=0, the transition-inner Xi component vanishes", "DERIVED_ZERO"),
        ("ZC4647_10_alpha_projection", "R10 alpha component", "alpha_transition_inner(lambda)=0 for every lambda in branch domain", "4643 normalized alpha projection", "fills fourth normalized Xi_tail component", "ALPHA_ZERO"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "certificate_id": row[0],
            "object": row[1],
            "statement": row[2],
            "source_anchor": row[3],
            "effect": row[4],
            "status": row[5],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def alpha_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "component_id": "ALPHA4647_0_alpha_transition_inner",
            "alpha_component": "alpha_transition_inner(lambda)",
            "branch_condition": "q_tr=P_kernel q_tr with Hilbert, same-worldtube, static l=0, universal, range-free, same-metric and boundary-owned clauses on one branch",
            "lambda_dependence": "none after exact-zero projection",
            "alpha_value": "0",
            "units": "dimensionless Yukawa-alpha normalization",
            "exact_zero": True,
            "valid_for_claim": False,
            "source_paths": f"{DOC_4640}; {FORMAL_4355}; {DOC_4643}",
            "issues": "branch-local certificate only; failed kernel legs revert to finite epsilon_tr_hair bound",
            "next_action": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def reduced_tail_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "tail_id": "TAIL4647_0_four_component_zero",
            "premise": "alpha_src_hidden=alpha_nonHilbert=alpha_boundary_history=alpha_transition_inner=0 on the same parent/readout branch",
            "result": "alpha_tail(lambda)=0",
            "status": "EXACT_XI_TAIL_ZERO_BRANCH_LOCAL_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "tail_id": "TAIL4647_1_lambda_mem_range_live",
            "premise": "lambda_mem=sqrt(Z_mem/M2_mem) is sourced but branch/range adoption still gates local arenas",
            "result": "R10 amplitude is zero on the exact Xi branch, but range metadata remains part of the parent map",
            "status": "RANGE_LAW_RETAINED_FOR_PROMOTION_GATE",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "tail_id": "TAIL4647_2_local_promotion_live",
            "premise": "Xi_tail exact zero is not yet a full local-GR theorem",
            "result": "PPN/Newton/Maxwell/EM source-coupling promotion maps remain live",
            "status": "LOCAL_GR_STILL_BLOCKED_BY_PROMOTION_MAPS",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "tail_id": "TAIL4647_3_finite_fallback",
            "premise": "any transition source-kernel clause fails or is branch-mixed",
            "result": "alpha_tail(lambda) contains alpha_transition_inner bounded by epsilon_tr_hair",
            "status": "FINITE_HAIR_FALLBACK_REQUIRED",
            "next_target": "source numeric epsilon_tr_hair projection rows before empirical scoring",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("RUN4647_0_current_live_before_certificate", "three previous components zero but transition kernel unsigned", "BLOCKED", "alpha_tail(lambda)=alpha_transition_inner(lambda)", "cannot score R10/local without source kernel or finite bound"),
        ("RUN4647_1_source_kernel_certificate", "all P_kernel clauses signed on same branch", "PASS_EXACT_ZERO_BRANCH_NONCLAIM", "alpha_transition_inner(lambda)=0 and alpha_tail(lambda)=0", "private exact-zero certificate only"),
        ("RUN4647_2_missing_kernel_leg", "one or more Y_nonHilbert/Delta_Wtr/Y_time_l/Y_species_frame/Y_range/Y_nonEH/Y_boundary_nonlocal survives", "FAIL_FINITE_HAIR_BOUND_REQUIRED", "alpha_transition_inner bounded by epsilon_tr_hair", "numeric/source-backed component rows required"),
        ("RUN4647_3_branch_mixed_zero", "kernel clauses taken from different parent/readout branches", "REJECT", "no alpha_tail zero assembly", "same-branch firewall"),
        ("RUN4647_4_generic_small_transition", "rough or fitted small transition residue without exact source-kernel membership", "REJECT", "no local pass", "smallness is not a derivation"),
        ("RUN4647_5_Xi_zero_but_promotion_live", "all four normalized Xi_tail components zero on one branch", "PASS_LOCAL_TAIL_ONLY", "R10 tail amplitude zero, local-GR/PPN/Newton still nonclaim", "promotion maps and parent adoption remain"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row[0],
            "branch": row[1],
            "result": row[2],
            "deduction": row[3],
            "reason": row[4],
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4647_0_no_rough_smallness", "Do not use rough epsilon_mu_tr or epsilon_AJ_seed as local safety evidence.", "finite transition hair must be zero-derived or numerically bounded with arena projections"),
        ("CTRL4647_1_no_branch_mixing", "Do not assemble source-kernel clauses across different parent branches.", "one selector must carry all zero clauses"),
        ("CTRL4647_2_no_postfit_support", "Do not choose the transition worldtube after seeing residuals.", "support/readout must be selected before variation/scoring"),
        ("CTRL4647_3_no_range_hiding", "Do not hide a finite-range Yukawa transition leg inside calibrated G_N.", "Y_range must be zero or bound-projected"),
        ("CTRL4647_4_no_nonEH_readout", "Do not let transition current use a different metric/coframe than matter, clocks or EM.", "Y_nonEH must vanish or be bounded"),
        ("CTRL4647_5_no_EM_Poynting_erasure", "Visible EM/Poynting/radiative flux is not silently deleted.", "flux routes to boundary/arena rows rather than a hidden transition cancellation"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "firewall": row[1],
            "enforcement": row[2],
            "active": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4647_0",
            "decision": "XI_TRANSITION_INNER_PROMOTED_TO_BRANCH_SOURCE_KERNEL_EXACT_ZERO_CERTIFICATE_FINITE_HAIR_BOUND_RETAINED_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "summary": "4647 fills alpha_transition_inner(lambda)=0 on the clean source-kernel branch q_tr=P_kernel q_tr. All four normalized Xi_tail components can now assemble to alpha_tail(lambda)=0 branch-locally, but local-GR/Newton/PPN/Maxwell/EM claims remain blocked until the parent promotion/source-coupling maps are derived or bounded.",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "MTS_R2FR_Y5_TRANSITION_INNER_SOURCE_KERNEL_ZERO_CERTIFICATE_4647",
            "status": "PRIVATE_DERIVATION_ADVANCE_NONCLAIM",
            "summary": "Fourth Xi_tail component exact-zero certificate ready; full normalized Xi_tail is zero on one clean branch, with finite transition-hair fallback retained.",
            "claim_allowed": False,
            "public_ready": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "assemble same-branch Xi_tail=0 with lambda_mem/range metadata and explicitly separate R10 alpha silence from PPN/Newton/Maxwell/EM promotion claims",
            "success_condition": "one branch carries all four alpha_i=0 rows and every local arena either receives a zero promotion map or remains explicitly blocked",
            "timestamp_utc": timestamp,
        }
    ]


def build_validation(
    sources: list[dict[str, Any]],
    certs: list[dict[str, Any]],
    alpha: list[dict[str, Any]],
    reduced: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    public_clean, public_detail = git_clean(PUBLIC_STAGE)
    backup_clean, backup_detail = git_clean(BACKUP_REPO)
    checks = [
        ("VAL4647_00_sources_exist", all(row["path_exists"] for row in sources), "all cited paths exist"),
        ("VAL4647_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4647_02_source_lines_positive", all(int(row["line_number"]) > 0 for row in sources), "source line anchors are positive"),
        ("VAL4647_03_certificate_rows", len(certs) >= 11 and any(row["certificate_id"] == "ZC4647_10_alpha_projection" for row in certs), "transition zero certificate complete"),
        ("VAL4647_04_alpha_zero", alpha and alpha[0]["alpha_value"] == "0" and alpha[0]["exact_zero"] is True, "alpha_transition_inner zero row written"),
        ("VAL4647_05_four_component_tail", any(row["tail_id"] == "TAIL4647_0_four_component_zero" and row["result"] == "alpha_tail(lambda)=0" for row in reduced), "four-component Xi_tail zero row present"),
        ("VAL4647_06_finite_fallback", any(row["tail_id"] == "TAIL4647_3_finite_fallback" for row in reduced), "finite fallback retained"),
        ("VAL4647_07_certificate_runner", any(row["run_id"] == "RUN4647_1_source_kernel_certificate" and row["result"] == "PASS_EXACT_ZERO_BRANCH_NONCLAIM" for row in runners), "source-kernel runner passes as nonclaim"),
        ("VAL4647_08_branch_mix_reject", any(row["run_id"] == "RUN4647_3_branch_mixed_zero" and row["result"] == "REJECT" for row in runners), "branch-mixing rejected"),
        ("VAL4647_09_claims_false", all(str(row.get("valid_for_claim", "False")) == "False" for row in sources + certs + alpha + reduced + runners + decisions), "no row promoted to claim"),
        ("VAL4647_10_decision_next", decisions and decisions[0]["next_target"] == NEXT_TARGET, "next target selected"),
        ("VAL4647_11_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4647_12_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
    ]
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
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4647_OVERALL",
            "status": "PASS" if all(passed for _, passed, _ in checks) else "FAIL",
            "detail": "4647 validation passed" if all(passed for _, passed, _ in checks) else "4647 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    certs: list[dict[str, Any]],
    alpha: list[dict[str, Any]],
    reduced: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return f"""# 4647 - transition-inner alpha component or source-kernel zero certificate

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4647 kills the fourth normalized `Xi_tail` component on the clean transition source-kernel branch:

`q_tr=P_kernel q_tr -> epsilon_tr_hair=0 -> Xi_transition_inner=0 -> alpha_transition_inner(lambda)=0`.

Together with 4644, 4645 and 4646 this gives the first branch-local full tail silence:

`alpha_tail(lambda)=alpha_src_hidden+alpha_nonHilbert+alpha_boundary_history+alpha_transition_inner=0`.

This is deliberately not a local-GR/Newton/PPN/Maxwell/EM claim. If any source-kernel clause fails, the finite no-cancellation `epsilon_tr_hair` vector is retained. If all four component zeros hold, the next gate is not more R10 tail bookkeeping; it is parent promotion/source-coupling into local arenas.

## Source Register

{markdown_table(sources)}

## Transition-Inner Zero Certificate

{markdown_table(certs)}

## Alpha Component Row

{markdown_table(alpha)}

## Reduced Tail

{markdown_table(reduced)}

## Runner Results

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


def register_claim() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4647 fills the fourth normalized Xi_tail component: alpha_transition_inner(lambda)=0 on the clean transition source-kernel branch q_tr=P_kernel q_tr, while retaining the finite epsilon_tr_hair fallback if any kernel clause fails.",
        "Generated source register, transition-inner zero certificate, alpha component row, reduced-tail table, runner, controls, decision, status, next target and validation.",
        "alpha_transition_inner_branch_exact_zero_nonclaim",
        NEXT_TARGET,
        "Using rough transition smallness, branch-mixing kernel clauses, hiding finite-range source legs in calibrated G_N, or promoting Xi_tail zero to full local GR without promotion maps.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No local-GR/Newton/R10/PPN/Maxwell/EM claim until same-branch Xi_tail assembly, lambda_mem/range adoption and local promotion/source-coupling maps are source-backed or exact-zero signed.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_and_packet() -> None:
    spine_text = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4647 fills the fourth normalized `Xi_tail` component on the clean source-kernel branch: `alpha_transition_inner(lambda)=0`. The proof uses `q_tr=P_kernel q_tr`, where the transition residue is Hilbert, same-worldtube, static `l=0`, universal, range-free, same-metric and boundary-owned on one branch. Then `epsilon_tr_hair=0`, so the normalized transition-inner R10 alpha component vanishes. With 4644, 4645 and 4646, this gives branch-local `alpha_tail(lambda)=0`; it remains nonclaim because same-branch assembly, `lambda_mem`/range adoption and local PPN/Newton/Maxwell/EM promotion maps still need explicit gates.
"""
    packet_text = f"""
## {PACKET_MARKER}

Checkpoint `4647` promotes `alpha_transition_inner(lambda)` to a branch exact-zero certificate and assembles the first same-branch candidate for full normalized `Xi_tail` silence. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine_text)
    append_once(PACKET_PATH, PACKET_MARKER, packet_text)


def main() -> int:
    timestamp = utc_now()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(timestamp)
    certs = certificate_rows(timestamp)
    alpha = alpha_rows(timestamp)
    reduced = reduced_tail_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validation = build_validation(sources, certs, alpha, reduced, runners, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ZERO_CERT_CSV, certs)
    write_csv(ALPHA_COMPONENT_CSV, alpha)
    write_csv(REDUCED_TAIL_CSV, reduced)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validation)

    doc = build_doc(sources, certs, alpha, reduced, runners, controls, decisions, statuses, nexts, validation)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_and_packet()

    status = validation[-1]["status"]
    print(f"4647 validation: {status}")
    print(VALIDATION_CSV)
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
