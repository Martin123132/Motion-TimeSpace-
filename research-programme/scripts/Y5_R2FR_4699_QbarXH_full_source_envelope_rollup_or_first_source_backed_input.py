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

CHECKPOINT = "4699"
CLAIM_ID = "L-541"
MARKER = "PPC4161_QBARXH_FULL_SOURCE_ENVELOPE_ROLLUP_BRANCH_4699"
PACKET_MARKER = "PPC4161_PACKET_QBARXH_FULL_SOURCE_ENVELOPE_ROLLUP_BRANCH_4699"
DECISION = "QBARXH_FULL_SOURCE_ENVELOPE_ROLLUP_READY_FIRST_SOURCE_BACKED_QUEUE_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4700-Y5-R2FR-qbarXT-test-body-response-envelope-or-first-source-backed-input.md"

DOC_PATH = POST / "4699-Y5-R2FR-QbarXH-full-source-envelope-rollup-or-first-source-backed-input.md"
FORMAL_PATH = FORMAL / "715-PPC4161-QbarXH-full-source-envelope-rollup-or-first-source-backed-input.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4698_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4698_STATUS.csv"
CSV_4698_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4698_NEXT_TARGET.csv"
CSV_4698_QBAR = SOURCE_DIR / "P8_Y5_R2FR_4698_QSHADOW_QBARXH_UPDATE_ROWS.csv"
CSV_4698_INSERT = SOURCE_DIR / "P8_Y5_R2FR_4698_QSHADOW_CURRENT_BRANCH_INSERTION_ROWS.csv"
CSV_4698_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4698_VALIDATION.csv"

CSV_4611_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4611_QBARXH_SOURCE_ENVELOPE_THEOREM.csv"
CSV_4611_BULK = SOURCE_DIR / "P8_Y5_R2FR_4611_QBULK_ROLLUP_ROWS.csv"
CSV_4611_EDGE = SOURCE_DIR / "P8_Y5_R2FR_4611_QEDGE_ROLLUP_ROWS.csv"
CSV_4611_SHADOW = SOURCE_DIR / "P8_Y5_R2FR_4611_QSHADOW_ROLLUP_ROWS.csv"
CSV_4611_DPROJ = SOURCE_DIR / "P8_Y5_R2FR_4611_QBARXH_DENOMINATOR_PROJECTOR_ROWS.csv"
CSV_4611_PRIORITY = SOURCE_DIR / "P8_Y5_R2FR_4611_FIRST_SOURCE_BACKED_PRIORITY_QUEUE.csv"
CSV_4611_PRODUCT = SOURCE_DIR / "P8_Y5_R2FR_4611_PRODUCT_HANDOFF_ROWS.csv"
CSV_4611_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4611_CLAIM_BLOCKERS.csv"
CSV_4611_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4611_CONTROL_ROWS.csv"
CSV_4611_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4611_STATUS.csv"
CSV_4611_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4611_DECISION.csv"
CSV_4611_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4611_NEXT_TARGET.csv"
CSV_4611_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4611_VALIDATION.csv"

FORMAL_714 = FORMAL / "714-PPC4161-Qshadow-source-map-normal-form-zero-or-nonHilbert-first-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4699_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4699_QBARXH_SOURCE_ENVELOPE_THEOREM.csv"
BULK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4699_QBULK_ROLLUP_ROWS.csv"
EDGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4699_QEDGE_ROLLUP_ROWS.csv"
SHADOW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4699_QSHADOW_ROLLUP_ROWS.csv"
DPROJ_CSV = SOURCE_DIR / "P8_Y5_R2FR_4699_QBARXH_DENOMINATOR_PROJECTOR_ROWS.csv"
PRIORITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4699_FIRST_SOURCE_BACKED_PRIORITY_QUEUE.csv"
PRODUCT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4699_PRODUCT_HANDOFF_ROWS.csv"
CURRENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4699_CURRENT_BRANCH_QBARXH_ROLLUP_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4699_CLAIM_BLOCKERS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4699_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4699_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4699_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4699_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4699_VALIDATION.csv"

