#!/usr/bin/env python3
"""Audit C_coh variation and the boundary/exchange current needed for conservation."""

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
    "64_binding_invariant_doc": Path("64-binding-invariant-domain-selector-attempt.md"),
    "68_conservation_doc": Path("68-chiD-gated-memory-conservation-contract.md"),
    "69_memory_gate_doc": Path("69-minimal-memory-gate-variation-attempt.md"),
    "69_status": Path("runs/20260531-112824-minimal-memory-gate-variation-attempt/status.json"),
    "69_conservation_terms": Path("runs/20260531-112824-minimal-memory-gate-variation-attempt/results/conservation_terms.csv"),
    "69_gates": Path("runs/20260531-112824-minimal-memory-gate-variation-attempt/results/gate_results.csv"),
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


def variation_dependency_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "C_coh",
            "definition": "<theta>_D^2/(<theta^2>_D+<sigma^2>_D+<omega^2>_D+eps_D)",
            "varies_through": "theta, sigma, omega, h_ij, u^mu, domain average D, eps_D prescription",
            "local_risk": "many hidden metric/congruence/domain variations",
            "status": "variationally_heavy",
        },
        {
            "object": "<theta>_D",
            "definition": "(1/V_D) integral_D theta dSigma",
            "varies_through": "volume measure, boundary motion, congruence expansion, chi_D/domain support",
            "local_risk": "boundary term appears when D changes",
            "status": "boundary_current_source",
        },
        {
            "object": "<theta^2/sigma^2/omega^2>_D",
            "definition": "domain averages of local deformation invariants",
            "varies_through": "metric projectors, covariant derivatives of u, boundary support",
            "local_risk": "can create derivative stress if made dynamical in bulk",
            "status": "bulk_and_boundary_source",
        },
        {
            "object": "domain D",
            "definition": "support/projector selected by chi_D=C_coh or relative class",
            "varies_through": "selector constraint and boundary deformation",
            "local_risk": "local-to-FLRW boundary exchange current",
            "status": "main_open_object",
        },
        {
            "object": "eps_D",
            "definition": "quiet-limit regularizer",
            "varies_through": "limiting prescription or parent scale",
            "local_risk": "becomes hidden threshold if finite/fitted",
            "status": "must_be_fixed_or_limit",
        },
    ]


def boundary_current_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "bulk_variation_current",
            "form": "J_C^nu from integration by parts of delta(theta,sigma,omega)",
            "what_it_solves": "organizes C_coh derivative terms into Noether exchange",
            "local_behavior": "zero if C_coh constant in quiet bulk",
            "status": "needed_but_not_constructed",
            "risk": "higher-derivative stress/fifth-force terms",
        },
        {
            "candidate": "domain_boundary_current",
            "form": "J_boundary^nu proportional n^nu delta_DeltaD L_mem delta C_coh",
            "what_it_solves": "captures local-to-FLRW transition exchange",
            "local_behavior": "localized at coherence boundary",
            "status": "main_candidate",
            "risk": "PPN-sized surface stress unless topological/auxiliary",
        },
        {
            "candidate": "relative_topological_current",
            "form": "closed relative current dJ_rel=0 with trivial local class and nontrivial FLRW class",
            "what_it_solves": "makes exchange a class/boundary bookkeeping term rather than propagating stress",
            "local_behavior": "trivial class in bound stationary domains",
            "status": "best_long_term_route",
            "risk": "needs actual relative current construction",
        },
        {
            "candidate": "freeze_Ccoh",
            "form": "set delta C_coh=0 during metric variation",
            "what_it_solves": "removes hard terms",
            "local_behavior": "artificially safe",
            "status": "rejected",
            "risk": "fake Bianchi identity",
        },
    ]


