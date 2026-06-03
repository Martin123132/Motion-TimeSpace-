from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "local-GR-spin2-rank2-bridge-or-boundary-PPN-gate"
STATUS = "spin2_rank2_bridge_rejected_as_amplitude_derivation_boundary_PPN_gate_selected"
CLAIM_CEILING = "no_rank2_Bmem_or_local_GR_promotion_spin2_is_PPN_consistency_only"
NEXT_TARGET = "352-boundary-nohair-and-PPN-residual-vector-gate.md"


SOURCE_DOCS = [
    (
        "343-dim27-rank2-origin-closure-decision-gate.md",
        "rank-2 and dim-27 amplitude route frozen as explicit closure",
    ),
    (
        "346-GR-and-derivation-north-star-spine.md",
        "GR reduction and PPN residual vector as main gate",
    ),
    (
        "347-local-GR-parent-reduction-theorem-attempt.md",
        "conditional local GR theorem and projector/boundary stress alternatives",
    ),
    (
        "348-N5-projector-stress-conservation-theorem.md",
        "conditional N5 no-bulk-stress theorem",
    ),
    (
        "349-parent-PD-FLRW-projection-compatibility-gate.md",
        "same P_D local/FLRW compatibility bridge",
    ),
    (
        "350-parent-PD-ownership-and-cell-state-derivation-gate.md",
        "quotient P_D parent ownership and spin-2/rank-2 bridge proposal",
    ),
]


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for filename, role in SOURCE_DOCS:
        path = ROOT / filename
        rows.append(
            {
                "source_path": relpath(path),
                "role": role,
                "exists": "yes" if path.exists() else "no",
                "issue": "" if path.exists() else "missing",
            }
        )
    script_path = Path(__file__).resolve()
    rows.append(
        {
            "source_path": relpath(script_path),
            "role": "this spin-2/rank-2 bridge gate builder",
            "exists": "yes" if script_path.exists() else "no",
            "issue": "" if script_path.exists() else "missing",
        }
    )
    return rows


def spin2_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "two_tensor_polarizations_exist_if_local_GR_recovered",
            "input_claim": "metric-only EH exterior has two physical massless spin-2 polarizations",
            "result": "pass_as_GR_consistency",
            "reason": "this is a property of the GR limit, so it is useful for the local branch",
            "impact_on_rank2": "suggestive_number_only",
        },
        {
            "test": "linear_TT_to_FLRW_scalar_map",
            "input_claim": "the two spin-2 polarizations directly give the two FLRW memory readout modes",
            "result": "fail",
            "reason": "TT tensor modes are trace-free anisotropic l=2 objects; FLRW memory load is scalar/isotropic l=0",
            "impact_on_rank2": "no_linear_parent_derivation",
        },
        {
            "test": "trace_readout",
            "input_claim": "rank-2 spin-2 modes can generate Tr(P_active)/dim(V_cell)",
            "result": "fail",
            "reason": "TT modes have zero trace, while the B_mem rank fraction is a scalar trace readout",
            "impact_on_rank2": "trace_mismatch",
        },
        {
            "test": "quadratic_TT_energy_to_scalar",
            "input_claim": "a quadratic tensor-energy scalar could source FLRW memory",
            "result": "allowed_but_not_amplitude_derivation",
            "reason": "quadratic invariants can be scalars, but their amplitude depends on spectrum/state/normalization",
            "impact_on_rank2": "does_not_fix_2over27",
        },
        {
            "test": "Ward_map_from_GR_to_memory_readout",
            "input_claim": "a parent Ward identity maps spin-2 GR content to active memory rank",
            "result": "missing",
            "reason": "no current checkpoint supplies a representation-changing Ward map from l=2 TT to l=0 FLRW readout",
            "impact_on_rank2": "future_theorem_target_only",
        },
    ]


def representation_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "h_ij^TT",
            "SO3_sector": "tensor / l=2 / trace-free",
            "trace": "0",
            "FLRW_background_value": "0 in exact isotropic background",
            "can_source_Bmem_linearly": "no",
            "note": "physical tensor polarizations are anisotropic perturbations, not homogeneous memory load",
        },
        {
            "object": "Q^i_j = X_FLRW delta^i_j",
            "SO3_sector": "scalar / l=0 / isotropic",
            "trace": "3 X_FLRW",
            "FLRW_background_value": "nonzero if memory branch active",
            "can_source_Bmem_linearly": "yes_if_parent_owned",
            "note": "this is the FLRW coherent-load shape from the same-projector route",
        },
        {
            "object": "Tr(P_active)/dim(V_cell)",
            "SO3_sector": "finite-fibre scalar readout",
            "trace": "rank over dimension",
            "FLRW_background_value": "closure target 2/27",
            "can_source_Bmem_linearly": "only_if_rank_dim_normalization_derived",
            "note": "not automatically tied to spacetime tensor polarizations",
        },
        {
            "object": "h_ij^TT h_TT^ij",
            "SO3_sector": "quadratic scalar built from tensor modes",
            "trace": "state-dependent",
            "FLRW_background_value": "depends on tensor background/spectrum",
            "can_source_Bmem_linearly": "no",
            "note": "allowed as second-order backreaction, not a fixed rank theorem",
        },
    ]


