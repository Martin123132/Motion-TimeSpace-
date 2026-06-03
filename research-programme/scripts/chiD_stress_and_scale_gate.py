#!/usr/bin/env python3
"""Gate chi_D stress and transition scale for local-GR safety."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "13_local_ppn_doc": Path("13-local-closure-PPN-benchmark.md"),
    "64_binding_invariant_doc": Path("64-binding-invariant-domain-selector-attempt.md"),
    "65_Ccoh_phase_doc": Path("65-Ccoh-phase-field-selector-attempt.md"),
    "65_status": Path("runs/20260531-111502-Ccoh-phase-field-selector-attempt/status.json"),
    "65_variation_chain": Path("runs/20260531-111502-Ccoh-phase-field-selector-attempt/results/variation_chain.csv"),
    "65_parameter_risks": Path("runs/20260531-111502-Ccoh-phase-field-selector-attempt/results/parameter_risk_register.csv"),
    "65_gates": Path("runs/20260531-111502-Ccoh-phase-field-selector-attempt/results/gate_results.csv"),
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


def stress_equation_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "equation": "S_chi = -1/2 integral sqrt(-g) rho_chi[ell_chi^2 h^munu nabla_mu chi nabla_nu chi + (chi-C_coh)^2]",
            "status": "canonical_rescaled_form",
            "meaning": "separates selector equation scale ell_chi from stress amplitude rho_chi",
            "risk": "rho_chi and ell_chi are new universal quantities unless parent-derived",
        },
        {
            "step": 2,
            "equation": "E_chi: ell_chi^2 D^2 chi - (chi-C_coh)=0",
            "status": "same_selector_equation",
            "meaning": "overall rho_chi cancels from the chi equation if rho_chi is nonzero",
            "risk": "very small rho_chi can suppress stress without changing classical selector, but this needs a parent reason",
        },
        {
            "step": 3,
            "equation": "T_chi_munu ~ rho_chi[ell_chi^2 nabla_mu chi nabla_nu chi + metric terms]",
            "status": "stress_owner_identified",
            "meaning": "a dynamical selector gravitates through gradients and potential mismatch",
            "risk": "unsuppressed rho_chi creates local fifth-source/PPN hair",
        },
        {
            "step": 4,
            "equation": "homogeneous branch chi=C_coh -> nabla chi=0 and (chi-C_coh)=0",
            "status": "bulk_stress_can_vanish",
            "meaning": "Minkowski, stationary local interiors, and FLRW background need not carry bulk chi stress",
            "risk": "transition layers and C_coh gradients still carry stress",
        },
        {
            "step": 5,
            "equation": "transition stress density ~ rho_chi, surface tension ~ rho_chi ell_chi (Delta chi)^2",
            "status": "boundary_risk",
            "meaning": "local danger is concentrated near domain walls or coherence-transition layers",
            "risk": "large boundaries with non-negligible rho_chi ell_chi can source metric deviations",
        },
        {
            "step": 6,
            "equation": "local safety requires Phi_chi ~ 4 pi G rho_chi R_D ell_chi (Delta chi)^2 << Phi_PPN_bound",
            "status": "bound_contract",
            "meaning": "PPN safety becomes a concrete amplitude/scale inequality",
            "risk": "without numeric or parent bound this remains an open gate",
        },
    ]


def branch_stress_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "Minkowski_quiet",
            "chi_behavior": "chi=0, C_coh=0, gradients absent",
            "bulk_stress": "zero",
            "boundary_stress": "none if no domain wall",
            "status": "pass_conditional",
            "remaining_gap": "quiet-limit convention must be parent-compatible",
        },
        {
            "branch": "stationary_bound_interior",
            "chi_behavior": "chi approximately 0 in low-C_coh domain",
            "bulk_stress": "suppressed if chi tracks C_coh",
            "boundary_stress": "possible at transition to exterior/coherent environment",
            "status": "pass_conditional",
            "remaining_gap": "need rho_chi ell_chi local bound",
        },
        {
            "branch": "tracefree_shear",
            "chi_behavior": "C_coh=0, chi=0",
            "bulk_stress": "zero in scalar selector channel",
            "boundary_stress": "none unless C_coh changes across domain",
            "status": "pass",
            "remaining_gap": "radiative/shear sector separate",
        },
        {
            "branch": "FLRW_background",
            "chi_behavior": "chi=1, C_coh=1, homogeneous",
            "bulk_stress": "zero for relaxation potential at minimum",
            "boundary_stress": "none for global homogeneous branch",
            "status": "pass_kinematic",
            "remaining_gap": "cosmological memory must come from memory sector, not T_chi dark energy",
        },
        {
            "branch": "local_to_FLRW_transition",
            "chi_behavior": "chi changes from low to high over ell_chi",
            "bulk_stress": "localized transition stress",
            "boundary_stress": "rho_chi ell_chi controlled surface source",
            "status": "open",
            "remaining_gap": "main local-GR danger",
        },
        {
            "branch": "collapse_merger",
            "chi_behavior": "C_exp/C_coh dynamic and gradient-rich",
            "bulk_stress": "possibly active",
            "boundary_stress": "possibly active",
            "status": "open",
            "remaining_gap": "strong-field branch not solved",
        },
    ]


def scale_option_rows() -> list[dict[str, Any]]:
    return [
        {
            "option": "auxiliary_zero_stress_selector",
            "definition": "chi_D is a constrained auxiliary/domain bookkeeping field with no independent T_chi",
            "local_safety": "best",
            "cosmology": "keeps memory-sector activation without adding dark energy stress",
            "status": "best_if_parent_legal",
            "risk": "must be justified by constrained/topological parent action, not wishful deletion of stress",
        },
        {
            "option": "small_rho_chi_universal",
            "definition": "rho_chi is universally tiny while E_chi remains valid",
            "local_safety": "possible if rho_chi R_D ell_chi is below PPN bound",
            "cosmology": "selector can still route memory, but does not itself drive expansion",
            "status": "conditional",
            "risk": "small amplitude is a new hierarchy unless parent-derived",
        },
        {
            "option": "microscopic_ell_chi",
            "definition": "transition layer is extremely thin",
            "local_safety": "surface potential can be small if rho_chi ell_chi is small",
            "cosmology": "sharp domain limit possible",
            "status": "conditional",
            "risk": "large gradients may invalidate continuum/coarse-grained treatment",
        },
        {
            "option": "cosmological_ell_chi",
            "definition": "transition layer is very broad",
            "local_safety": "gradients small locally but chi may vary through local systems",
            "cosmology": "smooth background selector",
            "status": "risky",
            "risk": "can become hidden MOND-like/coarse-graining length",
        },
        {
            "option": "fit_ell_chi_per_system",
            "definition": "choose transition width separately for solar, galaxy, and cosmology arenas",
            "local_safety": "can be made to pass",
            "cosmology": "can be made to pass",
            "status": "rejected",
            "risk": "empirical smoothing knob",
        },
    ]


def conservation_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "bulk_minimum_stress",
            "status": "pass_conditional",
            "test": "chi=C_coh and gradients vanish on homogeneous branches",
            "implication": "no unavoidable bulk T_chi in ideal local/FLRW interiors",
        },
        {
            "gate": "boundary_stress_bound",
            "status": "open",
            "test": "4 pi G rho_chi R_D ell_chi (Delta chi)^2 << Phi_PPN_bound",
            "implication": "must be satisfied for solar/local systems",
        },
        {
            "gate": "Bianchi_identity",
            "status": "open",
            "test": "nabla_mu(T_chi^munu + T_mem^munu + T_matter^munu)=0",
            "implication": "C_coh dependence on theta/sigma/omega must be included, not frozen by hand",
        },
        {
            "gate": "cosmology_not_from_Tchi",
            "status": "pass_conditional",
            "test": "FLRW chi=C_coh=1 gives T_chi approximately 0",
            "implication": "cosmological signal must remain in memory sector, avoiding extra dark-energy fluid claim",
        },
        {
            "gate": "new_scale_parent_origin",
            "status": "fail",
            "test": "ell_chi derived from existing u3/L_cg/cell scale or topological normalization",
            "implication": "currently not derived",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "stress_tensor_identified",
            "status": "pass",
            "detail": "T_chi source and boundary-stress scaling are explicit",
        },
        {
            "gate": "bulk_background_safe",
            "status": "pass_conditional",
            "detail": "homogeneous chi=C_coh branches have vanishing relaxation stress",
        },
        {
            "gate": "local_boundary_stress_bounded",
            "status": "open",
            "detail": "requires rho_chi ell_chi bound against PPN/local potential limits",
        },
        {
            "gate": "ell_chi_parent_derived",
            "status": "fail",
            "detail": "transition length is not yet tied to a parent cell/coherence scale",
        },
        {
            "gate": "Bianchi_conservation_resolved",
            "status": "open",
            "detail": "variation of C_coh and memory stress must be included in conserved total stress",
        },
        {
            "gate": "dynamic_scalar_promoted",
            "status": "fail",
            "detail": "a fully dynamical chi_D scalar cannot be promoted until stress and scale are controlled",
        },
        {
            "gate": "auxiliary_selector_route_open",
            "status": "pass_conditional",
            "detail": "the safest route is a constrained/topological auxiliary selector with no independent local stress",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "this is a safety gate, not evidence for MTS",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "chiD_stress_scale_status",
            "status": "dynamic_selector_not_promoted_auxiliary_route_preferred",
            "evidence": "bulk stress can vanish on ideal branches, but boundary stress rho_chi ell_chi and scale ell_chi remain unbounded",
            "next_action": "attempt constrained auxiliary/topological chi_D owner or derive ell_chi from existing cell scale",
        },
        {
            "decision": "local_GR_route_status",
            "status": "alive_but_dynamic_chiD_unsafe_until_bound",
            "evidence": "local interiors are conditionally safe; transition layers are the unresolved PPN danger",
            "next_action": "write auxiliary selector/no-stress parent contract",
        },
        {
            "decision": "recommended_next_target",
            "status": "67-auxiliary-selector-parent-contract.md",
            "evidence": "the cleanest route is to make chi_D a constrained domain projector/topological variable rather than a gravitating scalar",
            "next_action": "state the exact parent contract for a no-independent-stress selector",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "dynamic_selector_not_promoted_auxiliary_route_preferred",
        "key_metrics": {
            "stress_equation_steps": counts["stress_equation_chain"],
            "branch_stress_tests": counts["branch_stress_tests"],
            "scale_options": counts["scale_option_ledger"],
            "conservation_gates": counts["conservation_gate_tests"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "decision": decision_rows()[0],
        "next_target": "67-auxiliary-selector-parent-contract.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-chiD-stress-and-scale-gate"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "stress_equation_chain": (
            stress_equation_rows(),
            ["step", "equation", "status", "meaning", "risk"],
        ),
        "branch_stress_tests": (
            branch_stress_rows(),
            ["branch", "chi_behavior", "bulk_stress", "boundary_stress", "status", "remaining_gap"],
        ),
        "scale_option_ledger": (
            scale_option_rows(),
            ["option", "definition", "local_safety", "cosmology", "status", "risk"],
        ),
        "conservation_gate_tests": (
            conservation_gate_rows(),
            ["gate", "status", "test", "implication"],
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
