from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "rank-two-screen-projector-gate"
STATUS = "rank_two_full_cell_projector_constructed_conditionally_not_parent_derived"
CLAIM_CEILING = "conditional_rank_two_projector_no_Bmem_or_local_GR_promotion"


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


def matrix_diag_text(matrix: np.ndarray) -> str:
    diagonal = np.diag(matrix)
    return "[" + ",".join(f"{float(value):.12g}" for value in diagonal) + "]"


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    sources = [
        (script_path, "this rank-two projector gate"),
        (ROOT / "53-coherent-projection-local-silence-gate.md", "coherent projection local-silence predecessor"),
        (ROOT / "109-boundary-charge-two-ninth-theorem-attempt.md", "earlier two-ninth charge theorem attempt"),
        (ROOT / "309-MTS-boundary-projector-contract-attempt.md", "boundary projector contract predecessor"),
        (ROOT / "316-FLRW-memory-projection-amplitude-contract.md", "FLRW projection and amplitude contract"),
        (ROOT / "317-kappa-mem-Ward-scale-lock-attempt.md", "kappa rescaling no-go"),
        (ROOT / "320-parent-cell-amplitude-theorem-gate.md", "parent-cell amplitude theorem gate"),
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


def projectors() -> dict[str, np.ndarray]:
    identity_3 = np.eye(3)
    p_motion = np.diag([1.0, 0.0, 0.0])
    p_time = np.diag([1.0, 0.0, 0.0])
    n_vector = np.asarray([0.0, 0.0, 1.0])
    p_screen = identity_3 - np.outer(n_vector, n_vector)
    p_active = np.kron(np.kron(p_motion, p_time), p_screen)
    p_bad_spatial_lift = np.kron(np.kron(identity_3, identity_3), p_screen)
    p_scalar_trace = np.kron(np.kron(p_motion, p_time), np.diag([1.0, 0.0, 0.0]))
    p_full_spatial = np.kron(np.kron(p_motion, p_time), identity_3)
    return {
        "P_M": p_motion,
        "P_T": p_time,
        "P_screen": p_screen,
        "P_active": p_active,
        "P_bad_spatial_lift": p_bad_spatial_lift,
        "P_scalar_trace": p_scalar_trace,
        "P_full_spatial": p_full_spatial,
    }


def rank(matrix: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(matrix, tol=1.0e-10))


def projector_error(matrix: np.ndarray) -> float:
    return float(np.max(np.abs(matrix @ matrix - matrix)))


def algebra_rows(matrices: dict[str, np.ndarray]) -> list[dict[str, Any]]:
    rows = []
    for name, matrix in matrices.items():
        rows.append(
            {
                "object": name,
                "dimension": matrix.shape[0],
                "trace": float(np.trace(matrix)),
                "rank": rank(matrix),
                "idempotence_error": projector_error(matrix),
                "diagonal": matrix_diag_text(matrix) if matrix.shape[0] <= 27 else "",
                "normalized_trace_over_27": float(np.trace(matrix) / 27.0) if matrix.shape[0] == 27 else "",
                "amplitude_if_kappa1": fraction_text(Fraction(rank(matrix), matrix.shape[0])) if matrix.shape[0] == 27 else "",
            }
        )
    return rows


def angular_average_rows() -> list[dict[str, Any]]:
    identity_3 = np.eye(3)
    axes = [
        np.asarray([1.0, 0.0, 0.0]),
        np.asarray([-1.0, 0.0, 0.0]),
        np.asarray([0.0, 1.0, 0.0]),
        np.asarray([0.0, -1.0, 0.0]),
        np.asarray([0.0, 0.0, 1.0]),
        np.asarray([0.0, 0.0, -1.0]),
    ]
    screen_average = sum(identity_3 - np.outer(axis, axis) for axis in axes) / len(axes)
    p_motion = np.diag([1.0, 0.0, 0.0])
    p_time = np.diag([1.0, 0.0, 0.0])
    active_average = np.kron(np.kron(p_motion, p_time), screen_average)
    return [
        {
            "object": "angular_average_P_screen",
            "dimension": 3,
            "diagonal": matrix_diag_text(screen_average),
            "trace": float(np.trace(screen_average)),
            "rank": rank(screen_average),
            "idempotence_error": projector_error(screen_average),
            "is_isotropic": bool(np.allclose(screen_average, (2.0 / 3.0) * identity_3)),
            "meaning": "FLRW isotropic tensor average keeps trace two but is no longer idempotent",
        },
        {
            "object": "angular_average_P_active",
            "dimension": 27,
            "diagonal": matrix_diag_text(active_average),
            "trace": float(np.trace(active_average)),
            "rank": rank(active_average),
            "idempotence_error": projector_error(active_average),
            "is_isotropic": "spatial_block_isotropic",
            "meaning": "amplitude trace survives averaging; projector property is fiberwise, not averaged",
        },
    ]


def lift_hazard_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "spatial_screen_only",
            "construction": "I_M tensor I_T tensor P_screen",
            "rank_in_27D": 18,
            "amplitude_if_dim27_kappa1": "2/3",
            "verdict": "wrong_for_2over27",
            "reason": "a rank-two spatial screen lifted across all motion/time channels multiplies by 3*3",
        },
        {
            "candidate": "single_motion_single_time_screen",
            "construction": "P_M(rank1) tensor P_T(rank1) tensor P_screen(rank2)",
            "rank_in_27D": 2,
            "amplitude_if_dim27_kappa1": "2/27",
            "verdict": "lead_conditional_target",
            "reason": "requires parent action to pick one coherent motion channel and one no-clock/time channel",
        },
        {
            "candidate": "single_motion_single_time_scalar",
            "construction": "P_M(rank1) tensor P_T(rank1) tensor P_scalar(rank1)",
            "rank_in_27D": 1,
            "amplitude_if_dim27_kappa1": "1/27",
            "verdict": "not_excluded",
            "reason": "FLRW scalar symmetry alone can choose a scalar channel unless screen theorem is supplied",
        },
        {
            "candidate": "single_motion_single_time_full_spatial",
            "construction": "P_M(rank1) tensor P_T(rank1) tensor I_S(rank3)",
            "rank_in_27D": 3,
            "amplitude_if_dim27_kappa1": "1/9",
            "verdict": "not_excluded_without_trace_or_screen_gate",
            "reason": "all spatial directions active gives too large an amplitude",
        },
    ]