def rank2_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_origin": "local_GR_two_polarizations",
            "verdict": "reject_as_amplitude_derivation",
            "why": "number two is real in GR, but its representation is TT tensor rather than FLRW scalar trace",
            "allowed_use": "local GR consistency/PPN branch",
            "forbidden_use": "derive B_mem numerator",
        },
        {
            "candidate_origin": "finite_fibre_rank2_readout",
            "verdict": "closure_locked",
            "why": "active plane remains noncanonical without source/marker theorem",
            "allowed_use": "empirical closure target",
            "forbidden_use": "parent-derived rank claim",
        },
        {
            "candidate_origin": "quadratic_tensor_scalar",
            "verdict": "future_phenomenology_only",
            "why": "could make scalar stress but cannot fix universal 2/27 amplitude",
            "allowed_use": "later perturbation/backreaction study",
            "forbidden_use": "rank-2 theorem",
        },
        {
            "candidate_origin": "boundary_nohair_PPN",
            "verdict": "selected_next",
            "why": "this directly attacks local GR recovery instead of chasing amplitude numerology",
            "allowed_use": "next theorem gate",
            "forbidden_use": "claim local GR before residuals are bounded",
        },
    ]


def boundary_ppn_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_gate_item": "boundary_trace_mode",
            "required_result": "only monopole/trace boundary contribution survives or it renormalizes mass consistently",
            "PPN_risk": "beta/gamma shift if it changes 1/r potentials",
            "test_type": "symbolic residual then observational bound",
        },
        {
            "next_gate_item": "boundary_tracefree_shear",
            "required_result": "trace-free/shear boundary tensor vanishes or decays fast enough",
            "PPN_risk": "anisotropic metric potentials, light bending slip, preferred directions",
            "test_type": "no-hair theorem or multipole suppression bound",
        },
        {
            "next_gate_item": "vector_preferred_frame_terms",
            "required_result": "no surviving local vector/current background in compact exterior",
            "PPN_risk": "preferred-frame parameters and velocity-dependent anomalies",
            "test_type": "symmetry/constraint check plus PPN residual vector",
        },
        {
            "next_gate_item": "clock_ruler_coupling",
            "required_result": "matter, clocks, rulers, and photons see one physical metric",
            "PPN_risk": "WEP violations and non-GR redshift/lensing relations",
            "test_type": "single-metric coupling ledger",
        },
        {
            "next_gate_item": "bulk_MTS_support",
            "required_result": "no residual local bulk MTS stress after quotient P_D silence",
            "PPN_risk": "fifth-force or modified Poisson equation",
            "test_type": "stress ledger and residual source equation",
        },
    ]


def gate_result_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in sources)
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if sources_ok else "fail",
            "evidence": "all cited checkpoints and this script exist" if sources_ok else "missing cited source",
        },
        {
            "gate": "two_GR_tensor_polarizations_valid",
            "status": "pass_as_consistency",
            "evidence": "accepted only inside the conditional local GR/EH branch",
        },
        {
            "gate": "spin2_to_rank2_amplitude_derivation",
            "status": "fail",
            "evidence": "TT tensor representation does not linearly equal FLRW scalar trace readout",
        },
        {
            "gate": "quadratic_tensor_backreaction_derives_2over27",
            "status": "fail",
            "evidence": "quadratic scalar is state-dependent and not a fixed rank/dim theorem",
        },
        {
            "gate": "rank2_closure_lock_preserved",
            "status": "pass",
            "evidence": "rank(P_active)=2 stays closure/theorem target",
        },
        {
            "gate": "local_GR_or_PPN_promoted",
            "status": "fail",
            "evidence": "spin-2 consistency does not replace boundary no-hair or PPN residual calculation",
        },
        {
            "gate": "next_boundary_PPN_gate_selected",
            "status": "pass",
            "evidence": NEXT_TARGET,
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The GR spin-2 observation is useful but not enough. A recovered local Einstein-Hilbert exterior "
                "would have two tensor polarizations, yet those are transverse-traceless l=2 perturbations, while "
                "the FLRW memory amplitude is a scalar/isotropic trace readout. A linear map from the two tensor "
                "polarizations to B_mem's rank-2 numerator is therefore rejected. Quadratic tensor scalars are "
                "allowed in principle, but they are state-dependent backreaction terms and do not derive 2/27. "
                "Rank 2 remains closure-locked, and the next serious GR-first step is the boundary no-hair plus "
                "PPN residual-vector gate."
            ),
            "next_target": NEXT_TARGET,
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    result_dir = run_dir / "results"
    result_dir.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows()
    outputs = {
        "source_register.csv": (
            sources,
            ["source_path", "role", "exists", "issue"],
        ),
        "spin2_rank2_bridge_tests.csv": (
            spin2_bridge_rows(),
            ["test", "input_claim", "result", "reason", "impact_on_rank2"],
        ),
        "SO3_representation_ledger.csv": (
            representation_rows(),
            ["object", "SO3_sector", "trace", "FLRW_background_value", "can_source_Bmem_linearly", "note"],
        ),
        "rank2_decision_ledger.csv": (
            rank2_decision_rows(),
            ["candidate_origin", "verdict", "why", "allowed_use", "forbidden_use"],
        ),
        "boundary_PPN_next_gate.csv": (
            boundary_ppn_rows(),
            ["next_gate_item", "required_result", "PPN_risk", "test_type"],
        ),
        "gate_results.csv": (
            gate_result_rows(sources),
            ["gate", "status", "evidence"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "meaning", "next_target"],
        ),
    }

    for filename, (rows, fieldnames) in outputs.items():
        write_csv(result_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(result_dir),
        "generated": list(outputs),
        "missing_sources": sum(row["exists"] != "yes" for row in sources),
        "spin2_rank2_amplitude_derivation": False,
        "rank2_closure_lock_preserved": True,
        "local_GR_or_PPN_promoted": False,
        "boundary_PPN_gate_selected": True,
        "next_target": NEXT_TARGET,
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build checkpoint 351: local GR spin-2/rank-2 bridge or boundary PPN gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
