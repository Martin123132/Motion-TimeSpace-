from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "R11_source_normalization_operator_minimum_fill_written_eight_channel_rows_no_claim_valid_coefficients_no_Newton_or_local_GR_promotion"
CLAIM_CEILING = "R11_source_normalization_minimum_fill_only_no_mu_extra_zero_Newton_PPN_R11_or_local_GR_promotion"
NEXT_TARGET = "497-source-normalization-derived-zero-route-or-numeric-input-template.md"

DOC_PATH = Path("496-R11-source-normalization-operator-vector-minimum-fill.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_MINIMUM_SOURCE_REGISTER.csv")
MINIMUM_VECTOR_PATH = Path("source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv")
ACCEPTANCE_GATES_PATH = Path("source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_ACCEPTANCE_GATES.csv")
MISSING_LEDGER_PATH = Path("source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_MISSING_LEDGER.csv")
THEOREM_OR_NUMERIC_PATH = Path("source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_THEOREM_OR_NUMERIC_ROUTE.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_ROUTE_UPDATE.csv")

R11_VECTOR_PATH = Path("source-intake/mts_residuals/R11_nonEH_operator_vector_executable.csv")
R11_MU_LINK_PATH = Path("source-intake/mts_residuals/R11_MU_EXTRA_SOURCE_NORMALIZATION_LINK.csv")
MU_EXTRA_COEFFICIENT_VECTOR_PATH = Path("source-intake/mts_residuals/P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv")
LOCAL_VECTOR_PATH = Path("source-intake/mts_residuals/P8_LOCAL_GR_RESIDUAL_VECTOR_FROM_DOMAIN_SOURCE.csv")
SOURCE_NORM_FILL_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_COEFFICIENT_FILL.csv")


SOURCE_REGISTER = [
    {
        "source_file": "495-source-normalization-even-scalar-theorem-or-coefficient-fill.md",
        "role": "latest theorem stack and R11 source-normalization next target",
    },
    {
        "source_file": "479-R11-domain-source-normalization-zero-or-fill.md",
        "role": "domain source-normalization zero-route rejected and fill requirements",
    },
    {
        "source_file": "473-R11-domain-projector-operator-vector-minimum-fill.md",
        "role": "current R11 vector path and domain minimum rows",
    },
    {
        "source_file": "467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md",
        "role": "eight-channel mu_extra sum rule and coefficient vector",
    },
    {
        "source_file": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH/source-normalization theorem pair",
    },
    {
        "source_file": str(R11_VECTOR_PATH),
        "role": "current canonical R11 vector",
    },
    {
        "source_file": str(R11_MU_LINK_PATH),
        "role": "R11 to mu_extra/source-normalization link rows",
    },
    {
        "source_file": str(MU_EXTRA_COEFFICIENT_VECTOR_PATH),
        "role": "existing eight-channel mu_extra coefficient vector",
    },
    {
        "source_file": str(LOCAL_VECTOR_PATH),
        "role": "local residual vector containing LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
    },
    {
        "source_file": str(SOURCE_NORM_FILL_PATH),
        "role": "495 source-normalization coefficient fill rows",
    },
    {
        "source_file": "scripts/R11_source_normalization_operator_vector_minimum_fill.py",
        "role": "this checkpoint generator",
    },
]


