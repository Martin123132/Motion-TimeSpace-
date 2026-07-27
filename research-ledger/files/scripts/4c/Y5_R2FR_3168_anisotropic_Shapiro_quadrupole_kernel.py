from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3168_INPUTS.csv"
KERNEL = OUT / "P8_Y5_R2FR_3168_LOS_KERNEL_DERIVATION.csv"
EXAMPLES = OUT / "P8_Y5_R2FR_3168_ORIENTATION_EXAMPLES.csv"
GATES = OUT / "P8_Y5_R2FR_3168_QUADRUPOLE_GATE_CONTRACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3168_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3168_VALIDATION.csv"


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


def csv_value(path: Path, key: str, value: str, column: str) -> str:
    for row in read_csv(path):
        if row.get(key) == value:
            return row[column]
    raise KeyError(f"missing {key}={value} in {path}")


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("3167-Y5-R2FR-Pi-gamma-K2-Shapiro-projection-kernel-or-unit-smoke-only-under-AX1090.md", "3167 scalar-gamma/l2 split"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3167_SHAPIRO_PROJECTION_DERIVATION.csv", "l2 scalar gamma zero and anisotropic Shapiro survivor row"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3167_MIXING_GATE.csv", "3167 leakage/mixing gate"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3166_K2_GAMMA_EMPIRICAL_GATE.csv", "Cassini scalar envelope used only as borrowed smoke scale"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv", "C_K2_unit"),
        ("1182-Y5-R10-symbolic-PPN-KS-prediction-map-or-numeric-comparator-runner.md", "older STF/scalar PPN split support"),
    ]
    return [
        {
            "input_id": f"IN3168_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(rows)
    ]


def values() -> dict[str, float]:
    c_k2_unit = float(
        csv_value(
            OUT / "P8_Y5_R2FR_3165_K2_UNIT_RESIDUAL_COEFFICIENT.csv",
            "unit_id",
            "KU3165_0_definition",
            "value",
        )
    )
    default_gate = next(
        row
        for row in read_csv(OUT / "P8_Y5_R2FR_3166_K2_GAMMA_EMPIRICAL_GATE.csv")
        if row["gate_id"] == "KG3166_2_abs_2sigma_default"
    )
    internal_cap = float(
        csv_value(
            OUT / "P8_Y5_R2FR_3164_KLAMBDAW_CLOSURE_LANE.csv",
            "quantity",
            "K_2",
            "required_bound_l2",
        )
    )
    gamma_abs_bound = float(default_gate["gamma_abs_bound"])
    return {
        "c_k2_unit": c_k2_unit,
        "gamma_abs_bound": gamma_abs_bound,
        "borrowed_unit_bound": gamma_abs_bound / c_k2_unit,
        "internal_cap": internal_cap,
    }


def shapiro_b_weight(rho: float) -> float:
    if rho <= 0.0:
        raise ValueError("rho must be positive")
    return rho / (math.sqrt(1.0 + rho * rho) * math.asinh(rho))


def orientation_values(rho: float) -> dict[str, float]:
    b_weight = shapiro_b_weight(rho)
    return {
        "B_1_over_r": b_weight,
        "axis_parallel_to_ray": 1.0 - 1.5 * b_weight,
        "axis_along_impact": 0.5 * (3.0 * b_weight - 1.0),
        "axis_transverse_to_ray_and_impact": -0.5,
    }


def kernel_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "kernel_id": "KD3168_0_first_order_null_delay",
            "object": "quadrupole_Shapiro_delay",
            "derivation": "for a small spatial-trace residual delta g_ij = A W(r) P2(cos theta) delta_ij, the first-order null travel-time perturbation is proportional to the line integral of W(r) P2(cos theta)",
            "formula": "Delta_t_Q = (A/(2c)) int_path W(r(s)) P2(cos theta(s)) ds, convention factor retained in Pi_quad if metric normalization differs",
            "result": "A = K2*C_K2_unit enters through a line-of-sight quadrupole kernel",
            "status": "kernel_shape_derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "kernel_id": "KD3168_1_normalized_los_kernel",
            "object": "Pi_quad_LOS[W]",
            "derivation": "normalize the anisotropic delay by the same positive radial weight used by the comparator",
            "formula": "Pi_quad_LOS[W] = int W(r(s)) P2(cos theta(s)) ds / int W(r(s)) ds",
            "result": "Delta_quad_norm = K2*C_K2_unit*Pi_quad_LOS",
            "status": "normalized_kernel_derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "kernel_id": "KD3168_2_universal_bound",
            "object": "abs_Pi_quad_LOS",
            "derivation": "P2(x) lies in [-1/2,1] and W>=0",
            "formula": "|Pi_quad_LOS| <= 1",
            "result": fmt(1.0),
            "status": "rigorous_envelope",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "kernel_id": "KD3168_3_even_ray_formula",
            "object": "straight_ray_even_weight",
            "derivation": "with x(s)=b_vec+s*k, source axis a, and even W(r), the odd cross term integrates away",
            "formula": "Pi_Q=(3/2)*[(a.bhat)^2 B_W + (a.k)^2*(1-B_W)] - 1/2, B_W=<b^2/(b^2+s^2)>_W",
            "result": "orientation_kernel_exact_for_even_radial_weight",
            "status": "geometry_kernel_derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "kernel_id": "KD3168_4_shapiro_weight_1_over_r",
            "object": "B_W_for_W_equals_1_over_r",
            "derivation": "for symmetric endpoints s in [-L,L] and rho=L/b",
            "formula": "B_1/r(rho)=rho/(sqrt(1+rho^2)*asinh(rho))",
            "result": "closed_form_ready_for_path_smoke_rows",
            "status": "closed_form_kernel_derived",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "kernel_id": "KD3168_5_scalar_zero_not_los_zero",
            "object": "3167_to_3168_bridge",
            "derivation": "sphere-average monopole projection and line-of-sight projection are different linear functionals",
            "formula": "<P2>_S2=0 but Pi_quad_LOS[W] generally nonzero",
            "result": "scalar Cassini gamma can miss pure l2 while anisotropic Shapiro can still see it",
            "status": "derived_channel_split",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def example_rows() -> list[dict[str, object]]:
    now = stamp()
    rows: list[dict[str, object]] = []
    for rho in [1.0, 3.0, 10.0, 100.0, 1000.0]:
        values = orientation_values(rho)
        for orientation, kernel in [
            ("axis_parallel_to_ray", values["axis_parallel_to_ray"]),
            ("axis_along_impact", values["axis_along_impact"]),
            ("axis_transverse_to_ray_and_impact", values["axis_transverse_to_ray_and_impact"]),
        ]:
            rows.append(
                {
                    "example_id": f"EX3168_{int(rho) if rho.is_integer() else rho}_{orientation}",
                    "rho_L_over_b": fmt(rho),
                    "B_1_over_r": fmt(values["B_1_over_r"]),
                    "orientation": orientation,
                    "Pi_quad_LOS_1_over_r": fmt(kernel),
                    "abs_kernel_leq_1": str(abs(kernel) <= 1.0).lower(),
                    "meaning": "orientation/path kernels are order-unity unless geometry or fit covariance suppresses them",
                    "valid_for_claim": "false",
                    "generated_utc": now,
                }
            )
    return rows


def gate_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "gate_id": "QG3168_0_normalized_anisotropic_gate",
            "gate": "quadrupole_Shapiro_or_light_bending_residual",
            "formula": "K2 <= epsilon_quad/(|Pi_quad_LOS|*C_K2_unit)",
            "C_K2_unit": fmt(v["c_k2_unit"]),
            "epsilon_quad": "MISSING_PRIMARY_ANISOTROPIC_BOUND_OR_COVARIANCE",
            "Pi_quad_LOS": "derived_formula_or_abs_leq_1_envelope",
            "K2_bound": "not_scoreable_until_epsilon_quad_exists",
            "status": "gate_shape_derived_empirical_bound_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "QG3168_1_abs_leq_1_envelope",
            "gate": "profile_agnostic_kernel_bound",
            "formula": "|Delta_quad_norm| <= |K2|*C_K2_unit",
            "C_K2_unit": fmt(v["c_k2_unit"]),
            "epsilon_quad": "requires empirical anisotropic residual bound",
            "Pi_quad_LOS": "abs_leq_1",
            "K2_bound": "epsilon_quad/C_K2_unit",
            "status": "rigorous_kernel_envelope_ready",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "QG3168_2_borrowed_Cassini_envelope_smoke",
            "gate": "do_not_claim_borrowed_scalar_gamma_as_quadrupole_bound",
            "formula": "if epsilon_quad were set equal to 6.7e-5 only as a smoke scale and |Pi_quad_LOS|=1, then K2 <= 6.7e-5/C_K2_unit",
            "C_K2_unit": fmt(v["c_k2_unit"]),
            "epsilon_quad": fmt(v["gamma_abs_bound"]),
            "Pi_quad_LOS": "1.0_worst_case",
            "K2_bound": fmt(v["borrowed_unit_bound"]),
            "ratio_to_internal_AX1090_K2_cap": fmt(v["borrowed_unit_bound"] / v["internal_cap"]),
            "status": "borrowed_scale_smoke_only_not_empirical_quadrupole_bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "gate_id": "QG3168_3_source_transfer_contract",
            "gate": "Earth_l2_K2_to_Solar_Shapiro_K2",
            "formula": "K2_solar = T_source(Earth_l2_to_solar_los)*K2_earth or build K2_solar directly",
            "C_K2_unit": fmt(v["c_k2_unit"]),
            "epsilon_quad": "not_applicable",
            "Pi_quad_LOS": "not_applicable",
            "K2_bound": "not_transferable_without_T_source_or_solar_domain_lane",
            "status": "source_transfer_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "D3168_0_kernel_progress",
            "decision": "the anisotropic Shapiro/quadrupole kernel is now formula-derived",
            "evidence": "KD3168_1 through KD3168_4",
            "effect": "future empirical rows need epsilon_quad and path/source geometry, not a fresh symbolic placeholder",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3168_1_worst_case_not_dead",
            "decision": "line-of-sight quadrupole projection can be order-unity even though scalar gamma projection is zero",
            "evidence": "orientation examples for W=1/r",
            "effect": "do not claim safety from spherical orthogonality alone",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3168_2_next_target",
            "decision": "source the anisotropic/STF Shapiro bound or build a solar-domain K2 transfer law",
            "evidence": "QG3168_0 and QG3168_3 remain the active missing empirical/transfer inputs",
            "effect": "3169 should stop borrowing scalar gamma and go after a real quadrupole/STF comparator or source-transfer theorem",
            "next_action": "3169-Y5-R2FR-STF-Shapiro-source-bound-or-solar-domain-K2-transfer-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    kernels: list[dict[str, object]],
    examples: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    envelope_ok = any(row["kernel_id"] == "KD3168_2_universal_bound" and row["result"] == fmt(1.0) for row in kernels)
    example_ok = all(row["abs_kernel_leq_1"] == "true" for row in examples)
    missing_empirical_retained = any(row["gate_id"] == "QG3168_0_normalized_anisotropic_gate" and "MISSING" in str(row["epsilon_quad"]) for row in gates)
    transfer_guard = any(row["gate_id"] == "QG3168_3_source_transfer_contract" and row["status"] == "source_transfer_missing" for row in gates)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, kernels, examples, gates, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3168_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3168_1_universal_kernel_bound",
            "status": "pass" if envelope_ok else "fail",
            "detail": "|Pi_quad_LOS|<=1 recorded",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3168_2_examples_within_bound",
            "status": "pass" if example_ok else "fail",
            "detail": "all W=1/r orientation examples satisfy abs(kernel)<=1",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3168_3_empirical_bound_missing_retained",
            "status": "pass" if missing_empirical_retained else "fail",
            "detail": "epsilon_quad remains missing for actual anisotropic scoring",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3168_4_source_transfer_guard_retained",
            "status": "pass" if transfer_guard else "fail",
            "detail": "Earth-to-solar K2 transfer remains blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3168_5_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3168 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    v = values()
    inputs = input_rows()
    kernels = kernel_rows()
    examples = example_rows()
    gates = gate_rows(v)
    decisions = decision_rows()
    validations = validation_rows(inputs, kernels, examples, gates, decisions)
    write_csv(INPUTS, inputs)
    write_csv(KERNEL, kernels)
    write_csv(EXAMPLES, examples)
    write_csv(GATES, gates)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3168 validation failed: {failures}")


if __name__ == "__main__":
    main()
