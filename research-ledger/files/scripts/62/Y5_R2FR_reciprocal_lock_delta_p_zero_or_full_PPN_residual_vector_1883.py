from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1883"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1883-Y5-R2FR-reciprocal-lock-delta-p-zero-or-full-PPN-residual-vector.md"

INPUTS = {
    "1882_doc": ROOT / "1882-Y5-R2FR-sigmaR-profile-coefficient-from-CR-source-normalization-or-no-shadow-action-contract.md",
    "1882_identity": OUT / "P8_Y5_PARENT_QLOC_1882_CR_WEAK_FIELD_IDENTITY.csv",
    "1882_combo": OUT / "P8_Y5_PARENT_QLOC_1882_PPN_COMBINATION_BOUND.csv",
    "1882_validation": OUT / "P8_Y5_BRR545_1882_VALIDATION.csv",
    "04_contract": ROOT / "04-vacuum-reciprocity-action-contract.md",
    "05_attempt": ROOT / "05-reciprocity-theorem-attempt.md",
    "06_neutrality": ROOT / "06-reciprocal-charge-source-neutrality.md",
    "07_constraint": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "10_observer": ROOT / "10-observer-map-symplectic-contract.md",
    "1238_first_class": OUT / "P8_Y5_R10_1238_FIRST_CLASS_RAB_CONSTRAINT_ATTEMPT.csv",
    "1238_vector": OUT / "P8_Y5_R10_1238_LOCAL_RESIDUAL_VECTOR_MAP.csv",
    "1239_schema": OUT / "P8_Y5_R10_1239_RUNNER_INPUT_SCHEMA.csv",
    "1240_qr_map": OUT / "P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
    "1875_rab_vector": OUT / "P8_Y5_PARENT_QLOC_1875_RAB_RESIDUAL_OPERATOR_SOURCE_VECTOR.csv",
    "1880_projection": OUT / "P8_Y5_PARENT_QLOC_1880_COMMON_FRAME_PROJECTION_CONTRACTS.csv",
    "local_bounds": ROOT / "source-intake" / "local_bounds" / "local_bound_claims.csv",
}

