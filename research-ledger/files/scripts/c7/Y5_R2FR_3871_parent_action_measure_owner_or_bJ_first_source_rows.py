from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path


CHECKPOINT = "3871"
BRANCH = "MTS_R2FR_Y5_PARENT_ACTION_MEASURE_OWNER_OR_BJ_FIRST_SOURCE_ROWS_3871"

PCW = Path(__file__).resolve().parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
OUT = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "3871-Y5-R2FR-parent-action-measure-owner-or-bJ-first-source-rows.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

CSV_3870_NEXT = OUT / "P8_Y5_R2FR_3870_NEXT_TARGET.csv"
CSV_3870_THEOREM = OUT / "P8_Y5_R2FR_3870_NO_SOURCE_SLOT_THEOREM.csv"
CSV_3870_BJ = OUT / "P8_Y5_R2FR_3870_BJ_FINITE_INPUT_ROWS.csv"
CSV_1078_MEASURE = OUT / "P8_Y5_R10_1078_ACTION_MEASURE_PROOF_ATTEMPT.csv"
CSV_1066_FMQ = OUT / "P8_Y5_R10_1066_FIELD_MEASURE_QUANTUM_NORMALIZATION_AUDIT.csv"
CSV_1067_HMO = OUT / "P8_Y5_R10_1067_HBAR_MEASURE_OWNER_AUDIT.csv"
CSV_1067_ASO = OUT / "P8_Y5_R10_1067_PARENT_ACTION_SCALE_OWNER_ATTEMPT.csv"
CSV_1067_SWC = OUT / "P8_Y5_R10_1067_SOURCE_WEIGHT_CONSEQUENCE_LEDGER.csv"
CSV_1388_RETURN = OUT / "P8_Y5_R10_1388_ACTION_MEASURE_OWNER_RETURN_GATE.csv"
CSV_1388_REFUSE = OUT / "P8_Y5_R10_1388_SCORING_REFUSAL_MATRIX.csv"
CSV_1387_FILL = OUT / "P8_Y5_R10_1387_DELTA_W_SOURCE_BETA_FIRST_FILL.csv"
CSV_1214_NO_SLOT = OUT / "P8_Y5_R10_1214_NO_SOURCE_ONLY_SLOT_SIGNATURE_AUDIT.csv"
CSV_1220_TYPED = OUT / "P8_Y5_R10_1220_PARENT_TYPED_SIGNATURE_ATTEMPT.csv"
CSV_3819_SOURCE = OUT / "P8_Y5_R2FR_3819_FINITE_SOURCE_NORMALIZATION_RESIDUALS.csv"

OUTPUTS = {
    "sources": OUT / "P8_Y5_R2FR_3871_SOURCE_REGISTER.csv",
    "theorem": OUT / "P8_Y5_R2FR_3871_ACTION_MEASURE_OWNER_THEOREM.csv",
    "owner_audit": OUT / "P8_Y5_R2FR_3871_ACTION_MEASURE_OWNER_AUDIT.csv",
    "bj_source_rows": OUT / "P8_Y5_R2FR_3871_BJ_FIRST_SOURCE_ROW_CONTRACT.csv",
    "refusal": OUT / "P8_Y5_R2FR_3871_SCORING_REFUSAL_ROWS.csv",
    "gates": OUT / "P8_Y5_R2FR_3871_CLAIM_GATES.csv",
    "decisions": OUT / "P8_Y5_R2FR_3871_DECISION_ROWS.csv",
    "next": OUT / "P8_Y5_R2FR_3871_NEXT_TARGET.csv",
    "status": OUT / "P8_Y5_R2FR_3871_STATUS.csv",
    "validation": OUT / "P8_Y5_BRR545_3871_VALIDATION.csv",
}

