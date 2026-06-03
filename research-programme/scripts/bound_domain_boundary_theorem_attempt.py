#!/usr/bin/env python3
"""Attempt the bound-domain boundary theorem for the post-checkpoint MTS branch."""

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
    "15_local_observables_doc": Path("15-local-observables-data-map.md"),
    "53_projection_doc": Path("53-coherent-projection-local-silence-gate.md"),
    "60_relative_boundary_doc": Path("60-relative-cohomology-boundary-contract.md"),
    "60_status": Path("runs/20260531-105710-relative-cohomology-boundary-contract/status.json"),
    "60_boundary_contract": Path("runs/20260531-105710-relative-cohomology-boundary-contract/results/boundary_rule_contract.csv"),
    "60_split_tests": Path("runs/20260531-105710-relative-cohomology-boundary-contract/results/local_FLRW_split_tests.csv"),
    "60_gates": Path("runs/20260531-105710-relative-cohomology-boundary-contract/results/gate_results.csv"),
}


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


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


def boundary_theorem_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "claim": "domain_volume",
            "equation": "V_D(tau)=integral_D dSigma",
            "status": "kinematic_identity",
            "meaning": "the candidate local/coherent domain is tracked by its proper spatial volume",
            "derivation_gap": "the parent action still has not selected D",
        },
        {
            "step": 2,
            "claim": "boundary_flux_identity",
            "equation": "dV_D/dtau = integral_boundary(D) v_n dA = integral_D theta dSigma",
            "status": "kinematic_identity",
            "meaning": "net coherent expansion is the boundary-normal volume flux",
            "derivation_gap": "requires a clean covariant foliation/domain-current statement",
        },
        {
            "step": 3,
            "claim": "domain_mean_expansion",
            "equation": "<theta>_D = (1/V_D)dV_D/dtau = d ln V_D/dtau",
            "status": "kinematic_identity",
            "meaning": "the coherent scalar channel is volume flow, not local shear",
            "derivation_gap": "does not by itself prove that only this channel enters the memory action",
        },
        {
            "step": 4,
            "claim": "stationary_bound_boundary_zero",
            "equation": "dV_D/dtau=0 -> <theta>_D=0 -> P_coh[Theta]=0 -> Q_coh=0",
            "status": "partial_theorem_if_boundary_selected",
            "meaning": "a stationary/virialized bound domain is locally silent in the volume-memory channel",
            "derivation_gap": "bound boundary selection and virial averaging are not parent-derived",
        },
        {
            "step": 5,
            "claim": "FLRW_boundary_active",
            "equation": "V_D proportional a^3 -> <theta>_D=3H -> Q_coh^i_j=(N/u3)delta^i_j",
            "status": "pass_conditional",
            "meaning": "the same rule keeps homogeneous cosmological memory active",
            "derivation_gap": "normalization u3=1/4 and determinant activation remain separate obligations",
        },
        {
            "step": 6,
            "claim": "relative_class_split",
            "equation": "zero boundary flux -> trivial local class; coherent expansion flux -> nontrivial FLRW class",
            "status": "contract_sharpened",
            "meaning": "local silence is tied to boundary flux rather than PPN rescue tuning",
            "derivation_gap": "still needs a parent domain/boundary field or variational condition",
        },
    ]


