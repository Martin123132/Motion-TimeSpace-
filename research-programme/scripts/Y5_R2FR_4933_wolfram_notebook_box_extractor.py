from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

from mathics.core.definitions import Definitions
from mathics.core.parser import MathicsSingleLineFeeder, parse


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4932" / "RHS_general_regulator.nb"
OUTPUT_DIR = POST / "source-intake" / "functional_rg" / "4933"
OUTPUT_WL = OUTPUT_DIR / "RHS_general_regulator_extracted.wl"
OUTPUT_MANIFEST = OUTPUT_DIR / "RHS_general_regulator_extraction_manifest.json"

EXPECTED_SOURCE_HASH = "ec639eaddcfa2d5b642b96c556159c07c2a20e9f3b271670483bef6f7d30b65a"
MARKER = "MTS_4933_WOLFRAM_NOTEBOOK_BOX_EXTRACTION"


TOKEN_MAP = {
    "\\[IndentingNewLine]": "\n",
    "\\[Rule]": "->",
    "\\[RuleDelayed]": ":>",
    "\\[Equal]": "==",
    "\\[NotEqual]": "!=",
    "\\[LessEqual]": "<=",
    "\\[GreaterEqual]": ">=",
    "\\[And]": "&&",
    "\\[Or]": "||",
    "\\[Pi]": "Pi",
    "\\[Infinity]": "Infinity",
    "\\[ImaginaryI]": "I",
    "\\[ExponentialE]": "E",
    "\\[CenterDot]": "*",
    "\\[InvisibleTimes]": "*",
    "\\[Times]": "*",
    "WLIndentingNewLine": "\n",
    "WLRule": "->",
    "WLRuleDelayed": ":>",
    "WLEqual": "==",
    "WLNotEqual": "!=",
    "WLLessEqual": "<=",
    "WLGreaterEqual": ">=",
    "WLAnd": "&&",
    "WLOr": "||",
    "WLPi": "Pi",
    "WLInfinity": "Infinity",
    "WLImaginaryI": "I",
    "WLExponentialE": "E",
    "WLCenterDot": "*",
    "WLInvisibleTimes": "*",
    "WLTimes": "*",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def extract_boxdata_expressions(text: str) -> list[str]:
    expressions: list[str] = []
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
                        expressions.append(text[box_start : index + 1])
                        cursor = index + 1
                        break
            index += 1
        else:
            raise ValueError(f"unterminated BoxData expression at offset {box_start}")
    return expressions


def head_name(expression: Any) -> str:
    head = getattr(expression, "head", None)
    if head is None:
        return ""
    name = getattr(head, "name", str(head))
    return str(name).split("`")[-1]


def symbol_name(expression: Any) -> str:
    name = str(getattr(expression, "name", expression))
    return name.split("`")[-1]


def token_text(value: str) -> str:
    if value in TOKEN_MAP:
        return TOKEN_MAP[value]
    return value


def list_elements(expression: Any) -> tuple[Any, ...]:
    if head_name(expression) != "List":
        raise TypeError(f"expected List, found {expression!r}")
    return tuple(expression.elements)


def is_left_operand(text: str) -> bool:
    stripped = text.rstrip()
    return bool(stripped) and (stripped[-1].isalnum() or stripped[-1] in "_)]}")


def is_right_operand(text: str) -> bool:
    stripped = text.lstrip()
    return bool(stripped) and (stripped[0].isalnum() or stripped[0] in "_({")


def join_row_box(parts: list[str]) -> str:
    output = ""
    pending_space = False
    for part in parts:
        if part == "":
            continue
        if part == " ":
            pending_space = True
            continue
        if part == "\n":
            output = output.rstrip() + "\n"
            pending_space = False
            continue
        if output and is_left_operand(output) and is_right_operand(part):
            output += "*"
        elif pending_space and output and not output.endswith(("\n", " ")):
            output += " "
        output += part
        pending_space = False
    return output


def box_to_wl(expression: Any, unhandled: set[str]) -> str:
    name = head_name(expression)

    if not name and hasattr(expression, "value") and getattr(expression, "value", None) is not None:
        value = expression.value
        if isinstance(value, str):
            return token_text(value)
        return str(value)

    if not name and getattr(expression, "name", None) is not None:
        return symbol_name(expression)

    elements = tuple(getattr(expression, "elements", ()))

    if name == "BoxData":
        return box_to_wl(elements[0], unhandled)
    if name == "List":
        return "\n".join(box_to_wl(element, unhandled) for element in elements)
    if name == "RowBox":
        return join_row_box([box_to_wl(element, unhandled) for element in list_elements(elements[0])])
    if name == "InterpretationBox":
        return box_to_wl(elements[1], unhandled)
    if name in {
        "StyleBox",
        "TagBox",
        "FormBox",
        "TooltipBox",
        "ButtonBox",
        "PaneBox",
        "FrameBox",
    }:
        return box_to_wl(elements[0], unhandled)
    if name == "FractionBox":
        return f"(({box_to_wl(elements[0], unhandled)})/({box_to_wl(elements[1], unhandled)}))"
    if name == "SuperscriptBox":
        base = box_to_wl(elements[0], unhandled)
        exponent_box = elements[1]
        if head_name(exponent_box) == "TagBox" and len(exponent_box.elements) >= 2:
            tag = symbol_name(exponent_box.elements[1])
            if tag == "Derivative":
                orders = box_to_wl(exponent_box.elements[0], unhandled).strip()
                if orders.startswith("(") and orders.endswith(")"):
                    orders = orders[1:-1]
                return f"Derivative[{orders}][{base}]"
        exponent = box_to_wl(elements[1], unhandled)
        if exponent in {"\\[Prime]", "WLPrime"}:
            return f"Derivative[1][{base}]"
        if exponent in {"\\[Prime]\\[Prime]", "WLPrimeWLPrime"}:
            return f"Derivative[2][{base}]"
        return f"(({base})^({exponent}))"
    if name == "SubscriptBox":
        return f"Subscript[{box_to_wl(elements[0], unhandled)},{box_to_wl(elements[1], unhandled)}]"
    if name == "SubsuperscriptBox":
        return (
            f"Subsuperscript[{box_to_wl(elements[0], unhandled)},"
            f"{box_to_wl(elements[1], unhandled)},{box_to_wl(elements[2], unhandled)}]"
        )
    if name == "SqrtBox":
        return f"Sqrt[{box_to_wl(elements[0], unhandled)}]"
    if name == "RadicalBox":
        return f"({box_to_wl(elements[0], unhandled)})^(1/({box_to_wl(elements[1], unhandled)}))"
    if name == "OverscriptBox":
        return f"Overscript[{box_to_wl(elements[0], unhandled)},{box_to_wl(elements[1], unhandled)}]"
    if name == "UnderscriptBox":
        return f"Underscript[{box_to_wl(elements[0], unhandled)},{box_to_wl(elements[1], unhandled)}]"
    if name == "UnderoverscriptBox":
        return (
            f"Underoverscript[{box_to_wl(elements[0], unhandled)},"
            f"{box_to_wl(elements[1], unhandled)},{box_to_wl(elements[2], unhandled)}]"
        )
    if name == "TemplateBox":
        unhandled.add(name)
        return f"TemplateBox[{','.join(box_to_wl(element, unhandled) for element in elements)}]"
    if name == "GridBox":
        unhandled.add(name)
        return f"GridBox[{','.join(box_to_wl(element, unhandled) for element in elements)}]"
    if name in {"Rule", "RuleDelayed"}:
        operator = "->" if name == "Rule" else ":>"
        return f"{box_to_wl(elements[0], unhandled)}{operator}{box_to_wl(elements[1], unhandled)}"

    unhandled.add(name)
    converted = ",".join(box_to_wl(element, unhandled) for element in elements)
    return f"{name}[{converted}]"


def parse_boxdata(source: str, definitions: Definitions) -> Any:
    normalized = source.replace("$CellContext`", "Global`")
    normalized = normalized.replace("\\<", "").replace("\\>", "")
    normalized = re.sub(r"\\\[([A-Za-z0-9]+)\]", r"WL\1", normalized)
    expression = parse(definitions, MathicsSingleLineFeeder(normalized, None))
    if expression is None:
        raise ValueError("Mathics parser returned no expression")
    return expression


def main() -> int:
    source_hash = digest(SOURCE)
    if source_hash != EXPECTED_SOURCE_HASH:
        raise RuntimeError(f"source hash mismatch: {source_hash}")

    notebook_text = SOURCE.read_text(encoding="utf-8")
    box_sources = extract_boxdata_expressions(notebook_text)
    definitions = Definitions(add_builtin=False)
    unhandled: set[str] = set()
    converted_cells: list[str] = []
    parse_failures: list[dict[str, Any]] = []

    for index, box_source in enumerate(box_sources, start=1):
        try:
            parsed = parse_boxdata(box_source, definitions)
            converted = box_to_wl(parsed, unhandled)
            converted_cells.append(f"(* INPUT_CELL_{index:02d} *)\n{converted.strip()}\n")
        except Exception as error:
            parse_failures.append({"cell": index, "error": f"{type(error).__name__}: {error}"})

    if parse_failures:
        raise RuntimeError(f"BoxData conversion failed: {parse_failures}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    header = (
        f"(* {MARKER} *)\n"
        f"(* Source SHA256: {source_hash} *)\n"
        "(* Mechanical BoxData extraction; no evaluation performed. *)\n\n"
    )
    OUTPUT_WL.write_text(header + "\n".join(converted_cells), encoding="utf-8")

    output_hash = digest(OUTPUT_WL)
    manifest = {
        "marker": MARKER,
        "source": SOURCE.relative_to(ROOT).as_posix(),
        "source_sha256": source_hash,
        "output": OUTPUT_WL.relative_to(ROOT).as_posix(),
        "output_sha256": output_hash,
        "boxdata_cells_found": len(box_sources),
        "boxdata_cells_converted": len(converted_cells),
        "unhandled_box_heads": sorted(name for name in unhandled if name),
        "parse_failures": parse_failures,
        "evaluated": False,
    }
    OUTPUT_MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print("MTS_4933_WOLFRAM_NOTEBOOK_BOX_EXTRACTION_PASS")
    print(f"cells={len(converted_cells)}")
    print(f"unhandled={sorted(unhandled)}")
    print(f"output_sha256={output_hash}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
