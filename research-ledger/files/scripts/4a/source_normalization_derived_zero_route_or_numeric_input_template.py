from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "source_normalization_route_router_written_theorem_first_and_numeric_templates_no_mu_extra_zero_or_Newton_promotion"
CLAIM_CEILING = "source_normalization_route_router_only_no_mu_extra_zero_Newton_PPN_R11_or_local_GR_promotion"
NEXT_TARGET = "498-source-normalization-radial-and-calibration-theorem-attempt.md"

DOC_PATH = Path("497-source-normalization-derived-zero-route-or-numeric-input-template.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_ROUTER_SOURCE_REGISTER.csv")
ROUTE_CLASSIFICATION_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_ROUTE_CLASSIFICATION.csv")
DERIVED_ZERO_TARGETS_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_DERIVED_ZERO_TARGETS.csv")
NUMERIC_INPUT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv")
ROW_DECISIONS_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_ROW_DECISIONS.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_ROUTER_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_ROUTER_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_ROUTER_ROUTE_UPDATE.csv")

MINIMUM_VECTOR_PATH = Path("source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv")
MISSING_LEDGER_PATH = Path("source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_MISSING_LEDGER.csv")
ACCEPTANCE_GATES_PATH = Path("source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_ACCEPTANCE_GATES.csv")


SOURCE_REGISTER = [
    {
        "source_file": "496-R11-source-normalization-operator-vector-minimum-fill.md",
        "role": "eight-channel source-normalization minimum fill",
    },
    {
        "source_file": "495-source-normalization-even-scalar-theorem-or-coefficient-fill.md",
        "role": "same-frame EH/Gauss-law/source theorem stack",
    },
    {
        "source_file": "467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md",
        "role": "mu_extra eight-channel owner ledger",
    },
    {
        "source_file": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "measured GM absorption guardrails",
    },
    {
        "source_file": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
        "role": "conditional radial M_eff conservation theorem",
    },
    {
        "source_file": "402-EH-source-normalization-parent-pair.md",
        "role": "EH/source-normalization theorem pair",
    },
    {
        "source_file": "404-selector-blind-matter-axiom-origin.md",
        "role": "selector-blind source/matter remains primitive route",
    },
    {
        "source_file": str(MINIMUM_VECTOR_PATH),
        "role": "496 minimum vector rows",
    },
    {
        "source_file": str(MISSING_LEDGER_PATH),
        "role": "496 missing/conditional ledger",
    },
    {
        "source_file": str(ACCEPTANCE_GATES_PATH),
        "role": "496 acceptance gates",
    },
    {
        "source_file": "scripts/source_normalization_derived_zero_route_or_numeric_input_template.py",
        "role": "this checkpoint generator",
    },
]


ROUTE_CLASSIFICATION_ROWS = [
    {
        "p8_channel": "radial_Meff_hair",
        "coefficient_symbol": "epsilon_radial_Meff",
        "primary_route": "theorem_first",
        "reason": "244 already gives a conditional closed Pi_M flux theorem; parent source identity is the missing piece",
        "fallback_route": "numeric_radial_profile",
        "blocks": "R4;R10;R11",
        "valid_for_claim": "false",
    },
    {
        "p8_channel": "boundary_monopole_shift",
        "coefficient_symbol": "epsilon_boundary",
        "primary_route": "theorem_first",
        "reason": "boundary no-hair/no-flux is the clean route; coefficient fill needed if boundary class remains active",
        "fallback_route": "numeric_boundary_coefficient",
        "blocks": "R4;R7;R8;R9;R11",
        "valid_for_claim": "false",
    },
    {
        "p8_channel": "domain_projector_mass",
        "coefficient_symbol": "epsilon_domain_projector",
        "primary_route": "theorem_first_high_pressure",
        "reason": "domain/projector row controls alpha1/alpha2/alpha3/xi/R11; theorem route is ideal but alpha3 product may need numeric fallback",
        "fallback_route": "numeric_domain_products",
        "blocks": "R5;R6;R7;R8;R11",
        "valid_for_claim": "false",
    },
    {
        "p8_channel": "bulk_X_Yukawa_tail",
        "coefficient_symbol": "epsilon_bulk_X",
        "primary_route": "numeric_template_first",
        "reason": "without a parent mass-gap theorem, the meaningful object is an alpha(lambda) curve",
        "fallback_route": "mass_gap_theorem",
        "blocks": "R10;R11",
        "valid_for_claim": "false",
    },
    {
        "p8_channel": "nonEH_operator_potential",
        "coefficient_symbol": "epsilon_nonEH_source",
        "primary_route": "theorem_or_operator_vector",
        "reason": "EH-only local exterior would zero it; otherwise it must be mapped through R11 coefficients",
        "fallback_route": "numeric_R11_operator_vector",
        "blocks": "R3;R4;R10;R11",
        "valid_for_claim": "false",
    },
    {
        "p8_channel": "species_source_charge",
        "coefficient_symbol": "epsilon_species_A",
        "primary_route": "theorem_first",
        "reason": "selector-blind source/matter theorem is the clean WEP/source route; numeric species residual is fallback",
        "fallback_route": "numeric_species_charge_vector",
        "blocks": "R1;R2;R11",
        "valid_for_claim": "false",
    },
    {
        "p8_channel": "time_drift",
        "coefficient_symbol": "epsilon_time_drift",
        "primary_route": "theorem_or_numeric",
        "reason": "stationarity theorem is clean, but Gdot bound can also score a sourced time-drift row",
        "fallback_route": "numeric_Gdot_source_row",
        "blocks": "R9;R11",
        "valid_for_claim": "false",
    },
    {
        "p8_channel": "absolute_calibration_offset",
        "coefficient_symbol": "epsilon_calibration",
        "primary_route": "parent_fixed_calibration_or_retained_closure",
        "reason": "constant calibration is harmless only if universal, parent-fixed, range/time/species independent",
        "fallback_route": "retained_no_claim",
        "blocks": "R4;R9;R11",
        "valid_for_claim": "false",
    },
]


