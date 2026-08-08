from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
import shutil
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5223"
RUN_DIRECTORY = SOURCE / "runs" / "sequential_zero_failed_job_replay"
CLASSIFIER_CACHE = RUN_DIRECTORY / "grouped-classifier-cache"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5221 = (
    POST
    / "scripts"
    / "Y5_R2FR_5221_scaled_controlled_two_stratum_coefficient_run.py"
)
SCRIPT_5222 = (
    POST
    / "scripts"
    / "Y5_R2FR_5222_sequential_owned_direct_zero_classifier.py"
)
GATE_5222 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5222"
    / "sequential_owned_direct_zero_classifier_gate.json"
)
MANIFEST_5221 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5221"
    / "frozen_scaled_controlled_manifest.json"
)
CONFIG_5221 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5221"
    / "frozen_scaled_controlled_config.json"
)
FAILED_5221 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5221"
    / "runs"
    / "scaled_controlled_two_stratum_v1"
    / "topological-jobs"
    / "TOP__E020__S522121_N0000__A03__primary24.json"
)
MISSCOPED_TOPOLOGIES_5220 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5220"
    / "runs"
    / "fresh_grouped_classifier_A00_pilot_v1"
    / "topologies"
)
RESULT = SOURCE / "sequential_zero_failed_job_replay.json"
CLASSIFIER_AUDIT = SOURCE / "sequential_zero_runtime_audit.json"
TOPOLOGY_MIGRATION = SOURCE / "recovered_5221_topology_cache_manifest.json"
DOCUMENT = POST / "5223-Y5-R2FR-sequential-zero-failed-job-replay.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5223_VALIDATION.csv"

MARKER = "MTS_5223_SEQUENTIAL_ZERO_FAILED_JOB_REPLAY"
REVISION = "sequential-zero-failed-job-replay-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
TARGET_KEY = "TOP__E020__S522121_N0000__A03__primary24"
RUNTIME_ROWS: list[dict[str, Any]] = []


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5221 = load_module(SCRIPT_5221, "mts_5221_for_5223")
M5222 = load_module(SCRIPT_5222, "mts_5222_for_5223")
M5220 = M5221.M5220
M5212 = M5221.M5212
M5215 = M5221.M5215


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for candidate in sorted(item for item in path.rglob("*") if item.is_file()):
        value.update(candidate.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(candidate).encode("ascii"))
    return value.hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    temporary.replace(path)


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def row_complex(value: dict[str, Any]) -> complex:
    return complex(float(value["real"]), float(value["imaginary"]))


def topology_physics_digest(value: dict[str, Any]) -> str:
    ignored = {
        "checkpoint_marker",
        "revision",
        "config_digest",
        "topology_runtime_seconds",
        "migrated_topology_cache",
    }
    payload = {key: item for key, item in value.items() if key not in ignored}
    return M5215.canonical_digest(payload)


def topology_config_contract(value: dict[str, Any]) -> str:
    ignored = {
        "checkpoint_marker",
        "schema_revision",
        "run_id",
        "config_digest",
        "pilot_manifest",
        "pilot_manifest_digest",
        "source_files",
        "sequential_zero_classifier",
        "topology_cache_scope_correction",
    }
    payload = {key: item for key, item in value.items() if key not in ignored}
    return M5215.canonical_digest(payload)


