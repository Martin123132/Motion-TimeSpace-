#!/usr/bin/env python3
"""Attempt a non-circular origin for the FLRW load tensor Q^i_j."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


POST_CHECKPOINT = Path(__file__).resolve().parents[1]

SOURCE_PATHS = {
    "10_observer_map_doc": Path("10-observer-map-symplectic-contract.md"),
    "21_cosmology_bridge_doc": Path("21-cosmology-parent-bridge-audit.md"),
    "50_parent_activation_doc": Path("50-parent-activation-law-attempt.md"),
    "51_memory_current_doc": Path("51-FLRW-memory-current-contract.md"),
    "51_status": Path("runs/20260531-033502-FLRW-memory-current-contract/status.json"),
    "51_variable_contract": Path(
        "runs/20260531-033502-FLRW-memory-current-contract/results/memory_current_variable_contract.csv"
    ),
    "51_equation_contract": Path(
        "runs/20260531-033502-FLRW-memory-current-contract/results/memory_current_equation_contract.csv"
    ),
    "51_gates": Path("runs/20260531-033502-FLRW-memory-current-contract/results/gate_results.csv"),
}


def absolute_source(key: str) -> Path:
    return POST_CHECKPOINT / SOURCE_PATHS[key]


def load_json(key: str) -> dict[str, Any]:
    return json.loads(absolute_source(key).read_text(encoding="utf-8"))


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


def origin_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "accumulated_spatial_expansion_tensor",
            "definition": "Q^i_j=(1/u3) integral_t^t0 Theta^i_j dtau, with Theta^i_j=h^{i alpha} h_{j beta} nabla_alpha u^beta",
            "status": "best_partial_kinematic_origin",
            "FLRW_result": "Theta^i_j=H delta^i_j, so Q^i_j=N/u3 delta^i_j",
            "local_result": "stationary local congruence has Theta^i_j=0, so Q=0",
            "failure_or_gap": "u3, parent congruence, coarse-graining, and action origin remain missing",
        },
        {
            "candidate": "spatial_log_metric_strain",
            "definition": "Q^i_j=-(1/(2u3)) log[(h0^{-1}h)^i_j] with branch/reference chosen toward today",
            "status": "equivalent_FLRW_but_reference_dependent",
            "FLRW_result": "h_ij=a^2 delta_ij gives Q^i_j=N/u3 delta^i_j",
            "local_result": "static spatial metric strain may not vanish without subtracting stationary bound geometry",
            "failure_or_gap": "risks importing local metric load/hair unless a stationary reference rule is derived",
        },
        {
            "candidate": "coherent_isotropic_projection_of_expansion",
            "definition": "Q_cg=P_coh[(1/u3) integral Theta^i_j dtau], keeping only coherent isotropic expansion load",
            "status": "promising_but_projector_not_derived",
            "FLRW_result": "projection is identity on FLRW and gives Q=N/u3 delta",
            "local_result": "virialized/local anisotropic motion averages away if P_coh is legitimate",
            "failure_or_gap": "P_coh cannot be inserted as a rescue knob; parent theory must define it",
        },
        {
            "candidate": "full_deformation_gradient_determinant",
            "definition": "Q from full local deformation/shear gradient and I_M=det(Q)",
            "status": "rejected_or_high_risk",
            "FLRW_result": "can reproduce cubic law",
            "local_result": "anisotropic shear/collapse may create local memory hair",
            "failure_or_gap": "fails local silence unless projected/screened by a derived mechanism",
        },
        {
            "candidate": "pure_cubic_definition",
            "definition": "define Q only by requiring det(Q)=(N/u3)^3",
            "status": "rejected_circular",
            "FLRW_result": "trivially works",
            "local_result": "no predictive local content",
            "failure_or_gap": "invented after seeing the desired law",
        },
    ]


def flrw_reduction_rows(status_51: dict[str, Any]) -> list[dict[str, Any]]:
    metrics = status_51["key_metrics"]
    u3 = metrics["u3"]
    return [
        {
            "step": 1,
            "equation": "Theta^i_j = h^{i alpha} h_{j beta} nabla_alpha u^beta",
            "status": "standard_geometric_definition",
            "meaning": "spatial expansion/deformation tensor of the chosen parent time-flow congruence",
            "gap": "parent theory must choose u^mu without circular FLRW fitting",
        },
        {
            "step": 2,
            "equation": "Q^i_j=(1/u3) integral_t^t0 Theta^i_j dtau",
            "status": "candidate_definition_before_FLRW_symmetry",
            "meaning": "dimensionless accumulated motion/space load tensor",
            "gap": "u3 and integration/reference rule are not parent-predicted",
        },
        {
            "step": 3,
            "equation": "FLRW: Theta^i_j=H delta^i_j",
            "status": "pass",
            "meaning": "homogeneous isotropic expansion has three equal spatial load eigen-directions",
            "gap": "none for FLRW kinematics",
        },
        {
            "step": 4,
            "equation": "integral_t^t0 H dt = ln(a0/a)=N",
            "status": "pass_if_a0_equals_1",
            "meaning": "lookback e-fold load emerges from accumulated expansion",
            "gap": "normalization by u3 remains unexplained",
        },
        {
            "step": 5,
            "equation": f"Q^i_j=(N/u3) delta^i_j, u3={u3}",
            "status": "partial_derivation",
            "meaning": "the checkpoint-51 target X_FLRW=N/u3 follows from accumulated expansion load",
            "gap": "u3 still closure-level",
        },
        {
            "step": 6,
            "equation": "I_M=det(Q)=(N/u3)^3",
            "status": "conditional_pass",
            "meaning": "the cubic exposure follows from three equal accumulated expansion eigenvalues",
            "gap": "determinant/current must be action-owned",
        },
        {
            "step": 7,
            "equation": "J_M=dI_M/dN=3N^2/u3^3",
            "status": "conditional_pass",
            "meaning": "the required double-zero memory current follows",
            "gap": "conservation and perturbation response remain missing",
        },
    ]


def local_silence_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "Minkowski_local_inertial",
            "Theta_condition": "Theta^i_j=0",
            "Q_result": "Q=0",
            "memory_result": "I_M=0 and J_M=0",
            "status": "pass",
            "remaining_issue": "trivial flat-space check only",
        },
        {
            "arena": "stationary_static_exterior",
            "Theta_condition": "chosen stationary observer congruence has no coherent volume expansion",
            "Q_result": "Q approximately 0 for expansion-load definition",
            "memory_result": "no FLRW-style memory activation",
            "status": "pass_conditional",
            "remaining_issue": "must not import Schwarzschild/GR as the reason the congruence is stationary",
        },
        {
            "arena": "virialized_bound_system",
            "Theta_condition": "coarse-grained expansion averages to zero despite internal motion",
            "Q_result": "coherent Q approximately 0 if P_coh exists",
            "memory_result": "local PPN hair suppressed",
            "status": "open_requires_projector",
            "remaining_issue": "coherent projection/screening must be derived, not fitted",
        },
        {
            "arena": "anisotropic_shear_or_collapse",
            "Theta_condition": "tracefree or anisotropic components may be nonzero",
            "Q_result": "full det(Q) can be nonzero",
            "memory_result": "possible local/dynamical hair",
            "status": "fail_for_full_unprojected_Q",
            "remaining_issue": "must restrict to coherent isotropic expansion or define stress response",
        },
        {
            "arena": "gravitational_waves_or_time_dependent_local_fields",
            "Theta_condition": "transient shear/strain can exist",
            "Q_result": "not controlled by current contract",
            "memory_result": "unknown",
            "status": "open",
            "remaining_issue": "needs perturbation and radiation-sector treatment",
        },
        {
            "arena": "FLRW_perturbations",
            "Theta_condition": "Theta splits into background expansion plus perturbations",
            "Q_result": "background gives Q=N/u3, perturbations need response law",
            "memory_result": "background activation only is insufficient for CMB/lensing",
            "status": "open",
            "remaining_issue": "derive sound speed, anisotropic stress, metric potentials, and lensing",
        },
    ]


def parent_gap_rows() -> list[dict[str, Any]]:
    return [
        {
            "gap": "parent_time_flow_congruence",
            "status": "missing",
            "why_it_matters": "Theta^i_j depends on the chosen u^mu; the parent theory must define the physical time-flow",
            "next_action": "derive u^mu or clock-flow from MTS variables",
        },
        {
            "gap": "transition_scale_u3",
            "status": "missing",
            "why_it_matters": "Q normalization still uses fitted/borrowed u3",
            "next_action": "derive u3 from cell scale, threshold, coupling, or boundary condition",
        },
        {
            "gap": "coherent_projection_Pcoh",
            "status": "missing",
            "why_it_matters": "without it, anisotropic local shear may produce memory hair",
            "next_action": "derive a projector/screening rule or reject local-safe route",
        },
        {
            "gap": "determinant_action_owner",
            "status": "missing",
            "why_it_matters": "I_M=det(Q) is kinematically natural but not variationally owned",
            "next_action": "write action/constraint/current that uses det(Q) or its 3-form equivalent",
        },
        {
            "gap": "b_mem_amplitude",
            "status": "missing",
            "why_it_matters": "activation shape is not the amplitude of cosmological stress",
            "next_action": "derive memory stress scale after current owner is defined",
        },
        {
            "gap": "Bianchi_conservation",
            "status": "missing",
            "why_it_matters": "background activation must be compatible with covariant conservation",
            "next_action": "assign memory to fluid exchange or modified geometric side",
        },
        {
            "gap": "perturbation_lensing_response",
            "status": "missing",
            "why_it_matters": "official CMB support remains impossible without perturbations",
            "next_action": "derive perturbation equations after Q owner/projection is locked",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "Q_defined_before_FLRW_symmetry",
            "status": "pass_partial",
            "reason": "Q can be defined as normalized accumulated spatial expansion tensor before imposing FLRW",
            "allowed_claim": "kinematic load-tensor origin exists",
        },
        {
            "gate": "FLRW_reduces_to_X_equals_N_over_u3",
            "status": "pass_partial",
            "reason": "integral H dt from emission time to today gives N, so Q=N/u3 delta in FLRW",
            "allowed_claim": "X=N/u3 is kinematically derived up to u3",
        },
        {
            "gate": "cubic_exposure_from_determinant",
            "status": "pass_conditional",
            "reason": "det(Q) gives (N/u3)^3 for FLRW isotropic load",
            "allowed_claim": "p=3 follows from a 3D load-volume invariant if det(Q) is action-owned",
        },
        {
            "gate": "stationary_local_silence",
            "status": "pass_conditional",
            "reason": "stationary non-expanding local congruences give Q=0",
            "allowed_claim": "local silence is plausible for stationary systems",
        },
        {
            "gate": "anisotropic_dynamic_local_safety",
            "status": "fail_open",
            "reason": "full unprojected Q can respond to shear/collapse and may create local hair",
            "allowed_claim": "needs coherent projection or screening",
        },
        {
            "gate": "u3_parent_predicted",
            "status": "fail",
            "reason": "u3 remains inherited from the C2 closure",
            "allowed_claim": "transition scale still not derived",
        },
        {
            "gate": "parent_action_derived",
            "status": "fail",
            "reason": "no action/current/conservation equation yet owns Q or det(Q)",
            "allowed_claim": "kinematic origin, not parent field theory",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "reason": "local dynamic safety, amplitude, conservation, and perturbations are missing",
            "allowed_claim": "private derivation branch only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "load_tensor_origin_attempt",
            "status": "partial_kinematic_origin_not_parent_action",
            "best_route": "Q^i_j=(1/u3) integral_t^t0 Theta^i_j dtau",
            "what_was_earned": "Q is no longer just invented after the cubic law; FLRW gives X=N/u3 from accumulated expansion",
            "what_failed": "u3, coherent projection, action owner, conservation, amplitude, and perturbations remain missing",
            "next_target": "53-coherent-projection-local-silence-gate.md",
        },
        {
            "decision": "local_GR_relevance",
            "status": "promising_but_not_safe",
            "best_route": "stationary expansion-load silence",
            "what_was_earned": "stationary local systems can have Q=0 without forcing cosmology Q=0",
            "what_failed": "dynamic anisotropic local sources can still create hair unless projection/screening is derived",
            "next_target": "derive or reject P_coh/screening for local systems",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Load tensor origin attempt.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    status_51 = load_json("51_status")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-load-tensor-origin-attempt"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    candidates = origin_candidate_rows()
    flrw = flrw_reduction_rows(status_51)
    local = local_silence_rows()
    gaps = parent_gap_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "load_tensor_origin_candidates.csv", candidates, list(candidates[0].keys()))
    write_csv(results_dir / "FLRW_reduction_chain.csv", flrw, list(flrw[0].keys()))
    write_csv(results_dir / "local_silence_tests.csv", local, list(local[0].keys()))
    write_csv(results_dir / "parent_gap_register.csv", gaps, list(gaps[0].keys()))
    write_csv(results_dir / "gate_results.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    metrics = status_51["key_metrics"]
    status = {
        "status": "complete_load_tensor_origin_attempt",
        "readout": "load_tensor_has_partial_kinematic_origin_not_parent_action",
        "recommendation": "test_coherent_projection_local_silence_next",
        "next_target": "53-coherent-projection-local-silence-gate.md",
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "best_candidate": "Q^i_j=(1/u3) integral_t^t0 Theta^i_j dtau",
        "key_metrics": {
            "u3": metrics["u3"],
            "N50": metrics["N50"],
            "dX_dN": metrics["dX_dN"],
            "JM_quadratic_coefficient": metrics["JM_quadratic_coefficient"],
            "origin_candidates": len(candidates),
            "FLRW_reduction_steps": len(flrw),
            "local_silence_tests": len(local),
            "parent_gaps": len(gaps),
            "failed_or_open_gates": sum(1 for row in gates if row["status"] in {"fail", "fail_open"}),
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "load_tensor_origin_candidates": str(results_dir / "load_tensor_origin_candidates.csv"),
            "FLRW_reduction_chain": str(results_dir / "FLRW_reduction_chain.csv"),
            "local_silence_tests": str(results_dir / "local_silence_tests.csv"),
            "parent_gap_register": str(results_dir / "parent_gap_register.csv"),
            "gate_results": str(results_dir / "gate_results.csv"),
            "decision": str(results_dir / "decision.csv"),
            "status_json": str(out_dir / "status.json"),
        },
    }
    (out_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (out_dir / "log.txt").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    (out_dir / "DONE.txt").write_text(status["readout"] + "\n", encoding="utf-8")
    print(json.dumps(status, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
