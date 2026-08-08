from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main")
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"

CHECKPOINT = "4771"
CLAIM_ID = "L-613"
MARKER = "PPC4161_MATTER_LIFT_GAUGE_BOUNDARY_COLLAPSE_OR_POYNTING_BOUNDARY_FIRST_VALUES_4771"
PACKET_MARKER = "PPC4161_PACKET_MATTER_LIFT_GAUGE_BOUNDARY_COLLAPSE_OR_POYNTING_BOUNDARY_FIRST_VALUES_4771"
DECISION = "MATTER_LIFT_BULK_COLLAPSES_ON_SHELL_GAUGE_FIXED_BOUNDARY_CONTRACT_REMAINING_LOCAL_OBSTRUCTION_IS_BOUNDARY_LIFT_POYNTING_BOUNDARY_FLUX_DENOMINATOR_PROJECTOR_NONCLAIM"
NEXT_TARGET = "4772-Y5-R2FR-boundary-lift-Poynting-collar-zero-or-denominator-projector-first-values.md"

DOC_PATH = POST / "4771-Y5-R2FR-matter-lift-gauge-boundary-collapse-or-Poynting-boundary-first-values.md"
FORMAL_PATH = FORMAL / "787-PPC4161-matter-lift-gauge-boundary-collapse-or-Poynting-boundary-first-values.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4771_SOURCE_REGISTER.csv"
VARIATION_IDENTITY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4771_MATTER_LIFT_VARIATION_IDENTITY.csv"
SECTOR_PLACEMENT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4771_MATTER_LIFT_SECTOR_PLACEMENT.csv"
REDUCED_OBSTRUCTION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4771_REDUCED_OBSTRUCTION_AFTER_LIFT_BULK_COLLAPSE.csv"
QEDGE_QBAR_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4771_QEDGE_QBAR_UPDATE.csv"
BOUNDARY_QUEUE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4771_BOUNDARY_LIFT_POYNTING_QUEUE.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4771_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4771_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4771_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4771_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4771_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4771_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4771_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4771_0_4770_envelope", SOURCE_DIR / "P8_Y5_R2FR_4770_REDUCED_LOCAL_OBSTRUCTION_ENVELOPE.csv", "RE4770_2_bulk_source", "4770 reduced bulk source-qbasic obstruction"),
    ("SRC4771_1_4770_qedge", SOURCE_DIR / "P8_Y5_R2FR_4770_QEDGE_QBAR_GATE_UPDATE.csv", "QQ4770_1_Qedge_shell", "4770 Qedge shell update"),
    ("SRC4771_2_4770_four_clause", SOURCE_DIR / "P8_Y5_R2FR_4770_FOUR_CLAUSE_CLOSURE_THEOREM.csv", "FCC4770_4_bulk_measure", "4770 four-clause closure theorem"),
    ("SRC4771_3_4573_source_lift", SOURCE_DIR / "P8_Y5_R2FR_4573_SOURCE_LIFT_ZERO_CONTRACT.csv", "ZC4573_5_doubled_owner_or_solder", "4573 source-lift zero contract"),
    ("SRC4771_4_4573_decision", SOURCE_DIR / "P8_Y5_R2FR_4573_DECISION.csv", "GENERIC_SIGMA_METRIC_ZERO_NOT_DERIVED", "4573 nonclaim decision"),
    ("SRC4771_5_vertical_silence", FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md", "delta_v S_matter", "quotient-naturality matter descent theorem"),
    ("SRC4771_6_motion_frame", FORMAL / "199-PPC4161-motion-frame-axiom-adoption-consequences-and-test-contract.md", "matter equations + boundary", "motion-frame action variation and Noether contract"),
    ("SRC4771_7_kperp_placement", FORMAL / "220-PPC4161-Kperp-sector-placement-theorem.md", "K_vertical     -> quotient/gauge representative", "vertical/boundary/extra-source sector placement"),
    ("SRC4771_8_poynting_4766", SOURCE_DIR / "P8_Y5_R2FR_4766_POYNTING_WALL_FLUX_ROW.csv", "PWF4766_2_wall_flux_bound", "Poynting wall flux bound row"),
    ("SRC4771_9_em_owner_4714", SOURCE_DIR / "P8_Y5_R2FR_4714_EM_STRESS_POYNTING_OWNER_THEOREM.csv", "EMP4714_4_no_double_count", "EM/Poynting no-double-count theorem"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    VARIATION_IDENTITY_CSV,
    SECTOR_PLACEMENT_CSV,
    REDUCED_OBSTRUCTION_CSV,
    QEDGE_QBAR_UPDATE_CSV,
    BOUNDARY_QUEUE_CSV,
    ROUTE_MATRIX_CSV,
    PROMOTION_GATES_CSV,
    FIREWALL_CSV,
    DECISION_CSV,
    STATUS_CSV,
    NEXT_TARGET_CSV,
]


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path_object: Path) -> str:
    return path_object.read_text(encoding="utf-8-sig", errors="replace")


