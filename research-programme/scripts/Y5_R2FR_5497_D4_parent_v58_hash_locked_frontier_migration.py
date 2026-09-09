from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5497"
WORK = OUTPUT / "work-v1"

SCRIPT_5467 = SCRIPTS / "Y5_R2FR_5467_D4_all_outer_leaf_epsilon_fiber_transplant_runner.py"
SCRIPT_5469 = SCRIPTS / "Y5_R2FR_5469_D4_resumable_three_axis_cuboid_certificate_runner.py"
SCRIPT_5496 = SCRIPTS / "Y5_R2FR_5496_D4_parent_v58_adaptive_stable_edge_T2_gate.py"
SOURCE_STATE = (
    FUNCTIONAL_RG
    / "5484"
    / "work-v1"
    / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
)
CERTIFICATE_5496 = FUNCTIONAL_RG / "5496" / "D4_parent_v58_adaptive_complete_amplitude_certificate.json"
RESULT_5496 = FUNCTIONAL_RG / "5496" / "D4_parent_v58_adaptive_stable_edge_T2_result.json"
VALIDATION_5496 = FUNCTIONAL_RG / "5496" / "P8_Y5_BRR5495_5496_VALIDATION.csv"
SOURCE_REGISTER_5496 = FUNCTIONAL_RG / "5496" / "source_register.csv"
WORK_STATE_5496 = FUNCTIONAL_RG / "5496" / "work-v1" / "parent_v58_adaptive_stable_edge_T2_state.json"
COMPARISON_5496 = FUNCTIONAL_RG / "5496" / "D4_parent_v57_v58_adaptive_target_control_comparison.csv"
APPLICATION_AUDIT_5496 = FUNCTIONAL_RG / "5496" / "D4_parent_v58_adaptive_certificate_application_audit.csv"
BASE_AUDIT_5496 = FUNCTIONAL_RG / "5496" / "D4_parent_v58_adaptive_stable_edge_T2_base_audit.csv"

STATE = WORK / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
COLLAPSE_AUDIT = OUTPUT / "D4_parent_v58_frontier_collapse_audit.csv"
SUPERSESSION_AUDIT = OUTPUT / "D4_parent_v58_witness_supersession_audit.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5496_5497_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v58_hash_locked_frontier_migration_result.json"
DOCUMENT = POST / "5497-Y5-R2FR-D4-parent-v58-hash-locked-frontier-migration.md"

