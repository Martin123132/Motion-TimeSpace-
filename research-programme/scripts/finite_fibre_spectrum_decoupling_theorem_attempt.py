from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "finite-fibre-spectrum-decoupling-theorem-attempt"
CHECKPOINT_DOC = "421-finite-fibre-spectrum-decoupling-theorem-attempt.md"
STATUS = "finite_fibre_spectrum_decoupling_attempt_written_relabel_invariant_but_not_decoupled_no_local_GR_pass"
CLAIM_CEILING = "finite_fibre_spectrum_decoupling_attempt_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md"


SOURCE_DOCS = [
    {
        "path": "341-indistinguishable-cell-quotient-parent-action-gate.md",
        "role": "quotient finite-fibre class functions and marker-extension hazard",
    },
    {
        "path": "407-primitive-relational-quotient-action-sketch.md",
        "role": "basis-free finite fibre admitted but species/open matter-functor proof unresolved",
    },
    {
        "path": "410-quotient-matter-functor-theorem-attempt.md",
        "role": "quotient matter functor remains sufficient axiom, not parent-derived",
    },
    {
        "path": "413-no-marker-parent-action-theorem-attempt.md",
        "role": "quotient-invariant scalar and constant-sector counterexamples",
    },
    {
        "path": "414-local-quotient-invariant-algebra-triviality-gate.md",
        "role": "finite fibre listed as extra local invariant generator until integrated out or constant",
    },
    {
        "path": "420-relative-current-boundary-generator-theorem-attempt.md",
        "role": "candidate-domain generator still lacks physical representative selection",
    },
    {
        "path": "runs/20260602-052500-primitive-relational-quotient-action-sketch/results/configuration_space_sketch.csv",
        "role": "configuration object row for finite_cell_fibre",
    },
    {
        "path": "runs/20260602-064500-local-quotient-invariant-algebra-triviality-gate/results/invariant_generators.csv",
        "role": "finite fibre spectrum and species constants invariant-generator rows",
    },
    {
        "path": "runs/20260602-064500-local-quotient-invariant-algebra-triviality-gate/results/gate_results.csv",
        "role": "finite fibre decoupling and constant-sector gates",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 row states for no-promotion audit",
    },
]


FIBRE_OBSERVABLE_CLASSIFICATION = [
    {
        "observable": "basis_free_spectrum",
        "symbolic_form": "spec(h)",
        "quotient_status": "relabel_invariant",
        "local_marker_risk": "yes_if_nonuniversal_or_dynamic",
        "allowed_condition": "unique universal stationary spectrum or integrated-out constant",
        "row_risk": "R0;R1;R10",
        "verdict": "admissible_coordinate_not_decoupling_theorem",
    },
    {
        "observable": "trace_powers",
        "symbolic_form": "tr(h^n)",
        "quotient_status": "class_function",
        "local_marker_risk": "yes_if_local_values_or_gradients_remain",
        "allowed_condition": "all trace powers fixed to universal constants after variation",
        "row_risk": "R1;R2;R9;R10",
        "verdict": "extra_invariant_until_silenced",
    },
    {
        "observable": "trace_average",
        "symbolic_form": "tr(h)/N",
        "quotient_status": "class_function",
        "local_marker_risk": "yes_if_it_renormalizes_G_or_matter_nonuniversally",
        "allowed_condition": "single universal constant independent of source, clock, and domain",
        "row_risk": "R1;R2;R9",
        "verdict": "constant_candidate_only",
    },
    {
        "observable": "eigenvectors_or_cell_labels",
        "symbolic_form": "v_i(h), labelled cell index i",
        "quotient_status": "not_relabel_invariant",
        "local_marker_risk": "yes_active_marker_returns",
        "allowed_condition": "forbidden in parent bulk action",
        "row_risk": "R0;R1",
        "verdict": "rejected",
    },
    {
        "observable": "source_dependent_eigenvalues",
        "symbolic_form": "lambda_i(h;T_A,D,J_rel)",
        "quotient_status": "class_function_but_source_dependent",
        "local_marker_risk": "yes_WEP_and_fifth_force_channel",
        "allowed_condition": "must be proven absent by parent variation",
        "row_risk": "R1;R10",
        "verdict": "counterexample_until_blocked",
    },
    {
        "observable": "matter_functor_coefficients",
        "symbolic_form": "theta_A(spec(h)), q_A(tr(h^n)), m_A(h)",
        "quotient_status": "can_be_relabel_invariant",
        "local_marker_risk": "yes_species_charge_channel",
        "allowed_condition": "matter functor blind to h except universal constants",
        "row_risk": "R1;R2",
        "verdict": "requires_next_theorem",
    },
    {
        "observable": "readout_selected_component",
        "symbolic_form": "P_read h P_read or selected active block",
        "quotient_status": "observable_only_if_after_variation",
        "local_marker_risk": "yes_if_varied_as_reduced_action",
        "allowed_condition": "readout after parent variation with no backreaction",
        "row_risk": "R0;R1;R11",
        "verdict": "no_cheat_rule_needed",
    },
]


