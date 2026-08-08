from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from R10_alpha_lambda_bound_prediction_runner import run_runner


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RUN_ROOT = ROOT / "runs" / "3436-R10-alpha-lambda-bound-prediction-runner"
DOC = ROOT / "3436-Y5-R2FR-R10-alpha-lambda-runner-real-curve-or-q_loc-range-zero-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3435": ROOT / "3435-Y5-R2FR-first-score-ready-source-normalization-residual-runner-or-zero-row-under-AX1090.md",
    "next_3435": OUT / "P8_Y5_R2FR_3435_NEXT_TARGET.csv",
    "radial_runner_3435": OUT / "P8_Y5_R2FR_3435_RADIAL_SOURCE_HAIR_RESIDUAL_RUNNER.csv",
    "radial_zero_3435": OUT / "P8_Y5_R2FR_3435_RADIAL_MHREF_ZERO_THEOREM.csv",
    "qloc_owner_3432": OUT / "P8_Y5_R2FR_3432_QLOC_HILBERT_OWNER_THEOREM.csv",
    "qloc_decomposition_3432": OUT / "P8_Y5_R2FR_3432_QLOC_RESIDUAL_DECOMPOSITION.csv",
    "qloc_bound_3432": OUT / "P8_Y5_R2FR_3432_QLOC_RESIDUAL_BOUND_PACK.csv",
    "qloc_ppn_r10_3432": OUT / "P8_Y5_R2FR_3432_QLOC_PPN_R10_OPERATOR_UPDATE.csv",
    "ppn_stack_3434": OUT / "P8_Y5_R2FR_3434_FIRST_PPN_RESIDUAL_STACK.csv",
    "positive_x_nohair_1042": OUT / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv",
    "qloc_bound_runner_spec": OUT / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
    "r10_kernel_3013": OUT / "P8_Y5_R2FR_3013_R10_KERNEL_DERIVATION.csv",
    "r10_prediction_template_3013": OUT / "P8_Y5_R2FR_3013_R10_PREDICTION_ROW_TEMPLATE.csv",
    "r10_demotion_3014": OUT / "P8_Y5_R2FR_3014_R10_FINITE_RANGE_DEMOTION_LEDGER.csv",
    "r10_anchor_rows_2935": OUT / "P8_Y5_R2FR_2935_R10_SOURCE_BACKED_ANCHOR_ROWS.csv",
    "r10_machine_qa_2936": OUT / "P8_Y5_R2FR_2936_R10_REVIEW_CANDIDATE_MACHINE_QA.csv",
    "r10_reviewed_candidate_1572": OUT / "P8_Y5_PARENT_QLOC_1572_R10_ALPHA_LAMBDA_REVIEWED_CANDIDATE.csv",
    "r10_curve_status_1689": OUT / "P8_Y5_PARENT_QLOC_1689_R10_CURVE_DIGITIZATION_STATUS.csv",
    "r10_reconciliation_1690": OUT / "P8_Y5_PARENT_QLOC_1690_R10_CURVE_STATUS_RECONCILIATION.csv",
    "r10_bound_rows_3012": OUT / "P8_Y5_R2FR_3012_R10_BOUND_ROWS_NONCLAIM.csv",
    "r10_dryrun_3012": OUT / "P8_Y5_R2FR_3012_R10_DRYRUN_RESULTS.csv",
    "live_bound_curve": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv",
    "anchor_smoke_bound_curve": LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_ANCHOR_SMOKE.csv",
    "live_mts_curve": OUT / "R10_alpha_lambda_curve_MTS_source_normalization.csv",
    "smoke_mts_curve": OUT / "R10_alpha_lambda_curve_MTS_SMOKE_NONCLAIM.csv",
    "r10_runner": ROOT / "scripts" / "R10_alpha_lambda_bound_prediction_runner.py",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3436_SOURCE_REGISTER.csv",
    "qloc_range_zero_audit": OUT / "P8_Y5_R2FR_3436_QLOC_RANGE_ZERO_AUDIT.csv",
    "bound_curve_asset_audit": OUT / "P8_Y5_R2FR_3436_R10_BOUND_CURVE_ASSET_AUDIT.csv",
    "alpha_lambda_runner_contract": OUT / "P8_Y5_R2FR_3436_ALPHA_LAMBDA_RUNNER_CONTRACT.csv",
    "mts_alpha_source_map_status": OUT / "P8_Y5_R2FR_3436_MTS_ALPHA_SOURCE_MAP_STATUS.csv",
    "existing_runner_dryrun": OUT / "P8_Y5_R2FR_3436_EXISTING_RUNNER_DRYRUN.csv",
    "r10_score_readiness": OUT / "P8_Y5_R2FR_3436_R10_SCORE_READINESS.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3436_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3436_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3436_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3436_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3436_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def truthy(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def positive_float(value: Any) -> bool:
    try:
        return float(str(value)) > 0.0
    except ValueError:
        return False


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3435": "immediate 3435 handoff",
        "next_3435": "declares 3436 R10/range target",
        "radial_runner_3435": "radial residual runner feeding alpha(lambda)",
        "radial_zero_3435": "conditional M_H_ref radial zero theorem",
        "qloc_owner_3432": "q_loc Hilbert-owner zero contract",
        "qloc_decomposition_3432": "q_loc defect decomposition",
        "qloc_bound_3432": "q_loc bound-pack inputs",
        "qloc_ppn_r10_3432": "q_loc PPN/R10 operator rows",
        "ppn_stack_3434": "R10 range row in first PPN residual stack",
        "positive_x_nohair_1042": "positive-operator no-hair theorem target",
        "qloc_bound_runner_spec": "existing q_loc numeric-proxy/bound spec",
        "r10_kernel_3013": "Yukawa alpha(lambda) kernel contract",
        "r10_prediction_template_3013": "MTS alpha prediction row template",
        "r10_demotion_3014": "finite-range demotion/revival conditions",
        "r10_anchor_rows_2935": "source-backed anchor rows",
        "r10_machine_qa_2936": "machine QA for reviewed candidate curve",
        "r10_reviewed_candidate_1572": "reviewed internal candidate curve points",
        "r10_curve_status_1689": "curve readiness ledger",
        "r10_reconciliation_1690": "curve status reconciliation",
        "r10_bound_rows_3012": "nonclaim R10 bound rows",
        "r10_dryrun_3012": "prior R10 dry-run blocker result",
        "live_bound_curve": "live invalid placeholder bound curve",
        "anchor_smoke_bound_curve": "anchor-only nonclaim smoke bound file",
        "live_mts_curve": "live invalid MTS alpha template",
        "smoke_mts_curve": "symbolic MTS alpha smoke file",
        "r10_runner": "existing R10 comparator reused as guardrail",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "valid_for_claim": False,
        }
        for source_id, path in SOURCES.items()
    ]


