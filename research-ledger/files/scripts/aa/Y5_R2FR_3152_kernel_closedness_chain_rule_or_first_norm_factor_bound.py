from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3152_INPUTS.csv"
DERIVATION = OUT / "P8_Y5_R2FR_3152_KERNEL_CLOSEDNESS_DERIVATION.csv"
GATES = OUT / "P8_Y5_R2FR_3152_ANNIHILATOR_GATE_STATUS.csv"
FACTORS = OUT / "P8_Y5_R2FR_3152_DERIVATIVE_NORM_FACTORIZATION.csv"
SCORES = OUT / "P8_Y5_R2FR_3152_BOUND_SCORECARD.csv"
NEXT = OUT / "P8_Y5_R2FR_3152_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3152_VALIDATION.csv"


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
            "source_id": "SRC3152_0_3151_doc",
            "path": source_path("3151-Y5-R2FR-boundary-class-fixedness-or-derivative-input-contract-under-AX1090.md"),
            "role": "handoff requiring d_S Wbar zero or first derivative/Poynting norm rows",
        },
        {
            "source_id": "SRC3152_1_3151_theorem",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3151_BOUNDARY_CLASS_FIXEDNESS_THEOREM.csv"),
            "role": "boundary-class fixedness versus surface closedness refinement",
        },
        {
            "source_id": "SRC3152_2_3151_contract",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3151_DERIVATIVE_INPUT_CONTRACT.csv"),
            "role": "derivative and Poynting caps",
        },
        {
            "source_id": "SRC3152_3_3151_gates",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3151_GATE_STATUS.csv"),
            "role": "unsigned parent B_class, reference, readout and kernel gates",
        },
        {
            "source_id": "SRC3152_4_3105_poynting",
            "path": source_path("3105-Y5-R2FR-EM-wave-Poynting-public-geometry-route-under-AX1090.md"),
            "role": "Poynting belongs to public EM stress or explicit residual",
        },
        {
            "source_id": "SRC3152_5_3116_maxwell",
            "path": source_path("3116-Y5-R2FR-public-Hodge-Maxwell-stress-lock-or-constitutive-residual-vector-under-AX1090.md"),
            "role": "public Hodge/Maxwell stress lock and Delta_S_Poynting residual",
        },
        {
            "source_id": "SRC3152_6_3149_flux_schema",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3149_STOKES_FLUX_BOUND_SCHEMA.csv"),
            "role": "kernel derivative, Poynting, corner, harmonic, residual and readout terms",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def cap_values() -> dict[str, float | None]:
    contract = read_csv(OUT / "P8_Y5_R2FR_3151_DERIVATIVE_INPUT_CONTRACT.csv")
    scores = read_csv(OUT / "P8_Y5_R2FR_3151_SCORE_IMPACT.csv")
    derivative_single = find_row(contract, "contract_id", "DIC3151_2_product_single_term_cap")
    derivative_equal = find_row(contract, "contract_id", "DIC3151_3_product_equal_split_cap")
    poynting_single = find_row(contract, "contract_id", "DIC3151_4_poynting_single_term_cap")
    poynting_equal = find_row(contract, "contract_id", "DIC3151_5_poynting_equal_split_cap")
    active = find_row(scores, "score_id", "SC3151_0_current_active")
    conditional = find_row(scores, "score_id", "SC3151_3_if_all_surface_terms_zero")
    return {
        "derivative_single_coeff_cap": parse_float(derivative_single.get("coefficient_cap")) if derivative_single else None,
        "derivative_single_eta_cap": parse_float(derivative_single.get("eta_cap")) if derivative_single else None,
        "derivative_equal_coeff_cap": parse_float(derivative_equal.get("coefficient_cap")) if derivative_equal else None,
        "derivative_equal_eta_cap": parse_float(derivative_equal.get("eta_cap")) if derivative_equal else None,
        "poynting_single_coeff_cap": parse_float(poynting_single.get("coefficient_cap")) if poynting_single else None,
        "poynting_equal_coeff_cap": parse_float(poynting_equal.get("coefficient_cap")) if poynting_equal else None,
        "active_coeff": parse_float(active.get("coefficient_abs")) if active else None,
        "active_threshold": parse_float(active.get("threshold_abs")) if active else None,
        "active_eta": parse_float(active.get("eta_abs")) if active else None,
        "active_eta_bound": parse_float(active.get("eta_bound")) if active else None,
        "conditional_coeff": parse_float(conditional.get("coefficient_abs")) if conditional else None,
        "conditional_eta": parse_float(conditional.get("eta_abs")) if conditional else None,
    }


def derivation_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "derivation_id": "KCD3152_0_pullback_setup",
            "object": "weighted-Stokes kernel",
            "statement": "Restrict the weight to the certified boundary surface as a pullback from parent boundary data.",
            "formula": "W|S = z_S^* Wbar, with z_S=(B_class,lambda,epsilon,xi,mu_obs,reference)|S",
            "proof_content": "This is the object language needed for 3151: all readout/source dependence is routed through z_S.",
            "status": "definition_shape_nonclaim",
            "zero_route": "none_by_itself",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "KCD3152_1_chain_rule",
            "object": "surface derivative of W",
            "statement": "The missing derivative term factors by the surface chain rule.",
            "formula": "d_S W = (D_z Wbar) o d_S z_S",
            "proof_content": "For every tangent vector tau in T(S), d_S W[tau]=D_z Wbar[z_S](d_S z_S[tau]).",
            "status": "exact_math_identity",
            "zero_route": "factor_either_DzWbar_or_dSz",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "KCD3152_2_boundary_levelset_zero",
            "object": "boundary data drift",
            "statement": "If the allowed source surface is a level set of all kernel-relevant boundary data, then d_S(W)=0.",
            "formula": "d_S z_S=0 => d_S W=0",
            "proof_content": "Insert d_S z_S=0 into KCD3152_1. This is a real zero theorem if the parent action signs the level-set condition.",
            "status": "conditional_not_parent_signed",
            "zero_route": "boundary_levelset",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "KCD3152_3_annihilator_zero",
            "object": "kernel tangent annihilator",
            "statement": "The kernel can be closed even with tangential boundary variation if Wbar is blind to the allowed tangent image.",
            "formula": "D_z Wbar | Im(d_S z_S)=0 => d_S W=0",
            "proof_content": "This is the least-cheap nontrivial route: it permits boundary structure but requires the parent kernel to annihilate those directions.",
            "status": "conditional_not_parent_signed",
            "zero_route": "kernel_annihilator",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "KCD3152_4_lipschitz_bound",
            "object": "finite derivative norm",
            "statement": "If neither zero route is signed, the derivative term has a clean factor bound.",
            "formula": "||d_S W||_* <= ||D_z Wbar||_op ||d_S z_S||_*",
            "proof_content": "This is the operator-norm version of KCD3152_1 and replaces one foggy input by two sourceable factors.",
            "status": "exact_bound_identity_needs_numeric_factors",
            "zero_route": "finite_factor_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "KCD3152_5_poynting_stationary_vacuum_zero",
            "object": "Poynting flux",
            "statement": "The EM flux term is zero only under a public-Maxwell stationary/no-radiation crossing condition, not by hidden-background rhetoric.",
            "formula": "n_i S_EM^i|partialW=0 with public T_EM and fixed integration worldtube => poynting_flux_abs=0",
            "proof_content": "3105/3116 allow this only if Poynting is public Hilbert stress and no EM radiation/constitutive residual crosses the boundary.",
            "status": "conditional_not_parent_signed",
            "zero_route": "stationary_public_EM",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "G3152_0_chain_rule_written",
            "gate": "d_S W factors through parent boundary data",
            "status": "pass_nonclaim",
            "reason": "KCD3152_1 gives the exact chain-rule identity",
            "blocks_claim": "false",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3152_1_boundary_levelset_parent_signed",
            "gate": "parent action proves d_S z_S=0",
            "status": "fail_for_claim",
            "reason": "B_class/reference/readout/kernel data are not jointly parent-signed as level-set data on S",
            "blocks_claim": "true",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3152_2_kernel_annihilator_parent_signed",
            "gate": "D_z Wbar annihilates allowed tangential boundary variations",
            "status": "fail_for_claim",
            "reason": "the parent kernel functional Wbar has not supplied its tangent annihilator or symmetry owner",
            "blocks_claim": "true",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3152_3_lipschitz_factor_inputs",
            "gate": "L_W, boundary-data drift and Lambda norm are numeric/source-backed",
            "status": "fail_for_claim",
            "reason": "3152 creates source-ready factor rows but values are still missing",
            "blocks_claim": "true",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3152_4_poynting_stationary_public_EM",
            "gate": "EM Poynting boundary flux is zero or bounded",
            "status": "not_claim_ready",
            "reason": "public Maxwell stress route exists, but stationary/no-radiation worldtube is not parent-signed",
            "blocks_claim": "true",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def factor_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "factor_id": "DNF3152_0_L_W",
            "quantity": "L_W",
            "definition": "operator norm of parent kernel sensitivity to boundary data",
            "formula": "L_W := ||D_z Wbar||_op",
            "zero_condition": "D_z Wbar annihilates Im(d_S z_S)",
            "numeric_value": "MISSING_PARENT_KERNEL_DERIVATIVE",
            "required_source": "explicit Wbar functional and tangent domain for z_S",
            "status": "missing_parent_input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "factor_id": "DNF3152_1_B_z",
            "quantity": "B_z",
            "definition": "surface drift norm of all kernel-relevant boundary data",
            "formula": "B_z := ||d_S z_S||_*",
            "zero_condition": "boundary surface is a parent-signed level set of z_S",
            "numeric_value": "MISSING_BOUNDARY_LEVELSET_OR_DRIFT_BOUND",
            "required_source": "B_class, lambda, epsilon, xi, mu_obs and reference profiles on S",
            "status": "missing_parent_input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "factor_id": "DNF3152_2_norm_Lambda",
            "quantity": "norm_Lambda",
            "definition": "compatible primitive norm in B_surf=d_S Lambda+h+r",
            "formula": "||Lambda||_*",
            "zero_condition": "Lambda=0 or exact primitive killed by parent boundary condition",
            "numeric_value": "MISSING_PRIMITIVE_NORM",
            "required_source": "same surface S and same norm convention as L_W and B_z",
            "status": "missing_parent_input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "factor_id": "DNF3152_3_single_term_product",
            "quantity": "L_W_times_B_z_times_norm_Lambda",
            "definition": "single-survivor derivative leakage product",
            "formula": "L_W B_z ||Lambda||_* <= coefficient_cap",
            "zero_condition": "L_W=0 or B_z=0 or ||Lambda||=0",
            "numeric_value": "MISSING_FACTOR_PRODUCT",
            "required_source": "DNF3152_0, DNF3152_1 and DNF3152_2",
            "coefficient_cap": fmt(values["derivative_single_coeff_cap"]),
            "eta_cap": fmt(values["derivative_single_eta_cap"]),
            "status": "cap_ready_factors_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "factor_id": "DNF3152_4_equal_split_product",
            "quantity": "L_W_times_B_z_times_norm_Lambda",
            "definition": "six-way diagnostic derivative leakage product",
            "formula": "L_W B_z ||Lambda||_* <= equal_split_cap",
            "zero_condition": "same as DNF3152_3 with sibling terms included",
            "numeric_value": "MISSING_FACTOR_PRODUCT",
            "required_source": "DNF3152_0, DNF3152_1, DNF3152_2 and sibling-term assumptions",
            "coefficient_cap": fmt(values["derivative_equal_coeff_cap"]),
            "eta_cap": fmt(values["derivative_equal_eta_cap"]),
            "status": "cap_ready_factors_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "factor_id": "DNF3152_5_poynting_worldtube_flux",
            "quantity": "poynting_flux_abs",
            "definition": "normalized EM flux crossing the local integration worldtube",
            "formula": "|Int_partialW S_EM dot dA dt|/M_H",
            "zero_condition": "public Maxwell stress plus stationary/no-radiation crossing boundary",
            "numeric_value": "MISSING_STATIONARY_ZERO_OR_FLUX_BOUND",
            "required_source": "public T_EM, observed tetrad, integration worldtube, M_H normalization and radiation condition",
            "coefficient_cap_single": fmt(values["poynting_single_coeff_cap"]),
            "coefficient_cap_equal_split": fmt(values["poynting_equal_coeff_cap"]),
            "status": "cap_ready_flux_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def score_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "score_id": "SC3152_0_current_active",
            "scenario": "current active surface terms retained",
            "coefficient_abs": fmt(values["active_coeff"]),
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": fmt(values["active_eta"]),
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "above_threshold_pressure_retained",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3152_1_if_levelset_or_annihilator_zero",
            "scenario": "d_S W is theorem-zero by levelset or annihilator route",
            "coefficient_abs": "derivative_term_removed_only",
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "not_full_score_because_sibling_terms_remain",
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "useful_but_not_full_pass",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3152_2_if_factor_product_under_cap",
            "scenario": "L_W B_z ||Lambda|| under single-survivor cap",
            "coefficient_abs": "<= " + fmt(values["derivative_single_coeff_cap"]),
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "<= " + fmt(values["derivative_single_eta_cap"]),
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "derivative_term_acceptable_if_siblings_zero_or_bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3152_3_if_poynting_stationary_zero",
            "scenario": "Poynting boundary flux removed by public stationary/no-radiation condition",
            "coefficient_abs": "flux_term_removed_only",
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "not_full_score_because_corner_harmonic_residual_reference_readout_remain",
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "useful_but_not_full_pass",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3152_4_if_all_surface_terms_zero",
            "scenario": "Coulomb-only conditional inherited from 3151",
            "coefficient_abs": fmt(values["conditional_coeff"]),
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": fmt(values["conditional_eta"]),
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "would_pass_if_all_surface_terms_zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def next_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "next_id": "N3152_0_best_derivation_route",
            "target": "prove boundary-levelset condition d_S z_S=0 from local vacuum/source support",
            "why": "this zeros the derivative term without needing numeric L_W or Lambda",
            "risk": "may wrongly delete physical source/boundary charges if not tied to parent action",
            "next_checkpoint": "3153-Y5-R2FR-boundary-levelset-source-support-or-drift-bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "next_id": "N3152_1_parallel_derivation_route",
            "target": "prove kernel annihilator D_z Wbar|Im(d_S z_S)=0 from quotient symmetry",
            "why": "this permits nontrivial boundary structure while killing only the dangerous derivative",
            "risk": "requires explicit Wbar owner and tangent-domain signature",
            "next_checkpoint": "3153-Y5-R2FR-kernel-annihilator-symmetry-owner-or-LW-bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "next_id": "N3152_2_finite_bound_route",
            "target": "fill L_W, B_z, norm_Lambda or Poynting flux as real source-backed factor rows",
            "why": "if the theorem stalls, this gives a numerical gate instead of closure rhetoric",
            "risk": "values must be parent-sourced and below 3151 caps before any local claim",
            "next_checkpoint": "3153-Y5-R2FR-first-LW-Bz-Lambda-factor-source-row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    derivations: list[dict[str, str]],
    gates: list[dict[str, str]],
    factors: list[dict[str, str]],
    scores: list[dict[str, str]],
    next_targets: list[dict[str, str]],
    values: dict[str, float | None],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    derivation_cover = {"KCD3152_1_chain_rule", "KCD3152_2_boundary_levelset_zero", "KCD3152_3_annihilator_zero", "KCD3152_4_lipschitz_bound"}.issubset(
        {row["derivation_id"] for row in derivations}
    )
    gate_blockers = all(row["claim_allowed"] == "false" and row["valid_for_claim"] == "false" for row in gates)
    factor_cover = {"DNF3152_0_L_W", "DNF3152_1_B_z", "DNF3152_2_norm_Lambda", "DNF3152_3_single_term_product", "DNF3152_5_poynting_worldtube_flux"}.issubset(
        {row["factor_id"] for row in factors}
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
    active_retained = any(row["score_id"] == "SC3152_0_current_active" and row["result"] == "above_threshold_pressure_retained" for row in scores)
    next_cover = any(row["next_id"] == "N3152_0_best_derivation_route" for row in next_targets)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for collection in [derivations, gates, factors, scores, next_targets]
        for row in collection
    )
    return [
        {
            "check_id": "V3152_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3152_1_chain_rule_zero_routes_present",
            "status": "pass" if derivation_cover else "fail",
            "details": json.dumps([row["derivation_id"] for row in derivations], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3152_2_gates_block_claim",
            "status": "pass" if gate_blockers else "fail",
            "details": json.dumps({row["gate_id"]: row["status"] for row in gates}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3152_3_factor_rows_and_caps",
            "status": "pass" if factor_cover and caps_positive else "fail",
            "details": json.dumps({key: fmt(values[key]) for key in values if "cap" in key}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3152_4_active_pressure_retained",
            "status": "pass" if active_retained else "fail",
            "details": "chain rule narrows the obstruction but does not claim local closure",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3152_5_next_target_selected",
            "status": "pass" if next_cover else "fail",
            "details": "best next route is boundary-levelset/source-support or kernel-annihilator owner",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3152_6_no_claim_leak",
            "status": "pass" if all_nonclaim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    values = cap_values()
    derivations = derivation_rows()
    gates = gate_rows()
    factors = factor_rows(values)
    scores = score_rows(values)
    next_targets = next_rows()
    validations = validation_rows(inputs, derivations, gates, factors, scores, next_targets, values)
    write_csv(INPUTS, inputs)
    write_csv(DERIVATION, derivations)
    write_csv(GATES, gates)
    write_csv(FACTORS, factors)
    write_csv(SCORES, scores)
    write_csv(NEXT, next_targets)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
