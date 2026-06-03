from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "parent-PD-FLRW-projection-compatibility-gate"
STATUS = "parent_PD_same_operator_bridge_conditionally_coherent_FLRW_shape_only_Bmem_and_local_GR_stay_unpromoted"
CLAIM_CEILING = "same_projector_shape_bridge_only_no_parent_PD_Bmem_or_local_GR_promotion"
NEXT_TARGET = "350-parent-PD-ownership-and-cell-state-derivation-gate.md"


SOURCE_DOCS = [
    (
        "252-topological-projector-parent-action-skeleton.md",
        "parent-action skeleton for a metric-independent relative-chain projector",
    ),
    (
        "253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md",
        "earlier same-projector FLRW shape and B_mem closure target",
    ),
    (
        "343-dim27-rank2-origin-closure-decision-gate.md",
        "post-checkpoint lock that rank-27/rank-2 is closure, not derived",
    ),
    (
        "346-GR-and-derivation-north-star-spine.md",
        "project north star: recover GR locally and derive as much as possible",
    ),
    (
        "347-local-GR-parent-reduction-theorem-attempt.md",
        "conditional local GR reduction theorem and remaining blockers",
    ),
    (
        "348-N5-projector-stress-conservation-theorem.md",
        "N5 conditional theorem for metric-independent topological projector stress",
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
            "role": "this compatibility-gate builder",
            "exists": "yes" if script_path.exists() else "no",
            "issue": "" if script_path.exists() else "missing",
        }
    )
    return rows


def pd_limit_rows() -> list[dict[str, Any]]:
    return [
        {
            "limit": "abstract_parent_operator",
            "required_specialization": "P_D is defined before choosing local or FLRW symmetry reduction",
            "stress_or_projection_result": "one object can have different representations without becoming a sidecar",
            "status": "contract_written_not_parent_derived",
            "gap": "parent action still has to vary/select P_D rather than insert it by hand",
        },
        {
            "limit": "local_compact_exterior",
            "required_specialization": "P_D -> P_top, a metric-independent relative-chain/topological projector",
            "stress_or_projection_result": "delta_g S_top|bulk=0 and T_top_munu|bulk=0",
            "status": "conditional_pass_from_N5",
            "gap": "boundary shear/no-hair and full PPN residual vector remain to be proven",
        },
        {
            "limit": "FLRW_homogeneous_isotropic",
            "required_specialization": "P_D -> P_iso, the coherent spatial memory projection",
            "stress_or_projection_result": "Q^i_j=X_FLRW delta^i_j and determinant exposure gives I_M|FLRW=X_FLRW^3",
            "status": "conditional_shape_pass",
            "gap": "stress amplitude, rank fraction, and normalization are not derived",
        },
        {
            "limit": "metric_or_Hodge_projector",
            "required_specialization": "P_D depends on g, Hodge star, orthogonal projection, least-energy norm, or sqrt(-g) bulk term",
            "stress_or_projection_result": "bulk projector stress is generically nonzero and must be retained",
            "status": "no_go_for_simple_local_GR_route",
            "gap": "would require a modified-exterior branch and explicit PPN bounds",
        },
    ]


def same_operator_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "bridge_condition": "definition_before_limit",
            "why_it_is_not_patchwork": "P_D is an abstract relative-chain projector before local/FLRW reduction",
            "current_status": "conditional_pass",
            "remaining_gap": "need a parent variational principle whose Euler-Lagrange constraints select this P_D",
        },
        {
            "bridge_condition": "local_representation",
            "why_it_is_not_patchwork": "local exterior uses the same object in the metric-independent/topological representation",
            "current_status": "conditional_pass",
            "remaining_gap": "N0/N2/N3/N6 and PPN residuals remain open",
        },
        {
            "bridge_condition": "FLRW_representation",
            "why_it_is_not_patchwork": "FLRW symmetry collapses the same coherent projector to a scalar memory load",
            "current_status": "conditional_shape_pass",
            "remaining_gap": "B_mem=2/27 and kappa_mem are still closure targets",
        },
        {
            "bridge_condition": "shared_stress_ledger",
            "why_it_is_not_patchwork": "stress-free topological part and stress-response memory part must sit in one conserved ledger",
            "current_status": "open",
            "remaining_gap": "Bianchi-safe exchange law between topological selection and metric stress response is not derived",
        },
        {
            "bridge_condition": "no_late_sidecar_parameters",
            "why_it_is_not_patchwork": "rank, cell dimension, and normalization cannot be chosen after cosmology is fitted",
            "current_status": "fail_as_derivation",
            "remaining_gap": "derive dim(V_cell)=27, rank(P_active)=2, and kappa_mem=1 or keep B_mem as closure",
        },
    ]


