from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC_CHECKPOINTS = ROOT / "research-programme" / "checkpoints"
PUBLIC_SCRIPTS = ROOT / "research-programme" / "scripts"
PUBLIC_RESIDUALS = (
    ROOT / "research-programme" / "source-intake" / "mts_residuals"
)
PRIVATE_OFFSET = 3984
PRIVATE_IDS = (5251, 5252)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy private checkpoints 5251-5252 into the curated public sequence."
    )
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to the private post-checkpoint-work directory.",
    )
    return parser.parse_args()


def one_match(directory: Path, pattern: str) -> Path:
    matches = sorted(directory.glob(pattern))
    if len(matches) != 1:
        raise RuntimeError(
            f"Expected one match for {pattern} in {directory}, found {matches}"
        )
    return matches[0]


def copy_exact(source: Path, destination: Path) -> dict[str, object]:
    if destination.exists():
        raise RuntimeError(f"Refusing to overwrite existing file: {destination}")
    data = source.read_bytes()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(data)
    copied = destination.read_bytes()
    if copied != data:
        raise RuntimeError(f"Byte mismatch after copy: {destination}")
    return {
        "source": source.as_posix(),
        "destination": destination.relative_to(ROOT).as_posix(),
        "size_bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
    }


def main() -> None:
    args = parse_args()
    source = args.source.resolve()
    if source.name != "post-checkpoint-work":
        raise RuntimeError(f"Unexpected source directory: {source}")
    rows: list[dict[str, object]] = []
    for private_id in PRIVATE_IDS:
        public_id = private_id - PRIVATE_OFFSET
        document = one_match(source, f"{private_id}-*.md")
        public_document_name = (
            f"{public_id}{document.name[len(str(private_id)):]}"
        )
        rows.append(
            copy_exact(document, PUBLIC_CHECKPOINTS / public_document_name)
        )

        script = one_match(source / "scripts", f"*{private_id}*.py")
        rows.append(copy_exact(script, PUBLIC_SCRIPTS / script.name))

        validation = one_match(
            source / "source-intake" / "mts_residuals",
            f"*{private_id}*VALIDATION.csv",
        )
        rows.append(copy_exact(validation, PUBLIC_RESIDUALS / validation.name))

    expected = {
        "research-programme/checkpoints/"
        "1267-Y5-R2FR-order5-backbone-paired-transport-rebuild.md",
        "research-programme/checkpoints/"
        "1268-Y5-R2FR-Q01-Q07-full-order9-paired-transport-and-outer-gate.md",
        "research-programme/scripts/"
        "Y5_R2FR_5251_order5_backbone_paired_transport_rebuild.py",
        "research-programme/scripts/"
        "Y5_R2FR_5252_Q01_Q07_full_order9_paired_transport_and_outer_gate.py",
        "research-programme/source-intake/mts_residuals/"
        "P8_Y5_BRR545_5251_VALIDATION.csv",
        "research-programme/source-intake/mts_residuals/"
        "P8_Y5_BRR545_5252_VALIDATION.csv",
    }
    observed = {str(row["destination"]) for row in rows}
    if observed != expected:
        raise RuntimeError(
            f"Curated publication mapping mismatch: {sorted(observed ^ expected)}"
        )
    print(json.dumps({"passed": True, "files": rows}, indent=2))


if __name__ == "__main__":
    main()
