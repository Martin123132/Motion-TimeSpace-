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

CHECKPOINT = "4761"
CLAIM_ID = "L-603"
MARKER = "PPC4161_SAME_BRANCH_MEMORY_EXTREMUM_SIGNATURE_OR_BODY_CHARGE_FIRST_FILL_4761"
PACKET_MARKER = "PPC4161_PACKET_SAME_BRANCH_MEMORY_EXTREMUM_SIGNATURE_OR_BODY_CHARGE_FIRST_FILL_4761"
DECISION = "MEMORY_EXTREMUM_SIGNATURE_ASSEMBLED_BUT_BJQZM_NOT_PARENT_SIGNED_BODY_CHARGE_FIRST_FILL_SPLIT_TO_QBARXT_OR_QBARXH_NONCLAIM"
NEXT_TARGET = "4762-Y5-R2FR-qbarXT-same-branch-zero-or-QbarXH-first-source-row.md"

DOC_PATH = POST / "4761-Y5-R2FR-same-branch-memory-extremum-signature-or-body-charge-first-fill.md"
FORMAL_PATH = FORMAL / "777-PPC4161-same-branch-memory-extremum-signature-or-body-charge-first-fill.md"
CLAIMS_PATH = FORMAL / "02-claims-register.csv"
SPINE_PATH = FORMAL / "07-unification-spine.md"
PACKET_PATH = FORMAL / "180-PPC4161-private-local-packet-integration.md"
RESUME_PATH = POST / "CURRENT_LOCAL_RESUME.md"

SOURCE_REGISTER_CSV = SOURCE_DIR / "P8_Y5_R2FR_4761_SOURCE_REGISTER.csv"
MEMORY_SIGNATURE_CSV = SOURCE_DIR / "P8_Y5_R2FR_4761_MEMORY_EXTREMUM_SIGNATURE_AUDIT.csv"
ZERO_ASSEMBLY_CSV = SOURCE_DIR / "P8_Y5_R2FR_4761_SAME_BRANCH_ZERO_ASSEMBLY.csv"
FIRST_FILL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4761_BODY_CHARGE_FIRST_FILL_SELECTOR.csv"
PRODUCT_ROWS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4761_INVARIANT_PRODUCT_ROWS.csv"
ROUTE_MATRIX_CSV = SOURCE_DIR / "P8_Y5_R2FR_4761_ROUTE_SELECTION_MATRIX.csv"
PROMOTION_GATES_CSV = SOURCE_DIR / "P8_Y5_R2FR_4761_PROMOTION_GATES.csv"
FIREWALL_CSV = SOURCE_DIR / "P8_Y5_R2FR_4761_FIREWALL_ROWS.csv"
DECISION_CSV = SOURCE_DIR / "P8_Y5_R2FR_4761_DECISION.csv"
STATUS_CSV = SOURCE_DIR / "P8_Y5_R2FR_4761_STATUS.csv"
NEXT_TARGET_CSV = SOURCE_DIR / "P8_Y5_R2FR_4761_NEXT_TARGET.csv"
VALIDATION_CSV = SOURCE_DIR / "P8_Y5_BRR545_4761_VALIDATION.csv"

