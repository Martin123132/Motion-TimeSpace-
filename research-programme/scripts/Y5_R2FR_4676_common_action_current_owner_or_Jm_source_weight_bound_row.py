from __future__ import annotations

import csv
import io
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4676"
CLAIM_ID = "L-518"
BRANCH = "MTS_R2FR_Y5_COMMON_ACTION_CURRENT_OWNER_OR_JM_SOURCE_WEIGHT_BOUND_ROW_4676"
MARKER = "PPC4161_COMMON_ACTION_CURRENT_OWNER_OR_JM_SOURCE_WEIGHT_BOUND_ROW_4676"
PACKET_MARKER = "PPC4161_PACKET_COMMON_ACTION_CURRENT_OWNER_OR_JM_SOURCE_WEIGHT_BOUND_ROW_4676"
DECISION = "SOURCE_WEIGHT_SPLIT_COMMON_CALIBRATION_FROM_RELATIVE_DRIFT_TWO_LOCK_ZERO_THEOREM_UNSIGNED_BOUND_ROW_READY_NONCLAIM"
NEXT_TARGET = "4677-Y5-R2FR-visible-EM-action-edge-parent-signature-or-Jsourceweight-bound-input.md"

DOC_PATH = POST / "4676-Y5-R2FR-common-action-current-owner-or-Jm-source-weight-bound-row.md"
FORMAL_PATH = FORMAL / "692-PPC4161-common-action-current-owner-or-Jm-source-weight-bound-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4675_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4675_NEXT_TARGET.csv"
CSV_4675_SURVIVOR = SOURCE_DIR / "P8_Y5_R2FR_4675_JM_SURVIVOR_VECTOR.csv"
CSV_4675_REDUCTION = SOURCE_DIR / "P8_Y5_R2FR_4675_JM_UNOWNED_COMPONENT_REDUCTION.csv"
CSV_4675_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4675_VALIDATION.csv"
DOC_4675 = POST / "4675-Y5-R2FR-source-branch-force-residual-zero-or-first-numeric-bound-row.md"
FORMAL_691 = FORMAL / "691-PPC4161-source-branch-force-residual-zero-or-first-numeric-bound-row.md"

