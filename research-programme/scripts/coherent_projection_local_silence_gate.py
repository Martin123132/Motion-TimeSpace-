#!/usr/bin/env python3
"""Gate the coherent projection needed for local silence of the FLRW load tensor."""

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
    "51_memory_current_doc": Path("51-FLRW-memory-current-contract.md"),
    "52_load_tensor_doc": Path("52-load-tensor-origin-attempt.md"),
    "52_status": Path("runs/20260531-034248-load-tensor-origin-attempt/status.json"),
    "52_origin_candidates": Path("runs/20260531-034248-load-tensor-origin-attempt/results/load_tensor_origin_candidates.csv"),
    "52_local_silence_tests": Path("runs/20260531-034248-load-tensor-origin-attempt/results/local_silence_tests.csv"),
    "52_gates": Path("runs/20260531-034248-load-tensor-origin-attempt/results/gate_results.csv"),
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


def projection_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "domain_volume_expansion_projector",
            "definition": "P_coh[Theta]^i_j=(1/3)<theta>_D delta^i_j, with <theta>_D=d ln V_D/dtau",
            "status": "best_conditional_route",
            "FLRW_behavior": "<theta>_D=3H, so Q_coh=N/u3 delta",
            "local_behavior": "stationary or virialized bound domain has dV_D/dtau approximately 0, so Q_coh approximately 0",
            "non_circularity": "uses volume expansion before fitting p=3; does not reference det(Q) as the definition",
            "remaining_gap": "domain D and coarse-graining rule are not parent-derived",
        },
        {
            "candidate": "trace_only_isotropic_projection",
            "definition": "P_iso[Theta]^i_j=(1/3)theta delta^i_j pointwise",
            "status": "partial_but_too_local",
            "FLRW_behavior": "keeps the FLRW background expansion",
            "local_behavior": "kills pure shear but can react to local compression/expansion",
            "non_circularity": "kinematic decomposition is standard",
            "remaining_gap": "without domain averaging it may still create hair in local dynamical systems",
        },
        {
            "candidate": "virial_boundary_freeze",
            "definition": "bound systems with stable coarse-grained physical volume carry no coherent expansion memory",
            "status": "conditional_physical_rule",
            "FLRW_behavior": "does not suppress unbound homogeneous expansion",
            "local_behavior": "suppresses solar-system/galaxy-bound background leakage if parent defines bound domains",
            "non_circularity": "connects to volume stability, not observational rescue",
            "remaining_gap": "needs parent criterion for bound/non-bound domains",
        },
        {
            "candidate": "arbitrary_smoothing_filter",
            "definition": "choose a smoothing scale that removes local failures",
            "status": "rejected_circular",
            "FLRW_behavior": "can be tuned to keep FLRW",
            "local_behavior": "can be tuned to silence local systems",
            "non_circularity": "fails",
            "remaining_gap": "not allowed unless scale/rule is parent-predicted",
        },
        {
            "candidate": "no_projection_full_Q",
            "definition": "use full accumulated Theta^i_j in det(Q)",
            "status": "rejected_for_local_safety",
            "FLRW_behavior": "works for FLRW",
            "local_behavior": "anisotropic shear/collapse can create unwanted local memory",
            "non_circularity": "not circular but unsafe",
            "remaining_gap": "fails local silence gate",
        },
    ]


def equation_chain_rows(status_52: dict[str, Any]) -> list[dict[str, Any]]:
    u3 = status_52["key_metrics"]["u3"]
    return [
        {
            "step": 1,
            "equation": "Theta_ij = (1/3) theta h_ij + sigma_ij",
            "status": "kinematic_decomposition",
            "meaning": "separate coherent volume expansion theta from tracefree shear sigma",
            "gate_note": "memory determinant may use only the coherent volume part if parent justifies P_coh",
        },
        {
            "step": 2,
            "equation": "<theta>_D = (1/V_D) dV_D/dtau = d ln V_D/dtau",
            "status": "domain_volume_identity",
            "meaning": "domain-averaged expansion is physical volume growth rate",
            "gate_note": "this gives a non-fitted local silence criterion: no volume growth, no coherent load",
        },
        {
            "step": 3,
            "equation": "P_coh[Theta]^i_j = (1/3)<theta>_D delta^i_j",
            "status": "candidate_projection",
            "meaning": "keep only coherent isotropic expansion load",
            "gate_note": "projector is acceptable only if D is parent-defined",
        },
        {
            "step": 4,
            "equation": "Q_coh^i_j = (1/u3) integral_t^t0 P_coh[Theta]^i_j dtau",
            "status": "conditional_definition",
            "meaning": "coherent accumulated load tensor",
            "gate_note": f"u3={u3} remains underived",
        },
        {
            "step": 5,
            "equation": "FLRW: <theta>_D=3H -> Q_coh^i_j=(N/u3) delta^i_j",
            "status": "pass",
            "meaning": "FLRW activation route is preserved",
            "gate_note": "p=3 determinant route survives projection",
        },
        {
            "step": 6,
            "equation": "stationary_bound_domain: dV_D/dtau=0 -> Q_coh=0",
            "status": "pass_conditional",
            "meaning": "static/virialized local systems are silent if domain volume is stable",
            "gate_note": "requires parent-defined domain/bound criterion",
        },
        {
            "step": 7,
            "equation": "I_M=det(Q_coh), J_M=dI_M/dN",
            "status": "conditional_pass",
            "meaning": "same cubic memory current follows for coherent FLRW load",
            "gate_note": "action/conservation owner still missing",
        },
    ]


