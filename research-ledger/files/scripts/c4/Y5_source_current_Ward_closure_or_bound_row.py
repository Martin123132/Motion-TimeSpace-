from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_source_current_Ward_closure_bridge_written_Ward_conservation_insufficient_current_MTS_not_derived_Meff_bound_rows_updated"
CLAIM_CEILING = "Ward_bridge_or_bound_rows_only_no_Meff_closure_measured_GM_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "521-Y5-PiM-projector-owner-or-radial-bound-runner.md"

DOC_PATH = Path("520-Y5-source-current-Ward-closure-or-bound-row.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_WARD_CLOSURE_SOURCE_REGISTER.csv")
WARD_BRIDGE_PATH = Path("source-intake/mts_residuals/P8_Y5_SOURCE_CURRENT_WARD_BRIDGE.csv")
OBSTRUCTION_PATH = Path("source-intake/mts_residuals/P8_Y5_WARD_TO_MASS_FLUX_OBSTRUCTION.csv")
BOUND_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_MEFF_FLUX_BOUND_UPDATE.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_WARD_CLOSURE_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_WARD_CLOSURE_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_WARD_CLOSURE_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "519-fill-Y5-bound-runner-or-source-owner-clause.md",
        "role": "same observed coframe/source-current owner clause and next target",
    },
    {
        "source_file": "518-Y5-source-normalization-owner-or-q_loc-bound-implementation.md",
        "role": "Y5 owner theorem and bound runner input",
    },
    {
        "source_file": "510-worldtube-source-measure-glue-or-Meff-residual-runner.md",
        "role": "worldtube glue and M_eff residual runner",
    },
    {
        "source_file": "509-source-measure-Meff-flux-closure-after-kappa-gate.md",
        "role": "source-measure clauses, including flux closure and measured-GM residual map",
    },
    {
        "source_file": "505-parent-Noether-mass-charge-closure-theorem-or-closure-demotion.md",
        "role": "conditional Noether mass-charge closure theorem",
    },
    {
        "source_file": "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
        "role": "topological current equality attempt",
    },
    {
        "source_file": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
        "role": "exact d(Pi_M J_H) obstruction decomposition",
    },
    {
        "source_file": "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "role": "Pi_M flux closure Ward/topological contract",
    },
    {
        "source_file": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "role": "mass-flux projector Euler/calibration contract",
    },
    {
        "source_file": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
        "role": "Stokes theorem route: closed Pi_M flux implies radial M_eff stability",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "role": "519 same-coframe parent clause rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv",
        "role": "518 Y5 source-normalization bound runner inputs",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
        "role": "M_eff residual runner rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
        "role": "source-measure clause ledger",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv",
        "role": "Ward/topological Pi_M flux closure contract",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv",
        "role": "mass-flux projector Euler/calibration contract",
    },
    {
        "source_file": "scripts/Y5_source_current_Ward_closure_or_bound_row.py",
        "role": "this checkpoint generator",
    },
]


