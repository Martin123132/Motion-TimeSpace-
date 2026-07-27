from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path


STATUS = "Y5_R10_cmu_radial_calibration_identity_derived_zero_not_parent_signed_numeric_envelope_unfilled_nonclaim"
CLAIM_CEILING = "radial_calibration_identity_and_template_only_no_cmu_zero_no_Newton_no_PPN_no_R10_no_R11_no_local_GR_claim"
NEXT_TARGET = "659-Y5-R10-parent-source-identity-for-closed-PiM-flux-or-radial-profile-fill.md"

ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
DOC_PATH = ROOT / "658-Y5-R10-cmu-radial-calibration-zero-or-numeric-envelope.md"

FORMALIZATION_WORKBENCH = ROOT.parent / "formalization-workbench"
FORMALIZATION_CUTOFF = datetime.fromisoformat("2026-05-31T14:42:00")

SOURCE_PATHS = {
    "657_doc": ROOT / "657-Y5-R10-source-normalization-family-first-real-R11-fill.md",
    "657_validation": RESIDUALS / "P8_Y5_BRR545_657_VALIDATION.csv",
    "657_cmu_fill": RESIDUALS / "P8_Y5_R10_657_CMU_SOURCE_NORMALIZATION_FILL.csv",
    "657_channel_vector": RESIDUALS / "P8_Y5_R10_657_CMU_EIGHT_CHANNEL_VECTOR.csv",
    "657_weak_map": RESIDUALS / "P8_Y5_R10_657_CMU_WEAK_FIELD_MAP.csv",
    "244_meff_monopole": ROOT / "244-Meff-monopole-source-normalization-or-radial-memory-hair.md",
    "378_gm_absorption": ROOT / "378-source-normalization-Geff-Meff-GM-absorption-theorem.md",
    "402_parent_pair": ROOT / "402-EH-source-normalization-parent-pair.md",
    "465_derivative_hair_gate": ROOT / "465-constant-GM-derivative-hair-fill-gate.md",
    "466_constant_gm_runner": ROOT / "466-constant-GM-zero-theorem-or-local-residual-runner.md",
    "498_radial_calibration_attempt": ROOT / "498-source-normalization-radial-and-calibration-theorem-attempt.md",
    "499_parent_source_identity": ROOT / "499-parent-source-identity-for-closed-PiM-flux-or-radial-template.md",
    "520_ward_closure": ROOT / "520-Y5-source-current-Ward-closure-or-bound-row.md",
    "521_pim_owner": ROOT / "521-Y5-PiM-projector-owner-or-radial-bound-runner.md",
    "523_gauss_orbital": ROOT / "523-Y5-Gauss-orbital-calibration-or-source-normalization-residual-score.md",
    "454_pim_projector": ROOT / "454-PiM-parent-symplectic-projector-algebra-attempt.md",
    "455_pim_flux_closure": ROOT / "455-PiM-flux-closure-Ward-or-topological-current-attempt.md",
    "458_gauss_calibration": ROOT / "458-Hamiltonian-charge-to-Poisson-Gauss-calibration-gate.md",
    "local_bound_matrix": RESIDUALS / "P8_Y5_R10_639_LOCAL_BOUND_MATRIX.csv",
    "source_zero_targets": RESIDUALS / "P8_SOURCE_NORMALIZATION_DERIVED_ZERO_TARGETS.csv",
    "source_numeric_templates": RESIDUALS / "P8_SOURCE_NORMALIZATION_NUMERIC_INPUT_TEMPLATE.csv",
    "derivative_hair_vector": RESIDUALS / "R11_SOURCE_NORMALIZATION_DERIVATIVE_HAIR_VECTOR.csv",
}


def generated_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def bool_text(value: bool) -> str:
    return "true" if value else "false"


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def source_register_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "exists": bool_text(path.exists()),
            "role": "input_or_prior_contract_for_658_radial_calibration_gate",
            "generated_utc": now,
        }
        for source_id, path in SOURCE_PATHS.items()
    ]


