from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import sys
import time
import traceback
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
sys.dont_write_bytecode = True


CHECKPOINT = 5338
MARKER = "MTS_5338_D4_E0025_TARGETED_SUPPORT_EXIT_DEPTH4_REFINEMENT"
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
RESIDUALS = POST / "source-intake" / "mts_residuals"
VALIDATION = RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
RESULT = OUT / "D4_E0025_targeted_depth4_result.json"
STATUS = OUT / "status.json"
PREFLIGHT = OUT / "D4_E0025_depth4_preflight.csv"
PREPARE_VALIDATION = OUT / "D4_E0025_depth4_prepare_validation.csv"
MIGRATION = OUT / "D4_E0025_depth4_shard_migration.csv"
OLD_INVENTORY = OUT / "D4_E0025_pre_depth4_shard_inventory.csv"
LEAF_AUDIT = OUT / "D4_E0025_depth4_leaf_audit.csv"
SOURCE_REGISTER = OUT / "source_register.csv"
SNAPSHOT = OUT / "pre-depth4"
SNAPSHOT_MANIFEST = SNAPSHOT / "snapshot_manifest.csv"
SCRIPT_5334 = SCRIPTS / "Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py"
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
TARGET_BRANCH = "P12S02LLL"
TARGET_CHILDREN = ("P12S02LLLL", "P12S02LLLR")
OLD_MAXIMUM_DEPTH = 3
NEW_MAXIMUM_DEPTH = 4
EXPECTED_OLD_NODE_COUNT = 432
EXPECTED_OLD_PANEL_COUNT = 36
EXPECTED_OLD_LEAF_COUNT = 31
EXPECTED_NEW_NODE_COUNT = 24
LOCAL_OUTER_CHANGE_LIMIT = 5.0e-3
GLOBAL_ERROR_BUDGET_LIMIT = 1.0e-2

IMMUTABLE_LOCKS = {
    "scripts/Y5_R2FR_5326_D2_midpoint_event_aligned_E0025_refinement.py": "d14ddc258c3d95deb82cddcb6dc219eb06fde8edb5fe851d02d89188e3c5e032",
    "scripts/Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py": "8da808982fdfc61c45af9f349467ea4c38a62e9d470569714cf739d07fb6f2c8",
    "scripts/Y5_R2FR_5337_D4_regulator_fold_double_scaling_and_contrast_gate.py": "16953dda8588675845bbb7fc146898d684e30be0aea13b6634834453f5022a7e",
    "5337-Y5-R2FR-D4-regulator-fold-double-scaling-and-contrast-gate.md": "337132436b54519f8952b03fc9469de98a763ed3d1d7e98ae0a9a72f15461127",
    "source-intake/functional_rg/5337/D4_regulator_fold_double_scaling_contrast_result.json": "60811d04aa47c8b8c34121547eab6c2dacd639465a942c1a45ad564c9d595b54",
    "source-intake/mts_residuals/P8_Y5_BRR545_5337_VALIDATION.csv": "0c62e4f7d9c1a22aacb695cfe16c5df348ebdae8ab25dc21c3cc835e97ce4ea4",
    "source-intake/functional_rg/5334/E0025/D4_outer_refined_support_events.csv": "c50085b936f4d6f7aad04f3d5f875b7804945b88ffcc0d8249c603c96bd9b158",
    "source-intake/functional_rg/5334/E0025/D4_outer_reduced_MC04_cubature_contract.csv": "0f691d1fa568d930a2d362e3f6aafdad1aee2746f43dcba4709590b3ead96cc2",
}