MINIMUM_VECTOR_ROWS = [
    {
        "row_id": "R11SN_0_radial_Meff_hair",
        "r11_family": "source_normalization_operator",
        "p8_channel": "radial_Meff_hair",
        "coefficient_symbol": "epsilon_radial_Meff",
        "coefficient_value_or_theorem": "MISSING_RADIAL_NOHAIR_THEOREM_OR_NUMERIC_PROFILE",
        "coefficient_units": "dimensionless_or_profile_units_declared",
        "normalization": "epsilon_radial_Meff = mu_radial_Meff_hair/(G_EH*M_EH)",
        "operator_form": "dM_eff/dr != 0 or radial memory/source hair",
        "weak_field_map": "partial_r ln(mu_obs) and beta/fifth-force source response",
        "affected_rows": "R4;R10;R11",
        "induced_observable": "beta_minus_1;alpha(lambda);operator_ledger",
        "acceptance": "zero radial hair theorem or numeric radial profile below mapped bounds",
        "required_source_artifact": "P8_radial_mu_profile_or_zero.csv",
        "current_status": "minimum_row_missing_input",
        "valid_for_claim": "false",
    },
    {
        "row_id": "R11SN_1_boundary_monopole_shift",
        "r11_family": "source_normalization_operator",
        "p8_channel": "boundary_monopole_shift",
        "coefficient_symbol": "epsilon_boundary",
        "coefficient_value_or_theorem": "MISSING_BOUNDARY_NOHAIR_THEOREM_OR_NUMERIC_COEFFICIENT",
        "coefficient_units": "dimensionless",
        "normalization": "epsilon_boundary = mu_boundary/(G_EH*M_EH)",
        "operator_form": "boundary/class/topological monopole source contribution",
        "weak_field_map": "beta, alpha3, xi, and Gdot source-normalization shifts",
        "affected_rows": "R4;R7;R8;R9;R11",
        "induced_observable": "beta_minus_1;alpha3;xi;Gdot_over_G;operator_ledger",
        "acceptance": "boundary nohair/no-flux theorem or coefficient bounds for mapped rows",
        "required_source_artifact": "P8_mu_extra_boundary_coefficients.csv",
        "current_status": "minimum_row_missing_input",
        "valid_for_claim": "false",
    },
    {
        "row_id": "R11SN_2_domain_projector_mass",
        "r11_family": "source_normalization_operator",
        "p8_channel": "domain_projector_mass",
        "coefficient_symbol": "epsilon_domain_projector",
        "coefficient_value_or_theorem": "MISSING_DOMAIN_PROJECTOR_ZERO_THEOREM_OR_NUMERIC_PRODUCTS",
        "coefficient_units": "dimensionless",
        "normalization": "epsilon_domain_projector = mu_domain_projector/(G_EH*M_EH)",
        "operator_form": "domain/projector source-normalization contribution",
        "weak_field_map": "alpha1/alpha2/alpha3/xi plus R11 source-normalization ledger",
        "affected_rows": "R5;R6;R7;R8;R11",
        "induced_observable": "alpha1;alpha2;alpha3;xi;operator_ledger",
        "acceptance": "domain no-vector/no-flux/no-anisotropy theorem or numeric products below gates",
        "required_source_artifact": "P8_mu_extra_domain_projector_coefficients.csv",
        "current_status": "minimum_row_missing_input",
        "valid_for_claim": "false",
    },
    {
        "row_id": "R11SN_3_bulk_X_Yukawa_tail",
        "r11_family": "source_normalization_operator",
        "p8_channel": "bulk_X_Yukawa_tail",
        "coefficient_symbol": "epsilon_bulk_X",
        "coefficient_value_or_theorem": "MISSING_BULK_MASS_GAP_THEOREM_OR_ALPHA_LAMBDA_CURVE",
        "coefficient_units": "dimensionless_plus_length_scale",
        "normalization": "epsilon_bulk_X = mu_bulk_X/(G_EH*M_EH)",
        "operator_form": "delta a/a_GR = alpha_X(1+r/lambda_X) exp(-r/lambda_X)",
        "weak_field_map": "finite-range fifth-force curve",
        "affected_rows": "R10;R11",
        "induced_observable": "alpha(lambda);operator_ledger",
        "acceptance": "positive source-free mass-gap nohair theorem or alpha(lambda) curve below bounds",
        "required_source_artifact": "R10_alpha_lambda_curve_MTS_source_normalization.csv",
        "current_status": "minimum_row_missing_input",
        "valid_for_claim": "false",
    },
    {
        "row_id": "R11SN_4_nonEH_operator_potential",
        "r11_family": "source_normalization_operator",
        "p8_channel": "nonEH_operator_potential",
        "coefficient_symbol": "epsilon_nonEH_source",
        "coefficient_value_or_theorem": "MISSING_EH_ONLY_THEOREM_OR_NONEH_OPERATOR_COEFFICIENT_MAP",
        "coefficient_units": "dimensionless_or_operator_units_declared",
        "normalization": "epsilon_nonEH_source = mu_nonEH_operator/(G_EH*M_EH)",
        "operator_form": "Phi = Phi_EH + sum_i c_i Phi_i",
        "weak_field_map": "gamma/beta/fifth-force/R11 operator residuals",
        "affected_rows": "R3;R4;R10;R11",
        "induced_observable": "gamma_minus_1;beta_minus_1;alpha(lambda);operator_ledger",
        "acceptance": "EH-only exterior theorem or coefficient vector with source paths and bounds",
        "required_source_artifact": "R11_nonEH_operator_vector_executable.csv",
        "current_status": "minimum_row_missing_input",
        "valid_for_claim": "false",
    },
    {
        "row_id": "R11SN_5_species_source_charge",
        "r11_family": "source_normalization_operator",
        "p8_channel": "species_source_charge",
        "coefficient_symbol": "epsilon_species_A",
        "coefficient_value_or_theorem": "MISSING_SELECTOR_BLIND_SOURCE_THEOREM_OR_SPECIES_CHARGE_VECTOR",
        "coefficient_units": "dimensionless_by_species_pair",
        "normalization": "epsilon_species_A = Delta_A mu_obs/(G_EH*M_EH)",
        "operator_form": "composition/species-dependent source normalization",
        "weak_field_map": "source-side WEP and clock/source residual",
        "affected_rows": "R1;R2;R11",
        "induced_observable": "eta_source_AB;clock_redshift;operator_ledger",
        "acceptance": "selector-blind source theorem or eta_source_AB <= 2.8e-15 sourced vector",
        "required_source_artifact": "P8_species_source_charge_residual_or_zero.csv",
        "current_status": "minimum_row_missing_input",
        "valid_for_claim": "false",
    },
    {
        "row_id": "R11SN_6_time_drift",
        "r11_family": "source_normalization_operator",
        "p8_channel": "time_drift",
        "coefficient_symbol": "epsilon_time_drift",
        "coefficient_value_or_theorem": "MISSING_STATIONARITY_THEOREM_OR_TIME_DRIFT_COEFFICIENT",
        "coefficient_units": "dimensionless_or_per_time_with_map",
        "normalization": "epsilon_time_drift = mu_time_drift/(G_EH*M_EH)",
        "operator_form": "partial_t mu_obs != 0",
        "weak_field_map": "Gdot/G and source-normalization time drift",
        "affected_rows": "R9;R11",
        "induced_observable": "Gdot_over_G;operator_ledger",
        "acceptance": "stationarity theorem or Gdot/G <= 9.6e-15 yr^-1 sourced row",
        "required_source_artifact": "P8_time_drift_residual_or_zero.csv",
        "current_status": "minimum_row_missing_input",
        "valid_for_claim": "false",
    },
    {
        "row_id": "R11SN_7_absolute_calibration_offset",
        "r11_family": "source_normalization_operator",
        "p8_channel": "absolute_calibration_offset",
        "coefficient_symbol": "epsilon_calibration",
        "coefficient_value_or_theorem": "MISSING_PARENT_FIXED_UNIVERSAL_CALIBRATION_THEOREM_OR_RETAINED_OFFSET",
        "coefficient_units": "dimensionless",
        "normalization": "epsilon_calibration = mu_absolute_calibration_offset/(G_EH*M_EH)",
        "operator_form": "mu_obs = lambda0 G_ref M_bare",
        "weak_field_map": "harmless only if universal constant with zero derivatives",
        "affected_rows": "R4;R9;R11",
        "induced_observable": "beta_minus_1;Gdot_over_G;operator_ledger",
        "acceptance": "parent-fixed universal calibration with no range/time/species dependence",
        "required_source_artifact": "P8_absolute_calibration_owner.csv",
        "current_status": "conditional_calibration_not_claimable",
        "valid_for_claim": "false",
    },
]


