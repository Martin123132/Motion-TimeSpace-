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
PUBLIC_STAGE = Path(r"D:\Users\ollet\Desktop\Motion-TimeSpace-public-stage")
BACKUP_REPO = Path(r"D:\Users\ollet\Desktop\laptop-back-up-")

CHECKPOINT = "4650"
CLAIM_ID = "L-492"
BRANCH = "MTS_R2FR_Y5_SINGLE_PARENT_ACTION_SELECTOR_SIGNATURE_OR_RESIDUAL_VECTOR_4650"
MARKER = "PPC4161_SINGLE_PARENT_ACTION_SELECTOR_SIGNATURE_OR_RESIDUAL_VECTOR_4650"
PACKET_MARKER = "PPC4161_PACKET_SINGLE_PARENT_ACTION_SELECTOR_SIGNATURE_OR_RESIDUAL_VECTOR_4650"
NEXT_TARGET = "4651-Y5-R2FR-parent-action-BGR-signature-line-or-first-residual-attack.md"

DOC_PATH = POST / "4650-Y5-R2FR-single-parent-action-selector-signature-or-residual-vector.md"
FORMAL_PATH = FORMAL / "666-PPC4161-single-parent-action-selector-signature-or-residual-vector.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4650_SOURCE_REGISTER.csv"
SIGNATURE_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4650_SELECTOR_SIGNATURE_AUDIT.csv"
RESIDUAL_VECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4650_GR_RESIDUAL_VECTOR.csv"
ATTACK_ORDER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4650_ATTACK_ORDER.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4650_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4650_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4650_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4650_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4650_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4650_VALIDATION.csv"

DOC_4649 = POST / "4649-Y5-R2FR-parent-selector-promotion-map-or-local-GR-contract.md"
CSV_4649_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4649_VALIDATION.csv"
CSV_4642_PARENT = SOURCE_DIR / "P8_Y5_R2FR_4642_PARENT_SIGNATURE_PACK.csv"
FORMAL_186 = FORMAL / "186-PPC4161-Hamiltonian-worldtube-mass-readout-glue.md"
FORMAL_191 = FORMAL / "191-PPC4161-Maxwell-Hodge-Poynting-stress-owner-theorem.md"
FORMAL_194 = FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md"
FORMAL_350 = FORMAL / "350-PPC4161-local-test-projection-matrix-source-contract-or-R10-PPN-smoke-runner.md"


def ts() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_number(path: Path, needle: str) -> int:
    for index, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, text: str) -> None:
    current = read_text(path)
    if marker in current:
        return
    suffix = "" if not current or current.endswith("\n") else "\n"
    path.write_text(current + suffix + text.lstrip("\n"), encoding="utf-8")


def csv_line(values: list[str]) -> str:
    buffer = io.StringIO()
    csv.writer(buffer, lineterminator="\n").writerow(values)
    return buffer.getvalue()