SOURCE_SPECS = [
    ("SRC4761_0_4760_decision", SOURCE_DIR / "P8_Y5_R2FR_4760_DECISION.csv", "PARENT_SCALE_LAW_UNSIGNED_CGAMMA_E00_PROFILE_REDUCED_TO_MEMORY_EXTREMUM", "4760 handoff decision"),
    ("SRC4761_1_4760_body", SOURCE_DIR / "P8_Y5_R2FR_4760_BODY_CHARGE_INTERFACE_ROLLUP.csv", "BC4760_1_exact_zero_requirements", "4760 body-charge exact-zero requirement"),
    ("SRC4761_2_4656_memory_theorem", SOURCE_DIR / "P8_Y5_R2FR_4656_PARENT_MEMORY_EXTREMUM_THEOREM.csv", "PME4656_3_full_zero_bundle", "memory extremum theorem and full-zero bundle"),
    ("SRC4761_3_4656_nohair", SOURCE_DIR / "P8_Y5_R2FR_4656_POSITIVE_OPERATOR_NOHAIR_ROWS.csv", "NOH4656_4_finite_green_bound", "positive-operator/no-hair and finite bound"),
    ("SRC4761_4_4656_bounds", SOURCE_DIR / "P8_Y5_R2FR_4656_CMEM_SOURCE_BOUND_ROWS.csv", "CSB4656_6_source_test", "Cmem/source-test bound rows"),
    ("SRC4761_5_4668_reduction", SOURCE_DIR / "P8_Y5_R2FR_4668_DECISION.csv", "CMEM_FINAL_ZERO_INSERTED_BODY_CHARGE_REDUCED_TO_BJQ_ZM_SOURCE_CHARGE_GATE", "Cmem reduction to BJQZM gate"),
    ("SRC4761_6_4669_zero_attempt", SOURCE_DIR / "P8_Y5_R2FR_4669_BJQ_ZM_ZERO_ATTEMPT_MATRIX.csv", "ZAT4669_13_total", "BJQZM zero attempt matrix"),
    ("SRC4761_7_4669_contract", SOURCE_DIR / "P8_Y5_R2FR_4669_FIRST_BODY_CHARGE_SOURCE_ROW_CONTRACT.csv", "FBC4669_8_claim", "first body-charge source row contract"),
    ("SRC4761_8_4669_vector", SOURCE_DIR / "P8_Y5_R2FR_4669_REMAINING_SOURCE_NORMALIZATION_VECTOR.csv", "RSN4669_0_master", "remaining source-normalization vector"),
    ("SRC4761_9_4691_product_theorem", SOURCE_DIR / "P8_Y5_R2FR_4691_INVARIANT_PRODUCT_THEOREM.csv", "IP4691_4_product_zero_or_bound", "invariant source-test product theorem"),
    ("SRC4761_10_4691_product_rows", SOURCE_DIR / "P8_Y5_R2FR_4691_IXST_PRODUCT_BOUND_ROWS.csv", "IX4691_1_absolute_product_bound", "absolute invariant product bound row"),
    ("SRC4761_11_4691_qbarxt", SOURCE_DIR / "P8_Y5_R2FR_4691_QBARXT_FACTOR_ROWS.csv", "QT4691_4_total_guard", "qbarXT test response factor rows"),
    ("SRC4761_12_4692_qbarxh", SOURCE_DIR / "P8_Y5_R2FR_4692_QBARXH_FIRST_FILL_ROWS.csv", "QF4692_1_absolute_Qbar_bound", "QbarXH first-fill source row"),
    ("SRC4761_13_4700_qbarxt", SOURCE_DIR / "P8_Y5_R2FR_4700_QBARXT_RESPONSE_ENVELOPE_THEOREM.csv", "qbar_XT", "qbarXT response envelope theorem"),
    ("SRC4761_14_4705_composite", SOURCE_DIR / "P8_Y5_R2FR_4705_COMPOSITE_EM_RESIDUAL_LAW.csv", "LAW4705_3_composed_memory_F2_bound", "deduped EM residual law"),
]

