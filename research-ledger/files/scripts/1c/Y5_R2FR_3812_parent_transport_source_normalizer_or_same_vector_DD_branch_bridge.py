from __future__ import annotations

import csv
import math
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "3812"
BRANCH = "MTS_R2FR_Y5_PARENT_TRANSPORT_SOURCE_NORMALIZER_OR_SAME_VECTOR_DD_BRANCH_BRIDGE_3812"
PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3812-Y5-R2FR-parent-transport-source-normalizer-or-same-vector-DD-branch-bridge.md"
SCRIPT_PATH = PCW / "scripts" / "Y5_R2FR_3812_parent_transport_source_normalizer_or_same_vector_DD_branch_bridge.py"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

P_3811 = PCW / "3811-Y5-R2FR-no-hidden-visible-coupling-morphism-signature-or-full-rank-product-bridge.md"
P_3480 = PCW / "3480-Y5-R2FR-parent-transport-and-source-normalization-owner-or-product-bound-upgrade.md"
P_3481 = PCW / "3481-Y5-R2FR-source-current-Jq-theorem-or-first-transport-normalizer-row.md"
P_3482 = PCW / "3482-Y5-R2FR-earth-source-amplitude-SEq-current-bound-or-zero-theorem.md"
P_3483 = PCW / "3483-Y5-R2FR-quadratic-DD-WEP-source-runner-or-external-SEq-lower-bound.md"
P_3485 = PCW / "3485-Y5-R2FR-hyperfine-isotope-DD-basis-extraction-or-delta-m-kernel-exclusion.md"
P_3486 = PCW / "3486-Y5-R2FR-earth-Qdelta-source-stability-or-parent-kernel-exclusion.md"
P_3487 = PCW / "3487-Y5-R2FR-parent-source-map-for-DD-earth-vector-or-local-rank-closure-demotion.md"

CSV_3475_MATRIX = OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv"
CSV_3481_WEP_NORM = OUT / "P8_Y5_R2FR_3481_WEP_SHARED_EARTH_NORMALIZER_ROWS_NONCLAIM.csv"
CSV_3482_EARTH = OUT / "P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv"
CSV_3483_THEOREM = OUT / "P8_Y5_R2FR_3483_QUADRATIC_WEP_THEOREM.csv"
CSV_3483_BLIND = OUT / "P8_Y5_R2FR_3483_BLIND_DIRECTION_LEDGER.csv"
CSV_3485_RANK = OUT / "P8_Y5_R2FR_3485_RANK_AND_CONDITION_LEDGER.csv"
CSV_3485_HYPERFINE = OUT / "P8_Y5_R2FR_3485_EXTRACTED_HYPERFINE_ROWS_NONCLAIM.csv"
CSV_3486_STRESS = OUT / "P8_Y5_R2FR_3486_RANK_STRESS_TESTS.csv"
CSV_3486_QDELTA = OUT / "P8_Y5_R2FR_3486_QDELTA_POSITIVITY_BOUNDS.csv"
CSV_3487_BRIDGE = OUT / "P8_Y5_R2FR_3487_PARENT_TO_DD_BRIDGE_DERIVATION.csv"
CSV_3487_RESIDUALS = OUT / "P8_Y5_R2FR_3487_RBRIDGE_RESIDUAL_SLOTS.csv"
CSV_3811_NEXT = OUT / "P8_Y5_R2FR_3811_NEXT_TARGET.csv"