SOURCE_SPECS = [
    ("SRC3871_00_3870_next", CSV_3870_NEXT, "NEXT3870_0", "3870 selected action-measure owner or source rows"),
    ("SRC3871_01_3870_theorem", CSV_3870_THEOREM, "NST3870_5_verdict", "typed no-source-slot theorem verdict"),
    ("SRC3871_02_3870_bj", CSV_3870_BJ, "BJF3870_2_Delta_w_A", "3870 finite b_J row requirements"),
    ("SRC3871_03_1078_measure", CSV_1078_MEASURE, "AM1078_4_verdict", "action-measure proof attempt"),
    ("SRC3871_04_1066_fmq", CSV_1066_FMQ, "FMQ1066_4_verdict", "field/measure/quantum normalization audit"),
    ("SRC3871_05_1067_hmo", CSV_1067_HMO, "HMO1067_4_verdict", "hbar/measure owner audit"),
    ("SRC3871_06_1067_aso", CSV_1067_ASO, "ASO1067_5_verdict", "parent action-scale owner attempt"),
    ("SRC3871_07_1067_swc", CSV_1067_SWC, "SWC1067_4_verdict", "source-weight consequence ledger"),
    ("SRC3871_08_1388_return", CSV_1388_RETURN, "AMR1388_4_return_verdict", "action-measure owner return gate"),
    ("SRC3871_09_1388_refusal", CSV_1388_REFUSE, "SFM1388_5_local_GR", "scoring refusal matrix"),
    ("SRC3871_10_1387_fill", CSV_1387_FILL, "DWB1387_6_first_fill_verdict", "Delta_w first fill rows"),
    ("SRC3871_11_1214_no_slot", CSV_1214_NO_SLOT, "NSS1214_2_action_measure_owner", "no-source-only action-measure owner clause"),
    ("SRC3871_12_1220_typed", CSV_1220_TYPED, "PTOL1220_4_action_scale_measure_owner", "typed signature action-scale owner"),
    ("SRC3871_13_3819_source", CSV_3819_SOURCE, "R3819_6_total", "Newton/local-GR source-normalization residual"),
]

