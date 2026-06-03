#!/usr/bin/env python3
"""Checkpoint 233: boundary symplectic metric or local EH operator."""

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

CHECKPOINT_233_NAME = "boundary-symplectic-metric-or-local-EH-operator"
RUN_232 = RUNS_ROOT / "20260601-000049-parent-Pmem-projector-or-source-identity-variation"

STATUS = "boundary_Hodge_DeWitt_metric_candidate_projectors_orthogonal_Lovelock_EH_gate_written_no_promotion"
CLAIM_CEILING = "boundary_metric_candidate_and_EH_gate_no_parent_local_GR_or_PPN_promotion"
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


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_register_rows() -> list[dict[str, Any]]:
    paths = [
        (Path(__file__).resolve(), "checkpoint 233 runner"),
        (WORK_DIR / "211-GK-parent-metric-Ward-identity-attempt.md", "DeWitt/Hodge metric precedent"),
        (WORK_DIR / "221-Noether-source-identity-or-compact-PPN-closure-map.md", "source identity and stress accounting"),
        (WORK_DIR / "224-defect-potential-Vdef-or-X-route-demotion.md", "V_def block ownership status"),
        (WORK_DIR / "231-Jrel-cohomology-projector-or-local-EH-limit.md", "J_rel cohomology gate"),
        (WORK_DIR / "232-parent-Pmem-projector-or-source-identity-variation.md", "P_mem decomposition candidate"),
        (RUN_232 / "status.json", "checkpoint 232 machine status"),
        (RUN_232 / "results" / "coefficient_status_after_232.csv", "checkpoint 232 coefficient status"),
        (RUN_232 / "results" / "charge_projector_decomposition.csv", "checkpoint 232 projector decomposition"),
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


def boundary_metric_rows() -> list[dict[str, Any]]:
    return [
        {
            "block": "harmonic_mass_flux",
            "metric_piece": "<J1,J2>_H = integral_Sigma J1 wedge * J2 restricted to harmonic H^2_abs",
            "orthogonal_projector": "Pi_M",
            "owner_status": "Hodge_candidate",
            "promotion_gap": "parent boundary action has not derived this Hodge norm",
        },
        {
            "block": "tracefree_shear",
            "metric_piece": "<tau1_TF,tau2_TF>_DW = integral_boundary sqrt(gamma) tau1_TF_AB G_DW^{ABCD} tau2_TF_CD",
            "orthogonal_projector": "Pi_TF",
            "owner_status": "DeWitt_candidate",
            "promotion_gap": "parent scalar-boundary sector must forbid or penalize this block",
        },
        {
            "block": "matter_clock_direct",
            "metric_piece": "coupling-space block for direct matter/clock vertices",
            "orthogonal_projector": "Pi_matter",
            "owner_status": "universal_coupling_contract",
            "promotion_gap": "matter/clock action not specified",
        },
        {
            "block": "relative_memory_exchange",
            "metric_piece": "Hodge relative norm on Omega^2(Sigma,partial Sigma) after harmonic/shear/matter removal",
            "orthogonal_projector": "P_mem",
            "owner_status": "orthogonal_complement_candidate",
            "promotion_gap": "full parent boundary symplectic metric missing",
        },
    ]


def orthogonality_rows() -> list[dict[str, Any]]:
    return [
        {
            "orthogonality": "harmonic_vs_relative_exact",
            "reason": "Hodge decomposition separates harmonic absolute flux from relative exact/coexact sectors under boundary conditions",
            "consequence": "mass flux can be kept as M_eff while memory exchange is projected separately",
            "status": "mathematical_gate",
        },
        {
            "orthogonality": "scalar_trace_vs_tracefree_shear",
            "reason": "SO(3) irreducible scalar trace and l>=2 trace-free tensor sectors do not mix on isotropic compact collar",
            "consequence": "Pi_TF can be an orthogonal projector if the boundary metric respects shell symmetry",
            "status": "symmetry_gate",
        },
        {
            "orthogonality": "matter_coupling_vs_metric_memory",
            "reason": "universal metric coupling makes direct matter/clock vertices a forbidden separate coupling block",
            "consequence": "Pi_matter is zero by action contract, not by fitting",
            "status": "contract_gate",
        },
        {
            "orthogonality": "Pmem_as_complement",
            "reason": "P_mem is the orthogonal complement to Pi_M, Pi_TF, and Pi_matter under the candidate boundary metric",
            "consequence": "P_mem stops being an arbitrary eraser if the parent owns the metric",
            "status": "candidate_not_parent_derived",
        },
    ]


def local_eh_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause": "EH1",
            "condition": "four-dimensional diffeomorphism-invariant exterior metric action",
            "result_if_true": "metric equations are covariantly conserved",
            "status": "required_not_derived",
        },
        {
            "clause": "EH2",
            "condition": "only metric propagates outside compact collar; X/J_rel/V_def carry no hair",
            "result_if_true": "no extra fifth-force or scalar/vector exterior profile",
            "status": "required_not_derived",
        },
        {
            "clause": "EH3",
            "condition": "second-order local metric equations with no extra background tensor",
            "result_if_true": "Lovelock-style route leaves Einstein tensor plus cosmological term",
            "status": "sufficient_gate",
        },
        {
            "clause": "EH4",
            "condition": "compact local exterior has negligible/constant Lambda-like term and M_eff monopole only",
            "result_if_true": "G_mu_nu=0 to local PPN order around compact source",
            "status": "sufficient_gate",
        },
        {
            "clause": "EH5",
            "condition": "static spherical asymptotically flat exterior",
            "result_if_true": "Schwarzschild exterior and beta=1",
            "status": "conditional_consequence",
        },
    ]


