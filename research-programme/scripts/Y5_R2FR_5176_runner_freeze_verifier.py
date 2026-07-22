from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True


POST = Path(__file__).resolve().parents[1]
OUT = POST / "source-intake" / "functional_rg" / "5176"
FREEZE_PATH = OUT / "runner_freeze.json"
RUNNER_PATH = (
    POST
    / "scripts"
    / "Y5_R2FR_5176_predeclared_paired_high_mode_seed_ensemble.py"
)


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def verify_freeze() -> dict[str, Any]:
    freeze = json.loads(FREEZE_PATH.read_text(encoding="utf-8"))
    checks = {
        "runner_script": (
            RUNNER_PATH,
            freeze["runner_script_sha256"],
        ),
        "protocol_file": (
            OUT / "ensemble_protocol.json",
            freeze["protocol_file_sha256"],
        ),
        "schedule_file": (
            OUT / "predeclared_seed_schedule.csv",
            freeze["schedule_file_sha256"],
        ),
        "source_provenance": (
            OUT / "source_provenance.csv",
            freeze["source_provenance_sha256"],
        ),
        "first_seed_result": (
            OUT / "seeds/seed_01_3240854344/seed_result.json",
            freeze["first_seed_result_sha256"],
        ),
    }
    failures: list[dict[str, str]] = []
    verified: dict[str, str] = {}
    for check_id, (path, expected) in checks.items():
        if not path.is_file():
            failures.append(
                {
                    "check_id": check_id,
                    "path": str(path),
                    "failure": "missing",
                }
            )
            continue
        actual = file_digest(path)
        verified[check_id] = actual
        if actual.lower() != str(expected).lower():
            failures.append(
                {
                    "check_id": check_id,
                    "path": str(path),
                    "expected": str(expected),
                    "actual": actual,
                }
            )
    for source_id, expected in freeze["read_only_source_hashes"].items():
        provenance = OUT / "source_provenance.csv"
        rows = provenance.read_text(encoding="utf-8").splitlines()
        matches = [row for row in rows[1:] if row.startswith(f"{source_id},")]
        if len(matches) != 1:
            failures.append(
                {
                    "check_id": source_id,
                    "path": str(provenance),
                    "failure": "provenance row missing or duplicated",
                }
            )
            continue
        fields = matches[0].split(",")
        source_path = Path(fields[1])
        if not source_path.is_file():
            failures.append(
                {
                    "check_id": source_id,
                    "path": str(source_path),
                    "failure": "source missing",
                }
            )
            continue
        actual = file_digest(source_path)
        if actual.lower() != str(expected).lower():
            failures.append(
                {
                    "check_id": source_id,
                    "path": str(source_path),
                    "expected": str(expected),
                    "actual": actual,
                }
            )
    if failures:
        raise RuntimeError(
            "runner freeze verification failed:\n"
            + json.dumps(failures, indent=2)
        )
    return {
        "freeze_verified": True,
        "protocol_sha256": freeze["protocol_sha256"],
        "runner_script_sha256": freeze["runner_script_sha256"],
        "remaining_seed_count_at_freeze": freeze["remaining_seed_count"],
        "verified_files": verified,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-next", action="store_true")
    arguments = parser.parse_args()
    result = verify_freeze()
    print(json.dumps(result, indent=2))
    if arguments.run_next:
        subprocess.run(
            [sys.executable, str(RUNNER_PATH), "--run-next"],
            cwd=POST.parent,
            check=True,
        )


if __name__ == "__main__":
    main()

