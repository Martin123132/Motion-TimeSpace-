from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_PiM_projector_owner_fork_written_topological_route_conditional_Hodge_route_retained_radial_bound_inputs_updated"
CLAIM_CEILING = "PiM_owner_fork_or_radial_bound_inputs_only_no_Meff_closure_measured_GM_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "522-Y5-extra-mass-projection-silence-or-channelwise-bound.md"

DOC_PATH = Path("521-Y5-PiM-projector-owner-or-radial-bound-runner.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_OWNER_SOURCE_REGISTER.csv")
OWNER_FORK_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_PROJECTOR_OWNER_FORK.csv")
COMMUTATOR_GATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_GATE.csv")
RADIAL_BOUND_INPUT_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_OWNER_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_OWNER_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_OWNER_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "520-Y5-source-current-Ward-closure-or-bound-row.md",
        "role": "selects Pi_M ownership and commutator silence as next exact pressure point",
    },
    {
        "source_file": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "role": "Pi_M parent symplectic/projector algebra attempt",
    },
    {
        "source_file": "456-PiM-projector-variation-stress-ledger.md",
        "role": "Pi_M variation stress/product-rule ledger",
    },
    {
        "source_file": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "role": "Hamiltonian boundary charge mass-current route",
    },
    {
        "source_file": "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
        "role": "topological-Hilbert equality attempt and radial-bound fallback",
    },
    {
        "source_file": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
        "role": "parent source identity obstruction and radial template",
    },
    {
        "source_file": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
        "role": "closed Pi_M flux implies radial M_eff stability theorem route",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_SOURCE_CURRENT_WARD_BRIDGE.csv",
        "role": "520 Ward-to-mass-flux bridge rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_WARD_TO_MASS_FLUX_OBSTRUCTION.csv",
        "role": "520 Ward-to-mass-flux obstruction rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_MEFF_FLUX_BOUND_UPDATE.csv",
        "role": "520 Y5 M_eff/radial bound updates",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv",
        "role": "Pi_M parent algebra contract PM0-PM8",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv",
        "role": "Pi_M variation/stress contract PV0-PV8",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv",
        "role": "499 residual decomposition including projector commutator",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RADIAL_TEMPLATE.csv",
        "role": "499 radial template for identity integral and commutator profile",
    },
    {
        "source_file": "scripts/Y5_PiM_projector_owner_or_radial_bound_runner.py",
        "role": "this checkpoint generator",
    },
]


OWNER_FORK_ROWS = [
    {
        "fork_id": "PF521_0_topological_absolute_PiM",
        "candidate": "Pi_M is parent-derived as metric-independent absolute mass cohomology/charge data",
        "math_form": "Pi_M J = ell_M(J) omega_M_top; d omega_M_top = 0; delta_g omega_M_top = 0; ell_M fixed before readout",
        "would_solve": "zero projector commutator and no bulk projector metric stress",
        "open_debt": "must prove Q_M/ell_M is the same Hilbert source charge and not an independent topological label",
        "current_status": "best_route_conditional_not_current_MTS_derived",
        "valid_for_claim": "false",
    },
    {
        "fork_id": "PF521_1_Hodge_DeWitt_PiM",
        "candidate": "Pi_M is an orthogonal Hodge/DeWitt projector on the boundary/source-current space",
        "math_form": "Pi_M^2=Pi_M; Pi_M^dagger=Pi_M under parent boundary metric G_B",
        "would_solve": "canonical algebra if G_B and the source-current space are parent-owned",
        "open_debt": "delta_g Pi_M and Hodge/Green/boundary metric variation create retained projector stress unless cancelled",
        "current_status": "conditional_algebra_retained_variation_debt",
        "valid_for_claim": "false",
    },
    {
        "fork_id": "PF521_2_Hamiltonian_charge_PiM",
        "candidate": "Pi_M is inherited from the covariant phase-space/Hamiltonian mass charge",
        "math_form": "B_xi/G_eff = M_eff[Pi_M J_H]; delta B_xi = delta int_S Pi_M J_H",
        "would_solve": "ties source projector to a GR-like charge if EH exterior and integrability are derived",
        "open_debt": "EH-only exterior, charge integrability, no extra charge, and Poisson/Gauss calibration remain open",
        "current_status": "downstream_conditional_not_available_yet",
        "valid_for_claim": "false",
    },
    {
        "fork_id": "PF521_3_Euler_multiplier_PiM",
        "candidate": "a multiplier imposes d(Pi_M J_H)=0 directly",
        "math_form": "S_M = int lambda_M d(Pi_M J_H)",
        "would_solve": "formal closure equation",
        "open_debt": "lambda_M and Pi_M need independent gauge/topological/Ward origin and stress ledger",
        "current_status": "rejected_as_derivation_unless_independently_owned",
        "valid_for_claim": "false",
    },
    {
        "fork_id": "PF521_4_readout_or_fit_PiM",
        "candidate": "Pi_M is chosen after orbital data to isolate a good 1/r monopole",
        "math_form": "Pi_M := projector selected by measured GM readout",
        "would_solve": "nothing at derivation level",
        "open_debt": "post-fit projector cannot enter parent source variation or earn theorem credit",
        "current_status": "forbidden_as_derivation",
        "valid_for_claim": "false",
    },
]


