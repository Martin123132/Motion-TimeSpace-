from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1589"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1589-Y5-R2FR-parent-coefficient-source-hunt-or-curve-QA-promotion.md"

SOURCE_FILES = {
    "1588_doc": ROOT / "1588-Y5-R2FR-scalaron-coefficient-map-or-full-curve-bound-intake.md",
    "1588_validation": OUT / "P8_Y5_BRR545_1588_VALIDATION.csv",
    "1588_scalaron_map": OUT / "P8_Y5_PARENT_QLOC_1588_R2FR_SCALARON_MAP.csv",
    "1587_fill": OUT / "P8_Y5_PARENT_QLOC_1587_FIRST_COMPONENT_FILL_ROWS.csv",
    "r11_executable": OUT / "R11_nonEH_operator_vector_executable.csv",
    "r11_skeleton": OUT / "R11_MTS_MINIMUM_EXECUTABLE_VECTOR_SKELETON.csv",
    "local_eh_audit": OUT / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
    "1343_doc": ROOT / "1343-Y5-R10-RAB-R2FR-parent-coefficient-zero-signature-or-finite-scalar-map-fill.md",
    "1343_law": OUT / "P8_Y5_R10_1343_PARENT_COEFFICIENT_LAW.csv",
    "1343_finite_template": OUT / "P8_Y5_R10_1343_FINITE_SCALAR_MAP_TEMPLATE.csv",
    "1346_doc": ROOT / "1346-Y5-R10-RAB-memory-and-fibre-vertex-zero-or-symbolic-coefficient-fill.md",
    "1347_doc": ROOT / "1347-Y5-R10-RAB-memory-fibre-coefficient-owner-search-or-explicit-closure.md",
    "1347_owner_matrix": OUT / "P8_Y5_R10_1347_COEFFICIENT_OWNER_MATRIX.csv",
    "1348_doc": ROOT / "1348-Y5-R10-RAB-memory-branch-extremum-and-operator-signature-or-closure.md",
    "1349_doc": ROOT / "1349-Y5-R10-RAB-KMTS-trace-projection-owner-or-memory-closure-declaration.md",
    "1349_kmts": OUT / "P8_Y5_R10_1349_KMTS_TRACE_PROJECTION_OWNER_ATTEMPT.csv",
    "1349_declaration": OUT / "P8_Y5_R10_1349_MEMORY_CLOSURE_DECLARATION.csv",
    "1350_inputs": OUT / "P8_Y5_R10_1350_REQUIRED_INPUT_ROWS.csv",
    "1350_dryrun": OUT / "P8_Y5_R10_1350_RUNNER_DRY_RUN.csv",
    "review_candidate": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_1034_REVIEW_CANDIDATE_NONCLAIM.csv",
    "review_qa": LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CANDIDATE_QA.csv",
    "review_summary": LOCAL_BOUNDS / "P8_Y5_R10_570_REVIEW_CURVE_SUMMARY.csv",
    "live_digitized": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
}

