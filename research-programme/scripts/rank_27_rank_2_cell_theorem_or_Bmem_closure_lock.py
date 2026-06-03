from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "rank-27-rank-2-cell-theorem-or-Bmem-closure-lock"
STATUS = (
    "rank_27_rank_2_theorem_not_derived_Bmem_2over27_locked_as_empirical_"
    "closure_target_until_cell_rank_and_stress_normalization_owner_exists"
)
CLAIM_CEILING = "Bmem_2over27_closure_lock_no_parent_amplitude_derivation"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"
B_MEM_TARGET = 2.0 / 27.0


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (
            "u3 quarter parent-cell attempt",
            ROOT / "56-u3-quarter-parent-cell-theorem-attempt.md",
            "3+1 cell normalization route and open action gap",
        ),
        (
            "topological cell-current owner attempt",
            ROOT / "59-topological-cell-current-owner-attempt.md",
            "topology protects local hair but does not select branch",
        ),
        (
            "bound-domain boundary attempt",
            ROOT / "61-bound-domain-boundary-theorem-attempt.md",
            "local/FLRW boundary split and domain-selector gap",
        ),
        (
            "Bmem p u3 ownership gate",
            ROOT / "91-Bmem-p-u3-parent-ownership-gate.md",
            "amplitude not parent-predicted",
        ),
        (
            "FLRW reduction checkpoint",
            ROOT / "253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md",
            "rank-27/rank-2 theorem target",
        ),
        (
            "253 rank amplitude candidates",
            ROOT
            / "runs"
            / "20260601-000070-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure"
            / "results"
            / "projector_rank_amplitude_candidates.csv",
            "machine-readable 2/27 target requirements",
        ),
    ]
    return [
        {
            "source": source,
            "path": relpath(path),
            "exists": "yes" if path.exists() else "no",
            "use_in_254": use,
        }
        for source, path, use in sources
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "attempt": "spatial_dimension_count",
            "candidate_derivation": "three spatial dimensions give a cubic determinant and p=3",
            "what_it_gives": "p=3 shape",
            "what_it_fails_to_give": "denominator 27 or numerator 2",
            "verdict": "insufficient",
        },
        {
            "attempt": "3plus1_cell_count",
            "candidate_derivation": "three spatial legs plus one time/normalization leg give X_FLRW=4N",
            "what_it_gives": "u3=1/4 conditional route",
            "what_it_fails_to_give": "rank-27 state space or rank-2 active projector",
            "verdict": "insufficient",
        },
        {
            "attempt": "ternary_spatial_cell_complex",
            "candidate_derivation": "three spatial axes each carry three topological states, so D_cell=3^3=27",
            "what_it_gives": "denominator 27 if ternary states are parent-owned",
            "what_it_fails_to_give": "why each axis is ternary rather than binary/continuous",
            "verdict": "possible_but_unproved",
        },
        {
            "attempt": "FLRW_scalar_rank",
            "candidate_derivation": "homogeneous isotropic background has one scalar memory exchange mode",
            "what_it_gives": "rank 1, not rank 2",
            "what_it_fails_to_give": "numerator 2",
            "verdict": "rejects_rank2_from_scalar_symmetry_alone",
        },
        {
            "attempt": "two_tensor_polarizations",
            "candidate_derivation": "rank 2 from two transverse tensor polarizations",
            "what_it_gives": "a natural number two in GR-like perturbations",
            "what_it_fails_to_give": "background scalar amplitude B_mem without mixing sectors",
            "verdict": "wrong_sector_for_background_amplitude",
        },
        {
            "attempt": "two_boundary_orientations",
            "candidate_derivation": "rank 2 from inward/outward or past/future relative boundary orientations",
            "what_it_gives": "possible topological numerator",
            "what_it_fails_to_give": "owned orientation rule without reintroducing clock or pair-ruler sidecar",
            "verdict": "possible_but_unproved",
        },
        {
            "attempt": "stress_normalization_unity",
            "candidate_derivation": "Bianchi exchange maps projector trace fraction directly into H^2/H0^2",
            "what_it_gives": "kappa_mem=1 if exchange law is normalized",
            "what_it_fails_to_give": "actual memory stress action and conservation exchange",
            "verdict": "not_derived",
        },
    ]


