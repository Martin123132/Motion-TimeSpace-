from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "Y5_extra_mass_projection_silence_theorem_written_current_MTS_not_derived_channelwise_bound_inputs_written"
CLAIM_CEILING = "extra_mass_projection_silence_or_channelwise_bound_only_no_mu_extra_zero_Newton_PPN_or_local_GR_promotion"
NEXT_TARGET = "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md"

DOC_PATH = Path("522-Y5-extra-mass-projection-silence-or-channelwise-bound.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_SOURCE_REGISTER.csv")
SILENCE_THEOREM_PATH = Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_PROJECTION_SILENCE_THEOREM.csv")
CHANNEL_BOUND_PATH = Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_CHANNELWISE_BOUND_INPUT.csv")
OBSERVABLE_MAP_PATH = Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_OBSERVABLE_MAP.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_DECISION.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_VALIDATION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_Y5_EXTRA_MASS_ROUTE_UPDATE.csv")


SOURCE_REGISTER = [
    {
        "source_file": "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
        "role": "selects extra mass projection as next target after Pi_M owner fork",
    },
    {
        "source_file": "520-Y5-source-current-Ward-closure-or-bound-row.md",
        "role": "Ward-to-mass-flux bridge and extra exchange obstruction",
    },
    {
        "source_file": "507-field-specific-silence-queue-kappa-domain-memory-motion.md",
        "role": "field-specific silence queue for kappa, domain, memory, and motion sectors",
    },
    {
        "source_file": "506-local-EH-reduction-and-extra-sector-silence-theorem.md",
        "role": "local EH reduction and extra-sector silence theorem attempt",
    },
    {
        "source_file": "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
        "role": "exact source identity residual decomposition",
    },
    {
        "source_file": "496-R11-source-normalization-operator-vector-minimum-fill.md",
        "role": "eight-channel source-normalization minimum fill",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_PIM_RADIAL_BOUND_INPUT.csv",
        "role": "521 Pi_M radial bound input rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv",
        "role": "499 projector, boundary, domain, bulk, non-EH, coupling, frame/species, anomaly residual split",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_CLAUSES.csv",
        "role": "source-measure clauses including no-extra-channel condition",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
        "role": "source-measure residual map",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_WORLDTUBE_MEFF_RESIDUAL_RUNNER.csv",
        "role": "worldtube M_eff residual runner",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv",
        "role": "R11 source-normalization operator minimum fill rows",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv",
        "role": "mu_extra source-normalization coefficient vector",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv",
        "role": "numeric input template for source-normalization channels",
    },
    {
        "source_file": "scripts/Y5_extra_mass_projection_silence_or_channelwise_bound.py",
        "role": "this checkpoint generator",
    },
]


SILENCE_THEOREM_ROWS = [
    {
        "theorem_id": "EM522_0_extra_current_split",
        "statement": "All non-Hilbert source-normalization channels are split before any cancellation is considered.",
        "math_form": "J_extra = J_boundary + J_domain + J_bulk/memory + J_nonEH + J_kappa + J_frame/species + J_PiM + J_anomaly",
        "zero_condition": "each channel has zero Pi_M projection or a sourced bound",
        "current_status": "split_written_not_zero",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "EM522_1_projection_identity",
        "statement": "The Y5 extra mass obstruction is the projected derivative of those extra channels.",
        "math_form": "I_extra = int_A Pi_M dJ_extra = sum_i int_A Pi_M dJ_i",
        "zero_condition": "I_i=0 for every channel, without unsourced cancellation",
        "current_status": "identity_written",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "EM522_2_no_cancellation_gate",
        "statement": "A large open channel cannot be hidden by an opposite open channel.",
        "math_form": "|epsilon_extra| <= sum_i |epsilon_i|, not epsilon_total tuned to zero",
        "zero_condition": "each epsilon_i is theorem-zero or individually below its mapped local bound",
        "current_status": "policy_gate_written",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "EM522_3_silence_theorem",
        "statement": "If every extra mass projection channel is zero and Pi_M commutator is zero, then the extra projection part of Y5 vanishes.",
        "math_form": "Pi_M dJ_extra=0 and [d,Pi_M]J_H=0 => d(Pi_M J_H)=Pi_M dJ_H",
        "zero_condition": "all channel rows below pass plus Ward/mass-generator closure",
        "current_status": "conditional_not_current_MTS_derived",
        "valid_for_claim": "false",
    },
    {
        "theorem_id": "EM522_4_bound_fallback",
        "statement": "If the silence theorem does not land, every channel becomes a residual input.",
        "math_form": "epsilon_mu_extra_i = c_M I_i/M_eff_ref",
        "zero_condition": "numeric/source-backed coefficient with units, normalization, weak-field map, and bound comparison",
        "current_status": "fallback_input_written",
        "valid_for_claim": "false",
    },
]