DERIVED_ZERO_TARGET_ROWS = [
    {
        "target_id": "DZ0_radial_Meff",
        "p8_channel": "radial_Meff_hair",
        "theorem_target": "parent compact-exterior source identity gives d(Pi_M J)=0 and no radial memory hair",
        "required_proof_objects": "Pi_M flux owner; exterior annulus; no relative-memory leakage into absolute harmonic flux",
        "current_status": "conditional_from_244_not_parent_closed",
        "valid_for_claim": "false",
    },
    {
        "target_id": "DZ1_boundary_monopole",
        "p8_channel": "boundary_monopole_shift",
        "theorem_target": "boundary/class source is topological harmless constant or no-flux/no-monopole in compact local branch",
        "required_proof_objects": "boundary Ward no-flux; no alpha3 vector flux; zero derivative hair",
        "current_status": "not_derived",
        "valid_for_claim": "false",
    },
    {
        "target_id": "DZ2_domain_projector",
        "p8_channel": "domain_projector_mass",
        "theorem_target": "domain/projector has no vector, no flux, no anisotropy, no source-normalization monopole",
        "required_proof_objects": "topological P_D ownership; local trivial class; no-vector selector; R11 silence",
        "current_status": "not_derived_high_pressure",
        "valid_for_claim": "false",
    },
    {
        "target_id": "DZ3_bulk_mass_gap",
        "p8_channel": "bulk_X_Yukawa_tail",
        "theorem_target": "source-free positive mass gap removes finite-range bulk tail in compact exterior",
        "required_proof_objects": "bulk Euler equation; positive operator; zero source/boundary flux",
        "current_status": "not_derived_numeric_curve_preferred",
        "valid_for_claim": "false",
    },
    {
        "target_id": "DZ4_EH_only",
        "p8_channel": "nonEH_operator_potential",
        "theorem_target": "same-frame local compact exterior is metric-only, second-order, and EH plus Lambda",
        "required_proof_objects": "Lovelock/EH selection premises plus non-EH operator silence",
        "current_status": "conditional_not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "target_id": "DZ5_selector_blind_source",
        "p8_channel": "species_source_charge",
        "theorem_target": "selector-blind source action gives no species/source charge pullback",
        "required_proof_objects": "observed coframe/source neutrality; no species-dependent constants",
        "current_status": "not_parent_derived",
        "valid_for_claim": "false",
    },
    {
        "target_id": "DZ6_stationarity",
        "p8_channel": "time_drift",
        "theorem_target": "local compact source normalization is stationary and no hidden time flux survives",
        "required_proof_objects": "time-translation/local stationarity; Ward-owned flux silence; constant kappa",
        "current_status": "not_derived",
        "valid_for_claim": "false",
    },
    {
        "target_id": "DZ7_parent_fixed_calibration",
        "p8_channel": "absolute_calibration_offset",
        "theorem_target": "absolute calibration is parent-fixed universal constant with zero range/time/species derivatives",
        "required_proof_objects": "calibration owner; same-frame units; no derivative hair",
        "current_status": "conditional_harmless_not_parent_fixed",
        "valid_for_claim": "false",
    },
]


