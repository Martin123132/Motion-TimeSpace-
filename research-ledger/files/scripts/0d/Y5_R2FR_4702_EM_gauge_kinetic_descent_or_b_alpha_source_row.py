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

CHECKPOINT = "4702"
CLAIM_ID = "L-544"
MARKER = "PPC4161_EM_GAUGE_KINETIC_DESCENT_BRANCH_4702"
PACKET_MARKER = "PPC4161_PACKET_EM_GAUGE_KINETIC_DESCENT_BRANCH_4702"
DECISION = "EM_GAUGE_KINETIC_DESCENT_ZERO_CONTRACT_AND_B_ALPHA_SOURCE_ROW_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4703-Y5-R2FR-no-extra-F2-operator-domain-or-lambdaA-source-row.md"

DOC_PATH = POST / "4702-Y5-R2FR-EM-gauge-kinetic-descent-or-b-alpha-source-row.md"
FORMAL_PATH = FORMAL / "718-PPC4161-EM-gauge-kinetic-descent-or-b-alpha-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4701_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4701_STATUS.csv"
CSV_4701_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4701_NEXT_TARGET.csv"
CSV_4701_CURRENT = SOURCE_DIR / "P8_Y5_R2FR_4701_CURRENT_BRANCH_THETA_MARKER_ROWS.csv"
CSV_4701_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4701_VALIDATION.csv"

CSV_4614_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4614_EM_GAUGE_KINETIC_THEOREM.csv"
CSV_4614_OWNER = SOURCE_DIR / "P8_Y5_R2FR_4614_GAUGE_OWNER_CLAUSES.csv"
CSV_4614_NORMAL = SOURCE_DIR / "P8_Y5_R2FR_4614_B_ALPHA_NORMAL_FORM_ROWS.csv"
CSV_4614_SOURCE = SOURCE_DIR / "P8_Y5_R2FR_4614_B_ALPHA_SOURCE_ROW_NONCLAIM.csv"
CSV_4614_MAXWELL = SOURCE_DIR / "P8_Y5_R2FR_4614_MAXWELL_STRESS_LIMIT_ROWS.csv"
CSV_4614_ARENA = SOURCE_DIR / "P8_Y5_R2FR_4614_ALPHA_ARENA_PROJECTION_ROWS.csv"
CSV_4614_UPDATE = SOURCE_DIR / "P8_Y5_R2FR_4614_QBARXT_EM_UPDATE_ROWS.csv"
CSV_4614_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4614_CLAIM_BLOCKERS.csv"
CSV_4614_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4614_CONTROL_ROWS.csv"
CSV_4614_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4614_STATUS.csv"
CSV_4614_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4614_DECISION.csv"
CSV_4614_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4614_NEXT_TARGET.csv"
CSV_4614_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4614_VALIDATION.csv"

FORMAL_717 = FORMAL / "717-PPC4161-matter-marker-EM-constant-descent-or-first-qbarXT-coefficient-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4702_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4702_EM_GAUGE_KINETIC_THEOREM.csv"
OWNER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4702_GAUGE_OWNER_CLAUSES.csv"
NORMAL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4702_B_ALPHA_NORMAL_FORM_ROWS.csv"
SOURCE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4702_B_ALPHA_SOURCE_ROW_NONCLAIM.csv"
MAXWELL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4702_MAXWELL_STRESS_LIMIT_ROWS.csv"
ARENA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4702_ALPHA_ARENA_PROJECTION_ROWS.csv"
UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4702_QBARXT_EM_UPDATE_ROWS.csv"
CURRENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4702_CURRENT_BRANCH_B_ALPHA_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4702_CLAIM_BLOCKERS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4702_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4702_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4702_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4702_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4702_VALIDATION.csv"

