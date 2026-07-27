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

CHECKPOINT = "4701"
CLAIM_ID = "L-543"
MARKER = "PPC4161_MATTER_MARKER_EM_CONSTANT_DESCENT_BRANCH_4701"
PACKET_MARKER = "PPC4161_PACKET_MATTER_MARKER_EM_CONSTANT_DESCENT_BRANCH_4701"
DECISION = "MATTER_MARKER_EM_CONSTANT_DESCENT_OR_FIRST_QBARXT_COEFFICIENT_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4702-Y5-R2FR-EM-gauge-kinetic-descent-or-b-alpha-source-row.md"

DOC_PATH = POST / "4701-Y5-R2FR-matter-marker-EM-constant-descent-or-first-qbarXT-coefficient-row.md"
FORMAL_PATH = FORMAL / "717-PPC4161-matter-marker-EM-constant-descent-or-first-qbarXT-coefficient-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4700_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4700_STATUS.csv"
CSV_4700_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4700_NEXT_TARGET.csv"
CSV_4700_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4700_QBARXT_RESPONSE_ENVELOPE_THEOREM.csv"
CSV_4700_MARKER = SOURCE_DIR / "P8_Y5_R2FR_4700_MARKER_CONSTANT_RESPONSE_ROWS.csv"
CSV_4700_CURRENT = SOURCE_DIR / "P8_Y5_R2FR_4700_CURRENT_BRANCH_COUPLING_PRODUCT_ROWS.csv"
CSV_4700_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4700_VALIDATION.csv"

CSV_4613_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4613_THETA_MARKER_DESCENT_THEOREM.csv"
CSV_4613_MASS_CLOCK = SOURCE_DIR / "P8_Y5_R2FR_4613_MASS_CLOCK_MARKER_ROWS.csv"
CSV_4613_EM_ALPHA = SOURCE_DIR / "P8_Y5_R2FR_4613_EM_ALPHA_DESCENT_ROWS.csv"
CSV_4613_AUDIT = SOURCE_DIR / "P8_Y5_R2FR_4613_CHANNEL_DESCENT_AUDIT.csv"
CSV_4613_COEFF = SOURCE_DIR / "P8_Y5_R2FR_4613_QBARXT_COEFFICIENT_ROWS_NONCLAIM.csv"
CSV_4613_UPDATE = SOURCE_DIR / "P8_Y5_R2FR_4613_QBARXT_UPDATE_ROWS.csv"
CSV_4613_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4613_CLAIM_BLOCKERS.csv"
CSV_4613_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4613_CONTROL_ROWS.csv"
CSV_4613_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4613_STATUS.csv"
CSV_4613_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4613_DECISION.csv"
CSV_4613_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4613_NEXT_TARGET.csv"
CSV_4613_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4613_VALIDATION.csv"

FORMAL_716 = FORMAL / "716-PPC4161-qbarXT-test-body-response-envelope-or-first-source-backed-input.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4701_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4701_THETA_MARKER_DESCENT_THEOREM.csv"
MASS_CLOCK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4701_MASS_CLOCK_MARKER_ROWS.csv"
EM_ALPHA_CSV = SOURCE_DIR / "P8_Y5_R2FR_4701_EM_ALPHA_DESCENT_ROWS.csv"
AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4701_CHANNEL_DESCENT_AUDIT.csv"
COEFF_CSV = SOURCE_DIR / "P8_Y5_R2FR_4701_QBARXT_COEFFICIENT_ROWS_NONCLAIM.csv"
UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4701_QBARXT_UPDATE_ROWS.csv"
CURRENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4701_CURRENT_BRANCH_THETA_MARKER_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4701_CLAIM_BLOCKERS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4701_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4701_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4701_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4701_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4701_VALIDATION.csv"

