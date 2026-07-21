from __future__ import annotations

import csv
import importlib.util
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPT_5044 = POST / "scripts" / "Y5_R2FR_5044_symmetric_hybrid_fidelity_gate.py"
SCRIPT_5049 = POST / "scripts" / "Y5_R2FR_5049_restricted_coarse_E040_multilevel_reaudit.py"
SOURCE_5049 = POST / "source-intake" / "functional_rg" / "5049"
SOURCE = POST / "source-intake" / "functional_rg" / "5050"
RESULT_JSON = SOURCE / "restricted_symmetric_hybrid_fidelity_gate.json"
FAMILY_CSV = SOURCE / "restricted_symmetric_threshold_family.csv"
COMPONENT_CSV = SOURCE / "restricted_selected_component_gate.csv"
LOCK_JSON = SOURCE / "restricted_locked_reserve_multilevel_pilot.json"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5050_VALIDATION.csv"
)
MARKER = "MTS_5050_RESTRICTED_SYMMETRIC_HYBRID_FIDELITY_REAUDIT"
REVISION = "restricted-symmetric-hybrid-reaudit-v1"
PROFILE = "coarse12"
EXECUTION_CAP_HOURS = 10.0
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5049 = load_module("mts_5049_for_restricted_hybrid", SCRIPT_5049)
M5044 = load_module("mts_5044_for_restricted_hybrid", SCRIPT_5044)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True), encoding="utf-8")


def validation_rows(result: dict[str, Any], scope: dict[str, Any]) -> list[dict[str, str]]:
    status_path = SOURCE_5049 / "runs" / PROFILE / "status.json"
    status = json.loads(status_path.read_text(encoding="utf-8"))
    projected_hours = float(result["projected_minimum_pilot_hours"])
    selected = result["selected"]
    checks = [
        ("source_5049_exists", SCRIPT_5049.exists(), str(SCRIPT_5049)),
        (
            "restricted_source_matrix_complete",
            bool(status.get("complete"))
            and status.get("terminal_jobs") == status.get("expected_jobs") == 120,
            f"terminal={status.get('terminal_jobs')}; expected={status.get('expected_jobs')}",
        ),
        (
            "restricted_source_matrix_clean",
            status.get("failed_jobs") == 0 and status.get("unconverged_jobs") == 0,
            f"failed={status.get('failed_jobs')}; unconverged={status.get('unconverged_jobs')}",
        ),
        (
            "all_theorem_zeros_restricted",
            bool(scope.get("all_theorem_zeros_within_restricted_scope")),
            f"strict={scope.get('strict_scope_rows')}; total={scope.get('theorem_zero_rows')}",
        ),
        (
            "selected_design_reflection_symmetric",
            set(selected["upgraded_arguments"])
            == M5044.selected_arguments(int(selected["upgraded_group_count"])),
            str(selected["upgraded_arguments"]),
        ),
        (
            "target_values_not_fit",
            not result["target_values_used_to_fit_betas"],
            "required false",
        ),
        (
            "fresh_evidence_not_claimed",
            not result["valid_for_full_MTS_claim"],
            "required false",
        ),
        (
            "execution_cap_respected",
            result["pilot_execution_authorized"]
            == (
                result["statistical_design_locked_for_fresh_pilot"]
                and projected_hours <= EXECUTION_CAP_HOURS
            ),
            f"projected_hours={projected_hours}; cap={EXECUTION_CAP_HOURS}",
        ),
        (
            "formalization_workbench_unchanged",
            result["formalization_workbench_tree_sha256"] == FORMAL_BASELINE,
            result["formalization_workbench_tree_sha256"],
        ),
    ]
    return [
        {"check": name, "passed": str(bool(passed)).lower(), "evidence": evidence}
        for name, passed, evidence in checks
    ]


