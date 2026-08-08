from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3154_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3154_WBAR_BASIC_QUOTIENT_THEOREM.csv"
GATES = OUT / "P8_Y5_R2FR_3154_BASICNESS_GATE_STATUS.csv"
COMPONENTS = OUT / "P8_Y5_R2FR_3154_BPHYS_COMPONENT_BOUND_ROWS.csv"
SCORES = OUT / "P8_Y5_R2FR_3154_REDUCED_SCORECARD.csv"
DECISION = OUT / "P8_Y5_R2FR_3154_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3154_VALIDATION.csv"


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
            "source_id": "SRC3154_0_3153_doc",
            "path": source_path("3153-Y5-R2FR-source-support-levelset-split-or-physical-drift-bound-under-AX1090.md"),
            "role": "handoff requiring Wbar basicness or first B_phys component bound",
        },
        {
            "source_id": "SRC3154_1_3153_split",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3153_SOURCE_SUPPORT_DRIFT_SPLIT.csv"),
            "role": "drift decomposition and reduced derivative target",
        },
        {
            "source_id": "SRC3154_2_3153_components",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3153_PHYSICAL_DRIFT_COMPONENTS.csv"),
            "role": "physical drift component list",
        },
        {
            "source_id": "SRC3154_3_3153_contract",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3153_REDUCED_BOUND_CONTRACT.csv"),
            "role": "reduced B_phys product caps",
        },
        {
            "source_id": "SRC3154_4_3102_quotient",
            "path": source_path("3102-Y5-R2FR-verify-Xhat-verticality-and-matter-descent-under-AX1090.md"),
            "role": "quotient descent theorem shape for vertical directions",
        },
        {
            "source_id": "SRC3154_5_3114_strict_local",
            "path": source_path("3114-Y5-R2FR-strict-local-quotient-parent-signature-checklist-under-AX1090.md"),
            "role": "strict local quotient and boundary/pure-gauge warning",
        },
        {
            "source_id": "SRC3154_6_3105_poynting",
            "path": source_path("3105-Y5-R2FR-EM-wave-Poynting-public-geometry-route-under-AX1090.md"),
            "role": "Poynting public stress or residual double-counting guard",
        },
        {
            "source_id": "SRC3154_7_3116_maxwell",
            "path": source_path("3116-Y5-R2FR-public-Hodge-Maxwell-stress-lock-or-constitutive-residual-vector-under-AX1090.md"),
            "role": "public Hodge/Maxwell stress lock",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def cap_values() -> dict[str, float | None]:
    contracts = read_csv(OUT / "P8_Y5_R2FR_3153_REDUCED_BOUND_CONTRACT.csv")
    scores = read_csv(OUT / "P8_Y5_R2FR_3153_SCORE_IMPACT.csv")
    single = find_row(contracts, "contract_id", "RBC3153_3_single_cap")
    equal = find_row(contracts, "contract_id", "RBC3153_4_equal_split_cap")
    poynting = find_row(contracts, "contract_id", "RBC3153_5_poynting")
    active = find_row(scores, "score_id", "SC3153_0_current_active")
    conditional = find_row(scores, "score_id", "SC3153_3_if_all_surface_terms_zero")
    return {
        "single_coeff_cap": parse_float(single.get("coefficient_cap")) if single else None,
        "single_eta_cap": parse_float(single.get("eta_cap")) if single else None,
        "equal_coeff_cap": parse_float(equal.get("coefficient_cap")) if equal else None,
        "equal_eta_cap": parse_float(equal.get("eta_cap")) if equal else None,
        "poynting_single_coeff_cap": parse_float(poynting.get("coefficient_cap_single")) if poynting else None,
        "poynting_equal_coeff_cap": parse_float(poynting.get("coefficient_cap_equal_split")) if poynting else None,
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
            "theorem_id": "WBQ3154_0_boundary_group",
            "object": "boundary gauge group",
            "statement": "The pure boundary gauge directions are generated by tangential reparametrizations, local frame rotations/boosts, and visible U(1) gauge.",
            "formula": "G_S := Diff(S) semidirect SO(1,3)_S semidirect U(1)_S; V_G := ker(D pi_G)",
            "proof_content": "This defines which part of d_S z_S may be quotient noise rather than physical drift.",
            "status": "definition_shape",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "WBQ3154_1_basicness_annihilator",
            "object": "Wbar",
            "statement": "If Wbar descends to the quotient of boundary data by G_S, then its derivative annihilates pure boundary gauge directions.",
            "formula": "Wbar = Wtilde o pi_G => D_z Wbar[V_G]=0",
            "proof_content": "For a curve z(t)=g(t).z on a G_S orbit, pi_G(z(t)) is constant, so d/dt Wbar(z(t))=D_z Wbar[V_G]=0.",
            "status": "conditional_math_theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "WBQ3154_2_chain_reduction",
            "object": "d_S W",
            "statement": "If WBQ3154_1 is parent-signed and source support removes compact current crossing, the derivative depends only on physical boundary drift.",
            "formula": "d_S W = D_z Wbar[P_phys d_S z_S]",
            "proof_content": "Insert d_S z_S=d_S z_const+d_S z_gauge+d_S z_support+d_S z_phys into the 3152 chain rule and annihilate the first three pieces when their gates pass.",
            "status": "conditional_reduction",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "WBQ3154_3_nonquotient_guard",
            "object": "physical boundary drift",
            "statement": "Metric multipoles, reference/readout movement, EM flux and constitutive drift cannot be quotiented away without deleting physical observables.",
            "formula": "P_phys d_S z_S not in V_G unless a separate symmetry/no-flux/reference theorem is signed",
            "proof_content": "These components change observed geometry, flux or calibration conventions; they must be theorem-zeroed or bounded, not called gauge.",
            "status": "guard_active",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "WBQ3154_4_current_status",
            "object": "parent Wbar owner",
            "statement": "The theorem shape is clean, but current MTS has not supplied the parent Wbar functional, quotient map pi_G, or allowed tangent domain.",
            "formula": "MISSING(Wbar, pi_G, V_G, P_phys, source_worldtube)",
            "proof_content": "The basicness route is retained as the best derivation route but remains nonclaim.",
            "status": "not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "G3154_0_boundary_group_declared",
            "gate": "boundary gauge group and vertical tangent directions declared",
            "status": "pass_nonclaim",
            "reason": "G_S and V_G are defined for the proof contract",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3154_1_basicness_math",
            "gate": "basic function annihilates quotient vertical directions",
            "status": "pass_conditional_math",
            "reason": "standard quotient chain-rule theorem; conditional only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3154_2_parent_Wbar_owner",
            "gate": "parent action supplies Wbar and pi_G",
            "status": "fail_for_claim",
            "reason": "Wbar functional, quotient map and tangent-domain owner are not sourced",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3154_3_no_physical_gauge_overreach",
            "gate": "physical multipole/reference/EM drift is not classified as gauge",
            "status": "pass_nonclaim",
            "reason": "3154 explicitly retains these as B_phys components",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3154_4_Bphys_first_component_rows",
            "gate": "first B_phys component rows are source-ready",
            "status": "pass_nonclaim",
            "reason": "metric/reference/EM/harmonic component rows are staged with caps and blockers",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def component_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "component_id": "BPC3154_0_B_metric_multipole_tidal",
            "quantity": "B_metric_multipole_tidal",
            "definition": "physical tangential drift of public metric/coframe/measure on S from multipoles, tides, binding fields or non-spherical source structure",
            "zero_condition": "exact stationary spherical monopole exterior and S is a symmetry sphere with no external tides",
            "bound_formula": "B_metric <= B_J2 + B_tide + B_spin + B_binding + B_shape",
            "numeric_value": "MISSING_SYMMETRY_ZERO_OR_MULTIPOLE_BOUND",
            "coefficient_cap_if_single": fmt(values["single_coeff_cap"]),
            "coefficient_cap_equal_split": fmt(values["equal_coeff_cap"]),
            "required_source": "weak-field metric/coframe profile on S, source multipoles/tides, norm convention, same Wbar/P_phys map",
            "status": "first_component_bound_row_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "BPC3154_1_B_reference_readout",
            "quantity": "B_reference_readout",
            "definition": "physical drift of reference subtraction, projector/readout convention or calibration surface along S",
            "zero_condition": "reference/readout is a fixed quotient scalar functional chosen before source/calibration/readout comparison",
            "bound_formula": "B_ref <= ||d_S reference|| + ||d_S projector|| + ||d_S calibration_convention||",
            "numeric_value": "MISSING_FIXED_REFERENCE_ZERO_OR_READOUT_BOUND",
            "coefficient_cap_if_single": fmt(values["single_coeff_cap"]),
            "coefficient_cap_equal_split": fmt(values["equal_coeff_cap"]),
            "required_source": "parent reference/readout functional and proof it is fixed before comparison, or finite drift norm",
            "status": "component_bound_row_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "BPC3154_2_B_EM_flux_constitutive",
            "quantity": "B_EM_flux_constitutive",
            "definition": "physical EM/Poynting/constitutive/Hodge drift on S",
            "zero_condition": "public Maxwell stress, stationary no-radiation worldtube and metric-Hodge constitutive lock",
            "bound_formula": "B_EM <= poynting_flux_abs + delta_star + C_constitutive + delta_J + b_alpha",
            "numeric_value": "MISSING_STATIONARY_ZERO_OR_EM_CONSTITUTIVE_BOUND",
            "coefficient_cap_if_single": fmt(values["poynting_single_coeff_cap"]),
            "coefficient_cap_equal_split": fmt(values["poynting_equal_coeff_cap"]),
            "required_source": "public T_EM, observed tetrad, worldtube flux integral, constitutive/Hodge residual rows",
            "status": "component_bound_row_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "BPC3154_3_B_harmonic_corner",
            "quantity": "B_harmonic_corner",
            "definition": "harmonic/cohomology/corner part of physical boundary drift not removed by local support",
            "zero_condition": "corner-free harmonic-free relative boundary class signed by parent action",
            "bound_formula": "B_hc <= B_harmonic + B_corner + B_residual_surface",
            "numeric_value": "MISSING_COHOMOLOGY_CORNER_ZERO_OR_BOUND",
            "coefficient_cap_if_single": fmt(values["single_coeff_cap"]),
            "coefficient_cap_equal_split": fmt(values["equal_coeff_cap"]),
            "required_source": "relative cohomology certificate, corner policy and residual surface norm",
            "status": "component_bound_row_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "BPC3154_4_Bphys_total",
            "quantity": "B_phys",
            "definition": "retained physical boundary drift after quotient-basic, fixed-label and compact-support removals",
            "zero_condition": "all physical components above are theorem-zero",
            "bound_formula": "B_phys <= B_metric_multipole_tidal + B_reference_readout + B_EM_flux_constitutive + B_harmonic_corner",
            "numeric_value": "MISSING_COMPONENT_VALUES",
            "coefficient_cap_if_single": fmt(values["single_coeff_cap"]),
            "coefficient_cap_equal_split": fmt(values["equal_coeff_cap"]),
            "required_source": "all BPC3154 component values or zero theorems plus L_W_phys and Lambda norm",
            "status": "total_bound_row_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def score_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "score_id": "SC3154_0_current_active",
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
            "score_id": "SC3154_1_if_Wbar_basic_only",
            "scenario": "pure boundary gauge/reparam drift annihilated",
            "coefficient_abs": "not_computed_without_Bphys",
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "not_computed_without_Bphys",
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "problem_reduced_not_passed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3154_2_if_Bphys_product_under_single_cap",
            "scenario": "L_W_phys B_phys ||Lambda|| under single-survivor cap",
            "coefficient_abs": "<= " + fmt(values["single_coeff_cap"]),
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "<= " + fmt(values["single_eta_cap"]),
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "derivative_term_acceptable_if_sibling_terms_zero_or_bounded",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3154_3_if_all_surface_terms_zero",
            "scenario": "Coulomb-only conditional inherited from 3153",
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


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "D3154_0_basicness_result",
            "decision": "Wbar-basicness gives a real annihilator theorem for pure boundary gauge/reparametrization directions",
            "effect": "this can remove d_S z_gauge if the parent Wbar quotient owner is supplied",
            "next_action": "source Wbar/pi_G/V_G or keep basicness conditional",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3154_1_physical_drift_result",
            "decision": "physical drift cannot be classified as gauge",
            "effect": "B_metric_multipole_tidal, B_reference_readout, B_EM_flux_constitutive and B_harmonic_corner remain live",
            "next_action": "attack B_metric_multipole_tidal first for local Newton/PPN, or B_EM_flux_constitutive for Maxwell/Poynting",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3154_2_next",
            "decision": "next best target is the first physical component theorem/bound",
            "effect": "3155 should derive exact monopole/symmetry zero for B_metric_multipole_tidal or source the first finite multipole/tidal row",
            "next_action": "3155-Y5-R2FR-Bmetric-monopole-tidal-zero-or-first-bound-row",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    theorem: list[dict[str, str]],
    gates: list[dict[str, str]],
    components: list[dict[str, str]],
    scores: list[dict[str, str]],
    decisions: list[dict[str, str]],
    values: dict[str, float | None],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    theorem_cover = {"WBQ3154_1_basicness_annihilator", "WBQ3154_2_chain_reduction", "WBQ3154_3_nonquotient_guard"}.issubset(
        {row["theorem_id"] for row in theorem}
    )
    parent_blocked = any(row["gate_id"] == "G3154_2_parent_Wbar_owner" and row["status"] == "fail_for_claim" for row in gates)
    components_cover = {"BPC3154_0_B_metric_multipole_tidal", "BPC3154_1_B_reference_readout", "BPC3154_2_B_EM_flux_constitutive", "BPC3154_4_Bphys_total"}.issubset(
        {row["component_id"] for row in components}
    )
    caps_positive = all(
        values[key] is not None and values[key] > 0
        for key in [
            "single_coeff_cap",
            "equal_coeff_cap",
            "poynting_single_coeff_cap",
            "poynting_equal_coeff_cap",
        ]
    )
    active_retained = any(row["score_id"] == "SC3154_0_current_active" and row["result"] == "above_threshold_pressure_retained" for row in scores)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for collection in [theorem, gates, components, scores, decisions]
        for row in collection
    )
    return [
        {
            "check_id": "V3154_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3154_1_basicness_theorem_present",
            "status": "pass" if theorem_cover else "fail",
            "details": json.dumps([row["theorem_id"] for row in theorem], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3154_2_parent_owner_blocks_claim",
            "status": "pass" if parent_blocked else "fail",
            "details": json.dumps({row["gate_id"]: row["status"] for row in gates}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3154_3_Bphys_components_and_caps",
            "status": "pass" if components_cover and caps_positive else "fail",
            "details": json.dumps({key: fmt(values[key]) for key in values if "cap" in key}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3154_4_active_pressure_retained",
            "status": "pass" if active_retained else "fail",
            "details": "basicness theorem reduces gauge drift only; physical drift remains unfilled",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3154_5_no_claim_leak",
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
    components = component_rows(values)
    scores = score_rows(values)
    decisions = decision_rows()
    validations = validation_rows(inputs, theorem, gates, components, scores, decisions, values)
    write_csv(INPUTS, inputs)
    write_csv(THEOREM, theorem)
    write_csv(GATES, gates)
    write_csv(COMPONENTS, components)
    write_csv(SCORES, scores)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