CSV_2127_IDENTITY = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2127_INERTIAL_ACTIVE_SOURCE_IDENTITY_ATTEMPT.csv"
CSV_2127_OBS = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2127_RETAINED_SOURCE_PREFACTOR_OBSTRUCTIONS.csv"
CSV_2127_CLOSURE = SOURCE_DIR / "P8_Y5_PARENT_QLOC_2127_EXPLICIT_EP_CLOSURE.csv"
CSV_4266_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4266_SOURCE_READOUT_THEOREM.csv"
CSV_4266_REMAINDER = SOURCE_DIR / "P8_Y5_R2FR_4266_REMAINDER_SPLIT_ROWS.csv"
CSV_4430_DERIV = SOURCE_DIR / "P8_Y5_R2FR_4430_DERIVATION_ROWS.csv"
CSV_4430_SIG = SOURCE_DIR / "P8_Y5_R2FR_4430_SOURCE_OWNER_SIGNATURE_OUTPUT.csv"
CSV_4430_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4430_DECISION.csv"
CSV_4430_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4430_VALIDATION.csv"
FORMAL_446 = FORMAL / "446-PPC4161-total-Hilbert-source-owner-no-source-weight-signature-or-TiPt-DD-map.md"
CSV_4424_DERIV = SOURCE_DIR / "P8_Y5_R2FR_4424_DERIVATION_ROWS.csv"
CSV_4424_CEX = SOURCE_DIR / "P8_Y5_R2FR_4424_CONSTRUCTOR_EXHAUSTION_OUTPUT.csv"
CSV_4434_DERIV = SOURCE_DIR / "P8_Y5_R2FR_4434_DERIVATION_ROWS.csv"
CSV_4434_HBAR = SOURCE_DIR / "P8_Y5_R2FR_4434_HBAR_MEASURE_OWNER_OUTPUT.csv"
CSV_4434_GRAPH = SOURCE_DIR / "P8_Y5_R2FR_4434_CONNECTED_GRAPH_OUTPUT.csv"
CSV_4434_EDGE_QUEUE = SOURCE_DIR / "P8_Y5_R2FR_4434_EDGE_CERTIFICATE_QUEUE.csv"
CSV_4434_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4434_VALIDATION.csv"
FORMAL_450 = FORMAL / "450-PPC4161-parent-hbar-measure-owner-and-connected-matter-certificate-or-Kmactionscale-value.md"
CSV_4435_EDGE = SOURCE_DIR / "P8_Y5_R2FR_4435_ACTION_DENSITY_EDGE_OUTPUT.csv"
CSV_4435_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4435_DECISION.csv"
CSV_4435_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4435_VALIDATION.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4676_SOURCE_REGISTER.csv"
SPLIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4676_COMMON_RELATIVE_SOURCE_WEIGHT_SPLIT.csv"
TWO_LOCK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4676_TWO_LOCK_SOURCE_WEIGHT_ZERO_THEOREM.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4676_SOURCE_WEIGHT_SURVIVOR_VECTOR.csv"
BOUND_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4676_FIRST_SOURCE_WEIGHT_BOUND_ROW.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4676_CONTROL_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4676_RUNNER_RESULTS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4676_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4676_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4676_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4676_VALIDATION.csv"


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
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def table(rows: list[dict[str, Any]]) -> str:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    lines = ["| " + " | ".join(fields) + " |", "| " + " | ".join("---" for _ in fields) + " |"]
    for row in rows:
        values = [str(row.get(field, "")).replace("|", "\\|").replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
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


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4676_00_4675_next", CSV_4675_NEXT, "4676-Y5-R2FR-common-action-current-owner-or-Jm-source-weight-bound-row.md", "4675 selected this target."),
        ("SRC4676_01_4675_survivor", CSV_4675_SURVIVOR, "SURV4675_0_source_weight", "source-weight survivor."),
        ("SRC4676_02_4675_reduction", CSV_4675_REDUCTION, "RED4675_5_survivor_identity", "Jm survivor reduction."),
        ("SRC4676_03_4675_validation", CSV_4675_VALIDATION, "VAL4675_OVERALL,True,PASS", "4675 validation."),
        ("SRC4676_04_doc4675", DOC_4675, "J_m_survivor =", "4675 prose."),
        ("SRC4676_05_formal691", FORMAL_691, "J_m_survivor =", "4675 formal note."),
        ("SRC4676_06_2127_identity", CSV_2127_IDENTITY, "IAS2127_2_classical_rescale_obstruction", "classical rescale obstruction."),
        ("SRC4676_07_2127_obstruction", CSV_2127_OBS, "OBS2127_0_wA_action", "w_A countermodel."),
        ("SRC4676_08_2127_closure", CSV_2127_CLOSURE, "EPC2127_1_common_quotient", "measured-G common quotient."),
        ("SRC4676_09_4266_common", CSV_4266_THEOREM, "SRCRO4266_3_common_mode_split", "common calibration split."),
        ("SRC4676_10_4266_remainder", CSV_4266_REMAINDER, "REM4266_0_kappa_G_owner", "G/kappa owner retained."),
        ("SRC4676_11_4430_deriv", CSV_4430_DERIV, "THS4430_1_exchange_filter", "exchange-connected collapse."),
        ("SRC4676_12_4430_sig", CSV_4430_SIG, "SIG4430_2_no_source_weight_core", "same-action plus exchange filter."),
        ("SRC4676_13_4430_decision", CSV_4430_DECISION, "TOTAL_HILBERT_SOURCE_ZERO_SIGNATURE_EXACT", "4430 decision."),
        ("SRC4676_14_4430_validation", CSV_4430_VALIDATION, "VAL4430_18_pycache_absent", "4430 validation."),
        ("SRC4676_15_formal446", FORMAL_446, "C_species=DERIVED_ZERO", "formal 4430 theorem."),
        ("SRC4676_16_4424_deriv", CSV_4424_DERIV, "CEX4424_2_Hom_no_slot_result", "constructor exhaustion no-slot."),
        ("SRC4676_17_4424_cex", CSV_4424_CEX, "CEX4424_2_Hom_no_slot_if_exhausted", "Hom no-slot gate."),
        ("SRC4676_18_4434_deriv", CSV_4434_DERIV, "HMGC4434_0_two_lock_zero_theorem", "two-lock theorem."),
        ("SRC4676_19_4434_hbar", CSV_4434_HBAR, "HMO4434_2_hbar_measure_gap", "hbar/measure gap."),
        ("SRC4676_20_4434_graph", CSV_4434_GRAPH, "GRC4434_2_edge_rows_not_parent_signed", "graph edge gap."),
        ("SRC4676_21_4434_edge_queue", CSV_4434_EDGE_QUEUE, "EQ4434_0_single_L_to_EM", "first edge queue."),
        ("SRC4676_22_4434_validation", CSV_4434_VALIDATION, "VAL4434_20_pycache_absent", "4434 validation."),
        ("SRC4676_23_formal450", FORMAL_450, "w_A=w_*", "formal two-lock theorem."),
        ("SRC4676_24_4435_edge", CSV_4435_EDGE, "EDGE4435_1_L_parent_to_EM_visible_domain", "first edge attempt."),
        ("SRC4676_25_4435_decision", CSV_4435_DECISION, "FIRST_EDGE_CERTIFICATE_REDUCED", "4435 decision."),
        ("SRC4676_26_4435_validation", CSV_4435_VALIDATION, "VAL4435_18_pycache_absent", "4435 validation."),
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


def split_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "SPL4676_0_weighted_action",
            "S_matter=sum_A w_A S_A",
            "delta S_matter/delta e_obs = sum_A w_A T_A",
            "This is the obstruction: classical matter EOM may divide out w_A, but Hilbert source does not.",
            "EXACT_OBSTRUCTION",
        ),
        (
            "SPL4676_1_common_relative_split",
            "w_A=w_*+delta w_A with chosen common mode w_*",
            "T_source=w_* T_total + sum_A delta w_A T_A",
            "w_* is a universal calibration absorbed into kappa_eff/G_N; delta w_A is physical source-weight drift.",
            "NEW_LOCAL_SPLIT_APPLIED_TO_JM",
        ),
        (
            "SPL4676_2_common_mode",
            "J_common = w_* T_total",
            "kappa_eff J_common defines calibrated G_N/GM normalization",
            "MTS does not need to predict numerical G_N at this gate, just prevent relative hidden source weights.",
            "COMMON_CALIBRATION_NOT_A_SOURCE_VIOLATION",
        ),
        (
            "SPL4676_3_relative_mode",
            "J_relative=sum_A delta w_A T_A",
            "J_source_weight := J_relative plus source-current prefactor drift",
            "This is the piece that threatens WEP/R10/PPN/orbital/local-GR consistency.",
            "DANGEROUS_SURVIVOR",
        ),
        (
            "SPL4676_4_exchange_filter",
            "sum_A delta w_A C_A^nu=0 on exchange currents",
            "connected exchange graph => delta w_A constant on a connected component",
            "after subtracting w_*, connected-component relative weights vanish; disconnected blocks survive.",
            "PARTIAL_DERIVATION_IMPORT",
        ),
        (
            "SPL4676_5_bound_form",
            "|J_source_weight| <= |J_block|+|J_shadow|+|J_nonHilbert|+|J_marker_readout|+|J_current_norm|",
            "absolute no-cancellation survivor envelope",
            "This feeds 4675 J_m_survivor and therefore B826.",
            "BOUND_FORM_SHARPENED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "split_id": row[0],
            "object": row[1],
            "formula": row[2],
            "consequence": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def two_lock_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("LOCK4676_0_lock1", "Universal action/measure/current owner", "one parent phase, hbar_parent, common path/statistical measure, species-blind Jacobian, action-density owner, current owner, variation-before-readout", "would forbid independent w_A/hbar_A/current rescalings", "HBAR_MEASURE_OWNER_UNSIGNED"),
        ("LOCK4676_1_lock2", "Parent-owned connected ordinary-matter graph", "nonzero action-density/source morphisms connect ordinary sectors and source functor forgets labels", "propagates w_A=w_* by connected naturality/exchange", "PARENT_EDGES_UNSIGNED"),
        ("LOCK4676_2_result", "Relative source-weight zero theorem", "Lock1 + Lock2 + no source-shadow + no hidden/readout return + no non-Hilbert bypass => delta w_A=0", "kills J_source_weight relative channel without fitting it", "EXACT_CONDITIONAL_THEOREM"),
        ("LOCK4676_3_common_G", "Universal G/kappa calibration", "w_* is absorbed into kappa_eff or measured G_N/GM", "does not need derivation here and does not violate local GR if universal and stable", "COMMON_MODE_ALLOWED"),
        ("LOCK4676_4_current_status", "current MTS evidence", "phase seed and physical graph template exist, but hbar/measure/Jacobian/current owner and parent graph edges are unsigned", "zero theorem cannot be claimed yet", "NOT_PARENT_SIGNED_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "lock_id": row[0],
            "clause": row[1],
            "condition": row[2],
            "effect": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SW4676_0_block", "J_block", "disconnected-component or block-relative action/source weight", "delta_w_block;block graph certificate", "BOUND_OR_EDGE_PROOF_REQUIRED"),
        ("SW4676_1_shadow", "J_shadow", "source-shadow functional S_source=sum_A w_A S_A outside ordinary matter action", "C_shadow;source-shadow ban certificate", "PRIMARY_ZERO_TARGET"),
        ("SW4676_2_nonHilbert", "J_nonHilbert_weight", "non-Hilbert bypass current carrying active-source weight", "C_nonHilbert;J_NH_zero_certificate", "BOUND_OR_ZERO_REQUIRED"),
        ("SW4676_3_marker", "J_marker_readout", "hidden marker/readout/material return into source coefficient", "C_marker_readout;no-return certificate", "BOUND_OR_ZERO_REQUIRED"),
        ("SW4676_4_current_norm", "J_current_norm", "species/source current normalization drift J_A -> c_A J_A", "delta_c_A;current_owner_certificate", "BOUND_OR_ZERO_REQUIRED"),
        ("SW4676_5_total", "J_source_weight_abs", "absolute no-cancellation sum of all source-weight survivors", "all above in common normalization", "SCHEMA_READY_VALUES_MISSING"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": row[0],
            "symbol": row[1],
            "meaning": row[2],
            "required_inputs": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BND4676_0_master", "J_source_weight_abs", "|J_block|+|J_shadow|+|J_nonHilbert_weight|+|J_marker_readout|+|J_current_norm|", "common_m_lock_force_units", "MISSING_COMPONENT_VALUES"),
        ("BND4676_1_Jm", "J_m_survivor_update", "J_source_weight_abs + |J_coeff|+|J_nonHilbert|+|J_open_boundary|+|J_domain_reentry|+|E_m_res|", "common_m_lock_force_units", "MISSING_FULL_VECTOR_VALUES"),
        ("BND4676_2_B826", "B826_source_weight_bound", "|a_F| L_cg^-2 J_source_weight_abs", "B826_units_from_4507", "MISSING_AF_LCG_AND_SOURCE_WEIGHT_VALUES"),
        ("BND4676_3_WEP_DD", "TiPt_DD_projection", "0.00333 sum |K_mj C_j| + 0.00204 sum |K_ej C_j| <= 2.8e-15", "dimensionless_eta", "SYMBOLIC_TARGET_VALUES_MISSING"),
        ("BND4676_4_single_mhat", "single_channel_mhat_ceiling", "|D_mhat| <= 8.408408408408e-13", "dimensionless_nonclaim_ceiling", "COMPARATOR_ONLY_NOT_THEORY_VALUE"),
        ("BND4676_5_single_e", "single_channel_e_ceiling", "|D_e| <= 1.372549019608e-12", "dimensionless_nonclaim_ceiling", "COMPARATOR_ONLY_NOT_THEORY_VALUE"),
        ("BND4676_6_claim_gate", "valid_for_claim", "true only after theorem-zero or source-backed parent coefficient/source-leg values", "boolean", "FALSE_NOW"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row[0],
            "symbol": row[1],
            "formula": row[2],
            "units": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4676_0_no_classical_rescale", "Do not use classical EOM rescaling as proof; Hilbert source still scales by w_A.", "ACTIVE"),
        ("CTRL4676_1_common_G_allowed", "A universal stable common factor may be calibrated as G_N/kappa; only relative/source-only drift is dangerous here.", "ACTIVE"),
        ("CTRL4676_2_no_fitted_G_hiding", "Do not hide relative delta w_A or kappa_A inside fitted G/GM.", "ACTIVE"),
        ("CTRL4676_3_no_bound_inversion", "WEP/R10/PPN bounds are ceilings, not MTS coefficient values.", "ACTIVE"),
        ("CTRL4676_4_no_public_claim", "No local-GR/Newton/PPN/R10 claim until two-lock theorem or numeric source rows close.", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": row[0],
            "rule": row[1],
            "status": row[2],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "why": "4676 separates universal calibration from dangerous relative source-weight drift. The two-lock theorem would kill relative weights, but current MTS has unsigned hbar/measure/current owner and parent graph edge certificates. The finite source-weight bound row is now explicit.",
            "promoted": False,
            "claim_allowed": False,
            "valid_for_claim": False,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "common_relative_split_derived": True,
            "common_G_calibration_allowed": True,
            "two_lock_theorem_staged": True,
            "hbar_measure_owner_signed": False,
            "parent_graph_edges_signed": False,
            "source_weight_zero_claim": False,
            "numeric_bound_sourced": False,
            "local_GR_claim": False,
            "r10_claim": False,
            "ppn_claim": False,
            "decision": DECISION,
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "why": "The two-lock theorem now makes the next proof target concrete: sign one parent-owned ordinary-matter graph edge, starting with the visible EM action edge, or fill the first source-weight bound input.",
            "derive_route": "Parent-sign the visible EM action edge as same-parent action-density/current morphism with no source prefactor or extra F2 source-shadow.",
            "fallback_route": "Fill one source-backed K*C source-weight row for the Ti/Pt or m-lock projection.",
            "avoid": "Do not treat physical template edges as parent-owned certificates.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def runner_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    splits: list[dict[str, Any]],
    locks: list[dict[str, Any]],
    survivors: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    split_ok = any(row["split_id"] == "SPL4676_1_common_relative_split" for row in splits)
    two_lock_ok = any(row["lock_id"] == "LOCK4676_2_result" for row in locks)
    common_ok = any(row["lock_id"] == "LOCK4676_3_common_G" for row in locks)
    survivor_ok = any(row["survivor_id"] == "SW4676_5_total" for row in survivors)
    bound_ok = any(row["bound_id"] == "BND4676_0_master" for row in bounds)
    nonclaim_ok = all(not row["valid_for_claim"] and not row["claim_allowed"] for row in [*splits, *locks, *survivors, *bounds])
    checks = [
        ("RUN4676_0_sources", source_ok, "all source paths and needles found" if source_ok else "source path/needle failure"),
        ("RUN4676_1_split", split_ok, "common/relative split present" if split_ok else "split missing"),
        ("RUN4676_2_two_lock", two_lock_ok, "two-lock zero theorem staged" if two_lock_ok else "two-lock theorem missing"),
        ("RUN4676_3_common_G", common_ok, "common G calibration separated" if common_ok else "common mode missing"),
        ("RUN4676_4_survivor", survivor_ok, "source-weight survivor vector present" if survivor_ok else "survivor vector missing"),
        ("RUN4676_5_bound", bound_ok, "first source-weight bound row present" if bound_ok else "bound row missing"),
        ("RUN4676_6_nonclaim", nonclaim_ok, "all rows remain nonclaim" if nonclaim_ok else "claim flag promoted"),
        ("RUN4676_7_next", True, "next target selected"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "runner_id": check_id,
            "passed": passed,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for check_id, passed, detail in checks
    ]


def validation_rows(timestamp: str, csv_paths: list[Path], sources: list[dict[str, Any]], runners: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    rows.append({"validation_id": "VAL4676_0_sources", "passed": source_ok, "detail": "all source paths and needles found" if source_ok else "source path/needle failure", "timestamp_utc": timestamp})
    parse_ok = True
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            detail = f"rows={len(parsed)} columns={len(parsed[0]) if parsed else 0}"
            passed = bool(parsed)
        except Exception as exc:  # pragma: no cover
            detail = repr(exc)
            passed = False
        parse_ok = parse_ok and passed
        rows.append({"validation_id": f"VAL4676_parse_{path.name}", "passed": passed, "detail": detail, "timestamp_utc": timestamp})
    runner_ok = all(row["passed"] for row in runners)
    rows.append({"validation_id": "VAL4676_1_runner_pass", "passed": runner_ok, "detail": "runner rows passed" if runner_ok else "runner failure", "timestamp_utc": timestamp})
    output_paths = [DOC_PATH, FORMAL_PATH, *csv_paths]
    outputs_exist = all(path.exists() for path in output_paths)
    rows.append({"validation_id": "VAL4676_2_outputs_exist", "passed": outputs_exist, "detail": ";".join(str(path) for path in output_paths), "timestamp_utc": timestamp})
    nonclaim = "valid_for_claim,true" not in read_text(RUNNER_CSV).lower() and "claim_allowed,true" not in read_text(RUNNER_CSV).lower()
    rows.append({"validation_id": "VAL4676_3_no_claim_promotion", "passed": nonclaim, "detail": "valid_for_claim remains false", "timestamp_utc": timestamp})
    overall = source_ok and parse_ok and runner_ok and outputs_exist and nonclaim
    rows.append({"validation_id": "VAL4676_OVERALL", "passed": overall, "detail": "PASS" if overall else "FAIL", "timestamp_utc": timestamp})
    return rows


def write_documents(
    sources: list[dict[str, Any]],
    splits: list[dict[str, Any]],
    locks: list[dict[str, Any]],
    survivors: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    body = f"""# 4676 - Y5/R2FR Common Action/Current Owner or Jm Source-Weight Bound Row

**Current verdict:** 4676 makes the source-coupling problem sharper. A universal source factor is not the danger; it is the calibrated `G_N/kappa` mode. The dangerous term is the relative/source-only part:

```text
w_A = w_* + delta w_A
T_source = w_* T_total + sum_A delta w_A T_A.
```

The common mode `w_*` can be absorbed into calibrated `G_N/GM` if it is universal and stable. The local-GR threat is:

```text
J_source_weight = sum_A delta w_A T_A
```

plus source-current normalization drift. The two-lock theorem says relative source weights vanish if universal action/measure/current ownership and a parent-owned connected ordinary-matter graph both close. Current MTS has the theorem shape but not the parent signatures, so the first source-weight bound row remains live.

## Runner results

{table(runners)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next target

{table(nexts)}

## Common/relative split

{table(splits)}

## Two-lock source-weight zero theorem

{table(locks)}

## Source-weight survivor vector

{table(survivors)}

## First source-weight bound row

{table(bounds)}

## Controls

{table(controls)}

## Source register

{table(sources)}

## Validation

{table(validations)}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4676 -", "# 692 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        claim = csv_line(
            [
                CLAIM_ID,
                "local_gr_empirical_interface",
                "4676 separates universal source calibration from relative/source-only source-weight drift. A common factor is a calibrated G_N/kappa mode; the dangerous survivor is delta w_A/source-current normalization. The two-lock theorem would set relative weights to zero, but hbar/measure/current owner and parent graph edge signatures remain unsigned.",
                "Generated source register, common/relative source-weight split, two-lock theorem rows, survivor vector, first source-weight bound row, controls, runner, decision, status, next target and validation.",
                DECISION.lower(),
                NEXT_TARGET,
                "Using classical EOM rescaling as proof, hiding relative weights inside fitted G, treating comparator ceilings as MTS coefficients, or treating template graph edges as parent certificates.",
                "local_gr",
                str(DOC_PATH),
                NEXT_TARGET,
                "No public local-GR/Newton/PPN/R10 claim until relative source weights are theorem-zero or source-backed bounded.",
            ]
        )
        append_once(CLAIMS_PATH, CLAIM_ID, claim)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

4676 separates the coupling issue into:

```text
w_A = w_* + delta w_A
```

where `w_*` is universal calibrated `G_N/kappa` mode and `delta w_A` is the dangerous relative source-weight drift. The two-lock theorem is now the active derivation route: universal action/measure/current owner plus parent-owned connected matter graph implies `delta w_A=0`. Current signatures are unsigned, so the finite source-weight bound row remains live.

- checkpoint: `{DOC_PATH.name}`
- formal note: `{FORMAL_PATH.name}`
- decision: `{DECISION}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""

## {PACKET_MARKER}

Packet update: source coupling is no longer a blob. Universal `G_N` calibration is separated from relative source-weight drift. The next target is one parent-owned visible EM action edge or a first source-weight bound input.

- claim id: `{CLAIM_ID}`
- split csv: `{SPLIT_CSV.name}`
- two-lock csv: `{TWO_LOCK_CSV.name}`
- survivor csv: `{SURVIVOR_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def main() -> None:
    timestamp = now()
    sources = source_rows(timestamp)
    splits = split_rows(timestamp)
    locks = two_lock_rows(timestamp)
    survivors = survivor_rows(timestamp)
    bounds = bound_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    runners = runner_rows(timestamp, sources, splits, locks, survivors, bounds)

    csv_paths = [
        SOURCE_REGISTER,
        SPLIT_CSV,
        TWO_LOCK_CSV,
        SURVIVOR_CSV,
        BOUND_ROW_CSV,
        CONTROL_CSV,
        RUNNER_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(SPLIT_CSV, splits)
    write_csv(TWO_LOCK_CSV, locks)
    write_csv(SURVIVOR_CSV, survivors)
    write_csv(BOUND_ROW_CSV, bounds)
    write_csv(CONTROL_CSV, controls)
    write_csv(RUNNER_CSV, runners)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_documents(sources, splits, locks, survivors, bounds, controls, runners, decisions, statuses, nexts, [])
    validations = validation_rows(timestamp, csv_paths, sources, runners)
    write_csv(VALIDATION_CSV, validations)
    write_documents(sources, splits, locks, survivors, bounds, controls, runners, decisions, statuses, nexts, validations)
    update_registers(timestamp)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