DECOUPLING_ROUTES = [
    {
        "route": "quotient_class_function_only",
        "claim": "The parent may depend on spec(h) or tr(h^n), not labels.",
        "status": "conditional_pass_as_admissibility",
        "failure": "quotient invariance does not by itself remove a local scalar marker",
    },
    {
        "route": "universal_stationary_spectrum",
        "claim": "delta S_parent/delta h=0 has h=h0 for every local source and domain.",
        "status": "not_derived",
        "failure": "no parent fibre potential or uniqueness theorem fixes h0",
    },
    {
        "route": "auxiliary_heavy_fibre_integrated_out",
        "claim": "h is nondynamical/heavy and integrating it out leaves only universal constants.",
        "status": "not_derived",
        "failure": "mass gap, Hessian sign, and source-independence not proven",
    },
    {
        "route": "pure_topological_or_trace_constant",
        "claim": "fibre contribution is metric-independent or a fixed trace constant.",
        "status": "conditional_only",
        "failure": "must prove no matter vertex and no metric variation residue",
    },
    {
        "route": "matter_functor_blindness",
        "claim": "S_matter[e,psi;h] reduces to S_matter[e,psi;constants].",
        "status": "not_derived",
        "failure": "species constants can still depend on quotient invariants",
    },
    {
        "route": "species_multiplet_fibre",
        "claim": "finite fibre represents physically distinct species labels.",
        "status": "rejected_for_local_GR_theorem",
        "failure": "reintroduces source-charge/WEP channel",
    },
    {
        "route": "empirical_fitted_fibre_spectrum",
        "claim": "choose spec(h) because it fits local/cosmological residuals.",
        "status": "forbidden_for_derivation",
        "failure": "posthoc fitted marker; allowed only as explicit phenomenological closure",
    },
]


CONDITIONAL_DECOUPLING_CHAIN = [
    {
        "step": 1,
        "claim": "The parent configuration contains only the quotient fibre [h].",
        "identity": "[h] = h/G_fibre, no labelled cell/eigenvector observable",
        "status": "conditional_admissibility",
    },
    {
        "step": 2,
        "claim": "The parent action is a class function of [h].",
        "identity": "S_parent = S_geom[e,Q] + S_fibre(spec(h),tr(h^n)) + no matter vertex",
        "status": "template_only",
    },
    {
        "step": 3,
        "claim": "The fibre Euler-Lagrange equation has a unique universal solution.",
        "identity": "delta S_parent/delta h = 0 implies [h]=[h0] independent of T_A,D,J_rel,e_obs jets",
        "status": "not_derived",
    },
    {
        "step": 4,
        "claim": "Local fibre fluctuations are nonpropagating or gapped.",
        "identity": "inverse Hessian response delta h/delta T_A = 0 or bounded below local-lock threshold",
        "status": "not_derived",
    },
    {
        "step": 5,
        "claim": "Substitution or path integration leaves constants only.",
        "identity": "S_eff[e,Q] = S_geom[e,Q; c_i(h0)] with c_i universal",
        "status": "not_derived",
    },
    {
        "step": 6,
        "claim": "The matter functor is blind to [h].",
        "identity": "delta S_matter/delta h = 0 after parent variation, except universal constants",
        "status": "not_derived",
    },
    {
        "step": 7,
        "claim": "The local invariant algebra reduces to geometry plus constants.",
        "identity": "I_loc(Q) = I_geom[J^k(e_obs)] tensor constants",
        "status": "conditional_target_not_proven",
    },
]


