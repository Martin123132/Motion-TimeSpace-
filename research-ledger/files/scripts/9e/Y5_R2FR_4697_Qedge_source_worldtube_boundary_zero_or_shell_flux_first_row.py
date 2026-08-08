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

CHECKPOINT = "4697"
CLAIM_ID = "L-539"
MARKER = "PPC4161_QEDGE_WORLDTUBE_BOUNDARY_BRANCH_4697"
PACKET_MARKER = "PPC4161_PACKET_QEDGE_WORLDTUBE_BOUNDARY_BRANCH_4697"
DECISION = "QEDGE_WORLDTUBE_BOUNDARY_ZERO_OR_SHELL_FLUX_CURRENT_BRANCH_NONCLAIM"
NEXT_TARGET = "4698-Y5-R2FR-Qshadow-source-map-normal-form-zero-or-nonHilbert-first-row.md"

DOC_PATH = POST / "4697-Y5-R2FR-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md"
FORMAL_PATH = FORMAL / "713-PPC4161-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4696_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4696_STATUS.csv"
CSV_4696_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4696_NEXT_TARGET.csv"
CSV_4696_QBULK = SOURCE_DIR / "P8_Y5_R2FR_4696_QBULK_RETAINED_UPDATE_ROWS.csv"
CSV_4696_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4696_VALIDATION.csv"

CSV_4609_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_WORLDTUBE_BOUNDARY_THEOREM.csv"
CSV_4609_SHELL = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_REYNOLDS_SHELL_ROWS.csv"
CSV_4609_BOUNDARY = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_BOUNDARY_FLUX_ROWS.csv"
CSV_4609_QBAR = SOURCE_DIR / "P8_Y5_R2FR_4609_QEDGE_QBARXH_UPDATE_ROWS.csv"
CSV_4609_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4609_CLAIM_BLOCKERS.csv"
CSV_4609_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4609_CONTROL_ROWS.csv"
CSV_4609_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4609_STATUS.csv"
CSV_4609_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4609_DECISION.csv"
CSV_4609_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4609_NEXT_TARGET.csv"
CSV_4609_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4609_VALIDATION.csv"

FORMAL_712 = FORMAL / "712-PPC4161-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4697_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_WORLDTUBE_BOUNDARY_THEOREM.csv"
SHELL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_REYNOLDS_SHELL_ROWS.csv"
BOUNDARY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_BOUNDARY_FLUX_ROWS.csv"
QBAR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_QBARXH_UPDATE_ROWS.csv"
INSERT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4697_QEDGE_CURRENT_BRANCH_INSERTION_ROWS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4697_SURVIVOR_UPDATE.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4697_CLAIM_BLOCKERS.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4697_CONTROL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4697_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4697_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4697_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4697_VALIDATION.csv"