def coefficient_status_rows() -> list[dict[str, Any]]:
    previous = read_csv_rows(RUN_232 / "results" / "coefficient_status_after_232.csv")
    previous_by_residual = {row["residual"]: row for row in previous}
    updates = {
        "gamma_minus_1": (
            "boundary_metric_supports_TF_orthogonality",
            "Pi_TF can be orthogonal under SO(3)/DeWitt boundary metric",
            "derive parent boundary metric and scalar-only sector",
        ),
        "Phi_minus_Psi": (
            "boundary_metric_supports_TF_orthogonality",
            "trace-free shear is an orthogonal forbidden block if parent metric respects shell symmetry",
            "derive parent boundary metric",
        ),
        "G_eff_over_G_minus_1": (
            "Hodge_mass_projector_candidate",
            "Pi_M is harmonic H^2 flux and maps to M_eff",
            "derive mass/source normalization",
        ),
        "alpha_clock": (
            "unchanged_universal_metric_contract",
            "direct clock coupling remains separate forbidden block",
            "derive matter/clock action",
        ),
        "epsilon_matter": (
            "unchanged_universal_metric_contract",
            "direct composition coupling remains separate forbidden block",
            "derive matter action",
        ),
        "beta_minus_1": (
            "EH_gate_written_not_derived",
            "beta=1 follows through Lovelock/EH exterior gate if no-hair and metric-only assumptions hold",
            "derive local EH exterior operator and no-hair constraints",
        ),
    }
    rows: list[dict[str, Any]] = []
    for residual, prior in previous_by_residual.items():
        status, result, next_needed = updates[residual]
        rows.append(
            {
                "residual": residual,
                "checkpoint_232_status": prior["checkpoint_232_status"],
                "checkpoint_233_status": status,
                "coefficient_after_233": result,
                "parent_derived": "no",
                "promotion_allowed": "false",
                "next_needed": next_needed,
            }
        )
    return rows


def blocker_rows() -> list[dict[str, Any]]:
    return [
        {
            "blocker": "parent boundary symplectic metric",
            "why_it_matters": "turns Pi_M, Pi_TF, Pi_matter, and P_mem from convenient filters into canonical orthogonal projectors",
            "current_status": "Hodge/DeWitt candidate only",
            "next_attack": "derive as Hessian/Ward metric from V_def or boundary action",
        },
        {
            "blocker": "boundary stress variation",
            "why_it_matters": "must show projected blocks do not hide stress/Bianchi violations",
            "current_status": "not derived",
            "next_attack": "vary candidate metric blocks into T_boundary and Bianchi ledger",
        },
        {
            "blocker": "no-hair constraint algebra",
            "why_it_matters": "local EH gate needs no exterior X/J_rel/V_def propagating modes",
            "current_status": "open",
            "next_attack": "compute or avoid X constraint algebra with composite parent fields",
        },
        {
            "blocker": "local EH exterior operator",
            "why_it_matters": "beta=1 needs Schwarzschild branch, not just source silence",
            "current_status": "Lovelock sufficient gate only",
            "next_attack": "derive metric-only two-derivative exterior action from parent",
        },
    ]