NEEDLES = {
    "1588_doc": ["NEXT_1589_R2FR_PARENT_COEFFICIENT_SOURCE_HUNT_OR_CURVE_QA_PROMOTION", "SC1588_5_verdict"],
    "1588_validation": ["VAL1588_OVERALL", "PASS"],
    "1588_scalaron_map": ["SC1588_5_verdict", "FAIL_CURRENT_CLAIM_NO_SCALARON_PREDICTION"],
    "1587_fill": ["FC1587_0_R2FR", "MISSING_PARENT_COEFFICIENT_AND_FULL_CURVE"],
    "r11_executable": ["R2_fR_scalar_mode", "MISSING_NUMERIC_OR_DERIVED_ZERO_COEFFICIENT", "MISSING_COEFFICIENT_UNITS"],
    "r11_skeleton": ["R2_fR_scalar_mode", "retained_unfilled"],
    "local_eh_audit": ["R2_fR_scalar_mode", "missing_selector_or_coefficient"],
    "1343_doc": ["DERIVED_CONDITIONAL_COEFFICIENT_LAW", "ZERO_SIGNATURE_NOT_DERIVED_CURRENT_CORPUS"],
    "1343_law": ["LAW1343_0_quadratic_parent_block", "c_R2_eff"],
    "1343_finite_template": ["FSM1343_1_quadratic_fR_convention", "MISSING_SCREENING_REGIME"],
    "1346_doc": ["MEMORY_VERTEX_ZERO_NOT_DERIVED_SYMBOLIC_PACK_SELECTED", "COEFF1346_M_B", "COEFF1346_H_B"],
    "1347_doc": ["OWN1347_2_memory_branch_extremum", "PROMISING_CONDITIONAL_ROUTE_NOT_DERIVED"],
    "1347_owner_matrix": ["COWN1347_2_B_mem", "PROMISING_CONDITIONAL_ROUTE_NOT_DERIVED"],
    "1348_doc": ["B_MEM_ZERO_NOT_PARENT_OWNED_CURRENT_CORPUS", "NEXT1348_0_1349"],
    "1349_doc": ["KMTS_TRACE_PROJECTION_OWNER_NOT_DERIVED", "MDECL1349_1_private_closure_branch"],
    "1349_kmts": ["KMTS1349_5_verdict", "KMTS_TRACE_PROJECTION_OWNER_NOT_DERIVED"],
    "1349_declaration": ["MDECL1349_2_default_residual_branch", "DEFAULT_NONCLAIM_PUBLIC_DISCIPLINE"],
    "1350_inputs": ["REQ1350_0_Bmem", "SYMBOLIC_NONCLAIM_ONLY"],
    "1350_dryrun": ["DRY1350_4_future_complete_template", "WOULD_ACCEPT_IF_REAL_FILES_AND_VALUES_EXIST"],
    "review_candidate": ["R10_VECTOR_2020_REVIEW_0000", "review_candidate_only_requires_official_supplement_or_human_visual_QA"],
    "review_qa": ["QA570_2_promotion_gate", "blocked=2"],
    "review_summary": ["CS570_0_rows", "390"],
    "live_digitized": ["MISSING_DIGITIZED_ALPHA_BOUND", "R10_BOUND_PLACEHOLDER_0"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1589_SOURCE_REGISTER.csv"
COEFFICIENT_HUNT = OUT / "P8_Y5_PARENT_QLOC_1589_COEFFICIENT_SOURCE_HUNT.csv"
EFFECTIVE_LAW = OUT / "P8_Y5_PARENT_QLOC_1589_EFFECTIVE_COEFFICIENT_LAW.csv"
OWNER_STATUS = OUT / "P8_Y5_PARENT_QLOC_1589_MEMORY_FIBRE_OWNER_STATUS.csv"
CURVE_QA = OUT / "P8_Y5_PARENT_QLOC_1589_CURVE_QA_PROMOTION_GATE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1589_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1589_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1589_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1589_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1589_VALIDATION.csv"

COPY_TARGETS = {
    COEFFICIENT_HUNT: [
        QUARANTINE / "R2FR_COEFFICIENT_SOURCE_HUNT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_coefficient_source_hunt_nonclaim_1589.csv",
    ],
    EFFECTIVE_LAW: [
        QUARANTINE / "R2FR_EFFECTIVE_COEFFICIENT_LAW_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_effective_coefficient_law_nonclaim_1589.csv",
    ],
    OWNER_STATUS: [
        QUARANTINE / "R2FR_MEMORY_FIBRE_OWNER_STATUS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_memory_fibre_owner_status_nonclaim_1589.csv",
    ],
    CURVE_QA: [
        QUARANTINE / "R2FR_CURVE_QA_PROMOTION_GATE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_curve_QA_promotion_gate_nonclaim_1589.csv",
    ],
    RUNNER: [
        QUARANTINE / "R2FR_PARENT_COEFFICIENT_RUNNER_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_coefficient_runner_nonclaim_1589.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_parent_coefficient_or_curve_QA_decision_nonclaim_1589.csv",
    ],
}


def claim_flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def file_contains(path: Path, needles: list[str]) -> bool:
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    return all(needle in text for needle in needles)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def bool_text(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_index, (source_key, source_path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1589_{source_index}_{source_key}",
                "source_path": rel(source_path),
                "exists": source_path.exists(),
                "needle_found": file_contains(source_path, NEEDLES[source_key]),
                "needles": "; ".join(NEEDLES[source_key]),
                "purpose": "R2/fR parent coefficient source hunt or curve QA promotion gate",
                **claim_flags(),
            }
        )
    return rows


def coefficient_hunt_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "HUNT1589_0_R11_live_rows",
            "c_R2_or_c_fR",
            "R11 executable/skeleton/local EH audit",
            "R2_fR_scalar_mode exists but coefficient value, units, normalization and weak-field map are all missing.",
            "MISSING_PARENT_COEFFICIENT",
            "cannot build scalaron mass, lambda_s, alpha_s, beta/gamma residual or local-GR pass",
            "derive theorem-zero or fill real coefficient row with units and source path",
        ),
        (
            "HUNT1589_1_effective_law",
            "c_R2_eff(k)",
            "1343 coefficient law",
            "c_R2_eff(k)=c_bare+1/2 B^T L^-1(k)B+c_measure+c_boundary is derived symbolically.",
            "DERIVED_SYMBOLIC_LAW_NO_NUMERIC_INPUTS",
            "law tells us exactly what must be killed or sourced; it is not a prediction value",
            "attack c_bare, B_X, measure and boundary terms separately",
        ),
        (
            "HUNT1589_2_no_bare_R2",
            "c_bare",
            "1343 zero-signature attempt and local EH audit",
            "no parent clause proves the action excludes bare R^2/f(R)/R F(Box) R terms before reduction.",
            "UNSIGNED_NO_BARE_HIGHER_CURVATURE_CLAUSE",
            "bare term could source c_R2_eff directly",
            "derive parent operator-domain exclusion or retain c_bare as finite residual input",
        ),
        (
            "HUNT1589_3_memory_vertex",
            "B_mem",
            "1347/1348/1349/1350 memory chain",
            "F1/B_mem calculus is clean only under a Gamma_eff trace-projection ansatz; K_MTS/Gamma/Khat owner is not derived, so B_mem=0 is private closure only.",
            "B_MEM_ZERO_NOT_PARENT_OWNED",
            "cannot use memory branch-extremum as a public theorem-zero for R2/fR/local-GR",
            "derive Gamma_eff/Khat/Ploc owner bundle or keep finite B_mem row with units/bounds",
        ),
        (
            "HUNT1589_4_fibre_vertex",
            "B_h",
            "1346/1347 fibre rows",
            "fibre curvature vertex zero is exact only if a parent grammar/constraint is signed; current evidence is unsigned.",
            "FIBRE_CURVATURE_VERTEX_UNSIGNED",
            "integrating fibre fluctuations can generate R L_h^-1 R-like residuals",
            "prove hidden-visible coefficient typing or retain finite B_h row",
        ),
        (
            "HUNT1589_5_measure_boundary_frame",
            "c_measure;c_boundary;frame_transfer",
            "1343 tuning guard and 1587 field-redefinition escape",
            "measure/Jacobian, boundary/corner, and frame-transfer terms have no zero owner in the current source trail.",
            "MISSING_MEASURE_BOUNDARY_FRAME_OWNER",
            "a tuned cancellation is not allowed as a derivation",
            "source Ward/topological/redefinition identity or keep finite residual term",
        ),
        (
            "HUNT1589_6_curve_side",
            "R10 alpha(lambda) bound curve",
            "570 QA, 1588 curve intake and live bound file",
            "390 positive review-candidate rows exist, but the live claim curve remains placeholder and promotion requires official supplement or human visual QA.",
            "DATA_SIDE_NONCLAIM_SECONDARY_BLOCKER",
            "even a perfect curve cannot score without c_R2/fRR, lambda and alpha",
            "use curve only for smoke after prediction exists; do not backsolve coefficients",
        ),
        (
            "HUNT1589_7_verdict",
            "c_R2/fRR source hunt",
            "all registered coefficient sources",
            "no parent-owned theorem-zero, numeric coefficient, finite scalar source map, or claim-grade curve-scoring row was found.",
            "NO_CLAIM_READY_PARENT_COEFFICIENT_FOUND",
            "R2/fR remains an explicit retained residual branch, not a local-GR pass/fail claim",
            "next target must attack the Gamma/Khat/Ploc owner bundle or fill a finite coefficient row",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "hunt_id": hunt_id,
            "coefficient_or_clause": coefficient_or_clause,
            "source_basis": source_basis,
            "current_evidence": current_evidence,
            "status": status,
            "claim_effect": claim_effect,
            "next_action": next_action,
            "evidence_backed": True,
            "parent_signed": False,
            "numeric_value_present": False,
            **claim_flags(),
        }
        for hunt_id, coefficient_or_clause, source_basis, current_evidence, status, claim_effect, next_action in rows
    ]


