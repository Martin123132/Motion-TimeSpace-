from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3167_INPUTS.csv"
DERIVATION = OUT / "P8_Y5_R2FR_3167_SHAPIRO_PROJECTION_DERIVATION.csv"
MIXING = OUT / "P8_Y5_R2FR_3167_MIXING_GATE.csv"
DOMAIN = OUT / "P8_Y5_R2FR_3167_SOURCE_DOMAIN_COMPATIBILITY.csv"
DECISION = OUT / "P8_Y5_R2FR_3167_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3167_VALIDATION.csv"


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
        ("3165-Y5-R2FR-K2-local-residual-vector-and-PPN-clock-orbital-gate-under-AX1090.md", "defines K2 residual vector and gamma placeholder"),
        ("3166-Y5-R2FR-first-K2-empirical-projection-gate-source-intake-under-AX1090.md", "Cassini source intake and unit-projection smoke gate"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3165_K2_LOCAL_RESIDUAL_VECTOR.csv", "K2 component map"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3166_K2_GAMMA_EMPIRICAL_GATE.csv", "Cassini unit-projection bound"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3166_CASSINI_GAMMA_SOURCE_INTAKE.csv", "Cassini source provenance"),
    ]
    return [
        {
            "input_id": f"IN3167_{index}",
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
    internal_cap = float(
        csv_value(
            OUT / "P8_Y5_R2FR_3164_KLAMBDAW_CLOSURE_LANE.csv",
            "quantity",
            "K_2",
            "required_bound_l2",
        )
    )
    default_gate = next(
        row
        for row in read_csv(OUT / "P8_Y5_R2FR_3166_K2_GAMMA_EMPIRICAL_GATE.csv")
        if row["gate_id"] == "KG3166_2_abs_2sigma_default"
    )
    gamma_abs_bound = float(default_gate["gamma_abs_bound"])
    unit_projection_bound = float(default_gate["K2_bound_unit_projection"])
    return {
        "c_k2_unit": c_k2_unit,
        "internal_cap": internal_cap,
        "gamma_abs_bound": gamma_abs_bound,
        "unit_projection_bound": unit_projection_bound,
    }


def p2_average() -> float:
    # (1/2) int_{-1}^{1} (3 x^2 - 1)/2 dx = 0.
    return 0.5 * ((3.0 * (1.0**3 - (-1.0) ** 3) / 3.0) - (1.0 - (-1.0))) / 2.0


def p2_sphere_norm() -> float:
    return 4.0 * math.pi / 5.0


def derivation_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    average = p2_average()
    return [
        {
            "derivation_id": "SP3167_0_readout_distinction",
            "object": "PPN_gamma_vs_l2_spatial_trace",
            "statement": "PPN gamma is the scalar monopole coefficient of spatial curvature; a spatial-index trace carrying angular P2 is not automatically gamma_minus_1",
            "calculation": "decompose by spherical harmonics before mapping residual trace into PPN gamma",
            "result": "gamma_readout_requires_l0_projection",
            "status": "derived_sorting_rule",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "SP3167_1_l2_monopole_orthogonality",
            "object": "<Y00,P2>",
            "statement": "pure l=2 Legendre profile has zero monopole projection",
            "calculation": "0.5*int_-1^1 P2(x) dx = 0",
            "result": fmt(average),
            "status": "exact_math_pass",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "SP3167_2_pure_l2_scalar_gamma_kernel",
            "object": "Pi_gamma_K2_l0",
            "statement": "if K2 is a pure l=2 boundary/metric residual and the Cassini gamma readout is the l=0 PPN monopole coefficient, then Pi_gamma_K2_l0=0",
            "calculation": "Pi_gamma_K2_l0 = <Y00,P2>/<Y00,Y00>",
            "result": fmt(0.0),
            "status": "conditional_zero_theorem_for_scalar_gamma_only",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "SP3167_3_anisotropic_shapiro_survives",
            "object": "quadrupole_Shapiro_kernel",
            "statement": "the zero above does not erase a line-of-sight quadrupole time-delay/light-bending residual",
            "calculation": "anisotropic readout uses geometry/path kernel, not the l=0 gamma estimator",
            "result": "MISSING_LINE_OF_SIGHT_KERNEL",
            "status": "new_required_kernel_not_zero",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "derivation_id": "SP3167_4_sphere_norm_for_future_kernel",
            "object": "int_S2 P2^2 dOmega",
            "statement": "normalization for a future quadrupole/Shapiro projection row",
            "calculation": "int_S2 P_l^2 dOmega = 4*pi/(2l+1), l=2",
            "result": fmt(p2_sphere_norm()),
            "status": "normalization_ready",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def mixing_rows(v: dict[str, float]) -> list[dict[str, object]]:
    now = stamp()
    unit_bound = v["unit_projection_bound"]
    internal_ratio = unit_bound / v["internal_cap"]
    return [
        {
            "mixing_id": "MG3167_0_unit_leak_reproduces_3166",
            "mixing_case": "M20_Cassini=1",
            "formula": "K2 <= gamma_abs_bound/(|M20_Cassini|*C_K2_unit)",
            "K2_bound": fmt(unit_bound),
            "ratio_to_internal_AX1090_K2_cap": fmt(internal_ratio),
            "meaning": "this is exactly the 3166 unit-projection diagnostic, now reinterpreted as full l2-to-l0 leakage",
            "status": "diagnostic_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "mixing_id": "MG3167_1_pure_l2_monopole_zero",
            "mixing_case": "M20_Cassini=0",
            "formula": "Delta_gamma_scalar = 0*K2*C_K2_unit",
            "K2_bound": "not_applicable_from_scalar_gamma",
            "ratio_to_internal_AX1090_K2_cap": "not_applicable",
            "meaning": "pure l2 residual is not constrained by scalar gamma_minus_1; it must be tested through anisotropic Shapiro/quadrupole kernels",
            "status": "conditional_scalar_gamma_zero_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "mixing_id": "MG3167_2_symbolic_leak_gate",
            "mixing_case": "0<|M20_Cassini|<1",
            "formula": f"K2 <= {fmt(unit_bound)}/|M20_Cassini|",
            "K2_bound": "symbolic_depends_on_M20_Cassini",
            "ratio_to_internal_AX1090_K2_cap": f"{fmt(internal_ratio)}/|M20_Cassini|",
            "meaning": "Cassini scalar gamma constrains only monopole leakage/misprojection from the l2 lane",
            "status": "symbolic_gate_ready_leak_coefficient_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "mixing_id": "MG3167_3_internal_cap_leak_tolerance",
            "mixing_case": "K2_at_internal_AX1090_cap",
            "formula": "|M20_Cassini| <= gamma_abs_bound/(K2_internal*C_K2_unit)",
            "K2_bound": fmt(v["internal_cap"]),
            "max_allowed_abs_M20_Cassini": fmt(internal_ratio),
            "meaning": "if one tried to saturate the internal K2 cap, scalar-gamma leakage must be below this mixing fraction",
            "status": "diagnostic_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def domain_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "domain_id": "SD3167_0_earth_vs_solar_domain",
            "issue": "3161-3165 K2 cap was built from an Earth l=2/J2 source-domain lane, while Cassini gamma is a solar-conjunction Shapiro readout",
            "effect": "source-domain transfer/universality must be signed before the Earth-domain K2 cap is treated as the solar Shapiro K2 amplitude",
            "required_next_input": "source transfer law or separate solar-domain K2 construction",
            "status": "domain_transfer_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "domain_id": "SD3167_1_gamma_fit_vs_quadrupole_fit",
            "issue": "official gamma fit is a scalar PPN coefficient; quadrupole residuals need their own fit/covariance/readout",
            "effect": "scalar gamma bound cannot be used as a direct pure-l2 quadrupole bound unless l2-to-l0 mixing is sourced",
            "required_next_input": "Cassini/light-bending quadrupole Shapiro kernel or covariance row",
            "status": "arena_projection_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "decision_id": "D3167_0_zero_kernel_result",
            "decision": "Pi_gamma_K2_l0 is zero for a pure l=2 residual under the scalar monopole gamma readout",
            "evidence": "SP3167_1 and SP3167_2 spherical-harmonic orthogonality",
            "effect": "3166 unit-projection is retained only as a worst-case l2-to-l0 leakage diagnostic",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3167_1_real_danger_moves",
            "decision": "the real empirical danger is anisotropic Shapiro/quadrupole leakage, not scalar gamma_minus_1",
            "evidence": "SP3167_3 keeps line-of-sight quadrupole kernel active",
            "effect": "derive the quadrupole Shapiro kernel instead of hammering the wrong monopole gate",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3167_2_source_domain_guard",
            "decision": "do not transfer Earth-domain K2 caps to Solar Cassini readouts without a source-domain universality theorem",
            "evidence": "SD3167_0",
            "effect": "next run must either build the solar-domain K2 lane or derive a source-transfer law",
            "next_action": "3168-Y5-R2FR-anisotropic-Shapiro-quadrupole-kernel-or-source-transfer-contract-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    derivations: list[dict[str, object]],
    mixings: list[dict[str, object]],
    domains: list[dict[str, object]],
    decisions: list[dict[str, object]],
    v: dict[str, float],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    orthogonality = next(row for row in derivations if row["derivation_id"] == "SP3167_1_l2_monopole_orthogonality")
    orthogonality_ok = abs(float(str(orthogonality["result"]))) < 1e-30
    pure_zero = any(row["derivation_id"] == "SP3167_2_pure_l2_scalar_gamma_kernel" and float(str(row["result"])) == 0.0 for row in derivations)
    unit_leak = next(row for row in mixings if row["mixing_id"] == "MG3167_0_unit_leak_reproduces_3166")
    unit_reproduced = abs(float(str(unit_leak["K2_bound"])) - v["unit_projection_bound"]) / v["unit_projection_bound"] < 1e-12
    domain_guard = any(row["status"] == "domain_transfer_missing" for row in domains)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, derivations, mixings, domains, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3167_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3167_1_l2_monopole_orthogonality",
            "status": "pass" if orthogonality_ok else "fail",
            "detail": "average(P2)=0",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3167_2_pure_l2_scalar_gamma_zero",
            "status": "pass" if pure_zero else "fail",
            "detail": "Pi_gamma_K2_l0=0 under pure l2 scalar-monopole readout",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3167_3_unit_leak_reproduces_3166",
            "status": "pass" if unit_reproduced else "fail",
            "detail": "M20=1 mixing reproduces 3166 default unit-projection K2 bound",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3167_4_source_domain_guard_retained",
            "status": "pass" if domain_guard else "fail",
            "detail": "Earth-domain K2 and Solar Cassini readout transfer remains blocked",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3167_5_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3167 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    v = values()
    inputs = input_rows()
    derivations = derivation_rows(v)
    mixings = mixing_rows(v)
    domains = domain_rows()
    decisions = decision_rows()
    validations = validation_rows(inputs, derivations, mixings, domains, decisions, v)
    write_csv(INPUTS, inputs)
    write_csv(DERIVATION, derivations)
    write_csv(MIXING, mixings)
    write_csv(DOMAIN, domains)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3167 validation failed: {failures}")


if __name__ == "__main__":
    main()
