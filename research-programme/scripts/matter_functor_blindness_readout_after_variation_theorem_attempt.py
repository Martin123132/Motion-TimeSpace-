from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "matter-functor-blindness-readout-after-variation-theorem-attempt"
CHECKPOINT_DOC = "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md"
STATUS = "matter_functor_blindness_readout_after_variation_attempt_written_exact_no_cheat_contract_but_parent_factorization_not_derived_no_local_GR_pass"
CLAIM_CEILING = "matter_functor_blindness_readout_after_variation_attempt_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "423-parent-action-minimality-no-extension-theorem-attempt.md"


SOURCE_DOCS = [
    {
        "path": "404-selector-blind-matter-axiom-origin.md",
        "role": "primitive-origin audit identifying relational quotient/readout as best candidate",
    },
    {
        "path": "407-primitive-relational-quotient-action-sketch.md",
        "role": "parent action sketch with S_matter quotient functor and S_readout observables blocks",
    },
    {
        "path": "410-quotient-matter-functor-theorem-attempt.md",
        "role": "conditional chain-rule theorem for selector-blind matter",
    },
    {
        "path": "413-no-marker-parent-action-theorem-attempt.md",
        "role": "marker and post-readout EFT counterexamples",
    },
    {
        "path": "414-local-quotient-invariant-algebra-triviality-gate.md",
        "role": "local invariant algebra and readout projector no-cheat debts",
    },
    {
        "path": "421-finite-fibre-spectrum-decoupling-theorem-attempt.md",
        "role": "finite-fibre spectra require matter/readout blindness to avoid local dials",
    },
    {
        "path": "204-matter-metric-action-and-ruler-transport-owner-contract.md",
        "role": "universal matter metric action candidate and non-universal matter source hazard",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source and measured-GM source-charge debts",
    },
    {
        "path": "412-v4-source-charge-channel-map-review.md",
        "role": "R1 source-charge channel guardrail",
    },
    {
        "path": "runs/20260602-051500-local-runner-v4-derived-vs-closure-queue/results/runner_v4_matrix.csv",
        "role": "runner-v4 row states for no-promotion audit",
    },
    {
        "path": "runs/20260602-064500-local-quotient-invariant-algebra-triviality-gate/results/invariant_generators.csv",
        "role": "extra local quotient-invariant generators that matter must not see",
    },
    {
        "path": "runs/20260602-075500-finite-fibre-spectrum-decoupling-theorem-attempt/results/fibre_observable_classification.csv",
        "role": "finite-fibre observables whose matter/readout leakage must be blocked",
    },
]


BLINDNESS_REQUIREMENTS = [
    {
        "requirement": "parent_quotient_object",
        "symbolic_form": "Q in Conf/G_rel, with representative variables Z_I in ker Obs",
        "status": "sketched_not_derived",
        "failure_if_missing": "selectors can become material coordinates",
        "rows_at_risk": "R0;R1",
    },
    {
        "requirement": "observed_geometry_functor",
        "symbolic_form": "Obs(Q)=e_obs or g_obs, natural under quotient representatives",
        "status": "conditional_template",
        "failure_if_missing": "matter can see more than one coframe/metric",
        "rows_at_risk": "R0;R3;R4",
    },
    {
        "requirement": "matter_factorization",
        "symbolic_form": "S_matter=sum_A S_A[Psi_A, Obs(Q), omega[Obs(Q)], theta_A]",
        "status": "sufficient_axiom_not_parent_derived",
        "failure_if_missing": "hidden selector/fibre/domain dependence enters matter",
        "rows_at_risk": "R0;R1;R2;R10",
    },
    {
        "requirement": "constant_sector_universality",
        "symbolic_form": "partial_Z theta_A = partial_h theta_A = partial_IQ theta_A = 0, theta_A universal",
        "status": "not_derived",
        "failure_if_missing": "species charges and clock constants become marker channels",
        "rows_at_risk": "R1;R2;R9",
    },
    {
        "requirement": "finite_fibre_blindness",
        "symbolic_form": "delta S_matter/delta h = 0 except universal constants after h -> h0",
        "status": "not_derived",
        "failure_if_missing": "spec(h) or tr(h^n) becomes a local dial",
        "rows_at_risk": "R1;R10",
    },
    {
        "requirement": "readout_after_variation",
        "symbolic_form": "solve delta S_parent=0 first, then apply R_read: Sol(S)->Obs",
        "status": "conditional_no_cheat_rule",
        "failure_if_missing": "P_read or P_active can be varied as a reduced EFT marker",
        "rows_at_risk": "R0;R1;R11",
    },
    {
        "requirement": "no_reduced_EFT_backreaction",
        "symbolic_form": "delta S_parent/delta P_read = 0 because P_read not in parent action",
        "status": "not_parent_formalized",
        "failure_if_missing": "readout projection can alter equations while looking observational",
        "rows_at_risk": "R0;R5;R11",
    },
    {
        "requirement": "same_frame_source_pair",
        "symbolic_form": "matter stress T_munu = -2/sqrt(-g_obs) delta S_matter/delta g_obs^munu",
        "status": "conditional_separate_EH_source_debt",
        "failure_if_missing": "even blind matter may source a different frame than the EH operator",
        "rows_at_risk": "R3;R4;R9;R11",
    },
]


