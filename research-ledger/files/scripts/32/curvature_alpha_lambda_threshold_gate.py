from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Dict, Iterable, List, Sequence


HBAR_C_EV_M = 1.973269804e-7


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass"}


def as_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


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


def parse_curve_rows(rows: Sequence[Dict[str, str]]) -> List[Dict[str, object]]:
    parsed: List[Dict[str, object]] = []
    for row in rows:
        lambda_m = as_float(row.get("lambda_m"))
        alpha_abs_bound = as_float(row.get("alpha_bound_abs"))
        if lambda_m is None or alpha_abs_bound is None:
            continue
        if lambda_m <= 0 or alpha_abs_bound <= 0:
            continue
        parsed.append(
            {
                "curve_row_id": row.get("curve_row_id") or row.get("point_id") or "",
                "lambda_m": lambda_m,
                "lambda_um": lambda_m * 1e6,
                "alpha_bound_abs": alpha_abs_bound,
                "source_file": row.get("source_file") or row.get("figure_file") or "",
                "valid_for_claim": as_bool(row.get("valid_for_claim")),
                "confidence": row.get("confidence") or row.get("review_status") or "",
            }
        )
    parsed.sort(key=lambda item: float(item["lambda_m"]))
    return parsed


def interpolate_threshold(curve: Sequence[Dict[str, object]], target_alpha_abs: float) -> Dict[str, object]:
    if target_alpha_abs <= 0:
        return {
            "threshold_found": False,
            "threshold_status": "INVALID_TARGET_ALPHA",
            "lambda_threshold_m": "",
            "lambda_threshold_um": "",
            "mass_threshold_eV": "",
            "bracket_low_id": "",
            "bracket_high_id": "",
            "bracket_low_alpha": "",
            "bracket_high_alpha": "",
        }
    exact = [
        row
        for row in curve
        if abs(float(row["alpha_bound_abs"]) - target_alpha_abs) <= max(1e-12, target_alpha_abs * 1e-9)
    ]
    if exact:
        chosen = exact[0]
        lambda_m = float(chosen["lambda_m"])
        return {
            "threshold_found": True,
            "threshold_status": "EXACT_CANDIDATE_ROW",
            "lambda_threshold_m": lambda_m,
            "lambda_threshold_um": lambda_m * 1e6,
            "mass_threshold_eV": HBAR_C_EV_M / lambda_m,
            "bracket_low_id": chosen["curve_row_id"],
            "bracket_high_id": chosen["curve_row_id"],
            "bracket_low_alpha": chosen["alpha_bound_abs"],
            "bracket_high_alpha": chosen["alpha_bound_abs"],
        }

    crossings: List[Dict[str, object]] = []
    for left, right in zip(curve, curve[1:]):
        left_alpha = float(left["alpha_bound_abs"])
        right_alpha = float(right["alpha_bound_abs"])
        if (left_alpha - target_alpha_abs) * (right_alpha - target_alpha_abs) > 0:
            continue
        if left_alpha == right_alpha:
            continue
        x_left = math.log(float(left["lambda_m"]))
        x_right = math.log(float(right["lambda_m"]))
        y_left = math.log(left_alpha)
        y_right = math.log(right_alpha)
        y_target = math.log(target_alpha_abs)
        fraction = (y_target - y_left) / (y_right - y_left)
        if fraction < -1e-9 or fraction > 1 + 1e-9:
            continue
        lambda_m = math.exp(x_left + fraction * (x_right - x_left))
        crossings.append(
            {
                "threshold_found": True,
                "threshold_status": "LOG_LOG_INTERPOLATED_CANDIDATE",
                "lambda_threshold_m": lambda_m,
                "lambda_threshold_um": lambda_m * 1e6,
                "mass_threshold_eV": HBAR_C_EV_M / lambda_m,
                "bracket_low_id": left["curve_row_id"],
                "bracket_high_id": right["curve_row_id"],
                "bracket_low_alpha": left_alpha,
                "bracket_high_alpha": right_alpha,
            }
        )

    if not crossings:
        return {
            "threshold_found": False,
            "threshold_status": "TARGET_NOT_BRACKETED_BY_CANDIDATE_CURVE",
            "lambda_threshold_m": "",
            "lambda_threshold_um": "",
            "mass_threshold_eV": "",
            "bracket_low_id": "",
            "bracket_high_id": "",
            "bracket_low_alpha": "",
            "bracket_high_alpha": "",
        }
    return crossings[0]


