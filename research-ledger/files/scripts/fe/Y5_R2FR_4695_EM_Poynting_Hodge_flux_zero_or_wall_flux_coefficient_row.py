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

CHECKPOINT = "4695"
CLAIM_ID = "L-537"
MARKER = "PPC4161_EM_POYNTING_HODGE_FLUX_CURRENT_BRANCH_4695"
PACKET_MARKER = "PPC4161_PACKET_EM_POYNTING_HODGE_FLUX_CURRENT_BRANCH_4695"
DECISION = "EM_POYNTING_SAME_HODGE_NO_FLUX_OR_WALL_COEFFICIENT_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4696-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md"

DOC_PATH = POST / "4695-Y5-R2FR-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md"
FORMAL_PATH = FORMAL / "711-PPC4161-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4694_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4694_NEXT_TARGET.csv"
CSV_4694_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4694_STATUS.csv"
CSV_4607_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4607_EM_POYNTING_HODGE_FLUX_THEOREM.csv"
CSV_4607_HODGE = SOURCE_DIR / "P8_Y5_R2FR_4607_HODGE_OWNER_ROWS.csv"
CSV_4607_FLUX = SOURCE_DIR / "P8_Y5_R2FR_4607_POYNTING_FLUX_ROWS.csv"
CSV_4607_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4607_EM_BULK_BOUND_UPDATE_ROWS.csv"
CSV_4607_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4607_CLAIM_BLOCKERS.csv"
CSV_4607_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4607_CONTROL_ROWS.csv"
CSV_4607_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4607_STATUS.csv"
CSV_4607_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4607_NEXT_TARGET.csv"
CSV_4607_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4607_VALIDATION.csv"
CSV_4608_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4608_STATUS.csv"
CSV_4608_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4608_NEXT_TARGET.csv"
CSV_4608_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4608_VALIDATION.csv"
FORMAL_623 = FORMAL / "623-PPC4161-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md"
FORMAL_624 = FORMAL / "624-PPC4161-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4695_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4695_EM_POYNTING_HODGE_FLUX_THEOREM.csv"
HODGE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4695_HODGE_OWNER_ROWS.csv"
FLUX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4695_POYNTING_FLUX_ROWS.csv"
BOUND_CSV = SOURCE_DIR / "P8_Y5_R2FR_4695_EM_BULK_BOUND_UPDATE_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4695_CLAIM_BLOCKERS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4695_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4695_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4695_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4695_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4695_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4695_VALIDATION.csv"

