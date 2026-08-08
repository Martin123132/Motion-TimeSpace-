from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3157_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3157_LWLAMBDA_CONTROL_THEOREM.csv"
GATES = OUT / "P8_Y5_R2FR_3157_LWLAMBDA_GATE_STATUS.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3157_LWLAMBDA_PRODUCT_CONTRACT.csv"
REVERSE = OUT / "P8_Y5_R2FR_3157_REVERSE_SOURCE_CAPS.csv"
SCORES = OUT / "P8_Y5_R2FR_3157_SCORE_IMPACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3157_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3157_VALIDATION.csv"


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
            "source_id": "SRC3157_0_3156_doc",
            "path": source_path("3156-Y5-R2FR-local-isolation-symmetry-certificate-or-first-multipole-bound-fill-under-AX1090.md"),
            "role": "handoff requiring L_Wphys_Lambda or first source-domain multipole fill",
        },
        {
            "source_id": "SRC3157_1_3156_caps",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3156_FIRST_MULTIPOLE_CAP_CONTRACT.csv"),
            "role": "symbolic J2/tide/spin cap algebra",
        },
        {
            "source_id": "SRC3157_2_3153_reduced",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3153_REDUCED_BOUND_CONTRACT.csv"),
            "role": "L_W_phys, B_phys and Lambda product target",
        },
        {
            "source_id": "SRC3157_3_3152_factors",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3152_DERIVATIVE_NORM_FACTORIZATION.csv"),
            "role": "original L_W, B_z and Lambda factor rows",
        },
        {
            "source_id": "SRC3157_4_3154_basicness",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3154_WBAR_BASIC_QUOTIENT_THEOREM.csv"),
            "role": "Wbar quotient-basic theorem and physical drift guard",
        },
        {
            "source_id": "SRC3157_5_3155_bounds",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3155_MULTIPOLE_TIDAL_BOUND_ROWS.csv"),
            "role": "B_metric component rows",
        },
        {
            "source_id": "SRC3157_6_3108_Gauss",
            "path": source_path("3108-Y5-R2FR-source-charge-Gauss-bridge-or-GM-calibration-residual-under-AX1090.md"),
            "role": "source-domain and multipole correction structure",
        },
        {
            "source_id": "SRC3157_7_3111_Eres",
            "path": source_path("3111-Y5-R2FR-Eres-zero-through-PPN-order-or-component-bound-priority-under-AX1090.md"),
            "role": "boundary/reference and residual caveats",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def cap_values() -> dict[str, float | None]:
    caps = read_csv(OUT / "P8_Y5_R2FR_3156_FIRST_MULTIPOLE_CAP_CONTRACT.csv")
    scores = read_csv(OUT / "P8_Y5_R2FR_3156_SCORE_IMPACT.csv")
    product = find_row(caps, "cap_id", "MFC3156_0_product_gate")
    active = find_row(scores, "score_id", "SC3156_0_current_active")
    conditional = find_row(scores, "score_id", "SC3156_3_if_all_surface_terms_zero")
    single = None
    equal = None
    if product:
        single_text = product.get("formula_single_cap", "")
        equal_text = product.get("formula_equal_split_cap", "")
        single = parse_float(single_text.split("<=")[-1].strip()) if "<=" in single_text else None
        equal = parse_float(equal_text.split("<=")[-1].strip()) if "<=" in equal_text else None
    return {
        "single_coeff_cap": single,
        "equal_coeff_cap": equal,
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
            "theorem_id": "LWT3157_0_invariant_product",
            "object": "L_Wphys_Lambda",
            "statement": "The product L_W_phys ||Lambda||_* is the norm-invariant control object; rescaling the boundary norm only moves size between the two factors.",
            "formula": "if ||.|| -> a||.||, then L_W_phys -> L_W_phys/a and ||Lambda||_* -> a||Lambda||_*",
            "proof_content": "Dual norm scaling cancels in L_W_phys ||Lambda||_*, so the product cannot be set small by convention.",
            "status": "exact_norm_scaling_guard",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "LWT3157_1_kernel_zero_route",
            "object": "L_W_phys",
            "statement": "If Wbar annihilates physical boundary drift, then L_W_phys=0 and the metric multipole/tide product vanishes.",
            "formula": "D_z Wbar P_phys=0 => L_Wphys_Lambda=0",
            "proof_content": "This is stronger than 3154's pure-gauge annihilator and would require physical-drift blindness, not merely quotient gauge basicness.",
            "status": "conditional_not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "LWT3157_2_primitive_zero_route",
            "object": "Lambda",
            "statement": "If the exact primitive part of the boundary surface term is killed by the parent boundary condition, then ||Lambda||_*=0.",
            "formula": "Lambda=0 in B_surf=d_S Lambda+h+r => L_Wphys_Lambda=0",
            "proof_content": "This would zero the derivative product, but corner/harmonic/residual siblings still need separate handling.",
            "status": "conditional_not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "LWT3157_3_Hodge_Poincare_bound",
            "object": "Lambda",
            "statement": "If the boundary complex, gauge condition and relative cohomology class are parent-owned, a Hodge/Poincare estimate can bound the primitive norm.",
            "formula": "||Lambda||_* <= C_Hodge(S,norm,boundary_condition) ||B_exact||_*",
            "proof_content": "This is the honest finite route: a domain constant, exact-surface norm and cohomology/corner policy are required.",
            "status": "bound_shape_ready_inputs_missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "LWT3157_4_product_bound",
            "object": "L_Wphys_Lambda",
            "statement": "The first source-domain multipole fill should use either a direct product value or the factorized bound L_W_phys C_Hodge ||B_exact||.",
            "formula": "L_Wphys_Lambda <= L_W_phys C_Hodge ||B_exact||_*",
            "proof_content": "This turns the missing product into source/domain factors rather than a free multiplier.",
            "status": "product_contract_ready_inputs_missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "G3157_0_norm_scaling_guard",
            "gate": "L_Wphys_Lambda cannot be reduced by norm convention",
            "status": "pass_nonclaim",
            "reason": "dual norm scaling leaves the product invariant",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3157_1_kernel_zero",
            "gate": "D_z Wbar annihilates physical drift",
            "status": "fail_for_claim",
            "reason": "3154 only handles pure gauge drift; physical multipole/reference/EM drift is retained",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3157_2_Lambda_zero",
            "gate": "Lambda primitive is theorem-zero",
            "status": "fail_for_claim",
            "reason": "no parent boundary condition kills the exact primitive part while preserving physical charges",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3157_3_Hodge_bound_inputs",
            "gate": "C_Hodge, B_exact norm and cohomology/corner policy are sourced",
            "status": "fail_for_claim",
            "reason": "domain geometry and primitive norm constants remain missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3157_4_reverse_caps_ready",
            "gate": "reverse caps for L_Wphys_Lambda are written for J2/tide/spin fills",
            "status": "pass_nonclaim",
            "reason": "source-domain values can now be tested against product caps without inventing the product",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def contract_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    single = fmt(values["single_coeff_cap"])
    equal = fmt(values["equal_coeff_cap"])
    return [
        {
            "contract_id": "LPC3157_0_direct_product",
            "quantity": "L_Wphys_Lambda",
            "definition": "direct product of physical kernel sensitivity and primitive norm",
            "formula": "L_Wphys_Lambda := L_W_phys ||Lambda||_*",
            "numeric_value": "MISSING_DIRECT_PRODUCT_OR_ZERO_THEOREM",
            "cap_relevance": "source component passes if L_Wphys_Lambda * B_component <= cap",
            "single_cap": single,
            "equal_split_cap": equal,
            "required_source": "parent Wbar/P_phys derivative norm; same boundary norm; primitive norm Lambda",
            "status": "missing_parent_input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "LPC3157_1_factorized_bound",
            "quantity": "L_W_phys_C_Hodge_Bexact",
            "definition": "finite bound for L_Wphys_Lambda using a Hodge/Poincare primitive estimate",
            "formula": "L_Wphys_Lambda <= L_W_phys C_Hodge ||B_exact||_*",
            "numeric_value": "MISSING_FACTOR_VALUES",
            "cap_relevance": "sufficient condition if L_W_phys C_Hodge ||B_exact||_* B_component <= cap",
            "single_cap": single,
            "equal_split_cap": equal,
            "required_source": "L_W_phys; C_Hodge; exact boundary surface norm; harmonic/corner policy",
            "status": "symbolic_bound_ready_numeric_inputs_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "LPC3157_2_source_domain_first",
            "quantity": "source_domain_selection",
            "definition": "concrete domain needed before inserting J2, E_ext, spin or shape values",
            "formula": "domain := {source, W_source, S_R, R, norm, frame, readout}",
            "numeric_value": "MISSING_DOMAIN_SELECTION",
            "cap_relevance": "without a domain, source values are not physically meaningful",
            "single_cap": single,
            "equal_split_cap": equal,
            "required_source": "domain id and provenance for every geometric/source quantity",
            "status": "missing_domain_input",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def reverse_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    single = fmt(values["single_coeff_cap"])
    equal = fmt(values["equal_coeff_cap"])
    return [
        {
            "reverse_id": "RSC3157_0_generic_component",
            "component": "generic_B_component",
            "reverse_single_cap": "L_Wphys_Lambda <= " + single + "/B_component",
            "reverse_equal_cap": "L_Wphys_Lambda <= " + equal + "/B_component",
            "use": "after a source-domain value B_component is filled, this tests how small the product must be",
            "missing_inputs": "B_component numeric value",
            "status": "symbolic_reverse_cap_ready",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "reverse_id": "RSC3157_1_J2",
            "component": "J2_mass_quadrupole",
            "reverse_single_cap": "L_Wphys_Lambda <= " + single + "/(C2*epsilon_G*(R_body/R)^2*|J2|)",
            "reverse_equal_cap": "L_Wphys_Lambda <= " + equal + "/(C2*epsilon_G*(R_body/R)^2*|J2|)",
            "use": "if J2/domain is sourced before product, this is the required product ceiling",
            "missing_inputs": "C2; epsilon_G; R_body/R; J2; source/domain provenance",
            "status": "symbolic_reverse_cap_ready",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "reverse_id": "RSC3157_2_external_tide",
            "component": "external_tide",
            "reverse_single_cap": "L_Wphys_Lambda <= " + single + "*c^2/(C_tide*||E_ext||*R^2)",
            "reverse_equal_cap": "L_Wphys_Lambda <= " + equal + "*c^2/(C_tide*||E_ext||*R^2)",
            "use": "if tidal tensor/domain is sourced first, this is the required product ceiling",
            "missing_inputs": "C_tide; E_ext; R; frame convention; source/domain provenance",
            "status": "symbolic_reverse_cap_ready",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "reverse_id": "RSC3157_3_spin",
            "component": "spin_frame_drag",
            "reverse_single_cap": "L_Wphys_Lambda <= " + single + "*c^3*R^2/(C_spin*G*|J|)",
            "reverse_equal_cap": "L_Wphys_Lambda <= " + equal + "*c^3*R^2/(C_spin*G*|J|)",
            "use": "if spin/domain is sourced first, this is the required product ceiling",
            "missing_inputs": "C_spin; J; R; public g0i convention; source/domain provenance",
            "status": "symbolic_reverse_cap_ready",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def score_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "score_id": "SC3157_0_current_active",
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
            "score_id": "SC3157_1_if_LWlambda_zero",
            "scenario": "L_Wphys_Lambda theorem-zero by kernel or primitive zero",
            "coefficient_abs": "metric_derivative_component_removed_only",
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "not_full_score_because_sibling_surface_terms_remain",
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "useful_but_not_full_pass",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3157_2_if_product_bound_filled",
            "scenario": "L_Wphys_Lambda source-backed below source-component reverse cap",
            "coefficient_abs": "<= " + fmt(values["single_coeff_cap"]),
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "component_cap_only_not_total_eta",
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "component_acceptable_only_after_source_domain_and_siblings_are_handled",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3157_3_if_all_surface_terms_zero",
            "scenario": "Coulomb-only conditional inherited from 3156",
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
            "decision_id": "D3157_0_product_status",
            "decision": "L_Wphys_Lambda cannot be removed by norm choice and is not currently source-backed",
            "effect": "multipole/tide numeric fills must remain nonclaim until product or reverse cap is handled",
            "next_action": "derive kernel/primitive zero, fill Hodge/Poincare product factors, or choose a domain and compute reverse cap",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3157_1_best_next",
            "decision": "best next target is source-domain selection plus reverse-cap test, unless a parent primitive-zero theorem is visible",
            "effect": "a concrete domain makes J2/E_ext and required product ceilings comparable",
            "next_action": "3158-Y5-R2FR-first-source-domain-selection-and-reverse-cap-smoke",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    theorem: list[dict[str, str]],
    gates: list[dict[str, str]],
    contracts: list[dict[str, str]],
    reverse: list[dict[str, str]],
    scores: list[dict[str, str]],
    decisions: list[dict[str, str]],
    values: dict[str, float | None],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    theorem_cover = {"LWT3157_0_invariant_product", "LWT3157_3_Hodge_Poincare_bound", "LWT3157_4_product_bound"}.issubset(
        {row["theorem_id"] for row in theorem}
    )
    required_blocks = {"G3157_1_kernel_zero", "G3157_2_Lambda_zero", "G3157_3_Hodge_bound_inputs"}.issubset(
        {row["gate_id"] for row in gates if row["status"] == "fail_for_claim"}
    )
    contract_cover = {"LPC3157_0_direct_product", "LPC3157_1_factorized_bound", "LPC3157_2_source_domain_first"}.issubset(
        {row["contract_id"] for row in contracts}
    )
    reverse_cover = {"RSC3157_1_J2", "RSC3157_2_external_tide", "RSC3157_3_spin"}.issubset(
        {row["reverse_id"] for row in reverse}
    )
    caps_positive = all(values[key] is not None and values[key] > 0 for key in ["single_coeff_cap", "equal_coeff_cap"])
    active_retained = any(row["score_id"] == "SC3157_0_current_active" and row["result"] == "above_threshold_pressure_retained" for row in scores)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for collection in [theorem, gates, contracts, reverse, scores, decisions]
        for row in collection
    )
    return [
        {
            "check_id": "V3157_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3157_1_product_theorems_and_blocks",
            "status": "pass" if theorem_cover and required_blocks else "fail",
            "details": json.dumps({row["gate_id"]: row["status"] for row in gates}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3157_2_contract_and_reverse_caps",
            "status": "pass" if contract_cover and reverse_cover and caps_positive else "fail",
            "details": json.dumps({key: fmt(values[key]) for key in values if "cap" in key}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3157_3_no_norm_rescaling_cheat",
            "status": "pass" if any(row["gate_id"] == "G3157_0_norm_scaling_guard" and row["status"] == "pass_nonclaim" for row in gates) else "fail",
            "details": "product is invariant under dual norm scaling",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3157_4_active_pressure_retained",
            "status": "pass" if active_retained else "fail",
            "details": "3157 does not claim local closure or local GR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3157_5_no_claim_leak",
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
    contracts = contract_rows(values)
    reverse = reverse_rows(values)
    scores = score_rows(values)
    decisions = decision_rows()
    validations = validation_rows(inputs, theorem, gates, contracts, reverse, scores, decisions, values)
    write_csv(INPUTS, inputs)
    write_csv(THEOREM, theorem)
    write_csv(GATES, gates)
    write_csv(CONTRACT, contracts)
    write_csv(REVERSE, reverse)
    write_csv(SCORES, scores)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
