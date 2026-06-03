from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "same-frame-matter-functor-zero-route"
CHECKPOINT_DOC = "432-same-frame-matter-functor-zero-route.md"
STATUS = "same_frame_matter_functor_zero_route_written_universal_coupling_contract_sharpened_C0_not_parent_derived_no_local_GR_pass"
CLAIM_CEILING = "same_frame_matter_functor_zero_route_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "433-kappa-Geff-local-constancy-lemma.md"


SOURCE_DOCS = [
    {
        "path": "360-universal-matter-coupling-theorem-attempt.md",
        "role": "first conditional one-observed-coframe matter coupling theorem attempt",
    },
    {
        "path": "373-one-observed-coframe-parent-selector-or-WEP-closure.md",
        "role": "WEP closure axioms for one coframe, common class function, and constant independence",
    },
    {
        "path": "385-observed-coframe-selector-pullback-cancellation-theorem.md",
        "role": "selector pullback cancellation routes and failure of parent derivation",
    },
    {
        "path": "401-parent-matter-selector-theorem-attempt.md",
        "role": "counterexample showing covariance/species-blindness alone does not force identity coframe",
    },
    {
        "path": "410-quotient-matter-functor-theorem-attempt.md",
        "role": "conditional quotient matter functor chain-rule zero and counterexample functors",
    },
    {
        "path": "422-matter-functor-blindness-readout-after-variation-theorem-attempt.md",
        "role": "no-cheat matter/readout factorization contract",
    },
    {
        "path": "423-parent-action-minimality-no-extension-theorem-attempt.md",
        "role": "material marker extension counterexample and no-extension closure status",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "same-frame EH/source to Poisson bridge and unresolved parent premises",
    },
    {
        "path": "430-Ward-source-residual-zero-route-gate.md",
        "role": "C0 same-frame route ranking and residual rows blocked by C0",
    },
    {
        "path": "431-MTS-local-residual-vector-evaluator.md",
        "role": "local residual evaluator showing no row can be claimed while predictions are placeholders",
    },
    {
        "path": "runs/20260601-233000-one-observed-coframe-parent-selector-or-WEP-closure/results/WEP_closure_axioms.csv",
        "role": "machine-readable W1-W5 one-frame closure axioms",
    },
    {
        "path": "runs/20260602-025500-source-normalized-Newtonian-limit-under-identity-closure/results/weak_field_derivation_steps.csv",
        "role": "identity matter coframe weak-field bridge under closure-zero status",
    },
    {
        "path": "runs/20260602-025500-source-normalized-Newtonian-limit-under-identity-closure/results/source_normalization_contract.csv",
        "role": "source-normalization and species-universality contract not solved by C0 alone",
    },
    {
        "path": "runs/20260602-103000-Ward-source-residual-zero-route-gate/results/route_ranking.csv",
        "role": "C0-C7 priority list with same-frame as hard theorem route",
    },
    {
        "path": "runs/20260602-105000-MTS-local-residual-vector-evaluator/results/gate_results.csv",
        "role": "local-GR claim blocked until all residual rows are filled or theorem-zero",
    },
]


C0_THEOREM_CHAIN = [
    {
        "step": 1,
        "claim": "Define a single observed coframe and metric for local comparisons.",
        "symbolic_form": "e_obs^a_mu, g_obs_munu = eta_ab e_obs^a_mu e_obs^b_nu",
        "status": "definition_contract",
        "blocker": "none at definition level",
    },
    {
        "step": 2,
        "claim": "Matter is a functor of observed geometry, not of representative MTS selectors.",
        "symbolic_form": "F_matter: ObsFrame -> {S_A[Psi_A,e_obs,omega[e_obs],theta_A]}",
        "status": "sufficient_axiom_not_parent_derived",
        "blocker": "parent action has not proven factorization through ObsFrame",
    },
    {
        "step": 3,
        "claim": "All matter, clocks, rods, photons, and lab standards use that same frame.",
        "symbolic_form": "e_A = e_obs for every sector A",
        "status": "closure_until_selector_theorem_exists",
        "blocker": "species-dependent metrics e_A or g_A remain legal counterexamples",
    },
    {
        "step": 4,
        "claim": "No species-dependent class functions or matter constants carry MTS charge.",
        "symbolic_form": "partial_Z theta_A = 0 and F_A(C_D)=F(C_D)",
        "status": "not_derived",
        "blocker": "constant-sector universality is still an independent theorem target",
    },
    {
        "step": 5,
        "claim": "Representative variables sit in the observation kernel.",
        "symbolic_form": "partial_ZI Obs(Q)=0 for Z_I in {B_perp,b2,Cperp,j3,domain reps}",
        "status": "conditional_partial",
        "blocker": "global representative blindness and marker exclusion are not proven",
    },
    {
        "step": 6,
        "claim": "Matter Ward conservation holds in the same observed frame.",
        "symbolic_form": "nabla_obs_mu T_obs^mu_nu = 0 on matter shell",
        "status": "conditional_if_same_frame_action_holds",
        "blocker": "does not by itself kill source-normalization or non-EH operator residuals",
    },
    {
        "step": 7,
        "claim": "Direct matter-selector pullback vanishes by the chain rule.",
        "symbolic_form": "delta S_matter/delta Z_I = (delta S_matter/delta Obs)(partial_ZI Obs)+partial_ZI theta_A terms = 0",
        "status": "conditional_theorem_shape",
        "blocker": "requires factorization plus constant-sector blindness",
    },
    {
        "step": 8,
        "claim": "C0 can only promote rows after the parent forbids all alternate matter metrics and marker extensions.",
        "symbolic_form": "no g_A, no F_A(C_D), no Q_tilde=(Q,m)/G_rel, no post-readout EFT",
        "status": "not_parent_derived",
        "blocker": "universal-property/minimal parent theorem missing",
    },
]