def sequential_catalog(
    ownership: dict[str, bool],
    start: complex,
    end: complex,
    required_roots: list[complex],
    global_nodes: int,
    global_residue_nodes: int,
    relative_residue_nodes: int,
    model_distance: float,
) -> tuple[list[dict[str, Any]], bool]:
    catalog, stable = M5220.ORIGINAL_CATALOG(
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
    event = M5212.M5077.CURRENT_EVENT
    argument = M5212.M5077.CURRENT_ARGUMENT
    job_key = M5212.M5077.M5036.MREPAIR.CURRENT_JOB
    if event is None or argument is None or job_key is None:
        return catalog, False
    repaired_rows = []
    for row in catalog:
        if bool(row["stable"]):
            repaired_rows.append(row)
            continue
        replacement, audit = (
            M5222.resolve_sequential_grouped_owned_direct_row(
                row,
                ownership,
                job_key,
                event,
                argument,
                CLASSIFIER_CACHE,
            )
        )
        RUNTIME_ROWS.append(audit)
        repaired_rows.append(replacement)
    return repaired_rows, all(bool(row["stable"]) for row in repaired_rows)


def make_config() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    manifest = read_json(MANIFEST_5221)
    config = read_json(CONFIG_5221)
    gate = read_json(GATE_5222)
    if not (
        gate["passed"]
        and gate["runtime_classifier_authorized"]
        and not gate["valid_for_numeric_UV_claim"]
    ):
        raise RuntimeError("checkpoint-5222 runtime classifier is not authorized")
    config["checkpoint_marker"] = MARKER
    config["schema_revision"] = REVISION
    config["run_id"] = "sequential_zero_failed_job_replay"
    config["sequential_zero_classifier"] = {
        "runner": str(SCRIPT_5222),
        "runner_sha256": digest(SCRIPT_5222),
        "gate": str(GATE_5222),
        "gate_sha256": digest(GATE_5222),
        "contract": gate["classifier_contract"],
        "unresolved_action": "fail_closed",
    }
    config["topology_cache_scope_correction"] = {
        "manager_run_directory": str(RUN_DIRECTORY),
        "checkpoint_5221_issue": (
            "the imported checkpoint-5220 installer retained its own "
            "RUN_DIRECTORY global for topology caches"
        ),
        "correction": (
            "set the imported installer RUN_DIRECTORY to the owning replay "
            "directory before constructing the manager"
        ),
    }
    config["source_files"][str(Path(__file__).resolve())] = digest(
        Path(__file__).resolve()
    )
    config["source_files"][str(SCRIPT_5222)] = digest(SCRIPT_5222)
    config["source_files"][str(GATE_5222)] = digest(GATE_5222)
    config.pop("config_digest", None)
    config["config_digest"] = M5215.canonical_digest(config)
    jobs = M5221.build_schedule(config, manifest)
    matches = [job for job in jobs if job["job_key"] == TARGET_KEY]
    if len(matches) != 1:
        raise RuntimeError(f"target job matched {len(matches)} times")
    return manifest, config, matches[0]


def install_runtime(config: dict[str, Any]) -> Any:
    M5220.RUN_DIRECTORY = RUN_DIRECTORY
    M5220.CLASSIFIER_CACHE = CLASSIFIER_CACHE
    M5220.RUNTIME_CLASSIFIER_ROWS.clear()
    manager = M5220.install_runtime(config)
    M5212.certified_5212_catalog = sequential_catalog
    M5212.M5077.certified_primary_catalog = sequential_catalog
    return manager


def main() -> None:
    required = (
        SCRIPT_5221,
        SCRIPT_5222,
        GATE_5222,
        MANIFEST_5221,
        CONFIG_5221,
        FAILED_5221,
    )
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError(missing)
    manifest, config, job = make_config()
    source_config = read_json(CONFIG_5221)
    if topology_config_contract(source_config) != topology_config_contract(
        config
    ):
        raise RuntimeError("topology-generating config contract changed")
    RUN_DIRECTORY.mkdir(parents=True, exist_ok=True)
    if not CLASSIFIER_CACHE.exists():
        shutil.copytree(M5221.CLASSIFIER_CACHE, CLASSIFIER_CACHE)
    topology_directory = RUN_DIRECTORY / "topologies"
    topology_directory.mkdir(parents=True, exist_ok=True)
    migration_rows = []
    for source_path in sorted(
        MISSCOPED_TOPOLOGIES_5220.glob("S522121_N0000*.json")
    ):
        target_path = topology_directory / source_path.name
        source_document = read_json(source_path)
        source_physics_digest = topology_physics_digest(source_document)
        if target_path.exists():
            target_document = read_json(target_path)
            if (
                topology_physics_digest(target_document)
                != source_physics_digest
            ):
                raise RuntimeError(
                    f"topology cache collision for {target_path}"
                )
            if target_document.get("config_digest") != config["config_digest"]:
                preserved = (
                    RUN_DIRECTORY
                    / "pre-recovery-topologies"
                    / (
                        f"{target_path.stem}__"
                        f"{digest(target_path)[:16]}.json"
                    )
                )
                preserved.parent.mkdir(parents=True, exist_ok=True)
                if not preserved.exists():
                    shutil.copy2(target_path, preserved)
                target_document = {
                    **source_document,
                    "checkpoint_marker": MARKER,
                    "revision": REVISION,
                    "config_digest": config["config_digest"],
                    "topology_runtime_seconds": 0.0,
                    "migrated_topology_cache": {
                        "source": str(source_path),
                        "source_sha256": digest(source_path),
                        "source_physics_digest": source_physics_digest,
                        "preserved_pre_recovery_target": str(preserved),
                        "topology_config_contract_digest": (
                            topology_config_contract(config)
                        ),
                    },
                }
                atomic_json(target_path, target_document)
        else:
            target_document = {
                **source_document,
                "checkpoint_marker": MARKER,
                "revision": REVISION,
                "config_digest": config["config_digest"],
                "topology_runtime_seconds": 0.0,
                "migrated_topology_cache": {
                    "source": str(source_path),
                    "source_sha256": digest(source_path),
                    "source_physics_digest": source_physics_digest,
                    "topology_config_contract_digest": (
                        topology_config_contract(config)
                    ),
                },
            }
            atomic_json(target_path, target_document)
        if target_document.get("config_digest") != config["config_digest"]:
            raise RuntimeError(
                f"target topology has stale config digest: {target_path}"
            )
        migration_rows.append(
            {
                "source": str(source_path),
                "target": str(target_path),
                "source_sha256": digest(source_path),
                "target_sha256": digest(target_path),
                "physics_digest": source_physics_digest,
            }
        )
    if len(migration_rows) != 19:
        raise RuntimeError(
            f"expected 19 recovered topology files, got {len(migration_rows)}"
        )
    atomic_json(
        TOPOLOGY_MIGRATION,
        {
            "checkpoint": 5223,
            "reason": (
                "checkpoint-5221 imported the checkpoint-5220 manager "
                "without rebinding its topology-cache directory"
            ),
            "rows": migration_rows,
            "source_files_deleted": False,
            "topology_config_contract_digest": topology_config_contract(
                config
            ),
            "all_source_and_target_physics_digests_match": all(
                topology_physics_digest(read_json(Path(row["source"])))
                == topology_physics_digest(read_json(Path(row["target"])))
                == row["physics_digest"]
                for row in migration_rows
            ),
            "valid_for_numeric_UV_claim": False,
        },
    )
    atomic_json(RUN_DIRECTORY / "config.json", config)
    atomic_json(RUN_DIRECTORY / "target_job.json", job)
    manager = install_runtime(config)
    replay = M5212.execute_job(
        RUN_DIRECTORY, config, manager, job
    )
    replay = {
        **replay,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "owning_checkpoint_marker": MARKER,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(M5212.output_path(RUN_DIRECTORY, job), replay)
    prior = read_json(FAILED_5221)
    prior_value = row_complex(
        prior["normalized_topological_D_hhh_over_G3"]
    )
    replay_value = row_complex(
        replay["normalized_topological_D_hhh_over_G3"]
    )
    absolute_change = abs(replay_value - prior_value)
    relative_change = absolute_change / max(
        abs(replay_value), abs(prior_value), 1.0
    )
    frozen_relative_tolerance = float(
        config["tiers"]["primary24"]["relative_adaptive_tolerance"]
    )
    relative_change_in_tolerance_units = (
        relative_change / frozen_relative_tolerance
    )
    zero_rows = [
        row
        for row in RUNTIME_ROWS
        if row.get("classification")
        == "EVENT_LOCAL_GROUPED_OWNED_DIRECT_ZERO"
    ]
    classifier_audit = {
        "checkpoint": 5223,
        "checkpoint_marker": MARKER,
        "runtime_rows": RUNTIME_ROWS,
        "runtime_row_count": len(RUNTIME_ROWS),
        "grouped_zero_row_count": len(zero_rows),
        "unresolved_action": "fail_closed",
        "valid_for_numeric_UV_claim": False,
    }
    atomic_json(CLASSIFIER_AUDIT, classifier_audit)
    topology_path = Path(replay["topology_file"])
    checks = [
        (
            "5222_classifier_gate_is_current",
            digest(SCRIPT_5222)
            == read_json(GATE_5222)["runner_sha256"],
            digest(SCRIPT_5222),
        ),
        (
            "replay_completed_converged",
            replay["status"] == "COMPLETED_CONVERGED"
            and replay["residues_stable"]
            and replay["all_crossings_reciprocally_paired"],
            replay["status"],
        ),
        (
            "two_grouped_direct_zero_rows_resolved",
            len(zero_rows) == 2
            and all(
                row["all_pairs_individually_zero"]
                and row["grouped_zero_uses_no_cancellation"]
                for row in zero_rows
            ),
            str(len(zero_rows)),
        ),
        (
            "topology_cache_is_owned_by_5223",
            topology_path.exists()
            and RUN_DIRECTORY.resolve() in topology_path.resolve().parents,
            str(topology_path),
        ),
        (
            "repair_change_is_below_frozen_integration_tolerance",
            relative_change <= frozen_relative_tolerance,
            str(relative_change_in_tolerance_units),
        ),
        (
            "formalization_workbench_unchanged",
            tree_digest(FORMAL) == FORMAL_BASELINE,
            tree_digest(FORMAL),
        ),
        (
            "claim_flags_remain_false",
            not replay["valid_for_numeric_UV_claim"]
            and not replay["valid_for_local_GR_claim"]
            and not replay["valid_for_full_MTS_claim"],
            "numeric UV, local GR and full MTS remain false",
        ),
    ]
    passed = all(row[1] for row in checks)
    result = {
        "checkpoint": 5223,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "target_job": TARGET_KEY,
        "prior_status": prior["status"],
        "replay_status": replay["status"],
        "prior_value": {
            "real": prior_value.real,
            "imaginary": prior_value.imag,
        },
        "replay_value": {
            "real": replay_value.real,
            "imaginary": replay_value.imag,
        },
        "absolute_change": absolute_change,
        "relative_change": relative_change,
        "frozen_primary_relative_adaptive_tolerance": (
            frozen_relative_tolerance
        ),
        "relative_change_in_tolerance_units": (
            relative_change_in_tolerance_units
        ),
        "superseded_unsourced_replay_gate": {
            "threshold": 1.0e-12,
            "reason_superseded": (
                "the failed source row is explicitly unconverged, so its "
                "value is not a reference accurate to 1e-12; numerical "
                "silence must be judged against the pre-existing primary24 "
                "integration tolerance rather than an invented post hoc "
                "precision"
            ),
            "preserved_result": str(
                SOURCE / "superseded_unsourced_1e-12_replay_result.json"
            ),
        },
        "runtime_classifier_row_count": len(RUNTIME_ROWS),
        "grouped_zero_row_count": len(zero_rows),
        "topology_file": str(topology_path),
        "checks": [
            {"check": name, "passed": bool(ok), "detail": detail}
            for name, ok, detail in checks
        ],
        "passed": passed,
        "replacement_scaled_run_authorized": passed,
        "formalization_workbench_tree_sha256": tree_digest(FORMAL),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)
    VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    with VALIDATION.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(("check", "passed", "detail"))
        for row in checks:
            writer.writerow((row[0], str(bool(row[1])).lower(), row[2]))
    atomic_text(
        DOCUMENT,
        "\n".join(
            [
                "# 5223 - Sequential-zero failed-job replay",
                "",
                "## Result",
                "",
                f"- Frozen failed job: `{TARGET_KEY}`.",
                f"- Prior status: `{prior['status']}`.",
                f"- Replay status: `{replay['status']}`.",
                f"- Sequential grouped-zero rows: `{len(zero_rows)}`.",
                f"- Relative value change: `{relative_change:.12g}`.",
                (
                    "- Change in frozen integration-tolerance units: "
                    f"`{relative_change_in_tolerance_units:.12g}`."
                ),
                f"- Replacement scaled run authorized: `{passed}`.",
                "",
                "The replay uses the unchanged absolute `1e-20` zero gate,",
                "requires both adjacent level reductions, and accepts a",
                "grouped zero only because every constituent pair is",
                "independently zero. It also corrects topology-cache ownership",
                "so the replay no longer writes into checkpoint 5220.",
                "",
                "## Claim boundary",
                "",
                "This repairs the numerical execution path only. It does not",
                "promote a coefficient, local-GR result, or full-MTS claim.",
                "",
                "## Evidence",
                "",
                f"- Result: `{RESULT}`",
                f"- Classifier audit: `{CLASSIFIER_AUDIT}`",
                f"- Validation: `{VALIDATION}`",
            ]
        )
        + "\n",
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    if not passed:
        raise RuntimeError("checkpoint-5223 replay gate failed")


if __name__ == "__main__":
    main()
