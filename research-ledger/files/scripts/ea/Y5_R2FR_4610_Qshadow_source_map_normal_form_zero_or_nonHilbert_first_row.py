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

CHECKPOINT = "4610"
CLAIM_ID = "L-452"
BRANCH_ID = "MTS_R2FR_Y5_QSHADOW_SOURCE_MAP_NORMAL_FORM_GATE_4610"
MARKER = "PPC4161_QSHADOW_SOURCE_MAP_NORMAL_FORM_ZERO_OR_NONHILBERT_FIRST_ROW_4610"
PACKET_MARKER = "PPC4161_PACKET_QSHADOW_SOURCE_MAP_NORMAL_FORM_GATE_4610"
DECISION = "QSHADOW_SOURCE_MAP_NORMAL_FORM_ZERO_OR_NONHILBERT_ROWS_READY_NONCLAIM"
NEXT_TARGET = "4611-Y5-R2FR-QbarXH-full-source-envelope-rollup-or-first-source-backed-input.md"

DOC_PATH = POST / "4610-Y5-R2FR-Qshadow-source-map-normal-form-zero-or-nonHilbert-first-row.md"
FORMAL_PATH = FORMAL / "626-PPC4161-Qshadow-source-map-normal-form-zero-or-nonHilbert-first-row.md"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4610_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_NORMAL_FORM_THEOREM.csv"
ACTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_ACTION_ROWS.csv"
PROJECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_PROJECTOR_ROWS.csv"
NONVAR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_NONVARIATIONAL_ROWS.csv"
UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_QBARXH_UPDATE_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4610_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4610_CLAIM_BLOCKERS.csv"
PROMOTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4610_PROMOTION_GATES.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4610_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4610_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4610_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4610_VALIDATION.csv"

