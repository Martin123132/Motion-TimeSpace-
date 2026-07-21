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

CHECKPOINT = "4652"
CLAIM_ID = "L-494"
BRANCH = "MTS_R2FR_Y5_AMF_PALATINI_IR_SELECTOR_ORIGIN_OR_EH_EFFECTIVE_DEMOTION_4652"
MARKER = "PPC4161_AMF_PALATINI_IR_SELECTOR_ORIGIN_OR_EH_EFFECTIVE_DEMOTION_4652"
PACKET_MARKER = "PPC4161_PACKET_AMF_PALATINI_IR_SELECTOR_ORIGIN_OR_EH_EFFECTIVE_DEMOTION_4652"
NEXT_TARGET = "4653-Y5-R2FR-cD-same-coframe-parent-functor-or-WEP-clock-EM-bound.md"

DOC_PATH = POST / "4652-Y5-R2FR-AMF-Palatini-IR-selector-origin-or-EH-effective-demotion.md"
FORMAL_PATH = FORMAL / "668-PPC4161-AMF-Palatini-IR-selector-origin-or-EH-effective-demotion.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4652_SOURCE_REGISTER.csv"
ORIGIN_VERDICT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4652_AMF_PALATINI_ORIGIN_VERDICT.csv"
EFFECTIVE_DEMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4652_EFFECTIVE_GR_DEMOTION_GATE.csv"
TRIAD_CSV = SOURCE_DIR / "P8_Y5_R2FR_4652_LEAKAGE_ROOT_TRIAD_ATTACK_MAP.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4652_RUNNER_RESULTS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4652_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4652_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4652_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4652_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4652_VALIDATION.csv"

DOC_4651 = POST / "4651-Y5-R2FR-parent-action-BGR-signature-line-or-first-residual-attack.md"
CSV_4651_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4651_VALIDATION.csv"
FORMAL_578 = FORMAL / "578-PPC4161-A-MF-parent-origin-from-motion-time-space-or-effective-axiom-freeze.md"
FORMAL_579 = FORMAL / "579-PPC4161-A-MF-axiom-pack-to-IR-scale-law-and-no-extra-mode-contract.md"
DOC_4540 = POST / "4540-Y5-R2FR-parent-scale-law-for-IR-EH-selector-or-explicit-EFT-residual-envelope.md"
DOC_4649 = POST / "4649-Y5-R2FR-parent-selector-promotion-map-or-local-GR-contract.md"


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


def table(rows: list[dict[str, Any]]) -> str:
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
        ("SRC4652_00_4651_validation", CSV_4651_VALIDATION, "VAL4651_OVERALL", "4651 B_GR action-line checkpoint passed."),
        ("SRC4652_01_4651_AMF_gap", DOC_4651, "GAP4651_0_A_MF_origin", "A_MF is first adoption gap."),
        ("SRC4652_02_4651_EEH_decomp", DOC_4651, "EEH4651_2_new_decomposition", "E_EH decomposition from 4651."),
        ("SRC4652_03_4562_freeze", FORMAL_578, "frozen as an explicit equivalence-principle-like axiom candidate", "A_MF origin freeze."),
        ("SRC4652_04_4562_fail", FORMAL_578, "FAIL_PARENT_ORIGIN", "A_MF parent origin fails current corpus."),
        ("SRC4652_05_4562_next", FORMAL_578, "Do not spend another checkpoint rediscovering that A_MF is unsigned.", "do not reopen A_MF origin loop."),
        ("SRC4652_06_4563_A_MF_explicit", FORMAL_579, "PG4563_0_A_MF_pack", "A_MF is explicit, not smuggled."),
        ("SRC4652_07_4563_IR_conditional", FORMAL_579, "PG4563_1_IR_normal_form", "IR selector passes conditionally."),
        ("SRC4652_08_4563_scale_fail", FORMAL_579, "PG4563_2_parent_scale_gap", "parent scale gap unsigned."),
        ("SRC4652_09_4563_no_extra_fail", FORMAL_579, "PG4563_3_no_extra_modes", "no-extra-mode residuals open."),
        ("SRC4652_10_4563_first", FORMAL_579, "RT4563_0_first", "c_D first attack."),
        ("SRC4652_11_4540_EFT_master", DOC_4540, "EFT4540_0_master", "explicit EFT residual envelope."),
        ("SRC4652_12_4540_cD", DOC_4540, "EFT4540_1_cD", "c_D same-coframe failure root."),
        ("SRC4652_13_4540_deltaKappa", DOC_4540, "EFT4540_2_deltaKappa", "source-coupling drift root."),
        ("SRC4652_14_4540_cGamma", DOC_4540, "EFT4540_3_cGamma", "MTS memory hair root."),
        ("SRC4652_15_4649_contract", DOC_4649, "GRSEL4649_0_action_form", "B_GR local promotion contract."),
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