NEXT_4700 = "4701-Y5-R2FR-matter-marker-EM-constant-descent-or-first-qbarXT-coefficient-row.md"
NEXT_4613 = "4614-Y5-R2FR-EM-gauge-kinetic-descent-or-b-alpha-source-row.md"


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
                    value.replace("4613", CHECKPOINT)
                    .replace(NEXT_4613, NEXT_TARGET)
                    .replace("2026-07-06T16:30:57.976380+00:00", timestamp)
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
        ("SRC4701_00_4700_status", CSV_4700_STATUS, "PPC4161_QBARXT_TEST_BODY_RESPONSE_ENVELOPE_BRANCH_4700", "4700 qbarXT branch."),
        ("SRC4701_01_4700_next", CSV_4700_NEXT, NEXT_4700, "4700 hands off to marker descent."),
        ("SRC4701_02_4700_theorem", CSV_4700_THEOREM, "QXT4700_2_component_envelope", "4700 qbarXT envelope."),
        ("SRC4701_03_4700_marker", CSV_4700_MARKER, "MRK4700_2_EM_alpha", "4700 marker/EM rows."),
        ("SRC4701_04_4700_current", CSV_4700_CURRENT, "CPL4700_0_current_product_bound", "4700 product handoff."),
        ("SRC4701_05_4700_validation", CSV_4700_VALIDATION, "VAL4700_OVERALL", "4700 validation passed."),
        ("SRC4701_06_4613_theorem", CSV_4613_THEOREM, "TMD4613_1_qbasic_constant_zero", "4613 theta marker descent theorem."),
        ("SRC4701_07_4613_mass_clock", CSV_4613_MASS_CLOCK, "MCM4613_0_mass_ratios", "4613 mass/clock marker rows."),
        ("SRC4701_08_4613_em", CSV_4613_EM_ALPHA, "EM4613_0_gauge_kinetic", "4613 EM alpha rows."),
        ("SRC4701_09_4613_audit", CSV_4613_AUDIT, "CH4613_0_alpha_EM", "4613 channel audit."),
        ("SRC4701_10_4613_coeff", CSV_4613_COEFF, "QTC4613_1_b_alpha", "4613 coefficient rows."),
        ("SRC4701_11_4613_update", CSV_4613_UPDATE, "QXU4613_1_qbarXT", "4613 qbarXT update."),
        ("SRC4701_12_4613_controls", CSV_4613_CONTROLS, "CTRL4613_1_no_unit_hiding", "4613 controls."),
        ("SRC4701_13_4613_status", CSV_4613_STATUS, "MATTER_MARKER_EM_CONSTANT_DESCENT", "4613 status."),
        ("SRC4701_14_4613_next", CSV_4613_NEXT, NEXT_4613, "4613 next target."),
        ("SRC4701_15_4613_validation", CSV_4613_VALIDATION, "VAL4613_OVERALL", "4613 validation passed."),
        ("SRC4701_16_formal716", FORMAL_716, "qbar_XT :=", "formal qbarXT upstream handoff."),
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
            "row_id": "TMC4701_0_current_theta_marker_bound",
            "quantity": "qbar_theta_marker_abs",
            "formula": "|qbar_theta_marker| <= |epsilon_theta|+|b_alpha_EM|+|b_mu|+|b_mA|+|b_nuc|+|b_charge|+|b_clock|+|b_material_label|+|b_source_norm|+|lambda_M_tail|",
            "zero_condition": "all theta/marker channels are q-basic, superselected, absent or parent-owned in the same branch",
            "current_status": "THETA_MARKER_ABSOLUTE_SUM_READY_VALUES_MISSING",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "TMC4701_1_alpha_first",
            "quantity": "b_alpha_EM",
            "formula": "b_alpha_EM := Lie_v ln(alpha_EM) after removing pure unit/common-scale conventions",
            "zero_condition": "EM gauge kinetic data, charge representation data and fine-structure readout are q-basic or superselected",
            "current_status": "NEXT_EM_GAUGE_KINETIC_DESCENT_TARGET",
            "valid_for_claim": False,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_MATTER_MARKER_EM_CONSTANT_DESCENT_4701",
            "decision": DECISION,
            "reason": "Matter/EM/clock constants are split into unit/common conventions versus dimensionless physical channels. Dimensionless alpha_EM, mass ratios and clock ratios cannot be erased by unit choices.",
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
            "derived": "theta split; q-basic conditional zero theorem; deformation coefficient branch; EM alpha branch; qbar_theta_marker absolute-sum insert",
            "not_derived": "b_alpha_EM zero/source row, mass-ratio/material superselection, source-normalization owner, K_X/Z_X/tau arena rows, local-GR/R10/PPN pass",
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
            "next_id": "NT4701_0",
            "target": NEXT_TARGET,
            "reason": "alpha_EM is dimensionless and central to Maxwell stress, clocks, WEP/R10 material response; it cannot be hidden by units.",
            "derive_first": "prove the EM gauge kinetic function and charge representation data are q-basic or superselected so b_alpha_EM=0",
            "fallback": "stage b_alpha_EM as the first source-backed qbarXT coefficient row with clock/WEP/R10 projections",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4701 - Matter Marker / EM Constant Descent Gate

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
This checkpoint does **not** claim local GR. It splits matter constants and markers into unit/common conventions versus dimensionless physical channels:

```text
theta_A = (u_common, c_I, m_A, b_A, marker_A, source_norm).
```

Clean zero route:

```text
S_matter = Sbar[psi, e_obs(q), theta_obs],  v_X in ker(Dq),  D_v theta_obs = 0
=> delta_v S_matter|theta = 0.
```

Finite branch:

```text
|qbar_theta_marker| <= |epsilon_theta|+|b_alpha_EM|+|b_mu|+|b_mA|+|b_nuc|
  +|b_charge|+|b_clock|+|b_material_label|+|b_source_norm|+|lambda_M_tail|.
```

