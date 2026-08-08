from __future__ import annotations

import csv
import json
import math
import os
from pathlib import Path
from typing import Any


WORKBENCH = Path(__file__).resolve().parents[1]
FUNCTIONAL_RG = WORKBENCH / "source-intake" / "functional_rg"
SOURCE_5256 = FUNCTIONAL_RG / "5256"
SOURCE_5258 = FUNCTIONAL_RG / "5258"
SOURCE = FUNCTIONAL_RG / "5259"

ERROR_BUDGET_5256 = SOURCE_5256 / "boundary_location_error_budget.csv"
TRANSITIONS_5258 = SOURCE_5258 / "interval_transition_envelopes.csv"
VALIDATION_5258 = SOURCE_5258 / "interval_residue_validation.csv"
RESULT_5258 = SOURCE_5258 / "interval_residue_result.json"

ROWS = SOURCE / "certified_boundary_utility_gate.csv"
VALIDATION = SOURCE / "certified_boundary_utility_validation.csv"
RESULT = SOURCE / "certified_boundary_utility_result.json"

ANGULAR_JACOBIAN = 0.25
EXPECTED_TRANSITIONS = {
    "I01_T00",
    "I01_T01",
    "I06_T00",
    "I06_T01",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def required_bisections(current_width: float, target_width: float) -> int:
    if target_width <= 0.0:
        raise ValueError("target width must be positive")
    if current_width <= target_width:
        return 0
    return math.ceil(math.log2(current_width / target_width))


def execute() -> dict[str, Any]:
    for required in (
        ERROR_BUDGET_5256,
        TRANSITIONS_5258,
        VALIDATION_5258,
        RESULT_5258,
    ):
        if not required.exists():
            raise RuntimeError(f"missing source: {required}")

    budget_lookup = {
        row["transition_id"]: row for row in read_csv(ERROR_BUDGET_5256)
    }
    transition_lookup = {
        row["transition_id"]: row for row in read_csv(TRANSITIONS_5258)
    }
    validation_5258 = read_csv(VALIDATION_5258)
    result_5258 = json.loads(RESULT_5258.read_text(encoding="utf-8"))

    if set(budget_lookup) != EXPECTED_TRANSITIONS:
        raise RuntimeError("checkpoint-5256 transition set is incomplete")
    if set(transition_lookup) != EXPECTED_TRANSITIONS:
        raise RuntimeError("checkpoint-5258 transition set is incomplete")

    rows: list[dict[str, Any]] = []
    for transition_id in sorted(EXPECTED_TRANSITIONS):
        budget_row = budget_lookup[transition_id]
        certificate_row = transition_lookup[transition_id]
        budget = float(budget_row["equal_boundary_budget"])
        current_width = float(certificate_row["bracket_width"])
        certified_envelope = float(
            certificate_row["half_residue_triangle_envelope"]
        )
        certified_error = float(
            certificate_row["boundary_location_error_upper"]
        )
        sampled_envelope = float(
            budget_row["sampled_half_residue_triangle_envelope"]
        )
        target_width = budget / (
            ANGULAR_JACOBIAN * certified_envelope
        )
        envelope_inflation = certified_envelope / sampled_envelope
        error_to_budget = certified_error / budget
        bisections = required_bisections(current_width, target_width)
        if envelope_inflation > 10.0:
            next_action = (
                "TIGHTEN_INTERVAL_ENCLOSURE_THEN_TARGETED_BISECTION"
            )
        else:
            next_action = "TARGETED_BISECTION_WITH_CERTIFIED_ENVELOPE"
        budget_met = certified_error <= budget
        rows.append(
            {
                "transition_id": transition_id,
                "active_endpoint_id": certificate_row[
                    "active_endpoint_id"
                ],
                "current_bracket_width": current_width,
                "equal_boundary_budget": budget,
                "sampled_half_residue_envelope_5256": sampled_envelope,
                "certified_half_residue_envelope_5258": (
                    certified_envelope
                ),
                "certified_to_sampled_envelope_ratio": (
                    envelope_inflation
                ),
                "certified_boundary_error_upper": certified_error,
                "certified_error_to_budget_ratio": error_to_budget,
                "certified_target_width": target_width,
                "additional_binary_bisections_if_envelope_fixed": (
                    bisections
                ),
                "provisional_bisections_from_sampled_5256": int(
                    budget_row[
                        "provisional_remaining_bisection_generations"
                    ]
                ),
                "continuous_residue_envelope_certified": (
                    certificate_row[
                        "continuous_envelope_certified"
                    ].lower()
                    == "true"
                ),
                "boundary_budget_met": budget_met,
                "outer_stopping_gate_passed": budget_met,
                "recommended_next_action": next_action,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )

    reflected_left = next(
        row for row in rows if row["transition_id"] == "I01_T00"
    )
    reflected_right = next(
        row for row in rows if row["transition_id"] == "I06_T01"
    )
    reflection_relative_error = abs(
        reflected_left["certified_half_residue_envelope_5258"]
        - reflected_right["certified_half_residue_envelope_5258"]
    ) / max(
        abs(reflected_left["certified_half_residue_envelope_5258"]),
        1.0,
    )

    checks = [
        {
            "check_id": "SOURCE_5258_VALIDATION_PASSED",
            "passed": all(
                row["passed"].lower() == "true"
                for row in validation_5258
            )
            and bool(result_5258["validation_passed"]),
            "detail": (
                f"checks={len(validation_5258)}; "
                f"result={result_5258['validation_passed']}"
            ),
        },
        {
            "check_id": "CONTINUOUS_CERTIFICATE_PRESENT",
            "passed": bool(
                result_5258[
                    "continuous_residue_envelope_complete"
                ]
            )
            and all(
                bool(row["continuous_residue_envelope_certified"])
                for row in rows
            ),
            "detail": f"rows={len(rows)}",
        },
        {
            "check_id": "CERTIFIED_TARGET_WIDTHS_POSITIVE",
            "passed": all(
                float(row["certified_target_width"]) > 0.0
                for row in rows
            ),
            "detail": (
                "minimum="
                f"{min(float(row['certified_target_width']) for row in rows)}"
            ),
        },
        {
            "check_id": "REFLECTED_ENVELOPES_AGREE",
            "passed": reflection_relative_error <= 1.0e-5,
            "detail": (
                f"relative_error={reflection_relative_error}"
            ),
        },
        {
            "check_id": "BOUNDARY_STOPPING_GATE_NOT_SMUGGLED",
            "passed": all(
                not bool(row["boundary_budget_met"])
                and not bool(row["outer_stopping_gate_passed"])
                for row in rows
            ),
            "detail": (
                "minimum_error_to_budget="
                f"{min(float(row['certified_error_to_budget_ratio']) for row in rows)}"
            ),
        },
        {
            "check_id": "GR_AND_FULL_MTS_CLAIMS_REMAIN_FALSE",
            "passed": all(
                not bool(row["valid_for_numeric_UV_claim"])
                and not bool(row["valid_for_local_GR_claim"])
                and not bool(row["valid_for_full_MTS_claim"])
                for row in rows
            ),
            "detail": "utility gate does not promote downstream claims",
        },
    ]
    passed = all(bool(row["passed"]) for row in checks)
    maximum_inflation = max(
        float(row["certified_to_sampled_envelope_ratio"])
        for row in rows
    )
    maximum_required_bisections = max(
        int(row["additional_binary_bisections_if_envelope_fixed"])
        for row in rows
    )
    result = {
        "marker": "MTS_5259_CERTIFIED_BOUNDARY_UTILITY_AND_GR_HANDOFF_GATE",
        "revision": "certified-boundary-utility-and-gr-handoff-v1",
        "validation_passed": passed,
        "transition_count": len(rows),
        "continuous_residue_envelope_certified": True,
        "all_boundary_budgets_met": all(
            bool(row["boundary_budget_met"]) for row in rows
        ),
        "minimum_certified_error_to_budget_ratio": min(
            float(row["certified_error_to_budget_ratio"])
            for row in rows
        ),
        "maximum_certified_error_to_budget_ratio": max(
            float(row["certified_error_to_budget_ratio"])
            for row in rows
        ),
        "maximum_certified_to_sampled_envelope_ratio": (
            maximum_inflation
        ),
        "maximum_additional_bisections_if_envelope_fixed": (
            maximum_required_bisections
        ),
        "reflected_envelope_relative_error": reflection_relative_error,
        "decision": (
            "HOLD_GR_HANDOFF__TIGHTEN_CERTIFIED_ENVELOPE_"
            "BEFORE_MORE_TOPOLOGY_GENERATIONS"
        ),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }

    write_csv(ROWS, rows)
    write_csv(VALIDATION, checks)
    atomic_json(RESULT, result)
    if not passed:
        failed = [
            row["check_id"] for row in checks if not row["passed"]
        ]
        raise RuntimeError(f"5259 validation failed: {failed}")
    return result


def main() -> None:
    print(json.dumps(execute(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