def qloc_range_zero_audit() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "RZ3436_0_operator_identity",
            "zero_clause": "Put each finite-range local residual into L_X X = J_X with L_X self-adjoint on the compact exterior.",
            "derived_or_required_formula": "L_X=-nabla_i(Z_X^{ij} nabla_j .)+M_X^2+positive_mix",
            "current_evidence": "NH1042_0 and NH1042_1 provide the formal positive-operator setup.",
            "status": "CONDITIONAL_MATH_AVAILABLE_PARENT_SELECTION_MISSING",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "clause_id": "RZ3436_1_energy_identity",
            "zero_clause": "Multiply by X and integrate over the source-free annulus.",
            "derived_or_required_formula": "int_A[Z_X nabla X nabla X + M_X^2 X^2 + positive_mix] = int_A X J_X + Phi_boundary",
            "current_evidence": "This is the exact no-hair identity already present in NH1042_1.",
            "status": "DERIVED_CONDITIONAL_NONCLAIM",
            "blocks_zero_claim": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "RZ3436_2_positive_gap",
            "zero_clause": "The left side is strictly positive except at X=0.",
            "derived_or_required_formula": "Z_X >= Z_min > 0 and M_X^2 >= m_min^2 > 0, with no gauge/topological zero mode",
            "current_evidence": "NH1042 states this as a premise, but no parent-owned Z_X/M_X^2 row signs it channelwise for q_loc.",
            "status": "UNSIGNED_PARENT_INPUT",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "clause_id": "RZ3436_3_source_current_silence",
            "zero_clause": "No compact-source current drives the finite-range mode.",
            "derived_or_required_formula": "J_X = delta S_matter/delta X = 0 in the same source frame used by M_H_ref and tau_R10",
            "current_evidence": "The existing MTS alpha template still misses K_X, Qbar_XH, qbar_XT, tau_R10 and q_loc-to-Yukawa map.",
            "status": "MISSING_COUPLING_MAP",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "clause_id": "RZ3436_4_boundary_projector_silence",
            "zero_clause": "Boundary, projector and representative choices cannot inject an exterior profile.",
            "derived_or_required_formula": "Phi_boundary=0, [P_loc,nabla]T_GK=0, and no representative Weyl/disformal tail",
            "current_evidence": "3431/3432 keep projector and boundary defects as explicit residuals.",
            "status": "UNSIGNED_BOUNDARY_AND_PROJECTOR_CLAUSES",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "clause_id": "RZ3436_5_zero_conclusion",
            "zero_clause": "If all clauses above close, then the finite-range field and its alpha(lambda) row vanish.",
            "derived_or_required_formula": "J_X=0 and Phi_boundary=0 and positive L_X => X=0 => alpha_X(lambda)=0",
            "current_evidence": "Conditional theorem is sharp, but current corpus lacks the parent-signed coupling/source clauses.",
            "status": "ZERO_THEOREM_CONDITIONAL_NOT_CLAIMED",
            "blocks_zero_claim": True,
            "valid_for_claim": False,
        },
        {
            "clause_id": "RZ3436_6_bound_if_not_zero",
            "zero_clause": "If any clause fails, the residual must be bounded by a Yukawa/R10 operator, not hidden inside G0.",
            "derived_or_required_formula": "alpha_q(lambda;r)=|a_q/a_N| exp(r/lambda)/(1+r/lambda), then compare to alpha_bound(lambda)",
            "current_evidence": "KDER3013_1 gives the acceleration response; runner still lacks q_loc profile/source map and real claim curve.",
            "status": "BOUND_ROUTE_SELECTED_NONCLAIM",
            "blocks_zero_claim": False,
            "valid_for_claim": False,
        },
    ]


