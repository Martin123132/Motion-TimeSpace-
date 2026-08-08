from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_Hamiltonian_PiM_source_measure_contract_and_residual_scorecard_written_no_measured_GM_or_Newton_promotion"
CLAIM_CEILING = "source_measure_contract_scorecard_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "542-Y5-source-measure-theorem-attempt-or-first-residual-fill.md"

DOC_PATH = Path("541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SOURCE_REGISTER.csv")
CONTRACT_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv")
SCORECARD_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_SCORECARD.csv")
RESIDUAL_INPUTS_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_RESIDUAL_INPUTS.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_SOURCE_MEASURE_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md",
        "role": "Hamiltonian Pi_M source-measure and PPN readout gate",
    },
    {
        "source_file": "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
        "role": "Hamiltonian Pi_M candidate and topological demotion",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "worldtube/source-measure glue and M_eff residual runner",
    },
    {
        "source_file": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "Poisson/Gauss measured-GM calibration gate",
    },
    {
        "source_file": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert-monopole measured-GM calibration gate",
    },
    {
        "source_file": "531-Y5-source-normalized-Newton-and-beta-residual-envelope.md",
        "role": "source-normalized Newton precondition and beta envelope",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_SOURCE_MEASURE_TEST.csv",
        "role": "540 source-measure tests",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_GAUSS_PPN_TEST.csv",
        "role": "540 Gauss/PPN readout tests",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_RESIDUAL_ACTIVATION.csv",
        "role": "540 residual activation map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
        "role": "existing source-normalized Newton scorecard",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "role": "Poisson/Gauss calibration contract rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "role": "Hilbert monopole calibration contract rows",
    },
    {
        "source_file": "scripts/Y5_Hamiltonian_PiM_source_measure_contract_or_residual_scorecard.py",
        "role": "this checkpoint generator",
    },
]


CONTRACT_ROWS = [
    {
        "contract_id": "HSM541_0_adopt_Hamiltonian_PiM",
        "pass_condition": "Pi_M is explicitly the Hamiltonian/covariant-phase-space mass-charge map on the local branch",
        "mathematical_form": "Pi_M J_H := Pi_M^H J_H = ell_H[J_H;tau,S] omega_M^H",
        "current_status": "candidate_only_not_adopted_or_proved",
        "if_fail": "topological/readout Pi_M remains residual only",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "HSM541_1_integrable_charge",
        "pass_condition": "Hamiltonian charge has fixed reference, fixed time generator, and integrable variation",
        "mathematical_form": "delta H_tau = int_S(delta Q_tau - i_tau theta), reference fixed once",
        "current_status": "not_derived_for_current_MTS",
        "if_fail": "Delta_symp and boundary/reference residual activate",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "HSM541_2_observed_worldtube_source",
        "pass_condition": "worldtube source measure is fixed by the same observed Hilbert source current before readout",
        "mathematical_form": "W_source=supp(J_H[e_obs]); M_source[W]=H_tau[S]-H_ref",
        "current_status": "not_derived",
        "if_fail": "frame/source-measure residual activates",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "HSM541_3_radial_closure",
        "pass_condition": "the charge is radially closed in compact source-free exterior",
        "mathematical_form": "int_A(C_EH+C_extra+C_projector+C_boundary)=0",
        "current_status": "conditional_EH_reference_C_terms_open",
        "if_fail": "epsilon_radial_Meff and dln_Meff residuals activate",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "HSM541_4_zero_extra_source_channels",
        "pass_condition": "extra/non-EH/projector/domain/memory/range/frame/boundary channels add no independent mass charge",
        "mathematical_form": "Delta_nonEH=Delta_extra=Delta_PiM=Delta_frame=Delta_boundary=0",
        "current_status": "not_field_specific_derived",
        "if_fail": "mu_extra and channelwise residual vector activate",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "HSM541_5_Gauss_orbital_readout",
        "pass_condition": "same charge controls Poisson/Gauss surface integral and pure inverse-square orbital acceleration",
        "mathematical_form": "nabla^2 Phi=4*pi*G_ref*rho_H; a_r=-G_ref*M_source/r^2",
        "current_status": "not_derived",
        "if_fail": "Delta_cal, radial hair, and fifth-force residuals activate",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "HSM541_6_constant_universal_G",
        "pass_condition": "G_eff/kappa is constant, universal, source-blind, range-blind, and frame-blind",
        "mathematical_form": "partial_t,r,A,lambda,frame G_eff=0",
        "current_status": "conditional_not_parent_derived",
        "if_fail": "Gdot, source-charge, and range-dependence residuals activate",
        "valid_for_claim": "false",
    },
    {
        "contract_id": "HSM541_7_PPN_followthrough",
        "pass_condition": "the same source normalization survives beta/gamma/preferred-frame PPN order",
        "mathematical_form": "Delta_PPN={gamma-1,beta-1,alpha_i,zeta_i,xi}=0 or below official locks",
        "current_status": "not_reached",
        "if_fail": "PPN residual envelope remains active",
        "valid_for_claim": "false",
    },
]