def branch_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "quiet_local_bulk",
            "Ccoh_behavior": "constant zero",
            "delta_Ccoh": "zero if local parent solution fixes theta=sigma=omega quiet in scalar channel",
            "exchange_current": "none in bulk",
            "status": "pass_conditional",
            "gap": "prove parent local solution, not assumed",
        },
        {
            "branch": "stationary_bound_interior",
            "Ccoh_behavior": "low/constant after averaging",
            "delta_Ccoh": "small or zero under stationary volume-flow condition",
            "exchange_current": "none or small in interior",
            "status": "pass_conditional",
            "gap": "averaging/domain theorem still open",
        },
        {
            "branch": "FLRW_background",
            "Ccoh_behavior": "constant one by homogeneity",
            "delta_Ccoh": "zero for symmetry-preserving background variation, nonzero for perturbations",
            "exchange_current": "none in background",
            "status": "pass_background_only",
            "gap": "perturbation/lensing branch unresolved",
        },
        {
            "branch": "local_to_FLRW_boundary",
            "Ccoh_behavior": "varies from low to high",
            "delta_Ccoh": "nonzero",
            "exchange_current": "required",
            "status": "open_danger",
            "gap": "main local-GR obstruction",
        },
        {
            "branch": "collapse_merger_dynamic",
            "Ccoh_behavior": "time-dependent and inhomogeneous",
            "delta_Ccoh": "nonzero",
            "exchange_current": "dynamic",
            "status": "open",
            "gap": "strong-field sector",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "Ccoh_variation_dependencies_identified",
            "status": "pass",
            "detail": "theta/sigma/omega/domain/u/metric dependencies are explicit",
        },
        {
            "gate": "freezing_Ccoh_rejected",
            "status": "pass",
            "detail": "delta C_coh cannot be set to zero by hand",
        },
        {
            "gate": "quiet_bulk_safe",
            "status": "pass_conditional",
            "detail": "constant C_coh branches have no bulk exchange current",
        },
        {
            "gate": "FLRW_background_safe",
            "status": "pass_background_only",
            "detail": "homogeneous C_coh=1 background can avoid exchange current",
        },
        {
            "gate": "boundary_exchange_current_derived",
            "status": "fail",
            "detail": "no explicit conserved J_boundary or J_rel yet",
        },
        {
            "gate": "perturbation_conservation_resolved",
            "status": "open",
            "detail": "FLRW perturbations make delta C_coh nonzero",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "detail": "boundary current remains the obstruction",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "audit narrows the missing object; it is not evidence",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "Ccoh_variation_status",
            "status": "dependencies_identified_boundary_current_not_derived",
            "evidence": "C_coh can be constant-safe in ideal local/FLRW bulk branches, but varying boundaries and perturbations require an explicit exchange current",
            "next_action": "attempt relative topological boundary current construction",
        },
        {
            "decision": "local_GR_route_status",
            "status": "bulk_safe_boundary_current_bottleneck",
            "evidence": "quiet interiors remain plausible; local-to-FLRW boundary is the central unresolved source",
            "next_action": "derive or reject J_rel/J_boundary",
        },
        {
            "decision": "recommended_next_target",
            "status": "71-relative-boundary-current-construction-attempt.md",
            "evidence": "best remaining route is a closed relative boundary current with trivial local class and active FLRW class",
            "next_action": "construct J_rel and test closure/local/FLRW gates",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "dependencies_identified_boundary_current_not_derived",
        "key_metrics": {
            "variation_dependencies": counts["variation_dependencies"],
            "boundary_current_candidates": counts["boundary_current_candidates"],
            "branch_audits": counts["branch_audits"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "decision": decision_rows()[0],
        "next_target": "71-relative-boundary-current-construction-attempt.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-Ccoh-variation-and-boundary-current-audit"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "variation_dependencies": (
            variation_dependency_rows(),
            ["object", "definition", "varies_through", "local_risk", "status"],
        ),
        "boundary_current_candidates": (
            boundary_current_rows(),
            ["candidate", "form", "what_it_solves", "local_behavior", "status", "risk"],
        ),
        "branch_audits": (
            branch_audit_rows(),
            ["branch", "Ccoh_behavior", "delta_Ccoh", "exchange_current", "status", "gap"],
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
