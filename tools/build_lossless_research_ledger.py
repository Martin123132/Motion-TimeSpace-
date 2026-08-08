from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable
from urllib.parse import quote


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]
LEDGER_ROOT = REPOSITORY_ROOT / "research-ledger"
FILES_ROOT = LEDGER_ROOT / "files"
MANIFEST_ROOT = LEDGER_ROOT / "manifests"
CATALOGUE_ROOT = LEDGER_ROOT / "catalogue"
AUDIT_ROOT = LEDGER_ROOT / "audits"
SNAPSHOT_DATE = "2026-07-27"
LATEST_PRIVATE_CHECKPOINT = 5252
MANIFEST_SHARD_SIZE = 500
CATALOGUE_SHARD_SIZE = 250
MAX_DIRECTORY_ENTRIES = 500
MAX_GITHUB_FILE_BYTES = 99_000_000
RUN_CHECKPOINTS = (5250, 5251, 5252)
EXCLUDED_DIRECTORY_NAMES = {
    ".git",
    ".venv",
    ".venv-score",
    "__pycache__",
    ".ipynb_checkpoints",
    ".pytest_cache",
    ".mypy_cache",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".log", ".tmp"}
SECRET_PATTERNS = {
    "private_key": re.compile(
        rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----"
    ),
    "github_classic_token": re.compile(rb"gh[pousr]_[A-Za-z0-9]{30,}"),
    "github_fine_grained_token": re.compile(
        rb"github_pat_[A-Za-z0-9_]{30,}"
    ),
    "aws_access_key": re.compile(rb"AKIA[0-9A-Z]{16}"),
    "openai_project_key": re.compile(rb"sk-proj-[A-Za-z0-9_-]{30,}"),
}


@dataclass(frozen=True)
class SourceFile:
    category: str
    source_root: Path
    path: Path
    source_path: str
    category_path: str


@dataclass(frozen=True)
class ManifestRow:
    category: str
    source_path: str
    published_path: str
    size_bytes: int
    sha256: str

    def digest_line(self) -> bytes:
        return (
            f"{self.category}\0{self.source_path}\0{self.published_path}\0"
            f"{self.size_bytes}\0{self.sha256}\n"
        ).encode("utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build or verify the sharded, byte-exact MTS research ledger."
        )
    )
    parser.add_argument(
        "--source",
        type=Path,
        help="Path to the private post-checkpoint-work directory.",
    )
    parser.add_argument(
        "--replace",
        action="store_true",
        help="Replace an existing research-ledger directory after safety checks.",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="Verify the committed ledger without reading the private source.",
    )
    return parser.parse_args()