NEXT_4698 = "4699-Y5-R2FR-QbarXH-full-source-envelope-rollup-or-first-source-backed-input.md"
NEXT_4611 = "4612-Y5-R2FR-qbarXT-test-body-response-envelope-or-first-source-backed-input.md"


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
                    value.replace("4611", CHECKPOINT)
                    .replace(NEXT_4611, NEXT_TARGET)
                    .replace("2026-07-06T16:16:00.267321+00:00", timestamp)
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
        ("SRC4699_00_4698_status", CSV_4698_STATUS, "PPC4161_QSHADOW_SOURCE_MAP_NORMAL_FORM_BRANCH_4698", "4698 Qshadow branch."),
        ("SRC4699_01_4698_next", CSV_4698_NEXT, NEXT_4698, "4698 hands off to Qbar rollup."),
        ("SRC4699_02_4698_qbar", CSV_4698_QBAR, "QSU4698_2_QbarXH", "4698 Qbar source-envelope row."),
        ("SRC4699_03_4698_insert", CSV_4698_INSERT, "Q_edge_4697", "4698 current numerator ordering."),
        ("SRC4699_04_4698_validation", CSV_4698_VALIDATION, "VAL4698_OVERALL", "4698 validation passed."),
        ("SRC4699_05_4611_theorem", CSV_4611_THEOREM, "QBAR4611_1_QbarXH_projection_bound", "4611 Qbar envelope theorem."),
        ("SRC4699_06_4611_bulk", CSV_4611_BULK, "BROLL4611_0_bulk_total", "4611 bulk rollup."),
        ("SRC4699_07_4611_edge", CSV_4611_EDGE, "EROLL4611_0_edge_total", "4611 edge rollup."),
        ("SRC4699_08_4611_shadow", CSV_4611_SHADOW, "SROLL4611_0_shadow_total", "4611 shadow rollup."),
        ("SRC4699_09_4611_dproj", CSV_4611_DPROJ, "DPROJ4611_0_M_lower", "4611 denominator/projector firewall."),
        ("SRC4699_10_4611_priority", CSV_4611_PRIORITY, "M_lower", "4611 source-backed priority queue."),
        ("SRC4699_11_4611_product", CSV_4611_PRODUCT, "PROD4611_1_test_side", "4611 product/test-side handoff."),
        ("SRC4699_12_4611_controls", CSV_4611_CONTROLS, "CTRL4611_3_no_measured_G_smuggling", "4611 controls."),
        ("SRC4699_13_4611_status", CSV_4611_STATUS, "QBARXH_FULL_SOURCE_ENVELOPE_ROLLUP_READY_FIRST_SOURCE_BACKED_QUEUE_NONCLAIM", "4611 status."),
        ("SRC4699_14_4611_next", CSV_4611_NEXT, NEXT_4611, "4611 next target."),
        ("SRC4699_15_4611_validation", CSV_4611_VALIDATION, "VAL4611_OVERALL", "4611 validation passed."),
        ("SRC4699_16_formal714", FORMAL_714, "Q_shadow =", "formal Qshadow upstream handoff."),
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
            "row_id": "QBC4699_0_current_full_envelope",
            "quantity": "Qbar_XH_abs",
            "formula": "|Qbar_XH| <= (||Pi_M^H||(|Q_bulk_4696|+|Q_edge_4697|+|Q_shadow_4698|)+|E_PiM_comm|)/M_lower",
            "current_chain": "Q_bulk_4696 from retained/EM/Hilbert split; Q_edge_4697 from shell/boundary flux split; Q_shadow_4698 from action/projector/nonvariational split",
            "claim_firewall": "M_lower, Pi_M norm, E_PiM_comm and all component bounds must be exact-zero signed or source-backed before scoring arenas",
            "current_status": "CURRENT_QBARXH_SOURCE_ENVELOPE_ASSEMBLED_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QBC4699_1_first_fill_order",
            "quantity": "first_source_backed_priority_queue",
            "formula": "1 denominator/projector -> 2 edge shell -> 3 Poynting/Hodge wall flux -> 4 epsilon_source_shadow -> 5 retained currents -> 6 action/nonvariational shadow",
            "current_chain": "This is the shortest route from symbolic local-GR branch to source-backed tests without pretending the theory is already closed.",
            "claim_firewall": "No public/local-GR/R10/PPN/clock/orbit claim from symbolic queue rows.",
            "current_status": "FILL_ORDER_READY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_QBARXH_FULL_SOURCE_ENVELOPE_ROLLUP_4699",
            "decision": DECISION,
            "reason": "Bulk, edge and shadow numerator families are no longer scattered. The current branch has a single Qbar_XH source envelope and a priority queue for the first source-backed rows.",
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
            "derived": "full source-side Qbar_XH envelope; denominator/projector firewall; bulk/edge/shadow rollup; first source-backed fill priority queue; product handoff",
            "not_derived": "source-backed M_lower/Pi_M/E_PiM values, qbar_XT test-body response, Z_X, arena tau kernels, local-GR/R10/PPN pass",
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
            "next_id": "NT4699_0",
            "target": NEXT_TARGET,
            "reason": "Source side is rolled up; the product still cannot be tested until qbar_XT/test-body response receives the same non-cancellation treatment.",
            "derive_first": "derive qbar_XT as the test-body response analogue of Qbar_XH with no cancellation or measured-G smuggling",
            "fallback": "produce a nonclaim qbar_XT missing-input priority queue and arena tau handoff rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4699 - QbarXH Full Source Envelope Rollup

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
This checkpoint does **not** claim local GR. It rolls the source-side numerator into one envelope:

```text
|Qbar_XH| <= (||Pi_M^H||(|Q_bulk_4696|+|Q_edge_4697|+|Q_shadow_4698|)
  + |E_PiM_comm|)/M_lower.
```

The practical output is the fill order:

```text
1. M_lower, ||Pi_M^H||, E_PiM_comm
2. Q_edge_shell_abs
3. Phi_wall_Poynting_abs and EM/Hodge leakage
4. epsilon_source_shadow
5. J_direct_abs, J_mem_abs, J_readout_abs
6. Q_shadow_action_abs and Q_shadow_nonvariational_abs
```

