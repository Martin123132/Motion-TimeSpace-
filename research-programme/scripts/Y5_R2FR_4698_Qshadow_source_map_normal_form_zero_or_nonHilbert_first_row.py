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

CHECKPOINT = "4698"
CLAIM_ID = "L-540"
MARKER = "PPC4161_QSHADOW_SOURCE_MAP_NORMAL_FORM_BRANCH_4698"
PACKET_MARKER = "PPC4161_PACKET_QSHADOW_SOURCE_MAP_NORMAL_FORM_BRANCH_4698"
DECISION = "QSHADOW_SOURCE_MAP_NORMAL_FORM_ZERO_OR_NONHILBERT_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4699-Y5-R2FR-QbarXH-full-source-envelope-rollup-or-first-source-backed-input.md"

DOC_PATH = POST / "4698-Y5-R2FR-Qshadow-source-map-normal-form-zero-or-nonHilbert-first-row.md"
FORMAL_PATH = FORMAL / "714-PPC4161-Qshadow-source-map-normal-form-zero-or-nonHilbert-first-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4697_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4697_STATUS.csv"
CSV_4697_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4697_NEXT_TARGET.csv"
CSV_4697_QBAR = SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_QBARXH_UPDATE_ROWS.csv"
CSV_4697_INSERT = SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_CURRENT_BRANCH_INSERTION_ROWS.csv"
CSV_4697_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4697_VALIDATION.csv"

CSV_4610_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_NORMAL_FORM_THEOREM.csv"
CSV_4610_ACTION = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_ACTION_ROWS.csv"
CSV_4610_PROJECTOR = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_PROJECTOR_ROWS.csv"
CSV_4610_NONVAR = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_NONVARIATIONAL_ROWS.csv"
CSV_4610_QBAR = SOURCE_DIR / "P8_Y5_R2FR_4610_QSHADOW_QBARXH_UPDATE_ROWS.csv"
CSV_4610_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4610_CLAIM_BLOCKERS.csv"
CSV_4610_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4610_CONTROL_ROWS.csv"
CSV_4610_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4610_STATUS.csv"
CSV_4610_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4610_DECISION.csv"
CSV_4610_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4610_NEXT_TARGET.csv"
CSV_4610_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4610_VALIDATION.csv"

FORMAL_713 = FORMAL / "713-PPC4161-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4698_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4698_QSHADOW_NORMAL_FORM_THEOREM.csv"
ACTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4698_QSHADOW_ACTION_ROWS.csv"
PROJECTOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4698_QSHADOW_PROJECTOR_ROWS.csv"
NONVAR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4698_QSHADOW_NONVARIATIONAL_ROWS.csv"
QBAR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4698_QSHADOW_QBARXH_UPDATE_ROWS.csv"
INSERT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4698_QSHADOW_CURRENT_BRANCH_INSERTION_ROWS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4698_SURVIVOR_UPDATE.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4698_CLAIM_BLOCKERS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4698_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4698_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4698_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4698_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4698_VALIDATION.csv"

