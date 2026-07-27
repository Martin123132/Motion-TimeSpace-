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

CHECKPOINT = "4691"
CLAIM_ID = "L-533"
MARKER = "PPC4161_SOURCE_TEST_INVARIANT_PRODUCT_CURRENT_BRANCH_4691"
PACKET_MARKER = "PPC4161_PACKET_SOURCE_TEST_INVARIANT_PRODUCT_CURRENT_BRANCH_4691"
DECISION = "SOURCE_TEST_INVARIANT_PRODUCT_CURRENT_BRANCH_SCHEMA_READY_NONCLAIM"
NEXT_TARGET = "4692-Y5-R2FR-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md"

DOC_PATH = POST / "4691-Y5-R2FR-source-test-charge-invariant-product-or-first-numeric-bound-row.md"
FORMAL_PATH = FORMAL / "707-PPC4161-source-test-charge-invariant-product-or-first-numeric-bound-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4690_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4690_NEXT_TARGET.csv"
CSV_4690_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4690_STATUS.csv"
CSV_4603_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4603_INVARIANT_PRODUCT_THEOREM.csv"
CSV_4603_QH = SOURCE_DIR / "P8_Y5_R2FR_4603_QBARXH_FACTOR_ROWS.csv"
CSV_4603_QT = SOURCE_DIR / "P8_Y5_R2FR_4603_QBARXT_FACTOR_ROWS.csv"
CSV_4603_PRODUCT = SOURCE_DIR / "P8_Y5_R2FR_4603_IXST_PRODUCT_BOUND_ROWS.csv"
CSV_4603_ARENA = SOURCE_DIR / "P8_Y5_R2FR_4603_ARENA_SCORE_INSERT_ROWS.csv"
CSV_4603_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4603_CLAIM_BLOCKERS.csv"
CSV_4603_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4603_CONTROL_ROWS.csv"
CSV_4603_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4603_STATUS.csv"
CSV_4603_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4603_NEXT_TARGET.csv"
CSV_4603_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4603_VALIDATION.csv"
CSV_4604_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4604_STATUS.csv"
CSV_4604_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4604_NEXT_TARGET.csv"
CSV_4604_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4604_VALIDATION.csv"
FORMAL_619 = FORMAL / "619-PPC4161-source-test-charge-invariant-product-or-first-numeric-bound-row.md"
FORMAL_620 = FORMAL / "620-PPC4161-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4691_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4691_INVARIANT_PRODUCT_THEOREM.csv"
QH_CSV = SOURCE_DIR / "P8_Y5_R2FR_4691_QBARXH_FACTOR_ROWS.csv"
QT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4691_QBARXT_FACTOR_ROWS.csv"
PRODUCT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4691_IXST_PRODUCT_BOUND_ROWS.csv"
ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4691_ARENA_SCORE_INSERT_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4691_CLAIM_BLOCKERS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4691_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4691_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4691_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4691_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4691_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4691_VALIDATION.csv"