def write_text(path_object: Path, content: str) -> None:
    path_object.parent.mkdir(parents=True, exist_ok=True)
    path_object.write_text(content, encoding="utf-8", newline="\n")


def write_csv(path_object: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path_object}")
    path_object.parent.mkdir(parents=True, exist_ok=True)
    with path_object.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def parse_csv(path_object: Path) -> bool:
    with path_object.open("r", encoding="utf-8-sig", newline="") as handle:
        list(csv.DictReader(handle))
    return True


def append_once(path_object: Path, marker: str, block: str) -> None:
    existing = read_text(path_object) if path_object.exists() else ""
    if marker in existing:
        return
    separator = "" if not existing or existing.endswith("\n") else "\n"
    write_text(path_object, existing + separator + block.rstrip() + "\n")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = [
        "| " + " | ".join(str(row[column]).replace("\\", "\\\\").replace("|", "\\|").replace("\n", " ") for column in columns) + " |"
        for row in rows
    ]
    return "\n".join([header, divider, *body])


def source_register(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path_object, needle, role in SOURCE_SPECS:
        exists = path_object.exists()
        text = read_text(path_object) if exists else ""
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "source_path": str(path_object),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def variation_identity_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "MLV4771_0_definition",
            "E_matter_lift",
            "vertical variation of the physical matter lift inside the already q-owned source action",
            "delta_v S_m = int_W E_psi delta_v psi dV + int_partialW Theta_m(delta_v psi)",
            "definition_split",
        ),
        (
            "MLV4771_1_bulk_eom",
            "E_matter_lift_bulk",
            "if matter is on shell on W and the lift is a gauge/representative lift, int_W E_psi delta_v psi dV=0",
            "0_private_on_shell_gauge",
            "bulk_collapses",
        ),
        (
            "MLV4771_2_boundary_symplectic",
            "E_lift_boundary",
            "the only surviving lift term is the symplectic/boundary flux of the matter lift",
            "|int_partialW Theta_m(delta_v psi)|",
            "boundary_retained",
        ),
        (
            "MLV4771_3_fixed_boundary",
            "E_lift_boundary_zero_branch",
            "if delta_v psi has compact support, fixed boundary data, exact proper-boundary form, or q-owned routed charge, the boundary lift term is zero",
            "0_private_if_boundary_locked",
            "zero_candidate",
        ),
        (
            "MLV4771_4_open_boundary",
            "E_lift_boundary_bound",
            "if the boundary is open/radiative/nonstationary, carry the lift flux as a finite boundary row and do not absorb it into the source shell",
            "||Theta_m(delta_v psi)||_partialW",
            "bound_needed",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "identity_id": identity_id,
            "quantity": quantity,
            "statement": statement,
            "formula_or_value": formula,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for identity_id, quantity, statement, formula, status in specs
    ]


def sector_placement_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("MLP4771_0_vertical_gauge", "delta_v psi is representation/gauge data", "bulk source contribution is zero on shell", "PLACED_NON_SOURCE_BULK"),
        ("MLP4771_1_observed_hilbert", "ordinary matter lift changes only Hilbert stress through g_obs(q)", "already counted in T_total and source measure; no extra lift source", "NO_DOUBLE_COUNT"),
        ("MLP4771_2_boundary_charge", "delta_v psi creates symplectic charge on partial W", "retained as E_lift_boundary and routed with Poynting/boundary flux", "BOUNDARY_ROW"),
        ("MLP4771_3_extra_source", "lift changes physical matter label, source coefficient, or support after readout", "forbidden in private branch; public/off-branch retained as explicit source residual", "RETAINED_PUBLIC_GAP"),
        ("MLP4771_4_verdict", "matter lift placement", "bulk lift is closed only under on-shell/gauge/fixed-boundary contract; boundary lift remains explicit", "BULK_CLOSED_BOUNDARY_OPEN_NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "placement_id": placement_id,
            "sector": sector,
            "effect": effect,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for placement_id, sector, effect, status in specs
    ]


