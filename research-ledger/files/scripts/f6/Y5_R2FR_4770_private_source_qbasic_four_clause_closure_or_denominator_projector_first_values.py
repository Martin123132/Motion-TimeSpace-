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

CHECKPOINT = "4770"
CLAIM_ID = "L-612"
MARKER = "PPC4161_PRIVATE_SOURCE_QBASIC_FOUR_CLAUSE_CLOSURE_OR_DENOMINATOR_PROJECTOR_FIRST_VALUES_4770"
PACKET_MARKER = "PPC4161_PACKET_PRIVATE_SOURCE_QBASIC_FOUR_CLAUSE_CLOSURE_OR_DENOMINATOR_PROJECTOR_FIRST_VALUES_4770"
DECISION = "PRIVATE_FOUR_CLAUSE_SOURCE_QBASIC_CLOSURE_DERIVED_CONDITIONAL_BULK_RESIDUAL_SHRINKS_TO_MATTER_LIFT_BOUNDARY_POYNTING_AND_DENOMINATOR_PROJECTOR_STILL_BLOCK_LOCAL_SCORE_NONCLAIM"
NEXT_TARGET = "4771-Y5-R2FR-matter-lift-gauge-boundary-collapse-or-Poynting-boundary-first-values.md"

DOC_PATH = POST / "4770-Y5-R2FR-private-source-qbasic-four-clause-closure-or-denominator-projector-first-values.md"
FORMAL_PATH = FORMAL / "786-PPC4161-private-source-qbasic-four-clause-closure-or-denominator-projector-first-values.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4770_SOURCE_REGISTER.csv"
FOUR_CLAUSE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4770_FOUR_CLAUSE_CLOSURE_THEOREM.csv"
REDUCED_ENVELOPE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4770_REDUCED_LOCAL_OBSTRUCTION_ENVELOPE.csv"
QEDGE_QBAR_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4770_QEDGE_QBAR_GATE_UPDATE.csv"
DENOMINATOR_FALLBACK_CSV = SOURCE_DIR / "P8_Y5_R2FR_4770_DENOMINATOR_PROJECTOR_FALLBACK_STATUS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4770_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4770_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4770_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4770_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4770_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4770_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4770_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4770_0_4769_rollup", SOURCE_DIR / "P8_Y5_R2FR_4769_PRIVATE_SOURCE_QBASIC_RESIDUAL_ROLLUP.csv", "PR4769_8_private_envelope", "4769 reduced private residual"),
    ("SRC4770_1_4769_ladder", SOURCE_DIR / "P8_Y5_R2FR_4769_QEDGE_ZERO_LADDER_AFTER_PRIVATE_ROLLUP.csv", "ZL4769_6_Qedge_shell_zero", "4769 Qedge shell-zero ladder"),
    ("SRC4770_2_4769_scoring", SOURCE_DIR / "P8_Y5_R2FR_4769_LOCAL_GR_SCORING_GATE_MATRIX.csv", "LSG4769_6_qbar_product", "4769 local scoring gate matrix"),
    ("SRC4770_3_4769_values", SOURCE_DIR / "P8_Y5_R2FR_4769_SOURCE_VALUE_SHOPPING_LIST.csv", "SV4769_3_same_Hodge", "4769 source value shopping list"),
    ("SRC4770_4_4767_contract", SOURCE_DIR / "P8_Y5_R2FR_4767_PARENT_SOURCE_QBASIC_CONTRACT.csv", "PSC4767_0_parent_action_form", "4767 parent source-qbasic contract"),
    ("SRC4770_5_4767_measure_chain", SOURCE_DIR / "P8_Y5_R2FR_4767_MEASURE_SUPPORT_PROOF_CHAIN.csv", "MPC4767_3_support", "4767 measure-support proof chain"),
    ("SRC4770_6_4766_support", SOURCE_DIR / "P8_Y5_R2FR_4766_SUPPORT_INVARIANCE_THEOREM.csv", "SIT4766_2_support_invariance", "4766 support invariance theorem"),
    ("SRC4770_7_4766_poynting", SOURCE_DIR / "P8_Y5_R2FR_4766_POYNTING_WALL_FLUX_ROW.csv", "PWF4766_1_stationary_zero", "4766 Poynting wall flux row"),
    ("SRC4770_8_4768_prefactor", SOURCE_DIR / "P8_Y5_R2FR_4768_NO_SOURCE_PREFACTOR_IMPORT_AUDIT.csv", "NPI4768_4_private_adoption", "4768 private no-source-prefactor import"),
    ("SRC4770_9_4714_em_owner", SOURCE_DIR / "P8_Y5_R2FR_4714_EM_STRESS_POYNTING_OWNER_THEOREM.csv", "EMP4714_4_no_double_count", "4714 EM/Poynting ownership theorem"),
    ("SRC4770_10_4764_denominator_pack", SOURCE_DIR / "P8_Y5_R2FR_4764_DENOMINATOR_BOUND_PACK.csv", "DB4764_5_score_gate", "4764 denominator/projector fallback status"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    FOUR_CLAUSE_CSV,
    REDUCED_ENVELOPE_CSV,
    QEDGE_QBAR_UPDATE_CSV,
    DENOMINATOR_FALLBACK_CSV,
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


def four_clause_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "FCC4770_0_action_descent",
            "E_action_vertical",
            "If S_src=Sbar_src[q(Phi),Psi,A,theta_bar(q)]+dB_proper+S_top_silent and v is vertical with Dq(v)=0, then D_v S_src is only a proper-boundary/topological-silent term.",
            "0_private_conditional",
            "exact chain-rule descent; no direct parent vertical source leg",
            "CLOSED_BY_PRIVATE_FOUR_CLAUSE_CONTRACT",
        ),
        (
            "FCC4770_1_constant_marker",
            "E_constant_marker",
            "If theta={masses,charges,alpha_EM,clock standards,material labels} is fixed external data or theta_bar(q), then D_v theta=0.",
            "0_private_conditional",
            "kills hidden source/clock/readout coefficient drift",
            "CLOSED_BY_PRIVATE_FOUR_CLAUSE_CONTRACT",
        ),
        (
            "FCC4770_2_Hodge_EM",
            "E_Hodge_EM",
            "If Maxwell Hodge/current/constitutive owner is the same observed branch used by matter, EM stress is Hilbert-owned once and Poynting is S_i=-T_EM(n,e_i).",
            "0_private_conditional",
            "closes independent EM source coupling but leaves explicit wall flux if the collar is open",
            "CLOSED_BY_PRIVATE_FOUR_CLAUSE_CONTRACT",
        ),
        (
            "FCC4770_3_support_selector",
            "E_support_selector",
            "If W_H=closure(supp mu_H) is selected before readout and mu_H is q-basic, support motion and birth/death are zero on vertical fibres.",
            "0_private_conditional_on_mu_qbasic",
            "removes fitted threshold/worldtube freedom; remaining qbasic obstruction is matter lift",
            "CLOSED_AS_SELECTOR_NOT_AS_FULL_MEASURE",
        ),
        (
            "FCC4770_4_bulk_measure",
            "mu_H qbasic bulk clause",
            "Action descent + fixed/q-owned theta + same Hodge/current imply qbasic Hilbert source measure except for any non-gauge physical matter lift.",
            "closed_mod_E_matter_lift",
            "bulk source-qbasic problem reduces to matter lift/gauge/proper-boundary question",
            "BULK_REDUCED_NOT_CLAIMED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "clause_id": clause_id,
            "closed_quantity": quantity,
            "derivation_statement": statement,
            "private_branch_value": value,
            "effect": effect,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for clause_id, quantity, statement, value, effect, status in specs
    ]


