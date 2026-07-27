from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
INPUT = OUT / "P8_Y5_R2FR_3123_DELTAJ_PROJECTION_CLASSIFIER_INPUTS.csv"
OUTPUT = OUT / "P8_Y5_R2FR_3123_DELTAJ_PROJECTION_CLASSIFIER_OUTPUT.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3123_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if fieldnames is None:
        fieldnames = []
        for row in rows:
            for key in row:
                if key not in fieldnames:
                    fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def is_true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    root_candidate = ROOT / path_text
    if root_candidate.exists():
        return root_candidate
    return OUT / path_text


def source_paths_resolve(source_paths: str) -> tuple[bool, str]:
    resolved: list[str] = []
    missing: list[str] = []
    for item in source_paths.split(";"):
        item = item.strip()
        if not item:
            continue
        path = source_path(item)
        if path.exists():
            resolved.append(str(path))
        else:
            missing.append(str(path))
    return not missing, json.dumps({"resolved": resolved, "missing": missing}, sort_keys=True)


def all_signed(row: dict[str, str]) -> bool:
    required = [
        "parent_TQ_status",
        "fixed_nA_status",
        "qbasic_matter_status",
        "no_cA_slot_status",
        "variation_before_readout_status",
        "radiative_closure_status",
    ]
    return all(row.get(key, "") == "signed" for key in required)


def classify(row: dict[str, str]) -> dict[str, Any]:
    stage = row.get("insertion_stage", "")
    material = row.get("material_projection", "")
    source_profile = row.get("source_profile", "")
    calibration = row.get("calibration_status", "")

    classification = "UNCLASSIFIED_RETAIN"
    projects_material = False
    projects_source_gm = False
    observable_source_gm = False
    projects_wep = False
    projects_r10 = False
    projection_reason = ""

    if all_signed(row) or stage in {"forbidden_by_qbasic_action", "forbidden_by_parent_grammar"}:
        classification = "ZERO_BY_ACTION_VARIATION" if all_signed(row) else "ZERO_CONDITIONAL_UNSIGNED"
        projection_reason = "q-basic action variation commutes with Lie_v only after all owner clauses are signed"
    elif stage == "before_maxwell_and_hilbert_variation":
        projects_material = material in {"differential_material", "universal_material"}
        projects_source_gm = True
        projects_r10 = True
        if calibration == "calibrated_same_convention" and source_profile == "universal_constant":
            classification = "FINITE_CALIBRATION_ONLY"
            observable_source_gm = False
            projects_wep = False
            projection_reason = "raw current-unit rescaling is absorbed by shared calibration unless differential/time/source dependence appears"
        else:
            classification = "FINITE_BEFORE_VARIATION_PROJECTS_BOTH"
            observable_source_gm = True
            projects_wep = material == "differential_material"
            projection_reason = "current factor enters Maxwell solution and Hilbert stress before variation"
    elif stage == "after_action_variation_before_observed_readout":
        classification = "FINITE_READOUT_ONLY_NO_GM"
        projects_material = material in {"differential_readout", "universal_material"}
        projects_source_gm = False
        observable_source_gm = False
        projects_wep = material == "differential_readout"
        projects_r10 = True
        projection_reason = "readout selector is after Hilbert variation, so it does not change EM stress/source GM"
    elif stage == "effective_action_reentry":
        classification = "FINITE_EFFECTIVE_ACTION_AMBIGUOUS"
        projects_material = True
        projects_source_gm = True
        observable_source_gm = source_profile != "universal_constant"
        projects_wep = material in {"differential_material", "ambiguous"}
        projects_r10 = True
        projection_reason = "effective threshold must be split into before-variation versus readout-only re-entry"

    return {
        "classification": classification,
        "projects_material_coulomb": str(projects_material).lower(),
        "projects_source_GM_raw": str(projects_source_gm).lower(),
        "projects_source_GM_observable": str(observable_source_gm).lower(),
        "projects_WEP": str(projects_wep).lower(),
        "projects_R10": str(projects_r10).lower(),
        "projection_reason": projection_reason,
    }


