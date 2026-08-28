from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "status" / "PUBLICATION-MANIFEST-2026-08-29.csv"
START_PRIVATE = 5337
END_PRIVATE = 5417
PUBLIC_OFFSET = 3984
EXPECTED_COUNTS = {"checkpoint": 77, "script": 88, "residual": 47}
MAX_RESIDUAL_BYTES = 5 * 1024 * 1024
SECRET_PATTERNS = {
    "private_key": re.compile(
        rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"
    ),
    "github_token": re.compile(rb"gh[pousr]_[A-Za-z0-9]{30,}"),
    "github_fine_grained": re.compile(rb"github_pat_[A-Za-z0-9_]{30,}"),
    "openai_project_key": re.compile(rb"sk-proj-[A-Za-z0-9_-]{30,}"),
}
CATEGORY_CONFIG = {
    "checkpoint": (
        ROOT / "research-programme" / "checkpoints",
        "checkpoints-items-*.md",
    ),
    "script": (
        ROOT / "research-programme" / "scripts",
        "scripts-items-*.md",
    ),
    "residual": (
        ROOT / "research-programme" / "source-intake" / "mts_residuals",
        "residuals-items-*.md",
    ),
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        help="Private post-checkpoint-work directory; writes the dated manifest.",
    )
    return parser.parse_args()


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def ids_in_range(name: str) -> list[int]:
    return sorted(
        {
            int(match.group(1))
            for match in re.finditer(r"(?<!\d)(\d{4})(?!\d)", name)
            if START_PRIVATE <= int(match.group(1)) <= END_PRIVATE
        }
    )


def source_rows(source: Path) -> list[dict[str, str | int]]:
    source = source.resolve()
    if source.name != "post-checkpoint-work":
        raise RuntimeError(f"unexpected source directory: {source}")
    scripts = source / "scripts"
    residuals = source / "source-intake" / "mts_residuals"
    rows: list[dict[str, str | int]] = []

    for path in sorted(source.glob("*.md"), key=lambda item: item.name):
        match = re.match(r"^(\d+)([A-Za-z]*)-(.+)$", path.name)
        if not match:
            continue
        private_id = int(match.group(1))
        if not START_PRIVATE <= private_id <= END_PRIVATE:
            continue
        destination_name = (
            f"{private_id - PUBLIC_OFFSET}{match.group(2)}-{match.group(3)}"
        )
        rows.append(
            manifest_row(
                "checkpoint",
                str(private_id),
                path,
                source,
                ROOT / "research-programme" / "checkpoints" / destination_name,
            )
        )

    for path in sorted(scripts.glob("*.py"), key=lambda item: item.name):
        identifiers = ids_in_range(path.name)
        if identifiers:
            rows.append(
                manifest_row(
                    "script",
                    ";".join(str(value) for value in identifiers),
                    path,
                    source,
                    ROOT / "research-programme" / "scripts" / path.name,
                )
            )

    for path in sorted(residuals.iterdir(), key=lambda item: item.name):
        identifiers = ids_in_range(path.name)
        if (
            path.is_file()
            and path.suffix.lower() in {".csv", ".json"}
            and identifiers
        ):
            if path.stat().st_size > MAX_RESIDUAL_BYTES:
                raise RuntimeError(f"residual exceeds size ceiling: {path}")
            rows.append(
                manifest_row(
                    "residual",
                    ";".join(str(value) for value in identifiers),
                    path,
                    source,
                    ROOT
                    / "research-programme"
                    / "source-intake"
                    / "mts_residuals"
                    / path.name,
                )
            )
    return sorted(rows, key=lambda row: str(row["published_path"]))


def manifest_row(
    kind: str,
    private_id: str,
    source_path: Path,
    source_root: Path,
    published_path: Path,
) -> dict[str, str | int]:
    return {
        "kind": kind,
        "private_id": private_id,
        "source_path": source_path.relative_to(source_root).as_posix(),
        "published_path": published_path.relative_to(ROOT).as_posix(),
        "size_bytes": source_path.stat().st_size,
        "sha256": sha256(source_path),
    }


