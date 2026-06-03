from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUN_SLUG = "measured-GM-mu-extra-zero-route"
CHECKPOINT_DOC = "434-measured-GM-mu-extra-zero-route.md"
STATUS = "measured_GM_mu_extra_zero_route_written_Gauss_law_contract_sharpened_conditional_only_not_parent_derived_no_local_GR_pass"
CLAIM_CEILING = "measured_GM_mu_extra_zero_route_only_no_WEP_EH_Newton_PPN_fifth_force_flux_domain_or_local_GR_pass"
NEXT_TARGET = "435-exterior-extra-source-nohair-owner-gate.md"


SOURCE_DOCS = [
    {
        "path": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
        "role": "conditional M_eff monopole flux theorem and radial hair warning",
    },
    {
        "path": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "previous GM absorption gate and residual impact map",
    },
    {
        "path": "380-bulk-X-mass-gap-source-normalized-force-law.md",
        "role": "finite-range bulk/Yukawa source-normalized force-law contract",
    },
    {
        "path": "402-EH-source-normalization-parent-pair.md",
        "role": "EH/source-normalization pair and mu_obs=G_eff M_eff+mu_extra chain",
    },
    {
        "path": "424-same-frame-EH-source-Poisson-reduction-gate.md",
        "role": "Poisson bridge and measured-GM normalization requirements",
    },
    {
        "path": "425-EH-operator-retained-ledger-and-source-normalization-test-plan.md",
        "role": "source-normalization local-bound test plan",
    },
    {
        "path": "429-Ward-Bianchi-exchange-owner-for-Poisson-source.md",
        "role": "mu_extra decomposition and Ward-owned hidden contribution warning",
    },
    {
        "path": "430-Ward-source-residual-zero-route-gate.md",
        "role": "C6 mu_extra zero route ranking",
    },
    {
        "path": "433-kappa-Geff-local-constancy-lemma.md",
        "role": "C5 constant kappa/G_eff conditional lemma",
    },
    {
        "path": "runs/20260601-000061-Meff-monopole-source-normalization-or-radial-memory-hair/results/monopole_flux_theorem_chain.csv",
        "role": "machine-readable M_eff radial conservation chain",
    },
    {
        "path": "runs/20260601-000061-Meff-monopole-source-normalization-or-radial-memory-hair/results/source_normalization_readout.csv",
        "role": "M_eff readout channels and what remains unowned",
    },
    {
        "path": "runs/20260601-000061-Meff-monopole-source-normalization-or-radial-memory-hair/results/claim_gate_results.csv",
        "role": "claim gates for N1 M_eff conditional flux theorem",
    },
    {
        "path": "runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/GM_absorption_theorem_attempt.csv",
        "role": "GM absorption theorem attempt steps",
    },
    {
        "path": "runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/absorption_gate_matrix.csv",
        "role": "GM absorption gate matrix",
    },
    {
        "path": "runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/residual_impact_map.csv",
        "role": "observable row impacts when absorption gates fail",
    },
    {
        "path": "runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/runner_update.csv",
        "role": "runner row update after source-normalization audit",
    },
    {
        "path": "runs/20260602-114500-kappa-Geff-local-constancy-lemma/results/source_residual_implications.csv",
        "role": "C5 residual implications feeding C6",
    },
]