NUMERIC_TEMPLATE_ROWS = [
    {
        "template_id": "NI0_radial_profile",
        "p8_channel": "radial_Meff_hair",
        "coefficient_symbol": "epsilon_radial_Meff",
        "required_columns": "r;epsilon_radial_Meff(r);dln_mu_dr;units;source_file;assumptions",
        "bound_or_gate": "mapped R4/R10 bounds or theorem-zero radial hair",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "NI1_boundary",
        "p8_channel": "boundary_monopole_shift",
        "coefficient_symbol": "epsilon_boundary",
        "required_columns": "epsilon_boundary;boundary_flux_vector;alpha3_map;xi_map;Gdot_map;units;source_file",
        "bound_or_gate": "R4/R7/R8/R9 locks; alpha3 <= 4e-20 where applicable",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "NI2_domain_products",
        "p8_channel": "domain_projector_mass",
        "coefficient_symbol": "epsilon_domain_projector",
        "required_columns": "W_domain_alpha1;epsilon_domain_vector;W_domain_alpha2;W_domain_alpha3;epsilon_domain_flux;W_domain_xi;epsilon_domain_anisotropy;source_file",
        "bound_or_gate": "alpha1<=1e-4; alpha2<=2e-9; alpha3<=4e-20; xi<=4e-9",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "NI3_bulk_curve",
        "p8_channel": "bulk_X_Yukawa_tail",
        "coefficient_symbol": "epsilon_bulk_X",
        "required_columns": "lambda_X;alpha_X;epsilon_bulk_X;range_units;alpha_lambda_bound;source_file;assumptions",
        "bound_or_gate": "R10 alpha(lambda) curve below bounds",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "NI4_nonEH_vector",
        "p8_channel": "nonEH_operator_potential",
        "coefficient_symbol": "epsilon_nonEH_source",
        "required_columns": "operator_family;coefficient_value;units;normalization;weak_field_map;affected_rows;source_file",
        "bound_or_gate": "R3/R4/R10/R11 row-specific bounds",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "NI5_species",
        "p8_channel": "species_source_charge",
        "coefficient_symbol": "epsilon_species_A",
        "required_columns": "species_pair;epsilon_species_A;eta_source_AB;clock_residual;source_file;assumptions",
        "bound_or_gate": "eta_source_AB <= 2.8e-15 or theorem-zero",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "NI6_time",
        "p8_channel": "time_drift",
        "coefficient_symbol": "epsilon_time_drift",
        "required_columns": "time_window;epsilon_time_drift;dln_mu_dt;Gdot_over_G;units;source_file",
        "bound_or_gate": "Gdot/G <= 9.6e-15 yr^-1 or theorem-zero",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "NI7_calibration",
        "p8_channel": "absolute_calibration_offset",
        "coefficient_symbol": "epsilon_calibration",
        "required_columns": "lambda0;universality_certificate;range_derivative;time_derivative;species_derivative;source_file",
        "bound_or_gate": "all derivatives zero and parent-fixed universal calibration",
        "template_status": "retained_until_parent_fixed",
        "valid_for_claim": "false",
    },
]


