from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3153_INPUTS.csv"
DERIVATION = OUT / "P8_Y5_R2FR_3153_SOURCE_SUPPORT_DRIFT_SPLIT.csv"
GATES = OUT / "P8_Y5_R2FR_3153_LEVELSET_GATE_STATUS.csv"
DRIFT = OUT / "P8_Y5_R2FR_3153_PHYSICAL_DRIFT_COMPONENTS.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3153_REDUCED_BOUND_CONTRACT.csv"
SCORES = OUT / "P8_Y5_R2FR_3153_SCORE_IMPACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3153_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3153_VALIDATION.csv"


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
            "source_id": "SRC3153_0_3152_doc",
            "path": source_path("3152-Y5-R2FR-kernel-closedness-chain-rule-or-first-norm-factor-bound-under-AX1090.md"),
            "role": "handoff requiring boundary-levelset, kernel-annihilator, or factor bound",
        },
        {
            "source_id": "SRC3153_1_3152_derivation",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3152_KERNEL_CLOSEDNESS_DERIVATION.csv"),
            "role": "chain-rule and zero-route identity",
        },
        {
            "source_id": "SRC3153_2_3152_factors",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3152_DERIVATIVE_NORM_FACTORIZATION.csv"),
            "role": "L_W, B_z, norm_Lambda and Poynting factor rows",
        },
        {
            "source_id": "SRC3153_3_1015_worldtube",
            "path": source_path("1015-Y5-R10-topological-Hilbert-equality-or-R_eq-bound-runner.md"),
            "role": "compact source worldtube and same-class warning",
        },
        {
            "source_id": "SRC3153_4_1044_boundary_support",
            "path": source_path("1044-Y5-R10-matter-pullback-JX-zero-or-qbarXT-bound-row.md"),
            "role": "matter boundary support silence is only a sublemma",
        },
        {
            "source_id": "SRC3153_5_1045_descent",
            "path": source_path("1045-Y5-R10-parent-matter-functor-descent-signature-or-qbar-component-fill.md"),
            "role": "matter functor descent and boundary/source support residual",
        },
        {
            "source_id": "SRC3153_6_1068_source_worldtube",
            "path": source_path("1068-Y5-R10-WEP-tau-source-worldtube-orbit-readout-acquisition-pack.md"),
            "role": "source worldtube/profile requirements remain acquisition rows",
        },
        {
            "source_id": "SRC3153_7_3105_poynting",
            "path": source_path("3105-Y5-R2FR-EM-wave-Poynting-public-geometry-route-under-AX1090.md"),
            "role": "Poynting public-stress or residual double-counting guard",
        },
        {
            "source_id": "SRC3153_8_3116_maxwell",
            "path": source_path("3116-Y5-R2FR-public-Hodge-Maxwell-stress-lock-or-constitutive-residual-vector-under-AX1090.md"),
            "role": "public Hodge Maxwell stress lock and constitutive residual vector",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def cap_values() -> dict[str, float | None]:
    factors = read_csv(OUT / "P8_Y5_R2FR_3152_DERIVATIVE_NORM_FACTORIZATION.csv")
    scores = read_csv(OUT / "P8_Y5_R2FR_3152_BOUND_SCORECARD.csv")
    single = find_row(factors, "factor_id", "DNF3152_3_single_term_product")
    equal = find_row(factors, "factor_id", "DNF3152_4_equal_split_product")
    poynting = find_row(factors, "factor_id", "DNF3152_5_poynting_worldtube_flux")
    active = find_row(scores, "score_id", "SC3152_0_current_active")
    conditional = find_row(scores, "score_id", "SC3152_4_if_all_surface_terms_zero")
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


def derivation_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "derivation_id": "SSD3153_0_split",
            "object": "boundary data drift",
            "statement": "The boundary drift must be decomposed before asking whether source support makes it zero.",
            "formula": "d_S z_S = d_S z_const + d_S z_gauge + d_S z_support + d_S z_phys",
            "proof_content": "The chain-rule object z_S contains fixed labels, gauge/reparametrization data, compact source-support data, and physical boundary fields.",
            "status": "definition_split",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "SSD3153_1_constant_zero",
            "object": "calibrated/fixed labels",
            "statement": "Fixed boundary labels and calibrated constants have zero tangential derivative on S.",
            "formula": "d_S z_const = 0",
            "proof_content": "This follows from treating B_class labels and calibrated constants as fixed data, but it does not touch physical field profiles.",
            "status": "math_zero_for_declared_constants_only",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "SSD3153_2_gauge_annihilator",
            "object": "gauge/reparametrization drift",
            "statement": "Tangential diffeomorphism, frame, and U(1) gauge drift is harmless only if Wbar is basic under those transformations.",
            "formula": "D_z Wbar[d_S z_gauge]=0 if Wbar descends to the quotient of boundary data by gauge/reparametrization",
            "proof_content": "This is a kernel-annihilator subtheorem, not a level-set theorem.",
            "status": "conditional_not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "SSD3153_3_source_support_sublemma",
            "object": "compact source current crossing S",
            "statement": "If the matter/source support lies strictly inside the integration worldtube, the ordinary matter current crossing a vacuum collar is zero.",
            "formula": "supp(J_matter) cap S = empty => n.J_matter|S = 0",
            "proof_content": "This can silence compact-support matter boundary current, but it does not imply d_S z_phys=0.",
            "status": "conditional_support_sublemma",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "SSD3153_4_levelset_rejection",
            "object": "generic boundary level set",
            "statement": "Source support alone does not prove the full boundary level-set condition.",
            "formula": "supp(J) cap S=empty does not imply d_S(g_pub,e_pub,mu_obs,reference,lambda,epsilon)=0",
            "proof_content": "Vacuum exterior fields can carry multipoles, tidal gradients, stationary binding fields, reference drift, and radiation/constitutive flux.",
            "status": "generic_levelset_rejected",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "SSD3153_5_reduced_derivative",
            "object": "reduced kernel derivative",
            "statement": "After removing constant, gauge-basic, and compact-support-current pieces, only physical boundary drift remains.",
            "formula": "d_S W = D_z Wbar[P_phys d_S z_S]",
            "proof_content": "This is the reduced theorem target: the dangerous part is the physical projection of boundary drift.",
            "status": "conditional_reduction_not_claim",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "SSD3153_6_reduced_bound",
            "object": "physical drift bound",
            "statement": "The finite bound should use the physical operator norm and physical drift norm, not the full raw B_z.",
            "formula": "||d_S W|| ||Lambda|| <= L_W_phys B_phys ||Lambda||",
            "proof_content": "This is stronger than 3152 if gauge/support pieces are parent-signed, but it still needs numeric/source-backed physical factors.",
            "status": "exact_reduced_bound_shape_needs_inputs",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "G3153_0_constant_piece",
            "gate": "declared constants and labels have d_S=0",
            "status": "pass_nonclaim",
            "reason": "only fixed labels/constants are removed; no physical field is zeroed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3153_1_gauge_basic_kernel",
            "gate": "Wbar is basic under boundary reparametrization/frame/U(1) gauge",
            "status": "not_claim_ready",
            "reason": "plausible quotient requirement, but Wbar owner and tangent action are not parent-signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3153_2_source_support",
            "gate": "compact source current has no support on S",
            "status": "not_claim_ready",
            "reason": "source worldtube/profile remains an acquisition row in prior ledgers",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3153_3_full_levelset",
            "gate": "full d_S z_S=0 follows from source support",
            "status": "fail_for_claim",
            "reason": "false generically: vacuum exterior may have multipoles/tides/reference/readout/flux",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3153_4_physical_drift_bound",
            "gate": "B_phys and L_W_phys are numeric/source-backed",
            "status": "fail_for_claim",
            "reason": "3153 defines the reduced factors but does not fill values",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def drift_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "component_id": "PDC3153_0_fixed_labels",
            "component": "d_S z_const",
            "meaning": "fixed B_class labels, declared constants, and calibration identifiers",
            "status": "zero_as_declared_nonclaim",
            "zero_or_bound": "zero",
            "blocks": "none_if_parent_fixed_before_readout",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "PDC3153_1_gauge_reparam",
            "component": "d_S z_gauge",
            "meaning": "tangential reparametrization, local frame gauge, and U(1) gauge movement",
            "status": "conditional_annihilator",
            "zero_or_bound": "zero only if Wbar is boundary-basic",
            "blocks": "Wbar_basic_owner;gauge_tangent_domain",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "PDC3153_2_compact_support_current",
            "component": "d_S z_support",
            "meaning": "ordinary matter/source current crossing the boundary surface",
            "status": "conditional_support_zero",
            "zero_or_bound": "zero if supp(J_matter) cap S is empty",
            "blocks": "source_worldtube_profile;fixed_integration_surface",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "PDC3153_3_metric_multipole_tidal",
            "component": "d_S z_phys_metric",
            "meaning": "public metric/coframe, tidal, multipole, and binding-field variation along S",
            "status": "retained_physical_drift",
            "zero_or_bound": "requires symmetry/monopole theorem or finite multipole/tidal bound",
            "blocks": "B_metric_multipole",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "PDC3153_4_reference_readout",
            "component": "d_S z_phys_reference",
            "meaning": "reference subtraction, readout convention, and projector movement",
            "status": "retained_physical_drift",
            "zero_or_bound": "requires fixed reference/readout theorem or finite bound",
            "blocks": "B_reference_readout",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "PDC3153_5_em_flux_constitutive",
            "component": "d_S z_phys_EM",
            "meaning": "Poynting radiation, hidden Hodge/constitutive drift, alpha/current normalization movement",
            "status": "retained_physical_drift",
            "zero_or_bound": "requires stationary public EM no-flux theorem or finite flux/constitutive residual",
            "blocks": "B_EM_flux_constitutive",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "component_id": "PDC3153_6_reduced_total",
            "component": "B_phys",
            "meaning": "physical boundary drift after constant/gauge/support pieces are removed",
            "status": "missing_numeric_or_zero_theorem",
            "zero_or_bound": "B_phys <= B_metric_multipole+B_reference_readout+B_EM_flux_constitutive+B_harmonic_corner",
            "blocks": "reduced derivative product",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def contract_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "contract_id": "RBC3153_0_LW_phys",
            "quantity": "L_W_phys",
            "definition": "operator norm of D_z Wbar restricted to physical drift directions",
            "formula": "L_W_phys := ||D_z Wbar P_phys||_op",
            "numeric_value": "MISSING_KERNEL_OWNER_OR_OPERATOR_NORM",
            "required_source": "explicit Wbar, physical tangent projector P_phys, and same boundary norm",
            "status": "missing_parent_input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "RBC3153_1_B_phys",
            "quantity": "B_phys",
            "definition": "physical boundary drift after removing constants, gauge-basic drift, and compact-support current crossing",
            "formula": "B_phys := ||P_phys d_S z_S||_*",
            "numeric_value": "MISSING_PHYSICAL_DRIFT_BOUND",
            "required_source": "metric multipole/tidal, reference/readout, EM/constitutive, harmonic/corner drift rows",
            "status": "missing_parent_input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "RBC3153_2_Lambda",
            "quantity": "norm_Lambda",
            "definition": "same primitive norm as 3152 after physical drift projection",
            "formula": "||Lambda||_*",
            "numeric_value": "MISSING_PRIMITIVE_NORM",
            "required_source": "same surface, norm and primitive split B_surf=d_S Lambda+h+r",
            "status": "missing_parent_input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "RBC3153_3_single_cap",
            "quantity": "L_W_phys_times_B_phys_times_norm_Lambda",
            "definition": "single-survivor reduced derivative product",
            "formula": "L_W_phys B_phys ||Lambda||_* <= cap",
            "numeric_value": "MISSING_FACTOR_PRODUCT",
            "coefficient_cap": fmt(values["single_coeff_cap"]),
            "eta_cap": fmt(values["single_eta_cap"]),
            "required_source": "RBC3153_0, RBC3153_1, RBC3153_2",
            "status": "cap_ready_inputs_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "RBC3153_4_equal_split_cap",
            "quantity": "L_W_phys_times_B_phys_times_norm_Lambda",
            "definition": "six-way diagnostic reduced derivative product",
            "formula": "L_W_phys B_phys ||Lambda||_* <= equal_split_cap",
            "numeric_value": "MISSING_FACTOR_PRODUCT",
            "coefficient_cap": fmt(values["equal_coeff_cap"]),
            "eta_cap": fmt(values["equal_eta_cap"]),
            "required_source": "RBC3153_0, RBC3153_1, RBC3153_2, sibling-term assumptions",
            "status": "cap_ready_inputs_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "RBC3153_5_poynting",
            "quantity": "poynting_flux_abs",
            "definition": "public EM stress flux crossing the same worldtube, not double-counted as hidden background stress",
            "formula": "|Int_partialW S_EM dot dA dt|/M_H",
            "numeric_value": "MISSING_STATIONARY_ZERO_OR_FLUX_BOUND",
            "coefficient_cap_single": fmt(values["poynting_single_coeff_cap"]),
            "coefficient_cap_equal_split": fmt(values["poynting_equal_coeff_cap"]),
            "required_source": "public T_EM, no-radiation/stationary condition or finite flux integral",
            "status": "cap_ready_input_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def score_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "score_id": "SC3153_0_current_active",
            "scenario": "current active surface terms retained",
            "coefficient_abs": fmt(values["active_coeff"]),
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": fmt(values["active_eta"]),
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "above_threshold_pressure_retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3153_1_after_support_split",
            "scenario": "constant/gauge/support pieces removed but physical drift remains",
            "coefficient_abs": "not_computed_without_B_phys",
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "not_computed_without_B_phys",
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "reduced_problem_not_full_pass",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3153_2_if_reduced_product_under_cap",
            "scenario": "L_W_phys B_phys ||Lambda|| under single-survivor cap",
            "coefficient_abs": "<= " + fmt(values["single_coeff_cap"]),
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "<= " + fmt(values["single_eta_cap"]),
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "derivative_term_acceptable_if_sibling_terms_zero_or_bounded",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3153_3_if_all_surface_terms_zero",
            "scenario": "Coulomb-only conditional inherited from 3152",
            "coefficient_abs": fmt(values["conditional_coeff"]),
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": fmt(values["conditional_eta"]),
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "would_pass_if_all_surface_terms_zero",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "D3153_0_levelset",
            "decision": "full d_S z_S=0 from source support is rejected as a generic theorem",
            "effect": "do not claim the boundary-levelset route without symmetry/monopole/source-worldtube proof",
            "next_action": "attack reduced physical drift instead",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3153_1_reduction",
            "decision": "source support/gauge can reduce the derivative problem but not erase it",
            "effect": "replace raw B_z by B_phys after parent-signed gauge/support removals",
            "next_action": "derive Wbar basicness and then bound metric/reference/EM physical drift",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3153_2_next",
            "decision": "next best target is the Wbar-basic quotient theorem or first B_phys component bound",
            "effect": "3154 should prove D_z Wbar kills gauge/reparam directions, then source B_metric_multipole or Poynting flux",
            "next_action": "3154-Y5-R2FR-Wbar-basic-quotient-theorem-or-Bphys-first-component-bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    derivations: list[dict[str, str]],
    gates: list[dict[str, str]],
    drift: list[dict[str, str]],
    contracts: list[dict[str, str]],
    scores: list[dict[str, str]],
    decisions: list[dict[str, str]],
    values: dict[str, float | None],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    derivation_cover = {"SSD3153_0_split", "SSD3153_3_source_support_sublemma", "SSD3153_4_levelset_rejection", "SSD3153_6_reduced_bound"}.issubset(
        {row["derivation_id"] for row in derivations}
    )
    levelset_rejected = any(row["gate_id"] == "G3153_3_full_levelset" and row["status"] == "fail_for_claim" for row in gates)
    physical_components = {"PDC3153_3_metric_multipole_tidal", "PDC3153_4_reference_readout", "PDC3153_5_em_flux_constitutive", "PDC3153_6_reduced_total"}.issubset(
        {row["component_id"] for row in drift}
    )
    contract_cover = {"RBC3153_0_LW_phys", "RBC3153_1_B_phys", "RBC3153_3_single_cap", "RBC3153_5_poynting"}.issubset(
        {row["contract_id"] for row in contracts}
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
    active_retained = any(row["score_id"] == "SC3153_0_current_active" and row["result"] == "above_threshold_pressure_retained" for row in scores)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for collection in [derivations, gates, drift, contracts, scores, decisions]
        for row in collection
    )
    return [
        {
            "check_id": "V3153_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3153_1_split_and_rejection_present",
            "status": "pass" if derivation_cover and levelset_rejected else "fail",
            "details": json.dumps([row["derivation_id"] for row in derivations], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3153_2_physical_drift_components_retained",
            "status": "pass" if physical_components else "fail",
            "details": json.dumps([row["component_id"] for row in drift], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3153_3_reduced_contract_and_caps",
            "status": "pass" if contract_cover and caps_positive else "fail",
            "details": json.dumps({key: fmt(values[key]) for key in values if "cap" in key}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3153_4_active_pressure_retained",
            "status": "pass" if active_retained else "fail",
            "details": "source support reduces the target but does not claim local closure",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3153_5_no_claim_leak",
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
    drift = drift_rows()
    contracts = contract_rows(values)
    scores = score_rows(values)
    decisions = decision_rows()
    validations = validation_rows(inputs, derivations, gates, drift, contracts, scores, decisions, values)
    write_csv(INPUTS, inputs)
    write_csv(DERIVATION, derivations)
    write_csv(GATES, gates)
    write_csv(DRIFT, drift)
    write_csv(CONTRACT, contracts)
    write_csv(SCORES, scores)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
