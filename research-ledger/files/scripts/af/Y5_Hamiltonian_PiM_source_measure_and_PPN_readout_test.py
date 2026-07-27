from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_Hamiltonian_PiM_readout_test_written_source_measure_and_PPN_gates_open_no_Newton_or_local_GR_promotion"
CLAIM_CEILING = "Hamiltonian_PiM_source_measure_PPN_gate_only_no_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "541-Y5-Hamiltonian-PiM-source-measure-contract-or-residual-scorecard.md"

DOC_PATH = Path("540-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_READOUT_SOURCE_REGISTER.csv")
SOURCE_MEASURE_TEST_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_SOURCE_MEASURE_TEST.csv")
GAUSS_PPN_TEST_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_GAUSS_PPN_TEST.csv")
RESIDUAL_ACTIVATION_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_RESIDUAL_ACTIVATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_READOUT_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_READOUT_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_HAMILTONIAN_PIM_READOUT_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "539-Y5-PiM-as-Hamiltonian-charge-map-or-topological-demotion.md",
        "role": "Hamiltonian Pi_M candidate and topological Pi_M demotion",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "worldtube/source-measure glue and PPN readout warning",
    },
    {
        "source_file": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "Hamiltonian charge to measured orbital GM calibration gate",
    },
    {
        "source_file": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert source to measured monopole calibration gate",
    },
    {
        "source_file": "531-Y5-source-normalized-Newton-and-beta-residual-envelope.md",
        "role": "source-normalized Newton precondition and beta residual envelope",
    },
    {
        "source_file": "538-Y5-minimal-parent-action-Euler-Ward-test-or-closure-demotion.md",
        "role": "Euler/Ward chain test that isolated DAT537_4",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_BRANCH_DEFINITION.csv",
        "role": "539 Hamiltonian Pi_M candidate rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_GATE_RESULTS.csv",
        "role": "539 open Hamiltonian Pi_M gates",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_TOPOLOGICAL_PIM_DEMOTION_LEDGER.csv",
        "role": "539 demotion of old topological Pi_M route",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv",
        "role": "458 Poisson/Gauss calibration contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv",
        "role": "450 Hilbert-monopole measured-GM calibration contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv",
        "role": "531/523 source-normalized Newton scorecard",
    },
    {
        "source_file": "source-intake/local_bounds/local_bound_claims.csv",
        "role": "local PPN/source-normalization empirical locks",
    },
    {
        "source_file": "scripts/Y5_Hamiltonian_PiM_source_measure_and_PPN_readout_test.py",
        "role": "this checkpoint generator",
    },
]


SOURCE_MEASURE_TEST_ROWS = [
    {
        "test_id": "SMT540_0_branch_adoption",
        "gate": "Hamiltonian Pi_M branch is adopted as the parent mass-charge representative, not merely named",
        "mathematical_form": "Pi_M := Pi_M^H and old Pi_M^top is discarded or mapped to Pi_M^H + residuals",
        "current_result": "candidate_only_not_adopted_or_proved",
        "blocks": "DAT537_4;source_normalized_Newton",
        "valid_for_claim": "false",
    },
    {
        "test_id": "SMT540_1_charge_integrability",
        "gate": "Q_tau has fixed reference, boundary term, and integrable Hamiltonian variation",
        "mathematical_form": "delta H_tau = integral_S(delta Q_tau - i_tau theta) with integrable reference subtraction",
        "current_result": "not_derived_for_current_MTS",
        "blocks": "measured_GM;absolute_calibration",
        "valid_for_claim": "false",
    },
    {
        "test_id": "SMT540_2_same_source_worldtube",
        "gate": "the worldtube source measure is the same observed Hilbert matter source used by Q_tau",
        "mathematical_form": "W_source=supp(J_H[e_obs]); M_source[W]=H_tau[S]-H_ref before orbital fitting",
        "current_result": "not_derived",
        "blocks": "measured_GM;Newton",
        "valid_for_claim": "false",
    },
    {
        "test_id": "SMT540_3_radial_closure",
        "gate": "Hamiltonian mass charge is radially closed in the compact source-free exterior",
        "mathematical_form": "int_S2 Q_tau - int_S1 Q_tau = int_A(C_EH+C_extra+C_projector+C_boundary)=0",
        "current_result": "conditional_EH_reference_only_C_terms_open",
        "blocks": "epsilon_radial_Meff;source_normalized_Newton",
        "valid_for_claim": "false",
    },
    {
        "test_id": "SMT540_4_no_extra_mass_channels",
        "gate": "non-EH, projector, domain, memory, range, connection, frame, and boundary channels add no independent mass charge",
        "mathematical_form": "Delta_nonEH=Delta_PiM=Delta_extra=Delta_frame=Delta_symp=0 or source-backed below locks",
        "current_result": "not_field_specific_derived",
        "blocks": "mu_extra;Gdot;fifth_force;PPN",
        "valid_for_claim": "false",
    },
    {
        "test_id": "SMT540_5_old_topological_equivalence_optional",
        "gate": "old Pi_M^top need not be saved, but if cited it must equal Pi_M^H up to zero-flux terms",
        "mathematical_form": "Pi_M^top J_H - Pi_M^H J_H = R_Htop + dB_Htop",
        "current_result": "old_topological_route_demoted_unless_residuals_zero_or_bounded",
        "blocks": "topological_PiM_claim_credit",
        "valid_for_claim": "false",
    },
    {
        "test_id": "SMT540_6_measured_source_definition",
        "gate": "M_source is explicitly dressed Hamiltonian/Noether source charge, not bare rest mass",
        "mathematical_form": "M_source[W] := H_tau[S_outer]-H_tau[reference]",
        "current_result": "definition_guardrail_pass_but_not_full_MTS_theorem",
        "blocks": "public_claim_only_if_promoted",
        "valid_for_claim": "false",
    },
]


