from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "parent-cell-amplitude-theorem-gate"
STATUS = "parent_cell_amplitude_conditional_schema_but_not_parent_derived"
CLAIM_CEILING = "conditional_parent_cell_schema_no_Bmem_amplitude_promotion"
B_TARGET = Fraction(2, 27)


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


def source_register_rows(script_path: Path) -> list[dict[str, Any]]:
    sources = [
        (script_path, "this parent-cell amplitude theorem gate"),
        (ROOT / "140-boundary-charge-amplitude-decision-gate.md", "earlier endpoint/boundary-charge amplitude demotion"),
        (ROOT / "316-FLRW-memory-projection-amplitude-contract.md", "FLRW projection and amplitude contract"),
        (ROOT / "317-kappa-mem-Ward-scale-lock-attempt.md", "kappa rescaling no-go"),
        (ROOT / "318-fixed-2over27-fullcov-noSH0ES-release-matrix.md", "strict fixed 2/27 release matrix"),
        (ROOT / "319-fixed-2over27-split-robustness-readout.md", "strict fixed 2/27 split robustness readout"),
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


def theorem_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "C1_cell_factorization",
            "needed_statement": "V_cell = V_M tensor V_T tensor V_S with dim(V_M)=dim(V_T)=dim(V_S)=3, hence dim(V_cell)=27",
            "current_result": "conditional_schema",
            "status": "partial",
            "why": "3x3x3 is natural for a motion-time-space triad, but the parent action has not forced this representation uniquely",
            "if_missing": "replace 27 by dim(V_cell); 2/27 becomes 2/dim(V_cell)",
        },
        {
            "clause": "C2_normalized_cell_trace",
            "needed_statement": "the FLRW memory density is the normalized cell trace tau(P_active)=Tr(P_active)/dim(V_cell)",
            "current_result": "conditional_schema",
            "status": "partial",
            "why": "normalized trace is the clean non-post-fit bookkeeping measure, but it is still an action choice unless derived from measure normalization",
            "if_missing": "a free trace coefficient reappears",
        },
        {
            "clause": "C3_idempotent_projector",
            "needed_statement": "P_active^2=P_active, so Tr(P_active)=rank(P_active)",
            "current_result": "algebraic_if_projector_exists",
            "status": "partial",
            "why": "the algebra is exact, but a parent variation has not produced the projector",
            "if_missing": "rank counting is not a theorem",
        },
        {
            "clause": "C4_rank_two_active_channel",
            "needed_statement": "rank(P_active)=2 from a transverse/no-clock memory channel",
            "current_result": "plausible_transverse_screen_schema",
            "status": "partial",
            "why": "two active screen degrees are physically motivated, but FLRW scalar symmetry alone also permits rank 1 or rank 3 choices",
            "if_missing": "B_mem is rank/27, not fixed to 2/27",
        },
        {
            "clause": "C5_unit_kappa",
            "needed_statement": "kappa_mem=1 with no rescalable dimensionless prefactor",
            "current_result": "not_derived",
            "status": "fail",
            "why": "diffeomorphism Ward identities and continuity are homogeneous under S_mem -> lambda S_mem",
            "if_missing": "B_mem = kappa_mem rank(P_active)/dim(V_cell), with kappa_mem free",
        },
        {
            "clause": "C6_no_local_PPN_leakage",
            "needed_statement": "the same projector is FLRW-active but locally silent or volume-suppressed",
            "current_result": "conditional_effective_requirement",
            "status": "partial",
            "why": "local-GR/PPN compatibility is not yet parent-derived",
            "if_missing": "late-time background success can conflict with local GR",
        },
    ]


def amplitude_family_rows() -> list[dict[str, Any]]:
    rows = []
    for dim_cell in [9, 18, 27, 36, 54, 81]:
        for rank in range(0, min(dim_cell, 6) + 1):
            value = Fraction(rank, dim_cell)
            rows.append(
                {
                    "dim_V_cell": dim_cell,
                    "rank_P_active": rank,
                    "kappa_mem": "1",
                    "B_mem": fraction_text(value),
                    "B_mem_float": float(value),
                    "matches_2over27": value == B_TARGET,
                    "interpretation": "target" if value == B_TARGET else "allowed_without_rank_dim_lock",
                }
            )
    return rows


def rank_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "scalar_trace_rank_one",
            "rank": 1,
            "B_if_dim27_kappa1": "1/27",
            "status": "not_excluded_by_FLRW_scalar_symmetry_alone",
            "notes": "If memory is the isotropic trace scalar itself, rank one is natural and misses the target.",
        },
        {
            "route": "transverse_screen_rank_two",
            "rank": 2,
            "B_if_dim27_kappa1": "2/27",
            "status": "lead_theorem_target",
            "notes": "If no-clock projection leaves the two screen directions active, the target follows algebraically.",
        },
        {
            "route": "full_spatial_rank_three",
            "rank": 3,
            "B_if_dim27_kappa1": "1/9",
            "status": "not_excluded_without_local_silence_or_trace_subtraction",
            "notes": "If all spatial directions carry equal memory, the amplitude is too large.",
        },
        {
            "route": "traceless_symmetric_spatial_rank_five",
            "rank": 5,
            "B_if_dim27_kappa1": "5/27",
            "status": "not_FLRW_background_minimal",
            "notes": "Five shear components are natural for 3D traceless symmetric tensors but are not the scalar background memory channel.",
        },
    ]


