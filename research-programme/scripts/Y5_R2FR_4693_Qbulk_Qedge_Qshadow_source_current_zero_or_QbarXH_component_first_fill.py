from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4693"
CLAIM_ID = "L-535"
MARKER = "PPC4161_QBULK_QEDGE_QSHADOW_NUMERATOR_CURRENT_BRANCH_4693"
PACKET_MARKER = "PPC4161_PACKET_QBULK_QEDGE_QSHADOW_NUMERATOR_CURRENT_BRANCH_4693"
DECISION = "SOURCE_NUMERATOR_ZERO_OR_COMPONENT_BOUND_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4694-Y5-R2FR-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md"

DOC_PATH = POST / "4693-Y5-R2FR-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md"
FORMAL_PATH = FORMAL / "709-PPC4161-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4692_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4692_NEXT_TARGET.csv"
CSV_4692_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4692_STATUS.csv"
CSV_4605_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4605_SOURCE_NUMERATOR_THEOREM.csv"
CSV_4605_QBULK = SOURCE_DIR / "P8_Y5_R2FR_4605_QBULK_COMPONENT_ROWS.csv"
CSV_4605_QEDGE = SOURCE_DIR / "P8_Y5_R2FR_4605_QEDGE_COMPONENT_ROWS.csv"
CSV_4605_QSHADOW = SOURCE_DIR / "P8_Y5_R2FR_4605_QSHADOW_COMPONENT_ROWS.csv"
CSV_4605_QBAR = SOURCE_DIR / "P8_Y5_R2FR_4605_QBARXH_NUMERATOR_UPDATE_ROWS.csv"
CSV_4605_PRODUCT = SOURCE_DIR / "P8_Y5_R2FR_4605_IXST_PRODUCT_UPDATE_ROWS.csv"
CSV_4605_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4605_CLAIM_BLOCKERS.csv"
CSV_4605_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4605_CONTROL_ROWS.csv"
CSV_4605_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4605_STATUS.csv"
CSV_4605_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4605_NEXT_TARGET.csv"
CSV_4605_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4605_VALIDATION.csv"
CSV_4606_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4606_STATUS.csv"
CSV_4606_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4606_NEXT_TARGET.csv"
CSV_4606_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4606_VALIDATION.csv"
FORMAL_621 = FORMAL / "621-PPC4161-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md"
FORMAL_622 = FORMAL / "622-PPC4161-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4693_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4693_SOURCE_NUMERATOR_THEOREM.csv"
QBULK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4693_QBULK_COMPONENT_ROWS.csv"
QEDGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4693_QEDGE_COMPONENT_ROWS.csv"
QSHADOW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4693_QSHADOW_COMPONENT_ROWS.csv"
QBAR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4693_QBARXH_NUMERATOR_UPDATE_ROWS.csv"
PRODUCT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4693_IXST_PRODUCT_UPDATE_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4693_CLAIM_BLOCKERS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4693_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4693_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4693_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4693_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4693_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4693_VALIDATION.csv"

NEXT_4605 = "4606-Y5-R2FR-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md"
NEXT_4606 = "4607-Y5-R2FR-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md"


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def line_of(path: Path, needle: str) -> int:
    for index, line in enumerate(text(path).splitlines(), start=1):
        if needle in line:
            return index
    return 0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def table(rows: Iterable[dict[str, Any]]) -> str:
    rows = list(rows)
    if not rows:
        return ""
    headers = list(rows[0].keys())
    output = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        output.append("| " + " | ".join(str(row.get(header, "")).replace("|", "\\|").replace("\n", " ") for header in headers) + " |")
    return "\n".join(output)


def append_once(path: Path, marker: str, body: str) -> None:
    existing = text(path)
    if marker in existing:
        return
    path.write_text(existing.rstrip() + "\n\n" + body.strip() + "\n", encoding="utf-8")


