from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3988"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3988-Y5-R2FR-parent-source-current-origin-or-PPN-source-stability.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_3988_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_ORIGIN_AND_PPN_THEOREM.csv",
    "certificate": SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_CERTIFICATE.csv",
    "bound_rows": SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_BOUND_ROWS.csv",
    "runner_schema": SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_RUNNER_SCHEMA.csv",
    "runner_smoke": SRC / "P8_Y5_R2FR_3988_SOURCE_CURRENT_PPN_SMOKE_RESULTS.csv",
    "projector": SRC / "P8_Y5_R2FR_3988_PROJECTOR_RESULTS.csv",
    "feed": SRC / "P8_Y5_R2FR_3988_FEED_UPDATE.csv",
    "decision": SRC / "P8_Y5_R2FR_3988_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_3988_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_3988_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_3988_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_3988_VALIDATION.csv",
}

NEXT_DOC = "3989-Y5-R2FR-matter-descent-no-source-prefactor-or-PPN-vector-fill.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_3989_matter_descent_no_source_prefactor_or_PPN_vector_fill.py"

SOURCE_CURRENT_FIELDS = [
    "R_coframe_descent",
    "R_matter_descent",
    "R_source_prefactor",
    "R_Ward_exchange",
    "R_worldtube_support",
    "R_EM_Hilbert_descent",
    "R_nonHilbert_current",
]

PPN_FIELDS = [
    "delta_p",
    "b_R",
    "Delta_beta_total_abs",
    "d_R",
    "w_R_source",
    "epsilon_endpoint_R",
    "alpha_readout_delta_GM",
    "q_loc_Khat",
]

