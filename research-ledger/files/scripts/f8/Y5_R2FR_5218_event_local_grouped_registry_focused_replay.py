from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5218"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SCRIPT_5215_TRANSPORT = (
    POST
    / "scripts"
    / "Y5_R2FR_5215_transport_invalid_full_homotopy_repair.py"
)
SCRIPT_5217 = (
    POST
    / "scripts"
    / "Y5_R2FR_5217_L64_owned_direct_zero_confirmation.py"
)
SOURCE_5215 = POST / "source-intake" / "functional_rg" / "5215"
SOURCE_5217 = POST / "source-intake" / "functional_rg" / "5217"
TRANSPORT_LOCK = SOURCE_5215 / "frozen_transport_repair_lock.json"
REGISTRY_5217 = SOURCE_5217 / "resolved_grouped_owned_direct_registry.json"
RESULT_5217 = SOURCE_5217 / "L64_owned_direct_zero_confirmation.json"
SOURCE_JOB = (
    SOURCE_5215
    / "runs"
    / "fresh_A00_control_pilot_v1"
    / "topological-jobs"
    / "TOP__E040__S521509_N0000__A00__primary24.json"
)
LOCK = SOURCE / "event_local_grouped_registry_replay_lock.json"
PRE_REPLAY_JOB = SOURCE / "pre_replay_job_snapshot.json"
REPAIR_AUDIT = SOURCE / "event_local_grouped_registry_repair_audit.json"
RESULT = SOURCE / "event_local_grouped_registry_focused_replay.json"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5218_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5218-Y5-R2FR-event-local-grouped-registry-focused-replay.md"
)
MARKER = "MTS_5218_EVENT_LOCAL_GROUPED_REGISTRY_FOCUSED_REPLAY"
REVISION = "exact-registry-kernel-replay-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
JOB_KEY = "TOP__E040__S521509_N0000__A00__primary24"
ROOT_MATCH_TOLERANCE = 2.0e-8


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


MTRANSPORT = load_module(
    "mts_5215_transport_for_5218",
    SCRIPT_5215_TRANSPORT,
)
M5215 = MTRANSPORT.M5215
M5212 = M5215.M5212
ORIGINAL_CATALOG = M5212.certified_5212_catalog
REPAIR_ROWS: list[dict[str, Any]] = []


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
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def canonical_pairs(value: list[list[str]]) -> list[list[str]]:
    return [
        list(pair)
        for pair in sorted(
            tuple(sorted((str(pair[0]), str(pair[1])))) for pair in value
        )
    ]


def complex_from_row(value: dict[str, Any]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def registry_rows() -> list[dict[str, Any]]:
    registry = read_json(REGISTRY_5217)
    if (
        not registry["event_local_registry_complete"]
        or not registry["future_fresh_runner_integration_authorized"]
    ):
        raise RuntimeError("checkpoint-5217 registry is incomplete")
    return registry["rows"]


def lock_contract() -> dict[str, Any]:
    transport = read_json(TRANSPORT_LOCK)
    result_5217 = read_json(RESULT_5217)
    source_job = read_json(SOURCE_JOB)
    if (
        transport["contract"]["repair_runner_sha256"]
        != digest(SCRIPT_5215_TRANSPORT)
    ):
        raise RuntimeError("locked transport repair changed")
    if (
        not result_5217["validation_all_passed"]
        or not result_5217[
            "future_fresh_runner_integration_authorized"
        ]
    ):
        raise RuntimeError("checkpoint-5217 did not authorize integration")
    if source_job["status"] != "COMPLETED_UNCONVERGED":
        raise RuntimeError("focused source job is no longer unconverged")
    if not PRE_REPLAY_JOB.exists():
        atomic_json(PRE_REPLAY_JOB, source_job)
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "runner_sha256": digest(Path(__file__).resolve()),
        "script_5215_transport_sha256": digest(
            SCRIPT_5215_TRANSPORT
        ),
        "script_5217_sha256": digest(SCRIPT_5217),
        "transport_lock_sha256": digest(TRANSPORT_LOCK),
        "registry_5217_sha256": digest(REGISTRY_5217),
        "result_5217_sha256": digest(RESULT_5217),
        "pre_replay_job_sha256": digest(PRE_REPLAY_JOB),
        "job_key": JOB_KEY,
        "replacement_scope": (
            "exact job, event, argument, chamber, canonical pair set "
            "and relative collision root only"
        ),
        "root_match_relative_tolerance": ROOT_MATCH_TOLERANCE,
        "unmatched_unstable_action": "fail_closed",
        "integrand_changed": False,
        "contour_quadrature_changed": False,
        "double_precision_tolerance_changed": False,
        "development_event_outcome_exposed": True,
        "current_5215_scale_decision_allowed": False,
        "valid_for_numeric_UV_claim": False,
    }


