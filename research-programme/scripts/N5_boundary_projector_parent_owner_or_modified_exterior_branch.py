from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "N5-boundary-projector-parent-owner-or-modified-exterior-branch"
STATUS = (
    "N5_topological_projector_route_derived_as_conditional_contract_"
    "Hodge_projector_no_go_modified_exterior_fork_no_local_GR_promotion"
)
CLAIM_CEILING = "N5_contract_only_no_parent_action_or_PPN_promotion"
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
            ROOT / "245-exact-relative-memory-or-projector-stress-bianchi.md",
            "N4 exact relative memory and N5 Bianchi obligation",
            "defines why projector stress cannot be dropped",
        ),
        (
            ROOT / "248-projector-stress-zero-or-retained-theorem.md",
            "zero/retained projector stress fork",
            "establishes fake-drop versus retained-stress ledger",
        ),
        (
            ROOT / "249-projector-boundary-only-condition-or-metric-only-reduction-fail.md",
            "boundary-only condition attempt",
            "states why metric-only EH remains blocked",
        ),
        (
            ROOT / "250-local-GR-gate-scorecard-and-test-readiness.md",
            "local GR scorecard",
            "ranks N5 as sharpest metric-only blocker",
        ),
        (
            ROOT
            / "runs"
            / "20260601-000066-projector-boundary-only-condition-or-metric-only-reduction-fail"
            / "results"
            / "metric_only_reduction_verdict.csv",
            "249 metric-only verdict table",
            "machine-readable N5 blockage",
        ),
        (
            ROOT
            / "runs"
            / "20260601-000067-local-GR-gate-scorecard-and-test-readiness"
            / "results"
            / "local_GR_gate_scorecard.csv",
            "250 local GR scorecard",
            "machine-readable gate status",
        ),
    ]
    return [
        {
            "source": label,
            "path": relpath(path),
            "exists": "yes" if path.exists() else "no",
            "role": role,
            "use_in_251": use,
        }
        for path, label, use in sources
        for role in [label]
    ]


def variation_identity_rows() -> list[dict[str, Any]]:
    return [
        {
            "identity": "bulk_metric_variation_target",
            "statement": (
                "delta_g S_projector|on_shell = 1/2 int_E sqrt(-g) "
                "T_projector_mn delta g^mn + boundary"
            ),
            "derivation_use": "metric-only EH exterior requires T_projector_mn|bulk=0 or pure boundary support",
            "sufficient_condition": "bulk Euler derivative with respect to g^mn vanishes",
            "failure_mode": "bulk T_projector remains and exterior is not vacuum metric-only EH",
            "status": "derived_variational_gate",
        },
        {
            "identity": "projector_variation_chain_rule",
            "statement": (
                "delta_g L_projector includes (dL/dP_mem) delta_g P_mem, "
                "(dL/dJ_rel) delta_g J_rel, and any Hodge/measure/inner-product variation"
            ),
            "derivation_use": "isolates exactly where hidden stress enters",
            "sufficient_condition": "delta_g P_mem=0, delta_g J_rel=0 in exterior, and no bulk metric inner product",
            "failure_mode": "metric-dependent projection creates projector stress even when q_loc is exact",
            "status": "derived_chain_rule",
        },
        {
            "identity": "topological_projector_zero_stress",
            "statement": (
                "If P_mem is a metric-independent relative cohomology chain projector and "
                "L_projector=dB_projector in E, then delta_g S_projector|bulk=0"
            ),
            "derivation_use": "constructs the clean N5 closure route",
            "sufficient_condition": "P_mem commutes with d_rel and is independent of g under local exterior variations",
            "failure_mode": "parent action must own the topological projector; otherwise it is a closure axiom",
            "status": "conditional_sufficient_theorem",
        },
        {
            "identity": "hodge_projector_no_go",
            "statement": (
                "For a Hodge or orthogonal harmonic projector Pi_H(g), "
                "delta_g Pi_H generically contains Green-operator and delta_g Delta_g terms"
            ),
            "derivation_use": "rejects the tempting least-energy/local-orthogonal projector as a metric-only rescue",
            "sufficient_condition": "source sector annihilated, or projector never depends on Hodge star/Laplacian",
            "failure_mode": "bulk projector stress is generic and must be retained",
            "status": "no_go_for_generic_hodge_projector",
        },
        {
            "identity": "modified_exterior_fork",
            "statement": (
                "If T_projector_mn|bulk is retained, the exterior equation is "
                "G_mn+Lambda g_mn=8 pi G T_projector_mn, not vacuum EH"
            ),
            "derivation_use": "keeps Bianchi honest without pretending local GR has been derived",
            "sufficient_condition": "derive amplitude/profile and compare as proxy/PPN deformation",
            "failure_mode": "local beta/gamma claims become approximate-model claims, not GR-reduction claims",
            "status": "honest_fork_not_promotion",
        },
    ]