COMMUTATOR_GATE_ROWS = [
    {
        "gate_id": "PC521_0_product_rule",
        "condition": "full product rule for projected current is retained",
        "math_form": "d(Pi_M J_H)=Pi_M dJ_H + [d,Pi_M]J_H",
        "pass_if": "Pi_M is fixed/covariantly constant on the local source-current domain or the commutator is explicitly cancelled",
        "current_result": "active_obstruction",
        "maps_to": "Y5B_1;Y5B_2;MR510_3;S499_0",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "PC521_1_variation_rule",
        "condition": "parent variation includes projector variation",
        "math_form": "delta(Pi_M J_H)=Pi_M delta J_H + (delta Pi_M)J_H",
        "pass_if": "delta Pi_M is theorem-zero/topological or retained in stress/residual rows",
        "current_result": "not_parent_derived",
        "maps_to": "PV0;PV5;PV6;R3;R4;R7;R8;R10;R11",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "PC521_2_topological_zero_commutator",
        "condition": "topological absolute charge route fixes Pi_M independent of metric/domain variation",
        "math_form": "d omega_M_top=0 and delta_g Pi_M=0 => [d,Pi_M]J_H=0",
        "pass_if": "the topological mass current is proved equal to Pi_M J_H on shell",
        "current_result": "conditional_but_Hilbert_equality_missing",
        "maps_to": "PF521_0;OB501_0;OB501_2",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "PC521_3_Hodge_variation_retention",
        "condition": "Hodge/DeWitt projector route varies the boundary metric, Green operator, S2 representative, and domain selector",
        "math_form": "delta_g Pi_H(g), delta chi_D, delta n_mu, delta G_B all included",
        "pass_if": "the induced T_PiM is zero/topological or mapped below PPN/source-normalization bounds",
        "current_result": "retained_if_used",
        "maps_to": "PV2;PV3;PV4;PV6",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "PC521_4_no_readout_mask",
        "condition": "post-readout masks never enter S_parent or the source-current Ward derivation",
        "math_form": "delta S_parent/delta Pi_read = 0; Pi_read only acts after theorem or residual scoring",
        "pass_if": "Pi_M appears before readout as parent charge data",
        "current_result": "policy_pass_theorem_open",
        "maps_to": "PV7;PM3;WO520_1",
        "valid_for_claim": "false",
    },
    {
        "gate_id": "PC521_5_closure_not_from_algebra",
        "condition": "Pi_M algebra is not counted as flux closure",
        "math_form": "Pi_M^2=Pi_M does not imply d(Pi_M J_H)=0",
        "pass_if": "a separate Ward/Hamiltonian/topological/Euler mass-current equation is derived",
        "current_result": "no_closure_promotion",
        "maps_to": "PM6;WB520_6;Y5B_1;Y5B_2",
        "valid_for_claim": "false",
    },
]