def bound_curve_asset_audit() -> list[dict[str, Any]]:
    candidate_rows = read_csv(SOURCES["r10_reviewed_candidate_1572"])
    anchor_rows = read_csv(SOURCES["r10_anchor_rows_2935"])
    live_bound_rows = read_csv(SOURCES["live_bound_curve"])
    smoke_bound_rows = read_csv(SOURCES["anchor_smoke_bound_curve"])
    candidate_numeric_rows = [
        row
        for row in candidate_rows
        if positive_float(row.get("lambda_m")) and positive_float(row.get("alpha_abs_bound"))
    ]
    candidate_source_backed_rows = [row for row in candidate_rows if truthy(row.get("source_backed"))]
    candidate_claim_rows = [row for row in candidate_rows if truthy(row.get("valid_for_claim"))]
    source_image = ROOT / "source-intake" / "rab-sector" / "external" / "r10" / "1570" / "extracted_images" / "page_5_image_1_Im3.png"
    overlay_image = ROOT / "source-intake" / "rab-sector" / "external" / "r10" / "1571" / "R10_fig2_blue_curve_cleaned_trace_overlay_1571.png"
    return [
        {
            "asset_id": "RCA3436_0_live_digitized_file",
            "asset": rel(SOURCES["live_bound_curve"]),
            "row_count": len(live_bound_rows),
            "positive_numeric_rows": sum(
                1
                for row in live_bound_rows
                if positive_float(row.get("lambda_value")) and positive_float(row.get("alpha_bound"))
            ),
            "source_backed_rows": 0,
            "valid_for_claim_rows": sum(1 for row in live_bound_rows if truthy(row.get("valid_for_claim"))),
            "status": "LIVE_PLACEHOLDER_INVALID",
            "claim_use": "forbidden",
            "valid_for_claim": False,
        },
        {
            "asset_id": "RCA3436_1_source_backed_anchors",
            "asset": rel(SOURCES["r10_anchor_rows_2935"]),
            "row_count": len(anchor_rows),
            "positive_numeric_rows": sum(
                1
                for row in anchor_rows
                if positive_float(row.get("lambda_m")) and positive_float(row.get("alpha_bound"))
            ),
            "source_backed_rows": len(anchor_rows),
            "valid_for_claim_rows": sum(1 for row in anchor_rows if truthy(row.get("valid_for_claim"))),
            "status": "SOURCE_BACKED_ANCHOR_ONLY_NONCURVE",
            "claim_use": "smoke/provenance only",
            "valid_for_claim": False,
        },
        {
            "asset_id": "RCA3436_2_anchor_smoke_file",
            "asset": rel(SOURCES["anchor_smoke_bound_curve"]),
            "row_count": len(smoke_bound_rows),
            "positive_numeric_rows": sum(
                1
                for row in smoke_bound_rows
                if positive_float(row.get("lambda_value")) and positive_float(row.get("alpha_bound"))
            ),
            "source_backed_rows": len(smoke_bound_rows),
            "valid_for_claim_rows": sum(1 for row in smoke_bound_rows if truthy(row.get("valid_for_claim"))),
            "status": "ANCHOR_SMOKE_NONCLAIM",
            "claim_use": "guardrail runner only",
            "valid_for_claim": False,
        },
        {
            "asset_id": "RCA3436_3_reviewed_candidate_curve",
            "asset": rel(SOURCES["r10_reviewed_candidate_1572"]),
            "row_count": len(candidate_rows),
            "positive_numeric_rows": len(candidate_numeric_rows),
            "source_backed_rows": len(candidate_source_backed_rows),
            "valid_for_claim_rows": len(candidate_claim_rows),
            "status": "INTERNAL_REVIEWED_CANDIDATE_NOT_INDEPENDENTLY_SOURCE_BACKED",
            "claim_use": "curve-shape smoke only until source-backed calibration is locked",
            "valid_for_claim": False,
        },
        {
            "asset_id": "RCA3436_4_candidate_images",
            "asset": f"{rel(source_image)} ; {rel(overlay_image)}",
            "row_count": 2,
            "positive_numeric_rows": 0,
            "source_backed_rows": 0,
            "valid_for_claim_rows": 0,
            "status": f"source_image_exists={source_image.exists()}; overlay_exists={overlay_image.exists()}",
            "claim_use": "visual QA support only",
            "valid_for_claim": False,
        },
    ]