THEOREM = (
    "If one parent action functional is normalized by a single hbar_parent and one species-blind measure Dmu_parent before readout, "
    "then independent relative multipliers w_A S_A, c_A_pre J_A, and kappa_A T_A are not gauge redundancies; they are either absent by grammar, "
    "common derivative-silent calibration, or explicit residual source couplings."
)
ZERO_CONDITION = (
    "hbar_parent fixed + Dmu_parent species-blind + no sector Jacobian + same current owner + readout/radiative stability"
)


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(PCW))
    except ValueError:
        return str(path)


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def source_register_rows(timestamp: str) -> list[dict[str, object]]:
    rows = []
    for source_id, path, needle, role in SOURCE_SPECS:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "checkpoint": CHECKPOINT,
                "path": rel(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "claim_use": "nonclaim_action_measure_owner_or_bJ_source_contract",
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("AMT3871_0_classical_guard", "classical EOM scaling is not enough", "delta(w_A S_A)/delta Psi_A=0 may preserve isolated equations, but delta(w_A S_A)/delta g_obs=w_A T_A", "OBSTRUCTION_EXPLICIT", "do not dismiss w_A from classical equations"),
        ("AMT3871_1_quantum_measure", "single hbar/measure theorem", THEOREM, "EXACT_CONDITIONAL_THEOREM", "requires parent-owned hbar/measure and species-blind Jacobian"),
        ("AMT3871_2_common_mode", "common calibration law", "w_A=w_* is harmless only if w_* is universal and D_t,D_r,D_A,D_lambda,D_frame ln w_*=0", "EXACT_GUARD", "commonness and derivative silence must be proved"),
        ("AMT3871_3_relative_weight", "relative source weight consequence", "w_A=w_*(1+Delta_w_A) changes T_source and cannot be absorbed into G_N if Delta_w_A != 0", "LIVE_RESIDUAL", "requires theorem-zero or source-backed bound"),
        ("AMT3871_4_measure_jacobian", "measure/Jacobian reentry", "Dmu_parent=prod_A J_A Dpsi_A can mimic w_A if J_A is species/source dependent", "LIVE_REENTRY_UNTIL_MEASURE_DESCENT", "species-blind measure descent missing"),
        ("AMT3871_5_verdict", "action-measure owner status", "the action-measure owner theorem is exact conditional but not parent-derived in current corpus", "OWNER_NOT_DERIVED_SOURCE_ROWS_REQUIRED", "use first b_J source-row contract"),
    ]
    return [
        {
            "theorem_id": theorem_id,
            "claim_piece": claim_piece,
            "statement": statement,
            "result": result,
            "remaining_gap": gap,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for theorem_id, claim_piece, statement, result, gap in rows
    ]


def owner_audit_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("OWN3871_0_hbar_parent", "hbar_parent", "one action quantum/phase normalization for all ordinary matter sectors", "NOT_PARENT_OWNED", "HMO1067_0_hbar_parent", "derive fixed hbar/action scale owner"),
        ("OWN3871_1_measure_parent", "Dmu_parent", "species-blind path-integral/statistical/source measure", "NOT_PARENT_OWNED", "HMO1067_1_measure_parent", "derive species-blind measure/Jacobian descent"),
        ("OWN3871_2_current_owner", "J_owner", "same parent owner fixes current, charge labels and source normalization", "CANDIDATE_MISSING", "HMO1067_2_current_owner", "same-current owner parent certificate"),
        ("OWN3871_3_readout_descent", "readout/hbar*c", "dimensionless readout constants quotient-fixed or parent-owned", "UNSIGNED", "HMO1067_3_readout_descent", "readout/radiative stability"),
        ("OWN3871_4_common_G_guard", "G_N calibration", "only universal derivative-silent common factor may be absorbed", "POLICY_ONLY", "AMR1388_3_single_GN_calibration", "derivative silence checks"),
        ("OWN3871_5_verdict", "owner package", ZERO_CONDITION, "OWNER_NOT_DERIVED", "HMO1067_4_verdict; ASO1067_5_verdict", "owner proof or finite rows"),
    ]
    return [
        {
            "audit_id": audit_id,
            "object": obj,
            "required_signature": signature,
            "current_status": status,
            "source_row": source_row,
            "next_requirement": req,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for audit_id, obj, signature, status, source_row, req in rows
    ]


def bj_source_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("BJS3871_0_common_w", "w_common", "common action/source factor", "dimensionless", "MISSING_COMMON_ACTION_NORMALIZATION", "single parent hbar/action-measure owner; derivative silence", "do not absorb unless universal and derivative-silent"),
        ("BJS3871_1_Delta_w_A", "Delta_w_A", "relative pre-variation source/action multiplier", "dimensionless", "FIRST_FILL_ROW_READY_VALUE_MISSING", "material/source class value or upper bound", "cannot score WEP/Newton/source without value/zero"),
        ("BJS3871_2_beta_w_source", "beta_w_source", "partial_phi ln w_source(phi)", "canonical beta units", "MISSING_SOURCE_BETA_WEIGHT_FUNCTION", "canonical field and source weight function", "R10/source fifth-force source leg blocked"),
        ("BJS3871_3_beta_w_test", "beta_w_test", "partial_phi ln w_test(phi)", "canonical beta units", "MISSING_TEST_BETA_WEIGHT_FUNCTION", "test material action and composition map", "WEP/R10 test leg blocked"),
        ("BJS3871_4_measure_jacobian", "J_A_measure", "species/source measure Jacobian", "dimensionless", "MISSING_MEASURE_JACOBIAN_ZERO_OR_BOUND", "species-blind measure descent or Jacobian bound", "can mimic w_A"),
        ("BJS3871_5_cA_pre", "c_A_pre", "pre-variation current/source coefficient", "dimensionless", "MISSING_CURRENT_SLOT_ZERO_OR_VALUE", "same-current owner or finite coefficient value", "maps into b_J/source normalization"),
        ("BJS3871_6_kappa_A", "kappa_A", "active-source selector coefficient", "dimensionless", "MISSING_SOURCE_SELECTOR_ZERO_OR_VALUE", "source selector grammar theorem or finite source vector", "maps into Newton/PPN/local-GR source residual"),
        ("BJS3871_7_arena_kernel", "K_arena", "projection kernel for WEP/R10/PPN/clock/orbital", "arena units", "MISSING_ARENA_PROJECTIONS", "arena-specific material/source/readout map", "no numeric score without kernel"),
    ]
    return [
        {
            "row_id": row_id,
            "symbol": symbol,
            "definition": definition,
            "units": units,
            "current_status": status,
            "required_source_or_theorem": required,
            "claim_guard": guard,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, symbol, definition, units, status, required, guard in rows
    ]


def refusal_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("REF3871_0_owner", "theorem-zero source coupling", "blocked until hbar/measure/current/readout owner package signs", "OWNER_NOT_DERIVED"),
        ("REF3871_1_Newton", "Newton/source normalization", "blocked until common calibration or Delta_w/source vector rows are sourced", "BLOCKED_NO_SCORE"),
        ("REF3871_2_WEP", "WEP", "blocked until Delta_w_AB/beta_w/material kernel rows are sourced", "BLOCKED_NO_SCORE"),
        ("REF3871_3_R10", "R10", "blocked until beta_w source/test, K(lambda), tail and bound curve are sourced", "BLOCKED_NO_SCORE"),
        ("REF3871_4_PPN_local_GR", "PPN/local_GR", "blocked until complete finite source residual vector or owner theorem closes", "BLOCKED_NO_SCORE"),
    ]
    return [
        {
            "refusal_id": refusal_id,
            "claim_area": area,
            "reason": reason,
            "status": status,
            "claim_allowed": False,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for refusal_id, area, reason, status in rows
    ]


def gate_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    owner_audit: list[dict[str, object]],
    bj_rows: list[dict[str, object]],
    refusal: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    gates = [
        ("G3871_0_sources", "all source paths resolve", all(row["exists"] and row["needle_found"] for row in sources), "source register resolved"),
        ("G3871_1_theorem", "action-measure conditional theorem written", any(row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem), "single hbar/measure theorem present"),
        ("G3871_2_owner_package", "owner package parent-derived", False, "hbar, measure, current and readout owners remain unsigned"),
        ("G3871_3_source_rows", "first b_J source-row contract staged", {"Delta_w_A", "beta_w_source", "beta_w_test", "J_A_measure", "c_A_pre", "kappa_A"} <= {row["symbol"] for row in bj_rows}, "finite row contract covers live source slots"),
        ("G3871_4_scores_refused", "scores remain refused until rows are sourced", all(row["status"] == "BLOCKED_NO_SCORE" or row["status"] == "OWNER_NOT_DERIVED" for row in refusal), "no Newton/WEP/R10/PPN/local-GR scoring"),
        ("G3871_5_no_claim", "no generated row permits a claim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in theorem + owner_audit + bj_rows + refusal), "nonclaim discipline preserved"),
    ]
    return [
        {
            "gate_id": gate_id,
            "gate": gate,
            "status": "PASS" if passed else "BLOCKED",
            "claim_allowed": False,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for gate_id, gate, passed, reason in gates
    ]


def decision_rows(timestamp: str) -> list[dict[str, object]]:
    rows = [
        ("DEC3871_0", "do not use classical EOM to erase w_A", "source stress and quantum/statistical weighting still see action normalization", "keep obstruction explicit"),
        ("DEC3871_1", "action-measure owner remains the clean theorem route", "one hbar/measure owner would remove relative action weights up to common calibration", "keep owner theorem as conditional"),
        ("DEC3871_2", "finite b_J rows are now the executable fallback", "owner package is not parent-derived", "source or bound Delta_w, beta_w, measure Jacobian, c_A_pre, kappa_A and kernels"),
        ("DEC3871_3", "next route is material/source map acquisition", "the theorem route is blocked by missing parent owner, while finite rows need actual classes/kernels", "build material/source map or first candidate rows"),
    ]
    return [
        {
            "decision_id": decision_id,
            "decision": decision,
            "because": because,
            "next_action": action,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for decision_id, decision, because, action in rows
    ]


def next_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "next_id": "NEXT3871_0",
            "target_checkpoint": "3872-Y5-R2FR-bJ-material-source-map-or-first-candidate-coefficient-rows.md",
            "script": "scripts/Y5_R2FR_3872_bJ_material_source_map_or_first_candidate_coefficient_rows.py",
            "objective": "build the material/source class map and first candidate finite b_J coefficient rows for Delta_w_A, beta_w_source, beta_w_test, c_A_pre and kappa_A, while preserving no-claim gates",
            "why_next": "3871 shows the action-measure theorem is exact conditional but not parent-derived; progress now needs source/class/kernels for the finite branch",
            "claim_allowed": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, object]]:
    return [
        {
            "status_id": "STATUS3871_0",
            "checkpoint": CHECKPOINT,
            "branch": BRANCH,
            "result": "ACTION_MEASURE_OWNER_CONDITIONAL_SOURCE_ROWS_STAGED",
            "theorem": THEOREM,
            "zero_condition": ZERO_CONDITION,
            "claim_allowed": False,
            "next_gate": "3872 b_J material/source map or first candidate coefficient rows",
            "timestamp_utc": timestamp,
        }
    ]


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(str(row.get(column, "")).replace("\n", " ") for column in columns) + " |")
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    owner_audit: list[dict[str, object]],
    bj_rows: list[dict[str, object]],
    refusal: list[dict[str, object]],
    gates: list[dict[str, object]],
    decisions: list[dict[str, object]],
    next_target: list[dict[str, object]],
    timestamp: str,
) -> None:
    text = f"""# 3871 — Parent Action-Measure Owner Or bJ First Source Rows

Generated: `{timestamp}`

## Purpose

3870 made the typed no-source-slot theorem sharp. 3871 tests the cleanest missing owner: one parent action-scale / measure / hbar normalization.

## Conditional Theorem

`{THEOREM}`

Zero-condition package:

`{ZERO_CONDITION}`

## Source Register

{markdown_table(sources, ["source_id", "path", "exists", "needle_found", "role"])}

## Action-Measure Theorem

{markdown_table(theorem, ["theorem_id", "claim_piece", "result", "remaining_gap"])}

## Owner Audit

{markdown_table(owner_audit, ["audit_id", "object", "current_status", "source_row", "next_requirement"])}

## First bJ Source Row Contract

{markdown_table(bj_rows, ["row_id", "symbol", "definition", "current_status", "required_source_or_theorem"])}

## Scoring Refusals

{markdown_table(refusal, ["refusal_id", "claim_area", "status", "reason"])}

## Claim Gates

{markdown_table(gates, ["gate_id", "status", "claim_allowed", "reason"])}

## Decisions

{markdown_table(decisions, ["decision_id", "decision", "because", "next_action"])}

## Next Target

{markdown_table(next_target, ["next_id", "target_checkpoint", "objective", "why_next"])}

## Bottom Line

3871 closes the logical loop around `w_A`: isolated classical equations cannot erase it, because Hilbert source stress and quantum/statistical weighting still see the multiplier. A single parent `hbar/measure/action-scale` owner would kill relative `w_A` up to common calibration, but that owner is not currently derived.

So the branch is now honestly executable: either derive the owner package later, or source the finite `b_J` rows. No Newton/WEP/R10/PPN/local-GR score is allowed from this checkpoint.
"""
    DOC_PATH.write_text(text, encoding="utf-8")


