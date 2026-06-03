from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "FLRW-reduction-of-topological-projector-or-Bmem-stays-closure"
STATUS = (
    "FLRW_topological_projector_reduction_derives_shape_conditionally_"
    "Bmem_2over27_rank_fraction_target_not_parent_derived"
)
CLAIM_CEILING = "FLRW_shape_contract_only_Bmem_2over27_stays_closure_theorem_target"
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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    sources = [
        (
            "FLRW memory-current contract",
            ROOT / "51-FLRW-memory-current-contract.md",
            "p=3 determinant route and Q^i_j contract",
        ),
        (
            "Bmem p u3 ownership gate",
            ROOT / "91-Bmem-p-u3-parent-ownership-gate.md",
            "previous B_mem amplitude and u3 ownership status",
        ),
        (
            "topological projector parent skeleton",
            ROOT / "252-topological-projector-parent-action-skeleton.md",
            "same P_D must reduce to FLRW memory projector",
        ),
        (
            "91 empirical B_mem evidence",
            ROOT
            / "runs"
            / "20260531-132046-Bmem-p-u3-parent-ownership-gate"
            / "results"
            / "cosmology_parameter_evidence.csv",
            "fixed-branch B_mem range",
        ),
        (
            "252 FLRW compatibility table",
            ROOT
            / "runs"
            / "20260601-000069-topological-projector-parent-action-skeleton"
            / "results"
            / "FLRW_compatibility_requirements.csv",
            "machine-readable same-projector requirements",
        ),
        (
            "252 open parent obligations",
            ROOT
            / "runs"
            / "20260601-000069-topological-projector-parent-action-skeleton"
            / "results"
            / "open_parent_obligations.csv",
            "open FLRW amplitude and N6 obligations",
        ),
    ]
    return [
        {
            "source": source,
            "path": relpath(path),
            "exists": "yes" if path.exists() else "no",
            "use_in_253": use,
        }
        for source, path, use in sources
    ]


def empirical_bmem_summary() -> dict[str, Any]:
    path = (
        ROOT
        / "runs"
        / "20260531-132046-Bmem-p-u3-parent-ownership-gate"
        / "results"
        / "cosmology_parameter_evidence.csv"
    )
    if not path.exists():
        return {
            "count": 0,
            "min": "",
            "max": "",
            "target": f"{B_MEM_TARGET:.12f}",
            "target_minus_min": "",
            "relative_offset_from_min": "",
            "note": "evidence file missing",
        }
    values: list[float] = []
    for row in read_csv(path):
        if row.get("model") == "MTS_fixed_p3_u3quarter" and row.get("parameter") == "B_mem":
            try:
                values.append(float(row["best_fit"]))
            except (TypeError, ValueError):
                pass
    if not values:
        return {
            "count": 0,
            "min": "",
            "max": "",
            "target": f"{B_MEM_TARGET:.12f}",
            "target_minus_min": "",
            "relative_offset_from_min": "",
            "note": "no fixed branch B_mem rows",
        }
    bmin = min(values)
    bmax = max(values)
    return {
        "count": len(values),
        "min": f"{bmin:.12f}",
        "max": f"{bmax:.12f}",
        "target": f"{B_MEM_TARGET:.12f}",
        "target_minus_min": f"{B_MEM_TARGET - bmin:.12f}",
        "relative_offset_from_min": f"{(B_MEM_TARGET - bmin) / bmin:.12f}",
        "note": "target is near the lower fixed-branch corridor but this is not a derivation",
    }