MUTABLE_LOCKS = {
    "source-intake/functional_rg/5334/E0025/D4_outer_event_aligned_E0025_result.json": "285f134f9ce8145545905dbd2fdb3523455ded2eafcd0ad1f01a6964efd343d5",
    "source-intake/functional_rg/5334/E0025/D4_outer_event_aligned_E0025_finite_value.csv": "7d1d4915cc78198645d287e090adf5b3f8517ac08869579403492f7b5f097183",
    "source-intake/functional_rg/5334/E0025/D4_outer_event_aligned_E0025_adaptive_panels.csv": "3918141ce686b9425a192c8813d2014f396c2fad25683f2b25c24851afc9a138",
    "source-intake/functional_rg/5334/E0025/D4_outer_event_aligned_E0025_node_manifest.csv": "097e28d68a87254e07c81a3e0e5e9e93740f641f3f814f2bce6b23325735f3c7",
    "source-intake/functional_rg/5334/E0025/D4_outer_event_aligned_E0025_dry_run.json": "03acdc72e8e1ad136b0ee6cc16886a0492504109fc40bfa59490c8123129ea7c",
    "source-intake/functional_rg/5334/E0025/D4_outer_event_aligned_E0025_validation.csv": "99409c3515aa435c9e117ae06bc538d1457aedb033dc401d9bd6be6412d7a92c",
    "source-intake/functional_rg/5334/E0025/D4_outer_event_aligned_E0025_semantic_validation.csv": "515b08c4364e122f5d634e5f75adbe80e03cac8c417dcc6bc495bd6c550e6569",
    "source-intake/functional_rg/5334/E0025/D4_outer_event_aligned_initial_plan.csv": "34ac0685dcaef29298d44b0344f7d5efe0ffde3949366d37bbab2101e259181c",
    "source-intake/functional_rg/5334/E0025/status.json": "cba9a394c6cea1712b6ac9dcd1cc10ac3d46872022c9d22e505f752c1075d872",
}

