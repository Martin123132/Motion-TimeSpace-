from __future__ import annotations

import csv
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3160_INPUTS.csv"
HODGE = OUT / "P8_Y5_R2FR_3160_HODGE_SPHERE_PRODUCT_BOUND.csv"
ZERO = OUT / "P8_Y5_R2FR_3160_ZERO_THEOREM_AUDIT.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3160_PRODUCT_CLOSURE_CONTRACT.csv"
DECISION = OUT / "P8_Y5_R2FR_3160_DECISION.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3160_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def fmt(value: float) -> str:
    return f"{value:.15e}"


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


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_value(quantity: str) -> float:
    for row in read_csv(OUT / "P8_Y5_R2FR_3158_SOURCE_VALUES.csv"):
        if row.get("quantity") == quantity:
            return float(row["value"])
    raise KeyError(f"missing source value {quantity}")


def tightest_cap_value() -> float:
    rows = read_csv(OUT / "P8_Y5_R2FR_3159_NUMERIC_REVERSE_CAP_WITH_DERIVED_COEFFICIENTS.csv")
    for row in rows:
        if row.get("component") == "Earth_J2_full_shell_metric_projection":
            return float(row["single_cap_required_LWlambda"])
    raise KeyError("missing 3159 Earth_J2_full_shell_metric_projection row")


def internal(relative: str) -> str:
    return str((ROOT / relative).resolve())