def domain_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "volume_extremal_boundary",
            "definition": "select boundary surfaces extremizing coherent volume flow, delta(d ln V_D/dtau)=0, with stationary branch dV_D/dtau=0",
            "status": "best_conditional_route",
            "noncircularity": "defined by flux/extremality before PPN residuals",
            "local_result": "stationary bound systems have Q_coh=0 in the volume-memory channel",
            "FLRW_result": "homogeneous expansion remains active because d ln V_D/dtau=3H",
            "failure_mode": "extremal boundary condition is not yet varied from a parent action",
        },
        {
            "candidate": "turnaround_zero_expansion_surface",
            "definition": "use the surface where coherent expansion switches from unbound expansion to bound stationarity",
            "status": "plausible_but_import_risk",
            "noncircularity": "physically motivated by expansion flow rather than observations",
            "local_result": "can define isolated bound domains",
            "FLRW_result": "does not silence the background",
            "failure_mode": "may import Newtonian/GR spherical-collapse logic unless rederived inside MTS",
        },
        {
            "candidate": "virial_time_averaged_boundary",
            "definition": "time-averaged bound volume obeys <d ln V_D/dtau>_T=0",
            "status": "conditional",
            "noncircularity": "uses internal motion averaging, not fitted PPN residuals",
            "local_result": "orbital/shear motion does not activate volume memory",
            "FLRW_result": "global expansion is not time-averaged away",
            "failure_mode": "virial theorem or averaging theorem has not been derived from parent equations",
        },
        {
            "candidate": "arbitrary_silencing_boundary",
            "definition": "choose D separately for each local system to make Q_coh vanish",
            "status": "rejected",
            "noncircularity": "fails",
            "local_result": "can always silence local tests by construction",
            "FLRW_result": "can be tuned to keep cosmology",
            "failure_mode": "pure closure rescue knob",
        },
        {
            "candidate": "pointwise_no_boundary",
            "definition": "try to silence local systems without a domain or boundary rule",
            "status": "rejected_insufficient",
            "noncircularity": "underdefined",
            "local_result": "cannot distinguish local shear/collapse from coherent expansion safely",
            "FLRW_result": "may preserve background but loses local safety",
            "failure_mode": "no object exists to carry the relative class",
        },
    ]


def local_system_boundary_rows() -> list[dict[str, Any]]:
    return [
        {
            "system": "Minkowski_patch",
            "volume_flux_condition": "dV_D/dtau=0 exactly",
            "memory_channel": "Q_coh=0",
            "relative_class": "trivial",
            "status": "pass",
            "remaining_gap": "control case only",
        },
        {
            "system": "stationary_solar_system",
            "volume_flux_condition": "stationary bound domain has no net coherent boundary flux",
            "memory_channel": "Q_coh=0 if parent selects the bound boundary",
            "relative_class": "trivial conditional",
            "status": "pass_conditional",
            "remaining_gap": "derive bound-domain criterion without importing GR/PPN",
        },
        {
            "system": "virialized_galaxy",
            "volume_flux_condition": "time-averaged physical domain volume stable despite internal orbital flow",
            "memory_channel": "local volume-memory channel silent; galaxy empirical sector must remain separately mapped",
            "relative_class": "trivial for local channel conditional",
            "status": "pass_conditional",
            "remaining_gap": "avoid accidentally erasing the intended galaxy pillar",
        },
        {
            "system": "tracefree_shear",
            "volume_flux_condition": "theta trace averages to zero while shear sigma_ij may be nonzero",
            "memory_channel": "volume-memory channel silent",
            "relative_class": "trivial for scalar volume class",
            "status": "pass_conditional",
            "remaining_gap": "separate shear/radiative sector still open",
        },
        {
            "system": "collapse_or_merger",
            "volume_flux_condition": "dynamic local boundary has nonzero coherent volume flux",
            "memory_channel": "possibly active",
            "relative_class": "not generally trivial",
            "status": "open_active",
            "remaining_gap": "needs strong-field/dynamical boundary equations",
        },
        {
            "system": "FLRW_background",
            "volume_flux_condition": "d ln V_D/dtau=3H on any coherent comoving domain",
            "memory_channel": "Q_coh^i_j=(N/u3)delta^i_j",
            "relative_class": "nontrivial expansion class",
            "status": "pass_conditional",
            "remaining_gap": "u3, p=3, and amplitude still require parent selection",
        },
    ]


