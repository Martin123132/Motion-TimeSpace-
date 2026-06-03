from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "residual-gauge-principle-for-projected-matter-metric"
STATUS = "residual_gauge_selector_theorem_conditional_Cperp_exactness_still_open_projected_metric_not_promoted"
CLAIM_CEILING = "conditional_residual_gauge_selector_only_no_universal_coupling_WEP_or_local_GR_promotion"
NEXT_TARGET = "362-Cperp-relative-exactness-or-projected-metric-closure-decision.md"

RUN_360 = ROOT / "runs" / "20260601-191500-universal-matter-coupling-theorem-attempt"


SOURCE_DOCS = [
    {
        "path": "231-Jrel-cohomology-projector-or-local-EH-limit.md",
        "role": "relative cohomology exactness model for local memory currents",
    },
    {
        "path": "252-topological-projector-parent-action-skeleton.md",
        "role": "topological/relative projector parent-action skeleton",
    },
    {
        "path": "268-projected-matter-metric-parent-action-or-closure.md",
        "role": "projected matter metric action skeleton and Cperp source removal",
    },
    {
        "path": "269-metric-selector-principle-attempt.md",
        "role": "conditional selector theorem from residual representative invariance",
    },
    {
        "path": "272-quotient-configuration-principle-from-topological-projector.md",
        "role": "presymplectic quotient route for C/ker(P_D)",
    },
    {
        "path": "340-full-cell-equivalence-gauge-redundancy-gate.md",
        "role": "symmetry vs gauge-redundancy distinction and material-marker hazard",
    },
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "universal matter coupling theorem target and projected metric selector burden",
    },
    {
        "path": "runs/20260601-191500-universal-matter-coupling-theorem-attempt/results/theorem_axioms.csv",
        "role": "machine-readable universal coupling axiom status",
    },
]


GAUGE_SELECTOR_DERIVATION = [
    {
        "step": 1,
        "name": "C_decomposition",
        "statement": "C = C_D + Cperp with P_D Cperp = 0 and C_D = P_D C",
        "status": "definition_in_projected_metric_branch",
        "blocker": "P_D parent ownership still required",
    },
    {
        "step": 2,
        "name": "kernel_shift",
        "statement": "C -> C + eta_perp where P_D eta_perp = 0",
        "status": "candidate_gauge_transformation",
        "blocker": "must prove eta_perp is not a physical scalar perturbation",
    },
    {
        "step": 3,
        "name": "action_descent",
        "statement": "S_parent[C + eta_perp] = S_parent[C] + boundary for compact local domains",
        "status": "conditional_if_Cperp_relative_exact",
        "blocker": "C-sector relative exactness not parent-derived",
    },
    {
        "step": 4,
        "name": "presymplectic_null_direction",
        "statement": "Theta(eta_perp) is boundary/zero so Omega(eta_perp, delta)=0",
        "status": "conditional_from_topological_quotient_route",
        "blocker": "requires no local boundary charge/material marker for eta_perp",
    },
    {
        "step": 5,
        "name": "reduced_phase_space",
        "statement": "physical configurations are [C] = C/ker(P_D)",
        "status": "conditional_if_step_4_holds",
        "blocker": "not yet shown for the C-sector rather than J_rel analogy",
    },
    {
        "step": 6,
        "name": "matter_invariance",
        "statement": "F[C + eta_perp] = F[C] for any matter-visible conformal scalar F[C]",
        "status": "conditional_if_eta_perp_is_gauge",
        "blocker": "depends on parent gauge principle, not empirical convenience",
    },
    {
        "step": 7,
        "name": "projected_metric_selector",
        "statement": "coherent-limit locality fixes F[C] = P_D C, so ghat_munu = exp(P_D C) g_munu",
        "status": "conditional_selector_theorem",
        "blocker": "not promoted until Cperp gauge/exactness is derived",
    },
]


C_EXACTNESS_REQUIREMENTS = [
    {
        "requirement": "C_sector_class_valued",
        "needed_statement": "C is a representative of a topological/relative class, not an ordinary local scalar observable",
        "current_status": "not_derived",
        "failure_mode": "Cperp is physical scalar hair and projected metric becomes closure",
    },
    {
        "requirement": "relative_exact_kernel",
        "needed_statement": "every local Cperp residual can be written as d_rel alpha or a relative-trivial representative",
        "current_status": "analogy_to_Jrel_not_proof",
        "failure_mode": "kernel shift is not a gauge orbit",
    },
    {
        "requirement": "vanishing_local_boundary_primitive",
        "needed_statement": "the boundary primitive/charge associated with eta_perp vanishes in compact stationary local domains",
        "current_status": "contract",
        "failure_mode": "eta_perp carries physical boundary hair",
    },
    {
        "requirement": "presymplectic_degeneracy",
        "needed_statement": "Omega(eta_perp, delta)=0 on the constraint surface",
        "current_status": "conditional_if_exact_and_boundary_silent",
        "failure_mode": "Cperp has conjugate momentum and is physical",
    },
    {
        "requirement": "projector_covariance",
        "needed_statement": "P_D is a covariant/dynamical/topological parent object, not a fixed external nonlocal operation",
        "current_status": "conditional_from_P_D_route",
        "failure_mode": "selector breaks Ward closure or locality",
    },
    {
        "requirement": "no_material_marker",
        "needed_statement": "no material boundary marker, species label, or detector field transforms with eta_perp to make it physical",
        "current_status": "open_from_gauge_redundancy_gate",
        "failure_mode": "formal covariance hides physical marker coupling",
    },
    {
        "requirement": "FLRW_class_survives",
        "needed_statement": "local Cperp quotient does not quotient away the cosmological P_D C memory class",
        "current_status": "conditional_shape_only",
        "failure_mode": "local silence and cosmological memory use incompatible projectors",
    },
]


