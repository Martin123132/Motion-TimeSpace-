from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
INPUT = OUT / "P8_Y5_R2FR_3122_CJ_COEFFICIENT_FILL_INPUTS.csv"
OUTPUT = OUT / "P8_Y5_R2FR_3122_CJ_COEFFICIENT_FILL_OUTPUT.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3122_VALIDATION.csv"


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


def parse_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    if not math.isfinite(parsed):
        return None
    return parsed


def is_true(value: object) -> bool:
    return str(value).strip().lower() == "true"


def has_nonclaim_marker(value: object) -> bool:
    text = str(value)
    return any(marker in text for marker in ("MISSING", "SMOKE", "NOT_CLAIM", "REQUIRES"))


def source_path(path_text: str) -> Path:
    path = Path(path_text)
    if path.is_absolute():
        return path
    root_candidate = ROOT / path_text
    if root_candidate.exists():
        return root_candidate
    return OUT / path_text


def find_row(rows: list[dict[str, str]], row_id: str) -> dict[str, str] | None:
    if not row_id:
        return None
    for row in rows:
        if row_id in row.values():
            return row
    return None


def source_row(row: dict[str, str], key: str = "source_row_id") -> tuple[dict[str, str] | None, Path]:
    path = source_path(row.get("source_file", ""))
    return find_row(read_csv(path), row.get(key, "")), path


def eta_bound(row: dict[str, str]) -> tuple[float | None, str, Path]:
    path = source_path(row.get("eta_bound_file", ""))
    source = find_row(read_csv(path), row.get("eta_bound_row_id", ""))
    if source is None:
        return None, "eta_source_row_missing", path
    column = row.get("eta_bound_column", "")
    return parse_float(source.get(column, "")), source.get("units", ""), path


def q_alpha_from_source(row: dict[str, str], row_id_key: str) -> tuple[float | None, str]:
    path = source_path(row.get("source_file", ""))
    source = find_row(read_csv(path), row.get(row_id_key, ""))
    if source is None:
        return None, "source_row_missing"
    if source.get("channel") != "Q_alpha_Coulomb":
        return parse_float(source.get("charge_value", "")), f"source_channel={source.get('channel', '')}"
    return parse_float(source.get("charge_value", "")), "Q_alpha_Coulomb"


def cj_from_q(q_alpha: float | None, tau_em: float | None, c_relax: float | None) -> float | None:
    if q_alpha is None or tau_em is None or c_relax is None:
        return None
    return 2.0 * tau_em * q_alpha + c_relax