def sufficient_theorem_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "condition": "C1_cell_vector_space",
            "exact_requirement": "parent defines a metric-independent FLRW cell vector space V_cell",
            "needed_for": "prevents 27 being inserted after the fit",
            "current_status": "open",
        },
        {
            "condition": "C2_rank_27",
            "exact_requirement": "dim(V_cell)=27 from a non-circular topological/domain construction",
            "needed_for": "denominator of 2/27",
            "current_status": "not_derived",
        },
        {
            "condition": "C3_active_rank_2",
            "exact_requirement": "P_active is an idempotent projector with Tr(P_active)=2 in the FLRW exchange sector",
            "needed_for": "numerator of 2/27",
            "current_status": "not_derived",
        },
        {
            "condition": "C4_unity_stress_normalization",
            "exact_requirement": "Bianchi/stress exchange gives kappa_mem=1 with no fitted multiplier",
            "needed_for": "turns rank fraction into physical H^2/H0^2 amplitude",
            "current_status": "not_derived",
        },
        {
            "condition": "C5_no_clock_or_pair_sidecar",
            "exact_requirement": "rank selection uses domain/topology only, not a global clock or independent pair-ruler rule",
            "needed_for": "keeps lead no-clock branch honest",
            "current_status": "required_guard",
        },
        {
            "condition": "C6_same_local_projector",
            "exact_requirement": "same P_D still has delta_g P_D=0 and no bulk projector stress in local exterior",
            "needed_for": "prevents cosmology amplitude derivation from breaking local N5",
            "current_status": "conditional_from_251_252",
        },
    ]


def no_go_rows() -> list[dict[str, Any]]:
    return [
        {
            "no_go": "idempotent_projector_arithmetic",
            "statement": "P^2=P only forces eigenvalues 0 or 1; it does not fix dim(V) or rank(P)",
            "consequence": "2/27 cannot be derived from projector-ness alone",
            "escape_route": "derive V_cell and active subspace from parent topology",
        },
        {
            "no_go": "isotropy_scalar_rank",
            "statement": "strict FLRW scalar background supplies one homogeneous scalar exchange channel",
            "consequence": "rank 2 is not forced by FLRW symmetry alone",
            "escape_route": "derive two boundary/orientation classes without making them a clock/sidecar",
        },
        {
            "no_go": "dimension_count_limit",
            "statement": "three spatial dimensions explain cubic shape but not a 27-dimensional state space",
            "consequence": "p=3 is easier than B_mem=2/27",
            "escape_route": "derive ternary state space per spatial leg",
        },
        {
            "no_go": "stress_units_normalization",
            "statement": "a rank fraction is dimensionless bookkeeping until a stress/exchange law maps it to H^2/H0^2",
            "consequence": "kappa_mem is a hidden amplitude unless derived",
            "escape_route": "derive memory stress-energy or geometric Bianchi exchange",
        },
        {
            "no_go": "posthoc_rank_choice",
            "statement": "choosing D=27 and r=2 because 2/27 is attractive is not derivation",
            "consequence": "current 2/27 stays closure-only",
            "escape_route": "predict rank before fitting or from an independent parent object",
        },
    ]


def closure_lock_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "p",
            "value": "3",
            "status_after_254": "conditional_shape_route",
            "reason": "det(Q) on FLRW gives X^3 if Q/P_D are parent-owned",
            "public_claim": "not derived from complete parent action",
        },
        {
            "quantity": "u3",
            "value": "1/4",
            "status_after_254": "conditional_cell_route",
            "reason": "3+1 normalization route survives but clock/spatial split remains open",
            "public_claim": "not derived from complete parent action",
        },
        {
            "quantity": "B_mem",
            "value": "2/27",
            "status_after_254": "empirical_closure_theorem_target",
            "reason": "rank-27/rank-2/unity-normalization theorem not derived",
            "public_claim": "not derived",
        },
        {
            "quantity": "P_D",
            "value": "topological projector",
            "status_after_254": "same_object_route_conditional",
            "reason": "can serve local N5 and FLRW shape only if parent-owned",
            "public_claim": "not full unification",
        },
    ]


def next_derivation_queue_rows() -> list[dict[str, Any]]:
    return [
        {
            "rank": 1,
            "target": "derive_memory_stress_exchange_normalization",
            "why_first": "even a perfect rank fraction is not physics without kappa_mem",
            "success_condition": "kappa_mem predicted with sign and conservation law",
        },
        {
            "rank": 2,
            "target": "derive_or_reject_ternary_spatial_cell_space",
            "why_first": "D_cell=27 must not be chosen after seeing 2/27",
            "success_condition": "parent topological/domain action forces 3 states per spatial leg",
        },
        {
            "rank": 3,
            "target": "derive_two_active_exchange_classes",
            "why_first": "numerator 2 must be owned without tensor-sector mixing or clock sidecar",
            "success_condition": "Tr(P_active)=2 from cohomology/boundary orientation theorem",
        },
        {
            "rank": 4,
            "target": "local_N6_nohair_for_same_projector",
            "why_first": "cosmology derivation must not break local GR route",
            "success_condition": "P_D auxiliary/topological modes add no local propagating hair",
        },
    ]


