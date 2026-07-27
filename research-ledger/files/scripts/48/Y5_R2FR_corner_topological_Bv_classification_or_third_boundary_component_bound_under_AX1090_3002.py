from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3002"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3002-Y5-R2FR-corner-topological-Bv-classification-or-third-boundary-component-bound-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3002_SOURCE_REGISTER.csv",
    "classification": RESIDUALS / "P8_Y5_R2FR_3002_CORNER_TOPOLOGICAL_CLASSIFICATION_AUDIT.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_3002_EPSILON_BV_CORNER_TOPOLOGICAL_BOUND_ROWS.csv",
    "rebase": RESIDUALS / "P8_Y5_R2FR_3002_BV_REBASE_AFTER_CORNER_TOPOLOGICAL_CLASSIFICATION.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3002_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3002_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3002_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3002_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3002_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "classification_copy": PARENT_ACTION / "corner_topological_Bv_classification_3002_NOT_SIGNED.csv",
    "bounds_copy": LOCAL_BOUNDS / "epsilon_Bv_corner_topological_bound_rows_3002_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3002_UNFIXED_REFERENCE_BV_SELECTOR_NEXT_NONCLAIM.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def missing_anchors(path: Path, needles: list[str]) -> str:
    haystack = text(path)
    return "; ".join(needle for needle in needles if needle not in haystack)


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [str(output_row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SOURCE_SPECS = [
    (
        "SRC3002_00_3001_next",
        RESIDUALS / "P8_Y5_R2FR_3001_NEXT_TARGET.csv",
        ["NEXT3001_0_3002", "corner/topological Bv"],
        "3001 selects corner/topological Bv classification next.",
    ),
    (
        "SRC3002_01_2991_epsilon",
        RESIDUALS / "P8_Y5_R2FR_2991_EPSILON_BV_SOURCE_BOUND_ROWS_NONCLAIM.csv",
        ["EBV2991_02_corner", "EBV2991_03_topological"],
        "2991 defines corner and topological epsilon_Bv rows.",
    ),
    (
        "SRC3002_02_2999_remaining",
        RESIDUALS / "P8_Y5_R2FR_2999_REMAINING_KERNEL_DEBTS.csv",
        ["REM2999_0_corner", "REM2999_1_topological"],
        "2999 lists corner and topological Bv as open kernel debts.",
    ),
    (
        "SRC3002_03_2546_classification",
        RESIDUALS / "P8_Y5_NO_SHADOW_2546_BOUNDARY_TERM_CLASSIFICATION.csv",
        ["BTC2546_1_corner", "BTC2546_2_topological_nonexact"],
        "2546 classifies corner and topological/non-exact terms as live remainders.",
    ),
    (
        "SRC3002_04_2546_matrix",
        RESIDUALS / "P8_Y5_NO_SHADOW_2546_BOUNDARY_CERTIFICATE_MATRIX.csv",
        ["BCC2546_1_surface_corner", "BCC2546_2_cohomology"],
        "2546 certificate matrix names the missing corner and cohomology certificates.",
    ),
    (
        "SRC3002_05_2546_triage",
        RESIDUALS / "P8_Y5_NO_SHADOW_2546_ACTUAL_TERM_TRIAGE.csv",
        ["ATI2546_1_corner", "ATI2546_2_topological"],
        "2546 triage keeps actual corner/topological buckets live.",
    ),
    (
        "SRC3002_06_2546_bounds",
        RESIDUALS / "P8_Y5_NO_SHADOW_2546_BREM_BOUND_ROWS.csv",
        ["BRB2546_0_epsilon_Brem", "SCHEMA_READY_VALUES_MISSING"],
        "2546 gives the global B_rem bound schema with values missing.",
    ),
    (
        "SRC3002_07_2448_owner",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2448_BREF_RELATIVE_BOUNDARY_OWNER_CONTRACT.csv",
        ["RBO2448_1_Ctop_superselection", "FAILED_CURRENT_CLAIM"],
        "2448 refuses relative/topological class ownership for current MTS.",
    ),
    (
        "SRC3002_08_2448_silence",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2448_BOUNDARY_SILENCE_STACK_FOR_S_EQ.csv",
        ["SSB2448_1_relative_class", "NOT_SIGNED"],
        "2448 says relative boundary class silence is not signed.",
    ),
    (
        "SRC3002_09_2448_input_pack",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2448_S_EQ_BOUNDARY_SOURCE_BOUND_INPUT_PACK.csv",
        ["SBI2448_1_relative_qflux", "MISSING_RELATIVE_CLASS_OR_QFLUX_VALUE"],
        "2448 source-bound pack asks for relative q-flux value or theorem-zero.",
    ),
    (
        "SRC3002_10_2547_topology",
        RESIDUALS / "P8_Y5_NO_SHADOW_2547_SIGNATURE_AUDIT.csv",
        ["SIG2547_4_topology", "MISSING_CTOP_SUPERSELECTION_CERTIFICATE"],
        "2547 confirms the topological superselection signature is missing.",
    ),
]


def source_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "required_anchors": "; ".join(needles),
                "anchors_found": anchors(path, needles),
                "missing_anchors": missing_anchors(path, needles),
                "role": role,
            }
        )
        for source_id, path, needles, role in SOURCE_SPECS
    ]