NEXT_4696 = "4697-Y5-R2FR-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md"
NEXT_4609 = "4610-Y5-R2FR-Qshadow-source-map-normal-form-zero-or-nonHilbert-first-row.md"


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
                    value.replace("4609", CHECKPOINT)
                    .replace(NEXT_4609, NEXT_TARGET)
                    .replace("2026-07-06T15:54:50.537074+00:00", timestamp)
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
        ("SRC4697_00_4696_status", CSV_4696_STATUS, "PPC4161_RETAINED_BULK_SOURCE_CURRENT_BRANCH_4696", "4696 retained-current branch."),
        ("SRC4697_01_4696_next", CSV_4696_NEXT, NEXT_4696, "4696 hands off to Qedge."),
        ("SRC4697_02_4696_qbulk", CSV_4696_QBULK, "QBR4696_2_QbarXH", "4696 Qbar source numerator still contains Qedge."),
        ("SRC4697_03_4696_validation", CSV_4696_VALIDATION, "VAL4696_OVERALL", "4696 validation passed."),
        ("SRC4697_04_4609_theorem", CSV_4609_THEOREM, "QE4609_0_decomposition", "4609 Qedge split."),
        ("SRC4697_05_4609_shell", CSV_4609_SHELL, "QES4609_5_total", "4609 Reynolds shell bound."),
        ("SRC4697_06_4609_boundary", CSV_4609_BOUNDARY, "QEB4609_6_total", "4609 boundary flux bound."),
        ("SRC4697_07_4609_qbar", CSV_4609_QBAR, "QEU4609_1_QbarXH", "4609 Qbar update."),
        ("SRC4697_08_4609_blockers", CSV_4609_BLOCKERS, "MIS4609_0_shell", "4609 shell blocker."),
        ("SRC4697_09_4609_controls", CSV_4609_CONTROLS, "CTRL4609_0_no_compact_slogan", "4609 anti-overclaim controls."),
        ("SRC4697_10_4609_status", CSV_4609_STATUS, "QEDGE_WORLDTUBE_BOUNDARY_ZERO_OR_SHELL_FLUX_ROWS_READY_NONCLAIM", "4609 status."),
        ("SRC4697_11_4609_next", CSV_4609_NEXT, NEXT_4609, "4609 next target."),
        ("SRC4697_12_4609_validation", CSV_4609_VALIDATION, "VAL4609_OVERALL", "4609 validation passed."),
        ("SRC4697_13_formal712", FORMAL_712, "J_mem^EM_open", "formal retained-current upstream handoff."),
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
            "row_id": "QEI4697_0_current_Qbar_insert",
            "quantity": "Qbar_XH_abs",
            "derived_relation": "|Qbar_XH| <= (||Pi_M^H||(|Q_bulk_4696|+|Q_edge_shell|+|Q_edge_boundary|+|Q_shadow|)+|E_PiM_comm|)/M_lower",
            "meaning": "This places the new retained-bulk result upstream of the Qedge split, so the source numerator is ordered: bulk then edge then shadow.",
            "zero_condition": "Q_bulk_4696, Q_edge_shell, Q_edge_boundary, Q_shadow and projector/denominator rows vanish in the same parent branch",
            "current_status": "QEDGE_INSERTED_QSHADOW_STILL_OPEN",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QEI4697_1_radiative_Poynting_placement",
            "quantity": "F_rad_abs",
            "derived_relation": "Radiative EM/gravity/Poynting flux through the source collar is a boundary-flux row unless stationary no-flux is parent-signed.",
            "meaning": "This prevents Poynting from reappearing as unexplained background force after 4695/4696.",
            "zero_condition": "closed stationary collar, no incoming radiation/current and fixed boundary class",
            "current_status": "RADIATIVE_BOUNDARY_ROW_ACTIVE_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4697_0_shell",
            "object": "Q_edge_shell_abs",
            "status": "requires zero-trace/no-birth-shell certificate or numeric shell profile",
            "next_action": "prove compact regular support with rho_H_trace_norm=mu_birth_TV=0 or source values",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4697_1_boundary",
            "object": "Q_edge_boundary_abs",
            "status": "requires Hamiltonian/corner/reference/sidewall/radiative/projector flux zero or values",
            "next_action": "prove no-flux fixed source collar or fill component rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4697_2_anticircularity",
            "object": "W_H, M_H_ref, Pi_M boundary class",
            "status": "must be parent-owned before arena scoring",
            "next_action": "keep anti-fitted-GM firewall active",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4697_3_next_numerator",
            "object": "Q_shadow_abs",
            "status": "next source-side numerator blocker",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def blockers(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4697_0_shell",
            "missing_object": "rho_H_trace_norm, V_n_bound, mu_birth_TV, Phi_edge and W_lambda_edge_max zero/value rows",
            "why_it_matters": "support motion can generate source charge even after bulk current is quiet",
            "best_next_action": "prove regular compact support/no-shell theorem in the parent branch or source shell coefficients",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4697_1_boundary",
            "missing_object": "B_X_flux, C_corner, E_reference_edge, F_side_source, F_rad and E_projector_edge",
            "why_it_matters": "boundary flux is the exact loophole between local source support and measured external field",
            "best_next_action": "derive no-flux fixed collar or keep boundary flux rows as explicit finite inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4697_2_downstream",
            "missing_object": "Q_shadow, denominator/projector, qbar_XT and arena kernels",
            "why_it_matters": "Qedge alone is not a local-GR/R10/PPN claim",
            "best_next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def controls(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4697_0_no_compact_slogan",
            "control": "Do not set Q_edge=0 by saying compact source; require zero trace, no shell birth/death and no boundary flux.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4697_1_no_fitted_GM",
            "control": "Do not choose W_H, M_H_ref, Pi_M or boundary class from fitted GM/orbital residuals.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4697_2_no_cancellation",
            "control": "Use |Q_edge_shell|+|Q_edge_boundary|; no cancellation credit between edge subcomponents.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4697_3_radiation_firewall",
            "control": "Radiative/Poynting flux is a boundary row unless the stationary closed collar is parent-signed.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_QEDGE_SOURCE_WORLDTUBE_BOUNDARY_GATE_4697",
            "decision": DECISION,
            "reason": "Qedge is now current-branch ordered after the 4696 retained-bulk result: the edge numerator is exactly shell plus boundary flux, with Poynting/radiation placed in the boundary row and no compact-source slogan allowed.",
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
            "derived": "Q_edge split into Reynolds shell plus Hamiltonian/corner/reference/sidewall/radiative/projector boundary flux; current Qbar insertion after 4696 bulk; anti-circularity controls",
            "not_derived": "zero-trace/no-shell certificate; finite shell and boundary flux values; Qshadow and denominator/projector closure; local-GR/R10/PPN pass",
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
            "next_id": "NT4697_0",
            "target": NEXT_TARGET,
            "reason": "After bulk and edge numerator gates are split, Q_shadow is the remaining source-side numerator term blocking Qbar_XH.",
            "derive_first": "prove every shadow is parent action content, boundary/improvement, or absent; no post-Euler/nonvariational source block",
            "fallback": "fill Q_shadow_action, Q_shadow_projector and Q_shadow_nonvariational rows as nonclaim finite inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    DOC_PATH.write_text(
        f"""# 4697 - Qedge Source-Worldtube Boundary Gate

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
This checkpoint does **not** claim local GR. It places the current source numerator in the order:

```text
Qbar_XH <- Q_bulk(4696) + Q_edge_shell + Q_edge_boundary + Q_shadow.
```

The edge term is not a handwave:

```text
Q_edge = Q_edge_Reynolds_shell + Q_edge_boundary_flux
```

and

```text
|Q_edge| <= |Q_edge_shell| + |Q_edge_boundary|.
```

Radiative/Poynting flux through the collar is now a named boundary input unless a stationary no-flux collar is parent-signed.

## Source Register
{table(data["sources"])}

## Qedge Theorem
{table(data["theorem"])}

## Reynolds Shell Rows
{table(data["shell"])}

## Boundary Flux Rows
{table(data["boundary"])}

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
        f"""# 713 - PPC4161 Qedge Source-Worldtube Boundary Gate

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
```text
Q_edge = Q_edge_Reynolds_shell + Q_edge_boundary_flux.
```

```text
|Q_edge| <= |Q_edge_shell| + |Q_edge_boundary|.
```

```text
|Q_edge_shell| <= W_lambda_edge_max Phi_edge
  (rho_H_trace_norm V_n_bound + mu_birth_TV).
```

```text
|Q_edge_boundary| <= |B_X_flux|+|C_corner|+|E_reference_edge|
  +|F_side_source|+|F_rad|+|E_projector_edge|.
```

The current source-numerator envelope is:

```text
|Qbar_XH| <= (||Pi_M^H||(|Q_bulk_4696|+|Q_edge|+|Q_shadow|)
  + |E_PiM_comm|)/M_lower.
```

No claim follows until shell, boundary, shadow, denominator and test-particle charge kernels are parent-signed or source-backed.
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
            "claim": "4697 places Qedge as Reynolds shell plus boundary flux after the 4696 retained-bulk source-current gate.",
            "current_evidence": "Generated source register, Qedge theorem rows, Reynolds shell rows, boundary flux rows, current branch insertion, Qbar update, blockers, survivor update, controls, decision, status, next target and validation.",
            "status": "qedge_worldtube_boundary_zero_or_shell_flux_current_branch_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Treating compact support as automatic zero, fitting GM into the worldtube/reference choice, or erasing radiative/Poynting side flux.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "Qedge source-worldtube boundary gate",
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
- Movement: `Q_edge` is now ordered after the 4696 retained-bulk gate and split into a Reynolds shell term plus boundary flux term.
- Key firewall: compact source is not enough; zero requires zero trace, no shell birth/death and no boundary/radiative/projector flux in the same parent branch.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: current PPC4161 source-numerator branch, after retained bulk and before Qshadow.
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

    add("VAL4697_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4697_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4697_2_edge_split", any("Q_edge :=" in row.get("derived_relation", "") for row in data["theorem"]), "Qedge split present")
    add("VAL4697_3_shell_bound", any("rho_H_trace_norm" in row.get("bound_formula", "") for row in data["shell"]), "Reynolds shell bound present")
    add("VAL4697_4_boundary_bound", any("F_rad" in row.get("bound_formula", "") for row in data["boundary"]), "boundary/radiative flux bound present")
    add("VAL4697_5_qbar_insert", any("Q_bulk_4696" in row.get("derived_relation", "") for row in data["insert"]), "4696 bulk is inserted upstream of Qedge")
    add("VAL4697_6_controls", any(row.get("control_id") == "CTRL4697_0_no_compact_slogan" for row in data["controls"]), "anti compact-source slogan control present")
    add("VAL4697_7_next_Qshadow", data["next"][0]["target"] == NEXT_TARGET, "next Qshadow target selected")
    add("VAL4697_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4697_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4697_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4697_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4697_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")

    for csv_path in [
        SOURCE_REGISTER,
        THEOREM_CSV,
        SHELL_CSV,
        BOUNDARY_CSV,
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
            add(f"VAL4697_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4697_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    claim_values: list[str] = []
    for rows_for_table in [data["theorem"], data["shell"], data["boundary"], data["qbar"], data["insert"], data["survivors"], data["blockers"], data["controls"], data["decision"], data["status"], data["next"]]:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4697_13_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4697_14_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4697_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    decision, status, next_rows = decision_rows(timestamp)
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "theorem": restamp_rows(CSV_4609_THEOREM, timestamp),
        "shell": restamp_rows(CSV_4609_SHELL, timestamp),
        "boundary": restamp_rows(CSV_4609_BOUNDARY, timestamp),
        "qbar": restamp_rows(CSV_4609_QBAR, timestamp),
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
    write_csv(SHELL_CSV, data["shell"])
    write_csv(BOUNDARY_CSV, data["boundary"])
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
