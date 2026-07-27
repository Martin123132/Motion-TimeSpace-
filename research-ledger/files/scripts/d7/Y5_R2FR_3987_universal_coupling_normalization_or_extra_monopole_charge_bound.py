from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3987"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3987-Y5-R2FR-universal-coupling-normalization-or-extra-monopole-charge-bound.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3987_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3987_UNIVERSAL_COUPLING_AND_EXTRA_MONOPOLE_THEOREM.csv",
    "certificate": SRC / "P8_Y5_R2FR_3987_COUPLING_EXTRA_MONOPOLE_CERTIFICATE.csv",
    "bound_rows": SRC / "P8_Y5_R2FR_3987_COUPLING_EXTRA_MONOPOLE_BOUND_ROWS.csv",
    "runner_schema": SRC / "P8_Y5_R2FR_3987_COUPLING_EXTRA_MONOPOLE_RUNNER_SCHEMA.csv",
    "runner_smoke": SRC / "P8_Y5_R2FR_3987_COUPLING_EXTRA_MONOPOLE_SMOKE_RESULTS.csv",
    "projector": SRC / "P8_Y5_R2FR_3987_PROJECTOR_RESULTS.csv",
    "feed": SRC / "P8_Y5_R2FR_3987_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3987_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3987_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3987_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3987_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3987_VALIDATION.csv",
}

NEXT_DOC = "3988-Y5-R2FR-parent-source-current-origin-or-PPN-source-stability.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3988_parent_source_current_origin_or_PPN_source_stability.py"


PRODUCT_FIELDS = [
    "z_G",
    "z_w",
    "z_ellJ",
    "z_Rframe",
    "z_extra_product",
    "epsilon_Gref_match",
    "delta_kappa_source",
]

EXTRA_MONOPOLE_FIELDS = [
    "epsilon_boundary",
    "epsilon_domain_projector",
    "epsilon_bulk_X",
    "epsilon_nonEH_source",
    "epsilon_coupling_extra",
    "epsilon_species_A",
    "Delta_PiM",
    "A_parent",
    "epsilon_calibration",
]