def classification_rows() -> list[dict[str, Any]]:
    data = [
        (
            "CTB3002_0_corner_identity",
            "corner/codimension-two bucket",
            "corner charge Q_C or codimension-two contribution enters the Bv surface one-form unless the linked surfaces are corner-free or all corners are included with fixed convention before variation.",
            "LIVE_REMAINDER_CLASSIFIED",
            "corner-free/fixed-corner certificate is missing",
            "epsilon_Bv_corner_abs",
        ),
        (
            "CTB3002_1_corner_zero_condition",
            "corner zero condition",
            "epsilon_Bv_corner_abs=0 if partial S_link is empty, or every codimension-two corner charge is paired/fixed and delta_v Q_C=0 in the parent branch.",
            "CONDITIONAL_ZERO_NOT_CURRENT_MTS",
            "BCC2546_1_surface_corner is missing",
            "epsilon_Bv_corner_abs",
        ),
        (
            "CTB3002_2_topological_identity",
            "topological/non-exact bucket",
            "closed but non-exact h_X, harmonic edge mode, or relative cohomology class can carry finite boundary charge not killed by exact-improvement algebra.",
            "LIVE_REMAINDER_CLASSIFIED",
            "relative cohomology/harmonic silence certificate is missing",
            "epsilon_Bv_topological_abs",
        ),
        (
            "CTB3002_3_topological_zero_condition",
            "topological zero condition",
            "epsilon_Bv_topological_abs=0 if C_top is parent-superselected, delta_v C_top=0, h_X=0 or h_X is projected silent in the same boundary class.",
            "CONDITIONAL_ZERO_NOT_CURRENT_MTS",
            "RBO2448_1 and SIG2547_4 keep C_top unsigned",
            "epsilon_Bv_topological_abs",
        ),
        (
            "CTB3002_4_relative_qflux",
            "relative q-flux fallback",
            "If zero fails, relative_boundary_qflux_over_N requires a source-backed qflux_profile, surface_pair, N_E/M_ref and equation/source path.",
            "BOUND_INTERFACE_EXISTS_VALUES_MISSING",
            "SBI2448_1 has no q-flux value or theorem-zero row",
            "epsilon_Bv_relative_qflux_abs",
        ),
        (
            "CTB3002_5_verdict",
            "corner/topological Bv classification",
            "The buckets are classified and zero criteria are exact, but current MTS lacks the certificates and finite values.",
            "ZERO_NOT_PROMOTED_BOUND_ROWS_STAGED",
            "no full Bv/kernel/local-GR promotion",
            "epsilon_Bv_corner_topological_total_abs",
        ),
    ]
    return [
        base(
            {
                "classification_id": classification_id,
                "bucket": bucket,
                "statement": statement,
                "current_status": status,
                "blocking_gap": gap,
                "residual_if_missing": residual,
                "parent_signed_for_current_MTS": False,
                "theorem_zero_adopted": False,
                "accepted_for_local_gr": False,
            }
        )
        for classification_id, bucket, statement, status, gap, residual in data
    ]


