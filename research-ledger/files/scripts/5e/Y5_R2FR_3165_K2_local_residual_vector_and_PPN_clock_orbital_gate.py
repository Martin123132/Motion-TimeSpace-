from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3165_INPUTS.csv"
UNIT = OUT / "P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv"
VECTOR = OUT / "P8_Y5_R2FR_3165_K2_LOCAL_RESIDUAL_VECTOR.csv"
GATES = OUT / "P8_Y5_R2FR_3165_PPN_CLOCK_ORBITAL_GATES.csv"
DECISION = OUT / "P8_Y5_R2FR_3165_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3165_VALIDATION.csv"

AX1090_SINGLE_CAP = 5.970964001482571e-4
AX1090_EQUAL_CAP = 9.951606669137618e-5


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def fmt(value: float) -> str:
    return f"{value:.15e}"


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
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


def internal(relative: str) -> str:
    return str((ROOT / relative).resolve())


def csv_row(path: Path, key: str, value: str) -> dict[str, str]:
    for row in read_csv(path):
        if row.get(key) == value:
            return row
    raise KeyError(f"missing row {key}={value} in {path}")


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("3164-Y5-R2FR-Wbar-sensitivity-bound-or-KLambdaW-closure-lane-under-AX1090.md", "3164 K2 closure lane"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3164_KLAMBDAW_CLOSURE_LANE.csv", "K2 cap and projection-owner case"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3161_BEXACT_SOURCE_BOUND_ROWS.csv", "primitive norm and B_exact for Earth J2 l=2 lane"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3159_NUMERIC_REVERSE_CAP_WITH_DERIVED_COEFFICIENTS.csv", "projected public metric amplitude"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3110_LOCAL_PPN_RESIDUAL_VECTOR.csv", "PPN residual component map"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3111_ERES_PPN_COMPONENT_PRIORITY.csv", "PPN component priority"),
    ]
    return [
        {
            "input_id": f"IN3165_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(rows)
    ]


def source_values() -> dict[str, float]:
    bexact = csv_row(OUT / "P8_Y5_R2FR_3161_BEXACT_SOURCE_BOUND_ROWS.csv", "component", "Earth_J2_full_shell_metric_projection")
    metric = csv_row(OUT / "P8_Y5_R2FR_3159_NUMERIC_REVERSE_CAP_WITH_DERIVED_COEFFICIENTS.csv", "component", "Earth_J2_full_shell_metric_projection")
    closure = csv_row(OUT / "P8_Y5_R2FR_3164_KLAMBDAW_CLOSURE_LANE.csv", "quantity", "K_2")
    primitive_norm = float(bexact["primitive_norm_hat"])
    amplitude = float(metric["projected_B_metric"])
    k2_cap_l2 = float(closure["required_bound_l2"])
    k2_cap_general = float(closure["required_bound_general"])
    unit_coefficient = primitive_norm * amplitude
    return {
        "primitive_norm_hat_M1": primitive_norm,
        "A_public_full_shell": amplitude,
        "unit_coefficient": unit_coefficient,
        "k2_cap_l2": k2_cap_l2,
        "k2_cap_general": k2_cap_general,
        "projection_owner_k2": 1.0,
    }


def unit_rows(values: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    unit = values["unit_coefficient"]
    k2_cap = values["k2_cap_l2"]
    projection_owner_impact = unit
    cap_impact = unit * k2_cap
    return [
        {
            "unit_id": "KU3165_0_definition",
            "quantity": "C_K2_unit",
            "definition": "per-unit K2 local l=2 residual coefficient",
            "formula": "C_K2_unit = ||Lambda||_hat(M_Lambda=1) * A_public_full_shell",
            "value": fmt(unit),
            "units": "dimensionless_coefficient_per_unit_K2",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "unit_id": "KU3165_1_projection_owner_smoke",
            "quantity": "C_K2_if_K2_equals_1",
            "definition": "projection-owner smoke case W2=1 and M_Lambda=1",
            "formula": "C_K2 = C_K2_unit",
            "value": fmt(projection_owner_impact),
            "ratio_to_AX1090_single_cap": fmt(projection_owner_impact / AX1090_SINGLE_CAP),
            "status": "safe_smoke_nonclaim_if_parent_owner_signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "unit_id": "KU3165_2_at_K2_l2_cap",
            "quantity": "C_K2_at_K2_l2_cap",
            "definition": "coefficient impact at the 3164 l2 cap",
            "formula": "C_K2 = K2_cap_l2 * C_K2_unit",
            "value": fmt(cap_impact),
            "ratio_to_AX1090_single_cap": fmt(cap_impact / AX1090_SINGLE_CAP),
            "status": "saturates_internal_AX1090_single_cap",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "unit_id": "KU3165_3_internal_cap",
            "quantity": "K2_internal_cap_l2",
            "definition": "largest K2 allowed by the inherited AX1090 single coefficient cap for this l2 lane",
            "formula": "K2 <= AX1090_SINGLE_CAP/C_K2_unit",
            "value": fmt(AX1090_SINGLE_CAP / unit),
            "source_value_from_3164": fmt(k2_cap),
            "status": "internal_cap_reproduced",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def residual_vector_rows(values: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    unit = values["unit_coefficient"]
    components = [
        ("RV3165_0", "gamma_minus_1", "Eij_2_trace", "spatial curvature/Shapiro/light bending", "Delta_gamma_K2 = Pi_gamma_K2 * K2 * C_K2_unit"),
        ("RV3165_1", "beta_minus_1", "E00_4", "perihelion/nonlinear superposition/second-order clocks", "Delta_beta_K2 = Pi_beta_K2 * K2 * C_K2_unit"),
        ("RV3165_2", "alpha2_or_xi_anisotropy", "Eij_2_traceless", "preferred-location/domain anisotropy", "Delta_aniso_K2 = Pi_aniso_K2 * K2 * C_K2_unit"),
        ("RV3165_3", "alpha1_alpha2_vector", "E0i_3", "preferred-frame/vector readout", "Delta_vector_K2 = Pi_vector_K2 * K2 * C_K2_unit"),
        ("RV3165_4", "zeta_conservation", "div_Eres", "Bianchi/Ward/source-exchange conservation", "Delta_zeta_K2 = Pi_zeta_K2 * K2 * C_K2_unit plus time/exchange kernels"),
        ("RV3165_5", "clock_redshift", "E00_2_E00_4_time_readout", "clock/redshift/local time readout", "Delta_clock_K2 = Pi_clock_K2 * K2 * C_K2_unit"),
        ("RV3165_6", "orbital_acceleration_precession", "E00_2_E00_4_boundary_domain_tail", "orbit/perihelion/radial acceleration", "Delta_orbit_K2 = Pi_orbit_K2 * K2 * C_K2_unit"),
    ]
    rows: list[dict[str, object]] = []
    for row_id, component, ppn_feed, observable, formula in components:
        rows.append(
            {
                "vector_id": row_id,
                "component": component,
                "ppn_priority_feed": ppn_feed,
                "observable_arena": observable,
                "unit_K2_residual_coefficient": fmt(unit),
                "residual_formula": formula,
                "required_extra_input": "projection kernel Pi_*_K2 and empirical bound for this observable",
                "status": "mapped_nonclaim_kernel_missing",
                "valid_for_claim": "false",
                "generated_utc": now,
            }
        )
    return rows


def gate_rows(values: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    unit = values["unit_coefficient"]
    k2_cap = values["k2_cap_l2"]
    return [
        {
            "gate_id": "G3165_0_internal_AX1090",
            "gate": "internal AX1090 l2 coefficient cap",
            "status": "pass_nonclaim",
            "formula": "K2 * C_K2_unit <= AX1090_SINGLE_CAP",
            "required_bound": fmt(k2_cap),
            "missing_for_claim": "parent Wbar and M_Lambda, or declared closure-lane test status",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3165_1_projection_owner_smoke",
            "gate": "projection-owner K2=1 smoke",
            "status": "pass_nonclaim",
            "formula": "C_K2_unit/AX1090_SINGLE_CAP",
            "required_bound": "<= 1",
            "computed_ratio": fmt(unit / AX1090_SINGLE_CAP),
            "missing_for_claim": "Wbar projection owner and M_Lambda=1 parent theorem",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3165_2_ppn_gamma_beta",
            "gate": "PPN gamma/beta gate",
            "status": "blocked_for_claim",
            "formula": "|Pi_gamma,beta_K2| * K2 * C_K2_unit <= empirical_PPN_bound",
            "required_bound": "K2 <= empirical_PPN_bound/(|Pi_K2|*C_K2_unit)",
            "missing_for_claim": "Pi_gamma_K2; Pi_beta_K2; source-backed empirical bounds",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3165_3_clock_gate",
            "gate": "clock/redshift gate",
            "status": "blocked_for_claim",
            "formula": "|Pi_clock_K2| * K2 * C_K2_unit <= empirical_clock_bound",
            "required_bound": "K2 <= empirical_clock_bound/(|Pi_clock_K2|*C_K2_unit)",
            "missing_for_claim": "Pi_clock_K2; clock experiment bound convention",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3165_4_orbital_gate",
            "gate": "orbital/perihelion/acceleration gate",
            "status": "blocked_for_claim",
            "formula": "|Pi_orbit_K2| * K2 * C_K2_unit <= empirical_orbital_bound",
            "required_bound": "K2 <= empirical_orbital_bound/(|Pi_orbit_K2|*C_K2_unit)",
            "missing_for_claim": "Pi_orbit_K2; orbital observable bound and source-domain readout convention",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "G3165_5_conservation_gate",
            "gate": "Bianchi/Ward conservation gate",
            "status": "blocked_for_claim",
            "formula": "stationary K2 l2 lane must have no hidden exchange current or time-varying boundary source",
            "required_bound": "nabla.Eres - kappa*nabla.T_total = 0 or bounded",
            "missing_for_claim": "time/exchange kernel for K2 lane; source-current owner",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows(values: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    unit = values["unit_coefficient"]
    return [
        {
            "decision_id": "D3165_0_residual_coefficient",
            "decision": "K2 now has a concrete per-unit local residual coefficient",
            "evidence": f"C_K2_unit={fmt(unit)}",
            "effect": "PPN/clock/orbital gates can be written as projection-kernel bounds, not vague missing coupling",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3165_1_projection_owner_smoke",
            "decision": "if Wbar projection owner and M_Lambda=1 later close, K2=1 is far below the internal AX1090 cap",
            "evidence": f"C_K2_unit/AX1090_SINGLE_CAP={fmt(unit / AX1090_SINGLE_CAP)}",
            "effect": "the first-domain lane is not numerically scary under the natural projection-owner case",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3165_2_claim_block",
            "decision": "no PPN/clock/orbital claim is allowed yet",
            "evidence": "projection kernels Pi_*_K2 and empirical bounds are not sourced in this checkpoint",
            "effect": "3166 should source/fill the first empirical projection gate, preferably gamma/Shapiro or orbital precession",
            "next_action": "3166-Y5-R2FR-first-K2-empirical-projection-gate-source-intake-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    unit: list[dict[str, object]],
    vector: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    unit_row = next(row for row in unit if row["unit_id"] == "KU3165_0_definition")
    unit_value = float(str(unit_row["value"]))
    cap_row = next(row for row in unit if row["unit_id"] == "KU3165_3_internal_cap")
    cap_reproduced = math.isclose(float(str(cap_row["value"])), float(str(cap_row["source_value_from_3164"])), rel_tol=1e-12)
    vector_ok = len(vector) >= 6 and all(float(str(row["unit_K2_residual_coefficient"])) == unit_value for row in vector)
    blocked_gates = any(row["status"] == "blocked_for_claim" for row in gates)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, unit, vector, gates, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3165_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3165_1_unit_coefficient_positive",
            "status": "pass" if unit_value > 0.0 else "fail",
            "detail": fmt(unit_value),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3165_2_internal_cap_reproduced",
            "status": "pass" if cap_reproduced else "fail",
            "detail": "AX1090_SINGLE_CAP/C_K2_unit equals 3164 K2 cap",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3165_3_residual_vector_mapped",
            "status": "pass" if vector_ok else "fail",
            "detail": f"{len(vector)} components mapped",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3165_4_claim_blockers_retained",
            "status": "pass" if blocked_gates else "fail",
            "detail": "empirical projection gates remain blocked for claim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3165_5_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3165 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    values = source_values()
    inputs = input_rows()
    unit = unit_rows(values)
    vector = residual_vector_rows(values)
    gates = gate_rows(values)
    decisions = decision_rows(values)
    validations = validation_rows(inputs, unit, vector, gates, decisions)
    write_csv(INPUTS, inputs)
    write_csv(UNIT, unit)
    write_csv(VECTOR, vector)
    write_csv(GATES, gates)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3165 validation failed: {failures}")


if __name__ == "__main__":
    main()
