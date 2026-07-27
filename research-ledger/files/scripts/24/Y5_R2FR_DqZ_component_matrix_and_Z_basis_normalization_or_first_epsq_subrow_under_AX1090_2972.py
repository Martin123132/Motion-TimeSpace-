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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
SOURCE_WEIGHT = ROOT / "source-intake" / "source-weight"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "2972"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
RUN_UTC = SCRIPT_START_UTC.isoformat()

DOC = ROOT / "2972-Y5-R2FR-DqZ-component-matrix-and-Z-basis-normalization-or-first-epsq-subrow-under-AX1090.md"

SRC_2971_DOC = ROOT / "2971-Y5-R2FR-first-DqZ-JA-leakage-coefficient-acquisition-or-theorem-zero-under-AX1090.md"
SRC_2971_NEXT = RESIDUALS / "P8_Y5_R2FR_2971_NEXT_TARGET.csv"
SRC_2971_ACQ = RESIDUALS / "P8_Y5_R2FR_2971_COEFFICIENT_ACQUISITION_AUDIT.csv"
SRC_2971_SPLIT = RESIDUALS / "P8_Y5_R2FR_2971_SUBCOEFFICIENT_SPLIT_ROWS_NONCLAIM.csv"
SRC_2971_VALIDATION = RESIDUALS / "P8_Y5_BRR545_2971_VALIDATION.csv"

SRC_1671_DQZ_INPUTS = RESIDUALS / "P8_Y5_PARENT_QLOC_1671_DQZ_FACTOR_INPUT_ROWS.csv"
SRC_1672_ZLOCK = RESIDUALS / "P8_Y5_PARENT_QLOC_1672_Z_TO_RPHYS_LOCK_MAP_ATTEMPT.csv"
SRC_1674_DQZ_MATRIX = RESIDUALS / "P8_Y5_PARENT_QLOC_1674_DQZ_COMPONENT_DERIVATIVE_MATRIX.csv"
SRC_1667_DQ_LEAKS = RESIDUALS / "P8_Y5_PARENT_QLOC_1667_RETAINED_DQ_LEAK_ROWS.csv"
SRC_1541_DQVM = RESIDUALS / "P8_Y5_PARENT_QLOC_1541_DQVM_FINITE_COUPLING_ROW_NONCLAIM.csv"
SRC_2884_DQZ_FACTOR = SOURCE_WEIGHT / "RAB_FIRST_DQZ_FACTOR_SOURCE_ROW_2884_NONCLAIM.csv"
SRC_2885_BLOCKER = SOURCE_WEIGHT / "RAB_DQZ_ZERO_OR_FACTOR_BLOCKER_LEDGER_2885_NONCLAIM.csv"
SRC_2886_REQUIREMENTS = SOURCE_WEIGHT / "RAB_DQZ_COMPONENT_INPUT_REQUIREMENTS_2886_NONCLAIM.csv"
SRC_2911_QMAP = PARENT_ACTION / "Parent_qmap_kernel_attempt_2911_NONCLAIM.csv"
SRC_2913_AUX = PARENT_ACTION / "Parent_auxiliary_constraint_origin_2913_NONCLAIM.csv"
SRC_2914_COBS = PARENT_ACTION / "Cobs_no_shadow_head_audit_2914_NONCLAIM.csv"
SRC_2956_DESCENT = PARENT_ACTION / "matter_pullback_descent_audit_2956_NOT_DERIVED.csv"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_2972_SOURCE_REGISTER.csv",
    "factor": RESIDUALS / "P8_Y5_R2FR_2972_DQZ_FACTOR_AUDIT.csv",
    "matrix": RESIDUALS / "P8_Y5_R2FR_2972_COMPONENT_MATRIX_AUDIT.csv",
    "basis": RESIDUALS / "P8_Y5_R2FR_2972_Z_BASIS_NORMALIZATION_AUDIT.csv",
    "epsq": RESIDUALS / "P8_Y5_R2FR_2972_FIRST_EPSQ_SUBROWS_NONCLAIM.csv",
    "envelope": RESIDUALS / "P8_Y5_R2FR_2972_DQZ_NO_CANCELLATION_ENVELOPE.csv",
    "claims": RESIDUALS / "P8_Y5_R2FR_2972_CLAIM_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_2972_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_2972_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_2972_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_2972_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "matrix_copy": PARENT_ACTION / "DqZ_component_matrix_and_Z_basis_2972_NOT_DERIVED.csv",
    "epsq_copy": LOCAL_BOUNDS / "first_eps_q_subrows_2972_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR2972_Z_basis_physical_lock_next_NONCLAIM.csv",
}

