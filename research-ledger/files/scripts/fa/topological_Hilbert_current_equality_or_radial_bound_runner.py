from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "topological_Hilbert_current_equality_attempt_written_parent_glue_not_derived_radial_bound_runner_input_template_written_no_Newton_or_local_GR_promotion"
CLAIM_CEILING = "topological_Hilbert_equality_attempt_only_no_closed_Hilbert_flux_no_mu_extra_zero_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "502-radial-bound-runner-implementation-or-Hilbert-topological-glue.md"

DOC_PATH = Path("501-topological-Hilbert-current-equality-or-radial-bound-runner.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_SOURCE_REGISTER.csv")
EQUALITY_ATTEMPT_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ATTEMPT.csv")
OBSTRUCTION_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_OBSTRUCTIONS.csv")
ROUTE_TEST_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ROUTE_TESTS.csv")
BOUND_INPUT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_INPUT_TEMPLATE.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_HILBERT_EQUALITY_ROUTE_UPDATE.csv")

TOPOLOGICAL_PIM_CLAUSE_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_PARENT_CLAUSE_ATTEMPT.csv")
TOPOLOGICAL_PIM_CONDITIONS_PATH = Path("source-intake/mts_residuals/P8_TOPOLOGICAL_PIM_CLOSURE_CONDITIONS.csv")
RADIAL_BOUND_SPEC_PATH = Path("source-intake/mts_residuals/P8_RADIAL_BOUND_RUNNER_SPEC.csv")
SOURCE_WARD_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_source_current_Ward_universality_CONTRACT.csv")
HILBERT_MONOPOLE_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_Hilbert_monopole_calibration_CONTRACT.csv")
MASS_FLUX_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_mass_flux_projector_Euler_calibration_CONTRACT.csv")
SOURCE_OWNER_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_source_owner_parent_action_terms_CONTRACT.csv")
Q_RETAINED_CONTRACT_PATH = Path("source-intake/mts_residuals/P8_q_retained_zero_conditions_CONTRACT.csv")


SOURCE_REGISTER = [
    {
        "source_file": "500-topological-PiM-current-parent-clause-or-radial-bound-runner.md",
        "role": "selects Hilbert equality as the next exact topological Pi_M theorem",
    },
    {
        "source_file": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
        "role": "identity decomposition and radial numerator to be bounded if equality fails",
    },
    {
        "source_file": "445-measured-GM-Ward-source-ownership-theorem-attempt.md",
        "role": "Ward/Bianchi source ownership caveat",
    },
    {
        "source_file": "446-source-owner-current-parent-action-contract.md",
        "role": "parent action terms needed for K_owner and q_retained zero",
    },
    {
        "source_file": "449-source-current-Ward-universality-theorem-attempt.md",
        "role": "conditional Hilbert/coframe source current theorem",
    },
    {
        "source_file": "450-Hilbert-source-to-measured-monopole-calibration-gate.md",
        "role": "Hilbert current to measured monopole calibration blockers",
    },
    {
        "source_file": "451-mass-flux-projector-Euler-calibration-attempt.md",
        "role": "mass-flux projector Euler closure and no-ad-hoc multiplier warning",
    },
    {
        "source_file": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "measured-GM calibration guardrails after any charge equality",
    },
    {
        "source_file": str(TOPOLOGICAL_PIM_CLAUSE_PATH),
        "role": "500 topological PiM parent clause attempt",
    },
    {
        "source_file": str(TOPOLOGICAL_PIM_CONDITIONS_PATH),
        "role": "500 topological PiM closure conditions",
    },
    {
        "source_file": str(RADIAL_BOUND_SPEC_PATH),
        "role": "500 radial bound runner spec",
    },
    {
        "source_file": str(SOURCE_WARD_CONTRACT_PATH),
        "role": "449 source-current Ward universality contract",
    },
    {
        "source_file": str(HILBERT_MONOPOLE_CONTRACT_PATH),
        "role": "450 Hilbert-to-monopole calibration contract",
    },
    {
        "source_file": str(MASS_FLUX_CONTRACT_PATH),
        "role": "451 mass-flux projector contract",
    },
    {
        "source_file": str(SOURCE_OWNER_CONTRACT_PATH),
        "role": "446 source-owner parent-action contract",
    },
    {
        "source_file": str(Q_RETAINED_CONTRACT_PATH),
        "role": "446 q-retained zero condition contract",
    },
    {
        "source_file": "scripts/topological_Hilbert_current_equality_or_radial_bound_runner.py",
        "role": "this checkpoint generator",
    },
]


