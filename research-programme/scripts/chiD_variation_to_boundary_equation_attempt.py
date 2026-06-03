#!/usr/bin/env python3
"""Attempt to vary chi_D/domain actions into the required boundary equation."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "61_boundary_theorem_doc": Path("61-bound-domain-boundary-theorem-attempt.md"),
    "62_chiD_contract_doc": Path("62-domain-field-chiD-action-contract.md"),
    "62_status": Path("runs/20260531-110553-domain-field-chiD-action-contract/status.json"),
    "62_action_contract": Path("runs/20260531-110553-domain-field-chiD-action-contract/results/action_contract.csv"),
    "62_candidate_actions": Path("runs/20260531-110553-domain-field-chiD-action-contract/results/candidate_action_routes.csv"),
    "62_gates": Path("runs/20260531-110553-domain-field-chiD-action-contract/results/gate_results.csv"),
}


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for key, relative_path in SOURCE_PATHS.items():
        absolute_path = POST_CHECKPOINT / relative_path
        rows.append(
            {
                "source_key": key,
                "relative_path": str(relative_path),
                "absolute_path": str(absolute_path),
                "exists": absolute_path.exists(),
            }
        )
    missing = [row["absolute_path"] for row in rows if not row["exists"]]
    if missing:
        raise FileNotFoundError("missing source files: " + "; ".join(missing))
    return rows


def variation_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "identity": "V_D = integral_Sigma chi_D dSigma",
            "variation": "delta V_D = integral_Sigma delta chi_D dSigma",
            "readout": "chi_D variation changes the domain volume directly",
            "status": "usable",
        },
        {
            "step": 2,
            "identity": "dot V_D = integral_Sigma (L_u chi_D + chi_D theta) dSigma",
            "variation": "delta dot V_D = integral_Sigma (L_u delta chi_D + theta delta chi_D) dSigma",
            "readout": "domain flux depends on both boundary advection and expansion",
            "status": "usable",
        },
        {
            "step": 3,
            "identity": "material_domain_condition: L_u chi_D = 0",
            "variation": "dot V_D = integral_Sigma chi_D theta dSigma",
            "readout": "a transported boundary preserves FLRW activity and lets stationary zero-expansion domains be quiet",
            "status": "insufficient_selector",
        },
        {
            "step": 4,
            "identity": "stationary_branch_requirement: dot V_D = 0",
            "variation": "requires either theta average zero or a source/binding condition selecting the boundary",
            "readout": "the zero branch is not selected by advection alone",
            "status": "not_derived",
        },
        {
            "step": 5,
            "identity": "FLRW_branch_requirement: dot V_D/V_D = 3H",
            "variation": "material comoving chi_D gives dot V_D/V_D=theta=3H",
            "readout": "FLRW is easy to preserve; local bound selection is the hard part",
            "status": "pass_conditional",
        },
    ]


def candidate_variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "pure_advection_window",
            "schematic_action": "S_chi = integral sqrt(-g) lambda u^mu nabla_mu chi_D",
            "euler_equation": "u^mu nabla_mu chi_D = 0",
            "stationary_bound_result": "does not select dot V_D=0; only transports whatever D was chosen",
            "FLRW_result": "allows comoving domains with dot V_D/V_D=3H",
            "verdict": "useful_transport_not_selector",
        },
        {
            "candidate": "divergence_constraint_current",
            "schematic_action": "S_chi = integral sqrt(-g) lambda nabla_mu(chi_D u^mu)",
            "euler_equation": "nabla_mu(chi_D u^mu)=0 -> L_u chi_D + chi_D theta=0",
            "stationary_bound_result": "can force conserved volume density",
            "FLRW_result": "kills or absorbs FLRW volume growth into chi_D rather than producing active memory",
            "verdict": "fails_FLRW_activity",
        },
        {
            "candidate": "quadratic_flux_extremal",
            "schematic_action": "S_chi = integral d tau (kappa/2)(dot V_D)^2",
            "euler_equation": "d/dtau(kappa dot V_D)=0 plus endpoint/boundary terms",
            "stationary_bound_result": "dot V_D=0 is a solution with suitable boundary conditions",
            "FLRW_result": "prefers zero flux unless an external source term is added",
            "verdict": "engineered_unless_source_derived",
        },
        {
            "candidate": "phase_field_boundary",
            "schematic_action": "S_chi = integral sqrt(-g)[-kappa/2 h^munu nabla_mu chi_D nabla_nu chi_D - U(chi_D,C)]",
            "euler_equation": "kappa D^2 chi_D - dU/dchi_D = source(C)",
            "stationary_bound_result": "can form boundaries if C is a physical binding/coherence invariant",
            "FLRW_result": "can preserve FLRW only if U/source admits homogeneous comoving solution",
            "verdict": "promising_only_with_derived_binding_invariant",
        },
        {
            "candidate": "topological_relative_pairing",
            "schematic_action": "S_chi = integral_{D,boundary D} B wedge F plus boundary pairing",
            "euler_equation": "flatness/relative-class constraint plus boundary condition",
            "stationary_bound_result": "can make local class trivial if boundary class already selected",
            "FLRW_result": "can carry nontrivial expansion class if supplied",
            "verdict": "class_protector_not_domain_selector",
        },
    ]


def pass_fail_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "derive_zero_flux_bound_boundary",
            "pure_advection_window": "fail",
            "divergence_constraint_current": "partial_but_overconstrains",
            "quadratic_flux_extremal": "imposes_solution",
            "phase_field_boundary": "open_if_binding_invariant_exists",
            "topological_relative_pairing": "fail_as_selector",
        },
        {
            "requirement": "preserve_FLRW_active_memory",
            "pure_advection_window": "pass_conditional",
            "divergence_constraint_current": "fail",
            "quadratic_flux_extremal": "fail_without_source",
            "phase_field_boundary": "open",
            "topological_relative_pairing": "pass_if_class_supplied",
        },
        {
            "requirement": "avoid_PPN_tuned_boundary",
            "pure_advection_window": "partial",
            "divergence_constraint_current": "partial",
            "quadratic_flux_extremal": "partial",
            "phase_field_boundary": "pass_only_if_C_parent_derived",
            "topological_relative_pairing": "partial",
        },
        {
            "requirement": "Bianchi_conservation_ready",
            "pure_advection_window": "open",
            "divergence_constraint_current": "open",
            "quadratic_flux_extremal": "weak",
            "phase_field_boundary": "best_candidate",
            "topological_relative_pairing": "open",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "finding": "advection_is_not_selection",
            "statement": "u^mu nabla_mu chi_D=0 transports a chosen domain but does not decide which local domains are bound",
            "impact": "cannot by itself derive local GR safety",
        },
        {
            "finding": "divergence_constraint_overkills_FLRW",
            "statement": "nabla_mu(chi_D u^mu)=0 conserves the domain current and tends to absorb the 3H FLRW volume growth",
            "impact": "bad for the cosmology memory branch",
        },
        {
            "finding": "flux_square_prefers_silence",
            "statement": "a quadratic dot V_D action naturally makes zero flux an extremum unless a source selects FLRW activity",
            "impact": "looks engineered unless the source is parent-derived",
        },
        {
            "finding": "phase_field_needs_binding_invariant",
            "statement": "a phase-field boundary can select domains only if its potential is controlled by a derived binding/coherence invariant C",
            "impact": "moves next bottleneck to deriving C_bind or C_coh",
        },
        {
            "finding": "topology_protects_but_does_not_choose",
            "statement": "relative topology can protect the zero/nonzero class split after D is known, but does not yet choose D",
            "impact": "topological route remains auxiliary, not sufficient",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "variation_attempt_performed",
            "status": "pass",
            "detail": "candidate chi_D/domain actions were varied at contract level",
        },
        {
            "gate": "zero_flux_bound_boundary_derived",
            "status": "fail",
            "detail": "no minimal action produced stationary bound boundaries without extra physical input",
        },
        {
            "gate": "FLRW_active_branch_preserved",
            "status": "pass_conditional",
            "detail": "pure advection preserves FLRW, phase-field route can preserve it if source/potential is right",
        },
        {
            "gate": "noncircular_domain_selector_found",
            "status": "open",
            "detail": "phase-field route could work only with a parent-derived binding/coherence invariant",
        },
        {
            "gate": "closure_promotion_allowed",
            "status": "fail",
            "detail": "the local transition route cannot be promoted from closure on this variation alone",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "variation attempt is a red-team narrowing result, not theory support",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "chiD_variation_status",
            "status": "fails_as_full_derivation_points_to_binding_invariant",
            "evidence": "advection transports but does not select; current conservation overkills FLRW; flux extremal action imposes silence unless sourced; phase field needs derived C_bind/C_coh",
            "next_action": "attempt a parent binding/coherence invariant selector",
        },
        {
            "decision": "local_GR_route_status",
            "status": "not_dead_but_not_derived",
            "evidence": "the volume-memory silence theorem survives conditionally, but no action has selected local bound domains",
            "next_action": "derive or reject a physical C_bind/C_coh invariant that can drive chi_D",
        },
        {
            "decision": "recommended_next_target",
            "status": "64-binding-invariant-domain-selector-attempt.md",
            "evidence": "the least bad route is a phase-field/domain action controlled by a derived binding/coherence invariant",
            "next_action": "define candidate invariant C_bind or C_coh and test whether it separates bound local domains from FLRW without GR import",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "chiD_variation_fails_as_full_derivation_points_to_binding_invariant",
        "key_metrics": {
            "variation_identities": counts["variation_identity_chain"],
            "candidate_variations": counts["candidate_variation_ledger"],
            "pass_fail_requirements": counts["pass_fail_matrix"],
            "no_go_findings": counts["no_go_findings"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "decision": decision_rows()[0],
        "next_target": "64-binding-invariant-domain-selector-attempt.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-chiD-variation-to-boundary-equation-attempt"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "variation_identity_chain": (
            variation_identity_rows(),
            ["step", "identity", "variation", "readout", "status"],
        ),
        "candidate_variation_ledger": (
            candidate_variation_rows(),
            ["candidate", "schematic_action", "euler_equation", "stationary_bound_result", "FLRW_result", "verdict"],
        ),
        "pass_fail_matrix": (
            pass_fail_matrix_rows(),
            [
                "requirement",
                "pure_advection_window",
                "divergence_constraint_current",
                "quadratic_flux_extremal",
                "phase_field_boundary",
                "topological_relative_pairing",
            ],
        ),
        "no_go_findings": (
            no_go_rows(),
            ["finding", "statement", "impact"],
        ),
        "gate_results": (
            gate_rows(),
            ["gate", "status", "detail"],
        ),
        "decision": (
            decision_rows(),
            ["decision", "status", "evidence", "next_action"],
        ),
    }

    counts: dict[str, int] = {}
    for table_name, (rows, fieldnames) in tables.items():
        write_csv(result_dir / f"{table_name}.csv", rows, fieldnames)
        counts[table_name] = len(rows)

    status = status_payload(run_dir, counts)
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    return run_dir


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-root",
        type=Path,
        default=POST_CHECKPOINT / "runs",
        help="Directory where timestamped run output is written.",
    )
    args = parser.parse_args()

    run_dir = run(args.output_root)
    status = json.loads((run_dir / "status.json").read_text(encoding="utf-8"))
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
