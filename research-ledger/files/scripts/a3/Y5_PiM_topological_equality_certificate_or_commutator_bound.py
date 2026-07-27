from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_PiM_topological_equality_certificate_written_commutator_bound_template_active_no_epsilon_charge_or_Newton_promotion"
CLAIM_CEILING = "PiM_topological_equality_certificate_or_commutator_bound_only_no_epsilon_charge_measured_GM_Newton_PPN_or_local_GR_pass"
NEXT_TARGET = "535-Y5-PiM-commutator-bound-runner-or-Hilbert-worldtube-glue.md"

DOC_PATH = Path("534-Y5-PiM-topological-equality-certificate-or-commutator-bound.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_TOPO_EQUALITY_SOURCE_REGISTER.csv")
CERTIFICATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_TOPO_EQUALITY_CERTIFICATE.csv")
COMMUTATOR_BOUND_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_BOUND_TEMPLATE.csv")
EPSILON_CHARGE_MAP_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_TO_EPSILON_CHARGE_MAP.csv")
ACCEPTANCE_GATES_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_TOPO_EQUALITY_ACCEPTANCE_GATES.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_TOPO_EQUALITY_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_TOPO_EQUALITY_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_PIM_TOPO_EQUALITY_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "533-Y5-epsilon-charge-first-row-runner-or-source-current-theorem.md",
        "role": "selects Pi_M equality/commutator as the next epsilon_charge bottleneck",
    },
    {
        "source_file": "532-Y5-measured-GM-source-current-closure-or-first-input-fill.md",
        "role": "defines source-current closure rungs SC532_3 and SC532_4",
    },
    {
        "source_file": "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
        "role": "Pi_M owner fork, commutator gate, and radial bound inputs",
    },
    {
        "source_file": "501-topological-Hilbert-current-equality-or-radial-bound-runner.md",
        "role": "topological-Hilbert equality attempt and equality residual template",
    },
    {
        "source_file": "500-topological-PiM-current-parent-clause-or-radial-bound-runner.md",
        "role": "topological Pi_M parent clause and closure conditions",
    },
    {
        "source_file": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
        "role": "parent source identity and commutator/extra/anomaly radial numerator",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_THEOREM_CERTIFICATE_TEMPLATE.csv",
        "role": "533 theorem certificate rows for epsilon_charge",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_EVALUATOR.csv",
        "role": "533 epsilon_charge evaluator",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_PROJECTOR_OWNER_FORK.csv",
        "role": "521 Pi_M owner fork machine rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_GATE.csv",
        "role": "521 Pi_M commutator gate machine rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
        "role": "521 Pi_M radial/commutator/equality input rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_PARENT_CLAUSE_ATTEMPT.csv",
        "role": "500 topological Pi_M parent clause rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv",
        "role": "500 topological Pi_M closure conditions",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv",
        "role": "501 topological-Hilbert equality rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv",
        "role": "501 topological-Hilbert equality obstructions",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RADIAL_TEMPLATE.csv",
        "role": "499 radial fallback template",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PiM_projector_variation_stress_CONTRACT.csv",
        "role": "456 Pi_M variation/stress contract",
    },
    {
        "source_file": "scripts/Y5_PiM_topological_equality_certificate_or_commutator_bound.py",
        "role": "this checkpoint generator",
    },
]