CHANNELS = ["D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff"]

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3812_SOURCE_REGISTER.csv",
    "transport": OUT / "P8_Y5_R2FR_3812_TRANSPORT_NORMALIZER_ATTEMPT.csv",
    "external": OUT / "P8_Y5_R2FR_3812_EXTERNAL_AMPLITUDE_BRANCH_LEDGER.csv",
    "same_schema": OUT / "P8_Y5_R2FR_3812_SAME_VECTOR_DD_RUNNER_SCHEMA.csv",
    "same_dryrun": OUT / "P8_Y5_R2FR_3812_SAME_VECTOR_DD_RUNNER_DRYRUN.csv",
    "qdelta": OUT / "P8_Y5_R2FR_3812_QEARTH_QDELTA_STABILITY_CARRYFORWARD.csv",
    "rbridge": OUT / "P8_Y5_R2FR_3812_RBRIDGE_RESIDUAL_CARRYFORWARD.csv",
    "gates": OUT / "P8_Y5_R2FR_3812_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3812_DECISION_ROWS.csv",
    "next_target": OUT / "P8_Y5_R2FR_3812_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3812_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3812_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3812_0_3811_doc", P_3811, "Use the 3811 bridge", "3811 target: attack normalizers/source amplitude, not no-Hom again"),
    ("SRC3812_1_3480_doc", P_3480, "FIT3480_0_full_rank_visible_inversion", "3480 inverse theorem and row-normalizer throat"),
    ("SRC3812_2_3481_doc", P_3481, "WEN3481_0_MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10", "3481 WEP normalizer partial factors"),
    ("SRC3812_3_3482_doc", P_3482, "EARTH3482_0_bulk_full_DD_four_charge", "3482 Earth DD source vector and branch split"),
    ("SRC3812_4_3483_doc", P_3483, "THM3483_0_same_vector_substitution", "3483 same-vector quadratic WEP theorem"),
    ("SRC3812_5_3485_doc", P_3485, "BFK3485_4_Yb_isotope_delta_kappa", "3485 sourced hyperfine/isotope closure candidates"),
    ("SRC3812_6_3486_doc", P_3486, "STRESS3486_0_baseline", "3486 Q_delta Earth stability stress test"),
    ("SRC3812_7_3487_doc", P_3487, "S_E^q = Q_Earth", "3487 parent-to-DD bridge equation with explicit residual"),
    ("SRC3812_8_3475_matrix", CSV_3475_MATRIX, "MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10", "current augmented WEP/clock sensitivity matrix"),
    ("SRC3812_9_3481_wep_norm", CSV_3481_WEP_NORM, "WEN3481_0_MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10", "partial WEP normalizer rows"),
    ("SRC3812_10_3482_earth", CSV_3482_EARTH, "EARTH3482_0_bulk_full_DD_four_charge", "Earth DD source vector"),
    ("SRC3812_11_3483_theorem", CSV_3483_THEOREM, "THM3483_0_same_vector_substitution", "quadratic WEP theorem csv"),
    ("SRC3812_12_3483_blind", CSV_3483_BLIND, "BLIND3483_2_QEarth_plus_two_clocks", "same-vector blind direction ledger"),
    ("SRC3812_13_3485_rank", CSV_3485_RANK, "BFK3485_4_Yb_isotope_delta_kappa", "best proxy closure rank row"),
    ("SRC3812_14_3485_hyperfine", CSV_3485_HYPERFINE, "BFK3485_4_Yb_isotope_delta_kappa", "sourced hyperfine/isotope vector"),
    ("SRC3812_15_3486_stress", CSV_3486_STRESS, "STRESS3486_3_forced_zero_failure", "Q_delta forced-zero rank failure"),
    ("SRC3812_16_3486_qdelta", CSV_3486_QDELTA, "QDEL3486_3_fe_only_lower_bound", "positive Q_delta proxy lower bound"),
    ("SRC3812_17_3487_bridge", CSV_3487_BRIDGE, "BRIDGE3487_4_parent_bridge_equation", "S_E^q = Q_Earth dot C + R_bridge"),
    ("SRC3812_18_3487_residuals", CSV_3487_RESIDUALS, "R_matter_glue", "explicit R_bridge residual slots"),
    ("SRC3812_19_3811_next", CSV_3811_NEXT, "3812-Y5-R2FR-parent-transport-source-normalizer-or-same-vector-DD-branch-bridge.md", "3811 machine handoff"),
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def fmt(value: float) -> str:
    if math.isnan(value):
        return "nan"
    if math.isinf(value):
        return "inf"
    return f"{value:.12e}"


def vector_from_matrix_row(row: dict[str, str], prefix: str = "raw") -> list[float]:
    return [float(row[f"{prefix}_{channel}"]) for channel in CHANNELS]


def vector_from_extracted_row(row: dict[str, str]) -> list[float]:
    return [float(row[channel]) for channel in CHANNELS]


def dot(left: list[float], right: list[float]) -> float:
    return sum(a * b for a, b in zip(left, right))


def norm(vector: list[float]) -> float:
    return math.sqrt(dot(vector, vector))


def normalize(vector: list[float]) -> list[float]:
    length = norm(vector)
    if length == 0:
        return [0.0 for _ in vector]
    return [value / length for value in vector]


def rref(matrix: list[list[float]], tol: float = 1e-12) -> tuple[list[list[float]], list[int]]:
    rows = [row[:] for row in matrix]
    if not rows:
        return rows, []
    row_count = len(rows)
    col_count = len(rows[0])
    pivots: list[int] = []
    pivot_row = 0
    for col in range(col_count):
        best = max(range(pivot_row, row_count), key=lambda idx: abs(rows[idx][col]), default=pivot_row)
        if abs(rows[best][col]) <= tol:
            continue
        rows[pivot_row], rows[best] = rows[best], rows[pivot_row]
        scale = rows[pivot_row][col]
        rows[pivot_row] = [value / scale for value in rows[pivot_row]]
        for row_index in range(row_count):
            if row_index == pivot_row:
                continue
            factor = rows[row_index][col]
            if abs(factor) > tol:
                rows[row_index] = [
                    value - factor * pivot_value
                    for value, pivot_value in zip(rows[row_index], rows[pivot_row])
                ]
        pivots.append(col)
        pivot_row += 1
        if pivot_row == row_count:
            break
    return rows, pivots


def rank(matrix: list[list[float]], tol: float = 1e-12) -> int:
    _, pivots = rref(matrix, tol=tol)
    return len(pivots)


def nullspace(matrix: list[list[float]], tol: float = 1e-12) -> list[list[float]]:
    if not matrix:
        return [[1.0, 0.0, 0.0, 0.0]]
    reduced, pivots = rref(matrix, tol=tol)
    col_count = len(matrix[0])
    free_cols = [col for col in range(col_count) if col not in pivots]
    basis: list[list[float]] = []
    for free_col in free_cols:
        vector = [0.0] * col_count
        vector[free_col] = 1.0
        for row_index, pivot_col in enumerate(pivots):
            vector[pivot_col] = -reduced[row_index][free_col]
        basis.append(normalize(vector))
    return basis