NEXT_4603 = "4604-Y5-R2FR-MHref-PiM-denominator-lock-or-QbarXH-first-fill.md"
NEXT_4604 = "4605-Y5-R2FR-Qbulk-Qedge-Qshadow-source-current-zero-or-QbarXH-component-first-fill.md"


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
                    value.replace("4603", CHECKPOINT)
                    .replace(NEXT_4603, NEXT_TARGET)
                    .replace("2026-07-06T15:03:58.290604+00:00", timestamp)
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
        ("SRC4691_00_4690_next", CSV_4690_NEXT, "4691-Y5-R2FR-source-test-charge-invariant-product-or-first-numeric-bound-row.md", "4690 selected source/test invariant target."),
        ("SRC4691_01_4690_status", CSV_4690_STATUS, "PPC4161_RANGE_OWNER_NORMALIZATION_INVARIANT_CURRENT_BRANCH_4690", "4690 current branch status."),
        ("SRC4691_02_4603_theorem", CSV_4603_THEOREM, "IP4603_4_product_zero_or_bound", "4603 invariant product theorem."),
        ("SRC4691_03_4603_qbarxh", CSV_4603_QH, "QH4603_3_projected_source_charge", "4603 source-side factor rows."),
        ("SRC4691_04_4603_qbarxt", CSV_4603_QT, "QT4603_4_total_guard", "4603 test-side factor rows."),
        ("SRC4691_05_4603_product", CSV_4603_PRODUCT, "IX4603_1_absolute_product_bound", "4603 invariant product bound rows."),
        ("SRC4691_06_4603_arena", CSV_4603_ARENA, "AR4603_4_EM_Poynting", "4603 arena insert rows."),
        ("SRC4691_07_4603_blockers", CSV_4603_BLOCKERS, "MIS4603_0_MHref_PiM_lock", "4603 claim blockers."),
        ("SRC4691_08_4603_controls", CSV_4603_CONTROLS, "CTRL4603_3_same_branch", "4603 controls."),
        ("SRC4691_09_4603_status", CSV_4603_STATUS, "SOURCE_TEST_INVARIANT_PRODUCT_DERIVED_SCHEMA_READY_NONCLAIM", "4603 status."),
        ("SRC4691_10_4603_next", CSV_4603_NEXT, NEXT_4603, "4603 next target."),
        ("SRC4691_11_4603_validation", CSV_4603_VALIDATION, "VAL4603_OVERALL", "4603 validation passed."),
        ("SRC4691_12_4604_status", CSV_4604_STATUS, "MHREF_PIM_LOCK_THEOREM_AND_QBARXH_BOUND_ROW_READY_NONCLAIM", "4604 denominator/projector rung exists."),
        ("SRC4691_13_4604_next", CSV_4604_NEXT, NEXT_4604, "4604 next target."),
        ("SRC4691_14_4604_validation", CSV_4604_VALIDATION, "VAL4604_OVERALL", "4604 validation passed."),
        ("SRC4691_15_formal619", FORMAL_619, "I_X^ST(lambda_X)", "formal source/test invariant product."),
        ("SRC4691_16_formal620", FORMAL_620, "M_H_ref := H_tau", "formal denominator/projector handoff."),
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
        ("SURV4691_0_product_gate", "I_X^ST", "source/test product gate imported; zero-or-bound route explicit", NEXT_TARGET),
        ("SURV4691_1_source_factor", "Qbar_XH", "source-side charge depends first on M_H_ref/Pi_M lock", NEXT_TARGET),
        ("SURV4691_2_test_factor", "qbar_XT", "test-side zero theorem/components remain explicit but second in order", "return after source denominator/components"),
        ("SURV4691_3_arena_scores", "R10/PPN/clock/orbit/EM", "all arena insert rows remain blocked by product values and kernels", "defer pass/fail claims"),
        ("SURV4691_4_coupling_guard", "G_N/GM/calibration", "finite-range product cannot be hidden inside fitted G or GM", "keep no-absorption control active"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "status_after_4691": status,
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
            "summary": "4691 imports the source/test invariant product gate into the current branch. The amplitude problem is no longer vague coupling language: I_X^ST is zero only if Qbar_XH or qbar_XT is zero in the same branch; otherwise the claim-safe object is an absolute product bound. The next physical source-side blocker is M_H_ref/Pi_M.",
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
            "derived": "source/test invariant product definition; field-rescaling contract; Qbar_XH factor ledger; qbar_XT factor ledger; zero-or-absolute-bound product law; arena insert blockers",
            "not_derived": "numeric I_X^ST; parent-signed Qbar_XH zero; parent-signed qbar_XT zero; M_H_ref/Pi_M source denominator lock in current branch; R10/PPN/local-GR pass",
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
            "next_id": "NT4691_0",
            "target": NEXT_TARGET,
            "reason": "The source-side denominator/projector lock is the sharpest first missing factor: without M_H_ref/Pi_M, Qbar_XH and therefore I_X^ST are not physically owned.",
            "derive_first": "derive M_H_ref positivity/reference lock and Pi_M same-frame projector silence, then insert Qbar_XH_abs",
            "fallback": "retain Qbar_XH_abs as nonclaim source factor with explicit MISSING_MHREF_PIM/source-component blockers",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4691 - Y5/R2FR Source/Test Charge Invariant Product Or First Numeric Bound Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4691 imports the finite-range source/test amplitude gate:

```text
I_X^ST(lambda_X)=Qbar_XH(lambda_X) qbar_XT(lambda_X)/(4*pi Z_X G_N M_H_ref m_T)
```

The exact zero route is:

```text
Qbar_XH=0 or qbar_XT=0  =>  I_X^ST=0.
```

The claim-safe bounded route is:

```text
|I_X^ST| <= |Qbar_XH|_abs |qbar_XT|_abs/(4*pi |Z_X| G_N M_H_ref m_T).
```

No cancellation, no fitted-`G` absorption, and no raw-charge scoring are allowed. The next source-side lock is `M_H_ref/Pi_M`.

## Source Register

{table(rows["sources"])}

## Invariant Product Theorem

{table(rows["theorems"])}

## Qbar_XH Factor Rows

{table(rows["qbarxh"])}

## qbar_XT Factor Rows

{table(rows["qbarxt"])}

## I_X^ST Product Bound Rows

{table(rows["products"])}

## Arena Score Insert Rows

{table(rows["arenas"])}

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
    FORMAL_PATH.write_text(body.replace("# 4691 - Y5/R2FR", "# 707 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4691 imports the source/test invariant product gate: I_X^ST is the finite-range amplitude object, with exact-zero and absolute-bound routes but no numeric/local-GR claim.",
                "current_evidence": "Generated source register, invariant theorem, Qbar_XH/qbar_XT factor rows, product bound rows, arena inserts, blockers, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Treating source/test factors as fitted coupling knobs or absorbing the finite-range product into G_N/GM calibration.",
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
        f"""## Local GR Parent-Derivation Update - Current Source/Test Invariant Product

Marker: `{MARKER}`

4691 makes the finite-range amplitude gate explicit:

```text
I_X^ST=Qbar_XH qbar_XT/(4*pi Z_X G_N M_H_ref m_T).
```

This is the local coupling object that must be zeroed or bounded before R10, PPN, clock, orbital or EM claims. The next sharp source-side target is the `M_H_ref/Pi_M` denominator/projector lock.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current Source/Test Invariant Product

Marker: `{PACKET_MARKER}`

The packet now carries `I_X^ST` as the finite-range source/test amplitude object. No future score may use raw source/test charges or hide the product in `G_N`, `GM`, `M_H_ref` or readout normalization.

- theorem csv: `{THEOREM_CSV.name}`
- product csv: `{PRODUCT_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4691_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4691_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4691_2_invariant_product_defined", any(row.get("theorem_id") == "IP4691_1_invariant_product_definition" for row in rows["theorems"]), "invariant product and rescaling law present"),
        ("VAL4691_3_zero_or_bound_route", any(row.get("row_id") == "IX4691_1_absolute_product_bound" for row in rows["products"]), "zero route and absolute product bound present"),
        ("VAL4691_4_source_factor_rows", any(row.get("factor") == "Qbar_XH(lambda)" for row in rows["qbarxh"]), "Qbar source factors present"),
        ("VAL4691_5_test_factor_rows", any(row.get("factor") == "qbar_XT_bound_abs" for row in rows["qbarxt"]), "qbar test factors present"),
        ("VAL4691_6_arena_rows", len(rows["arenas"]) == 5, "five arena insert rows present"),
        ("VAL4691_7_mhref_next", rows["next"][0]["target"] == NEXT_TARGET, "next MHref/PiM target selected"),
        ("VAL4691_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-533"),
        ("VAL4691_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4691_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4691_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4691_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4691_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4691_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4691_13_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4691_14_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4691_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "theorems": restamp_rows(CSV_4603_THEOREM, timestamp),
        "qbarxh": restamp_rows(CSV_4603_QH, timestamp),
        "qbarxt": restamp_rows(CSV_4603_QT, timestamp),
        "products": restamp_rows(CSV_4603_PRODUCT, timestamp),
        "arenas": restamp_rows(CSV_4603_ARENA, timestamp),
        "blockers": restamp_rows(CSV_4603_BLOCKERS, timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": restamp_rows(CSV_4603_CONTROLS, timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        THEOREM_CSV: rows["theorems"],
        QH_CSV: rows["qbarxh"],
        QT_CSV: rows["qbarxt"],
        PRODUCT_CSV: rows["products"],
        ARENA_CSV: rows["arenas"],
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
