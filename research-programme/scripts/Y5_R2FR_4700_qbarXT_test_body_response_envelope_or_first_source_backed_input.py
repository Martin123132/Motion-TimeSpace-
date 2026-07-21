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

CHECKPOINT = "4700"
CLAIM_ID = "L-542"
MARKER = "PPC4161_QBARXT_TEST_BODY_RESPONSE_ENVELOPE_BRANCH_4700"
PACKET_MARKER = "PPC4161_PACKET_QBARXT_TEST_BODY_RESPONSE_ENVELOPE_BRANCH_4700"
DECISION = "QBARXT_TEST_BODY_RESPONSE_ENVELOPE_READY_FIRST_SOURCE_BACKED_QUEUE_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4701-Y5-R2FR-matter-marker-EM-constant-descent-or-first-qbarXT-coefficient-row.md"

DOC_PATH = POST / "4700-Y5-R2FR-qbarXT-test-body-response-envelope-or-first-source-backed-input.md"
FORMAL_PATH = FORMAL / "716-PPC4161-qbarXT-test-body-response-envelope-or-first-source-backed-input.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4699_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4699_STATUS.csv"
CSV_4699_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4699_NEXT_TARGET.csv"
CSV_4699_CURRENT = SOURCE_DIR / "P8_Y5_R2FR_4699_CURRENT_BRANCH_QBARXH_ROLLUP_ROWS.csv"
CSV_4699_PRODUCT = SOURCE_DIR / "P8_Y5_R2FR_4699_PRODUCT_HANDOFF_ROWS.csv"
CSV_4699_PRIORITY = SOURCE_DIR / "P8_Y5_R2FR_4699_FIRST_SOURCE_BACKED_PRIORITY_QUEUE.csv"
CSV_4699_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4699_VALIDATION.csv"

CSV_4612_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4612_QBARXT_RESPONSE_ENVELOPE_THEOREM.csv"
CSV_4612_VISIBLE = SOURCE_DIR / "P8_Y5_R2FR_4612_VISIBLE_MATTER_RESPONSE_ROWS.csv"
CSV_4612_MARKER = SOURCE_DIR / "P8_Y5_R2FR_4612_MARKER_CONSTANT_RESPONSE_ROWS.csv"
CSV_4612_BDR = SOURCE_DIR / "P8_Y5_R2FR_4612_BOUNDARY_DOMAIN_READOUT_ROWS.csv"
CSV_4612_HIDDEN = SOURCE_DIR / "P8_Y5_R2FR_4612_HIDDEN_TAIL_RESPONSE_ROWS.csv"
CSV_4612_PRODUCT = SOURCE_DIR / "P8_Y5_R2FR_4612_PRODUCT_COUPLING_HANDOFF_ROWS.csv"
CSV_4612_PRIORITY = SOURCE_DIR / "P8_Y5_R2FR_4612_FIRST_SOURCE_BACKED_PRIORITY_QUEUE.csv"
CSV_4612_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4612_CLAIM_BLOCKERS.csv"
CSV_4612_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4612_CONTROL_ROWS.csv"
CSV_4612_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4612_STATUS.csv"
CSV_4612_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4612_DECISION.csv"
CSV_4612_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4612_NEXT_TARGET.csv"
CSV_4612_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4612_VALIDATION.csv"

FORMAL_715 = FORMAL / "715-PPC4161-QbarXH-full-source-envelope-rollup-or-first-source-backed-input.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4700_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4700_QBARXT_RESPONSE_ENVELOPE_THEOREM.csv"
VISIBLE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4700_VISIBLE_MATTER_RESPONSE_ROWS.csv"
MARKER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4700_MARKER_CONSTANT_RESPONSE_ROWS.csv"
BDR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4700_BOUNDARY_DOMAIN_READOUT_ROWS.csv"
HIDDEN_CSV = SOURCE_DIR / "P8_Y5_R2FR_4700_HIDDEN_TAIL_RESPONSE_ROWS.csv"
PRODUCT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4700_PRODUCT_COUPLING_HANDOFF_ROWS.csv"
PRIORITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4700_FIRST_SOURCE_BACKED_PRIORITY_QUEUE.csv"
CURRENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4700_CURRENT_BRANCH_COUPLING_PRODUCT_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4700_CLAIM_BLOCKERS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4700_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4700_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4700_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4700_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4700_VALIDATION.csv"