MATTER_FUNCTOR_REQUIREMENTS = [
    {
        "requirement": "single_observed_frame",
        "mathematical_form": "S_matter=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A]",
        "current_status": "closure_until_parent_selector_exists",
        "rows_protected": "R0;R2;R3;R4",
        "failure_if_missing": "matter and photons can compare different geometries",
    },
    {
        "requirement": "species_blindness",
        "mathematical_form": "e_A=e_obs and F_A(C_D)=F(C_D) for every A",
        "current_status": "not_parent_derived",
        "rows_protected": "R0;R1;R2",
        "failure_if_missing": "composition-dependent WEP/source/clock residuals survive",
    },
    {
        "requirement": "representative_blindness",
        "mathematical_form": "delta S_matter/delta Z_I|e_obs = 0",
        "current_status": "conditional_partial",
        "rows_protected": "R0;R1;R10",
        "failure_if_missing": "representative variables become fifth-force or WEP dials",
    },
    {
        "requirement": "constant_sector_universality",
        "mathematical_form": "partial_Z theta_A = partial_h theta_A = partial_IQ theta_A = 0",
        "current_status": "not_derived",
        "rows_protected": "R1;R2;R9",
        "failure_if_missing": "dimensionless constants and masses drift by species or clock type",
    },
    {
        "requirement": "selector_variation_owned",
        "mathematical_form": "selector pullback stress is either zero or retained in total Ward ledger",
        "current_status": "conditional_retained",
        "rows_protected": "R0;R7;R9;R11",
        "failure_if_missing": "unowned exchange is hidden as conserved matter",
    },
    {
        "requirement": "same_EH_and_matter_frame",
        "mathematical_form": "T_obs_munu = -2/sqrt(-g_obs) delta S_matter/delta g_obs^munu",
        "current_status": "separate_open_gate",
        "rows_protected": "R3;R4;R9;R11",
        "failure_if_missing": "Poisson source can be in a different frame from the metric equation",
    },
    {
        "requirement": "source_normalization_species_blind",
        "mathematical_form": "partial_A ln mu_obs = 0 for matter, clocks, and compositions",
        "current_status": "not_derived",
        "rows_protected": "R1;R4;R9;R10",
        "failure_if_missing": "measured GM absorbs WEP/source-charge leakage",
    },
    {
        "requirement": "no_material_marker_extension",
        "mathematical_form": "no Q_tilde=(Q,m)/G_rel with matter-visible m",
        "current_status": "fixed_spurions_excluded_conditionally_material_markers_not_forbidden",
        "rows_protected": "R0;R1;R2;R10;R11",
        "failure_if_missing": "a covariant extension restores hidden matter charges",
    },
]