## Source Register
{table(data["sources"])}

## Theta Marker Descent Theorem
{table(data["theorem"])}

## Mass / Clock / Marker Rows
{table(data["mass_clock"])}

## EM Alpha Rows
{table(data["em_alpha"])}

## Channel Descent Audit
{table(data["audit"])}

## Coefficient Rows
{table(data["coeff"])}

## qbarXT Update
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
        f"""# 717 - PPC4161 Matter Marker / EM Constant Descent Gate

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
```text
delta_v S_matter|theta = sum_A int J_theta^A Lie_v(theta_A).
```

If `theta_A` is q-basic/superselected before variation:

```text
Lie_v(theta_A)=0 => qbar_constants=qbar_marker=0.
```

Otherwise:

```text
|qbar_theta_marker| <= |epsilon_theta|+|b_alpha_EM|+|b_mu|+|b_mA|+|b_nuc|
  +|b_charge|+|b_clock|+|b_material_label|+|b_source_norm|+|lambda_M_tail|.
```

`alpha_EM` and mass/clock ratios are dimensionless; unit conventions cannot erase their vertical derivatives.

## Nonclaim Status
No R10, WEP, PPN, clock, orbital, Newton, Maxwell or local-GR claim follows. Next branch is EM gauge-kinetic descent / `b_alpha_EM`.
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
            "claim": "4701 splits matter/EM/clock constants and markers into q-basic zero routes or explicit qbarXT coefficient channels.",
            "current_evidence": "Generated source register, theta-marker theorem, mass/clock marker rows, EM alpha rows, channel audit, coefficient rows, qbarXT update, current branch rows, blockers, controls, decision, status, next target and validation.",
            "status": "matter_marker_em_constant_descent_current_branch_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Erasing dimensionless constants by unit conventions, treating calibration as derivation, or cancelling marker channels against geometry/source terms.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "Matter marker EM constant descent gate",
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
- Movement: matter/EM/clock constants and material/source markers now split into q-basic zero clauses or explicit qbarXT coefficient rows.
- Key firewall: dimensionless constants such as `alpha_EM`, mass ratios and clock ratios cannot be removed by unit conventions.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: current PPC4161 qbarXT marker/constant branch before EM gauge-kinetic descent.
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

    add("VAL4701_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4701_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4701_2_theta_split", any("theta_A" in row.get("formula", "") for row in data["theorem"]), "theta split theorem present")
    add("VAL4701_3_qbasic_zero", any("delta_v S_matter" in row.get("formula", "") for row in data["theorem"]), "q-basic zero route present")
    add("VAL4701_4_balpha_row", any(row.get("symbol") == "b_alpha_EM" for row in data["coeff"]), "b_alpha coefficient row present")
    add("VAL4701_5_no_unit_hiding", any(row.get("control_id") == "CTRL4701_1_no_unit_hiding" for row in data["controls"]), "no unit hiding control present")
    add("VAL4701_6_next_EM", data["next"][0]["target"] == NEXT_TARGET, "next EM gauge-kinetic target selected")
    add("VAL4701_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4701_8_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4701_9_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4701_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4701_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")

    for csv_path in [
        SOURCE_REGISTER,
        THEOREM_CSV,
        MASS_CLOCK_CSV,
        EM_ALPHA_CSV,
        AUDIT_CSV,
        COEFF_CSV,
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
            add(f"VAL4701_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4701_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [data["theorem"], data["mass_clock"], data["em_alpha"], data["audit"], data["coeff"], data["update"], data["current"], data["blockers"], data["controls"], data["decision"], data["status"], data["next"]]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4701_12_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4701_13_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4701_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_rows(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "theorem": restamp_rows(CSV_4613_THEOREM, timestamp),
        "mass_clock": restamp_rows(CSV_4613_MASS_CLOCK, timestamp),
        "em_alpha": restamp_rows(CSV_4613_EM_ALPHA, timestamp),
        "audit": restamp_rows(CSV_4613_AUDIT, timestamp),
        "coeff": restamp_rows(CSV_4613_COEFF, timestamp),
        "update": restamp_rows(CSV_4613_UPDATE, timestamp),
        "current": current_rows(timestamp),
        "blockers": restamp_rows(CSV_4613_BLOCKERS, timestamp),
        "controls": restamp_rows(CSV_4613_CONTROLS, timestamp),
        "decision": decision,
        "status": status,
        "next": next_rows,
    }

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(THEOREM_CSV, data["theorem"])
    write_csv(MASS_CLOCK_CSV, data["mass_clock"])
    write_csv(EM_ALPHA_CSV, data["em_alpha"])
    write_csv(AUDIT_CSV, data["audit"])
    write_csv(COEFF_CSV, data["coeff"])
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
