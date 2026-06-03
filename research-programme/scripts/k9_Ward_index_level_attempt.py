from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "k9-Ward-index-level-attempt"
STATUS = "k9_Ward_index_level_not_derived_rank9_bundle_target_retained"
CLAIM_CEILING = "k9_theorem_target_only_no_Bmem_or_parent_promotion"


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def relpath(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (ROOT / "109-boundary-charge-two-ninth-theorem-attempt.md", "two-ninth theorem target and failed shortcuts"),
        (ROOT / "110-endpoint-charge-equation-attempt.md", "endpoint quadratic and coefficient target"),
        (ROOT / "111-endpoint-quadratic-variational-owner-attempt.md", "Ward-generated potential target, not coefficient derivation"),
        (ROOT / "142-domain-load-tensor-owner-promotion-gate.md", "Q as coherent-volume load and rank-3 spatial domain structure"),
        (ROOT / "287-boundary-current-charge-owner-attempt.md", "integer-level obstruction k=9, n=(1,3)"),
        (ROOT / "scripts" / "topological_cell_current_owner_attempt.py", "previous characteristic-class route"),
        (ROOT / "scripts" / "k9_Ward_index_level_attempt.py", "this Ward/index-level attempt"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def candidate_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "rank_End_spatial_coframe",
            "k9_source": "rank End(TSigma)=3x3=9",
            "what_it_can_explain": "why a nine-slot charge lattice is natural for Q^i_j",
            "failure": "rank is component counting unless parent action defines an integral charge lattice on End(TSigma)",
            "status": "best_theorem_target",
        },
        {
            "candidate": "GL3_component_count",
            "k9_source": "dim GL(3)=9",
            "what_it_can_explain": "full spatial deformation channel has nine components before isotropic projection",
            "failure": "FLRW branch uses trace/isotropic line, not all nine components dynamically",
            "status": "motivation_only",
        },
        {
            "candidate": "SO3_adjoint",
            "k9_source": "dim so(3)=3, not 9",
            "what_it_can_explain": "spatial rotational gauge sector",
            "failure": "gives wrong level and mostly gauge rotations, not load amplitude",
            "status": "rejected_for_k9",
        },
        {
            "candidate": "determinant_coefficient",
            "k9_source": "27/3=9 from det coefficient divided by trace dimension",
            "what_it_can_explain": "connects p=3 determinant route to trace partition",
            "failure": "post-hoc unless variation directly yields level and endpoint charges",
            "status": "algebraic_hint_only",
        },
        {
            "candidate": "Chern_Simons_or_BF_level",
            "k9_source": "integer level k can be assigned",
            "what_it_can_explain": "integral periods and topological quantization",
            "failure": "topological level is free unless anomaly/Ward cancellation fixes it to 9",
            "status": "open_not_derived",
        },
        {
            "candidate": "Euler_signature_index",
            "k9_source": "topological index of a cell bundle",
            "what_it_can_explain": "would be a genuine non-counting derivation if index=9",
            "failure": "no explicit bundle/operator/index produces 9",
            "status": "not_constructed",
        },
    ]


def rank9_bundle_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "parent_bundle_defined",
            "needed_statement": "E_D=End(TSigma_D) or equivalent spatial load bundle is selected before FLRW",
            "current_evidence": "Q^i_j coherent-volume load exists conditionally",
            "status": "partial",
            "promotion_blocker": "parent has not selected E_D as charge lattice",
        },
        {
            "test": "integral_period_structure",
            "needed_statement": "relative current periods lie in (1/rank(E_D))Z or equivalent",
            "current_evidence": "relative closure gives conserved classes but not period normalization",
            "status": "fail",
            "promotion_blocker": "Q_* remains free",
        },
        {
            "test": "isotropic_projection_compatibility",
            "needed_statement": "FLRW trace line inherits denominator 9 rather than collapsing to denominator 1 or 3",
            "current_evidence": "FLRW Q^i_j=(N/u3)delta^i_j is trace/isotropic",
            "status": "open",
            "promotion_blocker": "using all nine slots may conflict with isotropic trace branch",
        },
        {
            "test": "endpoint_occupancy_selection",
            "needed_statement": "allowed endpoint occupancies are n_today=1 and n_early=3",
            "current_evidence": "these values reproduce the target",
            "status": "fail",
            "promotion_blocker": "no dynamics selects occupancies",
        },
        {
            "test": "endpoint_arrow",
            "needed_statement": "relaxation selects n=3 -> n=1",
            "current_evidence": "formal potential arrow remains unresolved",
            "status": "fail",
            "promotion_blocker": "stability/arrow theorem missing",
        },
        {
            "test": "trace_partition",
            "needed_statement": "B_mem=(n_early-n_today)/(3k)",
            "current_evidence": "spatial trace partition is natural but Ward coupling not derived",
            "status": "conditional",
            "promotion_blocker": "trace Ward identity missing",
        },
    ]


def index_requirements_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "operator_or_complex",
            "must_exist": "a parent differential complex whose index counts the relative charge level",
            "why": "without an operator, index language is decoration",
            "status": "missing",
        },
        {
            "requirement": "bundle_choice",
            "must_exist": "the complex acts on the spatial load/coframe endomorphism bundle, not an arbitrary auxiliary bundle",
            "why": "k=9 must belong to MTS variables",
            "status": "missing",
        },
        {
            "requirement": "index_value",
            "must_exist": "index(E_D)=9 or effective period denominator 9",
            "why": "this is the exact level needed by checkpoint 287",
            "status": "missing",
        },
        {
            "requirement": "boundary_condition",
            "must_exist": "relative boundary conditions make local bound domains trivial and FLRW domains nontrivial",
            "why": "same theorem must protect local silence",
            "status": "missing",
        },
        {
            "requirement": "Ward_trace_coupling",
            "must_exist": "variation maps level charge into Gamma_eff/stress with one-third trace partition",
            "why": "otherwise k=9 does not become B_mem=2/27",
            "status": "missing",
        },
    ]


