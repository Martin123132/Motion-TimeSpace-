from __future__ import annotations

import csv
import io
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4677"
CLAIM_ID = "L-519"
BRANCH = "MTS_R2FR_Y5_VISIBLE_EM_ACTION_EDGE_TO_JSOURCEWEIGHT_4677"
MARKER = "PPC4161_VISIBLE_EM_ACTION_EDGE_TO_JSOURCEWEIGHT_4677"
PACKET_MARKER = "PPC4161_PACKET_VISIBLE_EM_ACTION_EDGE_TO_JSOURCEWEIGHT_4677"
DECISION = "VISIBLE_EM_FIXED_BRANCH_SOURCE_WEIGHT_PRODUCT_ZERO_IMPORTED_NONEM_AND_OPEN_EM_TAILS_REMAIN"
NEXT_TARGET = "4678-Y5-R2FR-source-charge-Htau-MHref-coupling-tail-or-Jsourceweight-nonEM-bound-row.md"

DOC_PATH = POST / "4677-Y5-R2FR-visible-EM-action-edge-parent-signature-or-Jsourceweight-bound-input.md"
FORMAL_PATH = FORMAL / "693-PPC4161-visible-EM-action-edge-parent-signature-or-Jsourceweight-bound-input.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

FORMAL_454 = FORMAL / "454-PPC4161-radiative-readout-EM-closure-or-total-Kmactionscale-source-value.md"
FORMAL_455 = FORMAL / "455-PPC4161-integrate-fixed-branch-EM-zero-into-local-residual-vector-or-source-charge-tail.md"
FORMAL_692 = FORMAL / "692-PPC4161-common-action-current-owner-or-Jm-source-weight-bound-row.md"
DOC_4676 = POST / "4676-Y5-R2FR-common-action-current-owner-or-Jm-source-weight-bound-row.md"

