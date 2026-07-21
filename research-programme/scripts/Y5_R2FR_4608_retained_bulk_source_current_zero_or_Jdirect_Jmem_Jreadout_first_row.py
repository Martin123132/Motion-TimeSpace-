from __future__ import annotations

import csv
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4608"
CLAIM_ID = "L-450"
BRANCH_ID = "MTS_R2FR_Y5_RETAINED_BULK_SOURCE_CURRENT_GATE_4608"
MARKER = "PPC4161_RETAINED_BULK_SOURCE_CURRENT_ZERO_OR_JDIRECT_JMEM_JREADOUT_FIRST_ROW_4608"
PACKET_MARKER = "PPC4161_PACKET_RETAINED_BULK_SOURCE_CURRENT_GATE_4608"
DECISION = "RETAINED_BULK_SOURCE_CURRENT_ZERO_OR_COMPONENT_ROWS_READY_NONCLAIM"
NEXT_TARGET = "4609-Y5-R2FR-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md"

DOC_PATH = POST / "4608-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md"
FORMAL_PATH = FORMAL / "624-PPC4161-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4608_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4608_RETAINED_BULK_SOURCE_CURRENT_THEOREM.csv"
JDIRECT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4608_JDIRECT_ROWS.csv"
JMEM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4608_JMEM_ROWS.csv"
JMARKER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4608_JMARKER_ROWS.csv"
JREADOUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4608_JREADOUT_ROWS.csv"
QBULK_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4608_QBULK_RETAINED_UPDATE_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4608_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4608_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4608_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4608_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4608_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4608_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4608_VALIDATION.csv"

DOC_4607 = POST / "4607-Y5-R2FR-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md"
FORMAL_623 = FORMAL / "623-PPC4161-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md"
CSV_4607_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4607_NEXT_TARGET.csv"
CSV_4607_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4607_CLAIM_BLOCKERS.csv"
CSV_4606_RETAINED = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_RETAINED_ROWS.csv"
CSV_4514_TAIL = SOURCE_DIR / "P8_Y5_R2FR_4514_REMAINING_SOURCE_TAIL_LEDGER.csv"
CSV_2642_SCI = SOURCE_DIR / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_PROOF_ATTEMPT.csv"
CSV_4520_RZSC = SOURCE_DIR / "P8_Y5_R2FR_4520_RANK_ZERO_SOURCE_CURRENT_SILENCE_THEOREM.csv"
CSV_4596_JMEM = SOURCE_DIR / "P8_Y5_R2FR_4596_JMEM_JH_REDUCED_RESIDUAL_VECTOR.csv"
CSV_4596_INS = SOURCE_DIR / "P8_Y5_R2FR_4596_SOURCE_KERNEL_TO_JMEM_INSERTION.csv"
CSV_4599_LHRS = SOURCE_DIR / "P8_Y5_R2FR_4599_LABEL_HODGE_SUPPORT_READOUT_ZERO_THEOREM.csv"
CSV_4599_NORM = SOURCE_DIR / "P8_Y5_R2FR_4599_CX_LABEL_HODGE_SUPPORT_READOUT_NORM.csv"
CSV_2624_READOUT = SOURCE_DIR / "P8_Y5_READOUT_SCHEMA_GATE_2624_READOUT_SCHEMA_THEOREM_ATTEMPT.csv"
CSV_2523_JREADOUT = SOURCE_DIR / "P8_Y5_NO_SHADOW_2523_JREADOUT_BOUND_ROWS.csv"
CSV_2508_GATES = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_NO_SOURCE_SLOT_THEOREM_GATES.csv"
CSV_2508_COUNTER = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_SOURCE_ONLY_COUNTERMODELS.csv"
CSV_2508_RESID = SOURCE_DIR / "P8_Y5_NO_SHADOW_2508_SOURCE_WEIGHT_RESIDUAL_ROWS.csv"
CSV_1850_MARKER = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1850_NO_MARKER_THEOREM_ATTEMPT.csv"
CSV_1850_SURVIVE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_1850_SURVIVING_MARKER_FAMILY_AUDIT.csv"