def update_spine(timestamp: str) -> None:
    if not SPINE_PATH.exists():
        return
    text = read_text(SPINE_PATH)
    text = text.replace("Current State After 3870", "Current State After 3871", 1)
    text = "\n".join(line for line in text.splitlines() if not line.startswith("<!-- Generated by 3871 at "))
    paragraph = (
        "`3871` tests the action-measure owner route. "
        "It records the exact conditional theorem: one parent `S_parent/hbar_parent/Dmu_parent` owner with species-blind measure/Jacobian, same current owner, and readout stability would kill relative `w_A/c_A/kappa_A` source slots up to common derivative-silent calibration. "
        "It also proves the guard that classical EOM scaling is not enough, because Hilbert source stress and quantum/statistical weighting still see `w_A`. "
        "The owner package is not parent-derived, so the finite `b_J` source-row contract is staged for `Delta_w_A`, `beta_w_source`, `beta_w_test`, `J_A_measure`, `c_A_pre`, `kappa_A`, and arena kernels. "
        "Next gate: `3872`, build the material/source map or first candidate coefficient rows.\n\n"
    )
    if paragraph not in text and "## Next Best Gate" in text:
        text = text.replace("## Next Best Gate", paragraph + "## Next Best Gate", 1)
    old_gate = """`3871-Y5-R2FR-parent-action-measure-owner-or-bJ-first-source-rows.md`

Target: derive one parent action-scale/measure owner that kills relative `w_A/c_A/kappa_A` source slots, or fill the first strict source-backed `b_J` finite input rows.

This is the best next move because 3870 gives the typed no-source-slot theorem but cannot parent-sign the grammar; action-measure ownership is the highest-pressure missing clause and the finite rows are now explicit."""
    new_gate = """`3872-Y5-R2FR-bJ-material-source-map-or-first-candidate-coefficient-rows.md`

Target: build the material/source class map and first candidate finite `b_J` coefficient rows for `Delta_w_A`, `beta_w_source`, `beta_w_test`, `c_A_pre`, and `kappa_A`, while preserving no-claim gates.

This is the best next move because 3871 shows the action-measure theorem is exact conditional but not parent-derived; progress now needs source/class/kernels for the finite branch."""
    if old_gate in text:
        text = text.replace(old_gate, new_gate, 1)
    artifact_anchor = "## Machine Artifacts\n\n"
    artifact_block = (
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3871_ACTION_MEASURE_OWNER_THEOREM.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3871_ACTION_MEASURE_OWNER_AUDIT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_R2FR_3871_BJ_FIRST_SOURCE_ROW_CONTRACT.csv`\n"
        "- `source-intake\\mts_residuals\\P8_Y5_BRR545_3871_VALIDATION.csv`\n"
    )
    if artifact_anchor in text and "P8_Y5_R2FR_3871_ACTION_MEASURE_OWNER_THEOREM.csv" not in text:
        text = text.replace(artifact_anchor, artifact_anchor + artifact_block, 1)
    text = text.rstrip() + f"\n\n<!-- Generated by 3871 at {timestamp} -->\n"
    SPINE_PATH.write_text(text, encoding="utf-8")


def validation_rows(
    sources: list[dict[str, object]],
    theorem: list[dict[str, object]],
    owner_audit: list[dict[str, object]],
    bj_rows: list[dict[str, object]],
    refusal: list[dict[str, object]],
    gates: list[dict[str, object]],
    timestamp: str,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    def add(check_id: str, check: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "check_id": check_id,
                "check": check,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "timestamp_utc": timestamp,
            }
        )

    all_rows = theorem + owner_audit + bj_rows + refusal + gates
    add("VAL3871_0_sources", "all cited source paths exist and needles are found", all(row["exists"] and row["needle_found"] for row in sources), f"{sum(1 for row in sources if row['exists'] and row['needle_found'])}/{len(sources)} sources resolved")
    add("VAL3871_1_theorem", "conditional action-measure theorem is present", any(row["statement"] == THEOREM and row["result"] == "EXACT_CONDITIONAL_THEOREM" for row in theorem), THEOREM)
    add("VAL3871_2_owner_block", "owner package remains not derived", any(row["object"] == "owner package" and row["current_status"] == "OWNER_NOT_DERIVED" for row in owner_audit), "owner package blocked")
    add("VAL3871_3_rows", "first b_J source rows cover live terms", {"Delta_w_A", "beta_w_source", "beta_w_test", "J_A_measure", "c_A_pre", "kappa_A"} <= {row["symbol"] for row in bj_rows}, "finite source-row contract covers key terms")
    add("VAL3871_4_refusal", "scoring refusals remain active", all(not bool(row["claim_allowed"]) for row in refusal), "all local claim areas blocked")
    add("VAL3871_5_no_claim", "all generated rows remain nonclaim", all(not bool(row.get("valid_for_claim", row.get("claim_allowed", False))) for row in all_rows), "valid_for_claim/claim_allowed false throughout")
    add("VAL3871_6_next", "next target selects material/source map", DOC_PATH.exists() and "3872-Y5-R2FR-bJ-material-source-map-or-first-candidate-coefficient-rows" in read_text(DOC_PATH), "3872 target recorded")
    for key, output_path in OUTPUTS.items():
        if key == "validation":
            continue
        parsed = False
        detail = rel(output_path)
        if output_path.suffix == ".csv" and output_path.exists():
            count = len(read_csv_rows(output_path))
            parsed = count > 0
            detail += f" rows={count}"
        add(f"VAL3871_7_parse_{key}", f"{key} CSV parses cleanly", parsed, detail)
    add("VAL3871_8_doc", "markdown checkpoint document exists", DOC_PATH.exists() and "3871 closes the logical loop around" in read_text(DOC_PATH), rel(DOC_PATH))
    formalization_hits = []
    if FWB.exists():
        for pattern in ("P8_Y5_R2FR_3871*", "P8_Y5_BRR545_3871*", "*Y5_R2FR_3871*", "3871-Y5-R2FR*"):
            formalization_hits.extend(path for path in FWB.rglob(pattern) if path.is_file())
    add("VAL3871_9_formalization_clean", "formalization-workbench has no generated 3871 project files", len(formalization_hits) == 0, "; ".join(str(path) for path in formalization_hits) if formalization_hits else "no generated 3871 project file hits under formalization-workbench")
    pycache_hits = list((PCW / "scripts").rglob("__pycache__"))
    add("VAL3871_10_pycache_removed", "scripts __pycache__ removed", len(pycache_hits) == 0, "; ".join(str(path) for path in pycache_hits) if pycache_hits else "no __pycache__ directories")
    return rows


def main() -> int:
    timestamp = now_utc()
    OUT.mkdir(parents=True, exist_ok=True)

    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    owner_audit = owner_audit_rows(timestamp)
    bj_rows = bj_source_rows(timestamp)
    refusal = refusal_rows(timestamp)
    gates = gate_rows(sources, theorem, owner_audit, bj_rows, refusal, timestamp)
    decisions = decision_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["owner_audit"], owner_audit)
    write_csv(OUTPUTS["bj_source_rows"], bj_rows)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decisions"], decisions)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(sources, theorem, owner_audit, bj_rows, refusal, gates, decisions, next_target, timestamp)
    update_spine(timestamp)

    for pycache in (PCW / "scripts").rglob("__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)

    validation = validation_rows(sources, theorem, owner_audit, bj_rows, refusal, gates, timestamp)
    write_csv(OUTPUTS["validation"], validation)
    failed = [row for row in validation if row["status"] != "PASS"]
    if failed:
        for row in failed:
            print(f"FAIL {row['check_id']}: {row['detail']}")
        return 1
    print(f"{CHECKPOINT} PASS_ACTION_MEASURE_CONDITIONAL_SOURCE_ROWS")
    print(rel(DOC_PATH))
    print(rel(OUTPUTS["validation"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