def evaluate_row(row: dict[str, str]) -> dict[str, Any]:
    issues: list[str] = []
    row_type = row.get("row_type", "")
    tau_em = parse_float(row.get("tau_EM", ""))
    c_relax = parse_float(row.get("C_relax", ""))
    eta, eta_units, eta_path = eta_bound(row)
    source_file_path = source_path(row.get("source_file", ""))

    q_alpha, q_status = q_alpha_from_source(row, "source_row_id")
    comparison_q_alpha: float | None = None
    comparison_status = ""
    if row.get("comparison_source_row_id", ""):
        comparison_q_alpha, comparison_status = q_alpha_from_source(row, "comparison_source_row_id")

    cj_value = cj_from_q(q_alpha, tau_em, c_relax)
    comparison_cj = cj_from_q(comparison_q_alpha, tau_em, c_relax) if comparison_q_alpha is not None else None
    delta_cj: float | str = ""
    delta_j_bound: float | str = ""

    if row_type == "differential_pair" and cj_value is not None and comparison_cj is not None:
        delta_cj = cj_value - comparison_cj
        if eta is not None and abs(delta_cj) > 0:
            delta_j_bound = eta / abs(delta_cj)

    if row_type == "single_material" and cj_value is None:
        issues.append("CJ_NOT_NUMERIC")
    if row_type == "differential_pair":
        if not isinstance(delta_cj, float):
            issues.append("DELTA_CJ_NOT_NUMERIC")
        if not isinstance(delta_j_bound, float):
            issues.append("DELTAJ_BOUND_NOT_NUMERIC")
    if tau_em is None:
        issues.append("TAU_EM_NOT_NUMERIC")
    if c_relax is None:
        issues.append("C_RELAX_NOT_NUMERIC")
    if q_alpha is None:
        issues.append("Q_ALPHA_NOT_NUMERIC")
    if row.get("comparison_source_row_id", "") and comparison_q_alpha is None:
        issues.append("COMPARISON_Q_ALPHA_NOT_NUMERIC")
    if eta is None:
        issues.append("ETA_BOUND_NOT_NUMERIC")
    if not source_file_path.exists():
        issues.append("SOURCE_FILE_MISSING")
    if not eta_path.exists():
        issues.append("ETA_BOUND_FILE_MISSING")
    if has_nonclaim_marker(row.get("assumptions_status", "")):
        issues.append(row.get("assumptions_status", "NONCLAIM_ASSUMPTION"))
    if not is_true(row.get("valid_for_claim", "")):
        issues.append("INPUT_VALID_FOR_CLAIM_FALSE")

    claim_allowed = not issues
    return {
        "coefficient_id": row.get("coefficient_id", ""),
        "row_type": row_type,
        "object": row.get("object", ""),
        "q_alpha": q_alpha if q_alpha is not None else "",
        "q_alpha_status": q_status,
        "comparison_q_alpha": comparison_q_alpha if comparison_q_alpha is not None else "",
        "comparison_status": comparison_status,
        "tau_EM": row.get("tau_EM", ""),
        "C_relax": row.get("C_relax", ""),
        "C_J": cj_value if cj_value is not None else "",
        "comparison_C_J": comparison_cj if comparison_cj is not None else "",
        "delta_C_J": delta_cj,
        "eta_bound": eta if eta is not None else "",
        "eta_units": eta_units,
        "deltaJ_bound_abs": delta_j_bound,
        "score": "computed_nonclaim" if (cj_value is not None or isinstance(delta_j_bound, float)) else "not_scoreable",
        "claim_allowed": str(claim_allowed).lower(),
        "valid_for_claim": str(claim_allowed).lower(),
        "issues": ";".join(issues),
        "source_path": str(source_file_path),
        "eta_bound_path": str(eta_path),
        "source_row_id": row.get("source_row_id", ""),
        "comparison_source_row_id": row.get("comparison_source_row_id", ""),
        "generated_utc": stamp(),
    }


def validate(rows: list[dict[str, str]], outputs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    required = [
        "coefficient_id",
        "row_type",
        "object",
        "source_file",
        "source_row_id",
        "tau_EM",
        "C_relax",
        "eta_bound_file",
        "eta_bound_row_id",
        "eta_bound_column",
        "assumptions_status",
        "valid_for_claim",
    ]
    columns = set(rows[0].keys()) if rows else set()
    missing_columns = [column for column in required if column not in columns]
    source_status = {
        row.get("coefficient_id", ""): Path(row.get("source_path", "")).exists()
        for row in outputs
    }
    eta_status = {
        row.get("coefficient_id", ""): Path(row.get("eta_bound_path", "")).exists()
        for row in outputs
    }
    differential = [row for row in outputs if row.get("coefficient_id") == "CJF3122_3"]
    validations: list[dict[str, Any]] = [
        {
            "check_id": "VAL3122_0_input_schema",
            "status": "pass" if rows and not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3122_1_all_outputs_nonclaim",
            "status": "pass" if outputs and all(not is_true(row.get("claim_allowed", "")) for row in outputs) else "fail",
            "details": f"output_rows={len(outputs)}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3122_2_source_paths_resolve",
            "status": "pass" if outputs and all(source_status.values()) and all(eta_status.values()) else "fail",
            "details": json.dumps({"source": source_status, "eta": eta_status}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3122_3_CJ_values_computed",
            "status": "pass" if any(row.get("coefficient_id") == "CJF3122_1" and row.get("C_J") for row in outputs) and any(row.get("coefficient_id") == "CJF3122_2" and row.get("C_J") for row in outputs) else "fail",
            "details": json.dumps({row["coefficient_id"]: row.get("C_J", "") for row in outputs}, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3122_4_deltaJ_envelope_computed",
            "status": "pass" if differential and differential[0].get("deltaJ_bound_abs") not in ("", None) else "fail",
            "details": json.dumps(differential[0] if differential else {}, sort_keys=True),
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