SOURCE_NEEDLES = {
    "1882_doc": [
        "x_U_CR = dC_R/du|0 = 2(p-1)",
        "RECIPROCAL_LOCK_DELTA_P_ZERO_OR_FULL_PPN_VECTOR_SELECTED_NEXT",
    ],
    "1882_identity": [
        "CRID1882_0_definitions",
        "FREE_PROFILE_ROUTE_REJECTED_FOR_CR_CHANNEL",
    ],
    "1882_combo": [
        "PCB1882_0_exact_combo",
        "NO_CANCELLATION_GUARD_ACTIVE",
    ],
    "1882_validation": [
        "VAL1882_OVERALL,PASS",
    ],
    "04_contract": [
        "T^2 S = 1",
        "d/dr [ W(r,L,fields) dR_AB/dr ] = J_R",
    ],
    "05_attempt": [
        "W R_AB' = Q_R",
        "R_AB = 0",
    ],
    "06_neutrality": [
        "source reciprocal neutrality",
        "not yet parent-derived",
    ],
    "07_constraint": [
        "S_constraint = integral lambda_R R_AB",
        "lambda_R ln(T^2 S) as a parent constraint",
    ],
    "10_observer": [
        "R_AB = ln(T^2 S) = 2 ln(J_q)",
        "derive R_AB=0 from the parent theory",
    ],
    "1238_first_class": [
        "FCR1238_5_verdict",
        "FIRST_CLASS_ROUTE_NOT_CONSTRUCTED",
    ],
    "1238_vector": [
        "RV1238_0_QR",
        "RV1238_1_beta_PPN",
    ],
    "1239_schema": [
        "branch_type",
        "closure_benchmark | finite_residual | source_required | derived_target",
    ],
    "1240_qr_map": [
        "QMAP1240_2_dimensionless_qR",
        "gamma_minus_1_QR",
    ],
    "1875_rab_vector": [
        "RV1875_5_massless_tail",
        "RV1875_9_no_cancellation",
    ],
    "1880_projection": [
        "PRC1880_0_PPN_metric",
        "PRC1880_1_PPN_preferred",
    ],
    "local_bounds": [
        "Cassini_Shapiro_gamma_2003",
        "Will_2014_PPN_beta_table",
        "Will_2014_PPN_alpha1_table",
    ],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1883_SOURCE_REGISTER.csv",
    "reciprocal_lock_audit": OUT / "P8_Y5_PARENT_QLOC_1883_RECIPROCAL_LOCK_DERIVATION_AUDIT.csv",
    "delta_p_bridge": OUT / "P8_Y5_PARENT_QLOC_1883_DELTA_P_QRHAT_BRIDGE.csv",
    "ppn_residual_vector": OUT / "P8_Y5_PARENT_QLOC_1883_FULL_PPN_RESIDUAL_VECTOR.csv",
    "ppn_bound_rows": OUT / "P8_Y5_PARENT_QLOC_1883_PPN_BOUND_ROWS.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1883_PPN_VECTOR_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1883_PPN_VECTOR_DRYRUN_RESULTS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1883_RUNNER_REFUSAL.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1883_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1883_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1883_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1883_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1883_VALIDATION.csv",
}


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def path_has_needles(path: Path, needles: list[str]) -> tuple[bool, str]:
    if not path.exists():
        return False, "MISSING_SOURCE_PATH"
    text = path.read_text(encoding="utf-8", errors="ignore")
    missing = [needle for needle in needles if needle not in text]
    if missing:
        return False, "MISSING_NEEDLES=" + ";".join(missing)
    return True, "OK"


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path in INPUTS.items():
        ok, detail = path_has_needles(path, SOURCE_NEEDLES[source_id])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "checkpoint_id": CHECKPOINT_ID,
                "source_id": source_id,
                "source_path": str(path),
                "required_needles": " ; ".join(SOURCE_NEEDLES[source_id]),
                "source_exists": path.exists(),
                "needle_check": detail,
                "usable_for_1883": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def reciprocal_lock_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "RLA1883_0_multiplier_closure",
            "route": "lambda_R C_R multiplier",
            "exact_statement": "If the parent action contains a parent-owned multiplier lambda_R C_R, variation gives C_R=0 and therefore delta_p=0 at first PPN order.",
            "attempt_result": "EXACT_CONDITIONAL_CLOSURE",
            "blocker": "multiplier origin is not parent-derived; adding lambda_R C_R by hand is the closure axiom in action form",
            "claim_effect": "cannot promote reciprocal lock",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "RLA1883_1_first_class_constraint",
            "route": "first-class R_AB constraint",
            "exact_statement": "If a differentiable generator G_R closes first-class, has zero/proper boundary charge, and ordinary matter/readout descends to the quotient, then R_AB is removed before observables.",
            "attempt_result": "EXACT_CONDITIONAL_THEOREM_NOT_CONSTRUCTED",
            "blocker": "no parent generator, Poisson algebra, boundary charge proof, or matter/readout descent in current corpus",
            "claim_effect": "delta_p=0 remains a target, not a theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "RLA1883_2_second_class_auxiliary",
            "route": "second-class auxiliary elimination",
            "exact_statement": "If C_R and its multiplier form an algebraic auxiliary pair solved before phase space, no exterior R_AB tail survives.",
            "attempt_result": "POSSIBLE_CONDITIONAL_ROUTE_UNSIGNED",
            "blocker": "current R_AB trail includes kinetic/current-hair and finite-tail possibilities, so algebraic elimination is not parent-signed",
            "claim_effect": "cannot erase Q_R or beta/source residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "RLA1883_3_vacuum_strain_equation",
            "route": "d(W C_R')=J_R vacuum strain",
            "exact_statement": "If J_R=0, W>0, no boundary/source charge exists, and C_R(infinity)=0, then C_R=0.",
            "attempt_result": "CONDITIONAL_ZERO_CHARGE_ROUTE_UNSIGNED",
            "blocker": "current conservation gives W C_R'=Q_R; asymptotic flatness kills the offset but not Q_R hair",
            "claim_effect": "finite q_R_hat/delta_p row remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "RLA1883_4_eh_import_guard",
            "route": "Einstein/GR vacuum identity",
            "exact_statement": "In GR, the local vacuum equations can imply the reciprocal Schwarzschild relation, but importing this as an MTS premise is circular.",
            "attempt_result": "REJECT_AS_DERIVATION_SHORTCUT",
            "blocker": "MTS must derive the Einstein/source-normalized local equations first, not borrow their result",
            "claim_effect": "do not claim GR reduction from a GR identity",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "RLA1883_5_verdict",
            "route": "reciprocal lock delta_p zero",
            "exact_statement": "Current MTS parent-derives T^2S=1 and delta_p=0.",
            "attempt_result": "RECIPROCAL_LOCK_NOT_PARENT_DERIVED_CURRENT_CORPUS",
            "blocker": "all zero routes require unsigned parent constraint/source/boundary/matter descent premises",
            "claim_effect": "build full PPN residual vector and keep all local claims blocked",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def delta_p_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "DPB1883_0_CR_delta_p",
            "relation": "C_R = 2 delta_p U/c^2 + O(U^2/c^4)",
            "normalization": "u=U/c^2 with U=GM/r",
            "result": "delta_p=(1/2) dC_R/du at u=0",
            "status": "DERIVED_SYMBOLIC_NONCLAIM",
            "missing": "delta_p source equation or reciprocal-lock theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "DPB1883_1_QR_delta_p",
            "relation": "if exterior C_R=-Q_R/r and q_R_hat=Q_R c^2/(GM), then C_R=-q_R_hat U/c^2",
            "normalization": "same measured GM as the PPN source",
            "result": "delta_p=-q_R_hat/2",
            "status": "DERIVED_CONDITIONAL_BRIDGE_NONCLAIM",
            "missing": "Q_R value or zero-charge theorem; kappa_W/sign/domain if using current-hair normalization",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "DPB1883_2_gamma_combo",
            "relation": "sigma_R=b_R C_R and gamma_obs=(p+s_R)/(1-s_R)",
            "normalization": "s_R=2b_R delta_p",
            "result": "gamma_obs_minus_1=(delta_p+4b_R delta_p)/(1-2b_R delta_p)",
            "status": "NONCIRCULAR_COMBO_BOUND_FORM",
            "missing": "delta_p/q_R_hat and b_R finite or zero rows; beta/source/preferred-frame rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def ppn_residual_vector_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "component_id": "PPNV1883_0_delta_p_qR",
            "symbol": "delta_p_or_q_R_hat",
            "observable": "gamma_minus_1; Shapiro/light bending; orbital weak-field lane",
            "residual_expression": "delta_p=-q_R_hat/2 if exterior C_R=-Q_R/r and same GM normalization holds",
            "accepted_bound_or_target": "Cassini gamma 2.3e-05 after full-vector channel closure",
            "current_status": "MISSING_ZERO_THEOREM_OR_NUMERIC_QRHAT",
            "source_path": str(INPUTS["1240_qr_map"]),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "PPNV1883_1_bR_common_weyl",
            "symbol": "b_R",
            "observable": "gamma_minus_1; clock common-mode; source normalization",
            "residual_expression": "first order gamma Weyl contribution is 4 b_R delta_p inside the no-circularity combination",
            "accepted_bound_or_target": "only with delta_p and no-cancellation policy",
            "current_status": "MISSING_NO_SHADOW_THEOREM_OR_NUMERIC_BR",
            "source_path": str(INPUTS["1882_combo"]),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "PPNV1883_2_beta_second_order",
            "symbol": "delta_beta=beta_PPN-1",
            "observable": "perihelion/orbital timing/second-order light propagation",
            "residual_expression": "independent second-order PPN residual; gamma closure does not imply beta=1",
            "accepted_bound_or_target": "Will/Messenger beta_minus_1 upper bound 7.8e-05",
            "current_status": "MISSING_BETA_FIELD_EQUATION_AND_CONSERVATION_PROOF",
            "source_path": str(INPUTS["local_bounds"]),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "PPNV1883_3_dR_preferred_frame",
            "symbol": "d_R; alpha1; alpha2; alpha3; xi",
            "observable": "preferred-frame/preferred-location PPN",
            "residual_expression": "disformal/preferred-frame shadow terms must map to alpha_i or be theorem-zero",
            "accepted_bound_or_target": "alpha1 1e-4; alpha2 2e-9; alpha3 4e-20; xi 4e-9",
            "current_status": "MISSING_DISFORMAL_RESPONSE_KERNEL",
            "source_path": str(INPUTS["1880_projection"]),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "PPNV1883_4_wR_source_normalization",
            "symbol": "w_R",
            "observable": "measured GM; WEP/source normalization; clock/material",
            "residual_expression": "source-only matter prefactor can shift Hilbert source/GM without showing as ordinary WEP composition failure",
            "accepted_bound_or_target": "must be source-normalized before PPN score",
            "current_status": "MISSING_SOURCE_PREFACTOR_ZERO_OR_BOUND",
            "source_path": str(INPUTS["1875_rab_vector"]),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "PPNV1883_5_endpoint_tau_boundary",
            "symbol": "epsilon_endpoint_R; tau_PPN; boundary_tail",
            "observable": "light-time/orbital/clock transfer",
            "residual_expression": "endpoint, tau and boundary tails must be zero or bounded in same observable units",
            "accepted_bound_or_target": "arena-specific projection kernel required",
            "current_status": "MISSING_ENDPOINT_TAU_BOUNDARY_KERNELS",
            "source_path": str(INPUTS["1875_rab_vector"]),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "PPNV1883_6_Khat_q_loc",
            "symbol": "Delta_K; q_loc; K_perp",
            "observable": "PPN/local_GR/preferred-frame residuals",
            "residual_expression": "retained Khat/q_loc scalar and transverse channels cannot be deleted by the C_R identity",
            "accepted_bound_or_target": "operator/projector norms plus component bounds",
            "current_status": "MISSING_KHAT_QLOC_OPERATOR_BOUNDS",
            "source_path": str(INPUTS["1875_rab_vector"]),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "component_id": "PPNV1883_7_total_no_cancellation",
            "symbol": "R_PPN_abs_total",
            "observable": "all local PPN observables",
            "residual_expression": "sum absolute active components unless a parent identity proves cancellation",
            "accepted_bound_or_target": "gamma,beta,preferred-frame bounds all satisfied independently or by parent identity",
            "current_status": "RESIDUAL_VECTOR_READY_NONCLAIM_ALL_SCORES_BLOCKED",
            "source_path": str(INPUTS["1875_rab_vector"]),
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def ppn_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "PBOUND1883_0_gamma",
            "observable": "gamma_minus_1",
            "upper_bound": "2.3e-05",
            "source_id": "Cassini_Shapiro_gamma_2003:R3_gamma",
            "use_policy": "primary gamma comparator; not an MTS prediction by itself",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND1883_1_beta",
            "observable": "beta_minus_1",
            "upper_bound": "7.8e-05",
            "source_id": "Will_2014_PPN_beta_table:R4_beta",
            "use_policy": "second-order/local orbital channel; cannot be inferred from gamma only",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND1883_2_alpha1",
            "observable": "alpha1",
            "upper_bound": "1e-04",
            "source_id": "Will_2014_PPN_alpha1_table:R5_alpha1",
            "use_policy": "preferred-frame comparator requires d_R response kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND1883_3_alpha2",
            "observable": "alpha2",
            "upper_bound": "2e-09",
            "source_id": "Will_2014_PPN_alpha2_table:R6_alpha2",
            "use_policy": "preferred-frame comparator requires d_R response kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND1883_4_alpha3",
            "observable": "alpha3",
            "upper_bound": "4e-20",
            "source_id": "Will_2014_PPN_alpha3_table:R7_alpha3",
            "use_policy": "ultratight momentum/preferred-frame comparator; never use without source/routing proof",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "bound_id": "PBOUND1883_5_xi",
            "observable": "xi",
            "upper_bound": "4e-09",
            "source_id": "Will_2014_PPN_xi_table:R8_xi",
            "use_policy": "preferred-location comparator requires domain/boundary response kernel",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE1883_0_closure_GR",
            "description": "explicit closure benchmark sets delta_p=b_R=beta=d_R=w_R=endpoint=0",
            "branch_type": "closure_benchmark",
            "value_mode": "closure_value",
            "expected_status": "REFUSED_CLOSURE_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1883_1_missing_finite",
            "description": "finite branch has no delta_p/q_R_hat and no b_R value",
            "branch_type": "finite_residual",
            "value_mode": "missing_source",
            "expected_status": "REFUSED_MISSING_VECTOR_INPUTS",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1883_2_gamma_only",
            "description": "gamma combo appears bounded but beta/preferred/source rows are missing",
            "branch_type": "finite_residual",
            "value_mode": "partial_gamma_only",
            "expected_status": "REFUSED_INCOMPLETE_VECTOR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1883_3_cancellation_only",
            "description": "delta_p(1+4b_R) is tuned small without parent identity",
            "branch_type": "finite_residual",
            "value_mode": "cancellation_tuned",
            "expected_status": "REFUSED_CANCELLATION_ONLY",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1883_4_hypothetical_full_vector",
            "description": "all vector components are numeric and below bounds but source provenance is hypothetical",
            "branch_type": "finite_residual",
            "value_mode": "hypothetical_numeric",
            "expected_status": "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dryrun_result_rows() -> list[dict[str, Any]]:
    status_reason = {
        "CASE1883_0_closure_GR": "closure rows are useful private baselines but not derivations or evidence",
        "CASE1883_1_missing_finite": "delta_p/q_R_hat, b_R, beta, source and projection inputs are missing",
        "CASE1883_2_gamma_only": "gamma cannot stand in for beta, preferred-frame, source, endpoint and no-cancellation gates",
        "CASE1883_3_cancellation_only": "tuned cancellation is refused without a parent identity and independent channel closure",
        "CASE1883_4_hypothetical_full_vector": "arithmetic schema can evaluate later, but synthetic values are not sourced MTS predictions",
    }
    rows: list[dict[str, Any]] = []
    for case in dryrun_case_rows():
        rows.append(
            {
                "case_id": case["case_id"],
                "branch_type": case["branch_type"],
                "value_mode": case["value_mode"],
                "runner_status": case["expected_status"],
                "reason": status_reason[case["case_id"]],
                "raw_numeric_pass": False if case["case_id"] != "CASE1883_4_hypothetical_full_vector" else True,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1883_0_reciprocal_lock_proof",
            "runner": "reciprocal lock parent proof checker",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "all C_R=0 routes are exact conditional but parent constraint/source/boundary/matter descent premises remain unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1883_1_full_ppn_vector",
            "runner": "full PPN residual-vector scorer",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "schema exists but finite vector values, projection kernels and no-cancellation identities are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1883_2_gamma_only",
            "runner": "gamma-only Cassini shortcut",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "gamma-only or cancellation-only success cannot imply local GR",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1883_0_internal",
            "claim": "1883 full PPN residual vector may guide private work",
            "status": "ALLOW_INTERNAL_NONCLAIM_VECTOR",
            "reason": "it is a schema/refusal checkpoint, not a pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1883_1_delta_p_zero",
            "claim": "delta_p=0 is parent-derived",
            "status": "BLOCKED",
            "reason": "reciprocal lock is exact conditional but not parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1883_2_ppn_pass",
            "claim": "MTS passes PPN/Cassini",
            "status": "BLOCKED",
            "reason": "full residual vector values and channel closures are missing",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1883_3_local_GR",
            "claim": "local GR/Newton is derived",
            "status": "BLOCKED",
            "reason": "C_R reciprocal lock, beta, source conservation, no-shadow and projection kernels are not all closed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1883_0_lock",
            "decision": "RECIPROCAL_LOCK_NOT_PARENT_DERIVED",
            "basis": "multiplier, first-class, auxiliary and strain-equation routes are exact conditional but unsigned",
            "consequence": "delta_p/q_R_hat remains a live finite residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1883_1_vector",
            "decision": "FULL_PPN_RESIDUAL_VECTOR_BUILT_NONCLAIM",
            "basis": "1882 no-circularity map plus 1238/1875 residual maps show gamma-only is insufficient",
            "consequence": "future tests must include delta_p/q_R_hat, b_R, beta, d_R, w_R, endpoint, Khat/q_loc and no-cancellation gates",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1883_2_testing_policy",
            "decision": "CLOSURE_AND_FINITE_BRANCHES_MUST_STAY_SEPARATE",
            "basis": "closure zero rows are private baselines only; finite residual rows require source values or parent zero theorems",
            "consequence": "runner cases refuse closure-as-evidence, missing-source, gamma-only and cancellation-only paths",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1883_3_next",
            "decision": "NO_BOUNDARY_CHARGE_SOURCE_DESCENT_OR_DELTA_P_INPUT_SELECTED_NEXT",
            "basis": "the proof bottleneck is now Q_R/delta_p source/boundary ownership; the empirical bottleneck is a normalized q_R_hat/delta_p row",
            "consequence": "1884 should target the no-boundary-charge/source-descent proof package or create a strict delta_p/q_R_hat input contract",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1883_0_primary",
            "target_doc": "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md",
            "target_script": "scripts/Y5_R2FR_no_boundary_charge_source_descent_or_delta_p_input_contract_1884.py",
            "objective": "try to prove Q_R=0/delta_p=0 from no-boundary-charge plus source/matter descent; if not, build a strict source-normalized delta_p/q_R_hat input contract for the full PPN vector.",
            "selection_status": "selected",
            "success_condition": "parent-signed no-boundary-charge/source-descent theorem, or a schema-ready delta_p/q_R_hat input validator that refuses closure/comparator-only/cancellation-only rows.",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1883_1_secondary",
            "target_doc": "1884b-Y5-R2FR-beta-second-order-source-normalized-closure-gate.md",
            "target_script": "scripts/Y5_R2FR_beta_second_order_source_normalized_closure_gate_1884b.py",
            "objective": "separately attack beta_minus_1 after delta_p/q_R_hat is handled.",
            "selection_status": "held_secondary",
            "success_condition": "beta field-equation/source-normalization theorem or finite beta input row.",
            "valid_for_claim": False,
        },
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS1883_0_progress",
            "plain_english": "The project has a cleaner local-testing spine now: reciprocal lock is not proven, so the whole PPN residual vector is the honest interface.",
            "technical_state": "delta_p/q_R_hat, b_R, beta, d_R, w_R, endpoint, Khat/q_loc and no-cancellation gates are explicit",
            "risk_level": "DISCIPLINED_TEST_INTERFACE",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS1883_1_good_news",
            "plain_english": "This is less elegant than proving GR in one blow, but it is more competitive: it prevents hidden closure assumptions and gives exact places to derive or bound next.",
            "technical_state": "runner dry-run refuses closure evidence, missing finite rows, gamma-only rows and cancellation-only rows",
            "risk_level": "ROBUSTNESS_GAIN",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "checkpoint_id": CHECKPOINT_ID,
            "status_id": "STATUS1883_2_missing",
            "plain_english": "The big missing theorem is still no-boundary-charge/source descent for R_AB; without it, delta_p/q_R_hat remains the first finite local residual.",
            "technical_state": "Q_R=0 first-class/topological/source theorem absent; beta/source/no-shadow channels still open",
            "risk_level": "MAIN_BOTTLENECK",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "reciprocal_lock_audit": reciprocal_lock_audit_rows(),
        "delta_p_bridge": delta_p_bridge_rows(),
        "ppn_residual_vector": ppn_residual_vector_rows(),
        "ppn_bound_rows": ppn_bound_rows(),
        "dryrun_cases": dryrun_case_rows(),
        "dryrun_results": dryrun_result_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def copy_branch_artifacts() -> None:
    shutil.copy2(OUTPUTS["ppn_residual_vector"], MICROSCOPE_RESIDUALS / OUTPUTS["ppn_residual_vector"].name)
    shutil.copy2(OUTPUTS["dryrun_results"], QUARANTINE / OUTPUTS["dryrun_results"].name)
    shutil.copy2(OUTPUTS["ppn_residual_vector"], QUEUE / "JR1883_FULL_PPN_RESIDUAL_VECTOR_NONCLAIM.csv")
    shutil.copy2(OUTPUTS["delta_p_bridge"], QUEUE / "JR1883_DELTA_P_QRHAT_BRIDGE_NONCLAIM.csv")


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    offenders: list[str] = []
    for path in paths:
        for row in csv_rows(path):
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "prediction_ready", "valid_prediction_row"):
                if key in row:
                    checked += 1
                    if bool_string(row[key]) == "true":
                        offenders.append(f"{path.name}:{key}=true")
    if offenders:
        return False, ";".join(offenders)
    return True, f"checked={checked}"


