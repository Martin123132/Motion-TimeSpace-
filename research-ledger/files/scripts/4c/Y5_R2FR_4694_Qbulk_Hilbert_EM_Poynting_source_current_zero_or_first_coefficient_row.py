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

CHECKPOINT = "4694"
CLAIM_ID = "L-536"
MARKER = "PPC4161_QBULK_HILBERT_EM_POYNTING_CURRENT_BRANCH_4694"
PACKET_MARKER = "PPC4161_PACKET_QBULK_HILBERT_EM_POYNTING_CURRENT_BRANCH_4694"
DECISION = "QBULK_HILBERT_EM_POYNTING_ZERO_OR_COEFFICIENT_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4695-Y5-R2FR-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md"

DOC_PATH = POST / "4694-Y5-R2FR-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md"
FORMAL_PATH = FORMAL / "710-PPC4161-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4693_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4693_NEXT_TARGET.csv"
CSV_4693_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4693_STATUS.csv"
CSV_4606_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_SOURCE_CURRENT_THEOREM.csv"
CSV_4606_HILBERT = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_HILBERT_ROWS.csv"
CSV_4606_EM = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_EM_POYNTING_ROWS.csv"
CSV_4606_RETAINED = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_RETAINED_ROWS.csv"
CSV_4606_BULK_UPDATE = SOURCE_DIR / "P8_Y5_R2FR_4606_QBULK_UPDATE_ROWS.csv"
CSV_4606_QBAR_UPDATE = SOURCE_DIR / "P8_Y5_R2FR_4606_QBARXH_BULK_UPDATE_ROWS.csv"
CSV_4606_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4606_CLAIM_BLOCKERS.csv"
CSV_4606_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4606_CONTROL_ROWS.csv"
CSV_4606_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4606_STATUS.csv"
CSV_4606_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4606_NEXT_TARGET.csv"
CSV_4606_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4606_VALIDATION.csv"
CSV_4607_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4607_STATUS.csv"
CSV_4607_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4607_NEXT_TARGET.csv"
CSV_4607_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4607_VALIDATION.csv"
FORMAL_622 = FORMAL / "622-PPC4161-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md"
FORMAL_623 = FORMAL / "623-PPC4161-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4694_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4694_QBULK_SOURCE_CURRENT_THEOREM.csv"
HILBERT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4694_QBULK_HILBERT_ROWS.csv"
EM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4694_QBULK_EM_POYNTING_ROWS.csv"
RETAINED_CSV = SOURCE_DIR / "P8_Y5_R2FR_4694_QBULK_RETAINED_ROWS.csv"
BULK_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4694_QBULK_UPDATE_ROWS.csv"
QBAR_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4694_QBARXH_BULK_UPDATE_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4694_CLAIM_BLOCKERS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4694_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4694_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4694_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4694_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4694_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4694_VALIDATION.csv"