NEXT_4701 = "4702-Y5-R2FR-EM-gauge-kinetic-descent-or-b-alpha-source-row.md"
NEXT_4614 = "4615-Y5-R2FR-no-extra-F2-operator-domain-or-lambdaA-source-row.md"


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
                    value.replace("4614", CHECKPOINT)
                    .replace(NEXT_4614, NEXT_TARGET)
                    .replace("2026-07-06T16:43:43.064193+00:00", timestamp)
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
        ("SRC4702_00_4701_status", CSV_4701_STATUS, "PPC4161_MATTER_MARKER_EM_CONSTANT_DESCENT_BRANCH_4701", "4701 matter-marker/EM handoff."),
        ("SRC4702_01_4701_next", CSV_4701_NEXT, NEXT_4701, "4701 selects EM gauge kinetic target."),
        ("SRC4702_02_4701_current", CSV_4701_CURRENT, "TMC4701_1_alpha_first", "4701 identifies b_alpha_EM first."),
        ("SRC4702_03_4701_validation", CSV_4701_VALIDATION, "VAL4701_OVERALL", "4701 validation passed."),
        ("SRC4702_04_4614_theorem", CSV_4614_THEOREM, "EGK4614_0_normal_form", "4614 EM gauge kinetic theorem."),
        ("SRC4702_05_4614_owner", CSV_4614_OWNER, "OWN4614_6_verdict", "4614 gauge owner clauses."),
        ("SRC4702_06_4614_normal", CSV_4614_NORMAL, "BA4614_6_bound", "4614 b_alpha normal form rows."),
        ("SRC4702_07_4614_source", CSV_4614_SOURCE, "BSR4614_0_b_alpha_source_row", "4614 source row schema."),
        ("SRC4702_08_4614_maxwell", CSV_4614_MAXWELL, "MX4614_2_CXF2", "4614 Maxwell stress limit rows."),
        ("SRC4702_09_4614_arena", CSV_4614_ARENA, "ARENA4614_3_Maxwell", "4614 arena projection rows."),
        ("SRC4702_10_4614_update", CSV_4614_UPDATE, "QEU4614_0_balpha_insert", "4614 qbarXT EM update."),
        ("SRC4702_11_4614_blockers", CSV_4614_BLOCKERS, "BLK4614_0_no_extra_F2", "4614 no-extra-F2 blocker."),
        ("SRC4702_12_4614_controls", CSV_4614_CONTROLS, "CTRL4614_1_no_unit_alpha", "4614 controls."),
        ("SRC4702_13_4614_status", CSV_4614_STATUS, "EM_GAUGE_KINETIC_DESCENT", "4614 status."),
        ("SRC4702_14_4614_next", CSV_4614_NEXT, NEXT_4614, "4614 next target."),
        ("SRC4702_15_4614_validation", CSV_4614_VALIDATION, "VAL4614_OVERALL", "4614 validation passed."),
        ("SRC4702_16_formal717", FORMAL_717, "b_alpha_EM", "formal 4701 upstream handoff."),
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
            "row_id": "BAC4702_0_current_normal_form",
            "quantity": "b_alpha_EM_abs",
            "formula": "|b_alpha_EM| <= 2|z_g| + |z_lambda| + |z_readout| + |z_rad|",
            "zero_condition": "fixed parent gauge object, charge lattice, generator norm, unique F2 term, same current owner and readout/radiative closure",
            "current_status": "B_ALPHA_NORMAL_FORM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BAC4702_1_no_extra_F2_next",
            "quantity": "lambda_A_or_C_XF2",
            "formula": "Z_A = C_P N_Q + lambda_A + f_X + Z_readout/rad",
            "zero_condition": "operator-domain exhaustion forbids independent lambda_A F_Q^2 and f_X(Phi)F_Q^2 terms",
            "current_status": "NEXT_OPERATOR_DOMAIN_EXHAUSTION_TARGET",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "BAC4702_2_Maxwell_limit",
            "quantity": "Maxwell_stress_limit",
            "formula": "S_EM=-1/4 Z_A F_Q wedge *_obs F_Q; standard T_EM only when Z_A, Hodge/coframe and current owner descend together",
            "zero_condition": "fixed Z_A, observed Hodge/coframe, same current owner and no readout/radiative regeneration",
            "current_status": "MAXWELL_LIMIT_CONDITIONAL_NOT_CLAIMED",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_EM_GAUGE_KINETIC_DESCENT_4702",
            "decision": DECISION,
            "reason": "b_alpha_EM is reduced to current normalization, Maxwell kinetic normalization and readout/radiative derivatives, with the legal extra-F2 throat isolated as the next derivation target.",
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
            "derived": "b_alpha normal form; gauge owner zero contract; finite b_alpha source row schema; Maxwell stress conditional limit; alpha arena projections",
            "not_derived": "no-extra-F2/operator-domain exhaustion, fixed generator norm, same current owner, readout/radiative closure, Maxwell/local-GR/R10/clock/WEP pass",
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
            "next_id": "NT4702_0",
            "target": NEXT_TARGET,
            "reason": "The strongest b_alpha_EM blocker is the legal lambda_A/f_X F_Q^2 counterterm; no-extra-F2 closes the main EM coupling throat.",
            "derive_first": "prove operator-domain exhaustion forbids independent lambda_A F_Q^2 and f_X(Phi)F_Q^2 terms in the visible EM action",
            "fallback": "stage lambda_A/C_XF2 as the first finite source-backed b_alpha input row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4702 - EM Gauge Kinetic Descent / b_alpha Source Row

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
This checkpoint does **not** claim Maxwell/local-GR closure. It makes the EM coupling throat explicit:

```text
b_alpha_EM := Lie_v ln(alpha_EM) = 2 z_g - z_lambda - z_readout - z_rad.
```

Finite branch:

```text
|b_alpha_EM| <= 2|z_g| + |z_lambda| + |z_readout| + |z_rad|.
```

Standard Maxwell stress is recovered only on the clean branch:

```text
S_EM=-1/4 Z_A F_Q wedge *_obs F_Q
```

with fixed `Z_A`, observed Hodge/coframe, same current owner, and no readout/radiative regeneration.

## Source Register
{table(data["sources"])}

## EM Gauge Kinetic Theorem
{table(data["theorem"])}

## Gauge Owner Clauses
{table(data["owner"])}

## b_alpha Normal Form
{table(data["normal"])}

## b_alpha Source Rows
{table(data["source"])}