MEASURED_GM_ZERO_CHAIN = [
    {
        "step": 1,
        "claim": "Define the actually observed Kepler/source parameter.",
        "mathematical_form": "mu_obs(r,t,A,lambda) := r^2 partial_r Phi_A(r,t,lambda)",
        "status": "definition",
        "meaning": "orbits measure mu_obs, not G_eff and M_eff separately",
    },
    {
        "step": 2,
        "claim": "Split the weak-field source into ordinary monopole plus retained extras.",
        "mathematical_form": "nabla^2 Phi = 4 pi G_eff rho_M + R_extra",
        "status": "conditional_EH_branch",
        "meaning": "requires same-frame EH/Poisson setup from earlier checkpoints",
    },
    {
        "step": 3,
        "claim": "Gauss law gives the measured source decomposition.",
        "mathematical_form": "mu_obs(r)=G_eff M_eff(r)+mu_extra(r)",
        "status": "algebra_pass",
        "meaning": "mu_extra is the integrated exterior/retained non-ordinary source contribution",
    },
    {
        "step": 4,
        "claim": "Import the conditional M_eff monopole result.",
        "mathematical_form": "d(Pi_M J)=0 on S^2 x [r1,r2] implies dM_eff/dr=0",
        "status": "conditional_from_244_not_global",
        "meaning": "radial ordinary-mass hair is removed only if Pi_M flux closure is parent-owned",
    },
    {
        "step": 5,
        "claim": "Identify the zero condition for mu_extra.",
        "mathematical_form": "mu_extra(r,t,A,lambda)=0 or constant universal calibration only",
        "status": "conditional_theorem_target",
        "meaning": "all boundary, domain, bulk, non-EH, finite-range, time, and species channels must vanish or be harmless calibration",
    },
    {
        "step": 6,
        "claim": "Ward ownership is not absence.",
        "mathematical_form": "nabla_mu T_total^mu_nu=0 does not imply mu_extra=0",
        "status": "counterexample_warning",
        "meaning": "a conserved hidden contribution can still shift measured GM",
    },
    {
        "step": 7,
        "claim": "Measured Newton is recovered only by universal constancy.",
        "mathematical_form": "partial_r mu_obs = partial_t mu_obs = partial_A mu_obs = partial_lambda mu_obs = 0",
        "status": "not_parent_derived",
        "meaning": "current corpus has not derived the full source-normalization theorem",
    },
]


MU_EXTRA_ZERO_REQUIREMENTS = [
    {
        "requirement": "same_frame_observed_potential",
        "required_form": "Phi measured by matter clocks/rods is the Phi sourced in the field equation",
        "current_status": "conditional_from_C0_not_parent_derived",
        "if_missing": "mu_obs is a frame artifact rather than Newtonian source proof",
        "rows_at_risk": "R0;R2;R3;R4;R11",
    },
    {
        "requirement": "constant_universal_Geff",
        "required_form": "G_eff=kappa_eff c^4/(8 pi) with no spacetime/source/species/range dependence",
        "current_status": "conditional_spacetime_lemma_only_from_433",
        "if_missing": "delta_G, Gdot, WEP-source, or range residuals survive",
        "rows_at_risk": "R1;R4;R9;R10",
    },
    {
        "requirement": "absolute_PiM_calibration",
        "required_form": "parent fixes physical units in M_eff=(4 pi G_ref)^-1 int Pi_M J",
        "current_status": "not_parent_derived",
        "if_missing": "M_eff is a fitted normalization rather than measured mass",
        "rows_at_risk": "R4;R9",
    },
    {
        "requirement": "radial_flux_closure",
        "required_form": "d(Pi_M J)=0 in compact ordinary exterior",
        "current_status": "conditional_from_244_not_parent_owned",
        "if_missing": "radial memory hair alters enclosed source",
        "rows_at_risk": "R4;R10",
    },
    {
        "requirement": "no_exterior_extra_source",
        "required_form": "R_extra=0 outside compact matter or all terms retained below bounds",
        "current_status": "not_derived",
        "if_missing": "boundary/bulk/domain/non-EH source becomes mu_extra",
        "rows_at_risk": "R3;R4;R7;R8;R9;R10;R11",
    },
    {
        "requirement": "no_finite_range_tail",
        "required_form": "alpha(lambda)=0 theorem or executable alpha(lambda) curve",
        "current_status": "symbolic_deferred",
        "if_missing": "Yukawa/spectral/domain-wall force is hidden as GM",
        "rows_at_risk": "R10",
    },
    {
        "requirement": "species_source_universality",
        "required_form": "partial_A ln mu_obs=0 for all matter, clocks, and compositions",
        "current_status": "not_parent_derived",
        "if_missing": "source-normalization WEP leakage survives",
        "rows_at_risk": "R1;R2",
    },
    {
        "requirement": "time_stationary_source",
        "required_form": "partial_t ln(G_eff M_eff + mu_extra)=0 locally",
        "current_status": "not_parent_derived",
        "if_missing": "Gdot/G and secular orbital drift remain active",
        "rows_at_risk": "R9",
    },
]