EQUALITY_ATTEMPT_ROWS = [
    {
        "attempt_id": "EH501_0_equality_statement",
        "target": "topological-Hilbert equality",
        "mathematical_form": "Pi_M J_H = J_M_top + dB_zero + R_eq",
        "status": "identity_target_written",
        "would_close": "if R_eq=0 and boundary integral of dB_zero is zero, closed J_M_top gives closed Pi_M J_H",
        "current_blocker": "R_eq is not parent-derived zero",
        "valid_for_claim": "false",
    },
    {
        "attempt_id": "EH501_1_worldtube_charge_route",
        "target": "define Q_M from the same compact Hilbert source worldtube",
        "mathematical_form": "Q_M = integral_{Sigma_source} rho_H dV, J_M_top = PD(worldtube Hilbert charge)",
        "status": "best_noncheat_route_conditional",
        "would_close": "makes the topological charge the same object as Hilbert matter mass, not an independent label",
        "current_blocker": "parent worldtube/domain selector and source measure are not derived without readout or preferred-frame leakage",
        "valid_for_claim": "false",
    },
    {
        "attempt_id": "EH501_2_Ward_current_route",
        "target": "separate Hilbert mass current conservation",
        "mathematical_form": "nabla_mu T_H^{mu nu}=0 plus observed time/current map gives d(Pi_M J_H)=0",
        "status": "conditional_sublemma_only",
        "would_close": "could identify the Hilbert mass current with a closed topological current if no exchange survives",
        "current_blocker": "hidden/boundary/domain/nonHilbert exchange and boundary flux are not zero",
        "valid_for_claim": "false",
    },
    {
        "attempt_id": "EH501_3_parent_glue_clause",
        "target": "parent equality glue",
        "mathematical_form": "S_glue = int Lambda_eq wedge (Pi_M J_H - J_M_top - dB_zero)",
        "status": "closure_only_without_independent_origin",
        "would_close": "Euler equation would impose equality directly",
        "current_blocker": "without independent gauge/topological/source reason, this is a multiplier relabel of Newton closure",
        "valid_for_claim": "false",
    },
    {
        "attempt_id": "EH501_4_Hamiltonian_charge_route",
        "target": "boundary charge equality",
        "mathematical_form": "B_xi/G_parent = Q_M = M_eff[Pi_M J_H]",
        "status": "conditional_downstream_route",
        "would_close": "would identify topological charge, Hilbert projected mass, and Hamiltonian boundary charge",
        "current_blocker": "requires EH constraint algebra, boundary integrability, no extra charge, and Gauss/orbital calibration",
        "valid_for_claim": "false",
    },
    {
        "attempt_id": "EH501_5_radial_bound_fallback",
        "target": "if equality fails, bound R_eq and source-current numerator",
        "mathematical_form": "I_parent_radial = int_A_ext dR_eq + residual channels",
        "status": "fallback_template_written",
        "would_close": "does not close theorem; makes the row testable",
        "current_blocker": "numeric/source-backed residual inputs are not filled",
        "valid_for_claim": "false",
    },
]


