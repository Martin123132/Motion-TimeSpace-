#!/usr/bin/env python3
"""Checkpoint 245: exact relative memory or projector-stress Bianchi."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
WORK_DIR = SCRIPT_DIR.parent
RUNS_ROOT = WORK_DIR / "runs"

CHECKPOINT_245_NAME = "exact-relative-memory-or-projector-stress-bianchi"
RUN_244 = RUNS_ROOT / "20260601-000061-Meff-monopole-source-normalization-or-radial-memory-hair"

STATUS = "N4_exact_relative_memory_gate_locked_N5_projector_stress_Bianchi_obligation_open_no_q_loc_or_PPN_promotion"
CLAIM_CEILING = "N4_N5_conditional_gate_no_q_loc_beta_or_local_GR_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 245 runner"),
        (WORK_DIR / "231-Jrel-cohomology-projector-or-local-EH-limit.md", "relative cohomology exactness gate"),
        (WORK_DIR / "232-parent-Pmem-projector-or-source-identity-variation.md", "P_mem source identity template"),
        (WORK_DIR / "234-boundary-metric-variation-and-Bianchi-ledger.md", "projector stress/Bianchi ledger"),
        (WORK_DIR / "235-projector-stress-variation-or-nohair-constraint-algebra.md", "projector variation safe conditions"),
        (WORK_DIR / "244-Meff-monopole-source-normalization-or-radial-memory-hair.md", "N1 M_eff gate and next target"),
        (RUN_244 / "status.json", "checkpoint 244 machine status"),
        (RUN_244 / "results" / "radial_memory_hair_exclusion.csv", "radial hair channels before N4/N5"),
    ]
    rows: list[dict[str, Any]] = []
    for path, role in paths:
        exists = path.exists()
        rows.append(
            {
                "source": path.name,
                "path": str(path),
                "exists": "yes" if exists else "no",
                "sha256": sha256_file(path) if exists and path.is_file() else "",
                "role": role,
                "issue": "" if exists else "missing",
            }
        )
    return rows


def exact_relative_memory_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "name": "remove_absolute_and_danger_blocks",
            "condition": "P_mem = 1 - Pi_M - Pi_TF - Pi_matter",
            "equation": "int_{S^2} P_mem J_rel = 0, Pi_TF P_mem J_rel=0, Pi_matter P_mem J_rel=0",
            "result": "relative memory current carries neither mass, shear, nor direct matter vertices",
        },
        {
            "step": 2,
            "name": "closed_relative_current",
            "condition": "parent source identity gives d_rel(P_mem J_rel)=0 in compact exterior",
            "equation": "d_rel(P_mem J_rel)=0",
            "result": "projected memory current is closed",
        },
        {
            "step": 3,
            "name": "relative_cohomology_vanishes",
            "condition": "Sigma_ext ~= S^2 x I with relative boundary primitive",
            "equation": "H^2(Sigma_ext, partial Sigma_ext)=0",
            "result": "closed projected relative memory flux is exact",
        },
        {
            "step": 4,
            "name": "exact_pure_gauge_representative",
            "condition": "A_rel|partial Sigma_ext is pure gauge or boundary-cancelled",
            "equation": "P_mem J_rel = d_rel A_rel",
            "result": "d_rel(P_mem J_rel)=d_rel^2 A_rel=0",
        },
        {
            "step": 5,
            "name": "qloc_readout",
            "condition": "source identity and exact relative memory hold",
            "equation": "q_loc^nu = -P_loc d_rel(P_mem J_rel)^nu = 0",
            "result": "local relative-memory force source is conditionally zero",
        },
        {
            "step": 6,
            "name": "promotion_limit",
            "condition": "P_mem/source identity/A_rel must be parent-derived",
            "equation": "delta S_parent -> P_mem, source identity, boundary primitive",
            "result": "N4 is a conditional topology gate, not a q_loc pass claim",
        },
    ]


def projector_stress_rows() -> list[dict[str, Any]]:
    return [
        {
            "stress_piece": "delta_Pi_M",
            "safe_if": "M_eff flux is conserved and Pi_M variation is carried as T_Meff",
            "unsafe_if": "mass projector varies while source normalization is held fixed by hand",
            "Bianchi_obligation": "include T_Meff or prove topological metric-independence",
            "status_after_245": "open_from_N1_parent_gap",
        },
        {
            "stress_piece": "delta_Pi_TF",
            "safe_if": "N2 scalar boundary theorem removes trace-free shear or T_TF retained",
            "unsafe_if": "anisotropic projector stress is dropped",
            "Bianchi_obligation": "include T_TF or derive tau_TF_AB=0 from parent",
            "status_after_245": "conditional_from_N2",
        },
        {
            "stress_piece": "delta_Pi_matter",
            "safe_if": "N3 strict universal coframe forbids direct matter/clock block",
            "unsafe_if": "direct matter vertex is projected away after variation",
            "Bianchi_obligation": "matter Ward identity on the observed coframe",
            "status_after_245": "conditional_from_N3",
        },
        {
            "stress_piece": "delta_Pmem_relative",
            "safe_if": "P_mem J_rel=dA_rel and boundary primitive is pure gauge, or T_rel/T_projector retained",
            "unsafe_if": "exactness is used while dropping projector/boundary stress",
            "Bianchi_obligation": "include T_rel + T_projector + T_boundary unless proven zero",
            "status_after_245": "open",
        },
        {
            "stress_piece": "delta_boundary_metric_B",
            "safe_if": "boundary Hodge/DeWitt metric is parent-derived and varied",
            "unsafe_if": "orthogonality metric is treated as fixed external structure",
            "Bianchi_obligation": "include T_boundary_metric",
            "status_after_245": "open",
        },
    ]


def bianchi_safe_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "zero_projector_stress_route",
            "requirements": "projector metric topological or metric-independent; projected current exact pure boundary; boundary primitive pure gauge",
            "q_loc_status": "conditionally_zero",
            "Bianchi_status": "safe only if T_projector=0 is derived",
            "verdict": "possible_not_derived",
        },
        {
            "route": "retained_projector_stress_route",
            "requirements": "vary Pi_M, Pi_TF, Pi_matter, P_mem, boundary metric, X, A_rel",
            "q_loc_status": "conditioned_on_full_source_identity",
            "Bianchi_status": "safe if total stress ledger is conserved on shell",
            "verdict": "formal_route_not_computed",
        },
        {
            "route": "dropped_projector_stress_route",
            "requirements": "use P_mem in q_loc but omit delta P_mem/delta g",
            "q_loc_status": "not_allowed",
            "Bianchi_status": "fake_conservation",
            "verdict": "rejected",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "residual": "beta_minus_1",
            "status_after_245": "still_open_but_q_loc_piece_conditionally_sharpened",
            "coefficient_status": "relative memory can be q_loc-silent if N4 and N5 hold",
            "remaining_gap": "projector stress and auxiliary no-hair plus EH exterior",
        },
        {
            "residual": "G_eff_over_G_minus_1",
            "status_after_245": "unchanged_N1_conditional",
            "coefficient_status": "M_eff monopole source requires Pi_M flux closure",
            "remaining_gap": "parent Pi_M and source normalization",
        },
        {
            "residual": "gamma_minus_1",
            "status_after_245": "unchanged_N2_conditional",
            "coefficient_status": "c_gamma=0 under scalar-boundary/no-shear theorem",
            "remaining_gap": "parent scalar-only boundary variable set",
        },
        {
            "residual": "Phi_minus_Psi",
            "status_after_245": "unchanged_N2_conditional",
            "coefficient_status": "c_slip=0 under tau_TF_AB=0 and compact matching",
            "remaining_gap": "parent no-shear theorem",
        },
        {
            "residual": "epsilon_matter",
            "status_after_245": "unchanged_N3_conditional",
            "coefficient_status": "c_matter_direct=0 under strict matter coframe",
            "remaining_gap": "parent R_loc selection",
        },
        {
            "residual": "alpha_clock",
            "status_after_245": "unchanged_direct_vertex_conditional",
            "coefficient_status": "c_clock_direct=0 under strict matter coframe",
            "remaining_gap": "metric clock redshift/C representative still open",
        },
    ]


def local_gate_priority_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank_after_245": 1,
            "target": "N5_projector_stress_Bianchi",
            "status": "open",
            "why": "N4 exactness is not enough unless projector stress is zero or retained",
            "next_action": "compute delta P_mem/delta g or derive topological zero-stress route",
        },
        {
            "rank_after_245": 2,
            "target": "N6_auxiliary_nohair",
            "status": "open",
            "why": "X/J_rel/V_def can still carry exterior propagating hair",
            "next_action": "derive rank/bracket closure or no exterior degrees",
        },
        {
            "rank_after_245": 3,
            "target": "local_EH_exterior",
            "status": "open",
            "why": "beta=1 still needs metric-only vacuum exterior",
            "next_action": "derive EH/Lovelock local exterior operator after no-hair gates",
        },
        {
            "rank_after_245": 4,
            "target": "Rloc_parent_selection",
            "status": "open",
            "why": "strict local coframe remains conditional",
            "next_action": "derive stationary bound-domain representative selection",
        },
        {
            "rank_after_245": 5,
            "target": "N1_N2_parent_owners",
            "status": "open",
            "why": "M_eff flux closure and scalar boundary no-shear remain parent gaps",
            "next_action": "derive boundary symplectic metric and scalar variable set",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "N4 exact relative memory topology chain written",
            "status": "conditional_pass",
            "evidence": "P_mem J_rel=dA_rel follows if closed relative current and H2_relative=0",
            "claim_allowed": "conditional theorem only",
        },
        {
            "gate": "q_loc public silence claimed",
            "status": "fail",
            "evidence": "P_mem/source identity/A_rel parent ownership missing",
            "claim_allowed": "no",
        },
        {
            "gate": "N5 projector stress cleared",
            "status": "fail",
            "evidence": "T_projector zero/retained route not computed",
            "claim_allowed": "no",
        },
        {
            "gate": "dropped projector stress route rejected",
            "status": "pass",
            "evidence": "explicitly marked fake conservation",
            "claim_allowed": "negative gate only",
        },
        {
            "gate": "local GR or PPN promoted",
            "status": "fail",
            "evidence": CLAIM_CEILING,
            "claim_allowed": "no",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "meaning": "N4 is now locked as a conditional topology gate: after mass, shear, and direct matter blocks are removed by owned projectors, a closed projected relative memory current on S2xI with relative boundary primitive is exact and gives q_loc=0. But N5 remains decisive: exactness cannot be used while dropping projector stress. Either T_projector is derived to vanish or it must be carried in the total Bianchi ledger.",
            "main_gain": "relative memory harmlessness now has a precise exactness theorem and an explicit conservation police gate",
            "main_failure": "projector stress and auxiliary no-hair remain open, so q_loc, beta, PPN, and local GR are not promoted",
            "next_target": "246-auxiliary-nohair-rank-bracket-or-local-EH-pivot.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_245_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    exact_rows = exact_relative_memory_rows()
    stress_rows = projector_stress_rows()
    bianchi_rows = bianchi_safe_branch_rows()
    coefficient_rows = coefficient_status_rows()
    priority_rows = local_gate_priority_rows()
    gates = claim_gate_rows()
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "exact_relative_memory_chain.csv": (
            exact_rows,
            ["step", "name", "condition", "equation", "result"],
        ),
        "projector_stress_obligations.csv": (
            stress_rows,
            ["stress_piece", "safe_if", "unsafe_if", "Bianchi_obligation", "status_after_245"],
        ),
        "Bianchi_safe_branch_options.csv": (
            bianchi_rows,
            ["route", "requirements", "q_loc_status", "Bianchi_status", "verdict"],
        ),
        "coefficient_status_after_245.csv": (
            coefficient_rows,
            ["residual", "status_after_245", "coefficient_status", "remaining_gap"],
        ),
        "local_gate_priority_after_245.csv": (
            priority_rows,
            ["rank_after_245", "target", "status", "why", "next_action"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            ["decision", "meaning", "main_gain", "main_failure", "next_target", "promotion_allowed", "claim_ceiling"],
        ),
    }
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": sum(row["exists"] != "yes" for row in source_rows),
        "N4_exact_relative_memory_gate_conditionally_locked": True,
        "N5_projector_stress_cleared": False,
        "dropped_projector_stress_route_rejected": True,
        "q_loc_public_silence_claimed": False,
        "local_GR_promoted": False,
        "PPN_promoted": False,
        "promotion_allowed": False,
        "next_target": decision[0]["next_target"],
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(status_payload["status"] + "\n", encoding="utf-8")
    return status_payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--timestamp", default=None, help="Optional run timestamp prefix.")
    args = parser.parse_args()
    print(json.dumps(run(args.timestamp), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