CHANNEL_BOUND_ROWS = [
    {
        "channel_id": "EX522_0_boundary_improvement",
        "p8_channel": "boundary_monopole_shift",
        "symbol": "epsilon_boundary",
        "projection": "I_boundary = int_A Pi_M dJ_boundary + int_boundary Pi_M K_owner",
        "theorem_zero_route": "boundary no-hair/no-flux theorem or class-only global constant with zero derivatives",
        "bound_input_required": "epsilon_boundary;boundary_flux_vector;alpha3_map;xi_map;Gdot_map;units;source_file",
        "observable_locks": "beta_minus_1;alpha3<=4e-20;xi<=4e-9;Gdot<=9.6e-15 yr^-1",
        "current_status": "not_derived_not_filled",
        "valid_for_claim": "false",
    },
    {
        "channel_id": "EX522_1_domain_projector",
        "p8_channel": "domain_projector_mass",
        "symbol": "epsilon_domain_projector",
        "projection": "I_domain = int_A Pi_M dJ_domain + domain/homology variation",
        "theorem_zero_route": "domain selector is topological/covariant with no mass projection, no vector, no anisotropy, and no time/range derivative",
        "bound_input_required": "W_domain_alpha1;epsilon_domain_vector;W_domain_alpha2;W_domain_alpha3;epsilon_domain_flux;W_domain_xi;epsilon_domain_anisotropy;source_file",
        "observable_locks": "alpha1<=1e-4;alpha2<=2e-9;alpha3<=4e-20;xi<=4e-9;R11",
        "current_status": "not_derived_not_filled",
        "valid_for_claim": "false",
    },
    {
        "channel_id": "EX522_2_bulk_memory_range",
        "p8_channel": "bulk_X_Yukawa_tail",
        "symbol": "epsilon_bulk_X",
        "projection": "I_bulk = int_A Pi_M dJ_bulk/memory/range",
        "theorem_zero_route": "positive source-free mass-gap/no-hair theorem or zero Pi_M projection of bulk/memory exchange",
        "bound_input_required": "lambda_X;alpha_X;epsilon_bulk_X;range_units;alpha_lambda_bound;source_file;assumptions",
        "observable_locks": "alpha(lambda) fifth-force curve below local bounds",
        "current_status": "not_derived_not_filled",
        "valid_for_claim": "false",
    },
    {
        "channel_id": "EX522_3_nonEH_operator",
        "p8_channel": "nonEH_operator_potential",
        "symbol": "epsilon_nonEH_source",
        "projection": "I_nonEH = int_A Pi_M dJ_nonEH plus non-EH source residual S_res",
        "theorem_zero_route": "same-frame local exterior is EH plus Lambda with all non-EH coefficients zero/topological/bounded",
        "bound_input_required": "operator_family;coefficient_value;units;normalization;weak_field_map;affected_rows;source_file",
        "observable_locks": "gamma<=2.3e-5;beta<=7.8e-5;alpha(lambda);R11",
        "current_status": "not_derived_not_filled",
        "valid_for_claim": "false",
    },
    {
        "channel_id": "EX522_4_coupling_drift",
        "p8_channel": "time_drift",
        "symbol": "epsilon_time_drift",
        "projection": "I_kappa = int_A Pi_M(T_obs d kappa_eff) plus running G_eff terms",
        "theorem_zero_route": "topological/global kappa sector with no time, range, species, radial, frame, or domain derivatives",
        "bound_input_required": "time_window;epsilon_time_drift;dln_mu_dt;Gdot_over_G;units;source_file",
        "observable_locks": "Gdot/G<=9.6e-15 yr^-1 or derived zero",
        "current_status": "conditional_from_508_not_derived_here",
        "valid_for_claim": "false",
    },
    {
        "channel_id": "EX522_5_frame_species_source",
        "p8_channel": "species_source_charge",
        "symbol": "epsilon_species_A",
        "projection": "I_species = int_A Pi_M dJ_frame/species",
        "theorem_zero_route": "same observed coframe plus selector-blind dressed source charge for all matter species",
        "bound_input_required": "species_pair;epsilon_species_A;eta_source_AB;clock_residual;source_file;assumptions",
        "observable_locks": "eta_source_AB<=2.8e-15 plus clock/frame residual locks",
        "current_status": "same_coframe_direct_charge_partial_dressed_source_not_derived",
        "valid_for_claim": "false",
    },
    {
        "channel_id": "EX522_6_projector_stress",
        "p8_channel": "projector_variation_mass",
        "symbol": "Delta_PiM",
        "projection": "I_PiM = int_A [d,Pi_M]J_H or int_S (delta Pi_M)J_H",
        "theorem_zero_route": "topological absolute Pi_M with Hilbert equality or variation stress theorem-cancelled",
        "bound_input_required": "projector_type;metric_dependence_flag;Delta_PiM;units;normalization;source_file;assumptions",
        "observable_locks": "projector stress mapped to gamma/beta/alpha_i/xi/R11/Y5 rows",
        "current_status": "not_derived_not_filled",
        "valid_for_claim": "false",
    },
    {
        "channel_id": "EX522_7_parent_anomaly_multiplier",
        "p8_channel": "parent_anomaly_or_multiplier",
        "symbol": "A_parent",
        "projection": "I_anomaly = int_A A_parent",
        "theorem_zero_route": "no ad hoc source-normalization multiplier, or multiplier is first-class/gauge/topological/Ward-owned with zero stress",
        "bound_input_required": "multiplier_id;A_parent_integral;units;stress_map;source_file;assumptions",
        "observable_locks": "closure-only radial residual;R1;R4;R7;R9;R11",
        "current_status": "not_satisfied",
        "valid_for_claim": "false",
    },
    {
        "channel_id": "EX522_8_absolute_calibration",
        "p8_channel": "absolute_calibration_offset",
        "symbol": "epsilon_calibration",
        "projection": "not a force channel by itself, but shifts measured-GM normalization if not parent-fixed",
        "theorem_zero_route": "parent-fixed universal calibration with zero range/time/species derivatives",
        "bound_input_required": "lambda0;universality_certificate;range_derivative;time_derivative;species_derivative;source_file",
        "observable_locks": "beta_minus_1;Gdot_over_G;absolute GM normalization",
        "current_status": "conditional_harmless_not_parent_fixed",
        "valid_for_claim": "false",
    },
]