FORK_TABLE = [
    {
        "fork": "residual_gauge_exact_representative",
        "meaning": "Cperp is a null direction of the parent presymplectic form",
        "matter_metric_status": "exp(P_D C)g conditionally derived",
        "WEP_clock_status": "direct Cperp trace source removed by theorem",
        "verdict": "best_conditional_route",
    },
    {
        "fork": "ordinary_physical_scalar_Cperp",
        "meaning": "Cperp has local kinetic/symplectic support or source",
        "matter_metric_status": "exp(P_D C)g is an imposed closure",
        "WEP_clock_status": "raw Cperp residual must stay in runner or be screened by another theorem",
        "verdict": "demote_projected_metric",
    },
    {
        "fork": "fixed_external_projector",
        "meaning": "P_D is chosen outside the parent variation",
        "matter_metric_status": "nonlocal closure with fake Ward risk",
        "WEP_clock_status": "selector stress/conservation not owned",
        "verdict": "forbidden_for_promotion",
    },
    {
        "fork": "material_marker_covariant_projector",
        "meaning": "a physical marker transforms with the state and selects P_D C",
        "matter_metric_status": "formally covariant but physically marked",
        "WEP_clock_status": "marker couplings can reintroduce composition/clock residuals",
        "verdict": "closure_or_retained_residual",
    },
    {
        "fork": "relative_cohomology_local_only",
        "meaning": "local Cperp is exact but FLRW class survives",
        "matter_metric_status": "promising if same P_D owns local and cosmology limits",
        "WEP_clock_status": "direct local Cperp source removed; common-mode drift remains",
        "verdict": "live_but_needs_FLRW_compatibility",
    },
]


RESIDUAL_IMPACT = [
    {
        "residual": "eta_WEP",
        "if_gauge_principle_holds": "direct Cperp/species representative coupling forbidden",
        "if_gauge_principle_fails": "projected metric closure must retain WEP/species-charge residuals",
        "source_lock_status": "ready_2.8e-15",
    },
    {
        "residual": "alpha_clock_redshift",
        "if_gauge_principle_holds": "direct Cperp clock vertex absent; common P_D C drift still needs silence",
        "if_gauge_principle_fails": "clock sector can probe local residual representative",
        "source_lock_status": "ready_3.1e-5",
    },
    {
        "residual": "gamma_minus_1",
        "if_gauge_principle_holds": "matter/photon mismatch from Cperp representative removed",
        "if_gauge_principle_fails": "nonmetric light/matter residual remains possible",
        "source_lock_status": "ready_2.3e-5",
    },
    {
        "residual": "delta_G_or_fifth_force",
        "if_gauge_principle_holds": "direct representative fifth force reduced, but bulk/radial/domain channels remain",
        "if_gauge_principle_fails": "Cperp can be physical fifth-force hair",
        "source_lock_status": "quarantined",
    },
]