def selected_channel_rows(channel_rows_657: list[dict[str, str]]) -> list[dict[str, str]]:
    wanted = {"radial_Meff_hair", "absolute_calibration_offset"}
    rows = []
    now = generated_utc()
    for row in channel_rows_657:
        if row.get("p8_channel") in wanted:
            copied = dict(row)
            copied["selected_for_658"] = "true"
            copied["658_role"] = (
                "radial_zero_or_profile"
                if row["p8_channel"] == "radial_Meff_hair"
                else "parent_fixed_calibration_or_derivative_envelope"
            )
            copied["generated_utc_658"] = now
            rows.append(copied)
    return rows


def radial_identity_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "radial_id": "RAD658_0_annulus",
            "object": "compact_exterior_annulus",
            "formula_or_condition": "A_ext=S^2 x [r1,r2] with ordinary matter support absent in the open annulus",
            "derived_status": "conditional_geometry_available",
            "parent_signed": "conditional",
            "if_passes": "Stokes/Gauss comparison can be made between two exterior spheres",
            "if_fails": "radial source hair cannot be separated from ordinary source support",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "radial_id": "RAD658_1_projected_mass_flux",
            "object": "M_eff(r)",
            "formula_or_condition": "M_eff(r)=c_M integral_{S^2_r} Pi_M J",
            "derived_status": "definition_imported_from_244_498",
            "parent_signed": "definition_only",
            "if_passes": "radial residual has a precise measured-source object",
            "if_fails": "epsilon_radial_Meff remains an undefined closure coefficient",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "radial_id": "RAD658_2_exact_difference",
            "object": "Delta_Meff",
            "formula_or_condition": "M_eff(r2)-M_eff(r1)=c_M integral_{A_ext} d(Pi_M J)",
            "derived_status": "exact_identity_conditional_on_projector_and_annulus",
            "parent_signed": "identity_not_zero",
            "if_passes": "radial source hair is exactly the projected-current nonclosure",
            "if_fails": "radial profile must be supplied numerically",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "radial_id": "RAD658_3_normalized_residual",
            "object": "epsilon_radial_Meff(r1,r2)",
            "formula_or_condition": "epsilon_radial_Meff=[c_M/M_eff(r1)] integral_{A_ext} d(Pi_M J)",
            "derived_status": "exact_residual_law_written",
            "parent_signed": "identity_not_zero",
            "if_passes": "sets the exact radial profile input for R4/R10/R11",
            "if_fails": "no score without source-current norm/profile",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "radial_id": "RAD658_4_zero_condition",
            "object": "radial_zero",
            "formula_or_condition": "d(Pi_M J)=0 and no boundary/domain/bulk/nonEH leakage into Pi_M J in A_ext => epsilon_radial_Meff=0",
            "derived_status": "zero_condition_identified_not_parent_signed",
            "parent_signed": "false",
            "if_passes": "radial_Meff_hair channel clears as theorem-zero",
            "if_fails": "carry radial profile or conservative envelope",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def calibration_lock_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "calibration_id": "CAL658_0_same_frame_source",
            "requirement": "same observed source frame",
            "formula_or_condition": "the stress/source defining Pi_M J is the same source read by slow matter, clocks, and orbital readout",
            "current_status": "closure_visible_but_not_parent_source_calibration",
            "parent_signed": "false",
            "failure_mode": "frame/source split hides a measured-GM offset",
            "claim_effect": "absolute calibration remains retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "calibration_id": "CAL658_1_flux_mass_equality",
            "requirement": "projected flux equals Hilbert/source mass",
            "formula_or_condition": "c_M integral_{S^2} Pi_M J = M_H in the compact local branch",
            "current_status": "not_derived",
            "parent_signed": "false",
            "failure_mode": "lambda0 or epsilon_calibration can remain as a constant offset",
            "claim_effect": "Newton measured-GM normalization not derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "calibration_id": "CAL658_2_parent_fixed_constant",
            "requirement": "calibration constant is parent-fixed",
            "formula_or_condition": "epsilon_calibration=lambda0-1 with lambda0 fixed by parent units, not fitted by local data",
            "current_status": "conditional_harmless_not_parent_fixed",
            "parent_signed": "false",
            "failure_mode": "fitted offset is closure, not derivation",
            "claim_effect": "cannot promote source-normalized Newton",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "calibration_id": "CAL658_3_derivative_silence",
            "requirement": "no derivative hair in calibration",
            "formula_or_condition": "D_r lambda0=D_t lambda0=D_A lambda0=D_lambda lambda0=0",
            "current_status": "not_parent_derived",
            "parent_signed": "false",
            "failure_mode": "derivative hair maps to R1/R4/R9/R10/R11",
            "claim_effect": "must use residual envelope if not proved",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "calibration_id": "CAL658_4_harmless_constant_rule",
            "requirement": "constant offset is harmless only as universal calibration",
            "formula_or_condition": "epsilon_calibration can be absorbed only when parent-fixed, universal, and derivative-free",
            "current_status": "policy_written_not_satisfied",
            "parent_signed": "false",
            "failure_mode": "calibration absorption cheat",
            "claim_effect": "constant offset can be labeled closure but not derivation",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def numeric_envelope_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "envelope_id": "ENV658_0_radial_profile",
            "channel": "radial_Meff_hair",
            "coefficient_symbol": "epsilon_radial_Meff",
            "envelope_formula": "E_rad(r1,r2)=abs([c_M/M_eff(r1)] integral_{A_ext} d(Pi_M J))",
            "required_columns": "r1;r2;epsilon_radial_Meff;dln_mu_dr;units;c_M;M_eff;source_current_norm;source_file;assumptions",
            "maps_to_rows": "R4;R10;R11",
            "acceptance_gate": "derived zero or mapped radial profile below beta/R10/R11 locks",
            "current_input_status": "MISSING_RADIAL_PROFILE_OR_PARENT_SOURCE_IDENTITY",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "envelope_id": "ENV658_1_calibration_derivatives",
            "channel": "absolute_calibration_offset",
            "coefficient_symbol": "epsilon_calibration",
            "envelope_formula": "E_cal=abs(D_r lambda0)L_r + abs(D_t lambda0)T + abs(D_A lambda0) + abs(D_lambda lambda0)Delta_lambda",
            "required_columns": "lambda0;D_r_lambda0;D_t_lambda0;D_A_lambda0;D_lambda_lambda0;universality_certificate;units;source_file;assumptions",
            "maps_to_rows": "R1;R4;R9;R10;R11",
            "acceptance_gate": "parent-fixed universal derivative-free calibration or derivative envelope below mapped row locks",
            "current_input_status": "MISSING_PARENT_FIXED_CALIBRATION_OR_DERIVATIVE_ENVELOPE",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "envelope_id": "ENV658_2_pair_no_cancellation",
            "channel": "radial_plus_calibration_pair",
            "coefficient_symbol": "E_radcal",
            "envelope_formula": "E_radcal=E_rad+E_cal with no tuned sign cancellation between radial and calibration channels",
            "required_columns": "E_rad;E_cal;component_status;source_file;no_cancellation_policy",
            "maps_to_rows": "R1;R4;R9;R10;R11",
            "acceptance_gate": "each component theorem-zero or individually bounded; pair sum is diagnostic only",
            "current_input_status": "MISSING_COMPONENT_EVIDENCE",
            "score_ready": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def scoreability_gate_rows(
    radial_rows: list[dict[str, str]],
    calibration_rows: list[dict[str, str]],
    envelope_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    radial_unsigned = [row for row in radial_rows if row["parent_signed"] == "false"]
    calibration_unsigned = [row for row in calibration_rows if row["parent_signed"] == "false"]
    return [
        {
            "gate_id": "G658_0_radial_identity",
            "gate": "exact radial residual identity is written",
            "result": "pass_identity",
            "detail": "epsilon_radial_Meff=[c_M/M_eff(r1)] integral_A d(Pi_M J)",
            "claim_effect": "identity only; not zero without parent current closure",
            "generated_utc": now,
        },
        {
            "gate_id": "G658_1_radial_zero",
            "gate": "parent proves d(Pi_M J)=0 plus no leakage",
            "result": "blocked",
            "detail": f"unsigned_radial_zero_clauses={len(radial_unsigned)}",
            "claim_effect": "radial_Meff_hair remains retained",
            "generated_utc": now,
        },
        {
            "gate_id": "G658_2_calibration_lock",
            "gate": "parent-fixed universal derivative-free calibration",
            "result": "blocked",
            "detail": f"unsigned_calibration_clauses={len(calibration_unsigned)}",
            "claim_effect": "absolute_calibration_offset remains retained",
            "generated_utc": now,
        },
        {
            "gate_id": "G658_3_numeric_envelope",
            "gate": "radial/calibration numeric envelope has sourced component values",
            "result": "blocked",
            "detail": f"envelope_rows={len(envelope_rows)}; all current_input_status values are MISSING_*",
            "claim_effect": "cannot score R1/R4/R9/R10/R11",
            "generated_utc": now,
        },
        {
            "gate_id": "G658_4_no_absorption_cheat",
            "gate": "constant calibration is not promoted unless parent-fixed and derivative-free",
            "result": "pass_policy",
            "detail": "fitted lambda0 or single-radius calibration is closure, not derivation",
            "claim_effect": "protects Newton/local-GR gate",
            "generated_utc": now,
        },
        {
            "gate_id": "G658_5_claim_guard",
            "gate": "no row is score-ready or claim-valid",
            "result": "pass",
            "detail": "score_ready_true=0; valid_for_claim_true=0",
            "claim_effect": CLAIM_CEILING,
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = generated_utc()
    return [
        {
            "decision_id": "D658_0_radial_identity",
            "status": "exact_identity_written",
            "meaning": "radial source hair is exactly the exterior nonclosure of the projected mass current",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
        {
            "decision_id": "D658_1_radial_zero",
            "status": "not_parent_signed",
            "meaning": "epsilon_radial_Meff=0 requires parent source identity, Pi_M ownership, and no leakage into the absolute mass flux",
            "claim_status": "false",
            "next_action": "try parent source identity for closed Pi_M flux",
            "generated_utc": now,
        },
        {
            "decision_id": "D658_2_calibration",
            "status": "not_parent_fixed",
            "meaning": "epsilon_calibration can be harmless only as parent-fixed universal derivative-free calibration, not as a fitted offset",
            "claim_status": "false",
            "next_action": "derive parent-fixed calibration or retain derivative envelope",
            "generated_utc": now,
        },
        {
            "decision_id": "D658_3_numeric_fallback",
            "status": "template_written_unfilled",
            "meaning": "if zero proof fails, radial/calibration channels need sourced numeric profiles with no cancellation credit",
            "claim_status": "false",
            "next_action": NEXT_TARGET,
            "generated_utc": now,
        },
    ]


def formalization_changed_count() -> int:
    if not FORMALIZATION_WORKBENCH.exists():
        return -1
    count = 0
    for path in FORMALIZATION_WORKBENCH.rglob("*"):
        if path.is_file():
            mtime = datetime.fromtimestamp(path.stat().st_mtime)
            if mtime > FORMALIZATION_CUTOFF:
                count += 1
    return count


def validation_rows(
    source_rows: list[dict[str, str]],
    prior_validation_657: list[dict[str, str]],
    selected_rows: list[dict[str, str]],
    radial_rows: list[dict[str, str]],
    calibration_rows: list[dict[str, str]],
    envelope_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = generated_utc()
    missing_sources = [row["source_id"] for row in source_rows if row["exists"] != "true"]
    prior_failures = [row for row in prior_validation_657 if row.get("result") != "pass"]
    selected_channels = {row["p8_channel"] for row in selected_rows}
    claim_rows = []
    for group in (selected_rows, radial_rows, calibration_rows, envelope_rows, gate_rows, decision):
        claim_rows.extend(
            [row for row in group if row.get("valid_for_claim") == "true" or row.get("claim_status") == "true"]
        )
    generic_fill_markers = []
    for group in (selected_rows, radial_rows, calibration_rows, envelope_rows, gate_rows, decision):
        for row in group:
            for value in row.values():
                if isinstance(value, str) and "fill_" in value.lower():
                    generic_fill_markers.append(value)
    blocked_gates = [row for row in gate_rows if row["result"] == "blocked"]
    formalization_changed = formalization_changed_count()
    checks = [
        (
            "V658_0_source_paths_exist",
            not missing_sources,
            "all cited local source paths exist" if not missing_sources else f"missing={';'.join(missing_sources)}",
        ),
        (
            "V658_1_prior_657_validation_clean",
            not prior_failures,
            "657 validation remains clean" if not prior_failures else f"657_failures={len(prior_failures)}",
        ),
        (
            "V658_2_selected_channels_loaded",
            selected_channels == {"radial_Meff_hair", "absolute_calibration_offset"},
            f"selected_channels={';'.join(sorted(selected_channels))}",
        ),
        (
            "V658_3_radial_identity_written",
            any("d(Pi_M J)" in row["formula_or_condition"] for row in radial_rows),
            "radial identity uses projected-current nonclosure",
        ),
        (
            "V658_4_radial_zero_not_parent_signed",
            any(row["radial_id"] == "RAD658_4_zero_condition" and row["parent_signed"] == "false" for row in radial_rows),
            "radial zero condition remains unsigned",
        ),
        (
            "V658_5_calibration_derivative_lock_written",
            any("D_r lambda0" in row["formula_or_condition"] for row in calibration_rows),
            "calibration derivative silence condition written",
        ),
        (
            "V658_6_calibration_not_parent_fixed",
            any(row["calibration_id"] == "CAL658_2_parent_fixed_constant" and row["parent_signed"] == "false" for row in calibration_rows),
            "parent-fixed calibration remains unsigned",
        ),
        (
            "V658_7_numeric_envelope_unfilled",
            len(envelope_rows) == 3 and all(row["current_input_status"].startswith("MISSING_") for row in envelope_rows),
            f"envelope_rows={len(envelope_rows)}",
        ),
        (
            "V658_8_scoreability_blocked",
            len(blocked_gates) >= 3,
            f"blocked_gates={len(blocked_gates)}",
        ),
        (
            "V658_9_no_claim_rows",
            not claim_rows,
            f"claim_rows={len(claim_rows)}",
        ),
        (
            "V658_10_no_generic_fill_placeholders",
            not generic_fill_markers,
            f"fill_markers={len(generic_fill_markers)}",
        ),
        (
            "V658_11_next_target_selected",
            NEXT_TARGET.startswith("659-") and "PiM-flux" in NEXT_TARGET,
            NEXT_TARGET,
        ),
        (
            "V658_12_claim_ceiling_active",
            CLAIM_CEILING.startswith("radial_calibration_identity"),
            CLAIM_CEILING,
        ),
        (
            "V658_13_formalization_workbench_untouched",
            formalization_changed == 0,
            f"formalization_changed_after_cutoff={formalization_changed}",
        ),
    ]
    return [
        {
            "check_id": check_id,
            "result": "pass" if passed else "fail",
            "detail": detail,
            "generated_utc": now,
        }
        for check_id, passed, detail in checks
    ]


def nonclaim_summary_rows(
    radial_rows: list[dict[str, str]],
    calibration_rows: list[dict[str, str]],
    envelope_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> list[dict[str, str]]:
    return [
        {
            "status": STATUS,
            "claim_ceiling": CLAIM_CEILING,
            "radial_rows": len(radial_rows),
            "calibration_rows": len(calibration_rows),
            "envelope_rows": len(envelope_rows),
            "blocked_scoreability_gates": sum(1 for row in gate_rows if row["result"] == "blocked"),
            "validation_failures": sum(1 for row in validation if row["result"] != "pass"),
            "next_target": NEXT_TARGET,
            "generated_utc": generated_utc(),
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str], limit: int | None = None) -> str:
    visible_rows = rows if limit is None else rows[:limit]
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = [
        "| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |"
        for row in visible_rows
    ]
    if limit is not None and len(rows) > limit:
        body.append("| " + " | ".join(["..."] * len(columns)) + " |")
    return "\n".join([header, separator, *body])


def write_document(
    source_rows: list[dict[str, str]],
    selected_rows: list[dict[str, str]],
    radial_rows: list[dict[str, str]],
    calibration_rows: list[dict[str, str]],
    envelope_rows: list[dict[str, str]],
    gate_rows: list[dict[str, str]],
    decision: list[dict[str, str]],
    summary_rows: list[dict[str, str]],
    validation: list[dict[str, str]],
) -> None:
    doc = f"""# 658 Y5/R10: c_mu Radial-Calibration Zero Or Numeric Envelope

## Verdict

Status: `{STATUS}`.

This checkpoint derives the exact radial residual identity for `epsilon_radial_Meff` and writes the parent-fixed calibration lock. It does not prove either one is zero. The radial/calibration pair is now a theorem-or-envelope target, not a closure fog bank.

## Source Register

{markdown_table(source_rows, ["source_id", "exists", "role"], limit=24)}

## Selected 657 Channels

{markdown_table(selected_rows, ["p8_channel", "coefficient_symbol", "theorem_status", "numeric_template", "affected_rows", "selected_for_658", "valid_for_claim"])}

## Radial Identity

{markdown_table(radial_rows, ["radial_id", "object", "formula_or_condition", "derived_status", "parent_signed", "valid_for_claim"])}

## Calibration Lock

{markdown_table(calibration_rows, ["calibration_id", "requirement", "formula_or_condition", "current_status", "parent_signed", "claim_effect", "valid_for_claim"])}

## Numeric Envelope

{markdown_table(envelope_rows, ["envelope_id", "channel", "coefficient_symbol", "envelope_formula", "current_input_status", "score_ready", "valid_for_claim"])}

## Scoreability Gates

{markdown_table(gate_rows, ["gate_id", "gate", "result", "claim_effect"])}

## Decision

{markdown_table(decision, ["decision_id", "status", "meaning", "claim_status", "next_action"])}

## Nonclaim Summary

{markdown_table(summary_rows, ["status", "claim_ceiling", "radial_rows", "calibration_rows", "envelope_rows", "blocked_scoreability_gates", "next_target"])}

## Validation

{markdown_table(validation, ["check_id", "result", "detail"])}

## Interpretation

This is the cleanest local-source equation we have for this subproblem:

`epsilon_radial_Meff(r1,r2) = [c_M/M_eff(r1)] integral_A d(Pi_M J)`.

So the next derivation target is not vague: prove the parent source identity that closes the projected mass flux, including Pi_M ownership and no leakage from boundary/domain/bulk/non-EH channels. Calibration is the companion lock: a constant offset is only harmless if the parent fixes it universally and all derivatives vanish.

## Next Target

`{NEXT_TARGET}`
"""
    DOC_PATH.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    prior_validation_657 = read_csv(SOURCE_PATHS["657_validation"])
    channel_rows_657 = read_csv(SOURCE_PATHS["657_channel_vector"])

    selected_rows = selected_channel_rows(channel_rows_657)
    radial_rows = radial_identity_rows()
    calibration_rows = calibration_lock_rows()
    envelope_rows = numeric_envelope_rows()
    gate_rows = scoreability_gate_rows(radial_rows, calibration_rows, envelope_rows)
    decision = decision_rows()
    validation = validation_rows(
        source_rows,
        prior_validation_657,
        selected_rows,
        radial_rows,
        calibration_rows,
        envelope_rows,
        gate_rows,
        decision,
    )
    summary_rows = nonclaim_summary_rows(radial_rows, calibration_rows, envelope_rows, gate_rows, validation)

    write_csv(
        RESIDUALS / "P8_Y5_R10_658_SOURCE_REGISTER.csv",
        source_rows,
        ["source_id", "source_path", "exists", "role", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_658_SELECTED_CHANNELS.csv",
        selected_rows,
        [
            "channel_id",
            "p8_channel",
            "coefficient_symbol",
            "coefficient_value_or_theorem",
            "coefficient_units",
            "normalization",
            "operator_form",
            "weak_field_map",
            "affected_rows",
            "induced_observable",
            "primary_route",
            "fallback_route",
            "theorem_target",
            "theorem_status",
            "numeric_template",
            "required_numeric_columns",
            "bound_or_gate",
            "current_status",
            "score_ready",
            "valid_for_claim",
            "claim_blocker",
            "generated_utc",
            "selected_for_658",
            "658_role",
            "generated_utc_658",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_658_RADIAL_IDENTITY.csv",
        radial_rows,
        [
            "radial_id",
            "object",
            "formula_or_condition",
            "derived_status",
            "parent_signed",
            "if_passes",
            "if_fails",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_658_CALIBRATION_LOCK.csv",
        calibration_rows,
        [
            "calibration_id",
            "requirement",
            "formula_or_condition",
            "current_status",
            "parent_signed",
            "failure_mode",
            "claim_effect",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_658_NUMERIC_ENVELOPE_TEMPLATE.csv",
        envelope_rows,
        [
            "envelope_id",
            "channel",
            "coefficient_symbol",
            "envelope_formula",
            "required_columns",
            "maps_to_rows",
            "acceptance_gate",
            "current_input_status",
            "score_ready",
            "valid_for_claim",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_658_SCOREABILITY_GATES.csv",
        gate_rows,
        ["gate_id", "gate", "result", "detail", "claim_effect", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_658_DECISION.csv",
        decision,
        ["decision_id", "status", "meaning", "claim_status", "next_action", "generated_utc"],
    )
    write_csv(
        RESIDUALS / "P8_Y5_R10_658_NONCLAIM_SUMMARY.csv",
        summary_rows,
        [
            "status",
            "claim_ceiling",
            "radial_rows",
            "calibration_rows",
            "envelope_rows",
            "blocked_scoreability_gates",
            "validation_failures",
            "next_target",
            "generated_utc",
        ],
    )
    write_csv(
        RESIDUALS / "P8_Y5_BRR545_658_VALIDATION.csv",
        validation,
        ["check_id", "result", "detail", "generated_utc"],
    )
    write_document(
        source_rows,
        selected_rows,
        radial_rows,
        calibration_rows,
        envelope_rows,
        gate_rows,
        decision,
        summary_rows,
        validation,
    )

    failures = [row for row in validation if row["result"] != "pass"]
    print(f"status={STATUS}")
    print(f"doc={DOC_PATH}")
    print(f"radial_rows={len(radial_rows)}")
    print(f"calibration_rows={len(calibration_rows)}")
    print(f"envelope_rows={len(envelope_rows)}")
    print(f"validation_failures={len(failures)}")
    print(f"next_target={NEXT_TARGET}")
    if failures:
        for failure in failures:
            print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