GENERATED_CSVS = [
    SOURCE_REGISTER_CSV,
    MEMORY_SIGNATURE_CSV,
    ZERO_ASSEMBLY_CSV,
    FIRST_FILL_CSV,
    PRODUCT_ROWS_CSV,
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


def memory_signature_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "MS4761_0_parent_quadratic_action",
            "S_mem^(2)=1/2 int[Z_mem |grad delta_m|^2+M_mem^2 delta_m^2]-int rho_mem delta_m + boundary",
            "Same parent action must own operator, source and boundary class.",
            "CONDITIONAL_IMPORTED",
            "not parent-signed as one global branch",
        ),
        (
            "MS4761_1_extremum_no_source_slot",
            "A_m(q,z)=A_m(q,-z) or no source-only A_m slot => partial_z ln A_m|0=0",
            "This is the elegant route: the memory source disappears by symmetry/object language, not tuning.",
            "CONDITIONAL_UNSIGNED",
            "full I_q/even-A_m/no-slot signatures not found together",
        ),
        (
            "MS4761_2_positive_operator",
            "Z_mem>=Z_min>0 and M2_mem>=M_min^2>0 with zero modes removed",
            "Coercive memory operator gives no-hair once rho_mem and boundary charge vanish.",
            "VALUES_OR_PARENT_HESSIAN_MISSING",
            "positive operator theorem exists but claim-grade Z/M or constraint elimination is missing",
        ),
        (
            "MS4761_3_Cmem_final",
            "C_mem^final_live=0 on the strict private q-basic/Hodge/worldtube/readout branch",
            "The matter-trace leg is the strongest closed piece; it really does reduce rho_mem.",
            "PRIVATE_ZERO_IMPORTED",
            "same-branch parent promotion remains nonclaim",
        ),
        (
            "MS4761_4_Bmem_eff",
            "B_mem_eff=abs(B826)+abs(BWeyl)+abs(BY5)+abs(BY6)+abs(Bsrc_boundary)+abs(Bsrc_readout)",
            "Curvature/source-normalization memory source is not killed by Cmem closure.",
            "ZERO_ATTEMPT_FAILS_CURRENT_SIGNATURE",
            "componentwise no-source/root-lock clauses remain unsigned",
        ),
        (
            "MS4761_5_Jmem_live",
            "J_mem_live=abs(J_EM_open)+abs(J_nonHilbert)+abs(J_dyn_exchange)+abs(J_boundary_readout)",
            "Poynting is handled once, but non-Hilbert/dynamic/boundary-readout currents remain live unless signed.",
            "ZERO_ATTEMPT_FAILS_CURRENT_SIGNATURE",
            "same-Hodge EM helps but does not close all J channels",
        ),
        (
            "MS4761_6_Qboundary_mem",
            "Q_boundary_mem=0 only under fixed no-flux/topological boundary class with no linked source-normalization boundary charge",
            "Boundary charge is separate from the already-closed Cmem boundary term.",
            "ZERO_ATTEMPT_FAILS_CURRENT_SIGNATURE",
            "Green-function boundary charge needs theorem-zero or finite integral",
        ),
        (
            "MS4761_7_total",
            "rho_mem=0 -> delta_m=0 -> P Gamma_mem=0 -> E_Gamma=0",
            "This is a valid theorem only if MS4761_0..6 are signed in the same branch.",
            "THEOREM_CONTRACT_ASSEMBLED_CLAIM_BLOCKED",
            "B/J/Q/ZM remain unsatisfied",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "signature_id": signature_id,
            "condition_or_formula": formula,
            "meaning": meaning,
            "status": status,
            "blocker": blocker,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for signature_id, formula, meaning, status, blocker in specs
    ]


def zero_assembly_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ZA4761_0_reduced_source", "rho_mem=B_mem_eff R_obs+J_mem_live after Cmem closure", "true only inside strict private branch", "REDUCED_BUT_NOT_ZERO"),
        ("ZA4761_1_exact_source_zero", "B_mem_eff=0 and J_mem_live=0 and Q_boundary_mem=0", "not parent-signed; no cancellation allowed", "CLAIM_BLOCKED"),
        ("ZA4761_2_operator_nohair", "rho_mem=0 and positive L_mem with silent boundary => delta_m=0", "conditional theorem stands", "EXACT_IF_INPUTS_SIGNED"),
        ("ZA4761_3_profile_silence", "delta_m=0 => ||P_00 Gamma_mem||=0 => E_Gamma=0", "profile product zero is legitimate only downstream of source/operator closure", "EXACT_IF_INPUTS_SIGNED"),
        ("ZA4761_4_public_state", "E_Gamma remains finite-bound row", "current public route must use invariant product/body-charge score interface", "NONCLAIM_BOUND_ROUTE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "assembly_id": assembly_id,
            "step": step,
            "same_branch_requirement": requirement,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for assembly_id, step, requirement, status in specs
    ]