def projector_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch": "metric_independent_topological_relative_projector",
            "bulk_stress_result": "zero_if_exact_or_boundary_action",
            "metric_only_EH_effect": "can_continue_conditionally",
            "derivation_status": "sufficient_condition_derived_not_parent_implemented",
            "risk": "must prove this projector also supports cosmology/global memory",
            "next_action": "write parent action skeleton with P_mem as relative cohomology chain map",
        },
        {
            "branch": "Hodge_orthogonal_or_least_energy_projector",
            "bulk_stress_result": "generic_nonzero_delta_g_Pmem",
            "metric_only_EH_effect": "fails_metric_only_EH",
            "derivation_status": "generic_no_go",
            "risk": "can look natural mathematically but smuggles metric stress back into exterior",
            "next_action": "reject for local-GR derivation unless source annihilation theorem is proved",
        },
        {
            "branch": "algebraic_auxiliary_projector",
            "bulk_stress_result": "unknown_until_constraint_algebra_owned",
            "metric_only_EH_effect": "blocked_by_N6",
            "derivation_status": "not_enough",
            "risk": "rank-zero kinetics alone does not prove no stress",
            "next_action": "derive symplectic/bracket owner or keep as closure",
        },
        {
            "branch": "boundary_counterterm_cancellation",
            "bulk_stress_result": "zero_only_if_parent_variation_cancels_identically",
            "metric_only_EH_effect": "can_continue_only_if_not_tuned",
            "derivation_status": "conditional_but_dangerous",
            "risk": "looks like post-hoc cancellation unless symmetry/topology enforces it",
            "next_action": "only allow if cancellation follows from exact form or gauge redundancy",
        },
        {
            "branch": "retained_bulk_projector_stress",
            "bulk_stress_result": "nonzero_conserved_source",
            "metric_only_EH_effect": "modified_exterior_not_GR_reduction",
            "derivation_status": "honest_alternative",
            "risk": "must survive PPN/local-bound proxy pressure",
            "next_action": "derive radial profile and amplitude before official bound use",
        },
    ]


def topological_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_item": "C1_metric_independent_projector",
            "mathematical_statement": "delta_g P_mem|E=0 for compactly supported exterior metric variations",
            "why_needed": "removes projector-chain stress from the bulk metric equation",
            "verification_test": "vary metric while holding relative cohomology chain data fixed",
            "current_status": "required_parent_contract",
        },
        {
            "contract_item": "C2_chain_map",
            "mathematical_statement": "d_rel P_mem = P_mem d_rel on the exterior complex",
            "why_needed": "lets exact relative memory stay exact after projection",
            "verification_test": "compute d_rel(P_mem J_rel)-P_mem(d_rel J_rel)",
            "current_status": "required_parent_contract",
        },
        {
            "contract_item": "C3_boundary_or_exact_action",
            "mathematical_statement": "L_projector|E=dB_projector or has no bulk metric dependence",
            "why_needed": "turns projector sector into boundary data rather than a bulk source",
            "verification_test": "Euler derivative delta S_projector/delta g^mn vanishes in E",
            "current_status": "required_parent_contract",
        },
        {
            "contract_item": "C4_boundary_shear_silence",
            "mathematical_statement": "delta B_projector has no trace-free two-sphere stress on matching surfaces",
            "why_needed": "protects N2 gamma/slip result from boundary shear",
            "verification_test": "project boundary stress to TF angular sector",
            "current_status": "required_parent_contract",
        },
        {
            "contract_item": "C5_global_compatibility",
            "mathematical_statement": "same P_mem must reduce to the cosmology/BAO memory projector in FLRW limit",
            "why_needed": "prevents a separate local-only rule",
            "verification_test": "derive FLRW projection from the same chain-level action",
            "current_status": "open_unification_gate",
        },
    ]


def modified_exterior_rows() -> list[dict[str, Any]]:
    return [
        {
            "case": "T_projector_zero",
            "equation": "G_mn+Lambda g_mn=0 in E",
            "local_gr_status": "metric_only_EH_route_open_conditionally",
            "observable_risk": "none from projector bulk stress",
            "allowed_claim": "conditional theorem only",
        },
        {
            "case": "T_projector_boundary_only",
            "equation": "G_mn+Lambda g_mn=0 in E with boundary matching terms",
            "local_gr_status": "metric_only_EH_route_open_if_boundary_TF_silent",
            "observable_risk": "boundary shear or mass renormalization",
            "allowed_claim": "conditional theorem only",
        },
        {
            "case": "T_projector_proportional_to_constant_g",
            "equation": "G_mn+(Lambda-8piG rho_projector)g_mn=0",
            "local_gr_status": "renormalized_Lambda_branch_not_full_derivation",
            "observable_risk": "small locally but must be parent-derived",
            "allowed_claim": "possible modified-exterior branch",
        },
        {
            "case": "T_projector_radial_or_anisotropic",
            "equation": "G_mn+Lambda g_mn=8piG T_projector_mn(r)",
            "local_gr_status": "not_metric_only_GR",
            "observable_risk": "gamma, beta, G_eff, clock, and WEP proxy pressure",
            "allowed_claim": "closure/proxy testing only",
        },
    ]