TAIL_FIELDS = [
    "epsilon_product_lock_total",
    "epsilon_extra_monopole_total",
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
        ("SRC3988_00_3987_next", SRC / "P8_Y5_R2FR_3987_NEXT_TARGET.csv", "NEXT3987_0", "3987 handoff"),
        ("SRC3988_01_3987_master", SRC / "P8_Y5_R2FR_3987_COUPLING_EXTRA_MONOPOLE_BOUND_ROWS.csv", "CEM3987_0_master", "3987 master residual"),
        ("SRC3988_02_3987_cert_total", SRC / "P8_Y5_R2FR_3987_COUPLING_EXTRA_MONOPOLE_CERTIFICATE.csv", "UCC3987_4_total", "3987 total certificate"),
        ("SRC3988_03_3987_theorem", SRC / "P8_Y5_R2FR_3987_UNIVERSAL_COUPLING_AND_EXTRA_MONOPOLE_THEOREM.csv", "UC3987_4_reduced_master", "3987 reduced master theorem"),
        ("SRC3988_04_3987_projector", SRC / "P8_Y5_R2FR_3987_PROJECTOR_RESULTS.csv", "REAL3987_0_controlled_EH_monopole_l2m0_product_extra_bound", "3987 controlled projector"),
        ("SRC3988_05_SC1", SRC / "P8_source_current_Ward_universality_CONTRACT.csv", "SC1_Hilbert_source_definition", "Hilbert source definition"),
        ("SRC3988_06_SC2", SRC / "P8_source_current_Ward_universality_CONTRACT.csv", "SC2_Ward_conservation_on_matter_shell", "Ward conservation"),
        ("SRC3988_07_SC8", SRC / "P8_source_current_Ward_universality_CONTRACT.csv", "SC8_second_order_source_stability", "second-order source stability"),
        ("SRC3988_08_ellJ_total", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_0_total", "source-current normalization decomposition"),
        ("SRC3988_09_ellJ_md", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_1_R_md", "matter descent obstruction"),
        ("SRC3988_10_ellJ_Ward", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_2_R_Ward", "Ward projection obstruction"),
        ("SRC3988_11_ellJ_PiM", SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv", "EJR3513_3_R_PiM", "PiM commutator obstruction"),
        ("SRC3988_12_parent_action_matter", SRC / "P8_Y5_PARENT_ACTION_2465_SOURCE_CURRENT_DESCENT.csv", "SRC2465_0_matter_origin", "parent action source-current missing"),
        ("SRC3988_13_parent_action_route", SRC / "P8_Y5_PARENT_ACTION_2465_SOURCE_CURRENT_DESCENT.csv", "SRC2465_6_candidate_route", "constructive route"),
        ("SRC3988_14_JH_def", SRC / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv", "JHT1720_0_definition", "observed Hilbert current definition"),
        ("SRC3988_15_JH_prefactor", SRC / "P8_Y5_PARENT_QLOC_1720_JH_CURRENT_DEFINITION_THEOREM.csv", "JHT1720_3_source_prefactor_countermodel", "source-prefactor countermodel"),
        ("SRC3988_16_JH_Hilbert", SRC / "P8_Y5_R2FR_3408_JH_HILBERT_SOURCE_DERIVATION.csv", "JH3408_0_variation", "Hilbert variation formula"),
        ("SRC3988_17_JH_EM", SRC / "P8_Y5_R2FR_3408_JH_HILBERT_SOURCE_DERIVATION.csv", "JH3408_2_EM_Poynting", "EM/Poynting Hilbert inclusion"),
        ("SRC3988_18_HWT_parent_frame", SRC / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv", "PAC537_1_single_observed_source_frame", "single observed source frame"),
        ("SRC3988_19_HWT_PPN", SRC / "P8_Y5_HILBERT_WORLDTUBE_PARENT_ACTION_CONTRACT.csv", "PAC537_9_second_order_PPN_stability", "parent PPN stability"),
        ("SRC3988_20_PPN_total", SRC / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv", "PPNV2631_8_total_abs", "full PPN vector total"),
        ("SRC3988_21_PPN_requirements", SRC / "P8_Y5_NO_SHADOW_2500_FULL_PPN_VECTOR_REQUIREMENTS.csv", "VREQ2500_6_total_no_cancellation", "full PPN no-cancellation requirement"),
        ("SRC3988_22_PPN_law_beta", SRC / "P8_Y5_NO_SHADOW_2502_NEWTON_PPN_COEFFICIENT_LAW.csv", "LAW2502_4_beta", "beta coefficient law"),
        ("SRC3988_23_beta_total", SRC / "P8_Y5_NO_SHADOW_2514_FINITE_BETA_SOURCE_VECTOR.csv", "DBETA2514_6_total_abs", "finite beta source vector"),
        ("SRC3988_24_beta_decision", SRC / "P8_Y5_BETA_ENVELOPE_DECISION.csv", "D531_3_next_target", "measured-GM source-current closure target"),
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
            "theorem_id": "JPPN3988_0_Hilbert_formula",
            "claim_piece": "source-current formula",
            "mathematical_form": "if S_matter+S_EM descends to one observed coframe/metric before readout, then T_total^{mu nu}=(-2/sqrt(-g_obs)) delta(S_matter+S_EM)/delta g_obs_munu and J_H[tau]=star(T_total(tau,.))",
            "derived_result": "the ordinary matter+EM Hilbert current formula is exact conditional structure, not a fitted source slot",
            "status": "CONDITIONAL_HILBERT_SOURCE_FORMULA_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JPPN3988_1_origin_split",
            "claim_piece": "parent source-current origin split",
            "mathematical_form": "epsilon_parent_JH_origin <= R_coframe_descent + R_matter_descent + R_source_prefactor + R_Ward_exchange + R_worldtube_support + R_EM_Hilbert_descent + R_nonHilbert_current",
            "derived_result": "source-current origin is split into seven executable nonclaim gates",
            "status": "PARENT_JH_ORIGIN_BOUND_VECTOR_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JPPN3988_2_prefactor_countermodel",
            "claim_piece": "no-source-prefactor guard",
            "mathematical_form": "S_ord=sum_A w_A S_A leaves ordinary equations possible while active source becomes T_source=sum_A w_A T_A unless w_A is parent-forbidden or universal",
            "derived_result": "a Ward identity alone cannot prove source-current origin; no-source-prefactor/descent is an independent gate",
            "status": "SOURCE_PREFACTOR_COUNTERMODEL_RETAINED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JPPN3988_3_PPN_envelope",
            "claim_piece": "PPN source stability envelope",
            "mathematical_form": "epsilon_PPN_source_stability <= |delta_p|+|b_R|+|Delta_beta_total_abs|+|d_R|+|w_R_source|+|epsilon_endpoint_R|+|alpha_readout_delta_GM|+|q_loc_Khat|",
            "derived_result": "PPN stability is kept as a full absolute vector; beta/Newton shape cannot promote local GR alone",
            "status": "PPN_SOURCE_STABILITY_ABSOLUTE_VECTOR_DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "JPPN3988_4_master",
            "claim_piece": "3988 master residual",
            "mathematical_form": "epsilon_closed_source_failure_3988 <= epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_parent_JH_origin_3988 + epsilon_PPN_source_stability_3988",
            "derived_result": "local GR source coupling now depends on product/extra bounds plus a precise source-current descent gate and full PPN envelope",
            "status": "MASTER_RESIDUAL_REDUCED_TO_SOURCE_DESCENT_AND_PPN_VECTOR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def certificate_rows(timestamp: str) -> list[dict[str, Any]]:
    common = {"claim_allowed": False, "valid_for_claim": False, "timestamp_utc": timestamp}
    return [
        {
            "certificate_id": "JPC3988_0_formula",
            "factor": "Z_Hilbert_source_formula",
            "3987_status": "OPEN_PARENT_JH_ORIGIN",
            "3988_status": "FORMULA_DERIVED_CONDITIONAL_ON_DESCENT",
            "content": "variation of descended matter+EM action defines T_total and J_H[tau]",
            "remaining_gap": "parent action must sign one observed coframe, no source-only weights, support/worldtube ownership, and non-Hilbert silence",
            "source_path": str(SRC / "P8_Y5_R2FR_3408_JH_HILBERT_SOURCE_DERIVATION.csv"),
            **common,
        },
        {
            "certificate_id": "JPC3988_1_origin",
            "factor": "Z_parent_JH_origin",
            "3987_status": "STILL_OPEN_PARENT_JH_ORIGIN",
            "3988_status": "NOT_CLOSED_BUT_SEVEN_GATE_BOUND_VECTOR_READY",
            "content": "epsilon_parent_JH_origin_3988 is the absolute sum of coframe, matter descent, source-prefactor, Ward, worldtube, EM descent, and non-Hilbert current gates",
            "remaining_gap": "R_matter_descent and R_source_prefactor are the sharpest next targets",
            "source_path": str(SRC / "P8_source_current_Ward_universality_CONTRACT.csv"),
            **common,
        },
        {
            "certificate_id": "JPC3988_2_PPN",
            "factor": "Z_PPN_source_stability",
            "3987_status": "STILL_OPEN_PPN_SOURCE_STABILITY",
            "3988_status": "NOT_CLOSED_FULL_PPN_ABSOLUTE_VECTOR_READY",
            "content": "epsilon_PPN_source_stability_3988 is the absolute full-PPN envelope including beta/source/readout/q_loc channels",
            "remaining_gap": "component theorem-zeros or numeric/source-backed values required before local GR claim",
            "source_path": str(SRC / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"),
            **common,
        },
        {
            "certificate_id": "JPC3988_3_EM",
            "factor": "Z_EM_Hilbert_descent",
            "3987_status": "PART_OF_PARENT_JH_ORIGIN",
            "3988_status": "CONDITIONAL_EM_STRESS_INCLUDED_IF_MAXWELL_DESCENT_SIGNED",
            "content": "ordinary Maxwell/Poynting stress belongs in T_total, not hidden mu_extra, once EM descends to the same observed metric",
            "remaining_gap": "MTS/emergent EM parent descent and nonminimal cross-terms remain separate coefficients",
            "source_path": str(SRC / "P8_Y5_R2FR_3408_JH_HILBERT_SOURCE_DERIVATION.csv"),
            **common,
        },
        {
            "certificate_id": "JPC3988_4_total",
            "factor": "Z_closed_total_source_monopole",
            "3987_status": "FALSE_PRODUCT_EXTRA_PARENT_JH_PPN_OPEN",
            "3988_status": "FALSE_BUT_REDUCED_TO_PRODUCT_EXTRA_SOURCE_DESCENT_PPN_VECTOR",
            "content": "epsilon_closed_source_failure_3988 is the current live local-GR source-coupling residual",
            "remaining_gap": "product lock, extra monopole bound, source-current descent, and full PPN stability",
            "source_path": str(SRC / "P8_Y5_R2FR_3987_COUPLING_EXTRA_MONOPOLE_CERTIFICATE.csv"),
            **common,
        },
    ]


def bound_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        {
            "row_id": "JPPNB3988_0_master",
            "group": "master",
            "symbol": "epsilon_closed_source_failure_3988",
            "formula": "epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_parent_JH_origin_3988 + epsilon_PPN_source_stability_3988",
            "status": "REDUCED_SOURCE_CURRENT_PPN_VECTOR_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_R2FR_3987_COUPLING_EXTRA_MONOPOLE_BOUND_ROWS.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JPPNB3988_1_JH_total",
            "group": "source_current_origin",
            "symbol": "epsilon_parent_JH_origin_3988",
            "formula": "sum_abs(source_current_origin_components)",
            "status": "EXACT_ABSOLUTE_SOURCE_CURRENT_BOUND_NONCLAIM",
            "source_path": str(SRC / "P8_source_current_Ward_universality_CONTRACT.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "JPPNB3988_2_PPN_total",
            "group": "PPN_source_stability",
            "symbol": "epsilon_PPN_source_stability_3988",
            "formula": "sum_abs(full_PPN_components)",
            "status": "EXACT_ABSOLUTE_PPN_BOUND_NONCLAIM",
            "source_path": str(SRC / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"),
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]
    for index, symbol in enumerate(SOURCE_CURRENT_FIELDS, start=3):
        rows.append(
            {
                "row_id": f"JPPNB3988_{index}_{symbol}",
                "group": "source_current_component",
                "symbol": symbol,
                "formula": f"abs({symbol})",
                "status": "OPEN_PARENT_ZERO_OR_NUMERIC_BOUND_REQUIRED",
                "source_path": str(SRC / "P8_EM_ellJ_source_current_owner_residual_law.csv"),
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    offset = 3 + len(SOURCE_CURRENT_FIELDS)
    for index, symbol in enumerate(PPN_FIELDS, start=offset):
        rows.append(
            {
                "row_id": f"JPPNB3988_{index}_{symbol}",
                "group": "PPN_component",
                "symbol": symbol,
                "formula": f"abs({symbol})",
                "status": "OPEN_PPN_ZERO_OR_NUMERIC_BOUND_REQUIRED",
                "source_path": str(SRC / "P8_Y5_NO_SHADOW_PPN_VECTOR_2631_FULL_PPN_VECTOR_LEDGER.csv"),
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def runner_schema_rows(timestamp: str) -> list[dict[str, Any]]:
    fields = ["source_id", *TAIL_FIELDS, *SOURCE_CURRENT_FIELDS, *PPN_FIELDS, "epsilon_closed_source_failure_3988"]
    return [
        {
            "field": field,
            "required": field != "epsilon_closed_source_failure_3988",
            "units": "dimensionless" if field != "source_id" else "text",
            "description": "3988 source-current/PPN residual input or computed output",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for field in fields
    ]


def compute_residual(row: dict[str, Any]) -> tuple[str, str, str]:
    required = [*TAIL_FIELDS, *SOURCE_CURRENT_FIELDS, *PPN_FIELDS]
    missing = [field for field in required if row.get(field, "") in {"", None, "MISSING"}]
    if missing:
        return ("BLOCKED_MISSING_INPUTS", "|".join(f"MISSING_{field}" for field in missing), "")
    try:
        value = sum(abs(float(row[field])) for field in required)
    except ValueError as exc:
        return ("BLOCKED_NONNUMERIC_INPUT", str(exc), "")
    return ("COMPUTED_NONCLAIM", "numeric smoke computation only", f"{value:.12g}")


def runner_smoke_rows(timestamp: str) -> list[dict[str, Any]]:
    fields = [*TAIL_FIELDS, *SOURCE_CURRENT_FIELDS, *PPN_FIELDS]
    zero = {"source_id": "SMOKE3988_0_all_zero_source_current_and_PPN"}
    for field in fields:
        zero[field] = "0"

    small = {"source_id": "SMOKE3988_1_small_absolute_envelope"}
    for index, field in enumerate(fields, start=1):
        small[field] = f"{index}e-6"

    missing = {"source_id": "SMOKE3988_2_real_parent_rows_missing"}
    for field in fields:
        missing[field] = ""

    rows: list[dict[str, Any]] = []
    for row in [zero, small, missing]:
        status, blockers, value = compute_residual(row)
        rows.append(
            {
                **row,
                "epsilon_closed_source_failure_3988": value,
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
            "source_id": "REAL3988_0_controlled_EH_monopole_l2m0_source_current_PPN_bound",
            "angular_projector_status": "PASS_LGE1_ANGULAR_ZERO",
            "Q_lm_residual": "0",
            "source_charge_residual_before": "epsilon_closed_source_failure_3987",
            "source_charge_residual_after": "epsilon_closed_source_failure_3988",
            "closed_or_reduced_in_3988": "Hilbert_formula_conditional|parent_JH_split_to_seven_gates|PPN_stability_split_to_full_absolute_vector",
            "still_open": "epsilon_product_lock_total|epsilon_extra_monopole_total|epsilon_parent_JH_origin_3988|epsilon_PPN_source_stability_3988",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def feed_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "feed_id": "FEED3988_0",
            "target": "epsilon_parent_JH_origin",
            "update": "source-current origin split into seven parent-descent/Ward/support/EM/non-Hilbert gates",
            "status": "SOURCE_CURRENT_ORIGIN_BOUND_VECTOR_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3988_1",
            "target": "epsilon_PPN_source_stability",
            "update": "PPN source stability split into full no-cancellation PPN envelope",
            "status": "PPN_SOURCE_STABILITY_VECTOR_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "feed_id": "FEED3988_2",
            "target": "epsilon_closed_source_failure_3987",
            "update": "reduced to epsilon_closed_source_failure_3988",
            "status": "MASTER_RESIDUAL_REDUCED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3988_0",
            "question": "is parent source-current origin closed",
            "answer": "no",
            "reason": "Hilbert formula is conditional, but matter descent/no-source-prefactor/worldtube/support and non-Hilbert silence remain unsigned",
            "status": "SOURCE_CURRENT_ORIGIN_NOT_CLOSED_BUT_FACTORED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3988_1",
            "question": "is PPN source stability closed",
            "answer": "no",
            "reason": "full PPN vector requires beta/source/readout/q_loc/preferred-frame components to be zero or bounded",
            "status": "PPN_STABILITY_NOT_CLOSED_BUT_VECTOR_READY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC3988_2",
            "question": "next best target",
            "answer": "matter descent/no-source-prefactor or first numeric PPN vector fill",
            "reason": "source-prefactor countermodel is the sharpest threat to derived active mass; PPN vector is the local-GR completion gate",
            "status": "MOVE_TO_MATTER_DESCENT_OR_PPN_VECTOR_FILL",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CLG3988_0",
            "gate": "parent source-current origin",
            "requirement": "epsilon_parent_JH_origin_3988=0 or source-backed bound below arena targets",
            "status": "BLOCKED_SOURCE_CURRENT_DESCENT_GATES_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3988_1",
            "gate": "PPN source stability",
            "requirement": "epsilon_PPN_source_stability_3988=0 or all PPN components bounded",
            "status": "BLOCKED_FULL_PPN_VECTOR_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CLG3988_2",
            "gate": "local GR",
            "requirement": "product lock, extra monopole bound, source-current origin, and PPN vector all pass",
            "status": "BLOCKED_LOCAL_GR_SOURCE_COUPLING_VECTOR_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT3988_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive matter descent/no-source-prefactor for active Hilbert source current, or fill the first full PPN vector rows",
            "success_condition": "R_matter_descent or R_source_prefactor is closed/bounded, or Delta_PPN_abs becomes executable without hiding source-current failures",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "SOURCE_CURRENT_ORIGIN_AND_PPN_STABILITY_BOUND_VECTORS_READY",
            "strongest_result": "Hilbert matter+EM source formula is conditionally derived; parent JH origin is split into seven gates; PPN source stability is split into a full absolute no-cancellation vector; master residual is executable but nonclaim",
            "claim_status": "NONCLAIM_SOURCE_DESCENT_AND_FULL_PPN_VECTOR_OPEN",
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
    return f"""# 3988 — Parent Source-Current Origin Or PPN Source Stability

Timestamp: `{timestamp}`

## Result

This checkpoint moves from “source current missing” to an explicit source-current and PPN gate.

The conditional formula is clean:

`T_total^{{mu nu}} = (-2/sqrt(-g_obs)) delta(S_matter+S_EM)/delta g_obs_munu`

and

`J_H[tau] = star(T_total(tau,.))`.

So ordinary matter and descended Maxwell/Poynting stress belong in the same Hilbert source slot when the parent action descends to one observed coframe before readout.

## Remaining Source-Current Origin Gate

The origin is not fully closed. It is now

`epsilon_parent_JH_origin_3988 <= R_coframe_descent + R_matter_descent + R_source_prefactor + R_Ward_exchange + R_worldtube_support + R_EM_Hilbert_descent + R_nonHilbert_current`.

The sharp countermodel is still source-prefactor weighting: `S_ord=sum_A w_A S_A` can leave ordinary equations plausible while changing active source mass unless parent grammar forbids it or makes it universal.

## PPN Stability Gate

Local GR cannot be claimed from Newton shape alone. The PPN source-stability residual is now

`epsilon_PPN_source_stability_3988 <= |delta_p|+|b_R|+|Delta_beta_total_abs|+|d_R|+|w_R_source|+|epsilon_endpoint_R|+|alpha_readout_delta_GM|+|q_loc_Khat|`.

## Master Residual

`epsilon_closed_source_failure_3988 <= epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_parent_JH_origin_3988 + epsilon_PPN_source_stability_3988`.

## Source Register

{source_lines}

## Next Target

`{NEXT_DOC}`

Attack matter descent/no-source-prefactor, or fill the first full PPN vector rows.
"""


def update_spine(timestamp: str) -> None:
    marker = "## 3988 - Source-Current Origin And PPN Stability Vectors"
    entry = f"""

{marker}

- Timestamp: `{timestamp}`
- Status: `SOURCE_CURRENT_ORIGIN_AND_PPN_STABILITY_BOUND_VECTORS_READY`
- Conditional formula:
  `T_total^{{mu nu}}=(-2/sqrt(-g_obs)) delta(S_matter+S_EM)/delta g_obs_munu`, with `J_H[tau]=star(T_total(tau,.))`.
- Source-current origin residual:
  `epsilon_parent_JH_origin_3988 <= R_coframe_descent + R_matter_descent + R_source_prefactor + R_Ward_exchange + R_worldtube_support + R_EM_Hilbert_descent + R_nonHilbert_current`.
- PPN stability residual:
  `epsilon_PPN_source_stability_3988 <= |delta_p|+|b_R|+|Delta_beta_total_abs|+|d_R|+|w_R_source|+|epsilon_endpoint_R|+|alpha_readout_delta_GM|+|q_loc_Khat|`.
- Current residual:
  `epsilon_closed_source_failure_3988 <= epsilon_product_lock_total + epsilon_extra_monopole_total + epsilon_parent_JH_origin_3988 + epsilon_PPN_source_stability_3988`.
- Still nonclaim:
  source-current descent/no-prefactor and full PPN vector remain open.
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
    cert_statuses = {str(row["3988_status"]) for row in certificate}
    bound_symbols = {str(row["symbol"]) for row in bound_data}
    schema_fields = {str(row["field"]) for row in runner_schema}
    smoke_by_id = {str(row["source_id"]): row for row in runner_smoke}
    feed_statuses = {str(row["status"]) for row in feed}
    decision_statuses = {str(row["status"]) for row in decisions}
    claim_statuses = {str(row["status"]) for row in claims}
    project = projector[0]
    required_schema = {"source_id", *TAIL_FIELDS, *SOURCE_CURRENT_FIELDS, *PPN_FIELDS, "epsilon_closed_source_failure_3988"}
    required_symbols = {"epsilon_closed_source_failure_3988", "epsilon_parent_JH_origin_3988", "epsilon_PPN_source_stability_3988", *SOURCE_CURRENT_FIELDS, *PPN_FIELDS}

    return [
        val("VAL3988_00_sources_exist", all(row["exists"] for row in sources), "all cited source paths exist"),
        val("VAL3988_01_needles_found", all(row["needle_found"] for row in sources), "all cited source needles found"),
        val("VAL3988_02_theorem_statuses", {"CONDITIONAL_HILBERT_SOURCE_FORMULA_DERIVED", "PARENT_JH_ORIGIN_BOUND_VECTOR_DERIVED", "SOURCE_PREFACTOR_COUNTERMODEL_RETAINED", "PPN_SOURCE_STABILITY_ABSOLUTE_VECTOR_DERIVED", "MASTER_RESIDUAL_REDUCED_TO_SOURCE_DESCENT_AND_PPN_VECTOR"} <= theorem_statuses, "source formula, origin split, prefactor guard, PPN vector, and master theorem rows present"),
        val("VAL3988_03_certificate_statuses", {"FORMULA_DERIVED_CONDITIONAL_ON_DESCENT", "NOT_CLOSED_BUT_SEVEN_GATE_BOUND_VECTOR_READY", "NOT_CLOSED_FULL_PPN_ABSOLUTE_VECTOR_READY", "CONDITIONAL_EM_STRESS_INCLUDED_IF_MAXWELL_DESCENT_SIGNED", "FALSE_BUT_REDUCED_TO_PRODUCT_EXTRA_SOURCE_DESCENT_PPN_VECTOR"} <= cert_statuses, "certificate captures formula progress and remaining blocks"),
        val("VAL3988_04_bound_symbols", required_symbols <= bound_symbols, "source-current and PPN bound symbols present"),
        val("VAL3988_05_runner_schema", required_schema <= schema_fields, "runner schema has all source-current, PPN, tail, and output fields"),
        val("VAL3988_06_runner_zero", smoke_by_id["SMOKE3988_0_all_zero_source_current_and_PPN"]["epsilon_closed_source_failure_3988"] == "0", "zero smoke computes zero"),
        val("VAL3988_07_runner_small", smoke_by_id["SMOKE3988_1_small_absolute_envelope"]["epsilon_closed_source_failure_3988"] == "0.000153", "small smoke computes expected absolute envelope"),
        val("VAL3988_08_runner_blocks_missing", smoke_by_id["SMOKE3988_2_real_parent_rows_missing"]["runner_status"] == "BLOCKED_MISSING_INPUTS", "runner blocks missing parent rows"),
        val("VAL3988_09_projector_reduced", project["source_charge_residual_after"] == "epsilon_closed_source_failure_3988" and "epsilon_parent_JH_origin_3988" in project["still_open"], "projector points at 3988 reduced residual"),
        val("VAL3988_10_feed", {"SOURCE_CURRENT_ORIGIN_BOUND_VECTOR_READY", "PPN_SOURCE_STABILITY_VECTOR_READY", "MASTER_RESIDUAL_REDUCED_NONCLAIM"} <= feed_statuses, "feed rows capture 3988 reductions"),
        val("VAL3988_11_decision", {"SOURCE_CURRENT_ORIGIN_NOT_CLOSED_BUT_FACTORED", "PPN_STABILITY_NOT_CLOSED_BUT_VECTOR_READY", "MOVE_TO_MATTER_DESCENT_OR_PPN_VECTOR_FILL"} <= decision_statuses, "decision gate records current stance and next target"),
        val("VAL3988_12_claim_gate", {"BLOCKED_SOURCE_CURRENT_DESCENT_GATES_OPEN", "BLOCKED_FULL_PPN_VECTOR_OPEN", "BLOCKED_LOCAL_GR_SOURCE_COUPLING_VECTOR_OPEN"} <= claim_statuses, "claim gates preserve remaining blocks"),
        val("VAL3988_13_next_target", next_target[0]["next_doc"] == NEXT_DOC and next_target[0]["next_script"] == NEXT_SCRIPT, "next target points to matter descent/no-prefactor or PPN fill"),
        val("VAL3988_14_all_nonclaim", all(not row.get("valid_for_claim", True) for group in rows.values() for row in group), "all generated physics rows remain nonclaim"),
        val("VAL3988_15_outputs_outside_fwb", all(FWB not in path.parents for path in generated_csvs) and FWB not in DOC_PATH.parents, "no generated output is inside formalization-workbench"),
        val("VAL3988_16_doc_exists", DOC_PATH.exists(), "checkpoint doc exists"),
        val("VAL3988_17_spine_updated", SPINE_PATH.exists() and "3988 - Source-Current Origin And PPN Stability Vectors" in read_text(SPINE_PATH), "spine updated"),
        val("VAL3988_18_csv_parse", parsed, parse_detail),
        val("VAL3988_19_script_compile", True, "script compiled before validation write"),
        val("VAL3988_20_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "scripts __pycache__ removed"),
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
    print(f"3988 validation passed: {len(validations)}/{len(validations)} checks")
    print(f"source needles: {sum(1 for row in rows['sources'] if row['needle_found'])}/{len(rows['sources'])}")
    print(rows["status"][0]["status"])


if __name__ == "__main__":
    run()