COUNTEREXAMPLE_FIBRE_COUPLINGS = [
    {
        "counterexample": "species_charge_from_trace",
        "symbolic_form": "q_A = q_A0 + epsilon_A tr(h)",
        "why_it_breaks": "WEP/source-charge channel survives while remaining quotient-invariant",
        "required_blocker": "constant-sector universality and matter-functor blindness",
    },
    {
        "counterexample": "finite_range_fibre_scalar",
        "symbolic_form": "L_h includes (partial h)^2 + m_h^2(h-h0)^2 + beta h T",
        "why_it_breaks": "fifth-force Yukawa mode appears unless beta=0 or m_h lock is derived",
        "required_blocker": "nonpropagating/gapped auxiliary theorem plus zero matter vertex",
    },
    {
        "counterexample": "source_dependent_stationary_spectrum",
        "symbolic_form": "h_star = h0 + M^{-2} T_A",
        "why_it_breaks": "local spectrum changes with material source, reopening marker dependence",
        "required_blocker": "source-independent Euler-Lagrange solution",
    },
    {
        "counterexample": "readout_selected_active_block",
        "symbolic_form": "P_active h P_active varied inside reduced action",
        "why_it_breaks": "the active-marker counterterm returns through the readout projector",
        "required_blocker": "readout-after-variation no-cheat theorem",
    },
    {
        "counterexample": "nonuniversal_constant_renormalization",
        "symbolic_form": "G_eff(A) = G0(1 + epsilon_A tr(h^2))",
        "why_it_breaks": "measured GM, clock, or species constants drift by sector",
        "required_blocker": "universal constants independent of A, D, and local state",
    },
    {
        "counterexample": "domain_coupled_spectrum",
        "symbolic_form": "lambda_i(h) = lambda_i(C_exp[D])",
        "why_it_breaks": "domain scoring leaks back into parent variables",
        "required_blocker": "candidate-before-score and no-backreaction rules",
    },
]


ROW_IDS = [
    "R0_identity_coframe_direct",
    "R1_WEP_source_charge",
    "R2_clock_redshift",
    "R5_alpha1",
    "R7_alpha3",
    "R9_Gdot",
    "R10_fifth_force",
    "R11_EH_operator_ledger",
]


DECISION = [
    {
        "decision": (
            "Finite fibre spectra/traces can be admitted as quotient/class-function parent coordinates, "
            "but this is not a decoupling theorem. A spectrum or trace invariant can still be a local "
            "matter-visible scalar unless the parent action proves a unique universal stationary spectrum, "
            "integrates the fibre out to universal constants, and makes the matter functor blind to h. "
            "Therefore finite fibre remains allowed only as a disciplined parent support or explicit closure; "
            "no WEP, EH, Newtonian, PPN, fifth-force, flux, domain, or local-GR row is promoted."
        )
    }
]


NEXT_QUEUE = [
    {
        "target": "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
        "reason": "the finite-fibre gate fails mainly because matter/readout couplings are not yet parent-owned",
    },
    {
        "target": "422-local-bounds-real-data-source-plan.md",
        "reason": "prepare verified local-bound source intake once the no-cheat branch is fenced",
    },
    {
        "target": "422-fibre-decoupling-retained-evaluator.md",
        "reason": "if blindness cannot be derived, quantify retained fibre coefficients instead of claiming theorem-zero",
    },
]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_doc in SOURCE_DOCS:
        source_path = ROOT / source_doc["path"]
        rows.append(
            {
                "source_file": source_doc["path"],
                "role": source_doc["role"],
                "exists": source_path.exists(),
            }
        )
    return rows


def runner_v4_rows() -> list[dict[str, str]]:
    return read_csv(ROOT / "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv")