ROW_DECISION_ROWS = [
    {
        "decision_id": "RD0",
        "p8_channel": "radial_Meff_hair",
        "decision": "attempt_theorem_first",
        "next_action": "498-source-normalization-radial-and-calibration-theorem-attempt.md",
    },
    {
        "decision_id": "RD1",
        "p8_channel": "boundary_monopole_shift",
        "decision": "defer_to_boundary_nohair_or_numeric_template",
        "next_action": "boundary odd-charge/nohair theorem or NI1 fill",
    },
    {
        "decision_id": "RD2",
        "p8_channel": "domain_projector_mass",
        "decision": "defer_to_domain_no_vector_or_numeric_products",
        "next_action": "domain odd-charge/no-vector theorem or NI2 fill",
    },
    {
        "decision_id": "RD3",
        "p8_channel": "bulk_X_Yukawa_tail",
        "decision": "numeric_curve_first",
        "next_action": "R10 alpha(lambda) curve template",
    },
    {
        "decision_id": "RD4",
        "p8_channel": "nonEH_operator_potential",
        "decision": "EH_only_theorem_or_R11_numeric_vector",
        "next_action": "R11 family coefficient map",
    },
    {
        "decision_id": "RD5",
        "p8_channel": "species_source_charge",
        "decision": "selector_blind_source_theorem_first",
        "next_action": "source-side WEP theorem or NI5 fill",
    },
    {
        "decision_id": "RD6",
        "p8_channel": "time_drift",
        "decision": "stationarity_or_Gdot_input",
        "next_action": "stationarity theorem or NI6 fill",
    },
    {
        "decision_id": "RD7",
        "p8_channel": "absolute_calibration_offset",
        "decision": "pair_with_radial_theorem",
        "next_action": "498-source-normalization-radial-and-calibration-theorem-attempt.md",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_router",
        "status": "written",
        "meaning": "all eight source-normalization channels are routed to theorem-first, numeric-first, mixed, or retained closure tracks",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D1_first_target",
        "status": "radial_and_calibration",
        "meaning": "the most derivable immediate route is closed M_eff flux plus parent-fixed calibration",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D2_numeric_templates",
        "status": "written_unfilled",
        "meaning": "numeric input schemas exist but no data/theorem values are supplied",
        "next_action": "fill only with sourced values or theorem certificates",
    },
    {
        "decision_id": "D3_promotion",
        "status": "forbidden",
        "meaning": "no mu_extra zero, source-normalized Newton, R11 silence, PPN, or local-GR pass is earned",
        "next_action": "continue derivation-first route",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "SOURCE_NORMALIZATION_ROUTER",
        "previous_status": "R11_source_normalization_minimum_eight_channel_fill_written_no_claim_rows",
        "new_status": "eight_channels_routed_to_theorem_or_numeric_templates",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "blocked_by_unfilled_mu_extra_channels",
        "new_status": "first_derivation_target_radial_Meff_plus_absolute_calibration",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_by_unfilled_mu_extra_channels_and_Textra",
        "new_status": "blocked_but_mu_extra_route_partitioned",
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
        exists = (ROOT / row["source_file"]).exists()
        rows.append({**row, "exists": str(exists)})
    return rows


def validation_rows(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    missing_sources = [row for row in sources if row["exists"] != "True"]
    minimum_rows = read_csv(MINIMUM_VECTOR_PATH)
    missing_rows = read_csv(MISSING_LEDGER_PATH)
    gate_rows = read_csv(ACCEPTANCE_GATES_PATH)
    claim_route_rows = [row for row in ROUTE_CLASSIFICATION_ROWS if row["valid_for_claim"] == "true"]
    claim_zero_rows = [row for row in DERIVED_ZERO_TARGET_ROWS if row["valid_for_claim"] == "true"]
    claim_numeric_rows = [row for row in NUMERIC_TEMPLATE_ROWS if row["valid_for_claim"] == "true"]
    required_channels = {
        "radial_Meff_hair",
        "boundary_monopole_shift",
        "domain_projector_mass",
        "bulk_X_Yukawa_tail",
        "nonEH_operator_potential",
        "species_source_charge",
        "time_drift",
        "absolute_calibration_offset",
    }
    route_channels = {row["p8_channel"] for row in ROUTE_CLASSIFICATION_ROWS}
    zero_channels = {row["p8_channel"] for row in DERIVED_ZERO_TARGET_ROWS}
    numeric_channels = {row["p8_channel"] for row in NUMERIC_TEMPLATE_ROWS}

    return [
        {
            "rule_id": "V497_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V497_1_inputs_loaded",
            "rule": "496 minimum rows, missing ledger, and acceptance gates are loaded",
            "result": "pass" if len(minimum_rows) == 8 and len(missing_rows) == 16 and len(gate_rows) == 6 else "fail",
            "evidence": f"minimum_rows={len(minimum_rows)};missing_rows={len(missing_rows)};gate_rows={len(gate_rows)}",
            "claim_effect": "router tied to 496",
        },
        {
            "rule_id": "V497_2_route_coverage",
            "rule": "all eight channels have route classifications",
            "result": "pass" if required_channels.issubset(route_channels) else "fail",
            "evidence": ";".join(sorted(route_channels)),
            "claim_effect": "no hidden channel",
        },
        {
            "rule_id": "V497_3_zero_target_coverage",
            "rule": "all eight channels have derived-zero theorem targets",
            "result": "pass" if required_channels.issubset(zero_channels) else "fail",
            "evidence": ";".join(sorted(zero_channels)),
            "claim_effect": "derivation targets explicit",
        },
        {
            "rule_id": "V497_4_numeric_template_coverage",
            "rule": "all eight channels have numeric/input templates",
            "result": "pass" if required_channels.issubset(numeric_channels) else "fail",
            "evidence": ";".join(sorted(numeric_channels)),
            "claim_effect": "test branch explicit",
        },
        {
            "rule_id": "V497_5_no_claim_rows",
            "rule": "no route, theorem, or numeric row is claim-valid",
            "result": "pass" if not claim_route_rows and not claim_zero_rows and not claim_numeric_rows else "fail",
            "evidence": f"claim_route_rows={len(claim_route_rows)};claim_zero_rows={len(claim_zero_rows)};claim_numeric_rows={len(claim_numeric_rows)}",
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
    return f"""# 497 - Source Normalization Derived-Zero Route Or Numeric Input Template

Private source-normalization routing checkpoint. This is not a public mu_extra-zero proof, Newtonian-limit proof, R11 pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `496` gave every `mu_extra` source-normalization channel a minimum R11 row. This checkpoint decides what kind of work each row needs next:

```text
derived-zero theorem,
numeric/source-backed input,
mixed theorem+numeric route,
or retained closure.
```

Short answer:

```text
The router is written.
The first derivation target should be radial M_eff conservation plus parent-fixed calibration.
Bulk finite-range and several retained rows need numeric templates unless stronger no-hair theorems are found.
No row is promoted.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/source_normalization_derived_zero_route_or_numeric_input_template.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Route Classification

{markdown_table(ROUTE_CLASSIFICATION_ROWS)}

## 5. Derived-Zero Targets

{markdown_table(DERIVED_ZERO_TARGET_ROWS)}

## 6. Numeric Input Templates

{markdown_table(NUMERIC_TEMPLATE_ROWS)}

## 7. Row Decisions

{markdown_table(ROW_DECISION_ROWS)}

## 8. Validation

{markdown_table(validations)}

## 9. Decision

{markdown_table(DECISION_ROWS)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
All eight source-normalization rows are routed to theorem or numeric work.
The immediate derivation target is closed radial M_eff flux plus parent-fixed calibration.
```

Forbidden:

```text
MTS has derived mu_extra=0.
MTS has filled numeric source-normalization inputs.
MTS has derived source-normalized Newtonian recovery.
MTS has passed R11, PPN, or local GR.
```

## 12. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | radial M_eff conservation has the strongest existing conditional theorem and calibration must be locked to avoid a hidden GM cheat |
| 2 | `R10_alpha_lambda_curve_MTS_source_normalization.csv` | bulk Yukawa row is numeric-template-first unless a mass-gap theorem lands |
| 3 | boundary/domain odd-charge theorem | needed for alpha3 and domain source-normalization routes |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-source-normalization-derived-zero-route-or-numeric-input-template"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(ROUTE_CLASSIFICATION_PATH, ROUTE_CLASSIFICATION_ROWS)
    write_csv(DERIVED_ZERO_TARGETS_PATH, DERIVED_ZERO_TARGET_ROWS)
    write_csv(NUMERIC_INPUT_TEMPLATE_PATH, NUMERIC_TEMPLATE_ROWS)
    write_csv(ROW_DECISIONS_PATH, ROW_DECISION_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_route_rows = [row for row in ROUTE_CLASSIFICATION_ROWS if row["valid_for_claim"] == "true"]
    claim_zero_rows = [row for row in DERIVED_ZERO_TARGET_ROWS if row["valid_for_claim"] == "true"]
    claim_numeric_rows = [row for row in NUMERIC_TEMPLATE_ROWS if row["valid_for_claim"] == "true"]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "route_classification": str(ROOT / ROUTE_CLASSIFICATION_PATH),
        "derived_zero_targets": str(ROOT / DERIVED_ZERO_TARGETS_PATH),
        "numeric_input_template": str(ROOT / NUMERIC_INPUT_TEMPLATE_PATH),
        "row_decisions": str(ROOT / ROW_DECISIONS_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "route_classification_rows": len(ROUTE_CLASSIFICATION_ROWS),
        "derived_zero_target_rows": len(DERIVED_ZERO_TARGET_ROWS),
        "numeric_input_template_rows": len(NUMERIC_TEMPLATE_ROWS),
        "row_decision_rows": len(ROW_DECISION_ROWS),
        "failed_validation_rows": len(failed_validations),
        "claim_route_rows": len(claim_route_rows),
        "claim_zero_rows": len(claim_zero_rows),
        "claim_numeric_rows": len(claim_numeric_rows),
        "all_mu_extra_channels_routed": True,
        "numeric_templates_written": True,
        "radial_Meff_first_derivation_target": True,
        "mu_extra_zero_derived": False,
        "source_normalized_Newton_promoted": False,
        "R11_silence_derived": False,
        "PPN_promoted": False,
        "local_GR_claim_allowed": False,
        "next_target": NEXT_TARGET,
    }
    (run_dir / "status.json").write_text(json.dumps(status, indent=2), encoding="utf-8")
    print(json.dumps(status, indent=2))


if __name__ == "__main__":
    main()