SCORECARD_ROWS = [
    {
        "score_id": "HSS541_0_Hamiltonian_PiM_branch",
        "contract_id": "HSM541_0_adopt_Hamiltonian_PiM",
        "pass_status": "fail_current_claim",
        "evidence": "539 wrote candidate; branch not adopted/proved",
        "residual_if_fail": "R_Htop;R_eq;I_commutator",
        "priority": "highest",
        "valid_for_claim": "false",
    },
    {
        "score_id": "HSS541_1_charge_integrability",
        "contract_id": "HSM541_1_integrable_charge",
        "pass_status": "fail_current_claim",
        "evidence": "510/540 keep reference and boundary terms open",
        "residual_if_fail": "Delta_symp;B_zero_flux",
        "priority": "highest",
        "valid_for_claim": "false",
    },
    {
        "score_id": "HSS541_2_worldtube_source_measure",
        "contract_id": "HSM541_2_observed_worldtube_source",
        "pass_status": "fail_current_claim",
        "evidence": "worldtube source measure not inherited for current MTS",
        "residual_if_fail": "Delta_frame;Delta_cal",
        "priority": "highest",
        "valid_for_claim": "false",
    },
    {
        "score_id": "HSS541_3_radial_closure",
        "contract_id": "HSM541_3_radial_closure",
        "pass_status": "fail_current_claim",
        "evidence": "C_extra/C_projector/C_boundary not field-specific zeroed",
        "residual_if_fail": "epsilon_radial_Meff;dln_Meff",
        "priority": "highest",
        "valid_for_claim": "false",
    },
    {
        "score_id": "HSS541_4_extra_channels",
        "contract_id": "HSM541_4_zero_extra_source_channels",
        "pass_status": "fail_current_claim",
        "evidence": "field-specific silence queue remains open",
        "residual_if_fail": "mu_extra;Delta_nonEH;Delta_PiM;Delta_extra",
        "priority": "high",
        "valid_for_claim": "false",
    },
    {
        "score_id": "HSS541_5_Gauss_readout",
        "contract_id": "HSM541_5_Gauss_orbital_readout",
        "pass_status": "fail_current_claim",
        "evidence": "Poisson/Gauss bridge conditional only; orbital readout not derived",
        "residual_if_fail": "Delta_cal;alpha_lambda;partial_r_ln_mu_obs",
        "priority": "highest",
        "valid_for_claim": "false",
    },
    {
        "score_id": "HSS541_6_constant_G",
        "contract_id": "HSM541_6_constant_universal_G",
        "pass_status": "fail_current_claim",
        "evidence": "constant kappa/G carried conditionally only",
        "residual_if_fail": "dln_Geff_dt;source_charge;range_dependence",
        "priority": "high",
        "valid_for_claim": "false",
    },
    {
        "score_id": "HSS541_7_PPN_followthrough",
        "contract_id": "HSM541_7_PPN_followthrough",
        "pass_status": "not_reached",
        "evidence": "531 beta envelope missing first-order Newton precondition and components",
        "residual_if_fail": "delta_beta_source;gamma_minus_one;alpha_i;zeta_i;xi",
        "priority": "high_after_Newton",
        "valid_for_claim": "false",
    },
]