def theorem_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "R1_rank1_motion_channel",
            "needed_statement": "parent action selects one coherent motion/load channel P_M with rank 1",
            "status": "not_derived",
            "evidence": "rank-one P_M can be written algebraically, but no parent variation selects it",
        },
        {
            "clause": "R2_rank1_time_channel",
            "needed_statement": "no-clock reduction selects one time/history channel P_T with rank 1",
            "status": "not_derived",
            "evidence": "rank-one P_T can be written algebraically, but the no-clock parent theorem is still open",
        },
        {
            "clause": "R3_screen_projector",
            "needed_statement": "for a supplied spatial unit normal n, P_screen=h-n n has rank 2 and P_screen^2=P_screen",
            "status": "pass_conditional",
            "evidence": "matrix algebra proves idempotence and trace two for every unit n",
        },
        {
            "clause": "R4_parent_origin_of_n",
            "needed_statement": "n is generated by a boundary/null/domain structure rather than chosen after the fact",
            "status": "not_derived",
            "evidence": "FLRW scalar symmetry has no preferred n; only the angular averaged screen bundle is isotropic",
        },
        {
            "clause": "R5_FLRW_isotropic_average",
            "needed_statement": "screen-bundle averaging gives an isotropic FLRW stress while retaining trace two",
            "status": "pass_conditional",
            "evidence": "average over ±axes gives <P_screen>=(2/3)I and trace two",
        },
        {
            "clause": "R6_local_silence",
            "needed_statement": "screen projector annihilates or suppresses local PPN-dangerous sources",
            "status": "fail_as_screen_only",
            "evidence": "ordinary local radiation and transverse fields also live on screens; needs P_MTS/P_coh/P_rel filters",
        },
        {
            "clause": "R7_kappa_unit",
            "needed_statement": "kappa_mem=1 is fixed by a nonhomogeneous normalization theorem",
            "status": "not_derived",
            "evidence": "checkpoint 317 rescaling no-go still applies",
        },
    ]


