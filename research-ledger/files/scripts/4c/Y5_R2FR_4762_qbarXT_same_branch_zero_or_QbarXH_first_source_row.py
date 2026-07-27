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

CHECKPOINT = "4762"
CLAIM_ID = "L-604"
MARKER = "PPC4161_QBARXT_SAME_BRANCH_ZERO_OR_QBARXH_FIRST_SOURCE_ROW_4762"
PACKET_MARKER = "PPC4161_PACKET_QBARXT_SAME_BRANCH_ZERO_OR_QBARXH_FIRST_SOURCE_ROW_4762"
DECISION = "QBARXT_ZERO_CONTRACT_ASSEMBLED_BUT_EM_F2_MARKER_HIDDEN_SUPPORT_TAILS_UNSIGNED_QBARXH_ABS_SOURCE_ROW_STAGED_NONCLAIM"
NEXT_TARGET = "4763-Y5-R2FR-QbarXH-source-numerator-first-fill-or-qbarXT-hard-blocker.md"

DOC_PATH = POST / "4762-Y5-R2FR-qbarXT-same-branch-zero-or-QbarXH-first-source-row.md"
FORMAL_PATH = FORMAL / "778-PPC4161-qbarXT-same-branch-zero-or-QbarXH-first-source-row.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4762_SOURCE_REGISTER.csv"
QBARXT_THEOREM_CSV = SOURCE_DIR / "P8_Y5_R2FR_4762_QBARXT_ZERO_THEOREM_ROWS.csv"
QBARXT_AUDIT_CSV = SOURCE_DIR / "P8_Y5_R2FR_4762_QBARXT_COMPONENT_AUDIT.csv"
QBARXH_SOURCE_ROW_CSV = SOURCE_DIR / "P8_Y5_R2FR_4762_QBARXH_FIRST_SOURCE_ROW.csv"
PRODUCT_UPDATE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4762_PRODUCT_GATE_UPDATE.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4762_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4762_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4762_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4762_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4762_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4762_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4762_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4762_0_4761_decision", SOURCE_DIR / "P8_Y5_R2FR_4761_DECISION.csv", "MEMORY_EXTREMUM_SIGNATURE_ASSEMBLED_BUT_BJQZM_NOT_PARENT_SIGNED", "4761 handoff decision"),
    ("SRC4762_1_4761_fill", SOURCE_DIR / "P8_Y5_R2FR_4761_BODY_CHARGE_FIRST_FILL_SELECTOR.csv", "FF4761_0_qbarXT_zero", "4761 selected qbarXT zero route"),
    ("SRC4762_2_4761_product", SOURCE_DIR / "P8_Y5_R2FR_4761_INVARIANT_PRODUCT_ROWS.csv", "IP4761_1_zero_gate", "4761 product zero gate"),
    ("SRC4762_3_4691_qbarxt", SOURCE_DIR / "P8_Y5_R2FR_4691_QBARXT_FACTOR_ROWS.csv", "QT4691_4_total_guard", "qbarXT factor envelope"),
    ("SRC4762_4_4700_theorem", SOURCE_DIR / "P8_Y5_R2FR_4700_QBARXT_RESPONSE_ENVELOPE_THEOREM.csv", "QXT4700_0_variational_definition", "qbarXT variational definition"),
    ("SRC4762_5_4700_queue", SOURCE_DIR / "P8_Y5_R2FR_4700_FIRST_SOURCE_BACKED_PRIORITY_QUEUE.csv", "qbar_constants, qbar_marker, s_alpha b_alpha", "qbarXT priority queue"),
    ("SRC4762_6_4701_theta", SOURCE_DIR / "P8_Y5_R2FR_4701_THETA_MARKER_DESCENT_THEOREM.csv", "TMD4701_1_qbasic_constant_zero", "theta/marker descent theorem"),
    ("SRC4762_7_4701_coeffs", SOURCE_DIR / "P8_Y5_R2FR_4701_QBARXT_COEFFICIENT_ROWS_NONCLAIM.csv", "QTC4701_7_qbar_theta_marker_abs", "theta/marker coefficient rows"),
    ("SRC4762_8_4702_em", SOURCE_DIR / "P8_Y5_R2FR_4702_EM_GAUGE_KINETIC_THEOREM.csv", "EGK4702_1_zero_contract", "EM alpha/gauge kinetic zero contract"),
    ("SRC4762_9_4703_f2", SOURCE_DIR / "P8_Y5_R2FR_4703_NO_EXTRA_F2_THEOREM.csv", "NEF4703_4_current_verdict", "no-extra-F2 verdict"),
    ("SRC4762_10_4704_image", SOURCE_DIR / "P8_Y5_R2FR_4704_VISIBLE_IMAGE_PROOF_ATTEMPT.csv", "VIP4704_3_reduced_exact_bottleneck", "visible image/no-Hom bottleneck"),
    ("SRC4762_11_4692_qbarxh", SOURCE_DIR / "P8_Y5_R2FR_4692_QBARXH_FIRST_FILL_ROWS.csv", "QF4692_1_absolute_Qbar_bound", "QbarXH absolute first source row"),
    ("SRC4762_12_4693_num", SOURCE_DIR / "P8_Y5_R2FR_4693_SOURCE_NUMERATOR_THEOREM.csv", "NUM4693_4_absolute_numerator_bound", "QbarXH source numerator theorem"),
    ("SRC4762_13_4693_qbulk", SOURCE_DIR / "P8_Y5_R2FR_4693_QBULK_COMPONENT_ROWS.csv", "QB4693_1_EM_Poynting", "Qbulk EM/Poynting component"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    QBARXT_THEOREM_CSV,
    QBARXT_AUDIT_CSV,
    QBARXH_SOURCE_ROW_CSV,
    PRODUCT_UPDATE_CSV,
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


def qbarxt_theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QXT4762_0_definition",
            "qbar_XT := M_T^-1 |delta_{v_X} S_T|",
            "Test-body response is a variational derivative along the vertical parent direction, not a fitted amplitude.",
            "DEFINITION_IMPORTED",
        ),
        (
            "QXT4762_1_chain_rule_zero",
            "If S_T=Sbar[psi,e_obs(q),theta(q),W(q),D(q)] and v_X in ker(Dq), then delta_{v_X}S_T=0.",
            "The desired zero is a chain-rule theorem when geometry, constants, support and domain all factor through q before variation.",
            "EXACT_CONDITIONAL_THEOREM",
        ),
        (
            "QXT4762_2_total_bound",
            "|qbar_XT| <= |qbar_geom|+|qbar_theta_marker|+|qbar_EM|+|qbar_nonH|+|qbar_support|+|qbar_boundary|+|qbar_domain|+|qbar_readout|",
            "If any chain-rule clause is unsigned, qbarXT stays as an absolute no-cancellation envelope.",
            "BOUND_FORM_DERIVED_VALUES_MISSING",
        ),
        (
            "QXT4762_3_product_zero",
            "qbar_XT=0 => I_mem^ST=0 for ordinary visible test bodies in the same branch.",
            "This is why qbarXT is the high-leverage route: it can kill the finite-range source-test product without modelling the source.",
            "PAYOFF_EXACT_IF_PARENT_SIGNED",
        ),
        (
            "QXT4762_4_current_verdict",
            "Current corpus has conditional zero clauses but not one parent-signed ordinary-visible test-body branch.",
            "The theorem is assembled but not promoted.",
            "CLAIM_BLOCKED",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "theorem_id": theorem_id,
            "formula_or_statement": statement,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, statement, meaning, status in specs
    ]