def alpha_lambda_runner_contract() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "ARC3436_0_kernel_convention",
            "object": "published Yukawa convention",
            "required_input": "V(r)=V_N(r)[1+alpha exp(-r/lambda)] and a_Y/a_N=alpha(1+r/lambda)exp(-r/lambda)",
            "current_status": "CONDITIONALLY_DERIVED_IN_3013",
            "failure_mode": "none for convention, but convention alone is not a prediction",
            "valid_for_claim": False,
        },
        {
            "contract_id": "ARC3436_1_bound_curve",
            "object": "real alpha_bound(lambda) curve",
            "required_input": "positive numeric lambda/alpha rows, source URL/DOI, digitization/table method, no MISSING markers, valid_for_claim=true",
            "current_status": "BLOCKED_FULL_CURVE_MISSING",
            "failure_mode": "anchors and internal trace candidate cannot replace a source-backed full curve",
            "valid_for_claim": False,
        },
        {
            "contract_id": "ARC3436_2_mts_prediction",
            "object": "MTS alpha_predicted(lambda)",
            "required_input": "numeric lambda_i and alpha_i or theorem-zero certificate sourced to parent action",
            "current_status": "BLOCKED_SOURCE_MAP_MISSING",
            "failure_mode": "symbolic K_X Qbar_XH qbar_XT rows cannot be scored",
            "valid_for_claim": False,
        },
        {
            "contract_id": "ARC3436_3_no_extrapolation",
            "object": "comparison rule",
            "required_input": "lambda_i must lie inside source-backed curve support; log interpolation only between valid rows",
            "current_status": "RUNNER_GUARD_PRESENT",
            "failure_mode": "lambda outside bound support blocks comparison",
            "valid_for_claim": False,
        },
        {
            "contract_id": "ARC3436_4_no_calibration_escape",
            "object": "G0/M_H_ref protection",
            "required_input": "finite-range and radial residuals must appear as alpha(lambda), not be absorbed into Newtonian source calibration",
            "current_status": "GUARD_ACTIVE",
            "failure_mode": "would otherwise hide a local fifth force inside G0",
            "valid_for_claim": False,
        },
    ]