for directory in {path.parent for path in OUTPUTS.values()} | {path.parent for path in BRANCH_OUTPUTS.values()} | {DOC.parent}:
    directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv_rows(path)
        return True
    except Exception:
        return False


def anchors_present(path: Path, anchors: str) -> tuple[bool, str]:
    if not path.exists():
        return False, anchors
    text = read_text(path)
    missing = [anchor for anchor in anchors.split(";") if anchor and anchor not in text]
    return not missing, ";".join(missing)


def add_common(row: dict[str, Any]) -> dict[str, Any]:
    row.update(
        {
            "checkpoint": CHECKPOINT,
            "branch_id": BRANCH_ID,
            "control_only": True,
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
            "generated_utc": RUN_UTC,
        }
    )
    return row


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def is_under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def md_table(rows: list[dict[str, Any]], columns: list[str] | None = None) -> str:
    if not rows:
        return "_No rows._"
    selected = columns or list(rows[0].keys())
    header = "| " + " | ".join(selected) + " |"
    separator = "| " + " | ".join("---" for _ in selected) + " |"
    body = ["| " + " | ".join(md_escape(row.get(column, "")) for column in selected) + " |" for row in rows]
    return "\n".join([header, separator, *body])


def source_register_rows() -> list[dict[str, Any]]:
    specs = [
        ("SRC2972_00_2971_doc", SRC_2971_DOC, "NEXT2971_0_2972;Next best move", "2971 handoff"),
        ("SRC2972_01_2971_next", SRC_2971_NEXT, "NEXT2971_0_2972", "machine-readable 2972 target"),
        ("SRC2972_02_2971_acq", SRC_2971_ACQ, "ACQ2971_0_eps_q_parent;ACQ2971_2_eps_factorization", "coefficient acquisition audit"),
        ("SRC2972_03_2971_split", SRC_2971_SPLIT, "SPL2971_00_eps_q_declaration;SPL2971_09_eps_component_matrix", "eps_q split rows"),
        ("SRC2972_04_2971_validation", SRC_2971_VALIDATION, "VAL2971_OVERALL", "2971 validation"),
        ("SRC2972_05_1671_dqz_inputs", SRC_1671_DQZ_INPUTS, "DQZ1671_0_basis;DQZ1671_2_derivative;DQZ1671_3_zero_candidate", "DqZ factor inputs"),
        ("SRC2972_06_1674_dqz_matrix", SRC_1674_DQZ_MATRIX, "DQM1674_0_coframe_metric;DQM1674_5_operator_norm", "DqZ component matrix"),
        ("SRC2972_07_1672_zlock", SRC_1672_ZLOCK, "LOCK1672_0_q_loc;LOCK1672_6_verdict", "Z-to-physical residual lock"),
        ("SRC2972_08_1667_dq_leaks", SRC_1667_DQ_LEAKS, "DQL1667_0_Dq_Z;DQL1667_7_Scg_envelope", "retained Dq leak rows"),
        ("SRC2972_09_1541_dqvm", SRC_1541_DQVM, "DQC1541_0_C_qm_definition;DQC1541_4_Scg_envelope", "finite coupling fallback"),
        ("SRC2972_10_2884_dqz_factor", SRC_2884_DQZ_FACTOR, "DQZ2884_0_first_factor_row", "first factor template"),
        ("SRC2972_11_2885_blocker", SRC_2885_BLOCKER, "DQZF2885_0_Dq_Z_norm;DQZF2885_1_N_Z", "DqZ blocker ledger"),
        ("SRC2972_12_2886_requirements", SRC_2886_REQUIREMENTS, "REQ2886_2_DqZ;REQ2886_3_NZ", "DqZ input requirements"),
        ("SRC2972_13_2911_qmap", SRC_2911_QMAP, "QMAP2911_6_operator_norm;QMAP2911_7_verdict", "qmap kernel attempt"),
        ("SRC2972_14_2913_aux", SRC_2913_AUX, "PAO2913_3_multiplier_units_rank;PAO2913_6_verdict", "auxiliary units/rank"),
        ("SRC2972_15_2914_cobs", SRC_2914_COBS, "COBS2914_1_projection_value;COBS2914_5_verdict", "observed coframe conditional norm"),
        ("SRC2972_16_2956_descent", SRC_2956_DESCENT, "DESC2956_1_parent_q;DESC2956_7_verdict", "matter descent dependency"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, source_path, anchors, role in specs:
        found, missing = anchors_present(source_path, anchors)
        rows.append(
            add_common(
                {
                    "source_id": source_id,
                    "source_type": "local_file",
                    "source_path": str(source_path),
                    "anchors": anchors,
                    "role": role,
                    "path_exists": source_path.exists(),
                    "anchors_found": found,
                    "missing_anchors": missing,
                }
            )
        )
    return rows


def factor_rows() -> list[dict[str, Any]]:
    rows = [
        ("FAC2972_0_Z_basis", "Z_basis", "MISSING_UNIFIED_Z_BASIS", "component map from formal doublet variables to local residual/channel basis", SRC_1671_DQZ_INPUTS),
        ("FAC2972_1_N_Z", "N_Z", "MISSING_Z_DIRECTION_NORMALIZATION", "Z field units, tangent vector convention and local branch norm", SRC_1671_DQZ_INPUTS),
        ("FAC2972_2_Dq_Z_norm", "Dq_Z_norm", "MISSING_DQ_DERIVATIVE_OR_THEOREM_ZERO", "parent q(Phi), derivative on Z direction, q norm and quotient sort", SRC_1671_DQZ_INPUTS),
        ("FAC2972_3_Dq_Z_zero", "Dq_Z_zero", "MISSING_PARENT_KERNEL_OR_CONSTRAINT_PROOF", "q independence theorem or constraint-elimination theorem", SRC_1671_DQZ_INPUTS),
        ("FAC2972_4_factor_template", "C_qm_Z", "SOURCE_READY_TEMPLATE_VALUE_MISSING", "Dq_Z_norm, N_Z and C_Obs_e must all be source-backed or theorem-zero", SRC_2884_DQZ_FACTOR),
        ("FAC2972_5_verdict", "DqZ factor package", "NOT_SOURCE_BACKED_SPLIT_REQUIRED", "no factor can be promoted from 1671/2884 in current corpus", SRC_2885_BLOCKER),
    ]
    return [
        add_common(
            {
                "factor_audit_id": factor_id,
                "symbol": symbol,
                "current_status": status,
                "missing_input": missing,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for factor_id, symbol, status, missing, path in rows
    ]


def matrix_rows() -> list[dict[str, Any]]:
    rows = [
        ("MAT2972_0_coframe_metric", "Dq_Z[e_obs,g_obs,mu_m,D_m]", "not_computed", "MISSING_OBSERVED_COFRAME_FUNCTOR", "eps_Dq_coframe_metric", SRC_1674_DQZ_MATRIX),
        ("MAT2972_1_source_current", "Dq_Z[source normalization/J_H]", "retained_leak", "SOURCE_CURRENT_ZERO_NOT_DERIVED", "eps_Dq_source_current", SRC_1674_DQZ_MATRIX),
        ("MAT2972_2_readouts", "Dq_Z[clock/photon/orbit/EM/PPN readouts]", "not_computed", "MISSING_READOUT_DESCENT", "eps_Dq_readout", SRC_1674_DQZ_MATRIX),
        ("MAT2972_3_boundary_projector", "Dq_Z[B_edge,P_loc,Q_X]", "retained_leak", "BOUNDARY_PROJECTOR_OPEN", "eps_Dq_boundary_projector", SRC_1674_DQZ_MATRIX),
        ("MAT2972_4_residual_lock", "Dq_Z[R_phys -> observed residuals]", "not_computed", "COMPONENT_MAP_NOT_CLOSED", "eps_Dq_residual_lock", SRC_1674_DQZ_MATRIX),
        ("MAT2972_5_operator_norm", "Dq_Z_norm", "not_filled", "MISSING_Q_Z_NORMS_AND_DQ_MATRIX", "Dq_Z_norm", SRC_1674_DQZ_MATRIX),
        ("MAT2972_6_verdict", "DqZ component derivative matrix", "NOT_COMPUTED_NONCLAIM_SUBROWS_REQUIRED", "no component row has a finite value or theorem-zero", "eps_Dq_matrix_total", SRC_1674_DQZ_MATRIX),
    ]
    return [
        add_common(
            {
                "matrix_audit_id": matrix_id,
                "component": component,
                "computation_status": status,
                "blocking_issue": blocker,
                "fallback_subrow": fallback,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "computed_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "prediction_source_backed": False,
                "accepted_for_scoring": False,
            }
        )
        for matrix_id, component, status, blocker, fallback, path in rows
    ]


def basis_rows() -> list[dict[str, Any]]:
    rows = [
        ("BAS2972_0_q_loc", "q_loc vector", "not_closed", "MISSING_GAMMA_EFF_KHAT_PLOC_OWNER_AND_COMPONENT_DATA", "Z_q^nu", SRC_1672_ZLOCK),
        ("BAS2972_1_Y5", "Y5 measured-GM/source normalization", "fails_current_route_exchange_even_scalar", "MISSING_SOURCE_CURRENT_CLOSURE_AND_GAUSS_ORBITAL_CALIBRATION", "Z_mu", SRC_1672_ZLOCK),
        ("BAS2972_2_Y6", "Y6 extra stress/local exterior metric", "not_closed", "EXCHANGE_EVEN_CONSERVED_STRESS_CAN_LIVE_IN_QLOC_KERNEL", "Z_T", SRC_1672_ZLOCK),
        ("BAS2972_3_PPN", "full PPN residual vector", "not_closed", "MISSING_PPN_RESPONSE_OPERATOR_AND_GAUGE_FRAME_CERTIFICATE", "Z_PPN", SRC_1672_ZLOCK),
        ("BAS2972_4_boundary", "boundary/harmonic flux", "not_closed", "MISSING_HODGE_FLUX_BOUNDARY_OPERATOR_AND_PROJECTOR_DESCENT", "Z_H", SRC_1672_ZLOCK),
        ("BAS2972_5_coupling", "matter/source/readout coupling", "partial_only_not_closed", "MISSING_QUOTIENT_MATTER_SOURCE_READOUT_DESCENT", "Z_coupling", SRC_1672_ZLOCK),
        ("BAS2972_6_full_rank", "full physical residual vector", "PHYSICAL_LOCK_NOT_PROVED", "all channel rows remain unsigned or incomplete", "Z^A=N^A_I R_phys^I", SRC_1672_ZLOCK),
        ("BAS2972_7_N_Z", "selected tangent normalization", "MISSING_Z_DIRECTION_NORMALIZATION", "no unified Z basis, tangent convention or units", "N_Z", SRC_2885_BLOCKER),
    ]
    return [
        add_common(
            {
                "basis_audit_id": basis_id,
                "physical_channel": channel,
                "current_status": status,
                "blocking_gap": blocker,
                "candidate_basis_component": component,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "parent_signed": False,
                "full_rank_component": False,
                "coercive_norm_component": False,
                "theorem_zero_adopted": False,
                "finite_value_present": False,
                "accepted_for_scoring": False,
            }
        )
        for basis_id, channel, status, blocker, component, path in rows
    ]


def epsq_rows() -> list[dict[str, Any]]:
    raw_rows = [
        ("eps_q_parent", "eps_q_declaration", "formal q(Phi)=Q_vis declaration without parent-owned chart", "dimensionless", "QMAP2911_0_projection_form", SRC_2911_QMAP),
        ("eps_q_parent", "eps_q_order", "q/readout not proved before variation and fitting", "dimensionless", "DESC2956_1_parent_q", SRC_2956_DESCENT),
        ("eps_q_parent", "eps_q_norm", "q norm missing", "dimensionless", "DQZF2885_0_Dq_Z_norm", SRC_2885_BLOCKER),
        ("eps_factorization", "eps_Z_basis", "unified Z basis missing", "dimensionless", "DQZ1671_0_basis", SRC_1671_DQZ_INPUTS),
        ("eps_factorization", "eps_N_Z", "selected Z tangent normalization missing", "dimensionless", "DQZ1671_1_norm", SRC_1671_DQZ_INPUTS),
        ("eps_factorization", "eps_Dq_derivative", "Dq derivative on Z direction missing", "dimensionless", "DQZ1671_2_derivative", SRC_1671_DQZ_INPUTS),
        ("eps_factorization", "eps_Dq_coframe_metric", "coframe/metric/measure/connection derivative row missing", "dimensionless", "DQM1674_0_coframe_metric", SRC_1674_DQZ_MATRIX),
        ("eps_factorization", "eps_Dq_source_current", "source-current derivative retained as live leak", "source_norm", "DQM1674_1_source_current", SRC_1674_DQZ_MATRIX),
        ("eps_factorization", "eps_Dq_readout", "clock/photon/orbit/EM/PPN readout derivative missing", "readout_norm", "DQM1674_2_readouts", SRC_1674_DQZ_MATRIX),
        ("eps_factorization", "eps_Dq_boundary_projector", "boundary/projector derivative retained as live leak", "boundary_norm", "DQM1674_3_boundary_projector", SRC_1674_DQZ_MATRIX),
        ("eps_factorization", "eps_Dq_residual_lock", "physical residual lock matrix missing", "residual_norm", "DQM1674_4_residual_lock", SRC_1674_DQZ_MATRIX),
        ("eps_factorization", "eps_Dq_operator_norm", "operator norm of component matrix missing", "dimensionless", "DQM1674_5_operator_norm", SRC_1674_DQZ_MATRIX),
        ("eps_constraint", "eps_aux_units_rank", "auxiliary units/rank/null projector missing", "dimensionless", "PAO2913_3_multiplier_units_rank", SRC_2913_AUX),
        ("eps_constraint", "eps_constraint_zero", "q independence or constraint-elimination theorem missing", "dimensionless", "DQZ1671_3_zero_candidate", SRC_1671_DQZ_INPUTS),
    ]
    rows: list[dict[str, Any]] = []
    for parent, symbol, definition, units, source_anchor, path in raw_rows:
        rows.append(
            add_common(
                {
                    "epsq_id": f"EPSQ2972_{len(rows):02d}_{symbol}",
                    "parent_coefficient": parent,
                    "subrow_symbol": symbol,
                    "definition": definition,
                    "units": units,
                    "candidate_value": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                    "lower_bound": 0,
                    "upper_bound": "MISSING_SOURCE_BACKED_UPPER_BOUND",
                    "source_anchor": source_anchor,
                    "source_path": str(path),
                    "source_path_exists": path.exists(),
                    "finite_value_present": False,
                    "prediction_source_backed": False,
                    "accepted_for_scoring": False,
                    "no_cancellation_policy": True,
                }
            )
        )
    return rows


def envelope_rows() -> list[dict[str, Any]]:
    rows = [
        ("ENV2972_0_DqZ_norm", "Dq_Z_norm", "Dq_Z_norm <= eps_Dq_operator_norm + eps_Dq_coframe_metric + eps_Dq_source_current + eps_Dq_readout + eps_Dq_boundary_projector + eps_Dq_residual_lock", "all Dq component rows finite/theorem-zero", SRC_1674_DQZ_MATRIX),
        ("ENV2972_1_factor_product", "C_qm_Z", "C_qm_Z <= C_Obs_e * Dq_Z_norm * N_Z + E_direct_Z", "C_Obs_e, Dq_Z_norm, N_Z and direct tails finite/theorem-zero", SRC_2884_DQZ_FACTOR),
        ("ENV2972_2_coupling_fallback", "S_cg_norm", "S_cg_norm <= 1/2||T||_source*C_qm + S_direct_m + S_source_norm_extra + S_boundary_m", "T norm, C_qm and direct/source/boundary terms finite", SRC_1541_DQVM),
        ("ENV2972_3_no_cancellation", "eps_q_total_abs", "absolute sum over all eps_q subrows; no cancellation or fitted-GM absorption", "every head source-backed or theorem-zero", SRC_1667_DQ_LEAKS),
    ]
    return [
        add_common(
            {
                "envelope_id": envelope_id,
                "quantity": quantity,
                "formula": formula,
                "promotion_requirement": requirement,
                "source_path": str(path),
                "source_path_exists": path.exists(),
                "numeric_bound_present": False,
                "accepted_for_scoring": False,
                "no_cancellation_policy": True,
            }
        )
        for envelope_id, quantity, formula, requirement, path in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("CG2972_0_Z_basis", "unified Z basis sourced", False, "Z_BASIS_MISSING"),
        ("CG2972_1_NZ", "N_Z normalization sourced", False, "N_Z_MISSING"),
        ("CG2972_2_matrix", "Dq component matrix computed", False, "DQ_MATRIX_NOT_COMPUTED"),
        ("CG2972_3_DqZ_norm", "Dq_Z_norm finite or theorem-zero", False, "DQZ_NORM_MISSING"),
        ("CG2972_4_epsq", "first eps_q subrows source-backed", False, "EPSQ_SUBROWS_MISSING_VALUES"),
        ("CG2972_5_local_GR", "derived local GR/Newton reduction claimed", False, "NO_LOCAL_GR_OR_NEWTON_CLAIM"),
    ]
    return [
        add_common(
            {
                "claim_gate_id": gate_id,
                "claim": claim,
                "condition_passed": passed,
                "status": status,
            }
        )
        for gate_id, claim, passed, status in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        ("DEC2972_0_matrix", "DqZ matrix not sourced", "1674 is a component audit with every computed value missing", "do not promote Dq_Z_norm"),
        ("DEC2972_1_basis", "Z basis and N_Z not sourced", "1671 has factor labels but no unified basis, tangent convention or norm", "target physical-lock/basis construction next"),
        ("DEC2972_2_epsq", "first eps_q subrows emitted", "the missing matrix and basis are now exact subrow targets", "fill eps_Z_basis, eps_N_Z and Dq component rows before scoring"),
        ("DEC2972_3_claims", "no local-GR, R10, PPN, clock, WEP or orbital claim", "all rows remain nonclaim and missing upper bounds", "private checkpoint only"),
    ]
    return [
        add_common(
            {
                "decision_id": decision_id,
                "decision": decision,
                "because": because,
                "next_action": action,
            }
        )
        for decision_id, decision, because, action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        add_common(
            {
                "next_id": "NEXT2972_0_2973",
                "priority": "selected_primary",
                "next_doc": "2973-Y5-R2FR-Z-basis-physical-lock-map-and-NZ-normalization-or-q_loc-first-component-under-AX1090.md",
                "next_script": "scripts/Y5_R2FR_Z_basis_physical_lock_map_and_NZ_normalization_or_q_loc_first_component_under_AX1090_2973.py",
                "objective": "Try to construct the selected Z basis and N_Z normalization from the physical-lock channels q_loc/Y5/Y6/PPN/boundary/coupling; if not, select the q_loc channel as the first component row to source.",
                "include": "Z_basis;N_Z;q_loc;Y5;Y6;PPN;boundary;coupling;full-rank/coercive norm test;physical-lock matrix;first q_loc component row",
                "exclude": "full Dq matrix scoring;boundary no-flux proof;CDB closure;M_AB signature proof;R10 alpha claim;PPN claim;clock/orbital claim;local-GR claim;GitHub action;formalization-workbench edits",
            }
        )
    ]


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = [
        ("matrix_copy", OUTPUTS["matrix"], BRANCH_OUTPUTS["matrix_copy"]),
        ("epsq_copy", OUTPUTS["epsq"], BRANCH_OUTPUTS["epsq_copy"]),
        ("next_copy", OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"]),
    ]
    rows: list[dict[str, Any]] = []
    for copy_id, source, target in copies:
        shutil.copyfile(source, target)
        rows.append(
            add_common(
                {
                    "copy_id": copy_id,
                    "source_path": str(source),
                    "copy_path": str(target),
                    "source_exists": source.exists(),
                    "copy_exists": target.exists(),
                }
            )
        )
    return rows


def validation_rows(all_rows: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = all_rows["sources"]
    generated_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    csv_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values())
    required_eps = {"eps_Z_basis", "eps_N_Z", "eps_Dq_coframe_metric", "eps_Dq_source_current", "eps_Dq_readout", "eps_Dq_boundary_projector", "eps_Dq_residual_lock", "eps_Dq_operator_norm"}
    eps_symbols = {row["subrow_symbol"] for row in all_rows["epsq"]}
    checks = [
        ("VAL2972_0_sources_exist", all(row["path_exists"] for row in source_rows), "all cited local source paths exist", True),
        ("VAL2972_1_anchors_found", all(row["anchors_found"] for row in source_rows), "all cited source anchors found", True),
        ("VAL2972_2_factor_not_promoted", all(row["finite_value_present"] is False and row["theorem_zero_adopted"] is False for row in all_rows["factor"]), "DqZ factor rows not promoted", True),
        ("VAL2972_3_matrix_not_computed", any(row["matrix_audit_id"] == "MAT2972_6_verdict" and row["computation_status"] == "NOT_COMPUTED_NONCLAIM_SUBROWS_REQUIRED" for row in all_rows["matrix"]), "DqZ matrix remains not computed", True),
        ("VAL2972_4_basis_not_sourced", any(row["basis_audit_id"] == "BAS2972_6_full_rank" and row["current_status"] == "PHYSICAL_LOCK_NOT_PROVED" for row in all_rows["basis"]), "physical-lock basis not proved", True),
        ("VAL2972_5_epsq_required_present", required_eps.issubset(eps_symbols), "required eps_q subrows are present", True),
        ("VAL2972_6_epsq_nonclaim", all(row["finite_value_present"] is False and row["accepted_for_scoring"] is False and row["valid_for_claim"] is False for row in all_rows["epsq"]), "eps_q subrows remain nonclaim", True),
        ("VAL2972_7_claims_blocked", all(row["condition_passed"] is False and row["claim_allowed"] is False for row in all_rows["claims"]), "all claim gates remain blocked", True),
        ("VAL2972_8_next_target_written", any(row["next_id"] == "NEXT2972_0_2973" for row in all_rows["next"]), "2973 Z-basis/physical-lock next target selected", True),
        ("VAL2972_9_branches_exist", all(Path(row["copy_path"]).exists() for row in all_rows["branches"]), "branch copy files exist", True),
        ("VAL2972_10_csvs_parse", all(csv_parses(path) for path in csv_paths), "all generated CSV files parse", True),
        ("VAL2972_11_outputs_under_post_checkpoint", all(is_under(path, ROOT) for path in generated_paths), "all generated outputs are under post-checkpoint-work", True),
        ("VAL2972_12_formalization_clean", not any(is_under(path, FORMALIZATION) for path in generated_paths), "no 2972 outputs were written to formalization-workbench", True),
        ("VAL2972_13_doc_written", DOC.exists(), "2972 markdown checkpoint exists", True),
    ]
    overall = all(passed == required for _, passed, _, required in checks)
    rows = [
        add_common(
            {
                "validation_id": validation_id,
                "passed": passed,
                "check": check,
                "required": required,
            }
        )
        for validation_id, passed, check, required in checks
    ]
    rows.append(add_common({"validation_id": "VAL2972_OVERALL", "passed": overall, "check": "2972 validation overall", "required": True}))
    return rows


def write_markdown(all_rows: dict[str, list[dict[str, Any]]]) -> None:
    doc = f"""# 2972 - Y5 R2FR: DqZ component matrix and Z-basis normalization or first epsq subrow under AX1090

Status: `Y5_R2FR_2972_DqZ_matrix_not_computed_Z_basis_NZ_missing_first_epsq_subrows_written_nonclaim`

Claim ceiling: `no_DqZ_norm_no_Z_basis_no_NZ_score_no_local_GR_no_Newton_no_R10_no_PPN_no_clock_no_orbital_no_WEP_no_public_claim`

2972 tested whether the 1671/1674 source rows already contain a source-backed `Dq_Z` component matrix and selected `Z_basis/N_Z` normalization.

- Result: they do not. The rows are useful requirement maps, but every actual value is missing or conditional.
- `Dq_Z_norm` cannot be promoted because the component matrix, q/Z norms, `Z_basis`, `N_Z`, and physical residual lock are all unsigned.
- First `eps_q` subrows are now explicit: coframe, source-current, readout, boundary/projector, residual-lock, basis, norm and operator-norm heads.
- Next best move is the physical-lock side: construct `Z_basis` and `N_Z` from q_loc/Y5/Y6/PPN/boundary/coupling channels, or select q_loc as the first sourced component.

## Source Register

{md_table(all_rows["sources"], ["source_id", "source_path", "path_exists", "anchors_found", "role"])}

## DqZ Factor Audit

{md_table(all_rows["factor"], ["factor_audit_id", "symbol", "current_status", "missing_input", "finite_value_present", "accepted_for_scoring"])}

## Component Matrix Audit

{md_table(all_rows["matrix"], ["matrix_audit_id", "component", "computation_status", "blocking_issue", "fallback_subrow", "accepted_for_scoring"])}

## Z-Basis Normalization Audit

{md_table(all_rows["basis"], ["basis_audit_id", "physical_channel", "current_status", "blocking_gap", "candidate_basis_component", "full_rank_component"])}

## First eps-q Subrows

{md_table(all_rows["epsq"], ["epsq_id", "parent_coefficient", "subrow_symbol", "definition", "candidate_value", "accepted_for_scoring"])}

## DqZ No-Cancellation Envelope

{md_table(all_rows["envelope"], ["envelope_id", "quantity", "formula", "promotion_requirement", "numeric_bound_present"])}

## Claim Gates

{md_table(all_rows["claims"], ["claim_gate_id", "claim", "condition_passed", "status", "claim_allowed"])}

## Decision Ledger

{md_table(all_rows["decision"], ["decision_id", "decision", "because", "next_action"])}

## Next Target

{md_table(all_rows["next"], ["next_id", "priority", "next_doc", "next_script", "objective", "exclude"])}

## Branch Copies

{md_table(all_rows["branches"], ["copy_id", "source_path", "copy_path", "source_exists", "copy_exists", "valid_for_claim"])}

## Validation

{md_table(all_rows["validation"], ["validation_id", "passed", "check", "required"])}

Validation overall: `{all_rows["validation"][-1]["passed"]}`.
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    all_rows: dict[str, list[dict[str, Any]]] = {
        "sources": source_register_rows(),
        "factor": factor_rows(),
        "matrix": matrix_rows(),
        "basis": basis_rows(),
        "epsq": epsq_rows(),
        "envelope": envelope_rows(),
        "claims": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_target_rows(),
    }

    for key, path in OUTPUTS.items():
        if key in {"branches", "validation"}:
            continue
        write_csv(path, all_rows[key])

    all_rows["branches"] = copy_branch_outputs()
    write_csv(OUTPUTS["branches"], all_rows["branches"])

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    all_rows["validation"] = validation_rows(all_rows)
    write_csv(OUTPUTS["validation"], all_rows["validation"])
    write_markdown(all_rows)

    print(f"2972 validation overall: {all_rows['validation'][-1]['passed']}")
    print(DOC)


if __name__ == "__main__":
    main()