OBSERVABLE_MAP_ROWS = [
    {
        "map_id": "OM522_0_total_extra_bound",
        "quantity": "epsilon_mu_extra_total",
        "formula": "epsilon_mu_extra_total <= sum_i |epsilon_i|",
        "needed_before_claim": "all channel units, normalization, source files, and no-cancellation flag",
        "claim_status": "not_run",
    },
    {
        "map_id": "OM522_1_radial_hair",
        "quantity": "epsilon_radial_Meff",
        "formula": "epsilon_radial_Meff = M_eff_ref^-1 int_A[-Pi_M dJ_extra + [d,Pi_M]J_H + A_parent]",
        "needed_before_claim": "channelwise I_i plus Pi_M commutator/anomaly integrals",
        "claim_status": "not_run",
    },
    {
        "map_id": "OM522_2_PPN_source_vector",
        "quantity": "Delta_PPN_source",
        "formula": "weak-field map of boundary/domain/nonEH/projector stress into gamma,beta,alpha_i,xi",
        "needed_before_claim": "operator coefficients and second-order PPN source expansion",
        "claim_status": "not_derived",
    },
    {
        "map_id": "OM522_3_local_bounds",
        "quantity": "local bound comparison",
        "formula": "compare each epsilon_i or operator coefficient to row-specific local locks",
        "needed_before_claim": "numeric residual values or theorem-zero certificates",
        "claim_status": "not_filled",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D522_0_silence_theorem",
        "status": "conditional_theorem_written",
        "meaning": "zero extra mass projection requires every boundary/domain/bulk/nonEH/kappa/frame/species/projector/anomaly channel to have zero Pi_M projection",
        "claim_status": "not_current_MTS_derived",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D522_1_no_cancellation",
        "status": "policy_gate_active",
        "meaning": "open extra channels cannot cancel each other into a claimed Newton/GR pass",
        "claim_status": "no_claim",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D522_2_bound_inputs",
        "status": "channelwise_inputs_written_not_filled",
        "meaning": "every extra mass projection channel now has required columns, observables, and theorem-zero route",
        "claim_status": "test_branch_only",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D522_3_next",
        "status": "calibration_is_next_if_bounds_or_theorems_land",
        "meaning": "even if extra projection were zero, measured GM still needs Gauss/orbital calibration and PPN source stability",
        "claim_status": "local_GR_claim_false",
        "next_action": NEXT_TARGET,
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "Y5_EXTRA_MASS_PROJECTION",
        "previous_status": "still_blocked_PiM_owner_not_enough_without_extra_projection_silence_and_calibration",
        "new_status": "silence_theorem_written_channelwise_bound_inputs_written_no_zero_derived",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Y5_MEFF_CONSERVATION",
        "previous_status": "still_open_PiM_commutator_and_owner_not_derived",
        "new_status": "still_open_extra_projection_channels_not_zero_or_scored",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "Y5_RADIAL_SOURCE_HAIR",
        "previous_status": "PiM_commutator_and_Delta_PiM_bound_inputs_written_not_filled",
        "new_status": "radial_integral_now_has_channelwise_extra_mass_inputs_not_filled",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "still_blocked_PiM_owner_not_enough_without_extra_projection_silence_and_calibration",
        "new_status": "still_blocked_by_unfilled_mu_extra_channels_and_Gauss_orbital_calibration",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "still_blocked_PiM_projector_not_current_MTS_derived",
        "new_status": "still_blocked_extra_mass_projection_and_second_order_PPN_source_stability",
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
    residual_rows = read_csv(Path("source-intake/mts_residuals/P8_PARENT_SOURCE_IDENTITY_RESIDUAL_DECOMPOSITION.csv"))
    r11_rows = read_csv(Path("source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv"))
    mu_extra_rows = read_csv(Path("source-intake/mts_residuals/P8_MU_EXTRA_SOURCE_NORMALIZATION_COEFFICIENT_VECTOR.csv"))
    numeric_rows = read_csv(Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv"))
    required_channels = {
        "boundary_monopole_shift",
        "domain_projector_mass",
        "bulk_X_Yukawa_tail",
        "nonEH_operator_potential",
        "time_drift",
        "species_source_charge",
        "projector_variation_mass",
        "parent_anomaly_or_multiplier",
        "absolute_calibration_offset",
    }
    channel_set = {row["p8_channel"] for row in CHANNEL_BOUND_ROWS}
    claim_theorem_rows = [row for row in SILENCE_THEOREM_ROWS if row["valid_for_claim"] == "true"]
    claim_channel_rows = [row for row in CHANNEL_BOUND_ROWS if row["valid_for_claim"] == "true"]
    return [
        {
            "check_id": "V522_0_source_paths_exist",
            "result": "pass" if not missing_sources else "fail",
            "detail": f"missing={len(missing_sources)}",
        },
        {
            "check_id": "V522_1_prior_decomposition_loaded",
            "result": "pass" if len(residual_rows) >= 8 else "fail",
            "detail": f"residual_rows={len(residual_rows)}",
        },
        {
            "check_id": "V522_2_source_norm_inputs_loaded",
            "result": "pass" if len(r11_rows) >= 8 and len(mu_extra_rows) >= 8 and len(numeric_rows) >= 8 else "fail",
            "detail": f"r11_rows={len(r11_rows)};mu_extra_rows={len(mu_extra_rows)};numeric_rows={len(numeric_rows)}",
        },
        {
            "check_id": "V522_3_channel_coverage",
            "result": "pass" if required_channels.issubset(channel_set) else "fail",
            "detail": ";".join(sorted(channel_set)),
        },
        {
            "check_id": "V522_4_silence_theorem_written",
            "result": "pass" if len(SILENCE_THEOREM_ROWS) == 5 else "fail",
            "detail": f"silence_rows={len(SILENCE_THEOREM_ROWS)}",
        },
        {
            "check_id": "V522_5_observable_map_written",
            "result": "pass" if len(OBSERVABLE_MAP_ROWS) == 4 else "fail",
            "detail": f"observable_rows={len(OBSERVABLE_MAP_ROWS)}",
        },
        {
            "check_id": "V522_6_no_overclaim",
            "result": "pass" if not claim_theorem_rows and not claim_channel_rows else "fail",
            "detail": "extra_mass_projection_zero_derived=false; channelwise_bounds_filled=false; mu_extra_zero_derived=false; source_normalized_Newton_promoted=false; local_GR_claim_allowed=false",
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
    return f"""# 522 - Y5 Extra Mass Projection Silence or Channelwise Bound

Generated: {generated_at_utc}  
Run: `{rel(run_dir)}`  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`

## 1. Verdict

Even a good `Pi_M` is not enough.

The Y5 source-normalization branch also needs:

```text
Pi_M dJ_extra = 0.
```

The extra current is now split channel-by-channel:

```text
J_extra = J_boundary + J_domain + J_bulk/memory + J_nonEH
        + J_kappa + J_frame/species + J_PiM + J_anomaly.
```

Current MTS has not derived zero projection for these channels. So this checkpoint writes the silence theorem and the channelwise bound inputs, with no cancellation credit.

## 2. Silence Theorem

{markdown_table(SILENCE_THEOREM_ROWS)}

## 3. Channelwise Bound Inputs

{markdown_table(CHANNEL_BOUND_ROWS)}

## 4. Observable Map

{markdown_table(OBSERVABLE_MAP_ROWS)}

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
MTS now has an explicit no-extra-mass-projection theorem target.
Every extra projected mass channel has a theorem-zero route and a bound-input schema.
The no-cancellation policy is explicit.
```

Forbidden:

```text
MTS has derived Pi_M dJ_extra=0 for the current corpus.
MTS has derived mu_extra=0.
MTS has scored the channelwise residuals below local bounds.
MTS has derived measured GM, source-normalized Newton, PPN silence, or local GR.
```

## 10. Next Target

`{NEXT_TARGET}`

If future work derives or fills the channel rows, the next gate is whether the closed/silent source charge calibrates to the actual orbital inverse-square `GM` and survives PPN source order.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-Y5-extra-mass-projection-silence-or-channelwise-bound"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)
    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (SILENCE_THEOREM_PATH, SILENCE_THEOREM_ROWS),
        (CHANNEL_BOUND_PATH, CHANNEL_BOUND_ROWS),
        (OBSERVABLE_MAP_PATH, OBSERVABLE_MAP_ROWS),
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
        "silence_theorem": str(ROOT / SILENCE_THEOREM_PATH),
        "channel_bound_input": str(ROOT / CHANNEL_BOUND_PATH),
        "observable_map": str(ROOT / OBSERVABLE_MAP_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "silence_theorem_rows": len(SILENCE_THEOREM_ROWS),
        "channel_bound_rows": len(CHANNEL_BOUND_ROWS),
        "observable_map_rows": len(OBSERVABLE_MAP_ROWS),
        "failed_validation_rows": len(failed_validations),
        "extra_mass_projection_silence_theorem_written": True,
        "extra_mass_projection_zero_derived_for_MTS": False,
        "channelwise_bound_inputs_written": True,
        "channelwise_bounds_filled": False,
        "no_cancellation_policy_active": True,
        "mu_extra_zero_derived": False,
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
