from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_START_UTC = datetime.now(timezone.utc)

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = PROJECT / "formalization-workbench"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "2880-Y5-R2FR-ZR-MR2-operator-normalization-or-range-source-row-under-AX1090.md"

SRC_2880_PREV_DOC = ROOT / "2879-Y5-R2FR-SR-over-ZR-source-map-or-source-zero-theorem-under-AX1090.md"
SRC_2879_NEXT = RESIDUALS / "P8_Y5_R2FR_2879_NEXT_TARGET.csv"
SRC_2879_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2879_VALIDATION.csv"
SRC_2879_FILL = RESIDUALS / "P8_Y5_R2FR_2879_SRZR_FILL_ATTEMPT.csv"
SRC_2878_RAW_QUEUE = RESIDUALS / "P8_Y5_R2FR_2878_RAW_COEFFICIENT_INTAKE_QUEUE.csv"
SRC_2878_DERIVATION = RESIDUALS / "P8_Y5_R2FR_2878_QREFF_NORMALIZATION_DERIVATION.csv"
SRC_2839_KERNEL = RESIDUALS / "P8_Y5_R2FR_2839_GREEN_KERNEL_NORMALIZATION.csv"
SRC_2840_CONTRACT = RESIDUALS / "P8_Y5_R2FR_2840_NORMALIZATION_PACK_CONTRACT.csv"
SRC_1625_BUILDER = RESIDUALS / "P8_Y5_PARENT_QLOC_1625_FINITE_ZR_PRIOR_ROW_BUILDER.csv"
SRC_1552_ACTION_TEMPLATE = RESIDUALS / "P8_Y5_PARENT_QLOC_1552_PARENT_QSECTOR_ACTION_TEMPLATE.csv"
SRC_1552_FAILURE_FILTERS = RESIDUALS / "P8_Y5_PARENT_QLOC_1552_ACTION_FAILURE_FILTERS.csv"
SRC_1553_ANSATZ = RESIDUALS / "P8_Y5_PARENT_QLOC_1553_MINIMAL_QSECTOR_ANSATZ_AUDIT.csv"
SRC_2210_COEFF_AUDIT = RESIDUALS / "P8_Y5_PARENT_QLOC_2210_PARENT_COEFFICIENT_AUDIT.csv"
SRC_2211_HVR = RESIDUALS / "P8_Y5_PARENT_QLOC_2211_HESSIAN_VS_RANGE_LEMMA.csv"
SRC_2211_ZM_AUDIT = RESIDUALS / "P8_Y5_PARENT_QLOC_2211_ZM_OWNER_AUDIT.csv"
SRC_2211_ACQ = RESIDUALS / "P8_Y5_PARENT_QLOC_2211_COEFFICIENT_ACQUISITION_ROWS.csv"
SRC_2211_GATE = RESIDUALS / "P8_Y5_PARENT_QLOC_2211_CLAIM_GATE.csv"
SRC_2212_PSA = RESIDUALS / "P8_Y5_PARENT_QLOC_2212_STRICT_L0_PRINCIPAL_SYMBOL_AUDIT.csv"
SRC_2214_MAP = RESIDUALS / "P8_Y5_PARENT_QLOC_2214_ALGEBRAIC_RESIDUAL_COEFFICIENT_MAP.csv"
SRC_2214_ACQ = RESIDUALS / "P8_Y5_PARENT_QLOC_2214_NONCLAIM_COEFFICIENT_ACQUISITION_ROWS.csv"
SRC_2215_LOCK = RESIDUALS / "P8_Y5_PARENT_QLOC_2215_MAB_LOCK_SIGNATURE_AUDIT.csv"
SRC_2215_THEOREM = RESIDUALS / "P8_Y5_PARENT_QLOC_2215_HESSIAN_LOCK_THEOREM_ATTEMPT.csv"
SRC_2215_ACQ = RESIDUALS / "P8_Y5_PARENT_QLOC_2215_MAB_SIGNATURE_ACQUISITION_ROWS.csv"
SRC_2215_DECISION = RESIDUALS / "P8_Y5_PARENT_QLOC_2215_DECISION_LEDGER.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2880_SOURCE_REGISTER.csv",
    "operator_law": RESIDUALS / "P8_Y5_R2FR_2880_OPERATOR_RANGE_LAW_AND_BRANCH_SPLIT.csv",
    "evidence": RESIDUALS / "P8_Y5_R2FR_2880_ZR_MR2_EVIDENCE_AUDIT.csv",
    "fill": RESIDUALS / "P8_Y5_R2FR_2880_ZR_MR2_ELLR_FILL_ATTEMPT.csv",
    "queue": RESIDUALS / "P8_Y5_R2FR_2880_OPERATOR_COEFFICIENT_ACQUISITION_QUEUE.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_2880_ACCEPTANCE_GATES.csv",
    "runner": RESIDUALS / "P8_Y5_R2FR_2880_RUNNER_STATUS.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2880_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2880_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2880_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2880_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "operator_law_copy": LOCAL_BOUNDS / "RAB_OPERATOR_RANGE_LAW_2880_NONCLAIM.csv",
    "queue_copy": SOURCE_WEIGHT / "RAB_OPERATOR_COEFFICIENT_ACQUISITION_QUEUE_2880_NONCLAIM.csv",
    "fill_copy": BETA_DOCS / "RAB_ZR_MR2_ELLR_FILL_ATTEMPT_2880_NONCLAIM.csv",
    "next_queue": RAB_QUEUE / "JR2880_matter_source_current_or_descent_zero_NEXT.csv",
}