def create_or_verify_lock() -> dict[str, Any]:
    if LOCK.exists():
        locked = read_json(LOCK)
        contract = locked["contract"]
        checks = (
            contract["runner_sha256"]
            == digest(Path(__file__).resolve()),
            contract["script_5215_transport_sha256"]
            == digest(SCRIPT_5215_TRANSPORT),
            contract["script_5217_sha256"] == digest(SCRIPT_5217),
            contract["registry_5217_sha256"] == digest(REGISTRY_5217),
            contract["pre_replay_job_sha256"] == digest(PRE_REPLAY_JOB),
        )
        if not all(checks):
            raise RuntimeError("checkpoint-5218 locked sources changed")
        return locked
    contract = lock_contract()
    locked = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "locked_at_utc": datetime.now(timezone.utc).isoformat(),
        "contract": contract,
        "replay_outcome_present_at_lock": False,
        "development_event_outcome_exposed": True,
        "current_5215_scale_decision_allowed": False,
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(LOCK, locked)
    return locked


def chamber_index_for(
    ownership: dict[str, bool],
) -> int:
    ownerships = M5212.M5077.M5036.N5030.physical_chambers()[1]
    matches = [
        index
        for index, candidate in enumerate(ownerships)
        if candidate == ownership
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"ownership matched {len(matches)} physical chambers"
        )
    return matches[0]


def matching_registry_row(
    row: dict[str, Any],
    chamber_index: int,
) -> dict[str, Any] | None:
    current_event = M5212.M5077.CURRENT_EVENT
    current_argument = M5212.M5077.CURRENT_ARGUMENT
    current_job = M5212.M5077.M5036.MREPAIR.CURRENT_JOB
    if current_event is None or current_argument is None:
        return None
    root = complex(row["root"])
    pairs = canonical_pairs(row["pairs"])
    matches = []
    for candidate in registry_rows():
        signature = candidate["signature"]
        candidate_root = complex_from_row(signature["root"])
        residual = abs(root - candidate_root) / max(
            1.0,
            abs(root),
            abs(candidate_root),
        )
        if (
            current_job == candidate["job_key"]
            and current_event["event_id"] == candidate["event_id"]
            and current_argument["argument_id"]
            == candidate["argument_id"]
            and chamber_index == int(signature["chamber_index"])
            and pairs == signature["pairs"]
            and residual <= ROOT_MATCH_TOLERANCE
            and candidate["stable"]
            and candidate["grouped_classification"]
            == "STABLE_GROUPED_DIRECT_NONZERO"
        ):
            matches.append((candidate, residual))
    if len(matches) > 1:
        raise RuntimeError("grouped registry row matched ambiguously")
    if not matches:
        return None
    return {**matches[0][0], "root_match_residual": matches[0][1]}