WARD_BRIDGE_ROWS = [
    {
        "bridge_id": "WB520_0_same_frame_source_current",
        "statement": "The same-observed-coframe clause defines a Hilbert/source current before orbital fitting.",
        "math_form": "J_H[tau] := T_m^{mu nu}[e_obs] tau_nu dSigma_mu",
        "what_it_gives": "source current is not purely phenomenological",
        "missing_for_flux_closure": "parent-defined mass projector and mass generator",
        "current_status": "conditional_from_519",
        "valid_for_claim": "false",
    },
    {
        "bridge_id": "WB520_1_matter_Ward_conservation",
        "statement": "Diffeomorphism invariance of same-frame matter gives stress conservation on matter equations.",
        "math_form": "E_psi=0 and delta_xi S_m=0 => nabla_mu T_m^{mu nu}=0",
        "what_it_gives": "ordinary local stress-energy conservation",
        "missing_for_flux_closure": "it does not select a closed scalar mass-channel current by itself",
        "current_status": "standard_conditional",
        "valid_for_claim": "false",
    },
    {
        "bridge_id": "WB520_2_stationary_mass_generator",
        "statement": "Stress conservation becomes mass-current conservation only after a stationary/Hamiltonian observed-time generator is owned.",
        "math_form": "j_M^mu := T_m^{mu nu} tau_nu; nabla_mu j_M^mu = T_m^{mu nu} nabla_(mu tau_nu)",
        "what_it_gives": "if tau is Killing or Hamiltonian-owned, the stress current can be conserved",
        "missing_for_flux_closure": "local stationary tau/Hamiltonian generator not current-MTS-derived",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "bridge_id": "WB520_3_projected_mass_current",
        "statement": "The physical closure target is not Ward conservation alone but closure of the projected mass channel.",
        "math_form": "J_M := Pi_M J_H; dJ_M = d(Pi_M J_H)",
        "what_it_gives": "the exact Y5 M_eff source-flux object",
        "missing_for_flux_closure": "Pi_M parent origin, commutator silence, and no projected exchange",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "bridge_id": "WB520_4_exact_product_obstruction",
        "statement": "The projected current product rule shows why Ward conservation does not automatically close M_eff.",
        "math_form": "d(Pi_M J_H) = Pi_M dJ_H + [d,Pi_M]J_H",
        "what_it_gives": "projector commutator is an explicit possible source of radial mass hair",
        "missing_for_flux_closure": "Pi_M covariantly constant/topological or metric-response cancellation",
        "current_status": "obstruction_active",
        "valid_for_claim": "false",
    },
    {
        "bridge_id": "WB520_5_extra_exchange_obstruction",
        "statement": "Even a conserved Hilbert source can exchange mass projection with non-Hilbert sectors.",
        "math_form": "d(Pi_M J_H) = -Pi_M dJ_extra + [d,Pi_M]J_H + A_parent",
        "what_it_gives": "exact 499 obstruction form carried into Y5",
        "missing_for_flux_closure": "zero extra projection, zero boundary flux, zero parent anomaly",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "bridge_id": "WB520_6_conditional_closure_theorem",
        "statement": "If the mass generator, parent Pi_M, zero commutator, zero exchange projection, and zero boundary/anomaly terms all hold, then d(Pi_M J_H)=0.",
        "math_form": "Ward_M + D Pi_M=0 + Pi_M dJ_extra=0 + A_parent=0 => d(Pi_M J_H)=0",
        "what_it_gives": "conditional Y5B_1/Y5B_2 zero route",
        "missing_for_flux_closure": "current MTS proof of all premises",
        "current_status": "conditional_theorem_written_not_MTS_derived",
        "valid_for_claim": "false",
    },
]


OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "WO520_0_no_stationary_tau",
        "problem": "nabla_mu T^{mu nu}=0 does not give a conserved energy/mass current without a time generator.",
        "math_form": "nabla_mu(T^{mu nu} tau_nu)=T^{mu nu} nabla_(mu tau_nu)",
        "if_open": "M_eff time drift remains an active residual",
        "mapped_rows": "Y5B_1;MR510_0;FC1",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "WO520_1_PiM_not_parent_owned",
        "problem": "Pi_M may be a readout projector rather than a parent-defined charge map.",
        "math_form": "Pi_M fitted after orbit readout cannot define source flux before calibration",
        "if_open": "d(Pi_M J_H)=0 would be closure-only",
        "mapped_rows": "Y5B_1;Y5B_2;MR510_3;MF0",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "WO520_2_projector_commutator",
        "problem": "field/domain/metric dependence of Pi_M creates a product-rule leakage term.",
        "math_form": "[d,Pi_M]J_H != 0",
        "if_open": "radial source hair and projector stress remain open",
        "mapped_rows": "Y5B_2;MR510_3;FC2;FC4",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "WO520_3_extra_mass_projection",
        "problem": "boundary, domain, memory, non-EH, coupling, and frame sectors can carry mass-channel projection.",
        "math_form": "Pi_M dJ_extra != 0",
        "if_open": "mu_extra and radial/range/source residuals remain active",
        "mapped_rows": "Y5B_5;Y5B_4;MR510_4;FC3",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "WO520_4_boundary_improvement_flux",
        "problem": "a total divergence can still carry finite compact-boundary mass flux.",
        "math_form": "int_boundary Pi_M K_owner != 0",
        "if_open": "boundary monopole shifts measured GM",
        "mapped_rows": "Y5B_2;Y5B_5;MR510_2;FC4",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "WO520_5_ad_hoc_multiplier",
        "problem": "adding lambda_M d(Pi_M J_H) solely to force closure imposes the Newton result.",
        "math_form": "S += int lambda_M d(Pi_M J_H) is legal only if lambda_M is gauge/topological/Ward-owned",
        "if_open": "closure is a closure axiom, not a derivation",
        "mapped_rows": "MF2;MF3;FC6",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "WO520_6_calibration_not_closure",
        "problem": "a closed charge is not yet the measured orbital GM.",
        "math_form": "dJ_M=0 does not imply mu_obs=G0 M_source without Gauss/orbital calibration",
        "if_open": "Newton/source-normalization remains unpromoted even if flux closure later lands",
        "mapped_rows": "Y5B_7;Y5B_8;MR510_6;FC7",
        "valid_for_claim": "false",
    },
]