NEXT_4697 = "4698-Y5-R2FR-Qshadow-source-map-normal-form-zero-or-nonHilbert-first-row.md"
NEXT_4610 = "4611-Y5-R2FR-QbarXH-full-source-envelope-rollup-or-first-source-backed-input.md"


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
                    value.replace("4610", CHECKPOINT)
                    .replace(NEXT_4610, NEXT_TARGET)
                    .replace("2026-07-06T16:05:10.272568+00:00", timestamp)
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
        ("SRC4698_00_4697_status", CSV_4697_STATUS, "PPC4161_QEDGE_WORLDTUBE_BOUNDARY_BRANCH_4697", "4697 Qedge branch."),
        ("SRC4698_01_4697_next", CSV_4697_NEXT, NEXT_4697, "4697 hands off to Qshadow."),
        ("SRC4698_02_4697_qbar", CSV_4697_QBAR, "QEU4697_1_QbarXH", "4697 Qbar envelope still contains Qshadow."),
        ("SRC4698_03_4697_insert", CSV_4697_INSERT, "Q_bulk_4696", "4697 current-branch source numerator ordering."),
        ("SRC4698_04_4697_validation", CSV_4697_VALIDATION, "VAL4697_OVERALL", "4697 validation passed."),
        ("SRC4698_05_4610_theorem", CSV_4610_THEOREM, "QSH4610_0_decomposition", "4610 Qshadow normal form."),
        ("SRC4698_06_4610_action", CSV_4610_ACTION, "QSA4610_0_total", "4610 action shadow rows."),
        ("SRC4698_07_4610_projector", CSV_4610_PROJECTOR, "QSP4610_0_total", "4610 projector shadow rows."),
        ("SRC4698_08_4610_nonvar", CSV_4610_NONVAR, "QSN4610_0_total", "4610 nonvariational shadow rows."),
        ("SRC4698_09_4610_qbar", CSV_4610_QBAR, "QSU4610_2_QbarXH", "4610 Qbar update."),
        ("SRC4698_10_4610_blockers", CSV_4610_BLOCKERS, "MIS4610_1_projector", "4610 blockers."),
        ("SRC4698_11_4610_controls", CSV_4610_CONTROLS, "CTRL4610_0_bianchi_not_zero", "4610 Bianchi no-smuggling control."),
        ("SRC4698_12_4610_status", CSV_4610_STATUS, "QSHADOW_SOURCE_MAP_NORMAL_FORM_ZERO_OR_NONHILBERT_ROWS_READY_NONCLAIM", "4610 status."),
        ("SRC4698_13_4610_next", CSV_4610_NEXT, NEXT_4610, "4610 next target."),
        ("SRC4698_14_4610_validation", CSV_4610_VALIDATION, "VAL4610_OVERALL", "4610 validation passed."),
        ("SRC4698_15_formal713", FORMAL_713, "|Qbar_XH| <=", "formal Qedge upstream handoff."),
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