def git_clean(repo: Path) -> tuple[bool, str]:
    if not repo.exists() or not (repo / ".git").exists():
        return True, "absent or not git"
    result = subprocess.run(["git", "-C", str(repo), "status", "--porcelain"], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        return False, result.stderr.strip() or "git status failed"
    status = result.stdout.strip()
    return status == "", status or "clean"


def source_rows(now: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4650_00_4649_validation", CSV_4649_VALIDATION, "VAL4649_OVERALL", "4649 parent-selector contract passed."),
        ("SRC4650_01_4649_action", DOC_4649, "GRSEL4649_0_action_form", "parent action contract row."),
        ("SRC4650_02_4649_current_fail", DOC_4649, "RUN4649_0_current_corpus", "current corpus fail-closed row."),
        ("SRC4650_03_4649_signed_branch", DOC_4649, "RUN4649_1_parent_selector_signed", "conditional signed-parent pass row."),
        ("SRC4650_04_PS0", CSV_4642_PARENT, "PS4642_0", "single Hilbert source owner unsigned source pack row."),
        ("SRC4650_05_PS1", CSV_4642_PARENT, "PS4642_1", "source-label forgetting unsigned source pack row."),
        ("SRC4650_06_PS6", CSV_4642_PARENT, "PS4642_6", "common observed coframe/Hodge/tau unsigned source pack row."),
        ("SRC4650_07_PS7", CSV_4642_PARENT, "PS4642_7", "fixed projector/domain/lambda unsigned source pack row."),
        ("SRC4650_08_mass_glue", FORMAL_186, "Pi_M/H_tau/worldtube glue = 0 residual.", "Hamiltonian mass glue support."),
        ("SRC4650_09_EM_selector", FORMAL_191, "parent selector forbids independent EM source weights", "EM owner needs parent selector."),
        ("SRC4650_10_Gcal_spine", FORMAL_194, "same EH block, same Hilbert source, same Hamiltonian mass, one calibrated coupling", "source coupling structural spine."),
        ("SRC4650_11_PPN_missing", FORMAL_350, "MISSING_LOCAL_METRIC_TRANSFER_MATRIX", "PPN residual matrix if selector fails."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, note in specs:
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
                "timestamp_utc": now,
            }
        )
    return rows


def signature_audit(now: str) -> list[dict[str, Any]]:
    rows = [
        ("SIG4650_0_EH_action_block", "EH[g_obs] local action block", "supported by 194/187 as local reduction spine", "NEEDS_SINGLE_PARENT_ACTION_LINE", "E_EH_action_owner"),
        ("SIG4650_1_constant_Gcal", "constant calibrated kappa_eff/G_cal", "supported structurally by 194; numeric G prediction not required", "STRUCTURAL_SUPPORT_PARENT_SCALE_OPEN", "E_kappa_drift"),
        ("SIG4650_2_Hilbert_source_owner", "single Hilbert source stress owner", "PS4642_0 formally compatible but unsigned; 186 supports mass glue", "UNSIGNED_PARENT_SELECTOR", "E_source_owner"),
        ("SIG4650_3_source_label_silence", "no source-label/source-weight/environment selector", "PS4642_1 formally compatible but unsigned", "UNSIGNED_PARENT_SELECTOR", "E_source_label"),
        ("SIG4650_4_common_readout", "same g_obs/e_obs/Hodge/tau for matter, EM, clocks, orbital and PPN", "PS4642_6 formally compatible but unsigned", "UNSIGNED_PARENT_SELECTOR", "E_metric_coframe_fork"),
        ("SIG4650_5_EM_stress_owner", "Maxwell-Hodge/Poynting stress inside same Hilbert T_total", "191 supports this only while parent selector forbids independent EM weights/metric", "CONDITIONAL_SUPPORT_SELECTOR_UNSIGNED", "E_EM_metric_source"),
        ("SIG4650_6_Btail_silence", "B_tail -> alpha_tail(lambda)=0", "4648 proves the contract but not that the parent signs B_tail globally", "CONDITIONAL_SUPPORT_SELECTOR_UNSIGNED", "E_tail_selector"),
        ("SIG4650_7_boundary_routing", "radiative/boundary flux routed as Hamiltonian boundary charge", "192 supports no-flux private selector; global parent adoption still needed", "CONDITIONAL_SUPPORT_SELECTOR_UNSIGNED", "E_boundary_flux"),
        ("SIG4650_8_fixed_domain_projector", "fixed worldtube/projector/lambda before scoring", "PS4642_7 formally compatible but unsigned", "UNSIGNED_PARENT_SELECTOR", "E_domain_projector"),
        ("SIG4650_9_PPN_transfer", "exact-GR PPN or explicit Pi_PPN transfer matrix", "350 says Pi_PPN remains matrix-gated if selector fails", "EXACT_IF_BGR_ELSE_MATRIX_MISSING", "E_PPN_transfer"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "signature_id": row[0],
            "selector_clause": row[1],
            "current_support": row[2],
            "signature_status": row[3],
            "residual_if_unsigned": row[4],
            "parent_signed_as_one_branch": False,
            "valid_for_claim": False,
            "timestamp_utc": now,
        }
        for row in rows
    ]


def residual_vector(now: str) -> list[dict[str, Any]]:
    rows = [
        ("RGR4650_0_E_EH_action_owner", "E_EH_action_owner", "parent action has no explicit single local EH-selector line", "derive/write S_local[B_GR] from parent action or keep EH-action residual"),
        ("RGR4650_1_E_kappa_drift", "E_kappa_drift", "kappa_eff/G_cal constancy not signed by one parent scale law branch", "prove D_A kappa_eff=0 on B_GR or bound Gdot/G"),
        ("RGR4650_2_E_source_owner", "E_source_owner", "single Hilbert source owner still unsigned in parent pack", "sign PS4642_0 or push to WEP/G_cal residual"),
        ("RGR4650_3_E_source_label", "E_source_label", "source-label/source-weight silence still unsigned", "sign PS4642_1 or compute source-composition residual"),
        ("RGR4650_4_E_metric_coframe_fork", "E_metric_coframe_fork", "common observed metric/coframe/Hodge/tau still unsigned", "sign PS4642_6 or compute PPN/clock/EM fork residual"),
        ("RGR4650_5_E_EM_metric_source", "E_EM_metric_source", "EM/Poynting owner is conditional on no second EM metric/source weights", "sign EM same-Hodge selector or retain EM stress residual"),
        ("RGR4650_6_E_tail_selector", "E_tail_selector", "B_tail component zeros not signed as one global parent selector", "sign 4648 B_tail inside parent action or use finite alpha component envelope"),
        ("RGR4650_7_E_boundary_flux", "E_boundary_flux", "boundary/no-flux selector not globally parent-adopted", "sign Hamiltonian boundary routing or keep flux residual"),
        ("RGR4650_8_E_domain_projector", "E_domain_projector", "fixed worldtube/projector/lambda before scoring still unsigned", "sign PS4642_7 or reject postfit scoring"),
        ("RGR4650_9_E_PPN_transfer", "E_PPN_transfer", "if B_GR is not signed, exact-GR PPN values cannot be imported", "derive Pi_PPN transfer matrix or fail closed"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "residual_id": row[0],
            "symbol": row[1],
            "meaning": row[2],
            "required_repair": row[3],
            "zero_condition": "single parent selector B_GR signs the corresponding clause before readout/scoring",
            "valid_for_claim": False,
            "timestamp_utc": now,
        }
        for row in rows
    ]


def attack_order(now: str) -> list[dict[str, Any]]:
    rows = [
        (1, "ATT4650_1_parent_action_line", "write or derive the explicit S_local[B_GR] parent action branch", "without this, every downstream clause can be accused of branch-mixing"),
        (2, "ATT4650_2_common_readout", "derive same g_obs/e_obs/Hodge/tau selector for matter, EM, clocks, orbital and PPN", "this collapses metric-fork, EM-Hodge and clock readout residuals together"),
        (3, "ATT4650_3_Hilbert_source_label", "prove single Hilbert source owner plus no source-label/source-weight slots", "this attacks WEP/source coupling and calibrated G at the root"),
        (4, "ATT4650_4_Btail_embedding", "embed 4648 B_tail inside the same parent selector instead of a separate branch certificate", "turns R10 tail silence into part of B_GR"),
        (5, "ATT4650_5_boundary_domain", "sign boundary/Hamiltonian routing and fixed worldtube/projector/lambda before scoring", "prevents postfit/domain leakage"),
        (6, "ATT4650_6_PPN_fallback", "if any of 1-5 fail, build Pi_PPN transfer matrix for the residual vector", "keeps the local branch testable instead of rhetorical"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "priority": priority,
            "attack_id": attack_id,
            "task": task,
            "why": why,
            "next_target": NEXT_TARGET if priority == 1 else "",
            "timestamp_utc": now,
        }
        for priority, attack_id, task, why in rows
    ]


def runner_rows(now: str) -> list[dict[str, Any]]:
    rows = [
        ("RUN4650_0_current_state", "component and promotion contracts exist, but B_GR is not signed as one parent action selector", "FAIL_CLOSED_TO_RGR_VECTOR", "use R_GR residual vector, no local claim"),
        ("RUN4650_1_direct_signature", "explicit S_local[B_GR] line found with all selector clauses", "PASS_CONDITIONAL_LOCAL_GR_BRANCH_NONCLAIM", "import 4649 promotion theorem"),
        ("RUN4650_2_piecewise_signature", "clauses supported by different files/branches only", "REJECT_BRANCH_MIXING", "supporting pieces are not one parent selector"),
        ("RUN4650_3_residual_attack", "B_GR cannot be signed yet", "PROCEED_TO_FIRST_RESIDUAL_ATTACK", "start with E_EH_action_owner/common readout rather than more R10 alpha rows"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "run_id": row[0],
            "branch": row[1],
            "result": row[2],
            "reason": row[3],
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": now,
        }
        for row in rows
    ]


def controls(now: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4650_0_no_branch_mixing", "Do not treat separately supported clauses as one selector."),
        ("CTRL4650_1_no_local_claim", "Do not claim local GR/Newton/Maxwell/PPN from 4650; current state fails closed."),
        ("CTRL4650_2_no_more_alpha_chase", "Do not keep chasing R10 alpha components before parent selector/source-coupling is attacked."),
        ("CTRL4650_3_no_G_trap", "Do not make numeric G prediction the gate; make one calibrated G_cal with no hidden source dependence the gate."),
        ("CTRL4650_4_no_PPN_import", "Do not import exact GR PPN values unless B_GR is signed; otherwise derive Pi_PPN."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "firewall": firewall,
            "active": True,
            "valid_for_claim": False,
            "timestamp_utc": now,
        }
        for control_id, firewall in rows
    ]


def decisions(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4650_0",
            "decision": "BGR_NOT_PARENT_SIGNED_YET_RESIDUAL_VECTOR_RGR_CREATED_ATTACK_PARENT_ACTION_LINE_FIRST",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "summary": "4650 attempts the actual signature check. The current corpus has strong supported pieces, but not one explicit parent action/readout selector B_GR signing them together. Therefore the route does not die; it fails into the compact residual vector R_GR, with the first attack being the parent action line S_local[B_GR].",
            "timestamp_utc": now,
        }
    ]