def qbarxt_component_audit_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QA4762_0_geom",
            "qbar_geom",
            "Lie_v e_obs(q)=0 by quotient-owned observed coframe; Weyl/disformal slots absent.",
            "PRIVATE_CONDITIONAL_ZERO",
            "public parent functor/common observed frame still unsigned",
        ),
        (
            "QA4762_1_theta_marker",
            "qbar_theta_marker",
            "q-basic theta_obs gives D_v theta=0, but dimensionless alpha, mass ratios, clock ratios and material labels need fixed/superselected status.",
            "CONDITIONAL_ZERO_WITH_RETAINED_COEFFICIENTS",
            "b_alpha,b_mu,b_clock,b_material_label,b_source_norm rows remain nonclaim",
        ),
        (
            "QA4762_2_EM_alpha",
            "b_alpha_EM / qbar_EM",
            "b_alpha_EM=0 only if gauge object, charge lattice, generator norm, unique F2, same-current owner and readout/radiative closure are signed.",
            "HARD_BLOCKER_PARENT_UNSIGNED",
            "no-extra-F2/operator-domain image and hidden-Hom bottleneck remain",
        ),
        (
            "QA4762_3_nonHilbert_hidden",
            "qbar_nonH",
            "ordinary matter functor has no non-Hilbert source slot and hidden tails vanish.",
            "CONDITIONAL_ZERO_UNSIGNED",
            "hidden/source-shadow tail absence not globally signed",
        ),
        (
            "QA4762_4_support_boundary_domain",
            "qbar_support+qbar_boundary+qbar_domain",
            "support, boundary, projector and domain are fixed q-basic maps with compact boundary silence.",
            "CONDITIONAL_ZERO_UNSIGNED",
            "fixed support/domain/readout certificates or bounds missing",
        ),
        (
            "QA4762_5_readout",
            "qbar_readout",
            "readout is pure post-variation postprocessing with no feedback into parent source/test action.",
            "CONDITIONAL_ZERO_UNSIGNED",
            "active readout/apparatus tails remain finite rows if this is not signed",
        ),
        (
            "QA4762_6_total",
            "qbar_XT",
            "all components must vanish in the same parent branch for qbar_XT=0.",
            "ZERO_CONTRACT_ASSEMBLED_CLAIM_BLOCKED",
            "EM/F2 plus marker/hidden/support/readout clauses are not jointly parent-signed",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "audit_id": audit_id,
            "component": component,
            "zero_route": route,
            "status": status,
            "blocker": blocker,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, component, route, status, blocker in specs
    ]