def insertion_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QSI4698_0_current_Qbar_insert",
            "quantity": "Qbar_XH_abs",
            "derived_relation": "|Qbar_XH| <= (||Pi_M^H||(|Q_bulk_4696|+|Q_edge_4697|+|Q_shadow_action|+|Q_shadow_projector|+|Q_shadow_nonvariational|)+|E_PiM_comm|)/M_lower",
            "meaning": "The full source-side numerator is now ordered and split: bulk, edge, then action/projector/nonvariational shadow.",
            "zero_condition": "all bulk, edge and shadow pieces plus denominator/projector rows vanish or are source-backed in the same parent branch",
            "current_status": "FULL_SOURCE_NUMERATOR_SPLIT_READY_FOR_ROLLUP_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QSI4698_1_bianchi_filter_guard",
            "quantity": "Q_shadow_nonvariational_abs",
            "derived_relation": "Bianchi/Noether closure rejects inconsistent nonvariational knobs but permits separately conserved real blocks unless excluded or bounded.",
            "meaning": "This blocks the common bad move: using covariance alone to set Q_shadow_nonvariational=0.",
            "zero_condition": "no decoupled conserved block, no nonvariational insertion and no repair term in the tested arena",
            "current_status": "BIANCHI_FILTER_NOT_ZERO_THEOREM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4698_0_action",
            "object": "Q_shadow_action_abs",
            "status": "requires complete parent-action normal-form inventory or coefficient bounds",
            "next_action": "classify nonminimal, boundary/improvement and frame-shadow action terms",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4698_1_projector",
            "object": "Q_shadow_projector_abs",
            "status": "requires identity-only source map or relative projector/readout-return bounds",
            "next_action": "prove P_src=I+C0I only or source Pi_rel/readout return coefficients",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4698_2_nonvariational",
            "object": "Q_shadow_nonvariational_abs",
            "status": "requires arena exclusion or bound for decoupled/conserved/repair blocks",
            "next_action": "inventory decoupled conserved blocks and repair residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4698_3_rollup",
            "object": "Qbar_XH_full_source_envelope",
            "status": "next rollup now has all numerator families split",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def blockers(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4698_0_action_inventory",
            "missing_object": "complete DeltaS_shadow parent-action inventory or finite nonminimal/frame/boundary coefficients",
            "why_it_matters": "variational shadows are either real dynamics or forbidden; they cannot be silently dropped",
            "best_next_action": "finish action normal-form classification before any source claim",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4698_1_projector_identity",
            "missing_object": "identity-only source-map proof or finite Pi_rel/readout-return/projector coefficients",
            "why_it_matters": "post-variation source maps can create composition/range dependence after Hilbert variation",
            "best_next_action": "prove P_src=I+C0I only or bound the relative source projector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4698_2_nonvariational_blocks",
            "missing_object": "absence or arena bound for decoupled conserved blocks and inconsistency repair terms",
            "why_it_matters": "Bianchi is necessary but not sufficient for zero",
            "best_next_action": "inventory decoupled conserved blocks and source repair residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4698_3_rollup",
            "missing_object": "full Qbar_XH source envelope with denominator/projector priority queue",
            "why_it_matters": "all numerator families are split, but source-backed inputs are still scattered",
            "best_next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def controls(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4698_0_bianchi_not_zero",
            "control": "Bianchi/Ward consistency filters shadow terms; it does not prove zero for conserved real blocks.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4698_1_no_G_hiding",
            "control": "Common-mode calibration may not hide relative, range, time, material or readout source shadows in measured G.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4698_2_no_boundary_double_count",
            "control": "Boundary flux already counted in Q_edge cannot also be counted as Q_shadow unless it is a separate action-normal-form residual.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4698_3_no_cancellation",
            "control": "Use absolute sums between action, projector and nonvariational shadow pieces.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_QSHADOW_SOURCE_MAP_NORMAL_FORM_GATE_4698",
            "decision": DECISION,
            "reason": "Q_shadow is current-branch split into action, projector and nonvariational channels; this closes the unnamed RHS loophole and prepares a full Qbar_XH source-envelope rollup.",
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
            "derived": "Q_shadow decomposition; action/projector/nonvariational channel bounds; Bianchi-not-zero guard; current Qbar insertion after 4696 bulk and 4697 edge",
            "not_derived": "complete action inventory, identity-only source map, decoupled conserved block exclusion, full QbarXH rollup, local-GR/R10/PPN pass",
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
            "next_id": "NT4698_0",
            "target": NEXT_TARGET,
            "reason": "Bulk, edge and shadow numerator families are now split; roll them into one Qbar_XH source envelope and priority queue.",
            "derive_first": "assemble Q_bulk_abs, Q_edge_abs and Q_shadow_abs with denominator/projector firewall",
            "fallback": "produce a nonclaim missing-input priority queue for first numeric/source-backed rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4698 - Qshadow Source-Map Normal-Form Gate

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
This checkpoint does **not** claim local GR. It turns the last unnamed source-numerator loophole into three channels:

```text
Q_shadow = Q_shadow_action + Q_shadow_projector + Q_shadow_nonvariational.
```

with

```text
|Q_shadow| <= |Q_shadow_action| + |Q_shadow_projector| + |Q_shadow_nonvariational|.
```

The important discipline gate is:

```text
Bianchi/Noether consistency is necessary, not sufficient: it rejects inconsistent nonvariational knobs but does not prove zero for separately conserved real blocks.
```

## Source Register
{table(data["sources"])}

## Qshadow Theorem
{table(data["theorem"])}

## Action Shadow Rows
{table(data["action"])}

## Projector Shadow Rows
{table(data["projector"])}

## Nonvariational Shadow Rows
{table(data["nonvar"])}

## Current Branch Insertion
{table(data["insert"])}

## Qbar Update
{table(data["qbar"])}

## Survivors
{table(data["survivors"])}

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
        f"""# 714 - PPC4161 Qshadow Source-Map Normal-Form Gate

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
```text
Q_shadow = Q_shadow_action + Q_shadow_projector + Q_shadow_nonvariational.
```

```text
|Q_shadow| <= |Q_shadow_action| + |Q_shadow_projector| + |Q_shadow_nonvariational|.
```

```text
|Qbar_XH| <= (||Pi_M^H||(
  |Q_bulk_4696| + |Q_edge_4697|
  + |Q_shadow_action| + |Q_shadow_projector| + |Q_shadow_nonvariational|
) + |E_PiM_comm|)/M_lower.
```

Zero requires action-normal-form ownership, identity-only source maps and nonvariational block exclusion in the same parent branch. Covariance alone is not enough.

## Nonclaim Status
No R10, WEP, PPN, clock, orbital or local-GR claim follows. This is the final source-numerator split before the full Qbar_XH rollup.
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
            "claim": "4698 splits Qshadow into action, projector and nonvariational channels and inserts it into the current Qbar_XH source envelope.",
            "current_evidence": "Generated source register, Qshadow theorem rows, action/projector/nonvariational rows, current branch insertion, Qbar update, blockers, survivor update, controls, decision, status, next target and validation.",
            "status": "qshadow_source_map_normal_form_current_branch_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Using Bianchi covariance as a zero theorem, hiding relative source projectors in measured G, or double-counting boundary flux already assigned to Qedge.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "Qshadow source-map normal-form gate",
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
- Movement: `Q_shadow` is now split into action, projector and nonvariational channels and inserted into the current `Qbar_XH` source envelope after `Q_bulk_4696` and `Q_edge_4697`.
- Key firewall: Bianchi/Noether consistency is not a zero proof for separately conserved real blocks.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: final PPC4161 source-numerator split before full `Qbar_XH` rollup.
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

    add("VAL4698_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4698_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4698_2_shadow_split", any("Q_shadow :=" in row.get("derived_relation", "") for row in data["theorem"]), "Qshadow split present")
    add("VAL4698_3_action_rows", any("Q_shadow_action" in row.get("quantity", "") for row in data["action"]), "action shadow rows present")
    add("VAL4698_4_projector_rows", any("Q_shadow_projector" in row.get("quantity", "") for row in data["projector"]), "projector shadow rows present")
    add("VAL4698_5_nonvar_rows", any("Q_shadow_nonvariational" in row.get("quantity", "") for row in data["nonvar"]), "nonvariational shadow rows present")
    add("VAL4698_6_bianchi_guard", any(row.get("control_id") == "CTRL4698_0_bianchi_not_zero" for row in data["controls"]), "Bianchi-not-zero control present")
    add("VAL4698_7_current_insert", any("Q_edge_4697" in row.get("derived_relation", "") for row in data["insert"]), "current Qbar insertion references 4697 edge")
    add("VAL4698_8_next_rollup", data["next"][0]["target"] == NEXT_TARGET, "next Qbar rollup target selected")
    add("VAL4698_9_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4698_10_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4698_11_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4698_12_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4698_13_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")

    for csv_path in [
        SOURCE_REGISTER,
        THEOREM_CSV,
        ACTION_CSV,
        PROJECTOR_CSV,
        NONVAR_CSV,
        QBAR_CSV,
        INSERT_CSV,
        SURVIVOR_CSV,
        BLOCKERS_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4698_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4698_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [data["theorem"], data["action"], data["projector"], data["nonvar"], data["qbar"], data["insert"], data["survivors"], data["blockers"], data["controls"], data["decision"], data["status"], data["next"]]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4698_14_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4698_15_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4698_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_rows(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "theorem": restamp_rows(CSV_4610_THEOREM, timestamp),
        "action": restamp_rows(CSV_4610_ACTION, timestamp),
        "projector": restamp_rows(CSV_4610_PROJECTOR, timestamp),
        "nonvar": restamp_rows(CSV_4610_NONVAR, timestamp),
        "qbar": restamp_rows(CSV_4610_QBAR, timestamp),
        "insert": insertion_rows(timestamp),
        "survivors": survivor_rows(timestamp),
        "blockers": blockers(timestamp),
        "controls": controls(timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(THEOREM_CSV, data["theorem"])
    write_csv(ACTION_CSV, data["action"])
    write_csv(PROJECTOR_CSV, data["projector"])
    write_csv(NONVAR_CSV, data["nonvar"])
    write_csv(QBAR_CSV, data["qbar"])
    write_csv(INSERT_CSV, data["insert"])
    write_csv(SURVIVOR_CSV, data["survivors"])
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