def mts_alpha_source_map_status() -> list[dict[str, Any]]:
    return [
        {
            "map_id": "MSM3436_0_lambda_i",
            "required_quantity": "lambda_i",
            "meaning": "range/eigenvalue of the finite mode",
            "required_formula": "lambda_i=sqrt(Z_i/M_i^2) after diagonalizing the parent local operator",
            "current_status": "MISSING_PARENT_Z_AND_M2",
            "next_derivation": "derive channelwise positive operator from parent action or prove mode absent",
            "valid_for_claim": False,
        },
        {
            "map_id": "MSM3436_1_source_current",
            "required_quantity": "Qbar_i^S or J_i",
            "meaning": "source charge/current in the same Hilbert/M_H_ref frame",
            "required_formula": "J_i=delta S_matter/delta X_i, projected into compact-source exterior collar",
            "current_status": "MISSING_COUPLING_MAP",
            "next_derivation": "derive matter coupling/vertical generator map rather than fit it from R10",
            "valid_for_claim": False,
        },
        {
            "map_id": "MSM3436_2_test_response",
            "required_quantity": "qbar_i^T",
            "meaning": "test-body response to the same finite mode",
            "required_formula": "qbar_i^T=delta ln m_T/delta X_i or equivalent local-force response",
            "current_status": "MISSING_TEST_BODY_RESPONSE",
            "next_derivation": "tie the test response to quotient-invariant matter action or prove it zero",
            "valid_for_claim": False,
        },
        {
            "map_id": "MSM3436_3_normalization",
            "required_quantity": "K_i and tau_R10",
            "meaning": "conversion from q_loc/current units to observable alpha(lambda)",
            "required_formula": "alpha_i = K_i Qbar_i^S qbar_i^T tau_R10_i plus absolute boundary/tail terms",
            "current_status": "SYMBOLIC_ONLY",
            "next_derivation": "lock same-frame normalization against M_H_ref and Newtonian source mass",
            "valid_for_claim": False,
        },
        {
            "map_id": "MSM3436_4_profile_or_zero",
            "required_quantity": "q_loc profile or zero certificate",
            "meaning": "radial acceleration profile to project onto Yukawa kernel",
            "required_formula": "alpha_q(lambda;r)=|a_q/a_N| exp(r/lambda)/(1+r/lambda), or parent-signed alpha_q=0",
            "current_status": "PROFILE_MISSING_ZERO_NOT_SIGNED",
            "next_derivation": "prove q_loc/source current zero or build source-current profile with absolute error envelope",
            "valid_for_claim": False,
        },
        {
            "map_id": "MSM3436_5_proxy_bound",
            "required_quantity": "compact-shell leakage proxy",
            "meaning": "older numeric q_loc proxy could bound a channel only after units are mapped",
            "required_formula": "epsilon_q_proxy <= 7.432631961576971e-06 mapped into R10/PPN source-normalized units",
            "current_status": "NUMERIC_PROXY_NOT_OBSERVABLE_VALUE",
            "next_derivation": "derive proxy-to-alpha or proxy-to-PPN operator norm",
            "valid_for_claim": False,
        },
    ]


