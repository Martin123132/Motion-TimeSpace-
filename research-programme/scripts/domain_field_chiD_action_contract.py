#!/usr/bin/env python3
"""Write the chi_D domain-selector action contract for the local-boundary route."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "53_projection_doc": Path("53-coherent-projection-local-silence-gate.md"),
    "60_relative_boundary_doc": Path("60-relative-cohomology-boundary-contract.md"),
    "61_boundary_theorem_doc": Path("61-bound-domain-boundary-theorem-attempt.md"),
    "61_status": Path("runs/20260531-110230-bound-domain-boundary-theorem-attempt/status.json"),
    "61_boundary_chain": Path("runs/20260531-110230-bound-domain-boundary-theorem-attempt/results/boundary_theorem_chain.csv"),
    "61_domain_candidates": Path("runs/20260531-110230-bound-domain-boundary-theorem-attempt/results/domain_candidate_tests.csv"),
    "61_gates": Path("runs/20260531-110230-bound-domain-boundary-theorem-attempt/results/gate_results.csv"),
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


def chiD_object_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "chi_D",
            "definition": "covariant domain selector or smooth window field with chi_D approximately 1 inside D and 0 outside",
            "required_role": "defines the support used in V_D, <theta>_D, Q_coh, and the relative memory class",
            "allowed": "may be a scalar, constrained phase/window field, or equivalent boundary current representation",
            "forbidden": "may not be chosen after seeing PPN, SPARC, or cosmology residuals",
        },
        {
            "object": "Sigma_D",
            "definition": "boundary hypersurface or level set associated with chi_D",
            "required_role": "carries the boundary flux integral integral_boundary(D) v_n dA",
            "allowed": "can be sharp-boundary limit of chi_D or independent boundary degree of freedom",
            "forbidden": "cannot be a hand-drawn silencing surface",
        },
        {
            "object": "J_D^mu",
            "definition": "domain/boundary current whose normal flux controls dV_D/dtau",
            "required_role": "turns volume-flow extremality into an Euler-Lagrange or conservation statement",
            "allowed": "may be built from u^mu, h_munu, chi_D, and coherent expansion data",
            "forbidden": "cannot be a fitted phenomenological switch",
        },
        {
            "object": "E_chi",
            "definition": "Euler-Lagrange equation from varying chi_D or its boundary representative",
            "required_role": "selects stationary bound boundaries and coherent FLRW domains",
            "allowed": "can include constraints and Lagrange multipliers if they are universal",
            "forbidden": "cannot encode local-observable pass/fail information",
        },
    ]


def action_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "covariant_domain_definition",
            "contract": "D is the support/level-set of chi_D on the observer/coherent foliation, with V_D=int chi_D dSigma",
            "success_requirement": "the same definition applies to local systems and FLRW",
            "current_status": "contract_written",
            "failure_mode": "D remains an informal coarse-graining choice",
        },
        {
            "condition": "volume_flux_variation",
            "contract": "variation of S_D with respect to chi_D or Sigma_D yields a boundary equation equivalent to extremal coherent volume flux",
            "success_requirement": "stationary branch gives dV_D/dtau=0 without referencing local-test residuals",
            "current_status": "not_derived",
            "failure_mode": "local silence is still assumed",
        },
        {
            "condition": "FLRW_comoving_solution",
            "contract": "on homogeneous FLRW, the same E_chi=0 admits coherent comoving domains with d ln V_D/dtau=3H",
            "success_requirement": "cosmological memory remains active",
            "current_status": "pass_conditional",
            "failure_mode": "domain action kills the cosmology branch",
        },
        {
            "condition": "bound_stationary_solution",
            "contract": "for stationary/virialized bound systems, E_chi=0 selects a closed or asymptotically stable boundary with zero net coherent volume flux",
            "success_requirement": "Q_coh=0 follows from the field equation",
            "current_status": "not_derived",
            "failure_mode": "PPN safety depends on manual boundary choice",
        },
        {
            "condition": "Bianchi_compatible_stress",
            "contract": "chi_D sector stress and memory stress must fit a covariant conservation identity",
            "success_requirement": "no hidden energy-momentum leak from switching domains",
            "current_status": "open",
            "failure_mode": "local GR reduction breaks at conservation level",
        },
        {
            "condition": "universal_parameters",
            "contract": "any stiffness, potential, multiplier, or transition scale in S_D is universal or parent-derived",
            "success_requirement": "no object-specific fitted smoothing length",
            "current_status": "open",
            "failure_mode": "chi_D becomes a flexible phenomenological patch",
        },
    ]


def candidate_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "constraint_current_action",
            "schematic_form": "S_D = int sqrt(-g) lambda_D nabla_mu J_D^mu plus boundary term",
            "what_it_could_do": "enforce conserved or extremal domain flux as a constraint",
            "status": "best_next_variation_attempt",
            "risk": "constraint may impose rather than derive the physical boundary",
        },
        {
            "candidate": "phase_field_boundary_action",
            "schematic_form": "S_D = int sqrt(-g)[-kappa_D/2 h^munu nabla_mu chi_D nabla_nu chi_D - U(chi_D,C)]",
            "what_it_could_do": "make boundaries into field solutions instead of hand-cut regions",
            "status": "plausible_contract",
            "risk": "requires a principled potential U and coupling C",
        },
        {
            "candidate": "volume_flux_extremal_action",
            "schematic_form": "S_D = int d tau Phi(d ln V_D/dtau, C_D) with delta S_D/delta chi_D = 0",
            "what_it_could_do": "directly extremize coherent volume flow",
            "status": "sharp_but_dangerous",
            "risk": "may be nonlocal or too engineered unless rewritten covariantly",
        },
        {
            "candidate": "relative_boundary_topological_pairing",
            "schematic_form": "S_D = int_{D,boundary D} B wedge F + boundary pairing with chi_D",
            "what_it_could_do": "tie domain selection to the relative memory class",
            "status": "live_extension",
            "risk": "still has not selected p=3, u3=1/4, or b_mem",
        },
        {
            "candidate": "empirical_window_function",
            "schematic_form": "choose chi_D from the system being tested",
            "what_it_could_do": "fit/silence almost anything",
            "status": "rejected",
            "risk": "not a theory",
        },
    ]


def selection_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "Minkowski_control",
            "required_E_chi_result": "constant/stationary chi_D solution with dV_D/dtau=0",
            "memory_result": "Q_coh=0",
            "status": "pass_conditional",
            "gap": "easy control, not a full derivation",
        },
        {
            "arena": "stationary_solar_system",
            "required_E_chi_result": "closed bound-domain boundary or equivalent asymptotically stationary selector",
            "memory_result": "Q_coh=0 from E_chi, not from PPN tuning",
            "status": "not_derived",
            "gap": "central target of the next variation attempt",
        },
        {
            "arena": "virialized_galaxy",
            "required_E_chi_result": "time-averaged stable volume boundary while preserving separate galaxy phenomenology",
            "memory_result": "local scalar volume channel quiet, galaxy pillar not erased",
            "status": "open",
            "gap": "needs an MTS averaging/virial theorem",
        },
        {
            "arena": "FLRW_background",
            "required_E_chi_result": "coherent comoving solution with d ln V_D/dtau=3H",
            "memory_result": "Q_coh^i_j=(N/u3)delta^i_j",
            "status": "pass_conditional",
            "gap": "normalization and amplitude still underived",
        },
        {
            "arena": "collapse_merger",
            "required_E_chi_result": "dynamic boundary equation with controlled active memory",
            "memory_result": "not forced to zero",
            "status": "open",
            "gap": "strong-field/radiative sector missing",
        },
    ]


def falsification_rows() -> list[dict[str, Any]]:
    return [
        {
            "failure": "chiD_depends_on_observed_residuals",
            "meaning": "the domain selector changes because a local/cosmology dataset fails",
            "consequence": "demote local transition route to closure-only",
        },
        {
            "failure": "no_covariant_E_chi",
            "meaning": "there is no Euler-Lagrange/conservation equation for the domain field",
            "consequence": "boundary rule remains kinematic dressing",
        },
        {
            "failure": "FLRW_solution_not_supported",
            "meaning": "the same domain action cannot admit d ln V_D/dtau=3H coherent domains",
            "consequence": "domain route kills the cosmology branch",
        },
        {
            "failure": "bound_stationary_solution_not_supported",
            "meaning": "stationary local domains are not zero-flux solutions",
            "consequence": "local PPN branch fails or needs a different local-GR mechanism",
        },
        {
            "failure": "stress_not_conserved",
            "meaning": "domain/memory stress violates the conservation identity required by the metric equations",
            "consequence": "local GR reduction is not credible",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "chiD_object_defined",
            "status": "pass",
            "detail": "domain selector/window field and boundary-current objects are specified as contract objects",
        },
        {
            "gate": "action_contract_written",
            "status": "pass",
            "detail": "parent action obligations are explicit enough for the next variation attempt",
        },
        {
            "gate": "stationary_bound_boundary_derived",
            "status": "fail",
            "detail": "no variation has yet produced dV_D/dtau=0 for bound systems",
        },
        {
            "gate": "FLRW_active_solution_preserved",
            "status": "pass_conditional",
            "detail": "contract requires same E_chi to admit d ln V_D/dtau=3H",
        },
        {
            "gate": "Bianchi_conservation_resolved",
            "status": "open",
            "detail": "domain/memory stress conservation remains a required compatibility gate",
        },
        {
            "gate": "no_empirical_window_tuning",
            "status": "pass_conditional",
            "detail": "contract forbids dataset-dependent chi_D choice, but parent action must enforce this",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "this is an action contract, not a derivation or empirical result",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "chiD_action_status",
            "status": "contract_written_not_varied",
            "evidence": "the future parent action obligations are now explicit, including E_chi, zero-flux bound solutions, FLRW active solutions, and conservation",
            "next_action": "attempt an explicit variation that yields the boundary equation",
        },
        {
            "decision": "local_transition_route_status",
            "status": "alive_but_closure_until_variation",
            "evidence": "chi_D can make the boundary theorem non-arbitrary only if varied from an action",
            "next_action": "derive or reject E_chi -> dV_D/dtau=0 for stationary bound domains",
        },
        {
            "decision": "recommended_next_target",
            "status": "63-chiD-variation-to-boundary-equation-attempt.md",
            "evidence": "checkpoint 62 defines the contract; checkpoint 63 must try the actual math",
            "next_action": "perform the variation on the least-engineered candidate action",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "chiD_action_contract_written_not_varied",
        "key_metrics": {
            "chiD_objects": counts["chiD_object_register"],
            "action_contract_conditions": counts["action_contract"],
            "candidate_actions": counts["candidate_action_routes"],
            "selection_gates": counts["selection_gate_tests"],
            "falsification_tests": counts["falsification_tests"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "decision": decision_rows()[0],
        "next_target": "63-chiD-variation-to-boundary-equation-attempt.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-domain-field-chiD-action-contract"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "chiD_object_register": (
            chiD_object_rows(),
            ["object", "definition", "required_role", "allowed", "forbidden"],
        ),
        "action_contract": (
            action_contract_rows(),
            ["condition", "contract", "success_requirement", "current_status", "failure_mode"],
        ),
        "candidate_action_routes": (
            candidate_action_rows(),
            ["candidate", "schematic_form", "what_it_could_do", "status", "risk"],
        ),
        "selection_gate_tests": (
            selection_gate_rows(),
            ["arena", "required_E_chi_result", "memory_result", "status", "gap"],
        ),
        "falsification_tests": (
            falsification_rows(),
            ["failure", "meaning", "consequence"],
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