FORMAL_625 = FORMAL / "625-PPC4161-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md"
CSV_4609_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4609_NEXT_TARGET.csv"
CSV_4609_UPDATE = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_QBARXH_UPDATE_ROWS.csv"
CSV_4605_QSHADOW = SOURCE_DIR / "P8_Y5_R2FR_4605_QSHADOW_COMPONENT_ROWS.csv"
CSV_4605_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4605_SOURCE_NUMERATOR_THEOREM.csv"
CSV_2617_IDENTITY = SOURCE_DIR / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SINGLE_SOURCE_MAP_IDENTITY_THEOREM.csv"
CSV_2617_ZERO = SOURCE_DIR / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_SOURCE_SHADOW_ZERO_ATTEMPT.csv"
CSV_2617_AUDIT = SOURCE_DIR / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_NONHILBERT_BOUNDARY_PROJECTOR_AUDIT.csv"
CSV_2617_COUNTER = SOURCE_DIR / "P8_Y5_SINGLE_SOURCE_MAP_GATE_2617_COUNTERMODEL_LEDGER.csv"
CSV_2618_ANF = SOURCE_DIR / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_PARENT_ACTION_NORMAL_FORM_SIGNATURE.csv"
CSV_2618_CLASS = SOURCE_DIR / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_SHADOW_TERM_CLASSIFICATION_LEDGER.csv"
CSV_2618_SMG = SOURCE_DIR / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_SOURCE_MAP_IDENTITY_GATE.csv"
CSV_2618_PACK = SOURCE_DIR / "P8_Y5_PARENT_ACTION_NORMAL_FORM_GATE_2618_SHADOW_COEFFICIENT_PACK.csv"
CSV_3085_STATUS = SOURCE_DIR / "P8_Y5_R2FR_3085_SOURCE_MAP_NORMAL_FORM_STATUS.csv"
CSV_3085_BAN = SOURCE_DIR / "P8_Y5_R2FR_3085_SOURCE_SHADOW_BAN_ATTEMPT.csv"
CSV_3347_PROJECTOR = SOURCE_DIR / "P8_Y5_R2FR_3347_SOURCE_SHADOW_PROJECTOR_NORMAL_FORM.csv"
CSV_3347_BOUNDS = SOURCE_DIR / "P8_Y5_R2FR_3347_EPSILON_SOURCE_SHADOW_BOUND_ROWS.csv"
CSV_4431_SHADOW = SOURCE_DIR / "P8_Y5_R2FR_4431_SOURCE_SHADOW_OUTPUT.csv"
CSV_4431_NH = SOURCE_DIR / "P8_Y5_R2FR_4431_NONHILBERT_BYPASS_OUTPUT.csv"
CSV_4432_SPLIT = SOURCE_DIR / "P8_Y5_R2FR_4432_SHADOW_SPLIT_OUTPUT.csv"
CSV_4432_VALUE = SOURCE_DIR / "P8_Y5_R2FR_4432_KMSHADOW_VALUE_OUTPUT.csv"
CSV_3564_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_3564_NONHILBERT_BYPASS_THEOREM.csv"
CSV_3564_FALLBACK = SOURCE_DIR / "P8_Y5_R2FR_3564_OFFICIAL_NONHILBERT_FALLBACK_ROWS.csv"
CSV_4100_NH = SOURCE_DIR / "P8_Y5_R2FR_4100_NONHILBERT_BYPASS_THEOREM.csv"
CSV_4600_BNH = SOURCE_DIR / "P8_Y5_R2FR_4600_BOUNDARY_NONHILBERT_ZERO_THEOREM.csv"
CSV_3625_BIANCHI = SOURCE_DIR / "P8_Y5_R2FR_3625_BIANCHI_NOETHER_DERIVATION.csv"
CSV_4113_BIANCHI = SOURCE_DIR / "P8_Y5_R2FR_4113_BIANCHI_CLOSURE_LAW.csv"
CSV_4271_CORE = SOURCE_DIR / "P8_Y5_R2FR_4271_CORE_SHADOW_ACTION_DOMAIN_THEOREM.csv"
CSV_3647_NOSHADOW = SOURCE_DIR / "P8_Y5_R2FR_3647_NO_SHADOW_THEOREM_ATTEMPT.csv"
CSV_3647_COUNTER = SOURCE_DIR / "P8_Y5_R2FR_3647_SHADOW_FRAME_COUNTERMODEL_AUDIT.csv"
CSV_2642_BOUND = SOURCE_DIR / "P8_Y5_SOURCE_CURRENT_IDENTITY_2642_COMPONENT_BOUND_PACK.csv"

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
        "claim": "4610 decomposes the Q_shadow source numerator into action-normal-form, source-map/projector and nonvariational/conserved-block channels; exact zero requires every apparent shadow to be parent-action content, boundary/improvement-silent, identity/common-mode only, or absent in one branch.",
        "current_evidence": "Generated Q_shadow normal-form theorem rows, action/projector/nonvariational rows, Qbar_XH update rows, blockers, controls and validation.",
        "status": "Qshadow_source_map_normal_form_zero_or_nonHilbert_rows_nonclaim",
        "next_test": NEXT_TARGET,
        "key_risk": "Using Bianchi/Ward consistency or measured G to erase a source shadow while post-variation projectors, nonminimal action terms, hidden frame returns or separately conserved blocks survive.",
        "sector": "local_gr",
        "evidence": str(DOC_PATH),
        "next_action": NEXT_TARGET,
        "risk": "No R10, PPN, clock, orbital or local-GR claim until the full Qbar_XH source envelope, denominator/projector, qbar_XT and arena kernels are exact zero or source-backed numeric rows.",
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
        ("SRC4610_00_4609_handoff", CSV_4609_NEXT, "4610-Y5-R2FR-Qshadow-source-map-normal-form-zero-or-nonHilbert-first-row.md", "4609 hands off to Q_shadow."),
        ("SRC4610_01_4609_qbar", CSV_4609_UPDATE, "QEU4609_1_QbarXH", "4609 keeps Q_shadow open in Qbar_XH."),
        ("SRC4610_02_4605_action", CSV_4605_QSHADOW, "QS4605_0_action_shadow", "4605 Q_shadow action component."),
        ("SRC4610_03_4605_projector", CSV_4605_QSHADOW, "QS4605_1_projector_shadow", "4605 Q_shadow projector component."),
        ("SRC4610_04_4605_nonvar", CSV_4605_QSHADOW, "QS4605_2_nonvariational_shadow", "4605 Q_shadow nonvariational component."),
        ("SRC4610_05_4605_total", CSV_4605_QSHADOW, "QS4605_TOTAL", "4605 Q_shadow total envelope."),
        ("SRC4610_06_4605_theorem", CSV_4605_THEOREM, "NUM4605_3_shadow_zero", "4605 conditional shadow zero theorem."),
        ("SRC4610_07_2617_trichotomy", CSV_2617_IDENTITY, "SMI2617_2_shadow_trichotomy", "2617 source-shadow trichotomy."),
        ("SRC4610_08_2617_verdict", CSV_2617_IDENTITY, "SMI2617_5_current_verdict", "2617 source-shadow zero verdict."),
        ("SRC4610_09_2617_action", CSV_2617_ZERO, "SSZ2617_1_shadow_as_action_term", "2617 action-term reclassification."),
        ("SRC4610_10_2617_nonvar", CSV_2617_ZERO, "SSZ2617_2_shadow_as_nonvariational", "2617 nonvariational rejection/bound."),
        ("SRC4610_11_2617_projector", CSV_2617_ZERO, "SSZ2617_3_shadow_as_projector", "2617 post-variation projector route."),
        ("SRC4610_12_2617_audit", CSV_2617_AUDIT, "NHB2617_5_verdict", "2617 non-Hilbert/source-shadow inventory."),
        ("SRC4610_13_2617_counter", CSV_2617_COUNTER, "CM2617_4_verdict", "2617 countermodel verdict."),
        ("SRC4610_14_2618_anf", CSV_2618_ANF, "ANF2618_6_current_verdict", "2618 parent action normal-form signature verdict."),
        ("SRC4610_15_2618_class", CSV_2618_CLASS, "SCL2618_7_verdict", "2618 shadow classification ledger verdict."),
        ("SRC4610_16_2618_source_map", CSV_2618_SMG, "SMG2618_4_current_verdict", "2618 source-map identity verdict."),
        ("SRC4610_17_2618_coeff", CSV_2618_PACK, "SCP2618_4_R_total_residual", "2618 shadow coefficient pack total row."),
        ("SRC4610_18_3085_status", CSV_3085_STATUS, "SMNF3085_2_shadow_residuals", "3085 shadow residual normal form status."),
        ("SRC4610_19_3085_ban", CSV_3085_BAN, "SSB3085_3_current_verdict", "3085 source-shadow ban verdict."),
        ("SRC4610_20_3347_projector", CSV_3347_PROJECTOR, "SSF3347_1_projector_decomposition", "3347 source projector decomposition."),
        ("SRC4610_21_3347_epsilon", CSV_3347_BOUNDS, "BND3347_0_MICROSCOPE_TiPt_unit_response", "3347 first epsilon_source_shadow bound row."),
        ("SRC4610_22_4431_shadow", CSV_4431_SHADOW, "SH4431_3_source_shadow_current_verdict", "4431 source-shadow current verdict."),
        ("SRC4610_23_4431_nh", CSV_4431_NH, "NH4431_3_official_fallback_status", "4431 non-Hilbert fallback verdict."),
        ("SRC4610_24_4432_split", CSV_4432_SPLIT, "SPLIT4432_3_readout_projector_shadow", "4432 shadow split output."),
        ("SRC4610_25_4432_value", CSV_4432_VALUE, "KM4432_4_original_Kmshadow_bound_target", "4432 K_m shadow bound target."),
        ("SRC4610_26_3564_theorem", CSV_3564_THEOREM, "NHB3564_4_official_fallback", "3564 official non-Hilbert fallback."),
        ("SRC4610_27_3564_fallback", CSV_3564_FALLBACK, "FNH3564_5_shadow_projector", "3564 shadow/projector fallback row."),
        ("SRC4610_28_4100_nonhilbert", CSV_4100_NH, "NHB4100_2_total_zero_conditions", "4100 non-Hilbert total zero condition."),
        ("SRC4610_29_4600_shadow", CSV_4600_BNH, "BNH4600_2_shadow_split", "4600 shadow split roll-forward."),
        ("SRC4610_30_3625_bianchi", CSV_3625_BIANCHI, "BND3625_5_necessary_not_sufficient", "Bianchi closure no-smuggling guard."),
        ("SRC4610_31_4113_bianchi", CSV_4113_BIANCHI, "BLC4113_3_not_sufficient", "4113 closure is not local-GR silence."),
        ("SRC4610_32_4271_core", CSV_4271_CORE, "CST4271_5_current_verdict", "4271 core shadow frame verdict."),
        ("SRC4610_33_3647_noshadow", CSV_3647_NOSHADOW, "NSF3647_6_verdict", "3647 no-shadow frame verdict."),
        ("SRC4610_34_3647_counter", CSV_3647_COUNTER, "CM3647_6_field_rename", "3647 field-rename countermodel."),
        ("SRC4610_35_2642_bound", CSV_2642_BOUND, "SCB2642_2_eps_JNH_abs", "2642 non-Hilbert source residual component."),
        ("SRC4610_36_formal_625", FORMAL_625, "PPC4161_QEDGE_SOURCE_WORLDTUBE_BOUNDARY_ZERO_OR_SHELL_FLUX_FIRST_ROW_4609", "formal handoff from 4609."),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in sources:
        source_line = line_of(path, needle)
        rows.append({
            "checkpoint": CHECKPOINT,
            "source_id": source_id,
            "source_path": str(path),
            "source_line": source_line,
            "needle": needle,
            "path_exists": path.exists(),
            "needle_found": source_line > 0,
            "role": role,
            "generated_utc": now,
            "valid_for_claim": False,
        })
    return rows