CSV_4676_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4676_NEXT_TARGET.csv"
CSV_4676_SURVIVOR = SOURCE_DIR / "P8_Y5_R2FR_4676_SOURCE_WEIGHT_SURVIVOR_VECTOR.csv"
CSV_4676_LOCKS = SOURCE_DIR / "P8_Y5_R2FR_4676_TWO_LOCK_SOURCE_WEIGHT_ZERO_THEOREM.csv"
CSV_4676_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4676_FIRST_SOURCE_WEIGHT_BOUND_ROW.csv"
CSV_4436_SIGNATURE = SOURCE_DIR / "P8_Y5_R2FR_4436_VISIBLE_EM_SIGNATURE_OUTPUT.csv"
CSV_4436_STRESS = SOURCE_DIR / "P8_Y5_R2FR_4436_EM_STRESS_EXCHANGE_ROWS.csv"
CSV_4437_COUPLING = SOURCE_DIR / "P8_Y5_R2FR_4437_SAME_OWNER_COUPLING_OUTPUT.csv"
CSV_4437_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4437_EM_COUPLING_ZERO_ROWS.csv"
CSV_4438_TOTAL_ZERO = SOURCE_DIR / "P8_Y5_R2FR_4438_TOTAL_EM_ZERO_ROWS.csv"
CSV_4438_OPEN = SOURCE_DIR / "P8_Y5_R2FR_4438_OPEN_EM_SURVIVOR_ROWS.csv"
CSV_4439_VECTOR = SOURCE_DIR / "P8_Y5_R2FR_4439_LOCAL_RESIDUAL_VECTOR_AFTER_EM.csv"
CSV_4439_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4439_REMAINING_BLOCKER_ROWS.csv"
CSV_4439_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4439_DECISION.csv"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4677_SOURCE_REGISTER.csv"
EDGE_IMPORT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4677_VISIBLE_EM_EDGE_IMPORT.csv"
FIXED_ZERO_CSV = SOURCE_DIR / "P8_Y5_R2FR_4677_FIXED_EM_ZERO_INTO_SOURCE_WEIGHT_VECTOR.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4677_JSOURCEWEIGHT_AFTER_VISIBLE_EM.csv"
OPEN_SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4677_OPEN_EM_AND_NONEM_SURVIVORS.csv"
BOUND_INPUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4677_BOUND_INPUT_ROWS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4677_CONTROL_ROWS.csv"
RUNNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4677_RUNNER_RESULTS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4677_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4677_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4677_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4677_VALIDATION.csv"


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
    if not rows:
        return ""
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
        ("SRC4677_00_4676_next", CSV_4676_NEXT, "visible EM action edge", "4676 selected visible EM as first source-weight edge."),
        ("SRC4677_01_4676_survivor", CSV_4676_SURVIVOR, "SW4676_5_total", "4676 total source-weight survivor vector."),
        ("SRC4677_02_4676_locks", CSV_4676_LOCKS, "LOCK4676_2_result", "4676 two-lock zero theorem."),
        ("SRC4677_03_4676_bound", CSV_4676_BOUND, "BND4676_0_master", "4676 source-weight bound row."),
        ("SRC4677_04_doc4676", DOC_4676, "J_source_weight", "4676 prose source-weight definition."),
        ("SRC4677_05_formal692", FORMAL_692, "w_A = w_* + delta w_A", "formal 4676 source-weight split."),
        ("SRC4677_06_4436_signature", CSV_4436_SIGNATURE, "EMS4436_0_standard_visible_import_branch", "visible EM action edge signed inside fixed visible branch."),
        ("SRC4677_07_4436_stress", CSV_4436_STRESS, "STX4436_2_poynting", "Poynting is Hilbert stress flux, not extra standalone source."),
        ("SRC4677_08_4437_same_owner", CSV_4437_COUPLING, "SOC4437_0_fixed_qbasic_standard_branch", "fixed q-basic same-owner EM coupling zero."),
        ("SRC4677_09_4437_zero", CSV_4437_ZERO, "ZERO4437_2_b_alpha", "alpha/coupling drift zero row in fixed branch."),
        ("SRC4677_10_4438_total_zero", CSV_4438_TOTAL_ZERO, "ZERO4438_0_total_EM_product", "total fixed-branch EM source product zero."),
        ("SRC4677_11_4438_open", CSV_4438_OPEN, "SURV4438_0_open_radiation", "open EM survivor firewall."),
        ("SRC4677_12_formal454", FORMAL_454, "ZERO4438_0_total_EM_product", "formal fixed EM total zero."),
        ("SRC4677_13_4439_vector", CSV_4439_VECTOR, "RV4439_0_fixed_clean_private_after_EM", "fixed EM deleted from local vector."),
        ("SRC4677_14_4439_blockers", CSV_4439_BLOCKERS, "BLK4439_5_open_EM_branch", "open EM branch retained."),
        ("SRC4677_15_4439_decision", CSV_4439_DECISION, "FIXED_BRANCH_EM_TAIL_DELETED", "4439 decision."),
        ("SRC4677_16_formal455", FORMAL_455, "Delta_local_fixed_after_EM", "formal fixed EM vector rewrite."),
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


