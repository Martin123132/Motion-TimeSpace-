from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

STATUS = "radial_Meff_flux_theorem_sharpened_calibration_lock_attempted_parent_source_identity_and_calibration_not_derived_no_Newton_or_local_GR_promotion"
CLAIM_CEILING = "radial_and_calibration_theorem_attempt_only_no_mu_extra_zero_Newton_PPN_R11_or_local_GR_promotion"
NEXT_TARGET = "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md"

DOC_PATH = Path("498-source-normalization-radial-and-calibration-theorem-attempt.md")
SOURCE_REGISTER_PATH = Path("source-intake/mts_residuals/P8_RADIAL_CALIBRATION_SOURCE_REGISTER.csv")
RADIAL_THEOREM_PATH = Path("source-intake/mts_residuals/P8_RADIAL_MEFF_THEOREM_ATTEMPT.csv")
CALIBRATION_LOCK_PATH = Path("source-intake/mts_residuals/P8_CALIBRATION_LOCK_ATTEMPT.csv")
COUPLING_GATES_PATH = Path("source-intake/mts_residuals/P8_RADIAL_CALIBRATION_COUPLING_GATES.csv")
NUMERIC_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_RADIAL_CALIBRATION_NUMERIC_TEMPLATE.csv")
VALIDATION_PATH = Path("source-intake/mts_residuals/P8_RADIAL_CALIBRATION_VALIDATION.csv")
DECISION_PATH = Path("source-intake/mts_residuals/P8_RADIAL_CALIBRATION_DECISION.csv")
ROUTE_UPDATE_PATH = Path("source-intake/mts_residuals/P8_RADIAL_CALIBRATION_ROUTE_UPDATE.csv")

ROUTE_CLASSIFICATION_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_ROUTE_CLASSIFICATION.csv")
DERIVED_ZERO_TARGETS_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_DERIVED_ZERO_TARGETS.csv")
NUMERIC_INPUT_TEMPLATE_PATH = Path("source-intake/mts_residuals/P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv")
MINIMUM_VECTOR_PATH = Path("source-intake/mts_residuals/P8_R11_SOURCE_NORMALIZATION_OPERATOR_MINIMUM_FILL.csv")
GM_ABSORPTION_PATH = Path("runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/GM_absorption_theorem_attempt.csv")
GM_CONTRACT_PATH = Path("runs/20260602-002500-source-normalization-Geff-Meff-GM-absorption-theorem/results/source_normalization_contract.csv")
MONOPOLE_CHAIN_PATH = Path("runs/20260601-000061-Meff-monopole-source-normalization-or-radial-memory-hair/results/monopole_flux_theorem_chain.csv")


SOURCE_REGISTER = [
    {
        "source_file": "497-source-normalization-derived-zero-route-or-numeric-input-template.md",
        "role": "selects radial M_eff plus absolute calibration as first source-normalization derivation target",
    },
    {
        "source_file": "496-R11-source-normalization-operator-vector-minimum-fill.md",
        "role": "defines epsilon_radial_Meff and epsilon_calibration as unfilled mu_extra channels",
    },
    {
        "source_file": "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
        "role": "conditional compact-exterior closed Pi_M flux theorem",
    },
    {
        "source_file": "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
        "role": "guardrails for measured-GM absorption and calibration derivatives",
    },
    {
        "source_file": "402-EH-source-normalization-parent-pair.md",
        "role": "same-frame EH to Poisson to measured-mass source-normalization chain",
    },
    {
        "source_file": "467-mu-extra-zero-owner-or-source-normalization-coefficient-vector.md",
        "role": "mu_extra coefficient vector requiring row-by-row ownership",
    },
    {
        "source_file": "454-PiM-parent-symplectic-projector-algebra-attempt.md",
        "role": "Pi_M projector ownership attempt feeding flux closure",
    },
    {
        "source_file": "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
        "role": "Pi_M flux closure/Ward current attempt",
    },
    {
        "source_file": "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "role": "Hamiltonian boundary mass-current route",
    },
    {
        "source_file": "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
        "role": "Poisson/Gauss calibration gate between charge and Newtonian source",
    },
    {
        "source_file": str(ROUTE_CLASSIFICATION_PATH),
        "role": "497 route classification machine artifact",
    },
    {
        "source_file": str(DERIVED_ZERO_TARGETS_PATH),
        "role": "497 derived-zero theorem targets",
    },
    {
        "source_file": str(NUMERIC_INPUT_TEMPLATE_PATH),
        "role": "497 numeric templates",
    },
    {
        "source_file": str(MINIMUM_VECTOR_PATH),
        "role": "496 minimum source-normalization vector",
    },
    {
        "source_file": str(GM_ABSORPTION_PATH),
        "role": "378 GM absorption attempt result rows where available",
    },
    {
        "source_file": str(GM_CONTRACT_PATH),
        "role": "378 source-normalization contract rows where available",
    },
    {
        "source_file": str(MONOPOLE_CHAIN_PATH),
        "role": "244 flux theorem chain where available",
    },
    {
        "source_file": "scripts/source_normalization_radial_and_calibration_theorem_attempt.py",
        "role": "this checkpoint generator",
    },
]


