from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "endpoint-occupancy-arrow-attempt"
STATUS = "endpoint_occupancy_delta_n2_conditionally_derived_arrow_not_parent_owned"
CLAIM_CEILING = "conditional_endpoint_law_only_no_full_Bmem_or_local_GR_promotion"


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
        (ROOT / "288-k9-Ward-index-level-attempt.md", "endpoint occupancy target n=3 -> n=1"),
        (ROOT / "292-relative-index-level-theorem-attempt.md", "conditional relative-index k=9 and B_mem chain"),
        (ROOT / "293-domain-topology-selection-attempt.md", "conditional B3 topology and next endpoint target"),
        (ROOT / "276-coherent-domain-projector-from-parent-variables.md", "coherent SO(3) isotropic projector route"),
    ]
    return [{"source": relpath(path), "role": role, "exists": "yes" if path.exists() else "no"} for path, role in sources]


def projector_algebra_rows() -> list[dict[str, Any]]:
    spatial_dimension = 3
    rank_diagonal_axis_sector = 3
    rank_isotropic_trace_sector = 1
    delta_n = rank_diagonal_axis_sector - rank_isotropic_trace_sector
    k_level = 9
    trace_partition = 3
    b_mem = delta_n / (trace_partition * k_level)
    return [
        {
            "object": "axis_load_sector_A",
            "definition": "A=span{E_11,E_22,E_33} inside End(TSigma_D)",
            "rank_or_trace": rank_diagonal_axis_sector,
            "meaning": "three resolved spatial axis-load occupancies before scalar trace quotient",
            "status": "kinematic_definition",
        },
        {
            "object": "early_axis_projector_P_axis",
            "definition": "P_axis=I_A on the diagonal axis-load sector",
            "rank_or_trace": rank_diagonal_axis_sector,
            "meaning": "n_early=Tr(P_axis)=3",
            "status": "conditional_endpoint_definition",
        },
        {
            "object": "late_scalar_projector_P_iso",
            "definition": "P_iso=(1/3) 11^T on A, equivalently Q -> (Tr Q/3)I",
            "rank_or_trace": rank_isotropic_trace_sector,
            "meaning": "n_today=Tr(P_iso)=1",
            "status": "SO3_equivariant_projection",
        },
        {
            "object": "rank_defect",
            "definition": "Delta n=Tr(P_axis)-Tr(P_iso)",
            "rank_or_trace": delta_n,
            "meaning": "Delta n=3-1=2",
            "status": "conditional_pass",
        },
        {
            "object": "amplitude_chain",
            "definition": "B_mem=Delta n/(3*k)",
            "rank_or_trace": b_mem,
            "meaning": "with k=9 this gives B_mem=2/27",
            "status": "conditional_chain_not_parent_promotion",
        },
    ]


def representation_decomposition_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector": "trace_scalar",
            "SO3_spin": "0",
            "dimension": 1,
            "FLRW_status": "retained",
            "role": "late scalar memory/ruler response",
        },
        {
            "sector": "antisymmetric_rotational",
            "SO3_spin": "1",
            "dimension": 3,
            "FLRW_status": "projected_out",
            "role": "rotation/vorticity-like non-scalar response",
        },
        {
            "sector": "symmetric_traceless_shear",
            "SO3_spin": "2",
            "dimension": 5,
            "FLRW_status": "projected_out",
            "role": "anisotropic/shear-like non-scalar response",
        },
        {
            "sector": "diagonal_axis_loads",
            "SO3_spin": "axis_resolved_prequotient",
            "dimension": 3,
            "FLRW_status": "collapsed_to_trace",
            "role": "source of n_early=3 before scalar quotient",
        },
    ]


def arrow_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "SO3_projection_only",
            "law": "P_axis -> P_iso by scalar projection",
            "what_it_derives": "Delta n=2 as a rank defect",
            "what_it_does_not_derive": "time direction or irreversibility",
            "status": "conditional_math_pass",
        },
        {
            "route": "coarse_graining_semigroup",
            "law": "P(t+s)=P(t)P(s), information/non-scalar rank cannot increase",
            "what_it_derives": "arrow from resolved axis loads to scalar quotient",
            "what_it_does_not_derive": "why this semigroup is the parent time flow",
            "status": "closure_unless_parent_owned",
        },
        {
            "route": "positive_anisotropy_penalty",
            "law": "V=||Q-(Tr Q/3)I||^2 drives non-scalar modes to zero",
            "what_it_derives": "late scalar endpoint as stable minimum",
            "what_it_does_not_derive": "occupancy trace jump as topological charge instead of relaxation amplitude",
            "status": "partial",
        },
        {
            "route": "Ward_trace_selection",
            "law": "only trace Ward charge couples to FLRW stress",
            "what_it_derives": "n_today=1 and one-third trace partition together",
            "what_it_does_not_derive": "n_early=3 unless axis-resolved endpoint is also parent-owned",
            "status": "best_parent_contract",
        },
        {
            "route": "built_endpoint_potential",
            "law": "V(n)=n(n-1)(n-3)",
            "what_it_derives": "roots 1 and 3",
            "what_it_does_not_derive": "noncircular origin of coefficients",
            "status": "rejected_if_inserted",
        },
    ]