PUBLIC_STAGE = Path("D:/Users/ollet/Desktop/Motion-TimeSpace-public-stage")
BACKUP_REPO = Path("D:/Users/ollet/Desktop/laptop-back-up-")


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def line_of(path: Path, needle: str) -> int:
    if not path.exists() or not needle:
        return 0
    for number, line in enumerate(read_text(path).splitlines(), start=1):
        if needle in line:
            return number
    return 0


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
        lines.append("| " + " | ".join(str(row.get(header, "")).replace("\n", "<br>") for header in headers) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    suffix = "\n" if text.endswith("\n") or not text else "\n\n"
    write_text(path, text + suffix + block.strip() + "\n")


def git_clean(path: Path) -> bool:
    if not path.exists() or not (path / ".git").exists():
        return True
    result = subprocess.run(["git", "-C", str(path), "status", "--porcelain"], text=True, capture_output=True, check=False)
    return result.returncode == 0 and result.stdout.strip() == ""


def append_claim_once() -> None:
    rows = read_csv(CLAIMS_PATH)
    if any(row.get("claim_id") == CLAIM_ID for row in rows):
        return
    fieldnames = [
        "claim_id", "domain", "claim", "current_evidence", "status", "next_test", "key_risk",
        "sector", "evidence", "next_action", "risk",
    ]
    rows.append({
        "claim_id": CLAIM_ID,
        "domain": "local_gr_empirical_interface",
        "claim": "4608 decomposes the retained bulk source-current numerator into direct, memory, marker and readout tails; exact zero requires all four to vanish in the same parent branch, otherwise Q_bulk_retained uses a no-cancellation component envelope.",
        "current_evidence": "Generated retained source-current theorem rows, J_direct/J_mem/J_marker/J_readout component rows, Q_bulk retained update rows, blockers, controls and validation.",
        "status": "retained_bulk_source_current_zero_or_component_rows_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Calling the retained current zero because Hilbert/EM/Poynting are controlled, while non-Hilbert source weights, memory exchange, markers or readout/projector re-entry still survive.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No R10, PPN, clock, orbital or local-GR claim until retained, edge/shadow, denominator/projector, qbar_XT and arena kernels are exact zero or source-backed numeric rows.",
    })
    existing = list(rows[0].keys()) if rows else fieldnames
    for name in fieldnames:
        if name not in existing:
            existing.append(name)
    with CLAIMS_PATH.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=existing)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in existing})


