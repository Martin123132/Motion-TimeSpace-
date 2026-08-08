from __future__ import annotations

import csv
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROOT = Path(__file__).resolve().parents[2]
FORMAL = ROOT / "formalization-workbench"
POST = ROOT / "post-checkpoint-work"
SOURCE_DIR = POST / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = POST / "source-intake" / "local_bounds"

CHECKPOINT = "4363"
CLAIM_ID = "L-204"
BRANCH = "MTS_R2FR_Y5_TRANSITION_FIRST_CSRC_PROJECTION_INPUT_OR_PARENT_GRAPH_EDGE_PROOF_4363"
MARKER = "PPC4161_TRANSITION_FIRST_CSRC_PROJECTION_INPUT_OR_PARENT_GRAPH_EDGE_PROOF_4363"
PACKET_MARKER = "PPC4161_PACKET_TRANSITION_FIRST_CSRC_PROJECTION_INPUT_OR_PARENT_GRAPH_EDGE_PROOF_4363"
DECISION = "FIRST_SOURCE_BACKED_CSRC_WEP_PRODUCT_PROJECTION_ROW_DERIVED_DELTAW_AMPLITUDE_STILL_BLOCKED_NONCLAIM"
NEXT_TARGET = "4364-Y5-R2FR-transition-tau-WEP-lower-bound-or-WEP-product-only-local-route.md"

FORMAL_PATH = FORMAL / "379-PPC4161-transition-first-Csrc-projection-input-or-parent-graph-edge-proof.md"
DOC_PATH = POST / "4363-Y5-R2FR-transition-first-Csrc-projection-input-or-parent-graph-edge-proof.md"
VALIDATION_PATH = SOURCE_DIR / "P8_Y5_BRR545_4363_VALIDATION.csv"
STAMP = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

WEP_BOUND_VALUE = 2.8e-15
CSRC_ORDER = "Delta_w_component_vector; Xi_open; p_WEP_TiPt; epsilon_Gsrc_open"
PROJECTION_ROW = "0;0;1;0"


LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4363_00_4362_formal": (
        FORMAL / "378-PPC4161-transition-parent-owned-graph-signature-or-Csrc-closure-runner.md",
        "R_arena = Pi_arena^C C_src_open + Pi_arena^T T_open",
        "4362 installs the local C_src/T_open projection contract.",
    ),
    "SRC4363_01_4362_vector": (
        SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_VECTOR_BASIS.csv",
        "CSRC4362_2_tau_WEP_product",
        "4362 keeps the WEP tau-product as a C_src component.",
    ),
    "SRC4363_02_4362_arena": (
        SOURCE_DIR / "P8_Y5_R2FR_4362_CSRC_ARENA_PROJECTION_CONTRACT.csv",
        "ARENA4362_0_WEP",
        "4362 WEP arena row waiting for a projection input.",
    ),
    "SRC4363_03_4361_csrc": (
        SOURCE_DIR / "P8_Y5_R2FR_4361_CSRC_CLOSURE_ROWS.csv",
        "CSRC4361_2_WEP_product",
        "4361 product-bound closure row before tau inversion.",
    ),
    "SRC4363_04_1694_bound_anchor": (
        SOURCE_DIR / "P8_Y5_PARENT_QLOC_1694_SOURCE_BACKED_BETA_DELTAW_CURRENT_ROWS.csv",
        "BDW1694_0_MICROSCOPE_Delta_w_tau_bound_anchor",
        "Source-backed MICROSCOPE WEP product-bound anchor.",
    ),
    "SRC4363_05_local_bound_claims": (
        LOCAL_BOUNDS / "local_bound_claims.csv",
        "R1_WEP_source_charge",
        "Local source-backed WEP bound row with URL/DOI provenance.",
    ),
    "SRC4363_06_1066_bound_import": (
        SOURCE_DIR / "P8_Y5_R10_1066_WEP_DELTA_W_BOUND_IMPORT.csv",
        "BOUND1066_0_WEP_source_charge",
        "Earlier imported WEP Delta_w/tau bound row.",
    ),
    "SRC4363_07_1694_validation": (
        SOURCE_DIR / "P8_Y5_BRR545_1694_VALIDATION.csv",
        "VAL1694_3_bound_anchor_imported",
        "1694 validator confirms the bound anchor import is schema-only nonprediction.",
    ),
}


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def find_line(path: Path, needle: str) -> str:
    text = read_text(path)
    index = text.find(needle)
    if index < 0:
        return ""
    return str(text[:index].count("\n") + 1)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: List[Dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: str(row.get(field, "")) for field in fields})