SAME_FRAME_FAILURE_MODES = [
    {
        "failure_mode": "species_metric_split",
        "symbolic_form": "g_A = exp(F_A(C_D)) g_obs",
        "damage": "direct WEP and clock-frame residuals return",
        "required_blocker": "parent-derived one-frame selector plus species symmetry",
    },
    {
        "failure_mode": "universal_but_selector_dependent_metric",
        "symbolic_form": "g_matter = exp(F(C_D)) g_obs with F_prime != 0",
        "damage": "common-mode pullback survives even without species split",
        "required_blocker": "selector-blind matter theorem or local common-mode silence",
    },
    {
        "failure_mode": "clock_EM_constant_drift",
        "symbolic_form": "alpha_EM(Z), m_A(Z), or q_A(Z)",
        "damage": "spectroscopy, clocks, and WEP tests see non-geometric MTS charge",
        "required_blocker": "constant-sector universality theorem",
    },
    {
        "failure_mode": "representative_pullback_force",
        "symbolic_form": "partial_ZI Obs(Q) != 0",
        "damage": "Cperp/domain/projector variables source local matter residuals",
        "required_blocker": "quotient observation-kernel proof",
    },
    {
        "failure_mode": "source_normalization_hidden_WEP",
        "symbolic_form": "partial_A ln mu_obs != 0",
        "damage": "Kepler GM looks fitted while composition source charge remains",
        "required_blocker": "universal source-normalization theorem",
    },
    {
        "failure_mode": "material_marker_extension",
        "symbolic_form": "Q_tilde=(Q,m)/G_rel",
        "damage": "covariant hidden markers create local material charges",
        "required_blocker": "primitive-minimal parent universal property",
    },
    {
        "failure_mode": "EH_matter_frame_split",
        "symbolic_form": "S_EH[g_EH] + S_matter[g_matter]",
        "damage": "Newton/PPN source does not own the same geometry matter measures",
        "required_blocker": "same-frame EH/source parent theorem",
    },
    {
        "failure_mode": "nonmetric_or_torsion_matter_vertex",
        "symbolic_form": "S_matter includes K_munu J_A^mu u_A^nu or torsion current terms",
        "damage": "preferred-frame or fifth-force residuals return",
        "required_blocker": "matter functor restricted to Levi-Civita observed geometry",
    },
]


ROW_IMPLICATIONS = [
    {
        "row_id": "R0_identity_coframe_direct",
        "if_C0_solved": "direct frame/WEP coframe mismatch can seek theorem_zero",
        "remaining_debt": "source charge and common-mode selector pullback still separate unless blocked",
        "current_transition": "closure_zero_not_upgraded",
    },
    {
        "row_id": "R1_WEP_source_charge",
        "if_C0_solved": "direct geometry species split is removed",
        "remaining_debt": "species source-normalization and mass/constant charge still open",
        "current_transition": "retained_contingent_budget_not_upgraded",
    },
    {
        "row_id": "R2_clock_redshift",
        "if_C0_solved": "clocks compare one observed metric",
        "remaining_debt": "alpha_EM/mass/clock constants and common-mode redshift silence still open",
        "current_transition": "retained_budget_not_upgraded",
    },
    {
        "row_id": "R3_gamma",
        "if_C0_solved": "photon and matter frame mismatch is removed",
        "remaining_debt": "EH operator, boundary hair, and non-EH coefficients still control gamma",
        "current_transition": "retained_budget_not_upgraded",
    },
    {
        "row_id": "R4_beta",
        "if_C0_solved": "same-frame source comparison becomes meaningful",
        "remaining_debt": "source normalization, kappa constancy, and nonlinear metric sector remain",
        "current_transition": "retained_budget_not_upgraded",
    },
    {
        "row_id": "R9_Gdot",
        "if_C0_solved": "matter clocks and source frame can be compared without hidden frame split",
        "remaining_debt": "G_eff M_eff time constancy is not a matter-frame theorem",
        "current_transition": "retained_contingent_budget_not_upgraded",
    },
    {
        "row_id": "R11_EH_operator_ledger",
        "if_C0_solved": "matter sources the same observed frame if EH/source gate also holds",
        "remaining_debt": "EH-only exterior and non-EH coefficient vector still separate",
        "current_transition": "retained_residual_not_upgraded",
    },
]


ALLOWED_MATTER_ACTION_FORMS = [
    {
        "form_id": "allowed_minimal_same_frame",
        "action_form": "S_matter=sum_A S_A[Psi_A,e_obs,omega[e_obs],theta_A]",
        "verdict": "allowed_as_C0_contract",
        "reason": "all local matter comparisons use one observed coframe and universal constants",
    },
    {
        "form_id": "allowed_universal_constant_rescaling",
        "action_form": "e_obs -> lambda0 e_obs with constant universal lambda0",
        "verdict": "harmless_if_absorbed_in_units",
        "reason": "constant universal calibration is not a local species/time/range residual",
    },
    {
        "form_id": "forbidden_species_metric",
        "action_form": "S_A[Psi_A,e_A] with e_A != e_obs",
        "verdict": "forbidden_for_theorem_zero",
        "reason": "creates WEP and clock-frame split",
    },
    {
        "form_id": "forbidden_selector_dependent_metric",
        "action_form": "S_matter[Psi,exp(F(Z))e_obs]",
        "verdict": "forbidden_unless_F_prime_zero_derived",
        "reason": "common-mode selector pullback remains a matter force",
    },
    {
        "form_id": "forbidden_marker_extended_action",
        "action_form": "S_matter[Psi,e_obs,m] with Q_tilde=(Q,m)/G_rel",
        "verdict": "retained_or_closure_only",
        "reason": "covariant marker extension is not excluded by present parent action",
    },
    {
        "form_id": "forbidden_post_readout_EFT",
        "action_form": "S_red[R_read(Q)] varied as parent dynamics",
        "verdict": "forbidden_for_theorem_zero",
        "reason": "readout can be used after variation, not as a hidden source term",
    },
]