CERTIFICATE_ROWS = [
    {
        "certificate_id": "PTEC534_0_fixed_parent_domain",
        "required_identity": "compact source/exterior domain and S2 class are fixed by parent topology before readout",
        "math_form": "Sigma_ext ~= S2 x I; [S2]_M selected without metric/readout/domain-fit dependence",
        "closes": "readout-mask and preferred-domain loophole",
        "current_status": "conditional_open_not_certificate",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "PTEC534_1_metric_independent_projector",
        "required_identity": "Pi_M is metric-independent topological charge data, not a Hodge/DeWitt metric projector",
        "math_form": "delta_g Pi_M=0; Pi_M J = ell_M(J) omega_M_top",
        "closes": "bulk projector stress and Hodge variation leakage",
        "current_status": "conditional_route_not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "PTEC534_2_closed_representative",
        "required_identity": "topological representative is closed and normalized",
        "math_form": "d omega_M_top=0; integral_S2 omega_M_top=1",
        "closes": "commutator if Pi_M is fixed on the current space",
        "current_status": "formal_topological_clause_only",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "PTEC534_3_Hilbert_defined_charge",
        "required_identity": "the topological charge scalar is defined from the same Hilbert compact-source worldtube",
        "math_form": "Q_M = integral_{Sigma_source} rho_H dV before readout; J_M_top=Q_M omega_M_top",
        "closes": "conserved-wrong-object failure",
        "current_status": "not_derived_parent_worldtube_glue_missing",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "PTEC534_4_topological_Hilbert_equality",
        "required_identity": "projected Hilbert current equals the closed topological current up to exact zero-boundary term",
        "math_form": "Pi_M J_H = J_M_top + dB_zero with integral_boundary dB_zero=0",
        "closes": "epsilon_PiM_equality and topological wrong-charge risk",
        "current_status": "not_derived_key_blocker",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "PTEC534_5_commutator_zero",
        "required_identity": "projected-current product rule has no commutator leakage",
        "math_form": "[d,Pi_M]J_H=0",
        "closes": "epsilon_commutator and radial source hair",
        "current_status": "not_derived_bound_template_required",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "PTEC534_6_no_projector_stress",
        "required_identity": "Pi_M variation creates no independent stress or retained Hodge/domain residue",
        "math_form": "T_PiM_munu=-2/sqrt(-g) delta S_PiM/delta g_munu=0 or not present",
        "closes": "R3/R4/R7/R8/R10/R11 projector stress leakage",
        "current_status": "not_derived_Hodge_route_retained_if_used",
        "valid_for_claim": "false",
    },
    {
        "certificate_id": "PTEC534_7_no_multiplier_or_readout_cheat",
        "required_identity": "no late equality multiplier or post-fit Pi_M is used to impose Newton closure",
        "math_form": "Pi_M appears in S_parent before readout; no lambda_eq-only closure",
        "closes": "closure axiom masquerading as derivation",
        "current_status": "policy_pass_theorem_open",
        "valid_for_claim": "false",
    },
]


COMMUTATOR_BOUND_TEMPLATE_ROWS = [
    {
        "input_id": "PCB534_0_equality_residual",
        "quantity": "R_eq_integral",
        "formula": "int_A_ext (Pi_M J_H - J_M_top - dB_zero)",
        "required_columns": "system_id;r1;r2;R_eq_integral;M_H_ref;units;norm_convention;source_file;assumptions",
        "maps_to": "epsilon_PiM_equality=R_eq_integral/M_H_ref",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PCB534_1_commutator_integral",
        "quantity": "I_commutator",
        "formula": "int_A_ext [d,Pi_M]J_H",
        "required_columns": "system_id;r1;r2;projector_type;metric_dependence_flag;I_commutator;M_H_ref;units;source_file;assumptions",
        "maps_to": "epsilon_commutator=I_commutator/M_H_ref; epsilon_radial_Meff; projector stress rows",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PCB534_2_projector_stress",
        "quantity": "T_PiM_munu",
        "formula": "-2/sqrt(-g) delta S_PiM/delta g_munu",
        "required_columns": "operator_family;coefficient;units;weak_field_map;affected_rows;source_file;assumptions",
        "maps_to": "gamma;beta;alpha_i;xi;R11;source-normalization",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PCB534_3_exact_boundary_term",
        "quantity": "B_zero_flux",
        "formula": "int_boundary dB_zero",
        "required_columns": "system_id;boundary_type;B_zero_flux;M_H_ref;units;source_file;assumptions",
        "maps_to": "boundary monopole shift; epsilon_PiM_equality; radial source hair",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "input_id": "PCB534_4_decision",
        "quantity": "PiM_equality_commutator_decision",
        "formula": "sum_abs(|epsilon_PiM_equality|+|epsilon_commutator|+|epsilon_projector_stress_map|+|epsilon_boundary_exact|)",
        "required_columns": "all_components_filled;no_cancellation_flag;pass_fail;bound_source;notes",
        "maps_to": "SRC523_0 epsilon_charge and SRC523_6/SRC523_8 source/radial rows",
        "current_status": "not_run",
        "valid_for_claim": "false",
    },
]