RADIAL_THEOREM_ROWS = [
    {
        "row_id": "R498_radial_0_setup",
        "object": "compact_exterior_annulus",
        "formula_or_condition": "A_ext = S2 x [r1,r2], with no ordinary matter support in the open annulus",
        "derived_if": "local exterior branch is compact, isolated, and uses the same observed source frame",
        "current_status": "conditional_geometry_available_from_244",
        "failure_mode": "source/current may leak through boundary/domain/relative-memory sectors",
        "claim_effect": "sets stage only",
        "valid_for_claim": "false",
    },
    {
        "row_id": "R498_radial_1_mass_projector",
        "object": "Pi_M",
        "formula_or_condition": "Pi_M extracts the absolute H2(S2) mass flux and commutes with exterior d on the mass subcomplex",
        "derived_if": "parent symplectic/projector algebra proves Pi_M is an owned projector rather than a chosen readout",
        "current_status": "conditional_projector_not_parent_locked",
        "failure_mode": "relative memory, boundary, or domain classes can contaminate the absolute flux",
        "claim_effect": "keeps radial theorem conditional",
        "valid_for_claim": "false",
    },
    {
        "row_id": "R498_radial_2_flux_difference",
        "object": "Delta_Meff",
        "formula_or_condition": "M_eff(r2)-M_eff(r1) = c_M * int_A_ext d(Pi_M J)",
        "derived_if": "Stokes theorem applies and M_eff(r)=c_M int_S2_r Pi_M J",
        "current_status": "derived_conditionally_from_244",
        "failure_mode": "nonzero d(Pi_M J) creates radial source hair",
        "claim_effect": "exact residual identity",
        "valid_for_claim": "false",
    },
    {
        "row_id": "R498_radial_3_zero_law",
        "object": "epsilon_radial_Meff",
        "formula_or_condition": "epsilon_radial_Meff(r1,r2) = [c_M/M_eff(r1)] * int_A_ext d(Pi_M J)",
        "derived_if": "d(Pi_M J)=0 in the compact exterior annulus",
        "current_status": "conditional_zero_law_not_parent_proved",
        "failure_mode": "any owned nonzero exterior source current becomes R4/R10/R11 residual",
        "claim_effect": "would zero radial_Meff_hair only if source identity is proved",
        "valid_for_claim": "false",
    },
    {
        "row_id": "R498_radial_4_bound_law",
        "object": "radial_bound",
        "formula_or_condition": "|epsilon_radial_Meff| <= |c_M|/M_eff * int_A_ext |d(Pi_M J)|",
        "derived_if": "a normed exterior source-current residual can be supplied",
        "current_status": "bound_form_written_numeric_input_missing",
        "failure_mode": "without a source-current norm or units the row cannot be scored",
        "claim_effect": "fallback numeric template target",
        "valid_for_claim": "false",
    },
    {
        "row_id": "R498_radial_5_no_leakage",
        "object": "source_channel_split",
        "formula_or_condition": "Pi_M J_extra = Pi_M(J_rel + J_boundary + J_domain + J_bulk + J_nonEH) = exact_or_zero_flux",
        "derived_if": "each non-mass channel is either exact on S2 or orthogonal to the absolute harmonic mass class",
        "current_status": "not_derived",
        "failure_mode": "a silent-looking extra sector can shift the mass monopole",
        "claim_effect": "blocks promotion",
        "valid_for_claim": "false",
    },
]