def source_rows(now: str) -> list[dict[str, Any]]:
    sources = [
        ("SRC4608_00_4607_handoff", CSV_4607_NEXT, "4608-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md", "4607 names retained bulk source current as the next live numerator."),
        ("SRC4608_01_4607_downstream", CSV_4607_BLOCKERS, "MIS4607_3_downstream", "4607 keeps downstream retained/edge/shadow gates open."),
        ("SRC4608_02_4606_retained_total", CSV_4606_RETAINED, "R4606_TOTAL", "4606 installed the retained bulk no-cancellation template."),
        ("SRC4608_03_4606_direct", CSV_4606_RETAINED, "R4606_0_direct", "4606 leaves J_direct_abs as missing."),
        ("SRC4608_04_4606_memory", CSV_4606_RETAINED, "R4606_1_memory", "4606 leaves J_mem_abs as missing."),
        ("SRC4608_05_4606_readout", CSV_4606_RETAINED, "R4606_2_readout", "4606 leaves J_readout_abs as missing."),
        ("SRC4608_06_4514_Jmem", CSV_4514_TAIL, "STL4514_3_Jmem", "4514 identifies J_mem direct/source current as a live tail."),
        ("SRC4608_07_2642_readout", CSV_2642_SCI, "SCI2642_4_readout", "2642 gives the readout zero condition and missing-value residual."),
        ("SRC4608_08_2642_JNH", CSV_2642_SCI, "SCI2642_2_JNH_channels", "2642 keeps non-Hilbert source channels live."),
        ("SRC4608_09_4520_retained", CSV_4520_RZSC, "RZSC4520_4_retained", "4520 proves the retained/non-Hilbert exception split."),
        ("SRC4608_10_4520_rhs", CSV_4520_RZSC, "RZSC4520_5_rhs_reduction", "4520 reduces the rank-zero RHS after Hilbert silence."),
        ("SRC4608_11_4596_jmem_live", CSV_4596_JMEM, "J4596_5_live_total", "4596 provides the reduced live J vector."),
        ("SRC4608_12_4596_insert", CSV_4596_INS, "INS4596_1_memory", "4596 inserts the source-kernel result into J_mem."),
        ("SRC4608_13_4599_readout_zero", CSV_4599_LHRS, "LHRS4599_3_readout", "4599 gives the postprocessing readout zero route."),
        ("SRC4608_14_4599_norm", CSV_4599_NORM, "N4599_4_total", "4599 keeps label/Hodge/support/readout norm values missing."),
        ("SRC4608_15_2624_readout_schema", CSV_2624_READOUT, "RAV2624_5_current_verdict", "2624 separates parent variation from readout but not parent-signs it."),
        ("SRC4608_16_2523_jreadout", CSV_2523_JREADOUT, "JRO2523_0_total", "2523 provides the J_readout component envelope."),
        ("SRC4608_17_2508_no_source_slot", CSV_2508_GATES, "GATE2508_6_theorem", "2508 leaves the no-source-only-slot theorem blocked."),
        ("SRC4608_18_2508_countermodel", CSV_2508_COUNTER, "CM2508_4_readout_projector", "2508 shows readout/projector source re-entry countermodel."),
        ("SRC4608_19_2508_residuals", CSV_2508_RESID, "RSW2508_5", "2508 source-weight residual rows include hidden marker/source tails."),
        ("SRC4608_20_1850_marker_attempt", CSV_1850_MARKER, "NMT1850_6_verdict", "1850 no-marker theorem remains open."),
        ("SRC4608_21_1850_survivors", CSV_1850_SURVIVE, "SMF1850_5_source_boundary_tail", "1850 keeps source-boundary tails as live marker families."),
        ("SRC4608_22_formal_623", FORMAL_623, "PPC4161_EM_POYNTING_HODGE_FLUX_ZERO_OR_WALL_FLUX_COEFFICIENT_ROW_4607", "formal handoff from 4607."),
    ]
    rows = []
    for source_id, path, needle, role in sources:
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "source_path": str(path),
            "source_line": line_of(path, needle),
            "needle": needle,
            "path_exists": path.exists(),
            "needle_found": line_of(path, needle) > 0,
            "role": role,
            "generated_utc": now,
            "valid_for_claim": False,
        })
    return rows


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RET4608_0_decomposition",
            "component": "retained bulk source current",
            "derived_relation": "J_retained := J_direct+J_mem+J_marker+J_readout",
            "zero_condition": "J_direct=J_mem=J_marker=J_readout=0 in the same parent branch",
            "fallback_bound": "|Q_bulk_retained| <= W_lambda_max(|J_direct_abs|+|J_mem_abs|+|J_marker_abs|+|J_readout_abs|)",
            "current_status": "DERIVED_DECOMPOSITION_NO_CANCELLATION",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RET4608_1_direct",
            "component": "J_direct",
            "derived_relation": "J_direct=0 follows if the parent object language has no non-Hilbert direct source slot, no source-only weights, one action-scale owner and no hidden marker return.",
            "zero_condition": "GATE2508_0 through GATE2508_6 pass plus SCI2642_2 non-Hilbert channels vanish",
            "fallback_bound": "|J_direct| <= |J_nonHilbert|+|epsilon_wA_source_weight|+|epsilon_kappaA_source|+|epsilon_action_scale|+|epsilon_noHom|+|epsilon_hidden_marker|",
            "current_status": "CONDITIONAL_ZERO_COUNTERMODELS_RETAINED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RET4608_2_memory",
            "component": "J_mem",
            "derived_relation": "J_mem_live = J_mem^EM_open+J_mem^nonHilbert+J_mem^dyn_exchange+J_mem^boundary_readout after source-kernel silence.",
            "zero_condition": "strict source-kernel branch, EM/Poynting no-flux, no retained non-Hilbert current, stationary exchange closure and boundary/readout neutrality",
            "fallback_bound": "|J_mem| <= |J_mem^EM_open|+|J_mem^nonHilbert|+|J_mem^dyn_exchange|+|J_mem^boundary_readout|",
            "current_status": "REDUCED_MEMORY_VECTOR_NOT_CLOSED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RET4608_3_marker",
            "component": "J_marker",
            "derived_relation": "J_marker=0 only if fixed spurions, material constants, common/disformal frames, alpha/clock constants and source-boundary tails are quotient-owned or absent.",
            "zero_condition": "NMT1850 no-marker theorem plus no source-boundary tail and no hidden marker Hom",
            "fallback_bound": "|J_marker| <= |epsilon_hidden_marker|+|b_A|+|b_alpha|+|c_g|+|b_dis|+|q_source_boundary_tail|",
            "current_status": "MARKER_ZERO_NOT_CLOSED_COMPONENT_ROWS_READY",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RET4608_4_readout",
            "component": "J_readout",
            "derived_relation": "J_readout=0 if readout is pure post-solution reporting, absent from S_parent and forbidden to re-enter through reduced EFT, projector, worldtube, material or calibration maps.",
            "zero_condition": "variation-before-readout plus parent-domain exclusion of readout/projector/source-worldtube re-entry",
            "fallback_bound": "J_readout <= J_PiM_comm+J_Ploc_comm+J_worldtube_comm+J_material_comm+J_coframe_DObs+J_EFT_pre+J_calibration+J_boundary_endpoint",
            "current_status": "CONDITIONAL_POSTPROCESSING_ZERO_PARENT_DOMAIN_UNSIGNED",
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": "RET4608_5_bulk_update",
            "component": "Q_bulk retained insertion",
            "derived_relation": "Q_bulk_abs <= Q_bulk_Hilbert_abs+Q_bulk_EM/Poynting_abs+Q_bulk_retained_abs with Q_bulk_retained_abs sourced by the four retained tails.",
            "zero_condition": "ordinary Hilbert, EM/Poynting and all retained tails vanish in the same parent branch",
            "fallback_bound": "|Q_bulk_retained| <= W_lambda_max(|J_direct_abs|+|J_mem_abs|+|J_marker_abs|+|J_readout_abs|)",
            "current_status": "BULK_RETAINED_UPDATE_READY_NONCLAIM",
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def jdirect_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JD4608_0_total",
            "quantity": "J_direct_abs",
            "zero_route": "no direct retained source slot, no source-only species weight, one action-scale owner, no hidden marker/source coefficient Hom",
            "bound_formula": "|J_direct| <= |J_nonHilbert|+|epsilon_wA_source_weight|+|epsilon_kappaA_source|+|epsilon_action_scale|+|epsilon_noHom|+|epsilon_hidden_marker|",
            "source_anchor": "GATE2508_6_theorem;RSW2508_0..5;SCI2642_2_JNH_channels",
            "current_status": "DIRECT_ZERO_NOT_PARENT_SIGNED_COMPONENT_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JD4608_1_nonHilbert",
            "quantity": "J_nonHilbert_abs",
            "zero_route": "metric/coframe-only LC branch with no hypermomentum/torsion/nonmetricity/projective source and no improvement/shadow/projector leakage",
            "bound_formula": "|J_nonHilbert| <= E_spin+E_boundary+E_readout+E_shadow+E_projector",
            "source_anchor": "SCI2642_2_JNH_channels",
            "current_status": "NONHILBERT_COMPONENT_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JD4608_2_source_weights",
            "quantity": "epsilon_wA_source_weight+epsilon_kappaA_source+epsilon_action_scale+epsilon_noHom",
            "zero_route": "no source-only slot, connected source category and single action-scale/current owner",
            "bound_formula": "direct source-weight contribution <= absolute sum of RSW2508 source-weight residuals",
            "source_anchor": "RSW2508_0;RSW2508_1;RSW2508_2;RSW2508_3",
            "current_status": "SOURCE_WEIGHT_ROWS_SYMBOLIC_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JD4608_3_hidden_marker",
            "quantity": "epsilon_hidden_marker",
            "zero_route": "no hidden/domain/boundary/material marker targets active source coefficient slots",
            "bound_formula": "hidden marker direct contribution <= |epsilon_hidden_marker|",
            "source_anchor": "RSW2508_5;CM2508_3_hidden_marker",
            "current_status": "HIDDEN_MARKER_VALUE_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def jmem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JM4608_0_total",
            "quantity": "J_mem_abs",
            "zero_route": "source-kernel silence plus EM no-flux plus no retained non-Hilbert current plus stationary exchange plus boundary/readout neutrality",
            "bound_formula": "|J_mem| <= |J_mem^EM_open|+|J_mem^nonHilbert|+|J_mem^dyn_exchange|+|J_mem^boundary_readout|",
            "source_anchor": "INS4596_1_memory;J4596_5_live_total;STL4514_3_Jmem",
            "current_status": "JMEM_REDUCED_VECTOR_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JM4608_1_EM_open",
            "quantity": "J_mem^EM_open",
            "zero_route": "same-Hodge Maxwell branch and stationary no-wall-flux collar",
            "bound_formula": "|J_mem^EM_open| <= source-coupling operator norm times |Phi_wall_Poynting|/|M_H_ref|",
            "source_anchor": "J4596_1_EM_open;4607 EM/Poynting gate",
            "current_status": "EM_OPEN_INHERITS_4607_FLUX_BLOCKER",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JM4608_2_nonHilbert",
            "quantity": "J_mem^nonHilbert",
            "zero_route": "no retained non-Hilbert memory source current",
            "bound_formula": "|J_mem^nonHilbert| <= ||J_X^nonHilbert|| memory projection",
            "source_anchor": "J4596_2_nonHilbert",
            "current_status": "NONHILBERT_MEMORY_VALUE_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JM4608_3_dynamic_boundary_readout",
            "quantity": "J_mem^dyn_exchange+J_mem^boundary_readout",
            "zero_route": "stationary exchange closure and boundary/readout neutral source reference",
            "bound_formula": "|J_mem^dyn_exchange|+|J_mem^boundary_readout| <= ||exchange/clock/source current||+||boundary/readout source reference shift||",
            "source_anchor": "J4596_3_dynamic_exchange;J4596_4_boundary_readout",
            "current_status": "DYNAMIC_BOUNDARY_READOUT_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def jmarker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JMK4608_0_total",
            "quantity": "J_marker_abs",
            "zero_route": "full no-marker theorem: ordinary matter, constants, material labels, frames and source-boundary tails are quotient-owned or absent",
            "bound_formula": "|J_marker| <= |epsilon_hidden_marker|+|b_A|+|b_alpha|+|c_g|+|b_dis|+|q_source_boundary_tail|",
            "source_anchor": "NMT1850_6_verdict;SMF1850_1..5",
            "current_status": "NO_MARKER_THEOREM_NOT_CLOSED_COMPONENT_ROWS_READY",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JMK4608_1_material_constants",
            "quantity": "b_A+b_alpha",
            "zero_route": "material constants, masses, alpha_EM and clock transition constants are quotient-owned/superselected",
            "bound_formula": "material/constant marker contribution <= |b_A|+|b_alpha|",
            "source_anchor": "SMF1850_3_material_constants;SMF1850_4_alpha_clock_constants",
            "current_status": "MATERIAL_CONSTANT_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JMK4608_2_frame_markers",
            "quantity": "c_g+b_dis",
            "zero_route": "common Weyl/conformal and disformal matter frames are absent or theorem-zero",
            "bound_formula": "frame marker contribution <= |c_g|+|b_dis|",
            "source_anchor": "SMF1850_1_common_frame;SMF1850_2_disformal_frame",
            "current_status": "FRAME_MARKER_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JMK4608_3_source_boundary_tail",
            "quantity": "q_source_boundary_tail",
            "zero_route": "no source-only weights, domain classes, support shifts, boundary/non-Hilbert current",
            "bound_formula": "source-boundary marker contribution <= |q_source_boundary_tail|",
            "source_anchor": "SMF1850_5_source_boundary_tail;NMT1850_5_source_weight_and_boundary",
            "current_status": "SOURCE_BOUNDARY_TAIL_VALUE_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def jreadout_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JR4608_0_total",
            "quantity": "J_readout_abs",
            "zero_route": "variation-before-readout; readout is post-solution only, excluded from S_parent, and cannot re-enter through projector/source-worldtube/material/EFT/calibration/boundary maps",
            "bound_formula": "J_readout <= J_PiM_comm+J_Ploc_comm+J_worldtube_comm+J_material_comm+J_coframe_DObs+J_EFT_pre+J_calibration+J_boundary_endpoint",
            "source_anchor": "JRO2523_0_total;RAV2624_5_current_verdict;LHRS4599_3_readout",
            "current_status": "READOUT_ZERO_NOT_PARENT_SIGNED_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JR4608_1_projectors",
            "quantity": "J_PiM_comm+J_Ploc_comm",
            "zero_route": "Pi_M and P_loc fixed before source variation and commute with retained direction",
            "bound_formula": "projector readout contribution <= J_PiM_comm+J_Ploc_comm",
            "source_anchor": "JRO2523_1_PiM_comm;JRO2523_2_Ploc_comm",
            "current_status": "PROJECTOR_COMMUTATOR_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JR4608_2_worldtube_material",
            "quantity": "J_worldtube_comm+J_material_comm",
            "zero_route": "source worldtube/support and material/composition readout are fixed quotient-owned maps",
            "bound_formula": "worldtube/material contribution <= J_worldtube_comm+J_material_comm",
            "source_anchor": "JRO2523_3_worldtube_comm;JRO2523_4_material_comm",
            "current_status": "WORLDTUBE_MATERIAL_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JR4608_3_coframe_eft_calibration_boundary",
            "quantity": "J_coframe_DObs+J_EFT_pre+J_calibration+J_boundary_endpoint",
            "zero_route": "observed coframe, EFT reduction, calibration and boundary endpoints do not feed the parent source variation",
            "bound_formula": "remaining readout contribution <= J_coframe_DObs+J_EFT_pre+J_calibration+J_boundary_endpoint",
            "source_anchor": "JRO2523_5_coframe_DObs;JRO2523_6_EFT_pre;JRO2523_7_calibration;JRO2523_8_boundary_endpoint",
            "current_status": "READOUT_REENTRY_TAIL_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def qbulk_update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QBR4608_0_retained",
            "quantity": "Q_bulk_retained_abs",
            "update_formula": "|Q_bulk_retained| <= W_lambda_max(|J_direct_abs|+|J_mem_abs|+|J_marker_abs|+|J_readout_abs|)",
            "zero_condition": "all retained component rows vanish in the same parent branch",
            "required_inputs": "J_direct_abs;J_mem_abs;J_marker_abs;J_readout_abs;W_lambda_max",
            "current_status": "ABSOLUTE_SUM_SCHEMA_READY_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QBR4608_1_bulk_total",
            "quantity": "Q_bulk_abs",
            "update_formula": "|Q_bulk| <= |Q_bulk_Hilbert|+|Q_bulk_EM/Poynting|+|Q_bulk_retained|",
            "zero_condition": "Hilbert, EM/Poynting and retained bulk tails vanish in the same branch",
            "required_inputs": "4606 Hilbert rows;4607 EM/Poynting rows;4608 retained rows",
            "current_status": "QBULK_TOTAL_STILL_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QBR4608_2_QbarXH",
            "quantity": "Qbar_XH_abs",
            "update_formula": "|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower",
            "zero_condition": "bulk retained plus edge/shadow plus denominator/projector commute and vanish",
            "required_inputs": "Q_bulk_abs;Q_edge_abs;Q_shadow_abs;Pi_M norm;E_PiM_comm;M_lower",
            "current_status": "QBARXH_STILL_BLOCKED_BY_EDGE_SHADOW_AND_DENOMINATOR",
            "claim_allowed": False,
            "valid_for_claim": False,
            "generated_utc": now,
        },
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4608_0_same_branch", "control": "Do not combine a J_direct zero from one branch with a J_mem/readout zero from another branch.", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4608_1_no_cancellation", "control": "Use absolute component sums; no direct/memory/marker/readout cancellation is allowed.", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4608_2_poynting_not_hidden", "control": "Poynting stays in the 4607 EM gate unless a retained nonminimal/flux current is explicitly sourced here.", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4608_3_readout_order", "control": "Variation-before-readout must be parent-domain signed; a reduced-action readout branch is a retained residual, not a theorem-zero.", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4608_4_no_claim_from_symbolic_rows", "control": "Symbolic component rows are a scaffold only and cannot score R10/PPN/clock/orbit tests.", "valid_for_claim": False, "generated_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4608_0_direct", "missing_object": "parent-signed no direct retained source/non-Hilbert/source-weight slot or finite J_direct_abs", "why_it_matters": "direct retained source weight would change local source normalization", "best_next_action": "prove no-source-only object language or source component coefficients", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4608_1_memory", "missing_object": "same-branch J_mem zero or finite J_mem live-vector components", "why_it_matters": "memory source current feeds Q_bulk_retained and A_mem", "best_next_action": "close EM/nonHilbert/dynamic/boundary-readout memory components", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4608_2_marker", "missing_object": "full no-marker theorem or finite material/frame/constant/source-boundary marker values", "why_it_matters": "markers can preserve WEP-looking behavior while shifting R10/PPN/clock normalization", "best_next_action": "source b_A, b_alpha, c_g, b_dis and source-boundary tails or prove quotient ownership", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4608_3_readout", "missing_object": "parent-domain readout exclusion or finite projector/worldtube/material/EFT/calibration/boundary readout coefficients", "why_it_matters": "readout/projector re-entry can recreate a source current after variation", "best_next_action": "turn readout schema into parent-domain certificate or source J_readout components", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4608_4_downstream", "missing_object": "Q_edge, Q_shadow, denominator/projector, qbar_XT and arena kernels", "why_it_matters": "retained bulk closure alone is not a local-GR/R10/PPN claim", "best_next_action": NEXT_TARGET, "valid_for_claim": False, "generated_utc": now},
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4608_0_sources", "promotion_requirement": "all source rows exist and cited needles are found", "current_status": "PASS" if all(row["path_exists"] and row["needle_found"] for row in sources) else "FAIL", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4608_1_zero", "promotion_requirement": "J_direct=J_mem=J_marker=J_readout=0 parent-signed in the same branch", "current_status": "NOT_SATISFIED", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4608_2_numeric", "promotion_requirement": "if zero fails, all four retained component rows have numeric source-backed nonnegative values and units", "current_status": "NOT_SATISFIED_SYMBOLIC_ROWS_ONLY", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4608_3_empirical", "promotion_requirement": "Q_bulk_retained row joins Q_edge/Q_shadow/denominator/qbar_XT/arena kernels before scoring", "current_status": "NOT_SATISFIED_DOWNSTREAM_OPEN", "valid_for_claim": False, "generated_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "decision": DECISION,
        "reason": "The retained bulk source-current fog is now split into four named tails with exact-zero clauses and nonclaim fallback envelopes; none is yet parent-signed or numeric.",
        "valid_for_claim": False,
        "generated_utc": now,
    }]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "status": DECISION,
        "what_moved": "Q_bulk_retained is no longer a single placeholder; it is a direct+memory+marker+readout absolute-sum gate.",
        "what_did_not_move": "No local-GR/R10/PPN/clock/orbit pass; all component values remain symbolic or conditional.",
        "valid_for_claim": False,
        "generated_utc": now,
    }]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "branch": BRANCH_ID,
        "generated_utc": now,
        "next_target": NEXT_TARGET,
        "reason": "After the bulk retained numerator is split, the next source-side numerator term is Q_edge: the source-worldtube/boundary shell flux gate.",
        "derive_first": "prove fixed source worldtube, compact collar, no birth/death shell and zero source-boundary flux in the same branch",
        "fallback": "fill Qedge shell/worldtube/corner flux rows as nonclaim finite inputs",
        "valid_for_claim": False,
    }]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4608 - Retained Bulk Source-Current Zero Or `J_direct/J_mem/J_readout` First Row

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register row: `{CLAIM_ID}`