EPSILON_CHARGE_MAP_ROWS = [
    {
        "map_id": "PECM534_0_if_certificate_passes",
        "condition": "PTEC534_0..PTEC534_7 all source-backed and valid_for_claim",
        "epsilon_charge_effect": "sets epsilon_PiM_equality=0 and epsilon_commutator=0 for the Pi_M part of SRC523_0",
        "remaining_debt": "observed-time Hamiltonian normalization, extra projection, G_eff normalization, Poisson/Gauss/orbital calibration",
        "current_status": "not_available",
        "valid_for_claim": "false",
    },
    {
        "map_id": "PECM534_1_if_equality_missing",
        "condition": "Pi_M J_H != J_M_top or R_eq unfilled",
        "epsilon_charge_effect": "epsilon_PiM_equality remains in epsilon_charge_abs_envelope",
        "remaining_debt": "fill R_eq_integral or derive worldtube Hilbert glue",
        "current_status": "active",
        "valid_for_claim": "false",
    },
    {
        "map_id": "PECM534_2_if_commutator_missing",
        "condition": "[d,Pi_M]J_H unfilled or nonzero",
        "epsilon_charge_effect": "epsilon_commutator feeds source-current/radial residual rows",
        "remaining_debt": "fill I_commutator and projector stress map",
        "current_status": "active",
        "valid_for_claim": "false",
    },
    {
        "map_id": "PECM534_3_if_Hodge_route_used",
        "condition": "Pi_M uses Hodge/DeWitt/boundary metric projector",
        "epsilon_charge_effect": "claim blocked unless delta_g Pi_M stress is retained and below local locks",
        "remaining_debt": "T_PiM weak-field map to R3/R4/R7/R8/R10/R11",
        "current_status": "retained_if_used",
        "valid_for_claim": "false",
    },
    {
        "map_id": "PECM534_4_if_readout_or_multiplier_used",
        "condition": "Pi_M chosen post-readout or equality imposed by unowned multiplier",
        "epsilon_charge_effect": "no derivation credit; row demotes to closure/residual branch",
        "remaining_debt": "must label as closure or supply independent gauge/topological origin",
        "current_status": "forbidden_as_derivation",
        "valid_for_claim": "false",
    },
]


