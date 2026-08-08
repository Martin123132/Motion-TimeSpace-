from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3989"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3989-Y5-R2FR-matter-descent-no-source-prefactor-or-PPN-vector-fill.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3989_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3989_MATTER_DESCENT_NO_SOURCE_PREFACTOR_THEOREM.csv",
    "certificate": SRC / "P8_Y5_R2FR_3989_NO_SOURCE_PREFACTOR_CERTIFICATE.csv",
    "ppn_fill": SRC / "P8_Y5_R2FR_3989_FIRST_PPN_SOURCE_WEIGHT_FILL.csv",
    "bound_rows": SRC / "P8_Y5_R2FR_3989_DESCENT_PREFAC_PPN_BOUND_ROWS.csv",
    "runner_schema": SRC / "P8_Y5_R2FR_3989_DESCENT_PREFAC_PPN_RUNNER_SCHEMA.csv",
    "runner_smoke": SRC / "P8_Y5_R2FR_3989_DESCENT_PREFAC_PPN_SMOKE_RESULTS.csv",
    "projector": SRC / "P8_Y5_R2FR_3989_PROJECTOR_RESULTS.csv",
    "feed": SRC / "P8_Y5_R2FR_3989_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3989_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3989_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3989_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3989_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3989_VALIDATION.csv",
}

NEXT_DOC = "3990-Y5-R2FR-parent-action-grammar-no-hom-or-first-real-source-weight-bound.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3990_parent_action_grammar_no_hom_or_first_real_source_weight_bound.py"

CORE_FIELDS = [
    "R_matter_descent",
    "R_source_prefactor",
    "epsilon_no_hom_species_source",
    "epsilon_action_line_universality",
    "epsilon_readout_reentry",
]

PPN_SOURCE_FIELDS = [
    "delta_beta_source",
    "w_R_source",
    "epsilon_SN",
]

