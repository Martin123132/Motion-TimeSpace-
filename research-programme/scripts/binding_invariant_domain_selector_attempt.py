#!/usr/bin/env python3
"""Attempt a binding/coherence invariant that can drive chi_D without GR/Newton import."""

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
    "61_boundary_theorem_doc": Path("61-bound-domain-boundary-theorem-attempt.md"),
    "62_chiD_contract_doc": Path("62-domain-field-chiD-action-contract.md"),
    "63_chiD_variation_doc": Path("63-chiD-variation-to-boundary-equation-attempt.md"),
    "63_status": Path("runs/20260531-110848-chiD-variation-to-boundary-equation-attempt/status.json"),
    "63_candidate_variations": Path("runs/20260531-110848-chiD-variation-to-boundary-equation-attempt/results/candidate_variation_ledger.csv"),
    "63_no_go": Path("runs/20260531-110848-chiD-variation-to-boundary-equation-attempt/results/no_go_findings.csv"),
    "63_gates": Path("runs/20260531-110848-chiD-variation-to-boundary-equation-attempt/results/gate_results.csv"),
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


def candidate_invariant_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "Newtonian_binding_energy",
            "schematic": "C_bind ~ |Phi|/v^2 or E_total<0",
            "uses": "potential energy and orbital binding",
            "local_bound_result": "good phenomenology",
            "FLRW_result": "not naturally defined without background subtraction",
            "verdict": "rejected_import",
            "reason": "imports Newton/GR-style binding instead of deriving MTS domain selection",
        },
        {
            "candidate": "GR_turnaround_surface",
            "schematic": "C_bind from turnaround or apparent static radius",
            "uses": "GR/geodesic or spherical-collapse logic",
            "local_bound_result": "plausible for isolated masses",
            "FLRW_result": "preserves expanding exterior",
            "verdict": "rejected_import",
            "reason": "too close to assuming the GR reduction we are trying to derive",
        },
        {
            "candidate": "coherent_volume_flow_purity",
            "schematic": "C_coh = <theta>_D^2 / (<theta^2>_D + <sigma^2>_D + <omega^2>_D + eps)",
            "uses": "expansion/shear/vorticity invariants of the motion congruence",
            "local_bound_result": "low for stationary, virial, shear, and orbital domains with near-zero mean volume flux",
            "FLRW_result": "high for homogeneous expansion where sigma=omega=0 and theta=3H",
            "verdict": "best_kinematic_candidate",
            "reason": "uses motion/volume-flow structure rather than Newtonian potential or PPN residuals",
        },
        {
            "candidate": "signed_coherent_expansion_index",
            "schematic": "C_exp = sign(<theta>_D) <theta>_D^2 / (<theta^2>_D + <sigma^2>_D + <omega^2>_D + eps)",
            "uses": "same invariants plus expansion sign",
            "local_bound_result": "zero/low for stationary bound domains; negative for coherent collapse",
            "FLRW_result": "positive/high for expanding FLRW",
            "verdict": "best_dynamic_extension",
            "reason": "distinguishes expansion from collapse without a fitted boundary switch",
        },
        {
            "candidate": "time_averaged_volume_flux",
            "schematic": "C_avg = |<d ln V_D/dtau>_T| / <|local deformation|>_T",
            "uses": "domain-averaged volume growth over internal dynamical time",
            "local_bound_result": "low for virialized systems",
            "FLRW_result": "high for secular expansion",
            "verdict": "conditional_support",
            "reason": "needs a parent averaging time and can otherwise become a smoothing knob",
        },
        {
            "candidate": "empirical_domain_score",
            "schematic": "C chosen to minimize PPN/cosmology residuals",
            "uses": "data residuals",
            "local_bound_result": "can pass by construction",
            "FLRW_result": "can pass by construction",
            "verdict": "rejected",
            "reason": "not theory; forbidden by checkpoints 61-63",
        },
    ]


