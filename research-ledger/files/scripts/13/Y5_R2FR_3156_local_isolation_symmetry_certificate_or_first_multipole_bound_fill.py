from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3156_INPUTS.csv"
CERTIFICATE = OUT / "P8_Y5_R2FR_3156_ISOLATION_SYMMETRY_CERTIFICATE.csv"
GATES = OUT / "P8_Y5_R2FR_3156_ISOLATION_GATE_STATUS.csv"
CAPS = OUT / "P8_Y5_R2FR_3156_FIRST_MULTIPOLE_CAP_CONTRACT.csv"
SCORES = OUT / "P8_Y5_R2FR_3156_SCORE_IMPACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3156_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3156_VALIDATION.csv"


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
            "source_id": "SRC3156_0_3155_doc",
            "path": source_path("3155-Y5-R2FR-Bmetric-monopole-tidal-zero-or-first-bound-row-under-AX1090.md"),
            "role": "handoff requiring isolation/symmetry certificate or first multipole/tide bound fill",
        },
        {
            "source_id": "SRC3156_1_3155_theorem",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3155_MONOPOLE_SYMMETRY_THEOREM.csv"),
            "role": "SO(3) zero theorem and strict hypotheses",
        },
        {
            "source_id": "SRC3156_2_3155_bounds",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3155_MULTIPOLE_TIDAL_BOUND_ROWS.csv"),
            "role": "first multipole/tide/spin/shape bound rows",
        },
        {
            "source_id": "SRC3156_3_3108_Gauss",
            "path": source_path("3108-Y5-R2FR-source-charge-Gauss-bridge-or-GM-calibration-residual-under-AX1090.md"),
            "role": "Poisson/Gauss exterior monopole and multipole correction structure",
        },
        {
            "source_id": "SRC3156_4_3109_worldtube",
            "path": source_path("3109-Y5-R2FR-Hilbert-worldtube-source-mass-lock-or-DeltaGM-residual-row-under-AX1090.md"),
            "role": "compact source worldtube and public Hamiltonian source lock",
        },
        {
            "source_id": "SRC3156_5_3111_Eres",
            "path": source_path("3111-Y5-R2FR-Eres-zero-through-PPN-order-or-component-bound-priority-under-AX1090.md"),
            "role": "E_res PPN component priority and boundary/reference residual caveats",
        },
        {
            "source_id": "SRC3156_6_3154_components",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3154_BPHYS_COMPONENT_BOUND_ROWS.csv"),
            "role": "B_phys component cap inheritance",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def cap_values() -> dict[str, float | None]:
    bounds = read_csv(OUT / "P8_Y5_R2FR_3155_MULTIPOLE_TIDAL_BOUND_ROWS.csv")
    scores = read_csv(OUT / "P8_Y5_R2FR_3155_SCORE_IMPACT.csv")
    total = find_row(bounds, "bound_id", "MB3155_5_Bmetric_total")
    active = find_row(scores, "score_id", "SC3155_0_current_active")
    conditional = find_row(scores, "score_id", "SC3155_3_if_all_surface_terms_zero")
    return {
        "single_coeff_cap": parse_float(total.get("coefficient_cap_if_single")) if total else None,
        "equal_coeff_cap": parse_float(total.get("coefficient_cap_equal_split")) if total else None,
        "active_coeff": parse_float(active.get("coefficient_abs")) if active else None,
        "active_threshold": parse_float(active.get("threshold_abs")) if active else None,
        "active_eta": parse_float(active.get("eta_abs")) if active else None,
        "active_eta_bound": parse_float(active.get("eta_bound")) if active else None,
        "conditional_coeff": parse_float(conditional.get("coefficient_abs")) if conditional else None,
        "conditional_eta": parse_float(conditional.get("eta_abs")) if conditional else None,
    }


def certificate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "certificate_id": "ISC3156_0_source_worldtube",
            "clause": "fixed compact Hilbert source worldtube",
            "required_condition": "W_source=closure(supp T_H[tau_pub]) is selected before readout/fitting",
            "effect_if_signed": "prevents post-readout source masks and fixes the center/source support for multipole language",
            "current_status": "not_parent_signed",
            "missing_input": "parent source/worldtube selector and same-frame Hilbert stress profile",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "certificate_id": "ISC3156_1_public_exterior",
            "clause": "public EH/Poisson exterior branch",
            "required_condition": "outside W_source, the public local branch has E_res=0 or bounded below target through the exterior annulus",
            "effect_if_signed": "lets the exterior metric/coframe be controlled by the public monopole/multipole expansion",
            "current_status": "not_parent_signed",
            "missing_input": "E_res and boundary/reference silence through the local annulus",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "certificate_id": "ISC3156_2_SO3_source",
            "clause": "SO(3)-invariant stationary source and exterior",
            "required_condition": "Lie_K T_H=0 and Lie_K g_pub=0 for all K in so(3), with K spanning tangent directions on S_R",
            "effect_if_signed": "activates the 3155 theorem B_metric_multipole_tidal=0",
            "current_status": "not_parent_signed",
            "missing_input": "source stress profile and exterior symmetry proof",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "certificate_id": "ISC3156_3_orbit_sphere",
            "clause": "chosen boundary surface is a symmetry sphere",
            "required_condition": "S=S_R is an SO(3) orbit sphere in the public geometry, not an arbitrary readout or calibration surface",
            "effect_if_signed": "ensures tangent derivatives are generated by Killing directions",
            "current_status": "not_parent_signed",
            "missing_input": "same surface S used by Wbar, Lambda, source worldtube and local readout",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "certificate_id": "ISC3156_4_no_tide_spin_radiation",
            "clause": "no external tide, spin/current multipole, radiation or nonspherical binding drift",
            "required_condition": "E_ext=0, J_source=0, radiation_flux=0, anisotropic binding component=0",
            "effect_if_signed": "removes the finite MB3155 fallback channels",
            "current_status": "not_parent_signed",
            "missing_input": "isolation, staticity, no-radiation and source anisotropy certificates",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "certificate_id": "ISC3156_5_verdict",
            "clause": "exact metric boundary-drift zero certificate",
            "required_condition": "ISC3156_0 through ISC3156_4 all signed by the same parent/readout domain",
            "effect_if_signed": "B_metric_multipole_tidal=0 for this branch only",
            "current_status": "fail_for_current_claim",
            "missing_input": "all clauses are not jointly signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "G3156_0_certificate_written",
            "gate": "isolation/symmetry certificate clauses are explicit",
            "status": "pass_nonclaim",
            "reason": "3156 lists exact parent-signature requirements for B_metric=0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3156_1_joint_parent_signature",
            "gate": "all certificate clauses are signed by one parent/readout domain",
            "status": "fail_for_claim",
            "reason": "source worldtube, E_res silence, SO(3) source, symmetry sphere and no-tide/spin/radiation are not jointly signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3156_2_cap_algebra_ready",
            "gate": "first multipole/tide cap algebra is written",
            "status": "pass_nonclaim",
            "reason": "J2, tidal, spin and normalized component caps are symbolically targetable",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3156_3_numeric_values_filled",
            "gate": "real source/domain numeric values are present",
            "status": "fail_for_claim",
            "reason": "L_W Lambda, R, M, J2, E_ext, spin and source profile values are not filled",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def cap_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    single = fmt(values["single_coeff_cap"])
    equal = fmt(values["equal_coeff_cap"])
    return [
        {
            "cap_id": "MFC3156_0_product_gate",
            "quantity": "metric_component_product",
            "formula_single_cap": "L_Wphys_Lambda * B_metric <= " + single,
            "formula_equal_split_cap": "L_Wphys_Lambda * B_metric <= " + equal,
            "normalized_bound_single": "B_metric <= " + single + "/L_Wphys_Lambda",
            "normalized_bound_equal": "B_metric <= " + equal + "/L_Wphys_Lambda",
            "missing_inputs": "L_Wphys_Lambda := L_W_phys ||Lambda||_*",
            "status": "symbolic_cap_ready_numeric_inputs_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "cap_id": "MFC3156_1_J2_mass_quadrupole",
            "quantity": "abs_J2_or_l2_mass_multipole",
            "formula_single_cap": "|J2| <= " + single + "/(L_Wphys_Lambda*C2*epsilon_G*(R_body/R)^2)",
            "formula_equal_split_cap": "|J2| <= " + equal + "/(L_Wphys_Lambda*C2*epsilon_G*(R_body/R)^2)",
            "normalized_bound_single": "epsilon_G:=G*M/(c^2*R); C2:=angular_norm_factor_for_P2",
            "normalized_bound_equal": "valid for weak-field exterior quadrupole term Phi_J2~GM/R*J2*(R_body/R)^2 P2",
            "missing_inputs": "M; R; R_body; J2 or quadrupole moment; C2; L_Wphys_Lambda",
            "status": "symbolic_cap_ready_numeric_inputs_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "cap_id": "MFC3156_2_external_tide",
            "quantity": "external_tidal_tensor_norm",
            "formula_single_cap": "||E_ext|| <= " + single + "*c^2/(L_Wphys_Lambda*C_tide*R^2)",
            "formula_equal_split_cap": "||E_ext|| <= " + equal + "*c^2/(L_Wphys_Lambda*C_tide*R^2)",
            "normalized_bound_single": "B_tide <= L_Wphys_Lambda*C_tide*||E_ext||*R^2/c^2",
            "normalized_bound_equal": "E_ext is the electric Weyl/Newtonian tidal tensor in the local public frame",
            "missing_inputs": "E_ext; R; C_tide; L_Wphys_Lambda; frame convention",
            "status": "symbolic_cap_ready_numeric_inputs_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "cap_id": "MFC3156_3_spin",
            "quantity": "source_angular_momentum_norm",
            "formula_single_cap": "|J| <= " + single + "*c^3*R^2/(L_Wphys_Lambda*C_spin*G)",
            "formula_equal_split_cap": "|J| <= " + equal + "*c^3*R^2/(L_Wphys_Lambda*C_spin*G)",
            "normalized_bound_single": "B_spin <= L_Wphys_Lambda*C_spin*G|J|/(c^3 R^2)",
            "normalized_bound_equal": "applies to leading frame-drag/current-multipole boundary drift",
            "missing_inputs": "J; R; C_spin; L_Wphys_Lambda; public g0i convention",
            "status": "symbolic_cap_ready_numeric_inputs_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "cap_id": "MFC3156_4_first_fill_priority",
            "quantity": "first_numeric_target_choice",
            "formula_single_cap": "choose J2/mass_multipole first if source is nearly isolated; choose E_ext first if external environment dominates",
            "formula_equal_split_cap": "do not combine values until L_Wphys_Lambda and same S/norm convention are fixed",
            "normalized_bound_single": "priority: source_domain -> R -> L_Wphys_Lambda -> J2/E_ext",
            "normalized_bound_equal": "all rows remain valid_for_claim=false until source-backed values are inserted",
            "missing_inputs": "source/domain selection and numeric/source-backed factors",
            "status": "decision_contract_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def score_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "score_id": "SC3156_0_current_active",
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
            "score_id": "SC3156_1_if_certificate_signed",
            "scenario": "B_metric zero by exact isolation/symmetry certificate",
            "coefficient_abs": "metric_component_removed_only",
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "not_full_score_because_other_Bphys_and_Lambda_terms_remain",
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "useful_but_not_full_pass",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3156_2_if_first_multipole_under_cap",
            "scenario": "first multipole/tide component below product-adjusted cap",
            "coefficient_abs": "<= " + fmt(values["single_coeff_cap"]),
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "component_cap_only_not_total_eta",
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "component_acceptable_only_after_LW_Lambda_and_siblings_are_handled",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3156_3_if_all_surface_terms_zero",
            "scenario": "Coulomb-only conditional inherited from 3155",
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
            "decision_id": "D3156_0_certificate",
            "decision": "exact isolation/symmetry certificate is now explicit but not parent-signed",
            "effect": "B_metric zero is available as a precise theorem route, not a generic vacuum shortcut",
            "next_action": "sign source worldtube, SO(3) source, symmetry sphere and no tide/spin/radiation clauses or use finite rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3156_1_bound_contract",
            "decision": "first multipole/tide caps are symbolically targetable",
            "effect": "numeric fill now knows what source/domain values are required and how caps scale with L_Wphys_Lambda",
            "next_action": "choose a concrete source/domain and fill J2 or E_ext only with source-backed values",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3156_2_next",
            "decision": "next target should select the first fill domain or attack L_Wphys_Lambda",
            "effect": "without L_Wphys_Lambda, multipole/tide caps remain symbolic; without a source domain, numeric values would be fake",
            "next_action": "3157-Y5-R2FR-LWlambda-factor-or-first-source-domain-multipole-fill",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    certificate: list[dict[str, str]],
    gates: list[dict[str, str]],
    caps: list[dict[str, str]],
    scores: list[dict[str, str]],
    decisions: list[dict[str, str]],
    values: dict[str, float | None],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    certificate_cover = {"ISC3156_0_source_worldtube", "ISC3156_2_SO3_source", "ISC3156_4_no_tide_spin_radiation", "ISC3156_5_verdict"}.issubset(
        {row["certificate_id"] for row in certificate}
    )
    certificate_blocks = any(row["certificate_id"] == "ISC3156_5_verdict" and row["current_status"] == "fail_for_current_claim" for row in certificate)
    gate_blocks = any(row["gate_id"] == "G3156_1_joint_parent_signature" and row["status"] == "fail_for_claim" for row in gates)
    cap_cover = {"MFC3156_0_product_gate", "MFC3156_1_J2_mass_quadrupole", "MFC3156_2_external_tide", "MFC3156_3_spin"}.issubset(
        {row["cap_id"] for row in caps}
    )
    caps_positive = all(
        values[key] is not None and values[key] > 0
        for key in ["single_coeff_cap", "equal_coeff_cap"]
    )
    active_retained = any(row["score_id"] == "SC3156_0_current_active" and row["result"] == "above_threshold_pressure_retained" for row in scores)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for collection in [certificate, gates, caps, scores, decisions]
        for row in collection
    )
    return [
        {
            "check_id": "V3156_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3156_1_certificate_explicit_and_blocked",
            "status": "pass" if certificate_cover and certificate_blocks and gate_blocks else "fail",
            "details": json.dumps({row["certificate_id"]: row["current_status"] for row in certificate}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3156_2_cap_contracts_present",
            "status": "pass" if cap_cover and caps_positive else "fail",
            "details": json.dumps({key: fmt(values[key]) for key in values if "cap" in key}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3156_3_numeric_fill_still_blocked",
            "status": "pass" if any(row["gate_id"] == "G3156_3_numeric_values_filled" and row["status"] == "fail_for_claim" for row in gates) else "fail",
            "details": "symbolic caps only; no fake J2/E_ext values",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3156_4_active_pressure_retained",
            "status": "pass" if active_retained else "fail",
            "details": "3156 does not claim local closure or local GR",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3156_5_no_claim_leak",
            "status": "pass" if all_nonclaim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    values = cap_values()
    certificate = certificate_rows()
    gates = gate_rows()
    caps = cap_rows(values)
    scores = score_rows(values)
    decisions = decision_rows()
    validations = validation_rows(inputs, certificate, gates, caps, scores, decisions, values)
    write_csv(INPUTS, inputs)
    write_csv(CERTIFICATE, certificate)
    write_csv(GATES, gates)
    write_csv(CAPS, caps)
    write_csv(SCORES, scores)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