def row_transition_rows() -> list[dict[str, Any]]:
    matrix_by_id = {row["row_id"]: row for row in runner_v4_rows()}
    reasons = {
        "R0_identity_coframe_direct": "finite-fibre quotient admissibility does not prove selector-blind matter or local invariant triviality",
        "R1_WEP_source_charge": "trace/spectrum-dependent species charge remains a quotient-invariant counterexample",
        "R2_clock_redshift": "clock constants can still depend on h unless universalized",
        "R5_alpha1": "domain/readout coupling to spectrum remains blocked but not derived away",
        "R7_alpha3": "boundary exchange coefficients unaffected by fibre admissibility",
        "R9_Gdot": "nonuniversal trace renormalization can mimic Gdot or measured-GM drift",
        "R10_fifth_force": "dynamic fibre scalar mode not excluded",
        "R11_EH_operator_ledger": "fibre decoupling does not select Einstein-Hilbert operator content",
    }
    rows: list[dict[str, Any]] = []
    for row_id in ROW_IDS:
        previous_state = matrix_by_id.get(row_id, {}).get("runner_v4_state", "missing")
        rows.append(
            {
                "row_id": row_id,
                "previous_state": previous_state,
                "new_state": previous_state,
                "result": "not_upgraded",
                "reason": reasons[row_id],
                "theorem_credit": False,
                "claim_allowed": False,
            }
        )
    return rows


