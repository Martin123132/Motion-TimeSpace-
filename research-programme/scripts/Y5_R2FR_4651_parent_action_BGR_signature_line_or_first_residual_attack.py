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

CHECKPOINT = "4651"
CLAIM_ID = "L-493"
BRANCH = "MTS_R2FR_Y5_PARENT_ACTION_BGR_SIGNATURE_LINE_OR_FIRST_RESIDUAL_ATTACK_4651"
MARKER = "PPC4161_PARENT_ACTION_BGR_SIGNATURE_LINE_OR_FIRST_RESIDUAL_ATTACK_4651"
PACKET_MARKER = "PPC4161_PACKET_PARENT_ACTION_BGR_SIGNATURE_LINE_OR_FIRST_RESIDUAL_ATTACK_4651"
NEXT_TARGET = "4652-Y5-R2FR-AMF-Palatini-IR-selector-origin-or-EH-effective-demotion.md"

DOC_PATH = POST / "4651-Y5-R2FR-parent-action-BGR-signature-line-or-first-residual-attack.md"
FORMAL_PATH = FORMAL / "667-PPC4161-parent-action-BGR-signature-line-or-first-residual-attack.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4651_SOURCE_REGISTER.csv"
ACTION_LINE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4651_BGR_ACTION_LINE_CANDIDATE.csv"
ADOPTION_GAP_CSV = SOURCE_DIR / "P8_Y5_R2FR_4651_ADOPTION_GAP_VECTOR.csv"
E_EH_REDUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4651_E_EH_ACTION_OWNER_REDUCTION.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4651_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4651_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4651_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4651_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4651_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4651_VALIDATION.csv"

DOC_4650 = POST / "4650-Y5-R2FR-single-parent-action-selector-signature-or-residual-vector.md"
CSV_4650_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4650_VALIDATION.csv"
DOC_4648 = POST / "4648-Y5-R2FR-same-branch-Xi-tail-zero-assembly-and-lambda-promotion-gate.md"
DOC_4278 = POST / "4278-Y5-R2FR-left-hand-EH-Newton-limit-or-residual-EFT-bound-gate.md"
FORMAL_190 = FORMAL / "190-PPC4161-parent-action-selector-or-local-branch-quarantine.md"
FORMAL_196 = FORMAL / "196-PPC4161-minimal-parent-action-adoption-matrix.md"
FORMAL_194 = FORMAL / "194-PPC4161-calibrated-source-coupling-kappa-to-GN-law.md"
SPINE_07 = FORMAL / "07-unification-spine.md"


def now() -> str:
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
    existing = read_text(path)
    if marker in existing:
        return
    suffix = "" if not existing or existing.endswith("\n") else "\n"
    path.write_text(existing + suffix + text.lstrip("\n"), encoding="utf-8")


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
    detail = result.stdout.strip()
    return detail == "", detail or "clean"


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4651_00_4650_validation", CSV_4650_VALIDATION, "VAL4650_OVERALL", "4650 selector audit passed."),
        ("SRC4651_01_4650_EEH", DOC_4650, "RGR4650_0_E_EH_action_owner", "first residual is EH action owner."),
        ("SRC4651_02_4650_attack", DOC_4650, "ATT4650_1_parent_action_line", "parent action line selected as first attack."),
        ("SRC4651_03_190_selector", FORMAL_190, "S_parent|loc =", "older parent-action selector line."),
        ("SRC4651_04_190_action_sig", FORMAL_190, "The selector clauses are action-level signatures.", "do not set clauses to zero unless action signs them."),
        ("SRC4651_05_196_candidate", FORMAL_196, "S_EH[g_obs;kappa_*]", "minimal action candidate includes EH block."),
        ("SRC4651_06_196_not_derived", FORMAL_196, "It is not yet a derivation of the EH block from MTS.", "candidate is not parent derivation."),
        ("SRC4651_07_196_hard_root", FORMAL_196, "EH/local metric principal block: hard root", "EH origin remains hard root."),
        ("SRC4651_08_4278_chain", DOC_4278, "A_MF + Palatini IR selector", "conditional Palatini/EC route."),
        ("SRC4651_09_4278_residuals", DOC_4278, "c_T, c_R2/M_R, c_D, c_Gamma, c_bdy, delta_kappa, Lambda_eff.", "residual EFT fallback."),
        ("SRC4651_10_4648_Btail", DOC_4648, "B_tail -> alpha_tail(lambda)=0", "local tail silence contract."),
        ("SRC4651_11_194_Gcal", FORMAL_194, "same EH block, same Hilbert source, same Hamiltonian mass, one calibrated coupling", "calibrated GR-like source coupling spine."),
        ("SRC4651_12_spine_4540", SPINE_07, "4540 derives the correct IR fork.", "later spine confirms IR fork remains effective/nonclaim."),
        ("SRC4651_13_spine_parent_false", SPINE_07, "But current parent derivation is still false because", "parent origin, IR scale law and no-extra-mode clauses remain unsigned."),
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
                "timestamp_utc": timestamp,
            }
        )
    return rows