def theorem_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "theorem_id": "QSH4610_0_decomposition", "component": "Q_shadow", "derived_relation": "Q_shadow := Q_shadow_action + Q_shadow_projector + Q_shadow_nonvariational", "zero_condition": "all three shadow channels vanish or are reclassified out of the RHS source in the same parent branch", "fallback_bound": "|Q_shadow|_abs <= |Q_shadow_action|+|Q_shadow_projector|+|Q_shadow_nonvariational|", "current_status": "DERIVED_SHADOW_SPLIT_NO_CANCELLATION", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "theorem_id": "QSH4610_1_action_normal_form", "component": "Q_shadow_action", "derived_relation": "Any variational shadow is delta DeltaS_shadow/delta e_obs and is therefore real parent action content, LHS geometry, modified matter, boundary/improvement or forbidden.", "zero_condition": "complete parent action inventory classifies every DeltaS candidate with no unowned source RHS term", "fallback_bound": "|Q_shadow_action| <= |delta DeltaS_shadow/delta X| + |c_nonminimal| + |c_boundary| + |c_frame_shadow|", "current_status": "ACTION_NORMAL_FORM_CONTRACT_READY_PARENT_UNSIGNED", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "theorem_id": "QSH4610_2_projector_identity", "component": "Q_shadow_projector", "derived_relation": "A post-Hilbert source map decomposes as P_src=I+C0 I+Pi_rel; C0 is a universal calibration mode, Pi_rel is the dangerous source-shadow projector.", "zero_condition": "field equation is Euler-Lagrange from one action and no post-variation source projector/readout map is admitted", "fallback_bound": "|Q_shadow_projector| <= |C0_common_unowned| ||T_H|| + epsilon_source_shadow ||T_H|| + |E_projector_source| + |E_readout_return|", "current_status": "PROJECTOR_NORMAL_FORM_DERIVED_VALUES_MISSING", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "theorem_id": "QSH4610_3_nonvariational_filter", "component": "Q_shadow_nonvariational", "derived_relation": "A nonvariational shadow either violates Bianchi/Noether consistency, is a separately conserved real block, or must be bounded as a repair term.", "zero_condition": "no decoupled conserved block, no nonvariational insertion, and no inconsistency repair in tested arenas", "fallback_bound": "|Q_shadow_nonvariational| <= |E_decoupled| + |Q_conserved_extra| + |Q_inconsistency_repair|", "current_status": "BIANCHI_FILTER_DERIVED_NOT_ZERO_PROOF", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "theorem_id": "QSH4610_4_nonHilbert_basis", "component": "non-Hilbert shadow support", "derived_relation": "J_NH includes spin/torsion, boundary/worldtube, readout, improvement, shadow/projector and decoupled blocks; Q_shadow uses only the unclaimed source-map/projector/nonvariational pieces after bulk and edge are separated.", "zero_condition": "P_source[J_NH]=0 componentwise with no readout/projector/boundary double counting", "fallback_bound": "epsilon_current_owner_NH_abs supplies the official no-cancellation non-Hilbert envelope", "current_status": "NONHILBERT_BASIS_REUSED_WITH_QEDGE_FIREWALL", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "theorem_id": "QSH4610_5_Qbar_update", "component": "Qbar_XH source numerator", "derived_relation": "Q_tot_XH=Q_bulk_XH+Q_edge_XH+Q_shadow_XH with every term now split into named nonclaim rows.", "zero_condition": "bulk, edge and shadow vanish or are source-backed, with denominator/projector and qbar_XT gates closed", "fallback_bound": "|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower", "current_status": "SOURCE_NUMERATOR_STRUCTURALLY_SPLIT_READY_FOR_ROLLUP", "valid_for_claim": False, "generated_utc": now},
    ]


