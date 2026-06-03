from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "representative-invariant-matter-action-for-lifted-C"
STATUS = "representative_invariance_conditionally_selects_class_metric_direct_Cperp_vertices_forbidden_universality_and_class_selection_open"
CLAIM_CEILING = "conditional_matter_selector_theorem_only_no_WEP_clock_PPN_EH_or_local_GR_promotion"
NEXT_TARGET = "367-topological-class-selection-or-local-GR-closure-ledger.md"


SOURCE_DOCS = [
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "universal observed coframe contract and forbidden direct matter vertices",
    },
    {
        "path": "361-residual-gauge-principle-for-projected-matter-metric.md",
        "role": "quotient selector argument for exp(P_D C)g if Cperp is gauge/exact",
    },
    {
        "path": "362-Cperp-relative-exactness-or-projected-metric-closure-decision.md",
        "role": "scalar Cperp exactness failure and projected metric closure demotion",
    },
    {
        "path": "364-lifted-C-sector-form-holonomy-theorem-attempt.md",
        "role": "lifted 3-form class mechanism and local representative invisibility condition",
    },
    {
        "path": "365-lifted-C-boundary-primitive-and-domain-Euler-equation.md",
        "role": "boundary primitive derived inside fixed relative class admissibility",
    },
    {
        "path": "359-source-locked-PPN-residual-runner-from-derived-force-ledger.md",
        "role": "local WEP/clock/PPN residual guardrail context",
    },
]


SYMMETRY_CONTRACT = [
    {
        "object": "lifted_C_current",
        "representative_shift": "delta j_3 = d B_perp",
        "invariant": "fixed relative class Q_rel[D]",
        "matter_requirement": "matter cannot depend on j_3 representative data except through class observables",
    },
    {
        "object": "boundary_representative",
        "representative_shift": "delta b_2 = B_perp + d_boundary gamma_1",
        "invariant": "Q_rel[D] = int_D j_3 - int_boundaryD b_2",
        "matter_requirement": "matter cannot couple to b_2/B_perp as a local species-sensitive source",
    },
    {
        "object": "class_scalar",
        "representative_shift": "delta C_D = N_D^-1 int_boundaryD B_perp",
        "invariant": "delta C_D = 0 inside fixed relative class sectors",
        "matter_requirement": "matter may depend on C_D or P_D C as the lifted class observable",
    },
    {
        "object": "observed_coframe",
        "representative_shift": "delta ehat = 0 under lifted representative shifts",
        "invariant": "S_matter[psi,ehat] is representative invariant",
        "matter_requirement": "all species see one ehat and no direct non-geometric MTS arguments",
    },
]


MATTER_ACTION_CANDIDATES = [
    {
        "candidate": "raw_scalar_metric",
        "action_shape": "S_m[psi, exp(C) g]",
        "representative_invariant": "no",
        "verdict": "reject_as_lead",
        "reason": "matter trace sources scalar Cperp and reopens local representative force",
    },
    {
        "candidate": "class_metric",
        "action_shape": "S_m[psi, exp(C_D) g]",
        "representative_invariant": "conditional_yes",
        "verdict": "best_theorem_target",
        "reason": "if C_D is fixed-class invariant, direct Cperp/B_perp vertices vanish",
    },
    {
        "candidate": "arbitrary_universal_class_function",
        "action_shape": "S_m[psi, exp(F(C_D)) g]",
        "representative_invariant": "yes",
        "verdict": "allowed_but_underselects_metric_normalization",
        "reason": "representative invariance alone allows any universal F(C_D)",
    },
    {
        "candidate": "species_specific_class_function",
        "action_shape": "S_A[psi_A, exp(F_A(C_D)) g]",
        "representative_invariant": "yes_but_not_universal",
        "verdict": "reject_for_WEP_route",
        "reason": "species-specific F_A creates composition and clock residuals",
    },
    {
        "candidate": "direct_boundary_current_coupling",
        "action_shape": "S_m + int_boundary b_2 O_matter",
        "representative_invariant": "no_unless_O_is_constrained_topological_zero",
        "verdict": "reject_for_local_GR_route",
        "reason": "boundary representative becomes physical matter source",
    },
    {
        "candidate": "single_observed_coframe",
        "action_shape": "sum_A S_A[psi_A, ehat, omega[ehat], constants_A]",
        "representative_invariant": "conditional_yes",
        "verdict": "conditional_universal_coupling_theorem",
        "reason": "direct non-geometric MTS vertices are absent at fixed ehat",
    },
]


