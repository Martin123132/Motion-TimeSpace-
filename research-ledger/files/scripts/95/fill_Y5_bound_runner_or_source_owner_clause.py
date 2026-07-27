from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_same_observed_coframe_source_owner_clause_written_conditional_not_current_MTS_derived_frame_bound_row_updated"
CLAIM_CEILING = "same_coframe_clause_only_no_Y5_zero_source_normalized_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "520-Y5-source-current-Ward-closure-or-bound-row.md"

DOC_PATH = Path("519-fill-Y5-bound-runner-or-source-owner-clause.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_OWNER_CLAUSE_SOURCE_REGISTER.csv")
PARENT_CLAUSE_PATH = Path("source-intake/mts_residuals/P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv")
VARIATION_PATH = Path("source-intake/mts_residuals/P8_Y5_SAME_COFRAME_VARIATION_DERIVATION.csv")
BOUND_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_SAME_COFRAME_BOUND_UPDATE.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_OWNER_CLAUSE_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_OWNER_CLAUSE_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_OWNER_CLAUSE_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "518-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "role": "Y5 owner theorem and bound-runner input that selected a source-owner clause or bound fill",
    },
    {
        "source_file": "511-minimal-parent-action-local-GR-fixed-point-ansatz.md",
        "role": "minimal parent action local-GR contract including universal observed coframe",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "worldtube source-measure glue and one observed source/readout frame blocker",
    },
    {
        "source_file": "509-source-measure-Meff-flux-closure-after-kappa-gate.md",
        "role": "source-measure and measured-GM equality clauses",
    },
    {
        "source_file": "508-constant-kappa-superselection-or-drift-residual.md",
        "role": "constant kappa gate and matter/source blindness warning",
    },
    {
        "source_file": "10-observer-map-symplectic-contract.md",
        "role": "observer coframe and symplectic/readout contract",
    },
    {
        "source_file": "13-local-closure-PPN-benchmark.md",
        "role": "local closure benchmark requiring universal matter coframe coupling",
    },
    {
        "source_file": "19-constrained-parent-action-skeleton.md",
        "role": "parent action skeleton with one coframe/metric carrier and universal matter coupling",
    },
    {
        "source_file": "204-matter-metric-action-and-ruler-transport-owner-contract.md",
        "role": "matter-frame action and Noether identity route",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv",
        "role": "518 Y5 owner theorem rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv",
        "role": "518 Y5 bound runner inputs",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv",
        "role": "source-normalized Newton stack, especially SN0 same observed frame",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
        "role": "worldtube residual row MR510_5 frame split",
    },
    {
        "source_file": "scripts/fill_Y5_bound_runner_or_source_owner_clause.py",
        "role": "this checkpoint generator",
    },
]


PARENT_CLAUSE_ROWS = [
    {
        "clause_id": "UOC519_0_single_coframe_field",
        "parent_clause": "There is one observed coframe/metric carrier in the local branch.",
        "math_form": "e_obs := e_matter := e_source := e_clock := e_photon := e_orbit",
        "derives": "the frame label cannot be adjusted independently between source, clocks, photons, and orbital readout",
        "current_status": "conditional_clause_written_not_current_MTS_derived",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "UOC519_1_universal_matter_pullback",
        "parent_clause": "All matter species pull back only through e_obs and species constants that are not MTS/domain/source fields.",
        "math_form": "S_m = sum_A S_A[psi_A, e_obs; m_A, q_A, ...], with partial_{Phi,D,kappa_local} m_A = 0",
        "derives": "no direct species-dependent MTS source charge in the matter action",
        "current_status": "conditional_clause_written_not_corpus_proved",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "UOC519_2_readout_uses_same_e",
        "parent_clause": "Clock, photon, ruler, and slow-orbit readout functionals use the same e_obs that defines the source stress.",
        "math_form": "L_clock[e_obs] ; L_photon[e_obs] ; a_orbit from geodesic/readout of g_obs=e_obs^T eta e_obs",
        "derives": "delta_frame_source is forced to zero by construction if the clause is adopted",
        "current_status": "conditional_clause_written_not_current_MTS_derived",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "UOC519_3_source_current_definition",
        "parent_clause": "The Hilbert/source current is defined by variation of the matter action with respect to e_obs before orbital calibration.",
        "math_form": "T_a^mu := e_obs^{-1} delta S_m / delta e_obs^a_mu ; J_H[tau] := T_a^mu tau^a dSigma_mu",
        "derives": "a source-side current exists before measured GM fitting",
        "current_status": "definition_conditional",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "UOC519_4_diffeomorphism_Ward_identity",
        "parent_clause": "If S_m is diffeomorphism invariant and matter equations hold, the matter stress obeys its same-frame Ward identity.",
        "math_form": "E_psi=0 and delta_xi S_m=0 => nabla_mu T_m^{mu nu}=0 in the e_obs geometry",
        "derives": "matter stress is conserved in the same observed frame",
        "current_status": "standard_conditional_not_MTS_full_source_measure",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "UOC519_5_no_conformal_disformal_shadow_frame",
        "parent_clause": "No hidden conformal/disformal/source-frame map may be introduced after the action is varied.",
        "math_form": "g_source != C(Phi) g_orbit and g_clock != C_clock(Phi,D) g_source unless C=1 and derivatives vanish by theorem",
        "derives": "prevents an apparent Newton match from being a frame calibration trick",
        "current_status": "policy_clause_written_theorem_open",
        "valid_for_claim": "false",
    },
    {
        "clause_id": "UOC519_6_dressed_source_guardrail",
        "parent_clause": "The source mass is still a dressed parent/Hilbert/Noether charge, not bare rest mass.",
        "math_form": "M_source != integral_W rho_rest unless binding, field, and boundary dressing terms are included or proved zero",
        "derives": "same coframe does not falsely solve M_eff closure or Gauss calibration",
        "current_status": "guardrail_retained",
        "valid_for_claim": "false",
    },
]


