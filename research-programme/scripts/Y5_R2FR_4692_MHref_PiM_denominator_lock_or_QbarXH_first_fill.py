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

CHECKPOINT = "4692"
CLAIM_ID = "L-534"
MARKER = "PPC4161_MHREF_PIM_DENOMINATOR_LOCK_CURRENT_BRANCH_4692"
PACKET_MARKER = "PPC4161_PACKET_MHREF_PIM_DENOMINATOR_LOCK_CURRENT_BRANCH_4692"
DECISION = "MHREF_PIM_LOCK_THEOREM_AND_QBARXH_BOUND_ROW_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4693-Y5-R2FR-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md"

DOC_PATH = POST / "4692-Y5-R2FR-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md"
FORMAL_PATH = FORMAL / "708-PPC4161-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4691_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4691_NEXT_TARGET.csv"
CSV_4691_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4691_STATUS.csv"
CSV_4604_MHREF_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4604_MHREF_DENOMINATOR_THEOREM.csv"
CSV_4604_PIM_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4604_PIM_PROJECTOR_THEOREM.csv"
CSV_4604_MHREF_INPUTS = SOURCE_DIR / "P8_Y5_R2FR_4604_MHREF_DENOMINATOR_INPUT_ROWS.csv"
CSV_4604_PIM_INPUTS = SOURCE_DIR / "P8_Y5_R2FR_4604_PIM_PROJECTOR_INPUT_ROWS.csv"
CSV_4604_QBAR = SOURCE_DIR / "P8_Y5_R2FR_4604_QBARXH_FIRST_FILL_ROWS.csv"
CSV_4604_PRODUCT = SOURCE_DIR / "P8_Y5_R2FR_4604_IXST_PRODUCT_UPDATE_ROWS.csv"
CSV_4604_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4604_CLAIM_BLOCKERS.csv"
CSV_4604_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4604_CONTROL_ROWS.csv"
CSV_4604_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4604_STATUS.csv"
CSV_4604_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4604_NEXT_TARGET.csv"
CSV_4604_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4604_VALIDATION.csv"
CSV_4605_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4605_STATUS.csv"
CSV_4605_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4605_NEXT_TARGET.csv"
CSV_4605_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4605_VALIDATION.csv"
FORMAL_620 = FORMAL / "620-PPC4161-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md"
FORMAL_621 = FORMAL / "621-PPC4161-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4692_SOURCE_REGISTER.csv"
MHREF_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4692_MHREF_DENOMINATOR_THEOREM.csv"
PIM_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4692_PIM_PROJECTOR_THEOREM.csv"
MHREF_INPUTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4692_MHREF_DENOMINATOR_INPUT_ROWS.csv"
PIM_INPUTS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4692_PIM_PROJECTOR_INPUT_ROWS.csv"
QBAR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4692_QBARXH_FIRST_FILL_ROWS.csv"
PRODUCT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4692_IXST_PRODUCT_UPDATE_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4692_CLAIM_BLOCKERS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4692_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4692_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4692_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4692_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4692_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4692_VALIDATION.csv"