def qbarxh_source_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "QXH4762_0_strict_zero",
            "Qbar_XH",
            "if Q_bulk=Q_edge=Q_shadow=0, M_H_ref>=M_lower>0, and [D_v,Pi_M]=0, then Qbar_XH=0",
            "CONDITIONAL_ZERO_NOT_PARENT_SIGNED",
            "source-current zero; edge zero; shadow zero; M_lower; Pi_M commutator zero",
        ),
        (
            "QXH4762_1_absolute_bound",
            "Qbar_XH_abs",
            "|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower",
            "FIRST_SOURCE_ROW_STAGED_VALUES_MISSING",
            "M_lower; Pi_M_op_norm; Q_bulk_abs; Q_edge_abs; Q_shadow_abs; E_PiM_comm; source paths",
        ),
        (
            "QXH4762_2_bulk",
            "Q_bulk_abs",
            "|Q_bulk|_abs <= |Q_bulk_Hilbert|+|Q_bulk_EM_Poynting|+|Q_bulk_retained|",
            "COMPONENT_BOUND_READY_VALUES_MISSING",
            "common matter action; EM/Poynting same-Hodge/no-flux; retained source tail inventory",
        ),
        (
            "QXH4762_3_edge",
            "Q_edge_abs",
            "|Q_edge|_abs <= |Q_edge_shell|+|Q_edge_boundary|",
            "COMPONENT_BOUND_READY_VALUES_MISSING",
            "boundary trace density; shell measure; Hamiltonian boundary/corner/reference edge terms",
        ),
        (
            "QXH4762_4_shadow",
            "Q_shadow_abs",
            "|Q_shadow|_abs <= |Q_shadow_action|+|Q_shadow_projector|+|Q_shadow_nonvariational|",
            "COMPONENT_BOUND_READY_VALUES_MISSING",
            "parent action classification; projector norm; nonvariational block absence or bound",
        ),
        (
            "QXH4762_5_claim_gate",
            "Qbar_XH_claim_gate",
            "valid_for_claim=true only if no MISSING inputs, M_lower>0, units declared, source paths exist and all components are zero or bounded.",
            "CLAIM_BLOCKED",
            "no numeric/source-backed component values introduced in 4762",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "source_row_id": source_row_id,
            "quantity": quantity,
            "formula": formula,
            "status": status,
            "required_inputs": inputs,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for source_row_id, quantity, formula, status, inputs in specs
    ]