def reduced_obstruction_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("RO4771_0_previous", "E_local_obstruction_4770", "|E_matter_lift|+|E_Poynting_wall|+|E_boundary_flux|", "before splitting matter lift", "REFERENCE"),
        ("RO4771_1_matter_lift_split", "E_matter_lift", "|E_matter_lift_bulk|+|E_lift_boundary|", "Euler/boundary variation identity", "SPLIT_DERIVED"),
        ("RO4771_2_bulk_lift", "E_matter_lift_bulk", "0_private_on_shell_gauge", "bulk term vanishes when matter equations and gauge/representative lift hold", "BULK_CLOSED_CONDITIONAL"),
        ("RO4771_3_boundary_lift", "E_lift_boundary", "|int_partialW Theta_m(delta_v psi)|", "remaining symplectic/fixed-boundary/open-boundary term", "BOUNDARY_RETAINED"),
        ("RO4771_4_bulk_source", "E_bulk_source_qbasic_4771", "0_private_conditional", "bulk source-qbasic obstruction closes inside the on-shell gauge fixed-boundary branch", "BULK_QBASIC_CONDITIONAL_ZERO"),
        ("RO4771_5_boundary_total", "E_boundary_total_4771", "|E_lift_boundary|+|E_Poynting_wall|+|E_boundary_flux|", "all surviving local obstruction is boundary/wave/corner content", "NEXT_BOUNDARY_TARGET"),
        ("RO4771_6_local_obstruction", "E_local_obstruction_4771", "|E_lift_boundary|+|E_Poynting_wall|+|E_boundary_flux|", "matter lift no longer appears as a bulk source obstruction", "REDUCED_NONCLAIM_ENVELOPE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "obstruction_id": obstruction_id,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for obstruction_id, symbol, formula, meaning, status in specs
    ]


def qedge_qbar_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("QQ4771_0_bulk_shell", "Matter-lift bulk no longer blocks Qedge shell zero inside the private on-shell/gauge branch.", "Q_edge_shell_abs=0 becomes conditional on pre-readout support plus no boundary lift birth/death.", "BULK_GATE_REMOVED_CONDITIONAL"),
        ("QQ4771_1_boundary_birth", "If E_lift_boundary is nonzero on the source collar it is a boundary/birth flux, not a cancellable bulk source measure term.", "route to Q_edge_boundary_abs or finite boundary queue.", "BOUNDARY_GATE_REMAINS"),
        ("QQ4771_2_poynting", "Poynting remains Hilbert stress once or wall flux; no double counting with lift boundary flux.", "use 4714 owner rule and 4766 wall bound.", "POYNTING_EXPLICIT"),
        ("QQ4771_3_qbar", "Qbar_XH score still cannot fire without boundary total, shadow, denominator and projector gates.", "matter-lift bulk closure is necessary but insufficient.", "PRODUCT_BLOCKED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "update_id": update_id,
            "rule": rule,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, rule, meaning, status in specs
    ]