def first_fill_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        (
            "FF4761_0_qbarXT_zero",
            "qbar_XT",
            "prove qbar_XT=0 for ordinary visible test bodies in the same parent branch",
            "qbar_XT=0 => I_mem^ST=0 even if source-side Qbar_XH is not numerically filled",
            "SELECTED_DERIVATION_FIRST",
            "observed coframe descent + matter/EM marker constants + no hidden/non-Hilbert/support/readout tail",
        ),
        (
            "FF4761_1_QbarXH_abs",
            "Qbar_XH_abs",
            "|Qbar_XH| <= (||Pi_M||(|Q_bulk|+|Q_edge|+|Q_shadow|)+|E_PiM_comm|)/M_lower",
            "best source-side fallback if qbar_XT zero fails",
            "SELECTED_EMPIRICAL_FALLBACK",
            "M_lower, Pi_M norm, Q_bulk/Q_edge/Q_shadow, commutator and source paths",
        ),
        (
            "FF4761_2_Zmem_M2mem",
            "Z_mem,M2_mem,lambda_mem",
            "lambda_mem=sqrt(Z_mem/M2_mem)",
            "required for any finite nonzero product score; exact zero can bypass numeric range only if a factor is zero",
            "REQUIRED_FOR_FINITE_SCORE",
            "positive parent Hessian or sourced range/normalization convention",
        ),
        (
            "FF4761_3_BJQ_components",
            "B_mem_eff,J_mem_live,Q_boundary_mem",
            "epsilon_BJQZM=|B|_profile+|J|_profile+|Q_boundary|/(4*pi|Z|)+epsilon_ZM+epsilon_charge",
            "source-side memory amplitude first-fill family if exact source zero is rejected",
            "SOURCE_SIDE_QUEUE",
            "componentwise theorem-zero or source-backed norms",
        ),
        (
            "FF4761_4_R10_insert",
            "alpha_R10(lambda_mem)",
            "|alpha_R10| <= |K_mem| |Qbar_XH|_abs |qbar_XT|_abs |tau_R10| + |alpha_tail_abs|",
            "do not run as a claim until product factors and range are filled",
            "DEFERRED_UNTIL_PRODUCT_READY",
            "full curve plus parent-owned prediction rows",
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "fill_id": fill_id,
            "quantity": quantity,
            "formula_or_task": formula,
            "why_this_moves_work": why,
            "selection_status": status,
            "required_inputs": inputs,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for fill_id, quantity, formula, why, status, inputs in specs
    ]


def product_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("IP4761_0_product_definition", "I_mem^ST(lambda_mem)=Qbar_mem,H qbar_mem,T/(4*pi Z_mem G_N M_H_ref m_T)", "dimensionless", "DERIVED_CONDITIONAL"),
        ("IP4761_1_zero_gate", "Qbar_mem,H=0 or qbar_mem,T=0 => I_mem^ST=0", "dimensionless", "EXACT_IF_SAME_BRANCH"),
        ("IP4761_2_abs_bound", "|I_mem^ST| <= |Qbar_mem,H|_abs |qbar_mem,T|_abs/(4*pi |Z_mem| G_N M_H_ref m_T)", "dimensionless", "BOUND_LAW_DERIVED_VALUES_MISSING"),
        ("IP4761_3_EGamma_insert", "|E_Gamma| <= |J_00^Gamma c_Gamma| A_mem + |tensor_perp|, with A_mem sourced by I_mem^ST/profile rows", "E00_profile_units", "PROFILE_INSERT_READY_NONCLAIM"),
        ("IP4761_4_no_G_absorption", "do not absorb I_mem^ST or E_Gamma into fitted G_N/GM", "control", "GUARD_ACTIVE"),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "product_id": product_id,
            "formula": formula,
            "units": units,
            "status": status,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for product_id, formula, units, status in specs
    ]


def route_rows(timestamp: str) -> list[dict[str, Any]]:
    specs = [
        ("ROUTE4761_0_memory_extremum", "same-branch memory extremum signature", "best clean derivation but currently blocked by B/J/Q/ZM and Z/M signatures", "ATTEMPTED_NOT_CLOSED"),
        ("ROUTE4761_1_qbarXT_zero", "derive qbar_XT=0 for ordinary visible test response", "can kill invariant product without source-side modelling; still derivation-first", "SELECTED_NEXT"),
        ("ROUTE4761_2_QbarXH_first_fill", "fill Qbar_XH_abs source row", "source-side empirical fallback if qbarXT does not close", "PARALLEL_FALLBACK"),
        ("ROUTE4761_3_R10_score", "score alpha_R10(lambda)", "deferred until product factors/range are source-backed", "DEFERRED"),
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
        ("PG4761_0_same_branch", "Memory extremum, Cmem zero, BJQ zero, Z/M positivity, qbar/Qbar zero and boundary silence must be signed in the same parent branch.", "blocks stitched-zero proof"),
        ("PG4761_1_no_product_claim", "Invariant product rows are nonclaim until source/test factors and range are numeric/source-backed or parent-zero.", "blocks amplitude overclaim"),
        ("PG4761_2_no_G_absorption", "Do not hide residual coupling inside calibrated G_N or ephemeris GM.", "blocks post-hoc normalization"),
        ("PG4761_3_Poynting_once", "Poynting remains Hilbert EM stress once or an explicit coefficient, not a second source.", "blocks EM double counting"),
        ("PG4761_4_exact_zero_bypass", "Exact qbarXT or QbarXH zero may bypass numeric product scoring only with parent-signed branch identity.", "blocks shortcut zero"),
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
        ("FW4761_0_no_local_gr_claim", "No local-GR/Newton/PPN/R10/clock/orbital pass from this checkpoint.", "NONCLAIM"),
        ("FW4761_1_memory_not_zero", "Do not state E_Gamma=0 publicly; current result is theorem contract plus finite route.", "NONCLAIM"),
        ("FW4761_2_qbar_not_zero", "qbarXT=0 is the next target, not a result of 4761.", "NONCLAIM"),
        ("FW4761_3_no_numeric_fill", "No numeric source-backed product value is introduced here.", "NONCLAIM"),
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
            "decision_id": "DEC4761_0",
            "decision": DECISION,
            "summary": "4761 assembles the memory-extremum route as a real same-branch theorem contract, then refuses the claim because B_mem_eff, J_mem_live, Q_boundary_mem and Z/M positivity are not parent-signed. It selects qbar_XT=0 as the next derivation-first body-charge route, with Qbar_XH_abs as the source-side fallback.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status_id": "STATUS4761_0",
            "state": "completed_nonclaim",
            "meaning": "The cGamma/E00 coupling problem is now a precise source-test product problem: prove a factor zero or fill the invariant product rows.",
            "next_target": NEXT_TARGET,
            "timestamp_utc": timestamp,
        }
    ]