def existing_runner_dryrun() -> list[dict[str, Any]]:
    run_specs = [
        {
            "runner_id": "R10_RUNNER_3436_LIVE_PLACEHOLDER_RECHECK",
            "mts_curve": SOURCES["live_mts_curve"],
            "bound_curve": SOURCES["live_bound_curve"],
            "output_dir": RUN_ROOT / "live_placeholder" / "results",
        },
        {
            "runner_id": "R10_RUNNER_3436_ANCHOR_SMOKE_RECHECK",
            "mts_curve": SOURCES["smoke_mts_curve"],
            "bound_curve": SOURCES["anchor_smoke_bound_curve"],
            "output_dir": RUN_ROOT / "anchor_smoke" / "results",
        },
    ]
    rows = []
    for spec in run_specs:
        result = run_runner(spec["mts_curve"], spec["bound_curve"], spec["output_dir"])
        status = result["status"]
        rows.append(
            {
                "runner_id": spec["runner_id"],
                "mts_curve": rel(spec["mts_curve"]),
                "bound_curve": rel(spec["bound_curve"]),
                "output_dir": rel(spec["output_dir"]),
                "mts_rows": status["mts_rows"],
                "valid_mts_rows": status["valid_mts_rows"],
                "bound_rows": status["bound_rows"],
                "valid_bound_rows": status["valid_bound_rows"],
                "comparison_rows": status["comparison_rows"],
                "passed_rows": status["passed_rows"],
                "blocked_or_failed_rows": status["blocked_or_failed_rows"],
                "R10_pass_for_claim": status["R10_pass_for_claim"],
                "claim_allowed": status["claim_allowed"],
                "required_result": "false_guardrail",
                "valid_for_claim": False,
            }
        )
    return rows