CLAIM_FIELDS = (
    "valid_for_D4_outer_E0025_fixed_decay_integral",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty CSV payload: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def no_claims() -> dict[str, bool]:
    return {field: False for field in CLAIM_FIELDS}


def validation_row(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "gate": gate,
        "passed": passed,
        "detail": detail,
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
    }


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5334 = load_module("mts_5334_for_5338", SCRIPT_5334)
M5326 = M5334.M5326
M5312 = M5334.M5312


def configure() -> None:
    M5334.configure_refinement("E0025")


def snapshot_path(relative: str) -> Path:
    return SNAPSHOT / Path(relative).name


def source_rows_and_snapshot() -> tuple[list[dict[str, Any]], bool]:
    rows: list[dict[str, Any]] = []
    passed = True
    for relative, expected in IMMUTABLE_LOCKS.items():
        path = POST / relative
        actual = digest(path) if path.is_file() else "MISSING"
        locked = actual == expected
        passed = passed and locked
        rows.append(
            {
                "source_class": "IMMUTABLE_PARENT",
                "relative_path": relative,
                "live_path": str(path),
                "snapshot_path": "NOT_APPLICABLE",
                "expected_sha256": expected,
                "actual_sha256": actual,
                "locked": locked,
                **no_claims(),
            }
        )

    if not SNAPSHOT_MANIFEST.is_file():
        for relative, expected in MUTABLE_LOCKS.items():
            path = POST / relative
            actual = digest(path) if path.is_file() else "MISSING"
            if actual != expected:
                raise RuntimeError(f"pre-depth4 source lock failed: {relative}")
        SNAPSHOT.mkdir(parents=True, exist_ok=True)
        manifest_rows: list[dict[str, Any]] = []
        for relative, expected in MUTABLE_LOCKS.items():
            source = POST / relative
            target = snapshot_path(relative)
            shutil.copy2(source, target)
            manifest_rows.append(
                {
                    "relative_path": relative,
                    "snapshot_path": str(target),
                    "sha256": digest(target),
                    "expected_sha256": expected,
                    "bytes": target.stat().st_size,
                }
            )
        write_csv(SNAPSHOT_MANIFEST, manifest_rows)

    manifest = read_csv(SNAPSHOT_MANIFEST)
    manifest_by_relative = {row["relative_path"]: row for row in manifest}
    for relative, expected in MUTABLE_LOCKS.items():
        row = manifest_by_relative.get(relative)
        path = Path(row["snapshot_path"]) if row else Path("MISSING")
        actual = digest(path) if path.is_file() else "MISSING"
        locked = bool(row) and actual == expected == row["sha256"]
        passed = passed and locked
        rows.append(
            {
                "source_class": "MUTABLE_PARENT_SNAPSHOT",
                "relative_path": relative,
                "live_path": str(POST / relative),
                "snapshot_path": str(path),
                "expected_sha256": expected,
                "actual_sha256": actual,
                "locked": locked,
                **no_claims(),
            }
        )
    write_csv(SOURCE_REGISTER, rows)
    return rows, passed


def snapshot_named(filename: str) -> Path:
    path = SNAPSHOT / filename
    if not path.is_file():
        raise FileNotFoundError(path)
    return path


def preflight_rows() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    result = read_json(snapshot_named(M5326.RESULT.name))
    finite = read_csv(snapshot_named(M5326.FINITE_VALUE.name))
    panels = read_csv(snapshot_named(M5326.ADAPTIVE_PANELS.name))
    manifest = read_csv(snapshot_named(M5326.NODE_MANIFEST.name))
    dry = read_json(snapshot_named(M5326.DRY_RUN.name))
    validation = read_csv(snapshot_named(M5326.VALIDATION.name))
    semantic = read_csv(snapshot_named(M5334.refinement_paths("E0025")["semantic_validation"].name))
    leaves = [row for row in panels if parse_bool(row["adaptive_leaf"])]
    failed = [row for row in leaves if not parse_bool(row["adaptive_gate_passes"])]
    failed_validation = {row["gate"] for row in validation if not parse_bool(row["passed"])}
    target = failed[0] if len(failed) == 1 else {}
    checks = [
        validation_row(
            "checkpoint_5337_geometry_preflight_passed",
            read_json(POST / "source-intake/functional_rg/5337/D4_regulator_fold_double_scaling_contrast_result.json").get("validation_passed") is True,
            "seven-rung fixed-topology gate",
        ),
        validation_row(
            "parent_run_is_complete_diagnostic_not_partial",
            bool(result.get("completed_full_run"))
            and int(result.get("encountered_node_count", -1)) == EXPECTED_OLD_NODE_COUNT
            and int(result.get("completed_node_count", -1)) == EXPECTED_OLD_NODE_COUNT
            and int(result.get("failed_inner_node_count", -1)) == 0,
            result.get("decision", ""),
        ),
        validation_row(
            "all_old_shards_are_complete_pass",
            len(manifest) == EXPECTED_OLD_NODE_COUNT
            and all(row["shard_state"] == "COMPLETE_PASS" for row in manifest),
            f"rows={len(manifest)}",
        ),
        validation_row(
            "exactly_one_depth3_leaf_fails",
            len(panels) == EXPECTED_OLD_PANEL_COUNT
            and len(leaves) == EXPECTED_OLD_LEAF_COUNT
            and len(failed) == 1
            and target.get("adaptive_panel_id") == TARGET_BRANCH
            and int(target.get("adaptive_depth", -1)) == OLD_MAXIMUM_DEPTH
            and target.get("failure_reason") == "MAXIMUM_ADAPTIVE_DEPTH",
            f"failed={len(failed)};target={target.get('adaptive_panel_id', 'NONE')}",
        ),
        validation_row(
            "target_failure_is_outer_only",
            bool(target)
            and parse_bool(target.get("all_inner_nodes_pass"))
            and parse_bool(target.get("exact_change_of_variables_gate_passes"))
            and float(target.get("outer_Q4_Q8_relative_change", math.inf))
            > LOCAL_OUTER_CHANGE_LIMIT,
            str(target.get("outer_Q4_Q8_relative_change", "MISSING")),
        ),
        validation_row(
            "all_other_leaves_pass",
            len(leaves) - len(failed) == EXPECTED_OLD_LEAF_COUNT - 1
            and all(
                parse_bool(row["adaptive_gate_passes"])
                for row in leaves
                if row.get("adaptive_panel_id") != TARGET_BRANCH
            ),
            f"passing={len(leaves) - len(failed)}",
        ),
        validation_row(
            "global_budget_already_passes",
            float(result.get("total_error_relative_conservative", math.inf))
            <= GLOBAL_ERROR_BUDGET_LIMIT,
            str(result.get("total_error_relative_conservative")),
        ),
        validation_row(
            "narrow_finite_claim_remains_blocked_pre_refinement",
            len(finite) == 1
            and not parse_bool(finite[0]["finite_regulator_fixed_decay_integral_accepted"])
            and not bool(result.get("acceptance_passed")),
            result.get("decision", ""),
        ),
        validation_row(
            "only_expected_parent_validation_gates_fail",
            failed_validation
            == {
                "all_D4_outer_adaptive_leaves_pass",
                "D4_outer_E0025_conservative_budget_passes",
            },
            "|".join(sorted(failed_validation)),
        ),
        validation_row(
            "semantic_validation_is_clean",
            bool(semantic) and all(parse_bool(row["passed"]) for row in semantic),
            f"rows={len(semantic)}",
        ),
        validation_row(
            "old_plan_is_depth3_contract",
            str(dry.get("node_plan_sha256"))
            == "39fd506f4652d549bb524b0751c937ab5c14a3449955292c0cbae0a66ef858b0",
            str(dry.get("node_plan_sha256")),
        ),
        validation_row(
            "formal_workbench_unchanged",
            result.get("formalization_workbench_end_digest") == FORMAL_DIGEST
            and int(result.get("formalization_workbench_modified_file_count", -1)) == 0,
            str(result.get("formalization_workbench_end_digest")),
        ),
    ]
    write_csv(PREFLIGHT, checks)
    context = {
        "result": result,
        "finite": finite,
        "panels": panels,
        "manifest": manifest,
        "dry": dry,
        "leaves": leaves,
        "target": target,
        "preflight_passed": all(parse_bool(row["passed"]) for row in checks),
    }
    return checks, context


def physical_result_signature(result: dict[str, Any]) -> str:
    payload = dict(result)
    payload.pop("node_plan_sha256", None)
    return serialized_hash(payload)


def shard_paths(node_id: str) -> dict[str, Path]:
    root = M5326.SHARDS / node_id
    return {
        "root": root,
        "result": root / "result.json",
        "poles": root / "geometric_poles.csv",
        "fits": root / "pole_residue_fits.csv",
        "classifications": root / "pole_classification.csv",
        "integrals": root / "cell_integrals.csv",
    }


def inventory_rows(old_manifest: list[dict[str, str]], old_plan: str) -> list[dict[str, Any]]:
    if OLD_INVENTORY.is_file():
        rows = read_csv(OLD_INVENTORY)
        if len(rows) != EXPECTED_OLD_NODE_COUNT:
            raise RuntimeError("stored pre-depth4 shard inventory is incomplete")
        return rows
    rows: list[dict[str, Any]] = []
    for node in old_manifest:
        paths = shard_paths(node["node_id"])
        if not all(path.is_file() for key, path in paths.items() if key != "root"):
            raise FileNotFoundError(node["node_id"])
        result = read_json(paths["result"])
        if result.get("node_plan_sha256") != old_plan:
            raise RuntimeError(f"unexpected old plan hash: {node['node_id']}")
        rows.append(
            {
                "node_id": node["node_id"],
                "x_panel_index": node["x_panel_index"],
                "absolute_soft_cosine": node["absolute_soft_cosine"],
                "mapped_outer_weight": node["mapped_outer_weight"],
                "old_node_plan_sha256": old_plan,
                "physical_result_signature": physical_result_signature(result),
                "poles_sha256": digest(paths["poles"]),
                "fits_sha256": digest(paths["fits"]),
                "classifications_sha256": digest(paths["classifications"]),
                "integrals_sha256": digest(paths["integrals"]),
                **no_claims(),
            }
        )
    write_csv(OLD_INVENTORY, rows)
    return rows


def migrate_shards(
    old_manifest: list[dict[str, str]],
    inventory: list[dict[str, Any]],
    old_plan: str,
    new_plan: str,
) -> list[dict[str, Any]]:
    inventory_by_node = {row["node_id"]: row for row in inventory}
    rows: list[dict[str, Any]] = []
    for node in old_manifest:
        node_id = node["node_id"]
        stored = inventory_by_node[node_id]
        paths = shard_paths(node_id)
        result = read_json(paths["result"])
        source_plan = str(result.get("node_plan_sha256", ""))
        coordinate_matches = math.isclose(
            float(result["absolute_soft_cosine"]),
            float(node["absolute_soft_cosine"]),
            rel_tol=0.0,
            abs_tol=2.0e-15,
        )
        weight_matches = math.isclose(
            float(result["mapped_outer_weight"]),
            float(node["mapped_outer_weight"]),
            rel_tol=0.0,
            abs_tol=2.0e-15,
        )
        signature_matches = (
            physical_result_signature(result) == stored["physical_result_signature"]
        )
        artifact_hashes_match = (
            digest(paths["poles"]) == stored["poles_sha256"]
            and digest(paths["fits"]) == stored["fits_sha256"]
            and digest(paths["classifications"]) == stored["classifications_sha256"]
            and digest(paths["integrals"]) == stored["integrals_sha256"]
        )
        reusable = (
            source_plan in {old_plan, new_plan}
            and result.get("node_revision") == M5326.NODE_REVISION
            and result.get("node_id") == node_id
            and bool(result.get("node_complete"))
            and bool(result.get("acceptance_passed"))
            and coordinate_matches
            and weight_matches
            and signature_matches
            and artifact_hashes_match
        )
        if not reusable:
            raise RuntimeError(f"shard migration gate failed: {node_id}")
        action = "ALREADY_MIGRATED_IDENTICAL_NODE"
        if source_plan == old_plan:
            result["node_plan_sha256"] = new_plan
            atomic_json(paths["result"], result)
            action = "MIGRATED_IDENTICAL_NODE_TO_DEPTH4_PLAN"
        migrated = read_json(paths["result"])
        migrated_signature_matches = (
            physical_result_signature(migrated) == stored["physical_result_signature"]
        )
        rows.append(
            {
                "node_id": node_id,
                "x_panel_index": node["x_panel_index"],
                "source_plan_sha256": source_plan,
                "depth4_plan_sha256": migrated.get("node_plan_sha256", ""),
                "coordinate_matches": coordinate_matches,
                "mapped_weight_matches": weight_matches,
                "physical_result_signature_matches": migrated_signature_matches,
                "artifact_hashes_match": artifact_hashes_match,
                "migration_action": action,
                "valid_for_reuse_in_depth4_plan": (
                    migrated.get("node_plan_sha256") == new_plan
                    and migrated_signature_matches
                    and artifact_hashes_match
                ),
                **no_claims(),
            }
        )
    write_csv(MIGRATION, rows)
    return rows


def prepare() -> dict[str, Any]:
    configure()
    source_rows, sources_locked = source_rows_and_snapshot()
    preflight, context = preflight_rows()
    if not sources_locked or not context["preflight_passed"]:
        raise RuntimeError("checkpoint 5338 preflight failed")
    old_plan = str(context["dry"]["node_plan_sha256"])
    inventory = inventory_rows(context["manifest"], old_plan)
    old_depth = int(M5326.MAXIMUM_ADAPTIVE_DEPTH)
    M5326.MAXIMUM_ADAPTIVE_DEPTH = NEW_MAXIMUM_DEPTH
    new_dry = M5334.d4_refinement_dry_run()
    new_plan = str(new_dry["node_plan_sha256"])
    initial_geometry_unchanged = (
        digest(M5326.INITIAL_PLAN)
        == MUTABLE_LOCKS[
            "source-intake/functional_rg/5334/E0025/D4_outer_event_aligned_initial_plan.csv"
        ]
    )
    migration = migrate_shards(
        context["manifest"], inventory, old_plan, new_plan
    )
    gates = [
        validation_row(
            "source_and_snapshot_locks_pass",
            sources_locked and len(source_rows) == len(IMMUTABLE_LOCKS) + len(MUTABLE_LOCKS),
            f"rows={len(source_rows)}",
        ),
        validation_row(
            "preflight_is_ruthlessly_localized",
            all(parse_bool(row["passed"]) for row in preflight),
            f"rows={len(preflight)}",
        ),
        validation_row(
            "depth_contract_changes_only_3_to_4",
            old_depth == OLD_MAXIMUM_DEPTH
            and int(M5326.MAXIMUM_ADAPTIVE_DEPTH) == NEW_MAXIMUM_DEPTH,
            f"old={old_depth};new={M5326.MAXIMUM_ADAPTIVE_DEPTH}",
        ),
        validation_row(
            "new_dry_run_passes",
            bool(new_dry.get("acceptance_passed")),
            str(new_dry.get("decision")),
        ),
        validation_row(
            "depth4_plan_hash_changes_without_geometry_change",
            old_plan != new_plan and initial_geometry_unchanged,
            f"old={old_plan};new={new_plan}",
        ),
        validation_row(
            "all_432_old_shards_migrate_by_exact_identity",
            len(migration) == EXPECTED_OLD_NODE_COUNT
            and all(parse_bool(row["valid_for_reuse_in_depth4_plan"]) for row in migration)
            and all(parse_bool(row["coordinate_matches"]) for row in migration)
            and all(parse_bool(row["mapped_weight_matches"]) for row in migration)
            and all(parse_bool(row["physical_result_signature_matches"]) for row in migration)
            and all(parse_bool(row["artifact_hashes_match"]) for row in migration),
            f"rows={len(migration)}",
        ),
        validation_row(
            "formal_workbench_unchanged",
            M5334.M5283.formal_inventory_digest() == FORMAL_DIGEST,
            FORMAL_DIGEST,
        ),
        validation_row(
            "no_claim_promoted_by_cache_migration",
            all(not any(parse_bool(row[field]) for field in CLAIM_FIELDS) for row in migration),
            "migration is numerical provenance only",
        ),
    ]
    write_csv(PREPARE_VALIDATION, gates)
    passed = all(parse_bool(row["passed"]) for row in gates)
    value = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "mode": "targeted-depth4-prepare",
        "acceptance_passed": passed,
        "decision": (
            "D4_E0025_TARGETED_DEPTH4_READY__RUN_24_NEW_NODES"
            if passed
            else "D4_E0025_TARGETED_DEPTH4_PREPARE_BLOCKED"
        ),
        "old_plan_sha256": old_plan,
        "depth4_plan_sha256": new_plan,
        "migrated_old_shard_count": len(migration),
        "target_branch": TARGET_BRANCH,
        "updated_utc": utc_now(),
    }
    atomic_json(
        STATUS,
        {
            **value,
            "state": "READY_TO_RUN" if passed else "BLOCKED",
        },
    )
    if not passed:
        raise RuntimeError("checkpoint 5338 prepare validation failed")
    return value