def origin_verdict_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("ORIG4652_0_A_MF_parent_origin", "A_MF parent origin from motion/time/space primitives", "FAIL_PARENT_ORIGIN_CURRENT_CORPUS", "import 4562 freeze; do not present as theorem"),
        ("ORIG4652_1_A_MF_private_use", "A_MF as explicit equivalence-principle-like axiom candidate", "PRIVATE_CONDITIONAL_USE_ALLOWED", "may support private B_GR calculations if labelled"),
        ("ORIG4652_2_Palatini_IR_selector", "A_MF + locality + two-derivative/one-curvature + no-extra-mode -> EC/Palatini/EH", "PASS_CONDITIONAL_ONLY", "selector depends on unsigned scale/no-extra clauses"),
        ("ORIG4652_3_parent_scale_gap", "parent mass/length hierarchy and two-derivative dominance", "FAIL_UNSIGNED_PARENT_SCALE_GAP", "must derive scale law or keep EFT residuals"),
        ("ORIG4652_4_no_extra_modes", "all non-EH carriers zero/heavy/projection-silent/bounded", "FAIL_RESIDUALS_OPEN", "triage c_D, delta_kappa, c_Gamma first"),
        ("ORIG4652_5_B_GR_status", "S_local[B_GR] after 4651", "EFFECTIVE_LOCAL_GR_BRANCH_NOT_PARENT_DERIVED", "use as private correspondence branch, not final MTS->GR theorem"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "origin_id": row[0],
            "object": row[1],
            "verdict": row[2],
            "action": row[3],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def demotion_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("DEM4652_0_allowed", "effective/private B_GR branch", "Use S_local[B_GR] as a controlled local GR comparator and derivation scaffold.", "allowed only with explicit nonclaim label"),
        ("DEM4652_1_forbidden", "parent-derived local GR claim", "Do not claim MTS derives GR/Newton publicly while A_MF origin, scale gap and no-extra modes are unsigned.", "blocked"),
        ("DEM4652_2_science_value", "why keep it", "The effective branch still fixes source coupling, Maxwell/Poynting ownership and exact residual names, making tests sharper.", "useful private theory work"),
        ("DEM4652_3_exit_to_derivation", "promotion exit", "Promote only if A_MF is parent-derived or replaced by a deeper quotient/coarse-graining theorem and residual triad closes.", "future theorem"),
        ("DEM4652_4_exit_to_bounds", "testable fallback", "If derivation stalls, score c_D, delta_kappa and c_Gamma residuals in WEP/clock/EM/PPN/orbital/R10 arenas.", "empirical robustness path"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "demotion_id": row[0],
            "branch": row[1],
            "statement": row[2],
            "status": row[3],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def triad_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("TRI4652_0_cD", 1, "c_D", "same-coframe / second-metric / shadow frame failure", "WEP, clocks, EM propagation, Poynting/Hilbert stress, preferred-frame PPN", "derive same-coframe parent functor from A_MF action descent or build WEP/clock/EM bound interface", NEXT_TARGET),
        ("TRI4652_1_deltaKappa", 2, "delta_kappa", "source-coupling or kappa/source-measure drift", "Gdot/G, orbital GM, calibrated G consistency, WEP/source normalization", "derive Hilbert-source normalization/kappa lock or calibrated-G residual row", "4654-Y5-R2FR-deltaKappa-source-coupling-lock-or-Gdot-orbital-bound.md"),
        ("TRI4652_2_cGamma", 3, "c_Gamma", "local memory/support/projector hair", "PPN, clocks, R10, local-G variation", "derive local memory support/projector silence or source profile coefficients", "4655-Y5-R2FR-cGamma-memory-support-projector-silence-or-profile-bound.md"),
        ("TRI4652_3_cR2_secondary", 4, "c_R2/M_R", "curvature-square finite-range pole", "R10, orbital precession, cosmology consistency", "parent scale gap/no-extra-mode or full finite-range bound", ""),
        ("TRI4652_4_cT_cBdy_secondary", 5, "c_T,c_bdy", "torsion/contact and boundary/projector leakage", "preferred-frame, spin/contact, boundary/orbital residuals", "torsion algebraic/heavy proof and boundary routing", ""),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "triad_id": row[0],
            "priority": row[1],
            "coefficient": row[2],
            "meaning": row[3],
            "arenas": row[4],
            "next_action": row[5],
            "next_target": row[6],
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in rows
    ]


def runner_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("RUN4652_0_current_state", "A_MF frozen; IR selector conditional; scale/no-extra gaps unsigned", "EFFECTIVE_BGR_BRANCH_ONLY", "no parent-derived local GR claim"),
        ("RUN4652_1_parent_derivation", "A_MF parent origin plus scale gap and no-extra-mode theorem derived", "PASS_FUTURE_PARENT_DERIVED_ROUTE", "would re-open public MTS->GR proof route"),
        ("RUN4652_2_private_effective", "use B_GR with explicit A_MF axiom label", "PASS_PRIVATE_EFFECTIVE_COMPARATOR", "allowed for disciplined derivations/testing"),
        ("RUN4652_3_no_extra_fail", "extra local coefficients remain finite", "FAIL_TO_TRIAD_BOUNDS", "attack c_D, delta_kappa, c_Gamma before c_R2/R10"),
        ("RUN4652_4_reopen_AMF_loop", "repeat A_MF origin search without new parent variables", "REJECT_CIRCULAR_WORK", "4562 already froze A_MF; move to c_D"),
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
        ("CTRL4652_0_no_axiom_laundering", "A_MF is explicit axiom candidate, not derived theorem."),
        ("CTRL4652_1_no_reopen_loop", "Do not rediscover A_MF is unsigned unless new parent variables/action are supplied."),
        ("CTRL4652_2_no_public_GR", "B_GR remains effective/private until parent scale gap and no-extra-mode gates close."),
        ("CTRL4652_3_no_R10_first", "Do not jump to R10 alpha before c_D/delta_kappa/cGamma projections are owned."),
        ("CTRL4652_4_no_hidden_G", "Numerical G remains calibrated; delta_kappa tracks source-coupling drift."),
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
            "decision_id": "DEC4652_0",
            "decision": "AMF_ORIGIN_FREEZE_IMPORTED_BGR_DEMOTED_TO_EFFECTIVE_PRIVATE_BRANCH_TRIAD_ATTACK_SELECTED",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "summary": "4652 imports the stronger existing 4562/4563 verdict: A_MF is explicitly frozen as an equivalence-principle-like axiom candidate, the Palatini/EC normal form is conditional, and the parent scale/no-extra-mode theorem is still unsigned. Therefore S_local[B_GR] is a controlled effective/private local-GR branch, not a parent-derived MTS->GR theorem. The next non-circular work is the leakage-root triad, starting with c_D same-coframe ownership.",
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": BRANCH,
            "status": "PRIVATE_DEMOTION_AND_TRIAGE_NONCLAIM",
            "summary": "B_GR action line retained as private effective local-GR scaffold; A_MF origin freeze imported; c_D/delta_kappa/cGamma triage selected.",
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
            "reason": "c_D is the first leakage root because same-coframe failure would break WEP, clocks, EM stress and PPN before cGamma/R10 details matter",
            "success_condition": "prove a same-coframe parent functor/no-shadow-metric theorem or produce source-backed WEP/clock/EM/PPN bounds for finite c_D",
            "timestamp_utc": timestamp,
        }
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    origins: list[dict[str, Any]],
    demotions: list[dict[str, Any]],
    triads: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    public_clean, public_detail = git_clean(PUBLIC_STAGE)
    backup_clean, backup_detail = git_clean(BACKUP_REPO)
    checks = [
        ("VAL4652_00_sources_exist", all(row["path_exists"] for row in sources), "all cited paths exist"),
        ("VAL4652_01_needles_found", all(row["needle_found"] for row in sources), "all source needles found"),
        ("VAL4652_02_line_anchors", all(int(row["line_number"]) > 0 for row in sources), "all source line anchors positive"),
        ("VAL4652_03_AMF_freeze_imported", any(row["origin_id"] == "ORIG4652_0_A_MF_parent_origin" and "FAIL_PARENT_ORIGIN" in row["verdict"] for row in origins), "A_MF freeze/fail imported"),
        ("VAL4652_04_private_use_allowed", any(row["origin_id"] == "ORIG4652_1_A_MF_private_use" for row in origins), "private conditional use recorded"),
        ("VAL4652_05_effective_demotion", any(row["demotion_id"] == "DEM4652_1_forbidden" for row in demotions), "public parent-derived GR claim blocked"),
        ("VAL4652_06_triad_order", triads and triads[0]["coefficient"] == "c_D" and triads[0]["next_target"] == NEXT_TARGET, "c_D selected first"),
        ("VAL4652_07_no_reopen_loop", any(row["run_id"] == "RUN4652_4_reopen_AMF_loop" and row["result"] == "REJECT_CIRCULAR_WORK" for row in runners), "A_MF loop rejected"),
        ("VAL4652_08_current_effective_only", any(row["run_id"] == "RUN4652_0_current_state" and row["result"] == "EFFECTIVE_BGR_BRANCH_ONLY" for row in runners), "current state demoted correctly"),
        ("VAL4652_09_no_claim_allowed", all(str(row.get("valid_for_claim", "False")) == "False" for row in sources + origins + demotions + triads + runners + decisions), "no row marked claim-grade"),
        ("VAL4652_10_decision_next", decisions and decisions[0]["next_target"] == NEXT_TARGET, "next target selected"),
        ("VAL4652_11_public_stage_clean", public_clean, f"public stage: {public_detail}"),
        ("VAL4652_12_backup_repo_clean", backup_clean, f"backup repo: {backup_detail}"),
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
            "validation_id": "VAL4652_OVERALL",
            "status": "PASS" if all(passed for _, passed, _ in checks) else "FAIL",
            "detail": "4652 validation passed" if all(passed for _, passed, _ in checks) else "4652 validation failed",
            "timestamp_utc": timestamp,
        }
    )
    return rows