VARIATION_ORDER_CONTRACT = [
    {
        "stage": 1,
        "operation": "define_parent_configuration",
        "allowed_objects": "Q, e_obs=Obs(Q), h if quotient-only, boundary/domain topological classes",
        "forbidden_objects": "P_read, P_active, fitted selector masks, material marker extensions",
        "status": "contract_written",
    },
    {
        "stage": 2,
        "operation": "vary_parent_action",
        "allowed_objects": "delta S_parent/delta Q, delta S_parent/delta h, delta S_matter/delta Obs(Q)",
        "forbidden_objects": "variation of readout-selected reduced blocks",
        "status": "not_fully_formalized",
    },
    {
        "stage": 3,
        "operation": "solve_or_integrate_auxiliary_sectors",
        "allowed_objects": "h -> h0 only if unique, universal, source-independent",
        "forbidden_objects": "source-dependent spectrum, local h gradients, fitted h residuals",
        "status": "not_derived",
    },
    {
        "stage": 4,
        "operation": "construct_observables",
        "allowed_objects": "R_read[solution], comparison with instruments/data",
        "forbidden_objects": "feeding readout projector back into S_parent",
        "status": "conditional_rule",
    },
    {
        "stage": 5,
        "operation": "run_local_bounds",
        "allowed_objects": "retained coefficients, theorem-zero rows, closure rows separated",
        "forbidden_objects": "using closure-zero as theorem-zero",
        "status": "runner_v4_guardrail",
    },
]


CONDITIONAL_THEOREM_CHAIN = [
    {
        "step": 1,
        "claim": "Selectors and cell labels are representative variables, not matter-visible fields.",
        "identity": "Z_I in ker Obs and fixed labels removed by quotient action",
        "status": "conditional_from_strict_quotient",
    },
    {
        "step": 2,
        "claim": "Matter factors only through observed geometry.",
        "identity": "S_matter[Psi,Q] = S_matter[Psi,Obs(Q),theta]",
        "status": "sufficient_if_assumed",
    },
    {
        "step": 3,
        "claim": "Constants are universal and independent of extra quotient invariants.",
        "identity": "partial_Z theta_A = partial_h theta_A = partial_IQ theta_A = 0",
        "status": "not_derived",
    },
    {
        "step": 4,
        "claim": "Finite-fibre spectra are either absent from matter or reduced to universal constants.",
        "identity": "delta S_matter/delta h = 0 after h -> h0",
        "status": "not_derived",
    },
    {
        "step": 5,
        "claim": "Readout happens after solving parent equations.",
        "identity": "R_read: Sol(S_parent)->Obs, not an argument of S_parent",
        "status": "conditional_no_cheat_contract",
    },
    {
        "step": 6,
        "claim": "Direct selector pullback vanishes by chain rule.",
        "identity": "delta S_matter/delta Z_I = (delta S_matter/delta Obs)(partial_ZI Obs) + partial_ZI theta terms = 0",
        "status": "conditional_theorem_shape",
    },
    {
        "step": 7,
        "claim": "No local WEP/source/clock/fifth-force channel is generated by hidden matter/readout dependence.",
        "identity": "q_A(Z,h,I_Q)=q_A0, m_A(Z,h,I_Q)=m_A0, beta_h=0, P_read not varied",
        "status": "not_parent_derived",
    },
]