def claim_policy_rows() -> list[dict[str, Any]]:
    return [
        {
            "claim": "N5 has a clean sufficient route",
            "status": "allowed_conditional",
            "reason": "topological relative projector plus exact/boundary action gives zero bulk stress",
        },
        {
            "claim": "N5 is fully derived for MTS now",
            "status": "forbidden",
            "reason": "parent action has not yet implemented and unified the topological projector",
        },
        {
            "claim": "Hodge/orthogonal projector solves local GR",
            "status": "forbidden",
            "reason": "generic metric variation creates bulk projector stress",
        },
        {
            "claim": "retained projector stress is fake or invalid",
            "status": "forbidden",
            "reason": "it is a valid modified-exterior fork if conserved and bounded",
        },
        {
            "claim": "local GR/PPN is promoted",
            "status": "forbidden",
            "reason": "N5 parent ownership, N6, and N1-N4 parent owners remain open",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    missing_sources = sum(row["exists"] != "yes" for row in source_register_rows())
    branch_rows = projector_branch_rows()
    topological_routes = sum(
        row["branch"] == "metric_independent_topological_relative_projector"
        and row["metric_only_EH_effect"] == "can_continue_conditionally"
        for row in branch_rows
    )
    hodge_no_go = sum(
        row["branch"] == "Hodge_orthogonal_or_least_energy_projector"
        and row["derivation_status"] == "generic_no_go"
        for row in branch_rows
    )
    return [
        {
            "gate": "all cited sources exist",
            "status": "pass" if missing_sources == 0 else "fail",
            "evidence": f"missing={missing_sources}",
            "promotion_allowed": "false",
        },
        {
            "gate": "topological projector route identified",
            "status": "pass" if topological_routes == 1 else "fail",
            "evidence": f"routes={topological_routes}",
            "promotion_allowed": "conditional only",
        },
        {
            "gate": "Hodge projector rejected as generic local rescue",
            "status": "pass" if hodge_no_go == 1 else "fail",
            "evidence": f"no_go_rows={hodge_no_go}",
            "promotion_allowed": "false",
        },
        {
            "gate": "modified exterior fork retained honestly",
            "status": "pass",
            "evidence": "bulk projector stress branch kept as non-GR-reduction alternative",
            "promotion_allowed": "proxy only",
        },
        {
            "gate": "local GR promoted",
            "status": "fail",
            "evidence": "parent action and N6 remain open",
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
                "N5 now has an exact sufficient route: the projector must be a metric-independent "
                "relative/topological chain projector and the projector action must be exact or "
                "boundary-only in the local exterior. A Hodge/orthogonal projector generically fails "
                "because its metric variation creates bulk projector stress. If bulk stress is retained, "
                "the branch becomes a modified exterior and cannot be sold as local-GR reduction."
            ),
            "promotion_allowed": "false",
            "local_GR_promoted": "false",
            "next_target": "252-topological-projector-parent-action-skeleton.md",
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
            ["source", "path", "exists", "role", "use_in_251"],
        ),
        "N5_variation_identities.csv": (
            variation_identity_rows(),
            ["identity", "statement", "derivation_use", "sufficient_condition", "failure_mode", "status"],
        ),
        "projector_branch_decision_table.csv": (
            projector_branch_rows(),
            [
                "branch",
                "bulk_stress_result",
                "metric_only_EH_effect",
                "derivation_status",
                "risk",
                "next_action",
            ],
        ),
        "topological_projector_contract.csv": (
            topological_contract_rows(),
            ["contract_item", "mathematical_statement", "why_needed", "verification_test", "current_status"],
        ),
        "modified_exterior_branch_implications.csv": (
            modified_exterior_rows(),
            ["case", "equation", "local_gr_status", "observable_risk", "allowed_claim"],
        ),
        "claim_policy_after_251.csv": (
            claim_policy_rows(),
            ["claim", "status", "reason"],
        ),
        "claim_gate_results.csv": (
            claim_gate_rows(),
            ["gate", "status", "evidence", "promotion_allowed"],
        ),
        "decision.csv": (
            decision_rows(),
            [
                "decision",
                "claim_ceiling",
                "lead_branch",
                "meaning",
                "promotion_allowed",
                "local_GR_promoted",
                "next_target",
            ],
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
        "topological_route_conditional": True,
        "hodge_projector_generic_no_go": True,
        "modified_exterior_fork_retained": True,
        "local_GR_promoted": False,
        "promotion_allowed": False,
        "next_target": "252-topological-projector-parent-action-skeleton.md",
    }
    write_json(run_dir / "status.json", status_payload)
    (run_dir / "DONE.txt").write_text(STATUS + "\n", encoding="utf-8")
    return status_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build checkpoint 251: N5 boundary/topological projector contract or modified exterior fork."
    )
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    payload = build_outputs(args.timestamp)
    print(json.dumps(payload, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
