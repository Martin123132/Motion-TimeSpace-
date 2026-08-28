from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sys
from typing import Any


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
PRIMARY_PATH = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
INPUT_5396 = FUNCTIONAL_RG / "5396"
LIVE_PARTS = INPUT_5396 / "partial" / "path_parts"
MANIFEST = INPUT_5396 / "run_manifest.json"
INPUT_5398 = FUNCTIONAL_RG / "5398"
STAGED_PARTS = INPUT_5398 / "staged_path_parts"
BACKFILL_RESULT = INPUT_5398 / "completed_path_chart_union_backfill_result.json"
BACKFILL_SUMMARY = INPUT_5398 / "completed_path_chart_union_backfill_summary.csv"
OUTPUT = FUNCTIONAL_RG / "5399"
ARCHIVE = OUTPUT / "archive_v39_path_parts"
MIGRATION_ROWS = OUTPUT / "atomic_selector_certificate_migration.csv"
RESULT_PATH = OUTPUT / "atomic_selector_certificate_migration_result.json"
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5399_VALIDATION.csv"
)

CHECKPOINT = 5399
REVISION = "D4-atomic-selector-certificate-migration-v1"
PRIMARY_REVISION = "D4-deformed-contour-regular-away-W3-v40"


def load_primary() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_5399_primary", PRIMARY_PATH
    )
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {PRIMARY_PATH}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[specification.name] = module
    specification.loader.exec_module(module)
    return module


def relative_path(path: Path) -> str:
    return str(path.relative_to(POST)).replace("\\", "/")


