from __future__ import annotations

import csv
import hashlib
import json
import os
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
RUN = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5111"
    / "runs"
    / "E020_primary_complex_control_extension_v1"
)
PROJECTIVE_GATE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5119"
    / "S507622_E020_projective_cluster_argument_independence.json"
)
ANALYSIS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5120"
    / "locked_beta_one_complex_control_analysis.json"
)
MECHANISM = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5121"
    / "locked_beta_one_failure_mechanism.json"
)
VALIDATIONS = {
    "5119": POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5119_VALIDATION.csv",
    "5120": POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5120_VALIDATION.csv",
    "5121": POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5121_VALIDATION.csv",
}
SOURCE = POST / "source-intake" / "functional_rg" / "5122"
RESULT_JSON = SOURCE / "control_matrix_and_analysis_reconciliation.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5122_VALIDATION.csv"
)
MARKER = "MTS_5122_CONTROL_MATRIX_AND_ANALYSIS_RECONCILIATION"
REVISION = "complete-matrix-locked-analysis-handoff-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)


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


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")
    os.replace(temporary, path)


def validation_passes(path: Path) -> bool:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    return bool(rows) and all(str(row["passed"]).lower() == "true" for row in rows)


def main() -> None:
    required = [RUN / "COMPLETED.json", PROJECTIVE_GATE, ANALYSIS, MECHANISM, FORMAL]
    required.extend(VALIDATIONS.values())
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing 5122 inputs: {missing}")
    completion = read_json(RUN / "COMPLETED.json")
    projective = read_json(PROJECTIVE_GATE)
    analysis = read_json(ANALYSIS)
    mechanism = read_json(MECHANISM)
    formal_hash = tree_digest(FORMAL)
    cache_directories = list((POST / "scripts").glob("__pycache__"))
    checks = [
        ("control_matrix_complete", completion["completed_converged"] == 180 and completion["failed"] == 0 and completion["missing"] == 0, json.dumps({key: completion[key] for key in ("completed_converged", "failed", "missing")})),
        ("projective_E020_gate_passed", projective["argument_independent_projective_cluster_zero_passed"] and len(projective["authorized_job_scopes"]) == 15, str(len(projective["authorized_job_scopes"]))),
        ("5119_validation_passed", validation_passes(VALIDATIONS["5119"]), str(VALIDATIONS["5119"])),
        ("5120_validation_passed", validation_passes(VALIDATIONS["5120"]), str(VALIDATIONS["5120"])),
        ("5121_validation_passed", validation_passes(VALIDATIONS["5121"]), str(VALIDATIONS["5121"])),
        ("locked_analysis_complete", analysis["high_units"] == 4 and analysis["low_units"] == 12 and analysis["fixed_beta_real"] == 1.0, analysis["decision"]),
        ("locked_decision_recorded", analysis["decision"] == "LOCKED_BETA_ONE_COMPLEX_CONTROL_DOES_NOT_PASS", str(analysis["realized_cost_normalized_score_ratio"])),
        ("failure_mechanism_closed", mechanism["decision"] == "LOCKED_BETA_ONE_CONTROL_VARIANCE_ROUTE_REJECTED_UNDER_ORIGINAL_BUDGET", mechanism["failure_mechanism"]),
        ("no_python_cache", not cache_directories, json.dumps([str(path) for path in cache_directories])),
        ("formalization_unchanged", formal_hash == FORMAL_BASELINE, formal_hash),
        ("claim_discipline", not analysis["valid_for_full_MTS_claim"] and not mechanism["valid_for_full_MTS_claim"], "numerical estimator decision only"),
    ]
    passed = all(row[1] for row in checks)
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "control_completion": str((RUN / "COMPLETED.json").resolve()),
        "control_completion_sha256": digest(RUN / "COMPLETED.json"),
        "control_matrix_converged": 180,
        "control_matrix_failed": 0,
        "analysis": str(ANALYSIS.resolve()),
        "analysis_sha256": digest(ANALYSIS),
        "locked_score": float(analysis["realized_cost_normalized_score_ratio"]),
        "locked_threshold": float(analysis["predeclared_efficiency_threshold"]),
        "accepted_runtime_hours": float(analysis["accepted_final_job_runtime_hours"]),
        "runtime_cap_hours": float(analysis["runtime_cap_hours"]),
        "locked_decision": analysis["decision"],
        "failure_mechanism": mechanism["failure_mechanism"],
        "mechanism_decision": mechanism["decision"],
        "next_route": mechanism["next_route"],
        "analysis_complete": passed,
        "independent_efficiency_claim_allowed": False,
        "full_MTS_claim_allowed": False,
        "formalization_workbench_tree_sha256": formal_hash,
        "passed": passed,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT_JSON, result)
    VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for name, check_passed, detail in checks:
            writer.writerow((name, str(bool(check_passed)).lower(), detail))
    print(json.dumps(result, indent=2))
    if not passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
