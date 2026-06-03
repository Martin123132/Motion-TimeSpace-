from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "topological-projector-parent-action-skeleton"
STATUS = (
    "topological_projector_parent_skeleton_written_N5_action_route_conditional_"
    "FLRW_Bmem_and_N6_open_no_promotion"
)
CLAIM_CEILING = "parent_skeleton_only_no_Bmem_derivation_or_local_GR_promotion"
LEAD_BRANCH = "MTS_2over27_no_clock_u3quarter"


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
            "N4 exact relative memory",
            ROOT / "245-exact-relative-memory-or-projector-stress-bianchi.md",
            "relative exactness and Bianchi warning",
        ),
        (
            "N5 boundary/projector blockage",
            ROOT / "249-projector-boundary-only-condition-or-metric-only-reduction-fail.md",
            "pre-252 obstruction",
        ),
        (
            "local GR scorecard",
            ROOT / "250-local-GR-gate-scorecard-and-test-readiness.md",
            "N5 ranked as hard blocker",
        ),
        (
            "N5 topological route",
            ROOT / "251-N5-boundary-projector-parent-owner-or-modified-exterior-branch.md",
            "conditional topological projector mechanism",
        ),
        (
            "251 topological contract table",
            ROOT
            / "runs"
            / "20260601-000068-N5-boundary-projector-parent-owner-or-modified-exterior-branch"
            / "results"
            / "topological_projector_contract.csv",
            "machine-readable C1-C5 contract",
        ),
    ]
    return [
        {
            "source": source_name,
            "path": relpath(path),
            "exists": "yes" if path.exists() else "no",
            "use_in_252": use_in_252,
        }
        for source_name, path, use_in_252 in sources
    ]


def parent_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "term": "S_EH",
            "schematic_form": "int_M sqrt(-g)(R-2 Lambda)/(16 pi G)",
            "metric_dependence": "yes",
            "local_exterior_variation": "gives Einstein tensor",
            "role": "metric dynamics",
            "status": "standard_skeleton_term",
        },
        {
            "term": "S_matter_strict_coframe",
            "schematic_form": "S_matter[Omega_D e, matter] with partial_mu Omega_D=0 in local exterior",
            "metric_dependence": "through observed coframe only",
            "local_exterior_variation": "zero when T_matter|E=0",
            "role": "N3 direct matter/clock silence",
            "status": "conditional_from_240_242",
        },
        {
            "term": "S_rel_closure",
            "schematic_form": "int_M Xi wedge d_rel J_rel",
            "metric_dependence": "no Hodge star or metric inner product",
            "local_exterior_variation": "zero in bulk",
            "role": "enforces relative current closure",
            "status": "topological_skeleton_term",
        },
        {
            "term": "S_projection_exactness",
            "schematic_form": "int_M Upsilon wedge (P_D J_rel - d_rel A_rel)",
            "metric_dependence": "none if P_D is domain/topology induced",
            "local_exterior_variation": "zero in bulk",
            "role": "owns N4 exact projected memory",
            "status": "conditional_parent_owner",
        },
        {
            "term": "S_projector_operator_contract",
            "schematic_form": "operator constraints P_D^2=P_D and d_rel P_D=P_D d_rel",
            "metric_dependence": "none if P_D comes from relative chain data",
            "local_exterior_variation": "zero in bulk",
            "role": "owns N5 topological projector rather than Hodge projector",
            "status": "skeleton_contract_not_full_operator_quantization",
        },
        {
            "term": "S_boundary",
            "schematic_form": "int_boundary B_projector + GHY/matching terms",
            "metric_dependence": "boundary only",
            "local_exterior_variation": "allowed only if trace-free boundary shear vanishes",
            "role": "N2 compatibility and mass matching",
            "status": "open_boundary_shear_check",
        },
    ]


