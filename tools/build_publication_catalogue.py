from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
CATALOGUE = ROOT / "research-programme" / "catalogue"
INVENTORY = ROOT / "docs" / "status" / "PUBLICATION-INVENTORY-2026-07-27.csv"
SHARD_SIZE = 250

CATEGORIES = {
    "checkpoints": {
        "directory": ROOT / "research-programme" / "checkpoints",
        "extensions": {".md"},
        "relative_target": "../checkpoints",
    },
    "scripts": {
        "directory": ROOT / "research-programme" / "scripts",
        "extensions": {".py"},
        "relative_target": "../scripts",
    },
    "residuals": {
        "directory": ROOT
        / "research-programme"
        / "source-intake"
        / "mts_residuals",
        "extensions": {".csv", ".json"},
        "relative_target": "../source-intake/mts_residuals",
    },
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build the bounded public catalogues and/or Git index inventory."
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--catalogue-only",
        action="store_true",
        help="Regenerate only the bounded catalogue shards.",
    )
    group.add_argument(
        "--inventory-only",
        action="store_true",
        help="Regenerate only the staged Git-index inventory.",
    )
    return parser.parse_args()


def checkpoint_sort_key(path: Path) -> tuple[int, str]:
    match = re.match(r"^(\d+)", path.name)
    return (int(match.group(1)) if match else 10**9, path.name.casefold())


def category_files(category: str) -> list[Path]:
    config = CATEGORIES[category]
    files = [
        path
        for path in config["directory"].iterdir()
        if path.is_file() and path.suffix.lower() in config["extensions"]
    ]
    if category == "checkpoints":
        return sorted(files, key=checkpoint_sort_key)
    return sorted(files, key=lambda path: path.name.casefold())


def write_catalogue() -> dict[str, object]:
    CATALOGUE.mkdir(parents=True, exist_ok=True)
    for stale_path in CATALOGUE.glob("*-items-*.md"):
        stale_path.unlink()

    summary: dict[str, object] = {}
    readme_lines = [
        "# Research Programme Catalogue",
        "",
        "GitHub can cap large directory and pull-request file listings. The",
        "underlying Git tree remains complete, but entries beyond the display",
        "limit may not appear in the normal folder view. These bounded catalogues",
        "provide direct links to every checkpoint, script, and compact residual.",
        "",
        "| Category | Files | Catalogue shards |",
        "|---|---:|---:|",
    ]
    shard_links: list[str] = []

    for category in CATEGORIES:
        files = category_files(category)
        shard_count = (len(files) + SHARD_SIZE - 1) // SHARD_SIZE
        readme_lines.append(f"| {category.title()} | {len(files)} | {shard_count} |")
        category_shards: list[str] = []

        for shard_index, start in enumerate(range(0, len(files), SHARD_SIZE), start=1):
            shard = files[start : start + SHARD_SIZE]
            first_ordinal = start + 1
            last_ordinal = start + len(shard)
            shard_name = (
                f"{category}-items-{first_ordinal:04d}-{last_ordinal:04d}.md"
            )
            shard_path = CATALOGUE / shard_name
            target = CATEGORIES[category]["relative_target"]
            lines = [
                f"# {category.title()} catalogue: items {first_ordinal}-{last_ordinal}",
                "",
                f"Direct links for {len(shard)} files. Item numbers are catalogue",
                "ordinals, not scientific checkpoint identifiers.",
                "",
            ]
            for path in shard:
                encoded_name = quote(path.name)
                lines.append(
                    f"- [`{path.name}`]({target}/{encoded_name})"
                    f" ({path.stat().st_size} bytes)"
                )
            shard_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            category_shards.append(shard_name)
            shard_links.append(
                f"- [{category.title()} items {first_ordinal}-{last_ordinal}]"
                f"({quote(shard_name)})"
            )

        summary[category] = {
            "files": len(files),
            "shards": category_shards,
        }

    readme_lines.extend(
        [
            "",
            "## Shards",
            "",
            *shard_links,
            "",
            "## Integrity",
            "",
            "The dated publication inventory at",
            "`../../docs/status/PUBLICATION-INVENTORY-2026-07-27.csv` records",
            "the path, byte count, and SHA-256 digest of every published file",
            "except the inventory itself.",
        ]
    )
    (CATALOGUE / "README.md").write_text(
        "\n".join(readme_lines) + "\n", encoding="utf-8"
    )
    return summary


def index_entries() -> list[tuple[str, str]]:
    result = subprocess.run(
        ["git", "-C", str(ROOT), "ls-files", "-s", "-z"],
        capture_output=True,
        check=True,
    )
    inventory_relative = INVENTORY.relative_to(ROOT).as_posix()
    entries: list[tuple[str, str]] = []
    for raw_record in result.stdout.split(b"\0"):
        if not raw_record:
            continue
        header, raw_path = raw_record.split(b"\t", maxsplit=1)
        _, object_id, stage = header.decode("ascii").split()
        path = raw_path.decode("utf-8", errors="surrogateescape")
        if stage == "0" and path != inventory_relative:
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


def write_inventory() -> dict[str, int]:
    INVENTORY.parent.mkdir(parents=True, exist_ok=True)
    entries = index_entries()
    blobs = index_blob_contents(entries)
    total_bytes = 0
    with INVENTORY.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["path", "size_bytes", "sha256"],
        )
        writer.writeheader()
        for (path, _), content in zip(entries, blobs, strict=True):
            size_bytes = len(content)
            total_bytes += size_bytes
            writer.writerow(
                {
                    "path": path,
                    "size_bytes": size_bytes,
                    "sha256": hashlib.sha256(content).hexdigest(),
                }
            )
    return {"files": len(entries), "bytes": total_bytes}


def main() -> None:
    args = parse_args()
    catalogue_summary = None if args.inventory_only else write_catalogue()
    inventory_summary = None if args.catalogue_only else write_inventory()
    print(
        json.dumps(
            {
                "catalogue": catalogue_summary,
                "inventory": inventory_summary,
                "inventory_excludes_itself": True,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