def action_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "row_id": "QSA4610_0_total", "quantity": "Q_shadow_action_abs", "zero_route": "all variational shadows are parent-action content already counted as geometry/matter, boundary/improvement-silent, or forbidden", "bound_formula": "|Q_shadow_action| <= |delta DeltaS_shadow/delta X|+|c_nonminimal|+|c_boundary|+|c_frame_shadow|", "source_anchor": "SSZ2617_1_shadow_as_action_term;ANF2618_6_current_verdict;SCL2618_7_verdict", "current_status": "ACTION_CLASSIFICATION_MISSING_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QSA4610_1_nonminimal", "quantity": "c_nonminimal_action_abs", "zero_route": "nonminimal matter-geometry terms are absent, moved to LHS geometry, or explicit modified matter dynamics", "bound_formula": "|delta(c_nonminimal f(X,Phi,labels)L_m)/delta X|", "source_anchor": "SCL2618_2_nonminimal_coupling;SCP2618_1_c_nonminimal", "current_status": "NONMINIMAL_OPERATOR_BASIS_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QSA4610_2_boundary_improvement", "quantity": "c_boundary_action_abs", "zero_route": "boundary/improvement term is already Q_edge, exact improvement with zero compact flux, or boundary-silent", "bound_formula": "|c_boundary| plus unclassified improvement flux not already counted in Q_edge", "source_anchor": "SCL2618_3_boundary_improvement;BNH4600_0_boundary_variation", "current_status": "BOUNDARY_DOUBLE_COUNT_FIREWALL_ACTIVE_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QSA4610_3_frame_shadow", "quantity": "c_frame_shadow_abs", "zero_route": "ordinary matter has one q-owned observed frame and no independent conformal/disformal/source-frame slot", "bound_formula": "|c_g|+|b_dis|+||h_perp|| plus source-frame/readout-frame return terms", "source_anchor": "CST4271_5_current_verdict;NSF3647_6_verdict;CM3647_6_field_rename", "current_status": "NO_SHADOW_FRAME_NOT_PARENT_SIGNED", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
    ]