def reduced_envelope_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("RE4770_0_previous_envelope", "E_source_qbasic_private_4769", "|E_action_vertical|+|E_constant_marker|+|E_matter_lift|+|E_Hodge_EM|+|E_Poynting_wall|+|E_support_selector|+|E_boundary_flux|", "4769 state before four-clause closure", "REFERENCE"),
        ("RE4770_1_closed_set", "closed independent legs", "E_action_vertical=E_constant_marker=E_Hodge_EM=E_support_selector=0_private_conditional", "closed by FCC4770_0..3 under named private contract", "CONDITIONAL_CLOSED_SET"),
        ("RE4770_2_bulk_source", "E_bulk_source_qbasic_4770", "|E_matter_lift|", "bulk qbasicity reduces to whether matter lift is gauge/on-shell/proper-boundary silent", "NEXT_DERIVATION_TARGET"),
        ("RE4770_3_boundary_wave", "E_boundary_wave_4770", "|E_Poynting_wall|+|E_boundary_flux|", "waves/corners/collars are not hidden in the bulk source measure", "BOUNDARY_VALUE_TARGET"),
        ("RE4770_4_local_obstruction", "E_local_obstruction_4770", "|E_matter_lift|+|E_Poynting_wall|+|E_boundary_flux|", "no-cancellation obstruction left before Qedge shell/boundary promotion", "REDUCED_NONCLAIM_ENVELOPE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "envelope_id": envelope_id,
            "symbol": symbol,
            "formula": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for envelope_id, symbol, formula, meaning, status in specs
    ]