def invariant_equation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "equation": "Theta_ij = (1/3) theta h_ij + sigma_ij; omega_ij from antisymmetric congruence rotation",
            "status": "kinematic",
            "meaning": "decompose motion into coherent volume expansion, shear, and rotation",
            "gap": "requires parent choice of observer/congruence u^mu",
        },
        {
            "step": 2,
            "equation": "C_coh[D] = <theta>_D^2 / (<theta^2>_D + <sigma^2>_D + <omega^2>_D + eps_D)",
            "status": "candidate",
            "meaning": "measure how much of the domain motion is coherent volume expansion",
            "gap": "eps_D and domain average must be parent-defined or limiting",
        },
        {
            "step": 3,
            "equation": "C_exp[D] = sign(<theta>_D) C_coh[D]",
            "status": "candidate_dynamic_extension",
            "meaning": "separate coherent expansion from coherent collapse",
            "gap": "collapse/merger branch remains open",
        },
        {
            "step": 4,
            "equation": "FLRW: sigma=omega=0, theta=3H -> C_coh approx 1, C_exp approx +1",
            "status": "pass_kinematic",
            "meaning": "homogeneous expansion is selected as active",
            "gap": "does not by itself derive memory amplitude",
        },
        {
            "step": 5,
            "equation": "stationary_bound: <theta>_D=0 -> C_coh approx 0 even with internal shear/orbital motion",
            "status": "pass_conditional",
            "meaning": "bound local systems can be selected as inactive in scalar volume memory",
            "gap": "must derive the averaging/domain D, not fit it",
        },
        {
            "step": 6,
            "equation": "phase-field drive: kappa D^2 chi_D - dU(chi_D,C_coh)/dchi_D = 0",
            "status": "next_action",
            "meaning": "C_coh can drive chi_D only inside a real action",
            "gap": "action variation and conservation still unproven",
        },
    ]


def arena_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "Minkowski_patch",
            "theta": "0",
            "sigma_omega": "0",
            "C_coh_result": "0 by quiet-limit convention",
            "domain_result": "inactive",
            "status": "pass_conditional",
            "gap": "quiet-limit convention must be explicit",
        },
        {
            "arena": "stationary_solar_system",
            "theta": "mean approximately 0",
            "sigma_omega": "internal orbital/shear terms nonzero",
            "C_coh_result": "low",
            "domain_result": "bound/inactive scalar volume channel",
            "status": "pass_conditional",
            "gap": "needs MTS averaging theorem, not PPN import",
        },
        {
            "arena": "virialized_galaxy",
            "theta": "time-averaged mean approximately 0",
            "sigma_omega": "orbital terms nonzero",
            "C_coh_result": "low for local-volume channel",
            "domain_result": "locally inactive while galaxy empirical pillar must be separate",
            "status": "pass_conditional",
            "gap": "avoid erasing galaxy phenomenology",
        },
        {
            "arena": "tracefree_shear_domain",
            "theta": "0",
            "sigma_omega": "sigma nonzero",
            "C_coh_result": "0",
            "domain_result": "inactive scalar volume channel",
            "status": "pass",
            "gap": "shear/radiative sector not addressed",
        },
        {
            "arena": "FLRW_background",
            "theta": "3H",
            "sigma_omega": "0",
            "C_coh_result": "near 1",
            "domain_result": "active coherent expansion",
            "status": "pass_kinematic",
            "gap": "normalization u3 and amplitude b_mem still separate",
        },
        {
            "arena": "collapse_or_merger",
            "theta": "nonzero and possibly negative/inhomogeneous",
            "sigma_omega": "large",
            "C_coh_result": "mixed or signed-negative",
            "domain_result": "dynamic/open",
            "status": "open",
            "gap": "strong-field dynamic branch needed",
        },
    ]