def effective_law_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "LAW1589_0_integrated_hidden_modes",
            "c_R2_eff(k)=c_bare+1/2 B^T L^-1(k)B+c_measure+c_boundary",
            "derived symbolic law from 1343",
            "a hidden curvature-linear vertex generates R2/fR residual even when ordinary J_X vanishes",
            "DERIVED_CONDITIONAL_COEFFICIENT_LAW",
            "needs c_bare, B_X, L_X, measure and boundary owners before prediction",
        ),
        (
            "LAW1589_1_low_momentum_limit",
            "c_R2_eff ~= c_bare + sum_X B_X^2/(2 M_X^2)+c_measure+c_boundary",
            "massive-mode local expansion",
            "coefficient zero requires no curvature-linear vertex or exact identity cancellation",
            "SYMBOLIC_LOW_MOMENTUM_MAP_NO_NUMERIC_INPUTS",
            "needs sign/units and M_X^2/Z_X if retained as finite scalar",
        ),
        (
            "LAW1589_2_zero_signature",
            "Z_cR2=true only if c_bare=0, B_X=0, c_measure=0, c_boundary=0 and no frame-transfer residue",
            "tuning guard",
            "zero by cancellation is forbidden unless Ward/topological/field-redefinition identity owns it",
            "ZERO_SIGNATURE_REFINED_NOT_SIGNED",
            "B_mem and B_h are especially unresolved",
        ),
        (
            "LAW1589_3_scalaron_prediction",
            "m_s^2=1/(6 c_R2), lambda_s=sqrt(6 c_R2), alpha_s=1/3 only in simple unscreened metric f(R)",
            "1588 scalaron map plus 1343 convention",
            "formula is available but not an MTS prediction until c_R2/fRR and branch regime are sourced",
            "FORMULA_AVAILABLE_PARENT_COEFFICIENT_MISSING",
            "missing coefficient value, units, sign, normalization, screening and source path",
        ),
        (
            "LAW1589_4_finite_mode_generalization",
            "lambda_X=sqrt(Z_X/M_X^2); alpha_X depends on source/test charge and matter-frame normalization",
            "1343/1346 finite scalar template",
            "generic memory/fibre branch can be made executable only after coefficient and source maps exist",
            "FINITE_MAP_SHAPE_DERIVED_INPUTS_MISSING",
            "missing Z_X, M_X^2, B_X, C_X, boundary charge, screening and observable projection",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "law_id": law_id,
            "coefficient_law_or_formula": law,
            "source_basis": source_basis,
            "meaning": meaning,
            "status": status,
            "blocking_gap": blocking_gap,
            "evidence_backed": True,
            "parent_signed": False,
            "numeric_value_present": False,
            **claim_flags(),
        }
        for law_id, law, source_basis, meaning, status, blocking_gap in rows
    ]