def local_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "system": "Minkowski_patch",
            "coherent_volume_condition": "dV_D/dtau=0",
            "Q_coh": "0",
            "PPN_risk": "none",
            "status": "pass",
            "remaining_gap": "none for flat control",
        },
        {
            "system": "stationary_solar_system_domain",
            "coherent_volume_condition": "stable bound volume; no coherent Hubble expansion inside domain",
            "Q_coh": "approximately 0",
            "PPN_risk": "suppressed if domain rule is real",
            "status": "pass_conditional",
            "remaining_gap": "derive bound-domain criterion without using PPN data",
        },
        {
            "system": "virialized_galaxy_domain",
            "coherent_volume_condition": "time-averaged volume stable despite internal orbital motion",
            "Q_coh": "approximately 0 for local-memory activation, while galaxy phenomenology can live in another sector",
            "PPN_risk": "low for local GR but must avoid erasing intended galaxy tests by accident",
            "status": "pass_conditional",
            "remaining_gap": "separate local PPN silence from galaxy empirical pillar cleanly",
        },
        {
            "system": "tracefree_shear",
            "coherent_volume_condition": "theta=0, sigma_ij nonzero",
            "Q_coh": "0 under trace-volume projection",
            "PPN_risk": "reduced",
            "status": "pass_conditional",
            "remaining_gap": "radiative/shear memory response still needs separate field equation",
        },
        {
            "system": "collapse_or_merger",
            "coherent_volume_condition": "dV_D/dtau nonzero and not FLRW-homogeneous",
            "Q_coh": "nonzero possible",
            "PPN_risk": "not a solar-system PPN baseline; could produce dynamical signatures",
            "status": "open_not_rejected",
            "remaining_gap": "needs dynamical strong-field/radiation-sector treatment",
        },
        {
            "system": "FLRW_perturbations",
            "coherent_volume_condition": "background plus perturbative theta fluctuations",
            "Q_coh": "background retained; perturbations unresolved",
            "PPN_risk": "CMB/lensing support not available yet",
            "status": "open",
            "remaining_gap": "derive perturbation closure after parent owner is defined",
        },
    ]