CALIBRATION_LOCK_ROWS = [
    {
        "row_id": "C498_cal_0_same_frame",
        "calibration_requirement": "same observed matter/metric frame",
        "formula_or_condition": "the stress tensor sourcing the weak-field Poisson equation is the same source whose flux defines M_eff",
        "current_status": "conditional_from_402_not_parent_derived",
        "failure_mode": "field-frame relabelling hides source debt in G_eff or M_eff",
        "claim_effect": "calibration cannot be promoted",
        "valid_for_claim": "false",
    },
    {
        "row_id": "C498_cal_1_flux_mass_equality",
        "calibration_requirement": "flux-to-Hilbert-mass equality",
        "formula_or_condition": "c_M int_S2 Pi_M J = M_EH for the inner boundary of the compact source",
        "current_status": "not_derived",
        "failure_mode": "constant offset epsilon_calibration remains possible",
        "claim_effect": "absolute_calibration_offset retained",
        "valid_for_claim": "false",
    },
    {
        "row_id": "C498_cal_2_constant_kappa",
        "calibration_requirement": "parent-fixed kappa",
        "formula_or_condition": "G_parent = kappa_parent c^4/(8*pi), with partial_r G_parent = partial_t G_parent = partial_A G_parent = 0",
        "current_status": "not_parent_derived",
        "failure_mode": "radial/time/species drift is physics, not a unit convention",
        "claim_effect": "R4/R9/R11 remain open",
        "valid_for_claim": "false",
    },
    {
        "row_id": "C498_cal_3_range_independence",
        "calibration_requirement": "no finite-range source dependence",
        "formula_or_condition": "partial_lambda mu_obs = 0 and alpha_X(lambda_X)=0 for source-normalization channels",
        "current_status": "not_derived",
        "failure_mode": "Yukawa/bulk tail cannot be absorbed into measured GM",
        "claim_effect": "R10 remains open",
        "valid_for_claim": "false",
    },
    {
        "row_id": "C498_cal_4_species_universality",
        "calibration_requirement": "source-side universality",
        "formula_or_condition": "Delta_A mu_obs = 0 for all source/test species pairs in the local branch",
        "current_status": "not_parent_derived",
        "failure_mode": "source-side WEP residual survives",
        "claim_effect": "R1/R2/R11 remain open",
        "valid_for_claim": "false",
    },
    {
        "row_id": "C498_cal_5_zero_constant_or_parent_unit",
        "calibration_requirement": "absolute offset either zero or a parent-fixed unit convention",
        "formula_or_condition": "epsilon_calibration = lambda0 - 1 is harmless only if lambda0 is universal and all derivatives vanish",
        "current_status": "conditional_harmless_not_parent_fixed",
        "failure_mode": "a fitted lambda0 is a closure, not a derivation",
        "claim_effect": "no source-normalized Newton claim",
        "valid_for_claim": "false",
    },
]