def csv_line(row: Iterable[str]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(list(row))
    return buffer.getvalue()


def md_cell(value: object) -> str:
    return str(value).replace("|", r"\|").replace("\n", "<br>")


def md_table(rows: List[Dict[str, str]], fields: List[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_cell(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def append_once(path: Path, marker: str, block: str) -> None:
    text = read_text(path)
    if marker in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + block.strip() + "\n", encoding="utf-8")


def append_claim_once(path: Path, claim_id: str, row: List[str]) -> None:
    text = read_text(path)
    if f"\n{claim_id}," in text:
        return
    if text and not text.endswith("\n"):
        text += "\n"
    path.write_text(text + csv_line(row), encoding="utf-8")


def source_rows() -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        line_number = find_line(path, needle)
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "source_id": source_id,
                "path": str(path),
                "path_exists": str(path.exists()),
                "needle": needle,
                "needle_found": str(bool(line_number)),
                "line_number": line_number,
                "role": role,
                "valid_for_claim": "False",
            }
        )
    return rows


def extract_bound_row() -> Dict[str, str]:
    rows = read_csv(LOCAL_BOUNDS / "local_bound_claims.csv")
    matches = [row for row in rows if row.get("row_id") == "R1_WEP_source_charge"]
    if len(matches) != 1:
        raise ValueError("expected exactly one R1_WEP_source_charge row")
    return matches[0]


def derivation_rows(bound_row: Dict[str, str]) -> List[Dict[str, str]]:
    return [
        {
            "derivation_id": "DER4363_0_ordered_vector",
            "statement": "Use the ordered C_src_open product basis for this partial WEP projection.",
            "formula": f"C_src_product_basis = ({CSRC_ORDER})",
            "proof_status": "DEFINITION_FROM_4362_WITH_PRODUCT_REFINEMENT",
            "what_is_closed": "product component p_WEP_TiPt is explicitly separated from Delta_w amplitude",
            "what_remains_open": "Delta_w vector, Xi_open and epsilon_Gsrc are not evaluated",
            "claim_allowed": "False",
        },
        {
            "derivation_id": "DER4363_1_product_projection",
            "statement": "The MICROSCOPE product observable reads the WEP product component directly.",
            "formula": f"P_WEP_TiPt = |p_WEP_TiPt| = |[ {PROJECTION_ROW} ] dot C_src_product_basis|",
            "proof_status": "EXACT_LINEAR_PROJECTION_FOR_PRODUCT_COMPONENT",
            "what_is_closed": "Pi_WEP_product row is numeric and fixed before scoring",
            "what_remains_open": "this does not invert tau_WEP and does not give |Delta_w_TiPt|",
            "claim_allowed": "False",
        },
        {
            "derivation_id": "DER4363_2_source_bound",
            "statement": "The accepted source-backed bound anchor supplies the product comparator.",
            "formula": f"|p_WEP_TiPt| <= {bound_row['upper_bound']}",
            "proof_status": "SOURCE_BACKED_BOUND_ANCHOR_IMPORTED",
            "what_is_closed": "numeric bound exists for the product row",
            "what_remains_open": "it is a bound anchor, not an MTS predicted product value",
            "claim_allowed": "False",
        },
        {
            "derivation_id": "DER4363_3_no_tau_inversion",
            "statement": "No lower bound on tau_WEP is used in 4363.",
            "formula": "|Delta_w_TiPt| <= 2.8e-15/tau_min is forbidden unless tau_min>0 is parent-signed or source-computed",
            "proof_status": "FIREWALL_RETAINED",
            "what_is_closed": "prevents the earlier illegal leap from product to amplitude",
            "what_remains_open": "4364 must derive tau_min or keep WEP product-only",
            "claim_allowed": "False",
        },
    ]


def projection_rows(bound_row: Dict[str, str]) -> List[Dict[str, str]]:
    return [
        {
            "projection_id": "PI4363_WEP_product",
            "arena": "WEP/source-composition",
            "input_vector": "C_src_product_basis",
            "input_order": CSRC_ORDER,
            "projection_matrix_row": PROJECTION_ROW,
            "projected_quantity": "P_WEP_TiPt_abs_product",
            "projection_formula": "P_WEP_TiPt = abs(p_WEP_TiPt)",
            "source_bound_value": bound_row["upper_bound"],
            "source_bound_units": bound_row["units"],
            "source_dataset_id": bound_row["dataset_id"],
            "source_row_id": bound_row["row_id"],
            "source_reference": bound_row["reference_path_or_url"],
            "source_note": bound_row["reference_note"],
            "projection_numeric": "True",
            "source_backed_bound": "True",
            "fixed_before_scoring": "True",
            "partial_score_ready": "True",
            "valid_prediction_row": "False",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def runner_rows(bound_row: Dict[str, str]) -> List[Dict[str, str]]:
    return [
        {
            "run_id": "RUN4363_0_schema_zero",
            "input_case": "future theorem gives p_WEP_TiPt=0",
            "projection_id": "PI4363_WEP_product",
            "computed_quantity": "0",
            "bound": bound_row["upper_bound"],
            "comparison": "0 <= bound",
            "runner_status": "WOULD_PASS_PRODUCT_ROW_ONLY",
            "what_it_does_not_prove": "Delta_w amplitude, tau_WEP nonzero, WEP full-vector pass, local GR",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "run_id": "RUN4363_1_symbolic_current",
            "input_case": "current corpus p_WEP_TiPt is symbolic",
            "projection_id": "PI4363_WEP_product",
            "computed_quantity": "MISSING_PARENT_PRODUCT_VALUE",
            "bound": bound_row["upper_bound"],
            "comparison": "not scored",
            "runner_status": "BLOCKED_NO_MTS_PRODUCT_VALUE",
            "what_it_does_not_prove": "the row is a comparator/projection input, not a prediction",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
        {
            "run_id": "RUN4363_2_future_numeric",
            "input_case": "future candidate supplies numeric p_WEP_TiPt before looking at residuals",
            "projection_id": "PI4363_WEP_product",
            "computed_quantity": "abs(candidate_p_WEP_TiPt)",
            "bound": bound_row["upper_bound"],
            "comparison": f"accept product row only if abs(candidate_p_WEP_TiPt) <= {bound_row['upper_bound']}",
            "runner_status": "READY_FOR_FUTURE_PARTIAL_NUMERIC_PRODUCT_CHECK",
            "what_it_does_not_prove": "full local branch still needs source-charge projection and tau inversion or zero theorem",
            "valid_for_claim": "False",
            "claim_allowed": "False",
        },
    ]


def blocker_rows() -> List[Dict[str, str]]:
    return [
        {
            "blocker_id": "BLK4363_0_tau_inversion",
            "remaining_blocker": "tau_WEP lower bound or parent-owned zero theorem",
            "why_it_matters": "without tau_min>0, |Delta_w_TiPt tau_WEP| does not bound |Delta_w_TiPt|",
            "next_action": "derive tau_min from source/readout geometry or keep product-only route",
            "claim_allowed": "False",
        },
        {
            "blocker_id": "BLK4363_1_source_charge_basis",
            "remaining_blocker": "source/test material charge basis",
            "why_it_matters": "full WEP source-composition projection needs material sensitivities and source-normalization map",
            "next_action": "source or derive DeltaQ_source/material tensor",
            "claim_allowed": "False",
        },
        {
            "blocker_id": "BLK4363_2_other_Csrc_components",
            "remaining_blocker": "Xi_open and epsilon_Gsrc_open projections",
            "why_it_matters": "the product row alone cannot cover hidden source-label tails or Newton/source normalization drift",
            "next_action": "fill Pi_WEP rows for Xi_open and epsilon_Gsrc_open or prove they vanish",
            "claim_allowed": "False",
        },
        {
            "blocker_id": "BLK4363_3_local_GR_transfer",
            "remaining_blocker": "metric/PPN/Newton transfer from WEP product to local GR residuals",
            "why_it_matters": "a WEP product bound is not a PPN or Newton source-normalization proof",
            "next_action": "build Pi_PPN/Pi_GR source-to-metric row or parent-sign graph zero",
            "claim_allowed": "False",
        },
    ]


def claim_gate_rows() -> List[Dict[str, str]]:
    return [
        {
            "gate_id": "GATE4363_0_projection_row",
            "gate": "first source-backed C_src projection input",
            "requirement": "numeric projection row, source-backed bound, fixed before scoring",
            "current_result": "PASS_PARTIAL_NONCLAIM",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4363_1_product_score",
            "gate": "score current MTS WEP product",
            "requirement": "parent-owned numeric p_WEP_TiPt or theorem-zero",
            "current_result": "BLOCKED_NO_MTS_PRODUCT_VALUE",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4363_2_delta_w_amplitude",
            "gate": "convert product bound to Delta_w amplitude",
            "requirement": "tau_min>0 or owner/no-wA theorem",
            "current_result": "FORBIDDEN",
            "claim_allowed": "False",
        },
        {
            "gate_id": "GATE4363_3_local_claim",
            "gate": "claim WEP/local-GR/Newton/PPN pass",
            "requirement": "all C_src components projected and bounded or theorem-zero with conservation/local transfer",
            "current_result": "FORBIDDEN",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> List[Dict[str, str]]:
    return [
        {
            "decision_id": "DEC4363_0",
            "decision": DECISION,
            "rationale": "4363 fills the first real C_src projection input without cheating: the WEP product component p_WEP_TiPt=Delta_w_TiPt*tau_WEP is read by a numeric row [0,0,1,0] and compared to the MICROSCOPE source-backed bound 2.8e-15. This is a real partial projection/comparator row, but it is not a Delta_w amplitude bound, not a full WEP pass and not local GR.",
            "next_target": NEXT_TARGET,
            "valid_for_claim": "False",
            "claim_allowed": "False",
        }
    ]


def status_rows() -> List[Dict[str, str]]:
    return [
        {
            "status_id": "STAT4363_0",
            "item": "first projection input",
            "status": "CLOSED_PARTIAL_NONCLAIM",
            "detail": "Pi_WEP_product is numeric, source-backed and fixed before scoring.",
        },
        {
            "status_id": "STAT4363_1",
            "item": "current MTS score",
            "status": "NOT_SCORED",
            "detail": "No parent-owned numeric p_WEP_TiPt or theorem-zero exists yet.",
        },
        {
            "status_id": "STAT4363_2",
            "item": "Delta_w amplitude",
            "status": "BLOCKED",
            "detail": "Product-to-amplitude conversion still requires tau_min>0 or owner/no-wA theorem.",
        },
        {
            "status_id": "STAT4363_3",
            "item": "best next move",
            "status": "TAU_WEP_LOWER_BOUND_OR_PRODUCT_ONLY_LOCAL_ROUTE",
            "detail": "Either derive tau_WEP lower bound or explicitly accept only product-level WEP discipline while attacking Pi_PPN/Pi_GR.",
        },
    ]


def next_target_rows() -> List[Dict[str, str]]:
    return [
        {
            "target_id": "NT4363_0",
            "next_target": NEXT_TARGET,
            "question": "Can the WEP product projection be lifted to a Delta_w/source-amplitude bound, or must the local route stay product-only?",
            "derive_route": "prove tau_WEP has a positive lower bound from source worldtube, material tensor, readout kernel and no-cancellation alignment",
            "safer_route": "keep the product bound only and move to Pi_PPN/Pi_GR source-to-metric rows without claiming Delta_w",
            "fallback_route": "parent-sign owner/no-wA graph and set p_WEP_TiPt=0 by theorem",
            "claim_allowed": "False",
        }
    ]


def validation_rows(
    sources: List[Dict[str, str]],
    derivation: List[Dict[str, str]],
    projections: List[Dict[str, str]],
    runner: List[Dict[str, str]],
    blockers: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> List[Dict[str, str]]:
    rows: List[Dict[str, str]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "check_id": check_id,
                "check": check,
                "passed": str(bool(passed)),
                "detail": detail,
            }
        )

    add("VAL4363_00_sources_exist", "all cited local source paths exist", all(row["path_exists"] == "True" for row in sources), "source register path_exists flags")
    add("VAL4363_01_needles_found", "all cited local source needles found", all(row["needle_found"] == "True" for row in sources), "source register needle_found flags")
    add(
        "VAL4363_02_projection_numeric",
        "WEP product projection row numeric",
        projections[0]["projection_matrix_row"] == PROJECTION_ROW and projections[0]["projection_numeric"] == "True",
        projections[0]["projection_matrix_row"],
    )
    add(
        "VAL4363_03_bound_source_backed",
        "WEP product bound source-backed and numeric",
        projections[0]["source_backed_bound"] == "True" and float(projections[0]["source_bound_value"]) == WEP_BOUND_VALUE,
        projections[0]["source_bound_value"],
    )
    add(
        "VAL4363_04_no_tau_inversion",
        "tau inversion remains forbidden",
        any(row["derivation_id"] == "DER4363_3_no_tau_inversion" for row in derivation)
        and any(row["blocker_id"] == "BLK4363_0_tau_inversion" for row in blockers),
        "product-to-amplitude firewall retained",
    )
    add(
        "VAL4363_05_runner_nonclaim",
        "runner rows remain nonclaim",
        all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in runner),
        "runner flags",
    )
    add(
        "VAL4363_06_claim_gates_block",
        "claim gates block local claims",
        any(row["gate_id"] == "GATE4363_3_local_claim" and row["current_result"] == "FORBIDDEN" for row in gates),
        "local claim gate",
    )
    add(
        "VAL4363_07_decision_nonclaim",
        "decision is nonclaim",
        decisions[0]["decision"] == DECISION and decisions[0]["claim_allowed"] == "False",
        DECISION,
    )
    add(
        "VAL4363_08_status_next_target",
        "next target selected",
        statuses[-1]["status"] == "TAU_WEP_LOWER_BOUND_OR_PRODUCT_ONLY_LOCAL_ROUTE" and next_targets[0]["next_target"] == NEXT_TARGET,
        NEXT_TARGET,
    )
    add("VAL4363_09_formal_marker", "formal marker written", MARKER in read_text(FORMAL_PATH), str(FORMAL_PATH))
    add("VAL4363_10_post_doc_marker", "post doc marker written", MARKER in read_text(DOC_PATH), str(DOC_PATH))
    add("VAL4363_11_spine_marker", "spine marker appended", MARKER in read_text(FORMAL / "07-unification-spine.md"), str(FORMAL / "07-unification-spine.md"))
    add("VAL4363_12_packet_marker", "packet marker appended", PACKET_MARKER in read_text(FORMAL / "180-PPC4161-private-local-packet-integration.md"), str(FORMAL / "180-PPC4161-private-local-packet-integration.md"))
    add("VAL4363_13_claim_register", "claim register updated", f"\n{CLAIM_ID}," in read_text(FORMAL / "02-claims-register.csv"), str(FORMAL / "02-claims-register.csv"))
    return rows


def write_docs(
    sources: List[Dict[str, str]],
    derivation: List[Dict[str, str]],
    projections: List[Dict[str, str]],
    runner: List[Dict[str, str]],
    blockers: List[Dict[str, str]],
    gates: List[Dict[str, str]],
    decisions: List[Dict[str, str]],
    statuses: List[Dict[str, str]],
    next_targets: List[Dict[str, str]],
) -> None:
    formal = f"""# PPC4161 transition: first C_src projection input or parent graph edge proof

Marker: `{MARKER}`

Generated: {STAMP}

## Purpose

4362 turned the source-coupling problem into an explicit closure runner. 4363 fills the first real projection input without overclaiming: the WEP product component can be projected and bounded directly, while the forbidden product-to-amplitude leap remains blocked.

## Derived product projection

Use the product-refined source-coupling basis:

`C_src_product_basis = ({CSRC_ORDER})`.

The first source-backed projection row is:

`Pi_WEP_product = [{PROJECTION_ROW}]`.

Therefore:

`P_WEP_TiPt = |Pi_WEP_product dot C_src_product_basis| = |p_WEP_TiPt| = |Delta_w_TiPt tau_WEP|`.

The MICROSCOPE source-backed bound anchor supplies:

`|p_WEP_TiPt| <= {WEP_BOUND_VALUE}`.

This closes a product-level projection row only. It does not infer `|Delta_w_TiPt|`, because `tau_WEP` may be zero or arbitrarily small until a lower bound or zero theorem is supplied.

## Derivation audit

{md_table(derivation, ["derivation_id", "statement", "formula", "proof_status", "what_is_closed", "what_remains_open", "claim_allowed"])}

## Projection row

{md_table(projections, ["projection_id", "arena", "input_order", "projection_matrix_row", "projected_quantity", "source_bound_value", "source_bound_units", "projection_numeric", "source_backed_bound", "partial_score_ready", "claim_allowed"])}

## Runner

{md_table(runner, ["run_id", "input_case", "computed_quantity", "bound", "comparison", "runner_status", "what_it_does_not_prove", "claim_allowed"])}

## Remaining blockers

{md_table(blockers, ["blocker_id", "remaining_blocker", "why_it_matters", "next_action", "claim_allowed"])}

## Claim gates

{md_table(gates, ["gate_id", "gate", "requirement", "current_result", "claim_allowed"])}

## Decision

{md_table(decisions, ["decision_id", "decision", "rationale", "next_target", "claim_allowed"])}

## Status

{md_table(statuses, ["status_id", "item", "status", "detail"])}

## Next target

{md_table(next_targets, ["target_id", "next_target", "question", "derive_route", "safer_route", "fallback_route", "claim_allowed"])}

## Source register

{md_table(sources, ["source_id", "path_exists", "needle_found", "line_number", "role"])}
"""
    FORMAL_PATH.write_text(formal, encoding="utf-8")

    post_doc = f"""# 4363 - first C_src projection input or parent graph edge proof

Marker: `{MARKER}`

Generated: {STAMP}

## Result

- First real projection row closed: `Pi_WEP_product = [0,0,1,0]`.
- Product comparator closed: `|Delta_w_TiPt tau_WEP| <= {WEP_BOUND_VALUE}`.
- Forbidden leap still blocked: no `|Delta_w_TiPt|` bound without `tau_min>0` or owner/no-wA zero theorem.

## Why this matters

This is the first post-4362 move where one part of `C_src_open` has a concrete source-backed projection/bound row. Small but real. The coupling gremlin now has one nail in the floor.

## Files

- Formal checkpoint: `{FORMAL_PATH}`
- Projection row: `{SOURCE_DIR / "P8_Y5_R2FR_4363_WEPPRODUCT_PROJECTION_ROW.csv"}`
- Runner: `{SOURCE_DIR / "P8_Y5_R2FR_4363_WEPPRODUCT_RUNNER.csv"}`
- Validation: `{VALIDATION_PATH}`

## Next

{NEXT_TARGET}
"""
    DOC_PATH.write_text(post_doc, encoding="utf-8")


def update_rollups() -> None:
    spine_block = f"""

## 4363 Transition first C_src projection input

Marker: `{MARKER}`

4363 fills the first real post-4362 projection input without pretending the whole coupling problem is solved. In the product-refined basis `C_src_product_basis=(Delta_w_component_vector, Xi_open, p_WEP_TiPt, epsilon_Gsrc_open)`, the WEP product observable has the fixed numeric row `Pi_WEP_product=[0,0,1,0]`, so `P_WEP_TiPt=|p_WEP_TiPt|=|Delta_w_TiPt tau_WEP|`. The MICROSCOPE source-backed bound anchor gives `|p_WEP_TiPt| <= 2.8e-15`.

This is a real partial C_src projection row, not a local-GR/WEP claim. The product-to-amplitude inference remains forbidden until `tau_WEP` has a positive lower bound or the owner/no-wA theorem sets the product to zero. Next target: `{NEXT_TARGET}`.
"""
    append_once(FORMAL / "07-unification-spine.md", MARKER, spine_block)

    packet_block = f"""

## 4363 packet update: first C_src projection row

Marker: `{PACKET_MARKER}`

Packet update: one source-coupling projection row is now fixed. `Pi_WEP_product=[0,0,1,0]` maps the product-refined `C_src` basis to `|Delta_w_TiPt tau_WEP|`, with the MICROSCOPE bound anchor `<=2.8e-15`. This does not bound `Delta_w_TiPt` by itself and does not prove local GR, but it gives the C_src runner its first real source-backed projection/comparator input.
"""
    append_once(FORMAL / "180-PPC4161-private-local-packet-integration.md", PACKET_MARKER, packet_block)

    append_claim_once(
        FORMAL / "02-claims-register.csv",
        CLAIM_ID,
        [
            CLAIM_ID,
            "local_gr",
            "4363 derives the first source-backed C_src projection input after the explicit closure runner: in the product-refined basis C_src_product_basis=(Delta_w_component_vector, Xi_open, p_WEP_TiPt, epsilon_Gsrc_open), the WEP product row Pi_WEP_product=[0,0,1,0] gives P_WEP_TiPt=|p_WEP_TiPt|=|Delta_w_TiPt tau_WEP|. The MICROSCOPE source-backed bound anchor supplies |p_WEP_TiPt|<=2.8e-15. This is a partial nonclaim comparator/projection row only; it does not infer |Delta_w_TiPt| without tau_min>0 or an owner/no-wA zero theorem, and it does not claim WEP/local-GR/Newton/PPN pass.",
            "4363 source register, derivation audit, WEP product projection row, WEP product runner, remaining blockers, claim gates, decision, status, next target and validation CSV.",
            "first_source_backed_Csrc_WEP_product_projection_row_nonclaim_Delta_w_amplitude_blocked",
            "Derive tau_WEP lower bound or keep WEP product-only while filling Pi_PPN/Pi_GR source-to-metric rows.",
            "Dividing by tau_WEP without tau_min; treating a product bound as a Delta_w amplitude bound; using a WEP comparator as local-GR proof.",
        ],
    )


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    bound_row = extract_bound_row()
    sources = source_rows()
    derivation = derivation_rows(bound_row)
    projections = projection_rows(bound_row)
    runner = runner_rows(bound_row)
    blockers = blocker_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    statuses = status_rows()
    next_targets = next_target_rows()

    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4363_SOURCE_REGISTER.csv", sources)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4363_WEPPRODUCT_DERIVATION_AUDIT.csv", derivation)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4363_WEPPRODUCT_PROJECTION_ROW.csv", projections)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4363_WEPPRODUCT_RUNNER.csv", runner)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4363_REMAINING_BLOCKERS.csv", blockers)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4363_CLAIM_GATES.csv", gates)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4363_DECISION.csv", decisions)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4363_STATUS.csv", statuses)
    write_csv(SOURCE_DIR / "P8_Y5_R2FR_4363_NEXT_TARGET.csv", next_targets)

    write_docs(sources, derivation, projections, runner, blockers, gates, decisions, statuses, next_targets)
    update_rollups()

    validations = validation_rows(sources, derivation, projections, runner, blockers, gates, decisions, statuses, next_targets)
    write_csv(VALIDATION_PATH, validations)
    failed = [row for row in validations if row["passed"] != "True"]
    if failed:
        details = "; ".join(f"{row['check_id']}={row['detail']}" for row in failed)
        raise SystemExit(f"4363 validation failed: {details}")

    print(f"{CHECKPOINT} generated: {DECISION}")
    print(f"formal={FORMAL_PATH}")
    print(f"validation={VALIDATION_PATH}")


if __name__ == "__main__":
    main()
