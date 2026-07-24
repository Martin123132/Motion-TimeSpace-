from __future__ import annotations

import csv
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
PUBLIC_START = 1192
PUBLIC_END = 1230
PRIVATE_OFFSET = 3984
PRIVATE_START = PUBLIC_START + PRIVATE_OFFSET
PRIVATE_END = PUBLIC_END + PRIVATE_OFFSET


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
        len(script_files) == 40 and not compile_failures,
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
    validation_row_count = 0
    for path in residual_files:
        try:
            if path.suffix.lower() == ".json":
                json.loads(path.read_text(encoding="utf-8"))
            else:
                passed, row_count = validation_rows_pass(path)
                validation_row_count += row_count
                if not passed:
                    validation_failures.append(path.name)
        except Exception as error:
            parse_failures.append(f"{path.name}: {error}")
    record(
        checks,
        "compact_residuals_parse_and_pass",
        len(residual_files) == 39
        and not parse_failures
        and not validation_failures,
        {
            "count": len(residual_files),
            "validation_rows": validation_row_count,
            "parse_failures": parse_failures,
            "validation_failures": validation_failures,
        },
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
        "STATUS-2026-07-24.md" in readme
        and "1230-Y5-R2FR" in readme
        and (
            "not presented as a completed theory" in readme.lower()
            or "not a completed unified" in readme.lower()
        )
        and re.search(r"not an\s+all-operator", claim_ceiling.lower())
        is not None,
        "README, status, latest checkpoint, and claim ceiling",
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