COUPLING_GATE_ROWS = [
    {
        "gate_id": "G498_0_radial_identity",
        "gate": "radial residual identity",
        "pass_condition": "Delta_Meff = c_M int_A d(Pi_M J) is explicit",
        "current_result": "conditional_pass",
        "evidence": "radial theorem rows R498_radial_2 and R498_radial_3",
        "claim_effect": "useful exact identity but not a zero theorem",
    },
    {
        "gate_id": "G498_1_parent_source_identity",
        "gate": "closed absolute mass flux",
        "pass_condition": "parent action proves d(Pi_M J)=0 in compact exterior vacuum",
        "current_result": "fail_open",
        "evidence": "244/378 list Pi_M flux closure as not parent-derived",
        "claim_effect": "epsilon_radial_Meff not claim-zero",
    },
    {
        "gate_id": "G498_2_no_leakage",
        "gate": "no relative/boundary/domain/bulk/nonEH leakage",
        "pass_condition": "all non-mass source channels are exact or orthogonal to Pi_M flux",
        "current_result": "fail_open",
        "evidence": "496 keeps all eight mu_extra channels unfilled",
        "claim_effect": "source-normalized Newton blocked",
    },
    {
        "gate_id": "G498_3_absolute_calibration",
        "gate": "flux charge equals same-frame Hilbert mass",
        "pass_condition": "c_M int Pi_M J = M_EH and kappa_parent fixes G_parent in the same frame",
        "current_result": "fail_open",
        "evidence": "378/402 reject measured-GM absorption as parent-derived",
        "claim_effect": "epsilon_calibration not claim-zero",
    },
    {
        "gate_id": "G498_4_derivative_hair",
        "gate": "no radius/time/range/species derivatives",
        "pass_condition": "partial_r mu = partial_t mu = partial_lambda mu = Delta_A mu = 0",
        "current_result": "fail_open",
        "evidence": "378 guardrails and 497 numeric templates remain active",
        "claim_effect": "GM absorption remains conditional only",
    },
    {
        "gate_id": "G498_5_promotion_guard",
        "gate": "no false local-GR promotion",
        "pass_condition": "local_GR_claim_allowed=false while source identity/calibration are open",
        "current_result": "pass",
        "evidence": "all claim-valid flags remain false",
        "claim_effect": "private derivation discipline preserved",
    },
]