def claim_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "rank-27/rank-2 theorem is derived",
            "status": "forbidden",
            "reason": "D_cell=27, rank=2, and kappa=1 are all unproved",
        },
        {
            "claim": "B_mem=2/27 is a precise theorem target",
            "status": "allowed",
            "reason": "the sufficient conditions are now explicit and testable",
        },
        {
            "claim": "B_mem=2/27 is closure-locked for now",
            "status": "allowed",
            "reason": "the derivation attempt found exact missing parent ingredients",
        },
        {
            "claim": "the branch is dead because 2/27 is not derived",
            "status": "not_supported",
            "reason": "p=3/u3 shape route survives and 2/27 remains near a plausible empirical corridor",
        },
        {
            "claim": "cosmology support/CMB pass/local GR pass",
            "status": "forbidden",
            "reason": "background amplitude, perturbations, and local N6 are not closed",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    not_derived_conditions = sum(row["current_status"] == "not_derived" for row in sufficient_theorem_contract_rows())
    no_go_count = len(no_go_rows())
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "promotion_allowed": "false",
        },
        {
            "gate": "sufficient theorem contract written",
            "status": "pass",
            "evidence": f"conditions={len(sufficient_theorem_contract_rows())}",
            "promotion_allowed": "theorem target only",
        },
        {
            "gate": "no-go reasons explicit",
            "status": "pass" if no_go_count >= 5 else "fail",
            "evidence": f"no_go_count={no_go_count}",
            "promotion_allowed": "false",
        },
        {
            "gate": "rank/stress derivation complete",
            "status": "fail",
            "evidence": f"not_derived_core_conditions={not_derived_conditions}",
            "promotion_allowed": "false",
        },
        {
            "gate": "B_mem closure lock applied",
            "status": "pass",
            "evidence": "2/27 remains empirical closure theorem-target",
            "promotion_allowed": "closure only",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "meaning": (
                "The rank-27/rank-2 route is now sharply specified but not derived. "
                "Three spatial dimensions can own the cubic p=3 shape conditionally, and 3+1 cell normalization "
                "can own u3=1/4 conditionally, but they do not force a 27-dimensional cell state space, a rank-2 "
                "active projector, or unity stress normalization. Therefore B_mem=2/27 is locked as a disciplined "
                "empirical closure theorem-target until a parent cell-rank and stress-exchange theorem exists."
            ),
            "Bmem_target": f"{B_MEM_TARGET:.12f}",
            "promotion_allowed": "false",
            "next_target": "255-memory-stress-exchange-normalization-or-kappa-mem-free.md",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_id = f"{timestamp}-{RUN_SLUG}"
    run_dir = ROOT / "runs" / run_id
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (
            source_register_rows(),
            ["source", "path", "exists", "use_in_254"],
        ),
        "rank_theorem_attempts.csv": (
            theorem_attempt_rows(),
            ["attempt", "candidate_derivation", "what_it_gives", "what_it_fails_to_give", "verdict"],
        ),
        "sufficient_theorem_contract.csv": (
            sufficient_theorem_contract_rows(),
            ["condition", "exact_requirement", "needed_for", "current_status"],
        ),
        "no_go_lemmas.csv": (
            no_go_rows(),
            ["no_go", "statement", "consequence", "escape_route"],
        ),
        "Bmem_closure_lock.csv": (
            closure_lock_rows(),
            ["quantity", "value", "status_after_254", "reason", "public_claim"],
        ),
        "next_derivation_queue.csv": (
            next_derivation_queue_rows(),
            ["rank", "target", "why_first", "success_condition"],
        ),
        "claim_policy_after_254.csv": (
            claim_policy_rows(),
            ["claim", "status", "reason"],
        ),
        "claim_gate_results.csv": (
            claim_gate_rows(),
            ["gate", "status", "evidence", "promotion_allowed"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "lead_branch", "meaning", "Bmem_target", "promotion_allowed", "next_target"],
        ),
    }

    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    status_payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "missing_sources": sum(row["exists"] != "yes" for row in source_register_rows()),
        "Bmem_2over27_target": f"{B_MEM_TARGET:.12f}",
        "rank_27_derived": False,
        "rank_2_derived": False,
        "kappa_mem_derived": False,
        "Bmem_parent_derived": False,
        "Bmem_closure_locked": True,
        "promotion_allowed": False,
        "next_target": "255-memory-stress-exchange-normalization-or-kappa-mem-free.md",
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return status_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build checkpoint 254: rank-27/rank-2 theorem attempt or closure lock.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
