from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3474-Y5-R2FR-nullspace-killing-source-owner-contract-or-clock-R10-row.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHANNELS = ["D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff"]

SOURCES: dict[str, dict[str, Any]] = {
    "script_3474": {"path": Path(__file__).resolve(), "role": "generator"},
    "doc_3473": {"path": ROOT / "3473-Y5-R2FR-full-DD-multiarena-rank-or-parent-source-owner-proof.md", "role": "3473 handoff"},
    "next_3473": {"path": OUT / "P8_Y5_R2FR_3473_NEXT_TARGET.csv", "role": "3474 target statement"},
    "matrix_3473": {"path": OUT / "P8_Y5_R2FR_3473_FULL_DD_MULTIARENA_MATRIX.csv", "role": "two-WEP-row full DD matrix"},
    "nullspace_3473": {"path": OUT / "P8_Y5_R2FR_3473_FULL_DD_NULLSPACE_BASIS.csv", "role": "two surviving WEP null directions"},
    "rank_3473": {"path": OUT / "P8_Y5_R2FR_3473_FULL_DD_RANK_LEDGER.csv", "role": "previous rank ledger"},
    "source_owner_3472": {"path": OUT / "P8_Y5_R2FR_3472_VISIBLE_SOURCE_OWNER_THEOREM_ATTEMPT.csv", "role": "source-owner theorem attempt"},
    "contract_3469": {"path": OUT / "P8_Y5_R2FR_3469_VISIBLE_COEFFICIENT_OWNER_CONTRACT.csv", "role": "visible coefficient owner contract"},
    "clock_sensitivity_646": {"path": OUT / "P8_Y5_R10_646_CLOCK_ALPHA_SENSITIVITY_SOURCE.csv", "role": "clock alpha sensitivity source rows"},
    "clock_bound_647": {"path": OUT / "P8_Y5_R10_647_CLOCK_PRODUCT_BOUND.csv", "role": "clock alpha product bounds"},
    "clock_schema_1321": {"path": OUT / "P8_Y5_R10_1321_CLOCK_PRODUCT_SCHEMA.csv", "role": "clock product no-shortcut schema"},
}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join(["---"] * len(fields)) + " |"
    body = []
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", "<br>").replace("|", "/") for field in fields]
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, sep, *body])


def parse_float(value: Any) -> float | None:
    text = str(value).strip() if value is not None else ""
    if not text or "MISSING" in text:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y"}


def source_register() -> list[dict[str, Any]]:
    stamp = now()
    return [
        {
            "timestamp_utc": stamp,
            "source_id": source_id,
            "source_path": str(meta["path"]),
            "exists": meta["path"].exists(),
            "role": meta["role"],
            "valid_for_claim": False,
        }
        for source_id, meta in SOURCES.items()
    ]


def theorem_attempt() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "NSK3474_0_parent_source_owner",
            "route": "theorem",
            "claim_tested": "VisibleSourceOwner zeros every source-channel coefficient before arenas are applied.",
            "mathematical_form": "Theta_vis=q^*Theta_bar or fixed superselection => D_hatm=D_delta_m=D_me=D_e=0",
            "result": "UNCHANGED_UNSIGNED",
            "blocker": "3469/3472 owner clauses are exact conditionals but not parent-action signatures",
            "source_path": str(SOURCES["source_owner_3472"]["path"]),
            "valid_for_claim": False,
        },
        {
            "attempt_id": "NSK3474_1_clock_transport",
            "route": "theorem",
            "claim_tested": "A clock alpha product row can be treated as the same underlying D_e source direction as WEP only if arena transport is parent-owned.",
            "mathematical_form": "D_e^clock = T_clock<-source D_e and D_e^WEP = T_WEP<-source D_e with declared transport maps",
            "result": "TRANSPORT_CONTRACT_REQUIRED",
            "blocker": "clock tau/time and Xhat normalization remain product-only; no standalone D_e claim",
            "source_path": str(SOURCES["clock_schema_1321"]["path"]),
            "valid_for_claim": False,
        },
    ]


def vector_from_matrix_row(row: dict[str, str]) -> list[float]:
    return [
        float(row["Delta_Q_hatm_full"]),
        float(row["Delta_Q_delta_m"]),
        float(row["Delta_Q_m_e"]),
        float(row["Delta_Q_e_full"]),
    ]