def next_target_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "next_target": NEXT_TARGET,
            "reason": "qbar_XT=0 is the highest-leverage derivation-first route because it kills I_mem^ST without needing a source-side numeric model; Qbar_XH_abs remains the fallback first source row.",
            "route_priority": "derive_qbarXT_zero_first_then_source_fill",
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
    memory_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    fill_rows: list[dict[str, Any]],
    product_rows_data: list[dict[str, Any]],
    routes: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> None:
    doc = f"""# 4761: Same-Branch Memory Extremum Signature or Body-Charge First Fill

Generated: `{timestamp}`

Marker: `{MARKER}`

## Result

4761 tries the clean derivation first.

- The memory-extremum/no-hair route is mathematically sharp: if one parent branch signs the extremum/no-source clause, positive memory operator, source silence and boundary silence, then `rho_mem=0 -> delta_m=0 -> P Gamma_mem=0 -> E_Gamma=0`.
- The current corpus does **not** sign the whole package. `C_mem^final_live=0` is the strongest private reduction, but `B_mem_eff`, `J_mem_live`, `Q_boundary_mem` and `Z_mem/M2_mem` remain unsigned or unfilled.
- The coupling problem is therefore now a concrete invariant product problem, not a fog bank: prove `qbar_XT=0`, prove `Qbar_XH=0`, or fill the absolute product bound.
- The next best route is `qbar_XT=0` for ordinary visible test bodies, because that can kill the source-test product without source-side modelling. `Qbar_XH_abs` is the fallback source row.
- No local-GR, Newton, R10, WEP, clock, orbital or Maxwell pass is claimed here.

## Memory-Extremum Signature Audit

{markdown_table(memory_rows, ["signature_id", "condition_or_formula", "status", "blocker"])}

## Same-Branch Zero Assembly

{markdown_table(zero_rows, ["assembly_id", "step", "status"])}

## Body-Charge First-Fill Selector

{markdown_table(fill_rows, ["fill_id", "quantity", "formula_or_task", "selection_status"])}

## Invariant Product Rows

{markdown_table(product_rows_data, ["product_id", "formula", "status"])}

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

    formal = f"""# PPC4161 4761: Memory Extremum vs Body-Charge First Fill

Generated: `{timestamp}`

## Core Result

The clean local memory route is now a same-branch theorem contract:

```text
extremum/no-source + positive L_mem + B_mem=0 + J_mem=0 + Q_boundary=0
  => rho_mem=0
  => delta_m=0
  => P Gamma_mem=0
  => E_Gamma=0.
```

The theorem is valid as a contract but not claimable from the current corpus because the `B/J/Q/ZM` package is not parent-signed.

The finite route is:

```text
I_mem^ST(lambda_mem)
  = Qbar_mem,H qbar_mem,T /(4*pi Z_mem G_N M_H_ref m_T)
```

with zero branch:

```text
Qbar_mem,H=0 or qbar_mem,T=0 => I_mem^ST=0.
```