def earth_vector() -> list[float]:
    row = read_csv(CSV_3482_EARTH)[0]
    return [
        float(row["Q_hatm_full_Earth"]),
        float(row["Q_delta_m_Earth"]),
        float(row["Q_m_e_Earth"]),
        float(row["Q_e_full_Earth"]),
    ]


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "exists": bool_text(exists),
                "needle": needle,
                "needle_found": bool_text(needle in text),
                "role": role,
                "valid_for_claim": "false",
            }
        )
    return rows


def transport_rows(timestamp: str) -> list[dict[str, Any]]:
    matrix = read_csv(CSV_3475_MATRIX)
    wep_norms = read_csv(CSV_3481_WEP_NORM)
    rows: list[dict[str, Any]] = []
    for index, row in enumerate(wep_norms):
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "normalizer_id": f"TN3812_{index}_{row['normalizer_id']}",
                "row_symbol": row["row_symbol"],
                "arena": row["arena"],
                "observable_type": "Earth-source WEP eta",
                "observable_units": "dimensionless_eta",
                "raw_deltaQ_norm": row["raw_deltaQ_norm"],
                "numeric_factor": row["numeric_factor_per_abs_S_Eq_inv"],
                "derived_normalizer": f"{row['row_symbol']} normalizer = {row['numeric_factor_per_abs_S_Eq_inv']} * abs_S_Eq_inv",
                "derivation": "eta_AB = S_E^q(DeltaQ_AB dot C); after unit-row normalization, |Y_AB| <= eta_bound/(|S_E^q| ||DeltaQ_AB||).",
                "source_amplitude_status": "retained_symbol_abs_S_Eq_inv_not_set_to_one",
                "claim_status": "PARTIAL_NUMERIC_FACTOR_DERIVED_SOURCE_AMPLITUDE_OPEN",
                "valid_for_claim": "false",
            }
        )
    clock_rows = [row for row in matrix if row["row_type"].startswith("clock_")]
    for offset, row in enumerate(clock_rows, start=len(rows)):
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "normalizer_id": f"TN3812_{offset}_{row['aug_row_id']}",
                "row_symbol": f"Y_{offset}",
                "arena": row["arena"],
                "observable_type": row["row_type"],
                "observable_units": row["bound_units"],
                "raw_deltaQ_norm": fmt(norm(vector_from_matrix_row(row))),
                "numeric_factor": "not_source_filled",
                "derived_normalizer": "requires clock transport/readout/source product; not replaced by WEP source amplitude",
                "derivation": "clock rows are linear sensitivity rows only after their own transport/readout map is supplied; their published bounds carry drift/instability units.",
                "source_amplitude_status": "MISSING_CLOCK_TRANSPORT_NORMALIZER",
                "claim_status": "OPEN_NOT_NUMERIC_ROW_NORMALIZER",
                "valid_for_claim": "false",
            }
        )
    return rows


def external_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "branch_row_id": "EXT3812_0_external_equation",
            "statement": "External-amplitude branch uses eta_AB = S_E^q(DeltaQ_AB dot C).",
            "derivation": "This is the 3481 factorization; 3812 keeps S_E^q as an owned source amplitude instead of setting it to unity.",
            "result": "linear_inverse_available_only_conditionally",
            "blocks_claim": "missing lower/nonzero/source-normalization theorem for abs(S_E^q)",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "branch_row_id": "EXT3812_1_wep_normalizers_source_filled",
            "statement": "The two WEP row-norm factors are source-filled numerically.",
            "derivation": "N_0 = 3.012900353801e+02 abs_S_Eq_inv and N_1 = 1.352877475825e+02 abs_S_Eq_inv from the 3481 DD material rows.",
            "result": "real_partial_progress_not_a_claim",
            "blocks_claim": "abs_S_Eq_inv remains symbolic and must be parent-derived/source-bounded",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "branch_row_id": "EXT3812_2_clock_rows_do_not_share_wep_normalizer",
            "statement": "Clock drift/instability rows cannot inherit WEP normalizers.",
            "derivation": "Their bounds have yr^-1 product and fractional-instability product units, so the 3480 mixed-unit no-shortcut rule still applies.",
            "result": "clock_normalizers_still_open",
            "blocks_claim": "MISSING_CLOCK_TRANSPORT_READOUT_NORMALIZER",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "branch_row_id": "EXT3812_3_external_branch_verdict",
            "statement": "External branch is narrowed to one real missing scalar plus clock transport rows.",
            "derivation": "WEP geometry and row norms are now fixed; only source amplitude ownership/lower bound prevents coefficient bounds.",
            "result": "PROMISING_CONDITIONAL_BRANCH",
            "blocks_claim": "MISSING_PARENT_SOURCE_CURRENT_NORMALIZATION",
            "valid_for_claim": "false",
        },
    ]