def stamp_parent_provenance(result: dict[str, Any]) -> dict[str, Any]:
    value = dict(result)
    sources = {
        Path(row["path"]): dict(row) for row in value.get("source_files", [])
    }
    sources[Path(__file__).resolve()] = {
        "path": str(Path(__file__).resolve()),
        "sha256": digest(Path(__file__).resolve()),
    }
    value["source_files"] = [
        sources[path] for path in sorted(sources, key=lambda item: str(item))
    ]
    value["depth4_owner_checkpoint"] = CHECKPOINT
    value["maximum_adaptive_depth"] = NEW_MAXIMUM_DEPTH
    value["targeted_depth4_parent_branch"] = TARGET_BRANCH
    value["targeted_depth4_children"] = list(TARGET_CHILDREN)
    atomic_json(M5326.RESULT, value)
    finite = read_csv(M5326.FINITE_VALUE)
    for row in finite:
        row["depth4_owner_checkpoint"] = CHECKPOINT
        row["maximum_adaptive_depth"] = NEW_MAXIMUM_DEPTH
        row["targeted_depth4_parent_branch"] = TARGET_BRANCH
    write_csv(M5326.FINITE_VALUE, finite)
    return value


def leaf_audit_rows() -> list[dict[str, Any]]:
    panels = read_csv(M5326.ADAPTIVE_PANELS)
    rows: list[dict[str, Any]] = []
    for row in panels:
        panel_id = row["adaptive_panel_id"]
        if panel_id == TARGET_BRANCH or panel_id.startswith(TARGET_BRANCH):
            rows.append(
                {
                    "adaptive_panel_id": panel_id,
                    "parent_adaptive_panel_id": row["parent_adaptive_panel_id"],
                    "adaptive_depth": row["adaptive_depth"],
                    "adaptive_leaf": row["adaptive_leaf"],
                    "lower_absolute_soft_cosine": row["lower_absolute_soft_cosine"],
                    "upper_absolute_soft_cosine": row["upper_absolute_soft_cosine"],
                    "segment_width": row["segment_width"],
                    "outer_Q4_Q8_absolute_change": row["outer_Q4_Q8_absolute_change"],
                    "outer_Q4_Q8_relative_change": row["outer_Q4_Q8_relative_change"],
                    "all_inner_nodes_pass": row["all_inner_nodes_pass"],
                    "exact_change_of_variables_gate_passes": row[
                        "exact_change_of_variables_gate_passes"
                    ],
                    "adaptive_gate_passes": row["adaptive_gate_passes"],
                    "failure_reason": row["failure_reason"],
                    **no_claims(),
                }
            )
    write_csv(LEAF_AUDIT, rows)
    return rows