def metric_variation_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "sector": "EH",
            "bulk_delta_g": "nonzero",
            "contribution": "G_mn+Lambda g_mn",
            "condition_for_local_GR": "standard vacuum exterior equation",
            "status": "kept",
        },
        {
            "sector": "ordinary matter",
            "bulk_delta_g": "zero in exterior",
            "contribution": "T_matter_mn|E=0",
            "condition_for_local_GR": "compact exterior outside source",
            "status": "definition_pass",
        },
        {
            "sector": "relative closure BF term",
            "bulk_delta_g": "zero",
            "contribution": "none if wedge/topological only",
            "condition_for_local_GR": "no Hodge star, no sqrt(-g) potential, no metric inner product",
            "status": "conditional_pass",
        },
        {
            "sector": "projection exactness term",
            "bulk_delta_g": "zero only if delta_g P_D=0",
            "contribution": "none for topology-induced P_D",
            "condition_for_local_GR": "P_D must not be Hodge/orthogonal/least-energy",
            "status": "conditional_pass",
        },
        {
            "sector": "operator contract",
            "bulk_delta_g": "zero if operator is chain/topological data",
            "contribution": "none",
            "condition_for_local_GR": "operator constraints cannot be metric minimization equations",
            "status": "conditional_pass",
        },
        {
            "sector": "boundary terms",
            "bulk_delta_g": "zero",
            "contribution": "surface stress only",
            "condition_for_local_GR": "boundary trace-free angular stress vanishes",
            "status": "open_N2_boundary_owner",
        },
    ]


def flrw_compatibility_rows() -> list[dict[str, Any]]:
    return [
        {
            "requirement": "same_projector_object",
            "statement": "local P_D and FLRW memory projector must be reductions of one parent object",
            "current_result": "skeleton permits this but does not prove it",
            "risk": "otherwise local projector becomes a patch",
            "next_test": "derive FLRW reduction from domain/topological chain map",
        },
        {
            "requirement": "no_global_clock",
            "statement": "domain labels may organize reduction but must not become a physical global clock",
            "current_result": "skeleton can be written without a clock kinetic term",
            "risk": "clock sneaks back through gauge fixing",
            "next_test": "check gauge/domain variation and no-clock constraint",
        },
        {
            "requirement": "B_mem_2_over_27",
            "statement": "locked empirical closure must arise from an index, rank, or averaging theorem",
            "current_result": "not derived",
            "risk": "B_mem remains fitted/closure rather than parent-owned",
            "next_test": "attempt FLRW projection amplitude theorem",
        },
        {
            "requirement": "no_pair_ruler_sidecar",
            "statement": "pair-ruler half-kernel cannot be separate parent law",
            "current_result": "skeleton does not require it",
            "risk": "sidecar returns if FLRW amplitude fails",
            "next_test": "keep pair-ruler as closure-only unless derived from P_D",
        },
        {
            "requirement": "CMB_safety",
            "statement": "topological memory projection must not claim CMB pass before official perturbation bridge",
            "current_result": "unresolved",
            "risk": "overclaiming from background-only derivation",
            "next_test": "only after FLRW amplitude and perturbations are owned",
        },
    ]


def open_obligation_rows() -> list[dict[str, Any]]:
    return [
        {
            "obligation": "operator_locality",
            "why_it_matters": "P_D is an operator, not an ordinary scalar field",
            "current_status": "skeleton_only",
            "blocking_if_unresolved": "parent action may be formal rather than variationally complete",
            "next_action": "write finite-dimensional/domain-field realization or accept closure",
        },
        {
            "obligation": "N6_constraint_algebra",
            "why_it_matters": "auxiliary/topological fields must not add propagating local hair",
            "current_status": "open",
            "blocking_if_unresolved": "no local no-hair promotion",
            "next_action": "derive symplectic degeneracy and first-class constraints",
        },
        {
            "obligation": "boundary_shear",
            "why_it_matters": "boundary terms can reintroduce Phi-Psi or gamma slip",
            "current_status": "open",
            "blocking_if_unresolved": "N2 remains conditional",
            "next_action": "project S_boundary variation onto TF two-sphere sector",
        },
        {
            "obligation": "FLRW_projection_amplitude",
            "why_it_matters": "unification needs same mechanism in cosmology",
            "current_status": "open",
            "blocking_if_unresolved": "B_mem=2/27 remains closure",
            "next_action": "derive or reject topological index/averaging route",
        },
        {
            "obligation": "source_normalization",
            "why_it_matters": "M_eff and G_eff calibration must be parent-owned",
            "current_status": "open",
            "blocking_if_unresolved": "N1 remains conditional",
            "next_action": "connect Pi_M flux to matter source normalization",
        },
    ]