def build_doc(
    sources: list[dict[str, Any]],
    origins: list[dict[str, Any]],
    demotions: list[dict[str, Any]],
    triads: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> str:
    return f"""# 4652 - A_MF / Palatini IR selector origin or EH effective demotion

Branch: `{BRANCH}`
Marker: `{MARKER}`

## Result

4652 imports the old work instead of re-circling it.

The current corpus already decided the `A_MF` origin question honestly: `A_MF` is an explicit equivalence-principle-like axiom candidate, not a parent-derived theorem. Under that explicit axiom, the Palatini/EC normal form is useful and conditional; but the parent scale gap and no-extra-mode theorem remain unsigned.

Therefore:

`S_local[B_GR] = effective/private local-GR scaffold, not public parent-derived MTS -> GR theorem`.

This is not a retreat. It selects the real next attack:

`c_D -> delta_kappa -> c_Gamma`,

starting with `c_D`, because if the same coframe/common readout fails, WEP, clocks, EM/Poynting stress and PPN fail before any elegant EH action matters.

## Source Register

{table(sources)}

## Origin Verdict

{table(origins)}

## Effective-GR Demotion Gate

{table(demotions)}

## Leakage-Root Triad Attack Map

{table(triads)}

## Runner Results

{table(runners)}

## Controls

{table(controls)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next Target

{table(nexts)}

## Validation

{table(validations)}
"""


def register_claim() -> None:
    if CLAIM_ID in read_text(CLAIMS_PATH):
        return
    row = [
        CLAIM_ID,
        "local_gr_empirical_interface",
        "4652 imports the A_MF origin freeze and demotes S_local[B_GR] to an explicit private/effective local-GR scaffold until A_MF, parent scale gap and no-extra-mode gates are derived; it selects c_D, delta_kappa and c_Gamma as the leakage-root triad, starting with c_D.",
        "Generated source register, origin verdict, effective-GR demotion gate, leakage-root triad attack map, runner, controls, decision, status, next target and validation.",
        "AMF_freeze_BGR_effective_demotion_cD_first_nonclaim",
        NEXT_TARGET,
        "Reopening the A_MF origin loop without new parent variables, laundering an axiom into a theorem, claiming public MTS-derived GR from B_GR, or jumping to R10 before same-coframe/source-coupling roots.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "No public local-GR/Newton/PPN/Maxwell/EM claim until A_MF/scale/no-extra-mode origins are parent-derived or c_D/delta_kappa/cGamma residuals are source-backed and pass.",
    ]
    append_once(CLAIMS_PATH, CLAIM_ID, csv_line(row))


def update_spine_packet() -> None:
    spine = f"""
## {MARKER}

Claim `{CLAIM_ID}`: 4652 imports the established A_MF verdict. `A_MF` remains an explicit equivalence-principle-like axiom candidate rather than a parent-derived theorem; the Palatini/EC normal form is conditional; and the parent scale gap/no-extra-mode theorem remains unsigned. Therefore `S_local[B_GR]` is retained as a private/effective local-GR scaffold, not a public MTS-derived GR theorem. The next non-circular route is the leakage-root triad `c_D`, `delta_kappa`, `c_Gamma`, starting with `c_D` same-coframe/common-readout ownership.
"""
    packet = f"""
## {PACKET_MARKER}

Checkpoint `4652` stops the A_MF loop and selects the first leakage-root attack: `c_D` same-coframe ownership. Next packet target: `{NEXT_TARGET}`.
"""
    append_once(SPINE_PATH, MARKER, spine)
    append_once(PACKET_PATH, PACKET_MARKER, packet)


def main() -> int:
    timestamp = now()
    sources = source_rows(timestamp)
    origins = origin_verdict_rows(timestamp)
    demotions = demotion_rows(timestamp)
    triads = triad_rows(timestamp)
    runners = runner_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    validations = validation_rows(sources, origins, demotions, triads, runners, decisions, timestamp)

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ORIGIN_VERDICT_CSV, origins)
    write_csv(EFFECTIVE_DEMOTION_CSV, demotions)
    write_csv(TRIAD_CSV, triads)
    write_csv(RUNNER_CSV, runners)
    write_csv(CONTROL_CSV, controls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_csv(VALIDATION_CSV, validations)

    doc = build_doc(sources, origins, demotions, triads, runners, controls, decisions, statuses, nexts, validations)
    DOC_PATH.write_text(doc, encoding="utf-8")
    FORMAL_PATH.write_text(doc, encoding="utf-8")
    register_claim()
    update_spine_packet()

    overall = validations[-1]["status"]
    print(f"4652 validation: {overall}")
    print(VALIDATION_CSV)
    return 0 if overall == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