def as_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def validation_row(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def inputs(primary: Any) -> tuple[dict[str, Any], list[dict[str, str]]]:
    result = primary.read_json(BACKFILL_RESULT)
    summary = primary.read_csv(BACKFILL_SUMMARY)
    if not result["valid_for_staged_atlas_migration"]:
        raise RuntimeError("5398 does not authorize staged atlas migration")
    if not summary or not all(as_bool(row["staged_complete"]) for row in summary):
        raise RuntimeError("5398 staged path set is incomplete")
    if primary.REVISION != PRIMARY_REVISION:
        raise RuntimeError(
            f"primary revision is {primary.REVISION}, expected {PRIMARY_REVISION}"
        )
    return result, summary


def source_register(
    primary: Any, summary: list[dict[str, str]]
) -> list[dict[str, Any]]:
    paths = [
        Path(__file__).resolve(),
        PRIMARY_PATH,
        BACKFILL_RESULT,
        BACKFILL_SUMMARY,
        MANIFEST,
        *[STAGED_PARTS / row["source_filename"] for row in summary],
    ]
    return [
        {
            "path": relative_path(path),
            "sha256": primary.digest(path),
            "source_exists": path.is_file(),
        }
        for path in paths
    ]


def preflight_rows(
    primary: Any, summary: list[dict[str, str]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in summary:
        filename = source["source_filename"]
        live = LIVE_PARTS / filename
        staged = STAGED_PARTS / filename
        archive = ARCHIVE / filename
        source_hash = source["source_sha256"]
        staged_hash = primary.digest(staged)
        live_hash = primary.digest(live)
        archive_hash = primary.digest(archive) if archive.is_file() else ""
        rows.append(
            {
                "source_filename": filename,
                "live_path": relative_path(live),
                "staged_path": relative_path(staged),
                "archive_path": relative_path(archive),
                "source_v39_sha256": source_hash,
                "staged_sha256": staged_hash,
                "live_sha256_before": live_hash,
                "archive_sha256_before": archive_hash,
                "live_is_original_or_already_staged": live_hash
                in {source_hash, staged_hash},
                "archive_is_absent_or_original": (
                    not archive_hash or archive_hash == source_hash
                ),
                "staged_row_count": int(source["staged_row_count"]),
                "closed_selector_margin_row_count": int(
                    source["closed_selector_margin_row_count"]
                ),
                "valid_for_claim": False,
            }
        )
    return rows


def dry_run(primary: Any) -> dict[str, Any]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    result, summary = inputs(primary)
    sources = source_register(primary, summary)
    preflight = preflight_rows(primary, summary)
    primary.atomic_csv(OUTPUT / "source_register.csv", sources)
    primary.atomic_csv(OUTPUT / "migration_preflight.csv", preflight)
    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "mode": "strict_dry_run",
        "primary_revision": primary.REVISION,
        "path_count": len(preflight),
        "staged_row_count": sum(row["staged_row_count"] for row in preflight),
        "closed_selector_margin_row_count": sum(
            row["closed_selector_margin_row_count"] for row in preflight
        ),
        "all_sources_exist_and_are_hashed": all(
            row["source_exists"] and row["sha256"] for row in sources
        ),
        "all_live_inputs_are_original_or_already_staged": all(
            row["live_is_original_or_already_staged"] for row in preflight
        ),
        "all_archives_are_absent_or_original": all(
            row["archive_is_absent_or_original"] for row in preflight
        ),
        "5398_staged_migration_gate": result[
            "valid_for_staged_atlas_migration"
        ],
        "writes_live_files": False,
        "valid_for_live_atlas_migration": False,
    }
    primary.atomic_json(OUTPUT / "dry_run_result.json", payload)
    return payload


def migrate(primary: Any) -> dict[str, Any]:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    _, summary = inputs(primary)
    sources = source_register(primary, summary)
    preflight = preflight_rows(primary, summary)
    if not all(
        row["live_is_original_or_already_staged"]
        and row["archive_is_absent_or_original"]
        for row in preflight
    ):
        raise RuntimeError("migration preflight rejected a live or archive hash")
    manifest_before = primary.read_json(MANIFEST)
    manifest_archive = OUTPUT / "run_manifest_v39.json"
    if manifest_archive.is_file():
        if primary.read_json(manifest_archive) != manifest_before and (
            manifest_before.get("revision") != PRIMARY_REVISION
        ):
            raise RuntimeError("manifest archive conflicts with live manifest")
    elif manifest_before.get("revision") != PRIMARY_REVISION:
        primary.atomic_json(manifest_archive, manifest_before)
    temporary_paths: list[tuple[Path, Path, str]] = []
    migration_rows: list[dict[str, Any]] = []
    for row in preflight:
        filename = row["source_filename"]
        live = LIVE_PARTS / filename
        staged = STAGED_PARTS / filename
        archive = ARCHIVE / filename
        source_hash = row["source_v39_sha256"]
        staged_hash = row["staged_sha256"]
        live_hash = primary.digest(live)
        if not archive.is_file():
            if live_hash != source_hash:
                raise RuntimeError(
                    f"cannot create original archive from migrated live file: {filename}"
                )
            shutil.copy2(live, archive)
        if primary.digest(archive) != source_hash:
            raise RuntimeError(f"archive hash mismatch: {filename}")
        if live_hash != staged_hash:
            temporary = live.with_suffix(live.suffix + ".5399.tmp")
            shutil.copy2(staged, temporary)
            if primary.digest(temporary) != staged_hash:
                raise RuntimeError(f"temporary staged hash mismatch: {filename}")
            temporary_paths.append((temporary, live, staged_hash))
        migration_rows.append(
            {
                **row,
                "archive_sha256_after": primary.digest(archive),
                "staged_temporary_prepared": live_hash != staged_hash,
            }
        )
    for temporary, live, staged_hash in temporary_paths:
        os.replace(temporary, live)
        if primary.digest(live) != staged_hash:
            raise RuntimeError(f"post-replace live hash mismatch: {live.name}")
    manifest_after = dict(manifest_before)
    manifest_after["revision"] = PRIMARY_REVISION
    manifest_after["selector_certificate_migration_checkpoint"] = CHECKPOINT
    manifest_after["selector_certificate_migration_revision"] = REVISION
    primary.atomic_json(MANIFEST, manifest_after)
    for row in migration_rows:
        live = LIVE_PARTS / row["source_filename"]
        row["live_sha256_after"] = primary.digest(live)
        row["live_matches_staged_after"] = (
            row["live_sha256_after"] == row["staged_sha256"]
        )
        row["archive_matches_source_after"] = (
            row["archive_sha256_after"] == row["source_v39_sha256"]
        )
        row["valid_for_atomic_selector_certificate_migration"] = (
            row["live_matches_staged_after"]
            and row["archive_matches_source_after"]
        )
    primary.atomic_csv(MIGRATION_ROWS, migration_rows)
    all_live_staged = all(row["live_matches_staged_after"] for row in migration_rows)
    all_archived = all(row["archive_matches_source_after"] for row in migration_rows)
    claims_locked = True
    for row in migration_rows:
        for certificate in primary.read_csv(LIVE_PARTS / row["source_filename"]):
            claims_locked = claims_locked and as_bool(
                certificate[primary.CLAIM_DEFORMATION]
            )
            claims_locked = claims_locked and as_bool(certificate[primary.CLAIM_AWAY])
            claims_locked = claims_locked and all(
                not as_bool(certificate[claim]) for claim in primary.OPEN_CLAIMS
            )
    validations = [
        validation_row(
            "all_sources_exist_and_are_hashed",
            all(row["source_exists"] and row["sha256"] for row in sources),
            len(sources),
        ),
        validation_row(
            "all_original_v39_path_files_are_archived",
            all_archived,
            len(migration_rows),
        ),
        validation_row(
            "all_live_path_files_match_the_5398_staged_certificates",
            all_live_staged,
            len(migration_rows),
        ),
        validation_row(
            "primary_and_manifest_use_v40_selector_logic",
            primary.REVISION == PRIMARY_REVISION
            and primary.read_json(MANIFEST)["revision"] == PRIMARY_REVISION,
            PRIMARY_REVISION,
        ),
        validation_row(
            "all_downstream_claims_remain_locked",
            claims_locked,
            "regular-away finite-box claims only",
        ),
    ]
    primary.atomic_csv(VALIDATION, validations)
    valid = all(row["passed"] for row in validations)
    payload = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": 5398,
        "revision": REVISION,
        "primary_revision": primary.REVISION,
        "migrated_path_count": len(migration_rows),
        "migrated_row_count": sum(
            int(row["staged_row_count"]) for row in migration_rows
        ),
        "closed_selector_margin_row_count": sum(
            int(row["closed_selector_margin_row_count"])
            for row in migration_rows
        ),
        "all_original_v39_paths_archived": all_archived,
        "all_live_paths_match_staged_certificates": all_live_staged,
        "all_downstream_claims_remain_locked": claims_locked,
        "valid_for_live_atlas_migration": valid,
        "valid_for_resuming_v40_regular_away_production": valid,
        "claim_boundary": (
            "The migration repairs selector ownership for the 15 completed "
            "paths and enables v40 production. It does not promote the open "
            "event-local, full-W3, regulator-limit, UV, local-GR, or MTS claims."
        ),
    }
    primary.atomic_csv(OUTPUT / "source_register.csv", sources)
    primary.atomic_json(RESULT_PATH, payload)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    primary = load_primary()
    primary.set_below_normal_priority()
    payload = dry_run(primary) if arguments.dry_run else migrate(primary)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