NEXT_4607 = "4608-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md"
NEXT_4608 = "4609-Y5-R2FR-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md"


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
                    value.replace("4607", CHECKPOINT)
                    .replace(NEXT_4607, NEXT_TARGET)
                    .replace("2026-07-06T15:34:21.454556+00:00", timestamp)
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
        ("SRC4695_00_4694_next", CSV_4694_NEXT, "4695-Y5-R2FR-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md", "4694 selected EM/Poynting target."),
        ("SRC4695_01_4694_status", CSV_4694_STATUS, "PPC4161_QBULK_HILBERT_EM_POYNTING_CURRENT_BRANCH_4694", "4694 current branch status."),
        ("SRC4695_02_4607_theorem", CSV_4607_THEOREM, "EMF4607_3_finite_EM_bound", "4607 EM/Poynting theorem."),
        ("SRC4695_03_4607_hodge", CSV_4607_HODGE, "HG4607_2_conformal_guard", "4607 Hodge owner rows."),
        ("SRC4695_04_4607_flux", CSV_4607_FLUX, "FX4607_2_closed_domain_wall", "4607 Poynting flux rows."),
        ("SRC4695_05_4607_bound", CSV_4607_BOUND, "EB4607_1_bound_route", "4607 EM bulk update."),
        ("SRC4695_06_4607_blockers", CSV_4607_BLOCKERS, "MIS4607_1_wall_flux", "4607 blockers."),
        ("SRC4695_07_4607_controls", CSV_4607_CONTROLS, "CTRL4607_2_local_not_global", "4607 controls."),
        ("SRC4695_08_4607_status", CSV_4607_STATUS, "EM_POYNTING_SAME_HODGE_NO_FLUX_OR_WALL_COEFFICIENT_SCHEMA_READY_NONCLAIM", "4607 status."),
        ("SRC4695_09_4607_next", CSV_4607_NEXT, NEXT_4607, "4607 next target."),
        ("SRC4695_10_4607_validation", CSV_4607_VALIDATION, "VAL4607_OVERALL", "4607 validation passed."),
        ("SRC4695_11_4608_status", CSV_4608_STATUS, "RETAINED_BULK_SOURCE_CURRENT_ZERO_OR_COMPONENT_ROWS_READY_NONCLAIM", "4608 retained-current rung exists."),
        ("SRC4695_12_4608_next", CSV_4608_NEXT, NEXT_4608, "4608 next target."),
        ("SRC4695_13_4608_validation", CSV_4608_VALIDATION, "VAL4608_OVERALL", "4608 validation passed."),
        ("SRC4695_14_formal623", FORMAL_623, "S_Poynting^i=-T_EM^i_nu", "formal EM/Poynting gate."),
        ("SRC4695_15_formal624", FORMAL_624, "J_retained := J_direct", "formal retained-current handoff."),
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
        ("SURV4695_0_once_only", "c_Poynt_extra", "zero only if no extra Poynting/background source is added after T_EM", "keep once-only guard active"),
        ("SURV4695_1_hodge", "Delta_Hodge_EM_abs", "same-Hodge zero or constitutive/readout/orientation envelope remains", "return if EM branch remains live"),
        ("SURV4695_2_wall_flux", "Phi_wall_Poynting_abs", "stationary local collar zero or finite wall flux coefficient", "source if open/radiative"),
        ("SURV4695_3_nonminimal", "epsilon_nonminimal_EM", "nonminimal EM/source multiplier route remains a coefficient if unsigned", "fold into retained/source rows if needed"),
        ("SURV4695_4_retained", "Q_bulk_retained_abs", "next live bulk numerator after EM/Poynting isolation", NEXT_TARGET),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": survivor_id,
            "residual_family": family,
            "status_after_4695": status,
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
            "summary": "4695 imports the EM/Poynting same-Hodge/no-wall-flux gate. Poynting is counted once as Hilbert EM stress on the public observed-Hodge branch; if same-Hodge or no local stationary collar is unsigned, the branch becomes explicit Delta_Hodge_EM/Phi_wall_Poynting/nonminimal coefficient rows.",
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
            "derived": "once-only EM/Poynting theorem; same-Hodge conditional zero and envelope; local stationary no-wall-flux theorem and finite flux bound; EM bulk bound update",
            "not_derived": "parent-signed same-Hodge branch; numeric Delta_Hodge_EM envelope; stationary no-wall-flux proof or numeric Phi_wall_Poynting; nonminimal EM zero/bound; R10/PPN/local-GR pass",
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
            "next_id": "NT4695_0",
            "target": NEXT_TARGET,
            "reason": "After EM/Poynting is isolated, the next live bulk numerator is retained source current: J_direct, J_mem, marker/readout tails.",
            "derive_first": "prove retained/direct/memory/readout source-current silence in the same parent branch",
            "fallback": "fill Jdirect_abs, Jmem_abs, Jmarker_abs and Jreadout_abs as nonclaim source rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_documents(rows: dict[str, list[dict[str, Any]]]) -> None:
    body = f"""# 4695 - Y5/R2FR EM/Poynting Hodge Flux Zero Or Wall-Flux Coefficient Row

Marker: `{MARKER}`

Decision: `{DECISION}`

## Result

4695 imports the EM/Poynting fork:

```text
S_EM=-(4 mu0)^-1 int F wedge *_obs F
T_EM=delta S_EM/delta g_obs
S_Poynting^i=-T_EM^i_nu tau^nu
```

Zero route:

```text
Delta_Hodge_EM=c_Poynt_extra=Phi_wall_Poynting=epsilon_nonminimal_EM=0
=> Q_bulk_EM/Poynting=0.
```

Bound route:

```text
|Q_bulk_EM/Poynting| <= W_lambda_max(
  M_ref|Delta_Hodge_EM| + |c_Poynt_extra Phi_wall|
  + |Phi_wall_Poynting| + M_ref|epsilon_nonminimal_EM|
).
```

This makes the Poynting/background-field idea testable: open or radiative collars are not erased; they become sourceable wall-flux rows.

## Source Register

{table(rows["sources"])}

## EM/Poynting Hodge Flux Theorem

{table(rows["theorems"])}

## Hodge Owner Rows

{table(rows["hodge"])}

## Poynting Flux Rows

{table(rows["flux"])}

## EM Bulk Bound Update Rows

{table(rows["bounds"])}

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
    FORMAL_PATH.write_text(body.replace("# 4695 - Y5/R2FR", "# 711 - PPC4161"), encoding="utf-8")


def update_registers(timestamp: str) -> None:
    claims = read_csv(CLAIMS_PATH)
    if not any(row.get("claim_id") == CLAIM_ID for row in claims):
        fieldnames = list(claims[0].keys())
        row = {field: "" for field in fieldnames}
        row.update(
            {
                "claim_id": CLAIM_ID,
                "domain": "local_gr_empirical_interface",
                "claim": "4695 imports the EM/Poynting same-Hodge/no-wall-flux gate and turns open Poynting/background-field leakage into explicit coefficient rows.",
                "current_evidence": "Generated source register, EM/Poynting theorem, Hodge rows, flux rows, EM bulk bound update, blockers, survivor update, controls, decision, status, next target and validation.",
                "status": DECISION.lower(),
                "next_test": NEXT_TARGET,
                "key_risk": "Treating gauge covariance or stationary intuition as same-Hodge/no-flux proof, or erasing open radiative wall flux.",
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
        f"""## Local GR Parent-Derivation Update - Current EM/Poynting Hodge-Flux Gate