DECISION_MATRIX = [
    {
        "claim": "matter selector follows from residual gauge invariance",
        "status": "conditional_pass",
        "evidence": "if eta_perp is in ker(P_D) and is gauge, matter invariance forces dependence only on P_D C",
    },
    {
        "claim": "Cperp is proven gauge/exact in the parent theory",
        "status": "fail",
        "evidence": "C-sector class-valued action and relative exactness are not derived",
    },
    {
        "claim": "projected matter metric is now parent-derived",
        "status": "fail",
        "evidence": "selector theorem depends on the unproved Cperp gauge principle",
    },
    {
        "claim": "projected matter metric should be demoted immediately to dead closure",
        "status": "not_supported",
        "evidence": "topological/presymplectic quotient route remains coherent and precise",
    },
    {
        "claim": "projected matter metric remains a theorem target",
        "status": "pass",
        "evidence": "exact next burden is Cperp relative exactness / presymplectic degeneracy",
    },
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "try to derive Cperp relative exactness for the C-sector, not just by analogy with J_rel",
        "pass_condition": "Cperp = d_rel alpha or relative-trivial with vanishing local primitive and null presymplectic pairing",
    },
    {
        "priority": 2,
        "target": "362-common-mode-clock-redshift-silence-for-projected-metric.md",
        "task": "derive or bound local drift/gradient of the surviving common projected factor P_D C",
        "pass_condition": "common-mode clock/redshift residual is zero or source-locked below guardrail",
    },
    {
        "priority": 3,
        "target": "363-projected-metric-closure-ledger-if-Cperp-exactness-fails.md",
        "task": "if exactness fails, label exp(P_D C)g as explicit closure and keep WEP/clock residuals in runner",
        "pass_condition": "no local-GR claim uses projected metric as a theorem without the gauge principle",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for doc in SOURCE_DOCS:
        source_path = ROOT / doc["path"]
        rows.append(
            {
                "source_file": doc["path"],
                "exists": source_path.exists(),
                "role": doc["role"],
            }
        )
    return rows


def axiom_context_rows() -> list[dict[str, Any]]:
    path = RUN_360 / "results" / "theorem_axioms.csv"
    if not path.exists():
        return [{"source": str(path), "issue": "missing"}]
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return [
            {
                "axiom": row["axiom"],
                "status_before_361": row["status"],
                "relevance": row["if_missing"],
            }
            for row in csv.DictReader(handle)
            if row["axiom"] in {"U3_residual_representative_invariance", "U4_projected_metric_selector", "U6_owned_selector_stress", "U7_common_mode_local_silence"}
        ]


def gate_result_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing = [row["source_file"] for row in source_rows if not row["exists"]]
    open_requirements = sum(1 for row in C_EXACTNESS_REQUIREMENTS if row["current_status"] in {"not_derived", "contract", "open_from_gauge_redundancy_gate", "conditional_shape_only", "analogy_to_Jrel_not_proof"})
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing else "fail",
            "evidence": "all cited source files exist" if not missing else "; ".join(missing),
        },
        {
            "gate": "selector_derivation_written",
            "status": "pass",
            "evidence": f"{len(GAUGE_SELECTOR_DERIVATION)} derivation steps connect residual gauge invariance to exp(P_D C)g",
        },
        {
            "gate": "matter_invariance_implies_projected_metric",
            "status": "conditional_pass",
            "evidence": "if eta_perp is gauge, F[C+eta_perp]=F[C] forces F to descend to P_D C",
        },
        {
            "gate": "Cperp_exactness_parent_derived",
            "status": "fail",
            "evidence": "C-sector relative exactness/topological class status is not derived",
        },
        {
            "gate": "presymplectic_null_direction_derived",
            "status": "fail",
            "evidence": "requires Cperp exactness and vanishing boundary primitive",
        },
        {
            "gate": "projected_metric_promoted",
            "status": "fail",
            "evidence": f"{open_requirements} C-exactness/gauge requirements remain open or conditional",
        },
        {
            "gate": "projected_metric_demoted_to_dead_closure",
            "status": "fail",
            "evidence": "not demoted as dead; a precise topological/presymplectic route remains live",
        },
        {
            "gate": "WEP_clock_pass_claimed",
            "status": "fail",
            "evidence": "direct vertices are only conditionally removed; selector not parent-derived",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "matter selector, no-hair, EH operator, and PPN gates remain open",
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
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "selector_theorem": "conditional",
            "Cperp_exactness_parent_derived": False,
            "projected_metric_promoted": False,
            "projected_metric_demoted": False,
            "WEP_clock_pass_claimed": False,
            "local_GR_promoted": False,
            "main_result": "residual gauge invariance would select exp(P_D C)g, but Cperp exactness/presymplectic degeneracy remains the missing parent theorem",
            "next_target": NEXT_TARGET,
        }
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    run_dir = ROOT / "runs" / f"{args.timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    source_rows = source_register_rows()
    outputs = {
        "source_register.csv": source_rows,
        "axiom_context.csv": axiom_context_rows(),
        "gauge_selector_derivation.csv": GAUGE_SELECTOR_DERIVATION,
        "C_exactness_requirements.csv": C_EXACTNESS_REQUIREMENTS,
        "fork_table.csv": FORK_TABLE,
        "residual_impact.csv": RESIDUAL_IMPACT,
        "decision_matrix.csv": DECISION_MATRIX,
        "next_queue.csv": NEXT_QUEUE,
        "gate_results.csv": gate_result_rows(source_rows),
        "decision.csv": decision_rows(),
    }
    for name, rows in outputs.items():
        write_csv(results_dir / name, rows)

    status = {
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "generated": sorted(outputs),
        "source_paths_missing": sum(1 for row in source_rows if not row["exists"]),
        "selector_derivation_steps": len(GAUGE_SELECTOR_DERIVATION),
        "C_exactness_requirements": len(C_EXACTNESS_REQUIREMENTS),
        "selector_theorem": "conditional",
        "Cperp_exactness_parent_derived": False,
        "projected_metric_promoted": False,
        "projected_metric_demoted": False,
        "WEP_clock_pass_claimed": False,
        "local_GR_promoted": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text("done\n", encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