def statuses(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": BRANCH,
            "status": "PRIVATE_SELECTOR_AUDIT_NONCLAIM",
            "summary": "B_GR selector is not signed as one branch yet; explicit R_GR residual vector and attack order created.",
            "claim_allowed": False,
            "public_ready": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": now,
        }
    ]


def nexts(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "try to write/derive the explicit parent action selector line S_local[B_GR]; if impossible, attack E_EH_action_owner and E_metric_coframe_fork first",
            "success_condition": "one parent action/readout branch signs EH metric block, common readout, Hilbert source, EM Hodge, B_tail, boundary routing and fixed domain before scoring",
            "timestamp_utc": now,
        }
    ]


def validation_rows(src: list[dict[str, Any]], sig: list[dict[str, Any]], residual: list[dict[str, Any]], attack: list[dict[str, Any]], runs: list[dict[str, Any]], dec: list[dict[str, Any]], now: str) -> list[dict[str, Any]]:
    public_clean, public_detail = git_clean(PUBLIC_STAGE)
    backup_clean, backup_detail = git_clean(BACKUP_REPO)
    checks = [
        ("VAL4650_00_sources_exist", all(row["path_exists"] for row in src), "all cited paths exist"),
        ("VAL4650_01_needles_found", all(row["needle_found"] for row in src), "all source needles found"),
        ("VAL4650_02_line_anchors", all(int(row["line_number"]) > 0 for row in src), "all source line anchors positive"),
        ("VAL4650_03_signature_audit_rows", len(sig) >= 10, "selector signature audit rows created"),
        ("VAL4650_04_not_parent_signed", all(row["parent_signed_as_one_branch"] is False for row in sig), "audit does not falsely sign B_GR"),
        ("VAL4650_05_residual_vector_rows", len(residual) >= 10 and any(row["symbol"] == "E_EH_action_owner" for row in residual), "R_GR residual vector created"),
        ("VAL4650_06_attack_order", attack and attack[0]["attack_id"] == "ATT4650_1_parent_action_line", "parent action line is first attack"),
        ("VAL4650_07_current_fail_closed", any(row["run_id"] == "RUN4650_0_current_state" and row["result"] == "FAIL_CLOSED_TO_RGR_VECTOR" for row in runs), "current state fails closed to residual vector"),
        ("VAL4650_08_branch_mix_reject", any(row["run_id"] == "RUN4650_2_piecewise_signature" and row["result"] == "REJECT_BRANCH_MIXING" for row in runs), "branch mixing rejected"),
        ("VAL4650_09_no_claim_allowed", all(str(row.get("valid_for_claim", "False")) == "False" for row in src + sig + residual + runs + dec), "no row marked claim-grade"),
        ("VAL4650_10_decision_next", dec and dec[0]["next_target"] == NEXT_TARGET, "next target selected"),
        ("VAL4650_11_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4650_12_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": now,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4650_OVERALL",
            "status": "PASS" if all(passed for _, passed, _ in checks) else "FAIL",
            "detail": "4650 validation passed" if all(passed for _, passed, _ in checks) else "4650 validation failed",
            "timestamp_utc": now,
        }
    )
    return rows


