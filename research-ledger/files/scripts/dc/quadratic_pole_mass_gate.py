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


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass"}


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


def coefficient_bounds_from_thresholds(threshold_rows: Sequence[Dict[str, str]]) -> List[Dict[str, object]]:
    output: List[Dict[str, object]] = []
    for row in threshold_rows:
        channel_id = row.get("channel_id", "")
        lambda_threshold_um = as_float(row.get("lambda_threshold_um"))
        mass_threshold_eV = as_float(row.get("mass_threshold_eV"))
        if lambda_threshold_um is None or mass_threshold_eV is None:
            continue
        lambda_m = lambda_threshold_um * 1e-6
        if channel_id == "CH4456_0_scalar":
            denominator_bound_m2 = 4.0 * lambda_m**2
            output.append(
                {
                    "bound_id": "QB4457_0_scalar_D0",
                    "source_channel_id": channel_id,
                    "canonical_denominator": "D0 = 12*alpha_QG + beta_QG",
                    "tachyon_free_condition": "D0 > 0",
                    "range_pass_condition": "D0 <= 4*lambda_0_star^2",
                    "lambda_threshold_um": lambda_threshold_um,
                    "mass_threshold_eV": mass_threshold_eV,
                    "coefficient_upper_bound_m2": denominator_bound_m2,
                    "coefficient_upper_bound_um2": denominator_bound_m2 * 1e12,
                    "claim_status": "PRIVATE_SMOKE_ONLY_REQUIRES_MTS_NORMALIZATION_MAP",
                    "valid_for_claim": False,
                }
            )
        elif channel_id == "CH4456_1_spin2":
            denominator_bound_m2 = 2.0 * lambda_m**2
            output.append(
                {
                    "bound_id": "QB4457_1_spin2_D2",
                    "source_channel_id": channel_id,
                    "canonical_denominator": "D2 = -beta_QG",
                    "tachyon_free_condition": "D2 > 0, equivalently beta_QG < 0",
                    "range_pass_condition": "D2 <= 2*lambda_2_star^2",
                    "lambda_threshold_um": lambda_threshold_um,
                    "mass_threshold_eV": mass_threshold_eV,
                    "coefficient_upper_bound_m2": denominator_bound_m2,
                    "coefficient_upper_bound_um2": denominator_bound_m2 * 1e12,
                    "claim_status": "PRIVATE_SMOKE_ONLY_REQUIRES_MTS_NORMALIZATION_MAP",
                    "valid_for_claim": False,
                }
            )
    if len(output) == 2:
        scalar = next(row for row in output if row["bound_id"] == "QB4457_0_scalar_D0")
        spin2 = next(row for row in output if row["bound_id"] == "QB4457_1_spin2_D2")
        output.append(
            {
                "bound_id": "QB4457_2_joint_canonical_region",
                "source_channel_id": "CH4456_0_scalar+CH4456_1_spin2",
                "canonical_denominator": "0 < 12*alpha_QG + beta_QG <= D0_star and 0 < -beta_QG <= D2_star",
                "tachyon_free_condition": "12*alpha_QG + beta_QG > 0 and beta_QG < 0",
                "range_pass_condition": f"D0 <= {scalar['coefficient_upper_bound_m2']} m^2; D2 <= {spin2['coefficient_upper_bound_m2']} m^2",
                "lambda_threshold_um": "channelwise",
                "mass_threshold_eV": max(float(scalar["mass_threshold_eV"]), float(spin2["mass_threshold_eV"])),
                "coefficient_upper_bound_m2": "channelwise",
                "coefficient_upper_bound_um2": "channelwise",
                "claim_status": "PRIVATE_SMOKE_ONLY_REQUIRES_PARENT_ALPHA_BETA_VALUES",
                "valid_for_claim": False,
            }
        )
    return output


def evaluate_parent_coefficient_row(row: Dict[str, str], bounds: Sequence[Dict[str, object]]) -> Dict[str, object]:
    alpha_qg = as_float(row.get("alpha_QG_m2"))
    beta_qg = as_float(row.get("beta_QG_m2"))
    source_exists = Path(str(row.get("source_path", ""))).exists()
    has_numbers = alpha_qg is not None and beta_qg is not None
    scalar_bound = next((item for item in bounds if item["bound_id"] == "QB4457_0_scalar_D0"), None)
    spin2_bound = next((item for item in bounds if item["bound_id"] == "QB4457_1_spin2_D2"), None)
    if has_numbers and scalar_bound and spin2_bound:
        d0 = 12.0 * alpha_qg + beta_qg
        d2 = -beta_qg
        scalar_pass = 0.0 < d0 <= float(scalar_bound["coefficient_upper_bound_m2"])
        spin2_pass = 0.0 < d2 <= float(spin2_bound["coefficient_upper_bound_m2"])
        verdict = "PASS_NONCLAIM" if scalar_pass and spin2_pass else "FAIL_OR_TACHYON_NONCLAIM"
    else:
        d0 = ""
        d2 = ""
        scalar_pass = False
        spin2_pass = False
        verdict = "REJECTED_MISSING_PARENT_ALPHA_BETA_OR_SOURCE"
    return {
        "candidate_id": row.get("candidate_id"),
        "alpha_QG_m2": row.get("alpha_QG_m2"),
        "beta_QG_m2": row.get("beta_QG_m2"),
        "normalization_map": row.get("normalization_map"),
        "source_path": row.get("source_path"),
        "source_exists": source_exists,
        "has_numeric_alpha_beta": has_numbers,
        "D0_12alpha_plus_beta_m2": d0,
        "D2_minus_beta_m2": d2,
        "scalar_channel_pass_nonclaim": scalar_pass,
        "spin2_channel_pass_nonclaim": spin2_pass,
        "verdict": verdict,
        "valid_for_claim": False,
        "claim_allowed": False,
    }