def owner_status_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OWN1589_0_memory_operator",
            "Z_mem;M2_mem;lambda_mem",
            "memory action/operator scaffold exists, but parent adoption, signs, units and branch Hessian are not signed",
            "SCAFFOLD_FOUND_VALUES_MISSING",
            "derive memory sector action and second variation from parent grammar",
        ),
        (
            "OWN1589_1_memory_Bmem",
            "B_mem",
            "branch-extremum/F1 calculus is conditional; K_MTS trace-projection owner is not derived; default public discipline is finite symbolic residual",
            "PRIVATE_CLOSURE_OR_FINITE_RESIDUAL_ONLY",
            "derive Gamma_eff/Khat/Ploc response bundle or source finite B_mem units/value/bound",
        ),
        (
            "OWN1589_2_memory_source_boundary",
            "C_mem;J_mem;Q_boundary_mem",
            "matter/source/boundary silence is not derived, so memory no-hair cannot be claimed from positive operator alone",
            "MISSING_ZERO_OR_BOUND_CERTIFICATE",
            "prove matter blindness/source Ward/boundary no-hair or retain finite source charge",
        ),
        (
            "OWN1589_3_fibre_gap_vertex",
            "Z_h;M2_h;B_h;C_h;Q_boundary_h",
            "fibre finite branch lacks signed zero owner; B_h=0 depends on still-unsigned parent grammar/constraint",
            "FIBRE_OWNER_UNSIGNED",
            "derive hidden-visible typing theorem or finite fibre source/test charge map",
        ),
        (
            "OWN1589_4_response_bundle",
            "Gamma_eff;K_hat;P_loc;q_loc",
            "1350 runner contract rejects symbolic B_mem, Gamma-only rows and q_loc-zero axioms until the response bundle is sourced",
            "MISSING_GAMMA_KHAT_PLOC_OWNER",
            "derive one parent response density/tensor/projector bundle before any local residual score",
        ),
        (
            "OWN1589_5_owner_verdict",
            "R2/fR owner family",
            "memory and fibre give the right coefficient names, not claim-ready coefficient owners",
            "NO_CLAIM_READY_OWNER",
            "continue derivation-first; curve/data work remains secondary",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "owner_id": owner_id,
            "symbols": symbols,
            "evidence_summary": evidence_summary,
            "status": status,
            "next_action": next_action,
            "evidence_backed": True,
            "parent_signed": False,
            "numeric_value_present": False,
            **claim_flags(),
        }
        for owner_id, symbols, evidence_summary, status, next_action in rows
    ]