MU_EXTRA_DECOMPOSITION = [
    {
        "channel": "radial_Meff_hair",
        "symbolic_form": "dM_eff/dr != 0",
        "zero_route": "Pi_M flux closure plus no radial memory leakage",
        "current_status": "conditional_not_parent_owned",
        "rows": "R4;R10",
    },
    {
        "channel": "boundary_monopole_shift",
        "symbolic_form": "mu_boundary = constant or time/radial dependent",
        "zero_route": "class/topological boundary no-hair or constant universal calibration",
        "current_status": "retained",
        "rows": "R4;R7;R8;R9",
    },
    {
        "channel": "domain_projector_mass",
        "symbolic_form": "mu_domain[P_D,D] != 0",
        "zero_route": "covariant projector plus no-vector/no-shear/no-monopole leakage",
        "current_status": "conditional_open",
        "rows": "R5;R6;R7;R8;R11",
    },
    {
        "channel": "bulk_X_Yukawa_tail",
        "symbolic_form": "delta a/a_GR = alpha_X (1+r/lambda_X) exp(-r/lambda_X)",
        "zero_route": "positive source-free mass-gap no-hair or executable force-law below bounds",
        "current_status": "symbolic_deferred",
        "rows": "R10",
    },
    {
        "channel": "nonEH_operator_potential",
        "symbolic_form": "Phi = Phi_EH + c_i Phi_i",
        "zero_route": "EH-only exterior or coefficient vector retained and scored",
        "current_status": "retained_symbolic",
        "rows": "R3;R4;R10;R11",
    },
    {
        "channel": "species_source_charge",
        "symbolic_form": "Delta_A mu_obs != 0",
        "zero_route": "same source normalization for all compositions",
        "current_status": "not_derived",
        "rows": "R1;R2",
    },
    {
        "channel": "time_drift",
        "symbolic_form": "partial_t mu_obs != 0",
        "zero_route": "stationary G_eff, M_eff, boundary/domain/bulk source",
        "current_status": "not_derived",
        "rows": "R9",
    },
    {
        "channel": "absolute_calibration_offset",
        "symbolic_form": "mu_obs = lambda0 G_ref M_bare",
        "zero_route": "constant universal calibration absorbed into measured GM",
        "current_status": "harmless_if_parent_fixed_not_derived",
        "rows": "R4;R9",
    },
]


GAUSS_LAW_CASES = [
    {
        "case_id": "GR_Newton_monopole",
        "assumptions": "constant G_eff, conserved M_eff, no R_extra, same frame",
        "result": "mu_obs=G_eff M_eff and mu_extra=0",
        "verdict": "conditional_target",
    },
    {
        "case_id": "conserved_Meff_only",
        "assumptions": "dM_eff/dr=0 but calibration, kappa, and R_extra open",
        "result": "ordinary radial mass hair is controlled but GM absorption is not proven",
        "verdict": "necessary_not_sufficient",
    },
    {
        "case_id": "constant_universal_calibration",
        "assumptions": "mu_extra=lambda0 G_ref M with lambda0 constant for all tests",
        "result": "can be absorbed into measured GM without local residual",
        "verdict": "harmless_calibration_if_parent_fixed",
    },
    {
        "case_id": "radial_hair",
        "assumptions": "mu_extra=mu_extra(r)",
        "result": "inverse-square law/source profile changes",
        "verdict": "R4_R10_retained",
    },
    {
        "case_id": "finite_range_tail",
        "assumptions": "mu_extra depends on lambda or Yukawa profile",
        "result": "range-dependent force cannot be absorbed into GM",
        "verdict": "R10_executable_or_fail",
    },
    {
        "case_id": "species_charge",
        "assumptions": "mu_extra differs by test body, clock, or composition",
        "result": "WEP/source-normalization leakage",
        "verdict": "R1_retained",
    },
    {
        "case_id": "Ward_owned_nonzero_flux",
        "assumptions": "hidden flux is conserved in total ledger but nonzero in measured source",
        "result": "Bianchi bookkeeping passes while Newton source normalization fails",
        "verdict": "retained_not_zero",
    },
]


