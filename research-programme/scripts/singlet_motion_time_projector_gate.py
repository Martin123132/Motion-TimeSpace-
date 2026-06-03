from __future__ import annotations

import argparse
import csv
import itertools
import json
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "singlet-motion-time-projector-gate"
STATUS = "singlet_motion_time_projectors_constructed_conditionally_not_parent_derived"
CLAIM_CEILING = "conditional_S3_singlet_projectors_no_Bmem_or_local_GR_promotion"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def yes_no(value: bool) -> str:
    return "yes" if value else "no"


def pass_fail(value: bool) -> str:
    return "pass" if value else "fail"


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def matrix_text(matrix: np.ndarray) -> str:
    return "[" + ";".join(",".join(f"{float(value):.12g}" for value in row) for row in matrix) + "]"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    sources = [
        (script_path, "this S3 singlet motion/time projector gate"),
        (ROOT / "56-u3-quarter-parent-cell-theorem-attempt.md", "3+1 cell and clock-leg predecessor"),
        (ROOT / "79-auxiliary-clock-cell-variation-attempt.md", "auxiliary clock/cell owner predecessor"),
        (ROOT / "310-ordinary-MTS-sector-split-attempt.md", "ordinary/MTS sector split predecessor"),
        (ROOT / "320-parent-cell-amplitude-theorem-gate.md", "parent-cell amplitude theorem gate"),
        (ROOT / "321-rank-two-screen-projector-gate.md", "rank-two screen projector predecessor"),
    ]
    return [
        {
            "source": relpath(path),
            "role": role,
            "exists": yes_no(path.exists()),
            "bytes": path.stat().st_size if path.exists() else 0,
        }
        for path, role in sources
    ]


def permutation_matrix(permutation: tuple[int, int, int]) -> np.ndarray:
    matrix = np.zeros((3, 3), dtype=float)
    for column, row in enumerate(permutation):
        matrix[row, column] = 1.0
    return matrix


def s3_matrices() -> list[np.ndarray]:
    return [permutation_matrix(permutation) for permutation in itertools.permutations((0, 1, 2))]


def rank(matrix: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(matrix, tol=1.0e-10))


def projector_error(matrix: np.ndarray) -> float:
    return float(np.max(np.abs(matrix @ matrix - matrix)))


def commutator_error(matrix: np.ndarray, group: list[np.ndarray]) -> float:
    return float(max(np.max(np.abs(matrix @ g - g @ matrix)) for g in group))


def singlet_projectors() -> dict[str, np.ndarray]:
    group = s3_matrices()
    identity = np.eye(3)
    p_singlet = sum(group) / len(group)
    p_doublet = identity - p_singlet
    n_vector = np.asarray([0.0, 0.0, 1.0])
    p_screen = identity - np.outer(n_vector, n_vector)
    p_active = np.kron(np.kron(p_singlet, p_singlet), p_screen)
    p_axis_active = np.kron(np.kron(np.diag([1.0, 0.0, 0.0]), np.diag([1.0, 0.0, 0.0])), p_screen)
    p_doublet_screen = np.kron(np.kron(p_doublet, p_singlet), p_screen)
    return {
        "P_singlet": p_singlet,
        "P_doublet": p_doublet,
        "P_screen": p_screen,
        "P_active_singlet": p_active,
        "P_axis_active_old_basis_choice": p_axis_active,
        "P_motion_doublet_time_singlet_screen": p_doublet_screen,
    }