GAUSS_PPN_TEST_ROWS = [
    {
        "test_id": "GPT540_0_Poisson_coefficient",
        "gate": "same-frame weak-field equation reduces to Poisson with standard coefficient",
        "mathematical_form": "g_00=-1+2Phi/c^2; nabla^2 Phi=4*pi*G_ref*rho_H",
        "current_result": "conditional_from_prior_EH_branch_not_current_promotion",
        "claim_effect": "first_order_Newton_not_earned",
        "valid_for_claim": "false",
    },
    {
        "test_id": "GPT540_1_Gauss_surface_calibration",
        "gate": "Poisson surface integral equals Hamiltonian Pi_M source mass with no source residual",
        "mathematical_form": "surface_integral grad Phi.dS = 4*pi*G_ref*M_source and S_res=0",
        "current_result": "not_parent_derived",
        "claim_effect": "measured_GM_false",
        "valid_for_claim": "false",
    },
    {
        "test_id": "GPT540_2_orbital_inverse_square_readout",
        "gate": "test bodies read the same potential as pure inverse-square acceleration",
        "mathematical_form": "a_r=-partial_r Phi=-G_ref*M_source/r^2 with no Yukawa/radial/frame/species hair",
        "current_result": "not_derived",
        "claim_effect": "Newton_false",
        "valid_for_claim": "false",
    },
    {
        "test_id": "GPT540_3_constant_universal_G",
        "gate": "G_eff/kappa is constant, universal, source-blind, range-blind, and frame-blind",
        "mathematical_form": "partial_t,r,A,lambda,frame G_eff=0",
        "current_result": "conditional_not_parent_derived",
        "claim_effect": "Gdot_source_charge_range_rows_active",
        "valid_for_claim": "false",
    },
    {
        "test_id": "GPT540_4_beta_source_stability",
        "gate": "same measured-GM normalization survives second-order beta order",
        "mathematical_form": "delta_beta_source=0 and B_source/A_source^2=1",
        "current_result": "not_derived_missing_531_components",
        "claim_effect": "beta_false",
        "valid_for_claim": "false",
    },
    {
        "test_id": "GPT540_5_full_PPN_vector",
        "gate": "gamma, beta, alpha_i, zeta_i, xi and preferred-frame components are zero or below official locks",
        "mathematical_form": "Delta_PPN={gamma-1,beta-1,alpha_i,zeta_i,xi} explicit absolute envelope",
        "current_result": "not_reached",
        "claim_effect": "local_GR_false",
        "valid_for_claim": "false",
    },
]