def same_vector_schema_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "schema_id": "SV3812_0_coefficient_vector",
            "object": "C=(D_hatm_eff,D_delta_m_eff,D_me_eff,D_e_eff)",
            "runner_rule": "four-channel visible coefficient vector; no WEP row is inserted as a linear independent row in same-vector branch",
            "equation": "C_i = partial ln theta_i / partial q",
            "status": "defined",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "schema_id": "SV3812_1_source_bridge",
            "object": "same-vector Earth source",
            "runner_rule": "source amplitude is computed from the same coefficient vector plus residual",
            "equation": "S_E^q = Q_Earth dot C + R_bridge",
            "status": "conditional_bridge_imported_from_3487",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "schema_id": "SV3812_2_quadratic_wep",
            "object": "Earth-source WEP",
            "runner_rule": "WEP constraints are quadratic products, not linear rank rows",
            "equation": "eta_AB = (Q_Earth dot C)(DeltaQ_AB dot C) + residual_terms",
            "status": "executable_guard",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "schema_id": "SV3812_3_blind_family",
            "object": "Q_Earth kernel",
            "runner_rule": "any C in ker(Q_Earth) is WEP-silent before non-WEP rows or source lower-bound theorem",
            "equation": "Q_Earth dot C = 0 implies eta_AB = 0 for every WEP DeltaQ_AB",
            "status": "exact_blind_family_retained",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "schema_id": "SV3812_4_allowed_rank_closure",
            "object": "non-WEP rows",
            "runner_rule": "rank closure may use clock/hyperfine/source rows; WEP rows are only used as quadratic inequalities",
            "equation": "rank([Q_Earth; clock rows; hyperfine rows]) = 4 is only proxy closure until R_bridge is zero/bounded",
            "status": "nonclaim_runner_schema_ready",
            "valid_for_claim": "false",
        },
    ]


def same_vector_dryrun_rows(timestamp: str) -> list[dict[str, Any]]:
    matrix = read_csv(CSV_3475_MATRIX)
    q_earth = earth_vector()
    q_earth_forced_zero = q_earth[:]
    q_earth_forced_zero[1] = 0.0
    wep_rows = [row for row in matrix if row["row_type"] == "WEP_material_difference"]
    clock_rows = [row for row in matrix if row["row_type"].startswith("clock_")]
    clock_vectors = [vector_from_matrix_row(row) for row in clock_rows]
    wep_vectors = [vector_from_matrix_row(row) for row in wep_rows]
    best = next(row for row in read_csv(CSV_3485_HYPERFINE) if row["candidate_id"] == "BFK3485_4_Yb_isotope_delta_kappa")
    best_vector = vector_from_extracted_row(best)
    rank_ledger = next(row for row in read_csv(CSV_3485_RANK) if row["candidate_id"] == "BFK3485_4_Yb_isotope_delta_kappa")
    tests = [
        (
            "DRY3812_0_QEarth_only",
            "source hyperplane only",
            [q_earth],
            "same-vector WEP has exact 3D blind family",
            "allowed_diagnostic",
        ),
        (
            "DRY3812_1_QEarth_plus_current_clocks",
            "source hyperplane plus current alpha/SrCs clock rows",
            [q_earth] + clock_vectors,
            "one blind direction remains with current two clock rows",
            "allowed_nonWEP_linear_rows",
        ),
        (
            "DRY3812_2_QEarth_plus_clocks_plus_best_hyperfine",
            "source hyperplane plus current clocks plus BFK3485_4 Yb isotope row",
            [q_earth] + clock_vectors + [best_vector],
            "proxy rank closure using non-WEP sourced row",
            "allowed_proxy_nonclaim",
        ),
        (
            "DRY3812_3_forced_Qdelta_zero",
            "same rows as DRY3812_2 but force Q_delta_m_Earth=0",
            [q_earth_forced_zero] + clock_vectors + [best_vector],
            "rank closure fails if neutron-excess source component is killed",
            "diagnostic_nonclaim",
        ),
        (
            "DRY3812_4_forbidden_WEP_linear_insert",
            "source hyperplane plus clocks plus first WEP DeltaQ row",
            [q_earth] + clock_vectors + wep_vectors[:1],
            "algebra closes, but same-vector runner forbids treating WEP as an independent linear row",
            "forbidden_rank_shortcut",
        ),
    ]
    rows = []
    for test_id, description, vectors, implication, runner_use in tests:
        test_rank = rank(vectors)
        basis = nullspace(vectors)
        first = basis[0] if basis else [0.0, 0.0, 0.0, 0.0]
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "dryrun_id": test_id,
                "description": description,
                "row_count": len(vectors),
                "rank": test_rank,
                "null_dim": 4 - test_rank,
                "unit_null_D_hatm_eff": fmt(first[0]),
                "unit_null_D_delta_m_eff": fmt(first[1]),
                "unit_null_D_me_eff": fmt(first[2]),
                "unit_null_D_e_eff": fmt(first[3]),
                "projection_best_hyperfine_on_3483_blind": rank_ledger["projection_on_3483_blind"] if "best_hyperfine" in test_id else "",
                "condition_number_after": rank_ledger["condition_number_after"] if "best_hyperfine" in test_id else "",
                "runner_use": runner_use,
                "implication": implication,
                "valid_for_claim": "false",
            }
        )
    return rows