def gate_rows(source_rows: list[dict[str, Any]], algebra: list[dict[str, Any]], clauses: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in source_rows)
    by_object = {row["object"]: row for row in algebra}
    clause = {row["clause"]: row for row in clauses}
    active = by_object["P_active"]
    bad_lift = by_object["P_bad_spatial_lift"]
    gates = [
        ("source_paths_exist", sources_ok, "all cited predecessor checkpoints and this script exist"),
        ("P_active_idempotent", float(active["idempotence_error"]) < 1.0e-12, "P_active^2=P_active for the supplied factor projectors"),
        ("P_active_rank_two", int(active["rank"]) == 2, "rank(P_M tensor P_T tensor P_screen)=1*1*2=2"),
        ("P_active_normalized_trace_2over27", abs(float(active["normalized_trace_over_27"]) - (2.0 / 27.0)) < 1.0e-12, "Tr(P_active)/27=2/27"),
        ("bad_spatial_lift_rejected", int(bad_lift["rank"]) == 18, "I_M tensor I_T tensor P_screen gives 18/27=2/3, not 2/27"),
        ("screen_bundle_FLRW_isotropic", clause["R5_FLRW_isotropic_average"]["status"] == "pass_conditional", "angular averaged screen is isotropic with trace two"),
        ("rank1_motion_parent_derived", clause["R1_rank1_motion_channel"]["status"] == "pass", "rank-one motion channel not parent-derived"),
        ("rank1_time_parent_derived", clause["R2_rank1_time_channel"]["status"] == "pass", "rank-one no-clock/time channel not parent-derived"),
        ("screen_normal_parent_derived", clause["R4_parent_origin_of_n"]["status"] == "pass", "spatial normal n requires boundary/null/domain origin"),
        ("screen_only_local_silence", clause["R6_local_silence"]["status"] == "pass", "screen projection alone does not kill ordinary local transverse baths"),
        ("kappa_unit_parent_derived", clause["R7_kappa_unit"]["status"] == "pass", "kappa_mem=1 still blocked by homogeneous rescaling"),
        ("Bmem_amplitude_promotion_allowed", False, "rank-two algebra exists only conditionally and kappa/local gates fail"),
    ]
    return [{"gate": gate, "status": pass_fail(ok), "evidence": evidence} for gate, ok, evidence in gates]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"key": "status", "value": STATUS},
        {"key": "claim_ceiling", "value": CLAIM_CEILING},
        {"key": "rank_two_constructed", "value": "conditional"},
        {"key": "parent_rank_two_derived", "value": "false"},
        {"key": "Bmem_amplitude_derived", "value": "false"},
        {"key": "main_gain", "value": "identified_full_27D_lift_P_M_rank1_tensor_P_T_rank1_tensor_P_screen_rank2"},
        {"key": "main_blocker", "value": "parent_origin_of_rank1_motion_time_channels_screen_normal_local_silence_and_kappa_unit"},
        {"key": "next_action", "value": "derive_parent_origin_of_P_M_and_P_T_or_demote_rank_two_to_screen_bundle_closure"},
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
    matrices = projectors()
    algebra = algebra_rows(matrices)
    averages = angular_average_rows()
    hazards = lift_hazard_rows()
    clauses = theorem_clause_rows()
    gates = gate_rows(sources, algebra, clauses)
    decisions = decision_rows()

    write_csv(result_dir / "source_register.csv", sources, ["source", "role", "exists", "bytes"])
    write_csv(result_dir / "projector_algebra.csv", algebra, ["object", "dimension", "trace", "rank", "idempotence_error", "diagonal", "normalized_trace_over_27", "amplitude_if_kappa1"])
    write_csv(result_dir / "angular_average.csv", averages, ["object", "dimension", "diagonal", "trace", "rank", "idempotence_error", "is_isotropic", "meaning"])
    write_csv(result_dir / "lift_hazard_ledger.csv", hazards, ["candidate", "construction", "rank_in_27D", "amplitude_if_dim27_kappa1", "verdict", "reason"])
    write_csv(result_dir / "theorem_clauses.csv", clauses, ["clause", "needed_statement", "status", "evidence"])
    write_csv(result_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(result_dir / "decision.csv", decisions, ["key", "value"])

    payload = {
        "script": str(script_path),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "rank_two_constructed": "conditional",
        "parent_rank_two_derived": False,
        "Bmem_amplitude_derived": False,
        "main_gain": "full_27D_rank_two_lift_identified",
        "main_blocker": "parent_origin_of_rank1_motion_time_channels_screen_normal_local_silence_and_kappa_unit",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(STATUS + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
