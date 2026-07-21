from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from mathics.core.definitions import Definitions

from Y5_R2FR_4933_wolfram_notebook_box_extractor import box_to_wl, parse_boxdata


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4933" / "Flow_mendeley.nb"
OUTPUT_DIR = POST / "source-intake" / "functional_rg" / "4933"
OUTPUT_INPUT = OUTPUT_DIR / "Flow_mendeley_input_extracted.wl"
OUTPUT_OUTPUT = OUTPUT_DIR / "Flow_mendeley_output_extracted.wl"
OUTPUT_MANIFEST = OUTPUT_DIR / "Flow_mendeley_extraction_manifest.json"

EXPECTED_SOURCE_HASH = "f09336e2251df69401cddca2639614eea37dfea9e12ee684f7fb8dc06269d52f"
MARKER = "MTS_4933_C3_NOTEBOOK_BOX_EXTRACTION"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def extract_boxdata_cells(text: str) -> list[dict[str, Any]]:
    cells: list[dict[str, Any]] = []
    cursor = 0
    needle = "Cell[BoxData["
    while True:
        cell_start = text.find(needle, cursor)
        if cell_start < 0:
            break
        box_start = cell_start + len("Cell[")
        index = box_start
        depth = 0
        in_string = False
        escaped = False
        while index < len(text):
            character = text[index]
            if in_string:
                if escaped:
                    escaped = False
                elif character == "\\":
                    escaped = True
                elif character == '"':
                    in_string = False
            else:
                if character == '"':
                    in_string = True
                elif character == "[":
                    depth += 1
                elif character == "]":
                    depth -= 1
                    if depth == 0:
                        tail = text[index + 1 : index + 200]
                        style_match = re.match(r"\s*,\s*\"(Input|Output)\"", tail)
                        if style_match is None:
                            raise ValueError(f"could not identify cell style at offset {index}")
                        cells.append(
                            {
                                "source": text[box_start : index + 1],
                                "style": style_match.group(1),
                                "offset": box_start,
                            }
                        )
                        cursor = index + 1
                        break
            index += 1
        else:
            raise ValueError(f"unterminated BoxData expression at offset {box_start}")
    return cells


def main() -> int:
    source_hash = digest(SOURCE)
    if source_hash != EXPECTED_SOURCE_HASH:
        raise RuntimeError(f"source hash mismatch: {source_hash}")

    text = SOURCE.read_text(encoding="utf-8")
    cells = extract_boxdata_cells(text)
    definitions = Definitions(add_builtin=False)
    unhandled: set[str] = set()
    input_cells: list[str] = []
    output_cells: list[str] = []
    failures: list[dict[str, Any]] = []

    for index, cell in enumerate(cells, start=1):
        try:
            parsed = parse_boxdata(cell["source"], definitions)
            converted = box_to_wl(parsed, unhandled).strip()
            target = input_cells if cell["style"] == "Input" else output_cells
            target.append(f"(* {cell['style'].upper()}_CELL_{index:02d} *)\n{converted}\n")
        except Exception as error:
            failures.append(
                {
                    "cell": index,
                    "style": cell["style"],
                    "offset": cell["offset"],
                    "error": f"{type(error).__name__}: {error}",
                }
            )

    if failures:
        raise RuntimeError(f"C3 BoxData conversion failed: {failures}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    header = (
        f"(* {MARKER} *)\n"
        f"(* Source SHA256: {source_hash} *)\n"
        "(* Mechanical BoxData extraction; no evaluation performed. *)\n\n"
    )
    safe_input_cells = []
    for cell in input_cells:
        if re.search(r"\nQuit\s*$", cell):
            safe_input_cells.append(cell.replace("\nQuit\n", "\n(* Quit suppressed by extractor *)\n"))
        else:
            safe_input_cells.append(cell)
    OUTPUT_INPUT.write_text(header + "\n".join(safe_input_cells), encoding="utf-8")
    OUTPUT_OUTPUT.write_text(header + "\n".join(output_cells), encoding="utf-8")

    manifest = {
        "marker": MARKER,
        "source": SOURCE.relative_to(ROOT).as_posix(),
        "source_sha256": source_hash,
        "input_output": OUTPUT_INPUT.relative_to(ROOT).as_posix(),
        "input_output_sha256": digest(OUTPUT_INPUT),
        "stored_output": OUTPUT_OUTPUT.relative_to(ROOT).as_posix(),
        "stored_output_sha256": digest(OUTPUT_OUTPUT),
        "boxdata_cells_found": len(cells),
        "input_cells": len(input_cells),
        "output_cells": len(output_cells),
        "unhandled_box_heads": sorted(name for name in unhandled if name),
        "parse_failures": failures,
        "evaluated": False,
    }
    OUTPUT_MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print("MTS_4933_C3_NOTEBOOK_BOX_EXTRACTION_PASS")
    print(f"cells={len(cells)}; input={len(input_cells)}; output={len(output_cells)}")
    print(f"unhandled={sorted(unhandled)}")
    print(f"input_sha256={manifest['input_output_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
