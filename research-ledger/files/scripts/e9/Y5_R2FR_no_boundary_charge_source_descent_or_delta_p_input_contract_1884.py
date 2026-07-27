from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path
from typing import Any


BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
CHECKPOINT_ID = "1884"

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / CHECKPOINT_ID
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
QRHAT_DOCS = ROOT / "source-intake" / "qr-hat" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1884-Y5-R2FR-no-boundary-charge-source-descent-or-delta-p-input-contract.md"

INPUTS = {
    "1883_doc": ROOT / "1883-Y5-R2FR-reciprocal-lock-delta-p-zero-or-full-PPN-residual-vector.md",
    "1883_bridge": OUT / "P8_Y5_PARENT_QLOC_1883_DELTA_P_QRHAT_BRIDGE.csv",
    "1883_vector": OUT / "P8_Y5_PARENT_QLOC_1883_FULL_PPN_RESIDUAL_VECTOR.csv",
    "1883_validation": OUT / "P8_Y5_BRR545_1883_VALIDATION.csv",
    "11_cell_current": ROOT / "11-cell-current-origin-attempt.md",
    "12_gauge_noether": ROOT / "12-gauge-noether-origin-audit.md",
    "07_constraint": ROOT / "07-nonpropagating-reciprocity-constraint.md",
    "1240_qr_map": OUT / "P8_Y5_R10_1240_QR_TO_PPN_MAPPING_SCHEMA.csv",
    "1240_zero_attempt": OUT / "P8_Y5_R10_1240_QR_ZERO_CHARGE_THEOREM_ATTEMPT.csv",
    "1242_contract": OUT / "P8_Y5_R10_1242_QR_HAT_INPUT_CONTRACT.csv",
    "1246_doc": ROOT / "1246-Y5-R10-parent-QR-zero-theorem-or-finite-residual-source-hunt.md",
    "1249_rules": OUT / "P8_Y5_R10_1249_FINITE_QRHAT_VALIDATION_RULES.csv",
    "1254_doc": ROOT / "1254-Y5-R10-boundary-flux-source-template-or-phenomenological-qRhat-row.md",
    "1244_gm": OUT / "P8_Y5_R10_1244_GM_CONVENTION_PACK.csv",
}

SOURCE_NEEDLES = {
    "1883_doc": [
        "NO_BOUNDARY_CHARGE_SOURCE_DESCENT_OR_DELTA_P_INPUT_SELECTED_NEXT",
        "delta_p=-q_R_hat/2",
    ],
    "1883_bridge": [
        "DPB1883_1_QR_delta_p",
        "delta_p=-q_R_hat/2",
    ],
    "1883_vector": [
        "PPNV1883_0_delta_p_qR",
        "RESIDUAL_VECTOR_READY_NONCLAIM_ALL_SCORES_BLOCKED",
    ],
    "1883_validation": [
        "VAL1883_OVERALL,PASS",
    ],
    "11_cell_current": [
        "W partial_r R_AB = Q_R",
        "asymptotic flatness does not kill the reciprocal charge",
    ],
    "12_gauge_noether": [
        "first-class parent constraint",
        "not in the current scaffold",
    ],
    "07_constraint": [
        "S_constraint = integral lambda_R R_AB",
        "parent origin is still open",
    ],
    "1240_qr_map": [
        "QMAP1240_2_dimensionless_qR",
        "gamma_minus_1_QR",
    ],
    "1240_zero_attempt": [
        "ZQR1240_5_verdict",
        "ZERO_CHARGE_THEOREM_NOT_DERIVED",
    ],
    "1242_contract": [
        "zero_theorem_statement",
        "GM_convention",
    ],
    "1246_doc": [
        "QZT1246_3_nonprop_constraint",
        "WORKS_ONLY_IF_PARENT_SIGNED",
    ],
    "1249_rules": [
        "QRV1249_1_numeric",
        "REJECT_MISSING_OR_NONNUMERIC_QR",
    ],
    "1254_doc": [
        "REQ1254_2_raw_flux",
        "q_R_hat = Q_R c^2/(G M_source)",
    ],
    "1244_gm": [
        "q_R_hat = Q_R c^2/(G M_source)",
        "measured/dynamical GM",
    ],
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_1884_SOURCE_REGISTER.csv",
    "no_boundary_charge_audit": OUT / "P8_Y5_PARENT_QLOC_1884_NO_BOUNDARY_CHARGE_SOURCE_DESCENT_AUDIT.csv",
    "source_descent_matrix": OUT / "P8_Y5_PARENT_QLOC_1884_SOURCE_DESCENT_PREMISE_MATRIX.csv",
    "delta_p_qrhat_contract": OUT / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_INPUT_CONTRACT.csv",
    "candidate_template": OUT / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_CANDIDATE_TEMPLATE_NONCLAIM.csv",
    "dryrun_cases": OUT / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_VALIDATOR_DRYRUN_CASES.csv",
    "dryrun_results": OUT / "P8_Y5_PARENT_QLOC_1884_DELTA_P_QRHAT_VALIDATOR_DRYRUN_RESULTS.csv",
    "runner_refusal": OUT / "P8_Y5_PARENT_QLOC_1884_RUNNER_REFUSAL.csv",
    "claim_gate": OUT / "P8_Y5_PARENT_QLOC_1884_CLAIM_GATE.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_1884_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_1884_NEXT_TARGET.csv",
    "project_status": OUT / "P8_Y5_PARENT_QLOC_1884_PROJECT_STATUS_SNAPSHOT.csv",
    "validation": OUT / "P8_Y5_BRR545_1884_VALIDATION.csv",
}

TEMPLATE_DOC_COPY = QRHAT_DOCS / "DPQR1884_DELTA_P_QRHAT_INPUT_TEMPLATE_NONCLAIM.csv"


def ensure_dirs() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    QUEUE.mkdir(parents=True, exist_ok=True)
    QRHAT_DOCS.mkdir(parents=True, exist_ok=True)