ACCEPTANCE_GATE_ROWS = [
    {
        "gate_id": "G0_schema",
        "rule": "minimum source-normalization vector has one row for each mu_extra channel",
        "pass_condition": "8 rows, all with coefficient symbol, normalization, map, affected rows, and required artifact",
        "claim_effect": "wiring only",
    },
    {
        "gate_id": "G1_no_missing_for_claim",
        "rule": "a row cannot be claim-valid while coefficient_value_or_theorem starts with MISSING or status is conditional/retained",
        "pass_condition": "valid_for_claim=true only after concrete theorem-zero or numeric coefficient with source path",
        "claim_effect": "prevents fake Newton pass",
    },
    {
        "gate_id": "G2_domain_sibling_rows",
        "rule": "domain_projector_mass row must propagate to R5/R6/R7/R8/R11",
        "pass_condition": "all sibling rows named and no tuned cancellation credit",
        "claim_effect": "alpha3 cannot be scored alone",
    },
    {
        "gate_id": "G3_even_scalar_guard",
        "rule": "even measured-GM offsets are not killed by exchange oddness",
        "pass_condition": "absolute/even source offsets require independent theorem or coefficient",
        "claim_effect": "prevents oddness overclaim",
    },
    {
        "gate_id": "G4_no_absorption_cheat",
        "rule": "range/time/species/radial dependence cannot be absorbed into measured GM",
        "pass_condition": "derivative hair is zero or explicitly mapped to residual rows",
        "claim_effect": "protects Newton gate",
    },
    {
        "gate_id": "G5_no_promotion",
        "rule": "no R11/source-normalization row promotes local GR without all source and stress rows closed",
        "pass_condition": "local_GR_claim_allowed=false until all rows pass",
        "claim_effect": "claim ceiling",
    },
]