def curve_qa_rows() -> list[dict[str, Any]]:
    review_rows = read_csv(SOURCE_FILES["review_candidate"])
    live_rows = read_csv(SOURCE_FILES["live_digitized"])
    qa_rows = read_csv(SOURCE_FILES["review_qa"])
    summary_rows = read_csv(SOURCE_FILES["review_summary"])
    positive_numeric = all(
        float(row["lambda_value"]) > 0 and float(row["alpha_bound"]) > 0
        for row in review_rows
        if row.get("lambda_value") and row.get("alpha_bound")
    )
    claim_rows = [row for row in review_rows if bool_text(row.get("valid_for_claim"))]
    qa_blocked = any("blocked=2" in row.get("detail", "") for row in qa_rows)
    live_placeholder = any("MISSING_DIGITIZED_ALPHA_BOUND" in ",".join(row.values()) for row in live_rows)
    rows = [
        (
            "CURVEQA1589_0_review_candidate_shape",
            "390-row Eot-Wash 2020 vector review candidate",
            rel(SOURCE_FILES["review_candidate"]),
            len(review_rows),
            "positive_numeric_rows" if positive_numeric else "NON_POSITIVE_OR_MALFORMED_ROW",
            "REVIEW_CANDIDATE_AVAILABLE_NONCLAIM",
            "all candidate rows remain valid_for_claim=false; row_count from summary is "
            + next((row["value"] for row in summary_rows if row["summary_id"] == "CS570_0_rows"), "MISSING"),
        ),
        (
            "CURVEQA1589_1_promotion_gate",
            "review candidate promotion QA",
            rel(SOURCE_FILES["review_qa"]),
            len(qa_rows),
            "blocked=2" if qa_blocked else "promotion_gate_missing",
            "PROMOTION_BLOCKED",
            "requires official supplemental table or human visual QA before live claim file update",
        ),
        (
            "CURVEQA1589_2_live_claim_curve",
            "live digitized R10 bound curve",
            rel(SOURCE_FILES["live_digitized"]),
            len(live_rows),
            "placeholder_present" if live_placeholder else "unexpected_nonplaceholder",
            "LIVE_CURVE_NOT_CLAIM_GRADE",
            "live file still contains MISSING_DIGITIZED_ALPHA_BOUND placeholder rows",
        ),
        (
            "CURVEQA1589_3_claim_rows",
            "candidate valid_for_claim audit",
            rel(SOURCE_FILES["review_candidate"]),
            len(claim_rows),
            "claim_rows=0" if len(claim_rows) == 0 else f"claim_rows={len(claim_rows)}",
            "NO_CLAIM_ROWS_PROMOTED",
            "review candidate remains private pressure/smoke data only",
        ),
        (
            "CURVEQA1589_4_coefficient_dependency",
            "R10 score precondition",
            "MTS c_R2/fRR prediction row",
            0,
            "prediction_missing",
            "CURVE_QA_SECONDARY_TO_COEFFICIENT_OWNER",
            "without alpha_predicted and lambda_predicted, curve promotion cannot test MTS",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "curve_gate_id": gate_id,
            "gate": gate,
            "path_or_required_source": path_or_source,
            "row_count": row_count,
            "qa_observation": observation,
            "status": status,
            "notes": notes,
            "evidence_backed": True,
            **claim_flags(),
        }
        for gate_id, gate, path_or_source, row_count, observation, status, notes in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN1589_0_parent_source_hunt",
            "search current parent coefficient rows",
            "NO_CLAIM_READY_COEFFICIENT_FOUND",
            "R11 row, 1343 law, memory/fibre owners and 1350 residual contract all remain missing theorem-zero or numeric source inputs",
            False,
        ),
        (
            "RUN1589_1_zero_theorem",
            "c_R2/fRR theorem-zero branch",
            "REJECTED_ZERO_SIGNATURE_UNSIGNED",
            "no-bare-R2, B_mem/B_h, measure/boundary and frame-transfer clauses are not all parent-signed",
            False,
        ),
        (
            "RUN1589_2_finite_scalaron_prediction",
            "build alpha/lambda row",
            "REJECTED_MISSING_PARENT_PREDICTION",
            "c_R2/fRR value, units, sign, screening regime and source path are absent",
            False,
        ),
        (
            "RUN1589_3_curve_QA_promotion",
            "promote 390-row review candidate to live claim curve",
            "REJECTED_PROMOTION_GATE_BLOCKED",
            "candidate has positive numeric rows but still requires official supplement or human visual QA",
            False,
        ),
        (
            "RUN1589_4_anchor_backsolve",
            "infer c_R2/fRR from R10 alpha=1 thresholds",
            "FORBIDDEN_BACKSOLVE_REJECTED",
            "bound anchors constrain external parameter space; they do not derive MTS parent coefficients",
            False,
        ),
        (
            "RUN1589_5_Bmem_private_closure",
            "use B_mem=0 closure as local-GR/R10 pass",
            "FORBIDDEN_PRIVATE_CLOSURE_AS_CLAIM",
            "1349 declares B_mem=0 private closure only unless K_MTS/Gamma/Khat response owner is later derived",
            False,
        ),
        (
            "RUN1589_6_future_complete_template",
            "future fully sourced row",
            "WOULD_ACCEPT_IF_REAL_VALUES_AND_FILES_EXIST",
            "requires theorem-zero or numeric coefficient, explicit units, source path, observable map and claim-grade bound source",
            False,
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "case": case,
            "status": status,
            "reason": reason,
            "can_score": can_score,
            **claim_flags(),
        }
        for runner_id, case, status, reason, can_score in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "GATE1589_0_cR2_zero",
            "c_R2/fRR theorem-zero",
            "BLOCKED_NO_CLAIM",
            "effective coefficient law has unsigned no-bare, B_X, measure, boundary and frame-transfer clauses",
        ),
        (
            "GATE1589_1_scalaron_prediction",
            "finite R2/fR alpha/lambda prediction",
            "BLOCKED_NO_CLAIM",
            "no parent-owned c_R2/fRR value, units, sign, normalization, screening or source path",
        ),
        (
            "GATE1589_2_full_curve",
            "claim-grade R10 full bound curve",
            "BLOCKED_NO_CLAIM",
            "390-row candidate is nonclaim and live curve remains placeholder",
        ),
        (
            "GATE1589_3_R10_score",
            "R10 alpha(lambda) comparison",
            "BLOCKED_NO_CLAIM",
            "both MTS prediction and claim-grade curve are missing",
        ),
        (
            "GATE1589_4_Bmem_zero",
            "B_mem=0 local branch",
            "BLOCKED_NO_CLAIM",
            "K_MTS/Gamma/Khat/P_loc owner bundle is not derived; private closure cannot score",
        ),
        (
            "GATE1589_5_local_GR_beta",
            "R11 beta/local-GR promotion",
            "BLOCKED_NO_CLAIM",
            "R2/fR residual is not theorem-zero or bounded; cannot promote local GR from formula-only rows",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **claim_flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1589_0_progress",
            "COEFFICIENT_LAW_IS_REAL_PROGRESS",
            "1343/1589 put the R2/fR problem in exact coefficient language: c_bare, B^T L^-1 B, measure, boundary and frame-transfer terms.",
            "we now know what to derive rather than hand-waving around scalar hair",
        ),
        (
            "DEC1589_1_blocker",
            "PARENT_COEFFICIENT_OWNER_STILL_MISSING",
            "no current source gives theorem-zero or numeric c_R2/fRR; B_mem=0 is private closure only after 1349.",
            "R2/fR remains retained residual pressure, not a local-GR pass",
        ),
        (
            "DEC1589_2_data",
            "R10_CURVE_QA_IS_SECONDARY",
            "390 review-candidate rows exist but are nonclaim, and the live curve is placeholder.",
            "do not spend main effort on curve promotion until MTS has alpha/lambda prediction",
        ),
        (
            "DEC1589_3_next",
            "NEXT_1590_GAMMA_KHAT_PLOC_OWNER_OR_FINITE_CR2_ROW",
            "the best route is to derive the one parent response bundle that can own Gamma_eff, Khat and P_loc; if that fails, fill finite c_R2/fRR/B_mem rows with units and source paths.",
            "derive owner bundle first; no private closure, no anchor backsolve, no R10 score yet",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "consequence": consequence,
            **claim_flags(),
        }
        for decision_id, decision, reason, consequence in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1590-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-finite-coefficient-row.md",
            "script": "scripts/Y5_R2FR_Gamma_Khat_Ploc_owner_bundle_or_cR2_finite_coefficient_row.py",
            "objective": "derive a parent-owned Gamma_eff/K_hat/P_loc response bundle that theorem-zeros the R2/fR effective coefficient, or create a finite c_R2/fRR/B_mem coefficient row with units, signs, source paths and observable maps",
            "success_condition": "source-backed theorem-zero or complete nonclaim finite coefficient row ready for later R10/PPN/clock/orbital comparison",
            "do_not": "do not use B_mem=0 as public theorem, do not backsolve from R10 anchors, do not score review-candidate curves as claims",
            **claim_flags(),
        }
    ]


