from __future__ import annotations

import csv
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
ANALYSIS_JSON = POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_analysis_v12.json"
CHANNEL_CSV = POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_channels_v12.csv"
JACKKNIFE_CSV = POST / "source-intake" / "functional_rg" / "5080" / "fresh_pilot_jackknife_v12.csv"
EXECUTION_JSON = POST / "source-intake" / "functional_rg" / "5107" / "predeclared_5080_v12_margin_adapter_execution.json"
SOURCE = POST / "source-intake" / "functional_rg" / "5108"
RESULT_JSON = SOURCE / "locked_pilot_failure_mechanism.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5108_VALIDATION.csv"
MARKER = "MTS_5108_LOCKED_PILOT_FAILURE_MECHANISM"
REVISION = "inactive-bottleneck-cost-floor-diagnosis-v1"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def main() -> None:
    required = [ANALYSIS_JSON, CHANNEL_CSV, JACKKNIFE_CSV, EXECUTION_JSON, FORMAL]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    analysis = read_json(ANALYSIS_JSON)
    execution = read_json(EXECUTION_JSON)
    channels = read_csv(CHANNEL_CSV)
    jackknife = read_csv(JACKKNIFE_CSV)
    for row in channels:
        row["active_control"] = row["active_control"].lower() == "true"
        for field in (
            "target_margin",
            "high_only_standard_error",
            "standard_error",
            "same_high_sample_se_ratio",
            "standard_error_over_margin",
            "realized_cost_normalized_component_score_ratio",
        ):
            row[field] = float(row[field])
        row["high_only_standard_error_over_margin"] = (
            row["high_only_standard_error"] / row["target_margin"]
        )
    bottleneck = max(
        channels,
        key=lambda row: row["high_only_standard_error_over_margin"],
    )
    high_units = int(analysis["high_units"])
    low_units = int(analysis["low_units"])
    low_to_high_ratio = low_units / high_units
    high_cost = float(analysis["mean_high_only_runtime_seconds"])
    correction_cost = float(analysis["mean_locked_correction_runtime_seconds"])
    low_cost = float(analysis["mean_low_only_runtime_seconds"])
    inactive_bottleneck_cost_floor = math.sqrt(
        (correction_cost + low_to_high_ratio * low_cost) / high_cost
    )
    threshold = float(analysis["predeclared_efficiency_threshold"])
    observed_score = float(analysis["realized_cost_normalized_score_ratio"])
    active_failures = [
        row["channel"]
        for row in channels
        if row["active_control"]
        and row["realized_cost_normalized_component_score_ratio"] >= threshold
    ]
    inactive_failures = [
        row["channel"]
        for row in channels
        if not row["active_control"]
        and row["realized_cost_normalized_component_score_ratio"] >= threshold
    ]
    maximum_delete_one_shift = max(
        float(row["maximum_shift_in_full_standard_errors"]) for row in jackknife
    )
    formal_digest = tree_digest(FORMAL)
    guards = {
        "execution_was_valid": bool(execution.get("execution_valid")),
        "locked_decision_is_failure": analysis.get("decision")
        == "LOCKED_FRESH_PILOT_DOES_NOT_PASS"
        and not bool(analysis.get("locked_numerical_efficiency_gate_passed")),
        "matrix_requirement_passed": bool(analysis.get("pilot_matrix_complete")),
        "runtime_requirement_passed": float(
            analysis["direct_recorded_job_runtime_hours"]
        )
        <= 10.0,
        "efficiency_requirement_failed": observed_score >= threshold,
        "high_only_bottleneck_is_inactive": not bool(bottleneck["active_control"]),
        "bottleneck_is_imaginary_minus_0p3": bottleneck["channel"]
        == "imag_z-0.3",
        "observed_score_equals_inactive_cost_floor": math.isclose(
            observed_score,
            inactive_bottleneck_cost_floor,
            rel_tol=1.0e-12,
            abs_tol=1.0e-12,
        ),
        "inactive_cost_floor_exceeds_threshold": inactive_bottleneck_cost_floor
        >= threshold,
        "target_central_values_not_used": not bool(
            analysis.get("target_central_values_used")
        ),
        "formalization_unchanged": formal_digest == FORMAL_BASELINE,
    }
    diagnosis_valid = all(guards.values())
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "analysis_result": str(ANALYSIS_JSON),
        "analysis_result_sha256": digest(ANALYSIS_JSON),
        "locked_decision": analysis["decision"],
        "predeclared_threshold": threshold,
        "observed_score_ratio": observed_score,
        "recorded_runtime_hours": analysis["direct_recorded_job_runtime_hours"],
        "runtime_cap_hours": 10.0,
        "bottleneck_channel": bottleneck["channel"],
        "bottleneck_control_active": bottleneck["active_control"],
        "bottleneck_high_only_standard_error_over_margin": bottleneck[
            "high_only_standard_error_over_margin"
        ],
        "inactive_bottleneck_cost_floor": inactive_bottleneck_cost_floor,
        "cost_floor_identity": "sqrt((C_correction+(N_low/N_high) C_low)/C_high)",
        "active_channels_at_or_above_threshold": active_failures,
        "inactive_channels_at_or_above_threshold": inactive_failures,
        "maximum_delete_one_shift_in_full_standard_errors": maximum_delete_one_shift,
        "failure_mechanism": (
            "The high-only precision bottleneck is imag_z-0.3, where the locked "
            "control is beta=0. Its variance is unchanged while the shared low-bank "
            "cost is positive, forcing the primary score to the observed cost floor."
        ),
        "decision_scope": "reject this locked multifidelity estimator, not the MTS kernel or theory",
        "next_derivation": (
            "prove or reject a conjugation/reflection-symmetric imaginary control "
            "for the bottleneck before authorizing more kernels; if no exact control "
            "exists, retain high-only sampling and reject the low-only bank route"
        ),
        "guards": guards,
        "diagnosis_valid": diagnosis_valid,
        "formalization_workbench_tree_sha256": formal_digest,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    checks = [
        ("sources_exist", not missing, "all 5108 sources exist"),
        *[(name, passed, str(passed)) for name, passed in guards.items()],
        ("diagnosis_valid", diagnosis_valid, result["failure_mechanism"]),
        ("claim_discipline", not result["valid_for_full_MTS_claim"], result["decision_scope"]),
    ]
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=("check_id", "passed", "detail", "checkpoint_marker"),
        )
        writer.writeheader()
        for index, (name, passed, detail) in enumerate(checks, start=1):
            writer.writerow(
                {
                    "check_id": f"V5108_{index:02d}_{name}",
                    "passed": passed,
                    "detail": detail,
                    "checkpoint_marker": MARKER,
                }
            )
    failed = [name for name, passed, _ in checks if not passed]
    if failed:
        raise RuntimeError(f"checkpoint 5108 validation failed: {failed}")


if __name__ == "__main__":
    main()