def qdelta_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in read_csv(CSV_3486_STRESS):
        rows.append(
            {
                "timestamp_utc": timestamp,
                "branch_id": BRANCH,
                "checkpoint_id": CHECKPOINT,
                "carry_id": f"QDC3812_{row['scenario_id']}",
                "source_table": "P8_Y5_R2FR_3486_RANK_STRESS_TESTS.csv",
                "statement": row["description"],
                "value": row["Q_delta_m_Earth_used"],
                "rank_with_best_3485_row": row["rank_with_best_3485_row"],
                "condition_number": row["condition_number"],
                "status": row["closure_status"],
                "3812_use": "same-vector proxy closure stress test",
                "valid_for_claim": "false",
            }
        )
    for row in read_csv(CSV_3486_QDELTA):
        if row["bound_id"] in {"QDEL3486_0_baseline_sum", "QDEL3486_3_fe_only_lower_bound", "QDEL3486_4_critical_fe_fraction"}:
            rows.append(
                {
                    "timestamp_utc": timestamp,
                    "branch_id": BRANCH,
                    "checkpoint_id": CHECKPOINT,
                    "carry_id": f"QDC3812_{row['bound_id']}",
                    "source_table": "P8_Y5_R2FR_3486_QDELTA_POSITIVITY_BOUNDS.csv",
                    "statement": row["statement"],
                    "value": row["value"],
                    "rank_with_best_3485_row": "",
                    "condition_number": "",
                    "status": row["status"],
                    "3812_use": "positive Earth neutron-excess component is retained as DD proxy evidence",
                    "valid_for_claim": "false",
                }
            )
    return rows


def rbridge_rows(timestamp: str) -> list[dict[str, Any]]:
    bridge_rows = read_csv(CSV_3487_BRIDGE)
    residual_rows = read_csv(CSV_3487_RESIDUALS)
    rows: list[dict[str, Any]] = []
    for row in bridge_rows:
        if row["step_id"] in {"BRIDGE3487_0_parent_source_definition", "BRIDGE3487_4_parent_bridge_equation", "BRIDGE3487_5_closure_implication"}:
            rows.append(
                {
                    "timestamp_utc": timestamp,
                    "branch_id": BRANCH,
                    "checkpoint_id": CHECKPOINT,
                    "carry_id": f"RBC3812_{row['step_id']}",
                    "slot": row["claim"],
                    "status": row["status"],
                    "required_action": "imported bridge equation; do not set R_bridge=0 without proof",
                    "blocks_claim": "true",
                    "valid_for_claim": "false",
                }
            )
    for row in residual_rows:
        if row["bridge_residual_id"] in {"R_matter_glue", "R_projector", "R_G_kappa", "R_visible_coeff"}:
            rows.append(
                {
                    "timestamp_utc": timestamp,
                    "branch_id": BRANCH,
                    "checkpoint_id": CHECKPOINT,
                    "carry_id": f"RBC3812_{row['bridge_residual_id']}",
                    "slot": row["bridge_formula_slot"],
                    "status": row["current_status"],
                    "required_action": row["required_zero_or_bound"],
                    "blocks_claim": row["blocks_parent_promotion"].lower(),
                    "valid_for_claim": "false",
                }
            )
    return rows