RESIDUAL_INPUT_ROWS = [
    {
        "input_id": "HSI541_0_boundary_reference",
        "quantity": "B_zero_flux;Delta_symp",
        "required_columns": "system_id;surface_pair;B_zero_flux;Delta_symp;M_H_ref;units;source_file;assumptions;valid_for_claim",
        "acceptance_rule": "fixed reference convention and source-backed value/theorem zero",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "HSI541_1_worldtube_frame",
        "quantity": "Delta_frame;Delta_cal",
        "required_columns": "system_id;source_frame;readout_frame;Delta_frame;Delta_cal;units;source_file;assumptions;valid_for_claim",
        "acceptance_rule": "same-frame theorem or explicit frame/calibration residual below locks",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "HSI541_2_radial_mass_closure",
        "quantity": "epsilon_radial_Meff;dln_Meff_dlnr",
        "required_columns": "system_id;r1;r2;epsilon_radial_Meff;dln_Meff_dlnr;bound_source;source_file;assumptions;valid_for_claim",
        "acceptance_rule": "theorem zero or sourced radial bound, no cancellation-only acceptance",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "HSI541_3_mu_extra_vector",
        "quantity": "mu_extra;Delta_extra_vector",
        "required_columns": "system_id;channel;Delta_charge;mu_extra_over_GM;local_lock;source_file;assumptions;valid_for_claim",
        "acceptance_rule": "each channel separately zero or below lock",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "HSI541_4_Gauss_orbital",
        "quantity": "Delta_cal;alpha_lambda;partial_r_ln_mu_obs",
        "required_columns": "system_id;Delta_cal;alpha_lambda;lambda_scale;partial_r_ln_mu_obs;source_file;assumptions;valid_for_claim",
        "acceptance_rule": "same-frame Gauss/orbit theorem or fifth-force/radial bound",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "HSI541_5_constant_G",
        "quantity": "dln_Geff_dt;eta_source;range_dependence",
        "required_columns": "system_id;dln_Geff_dt;eta_source;range_dependence;bound_source;source_file;assumptions;valid_for_claim",
        "acceptance_rule": "constant universal G theorem or official local-bound residual",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "HSI541_6_PPN_vector",
        "quantity": "delta_beta_source;gamma_minus_one;alpha_i;zeta_i;xi",
        "required_columns": "system_id;delta_beta_source;gamma_minus_one;alpha_i_vector;zeta_i_vector;xi;source_file;assumptions;valid_for_claim",
        "acceptance_rule": "after first-order Newton precondition passes, compare absolute envelope to official locks",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D541_0_contract_written",
        "status": "source_measure_contract_scorecard_written",
        "meaning": "Hamiltonian PiM now has a single referee card from adoption through PPN followthrough",
        "claim_status": "contract_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D541_1_all_claim_gates_fail_or_not_reached",
        "status": "no_measured_GM_Newton_or_PPN_promotion",
        "meaning": "every required source-measure/readout gate is still false or not reached for current MTS",
        "claim_status": "safe_private_work",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D541_2_next_choice",
        "status": "theorem_attempt_or_first_residual_fill",
        "meaning": "next work should either prove HSM541_1-HSM541_3 or fill first residual rows without pretending",
        "claim_status": "active_private_derivation",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D541_3_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "HAMILTONIAN_PIM_SOURCE_MEASURE",
        "previous_status": "central_next_contract_or_residual_scorecard",
        "new_status": "contract_scorecard_written_all_claim_gates_open",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_source_measure_Gauss_constant_G_residuals",
        "new_status": "still_blocked_HSS541_0_to_HSS541_6",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BETA_PPN",
        "previous_status": "still_blocked_until_Newton_precondition_passes",
        "new_status": "still_not_reached_HSS541_7_after_Newton",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_source_measure_Newton_PPN_stack",
        "new_status": "still_blocked_contract_scorecard_unfilled",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in SOURCE_REGISTER:
        full_path = ROOT / item["source_file"]
        rows.append({**item, "exists": full_path.exists()})
    return rows


def validation_rows(sources: list[dict[str, Any]]) -> list[dict[str, str]]:
    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    source_tests = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_SOURCE_MEASURE_TEST.csv"))
    gauss_tests = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_GAUSS_PPN_TEST.csv"))
    residual_activation = read_csv(Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_RESIDUAL_ACTIVATION.csv"))
    claim_contract_rows = [row for row in CONTRACT_ROWS if row["valid_for_claim"] == "true"]
    claim_score_rows = [row for row in SCORECARD_ROWS if row["valid_for_claim"] == "true"]
    claim_input_rows = [row for row in RESIDUAL_INPUT_ROWS if row["valid_for_claim"] == "true"]
    fail_or_not_reached = [
        row for row in SCORECARD_ROWS if row["pass_status"] in {"fail_current_claim", "not_reached"}
    ]
    return [
        {
            "check_id": "V541_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V541_1_prior_540_loaded",
            "result": "pass" if len(source_tests) == 7 and len(gauss_tests) == 6 else "fail",
            "detail": f"source_tests={len(source_tests)};gauss_tests={len(gauss_tests)}",
        },
        {
            "check_id": "V541_2_prior_residual_activation_loaded",
            "result": "pass" if len(residual_activation) == 7 else "fail",
            "detail": f"residual_activation_rows={len(residual_activation)}",
        },
        {
            "check_id": "V541_3_contract_scorecard_complete",
            "result": "pass" if len(CONTRACT_ROWS) == 8 and len(SCORECARD_ROWS) == 8 else "fail",
            "detail": f"contract_rows={len(CONTRACT_ROWS)};scorecard_rows={len(SCORECARD_ROWS)}",
        },
        {
            "check_id": "V541_4_residual_inputs_complete",
            "result": "pass" if len(RESIDUAL_INPUT_ROWS) == 7 else "fail",
            "detail": f"residual_input_rows={len(RESIDUAL_INPUT_ROWS)}",
        },
        {
            "check_id": "V541_5_all_score_rows_fail_or_not_reached",
            "result": "pass" if len(fail_or_not_reached) == len(SCORECARD_ROWS) else "fail",
            "detail": f"fail_or_not_reached_rows={len(fail_or_not_reached)}",
        },
        {
            "check_id": "V541_6_no_claim_rows",
            "result": "pass" if not claim_contract_rows and not claim_score_rows and not claim_input_rows else "fail",
            "detail": f"claim_contract_rows={len(claim_contract_rows)};claim_score_rows={len(claim_score_rows)};claim_input_rows={len(claim_input_rows)}",
        },
        {
            "check_id": "V541_7_no_overclaim",
            "result": "pass" if not claim_contract_rows and not claim_score_rows and not claim_input_rows else "fail",
            "detail": "source_measure_contract_only=true; measured_GM=false; Newton=false; beta=false; PPN=false; local_GR=false",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    full_path = ROOT / path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with full_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers = list(rows[0].keys())
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ").replace("|", "\\|") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 541 - Y5 Hamiltonian PiM Source-Measure Contract or Residual Scorecard

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The Hamiltonian `Pi_M` branch now has a compact referee card.

The result is blunt:

```text
All measured-GM/Newton/PPN claim gates are still false or not reached.
But each false gate now has a named residual input row.
```

That is progress because the next work no longer has to decide whether a failed proof is fatal or useful. It is useful only if it becomes a theorem-zero row or a source-backed residual row.

## 2. Source-Measure Contract

{markdown_table(CONTRACT_ROWS)}

## 3. Scorecard

{markdown_table(SCORECARD_ROWS)}

## 4. Residual Input Rows

{markdown_table(RESIDUAL_INPUT_ROWS)}

## 5. Decision

{markdown_table(DECISION_ROWS)}

## 6. Source Register

{markdown_table(sources)}

## 7. Validation

{markdown_table(validations)}

## 8. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 9. Claim Ceiling

Allowed:

```text
MTS has a compact Hamiltonian-PiM source-measure contract and residual scorecard.
Every open gate maps to a theorem target or fillable residual row.
```

Forbidden:

```text
MTS has derived measured GM.
MTS has derived source-normalized Newton.
MTS has passed beta, PPN, or local GR.
```

## 10. Practical Read

This is the boring but powerful bit: the theory now has a scoreboard. If the derivation lands, rows flip to theorem-zero. If it does not, the same rows become residual tests. Either way, no more hiding first-order Newton inside the word "mass".

## 11. Next Target

`{NEXT_TARGET}`

Next: attempt the theorem route for `HSM541_1` through `HSM541_3`. If it stalls, fill the first residual row instead of inventing closure.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (CONTRACT_PATH, CONTRACT_ROWS),
        (SCORECARD_PATH, SCORECARD_ROWS),
        (RESIDUAL_INPUTS_PATH, RESIDUAL_INPUT_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] is not True]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "results_dir": str(results_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "contract": str(ROOT / CONTRACT_PATH),
        "scorecard": str(ROOT / SCORECARD_PATH),
        "residual_inputs": str(ROOT / RESIDUAL_INPUTS_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "contract_rows": len(CONTRACT_ROWS),
        "scorecard_rows": len(SCORECARD_ROWS),
        "residual_input_rows": len(RESIDUAL_INPUT_ROWS),
        "worldtube_source_measure_derived": False,
        "measured_GM_derived": False,
        "source_normalized_Newton_derived": False,
        "beta_equals_one_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "github_push_performed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        "done\nprivate_no_github\nsource_measure_scorecard_only_no_measured_GM_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