NEXT_4604 = "4605-Y5-R2FR-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md"
NEXT_4605 = "4606-Y5-R2FR-Qbulk-Hilbert-EM-Poynting-source-current-zero-or-first-coefficient-row.md"


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
                    value.replace("4604", CHECKPOINT)
                    .replace(NEXT_4604, NEXT_TARGET)
                    .replace("2026-07-06T15:12:08.627246+00:00", timestamp)
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
        ("SRC4692_00_4691_next", CSV_4691_NEXT, "4692-Y5-R2FR-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md", "4691 selected denominator/projector target."),
        ("SRC4692_01_4691_status", CSV_4691_STATUS, "PPC4161_SOURCE_TEST_INVARIANT_PRODUCT_CURRENT_BRANCH_4691", "4691 current branch status."),
        ("SRC4692_02_4604_mhref_theorem", CSV_4604_MHREF_THEOREM, "MHR4604_3_denominator_drift_bound", "4604 MHref theorem."),
        ("SRC4692_03_4604_pim_theorem", CSV_4604_PIM_THEOREM, "PIM4604_2_projector_commutator_bound", "4604 PiM theorem."),
        ("SRC4692_04_4604_mhref_inputs", CSV_4604_MHREF_INPUTS, "MD4604_2_M_lower", "4604 denominator input rows."),
        ("SRC4692_05_4604_pim_inputs", CSV_4604_PIM_INPUTS, "PM4604_2_commutator", "4604 projector input rows."),
        ("SRC4692_06_4604_qbar", CSV_4604_QBAR, "QF4604_1_absolute_Qbar_bound", "4604 QbarXH first fill rows."),
        ("SRC4692_07_4604_product", CSV_4604_PRODUCT, "PU4604_1_alpha_update", "4604 product update rows."),
        ("SRC4692_08_4604_blockers", CSV_4604_BLOCKERS, "MIS4604_2_Q_components", "4604 blockers."),
        ("SRC4692_09_4604_controls", CSV_4604_CONTROLS, "CTRL4604_2_no_GM_backfill", "4604 controls."),
        ("SRC4692_10_4604_status", CSV_4604_STATUS, "MHREF_PIM_LOCK_THEOREM_AND_QBARXH_BOUND_ROW_READY_NONCLAIM", "4604 status."),
        ("SRC4692_11_4604_next", CSV_4604_NEXT, NEXT_4604, "4604 next target."),
        ("SRC4692_12_4604_validation", CSV_4604_VALIDATION, "VAL4604_OVERALL", "4604 validation passed."),
        ("SRC4692_13_4605_status", CSV_4605_STATUS, "SOURCE_NUMERATOR_ZERO_OR_COMPONENT_BOUND_SCHEMA_READY_NONCLAIM", "4605 numerator rung exists."),
        ("SRC4692_14_4605_next", CSV_4605_NEXT, NEXT_4605, "4605 next target."),
        ("SRC4692_15_4605_validation", CSV_4605_VALIDATION, "VAL4605_OVERALL", "4605 validation passed."),
        ("SRC4692_16_formal620", FORMAL_620, "M_H_ref := H_tau", "formal denominator/projector lock."),
        ("SRC4692_17_formal621", FORMAL_621, "Q_tot_XH(lambda)=Q_bulk_XH", "formal numerator handoff."),
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
        ("SURV4692_0_denominator", "M_H_ref/M_lower", "same-frame denominator and positivity guard imported; values still missing", NEXT_TARGET),
        ("SURV4692_1_projector", "Pi_M^H", "fixed-list projector/commutator gate imported; norm and commutator values missing", NEXT_TARGET),
        ("SURV4692_2_qbarxh_abs", "Qbar_XH_abs", "source charge bound row exists but numerator components are still missing", NEXT_TARGET),
        ("SURV4692_3_product", "I_X^ST", "product update now uses MHref/PiM protected source charge", "return after Q numerator and qbarXT factors"),
        ("SURV4692_4_calibration", "G_N/GM/source mass", "no absorption into fitted calibration remains active", "keep private nonclaim"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "status_after_4692": status,
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
            "summary": "4692 imports the M_H_ref/Pi_M denominator-projector lock into the current branch. Qbar_XH is now a locked source-amplitude problem: divide only by a positive same-frame M_lower, use a fixed q-basic Pi_M projector, and retain commutator/denominator drift as explicit residuals. The next numerator target is Q_bulk+Q_edge+Q_shadow.",
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
            "derived": "same-frame M_H_ref definition; vertical silence theorem; positive denominator lower-bound contract; Pi_M fixed-list/projector commutator theorem; Qbar_XH absolute bound row; I_X^ST update",
            "not_derived": "numeric/source-backed M_lower; Pi_M operator norm; Pi_M commutator zero/bound value; Q_bulk/Q_edge/Q_shadow component values; R10/PPN/local-GR pass",
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
            "next_id": "NT4692_0",
            "target": NEXT_TARGET,
            "reason": "After 4692, the denominator/projector envelope exists. The next physical numerator is Q_bulk+Q_edge+Q_shadow.",
            "derive_first": "prove source-current/edge/shadow zero in the same parent branch",
            "fallback": "fill Q_bulk_abs, Q_edge_abs and Q_shadow_abs as nonclaim component rows under the 4692 Qbar_XH_abs formula",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4692 - Y5/R2FR MHref/PiM Denominator Lock Or QbarXH First Fill

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4692 imports the source-side denominator/projector lock:

```text
M_H_ref := H_tau[S_outer;tau_*,e_*] - H_ref[Sigma_ref;tau_*,e_*]
```

Strict branch:

```text
D_v M_H_ref=0,  M_H_ref >= M_lower > 0,  [D_v,Pi_M^H]=0.
```

Bound branch:

```text
|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower.
```

This blocks the bad route where source amplitude is hidden inside fitted `G`, `GM`, source masks, reference subtraction, or a moving projector. The next object is the numerator split `Q_bulk+Q_edge+Q_shadow`.

## Source Register

{table(rows["sources"])}

## MHref Denominator Theorem

{table(rows["mhref_theorems"])}

## PiM Projector Theorem

{table(rows["pim_theorems"])}

## MHref Denominator Input Rows

{table(rows["mhref_inputs"])}

## PiM Projector Input Rows

{table(rows["pim_inputs"])}

## QbarXH First Fill Rows

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
    FORMAL_PATH.write_text(body.replace("# 4692 - Y5/R2FR", "# 708 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4692 imports the MHref/PiM denominator-projector lock: Qbar_XH_abs is allowed only with positive same-frame M_lower, fixed Pi_M, explicit commutator drift, and non-hidden calibration.",
                "current_evidence": "Generated source register, denominator theorem, projector theorem, denominator/projector input rows, QbarXH first-fill rows, product updates, blockers, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Letting the source charge absorb reference, boundary, mask, projector or fitted-G/GM variation.",
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
        f"""## Local GR Parent-Derivation Update - Current MHref/PiM Lock

Marker: `{MARKER}`

4692 locks the source-side denominator/projector route:

```text
|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower.
```

The next local coupling target is now the numerator split, not a floating source amplitude.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current MHref/PiM Lock

Marker: `{PACKET_MARKER}`

The packet now requires a positive same-frame `M_lower`, fixed `Pi_M^H`, and explicit `E_PiM_comm` before `Qbar_XH_abs` can be used. Calibration hiding through `G_N`, `GM`, `M_H_ref`, reference masks or projectors remains forbidden.

- Qbar csv: `{QBAR_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4692_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4692_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4692_2_mhref_definition", any(row.get("theorem_id") == "MHR4692_0_same_frame_denominator_definition" for row in rows["mhref_theorems"]), "denominator definition present"),
        ("VAL4692_3_pim_commutator", any(row.get("theorem_id") == "PIM4692_2_projector_commutator_bound" for row in rows["pim_theorems"]), "projector/commutator theorem present"),
        ("VAL4692_4_mlower_input", any(row.get("quantity") == "M_lower" for row in rows["mhref_inputs"]), "M_lower input row present"),
        ("VAL4692_5_qbar_bound", any(row.get("row_id") == "QF4692_1_absolute_Qbar_bound" for row in rows["qbar"]), "QbarXH absolute bound present"),
        ("VAL4692_6_product_update", len(rows["products"]) == 2, "I_X^ST and alpha updates present"),
        ("VAL4692_7_next_numerator", rows["next"][0]["target"] == NEXT_TARGET, "next numerator target selected"),
        ("VAL4692_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-534"),
        ("VAL4692_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4692_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4692_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4692_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4692_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4692_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4692_13_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4692_14_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4692_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "mhref_theorems": restamp_rows(CSV_4604_MHREF_THEOREM, timestamp),
        "pim_theorems": restamp_rows(CSV_4604_PIM_THEOREM, timestamp),
        "mhref_inputs": restamp_rows(CSV_4604_MHREF_INPUTS, timestamp),
        "pim_inputs": restamp_rows(CSV_4604_PIM_INPUTS, timestamp),
        "qbar": restamp_rows(CSV_4604_QBAR, timestamp),
        "products": restamp_rows(CSV_4604_PRODUCT, timestamp),
        "blockers": restamp_rows(CSV_4604_BLOCKERS, timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": restamp_rows(CSV_4604_CONTROLS, timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        MHREF_THEOREM_CSV: rows["mhref_theorems"],
        PIM_THEOREM_CSV: rows["pim_theorems"],
        MHREF_INPUTS_CSV: rows["mhref_inputs"],
        PIM_INPUTS_CSV: rows["pim_inputs"],
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