def endpoint_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_candidate": "endpoint_quadratic",
            "equation": "27R^2-12R+1=0",
            "integer_readout": "k=9 gives endpoints n=1,3",
            "status": "formal_target",
            "reason_not_derived": "coefficients are not produced by a parent variation",
        },
        {
            "law_candidate": "occupancy_potential",
            "equation": "V(n)=n(n-1)(n-3) or similar",
            "integer_readout": "selects n=1,3 if built to order",
            "status": "rejected_if_inserted",
            "reason_not_derived": "polynomial over n would be circular unless produced by Ward/index data",
        },
        {
            "law_candidate": "monotone_charge_relaxation",
            "equation": "dn/dtau<0 with fixed points n=3,1",
            "integer_readout": "arrow 3->1",
            "status": "open",
            "reason_not_derived": "no event law or entropy functional selects this arrow",
        },
        {
            "law_candidate": "rank_drop",
            "equation": "rank-active 3 -> rank-residual 1",
            "integer_readout": "delta_n=2",
            "status": "motivation_only",
            "reason_not_derived": "rank drop is plausible language, not a variational theorem",
        },
    ]


def noncircularity_rows() -> list[dict[str, Any]]:
    return [
        {
            "rule": "no_component_counting_as_derivation",
            "test": "does route derive a charge measure, not only count components?",
            "result": "fail_for_rank9_alone",
        },
        {
            "rule": "no_postfit_polynomial",
            "test": "does route generate endpoint roots before knowing 2/27?",
            "result": "fail_for_built_endpoint_potential",
        },
        {
            "rule": "no_free_topological_level",
            "test": "is k fixed by anomaly/Ward/index rather than chosen?",
            "result": "fail_for_BF_level_without_anomaly",
        },
        {
            "rule": "local_silence_same_theorem",
            "test": "does k=9 route also give local trivial relative class?",
            "result": "open",
        },
        {
            "rule": "trace_partition_same_action",
            "test": "does the same variation produce B_mem=DeltaR/3?",
            "result": "open_fail",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    source_missing = [row for row in source_register_rows() if row["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all sources present" if not source_missing else ";".join(row["source"] for row in source_missing),
            "claim_effect": "audit traceable",
        },
        {
            "gate": "rank9_natural_target",
            "status": "pass_as_target",
            "evidence": "End(TSigma) has rank 9 and matches minimal level k=9",
            "claim_effect": "best noncircular target identified",
        },
        {
            "gate": "rank9_derives_charge_lattice",
            "status": "fail",
            "evidence": "rank does not by itself define periods or Q_*",
            "claim_effect": "k=9 not promoted",
        },
        {
            "gate": "Ward_or_index_theorem_exists",
            "status": "fail",
            "evidence": "no operator/complex/anomaly cancellation constructed",
            "claim_effect": "component counting remains insufficient",
        },
        {
            "gate": "endpoint_occupancies_derived",
            "status": "fail",
            "evidence": "n=1,3 are target occupancies only",
            "claim_effect": "DeltaR=2/9 not derived",
        },
        {
            "gate": "trace_partition_derived",
            "status": "fail",
            "evidence": "B_mem=DeltaR/3 remains conditional trace map",
            "claim_effect": "amplitude not promoted",
        },
        {
            "gate": "local_silence_derived",
            "status": "fail",
            "evidence": "relative local trivial class still conditional",
            "claim_effect": "no local-GR promotion",
        },
        {
            "gate": "B_mem_derived",
            "status": "fail",
            "evidence": "k=9, n=1,3, arrow, and trace partition all unproven",
            "claim_effect": "locked empirical closure retained",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The cleanest k=9 candidate is the rank-nine spatial load/coframe endomorphism bundle. "
                "That is a legitimate theorem target because it uses MTS variables already in the Q^i_j branch. "
                "But rank is not a Ward identity: it does not define Q_*, integral periods, endpoint occupancies, endpoint arrow, or trace partition."
            ),
            "next_target": "empirical_no_SH0ES_or_construct_explicit_index_complex_if_theory_route_continues",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "candidate_k9_routes.csv": (
            candidate_route_rows(),
            ["candidate", "k9_source", "what_it_can_explain", "failure", "status"],
        ),
        "rank9_bundle_tests.csv": (
            rank9_bundle_test_rows(),
            ["test", "needed_statement", "current_evidence", "status", "promotion_blocker"],
        ),
        "index_theorem_requirements.csv": (
            index_requirements_rows(),
            ["requirement", "must_exist", "why", "status"],
        ),
        "endpoint_occupancy_law.csv": (
            endpoint_law_rows(),
            ["law_candidate", "equation", "integer_readout", "status", "reason_not_derived"],
        ),
        "noncircularity_tests.csv": (
            noncircularity_rows(),
            ["rule", "test", "result"],
        ),
        "gate_results.csv": (gate_rows(), ["gate", "status", "evidence", "claim_effect"]),
        "decision.csv": (decision_rows(), ["decision", "claim_ceiling", "meaning", "next_target"]),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "k9_best_target": "rank_End_TSigma_equals_9",
        "k9_derived_now": False,
        "B_mem_derived_now": False,
        "rank9_status": "natural_theorem_target_not_Ward_index_derivation",
        "next_target": "empirical_no_SH0ES_or_construct_explicit_index_complex_if_theory_route_continues",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="k=9 Ward/index-level derivation attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
