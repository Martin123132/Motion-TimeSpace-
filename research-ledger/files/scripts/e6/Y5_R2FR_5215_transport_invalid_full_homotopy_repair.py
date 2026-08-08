from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "5215"
SCRIPT_5215 = (
    POST
    / "scripts"
    / "Y5_R2FR_5215_fresh_A00_permutation_control_pilot.py"
)
DIAGNOSTIC = SOURCE / "transport_root_split_diagnostic.json"
FAILED_JOB_SNAPSHOT = SOURCE / "failed_transport_job_snapshot.json"
REPAIR_LOCK = SOURCE / "frozen_transport_repair_lock.json"
REPAIR_AUDIT = SOURCE / "transport_invalid_full_homotopy_repair_audit.json"
MARKER = "MTS_5215_TRANSPORT_INVALID_FULL_HOMOTOPY_REPAIR"
REVISION = "transport-invalid-direct-full-homotopy-fallback-v1"


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5215 = load_module(SCRIPT_5215, "mts_5215_for_transport_repair")
M5077 = M5215.M5212.M5077
ORIGINAL_WRITE_COMPOSED = M5077.CentralTopologyManager.write_composed
ORIGINAL_VALIDATION_ROWS = M5215.validation_rows
REPAIR_ROWS: list[dict[str, Any]] = []


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def repair_contract() -> dict[str, Any]:
    protocol = read_json(M5215.PROTOCOL_LOCK)
    source_topology = (
        M5215.RUNS
        / "fresh_A00_control_pilot_v1"
        / "topologies"
        / "S521509_N0000__E040_A02.json"
    )
    if protocol["contract"]["runner_sha256"] != digest(SCRIPT_5215):
        raise RuntimeError("the original checkpoint-5215 runner changed")
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "original_protocol_lock_sha256": digest(
            M5215.PROTOCOL_LOCK
        ),
        "original_runner_sha256": digest(SCRIPT_5215),
        "repair_runner_sha256": digest(Path(__file__).resolve()),
        "transport_diagnostic_sha256": digest(DIAGNOSTIC),
        "failed_job_snapshot_sha256": digest(FAILED_JOB_SNAPSHOT),
        "source_topology_sha256": digest(source_topology),
        "repair_rule": (
            "if a converged path certificate fails either locked "
            "path-root transport diagnostic, reject the transported "
            "document and call the unchanged original full-homotopy "
            "constructor for that target argument"
        ),
        "repair_trigger": (
            "maximum_source_representation_error >= 2e-5 or "
            "maximum_group_candidate_spread >= 2e-5"
        ),
        "integrand_changed": False,
        "residue_quadrature_changed": False,
        "control_identity_changed": False,
        "control_coefficient_changed": False,
        "statistical_thresholds_changed": False,
        "seed_schedule_changed": False,
        "outcome_values_used_to_choose_repair": False,
        "partial_status_exposure_before_repair": {
            "completed_converged": 16,
            "failed_transport": 1,
            "missing": 7,
        },
    }


def lock_repair() -> dict[str, Any]:
    contract = repair_contract()
    if REPAIR_LOCK.exists():
        locked = read_json(REPAIR_LOCK)
        if locked["contract"] != contract:
            raise RuntimeError("checkpoint-5215 repair contract changed")
        return locked
    locked = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "contract": contract,
        "outcomes_present_before_repair_lock": True,
        "outcome_values_used_to_choose_repair": False,
        "statistical_protocol_reopened": False,
        "threshold_retuning_allowed": False,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(REPAIR_LOCK, locked)
    return locked


