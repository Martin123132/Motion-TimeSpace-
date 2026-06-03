#!/usr/bin/env python3
"""Test a minimal C_coh-driven phase-field selector for chi_D."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "63_chiD_variation_doc": Path("63-chiD-variation-to-boundary-equation-attempt.md"),
    "64_binding_invariant_doc": Path("64-binding-invariant-domain-selector-attempt.md"),
    "64_status": Path("runs/20260531-111219-binding-invariant-domain-selector-attempt/status.json"),
    "64_candidate_invariants": Path("runs/20260531-111219-binding-invariant-domain-selector-attempt/results/candidate_invariant_ledger.csv"),
    "64_equation_chain": Path("runs/20260531-111219-binding-invariant-domain-selector-attempt/results/invariant_equation_chain.csv"),
    "64_gates": Path("runs/20260531-111219-binding-invariant-domain-selector-attempt/results/gate_results.csv"),
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


def phase_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "linear_relaxation_to_Ccoh",
            "potential": "U(chi,C)=m_chi^2/2 (chi-C)^2",
            "euler_equation": "kappa_chi D^2 chi - m_chi^2(chi-C_coh)=0",
            "threshold": "none",
            "local_result": "C_coh=0 -> homogeneous chi=0",
            "FLRW_result": "C_coh=1 -> homogeneous chi=1",
            "verdict": "best_minimal_candidate",
        },
        {
            "candidate": "double_well_with_C_threshold",
            "potential": "U=lambda chi^2(1-chi)^2/4 - mu(C-C_star)chi",
            "euler_equation": "domain phase selected by C relative to C_star",
            "threshold": "C_star",
            "local_result": "can force local inactive phase",
            "FLRW_result": "can force FLRW active phase",
            "verdict": "rejected_or_deferred_threshold_risk",
        },
        {
            "candidate": "hard_step_selector",
            "potential": "chi=Heaviside(C-C_star)",
            "euler_equation": "none/singular",
            "threshold": "C_star",
            "local_result": "passes by cut",
            "FLRW_result": "passes by cut",
            "verdict": "rejected_empirical_switch",
        },
        {
            "candidate": "signed_relaxation_to_Cexp",
            "potential": "U=m_chi^2/2 (chi-C_exp)^2 with projection to allowed range",
            "euler_equation": "kappa_chi D^2 chi - m_chi^2(chi-C_exp)=0",
            "threshold": "none but needs collapse rule",
            "local_result": "stationary chi=0; collapse can become signed-active",
            "FLRW_result": "expanding FLRW chi=1",
            "verdict": "dynamic_extension_not_local_baseline",
        },
    ]


def homogeneous_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "quiet_Minkowski",
            "C_value": "0",
            "equation_reduction": "m_chi^2 chi = 0",
            "chi_solution": "chi=0",
            "memory_result": "inactive scalar volume-memory channel",
            "status": "pass_conditional",
        },
        {
            "branch": "stationary_bound_local",
            "C_value": "low or 0 after allowed averaging",
            "equation_reduction": "chi approximately C_coh",
            "chi_solution": "chi low",
            "memory_result": "local scalar volume-memory suppressed",
            "status": "pass_conditional",
        },
        {
            "branch": "tracefree_shear",
            "C_value": "0",
            "equation_reduction": "chi=0",
            "chi_solution": "chi=0",
            "memory_result": "shear does not activate scalar volume-memory",
            "status": "pass",
        },
        {
            "branch": "FLRW_background",
            "C_value": "1",
            "equation_reduction": "m_chi^2(chi-1)=0",
            "chi_solution": "chi=1",
            "memory_result": "coherent expansion remains active",
            "status": "pass_kinematic",
        },
        {
            "branch": "collapse_merger",
            "C_value": "mixed or signed",
            "equation_reduction": "depends on C_exp and gradients",
            "chi_solution": "dynamic",
            "memory_result": "open active branch",
            "status": "open",
        },
    ]


def variation_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "statement": "S_chi = integral sqrt(-g)[-kappa_chi/2 h^munu nabla_mu chi nabla_nu chi - m_chi^2/2(chi-C_coh)^2]",
            "status": "candidate_action",
            "meaning": "chi_D is a relaxed domain/coherence field sourced by coherent expansion purity",
            "gap": "C_coh depends on domain averaging and observer congruence",
        },
        {
            "step": 2,
            "statement": "delta S/delta chi -> kappa_chi D^2 chi - m_chi^2(chi-C_coh)=0",
            "status": "variation_success",
            "meaning": "the field equation is explicit and not just a multiplier restatement",
            "gap": "stress/conservation and C_coh variation are not included",
        },
        {
            "step": 3,
            "statement": "homogeneous limit -> chi=C_coh",
            "status": "branch_selector",
            "meaning": "local low-C domains and FLRW high-C domains separate without a threshold",
            "gap": "diffuse chi is not yet a sharp relative boundary class",
        },
        {
            "step": 4,
            "statement": "transition width ell_chi=sqrt(kappa_chi)/m_chi",
            "status": "new_parameter",
            "meaning": "the boundary thickness is universal if kappa_chi and m_chi are universal",
            "gap": "ell_chi is not parent-derived and risks becoming a smoothing scale",
        },
        {
            "step": 5,
            "statement": "T_chi_munu must be included in conservation/Bianchi gate",
            "status": "required_next_gate",
            "meaning": "a real field has stress; it cannot be added for free",
            "gap": "local GR safety needs stress suppression or cancellation",
        },
    ]


def parameter_risk_rows() -> list[dict[str, Any]]:
    return [
        {
            "parameter": "m_chi",
            "role": "sets relaxation stiffness toward C_coh",
            "allowed_status": "universal_or_parent_derived",
            "risk": "if fitted per system, it becomes a hidden window knob",
        },
        {
            "parameter": "kappa_chi",
            "role": "sets spatial/domain gradient cost",
            "allowed_status": "universal_or_parent_derived",
            "risk": "controls smoothing width",
        },
        {
            "parameter": "ell_chi=sqrt(kappa_chi)/m_chi",
            "role": "diffuse boundary thickness",
            "allowed_status": "must be checked against local tests and cosmology",
            "risk": "new length scale may reintroduce MOND-like phenomenology if not derived",
        },
        {
            "parameter": "eps_D",
            "role": "regularizes C_coh quiet limit",
            "allowed_status": "limiting prescription preferred over fitted constant",
            "risk": "can become a threshold if not fixed",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "explicit_variation_obtained",
            "status": "pass",
            "detail": "linear relaxation action gives kappa D^2 chi - m^2(chi-C_coh)=0",
        },
        {
            "gate": "threshold_avoided",
            "status": "pass",
            "detail": "best candidate uses chi=C_coh in homogeneous limit, not C>C_star",
        },
        {
            "gate": "local_FLRW_branch_split",
            "status": "pass_kinematic",
            "detail": "low-C local stationary domains map to low chi; FLRW C=1 maps to chi=1",
        },
        {
            "gate": "binding_domain_fully_derived",
            "status": "fail",
            "detail": "C_coh remains a coherent-expansion classifier, not a full binding derivation",
        },
        {
            "gate": "new_scale_removed",
            "status": "fail",
            "detail": "ell_chi appears and is not parent-derived",
        },
        {
            "gate": "Bianchi_stress_checked",
            "status": "open",
            "detail": "chi field stress and variation of C_coh must be checked before local GR promotion",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "this is a promising construction test, not evidence",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "Ccoh_phase_field_status",
            "status": "explicit_selector_equation_found_but_new_scale_and_stress_open",
            "evidence": "threshold-free chi=C_coh relaxation separates homogeneous local/FLRW branches but introduces ell_chi and untested stress",
            "next_action": "run Bianchi/stress and local-amplitude gate for chi field",
        },
        {
            "decision": "local_transition_route_status",
            "status": "improved_but_not_promoted",
            "evidence": "the selector is no longer pure handwave, but still needs scale derivation and stress suppression",
            "next_action": "derive or bound T_chi and ell_chi",
        },
        {
            "decision": "recommended_next_target",
            "status": "66-chiD-stress-and-scale-gate.md",
            "evidence": "the new field equation introduces stress and a transition length that could break local GR",
            "next_action": "calculate whether chi gradients/source stress can be locally negligible and cosmologically useful",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "explicit_selector_equation_found_but_new_scale_and_stress_open",
        "key_metrics": {
            "phase_action_candidates": counts["phase_action_candidates"],
            "homogeneous_branches": counts["homogeneous_branch_tests"],
            "variation_steps": counts["variation_chain"],
            "parameter_risks": counts["parameter_risk_register"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
        },
        "decision": decision_rows()[0],
        "next_target": "66-chiD-stress-and-scale-gate.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-Ccoh-phase-field-selector-attempt"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "phase_action_candidates": (
            phase_action_rows(),
            ["candidate", "potential", "euler_equation", "threshold", "local_result", "FLRW_result", "verdict"],
        ),
        "homogeneous_branch_tests": (
            homogeneous_branch_rows(),
            ["branch", "C_value", "equation_reduction", "chi_solution", "memory_result", "status"],
        ),
        "variation_chain": (
            variation_chain_rows(),
            ["step", "statement", "status", "meaning", "gap"],
        ),
        "parameter_risk_register": (
            parameter_risk_rows(),
            ["parameter", "role", "allowed_status", "risk"],
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