def noncircularity_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "boundary_defined_by_volume_flux_not_PPN_residual",
            "status": "pass_partial",
            "evidence": "the rule uses dV_D/dtau or d ln V_D/dtau before local-observable fitting",
            "failure_mode": "if the boundary is later adjusted per failed local test, the pass is lost",
        },
        {
            "test": "bound_criterion_parent_derived",
            "status": "fail",
            "evidence": "no action, constraint, or domain field currently selects bound/unbound domains",
            "failure_mode": "local silence remains a closure assumption",
        },
        {
            "test": "virial_average_parent_derived",
            "status": "fail_open",
            "evidence": "time-averaged volume stability is plausible but imported until an MTS virial/averaging theorem exists",
            "failure_mode": "local orbital systems may not be safely silent in the parent theory",
        },
        {
            "test": "FLRW_preserved",
            "status": "pass",
            "evidence": "homogeneous domains have V_D proportional a^3 and retain <theta>_D=3H",
            "failure_mode": "none at background kinematic level",
        },
        {
            "test": "no_arbitrary_smoothing_scale",
            "status": "pass_partial",
            "evidence": "the best route uses a boundary/extremum condition rather than a hand-set smoothing length",
            "failure_mode": "scale/domain still becomes arbitrary unless chi_D or a boundary current is derived",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "volume_flux_boundary_contract_written",
            "status": "pass",
            "detail": "local/FLRW split can be expressed through boundary volume flux",
        },
        {
            "gate": "local_zero_boundary_nonarbitrary",
            "status": "pass_conditional",
            "detail": "local zero follows from dV_D/dtau=0 if the bound boundary is selected by parent equations",
        },
        {
            "gate": "FLRW_nonzero_boundary_preserved",
            "status": "pass",
            "detail": "FLRW has d ln V_D/dtau=3H and remains an active memory class",
        },
        {
            "gate": "bound_domain_parent_variation_derived",
            "status": "fail",
            "detail": "no parent variational principle has selected the bound-domain boundary",
        },
        {
            "gate": "virial_average_parent_derived",
            "status": "fail",
            "detail": "virial/time-averaged silence is plausible but imported, not derived",
        },
        {
            "gate": "dynamic_systems_resolved",
            "status": "open",
            "detail": "collapse, mergers, and strong-field boundaries may activate the memory channel",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "detail": "this is a partial kinematic theorem/contract, not evidence for the branch",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "bound_domain_boundary_status",
            "status": "partial_volume_extremum_theorem_not_parent_action",
            "evidence": "volume flux identities give a non-arbitrary local-zero/FLRW-active split if D is parent-selected",
            "next_action": "derive the domain selector or boundary field action",
        },
        {
            "decision": "topological_owner_status",
            "status": "still_live_pending_domain_action",
            "evidence": "relative class split has a sharper boundary object but not a parent selection rule",
            "next_action": "write chi_D/boundary-current contract and variation gates",
        },
        {
            "decision": "recommended_next_target",
            "status": "62-domain-field-chiD-action-contract.md",
            "evidence": "checkpoint 61 shows the theorem is kinematic unless an action selects D",
            "next_action": "introduce exact contract for a domain selector/window field chi_D",
        },
    ]


def status_payload(run_dir: Path, counts: dict[str, int]) -> dict[str, Any]:
    gates = gate_rows()
    return {
        "script": str(Path(__file__).resolve()),
        "run_dir": str(run_dir),
        "timestamp": run_dir.name.removeprefix("run-"),
        "readout": "bound_domain_boundary_theorem_partial_volume_extremum_not_parent_action",
        "key_metrics": {
            "boundary_theorem_steps": counts["boundary_theorem_chain"],
            "domain_candidates": counts["domain_candidate_tests"],
            "local_system_tests": counts["local_system_boundary_tests"],
            "noncircularity_tests": counts["noncircularity_tests"],
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "decision": decision_rows()[0],
        "next_target": "62-domain-field-chiD-action-contract.md",
    }


def run(output_root: Path) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = output_root / f"{timestamp}-bound-domain-boundary-theorem-attempt"
    result_dir = run_dir / "results"

    tables: dict[str, tuple[list[dict[str, Any]], list[str]]] = {
        "source_checkpoint_register": (
            source_register_rows(),
            ["source_key", "relative_path", "absolute_path", "exists"],
        ),
        "boundary_theorem_chain": (
            boundary_theorem_chain_rows(),
            ["step", "claim", "equation", "status", "meaning", "derivation_gap"],
        ),
        "domain_candidate_tests": (
            domain_candidate_rows(),
            ["candidate", "definition", "status", "noncircularity", "local_result", "FLRW_result", "failure_mode"],
        ),
        "local_system_boundary_tests": (
            local_system_boundary_rows(),
            ["system", "volume_flux_condition", "memory_channel", "relative_class", "status", "remaining_gap"],
        ),
        "noncircularity_tests": (
            noncircularity_rows(),
            ["test", "status", "evidence", "failure_mode"],
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