OBSTRUCTION_ROWS = [
    {
        "obstruction_id": "OB501_0_independent_topological_label",
        "obstruction": "Q_M is an independent topological label rather than the Hilbert source charge",
        "required_zero_or_repair": "define Q_M from same-frame Hilbert source variation before readout",
        "current_status": "not_parent_derived",
        "affected_rows": "R1;R4;R9;R11",
        "fallback": "treat J_M_top as conserved wrong object; retain radial/source-normalization rows",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "OB501_1_worldtube_domain_selection",
        "obstruction": "source worldtube or S2 class is chosen by local metric/readout/domain rule",
        "required_zero_or_repair": "covariant/topological parent domain selector fixed before scoring",
        "current_status": "not_parent_derived",
        "affected_rows": "R5;R6;R8;R9;R11",
        "fallback": "preferred-frame/location/domain residuals remain active",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "OB501_2_boundary_improvement",
        "obstruction": "Pi_M J_H differs from J_M_top by a boundary/improvement term with nonzero compact flux",
        "required_zero_or_repair": "dB_zero exact with zero boundary integral, or class-only universal constant calibration",
        "current_status": "fail_open",
        "affected_rows": "R3;R4;R7;R8;R9;R11",
        "fallback": "boundary monopole/radial flux coefficient row",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "OB501_3_hidden_exchange",
        "obstruction": "observed Hilbert matter exchanges mass-channel current with hidden/bulk/domain/nonEH sectors",
        "required_zero_or_repair": "Pi_M dJ_extra=0 from legal owner/topological/no-hair route",
        "current_status": "not_parent_derived",
        "affected_rows": "R3;R4;R7;R8;R10;R11",
        "fallback": "channelwise residual integrals in radial bound runner",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "OB501_4_universal_kappa_and_calibration",
        "obstruction": "equality of currents still lacks measured-GM normalization or constant G",
        "required_zero_or_repair": "Q_M=M_EH and G_parent constant/universal with no derivatives",
        "current_status": "not_parent_derived",
        "affected_rows": "R1;R4;R9;R10;R11",
        "fallback": "calibration and Gdot/range/source residual rows",
        "valid_for_claim": "false",
    },
    {
        "obstruction_id": "OB501_5_second_order_stability",
        "obstruction": "first-order equality may fail at PPN beta/source order",
        "required_zero_or_repair": "delta_beta_source=0 after same measured-GM normalization",
        "current_status": "not_derived",
        "affected_rows": "R4;R11",
        "fallback": "no local-GR promotion even if first-order equality lands",
        "valid_for_claim": "false",
    },
]


ROUTE_TEST_ROWS = [
    {
        "route_id": "R501_0_define_top_charge_from_Hilbert_source",
        "route": "make Q_M the parent-defined Hilbert compact-source charge",
        "test_result": "best_route_but_not_derived",
        "reason": "it avoids conserved-wrong-object failure, but needs a parent worldtube/source-measure selector before readout",
        "next_action": "derive glue or use radial bound runner",
        "valid_for_claim": "false",
    },
    {
        "route_id": "R501_1_late_equality_multiplier",
        "route": "impose Pi_M J_H = J_M_top with Lambda_eq",
        "test_result": "rejected_as_derivation",
        "reason": "unless independently owned, it inserts the desired closure by hand",
        "next_action": "only allowed as explicit closure label",
        "valid_for_claim": "false",
    },
    {
        "route_id": "R501_2_Hamiltonian_dictionary",
        "route": "identify both charges through the same Hamiltonian/Noether boundary charge",
        "test_result": "conditional_downstream",
        "reason": "requires EH exterior, integrable charge, no extra sector charge, and Poisson/Gauss calibration",
        "next_action": "retain for later local EH branch",
        "valid_for_claim": "false",
    },
    {
        "route_id": "R501_3_bound_runner",
        "route": "bound R_eq and residual channel integrals",
        "test_result": "fallback_now_needed_if_no_new_parent_glue",
        "reason": "keeps the source-normalization row empirical and falsifiable without claiming derivation",
        "next_action": NEXT_TARGET,
        "valid_for_claim": "false",
    },
]