def evaluate_channel_threshold(row: Dict[str, object], curve: Sequence[Dict[str, object]]) -> Dict[str, object]:
    alpha_standard = as_float(row.get("alpha_standard"))
    alpha_abs = abs(alpha_standard) if alpha_standard is not None else None
    if alpha_abs is None:
        threshold = interpolate_threshold(curve, -1.0)
        alpha_abs = float("nan")
    else:
        threshold = interpolate_threshold(curve, alpha_abs)
    curve_claim_ready = bool(curve) and all(bool(item["valid_for_claim"]) for item in curve)
    threshold_found = as_bool(threshold.get("threshold_found"))
    return {
        "channel_id": row.get("channel_id"),
        "mode": row.get("mode"),
        "alpha_standard": alpha_standard if alpha_standard is not None else "",
        "alpha_abs": alpha_abs if math.isfinite(alpha_abs) else "",
        "lambda_symbol": row.get("lambda_symbol"),
        "mass_symbol": row.get("mass_symbol"),
        **threshold,
        "candidate_curve_rows": len(curve),
        "candidate_curve_claim_ready": curve_claim_ready,
        "derived_parent_mass_rule": (
            f"{row.get('mass_symbol')} >= {threshold.get('mass_threshold_eV')} eV"
            if threshold_found
            else "UNAVAILABLE"
        ),
        "derived_parent_range_rule": (
            f"{row.get('lambda_symbol')} <= {threshold.get('lambda_threshold_um')} micrometer"
            if threshold_found
            else "UNAVAILABLE"
        ),
        "score_ready_nonclaim": threshold_found,
        "valid_for_claim": False,
        "claim_allowed": False,
        "claim_blocker": "CANDIDATE_CURVE_NOT_CLAIM_READY;MTS_PARENT_MASS_VALUE_MISSING;SIGNED_PLUS_MINUS_SUPPLEMENTAL_ROWS_MISSING",
    }


def curve_quality_rows(curve: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
    lambdas = [float(row["lambda_m"]) for row in curve]
    alphas = [float(row["alpha_bound_abs"]) for row in curve]
    has_anchor = any(abs(float(row["lambda_um"]) - 38.6) < 0.05 and abs(float(row["alpha_bound_abs"]) - 1.0) < 1e-6 for row in curve)
    return [
        {
            "quality_id": "CQ4456_0_positive_numeric",
            "passed": bool(curve) and all(value > 0 for value in lambdas + alphas),
            "detail": "all candidate lambda and alpha rows are positive numeric",
            "valid_for_claim": False,
        },
        {
            "quality_id": "CQ4456_1_sorted_lambda",
            "passed": lambdas == sorted(lambdas),
            "detail": "candidate curve sorted by lambda",
            "valid_for_claim": False,
        },
        {
            "quality_id": "CQ4456_2_official_anchor_reproduced",
            "passed": has_anchor,
            "detail": "candidate includes alpha=1 at approximately 38.6 micrometer",
            "valid_for_claim": False,
        },
        {
            "quality_id": "CQ4456_3_nonclaim_firewall",
            "passed": bool(curve) and not any(bool(row["valid_for_claim"]) for row in curve),
            "detail": "candidate rows remain nonclaim until supplemental/manual review",
            "valid_for_claim": False,
        },
    ]

