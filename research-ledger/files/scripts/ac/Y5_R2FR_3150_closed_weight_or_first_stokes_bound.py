from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3150_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3150_CLOSED_WEIGHT_THEOREM.csv"
GATES = OUT / "P8_Y5_R2FR_3150_CLOSED_WEIGHT_GATES.csv"
BOUNDS = OUT / "P8_Y5_R2FR_3150_FIRST_STOKES_BOUND_TARGETS.csv"
SCORES = OUT / "P8_Y5_R2FR_3150_SCORE_IMPACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3150_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3150_VALIDATION.csv"


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
            "source_id": "SRC3150_0_3149_doc",
            "path": source_path("3149-Y5-R2FR-weighted-Stokes-flux-clause-gate-under-AX1090.md"),
            "role": "handoff selecting closed-weight theorem or first finite bound term",
        },
        {
            "source_id": "SRC3150_1_3149_bounds",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3149_STOKES_FLUX_BOUND_SCHEMA.csv"),
            "role": "derivative and Poynting bound schema",
        },
        {
            "source_id": "SRC3150_2_3149_scores",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3149_SCORE_IMPACT.csv"),
            "role": "active and conditional score rows",
        },
        {
            "source_id": "SRC3150_3_3089_stokes",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3089_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv"),
            "role": "precedent closed-weight theorem and residual bound",
        },
        {
            "source_id": "SRC3150_4_3132_allocator",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3132_RHO_SURF_ALLOCATOR.csv"),
            "role": "rho allocator for derivative and flux components",
        },
        {
            "source_id": "SRC3150_5_3129_smoke",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_OUTPUT.csv"),
            "role": "Coulomb row margin and raw surface coefficient",
        },
        {
            "source_id": "SRC3150_6_3142_poynting",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3142_POYNTING_STRESS_READOUT.csv"),
            "role": "Poynting readout definition",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def extracted_values() -> dict[str, float | None]:
    smoke = read_csv(OUT / "P8_Y5_R2FR_3129_EARTH_SOURCE_CAL_SMOKE_OUTPUT.csv")
    coulomb = find_row(smoke, "row_id", "ESC3129_1")
    surface = find_row(smoke, "row_id", "ESC3129_2")
    scores = read_csv(OUT / "P8_Y5_R2FR_3149_SCORE_IMPACT.csv")
    active = find_row(scores, "score_id", "SI3149_0_current_active")
    conditional = find_row(scores, "score_id", "SI3149_1_if_all_stokes_flux_gates_close")
    threshold = parse_float(active.get("threshold_abs")) if active else None
    eta_bound = parse_float(active.get("eta_bound")) if active else None
    coulomb_coeff = abs(parse_float(coulomb.get("coefficient_value"))) if coulomb else None
    coulomb_eta = parse_float(coulomb.get("predicted_abs_at_deltaJ_bound")) if coulomb else None
    surface_coeff = abs(parse_float(surface.get("coefficient_value"))) if surface else None
    surface_eta = parse_float(surface.get("predicted_abs_at_deltaJ_bound")) if surface else None
    active_coeff = parse_float(active.get("coefficient_abs")) if active else None
    active_eta = parse_float(active.get("eta_abs")) if active else None
    conditional_coeff = parse_float(conditional.get("coefficient_abs")) if conditional else None
    conditional_eta = parse_float(conditional.get("eta_abs")) if conditional else None
    remaining_coeff = None if threshold is None or coulomb_coeff is None else max(0.0, threshold - coulomb_coeff)
    remaining_eta = None if eta_bound is None or coulomb_eta is None else max(0.0, eta_bound - coulomb_eta)
    remaining_rho = None if remaining_coeff is None or surface_coeff in (None, 0) else remaining_coeff / surface_coeff
    equal_split_coeff = None if remaining_coeff is None else remaining_coeff / 6.0
    equal_split_eta = None if remaining_eta is None else remaining_eta / 6.0
    equal_split_rho = None if remaining_rho is None else remaining_rho / 6.0
    return {
        "threshold_coeff": threshold,
        "eta_bound": eta_bound,
        "coulomb_coeff": coulomb_coeff,
        "coulomb_eta": coulomb_eta,
        "surface_coeff": surface_coeff,
        "surface_eta": surface_eta,
        "active_coeff": active_coeff,
        "active_eta": active_eta,
        "conditional_coeff": conditional_coeff,
        "conditional_eta": conditional_eta,
        "remaining_coeff_after_coulomb": remaining_coeff,
        "remaining_eta_after_coulomb": remaining_eta,
        "remaining_rho_after_coulomb": remaining_rho,
        "equal_split_coeff_six_terms": equal_split_coeff,
        "equal_split_eta_six_terms": equal_split_eta,
        "equal_split_rho_six_terms": equal_split_rho,
    }


def theorem_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "theorem_id": "CW3150_0_weight_object",
            "statement": "The weighted-Stokes weight is the local source projector kernel restricted to the boundary class.",
            "formula": "W := W_local|S = q^* Wbar(B_class, lambda, epsilon, xi, mu_obs, reference)",
            "current_status": "definition_shape",
            "effect_if_signed": "closed-weight can be tested as d_S(W)=0 on the certified boundary class",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "CW3150_1_closed_weight_condition",
            "statement": "d_S(W)=0 follows if the boundary class, kernel/range parameter, representative epsilon, observed tetrad, and reference convention are fixed before source/readout variation.",
            "formula": "D_S B_class=D_S lambda=D_S epsilon=D_S xi=D_S reference=0 => d_S(W)=0",
            "current_status": "conditional_theorem_shape",
            "effect_if_signed": "kernel-derivative term ||d_S(W)|| ||Lambda|| is zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "CW3150_2_current_blockers",
            "statement": "The current corpus does not sign all closed-weight hypotheses in the same parent boundary class.",
            "formula": "boundary_class_fixed AND kernel_owner AND reference_silence AND no_readout_reentry are not jointly signed",
            "current_status": "not_claim_ready",
            "effect_if_signed": "would remove one weighted-Stokes blocker but not the other surface-null blockers",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "CW3150_3_bound_fallback",
            "statement": "If closed-weight is unsigned, the first finite term is bounded directly as ||d_S(W)||_* ||Lambda||_*.",
            "formula": "Q_deriv_abs <= ||d_S(W)||_* ||Lambda||_*",
            "current_status": "bound_target_staged_nonclaim",
            "effect_if_signed": "gives a concrete target for derivative leakage instead of retaining fog",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "G3150_0_boundary_class_fixed",
            "gate": "same boundary class B_class fixed before readout",
            "status": "fail_for_claim",
            "reason": "3089/3132 keep boundary/reference class unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3150_1_kernel_owner",
            "gate": "kernel/range/epsilon owner fixed on S",
            "status": "fail_for_claim",
            "reason": "d_S(F epsilon) or d_S(W) closedness is not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3150_2_reference_readout_silence",
            "gate": "reference and readout cannot move W",
            "status": "fail_for_claim",
            "reason": "reference/readout counterterms remain allocator heads",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3150_3_closed_weight",
            "gate": "d_S(W)=0",
            "status": "not_claim_ready",
            "reason": "all closed-weight clauses above must close together",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3150_4_first_bound_target",
            "gate": "derivative and flux bound targets staged",
            "status": "pass_nonclaim",
            "reason": "3150 computes coefficient/eta/rho caps for first finite bound terms",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def bound_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    remaining_coeff = values["remaining_coeff_after_coulomb"]
    remaining_eta = values["remaining_eta_after_coulomb"]
    remaining_rho = values["remaining_rho_after_coulomb"]
    equal_coeff = values["equal_split_coeff_six_terms"]
    equal_eta = values["equal_split_eta_six_terms"]
    equal_rho = values["equal_split_rho_six_terms"]
    return [
        {
            "bound_id": "BT3150_0_total_remaining_after_coulomb",
            "term": "all_unsigned_surface_terms_total",
            "coefficient_cap": fmt(remaining_coeff),
            "eta_cap": fmt(remaining_eta),
            "rho_cap_against_raw_surface": fmt(remaining_rho),
            "formula": "sum_unsigned_abs <= threshold - |DeltaK_Coulomb|",
            "status": "target_cap_nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "BT3150_1_derivative_single_term_cap",
            "term": "norm_dS_W_times_norm_Lambda",
            "coefficient_cap": fmt(remaining_coeff),
            "eta_cap": fmt(remaining_eta),
            "rho_cap_against_raw_surface": fmt(remaining_rho),
            "formula": "||d_S(W)||_* ||Lambda||_* <= remaining_coeff if every sibling term is zero",
            "status": "single_term_cap_nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "BT3150_2_derivative_equal_split_cap",
            "term": "norm_dS_W_times_norm_Lambda",
            "coefficient_cap": fmt(equal_coeff),
            "eta_cap": fmt(equal_eta),
            "rho_cap_against_raw_surface": fmt(equal_rho),
            "formula": "equal diagnostic split across six unsigned Stokes/flux terms",
            "status": "diagnostic_equal_split_nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "BT3150_3_poynting_single_term_cap",
            "term": "poynting_flux_abs",
            "coefficient_cap": fmt(remaining_coeff),
            "eta_cap": fmt(remaining_eta),
            "rho_cap_against_raw_surface": fmt(remaining_rho),
            "formula": "|Int_partialW S_EM dot dA dt|/M_H <= remaining_coeff if every sibling term is zero",
            "status": "single_term_cap_nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "BT3150_4_poynting_equal_split_cap",
            "term": "poynting_flux_abs",
            "coefficient_cap": fmt(equal_coeff),
            "eta_cap": fmt(equal_eta),
            "rho_cap_against_raw_surface": fmt(equal_rho),
            "formula": "equal diagnostic split across six unsigned Stokes/flux terms",
            "status": "diagnostic_equal_split_nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def score_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "score_id": "SC3150_0_active_pressure",
            "scenario": "current_active_absolute_surface_retained",
            "coefficient_abs": fmt(values["active_coeff"]),
            "threshold_abs": fmt(values["threshold_coeff"]),
            "eta_abs": fmt(values["active_eta"]),
            "eta_bound": fmt(values["eta_bound"]),
            "score": "above_threshold_pressure",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "CLOSED_WEIGHT_UNSIGNED;OTHER_SURFACE_TERMS_UNSIGNED",
            "generated_utc": now,
        },
        {
            "score_id": "SC3150_1_if_closed_weight_only",
            "scenario": "kernel_derivative_term_removed_only",
            "coefficient_abs": "not_computed_because_sibling_surface_terms_unfilled",
            "threshold_abs": fmt(values["threshold_coeff"]),
            "eta_abs": "not_computed_because_sibling_surface_terms_unfilled",
            "eta_bound": fmt(values["eta_bound"]),
            "score": "not_enough_for_pass_by_itself",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "corner_harmonic_residual_flux_reference_readout_still_active",
            "generated_utc": now,
        },
        {
            "score_id": "SC3150_2_if_all_surface_terms_zero",
            "scenario": "Coulomb_only_conditional",
            "coefficient_abs": fmt(values["conditional_coeff"]),
            "threshold_abs": fmt(values["threshold_coeff"]),
            "eta_abs": fmt(values["conditional_eta"]),
            "eta_bound": fmt(values["eta_bound"]),
            "score": "would_pass_if_all_surface_terms_zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "CONDITIONAL_ONLY",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "D3150_0_closed_weight",
            "decision": "closed-weight theorem has exact shape but is not signed",
            "effect": "d_S(W)=0 cannot be used to remove derivative term yet",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3150_1_bound_target",
            "decision": "first finite derivative/flux bound targets are now numeric caps",
            "effect": "future bound rows know the required coefficient, eta and rho caps",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3150_2_next",
            "decision": "next target should either sign boundary-class fixedness or fill norm_dS_W/norm_Lambda",
            "effect": "3151 should attack B_class fixed before readout, or produce the first numeric/source-backed derivative bound input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    theorem: list[dict[str, str]],
    gates: list[dict[str, str]],
    bounds: list[dict[str, str]],
    scores: list[dict[str, str]],
    decisions: list[dict[str, str]],
    values: dict[str, float | None],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    theorem_cover = {"CW3150_1_closed_weight_condition", "CW3150_3_bound_fallback"}.issubset(
        {row["theorem_id"] for row in theorem}
    )
    gates_block = all(row["claim_allowed"] == "false" for row in gates)
    bound_cover = {"BT3150_1_derivative_single_term_cap", "BT3150_2_derivative_equal_split_cap", "BT3150_3_poynting_single_term_cap"}.issubset(
        {row["bound_id"] for row in bounds}
    )
    caps_positive = all(
        values[key] is not None and values[key] >= 0
        for key in [
            "remaining_coeff_after_coulomb",
            "remaining_eta_after_coulomb",
            "remaining_rho_after_coulomb",
            "equal_split_coeff_six_terms",
        ]
    )
    active_retained = any(
        row["score_id"] == "SC3150_0_active_pressure" and row["score"] == "above_threshold_pressure"
        for row in scores
    )
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decisions)
    numerics = all(value is not None for value in values.values())
    return [
        {
            "check_id": "V3150_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3150_1_closed_weight_and_bound_shapes",
            "status": "pass" if theorem_cover else "fail",
            "details": json.dumps([row["theorem_id"] for row in theorem], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3150_2_bound_caps_positive",
            "status": "pass" if caps_positive else "fail",
            "details": json.dumps({key: fmt(value) for key, value in values.items() if "remaining" in key or "equal_split" in key}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3150_3_bound_rows_cover_derivative_and_flux",
            "status": "pass" if bound_cover else "fail",
            "details": json.dumps([row["bound_id"] for row in bounds], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3150_4_active_pressure_retained",
            "status": "pass" if active_retained else "fail",
            "details": "closed weight alone is not enough and remains unsigned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3150_5_no_claim_leak",
            "status": "pass" if gates_block and decisions_nonclaim and numerics else "fail",
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
    bounds = bound_rows(values)
    scores = score_rows(values)
    decisions = decision_rows()
    validations = validation_rows(inputs, theorem, gates, bounds, scores, decisions, values)
    write_csv(INPUTS, inputs)
    write_csv(THEOREM, theorem)
    write_csv(GATES, gates)
    write_csv(BOUNDS, bounds)
    write_csv(SCORES, scores)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