VARIATION_ROWS = [
    {
        "step_id": "VD519_0_action_split",
        "operation": "write the local parent action in one-coframe form",
        "equation": "S_parent = S_grav[e_obs,Phi] + S_silent[Phi,e_obs] + sum_A S_A[psi_A,e_obs] + S_readout[e_obs]",
        "result": "all source/readout variations reference e_obs",
        "claim_status": "conditional_formal",
    },
    {
        "step_id": "VD519_1_source_variation",
        "operation": "define source stress before fitting measured GM",
        "equation": "delta S_m = 1/2 int sqrt(-g_obs) T_m^{mu nu} delta g_obs_mu_nu + E_psi delta psi",
        "result": "T_m is not a phenomenological orbital mass",
        "claim_status": "conditional_formal",
    },
    {
        "step_id": "VD519_2_same_frame_identity",
        "operation": "compare source, clock, photon, and orbit frame variations",
        "equation": "delta_frame_source := delta ln(e_source/e_orbit) = 0 if all functionals use e_obs",
        "result": "Y5B_6 frame split becomes a conditional zero under UOC519",
        "claim_status": "conditional_zero_not_current_MTS_claim",
    },
    {
        "step_id": "VD519_3_species_direct_charge",
        "operation": "differentiate the matter pullback with respect to non-metric MTS fields",
        "equation": "partial_{Phi,D} ln m_A = 0 and partial_{Phi,D} S_A|e_obs fixed = 0",
        "result": "direct species-specific MTS source charge is absent if universal pullback holds",
        "claim_status": "partial_conditional_zero_not_binding_or_dressed_charge",
    },
    {
        "step_id": "VD519_4_Ward_identity",
        "operation": "apply diffeomorphism invariance of S_m",
        "equation": "delta_xi S_m = 0 => nabla_mu T_m^{mu nu} = 0 on matter EOM",
        "result": "same-frame matter conservation follows, but not exterior mass-charge equality",
        "claim_status": "conditional_standard_identity",
    },
    {
        "step_id": "VD519_5_limit_of_clause",
        "operation": "separate what same-coframe proves from what it cannot prove",
        "equation": "delta_frame_source=0 does not imply d(Pi_M J_H)=0, mu_extra=0, or Delta_PPN_source=0",
        "result": "Y5O_1 gets a clean conditional owner; Y5O_3-Y5O_7 remain open",
        "claim_status": "no_Y5_promotion",
    },
]


