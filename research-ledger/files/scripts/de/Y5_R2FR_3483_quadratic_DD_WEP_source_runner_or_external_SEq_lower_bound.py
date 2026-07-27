from __future__ import annotations

import csv
import math
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3483-Y5-R2FR-quadratic-DD-WEP-source-runner-or-external-SEq-lower-bound.md"
CHANNELS = ["D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff"]

SOURCES: dict[str, dict[str, Any]] = {
    "script_3483": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3482": {
        "path": ROOT / "3482-Y5-R2FR-earth-source-amplitude-SEq-current-bound-or-zero-theorem.md",
        "role": "3482 branch split handoff",
    },
    "earth_source_3482": {
        "path": OUT / "P8_Y5_R2FR_3482_EARTH_FULL_DD_SOURCE_VECTOR_NONCLAIM.csv",
        "role": "same-vector Earth DD source proxy",
    },
    "matrix_3475": {
        "path": OUT / "P8_Y5_R2FR_3475_AUGMENTED_FULL_RANK_MATRIX.csv",
        "role": "WEP and clock rows before same-vector correction",
    },
    "branch_logic_3482": {
        "path": OUT / "P8_Y5_R2FR_3482_SEQ_BRANCH_LOGIC.csv",
        "role": "external/source-zero/same-vector branch logic",
    },
    "obstructions_3482": {
        "path": OUT / "P8_Y5_R2FR_3482_SEQ_BOUND_OBSTRUCTION_THEOREMS.csv",
        "role": "lower-bound and quadratic-guard obstructions",
    },
    "wep_norm_3481": {
        "path": OUT / "P8_Y5_R2FR_3481_WEP_SHARED_EARTH_NORMALIZER_ROWS_NONCLAIM.csv",
        "role": "external-amplitude WEP normalizer rows",
    },
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def fmt(value: float) -> str:
    if math.isinf(value):
        return "inf"
    if math.isnan(value):
        return "nan"
    return f"{value:.12e}"


def as_bool_text(value: bool) -> str:
    return "True" if value else "False"


def vector_from_row(row: dict[str, str], prefix: str = "raw") -> list[float]:
    return [float(row[f"{prefix}_{channel}"]) for channel in CHANNELS]


def earth_vector() -> list[float]:
    row = read_csv(SOURCES["earth_source_3482"]["path"])[0]
    return [
        float(row["Q_hatm_full_Earth"]),
        float(row["Q_delta_m_Earth"]),
        float(row["Q_m_e_Earth"]),
        float(row["Q_e_full_Earth"]),
    ]


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(a: list[float]) -> float:
    return math.sqrt(dot(a, a))


def normalize(a: list[float]) -> list[float]:
    length = norm(a)
    if length == 0:
        return [0.0 for _ in a]
    return [x / length for x in a]


def rref(matrix: list[list[float]], tol: float = 1e-12) -> tuple[list[list[float]], list[int]]:
    rows = [row[:] for row in matrix]
    if not rows:
        return rows, []
    row_count = len(rows)
    col_count = len(rows[0])
    pivots: list[int] = []
    pivot_row = 0
    for col in range(col_count):
        best = max(range(pivot_row, row_count), key=lambda r: abs(rows[r][col]), default=pivot_row)
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
    cleaned = [[0.0 if abs(value) <= tol else value for value in row] for row in rows]
    return cleaned, pivots


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
        vec = [0.0] * col_count
        vec[free_col] = 1.0
        for row_index, pivot_col in enumerate(pivots):
            vec[pivot_col] = -reduced[row_index][free_col]
        basis.append(normalize(vec))
    return basis


def matrix_rows() -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    rows = read_csv(SOURCES["matrix_3475"]["path"])
    wep = [row for row in rows if row["row_type"] == "WEP_material_difference"]
    clocks = [row for row in rows if row["row_type"].startswith("clock_")]
    return wep, clocks


def input_register() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(meta["path"]),
            "exists": as_bool_text(Path(meta["path"]).exists()),
            "role": meta["role"],
            "valid_for_claim": "False",
        }
        for source_id, meta in SOURCES.items()
    ]


