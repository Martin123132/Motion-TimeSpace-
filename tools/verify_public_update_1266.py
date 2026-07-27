from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CHECKPOINTS = ROOT / "research-programme" / "checkpoints"
SCRIPTS = ROOT / "research-programme" / "scripts"
RESIDUALS = ROOT / "research-programme" / "source-intake" / "mts_residuals"
CATALOGUE = ROOT / "research-programme" / "catalogue"
INVENTORY = ROOT / "docs" / "status" / "PUBLICATION-INVENTORY-2026-07-27.csv"
PUBLIC_START = 1192
PUBLIC_END = 1266
PRIVATE_OFFSET = 3984
PRIVATE_START = PUBLIC_START + PRIVATE_OFFSET
PRIVATE_END = PUBLIC_END + PRIVATE_OFFSET
EXPECTED_SCRIPT_COUNT = 77
EXPECTED_RESIDUAL_COUNT = 74
INTENTIONAL_MISSING_VALIDATION_IDS = {5243}
EXPECTED_NONPASS_VALIDATION_IDS = {5216, 5221, 5240, 5241, 5244}


def checkpoint_id(path: Path) -> int | None:
    match = re.match(r"^(\d+)", path.name)
    return int(match.group(1)) if match else None


def contains_private_id(path: Path) -> bool:
    return any(
        PRIVATE_START <= int(match.group(1)) <= PRIVATE_END
        for match in re.finditer(r"(?<!\d)(\d{4})(?!\d)", path.name)
    )


def record(
    checks: list[dict[str, Any]], check_id: str, passed: bool, evidence: Any
) -> None:
    checks.append(
        {"check_id": check_id, "passed": bool(passed), "evidence": evidence}
    )


def validation_rows_pass(path: Path) -> tuple[bool, int]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return False, 0
    if "passed" in rows[0]:
        return all(row["passed"].strip().lower() == "true" for row in rows), len(
            rows
        )
    if "status" in rows[0]:
        accepted = {"pass", "passed"}
        return all(row["status"].strip().lower() in accepted for row in rows), len(
            rows
        )
    return False, len(rows)


def index_entries() -> list[tuple[str, str]]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-s", "-z"],
        capture_output=True,
        check=True,
    )
    inventory_path = INVENTORY.relative_to(ROOT).as_posix()
    entries: list[tuple[str, str]] = []
    for raw_record in result.stdout.split(b"\0"):
        if not raw_record:
            continue
        header, raw_path = raw_record.split(b"\t", maxsplit=1)
        _, object_id, stage = header.decode("ascii").split()
        path = raw_path.decode("utf-8", errors="surrogateescape")
        if stage == "0" and path != inventory_path:
            entries.append((path, object_id))
    return sorted(entries, key=lambda entry: entry[0])


def index_blob_contents(entries: list[tuple[str, str]]) -> list[bytes]:
    object_input = "".join(f"{object_id}\n" for _, object_id in entries).encode(
        "ascii"
    )
    result = subprocess.run(
        ["git", "-C", str(ROOT), "cat-file", "--batch"],
        input=object_input,
        capture_output=True,
        check=True,
    )
    output = result.stdout
    offset = 0
    blobs: list[bytes] = []
    for _, expected_object_id in entries:
        header_end = output.find(b"\n", offset)
        if header_end < 0:
            raise RuntimeError("Incomplete git cat-file batch header")
        header = output[offset:header_end].decode("ascii")
        object_id, object_type, size_text = header.split()
        if object_id != expected_object_id or object_type != "blob":
            raise RuntimeError(f"Unexpected git object header: {header}")
        size = int(size_text)
        content_start = header_end + 1
        content_end = content_start + size
        content = output[content_start:content_end]
        if output[content_end : content_end + 1] != b"\n":
            raise RuntimeError(f"Malformed git cat-file payload for {object_id}")
        blobs.append(content)
        offset = content_end + 1
    return blobs


