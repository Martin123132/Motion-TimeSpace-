from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3155_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3155_MONOPOLE_SYMMETRY_THEOREM.csv"
GATES = OUT / "P8_Y5_R2FR_3155_METRIC_DRIFT_GATE_STATUS.csv"
BOUNDS = OUT / "P8_Y5_R2FR_3155_MULTIPOLE_TIDAL_BOUND_ROWS.csv"
SCORES = OUT / "P8_Y5_R2FR_3155_SCORE_IMPACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3155_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3155_VALIDATION.csv"


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
            "source_id": "SRC3155_0_3154_doc",
            "path": source_path("3154-Y5-R2FR-Wbar-basic-quotient-theorem-or-Bphys-first-component-bound-under-AX1090.md"),
            "role": "handoff requiring B_metric_multipole_tidal theorem or first bound row",
        },
        {
            "source_id": "SRC3155_1_3154_components",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3154_BPHYS_COMPONENT_BOUND_ROWS.csv"),
            "role": "B_metric_multipole_tidal row and caps",
        },
        {
            "source_id": "SRC3155_2_3154_theorem",
            "path": source_path("source-intake/mts_residuals/P8_Y5_R2FR_3154_WBAR_BASIC_QUOTIENT_THEOREM.csv"),
            "role": "quotient-basic/gauge removal theorem",
        },
        {
            "source_id": "SRC3155_3_3104_EH_Newton",
            "path": source_path("3104-Y5-R2FR-left-hand-EH-Newton-reduction-under-quotient-matter-domain.md"),
            "role": "public EH/Newton branch and residual caveats",
        },
        {
            "source_id": "SRC3155_4_3108_Gauss",
            "path": source_path("3108-Y5-R2FR-source-charge-Gauss-bridge-or-GM-calibration-residual-under-AX1090.md"),
            "role": "Poisson/Gauss bridge and multipole residual rows",
        },
        {
            "source_id": "SRC3155_5_3110_PPN",
            "path": source_path("3110-Y5-R2FR-local-PPN-residual-vector-from-Eres-and-RHsrc-under-AX1090.md"),
            "role": "PPN residual vector",
        },
        {
            "source_id": "SRC3155_6_3111_Eres",
            "path": source_path("3111-Y5-R2FR-Eres-zero-through-PPN-order-or-component-bound-priority-under-AX1090.md"),
            "role": "E_res PPN component priority",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def cap_values() -> dict[str, float | None]:
    components = read_csv(OUT / "P8_Y5_R2FR_3154_BPHYS_COMPONENT_BOUND_ROWS.csv")
    scores = read_csv(OUT / "P8_Y5_R2FR_3154_REDUCED_SCORECARD.csv")
    metric = find_row(components, "component_id", "BPC3154_0_B_metric_multipole_tidal")
    active = find_row(scores, "score_id", "SC3154_0_current_active")
    conditional = find_row(scores, "score_id", "SC3154_3_if_all_surface_terms_zero")
    return {
        "metric_single_coeff_cap": parse_float(metric.get("coefficient_cap_if_single")) if metric else None,
        "metric_equal_coeff_cap": parse_float(metric.get("coefficient_cap_equal_split")) if metric else None,
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
            "theorem_id": "MST3155_0_metric_boundary_object",
            "object": "z_metric",
            "statement": "The metric/coframe physical boundary datum is the public geometry restricted to S after quotienting coordinate/frame gauge.",
            "formula": "z_metric := [g_pub,e_pub,mu_obs]|S / (Diff(S) x SO(1,3)_S)",
            "proof_content": "3154 removes pure boundary gauge; what remains is physical geometry on S.",
            "status": "definition_shape",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MST3155_1_SO3_symmetry_zero",
            "object": "B_metric_multipole_tidal",
            "statement": "If S is an SO(3) orbit sphere and the public exterior geometry is stationary spherical monopole data, then tangential physical metric drift vanishes.",
            "formula": "Lie_K z_metric=0 for all K in so(3) spanning TS => P_phys d_S z_metric=0",
            "proof_content": "Each tangent direction on a round symmetry sphere is generated by an SO(3) Killing field. Invariance makes the derivative along every tangent generator zero after quotienting coordinate/frame gauge.",
            "status": "conditional_math_theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MST3155_2_monopole_conditions",
            "object": "exact zero hypotheses",
            "statement": "The zero theorem requires exact symmetry, not just vacuum.",
            "formula": "B_metric=0 if stationary + spherical + no spin/tide/radiation + S=S_R symmetry sphere + fixed public geometry",
            "proof_content": "Vacuum with quadrupoles, external tides, spin, radiation, or nonspherical binding fields can still have tangential physical drift.",
            "status": "strict_conditions_listed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MST3155_3_weak_field_fallback",
            "object": "finite multipole/tidal bound",
            "statement": "If exact symmetry fails, the first finite row is a weak-field boundary-gradient norm of multipole, tide, spin and shape terms.",
            "formula": "B_metric <= sup_S(|grad_S Phi_multi|+|grad_S Psi_multi|)/c^2 + B_tide + B_spin + B_shape + B_binding",
            "proof_content": "This follows by writing the weak-field public geometry in potentials and retaining tangential physical gradients on S.",
            "status": "bound_shape_ready_inputs_missing",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "MST3155_4_scope_guard",
            "object": "local GR/Newton status",
            "statement": "The monopole theorem zeros one boundary-drift component only; it does not prove EH, source transfer, PPN, or local-GR recovery.",
            "formula": "B_metric=0 does not imply E_res=0, B_reference=0, B_EM=0, B_harmonic=0, or GM transfer",
            "proof_content": "3104/3108/3111 still supply the wider local-GR requirements.",
            "status": "guard_active",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "G3155_0_SO3_theorem_shape",
            "gate": "SO(3) orbit-sphere tangential zero theorem written",
            "status": "pass_conditional_math",
            "reason": "Killing fields spanning TS annihilate invariant z_metric",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3155_1_current_source_is_exact_monopole",
            "gate": "actual local source/domain is exact stationary spherical monopole",
            "status": "fail_for_claim",
            "reason": "current branch has not parent-signed exact spherical source, no external tide, no spin, and symmetry-sphere S",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3155_2_no_tide_spin_radiation",
            "gate": "external tides, spin/frame dragging, radiation and nonspherical binding are zero",
            "status": "fail_for_claim",
            "reason": "these are physical finite components until a theorem or source row removes them",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3155_3_first_bound_rows_ready",
            "gate": "multipole/tidal bound rows are source-ready",
            "status": "pass_nonclaim",
            "reason": "component formulas, units and required sources are staged",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3155_4_no_local_GR_promotion",
            "gate": "local-GR/Newton claim remains blocked",
            "status": "pass_nonclaim",
            "reason": "metric boundary drift is only one component of the local closure problem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def bound_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    single = fmt(values["metric_single_coeff_cap"])
    equal = fmt(values["metric_equal_coeff_cap"])
    return [
        {
            "bound_id": "MB3155_0_exact_monopole_zero",
            "quantity": "B_metric_multipole_tidal",
            "component": "exact_stationary_spherical_monopole",
            "formula": "B_metric=0",
            "units": "dimensionless_boundary_drift_norm",
            "numeric_value": "THEOREM_ZERO_IF_ALL_MONOPOLE_GATES_PASS",
            "coefficient_cap_if_single": single,
            "coefficient_cap_equal_split": equal,
            "required_source": "SO3 symmetry of public geometry; S is an orbit sphere; no tides/spin/radiation; fixed quotient gauge",
            "status": "conditional_zero_not_current_claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "MB3155_1_mass_multipoles",
            "quantity": "B_mass_multipoles",
            "component": "l>=2 mass multipoles including quadrupole/J2",
            "formula": "B_mass_multi <= sup_S |grad_S Phi_l>=2|/c^2; for one l term scales like C_l |Phi_l(R)|/c^2",
            "units": "dimensionless_boundary_drift_norm",
            "numeric_value": "MISSING_MULTIPOLE_PROFILE_OR_ZERO_SYMMETRY",
            "coefficient_cap_if_single": single,
            "coefficient_cap_equal_split": equal,
            "required_source": "source multipole moments or public weak-field potential on S; radius R; norm convention",
            "status": "source_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "MB3155_2_external_tide",
            "quantity": "B_external_tide",
            "component": "external tidal field",
            "formula": "B_tide <= C_tide ||E_ij|| R^2/c^2",
            "units": "dimensionless_boundary_drift_norm",
            "numeric_value": "MISSING_TIDAL_TENSOR_OR_ZERO_ISOLATION_THEOREM",
            "coefficient_cap_if_single": single,
            "coefficient_cap_equal_split": equal,
            "required_source": "external tidal tensor at source/worldtube, chosen boundary radius R, isolation assumptions",
            "status": "source_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "MB3155_3_spin_frame_drag",
            "quantity": "B_spin_frame_drag",
            "component": "spin/current multipole frame-dragging",
            "formula": "B_spin <= C_spin G|J|/(c^3 R^2) plus higher current multipoles",
            "units": "dimensionless_boundary_drift_norm",
            "numeric_value": "MISSING_SPIN_OR_ZERO_STATIC_THEOREM",
            "coefficient_cap_if_single": single,
            "coefficient_cap_equal_split": equal,
            "required_source": "source angular momentum/current multipoles, public metric g0i convention, boundary radius",
            "status": "source_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "MB3155_4_shape_binding",
            "quantity": "B_shape_binding",
            "component": "nonspherical binding or finite-shape geometry",
            "formula": "B_shape <= C_shape ||delta T_ij^anisotropic||_S/kappa-normalized + B_binding_aniso",
            "units": "dimensionless_boundary_drift_norm",
            "numeric_value": "MISSING_SHAPE_BINDING_PROFILE",
            "coefficient_cap_if_single": single,
            "coefficient_cap_equal_split": equal,
            "required_source": "anisotropic stress/binding source profile or theorem reducing it to modeled multipoles",
            "status": "source_ready_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "MB3155_5_Bmetric_total",
            "quantity": "B_metric_multipole_tidal",
            "component": "total physical metric boundary drift",
            "formula": "B_metric <= B_mass_multipoles + B_external_tide + B_spin_frame_drag + B_shape_binding + B_res_metric",
            "units": "dimensionless_boundary_drift_norm",
            "numeric_value": "MISSING_COMPONENT_SUM_OR_EXACT_ZERO",
            "coefficient_cap_if_single": single,
            "coefficient_cap_equal_split": equal,
            "required_source": "all MB3155 component values or zero theorems, plus residual metric boundary term",
            "status": "total_bound_row_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def score_rows(values: dict[str, float | None]) -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "score_id": "SC3155_0_current_active",
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
            "score_id": "SC3155_1_if_exact_monopole",
            "scenario": "B_metric_multipole_tidal theorem-zero only",
            "coefficient_abs": "metric_component_removed_only",
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "not_full_score_because_reference_EM_harmonic_Lambda_LW_remain",
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "useful_but_not_full_pass",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3155_2_if_Bmetric_under_cap",
            "scenario": "B_metric component below single-survivor cap before L_W/Lambda multiplication is resolved",
            "coefficient_abs": "<= " + fmt(values["metric_single_coeff_cap"]),
            "threshold_abs": fmt(values["active_threshold"]),
            "eta_abs": "cap_component_only_not_total_eta",
            "eta_bound": fmt(values["active_eta_bound"]),
            "result": "component_acceptable_only_after_LW_Lambda_and_siblings_are_handled",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "score_id": "SC3155_3_if_all_surface_terms_zero",
            "scenario": "Coulomb-only conditional inherited from 3154",
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
            "decision_id": "D3155_0_monopole_result",
            "decision": "exact SO(3) monopole symmetry zeros B_metric_multipole_tidal on a symmetry sphere",
            "effect": "this is a theorem route for one physical drift component",
            "next_action": "parent-sign actual source/domain as exact monopole or keep finite multipole rows",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3155_1_fallback_result",
            "decision": "generic sources require multipole/tidal/spin/shape finite rows",
            "effect": "the first metric drift fallback is now source-ready rather than vague",
            "next_action": "choose whether to attack exact local symmetry theorem or fill MB3155 component data",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3155_2_next",
            "decision": "next best target is the isolation/symmetry certificate or first real multipole bound",
            "effect": "3156 should either parent-sign exact symmetry surface conditions or source MB3155_1/MB3155_2 values",
            "next_action": "3156-Y5-R2FR-local-isolation-symmetry-certificate-or-first-multipole-bound-fill",
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
    theorem_cover = {"MST3155_1_SO3_symmetry_zero", "MST3155_3_weak_field_fallback", "MST3155_4_scope_guard"}.issubset(
        {row["theorem_id"] for row in theorem}
    )
    exact_current_blocked = any(row["gate_id"] == "G3155_1_current_source_is_exact_monopole" and row["status"] == "fail_for_claim" for row in gates)
    bound_cover = {"MB3155_0_exact_monopole_zero", "MB3155_1_mass_multipoles", "MB3155_2_external_tide", "MB3155_5_Bmetric_total"}.issubset(
        {row["bound_id"] for row in bounds}
    )
    caps_positive = all(
        values[key] is not None and values[key] > 0
        for key in ["metric_single_coeff_cap", "metric_equal_coeff_cap"]
    )
    active_retained = any(row["score_id"] == "SC3155_0_current_active" and row["result"] == "above_threshold_pressure_retained" for row in scores)
    all_nonclaim = all(
        row.get("valid_for_claim") == "false"
        for collection in [theorem, gates, bounds, scores, decisions]
        for row in collection
    )
    return [
        {
            "check_id": "V3155_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3155_1_monopole_theorem_and_scope_guard",
            "status": "pass" if theorem_cover else "fail",
            "details": json.dumps([row["theorem_id"] for row in theorem], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3155_2_current_exact_monopole_not_claimed",
            "status": "pass" if exact_current_blocked else "fail",
            "details": json.dumps({row["gate_id"]: row["status"] for row in gates}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3155_3_bound_rows_and_caps",
            "status": "pass" if bound_cover and caps_positive else "fail",
            "details": json.dumps({key: fmt(values[key]) for key in values if "cap" in key}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3155_4_active_pressure_retained",
            "status": "pass" if active_retained else "fail",
            "details": "B_metric theorem/bounds affect only one physical drift component",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3155_5_no_claim_leak",
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