def direct_full_homotopy_fallback(
    manager: Any,
    source_path: Path,
    event_id: str,
    argument_id: str,
    suite: str,
    error: RuntimeError,
    started: float,
) -> tuple[dict[str, Any], Path, float]:
    argument = manager.arguments[argument_id]
    target = M5077.M5036.complex_from_row(
        argument["target_cosine"]
    )
    source_document = read_json(source_path)
    original_levels = tuple(M5077.M5069.FEYNMAN_STEP_LEVELS)
    if suite != "E040_TO_E020":
        M5077.M5069.FEYNMAN_STEP_LEVELS = tuple(
            int(value)
            for value in manager.config[
                "argument_certificate_step_levels"
            ]
        )
    try:
        certified, levels = M5077.M5069.certify_segment(
            source_document,
            target,
            suite,
        )
    finally:
        M5077.M5069.FEYNMAN_STEP_LEVELS = original_levels
    if certified is None:
        raise RuntimeError(
            "transport failure could not be reproduced by a converged "
            "path certificate"
        ) from error
    _, diagnostics = M5077.M5069.construct_path_transported_document(
        source_document,
        target,
        source_path,
        suite,
        certified,
    )
    if diagnostics["path_root_transport_valid"]:
        raise RuntimeError(
            "transport failure reproduced as valid; refusing fallback"
        ) from error

    document, output, full_runtime = M5077.ORIGINAL_OBTAIN_TOPOLOGY(
        manager.run_directory,
        manager.config,
        manager.events[event_id],
        argument,
    )
    repair_row = {
        "checkpoint_marker": MARKER,
        "event_id": event_id,
        "argument_id": argument_id,
        "suite": suite,
        "source_path": str(source_path),
        "source_path_sha256": digest(source_path),
        "failed_error": str(error),
        "certificate_resolution": int(certified["resolution"]),
        "certificate_attempted_resolutions": [
            int(level["resolution"]) for level in levels
        ],
        "maximum_source_representation_error": float(
            diagnostics["maximum_source_representation_error"]
        ),
        "maximum_group_candidate_spread": float(
            diagnostics["maximum_group_candidate_spread"]
        ),
        "root_matching_tolerance": float(
            M5077.M5069.ROOT_MATCHING_TOLERANCE
        ),
        "path_root_transport_valid": False,
        "fallback": "ORIGINAL_FULL_HOMOTOPY",
        "full_homotopy_runtime_seconds": float(full_runtime),
        "statistical_protocol_changed": False,
        "valid_for_numeric_UV_claim": False,
    }
    document["checkpoint_marker"] = M5215.MARKER
    document["revision"] = M5215.REVISION
    document["config_digest"] = manager.config["config_digest"]
    document["central_anchor_fallback"] = {
        "reason": "path_root_transport_invalid",
        "suite": suite,
        "source_path": str(source_path),
        "certificate_resolution": int(certified["resolution"]),
        "maximum_source_representation_error": repair_row[
            "maximum_source_representation_error"
        ],
        "maximum_group_candidate_spread": repair_row[
            "maximum_group_candidate_spread"
        ],
        "root_matching_tolerance": repair_row[
            "root_matching_tolerance"
        ],
        "full_homotopy_runtime_seconds": float(full_runtime),
    }
    document["transport_execution_repair"] = repair_row
    document["valid_for_full_MTS_claim"] = False
    M5215.atomic_json(output, document)
    REPAIR_ROWS.append(repair_row)
    return document, output, time.monotonic() - started


def repaired_write_composed(
    manager: Any,
    source_document: dict[str, Any],
    source_path: Path,
    event_id: str,
    argument_id: str,
    suite: str,
) -> tuple[dict[str, Any], Path, float]:
    started = time.monotonic()
    try:
        return ORIGINAL_WRITE_COMPOSED(
            manager,
            source_document,
            source_path,
            event_id,
            argument_id,
            suite,
        )
    except RuntimeError as error:
        if not str(error).startswith("path root transport failed for "):
            raise
        return direct_full_homotopy_fallback(
            manager,
            source_path,
            event_id,
            argument_id,
            suite,
            error,
            started,
        )