def projector_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "row_id": "QSP4610_0_total", "quantity": "Q_shadow_projector_abs", "zero_route": "identity-only Hilbert source map with no post-variation material/readout/source-worldtube projector", "bound_formula": "|Q_shadow_projector| <= |C0_common_unowned| ||T_H|| + epsilon_source_shadow ||T_H|| + |E_projector_source| + |E_readout_return|", "source_anchor": "SMI2617_1_identity_source_map;SSZ2617_3_shadow_as_projector;SMG2618_4_current_verdict", "current_status": "PROJECTOR_ZERO_UNSIGNED_COMPONENT_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QSP4610_1_common_mode", "quantity": "C0_common_unowned", "zero_route": "universal common source normalization is fixed before readout and absorbed only into measured G_N", "bound_formula": "G_N=G_*(1+C0) but local/range/species/time derivatives remain explicit", "source_anchor": "SSF3347_1_projector_decomposition;BND3347_1_common_mode_absorbed", "current_status": "COMMON_MODE_GUARD_READY_NOT_LOCAL_CLAIM", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QSP4610_2_relative_projector", "quantity": "epsilon_source_shadow", "zero_route": "Pi_rel=0 in P_src=I+C0 I+Pi_rel", "bound_formula": "epsilon_source_shadow := ||Pi_rel(T_H)||_arena/||T_H||_arena", "source_anchor": "SSF3347_2_epsilon_definition;BND3347_0_MICROSCOPE_TiPt_unit_response", "current_status": "ONE_WEP_SMOKE_BOUND_NOT_GENERAL_SOURCE_CLAIM", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QSP4610_3_readout_return", "quantity": "E_readout_return", "zero_route": "hidden readout/source-worldtube/material projector has no return path to active source coefficients", "bound_formula": "|E_readout_return| includes hidden return and readout_projector shadow subblocks", "source_anchor": "SPLIT4432_2_hidden_marker_shadow;SPLIT4432_3_readout_projector_shadow", "current_status": "HIDDEN_READOUT_RETURN_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
    ]


def nonvar_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "row_id": "QSN4610_0_total", "quantity": "Q_shadow_nonvariational_abs", "zero_route": "no post-Euler nonvariational source insertion and no separately conserved real block in tested arenas", "bound_formula": "|Q_shadow_nonvariational| <= |E_decoupled|+|Q_conserved_extra|+|Q_inconsistency_repair|", "source_anchor": "SSZ2617_2_shadow_as_nonvariational;SMI2617_3_bianchi_filter", "current_status": "NONVARIATIONAL_ZERO_UNSIGNED_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QSN4610_1_decoupled", "quantity": "E_decoupled", "zero_route": "separately conserved blocks are absent from ordinary local source arenas", "bound_formula": "E_decoupled source-backed arena envelope", "source_anchor": "FNH3564_6_decoupled;NHB2617_2_decoupled_conserved_block", "current_status": "ARENA_EXCLUSION_OR_BOUND_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QSN4610_2_inconsistency_repair", "quantity": "Q_inconsistency_repair", "zero_route": "Bianchi/Noether identity closes from one parent action with no repair source", "bound_formula": "repair residual required if nonvariational source violates closure", "source_anchor": "BND3625_5_necessary_not_sufficient;BLC4113_3_not_sufficient", "current_status": "BIANCHI_IS_FILTER_NOT_ZERO_VALUE", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QSN4610_3_nonHilbert_shadow_projector", "quantity": "E_shadow_projector", "zero_route": "non-Hilbert shadow/projector/support source tail is absent or projection-silent", "bound_formula": "E_shadow_projector official non-Hilbert fallback row", "source_anchor": "FNH3564_5_shadow_projector;NHB4100_2_total_zero_conditions", "current_status": "OFFICIAL_NONHILBERT_FALLBACK_RETAINED", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
    ]