def evaluate_row(row: dict[str, str]) -> dict[str, Any]:
    sources_ok, source_details = source_paths_resolve(row.get("source_paths", ""))
    result = classify(row)
    issues: list[str] = []
    if not sources_ok:
        issues.append("SOURCE_PATH_MISSING")
    if result["classification"] == "ZERO_CONDITIONAL_UNSIGNED":
        issues.append("ZERO_ROUTE_UNSIGNED")
    if any(row.get(key, "") in {"unsigned", "partial"} for key in row if key.endswith("_status")):
        issues.append("PARENT_CLAUSES_UNSIGNED")
    if "fails" in ";".join(row.get(key, "") for key in row if key.endswith("_status")):
        issues.append("COUNTERMODEL_OR_FAILED_CLAUSE_PRESENT")
    if "ambiguous" in row.get("source_profile", "") or "ambiguous" in row.get("material_projection", ""):
        issues.append("PROJECTION_STAGE_AMBIGUOUS")
    if not is_true(row.get("valid_for_claim", "")):
        issues.append("INPUT_VALID_FOR_CLAIM_FALSE")

    claim_allowed = not issues and result["classification"] == "ZERO_BY_ACTION_VARIATION"
    return {
        "case_id": row.get("case_id", ""),
        "case_type": row.get("case_type", ""),
        "insertion_stage": row.get("insertion_stage", ""),
        **result,
        "claim_allowed": str(claim_allowed).lower(),
        "valid_for_claim": str(claim_allowed).lower(),
        "issues": ";".join(issues),
        "source_paths_resolve": str(sources_ok).lower(),
        "source_details": source_details,
        "notes": row.get("notes", ""),
        "generated_utc": stamp(),
    }


def validate(rows: list[dict[str, str]], outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    required = [
        "case_id",
        "case_type",
        "insertion_stage",
        "parent_TQ_status",
        "fixed_nA_status",
        "qbasic_matter_status",
        "no_cA_slot_status",
        "variation_before_readout_status",
        "radiative_closure_status",
        "material_projection",
        "source_profile",
        "calibration_status",
        "source_paths",
        "valid_for_claim",
    ]
    columns = set(rows[0].keys()) if rows else set()
    missing_columns = [column for column in required if column not in columns]
    classifications = {row.get("classification", "") for row in outputs}
    validations: list[dict[str, Any]] = [
        {
            "check_id": "VAL3123_0_input_schema",
            "status": "pass" if rows and not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3123_1_all_outputs_nonclaim",
            "status": "pass" if outputs and all(not is_true(row.get("claim_allowed", "")) for row in outputs) else "fail",
            "details": f"output_rows={len(outputs)}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3123_2_source_paths_resolve",
            "status": "pass" if outputs and all(is_true(row.get("source_paths_resolve", "")) for row in outputs) else "fail",
            "details": json.dumps({row["case_id"]: row.get("source_details", "") for row in outputs}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3123_3_required_classifications_present",
            "status": "pass" if {"ZERO_BY_ACTION_VARIATION", "FINITE_BEFORE_VARIATION_PROJECTS_BOTH", "FINITE_CALIBRATION_ONLY", "FINITE_READOUT_ONLY_NO_GM", "FINITE_EFFECTIVE_ACTION_AMBIGUOUS"}.issubset(classifications) else "fail",
            "details": json.dumps(sorted(classifications)),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3123_4_before_variation_projects_both",
            "status": "pass" if any(row.get("classification") == "FINITE_BEFORE_VARIATION_PROJECTS_BOTH" and is_true(row.get("projects_material_coulomb")) and is_true(row.get("projects_source_GM_observable")) for row in outputs) else "fail",
            "details": "before-variation c_A branch must project to material and source GM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3123_5_readout_has_no_GM",
            "status": "pass" if any(row.get("classification") == "FINITE_READOUT_ONLY_NO_GM" and not is_true(row.get("projects_source_GM_raw")) for row in outputs) else "fail",
            "details": "post-variation readout branch must not source Hilbert GM",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return validations


def main() -> None:
    rows = read_csv(INPUT)
    outputs = [evaluate_row(row) for row in rows]
    write_csv(OUTPUT, outputs)
    write_csv(VALIDATION, validate(rows, outputs))
    print(
        json.dumps(
            {
                "input_rows": len(rows),
                "output_rows": len(outputs),
                "output": str(OUTPUT),
                "validation": str(VALIDATION),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