SELECTOR_DERIVATION = [
    {
        "step": 1,
        "statement": "Lifted C representative shifts are gauge/admissible inside a fixed relative class.",
        "equation": "delta_B j_3=dB_perp, delta_B b_2=B_perp+d_boundary gamma_1, delta_B Q_rel=0",
        "status": "conditional_from_365",
    },
    {
        "step": 2,
        "statement": "Matter observables must be invariant under unphysical representative changes.",
        "equation": "delta_B S_matter = 0",
        "status": "gauge_principle_assumption",
    },
    {
        "step": 3,
        "statement": "Local dependence on B_perp, b_2, or scalar Cperp violates representative invariance.",
        "equation": "delta S_matter / delta B_perp = delta S_matter / delta Cperp = 0",
        "status": "derived_selection_rule_if_symmetry_is_parent_owned",
    },
    {
        "step": 4,
        "statement": "Matter dependence descends to the quotient/class observable.",
        "equation": "S_matter = S_matter[psi, ehat(C_D,g)]",
        "status": "conditional_pass",
    },
    {
        "step": 5,
        "statement": "A universal observed coframe removes direct WEP/clock/species vertices.",
        "equation": "S_matter=sum_A S_A[psi_A, ehat, omega[ehat], constants_A]",
        "status": "conditional_from_360",
    },
    {
        "step": 6,
        "statement": "Representative invariance does not by itself choose physical class branches or species universality.",
        "equation": "C_D branch and common F(C_D) still require parent selection",
        "status": "open",
    },
]


EXPONENTIAL_COMPOSITION = [
    {
        "input": "class_additivity",
        "condition": "independent class contributions add: C12 = C1 + C2",
        "result": "metric scale should compose multiplicatively",
        "status": "theorem_assumption",
    },
    {
        "input": "multiplicative_metric_scale",
        "condition": "A(C1+C2)=A(C1)A(C2), A(0)=1, A continuous",
        "result": "A(C)=exp(lambda C)",
        "status": "derived_functional_form",
    },
    {
        "input": "normalization",
        "condition": "define C so lambda=1 or derive lambda from parent units",
        "result": "ghat_mn=exp(C_D) g_mn or exp(P_D C)g_mn",
        "status": "normalization_open",
    },
    {
        "input": "universal_species_response",
        "condition": "same A(C_D) for all matter sectors",
        "result": "no species-specific Weyl factor",
        "status": "required_not_parent_derived",
    },
]


RESIDUAL_IMPACT = [
    {
        "residual": "eta_WEP",
        "effect_if_theorem_holds": "direct representative/species vertices are forbidden",
        "still_open": "species universality and hidden F_A(C_D) exclusion need parent rule",
        "runner_policy": "do not mark WEP passed",
    },
    {
        "residual": "alpha_clock_redshift",
        "effect_if_theorem_holds": "direct Cperp clock vertex is absent",
        "still_open": "common-mode C_D/P_D C drift or gradient must be zero-derived or bounded",
        "runner_policy": "keep clock residual active",
    },
    {
        "residual": "gamma_minus_1",
        "effect_if_theorem_holds": "matter/photon representative mismatch is removed if they share ehat",
        "still_open": "EH exterior/operator and boundary residuals remain",
        "runner_policy": "keep PPN residual vector active",
    },
    {
        "residual": "delta_G_or_fifth_force",
        "effect_if_theorem_holds": "direct scalar/boundary representative fifth force is forbidden",
        "still_open": "class-changing events, bulk fields, and radial/domain forces remain open",
        "runner_policy": "quarantine until source-locked or theorem-zero",
    },
]


FAILURE_MODES = [
    {
        "failure": "matter_couples_to_representative",
        "meaning": "b_2, B_perp, scalar Cperp, or j_3 representative data appear in matter action",
        "consequence": "projected metric remains closure and local fifth-force/WEP risks return",
    },
    {
        "failure": "species_specific_class_metric",
        "meaning": "different species see different F_A(C_D)",
        "consequence": "representative invariance survives but WEP route fails",
    },
    {
        "failure": "arbitrary_universal_F",
        "meaning": "matter sees F(C_D), but F is not fixed by composition/normalization",
        "consequence": "metric selector is class-invariant but not fully derived",
    },
    {
        "failure": "physical_class_not_selected",
        "meaning": "local Q_rel=0 and FLRW nonzero branch are branch assignments, not equations",
        "consequence": "local silence remains conditional",
    },
    {
        "failure": "EH_operator_missing",
        "meaning": "even with matter selector, exterior gravitational operator is not proven EH",
        "consequence": "no local GR promotion",
    },
]