def theorem_rows(q_earth: list[float]) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "THM3483_0_same_vector_substitution",
            "statement": "If the Earth source amplitude is S_Eq = Q_Earth dot C, then every Earth-source WEP row is quadratic in C.",
            "derivation": "eta_AB = S_Eq(DeltaQ_AB dot C) = (Q_Earth dot C)(DeltaQ_AB dot C).",
            "consequence": "The two WEP rows cannot be inserted as independent linear rows in the 3475 rank matrix on this branch.",
            "numeric_support": f"||Q_Earth||={fmt(norm(q_earth))}",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3483_1_source_hyperplane_escape",
            "statement": "Same-vector WEP has an exact unbounded blind family whenever Q_Earth dot C = 0.",
            "derivation": "For any amplitude r and any unit u in ker(Q_Earth), eta_AB(r u)=r^2(Q_Earth dot u)(DeltaQ_AB dot u)=0.",
            "consequence": "WEP alone cannot globally bound coefficient amplitude in the same-vector branch.",
            "numeric_support": "dim ker(Q_Earth)=3 because Q_Earth is nonzero in four channels.",
            "valid_for_claim": "False",
        },
        {
            "theorem_id": "THM3483_2_clock_rows_needed_or_source_lower_bound",
            "statement": "A local coefficient bound needs either a parent lower bound |S_Eq| >= L_E > 0, enough independent linear non-WEP observables, or a parent rule excluding the Q_Earth dot C = 0 family.",
            "derivation": "Quadratic WEP products vanish on ker(Q_Earth), so additional rank must come from clocks/EM/orbital rows or from a source theorem.",
            "consequence": "The next derivation target is not another WEP normalizer; it is the missing fourth independent transport/readout row or a source-lower-bound theorem.",
            "numeric_support": "tested in rank ledger below",
            "valid_for_claim": "False",
        },
    ]