TAIL_FIELDS = [
    "epsilon_product_lock_total",
    "epsilon_extra_monopole_total",
    "R_coframe_descent",
    "R_Ward_exchange",
    "R_worldtube_support",
    "R_EM_Hilbert_descent",
    "R_nonHilbert_current",
    "epsilon_PPN_other",
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
        ("SRC3989_00_3988_next", SRC / "P8_Y5_R2FR_3988_NEXT_TARGET.csv", "NEXT3988_0", "3988 handoff"),
        ("SRC3989_01_3988_bound_matter", SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_BOUND_ROWS.csv", "JPPNB3988_4_R_matter_descent", "3988 matter descent residual"),
        ("SRC3989_02_3988_bound_prefac", SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_BOUND_ROWS.csv", "JPPNB3988_5_R_source_prefactor", "3988 source-prefactor residual"),
        ("SRC3989_03_3988_ppn", SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_BOUND_ROWS.csv", "JPPNB3988_14_w_R_source", "3988 PPN source weight component"),
        ("SRC3989_04_3988_theorem_prefac", SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_ORIGIN_AND_PPN_THEOREM.csv", "JPPN3988_2_prefactor_countermodel", "3988 prefactor countermodel"),
        ("SRC3989_05_3988_cert_origin", SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_CERTIFICATE.csv", "JPC3988_1_origin", "3988 JH origin certificate"),
        ("SRC3989_06_1720_def", SRC / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv", "JHT1720_0_definition", "observed Hilbert current definition"),
        ("SRC3989_07_1720_prefac", SRC / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv", "JHT1720_3_source_prefactor_countermodel", "source-prefactor countermodel"),
        ("SRC3989_08_SC0", SRC / "P8_source_current_Ward_universality_CONTRACT.csv", "SC0_single_observed_coframe_input", "single observed coframe"),
        ("SRC3989_09_SC1", SRC / "P8_source_current_Ward_universality_CONTRACT.csv", "SC1_Hilbert_source_definition", "Hilbert source definition"),
        ("SRC3989_10_SC3", SRC / "P8_source_current_Ward_universality_CONTRACT.csv", "SC3_universal_kappa_coupling", "universal source coupling"),
        ("SRC3989_11_EJR_Rmd", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_1_R_md", "matter descent/source multiplier obstruction"),
        ("SRC3989_12_EJR_Runits", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_8_R_units", "duplicate source unit normalization"),
        ("SRC3989_13_2465_matter", SRC / "P8_Y5_PARENT_ACTION_2465_SOURCE_CURRENT_DESCENT.csv", "SRC2465_0_matter_origin", "matter origin missing"),
        ("SRC3989_14_2465_univ", SRC / "P8_Y5_PARENT_ACTION_2465_SOURCE_CURRENT_DESCENT.csv", "SRC2465_5_universality", "universality missing"),
        ("SRC3989_15_2521_shadow", SRC / "P8_Y5_NO_SHADOW_2521_SOURCE_CURRENT_DESCENT_CONTRACT.csv", "SCC2521_3_source_shadow", "source shadow/no-source-only blocker"),
        ("SRC3989_16_2555_candidate", SRC / "P8_Y5_NO_SHADOW_2555_SOURCE_CURRENT_DESCENT.csv", "SRC2555_6_candidate_route", "constructive candidate route"),
        ("SRC3989_17_2631_wR", SRC / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv", "PPNV2631_4_wR", "PPN source weight component"),
        ("SRC3989_18_2500_wR", SRC / "P8_Y5_NO_SHADOW_2500_FULL_PPN_VECTOR_REQUIREMENTS.csv", "VREQ2500_4_wR_source", "wR source requirement"),
        ("SRC3989_19_2502_beta", SRC / "P8_Y5_NO_SHADOW_2502_NEWTON_PPN_COEFFICIENT_LAW.csv", "LAW2502_4_beta", "beta law"),
        ("SRC3989_20_2514_source", SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv", "DBETA2514_0_source", "finite beta source component"),
        ("SRC3989_21_2514_SN", SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv", "DBETA2514_5_SN", "source-normalization stability"),
        ("SRC3989_22_531_source", SRC / "P8_Y5_BETA_ENVELOPE_COMPONENTS.csv", "ENV531_1_source_AB", "beta source A/B component"),
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
            "theorem_id": "NP3989_0_no_prefactor_criterion",
            "claim_piece": "no-source-prefactor criterion",
            "mathematical_form": "If S_matter descends as a source-label-blind natural functor Sbar[q(Phi),psi,theta] with one observed coframe, no Hom(source/species/material label -> R_+ source weight), and no post-variation readout re-entry, then R_matter_descent=R_source_prefactor=0.",
            "derived_result": "the exact theorem condition for killing source-only active-mass weights is now written",
            "status": "NO_SOURCE_PREFACTOR_ZERO_CRITERION_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NP3989_1_countermodel_retained",
            "claim_piece": "source-prefactor countermodel",
            "mathematical_form": "S_ord=sum_A w_A S_A gives T_source=sum_A w_A T_A while ordinary equations can remain plausible; Ward conservation does not force w_A=1.",
            "derived_result": "matter descent cannot be claimed from Ward identity alone; the no-Hom/no-prefactor premise is essential",
            "status": "SOURCE_PREFACTOR_COUNTERMODEL_SURVIVES_UNTIL_PARENT_GRAMMAR_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NP3989_2_bound_split",
            "claim_piece": "descent/prefactor bound split",
            "mathematical_form": "epsilon_descent_prefactor_3989 <= |R_matter_descent| + |R_source_prefactor| + epsilon_no_hom_species_source + epsilon_action_line_universality + epsilon_readout_reentry",
            "derived_result": "the source-current origin threat is narrowed to a no-Hom grammar and action-line universality problem",
            "status": "DESCENT_PREFACTOR_BOUND_VECTOR_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NP3989_3_first_PPN_fill",
            "claim_piece": "first PPN source-weight fill",
            "mathematical_form": "w_R_source_3989 <= epsilon_descent_prefactor_3989 and delta_beta_source <= |w_R_source_3989| + |epsilon_SN|",
            "derived_result": "the first full-PPN source-weight row is connected to the source-current descent gate instead of left as an empty placeholder",
            "status": "FIRST_PPN_SOURCE_WEIGHT_FILL_DERIVED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "NP3989_4_master",
            "claim_piece": "3989 master residual",
            "mathematical_form": "epsilon_closed_source_failure_3989 <= epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_descent_prefactor_3989 + epsilon_PPN_rest_3989",
            "derived_result": "local source coupling now has a focused no-source-prefactor gate plus remaining PPN rest vector",
            "status": "MASTER_RESIDUAL_REDUCED_TO_NO_PREFACTOR_AND_PPN_REST",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    common = {"claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp}
    return [
        {
            "certificate_id": "NPC3989_0_criterion",
            "factor": "Z_no_source_prefactor_criterion",
            "3988_status": "OPEN_PARENT_ZERO_OR_NUMERIC_BOUND_REQUIRED",
            "3989_status": "EXACT_ZERO_CRITERION_AVAILABLE_NOT_PARENT_SIGNED",
            "content": "no Hom(source/species/material label -> source weight), one action line, one observed coframe, no readout re-entry",
            "remaining_gap": "parent action grammar must prove this is the only allowed matter descent",
            "source_path": str(SRC / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv"),
            **common,
        },
        {
            "certificate_id": "NPC3989_1_prefactor",
            "factor": "Z_source_prefactor_zero",
            "3988_status": "OPEN_PARENT_ZERO_OR_NUMERIC_BOUND_REQUIRED",
            "3989_status": "NOT_CLOSED_BUT_BOUNDABLE_BY_W_SOURCE",
            "content": "R_source_prefactor is represented by active-source weights w_A or source-label weights before variation",
            "remaining_gap": "real parent coefficient rows or no-Hom theorem required",
            "source_path": str(SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv"),
            **common,
        },
        {
            "certificate_id": "NPC3989_2_matter_descent",
            "factor": "Z_matter_descent",
            "3988_status": "OPEN_PARENT_ZERO_OR_NUMERIC_BOUND_REQUIRED",
            "3989_status": "NOT_CLOSED_BUT_GRAMMAR_CONTRACT_READY",
            "content": "R_matter_descent=0 if S_matter=Sbar[q(Phi),psi,theta] with same observed coframe and no source-only weights",
            "remaining_gap": "parent functor/action has not signed the descent grammar",
            "source_path": str(SRC / "P8_source_current_Ward_universality_CONTRACT.csv"),
            **common,
        },
        {
            "certificate_id": "NPC3989_3_ppn_source",
            "factor": "Z_PPN_source_weight_fill",
            "3988_status": "OPEN_PPN_ZERO_OR_NUMERIC_BOUND_REQUIRED",
            "3989_status": "FIRST_SOURCE_WEIGHT_COMPONENT_FILLED_NONCLAIM",
            "content": "w_R_source_3989 and delta_beta_source are now driven by epsilon_descent_prefactor_3989",
            "remaining_gap": "numeric values/theorem zeros still required before PPN pass",
            "source_path": str(SRC / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"),
            **common,
        },
        {
            "certificate_id": "NPC3989_4_total",
            "factor": "Z_closed_total_source_monopole",
            "3988_status": "FALSE_PRODUCT_EXTRA_SOURCE_DESCENT_PPN_OPEN",
            "3989_status": "FALSE_BUT_SOURCE_PREFAC_GATE_AND_FIRST_PPN_FILL_READY",
            "content": "epsilon_closed_source_failure_3989 is the current live local-GR source-coupling residual",
            "remaining_gap": "product lock, extra monopole, parent no-Hom grammar, and PPN rest vector",
            "source_path": str(SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_CERTIFICATE.csv"),
            **common,
        },
    ]


def ppn_fill_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "fill_id": "PPNF3989_0_wR_source",
            "ppn_component": "w_R_source",
            "source_driver": "epsilon_descent_prefactor_3989",
            "formula": "w_R_source_3989 <= |R_matter_descent| + |R_source_prefactor| + epsilon_no_hom_species_source + epsilon_action_line_universality + epsilon_readout_reentry",
            "status": "FIRST_SOURCE_WEIGHT_PPN_FILL_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "fill_id": "PPNF3989_1_delta_beta_source",
            "ppn_component": "delta_beta_source",
            "source_driver": "w_R_source_3989|epsilon_SN",
            "formula": "delta_beta_source_abs_3989 <= |w_R_source_3989| + |epsilon_SN|",
            "status": "BETA_SOURCE_COMPONENT_FILLED_FROM_SOURCE_WEIGHT_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "fill_id": "PPNF3989_2_ppn_rest",
            "ppn_component": "epsilon_PPN_rest_3989",
            "source_driver": "full_PPN_vector_minus_source_weight_fill",
            "formula": "epsilon_PPN_rest_3989 = epsilon_PPN_source_stability_3988 - filled_source_weight_part, kept as no-cancellation absolute remainder",
            "status": "PPN_REST_VECTOR_RETAINED",
            "source_path": str(SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_BOUND_ROWS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "NPB3989_0_master",
            "group": "master",
            "symbol": "epsilon_closed_source_failure_3989",
            "formula": "epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_descent_prefactor_3989 + epsilon_PPN_rest_3989",
            "status": "REDUCED_NO_PREFACTOR_PPN_FILL_VECTOR_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_BOUND_ROWS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NPB3989_1_descent_prefactor_total",
            "group": "descent_prefactor",
            "symbol": "epsilon_descent_prefactor_3989",
            "formula": "abs(R_matter_descent)+abs(R_source_prefactor)+epsilon_no_hom_species_source+epsilon_action_line_universality+epsilon_readout_reentry",
            "status": "EXACT_ABSOLUTE_DESCENT_PREFACTOR_BOUND_NONCLAIM",
            "source_path": str(SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NPB3989_2_ppn_source_fill",
            "group": "PPN_source_fill",
            "symbol": "w_R_source_3989",
            "formula": "epsilon_descent_prefactor_3989",
            "status": "FIRST_PPN_SOURCE_WEIGHT_FILL_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NPB3989_3_beta_source_fill",
            "group": "PPN_source_fill",
            "symbol": "delta_beta_source_abs_3989",
            "formula": "abs(w_R_source_3989)+abs(epsilon_SN)",
            "status": "BETA_SOURCE_FILL_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "NPB3989_4_ppn_rest",
            "group": "PPN_rest",
            "symbol": "epsilon_PPN_rest_3989",
            "formula": "abs(delta_p)+abs(b_R)+abs(Delta_beta_operator_q_boundary_readout_rest)+abs(d_R)+abs(epsilon_endpoint_R)+abs(alpha_readout_delta_GM)+abs(q_loc_Khat)",
            "status": "PPN_REST_RETAINED_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_BOUND_ROWS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]
    for index, symbol in enumerate(CORE_FIELDS, start=5):
        rows.append(
            {
                "row_id": f"NPB3989_{index}_{symbol}",
                "group": "descent_prefactor_component",
                "symbol": symbol,
                "formula": f"abs({symbol})",
                "status": "OPEN_NO_HOM_THEOREM_OR_NUMERIC_BOUND_REQUIRED",
                "source_path": str(SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv"),
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def runner_schema_rows(timestamp: str) -> list[dict[str, Any]]:
    fields = ["source_id", "epsilon_product_lock_total", "epsilon_extra_monopole_total", *CORE_FIELDS, "epsilon_SN", "epsilon_PPN_rest_3989", "epsilon_closed_source_failure_3989"]
    return [
        {
            "field": field,
            "required": field != "epsilon_closed_source_failure_3989",
            "units": "dimensionless" if field != "source_id" else "text",
            "description": "3989 no-prefactor/PPN-fill residual input or computed output",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for field in fields
    ]


def compute_residual(row: dict[str, Any]) -> tuple[str, str, str, str, str]:
    required = ["epsilon_product_lock_total", "epsilon_extra_monopole_total", *CORE_FIELDS, "epsilon_SN", "epsilon_PPN_rest_3989"]
    missing = [field for field in required if row.get(field, "") in {"", None, "MISSING"}]
    if missing:
        return ("BLOCKED_MISSING_INPUTS", "|".join(f"MISSING_{field}" for field in missing), "", "", "")
    try:
        descent_prefactor = sum(abs(float(row[field])) for field in CORE_FIELDS)
        w_source = descent_prefactor
        beta_source = w_source + abs(float(row["epsilon_SN"]))
        total = abs(float(row["epsilon_product_lock_total"])) + abs(float(row["epsilon_extra_monopole_total"])) + descent_prefactor + abs(float(row["epsilon_PPN_rest_3989"]))
    except ValueError as exc:
        return ("BLOCKED_NONNUMERIC_INPUT", str(exc), "", "", "")
    return ("COMPUTED_NONCLAIM", "numeric smoke computation only", f"{descent_prefactor:.12g}", f"{beta_source:.12g}", f"{total:.12g}")


def runner_smoke_rows(timestamp: str) -> list[dict[str, Any]]:
    fields = ["epsilon_product_lock_total", "epsilon_extra_monopole_total", *CORE_FIELDS, "epsilon_SN", "epsilon_PPN_rest_3989"]
    zero = {"source_id": "SMOKE3989_0_all_zero_no_prefactor"}
    for field in fields:
        zero[field] = "0"

    small = {"source_id": "SMOKE3989_1_small_no_prefactor_envelope"}
    for index, field in enumerate(fields, start=1):
        small[field] = f"{index}e-6"

    missing = {"source_id": "SMOKE3989_2_real_parent_rows_missing"}
    for field in fields:
        missing[field] = ""

    rows: list[dict[str, Any]] = []
    for row in [zero, small, missing]:
        status, blockers, descent, beta_source, total = compute_residual(row)
        rows.append(
            {
                **row,
                "epsilon_descent_prefactor_3989": descent,
                "delta_beta_source_abs_3989": beta_source,
                "epsilon_closed_source_failure_3989": total,
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
            "source_id": "REAL3989_0_controlled_EH_monopole_l2m0_no_prefactor_PPN_fill",
            "angular_projector_status": "PASS_LGE1_ANGULAR_ZERO",
            "Q_lm_residual": "0",
            "source_charge_residual_before": "epsilon_closed_source_failure_3988",
            "source_charge_residual_after": "epsilon_closed_source_failure_3989",
            "closed_or_reduced_in_3989": "no_source_prefactor_zero_criterion_written|descent_prefactor_bound_vector_ready|first_PPN_source_weight_fill_ready",
            "still_open": "epsilon_product_lock_total|epsilon_extra_monopole_total|epsilon_descent_prefactor_3989|epsilon_PPN_rest_3989",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "feed_id": "FEED3989_0",
            "target": "R_matter_descent|R_source_prefactor",
            "update": "reduced to no-Hom/no-source-prefactor grammar plus action-line universality/readout re-entry residuals",
            "status": "DESCENT_PREFACTOR_GATE_FACTORED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3989_1",
            "target": "w_R_source|delta_beta_source",
            "update": "first PPN source-weight fill now driven by epsilon_descent_prefactor_3989",
            "status": "FIRST_PPN_SOURCE_WEIGHT_FILL_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3989_2",
            "target": "epsilon_closed_source_failure_3988",
            "update": "reduced to epsilon_closed_source_failure_3989",
            "status": "MASTER_RESIDUAL_REDUCED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3989_0",
            "question": "is no-source-prefactor globally proved",
            "answer": "no",
            "reason": "the exact zero criterion is written, but parent action grammar has not excluded Hom(source/species/material label -> source weight)",
            "status": "NO_SOURCE_PREFACTOR_NOT_CLOSED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3989_1",
            "question": "did the source-weight PPN component move",
            "answer": "yes",
            "reason": "w_R_source and delta_beta_source now inherit the descent/prefactor vector instead of remaining blank placeholders",
            "status": "PPN_SOURCE_WEIGHT_COMPONENT_FILLED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3989_2",
            "question": "next best target",
            "answer": "prove no-Hom parent action grammar or source first real source-weight bound",
            "reason": "this is now the minimal route to remove source-prefactor freedom without faking local GR",
            "status": "MOVE_TO_NO_HOM_OR_REAL_SOURCE_WEIGHT_BOUND",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3989_0",
            "gate": "no-source-prefactor",
            "requirement": "no-Hom parent grammar or numeric source-weight residual below WEP/PPN/source bounds",
            "status": "BLOCKED_NO_HOM_GRAMMAR_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3989_1",
            "gate": "PPN source weight",
            "requirement": "w_R_source_3989 and delta_beta_source_abs_3989 zero or bounded",
            "status": "BLOCKED_PPN_SOURCE_WEIGHT_NUMERIC_ROWS_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3989_2",
            "gate": "local GR",
            "requirement": "product lock, extra monopole, no-source-prefactor, and PPN rest vector all pass",
            "status": "BLOCKED_LOCAL_GR_VECTOR_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3989_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "prove the no-Hom/no-source-prefactor parent action grammar or build the first real source-weight bound row",
            "success_condition": "R_source_prefactor or epsilon_no_hom_species_source is closed/bounded with source-backed rows and feeds w_R_source/delta_beta_source",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "NO_SOURCE_PREFACTOR_GATE_AND_FIRST_PPN_SOURCE_WEIGHT_FILL_READY",
            "strongest_result": "exact no-source-prefactor zero criterion derived; source-prefactor countermodel retained; descent/prefactor vector built; first PPN source-weight and beta-source rows filled nonclaim",
            "claim_status": "NONCLAIM_NO_HOM_GRAMMAR_AND_NUMERIC_SOURCE_WEIGHT_ROWS_OPEN",
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
        "ppn_fill": ppn_fill_rows(timestamp),
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
    return f"""# 3989 — Matter Descent No-Source-Prefactor Or PPN Vector Fill

Timestamp: `{timestamp}`

## Result

This checkpoint attacks the source-prefactor loophole.

The exact zero criterion is:

`S_matter = Sbar[q(Phi),psi,theta]`

with one observed coframe, no source/species/material-label homomorphism into a pre-action source weight, one action-density line, and no post-variation readout re-entry. Under that grammar,

`R_matter_descent = R_source_prefactor = 0`.

## Countermodel Guard

The global proof is not claimed. The countermodel still matters:

`S_ord=sum_A w_A S_A`

can leave ordinary matter equations plausible while changing active gravitational source weight. Ward conservation alone does not kill this.

## Bound Vector

`epsilon_descent_prefactor_3989 <= |R_matter_descent| + |R_source_prefactor| + epsilon_no_hom_species_source + epsilon_action_line_universality + epsilon_readout_reentry`.

## First PPN Fill

`w_R_source_3989 <= epsilon_descent_prefactor_3989`

and

`delta_beta_source_abs_3989 <= |w_R_source_3989| + |epsilon_SN|`.

This makes the PPN source-weight slot executable instead of a blank missing row.

## Master Residual

`epsilon_closed_source_failure_3989 <= epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_descent_prefactor_3989 + epsilon_PPN_rest_3989`.

## Source Register

{source_lines}

## Next Target

`{NEXT_DOC}`

Prove the no-Hom/no-source-prefactor parent action grammar, or source the first real source-weight bound row.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3989 - No-Source-Prefactor Gate And First PPN Fill"
    entry = f"""

{marker}

- Timestamp: `{timestamp}`
- Status: `NO_SOURCE_PREFACTOR_GATE_AND_FIRST_PPN_SOURCE_WEIGHT_FILL_READY`
- Exact zero criterion:
  if `S_matter=Sbar[q(Phi),psi,theta]` with one observed coframe, no source/species/material-label homomorphism into source weights, one action-density line, and no readout re-entry, then `R_matter_descent=R_source_prefactor=0`.
- Countermodel retained:
  `S_ord=sum_A w_A S_A` can change active source weight while keeping ordinary equations plausible.
- Bound vector:
  `epsilon_descent_prefactor_3989 <= |R_matter_descent| + |R_source_prefactor| + epsilon_no_hom_species_source + epsilon_action_line_universality + epsilon_readout_reentry`.
- First PPN fill:
  `w_R_source_3989 <= epsilon_descent_prefactor_3989`; `delta_beta_source_abs_3989 <= |w_R_source_3989| + |epsilon_SN|`.
- Current residual:
  `epsilon_closed_source_failure_3989 <= epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_descent_prefactor_3989 + epsilon_PPN_rest_3989`.
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
    ppn_fill = rows["ppn_fill"]
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
    cert_statuses = {str(row["3989_status"]) for row in certificate}
    ppn_statuses = {str(row["status"]) for row in ppn_fill}
    bound_symbols = {str(row["symbol"]) for row in bound_data}
    schema_fields = {str(row["field"]) for row in runner_schema}
    smoke_by_id = {str(row["source_id"]): row for row in runner_smoke}
    feed_statuses = {str(row["status"]) for row in feed}
    decision_statuses = {str(row["status"]) for row in decisions}
    claim_statuses = {str(row["status"]) for row in claims}
    project = projector[0]
    required_schema = {"source_id", "epsilon_product_lock_total", "epsilon_extra_monopole_total", *CORE_FIELDS, "epsilon_SN", "epsilon_PPN_rest_3989", "epsilon_closed_source_failure_3989"}
    required_symbols = {"epsilon_closed_source_failure_3989", "epsilon_descent_prefactor_3989", "w_R_source_3989", "delta_beta_source_abs_3989", "epsilon_PPN_rest_3989", *CORE_FIELDS}

    return [
        val("VAL3989_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3989_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3989_02_theorem_statuses", {"NO_SOURCE_PREFACTOR_ZERO_CRITERION_DERIVED", "SOURCE_PREFACTOR_COUNTERMODEL_SURVIVES_UNTIL_PARENT_GRAMMAR_SIGNED", "DESCENT_PREFACTOR_BOUND_VECTOR_DERIVED", "FIRST_PPN_SOURCE_WEIGHT_FILL_DERIVED_NONCLAIM", "MASTER_RESIDUAL_REDUCED_TO_NO_PREFACTOR_AND_PPN_REST"} <= theorem_statuses, "no-prefactor criterion, countermodel, bound, PPN fill, and master theorem rows present"),
        val("VAL3989_03_certificate_statuses", {"EXACT_ZERO_CRITERION_AVAILABLE_NOT_PARENT_SIGNED", "NOT_CLOSED_BUT_BOUNDABLE_BY_W_SOURCE", "NOT_CLOSED_BUT_GRAMMAR_CONTRACT_READY", "FIRST_SOURCE_WEIGHT_COMPONENT_FILLED_NONCLAIM", "FALSE_BUT_SOURCE_PREFAC_GATE_AND_FIRST_PPN_FILL_READY"} <= cert_statuses, "certificate captures no-prefactor progress and nonclaim state"),
        val("VAL3989_04_ppn_fill", {"FIRST_SOURCE_WEIGHT_PPN_FILL_NONCLAIM", "BETA_SOURCE_COMPONENT_FILLED_FROM_SOURCE_WEIGHT_NONCLAIM", "PPN_REST_VECTOR_RETAINED"} <= ppn_statuses, "PPN source-weight fill rows present"),
        val("VAL3989_05_bound_symbols", required_symbols <= bound_symbols, "descent/prefactor and PPN fill symbols present"),
        val("VAL3989_06_runner_schema", required_schema <= schema_fields, "runner schema has all required fields"),
        val("VAL3989_07_runner_zero", smoke_by_id["SMOKE3989_0_all_zero_no_prefactor"]["epsilon_closed_source_failure_3989"] == "0", "zero smoke computes zero"),
        val("VAL3989_08_runner_small_descent", smoke_by_id["SMOKE3989_1_small_no_prefactor_envelope"]["epsilon_descent_prefactor_3989"] == "2.5e-05", "small smoke descent/prefactor expected sum"),
        val("VAL3989_09_runner_small_total", smoke_by_id["SMOKE3989_1_small_no_prefactor_envelope"]["epsilon_closed_source_failure_3989"] == "3.7e-05", "small smoke total expected sum"),
        val("VAL3989_10_runner_blocks_missing", smoke_by_id["SMOKE3989_2_real_parent_rows_missing"]["runner_status"] == "BLOCKED_MISSING_INPUTS", "runner blocks missing parent rows"),
        val("VAL3989_11_projector_reduced", project["source_charge_residual_after"] == "epsilon_closed_source_failure_3989" and "epsilon_descent_prefactor_3989" in project["still_open"], "projector points at 3989 reduced residual"),
        val("VAL3989_12_feed", {"DESCENT_PREFACTOR_GATE_FACTORED", "FIRST_PPN_SOURCE_WEIGHT_FILL_READY", "MASTER_RESIDUAL_REDUCED_NONCLAIM"} <= feed_statuses, "feed rows capture 3989 reductions"),
        val("VAL3989_13_decision", {"NO_SOURCE_PREFACTOR_NOT_CLOSED", "PPN_SOURCE_WEIGHT_COMPONENT_FILLED_NONCLAIM", "MOVE_TO_NO_HOM_OR_REAL_SOURCE_WEIGHT_BOUND"} <= decision_statuses, "decision gate records current stance and next target"),
        val("VAL3989_14_claim_gate", {"BLOCKED_NO_HOM_GRAMMAR_UNSIGNED", "BLOCKED_PPN_SOURCE_WEIGHT_NUMERIC_ROWS_MISSING", "BLOCKED_LOCAL_GR_VECTOR_OPEN"} <= claim_statuses, "claim gates preserve remaining blocks"),
        val("VAL3989_15_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to no-Hom or real source-weight bound"),
        val("VAL3989_16_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3989_17_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3989_18_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3989_19_spine_updated", SPINE_PATH.exists() and "3989 - No-Source-Prefactor Gate And First PPN Fill" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3989_20_csv_parse", parsed, parse_detail),
        val("VAL3989_21_script_compile", True, "script compiled before validation write"),
        val("VAL3989_22_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
    ]


def run() -> None:
    timestamp = now_utc()
    rows = all_rows(timestamp)

    write_csv(OUTPUTS["sources"], rows["sources"])
    write_csv(OUTPUTS["theorem"], rows["theorem"])
    write_csv(OUTPUTS["certificate"], rows["certificate"])
    write_csv(OUTPUTS["ppn_fill"], rows["ppn_fill"])
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
    print(f"3989 validation passed: {len(validations)}/{len(validations)} checks")
    print(f"source needles: {sum(1 for row in rows['sources'] if row['needle_found'])}/{len(rows['sources'])}")
    print(rows["status"][0]["status"])


if __name__ == "__main__":
    run()