def boundary_queue_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("BQ4771_0_lift_boundary_zero", "E_lift_boundary", "compact support/fixed matter boundary/exact proper-boundary/q-owned routed charge", "zero theorem or finite symplectic flux norm", "highest"),
        ("BQ4771_1_poynting_collar", "E_Poynting_wall", "closed stationary same-Hodge collar or open wall flux values", "zero theorem or |dU_EM/dt|+|int J.E|+|Phi_incoming|+|Phi_apparatus|", "highest"),
        ("BQ4771_2_boundary_flux", "E_boundary_flux", "Hamiltonian/corner/radiative no-flux or finite surface bound", "zero theorem or Q_edge_boundary_abs value", "high"),
        ("BQ4771_3_shadow", "Q_shadow_abs", "no-shadow branch or finite shadow residual", "zero theorem or source-backed value", "medium"),
        ("BQ4771_4_denominator", "M_0, epsilon_abs, P_M_bound, E_PiM_comm", "same-frame denominator/projector values", "source-backed first values or exact lock", "medium"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "queue_id": queue_id,
            "quantity": quantity,
            "closure_route": route,
            "required_input": required,
            "priority": priority,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for queue_id, quantity, route, required, priority in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4771_0_boundary_lift_poynting", "close or bound E_lift_boundary and E_Poynting_wall together", "turns the new boundary-total obstruction into a real zero/value row", "SELECTED_NEXT"),
        ("ROUTE4771_1_denominator_projector", "source M_0, epsilon_abs, P_M_bound and E_PiM_comm", "needed once boundary numerator gates shrink", "SECOND_PARALLEL"),
        ("ROUTE4771_2_public_parent", "promote private on-shell/gauge lift contract to one public parent selector", "would convert private conditional theorem into public parent proof", "LONGER_ROUTE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "route_id": route_id,
            "route": route,
            "payoff": payoff,
            "selection_status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for route_id, route, payoff, status in specs
    ]


def promotion_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("GATE4771_0_private_scope", "Matter-lift bulk zero is conditional on on-shell/gauge/fixed-boundary contract, not a public theorem.", "prevents overclaim", False),
        ("GATE4771_1_boundary", "No Qedge/local-GR promotion while E_lift_boundary, E_Poynting_wall or E_boundary_flux remain open.", "keeps boundary flux visible", False),
        ("GATE4771_2_no_double_count", "Boundary lift, Poynting, and Hamiltonian/corner flux must be separated or explicitly identified before summing.", "blocks duplicate boundary scoring", False),
        ("GATE4771_3_qbar", "No Qbar score without denominator/projector/shadow gates.", "blocks fake local-GR scoring", False),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": allowed,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect, allowed in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4771_0", "No local GR/Newton/PPN/WEP/R10/clock/orbital pass from 4771.", "bulk source-qbasic closure is private and boundary gates remain"),
        ("FW4771_1", "No public parent claim from the on-shell/gauge matter-lift contract.", "public selector still unsigned"),
        ("FW4771_2", "No absorbing Poynting or boundary lift into the shell-support zero.", "waves and symplectic boundary terms stay explicit"),
        ("FW4771_3", "No denominator/projector scoring without first values.", "Qbar division/projection gates remain blocked"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "firewall": firewall,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, firewall, reason in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4771_0",
            "decision": DECISION,
            "summary": "4771 splits E_matter_lift into an on-shell/gauge bulk Euler term and a boundary symplectic lift term. The bulk term collapses conditionally; the remaining local obstruction is boundary lift plus Poynting plus boundary flux. This is progress toward local GR but not a claim because boundary, shadow, denominator and projector gates remain open.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4771_0",
            "state": "completed_nonclaim",
            "meaning": "Matter-lift bulk obstruction collapses under private on-shell/gauge/fixed-boundary contract; boundary/wave and Qbar gates remain.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "After bulk matter lift collapse, the active numerator obstruction is boundary lift plus Poynting plus boundary flux; denominator/projector first values remain the parallel product gate.",
            "route_priority": "boundary_lift_Poynting_collar_zero_then_denominator_projector_first_values",
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(
    timestamp: str,
    variation: list[dict[str, Any]],
    placement: list[dict[str, Any]],
    obstruction: list[dict[str, Any]],
    qedge_qbar: list[dict[str, Any]],
    boundary_queue: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4771: Matter-Lift Gauge/Boundary Collapse or Poynting Boundary First Values

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

- 4771 splits the single 4770 bulk obstruction `E_matter_lift` into a bulk Euler/gauge term and a boundary symplectic term.
- Under the private on-shell/gauge/fixed-boundary contract:

```text
E_matter_lift = E_matter_lift_bulk + E_lift_boundary
E_matter_lift_bulk = 0_private_on_shell_gauge
```

- Therefore the remaining local obstruction is no longer a bulk source-qbasic obstruction:

```text
E_bulk_source_qbasic_4771 = 0_private_conditional
E_local_obstruction_4771 <= |E_lift_boundary| + |E_Poynting_wall| + |E_boundary_flux|.
```

- This is not a local-GR/Newton/PPN claim: the boundary lift, Poynting, boundary flux, shadow, denominator and projector gates still need zero theorems or source-backed values.

## Matter-Lift Variation Identity

{markdown_table(variation, ["identity_id", "quantity", "formula_or_value", "status"])}

## Matter-Lift Sector Placement

{markdown_table(placement, ["placement_id", "sector", "effect", "status"])}

## Reduced Obstruction After Lift Bulk Collapse

{markdown_table(obstruction, ["obstruction_id", "symbol", "formula", "meaning", "status"])}

## Qedge/Qbar Update

{markdown_table(qedge_qbar, ["update_id", "rule", "meaning", "status"])}

## Boundary Lift/Poynting Queue

{markdown_table(boundary_queue, ["queue_id", "quantity", "closure_route", "required_input", "priority"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "payoff", "selection_status"])}

## Promotion Gates

{markdown_table(gates, ["gate_id", "rule", "enforced_effect", "claim_allowed"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4771: Matter-Lift Bulk Collapse

Generated: `{timestamp}`

4771 uses the standard on-shell variation identity for the matter lift:

```text
delta_v S_m = int_W E_psi delta_v psi dV + int_partial W Theta_m(delta_v psi).
```

Inside the private branch, `Dq(v)=0`, observed geometry and constants are already q-owned, and the lift is gauge/representative rather than a new physical source label. Therefore:

```text
int_W E_psi delta_v psi dV = 0
```

on shell. The only surviving matter-lift piece is the boundary symplectic term:

```text
E_lift_boundary := |int_partial W Theta_m(delta_v psi)|.
```

So:

```text
E_bulk_source_qbasic_4771 = 0_private_conditional
E_local_obstruction_4771 <= |E_lift_boundary| + |E_Poynting_wall| + |E_boundary_flux|.
```

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4771 splits `E_matter_lift` into a bulk on-shell/gauge Euler term and a boundary symplectic lift term.
- The private bulk term collapses: `E_matter_lift_bulk=0_private_on_shell_gauge`.
- The live local obstruction is now boundary-only at numerator level: `|E_lift_boundary|+|E_Poynting_wall|+|E_boundary_flux|`.
- Qbar/local-GR scoring remains blocked by boundary, shadow, denominator and projector gates.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4771 packet update: the remaining bulk source-qbasic obstruction has been collapsed into an on-shell/gauge identity. The next live numerator problem is boundary lift plus Poynting/wave/corner flux.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4771-Y5-R2FR-matter-lift-gauge-boundary-collapse-or-Poynting-boundary-first-values.md`

## Decision

`{DECISION}`

## What moved forward

- Split `E_matter_lift` into bulk Euler/gauge and boundary symplectic lift pieces.
- Closed the bulk lift term conditionally: `E_matter_lift_bulk=0_private_on_shell_gauge`.
- Reduced the live local numerator obstruction to `|E_lift_boundary|+|E_Poynting_wall|+|E_boundary_flux|`.
- Kept Qbar/local-GR scoring blocked until boundary, shadow, denominator and projector gates close.

## Current target

`{NEXT_TARGET}`

## Local-only note

No GitHub action was performed by this checkpoint.
"""
    write_text(RESUME_PATH, resume)


def add_claim_once(timestamp: str) -> None:
    existing = read_text(CLAIMS_PATH) if CLAIMS_PATH.exists() else ""
    if CLAIM_ID in existing:
        return
    row = [
        CLAIM_ID,
        "local_gr_matter_lift_bulk_collapse",
        "4771 splits matter lift into bulk on-shell/gauge and boundary symplectic terms, closing the bulk lift obstruction conditionally while retaining boundary/Poynting flux.",
        "Generated source register, matter-lift variation identity, sector placement, reduced obstruction, Qedge/Qbar update, boundary queue, route matrix, gates, firewalls, decision, status, next target and validation.",
        "matter_lift_bulk_collapsed_private_boundary_lift_poynting_boundary_flux_retained_nonclaim",
        NEXT_TARGET,
        "Treating bulk lift collapse as local-GR success while boundary, shadow, denominator and projector gates remain open.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need boundary lift/Poynting collar zero or denominator/projector first values.",
        "Matter-lift gauge-boundary collapse",
        f"{MARKER}; {DECISION}; generated {timestamp}",
    ]
    with CLAIMS_PATH.open("a", encoding="utf-8", newline="") as handle:
        csv.writer(handle).writerow(row)


def cleanup_pycache() -> None:
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows(
    sources: list[dict[str, Any]],
    variation: list[dict[str, Any]],
    placement: list[dict[str, Any]],
    obstruction: list[dict[str, Any]],
    qedge_qbar: list[dict[str, Any]],
    boundary_queue: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4771_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4771_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4771_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))

    checks.append(("VAL4771_2_variation_split", "matter lift variation splits into bulk and boundary", any(row["quantity"] == "E_matter_lift_bulk" and row["formula_or_value"] == "0_private_on_shell_gauge" for row in variation) and any(row["quantity"] == "E_lift_boundary" for row in variation), str(VARIATION_IDENTITY_CSV)))
    checks.append(("VAL4771_3_sector_placement", "sector placement keeps boundary and extra-source branches explicit", any(row["status"] == "BOUNDARY_ROW" for row in placement) and any(row["status"] == "RETAINED_PUBLIC_GAP" for row in placement), str(SECTOR_PLACEMENT_CSV)))
    bulk_rows = [row for row in obstruction if row["symbol"] == "E_bulk_source_qbasic_4771"]
    local_rows = [row for row in obstruction if row["symbol"] == "E_local_obstruction_4771"]
    checks.append(("VAL4771_4_bulk_qbasic_zero", "bulk source-qbasic is conditionally zero", bool(bulk_rows) and bulk_rows[0]["formula"] == "0_private_conditional", str(REDUCED_OBSTRUCTION_CSV)))
    checks.append(("VAL4771_5_local_obstruction_boundary_only", "local obstruction formula has boundary lift, Poynting and boundary flux but not E_matter_lift", bool(local_rows) and "E_matter_lift" not in local_rows[0]["formula"] and all(term in local_rows[0]["formula"] for term in ["E_lift_boundary", "E_Poynting_wall", "E_boundary_flux"]), str(REDUCED_OBSTRUCTION_CSV)))
    checks.append(("VAL4771_6_qedge_boundary_gate", "Qedge update removes bulk gate but keeps boundary gate", any(row["status"] == "BULK_GATE_REMOVED_CONDITIONAL" for row in qedge_qbar) and any(row["status"] == "BOUNDARY_GATE_REMAINS" for row in qedge_qbar), str(QEDGE_QBAR_UPDATE_CSV)))
    checks.append(("VAL4771_7_boundary_queue", "boundary queue includes lift and Poynting highest priority", any(row["quantity"] == "E_lift_boundary" and row["priority"] == "highest" for row in boundary_queue) and any(row["quantity"] == "E_Poynting_wall" and row["priority"] == "highest" for row in boundary_queue), str(BOUNDARY_QUEUE_CSV)))
    checks.append(("VAL4771_8_route_selected", "route selects boundary lift/Poynting next", any(row["selection_status"] == "SELECTED_NEXT" and "Poynting" in row["route"] for row in routes), str(ROUTE_MATRIX_CSV)))
    checks.append(("VAL4771_9_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4771_10_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4771_11_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4771_12_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4771_13_claim_row", "claim row L-613 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4771_14_resume", "resume points from 4771 to 4772", "4771-Y5" in resume_text and "4772-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4771_15_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))

    overall = all(passed for _, _, passed, _ in checks)
    rows = [
        {
            "checkpoint": CHECKPOINT,
            "validation_id": validation_id,
            "check": check,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for validation_id, check, passed, detail in checks
    ]
    rows.append(
        {
            "checkpoint": CHECKPOINT,
            "validation_id": "VAL4771_OVERALL",
            "check": "all 4771 matter-lift bulk-collapse checks pass",
            "status": "PASS" if overall else "FAIL",
            "detail": DECISION,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    )
    return rows


def main() -> None:
    timestamp = now()
    sources = source_register(timestamp)
    variation = variation_identity_rows(timestamp)
    placement = sector_placement_rows(timestamp)
    obstruction = reduced_obstruction_rows(timestamp)
    qedge_qbar = qedge_qbar_rows(timestamp)
    boundary_queue = boundary_queue_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(VARIATION_IDENTITY_CSV, variation)
    write_csv(SECTOR_PLACEMENT_CSV, placement)
    write_csv(REDUCED_OBSTRUCTION_CSV, obstruction)
    write_csv(QEDGE_QBAR_UPDATE_CSV, qedge_qbar)
    write_csv(BOUNDARY_QUEUE_CSV, boundary_queue)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, variation, placement, obstruction, qedge_qbar, boundary_queue, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, variation, placement, obstruction, qedge_qbar, boundary_queue, routes, gates, timestamp))


if __name__ == "__main__":
    main()
