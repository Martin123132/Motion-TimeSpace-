from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3151_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3151_BOUNDARY_CLASS_FIXEDNESS_THEOREM.csv"
GATES = OUT / "P8_Y5_R2FR_3151_GATE_STATUS.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3151_DERIVATIVE_INPUT_CONTRACT.csv"
SCORES = OUT / "P8_Y5_R2FR_3151_SCORE_IMPACT.csv"
FORK_RULES = OUT / "P8_Y5_R2FR_3151_RESEARCH_FORK_RULES.csv"
DECISION = OUT / "P8_Y5_R2FR_3151_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3151_VALIDATION.csv"


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
            "source_id": "SRC3151_0_3150_doc",
            "path": source_path("3150-Y5-R2FR-closed-weight-or-first-Stokes-bound-target-under-AX1090.md"),
            "role": "handoff requiring boundary-class fixedness or derivative input",
        },
        {
            "source_id": "SRC3151_1_3150_bounds",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3150_FIRST_STOKES_BOUND_TARGETS.csv"),
            "role": "numeric derivative and Poynting caps",
        },
        {
            "source_id": "SRC3151_2_3150_gates",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3150_CLOSED_WEIGHT_GATES.csv"),
            "role": "current unsigned closed-weight gate state",
        },
        {
            "source_id": "SRC3151_3_3089_domain",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3089_BOUNDARY_DOMAIN_CERTIFICATE.csv"),
            "role": "boundary class and kernel-weight certificate blockers",
        },
        {
            "source_id": "SRC3151_4_3132_allocator",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3132_RHO_SURF_ALLOCATOR.csv"),
            "role": "surface allocator heads that remain active",
        },
        {
            "source_id": "SRC3151_5_3134_leakage",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3134_FINITE_LEAKAGE_CARRY_FORWARD.csv"),
            "role": "J_direct, J_spurion and readout leakage blockers",
        },
        {
            "source_id": "SRC3151_6_3142_poynting",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3142_POYNTING_STRESS_READOUT.csv"),
            "role": "Poynting flux readout branch that may source a separate finite bound",
        },
        {
            "source_id": "SRC3151_7_3149_scores",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3149_SCORE_IMPACT.csv"),
            "role": "active pressure and Coulomb-only conditional score",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def cap_values() -> dict[str, float | None]:
    bounds = read_csv(OUT / "P8_Y5_R2FR_3150_FIRST_STOKES_BOUND_TARGETS.csv")
    scores = read_csv(OUT / "P8_Y5_R2FR_3150_SCORE_IMPACT.csv")
    derivative_single = find_row(bounds, "bound_id", "BT3150_1_derivative_single_term_cap")
    derivative_equal = find_row(bounds, "bound_id", "BT3150_2_derivative_equal_split_cap")
    poynting_single = find_row(bounds, "bound_id", "BT3150_3_poynting_single_term_cap")
    poynting_equal = find_row(bounds, "bound_id", "BT3150_4_poynting_equal_split_cap")
    active = find_row(scores, "score_id", "SC3150_0_active_pressure")
    conditional = find_row(scores, "score_id", "SC3150_2_if_all_surface_terms_zero")
    return {
        "derivative_single_coeff_cap": parse_float(derivative_single.get("coefficient_cap")) if derivative_single else None,
        "derivative_single_eta_cap": parse_float(derivative_single.get("eta_cap")) if derivative_single else None,
        "derivative_single_rho_cap": parse_float(derivative_single.get("rho_cap_against_raw_surface")) if derivative_single else None,
        "derivative_equal_coeff_cap": parse_float(derivative_equal.get("coefficient_cap")) if derivative_equal else None,
        "derivative_equal_eta_cap": parse_float(derivative_equal.get("eta_cap")) if derivative_equal else None,
        "derivative_equal_rho_cap": parse_float(derivative_equal.get("rho_cap_against_raw_surface")) if derivative_equal else None,
        "poynting_single_coeff_cap": parse_float(poynting_single.get("coefficient_cap")) if poynting_single else None,
        "poynting_equal_coeff_cap": parse_float(poynting_equal.get("coefficient_cap")) if poynting_equal else None,
        "active_coeff": parse_float(active.get("coefficient_abs")) if active else None,
        "active_threshold": parse_float(active.get("threshold_abs")) if active else None,
        "active_eta": parse_float(active.get("eta_abs")) if active else None,
        "active_eta_bound": parse_float(active.get("eta_bound")) if active else None,
        "conditional_coeff": parse_float(conditional.get("coefficient_abs")) if conditional else None,
        "conditional_eta": parse_float(conditional.get("eta_abs")) if conditional else None,
    }


def theorem_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "theorem_id": "BCF3151_0_boundary_class_object",
            "object": "B_class",
            "statement": "The boundary class must be a single parent-owned object, not a readout-time convention.",
            "formula": "B_class := [S, orientation, corner_policy, cohomology_sector, reference_counterterm, readout_convention]",
            "what_it_proves": "defines the object whose fixedness is being tested",
            "current_status": "definition_shape",
            "missing_parent_signature": "parent action has not signed one immutable B_class for source, calibration and readout",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "BCF3151_1_fixedness_before_readout",
            "object": "source/readout drift of W",
            "statement": "If the parent action fixes B_class, reference, readout and kernel data before source variation, then W cannot acquire a source/readout drift term.",
            "formula": "D_source B_class=D_readout B_class=D_reference B_class=D_source(lambda,epsilon,xi)=0 => D_source W|S=0",
            "what_it_proves": "removes source/readout retuning of the weighted-Stokes weight",
            "current_status": "conditional_theorem_shape",
            "missing_parent_signature": "BDC3089_1, BDC3089_4, reference silence and no readout re-entry are not jointly signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "BCF3151_2_source_fixedness_not_surface_closedness",
            "object": "d_S(W)",
            "statement": "Boundary-class fixedness removes source/readout drift, but full surface closedness still needs the kernel/weight to be closed or constant on S.",
            "formula": "D_source W|S=0 does not by itself imply d_S(W)=0; need d_S Wbar(B_class,lambda,epsilon,xi,reference)=0 or a norm bound",
            "what_it_proves": "prevents smuggling d_S(W)=0 from fixed boundary labels alone",
            "current_status": "refinement_required",
            "missing_parent_signature": "kernel closedness on the boundary surface is still unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "BCF3151_3_current_blocker",
            "object": "B_class before readout",
            "statement": "The current corpus does not yet prove that B_class is frozen before readout, nor that J_direct/J_spurion cannot move the readout convention.",
            "formula": "NOT_SIGNED(B_class_fixed AND reference_silent AND readout_no_reentry AND no_spurion_direct)",
            "what_it_proves": "keeps closed-weight branch nonclaim",
            "current_status": "fail_for_claim",
            "missing_parent_signature": "needs parent variation order and quotient/readout map signature",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "BCF3151_4_bound_fallback",
            "object": "first derivative leakage input",
            "statement": "If fixedness and closedness are unsigned, the branch must source norm_dS_W and norm_Lambda or keep the derivative term active.",
            "formula": "|Q_deriv| <= ||d_S(W)||_* ||Lambda||_*",
            "what_it_proves": "turns the missing theorem into a finite input contract",
            "current_status": "bound_contract_staged_nonclaim",
            "missing_parent_signature": "numeric/source-backed norms are not present yet",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "G3151_0_boundary_class_declared",
            "gate": "B_class object explicitly declared",
            "status": "pass_nonclaim",
            "reason": "3151 declares the object but does not promote it to a parent-signed invariant",
            "evidence_source": source_path("3150-Y5-R2FR-closed-weight-or-first-Stokes-bound-target-under-AX1090.md"),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3151_1_parent_fixed_B_class",
            "gate": "parent action fixes B_class before source/readout variation",
            "status": "fail_for_claim",
            "reason": "3089 boundary-domain certificate keeps BDC3089_1 unsigned",
            "evidence_source": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3089_BOUNDARY_DOMAIN_CERTIFICATE.csv"),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3151_2_reference_silent",
            "gate": "reference and counterterm convention cannot change W",
            "status": "fail_for_claim",
            "reason": "reference/counterterm remains an allocator head and has no parent silence proof",
            "evidence_source": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3132_RHO_SURF_ALLOCATOR.csv"),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3151_3_readout_no_reentry",
            "gate": "readout cannot re-enter source projector after boundary class choice",
            "status": "fail_for_claim",
            "reason": "J_direct, J_spurion and C_Obs_e leakage rows remain active",
            "evidence_source": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3134_FINITE_LEAKAGE_CARRY_FORWARD.csv"),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3151_4_kernel_closed_on_S",
            "gate": "kernel/weight is closed or constant on S",
            "status": "not_claim_ready",
            "reason": "fixed boundary labels do not automatically prove d_S(W)=0",
            "evidence_source": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3150_CLOSED_WEIGHT_GATES.csv"),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3151_5_derivative_input_contract_ready",
            "gate": "norm_dS_W and norm_Lambda contract stated with caps",
            "status": "pass_nonclaim",
            "reason": "3150 caps are imported and mapped to source-ready input rows",
            "evidence_source": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3150_FIRST_STOKES_BOUND_TARGETS.csv"),
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def contract_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "contract_id": "DIC3151_0_norm_dS_W",
            "quantity": "norm_dS_W",
            "definition": "dual norm of the surface derivative of the weighted-Stokes source/readout kernel on S",
            "required_units": "1/boundary_length_or_declared_dual_surface_norm",
            "required_source": "parent boundary class plus kernel/range/epsilon definition on the same S",
            "numeric_value": "MISSING_NUMERIC_OR_ZERO_THEOREM",
            "coefficient_cap": "not_applicable_without_norm_Lambda",
            "eta_cap": "not_applicable_without_norm_Lambda",
            "rho_cap_against_raw_surface": "not_applicable_without_norm_Lambda",
            "status": "missing_parent_input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "DIC3151_1_norm_Lambda",
            "quantity": "norm_Lambda",
            "definition": "compatible norm of the boundary primitive Lambda in B_surf=d_S Lambda+h+r",
            "required_units": "coefficient_length_or_declared_primitive_surface_norm",
            "required_source": "parent primitive construction and cohomology/residual split on the same S",
            "numeric_value": "MISSING_NUMERIC_OR_ZERO_THEOREM",
            "coefficient_cap": "not_applicable_without_norm_dS_W",
            "eta_cap": "not_applicable_without_norm_dS_W",
            "rho_cap_against_raw_surface": "not_applicable_without_norm_dS_W",
            "status": "missing_parent_input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "DIC3151_2_product_single_term_cap",
            "quantity": "norm_dS_W_times_norm_Lambda",
            "definition": "single surviving derivative leakage product if every sibling surface/flux term is zero",
            "required_units": "dimensionless_coefficient_or_declared_normalized_surface_pairing",
            "required_source": "DIC3151_0 and DIC3151_1 with the same S, norm and parent action",
            "numeric_value": "MISSING_NUMERIC_OR_ZERO_THEOREM",
            "coefficient_cap": fmt(values["derivative_single_coeff_cap"]),
            "eta_cap": fmt(values["derivative_single_eta_cap"]),
            "rho_cap_against_raw_surface": fmt(values["derivative_single_rho_cap"]),
            "status": "cap_ready_input_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "DIC3151_3_product_equal_split_cap",
            "quantity": "norm_dS_W_times_norm_Lambda",
            "definition": "diagnostic per-term derivative leakage product under equal split across six unsigned surface/flux heads",
            "required_units": "dimensionless_coefficient_or_declared_normalized_surface_pairing",
            "required_source": "DIC3151_0 and DIC3151_1 with all sibling term assumptions declared",
            "numeric_value": "MISSING_NUMERIC_OR_ZERO_THEOREM",
            "coefficient_cap": fmt(values["derivative_equal_coeff_cap"]),
            "eta_cap": fmt(values["derivative_equal_eta_cap"]),
            "rho_cap_against_raw_surface": fmt(values["derivative_equal_rho_cap"]),
            "status": "cap_ready_input_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "DIC3151_4_poynting_single_term_cap",
            "quantity": "poynting_flux_abs",
            "definition": "normalized EM/Poynting flux contribution if it is the only surviving flux term",
            "required_units": "dimensionless_coefficient_or_declared_normalized_flux",
            "required_source": "stress-energy/Poynting readout with integration domain and normalization M_H",
            "numeric_value": "MISSING_NUMERIC_OR_ZERO_THEOREM",
            "coefficient_cap": fmt(values["poynting_single_coeff_cap"]),
            "eta_cap": fmt(values["derivative_single_eta_cap"]),
            "rho_cap_against_raw_surface": fmt(values["derivative_single_rho_cap"]),
            "status": "cap_ready_input_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "DIC3151_5_poynting_equal_split_cap",
            "quantity": "poynting_flux_abs",
            "definition": "diagnostic per-term EM/Poynting flux cap under equal split across six unsigned surface/flux heads",
            "required_units": "dimensionless_coefficient_or_declared_normalized_flux",
            "required_source": "stress-energy/Poynting readout with all sibling term assumptions declared",
            "numeric_value": "MISSING_NUMERIC_OR_ZERO_THEOREM",
            "coefficient_cap": fmt(values["poynting_equal_coeff_cap"]),
            "eta_cap": fmt(values["derivative_equal_eta_cap"]),
            "rho_cap_against_raw_surface": fmt(values["derivative_equal_rho_cap"]),
            "status": "cap_ready_input_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def score_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "score_id": "SC3151_0_current_active",
            "scenario": "current_absolute_surface_terms_retained",
            "coefficient_abs": fmt(values["active_coeff"]),
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": fmt(values["active_eta"]),
            "eta_bound": fmt(values["active_eta_bound"]),
            "score": "above_threshold_pressure_retained",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "BOUNDARY_FIXEDNESS_UNSIGNED;KERNEL_CLOSEDNESS_UNSIGNED;DERIVATIVE_INPUT_MISSING",
            "generated_utc": now,
        },
        {
            "score_id": "SC3151_1_if_boundary_fixed_only",
            "scenario": "B_class fixed before readout but d_S(W) not yet closed",
            "coefficient_abs": "not_promoted",
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "not_promoted",
            "eta_bound": fmt(values["active_eta_bound"]),
            "score": "not_enough_for_pass",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "D_source_W_zero_does_not_imply_dS_W_zero",
            "generated_utc": now,
        },
        {
            "score_id": "SC3151_2_if_derivative_product_under_single_cap",
            "scenario": "derivative term bounded below single-term cap",
            "coefficient_abs": "<= " + fmt(values["derivative_single_coeff_cap"]),
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "<= " + fmt(values["derivative_single_eta_cap"]),
            "eta_bound": fmt(values["active_eta_bound"]),
            "score": "derivative_term_acceptable_only_if_sibling_terms_zero_or_bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "SIBLING_SURFACE_FLUX_TERMS_REMAIN",
            "generated_utc": now,
        },
        {
            "score_id": "SC3151_3_if_all_surface_terms_zero",
            "scenario": "Coulomb-only conditional inherited from 3150",
            "coefficient_abs": fmt(values["conditional_coeff"]),
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": fmt(values["conditional_eta"]),
            "eta_bound": fmt(values["active_eta_bound"]),
            "score": "would_pass_if_all_surface_terms_zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "issues": "CONDITIONAL_ONLY",
            "generated_utc": now,
        },
    ]


