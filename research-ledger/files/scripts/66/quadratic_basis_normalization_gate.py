from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


def as_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def basis_map_rows() -> List[Dict[str, object]]:
    return [
        {
            "basis_id": "BM4458_0_R2",
            "mts_operator": "c_R2 R^2",
            "canonical_alpha_QG_contribution": "c_R2",
            "canonical_beta_QG_contribution": "0",
            "D0_contribution": "12*c_R2",
            "D2_contribution": "0",
            "local_effect": "massive_scalar_only_in_pure_metric_template",
            "safe_zero_route": "c_R2=0 or parent curvature-linear selector",
            "valid_for_claim": False,
        },
        {
            "basis_id": "BM4458_1_Ricci2",
            "mts_operator": "c_Ric R_mn R^mn",
            "canonical_alpha_QG_contribution": "0",
            "canonical_beta_QG_contribution": "c_Ric",
            "D0_contribution": "c_Ric",
            "D2_contribution": "-c_Ric",
            "local_effect": "scalar_and_massive_spin2_denominators",
            "safe_zero_route": "c_Ric=0 or exact topological/redefinition certificate",
            "valid_for_claim": False,
        },
        {
            "basis_id": "BM4458_2_Weyl2",
            "mts_operator": "c_W C_mnrs C^mnrs",
            "canonical_alpha_QG_contribution": "-(2/3)*c_W up to Gauss-Bonnet",
            "canonical_beta_QG_contribution": "2*c_W up to Gauss-Bonnet",
            "D0_contribution": "-6*c_W",
            "D2_contribution": "-2*c_W",
            "local_effect": "scalar_and_massive_spin2_denominators_after_4D_GB_split",
            "safe_zero_route": "c_W=0 or exact GB/topological local silence certificate",
            "valid_for_claim": False,
        },
        {
            "basis_id": "BM4458_3_Riemann2",
            "mts_operator": "c_Riem R_mnrs R^mnrs",
            "canonical_alpha_QG_contribution": "-c_Riem up to Gauss-Bonnet",
            "canonical_beta_QG_contribution": "4*c_Riem up to Gauss-Bonnet",
            "D0_contribution": "-8*c_Riem",
            "D2_contribution": "-4*c_Riem",
            "local_effect": "canonical_if_parent_uses_Riemann2_basis",
            "safe_zero_route": "exact GB combination or c_Riem=0",
            "valid_for_claim": False,
        },
        {
            "basis_id": "BM4458_4_GaussBonnet",
            "mts_operator": "b_GB (Riemann^2 - 4 Ricci^2 + R^2)",
            "canonical_alpha_QG_contribution": "locally_silent_only_if_constant_uncoupled_4D_boundary_harmless",
            "canonical_beta_QG_contribution": "locally_silent_only_if_constant_uncoupled_4D_boundary_harmless",
            "D0_contribution": "0_only_under_strict_GB_guard",
            "D2_contribution": "0_only_under_strict_GB_guard",
            "local_effect": "topological_safe_case_not_generic_quadratic_operator",
            "safe_zero_route": "constant_uncoupled_4D_GB_plus_boundary_no_flux",
            "valid_for_claim": False,
        },
    ]