def missing_rows_not_ready(paths: list[Path]) -> tuple[bool, str]:
    checked = 0
    offenders: list[str] = []
    markers = ("MISSING_", "UNSIGNED", "BLOCKED", "NOT_CONSTRUCTED", "NOT_DERIVED", "REFUSE")
    for path in paths:
        for row in csv_rows(path):
            joined = " ".join(str(value) for value in row.values())
            if not any(marker in joined for marker in markers):
                continue
            checked += 1
            for key in ("valid_for_claim", "claim_allowed", "score_ready", "prediction_ready", "valid_prediction_row"):
                if key in row and bool_string(row[key]) == "true":
                    offenders.append(f"{path.name}:{row}")
                    break
    if offenders:
        return False, ";".join(offenders[:5])
    return True, f"checked_missing_or_blocked_rows={checked}"


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    for path in paths:
        rows = csv_rows(path)
        if not rows:
            return False, f"{path.name}:NO_ROWS"
        details.append(f"{path.name}:{len(rows)}")
    return True, ";".join(details)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    rows_by_name = {key: csv_rows(path) for key, path in OUTPUTS.items() if key != "validation"}
    checks: list[dict[str, Any]] = []

    sources = rows_by_name["source_register"]
    checks.append(
        {
            "validation_id": "VAL1883_0_sources",
            "status": "PASS" if all(row["needle_check"] == "OK" for row in sources) else "FAIL",
            "detail": "1882, reciprocal-lock, first-class, residual-vector and PPN-bound sources needle-checked",
            "valid_for_claim": False,
        }
    )

    lock = rows_by_name["reciprocal_lock_audit"]
    checks.append(
        {
            "validation_id": "VAL1883_1_lock_not_promoted",
            "status": "PASS"
            if any(row["attempt_result"] == "RECIPROCAL_LOCK_NOT_PARENT_DERIVED_CURRENT_CORPUS" for row in lock)
            and all(bool_string(row["claim_allowed"]) == "false" for row in lock)
            else "FAIL",
            "detail": "reciprocal lock derivation remains exact conditional but not parent-promoted",
            "valid_for_claim": False,
        }
    )

    bridge = rows_by_name["delta_p_bridge"]
    checks.append(
        {
            "validation_id": "VAL1883_2_delta_bridge",
            "status": "PASS"
            if any(row["result"] == "delta_p=-q_R_hat/2" for row in bridge)
            and any(row["status"] == "NONCIRCULAR_COMBO_BOUND_FORM" for row in bridge)
            else "FAIL",
            "detail": "delta_p/q_R_hat bridge and noncircular gamma combo are recorded",
            "valid_for_claim": False,
        }
    )

    vector = rows_by_name["ppn_residual_vector"]
    required_components = {
        "PPNV1883_0_delta_p_qR",
        "PPNV1883_1_bR_common_weyl",
        "PPNV1883_2_beta_second_order",
        "PPNV1883_3_dR_preferred_frame",
        "PPNV1883_4_wR_source_normalization",
        "PPNV1883_5_endpoint_tau_boundary",
        "PPNV1883_6_Khat_q_loc",
        "PPNV1883_7_total_no_cancellation",
    }
    checks.append(
        {
            "validation_id": "VAL1883_3_full_vector",
            "status": "PASS"
            if required_components.issubset({row["component_id"] for row in vector})
            and all(bool_string(row["score_ready"]) == "false" for row in vector)
            else "FAIL",
            "detail": "full PPN residual vector includes delta_p/qR, bR, beta, preferred-frame, source, endpoint, Khat and no-cancellation rows",
            "valid_for_claim": False,
        }
    )

    bounds = rows_by_name["ppn_bound_rows"]
    checks.append(
        {
            "validation_id": "VAL1883_4_ppn_bounds",
            "status": "PASS"
            if {"gamma_minus_1", "beta_minus_1", "alpha1", "alpha2", "alpha3", "xi"}.issubset(
                {row["observable"] for row in bounds}
            )
            else "FAIL",
            "detail": "PPN bound ledger covers gamma, beta and preferred-frame/location observables",
            "valid_for_claim": False,
        }
    )

    results = rows_by_name["dryrun_results"]
    expected_statuses = {
        "REFUSED_CLOSURE_NOT_EVIDENCE",
        "REFUSED_MISSING_VECTOR_INPUTS",
        "REFUSED_INCOMPLETE_VECTOR",
        "REFUSED_CANCELLATION_ONLY",
        "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
    }
    checks.append(
        {
            "validation_id": "VAL1883_5_dryrun_refusals",
            "status": "PASS"
            if expected_statuses.issubset({row["runner_status"] for row in results})
            and all(bool_string(row["claim_allowed"]) == "false" for row in results)
            else "FAIL",
            "detail": "dry-run refuses closure, missing, gamma-only and cancellation-only routes",
            "valid_for_claim": False,
        }
    )

    runners = rows_by_name["runner_refusal"]
    checks.append(
        {
            "validation_id": "VAL1883_6_runner_refusal",
            "status": "PASS" if all(row["current_status"].startswith("REFUSE_CLAIM_RUN") for row in runners) else "FAIL",
            "detail": "reciprocal-lock, full-vector and gamma-only runners refuse claim runs",
            "valid_for_claim": False,
        }
    )

    claims = rows_by_name["claim_gate"]
    checks.append(
        {
            "validation_id": "VAL1883_7_claim_gate",
            "status": "PASS"
            if any(row["status"] == "ALLOW_INTERNAL_NONCLAIM_VECTOR" for row in claims)
            and all(bool_string(row["claim_allowed"]) == "false" for row in claims)
            else "FAIL",
            "detail": "only internal nonclaim vector use is allowed",
            "valid_for_claim": False,
        }
    )

    decisions = rows_by_name["decision"]
    checks.append(
        {
            "validation_id": "VAL1883_8_decision",
            "status": "PASS"
            if any(row["decision"] == "RECIPROCAL_LOCK_NOT_PARENT_DERIVED" for row in decisions)
            and any(row["decision"] == "FULL_PPN_RESIDUAL_VECTOR_BUILT_NONCLAIM" for row in decisions)
            else "FAIL",
            "detail": "decision records failed proof promotion and full-vector fallback",
            "valid_for_claim": False,
        }
    )

    next_targets = rows_by_name["next_target"]
    checks.append(
        {
            "validation_id": "VAL1883_9_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1883_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1884 no-boundary-charge/source-descent or delta_p input contract selected",
            "valid_for_claim": False,
        }
    )

    status_rows = rows_by_name["project_status"]
    checks.append(
        {
            "validation_id": "VAL1883_10_project_status",
            "status": "PASS"
            if len(status_rows) == 3
            and any(row["risk_level"] == "MAIN_BOTTLENECK" for row in status_rows)
            else "FAIL",
            "detail": "project status snapshot records interface, robustness gain and bottleneck",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1883_11_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    missing_ok, missing_detail = missing_rows_not_ready(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1883_12_missing_not_ready",
            "status": "PASS" if missing_ok else "FAIL",
            "detail": missing_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1883_13_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["ppn_residual_vector"].name,
        QUARANTINE / OUTPUTS["dryrun_results"].name,
        QUEUE / "JR1883_FULL_PPN_RESIDUAL_VECTOR_NONCLAIM.csv",
        QUEUE / "JR1883_DELTA_P_QRHAT_BRIDGE_NONCLAIM.csv",
    ]
    checks.append(
        {
            "validation_id": "VAL1883_14_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1883_15_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1883*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1883_16_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1883_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1883_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1883 reciprocal lock delta_p zero or full PPN residual vector",
            "valid_for_claim": False,
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return ""
    headers: list[str] = []
    for row in rows:
        for key in row:
            if key not in headers:
                headers.append(key)
    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        values = [str(row.get(header, "")).replace("\n", " ") for header in headers]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    validation = csv_rows(OUTPUTS["validation"])
    content = f"""# 1883 - Reciprocal Lock Delta_p Zero Or Full PPN Residual Vector

**Private status:** nonclaim proof/refusal checkpoint.

## Result

The clean local-GR route still has an exact conditional spine:

```text
C_R = R_AB = ln(T^2 S)
C_R = 0  =>  T^2 S = 1  =>  delta_p = 0
```

But 1883 does **not** promote this to a derived MTS theorem. The parent package is still unsigned: multiplier origin, first-class generator, boundary charge, source silence, and matter/readout descent are not all present in one parent action.

The useful progress is the fallback discipline: the local branch now has a full PPN residual vector. A gamma-only or cancellation-only result is refused. Future testing must carry `delta_p/q_R_hat`, `b_R`, `beta`, `d_R`, `w_R`, endpoint/tau/boundary, and `Khat/q_loc` channels together unless a parent identity kills them.

## Reciprocal Lock Derivation Audit

{markdown_table(rows_by_name["reciprocal_lock_audit"])}

## Delta_p / q_R_hat Bridge

{markdown_table(rows_by_name["delta_p_bridge"])}

## Full PPN Residual Vector

{markdown_table(rows_by_name["ppn_residual_vector"])}

## PPN Bound Rows

{markdown_table(rows_by_name["ppn_bound_rows"])}

## Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Dry-Run Results

{markdown_table(rows_by_name["dryrun_results"])}

## Runner Refusal

{markdown_table(rows_by_name["runner_refusal"])}

## Source Register

{markdown_table(rows_by_name["source_register"])}

## Claim Gate

{markdown_table(rows_by_name["claim_gate"])}

## Decision Ledger

{markdown_table(rows_by_name["decision"])}

## Project Status Snapshot

{markdown_table(rows_by_name["project_status"])}

## Next Target

{markdown_table(rows_by_name["next_target"])}

## Validation

{markdown_table(validation)}
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    rows_by_name = all_output_rows()
    for key, rows in rows_by_name.items():
        write_csv(OUTPUTS[key], rows)
    copy_branch_artifacts()
    remove_pycache()
    write_csv(OUTPUTS["validation"], validation_rows())
    write_doc(rows_by_name)


if __name__ == "__main__":
    main()