BOUND_UPDATE_ROWS = [
    {
        "bound_id": "Y5B_1_Meff_conservation",
        "previous_state": "missing",
        "ward_result": "same-frame Ward conservation defines the source current but does not close Pi_M J_H",
        "update_value": "conditional_zero_if_WB520_2_to_WB520_6_all_hold",
        "residual_if_clause_fails": "dln_Meff_dt remains required input; use time/radial profile or theorem row closing d(Pi_M J_H)",
        "bound_or_target": "<= 9.6e-15 yr^-1 proxy until a separate GMdot bound is sourced, or derived zero",
        "source_path": "source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
        "claim_effect": "not_scored_no_claim",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_2_radial_source_hair",
        "previous_state": "missing",
        "ward_result": "closed projected mass current would zero finite-shell radial hair by Stokes",
        "update_value": "epsilon_radial_Meff = M_eff^-1 int_A d(Pi_M J_H)",
        "residual_if_clause_fails": "fill radial shell profile or parent identity integral from 499",
        "bound_or_target": "zero radial hair or mapped PPN/fifth-force/orbital residuals",
        "source_path": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
        "claim_effect": "formula_written_not_scored",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_5_extra_mass_projection",
        "previous_state": "missing",
        "ward_result": "Ward conservation of matter does not zero non-Hilbert projected mass exchange",
        "update_value": "mu_extra includes Pi_M dJ_extra, boundary, domain, memory, non-EH, coupling, frame, and anomaly terms",
        "residual_if_clause_fails": "fill channelwise mu_extra coefficients or derive zero projection/no-flux theorems",
        "bound_or_target": "channelwise residuals below gamma/beta/alpha3/xi/Gdot/R11 locks",
        "source_path": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
        "claim_effect": "still_open",
        "valid_for_claim": "false",
    },
    {
        "bound_id": "Y5B_9_q_loc_projection",
        "previous_state": "missing_projection",
        "ward_result": "q_loc can be interpreted as retained projected force/stress-divergence if Ward closure fails",
        "update_value": "C_qmu q_loc must map into d(Pi_M J_H) or Delta_PPN_source before scoring",
        "residual_if_clause_fails": "compact-shell proxy remains dimensionless and not source-normalization units",
        "bound_or_target": "map 7.432631961576971e-06 proxy to Y5/PPN units or keep unscored",
        "source_path": "source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv",
        "claim_effect": "projection_missing",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D520_0_Ward_bridge",
        "status": "conditional_bridge_written",
        "meaning": "same-frame stress Ward identity is necessary but not sufficient for d(Pi_M J_H)=0",
        "claim_status": "not_current_MTS_derived",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D520_1_flux_closure",
        "status": "blocked_by_mass_generator_PiM_exchange_boundary",
        "meaning": "mass-current closure requires stationary/Hamiltonian tau, parent-owned Pi_M, zero commutator, zero extra projection, and zero boundary/anomaly terms",
        "claim_status": "Y5B_1_Y5B_2_open",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D520_2_bound_rows",
        "status": "bound_rows_updated_not_scored",
        "meaning": "M_eff drift and radial source hair now have exact Ward/product-rule residual formulas",
        "claim_status": "test_branch_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D520_3_promotion",
        "status": "forbidden",
        "meaning": "no M_eff closure, measured GM, source-normalized Newton, PPN, or local-GR claim is earned",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "Y5_SOURCE_CURRENT_WARD",
        "previous_status": "same_coframe_source_current_defined_conditionally",
        "new_status": "Ward_to_mass_flux_bridge_written_but_not_current_MTS_derived",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Y5_MEFF_CONSERVATION",
        "previous_status": "dln_Meff_dt_missing",
        "new_status": "conditional_zero_if_mass_generator_PiM_exchange_boundary_clauses_hold_else_residual",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Y5_RADIAL_SOURCE_HAIR",
        "previous_status": "partial_r_ln_mu_obs_missing",
        "new_status": "epsilon_radial_formula_written_from_int_A_dPiMJH_not_scored",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "same_frame_piece_sharpened_but_source_charge_flux_and_Gauss_calibration_still_open",
        "new_status": "still_blocked_by_PiM_owner_flux_closure_extra_projection_and_calibration",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_same_coframe_clause_needed_but_not_sufficient",
        "new_status": "still_blocked_Ward_closure_not_enough_without_mass_channel_projector",
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
    same_coframe_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv"))
    y5_bound_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_NORMALIZATION_BOUND_RUNNER_INPUT.csv"))
    meff_rows = read_csv(Path("source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv"))
    ward_contract_rows = read_csv(Path("source-intake/mts_residuals/P8_PiM_flux_closure_Ward_topological_CONTRACT.csv"))
    mass_flux_rows = read_csv(Path("source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv"))
    y5b1 = [row for row in y5_bound_rows if row.get("bound_id") == "Y5B_1_Meff_conservation"]
    y5b2 = [row for row in y5_bound_rows if row.get("bound_id") == "Y5B_2_radial_source_hair"]
    mr510_0 = [row for row in meff_rows if row.get("residual_id") == "MR510_0_flux_leak"]
    claim_bridge_rows = [row for row in WARD_BRIDGE_ROWS if row["valid_for_claim"] == "true"]
    claim_bound_rows = [row for row in BOUND_UPDATE_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V520_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V520_1_prior_rows_loaded",
            "result": "pass" if len(same_coframe_rows) >= 7 and len(y5_bound_rows) >= 10 and len(meff_rows) >= 8 else "fail",
            "detail": f"same_coframe_rows={len(same_coframe_rows)};y5_bound_rows={len(y5_bound_rows)};meff_rows={len(meff_rows)}",
        },
        {
            "check_id": "V520_2_flux_targets_loaded",
            "result": "pass" if len(y5b1) == 1 and len(y5b2) == 1 and len(mr510_0) == 1 else "fail",
            "detail": f"Y5B_1={len(y5b1)};Y5B_2={len(y5b2)};MR510_0={len(mr510_0)}",
        },
        {
            "check_id": "V520_3_Ward_contracts_loaded",
            "result": "pass" if len(ward_contract_rows) >= 9 and len(mass_flux_rows) >= 9 else "fail",
            "detail": f"Ward_contract_rows={len(ward_contract_rows)};mass_flux_rows={len(mass_flux_rows)}",
        },
        {
            "check_id": "V520_4_bridge_rows_complete",
            "result": "pass" if len(WARD_BRIDGE_ROWS) == 7 else "fail",
            "detail": f"bridge_rows={len(WARD_BRIDGE_ROWS)}",
        },
        {
            "check_id": "V520_5_obstruction_rows_complete",
            "result": "pass" if len(OBSTRUCTION_ROWS) == 7 else "fail",
            "detail": f"obstruction_rows={len(OBSTRUCTION_ROWS)}",
        },
        {
            "check_id": "V520_6_bound_update_rows_present",
            "result": "pass" if len(BOUND_UPDATE_ROWS) == 4 else "fail",
            "detail": f"bound_update_rows={len(BOUND_UPDATE_ROWS)}",
        },
        {
            "check_id": "V520_7_no_overclaim",
            "result": "pass" if not claim_bridge_rows and not claim_bound_rows else "fail",
            "detail": "Ward_closure_derived_for_current_MTS=false; Meff_flux_closure_derived=false; source_normalized_Newton_promoted=false; local_GR_claim_allowed=false",
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
    return f"""# 520 - Y5 Source-Current Ward Closure or Bound Row

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The same-coframe clause from `519` gives a real source current:

```text
J_H[tau] = T_m^{{mu nu}}[e_obs] tau_nu dSigma_mu.
```

It also gives the ordinary Ward identity:

```text
nabla_mu T_m^{{mu nu}}=0.
```

But the hard local-GR source-normalization target is stronger:

```text
d(Pi_M J_H)=0.
```

Ward conservation alone does not prove that. It only reaches the measured source-flux theorem if the parent action also supplies a stationary/Hamiltonian mass generator, a parent-owned `Pi_M`, zero projector commutator, zero extra projected mass exchange, and zero compact boundary/anomaly terms.

So this is progress, not promotion: the exact bridge is written; the `M_eff` and radial-hair rows remain unscored.

## 2. Ward Bridge

{markdown_table(WARD_BRIDGE_ROWS)}

## 3. Obstruction Ledger

{markdown_table(OBSTRUCTION_ROWS)}

## 4. Bound Row Update

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
MTS now has an exact Ward-to-mass-flux bridge contract.
The difference between stress conservation and projected source-flux closure is explicit.
Y5B_1 and Y5B_2 now have exact residual formulas tied to d(Pi_M J_H).
```

Forbidden:

```text
MTS has derived d(Pi_M J_H)=0 for the current parent action.
MTS has derived M_eff conservation or radial source-hair silence.
MTS has derived measured GM, source-normalized Newton, PPN silence, or local GR.
```

## 10. Next Target

`{NEXT_TARGET}`

The next exact pressure point is now `Pi_M`: either derive it as a parent-owned mass projector/charge map with zero commutator, or keep `Y5B_1` and `Y5B_2` as residual inputs.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-source-current-Ward-closure-or-bound-row"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (WARD_BRIDGE_PATH, WARD_BRIDGE_ROWS),
        (OBSTRUCTION_PATH, OBSTRUCTION_ROWS),
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
        "ward_bridge": str(ROOT / WARD_BRIDGE_PATH),
        "obstruction_ledger": str(ROOT / OBSTRUCTION_PATH),
        "bound_update": str(ROOT / BOUND_UPDATE_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "ward_bridge_rows": len(WARD_BRIDGE_ROWS),
        "obstruction_rows": len(OBSTRUCTION_ROWS),
        "bound_update_rows": len(BOUND_UPDATE_ROWS),
        "failed_validation_rows": len(failed_validations),
        "same_frame_source_current_defined": True,
        "matter_Ward_identity_written": True,
        "Ward_closure_derived_for_current_MTS": False,
        "PiM_parent_owned": False,
        "PiM_commutator_zero_derived": False,
        "extra_mass_projection_zero_derived": False,
        "Meff_flux_closure_derived": False,
        "Meff_bound_rows_updated": True,
        "Meff_bound_rows_scored": False,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