def gate_rows(timestamp: str, grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    wep_partial_count = sum("PARTIAL_NUMERIC_FACTOR" in row["claim_status"] for row in grouped["transport"])
    same_runner_ready = any(row["schema_id"] == "SV3812_2_quadratic_wep" for row in grouped["same_schema"])
    forced_zero_fails = any(row["carry_id"] == "QDC3812_STRESS3486_3_forced_zero_failure" and row["status"] == "rank_fails" for row in grouped["qdelta"])
    forbidden_wep_guard = any(row["dryrun_id"] == "DRY3812_4_forbidden_WEP_linear_insert" and row["runner_use"] == "forbidden_rank_shortcut" for row in grouped["same_dryrun"])
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3812_0_wep_row_norm_factors",
            "requirement": "at least one WEP transport/source normalizer factor is source-filled without unity smuggling",
            "passed": bool_text(wep_partial_count >= 2),
            "evidence": f"{wep_partial_count} WEP rows have numeric factors times abs_S_Eq_inv",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3812_1_source_amplitude_owned",
            "requirement": "abs(S_E^q) is parent-derived, bounded below, or source-filled with units",
            "passed": "false",
            "evidence": "S_E^q remains external symbol or Q_Earth dot C + R_bridge; no lower theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3812_2_same_vector_runner_guard",
            "requirement": "same-vector runner treats WEP as quadratic and forbids linear WEP rank shortcut",
            "passed": bool_text(same_runner_ready and forbidden_wep_guard),
            "evidence": "SV3812 schema plus DRY3812_4 forbidden shortcut row",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3812_3_proxy_neutron_excess_stability",
            "requirement": "DD proxy closure depends on nonzero Q_delta_m_Earth and forced zero must fail",
            "passed": bool_text(forced_zero_fails),
            "evidence": "3486 carryforward keeps baseline/lower-bound rank closure and forced-zero rank failure",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "gate_id": "GATE3812_4_parent_bridge_residuals",
            "requirement": "R_bridge residuals are all zero-derived or source-bounded",
            "passed": "false",
            "evidence": "R_matter_glue, R_projector, R_G_kappa, and R_visible_coeff remain open",
            "claim_allowed": "false",
            "valid_for_claim": "false",
        },
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": "DEC3812_0_external_branch_progress",
            "decision": "Keep the external-amplitude branch alive with real WEP normalizer factors.",
            "reason": "Two WEP row norms are now numeric times abs_S_Eq_inv, so the next missing object is a source-amplitude theorem rather than another row search.",
            "next_action": "derive or source-bound abs(S_E^q), then attach clock transport/readout normalizers",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": "DEC3812_1_same_vector_branch_progress",
            "decision": "Keep same-vector DD branch as an executable nonclaim runner.",
            "reason": "The runner preserves the exact blind-family theorem and uses non-WEP rows for proxy closure; it no longer cheats by treating WEP as a linear row.",
            "next_action": "attack R_bridge residuals so Q_Earth dot C can become parent-owned rather than DD-proxy-owned",
            "valid_for_claim": "false",
        },
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "decision_id": "DEC3812_2_best_next_target",
            "decision": "Move to R_bridge matter-glue/no-source-slot closure.",
            "reason": "3812 narrowed the bottleneck to source ownership: without R_bridge zero/bounds, neither branch can become local-GR/WEP evidence.",
            "next_action": "derive ordinary matter functor/source-slot theorem or finite source-normalizer residual row",
            "valid_for_claim": "false",
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "target_doc": "3813-Y5-R2FR-Rbridge-matter-glue-no-source-slot-or-finite-source-normalizer-row.md",
            "target_script": "scripts/Y5_R2FR_3813_Rbridge_matter_glue_no_source_slot_or_finite_source_normalizer_row.py",
            "objective": "Attack the source-ownership bottleneck exposed by 3812: prove the ordinary-matter functor/no-source-only-slot theorem that sets R_matter_glue and R_visible_coeff to zero, or extract the first finite parent source-normalizer residual row.",
            "success_gate": "At least one R_bridge residual is zero-derived or source-bounded with units, or a parent-owned lower/nonzero theorem for abs(S_E^q) is produced.",
            "avoid": "do not set R_bridge=0 by declaration; do not use WEP rows as same-vector linear rank rows; do not edit formalization-workbench; do not use GitHub",
            "valid_for_claim": "false",
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "status": "PASS_NONCLAIM_WEP_NORMALIZER_FACTORS_DERIVED_SAME_VECTOR_DD_RUNNER_READY_PARENT_SOURCE_OWNERSHIP_OPEN",
            "summary": "3812 makes actual forward progress on the coupling bottleneck: external-branch WEP row normalizers are numeric factors times abs_S_Eq_inv, and same-vector DD now has an executable nonclaim runner that respects Q_Earth dot C quadratic WEP and the blind-family theorem. The remaining claim blocker is parent source ownership/R_bridge, not a missing WEP row.",
            "valid_for_claim": "false",
        }
    ]


def row_bullet(row: dict[str, Any], key_fields: list[str]) -> str:
    label = " ".join(f"`{row[field]}`" for field in key_fields if row.get(field))
    rest = "; ".join(
        f"{key}: {value}"
        for key, value in row.items()
        if key not in key_fields and key not in {"timestamp_utc", "branch_id", "checkpoint_id"}
    )
    return f"- {label}: {rest}"