ROW_IMPLICATIONS = [
    {
        "row_id": "R1_WEP_source_charge",
        "mu_extra_risk": "species or composition dependence in mu_obs",
        "current_transition": "retained_contingent_budget_not_upgraded",
    },
    {
        "row_id": "R4_beta",
        "mu_extra_risk": "radial/nonlinear source hair or unabsorbed monopole shift",
        "current_transition": "retained_budget_not_upgraded",
    },
    {
        "row_id": "R7_alpha3",
        "mu_extra_risk": "unowned boundary/projector momentum flux",
        "current_transition": "retained_contingent_budget_not_upgraded",
    },
    {
        "row_id": "R8_xi",
        "mu_extra_risk": "boundary/domain preferred-location source anisotropy",
        "current_transition": "retained_budget_not_upgraded",
    },
    {
        "row_id": "R9_Gdot",
        "mu_extra_risk": "time-dependent G_eff, M_eff, or boundary/bulk source",
        "current_transition": "retained_contingent_budget_not_upgraded",
    },
    {
        "row_id": "R10_fifth_force",
        "mu_extra_risk": "finite-range Yukawa/spectral/domain-wall tail",
        "current_transition": "symbolic_deferred_not_upgraded",
    },
    {
        "row_id": "R11_EH_operator_ledger",
        "mu_extra_risk": "non-EH operator potential contributes to measured force",
        "current_transition": "retained_residual_not_upgraded",
    },
]


BOUND_FALLBACK_MATRIX = [
    {
        "failed_condition": "partial_r mu_extra=0 not derived",
        "runner_row": "R4;R10",
        "required_action": "score radial source hair or supply no-hair theorem",
    },
    {
        "failed_condition": "partial_t mu_obs=0 not derived",
        "runner_row": "R9",
        "required_action": "score Gdot/G or secular orbital drift",
    },
    {
        "failed_condition": "partial_A ln mu_obs=0 not derived",
        "runner_row": "R1",
        "required_action": "score WEP/source-normalization subchannel",
    },
    {
        "failed_condition": "alpha(lambda)=0 not derived",
        "runner_row": "R10",
        "required_action": "provide executable alpha(lambda) curve; symbolic cannot pass",
    },
    {
        "failed_condition": "non-EH/boundary/domain source not silenced",
        "runner_row": "R3;R4;R7;R8;R11",
        "required_action": "retain coefficient vector or prove no-hair/topological silence",
    },
]


THEOREM_ATTEMPT_STATUS = [
    {
        "claim": "Gauss-law decomposition of measured mu_obs is exact in the weak-field branch",
        "status": "pass",
        "evidence": "mu_obs=G_eff M_eff+mu_extra chain written",
    },
    {
        "claim": "conditional mu_extra=0 theorem shape is identified",
        "status": "conditional_pass",
        "evidence": "requires no exterior extra source, flux closure, same frame, constant G_eff, and universality",
    },
    {
        "claim": "M_eff conservation alone proves measured GM absorption",
        "status": "fail",
        "evidence": "old 244/378 gates show calibration, kappa, range, time, species, and Ward ownership remain open",
    },
    {
        "claim": "Ward-owned hidden flux implies mu_extra=0",
        "status": "fail",
        "evidence": "conserved hidden contribution may still shift measured GM",
    },
    {
        "claim": "C6 mu_extra zero is parent-derived",
        "status": "fail",
        "evidence": "no parent theorem eliminates all boundary/domain/bulk/non-EH/fifth-force/source-normalization channels",
    },
]