TAIL_FIELDS = [
    "epsilon_parent_JH_origin",
    "epsilon_PPN_source_stability",
]


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC3987_00_3986_next", SRC / "P8_Y5_R2FR_3986_NEXT_TARGET.csv", "NEXT3986_0", "3986 handoff"),
        ("SRC3987_01_3986_master", SRC / "P8_Y5_R2FR_3986_GM_SOURCE_AMPLITUDE_BOUND_ROWS.csv", "GMA3986_0_master", "3986 amplitude master"),
        ("SRC3987_02_3986_universal_G", SRC / "P8_Y5_R2FR_3986_GM_SOURCE_AMPLITUDE_BOUND_ROWS.csv", "GMA3986_4_universal_G", "3986 universal G residual"),
        ("SRC3987_03_3986_extra", SRC / "P8_Y5_R2FR_3986_GM_SOURCE_AMPLITUDE_BOUND_ROWS.csv", "GMA3986_2_extra", "3986 extra monopole residual"),
        ("SRC3987_04_3986_cert_G", SRC / "P8_Y5_R2FR_3986_PIM_HILBERT_CERTIFICATE_UPDATE.csv", "PHC3986_4_universal_G", "3986 universal G certificate"),
        ("SRC3987_05_3986_cert_extra", SRC / "P8_Y5_R2FR_3986_PIM_HILBERT_CERTIFICATE_UPDATE.csv", "PHC3986_5_extra_monopole", "3986 extra monopole certificate"),
        ("SRC3987_06_constant_contract_CU1", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU1_global_coupling_status", "constant kappa global status"),
        ("SRC3987_07_constant_contract_CU7", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU7_measured_GM_product_silence", "measured GM product silence"),
        ("SRC3987_08_constant_contract_CU8", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU8_retained_residual_fallback", "coupling residual fallback"),
        ("SRC3987_09_kappa_top", SRC / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv", "T508_1_topological_zeroform", "topological kappa route"),
        ("SRC3987_10_kappa_residual", SRC / "P8_CONSTANT_KAPPA_RESIDUAL_MAP.csv", "KR508_5_Bianchi_exchange", "Bianchi exchange residual"),
        ("SRC3987_11_global_GS5", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS5_Bianchi_arbitrary_source_consistency", "Bianchi arbitrary source consistency"),
        ("SRC3987_12_global_GS6", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS6_constant_offset_policy", "constant offset policy"),
        ("SRC3987_13_delta_kappa", SRC / "P8_delta_kappa_source_exchange_residual.csv", "BK3048_0_bianchi_exchange_definition", "delta kappa source exchange"),
        ("SRC3987_14_GST3880_target", SRC / "P8_Y5_R2FR_3880_GEFF_DERIVATIVE_SILENCE_THEOREM.csv", "GST3880_0_target", "Geff derivative silence theorem"),
        ("SRC3987_15_GST3880_guard", SRC / "P8_Y5_R2FR_3880_GEFF_DERIVATIVE_SILENCE_THEOREM.csv", "GST3880_3_Bianchi_guard", "Bianchi/source-exchange guard"),
        ("SRC3987_16_GPL3600_product", SRC / "P8_Y5_R2FR_3600_GEFF_PRODUCT_LOCK_THEOREM.csv", "GPL3600_1_product_identity", "effective product identity"),
        ("SRC3987_17_GPL3600_conditional", SRC / "P8_Y5_R2FR_3600_GEFF_PRODUCT_LOCK_THEOREM.csv", "GPL3600_8_conditional_product_lock_theorem", "conditional product lock"),
        ("SRC3987_18_GPB3600_total", SRC / "P8_Y5_R2FR_3600_GEFF_PRODUCT_BOUND_ROWS.csv", "GPB3600_11_product_lock_total", "product lock total bound"),
        ("SRC3987_19_NEM3970_split", SRC / "P8_Y5_R2FR_3970_NO_EXTRA_MONOPOLE_THEOREM_OR_BOUND.csv", "NEM3970_0_split_identity", "extra monopole split"),
        ("SRC3987_20_NEM3970_bound", SRC / "P8_Y5_R2FR_3970_NO_EXTRA_MONOPOLE_THEOREM_OR_BOUND.csv", "NEM3970_2_no_cancellation_envelope", "absolute no-cancellation envelope"),
        ("SRC3987_21_CH3970_vector", SRC / "P8_Y5_R2FR_3970_EXTRA_MONOPOLE_CHANNEL_VECTOR.csv", "CH3970_8_calibration", "extra monopole channel vector"),
        ("SRC3987_22_HM4", SRC / "P8_Hilbert_monopole_calibration_CONTRACT.csv", "HM4_constant_universal_Geff", "Hilbert monopole constant Geff"),
        ("SRC3987_23_HM5", SRC / "P8_Hilbert_monopole_calibration_CONTRACT.csv", "HM5_zero_mu_extra", "Hilbert monopole extra charge"),
        ("SRC3987_24_EMV3501_extra", SRC / "P8_mu_extra_over_Geff_Meff_vector.csv", "EMV3501_11_absolute_calibration_offset", "mu extra calibration offset"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": exists,
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "UC3987_0_absolute_G_policy",
            "claim_piece": "absolute coupling value is calibration, not prediction",
            "mathematical_form": "if lambda_PiM_EH and kappa_eff are global source/range/time/frame/domain-blind constants, then lambda_PiM_EH*kappa_eff can be absorbed into the measured G_ref normalization",
            "derived_result": "local Newton/GR recovery does not require predicting the decimal value of G; it requires derivative/source/range silence of the effective coupling product",
            "status": "ABSOLUTE_G_VALUE_DEMOTED_TO_GLOBAL_CALIBRATION_POLICY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "UC3987_1_product_identity",
            "claim_piece": "universal coupling product bound",
            "mathematical_form": "D_X ln G_eff_product = z_G + z_w + z_ellJ + z_Rframe + z_extra_product + epsilon_Gref_match + delta_kappa_source",
            "derived_result": "epsilon_universal_G_normalization is replaced by an exact product-lock residual vector rather than an opaque coupling symbol",
            "status": "UNIVERSAL_COUPLING_PRODUCT_VECTOR_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "UC3987_2_kappa_zero_route",
            "claim_piece": "kappa derivative silence route",
            "mathematical_form": "if kappa_eff is a global/superselected or topological zero-form integration constant and carries no source/species/range/frame/domain labels, then D_X ln kappa_eff=0 and delta_kappa_source=0",
            "derived_result": "the kappa part has a clean derivation route, but current parent action has not signed it",
            "status": "KAPPA_ZERO_ROUTE_EXACT_BUT_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "UC3987_3_extra_monopole_envelope",
            "claim_piece": "extra monopole absolute envelope",
            "mathematical_form": "epsilon_extra_monopole_total = sum_i |epsilon_i| over boundary, domain, bulk/range, nonEH, coupling, frame/species, PiM, anomaly, and calibration channels",
            "derived_result": "Q_extra is bounded without sign-cancellation or hidden source normalization",
            "status": "EXTRA_MONOPOLE_ABSOLUTE_BOUND_VECTOR_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "UC3987_4_reduced_master",
            "claim_piece": "3987 source-coupling master residual",
            "mathematical_form": "epsilon_closed_source_failure_3987 <= epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_parent_JH_origin + epsilon_PPN_source_stability",
            "derived_result": "the remaining local Newton/GR source-coupling gate is now a product-lock plus extra-monopole bound problem",
            "status": "MASTER_RESIDUAL_REDUCED_TO_PRODUCT_AND_EXTRA_MONOPOLE_BOUNDS",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    common = {"claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp}
    return [
        {
            "certificate_id": "UCC3987_0_abs_G",
            "factor": "Z_absolute_G_not_predicted",
            "3986_status": "OPEN_INSIDE_AMPLITUDE",
            "3987_status": "CLOSED_AS_CALIBRATION_POLICY_IF_GLOBAL_CONSTANT",
            "content": "a global constant factor in kappa/lambda can set measured G_ref; derivative/source/range silence is the physics gate",
            "remaining_gap": "prove or bound the effective coupling product is constant and universal",
            "source_path": str(SRC / "P8_global_coupling_superselection_CONTRACT.csv"),
            **common,
        },
        {
            "certificate_id": "UCC3987_1_product_lock",
            "factor": "Z_universal_coupling_product_lock",
            "3986_status": "STILL_OPEN_NEXT_PRIMARY_TARGET",
            "3987_status": "NOT_CLOSED_EXACT_PRODUCT_BOUND_READY",
            "content": "epsilon_product_lock_total absolute-sums z_G, z_w, z_ellJ, z_Rframe, z_extra_product, epsilon_Gref_match, and delta_kappa_source",
            "remaining_gap": "all product factors must be parent-zero or numerically bounded; no fitted cancellation credited",
            "source_path": str(SRC / "P8_Y5_R2FR_3600_GEFF_PRODUCT_LOCK_THEOREM.csv"),
            **common,
        },
        {
            "certificate_id": "UCC3987_2_kappa_route",
            "factor": "Z_kappa_global_or_topological",
            "3986_status": "OPEN_INSIDE_UNIVERSAL_G",
            "3987_status": "EXACT_ZERO_ROUTE_AVAILABLE_NOT_PARENT_SIGNED",
            "content": "global/superselected kappa or topological zero-form route gives d kappa_eff=0 and kills delta_kappa_source",
            "remaining_gap": "parent action must actually include/adopt this mechanism",
            "source_path": str(SRC / "P8_CONSTANT_KAPPA_SUPERSELECTION_THEOREM.csv"),
            **common,
        },
        {
            "certificate_id": "UCC3987_3_extra_monopole",
            "factor": "Z_extra_monopole_charge_bound",
            "3986_status": "STILL_OPEN_EXPLICIT_Q_EXTRA_BOUND_ROW",
            "3987_status": "NOT_ZERO_BUT_ABSOLUTE_BOUND_VECTOR_READY",
            "content": "epsilon_extra_monopole_total=sum_i |epsilon_i| across nine source-channel rows",
            "remaining_gap": "channel zero theorems or real numeric/source bounds required before claim",
            "source_path": str(SRC / "P8_Y5_R2FR_3970_NO_EXTRA_MONOPOLE_THEOREM_OR_BOUND.csv"),
            **common,
        },
        {
            "certificate_id": "UCC3987_4_total",
            "factor": "Z_closed_total_source_monopole",
            "3986_status": "FALSE_BUT_REDUCED_TO_AMPLITUDE_SOURCE_VECTOR",
            "3987_status": "FALSE_BUT_REDUCED_TO_PRODUCT_LOCK_AND_EXTRA_MONOPOLE_BOUNDS",
            "content": "epsilon_closed_source_failure_3987 is the current live local source-coupling residual",
            "remaining_gap": "product-lock factors, extra monopole channels, parent JH origin, and PPN source stability",
            "source_path": str(SRC / "P8_Y5_R2FR_3986_PIM_HILBERT_CERTIFICATE_UPDATE.csv"),
            **common,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "CEM3987_0_master",
            "group": "master",
            "symbol": "epsilon_closed_source_failure_3987",
            "formula": "epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_parent_JH_origin + epsilon_PPN_source_stability",
            "status": "REDUCED_PRODUCT_PLUS_EXTRA_MONOPOLE_VECTOR_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3986_GM_SOURCE_AMPLITUDE_BOUND_ROWS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CEM3987_1_product_total",
            "group": "product_lock",
            "symbol": "epsilon_product_lock_total",
            "formula": "abs(z_G)+abs(z_w)+abs(z_ellJ)+abs(z_Rframe)+abs(z_extra_product)+abs(epsilon_Gref_match)+abs(delta_kappa_source)",
            "status": "EXACT_ABSOLUTE_PRODUCT_BOUND_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3600_GEFF_PRODUCT_BOUND_ROWS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CEM3987_2_extra_total",
            "group": "extra_monopole",
            "symbol": "epsilon_extra_monopole_total",
            "formula": "sum_abs(boundary,domain,bulk,nonEH,coupling,frame_species,PiM,anomaly,calibration)",
            "status": "EXACT_ABSOLUTE_EXTRA_MONOPOLE_BOUND_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3970_NO_EXTRA_MONOPOLE_THEOREM_OR_BOUND.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]
    for index, symbol in enumerate(PRODUCT_FIELDS, start=3):
        rows.append(
            {
                "row_id": f"CEM3987_{index}_{symbol}",
                "group": "product_lock_component",
                "symbol": symbol,
                "formula": f"abs({symbol})",
                "status": "OPEN_PARENT_ZERO_OR_NUMERIC_BOUND_REQUIRED",
                "source_path": str(SRC / "P8_Y5_R2FR_3600_GEFF_PRODUCT_BOUND_ROWS.csv"),
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    offset = 3 + len(PRODUCT_FIELDS)
    for index, symbol in enumerate(EXTRA_MONOPOLE_FIELDS, start=offset):
        rows.append(
            {
                "row_id": f"CEM3987_{index}_{symbol}",
                "group": "extra_monopole_component",
                "symbol": symbol,
                "formula": f"abs({symbol})",
                "status": "OPEN_CHANNEL_ZERO_OR_NUMERIC_BOUND_REQUIRED",
                "source_path": str(SRC / "P8_Y5_R2FR_3970_EXTRA_MONOPOLE_CHANNEL_VECTOR.csv"),
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def runner_schema_rows(timestamp: str) -> list[dict[str, Any]]:
    fields = ["source_id", *PRODUCT_FIELDS, *EXTRA_MONOPOLE_FIELDS, *TAIL_FIELDS, "epsilon_closed_source_failure_3987"]
    return [
        {
            "field": field,
            "required": field != "epsilon_closed_source_failure_3987",
            "units": "dimensionless" if field != "source_id" else "text",
            "description": "3987 product-lock/extra-monopole residual input or computed output",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for field in fields
    ]


def compute_residual(row: dict[str, Any]) -> tuple[str, str, str]:
    required = [*PRODUCT_FIELDS, *EXTRA_MONOPOLE_FIELDS, *TAIL_FIELDS]
    missing = [field for field in required if row.get(field, "") in {"", None, "MISSING"}]
    if missing:
        return ("BLOCKED_MISSING_INPUTS", "|".join(f"MISSING_{field}" for field in missing), "")
    try:
        value = sum(abs(float(row[field])) for field in required)
    except ValueError as exc:
        return ("BLOCKED_NONNUMERIC_INPUT", str(exc), "")
    return ("COMPUTED_NONCLAIM", "numeric smoke computation only", f"{value:.12g}")


def runner_smoke_rows(timestamp: str) -> list[dict[str, Any]]:
    zero = {"source_id": "SMOKE3987_0_all_zero_product_and_extra"}
    for field in [*PRODUCT_FIELDS, *EXTRA_MONOPOLE_FIELDS, *TAIL_FIELDS]:
        zero[field] = "0"

    small = {"source_id": "SMOKE3987_1_small_absolute_envelope"}
    all_fields = [*PRODUCT_FIELDS, *EXTRA_MONOPOLE_FIELDS, *TAIL_FIELDS]
    for index, field in enumerate(all_fields, start=1):
        small[field] = f"{index}e-6"

    missing = {"source_id": "SMOKE3987_2_real_parent_rows_missing"}
    for field in all_fields:
        missing[field] = ""

    rows: list[dict[str, Any]] = []
    for row in [zero, small, missing]:
        status, blockers, value = compute_residual(row)
        rows.append(
            {
                **row,
                "epsilon_closed_source_failure_3987": value,
                "runner_status": status,
                "blockers": blockers,
                "claim_allowed": False,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def projector_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "source_id": "REAL3987_0_controlled_EH_monopole_l2m0_product_extra_bound",
            "angular_projector_status": "PASS_LGE1_ANGULAR_ZERO",
            "Q_lm_residual": "0",
            "source_charge_residual_before": "epsilon_closed_source_failure_3986",
            "source_charge_residual_after": "epsilon_closed_source_failure_3987",
            "closed_or_reduced_in_3987": "absolute_G_value_demoted_to_calibration|universal_G_replaced_by_product_lock|Q_extra_replaced_by_channelwise_absolute_bound",
            "still_open": "epsilon_product_lock_total|epsilon_extra_monopole_total|epsilon_parent_JH_origin|epsilon_PPN_source_stability",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "feed_id": "FEED3987_0",
            "target": "epsilon_universal_G_normalization",
            "update": "replaced by exact product-lock residual vector; absolute G value is calibration only if global/source-blind",
            "status": "UNIVERSAL_G_REDUCED_TO_PRODUCT_LOCK",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3987_1",
            "target": "epsilon_extra_monopole_charge",
            "update": "replaced by nine-channel absolute no-cancellation envelope",
            "status": "EXTRA_MONOPOLE_BOUND_VECTOR_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3987_2",
            "target": "epsilon_closed_source_failure_3986",
            "update": "reduced to epsilon_closed_source_failure_3987",
            "status": "MASTER_RESIDUAL_REDUCED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3987_0",
            "question": "is absolute numerical G derivation required",
            "answer": "no",
            "reason": "a global constant coupling can be empirical calibration; local GR requires universal/source-blind derivative silence, not numerology",
            "status": "ABSOLUTE_G_NOT_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3987_1",
            "question": "can universal coupling be claimed",
            "answer": "no",
            "reason": "product-lock factors z_G, z_w, z_ellJ, z_Rframe, z_extra, Gref-match, and kappa exchange need parent zeros or numeric bounds",
            "status": "UNIVERSAL_COUPLING_STILL_BOUND_REQUIRED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3987_2",
            "question": "next best target",
            "answer": "parent source-current origin or PPN source stability",
            "reason": "the remaining source-coupling problem is now product-lock plus extra-monopole bounds plus parent JH/PPN",
            "status": "MOVE_TO_PARENT_JH_OR_PPN_STABILITY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3987_0",
            "gate": "universal coupling product",
            "requirement": "epsilon_product_lock_total=0 or source-backed bound below local arena target",
            "status": "BLOCKED_PRODUCT_LOCK_FACTORS_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3987_1",
            "gate": "extra monopole charge",
            "requirement": "all nine channels zero or epsilon_extra_monopole_total bounded",
            "status": "BLOCKED_EXTRA_MONOPOLE_CHANNELS_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3987_2",
            "gate": "local GR/PPN",
            "requirement": "product lock, extra monopole bound, parent JH origin, and PPN source stability",
            "status": "BLOCKED_PARENT_JH_AND_PPN_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3987_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive parent source-current origin or PPN source stability after universal coupling and extra-monopole residuals are made executable",
            "success_condition": "epsilon_parent_JH_origin or epsilon_PPN_source_stability is split/closed/bounded without hiding source-coupling failures",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "UNIVERSAL_COUPLING_PRODUCT_AND_EXTRA_MONOPOLE_BOUND_VECTOR_READY",
            "strongest_result": "absolute G value demoted to calibration; universal coupling becomes exact product-lock vector; extra monopole charge becomes nine-channel absolute bound; master source residual reduced to executable product/extra/JH/PPN vector",
            "claim_status": "NONCLAIM_PRODUCT_LOCK_EXTRA_MONOPOLE_PARENT_JH_PPN_OPEN",
            "next_target": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def all_rows(timestamp: str) -> dict[str, list[dict[str, Any]]]:
    return {
        "sources": source_register_rows(timestamp),
        "theorem": theorem_rows(timestamp),
        "certificate": certificate_rows(timestamp),
        "bound_rows": bound_rows(timestamp),
        "runner_schema": runner_schema_rows(timestamp),
        "runner_smoke": runner_smoke_rows(timestamp),
        "projector": projector_rows(timestamp),
        "feed": feed_rows(timestamp),
        "decision": decision_rows(timestamp),
        "claim_gate": claim_gate_rows(timestamp),
        "next": next_rows(timestamp),
        "status": status_rows(timestamp),
    }


def doc_text(timestamp: str, sources: list[dict[str, Any]]) -> str:
    source_lines = "\n".join(
        f"- `{row['source_id']}`: `{row['path']}` needle `{row['needle']}` found={row['needle_found']}"
        for row in sources
    )
    return f"""# 3987 — Universal Coupling Normalization Or Extra Monopole Charge Bound

Timestamp: `{timestamp}`

## Result

This checkpoint makes the coupling problem sharper.

The numerical value of `G` does not have to be derived for a GR/Newton recovery branch. A global constant coupling can be empirical calibration. What must be derived or bounded is that the effective coupling is constant, universal, source-blind, range-blind, and frame-blind.

So `epsilon_universal_G_normalization` is replaced by the product-lock vector

`epsilon_product_lock_total = |z_G| + |z_w| + |z_ellJ| + |z_Rframe| + |z_extra_product| + |epsilon_Gref_match| + |delta_kappa_source|`.

The extra monopole charge is replaced by the no-cancellation channel envelope

`epsilon_extra_monopole_total = sum_i |epsilon_i|`.

## New Master Residual

`epsilon_closed_source_failure_3987 <= epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_parent_JH_origin + epsilon_PPN_source_stability`.

That is the live source-coupling gate now.

## Nonclaim Guard

The kappa/global-coupling route has an exact conditional derivation through superselection or a topological zero-form, but the parent action has not signed that mechanism. Product factors and extra-monopole channels therefore remain executable bound rows, not claims.

## Runner

`P8_Y5_R2FR_3987_COUPLING_EXTRA_MONOPOLE_SMOKE_RESULTS.csv` computes the product-plus-extra envelope and blocks real rows when parent inputs are missing.

## Source Register

{source_lines}

## Next Target

`{NEXT_DOC}`

Attack parent source-current origin or PPN source stability next.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3987 - Universal Coupling Product And Extra Monopole Bound"
    entry = f"""

{marker}

- Timestamp: `{timestamp}`
- Status: `UNIVERSAL_COUPLING_PRODUCT_AND_EXTRA_MONOPOLE_BOUND_VECTOR_READY`
- Main derivation:
  absolute numerical `G` is not the local-GR recovery target; if it is a global source-blind constant, it is calibration. The physics gate is the product-lock residual.
- Product lock:
  `epsilon_product_lock_total = |z_G| + |z_w| + |z_ellJ| + |z_Rframe| + |z_extra_product| + |epsilon_Gref_match| + |delta_kappa_source|`.
- Extra monopole:
  `epsilon_extra_monopole_total = sum_i |epsilon_i|` over the nine 3970 channels, with no sign-cancellation credit.
- Current residual:
  `epsilon_closed_source_failure_3987 <= epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_parent_JH_origin + epsilon_PPN_source_stability`.
- Still nonclaim:
  parent product-lock zeros, extra-channel zeros/bounds, parent `J_H`, and PPN source stability remain open.
- Next: `{NEXT_DOC}`.
"""
    existing = read_text(SPINE_PATH) if SPINE_PATH.exists() else "# Local GR Coupling Spine Current State\n"
    if marker not in existing:
        SPINE_PATH.write_text(existing.rstrip() + entry + "\n", encoding="utf-8")


def validation_rows(timestamp: str, rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    generated_csvs = [path for key, path in OUTPUTS.items() if key != "validation"]
    sources = rows["sources"]
    theorem = rows["theorem"]
    certificate = rows["certificate"]
    bound_data = rows["bound_rows"]
    runner_schema = rows["runner_schema"]
    runner_smoke = rows["runner_smoke"]
    projector = rows["projector"]
    feed = rows["feed"]
    decisions = rows["decision"]
    claims = rows["claim_gate"]
    next_target = rows["next"]

    def val(validation_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "validation_id": validation_id,
            "passed": bool(passed),
            "detail": detail,
            "timestamp_utc": timestamp,
        }

    parsed = True
    parse_detail = "generated CSV files parse cleanly"
    for path in generated_csvs:
        try:
            read_csv(path)
        except Exception as exc:
            parsed = False
            parse_detail = f"{path} failed to parse: {exc}"
            break

    theorem_statuses = {str(row["status"]) for row in theorem}
    cert_statuses = {str(row["3987_status"]) for row in certificate}
    bound_symbols = {str(row["symbol"]) for row in bound_data}
    schema_fields = {str(row["field"]) for row in runner_schema}
    smoke_by_id = {str(row["source_id"]): row for row in runner_smoke}
    feed_statuses = {str(row["status"]) for row in feed}
    decision_statuses = {str(row["status"]) for row in decisions}
    claim_statuses = {str(row["status"]) for row in claims}
    project = projector[0]
    required_schema = {"source_id", *PRODUCT_FIELDS, *EXTRA_MONOPOLE_FIELDS, *TAIL_FIELDS, "epsilon_closed_source_failure_3987"}
    required_symbols = {"epsilon_closed_source_failure_3987", "epsilon_product_lock_total", "epsilon_extra_monopole_total", *PRODUCT_FIELDS, *EXTRA_MONOPOLE_FIELDS}

    return [
        val("VAL3987_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3987_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3987_02_theorem_statuses", {"ABSOLUTE_G_VALUE_DEMOTED_TO_GLOBAL_CALIBRATION_POLICY", "UNIVERSAL_COUPLING_PRODUCT_VECTOR_DERIVED", "KAPPA_ZERO_ROUTE_EXACT_BUT_NOT_PARENT_SIGNED", "EXTRA_MONOPOLE_ABSOLUTE_BOUND_VECTOR_DERIVED", "MASTER_RESIDUAL_REDUCED_TO_PRODUCT_AND_EXTRA_MONOPOLE_BOUNDS"} <= theorem_statuses, "G policy, product vector, kappa route, extra bound, and master residual rows present"),
        val("VAL3987_03_certificate_statuses", {"CLOSED_AS_CALIBRATION_POLICY_IF_GLOBAL_CONSTANT", "NOT_CLOSED_EXACT_PRODUCT_BOUND_READY", "EXACT_ZERO_ROUTE_AVAILABLE_NOT_PARENT_SIGNED", "NOT_ZERO_BUT_ABSOLUTE_BOUND_VECTOR_READY", "FALSE_BUT_REDUCED_TO_PRODUCT_LOCK_AND_EXTRA_MONOPOLE_BOUNDS"} <= cert_statuses, "certificate captures calibration closure and remaining bound rows"),
        val("VAL3987_04_bound_symbols", required_symbols <= bound_symbols, "all product and extra-monopole bound symbols present"),
        val("VAL3987_05_runner_schema", required_schema <= schema_fields, "runner schema has product, extra, tail, and output fields"),
        val("VAL3987_06_runner_zero", smoke_by_id["SMOKE3987_0_all_zero_product_and_extra"]["epsilon_closed_source_failure_3987"] == "0", "zero smoke computes zero"),
        val("VAL3987_07_runner_small", smoke_by_id["SMOKE3987_1_small_absolute_envelope"]["epsilon_closed_source_failure_3987"] == "0.000171", "small smoke computes expected absolute envelope"),
        val("VAL3987_08_runner_blocks_missing", smoke_by_id["SMOKE3987_2_real_parent_rows_missing"]["runner_status"] == "BLOCKED_MISSING_INPUTS", "runner blocks missing parent rows"),
        val("VAL3987_09_projector_reduced", project["source_charge_residual_after"] == "epsilon_closed_source_failure_3987" and "epsilon_product_lock_total" in project["still_open"], "projector points at product/extra residual"),
        val("VAL3987_10_feed", {"UNIVERSAL_G_REDUCED_TO_PRODUCT_LOCK", "EXTRA_MONOPOLE_BOUND_VECTOR_READY", "MASTER_RESIDUAL_REDUCED_NONCLAIM"} <= feed_statuses, "feed rows capture 3987 reductions"),
        val("VAL3987_11_decision", {"ABSOLUTE_G_NOT_REQUIRED", "UNIVERSAL_COUPLING_STILL_BOUND_REQUIRED", "MOVE_TO_PARENT_JH_OR_PPN_STABILITY"} <= decision_statuses, "decision gate records current stance and next target"),
        val("VAL3987_12_claim_gate", {"BLOCKED_PRODUCT_LOCK_FACTORS_OPEN", "BLOCKED_EXTRA_MONOPOLE_CHANNELS_OPEN", "BLOCKED_PARENT_JH_AND_PPN_OPEN"} <= claim_statuses, "claim gates preserve remaining blocks"),
        val("VAL3987_13_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to parent JH or PPN stability"),
        val("VAL3987_14_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3987_15_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3987_16_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3987_17_spine_updated", SPINE_PATH.exists() and "3987 - Universal Coupling Product And Extra Monopole Bound" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3987_18_csv_parse", parsed, parse_detail),
        val("VAL3987_19_script_compile", True, "script compiled before validation write"),
        val("VAL3987_20_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["theorem"], rows["theorem"])
    write_csv(OUTPUTS["certificate"], rows["certificate"])
    write_csv(OUTPUTS["bound_rows"], rows["bound_rows"])
    write_csv(OUTPUTS["runner_schema"], rows["runner_schema"])
    write_csv(OUTPUTS["runner_smoke"], rows["runner_smoke"])
    write_csv(OUTPUTS["projector"], rows["projector"])
    write_csv(OUTPUTS["feed"], rows["feed"])
    write_csv(OUTPUTS["decision"], rows["decision"])
    write_csv(OUTPUTS["claim_gate"], rows["claim_gate"])
    write_csv(OUTPUTS["next"], rows["next"])
    write_csv(OUTPUTS["status"], rows["status"])

    DOC_PATH.write_text(doc_text(timestamp, rows["sources"]), encoding="utf-8")
    update_spine(timestamp)

    py_compile.compile(str(SCRIPT_PATH), doraise=True)
    pycache = SCRIPT_PATH.parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)

    validations = validation_rows(timestamp, rows)
    write_csv(OUTPUTS["validation"], validations)
    failed = [row for row in validations if not row["passed"]]
    if failed:
        for row in failed:
            print(f"FAILED {row['validation_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"3987 validation passed: {len(validations)}/{len(validations)} checks")
    print(f"source needles: {sum(1 for row in rows['sources'] if row['needle_found'])}/{len(rows['sources'])}")
    print(rows["status"][0]["status"])


if __name__ == "__main__":
    run()