Marker: `{MARKER}`

4695 makes EM/Poynting local-source testable:

```text
S_Poynting^i=-T_EM^i_nu tau^nu.
```

On the same-Hodge/no-wall-flux branch it is silent. Otherwise it remains as `Delta_Hodge_EM`, `Phi_wall_Poynting` or nonminimal EM coefficients.

- claim id: `{CLAIM_ID}`
- checkpoint: `{DOC_PATH.name}`
- next: `{NEXT_TARGET}`
- timestamp_utc: `{timestamp}`
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""## PPC4161 Packet Addendum - Current EM/Poynting Hodge-Flux Gate

Marker: `{PACKET_MARKER}`

The packet now requires same-Hodge ownership and a local stationary/no-wall-flux collar before EM/Poynting is removed from Qbulk. Open/radiative collars stay as finite coefficient rows.

- flux csv: `{FLUX_CSV.name}`
- next: `{NEXT_TARGET}`
""",
    )


def validation_rows(rows: dict[str, list[dict[str, Any]]], csv_paths: list[Path]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = [
        ("VAL4695_0_sources_exist", all(row["path_exists"] for row in rows["sources"]), "all source-register paths exist"),
        ("VAL4695_1_needles_found", all(row["needle_found"] for row in rows["sources"]), "all source-register needles found"),
        ("VAL4695_2_once_only", any(row.get("theorem_id") == "EMF4695_0_once_only" for row in rows["theorems"]), "once-only theorem present"),
        ("VAL4695_3_hodge_rows", any(row.get("quantity") == "Delta_Hodge_EM_abs" for row in rows["hodge"]), "Hodge rows present"),
        ("VAL4695_4_flux_rows", any(row.get("quantity") == "Phi_wall_Poynting_abs" for row in rows["flux"]), "flux rows present"),
        ("VAL4695_5_bound_update", any(row.get("quantity") == "Q_bulk_EM_Poynting_abs" for row in rows["bounds"]), "EM bulk bound update present"),
        ("VAL4695_6_next_retained", rows["next"][0]["target"] == NEXT_TARGET, "next retained-current target selected"),
        ("VAL4695_7_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), "claims register contains L-537"),
        ("VAL4695_8_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker"),
        ("VAL4695_9_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker"),
        ("VAL4695_10_spine_marker", MARKER in text(SPINE_PATH), "spine marker written"),
        ("VAL4695_11_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written"),
    ]
    for path in csv_paths:
        try:
            parsed = read_csv(path)
            checks.append((f"VAL4695_csv_{path.stem}", bool(parsed), f"{path} parses with {len(parsed)} rows"))
        except Exception as exc:
            checks.append((f"VAL4695_csv_{path.stem}", False, repr(exc)))
    checks.append(("VAL4695_12_no_claim_rows_true", all(not row.get("valid_for_claim", False) for group in rows.values() for row in group), "generated rows keep valid_for_claim false"))
    checks.append(("VAL4695_13_pycache_absent", not (POST / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"))
    overall = all(passed for _, passed, _ in checks)
    checks.append(("VAL4695_OVERALL", overall, "PASS" if overall else "FAIL"))
    return [{"checkpoint": CHECKPOINT, "check_id": check_id, "passed": passed, "detail": detail, "valid_for_claim": False} for check_id, passed, detail in checks]


def main() -> None:
    timestamp = now()
    rows = {
        "sources": source_rows(timestamp),
        "theorems": restamp_rows(CSV_4607_THEOREM, timestamp),
        "hodge": restamp_rows(CSV_4607_HODGE, timestamp),
        "flux": restamp_rows(CSV_4607_FLUX, timestamp),
        "bounds": restamp_rows(CSV_4607_BOUND, timestamp),
        "blockers": restamp_rows(CSV_4607_BLOCKERS, timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": restamp_rows(CSV_4607_CONTROLS, timestamp),
        "decisions": decision_rows(timestamp),
        "statuses": status_rows(timestamp),
        "next": next_rows(timestamp),
    }
    csv_map = {
        SOURCE_REGISTER: rows["sources"],
        THEOREM_CSV: rows["theorems"],
        HODGE_CSV: rows["hodge"],
        FLUX_CSV: rows["flux"],
        BOUND_CSV: rows["bounds"],
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