GATE_RESULTS_TEMPLATE = [
    {
        "gate": "measured_GM_chain_written",
        "status": "pass",
        "evidence": "7 measured-GM chain stages recorded",
    },
    {
        "gate": "mu_extra_decomposition_written",
        "status": "pass",
        "evidence": "8 mu_extra channels recorded",
    },
    {
        "gate": "conditional_Meff_flux_imported",
        "status": "conditional_pass",
        "evidence": "checkpoint 244 gives M_eff radial conservation only if Pi_M flux closure is parent-owned",
    },
    {
        "gate": "conditional_mu_extra_zero_contract_written",
        "status": "conditional_pass",
        "evidence": "zero theorem shape recorded but depends on C0/C3/C4/C5/C6/C7 premises",
    },
    {
        "gate": "absolute_calibration_derived",
        "status": "fail",
        "evidence": "parent-fixed Pi_M-to-physical-mass units remain open",
    },
    {
        "gate": "no_exterior_extra_source_derived",
        "status": "fail",
        "evidence": "boundary/domain/bulk/non-EH exterior sources remain retained or symbolic",
    },
    {
        "gate": "species_time_range_universality_derived",
        "status": "fail",
        "evidence": "partial_A, partial_t, and alpha(lambda) conditions remain not derived",
    },
    {
        "gate": "Ward_owned_flux_absent_not_just_owned",
        "status": "fail",
        "evidence": "Ward ownership can conserve a nonzero hidden measured-GM shift",
    },
    {
        "gate": "runner_rows_promoted_to_theorem_zero",
        "status": "fail",
        "evidence": "0 row upgrades; R1/R4/R7/R8/R9/R10/R11 remain retained/symbolic",
    },
    {
        "gate": "Newton_or_local_GR_promoted",
        "status": "fail",
        "evidence": "measured-GM route only; no Newton/PPN/local-GR pass",
    },
    {
        "gate": "claim_ceiling_enforced",
        "status": "pass",
        "evidence": CLAIM_CEILING,
    },
]


DECISION = [
    {
        "decision": "The C6 measured-GM route is now exact enough to prevent hidden source normalization. In the weak-field same-frame branch, mu_obs=r^2 partial_r Phi decomposes as G_eff M_eff plus mu_extra. The existing M_eff monopole result is useful but only conditional and not sufficient: mu_extra=0 additionally needs parent-fixed calibration, constant universal G_eff, no exterior boundary/domain/bulk/non-EH/fifth-force source, species/time/range universality, and proof that Ward-owned hidden flux is absent rather than merely conserved. The current corpus does not derive those premises, so C6 remains a conditional zero route and retained test contract, not a Newton/local-GR promotion.",
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "next_target": NEXT_TARGET,
    }
]


