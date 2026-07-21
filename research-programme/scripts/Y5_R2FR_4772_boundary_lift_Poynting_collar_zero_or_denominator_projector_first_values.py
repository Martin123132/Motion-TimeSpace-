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

CHECKPOINT = "4772"
CLAIM_ID = "L-614"
MARKER = "PPC4161_BOUNDARY_LIFT_POYNTING_COLLAR_ZERO_OR_DENOMINATOR_PROJECTOR_FIRST_VALUES_4772"
PACKET_MARKER = "PPC4161_PACKET_BOUNDARY_LIFT_POYNTING_COLLAR_ZERO_OR_DENOMINATOR_PROJECTOR_FIRST_VALUES_4772"
DECISION = "COMPACT_STATIONARY_COLLAR_ZERO_THEOREM_DERIVED_CONDITIONAL_BOUNDARY_TOTAL_ZERO_CANDIDATE_OPEN_COLLAR_FINITE_ENVELOPE_RETAINED_QBAR_STILL_BLOCKED_BY_SHADOW_DENOMINATOR_PROJECTOR_NONCLAIM"
NEXT_TARGET = "4773-Y5-R2FR-collar-instance-certificate-or-shadow-denominator-projector-first-values.md"

DOC_PATH = POST / "4772-Y5-R2FR-boundary-lift-Poynting-collar-zero-or-denominator-projector-first-values.md"
FORMAL_PATH = FORMAL / "788-PPC4161-boundary-lift-Poynting-collar-zero-or-denominator-projector-first-values.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4772_SOURCE_REGISTER.csv"
COLLAR_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4772_COMPACT_STATIONARY_COLLAR_ZERO_THEOREM.csv"
FINITE_ENVELOPE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4772_OPEN_COLLAR_FINITE_ENVELOPE.csv"
QEDGE_QBAR_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4772_QEDGE_QBAR_UPDATE.csv"
SCORING_GATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4772_LOCAL_SCORING_GATE_STATUS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4772_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4772_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4772_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4772_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4772_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4772_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4772_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4772_0_4771_obstruction", SOURCE_DIR / "P8_Y5_R2FR_4771_REDUCED_OBSTRUCTION_AFTER_LIFT_BULK_COLLAPSE.csv", "RO4771_6_local_obstruction", "4771 boundary-only local obstruction"),
    ("SRC4772_1_4771_queue", SOURCE_DIR / "P8_Y5_R2FR_4771_BOUNDARY_LIFT_POYNTING_QUEUE.csv", "BQ4771_1_poynting_collar", "4771 boundary/Poynting queue"),
    ("SRC4772_2_4771_qedge", SOURCE_DIR / "P8_Y5_R2FR_4771_QEDGE_QBAR_UPDATE.csv", "QQ4771_1_boundary_birth", "4771 Qedge boundary birth gate"),
    ("SRC4772_3_4766_poynting", SOURCE_DIR / "P8_Y5_R2FR_4766_POYNTING_WALL_FLUX_ROW.csv", "PWF4766_2_wall_flux_bound", "4766 Poynting wall bound"),
    ("SRC4772_4_4768_poynting_candidate", SOURCE_DIR / "P8_Y5_R2FR_4768_POYNTING_WALL_FIRST_VALUE_CANDIDATE.csv", "PFV4768_5_total", "4768 Poynting zero candidate"),
    ("SRC4772_5_4695_poynting", SOURCE_DIR / "P8_Y5_R2FR_4695_POYNTING_FLUX_ROWS.csv", "FX4695_0_stationary_zero", "4695 stationary Poynting zero"),
    ("SRC4772_6_4714_owner", SOURCE_DIR / "P8_Y5_R2FR_4714_EM_STRESS_POYNTING_OWNER_THEOREM.csv", "EMP4714_4_no_double_count", "4714 EM/Poynting no-double-count owner"),
    ("SRC4772_7_boundary_alpha3", SOURCE_DIR / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv", "T2_no_normal_flux_from_tangential_trace", "boundary no-normal-flux conditional lemma"),
    ("SRC4772_8_boundary_repair", SOURCE_DIR / "P8_BOUNDARY_SCALAR_PREMISE_REPAIR_LEDGER.csv", "R4_flux_zero", "boundary scalar premise repair ledger"),
    ("SRC4772_9_vertical_silence", FORMAL / "193-PPC4161-quotient-naturality-vertical-silence-theorem.md", "B_v | partial W_loc = fixed/exact/routed", "vertical boundary fixed/exact/routed clause"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    COLLAR_THEOREM_CSV,
    FINITE_ENVELOPE_CSV,
    QEDGE_QBAR_UPDATE_CSV,
    SCORING_GATE_CSV,
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


def collar_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "CCT4772_0_branch_selector",
            "compact_stationary_isolated_same_Hodge_fixed_boundary_collar",
            "source collar is compact/fixed before readout, stationary, same Maxwell-Hodge/current owner, no incoming/apparatus/radiative flux, and boundary terms are fixed/exact/q-owned/scalar-trace no-flux",
            "branch_contract_written",
            "CONDITIONAL_BRANCH_NOT_INSTANCE",
        ),
        (
            "CCT4772_1_lift_boundary_zero",
            "E_lift_boundary",
            "delta_v psi has compact support or fixed boundary data, or Theta_m(delta_v psi) is exact/q-owned/routed on partial W",
            "0_private_if_CCT4772_0",
            "ZERO_CANDIDATE",
        ),
        (
            "CCT4772_2_poynting_zero",
            "E_Poynting_wall",
            "time_avg(dU_EM/dt)=0, time_avg(int_W J.E dV)=0, Phi_incoming=0, Phi_apparatus=0 on same-Hodge stationary collar",
            "0_private_if_CCT4772_0",
            "ZERO_CANDIDATE",
        ),
        (
            "CCT4772_3_boundary_flux_zero",
            "E_boundary_flux",
            "Hamiltonian/corner/boundary stress is fixed/exact/q-owned or scalar trace with no normal momentum flux",
            "0_private_if_CCT4772_0",
            "ZERO_CANDIDATE_CONDITIONAL",
        ),
        (
            "CCT4772_4_no_double_count",
            "boundary channel placement",
            "E_lift_boundary, E_Poynting_wall and Hamiltonian/corner flux must be disjoint rows or explicitly identified before summing",
            "no_hidden_cancellation",
            "ACCOUNTING_RULE",
        ),
        (
            "CCT4772_5_total",
            "E_boundary_total_4772",
            "|E_lift_boundary|+|E_Poynting_wall|+|E_boundary_flux|",
            "0_private_collar_candidate",
            "TOTAL_ZERO_CANDIDATE_NONCLAIM",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "quantity": quantity,
            "condition_or_statement": statement,
            "value_or_rule": value,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, quantity, statement, value, status in specs
    ]


def finite_envelope_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("OCE4772_0_lift", "E_lift_boundary", "|int_partialW Theta_m(delta_v psi)|", "matter lift symplectic boundary flux", "VALUE_NEEDED_IF_OPEN"),
        ("OCE4772_1_poynting", "E_Poynting_wall", "|dU_EM/dt|+|int_W J.E dV|+|Phi_incoming|+|Phi_apparatus|", "open/radiative/nonstationary EM wall flux", "VALUE_NEEDED_IF_OPEN"),
        ("OCE4772_2_hamiltonian_corner", "E_boundary_flux", "|F_rad|+|B_Ham_corner|+|B_normal_momentum|+|B_app_support|", "Hamiltonian/corner/radiative/non-scalar normal flux", "VALUE_NEEDED_IF_OPEN"),
        ("OCE4772_3_total", "E_boundary_total_4772", "|int_partialW Theta_m(delta_v psi)|+|dU_EM/dt|+|int_W J.E dV|+|Phi_incoming|+|Phi_apparatus|+|F_rad|+|B_Ham_corner|+|B_normal_momentum|+|B_app_support|", "no-cancellation finite open-collar envelope", "FINITE_FALLBACK_TEMPLATE"),
        ("OCE4772_4_score_policy", "boundary score policy", "zero candidate can be used only after a source collar instance signs CCT4772_0; otherwise use OCE4772_3", "prevents branch smuggling", "POLICY_ROW"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "envelope_id": envelope_id,
            "quantity": quantity,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for envelope_id, quantity, formula, meaning, status in specs
    ]


def qedge_qbar_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("QQ4772_0_bulk_qbasic", "E_bulk_source_qbasic_4771=0_private_conditional is retained.", "bulk source-qbasic no longer blocks the private compact-collar branch", "BULK_CLOSED_PRIVATE"),
        ("QQ4772_1_shell_zero", "Q_edge_shell_abs=0 if bulk qbasicity, pre-readout support, and no boundary lift birth/death hold.", "compact collar branch supplies no boundary birth/death; open collar uses finite envelope", "SHELL_ZERO_CONDITIONAL"),
        ("QQ4772_2_boundary_zero", "Q_edge_boundary_abs=0_private_collar_candidate if E_boundary_total_4772=0.", "requires actual compact stationary isolated source-collar instance", "BOUNDARY_ZERO_CANDIDATE"),
        ("QQ4772_3_open_boundary", "Q_edge_boundary_abs <= E_boundary_total_4772_open + other corner/shadow rows on open collars.", "no cancellation; use finite envelope if branch is not signed", "FINITE_FALLBACK"),
        ("QQ4772_4_qbar_product", "Qbar_XH score remains blocked by Q_shadow_abs, M_lower, P_M_bound and E_PiM_comm.", "boundary progress is necessary but not enough for local-GR/Newton scoring", "PRODUCT_BLOCKED"),
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


def scoring_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("SG4772_0_collar_instance", "compact collar instance", "must sign CCT4772_0 for the actual local source arena", "not yet supplied", False, "INSTANCE_MISSING"),
        ("SG4772_1_boundary_total", "E_boundary_total_4772", "zero candidate or finite source-backed envelope", "conditional zero candidate plus finite template exists", False, "CONDITIONAL_OR_VALUE_NEEDED"),
        ("SG4772_2_shadow", "Q_shadow_abs", "no-shadow theorem or finite residual", "not closed by collar theorem", False, "MISSING"),
        ("SG4772_3_denominator", "M_lower=M_0(1-epsilon_abs)>0", "source-backed positive denominator", "M_0 and epsilon_abs still missing values", False, "MISSING"),
        ("SG4772_4_projector", "P_M_bound and E_PiM_comm", "finite norm and zero/bounded commutator", "projector first values still missing", False, "MISSING"),
        ("SG4772_5_qbar", "Qbar_XH local score", "collar instance, shadow, denominator and projector all closed", "blocked by SG4772_0..4", False, "PRODUCT_BLOCKED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "gate": gate,
            "needed_evidence": needed,
            "current_status": current,
            "score_fires_now": fires,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, needed, current, fires, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4772_0_collar_instance", "write the actual compact-collar source instance certificate", "turns the zero candidate into a branch-specific usable gate, or rejects it cleanly", "SELECTED_NEXT"),
        ("ROUTE4772_1_shadow_denominator_projector", "fill Q_shadow_abs, M_0, epsilon_abs, P_M_bound and E_PiM_comm", "needed before any Qbar/local-GR score can fire even if collar zero holds", "PARALLEL_HIGH_VALUE"),
        ("ROUTE4772_2_open_collar_values", "fill finite open-collar boundary envelope values", "lets the branch be bounded instead of zero-assumed if compact collar fails", "FALLBACK"),
        ("ROUTE4772_3_public_parent", "promote collar branch to public parent selector", "would turn conditional private collar theorem into public MTS result", "LONGER_ROUTE"),
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
        ("GATE4772_0_instance", "Do not use E_boundary_total_4772=0 until an actual compact stationary isolated collar instance signs all CCT4772_0 clauses.", "blocks branch smuggling", False),
        ("GATE4772_1_open_fallback", "Open/radiative/nonstationary collars must use the finite envelope, not the zero candidate.", "keeps waves and apparatus visible", False),
        ("GATE4772_2_no_double_count", "Boundary lift, Poynting and Hamiltonian/corner flux cannot be double-counted or cancelled against each other unless one owner identity proves equivalence.", "blocks fake no-cancellation algebra", False),
        ("GATE4772_3_qbar", "Qbar/local-GR score cannot fire without shadow, denominator and projector gates.", "blocks premature local-GR/Newton scoring", False),
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
        ("FW4772_0", "No local GR/Newton/PPN/WEP/R10/clock/orbital pass from 4772.", "collar theorem is conditional and product gates remain blocked"),
        ("FW4772_1", "No zero boundary unless the actual source collar signs compact, stationary, same-Hodge, fixed/exact/q-owned, no-flux clauses.", "prevents zero by naming"),
        ("FW4772_2", "No hidden cancellation between lift boundary, Poynting and Hamiltonian/corner terms.", "keeps no-cancellation accounting"),
        ("FW4772_3", "No Qbar score without shadow/denominator/projector values.", "division/projection gates remain missing"),
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
            "decision_id": "DEC4772_0",
            "decision": DECISION,
            "summary": "4772 derives the compact stationary isolated collar zero theorem for the remaining boundary numerator obstruction. It sets E_lift_boundary, E_Poynting_wall and E_boundary_flux to zero only under a named private collar contract, and writes the finite open-collar envelope when that contract is not signed. Qbar/local-GR scoring remains blocked by missing collar instance, shadow, denominator and projector gates.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4772_0",
            "state": "completed_nonclaim",
            "meaning": "Boundary total zero candidate is derived for compact stationary collar branch; open-collar finite envelope and product gates remain.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "The zero theorem now needs an actual source-collar instance certificate; in parallel, Qbar still needs shadow, denominator and projector first values.",
            "route_priority": "collar_instance_certificate_then_shadow_denominator_projector_first_values",
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(
    timestamp: str,
    collar: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    qedge_qbar: list[dict[str, Any]],
    scoring: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4772: Boundary-Lift/Poynting Collar Zero or Denominator/Projector First Values

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

- 4772 derives a compact stationary isolated collar zero theorem for the remaining boundary numerator obstruction.
- The theorem is conditional/private: it is not yet an actual source-collar instance and not a local-GR/Newton claim.
- Under the collar contract:

```text
E_lift_boundary = 0
E_Poynting_wall = 0
E_boundary_flux = 0
E_boundary_total_4772 := |E_lift_boundary|+|E_Poynting_wall|+|E_boundary_flux| = 0.
```

- If the collar is open, radiative, nonstationary, apparatus-supported, or not fixed/exact/q-owned, the finite envelope must be used instead:

```text
E_boundary_total_4772_open <=
  |int_partialW Theta_m(delta_v psi)|
+ |dU_EM/dt| + |int_W J.E dV|
+ |Phi_incoming| + |Phi_apparatus|
+ |F_rad| + |B_Ham_corner| + |B_normal_momentum| + |B_app_support|.
```

## Compact Stationary Collar Zero Theorem

{markdown_table(collar, ["theorem_id", "quantity", "value_or_rule", "status"])}

## Open-Collar Finite Envelope

{markdown_table(finite, ["envelope_id", "quantity", "formula", "status"])}

## Qedge/Qbar Update

{markdown_table(qedge_qbar, ["update_id", "rule", "meaning", "status"])}

## Local Scoring Gate Status

{markdown_table(scoring, ["gate_id", "gate", "needed_evidence", "current_status", "score_fires_now", "status"])}

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

    formal = f"""# PPC4161 4772: Boundary-Lift/Poynting Compact Collar Theorem

Generated: `{timestamp}`

4772 combines the remaining boundary numerator rows into one collar gate:

```text
E_boundary_total_4772 :=
  |E_lift_boundary| + |E_Poynting_wall| + |E_boundary_flux|.
```

On the compact stationary isolated collar branch:

```text
fixed/exact/q-owned matter boundary       -> E_lift_boundary = 0
same-Hodge stationary EM no-flux collar   -> E_Poynting_wall = 0
scalar/topological/fixed boundary no-flux -> E_boundary_flux = 0
```

so:

```text
E_boundary_total_4772 = 0_private_collar_candidate.
```

For open collars the finite no-cancellation envelope is retained. Qbar/local-GR still cannot score until a real collar instance plus shadow, denominator and projector gates are supplied.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4772 derives the compact stationary isolated collar zero theorem for the remaining boundary numerator obstruction.
- The zero is conditional/private: `E_boundary_total_4772=0_private_collar_candidate` only if fixed/exact/q-owned matter boundary, same-Hodge stationary EM no-flux, and scalar/topological/fixed boundary no-flux clauses are signed for the actual source collar.
- Open/radiative/nonstationary collars retain the finite no-cancellation envelope.
- Qbar/local-GR scoring remains blocked by collar instance, shadow, denominator and projector gates.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4772 packet update: the boundary numerator problem is now a precise two-branch gate: compact stationary collar zero candidate versus finite open-collar envelope. Next is source-collar instance certification or shadow/denominator/projector first values.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4772-Y5-R2FR-boundary-lift-Poynting-collar-zero-or-denominator-projector-first-values.md`

## Decision

`{DECISION}`

## What moved forward

- Derived the compact stationary isolated collar zero theorem for `E_boundary_total_4772`.
- Kept the open/radiative/nonstationary collar as a finite no-cancellation envelope.
- Clarified that Qedge boundary zero needs an actual source-collar instance, not just the branch theorem.
- Left Qbar/local-GR scoring blocked by collar instance, shadow, denominator and projector gates.

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
        "local_gr_boundary_lift_poynting_collar_zero",
        "4772 derives a conditional compact stationary collar zero theorem for the boundary numerator obstruction and retains an open-collar finite envelope.",
        "Generated source register, collar zero theorem, open-collar finite envelope, Qedge/Qbar update, local scoring gates, route matrix, promotion gates, firewalls, decision, status, next target and validation.",
        "compact_collar_zero_theorem_conditional_open_collar_finite_envelope_qbar_blocked_nonclaim",
        NEXT_TARGET,
        "Using the collar zero theorem without an actual source-collar instance, or scoring Qbar before shadow/denominator/projector gates close.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need collar instance certificate or shadow/denominator/projector first values.",
        "Boundary lift/Poynting collar zero theorem",
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
    collar: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    qedge_qbar: list[dict[str, Any]],
    scoring: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4772_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4772_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4772_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))

    checks.append(("VAL4772_2_zero_candidate", "collar theorem has total zero candidate", any(row["quantity"] == "E_boundary_total_4772" and row["value_or_rule"] == "0_private_collar_candidate" for row in collar), str(COLLAR_THEOREM_CSV)))
    checks.append(("VAL4772_3_three_boundary_zeros", "lift, Poynting and boundary flux zero candidates exist", all(any(row["quantity"] == quantity and "ZERO" in row["status"] for row in collar) for quantity in ["E_lift_boundary", "E_Poynting_wall", "E_boundary_flux"]), str(COLLAR_THEOREM_CSV)))
    checks.append(("VAL4772_4_open_fallback", "finite envelope has no-cancellation open-collar total", any(row["quantity"] == "E_boundary_total_4772" and "Theta_m" in row["formula"] and "Phi_incoming" in row["formula"] and "B_Ham_corner" in row["formula"] for row in finite), str(FINITE_ENVELOPE_CSV)))
    checks.append(("VAL4772_5_qedge_branches", "Qedge update has boundary zero candidate and finite fallback", any(row["status"] == "BOUNDARY_ZERO_CANDIDATE" for row in qedge_qbar) and any(row["status"] == "FINITE_FALLBACK" for row in qedge_qbar), str(QEDGE_QBAR_UPDATE_CSV)))
    checks.append(("VAL4772_6_score_blocked", "local scoring remains blocked", all(row["score_fires_now"] is False for row in scoring) and any(row["status"] == "PRODUCT_BLOCKED" for row in scoring), str(SCORING_GATE_CSV)))
    checks.append(("VAL4772_7_route_selected", "route selects collar instance next", any(row["selection_status"] == "SELECTED_NEXT" and "collar" in row["route"] for row in routes), str(ROUTE_MATRIX_CSV)))
    checks.append(("VAL4772_8_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4772_9_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4772_10_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4772_11_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4772_12_claim_row", "claim row L-614 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4772_13_resume", "resume points from 4772 to 4773", "4772-Y5" in resume_text and "4773-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4772_14_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))

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
            "validation_id": "VAL4772_OVERALL",
            "check": "all 4772 collar-zero/finite-envelope checks pass",
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
    collar = collar_theorem_rows(timestamp)
    finite = finite_envelope_rows(timestamp)
    qedge_qbar = qedge_qbar_rows(timestamp)
    scoring = scoring_gate_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(COLLAR_THEOREM_CSV, collar)
    write_csv(FINITE_ENVELOPE_CSV, finite)
    write_csv(QEDGE_QBAR_UPDATE_CSV, qedge_qbar)
    write_csv(SCORING_GATE_CSV, scoring)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, collar, finite, qedge_qbar, scoring, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, collar, finite, qedge_qbar, scoring, routes, gates, timestamp))


if __name__ == "__main__":
    main()