THEOREM_ATTEMPT_STATUS = [
    {
        "claim": "same-frame matter functor can be stated exactly",
        "status": "pass",
        "evidence": "C0 theorem chain and allowed matter action forms written",
    },
    {
        "claim": "same-frame matter functor is sufficient to remove direct frame mismatch if assumed",
        "status": "conditional_pass",
        "evidence": "chain-rule zero follows under factorization and constant-sector blindness",
    },
    {
        "claim": "same-frame matter functor is parent-derived",
        "status": "fail",
        "evidence": "species metrics, universal selector-dependent metrics, and marker extensions remain legal counterexamples",
    },
    {
        "claim": "C0 solves WEP/source-charge fully",
        "status": "fail",
        "evidence": "source-normalization species blindness and constant-sector universality remain independent debts",
    },
    {
        "claim": "C0 solves Newton/PPN/local GR",
        "status": "fail",
        "evidence": "EH operator, kappa/G_eff constancy, mu_extra, and R10/R11 remain separate gates",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "C0_chain_written",
        "status": "pass",
        "evidence": "8 theorem-chain stages recorded",
    },
    {
        "gate": "matter_functor_requirements_written",
        "status": "pass",
        "evidence": "8 same-frame matter functor requirements recorded",
    },
    {
        "gate": "same_frame_parent_derived",
        "status": "fail",
        "evidence": "no parent theorem forbids all alternate matter metrics and marker extensions",
    },
    {
        "gate": "species_blindness_derived",
        "status": "fail",
        "evidence": "F_A(C_D), theta_A(Z), and partial_A ln mu_obs remain open",
    },
    {
        "gate": "representative_blindness_globally_derived",
        "status": "fail",
        "evidence": "quotient/functor route is conditional and not global parent proof",
    },
    {
        "gate": "source_normalization_derived",
        "status": "fail",
        "evidence": "identity matter frame does not derive universal measured GM",
    },
    {
        "gate": "material_marker_extensions_forbidden",
        "status": "fail",
        "evidence": "Q_tilde=(Q,m)/G_rel remains legal without primitive-minimal theorem",
    },
    {
        "gate": "runner_rows_promoted_to_theorem_zero",
        "status": "fail",
        "evidence": "0 row upgrades; C0 remains closure/conditional",
    },
    {
        "gate": "local_GR_promoted",
        "status": "fail",
        "evidence": "C0 route only; no EH/Newton/PPN/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "C0 is now a sharp same-frame matter-functor contract, not a derived local-GR theorem. If the parent action derives one universal observed metric/coframe for all matter, clocks, rods, photons, and source definitions, and also derives species-blind constants plus no material marker extensions, then direct frame-mismatch residuals can move toward theorem-zero. The current corpus does not yet derive those premises. Therefore C0 remains closure/conditional, R0-R4/R9/R11 are not promoted, and the next derivation pressure moves to source normalization, especially constant universal kappa/G_eff.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "433-kappa-Geff-local-constancy-lemma.md",
        "why_next": "C0 cannot make Poisson/Newton physical unless kappa_eff/G_eff is constant, universal, and source/species/range independent",
    },
    {
        "rank": 2,
        "target": "filled MTS local residual vector smoke",
        "why_next": "once any residual predictions are supplied, runner 431 can separate theorem-zero, closure, and empirical retained rows",
    },
    {
        "rank": 3,
        "target": "primitive-minimal parent universal-property theorem",
        "why_next": "would be the route to forbid material marker extensions and promote C0 beyond closure",
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


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, "")).replace("\n", " ")
            values.append(value)
        body.append("| " + " | ".join(values) + " |")
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCE_DOCS:
        source_path = ROOT / source["path"]
        rows.append(
            {
                "source_file": source["path"],
                "exists": source_path.exists(),
                "role": source["role"],
            }
        )
    return rows