def restamp_rows(path: Path, timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in read_csv(path):
        row: dict[str, Any] = {}
        for key, value in source.items():
            if key in {"source_paths", "path"}:
                new_value = value
            else:
                new_value = (
                    value.replace("4605", CHECKPOINT)
                    .replace(NEXT_4605, NEXT_TARGET)
                    .replace("2026-07-06T15:20:33.767498+00:00", timestamp)
                )
            row[key] = new_value
        row["checkpoint"] = CHECKPOINT
        row["claim_allowed"] = False
        row["valid_for_claim"] = False
        row["timestamp_utc"] = timestamp
        row.pop("generated_utc", None)
        rows.append(row)
    return rows


def source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SRC4693_00_4692_next", CSV_4692_NEXT, "4693-Y5-R2FR-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md", "4692 selected numerator target."),
        ("SRC4693_01_4692_status", CSV_4692_STATUS, "PPC4161_MHREF_PIM_DENOMINATOR_LOCK_CURRENT_BRANCH_4692", "4692 current branch status."),
        ("SRC4693_02_4605_theorem", CSV_4605_THEOREM, "NUM4605_4_absolute_numerator_bound", "4605 source numerator theorem."),
        ("SRC4693_03_4605_qbulk", CSV_4605_QBULK, "QB4605_TOTAL", "4605 Qbulk rows."),
        ("SRC4693_04_4605_qedge", CSV_4605_QEDGE, "QE4605_TOTAL", "4605 Qedge rows."),
        ("SRC4693_05_4605_qshadow", CSV_4605_QSHADOW, "QS4605_TOTAL", "4605 Qshadow rows."),
        ("SRC4693_06_4605_qbar", CSV_4605_QBAR, "QU4605_1_Qbar_insert", "4605 Qbar numerator update."),
        ("SRC4693_07_4605_product", CSV_4605_PRODUCT, "PU4605_1_zero_route", "4605 product update."),
        ("SRC4693_08_4605_blockers", CSV_4605_BLOCKERS, "MIS4605_0_Qbulk", "4605 blockers."),
        ("SRC4693_09_4605_controls", CSV_4605_CONTROLS, "CTRL4605_1_poynting_not_magic", "4605 controls."),
        ("SRC4693_10_4605_status", CSV_4605_STATUS, "SOURCE_NUMERATOR_ZERO_OR_COMPONENT_BOUND_SCHEMA_READY_NONCLAIM", "4605 status."),
        ("SRC4693_11_4605_next", CSV_4605_NEXT, NEXT_4605, "4605 next target."),
        ("SRC4693_12_4605_validation", CSV_4605_VALIDATION, "VAL4605_OVERALL", "4605 validation passed."),
        ("SRC4693_13_4606_status", CSV_4606_STATUS, "QBULK_HILBERT_EM_POYNTING_ZERO_OR_COEFFICIENT_SCHEMA_READY_NONCLAIM", "4606 Qbulk rung exists."),
        ("SRC4693_14_4606_next", CSV_4606_NEXT, NEXT_4606, "4606 next target."),
        ("SRC4693_15_4606_validation", CSV_4606_VALIDATION, "VAL4606_OVERALL", "4606 validation passed."),
        ("SRC4693_16_formal621", FORMAL_621, "Q_tot_XH(lambda)=Q_bulk_XH", "formal numerator split."),
        ("SRC4693_17_formal622", FORMAL_622, "Q_bulk = Q_bulk_Hilbert", "formal Qbulk handoff."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "line_number": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    data = [
        ("SURV4693_0_numerator", "Q_tot_XH_abs", "bulk/edge/shadow numerator envelope imported", NEXT_TARGET),
        ("SURV4693_1_bulk", "Q_bulk_abs", "dominant source-current route; includes Hilbert, EM/Poynting and retained tails", NEXT_TARGET),
        ("SURV4693_2_edge", "Q_edge_abs", "Reynolds shell and boundary/corner/reference pieces remain explicit", "return after Qbulk"),
        ("SURV4693_3_shadow", "Q_shadow_abs", "action/projector/nonvariational source-shadow pieces remain explicit", "return after Qbulk/edge"),
        ("SURV4693_4_product", "I_X^ST", "product now uses numerator envelope under MHref/PiM lock", "defer empirical score until factors are live"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "status_after_4693": status,
            "next_action": action,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for survivor_id, family, status, action in data
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision": DECISION,
            "summary": "4693 imports the Q_bulk/Q_edge/Q_shadow numerator split into the current branch. Source charge is now a concrete component envelope, with Poynting/EM placed inside the bulk Hilbert-stress route rather than treated as a loose background source. The next target is the Q_bulk Hilbert/EM/Poynting coefficient row.",
            "next_target": NEXT_TARGET,
            "public_claim": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "Q_tot numerator split; bulk Hilbert/EM/Poynting/retained component rows; edge Reynolds/boundary component rows; shadow action/projector/nonvariational component rows; Qbar/I_X^ST numerator updates",
            "not_derived": "numeric Q_bulk/Q_edge/Q_shadow values; same-branch bulk/edge/shadow zero theorem; Qbulk Hilbert/EM/Poynting coefficient values; R10/PPN/local-GR pass",
            "claim_status": "PRIVATE_NONCLAIM",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4693_0",
            "target": NEXT_TARGET,
            "reason": "Q_bulk is the largest and most physical numerator route, and it contains the Hilbert/EM/Poynting source-current question.",
            "derive_first": "prove Q_bulk_Hilbert and Q_bulk_EM_Poynting vanish under one q-basic source functor/no-flux branch",
            "fallback": "fill Q_bulk_Hilbert_abs, Q_bulk_EM_Poynting_abs and Q_bulk_retained_abs as nonclaim coefficient rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4693 - Y5/R2FR Qbulk/Qedge/Qshadow Source-Current Zero Or QbarXH Component First Fill

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4693 imports the source-side numerator split:

```text
Q_tot_XH(lambda)=Q_bulk_XH(lambda)+Q_edge_XH(lambda)+Q_shadow_XH(lambda)
```

Strict zero route:

```text
Q_bulk=Q_edge=Q_shadow=0 => Q_tot_XH=0.
```

Bound route:

```text
|Q_tot_XH| <= |Q_bulk|_abs + |Q_edge|_abs + |Q_shadow|_abs
|Qbar_XH| <= (||Pi_M^H|| Q_tot_XH_abs + |E_PiM_comm|)/M_lower.
```

The important physics bookkeeping is that EM/Poynting is inside the bulk source-current problem: it is either once-only Hilbert EM stress with no wall flux, or it becomes an explicit coefficient row.

## Source Register

{table(rows["sources"])}

## Source Numerator Theorem

{table(rows["theorems"])}

## Qbulk Component Rows

{table(rows["qbulk"])}

## Qedge Component Rows

{table(rows["qedge"])}

## Qshadow Component Rows

{table(rows["qshadow"])}

## QbarXH Numerator Update Rows

{table(rows["qbar"])}

## I_X^ST Product Update Rows

{table(rows["products"])}

## Claim Blockers

{table(rows["blockers"])}

## Survivor Update

{table(rows["survivors"])}

## Controls

{table(rows["controls"])}

## Decision

{table(rows["decisions"])}

## Status

{table(rows["statuses"])}

## Next Target

{table(rows["next"])}

## Validation

{table(rows.get("validations", []))}
"""
    DOC_PATH.write_text(body, encoding="utf-8")
    FORMAL_PATH.write_text(body.replace("# 4693 - Y5/R2FR", "# 709 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4693 imports the Q_bulk/Q_edge/Q_shadow source numerator split and its Qbar/I_X^ST updates, with EM/Poynting tracked inside the bulk Hilbert-stress route.",
                "current_evidence": "Generated source register, numerator theorem, Qbulk/Qedge/Qshadow component rows, Qbar update, product update, blockers, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Letting bulk, edge, shadow, EM/Poynting or source-worldtube terms cancel or hide as a source RHS knob.",
                "sector": "local_gr",
                "evidence": str(DOC_PATH),
                "next_action": NEXT_TARGET,
            }
        )
        with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=fieldnames)
            writer.writerow(row)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""## Local GR Parent-Derivation Update - Current Source Numerator Split

Marker: `{MARKER}`

4693 decomposes the source numerator:

```text
Q_tot_XH=Q_bulk_XH+Q_edge_XH+Q_shadow_XH.
```

Poynting/EM is now forced through the bulk Hilbert-stress/no-wall-flux route or into a named coefficient row. It is no longer a loose background-field phrase.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current Source Numerator Split

Marker: `{PACKET_MARKER}`

The packet now carries `Q_tot_XH_abs = Q_bulk_abs + Q_edge_abs + Q_shadow_abs` under the 4692 MHref/PiM lock. No cancellation between numerator channels is allowed.

- Qbulk csv: `{QBULK_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4693_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4693_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4693_2_numerator_split", any(row.get("theorem_id") == "NUM4693_0_decomposition" for row in rows["theorems"]), "numerator split present"),
        ("VAL4693_3_poynting_in_bulk", any(row.get("component") == "Q_bulk_EM_Poynting" for row in rows["qbulk"]), "EM/Poynting routed through bulk"),
        ("VAL4693_4_edge_shadow_rows", any(row.get("component") == "Q_edge_abs" for row in rows["qedge"]) and any(row.get("component") == "Q_shadow_abs" for row in rows["qshadow"]), "edge and shadow component totals present"),
        ("VAL4693_5_qbar_update", any(row.get("quantity") == "Qbar_XH_abs" for row in rows["qbar"]), "Qbar numerator update present"),
        ("VAL4693_6_next_qbulk", rows["next"][0]["target"] == NEXT_TARGET, "next Qbulk target selected"),
        ("VAL4693_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-535"),
        ("VAL4693_8_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4693_9_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4693_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4693_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4693_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4693_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4693_12_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4693_13_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4693_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "theorems": restamp_rows(CSV_4605_THEOREM, timestamp),
        "qbulk": restamp_rows(CSV_4605_QBULK, timestamp),
        "qedge": restamp_rows(CSV_4605_QEDGE, timestamp),
        "qshadow": restamp_rows(CSV_4605_QSHADOW, timestamp),
        "qbar": restamp_rows(CSV_4605_QBAR, timestamp),
        "products": restamp_rows(CSV_4605_PRODUCT, timestamp),
        "blockers": restamp_rows(CSV_4605_BLOCKERS, timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": restamp_rows(CSV_4605_CONTROLS, timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        THEOREM_CSV: rows["theorems"],
        QBULK_CSV: rows["qbulk"],
        QEDGE_CSV: rows["qedge"],
        QSHADOW_CSV: rows["qshadow"],
        QBAR_CSV: rows["qbar"],
        PRODUCT_CSV: rows["products"],
        BLOCKERS_CSV: rows["blockers"],
        SURVIVOR_CSV: rows["survivors"],
        CONTROL_CSV: rows["controls"],
        DECISION_CSV: rows["decisions"],
        STATUS_CSV: rows["statuses"],
        NEXT_CSV: rows["next"],
    }
    for path, data in csv_map.items():
        write_csv(path, data)
    write_documents(rows)
    update_registers(timestamp)
    cache = POST / "scripts" / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)
    rows["validations"] = validation_rows(rows, list(csv_map))
    write_csv(VALIDATION_CSV, rows["validations"])
    write_documents(rows)
    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