def main() -> None:
    required = [
        SCRIPT_5044,
        SCRIPT_5049,
        SOURCE_5049 / "restricted_multilevel_coarse_E040_gate.json",
        SOURCE_5049 / "runs" / PROFILE / "status.json",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(f"missing restricted-source inputs: {missing}")
    M5049.configure_modules()
    try:
        scope = M5049.strict_scope_audit(PROFILE)
        if not scope["all_theorem_zeros_within_restricted_scope"]:
            raise RuntimeError("restricted theorem-scope audit failed")
        M5044.SCRIPT_5043 = SCRIPT_5049
        M5044.SOURCE = SOURCE
        M5044.RESULT_JSON = RESULT_JSON
        M5044.FAMILY_CSV = FAMILY_CSV
        M5044.COMPONENT_CSV = COMPONENT_CSV
        M5044.LOCK_JSON = LOCK_JSON
        M5044.VALIDATION_CSV = VALIDATION_CSV
        M5044.MARKER = MARKER
        M5044.M5043 = M5049.M5043
        M5044.main()
        result = json.loads(RESULT_JSON.read_text(encoding="utf-8"))
        projected_hours = float(result["projected_minimum_pilot_hours"])
        statistically_locked = bool(result["statistical_design_locked_for_fresh_pilot"])
        execution_authorized = statistically_locked and projected_hours <= EXECUTION_CAP_HOURS
        result.update(
            {
                "checkpoint_marker": MARKER,
                "revision": REVISION,
                "supersedes_checkpoint": 5044,
                "source_script": str(SCRIPT_5049),
                "source_script_sha256": M5049.digest(SCRIPT_5049),
                "source_result": str(
                    SOURCE_5049 / "restricted_multilevel_coarse_E040_gate.json"
                ),
                "source_result_sha256": M5049.digest(
                    SOURCE_5049 / "restricted_multilevel_coarse_E040_gate.json"
                ),
                "source_status_sha256": M5049.digest(
                    SOURCE_5049 / "runs" / PROFILE / "status.json"
                ),
                "restricted_scope_audit": scope,
                "restricted_scope_source": str(M5049.M5046.SCRIPT_5045_SCOPE),
                "restricted_scope_source_sha256": M5049.digest(
                    M5049.M5046.SCRIPT_5045_SCOPE
                ),
                "execution_cap_hours": EXECUTION_CAP_HOURS,
                "pilot_execution_authorized": execution_authorized,
                "decision": (
                    "LOCK_AS_RESERVE_BUT_DO_NOT_RUN"
                    if statistically_locked and not execution_authorized
                    else (
                        "FRESH_PILOT_AUTHORIZED_WITHIN_CAP"
                        if execution_authorized
                        else "REJECT_OR_REVISE_HYBRID_ROUTE"
                    )
                ),
                "valid_for_full_MTS_claim": False,
            }
        )
        result.pop("four_hour_execution_cap", None)
        atomic_json(RESULT_JSON, result)
        lock = json.loads(LOCK_JSON.read_text(encoding="utf-8"))
        lock.update(
            {
                "checkpoint_marker": MARKER,
                "revision": REVISION,
                "source_checkpoint": 5049,
                "execution_cap_hours": EXECUTION_CAP_HOURS,
                "execution_authorized": execution_authorized,
                "execution_blocker": (
                    f"projected minimum {projected_hours:.3f} h exceeds the "
                    f"{EXECUTION_CAP_HOURS:g} h cap"
                    if statistically_locked and not execution_authorized
                    else None
                ),
                "future_samples_independent_of_training_data_through_checkpoint": 5050,
                "valid_for_full_MTS_claim": False,
            }
        )
        lock.pop("future_samples_independent_of_5034_through_5044_training_data", None)
        atomic_json(LOCK_JSON, lock)
        checks = validation_rows(result, scope)
        VALIDATION_CSV.parent.mkdir(parents=True, exist_ok=True)
        with VALIDATION_CSV.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=("check", "passed", "evidence"))
            writer.writeheader()
            writer.writerows(checks)
        print(
            json.dumps(
                {
                    "selected_upgraded_arguments": result["selected"][
                        "upgraded_arguments"
                    ],
                    "equal_cost_score_ratio": result["selected"][
                        "equal_cost_score_ratio"
                    ],
                    "worst_crossfit_sd_ratio": result["selected"][
                        "worst_crossfit_sd_ratio"
                    ],
                    "components_improved_crossfit": result["selected"][
                        "components_improved_crossfit"
                    ],
                    "projected_minimum_pilot_hours": projected_hours,
                    "statistical_design_locked": statistically_locked,
                    "execution_authorized": execution_authorized,
                    "restricted_scope_passed": scope[
                        "all_theorem_zeros_within_restricted_scope"
                    ],
                    "validation_passed": sum(row["passed"] == "true" for row in checks),
                    "validation_total": len(checks),
                },
                indent=2,
            )
        )
    finally:
        M5049.restore_modules()


if __name__ == "__main__":
    main()