BOUND_INPUT_TEMPLATE_ROWS = [
    {
        "template_id": "BR501_0_equality_residual",
        "quantity": "R_eq",
        "definition": "Pi_M J_H - J_M_top - dB_zero",
        "required_columns": "system_id;r1;r2;R_eq_integral;norm_convention;units;source_file;assumptions",
        "maps_to": "epsilon_radial_Meff equality residual contribution",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "BR501_1_boundary_term",
        "quantity": "B_zero_flux",
        "definition": "integral_boundary dB_zero or improvement flux",
        "required_columns": "system_id;boundary_type;B_zero_flux;units;source_file;assumptions",
        "maps_to": "boundary_monopole_shift and radial source hair",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "BR501_2_channelwise_extra",
        "quantity": "I_extra_channel",
        "definition": "Pi_M dJ_extra by boundary/domain/bulk/nonEH/kappa/frame/species channel",
        "required_columns": "system_id;channel;r1;r2;I_extra_channel;units;affected_rows;source_file;assumptions",
        "maps_to": "mu_extra vector and R4/R9/R10/R11 residuals",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "BR501_3_bound_decision",
        "quantity": "epsilon_radial_bound_decision",
        "definition": "epsilon_radial_Meff and dln_mu_dlnr compared against local-bound rows",
        "required_columns": "system_id;epsilon_radial_Meff;dln_mu_dlnr;bound_source;pass_fail;no_cancellation_flag;notes",
        "maps_to": "source-normalization local bound decision",
        "template_status": "not_run",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D501_0_equality",
        "status": "not_derived",
        "meaning": "the closed topological current is not yet proved equal to the observed Hilbert Pi_M mass current",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D501_1_best_route",
        "status": "Hilbert_defined_topological_charge",
        "meaning": "the only clean derivation route is to define Q_M from the same parent Hilbert compact-source charge before readout",
        "next_action": "derive parent worldtube/source-measure glue or demote to bound input",
    },
    {
        "decision_id": "D501_2_bound_runner",
        "status": "input_template_written",
        "meaning": "the equality residual and channelwise integrals now have an executable input schema",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D501_3_promotion",
        "status": "forbidden",
        "meaning": "no closed Hilbert flux, epsilon_radial zero, mu_extra zero, Newton, PPN, or local-GR pass is earned",
        "next_action": NEXT_TARGET,
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "TOPOLOGICAL_HILBERT_EQUALITY",
        "previous_status": "key_remaining_theorem",
        "new_status": "not_derived_parent_glue_missing",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "TOPOLOGICAL_PIM",
        "previous_status": "conditional_topological_current_clause_written_Hilbert_equality_missing",
        "new_status": "conserved_wrong_object_risk_explicit",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "RADIAL_BOUND_FALLBACK",
        "previous_status": "bound_runner_schema_written_not_filled",
        "new_status": "equality_residual_input_template_written",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_by_Hilbert_equality_extra_projection_calibration_and_PPN_source_stability",
        "new_status": "still_blocked_by_parent_glue_calibration_and_second_order_source_stability",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    full_path = ROOT / path
    if not full_path.exists():
        return []
    with full_path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in SOURCE_REGISTER:
        source_file = row["source_file"]
        rows.append({**row, "exists": str((ROOT / source_file).exists())})
    return rows


def validation_rows(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    topo_rows = read_csv(TOPOLOGICAL_PIM_CLAUSE_PATH)
    source_ward_rows = read_csv(SOURCE_WARD_CONTRACT_PATH)
    hilbert_rows = read_csv(HILBERT_MONOPOLE_CONTRACT_PATH)
    flux_rows = read_csv(MASS_FLUX_CONTRACT_PATH)
    bound_spec_rows = read_csv(RADIAL_BOUND_SPEC_PATH)

    missing_sources = [row for row in sources if row["exists"] != "True"]
    claim_equality_rows = [row for row in EQUALITY_ATTEMPT_ROWS if row["valid_for_claim"] == "true"]
    claim_obstruction_rows = [row for row in OBSTRUCTION_ROWS if row["valid_for_claim"] == "true"]
    claim_route_rows = [row for row in ROUTE_TEST_ROWS if row["valid_for_claim"] == "true"]
    claim_template_rows = [row for row in BOUND_INPUT_TEMPLATE_ROWS if row["valid_for_claim"] == "true"]
    required_obstructions = {
        "OB501_0_independent_topological_label",
        "OB501_1_worldtube_domain_selection",
        "OB501_2_boundary_improvement",
        "OB501_3_hidden_exchange",
        "OB501_4_universal_kappa_and_calibration",
        "OB501_5_second_order_stability",
    }
    obstruction_ids = {row["obstruction_id"] for row in OBSTRUCTION_ROWS}

    return [
        {
            "rule_id": "V501_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V501_1_prior_contracts_loaded",
            "rule": "500 topological clause, Ward, Hilbert, mass-flux, and bound spec rows are loaded",
            "result": "pass" if topo_rows and source_ward_rows and hilbert_rows and flux_rows and bound_spec_rows else "fail",
            "evidence": f"topo={len(topo_rows)};SC={len(source_ward_rows)};HM={len(hilbert_rows)};MF={len(flux_rows)};bound_spec={len(bound_spec_rows)}",
            "claim_effect": "501 tied to prior gates",
        },
        {
            "rule_id": "V501_2_equality_attempts",
            "rule": "equality attempt covers statement, worldtube route, Ward route, glue clause, Hamiltonian route, and bound fallback",
            "result": "pass" if len(EQUALITY_ATTEMPT_ROWS) == 6 else "fail",
            "evidence": f"equality_rows={len(EQUALITY_ATTEMPT_ROWS)}",
            "claim_effect": "theorem attempt concrete",
        },
        {
            "rule_id": "V501_3_obstruction_coverage",
            "rule": "obstructions cover independent label, domain selection, boundary, hidden exchange, calibration, and second-order stability",
            "result": "pass" if required_obstructions.issubset(obstruction_ids) else "fail",
            "evidence": ";".join(sorted(obstruction_ids)),
            "claim_effect": "no hidden equality debt",
        },
        {
            "rule_id": "V501_4_bound_input_template",
            "rule": "radial bound input template covers equality residual, boundary term, channelwise extra, and bound decision",
            "result": "pass" if len(BOUND_INPUT_TEMPLATE_ROWS) == 4 else "fail",
            "evidence": f"bound_input_rows={len(BOUND_INPUT_TEMPLATE_ROWS)}",
            "claim_effect": "test branch explicit but unfilled",
        },
        {
            "rule_id": "V501_5_no_false_claims",
            "rule": "no equality, obstruction, route, or template row is claim-valid",
            "result": "pass"
            if not claim_equality_rows and not claim_obstruction_rows and not claim_route_rows and not claim_template_rows
            else "fail",
            "evidence": f"equality_claims={len(claim_equality_rows)};obstruction_claims={len(claim_obstruction_rows)};route_claims={len(claim_route_rows)};template_claims={len(claim_template_rows)}",
            "claim_effect": "no Newton/local-GR promotion",
        },
    ]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    if fieldnames is None:
        fieldnames = list(rows[0].keys()) if rows else []
    out = ROOT / path
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_run_csv(results_dir: Path, filename: str, rows: list[dict[str, Any]]) -> None:
    fieldnames = list(rows[0].keys()) if rows else []
    with (results_dir / filename).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_table(rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> str:
    if not rows:
        return ""
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    lines = [
        "| " + " | ".join(fieldnames) + " |",
        "| " + " | ".join("---" for _ in fieldnames) + " |",
    ]
    for row in rows:
        values = [str(row.get(fieldname, "")).replace("\n", " ") for fieldname in fieldnames]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    timestamp: str,
    generated_at_utc: str,
    run_dir: Path,
    sources: list[dict[str, str]],
    validations: list[dict[str, str]],
) -> str:
    return f"""# 501 - Topological Hilbert Current Equality Or Radial Bound Runner

Private source-normalization/topological-projector checkpoint. This is not a public closed-flux proof, mu_extra-zero proof, Newtonian-limit proof, R11 pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `500` wrote a closed topological current:

```text
J_M_top = Q_M omega_M_top.
```

This checkpoint asks whether it is the same current as the observed Hilbert mass channel:

```text
Pi_M J_H = J_M_top.
```

Short answer:

```text
The equality theorem is not derived.

The best route is to define Q_M from the same parent Hilbert compact-source worldtube before readout.
That route is clean but still missing the parent worldtube/source-measure glue.

Without that glue, J_M_top is a conserved wrong object.
The radial bound runner input template is now written.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/topological_Hilbert_current_equality_or_radial_bound_runner.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Equality Attempt

The equality target is:

```text
Pi_M J_H = J_M_top + dB_zero + R_eq.
```

Closed Hilbert flux follows only if:

```text
R_eq = 0
and integral_boundary dB_zero = 0.
```

{markdown_table(EQUALITY_ATTEMPT_ROWS)}

## 5. Obstructions

{markdown_table(OBSTRUCTION_ROWS)}

## 6. Route Tests

{markdown_table(ROUTE_TEST_ROWS)}

## 7. Bound Runner Input Template

If equality is not derived, the exact fallback is:

{markdown_table(BOUND_INPUT_TEMPLATE_ROWS)}

## 8. Validation

{markdown_table(validations)}

## 9. Decision

{markdown_table(DECISION_ROWS)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
The topological-Hilbert equality theorem has been attempted.
The clean route is parent Hilbert-worldtube definition of Q_M before readout.
The equality residual input template is explicit.
```

Forbidden:

```text
MTS has derived Pi_M J_H = J_M_top.
MTS has derived d(Pi_M J_H)=0.
MTS has derived epsilon_radial_Meff=0.
MTS has derived mu_extra=0 or source-normalized Newtonian recovery.
MTS has passed R11, PPN, or local GR.
```

## 12. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | implement the radial bound runner unless a new parent glue clause can prove Q_M is the same Hilbert source charge |
| 2 | parent Hilbert-worldtube glue | derive Q_M from same-frame Hilbert matter source before readout and without domain leakage |
| 3 | calibration lock | even equality still needs measured-GM/Poisson/Gauss and constant universal G |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-topological-Hilbert-current-equality-or-radial-bound-runner"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (EQUALITY_ATTEMPT_PATH, EQUALITY_ATTEMPT_ROWS),
        (OBSTRUCTION_PATH, OBSTRUCTION_ROWS),
        (ROUTE_TEST_PATH, ROUTE_TEST_ROWS),
        (BOUND_INPUT_TEMPLATE_PATH, BOUND_INPUT_TEMPLATE_ROWS),
        (VALIDATION_PATH, validations),
        (DECISION_PATH, DECISION_ROWS),
        (ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS),
    ]

    for path, rows in csv_outputs:
        write_csv(path, rows)
        write_run_csv(results_dir, path.name, rows)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
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
        "equality_attempt": str(ROOT / EQUALITY_ATTEMPT_PATH),
        "obstruction_map": str(ROOT / OBSTRUCTION_PATH),
        "route_tests": str(ROOT / ROUTE_TEST_PATH),
        "bound_input_template": str(ROOT / BOUND_INPUT_TEMPLATE_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "equality_rows": len(EQUALITY_ATTEMPT_ROWS),
        "obstruction_rows": len(OBSTRUCTION_ROWS),
        "route_test_rows": len(ROUTE_TEST_ROWS),
        "bound_input_rows": len(BOUND_INPUT_TEMPLATE_ROWS),
        "failed_validation_rows": len(failed_validations),
        "topological_Hilbert_equality_attempted": True,
        "Hilbert_topological_current_equality_derived": False,
        "parent_worldtube_source_measure_glue_derived": False,
        "radial_bound_runner_input_template_written": True,
        "radial_bound_runner_executed": False,
        "Hilbert_PiM_flux_closed_parent_derived": False,
        "epsilon_radial_Meff_zero_derived": False,
        "mu_extra_zero_derived": False,
        "source_normalized_Newton_promoted": False,
        "R11_silence_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    (run_dir / "DONE.txt").write_text(
        f"{STATUS}\nnext={NEXT_TARGET}\nlocal_GR_claim_allowed=false\n",
        encoding="utf-8",
    )
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