def product_update_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("PU4762_0_qbarxt_zero_payoff", "qbar_XT=0 => I_mem^ST=0", "exact only after same-branch qbarXT parent signature", "NOT_CLAIMED"),
        ("PU4762_1_current_product_bound", "|I_mem^ST| <= |Qbar_XH|_abs |qbar_XT|_abs/(4*pi |Z_mem| G_N M_H_ref m_T)", "fallback absolute product score", "VALUES_MISSING"),
        ("PU4762_2_QbarXH_insert", "|Qbar_XH|_abs formula staged from 4692/4693", "source side now has a first-fill row shape", "SOURCE_ROW_STAGED"),
        ("PU4762_3_qbarXT_insert", "|qbar_XT|_abs remains component envelope", "test side not parent-zero yet", "TEST_ZERO_BLOCKED"),
        ("PU4762_4_no_G_absorption", "calibrated G_N/GM cannot absorb qbarXT or QbarXH", "normalization firewall", "ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "product_update_id": update_id,
            "formula_or_rule": formula,
            "meaning": meaning,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for update_id, formula, meaning, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4762_0_qbarXT_zero", "prove qbar_XT=0", "attempted; theorem assembled but EM/F2, marker, hidden/support/readout tails are unsigned", "ATTEMPTED_NOT_PROMOTED"),
        ("ROUTE4762_1_EM_F2_hard_blocker", "parent-sign no-extra-F2/hidden-Hom/gauge-current package", "would close the hardest qbarXT test-side component", "DERIVATION_SUBTARGET"),
        ("ROUTE4762_2_QbarXH_first_source_row", "fill Qbar_XH_abs first source row", "best fallback because qbarXT zero is not parent-signed", "SELECTED_NEXT_FALLBACK"),
        ("ROUTE4762_3_product_score", "score I_mem^ST/R10", "deferred until qbarXT or QbarXH values/zeros and range exist", "DEFERRED"),
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
        ("PG4762_0_same_branch", "qbarXT zero requires geometry, theta, EM, hidden, support, boundary, domain and readout silence in one parent branch.", "blocks component collage"),
        ("PG4762_1_alpha_not_units", "alpha_EM/mass/clock dimensionless channels cannot be erased by unit convention.", "blocks calibration shortcut"),
        ("PG4762_2_poynting_once", "Poynting is Hilbert EM stress once or explicit wall/Hodge coefficient.", "blocks EM double counting"),
        ("PG4762_3_qbarxh_values", "QbarXH source row is nonclaim until component values or theorem-zeros are supplied.", "blocks empty source-row claim"),
        ("PG4762_4_no_G_absorption", "Do not absorb finite product into calibrated G_N/GM.", "blocks post-hoc normalization"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "gate_id": gate_id,
            "rule": rule,
            "enforced_effect": effect,
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, rule, effect in specs
    ]


def firewall_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("FW4762_0_no_qbar_claim", "Do not claim qbar_XT=0 publicly from 4762.", "NONCLAIM"),
        ("FW4762_1_no_Qbar_value", "Do not claim a numeric Qbar_XH value; only the first source-row formula is staged.", "NONCLAIM"),
        ("FW4762_2_no_R10_score", "Do not run R10/local test scoring until product factors and range are filled.", "NONCLAIM"),
        ("FW4762_3_no_G_prediction", "Do not turn the calibrated common-G bridge into a numerical prediction of G_N.", "NONCLAIM"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "firewall_id": firewall_id,
            "rule": rule,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for firewall_id, rule, status in specs
    ]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "decision_id": "DEC4762_0",
            "decision": DECISION,
            "summary": "4762 assembles the qbarXT chain-rule zero theorem but refuses promotion because EM/F2, dimensionless marker, hidden/non-Hilbert, support/domain/boundary and readout tails are not jointly parent-signed. It stages the QbarXH_abs first source row as the concrete fallback.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4762_0",
            "state": "completed_nonclaim",
            "meaning": "The test-body zero route is now explicit; the next work is either close its hard blocker or fill QbarXH_abs.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "qbarXT zero is assembled but not parent-signed; move to the source-side first-fill row while preserving the qbarXT EM/F2 hard-blocker route.",
            "route_priority": "QbarXH_first_fill_with_qbarXT_hard_blocker_available",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row[column]).replace("\n", " ") for column in columns) + " |" for row in rows]
    return "\n".join([header, divider, *body])