def flrw_reduction_chain_rows() -> list[dict[str, Any]]:
    return [
        {
            "step": 1,
            "object": "P_D",
            "statement": "same metric-independent relative/topological chain projector used in local N5 route",
            "result": "allowed_parent_object",
            "derived_status": "conditional_from_252",
            "blocking_gap": "operator realization still skeleton-only",
        },
        {
            "step": 2,
            "object": "homogeneous_isotropic_reduction",
            "statement": "FLRW symmetry collapses any spatial coherent load tensor to Q^i_j=X_FLRW delta^i_j",
            "result": "shape_reduction",
            "derived_status": "kinematic_symmetry_if_Q_owned",
            "blocking_gap": "Q^i_j still needs parent definition before imposing FLRW",
        },
        {
            "step": 3,
            "object": "I_M=det(Q)",
            "statement": "det(X delta)=X^3 gives cubic memory exposure",
            "result": "p=3",
            "derived_status": "conditional_shape_theorem",
            "blocking_gap": "determinant invariant must be selected by parent action/current",
        },
        {
            "step": 4,
            "object": "X_FLRW=4N",
            "statement": "3+1 cell normalization would give u3=1/4 while time leg normalizes rather than exposing",
            "result": "u3=1/4",
            "derived_status": "conditional_cell_rule",
            "blocking_gap": "clock/spatial split not yet parent-derived",
        },
        {
            "step": 5,
            "object": "B_mem",
            "statement": "topological projector can at most supply a rank/trace fraction times a stress normalization",
            "result": "B_mem=kappa_mem Tr(P_active)/dim(V_cell)",
            "derived_status": "amplitude_contract_only",
            "blocking_gap": "rank, active subspace, and kappa_mem are not parent-derived",
        },
        {
            "step": 6,
            "object": "2/27",
            "statement": "2/27 would follow only if dim(V_cell)=27, rank(P_active)=2, and kappa_mem=1",
            "result": "theorem_target",
            "derived_status": "not_derived",
            "blocking_gap": "rank-27/rank-2/kappa=1 theorem missing",
        },
    ]


def rank_fraction_candidate_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate": "rank_fraction_2_over_27",
            "formula": "B_mem = kappa_mem r_active / D_cell",
            "requirements": "D_cell=27, r_active=2, kappa_mem=1",
            "what_it_would_explain": "exact 2/27 amplitude from projector trace fraction",
            "current_status": "best_theorem_target_not_derivation",
            "failure_mode": "choosing 27 and 2 after seeing 2/27 is numerology",
        },
        {
            "candidate": "three_spatial_ternary_cell_complex",
            "formula": "D_cell = 3^3",
            "requirements": "parent domain cell has three spatial axes each with three allowed memory states",
            "what_it_would_explain": "why denominator is 27 without metric dependence",
            "current_status": "unproved_candidate",
            "failure_mode": "state count not currently forced by action or topology",
        },
        {
            "candidate": "two_active_memory_orientations",
            "formula": "r_active = 2",
            "requirements": "projector selects exactly two independent FLRW memory exchange modes",
            "what_it_would_explain": "why numerator is 2 and sign is positive",
            "current_status": "unproved_candidate",
            "failure_mode": "active rank could be 1, 3, or another value without parent selection",
        },
        {
            "candidate": "stress_exchange_normalization",
            "formula": "kappa_mem = 1",
            "requirements": "Bianchi/exchange law normalizes rank fraction directly into H^2/H0^2 response",
            "what_it_would_explain": "why no extra fitted amplitude multiplies 2/27",
            "current_status": "not_derived",
            "failure_mode": "kappa_mem becomes the hidden fitted amplitude",
        },
        {
            "candidate": "topology_only_no_go",
            "formula": "idempotent projector eigenvalues are 0 or 1, but amplitudes need normalization",
            "requirements": "none",
            "what_it_would_explain": "why topology can quantize a fraction but not by itself set stress units",
            "current_status": "warning",
            "failure_mode": "overclaiming rank arithmetic as physics",
        },
    ]


