from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3148_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3148_LOCAL_PROJECTOR_SURFACE_NULL_THEOREM.csv"
GATES = OUT / "P8_Y5_R2FR_3148_GATE_STATUS.csv"
SCORES = OUT / "P8_Y5_R2FR_3148_SURFACE_NULL_SCORECARD.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3148_PROOF_CONTRACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3148_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3148_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(relative: str) -> str:
    return str((ROOT / relative).resolve())


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def fmt(value: float | None) -> str:
    if value is None:
        return "MISSING_NUMERIC_VALUE"
    return f"{value:.15e}"


def find_row(rows: list[dict[str, str]], column: str, value: str) -> dict[str, str] | None:
    for row in rows:
        if row.get(column) == value:
            return row
    return None


def input_rows() -> list[dict[str, str]]:
    now = stamp()
    rows = [
        {
            "source_id": "SRC3148_0_3147_doc",
            "path": source_path("3147-Y5-R2FR-signed-orthogonality-common-mode-gate-under-AX1090.md"),
            "role": "handoff: prove Pi_local P_surface=0 or K_source=K_cal",
        },
        {
            "source_id": "SRC3148_1_3147_scores",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3147_SIGNED_VS_ABSOLUTE_SCORECARD.csv"),
            "role": "absolute/signed/profile scorecard",
        },
        {
            "source_id": "SRC3148_2_3131_doc",
            "path": source_path("3131-Y5-R2FR-boundary-exactness-common-worldtube-proof-or-rho-surf-retention-under-AX1090.md"),
            "role": "boundary exactness/common-worldtube theorem attempt",
        },
        {
            "source_id": "SRC3148_3_3131_output",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3131_BOUNDARY_EXACTNESS_OUTPUT.csv"),
            "role": "boundary exactness clauses",
        },
        {
            "source_id": "SRC3148_4_3132_doc",
            "path": source_path("3132-Y5-R2FR-parent-action-boundary-primitive-or-rho-surf-allocator-under-AX1090.md"),
            "role": "parent boundary primitive attempt and rho allocator",
        },
        {
            "source_id": "SRC3148_5_3132_output",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3132_PARENT_BOUNDARY_PRIMITIVE_OUTPUT.csv"),
            "role": "weighted-Stokes and boundary primitive clauses",
        },
        {
            "source_id": "SRC3148_6_3134_leakage",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3134_FINITE_LEAKAGE_CARRY_FORWARD.csv"),
            "role": "J_direct/J_spurion leakage blockers",
        },
        {
            "source_id": "SRC3148_7_3146_pairs",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3146_SOURCE_CALIBRATION_KERNEL_PAIR.csv"),
            "role": "Coulomb and surface/profile coefficients",
        },
        {
            "source_id": "SRC3148_8_3129_smoke",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_OUTPUT.csv"),
            "role": "Coulomb channel below-threshold smoke row",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def extracted_values() -> dict[str, float | None]:
    scores = read_csv(OUT / "P8_Y5_R2FR_3147_SIGNED_VS_ABSOLUTE_SCORECARD.csv")
    absolute = find_row(scores, "score_id", "SC3147_0_absolute_fallback")
    signed = find_row(scores, "score_id", "SC3147_1_signed_if_parent_identity")
    profile = find_row(scores, "score_id", "SC3147_2_profile_suppression_target")
    smoke = read_csv(OUT / "P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_OUTPUT.csv")
    coulomb = find_row(smoke, "row_id", "ESC3129_1")
    binding = find_row(smoke, "row_id", "ESC3129_2")
    return {
        "absolute_coeff": parse_float(absolute.get("coefficient_abs")) if absolute else None,
        "absolute_eta": parse_float(absolute.get("eta_abs")) if absolute else None,
        "signed_coeff": parse_float(signed.get("coefficient_abs")) if signed else None,
        "signed_eta": parse_float(signed.get("eta_abs")) if signed else None,
        "threshold_coeff": parse_float(absolute.get("threshold_abs")) if absolute else None,
        "wep_eta_bound": parse_float(absolute.get("eta_bound")) if absolute else None,
        "current_profile_rho": parse_float(profile.get("coefficient_abs")) if profile else None,
        "required_profile_rho": parse_float(profile.get("threshold_abs")) if profile else None,
        "coulomb_coeff": parse_float(coulomb.get("coefficient_value")) if coulomb else None,
        "coulomb_eta": parse_float(coulomb.get("predicted_abs_at_deltaJ_bound")) if coulomb else None,
        "surface_raw_coeff": parse_float(binding.get("coefficient_value")) if binding else None,
        "surface_raw_eta": parse_float(binding.get("predicted_abs_at_deltaJ_bound")) if binding else None,
    }


def theorem_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "theorem_id": "PST3148_0_projector_definition",
            "claim": "The local source-GM projection is the Hilbert/worldtube functional applied to the Frechet EM-stress perturbation.",
            "formula": "Pi_local[P] := (1/M_H,S) Int_W xi_nu P^{mu nu} dSigma_mu with calibration subtraction",
            "proof_status": "definition_from_3145_kernel",
            "effect_if_signed": "surface null can be tested as Pi_local P_surface=0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "PST3148_1_weighted_stokes_annihilator",
            "claim": "If the surface/profile stress is a weighted exact boundary divergence with zero compact boundary flux, the local projector annihilates it.",
            "formula": "P_surface=d_S Lambda, partial W=empty or common-calibrated, xi.Lambda|partial W=0 => Pi_local P_surface=0",
            "proof_status": "exact_conditional_theorem_shape",
            "effect_if_signed": "surface/profile channel drops from the absolute score",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "PST3148_2_common_worldtube_subtraction",
            "claim": "If source and calibration use the same worldtube functional on the surface channel, calibration subtraction kills the surface channel.",
            "formula": "K_surface[S;W]-K_surface[cal;W]=0",
            "proof_status": "exact_conditional_theorem_shape",
            "effect_if_signed": "DeltaK_surface=0 even if raw surface term is nonzero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "PST3148_3_poynting_stationarity_guard",
            "claim": "Static source-GM scoring may ignore the surface channel only if unresolved Poynting/radiative flux is zero, averaged, or separated from ADM mass.",
            "formula": "Int_W div S_EM = flux_partial_W = 0 or separate_dynamic_channel",
            "proof_status": "required_guard_not_signed",
            "effect_if_signed": "prevents radiative flow from masquerading as static boundary exactness",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "PST3148_4_no_spurion_reentry",
            "claim": "Projector silence is invalid if J_direct, J_spurion, readout, or reference counterterms re-enter after the boundary cancellation.",
            "formula": "J_direct=J_spurion=C_readout=C_ref=0 or separately bounded",
            "proof_status": "required_guard_not_signed",
            "effect_if_signed": "surface null theorem becomes stable under parent/source grammar",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "G3148_0_boundary_exactness",
            "gate": "P_surface_is_exact_or_cohomologically_silent",
            "status": "fail_for_claim",
            "evidence": "3131/3132 identify exactness route but do not parent-sign it",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3148_1_same_worldtube",
            "gate": "source_and_calibration_same_worldtube_functional",
            "status": "fail_for_claim",
            "evidence": "3131 same-worldtube calibration remains conditional",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3148_2_poynting_flux",
            "gate": "stationary_no_unresolved_Poynting_flux",
            "status": "fail_for_claim",
            "evidence": "3127/3131 keep Poynting guard active",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3148_3_reference_readout",
            "gate": "no_reference_or_readout_counterterm_reentry",
            "status": "fail_for_claim",
            "evidence": "3132 allocator retains rho_reference_counterterm and rho_projector_readout",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3148_4_spurion_direct",
            "gate": "no_J_direct_or_J_spurion_reentry",
            "status": "fail_for_claim",
            "evidence": "3134 carries J_direct and J_spurion finite leakage heads",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3148_5_surface_null_promotion",
            "gate": "Pi_local_P_surface_zero_claim",
            "status": "not_claim_ready",
            "evidence": "all prior gates must pass before surface channel can be removed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def score_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    threshold = values["threshold_coeff"]
    eta_bound = values["wep_eta_bound"]
    coulomb_coeff = abs(values["coulomb_coeff"]) if values["coulomb_coeff"] is not None else None
    coulomb_eta = values["coulomb_eta"]
    absolute_coeff = values["absolute_coeff"]
    absolute_eta = values["absolute_eta"]
    signed_coeff = values["signed_coeff"]
    signed_eta = values["signed_eta"]
    surface_raw_coeff = abs(values["surface_raw_coeff"]) if values["surface_raw_coeff"] is not None else None
    surface_raw_eta = values["surface_raw_eta"]
    current_rho = values["current_profile_rho"]
    required_rho = values["required_profile_rho"]

    def status(coeff: float | None, eta: float | None, claim: str) -> str:
        if coeff is None or eta is None or threshold is None or eta_bound is None:
            return "not_scoreable_missing_numeric"
        if coeff <= threshold and eta <= eta_bound:
            return claim
        return "above_threshold_pressure"

    return [
        {
            "score_id": "PS3148_0_active_absolute_fallback",
            "scenario": "current_active_absolute_policy",
            "coefficient_abs": fmt(absolute_coeff),
            "threshold_abs": fmt(threshold),
            "eta_abs": fmt(absolute_eta),
            "eta_bound": fmt(eta_bound),
            "score": status(absolute_coeff, absolute_eta, "below_threshold_but_not_expected"),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "ACTIVE_FALLBACK;SURFACE_NULL_NOT_SIGNED",
            "generated_utc": now,
        },
        {
            "score_id": "PS3148_1_if_surface_projector_zero",
            "scenario": "Pi_local_P_surface_zero_then_Coulomb_only",
            "coefficient_abs": fmt(coulomb_coeff),
            "threshold_abs": fmt(threshold),
            "eta_abs": fmt(coulomb_eta),
            "eta_bound": fmt(eta_bound),
            "score": status(coulomb_coeff, coulomb_eta, "would_pass_if_surface_null_signed"),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "SURFACE_NULL_THEOREM_UNSIGNED;COULOMB_ROW_SMOKE",
            "generated_utc": now,
        },
        {
            "score_id": "PS3148_2_if_common_worldtube_all",
            "scenario": "K_source_equals_K_cal_all_channels",
            "coefficient_abs": fmt(0.0),
            "threshold_abs": fmt(threshold),
            "eta_abs": fmt(0.0),
            "eta_bound": fmt(eta_bound),
            "score": "would_pass_if_common_worldtube_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "COMMON_WORLDTUBE_THEOREM_UNSIGNED",
            "generated_utc": now,
        },
        {
            "score_id": "PS3148_3_signed_parent_identity",
            "scenario": "signed_parent_orientation",
            "coefficient_abs": fmt(signed_coeff),
            "threshold_abs": fmt(threshold),
            "eta_abs": fmt(signed_eta),
            "eta_bound": fmt(eta_bound),
            "score": status(signed_coeff, signed_eta, "would_pass_if_parent_orientation_signed"),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "PARENT_ORIENTATION_UNSIGNED",
            "generated_utc": now,
        },
        {
            "score_id": "PS3148_4_raw_surface_hazard",
            "scenario": "raw_surface_binding_without_projector",
            "coefficient_abs": fmt(surface_raw_coeff),
            "threshold_abs": fmt(threshold),
            "eta_abs": fmt(surface_raw_eta),
            "eta_bound": fmt(eta_bound),
            "score": status(surface_raw_coeff, surface_raw_eta, "would_pass_unexpected"),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "RAW_SURFACE_OVER_THRESHOLD;PROJECTOR_OR_PROFILE_REQUIRED",
            "generated_utc": now,
        },
        {
            "score_id": "PS3148_5_profile_target_if_theorem_fails",
            "scenario": "finite_profile_fallback",
            "coefficient_abs": fmt(current_rho),
            "threshold_abs": fmt(required_rho),
            "eta_abs": "rho_ratio=" + fmt(None if current_rho is None or required_rho in (None, 0) else current_rho / required_rho),
            "eta_bound": "not_eta_row",
            "score": "current_profile_above_tightened_target" if current_rho is not None and required_rho is not None and current_rho > required_rho else "profile_below_target_or_missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "PREM_PROFILE_OR_PROJECTOR_THEOREM_REQUIRED",
            "generated_utc": now,
        },
    ]


def contract_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "contract_id": "PC3148_0_surface_exactness",
            "required_clause": "P_surface=d_S Lambda plus zero harmonic/nonexact/corner terms",
            "proof_needed": "derive from parent boundary primitive or absent/nonprimitive quotient variable",
            "failure_fallback": "rho_nonexact, rho_corner, rho_harmonic remain in allocator",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PC3148_1_projector_closedness",
            "required_clause": "Pi_local annihilates exact surface terms on the compact/common-calibrated worldtube",
            "proof_needed": "weighted Stokes with fixed orientation, no reference/readout counterterm and same boundary class",
            "failure_fallback": "rho_kernel_derivative, rho_reference_counterterm, rho_projector_readout remain",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PC3148_2_static_flux",
            "required_clause": "Poynting/radiative flux is zero, averaged, or separated from static ADM/source mass",
            "proof_needed": "stationary source worldtube or explicit dynamic flux channel",
            "failure_fallback": "rho_flux_poynting remains active",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PC3148_3_no_reentry",
            "required_clause": "J_direct, J_spurion, readout and source labels do not re-enter after quotient/projector cancellation",
            "proof_needed": "no-source-slot grammar and matter pullback closure",
            "failure_fallback": "3134 finite leakage heads remain active",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "D3148_0_theorem",
            "decision": "Pi_local P_surface=0 has an exact weighted-Stokes/common-worldtube theorem shape",
            "effect": "if signed, the local source-GM pressure row reduces to the Coulomb-only row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3148_1_claim",
            "decision": "surface-null theorem is not promoted",
            "effect": "absolute no-cancellation pressure row remains the active gate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3148_2_next",
            "decision": "next target should either sign one projector clause or switch to profile acquisition",
            "effect": "3149 should attack Poynting/static flux or weighted-Stokes exactness first; if that fails, import/source PREM profile rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    theorem: list[dict[str, str]],
    gates: list[dict[str, str]],
    scores: list[dict[str, str]],
    contract: list[dict[str, str]],
    decisions: list[dict[str, str]],
    values: dict[str, float | None],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    theorem_cover = {"PST3148_1_weighted_stokes_annihilator", "PST3148_2_common_worldtube_subtraction"}.issubset(
        {row["theorem_id"] for row in theorem}
    )
    gates_block = all(row["claim_allowed"] == "false" for row in gates)
    score_cover = {"PS3148_0_active_absolute_fallback", "PS3148_1_if_surface_projector_zero", "PS3148_2_if_common_worldtube_all", "PS3148_5_profile_target_if_theorem_fails"}.issubset(
        {row["score_id"] for row in scores}
    )
    surface_null_would_pass = any(
        row["score_id"] == "PS3148_1_if_surface_projector_zero"
        and row["score"] == "would_pass_if_surface_null_signed"
        and row["claim_allowed"] == "false"
        for row in scores
    )
    active_pressure_retained = any(
        row["score_id"] == "PS3148_0_active_absolute_fallback"
        and row["score"] == "above_threshold_pressure"
        for row in scores
    )
    contracts_cover = {"PC3148_0_surface_exactness", "PC3148_1_projector_closedness", "PC3148_2_static_flux", "PC3148_3_no_reentry"}.issubset(
        {row["contract_id"] for row in contract}
    )
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decisions)
    numerics = all(value is not None for value in values.values())
    return [
        {
            "check_id": "V3148_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3148_1_theorem_shapes_present",
            "status": "pass" if theorem_cover else "fail",
            "details": json.dumps([row["theorem_id"] for row in theorem], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3148_2_numeric_values_extracted",
            "status": "pass" if numerics else "fail",
            "details": json.dumps({key: fmt(value) for key, value in values.items()}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3148_3_surface_null_would_pass_but_nonclaim",
            "status": "pass" if surface_null_would_pass else "fail",
            "details": "surface projector zero reduces score to Coulomb-only below threshold",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3148_4_active_pressure_retained",
            "status": "pass" if active_pressure_retained else "fail",
            "details": "absolute fallback remains active because gates fail",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3148_5_contract_and_no_claim_leak",
            "status": "pass" if gates_block and score_cover and contracts_cover and decisions_nonclaim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    values = extracted_values()
    theorem = theorem_rows()
    gates = gate_rows()
    scores = score_rows(values)
    contract = contract_rows()
    decisions = decision_rows()
    validations = validation_rows(inputs, theorem, gates, scores, contract, decisions, values)
    write_csv(INPUTS, inputs)
    write_csv(THEOREM, theorem)
    write_csv(GATES, gates)
    write_csv(SCORES, scores)
    write_csv(CONTRACT, contract)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