def claim_gate_rows(source_rows: list[dict[str, Any]], coefficient_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    beta_gate = any(row["residual"] == "beta_minus_1" and row["checkpoint_233_status"] == "EH_gate_written_not_derived" for row in coefficient_rows)
    return [
        {
            "gate": "all cited local sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "claim_allowed": "internal checkpoint only",
        },
        {
            "gate": "boundary Hodge/DeWitt metric candidate written",
            "status": "pass",
            "evidence": "harmonic, trace-free, matter, and relative-memory blocks defined",
            "claim_allowed": "candidate only",
        },
        {
            "gate": "P_mem orthogonal-complement route written",
            "status": "pass",
            "evidence": "P_mem is complement under candidate metric",
            "claim_allowed": "conditional only",
        },
        {
            "gate": "local EH/Lovelock sufficient gate written",
            "status": "pass" if beta_gate else "fail",
            "evidence": "metric-only diffeo-invariant second-order exterior would yield EH branch",
            "claim_allowed": "theorem target only",
        },
        {
            "gate": "parent boundary metric derived",
            "status": "fail",
            "evidence": "Hodge/DeWitt choice not derived from parent action",
            "claim_allowed": "no q_loc promotion",
        },
        {
            "gate": "local EH exterior operator parent-derived",
            "status": "fail",
            "evidence": "metric-only/no-hair assumptions not derived",
            "claim_allowed": "no beta promotion",
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
            "meaning": "The parent-projector route is improved by a concrete boundary Hodge/DeWitt metric candidate: harmonic H^2 flux defines Pi_M and M_eff, trace-free shell tensors define Pi_TF, direct matter/clock vertices define Pi_matter, and P_mem is their orthogonal complement in the relative memory sector. The beta route is also sharpened by a local EH/Lovelock sufficient gate. Neither route is parent-derived yet because the boundary metric, Bianchi-safe variation, no-hair algebra, and metric-only exterior operator remain open.",
            "main_gain": "P_mem can now be judged against a concrete Hodge/DeWitt orthogonality contract instead of a loose projection",
            "main_failure": "the boundary metric and local EH exterior operator are candidates, not parent theorems",
            "next_target": "234-boundary-metric-variation-and-Bianchi-ledger.md",
            "promotion_allowed": "false",
            "claim_ceiling": CLAIM_CEILING,
        }
    ]


def run(timestamp: str | None = None) -> dict[str, Any]:
    run_timestamp = timestamp or datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RUNS_ROOT / f"{run_timestamp}-{CHECKPOINT_233_NAME}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    boundary_metric = boundary_metric_rows()
    orthogonality = orthogonality_rows()
    eh_gate = local_eh_gate_rows()
    coefficients = coefficient_status_rows()
    blockers = blocker_rows()
    gates = claim_gate_rows(source_rows, coefficients)
    decision = decision_rows()

    files: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_register.csv": (
            source_rows,
            ["source", "path", "exists", "sha256", "role", "issue"],
        ),
        "boundary_metric_candidate.csv": (
            boundary_metric,
            ["block", "metric_piece", "orthogonal_projector", "owner_status", "promotion_gap"],
        ),
        "projector_orthogonality_ledger.csv": (
            orthogonality,
            ["orthogonality", "reason", "consequence", "status"],
        ),
        "local_EH_operator_gate.csv": (
            eh_gate,
            ["clause", "condition", "result_if_true", "status"],
        ),
        "coefficient_status_after_233.csv": (
            coefficients,
            [
                "residual",
                "checkpoint_232_status",
                "checkpoint_233_status",
                "coefficient_after_233",
                "parent_derived",
                "promotion_allowed",
                "next_needed",
            ],
        ),
        "blocker_priority_after_233.csv": (
            blockers,
            ["blocker", "why_it_matters", "current_status", "next_attack"],
        ),
        "claim_gate_results.csv": (
            gates,
            ["gate", "status", "evidence", "claim_allowed"],
        ),
        "decision.csv": (
            decision,
            [
                "decision",
                "meaning",
                "main_gain",
                "main_failure",
                "next_target",
                "promotion_allowed",
                "claim_ceiling",
            ],
        ),
    }
    for filename, file_data in files.items():
        rows, fieldnames = file_data
        write_csv(results_dir / filename, rows, fieldnames)

    missing_sources = sum(row["exists"] != "yes" for row in source_rows)
    status_payload = {
        "status": decision[0]["decision"],
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(files.keys()),
        "missing_sources": missing_sources,
        "boundary_Hodge_DeWitt_metric_candidate_written": True,
        "Pmem_orthogonal_complement_route_written": True,
        "local_EH_Lovelock_gate_written": True,
        "parent_boundary_metric_derived": False,
        "local_EH_exterior_operator_derived": False,
        "beta_second_order_parent_derived": False,
        "official_bounds_applied_as_pass_fail": False,
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