THEOREM_OR_NUMERIC_ROWS = [
    {
        "route_id": "T0_parent_zero",
        "route": "derive mu_extra_i=0 for every channel from same-frame EH, local no-hair, source neutrality, and topological/stress silence",
        "needed_inputs": "parent theorem certificates for all eight channels",
        "current_status": "not_derived",
        "valid_for_claim": "false",
    },
    {
        "route_id": "T1_numeric_vector",
        "route": "fill every channel with numeric/source-backed coefficient, units, normalization, weak-field map, and bound comparison",
        "needed_inputs": "required_source_artifact for each row",
        "current_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "route_id": "T2_mixed_theorem_numeric",
        "route": "allow some theorem-zero rows and some numeric rows, with no hidden cancellation between channels",
        "needed_inputs": "row-by-row claim status and total no-cancellation guard",
        "current_status": "allowed_future_branch",
        "valid_for_claim": "false",
    },
    {
        "route_id": "T3_closure_retention",
        "route": "retain missing rows as closure coefficients and do not claim Newton/local GR",
        "needed_inputs": "explicit retained status in local residual vector",
        "current_status": "active_current_branch",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D0_minimum_fill",
        "status": "written",
        "meaning": "the source-normalization R11 operator now has an eight-channel minimum fill contract",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D1_claimable_rows",
        "status": "zero",
        "meaning": "no minimum row is claim-valid because every channel still needs theorem-zero or numeric input",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D2_Newton_gate",
        "status": "blocked",
        "meaning": "source-normalized Newton remains blocked by mu_extra coefficient/theorem rows",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D3_promotion",
        "status": "forbidden",
        "meaning": "no mu_extra zero, Newton, R11 silence, PPN, or local-GR pass is earned",
        "next_action": "continue derivation-first or numeric-fill route",
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "same_frame_Gauss_law_theorem_stack_written_R11_coefficients_retained",
        "new_status": "R11_source_normalization_minimum_eight_channel_fill_written_no_claim_rows",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "R11_SOURCE_NORMALIZATION",
        "previous_status": "retained_missing_coefficients",
        "new_status": "minimum_fill_rows_written_for_all_mu_extra_channels",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_by_R11_source_normalization_coefficients_and_extra_stress",
        "new_status": "blocked_by_unfilled_mu_extra_channels_and_Textra",
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
    r11_rows = read_csv(R11_VECTOR_PATH)
    r11_mu_link_rows = read_csv(R11_MU_LINK_PATH)
    mu_extra_rows = read_csv(MU_EXTRA_COEFFICIENT_VECTOR_PATH)
    local_rows = read_csv(LOCAL_VECTOR_PATH)
    fill_rows = read_csv(SOURCE_NORM_FILL_PATH)
    claim_rows = [row for row in MINIMUM_VECTOR_ROWS if row["valid_for_claim"] == "true"]
    missing_marker_rows = [
        row for row in MINIMUM_VECTOR_ROWS
        if str(row["coefficient_value_or_theorem"]).startswith("MISSING")
        or row["current_status"] in {"minimum_row_missing_input", "conditional_calibration_not_claimable"}
    ]
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
    channels = {row["p8_channel"] for row in MINIMUM_VECTOR_ROWS}
    source_norm_r11_rows = [
        row for row in r11_rows
        if row.get("operator_family", "") == "source_normalization_operator"
    ]
    local_source_norm_rows = [
        row for row in local_rows
        if row.get("component_id", "") == "LRV_DOMAIN_R11_SOURCE_NORMALIZATION"
    ]

    return [
        {
            "rule_id": "V496_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V496_1_inputs_loaded",
            "rule": "R11 vector, R11 mu link, mu_extra vector, local vector, and 495 fill rows are loaded",
            "result": "pass" if len(r11_rows) >= 10 and len(r11_mu_link_rows) >= 8 and len(mu_extra_rows) >= 8 and len(local_rows) >= 7 and len(fill_rows) >= 5 else "fail",
            "evidence": f"r11_rows={len(r11_rows)};r11_mu_link_rows={len(r11_mu_link_rows)};mu_extra_rows={len(mu_extra_rows)};local_rows={len(local_rows)};fill_rows={len(fill_rows)}",
            "claim_effect": "minimum fill is tied to active artifacts",
        },
        {
            "rule_id": "V496_2_source_norm_R11_present",
            "rule": "canonical R11 vector contains source_normalization_operator",
            "result": "pass" if source_norm_r11_rows else "fail",
            "evidence": f"source_norm_R11_rows={len(source_norm_r11_rows)}",
            "claim_effect": "R11 family is wired",
        },
        {
            "rule_id": "V496_3_channel_coverage",
            "rule": "minimum vector covers all eight mu_extra channels",
            "result": "pass" if required_channels.issubset(channels) else "fail",
            "evidence": ";".join(sorted(channels)),
            "claim_effect": "no hidden source-normalization channel",
        },
        {
            "rule_id": "V496_4_local_blocker_present",
            "rule": "local residual vector contains LRV_DOMAIN_R11_SOURCE_NORMALIZATION",
            "result": "pass" if local_source_norm_rows else "fail",
            "evidence": f"local_source_norm_rows={len(local_source_norm_rows)}",
            "claim_effect": "Newton blocker remains active",
        },
        {
            "rule_id": "V496_5_no_claim_rows",
            "rule": "minimum rows are not claim-valid while missing/conditional inputs remain",
            "result": "pass" if not claim_rows and len(missing_marker_rows) == len(MINIMUM_VECTOR_ROWS) else "fail",
            "evidence": f"claim_rows={len(claim_rows)};missing_or_conditional_rows={len(missing_marker_rows)}",
            "claim_effect": "no Newton/local-GR promotion",
        },
    ]


def missing_ledger_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for row in MINIMUM_VECTOR_ROWS:
        rows.append(
            {
                "row_id": row["row_id"],
                "p8_channel": row["p8_channel"],
                "missing_or_conditional_field": "coefficient_value_or_theorem",
                "current_value": row["coefficient_value_or_theorem"],
                "required_replacement": row["acceptance"],
                "required_source_artifact": row["required_source_artifact"],
                "valid_for_claim": "false",
            }
        )
        rows.append(
            {
                "row_id": row["row_id"],
                "p8_channel": row["p8_channel"],
                "missing_or_conditional_field": "current_status",
                "current_value": row["current_status"],
                "required_replacement": "derived_zero, derived_bound, numeric_bound, or retained_unfilled with explicit no-claim status",
                "required_source_artifact": row["required_source_artifact"],
                "valid_for_claim": "false",
            }
        )
    return rows


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
    missing_rows: list[dict[str, str]],
) -> str:
    return f"""# 496 - R11 Source Normalization Operator Vector Minimum Fill

Private R11/source-normalization checkpoint. This is not a public R11 pass, mu_extra-zero pass, Newtonian-limit pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `495` showed that source-normalized Newtonian recovery needs:

```text
mu_obs = G_EH M_EH + mu_extra
```

with either:

```text
mu_extra = 0
```

or an explicit coefficient/theorem row for every channel.

This checkpoint writes the minimum R11 source-normalization operator fill for all eight `mu_extra` channels.

Short answer:

```text
The eight-channel R11 source-normalization fill is now explicit and parseable.
No row is claim-valid.
Newton/source-normalization remains blocked until rows are theorem-zero or numerically filled.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/R11_source_normalization_operator_vector_minimum_fill.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Minimum Vector Rows

{markdown_table(MINIMUM_VECTOR_ROWS)}

## 5. Acceptance Gates

{markdown_table(ACCEPTANCE_GATE_ROWS)}

## 6. Missing / Conditional Ledger

{markdown_table(missing_rows)}

## 7. Theorem Or Numeric Routes

{markdown_table(THEOREM_OR_NUMERIC_ROWS)}

## 8. Validation

{markdown_table(validations)}

## 9. Decision

{markdown_table(DECISION_ROWS)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
The R11 source-normalization minimum fill now covers all eight mu_extra channels.
The rows are parseable and ready for theorem-zero or numeric input.
```

Forbidden:

```text
MTS has derived mu_extra=0.
MTS has an executable claim-valid R11 source-normalization vector.
MTS has derived source-normalized Newtonian recovery.
MTS has passed PPN or local GR from this row.
```

## 12. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | decide row-by-row whether each channel is a derived-zero theorem target or a numeric input template |
| 2 | T_extra topological theorem or residual score | source normalization is now explicit; extra stress still blocks EH-only local exterior |
| 3 | boundary/domain odd-charge theorem | needed for the conditional Y2/Y3 exchange lanes |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-R11-source-normalization-operator-vector-minimum-fill"
    run_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    missing_rows = missing_ledger_rows()

    write_csv(SOURCE_REGISTER_PATH, sources)
    write_csv(MINIMUM_VECTOR_PATH, MINIMUM_VECTOR_ROWS)
    write_csv(ACCEPTANCE_GATES_PATH, ACCEPTANCE_GATE_ROWS)
    write_csv(MISSING_LEDGER_PATH, missing_rows)
    write_csv(THEOREM_OR_NUMERIC_PATH, THEOREM_OR_NUMERIC_ROWS)
    write_csv(VALIDATION_PATH, validations)
    write_csv(DECISION_PATH, DECISION_ROWS)
    write_csv(ROUTE_UPDATE_PATH, ROUTE_UPDATE_ROWS)

    doc = build_doc(args.timestamp, generated_at_utc, run_dir, sources, validations, missing_rows)
    (ROOT / DOC_PATH).write_text(doc, encoding="utf-8")

    missing_sources = [row["source_file"] for row in sources if row["exists"] != "True"]
    failed_validations = [row for row in validations if row["result"] == "fail"]
    claim_rows = [row for row in MINIMUM_VECTOR_ROWS if row["valid_for_claim"] == "true"]
    missing_or_conditional_rows = [
        row for row in MINIMUM_VECTOR_ROWS
        if str(row["coefficient_value_or_theorem"]).startswith("MISSING")
        or row["current_status"] in {"minimum_row_missing_input", "conditional_calibration_not_claimable"}
    ]
    status = {
        "timestamp": args.timestamp,
        "generated_at_utc": generated_at_utc,
        "status": STATUS,
        "claim_ceiling": CLAIM_CEILING,
        "checkpoint_doc": str(DOC_PATH),
        "run_dir": str(run_dir),
        "source_register": str(ROOT / SOURCE_REGISTER_PATH),
        "minimum_vector": str(ROOT / MINIMUM_VECTOR_PATH),
        "acceptance_gates": str(ROOT / ACCEPTANCE_GATES_PATH),
        "missing_ledger": str(ROOT / MISSING_LEDGER_PATH),
        "theorem_or_numeric_routes": str(ROOT / THEOREM_OR_NUMERIC_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "minimum_vector_rows": len(MINIMUM_VECTOR_ROWS),
        "acceptance_gate_rows": len(ACCEPTANCE_GATE_ROWS),
        "missing_ledger_rows": len(missing_rows),
        "theorem_or_numeric_rows": len(THEOREM_OR_NUMERIC_ROWS),
        "failed_validation_rows": len(failed_validations),
        "claim_valid_minimum_rows": len(claim_rows),
        "missing_or_conditional_minimum_rows": len(missing_or_conditional_rows),
        "all_mu_extra_channels_covered": True,
        "R11_source_normalization_minimum_fill_written": True,
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