def gate_rows(source_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    missing_sources = [row["source_file"] for row in source_rows if not row["exists"]]
    source_gate = {
        "gate": "source_paths_exist",
        "status": "pass" if not missing_sources else "fail",
        "evidence": "all cited source paths exist" if not missing_sources else ";".join(missing_sources),
    }
    return [source_gate, *GATE_RESULTS_TEMPLATE]


def write_checkpoint_markdown(run_dir: Path, gate_result_rows: list[dict[str, Any]]) -> None:
    source_rows = source_register_rows()
    text = f"""# 432 - Same-Frame Matter-Functor Zero Route

Private C0/local-GR derivation checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 430 ranked `C0_same_frame` as the hard matter-frame route, and checkpoint 431 showed the local residual vector cannot be claimed while rows are placeholders. This checkpoint asks the exact question: can MTS derive a universal same-frame matter functor, or must one observed coframe remain closure?

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/same_frame_matter_functor_zero_route.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. C0 Theorem Chain

{markdown_table(C0_THEOREM_CHAIN, ["step", "claim", "status", "blocker"])}

Exact theorem target:

```text
Let Obs(Q_MTS)=e_obs be the observed coframe, and let every matter,
clock, rod, photon, and local mass-standard sector factor as

S_matter = sum_A S_A[Psi_A, e_obs, omega[e_obs], theta_A].

If all representative selectors Z_I lie in ker Obs,
if partial_ZI theta_A = 0 and partial_A ln mu_obs = 0,
if no material marker extension Q_tilde=(Q,m)/G_rel is admitted,
and if the EH/source variation uses the same observed frame,
then direct matter-frame exchange and direct coframe WEP/clock pullback vanish.
```

This is the right theorem shape. The current parent action has not derived all premises.

## 5. Matter-Functor Requirements

{markdown_table(MATTER_FUNCTOR_REQUIREMENTS, ["requirement", "current_status", "rows_protected", "failure_if_missing"])}

## 6. Failure Modes

{markdown_table(SAME_FRAME_FAILURE_MODES, ["failure_mode", "damage", "required_blocker"])}

## 7. Row Implications

{markdown_table(ROW_IMPLICATIONS, ["row_id", "if_C0_solved", "remaining_debt", "current_transition"])}

## 8. Allowed And Forbidden Matter Actions

{markdown_table(ALLOWED_MATTER_ACTION_FORMS, ["form_id", "verdict", "reason"])}

## 9. Theorem Attempt Status

{markdown_table(THEOREM_ATTEMPT_STATUS, ["claim", "status", "evidence"])}

## 10. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 11. Decision

{DECISION[0]["decision"]}

Practical read: this is still a useful result. It is Mayweather progress, not a knockout. The route is now narrow enough that we know exactly what has to be derived, and exactly which rows must stay retained until that happens.

## 12. Next Queue

{markdown_table(NEXT_QUEUE, ["rank", "target", "why_next"])}
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "C0_theorem_chain.csv", C0_THEOREM_CHAIN)
    write_csv(results_dir / "matter_functor_requirements.csv", MATTER_FUNCTOR_REQUIREMENTS)
    write_csv(results_dir / "same_frame_failure_modes.csv", SAME_FRAME_FAILURE_MODES)
    write_csv(results_dir / "row_implications.csv", ROW_IMPLICATIONS)
    write_csv(results_dir / "allowed_matter_action_forms.csv", ALLOWED_MATTER_ACTION_FORMS)
    write_csv(results_dir / "theorem_attempt_status.csv", THEOREM_ATTEMPT_STATUS)
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
        "C0_theorem_chain_steps": len(C0_THEOREM_CHAIN),
        "matter_functor_requirements": len(MATTER_FUNCTOR_REQUIREMENTS),
        "failure_modes": len(SAME_FRAME_FAILURE_MODES),
        "row_implications": len(ROW_IMPLICATIONS),
        "same_frame_parent_derived": False,
        "species_blindness_derived": False,
        "representative_blindness_globally_derived": False,
        "source_normalization_derived": False,
        "material_marker_extensions_forbidden": False,
        "theorem_zero_upgrades": 0,
        "claim_allowed_rows": 0,
        "local_GR_claim_allowed": False,
        "checkpoint_doc": CHECKPOINT_DOC,
        "next_target": NEXT_TARGET,
    }
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(f"{STATUS}\n", encoding="utf-8")
    write_checkpoint_markdown(run_dir, gate_result_rows)
    return run_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Write checkpoint 432 same-frame matter-functor zero-route artifacts."
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