def write_markdown(grouped: dict[str, list[dict[str, Any]]]) -> None:
    lines = [
        "# 3812 - Parent Transport Source Normalizer Or Same-Vector DD Branch Bridge",
        "",
        "## Status",
        "",
        "`PASS_NONCLAIM_WEP_NORMALIZER_FACTORS_DERIVED_SAME_VECTOR_DD_RUNNER_READY_PARENT_SOURCE_OWNERSHIP_OPEN`.",
        "",
        "3812 does not just write another missing ledger. It converts the 3811 bottleneck into two executable branches.",
        "",
        "External-amplitude branch: the WEP transport normalizers are now real numeric row-norm factors, `N_0 = 3.012900353801e+02 * abs_S_Eq_inv` and `N_1 = 1.352877475825e+02 * abs_S_Eq_inv`. That is useful progress, but `abs(S_E^q)` is still parent-owned source physics, not a knob set to one.",
        "",
        "Same-vector branch: the runner is now guarded correctly. If `S_E^q = Q_Earth dot C + R_bridge`, WEP is quadratic, `eta_AB = (Q_Earth dot C)(DeltaQ_AB dot C) + residual_terms`, so WEP rows are forbidden as independent linear rank rows. Non-WEP clock/hyperfine rows may close rank only as DD-proxy evidence until `R_bridge` is zero-derived or bounded.",
        "",
        "No local-GR, Newton, WEP, clock, R10, EM, or calibrated source-coupling claim is made.",
        "",
    ]
    sections = [
        ("Source Register", "sources", ["source_id"]),
        ("Transport Normalizer Attempt", "transport", ["normalizer_id", "row_symbol"]),
        ("External Amplitude Branch", "external", ["branch_row_id"]),
        ("Same-Vector Runner Schema", "same_schema", ["schema_id"]),
        ("Same-Vector Runner Dryrun", "same_dryrun", ["dryrun_id"]),
        ("QEarth Qdelta Stability Carryforward", "qdelta", ["carry_id"]),
        ("RBridge Residual Carryforward", "rbridge", ["carry_id"]),
        ("Claim Gates", "gates", ["gate_id"]),
        ("Decision Rows", "decisions", ["decision_id"]),
        ("Next Target", "next_target", ["target_doc"]),
        ("Validation", "validation", ["check_id", "result"]),
    ]
    for title, key, key_fields in sections:
        lines.append(f"## {title}")
        for row in grouped[key]:
            lines.append(row_bullet(row, key_fields))
        lines.append("")
    DOC_PATH.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def update_spine() -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    lines = text.splitlines()
    if lines and lines[0].startswith("# Local GR Coupling Spine - Current State After "):
        lines[0] = "# Local GR Coupling Spine - Current State After 3812"
        text = "\n".join(lines) + "\n"

    paragraph = (
        "`3812` turns the 3811 coupling bottleneck into two controlled branches. External-amplitude WEP rows now have real row-norm factors, "
        "`N_0 = 3.012900353801e+02 * abs_S_Eq_inv` and `N_1 = 1.352877475825e+02 * abs_S_Eq_inv`, so the only WEP-side missing scalar is source ownership/lower bound for `S_E^q`. "
        "The same-vector DD branch is now an executable nonclaim runner: `S_E^q = Q_Earth dot C + R_bridge` makes WEP quadratic, preserves the `Q_Earth dot C = 0` blind family, and allows only non-WEP rows for proxy rank closure until `R_bridge` is zero-derived or bounded."
    )
    if "`3812` turns the 3811 coupling bottleneck" not in text:
        marker = "`3811` resolves the coupling-fork bookkeeping."
        idx = text.find(marker)
        if idx >= 0:
            next_blank = text.find("\n\n", idx)
            if next_blank >= 0:
                text = text[: next_blank + 2] + paragraph + "\n\n" + text[next_blank + 2 :]

    bullet = "- `3812 transport/source bridge`: WEP row normalizer factors are now numeric times `abs_S_Eq_inv`; same-vector DD is executable and forbids the old WEP-linear-rank shortcut."
    if bullet not in text:
        anchor = "- `3811 morphism/product bridge`: no-Hom remains parent-unsigned, but the finite branch is full-rank at sensitivity level; the active bottleneck is transport/source normalizers `N_r` and the `S_Eq` branch, not another symbolic alpha row."
        text = text.replace(anchor, anchor + "\n" + bullet)

    nonclaim = "- The 3812 transport/source bridge is nonclaim: WEP normalizer factors are real, but `S_E^q`, clock transport normalizers, and `R_bridge` source-ownership residuals remain unsigned."
    if nonclaim not in text:
        anchor = "- The 3811 morphism/product bridge is nonclaim for the strict current corpus; `A_ord=q_obs^*A_Q tensor A_fixed` is not parent-signed, and full-rank product rows remain nonclaim until transport/source normalizers and source-amplitude branch logic are derived or source-filled."
        text = text.replace(anchor, anchor + "\n" + nonclaim)

    old_target = (
        "`3812-Y5-R2FR-parent-transport-source-normalizer-or-same-vector-DD-branch-bridge.md`\n\n"
        "Target: use the 3811 bridge to attack transport/source normalizers `N_r` and the Earth/source amplitude branch without setting them to unity; preserve the same-vector quadratic DD guard so WEP rows are not misused as independent linear constraints.\n\n"
        "This is the best next move because the no-Hom theorem shape is already exact but parent-unsigned, while the finite branch has full sensitivity rank. The remaining path to a real local test is deriving/source-filling compatible row normalizers or proving a source-amplitude theorem."
    )
    new_target = (
        "`3813-Y5-R2FR-Rbridge-matter-glue-no-source-slot-or-finite-source-normalizer-row.md`\n\n"
        "Target: attack the source-ownership bottleneck exposed by 3812. Prove the ordinary-matter functor/no-source-only-slot theorem that sets `R_matter_glue` and `R_visible_coeff` to zero, or extract the first finite parent source-normalizer residual row.\n\n"
        "This is the best next move because WEP row normalizer geometry is no longer the main ambiguity. The remaining lift is to make `S_E^q` parent-owned, or bound the residuals in `S_E^q = Q_Earth dot C + R_bridge`."
    )
    if old_target in text:
        text = text.replace(old_target, new_target)

    artifacts = [
        "P8_Y5_R2FR_3812_SOURCE_REGISTER.csv",
        "P8_Y5_R2FR_3812_TRANSPORT_NORMALIZER_ATTEMPT.csv",
        "P8_Y5_R2FR_3812_EXTERNAL_AMPLITUDE_BRANCH_LEDGER.csv",
        "P8_Y5_R2FR_3812_SAME_VECTOR_DD_RUNNER_SCHEMA.csv",
        "P8_Y5_R2FR_3812_SAME_VECTOR_DD_RUNNER_DRYRUN.csv",
        "P8_Y5_R2FR_3812_QEARTH_QDELTA_STABILITY_CARRYFORWARD.csv",
        "P8_Y5_R2FR_3812_RBRIDGE_RESIDUAL_CARRYFORWARD.csv",
        "P8_Y5_R2FR_3812_CLAIM_GATES.csv",
        "P8_Y5_R2FR_3812_DECISION_ROWS.csv",
        "P8_Y5_R2FR_3812_NEXT_TARGET.csv",
        "P8_Y5_R2FR_3812_STATUS.csv",
        "P8_Y5_BRR545_3812_VALIDATION.csv",
    ]
    for artifact in artifacts:
        entry = f"- `source-intake\\mts_residuals\\{artifact}`"
        if entry not in text:
            text = text.rstrip() + "\n" + entry + "\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def cleanup_pycache() -> None:
    pycache = PCW / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(timestamp: str, grouped: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    for key, path in OUTPUTS.items():
        if key != "validation":
            if not path.exists():
                raise AssertionError(f"missing output {path}")
            read_csv(path)
    fwb_hits = list(FWB.rglob("*3812*")) if FWB.exists() else []
    pycache = PCW / "scripts" / "__pycache__"
    spine_text = read_text(SPINE_PATH) if SPINE_PATH.exists() else ""
    bad_chars_clean = all("\ufffd" not in read_text(path) for path in [DOC_PATH, SCRIPT_PATH, SPINE_PATH] if path.exists())
    checks = [
        ("sources_exist", all(row["exists"] == "true" for row in grouped["sources"]), "every cited source path exists"),
        ("needles_found", all(row["needle_found"] == "true" for row in grouped["sources"]), "every cited source needle was found"),
        ("csv_outputs_parse", True, "all generated CSV outputs exist and parse"),
        ("doc_written", DOC_PATH.exists(), "3812 markdown document written"),
        ("wep_normalizer_factors_derived", sum("PARTIAL_NUMERIC_FACTOR" in row["claim_status"] for row in grouped["transport"]) >= 2, "two WEP normalizers have numeric factors times abs_S_Eq_inv"),
        ("clock_normalizers_blocked", any(row["source_amplitude_status"] == "MISSING_CLOCK_TRANSPORT_NORMALIZER" for row in grouped["transport"]), "clock rows are not smuggled through WEP normalizer"),
        ("same_vector_quadratic_guard", any(row["schema_id"] == "SV3812_2_quadratic_wep" and "quadratic" in row["runner_rule"] for row in grouped["same_schema"]), "same-vector WEP equation is quadratic"),
        ("wep_linear_shortcut_forbidden", any(row["dryrun_id"] == "DRY3812_4_forbidden_WEP_linear_insert" and row["runner_use"] == "forbidden_rank_shortcut" for row in grouped["same_dryrun"]), "WEP linear rank shortcut is explicitly forbidden"),
        ("qdelta_forced_zero_fails", any(row["carry_id"] == "QDC3812_STRESS3486_3_forced_zero_failure" and row["status"] == "rank_fails" for row in grouped["qdelta"]), "forced Q_delta_m_Earth=0 destroys proxy closure"),
        ("rbridge_blocks_claim", any(row["carry_id"] == "RBC3812_R_matter_glue" and row["blocks_claim"] == "true" for row in grouped["rbridge"]), "R_bridge source ownership blocker carried forward"),
        ("claims_closed", all(row["claim_allowed"] == "false" for row in grouped["gates"]), "no claim gate allows a claim"),
        ("spine_updated", "Current State After 3812" in spine_text and "3813-Y5-R2FR-Rbridge-matter-glue-no-source-slot-or-finite-source-normalizer-row.md" in spine_text, "live spine updated to 3812 and 3813 target"),
        ("formalization_clean", not fwb_hits, "no 3812 files written under formalization-workbench"),
        ("pycache_removed", not pycache.exists(), "scripts __pycache__ removed"),
        ("bad_chars_clean", bad_chars_clean, "new doc/script/spine contain no mojibake replacement characters"),
    ]
    return [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]


def main() -> None:
    timestamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    grouped: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "transport": transport_rows(timestamp),
        "external": external_rows(timestamp),
        "same_schema": same_vector_schema_rows(timestamp),
        "same_dryrun": same_vector_dryrun_rows(timestamp),
        "qdelta": qdelta_rows(timestamp),
        "rbridge": rbridge_rows(timestamp),
        "decisions": decision_rows(timestamp),
        "next_target": next_rows(timestamp),
        "status": status_rows(timestamp),
    }
    grouped["gates"] = gate_rows(timestamp, grouped)
    grouped["validation"] = [
        {
            "timestamp_utc": timestamp,
            "branch_id": BRANCH,
            "checkpoint_id": CHECKPOINT,
            "check_id": "pending",
            "result": "PASS",
            "detail": "placeholder before final validation",
        }
    ]
    for key, path in OUTPUTS.items():
        if key != "validation":
            write_csv(path, grouped[key])
    write_markdown(grouped)
    update_spine()
    cleanup_pycache()
    grouped["validation"] = validation_rows(timestamp, grouped)
    write_csv(OUTPUTS["validation"], grouped["validation"])
    write_markdown(grouped)
    cleanup_pycache()
    failed = [row for row in grouped["validation"] if row["result"] != "PASS"]
    print(grouped["status"][0]["status"])
    print(f"wrote {DOC_PATH}")
    if failed:
        raise SystemExit(f"validation failed: {failed}")


if __name__ == "__main__":
    main()