NUMERIC_TEMPLATE_ROWS = [
    {
        "template_id": "N498_0_source_current_norm",
        "target_channel": "radial_Meff_hair",
        "coefficient_symbol": "epsilon_radial_Meff",
        "required_columns": "r1;r2;c_M;M_eff_ref;int_A_dPiMJ;norm_convention;units;source_file;assumptions",
        "bound_formula": "epsilon_radial_Meff = c_M*int_A_dPiMJ/M_eff_ref",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "N498_1_radial_profile",
        "target_channel": "radial_Meff_hair",
        "coefficient_symbol": "epsilon_radial_Meff",
        "required_columns": "r;M_eff_r;dln_Meff_dlnr;dln_Geff_dlnr;dln_mu_dlnr;units;source_file;assumptions",
        "bound_formula": "dln_mu_dlnr = dln_Geff_dlnr + dln_Meff_dlnr",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "N498_2_calibration_owner",
        "target_channel": "absolute_calibration_offset",
        "coefficient_symbol": "epsilon_calibration",
        "required_columns": "lambda0;G_parent_definition;M_flux_definition;M_EH_definition;same_frame_certificate;source_file;assumptions",
        "bound_formula": "epsilon_calibration = lambda0 - 1 unless lambda0 is parent-fixed universal unit normalization",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
    {
        "template_id": "N498_3_derivative_hair",
        "target_channel": "absolute_calibration_offset",
        "coefficient_symbol": "epsilon_calibration",
        "required_columns": "dln_mu_dr;dln_mu_dt;dln_mu_dlambda;Delta_species_mu;units;source_file;assumptions",
        "bound_formula": "all derivative hair must be zero or mapped to R4/R9/R10/R11 bounds",
        "template_status": "not_filled",
        "valid_for_claim": "false",
    },
]


DECISION_ROWS = [
    {
        "decision_id": "D498_0_radial_theorem",
        "status": "conditional_identity_sharpened",
        "meaning": "epsilon_radial_Meff is exactly the normalized exterior Pi_M source-current integral",
        "next_action": NEXT_TARGET,
    },
    {
        "decision_id": "D498_1_zero_route",
        "status": "not_parent_derived",
        "meaning": "closed Pi_M flux would zero radial hair, but the parent source identity and no-leakage theorem are still missing",
        "next_action": "derive parent source identity or fill radial numeric template",
    },
    {
        "decision_id": "D498_2_calibration",
        "status": "not_locked",
        "meaning": "absolute calibration remains harmless only as a parent-fixed universal constant, not as a fitted closure",
        "next_action": "prove flux-to-Hilbert-mass equality and constant universal kappa",
    },
    {
        "decision_id": "D498_3_promotion",
        "status": "forbidden",
        "meaning": "no mu_extra zero, Newtonian source-normalization, R11, PPN, or local-GR pass is earned",
        "next_action": NEXT_TARGET,
    },
]


ROUTE_UPDATE_ROWS = [
    {
        "route_id": "RADIAL_MEFF_HAIR",
        "previous_status": "theorem_first_conditional_from_244",
        "new_status": "exact_residual_identity_written_parent_closed_flux_missing",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "ABSOLUTE_CALIBRATION_OFFSET",
        "previous_status": "parent_fixed_calibration_or_retained_closure",
        "new_status": "calibration_lock_conditions_written_not_parent_fixed",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "SOURCE_NORMALIZED_NEWTON",
        "previous_status": "first_derivation_target_radial_Meff_plus_absolute_calibration",
        "new_status": "blocked_by_parent_source_identity_and_calibration_lock",
        "accepted_for_claim": "false",
        "next_target": NEXT_TARGET,
    },
    {
        "route_id": "LOCAL_GR",
        "previous_status": "blocked_but_mu_extra_route_partitioned",
        "new_status": "still_blocked_source_normalization_plus_extra_stress",
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
        rows.append(
            {
                **row,
                "exists": str((ROOT / source_file).exists()),
            }
        )
    return rows


def validation_rows(sources: list[dict[str, str]]) -> list[dict[str, str]]:
    route_rows = read_csv(ROUTE_CLASSIFICATION_PATH)
    zero_rows = read_csv(DERIVED_ZERO_TARGETS_PATH)
    numeric_rows = read_csv(NUMERIC_INPUT_TEMPLATE_PATH)
    minimum_rows = read_csv(MINIMUM_VECTOR_PATH)

    missing_sources = [row for row in sources if row["exists"] != "True"]
    failed_radial_claims = [row for row in RADIAL_THEOREM_ROWS if row["valid_for_claim"] == "true"]
    failed_cal_claims = [row for row in CALIBRATION_LOCK_ROWS if row["valid_for_claim"] == "true"]
    failed_numeric_claims = [row for row in NUMERIC_TEMPLATE_ROWS if row["valid_for_claim"] == "true"]
    gate_failures_hidden = [
        row for row in COUPLING_GATE_ROWS if row["current_result"] == "pass" and row["claim_effect"].endswith("claim-zero")
    ]
    radial_routes = {row.get("p8_channel", "") for row in route_rows if row.get("p8_channel") in {"radial_Meff_hair", "absolute_calibration_offset"}}
    zero_targets = {row.get("p8_channel", "") for row in zero_rows if row.get("p8_channel") in {"radial_Meff_hair", "absolute_calibration_offset"}}
    numeric_targets = {row.get("p8_channel", "") for row in numeric_rows if row.get("p8_channel") in {"radial_Meff_hair", "absolute_calibration_offset"}}
    minimum_targets = {row.get("p8_channel", "") for row in minimum_rows if row.get("p8_channel") in {"radial_Meff_hair", "absolute_calibration_offset"}}

    return [
        {
            "rule_id": "V498_0_sources",
            "rule": "all cited source paths exist",
            "result": "pass" if not missing_sources else "fail",
            "evidence": f"missing_sources={len(missing_sources)}",
            "claim_effect": "traceability only",
        },
        {
            "rule_id": "V498_1_prior_router_loaded",
            "rule": "497 router and 496 minimum rows expose radial and calibration channels",
            "result": "pass"
            if radial_routes == {"radial_Meff_hair", "absolute_calibration_offset"}
            and zero_targets == {"radial_Meff_hair", "absolute_calibration_offset"}
            and numeric_targets == {"radial_Meff_hair", "absolute_calibration_offset"}
            and minimum_targets == {"radial_Meff_hair", "absolute_calibration_offset"}
            else "fail",
            "evidence": f"routes={';'.join(sorted(radial_routes))};zero={';'.join(sorted(zero_targets))};numeric={';'.join(sorted(numeric_targets))};minimum={';'.join(sorted(minimum_targets))}",
            "claim_effect": "ties 498 to 497 and 496",
        },
        {
            "rule_id": "V498_2_radial_identity_written",
            "rule": "radial theorem attempt contains flux-difference, zero-law, bound-law, and no-leakage rows",
            "result": "pass"
            if {"R498_radial_2_flux_difference", "R498_radial_3_zero_law", "R498_radial_4_bound_law", "R498_radial_5_no_leakage"}.issubset(
                {row["row_id"] for row in RADIAL_THEOREM_ROWS}
            )
            else "fail",
            "evidence": f"radial_rows={len(RADIAL_THEOREM_ROWS)}",
            "claim_effect": "theorem attempt is concrete",
        },
        {
            "rule_id": "V498_3_calibration_contract_written",
            "rule": "calibration lock has same-frame, flux-mass, kappa, range, species, and lambda0 gates",
            "result": "pass" if len(CALIBRATION_LOCK_ROWS) == 6 else "fail",
            "evidence": f"calibration_rows={len(CALIBRATION_LOCK_ROWS)}",
            "claim_effect": "calibration debt explicit",
        },
        {
            "rule_id": "V498_4_numeric_fallback_written",
            "rule": "numeric fallback templates exist for radial current, radial profile, calibration owner, and derivative hair",
            "result": "pass" if len(NUMERIC_TEMPLATE_ROWS) == 4 else "fail",
            "evidence": f"numeric_template_rows={len(NUMERIC_TEMPLATE_ROWS)}",
            "claim_effect": "test branch ready but unfilled",
        },
        {
            "rule_id": "V498_5_no_false_claims",
            "rule": "no theorem or numeric row is claim-valid while parent source identity and calibration lock are open",
            "result": "pass" if not failed_radial_claims and not failed_cal_claims and not failed_numeric_claims and not gate_failures_hidden else "fail",
            "evidence": f"radial_claim_rows={len(failed_radial_claims)};cal_claim_rows={len(failed_cal_claims)};numeric_claim_rows={len(failed_numeric_claims)};hidden_gate_rows={len(gate_failures_hidden)}",
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
    return f"""# 498 - Source Normalization Radial And Calibration Theorem Attempt

Private source-normalization checkpoint. This is not a public mu_extra-zero proof, Newtonian-limit proof, R11 pass, PPN pass, local-GR derivation, cosmology result, EM result, or unified-field claim.

## 1. Purpose

Checkpoint `497` selected the first serious source-normalization derivation target:

```text
radial M_eff conservation plus parent-fixed absolute calibration.
```

This checkpoint tries the theorem rather than hiding the problem inside measured `GM`.

Short answer:

```text
The radial residual identity is sharp:
epsilon_radial_Meff is the normalized exterior integral of d(Pi_M J).

So closed Pi_M flux would kill radial source hair.

But the parent source identity, no-leakage theorem, and absolute calibration lock are not derived.
Therefore epsilon_radial_Meff and epsilon_calibration remain non-claim rows.
```

## 2. Run Manifest

| Item | Value |
| --- | --- |
| Script | `scripts/source_normalization_radial_and_calibration_theorem_attempt.py` |
| Run directory | `{run_dir.relative_to(ROOT)}` |
| Timestamp | `{timestamp}` |
| Generated UTC | `{generated_at_utc}` |
| Status | `{STATUS}` |
| Claim ceiling | `{CLAIM_CEILING}` |
| Next target | `{NEXT_TARGET}` |

## 3. Source Register

{markdown_table(sources)}

## 4. Theorem Attempt

The compact exterior branch gives the exact identity:

```text
M_eff(r) := c_M int_{{S2_r}} Pi_M J

M_eff(r2) - M_eff(r1)
  = c_M int_{{S2 x [r1,r2]}} d(Pi_M J)

epsilon_radial_Meff(r1,r2)
  = [c_M / M_eff(r1)] int_{{S2 x [r1,r2]}} d(Pi_M J).
```

Therefore:

```text
d(Pi_M J)=0  =>  epsilon_radial_Meff=0.
```

That is a real local-Newton route, but only if the parent action proves the source identity and proves that boundary/domain/bulk/non-EH channels do not leak into the absolute mass flux.

{markdown_table(RADIAL_THEOREM_ROWS)}

## 5. Calibration Lock Attempt

Radial constancy is not enough. Source-normalized Newton also needs:

```text
mu_obs = G_parent M_EH
```

in the same observed frame, with the flux charge equal to the Hilbert/source mass and with no radial, time, range, or species derivative hair.

{markdown_table(CALIBRATION_LOCK_ROWS)}

## 6. Coupling Gates

{markdown_table(COUPLING_GATE_ROWS)}

## 7. Numeric Fallback Template

If the parent source identity does not land, the fallback is not prose. The needed objects are:

{markdown_table(NUMERIC_TEMPLATE_ROWS)}

## 8. Validation

{markdown_table(validations)}

## 9. Decision

{markdown_table(DECISION_ROWS)}

## 10. Route Update

{markdown_table(ROUTE_UPDATE_ROWS)}

## 11. Claim Ceiling

Allowed:

```text
The radial source-normalization problem has been reduced to a precise Pi_M source-current identity.
Closed absolute mass flux would kill radial M_eff hair.
Absolute calibration requires a separate parent-fixed same-frame lock.
```

Forbidden:

```text
MTS has derived mu_extra=0.
MTS has proved source-normalized Newtonian recovery.
MTS has absorbed source-normalization into measured GM.
MTS has passed R11, PPN, or local GR.
```

## 12. Next Queue

| Priority | Target | Reason |
| --- | --- | --- |
| 1 | `{NEXT_TARGET}` | this is now the exact missing theorem: derive d(Pi_M J)=0 plus no leakage from the parent action, or fill the radial template |
| 2 | parent-fixed calibration lock | prove c_M int Pi_M J = M_EH and constant universal kappa in the same frame |
| 3 | R10 alpha(lambda) curve | finite-range source-normalization remains numeric-template-first if no mass-gap theorem lands |
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S"))
    args = parser.parse_args()

    generated_at_utc = datetime.now(timezone.utc).isoformat()
    run_dir = ROOT / "runs" / f"{args.timestamp}-source-normalization-radial-and-calibration-theorem-attempt"
    results_dir = run_dir / "results"
    results_dir.mkdir(parents=True, exist_ok=True)

    sources = source_rows()
    validations = validation_rows(sources)

    csv_outputs: list[tuple[Path, list[dict[str, Any]]]] = [
        (SOURCE_REGISTER_PATH, sources),
        (RADIAL_THEOREM_PATH, RADIAL_THEOREM_ROWS),
        (CALIBRATION_LOCK_PATH, CALIBRATION_LOCK_ROWS),
        (COUPLING_GATES_PATH, COUPLING_GATE_ROWS),
        (NUMERIC_TEMPLATE_PATH, NUMERIC_TEMPLATE_ROWS),
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
        "radial_theorem_attempt": str(ROOT / RADIAL_THEOREM_PATH),
        "calibration_lock_attempt": str(ROOT / CALIBRATION_LOCK_PATH),
        "coupling_gates": str(ROOT / COUPLING_GATES_PATH),
        "numeric_template": str(ROOT / NUMERIC_TEMPLATE_PATH),
        "validation": str(ROOT / VALIDATION_PATH),
        "decision": str(ROOT / DECISION_PATH),
        "route_update": str(ROOT / ROUTE_UPDATE_PATH),
        "source_rows": len(sources),
        "source_paths_missing": len(missing_sources),
        "missing_sources": missing_sources,
        "radial_theorem_rows": len(RADIAL_THEOREM_ROWS),
        "calibration_lock_rows": len(CALIBRATION_LOCK_ROWS),
        "coupling_gate_rows": len(COUPLING_GATE_ROWS),
        "numeric_template_rows": len(NUMERIC_TEMPLATE_ROWS),
        "failed_validation_rows": len(failed_validations),
        "radial_residual_identity_written": True,
        "closed_PiM_flux_parent_derived": False,
        "no_leakage_parent_derived": False,
        "absolute_calibration_parent_fixed": False,
        "epsilon_radial_Meff_zero_derived": False,
        "epsilon_calibration_zero_derived": False,
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