def copy_outputs() -> None:
    for source_path, target_paths in COPY_TARGETS.items():
        for target_path in target_paths:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def generated_claim_flags_false(generated_csvs: list[Path]) -> bool:
    flag_columns = {"score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"}
    for csv_path in generated_csvs:
        for row in read_csv(csv_path):
            for flag_column in flag_columns.intersection(row):
                if row[flag_column] != "False":
                    return False
    return True


def formalization_scope_clean(generated_csvs: list[Path]) -> bool:
    if any(FORMALIZATION in csv_path.parents for csv_path in generated_csvs):
        return False
    try:
        result = subprocess.run(
            ["git", "-C", str(ROOT.parent), "status", "--short", "--", "formalization-workbench"],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return True
    if result.returncode != 0:
        return True
    return len([line for line in result.stdout.splitlines() if line.strip()]) == 0


def has_1589_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1589" in csv_path.name for csv_path in folder.glob("*.csv"))


def review_candidate_positive_nonclaim() -> bool:
    rows = read_csv(SOURCE_FILES["review_candidate"])
    if len(rows) != 390:
        return False
    for row in rows:
        try:
            if float(row["lambda_value"]) <= 0 or float(row["alpha_bound"]) <= 0:
                return False
        except (KeyError, ValueError):
            return False
        if bool_text(row.get("valid_for_claim")):
            return False
    return True


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    hunt = read_csv(COEFFICIENT_HUNT)
    laws = read_csv(EFFECTIVE_LAW)
    owners = read_csv(OWNER_STATUS)
    curves = read_csv(CURVE_QA)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    required_claims = {
        "c_R2/fRR theorem-zero",
        "finite R2/fR alpha/lambda prediction",
        "claim-grade R10 full bound curve",
        "R10 alpha(lambda) comparison",
        "B_mem=0 local branch",
        "R11 beta/local-GR promotion",
    }
    checks = [
        ("VAL1589_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1589 source paths exist"),
        ("VAL1589_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all 1589 source needles found"),
        (
            "VAL1589_2_hunt_verdict_blocks",
            any(row["hunt_id"] == "HUNT1589_7_verdict" and row["status"] == "NO_CLAIM_READY_PARENT_COEFFICIENT_FOUND" for row in hunt),
            "source hunt finds no parent-owned c_R2/fRR theorem-zero or numeric coefficient",
        ),
        (
            "VAL1589_3_effective_law_written",
            any(row["law_id"] == "LAW1589_0_integrated_hidden_modes" and "c_R2_eff(k)" in row["coefficient_law_or_formula"] for row in laws)
            and any(row["law_id"] == "LAW1589_2_zero_signature" and row["status"] == "ZERO_SIGNATURE_REFINED_NOT_SIGNED" for row in laws),
            "effective coefficient law and zero-signature guard are written",
        ),
        (
            "VAL1589_4_bmem_closure_not_claim",
            any(row["owner_id"] == "OWN1589_1_memory_Bmem" and row["status"] == "PRIVATE_CLOSURE_OR_FINITE_RESIDUAL_ONLY" for row in owners)
            and any(row["owner_id"] == "OWN1589_4_response_bundle" and row["status"] == "MISSING_GAMMA_KHAT_PLOC_OWNER" for row in owners),
            "B_mem=0 remains private closure unless Gamma/Khat/Ploc owner is derived",
        ),
        (
            "VAL1589_5_curve_candidate_nonclaim",
            review_candidate_positive_nonclaim()
            and any(row["curve_gate_id"] == "CURVEQA1589_0_review_candidate_shape" and row["row_count"] == "390" for row in curves)
            and any(row["curve_gate_id"] == "CURVEQA1589_2_live_claim_curve" and row["status"] == "LIVE_CURVE_NOT_CLAIM_GRADE" for row in curves),
            "390-row review candidate is positive numeric but nonclaim; live curve remains placeholder",
        ),
        (
            "VAL1589_6_runner_rejects",
            all(row["can_score"] == "False" for row in runner)
            and any(row["runner_id"] == "RUN1589_4_anchor_backsolve" and row["status"] == "FORBIDDEN_BACKSOLVE_REJECTED" for row in runner)
            and any(row["runner_id"] == "RUN1589_6_future_complete_template" and row["status"] == "WOULD_ACCEPT_IF_REAL_VALUES_AND_FILES_EXIST" for row in runner),
            "runner rejects current rows and documents future accept template only",
        ),
        (
            "VAL1589_7_claim_gates_closed",
            {row["claim"] for row in gates} == required_claims
            and all(row["claim_allowed"] == "False" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates),
            "all 1589 claim gates remain closed",
        ),
        (
            "VAL1589_8_decision_next",
            any(row["decision"] == "NEXT_1590_GAMMA_KHAT_PLOC_OWNER_OR_FINITE_CR2_ROW" for row in decisions),
            "decision selects Gamma/Khat/Ploc owner or finite coefficient row next",
        ),
        ("VAL1589_9_csv_parse", all(len(read_csv(csv_path)) > 0 for csv_path in generated_csvs), "all generated 1589 CSVs parse cleanly"),
        ("VAL1589_10_claim_flags_false", generated_claim_flags_false(generated_csvs), "all generated score/prediction/claim flags remain false"),
        ("VAL1589_11_no_raw_accepted", not has_1589_rows(RAB_RAW) and not has_1589_rows(RAB_ACCEPTED), "no 1589 rows written to raw/accepted finite directories"),
        ("VAL1589_12_branch_copies", all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths), "branch/quarantine nonclaim copies written"),
        ("VAL1589_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1589_14_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1589 paths are outside formalization-workbench; git status is clean when available"),
    ]
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if passed else "FAIL",
            "detail": detail,
        }
        for check_id, passed, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1589_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1589 R2/fR parent coefficient source hunt or curve QA promotion validation",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join(["---"] * len(columns)) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def write_doc(
    sources: list[dict[str, Any]],
    hunt: list[dict[str, Any]],
    laws: list[dict[str, Any]],
    owners: list[dict[str, Any]],
    curves: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1589 - R2/fR Parent Coefficient Source Hunt Or Curve QA Promotion",
                "## Verdict\n"
                "- The hunt did not find a parent-owned `c_R2/fRR` theorem-zero or numeric coefficient. That is the live bottleneck.\n"
                "- The useful win is sharper: `c_R2_eff(k)=c_bare+1/2 B^T L^-1(k)B+c_measure+c_boundary`, so the R2/fR branch now has an exact coefficient target rather than a vague scalar-hair worry.\n"
                "- `B_mem=0` remains mathematically tempting but only private closure: the `K_MTS`/`Gamma_eff`/`K_hat`/`P_loc` owner bundle is not derived.\n"
                "- The 390-row R10 review candidate is positive numeric but still nonclaim; the live curve remains placeholder, and curve promotion is secondary until MTS has an alpha/lambda prediction.\n"
                "- No R2/fR, R10, beta, EH, Newton, PPN, local-GR, WEP, clock, orbital, conservation or common-matter claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## Coefficient Source Hunt",
                md_table(hunt, ["hunt_id", "coefficient_or_clause", "source_basis", "current_evidence", "status", "next_action"]),
                "## Effective Coefficient Law",
                md_table(laws, ["law_id", "coefficient_law_or_formula", "source_basis", "meaning", "status", "blocking_gap"]),
                "## Memory And Fibre Owner Status",
                md_table(owners, ["owner_id", "symbols", "evidence_summary", "status", "next_action"]),
                "## Curve QA Promotion Gate",
                md_table(curves, ["curve_gate_id", "gate", "path_or_required_source", "row_count", "qa_observation", "status", "notes"]),
                "## Runner",
                md_table(runner, ["runner_id", "case", "status", "reason", "can_score"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "consequence"]),
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "## Next Target",
                md_table(next_rows, ["next_target", "script", "objective", "success_condition", "do_not"]),
            ]
        )
        + "\n",
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    hunt = coefficient_hunt_rows()
    laws = effective_law_rows()
    owners = owner_status_rows()
    curves = curve_qa_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        COEFFICIENT_HUNT,
        EFFECTIVE_LAW,
        OWNER_STATUS,
        CURVE_QA,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(COEFFICIENT_HUNT, hunt)
    write_csv(EFFECTIVE_LAW, laws)
    write_csv(OWNER_STATUS, owners)
    write_csv(CURVE_QA, curves)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, hunt, laws, owners, curves, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