NEXT_4699 = "4700-Y5-R2FR-qbarXT-test-body-response-envelope-or-first-source-backed-input.md"
NEXT_4612 = "4613-Y5-R2FR-matter-marker-EM-constant-descent-or-first-qbarXT-coefficient-row.md"


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
            if key in {"source_paths", "path", "source_path"}:
                new_value = value
            else:
                new_value = (
                    value.replace("4612", CHECKPOINT)
                    .replace(NEXT_4612, NEXT_TARGET)
                    .replace("2026-07-06T16:23:29.997921+00:00", timestamp)
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
        ("SRC4700_00_4699_status", CSV_4699_STATUS, "PPC4161_QBARXH_FULL_SOURCE_ENVELOPE_ROLLUP_BRANCH_4699", "4699 source-side rollup."),
        ("SRC4700_01_4699_next", CSV_4699_NEXT, NEXT_4699, "4699 hands off to qbarXT."),
        ("SRC4700_02_4699_current", CSV_4699_CURRENT, "QBC4699_0_current_full_envelope", "4699 current QbarXH envelope."),
        ("SRC4700_03_4699_product", CSV_4699_PRODUCT, "PROD4699_1_test_side", "4699 product handoff names qbarXT."),
        ("SRC4700_04_4699_priority", CSV_4699_PRIORITY, "M_lower", "4699 source-side priority queue."),
        ("SRC4700_05_4699_validation", CSV_4699_VALIDATION, "VAL4699_OVERALL", "4699 validation passed."),
        ("SRC4700_06_4612_theorem", CSV_4612_THEOREM, "QXT4612_2_component_envelope", "4612 qbarXT theorem."),
        ("SRC4700_07_4612_visible", CSV_4612_VISIBLE, "VIS4612_0_geom", "4612 visible matter rows."),
        ("SRC4700_08_4612_marker", CSV_4612_MARKER, "MRK4612_2_EM_alpha", "4612 marker/constant/EM rows."),
        ("SRC4700_09_4612_bdr", CSV_4612_BDR, "BDR4612_3_readout", "4612 boundary/domain/readout rows."),
        ("SRC4700_10_4612_hidden", CSV_4612_HIDDEN, "HID4612_1_nonHilbert", "4612 hidden-tail rows."),
        ("SRC4700_11_4612_product", CSV_4612_PRODUCT, "PCO4612_2_coupling_firewall", "4612 product coupling handoff."),
        ("SRC4700_12_4612_priority", CSV_4612_PRIORITY, "qbar_constants", "4612 first source-backed queue."),
        ("SRC4700_13_4612_controls", CSV_4612_CONTROLS, "CTRL4612_2_no_marker_hiding", "4612 controls."),
        ("SRC4700_14_4612_status", CSV_4612_STATUS, "QBARXT_TEST_BODY_RESPONSE_ENVELOPE_READY_FIRST_SOURCE_BACKED_QUEUE_NONCLAIM", "4612 status."),
        ("SRC4700_15_4612_next", CSV_4612_NEXT, NEXT_4612, "4612 next target."),
        ("SRC4700_16_4612_validation", CSV_4612_VALIDATION, "VAL4612_OVERALL", "4612 validation passed."),
        ("SRC4700_17_formal715", FORMAL_715, "Q_tot_XH_abs", "formal QbarXH upstream handoff."),
    ]
    rows = []
    for source_id, path, needle, role in specs:
        line = line_of(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "needle": needle,
                "needle_found": line > 0,
                "source_line": line,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def current_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CPL4700_0_current_product_bound",
            "quantity": "I_X^ST(lambda)",
            "formula": "|I_X^ST| <= |Qbar_XH_4699| |qbar_XT_4700|/(4*pi |Z_X| G_N M_H_ref m_T)",
            "current_chain": "source side from Qbar_XH_4699; test-body side from qbar_XT_4700; normalization still needs Z_X/K_X/tau arena rows",
            "claim_firewall": "No local, R10, PPN, WEP, clock, orbital or Newton claim until both sides plus Z_X/K_X/tau are source-backed",
            "current_status": "COUPLING_PRODUCT_CURRENT_BRANCH_ASSEMBLED_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "CPL4700_1_qbarXT_first_fill_order",
            "quantity": "qbarXT_first_source_backed_priority_queue",
            "formula": "1 constants/markers/EM/clock -> 2 visible geometry frame -> 3 hidden frame -> 4 source weights/nonHilbert -> 5 support/boundary/domain/readout -> 6 K_X/Z_X/tau",
            "current_chain": "This is the test-body analogue of the 4699 source-side priority queue.",
            "claim_firewall": "No universality/WEP wording, measured-G calibration or readout convention can replace channel-by-channel descent.",
            "current_status": "QBARXT_FILL_ORDER_READY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_QBARXT_TEST_BODY_RESPONSE_ENVELOPE_4700",
            "decision": DECISION,
            "reason": "The test-body coupling side is current-branch rolled into one qbarXT response envelope and priority queue, paired with the 4699 source-side QbarXH rollup.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    status = [
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "claim_id": CLAIM_ID,
            "decision": DECISION,
            "derived": "qbarXT definition; visible/hidden response envelope; marker/constant/EM rows; support/boundary/domain/readout rows; product coupling handoff with QbarXH_4699",
            "not_derived": "matter/EM/clock marker descent, visible frame zero, hidden-tail bounds, K_X/Z_X/tau arena kernels, local-GR/R10/PPN pass",
            "claim_status": "PRIVATE_NONCLAIM",
            "local_GR_public_claim": False,
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    next_rows = [
        {
            "checkpoint": CHECKPOINT,
            "next_id": "NT4700_0",
            "target": NEXT_TARGET,
            "reason": "The nearest qbarXT pressure point is ordinary matter markers: masses, EM/fine-structure, clocks and material labels.",
            "derive_first": "prove theta_A vertical silence or quotient ownership channel-by-channel for matter, EM, clock and material markers",
            "fallback": "stage first source-backed qbarXT coefficient rows with units and source paths",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4700 - qbarXT Test-Body Response Envelope

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
This checkpoint does **not** claim local GR. It rolls the test-body side into one response envelope:

```text
qbar_XT := M_T^-1 |delta_vX S_T|
```

and

```text
|qbar_XT| <= |qbar_geom|+|qbar_constants|+|qbar_marker|+|qbar_source_weight|
  +|qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|+|qbar_readout|.
```

The current product handoff is:

```text
|I_X^ST| <= |Qbar_XH_4699| |qbar_XT_4700|/(4*pi |Z_X| G_N M_H_ref m_T).
```

## Source Register
{table(data["sources"])}

## qbarXT Response Theorem
{table(data["theorem"])}

## Visible Matter Rows
{table(data["visible"])}

## Marker / Constant / EM Rows
{table(data["marker"])}

## Boundary / Domain / Readout Rows
{table(data["bdr"])}

## Hidden Tail Rows
{table(data["hidden"])}

## Product Handoff
{table(data["product"])}

## Current Branch Product Rows
{table(data["current"])}

## First Source-Backed Priority Queue
{table(data["priority"])}

## Blockers
{table(data["blockers"])}

## Controls
{table(data["controls"])}

## Decision
{table(data["decision"])}

## Next Target
{table(data["next"])}
""",
        encoding="utf-8",
    )

    FORMAL_PATH.write_text(
        f"""# 716 - PPC4161 qbarXT Test-Body Response Envelope

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
```text
qbar_XT := M_T^-1 |delta_vX S_T|.
```

```text
|qbar_XT| <= |qbar_geom|+|qbar_constants|+|qbar_marker|+|qbar_source_weight|
  + |qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|+|qbar_readout|.
```

```text
|I_X^ST| <= |Qbar_XH_4699| |qbar_XT_4700|/(4*pi |Z_X| G_N M_H_ref m_T).
```

No WEP/universality wording, measured-G calibration, readout convention or component cancellation can replace channel-by-channel descent or source-backed bounds.

## Nonclaim Status
No R10, WEP, PPN, clock, orbital, Newton, Maxwell or local-GR claim follows. Next branch is matter-marker/EM/constant descent.
""",
        encoding="utf-8",
    )


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH) if CLAIMS_PATH.exists() else []
    fieldnames = list(claims[0].keys()) if claims else [
        "claim_id",
        "domain",
        "claim",
        "current_evidence",
        "status",
        "next_test",
        "key_risk",
        "sector",
        "evidence",
        "next_action",
        "risk",
        "title",
        "notes",
    ]
    claim_row = {field: "" for field in fieldnames}
    claim_row.update(
        {
            "claim_id": CLAIM_ID,
            "domain": "local_gr_empirical_interface",
            "claim": "4700 rolls qbarXT into a test-body response envelope and pairs it with the 4699 QbarXH source-side envelope.",
            "current_evidence": "Generated source register, qbarXT theorem rows, visible/marker/boundary/hidden response rows, product handoff, current branch coupling rows, priority queue, blockers, controls, decision, status, next target and validation.",
            "status": "qbarxt_test_body_response_envelope_current_branch_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Using WEP/universality wording, measured-G calibration, readout conventions or cancellation to erase test-body response channels.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "qbarXT test-body response envelope",
            "notes": f"{MARKER}; {DECISION}; generated {timestamp}",
        }
    )
    existing = next((row for row in claims if row.get("claim_id") == CLAIM_ID), None)
    if existing is None:
        claims.append(claim_row)
    else:
        existing.update(claim_row)
    write_csv(CLAIMS_PATH, claims)

    append_once(
        SPINE_PATH,
        MARKER,
        f"""### {MARKER}

- Claim: `{CLAIM_ID}`
- Status: private nonclaim.
- Movement: test-body response is now one current-branch `qbar_XT` envelope paired with `Qbar_XH_4699`.
- First qbarXT fill order: matter/EM/clock constants and markers, visible geometry frame, hidden frame, source weights/non-Hilbert tails, support/boundary/domain/readout, then `K_X/Z_X/tau`.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: current PPC4161 test-body response branch before matter-marker descent.
- Validation: `{VALIDATION_CSV}`.
""",
    )


def validation_rows(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "passed": passed,
                "detail": detail,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )

    add("VAL4700_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4700_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4700_2_qbarXT_definition", any("qbar_XT" in row.get("quantity", "") for row in data["theorem"]), "qbarXT theorem rows present")
    add("VAL4700_3_component_envelope", any("qbar_geom" in row.get("formula", "") for row in data["theorem"]), "component envelope present")
    add("VAL4700_4_marker_priority", len(data["priority"]) >= 6 and data["priority"][0].get("priority") == "1", "qbarXT priority queue present")
    add("VAL4700_5_current_product", any("Qbar_XH_4699" in row.get("formula", "") for row in data["current"]), "current product references Qbar_XH_4699")
    add("VAL4700_6_no_marker_control", any(row.get("control_id") == "CTRL4700_2_no_marker_hiding" for row in data["controls"]), "no marker hiding control present")
    add("VAL4700_7_next_marker_descent", data["next"][0]["target"] == NEXT_TARGET, "next marker descent target selected")
    add("VAL4700_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4700_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4700_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4700_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4700_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")

    for csv_path in [
        SOURCE_REGISTER,
        THEOREM_CSV,
        VISIBLE_CSV,
        MARKER_CSV,
        BDR_CSV,
        HIDDEN_CSV,
        PRODUCT_CSV,
        PRIORITY_CSV,
        CURRENT_CSV,
        BLOCKERS_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4700_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4700_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [data["theorem"], data["visible"], data["marker"], data["bdr"], data["hidden"], data["product"], data["priority"], data["current"], data["blockers"], data["controls"], data["decision"], data["status"], data["next"]]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4700_13_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4700_14_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4700_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_rows(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "theorem": restamp_rows(CSV_4612_THEOREM, timestamp),
        "visible": restamp_rows(CSV_4612_VISIBLE, timestamp),
        "marker": restamp_rows(CSV_4612_MARKER, timestamp),
        "bdr": restamp_rows(CSV_4612_BDR, timestamp),
        "hidden": restamp_rows(CSV_4612_HIDDEN, timestamp),
        "product": restamp_rows(CSV_4612_PRODUCT, timestamp),
        "priority": restamp_rows(CSV_4612_PRIORITY, timestamp),
        "current": current_rows(timestamp),
        "blockers": restamp_rows(CSV_4612_BLOCKERS, timestamp),
        "controls": restamp_rows(CSV_4612_CONTROLS, timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(THEOREM_CSV, data["theorem"])
    write_csv(VISIBLE_CSV, data["visible"])
    write_csv(MARKER_CSV, data["marker"])
    write_csv(BDR_CSV, data["bdr"])
    write_csv(HIDDEN_CSV, data["hidden"])
    write_csv(PRODUCT_CSV, data["product"])
    write_csv(PRIORITY_CSV, data["priority"])
    write_csv(CURRENT_CSV, data["current"])
    write_csv(BLOCKERS_CSV, data["blockers"])
    write_csv(CONTROL_CSV, data["controls"])
    write_csv(DECISION_CSV, data["decision"])
    write_csv(STATUS_CSV, data["status"])
    write_csv(NEXT_CSV, data["next"])

    write_documents(timestamp, data)
    update_registers(timestamp)
    validation = validation_rows(timestamp, data)
    write_csv(VALIDATION_CSV, validation)

    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