def write_manifest(rows: list[dict[str, str | int]]) -> None:
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    with MANIFEST.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def read_manifest() -> list[dict[str, str]]:
    with MANIFEST.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def catalogue_text(kind: str) -> tuple[str, list[Path]]:
    _, pattern = CATEGORY_CONFIG[kind]
    paths = sorted((ROOT / "research-programme" / "catalogue").glob(pattern))
    return "\n".join(path.read_text(encoding="utf-8") for path in paths), paths


def all_true(values: Iterable[bool]) -> bool:
    return all(values)


def verify(rows: list[dict[str, str]]) -> dict[str, object]:
    failures: list[str] = []
    counts = {kind: 0 for kind in EXPECTED_COUNTS}
    published_paths: list[str] = []
    secret_findings: list[str] = []
    compile_failures: list[str] = []

    for row in rows:
        kind = row["kind"]
        counts[kind] = counts.get(kind, 0) + 1
        published = ROOT / Path(row["published_path"])
        published_paths.append(row["published_path"])
        if not published.is_file():
            failures.append(f"missing:{row['published_path']}")
            continue
        content = published.read_bytes()
        if len(content) != int(row["size_bytes"]):
            failures.append(f"size:{row['published_path']}")
        if hashlib.sha256(content).hexdigest() != row["sha256"]:
            failures.append(f"sha256:{row['published_path']}")
        for finding, pattern in SECRET_PATTERNS.items():
            if pattern.search(content):
                secret_findings.append(f"{finding}:{row['published_path']}")
        if kind == "script":
            try:
                compile(
                    published.read_text(encoding="utf-8-sig"),
                    str(published),
                    "exec",
                )
            except Exception as error:
                compile_failures.append(
                    f"{row['published_path']}:{type(error).__name__}:{error}"
                )

    if counts != EXPECTED_COUNTS:
        failures.append(f"counts:{counts}")
    if len(published_paths) != len(set(published_paths)):
        failures.append("duplicate-published-path")
    failures.extend(secret_findings)
    failures.extend(f"compile:{value}" for value in compile_failures)

    catalogue_missing: list[str] = []
    catalogue_link_ceiling = True
    for kind in EXPECTED_COUNTS:
        text, shards = catalogue_text(kind)
        for row in rows:
            if row["kind"] != kind:
                continue
            name = Path(row["published_path"]).name
            if f"`{name}`" not in text:
                catalogue_missing.append(row["published_path"])
        for shard in shards:
            direct_links = sum(
                line.startswith("- [`")
                for line in shard.read_text(encoding="utf-8").splitlines()
            )
            catalogue_link_ceiling &= direct_links <= 250
    if catalogue_missing:
        failures.append(f"catalogue-missing:{catalogue_missing[:10]}")
    if not catalogue_link_ceiling:
        failures.append("catalogue-link-ceiling")

    required_docs = (
        ROOT / "docs" / "status" / "STATUS-2026-08-29.md",
        ROOT / "docs" / "status" / "PUBLICATION-NOTES-2026-08-29.md",
        ROOT / "research-programme" / "checkpoints"
        / "1433-Y5-R2FR-D4-v43-right-connector-frontier-expansion-gate.md",
    )
    missing_docs = [str(path.relative_to(ROOT)) for path in required_docs if not path.is_file()]
    if missing_docs:
        failures.append(f"missing-docs:{missing_docs}")

    forbidden_functional = ROOT / "research-programme" / "source-intake" / "functional_rg"
    if forbidden_functional.exists():
        failures.append("functional-rg-tree-published")

    return {
        "passed": not failures,
        "manifest_rows": len(rows),
        "counts": counts,
        "compiled_scripts": counts.get("script", 0),
        "compile_failures": compile_failures,
        "secret_findings": secret_findings,
        "catalogue_missing_count": len(catalogue_missing),
        "catalogue_link_ceiling": catalogue_link_ceiling,
        "failures": failures,
    }


def main() -> int:
    args = parse_args()
    if args.source is not None:
        generated = source_rows(args.source)
        for row in generated:
            published = ROOT / Path(str(row["published_path"]))
            if not published.is_file():
                raise RuntimeError(f"missing staged publication file: {published}")
            if sha256(published) != row["sha256"]:
                raise RuntimeError(f"source/public hash mismatch: {published}")
        write_manifest(generated)
    rows = read_manifest()
    result = verify(rows)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