COUNTEREXAMPLE_LEAKS = [
    {
        "counterexample": "selector_dependent_matter_metric",
        "symbolic_form": "g_matter = exp(F(Z_I)) g_obs",
        "damage": "direct coframe/WEP pullback returns while preserving a common-looking metric form",
        "required_blocker": "Obs-kernel proof plus matter factorization",
    },
    {
        "counterexample": "species_constants_depend_on_fibre",
        "symbolic_form": "theta_A = theta_A0 + epsilon_A tr(h)",
        "damage": "source-charge and clock rows survive through universal-looking quotient invariants",
        "required_blocker": "constant-sector universality",
    },
    {
        "counterexample": "post_readout_EFT_action",
        "symbolic_form": "S_red[P_read Q] varied instead of S_parent[Q]",
        "damage": "closure-zero can be mistaken for theorem-zero",
        "required_blocker": "readout-after-variation theorem",
    },
    {
        "counterexample": "active_block_material_marker",
        "symbolic_form": "Q_tilde=(Q,m_active)/G_rel",
        "damage": "fixed label is gone but material marker extension remains legal",
        "required_blocker": "parent minimality/no-extension theorem",
    },
    {
        "counterexample": "domain_scored_matter_coupling",
        "symbolic_form": "S_matter includes lambda(C_exp[D]) T",
        "damage": "posthoc domain scoring becomes a physical source",
        "required_blocker": "candidate-before-score and no-backreaction rules",
    },
    {
        "counterexample": "different_EH_and_matter_frames",
        "symbolic_form": "S_EH[g] + S_matter[tilde_g]",
        "damage": "blind matter is still not Newton/GR if source and EH operator are in different frames",
        "required_blocker": "same-frame EH/source theorem",
    },
    {
        "counterexample": "dynamic_fibre_matter_vertex",
        "symbolic_form": "beta h T or beta partial_mu h J^mu_A",
        "damage": "finite-range fifth force or composition-dependent force appears",
        "required_blocker": "zero matter vertex or gapped auxiliary proof",
    },
]


FINITE_FIBRE_IMPACT = [
    {
        "fibre_issue": "basis_free_spectrum",
        "blindness_result": "safe_only_if_matter_never_couples_to_spec_h",
        "current_status": "not_derived",
        "runner_effect": "R1 and R10 retained",
    },
    {
        "fibre_issue": "trace_powers",
        "blindness_result": "safe_only_if_trace_powers_are_universal_constants",
        "current_status": "not_derived",
        "runner_effect": "R1/R2/R9 retained",
    },
    {
        "fibre_issue": "readout_selected_component",
        "blindness_result": "safe_only_if_readout_is_after_variation",
        "current_status": "conditional_no_cheat_rule",
        "runner_effect": "R0/R11 not promoted",
    },
    {
        "fibre_issue": "source_dependent_eigenvalues",
        "blindness_result": "rejected_unless_parent_EL_forces_source_independent_h0",
        "current_status": "not_derived",
        "runner_effect": "R1/R10 retained",
    },
]


ROW_IDS = [
    "R0_identity_coframe_direct",
    "R1_WEP_source_charge",
    "R2_clock_redshift",
    "R3_gamma",
    "R4_beta",
    "R5_alpha1",
    "R7_alpha3",
    "R9_Gdot",
    "R10_fifth_force",
    "R11_EH_operator_ledger",
]