def certified_catalog_with_event_local_grouped_registry(
    ownership: dict[str, bool],
    start: complex,
    end: complex,
    required_roots: list[complex],
    global_nodes: int,
    global_residue_nodes: int,
    relative_residue_nodes: int,
    model_distance: float,
) -> tuple[list[dict[str, Any]], bool]:
    catalog, stable = ORIGINAL_CATALOG(
        ownership,
        start,
        end,
        required_roots,
        global_nodes,
        global_residue_nodes,
        relative_residue_nodes,
        model_distance,
    )
    if stable:
        return catalog, stable
    chamber_index = chamber_index_for(ownership)
    repaired = []
    for row in catalog:
        if bool(row["stable"]):
            repaired.append(row)
            continue
        registry = matching_registry_row(row, chamber_index)
        if registry is None:
            repaired.append(row)
            continue
        replacement = complex_from_row(registry["replacement_residue"])
        repaired_row = {
            **row,
            "outer_residue": replacement,
            "inner_residue": replacement,
            "residue": replacement,
            "residue_stability": 0.0,
            "numerically_zero": False,
            "stable": True,
            "event_local_grouped_direct_registry_repair": {
                "checkpoint_marker": MARKER,
                "registry": str(REGISTRY_5217),
                "registry_sha256": digest(REGISTRY_5217),
                "root_match_residual": registry[
                    "root_match_residual"
                ],
                "scope": registry["scope"],
                "current_5215_scale_decision_allowed": False,
            },
        }
        repaired.append(repaired_row)
        REPAIR_ROWS.append(
            {
                "job_key": M5212.M5077.M5036.MREPAIR.CURRENT_JOB,
                "event_id": M5212.M5077.CURRENT_EVENT["event_id"],
                "argument_id": M5212.M5077.CURRENT_ARGUMENT[
                    "argument_id"
                ],
                "chamber_index": chamber_index,
                "root": str(row["root"]),
                "pairs": row["pairs"],
                "replacement_residue": registry[
                    "replacement_residue"
                ],
                "root_match_residual": registry[
                    "root_match_residual"
                ],
                "valid_for_numeric_UV_claim": False,
            }
        )
    return repaired, all(bool(row["stable"]) for row in repaired)


def install_runtime() -> tuple[dict[str, Any], Any, dict[str, Any]]:
    MTRANSPORT.lock_repair()
    MTRANSPORT.M5077.CentralTopologyManager.write_composed = (
        MTRANSPORT.repaired_write_composed
    )
    M5212.certified_5212_catalog = (
        certified_catalog_with_event_local_grouped_registry
    )
    manifest = M5215.read_json(M5215.MANIFEST)
    config = M5215.make_config(manifest, "fresh_A00_control_pilot_v1")
    jobs = M5215.build_schedule(config, manifest)
    matches = [job for job in jobs if job["job_key"] == JOB_KEY]
    if len(matches) != 1:
        raise RuntimeError(f"focused job matched {len(matches)} rows")
    M5212.source_separated_cluster_gate()
    M5212.M5077.certified_primary_catalog = (
        M5212.certified_5212_catalog
    )
    M5212.M5077.M5085.CertifiedRemovableGlobalExtension = (
        M5212.AdaptiveRemovableGlobalExtension
    )
    M5212.M5077.install_history_invariant_breakpoints(
        M5212.M5077.M5036.N5030
    )
    run_directory = (
        SOURCE_5215 / "runs" / "fresh_A00_control_pilot_v1"
    )
    manager = M5212.M5077.CentralTopologyManager(
        run_directory,
        config,
    )
    return config, manager, matches[0]