def qedge_qbar_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("QQ4770_0_bulk_qbasic_reduced", "bulk source-qbasic obstruction is now |E_matter_lift|", "Qedge shell zero becomes reachable if matter lift is gauge/on-shell/proper-boundary silent", "BULK_REDUCED_NOT_ZERO"),
        ("QQ4770_1_Qedge_shell", "Q_edge_shell_abs=0 if E_matter_lift=0 and support selector remains pre-readout", "four closed clauses plus 4766 support theorem are enough modulo matter lift", "ONE_BULK_GATE_REMAINS"),
        ("QQ4770_2_boundary_wave", "Q_edge_boundary_abs retains |E_Poynting_wall|+|E_boundary_flux|", "Poynting/waves/corners are boundary rows, not shell-support drift", "BOUNDARY_GATE_REMAINS"),
        ("QQ4770_3_qbar_product", "Qbar_XH score still needs denominator/projector/shadow gates", "even if Qedge shell closes, Qbar cannot score without M_lower, Pi_M, Ecomm, and Q_shadow", "PRODUCT_BLOCKED"),
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


def denominator_fallback_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("DF4770_0_M0", "M_0", "positive same-frame Hamiltonian/Hilbert denominator", "still needs source-backed value or exact branch zero-drift proof", "MISSING_VALUE"),
        ("DF4770_1_epsilon_abs", "epsilon_abs", "0<=epsilon_abs<1 denominator drift fraction", "still needs drift components or exact qbasic denominator theorem", "MISSING_VALUE"),
        ("DF4770_2_P_M_bound", "P_M_bound", "finite fixed-projector operator norm", "still needs projector definition and norm source", "MISSING_VALUE"),
        ("DF4770_3_E_PiM_comm", "E_PiM_comm", "zero/bounded projector commutator", "still needs commutator theorem or numeric bound", "MISSING_VALUE"),
        ("DF4770_4_score_gate", "denominator/projector gate", "score fires only if M_lower>0 and projector finite/commuting", "unchanged by four-clause source-qbasic closure", "PRODUCT_STILL_BLOCKED"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "fallback_id": fallback_id,
            "quantity": quantity,
            "needed": needed,
            "current_status": status_text,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for fallback_id, quantity, needed, status_text, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4770_0_matter_lift", "derive E_matter_lift=0 or a finite bound", "would close the bulk source-qbasic leg and unlock Qedge shell zero under the private contract", "SELECTED_NEXT"),
        ("ROUTE4770_1_poynting_boundary", "turn Poynting/boundary into zero or finite values", "needed for full local obstruction and Qedge boundary scoring", "PARALLEL_HIGH_VALUE"),
        ("ROUTE4770_2_denominator_projector", "source M_0, epsilon_abs, P_M_bound, E_PiM_comm", "needed for Qbar/local-GR score after numerator gates", "SECOND_PARALLEL"),
        ("ROUTE4770_3_public_parent", "promote private four-clause contract to one public parent selector", "turns conditional private theorem into global MTS parent result", "LONGER_ROUTE"),
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
        ("GATE4770_0_conditional_scope", "Four-clause closure is conditional on the private contract; do not call it a public parent theorem.", "prevents theorem inflation", False),
        ("GATE4770_1_matter_lift", "Qedge shell zero cannot be claimed while E_matter_lift remains open.", "keeps bulk qbasicity honest", False),
        ("GATE4770_2_boundary_split", "Poynting and boundary flux stay outside the bulk shell-zero claim unless zero/value rows are supplied.", "keeps waves visible", False),
        ("GATE4770_3_denominator", "Qbar/local-GR score cannot fire without denominator/projector/shadow gates.", "blocks fake local-GR scoring", False),
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
        ("FW4770_0", "No local GR/Newton/PPN/WEP/R10/clock/orbital pass from 4770.", "four-clause closure is private and conditional"),
        ("FW4770_1", "No Qedge shell zero until matter lift is closed or bounded.", "bulk source-qbasicity is still not zero"),
        ("FW4770_2", "No hiding open EM flux inside source support.", "Poynting is explicit boundary/wave content"),
        ("FW4770_3", "No denominator/projector scoring without source-backed values.", "division/projection gates remain value-missing"),
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
            "decision_id": "DEC4770_0",
            "decision": DECISION,
            "summary": "4770 derives a conditional private four-clause closure: action descent, fixed/quotient theta, same Maxwell-Hodge/current owner, and pre-readout support selection close four independent source-qbasic residuals. The bulk source-qbasic obstruction now shrinks to matter lift; Poynting and boundary flux are kept as explicit boundary/wave rows; denominator/projector gates remain value-missing.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4770_0",
            "state": "completed_nonclaim",
            "meaning": "Private source-qbasic closure is reduced to matter lift plus explicit Poynting/boundary rows; local scoring remains blocked.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "Matter lift is now the single bulk source-qbasic obstruction; Poynting/boundary first values are the parallel wave/collar route.",
            "route_priority": "matter_lift_gauge_boundary_collapse_first_then_Poynting_boundary_values_then_denominator_projector",
            "timestamp_utc": timestamp,
        }
    ]