def action_line_rows(timestamp: str) -> list[dict[str, Any]]:
    line = (
        "S_local[B_GR] := S_EC[e,omega;kappa_eff] + S_src[psi,A,g_obs,theta] "
        "+ S_top^kappa[A_3,kappa_*] + S_MTS^perp[Xi,g_obs;q] + S_bdy"
    )
    reduced = (
        "B_GR plus Palatini/EC torsion-nonmetricity silence plus no-extra-light-mode/scale-gap selector "
        "gives S_EH[g_obs;kappa_eff] + S_src[g_obs,psi,A,theta] + S_bdy + harmless topological/zero terms"
    )
    rows = [
        ("BGR4651_0_candidate_line", "candidate parent action line", line, "WRITTEN_AS_ADOPTION_NORMAL_FORM", "not parent-derived from MTS yet"),
        ("BGR4651_1_visible_source", "source action", "S_src=S_matter[psi,g_obs,theta]+S_EM[A,g_obs]+S_binding[psi,A,g_obs]+int dB_impr+S_rest^top/zero", "SUPPORTED_BY_EXISTING_HILBERT_SOURCE_LADDER", "must be signed by same parent selector"),
        ("BGR4651_2_EC_to_EH", "Palatini/EC reduction", "S_EC[e,omega;kappa_eff] -> S_EH[g_obs;kappa_eff]+boundary", "CONDITIONAL_ON_IR_SELECTOR", "A_MF, scale gap, torsion/nonmetricity/no-extra-mode clauses unsigned"),
        ("BGR4651_3_tail_embedding", "MTS perpendicular sector", "B_tail -> delta S_MTS^perp/delta g_obs is zero or routed to explicit EFT residuals", "USES_4648_TAIL_SILENCE_CONTRACT", "must be embedded inside same B_GR branch"),
        ("BGR4651_4_reduced_local_packet", "reduced local packet", reduced, "CONDITIONAL_LOCAL_GR_PACKET", "private nonclaim until adoption gaps close"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "line_id": row[0],
            "object": row[1],
            "statement": row[2],
            "status": row[3],
            "remaining_gap": row[4],
            "parent_derived": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def adoption_gap_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("GAP4651_0_A_MF_origin", "A_MF parent origin", "equivalence/frame map that selects the observed local metric/coframe", "unsigned", "derive from parent quotient/coarse-graining or demote to explicit equivalence-principle-like axiom"),
        ("GAP4651_1_Palatini_IR_selector", "Palatini/EC IR selector", "why EC/Palatini is the selected local principal block", "conditional", "prove IR selector from MTS parent structure"),
        ("GAP4651_2_scale_gap", "scale/gap hierarchy", "why non-EH carriers are heavy, zero, topological, boundary-routed or projected silent", "unsigned", "derive parent scale law or keep EFT coefficients"),
        ("GAP4651_3_no_extra_light_modes", "no extra unscreened mode rule", "forbid light scalar/tensor/vector residues at Solar/local scales", "unsigned", "prove no-extra-mode selector or score R10/PPN/orbital bounds"),
        ("GAP4651_4_q_natural_descent", "quotient/q-natural descent", "same action descends to g_obs, matter, EM, clocks and local tests", "unsigned", "derive one parent readout functor/selector"),
        ("GAP4651_5_tail_embedding", "B_tail embedding", "four alpha-zero certificates are inside S_local[B_GR], not a detached branch", "conditional", "sign B_tail clauses in the parent action line"),
        ("GAP4651_6_cGamma_survivor", "c_Gamma memory hair", "MTS-specific local memory coupling surviving previous private reductions", "live", "derive parent memory no-hair/operator or keep finite product bounds"),
        ("GAP4651_7_cR2_Lambda_boundary", "c_R2/M_R, Lambda_eff and boundary leakage", "curvature-square/range, local cosmological payload and boundary/projector residues", "fallback", "zero/heavy/boundary-route or score finite rows"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gap_id": row[0],
            "gap": row[1],
            "meaning": row[2],
            "current_status": row[3],
            "required_next": row[4],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def eh_reduction_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("EEH4651_0_before", "E_EH_action_owner", "parent action has no explicit single local EH-selector line", "from 4650", "BROAD_RESIDUAL"),
        ("EEH4651_1_after_line", "E_EH_action_owner", "S_local[B_GR] candidate/adoption-normal-form line is now written", "4651", "NARROWED_NOT_ZERO"),
        ("EEH4651_2_new_decomposition", "E_EH_action_owner", "E_A_MF_origin + E_Palatini_IR + E_scale_gap + E_no_extra_modes + E_q_descent", "4651", "DECOMPOSED_RESIDUAL"),
        ("EEH4651_3_zero_condition", "E_EH_action_owner=0", "all adoption gaps close on one parent action/readout branch", "future", "ZERO_CONDITION_DEFINED"),
        ("EEH4651_4_fallback", "E_EH_action_owner!=0", "use residual EFT envelope c_T,c_R2/M_R,c_D,c_Gamma,c_bdy,delta_kappa,Lambda_eff", "4278", "FINITE_EFT_FALLBACK"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "reduction_id": row[0],
            "object": row[1],
            "statement": row[2],
            "basis": row[3],
            "status": row[4],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("RUN4651_0_current_state", "candidate S_local[B_GR] line written, adoption gaps unsigned", "PARTIAL_PROGRESS_FAIL_CLOSED", "E_EH_action_owner narrowed but not zero"),
        ("RUN4651_1_parent_adoption_signed", "A_MF, Palatini IR, scale gap, no extra modes, q-natural descent and B_tail embedding signed on one branch", "PASS_CONDITIONAL_BGR_ACTION_NONCLAIM", "import 4649 local-GR promotion theorem"),
        ("RUN4651_2_effective_GR_demote", "S_local[B_GR] adopted as effective local closure without parent origin proof", "ALLOW_PRIVATE_EFFECTIVE_BRANCH_ONLY", "label as effective GR reduction, not derived fundamental theory"),
        ("RUN4651_3_EFT_fallback", "any adoption gap fails", "FAIL_TO_EFT_RESIDUAL_ENVELOPE", "score c_T,c_R2/M_R,c_D,c_Gamma,c_bdy,delta_kappa,Lambda_eff"),
        ("RUN4651_4_branch_mix", "Palatini, source, tail or readout clauses assembled from different selectors", "REJECT", "not one parent action branch"),
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
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("CTRL4651_0_no_candidate_as_derivation", "Writing S_local[B_GR] is progress, not proof that MTS derives EH."),
        ("CTRL4651_1_no_effective_GR_disguise", "If EH is adopted as effective closure, label it that way."),
        ("CTRL4651_2_no_clause_mixing", "A_MF, Palatini, source, EM, B_tail and boundary clauses must be on one branch."),
        ("CTRL4651_3_no_G_trap", "Numeric G prediction is not the gate; constant calibrated G_cal with no hidden source dependence is the gate."),
        ("CTRL4651_4_no_tail_escape", "B_tail silence must be embedded inside S_local[B_GR], not attached after local tests."),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": control_id,
            "firewall": firewall,
            "active": True,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for control_id, firewall in rows
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4651_0",
            "decision": "BGR_ACTION_LINE_WRITTEN_AS_ADOPTION_NORMAL_FORM_EEH_NARROWED_TO_ADOPTION_GAPS_NONCLAIM",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "summary": "4651 recovers and sharpens the parent action route: an explicit S_local[B_GR] candidate/adoption-normal-form line is now written using the existing selector theorem, minimal adoption matrix, Palatini/EC-to-EH chain, source/Hilbert packet and 4648 B_tail silence. This narrows E_EH_action_owner from line-missing to adoption-origin gaps: A_MF origin, Palatini IR selector, scale gap, no extra light modes, q-natural descent and B_tail embedding. It is not a parent derivation yet.",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": BRANCH,
            "status": "PRIVATE_DERIVATION_ADVANCE_NONCLAIM",
            "summary": "S_local[B_GR] candidate line exists; E_EH_action_owner reduced to adoption gaps and EFT fallback.",
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
            "reason": "attack the actual origin of the B_GR action line: A_MF/Palatini IR selector, parent scale gap, no-extra-mode rule and q-natural descent",
            "success_condition": "S_local[B_GR] is derived from parent MTS variables rather than adopted as an effective local GR closure; otherwise explicitly demote the branch and score EFT residuals",
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    action: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    public_clean, public_detail = git_clean(PUBLIC_STAGE)
    backup_clean, backup_detail = git_clean(BACKUP_REPO)
    checks = [
        ("VAL4651_00_sources_exist", all(row["path_exists"] for row in sources), "all cited paths exist"),
        ("VAL4651_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4651_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4651_03_action_line_written", any(row["line_id"] == "BGR4651_0_candidate_line" and "S_local[B_GR]" in row["statement"] for row in action), "candidate B_GR action line written"),
        ("VAL4651_04_not_parent_derived", all(row["parent_derived"] is False for row in action), "action line not falsely marked parent-derived"),
        ("VAL4651_05_gap_vector", len(gaps) >= 8 and any(row["gap_id"] == "GAP4651_0_A_MF_origin" for row in gaps), "adoption gap vector written"),
        ("VAL4651_06_EEH_narrowed", any(row["reduction_id"] == "EEH4651_2_new_decomposition" for row in reduction), "E_EH residual decomposed"),
        ("VAL4651_07_EFT_fallback", any(row["reduction_id"] == "EEH4651_4_fallback" for row in reduction), "EFT fallback retained"),
        ("VAL4651_08_current_fail_closed", any(row["run_id"] == "RUN4651_0_current_state" and row["result"] == "PARTIAL_PROGRESS_FAIL_CLOSED" for row in runners), "current branch fails closed after partial progress"),
        ("VAL4651_09_effective_demote_guard", any(row["run_id"] == "RUN4651_2_effective_GR_demote" for row in runners), "effective GR demotion guard present"),
        ("VAL4651_10_no_claim_allowed", all(str(row.get("valid_for_claim", "False")) == "False" for row in sources + action + gaps + reduction + runners + decisions), "no row marked claim-grade"),
        ("VAL4651_11_decision_next", decisions and decisions[0]["next_target"] == NEXT_TARGET, "next target selected"),
        ("VAL4651_12_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4651_13_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
    ]
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4651_OVERALL",
            "status": "PASS" if all(passed for _, passed, _ in checks) else "FAIL",
            "detail": "4651 validation passed" if all(passed for _, passed, _ in checks) else "4651 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    action: list[dict[str, Any]],
    gaps: list[dict[str, Any]],
    reduction: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4651 - parent action B_GR signature line or first residual attack

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4651 does not pretend the parent action is solved. It does something better: it writes the explicit local action line that the parent must derive.

`S_local[B_GR] := S_EC[e,omega;kappa_eff] + S_src[psi,A,g_obs,theta] + S_top^kappa[A_3,kappa_*] + S_MTS^perp[Xi,g_obs;q] + S_bdy`.

With the Palatini/EC IR selector, torsion/nonmetricity silence, no-extra-light-mode/scale-gap selector, common readout, Hilbert source, Maxwell-Hodge source, and embedded `B_tail`, this reduces to the local GR packet. But existing sources say this is an adoption candidate, not yet a derivation of EH from MTS.

So the first residual is narrowed:

`E_EH_action_owner -> E_A_MF_origin + E_Palatini_IR + E_scale_gap + E_no_extra_modes + E_q_descent`.

That is a useful rung: we now know exactly what must be proved to make the local GR bridge more than effective-GR closure.

## Source Register

{md_table(sources)}

## B_GR Action Line Candidate

{md_table(action)}

## Adoption Gap Vector

{md_table(gaps)}

## E_EH Action Owner Reduction

{md_table(reduction)}

## Runner Results

{md_table(runners)}

## Controls

{md_table(controls)}

## Decision

{md_table(decisions)}

## Status

{md_table(statuses)}

## Next Target

{md_table(nexts)}

## Validation

{md_table(validations)}
"""


def register_claim() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4651 writes the explicit S_local[B_GR] parent-action candidate/adoption-normal-form line and narrows E_EH_action_owner into concrete adoption gaps: A_MF origin, Palatini IR selector, scale gap, no extra light modes, q-natural descent and B_tail embedding.",
        "Generated source register, B_GR action-line candidate, adoption gap vector, E_EH reduction, runner, controls, decision, status, next target and validation.",
        "BGR_action_line_candidate_EEH_gap_reduction_nonclaim",
        NEXT_TARGET,
        "Treating the candidate action line as a parent derivation, hiding EH adoption as MTS derivation, or mixing Palatini/source/tail/readout clauses across branches.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/Maxwell/EM claim until S_local[B_GR] is derived from parent MTS variables or the EFT residual envelope is source-backed and passes.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4651 writes the explicit candidate local parent-action selector line `S_local[B_GR] := S_EC[e,omega;kappa_eff] + S_src[psi,A,g_obs,theta] + S_top^kappa[A_3,kappa_*] + S_MTS^perp[Xi,g_obs;q] + S_bdy`. Under the Palatini/EC IR selector, torsion/nonmetricity silence, no-extra-light-mode/scale-gap rule, common readout, Hilbert source, Maxwell-Hodge source and embedded `B_tail`, this reduces to the local GR packet. Existing sources still mark it as an adoption candidate, not a parent derivation, so `E_EH_action_owner` is narrowed to `E_A_MF_origin + E_Palatini_IR + E_scale_gap + E_no_extra_modes + E_q_descent` rather than killed.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4651` turns the first local-GR residual into a precise parent-action origin problem. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    action = action_line_rows(timestamp)
    gaps = adoption_gap_rows(timestamp)
    reduction = eh_reduction_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, action, gaps, reduction, runners, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ACTION_LINE_CSV, action)
    write_csv(ADOPTION_GAP_CSV, gaps)
    write_csv(E_EH_REDUCTION_CSV, reduction)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, action, gaps, reduction, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4651 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
