from __future__ import annotations

import csv
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

import verify_public_update_1266 as base


ROOT = Path(__file__).resolve().parents[1]
LEDGER_MANIFESTS = ROOT / "research-ledger" / "manifests"
PUBLIC_INVENTORY = (
    ROOT / "docs" / "status" / "PUBLICATION-INVENTORY-2026-07-27.csv"
)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def verify_ledger_against_git_inventory() -> None:
    inventory = {
        row["path"]: row for row in read_csv_rows(PUBLIC_INVENTORY)
    }
    ledger_rows: list[dict[str, str]] = []
    for path in sorted(LEDGER_MANIFESTS.glob("*.csv")):
        ledger_rows.extend(read_csv_rows(path))
    failures: list[str] = []
    by_source: dict[str, dict[str, str]] = {}
    for row in ledger_rows:
        by_source[row["source_path"]] = row
        indexed = inventory.get(row["published_path"])
        if indexed is None:
            failures.append(f"missing-index:{row['published_path']}")
            continue
        if indexed["size_bytes"] != row["size_bytes"]:
            failures.append(f"size:{row['published_path']}")
            continue
        if indexed["sha256"] != row["sha256"]:
            failures.append(f"sha256:{row['published_path']}")

    curated_pairs = {
        "5251-Y5-R2FR-order5-backbone-paired-transport-rebuild.md": (
            "research-programme/checkpoints/"
            "1267-Y5-R2FR-order5-backbone-paired-transport-rebuild.md"
        ),
        "5252-Y5-R2FR-Q01-Q07-full-order9-paired-transport-and-outer-gate.md": (
            "research-programme/checkpoints/"
            "1268-Y5-R2FR-Q01-Q07-full-order9-paired-transport-and-outer-gate.md"
        ),
        "scripts/Y5_R2FR_5251_order5_backbone_paired_transport_rebuild.py": (
            "research-programme/scripts/"
            "Y5_R2FR_5251_order5_backbone_paired_transport_rebuild.py"
        ),
        (
            "scripts/"
            "Y5_R2FR_5252_Q01_Q07_full_order9_paired_transport_and_outer_gate.py"
        ): (
            "research-programme/scripts/"
            "Y5_R2FR_5252_Q01_Q07_full_order9_paired_transport_and_outer_gate.py"
        ),
        (
            "source-intake/mts_residuals/"
            "P8_Y5_BRR545_5251_VALIDATION.csv"
        ): (
            "research-programme/source-intake/mts_residuals/"
            "P8_Y5_BRR545_5251_VALIDATION.csv"
        ),
        (
            "source-intake/mts_residuals/"
            "P8_Y5_BRR545_5252_VALIDATION.csv"
        ): (
            "research-programme/source-intake/mts_residuals/"
            "P8_Y5_BRR545_5252_VALIDATION.csv"
        ),
    }
    for source_path, public_path in curated_pairs.items():
        source_row = by_source.get(source_path)
        public_row = inventory.get(public_path)
        if source_row is None or public_row is None:
            failures.append(f"curated-missing:{source_path}:{public_path}")
            continue
        if (
            source_row["size_bytes"] != public_row["size_bytes"]
            or source_row["sha256"] != public_row["sha256"]
        ):
            failures.append(f"curated-byte-mismatch:{public_path}")

    if len(ledger_rows) != 57_444:
        failures.append(f"ledger-row-count:{len(ledger_rows)}")
    if failures:
        raise SystemExit(
            "Ledger-to-Git inventory verification failed: "
            + "; ".join(failures[:20])
        )
    print(
        "ledger_git_inventory_match "
        f"rows={len(ledger_rows)} curated_pairs={len(curated_pairs)}"
    )


def main() -> None:
    ledger = subprocess.run(
        [
            sys.executable,
            str(ROOT / "tools" / "build_lossless_research_ledger.py"),
            "--verify-only",
        ],
        cwd=ROOT,
        check=False,
    )
    if ledger.returncode != 0:
        raise SystemExit("Lossless research-ledger verification failed")
    verify_ledger_against_git_inventory()

    base.PUBLIC_END = 1268
    base.PRIVATE_END = 5252
    base.EXPECTED_SCRIPT_COUNT = 79
    base.EXPECTED_RESIDUAL_COUNT = 76
    base.EXPECTED_NONPASS_VALIDATION_IDS = {
        5216,
        5221,
        5240,
        5241,
        5244,
        5251,
        5252,
    }
    base.main()


if __name__ == "__main__":
    main()