def update_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "row_id": "QSU4610_0_shadow_total", "quantity": "Q_shadow_abs", "update_formula": "|Q_shadow|_abs <= |Q_shadow_action|+|Q_shadow_projector|+|Q_shadow_nonvariational|", "zero_condition": "action, projector and nonvariational shadow rows close in the same parent branch", "required_inputs": "Q_shadow_action_abs;Q_shadow_projector_abs;Q_shadow_nonvariational_abs", "current_status": "ABSOLUTE_SUM_SCHEMA_READY_VALUES_MISSING", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QSU4610_1_Qtot", "quantity": "Q_tot_XH_abs", "update_formula": "|Q_tot_XH| <= |Q_bulk|_abs + |Q_edge|_abs + |Q_shadow|_abs", "zero_condition": "bulk, edge and shadow source numerator pieces all close", "required_inputs": "Q_bulk_abs;Q_edge_abs;Q_shadow_abs", "current_status": "FULL_SOURCE_NUMERATOR_SPLIT_READY_NONCLAIM", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "row_id": "QSU4610_2_QbarXH", "quantity": "Qbar_XH_abs", "update_formula": "|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower", "zero_condition": "full numerator plus denominator/projector rows close", "required_inputs": "Q_tot_XH_abs;Pi_M norm;E_PiM_comm;M_lower", "current_status": "SOURCE_ENVELOPE_READY_FOR_4611_ROLLUP", "claim_allowed": False, "valid_for_claim": False, "generated_utc": now},
    ]


def control_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4610_0_bianchi_not_zero", "control": "Bianchi/Ward consistency filters shadow terms; it does not prove zero for conserved real blocks.", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4610_1_no_measured_G_hiding", "control": "Common-mode calibration may not hide relative, range, time, material or readout source shadows.", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4610_2_no_boundary_double_count", "control": "Boundary flux already counted in Q_edge must not also be counted as Q_shadow unless it is a separate action-normal-form residual.", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4610_3_no_cancellation", "control": "Use absolute sums between action, projector and nonvariational shadow pieces.", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "control_id": "CTRL4610_4_no_claim_from_symbolic_rows", "control": "Symbolic Q_shadow rows cannot score R10, PPN, clock, orbit or local-GR tests.", "valid_for_claim": False, "generated_utc": now},
    ]


def blocker_rows(now: str) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4610_0_action", "missing_object": "complete parent action normal-form inventory or finite Q_shadow_action_abs", "why_it_matters": "variational shadow action terms can be real source/operator content", "best_next_action": "classify every DeltaS candidate or source nonminimal/frame/boundary coefficients", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4610_1_projector", "missing_object": "identity-only source-map proof or finite projector/readout shadow coefficients", "why_it_matters": "post-variation source maps can fake composition/source dependence after clean Hilbert variation", "best_next_action": "prove P_src=I+C0I only or source Pi_rel/readout return rows", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4610_2_nonvariational", "missing_object": "absence/arena exclusion/bound for separately conserved and nonvariational source blocks", "why_it_matters": "Bianchi permits conserved real residuals; it only rejects inconsistent knobs", "best_next_action": "inventory decoupled blocks and source E_decoupled/Q_inconsistency rows", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "blocker_id": "MIS4610_3_rollup", "missing_object": "full Qbar_XH source envelope rollup with denominator/projector status", "why_it_matters": "bulk, edge and shadow are now split but not assembled into one source-side audit row", "best_next_action": NEXT_TARGET, "valid_for_claim": False, "generated_utc": now},
    ]


def promotion_rows(now: str, sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4610_0_sources", "promotion_requirement": "all cited sources exist and needles are found", "current_status": "PASS" if all(row["path_exists"] and row["needle_found"] for row in sources) else "FAIL", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4610_1_action_zero", "promotion_requirement": "all action-shadow candidates classified as LHS/matter/boundary-silent/forbidden or source-backed", "current_status": "NOT_SATISFIED", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4610_2_projector_zero", "promotion_requirement": "source map has no Pi_rel/readout return beyond fixed universal common mode", "current_status": "NOT_SATISFIED_SYMBOLIC_ROWS_ONLY", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4610_3_nonvar_zero", "promotion_requirement": "no separately conserved/nonvariational block survives tested arenas", "current_status": "NOT_SATISFIED_SYMBOLIC_ROWS_ONLY", "valid_for_claim": False, "generated_utc": now},
        {"checkpoint": CHECKPOINT, "gate_id": "PROM4610_4_empirical", "promotion_requirement": "Q_shadow row joins Q_bulk/Q_edge/denominator/qbar_XT/arena kernels before scoring", "current_status": "NOT_SATISFIED_DOWNSTREAM_OPEN", "valid_for_claim": False, "generated_utc": now},
    ]


def decision_rows(now: str) -> list[dict[str, Any]]:
    return [{"checkpoint": CHECKPOINT, "branch": BRANCH_ID, "decision": DECISION, "reason": "Q_shadow is now a normal-form gate with action, projector and nonvariational channels rather than an unnamed RHS loophole.", "valid_for_claim": False, "generated_utc": now}]


