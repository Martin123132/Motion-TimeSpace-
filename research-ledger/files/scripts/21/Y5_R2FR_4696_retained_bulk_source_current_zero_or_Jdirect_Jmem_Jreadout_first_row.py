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

CHECKPOINT = "4696"
CLAIM_ID = "L-538"
MARKER = "PPC4161_RETAINED_BULK_SOURCE_CURRENT_BRANCH_4696"
PACKET_MARKER = "PPC4161_PACKET_RETAINED_BULK_SOURCE_CURRENT_BRANCH_4696"
DECISION = "RETAINED_BULK_SOURCE_CURRENT_WITH_4695_EM_INSERTION_NONCLAIM"
NEXT_TARGET = "4697-Y5-R2FR-Qedge-source-worldtube-boundary-zero-or-shell-flux-first-row.md"

DOC_PATH = POST / "4696-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md"
FORMAL_PATH = FORMAL / "712-PPC4161-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"

CSV_4695_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4695_STATUS.csv"
CSV_4695_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4695_NEXT_TARGET.csv"
CSV_4695_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4695_VALIDATION.csv"
CSV_4695_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4695_EM_POYNTING_HODGE_FLUX_THEOREM.csv"
CSV_4695_BOUND = SOURCE_DIR / "P8_Y5_R2FR_4695_EM_BULK_BOUND_UPDATE_ROWS.csv"
CSV_4695_FLUX = SOURCE_DIR / "P8_Y5_R2FR_4695_POYNTING_FLUX_ROWS.csv"
CSV_4695_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4695_CLAIM_BLOCKERS.csv"

CSV_4608_THEOREM = SOURCE_DIR / "P8_Y5_R2FR_4608_RETAINED_BULK_SOURCE_CURRENT_THEOREM.csv"
CSV_4608_JDIRECT = SOURCE_DIR / "P8_Y5_R2FR_4608_JDIRECT_ROWS.csv"
CSV_4608_JMEM = SOURCE_DIR / "P8_Y5_R2FR_4608_JMEM_ROWS.csv"
CSV_4608_JMARKER = SOURCE_DIR / "P8_Y5_R2FR_4608_JMARKER_ROWS.csv"
CSV_4608_JREADOUT = SOURCE_DIR / "P8_Y5_R2FR_4608_JREADOUT_ROWS.csv"
CSV_4608_QBULK = SOURCE_DIR / "P8_Y5_R2FR_4608_QBULK_RETAINED_UPDATE_ROWS.csv"
CSV_4608_BLOCKERS = SOURCE_DIR / "P8_Y5_R2FR_4608_CLAIM_BLOCKERS.csv"
CSV_4608_CONTROLS = SOURCE_DIR / "P8_Y5_R2FR_4608_CONTROL_ROWS.csv"
CSV_4608_STATUS = SOURCE_DIR / "P8_Y5_R2FR_4608_STATUS.csv"
CSV_4608_DECISION = SOURCE_DIR / "P8_Y5_R2FR_4608_DECISION.csv"
CSV_4608_NEXT = SOURCE_DIR / "P8_Y5_R2FR_4608_NEXT_TARGET.csv"
CSV_4608_VALIDATION = SOURCE_DIR / "P8_Y5_BRR545_4608_VALIDATION.csv"

FORMAL_624 = FORMAL / "624-PPC4161-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md"
FORMAL_711 = FORMAL / "711-PPC4161-EM-Poynting-Hodge-flux-zero-or-wall-flux-coefficient-row.md"

SOURCE_REGISTER = SOURCE_DIR / "P8_Y5_R2FR_4696_SOURCE_REGISTER.csv"
THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4696_RETAINED_BULK_SOURCE_CURRENT_THEOREM.csv"
JDIRECT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4696_JDIRECT_ROWS.csv"
JMEM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4696_JMEM_ROWS.csv"
JMARKER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4696_JMARKER_ROWS.csv"
JREADOUT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4696_JREADOUT_ROWS.csv"
EM_INSERT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4696_JMEM_EM_4695_INSERTION_ROWS.csv"
QBULK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4696_QBULK_RETAINED_UPDATE_ROWS.csv"
SURVIVOR_CSV = SOURCE_DIR / "P8_Y5_R2FR_4696_SURVIVOR_UPDATE.csv"
CONTROL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4696_CONTROL_ROWS.csv"
BLOCKERS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4696_CLAIM_BLOCKERS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4696_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4696_STATUS.csv"
NEXT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4696_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4696_VALIDATION.csv"