def coefficient_region_rows(bounds: Sequence[Dict[str, str]]) -> List[Dict[str, object]]:
    scalar = next(row for row in bounds if row.get("bound_id") == "QB4457_0_scalar_D0")
    spin2 = next(row for row in bounds if row.get("bound_id") == "QB4457_1_spin2_D2")
    d0_bound = as_float(scalar.get("coefficient_upper_bound_m2"))
    d2_bound = as_float(spin2.get("coefficient_upper_bound_m2"))
    if d0_bound is None or d2_bound is None:
        raise ValueError("4457 coefficient bounds are missing numeric D0/D2 limits")
    return [
        {
            "region_id": "REG4458_0_full_basis",
            "basis": "R2 + Ricci2 + Weyl2 + Riemann2 + strict_GB_guard",
            "alpha_QG_map": "alpha_QG = c_R2 - (2/3)c_W - c_Riem",
            "beta_QG_map": "beta_QG = c_Ric + 2c_W + 4c_Riem",
            "D0_map": "D0 = 12*c_R2 + c_Ric - 6*c_W - 8*c_Riem",
            "D2_map": "D2 = -c_Ric - 2*c_W - 4*c_Riem",
            "candidate_pass_region": f"0 < D0 <= {d0_bound} m^2 and 0 < D2 <= {d2_bound} m^2",
            "zero_region": "D0,D2 absent only if all non-topological quadratic coefficients are parent-zero or exact GB-safe",
            "valid_for_claim": False,
        },
        {
            "region_id": "REG4458_1_no_Riemann_basis",
            "basis": "R2 + Ricci2 + Weyl2 with no independent Riemann2",
            "alpha_QG_map": "alpha_QG = c_R2 - (2/3)c_W",
            "beta_QG_map": "beta_QG = c_Ric + 2c_W",
            "D0_map": "D0 = 12*c_R2 + c_Ric - 6*c_W",
            "D2_map": "D2 = -c_Ric - 2*c_W",
            "candidate_pass_region": f"0 < 12*c_R2 + c_Ric - 6*c_W <= {d0_bound} m^2 and 0 < -c_Ric - 2*c_W <= {d2_bound} m^2",
            "zero_region": "c_R2=c_Ric=c_W=0, or exact topological combination with boundary silence",
            "valid_for_claim": False,
        },
        {
            "region_id": "REG4458_2_pure_R2_scalar_only",
            "basis": "R2 only",
            "alpha_QG_map": "alpha_QG = c_R2",
            "beta_QG_map": "beta_QG = 0",
            "D0_map": "D0 = 12*c_R2",
            "D2_map": "D2 = 0",
            "candidate_pass_region": f"0 < c_R2 <= {d0_bound / 12.0} m^2 for scalar channel; no massive spin2 pole",
            "zero_region": "c_R2=0 if parent curvature-linear selector is signed",
            "valid_for_claim": False,
        },
        {
            "region_id": "REG4458_3_pure_Weyl2",
            "basis": "Weyl2 only",
            "alpha_QG_map": "alpha_QG = -(2/3)c_W",
            "beta_QG_map": "beta_QG = 2*c_W",
            "D0_map": "D0 = -6*c_W",
            "D2_map": "D2 = -2*c_W",
            "candidate_pass_region": f"{-d0_bound / 6.0} <= c_W < 0 and {-d2_bound / 2.0} <= c_W < 0; strictest lower magnitude applies",
            "zero_region": "c_W=0 or exact GB-safe route",
            "valid_for_claim": False,
        },
    ]


def evaluate_parent_basis_row(row: Dict[str, str], bounds: Sequence[Dict[str, str]]) -> Dict[str, object]:
    c_r2 = as_float(row.get("c_R2_m2"))
    c_ric = as_float(row.get("c_Ric_m2"))
    c_w = as_float(row.get("c_Weyl_m2"))
    c_riem = as_float(row.get("c_Riemann_m2"))
    source_path = str(row.get("source_path", ""))
    source_exists = bool(source_path and Path(source_path).exists())
    has_numbers = all(value is not None for value in [c_r2, c_ric, c_w, c_riem])
    scalar = next(item for item in bounds if item.get("bound_id") == "QB4457_0_scalar_D0")
    spin2 = next(item for item in bounds if item.get("bound_id") == "QB4457_1_spin2_D2")
    d0_bound = as_float(scalar.get("coefficient_upper_bound_m2"))
    d2_bound = as_float(spin2.get("coefficient_upper_bound_m2"))
    if has_numbers and d0_bound is not None and d2_bound is not None:
        alpha_qg = c_r2 - (2.0 / 3.0) * c_w - c_riem
        beta_qg = c_ric + 2.0 * c_w + 4.0 * c_riem
        d0 = 12.0 * alpha_qg + beta_qg
        d2 = -beta_qg
        scalar_pass = 0.0 < d0 <= d0_bound
        spin2_pass = 0.0 < d2 <= d2_bound
        verdict = "PASS_NONCLAIM" if scalar_pass and spin2_pass and source_exists else "FAIL_OR_UNSOURCED_NONCLAIM"
    else:
        alpha_qg = ""
        beta_qg = ""
        d0 = ""
        d2 = ""
        scalar_pass = False
        spin2_pass = False
        verdict = "REJECTED_MISSING_PARENT_BASIS_COEFFICIENTS_OR_SOURCE"
    return {
        "candidate_id": row.get("candidate_id"),
        "source_path": source_path,
        "source_exists": source_exists,
        "has_numeric_basis_coefficients": has_numbers,
        "alpha_QG_m2": alpha_qg,
        "beta_QG_m2": beta_qg,
        "D0_m2": d0,
        "D2_m2": d2,
        "scalar_region_pass_nonclaim": scalar_pass,
        "spin2_region_pass_nonclaim": spin2_pass,
        "verdict": verdict,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