def fork_rule_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "rule_id": "FR3151_0_time_story_not_auto_reject",
            "rule": "A branch is not rejected merely because its coordinate-time story appears opposite to GR.",
            "use": "test invariant observables, weak-field GR/Newton limits, conservation and calibration before rejection",
            "status": "method_note_nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "rule_id": "FR3151_1_engineering_derivation_bias",
            "rule": "Nothing just is: prefer a derivation or a sourced finite bound before accepting a closure axiom.",
            "use": "when a fork appears plausible, push once for parent-owned mechanism before demoting to closure",
            "status": "method_note_nonclaim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "D3151_0_boundary_class",
            "decision": "boundary-class fixedness has a precise theorem shape but is not parent-signed",
            "effect": "do not use B_class fixedness to claim d_S(W)=0",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3151_1_refinement",
            "decision": "fixed boundary labels remove source/readout drift but do not alone prove surface closedness",
            "effect": "the next proof must target kernel closedness on S or supply a derivative norm bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3151_2_contract",
            "decision": "norm_dS_W, norm_Lambda and poynting_flux_abs are staged as source-ready input rows",
            "effect": "future work can fill numbers without re-opening the score algebra",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3151_3_next",
            "decision": "next target should prove kernel closedness under fixed B_class or acquire the first numeric derivative/Poynting bound",
            "effect": "3152 should attack d_S Wbar=0 on S, or source norm_dS_W, norm_Lambda and Poynting flux from the parent geometry",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    theorem: list[dict[str, str]],
    gates: list[dict[str, str]],
    contract: list[dict[str, str]],
    scores: list[dict[str, str]],
    fork_rules: list[dict[str, str]],
    decisions: list[dict[str, str]],
    values: dict[str, float | None],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    theorem_refinement = {"BCF3151_1_fixedness_before_readout", "BCF3151_2_source_fixedness_not_surface_closedness", "BCF3151_4_bound_fallback"}.issubset(
        {row["theorem_id"] for row in theorem}
    )
    gates_block = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in gates)
    required_contract = {"DIC3151_0_norm_dS_W", "DIC3151_1_norm_Lambda", "DIC3151_2_product_single_term_cap", "DIC3151_4_poynting_single_term_cap"}.issubset(
        {row["contract_id"] for row in contract}
    )
    caps_positive = all(
        values[key] is not None and values[key] > 0
        for key in [
            "derivative_single_coeff_cap",
            "derivative_equal_coeff_cap",
            "poynting_single_coeff_cap",
            "poynting_equal_coeff_cap",
        ]
    )
    contract_nonclaim = all(row["valid_for_claim"] == "false" for row in contract)
    active_retained = any(row["score_id"] == "SC3151_0_current_active" and row["score"] == "above_threshold_pressure_retained" for row in scores)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for collection in [theorem, gates, contract, scores, fork_rules, decisions]
        for row in collection
    )
    score_numerics = all(
        values[key] is not None
        for key in [
            "active_coeff",
            "active_threshold",
            "active_eta",
            "active_eta_bound",
            "conditional_coeff",
            "conditional_eta",
        ]
    )
    return [
        {
            "check_id": "V3151_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3151_1_theorem_refinement_present",
            "status": "pass" if theorem_refinement else "fail",
            "details": json.dumps([row["theorem_id"] for row in theorem], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3151_2_gate_blockers_retained",
            "status": "pass" if gates_block else "fail",
            "details": json.dumps({row["gate_id"]: row["status"] for row in gates}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3151_3_contract_rows_and_caps",
            "status": "pass" if required_contract and caps_positive and contract_nonclaim else "fail",
            "details": json.dumps({key: fmt(values[key]) for key in values if "cap" in key}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3151_4_active_pressure_retained",
            "status": "pass" if active_retained and score_numerics else "fail",
            "details": "boundary fixedness is not promoted to d_S(W)=0; derivative input remains missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3151_5_no_claim_leak",
            "status": "pass" if all_nonclaim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    values = cap_values()
    theorem = theorem_rows()
    gates = gate_rows()
    contract = contract_rows(values)
    scores = score_rows(values)
    fork_rules = fork_rule_rows()
    decisions = decision_rows()
    validations = validation_rows(inputs, theorem, gates, contract, scores, fork_rules, decisions, values)
    write_csv(INPUTS, inputs)
    write_csv(THEOREM, theorem)
    write_csv(GATES, gates)
    write_csv(CONTRACT, contract)
    write_csv(SCORES, scores)
    write_csv(FORK_RULES, fork_rules)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