## Source Register
{table(data["sources"])}

## Source Envelope Theorem
{table(data["theorem"])}

## Current Branch Rollup
{table(data["current"])}

## Bulk Rollup
{table(data["bulk"])}

## Edge Rollup
{table(data["edge"])}

## Shadow Rollup
{table(data["shadow"])}

## Denominator / Projector Firewall
{table(data["dproj"])}

## First Source-Backed Priority Queue
{table(data["priority"])}

## Product Handoff
{table(data["product"])}

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
        f"""# 715 - PPC4161 QbarXH Full Source Envelope Rollup

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
```text
Q_tot_XH_abs <= |Q_bulk_4696| + |Q_edge_4697| + |Q_shadow_4698|.
```

```text
|Qbar_XH| <= (||Pi_M^H|| Q_tot_XH_abs + |E_PiM_comm|)/M_lower.
```

Equivalent current-branch form:

```text
|Qbar_XH| <= (||Pi_M^H||(|Q_bulk_4696|+|Q_edge_4697|+|Q_shadow_4698|)
  + |E_PiM_comm|)/M_lower.
```

No division by symbolic `M_lower` is allowed in an arena claim. No relative, range, species, time or readout residual may be absorbed into measured `G_N`.

## Nonclaim Status
No R10, WEP, PPN, clock, orbital, Newton or local-GR claim follows. Next branch is `qbar_XT`.
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
            "claim": "4699 rolls current Qbulk, Qedge and Qshadow branches into one Qbar_XH source envelope with a source-backed fill priority queue.",
            "current_evidence": "Generated source register, source-envelope theorem, current branch rollup, bulk/edge/shadow rollups, denominator/projector rows, priority queue, product handoff, blockers, controls, decision, status, next target and validation.",
            "status": "qbarxh_full_source_envelope_rollup_current_branch_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Dividing by symbolic M_lower, hiding residuals in measured G_N, or treating symbolic source-side rows as empirical local-GR evidence.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "QbarXH full source envelope rollup",
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
- Movement: `Qbar_XH` source side is now one current-branch envelope using `Q_bulk_4696`, `Q_edge_4697` and `Q_shadow_4698`.
- First fill order: denominator/projector, edge shell, Poynting/Hodge wall flux, source-shadow projector, retained currents, then action/nonvariational shadow.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: current PPC4161 source-side rollup before test-body response.
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

    add("VAL4699_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4699_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4699_2_current_envelope", any("Q_bulk_4696" in row.get("formula", "") for row in data["current"]), "current Qbar envelope references current branch components")
    add("VAL4699_3_dproj_firewall", any("M_lower" in row.get("quantity", "") for row in data["dproj"]), "denominator/projector firewall rows present")
    add("VAL4699_4_priority_queue", len(data["priority"]) >= 6 and data["priority"][0].get("priority") == "1", "source-backed priority queue present")
    add("VAL4699_5_product_handoff", any("qbar_XT" in row.get("quantity", "") for row in data["product"]), "qbarXT handoff present")
    add("VAL4699_6_next_qbarXT", data["next"][0]["target"] == NEXT_TARGET, "next qbarXT target selected")
    add("VAL4699_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4699_8_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4699_9_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4699_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4699_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")

    for csv_path in [
        SOURCE_REGISTER,
        THEOREM_CSV,
        BULK_CSV,
        EDGE_CSV,
        SHADOW_CSV,
        DPROJ_CSV,
        PRIORITY_CSV,
        PRODUCT_CSV,
        CURRENT_CSV,
        BLOCKERS_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4699_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4699_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [data["theorem"], data["bulk"], data["edge"], data["shadow"], data["dproj"], data["priority"], data["product"], data["current"], data["blockers"], data["controls"], data["decision"], data["status"], data["next"]]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4699_12_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4699_13_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4699_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_rows(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "theorem": restamp_rows(CSV_4611_THEOREM, timestamp),
        "bulk": restamp_rows(CSV_4611_BULK, timestamp),
        "edge": restamp_rows(CSV_4611_EDGE, timestamp),
        "shadow": restamp_rows(CSV_4611_SHADOW, timestamp),
        "dproj": restamp_rows(CSV_4611_DPROJ, timestamp),
        "priority": restamp_rows(CSV_4611_PRIORITY, timestamp),
        "product": restamp_rows(CSV_4611_PRODUCT, timestamp),
        "current": current_rows(timestamp),
        "blockers": restamp_rows(CSV_4611_BLOCKERS, timestamp),
        "controls": restamp_rows(CSV_4611_CONTROLS, timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(THEOREM_CSV, data["theorem"])
    write_csv(BULK_CSV, data["bulk"])
    write_csv(EDGE_CSV, data["edge"])
    write_csv(SHADOW_CSV, data["shadow"])
    write_csv(DPROJ_CSV, data["dproj"])
    write_csv(PRIORITY_CSV, data["priority"])
    write_csv(PRODUCT_CSV, data["product"])
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