def r10_score_readiness() -> list[dict[str, Any]]:
    return [
        {
            "score_id": "SR3436_0_zero_route",
            "item": "q_loc/range zero theorem",
            "before_status": "conditional positive-X no-hair identity",
            "after_status": "ZERO_THEOREM_CONDITIONAL_NOT_PARENT_SIGNED",
            "score_readiness": "not score-ready; coupling/source-current silence is missing",
            "valid_for_claim": False,
        },
        {
            "score_id": "SR3436_1_bound_curve",
            "item": "alpha_bound(lambda)",
            "before_status": "placeholder plus anchors/candidate",
            "after_status": "ASSET_AUDITED_NONCLAIM",
            "score_readiness": "not score-ready; source-backed full curve absent",
            "valid_for_claim": False,
        },
        {
            "score_id": "SR3436_2_kernel",
            "item": "R10 Yukawa kernel",
            "before_status": "conditional 3013 contract",
            "after_status": "RUNNER_CONTRACT_LOCKED",
            "score_readiness": "kernel is ready as a convention, not as an MTS prediction",
            "valid_for_claim": False,
        },
        {
            "score_id": "SR3436_3_mts_alpha",
            "item": "alpha_predicted(lambda)",
            "before_status": "symbolic template",
            "after_status": "SOURCE_MAP_BLOCKED",
            "score_readiness": "not score-ready; K_i, lambda_i, source/test charges and q_loc profile absent",
            "valid_for_claim": False,
        },
        {
            "score_id": "SR3436_4_runner_guard",
            "item": "existing comparator",
            "before_status": "available",
            "after_status": "DRYRUN_CONFIRMS_CLAIM_BLOCKED",
            "score_readiness": "guardrail works; no false R10 pass",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3436_0_range_zero",
            "gate": "finite-range/q_loc branch is theorem-zero",
            "result": "BLOCKED",
            "evidence": "RZ3436_3 source-current silence and RZ3436_4 boundary/projector silence are unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3436_1_r10_score",
            "gate": "R10 alpha(lambda) comparison can be scored",
            "result": "BLOCKED",
            "evidence": "full source-backed bound curve and MTS alpha source map absent",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3436_2_no_false_runner_pass",
            "gate": "existing runner blocks placeholders and smoke rows",
            "result": "PASS_GUARD",
            "evidence": "3436 dry-run returns R10_pass_for_claim=false for live and anchor-smoke branches",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3436_3_newton",
            "gate": "Newtonian inverse-square local source branch is clean",
            "result": "BLOCKED_RANGE_RESIDUAL_RETAINED",
            "evidence": "finite-range alpha(lambda) lane remains an explicit residual rather than G0 calibration",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3436_4_local_GR",
            "gate": "local GR/PPN is derived",
            "result": "BLOCKED",
            "evidence": "R10 range, PPN, q_loc and boundary/projector rows remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3436_0_do_not_promote_zero",
            "decision": "Do not claim q_loc/range zero.",
            "reason": "The positive-operator proof is mathematically clean, but the MTS parent has not signed the coupling/source-current and boundary/projector silence clauses.",
            "next_action": "derive the source-current/coupling map from the parent matter action or prove it vertical-silent",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3436_1_do_not_promote_curve",
            "decision": "Do not use the internal candidate curve for a public R10 pass.",
            "reason": "It has positive numeric rows, but source_backed=false and valid_for_claim=false throughout.",
            "next_action": "keep it as smoke/shape infrastructure only until source-backed digitization is independently locked",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3436_2_best_route",
            "decision": "Attack the coupling next, not another broad ledger.",
            "reason": "Both zero and score routes collapse to the same missing object: J_X=delta S_matter/delta X and its source/test response.",
            "next_action": "3437 source-current coupling map or zero-current theorem",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3437-Y5-R2FR-q_loc-source-current-coupling-map-or-zero-current-theorem-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3437_q_loc_source_current_coupling_map_or_zero_current_theorem.py",
            "objective": "derive the parent matter-coupling/source-current map J_X=delta S_matter/delta X that either makes the R10/q_loc finite-range branch zero or supplies the first real alpha(lambda) numerator",
            "success_condition": "one channel obtains a parent-signed J_X=0 zero-current theorem, or a nonclaim numeric/source-ready alpha numerator template with explicit K_i, Qbar_i^S, qbar_i^T, tau_R10 and source paths",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3436_0",
            "status": "R10_RANGE_ZERO_NOT_CLOSED_RUNNER_GUARD_WORKS",
            "claim_allowed": False,
            "reason": "source-current/coupling map and source-backed full bound curve are still missing",
            "next_safe_action": "derive coupling map before any R10 claim language",
            "valid_for_claim": False,
        }
    ]