DECISION = [
    {
        "status": STATUS,
        "decision": "Representative invariance conditionally forces matter to ignore lifted C representative data and depend only on class observables, but universal species coupling, class selection, and normalization remain open.",
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "priority": 1,
        "target": NEXT_TARGET,
        "task": "attempt topological/discrete relative class selection after smooth boundary polarization underselected the representative",
        "pass_condition": "local Q_rel=0 and FLRW Q_rel nonzero are parent-selected without arbitrary smoothing scale",
    },
    {
        "priority": 2,
        "target": "368-common-mode-class-metric-clock-PPN-residual-gate.md",
        "task": "derive or bound common-mode C_D/P_D C local gradients after representative vertices are removed",
        "pass_condition": "clock/redshift and gamma residuals are theorem-zero or source-locked",
    },
    {
        "priority": 3,
        "target": "369-EH-exterior-reduction-after-lifted-C-and-matter-selector.md",
        "task": "reconnect the matter selector branch to the metric-only Einstein-Hilbert exterior operator gate",
        "pass_condition": "EH operator follows or the residual operator is explicitly retained and bounded",
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
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "exists": source_path.exists(),
                "role": source_doc["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": ";".join(missing_sources) if missing_sources else "all cited source paths exist",
        },
        {
            "gate": "lifted_C_representative_invariance_imported",
            "status": "conditional_pass",
            "evidence": "checkpoint 365 gives fixed-class representative admissibility",
        },
        {
            "gate": "matter_ignores_representative_data",
            "status": "conditional_pass",
            "evidence": "if representative shifts are gauge, S_matter must descend to C_D/P_D C",
        },
        {
            "gate": "raw_C_metric_rejected",
            "status": "pass",
            "evidence": "raw exp(C)g sources scalar Cperp through matter trace",
        },
        {
            "gate": "exponential_form_derived",
            "status": "conditional_pass",
            "evidence": "continuous multiplicative composition of additive class charge gives exp(lambda C_D)",
        },
        {
            "gate": "normalization_lambda_derived",
            "status": "fail",
            "evidence": "lambda can be absorbed by C definition unless parent amplitude/units fix it",
        },
        {
            "gate": "species_universality_parent_derived",
            "status": "fail",
            "evidence": "representative invariance alone permits species-specific F_A(C_D)",
        },
        {
            "gate": "physical_class_selection_derived",
            "status": "fail",
            "evidence": "local zero and FLRW nonzero classes remain branch assignments",
        },
        {
            "gate": "WEP_clock_PPN_or_local_GR_promoted",
            "status": "fail",
            "evidence": "common-mode gradients, class selection, and EH operator remain open",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "symmetry_contract.csv", SYMMETRY_CONTRACT)
    write_csv(results_dir / "matter_action_candidates.csv", MATTER_ACTION_CANDIDATES)
    write_csv(results_dir / "selector_derivation.csv", SELECTOR_DERIVATION)
    write_csv(results_dir / "exponential_composition.csv", EXPONENTIAL_COMPOSITION)
    write_csv(results_dir / "residual_impact.csv", RESIDUAL_IMPACT)
    write_csv(results_dir / "failure_modes.csv", FAILURE_MODES)
    write_csv(results_dir / "gate_results.csv", gate_rows(source_rows))
    write_csv(results_dir / "decision.csv", DECISION)
    write_csv(results_dir / "next_queue.csv", NEXT_QUEUE)

    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    status = {
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "run_dir": str(run_dir),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 366 representative-invariant matter action artifacts."
    )
    parser.add_argument(
        "--timestamp",
        default=datetime.now().strftime("%Y%m%d-%H%M%S"),
        help="Run timestamp prefix.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    run_dir = write_run(args.timestamp)
    print(json.dumps({"status": STATUS, "run_dir": str(run_dir)}, indent=2))


if __name__ == "__main__":
    main()