def s3_projector_rows(matrices: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    group = s3_matrices()
    rows = []
    for name in ["P_singlet", "P_doublet", "P_screen"]:
        matrix = matrices[name]
        rows.append(
            {
                "object": name,
                "dimension": matrix.shape[0],
                "trace": float(np.trace(matrix)),
                "rank": rank(matrix),
                "idempotence_error": projector_error(matrix),
                "S3_commutator_error": commutator_error(matrix, group) if matrix.shape == (3, 3) else "",
                "matrix": matrix_text(matrix),
                "meaning": {
                    "P_singlet": "unique S3-invariant coherent channel in a three-state sector",
                    "P_doublet": "orthogonal two-dimensional noncoherent sector",
                    "P_screen": "spatial screen projector; not S3-invariant because it needs a normal/screen bundle",
                }[name],
            }
        )
    return rows


def full_lift_rows(matrices: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    rows = []
    for name in ["P_active_singlet", "P_axis_active_old_basis_choice", "P_motion_doublet_time_singlet_screen"]:
        matrix = matrices[name]
        normalized = Fraction(rank(matrix), matrix.shape[0])
        rows.append(
            {
                "object": name,
                "dimension": matrix.shape[0],
                "trace": float(np.trace(matrix)),
                "rank": rank(matrix),
                "idempotence_error": projector_error(matrix),
                "normalized_trace": float(np.trace(matrix) / matrix.shape[0]),
                "rank_over_dimension": fraction_text(normalized),
                "verdict": {
                    "P_active_singlet": "lead_conditional_S3_singlet_lift",
                    "P_axis_active_old_basis_choice": "algebraically_same_rank_but_basis_chosen_by_hand",
                    "P_motion_doublet_time_singlet_screen": "wrong_sector_gives_4over27",
                }[name],
            }
        )
    return rows


def invariant_source_rows(matrices: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    p_singlet = matrices["P_singlet"]
    p_doublet = matrices["P_doublet"]
    group = s3_matrices()
    sources = {
        "coherent_equal_load": np.asarray([1.0, 1.0, 1.0]),
        "basis_axis_load": np.asarray([1.0, 0.0, 0.0]),
        "tracefree_difference": np.asarray([1.0, -1.0, 0.0]),
        "generic_load": np.asarray([1.0, 2.0, 4.0]),
    }
    rows = []
    for label, vector in sources.items():
        singlet = p_singlet @ vector
        doublet = p_doublet @ vector
        invariant_error = max(float(np.linalg.norm(g @ vector - vector)) for g in group)
        rows.append(
            {
                "source": label,
                "vector": "[" + ",".join(str(float(value)) for value in vector) + "]",
                "S3_invariant": invariant_error < 1.0e-12,
                "invariant_error": invariant_error,
                "singlet_projection": "[" + ",".join(f"{float(value):.12g}" for value in singlet) + "]",
                "doublet_norm": float(np.linalg.norm(doublet)),
                "singlet_norm": float(np.linalg.norm(singlet)),
                "readout": "pure_singlet" if float(np.linalg.norm(doublet)) < 1.0e-12 else "contains_doublet_or_symmetry_breaking",
            }
        )
    return rows


def theorem_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "S1_three_state_sector",
            "needed_statement": "motion and time/history sectors are each three-dimensional cell factors",
            "status": "conditional",
            "evidence": "matches the 27D parent-cell schema but the cell representation is not parent-derived",
        },
        {
            "clause": "S2_S3_permutation_symmetry",
            "needed_statement": "each 3-state sector has an S3 permutation symmetry before domain/source breaking",
            "status": "not_derived",
            "evidence": "S3 is mathematically natural for equal cell slots but not yet forced by the action",
        },
        {
            "clause": "S3_group_average_projector",
            "needed_statement": "P_singlet=(1/|S3|) sum_g g is the coherent rank-one projector",
            "status": "pass_algebraic",
            "evidence": "matrix group average is idempotent, trace one, rank one, and commutes with S3",
        },
        {
            "clause": "S4_FLRW_source_is_singlet",
            "needed_statement": "FLRW coherent memory source is S3-invariant in motion and time/history sectors",
            "status": "conditional",
            "evidence": "equal-load vector is pure singlet; parent action has not proven the source is only equal-load",
        },
        {
            "clause": "S5_no_clock_rank_one",
            "needed_statement": "no-clock reduction selects the time/history singlet rather than a physical clock/aether mode",
            "status": "not_derived",
            "evidence": "auxiliary clock/cell work allows only stress-free reference structure; no parent no-clock singlet theorem yet",
        },
        {
            "clause": "S6_boundary_sector_superselection",
            "needed_statement": "ordinary local baths cannot source the same singlet memory channel",
            "status": "not_derived",
            "evidence": "sector split has conditional block-kernel lemma, but parent sector label S_D is missing",
        },
        {
            "clause": "S7_screen_bundle_and_kappa",
            "needed_statement": "screen-bundle, local silence, and kappa_mem=1 are also parent-derived",
            "status": "not_derived",
            "evidence": "checkpoint 321 screen/local gates and checkpoint 317 kappa no-go remain active",
        },
    ]


def gate_rows(source_rows: list[dict[str, Any]], s3_rows: list[dict[str, Any]], lift_rows: list[dict[str, Any]], source_tests: list[dict[str, Any]], clauses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in source_rows)
    s3 = {row["object"]: row for row in s3_rows}
    lift = {row["object"]: row for row in lift_rows}
    tests = {row["source"]: row for row in source_tests}
    clause = {row["clause"]: row for row in clauses}
    gates = [
        ("source_paths_exist", sources_ok, "all cited predecessor checkpoints and this script exist"),
        ("S3_singlet_idempotent", float(s3["P_singlet"]["idempotence_error"]) < 1.0e-12, "P_singlet^2=P_singlet"),
        ("S3_singlet_rank_one", int(s3["P_singlet"]["rank"]) == 1, "S3 group average has trace/rank one"),
        ("S3_singlet_commutes_with_group", float(s3["P_singlet"]["S3_commutator_error"]) < 1.0e-12, "P_singlet commutes with all S3 permutations"),
        ("coherent_source_pure_singlet", tests["coherent_equal_load"]["readout"] == "pure_singlet", "equal-load FLRW source projects entirely to the singlet"),
        ("generic_sources_not_singlet", tests["generic_load"]["readout"] != "pure_singlet", "generic local/source data contains doublet symmetry-breaking content"),
        ("full_lift_rank_two", int(lift["P_active_singlet"]["rank"]) == 2, "P_singlet(M) tensor P_singlet(T) tensor P_screen has rank two"),
        ("full_lift_trace_2over27", lift["P_active_singlet"]["rank_over_dimension"] == "2/27", "normalized rank is 2/27"),
        ("basis_choice_removed", lift["P_active_singlet"]["rank_over_dimension"] == lift["P_axis_active_old_basis_choice"]["rank_over_dimension"], "singlet version keeps rank without choosing a basis axis"),
        ("parent_S3_symmetry_derived", clause["S2_S3_permutation_symmetry"]["status"] == "pass", "S3 symmetry is not yet forced by the action"),
        ("no_clock_singlet_parent_derived", clause["S5_no_clock_rank_one"]["status"] == "pass", "time/history singlet is not yet a parent no-clock theorem"),
        ("ordinary_bath_superselection_parent_derived", clause["S6_boundary_sector_superselection"]["status"] == "pass", "ordinary/MTS sector label remains conditional"),
        ("Bmem_amplitude_promotion_allowed", False, "singlet projectors are conditional and screen/kappa/local gates remain open"),
    ]
    return [{"gate": gate, "status": pass_fail(ok), "evidence": evidence} for gate, ok, evidence in gates]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"key": "status", "value": STATUS},
        {"key": "claim_ceiling", "value": CLAIM_CEILING},
        {"key": "rank_one_motion_time_constructed", "value": "conditional_S3_singlet"},
        {"key": "parent_rank_one_motion_time_derived", "value": "false"},
        {"key": "Bmem_amplitude_derived", "value": "false"},
        {"key": "main_gain", "value": "basis_choice_replaced_by_unique_S3_singlet_projector"},
        {"key": "main_blocker", "value": "parent_S3_symmetry_no_clock_singlet_and_ordinary_MTS_superselection_not_derived"},
        {"key": "next_action", "value": "derive_or_reject_parent_S3_cell_symmetry_and_sector_label_S_D"},
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=None)
    args = parser.parse_args()

    timestamp = args.timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    script_path = Path(__file__).resolve()
    sources = source_register_rows(script_path)
    matrices = singlet_projectors()
    s3_rows = s3_projector_rows(matrices)
    lift_rows = full_lift_rows(matrices)
    source_tests = invariant_source_rows(matrices)
    clauses = theorem_clause_rows()
    gates = gate_rows(sources, s3_rows, lift_rows, source_tests, clauses)
    decisions = decision_rows()

    write_csv(result_dir / "source_register.csv", sources, ["source", "role", "exists", "bytes"])
    write_csv(result_dir / "S3_projector_algebra.csv", s3_rows, ["object", "dimension", "trace", "rank", "idempotence_error", "S3_commutator_error", "matrix", "meaning"])
    write_csv(result_dir / "full_cell_lift.csv", lift_rows, ["object", "dimension", "trace", "rank", "idempotence_error", "normalized_trace", "rank_over_dimension", "verdict"])
    write_csv(result_dir / "invariant_source_tests.csv", source_tests, ["source", "vector", "S3_invariant", "invariant_error", "singlet_projection", "doublet_norm", "singlet_norm", "readout"])
    write_csv(result_dir / "theorem_clauses.csv", clauses, ["clause", "needed_statement", "status", "evidence"])
    write_csv(result_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(result_dir / "decision.csv", decisions, ["key", "value"])

    payload = {
        "script": str(script_path),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "rank_one_motion_time_constructed": "conditional_S3_singlet",
        "parent_rank_one_motion_time_derived": False,
        "Bmem_amplitude_derived": False,
        "main_gain": "basis_choice_replaced_by_unique_S3_singlet_projector",
        "main_blocker": "parent_S3_symmetry_no_clock_singlet_and_ordinary_MTS_superselection_not_derived",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(STATUS + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