def claim_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "a minimal N5-compatible parent skeleton exists",
            "status": "allowed_conditional",
            "reason": "topological wedge/relative-chain terms have zero bulk metric variation if P_D is metric independent",
        },
        {
            "claim": "the parent action is complete",
            "status": "forbidden",
            "reason": "operator realization, N6, boundary shear, and FLRW amplitude are open",
        },
        {
            "claim": "B_mem=2/27 is derived",
            "status": "forbidden",
            "reason": "FLRW projection amplitude theorem has not been proved",
        },
        {
            "claim": "local GR/PPN is derived",
            "status": "forbidden",
            "reason": "skeleton is conditional and does not close N6/N1/N2/N3/N4 parent ownership",
        },
        {
            "claim": "this route is useless",
            "status": "not_supported",
            "reason": "it cleanly removes the N5 metric-variation obstruction if parent ownership is achieved",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    metric_pass_terms = sum(row["status"] == "conditional_pass" for row in metric_variation_ledger_rows())
    open_obligations = sum(row["current_status"] in {"open", "skeleton_only"} for row in open_obligation_rows())
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "promotion_allowed": "false",
        },
        {
            "gate": "N5-compatible topological action terms written",
            "status": "pass",
            "evidence": f"parent_terms={len(parent_action_rows())}",
            "promotion_allowed": "conditional only",
        },
        {
            "gate": "bulk metric variation silenced for topological sectors",
            "status": "pass" if metric_pass_terms >= 3 else "fail",
            "evidence": f"conditional_pass_terms={metric_pass_terms}",
            "promotion_allowed": "conditional only",
        },
        {
            "gate": "open obligations remain explicit",
            "status": "pass" if open_obligations >= 4 else "fail",
            "evidence": f"open_obligations={open_obligations}",
            "promotion_allowed": "false",
        },
        {
            "gate": "B_mem or local GR promoted",
            "status": "fail",
            "evidence": "FLRW amplitude and N6 remain open",
            "promotion_allowed": "false",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "lead_branch": LEAD_BRANCH,
            "meaning": (
                "A minimal parent-action skeleton can own the N5 topological projector route: "
                "use relative closure and projection-exactness terms built from wedge products and "
                "a metric-independent domain/topology-induced chain projector P_D. This conditionally "
                "kills bulk projector stress. It does not derive B_mem=2/27, N6 no-hair, boundary shear "
                "silence, or the full local-GR/PPN branch."
            ),
            "promotion_allowed": "false",
            "next_target": "253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md",
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
            ["source", "path", "exists", "use_in_252"],
        ),
        "parent_action_skeleton_terms.csv": (
            parent_action_rows(),
            [
                "term",
                "schematic_form",
                "metric_dependence",
                "local_exterior_variation",
                "role",
                "status",
            ],
        ),
        "metric_variation_ledger.csv": (
            metric_variation_ledger_rows(),
            ["sector", "bulk_delta_g", "contribution", "condition_for_local_GR", "status"],
        ),
        "FLRW_compatibility_requirements.csv": (
            flrw_compatibility_rows(),
            ["requirement", "statement", "current_result", "risk", "next_test"],
        ),
        "open_parent_obligations.csv": (
            open_obligation_rows(),
            ["obligation", "why_it_matters", "current_status", "blocking_if_unresolved", "next_action"],
        ),
        "claim_policy_after_252.csv": (
            claim_policy_rows(),
            ["claim", "status", "reason"],
        ),
        "claim_gate_results.csv": (
            claim_gate_rows(),
            ["gate", "status", "evidence", "promotion_allowed"],
        ),
        "decision.csv": (
            decision_rows(),
            ["decision", "claim_ceiling", "lead_branch", "meaning", "promotion_allowed", "next_target"],
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
        "N5_action_route_conditional": True,
        "bulk_projector_stress_silenced_conditionally": True,
        "B_mem_derived": False,
        "N6_closed": False,
        "local_GR_promoted": False,
        "promotion_allowed": False,
        "next_target": "253-FLRW-reduction-of-topological-projector-or-Bmem-stays-closure.md",
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return status_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build checkpoint 252: topological projector parent-action skeleton.")
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