def verify_inventory() -> dict[str, Any]:
    with INVENTORY.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    entries = index_entries()
    blobs = index_blob_contents(entries)
    indexed = {
        path: {
            "size_bytes": len(content),
            "sha256": hashlib.sha256(content).hexdigest(),
        }
        for (path, _), content in zip(entries, blobs, strict=True)
    }
    expected_paths = set(indexed)
    inventory_paths = {row["path"] for row in rows}
    failures: list[str] = []
    for row in rows:
        indexed_row = indexed.get(row["path"])
        if indexed_row is None:
            failures.append(f"missing-index-entry:{row['path']}")
            continue
        if indexed_row["size_bytes"] != int(row["size_bytes"]):
            failures.append(f"size:{row['path']}")
            continue
        if indexed_row["sha256"] != row["sha256"]:
            failures.append(f"sha256:{row['path']}")
    return {
        "passed": expected_paths == inventory_paths and not failures,
        "row_count": len(rows),
        "missing_from_inventory": sorted(expected_paths - inventory_paths),
        "extra_in_inventory": sorted(inventory_paths - expected_paths),
        "hash_or_size_failures": failures,
    }


def main() -> None:
    checks: list[dict[str, Any]] = []
    checkpoint_files = sorted(
        (
            path
            for path in CHECKPOINTS.glob("*.md")
            if (identifier := checkpoint_id(path)) is not None
            and PUBLIC_START <= identifier <= PUBLIC_END
        ),
        key=lambda path: checkpoint_id(path) or -1,
    )
    public_ids = [checkpoint_id(path) for path in checkpoint_files]
    record(
        checks,
        "public_checkpoint_range_is_contiguous",
        public_ids == list(range(PUBLIC_START, PUBLIC_END + 1)),
        public_ids,
    )

    heading_mismatches: list[str] = []
    for path in checkpoint_files:
        first_line = path.read_text(encoding="utf-8").splitlines()[0]
        match = re.match(r"^#\s+(\d+)", first_line)
        expected = (checkpoint_id(path) or 0) + PRIVATE_OFFSET
        if match is None or int(match.group(1)) != expected:
            heading_mismatches.append(path.name)
    record(
        checks,
        "public_private_checkpoint_mapping",
        not heading_mismatches,
        heading_mismatches,
    )

    script_files = sorted(
        path for path in SCRIPTS.glob("*.py") if contains_private_id(path)
    )
    compile_failures: list[str] = []
    for path in script_files:
        try:
            compile(path.read_text(encoding="utf-8"), str(path), "exec")
        except Exception as error:
            compile_failures.append(f"{path.name}: {error}")
    record(
        checks,
        "published_scripts_compile",
        len(script_files) == EXPECTED_SCRIPT_COUNT and not compile_failures,
        {"count": len(script_files), "failures": compile_failures},
    )

    residual_files = sorted(
        path
        for path in RESIDUALS.iterdir()
        if path.is_file()
        and path.suffix.lower() in {".csv", ".json"}
        and contains_private_id(path)
    )
    parse_failures: list[str] = []
    validation_failures: list[str] = []
    nonpass_validation_ids: set[int] = set()
    unsafe_failed_claim_rows: list[str] = []
    validation_row_count = 0
    validation_ids: set[int] = set()
    for path in residual_files:
        try:
            if path.suffix.lower() == ".json":
                json.loads(path.read_text(encoding="utf-8"))
            else:
                passed, row_count = validation_rows_pass(path)
                validation_row_count += row_count
                file_private_ids: set[int] = set()
                for match in re.finditer(r"(?<!\d)(\d{4})(?!\d)", path.name):
                    identifier = int(match.group(1))
                    if PRIVATE_START <= identifier <= PRIVATE_END:
                        validation_ids.add(identifier)
                        file_private_ids.add(identifier)
                if not passed:
                    nonpass_validation_ids.update(file_private_ids)
                    if not file_private_ids.intersection(
                        EXPECTED_NONPASS_VALIDATION_IDS
                    ):
                        validation_failures.append(path.name)
                    with path.open(encoding="utf-8", newline="") as handle:
                        rows = list(csv.DictReader(handle))
                    for row in rows:
                        if row.get("passed", "").strip().lower() != "false":
                            continue
                        claim_fields = [
                            value
                            for key, value in row.items()
                            if key.startswith("valid_for_") and key.endswith("_claim")
                        ]
                        if any(value.strip().lower() != "false" for value in claim_fields):
                            unsafe_failed_claim_rows.append(path.name)
        except Exception as error:
            parse_failures.append(f"{path.name}: {error}")
    missing_validation_ids = (
        set(range(PRIVATE_START, PRIVATE_END + 1)) - validation_ids
    )
    record(
        checks,
        "compact_residuals_parse_and_pass",
        len(residual_files) == EXPECTED_RESIDUAL_COUNT
        and not parse_failures
        and not validation_failures
        and nonpass_validation_ids == EXPECTED_NONPASS_VALIDATION_IDS
        and not unsafe_failed_claim_rows
        and missing_validation_ids == INTENTIONAL_MISSING_VALIDATION_IDS,
        {
            "count": len(residual_files),
            "validation_rows": validation_row_count,
            "parse_failures": parse_failures,
            "validation_failures": validation_failures,
            "expected_nonpass_validation_ids": sorted(nonpass_validation_ids),
            "unsafe_failed_claim_rows": unsafe_failed_claim_rows,
            "intentional_missing_validation_ids": sorted(missing_validation_ids),
        },
    )

    checkpoint_1259 = (
        CHECKPOINTS
        / "1259-Y5-R2FR-adaptive-homotopy-winding-rebuild-and-Q03-Q05-slice-rerun.md"
    )
    checkpoint_1259_text = checkpoint_1259.read_text(encoding="utf-8")
    record(
        checks,
        "stopped_5243_run_is_explicitly_nonclaim",
        "stopped before integration" in checkpoint_1259_text
        and "No corrected Q03/Q05 integral" in checkpoint_1259_text,
        "checkpoint 1259 documents the intentional absent compact validation row",
    )

    selected_files = checkpoint_files + script_files + residual_files
    oversized = [
        {"path": str(path.relative_to(ROOT)), "bytes": path.stat().st_size}
        for path in selected_files
        if path.stat().st_size > 5 * 1024 * 1024
    ]
    record(
        checks,
        "published_checkpoint_artifacts_below_size_ceiling",
        not oversized,
        oversized,
    )

    forbidden_parts = {".venv", "__pycache__", "runs"}
    forbidden = [
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file()
        and (
            path.suffix.lower() in {".ipynb", ".pyc"}
            or any(part in forbidden_parts for part in path.parts)
        )
        and ".git" not in path.parts
    ]
    record(
        checks,
        "no_forbidden_runtime_artifacts",
        not forbidden,
        forbidden,
    )

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    claim_ceiling = (ROOT / "CLAIM_CEILING.md").read_text(encoding="utf-8")
    record(
        checks,
        "front_door_points_to_current_nonclaim_state",
        "STATUS-2026-07-27.md" in readme
        and "1266-Y5-R2FR" in readme
        and "research-programme/catalogue/README.md" in readme
        and (
            "not presented as a completed theory" in readme.lower()
            or "not a completed unified" in readme.lower()
        )
        and re.search(
            r"coefficient\s+remains\s+unresolved", claim_ceiling.lower()
        )
        is not None,
        "README, latest checkpoint, catalogue, status, and claim ceiling",
    )

    catalogue_readme = (CATALOGUE / "README.md").read_text(encoding="utf-8")
    catalogue_shards = list(CATALOGUE.glob("*-items-*.md"))
    maximum_links = max(
        (
            sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("- ["))
            for path in catalogue_shards
        ),
        default=0,
    )
    record(
        checks,
        "bounded_catalogue_bypasses_folder_display_caps",
        "GitHub can cap large directory" in catalogue_readme
        and maximum_links <= 250
        and len(catalogue_shards) > 0,
        {"shards": len(catalogue_shards), "maximum_links_per_shard": maximum_links},
    )

    inventory_result = verify_inventory()
    record(
        checks,
        "publication_inventory_matches_worktree",
        inventory_result["passed"],
        inventory_result,
    )

    protocol_check = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "verify_checkpoint_1192_snapshot.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    protocol_report = (
        json.loads(protocol_check.stdout)
        if protocol_check.returncode == 0
        else {"stderr": protocol_check.stderr, "stdout": protocol_check.stdout}
    )
    record(
        checks,
        "checkpoint_1192_final_snapshot",
        protocol_check.returncode == 0 and protocol_report.get("passed") is True,
        protocol_report,
    )

    failures = [row for row in checks if not row["passed"]]
    report = {
        "public_checkpoint_range": [PUBLIC_START, PUBLIC_END],
        "private_checkpoint_range": [PRIVATE_START, PRIVATE_END],
        "passed": not failures,
        "checks": checks,
    }
    print(json.dumps(report, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