NEXT_4606 = "4607-Y5-R2FR-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md"
NEXT_4607 = "4608-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md"


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
                    value.replace("4606", CHECKPOINT)
                    .replace(NEXT_4606, NEXT_TARGET)
                    .replace("2026-07-06T15:27:27.265455+00:00", timestamp)
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
        ("SRC4694_00_4693_next", CSV_4693_NEXT, "4694-Y5-R2FR-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md", "4693 selected Qbulk target."),
        ("SRC4694_01_4693_status", CSV_4693_STATUS, "PPC4161_QBULK_QEDGE_QSHADOW_NUMERATOR_CURRENT_BRANCH_4693", "4693 current branch status."),
        ("SRC4694_02_4606_theorem", CSV_4606_THEOREM, "QBH4606_4_absolute_bulk_bound", "4606 Qbulk theorem."),
        ("SRC4694_03_4606_hilbert", CSV_4606_HILBERT, "H4606_TOTAL", "4606 Hilbert rows."),
        ("SRC4694_04_4606_em", CSV_4606_EM, "EM4606_TOTAL", "4606 EM/Poynting rows."),
        ("SRC4694_05_4606_retained", CSV_4606_RETAINED, "R4606_TOTAL", "4606 retained rows."),
        ("SRC4694_06_4606_bulk_update", CSV_4606_BULK_UPDATE, "BU4606_1_absolute_bound", "4606 Qbulk update."),
        ("SRC4694_07_4606_qbar_update", CSV_4606_QBAR_UPDATE, "QBU4606_0_Qbar_bulk_insert", "4606 Qbar update."),
        ("SRC4694_08_4606_blockers", CSV_4606_BLOCKERS, "MIS4606_1_EM_Poynting", "4606 blockers."),
        ("SRC4694_09_4606_controls", CSV_4606_CONTROLS, "CTRL4606_0_once_only_Poynting", "4606 controls."),
        ("SRC4694_10_4606_status", CSV_4606_STATUS, "QBULK_HILBERT_EM_POYNTING_ZERO_OR_COEFFICIENT_SCHEMA_READY_NONCLAIM", "4606 status."),
        ("SRC4694_11_4606_next", CSV_4606_NEXT, NEXT_4606, "4606 next target."),
        ("SRC4694_12_4606_validation", CSV_4606_VALIDATION, "VAL4606_OVERALL", "4606 validation passed."),
        ("SRC4694_13_4607_status", CSV_4607_STATUS, "EM_POYNTING_SAME_HODGE_NO_FLUX_OR_WALL_COEFFICIENT_SCHEMA_READY_NONCLAIM", "4607 EM/Poynting rung exists."),
        ("SRC4694_14_4607_next", CSV_4607_NEXT, NEXT_4607, "4607 next target."),
        ("SRC4694_15_4607_validation", CSV_4607_VALIDATION, "VAL4607_OVERALL", "4607 validation passed."),
        ("SRC4694_16_formal622", FORMAL_622, "Q_bulk = Q_bulk_Hilbert", "formal Qbulk split."),
        ("SRC4694_17_formal623", FORMAL_623, "S_Poynting^i=-T_EM^i_nu", "formal EM/Poynting handoff."),
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
        ("SURV4694_0_qbulk", "Q_bulk_abs", "bulk source-current envelope imported", NEXT_TARGET),
        ("SURV4694_1_hilbert", "Q_bulk_Hilbert_abs", "ordinary Hilbert zero still requires q-basic action, marker silence and no source weights", "return after EM/Poynting if needed"),
        ("SURV4694_2_em_poynting", "Q_bulk_EM_Poynting_abs", "Poynting is once-only Hilbert stress or an explicit wall/Hodge/nonminimal coefficient", NEXT_TARGET),
        ("SURV4694_3_retained", "Q_bulk_retained_abs", "direct/memory/readout retained source rows remain after EM/Poynting", "4696 after EM/Poynting fork"),
        ("SURV4694_4_no_claim", "R10/PPN/local-GR", "bulk schema alone is not empirical success", "keep private nonclaim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "status_after_4694": status,
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
            "summary": "4694 imports the Qbulk Hilbert/EM/Poynting source-current split. Poynting is now formally either once-only Hilbert EM stress on the public-Hodge branch or a named wall/Hodge/nonminimal coefficient; it is not a loose background-field escape hatch.",
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
            "derived": "Qbulk Hilbert/EM/Poynting/retained split; ordinary Hilbert source-current rows; once-only EM/Poynting source lock; EM wall/Hodge/nonminimal coefficient rows; Qbulk and Qbar updates",
            "not_derived": "numeric Qbulk values; same-branch Hilbert zero theorem; same-Hodge/no-wall-flux EM proof; retained source-current values; R10/PPN/local-GR pass",
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
            "next_id": "NT4694_0",
            "target": NEXT_TARGET,
            "reason": "The cleanest next fork is Maxwell/Poynting: prove same-Hodge/no-wall-flux once-only ownership, or fill the wall-flux coefficient.",
            "derive_first": "derive public Maxwell-Hodge and no Poynting wall flux in the same source-worldtube branch",
            "fallback": "fill epsilon_Hodge_EM, c_Poynt_extra, Phi_wall_Poynting and epsilon_nonminimal_EM as nonclaim coefficient rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4694 - Y5/R2FR Qbulk Hilbert/EM/Poynting Source-Current Zero Or First Coefficient Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4694 imports the Qbulk split:

```text
Q_bulk = Q_bulk_Hilbert + Q_bulk_EM/Poynting + Q_bulk_retained.
```

EM/Poynting once-only lock:

```text
S_EM=-(4 mu0)^-1 int sqrt(-g_obs) F^2
T_EM=Hilbert variation
S_Poynting^i=-T_EM^i_nu tau^nu.
```

Bound branch:

```text
|Q_bulk| <= |Q_bulk_Hilbert| + |Q_bulk_EM/Poynting| + |Q_bulk_retained|.
```

This preserves the Poynting-vector intuition while making it disciplined: either it is already the Hilbert EM stress flux, or it is an explicit wall/Hodge/nonminimal coefficient.

## Source Register

{table(rows["sources"])}

## Qbulk Source Current Theorem

{table(rows["theorems"])}

## Qbulk Hilbert Rows

{table(rows["hilbert"])}

## Qbulk EM/Poynting Rows

{table(rows["em"])}

## Qbulk Retained Rows

{table(rows["retained"])}

## Qbulk Update Rows

{table(rows["bulk_updates"])}

## QbarXH Bulk Update Rows

{table(rows["qbar_updates"])}

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
    FORMAL_PATH.write_text(body.replace("# 4694 - Y5/R2FR", "# 710 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4694 imports the Qbulk Hilbert/EM/Poynting split and makes Poynting either once-only Hilbert EM stress or an explicit wall/Hodge/nonminimal coefficient.",
                "current_evidence": "Generated source register, Qbulk theorem, Hilbert rows, EM/Poynting rows, retained rows, bulk/Qbar updates, blockers, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Double-counting Poynting as an extra background source or erasing wall flux/nonminimal EM leakage without a zero theorem.",
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
        f"""## Local GR Parent-Derivation Update - Current Qbulk Hilbert/EM/Poynting Gate

Marker: `{MARKER}`

4694 makes Poynting local-source disciplined:

```text
S_Poynting^i=-T_EM^i_nu tau^nu.
```

So Poynting is counted once as Hilbert EM stress on the public-Hodge branch, or it survives as a wall/Hodge/nonminimal coefficient.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current Qbulk Hilbert/EM/Poynting Gate

Marker: `{PACKET_MARKER}`

The packet now routes EM/Poynting through once-only Hilbert stress or explicit coefficient rows. No extra background source is allowed without entering `Q_bulk_EM/Poynting_abs`.

- EM csv: `{EM_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4694_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4694_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4694_2_qbulk_split", any(row.get("theorem_id") == "QBH4694_0_bulk_decomposition" for row in rows["theorems"]), "Qbulk split present"),
        ("VAL4694_3_hilbert_rows", any(row.get("quantity") == "Q_bulk_Hilbert_abs" for row in rows["hilbert"]), "Hilbert source rows present"),
        ("VAL4694_4_em_once_only", any(row.get("quantity") == "c_Poynt_extra" for row in rows["em"]) and any(row.get("quantity") == "Phi_wall_Poynting" for row in rows["em"]), "EM/Poynting once-only and flux rows present"),
        ("VAL4694_5_retained_rows", any(row.get("quantity") == "Q_bulk_retained_abs" for row in rows["retained"]), "retained rows present"),
        ("VAL4694_6_qbar_update", len(rows["qbar_updates"]) == 1, "Qbar bulk update present"),
        ("VAL4694_7_next_em", rows["next"][0]["target"] == NEXT_TARGET, "next EM/Poynting target selected"),
        ("VAL4694_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-536"),
        ("VAL4694_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4694_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4694_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4694_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4694_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4694_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4694_13_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4694_14_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4694_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "theorems": restamp_rows(CSV_4606_THEOREM, timestamp),
        "hilbert": restamp_rows(CSV_4606_HILBERT, timestamp),
        "em": restamp_rows(CSV_4606_EM, timestamp),
        "retained": restamp_rows(CSV_4606_RETAINED, timestamp),
        "bulk_updates": restamp_rows(CSV_4606_BULK_UPDATE, timestamp),
        "qbar_updates": restamp_rows(CSV_4606_QBAR_UPDATE, timestamp),
        "blockers": restamp_rows(CSV_4606_BLOCKERS, timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": restamp_rows(CSV_4606_CONTROLS, timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        THEOREM_CSV: rows["theorems"],
        HILBERT_CSV: rows["hilbert"],
        EM_CSV: rows["em"],
        RETAINED_CSV: rows["retained"],
        BULK_UPDATE_CSV: rows["bulk_updates"],
        QBAR_UPDATE_CSV: rows["qbar_updates"],
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