def circularity_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "projector_defined_before_failures",
            "status": "pass_partial",
            "evidence": "P_coh is defined by domain volume expansion d ln V_D/dtau, not by local PPN residuals",
            "failure_mode": "if D is later tuned per system, the projector becomes a rescue knob",
        },
        {
            "test": "FLRW_not_damaged",
            "status": "pass",
            "evidence": "for homogeneous expansion <theta>_D=3H and the old Q=N/u3 delta result is recovered",
            "failure_mode": "projection would fail if it erased the background expansion",
        },
        {
            "test": "shear_not_silenced_by_magic",
            "status": "pass_conditional",
            "evidence": "tracefree shear drops out because the candidate memory is volume-expansion memory",
            "failure_mode": "if the parent action couples memory to shear, this projection is incomplete",
        },
        {
            "test": "bound_domain_rule_parent_defined",
            "status": "fail_currently",
            "evidence": "no parent equation defines the coarse-graining domain D",
            "failure_mode": "choosing D to dodge solar-system tests is not allowed",
        },
        {
            "test": "u3_parent_predicted",
            "status": "fail",
            "evidence": "u3 remains inherited from the C2 closure",
            "failure_mode": "transition scale stays phenomenological",
        },
        {
            "test": "conservation_owner_defined",
            "status": "fail",
            "evidence": "no Bianchi-compatible memory stress/geometric owner is defined",
            "failure_mode": "background and perturbation equations remain closure-level",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate": "nonarbitrary_coherent_projection_identified",
            "status": "pass_partial",
            "reason": "domain volume expansion gives a defined scalar coherent load before FLRW symmetry",
            "allowed_claim": "a plausible non-fitted projector exists",
        },
        {
            "gate": "FLRW_activation_preserved",
            "status": "pass",
            "reason": "P_coh is identity on homogeneous isotropic expansion",
            "allowed_claim": "projection does not kill the cosmology branch",
        },
        {
            "gate": "stationary_local_silence",
            "status": "pass_conditional",
            "reason": "stable bound volume gives <theta>_D=0 and Q_coh=0",
            "allowed_claim": "stationary local PPN silence is plausible if bound domains are parent-defined",
        },
        {
            "gate": "anisotropic_tracefree_safety",
            "status": "pass_conditional",
            "reason": "tracefree shear is removed by volume-expansion projection",
            "allowed_claim": "pure shear does not source this scalar memory channel",
        },
        {
            "gate": "bound_domain_D_parent_defined",
            "status": "fail",
            "reason": "no non-fitted rule defines the averaging/coherence domain",
            "allowed_claim": "domain rule remains a required derivation",
        },
        {
            "gate": "dynamic_local_systems_safe",
            "status": "open",
            "reason": "collapse, mergers, waves, and perturbations may still source memory or other channels",
            "allowed_claim": "not covered by PPN silence gate",
        },
        {
            "gate": "u3_parent_predicted",
            "status": "fail",
            "reason": "normalization still uses closure value",
            "allowed_claim": "u3 not derived",
        },
        {
            "gate": "parent_action_or_conservation_owner",
            "status": "fail",
            "reason": "P_coh and det(Q_coh) are not yet owned by a variational or Bianchi-compatible law",
            "allowed_claim": "not parent field theory yet",
        },
        {
            "gate": "support_claim_allowed",
            "status": "fail",
            "reason": "local silence is conditional and perturbation/amplitude sectors remain missing",
            "allowed_claim": "private derivation branch only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": "coherent_projection_local_silence_gate",
            "status": "conditional_projector_retained_not_parent_derived",
            "best_route": "P_coh[Theta]^i_j=(1/3)<theta>_D delta^i_j",
            "what_was_earned": "FLRW expansion is preserved while stationary and virialized volume-stable local domains are plausibly silent",
            "what_failed": "domain D, u3, action owner, conservation, and perturbations remain underived",
            "next_target": "54-coherent-domain-and-u3-origin.md",
        },
        {
            "decision": "local_branch_risk",
            "status": "reduced_not_closed",
            "best_route": "volume-expansion memory instead of full shear/deformation memory",
            "what_was_earned": "the dangerous full-Q local hair route is rejected",
            "what_failed": "dynamic local systems and radiative channels are still open",
            "next_target": "derive the domain/coherence scale or demote projection to closure",
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description="Coherent projection local-silence gate.")
    parser.add_argument("--out-dir", type=Path, default=None)
    args = parser.parse_args()

    source_register = source_register_rows()
    status_52 = load_json("52_status")

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    out_dir = args.out_dir or POST_CHECKPOINT / "runs" / f"{timestamp}-coherent-projection-local-silence-gate"
    if not out_dir.is_absolute():
        out_dir = (Path.cwd() / out_dir).resolve()
    results_dir = out_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    candidates = projection_candidate_rows()
    equations = equation_chain_rows(status_52)
    local = local_gate_rows()
    circularity = circularity_rows()
    gates = gate_rows()
    decisions = decision_rows()

    write_csv(results_dir / "source_checkpoint_register.csv", source_register, list(source_register[0].keys()))
    write_csv(results_dir / "projection_candidate_ledger.csv", candidates, list(candidates[0].keys()))
    write_csv(results_dir / "coherent_projection_equation_chain.csv", equations, list(equations[0].keys()))
    write_csv(results_dir / "local_silence_gate_tests.csv", local, list(local[0].keys()))
    write_csv(results_dir / "circularity_tests.csv", circularity, list(circularity[0].keys()))
    write_csv(results_dir / "gate_results.csv", gates, list(gates[0].keys()))
    write_csv(results_dir / "decision.csv", decisions, list(decisions[0].keys()))

    metrics = status_52["key_metrics"]
    status = {
        "status": "complete_coherent_projection_local_silence_gate",
        "readout": "coherent_projection_retained_conditional_not_parent_derived",
        "recommendation": "derive_domain_and_u3_origin_next",
        "next_target": "54-coherent-domain-and-u3-origin.md",
        "support_claim_allowed": False,
        "public_claim_allowed": False,
        "best_candidate": "P_coh[Theta]^i_j=(1/3)<theta>_D delta^i_j, <theta>_D=d ln V_D/dtau",
        "key_metrics": {
            "u3": metrics["u3"],
            "N50": metrics["N50"],
            "projection_candidates": len(candidates),
            "local_gate_tests": len(local),
            "failed_gates": sum(1 for row in gates if row["status"] == "fail"),
            "open_gates": sum(1 for row in gates if row["status"] == "open"),
            "conditional_pass_gates": sum(1 for row in gates if row["status"] == "pass_conditional"),
        },
        "outputs": {
            "source_checkpoint_register": str(results_dir / "source_checkpoint_register.csv"),
            "projection_candidate_ledger": str(results_dir / "projection_candidate_ledger.csv"),
            "coherent_projection_equation_chain": str(results_dir / "coherent_projection_equation_chain.csv"),
            "local_silence_gate_tests": str(results_dir / "local_silence_gate_tests.csv"),
            "circularity_tests": str(results_dir / "circularity_tests.csv"),
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
