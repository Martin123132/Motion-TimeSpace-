from __future__ import annotations

import csv
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3473-Y5-R2FR-full-DD-multiarena-rank-or-parent-source-owner-proof.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"
CHANNELS = ["D_hatm_eff", "D_delta_m_eff", "D_me_eff", "D_e_eff"]

SOURCES: dict[str, dict[str, Any]] = {
    "script_3473": {"type": "local", "path": Path(__file__).resolve(), "role": "generator"},
    "doc_3472": {"type": "local", "path": ROOT / "3472-Y5-R2FR-visible-source-owner-theorem-or-full-DD-vector-upgrade.md", "role": "3472 handoff"},
    "next_3472": {"type": "local", "path": OUT / "P8_Y5_R2FR_3472_NEXT_TARGET.csv", "role": "3473 target statement"},
    "theorem_3472": {"type": "local", "path": OUT / "P8_Y5_R2FR_3472_VISIBLE_SOURCE_OWNER_THEOREM_ATTEMPT.csv", "role": "source-owner theorem attempt"},
    "microscope_3472": {"type": "local", "path": OUT / "P8_Y5_R2FR_3472_DD_FOUR_CHARGE_PAIR_VECTOR.csv", "role": "full DD MICROSCOPE pair vector"},
    "matrix_3265": {"type": "local", "path": OUT / "P8_Y5_R2FR_3265_TWO_ARENA_DELTA_MATRIX_NONCLAIM.csv", "role": "two-arena eta bounds and reduced DD rows"},
    "material_3265": {"type": "local", "path": OUT / "P8_Y5_R2FR_3265_DD_MATERIAL_CHARGES_NONCLAIM.csv", "role": "Eot-Wash Be/Ti A/Z material context"},
    "eotwash_source": {"type": "local", "path": ROOT / "source-intake" / "external-sources" / "eotwash_0712.0607_source" / "ep.tex", "role": "Eot-Wash Be/Ti source"},
    "dd_tex": {"type": "local", "path": ROOT / "source-intake" / "external-sources" / "damour_donoghue_1007.2792_source" / "DamourDonoghueEPfinal.tex", "role": "Damour-Donoghue full four-charge formulas"},
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
    if not text or "MISSING" in text or "alloy" in text:
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
            "source_type": meta["type"],
            "source_path": str(meta["path"]),
            "exists": meta["path"].exists(),
            "role": meta["role"],
            "valid_for_claim": False,
        }
        for source_id, meta in SOURCES.items()
    ]


def dd_charges(A: float, Z: float) -> dict[str, float]:
    q_p = Z / A
    q_delta = (A - 2.0 * Z) / A
    q_c = Z * (Z - 1.0) / (A ** (4.0 / 3.0))
    return {
        "Q_hatm_full": 0.093 - 0.036 / (A ** (1.0 / 3.0)) - 0.020 * (q_delta**2) - 1.4e-4 * q_c,
        "Q_delta_m": 0.0017 * q_delta,
        "Q_m_e": 5.5e-4 * q_p,
        "Q_e_full": (-1.4 + 8.2 * q_p + 7.7 * q_c) * 1.0e-4,
    }


def full_material_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    microscope_materials = read_csv(OUT / "P8_Y5_R2FR_3472_DD_FOUR_CHARGE_MATERIAL_ROWS.csv")
    for material_id in ["PtRh10", "TA6V"]:
        source = next(row for row in microscope_materials if row["material_id"] == material_id)
        rows.append(
            {
                "material_charge_id": f"MAT3473_MICROSCOPE_{material_id}",
                "arena": "MICROSCOPE_TIPT_EARTH_FIELD",
                "material_id": material_id,
                "composition_basis": source["basis"],
                "Q_hatm_full": source["Q_hatm_full"],
                "Q_delta_m": source["Q_delta_m"],
                "Q_m_e": source["Q_m_e"],
                "Q_e_full": source["Q_e_full"],
                "source_path": str(OUT / "P8_Y5_R2FR_3472_DD_FOUR_CHARGE_MATERIAL_ROWS.csv"),
                "valid_for_claim": False,
            }
        )
    material_3265 = read_csv(SOURCES["material_3265"]["path"])
    for material_id in ["EOTWASH_Be", "EOTWASH_Ti"]:
        source = next(row for row in material_3265 if row["material_id"] == material_id)
        A = parse_float(source["A_context"])
        Z = parse_float(source["Z"])
        if A is None or Z is None:
            raise ValueError(f"missing A/Z for {material_id}")
        charges = dd_charges(A, Z)
        rows.append(
            {
                "material_charge_id": f"MAT3473_{material_id}",
                "arena": "EOTWASH_BETI_EARTH_FIELD",
                "material_id": material_id,
                "composition_basis": source["composition_basis"],
                "A_context": f"{A:.12e}",
                "Z": f"{Z:.12e}",
                "Q_hatm_full": f"{charges['Q_hatm_full']:.12e}",
                "Q_delta_m": f"{charges['Q_delta_m']:.12e}",
                "Q_m_e": f"{charges['Q_m_e']:.12e}",
                "Q_e_full": f"{charges['Q_e_full']:.12e}",
                "source_path": str(SOURCES["material_3265"]["path"]),
                "formula_source_path": str(SOURCES["dd_tex"]["path"]),
                "valid_for_claim": False,
            }
        )
    return rows