def status_rows(now: str) -> list[dict[str, Any]]:
    return [{"checkpoint": CHECKPOINT, "branch": BRANCH_ID, "status": DECISION, "what_moved": "The final source-numerator piece is split and inserted into Qbar_XH as an auditable absolute-sum row.", "what_did_not_move": "No empirical/local-GR claim; shadow coefficients and full Qbar_XH rollup remain nonclaim.", "valid_for_claim": False, "generated_utc": now}]


def next_rows(now: str) -> list[dict[str, Any]]:
    return [{"checkpoint": CHECKPOINT, "branch": BRANCH_ID, "generated_utc": now, "next_target": NEXT_TARGET, "reason": "Bulk, retained, edge and shadow have all been split; the next useful move is a single Qbar_XH source-envelope rollup showing what is zero, symbolic, or source-backed before moving to qbar_XT/arena testing.", "derive_first": "assemble Q_bulk_abs, Q_edge_abs and Q_shadow_abs into the full Qbar_XH source envelope with denominator/projector firewall", "fallback": "produce a nonclaim missing-input priority queue for first numeric/source-backed rows", "valid_for_claim": False}]


def build_doc(now: str, tables: dict[str, list[dict[str, Any]]]) -> str:
    return f"""# 4610 - `Q_shadow` Source-Map Normal Form Zero Or Non-Hilbert First Row

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register row: `{CLAIM_ID}`

## Decision

`{DECISION}`

This checkpoint goes after the last source-numerator fog bank. The shadow source term is split as:

```text
Q_shadow := Q_shadow_action + Q_shadow_projector + Q_shadow_nonvariational.
```

The exact zero route is not "Bianchi says no". The actual contract is:

```text
action shadows are parent-owned/reclassified,
post-Hilbert projectors reduce to identity plus fixed common mode,
and nonvariational blocks are absent, inconsistent, or source-bounded.
```

The fallback is:

```text
|Q_shadow|_abs <= |Q_shadow_action|+|Q_shadow_projector|+|Q_shadow_nonvariational|.
```

## Source Register

{markdown_table(tables["sources"])}

## `Q_shadow` Theorem Rows

{markdown_table(tables["theorem"])}

## Action-Normal-Form Rows

{markdown_table(tables["action"])}

## Projector/Source-Map Rows

{markdown_table(tables["projector"])}

## Nonvariational Rows

{markdown_table(tables["nonvar"])}

## `Qbar_XH` Update Rows

{markdown_table(tables["update"])}

## Controls

{markdown_table(tables["controls"])}

## Claim Blockers

{markdown_table(tables["blockers"])}

## Promotion Gates

{markdown_table(tables["promotion"])}

## Next Target

`{NEXT_TARGET}`

Bulk, retained, edge and shadow source numerator pieces are now split. The next step is a full `Qbar_XH` source-envelope rollup before pushing to `qbar_XT`/arena tests.

Private nonclaim. No R10, PPN, clock, orbital, Newton or local-GR pass is claimed.
"""


def build_formal(now: str) -> str:
    return f"""# PPC4161 Formal Addendum 626 - `Q_shadow` Source-Map Normal-Form Gate

Generated UTC: `{now}`

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

## Shadow Split

The source-shadow numerator is

```text
Q_shadow := Q_shadow_action + Q_shadow_projector + Q_shadow_nonvariational.
```

The non-cancelling envelope is

```text
|Q_shadow|_abs <= |Q_shadow_action|+|Q_shadow_projector|+|Q_shadow_nonvariational|.
```

Action shadows are legal only as explicit parent action content:

```text
J_shadow^action = delta DeltaS_shadow / delta e_obs.
```

Projector shadows are legal only as identity/common-mode plus residual:

```text
P_src = I + C0 I + Pi_rel.
```

Nonvariational shadows are filtered by Bianchi/Noether:

```text
nonvariational J_shadow -> inconsistent, separately conserved real block, or bounded repair term.
```

Thus the full source numerator now has named pieces:

```text
|Q_tot_XH| <= |Q_bulk|_abs + |Q_edge|_abs + |Q_shadow|_abs.
```

## Status

This is a source-map normal-form gate, not a claim. It prevents hidden RHS knobs from being smuggled in, but it does not yet provide numeric/source-backed coefficients.

Next target: `{NEXT_TARGET}`.
"""