def nonimport_tests_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "does_not_use_Newtonian_potential",
            "status": "pass",
            "evidence": "C_coh uses theta, sigma, omega rather than Phi, E_total, or escape speed",
            "remaining_risk": "observer/congruence choice still must be parent-derived",
        },
        {
            "test": "does_not_use_GR_turnaround",
            "status": "pass_partial",
            "evidence": "no Schwarzschild/de Sitter or spherical collapse radius is used",
            "remaining_risk": "kinematic decomposition must not secretly assume GR field equations",
        },
        {
            "test": "separates_FLRW_from_stationary_local",
            "status": "pass_kinematic",
            "evidence": "FLRW has coherent theta with no shear/vorticity; stationary bound domains have near-zero mean theta",
            "remaining_risk": "needs robust averaging/domain theorem",
        },
        {
            "test": "not_data_tuned",
            "status": "pass_partial",
            "evidence": "definition is fixed before fitting",
            "remaining_risk": "eps_D, thresholds, and time averages could become tunable unless action-derived",
        },
        {
            "test": "derives_binding",
            "status": "fail",
            "evidence": "C_coh classifies coherent expansion purity; it does not yet derive gravitational binding",
            "remaining_risk": "local branch remains closure-level if phase-field action cannot use C_coh non-arbitrarily",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "candidate_invariant_identified",
            "status": "pass",
            "detail": "C_coh/C_exp provide a kinematic motion-volume invariant candidate",
        },
        {
            "gate": "Newton_GR_import_avoided",
            "status": "pass_partial",
            "detail": "best candidate avoids potentials/turnaround radii but still needs parent congruence and averaging",
        },
        {
            "gate": "FLRW_local_separation",
            "status": "pass_kinematic",
            "detail": "FLRW is high coherent expansion; stationary local/virial domains are low coherent expansion",
        },
        {
            "gate": "binding_selector_derived",
            "status": "fail",
            "detail": "C_coh is a classifier/invariant, not yet a derived binding equation",
        },
        {
            "gate": "chiD_drive_ready",
            "status": "open",
            "detail": "phase-field chi_D action can now be attempted with C_coh as source/potential argument",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "this is a candidate invariant, not evidence or a complete local-GR derivation",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "binding_invariant_status",
            "status": "coherent_expansion_invariant_found_not_binding_derivation",
            "evidence": "C_coh/C_exp distinguish FLRW coherent expansion from stationary local volume flow without Newtonian potential or GR turnaround",
            "next_action": "test phase-field chi_D action driven by C_coh",
        },
        {
            "decision": "local_GR_route_status",
            "status": "alive_with_new_bottleneck",
            "evidence": "local silence can be tied to low coherent volume-flow purity, but binding/domain selection is not yet derived",
            "next_action": "derive or reject chi_D potential U(chi_D,C_coh)",
        },
        {
            "decision": "recommended_next_target",
            "status": "65-Ccoh-phase-field-selector-attempt.md",
            "evidence": "the next mathematical test is whether C_coh can source chi_D without becoming a tunable threshold",
            "next_action": "vary a minimal phase-field action with C_coh and check local/FLRW branches",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "coherent_expansion_invariant_found_not_binding_derivation",
        "key_metrics": {
            "candidate_invariants": counts["candidate_invariant_ledger"],
            "equation_chain_steps": counts["invariant_equation_chain"],
            "arena_tests": counts["arena_separation_tests"],
            "nonimport_tests": counts["nonimport_tests"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "partial_pass_gates": sum(1 for row in gates if row["status"] == "pass_partial"),
        },
        "decision": decision_rows()[0],
        "next_target": "65-Ccoh-phase-field-selector-attempt.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-binding-invariant-domain-selector-attempt"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "candidate_invariant_ledger": (
            candidate_invariant_rows(),
            ["candidate", "schematic", "uses", "local_bound_result", "FLRW_result", "verdict", "reason"],
        ),
        "invariant_equation_chain": (
            invariant_equation_chain_rows(),
            ["step", "equation", "status", "meaning", "gap"],
        ),
        "arena_separation_tests": (
            arena_test_rows(),
            ["arena", "theta", "sigma_omega", "C_coh_result", "domain_result", "status", "gap"],
        ),
        "nonimport_tests": (
            nonimport_tests_rows(),
            ["test", "status", "evidence", "remaining_risk"],
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