def relative_posix(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def iter_regular_files(root: Path, *, recursive: bool) -> Iterable[Path]:
    iterator = root.rglob("*") if recursive else root.iterdir()
    for path in sorted(iterator, key=lambda item: item.as_posix().lower()):
        if any(part in EXCLUDED_DIRECTORY_NAMES for part in path.parts):
            continue
        if path.is_symlink():
            raise RuntimeError(f"Symlinks are not accepted: {path}")
        if not path.is_file():
            continue
        if path.suffix.lower() in EXCLUDED_SUFFIXES:
            continue
        yield path


def discover_sources(source_root: Path) -> list[SourceFile]:
    scripts_root = source_root / "scripts"
    residuals_root = source_root / "source-intake" / "mts_residuals"
    runs_root = source_root / "source-intake" / "functional_rg"
    required = (source_root, scripts_root, residuals_root, runs_root)
    missing = [str(path) for path in required if not path.is_dir()]
    if missing:
        raise RuntimeError(f"Missing required source directories: {missing}")

    sources: list[SourceFile] = []
    for path in iter_regular_files(source_root, recursive=False):
        relative = relative_posix(path, source_root)
        sources.append(
            SourceFile(
                category="checkpoints",
                source_root=source_root,
                path=path,
                source_path=relative,
                category_path=relative,
            )
        )

    for path in iter_regular_files(scripts_root, recursive=True):
        relative = relative_posix(path, scripts_root)
        sources.append(
            SourceFile(
                category="scripts",
                source_root=source_root,
                path=path,
                source_path=f"scripts/{relative}",
                category_path=relative,
            )
        )

    for path in iter_regular_files(residuals_root, recursive=True):
        relative = relative_posix(path, residuals_root)
        sources.append(
            SourceFile(
                category="residuals",
                source_root=source_root,
                path=path,
                source_path=f"source-intake/mts_residuals/{relative}",
                category_path=relative,
            )
        )

    for checkpoint in RUN_CHECKPOINTS:
        run_root = runs_root / str(checkpoint)
        if not run_root.is_dir():
            raise RuntimeError(f"Missing selected run directory: {run_root}")
        for path in iter_regular_files(run_root, recursive=True):
            relative = relative_posix(path, run_root)
            sources.append(
                SourceFile(
                    category="runs",
                    source_root=source_root,
                    path=path,
                    source_path=(
                        f"source-intake/functional_rg/{checkpoint}/{relative}"
                    ),
                    category_path=f"{checkpoint}/{relative}",
                )
            )

    source_paths = [source.source_path for source in sources]
    duplicates = [
        path for path, count in Counter(source_paths).items() if count > 1
    ]
    if duplicates:
        raise RuntimeError(f"Duplicate logical source paths: {duplicates[:10]}")
    return sorted(sources, key=lambda source: source.source_path)


def destination_for(source: SourceFile) -> Path:
    bucket = hashlib.sha256(source.source_path.encode("utf-8")).hexdigest()[:2]
    destination = (
        FILES_ROOT / source.category / bucket / Path(source.category_path)
    )
    try:
        destination.resolve().relative_to(FILES_ROOT.resolve())
    except ValueError as error:
        raise RuntimeError(f"Unsafe destination for {source.source_path}") from error
    return destination


def scan_and_copy(sources: list[SourceFile]) -> tuple[list[ManifestRow], list[dict[str, str]]]:
    rows: list[ManifestRow] = []
    secret_findings: list[dict[str, str]] = []
    published_paths: set[str] = set()
    for index, source in enumerate(sources, start=1):
        data = source.path.read_bytes()
        if len(data) > MAX_GITHUB_FILE_BYTES:
            raise RuntimeError(
                f"File exceeds safe GitHub size limit: {source.path} "
                f"({len(data)} bytes)"
            )
        for finding_id, pattern in SECRET_PATTERNS.items():
            if pattern.search(data):
                secret_findings.append(
                    {
                        "finding_id": finding_id,
                        "source_path": source.source_path,
                        "status": "BLOCK_PUBLICATION",
                    }
                )
        destination = destination_for(source)
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(data)
        published_path = relative_posix(destination, REPOSITORY_ROOT)
        if published_path in published_paths:
            raise RuntimeError(f"Published path collision: {published_path}")
        published_paths.add(published_path)
        rows.append(
            ManifestRow(
                category=source.category,
                source_path=source.source_path,
                published_path=published_path,
                size_bytes=len(data),
                sha256=hashlib.sha256(data).hexdigest(),
            )
        )
        if index % 5000 == 0:
            print(f"copied {index:,}/{len(sources):,} source files", flush=True)
    return rows, secret_findings


def write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_manifest_shards(rows: list[ManifestRow]) -> list[str]:
    shard_paths: list[str] = []
    grouped: dict[str, list[ManifestRow]] = defaultdict(list)
    for row in rows:
        grouped[row.category].append(row)
    for category in sorted(grouped):
        category_rows = sorted(
            grouped[category], key=lambda row: row.source_path.lower()
        )
        for start in range(0, len(category_rows), MANIFEST_SHARD_SIZE):
            shard = category_rows[start : start + MANIFEST_SHARD_SIZE]
            first = start + 1
            last = start + len(shard)
            path = (
                MANIFEST_ROOT
                / f"{category}-items-{first:05d}-{last:05d}.csv"
            )
            write_csv(
                path,
                [
                    "category",
                    "source_path",
                    "published_path",
                    "size_bytes",
                    "sha256",
                ],
                [
                    {
                        "category": row.category,
                        "source_path": row.source_path,
                        "published_path": row.published_path,
                        "size_bytes": row.size_bytes,
                        "sha256": row.sha256,
                    }
                    for row in shard
                ],
            )
            shard_paths.append(relative_posix(path, REPOSITORY_ROOT))
    return shard_paths


def markdown_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("[", "\\[").replace("]", "\\]")


def write_catalogue_shards(rows: list[ManifestRow]) -> list[dict[str, object]]:
    summaries: list[dict[str, object]] = []
    grouped: dict[str, list[ManifestRow]] = defaultdict(list)
    for row in rows:
        grouped[row.category].append(row)
    for category in sorted(grouped):
        category_rows = sorted(
            grouped[category], key=lambda row: row.source_path.lower()
        )
        category_shards: list[str] = []
        for start in range(0, len(category_rows), CATALOGUE_SHARD_SIZE):
            shard = category_rows[start : start + CATALOGUE_SHARD_SIZE]
            first = start + 1
            last = start + len(shard)
            path = (
                CATALOGUE_ROOT
                / f"{category}-items-{first:05d}-{last:05d}.md"
            )
            lines = [
                f"# {category.title()} items {first}-{last}",
                "",
                (
                    "These links point to the byte-exact sharded publication "
                    "files. The displayed label is the original source-relative path."
                ),
                "",
            ]
            for row in shard:
                destination = REPOSITORY_ROOT / Path(row.published_path)
                link = Path("..") / destination.relative_to(LEDGER_ROOT)
                encoded_link = quote(link.as_posix(), safe="/-._~")
                lines.append(
                    f"- [{markdown_escape(row.source_path)}]"
                    f"({encoded_link})"
                )
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("\n".join(lines) + "\n", encoding="utf-8")
            category_shards.append(relative_posix(path, REPOSITORY_ROOT))
        summaries.append(
            {
                "category": category,
                "file_count": len(category_rows),
                "size_bytes": sum(row.size_bytes for row in category_rows),
                "catalogue_shards": category_shards,
            }
        )
    return summaries


def compile_script_audit(sources: list[SourceFile]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for source in sources:
        if source.category != "scripts" or source.path.suffix.lower() != ".py":
            continue
        status = "PASS"
        detail = ""
        try:
            text = source.path.read_text(encoding="utf-8-sig")
            compile(text, str(source.path), "exec")
        except Exception as error:
            status = "HISTORICAL_COMPILE_FAILURE"
            detail = f"{type(error).__name__}: {error}"
        rows.append(
            {
                "source_path": source.source_path,
                "status": status,
                "detail": detail,
            }
        )
    return rows


def aggregate_digest(rows: Iterable[ManifestRow]) -> str:
    digest = hashlib.sha256()
    for row in sorted(rows, key=lambda item: item.source_path):
        digest.update(row.digest_line())
    return digest.hexdigest()


def write_metadata(
    rows: list[ManifestRow],
    manifest_shards: list[str],
    catalogue_summaries: list[dict[str, object]],
    compile_rows: list[dict[str, str]],
    secret_findings: list[dict[str, str]],
) -> None:
    write_csv(
        AUDIT_ROOT / "script-compile-audit.csv",
        ["source_path", "status", "detail"],
        compile_rows,
    )
    write_csv(
        AUDIT_ROOT / "secret-scan-audit.csv",
        ["finding_id", "source_path", "status"],
        secret_findings,
    )
    category_rows: list[dict[str, object]] = []
    for summary in catalogue_summaries:
        category = str(summary["category"])
        selected = [row for row in rows if row.category == category]
        category_rows.append(
            {
                "category": category,
                "file_count": len(selected),
                "size_bytes": sum(row.size_bytes for row in selected),
                "sha256_manifest_digest": aggregate_digest(selected),
            }
        )
    write_csv(
        AUDIT_ROOT / "category-summary.csv",
        [
            "category",
            "file_count",
            "size_bytes",
            "sha256_manifest_digest",
        ],
        category_rows,
    )
    snapshot = {
        "snapshot_date": SNAPSHOT_DATE,
        "latest_private_checkpoint": LATEST_PRIVATE_CHECKPOINT,
        "source_scope": {
            "checkpoint_root_files": "all regular top-level files",
            "scripts": "all regular files under scripts",
            "residuals": "all regular files under source-intake/mts_residuals",
            "selected_runs": list(RUN_CHECKPOINTS),
            "excluded": [
                "virtual environments",
                "__pycache__ and bytecode",
                "the remaining multi-gigabyte functional_rg cache",
                "third-party datasets outside post-checkpoint-work",
            ],
        },
        "file_count": len(rows),
        "size_bytes": sum(row.size_bytes for row in rows),
        "sha256_manifest_digest": aggregate_digest(rows),
        "manifest_shards": manifest_shards,
        "categories": category_rows,
        "script_compile": {
            "checked": len(compile_rows),
            "passed": sum(row["status"] == "PASS" for row in compile_rows),
            "historical_failures": sum(
                row["status"] != "PASS" for row in compile_rows
            ),
        },
        "secret_scan_findings": len(secret_findings),
        "generated_utc": datetime.now(timezone.utc).isoformat(),
    }
    (LEDGER_ROOT / "snapshot.json").write_text(
        json.dumps(snapshot, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    catalogue_lines = [
        "# Lossless Research Ledger Catalogue",
        "",
        (
            "Every catalogue shard has at most "
            f"{CATALOGUE_SHARD_SIZE} direct links, avoiding GitHub's "
            "large-flat-folder display cap."
        ),
        "",
        "| Category | Files | Size | Shards |",
        "|---|---:|---:|---:|",
    ]
    for summary in catalogue_summaries:
        catalogue_lines.append(
            f"| {summary['category']} | {summary['file_count']:,} | "
            f"{int(summary['size_bytes']):,} bytes | "
            f"{len(summary['catalogue_shards']):,} |"
        )
    catalogue_lines.extend(["", "## Shards", ""])
    for summary in catalogue_summaries:
        catalogue_lines.append(f"### {str(summary['category']).title()}")
        catalogue_lines.append("")
        for shard_path in summary["catalogue_shards"]:
            shard = Path(str(shard_path))
            catalogue_lines.append(
                f"- [{shard.stem}]({quote(shard.name, safe='-._~')})"
            )
        catalogue_lines.append("")
    (CATALOGUE_ROOT / "README.md").write_text(
        "\n".join(catalogue_lines).rstrip() + "\n",
        encoding="utf-8",
    )

    readme = f"""# Lossless MTS Research Ledger

This directory is the byte-exact, physically sharded publication snapshot of
the private `post-checkpoint-work` ledger through private checkpoint
`{LATEST_PRIVATE_CHECKPOINT}` on {SNAPSHOT_DATE}.

It exists because the earlier compact public sequence was deliberately curated
and its flat directories exceeded GitHub's ordinary folder-display limit.
GitHub's interface could therefore look incomplete even when the Git objects
were present. This ledger fixes both problems:

- every selected local source file is copied byte-for-byte;
- every published file has a size and SHA-256 row in `manifests/`;
- files are distributed by stable two-character path-hash buckets;
- no physical directory may exceed {MAX_DIRECTORY_ENTRIES} entries;
- bounded direct-link indexes live in `catalogue/`;
- `snapshot.json` records the aggregate manifest digest.

## Scope

The snapshot contains {len(rows):,} source files totalling
{sum(row.size_bytes for row in rows):,} bytes:

"""
    for row in category_rows:
        readme += (
            f"- **{row['category']}**: {int(row['file_count']):,} files, "
            f"{int(row['size_bytes']):,} bytes\n"
        )
    readme += f"""

The selected run evidence is limited to private checkpoints
`{RUN_CHECKPOINTS[0]}`-`{RUN_CHECKPOINTS[-1]}`. The remaining multi-gigabyte
`functional_rg` cache, virtual environments, and third-party datasets are not
committed.

## Integrity

Run:

```powershell
python tools/build_lossless_research_ledger.py --verify-only
```

The verifier checks every manifest row against the committed byte stream,
detects missing or extra ledger files, verifies the aggregate digest, enforces
the directory-entry ceiling, and confirms the latest scripts and validations
are present.

This ledger is an audit trail, not a promotion of every historical result.
The repository's root `CLAIM_CEILING.md` remains controlling.
"""
    (LEDGER_ROOT / "README.md").write_text(readme, encoding="utf-8")


def read_manifest_rows() -> list[ManifestRow]:
    rows: list[ManifestRow] = []
    for path in sorted(MANIFEST_ROOT.glob("*.csv")):
        with path.open(encoding="utf-8", newline="") as handle:
            for row in csv.DictReader(handle):
                rows.append(
                    ManifestRow(
                        category=row["category"],
                        source_path=row["source_path"],
                        published_path=row["published_path"],
                        size_bytes=int(row["size_bytes"]),
                        sha256=row["sha256"],
                    )
                )
    return rows


def verify_directory_limits() -> tuple[bool, list[dict[str, object]]]:
    violations: list[dict[str, object]] = []
    for directory in [LEDGER_ROOT, *LEDGER_ROOT.rglob("*")]:
        if not directory.is_dir():
            continue
        count = sum(1 for _ in directory.iterdir())
        if count > MAX_DIRECTORY_ENTRIES:
            violations.append(
                {
                    "path": relative_posix(directory, REPOSITORY_ROOT),
                    "entry_count": count,
                }
            )
    return not violations, violations


def verify_ledger() -> dict[str, object]:
    snapshot_path = LEDGER_ROOT / "snapshot.json"
    if not snapshot_path.is_file():
        raise RuntimeError(f"Missing snapshot metadata: {snapshot_path}")
    snapshot = json.loads(snapshot_path.read_text(encoding="utf-8"))
    rows = read_manifest_rows()
    failures: list[str] = []
    expected_paths = {row.published_path for row in rows}
    actual_paths = {
        relative_posix(path, REPOSITORY_ROOT)
        for path in FILES_ROOT.rglob("*")
        if path.is_file()
    }
    duplicate_source_paths = [
        path
        for path, count in Counter(row.source_path for row in rows).items()
        if count > 1
    ]
    duplicate_published_paths = [
        path
        for path, count in Counter(row.published_path for row in rows).items()
        if count > 1
    ]
    if duplicate_source_paths:
        failures.append(
            f"duplicate-source-paths:{duplicate_source_paths[:10]}"
        )
    if duplicate_published_paths:
        failures.append(
            f"duplicate-published-paths:{duplicate_published_paths[:10]}"
        )
    missing = sorted(expected_paths - actual_paths)
    extra = sorted(actual_paths - expected_paths)
    if missing:
        failures.append(f"missing-files:{missing[:10]}")
    if extra:
        failures.append(f"extra-files:{extra[:10]}")
    for index, row in enumerate(rows, start=1):
        path = REPOSITORY_ROOT / Path(row.published_path)
        if not path.is_file():
            continue
        data = path.read_bytes()
        if len(data) != row.size_bytes:
            failures.append(f"size:{row.published_path}")
            continue
        if hashlib.sha256(data).hexdigest() != row.sha256:
            failures.append(f"sha256:{row.published_path}")
        if index % 10000 == 0:
            print(f"verified {index:,}/{len(rows):,} ledger files", flush=True)
    directory_limits_pass, directory_violations = verify_directory_limits()
    if not directory_limits_pass:
        failures.append(f"directory-limits:{directory_violations[:10]}")
    digest = aggregate_digest(rows)
    if digest != snapshot.get("sha256_manifest_digest"):
        failures.append("aggregate-manifest-digest")
    if len(rows) != int(snapshot.get("file_count", -1)):
        failures.append("snapshot-file-count")
    if sum(row.size_bytes for row in rows) != int(
        snapshot.get("size_bytes", -1)
    ):
        failures.append("snapshot-size-bytes")
    if int(snapshot.get("secret_scan_findings", -1)) != 0:
        failures.append("secret-scan-findings")

    required_source_suffixes = {
        "5251-Y5-R2FR-order5-backbone-paired-transport-rebuild.md",
        "5252-Y5-R2FR-Q01-Q07-full-order9-paired-transport-and-outer-gate.md",
        "scripts/Y5_R2FR_5251_order5_backbone_paired_transport_rebuild.py",
        (
            "scripts/"
            "Y5_R2FR_5252_Q01_Q07_full_order9_paired_transport_and_outer_gate.py"
        ),
        (
            "source-intake/mts_residuals/"
            "P8_Y5_BRR545_5251_VALIDATION.csv"
        ),
        (
            "source-intake/mts_residuals/"
            "P8_Y5_BRR545_5252_VALIDATION.csv"
        ),
    }
    source_paths = {row.source_path for row in rows}
    missing_latest = sorted(required_source_suffixes - source_paths)
    if missing_latest:
        failures.append(f"missing-latest:{missing_latest}")

    result = {
        "passed": not failures,
        "file_count": len(rows),
        "size_bytes": sum(row.size_bytes for row in rows),
        "sha256_manifest_digest": digest,
        "missing_count": len(missing),
        "extra_count": len(extra),
        "directory_limits_pass": directory_limits_pass,
        "directory_violations": directory_violations,
        "failures": failures,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def safe_replace_ledger() -> None:
    expected = (REPOSITORY_ROOT / "research-ledger").resolve()
    actual = LEDGER_ROOT.resolve()
    if actual != expected or actual.parent != REPOSITORY_ROOT.resolve():
        raise RuntimeError(f"Refusing unsafe ledger deletion: {actual}")
    if LEDGER_ROOT.exists():
        shutil.rmtree(LEDGER_ROOT)


def build(source_root: Path, *, replace: bool) -> None:
    source_root = source_root.resolve()
    if source_root.name != "post-checkpoint-work":
        raise RuntimeError(
            "The source must be the post-checkpoint-work directory, got "
            f"{source_root}"
        )
    if LEDGER_ROOT.exists() and not replace:
        raise RuntimeError(
            f"{LEDGER_ROOT} already exists; pass --replace to rebuild it"
        )
    if replace:
        safe_replace_ledger()
    LEDGER_ROOT.mkdir(parents=True, exist_ok=False)
    sources = discover_sources(source_root)
    print(f"discovered {len(sources):,} source files")
    rows, secret_findings = scan_and_copy(sources)
    compile_rows = compile_script_audit(sources)
    manifest_shards = write_manifest_shards(rows)
    catalogue_summaries = write_catalogue_shards(rows)
    write_metadata(
        rows,
        manifest_shards,
        catalogue_summaries,
        compile_rows,
        secret_findings,
    )
    if secret_findings:
        raise RuntimeError(
            "Credential-like material blocked publication; inspect "
            f"{AUDIT_ROOT / 'secret-scan-audit.csv'}"
        )
    result = verify_ledger()
    if not result["passed"]:
        raise RuntimeError("Lossless ledger verification failed")


def main() -> None:
    args = parse_args()
    if args.verify_only:
        result = verify_ledger()
        raise SystemExit(0 if result["passed"] else 1)
    if args.source is None:
        raise SystemExit("--source is required unless --verify-only is used")
    build(args.source, replace=args.replace)


if __name__ == "__main__":
    main()
