from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SOURCE = POST / "source-intake" / "functional_rg" / "5396"
OUTPUT = POST / "source-intake" / "functional_rg" / "5400"
AUDITED_PATH = "RDRDRDLDRDLDRU"
SCOPE = "S_X003_MC04_SP_DM_LEFT_CONNECTOR_d14_RDRDRDLDRDLDRU"

ANGLE_SCRIPT = POST / "scripts" / "Y5_R2FR_5396_D4_frontier_angle_audit.py"
CENTERED_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_centered_jacobian_crosscheck.py"
)
GALE_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_frontier_gale_nikaido_audit.py"
)
ANGLE_RESULT = SOURCE / f"external41_frontier_angle_{SCOPE}_audit_result.json"
CENTERED_RESULT = SOURCE / f"external01_centered_jacobian_{SCOPE}_result.json"
GALE_RESULT = (
    SOURCE / f"external01_frontier_gale_nikaido_{SCOPE}_result.json"
)
STATUS = SOURCE / "status.json"
STATE = (
    SOURCE
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X003_MC04_SP_DM_LEFT_CONNECTOR_part_00_of_01.state.json"
)
ROWS = STATE.with_suffix(".rows.csv")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError("validation rows cannot be empty")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def validation_row(check: str, passed: bool, evidence: str) -> dict[str, Any]:
    return {"check": check, "passed": passed, "evidence": evidence}


def run_gate() -> dict[str, Any]:
    required_paths = (
        ANGLE_SCRIPT,
        CENTERED_SCRIPT,
        GALE_SCRIPT,
        ANGLE_RESULT,
        CENTERED_RESULT,
        GALE_RESULT,
        STATUS,
        STATE,
        ROWS,
    )
    missing = [str(path) for path in required_paths if not path.exists()]
    if missing:
        raise FileNotFoundError("missing checkpoint input: " + " | ".join(missing))

    angle = read_json(ANGLE_RESULT)
    centered = read_json(CENTERED_RESULT)
    gale = read_json(GALE_RESULT)
    status = read_json(STATUS)
    state = read_json(STATE)
    with ROWS.open("r", encoding="utf-8", newline="") as handle:
        production_rows = list(csv.DictReader(handle))
    audited_rows = [
        row for row in production_rows if row["refinement_path"] == AUDITED_PATH
    ]

    source_contract = all(
        all(
            flag in path.read_text(encoding="utf-8")
            for flag in ("--mapped-cell-id", "--term-id", "--path-segment")
        )
        for path in (ANGLE_SCRIPT, CENTERED_SCRIPT, GALE_SCRIPT)
    )
    angle_schemes = list(angle["schemes"])
    maximum_centered_error = float(
        centered["maximum_centered_to_direct_relative_error"]
    )
    audited_margin = (
        float(audited_rows[0]["minimum_amplitude_denominator_abs_lower"])
        if len(audited_rows) == 1
        else 0.0
    )
    pending_depths = [int(row[4]) for row in state["stack"]]

    validations = [
        validation_row(
            "required_inputs_exist",
            not missing,
            f"{len(required_paths)} source/artifact paths present",
        ),
        validation_row(
            "audit_runners_are_cell_term_path_general",
            source_contract,
            "all three CLIs expose mapped-cell, term, and path-segment arguments",
        ),
        validation_row(
            "centered_derivative_identity_passes",
            bool(centered["all_identities_passed"])
            and int(centered["row_count"]) == 108
            and maximum_centered_error <= 5.0e-12,
            f"108 rows; maximum relative error {maximum_centered_error:.17g}",
        ),
        validation_row(
            "closed_factorized_angle_cover_passes",
            angle["selected_scheme"] is not None
            and all(
                bool(row["all_nonzero_half_plane_passed"])
                for row in angle_schemes
            )
            and min(
                float(row["minimum_imaginary_lower"])
                for row in angle_schemes
            )
            > 0.0,
            "all closed schemes lie in the positive-imaginary half-plane",
        ),
        validation_row(
            "failed_global_univalence_route_not_promoted",
            gale["selected_scheme"] is None
            and gale["global_univalence_proved"] is False,
            "Gale-Nikaido principal-minor cover remains explicitly unproved",
        ),
        validation_row(
            "audited_leaf_committed_by_production",
            len(audited_rows) == 1
            and int(audited_rows[0]["refinement_depth"]) == 14
            and audited_margin > 0.0,
            f"stored margin {audited_margin:.17g}",
        ),
        validation_row(
            "frontier_retreated_below_trigger",
            int(state["accepted_count"]) == 84
            and len(state["stack"]) == 7
            and max(pending_depths, default=-1) == 10
            and AUDITED_PATH not in {str(row[5]) for row in state["stack"]},
            "84 accepted, 7 pending, maximum depth 10",
        ),
        validation_row(
            "production_is_resume_safe",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"])
            and int(status["completed_path_jobs"]) == 15,
            "15/240 paths; paused at runtime budget; resume_safe=true",
        ),
    ]
    failed = [row for row in validations if not bool(row["passed"])]
    provenance = {
        str(path.relative_to(POST)): sha256(path)
        for path in required_paths
    }
    payload = {
        "checkpoint": 5400,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "audited_scope": SCOPE,
        "validation_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_continued_v40_production": not failed,
        "valid_for_global_univalence_claim": False,
        "valid_for_regular_away_W3_claim": False,
        "accepted_box_count": int(state["accepted_count"]),
        "pending_box_count": len(state["stack"]),
        "maximum_pending_depth": max(pending_depths, default=-1),
        "audited_leaf_amplitude_denominator_lower": audited_margin,
        "maximum_centered_derivative_relative_error": maximum_centered_error,
        "minimum_closed_angle_imaginary_lower": min(
            float(row["minimum_imaginary_lower"]) for row in angle_schemes
        ),
        "provenance_sha256": provenance,
    }
    atomic_csv(OUTPUT / "P8_Y5_BRR5396_5400_VALIDATION.csv", validations)
    atomic_json(OUTPUT / "generalized_depth_trigger_audit_gate_result.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    if failed:
        raise RuntimeError(
            "checkpoint 5400 validation failed: "
            + " | ".join(str(row["check"]) for row in failed)
        )
    return payload


if __name__ == "__main__":
    run_gate()