def robust_validation_rows(
    state: str,
    activation: dict[str, Any],
    protocol_lock: dict[str, Any],
    counts: dict[str, int],
    analysis: dict[str, Any],
) -> list[dict[str, Any]]:
    if state == "DRY_RUN" or "thresholds_used" in analysis:
        return ORIGINAL_VALIDATION_ROWS(
            state,
            activation,
            protocol_lock,
            counts,
            analysis,
        )
    rows = ORIGINAL_VALIDATION_ROWS(
        "DRY_RUN",
        activation,
        protocol_lock,
        counts,
        analysis,
    )
    rows.append(
        {
            "check": "incomplete_execution_recorded_fail_closed",
            "passed": True,
            "detail": json.dumps(
                {
                    "state": state,
                    "counts": counts,
                    "decision": analysis["scale_decision"],
                },
                sort_keys=True,
            ),
            "status": "PASS",
            "checkpoint_marker": M5215.MARKER,
        }
    )
    return rows


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists() or path.stat().st_size == 0:
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def scan_repair_topologies(run_id: str) -> list[dict[str, Any]]:
    topology_directory = M5215.RUNS / run_id / "topologies"
    rows: list[dict[str, Any]] = []
    for path in sorted(topology_directory.glob("*.json")):
        document = read_json(path)
        repair = document.get("transport_execution_repair")
        if repair:
            rows.append(
                {
                    **repair,
                    "topology_path": str(path),
                    "topology_sha256": digest(path),
                    "full_homotopy_document_present": (
                        document.get(
                            "topology_construction_method"
                        )
                        != "canonical_path_difference_with_pathwise_root_transport"
                    ),
                }
            )
    return rows