CHECKPOINT = 5497
REVISION = "D4-parent-v58-hash-locked-frontier-migration-v1"
PARENT_V57_REVISION = "D4-deformed-contour-regular-away-W3-v57-scoped-E16-X32-T128-certificate"
PARENT_V58_REVISION = "D4-deformed-contour-regular-away-W3-v58-adaptive-stable-edge-local-T2-union"
TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
TARGET_PATH = "R_E0S_E0S_E0S_E1S"
EXPECTED_DESCENDANT_PATHS = (
    "R_E0S_E0S_E0S_E1S_X1S",
    "R_E0S_E0S_E0S_E1S_X0S_X1S",
    "R_E0S_E0S_E0S_E1S_X0S_X0S_T1S",
    "R_E0S_E0S_E0S_E1S_X0S_X0S_T0S_X1S",
    "R_E0S_E0S_E0S_E1S_X0S_X0S_T0S_X0S",
)
EXPECTED_SOURCE_STATE_SHA256 = "3f485d18bb2a55d3fda317091e58c0330166a7b5ae7e2185a82ab46602e23faa"
EXPECTED_SCRIPT_5496_SHA256 = "8709e97da3fdd0a0d8453c6ead0299c6024ca82e3214f5e2d045b8fca6239537"
EXPECTED_WORK_STATE_5496_SHA256 = "63745c8d0ac00efc0809a77696206f2ee049b4ef35c1bd60d1e712085fb68b95"
EXPECTED_CERTIFICATE_5496_SHA256 = "27dc7fce1f83b424e9d9341778a392b83ed7c8659d12e05afd561338782fc708"
EXPECTED_RESULT_5496_SHA256 = "615ba9da7bef062fbfeb5ea0b5fe33d537715e2c46527c49416d18d4b629ed9a"
EXPECTED_VALIDATION_5496_SHA256 = "ae0ef0a2c5fba86a3b1b667a55aeefc212aad2193bd1c5528ef4a73510d954e4"
EXPECTED_SOURCE_REGISTER_5496_SHA256 = "18b614194e4a221648a94ab4fcb4385621acc306427e3792718760706df676fc"
EXPECTED_COMPARISON_5496_SHA256 = "518d1b93354607e2968721f692b90ccdac055e1b509f6c4c3a29ba30bd1c2769"
EXPECTED_APPLICATION_AUDIT_5496_SHA256 = "ca34676edd3bb92f99bdfabeca762dc1f39dd5f067bceb1bc19a46939c2ae115"
EXPECTED_BASE_AUDIT_5496_SHA256 = "ccba211f915ea5678f79126d01b5554b2d68747255f2cfd98cf568345efe6e37"
EXPECTED_SOURCE_COUNTS = (178, 8, 0)
EXPECTED_MIGRATED_COUNTS = (179, 3, 0)
EXPECTED_ACCEPTED_VOLUME = 5.96085317405059e-07
METRIC_FIELDS = (
    "integrated_regular_path_abs_upper",
    "minimum_amplitude_denominator_abs_lower",
    "relative_root_abs_lower",
    "selected_global_root_abs_lower",
    "collision_jacobian_abs_lower",
)
SUPERSESSION_FIELDS = (
    "superseded_by_checkpoint",
    "superseded_by_refinement_path",
    "superseded_reason",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def truth(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5467,
        SCRIPT_5469,
        SCRIPT_5496,
        SOURCE_STATE,
        WORK_STATE_5496,
        CERTIFICATE_5496,
        RESULT_5496,
        VALIDATION_5496,
        SOURCE_REGISTER_5496,
        COMPARISON_5496,
        APPLICATION_AUDIT_5496,
        BASE_AUDIT_5496,
    )


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def is_target_descendant(path: str) -> bool:
    return path.startswith(f"{TARGET_PATH}_")


def node_volume(base_5469: Any, row: dict[str, Any]) -> float:
    return float(base_5469.node_volume(row))


def exact_coordinate(value: Any) -> Fraction:
    return Fraction(str(value))


def exact_node_volume(row: dict[str, Any]) -> Fraction:
    volume = Fraction(1)
    for lower, upper in (
        ("epsilon_real_lower", "epsilon_real_upper"),
        ("x_lower", "x_upper"),
        ("t_lower", "t_upper"),
    ):
        volume *= exact_coordinate(row[upper]) - exact_coordinate(row[lower])
    return volume


def boxes_have_positive_interior_overlap(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return all(
        min(exact_coordinate(left[upper]), exact_coordinate(right[upper]))
        > max(exact_coordinate(left[lower]), exact_coordinate(right[lower]))
        for lower, upper in (
            ("epsilon_real_lower", "epsilon_real_upper"),
            ("x_lower", "x_upper"),
            ("t_lower", "t_upper"),
        )
    )


def exact_descendant_partition(
    base_5469: Any,
    target: dict[str, Any],
    descendants: list[dict[str, Any]],
) -> tuple[bool, float, float]:
    target_volume = node_volume(base_5469, target)
    target_volume_exact = exact_node_volume(target)
    descendant_volume_exact = sum(
        (exact_node_volume(row) for row in descendants),
        start=Fraction(0),
    )
    volume_error_exact = abs(target_volume_exact - descendant_volume_exact)
    contained = all(
        exact_coordinate(row[lower]) >= exact_coordinate(target[lower])
        and exact_coordinate(row[upper]) <= exact_coordinate(target[upper])
        for row in descendants
        for lower, upper in (
            ("epsilon_real_lower", "epsilon_real_upper"),
            ("x_lower", "x_upper"),
            ("t_lower", "t_upper"),
        )
    )
    hull_matches = all(
        min(exact_coordinate(row[lower]) for row in descendants)
        == exact_coordinate(target[lower])
        and max(exact_coordinate(row[upper]) for row in descendants)
        == exact_coordinate(target[upper])
        for lower, upper in (
            ("epsilon_real_lower", "epsilon_real_upper"),
            ("x_lower", "x_upper"),
            ("t_lower", "t_upper"),
        )
    )
    disjoint = all(
        not boxes_have_positive_interior_overlap(left, right)
        for index, left in enumerate(descendants)
        for right in descendants[index + 1 :]
    )
    exact = (
        bool(descendants)
        and contained
        and hull_matches
        and disjoint
        and volume_error_exact == 0
    )
    return exact, target_volume, float(volume_error_exact)


def strip_supersession(row: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key not in SUPERSESSION_FIELDS}


def accepted_target_row(
    target: dict[str, Any],
    certificate: dict[str, Any],
    target_comparison: dict[str, str],
) -> dict[str, Any]:
    aggregate = certificate["aggregate_result"]
    row = dict(target)
    row.update(
        {
            "probe_passed": True,
            "failure_type": "",
            "failure_message": "",
            **{field: float(aggregate[field]) for field in METRIC_FIELDS},
            "active_material_branch_count": int(
                aggregate["active_material_branch_count"]
            ),
            "active_material_branch_ids": aggregate["active_material_branch_ids"],
            "path_integral_enclosure_method": aggregate[
                "path_integral_enclosure_method"
            ],
            "runtime_seconds": 0.0,
            "certificate_source": "checkpoint_5496_parent_v58_target_certificate",
            "parent_revision": PARENT_V58_REVISION,
            "certificate_sha256": EXPECTED_CERTIFICATE_5496_SHA256,
            "certificate_target_binding_sha256": certificate[
                "target_binding_sha256"
            ],
            "certificate_final_leaf_count": int(certificate["final_leaf_count"]),
            "certificate_t2_replacement_count": int(
                certificate["t2_replacement_count"]
            ),
            "certificate_parameter_area_coverage_error": float(
                certificate["parameter_area_coverage_error"]
            ),
            "certificate_target_probe_passed": truth(
                target_comparison["probe_passed"]
            ),
        }
    )
    return row


def migrate_state(
    base_5467: Any,
    base_5469: Any,
    certificate: dict[str, Any],
    target_comparison: dict[str, str],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    source = read_json(SOURCE_STATE)
    counts = (len(source["accepted"]), len(source["stack"]), len(source["unresolved"]))
    if counts != EXPECTED_SOURCE_COUNTS:
        raise RuntimeError(f"checkpoint-5484 frontier changed: {counts}")
    if source["cuboid_job_id"] != TARGET_CUBOID_ID:
        raise RuntimeError("checkpoint-5484 source has the wrong cuboid")
    target_candidates = [
        row
        for row in source["refinement_witnesses"]
        if row.get("refinement_path") == TARGET_PATH
    ]
    if len(target_candidates) != 1:
        raise RuntimeError("checkpoint-5497 target witness is not unique")
    target = target_candidates[0]
    descendants = [
        row
        for row in source["stack"]
        if is_target_descendant(str(row.get("refinement_path", "")))
    ]
    descendant_paths = tuple(str(row["refinement_path"]) for row in descendants)
    if set(descendant_paths) != set(EXPECTED_DESCENDANT_PATHS):
        raise RuntimeError("checkpoint-5497 pending descendant set changed")
    accepted_descendants = [
        row
        for row in source["accepted"]
        if row.get("refinement_path") == TARGET_PATH
        or is_target_descendant(str(row.get("refinement_path", "")))
    ]
    unresolved_descendants = [
        row
        for row in source["unresolved"]
        if row.get("refinement_path") == TARGET_PATH
        or is_target_descendant(str(row.get("refinement_path", "")))
    ]
    exact_partition, target_volume, descendant_volume_error = exact_descendant_partition(
        base_5469,
        target,
        descendants,
    )
    if not exact_partition or accepted_descendants or unresolved_descendants:
        raise RuntimeError("checkpoint-5497 target collapse is not an exact partition")
    source_accepted_sha256 = canonical_digest(source["accepted"])
    source_stack_sha256 = canonical_digest(source["stack"])
    source_unresolved_sha256 = canonical_digest(source["unresolved"])
    source_witnesses_sha256 = canonical_digest(source["refinement_witnesses"])
    migrated = deepcopy(source)
    migrated["accepted"].append(
        accepted_target_row(target, certificate, target_comparison)
    )
    migrated["stack"] = [
        row
        for row in migrated["stack"]
        if not is_target_descendant(str(row.get("refinement_path", "")))
    ]
    supersession_rows: list[dict[str, Any]] = []
    for witness in migrated["refinement_witnesses"]:
        path = str(witness.get("refinement_path", ""))
        if path == TARGET_PATH or is_target_descendant(path):
            witness.update(
                {
                    "superseded_by_checkpoint": CHECKPOINT,
                    "superseded_by_refinement_path": TARGET_PATH,
                    "superseded_reason": (
                        "checkpoint-5496 exact parent-v58 complete-amplitude certificate"
                    ),
                }
            )
            supersession_rows.append(
                {
                    "refinement_path": path,
                    "failure_type": witness.get("failure_type", ""),
                    "failure_message": witness.get("failure_message", ""),
                    "superseded_by_checkpoint": CHECKPOINT,
                    "superseded_by_refinement_path": TARGET_PATH,
                    "superseded_reason": witness["superseded_reason"],
                }
            )
    migrated["checkpoint"] = CHECKPOINT
    migrated["revision"] = REVISION
    migrated["parent_revision"] = PARENT_V58_REVISION
    history = list(migrated.get("parent_revision_history", []))
    for revision in (PARENT_V57_REVISION, PARENT_V58_REVISION):
        if revision not in history:
            history.append(revision)
    migrated["parent_revision_history"] = history
    migrated.setdefault("external_repair_history", []).append(
        {
            "checkpoint": CHECKPOINT,
            "repair_class": "ADAPTIVE_STABLE_EDGE_LOCAL_T2_COMPLETE_AMPLITUDE_UNION",
            "target_refinement_path": TARGET_PATH,
            "removed_pending_refinement_paths": list(descendant_paths),
            "removed_pending_subcuboid_count": len(descendants),
            "accepted_coarse_target_count": 1,
            "target_volume": target_volume,
            "removed_descendant_volume_error": descendant_volume_error,
            "certificate_path": str(CERTIFICATE_5496),
            "certificate_sha256": EXPECTED_CERTIFICATE_5496_SHA256,
        }
    )
    migrated["v58_carry_forward"] = {
        "source_checkpoint": 5484,
        "source_state_path": str(SOURCE_STATE),
        "source_state_sha256": EXPECTED_SOURCE_STATE_SHA256,
        "source_accepted_sha256": source_accepted_sha256,
        "source_stack_sha256": source_stack_sha256,
        "source_unresolved_sha256": source_unresolved_sha256,
        "source_refinement_witnesses_sha256": source_witnesses_sha256,
        "certificate_path": str(CERTIFICATE_5496),
        "certificate_sha256": EXPECTED_CERTIFICATE_5496_SHA256,
        "target_refinement_path": TARGET_PATH,
        "removed_pending_refinement_paths": list(descendant_paths),
        "removed_pending_sha256": canonical_digest(descendants),
        "removed_pending_subcuboid_count": len(descendants),
        "removed_pending_volume_error": descendant_volume_error,
        "accepted_target_volume": target_volume,
        "carry_rule": (
            "replace the exact five-node pending partition by its source-locked "
            "parent-v58 coarse-target certificate; retain failures as superseded history"
        ),
        "carried_utc": datetime.now(timezone.utc).isoformat(),
    }
    migrated["v58_node_evaluation_count"] = 0
    migrated["v58_accepted_subcuboid_count"] = 1
    migrated["v58_refinement_witness_count"] = 0
    migrated["v58_certificate_application_audit_rows"] = read_csv(
        APPLICATION_AUDIT_5496
    )
    migrated["accepted_subcuboid_count"] = len(migrated["accepted"])
    migrated["pending_subcuboid_count"] = len(migrated["stack"])
    migrated["unresolved_subcuboid_count"] = len(migrated["unresolved"])
    migrated["accepted_volume"] = math.fsum(
        node_volume(base_5469, row) for row in migrated["accepted"]
    )
    migrated["coverage_error"] = abs(
        math.fsum(
            node_volume(base_5469, row)
            for row in migrated["accepted"]
            + migrated["stack"]
            + migrated["unresolved"]
        )
        - float(migrated["root_volume"])
    )
    migrated["processed_this_run"] = 0
    migrated["decision"] = "PARENT_V58_FRONTIER_PARTIAL__RESUME"
    migrated["valid_for_parent_v58_active_cuboid"] = False
    migrated["valid_for_full_outer_parent_leaf_enclosure"] = False
    migrated["valid_for_D4_event_local_W3_bound"] = False
    migrated["valid_for_all_operator_local_GR_claim"] = False
    migrated["valid_for_full_MTS_claim"] = False
    migrated["last_update_utc"] = datetime.now(timezone.utc).isoformat()
    collapse_rows = [
        {
            "row_type": "REMOVED_PENDING_DESCENDANT",
            "refinement_path": row["refinement_path"],
            "epsilon_real_lower": row["epsilon_real_lower"],
            "epsilon_real_upper": row["epsilon_real_upper"],
            "x_lower": row["x_lower"],
            "x_upper": row["x_upper"],
            "t_lower": row["t_lower"],
            "t_upper": row["t_upper"],
            "parameter_volume": node_volume(base_5469, row),
            "certificate_sha256": EXPECTED_CERTIFICATE_5496_SHA256,
        }
        for row in descendants
    ]
    collapse_rows.append(
        {
            "row_type": "ACCEPTED_CERTIFIED_TARGET",
            "refinement_path": TARGET_PATH,
            "epsilon_real_lower": target["epsilon_real_lower"],
            "epsilon_real_upper": target["epsilon_real_upper"],
            "x_lower": target["x_lower"],
            "x_upper": target["x_upper"],
            "t_lower": target["t_lower"],
            "t_upper": target["t_upper"],
            "parameter_volume": target_volume,
            "certificate_sha256": EXPECTED_CERTIFICATE_5496_SHA256,
        }
    )
    base_5467.atomic_json(STATE, migrated, compact=True)
    return migrated, collapse_rows, supersession_rows


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5497: D4 parent-v58 hash-locked frontier migration",
        "",
        "Checkpoint 5496 certifies the coarse target `R_E0S_E0S_E0S_E1S`. Its five pending descendants are interior-disjoint, contained in that target and have exactly equal total volume. No accepted or unresolved target descendant exists. This status-only migration replaces that pending partition by one accepted parent-v58 certificate while retaining all old failures as superseded history.",
        "",
        f"Source frontier: `{payload['source_accepted_count']}/{payload['source_pending_count']}/{payload['source_unresolved_count']}`. Migrated frontier: `{payload['accepted_subcuboid_count']}/{payload['pending_subcuboid_count']}/{payload['unresolved_subcuboid_count']}`.",
        "",
        f"Removed pending descendants: `{payload['removed_pending_descendant_count']}`. Target-partition volume error: `{payload['target_partition_volume_error']}`. Full frontier partition error: `{payload['partition_volume_error']}`.",
        "",
        f"**{payload['decision']}**",
        "",
        "No new numerical node is evaluated here. Parent-v58 active-cuboid, full outer, event-local/combined W3, regulator-limit, all-operator local GR and full MTS claims remain false.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    base_5467 = load_module("mts_5467_for_5497", SCRIPT_5467)
    base_5469 = load_module("mts_5469_for_5497", SCRIPT_5469)
    base_5467.set_below_normal_priority()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    inherited_hashes = {
        "source_state": digest(SOURCE_STATE),
        "script_5496": digest(SCRIPT_5496),
        "work_state_5496": digest(WORK_STATE_5496),
        "certificate_5496": digest(CERTIFICATE_5496),
        "result_5496": digest(RESULT_5496),
        "validation_5496": digest(VALIDATION_5496),
        "source_register_5496": digest(SOURCE_REGISTER_5496),
        "comparison_5496": digest(COMPARISON_5496),
        "application_audit_5496": digest(APPLICATION_AUDIT_5496),
        "base_audit_5496": digest(BASE_AUDIT_5496),
    }
    expected_hashes = {
        "source_state": EXPECTED_SOURCE_STATE_SHA256,
        "script_5496": EXPECTED_SCRIPT_5496_SHA256,
        "work_state_5496": EXPECTED_WORK_STATE_5496_SHA256,
        "certificate_5496": EXPECTED_CERTIFICATE_5496_SHA256,
        "result_5496": EXPECTED_RESULT_5496_SHA256,
        "validation_5496": EXPECTED_VALIDATION_5496_SHA256,
        "source_register_5496": EXPECTED_SOURCE_REGISTER_5496_SHA256,
        "comparison_5496": EXPECTED_COMPARISON_5496_SHA256,
        "application_audit_5496": EXPECTED_APPLICATION_AUDIT_5496_SHA256,
        "base_audit_5496": EXPECTED_BASE_AUDIT_5496_SHA256,
    }
    if inherited_hashes != expected_hashes:
        raise RuntimeError("checkpoint-5497 inherited source hash mismatch")
    source = read_json(SOURCE_STATE)
    certificate = read_json(CERTIFICATE_5496)
    result_5496 = read_json(RESULT_5496)
    validation_5496 = read_csv(VALIDATION_5496)
    source_register_5496 = read_csv(SOURCE_REGISTER_5496)
    comparison_5496 = read_csv(COMPARISON_5496)
    target_comparison = next(
        row for row in comparison_5496 if row.get("role") == "target_v58"
    )
    source_register_current = bool(source_register_5496) and all(
        truth(row.get("exists"))
        and Path(row["source_path"]).is_file()
        and digest(Path(row["source_path"])) == row["sha256"]
        for row in source_register_5496
    )
    certificate_valid = (
        truth(result_5496.get("valid_for_parent_v58_adaptive_stable_edge_T2"))
        and int(result_5496.get("failed_validation_count", -1)) == 0
        and all(truth(row.get("passed")) for row in validation_5496)
        and source_register_current
        and truth(target_comparison.get("probe_passed"))
        and int(certificate.get("base_cell_count", -1)) == 256
        and int(certificate.get("final_leaf_count", -1)) == 259
        and int(certificate.get("t2_replacement_count", -1)) == 3
        and float(certificate.get("parameter_area_coverage_error", math.nan)) == 0.0
    )
    if not certificate_valid:
        raise RuntimeError("checkpoint-5496 parent-v58 certificate is not valid")
    source_target = next(
        row
        for row in source["refinement_witnesses"]
        if row.get("refinement_path") == TARGET_PATH
    )
    source_descendants = [
        row
        for row in source["stack"]
        if is_target_descendant(str(row.get("refinement_path", "")))
    ]
    source_partition_exact, source_target_volume, source_partition_error = (
        exact_descendant_partition(base_5469, source_target, source_descendants)
    )
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint": CHECKPOINT,
                    "dry_run": True,
                    "source_counts": [
                        len(source["accepted"]),
                        len(source["stack"]),
                        len(source["unresolved"]),
                    ],
                    "removed_descendant_paths": [
                        row["refinement_path"] for row in source_descendants
                    ],
                    "target_volume": source_target_volume,
                    "target_partition_volume_error": source_partition_error,
                    "target_partition_exact": source_partition_exact,
                    "expected_migrated_counts": list(EXPECTED_MIGRATED_COUNTS),
                },
                indent=2,
            )
        )
        return 0
    if STATE.is_file():
        state = read_json(STATE)
        collapse_rows = read_csv(COLLAPSE_AUDIT)
        supersession_rows = read_csv(SUPERSESSION_AUDIT)
    else:
        WORK.mkdir(parents=True, exist_ok=True)
        state, collapse_rows, supersession_rows = migrate_state(
            base_5467,
            base_5469,
            certificate,
            target_comparison,
        )
    counts = (len(state["accepted"]), len(state["stack"]), len(state["unresolved"]))
    partition_total = math.fsum(
        node_volume(base_5469, row)
        for row in state["accepted"] + state["stack"] + state["unresolved"]
    )
    partition_error = abs(partition_total - float(state["root_volume"]))
    source_unrelated_stack = [
        row
        for row in source["stack"]
        if not is_target_descendant(str(row.get("refinement_path", "")))
    ]
    witnesses_preserved = [
        strip_supersession(row) for row in state["refinement_witnesses"]
    ] == source["refinement_witnesses"]
    unrelated_ledgers_preserved = (
        state["accepted"][:-1] == source["accepted"]
        and state["stack"] == source_unrelated_stack
        and state["unresolved"] == source["unresolved"]
        and witnesses_preserved
    )
    target_accepted = [
        row for row in state["accepted"] if row.get("refinement_path") == TARGET_PATH
    ]
    accepted_target_matches = (
        len(target_accepted) == 1
        and truth(target_accepted[0].get("probe_passed"))
        and all(
            float(target_accepted[0][field])
            == float(certificate["aggregate_result"][field])
            for field in METRIC_FIELDS
        )
    )
    source_expected_accepted_volume_exact = sum(
        (exact_node_volume(row) for row in source["accepted"]),
        start=exact_node_volume(source_target),
    )
    migrated_accepted_volume_exact = sum(
        (exact_node_volume(row) for row in state["accepted"]),
        start=Fraction(0),
    )
    accepted_volume_matches_derived_value = (
        migrated_accepted_volume_exact == source_expected_accepted_volume_exact
        and math.isclose(
            float(state["accepted_volume"]),
            EXPECTED_ACCEPTED_VOLUME,
            rel_tol=0.0,
            abs_tol=8.0 * math.ulp(EXPECTED_ACCEPTED_VOLUME),
        )
    )
    after_formalization = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check("source_state_and_parent_v58_evidence_are_hash_locked", inherited_hashes == expected_hashes, inherited_hashes),
        check("checkpoint_5496_parent_v58_target_is_certified", certificate_valid, result_5496.get("decision")),
        check("source_frontier_has_expected_counts", (len(source["accepted"]), len(source["stack"]), len(source["unresolved"])) == EXPECTED_SOURCE_COUNTS, EXPECTED_SOURCE_COUNTS),
        check("five_pending_descendants_are_the_exact_target_partition", source_partition_exact and set(row["refinement_path"] for row in source_descendants) == set(EXPECTED_DESCENDANT_PATHS), source_partition_error),
        check("target_has_no_accepted_or_unresolved_descendant", not any(row.get("refinement_path") == TARGET_PATH or is_target_descendant(str(row.get("refinement_path", ""))) for row in source["accepted"] + source["unresolved"]), TARGET_PATH),
        check("certified_target_is_added_once_with_exact_metrics", accepted_target_matches, len(target_accepted)),
        check("unrelated_partition_and_witness_history_are_preserved", unrelated_ledgers_preserved, "accepted-prefix/stack/unresolved/witnesses"),
        check("old_failures_are_retained_as_superseded_history", len(supersession_rows) == 4 and all(str(row.get("superseded_by_checkpoint")) == str(CHECKPOINT) for row in supersession_rows), len(supersession_rows)),
        check("migrated_frontier_has_expected_counts", counts == EXPECTED_MIGRATED_COUNTS, counts),
        check(
            "accepted_volume_matches_derived_value",
            accepted_volume_matches_derived_value,
            (
                f"exact_rational={migrated_accepted_volume_exact == source_expected_accepted_volume_exact};"
                f"stored={state['accepted_volume']};reference={EXPECTED_ACCEPTED_VOLUME}"
            ),
        ),
        check("migrated_partition_preserves_root_volume", partition_error == 0.0, partition_error),
        check("status_only_migration_performs_no_new_node_evaluation", int(state["node_evaluation_count"]) == int(source["node_evaluation_count"]) and int(state["v58_node_evaluation_count"]) == 0, state["node_evaluation_count"]),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", not state["valid_for_parent_v58_active_cuboid"] and not state["valid_for_full_outer_parent_leaf_enclosure"] and not state["valid_for_D4_event_local_W3_bound"] and not state["valid_for_all_operator_local_GR_claim"] and not state["valid_for_full_MTS_claim"], "status-only one-target migration"),
    ]
    failed_validations = [row for row in validations if not row["passed"]]
    decision = (
        "PARENT_V58_STATUS_ONLY_MIGRATION_CERTIFIED__RUN_ONE_FRONTIER_NODE"
        if not failed_validations
        else "PARENT_V58_STATUS_ONLY_MIGRATION_NOT_CERTIFIED"
    )
    state["decision"] = "PARENT_V58_FRONTIER_PARTIAL__RESUME"
    base_5467.atomic_json(STATE, state, compact=True)
    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_V58_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "target_cuboid_id": TARGET_CUBOID_ID,
        "target_refinement_path": TARGET_PATH,
        "source_accepted_count": EXPECTED_SOURCE_COUNTS[0],
        "source_pending_count": EXPECTED_SOURCE_COUNTS[1],
        "source_unresolved_count": EXPECTED_SOURCE_COUNTS[2],
        "accepted_subcuboid_count": counts[0],
        "pending_subcuboid_count": counts[1],
        "unresolved_subcuboid_count": counts[2],
        "removed_pending_descendant_count": len(source_descendants),
        "retained_superseded_witness_count": len(supersession_rows),
        "target_partition_volume": source_target_volume,
        "target_partition_volume_error": source_partition_error,
        "accepted_volume": state["accepted_volume"],
        "partition_volume_error": partition_error,
        "node_evaluation_count": state["node_evaluation_count"],
        "v58_node_evaluation_count": state["v58_node_evaluation_count"],
        "source_state_sha256": EXPECTED_SOURCE_STATE_SHA256,
        "certificate_5496_sha256": EXPECTED_CERTIFICATE_5496_SHA256,
        "validation_row_count": len(validations),
        "failed_validation_count": len(failed_validations),
        "valid_for_parent_v58_status_only_migration": not failed_validations,
        "valid_for_parent_v58_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "RUN_ONE_ATOMIC_PARENT_V58_FRONTIER_NODE",
    }
    base_5467.atomic_csv(COLLAPSE_AUDIT, collapse_rows)
    base_5467.atomic_csv(SUPERSESSION_AUDIT, supersession_rows)
    base_5467.atomic_csv(
        SOURCE_REGISTER,
        [
            {
                "source_path": str(path),
                "sha256": digest(path),
                "exists": path.is_file(),
            }
            for path in source_paths()
        ],
    )
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, base_5467)
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "decision",
                    "accepted_subcuboid_count",
                    "pending_subcuboid_count",
                    "unresolved_subcuboid_count",
                    "removed_pending_descendant_count",
                    "retained_superseded_witness_count",
                    "target_partition_volume_error",
                    "accepted_volume",
                    "partition_volume_error",
                    "v58_node_evaluation_count",
                    "failed_validation_count",
                    "next_target",
                )
            },
            indent=2,
        )
    )
    return 0 if not failed_validations else 1


if __name__ == "__main__":
    raise SystemExit(main())