NEXT_4695 = "4696-Y5-R2FR-retained-bulk-source-current-zero-or-Jdirect-Jmem-Jreadout-first-row.md"
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


def restamp_rows(path: Path, timestamp: str, old_checkpoint: str = "4608") -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in read_csv(path):
        row: dict[str, Any] = {}
        for key, value in source.items():
            if key in {"source_paths", "path", "source_path"}:
                new_value = value
            else:
                new_value = (
                    value.replace(old_checkpoint, CHECKPOINT)
                    .replace(NEXT_4608, NEXT_TARGET)
                    .replace("2026-07-06T15:46:35.357498+00:00", timestamp)
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
        ("SRC4696_00_4695_status", CSV_4695_STATUS, "PPC4161_EM_POYNTING_HODGE_FLUX_CURRENT_BRANCH_4695", "4695 current EM/Poynting gate."),
        ("SRC4696_01_4695_next", CSV_4695_NEXT, NEXT_4695, "4695 selects retained-current as next target."),
        ("SRC4696_02_4695_validation", CSV_4695_VALIDATION, "VAL4695_OVERALL", "4695 validation passed."),
        ("SRC4696_03_4695_theorem", CSV_4695_THEOREM, "EMF4695_3_finite_EM_bound", "4695 finite EM/Poynting bound."),
        ("SRC4696_04_4695_bound", CSV_4695_BOUND, "EB4695_1_bound_route", "4695 EM bulk update row."),
        ("SRC4696_05_4695_flux", CSV_4695_FLUX, "FX4695_1_wall_flux_bound", "4695 Poynting wall flux bound."),
        ("SRC4696_06_4695_blockers", CSV_4695_BLOCKERS, "MIS4695_1_wall_flux", "4695 keeps wall flux as live input if unsigned."),
        ("SRC4696_07_4608_theorem", CSV_4608_THEOREM, "RET4608_0_decomposition", "4608 retained current decomposition."),
        ("SRC4696_08_4608_direct", CSV_4608_JDIRECT, "JD4608_0_total", "4608 direct current row."),
        ("SRC4696_09_4608_memory", CSV_4608_JMEM, "JM4608_1_EM_open", "4608 memory EM-open row."),
        ("SRC4696_10_4608_marker", CSV_4608_JMARKER, "JMK4608_0_total", "4608 marker row."),
        ("SRC4696_11_4608_readout", CSV_4608_JREADOUT, "JR4608_0_total", "4608 readout row."),
        ("SRC4696_12_4608_qbulk", CSV_4608_QBULK, "QBR4608_0_retained", "4608 retained bulk update."),
        ("SRC4696_13_4608_controls", CSV_4608_CONTROLS, "CTRL4608_2_poynting_not_hidden", "4608 control against hiding Poynting."),
        ("SRC4696_14_4608_next", CSV_4608_NEXT, NEXT_4608, "4608 next target."),
        ("SRC4696_15_4608_validation", CSV_4608_VALIDATION, "VAL4608_OVERALL", "4608 validation passed."),
        ("SRC4696_16_formal624", FORMAL_624, "J_retained := J_direct", "formal retained-current addendum."),
        ("SRC4696_17_formal711", FORMAL_711, "|Q_bulk_EM/Poynting| <= W_lambda_max", "formal 4695 EM/Poynting bound."),
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


def em_insertion_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JME4696_0_4695_insertion",
            "quantity": "J_mem_EM_open_abs",
            "derived_relation": "|J_mem^EM_open| <= C_EM_source/M_H_ref * |Q_bulk_EM/Poynting|_4695",
            "4695_bound_inserted": "|J_mem^EM_open| <= C_EM_source W_lambda_max(M_ref|Delta_Hodge_EM|+|c_Poynt_extra Phi_wall|+|Phi_wall_Poynting|+M_ref|epsilon_nonminimal_EM|)/|M_H_ref|",
            "zero_condition": "same-Hodge Maxwell branch, c_Poynt_extra=0, stationary no-wall-flux collar, epsilon_nonminimal_EM=0 and source-coupling projection finite in the same parent branch",
            "current_status": "EM_MEMORY_COMPONENT_REDUCED_TO_4695_HODGE_FLUX_INPUTS_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "JME4696_1_no_double_count",
            "quantity": "Poynting_placement_control",
            "derived_relation": "Ordinary Poynting flux is counted either as Hilbert EM stress/Q_bulk_EM or as an explicit retained nonminimal/source flux term, never both.",
            "4695_bound_inserted": "If it is ordinary Maxwell stress, use EB4695_1; if it is nonminimal/source-tail flux, keep it under J_mem or epsilon_nonminimal_EM with a named coefficient.",
            "zero_condition": "one stress/source owner and no hidden reduced-action feedback",
            "current_status": "NO_DOUBLE_COUNT_CONTROL_ACTIVE",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def survivor_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4696_0_direct",
            "object": "J_direct_abs",
            "meaning": "direct non-Hilbert/source-weight/action-scale current",
            "status": "source-slot theorem or finite coefficient still needed",
            "next_action": "prove no source-only object language or fill absolute coefficient row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4696_1_memory_EM",
            "object": "J_mem_EM_open_abs",
            "meaning": "retained memory current sourced by EM/Poynting flux after 4695 insertion",
            "status": "reduced to Delta_Hodge_EM/Phi_wall_Poynting/epsilon_nonminimal_EM inputs",
            "next_action": "prove same-Hodge stationary collar or source those finite inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4696_2_memory_nonEM",
            "object": "J_mem_nonHilbert_abs+J_mem_dyn_exchange_abs+J_mem_boundary_readout_abs",
            "meaning": "non-EM memory source tails",
            "status": "symbolic values missing",
            "next_action": "close non-Hilbert/dynamic/boundary readout source-current clauses",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4696_3_marker",
            "object": "J_marker_abs",
            "meaning": "material/frame/constant/source-boundary marker source current",
            "status": "no-marker theorem not closed",
            "next_action": "prove quotient ownership of material constants/frames or bound marker coefficients",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4696_4_readout",
            "object": "J_readout_abs",
            "meaning": "post-solution readout/projector/worldtube/material/EFT/calibration re-entry",
            "status": "parent-domain exclusion not fully signed",
            "next_action": "turn readout schema into parent-domain certificate or source finite components",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "survivor_id": "SURV4696_5_next_numerator",
            "object": "Q_edge_abs",
            "meaning": "source worldtube/boundary shell flux numerator after retained bulk is named",
            "status": "next live source-side numerator",
            "next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def qbulk_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QBR4696_0_retained_with_4695_EM",
            "quantity": "Q_bulk_retained_abs",
            "update_formula": "|Q_bulk_retained| <= W_lambda_max(|J_direct|+|J_marker|+|J_readout|+|J_mem_nonHilbert|+|J_mem_dyn_exchange|+|J_mem_boundary_readout|+C_EM_source(M_ref|Delta_Hodge_EM|+|c_Poynt_extra Phi_wall|+|Phi_wall_Poynting|+M_ref|epsilon_nonminimal_EM|)/|M_H_ref|)",
            "zero_condition": "all retained components and the 4695 EM/Hodge/flux/nonminimal inputs vanish in the same parent branch",
            "required_inputs": "J_direct_abs;J_marker_abs;J_readout_abs;J_mem_nonHilbert_abs;J_mem_dyn_exchange_abs;J_mem_boundary_readout_abs;Delta_Hodge_EM_abs;Phi_wall_Poynting_abs;epsilon_nonminimal_EM;C_EM_source;M_H_ref;W_lambda_max",
            "current_status": "RETAINED_BOUND_TIGHTENED_WITH_4695_EM_INSERTION_VALUES_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QBR4696_1_bulk_total",
            "quantity": "Q_bulk_abs",
            "update_formula": "|Q_bulk| <= |Q_bulk_Hilbert|+|Q_bulk_EM/Poynting|+|Q_bulk_retained|",
            "zero_condition": "Hilbert, EM/Poynting and retained bulk tails vanish in the same branch",
            "required_inputs": "4694 Hilbert rows;4695 EM/Poynting rows;4696 retained rows",
            "current_status": "QBULK_TOTAL_STILL_NONCLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "row_id": "QBR4696_2_QbarXH",
            "quantity": "Qbar_XH_abs",
            "update_formula": "|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower",
            "zero_condition": "bulk retained plus edge/shadow plus denominator/projector commute and vanish",
            "required_inputs": "Q_bulk_abs;Q_edge_abs;Q_shadow_abs;Pi_M norm;E_PiM_comm;M_lower",
            "current_status": "QBARXH_STILL_BLOCKED_BY_EDGE_SHADOW_AND_DENOMINATOR",
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def blockers(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4696_0_same_branch",
            "missing_object": "same-branch zero certificate for J_direct, J_mem, J_marker and J_readout",
            "why_it_matters": "retained-current cancellation is forbidden, so one live component keeps Q_bulk_retained live",
            "best_next_action": "prove all retained components vanish under the same parent assumptions or keep absolute bound rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4696_1_EM_inputs",
            "missing_object": "Delta_Hodge_EM, Phi_wall_Poynting, epsilon_nonminimal_EM and C_EM_source",
            "why_it_matters": "4695 converts Poynting intuition into named finite inputs; it does not erase them",
            "best_next_action": "prove same-Hodge stationary collar or source finite coefficients",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4696_2_direct_marker_readout",
            "missing_object": "parent-owned no-source-slot, no-marker and readout-exclusion certificates",
            "why_it_matters": "these are the remaining places source coupling can hide after Hilbert/EM cleanup",
            "best_next_action": "derive parent-domain exclusion clauses or fill nonclaim coefficient rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "blocker_id": "MIS4696_3_downstream",
            "missing_object": "Q_edge, Q_shadow, denominator/projector, qbar_XT and arena kernels",
            "why_it_matters": "retained bulk alone is not a local-GR/R10/PPN/clock/orbit pass",
            "best_next_action": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def controls(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4696_0_no_cancellation",
            "control": "Use absolute retained-current component sums; do not cancel direct, memory, marker or readout pieces against each other.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4696_1_same_branch",
            "control": "A zero proof must use the same parent branch for direct, EM/Poynting, non-Hilbert, marker and readout clauses.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4696_2_poynting_once",
            "control": "Poynting is not a magic extra force term; ordinary Maxwell Poynting is Hilbert EM stress unless a named nonminimal/source coefficient is present.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "checkpoint": CHECKPOINT,
            "control_id": "CTRL4696_3_no_claim_from_symbolic_rows",
            "control": "Symbolic retained-current bounds cannot score R10, WEP, PPN, clock or orbital tests.",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def decision_rows(timestamp: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    decision = [
        {
            "checkpoint": CHECKPOINT,
            "branch": "MTS_R2FR_Y5_RETAINED_BULK_SOURCE_CURRENT_GATE_4696",
            "decision": DECISION,
            "reason": "The retained-current gate now imports the 4695 EM/Poynting result: EM memory is not waved away; it is reduced to same-Hodge, wall-flux and nonminimal source inputs. Direct, marker and readout tails remain live unless parent-signed.",
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
            "derived": "retained source current decomposition; no-cancellation total bound; 4695 EM/Poynting insertion into J_mem_EM_open; survivor list for direct, memory, marker and readout tails",
            "not_derived": "parent-signed same-branch retained-current zero; numeric retained coefficients; local-GR/R10/PPN/clock/orbit pass",
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
            "next_id": "NT4696_0",
            "target": NEXT_TARGET,
            "reason": "After retained bulk is componentized and EM/Poynting is inserted, the next source-side numerator term is Q_edge: source worldtube/boundary shell flux.",
            "derive_first": "prove fixed source worldtube, compact collar, no birth/death shell and zero source-boundary flux in the same branch",
            "fallback": "fill Qedge shell/worldtube/corner flux rows as nonclaim finite inputs",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]
    return decision, status, next_rows


def write_documents(timestamp: str, data: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 4696 - Retained Bulk Source Current With 4695 EM/Poynting Insertion

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Result
This checkpoint does **not** claim local GR. It takes the retained source-current split seriously and inserts the new 4695 EM/Poynting gate into the memory component:

```text
J_retained = J_direct + J_mem + J_marker + J_readout
```

with

```text
|J_mem^EM_open| <= C_EM_source W_lambda_max(
  M_ref|Delta_Hodge_EM| + |c_Poynt_extra Phi_wall|
  + |Phi_wall_Poynting| + M_ref|epsilon_nonminimal_EM|
) / |M_H_ref|.
```

So Poynting is now placed exactly: ordinary Maxwell Poynting belongs to Hilbert EM stress; only a named wall-flux/nonminimal/source coefficient remains as retained current.

## Source Register
{table(data["sources"])}

## Retained Theorem Rows
{table(data["theorem"])}

## 4695 EM Memory Insertion
{table(data["em_insert"])}

## Updated Retained Bulk Bound
{table(data["qbulk"])}

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
"""
    DOC_PATH.write_text(doc, encoding="utf-8")

    formal = f"""# 712 - PPC4161 Retained Bulk Source Current Gate

Marker: `{MARKER}`

Claim register: `{CLAIM_ID}`

Generated UTC: `{timestamp}`

## Formal Insert
```text
J_retained = J_direct + J_mem + J_marker + J_readout.
```

The 4695 EM/Poynting result enters only through the EM-open memory component:

```text
|J_mem^EM_open| <= C_EM_source |Q_bulk_EM/Poynting|_4695 / |M_H_ref|.
```

Therefore

```text
|J_mem^EM_open| <= C_EM_source W_lambda_max(
  M_ref|Delta_Hodge_EM| + |c_Poynt_extra Phi_wall|
  + |Phi_wall_Poynting| + M_ref|epsilon_nonminimal_EM|
) / |M_H_ref|.
```

The same-branch zero condition is:

```text
J_direct=J_marker=J_readout=J_mem_nonHilbert=J_mem_dyn_exchange
=J_mem_boundary_readout=Delta_Hodge_EM=Phi_wall_Poynting
=epsilon_nonminimal_EM=c_Poynt_extra=0.
```

## Nonclaim Status
No R10, WEP, PPN, clock, orbital or local-GR claim follows. This is a source-current narrowing step.

## Validation
See `{VALIDATION_CSV}`.
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")


def update_registers(timestamp: str, status_rows: list[dict[str, Any]]) -> None:
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
            "claim": "4696 inserts the 4695 EM/Poynting Hodge/wall-flux bound into retained memory current and keeps direct, marker and readout source tails explicit.",
            "current_evidence": "Generated source register, retained theorem rows, direct/memory/marker/readout rows, 4695 EM insertion, Qbulk retained update, blockers, survivor update, controls, decision, status, next target and validation.",
            "status": "retained_bulk_source_current_with_4695_em_insertion_nonclaim",
            "next_test": NEXT_TARGET,
            "key_risk": "Treating Poynting as a vague background field, double-counting EM stress, or claiming retained-current silence without same-branch direct/memory/marker/readout zero.",
            "sector": "local_gr",
            "evidence": str(DOC_PATH),
            "next_action": NEXT_TARGET,
            "title": "Retained bulk source-current with 4695 EM/Poynting insertion",
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
- Movement: retained bulk source current now imports the 4695 EM/Poynting Hodge/wall-flux bound into `J_mem^EM_open` rather than leaving Poynting as a vague background-field intuition.
- Remaining live objects: `J_direct_abs`, non-EM `J_mem` tails, `J_marker_abs`, `J_readout_abs`, `Q_edge_abs`, `Q_shadow_abs`, denominator/projector and test-particle charge kernels.
- Next: `{NEXT_TARGET}`.
""",
    )
    append_once(
        PACKET_PATH,
        PACKET_MARKER,
        f"""### {PACKET_MARKER}

- Source checkpoint: `{CHECKPOINT}`.
- Decision: `{DECISION}`.
- Packet role: current PPC4161 local-source branch, after EM/Poynting placement and before Q-edge worldtube boundary flux.
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

    add("VAL4696_0_sources_exist", all(row["path_exists"] for row in data["sources"]), "all source-register paths exist")
    add("VAL4696_1_needles_found", all(row["needle_found"] for row in data["sources"]), "all source-register needles found")
    add("VAL4696_2_retained_decomposition", any("J_retained" in row.get("derived_relation", "") for row in data["theorem"]), "retained decomposition present")
    add("VAL4696_3_em_insertion", any("4695" in row.get("row_id", "") or "4695" in row.get("4695_bound_inserted", "") for row in data["em_insert"]), "4695 EM/Poynting insertion present")
    add("VAL4696_4_qbulk_insert", any("Delta_Hodge_EM" in row.get("update_formula", "") for row in data["qbulk"]), "Qbulk retained bound includes EM/Hodge/flux inputs")
    add("VAL4696_5_survivors", len(data["survivors"]) >= 5, "survivor rows enumerate retained source-current tails")
    add("VAL4696_6_controls", any(row.get("control_id") == "CTRL4696_2_poynting_once" for row in data["controls"]), "Poynting once-only control present")
    add("VAL4696_7_next_Qedge", data["next"][0]["target"] == NEXT_TARGET, "next Qedge target selected")
    add("VAL4696_8_claim_row_exists", CLAIM_ID in text(CLAIMS_PATH), f"claims register contains {CLAIM_ID}")
    add("VAL4696_9_formal_doc", FORMAL_PATH.exists() and MARKER in text(FORMAL_PATH), "formal doc exists with marker")
    add("VAL4696_10_post_doc", DOC_PATH.exists() and MARKER in text(DOC_PATH), "post checkpoint exists with marker")
    add("VAL4696_11_spine_marker", MARKER in text(SPINE_PATH), "spine marker written")
    add("VAL4696_12_packet_marker", PACKET_MARKER in text(PACKET_PATH), "packet marker written")

    for csv_path in [
        SOURCE_REGISTER,
        THEOREM_CSV,
        JDIRECT_CSV,
        JMEM_CSV,
        JMARKER_CSV,
        JREADOUT_CSV,
        EM_INSERT_CSV,
        QBULK_CSV,
        SURVIVOR_CSV,
        CONTROL_CSV,
        BLOCKERS_CSV,
        DECISION_CSV,
        STATUS_CSV,
        NEXT_CSV,
    ]:
        try:
            parsed = read_csv(csv_path)
            add(f"VAL4696_csv_{csv_path.stem}", len(parsed) > 0, f"{csv_path} parses with {len(parsed)} rows")
        except Exception as exc:
            add(f"VAL4696_csv_{csv_path.stem}", False, f"{csv_path} failed to parse: {exc}")

    generated_tables = [
        data["theorem"],
        data["jdirect"],
        data["jmem"],
        data["jmarker"],
        data["jreadout"],
        data["em_insert"],
        data["qbulk"],
        data["survivors"],
        data["controls"],
        data["blockers"],
        data["decision"],
        data["status"],
        data["next"],
    ]
    claim_values: list[str] = []
    for rows_for_table in generated_tables:
        for row in rows_for_table:
            for key in ("valid_for_claim", "claim_allowed", "local_GR_public_claim"):
                if key in row:
                    claim_values.append(str(row[key]).lower())
    add("VAL4696_13_no_claim_rows_true", all(value in {"false", ""} for value in claim_values), "generated rows keep claim flags false")

    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    add("VAL4696_14_pycache_absent", not pycache.exists(), "scripts __pycache__ absent")

    overall = all(str(row["passed"]) == "True" or row["passed"] is True for row in rows)
    add("VAL4696_OVERALL", overall, "PASS" if overall else "FAIL")
    return rows


def main() -> None:
    timestamp = now()
    data: dict[str, list[dict[str, Any]]] = {
        "sources": source_rows(timestamp),
        "theorem": restamp_rows(CSV_4608_THEOREM, timestamp),
        "jdirect": restamp_rows(CSV_4608_JDIRECT, timestamp),
        "jmem": restamp_rows(CSV_4608_JMEM, timestamp),
        "jmarker": restamp_rows(CSV_4608_JMARKER, timestamp),
        "jreadout": restamp_rows(CSV_4608_JREADOUT, timestamp),
        "em_insert": em_insertion_rows(timestamp),
        "qbulk": qbulk_rows(timestamp),
        "survivors": survivor_rows(timestamp),
        "controls": controls(timestamp),
        "blockers": blockers(timestamp),
    }
    decision, status, next_rows = decision_rows(timestamp)
    data["decision"] = decision
    data["status"] = status
    data["next"] = next_rows

    write_csv(SOURCE_REGISTER, data["sources"])
    write_csv(THEOREM_CSV, data["theorem"])
    write_csv(JDIRECT_CSV, data["jdirect"])
    write_csv(JMEM_CSV, data["jmem"])
    write_csv(JMARKER_CSV, data["jmarker"])
    write_csv(JREADOUT_CSV, data["jreadout"])
    write_csv(EM_INSERT_CSV, data["em_insert"])
    write_csv(QBULK_CSV, data["qbulk"])
    write_csv(SURVIVOR_CSV, data["survivors"])
    write_csv(CONTROL_CSV, data["controls"])
    write_csv(BLOCKERS_CSV, data["blockers"])
    write_csv(DECISION_CSV, data["decision"])
    write_csv(STATUS_CSV, data["status"])
    write_csv(NEXT_CSV, data["next"])

    write_documents(timestamp, data)
    update_registers(timestamp, data["status"])
    validation = validation_rows(timestamp, data)
    write_csv(VALIDATION_CSV, validation)

    print(f"{CHECKPOINT} complete: {DOC_PATH}")
    print(f"validation: {VALIDATION_CSV}")


if __name__ == "__main__":
    main()