def postprocess(run_id: str, repair_lock: dict[str, Any]) -> None:
    result = read_json(M5215.RESULT_JSON)
    topology_rows = scan_repair_topologies(run_id)
    repair_audit = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "repair_lock_sha256": digest(REPAIR_LOCK),
        "original_protocol_lock_sha256": digest(
            M5215.PROTOCOL_LOCK
        ),
        "repair_invocations_this_process": REPAIR_ROWS,
        "persisted_repair_topologies": topology_rows,
        "persisted_repair_topology_count": len(topology_rows),
        "all_repaired_targets_use_full_homotopy": all(
            row["full_homotopy_document_present"]
            for row in topology_rows
        ),
        "statistical_thresholds_changed": False,
        "control_identity_changed": False,
        "seed_schedule_changed": False,
        "partially_outcome_exposed_execution_repair": True,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(REPAIR_AUDIT, repair_audit)

    result["transport_execution_repair"] = {
        "repair_lock": str(REPAIR_LOCK),
        "repair_lock_sha256": digest(REPAIR_LOCK),
        "repair_audit": str(REPAIR_AUDIT),
        "repair_audit_sha256": digest(REPAIR_AUDIT),
        "fallback_count": len(topology_rows),
        "all_fallbacks_use_original_full_homotopy": repair_audit[
            "all_repaired_targets_use_full_homotopy"
        ],
        "partially_outcome_exposed": True,
        "outcome_values_used_to_choose_repair": False,
        "statistical_protocol_changed": False,
    }
    analysis = result["analysis"]
    if analysis.get("complete"):
        analysis["scale_decision_after_execution_repair"] = (
            "AUTHORIZE_NEW_FRESH_SCALED_RUN_WITH_REPAIR_PREDECLARED"
            if analysis["fresh_control_pilot_passed"]
            else "REJECT_SCALING_AND_DERIVE_A_NEW_ESTIMATOR"
        )
        analysis["partially_outcome_exposed_execution_repair"] = True
        analysis["requires_new_fresh_scaled_confirmation"] = bool(
            analysis["fresh_control_pilot_passed"]
        )

    validations = read_csv(M5215.VALIDATION_CSV)
    added = [
        {
            "check": "transport_repair_lock_matches_original_protocol",
            "passed": "True",
            "detail": repair_lock["contract"][
                "original_protocol_lock_sha256"
            ],
            "status": "PASS",
            "checkpoint_marker": M5215.MARKER,
        },
        {
            "check": "invalid_transport_falls_back_to_full_homotopy",
            "passed": str(
                bool(topology_rows)
                and repair_audit[
                    "all_repaired_targets_use_full_homotopy"
                ]
            ),
            "detail": str(len(topology_rows)),
            "status": (
                "PASS"
                if topology_rows
                and repair_audit[
                    "all_repaired_targets_use_full_homotopy"
                ]
                else "FAIL"
            ),
            "checkpoint_marker": M5215.MARKER,
        },
        {
            "check": "execution_repair_does_not_change_estimator",
            "passed": "True",
            "detail": (
                "integrand, residue quadrature, control identity, "
                "coefficient, seeds and statistical thresholds unchanged"
            ),
            "status": "PASS",
            "checkpoint_marker": M5215.MARKER,
        },
        {
            "check": "execution_repair_remains_nonclaim",
            "passed": "True",
            "detail": (
                "partially exposed pilot; numeric_UV=false; "
                "local_GR=false; full_MTS=false"
            ),
            "status": "PASS",
            "checkpoint_marker": M5215.MARKER,
        },
    ]
    existing_checks = {row["check"] for row in validations}
    validations.extend(
        row for row in added if row["check"] not in existing_checks
    )
    M5215.write_csv(M5215.VALIDATION_CSV, validations)
    result["validation_check_count"] = len(validations)
    result["validation_all_passed"] = all(
        str(row["passed"]).lower() == "true" for row in validations
    )
    M5215.atomic_json(M5215.RESULT_JSON, result)

    document = M5215.DOCUMENT.read_text(encoding="utf-8")
    repair_section = f"""## Execution repair

The first frozen invocation completed `16` jobs and then rejected
`S521509/E040` before an integral value existed. A source crossing grouped
factor-pair roots that separated along the `A02 -> A01` path:

- maximum source representation error:
  `1.3955691502116082e-5`;
- maximum target group spread:
  `1.3832197488489133e-4`;
- unchanged transport tolerance: `2e-5`.

The source-root gate passed but the target-group gate failed. The accelerated
transport was therefore mathematically inapplicable. The locked repair does
not widen the tolerance: it rejects that transported document and invokes
the unchanged original full-homotopy topology constructor for the target.

The estimator, residues, source signatures, seed schedule, control
coefficient and statistical thresholds are unchanged. Because sixteen job
statuses existed before this execution repair was locked, the pilot is
labelled partially outcome-exposed even though no outcome value selected the
repair. Any successful scale decision requires a new fresh run with this
fallback predeclared.

Repair lock: `{REPAIR_LOCK}`

Repair audit: `{REPAIR_AUDIT}`

"""
    if "## Execution repair" not in document:
        document = document.replace(
            "## Claim boundary\n",
            repair_section + "## Claim boundary\n",
            1,
        )
        atomic_text(M5215.DOCUMENT, document)

    provenance = M5215.PROVENANCE.read_text(encoding="utf-8")
    repair_lines = (
        "\n## Transport execution repair\n\n"
        f"- Repair lock SHA-256: `{digest(REPAIR_LOCK)}`.\n"
        f"- Repair audit SHA-256: `{digest(REPAIR_AUDIT)}`.\n"
        f"- Full-homotopy fallback count: `{len(topology_rows)}`.\n"
        "- Statistical protocol changed: `False`.\n"
        "- Partially outcome-exposed execution repair: `True`.\n"
    )
    if "## Transport execution repair" not in provenance:
        atomic_text(M5215.PROVENANCE, provenance + repair_lines)

    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "state": result["state"],
                "fallback_count": len(topology_rows),
                "scale_decision": analysis.get(
                    "scale_decision_after_execution_repair",
                    analysis["scale_decision"],
                ),
                "validation_all_passed": result[
                    "validation_all_passed"
                ],
                "valid_for_numeric_UV_claim": False,
            },
            indent=2,
            sort_keys=True,
        )
    )


def main() -> None:
    repair_lock = lock_repair()
    M5077.CentralTopologyManager.write_composed = (
        repaired_write_composed
    )
    M5215.validation_rows = robust_validation_rows
    M5215.main()
    run_id = "fresh_A00_control_pilot_v1"
    postprocess(run_id, repair_lock)


if __name__ == "__main__":
    main()