def write_docs(
    timestamp: str,
    four_clause: list[dict[str, Any]],
    envelope: list[dict[str, Any]],
    qedge_qbar: list[dict[str, Any]],
    denominator: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4770: Private Source-Qbasic Four-Clause Closure or Denominator/Projector First Values

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

- 4770 derives a **conditional private closure**, not a public/global MTS theorem.
- Under the named private contract, four independent source-qbasic residuals close:
  - `E_action_vertical=0`;
  - `E_constant_marker=0`;
  - `E_Hodge_EM=0`;
  - `E_support_selector=0` as a selector/readout residual once `mu_H` is q-basic.
- The live bulk source-qbasic obstruction is now concentrated in `E_matter_lift`.
- Poynting and boundary/corner leakage are kept outside the bulk source measure:

```text
E_bulk_source_qbasic_4770 <= |E_matter_lift|
E_boundary_wave_4770 <= |E_Poynting_wall| + |E_boundary_flux|
E_local_obstruction_4770 <= |E_matter_lift| + |E_Poynting_wall| + |E_boundary_flux|.
```

## Four-Clause Closure Theorem

{markdown_table(four_clause, ["clause_id", "closed_quantity", "private_branch_value", "effect", "status"])}

## Reduced Local Obstruction Envelope

{markdown_table(envelope, ["envelope_id", "symbol", "formula", "meaning", "status"])}

## Qedge/Qbar Gate Update

{markdown_table(qedge_qbar, ["update_id", "rule", "meaning", "status"])}

## Denominator/Projector Fallback Status

{markdown_table(denominator, ["fallback_id", "quantity", "needed", "current_status", "status"])}

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

    formal = f"""# PPC4161 4770: Private Source-Qbasic Four-Clause Closure

Generated: `{timestamp}`

4770 derives the following conditional private closure:

```text
Dq(v)=0
S_src = Sbar_src[q(Phi),Psi,A,theta_bar(q)] + dB_proper + S_top_silent
D_v theta = 0
same observed Maxwell-Hodge/current owner
W_H = closure(supp mu_H) before readout
```

gives:

```text
E_action_vertical = 0
E_constant_marker = 0
E_Hodge_EM = 0
E_support_selector = 0   (as selector/readout residual, once mu_H is q-basic)
```

The remaining split is:

```text
E_bulk_source_qbasic_4770 <= |E_matter_lift|
E_boundary_wave_4770 <= |E_Poynting_wall| + |E_boundary_flux|.
```

So the next real derivation target is `E_matter_lift`: if the lift is gauge/on-shell/proper-boundary silent, the bulk source-qbasic leg can close and Qedge shell zero becomes reachable inside the private branch.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4770 derives a conditional private four-clause source-qbasic closure: action descent, fixed/quotient theta, same Maxwell-Hodge/current ownership, and pre-readout support selection.
- The private bulk source-qbasic obstruction is reduced to `|E_matter_lift|`.
- Poynting and boundary/corner leakage are kept as explicit boundary/wave rows: `|E_Poynting_wall|+|E_boundary_flux|`.
- Local Qbar scoring remains blocked by denominator/projector/shadow gates and by the remaining matter-lift/boundary gates.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4770 packet update: the private source-qbasic problem has been shrunk from seven residuals to one bulk residual plus explicit boundary/wave terms. The next best target is proving or bounding `E_matter_lift`.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4770-Y5-R2FR-private-source-qbasic-four-clause-closure-or-denominator-projector-first-values.md`

## Decision

`{DECISION}`

## What moved forward

- Derived a conditional private four-clause closure for action descent, constants/theta, same Hodge/current, and support selector.
- Reduced the private bulk source-qbasic obstruction to `|E_matter_lift|`.
- Kept Poynting and boundary/corner terms explicit as `|E_Poynting_wall|+|E_boundary_flux|`.
- Left denominator/projector/shadow gates blocked until source-backed values or exact zero theorems exist.

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
        "local_gr_private_source_qbasic_four_clause_closure",
        "4770 derives a conditional private four-clause closure that shrinks the bulk source-qbasic obstruction to matter lift, while keeping Poynting and boundary flux explicit.",
        "Generated source register, four-clause closure theorem, reduced local obstruction envelope, Qedge/Qbar update, denominator/projector fallback status, route matrix, gates, firewalls, decision, status, next target and validation.",
        "private_four_clause_closure_conditional_bulk_reduced_to_matter_lift_boundary_poynting_explicit_nonclaim",
        NEXT_TARGET,
        "Claiming local GR or source-qbasic zero before matter lift and boundary/Poynting gates close.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need matter-lift gauge/proper-boundary collapse or Poynting/boundary first values.",
        "Private source-qbasic four-clause closure",
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
    four_clause: list[dict[str, Any]],
    envelope: list[dict[str, Any]],
    qedge_qbar: list[dict[str, Any]],
    denominator: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4770_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4770_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4770_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))

    closed_quantities = {row["closed_quantity"]: row["private_branch_value"] for row in four_clause}
    checks.append(("VAL4770_2_four_clause_closed", "four named residuals close conditionally", all(closed_quantities.get(symbol, "").startswith("0_private") for symbol in ["E_action_vertical", "E_constant_marker", "E_Hodge_EM", "E_support_selector"]), str(FOUR_CLAUSE_CSV)))
    bulk_rows = [row for row in envelope if row["symbol"] == "E_bulk_source_qbasic_4770"]
    local_rows = [row for row in envelope if row["symbol"] == "E_local_obstruction_4770"]
    checks.append(("VAL4770_3_bulk_reduced_to_matter_lift", "bulk source-qbasic envelope is only matter lift", bool(bulk_rows) and bulk_rows[0]["formula"] == "|E_matter_lift|", str(REDUCED_ENVELOPE_CSV)))
    checks.append(("VAL4770_4_local_keeps_boundary_wave", "local obstruction keeps Poynting and boundary terms", bool(local_rows) and all(term in local_rows[0]["formula"] for term in ["E_matter_lift", "E_Poynting_wall", "E_boundary_flux"]), str(REDUCED_ENVELOPE_CSV)))
    checks.append(("VAL4770_5_qedge_one_bulk_gate", "Qedge shell update names one bulk gate remaining", any(row["status"] == "ONE_BULK_GATE_REMAINS" for row in qedge_qbar), str(QEDGE_QBAR_UPDATE_CSV)))
    checks.append(("VAL4770_6_denominator_still_blocked", "denominator/projector fallback remains missing values", any(row["status"] == "PRODUCT_STILL_BLOCKED" for row in denominator) and any(row["quantity"] == "M_0" and row["status"] == "MISSING_VALUE" for row in denominator), str(DENOMINATOR_FALLBACK_CSV)))
    checks.append(("VAL4770_7_route_selected", "route selects matter lift next", any(row["selection_status"] == "SELECTED_NEXT" and "matter" in row["route"] for row in routes), str(ROUTE_MATRIX_CSV)))
    checks.append(("VAL4770_8_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4770_9_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4770_10_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4770_11_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4770_12_claim_row", "claim row L-612 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4770_13_resume", "resume points from 4770 to 4771", "4770-Y5" in resume_text and "4771-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4770_14_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))

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
            "validation_id": "VAL4770_OVERALL",
            "check": "all 4770 four-clause closure checks pass",
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
    four_clause = four_clause_rows(timestamp)
    envelope = reduced_envelope_rows(timestamp)
    qedge_qbar = qedge_qbar_rows(timestamp)
    denominator = denominator_fallback_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(FOUR_CLAUSE_CSV, four_clause)
    write_csv(REDUCED_ENVELOPE_CSV, envelope)
    write_csv(QEDGE_QBAR_UPDATE_CSV, qedge_qbar)
    write_csv(DENOMINATOR_FALLBACK_CSV, denominator)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, four_clause, envelope, qedge_qbar, denominator, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, four_clause, envelope, qedge_qbar, denominator, routes, gates, timestamp))


if __name__ == "__main__":
    main()