for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": now(),
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def csv_parses(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2880_0_2879_doc", SRC_2880_PREV_DOC, "Status: `Y5_R2FR_2879_SRZR_source_map_contract_written_source_zero_rejected_operator_normalization_2880_next`;Z_R/M_R^2", "2879 handoff doc"),
        ("SRC2880_1_2879_next", SRC_2879_NEXT, "NEXT2879_0_2880", "2879 selected this target"),
        ("SRC2880_2_2879_validation", SRC_2879_VALIDATION, "VAL2879_OVERALL", "2879 validation"),
        ("SRC2880_3_2879_fill", SRC_2879_FILL, "FILL2879_0_SRZR_live_row_attempt", "S_R/Z_R refused"),
        ("SRC2880_4_2878_raw_queue", SRC_2878_RAW_QUEUE, "RAW2878_0_ZR;RAW2878_1_MR2", "operator coefficient queue"),
        ("SRC2880_5_2878_derivation", SRC_2878_DERIVATION, "DER2878_1_normalize_by_ZR;DER2878_2_range", "range algebra"),
        ("SRC2880_6_2839_kernel", SRC_2839_KERNEL, "KER2839_1_normalized_operator;KER2839_4_compact_body", "normalized operator"),
        ("SRC2880_7_2840_contract", SRC_2840_CONTRACT, "PACK2840_0_range;PACK2840_1_amplitude", "normalization contract"),
        ("SRC2880_8_1625_builder", SRC_1625_BUILDER, "PB1625_0_ZR;PB1625_1_MR2;PB1625_2_JR", "older coefficient builder"),
        ("SRC2880_9_1552_action_template", SRC_1552_ACTION_TEMPLATE, "ACT1552_1_quadratic_form;ACT1552_2_derivative_operator;ACT1552_6_parent_action_verdict", "q-sector parent action template"),
        ("SRC2880_10_1552_filters", SRC_1552_FAILURE_FILTERS, "FAIL1552_2_negative_mode;FAIL1552_3_zero_mode;FAIL1552_6_long_range_hair", "operator/action failure filters"),
        ("SRC2880_11_1553_ansatz", SRC_1553_ANSATZ, "ANS1553_1_massive_kinetic_q;ANS1553_6_current_verdict", "massive kinetic ansatz rejection"),
        ("SRC2880_12_2210_coeff", SRC_2210_COEFF_AUDIT, "PCA2210_0_Z_AB;PCA2210_1_M_AB;PCA2210_2_domain;PCA2210_3_source_split", "parent coefficient audit"),
        ("SRC2880_13_2211_hvr", SRC_2211_HVR, "HVR2211_0_hessian_not_range;HVR2211_1_finite_range_case;HVR2211_2_rank_zero_constraint_case;HVR2211_4_verdict", "Hessian/range lemma"),
        ("SRC2880_14_2211_zm", SRC_2211_ZM_AUDIT, "ZMO2211_0_parent_quadratic_form;ZMO2211_2_Z_kinetic_principal_symbol;ZMO2211_5_verdict", "Z/M ownership audit"),
        ("SRC2880_15_2211_acq", SRC_2211_ACQ, "ZMC2211_0_Z_AB_principal_symbol;ZMC2211_1_M_AB_Hessian;ZMC2211_3_source_current", "operator coefficient acquisition rows"),
        ("SRC2880_16_2211_gate", SRC_2211_GATE, "CG2211_1_Z_owner;CG2211_4_R10_score;CG2211_5_local_GR", "claim gates blocked"),
        ("SRC2880_17_2212_psa", SRC_2212_PSA, "PSA2212_0_strict_branch_definition;PSA2212_4_strict_verdict", "strict branch principal symbol audit"),
        ("SRC2880_18_2214_map", SRC_2214_MAP, "CM2214_0_M_inverse;CM2214_1_J_source;CM2214_7_verdict", "algebraic residual map"),
        ("SRC2880_19_2214_acq", SRC_2214_ACQ, "ACQ2214_0_M;ACQ2214_1_J;ACQ2214_8_LR10", "algebraic acquisition rows"),
        ("SRC2880_20_2215_lock", SRC_2215_LOCK, "LOCK2215_0_shape;LOCK2215_7_verdict", "M_AB lock signature audit"),
        ("SRC2880_21_2215_theorem", SRC_2215_THEOREM, "HLT2215_0_abstract_lock_theorem;HLT2215_3_verdict", "conditional algebraic lock theorem"),
        ("SRC2880_22_2215_acq", SRC_2215_ACQ, "MSA2215_0_parent_density;MSA2215_4_rank_sign;MSA2215_8_Khat_identity", "M_AB signature acquisition rows"),
        ("SRC2880_23_2215_decision", SRC_2215_DECISION, "DEC2215_2_next;DEC2215_3_scope", "parent Hessian signature handoff"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, anchors, role in specs:
        found, missing = anchors_present(path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_path": str(path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def operator_law_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "law_id": "LAW2880_0_normalized_scalar_operator",
            "statement": "If a parent quadratic action supplies E_R=-Div(Z_R Grad delta_R)+M_R^2 delta_R+S_R=0, then after same-normalization (-Laplace+M_R^2/Z_R)delta_R=-S_R/Z_R.",
            "branch_implication": "finite range is legal only after Z_R and M_R^2 are source-owned in the same operator convention",
            "current_status": "CONDITIONAL_ALGEBRA_ONLY",
            "source_path": str(SRC_2878_DERIVATION),
            "source_anchor": "DER2878_1_normalize_by_ZR",
            "accepted_operator_row": False,
        },
        {
            "law_id": "LAW2880_1_range_rule",
            "statement": "ell_R=sqrt(Z_R/M_R^2) for a one-mode positive branch, or lambda_i=1/mu_i from M v=mu_i^2 Z v in the multi-mode quotient.",
            "branch_implication": "range cannot be read from M_AB alone",
            "current_status": "CONDITIONAL_RANGE_RULE_READY_INPUTS_MISSING",
            "source_path": str(SRC_2211_HVR),
            "source_anchor": "HVR2211_1_finite_range_case",
            "accepted_operator_row": False,
        },
        {
            "law_id": "LAW2880_2_hessian_not_range",
            "statement": "An algebraic Hessian H_AB=M_AB by itself does not define a Yukawa range because range comes from the inverse of a differential operator with nonzero principal symbol.",
            "branch_implication": "M_AB can be an algebraic lock candidate, not direct ell_R evidence",
            "current_status": "PROVED_GATE_LEMMA_RETAINED",
            "source_path": str(SRC_2211_HVR),
            "source_anchor": "HVR2211_0_hessian_not_range",
            "accepted_operator_row": False,
        },
        {
            "law_id": "LAW2880_3_strict_rank_zero_branch",
            "statement": "If Z_R/Z_AB has no physical quotient rank, the strict branch equation is algebraic M_AB Z^B=S_A and no finite-range R10 lambda exists.",
            "branch_implication": "possible local-GR route becomes algebraic/source-current silence, not fifth-force screening",
            "current_status": "STRICT_BRANCH_CLASSIFIED_NONCLAIM",
            "source_path": str(SRC_2212_PSA),
            "source_anchor": "PSA2212_4_strict_verdict",
            "accepted_operator_row": False,
        },
        {
            "law_id": "LAW2880_4_current_verdict",
            "statement": "Current corpus supplies no accepted Z_R, M_R^2, Z_AB/M_AB pair, or direct ell_R source row.",
            "branch_implication": "keep q_R_eff blocked; do not score R10/PPN/local-GR from this route",
            "current_status": "OPERATOR_NORMALIZATION_NOT_FILLED",
            "source_path": str(SRC_2211_ZM_AUDIT),
            "source_anchor": "ZMO2211_5_verdict",
            "accepted_operator_row": False,
        },
    ]
    return [add_common(row) for row in rows]


def evidence_rows() -> list[dict[str, Any]]:
    rows = [
        ("EVID2880_0_ZR_raw", "Z_R", "MISSING_NUMERIC_VALUE", "2878 raw queue contains a target but no source-owned value", SRC_2878_RAW_QUEUE, "RAW2878_0_ZR"),
        ("EVID2880_1_MR2_raw", "M_R^2", "MISSING_NUMERIC_VALUE", "2878 raw queue contains a target but no source-owned value", SRC_2878_RAW_QUEUE, "RAW2878_1_MR2"),
        ("EVID2880_2_ZAB_parent", "Z_AB principal symbol", "MISSING_PARENT_RESIDUE", "2210 says no current source gives parent-owned Z_AB for q_loc branch", SRC_2210_COEFF_AUDIT, "PCA2210_0_Z_AB"),
        ("EVID2880_3_MAB_parent", "M_AB Hessian", "MISSING_PARENT_HESSIAN", "M_AB exists as a response-doublet shape but not a proven kinetic/mass operator", SRC_2210_COEFF_AUDIT, "PCA2210_1_M_AB"),
        ("EVID2880_4_derivative_template", "derivative operator", "TEMPLATE_OPTIONAL_ROUTE", "action template lists Z_AB kinetic terms but no parent-sourced coefficient", SRC_1552_ACTION_TEMPLATE, "ACT1552_2_derivative_operator"),
        ("EVID2880_5_massive_kinetic_ansatz", "massive kinetic q-sector", "REJECTED_HAIR_RISK_AND_PARENT_INPUTS_MISSING", "kinetic route can create exterior hair and lacks Z/M parent inputs", SRC_1553_ANSATZ, "ANS1553_1_massive_kinetic_q"),
        ("EVID2880_6_hessian_range_gate", "Hessian vs range", "RANGE_NOT_NUMERIC", "M_AB is algebraic curvature candidate, not range owner", SRC_2211_HVR, "HVR2211_4_verdict"),
        ("EVID2880_7_ZM_verdict", "Z_AB/M_AB owner", "NO_COEFFICIENT_OWNER_SIGNED_FINITE_RANGE_DEMOTED", "no kinetic principal symbol or live parent operator is signed", SRC_2211_ZM_AUDIT, "ZMO2211_5_verdict"),
        ("EVID2880_8_strict_branch", "strict fixed-L0 branch", "FINITE_RANGE_R10_REJECTED_FOR_STRICT_BRANCH", "no generalized eigenvalue problem when principal symbol is absent", SRC_2212_PSA, "PSA2212_4_strict_verdict"),
        ("EVID2880_9_M_lock", "M_AB lock", "MAB_LOCK_NOT_PARENT_SIGNED", "shape clause passes only nonclaim; parent density, units, domain, rank/sign and null/source compatibility fail", SRC_2215_LOCK, "LOCK2215_7_verdict"),
    ]
    return [
        add_common(
            {
                "evidence_id": evidence_id,
                "quantity": quantity,
                "status": status,
                "reason": reason,
                "source_path": str(path),
                "source_anchor": anchor,
                "accepted_live_input": False,
                "parent_signed": False,
            }
        )
        for evidence_id, quantity, status, reason, path, anchor in rows
    ]


def fill_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "fill_id": "FILL2880_0_ZR",
            "quantity": "Z_R",
            "candidate_value": "MISSING_Z_R",
            "units": "MISSING_OPERATOR_UNITS",
            "source_path": "MISSING_PARENT_QUADRATIC_ACTION_PATH",
            "equation_anchor": "MISSING_ZR_ANCHOR",
            "status": "FAILED_TO_FILL",
            "failure_mode": "no parent-owned kinetic/principal-symbol residue in current corpus",
            "accepted_live_input": False,
            "parent_signed": False,
        },
        {
            "fill_id": "FILL2880_1_MR2",
            "quantity": "M_R^2",
            "candidate_value": "MISSING_M_R2",
            "units": "MISSING_MASS_GAP_UNITS",
            "source_path": "MISSING_PARENT_HESSIAN_PATH",
            "equation_anchor": "MISSING_MR2_ANCHOR",
            "status": "FAILED_TO_FILL",
            "failure_mode": "M_AB is only a response-doublet Hessian candidate and lacks parent signature/units/rank",
            "accepted_live_input": False,
            "parent_signed": False,
        },
        {
            "fill_id": "FILL2880_2_ellR",
            "quantity": "ell_R",
            "candidate_value": "MISSING_ELL_R",
            "units": "length",
            "source_path": "MISSING_DIRECT_RANGE_PATH",
            "equation_anchor": "MISSING_RANGE_ANCHOR",
            "status": "FAILED_TO_FILL",
            "failure_mode": "no direct range row and no valid sqrt(Z_R/M_R^2) pair",
            "accepted_live_input": False,
            "parent_signed": False,
        },
        {
            "fill_id": "FILL2880_3_strict_algebraic_branch",
            "quantity": "rank-zero/algebraic branch",
            "candidate_value": "Z_R=0_strict_branch_NONCLAIM",
            "units": "n/a",
            "source_path": str(SRC_2212_PSA),
            "equation_anchor": "PSA2212_4_strict_verdict",
            "status": "CLASSIFIED_NOT_PROMOTED",
            "failure_mode": "strict branch would need M_AB lock, J_R/source silence, null projector and arena leakage bounds",
            "accepted_live_input": False,
            "parent_signed": False,
        },
    ]
    return [add_common(row) for row in rows]