def build_doc(src: list[dict[str, Any]], sig: list[dict[str, Any]], residual: list[dict[str, Any]], attack: list[dict[str, Any]], runs: list[dict[str, Any]], ctrl: list[dict[str, Any]], dec: list[dict[str, Any]], stat: list[dict[str, Any]], nxt: list[dict[str, Any]], val: list[dict[str, Any]]) -> str:
    return f"""# 4650 - single parent action selector signature or residual vector

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4650 performs the signature check that 4649 demanded.

Outcome: the current corpus has strong supported pieces, but it does **not** yet contain one explicit parent action/readout branch `B_GR` signing all of them together. So the correct result is not another broad blocker and not a fake pass. It is:

`current corpus -> fail closed to R_GR`.

The residual vector is now compact:

`R_GR = (E_EH_action_owner, E_kappa_drift, E_source_owner, E_source_label, E_metric_coframe_fork, E_EM_metric_source, E_tail_selector, E_boundary_flux, E_domain_projector, E_PPN_transfer)`.

Next best attack is the parent action line itself: derive or write `S_local[B_GR]` from the parent MTS action, then prove the common readout/source/Hodge/domain clauses are not separate branch assumptions.

## Source Register

{md_table(src)}

## Selector Signature Audit

{md_table(sig)}

## GR Residual Vector

{md_table(residual)}

## Attack Order

{md_table(attack)}

## Runner Results

{md_table(runs)}

## Controls

{md_table(ctrl)}

## Decision

{md_table(dec)}

## Status

{md_table(stat)}

## Next Target

{md_table(nxt)}

## Validation

{md_table(val)}
"""