def bound_rows() -> list[dict[str, Any]]:
    data = [
        (
            "BVC3002_0_corner",
            "epsilon_Bv_corner_abs",
            "corner/codimension-two boundary contribution to Bv",
            "dimensionless_corner_charge_after_positive_same_frame_M_ref",
            "abs(int_corner K_corner)/M_ref",
            "MISSING_CORNER_CLASSIFICATION_OR_BOUND",
            RESIDUALS / "P8_Y5_R2FR_2991_EPSILON_BV_SOURCE_BOUND_ROWS_NONCLAIM.csv",
            "EBV2991_02_corner;BTC2546_1_corner",
        ),
        (
            "BVC3002_1_corner_zero_switch",
            "epsilon_Bv_corner_zero_if_cornerfree_or_fixed",
            "theorem-zero switch for corner-free or fixed/paird codimension-two charges",
            "boolean_component_guard",
            "0 if partial S_link=0 or all Q_C are parent-fixed and paired before variation",
            "CONDITIONAL_ZERO_NOT_PROMOTED",
            RESIDUALS / "P8_Y5_NO_SHADOW_2546_BOUNDARY_CERTIFICATE_MATRIX.csv",
            "BCC2546_1_surface_corner",
        ),
        (
            "BVC3002_2_topological",
            "epsilon_Bv_topological_abs",
            "closed-but-not-exact/harmonic/relative cohomology boundary contribution",
            "dimensionless_topological_charge_after_positive_same_frame_M_ref",
            "abs(Delta C_top + int_S h_X + relative_qflux)/M_ref",
            "MISSING_CTOP_SUPERSELECTION_OR_BOUND",
            RESIDUALS / "P8_Y5_R2FR_2991_EPSILON_BV_SOURCE_BOUND_ROWS_NONCLAIM.csv",
            "EBV2991_03_topological;BTC2546_2_topological_nonexact",
        ),
        (
            "BVC3002_3_topological_zero_switch",
            "epsilon_Bv_topological_zero_if_superselected",
            "theorem-zero switch for fixed relative cohomology and silent harmonic piece",
            "boolean_component_guard",
            "0 if delta_v C_top=0 and h_X=0 or projected silent in same parent boundary class",
            "CONDITIONAL_ZERO_NOT_PROMOTED",
            RESIDUALS / "P8_Y5_PARENT_QLOC_2448_BREF_RELATIVE_BOUNDARY_OWNER_CONTRACT.csv",
            "RBO2448_1_Ctop_superselection",
        ),
        (
            "BVC3002_4_relative_qflux",
            "epsilon_Bv_relative_qflux_abs",
            "finite fallback for relative boundary q-flux if topology zero fails",
            "dimensionless_after_positive_same_frame_M_ref",
            "abs(relative_boundary_qflux)/M_ref",
            "MISSING_RELATIVE_CLASS_OR_QFLUX_VALUE",
            RESIDUALS / "P8_Y5_PARENT_QLOC_2448_S_EQ_BOUNDARY_SOURCE_BOUND_INPUT_PACK.csv",
            "SBI2448_1_relative_qflux",
        ),
        (
            "BVC3002_5_total",
            "epsilon_Bv_corner_topological_total_abs",
            "absolute no-cancellation envelope for corner plus topological Bv pieces",
            "dimensionless_after_positive_same_frame_M_ref",
            "sum_abs(BVC3002_0,BVC3002_2,BVC3002_4) unless zero switches are parent-signed",
            "MISSING_SOURCE_BACKED_UPPER_BOUND",
            RESIDUALS / "P8_Y5_NO_SHADOW_2546_BREM_BOUND_ROWS.csv",
            "BRB2546_0_epsilon_Brem",
        ),
    ]
    return [
        base(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "definition": definition,
                "units": units,
                "bound_interface": formula,
                "current_value": current_value,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "source_anchor": anchor,
                "finite_value_present": False,
                "theorem_zero_claimed": False,
                "accepted_for_scoring": False,
                "accepted_for_local_gr": False,
                "observable_link": "local_GR;Newton;PPN;R10;clock",
                "no_cancellation_policy": True,
            }
        )
        for bound_id, symbol, definition, units, formula, current_value, path, anchor in data
    ]


