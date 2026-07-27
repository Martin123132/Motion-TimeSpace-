from __future__ import annotations

import argparse
import csv
from pathlib import Path
from typing import Dict, Iterable, List


TRUE_VALUES = {"1", "true", "yes", "y", "pass", "ready", "proved", "signed"}


def as_bool(value: object) -> bool:
    return str(value).strip().lower() in TRUE_VALUES


def as_float(value: object) -> float | None:
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def path_exists(value: object) -> bool:
    text = str(value).strip()
    return bool(text) and Path(text).exists()


def url_recorded(value: object) -> bool:
    text = str(value).strip().lower()
    return text.startswith("https://") or text.startswith("http://")


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    materialized = [{key: str(value) for key, value in row.items()} for row in rows]
    path.parent.mkdir(parents=True, exist_ok=True)
    if not materialized:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(materialized[0].keys()))
        writer.writeheader()
        writer.writerows(materialized)


def evaluate_mode_row(row: Dict[str, str]) -> Dict[str, object]:
    source_ok = path_exists(row.get("source_path", ""))
    mode_written = as_bool(row.get("mode_written", "False"))
    potential_projection = as_bool(row.get("potential_projection_written", "False"))
    alpha_fixed = as_bool(row.get("alpha_projection_fixed", "False"))
    mass_scale_parent_signed = as_bool(row.get("mass_scale_parent_signed", "False"))
    numeric_scale = as_bool(row.get("numeric_scale_available", "False"))
    public_claim_false = as_bool(row.get("public_claim_false", "True"))

    if source_ok and mode_written and potential_projection and alpha_fixed and mass_scale_parent_signed and numeric_scale:
        status = "CURVATURE_MODE_NUMERIC_SCALE_READY"
    elif source_ok and mode_written and potential_projection:
        status = "CURVATURE_MODE_SYMBOLIC_YUKAWA_PROJECTION_READY_SCALE_OR_ALPHA_MISSING"
    elif source_ok and mode_written:
        status = "CURVATURE_MODE_WRITTEN_PROJECTION_OPEN"
    elif source_ok:
        status = "SOURCE_PRESENT_MODE_OPEN"
    else:
        status = "SOURCE_MISSING"

    valid_for_claim = source_ok and mode_written and potential_projection and alpha_fixed and mass_scale_parent_signed and numeric_scale and not public_claim_false
    reasons = []
    if not source_ok:
        reasons.append("SOURCE_PATH_MISSING")
    if not mode_written:
        reasons.append("MODE_WRITTEN_FALSE")
    if not potential_projection:
        reasons.append("POTENTIAL_PROJECTION_WRITTEN_FALSE")
    if not alpha_fixed:
        reasons.append("ALPHA_PROJECTION_FIXED_FALSE")
    if not mass_scale_parent_signed:
        reasons.append("MASS_SCALE_PARENT_SIGNED_FALSE")
    if not numeric_scale:
        reasons.append("NUMERIC_SCALE_AVAILABLE_FALSE")
    if public_claim_false:
        reasons.append("PUBLIC_CLAIM_FALSE")

    return {
        "mode_id": row.get("mode_id", ""),
        "mode": row.get("mode", ""),
        "source_path": row.get("source_path", ""),
        "source_exists": source_ok,
        "linearized_effect": row.get("linearized_effect", ""),
        "potential_projection": row.get("potential_projection", ""),
        "mode_written": mode_written,
        "potential_projection_written": potential_projection,
        "alpha_projection_fixed": alpha_fixed,
        "mass_scale_parent_signed": mass_scale_parent_signed,
        "numeric_scale_available": numeric_scale,
        "current_status": status,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
    }


def evaluate_bound_row(row: Dict[str, str]) -> Dict[str, object]:
    url_ok = url_recorded(row.get("source_url", ""))
    source_verified = as_bool(row.get("source_verified", "False"))
    lambda_anchor_um = as_float(row.get("lambda_anchor_um", ""))
    alpha_anchor = as_float(row.get("alpha_anchor", ""))
    mass_floor_eV = as_float(row.get("mass_floor_eV", ""))
    numeric_anchor = lambda_anchor_um is not None and alpha_anchor is not None and mass_floor_eV is not None
    full_curve = as_bool(row.get("full_curve_available", "False"))
    projection_ready = as_bool(row.get("projection_to_cR2_ready", "False"))
    public_claim_false = as_bool(row.get("public_claim_false", "True"))

    if url_ok and source_verified and numeric_anchor and full_curve and projection_ready:
        status = "R10_CURVE_PROJECTION_READY"
    elif url_ok and source_verified and numeric_anchor:
        status = "R10_GRAVITATIONAL_STRENGTH_ANCHOR_READY_FULL_CURVE_OR_PROJECTION_MISSING"
    elif url_ok and source_verified:
        status = "R10_SOURCE_VERIFIED_NUMERIC_ANCHOR_MISSING"
    elif url_ok:
        status = "SOURCE_URL_RECORDED_UNVERIFIED"
    else:
        status = "SOURCE_URL_MISSING"

    valid_for_claim = url_ok and source_verified and numeric_anchor and full_curve and projection_ready and not public_claim_false
    reasons = []
    if not url_ok:
        reasons.append("SOURCE_URL_MISSING")
    if not source_verified:
        reasons.append("SOURCE_VERIFIED_FALSE")
    if not numeric_anchor:
        reasons.append("NUMERIC_ANCHOR_MISSING")
    if not full_curve:
        reasons.append("FULL_CURVE_AVAILABLE_FALSE")
    if not projection_ready:
        reasons.append("PROJECTION_TO_CR2_READY_FALSE")
    if public_claim_false:
        reasons.append("PUBLIC_CLAIM_FALSE")

    return {
        "bound_id": row.get("bound_id", ""),
        "arena": row.get("arena", ""),
        "source_url": row.get("source_url", ""),
        "source_url_recorded": url_ok,
        "source_verified": source_verified,
        "observable": row.get("observable", ""),
        "lambda_anchor_um": "" if lambda_anchor_um is None else lambda_anchor_um,
        "alpha_anchor": "" if alpha_anchor is None else alpha_anchor,
        "mass_floor_eV": "" if mass_floor_eV is None else mass_floor_eV,
        "numeric_anchor_ready": numeric_anchor,
        "full_curve_available": full_curve,
        "projection_to_cR2_ready": projection_ready,
        "current_status": status,
        "valid_for_claim": valid_for_claim,
        "claim_allowed": valid_for_claim,
        "refusal_reasons": ";".join(dict.fromkeys(reasons)),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate curvature-square mode scale and short-range/orbital bound rows.")
    parser.add_argument("--mode", choices=["modes", "bounds"], required=True)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    rows = read_csv(args.input)
    output = [evaluate_mode_row(row) for row in rows] if args.mode == "modes" else [evaluate_bound_row(row) for row in rows]
    write_csv(args.output, output)


if __name__ == "__main__":
    main()