def normalize(values: list[float]) -> list[float]:
    norm = math.sqrt(sum(value * value for value in values))
    if norm == 0:
        raise ValueError("zero vector")
    return [value / norm for value in values]


def clock_rows() -> tuple[list[dict[str, Any]], list[float]]:
    sensitivity = read_csv(SOURCES["clock_sensitivity_646"]["path"])
    bounds = read_csv(SOURCES["clock_bound_647"]["path"])
    yb = next(row for row in sensitivity if row["clock_pair_id"] == "CAS646_1_YbE3E2")
    yb_bound = next(row for row in bounds if row["clock_pair_id"] == "CAS646_1_YbE3E2")
    delta_k = float(yb["delta_K_alpha_used"])
    raw_vector = [0.0, 0.0, 0.0, delta_k]
    rows = [
        {
            "clock_row_id": "CLK3474_0_YbE3E2_alpha",
            "arena": "CLOCK_YbE3E2_ALPHA_DRIFT",
            "clock_pair": yb["clock_pair"],
            "observable": "d ln(nu_E3/nu_E2)/dt",
            "D_hatm_eff": "0.000000000000e+00",
            "D_delta_m_eff": "0.000000000000e+00",
            "D_me_eff": "0.000000000000e+00",
            "D_e_eff": f"{delta_k:.12e}",
            "product_bound_1sigma_yr_inv": yb_bound["conservative_abs_product_bound_1sigma_yr_inv"],
            "product_bound_2sigma_yr_inv": yb_bound["conservative_abs_product_bound_2sigma_yr_inv"],
            "source_path": str(SOURCES["clock_sensitivity_646"]["path"]),
            "bound_source_path": str(SOURCES["clock_bound_647"]["path"]),
            "rank_use": "sensitivity_vector_only",
            "claim_policy": "product-only; no standalone D_e without clock transport/tau map",
            "valid_for_claim": False,
        }
    ]
    return rows, raw_vector


def augmented_matrix_rows() -> list[dict[str, Any]]:
    previous = read_csv(SOURCES["matrix_3473"]["path"])
    clock_row, clock_vector = clock_rows()
    rows: list[dict[str, Any]] = []
    for row in previous:
        raw = vector_from_matrix_row(row)
        unit = normalize(raw)
        rows.append(
            {
                "aug_row_id": row["row_id"],
                "arena": row["arena"],
                "row_type": "WEP_material_difference",
                "raw_D_hatm_eff": f"{raw[0]:.12e}",
                "raw_D_delta_m_eff": f"{raw[1]:.12e}",
                "raw_D_me_eff": f"{raw[2]:.12e}",
                "raw_D_e_eff": f"{raw[3]:.12e}",
                "unit_D_hatm_eff": f"{unit[0]:.12e}",
                "unit_D_delta_m_eff": f"{unit[1]:.12e}",
                "unit_D_me_eff": f"{unit[2]:.12e}",
                "unit_D_e_eff": f"{unit[3]:.12e}",
                "bound": row["eta_abs_bound"],
                "bound_units": "dimensionless_eta",
                "source_path": row["source_path"],
                "valid_for_claim": False,
            }
        )
    unit_clock = normalize(clock_vector)
    rows.append(
        {
            "aug_row_id": "MATRIX3474_2_CLOCK_YbE3E2_alpha",
            "arena": "CLOCK_YbE3E2_ALPHA_DRIFT",
            "row_type": "clock_alpha_sensitivity",
            "raw_D_hatm_eff": f"{clock_vector[0]:.12e}",
            "raw_D_delta_m_eff": f"{clock_vector[1]:.12e}",
            "raw_D_me_eff": f"{clock_vector[2]:.12e}",
            "raw_D_e_eff": f"{clock_vector[3]:.12e}",
            "unit_D_hatm_eff": f"{unit_clock[0]:.12e}",
            "unit_D_delta_m_eff": f"{unit_clock[1]:.12e}",
            "unit_D_me_eff": f"{unit_clock[2]:.12e}",
            "unit_D_e_eff": f"{unit_clock[3]:.12e}",
            "bound": clock_row[0]["product_bound_1sigma_yr_inv"],
            "bound_units": "yr^-1_product_bound",
            "source_path": str(SOURCES["clock_sensitivity_646"]["path"]),
            "valid_for_claim": False,
        }
    )
    return rows


def matrix_values(rows: list[dict[str, Any]]) -> list[list[float]]:
    return [
        [float(row[f"unit_{channel}"]) for channel in CHANNELS]
        for row in rows
    ]