## Decision

`{DECISION}`

This checkpoint does the leap that 4607 handed off: after ordinary Hilbert matter and Maxwell/Poynting bookkeeping have been separated, the remaining bulk source current is not a misty word called "retained". It is split into four named tails:

```text
J_retained := J_direct + J_mem + J_marker + J_readout.
```

The local source numerator now uses the no-cancellation envelope:

```text
|Q_bulk_retained| <= W_lambda_max(|J_direct_abs|+|J_mem_abs|+|J_marker_abs|+|J_readout_abs|).
```

## Result

- `J_direct` is killed only by a parent-signed no-source-only/no-nonHilbert/no-hidden-marker object language.
- `J_mem` is reduced to the live vector `EM_open + nonHilbert + dynamic_exchange + boundary_readout`.
- `J_marker` is the honest bucket for material constants, frame markers, alpha/clock constants and source-boundary tails.
- `J_readout` is zero only for true post-solution readout with no projector/worldtube/material/EFT/calibration/boundary re-entry.

No component is currently promoted to a claim row; each has a source-ready fallback row.

## Source Register

{markdown_table(tables["sources"])}

## Retained Theorem Rows

{markdown_table(tables["theorem"])}

## `J_direct` Rows

{markdown_table(tables["jdirect"])}

## `J_mem` Rows