def Bmem_gate_rows() -> list[dict[str, Any]]:
    empirical = empirical_bmem_summary()
    near_lower = ""
    if empirical["relative_offset_from_min"] not in {"", None}:
        try:
            near_lower = "yes" if abs(float(empirical["relative_offset_from_min"])) < 0.02 else "no"
        except ValueError:
            near_lower = "unknown"
    return [
        {
            "gate": "same_P_D_can_reduce_to_FLRW_shape",
            "result": "pass_conditional",
            "evidence": "topological chain projector can be evaluated on homogeneous isotropic sector",
            "claim_allowed": "shape only",
        },
        {
            "gate": "p3_from_same_structure",
            "result": "pass_conditional",
            "evidence": "I_M=det(Q) gives X^3 if Q is parent-owned",
            "claim_allowed": "conditional p=3 route",
        },
        {
            "gate": "u3_quarter_from_same_structure",
            "result": "open_conditional",
            "evidence": "requires 3+1 cell normalization and no-clock split",
            "claim_allowed": "not promoted",
        },
        {
            "gate": "Bmem_2over27_rank_fraction",
            "result": "theorem_target_not_pass",
            "evidence": "needs D_cell=27, r_active=2, kappa_mem=1",
            "claim_allowed": "closure target only",
        },
        {
            "gate": "Bmem_target_near_empirical_fixed_corridor",
            "result": "interesting_not_evidence",
            "evidence": (
                f"target={empirical['target']}; min={empirical['min']}; "
                f"target_minus_min={empirical['target_minus_min']}; near_lower_2pct={near_lower}"
            ),
            "claim_allowed": "private clue only",
        },
        {
            "gate": "Bmem_parent_derived",
            "result": "fail",
            "evidence": "rank/state/stress normalization theorem missing",
            "claim_allowed": "false",
        },
    ]


def unification_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test": "local_metric_independence",
            "required_result": "delta_g P_D=0 in compact local exterior",
            "current_status": "conditional_from_251_252",
            "if_fails": "N5 metric-only local GR route fails",
            "next_action": "keep P_D topological; reject Hodge projection",
        },
        {
            "test": "FLRW_homogeneous_projection",
            "required_result": "P_D reduces to scalar homogeneous memory load without a global physical clock",
            "current_status": "conditional_shape_possible",
            "if_fails": "cosmology projector is a separate sidecar",
            "next_action": "derive domain labels as gauge/topological data",
        },
        {
            "test": "rank_fraction_amplitude",
            "required_result": "Tr(P_active)/dim(V_cell)=2/27 and kappa_mem=1",
            "current_status": "open",
            "if_fails": "B_mem stays empirical closure",
            "next_action": "derive rank-27/rank-2 cell theorem or reject",
        },
        {
            "test": "no_pair_ruler_sidecar",
            "required_result": "half-kernel/pair-ruler route not used as independent law",
            "current_status": "protected",
            "if_fails": "unification weakens into multiple rules",
            "next_action": "keep pair-ruler closure-only unless derived from P_D",
        },
        {
            "test": "perturbation_and_CMB_bridge",
            "required_result": "same projected memory has stable perturbations and official likelihood bridge",
            "current_status": "unresolved",
            "if_fails": "background-only branch cannot be claimed as cosmology support",
            "next_action": "defer until amplitude and conservation owner are derived",
        },
    ]