def gate_rows(
    source_rows: list[dict[str, Any]],
    transition_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    missing_sources = [row for row in source_rows if not row["exists"]]
    theorem_rows = [row for row in transition_rows if row["theorem_credit"]]
    claim_rows = [row for row in transition_rows if row["claim_allowed"]]
    return [
        {
            "gate": "source_paths_exist",
            "status": "pass" if not missing_sources else "fail",
            "evidence": "all cited source paths exist" if not missing_sources else f"{len(missing_sources)} missing source paths",
        },
        {
            "gate": "fibre_observables_classified",
            "status": "pass",
            "evidence": f"{len(FIBRE_OBSERVABLE_CLASSIFICATION)} fibre observables classified",
        },
        {
            "gate": "relabel_invariant_class_functions_written",
            "status": "conditional_pass",
            "evidence": "spec(h), tr(h^n), and trace average are admissible class functions",
        },
        {
            "gate": "quotient_invariance_not_decoupling_guardrail",
            "status": "pass",
            "evidence": "class functions are explicitly denied theorem-zero credit without decoupling",
        },
        {
            "gate": "universal_stationary_spectrum_derived",
            "status": "fail",
            "evidence": "no parent fibre potential, uniqueness theorem, or source-independent h0 is derived",
        },
        {
            "gate": "fibre_integrated_out_to_universal_constants",
            "status": "fail",
            "evidence": "mass gap/Hessian/source-independence and constant-only effective action are not proven",
        },
        {
            "gate": "matter_functor_blindness_derived",
            "status": "fail",
            "evidence": "theta_A(spec(h)) and q_A(tr(h^n)) counterexamples remain open",
        },
        {
            "gate": "constant_sector_independence_derived",
            "status": "fail",
            "evidence": "species constants are not yet universalized against fibre invariants",
        },
        {
            "gate": "fifth_force_fibre_mode_excluded",
            "status": "fail",
            "evidence": "dynamic fibre scalar/Yukawa mode is not excluded by theorem",
        },
        {
            "gate": "runner_rows_promoted_to_theorem_zero",
            "status": "fail",
            "evidence": f"{len(theorem_rows)} theorem-credit row upgrades",
        },
        {
            "gate": "claim_leaks",
            "status": "pass" if not claim_rows else "fail",
            "evidence": f"{len(claim_rows)} claim-allowed rows",
        },
        {
            "gate": "local_GR_promoted",
            "status": "fail",
            "evidence": "finite-fibre decoupling attempt only; no local-GR pass",
        },
        {
            "gate": "claim_ceiling_enforced",
            "status": "pass",
            "evidence": CLAIM_CEILING,
        },
    ]


def md_cell(value: Any) -> str:
    return str(value).replace("|", ";")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(md_cell(row[column]) for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_checkpoint_markdown(
    run_dir: Path,
    transition_rows: list[dict[str, Any]],
    gate_result_rows: list[dict[str, Any]],
) -> None:
    fibre_table_rows = [
        {
            "observable": row["observable"],
            "quotient_status": row["quotient_status"],
            "local_marker_risk": row["local_marker_risk"],
            "verdict": row["verdict"],
        }
        for row in FIBRE_OBSERVABLE_CLASSIFICATION
    ]
    route_table_rows = [
        {
            "route": row["route"],
            "status": row["status"],
            "failure": row["failure"],
        }
        for row in DECOUPLING_ROUTES
    ]
    chain_table_rows = [
        {
            "step": row["step"],
            "claim": row["claim"],
            "status": row["status"],
        }
        for row in CONDITIONAL_DECOUPLING_CHAIN
    ]
    counterexample_table_rows = [
        {
            "counterexample": row["counterexample"],
            "why_it_breaks": row["why_it_breaks"],
            "required_blocker": row["required_blocker"],
        }
        for row in COUNTEREXAMPLE_FIBRE_COUPLINGS
    ]
    transition_table_rows = [
        {
            "row_id": row["row_id"],
            "previous_state": row["previous_state"],
            "new_state": row["new_state"],
            "result": row["result"],
        }
        for row in transition_rows
    ]
    gate_table_rows = [
        {
            "gate": row["gate"],
            "status": row["status"],
            "evidence": row["evidence"],
        }
        for row in gate_result_rows
    ]
    text = f"""# 421 - Finite-Fibre Spectrum Decoupling Theorem Attempt

Private finite-fibre/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 414 left `finite_cell_fibre_spectrum` as an extra local quotient-invariant generator. This checkpoint tests whether basis-free spectra and trace powers are merely harmless quotient data, or whether they still need a real decoupling theorem before the local GR branch can use them.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/finite_fibre_spectrum_decoupling_theorem_attempt.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Fibre Observable Classification

{markdown_table(fibre_table_rows, ["observable", "quotient_status", "local_marker_risk", "verdict"])}

## 4. Decoupling Routes

{markdown_table(route_table_rows, ["route", "status", "failure"])}

## 5. Conditional Decoupling Chain

{markdown_table(chain_table_rows, ["step", "claim", "status"])}

Exact theorem contract:

```text
If [h] is quotient-only, delta S_parent/delta h has the unique source-independent solution [h0],
local fibre fluctuations are nonpropagating or gapped, and S_matter is blind to [h] except universal constants,
then finite-fibre spectra/traces renormalize constants only and do not create local marker, WEP, clock, Gdot, or fifth-force rows.
```

## 6. Counterexample Fibre Couplings

{markdown_table(counterexample_table_rows, ["counterexample", "why_it_breaks", "required_blocker"])}

## 7. Row Transition Attempt

{markdown_table(transition_table_rows, ["row_id", "previous_state", "new_state", "result"])}

## 8. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 9. Decision

{DECISION[0]["decision"]}

Practical read: this is a useful narrowing, not a win-condition yet. The finite fibre is not automatically poison, but it is also not automatically silent. It can sit in the parent theory as basis-free support only if the next matter/readout theorem keeps it from becoming a local dial.

## 10. Next Target

`{NEXT_TARGET}`
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    transition_rows = row_transition_rows()
    gate_result_rows = gate_rows(source_rows, transition_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "fibre_observable_classification.csv", FIBRE_OBSERVABLE_CLASSIFICATION)
    write_csv(results_dir / "decoupling_routes.csv", DECOUPLING_ROUTES)
    write_csv(results_dir / "conditional_decoupling_chain.csv", CONDITIONAL_DECOUPLING_CHAIN)
    write_csv(results_dir / "counterexample_fibre_couplings.csv", COUNTEREXAMPLE_FIBRE_COUPLINGS)
    write_csv(results_dir / "row_transition_attempt.csv", transition_rows)
    write_csv(results_dir / "gate_results.csv", gate_result_rows)
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
        "fibre_observables_classified": len(FIBRE_OBSERVABLE_CLASSIFICATION),
        "relabel_invariant_class_functions_written": True,
        "universal_stationary_spectrum_derived": False,
        "fibre_integrated_out_to_universal_constants": False,
        "matter_functor_blindness_derived": False,
        "constant_sector_independence_derived": False,
        "fifth_force_fibre_mode_excluded": False,
        "theorem_zero_upgrades": 0,
        "claim_allowed_rows": 0,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, transition_rows, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 421 finite-fibre spectrum decoupling theorem attempt artifacts."
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