def finalize() -> dict[str, Any]:
    configure()
    M5326.MAXIMUM_ADAPTIVE_DEPTH = NEW_MAXIMUM_DEPTH
    source_rows, sources_locked = source_rows_and_snapshot()
    preflight = read_csv(PREFLIGHT)
    prepare_gates = read_csv(PREPARE_VALIDATION)
    migration = read_csv(MIGRATION)
    old_manifest = read_csv(snapshot_named(M5326.NODE_MANIFEST.name))
    current_manifest = read_csv(M5326.NODE_MANIFEST)
    panels = read_csv(M5326.ADAPTIVE_PANELS)
    leaves = [row for row in panels if parse_bool(row["adaptive_leaf"])]
    depth4 = [row for row in panels if int(row["adaptive_depth"]) == NEW_MAXIMUM_DEPTH]
    audit = leaf_audit_rows()
    result = read_json(M5326.RESULT)
    finite = read_csv(M5326.FINITE_VALUE)
    parent_validation = read_csv(M5326.VALIDATION)
    old_ids = {row["node_id"] for row in old_manifest}
    new_nodes = [row for row in current_manifest if row["node_id"] not in old_ids]
    fixed_claim = "valid_for_D4_outer_E0025_fixed_decay_integral"
    broader_claims_false = (
        not bool(result["claim_boundary"]["valid_for_D4_outer_regulator_zero_limit"])
        and all(
            not bool(result["claim_boundary"].get(field, False))
            for field in M5334.CLAIM_FIELDS
        )
    )
    gates = [
        validation_row(
            "source_snapshot_and_preparation_gates_pass",
            sources_locked
            and all(parse_bool(row["passed"]) for row in preflight)
            and all(parse_bool(row["passed"]) for row in prepare_gates),
            f"sources={len(source_rows)};preflight={len(preflight)};prepare={len(prepare_gates)}",
        ),
        validation_row(
            "all_old_shards_reused_without_physical_mutation",
            len(migration) == EXPECTED_OLD_NODE_COUNT
            and all(parse_bool(row["valid_for_reuse_in_depth4_plan"]) for row in migration)
            and all(parse_bool(row["physical_result_signature_matches"]) for row in migration)
            and all(parse_bool(row["artifact_hashes_match"]) for row in migration),
            f"rows={len(migration)}",
        ),
        validation_row(
            "only_two_targeted_depth4_panels_are_created",
            {row["adaptive_panel_id"] for row in depth4} == set(TARGET_CHILDREN),
            "|".join(sorted(row["adaptive_panel_id"] for row in depth4)),
        ),
        validation_row(
            "exactly_24_target_child_nodes_are_new",
            len(new_nodes) == EXPECTED_NEW_NODE_COUNT
            and all(
                any(
                    row["node_id"].startswith(f"P12_{child}_")
                    for child in TARGET_CHILDREN
                )
                for row in new_nodes
            ),
            f"new_nodes={len(new_nodes)}",
        ),
        validation_row(
            "all_456_nodes_complete_and_pass",
            len(current_manifest) == EXPECTED_OLD_NODE_COUNT + EXPECTED_NEW_NODE_COUNT
            and all(row["shard_state"] == "COMPLETE_PASS" for row in current_manifest)
            and int(result.get("failed_inner_node_count", -1)) == 0,
            f"nodes={len(current_manifest)}",
        ),
        validation_row(
            "target_depth4_children_pass_local_gate",
            len(depth4) == 2
            and all(parse_bool(row["adaptive_leaf"]) for row in depth4)
            and all(parse_bool(row["adaptive_gate_passes"]) for row in depth4)
            and all(
                float(row["outer_Q4_Q8_relative_change"])
                <= LOCAL_OUTER_CHANGE_LIMIT
                for row in depth4
            ),
            "|".join(
                f"{row['adaptive_panel_id']}={row['outer_Q4_Q8_relative_change']}"
                for row in depth4
            ),
        ),
        validation_row(
            "all_32_adaptive_leaves_pass",
            len(panels) == EXPECTED_OLD_PANEL_COUNT + 2
            and len(leaves) == EXPECTED_OLD_LEAF_COUNT + 1
            and all(parse_bool(row["adaptive_gate_passes"]) for row in leaves)
            and bool(result.get("all_adaptive_leaf_gates_pass")),
            f"panels={len(panels)};leaves={len(leaves)}",
        ),
        validation_row(
            "global_conservative_budget_passes",
            float(result.get("total_error_relative_conservative", math.inf))
            <= GLOBAL_ERROR_BUDGET_LIMIT,
            str(result.get("total_error_relative_conservative")),
        ),
        validation_row(
            "parent_E0025_result_and_validation_accept",
            bool(result.get("acceptance_passed"))
            and bool(parent_validation)
            and all(parse_bool(row["passed"]) for row in parent_validation),
            result.get("decision", ""),
        ),
        validation_row(
            "only_narrow_finite_E0025_claim_is_promoted",
            len(finite) == 1
            and parse_bool(finite[0]["finite_regulator_fixed_decay_integral_accepted"])
            and bool(result["claim_boundary"][fixed_claim])
            and broader_claims_false,
            f"fixed={result['claim_boundary'].get(fixed_claim)};broader_false={broader_claims_false}",
        ),
        validation_row(
            "checkpoint_5338_is_in_parent_provenance",
            int(result.get("depth4_owner_checkpoint", -1)) == CHECKPOINT
            and int(result.get("maximum_adaptive_depth", -1)) == NEW_MAXIMUM_DEPTH
            and any(
                Path(row["path"]).resolve() == Path(__file__).resolve()
                and digest(Path(row["path"])) == row["sha256"]
                for row in result["source_files"]
            ),
            f"source_rows={len(result['source_files'])}",
        ),
        validation_row(
            "formal_workbench_unchanged",
            M5334.M5283.formal_inventory_digest()
            == result.get("formalization_workbench_end_digest")
            == FORMAL_DIGEST
            and int(result.get("formalization_workbench_modified_file_count", -1)) == 0,
            str(result.get("formalization_workbench_end_digest")),
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
    ]
    write_csv(VALIDATION, gates)
    passed = all(parse_bool(row["passed"]) for row in gates)
    value = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "mode": "targeted-support-exit-depth4-validation",
        "validation_passed": passed,
        "validation_rows": len(gates),
        "decision": (
            "D4_E0025_TARGETED_DEPTH4_ACCEPTED__FINITE_RUNG_VALIDATED__RUN_ADJACENT_REGULATORS"
            if passed
            else "D4_E0025_TARGETED_DEPTH4_BLOCKED__DERIVE_SUPPORT_EXIT_ASYMPTOTIC"
        ),
        "target_branch": TARGET_BRANCH,
        "target_children": list(TARGET_CHILDREN),
        "old_shard_count_reused": len(migration),
        "new_node_count": len(new_nodes),
        "adaptive_panel_count": len(panels),
        "adaptive_leaf_count": len(leaves),
        "fixed_decay_integral_real": result.get("fixed_decay_integral_real"),
        "fixed_decay_integral_imaginary": result.get("fixed_decay_integral_imaginary"),
        "fixed_decay_integral_magnitude": result.get("fixed_decay_integral_magnitude"),
        "outer_error_absolute_conservative": result.get("outer_error_absolute_conservative"),
        "inner_error_absolute_conservative": result.get("inner_error_absolute_conservative"),
        "total_error_absolute_conservative": result.get("total_error_absolute_conservative"),
        "total_error_relative_conservative": result.get("total_error_relative_conservative"),
        "depth4_leaf_rows": audit,
        "claim_boundary": {
            fixed_claim: bool(result["claim_boundary"].get(fixed_claim, False)),
            "valid_for_D4_outer_regulator_zero_limit": False,
            **{field: False for field in M5334.CLAIM_FIELDS},
        },
        "formalization_workbench_modified_file_count": result.get(
            "formalization_workbench_modified_file_count"
        ),
        "next_action": (
            ".\\.venv-score\\Scripts\\python.exe "
            ".\\scripts\\Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py "
            "--mode target-run --epsilon-id E00125 --max-runtime-hours 2"
            if passed
            else "DERIVE_P12S02_SUPPORT_EXIT_ENDPOINT_ASYMPTOTIC"
        ),
        "updated_utc": utc_now(),
    }
    atomic_json(RESULT, value)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "state": "COMPLETE" if passed else "BLOCKED",
            "decision": value["decision"],
            "validation_passed": passed,
            "updated_utc": utc_now(),
        },
    )
    return value