DECISION = [
    {
        "decision": (
            "The matter/readout route now has an exact no-cheat contract: vary the parent quotient action first, "
            "derive matter factorization through Obs(Q), require selector/fibre/class-independent universal constants, "
            "integrate or fix finite fibre to universal constants, and apply readout only on the solution space. "
            "Under those assumptions the direct matter selector derivative vanishes by the chain rule and the readout "
            "projector cannot act as a parent source. But the current corpus still does not derive parent factorization, "
            "constant-sector universality, finite-fibre blindness, no material marker extension, or same-frame EH/source. "
            "Therefore this checkpoint is a precise theorem contract, not a local-GR/Newton derivation, and no runner row is promoted."
        )
    }
]


NEXT_QUEUE = [
    {
        "target": "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "reason": "matter/readout blindness fails mostly because material marker and reduced-EFT extensions remain legal",
    },
    {
        "target": "423-same-frame-EH-source-Poisson-reduction-gate.md",
        "reason": "even blind matter must source the same frame whose EH operator gives the Newtonian limit",
    },
    {
        "target": "423-local-bound-real-data-source-plan.md",
        "reason": "prepare local-bound tests with closure/theorem/retained labels kept separate",
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
        "R0_identity_coframe_direct": "chain-rule zero is conditional; parent factorization/readout-after-variation not derived",
        "R1_WEP_source_charge": "species constants can still depend on fibre/class/marker invariants",
        "R2_clock_redshift": "clock constants and matter metric factors are not universalized",
        "R3_gamma": "same-frame EH/source and non-EH slip operator selection remain separate",
        "R4_beta": "source normalization and nonlinear source hair remain open",
        "R5_alpha1": "domain/readout projector no-backreaction is a contract, not a theorem",
        "R7_alpha3": "boundary/Ward exchange ownership is unaffected by matter blindness contract",
        "R9_Gdot": "measured-GM drift and constant-sector time dependence remain retained",
        "R10_fifth_force": "dynamic fibre or marker matter vertices are not excluded",
        "R11_EH_operator_ledger": "readout discipline does not select EH operator content",
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
            "gate": "blindness_requirements_written",
            "status": "pass",
            "evidence": f"{len(BLINDNESS_REQUIREMENTS)} requirements recorded",
        },
        {
            "gate": "variation_order_contract_written",
            "status": "pass",
            "evidence": f"{len(VARIATION_ORDER_CONTRACT)} variation stages recorded",
        },
        {
            "gate": "conditional_chain_rule_zero_written",
            "status": "conditional_pass",
            "evidence": "delta S_matter/delta Z_I = 0 follows only if factorization and constant blindness hold",
        },
        {
            "gate": "readout_after_variation_contract_written",
            "status": "conditional_pass",
            "evidence": "R_read: Sol(S_parent)->Obs is stated as no-cheat rule",
        },
        {
            "gate": "parent_factorization_derived",
            "status": "fail",
            "evidence": "S_matter quotient functor remains sufficient axiom, not parent derivation",
        },
        {
            "gate": "constant_sector_universality_derived",
            "status": "fail",
            "evidence": "theta_A(Z,h,I_Q) counterexamples remain legal",
        },
        {
            "gate": "finite_fibre_blindness_derived",
            "status": "fail",
            "evidence": "spec(h)/tr(h^n) matter coupling is not ruled out by parent action",
        },
        {
            "gate": "material_marker_extension_blocked",
            "status": "fail",
            "evidence": "Q_tilde=(Q,m_active)/G_rel remains legal without no-extension theorem",
        },
        {
            "gate": "same_frame_EH_source_derived",
            "status": "fail",
            "evidence": "matter blindness does not by itself prove EH operator/source frame identity",
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
            "evidence": "matter/readout no-cheat contract only; no local-GR/Newton pass",
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
    requirement_table_rows = [
        {
            "requirement": row["requirement"],
            "status": row["status"],
            "failure_if_missing": row["failure_if_missing"],
            "rows_at_risk": row["rows_at_risk"],
        }
        for row in BLINDNESS_REQUIREMENTS
    ]
    variation_table_rows = [
        {
            "stage": row["stage"],
            "operation": row["operation"],
            "status": row["status"],
            "forbidden_objects": row["forbidden_objects"],
        }
        for row in VARIATION_ORDER_CONTRACT
    ]
    chain_table_rows = [
        {
            "step": row["step"],
            "claim": row["claim"],
            "status": row["status"],
        }
        for row in CONDITIONAL_THEOREM_CHAIN
    ]
    leak_table_rows = [
        {
            "counterexample": row["counterexample"],
            "damage": row["damage"],
            "required_blocker": row["required_blocker"],
        }
        for row in COUNTEREXAMPLE_LEAKS
    ]
    fibre_table_rows = [
        {
            "fibre_issue": row["fibre_issue"],
            "blindness_result": row["blindness_result"],
            "current_status": row["current_status"],
            "runner_effect": row["runner_effect"],
        }
        for row in FINITE_FIBRE_IMPACT
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
    text = f"""# 422 - Matter-Functor Blindness and Readout-After-Variation Theorem Attempt

Private matter/readout/local-GR checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 421 showed that finite-fibre spectra are not automatically silent. This checkpoint attacks the real loophole: can matter be forced to see only observed geometry plus universal constants, with all readout projectors applied after parent variation?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/matter_functor_blindness_readout_after_variation_theorem_attempt.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Blindness Requirements

{markdown_table(requirement_table_rows, ["requirement", "status", "failure_if_missing", "rows_at_risk"])}

## 4. Variation-Order Contract

{markdown_table(variation_table_rows, ["stage", "operation", "status", "forbidden_objects"])}

## 5. Conditional Theorem Chain

{markdown_table(chain_table_rows, ["step", "claim", "status"])}

Exact no-cheat theorem shape:

```text
Let Z_I be representative selectors with partial_ZI Obs(Q)=0.
If S_matter factors only through Obs(Q) and universal constants theta_A,
if partial_ZI theta_A = partial_h theta_A = partial_IQ theta_A = 0,
if finite fibre h is absent from matter or reduced to a universal h0,
and if readout R_read is defined only on Sol(S_parent),
then delta S_matter/delta Z_I = 0 and delta S_parent/delta P_read = 0.
```

This is a valid conditional theorem shape. It is not yet a derived parent-action theorem.

## 6. Counterexample Leaks

{markdown_table(leak_table_rows, ["counterexample", "damage", "required_blocker"])}

## 7. Finite-Fibre Impact

{markdown_table(fibre_table_rows, ["fibre_issue", "blindness_result", "current_status", "runner_effect"])}

## 8. Row Transition Attempt

{markdown_table(transition_table_rows, ["row_id", "previous_state", "new_state", "result"])}

## 9. Gate Results

{markdown_table(gate_table_rows, ["gate", "status", "evidence"])}

## 10. Decision

{DECISION[0]["decision"]}

Practical read: this is the cleanest version of the rule we need. It proves what would be true if the parent action obeys the contract, but it also exposes the unresolved enemy: why is this the only allowed parent action rather than just the neat one we want?

## 11. Next Target

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
    write_csv(results_dir / "blindness_requirements.csv", BLINDNESS_REQUIREMENTS)
    write_csv(results_dir / "variation_order_contract.csv", VARIATION_ORDER_CONTRACT)
    write_csv(results_dir / "conditional_theorem_chain.csv", CONDITIONAL_THEOREM_CHAIN)
    write_csv(results_dir / "counterexample_leaks.csv", COUNTEREXAMPLE_LEAKS)
    write_csv(results_dir / "finite_fibre_impact.csv", FINITE_FIBRE_IMPACT)
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
        "blindness_requirements": len(BLINDNESS_REQUIREMENTS),
        "variation_order_contract_written": True,
        "conditional_chain_rule_zero_written": True,
        "readout_after_variation_contract_written": True,
        "parent_factorization_derived": False,
        "constant_sector_universality_derived": False,
        "finite_fibre_blindness_derived": False,
        "material_marker_extension_blocked": False,
        "same_frame_EH_source_derived": False,
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
        description="Write checkpoint 422 matter-functor blindness and readout-after-variation theorem attempt artifacts."
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