def input_rows() -> list[dict[str, object]]:
    now = stamp()
    rows = [
        ("3152-Y5-R2FR-kernel-closedness-chain-rule-or-first-norm-factor-bound-under-AX1090.md", "chain-rule split L_W B_z ||Lambda||"),
        ("3157-Y5-R2FR-LWlambda-factor-or-first-source-domain-multipole-fill-under-AX1090.md", "L_Wphys_Lambda product contract"),
        ("3159-Y5-R2FR-projection-coefficient-derivation-for-J2-and-tide-under-AX1090.md", "derived C2/Ctide and tightest local source-domain cap"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3158_SOURCE_VALUES.csv", "Earth radius for round-sphere Hodge constant"),
        ("source-intake/mts_residuals/P8_Y5_R2FR_3159_NUMERIC_REVERSE_CAP_WITH_DERIVED_COEFFICIENTS.csv", "tightest derived reverse cap"),
    ]
    return [
        {
            "input_id": f"IN3160_{index}",
            "path": internal(path),
            "exists": str((ROOT / path).exists()).lower(),
            "role": role,
            "valid_for_claim": "false",
            "generated_utc": now,
        }
        for index, (path, role) in enumerate(rows)
    ]


def hodge_rows(radius_m: float, tightest_lwlambda_cap: float) -> list[dict[str, object]]:
    now = stamp()
    lambda1 = 2.0 / (radius_m * radius_m)
    c_poincare_m = 1.0 / math.sqrt(lambda1)
    c_hodge_dimensionless = 1.0 / math.sqrt(2.0)
    allowed_lw_bexact = tightest_lwlambda_cap / c_hodge_dimensionless
    return [
        {
            "bound_id": "HB3160_0_round_sphere_spectrum",
            "object": "scalar_Laplacian_first_nonzero_eigenvalue_on_S2_R",
            "formula": "lambda_1 = 2/R^2",
            "numeric_value": fmt(lambda1),
            "units": "m^-2",
            "meaning": "round-sphere Poincare/Hodge input for exact boundary primitive",
            "status": "derived_for_first_domain_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "HB3160_1_dimensional_poincare_constant",
            "object": "C_Poincare_dimensional",
            "formula": "||Lambda||_L2 <= (R/sqrt(2)) ||d_S Lambda||_L2 for zero-mean scalar primitive",
            "numeric_value": fmt(c_poincare_m),
            "units": "m",
            "meaning": "dimensional constant for a round Earth-radius boundary sphere",
            "status": "derived_for_first_domain_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "HB3160_2_dimensionless_hodge_constant",
            "object": "C_Hodge_hat",
            "formula": "||Lambda||_L2/R <= (1/sqrt(2)) ||d_S Lambda||_L2",
            "numeric_value": fmt(c_hodge_dimensionless),
            "units": "dimensionless",
            "meaning": "dimensionless primitive bound under the normalized 3159 Earth sphere convention",
            "status": "derived_for_first_domain_nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "bound_id": "HB3160_3_product_sufficient_condition",
            "object": "L_W_phys_times_B_exact_ceiling",
            "formula": "if L_Wphys_Lambda <= L_W_phys C_Hodge_hat B_exact, require L_W_phys B_exact <= cap/C_Hodge_hat",
            "numeric_value": fmt(allowed_lw_bexact),
            "units": "dimensionless_product_in_selected_norm",
            "meaning": "sufficient first-domain condition after deriving C_Hodge_hat; still needs parent L_W_phys and B_exact",
            "status": "numeric_contract_ready_parent_factors_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def zero_rows() -> list[dict[str, object]]:
    now = stamp()
    return [
        {
            "zero_id": "ZT3160_0_physical_kernel_zero",
            "route": "D_z Wbar P_phys = 0",
            "proof_status": "not_parent_signed",
            "what_would_be_needed": "explicit Wbar, physical tangent domain, and proof that physical multipole/tide drift is in the annihilator",
            "effect_if_signed": "L_W_phys=0 => L_Wphys_Lambda=0",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "zero_id": "ZT3160_1_exact_primitive_zero",
            "route": "B_exact=d_S Lambda=0 plus zero-mean gauge => Lambda=0",
            "proof_status": "conditional_math_ready_not_parent_signed",
            "what_would_be_needed": "parent boundary condition making the exact part vanish without deleting public charges",
            "effect_if_signed": "||Lambda||_*=0 => L_Wphys_Lambda=0",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "zero_id": "ZT3160_2_round_sphere_hodge_bound",
            "route": "zero-mean Hodge/Poincare bound on round S2_R",
            "proof_status": "finite_bound_derived_nonclaim",
            "what_would_be_needed": "parent values for L_W_phys and B_exact in the same normalized L2 metric-component convention",
            "effect_if_signed": "L_Wphys_Lambda <= L_W_phys C_Hodge_hat B_exact",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def contract_rows(tightest_lwlambda_cap: float) -> list[dict[str, object]]:
    now = stamp()
    c_hodge = 1.0 / math.sqrt(2.0)
    allowed_lw_bexact = tightest_lwlambda_cap / c_hodge
    return [
        {
            "contract_id": "PC3160_0_direct_product_cap",
            "quantity": "L_Wphys_Lambda",
            "required_bound": fmt(tightest_lwlambda_cap),
            "formula": "L_Wphys_Lambda <= tightest_3159_first_domain_cap",
            "source": "3159 Earth_J2_full_shell_metric_projection",
            "status": "cap_numeric_product_value_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PC3160_1_hodge_factorized_cap",
            "quantity": "L_W_phys_times_B_exact",
            "required_bound": fmt(allowed_lw_bexact),
            "formula": "L_W_phys B_exact <= tightest_3159_cap / C_Hodge_hat with C_Hodge_hat=1/sqrt(2)",
            "source": "3160 round-sphere Hodge/Poincare bound",
            "status": "cap_numeric_parent_factors_missing",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "PC3160_2_closure_if_parent_factors_absent",
            "quantity": "local_branch_closure_parameter",
            "required_bound": fmt(tightest_lwlambda_cap),
            "formula": "declare kappa_boundary := L_Wphys_Lambda and require kappa_boundary <= tightest_3159_cap",
            "source": "only allowed if parent derivation fails after explicit attempt",
            "status": "closure_only_not_theory_success",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows(tightest_lwlambda_cap: float) -> list[dict[str, object]]:
    now = stamp()
    allowed_lw_bexact = tightest_lwlambda_cap * math.sqrt(2.0)
    return [
        {
            "decision_id": "D3160_0_hodge_factor_removed",
            "decision": "C_Hodge is no longer a fog variable for the first round-sphere local domain",
            "evidence": "C_Hodge_hat=1/sqrt(2) under normalized L2 exact-primitive convention",
            "effect": "remaining parent product is L_W_phys B_exact, not L_W_phys C_Hodge B_exact",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3160_1_required_parent_product",
            "decision": "first-domain local branch requires L_W_phys B_exact below a loose numeric ceiling",
            "evidence": f"L_W_phys B_exact <= {fmt(allowed_lw_bexact)} under the 3159 tightest single cap",
            "effect": "no local pass until L_W_phys and B_exact are derived/sourced in the same convention",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "D3160_2_next_attack",
            "decision": "derive or source B_exact first because it is closer to boundary data than Wbar sensitivity",
            "evidence": "B_exact is the exact surface drift norm; Wbar derivative remains parent-action dependent",
            "effect": "next checkpoint should try to compute/bound B_exact from source-domain boundary data before declaring closure",
            "next_action": "3161-Y5-R2FR-Bexact-source-bound-or-Wbar-sensitivity-interface-under-AX1090",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, object]],
    hodge: list[dict[str, object]],
    zero: list[dict[str, object]],
    contracts: list[dict[str, object]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    now = stamp()
    input_ok = all(row["exists"] == "true" for row in inputs)
    hodge_by_id = {row["bound_id"]: row for row in hodge}
    c_hodge_ok = math.isclose(
        float(str(hodge_by_id["HB3160_2_dimensionless_hodge_constant"]["numeric_value"])),
        1.0 / math.sqrt(2.0),
        rel_tol=1e-12,
    )
    contract_positive = all(float(str(row["required_bound"])) > 0.0 for row in contracts[:2])
    zero_nonclaim = all(row["valid_for_claim"] == "false" for row in zero)
    no_claim = all(
        str(row.get("valid_for_claim", "")).lower() == "false"
        for rows in [inputs, hodge, zero, contracts, decisions]
        for row in rows
    )
    return [
        {
            "check_id": "V3160_0_inputs_exist",
            "status": "pass" if input_ok else "fail",
            "detail": "; ".join(f"{row['input_id']}={row['exists']}" for row in inputs),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3160_1_hodge_constant_derived",
            "status": "pass" if c_hodge_ok else "fail",
            "detail": "C_Hodge_hat=1/sqrt(2)",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3160_2_contract_bounds_positive",
            "status": "pass" if contract_positive else "fail",
            "detail": "direct and Hodge-factorized product bounds are positive",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3160_3_zero_routes_nonclaim",
            "status": "pass" if zero_nonclaim else "fail",
            "detail": "zero routes remain conditional/nonclaim",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3160_4_no_claim_leak",
            "status": "pass" if no_claim else "fail",
            "detail": "all 3160 rows valid_for_claim=false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    radius = source_value("R_Earth_equatorial")
    cap = tightest_cap_value()
    inputs = input_rows()
    hodge = hodge_rows(radius, cap)
    zero = zero_rows()
    contracts = contract_rows(cap)
    decisions = decision_rows(cap)
    validations = validation_rows(inputs, hodge, zero, contracts, decisions)
    write_csv(INPUTS, inputs)
    write_csv(HODGE, hodge)
    write_csv(ZERO, zero)
    write_csv(CONTRACT, contracts)
    write_csv(DECISION, decisions)
    write_csv(VALIDATION, validations)
    failures = [row for row in validations if row["status"] != "pass"]
    if failures:
        raise SystemExit(f"3160 validation failed: {failures}")


if __name__ == "__main__":
    main()