def queue_rows() -> list[dict[str, Any]]:
    rows = [
        ("Q2880_0_ZR", "Z_R/Z_AB", "principal_symbol", "derive second variation derivative term from parent action or prove rank-zero on physical quotient", "MISSING_PARENT_RESIDUE", 1, False),
        ("Q2880_1_MR2", "M_R^2/M_AB", "Hessian_mass_gap", "derive parent Hessian with field basis, units, self-adjoint domain, rank/sign and null projector", "MISSING_PARENT_HESSIAN_SIGNATURE", 2, False),
        ("Q2880_2_ellR", "ell_R/lambda_i", "range", "source direct range or compute from same-normalized Z/M generalized eigenproblem", "MISSING_RANGE_OWNER", 3, False),
        ("Q2880_3_domain", "Dom(L_R)", "operator_domain", "derive boundary/no-flux/self-adjoint domain or include boundary charge", "MISSING_DOMAIN_CERTIFICATE", 4, False),
        ("Q2880_4_JR", "J_R", "matter_source_current", "derive matter-source current or matter descent zero theorem now that operator route did not fill", "MISSING_SOURCE_CURRENT", 5, True),
        ("Q2880_5_HR", "H_R", "boundary_homogeneous", "prove no-hair or carry finite boundary residual row", "MISSING_BOUNDARY_CLASS", 6, False),
        ("Q2880_6_tau", "tau_R10/tau_PPN/tau_clock/tau_orbital", "arena_projection", "map operator/algebraic branch into observables only after coefficients/source rows exist", "MISSING_ARENA_PROJECTION", 7, False),
    ]
    return [
        add_common(
            {
                "queue_id": queue_id,
                "symbol": symbol,
                "row_type": row_type,
                "needed_action": action,
                "current_marker": marker,
                "priority": priority,
                "accepted_live_input": False,
                "selected_for_next": selected,
            }
        )
        for queue_id, symbol, row_type, action, marker, priority, selected in rows
    ]


def gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE2880_0_range_law", "range law is mathematically written", "PASS_CONTROL_ONLY", "ell_R=sqrt(Z_R/M_R^2) or generalized eigenvalues are conditional laws, not live rows", False),
        ("GATE2880_1_ZR", "Z_R/Z_AB principal symbol is parent-owned", "FAIL", "Z_R and Z_AB remain missing parent residue", False),
        ("GATE2880_2_MR2", "M_R^2/M_AB Hessian is parent-owned", "FAIL", "M_AB shape exists only as nonclaim; rank/sign/units/domain missing", False),
        ("GATE2880_3_ellR", "direct or computed ell_R exists", "FAIL", "no valid direct range and no same-normalized Z/M pair", False),
        ("GATE2880_4_strict_branch", "rank-zero branch closes local GR by algebra", "FAIL", "M_AB lock, J_R/source silence, null projector and arena leakage remain open", False),
        ("GATE2880_5_qReff", "q_R_eff can be integrated/scored", "FAIL", "operator normalization and S_R/Z_R are both non-live", False),
        ("GATE2880_6_claim", "R10/PPN/local-GR claim can be made", "FAIL_CLOSED", "finite range, source, boundary and projection inputs are missing", False),
    ]
    return [
        add_common(
            {
                "gate_id": gate_id,
                "criterion": criterion,
                "result": result,
                "reason": reason,
                "gate_passed": passed,
            }
        )
        for gate_id, criterion, result, reason, passed in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "runner_id": "RUN2880_0_operator_import",
                "status": "REFUSED_OPERATOR_NORMALIZATION_NOT_LIVE",
                "accepted_operator_fields": 0,
                "required_operator_fields": 5,
                "reason": "no accepted Z_R, M_R^2, direct ell_R, domain, or source-current row exists",
                "runner_ready": False,
                "claim_unlocked": False,
                "score_allowed": False,
            }
        )
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2880_0_law", "Install the exact finite-range law.", "COMPLETE_CONTROL_ONLY", "range needs same-normalized operator pair, not an isolated Hessian"),
        ("DEC2880_1_hessian_guard", "Keep Hessian-not-range guard active.", "RETAINED_AS_GATE", "M_AB alone cannot be used as ell_R evidence"),
        ("DEC2880_2_strict_branch", "Classify strict fixed-L0 route as algebraic/rank-zero.", "CLASSIFIED_NONCLAIM", "no principal symbol means no R10 Yukawa lambda"),
        ("DEC2880_3_fill", "Try to fill Z_R, M_R^2 and ell_R.", "FAILED_NONCLAIM", "all parent coefficient/range rows remain missing"),
        ("DEC2880_4_next", "Route next to J_R matter-source current or matter-descent zero.", "SELECTED_2881", "after operator route fails, the next decisive numerator/source object is J_R"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "result": result,
                "because": because,
            }
        )
        for decision_id, decision, result, because in rows
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2880_0_2881",
                "status": "selected_primary",
                "target_doc": "2881-Y5-R2FR-JR-matter-source-current-or-matter-descent-zero-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_JR_matter_source_current_or_matter_descent_zero_under_AX1090_2881.py",
                "mission": "derive the parent matter-source current J_R or prove matter-descent zero for the residual channel; if neither closes, write source-current acquisition rows and keep q_R_eff blocked",
                "selected": True,
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    pairs = [
        ("COPY2880_0_operator_law", OUTPUTS["operator_law"], BRANCH_OUTPUTS["operator_law_copy"], "operator range law and branch split nonclaim copy"),
        ("COPY2880_1_queue", OUTPUTS["queue"], BRANCH_OUTPUTS["queue_copy"], "operator coefficient acquisition queue nonclaim copy"),
        ("COPY2880_2_fill", OUTPUTS["fill"], BRANCH_OUTPUTS["fill_copy"], "failed Z_R/M_R^2/ell_R fill attempt nonclaim copy"),
        ("COPY2880_3_next_queue", OUTPUTS["next"], BRANCH_OUTPUTS["next_queue"], "RAB queue handoff to J_R matter-source target"),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, destination, purpose in pairs:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_table": str(source),
                    "copy_path": str(destination),
                    "purpose": purpose,
                    "exists": destination.exists(),
                }
            )
        )
    return rows