ACCEPTANCE_GATE_ROWS = [
    {
        "gate_id": "AG534_0_certificate_completeness",
        "pass_condition": "all eight Pi_M topological-equality certificate rows are source-backed and claim-valid",
        "current_result": "fail_missing_certificates",
        "claim_effect": "no epsilon_charge theorem-zero",
    },
    {
        "gate_id": "AG534_1_no_wrong_conserved_object",
        "pass_condition": "Q_M is defined from the same Hilbert compact-source worldtube, not an independent topological label",
        "current_result": "fail_worldtube_glue_missing",
        "claim_effect": "J_M_top closure cannot close Pi_M J_H",
    },
    {
        "gate_id": "AG534_2_commutator_or_bound",
        "pass_condition": "[d,Pi_M]J_H=0 theorem or source-backed I_commutator bound exists",
        "current_result": "fail_unfilled",
        "claim_effect": "source-current and radial rows stay open",
    },
    {
        "gate_id": "AG534_3_projector_stress_guard",
        "pass_condition": "Hodge/metric/domain Pi_M stress is absent, theorem-cancelled, or mapped below locks",
        "current_result": "fail_if_Hodge_used",
        "claim_effect": "blocks local-GR and R11 promotion",
    },
    {
        "gate_id": "AG534_4_no_overclaim",
        "pass_condition": "no Pi_M equality/commutator row grants measured-GM/Newton/local-GR credit before source evidence",
        "current_result": "pass_policy_enforced",
        "claim_effect": "private checkpoint safe",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D534_0_certificate_written",
        "status": "PiM_topological_equality_certificate_written",
        "meaning": "the exact parent-owned Pi_M equality certificate needed by epsilon_charge is explicit",
        "claim_status": "not_satisfied",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D534_1_commutator_template",
        "status": "commutator_bound_template_written",
        "meaning": "if equality is not derived, R_eq and I_commutator have executable bound rows",
        "claim_status": "template_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D534_2_current_MTS",
        "status": "worldtube_Hilbert_glue_missing",
        "meaning": "current MTS still risks a conserved wrong object rather than the observed Hilbert mass channel",
        "claim_status": "epsilon_charge_false",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D534_3_no_promotion",
        "status": "no_epsilon_charge_measured_GM_Newton_or_local_GR_promotion",
        "meaning": "this is a certificate/bound gate, not a proof that the gate passes",
        "claim_status": "safe_private_work",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D534_4_private_no_push",
        "status": "private_no_github",
        "meaning": "no public/GitHub action is performed",
        "claim_status": "safe_private_work",
        "next_action": "continue_private_derivation",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "PIM_PROJECTOR",
        "previous_status": "next_target_topological_equality_or_commutator_bound",
        "new_status": "topological_equality_certificate_written_commutator_bound_template_active",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SRC523_0_EPSILON_CHARGE",
        "previous_status": "runner_written_inputs_missing",
        "new_status": "still_blocked_by_PiM_equality_and_commutator_inputs",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_SRC523_0_runner_has_no_input",
        "new_status": "still_blocked_PiM_certificate_or_bound_unfilled",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_first_source_score_row_unfilled",
        "new_status": "still_blocked_measured_GM_source_current_PiM_gate",
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
    epsilon_eval = read_csv(Path("source-intake/mts_residuals/P8_Y5_EPSILON_CHARGE_EVALUATOR.csv"))
    owner_fork = read_csv(Path("source-intake/mts_residuals/P8_Y5_PIM_PROJECTOR_OWNER_FORK.csv"))
    comm_gate = read_csv(Path("source-intake/mts_residuals/P8_Y5_PIM_COMMUTATOR_GATE.csv"))
    topo_clause = read_csv(Path("source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_PARENT_CLAUSE_ATTEMPT.csv"))
    hilbert_eq = read_csv(Path("source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv"))
    radial_template = read_csv(Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RADIAL_TEMPLATE.csv"))
    claim_cert_rows = [row for row in CERTIFICATE_ROWS if row["valid_for_claim"] == "true"]
    claim_bound_rows = [row for row in COMMUTATOR_BOUND_TEMPLATE_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V534_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V534_1_prior_epsilon_runner_loaded",
            "result": "pass" if len(epsilon_eval) >= 2 else "fail",
            "detail": f"epsilon_eval_rows={len(epsilon_eval)}",
        },
        {
            "check_id": "V534_2_PiM_prior_rows_loaded",
            "result": "pass" if len(owner_fork) >= 5 and len(comm_gate) >= 6 else "fail",
            "detail": f"owner_fork_rows={len(owner_fork)};comm_gate_rows={len(comm_gate)}",
        },
        {
            "check_id": "V534_3_topological_rows_loaded",
            "result": "pass" if len(topo_clause) >= 7 and len(hilbert_eq) >= 6 else "fail",
            "detail": f"topo_clause_rows={len(topo_clause)};hilbert_eq_rows={len(hilbert_eq)}",
        },
        {
            "check_id": "V534_4_radial_template_loaded",
            "result": "pass" if len(radial_template) >= 4 else "fail",
            "detail": f"radial_template_rows={len(radial_template)}",
        },
        {
            "check_id": "V534_5_certificate_and_bound_rows_written",
            "result": "pass" if len(CERTIFICATE_ROWS) == 8 and len(COMMUTATOR_BOUND_TEMPLATE_ROWS) == 5 else "fail",
            "detail": f"certificate_rows={len(CERTIFICATE_ROWS)};bound_rows={len(COMMUTATOR_BOUND_TEMPLATE_ROWS)}",
        },
        {
            "check_id": "V534_6_no_claim_rows",
            "result": "pass" if not claim_cert_rows and not claim_bound_rows else "fail",
            "detail": f"claim_cert_rows={len(claim_cert_rows)};claim_bound_rows={len(claim_bound_rows)}",
        },
        {
            "check_id": "V534_7_no_overclaim",
            "result": "pass" if not claim_cert_rows and not claim_bound_rows else "fail",
            "detail": "PiM_parent_owned=false; PiM_Hilbert_equality=false; commutator_zero=false; epsilon_charge_filled=false; local_GR_claim_allowed=false",
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
    return f"""# 534 - Y5 PiM Topological Equality Certificate or Commutator Bound

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

The `Pi_M` route now has a sharper referee card.

The topological route is promising only if it proves:

```text
Pi_M J_H = J_M_top + dB_zero,
integral_boundary dB_zero = 0,
[d,Pi_M]J_H = 0.
```

Current MTS does not yet prove this. A closed topological current can still be the wrong conserved object. Therefore the commutator/equality residual branch remains active and fillable.

## 2. Topological Equality Certificate

{markdown_table(CERTIFICATE_ROWS)}

## 3. Commutator Bound Template

{markdown_table(COMMUTATOR_BOUND_TEMPLATE_ROWS)}

## 4. Epsilon-Charge Map

{markdown_table(EPSILON_CHARGE_MAP_ROWS)}

## 5. Acceptance Gates

{markdown_table(ACCEPTANCE_GATE_ROWS)}

## 6. Decision

{markdown_table(DECISION_ROWS)}

## 7. Source Register

{markdown_table(sources)}

## 8. Validation

{markdown_table(validations)}

## 9. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 10. Claim Ceiling

Allowed:

```text
The Pi_M topological-equality certificate is explicit.
The commutator/equality bound template is explicit.
Current MTS has not proved Pi_M J_H = J_M_top or [d,Pi_M]J_H = 0.
```

Forbidden:

```text
MTS has filled epsilon_charge.
MTS has derived measured GM, source-normalized Newton, beta, PPN, or local GR.
```

## 11. Practical Read

This is the exact place where a nice mathematical object can fool us. A conserved topological mass current is only useful for Newton if it is the Hilbert source mass current that matter/orbits actually read. Until that equality lands, `Pi_M` is a controlled residual route, not a GR derivation.

## 12. Next Target

`{NEXT_TARGET}`

Next: either build the commutator/equality bound runner, or derive the Hilbert-worldtube glue that turns `J_M_top` into the same source current used by the observed matter branch.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-PiM-topological-equality-certificate-or-commutator-bound"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (CERTIFICATE_PATH, CERTIFICATE_ROWS),
        (COMMUTATOR_BOUND_TEMPLATE_PATH, COMMUTATOR_BOUND_TEMPLATE_ROWS),
        (EPSILON_CHARGE_MAP_PATH, EPSILON_CHARGE_MAP_ROWS),
        (ACCEPTANCE_GATES_PATH, ACCEPTANCE_GATE_ROWS),
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
        "certificate": str(ROOT / CERTIFICATE_PATH),
        "commutator_bound_template": str(ROOT / COMMUTATOR_BOUND_TEMPLATE_PATH),
        "epsilon_charge_map": str(ROOT / EPSILON_CHARGE_MAP_PATH),
        "acceptance_gates": str(ROOT / ACCEPTANCE_GATES_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "failed_validation_rows": len(failed_validations),
        "certificate_rows": len(CERTIFICATE_ROWS),
        "commutator_bound_rows": len(COMMUTATOR_BOUND_TEMPLATE_ROWS),
        "PiM_topological_equality_certificate_written": True,
        "PiM_parent_owned_derived_for_MTS": False,
        "PiM_Hilbert_equality_derived_for_MTS": False,
        "PiM_commutator_zero_derived": False,
        "epsilon_charge_filled": False,
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
        "done\nprivate_no_github\nno_epsilon_charge_measured_GM_Newton_PPN_or_local_GR_promotion\n",
        encoding="utf-8",
    )

    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