BOUND_UPDATE_ROWS = [
    {
        "bound_id": "Y5B_6_frame_calibration_split",
        "previous_state": "missing",
        "update_value": "delta_frame_source = 0 if UOC519_0-UOC519_5 are adopted or derived",
        "residual_if_clause_fails": "delta_frame_source remains explicit dimensionless frame/source residual",
        "affected_owner_rows": "Y5O_1",
        "affected_newton_rows": "SN0;SN9;SN10",
        "claim_effect": "conditional_zero_only_no_claim",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_3_species_source_charge",
        "previous_state": "missing",
        "update_value": "direct non-metric species source charge is zero if universal matter pullback has no Phi,D,kappa_A labels",
        "residual_if_clause_fails": "eta_source_AB remains open and must be <= 2.8e-15 or theorem-zero",
        "affected_owner_rows": "Y5O_1;Y5O_5",
        "affected_newton_rows": "SN0;SN7;SN10",
        "claim_effect": "partial_conditional_zero_not_full_source_WEP",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_0_Geff_time_drift",
        "previous_state": "missing",
        "update_value": "same coframe supplies the clock/source frame needed to interpret dln_Geff_dt",
        "residual_if_clause_fails": "Gdot/G cannot be cleanly separated from frame drift",
        "affected_owner_rows": "Y5O_1;Y5O_2",
        "affected_newton_rows": "SN7;SN10",
        "claim_effect": "interpretation_support_only",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_1_Meff_conservation",
        "previous_state": "missing",
        "update_value": "unchanged: same coframe defines J_H but does not prove d(Pi_M J_H)=0",
        "residual_if_clause_fails": "dln_Meff_dt and radial flux remain unowned",
        "affected_owner_rows": "Y5O_3;Y5O_4",
        "affected_newton_rows": "SN3;SN4;SN8",
        "claim_effect": "still_open",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_5_extra_mass_projection",
        "previous_state": "missing",
        "update_value": "unchanged: same coframe does not zero boundary/domain/bulk/non-EH mass projection",
        "residual_if_clause_fails": "mu_extra channel vector remains open",
        "affected_owner_rows": "Y5O_5",
        "affected_newton_rows": "SN6;SN10",
        "claim_effect": "still_open",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_8_full_PPN_source_vector",
        "previous_state": "missing",
        "update_value": "unchanged: same coframe is necessary for PPN but not a second-order PPN expansion",
        "residual_if_clause_fails": "Delta_PPN_source remains open",
        "affected_owner_rows": "Y5O_7",
        "affected_newton_rows": "SN11",
        "claim_effect": "still_open",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D519_0_clause",
        "status": "same_observed_coframe_clause_written",
        "meaning": "Y5O_1 has a clean parent-action sufficient condition: all matter/readout/source variations use one e_obs",
        "claim_status": "conditional_not_current_MTS_derived",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D519_1_frame_bound",
        "status": "frame_split_conditional_zero",
        "meaning": "Y5B_6 can be set to zero only under the UOC519 clause; otherwise it remains a residual row",
        "claim_status": "not_claim_valid",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D519_2_species",
        "status": "direct_species_charge_partially_conditioned",
        "meaning": "universal matter pullback kills direct non-metric species labels but does not yet prove dressed source universality",
        "claim_status": "partial_no_promotion",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D519_3_source_measure",
        "status": "still_open",
        "meaning": "same coframe defines J_H, but it does not prove d(Pi_M J_H)=0, mu_extra=0, Gauss calibration, or PPN stability",
        "claim_status": "Y5_owner_false_for_current_MTS",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D519_4_promotion",
        "status": "forbidden",
        "meaning": "no source-normalized Newton, measured GM, PPN, or local-GR claim is earned",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "Y5O_1_SAME_OBSERVED_COFRAME",
        "previous_status": "not_parent_derived",
        "new_status": "conditional_parent_clause_written_frame_residual_zero_if_adopted",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Y5_BOUND_RUNNER",
        "previous_status": "input_rows_written_all_current_values_missing",
        "new_status": "Y5B_6_frame_split_has_conditional_zero_clause_Y5B_3_partial_direct_charge_clause",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "blocked_until_mu_obs_equals_G0_parent_source_charge_with_no_derivative_hair",
        "new_status": "same_frame_piece_sharpened_but_source_charge_flux_and_Gauss_calibration_still_open",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_Y5_sharpened_to_owner_or_bound_gate",
        "new_status": "still_blocked_same_coframe_clause_needed_but_not_sufficient",
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
    owner_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_OWNER_THEOREM.csv"))
    bound_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv"))
    newton_stack_rows = read_csv(Path("source-intake/mts_residuals/P8_source_normalized_Newton_branch_STACK.csv"))
    frame_rows = [row for row in bound_rows if row.get("bound_id") == "Y5B_6_frame_calibration_split"]
    sn0_rows = [row for row in newton_stack_rows if row.get("rung_id") == "SN0_same_observed_frame"]
    claim_clause_rows = [row for row in PARENT_CLAUSE_ROWS if row["valid_for_claim"] == "true"]
    claim_bound_rows = [row for row in BOUND_UPDATE_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V519_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V519_1_prior_Y5_rows_loaded",
            "result": "pass" if len(owner_rows) >= 9 and len(bound_rows) >= 10 else "fail",
            "detail": f"owner_rows={len(owner_rows)};bound_rows={len(bound_rows)}",
        },
        {
            "check_id": "V519_2_frame_target_loaded",
            "result": "pass" if len(frame_rows) == 1 and len(sn0_rows) == 1 else "fail",
            "detail": f"Y5B_6_rows={len(frame_rows)};SN0_rows={len(sn0_rows)}",
        },
        {
            "check_id": "V519_3_parent_clause_complete",
            "result": "pass" if len(PARENT_CLAUSE_ROWS) == 7 else "fail",
            "detail": f"clause_rows={len(PARENT_CLAUSE_ROWS)}",
        },
        {
            "check_id": "V519_4_variation_derivation_complete",
            "result": "pass" if len(VARIATION_ROWS) == 6 else "fail",
            "detail": f"variation_rows={len(VARIATION_ROWS)}",
        },
        {
            "check_id": "V519_5_bound_update_present",
            "result": "pass" if len(BOUND_UPDATE_ROWS) == 6 else "fail",
            "detail": f"bound_update_rows={len(BOUND_UPDATE_ROWS)}",
        },
        {
            "check_id": "V519_6_no_overclaim",
            "result": "pass" if not claim_clause_rows and not claim_bound_rows else "fail",
            "detail": "same_coframe_derived_for_current_MTS=false; Y5_owner_derived_for_MTS=false; source_normalized_Newton_promoted=false; local_GR_claim_allowed=false",
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
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, Any]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 519 - Fill Y5 Bound Runner or Source Owner Clause

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

This checkpoint attacks the first Y5 owner premise:

```text
e_obs = e_matter = e_source = e_clock = e_photon = e_orbit.
```

The result is useful but not a magic wand:

```text
If the future parent action has one universal observed coframe,
then delta_frame_source = 0 by construction.
```

That gives a real theorem route for the frame-calibration part of Y5. It also gives a clean definition of the Hilbert/source current before measured-GM fitting. But it still does **not** derive `d(Pi_M J_H)=0`, `mu_extra=0`, Gauss/orbital calibration, or second-order PPN stability.

So the source-owner route improves; local GR is not promoted.

## 2. Same-Coframe Parent Clause

{markdown_table(PARENT_CLAUSE_ROWS)}

## 3. Variation Derivation

{markdown_table(VARIATION_ROWS)}

## 4. Bound Runner Update

{markdown_table(BOUND_UPDATE_ROWS)}

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
MTS now has a precise same-observed-coframe parent clause for the Y5 source-owner route.
The frame-split residual has a conditional zero if that clause is adopted or derived.
The source current can be defined by same-frame matter variation under the clause.
```

Forbidden:

```text
MTS has derived the same-coframe clause for the current corpus.
MTS has derived Y5_source_normalization = 0.
MTS has derived measured GM, source-normalized Newton, PPN silence, or local GR.
MTS has equated dressed source mass with bare rest mass.
```

## 10. Next Target

`{NEXT_TARGET}`

Now that the same-frame source current is explicit, the next derivation pressure is whether diffeomorphism/Ward structure plus the parent mass projector can close the actual measured source current:

```text
d(Pi_M J_H)=0
```

or whether `Y5B_1_Meff_conservation` and `Y5B_2_radial_source_hair` must be filled as residual rows.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-fill-Y5-bound-runner-or-source-owner-clause"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (PARENT_CLAUSE_PATH, PARENT_CLAUSE_ROWS),
        (VARIATION_PATH, VARIATION_ROWS),
        (BOUND_UPDATE_PATH, BOUND_UPDATE_ROWS),
        (DECISION_PATH, DECISION_ROWS),
        (VALIDATION_PATH, validations),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
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
        "parent_clause": str(ROOT / PARENT_CLAUSE_PATH),
        "variation_derivation": str(ROOT / VARIATION_PATH),
        "bound_update": str(ROOT / BOUND_UPDATE_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "parent_clause_rows": len(PARENT_CLAUSE_ROWS),
        "variation_rows": len(VARIATION_ROWS),
        "bound_update_rows": len(BOUND_UPDATE_ROWS),
        "failed_validation_rows": len(failed_validations),
        "same_coframe_clause_written": True,
        "same_coframe_derived_for_current_MTS": False,
        "frame_split_zero_if_clause_adopted": True,
        "frame_split_bound_scored": False,
        "direct_species_charge_zero_if_clause_adopted": True,
        "dressed_source_universality_derived": False,
        "Meff_flux_closure_derived": False,
        "Y5_owner_derived_for_MTS": False,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