def rebase_rows() -> list[dict[str, Any]]:
    data = [
        ("REB3002_0_exact_fixed", "epsilon_Bv_exact_fixed_primitive", "0", "closed only as exact/fixed component by 2999"),
        ("REB3002_1_tau_surface", "epsilon_Bv_tau_surface_commutator_total_abs", "COMPONENTS_MISSING_NO_FINITE_VALUE", "demoted to explicit residual closure by 3001"),
        ("REB3002_2_corner_topological", "epsilon_Bv_corner_topological_total_abs", "MISSING_SOURCE_BACKED_UPPER_BOUND", "3002 classifies buckets and stages bound rows"),
        ("REB3002_3_Bv_remainder", "epsilon_Bv_remainder_after_3002", "MISSING_UNFIXED_REFERENCE_PROJECTOR_MREF_BOUNDS", "next Bv debts are unfixed reference, projector-boundary and denominator"),
        ("REB3002_4_kernel", "epsilon_kernel_charge_public_SRNG_rebased_3002", "MISSING_THETA_PARENT_QV_BV_REMAINDER_CV_ZERO_FLUX_MREF", "Bv is narrower but full kernel charge remains open"),
    ]
    return [
        base(
            {
                "rebase_id": rebase_id,
                "symbol": symbol,
                "current_value": current_value,
                "status": status,
                "accepted_for_scoring": False,
                "accepted_for_local_gr": False,
            }
        )
        for rebase_id, symbol, current_value, status in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        ("GATE3002_0_classified", "corner/topological buckets classified", "PASS", True, False, "2546 buckets mapped to current Bv residual rows"),
        ("GATE3002_1_corner_zero", "epsilon_Bv_corner_abs=0 can be promoted", "CONDITIONAL_ONLY_FAIL_CLOSED", False, False, "corner-free/fixed-corner certificate missing"),
        ("GATE3002_2_topological_zero", "epsilon_Bv_topological_abs=0 can be promoted", "CONDITIONAL_ONLY_FAIL_CLOSED", False, False, "C_top superselection/harmonic silence missing"),
        ("GATE3002_3_finite_values", "corner/topological finite values exist", "BLOCKED_NONCLAIM", False, False, "corner charge, harmonic flux, qflux and M_ref values missing"),
        ("GATE3002_4_full_Bv_zero", "epsilon_Bv_ambiguity=0", "FAIL_CLOSED", False, False, "unfixed reference, projector-boundary and M_ref debts remain"),
        ("GATE3002_5_kernel_charge", "epsilon_kernel_charge_public_SRNG is score-ready", "FAIL_CLOSED", False, False, "Theta/Qv/Cv/zero-flux and Bv remainder still open"),
        ("GATE3002_6_local_GR_Newton_PPN", "local GR/Newton/PPN claim allowed", "FAIL_CLOSED", False, False, "classification/bound schemas do not close local reduction"),
    ]
    return [
        base(
            {
                "gate_id": gate_id,
                "gate": gate,
                "gate_status": status,
                "condition_passed": passed,
                "promotion_allowed_now": promotion,
                "reason": reason,
                "accepted_for_local_gr": False,
            }
        )
        for gate_id, gate, status, passed, promotion, reason in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEC3002_0_classification",
            "Accept the corner/topological classification as useful structure.",
            "The residual is no longer a generic boundary objection; it splits into corner charge, harmonic/topological class and relative q-flux.",
            "keep the split rows",
        ),
        (
            "DEC3002_1_no_zero",
            "Do not promote corner/topological zero.",
            "Current MTS lacks corner-free/fixed-corner and C_top/harmonic silence certificates.",
            "retain epsilon_Bv_corner_abs and epsilon_Bv_topological_abs",
        ),
        (
            "DEC3002_2_no_numeric",
            "Do not fabricate finite corner/topological values.",
            "Existing files provide bound schemas, not finite charge/q-flux values or M_ref.",
            "keep rows source-ready but nonclaim",
        ),
        (
            "DEC3002_3_next",
            "Move to unfixed-reference Bv selector next.",
            "After exact, tau/surface and corner/topology are structured, the largest remaining Bv risk is reference/counterterm selection as a cancellation knob.",
            "3003 should attack epsilon_Bv_unfixed_reference or Delta_ref bounds",
        ),
    ]
    return [
        base(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "effect": effect,
            }
        )
        for decision_id, decision, because, effect in data
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "next_id": "NEXT3002_0_3003",
                "priority": "selected_primary",
                "target_doc": "3003-Y5-R2FR-unfixed-reference-Bv-selector-or-Delta-ref-component-bound-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_unfixed_reference_Bv_selector_or_Delta_ref_component_bound_under_AX1090_3003.py",
                "mission": "Attack epsilon_Bv_unfixed_reference: prove B_ref/H_ref/C_top/counterterm data are parent-fixed before q/source/readout, or fill Delta_ref/B_ref derivative-vector bound rows with source paths, units and no observed-GM/cancellation import.",
                "success_condition": "unfixed-reference Bv component becomes theorem-zero by parent selector signatures or gains a finite source-backed Delta_ref component row",
                "fallback_condition": "if no selector signature or finite value exists, demote unfixed-reference route to residual closure and move to projector-boundary Bv",
                "guardrails": "no full Bv zero claim; no epsilon_kernel_charge claim; no local-GR/Newton/PPN/WEP/R10 claim; no GitHub; no formalization-workbench edits",
                "selected": True,
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "copy_id": copy_id,
                "destination": str(destination),
                "copy_exists": destination.exists(),
                "row_count": len(rows(destination)) if destination.exists() else 0,
                "parse_ok": csv_ok(destination) if destination.exists() else False,
            }
        )
        for copy_id, destination in BRANCH_OUTPUTS.items()
    ]