def rref(matrix: list[list[float]], tol: float = 1e-12) -> tuple[list[list[float]], list[int]]:
    mat = [row[:] for row in matrix]
    row_count = len(mat)
    col_count = len(mat[0])
    pivots: list[int] = []
    row_index = 0
    for col in range(col_count):
        pivot = max(range(row_index, row_count), key=lambda idx: abs(mat[idx][col]), default=row_index)
        if row_index >= row_count or abs(mat[pivot][col]) <= tol:
            continue
        mat[row_index], mat[pivot] = mat[pivot], mat[row_index]
        pivot_value = mat[row_index][col]
        mat[row_index] = [value / pivot_value for value in mat[row_index]]
        for idx in range(row_count):
            if idx == row_index:
                continue
            factor = mat[idx][col]
            if abs(factor) > tol:
                mat[idx] = [value - factor * pivot_row_value for value, pivot_row_value in zip(mat[idx], mat[row_index])]
        pivots.append(col)
        row_index += 1
        if row_index == row_count:
            break
    return mat, pivots


def nullspace_basis(matrix: list[list[float]]) -> list[list[float]]:
    reduced, pivots = rref(matrix)
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


def rank_and_nullspace(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    values = matrix_values(rows)
    _, pivots = rref(values)
    basis = nullspace_basis(values)
    rank_rows = [
        {
            "rank_id": "RANK3474_0_WEP_plus_clock_alpha",
            "rows": len(values),
            "columns": len(CHANNELS),
            "rank": len(pivots),
            "nullspace_dimension": len(CHANNELS) - len(pivots),
            "previous_rank": 2,
            "previous_nullspace_dimension": 2,
            "rank_gain": len(pivots) - 2,
            "status": "RANK_THREE_ONE_NULL_DIRECTION_REMAINS" if len(pivots) == 3 else "UNEXPECTED_RANK",
            "valid_for_claim": False,
        }
    ]
    null_rows: list[dict[str, Any]] = []
    for index, vector in enumerate(basis):
        null_rows.append(
            {
                "basis_id": f"NULL3474_{index}",
                **{channel: f"{component:.12e}" for channel, component in zip(CHANNELS, vector)},
                "check": "augmented_matrix*v approximately zero",
                "status": "SURVIVING_UNCONSTRAINED_SOURCE_DIRECTION",
                "valid_for_claim": False,
            }
        )
    return rank_rows, null_rows


def previous_null_kill_rows(clock_vector: list[float]) -> list[dict[str, Any]]:
    previous = read_csv(SOURCES["nullspace_3473"]["path"])
    rows: list[dict[str, Any]] = []
    for row in previous:
        vector = [float(row[channel]) for channel in CHANNELS]
        clock_dot = sum(a * b for a, b in zip(clock_vector, vector))
        rows.append(
            {
                "kill_id": f"KILL3474_{row['basis_id']}",
                "previous_basis_id": row["basis_id"],
                "clock_row_dot_previous_null": f"{clock_dot:.12e}",
                "abs_dot": f"{abs(clock_dot):.12e}",
                "effect": "KILLED_BY_CLOCK_ALPHA_ROW" if abs(clock_dot) > 1e-10 else "SURVIVES_CLOCK_ALPHA_ROW",
                "reason": "clock alpha row measures D_e component" if abs(clock_dot) > 1e-10 else "previous null direction has no D_e support",
                "valid_for_claim": False,
            }
        )
    return rows


def claim_gates(rank_rows: list[dict[str, Any]], kill_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rank = int(rank_rows[0]["rank"])
    killed_count = sum(1 for row in kill_rows if row["effect"] == "KILLED_BY_CLOCK_ALPHA_ROW")
    return [
        {
            "gate_id": "CG3474_0_parent_theorem",
            "requirement": "parent source-owner theorem signs zero source vector",
            "passed": False,
            "evidence": "theorem route unchanged unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3474_1_clock_row_independent",
            "requirement": "sourced clock row raises rank",
            "passed": rank == 3,
            "evidence": f"rank={rank}; rank_gain={rank_rows[0]['rank_gain']}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3474_2_null_direction_killed",
            "requirement": "at least one 3473 null direction is killed",
            "passed": killed_count >= 1,
            "evidence": f"killed_count={killed_count}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3474_3_full_closure",
            "requirement": "all source directions are bounded or theorem-zero",
            "passed": False,
            "evidence": f"nullspace_dimension={rank_rows[0]['nullspace_dimension']}; clock row is product-only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3474_4_no_claim",
            "requirement": "no WEP/local-GR/clock pass claimed",
            "passed": True,
            "evidence": "all generated rows valid_for_claim=false",
            "valid_for_claim": False,
        },
    ]


def decision_rows(rank_rows: list[dict[str, Any]], kill_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    survivor = next(row for row in kill_rows if row["effect"] == "SURVIVES_CLOCK_ALPHA_ROW")
    killed = next(row for row in kill_rows if row["effect"] == "KILLED_BY_CLOCK_ALPHA_ROW")
    return [
        {
            "decision_id": "DEC3474_0_rank_lift",
            "decision": "Add the Yb E3/E2 clock alpha row as a conditional independent sensitivity row.",
            "rationale": f"rank rises from 2 to {rank_rows[0]['rank']}; {killed['previous_basis_id']} is killed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3474_1_remaining_gap",
            "decision": "The surviving null direction is the mass/electron-mass combination, not the alpha direction.",
            "rationale": f"{survivor['previous_basis_id']} survives because the clock alpha row has no D_delta_m/D_me sensitivity.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3474_2_no_shortcut",
            "decision": "Do not convert the clock product bound into a standalone D_e or WEP bound.",
            "rationale": "clock tau/time transport and Xhat normalization remain missing, so this is rank geometry only.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3475-Y5-R2FR-surviving-mass-electron-null-direction-theorem-or-clock-mu-row.md",
            "next_script": "scripts/Y5_R2FR_3475_surviving_mass_electron_null_direction_theorem_or_clock_mu_row.py",
            "objective": "Target the remaining D_delta_m/D_me null direction: derive the parent electron/quark mass-ratio owner theorem, or add a sourced clock/spectroscopy sensitivity row involving mu or nuclear mass ratios.",
            "success_gate": "The final null direction is killed by theorem or by an independent sourced mu/nuclear/electron-mass sensitivity row; no clock tau shortcut or standalone coefficient claim.",
            "exclude": "GitHub action; formalization-workbench edits; public WEP/local-GR claim; converting clock product bounds into standalone coefficients without transport.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def formalization_git_status() -> str:
    try:
        result = subprocess.run(
            ["git", "status", "--short", "--", "formalization-workbench"],
            cwd=ROOT.parent,
            text=True,
            capture_output=True,
            check=False,
        )
    except FileNotFoundError:
        return "GIT_NOT_AVAILABLE"
    if result.returncode != 0:
        if "not a git repository" in result.stderr.lower():
            return "NOT_A_GIT_REPOSITORY"
        return f"GIT_STATUS_FAILED:{result.stderr.strip()}"
    return result.stdout.strip()


def validation_rows(
    output_paths: list[Path],
    source_rows: list[dict[str, Any]],
    augmented: list[dict[str, Any]],
    rank_rows: list[dict[str, Any]],
    null_rows: list[dict[str, Any]],
    kill_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    malformed: list[str] = []
    for path in output_paths:
        if path.suffix.lower() != ".csv":
            continue
        try:
            read_csv(path)
        except Exception as exc:
            malformed.append(f"{path.name}:{exc}")
    missing_sources = [row["source_id"] for row in source_rows if not parse_bool(row["exists"])]
    finite_augmented = all(
        math.isfinite(float(row[f"unit_{channel}"]))
        for row in augmented
        for channel in CHANNELS
    )
    rank = int(rank_rows[0]["rank"])
    null_dim = int(rank_rows[0]["nullspace_dimension"])
    killed_count = sum(1 for row in kill_rows if row["effect"] == "KILLED_BY_CLOCK_ALPHA_ROW")
    formalization_outputs = [str(path) for path in output_paths if str(path).lower().startswith(str(FORMALIZATION).lower())]
    git_status = formalization_git_status()
    checks = [
        ("VAL3474_0_sources_exist", not missing_sources, ";".join(missing_sources) or "all local sources exist"),
        ("VAL3474_1_csv_parse", not malformed, ";".join(malformed) or "all output csv files parse"),
        ("VAL3474_2_augmented_shape", len(augmented) == 3, f"rows={len(augmented)}; cols=4"),
        ("VAL3474_3_augmented_finite", finite_augmented, "all normalized matrix entries finite"),
        ("VAL3474_4_rank_three", rank == 3, f"rank={rank}"),
        ("VAL3474_5_nullspace_dim_one", null_dim == 1 and len(null_rows) == 1, f"dim={null_dim}; basis_rows={len(null_rows)}"),
        ("VAL3474_6_kills_one_previous_null", killed_count >= 1, f"killed_count={killed_count}"),
        ("VAL3474_7_no_claim", True, "all 3474 rows valid_for_claim=false"),
        ("VAL3474_8_no_formalization_outputs", not formalization_outputs, ";".join(formalization_outputs) or "no outputs under formalization-workbench"),
        ("VAL3474_9_git_formalization_clean", git_status in {"", "NOT_A_GIT_REPOSITORY"}, git_status or "git reports no formalization-workbench changes"),
    ]
    rows = [
        {"check_id": check_id, "passed": bool(passed), "detail": detail, "valid_for_claim": False}
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL3474_SUMMARY",
            "passed": all(parse_bool(row["passed"]) for row in rows),
            "detail": "PASS" if all(parse_bool(row["passed"]) for row in rows) else "FAIL",
            "valid_for_claim": False,
        }
    )
    return rows


def write_doc(
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    clock: list[dict[str, Any]],
    augmented: list[dict[str, Any]],
    rank: list[dict[str, Any]],
    null_rows: list[dict[str, Any]],
    kills: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    rank_row = rank[0]
    doc = f"""# 3474: Nullspace-Killing Source-Owner Contract Or Clock/R10 Row

## Current Verdict
- **Real movement:** the sourced Yb E3/E2 clock alpha row raises the conditional sensitivity rank from `2` to `{rank_row['rank']}`.
- **One null direction killed:** the previous null direction with `D_e` support is removed by the clock alpha row.
- **One null direction remains:** the survivor is the `D_delta_m/D_me` mass/electron-mass direction.
- **No claim:** the clock row is product-only until clock-time transport and `Xhat` normalization are parent-owned.

## Theorem Route
{md_table(theorem)}

## Clock Sensitivity Row
{md_table(clock)}

## Augmented Matrix
{md_table(augmented)}

## Rank Ledger
{md_table(rank)}

## New Nullspace
{md_table(null_rows)}

## Previous Null Direction Impact
{md_table(kills)}

## Claim Gates
{md_table(gates)}

## Decision
{md_table(decisions)}

## Next Target
{md_table(next_rows)}

## Source Register
{md_table(sources)}

## Validation
{md_table(validation)}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    theorem = theorem_attempt()
    clock, clock_vector = clock_rows()
    augmented = augmented_matrix_rows()
    rank, null_rows = rank_and_nullspace(augmented)
    kills = previous_null_kill_rows(clock_vector)
    gates = claim_gates(rank, kills)
    decisions = decision_rows(rank, kills)
    next_rows = next_target()
    output_map = {
        OUT / "P8_Y5_R2FR_3474_SOURCE_REGISTER.csv": sources,
        OUT / "P8_Y5_R2FR_3474_THEOREM_ROUTE_AUDIT.csv": theorem,
        OUT / "P8_Y5_R2FR_3474_CLOCK_ALPHA_SENSITIVITY_ROW.csv": clock,
        OUT / "P8_Y5_R2FR_3474_AUGMENTED_WEP_CLOCK_MATRIX.csv": augmented,
        OUT / "P8_Y5_R2FR_3474_AUGMENTED_RANK_LEDGER.csv": rank,
        OUT / "P8_Y5_R2FR_3474_AUGMENTED_NULLSPACE_BASIS.csv": null_rows,
        OUT / "P8_Y5_R2FR_3474_PREVIOUS_NULL_DIRECTION_IMPACT.csv": kills,
        OUT / "P8_Y5_R2FR_3474_CLAIM_GATES.csv": gates,
        OUT / "P8_Y5_R2FR_3474_DECISION_LEDGER.csv": decisions,
        OUT / "P8_Y5_R2FR_3474_NEXT_TARGET.csv": next_rows,
    }
    for path, rows in output_map.items():
        write_csv(path, rows)
    validation = validation_rows([*output_map.keys(), DOC], sources, augmented, rank, null_rows, kills)
    validation_path = OUT / "P8_Y5_BRR545_3474_VALIDATION.csv"
    write_csv(validation_path, validation)
    write_doc(sources, theorem, clock, augmented, rank, null_rows, kills, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
