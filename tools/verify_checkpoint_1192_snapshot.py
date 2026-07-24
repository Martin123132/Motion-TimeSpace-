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
SEED_ARTIFACTS = (
    "COMPLETE.marker",
    "forward_scores.csv",
    "phase_diagnostics.csv",
    "seed_result.json",
    "status.json",
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
        "ensemble_is_complete_nonclaim_metric_split",
        result["completed_confirmatory_seeds"] == 12
        and result["final_confirmatory_seed_count"] == 12
        and result["valid_for_claim"] is False
        and result["verdict"]
        == "STATISTICAL_DRAW_OR_METRIC_SPLIT_WITHIN_THIS_LOCKED_FORMATION_GATE",
        result["verdict"],
    )
    q_statistics = result["q_statistics"]
    rmse_statistics = result["RMSE_statistics"]
    record(
        checks,
        "q_metric_has_MTS_directed_nonzero_component",
        q_statistics["mean"] < 0.0
        and q_statistics["bootstrap_95_upper"] < 0.0
        and q_statistics["exact_two_sided_sign_flip_p"] <= 0.05,
        q_statistics,
    )
    record(
        checks,
        "RMSE_metric_does_not_select_either_model",
        rmse_statistics["bootstrap_95_lower"] < 0.0
        < rmse_statistics["bootstrap_95_upper"]
        and rmse_statistics["exact_two_sided_sign_flip_p"] > 0.05,
        rmse_statistics,
    )
    record(
        checks,
        "joint_outcome_remains_nonpreference",
        result["MTS_joint_wins"] == 3
        and result["CDM_joint_wins"] == 0
        and result["joint_ties_or_splits"] == 9
        and result["joint_exact_two_sided_sign_p"] > 0.05,
        {
            "MTS": result["MTS_joint_wins"],
            "CDM": result["CDM_joint_wins"],
            "tie_or_split": result["joint_ties_or_splits"],
            "p": result["joint_exact_two_sided_sign_p"],
        },
    )

    execution_rows = read_csv(PROTOCOL / "seed_execution_status.csv")
    record(
        checks,
        "all_12_seed_status_rows_are_complete_nonclaim",
        len(execution_rows) == 12
        and all(
            row["state"] == "COMPLETE"
            and row["complete_marker_exists"].lower() == "true"
            and row["valid_for_claim"].lower() == "false"
            for row in execution_rows
        ),
        len(execution_rows),
    )
    score_rows = read_csv(PROTOCOL / "paired_seed_scores.csv")
    confirmatory_rows = [
        row
        for row in score_rows
        if row["included_in_confirmatory_statistics"].lower() == "true"
    ]
    record(
        checks,
        "paired_score_table_contains_pilot_plus_12_confirmatory_rows",
        len(score_rows) == 13
        and len(confirmatory_rows) == 12
        and all(row["valid_for_claim"].lower() == "false" for row in score_rows),
        {"all": len(score_rows), "confirmatory": len(confirmatory_rows)},
    )

    compact_seed_failures: list[str] = []
    for row in execution_rows:
        seed_directory = (
            PROTOCOL
            / "seeds"
            / f"seed_{int(row['seed_index']):02d}_{row['high_mode_seed']}"
        )
        for name in SEED_ARTIFACTS:
            path = seed_directory / name
            if not path.is_file():
                compact_seed_failures.append(str(path))
        result_path = seed_directory / "seed_result.json"
        if result_path.is_file():
            seed_result = json.loads(result_path.read_text(encoding="utf-8"))
            if seed_result.get("valid_for_claim") is not False:
                compact_seed_failures.append(f"{result_path}:claim")
    record(
        checks,
        "all_12_compact_seed_snapshots_are_present_nonclaim",
        not compact_seed_failures,
        compact_seed_failures,
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
        "snapshot_state": "FINAL_12_OF_12_NONCLAIM",
        "passed": not failures,
        "checks": checks,
    }
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