def blind_rows(q_earth: list[float], wep_rows: list[dict[str, str]], clock_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    wep_vectors = [vector_from_row(row) for row in wep_rows]
    clock_vectors = [vector_from_row(row) for row in clock_rows]
    tests: list[tuple[str, str, list[list[float]]]] = [
        ("BLIND3483_0_QEarth_kernel", "Q_Earth dot C = 0 source hyperplane", [q_earth]),
        (
            "BLIND3483_1_both_deltaQ_kernel",
            "DeltaQ_MICROSCOPE dot C = 0 and DeltaQ_EotWash dot C = 0",
            wep_vectors,
        ),
        (
            "BLIND3483_2_QEarth_plus_two_clocks",
            "Q_Earth dot C = 0 plus both current clock product rows vanish",
            [q_earth] + clock_vectors,
        ),
        (
            "BLIND3483_3_QEarth_plus_clocks_plus_one_WEP_delta",
            "Q_Earth dot C = 0 plus clocks plus first DeltaQ row",
            [q_earth] + clock_vectors + wep_vectors[:1],
        ),
    ]
    rows: list[dict[str, Any]] = []
    for test_id, condition, vectors in tests:
        test_rank = rank(vectors)
        basis = nullspace(vectors)
        first = basis[0] if basis else [0.0, 0.0, 0.0, 0.0]
        rows.append(
            {
                "blind_id": test_id,
                "condition": condition,
                "row_count": len(vectors),
                "rank": test_rank,
                "null_dim": 4 - test_rank,
                "unit_null_D_hatm_eff": fmt(first[0]),
                "unit_null_D_delta_m_eff": fmt(first[1]),
                "unit_null_D_me_eff": fmt(first[2]),
                "unit_null_D_e_eff": fmt(first[3]),
                "implication": "unbounded amplitude direction exists" if 4 - test_rank > 0 else "no null direction in four-channel proxy",
                "valid_for_claim": "False",
            }
        )
    return rows


def directional_bound(direction: list[float], q_earth: list[float], wep_rows: list[dict[str, str]]) -> tuple[float, str]:
    limits: list[tuple[float, str]] = []
    q_proj = dot(q_earth, direction)
    for row in wep_rows:
        delta = vector_from_row(row)
        product = abs(q_proj * dot(delta, direction))
        if product == 0:
            continue
        bound = float(row["bound"])
        limits.append((math.sqrt(bound / product), row["aug_row_id"]))
    if not limits:
        return math.inf, "WEP_SILENT_DIRECTION"
    value, source = min(limits, key=lambda item: item[0])
    return value, source


def clock_bound(direction: list[float], clock_rows: list[dict[str, str]]) -> tuple[float, str]:
    limits: list[tuple[float, str]] = []
    for row in clock_rows:
        vector = vector_from_row(row)
        projection = abs(dot(vector, direction))
        if projection == 0:
            continue
        try:
            bound = float(row["bound"])
        except ValueError:
            continue
        limits.append((bound / projection, row["aug_row_id"]))
    if not limits:
        return math.inf, "CLOCK_SILENT_DIRECTION"
    value, source = min(limits, key=lambda item: item[0])
    return value, source


def candidate_directions(q_earth: list[float], wep_rows: list[dict[str, str]], clock_rows: list[dict[str, str]]) -> list[tuple[str, list[float]]]:
    directions: list[tuple[str, list[float]]] = []
    basis = [
        ("basis_D_hatm_eff", [1.0, 0.0, 0.0, 0.0]),
        ("basis_D_delta_m_eff", [0.0, 1.0, 0.0, 0.0]),
        ("basis_D_me_eff", [0.0, 0.0, 1.0, 0.0]),
        ("basis_D_e_eff", [0.0, 0.0, 0.0, 1.0]),
        ("QEarth_direction", normalize(q_earth)),
    ]
    directions.extend(basis)
    for row in wep_rows + clock_rows:
        directions.append((f"row_{row['aug_row_id']}", normalize(vector_from_row(row))))
    for index, vec in enumerate(nullspace([q_earth])):
        directions.append((f"QEarth_null_{index}", vec))
    for index, vec in enumerate(nullspace([q_earth] + [vector_from_row(row) for row in clock_rows])):
        directions.append((f"QEarth_clock_null_{index}", vec))
    rng = random.Random(3483)
    for index in range(512):
        vec = [rng.gauss(0.0, 1.0) for _ in range(4)]
        directions.append((f"seed3483_random_{index:03d}", normalize(vec)))
    return directions


def direction_rows(q_earth: list[float], wep_rows: list[dict[str, str]], clock_rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    for label, direction in candidate_directions(q_earth, wep_rows, clock_rows):
        wep_limit, wep_source = directional_bound(direction, q_earth, wep_rows)
        clock_limit, clock_source = clock_bound(direction, clock_rows)
        rows.append(
            {
                "direction_id": label,
                "u_D_hatm_eff": fmt(direction[0]),
                "u_D_delta_m_eff": fmt(direction[1]),
                "u_D_me_eff": fmt(direction[2]),
                "u_D_e_eff": fmt(direction[3]),
                "QEarth_dot_u": fmt(dot(q_earth, direction)),
                "same_vector_WEP_r_limit": fmt(wep_limit),
                "same_vector_WEP_limiter": wep_source,
                "clock_product_r_limit_nonclaim": fmt(clock_limit),
                "clock_limiter_nonclaim": clock_source,
                "valid_for_claim": "False",
            }
        )
    finite_wep = [float(row["same_vector_WEP_r_limit"]) for row in rows if row["same_vector_WEP_r_limit"] != "inf"]
    finite_clock = [float(row["clock_product_r_limit_nonclaim"]) for row in rows if row["clock_product_r_limit_nonclaim"] != "inf"]
    silent_wep = sum(1 for row in rows if row["same_vector_WEP_r_limit"] == "inf")
    silent_clock = sum(1 for row in rows if row["clock_product_r_limit_nonclaim"] == "inf")
    summary = [
        {
            "summary_id": "DIR3483_0_sample_size",
            "value": len(rows),
            "detail": "deterministic basis/null/random unit directions",
            "valid_for_claim": "False",
        },
        {
            "summary_id": "DIR3483_1_finite_wep_min",
            "value": fmt(min(finite_wep)) if finite_wep else "nan",
            "detail": "smallest same-vector WEP amplitude envelope among sampled non-silent directions",
            "valid_for_claim": "False",
        },
        {
            "summary_id": "DIR3483_2_finite_wep_max",
            "value": fmt(max(finite_wep)) if finite_wep else "nan",
            "detail": "largest finite same-vector WEP amplitude envelope among sampled non-silent directions",
            "valid_for_claim": "False",
        },
        {
            "summary_id": "DIR3483_3_wep_silent_count",
            "value": silent_wep,
            "detail": "sampled directions where same-vector WEP product is exactly silent in floating arithmetic",
            "valid_for_claim": "False",
        },
        {
            "summary_id": "DIR3483_4_clock_product_min",
            "value": fmt(min(finite_clock)) if finite_clock else "nan",
            "detail": "nonclaim clock product envelope; not a coefficient bound without transport normalization",
            "valid_for_claim": "False",
        },
        {
            "summary_id": "DIR3483_5_clock_silent_count",
            "value": silent_clock,
            "detail": "sampled directions where current clock rows are silent",
            "valid_for_claim": "False",
        },
    ]
    return rows, summary


def branch_comparison_rows(blind: list[dict[str, Any]]) -> list[dict[str, Any]]:
    q_clock_blind = next(row for row in blind if row["blind_id"] == "BLIND3483_2_QEarth_plus_two_clocks")
    return [
        {
            "branch_id": "BR3483_0_external_amplitude_linear",
            "model": "S_Eq is parent-owned and independent of visible C",
            "math_form": "eta_AB = S_Eq(DeltaQ_AB dot C)",
            "can_use_3475_linear_rank": "only after |S_Eq| >= L_E > 0 is derived",
            "current_status": "blocked_by_missing_parent_lower_bound",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR3483_1_same_visible_vector_quadratic",
            "model": "S_Eq = Q_Earth dot C",
            "math_form": "eta_AB = (Q_Earth dot C)(DeltaQ_AB dot C)",
            "can_use_3475_linear_rank": "no",
            "current_status": f"blind_null_dim_with_two_clock_rows={q_clock_blind['null_dim']}",
            "valid_for_claim": "False",
        },
        {
            "branch_id": "BR3483_2_zero_source_current",
            "model": "J_q projects to local source silence",
            "math_form": "S_Eq = 0",
            "can_use_3475_linear_rank": "no",
            "current_status": "conditional_zero_not_parent_signed",
            "valid_for_claim": "False",
        },
    ]


def decision_rows(blind: list[dict[str, Any]]) -> list[dict[str, Any]]:
    q_clock_blind = next(row for row in blind if row["blind_id"] == "BLIND3483_2_QEarth_plus_two_clocks")
    null_dim = int(q_clock_blind["null_dim"])
    return [
        {
            "decision_id": "DEC3483_0_3475_rank_scope",
            "decision": "The 3475 full-rank result survives only on the external-amplitude branch, not on the same-visible-vector DD branch.",
            "rationale": "same-vector WEP rows are quadratic products and have a source-hyperplane escape.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3483_1_same_vector_status",
            "decision": "The same-vector branch is not dead, but it is under-ranked with the current two clock rows.",
            "rationale": f"Q_Earth plus the two current clock rows has null_dim={null_dim}; WEP is silent on Q_Earth dot C=0.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
        {
            "decision_id": "DEC3483_2_best_next_attack",
            "decision": "Add or derive a fourth independent non-WEP transport/readout row, or prove a parent lower bound that excludes Q_Earth dot C=0.",
            "rationale": "this is the shortest route to restoring a real four-channel local coefficient bound without smuggling S_Eq=1.",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3484-Y5-R2FR-fourth-nonWEP-row-or-QEarth-kernel-exclusion-theorem.md",
            "next_script": "scripts/Y5_R2FR_3484_fourth_nonWEP_row_or_QEarth_kernel_exclusion_theorem.py",
            "objective": "Try to close the one-dimensional blind direction by deriving a fourth independent non-WEP readout row, or prove a parent theorem excluding Q_Earth dot C = 0.",
            "success_gate": "rank(Q_Earth, clock/readout rows) = 4 or a parent-signed source lower bound exists",
            "forbidden_shortcuts": "using WEP rows as linear rank rows on the same-vector branch; setting S_Eq=1; claiming local GR",
            "claim_allowed": "False",
            "valid_for_claim": "False",
        }
    ]


def validation_rows(outputs: dict[str, Path], q_earth: list[float], wep_rows: list[dict[str, str]], clock_rows: list[dict[str, str]], blind: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    rows.append(
        {
            "check_id": "VAL3483_0_sources_exist",
            "passed": all(Path(meta["path"]).exists() for meta in SOURCES.values()),
            "detail": "all local sources exist",
            "valid_for_claim": "False",
        }
    )
    parse_details = []
    parse_ok = True
    for name, path in outputs.items():
        try:
            parsed = read_csv(path)
            parse_details.append(f"{name}:{len(parsed)}")
        except Exception as exc:
            parse_ok = False
            parse_details.append(f"{name}:ERROR:{exc}")
    rows.append(
        {
            "check_id": "VAL3483_1_csv_parse",
            "passed": parse_ok,
            "detail": "; ".join(parse_details),
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3483_2_inputs_present",
            "passed": norm(q_earth) > 0 and len(wep_rows) >= 2 and len(clock_rows) >= 2,
            "detail": f"earth_norm={fmt(norm(q_earth))}; wep_rows={len(wep_rows)}; clock_rows={len(clock_rows)}",
            "valid_for_claim": "False",
        }
    )
    q_kernel = next(row for row in blind if row["blind_id"] == "BLIND3483_0_QEarth_kernel")
    rows.append(
        {
            "check_id": "VAL3483_3_source_hyperplane_exists",
            "passed": int(q_kernel["null_dim"]) == 3,
            "detail": f"rank={q_kernel['rank']}; null_dim={q_kernel['null_dim']}",
            "valid_for_claim": "False",
        }
    )
    q_clock = next(row for row in blind if row["blind_id"] == "BLIND3483_2_QEarth_plus_two_clocks")
    rows.append(
        {
            "check_id": "VAL3483_4_current_clock_rows_under_ranked",
            "passed": int(q_clock["null_dim"]) >= 1,
            "detail": f"rank={q_clock['rank']}; null_dim={q_clock['null_dim']}",
            "valid_for_claim": "False",
        }
    )
    all_rows: list[dict[str, str]] = []
    for path in outputs.values():
        all_rows.extend(read_csv(path))
    rows.append(
        {
            "check_id": "VAL3483_5_no_claim",
            "passed": all(row.get("valid_for_claim") == "False" for row in all_rows),
            "detail": "all generated rows valid_for_claim=false",
            "valid_for_claim": "False",
        }
    )
    rows.append(
        {
            "check_id": "VAL3483_6_no_formalization_outputs",
            "passed": all(FORMALIZATION not in path.parents for path in outputs.values()),
            "detail": "outputs are under post-checkpoint-work/source-intake only",
            "valid_for_claim": "False",
        }
    )
    summary_passed = all(str(row["passed"]) == "True" for row in rows)
    rows.append(
        {
            "check_id": "VAL3483_SUMMARY",
            "passed": summary_passed,
            "detail": "PASS" if summary_passed else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join([header, sep] + body)


def write_doc(
    q_earth: list[float],
    theorem: list[dict[str, Any]],
    blind: list[dict[str, Any]],
    summary: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 3483: Quadratic DD WEP Source Runner Or External `S_Eq` Lower Bound",
                "",
                "## Current Verdict",
                "- **Real derivation result:** on the same-visible-vector branch, WEP is quadratic: `eta_AB = (Q_Earth dot C)(DeltaQ_AB dot C)`.",
                "- **Important consequence:** WEP has an exact source-hyperplane blind family `Q_Earth dot C = 0`, so WEP alone cannot bound the four-channel coefficient vector.",
                "- **Scope correction:** the 3475 full-rank linear inversion is only valid on the external-amplitude branch after `|S_Eq| >= L_E > 0`; it is not valid on the same-vector DD branch.",
                "- **Not dead:** the same-vector route remains mathematically meaningful, but it now needs one more independent non-WEP row or a parent source lower-bound theorem.",
                "- **No claim:** no local-GR, WEP, clock, or source-coupling pass is claimed here.",
                "",
                "## Earth Source Vector Used",
                f"- `Q_Earth = ({fmt(q_earth[0])}, {fmt(q_earth[1])}, {fmt(q_earth[2])}, {fmt(q_earth[3])})` in the full-DD four-channel proxy basis.",
                f"- `||Q_Earth|| = {fmt(norm(q_earth))}`.",
                "",
                "## Quadratic WEP Theorems",
                md_table(theorem, ["theorem_id", "statement", "derivation", "consequence", "numeric_support", "valid_for_claim"]),
                "",
                "## Blind Direction Ledger",
                md_table(
                    blind,
                    [
                        "blind_id",
                        "condition",
                        "rank",
                        "null_dim",
                        "unit_null_D_hatm_eff",
                        "unit_null_D_delta_m_eff",
                        "unit_null_D_me_eff",
                        "unit_null_D_e_eff",
                        "implication",
                        "valid_for_claim",
                    ],
                ),
                "",
                "## Directional Smoke Summary",
                md_table(summary, ["summary_id", "value", "detail", "valid_for_claim"]),
                "",
                "## Branch Comparison",
                md_table(branches, ["branch_id", "model", "math_form", "can_use_3475_linear_rank", "current_status", "valid_for_claim"]),
                "",
                "## Decision Ledger",
                md_table(decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "passed", "detail", "valid_for_claim"]),
                "",
                f"_Generated: {now()}_",
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    q_earth = earth_vector()
    wep_rows, clock_rows = matrix_rows()
    theorem = theorem_rows(q_earth)
    blind = blind_rows(q_earth, wep_rows, clock_rows)
    directions, direction_summary = direction_rows(q_earth, wep_rows, clock_rows)
    branches = branch_comparison_rows(blind)
    decisions = decision_rows(blind)
    next_rows = next_target_rows()

    outputs = {
        "input_register": OUT / "P8_Y5_R2FR_3483_INPUT_REGISTER.csv",
        "quadratic_theorem": OUT / "P8_Y5_R2FR_3483_QUADRATIC_WEP_THEOREM.csv",
        "blind_directions": OUT / "P8_Y5_R2FR_3483_BLIND_DIRECTION_LEDGER.csv",
        "directional_smoke": OUT / "P8_Y5_R2FR_3483_DIRECTIONAL_SMOKE_SAMPLE.csv",
        "directional_summary": OUT / "P8_Y5_R2FR_3483_DIRECTIONAL_ENVELOPE_SUMMARY.csv",
        "branch_comparison": OUT / "P8_Y5_R2FR_3483_BRANCH_COMPARISON.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3483_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3483_NEXT_TARGET.csv",
    }
    write_csv(outputs["input_register"], input_register(), ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["quadratic_theorem"], theorem, ["theorem_id", "statement", "derivation", "consequence", "numeric_support", "valid_for_claim"])
    write_csv(
        outputs["blind_directions"],
        blind,
        [
            "blind_id",
            "condition",
            "row_count",
            "rank",
            "null_dim",
            "unit_null_D_hatm_eff",
            "unit_null_D_delta_m_eff",
            "unit_null_D_me_eff",
            "unit_null_D_e_eff",
            "implication",
            "valid_for_claim",
        ],
    )
    write_csv(
        outputs["directional_smoke"],
        directions,
        [
            "direction_id",
            "u_D_hatm_eff",
            "u_D_delta_m_eff",
            "u_D_me_eff",
            "u_D_e_eff",
            "QEarth_dot_u",
            "same_vector_WEP_r_limit",
            "same_vector_WEP_limiter",
            "clock_product_r_limit_nonclaim",
            "clock_limiter_nonclaim",
            "valid_for_claim",
        ],
    )
    write_csv(outputs["directional_summary"], direction_summary, ["summary_id", "value", "detail", "valid_for_claim"])
    write_csv(outputs["branch_comparison"], branches, ["branch_id", "model", "math_form", "can_use_3475_linear_rank", "current_status", "valid_for_claim"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "claim_allowed", "valid_for_claim"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed", "valid_for_claim"])
    validation = validation_rows(outputs, q_earth, wep_rows, clock_rows, blind)
    validation_path = OUT / "P8_Y5_BRR545_3483_VALIDATION.csv"
    write_csv(validation_path, validation, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(q_earth, theorem, blind, direction_summary, branches, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