def claim_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "same P_D route can conditionally reproduce FLRW p=3 shape",
            "status": "allowed_conditional",
            "reason": "FLRW symmetry plus determinant exposure gives cubic shape if Q/P_D are parent-owned",
        },
        {
            "claim": "B_mem=2/27 is now derived",
            "status": "forbidden",
            "reason": "rank-27/rank-2/kappa=1 theorem is not proved",
        },
        {
            "claim": "2/27 being near fitted corridor is evidence of truth",
            "status": "forbidden",
            "reason": "private clue only; not a parent derivation or robustness result",
        },
        {
            "claim": "local-GR and cosmology projector are unified",
            "status": "not_yet",
            "reason": "same-object route exists but full FLRW amplitude/local N6 closure is open",
        },
        {
            "claim": "B_mem remains a disciplined closure theorem-target",
            "status": "allowed",
            "reason": "the exact missing theorem is now named rather than hidden",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    gates = Bmem_gate_rows()
    failed_derivations = sum(row["result"] == "fail" for row in gates)
    target_rows = sum(row["gate"] == "Bmem_2over27_rank_fraction" for row in gates)
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "promotion_allowed": "false",
        },
        {
            "gate": "FLRW shape route written",
            "status": "pass",
            "evidence": "determinant/cell reduction chain recorded",
            "promotion_allowed": "conditional shape only",
        },
        {
            "gate": "2/27 theorem target isolated",
            "status": "pass" if target_rows == 1 else "fail",
            "evidence": f"target_rows={target_rows}",
            "promotion_allowed": "closure target",
        },
        {
            "gate": "failed derivation remains explicit",
            "status": "pass" if failed_derivations >= 1 else "fail",
            "evidence": f"failed_derivations={failed_derivations}",
            "promotion_allowed": "false",
        },
        {
            "gate": "B_mem promoted as derived",
            "status": "fail",
            "evidence": "rank/state/stress theorem missing",
            "promotion_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    empirical = empirical_bmem_summary()
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "meaning": (
                "The same topological projector skeleton can conditionally reduce to the FLRW determinant "
                "shape route: p=3 is still structurally natural if Q and P_D are parent-owned, and u3=1/4 "
                "remains tied to the 3+1 no-clock cell normalization. But B_mem=2/27 is not derived. "
                "It would require a rank-fraction theorem D_cell=27, r_active=2 plus stress normalization "
                "kappa_mem=1. Until that theorem exists, 2/27 is a sharp closure target, not a claim."
            ),
            "empirical_note": (
                f"2/27={empirical['target']}; fixed-branch range={empirical['min']} to {empirical['max']}; "
                "near lower corridor but not evidence"
            ),
            "promotion_allowed": "false",
            "next_target": "254-rank-27-rank-2-cell-theorem-or-Bmem-closure-lock.md",
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
            ["source", "path", "exists", "use_in_253"],
        ),
        "FLRW_reduction_chain.csv": (
            flrw_reduction_chain_rows(),
            ["step", "object", "statement", "result", "derived_status", "blocking_gap"],
        ),
        "projector_rank_amplitude_candidates.csv": (
            rank_fraction_candidate_rows(),
            ["candidate", "formula", "requirements", "what_it_would_explain", "current_status", "failure_mode"],
        ),
        "Bmem_2over27_derivation_gate.csv": (
            Bmem_gate_rows(),
            ["gate", "result", "evidence", "claim_allowed"],
        ),
        "same_projector_unification_tests.csv": (
            unification_test_rows(),
            ["test", "required_result", "current_status", "if_fails", "next_action"],
        ),
        "claim_policy_after_253.csv": (
            claim_policy_rows(),
            ["claim", "status", "reason"],
        ),
        "claim_gate_results.csv": (
            claim_gate_rows(),
            ["gate", "status", "evidence", "promotion_allowed"],
        ),
        "empirical_Bmem_target_comparison.csv": (
            [empirical_bmem_summary()],
            ["count", "min", "max", "target", "target_minus_min", "relative_offset_from_min", "note"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "lead_branch", "meaning", "empirical_note", "promotion_allowed", "next_target"],
        ),
    }

    for filename, (rows, fieldnames) in outputs.items():
        write_csv(results_dir / filename, rows, fieldnames)

    empirical = empirical_bmem_summary()
    status_payload = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "lead_branch": LEAD_BRANCH,
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "generated": list(outputs),
        "missing_sources": sum(row["exists"] != "yes" for row in source_register_rows()),
        "FLRW_shape_route_conditional": True,
        "Bmem_2over27_target": f"{B_MEM_TARGET:.12f}",
        "Bmem_empirical_min": empirical["min"],
        "Bmem_empirical_max": empirical["max"],
        "Bmem_parent_derived": False,
        "Bmem_stays_closure_theorem_target": True,
        "local_GR_promoted": False,
        "promotion_allowed": False,
        "next_target": "254-rank-27-rank-2-cell-theorem-or-Bmem-closure-lock.md",
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return status_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build checkpoint 253: FLRW reduction of topological projector or B_mem stays closure."
    )
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