def register_claim() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4650 audits whether the 4649 B_GR local-GR selector is signed by one parent action branch. Current corpus has supported pieces but no single explicit parent action/readout selector, so it fails closed into R_GR with a prioritized attack order.",
        "Generated source register, selector signature audit, GR residual vector, attack order, runner, controls, decision, status, next target and validation.",
        "BGR_signature_audit_residual_vector_nonclaim",
        NEXT_TARGET,
        "Treating supported pieces as one parent branch, claiming local GR before B_GR is signed, continuing R10 alpha chasing before parent selector attack, or importing exact GR PPN values without B_GR.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/Maxwell/EM claim until B_GR is parent-signed or R_GR residuals are explicitly bounded/source-backed and pass.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4650 tests whether the 4649 `B_GR` selector is actually parent-signed. It is not yet signed as one explicit parent action/readout branch. The current route therefore fails closed into `R_GR=(E_EH_action_owner,E_kappa_drift,E_source_owner,E_source_label,E_metric_coframe_fork,E_EM_metric_source,E_tail_selector,E_boundary_flux,E_domain_projector,E_PPN_transfer)`. This is useful: the next target is no longer vague local-GR repair, but the parent action line `S_local[B_GR]` or the first residual attack.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4650` converts the local-GR promotion problem into a single selector-signature target plus explicit `R_GR` fallback. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    now = ts()
    src = source_rows(now)
    sig = signature_audit(now)
    residual = residual_vector(now)
    attack = attack_order(now)
    runs = runner_rows(now)
    ctrl = controls(now)
    dec = decisions(now)
    stat = statuses(now)
    nxt = nexts(now)
    val = validation_rows(src, sig, residual, attack, runs, dec, now)

    write_csv(SOURCE_REGISTER, src)
    write_csv(SIGNATURE_AUDIT_CSV, sig)
    write_csv(RESIDUAL_VECTOR_CSV, residual)
    write_csv(ATTACK_ORDER_CSV, attack)
    write_csv(RUNNER_CSV, runs)
    write_csv(CONTROL_CSV, ctrl)
    write_csv(DECISION_CSV, dec)
    write_csv(STATUS_CSV, stat)
    write_csv(NEXT_CSV, nxt)
    write_csv(VALIDATION_CSV, val)

    doc = build_doc(src, sig, residual, attack, runs, ctrl, dec, stat, nxt, val)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = val[-1]["status"]
    print(f"4650 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
