from __future__ import annotations

import csv
import sys
from pathlib import Path
from typing import Any


CERTIFICATE_CLAUSES = (
    "parent_q_signed",
    "NX_integrability_signed",
    "Dq_vX_zero_signed",
    "action_descent_signed",
    "matter_descent_signed",
    "constants_marker_silence_signed",
    "hidden_frame_exclusion_signed",
    "vertical_generator_signed",
    "momentum_map_signed",
    "boundary_silence_signed",
    "degree_count_signed",
    "no_GR_import_signed",
    "no_fit_to_bound_signed",
)

FORBIDDEN_SOURCE_TOKENS = (
    "GR_IMPORT",
    "FIT_TO_BOUND",
    "BOUND_AS_SOURCE",
    "ORBITAL_GM_AS_SOURCE",
    "POST_READOUT_QUOTIENT",
    "SCALAR_NOHAIR_AS_EDGE_EXACTNESS",
    "SOURCE_FREE_BY_ASSERTION",
    "CANCEL_UNKNOWN_COMPONENTS",
    "ASSERT_VERTICALITY_AFTER_READOUT",
)


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "y", "pass", "signed"}


def forbidden_source_used(row: dict[str, Any]) -> bool:
    text = " ".join(
        str(row.get(field, ""))
        for field in (
            "certificate_id",
            "source_path",
            "equation_ref",
            "current_evidence",
            "notes",
            "provenance",
        )
    ).upper()
    return any(token in text for token in FORBIDDEN_SOURCE_TOKENS)


def missing_clauses(row: dict[str, Any]) -> list[str]:
    return [clause for clause in CERTIFICATE_CLAUSES if not bool_text(row.get(clause))]


def certificate_row(row: dict[str, Any]) -> dict[str, Any]:
    certificate_id = str(row.get("certificate_id", "")).strip() or "UNNAMED_QVX_CERTIFICATE"
    output: dict[str, Any] = {
        "certificate_id": certificate_id,
        "route": row.get("route", ""),
        "required_object": row.get("required_object", ""),
        "claim_effect_if_signed": row.get("claim_effect_if_signed", ""),
        "valid_for_claim": False,
        "claim_allowed": False,
    }
    if forbidden_source_used(row):
        output.update(
            {
                "certificate_status": "FAILED_QVX_CERTIFICATE_GATE",
                "certificate_theorem": False,
                "missing_for_claim": "FORBIDDEN_SOURCE_OR_CIRCULAR_ROUTE",
                "anti_circularity_status": "FAIL_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    missing = missing_clauses(row)
    if missing:
        output.update(
            {
                "certificate_status": "BLOCKED_MISSING_QVX_CERTIFICATE_INPUTS",
                "certificate_theorem": False,
                "missing_for_claim": ";".join(missing),
                "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
            }
        )
        return output
    output.update(
        {
            "certificate_status": "QVX_CERTIFICATE_SIGNED_CONDITIONAL_NONCLAIM",
            "certificate_theorem": True,
            "missing_for_claim": "",
            "anti_circularity_status": "PASS_NO_FORBIDDEN_SOURCE_USED",
        }
    )
    return output


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(dict.fromkeys(field for row in rows for field in row))
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: q_vX_action_descent_certificate_runner.py INPUT_CSV OUTPUT_CSV", file=sys.stderr)
        return 2
    outputs = [certificate_row(row) for row in read_csv(Path(sys.argv[1]))]
    write_csv(Path(sys.argv[2]), outputs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