def bool_string(value: Any) -> str:
    return str(value).strip().lower()


def is_placeholder(value: Any) -> bool:
    text = str(value).strip()
    if not text:
        return True
    markers = ("MISSING", "PLACEHOLDER", "TBD", "UNSIGNED", "HYPOTHETICAL")
    return any(marker in text.upper() for marker in markers)


def finite_float(value: Any) -> tuple[bool, float | None]:
    try:
        number = float(str(value).strip())
    except (TypeError, ValueError):
        return False, None
    return math.isfinite(number), number


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
                "usable_for_1884": ok,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def no_boundary_charge_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NBC1884_0_exterior_field_equation",
            "route": "vacuum reciprocal-current equation",
            "formal_statement": "If partial_r(W partial_r C_R)=J_R and J_R=0 outside the source, then W partial_r C_R=Q_R.",
            "attempt_result": "DERIVED_FROM_EXISTING_CURRENT_AUDIT",
            "blocker": "this identifies a conserved exterior charge but does not set it to zero",
            "claim_effect": "finite q_R_hat/delta_p branch remains live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NBC1884_1_exact_zero_flux_lemma",
            "route": "no-boundary-charge plus asymptotic reciprocity",
            "formal_statement": "If Q_R=0, W>0, J_R=0 in the exterior, and C_R(infinity)=0, then C_R is constant and C_R=0.",
            "attempt_result": "EXACT_CONDITIONAL_LEMMA",
            "blocker": "Q_R=0 is the missing parent theorem, not a consequence of asymptotic flatness alone",
            "claim_effect": "delta_p=0 follows only after no-boundary-charge is parent-signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NBC1884_2_delta_p_consequence",
            "route": "weak-field identity",
            "formal_statement": "C_R=2 delta_p U/c^2+O(U^2/c^4), so C_R=0 implies delta_p=0 at first PPN order.",
            "attempt_result": "EXACT_CONDITIONAL_CONSEQUENCE",
            "blocker": "depends on NBC1884_1 rather than replacing it",
            "claim_effect": "do not advertise derived local GR unless Q_R=0 is proven upstream",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NBC1884_3_qRhat_bridge",
            "route": "finite charge normalization",
            "formal_statement": "If exterior C_R=-Q_R/r and q_R_hat=Q_R c^2/(GM_source), then delta_p=-q_R_hat/2.",
            "attempt_result": "DERIVED_CONDITIONAL_BRIDGE_NONCLAIM",
            "blocker": "requires source-normalized GM convention plus a real Q_R value or theorem-zero",
            "claim_effect": "future finite rows must carry delta_p and q_R_hat consistently",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NBC1884_4_no_boundary_charge_parent_signature",
            "route": "first-class/no-boundary-charge theorem",
            "formal_statement": "The parent generator for reciprocal splitting has zero/proper boundary charge and ordinary sources carry no R_AB charge.",
            "attempt_result": "NOT_PARENT_SIGNED_CURRENT_CORPUS",
            "blocker": "no single parent action supplies generator, boundary term, source silence, matter/readout descent, and projection silence",
            "claim_effect": "Q_R=0 remains a target, not a theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NBC1884_5_closure_guard",
            "route": "lambda_R C_R closure",
            "formal_statement": "A parent-owned multiplier would kill the charge channel before exterior propagation.",
            "attempt_result": "WORKS_ONLY_IF_PARENT_SIGNED",
            "blocker": "inserting lambda_R by hand is closure in action language",
            "claim_effect": "can be benchmark branch but not evidence for derivation",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "NBC1884_6_verdict",
            "route": "no-boundary-charge/source-descent proof",
            "formal_statement": "Current MTS parent derives Q_R=0 and therefore delta_p=q_R_hat=0.",
            "attempt_result": "NO_BOUNDARY_CHARGE_NOT_PARENT_DERIVED",
            "blocker": "zero-flux lemma is exact but the no-boundary-charge/source-descent premises remain unsigned",
            "claim_effect": "build strict delta_p/q_R_hat input contract for full PPN vector",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def source_descent_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "premise_id": "SDM1884_0_parent_quotient_map",
            "premise": "parent quotient map removes reciprocal split before observables",
            "required_signature": "explicit q: Phi -> q(Phi) plus vertical reciprocal generator v_R in ker(Dq)",
            "current_evidence": "first-class route possible in principle but not constructed",
            "status": "MISSING_PARENT_INPUT",
            "failure_mode_if_absent": "R_AB remains a physical scalar/tail rather than gauge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "SDM1884_1_boundary_charge",
            "premise": "reciprocal generator has zero/proper boundary charge",
            "required_signature": "Q_R[epsilon] boundary term exists and vanishes for allowed local source class without imposing C_R=0",
            "current_evidence": "cell-current audit gives W C_R'=Q_R and permits exterior hair",
            "status": "MISSING_BOUNDARY_CHARGE_ZERO_THEOREM",
            "failure_mode_if_absent": "finite q_R_hat channel survives",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "SDM1884_2_source_silence",
            "premise": "ordinary local sources carry no reciprocal charge",
            "required_signature": "source current J_R or rho_R integrates to zero from source representation/topology",
            "current_evidence": "topological_zero_charge was named but not derived",
            "status": "MISSING_SOURCE_DESCENT",
            "failure_mode_if_absent": "matter can source Q_R even if vacuum exterior is conserved",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "SDM1884_3_matter_action_descent",
            "premise": "ordinary matter action descends to the quotient",
            "required_signature": "S_matter=Sbar[q(Phi),Psi,theta] with no representative Weyl/disformal/source prefactor residue",
            "current_evidence": "1883 full vector still carries b_R, w_R, d_R, endpoint and Khat channels",
            "status": "MISSING_MATTER_READOUT_DESCENT",
            "failure_mode_if_absent": "gamma may close while clocks, source normalization, or preferred-frame channels remain live",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "SDM1884_4_measure_connection_descent",
            "premise": "measure/coframe/connection terms do not reintroduce representative dependence",
            "required_signature": "no leftover Weyl, disformal, torsion, boundary, endpoint, or connection coefficient in local observables",
            "current_evidence": "projection kernels are explicitly missing in 1883",
            "status": "MISSING_ARENA_PROJECTION",
            "failure_mode_if_absent": "local GR can fail outside gamma even when C_R is small",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "SDM1884_5_GM_normalization",
            "premise": "same measured GM convention is used in q_R_hat and PPN comparator",
            "required_signature": "q_R_hat=Q_R c^2/(G M_source) tied to the source used in U=GM/r",
            "current_evidence": "1244/1254 provide convention language, but no Q_R value/source body",
            "status": "READY_CONTRACT_ONLY",
            "failure_mode_if_absent": "dimensionless q_R_hat can be numerically meaningless",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "premise_id": "SDM1884_6_no_cancellation_policy",
            "premise": "do not rescue a local pass by tuning independent residuals",
            "required_signature": "all active components of the full PPN vector are zero/bounded separately unless a parent identity kills them",
            "current_evidence": "1883 full-vector no-cancellation row exists",
            "status": "POLICY_READY_NONCLAIM",
            "failure_mode_if_absent": "gamma-only or cancellation-only pseudo-pass",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def delta_p_qrhat_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "DPQR1884_0_route_type",
            "field_name": "route_type",
            "required_for": "finite_or_zero",
            "accepted_content": "parent_zero_theorem | finite_qR_hat",
            "reject_if": "closure_benchmark, comparator_only, gamma_only, or cancellation_only",
            "reason": "forces the row to declare whether it is a theorem-zero or finite residual",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "DPQR1884_1_qRhat",
            "field_name": "q_R_hat",
            "required_for": "finite_qR_hat_or_parent_zero",
            "accepted_content": "finite dimensionless number; zero only with parent_zero_theorem",
            "reject_if": "missing marker, nonnumeric value, hidden closure zero, or comparator bound masquerading as prediction",
            "reason": "q_R_hat is the source-normalized charge input to the PPN bridge",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "DPQR1884_2_delta_p",
            "field_name": "delta_p",
            "required_for": "finite_qR_hat_or_parent_zero",
            "accepted_content": "finite number satisfying delta_p=-q_R_hat/2 within tolerance, or exactly zero for signed theorem route",
            "reject_if": "missing, nonnumeric, or inconsistent with the q_R_hat bridge",
            "reason": "prevents the full PPN vector from mixing unrelated first-order profile coefficients",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "DPQR1884_3_GM_convention",
            "field_name": "GM_convention",
            "required_for": "finite_qR_hat",
            "accepted_content": "same measured GM/source convention used in U=GM/r and local PPN comparator",
            "reject_if": "missing, placeholder, or not tied to q_R_hat=Q_R c^2/(G M_source)",
            "reason": "normalization is part of the prediction, not metadata decoration",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "DPQR1884_4_source_path",
            "field_name": "source_path",
            "required_for": "finite_or_zero",
            "accepted_content": "existing local path or explicit source/provenance id with no placeholder markers",
            "reject_if": "missing, MISSING_ marker, docs-only template used as evidence, or unsupported external string",
            "reason": "keeps future rows audit-trailed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "DPQR1884_5_zero_theorem_status",
            "field_name": "zero_theorem_status",
            "required_for": "parent_zero_theorem",
            "accepted_content": "PARENT_SIGNED_NO_BOUNDARY_CHARGE_SOURCE_DESCENT",
            "reject_if": "closure-only, comparator-only, unsigned, or GR-imported theorem",
            "reason": "zero rows are allowed only after the missing parent theorem exists",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "DPQR1884_6_descent_statuses",
            "field_name": "boundary_charge_status; source_descent_status; matter_descent_status; projection_status",
            "required_for": "parent_zero_theorem_or_local_claim",
            "accepted_content": "all signed/closed by the same parent package",
            "reject_if": "any MISSING_PARENT_INPUT, MISSING_SOURCE_DESCENT, MISSING_MATTER_READOUT_DESCENT, or MISSING_ARENA_PROJECTION remains",
            "reason": "local GR requires more than gamma closure",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "contract_id": "DPQR1884_7_claim_flags",
            "field_name": "valid_for_claim; claim_allowed",
            "required_for": "all_1884_rows",
            "accepted_content": "False in this checkpoint",
            "reject_if": "either flag is true",
            "reason": "1884 is a private derivation/input-contract checkpoint",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def candidate_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "candidate_id": "DPQR1884_TEMPLATE_PARENT_ZERO",
            "branch_id": BRANCH_ID,
            "route_type": "parent_zero_theorem",
            "delta_p": "0",
            "q_R_hat": "0",
            "relation": "delta_p=-q_R_hat/2",
            "relation_tolerance": "1e-12",
            "units": "dimensionless",
            "GM_convention": "not_required_for_theorem_but_required_if_scored_against_PPN",
            "source_path": "MISSING_PARENT_NO_BOUNDARY_CHARGE_SOURCE_DESCENT_THEOREM",
            "source_id": "MISSING_PARENT_SOURCE",
            "derivation_status": "parent_derived_zero_required",
            "zero_theorem_status": "MISSING_PARENT_INPUT",
            "boundary_charge_status": "MISSING_BOUNDARY_CHARGE_ZERO_THEOREM",
            "source_descent_status": "MISSING_SOURCE_DESCENT",
            "matter_descent_status": "MISSING_MATTER_READOUT_DESCENT",
            "projection_status": "MISSING_ARENA_PROJECTION",
            "closure_used": False,
            "comparator_only": False,
            "cancellation_only": False,
            "full_vector_ready": False,
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "candidate_id": "DPQR1884_TEMPLATE_FINITE_QRHAT",
            "branch_id": BRANCH_ID,
            "route_type": "finite_qR_hat",
            "delta_p": "MISSING_NUMERIC_DELTA_P",
            "q_R_hat": "MISSING_NUMERIC_Q_R_HAT",
            "relation": "delta_p=-q_R_hat/2",
            "relation_tolerance": "1e-12",
            "units": "dimensionless",
            "GM_convention": "MISSING_MEASURED_GM_SOURCE_CONVENTION",
            "source_path": "MISSING_SOURCE_PATH_OR_EXTERNAL_PROVENANCE",
            "source_id": "MISSING_SOURCE_ID",
            "derivation_status": "sourced_finite_model_or_parent_coefficients_required",
            "zero_theorem_status": "not_applicable",
            "boundary_charge_status": "finite_charge_branch_requires_Q_R_source",
            "source_descent_status": "finite_source_body_required",
            "matter_descent_status": "MISSING_MATTER_READOUT_DESCENT",
            "projection_status": "MISSING_ARENA_PROJECTION",
            "closure_used": False,
            "comparator_only": False,
            "cancellation_only": False,
            "full_vector_ready": False,
            "valid_prediction_row": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def dryrun_case_rows() -> list[dict[str, Any]]:
    existing_source = str(OUTPUTS["candidate_template"])
    return [
        {
            "case_id": "CASE1884_0_closure_zero",
            "route_type": "parent_zero_theorem",
            "delta_p": "0",
            "q_R_hat": "0",
            "GM_convention": "closure_not_needed",
            "source_path": str(INPUTS["07_constraint"]),
            "derivation_status": "closure_benchmark",
            "zero_theorem_status": "CLOSURE_ONLY",
            "boundary_charge_status": "CLOSURE_ONLY",
            "source_descent_status": "UNSIGNED",
            "matter_descent_status": "UNSIGNED",
            "projection_status": "UNSIGNED",
            "closure_used": True,
            "comparator_only": False,
            "cancellation_only": False,
            "full_vector_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1884_1_missing_finite",
            "route_type": "finite_qR_hat",
            "delta_p": "MISSING_NUMERIC_DELTA_P",
            "q_R_hat": "MISSING_NUMERIC_Q_R_HAT",
            "GM_convention": "MISSING_GM_CONVENTION",
            "source_path": "MISSING_SOURCE_PATH",
            "derivation_status": "sourced_finite_model",
            "zero_theorem_status": "not_applicable",
            "boundary_charge_status": "finite_charge_branch",
            "source_descent_status": "MISSING_SOURCE_BODY",
            "matter_descent_status": "UNSIGNED",
            "projection_status": "UNSIGNED",
            "closure_used": False,
            "comparator_only": False,
            "cancellation_only": False,
            "full_vector_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1884_2_comparator_bound",
            "route_type": "finite_qR_hat",
            "delta_p": "-1.15e-05",
            "q_R_hat": "2.3e-05",
            "GM_convention": "Cassini comparator only",
            "source_path": str(INPUTS["1883_vector"]),
            "derivation_status": "comparator_bound_not_prediction",
            "zero_theorem_status": "not_applicable",
            "boundary_charge_status": "not_supplied",
            "source_descent_status": "not_supplied",
            "matter_descent_status": "UNSIGNED",
            "projection_status": "UNSIGNED",
            "closure_used": False,
            "comparator_only": True,
            "cancellation_only": False,
            "full_vector_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1884_3_bad_relation",
            "route_type": "finite_qR_hat",
            "delta_p": "1.0e-06",
            "q_R_hat": "2.0e-05",
            "GM_convention": "q_R_hat=Q_R c^2/(G M_source); same measured GM as U=GM/r",
            "source_path": existing_source,
            "derivation_status": "schema_test_only",
            "zero_theorem_status": "not_applicable",
            "boundary_charge_status": "finite_charge_branch",
            "source_descent_status": "source_body_present_for_schema_test",
            "matter_descent_status": "UNSIGNED",
            "projection_status": "UNSIGNED",
            "closure_used": False,
            "comparator_only": False,
            "cancellation_only": False,
            "full_vector_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1884_4_zero_unsigned",
            "route_type": "parent_zero_theorem",
            "delta_p": "0",
            "q_R_hat": "0",
            "GM_convention": "same measured GM if scored",
            "source_path": str(INPUTS["1246_doc"]),
            "derivation_status": "parent_derived_zero",
            "zero_theorem_status": "UNSIGNED_NO_BOUNDARY_CHARGE",
            "boundary_charge_status": "MISSING_BOUNDARY_CHARGE_ZERO_THEOREM",
            "source_descent_status": "MISSING_SOURCE_DESCENT",
            "matter_descent_status": "MISSING_MATTER_READOUT_DESCENT",
            "projection_status": "MISSING_ARENA_PROJECTION",
            "closure_used": False,
            "comparator_only": False,
            "cancellation_only": False,
            "full_vector_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1884_5_gamma_only",
            "route_type": "finite_qR_hat",
            "delta_p": "-1.0e-06",
            "q_R_hat": "2.0e-06",
            "GM_convention": "q_R_hat=Q_R c^2/(G M_source); same measured GM as U=GM/r",
            "source_path": existing_source,
            "derivation_status": "schema_test_only",
            "zero_theorem_status": "not_applicable",
            "boundary_charge_status": "finite_charge_branch",
            "source_descent_status": "source_body_present_for_schema_test",
            "matter_descent_status": "UNSIGNED",
            "projection_status": "UNSIGNED",
            "closure_used": False,
            "comparator_only": False,
            "cancellation_only": False,
            "full_vector_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1884_6_cancellation_tuned",
            "route_type": "finite_qR_hat",
            "delta_p": "1.0e-04",
            "q_R_hat": "-2.0e-04",
            "GM_convention": "q_R_hat=Q_R c^2/(G M_source); same measured GM as U=GM/r",
            "source_path": existing_source,
            "derivation_status": "schema_test_only",
            "zero_theorem_status": "not_applicable",
            "boundary_charge_status": "finite_charge_branch",
            "source_descent_status": "source_body_present_for_schema_test",
            "matter_descent_status": "UNSIGNED",
            "projection_status": "UNSIGNED",
            "closure_used": False,
            "comparator_only": False,
            "cancellation_only": True,
            "full_vector_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "case_id": "CASE1884_7_schema_complete_nonclaim",
            "route_type": "finite_qR_hat",
            "delta_p": "-1.0e-06",
            "q_R_hat": "2.0e-06",
            "GM_convention": "q_R_hat=Q_R c^2/(G M_source); same measured GM as U=GM/r",
            "source_path": existing_source,
            "derivation_status": "schema_test_only_not_physics_evidence",
            "zero_theorem_status": "not_applicable",
            "boundary_charge_status": "finite_charge_branch_schema_ready",
            "source_descent_status": "source_body_present_for_schema_test",
            "matter_descent_status": "SIGNED_FOR_SCHEMA_TEST",
            "projection_status": "SIGNED_FOR_SCHEMA_TEST",
            "closure_used": False,
            "comparator_only": False,
            "cancellation_only": False,
            "full_vector_ready": True,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def validate_dryrun_case(row: dict[str, Any]) -> dict[str, Any]:
    route_type = str(row.get("route_type", "")).strip()
    delta_ok, delta_p = finite_float(row.get("delta_p", ""))
    qr_ok, q_r_hat = finite_float(row.get("q_R_hat", ""))
    closure_used = bool_string(row.get("closure_used", "")) == "true"
    comparator_only = bool_string(row.get("comparator_only", "")) == "true"
    cancellation_only = bool_string(row.get("cancellation_only", "")) == "true"
    full_vector_ready = bool_string(row.get("full_vector_ready", "")) == "true"

    rejection = ""
    relation_residual = "not_evaluated"
    valid_prediction_row = False
    score_ready = False

    if bool_string(row.get("valid_for_claim", "")) != "false" or bool_string(row.get("claim_allowed", "")) != "false":
        rejection = "REFUSED_CLAIM_FLAG"
    elif closure_used:
        rejection = "REFUSED_CLOSURE_NOT_EVIDENCE"
    elif comparator_only:
        rejection = "REFUSED_COMPARATOR_ONLY"
    elif cancellation_only:
        rejection = "REFUSED_CANCELLATION_ONLY"
    elif route_type not in {"finite_qR_hat", "parent_zero_theorem"}:
        rejection = "REFUSED_BAD_ROUTE_TYPE"
    elif route_type == "parent_zero_theorem":
        if not (delta_ok and qr_ok and abs(delta_p or 0.0) <= 1e-12 and abs(q_r_hat or 0.0) <= 1e-12):
            rejection = "REFUSED_ZERO_THEOREM_NUMERIC_MISMATCH"
        elif str(row.get("zero_theorem_status", "")) != "PARENT_SIGNED_NO_BOUNDARY_CHARGE_SOURCE_DESCENT":
            rejection = "REFUSED_ZERO_THEOREM_UNSIGNED"
        elif any(
            "MISSING" in str(row.get(field, "")).upper() or "UNSIGNED" in str(row.get(field, "")).upper()
            for field in ("boundary_charge_status", "source_descent_status", "matter_descent_status", "projection_status")
        ):
            rejection = "REFUSED_MISSING_DESCENT_PREMISES"
        else:
            valid_prediction_row = True
            score_ready = full_vector_ready
            rejection = "SCHEMA_READY_ZERO_ROUTE_NONCLAIM" if full_vector_ready else "SCHEMA_READY_BUT_VECTOR_INCOMPLETE"
    else:
        if not (delta_ok and qr_ok):
            rejection = "REFUSED_MISSING_OR_NONNUMERIC_DELTA_P_OR_QRHAT"
        elif str(row.get("units", "dimensionless")).strip() not in {"", "dimensionless"}:
            rejection = "REFUSED_BAD_UNITS"
        elif is_placeholder(row.get("GM_convention", "")):
            rejection = "REFUSED_MISSING_GM_CONVENTION"
        elif is_placeholder(row.get("source_path", "")):
            rejection = "REFUSED_MISSING_SOURCE"
        else:
            relation_residual_value = abs((delta_p or 0.0) + 0.5 * (q_r_hat or 0.0))
            relation_residual = f"{relation_residual_value:.12g}"
            if relation_residual_value > 1e-12:
                rejection = "REFUSED_DELTA_P_QRHAT_RELATION_MISMATCH"
            elif "schema_test_only" in str(row.get("derivation_status", "")):
                valid_prediction_row = True
                score_ready = False
                rejection = "SCHEMA_MATH_ONLY_NOT_EVIDENCE"
            elif not full_vector_ready:
                valid_prediction_row = True
                score_ready = False
                rejection = "SCHEMA_READY_BUT_VECTOR_INCOMPLETE"
            else:
                valid_prediction_row = True
                score_ready = True
                rejection = "SCHEMA_READY_NONCLAIM"

    if row.get("case_id") == "CASE1884_5_gamma_only" and rejection == "SCHEMA_MATH_ONLY_NOT_EVIDENCE":
        rejection = "REFUSED_GAMMA_ONLY_INCOMPLETE_VECTOR"

    result = dict(row)
    result.update(
        {
            "relation_residual": relation_residual,
            "validator_status": rejection,
            "valid_prediction_row": valid_prediction_row,
            "score_ready": score_ready,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    )
    return result


def dryrun_result_rows() -> list[dict[str, Any]]:
    return [validate_dryrun_case(row) for row in dryrun_case_rows()]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1884_0_no_boundary_charge_proof_checker",
            "runner": "no-boundary-charge/source-descent proof checker",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "zero-flux lemma is exact but parent no-boundary-charge/source-descent premises are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1884_1_delta_p_qrhat_input_validator",
            "runner": "delta_p/q_R_hat source-normalized row validator",
            "current_status": "ALLOW_SCHEMA_DRYRUN_NONCLAIM",
            "reason": "contract and failure modes work, but no live sourced row is supplied",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "runner_id": "RUN1884_2_full_ppn_vector_scorer",
            "runner": "full local PPN residual-vector scorer",
            "current_status": "REFUSE_CLAIM_RUN",
            "reason": "delta_p/q_R_hat row is missing and beta/preferred/source/endpoint/Khat channels remain open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1884_0_conditional_lemma",
            "claim": "if Q_R=0 and C_R(infinity)=0 then delta_p=0",
            "status": "PASS_CONDITIONAL_NONCLAIM",
            "reason": "mathematically exact as a lemma, not a parent theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1884_1_parent_zero",
            "claim": "MTS parent derives Q_R=0",
            "status": "BLOCKED",
            "reason": "boundary charge, source silence, matter/readout descent, and projection silence are unsigned",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1884_2_delta_p_qrhat_row",
            "claim": "delta_p/q_R_hat input row is available for local PPN scoring",
            "status": "BLOCKED",
            "reason": "only templates and dryrun cases exist; no live sourced row is accepted",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1884_3_local_gr",
            "claim": "local GR/Newton limit is derived",
            "status": "BLOCKED",
            "reason": "full PPN vector still lacks parent-signed zeros or finite source-normalized values",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1884_0_zero_flux_lemma_kept",
            "decision": "KEEP_EXACT_CONDITIONAL_ZERO_FLUX_LEMMA",
            "because": "Q_R=0 plus exterior silence and asymptotic reciprocity really does force C_R=0 and delta_p=0",
            "next_action": "do not discard the route; hunt for the parent no-boundary-charge/source-descent signature",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1884_1_no_parent_zero_claim",
            "decision": "NO_BOUNDARY_CHARGE_NOT_PARENT_DERIVED",
            "because": "the current corpus proves conservation of Q_R more easily than absence of Q_R",
            "next_action": "treat theorem-zero rows as blocked until all descent premises are signed",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1884_2_contract_fallback",
            "decision": "DELTA_P_QRHAT_INPUT_CONTRACT_BUILT_NONCLAIM",
            "because": "if the proof route remains unsigned, the full PPN vector needs a source-normalized finite input instead of a hand-set closure",
            "next_action": "attack beta/source coupling or produce a real parent-signed zero/finite row",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1884_0_primary",
            "selection_status": "selected",
            "target_file": "1885-Y5-R2FR-beta-second-order-source-coupling-gate-or-parent-zero-row.md",
            "target_script": "scripts/Y5_R2FR_beta_second_order_source_coupling_gate_or_parent_zero_row_1885.py",
            "objective": "keep the derivation-first route live by attacking the next full-vector blocker: either parent-sign a real zero/finite delta_p-q_R_hat row, or derive the beta/source-coupling second-order gate needed for local GR",
            "success_condition": "a parent-signed zero/finite input row with all descent premises, or a strict beta/source-coupling contract that prevents gamma-only local claims",
            "do_not_do": "do not use closure, comparator bounds, GR Schwarzschild AB=1, or cancellation-tuning as evidence",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def project_status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "PSTAT1884_0_gain",
            "topic": "local GR route",
            "status": "ZERO_FLUX_LEMMA_EXACT_BUT_UNSIGNED",
            "risk_level": "HIGH_VALUE_OPEN_PROOF",
            "detail": "we now know exactly what must be parent-signed for q_R_hat=delta_p=0",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "PSTAT1884_1_blocker",
            "topic": "full PPN scoring",
            "status": "INPUT_CONTRACT_READY_NO_LIVE_ROW",
            "risk_level": "MAIN_BOTTLENECK",
            "detail": "delta_p/q_R_hat, beta, source coupling, preferred-frame and endpoint/Khat channels are still not scored as MTS predictions",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "status_id": "PSTAT1884_2_best_attack",
            "topic": "next route",
            "status": "BETA_SOURCE_COUPLING_OR_PARENT_ZERO_ROW",
            "risk_level": "NEXT_BEST_MOVE",
            "detail": "gamma is no longer enough; the safest route is source coupling/beta derivation while keeping theorem-zero acquisition open",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def all_output_rows() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "no_boundary_charge_audit": no_boundary_charge_audit_rows(),
        "source_descent_matrix": source_descent_matrix_rows(),
        "delta_p_qrhat_contract": delta_p_qrhat_contract_rows(),
        "candidate_template": candidate_template_rows(),
        "dryrun_cases": dryrun_case_rows(),
        "dryrun_results": dryrun_result_rows(),
        "runner_refusal": runner_refusal_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "project_status": project_status_rows(),
    }


def csv_parse_check(paths: list[Path]) -> tuple[bool, str]:
    details: list[str] = []
    ok = True
    for path in paths:
        try:
            rows = csv_rows(path)
            details.append(f"{path.name}:{len(rows)}")
        except Exception as exc:  # pragma: no cover - validation report path
            ok = False
            details.append(f"{path.name}:ERROR:{exc}")
    return ok, "; ".join(details)


def all_claim_flags_false(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            for field in ("valid_for_claim", "claim_allowed"):
                if field in row and bool_string(row[field]) != "false":
                    bad.append(f"{path.name}:line{index}:{field}={row[field]}")
    return not bad, "all claim flags false" if not bad else "; ".join(bad)


def missing_statuses_not_claim_ready(paths: list[Path]) -> tuple[bool, str]:
    bad: list[str] = []
    for path in paths:
        for index, row in enumerate(csv_rows(path), start=2):
            row_text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in row_text or "UNSIGNED" in row_text or "CLOSURE" in row_text:
                if bool_string(row.get("valid_for_claim", "false")) != "false" or bool_string(row.get("claim_allowed", "false")) != "false":
                    bad.append(f"{path.name}:line{index}:claim flag with missing/unsigned/closure")
                if bool_string(row.get("score_ready", "false")) == "true":
                    bad.append(f"{path.name}:line{index}:score_ready with missing/unsigned/closure")
    return not bad, "missing/unsigned/closure rows are not claim-ready" if not bad else "; ".join(bad)


def copy_branch_artifacts() -> None:
    copy_pairs = [
        (OUTPUTS["no_boundary_charge_audit"], MICROSCOPE_RESIDUALS / OUTPUTS["no_boundary_charge_audit"].name),
        (OUTPUTS["delta_p_qrhat_contract"], QUEUE / "JR1884_DELTA_P_QRHAT_INPUT_CONTRACT_NONCLAIM.csv"),
        (OUTPUTS["candidate_template"], TEMPLATE_DOC_COPY),
        (OUTPUTS["dryrun_results"], QUARANTINE / OUTPUTS["dryrun_results"].name),
    ]
    for src, dst in copy_pairs:
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def validation_rows() -> list[dict[str, Any]]:
    generated_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    checks: list[dict[str, Any]] = []

    sources = csv_rows(OUTPUTS["source_register"])
    source_count = len(sources)
    source_ok = sum(1 for row in sources if bool_string(row["source_exists"]) == "true")
    needle_ok = sum(1 for row in sources if row["needle_check"] == "OK")
    checks.append(
        {
            "validation_id": "VAL1884_0_sources_exist",
            "status": "PASS" if source_ok == source_count else "FAIL",
            "detail": f"{source_ok}/{source_count} sources exist",
            "valid_for_claim": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1884_1_needles_found",
            "status": "PASS" if needle_ok == source_count else "FAIL",
            "detail": f"{needle_ok}/{source_count} source needles found",
            "valid_for_claim": False,
        }
    )

    audit = csv_rows(OUTPUTS["no_boundary_charge_audit"])
    checks.append(
        {
            "validation_id": "VAL1884_2_zero_flux_lemma",
            "status": "PASS"
            if any(row["audit_id"] == "NBC1884_1_exact_zero_flux_lemma" and row["attempt_result"] == "EXACT_CONDITIONAL_LEMMA" for row in audit)
            else "FAIL",
            "detail": "Q_R=0 plus exterior/asymptotic conditions forces C_R=0 conditionally",
            "valid_for_claim": False,
        }
    )
    checks.append(
        {
            "validation_id": "VAL1884_3_no_parent_zero_promotion",
            "status": "PASS"
            if any(row["audit_id"] == "NBC1884_6_verdict" and row["attempt_result"] == "NO_BOUNDARY_CHARGE_NOT_PARENT_DERIVED" for row in audit)
            else "FAIL",
            "detail": "no-boundary-charge/source-descent proof is not promoted",
            "valid_for_claim": False,
        }
    )

    matrix = csv_rows(OUTPUTS["source_descent_matrix"])
    missing_codes = {"MISSING_PARENT_INPUT", "MISSING_BOUNDARY_CHARGE_ZERO_THEOREM", "MISSING_SOURCE_DESCENT", "MISSING_MATTER_READOUT_DESCENT", "MISSING_ARENA_PROJECTION"}
    checks.append(
        {
            "validation_id": "VAL1884_4_descent_blockers_explicit",
            "status": "PASS" if missing_codes.issubset({row["status"] for row in matrix}) else "FAIL",
            "detail": "parent, boundary, source, matter/readout and projection blockers recorded",
            "valid_for_claim": False,
        }
    )

    contract = csv_rows(OUTPUTS["delta_p_qrhat_contract"])
    required_fields = {"route_type", "q_R_hat", "delta_p", "GM_convention", "source_path", "zero_theorem_status", "boundary_charge_status; source_descent_status; matter_descent_status; projection_status"}
    checks.append(
        {
            "validation_id": "VAL1884_5_contract_fields",
            "status": "PASS" if required_fields.issubset({row["field_name"] for row in contract}) else "FAIL",
            "detail": f"contract_fields={len(contract)}",
            "valid_for_claim": False,
        }
    )

    templates = csv_rows(OUTPUTS["candidate_template"])
    checks.append(
        {
            "validation_id": "VAL1884_6_templates_nonclaim",
            "status": "PASS"
            if len(templates) == 2
            and all(bool_string(row["valid_for_claim"]) == "false" and bool_string(row["claim_allowed"]) == "false" for row in templates)
            and any("MISSING" in " ".join(row.values()).upper() for row in templates)
            else "FAIL",
            "detail": "parent-zero and finite-qRhat templates remain nonclaim with missing markers",
            "valid_for_claim": False,
        }
    )

    dryruns = csv_rows(OUTPUTS["dryrun_results"])
    expected_statuses = {
        "REFUSED_CLOSURE_NOT_EVIDENCE",
        "REFUSED_MISSING_OR_NONNUMERIC_DELTA_P_OR_QRHAT",
        "REFUSED_COMPARATOR_ONLY",
        "REFUSED_DELTA_P_QRHAT_RELATION_MISMATCH",
        "REFUSED_ZERO_THEOREM_UNSIGNED",
        "REFUSED_GAMMA_ONLY_INCOMPLETE_VECTOR",
        "REFUSED_CANCELLATION_ONLY",
        "SCHEMA_MATH_ONLY_NOT_EVIDENCE",
    }
    checks.append(
        {
            "validation_id": "VAL1884_7_dryrun_failure_modes",
            "status": "PASS" if expected_statuses.issubset({row["validator_status"] for row in dryruns}) else "FAIL",
            "detail": f"dryrun_statuses={','.join(row['validator_status'] for row in dryruns)}",
            "valid_for_claim": False,
        }
    )

    runners = csv_rows(OUTPUTS["runner_refusal"])
    checks.append(
        {
            "validation_id": "VAL1884_8_runner_refusal",
            "status": "PASS"
            if any(row["current_status"] == "ALLOW_SCHEMA_DRYRUN_NONCLAIM" for row in runners)
            and sum(1 for row in runners if row["current_status"] == "REFUSE_CLAIM_RUN") == 2
            else "FAIL",
            "detail": "proof/full-vector claim runs refuse while schema dryrun is allowed nonclaim",
            "valid_for_claim": False,
        }
    )

    claims = csv_rows(OUTPUTS["claim_gate"])
    checks.append(
        {
            "validation_id": "VAL1884_9_claim_gates",
            "status": "PASS"
            if any(row["status"] == "PASS_CONDITIONAL_NONCLAIM" for row in claims)
            and sum(1 for row in claims if row["status"] == "BLOCKED") == 3
            else "FAIL",
            "detail": "only the conditional lemma passes; parent-zero/local-GR gates remain blocked",
            "valid_for_claim": False,
        }
    )

    decisions = csv_rows(OUTPUTS["decision"])
    checks.append(
        {
            "validation_id": "VAL1884_10_decision_ledger",
            "status": "PASS"
            if any(row["decision"] == "NO_BOUNDARY_CHARGE_NOT_PARENT_DERIVED" for row in decisions)
            and any(row["decision"] == "DELTA_P_QRHAT_INPUT_CONTRACT_BUILT_NONCLAIM" for row in decisions)
            else "FAIL",
            "detail": "decision records failed proof promotion and strict fallback contract",
            "valid_for_claim": False,
        }
    )

    next_targets = csv_rows(OUTPUTS["next_target"])
    checks.append(
        {
            "validation_id": "VAL1884_11_next_target",
            "status": "PASS"
            if any(row["route_id"] == "NEXT1884_0_primary" and row["selection_status"] == "selected" for row in next_targets)
            else "FAIL",
            "detail": "1885 beta/source-coupling or parent-zero row selected",
            "valid_for_claim": False,
        }
    )

    status_rows = csv_rows(OUTPUTS["project_status"])
    checks.append(
        {
            "validation_id": "VAL1884_12_project_status",
            "status": "PASS" if any(row["risk_level"] == "MAIN_BOTTLENECK" for row in status_rows) else "FAIL",
            "detail": "project status snapshot keeps full-vector bottleneck visible",
            "valid_for_claim": False,
        }
    )

    flags_ok, flags_detail = all_claim_flags_false(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1884_13_claim_flags_false",
            "status": "PASS" if flags_ok else "FAIL",
            "detail": flags_detail,
            "valid_for_claim": False,
        }
    )

    missing_ok, missing_detail = missing_statuses_not_claim_ready(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1884_14_missing_not_ready",
            "status": "PASS" if missing_ok else "FAIL",
            "detail": missing_detail,
            "valid_for_claim": False,
        }
    )

    parse_ok, parse_detail = csv_parse_check(generated_without_validation)
    checks.append(
        {
            "validation_id": "VAL1884_15_csv_parse",
            "status": "PASS" if parse_ok else "FAIL",
            "detail": parse_detail,
            "valid_for_claim": False,
        }
    )

    copied_paths = [
        MICROSCOPE_RESIDUALS / OUTPUTS["no_boundary_charge_audit"].name,
        QUEUE / "JR1884_DELTA_P_QRHAT_INPUT_CONTRACT_NONCLAIM.csv",
        TEMPLATE_DOC_COPY,
        QUARANTINE / OUTPUTS["dryrun_results"].name,
    ]
    checks.append(
        {
            "validation_id": "VAL1884_16_branch_copies",
            "status": "PASS" if all(path.exists() for path in copied_paths) else "FAIL",
            "detail": ";".join(str(path) for path in copied_paths),
            "valid_for_claim": False,
        }
    )

    pycache = Path(__file__).resolve().parent / "__pycache__"
    checks.append(
        {
            "validation_id": "VAL1884_17_pycache_absent",
            "status": "PASS" if not pycache.exists() else "FAIL",
            "detail": str(pycache),
            "valid_for_claim": False,
        }
    )

    formalization_hits = list(FORMALIZATION.rglob("*1884*")) if FORMALIZATION.exists() else []
    checks.append(
        {
            "validation_id": "VAL1884_18_formalization_untouched",
            "status": "PASS" if not formalization_hits else "FAIL",
            "detail": f"formalization_1884_count={len(formalization_hits)}",
            "valid_for_claim": False,
        }
    )

    fail_count = sum(1 for row in checks if row["status"] != "PASS")
    checks.append(
        {
            "validation_id": "VAL1884_OVERALL",
            "status": "PASS" if fail_count == 0 else "FAIL",
            "detail": "1884 no-boundary-charge/source-descent or delta_p/q_R_hat input contract",
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
    content = f"""# 1884 - No Boundary Charge Source Descent Or Delta_p Input Contract

**Private status:** derivation-first proof attempt plus strict nonclaim fallback contract.

## Result

1884 gets one useful theorem-shaped piece, but not the full theorem:

```text
partial_r(W partial_r C_R)=J_R
J_R=0 outside the source
W partial_r C_R=Q_R
Q_R=0 and C_R(infinity)=0  =>  C_R=0  =>  delta_p=0
```

That is an exact conditional zero-flux lemma. The sting is that current corpus still does **not** parent-sign `Q_R=0`. The no-boundary-charge/source-descent package is missing the parent generator, boundary charge theorem, ordinary-source silence, matter/readout descent, and projection silence in one action.

So the local branch is not dead, but the route is disciplined: either prove the missing parent no-charge theorem, or feed the full PPN vector with a real source-normalized `delta_p/q_R_hat` row. Closure zero, comparator-only rows, gamma-only rows, and cancellation tuning are refused.

## No-Boundary-Charge Audit

{markdown_table(rows_by_name["no_boundary_charge_audit"])}

## Source Descent Premise Matrix

{markdown_table(rows_by_name["source_descent_matrix"])}

## Delta_p / q_R_hat Input Contract

{markdown_table(rows_by_name["delta_p_qrhat_contract"])}

## Candidate Template

{markdown_table(rows_by_name["candidate_template"])}

## Validator Dry-Run Cases

{markdown_table(rows_by_name["dryrun_cases"])}

## Validator Dry-Run Results

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