{markdown_table(tables["jmem"])}

## `J_marker` Rows

{markdown_table(tables["jmarker"])}

## `J_readout` Rows

{markdown_table(tables["jreadout"])}

## `Q_bulk` Update Rows

{markdown_table(tables["qbulk_update"])}

## Controls

{markdown_table(tables["controls"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Next Target

`{NEXT_TARGET}`

The best next step is the edge/source-worldtube boundary gate. Bulk retained is now no longer unnamed; edge is the next numerator term blocking `Qbar_XH`.

Private nonclaim. No R10, PPN, clock, orbital, Newton or local-GR pass is claimed.
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 Formal Addendum 624 - Retained Bulk Source-Current Gate

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

## Local Source-Current Split

The retained bulk source-current term is defined by

```text
J_retained := J_direct+J_mem+J_marker+J_readout.
```

Therefore the bulk retained numerator obeys the non-cancelling envelope

```text
|Q_bulk_retained| <= W_lambda_max(|J_direct_abs|+|J_mem_abs|+|J_marker_abs|+|J_readout_abs|).
```

The exact-zero route is the conjunction

```text
J_direct=0, J_mem=0, J_marker=0, J_readout=0
```

in the same parent branch. The clauses are:

1. no direct retained source/non-Hilbert/source-weight slot;
2. memory source-kernel silence plus no EM-open/nonHilbert/dynamic/boundary-readout memory current;
3. no material/frame/constant/source-boundary marker re-entry;
4. post-solution readout only, with no projector/worldtube/material/EFT/calibration/boundary re-entry.

## Status

This is progress, but not a claim. The checkpoint converts the retained bulk tail into four auditable source rows. It does not prove local GR, R10, PPN, clocks or orbital silence.

Next target: `{NEXT_TARGET}`.
"""


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({
            "checkpoint": CHECKPOINT,
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "claim_allowed": False,
        })

    add("VAL4608_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    missing_needles = [row["source_id"] for row in tables["sources"] if not row["needle_found"]]
    add("VAL4608_01_needles_found", not missing_needles, "missing needles: " + ",".join(missing_needles) if missing_needles else "all cited source needles found")
    csv_paths = [
        SOURCE_REGISTER, THEOREM_CSV, JDIRECT_CSV, JMEM_CSV, JMARKER_CSV, JREADOUT_CSV,
        QBULK_UPDATE_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV,
    ]
    details = []
    csv_ok = True
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4608_02_csv_parse", csv_ok, ";".join(details))
    theorem_text = "\n".join(str(row) for row in tables["theorem"])
    direct_text = "\n".join(str(row) for row in tables["jdirect"])
    memory_text = "\n".join(str(row) for row in tables["jmem"])
    marker_text = "\n".join(str(row) for row in tables["jmarker"])
    readout_text = "\n".join(str(row) for row in tables["jreadout"])
    update_text = "\n".join(str(row) for row in tables["qbulk_update"])
    add("VAL4608_03_decomposition", "J_retained := J_direct+J_mem+J_marker+J_readout" in theorem_text, "retained decomposition present")
    add("VAL4608_04_direct_rows", "epsilon_kappaA_source" in direct_text and "DIRECT_ZERO_NOT_PARENT_SIGNED" in direct_text, "direct source rows present")
    add("VAL4608_05_memory_rows", "J_mem^EM_open" in memory_text and "J_mem^boundary_readout" in memory_text, "memory live-vector rows present")
    add("VAL4608_06_marker_rows", "SMF1850_5_source_boundary_tail" in marker_text and "c_g+b_dis" in marker_text, "marker rows present")
    add("VAL4608_07_readout_rows", "J_PiM_comm" in readout_text and "variation-before-readout" in readout_text, "readout component rows present")
    add("VAL4608_08_qbulk_update", "Q_bulk_retained" in update_text and "Qbar_XH" in update_text, "bulk/Qbar update present")
    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "empirical_pass_claimed", "score_ready", "numeric_value_present", "claim_pass"} and value is True:
                    all_false = False
    add("VAL4608_09_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4608_10_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4608_11_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4608_12_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4608_13_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4608_14_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4608_15_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4608_16_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4608_17_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4608_OVERALL", all(row["status"] == "PASS" for row in rows), "4608 retained bulk source-current gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "jdirect": jdirect_rows(now),
        "jmem": jmem_rows(now),
        "jmarker": jmarker_rows(now),
        "jreadout": jreadout_rows(now),
        "qbulk_update": qbulk_update_rows(now),
        "controls": control_rows(now),
        "blockers": blocker_rows(now),
        "promotion": [],
        "decision": decision_rows(now),
        "status": status_rows(now),
        "next": next_rows(now),
    }
    tables["promotion"] = promotion_rows(now, tables["sources"])
    write_csv(SOURCE_REGISTER, tables["sources"])
    write_csv(THEOREM_CSV, tables["theorem"])
    write_csv(JDIRECT_CSV, tables["jdirect"])
    write_csv(JMEM_CSV, tables["jmem"])
    write_csv(JMARKER_CSV, tables["jmarker"])
    write_csv(JREADOUT_CSV, tables["jreadout"])
    write_csv(QBULK_UPDATE_CSV, tables["qbulk_update"])
    write_csv(CONTROL_CSV, tables["controls"])
    write_csv(BLOCKERS_CSV, tables["blockers"])
    write_csv(PROMOTION_CSV, tables["promotion"])
    write_csv(DECISION_CSV, tables["decision"])
    write_csv(STATUS_CSV, tables["status"])
    write_csv(NEXT_CSV, tables["next"])
    write_text(DOC_PATH, build_doc(now, tables))
    write_text(FORMAL_PATH, build_formal(now))
    append_claim_once()
    append_once(
        SPINE_PATH,
        MARKER,
        f"""
## PPC4161 Local Addendum - Retained Bulk Source-Current Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The retained bulk source-current numerator is now split as `J_retained := J_direct+J_mem+J_marker+J_readout`. This turns the previous fog bank into a no-cancellation four-tail gate feeding `Q_bulk_retained_abs`, while keeping every row nonclaim until same-branch zeros or source-backed numeric values exist.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Retained Bulk Source-Current Gate

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now treats direct source slots, memory source current, marker return and readout/projector re-entry as distinct retained bulk tails. The next numerator target is edge/source-worldtube boundary flux.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4608 validation failed: {failed}")
    print(f"4608 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