def amplitude_chain_rows() -> list[dict[str, Any]]:
    k_level = 9
    trace_partition = 3
    n_early = 3
    n_today = 1
    delta_n = n_early - n_today
    b_mem = delta_n / (trace_partition * k_level)
    return [
        {
            "step": "k_level",
            "value": k_level,
            "formula": "|index(End(TSigma_D),rel)|",
            "status": "conditional_from_292",
            "blocker": "depends on B3 coherent-domain topology from checkpoint 293",
        },
        {
            "step": "trace_partition",
            "value": trace_partition,
            "formula": "Pi_iso(Q)=(Tr Q/3)I",
            "status": "conditional_from_SO3_projection",
            "blocker": "parent Ward coupling must choose normalized trace",
        },
        {
            "step": "n_early",
            "value": n_early,
            "formula": "Tr(P_axis)=3",
            "status": "conditional_projector_rank",
            "blocker": "early endpoint must be parent-defined as axis-resolved occupancy",
        },
        {
            "step": "n_today",
            "value": n_today,
            "formula": "Tr(P_iso)=1",
            "status": "conditional_projector_rank",
            "blocker": "late endpoint must be parent-defined as scalar trace occupancy",
        },
        {
            "step": "Delta_n",
            "value": delta_n,
            "formula": "Tr(P_axis)-Tr(P_iso)=2",
            "status": "conditional_pass",
            "blocker": "arrow is not yet parent-owned",
        },
        {
            "step": "B_mem",
            "value": b_mem,
            "formula": "Delta n/(3*k)=2/(3*9)=2/27",
            "status": "conditional_chain_only",
            "blocker": "no full parent derivation until k, trace, endpoints, and arrow are all action-owned",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    source_missing = [source for source in source_register_rows() if source["exists"] != "yes"]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not source_missing else "fail",
            "evidence": "all cited post-checkpoint sources exist" if not source_missing else ";".join(source["source"] for source in source_missing),
            "claim_effect": "audit traceable",
        },
        {
            "gate": "endpoint_projectors_defined",
            "status": "pass",
            "evidence": "P_axis=I_A has trace 3; P_iso=(1/3)11^T has trace 1",
            "claim_effect": "n=3 and n=1 have an exact projector interpretation",
        },
        {
            "gate": "Delta_n_derived",
            "status": "conditional_pass",
            "evidence": "Delta n=Tr(P_axis)-Tr(P_iso)=2",
            "claim_effect": "endpoint integer gap is no longer arbitrary if occupancy means projector trace",
        },
        {
            "gate": "SO3_trace_projection_unique",
            "status": "pass",
            "evidence": "the only SO(3)-invariant scalar endomorphism projection is the trace line",
            "claim_effect": "n_today=1 is well motivated in the scalar FLRW branch",
        },
        {
            "gate": "early_axis_endpoint_parent_owned",
            "status": "fail",
            "evidence": "parent action has not yet forced the early endpoint to be axis-resolved P_axis rather than already trace-projected",
            "claim_effect": "n_early=3 remains conditional",
        },
        {
            "gate": "arrow_parent_owned",
            "status": "fail",
            "evidence": "coarse-graining direction P_axis -> P_iso is plausible but not derived from the parent time/action principle",
            "claim_effect": "3 -> 1 not promoted as a dynamical theorem",
        },
        {
            "gate": "B_mem_derived",
            "status": "fail",
            "evidence": "B_mem=2/27 follows only as a conditional chain using k=9, trace partition, projector endpoints, and assumed arrow",
            "claim_effect": "locked empirical closure retained",
        },
        {
            "gate": "local_silence_derived",
            "status": "fail",
            "evidence": "endpoint projector algebra does not suppress q_loc or prove PPN safety",
            "claim_effect": "no local-GR promotion",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "meaning": (
                "The endpoint integers can be given a clean non-polynomial meaning: n_early=3 is the trace/rank "
                "of the resolved diagonal spatial-axis projector, and n_today=1 is the trace/rank of the SO(3) "
                "scalar trace projector. Therefore Delta n=2 follows as a projector rank defect. This is a real "
                "conditional derivation of the integer gap, but the parent action still has to derive the early "
                "axis-resolved endpoint and the irreversible arrow P_axis -> P_iso."
            ),
            "next_target": "derive_arrow_from_parent_time_or_Ward_trace_action",
        }
    ]


def build_outputs(timestamp: str) -> dict[str, Any]:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "source_register.csv": (source_register_rows(), ["source", "role", "exists"]),
        "projector_algebra.csv": (
            projector_algebra_rows(),
            ["object", "definition", "rank_or_trace", "meaning", "status"],
        ),
        "representation_decomposition.csv": (
            representation_decomposition_rows(),
            ["sector", "SO3_spin", "dimension", "FLRW_status", "role"],
        ),
        "arrow_routes.csv": (
            arrow_route_rows(),
            ["route", "law", "what_it_derives", "what_it_does_not_derive", "status"],
        ),
        "amplitude_chain.csv": (
            amplitude_chain_rows(),
            ["step", "value", "formula", "status", "blocker"],
        ),
        "gate_results.csv": (
            gate_rows(),
            ["gate", "status", "evidence", "claim_effect"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "meaning", "next_target"],
        ),
    }
    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "Delta_n_derived_conditionally": True,
        "B_mem_derived_now": False,
        "local_GR_promoted_now": False,
        "next_target": "derive_arrow_from_parent_time_or_Ward_trace_action",
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Endpoint occupancy and arrow derivation attempt.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