Next derivation-first target: try to prove `qbar_XT=0` for ordinary visible test bodies in the same branch; keep `Qbar_XH_abs` as the source-side fallback.

Decision: `{DECISION}`

Next: `{NEXT_TARGET}`
"""
    write_text(FORMAL_PATH, formal)


def update_spine_packet_resume(timestamp: str) -> None:
    spine_block = f"""

## {MARKER}

Generated: `{timestamp}`

- 4761 assembles the memory-extremum/no-hair route as a valid same-branch theorem contract: `rho_mem=0 -> delta_m=0 -> P Gamma_mem=0 -> E_Gamma=0`.
- It refuses promotion because `B_mem_eff`, `J_mem_live`, `Q_boundary_mem` and `Z_mem/M2_mem` are not parent-signed together.
- The coupling problem is reduced to the invariant source-test product `I_mem^ST=Qbar_mem,H qbar_mem,T/(4*pi Z_mem G_N M_H_ref m_T)`.
- Best next derivation route: prove `qbar_XT=0` for ordinary visible test bodies; source-side fallback: fill `Qbar_XH_abs`.
- Decision: `{DECISION}`.
"""
    append_once(SPINE_PATH, MARKER, spine_block)

    packet_block = f"""

## {PACKET_MARKER}

Generated: `{timestamp}`

4761 packet update: stop treating coupling as vague. The memory profile is zero only under one signed branch; otherwise score the invariant product. Next target is `qbar_XT=0` first, `Qbar_XH_abs` second.

Next: `{NEXT_TARGET}`.
"""
    append_once(PACKET_PATH, PACKET_MARKER, packet_block)

    resume = f"""# Current Local Resume

Updated: `{timestamp}`

## Latest completed checkpoint

`4761-Y5-R2FR-same-branch-memory-extremum-signature-or-body-charge-first-fill.md`

## Decision

`{DECISION}`

## What moved forward