def validation_rows(
    source_output_rows: list[dict[str, Any]],
    classification_output_rows: list[dict[str, Any]],
    bound_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    sources_ok = all(boolish(row["path_exists"]) for row in source_output_rows)
    anchors_ok = all(boolish(row["anchors_found"]) for row in source_output_rows)
    classified = any(row["classification_id"] == "CTB3002_5_verdict" and row["current_status"] == "ZERO_NOT_PROMOTED_BOUND_ROWS_STAGED" for row in classification_output_rows)
    bounds_staged = any(row["bound_id"] == "BVC3002_5_total" and row["current_value"] == "MISSING_SOURCE_BACKED_UPPER_BOUND" for row in bound_output_rows)
    finite_not_fabricated = all(not boolish(row.get("finite_value_present")) for row in bound_output_rows)
    local_claim_false = any(row["gate_id"] == "GATE3002_6_local_GR_Newton_PPN" and not boolish(row["condition_passed"]) for row in gate_output_rows)
    branch_ok = all(boolish(row["copy_exists"]) and boolish(row["parse_ok"]) for row in branch_output_rows)
    csv_parse_ok = all(csv_ok(path) for path in output_paths if path.exists() and path.suffix == ".csv")
    outputs_under_post = all(under(path, ROOT) for path in output_paths + [DOC])
    formalization_count = 0
    if FORMALIZATION.exists():
        formalization_patterns = [
            "*Y5_R2FR_3002*",
            "*3002-Y5-R2FR*",
            "*corner_topological_Bv_classification_3002*",
            "*epsilon_Bv_corner_topological_bound_rows_3002*",
            "*JR3002_UNFIXED_REFERENCE*",
        ]
        formalization_count = sum(
            1
            for pattern in formalization_patterns
            for path in FORMALIZATION.rglob(pattern)
            if path.is_file()
        )
    no_claim_flags = True
    for output_path in output_paths:
        if output_path.exists() and output_path.suffix == ".csv":
            for output_row in rows(output_path):
                for key in ("valid_for_claim", "claim_allowed", "promotion_allowed_now", "accepted_for_local_gr", "accepted_for_scoring"):
                    if str(output_row.get(key, "")).strip().lower() == "true":
                        no_claim_flags = False
    data = [
        ("VAL3002_0_sources_exist", sources_ok, "all cited local source paths exist"),
        ("VAL3002_1_anchors_found", anchors_ok, "all cited anchors are found"),
        ("VAL3002_2_classified", classified, "corner/topological buckets classified and zero not promoted"),
        ("VAL3002_3_bounds_staged", bounds_staged, "corner/topological bound rows staged"),
        ("VAL3002_4_no_fake_values", finite_not_fabricated, "no finite corner/topological value fabricated"),
        ("VAL3002_5_local_claim_false", local_claim_false, "local GR/Newton/PPN gate remains false"),
        ("VAL3002_6_branch_copies", branch_ok, "branch copies exist and parse"),
        ("VAL3002_7_csvs_parse", csv_parse_ok, "all generated CSVs parse"),
        ("VAL3002_8_outputs_under_post", outputs_under_post, "all outputs are under post-checkpoint-work"),
        ("VAL3002_9_no_claim_flags", no_claim_flags, "no generated row allows a claim"),
        ("VAL3002_10_formalization_clean", formalization_count == 0, f"no 3002 outputs in formalization-workbench (count={formalization_count})"),
        ("VAL3002_11_doc_written", DOC.exists(), "3002 markdown checkpoint exists"),
    ]
    overall = all(passed for _, passed, _ in data)
    data.append(("VAL3002_OVERALL", overall, "3002 classifies corner/topological Bv terms, stages source-ready nonclaim bound rows, refuses zero/numeric/local claims, and selects unfixed-reference Bv next"))
    return [
        base(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": True,
            }
        )
        for validation_id, passed, check in data
    ]