def validate(tables: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append({"checkpoint": CHECKPOINT, "check_id": check_id, "status": "PASS" if passed else "FAIL", "detail": detail, "valid_for_claim": False, "claim_allowed": False})

    add("VAL4610_00_sources_exist", all(row["path_exists"] for row in tables["sources"]), "all cited source paths exist")
    missing_needles = [row["source_id"] for row in tables["sources"] if not row["needle_found"]]
    add("VAL4610_01_needles_found", not missing_needles, "missing needles: " + ",".join(missing_needles) if missing_needles else "all cited source needles found")
    csv_paths = [SOURCE_REGISTER, THEOREM_CSV, ACTION_CSV, PROJECTOR_CSV, NONVAR_CSV, UPDATE_CSV, CONTROL_CSV, BLOCKERS_CSV, PROMOTION_CSV, DECISION_CSV, STATUS_CSV, NEXT_CSV]
    details = []
    csv_ok = True
    for path in csv_paths:
        parsed = read_csv(path)
        details.append(f"{path.name}:{len(parsed)}")
        csv_ok = csv_ok and bool(parsed)
    add("VAL4610_02_csv_parse", csv_ok, ";".join(details))
    theorem_text = "\n".join(str(row) for row in tables["theorem"])
    action_text = "\n".join(str(row) for row in tables["action"])
    projector_text = "\n".join(str(row) for row in tables["projector"])
    nonvar_text = "\n".join(str(row) for row in tables["nonvar"])
    update_text = "\n".join(str(row) for row in tables["update"])
    add("VAL4610_03_shadow_split", "Q_shadow := Q_shadow_action + Q_shadow_projector + Q_shadow_nonvariational" in theorem_text, "shadow split present")
    add("VAL4610_04_action_rows", "c_nonminimal_action_abs" in action_text and "c_frame_shadow_abs" in action_text, "action-normal-form rows present")
    add("VAL4610_05_projector_rows", "epsilon_source_shadow" in projector_text and "E_readout_return" in projector_text, "projector/source-map rows present")
    add("VAL4610_06_nonvar_rows", "E_decoupled" in nonvar_text and "Q_inconsistency_repair" in nonvar_text, "nonvariational rows present")
    add("VAL4610_07_update_rows", "Q_shadow_abs" in update_text and "Q_tot_XH_abs" in update_text and "Qbar_XH_abs" in update_text, "Qshadow/Qbar update present")
    all_false = True
    for table in tables.values():
        for row in table:
            for key, value in row.items():
                if key in {"valid_for_claim", "claim_allowed", "empirical_pass_claimed", "score_ready", "numeric_value_present", "claim_pass"} and value is True:
                    all_false = False
    add("VAL4610_08_no_claim_true", all_false, "no generated table promotes a claim")
    add("VAL4610_09_doc_marker", MARKER in read_text(DOC_PATH), "checkpoint doc marker present")
    add("VAL4610_10_formal_marker", MARKER in read_text(FORMAL_PATH), "formal marker present")
    add("VAL4610_11_claim_register", CLAIM_ID in read_text(CLAIMS_PATH), "claim register row present")
    add("VAL4610_12_spine_marker", MARKER in read_text(SPINE_PATH), "spine marker present")
    add("VAL4610_13_packet_marker", PACKET_MARKER in read_text(PACKET_PATH), "packet marker present")
    add("VAL4610_14_next_target", NEXT_TARGET in read_text(NEXT_CSV), NEXT_TARGET)
    add("VAL4610_15_public_stage_clean", git_clean(PUBLIC_STAGE), str(PUBLIC_STAGE))
    add("VAL4610_16_backup_repo_clean", git_clean(BACKUP_REPO), str(BACKUP_REPO))
    add("VAL4610_OVERALL", all(row["status"] == "PASS" for row in rows), "4610 Qshadow source-map normal-form gate")
    return rows


def main() -> None:
    now = utc_now()
    tables = {
        "sources": source_rows(now),
        "theorem": theorem_rows(now),
        "action": action_rows(now),
        "projector": projector_rows(now),
        "nonvar": nonvar_rows(now),
        "update": update_rows(now),
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
    write_csv(ACTION_CSV, tables["action"])
    write_csv(PROJECTOR_CSV, tables["projector"])
    write_csv(NONVAR_CSV, tables["nonvar"])
    write_csv(UPDATE_CSV, tables["update"])
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
## PPC4161 Local Addendum - Qshadow Source-Map Normal-Form Gate

Marker: `{MARKER}`
Source checkpoint: `{DOC_PATH}`

The source-shadow numerator is now split as `Q_shadow := Q_shadow_action + Q_shadow_projector + Q_shadow_nonvariational`. Bianchi/Ward consistency is treated as a filter, not a zero proof: shadows must be parent-action content, identity/common-mode projector content, boundary/improvement-silent, absent, or retained as explicit nonclaim coefficients.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""
## PPC4161 Packet Addendum - Qshadow Source-Map Normal-Form Gate

Marker: `{PACKET_MARKER}`
Source checkpoint: `{DOC_PATH}`

The private packet now treats hidden source maps, post-Hilbert projectors, nonminimal action terms, shadow frames and nonvariational conserved blocks as explicit Q_shadow channels. The next move is a full Qbar_XH source-envelope rollup.
""",
    )
    validation = validate(tables)
    write_csv(VALIDATION_CSV, validation)
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        raise SystemExit(f"4610 validation failed: {failed}")
    print(f"4610 checkpoint generated: {DOC_PATH}")
    print(f"Validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