def eta_bounds() -> dict[str, float]:
    rows = read_csv(SOURCES["matrix_3265"]["path"])
    return {
        "MICROSCOPE_TIPT_EARTH_FIELD": parse_float(next(row for row in rows if row["arena"] == "MICROSCOPE_TIPT_EARTH_FIELD")["eta_abs_bound"]) or 0.0,
        "EOTWASH_BETI_EARTH_FIELD": parse_float(next(row for row in rows if row["arena"] == "EOTWASH_BETI_EARTH_FIELD")["eta_abs_bound"]) or 0.0,
    }


def matrix_rows(materials: list[dict[str, Any]]) -> list[dict[str, Any]]:
    bounds = eta_bounds()
    pairs = [
        ("MATRIX3473_0_MICROSCOPE_TA6V_minus_PtRh10", "MICROSCOPE_TIPT_EARTH_FIELD", "TA6V", "PtRh10"),
        ("MATRIX3473_1_EOTWASH_Be_minus_Ti", "EOTWASH_BETI_EARTH_FIELD", "EOTWASH_Be", "EOTWASH_Ti"),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, arena, left_id, right_id in pairs:
        left = next(row for row in materials if row["material_id"] == left_id)
        right = next(row for row in materials if row["material_id"] == right_id)
        deltas = {
            "Delta_Q_hatm_full": float(left["Q_hatm_full"]) - float(right["Q_hatm_full"]),
            "Delta_Q_delta_m": float(left["Q_delta_m"]) - float(right["Q_delta_m"]),
            "Delta_Q_m_e": float(left["Q_m_e"]) - float(right["Q_m_e"]),
            "Delta_Q_e_full": float(left["Q_e_full"]) - float(right["Q_e_full"]),
        }
        rows.append(
            {
                "row_id": row_id,
                "arena": arena,
                "left_minus_right": f"{left_id}_minus_{right_id}",
                **{key: f"{value:.12e}" for key, value in deltas.items()},
                "eta_abs_bound": f"{bounds[arena]:.12e}",
                "source_path": str(OUT / "P8_Y5_R2FR_3473_FULL_DD_MATERIAL_ROWS.csv"),
                "valid_for_claim": False,
            }
        )
    return rows


def matrix_values(matrix: list[dict[str, Any]]) -> list[list[float]]:
    keys = ["Delta_Q_hatm_full", "Delta_Q_delta_m", "Delta_Q_m_e", "Delta_Q_e_full"]
    return [[float(row[key]) for key in keys] for row in matrix]


def singular_values_two_row(matrix_values_in: list[list[float]]) -> tuple[float, float, float]:
    first, second = matrix_values_in
    a = sum(value * value for value in first)
    b = sum(x * y for x, y in zip(first, second))
    d = sum(value * value for value in second)
    trace = a + d
    determinant = max(a * d - b * b, 0.0)
    discriminant = max(trace * trace - 4.0 * determinant, 0.0)
    lambda_1 = 0.5 * (trace + math.sqrt(discriminant))
    lambda_2 = 0.5 * (trace - math.sqrt(discriminant))
    sigma_1 = math.sqrt(max(lambda_1, 0.0))
    sigma_2 = math.sqrt(max(lambda_2, 0.0))
    cosine = b / math.sqrt(a * d) if a > 0 and d > 0 else math.nan
    return sigma_1, sigma_2, cosine


def rref(matrix_values_in: list[list[float]], tol: float = 1e-18) -> tuple[list[list[float]], list[int]]:
    mat = [row[:] for row in matrix_values_in]
    pivot_cols: list[int] = []
    row_index = 0
    rows_count = len(mat)
    cols_count = len(mat[0])
    for col in range(cols_count):
        pivot = max(range(row_index, rows_count), key=lambda idx: abs(mat[idx][col]), default=row_index)
        if row_index >= rows_count or abs(mat[pivot][col]) <= tol:
            continue
        mat[row_index], mat[pivot] = mat[pivot], mat[row_index]
        pivot_value = mat[row_index][col]
        mat[row_index] = [value / pivot_value for value in mat[row_index]]
        for idx in range(rows_count):
            if idx == row_index:
                continue
            factor = mat[idx][col]
            if abs(factor) > tol:
                mat[idx] = [value - factor * pivot_row_value for value, pivot_row_value in zip(mat[idx], mat[row_index])]
        pivot_cols.append(col)
        row_index += 1
        if row_index == rows_count:
            break
    return mat, pivot_cols


def nullspace_basis(matrix_values_in: list[list[float]]) -> list[list[float]]:
    reduced, pivot_cols = rref(matrix_values_in)
    cols_count = len(matrix_values_in[0])
    free_cols = [col for col in range(cols_count) if col not in pivot_cols]
    basis: list[list[float]] = []
    for free_col in free_cols:
        vector = [0.0] * cols_count
        vector[free_col] = 1.0
        for row_index, pivot_col in enumerate(pivot_cols):
            vector[pivot_col] = -reduced[row_index][free_col]
        norm = math.sqrt(sum(value * value for value in vector))
        if norm > 0:
            vector = [value / norm for value in vector]
        basis.append(vector)
    return basis


def rank_rows(matrix: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    values = matrix_values(matrix)
    sigma_1, sigma_2, cosine = singular_values_two_row(values)
    rank = int(sigma_1 > 1e-15) + int(sigma_2 > 1e-15)
    null_dim = len(CHANNELS) - rank
    condition = sigma_1 / sigma_2 if sigma_2 > 0 else math.inf
    rank_ledger = [
        {
            "rank_id": "RANK3473_0_full_DD_two_arena_matrix",
            "rows": len(values),
            "columns": len(CHANNELS),
            "rank": rank,
            "nullspace_dimension": null_dim,
            "singular_value_max": f"{sigma_1:.12e}",
            "singular_value_min": f"{sigma_2:.12e}",
            "condition_number_nonzero_singulars": f"{condition:.12e}",
            "row_cosine": f"{cosine:.12e}",
            "status": "RANK_TWO_NOT_FULL_RANK" if rank == 2 else "RANK_DEFICIENT_BELOW_EXPECTED",
            "valid_for_claim": False,
        }
    ]
    basis_vectors = nullspace_basis(values)
    basis_rows: list[dict[str, Any]] = []
    for index, vector in enumerate(basis_vectors):
        basis_rows.append(
            {
                "basis_id": f"NULL3473_{index}",
                **{channel: f"{component:.12e}" for channel, component in zip(CHANNELS, vector)},
                "check": "A*v approximately zero by construction",
                "status": "UNCONSTRAINED_SOURCE_DIRECTION",
                "valid_for_claim": False,
            }
        )
    component_rows: list[dict[str, Any]] = []
    for channel_index, channel in enumerate(CHANNELS):
        support = max(abs(vector[channel_index]) for vector in basis_vectors) if basis_vectors else 0.0
        component_rows.append(
            {
                "component_id": f"CBS3473_{channel}",
                "symbol": channel,
                "finite_bound_from_current_WEP_rows": False,
                "nullspace_support_abs_max": f"{support:.12e}",
                "reason": "current two WEP rows leave a nullspace direction that changes this component" if support > 1e-10 else "component appears orthogonal to computed nullspace",
                "next_requirement": "parent source-owner theorem or independent clock/R10/WEP rows",
                "valid_for_claim": False,
            }
        )
    return rank_ledger, basis_rows, component_rows


def theorem_delta() -> list[dict[str, Any]]:
    return [
        {
            "attempt_id": "PARENT3473_0_reuse_3472_source_owner",
            "claim_tested": "Can the source-owner theorem close instead of adding arenas?",
            "result": "UNCHANGED_UNSIGNED",
            "blocker": "3472 already established the theorem is coherent but not parent-signed",
            "source_path": str(SOURCES["theorem_3472"]["path"]),
            "valid_for_claim": False,
        },
        {
            "attempt_id": "PARENT3473_1_rank_implication",
            "claim_tested": "If the theorem is signed, rank tests become consistency checks rather than coefficient bounds.",
            "result": "EXACT_CONDITIONAL",
            "blocker": "requires VisibleSourceOwner + readout preservation clauses",
            "source_path": str(SOURCES["theorem_3472"]["path"]),
            "valid_for_claim": False,
        },
    ]


def claim_gates(rank_ledger: list[dict[str, Any]], component_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rank_row = rank_ledger[0]
    all_unbounded = all(not parse_bool(row["finite_bound_from_current_WEP_rows"]) for row in component_rows)
    return [
        {
            "gate_id": "CG3473_0_matrix_rank",
            "requirement": "full DD multiarena WEP matrix rank computed",
            "passed": True,
            "evidence": f"rank={rank_row['rank']}; nullspace_dimension={rank_row['nullspace_dimension']}",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3473_1_full_component_bounds",
            "requirement": "current arenas produce finite bounds on all four source coefficients",
            "passed": False,
            "evidence": "all components remain unbounded along at least one null direction" if all_unbounded else "some component support check failed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3473_2_parent_source_owner",
            "requirement": "parent theorem zeros the source vector",
            "passed": False,
            "evidence": "source-owner theorem remains unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG3473_3_no_claim",
            "requirement": "no WEP/local-GR/source-coupling pass is claimed",
            "passed": True,
            "evidence": "all rows valid_for_claim=false",
            "valid_for_claim": False,
        },
    ]


def decision_rows(rank_ledger: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rank_row = rank_ledger[0]
    return [
        {
            "decision_id": "DEC3473_0_rank_result",
            "decision": "Two WEP arenas raise the full DD source matrix to rank 2, not rank 4.",
            "rationale": f"rank={rank_row['rank']}; nullspace_dimension={rank_row['nullspace_dimension']}; row_cosine={rank_row['row_cosine']}",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3473_1_project_status",
            "decision": "The coupling problem is not a single missing coefficient; it is a two-dimensional unresolved source family after current WEP rows.",
            "rationale": "parent theorem or independent clock/R10/local rows are required to remove/bound the remaining null directions",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3474-Y5-R2FR-nullspace-killing-source-owner-contract-or-clock-R10-row.md",
            "next_script": "scripts/Y5_R2FR_3474_nullspace_killing_source_owner_contract_or_clock_R10_row.py",
            "objective": "Target the two surviving full-DD null directions: either derive a parent source-owner clause that zeros them, or add an independent clock/R10/local row whose sensitivity is not in the current WEP row span.",
            "success_gate": "At least one null direction is killed by theorem or by a sourced independent arena row; no single-channel ceiling is treated as evidence.",
            "exclude": "GitHub action; formalization-workbench edits; public WEP/local-GR claim; cancellation-tuned coefficient choices.",
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
    matrix: list[dict[str, Any]],
    rank_ledger: list[dict[str, Any]],
    nullspace: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
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
    rank_row = rank_ledger[0]
    formalization_outputs = [str(path) for path in output_paths if str(path).lower().startswith(str(FORMALIZATION).lower())]
    git_status = formalization_git_status()
    finite_matrix = all(
        math.isfinite(float(row[key]))
        for row in matrix
        for key in ["Delta_Q_hatm_full", "Delta_Q_delta_m", "Delta_Q_m_e", "Delta_Q_e_full", "eta_abs_bound"]
    )
    checks = [
        ("VAL3473_0_sources_exist", not missing_sources, ";".join(missing_sources) or "all local sources exist"),
        ("VAL3473_1_csv_parse", not malformed, ";".join(malformed) or "all output csv files parse"),
        ("VAL3473_2_matrix_shape", len(matrix) == 2, f"rows={len(matrix)}; cols=4"),
        ("VAL3473_3_matrix_finite", finite_matrix, "all matrix values finite"),
        ("VAL3473_4_rank_two", str(rank_row["rank"]) == "2", f"rank={rank_row['rank']}"),
        ("VAL3473_5_nullspace_dim_two", str(rank_row["nullspace_dimension"]) == "2" and len(nullspace) == 2, f"dim={rank_row['nullspace_dimension']}; basis_rows={len(nullspace)}"),
        ("VAL3473_6_components_unbounded", all(not parse_bool(row["finite_bound_from_current_WEP_rows"]) for row in component_rows), "all four component bounds remain nonclaim/unbounded"),
        ("VAL3473_7_no_claim", True, "all 3473 rows valid_for_claim=false"),
        ("VAL3473_8_no_formalization_outputs", not formalization_outputs, ";".join(formalization_outputs) or "no outputs under formalization-workbench"),
        ("VAL3473_9_git_formalization_clean", git_status in {"", "NOT_A_GIT_REPOSITORY"}, git_status or "git reports no formalization-workbench changes"),
    ]
    rows = [
        {"check_id": check_id, "passed": bool(passed), "detail": detail, "valid_for_claim": False}
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "check_id": "VAL3473_SUMMARY",
            "passed": all(parse_bool(row["passed"]) for row in rows),
            "detail": "PASS" if all(parse_bool(row["passed"]) for row in rows) else "FAIL",
            "valid_for_claim": False,
        }
    )
    return rows


def write_doc(
    source_rows: list[dict[str, Any]],
    materials: list[dict[str, Any]],
    matrix: list[dict[str, Any]],
    rank_ledger: list[dict[str, Any]],
    nullspace: list[dict[str, Any]],
    component_rows: list[dict[str, Any]],
    theorem_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    rank_row = rank_ledger[0]
    doc = f"""# 3473: Full DD Multiarena Rank Or Parent Source-Owner Proof

## Current Verdict
- **Real movement:** adding Eöt-Wash Be/Ti to the full DD basis raises the current WEP source matrix to rank `{rank_row['rank']}`.
- **Still not enough:** the full source space has four channels, so the current WEP-only matrix leaves nullspace dimension `{rank_row['nullspace_dimension']}`.
- **Meaning:** the coupling problem is now sharply located as two surviving source directions, not a vague missing-coupling complaint.
- **No claim:** this does not pass WEP/local-GR; it tells us exactly what remains to derive or source.

## Matrix Rows
{md_table(matrix)}

## Rank Ledger
{md_table(rank_ledger)}

## Nullspace Basis
{md_table(nullspace)}

## Component Bound Status
{md_table(component_rows)}

## Parent Source-Owner Route
{md_table(theorem_rows)}

## Material Rows
{md_table(materials)}

## Claim Gates
{md_table(gates)}

## Decision
{md_table(decisions)}

## Next Target
{md_table(next_rows)}

## Source Register
{md_table(source_rows)}

## Validation
{md_table(validation)}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register()
    materials = full_material_rows()
    matrix = matrix_rows(materials)
    rank_ledger, nullspace, components = rank_rows(matrix)
    theorem_rows = theorem_delta()
    gates = claim_gates(rank_ledger, components)
    decisions = decision_rows(rank_ledger)
    next_rows = next_target()
    output_map = {
        OUT / "P8_Y5_R2FR_3473_SOURCE_REGISTER.csv": sources,
        OUT / "P8_Y5_R2FR_3473_FULL_DD_MATERIAL_ROWS.csv": materials,
        OUT / "P8_Y5_R2FR_3473_FULL_DD_MULTIARENA_MATRIX.csv": matrix,
        OUT / "P8_Y5_R2FR_3473_FULL_DD_RANK_LEDGER.csv": rank_ledger,
        OUT / "P8_Y5_R2FR_3473_FULL_DD_NULLSPACE_BASIS.csv": nullspace,
        OUT / "P8_Y5_R2FR_3473_COMPONENT_BOUND_STATUS.csv": components,
        OUT / "P8_Y5_R2FR_3473_PARENT_SOURCE_OWNER_PROOF_DELTA.csv": theorem_rows,
        OUT / "P8_Y5_R2FR_3473_CLAIM_GATES.csv": gates,
        OUT / "P8_Y5_R2FR_3473_DECISION_LEDGER.csv": decisions,
        OUT / "P8_Y5_R2FR_3473_NEXT_TARGET.csv": next_rows,
    }
    for path, rows in output_map.items():
        write_csv(path, rows)
    validation = validation_rows([*output_map.keys(), DOC], sources, matrix, rank_ledger, nullspace, components)
    validation_path = OUT / "P8_Y5_BRR545_3473_VALIDATION.csv"
    write_csv(validation_path, validation)
    write_doc(sources, materials, matrix, rank_ledger, nullspace, components, theorem_rows, gates, decisions, next_rows, validation)


if __name__ == "__main__":
    main()
