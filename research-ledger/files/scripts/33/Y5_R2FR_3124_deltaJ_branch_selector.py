from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
CLAUSES = OUT / "P8_Y5_R2FR_3124_NO_CA_SLOT_GRAMMAR_CLAUSES.csv"
CLASSIFIER = OUT / "P8_Y5_R2FR_3123_DELTAJ_PROJECTION_CLASSIFIER_OUTPUT.csv"
OUTPUT = OUT / "P8_Y5_R2FR_3124_DELTAJ_BRANCH_SELECTION_OUTPUT.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3124_VALIDATION.csv"


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


def resolve_source_paths(source_paths: str) -> tuple[bool, list[str], list[str]]:
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
    return not missing, resolved, missing


def proof_closed(clauses: list[dict[str, str]]) -> bool:
    required = [row for row in clauses if is_true(row.get("proof_required", ""))]
    return bool(required) and all(row.get("status") == "signed" for row in required)


def blocking_clauses(clauses: list[dict[str, str]]) -> list[str]:
    return [
        f"{row.get('clause_id')}:{row.get('status')}"
        for row in clauses
        if is_true(row.get("proof_required", "")) and row.get("status") != "signed"
    ]


def classifier_by_class(outputs: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    return {row.get("classification", ""): row for row in outputs}


def row_from_classifier(
    branch_id: str,
    branch: str,
    selected: bool,
    source: dict[str, str] | None,
    reason: str,
    blockers: list[str],
) -> dict[str, Any]:
    source = source or {}
    return {
        "decision_id": branch_id,
        "branch": branch,
        "selected_default": str(selected).lower(),
        "claim_allowed": "false",
        "valid_for_claim": "false",
        "reason": reason,
        "projects_material_coulomb": source.get("projects_material_coulomb", "false"),
        "projects_source_GM_observable": source.get("projects_source_GM_observable", "false"),
        "projects_WEP": source.get("projects_WEP", "false"),
        "projects_R10": source.get("projects_R10", "false"),
        "source_case_id": source.get("case_id", ""),
        "blocking_clauses": ";".join(blockers),
        "next_action": "prove no-cA grammar" if branch == "ZERO_BY_NO_CA_GRAMMAR" else "use this branch for 3125 strict bound interface" if selected else "retain as guard/subbranch",
        "generated_utc": stamp(),
    }


def select_branches(clauses: list[dict[str, str]], classifier_rows: list[dict[str, str]]) -> list[dict[str, Any]]:
    closed = proof_closed(clauses)
    blockers = blocking_clauses(clauses)
    by_class = classifier_by_class(classifier_rows)
    before = by_class.get("FINITE_BEFORE_VARIATION_PROJECTS_BOTH")
    calibration = by_class.get("FINITE_CALIBRATION_ONLY")
    readout = by_class.get("FINITE_READOUT_ONLY_NO_GM")
    effective = by_class.get("FINITE_EFFECTIVE_ACTION_AMBIGUOUS")
    zero = by_class.get("ZERO_BY_ACTION_VARIATION")

    rows = [
        row_from_classifier(
            "SEL3124_0",
            "ZERO_BY_NO_CA_GRAMMAR",
            closed,
            zero,
            "No-cA grammar would kill delta_J if every proof-required clause is signed.",
            blockers,
        ),
        row_from_classifier(
            "SEL3124_1",
            "FINITE_BEFORE_VARIATION_PROJECTS_BOTH",
            not closed,
            before,
            "Selected default live branch because no-cA grammar is not signed and this is the strictest unexcluded source-coupling countermodel.",
            blockers,
        ),
        row_from_classifier(
            "SEL3124_2",
            "FINITE_CALIBRATION_ONLY",
            False,
            calibration,
            "Retained as guard for universal common current-unit shifts; not selected for source-coupling bounds.",
            blockers,
        ),
        row_from_classifier(
            "SEL3124_3",
            "FINITE_READOUT_ONLY_NO_GM",
            False,
            readout,
            "Retained as guard for post-variation observed-charge/readout effects; does not source Hilbert GM.",
            blockers,
        ),
        row_from_classifier(
            "SEL3124_4",
            "FINITE_EFFECTIVE_ACTION_AMBIGUOUS",
            False,
            effective,
            "Retained but must be split into before-variation versus readout-only before scoring.",
            blockers,
        ),
    ]
    return rows


def validate(clauses: list[dict[str, str]], selections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    required = [
        "clause_id",
        "clause",
        "required_statement",
        "status",
        "proof_required",
        "source_paths",
        "valid_for_claim",
    ]
    columns = set(clauses[0].keys()) if clauses else set()
    missing_columns = [column for column in required if column not in columns]
    source_status: dict[str, bool] = {}
    source_details: dict[str, Any] = {}
    for row in clauses:
        ok, resolved, missing = resolve_source_paths(row.get("source_paths", ""))
        source_status[row.get("clause_id", "")] = ok
        source_details[row.get("clause_id", "")] = {"resolved": resolved, "missing": missing}

    selected = [row for row in selections if row.get("selected_default") == "true"]
    validations: list[dict[str, Any]] = [
        {
            "check_id": "VAL3124_0_clause_schema",
            "status": "pass" if clauses and not missing_columns else "fail",
            "details": ";".join(missing_columns),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3124_1_clause_sources_resolve",
            "status": "pass" if clauses and all(source_status.values()) else "fail",
            "details": json.dumps(source_details, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3124_2_no_cA_not_promoted",
            "status": "pass" if not proof_closed(clauses) else "fail",
            "details": ";".join(blocking_clauses(clauses)),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3124_3_exactly_one_default_branch",
            "status": "pass" if len(selected) == 1 else "fail",
            "details": json.dumps(selected, sort_keys=True),
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3124_4_selected_before_variation_when_unsigned",
            "status": "pass" if selected and selected[0].get("branch") == "FINITE_BEFORE_VARIATION_PROJECTS_BOTH" else "fail",
            "details": selected[0].get("branch", "") if selected else "",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
        {
            "check_id": "VAL3124_5_all_outputs_nonclaim",
            "status": "pass" if selections and all(row.get("claim_allowed") == "false" and row.get("valid_for_claim") == "false" for row in selections) else "fail",
            "details": f"selection_rows={len(selections)}",
            "valid_for_claim": "false",
            "generated_utc": stamp(),
        },
    ]
    return validations


def main() -> None:
    clauses = read_csv(CLAUSES)
    classifier_rows = read_csv(CLASSIFIER)
    selections = select_branches(clauses, classifier_rows)
    write_csv(OUTPUT, selections)
    write_csv(VALIDATION, validate(clauses, selections))
    print(
        json.dumps(
            {
                "clause_rows": len(clauses),
                "selection_rows": len(selections),
                "output": str(OUTPUT),
                "validation": str(VALIDATION),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
