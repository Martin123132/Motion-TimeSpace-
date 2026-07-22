from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT / "research-programme" / "protocols" / "1192"
RUNNER = (
    ROOT
    / "research-programme"
    / "scripts"
    / "Y5_R2FR_5176_predeclared_paired_high_mode_seed_ensemble.py"
)
VALIDATION = (
    ROOT
    / "research-programme"
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5176_VALIDATION.csv"
)


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def record(
    checks: list[dict[str, Any]], check_id: str, passed: bool, evidence: Any
) -> None:
    checks.append(
        {"check_id": check_id, "passed": bool(passed), "evidence": evidence}
    )


def main() -> None:
    checks: list[dict[str, Any]] = []
    freeze = json.loads((PROTOCOL / "runner_freeze.json").read_text(encoding="utf-8"))
    hash_targets = {
        "runner_script": (RUNNER, freeze["runner_script_sha256"]),
        "protocol_file": (
            PROTOCOL / "ensemble_protocol.json",
            freeze["protocol_file_sha256"],
        ),
        "schedule_file": (
            PROTOCOL / "predeclared_seed_schedule.csv",
            freeze["schedule_file_sha256"],
        ),
        "source_provenance": (
            PROTOCOL / "source_provenance.csv",
            freeze["source_provenance_sha256"],
        ),
        "first_seed_result": (
            PROTOCOL / "seeds" / "seed_01_3240854344" / "seed_result.json",
            freeze["first_seed_result_sha256"],
        ),
    }
    for check_id, (path, expected) in hash_targets.items():
        actual = file_digest(path) if path.is_file() else None
        record(checks, f"{check_id}_sha256", actual == expected, actual)

    schedule = read_csv(PROTOCOL / "predeclared_seed_schedule.csv")
    seeds = [int(row["high_mode_seed"]) for row in schedule]
    record(
        checks,
        "schedule_has_12_unique_confirmatory_seeds",
        len(seeds) == 12
        and len(set(seeds)) == 12
        and all(row["analysis_role"] == "confirmatory" for row in schedule),
        seeds,
    )
    record(
        checks,
        "pilot_excluded",
        int(freeze["pilot_seed_excluded"]) not in seeds,
        freeze["pilot_seed_excluded"],
    )
    record(
        checks,
        "schedule_rows_nonclaim",
        all(row["valid_for_claim"].lower() == "false" for row in schedule),
        len(schedule),
    )

    result = json.loads(
        (PROTOCOL / "paired_ensemble_results.json").read_text(encoding="utf-8")
    )
    record(
        checks,
        "ensemble_is_incomplete_nonclaim",
        result["completed_confirmatory_seeds"] == 1
        and result["final_confirmatory_seed_count"] == 12
        and result["valid_for_claim"] is False
        and result["verdict"]
        == "INCOMPLETE_PREDECLARED_ENSEMBLE_NO_PREFERENCE_ALLOWED",
        result["verdict"],
    )

    validation_rows = read_csv(VALIDATION)
    record(
        checks,
        "checkpoint_validation",
        len(validation_rows) == 12
        and all(row["passed"].lower() == "true" for row in validation_rows),
        f"{sum(row['passed'].lower() == 'true' for row in validation_rows)}/{len(validation_rows)}",
    )

    failures = [row for row in checks if not row["passed"]]
    report = {
        "checkpoint": 1192,
        "private_checkpoint": 5176,
        "passed": not failures,
        "checks": checks,
    }
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