RADIAL_BOUND_INPUT_ROWS = [
    {
        "input_id": "PI521_0_Delta_PiM",
        "quantity": "Delta_PiM",
        "definition": "projector-ownership/variation residual in the measured source flux",
        "formula": "Delta_PiM = int_S (delta Pi_M)J_H or int_A [d,Pi_M]J_H",
        "required_columns": "system_id;projector_type;metric_dependence_flag;Delta_PiM;units;normalization;source_file;assumptions",
        "maps_to": "Y5B_1_Meff_conservation;Y5B_2_radial_source_hair;MR510_3_projector_hair",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI521_1_commutator_profile",
        "quantity": "I_commutator",
        "definition": "finite-shell integral of the projector commutator obstruction",
        "formula": "I_commutator = int_A_ext [d,Pi_M]J_H",
        "required_columns": "system_id;r1;r2;I_commutator;units;norm_convention;source_file;assumptions",
        "maps_to": "epsilon_radial_Meff = c_M I_commutator/M_eff_ref",
        "current_status": "template_from_499_not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI521_2_projector_stress_vector",
        "quantity": "T_PiM_munu",
        "definition": "metric/domain/boundary stress generated by Pi_M variation if Hodge/DeWitt route is used",
        "formula": "T_PiM_munu := -2/sqrt(-g) delta S_PiM/delta g_munu",
        "required_columns": "operator_family;coefficient;units;weak_field_map;affected_rows;source_file;assumptions",
        "maps_to": "gamma;beta;alpha_i;xi;R11;Y5 source-normalization",
        "current_status": "not_executable",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI521_3_topological_equality_residual",
        "quantity": "R_eq",
        "definition": "failure of topological absolute mass current to equal the observed Hilbert projected source current",
        "formula": "R_eq = Pi_M J_H - J_M_top - dB_zero",
        "required_columns": "system_id;r1;r2;R_eq_integral;units;norm_convention;source_file;assumptions",
        "maps_to": "radial source hair and conserved-wrong-object risk",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PI521_4_radial_decision",
        "quantity": "epsilon_radial_Meff",
        "definition": "radial source-hair envelope after Pi_M ownership failures are integrated",
        "formula": "epsilon_radial_Meff = M_eff_ref^-1 int_A[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent]",
        "required_columns": "system_id;r1;r2;epsilon_radial_Meff;dln_mu_dlnr;bound_source;pass_fail;no_cancellation_flag;notes",
        "maps_to": "Y5B_2 and PPN/fifth-force/orbital radial bounds",
        "current_status": "not_run",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D521_0_PiM_owner",
        "status": "fork_written_not_derived",
        "meaning": "topological, Hodge/DeWitt, Hamiltonian, multiplier, and readout Pi_M routes are separated",
        "claim_status": "no_current_MTS_PiM_owner",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D521_1_best_route",
        "status": "topological_absolute_route_best_conditional",
        "meaning": "a metric-independent absolute mass projector could kill the commutator, but only if it equals the Hilbert source current on shell",
        "claim_status": "conditional_no_promotion",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D521_2_Hodge_route",
        "status": "retained_unless_variation_cancelled",
        "meaning": "Hodge/DeWitt Pi_M cannot be used as local-GR proof unless delta Pi_M stress is included and shown harmless",
        "claim_status": "retained_residual_branch",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D521_3_radial_bound",
        "status": "PiM_bound_inputs_written_not_filled",
        "meaning": "Delta_PiM, commutator profile, projector stress, equality residual, and radial decision rows are explicit",
        "claim_status": "test_branch_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D521_4_promotion",
        "status": "forbidden",
        "meaning": "no d(Pi_M J_H)=0, M_eff closure, measured GM, Newton, PPN, or local-GR claim is earned",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "Y5_PIM_PROJECTOR_OWNER",
        "previous_status": "PiM_parent_owned_false_from_520",
        "new_status": "owner_fork_written_topological_best_Hodge_retained_readout_forbidden",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Y5_MEFF_CONSERVATION",
        "previous_status": "conditional_zero_if_mass_generator_PiM_exchange_boundary_clauses_hold_else_residual",
        "new_status": "still_open_PiM_commutator_and_owner_not_derived",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Y5_RADIAL_SOURCE_HAIR",
        "previous_status": "epsilon_radial_formula_written_from_int_A_dPiMJH_not_scored",
        "new_status": "PiM_commutator_and_Delta_PiM_bound_inputs_written_not_filled",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_by_PiM_owner_flux_closure_extra_projection_and_calibration",
        "new_status": "still_blocked_PiM_owner_not_enough_without_extra_projection_silence_and_calibration",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_Ward_closure_not_enough_without_mass_channel_projector",
        "new_status": "still_blocked_PiM_projector_not_current_MTS_derived",
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
    ward_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_SOURCE_CURRENT_WARD_BRIDGE.csv"))
    obstruction_rows = read_csv(Path("source-intake/mts_residuals/P8_Y5_WARD_TO_MASS_FLUX_OBSTRUCTION.csv"))
    pim_contract_rows = read_csv(Path("source-intake/mts_residuals/P8_PiM_parent_symplectic_projector_algebra_CONTRACT.csv"))
    pv_rows = read_csv(Path("source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv"))
    radial_template_rows = read_csv(Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RADIAL_TEMPLATE.csv"))
    pm5_rows = [row for row in pim_contract_rows if row.get("contract_id") == "PM5_projector_variation_owned"]
    pv0_rows = [row for row in pv_rows if row.get("contract_id") == "PV0_product_variation_included"]
    claim_owner_rows = [row for row in OWNER_FORK_ROWS if row["valid_for_claim"] == "true"]
    claim_radial_rows = [row for row in RADIAL_BOUND_INPUT_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V521_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V521_1_prior_520_rows_loaded",
            "result": "pass" if len(ward_rows) >= 7 and len(obstruction_rows) >= 7 else "fail",
            "detail": f"ward_rows={len(ward_rows)};obstruction_rows={len(obstruction_rows)}",
        },
        {
            "check_id": "V521_2_PiM_contracts_loaded",
            "result": "pass" if len(pim_contract_rows) >= 9 and len(pv_rows) >= 9 else "fail",
            "detail": f"pim_contract_rows={len(pim_contract_rows)};pv_rows={len(pv_rows)}",
        },
        {
            "check_id": "V521_3_variation_targets_loaded",
            "result": "pass" if len(pm5_rows) == 1 and len(pv0_rows) == 1 else "fail",
            "detail": f"PM5_rows={len(pm5_rows)};PV0_rows={len(pv0_rows)}",
        },
        {
            "check_id": "V521_4_radial_template_loaded",
            "result": "pass" if len(radial_template_rows) >= 4 else "fail",
            "detail": f"radial_template_rows={len(radial_template_rows)}",
        },
        {
            "check_id": "V521_5_owner_fork_complete",
            "result": "pass" if len(OWNER_FORK_ROWS) == 5 else "fail",
            "detail": f"owner_fork_rows={len(OWNER_FORK_ROWS)}",
        },
        {
            "check_id": "V521_6_bound_inputs_complete",
            "result": "pass" if len(RADIAL_BOUND_INPUT_ROWS) == 5 else "fail",
            "detail": f"radial_bound_input_rows={len(RADIAL_BOUND_INPUT_ROWS)}",
        },
        {
            "check_id": "V521_7_no_overclaim",
            "result": "pass" if not claim_owner_rows and not claim_radial_rows else "fail",
            "detail": "PiM_parent_owned=false; PiM_commutator_zero_derived=false; Meff_flux_closure_derived=false; source_normalized_Newton_promoted=false; local_GR_claim_allowed=false",
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
    return f"""# 521 - Y5 PiM Projector Owner or Radial Bound Runner

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

This checkpoint asks whether `Pi_M` is a real parent object or a readout mask.

The best non-cheating route is:

```text
Pi_M J = ell_M(J) omega_M_top,
d omega_M_top = 0,
delta_g Pi_M = 0,
```

with `ell_M` fixed before orbital readout and proved equal to the same-frame Hilbert source charge. If that lands, the dangerous commutator term can vanish:

```text
[d,Pi_M]J_H = 0.
```

But current MTS has not derived that equality. Hodge/DeWitt projector algebra remains useful only if `delta Pi_M` stress is retained or cancelled. A fitted/readout projector is rejected as derivation.

So `Pi_M` is sharpened, not promoted. The radial bound inputs for `Delta_PiM`, commutator flux, projector stress, and equality residual are now explicit.

## 2. PiM Owner Fork

{markdown_table(OWNER_FORK_ROWS)}

## 3. Commutator Gate

{markdown_table(COMMUTATOR_GATE_ROWS)}

## 4. Radial Bound Inputs

{markdown_table(RADIAL_BOUND_INPUT_ROWS)}

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
MTS now has an explicit Pi_M owner fork.
The topological absolute-mass projector route is identified as the cleanest conditional route.
Hodge/DeWitt Pi_M is legal only with retained/cancelled variation stress.
Radial bound inputs for Pi_M failure modes are explicit.
```

Forbidden:

```text
MTS has derived Pi_M as a parent-owned mass projector in the current corpus.
MTS has derived [d,Pi_M]J_H=0.
MTS has derived d(Pi_M J_H)=0, M_eff closure, measured GM, source-normalized Newton, PPN silence, or local GR.
```

## 10. Next Target

`{NEXT_TARGET}`

Even a good `Pi_M` is not enough if boundary/domain/memory/non-EH sectors carry projected mass. Next target is zero extra mass projection or channelwise bound input.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-PiM-projector-owner-or-radial-bound-runner"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (OWNER_FORK_PATH, OWNER_FORK_ROWS),
        (COMMUTATOR_GATE_PATH, COMMUTATOR_GATE_ROWS),
        (RADIAL_BOUND_INPUT_PATH, RADIAL_BOUND_INPUT_ROWS),
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
        "owner_fork": str(ROOT / OWNER_FORK_PATH),
        "commutator_gate": str(ROOT / COMMUTATOR_GATE_PATH),
        "radial_bound_input": str(ROOT / RADIAL_BOUND_INPUT_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "owner_fork_rows": len(OWNER_FORK_ROWS),
        "commutator_gate_rows": len(COMMUTATOR_GATE_ROWS),
        "radial_bound_input_rows": len(RADIAL_BOUND_INPUT_ROWS),
        "failed_validation_rows": len(failed_validations),
        "PiM_owner_fork_written": True,
        "PiM_parent_owned": False,
        "PiM_topological_route_conditional": True,
        "PiM_Hodge_route_retained_unless_variation_cancelled": True,
        "PiM_readout_route_forbidden_as_derivation": True,
        "PiM_commutator_zero_derived": False,
        "Delta_PiM_bound_inputs_written": True,
        "PiM_bound_inputs_filled": False,
        "Meff_flux_closure_derived": False,
        "source_normalized_Newton_promoted": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