def amplitude_debt_rows() -> list[dict[str, Any]]:
    return [
        {
            "object": "dim(V_cell)=27",
            "needed_for": "denominator of B_mem rank fraction",
            "current_status": "closure_locked_after_343",
            "why_not_derived": "finite-fibre/state-space count is not forced by the parent action",
            "next_derivation_attempt": "derive cell state space from parent boundary/cohomology data",
        },
        {
            "object": "rank(P_active)=2",
            "needed_for": "numerator of B_mem rank fraction",
            "current_status": "closure_locked_after_343",
            "why_not_derived": "active FLRW exchange subspace is not selected by a Ward identity or extremum law",
            "next_derivation_attempt": "prove active-mode selection from P_D variation or demote permanently",
        },
        {
            "object": "kappa_mem=1",
            "needed_for": "turn topological rank fraction into physical H^2 stress amplitude",
            "current_status": "open_normalization_debt",
            "why_not_derived": "metric stress-response sector is separate from stress-free topological selection",
            "next_derivation_attempt": "derive stress-exchange normalization from Bianchi/Ward ledger",
        },
        {
            "object": "boundary_shear_nohair",
            "needed_for": "local GR and PPN safety",
            "current_status": "open_local_GR_debt",
            "why_not_derived": "boundary-only topological variation may still source trace-free local residuals",
            "next_derivation_attempt": "prove no-hair theorem or compute full PPN residual vector",
        },
        {
            "object": "metric_only_EH_exterior",
            "needed_for": "GR reduction in the Newton/PPN limit",
            "current_status": "conditional_only",
            "why_not_derived": "depends on parent-owned P_D, no bulk MTS exterior support, and conserved stress ledger",
            "next_derivation_attempt": "fold P_D compatibility result into the local GR reduction theorem",
        },
    ]


def local_gr_dependency_rows() -> list[dict[str, Any]]:
    return [
        {
            "dependency": "single physical metric/coframe",
            "role_in_GR_recovery": "prevents multiple-metric ambiguity in the local weak-field limit",
            "status_after_349": "still_required",
            "promotion_allowed": "no",
        },
        {
            "dependency": "metric-independent local P_D",
            "role_in_GR_recovery": "kills bulk projector stress in compact local exterior",
            "status_after_349": "conditional_pass",
            "promotion_allowed": "conditional_only",
        },
        {
            "dependency": "conserved stress ledger",
            "role_in_GR_recovery": "keeps Bianchi identity honest rather than dropping hidden stress",
            "status_after_349": "open_for_full_parent",
            "promotion_allowed": "no",
        },
        {
            "dependency": "metric-only EH exterior",
            "role_in_GR_recovery": "gives Einstein equations and Newton/PPN limits locally",
            "status_after_349": "conditional_not_proved",
            "promotion_allowed": "no",
        },
        {
            "dependency": "PPN residual vector",
            "role_in_GR_recovery": "checks gamma, beta, preferred-frame, clock, and WEP residuals",
            "status_after_349": "not_calculated_here",
            "promotion_allowed": "no",
        },
    ]


def gate_result_rows(sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources_ok = all(row["exists"] == "yes" for row in sources)
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if sources_ok else "fail",
            "evidence": "all cited post-checkpoint sources exist" if sources_ok else "one or more cited sources missing",
        },
        {
            "gate": "local_topological_no_bulk_stress",
            "status": "conditional_pass",
            "evidence": "348 supplies the local N5 theorem under metric-independent P_D",
        },
        {
            "gate": "FLRW_shape_from_same_projector",
            "status": "conditional_pass",
            "evidence": "same abstract P_D can reduce to FLRW coherent load shape if parent-owned",
        },
        {
            "gate": "parent_owns_P_D",
            "status": "fail",
            "evidence": "P_D is still a contract/skeleton object, not a derived Euler-Lagrange output",
        },
        {
            "gate": "same_operator_not_sidecar",
            "status": "conditional_pass",
            "evidence": "one pre-metric relative-chain projector can have local and FLRW representations",
        },
        {
            "gate": "Bmem_2over27_parent_derived",
            "status": "fail",
            "evidence": "dim=27, rank=2, and kappa_mem=1 remain closure debts after 343",
        },
        {
            "gate": "local_GR_or_PPN_promoted",
            "status": "fail",
            "evidence": "conditional projector silence is not yet a full GR/PPN theorem",
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
                "The local-GR route and the FLRW memory route can still be one framework if P_D is a pre-metric "
                "relative-chain projector selected by the parent action. In the local compact exterior it takes the "
                "topological/no-bulk-stress representation needed for N5. In the FLRW representation it gives the "
                "coherent scalar-load shape Q^i_j=X_FLRW delta^i_j and the cubic determinant exposure. This is a "
                "real compatibility bridge, not yet a derivation: the parent action does not yet select P_D, the "
                "B_mem=2/27 amplitude remains closure, and local GR/PPN is not promoted."
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
        "PD_limit_compatibility.csv": (
            pd_limit_rows(),
            ["limit", "required_specialization", "stress_or_projection_result", "status", "gap"],
        ),
        "same_operator_bridge.csv": (
            same_operator_bridge_rows(),
            ["bridge_condition", "why_it_is_not_patchwork", "current_status", "remaining_gap"],
        ),
        "amplitude_debt_register.csv": (
            amplitude_debt_rows(),
            ["object", "needed_for", "current_status", "why_not_derived", "next_derivation_attempt"],
        ),
        "local_GR_dependency_register.csv": (
            local_gr_dependency_rows(),
            ["dependency", "role_in_GR_recovery", "status_after_349", "promotion_allowed"],
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
        "same_operator_bridge": "conditional_pass",
        "local_topological_no_bulk_stress": "conditional_pass",
        "FLRW_shape_bridge": "conditional_pass",
        "parent_owns_P_D": False,
        "Bmem_2over27_parent_derived": False,
        "local_GR_or_PPN_promoted": False,
        "next_target": NEXT_TARGET,
    }
    write_json(run_dir / "status.json", payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build checkpoint 349: parent P_D / FLRW compatibility gate.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