def finalize(job: dict[str, Any]) -> dict[str, Any]:
    formal_digest = tree_digest(FORMAL)
    validations = [
        (
            "formalization_workbench_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
        (
            "exact_three_registry_rows_applied",
            len(REPAIR_ROWS) == 3,
            str(len(REPAIR_ROWS)),
        ),
        (
            "focused_job_completed_converged",
            job["status"] == "COMPLETED_CONVERGED",
            job["status"],
        ),
        (
            "focused_job_residues_stable",
            bool(job["residues_stable"]),
            str(job["residues_stable"]),
        ),
        (
            "focused_job_structural_gates_pass",
            bool(
                job["all_crossings_reciprocally_paired"]
                and job["all_partition_ratios_finite"]
                and job["selected_control_pairs_safe_and_direct"]
            ),
            (
                f"pairs={job['all_crossings_reciprocally_paired']};"
                f" ratios={job['all_partition_ratios_finite']};"
                f" selected={job['selected_control_pairs_safe_and_direct']}"
            ),
        ),
        (
            "current_exposed_pilot_not_used_for_scale_decision",
            True,
            "focused replay is pipeline validation only",
        ),
        (
            "claim_flags_remain_false",
            not bool(
                job["valid_for_numeric_UV_claim"]
                or job["valid_for_local_GR_claim"]
                or job["valid_for_full_MTS_claim"]
            ),
            "numeric UV, local GR and full MTS remain false",
        ),
    ]
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for name, passed, detail in validations:
            writer.writerow((name, str(bool(passed)).lower(), detail))
    audit = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "repair_rows": REPAIR_ROWS,
        "repair_row_count": len(REPAIR_ROWS),
        "source_registry": str(REGISTRY_5217),
        "source_registry_sha256": digest(REGISTRY_5217),
        "development_event_outcome_exposed": True,
        "current_5215_scale_decision_allowed": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(REPAIR_AUDIT, audit)
    passed = all(row[1] for row in validations)
    result = {
        "checkpoint": 5218,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "state": "COMPLETE" if passed else "BLOCKED",
        "focused_job_key": JOB_KEY,
        "focused_job_status": job["status"],
        "focused_job_residues_stable": bool(job["residues_stable"]),
        "repair_audit_sha256": digest(REPAIR_AUDIT),
        "current_5215_scale_decision_allowed": False,
        "new_fresh_predeclared_run_required_for_scale_decision": True,
        "formalization_workbench_tree_sha256": formal_digest,
        "validation_all_passed": passed,
        "validation_check_count": len(validations),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)
    lines = [
        "# 5218 - Event-local grouped-registry focused replay",
        "",
        "## Purpose",
        "",
        "The three exact checkpoint-5217 grouped residues were integrated",
        "into the unchanged checkpoint-5215 kernel policy and only the",
        "previously blocked `S521509/E040/A00` job was replayed.",
        "",
        "## Result",
        "",
        f"- Focused job status: `{job['status']}`.",
        f"- Exact registry rows applied: `{len(REPAIR_ROWS)}`.",
        f"- Residues stable: `{job['residues_stable']}`.",
        f"- Validation: `{sum(1 for row in validations if row[1])}/"
        f"{len(validations)}`.",
        "",
        "No contour, integrand, root tolerance, source event, control",
        "coefficient or statistical threshold was changed.",
        "",
        "## Claim boundary",
        "",
        "This replay validates the exact repair path on an outcome-exposed",
        "event. It cannot rescue the current pilot's scale decision. A new",
        "fresh run must predeclare a general grouped-owned-direct classifier.",
        "",
        "## Evidence",
        "",
        f"- Lock: `{LOCK}`",
        f"- Pre-replay snapshot: `{PRE_REPLAY_JOB}`",
        f"- Repair audit: `{REPAIR_AUDIT}`",
        f"- Result: `{RESULT}`",
        f"- Validation: `{VALIDATION}`",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def execute() -> dict[str, Any]:
    config, manager, selected = install_runtime()
    run_directory = (
        SOURCE_5215 / "runs" / "fresh_A00_control_pilot_v1"
    )
    row = M5215.execute_job(
        run_directory,
        config,
        manager,
        selected,
    )
    return finalize(row)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("lock", "run"),
        default="lock",
    )
    arguments = parser.parse_args()
    locked = create_or_verify_lock()
    if arguments.mode == "lock":
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "state": "LOCKED_AWAITING_FOCUSED_REPLAY",
                    "lock": str(LOCK),
                    "lock_sha256": digest(LOCK),
                    "job_key": locked["contract"]["job_key"],
                    "valid_for_numeric_UV_claim": False,
                },
                indent=2,
                sort_keys=True,
            )
        )
        return
    execute()


if __name__ == "__main__":
    main()