def write_docs(
    timestamp: str,
    theorem_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
    product_rows: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4762: qbarXT Same-Branch Zero or QbarXH First Source Row

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

4762 goes after the high-leverage test-body zero route.

- The `qbar_XT=0` theorem is assembled as a real chain-rule result: if the ordinary visible test-body action descends through `q`, and all geometry/constants/EM/support/domain/readout data are q-basic before variation, then `delta_v S_T=0`.
- It is **not** promoted. The hard blockers are the dimensionless marker channels, EM/fine-structure `F^2` throat, hidden/non-Hilbert tails, and support/boundary/domain/readout certificates.
- The fallback is no longer vague: the first source-side row is `Qbar_XH_abs` with explicit `Q_bulk`, `Q_edge`, `Q_shadow`, `Pi_M`, commutator and `M_lower` inputs.
- The invariant product remains nonclaim until either `qbar_XT=0`, `Qbar_XH=0`, or both absolute factors are source-backed.
- No R10, WEP, clock, orbital, Maxwell, Newton or local-GR pass is claimed here.

## qbarXT Zero Theorem

{markdown_table(theorem_rows, ["theorem_id", "formula_or_statement", "status"])}

## qbarXT Component Audit

{markdown_table(audit_rows, ["audit_id", "component", "status", "blocker"])}

## QbarXH First Source Row

{markdown_table(source_rows, ["source_row_id", "quantity", "formula", "status"])}

## Product Gate Update

{markdown_table(product_rows, ["product_update_id", "formula_or_rule", "status"])}

## Route Selection

{markdown_table(routes, ["route_id", "route", "payoff", "selection_status"])}

## Promotion Gates

{markdown_table(gates, ["gate_id", "rule", "enforced_effect"])}

## Decision

`{DECISION}`

## Next Target

`{NEXT_TARGET}`
"""
    write_text(DOC_PATH, doc)

    formal = f"""# PPC4161 4762: qbarXT Zero or QbarXH First Source Row

Generated: `{timestamp}`

## Core Result

The test-body zero route is now explicit:

```text
S_T = Sbar[psi, e_obs(q), theta(q), W(q), D(q)]
v_X in ker(Dq)
=> delta_{{v_X}} S_T = 0
=> qbar_XT = 0
=> I_mem^ST = 0.
```

The route is not parent-signed because the current corpus still leaves:

```text
qbar_theta_marker, b_alpha_EM, no-extra-F2/hidden-Hom,
qbar_nonH, support/boundary/domain/readout tails
```

as unsigned or finite channels.

Fallback source-side row:

```text
|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)
              + |E_PiM_comm|)/M_lower.
```

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4762 assembles `qbar_XT=0` as a valid chain-rule theorem for ordinary visible test bodies when all geometry, marker, EM, support, boundary, domain and readout data descend through `q` in the same branch.
- It refuses promotion because the EM/fine-structure `F^2` throat, dimensionless marker channels, hidden/non-Hilbert tails and support/readout certificates are not jointly parent-signed.
- The fallback first source row is now explicit: `|Qbar_XH| <= (||Pi_M^H||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower`.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4762 packet update: `qbar_XT=0` is a theorem contract, not a claim. Since the test side is unsigned, move to `Qbar_XH_abs` first-fill while keeping the EM/F2 qbar hard blocker as a derivation subtarget.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4762-Y5-R2FR-qbarXT-same-branch-zero-or-QbarXH-first-source-row.md`

## Decision

`{DECISION}`

## What moved forward

- Assembled the `qbar_XT=0` chain-rule theorem for ordinary visible test bodies.
- Refused the claim because EM/F2, dimensionless marker, hidden/non-Hilbert, support/domain/boundary and readout tails are not parent-signed together.
- Staged the concrete `Qbar_XH_abs` first source row as the fallback source-side route.
- Kept the invariant product gate nonclaim until a test-side zero or source-side row is filled.

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
        "local_gr_test_response_source_product_gate",
        "4762 assembles the qbarXT chain-rule zero theorem and stages QbarXH_abs as the first source-side fallback row.",
        "Generated source register, qbarXT theorem rows, component audit, QbarXH first source row, product update, route matrix, gates, firewalls, decision, status, next target and validation.",
        "qbarXT_zero_contract_assembled_QbarXH_abs_source_row_staged_nonclaim",
        NEXT_TARGET,
        "Claiming qbarXT=0 or QbarXH numeric values without parent signature or source-backed inputs.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need QbarXH numerator first fill or qbarXT EM/F2 hard-blocker closure.",
        "qbarXT same-branch zero or QbarXH first source row",
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
    theorem_rows: list[dict[str, Any]],
    audit_rows: list[dict[str, Any]],
    source_rows: list[dict[str, Any]],
    product_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4762_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4762_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4762_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4762_2_theorem_assembled", "qbarXT theorem rows include chain rule zero and claim block", any(row["theorem_id"] == "QXT4762_1_chain_rule_zero" for row in theorem_rows) and any(row["status"] == "CLAIM_BLOCKED" for row in theorem_rows), str(QBARXT_THEOREM_CSV)))
    checks.append(("VAL4762_3_hard_blockers", "component audit keeps EM/F2 and total qbarXT blockers live", any(row["component"] == "b_alpha_EM / qbar_EM" and "HARD_BLOCKER" in row["status"] for row in audit_rows) and any(row["component"] == "qbar_XT" and "CLAIM_BLOCKED" in row["status"] for row in audit_rows), str(QBARXT_AUDIT_CSV)))
    checks.append(("VAL4762_4_qbarxh_row", "QbarXH absolute source row is staged and claim blocked", any(row["quantity"] == "Qbar_XH_abs" and "FIRST_SOURCE_ROW_STAGED" in row["status"] for row in source_rows) and any(row["quantity"] == "Qbar_XH_claim_gate" and row["status"] == "CLAIM_BLOCKED" for row in source_rows), str(QBARXH_SOURCE_ROW_CSV)))
    checks.append(("VAL4762_5_product_gate", "product update retains qbarXT zero payoff and absolute product bound", any("qbar_XT=0" in row["formula_or_rule"] for row in product_rows) and any("|I_mem^ST|" in row["formula_or_rule"] for row in product_rows), str(PRODUCT_UPDATE_CSV)))
    checks.append(("VAL4762_6_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4762_7_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4762_8_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4762_9_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4762_10_claim_row", "claim row L-604 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4762_11_resume", "resume points from 4762 to 4763", "4762-Y5" in resume_text and "4763-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4762_12_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4762_OVERALL",
            "check": "all 4762 qbarXT/QbarXH selector checks pass",
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
    theorem_rows = qbarxt_theorem_rows(timestamp)
    audit_rows = qbarxt_component_audit_rows(timestamp)
    source_rows = qbarxh_source_rows(timestamp)
    product_rows_data = product_update_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(QBARXT_THEOREM_CSV, theorem_rows)
    write_csv(QBARXT_AUDIT_CSV, audit_rows)
    write_csv(QBARXH_SOURCE_ROW_CSV, source_rows)
    write_csv(PRODUCT_UPDATE_CSV, product_rows_data)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, theorem_rows, audit_rows, source_rows, product_rows_data, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, theorem_rows, audit_rows, source_rows, product_rows_data, gates, timestamp))


if __name__ == "__main__":
    main()