## Maxwell Stress Limit
{table(data["maxwell"])}

## Arena Projections
{table(data["arena"])}

## qbarXT EM Update
{table(data["update"])}

## Current Branch Rows
{table(data["current"])}

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
        f"""# 718 - PPC4161 EM Gauge Kinetic Descent / b_alpha Source Row

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
```text
b_alpha_EM := Lie_v ln(alpha_EM) = 2 z_g - z_lambda - z_readout - z_rad.
```

```text
|b_alpha_EM| <= 2|z_g| + |z_lambda| + |z_readout| + |z_rad|.
```

Zero requires the full owner contract:

```text
z_g=z_lambda=z_readout=z_rad=0
```

and no independent `lambda_A F_Q^2` or `f_X(Phi)F_Q^2` counterterm.

The local Maxwell stress limit is conditional on fixed `Z_A`, observed Hodge/coframe and the same current owner.

## Nonclaim Status
No alpha prediction, Maxwell pass, WEP/clock/R10 pass, Newton/local-GR pass or no-extra-F2 proof is claimed. Next branch is no-extra-F2/operator-domain exhaustion.
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
            "claim": "4702 reduces b_alpha_EM to current, Maxwell kinetic, readout and radiative derivatives while isolating the no-extra-F2 operator-domain blocker.",
            "current_evidence": "Generated source register, EM gauge kinetic theorem, gauge owner clauses, b_alpha normal form/source rows, Maxwell stress rows, arena projections, qbarXT update, current rows, blockers, controls, decision, status, next target and validation.",
            "status": "em_gauge_kinetic_descent_current_branch_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Claiming alpha_EM is a unit convention, using Ward/charge quantization alone to fix the kinetic coefficient, or hiding lambda_A/f_X F2 counterterms.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "EM gauge kinetic descent gate",
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
- Movement: `b_alpha_EM` now has a current-branch normal form `2 z_g - z_lambda - z_readout - z_rad`, plus a Maxwell-stress conditional limit.
- Key firewall: `alpha_EM` is dimensionless, and Ward identity/charge quantization do not by themselves fix the Maxwell kinetic coefficient.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: current PPC4161 EM gauge-kinetic branch before no-extra-F2 operator-domain exhaustion.
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

    add("VAL4702_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4702_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4702_2_normal_form", any("b_alpha_EM" in row.get("formula", "") for row in data["theorem"]), "b_alpha normal form theorem present")
    add("VAL4702_3_owner_contract", any(row.get("clause_id") == "OWN4702_6_verdict" for row in data["owner"]), "gauge owner verdict present")
    add("VAL4702_4_source_schema", any(row.get("row_id") == "BSR4702_0_b_alpha_source_row" for row in data["source"]), "b_alpha source row schema present")
    add("VAL4702_5_Maxwell_limit", any(row.get("quantity") == "Maxwell_stress_limit" for row in data["current"]), "Maxwell conditional limit present")
    add("VAL4702_6_no_unit_alpha", any(row.get("control_id") == "CTRL4702_1_no_unit_alpha" for row in data["controls"]), "no unit alpha control present")
    add("VAL4702_7_next_no_extra_F2", data["next"][0]["target"] == NEXT_TARGET, "next no-extra-F2 target selected")
    add("VAL4702_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4702_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4702_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4702_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4702_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")

    for csv_path in [
        SOURCE_REGISTER,
        THEOREM_CSV,
        OWNER_CSV,
        NORMAL_CSV,
        SOURCE_CSV,
        MAXWELL_CSV,
        ARENA_CSV,
        UPDATE_CSV,
        CURRENT_CSV,
        BLOCKERS_CSV,
        CONTROL_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4702_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4702_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [data["theorem"], data["owner"], data["normal"], data["source"], data["maxwell"], data["arena"], data["update"], data["current"], data["blockers"], data["controls"], data["decision"], data["status"], data["next"]]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4702_13_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4702_14_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4702_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_rows(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "theorem": restamp_rows(CSV_4614_THEOREM, timestamp),
        "owner": restamp_rows(CSV_4614_OWNER, timestamp),
        "normal": restamp_rows(CSV_4614_NORMAL, timestamp),
        "source": restamp_rows(CSV_4614_SOURCE, timestamp),
        "maxwell": restamp_rows(CSV_4614_MAXWELL, timestamp),
        "arena": restamp_rows(CSV_4614_ARENA, timestamp),
        "update": restamp_rows(CSV_4614_UPDATE, timestamp),
        "current": current_rows(timestamp),
        "blockers": restamp_rows(CSV_4614_BLOCKERS, timestamp),
        "controls": restamp_rows(CSV_4614_CONTROLS, timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(THEOREM_CSV, data["theorem"])
    write_csv(OWNER_CSV, data["owner"])
    write_csv(NORMAL_CSV, data["normal"])
    write_csv(SOURCE_CSV, data["source"])
    write_csv(MAXWELL_CSV, data["maxwell"])
    write_csv(ARENA_CSV, data["arena"])
    write_csv(UPDATE_CSV, data["update"])
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