def all_generated_nonclaim(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for output_name, rows in rows_by_name.items():
        if output_name == "validation":
            continue
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    zero_rows = rows_by_name["qloc_range_zero_audit"]
    bound_rows = rows_by_name["bound_curve_asset_audit"]
    source_map_rows = rows_by_name["mts_alpha_source_map_status"]
    dryrun_rows = rows_by_name["existing_runner_dryrun"]
    promotion_rows = rows_by_name["promotion_gates"]
    next_rows = rows_by_name["next_target"]
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1 for checked_path in FORMALIZATION.rglob("*") if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )
    validations = [
        {
            "check_id": "VAL3436_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3436_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": all(str(path).startswith(str(ROOT)) for path in OUTPUTS.values()) and str(RUN_ROOT).startswith(str(ROOT)),
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3436_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": all_generated_nonclaim(rows_by_name),
            "detail": "valid_for_claim=false and claim_allowed=false throughout generated rows",
        },
        {
            "check_id": "VAL3436_3_zero_not_overpromoted",
            "condition": "range zero theorem is not promoted while source current is missing",
            "passed": any(row["clause_id"] == "RZ3436_3_source_current_silence" and row["status"] == "MISSING_COUPLING_MAP" for row in zero_rows)
            and any(row["gate_id"] == "PG3436_0_range_zero" and row["result"] == "BLOCKED" for row in promotion_rows),
            "detail": "J_X/source-current silence remains unsigned",
        },
        {
            "check_id": "VAL3436_4_bound_curve_audited",
            "condition": "bound curve assets are counted and not promoted",
            "passed": any(row["asset_id"] == "RCA3436_3_reviewed_candidate_curve" and int(row["positive_numeric_rows"]) > 0 and int(row["valid_for_claim_rows"]) == 0 for row in bound_rows),
            "detail": "candidate curve present as nonclaim shape asset",
        },
        {
            "check_id": "VAL3436_5_runner_guard",
            "condition": "existing runner keeps live and smoke branches blocked",
            "passed": len(dryrun_rows) == 2 and all(str(row["R10_pass_for_claim"]).lower() == "false" and str(row["claim_allowed"]).lower() == "false" for row in dryrun_rows),
            "detail": "R10_pass_for_claim=false for both dry-runs",
        },
        {
            "check_id": "VAL3436_6_source_map_blocked",
            "condition": "MTS alpha map still records missing coupling/source inputs",
            "passed": any(row["map_id"] == "MSM3436_1_source_current" and row["current_status"] == "MISSING_COUPLING_MAP" for row in source_map_rows),
            "detail": "coupling/source-current map selected as next derivation",
        },
        {
            "check_id": "VAL3436_7_next_target",
            "condition": "next target attacks coupling/source-current derivation",
            "passed": "source-current" in next_rows[0]["objective"] and "coupling" in next_rows[0]["target_doc"],
            "detail": next_rows[0]["target_doc"],
        },
        {
            "check_id": "VAL3436_8_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3436_9_overall",
            "condition": "3436 R10/range-zero checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3436 - R10 Alpha Lambda Runner Real Curve or q_loc Range Zero

## Summary
- This checkpoint takes the derivation-first route: try to make the finite-range `q_loc`/bulk-X branch vanish before treating it as a fitted fifth force.
- The proof structure is clean: a positive local operator with zero source current and zero boundary/projector injection gives `X=0`, hence `alpha_X(lambda)=0`.
- The proof is not yet claimable for MTS because the missing object is exactly the coupling/source-current map `J_X = delta S_matter / delta X`.
- The fallback R10 lane is now explicit: source-backed full bound curve plus MTS alpha numerator/source map, or no score.
- The existing comparator was re-run as a guardrail and correctly blocks both live placeholders and anchor-smoke rows.

## Source Register
{md_table(rows_by_name["source_register"])}

## q_loc Range-Zero Audit
{md_table(rows_by_name["qloc_range_zero_audit"])}

## R10 Bound-Curve Asset Audit
{md_table(rows_by_name["bound_curve_asset_audit"])}

## Alpha Lambda Runner Contract
{md_table(rows_by_name["alpha_lambda_runner_contract"])}

## MTS Alpha Source-Map Status
{md_table(rows_by_name["mts_alpha_source_map_status"])}

## Existing Runner Dry-Run
{md_table(rows_by_name["existing_runner_dryrun"])}

## R10 Score Readiness
{md_table(rows_by_name["r10_score_readiness"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
The range-zero route did not die; it sharpened. The math says exactly what we need: if the parent matter action makes the local source current vanish, the finite-range branch vanishes without asking R10 to rescue it. If that current does not vanish, R10 becomes a proper alpha(lambda) bound problem. Either way, the next real leap is the coupling map, not another broad audit.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "qloc_range_zero_audit": qloc_range_zero_audit(),
        "bound_curve_asset_audit": bound_curve_asset_audit(),
        "alpha_lambda_runner_contract": alpha_lambda_runner_contract(),
        "mts_alpha_source_map_status": mts_alpha_source_map_status(),
        "existing_runner_dryrun": existing_runner_dryrun(),
        "r10_score_readiness": r10_score_readiness(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3436 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