RESIDUAL_ACTIVATION_ROWS = [
    {
        "residual_id": "RA540_0_charge_integrability",
        "failed_gate": "SMT540_1_charge_integrability",
        "residual_quantity": "Delta_symp;Delta_boundary_reference",
        "maps_to": "MR510_2;PG0;PG4",
        "required_artifact": "boundary/reference theorem or source-backed boundary shift row",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "RA540_1_source_measure",
        "failed_gate": "SMT540_2_same_source_worldtube",
        "residual_quantity": "Delta_frame;Delta_cal",
        "maps_to": "MR510_5;MR510_6;HM0;HM3",
        "required_artifact": "same-frame worldtube source theorem or calibration residual row",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "RA540_2_radial_closure",
        "failed_gate": "SMT540_3_radial_closure",
        "residual_quantity": "epsilon_radial_Meff;dln_Meff",
        "maps_to": "MR510_0;P8_Y5_PIM_INPUT_FILL_TEMPLATE",
        "required_artifact": "C-term zero theorem or sourced radial profile/bound",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "RA540_3_extra_mass_channels",
        "failed_gate": "SMT540_4_no_extra_mass_channels",
        "residual_quantity": "mu_extra;Delta_nonEH;Delta_PiM;Delta_extra",
        "maps_to": "MR510_1;MR510_3;MR510_4;PG6",
        "required_artifact": "field-specific silence theorem or channelwise residual vector",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "RA540_4_Gauss_orbital",
        "failed_gate": "GPT540_1_Gauss_surface_calibration;GPT540_2_orbital_inverse_square_readout",
        "residual_quantity": "Delta_cal;alpha(lambda);partial_r ln mu_obs",
        "maps_to": "PG4;PG5;PG10;R10;R11",
        "required_artifact": "Gauss/orbital readout theorem or fifth-force/radial residual",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "RA540_5_constant_G",
        "failed_gate": "GPT540_3_constant_universal_G",
        "residual_quantity": "dln_Geff_dt;source_charge;range_dependence",
        "maps_to": "PG7;PG8;R1;R9;R10",
        "required_artifact": "constant kappa/G theorem or Gdot/source/range rows",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
    {
        "residual_id": "RA540_6_PPN",
        "failed_gate": "GPT540_4_beta_source_stability;GPT540_5_full_PPN_vector",
        "residual_quantity": "delta_beta_source;gamma_minus_one;alpha_i;zeta_i;xi",
        "maps_to": "PG9;MR510_7;ENV531",
        "required_artifact": "second-order weak-field/PPN expansion or residual envelope inputs",
        "current_status": "unfilled",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D540_0_Hamiltonian_PiM_not_enough",
        "status": "candidate_charge_map_does_not_by_itself_derive_measured_GM",
        "meaning": "Pi_M^H fixes the wrong-object problem only at charge-map level; source-measure and readout gates remain",
        "claim_status": "measured_GM_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D540_1_source_measure_gate_open",
        "status": "worldtube_source_measure_not_derived",
        "meaning": "M_source must still be proved to equal the dressed Hamiltonian charge in the observed frame",
        "claim_status": "Newton_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D540_2_Poisson_Gauss_gate_open",
        "status": "Gauss_orbital_readout_not_derived",
        "meaning": "the same charge must still control Poisson/Gauss and pure inverse-square orbital readout",
        "claim_status": "source_normalized_Newton_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D540_3_PPN_gate_not_reached",
        "status": "beta_and_PPN_not_promoted",
        "meaning": "PPN stays blocked until first-order source-normalized Newton closes",
        "claim_status": "local_GR_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D540_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "HAMILTONIAN_PIM",
        "previous_status": "Hamiltonian_charge_map_candidate_written",
        "new_status": "candidate_survives_but_readout_gates_open",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_MEASURE_GLUE",
        "previous_status": "not_derived",
        "new_status": "central_next_contract_or_residual_scorecard",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "blocked_source_measure_and_Gauss_readout",
        "new_status": "still_blocked_source_measure_Gauss_constant_G_residuals",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "BETA_PPN",
        "previous_status": "missing_components_not_evaluable",
        "new_status": "still_blocked_until_Newton_precondition_passes",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_PPN_readout_not_reached",
        "new_status": "still_blocked_source_measure_Newton_PPN_stack",
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
    hamiltonian_gates = read_csv(Path("source-intake/mts_residuals/P8_Y5_PIM_HAMILTONIAN_GATE_RESULTS.csv"))
    pg_contract = read_csv(Path("source-intake/mts_residuals/P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv"))
    hm_contract = read_csv(Path("source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv"))
    scorecard = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_RESIDUAL_SCORECARD.csv"))
    local_bounds = read_csv(Path("source-intake/local_bounds/local_bound_claims.csv"))
    claim_source_rows = [row for row in SOURCE_MEASURE_TEST_ROWS if row["valid_for_claim"] == "true"]
    claim_gauss_rows = [row for row in GAUSS_PPN_TEST_ROWS if row["valid_for_claim"] == "true"]
    claim_residual_rows = [row for row in RESIDUAL_ACTIVATION_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V540_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V540_1_prior_539_loaded",
            "result": "pass" if len(hamiltonian_gates) == 7 else "fail",
            "detail": f"hamiltonian_gate_rows={len(hamiltonian_gates)}",
        },
        {
            "check_id": "V540_2_calibration_contracts_loaded",
            "result": "pass" if len(pg_contract) >= 10 and len(hm_contract) >= 8 else "fail",
            "detail": f"PG_rows={len(pg_contract)};HM_rows={len(hm_contract)}",
        },
        {
            "check_id": "V540_3_scorecard_and_bounds_loaded",
            "result": "pass" if len(scorecard) >= 12 and len(local_bounds) > 0 else "fail",
            "detail": f"scorecard_rows={len(scorecard)};local_bounds_rows={len(local_bounds)}",
        },
        {
            "check_id": "V540_4_tests_complete",
            "result": "pass" if len(SOURCE_MEASURE_TEST_ROWS) == 7 and len(GAUSS_PPN_TEST_ROWS) == 6 else "fail",
            "detail": f"source_measure_rows={len(SOURCE_MEASURE_TEST_ROWS)};gauss_ppn_rows={len(GAUSS_PPN_TEST_ROWS)}",
        },
        {
            "check_id": "V540_5_residual_activation_complete",
            "result": "pass" if len(RESIDUAL_ACTIVATION_ROWS) == 7 else "fail",
            "detail": f"residual_rows={len(RESIDUAL_ACTIVATION_ROWS)}",
        },
        {
            "check_id": "V540_6_no_claim_rows",
            "result": "pass" if not claim_source_rows and not claim_gauss_rows and not claim_residual_rows else "fail",
            "detail": f"claim_source_rows={len(claim_source_rows)};claim_gauss_rows={len(claim_gauss_rows)};claim_residual_rows={len(claim_residual_rows)}",
        },
        {
            "check_id": "V540_7_no_overclaim",
            "result": "pass" if not claim_source_rows and not claim_gauss_rows and not claim_residual_rows else "fail",
            "detail": "Hamiltonian_PiM_candidate_only=true; measured_GM=false; Newton=false; beta=false; PPN=false; local_GR=false",
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
    return f"""# 540 - Y5 Hamiltonian PiM Source-Measure and PPN Readout Test

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The Hamiltonian `Pi_M^H` pivot is useful, but it is not enough by itself.

It repairs the old topological wrong-object risk at the charge-map level:

```text
Pi_M^H J_H := ell_H[J_H;tau,S] omega_M^H
```

But source-normalized Newton still requires:

```text
worldtube source measure = dressed Hamiltonian charge
same-frame Poisson/Gauss coefficient
pure inverse-square orbital readout
constant universal G_eff
zero mu_extra/source residuals
```

and local GR still requires the same branch to pass the second-order PPN vector.

## 2. Source-Measure Tests

{markdown_table(SOURCE_MEASURE_TEST_ROWS)}

## 3. Gauss/PPN Readout Tests

{markdown_table(GAUSS_PPN_TEST_ROWS)}

## 4. Residual Activation Map

{markdown_table(RESIDUAL_ACTIVATION_ROWS)}

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
MTS has a Hamiltonian Pi_M candidate that keeps the measured source charge tied to the parent charge map.
MTS has explicit source-measure, Gauss, Newton, and PPN gates for that branch.
Failed gates now map to residual rows instead of hidden calibration.
```

Forbidden:

```text
MTS has derived measured GM.
MTS has derived source-normalized Newton.
MTS has passed beta, PPN, or local GR.
MTS may treat Hamiltonian Pi_M notation as proof of source-measure glue.
```

## 10. Practical Read

This is a real improvement, but the honest read is still strict: `Pi_M^H` is the right-looking object only if it produces the measured mass that matter orbits read. Until the source-measure/Gauss/PPN stack closes, it is disciplined notation plus a repair route, not a GR reduction theorem.

## 11. Next Target

`{NEXT_TARGET}`

Next: turn the open source-measure gates into a compact contract or scorecard. Either prove the worldtube source measure equals `Pi_M^H`, or activate the residual rows for boundary, frame, radial, extra-sector, constant-G, and PPN channels.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-Hamiltonian-PiM-source-measure-and-PPN-readout-test"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (SOURCE_MEASURE_TEST_PATH, SOURCE_MEASURE_TEST_ROWS),
        (GAUSS_PPN_TEST_PATH, GAUSS_PPN_TEST_ROWS),
        (RESIDUAL_ACTIVATION_PATH, RESIDUAL_ACTIVATION_ROWS),
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
        "source_measure_test": str(ROOT / SOURCE_MEASURE_TEST_PATH),
        "gauss_ppn_test": str(ROOT / GAUSS_PPN_TEST_PATH),
        "residual_activation": str(ROOT / RESIDUAL_ACTIVATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "source_measure_test_rows": len(SOURCE_MEASURE_TEST_ROWS),
        "gauss_ppn_test_rows": len(GAUSS_PPN_TEST_ROWS),
        "residual_activation_rows": len(RESIDUAL_ACTIVATION_ROWS),
        "Hamiltonian_PiM_candidate_survives": True,
        "Hamiltonian_PiM_branch_adopted_or_proved": False,
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
        "done\nprivate_no_github\nHamiltonian_PiM_candidate_only_no_measured_GM_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