NEXT_QUEUE = [
    {
        "rank": 1,
        "target": "435-exterior-extra-source-nohair-owner-gate.md",
        "why_next": "mu_extra=0 now reduces to proving boundary/domain/bulk/non-EH/fifth-force exterior sources are absent, pure calibration, or retained below bounds",
    },
    {
        "rank": 2,
        "target": "auxiliary/projector local Euler-equation ledger",
        "why_next": "C1 remains the strongest Ward route for killing unowned local exchange terms",
    },
    {
        "rank": 3,
        "target": "R10 alpha(lambda) executable curve contract",
        "why_next": "finite-range tails cannot stay symbolic if the local residual vector is to be tested",
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
    text = f"""# 434 - Measured-GM / mu_extra Zero Route

Private C6/source-normalization derivation checkpoint. This is not a public WEP, Einstein-Hilbert, Newtonian-limit, PPN, fifth-force, flux, domain, cosmology, or unified-field claim.

## 1. Purpose

Checkpoint 433 gave a conditional route to constant `kappa_eff/G_eff`, but constant `G_eff` is not the same thing as measured Newtonian source normalization. This checkpoint asks whether `mu_obs=G_eff M_eff` can be derived with `mu_extra=0`, or whether hidden source hair must remain retained.

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/measured_GM_mu_extra_zero_route.py` |
| Run directory | `runs/{run_dir.name}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(source_rows, ["source_file", "exists", "role"])}

## 4. Measured-GM Zero Chain

{markdown_table(MEASURED_GM_ZERO_CHAIN, ["step", "claim", "status", "meaning"])}

Exact measured-source decomposition:

```text
mu_obs(r,t,A,lambda) := r^2 partial_r Phi_A(r,t,lambda)

nabla^2 Phi = 4 pi G_eff rho_M + R_extra

mu_obs(r,t,A,lambda)
  = G_eff M_eff(r,t) + mu_extra(r,t,A,lambda).

mu_extra=0 requires every non-ordinary exterior source, finite-range tail,
species charge, time drift, and non-universal calibration to vanish or be
reduced to one parent-fixed constant universal measured-GM calibration.
```

## 5. mu_extra Zero Requirements

{markdown_table(MU_EXTRA_ZERO_REQUIREMENTS, ["requirement", "current_status", "if_missing", "rows_at_risk"])}

## 6. mu_extra Decomposition

{markdown_table(MU_EXTRA_DECOMPOSITION, ["channel", "zero_route", "current_status", "rows"])}

## 7. Gauss-Law Case Analysis

{markdown_table(GAUSS_LAW_CASES, ["case_id", "result", "verdict"])}

## 8. Row Implications

{markdown_table(ROW_IMPLICATIONS, ["row_id", "mu_extra_risk", "current_transition"])}

## 9. Bound Fallback Matrix

{markdown_table(BOUND_FALLBACK_MATRIX, ["failed_condition", "runner_row", "required_action"])}

## 10. Theorem Attempt Status

{markdown_table(THEOREM_ATTEMPT_STATUS, ["claim", "status", "evidence"])}

## 11. Gate Results

{markdown_table(gate_result_rows, ["gate", "status", "evidence"])}

## 12. Decision

{DECISION[0]["decision"]}

Practical read: this is another narrow-but-good result. We are no longer letting measured `GM` act like a magic bin. Either the extra source is mathematically zero/harmless universal calibration, or it becomes a scored residual row.

## 13. Next Queue

{markdown_table(NEXT_QUEUE, ["rank", "target", "why_next"])}
"""
    (ROOT / CHECKPOINT_DOC).write_text(text, encoding="utf-8")


def write_run(timestamp: str) -> Path:
    run_dir = ROOT / "runs" / f"{timestamp}-{RUN_SLUG}"
    results_dir = run_dir / "results"
    source_rows = source_register_rows()
    gate_result_rows = gate_rows(source_rows)

    write_csv(results_dir / "source_register.csv", source_rows)
    write_csv(results_dir / "measured_GM_zero_chain.csv", MEASURED_GM_ZERO_CHAIN)
    write_csv(results_dir / "mu_extra_zero_requirements.csv", MU_EXTRA_ZERO_REQUIREMENTS)
    write_csv(results_dir / "mu_extra_decomposition.csv", MU_EXTRA_DECOMPOSITION)
    write_csv(results_dir / "Gauss_law_case_analysis.csv", GAUSS_LAW_CASES)
    write_csv(results_dir / "row_implications.csv", ROW_IMPLICATIONS)
    write_csv(results_dir / "bound_fallback_matrix.csv", BOUND_FALLBACK_MATRIX)
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
        "measured_GM_chain_steps": len(MEASURED_GM_ZERO_CHAIN),
        "mu_extra_requirements": len(MU_EXTRA_ZERO_REQUIREMENTS),
        "mu_extra_channels": len(MU_EXTRA_DECOMPOSITION),
        "Gauss_law_cases": len(GAUSS_LAW_CASES),
        "conditional_mu_extra_zero_contract": True,
        "M_eff_conservation_sufficient_for_GM_absorption": False,
        "absolute_calibration_derived": False,
        "no_exterior_extra_source_derived": False,
        "species_time_range_universality_derived": False,
        "Ward_owned_flux_absent_not_just_owned": False,
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
        description="Write checkpoint 434 measured-GM/mu_extra zero-route artifacts."
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