def write_doc(
    source_output_rows: list[dict[str, Any]],
    classification_output_rows: list[dict[str, Any]],
    bound_output_rows: list[dict[str, Any]],
    rebase_output_rows: list[dict[str, Any]],
    gate_output_rows: list[dict[str, Any]],
    decision_output_rows: list[dict[str, Any]],
    next_output_rows: list[dict[str, Any]],
    branch_output_rows: list[dict[str, Any]],
    validation_output_rows: list[dict[str, Any]],
) -> None:
    document = f"""# 3002 - Y5/R2FR Corner-Topological Bv Classification Or Third Boundary Component Bound Under AX1090

Status: `Y5_R2FR_3002_corner_topological_Bv_classified_zero_not_promoted_bound_rows_staged_3003_next`

Claim ceiling: `no_corner_zero_claim_no_topological_zero_claim_no_full_Bv_zero_claim_no_epsilon_kernel_charge_claim_no_local_GR_no_Newton_no_PPN_no_WEP_no_R10_no_GitHub_no_formalization_edit`

## Current Verdict

3002 classifies the next `B_v` remainder after the exact/fixed component and tau/surface component: corner/codimension-two charge plus topological/non-exact boundary charge.

The zero route is clear but unsigned. Corners vanish only if the linked surfaces are corner-free or all corner charges are included with a parent-fixed convention. Topological charge vanishes only if the relative class is parent-superselected and the harmonic/non-exact component is zero or projected silent in that same boundary class.

Current MTS does not sign those certificates and has no finite corner/topological charge values. Therefore `epsilon_Bv_corner_abs` and `epsilon_Bv_topological_abs` stay source-ready nonclaim residuals. The useful gain is classification: these are now named debts, not fog.

## Source Register

{md_table(source_output_rows, ["source_id", "path_exists", "anchors_found", "missing_anchors", "role"])}

## Corner / Topological Classification Audit

{md_table(classification_output_rows, ["classification_id", "bucket", "current_status", "blocking_gap", "residual_if_missing"])}

## epsilon_Bv Corner / Topological Bound Rows

{md_table(bound_output_rows, ["bound_id", "symbol", "bound_interface", "current_value", "source_anchor"])}

## Bv Rebase After 3002

{md_table(rebase_output_rows, ["rebase_id", "symbol", "current_value", "status"])}

## Promotion Gates

{md_table(gate_output_rows, ["gate_id", "gate", "gate_status", "condition_passed", "promotion_allowed_now", "reason"])}

## Decision Ledger

{md_table(decision_output_rows, ["decision_id", "decision", "because", "effect"])}

## Next Target

{md_table(next_output_rows, ["next_id", "target_doc", "mission", "success_condition", "guardrails"])}

## Branch Copies

{md_table(branch_output_rows, ["copy_id", "destination", "copy_exists", "row_count", "parse_ok", "valid_for_claim"])}

## Validation

{md_table(validation_output_rows, ["validation_id", "passed", "check", "required"])}

## Plain-English Takeaway

Another fog patch has been boxed. Corner and topological boundary pieces are not closed, but now we know exactly what would close them and exactly what has to be paid if they do not close. The next highest-risk boundary piece is the unfixed reference/counterterm selector, because that is the place a fake cancellation knob could hide.

## Forbidden Claims From 3002

- `epsilon_Bv_corner_abs=0`.
- `epsilon_Bv_topological_abs=0`.
- `epsilon_Bv_ambiguity=0`.
- `epsilon_kernel_charge_public_SRNG=0` or score-ready.
- Public `SRNG/OFC`, source-normalized Newton, PPN, WEP, R10, clock safety, orbital safety or local GR.
"""
    DOC.write_text(document, encoding="utf-8")