- Assembled the same-branch memory-extremum/no-hair theorem contract for `E_Gamma=0`.
- Refused the claim because `B_mem_eff`, `J_mem_live`, `Q_boundary_mem` and `Z_mem/M2_mem` are not parent-signed together.
- Reduced the remaining coupling/profile problem to the invariant product `I_mem^ST`.
- Selected the next derivation-first target: prove `qbar_XT=0`, with `Qbar_XH_abs` as fallback source row.

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
        "local_gr_memory_coupling_product_gate",
        "4761 assembles the same-branch memory-extremum theorem contract and reduces the finite route to qbarXT/QbarXH invariant product rows.",
        "Generated source register, memory signature audit, same-branch assembly, body-charge first-fill selector, invariant product rows, route matrix, gates, firewalls, decision, status, next target and validation.",
        "memory_extremum_signature_assembled_BJQZM_unsigned_body_charge_product_nonclaim",
        NEXT_TARGET,
        "Claiming E_Gamma=0 without same-branch B/J/Q/ZM and operator positivity signatures.",
        "local_gr",
        str(DOC_PATH),
        NEXT_TARGET,
        "Need qbarXT same-branch zero or QbarXH source row plus product/range fill.",
        "Same-branch memory extremum signature or body-charge first fill",
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
    memory_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    fill_rows: list[dict[str, Any]],
    product_rows_data: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    timestamp: str,
) -> list[dict[str, Any]]:
    checks: list[tuple[str, str, bool, str]] = []
    checks.append(("VAL4761_0_sources_exist", "all cited source paths exist", all(row["exists"] for row in sources), str(SOURCE_REGISTER_CSV)))
    checks.append(("VAL4761_1_needles_found", "all source needles found", all(row["needle_found"] for row in sources), str(SOURCE_REGISTER_CSV)))
    for csv_path in GENERATED_CSVS:
        checks.append((f"VAL4761_csv_{csv_path.stem}", f"{csv_path.name} parses", csv_path.exists() and parse_csv(csv_path), str(csv_path)))
    checks.append(("VAL4761_2_memory_blockers", "memory audit keeps B/J/Q/ZM blockers live", any(row["signature_id"] == "MS4761_4_Bmem_eff" and "FAILS" in row["status"] for row in memory_rows) and any(row["signature_id"] == "MS4761_5_Jmem_live" and "FAILS" in row["status"] for row in memory_rows) and any(row["signature_id"] == "MS4761_6_Qboundary_mem" and "FAILS" in row["status"] for row in memory_rows) and any(row["signature_id"] == "MS4761_2_positive_operator" and "MISSING" in row["status"] for row in memory_rows), str(MEMORY_SIGNATURE_CSV)))
    checks.append(("VAL4761_3_zero_claim_blocked", "same-branch zero assembly blocks public E_Gamma zero", any(row["status"] == "CLAIM_BLOCKED" for row in zero_rows) and any(row["status"] == "NONCLAIM_BOUND_ROUTE" for row in zero_rows), str(ZERO_ASSEMBLY_CSV)))
    checks.append(("VAL4761_4_first_fill_selected", "first-fill selector chooses qbarXT derivation and QbarXH fallback", any(row["quantity"] == "qbar_XT" and row["selection_status"] == "SELECTED_DERIVATION_FIRST" for row in fill_rows) and any(row["quantity"] == "Qbar_XH_abs" and row["selection_status"] == "SELECTED_EMPIRICAL_FALLBACK" for row in fill_rows), str(FIRST_FILL_CSV)))
    checks.append(("VAL4761_5_product_gate", "invariant product rows include zero gate and absolute bound", any("Qbar_mem,H=0 or qbar_mem,T=0" in row["formula"] for row in product_rows_data) and any("|I_mem^ST|" in row["formula"] for row in product_rows_data), str(PRODUCT_ROWS_CSV)))
    checks.append(("VAL4761_6_gates_nonclaim", "promotion gates keep claims closed", all(row["claim_allowed"] is False for row in gates), str(PROMOTION_GATES_CSV)))
    checks.append(("VAL4761_7_docs_exist", "post and formal docs exist", DOC_PATH.exists() and FORMAL_PATH.exists(), f"{DOC_PATH}; {FORMAL_PATH}"))
    checks.append(("VAL4761_8_spine_marker", "spine marker appended", MARKER in read_text(SPINE_PATH), str(SPINE_PATH)))
    checks.append(("VAL4761_9_packet_marker", "packet marker appended", PACKET_MARKER in read_text(PACKET_PATH), str(PACKET_PATH)))
    checks.append(("VAL4761_10_claim_row", "claim row L-603 present", CLAIM_ID in read_text(CLAIMS_PATH), str(CLAIMS_PATH)))
    resume_text = read_text(RESUME_PATH)
    checks.append(("VAL4761_11_resume", "resume points from 4761 to 4762", "4761-Y5" in resume_text and "4762-Y5" in resume_text, str(RESUME_PATH)))
    checks.append(("VAL4761_12_pycache_absent", "scripts __pycache__ removed", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts")))
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
            "validation_id": "VAL4761_OVERALL",
            "check": "all 4761 memory-extremum/body-charge selector checks pass",
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
    memory_rows = memory_signature_rows(timestamp)
    zero_rows = zero_assembly_rows(timestamp)
    fill_rows = first_fill_rows(timestamp)
    product_rows_data = product_rows(timestamp)
    routes = route_rows(timestamp)
    gates = promotion_gate_rows(timestamp)
    firewalls = firewall_rows(timestamp)
    decisions = decision_rows(timestamp)
    statuses = status_rows(timestamp)
    next_targets = next_target_rows(timestamp)

    write_csv(SOURCE_REGISTER_CSV, sources)
    write_csv(MEMORY_SIGNATURE_CSV, memory_rows)
    write_csv(ZERO_ASSEMBLY_CSV, zero_rows)
    write_csv(FIRST_FILL_CSV, fill_rows)
    write_csv(PRODUCT_ROWS_CSV, product_rows_data)
    write_csv(ROUTE_MATRIX_CSV, routes)
    write_csv(PROMOTION_GATES_CSV, gates)
    write_csv(FIREWALL_CSV, firewalls)
    write_csv(DECISION_CSV, decisions)
    write_csv(STATUS_CSV, statuses)
    write_csv(NEXT_TARGET_CSV, next_targets)
    write_docs(timestamp, memory_rows, zero_rows, fill_rows, product_rows_data, routes, gates)
    update_spine_packet_resume(timestamp)
    add_claim_once(timestamp)
    cleanup_pycache()
    write_csv(VALIDATION_CSV, validation_rows(sources, memory_rows, zero_rows, fill_rows, product_rows_data, gates, timestamp))


if __name__ == "__main__":
    main()