def run(max_runtime_hours: float) -> dict[str, Any]:
    prepared = prepare()
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "state": "RUNNING",
            "decision": "D4_E0025_TARGETED_DEPTH4_RUNNING",
            "old_shard_count_reused": prepared["migrated_old_shard_count"],
            "updated_utc": utc_now(),
        },
    )
    M5326.MAXIMUM_ADAPTIVE_DEPTH = NEW_MAXIMUM_DEPTH
    raw = M5326.execute(max(max_runtime_hours, 0.0) * 3600.0)
    canonical = M5334.canonicalize_refinement_result(raw)
    stamp_parent_provenance(canonical)
    M5334.canonicalize_saved_refinement()
    M5334.validate_refinement_outputs()
    return finalize()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("prepare", "run", "validate"), required=True)
    parser.add_argument("--max-runtime-hours", type=float, default=2.0)
    arguments = parser.parse_args()
    M5312.set_below_normal_priority()
    started = time.perf_counter()
    try:
        if arguments.mode == "prepare":
            value = prepare()
            passed = bool(value["acceptance_passed"])
        elif arguments.mode == "run":
            value = run(arguments.max_runtime_hours)
            passed = bool(value["validation_passed"])
        else:
            value = finalize()
            passed = bool(value["validation_passed"])
    except Exception as error:
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "marker": MARKER,
                "state": "FAILED",
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
                "updated_utc": utc_now(),
            },
        )
        raise
    summary = {
        "checkpoint": CHECKPOINT,
        "mode": arguments.mode,
        "acceptance_passed": passed,
        "decision": value["decision"],
        "runtime_seconds": time.perf_counter() - started,
    }
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