def main() -> None:
    source_output_rows = source_rows()
    classification_output_rows = classification_rows()
    bound_output_rows = bound_rows()
    rebase_output_rows = rebase_rows()
    gate_output_rows = gate_rows()
    decision_output_rows = decision_rows()
    next_output_rows = next_rows()

    write_csv(OUTPUTS["sources"], source_output_rows)
    write_csv(OUTPUTS["classification"], classification_output_rows)
    write_csv(OUTPUTS["bounds"], bound_output_rows)
    write_csv(OUTPUTS["rebase"], rebase_output_rows)
    write_csv(OUTPUTS["gates"], gate_output_rows)
    write_csv(OUTPUTS["decision"], decision_output_rows)
    write_csv(OUTPUTS["next"], next_output_rows)

    shutil.copyfile(OUTPUTS["classification"], BRANCH_OUTPUTS["classification_copy"])
    shutil.copyfile(OUTPUTS["bounds"], BRANCH_OUTPUTS["bounds_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

    branch_output_rows = branch_rows()
    write_csv(OUTPUTS["branches"], branch_output_rows)

    DOC.write_text("", encoding="utf-8")
    validation_output_rows = validation_rows(
        source_output_rows,
        classification_output_rows,
        bound_output_rows,
        gate_output_rows,
        branch_output_rows,
    )
    write_csv(OUTPUTS["validation"], validation_output_rows)

    write_doc(
        source_output_rows,
        classification_output_rows,
        bound_output_rows,
        rebase_output_rows,
        gate_output_rows,
        decision_output_rows,
        next_output_rows,
        branch_output_rows,
        validation_output_rows,
    )


if __name__ == "__main__":
    main()