def remove_pycache() -> None:
    pycache = Path(__file__).resolve().parent / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*"):
        if path.is_file():
            modified = datetime.fromtimestamp(path.stat().st_mtime, timezone.utc)
            if modified > SCRIPT_START_UTC:
                return False
    return True


def generated_under_root(paths: list[Path]) -> bool:
    root_resolved = ROOT.resolve()
    for path in paths:
        try:
            path.resolve().relative_to(root_resolved)
        except ValueError:
            return False
    return True


def no_claim_flags(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    claim_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "parent_signed",
        "accepted_operator_row",
        "accepted_live_input",
        "gate_passed",
        "runner_ready",
        "claim_unlocked",
        "score_allowed",
    }
    for rows in rows_by_name.values():
        for row in rows:
            for key in claim_keys:
                if row.get(key) is True:
                    return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sources = rows_by_name["sources"]
    law = rows_by_name["operator_law"]
    evidence = rows_by_name["evidence"]
    fill = rows_by_name["fill"]
    queue = rows_by_name["queue"]
    gates = rows_by_name["gates"]
    runner = rows_by_name["runner"]
    next_target = rows_by_name["next"]

    output_paths_without_validation = [path for key, path in OUTPUTS.items() if key != "validation"]
    branch_paths = list(BRANCH_OUTPUTS.values())
    all_generated_paths = output_paths_without_validation + branch_paths + [DOC, OUTPUTS["validation"]]

    checks = [
        ("VAL2880_0_sources_exist", all(row["path_exists"] for row in sources), "all registered source paths exist"),
        ("VAL2880_1_source_anchors", all(row["anchors_found"] for row in sources), "all registered source anchors were found"),
        ("VAL2880_2_operator_law_complete", len(law) == 5 and any(row["law_id"] == "LAW2880_2_hessian_not_range" for row in law), "operator/range law and Hessian guard recorded"),
        ("VAL2880_3_no_operator_promotion", not any(row["accepted_operator_row"] for row in law), "operator law remains control-only"),
        ("VAL2880_4_evidence_blocks_ZM", len(evidence) >= 10 and not any(row["accepted_live_input"] for row in evidence), "Z_R/M_R^2 evidence reviewed without promotion"),
        ("VAL2880_5_fill_refused", not any(row["accepted_live_input"] for row in fill) and all("MISSING" in row["candidate_value"] or row["status"] == "CLASSIFIED_NOT_PROMOTED" for row in fill), "Z_R/M_R^2/ell_R fill attempt refused"),
        ("VAL2880_6_queue_selects_JR", any(row["queue_id"] == "Q2880_4_JR" and row["selected_for_next"] is True for row in queue), "J_R selected as next numerator/source target"),
        ("VAL2880_7_gates_fail_closed", all(row["gate_passed"] is False for row in gates), "all operator claim gates fail closed"),
        ("VAL2880_8_runner_refused", runner[0]["status"] == "REFUSED_OPERATOR_NORMALIZATION_NOT_LIVE" and runner[0]["runner_ready"] is False, "runner remains refused"),
        ("VAL2880_9_next_target_2881", next_target[0]["next_id"] == "NEXT2880_0_2881" and next_target[0]["selected"] is True, "2881 J_R target selected"),
        ("VAL2880_10_outputs_exist", all(path.exists() for path in output_paths_without_validation), "all generated CSV outputs exist before validation write"),
        ("VAL2880_11_branch_outputs_exist", all(path.exists() for path in branch_paths) and all(row["exists"] for row in branch_rows), "branch copies were written"),
        ("VAL2880_12_csv_parse", all(csv_parses(path) for path in output_paths_without_validation + branch_paths), "all generated CSV outputs parse"),
        ("VAL2880_13_no_claim_flags", no_claim_flags(rows_by_name | {"branches": branch_rows}), "no claim/score/prediction flags are true"),
        ("VAL2880_14_generated_under_post_checkpoint", generated_under_root(all_generated_paths), "all generated artifacts remain under post-checkpoint-work"),
        ("VAL2880_15_formalization_untouched", formalization_untouched(), "formalization-workbench was not modified during this run"),
        ("VAL2880_16_pycache_absent", not (Path(__file__).resolve().parent / "__pycache__").exists(), "scripts __pycache__ absent during validation"),
    ]
    rows = [
        {
            "validation_id": validation_id,
            "passed": passed,
            "detail": detail,
            "timestamp_utc": now(),
        }
        for validation_id, passed, detail in checks
    ]
    rows.append(
        {
            "validation_id": "VAL2880_OVERALL",
            "passed": all(row["passed"] for row in rows),
            "detail": "2880 installed the operator/range law, preserved the Hessian-not-range guard, refused Z_R/M_R^2/ell_R promotion, and selected J_R matter-source derivation for 2881.",
            "timestamp_utc": now(),
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    separator = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        cells = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", " ").replace("|", "\\|")
            cells.append(value)
        body.append("| " + " | ".join(cells) + " |")
    return "\n".join([header, separator, *body])


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]], branch_rows: list[dict[str, Any]], validation: list[dict[str, Any]]) -> None:
    text = f"""# 2880 - Y5 R2FR Z_R M_R^2 Operator Normalization Or Range Source Row Under AX1090

Status: `Y5_R2FR_2880_operator_range_law_installed_ZR_MR2_ellR_not_filled_JR_2881_next`

## Private Verdict

2880 does not get a live `ell_R`, but it sharpens the route a lot.

The allowed finite-range law is:

`(-Laplace+M_R^2/Z_R)delta_R=-S_R/Z_R`, so `ell_R=sqrt(Z_R/M_R^2)` only if `Z_R` and `M_R^2` are parent-owned in the same normalization.

The critical guard is now explicit: `M_AB` or `M_R^2` alone is not a range. A Hessian can give an algebraic lock or mass curvature, but a Yukawa range needs a nonzero principal symbol/gradient residue. In the strict fixed-`L0` branch, the principal symbol is absent, so that branch is rank-zero/algebraic rather than finite-range R10.

Current corpus verdict: no accepted `Z_R`, no accepted `M_R^2`, no direct `ell_R`, and no local-GR/R10/PPN claim. Since the operator denominator route will not fill yet, the next best target is the numerator/source side: derive `J_R` or prove matter-descent zero.

## Source Register

{md_table(rows_by_name["sources"], ["source_id", "role", "path_exists", "anchors_found", "missing_anchors", "valid_for_claim"])}

## Operator Range Law And Branch Split

{md_table(rows_by_name["operator_law"], ["law_id", "statement", "branch_implication", "current_status", "accepted_operator_row", "valid_for_claim"])}

## Z_R/M_R^2 Evidence Audit

{md_table(rows_by_name["evidence"], ["evidence_id", "quantity", "status", "reason", "accepted_live_input", "parent_signed", "valid_for_claim"])}

## Z_R/M_R^2/ell_R Fill Attempt

{md_table(rows_by_name["fill"], ["fill_id", "quantity", "candidate_value", "units", "status", "failure_mode", "accepted_live_input", "valid_for_claim"])}

## Operator Coefficient Acquisition Queue

{md_table(rows_by_name["queue"], ["queue_id", "symbol", "row_type", "needed_action", "current_marker", "priority", "selected_for_next", "valid_for_claim"])}

## Acceptance Gates

{md_table(rows_by_name["gates"], ["gate_id", "criterion", "result", "reason", "gate_passed", "valid_for_claim"])}

## Runner Status

{md_table(rows_by_name["runner"], ["runner_id", "status", "accepted_operator_fields", "required_operator_fields", "reason", "runner_ready", "valid_for_claim"])}

## Decision Ledger

{md_table(rows_by_name["decision"], ["decision_id", "decision", "result", "because", "valid_for_claim"])}

## Next Target

{md_table(rows_by_name["next"], ["next_id", "status", "target_doc", "target_script", "mission", "selected", "valid_for_claim"])}

## Branch Copies

{md_table(branch_rows, ["copy_id", "source_table", "copy_path", "purpose", "exists", "valid_for_claim"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "timestamp_utc"])}
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    remove_pycache()

    rows_by_name = {
        "sources": source_register_rows(),
        "operator_law": operator_law_rows(),
        "evidence": evidence_rows(),
        "fill": fill_rows(),
        "queue": queue_rows(),
        "gates": gate_rows(),
        "runner": runner_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }

    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)

    branch_rows = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], branch_rows)
    rows_by_name["branches"] = branch_rows

    remove_pycache()
    validation = validation_rows(rows_by_name, branch_rows)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(rows_by_name, branch_rows, validation)
    remove_pycache()

    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation if row["validation_id"] == "VAL2880_OVERALL")
    print(f"VAL2880_OVERALL={overall['passed']}")


if __name__ == "__main__":
    main()