def edge_import_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "EDGE4677_0_fixed_visible_EM_action",
            "standard visible import / fixed q-basic same-Hodge static closed-collar branch",
            "S_EM=-1/4 int sqrt(-g_obs) F^2 + int A_mu J^mu",
            "same branch owns Hodge/stress/current; no independent source prefactor in the fixed branch",
            "J_EM_fixed_source_weight=0",
            "VISIBLE_EM_EDGE_IMPORTED_TO_JSOURCEWEIGHT_FIXED_ZERO",
        ),
        (
            "EDGE4677_1_poynting_once_only",
            "same fixed branch",
            "S^i=(E x B)^i/mu0 appears as Hilbert stress-energy flux",
            "do not add a second Poynting force/source-weight term",
            "no extra J_Poynting_source_weight channel",
            "POYNTING_DOUBLE_COUNT_FIREWALL",
        ),
        (
            "EDGE4677_2_open_dynamic_EM",
            "open radiation/readout/global-dynamic EM branch",
            "Delta_EM_open_dynamic retained",
            "fixed closed-collar zero does not apply",
            "finite source or boundary value still required",
            "OPEN_EM_RETAINED",
        ),
        (
            "EDGE4677_3_nonEM_source_weight",
            "ordinary non-EM source sectors",
            "J_block/J_shadow/J_nonHilbert/J_marker_readout/J_current_norm",
            "visible EM edge does not prove non-EM matter graph connectedness or source-current ownership",
            "survivor vector remains live",
            "NONEM_SOURCE_WEIGHT_REMAINS",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "edge_id": row[0],
            "domain": row[1],
            "object": row[2],
            "import_rule": row[3],
            "effect_on_Jsourceweight": row[4],
            "status": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def fixed_zero_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "ZERO4677_0_fixed_EM_source_weight_product",
            "J_EM_fixed_source_weight",
            "|K_m_EM_action_scale C_EM_action_scale_total|",
            "0",
            "4438 total fixed-branch EM product zero + 4439 vector rewrite",
            "DERIVED_ZERO_FIXED_BRANCH_NONCLAIM",
        ),
        (
            "ZERO4677_1_coupling_drift_bundle",
            "C_XF2,C_JQ,b_alpha,C_EM_readout,Phi_EM_rad,Delta_Hodge_EM",
            "fixed q-basic same-Hodge static closed-collar bundle",
            "0 as total fixed bundle",
            "4437 same-owner coupling zero + 4438 radiative/readout closure",
            "DERIVED_ZERO_FIXED_BRANCH_NONCLAIM",
        ),
        (
            "ZERO4677_2_poynting_extra_source",
            "J_Poynting_extra",
            "standalone Poynting force/source outside Hilbert stress",
            "0 in fixed branch",
            "4436 Poynting once-only guard",
            "NO_DOUBLE_COUNT_FIXED_BRANCH",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "zero_id": row[0],
            "symbol": row[1],
            "expression": row[2],
            "value_in_fixed_branch": row[3],
            "source_logic": row[4],
            "status": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        (
            "JSW4677_0_before_visible_EM_import",
            "J_source_weight_abs",
            "|J_EM_fixed_source_weight| + |J_EM_open_dynamic| + |J_source_weight_nonEM|",
            "pre-4677 visible EM split inside 4676 source-weight vector",
            "SPLIT_FOR_IMPORT",
        ),
        (
            "JSW4677_1_after_fixed_visible_EM_import",
            "J_source_weight_abs_after_visible_EM",
            "|J_EM_open_dynamic| + |J_source_weight_nonEM|",
            "fixed visible EM product removed; open/dynamic EM retained",
            "REAL_NARROWING_NONCLAIM",
        ),
        (
            "JSW4677_2_nonEM_source_weight",
            "J_source_weight_nonEM",
            "|J_block_nonEM|+|J_shadow_nonEM|+|J_nonHilbert_weight_nonEM|+|J_marker_readout_nonEM|+|J_current_norm_nonEM|",
            "ordinary non-EM source-current owner still unsigned",
            "NEXT_DERIVE_OR_BOUND_TARGET",
        ),
        (
            "JSW4677_3_local_B826_update",
            "B826_source_weight_tail_after_visible_EM",
            "|a_F| L_cg^-2 (|J_EM_open_dynamic|+|J_source_weight_nonEM|)",
            "feeds 4674/4675 B826 residual only after common units/projections are sourced",
            "BOUND_SCHEMA_ONLY",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "vector_id": row[0],
            "symbol": row[1],
            "formula": row[2],
            "meaning": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def open_survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("OPEN4677_0_open_radiation", "Delta_EM_open_dynamic", "open radiation/boundary flux outside fixed closed collar", "E_rad_EM or P_rad_EM boundary value/source row", "MISSING_SOURCE_VALUE"),
        ("OPEN4677_1_readout_regeneration", "C_EM_readout", "effective readout can regenerate EM coupling outside fixed branch", "readout owner/no-return theorem or finite coefficient", "MISSING_OWNER_OR_BOUND"),
        ("OPEN4677_2_global_dynamic_F2", "C_XF2_global_dynamic", "global/dynamic EM deformation may carry extra F2/source prefactor", "parent unique-F2 certificate or finite source-backed row", "MISSING_PARENT_SIGNATURE"),
        ("OPEN4677_3_nonEM_weight", "J_source_weight_nonEM", "visible EM edge does not close non-EM matter graph/source-current weights", "ordinary matter graph/current owner or finite rows", "NEXT_HIGH_LEVERAGE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": row[0],
            "symbol": row[1],
            "why_survives": row[2],
            "needed_to_close": row[3],
            "status": row[4],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("BND4677_0_fixed_EM_zero", "J_EM_fixed_source_weight", "0", "fixed branch theorem value", "source_path_backed_by_4438_4439", "DERIVED_ZERO_FIXED_BRANCH_BUT_NONPUBLIC"),
        ("BND4677_1_open_EM_bound", "J_EM_open_dynamic", "|E_rad_EM|+|C_EM_readout|+|C_XF2_global_dynamic|+|C_JQ_global_dynamic|", "common source-weight units", "MISSING_NUMERIC_SOURCE_ROWS", "BOUND_INPUT_REQUIRED"),
        ("BND4677_2_nonEM_bound", "J_source_weight_nonEM", "|J_block_nonEM|+|J_shadow_nonEM|+|J_nonHilbert_weight_nonEM|+|J_marker_readout_nonEM|+|J_current_norm_nonEM|", "common source-weight units", "MISSING_PARENT_OWNER_OR_NUMERIC_ROWS", "NEXT_MAIN_TARGET"),
        ("BND4677_3_total_after_visible_EM", "J_source_weight_abs_after_visible_EM", "|J_EM_open_dynamic|+|J_source_weight_nonEM|", "common source-weight units", "MISSING_SURVIVOR_VALUES", "SCHEMA_READY_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "bound_id": row[0],
            "symbol": row[1],
            "formula_or_value": row[2],
            "units": row[3],
            "source_status": row[4],
            "status": row[5],
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row in data
    ]


def control_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("CTRL4677_0_scope", "Use the fixed visible EM zero only on the q-basic same-Hodge static closed-collar branch.", "ACTIVE"),
        ("CTRL4677_1_poynting", "Poynting flux is counted once through Hilbert stress; open radiative flux is a boundary/source survivor, not a second local force.", "ACTIVE"),
        ("CTRL4677_2_no_nonEM_promotion", "Do not use the visible EM edge to prove non-EM source weights or the full ordinary matter graph.", "ACTIVE"),
        ("CTRL4677_3_no_public_claim", "No local-GR/Newton/PPN/R10 claim from this narrowing alone.", "ACTIVE"),
        ("CTRL4677_4_next", "Next route is source-charge/H_tau/MHref/nonEM source-current ownership or finite source-backed bound rows.", "ACTIVE"),
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
            "why": "4677 imports the already-derived 4436-4439 fixed visible EM branch into the stricter 4676 source-weight vector. The fixed visible EM source-weight product is zero, Poynting is protected against double counting, but open/dynamic EM and non-EM source-weight/current tails remain live.",
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
            "fixed_visible_EM_source_weight_zero": True,
            "poynting_double_count_blocked": True,
            "open_dynamic_EM_retained": True,
            "nonEM_source_weight_closed": False,
            "global_parent_EM_edge_signed": False,
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
            "why": "The fixed visible EM part is now removed from the 4676 source-weight vector. The next useful leap is source-charge/H_tau/MHref/nonEM source-current ownership, or the first finite source-backed nonEM/open-EM bound row.",
            "derive_route": "Prove the same parent-owned source charge, H_tau/MHref reference subtraction, tau/frame/surface lock, source-blind kappa_eff and nonEM current owner close on one branch.",
            "fallback_route": "Write finite no-cancellation rows for J_source_weight_nonEM and J_EM_open_dynamic in R10/PPN/clock/orbital units.",
            "avoid": "Do not re-open fixed EM, claim G_N as predicted, or use fitted G/GM to hide relative source weights.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def runner_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    survivors: list[dict[str, Any]],
    open_survivors: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source_ok = all(row["path_exists"] and row["needle_found"] for row in sources)
    fixed_import_ok = any(row["zero_id"] == "ZERO4677_0_fixed_EM_source_weight_product" and row["value_in_fixed_branch"] == "0" for row in zeros)
    poynting_ok = any(row["edge_id"] == "EDGE4677_1_poynting_once_only" for row in edges)
    survivor_ok = any(row["vector_id"] == "JSW4677_1_after_fixed_visible_EM_import" for row in survivors)
    open_ok = any(row["survivor_id"] == "OPEN4677_0_open_radiation" for row in open_survivors)
    nonclaim_ok = all(not row["valid_for_claim"] and not row["claim_allowed"] for row in [*edges, *zeros, *survivors, *open_survivors])
    checks = [
        ("RUN4677_0_sources", source_ok, "all source paths and needles found" if source_ok else "source path/needle failure"),
        ("RUN4677_1_fixed_EM_import", fixed_import_ok, "fixed visible EM source-weight product set to zero in branch" if fixed_import_ok else "fixed EM import missing"),
        ("RUN4677_2_poynting_guard", poynting_ok, "Poynting double-count firewall present" if poynting_ok else "Poynting guard missing"),
        ("RUN4677_3_vector_rewrite", survivor_ok, "source-weight vector rewritten after visible EM" if survivor_ok else "vector rewrite missing"),
        ("RUN4677_4_open_retained", open_ok, "open/dynamic EM retained" if open_ok else "open EM survivor missing"),
        ("RUN4677_5_nonclaim", nonclaim_ok, "all rows remain nonclaim" if nonclaim_ok else "claim flag promoted"),
        ("RUN4677_6_next", True, "next target selected"),
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
    rows.append({"validation_id": "VAL4677_0_sources", "passed": source_ok, "detail": "all source paths and needles found" if source_ok else "source path/needle failure", "timestamp_utc": timestamp})
    parse_ok = True
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            passed = bool(parsed)
            detail = f"rows={len(parsed)} columns={len(parsed[0]) if parsed else 0}"
        except Exception as exc:
            passed = False
            detail = repr(exc)
        parse_ok = parse_ok and passed
        rows.append({"validation_id": f"VAL4677_parse_{path.name}", "passed": passed, "detail": detail, "timestamp_utc": timestamp})
    runner_ok = all(row["passed"] for row in runners)
    rows.append({"validation_id": "VAL4677_1_runner_pass", "passed": runner_ok, "detail": "runner rows passed" if runner_ok else "runner failure", "timestamp_utc": timestamp})
    outputs_exist = all(path.exists() for path in [DOC_PATH, FORMAL_PATH, *csv_paths])
    rows.append({"validation_id": "VAL4677_2_outputs_exist", "passed": outputs_exist, "detail": "post/formal/csv outputs exist", "timestamp_utc": timestamp})
    claim_row = CLAIM_ID in read_text(CLAIMS_PATH)
    rows.append({"validation_id": "VAL4677_3_claim_row_exists", "passed": claim_row, "detail": f"{CLAIM_ID} present" if claim_row else f"{CLAIM_ID} missing", "timestamp_utc": timestamp})
    spine = MARKER in read_text(SPINE_PATH)
    packet = PACKET_MARKER in read_text(PACKET_PATH)
    rows.append({"validation_id": "VAL4677_4_markers", "passed": spine and packet, "detail": "spine and packet markers present" if spine and packet else "marker missing", "timestamp_utc": timestamp})
    pycache_absent = not (POST / "scripts" / "__pycache__").exists()
    rows.append({"validation_id": "VAL4677_5_pycache_absent", "passed": pycache_absent, "detail": "scripts __pycache__ absent" if pycache_absent else "scripts __pycache__ present", "timestamp_utc": timestamp})
    overall = source_ok and parse_ok and runner_ok and outputs_exist and claim_row and spine and packet and pycache_absent
    rows.append({"validation_id": "VAL4677_OVERALL", "passed": overall, "detail": "PASS" if overall else "FAIL", "timestamp_utc": timestamp})
    return rows


def write_documents(
    sources: list[dict[str, Any]],
    edges: list[dict[str, Any]],
    zeros: list[dict[str, Any]],
    survivors: list[dict[str, Any]],
    open_survivors: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    controls: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    statuses: list[dict[str, Any]],
    nexts: list[dict[str, Any]],
    validations: list[dict[str, Any]],
) -> None:
    body = f"""# 4677 - Y5/R2FR Visible EM Action Edge Parent Signature or Jsourceweight Bound Input

**Current verdict:** 4677 is a real narrowing step. It imports the already-derived fixed visible EM branch into the stricter 4676 source-weight language.

```text
J_source_weight_abs
  = |J_EM_fixed_source_weight|
  + |J_EM_open_dynamic|
  + |J_source_weight_nonEM|

Fixed visible EM branch:
J_EM_fixed_source_weight = 0

Therefore:
J_source_weight_abs_after_visible_EM
  = |J_EM_open_dynamic|
  + |J_source_weight_nonEM|.
```

This does **not** claim local GR, Newton, PPN or R10. It says the fixed q-basic same-Hodge static closed-collar visible EM contribution is no longer part of the dangerous source-weight vector. Open/dynamic EM and non-EM source-current/source-weight ownership remain live.

## Runner results

{table(runners)}

## Decision

{table(decisions)}

## Status

{table(statuses)}

## Next target

{table(nexts)}

## Visible EM edge import

{table(edges)}

## Fixed EM zero imported into source-weight vector

{table(zeros)}

## Jsourceweight after visible EM

{table(survivors)}

## Open EM and nonEM survivors

{table(open_survivors)}

## Bound input rows

{table(bounds)}

## Controls

{table(controls)}

## Source register

{table(sources)}

## Validation

{table(validations)}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4677 -", "# 693 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    if CLAIM_ID not in read_text(CLAIMS_PATH):
        append_once(
            CLAIMS_PATH,
            CLAIM_ID,
            csv_line(
                [
                    CLAIM_ID,
                    "local_gr_empirical_interface",
                    "4677 imports the fixed visible EM action edge into the 4676 source-weight vector: the fixed q-basic same-Hodge static closed-collar EM source-weight product is zero, Poynting is counted once as Hilbert stress flux, but open/dynamic EM and non-EM source-weight/current tails remain live.",
                    "Generated source register, visible EM edge import rows, fixed EM zero-to-source-weight rows, after-visible-EM source-weight vector, open/nonEM survivor rows, bound inputs, controls, runner, decision, status, next target and validation.",
                    DECISION.lower(),
                    NEXT_TARGET,
                    "Using the fixed EM zero outside the closed-collar branch, double-counting Poynting, treating visible EM as proof of non-EM source-current ownership, or claiming local GR/R10/PPN from this narrowing.",
                    "local_gr",
                    str(DOC_PATH),
                    NEXT_TARGET,
                    "No public local-GR/Newton/PPN/R10 claim until open/dynamic EM and non-EM source-weight/current tails are theorem-zero or source-backed bounded.",
                ]
            ),
        )

    append_once(
        SPINE_PATH,
        MARKER,
        f"""

## {MARKER}

4677 imports the fixed visible EM action edge into the current source-weight ladder:

```text
J_source_weight_abs_after_visible_EM
  = |J_EM_open_dynamic| + |J_source_weight_nonEM|
```

The fixed q-basic same-Hodge static closed-collar visible EM product is zero, and Poynting is counted once as Hilbert stress flux. This removes a real piece from the coupling problem, but open/dynamic EM and non-EM source-current/source-weight ownership remain blockers.

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

Packet update: the fixed visible EM branch has been wired into the `J_source_weight` vector. The next target is no longer “does EM/Poynting wreck this?” in the fixed branch; it is the open/dynamic EM tail plus non-EM source-charge/current ownership.

- claim id: `{CLAIM_ID}`
- fixed zero csv: `{FIXED_ZERO_CSV.name}`
- vector csv: `{SURVIVOR_CSV.name}`
- open survivor csv: `{OPEN_SURVIVOR_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def main() -> None:
    timestamp = now()
    sources = source_rows(timestamp)
    edges = edge_import_rows(timestamp)
    zeros = fixed_zero_rows(timestamp)
    survivors = survivor_rows(timestamp)
    open_survivors = open_survivor_rows(timestamp)
    bounds = bound_rows(timestamp)
    controls = control_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    nexts = next_rows(timestamp)
    runners = runner_rows(timestamp, sources, edges, zeros, survivors, open_survivors)

    csv_paths = [
        SOURCE_REGISTER,
        EDGE_IMPORT_CSV,
        FIXED_ZERO_CSV,
        SURVIVOR_CSV,
        OPEN_SURVIVOR_CSV,
        BOUND_INPUT_CSV,
        CONTROL_CSV,
        RUNNER_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]

    write_csv(SOURCE_REGISTER, sources)
    write_csv(EDGE_IMPORT_CSV, edges)
    write_csv(FIXED_ZERO_CSV, zeros)
    write_csv(SURVIVOR_CSV, survivors)
    write_csv(OPEN_SURVIVOR_CSV, open_survivors)
    write_csv(BOUND_INPUT_CSV, bounds)
    write_csv(CONTROL_CSV, controls)
    write_csv(RUNNER_CSV, runners)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_CSV, nexts)
    write_documents(sources, edges, zeros, survivors, open_survivors, bounds, controls, runners, decisions, statuses, nexts, [])
    update_registers(timestamp)
    cache = POST / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    validations = validation_rows(timestamp, csv_paths, sources, runners)
    write_csv(VALIDATION_CSV, validations)
    write_documents(sources, edges, zeros, survivors, open_survivors, bounds, controls, runners, decisions, statuses, nexts, validations)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