def kappa_degeneracy_rows() -> list[dict[str, Any]]:
    rows = []
    for kappa in [Fraction(1, 2), Fraction(3, 4), Fraction(1, 1), Fraction(27, 20), Fraction(3, 2)]:
        value = kappa * B_TARGET
        rows.append(
            {
                "rank_P_active": 2,
                "dim_V_cell": 27,
                "kappa_mem": fraction_text(kappa),
                "B_mem": fraction_text(value),
                "B_mem_float": float(value),
                "ward_continuity_status": "still_allowed_by_homogeneous_rescaling",
            }
        )
    return rows


def conditional_theorem_rows() -> list[dict[str, Any]]:
    assumptions = [
        "V_cell = V_M tensor V_T tensor V_S with dimensions 3,3,3",
        "memory density uses the normalized cell trace tau(A)=Tr(A)/27",
        "P_active is an idempotent projector",
        "no-clock FLRW memory leaves exactly the two transverse/screen channels active",
        "parent measure or anomaly forbids S_mem -> lambda S_mem and fixes kappa_mem=1",
        "local branch suppresses the same channel in PPN domains",
    ]
    conclusion = "B_mem = kappa_mem Tr(P_active)/dim(V_cell) = 1*2/27 = 2/27"
    return [
        {
            "theorem_name": "conditional_parent_cell_amplitude_theorem",
            "assumptions": " | ".join(assumptions),
            "conclusion": conclusion,
            "proved_in_current_corpus": "no",
            "usable_status": "conditional_schema_only",
        }
    ]


def gate_rows(source_rows: list[dict[str, Any]], clause_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in source_rows)
    clauses = {row["clause"]: row for row in clause_rows}
    gates = [
        ("source_paths_exist", sources_ok, "all cited checkpoints and this script exist"),
        ("dim27_parent_derived", clauses["C1_cell_factorization"]["status"] == "pass", "3x3x3 cell is not uniquely forced by a parent action"),
        ("normalized_trace_parent_derived", clauses["C2_normalized_cell_trace"]["status"] == "pass", "normalized trace remains an action/measure choice"),
        ("projector_parent_derived", clauses["C3_idempotent_projector"]["status"] == "pass", "idempotent projector has not been produced by variation"),
        ("rank2_parent_derived", clauses["C4_rank_two_active_channel"]["status"] == "pass", "rank two is physically motivated but not uniquely forced"),
        ("kappa_unit_parent_derived", clauses["C5_unit_kappa"]["status"] == "pass", "rescaling no-go remains active"),
        ("local_silence_parent_derived", clauses["C6_no_local_PPN_leakage"]["status"] == "pass", "local PPN branch remains conditional/effective"),
        ("conditional_theorem_schema_valid", True, "if all clauses are supplied, B_mem=2/27 follows algebraically"),
        ("Bmem_amplitude_promotion_allowed", False, "at least one required parent clause fails"),
    ]
    return [{"gate": gate, "status": pass_fail(ok), "evidence": evidence} for gate, ok, evidence in gates]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {"key": "status", "value": STATUS},
        {"key": "claim_ceiling", "value": CLAIM_CEILING},
        {"key": "derived_now", "value": "false"},
        {"key": "conditional_schema", "value": "true"},
        {"key": "amplitude_target", "value": "B_mem=2/27"},
        {"key": "main_blocker", "value": "kappa_mem_unit_normalization_plus_rank2_parent_projector"},
        {"key": "next_action", "value": "derive_rank2_projector_or_kappa_unit_from_a_parent_action_or_keep_2over27_as_closure"},
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
    clauses = theorem_clause_rows()
    amplitudes = amplitude_family_rows()
    ranks = rank_route_rows()
    kappas = kappa_degeneracy_rows()
    theorem = conditional_theorem_rows()
    gates = gate_rows(sources, clauses)
    decisions = decision_rows()

    write_csv(result_dir / "source_register.csv", sources, ["source", "role", "exists", "bytes"])
    write_csv(result_dir / "theorem_clauses.csv", clauses, ["clause", "needed_statement", "current_result", "status", "why", "if_missing"])
    write_csv(result_dir / "amplitude_family.csv", amplitudes, ["dim_V_cell", "rank_P_active", "kappa_mem", "B_mem", "B_mem_float", "matches_2over27", "interpretation"])
    write_csv(result_dir / "rank_route_ledger.csv", ranks, ["route", "rank", "B_if_dim27_kappa1", "status", "notes"])
    write_csv(result_dir / "kappa_degeneracy.csv", kappas, ["rank_P_active", "dim_V_cell", "kappa_mem", "B_mem", "B_mem_float", "ward_continuity_status"])
    write_csv(result_dir / "conditional_theorem.csv", theorem, ["theorem_name", "assumptions", "conclusion", "proved_in_current_corpus", "usable_status"])
    write_csv(result_dir / "gate_results.csv", gates, ["gate", "status", "evidence"])
    write_csv(result_dir / "decision.csv", decisions, ["key", "value"])

    payload = {
        "script": str(script_path),
        "run_dir": str(run_dir),
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "Bmem_amplitude_derived": False,
        "conditional_theorem_schema": True,
        "target": "B_mem=2/27",
        "main_blocker": "kappa_mem_unit_normalization_plus_rank2_parent_projector",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "COMPLETE.txt").write_text(STATUS + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
