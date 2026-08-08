from __future__ import annotations

import csv
import shutil
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FORMALIZATION = ROOT.parent / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
RAB = ROOT / "source-intake" / "rab-sector"
RAB_RAW = RAB / "raw"
RAB_ACCEPTED = RAB / "accepted"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1591"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1591-Y5-R2FR-fixed-L0-cdb-memory-Qnorm-first-fill-or-cR2-bound-row.md"

SOURCE_FILES = {
    "1590_doc": ROOT / "1590-Y5-R2FR-Gamma-Khat-Ploc-owner-bundle-or-cR2-finite-coefficient-row.md",
    "1590_validation": OUT / "P8_Y5_BRR545_1590_VALIDATION.csv",
    "1590_fixed_l0_gate": OUT / "P8_Y5_PARENT_QLOC_1590_FIXED_L0_DOUBLE_ZERO_CONTRACT_GATE.csv",
    "1590_cr2_implications": OUT / "P8_Y5_PARENT_QLOC_1590_CR2_COEFFICIENT_IMPLICATIONS.csv",
    "1590_finite_template": OUT / "P8_Y5_PARENT_QLOC_1590_FINITE_COEFFICIENT_ROW_TEMPLATE.csv",
    "1590_qgamma_bridge": OUT / "P8_Y5_PARENT_QLOC_1590_QGAMMA_QNORM_RUNNER_BRIDGE.csv",
    "1373_cdb_attempt": OUT / "P8_Y5_R10_1373_CDB_NO_FLUX_THEOREM_ATTEMPT.csv",
    "1373_qnorm_contracts": OUT / "P8_Y5_R10_1373_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv",
    "1374_kcdb_contracts": OUT / "P8_Y5_R10_1374_KCDB_SUBCHANNEL_BOUND_CONTRACTS.csv",
    "1374_qalg_qtrans": OUT / "P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv",
    "1375_kconn_contract": OUT / "P8_Y5_R10_1375_KCONN_FIRST_BOUND_CONTRACT.csv",
    "1375_transition_validator": OUT / "P8_Y5_R10_1375_TRANSITION_INPUT_VALIDATOR_RESULTS.csv",
    "1376_kconn_fill_attempt": OUT / "P8_Y5_R10_1376_KCONN_OPERATOR_NORM_FILL_ATTEMPT.csv",
    "1376_transition_acquisition": OUT / "P8_Y5_R10_1376_TRANSITION_PARENT_SOURCE_ACQUISITION.csv",
    "1377_transition_candidate": OUT / "P8_Y5_R10_1377_TRANSITION_PARENT_CANDIDATE_ROW_ATTEMPT.csv",
    "1377_kconn_source_hunt": OUT / "P8_Y5_R10_1377_KCONN_OPERATOR_SOURCE_HUNT.csv",
    "1378_transition_law": OUT / "P8_Y5_R10_1378_TRANSITION_PARENT_LAW_DERIVATION.csv",
    "1378_closure_pack": OUT / "P8_Y5_R10_1378_EXPLICIT_CLOSURE_INPUT_PACK.csv",
    "1379_gradient_audit": OUT / "P8_Y5_R10_1379_GRADIENT_PARENT_SIGNATURE_AUDIT.csv",
    "1379_closure_schema": OUT / "P8_Y5_R10_1379_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv",
    "1428_branch_classifier": OUT / "P8_Y5_R10_1428_BRANCH_CLASSIFIER_ROW.csv",
}

NEEDLES = {
    "1590_doc": ["NEXT_1591_FIXED_L0_CDB_MEMORY_QNORM_FIRST_FILL_OR_CR2_BOUND_ROW", "attempt to close K_conn/K_domain/K_boundary"],
    "1590_validation": ["VAL1590_OVERALL", "PASS"],
    "1590_fixed_l0_gate": ["FLG1590_5_verdict", "ZERO_THEOREM_NOT_DERIVED"],
    "1590_cr2_implications": ["CR2I1590_4_finite_row_trigger", "FINITE_ROW_REQUIRED_IF_RESIDUALS_RETAINED"],
    "1590_finite_template": ["FCR1590_4_Qnorm_components", "REJECT_CURRENT_ROW"],
    "1590_qgamma_bridge": ["QGB1590_1_Qnorm_decomposition", "Q_alg+Q_cdb+Q_mem+Q_bdy+Q_trans+Q_proj"],
    "1373_cdb_attempt": ["CDB1373_4_verdict", "CDB_ZERO_THEOREM_NOT_DERIVED"],
    "1373_qnorm_contracts": ["QFF1373_0_Q_alg", "QFF1373_5_Q_proj"],
    "1374_kcdb_contracts": ["KCS1374_6_Q_cdb_update", "SUBCHANNEL_DECOMPOSITION_READY_NUMERIC_VALUES_MISSING"],
    "1374_qalg_qtrans": ["QQF1374_0_Q_alg_transition_reduction", "QQF1374_4_Qalg_Qtrans_verdict"],
    "1375_kconn_contract": ["KCB1375_5_verdict", "BOUND_CONTRACT_READY_NUMERIC_VALUES_MISSING"],
    "1375_transition_validator": ["VALIDATOR1375_VERDICT", "NO_SOURCE_READY_TRANSITION_ROW_FOUND"],
    "1376_kconn_fill_attempt": ["KOF1376_7_verdict", "NO_SOURCE_BACKED_KCONN_OPERATOR_NORM_ROW"],
    "1376_transition_acquisition": ["TPS1376_16_shell_projector_or_bound", "MISSING_SHELL_CLOSURE"],
    "1377_transition_candidate": ["CAND1377_VERDICT", "NO_SOURCE_BACKED_TRANSITION_PARENT_ROW_FOUND"],
    "1377_kconn_source_hunt": ["KOH1377_VERDICT", "NO_EXACT_SOURCE_BACKED_OPERATOR_CONVENTION_ROW_FOUND"],
    "1378_transition_law": ["DER1378_8_verdict", "NO_PARENT_SIGNED_TRANSITION_LAW_YET"],
    "1378_closure_pack": ["CIP1378_12_verdict", "EXPLICIT_CLOSURE_INPUT_PACK_READY_NONCLAIM"],
    "1379_gradient_audit": ["GPA1379_8_verdict", "NO_PARENT_SIGNED_GRADIENT_COMPLETION_ROW"],
    "1379_closure_schema": ["CRS1379_13_verdict", "CLOSURE_RUNNER_SCHEMA_READY_NONCLAIM"],
    "1428_branch_classifier": ["BRANCH_LOCK_CREATED_INPUTS_PENDING", "valid_for_claim"],
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1591_SOURCE_REGISTER.csv"
CDB_MEMORY_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1591_CDB_MEMORY_THEOREM_ATTEMPT.csv"
QNORM_FIRST_FILL = OUT / "P8_Y5_PARENT_QLOC_1591_QNORM_FIRST_FILL_SYNTHESIS.csv"
TRANSITION_CLOSURE_PACK = OUT / "P8_Y5_PARENT_QLOC_1591_TRANSITION_CLOSURE_PACK.csv"
CR2_BOUND_INTERFACE = OUT / "P8_Y5_PARENT_QLOC_1591_CR2_BOUND_ROW_INTERFACE.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1591_RUNNER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1591_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1591_DECISION.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1591_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1591_VALIDATION.csv"

COPY_TARGETS = {
    CDB_MEMORY_AUDIT: [
        QUARANTINE / "CDB_MEMORY_THEOREM_ATTEMPT_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_cdb_memory_theorem_attempt_nonclaim_1591.csv",
    ],
    QNORM_FIRST_FILL: [
        QUARANTINE / "QNORM_FIRST_FILL_SYNTHESIS_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_qnorm_first_fill_synthesis_nonclaim_1591.csv",
    ],
    TRANSITION_CLOSURE_PACK: [
        QUARANTINE / "TRANSITION_CLOSURE_PACK_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_transition_closure_pack_nonclaim_1591.csv",
    ],
    CR2_BOUND_INTERFACE: [
        QUARANTINE / "CR2_BOUND_ROW_INTERFACE_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_cR2_bound_row_interface_nonclaim_1591.csv",
    ],
    RUNNER: [
        QUARANTINE / "RUNNER_REFUSAL_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_runner_refusal_nonclaim_1591.csv",
    ],
    DECISION: [
        QUARANTINE / "DECISION_NONCLAIM.csv",
        BRANCH_RESIDUALS / "R2FR_fixed_L0_cdb_memory_qnorm_decision_nonclaim_1591.csv",
    ],
}


def false_flags() -> dict[str, bool]:
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


def source_register_rows() -> list[dict[str, Any]]:
    rows = []
    for source_index, (source_key, source_path) in enumerate(SOURCE_FILES.items()):
        rows.append(
            {
                "same_parent_branch_id": BRANCH_ID,
                "source_id": f"SRC1591_{source_index}_{source_key}",
                "source_path": rel(source_path),
                "exists": source_path.exists(),
                "needle_found": file_contains(source_path, NEEDLES[source_key]),
                "needles": "; ".join(NEEDLES[source_key]),
                "purpose": "fixed-L0 CDB/memory residual closure attempt and Q_norm/cR2 first-fill interface",
                **false_flags(),
            }
        )
    return rows


def cdb_memory_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CMA1591_0_fixed_L0_scope",
            "fixed-L0 double-zero algebraic branch",
            "Use fixed L0 and Fhat(m*)=Fhat_prime(m*)=0 to silence every local residual.",
            "Fixed L0 closes the algebraic volume/m/L chain only; it does not silence connection, domain, boundary, memory stress, shell or projector channels.",
            "ALGEBRAIC_CLOSURE_ONLY_NOT_FULL_ZERO",
            "source-backed parent adoption plus separate CDB/memory no-flux theorem",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1590_FIXED_L0_DOUBLE_ZERO_CONTRACT_GATE.csv",
        ),
        (
            "CMA1591_1_K_conn",
            "K_conn",
            "Promote connection/derivative response to zero from local vacuum and double-zero.",
            "K_conn has a sharpened operator-norm bound, but N_conn,nabla, N_conn,star, N_conn,ibp, edge terms, gauge/frame, domain norm and A_ref/N_div are missing.",
            "BOUND_CONTRACT_READY_OPERATOR_NORMS_MISSING",
            "source-backed operator norm row or exact connection no-flux identity",
            "source-intake/mts_residuals/P8_Y5_R10_1375_KCONN_FIRST_BOUND_CONTRACT.csv;source-intake/mts_residuals/P8_Y5_R10_1376_KCONN_OPERATOR_NORM_FILL_ATTEMPT.csv",
        ),
        (
            "CMA1591_2_K_domain",
            "K_domain",
            "Set domain/projector response to zero by compact local/domain selector arguments.",
            "The current corpus keeps the domain selector theorem failed or conditional; domain/source-normalization and projector variation remain live.",
            "DOMAIN_ZERO_THEOREM_FAILED_CURRENT_CORPUS",
            "domain selector law, projector variation and source-normalization row",
            "source-intake/mts_residuals/P8_Y5_R10_1373_CDB_NO_FLUX_THEOREM_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1374_KCDB_SUBCHANNEL_BOUND_CONTRACTS.csv",
        ),
        (
            "CMA1591_3_K_boundary",
            "K_boundary",
            "Use natural boundary, topology, gauge or compact support to delete boundary primitive/corner terms.",
            "No general no-flux theorem exists; boundary primitive, reference subtraction, corner/edge and shell terms remain explicit.",
            "BOUNDARY_ZERO_THEOREM_FAILED_GENERAL",
            "boundary primitive/source path or exact no-flux theorem with stated domain",
            "source-intake/mts_residuals/P8_Y5_R10_1373_CDB_NO_FLUX_THEOREM_ATTEMPT.csv;source-intake/mts_residuals/P8_Y5_R10_1374_KCDB_SUBCHANNEL_BOUND_CONTRACTS.csv",
        ),
        (
            "CMA1591_4_K_comm_trace_index",
            "K_comm, spatial trace and index/frame gates",
            "Treat projector/readout commutators and spatial trace conversion as harmless conventions.",
            "The 00/ii trace-reversal, P_loc commutator, readout frame and index placement locks are required before Q_cdb can be scoreable.",
            "COMM_TRACE_INDEX_GATES_VALUES_MISSING",
            "local orthonormal frame, trace convention and commutator norm",
            "source-intake/mts_residuals/P8_Y5_R10_1374_KCDB_SUBCHANNEL_BOUND_CONTRACTS.csv",
        ),
        (
            "CMA1591_5_memory_source_stress",
            "Q_mem and active memory/source/bath stress",
            "Delete memory stress after using the branch to create a transition profile.",
            "The kinetic/source/bath/boundary memory terms remain active unless a no-hair/source-silence theorem or finite stress row is supplied.",
            "MEMORY_STRESS_RETAINED",
            "N_kin, K_mem_kin, N_pot, K_mem_drift, J_mem, B_mem or no-hair theorem",
            "source-intake/mts_residuals/P8_Y5_R10_1373_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv;source-intake/mts_residuals/P8_Y5_R10_1379_GRADIENT_PARENT_SIGNATURE_AUDIT.csv",
        ),
        (
            "CMA1591_6_transition_shell",
            "Q_trans and transition shell",
            "Use the conditional gradient relaxation profile as a parent-derived local plateau.",
            "Gradient relaxation is the best route but is not parent-signed; kappa_m, F2, L0, ell_tr, U_B, support powers, shell and provenance are not claim-grade.",
            "TRANSITION_PARENT_LAW_NOT_SIGNED",
            "parent-signed gradient completion or source-backed closure pack values",
            "source-intake/mts_residuals/P8_Y5_R10_1378_TRANSITION_PARENT_LAW_DERIVATION.csv;source-intake/mts_residuals/P8_Y5_R10_1379_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv",
        ),
        (
            "CMA1591_7_projector_leakage",
            "Q_proj",
            "Assume P_loc projection kills residual leakage.",
            "The projector/readout residual still needs an exact projector-zero theorem or finite commutator/leakage bound.",
            "PROJECTOR_LEAKAGE_BOUND_MISSING",
            "P_loc definition, readout frame and commutator norm",
            "source-intake/mts_residuals/P8_Y5_R10_1373_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv;source-intake/mts_residuals/P8_Y5_R10_1374_KCDB_SUBCHANNEL_BOUND_CONTRACTS.csv",
        ),
        (
            "CMA1591_8_verdict",
            "CDB/memory zero theorem under fixed L0",
            "Close K_conn, K_domain, K_boundary, memory/source stress, transition shell and projector leakage.",
            "The route is narrowed and cleaner, but the exact zero theorem is not derived. Move to componentwise Q_norm/cR2 finite interface while continuing the gradient-signature hunt.",
            "CDB_MEMORY_ZERO_THEOREM_NOT_DERIVED",
            "either parent-sign the gradient/transition mechanism or acquire finite component bounds",
            "aggregate_CMA1591_0_to_CMA1591_7",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "channel": channel,
            "attempted_zero": attempted_zero,
            "evidence_summary": evidence_summary,
            "status": status,
            "blocking_gap": blocking_gap,
            "source_paths": source_paths,
            **false_flags(),
        }
        for audit_id, channel, attempted_zero, evidence_summary, status, blocking_gap, source_paths in rows
    ]


def qnorm_first_fill_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "QNF1591_0_Q_alg",
            "Q_alg",
            "Q_alg <= A_ref^-1 |F2| A_S^2 U_B^(2pS)/(L0^2 L_tr), or conditional gradient form A_ref^-1 |F2| A_S^2 U_B^2/(L0^2 ell_tr)",
            "dimensionless_after_A_ref_normalization",
            "SYMBOLIC_FIRST_FILL_READY_VALUES_MISSING",
            "F2;A_S;U_B;pS;L0;L_tr_or_ell_tr;A_ref;source_path;units",
            "PPN_gamma;R10;clocks;orbital",
            "source-intake/mts_residuals/P8_Y5_R10_1374_QALG_QTRANS_FIRST_FILL.csv;source-intake/mts_residuals/P8_Y5_R10_1379_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv",
        ),
        (
            "QNF1591_1_Q_cdb",
            "Q_cdb",
            "Q_cdb <= A_ref^-1 N_div(K_conn_norm + K_domain_norm + K_boundary_norm + K_comm_norm), with spatial trace/index gates",
            "dimensionless_after_A_ref_normalization",
            "SUBCHANNEL_DECOMPOSITION_READY_NUMERIC_VALUES_MISSING",
            "K_conn;K_domain;K_boundary;K_comm;N_div;A_ref;trace/index convention;source_path",
            "PPN_gamma;R10;clocks;orbital",
            "source-intake/mts_residuals/P8_Y5_R10_1374_KCDB_SUBCHANNEL_BOUND_CONTRACTS.csv;source-intake/mts_residuals/P8_Y5_R10_1376_KCONN_OPERATOR_NORM_FILL_ATTEMPT.csv",
        ),
        (
            "QNF1591_2_Q_mem",
            "Q_mem",
            "Q_mem <= A_ref^-1(N_kin K_mem_kin + N_pot K_mem_drift + N_src J_mem + N_bath B_mem)",
            "dimensionless_after_A_ref_normalization",
            "MEMORY_STRESS_CONTRACT_READY_VALUES_MISSING",
            "N_kin;K_mem_kin;N_pot;K_mem_drift;N_src;J_mem;N_bath;B_mem;source/no-hair theorem",
            "PPN_gamma;R10;clocks;orbital;cosmology_interface",
            "source-intake/mts_residuals/P8_Y5_R10_1373_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv;source-intake/mts_residuals/P8_Y5_R10_1379_GRADIENT_PARENT_SIGNATURE_AUDIT.csv",
        ),
        (
            "QNF1591_3_Q_bdy",
            "Q_bdy",
            "Q_bdy <= A_ref^-1(boundary primitive + reference subtraction + corner/edge terms)",
            "dimensionless_after_A_ref_normalization",
            "BOUNDARY_FIRST_FILL_READY_NO_FLUX_OR_VALUES_MISSING",
            "boundary primitive;domain;normal convention;corner terms;reference subtraction;source_path",
            "PPN_gamma;R10;clocks;orbital",
            "source-intake/mts_residuals/P8_Y5_R10_1373_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv;source-intake/mts_residuals/P8_Y5_R10_1374_KCDB_SUBCHANNEL_BOUND_CONTRACTS.csv",
        ),
        (
            "QNF1591_4_Q_trans",
            "Q_trans",
            "Q_trans <= A_ref^-1[A_L U_B^pL/(L0^2 L_tr)+A_T U_B^pT/L_tr+A_B U_B^pB/(L0^2 L_tr)+|b_mem|A_S^2 U_B^(2pS)/L_tr^3]",
            "dimensionless_after_A_ref_normalization",
            "CLOSURE_SCHEMA_READY_PARENT_SIGNATURE_AND_VALUES_MISSING",
            "A_L;A_T;A_B;b_mem;U_B;pL;pT;pB;A_S;L0;L_tr_or_ell_tr;shell_bound",
            "PPN_gamma;R10;clocks;orbital",
            "source-intake/mts_residuals/P8_Y5_R10_1378_EXPLICIT_CLOSURE_INPUT_PACK.csv;source-intake/mts_residuals/P8_Y5_R10_1379_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv",
        ),
        (
            "QNF1591_5_Q_proj",
            "Q_proj",
            "Q_proj <= A_ref^-1 ||[P_loc, readout/divergence/trace] residual||",
            "dimensionless_after_A_ref_normalization",
            "PROJECTOR_FIRST_FILL_READY_VALUES_MISSING",
            "P_loc;readout frame;trace convention;commutator norm;source_path",
            "PPN_gamma;R10;clocks;orbital",
            "source-intake/mts_residuals/P8_Y5_R10_1373_QNORM_COMPONENT_FIRST_FILL_CONTRACTS.csv;source-intake/mts_residuals/P8_Y5_R10_1374_KCDB_SUBCHANNEL_BOUND_CONTRACTS.csv",
        ),
        (
            "QNF1591_6_Q_norm_total",
            "Q_norm",
            "Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj",
            "dimensionless_or_declared_arena_normalized_norm",
            "TOTAL_BOUND_FORM_READY_ALL_COMPONENT_VALUES_MISSING",
            "all Q_i values;units;source_paths;no-cancellation proof;arena projection",
            "PPN_gamma;R10;clocks;orbital",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1590_QGAMMA_QNORM_RUNNER_BRIDGE.csv",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "qnorm_id": qnorm_id,
            "quantity": quantity,
            "first_fill_expression": expression,
            "required_units": required_units,
            "current_status": status,
            "missing_inputs": missing_inputs,
            "arena_map": arena_map,
            "source_paths": source_paths,
            "no_cancellation_policy": "NO_CANCELLATION_ALLOWED",
            **false_flags(),
        }
        for qnorm_id, quantity, expression, required_units, status, missing_inputs, arena_map, source_paths in rows
    ]


def transition_closure_pack_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "TCP1591_0_branch_selector",
            "transition_branch",
            "gradient_relaxation_closure_only",
            "Explicit closure branch selected only for symbolic dry-run; not a parent derivation.",
            "CLOSURE_ONLY_DEFAULT",
            "source-intake/mts_residuals/P8_Y5_R10_1379_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv",
        ),
        (
            "TCP1591_1_kappa_m",
            "kappa_m",
            "positive scalar stiffness with units fixed by eta kinetic term",
            "value_or_symbol; units; sign; source_path; source_anchor; extraction_method",
            "MISSING_PARENT_VALUE_ALLOWED_SYMBOLIC_ONLY",
            "source-intake/mts_residuals/P8_Y5_R10_1379_GRADIENT_PARENT_SIGNATURE_AUDIT.csv",
        ),
        (
            "TCP1591_2_F2",
            "F2",
            "Fhat''(m_*)",
            "value_or_symbol; units; sign; source_path; source_anchor; extraction_method",
            "MISSING_PARENT_VALUE_ALLOWED_SYMBOLIC_ONLY",
            "source-intake/mts_residuals/P8_Y5_R10_1378_TRANSITION_PARENT_LAW_DERIVATION.csv",
        ),
        (
            "TCP1591_3_L0",
            "L0",
            "fixed parent scale in the fixed-L0 closure branch",
            "value_or_symbol; units; scale-setting rule; source_path; source_anchor",
            "ACTION_ROLE_ONLY_VALUE_MISSING",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1590_FIXED_L0_DOUBLE_ZERO_CONTRACT_GATE.csv",
        ),
        (
            "TCP1591_4_ell_tr",
            "ell_tr",
            "ell_tr = sqrt(kappa_m L0^2 / F2)",
            "kappa_m;F2;L0;sign_condition",
            "FORMULA_READY_SYMBOLIC_ONLY",
            "source-intake/mts_residuals/P8_Y5_R10_1379_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv",
        ),
        (
            "TCP1591_5_U_B",
            "U_B",
            "U_B = exp(-d/ell_tr)",
            "d;ell_tr;domain/reference boundary definition",
            "FORMULA_READY_DISTANCE_MISSING",
            "source-intake/mts_residuals/P8_Y5_R10_1378_TRANSITION_PARENT_LAW_DERIVATION.csv",
        ),
        (
            "TCP1591_6_Delta_m",
            "Delta_m",
            "Delta_m = A_S U_B",
            "A_S;U_B;boundary amplitude source",
            "FORMULA_READY_AMPLITUDE_MISSING",
            "source-intake/mts_residuals/P8_Y5_R10_1379_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv",
        ),
        (
            "TCP1591_7_Delta_grad_m",
            "Delta_grad_m",
            "Delta_grad_m <= A_S U_B / ell_tr",
            "A_S;U_B;ell_tr;domain norm",
            "FORMULA_READY_DOMAIN_NORM_MISSING",
            "source-intake/mts_residuals/P8_Y5_R10_1379_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv",
        ),
        (
            "TCP1591_8_support_powers",
            "pS;pL;pT;pB",
            "pS=1; pL inactive if A_L=0; pT=2 conditional for gradient stress; pB unresolved",
            "fixed-L0 signature; stress projection; boundary/shell theorem",
            "PARTIAL_CONDITIONAL_NOT_PARENT_SIGNED",
            "source-intake/mts_residuals/P8_Y5_R10_1378_TRANSITION_PARENT_LAW_DERIVATION.csv;source-intake/mts_residuals/P8_Y5_R10_1379_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv",
        ),
        (
            "TCP1591_9_Q_alg_conditional",
            "Q_alg_conditional",
            "A_ref^-1 |F2| A_S^2 U_B^2/(L0^2 ell_tr)",
            "A_ref;F2;A_S;U_B;L0;ell_tr",
            "FORMULA_READY_VALUES_MISSING",
            "source-intake/mts_residuals/P8_Y5_R10_1379_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv",
        ),
        (
            "TCP1591_10_Q_trans_conditional",
            "Q_trans_conditional",
            "retain A_T U_B^2/ell_tr + A_B U_B^pB/(L0^2 ell_tr) + |b_mem|A_S^2 U_B^2/ell_tr^3; A_L term only if fixed-L0 closure fails",
            "A_T;A_B;pB;b_mem;A_S;U_B;ell_tr;L0;shell_bound",
            "FORMULA_PARTIAL_SHELL_UNRESOLVED",
            "source-intake/mts_residuals/P8_Y5_R10_1379_TRANSITION_CLOSURE_RUNNER_SCHEMA.csv",
        ),
        (
            "TCP1591_11_shell_gate",
            "shell_status",
            "must be exact_projector_zero or explicit_finite_shell_bound",
            "projector identity/no-flux/boundary row or finite shell contribution",
            "MISSING_SHELL_CLOSURE",
            "source-intake/mts_residuals/P8_Y5_R10_1376_TRANSITION_PARENT_SOURCE_ACQUISITION.csv;source-intake/mts_residuals/P8_Y5_R10_1378_TRANSITION_PARENT_LAW_DERIVATION.csv",
        ),
        (
            "TCP1591_12_provenance_gate",
            "provenance",
            "every numeric/theorem input has source_path, source_anchor, units, extraction_method",
            "all runner fields",
            "GATE_READY_REJECT_MISSING_OR_TOY",
            "source-intake/mts_residuals/P8_Y5_R10_1377_TRANSITION_PARENT_CANDIDATE_ROW_ATTEMPT.csv",
        ),
        (
            "TCP1591_13_verdict",
            "closure_runner_status",
            "closure pack can run symbolic dry-runs and refuse claims; numeric scoring blocked",
            "TCP1591_0 through TCP1591_12",
            "TRANSITION_CLOSURE_PACK_READY_NONCLAIM",
            "aggregate_TCP1591_0_to_TCP1591_12",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "input_id": input_id,
            "input_name": input_name,
            "role_or_expression": role_or_expression,
            "required_value_or_gate": required_value_or_gate,
            "status": status,
            "source_paths": source_paths,
            "parent_signed": False,
            **false_flags(),
        }
        for input_id, input_name, role_or_expression, required_value_or_gate, status, source_paths in rows
    ]


def cr2_bound_interface_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "CBI1591_0_cR2_effective_law",
            "c_R2_eff",
            "c_R2_eff(k)=c_bare + 1/2 B^T L^-1(k)B + c_measure + c_boundary",
            "length^2_or_inverse_mass_squared_after_EH_normalization",
            "SYMBOLIC_LAW_READY_NUMERIC_OR_ZERO_MISSING",
            "c_bare;B;L^-1;c_measure;c_boundary;normalization;source_path",
            "R10;PPN;R11",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1590_CR2_COEFFICIENT_IMPLICATIONS.csv",
        ),
        (
            "CBI1591_1_Qnorm_to_gamma",
            "B_gamma",
            "B_gamma <= (c^2/(2 U_min)) N_G N_D Q_norm",
            "dimensionless_gamma_bound_after_declared_c_convention",
            "SYMBOLIC_RUNNER_FEED_READY_VALUES_MISSING",
            "U_min;N_G;N_D;Q_norm;arena potential convention;source_path",
            "PPN_gamma;Cassini",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1590_QGAMMA_QNORM_RUNNER_BRIDGE.csv;source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1591_QNORM_FIRST_FILL_SYNTHESIS.csv",
        ),
        (
            "CBI1591_2_R10_scalaron_projection",
            "alpha(lambda) from c_R2_eff/fRR",
            "R10 needs finite c_R2/fRR normalization and scalaron/range projection, or theorem-zero with source-signed proof.",
            "alpha_dimensionless_lambda_length",
            "R10_PROJECTION_BLOCKED",
            "c_R2_eff/fRR;Z;M^2;lambda;alpha;bound curve;source_path",
            "R10_short_range",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1590_FINITE_COEFFICIENT_ROW_TEMPLATE.csv",
        ),
        (
            "CBI1591_3_clock_orbital_projection",
            "clock_orbital_residual_vector",
            "Local residual vector can only feed clock/orbital arenas after Q_i values and projection matrices are source-backed.",
            "declared_clock_or_orbital_response_units",
            "ARENA_PROJECTION_BLOCKED",
            "Q_i;projection matrix;clock/orbital observable kernel;units;source_path",
            "clocks;orbital",
            "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1591_QNORM_FIRST_FILL_SYNTHESIS.csv",
        ),
        (
            "CBI1591_4_minimum_acceptance_contract",
            "finite coefficient row",
            "A row becomes scoreable only if every value has units, source path, extraction method, arena map, no-cancellation handling, and same branch id.",
            "logic_gate",
            "ACCEPTANCE_CONTRACT_READY_NO_ROW_ACCEPTED",
            "all coefficient and Q_i rows numeric or theorem-zero; no MISSING_*; same_parent_branch_id",
            "R10;PPN;clocks;orbital",
            "source-intake/mts_residuals/P8_Y5_R10_1428_BRANCH_CLASSIFIER_ROW.csv",
        ),
        (
            "CBI1591_5_verdict",
            "c_R2/Q_norm empirical fallback",
            "The fallback interface is now explicit, but no c_R2, R10, PPN, clock or orbital claim can be made from symbolic rows.",
            "logic_gate",
            "FINITE_CR2_BOUND_ROW_INTERFACE_READY_NONCLAIM",
            "source-backed numerical rows or theorem-zero certificates",
            "R10;PPN;clocks;orbital",
            "aggregate_CBI1591_0_to_CBI1591_4",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "interface_id": interface_id,
            "quantity": quantity,
            "formula_or_role": formula_or_role,
            "required_units": required_units,
            "current_status": status,
            "missing_inputs": missing_inputs,
            "observable_links": observable_links,
            "source_paths": source_paths,
            **false_flags(),
        }
        for interface_id, quantity, formula_or_role, required_units, status, missing_inputs, observable_links, source_paths in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "RUN1591_0_cdb_memory_zero",
            "accept zero theorem only if CMA1591_1 through CMA1591_7 are exact source-signed zeros",
            "CMA1591 verdict is CDB_MEMORY_ZERO_THEOREM_NOT_DERIVED",
            "REJECT_ZERO_THEOREM",
            "local-GR branch cannot reopen from fixed-L0 closure alone",
        ),
        (
            "RUN1591_1_qnorm_numeric",
            "accept Q_norm only if every Q_i has source-backed numeric/theorem-zero input and no cancellation policy passes",
            "Q_norm rows are symbolic with missing values/source locks",
            "REJECT_QNORM_NUMERIC_PASS",
            "PPN/R10/clock/orbital score blocked",
        ),
        (
            "RUN1591_2_transition_closure",
            "accept transition runner only if gradient completion is parent-signed or every closure value has finite source provenance",
            "transition closure pack is explicitly nonclaim and parent_signed=False",
            "REJECT_CLOSURE_AS_DERIVATION",
            "do not hide plateau/transition as theorem",
        ),
        (
            "RUN1591_3_cR2_bound_row",
            "accept c_R2/R10 row only if c_R2_eff, scalaron/range map and real bound curve are source-backed",
            "c_R2 interface is symbolic and R10 projection is blocked",
            "REJECT_CR2_R10_SCORE",
            "no short-range/local-GR claim",
        ),
        (
            "RUN1591_4_branch_lock",
            "accept finite rows only if same_parent_branch_id matches the 1428 branch manifest",
            f"all 1591 rows use {BRANCH_ID} but remain missing inputs",
            "BRANCH_LOCK_OK_INPUTS_PENDING",
            "branch hygiene passes; physics claim still blocked",
        ),
        (
            "RUN1591_5_future_acceptance",
            "future runner may promote only source-backed values with units, source anchors, extraction method, arena projection and no MISSING_*",
            "no current row satisfies the full rule",
            "WAIT_FOR_SOURCE_BACKED_ROWS",
            "next target should try parent signature first, then acquisition",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": runner_id,
            "acceptance_rule": acceptance_rule,
            "input_state": input_state,
            "runner_result": runner_result,
            "effect": effect,
            **false_flags(),
        }
        for runner_id, acceptance_rule, input_state, runner_result, effect in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1591_0_CDB_zero", "K_conn/K_domain/K_boundary theorem-zero", "BLOCKED_NO_CLAIM", "CDB/memory zero theorem not derived"),
        ("GATE1591_1_Qnorm_bound", "Q_norm finite bound pass", "BLOCKED_NO_CLAIM", "all component values remain missing or closure-only"),
        ("GATE1591_2_cR2_zero", "c_R2/fRR theorem-zero", "BLOCKED_NO_CLAIM", "fixed-L0 algebra does not remove c_bare, c_measure, c_boundary, K_cdb or memory stress"),
        ("GATE1591_3_R10", "R10 alpha/lambda score", "BLOCKED_NO_CLAIM", "no finite c_R2/scalaron/range projection row"),
        ("GATE1591_4_PPN", "PPN gamma/Cassini score", "BLOCKED_NO_CLAIM", "B_gamma feed has Q_norm, U_min, N_G and N_D missing"),
        ("GATE1591_5_clock_orbital", "clock/orbital local residual pass", "BLOCKED_NO_CLAIM", "arena projection matrices and residual values missing"),
        ("GATE1591_6_local_GR", "local GR / Newton recovery", "BLOCKED_NO_CLAIM", "neither exact zero theorem nor finite empirical pass is available"),
        ("GATE1591_7_public_claim", "public/publishable local branch claim", "BLOCKED_NO_CLAIM", "1591 is private derivation discipline and nonclaim interface work"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **false_flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1591_0_fixed_L0_kept",
            "KEEP_FIXED_L0_DOUBLE_ZERO_AS_BEST_LOCAL_BRANCH",
            "it remains the cleanest algebraic local route and avoids the old L_cg/profile smuggling problem",
            "continue to use it as a branch, not as a live parent theorem",
        ),
        (
            "DEC1591_1_residual_theorem_failed",
            "CDB_MEMORY_ZERO_THEOREM_NOT_DERIVED",
            "K_conn, K_domain, K_boundary, memory stress, shell and projector leakage still need source-signed zeros or finite bounds",
            "do not claim local GR; route through Q_norm/cR2 interface",
        ),
        (
            "DEC1591_2_interface_gain",
            "QNORM_AND_CR2_FIRST_FILL_INTERFACE_NOW_EXPLICIT",
            "the missing work is no longer vague: each Q_i, c_R2_eff and arena projection has a named slot, formula and source requirement",
            "future code can refuse bad rows and accept only source-backed/theorem-zero rows",
        ),
        (
            "DEC1591_3_best_next",
            "NEXT_1592_TRANSITION_GRADIENT_PARENT_SIGNATURE_OR_QNORM_SOURCE_ACQUISITION",
            "derivation-first still says try to parent-sign kappa_m/eta/Euler/source/boundary; if that fails, start filling real finite Q_i rows",
            "try the gradient parent signature route first, then source acquisition for operator norms and arena maps",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "reason": reason,
            "next_action": next_action,
            **false_flags(),
        }
        for decision_id, decision, reason, next_action in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_target": "1592-Y5-R2FR-transition-gradient-parent-signature-or-Qnorm-source-acquisition.md",
            "script": "scripts/Y5_R2FR_transition_gradient_parent_signature_or_Qnorm_source_acquisition.py",
            "objective": "try to parent-sign the gradient completion branch by locating or writing the exact action slot for eta, kappa_m, Euler/source map, boundary/shell condition and stress routing; if not, begin source acquisition for Q_i/operator norm rows",
            "success_condition": "parent-signed transition/gradient mechanism for Q_alg/Q_trans and K_conn source amplitudes, or source-ready nonclaim Q_i rows with units, provenance and arena maps",
            "do_not": "do not adopt closure as derivation, do not score local tests from symbolic rows, do not edit formalization-workbench or GitHub",
            **false_flags(),
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


def generated_flags_false(generated_csvs: list[Path]) -> bool:
    flag_columns = {"score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed", "parent_signed"}
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


def has_1591_rows(folder: Path) -> bool:
    if not folder.exists():
        return False
    return any("1591" in csv_path.name for csv_path in folder.glob("*.csv"))


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    cdb_memory = read_csv(CDB_MEMORY_AUDIT)
    qnorm = read_csv(QNORM_FIRST_FILL)
    transition = read_csv(TRANSITION_CLOSURE_PACK)
    interface = read_csv(CR2_BOUND_INTERFACE)
    runner = read_csv(RUNNER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    qnorm_components = {"Q_alg", "Q_cdb", "Q_mem", "Q_bdy", "Q_trans", "Q_proj"}
    checks = [
        ("VAL1591_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1591 source paths exist"),
        ("VAL1591_1_needles_found", all(row["needle_found"] == "True" for row in sources), "all 1591 source needles found"),
        (
            "VAL1591_2_cdb_memory_zero_not_derived",
            any(row["audit_id"] == "CMA1591_8_verdict" and row["status"] == "CDB_MEMORY_ZERO_THEOREM_NOT_DERIVED" for row in cdb_memory),
            "CDB/memory exact zero theorem remains blocked",
        ),
        (
            "VAL1591_3_qnorm_components_complete_nonclaim",
            qnorm_components.issubset({row["quantity"] for row in qnorm})
            and all(row["valid_for_claim"] == "False" and "MISSING" in row["current_status"] for row in qnorm if row["quantity"] in qnorm_components),
            "all six Q_norm components have first-fill formulas and missing-value status",
        ),
        (
            "VAL1591_4_transition_pack_closure_only",
            any(row["input_id"] == "TCP1591_13_verdict" and row["status"] == "TRANSITION_CLOSURE_PACK_READY_NONCLAIM" for row in transition)
            and all(row["parent_signed"] == "False" and row["valid_for_claim"] == "False" for row in transition),
            "transition pack is explicit closure-only and parent_unsigned",
        ),
        (
            "VAL1591_5_cR2_interface_blocks_claims",
            any(row["interface_id"] == "CBI1591_5_verdict" and row["current_status"] == "FINITE_CR2_BOUND_ROW_INTERFACE_READY_NONCLAIM" for row in interface)
            and all(row["valid_for_claim"] == "False" for row in interface),
            "c_R2/Q_norm interface exists but remains nonclaim",
        ),
        (
            "VAL1591_6_runner_rejects_current_rows",
            any(row["runner_result"] == "REJECT_ZERO_THEOREM" for row in runner)
            and any(row["runner_result"] == "REJECT_QNORM_NUMERIC_PASS" for row in runner)
            and any(row["runner_result"] == "REJECT_CLOSURE_AS_DERIVATION" for row in runner)
            and any(row["runner_result"] == "REJECT_CR2_R10_SCORE" for row in runner),
            "runner refuses current zero, Q_norm, closure and c_R2/R10 claims",
        ),
        (
            "VAL1591_7_claim_gates_closed",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in gates),
            "all 1591 claim gates remain closed",
        ),
        (
            "VAL1591_8_decision_next",
            any(row["decision"] == "NEXT_1592_TRANSITION_GRADIENT_PARENT_SIGNATURE_OR_QNORM_SOURCE_ACQUISITION" for row in decisions),
            "decision selects gradient parent signature or Qnorm source acquisition",
        ),
        ("VAL1591_9_csv_parse", all(len(read_csv(csv_path)) > 0 for csv_path in generated_csvs), "all generated 1591 CSVs parse cleanly"),
        ("VAL1591_10_claim_flags_false", generated_flags_false(generated_csvs), "all generated claim/prediction/parent-signed flags remain false"),
        ("VAL1591_11_no_raw_accepted", not has_1591_rows(RAB_RAW) and not has_1591_rows(RAB_ACCEPTED), "no 1591 rows written to raw/accepted finite directories"),
        ("VAL1591_12_branch_copies", all(target_path.exists() for target_paths in COPY_TARGETS.values() for target_path in target_paths), "branch/quarantine nonclaim copies written"),
        ("VAL1591_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1591_14_formalization_untouched", formalization_scope_clean(generated_csvs), "all generated 1591 paths are outside formalization-workbench; git status is clean when available"),
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
            "check_id": "VAL1591_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1591 fixed-L0 CDB/memory Qnorm first-fill or cR2 bound row validation",
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
    cdb_memory: list[dict[str, Any]],
    qnorm: list[dict[str, Any]],
    transition: list[dict[str, Any]],
    interface: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n\n".join(
            [
                "# 1591 - R2/fR Fixed-L0 CDB Memory Qnorm First Fill Or cR2 Bound Row",
                "## Verdict\n"
                "- 1591 tries the derivation-first move: can fixed `L0` plus the strict double-zero branch make `K_conn`, `K_domain`, `K_boundary`, memory stress, transition shell and projector leakage vanish? Current answer: **not yet**.\n"
                "- The good news is that the bottleneck is now precise, not foggy: the algebraic `m/L0` sector is clean, but the CDB/memory/source couplings need parent-signed zero theorems or finite source-backed component rows.\n"
                "- `Q_norm <= Q_alg + Q_cdb + Q_mem + Q_bdy + Q_trans + Q_proj` is retained as the no-cancellation testing lane, with each component given a first-fill formula, units requirement, source path requirement and arena map.\n"
                "- The transition-gradient route remains the best mathematical route, but it is closure-only until `eta`, `kappa_m`, the Euler/source map, boundary/shell condition and stress routing are parent-signed.\n"
                "- No local-GR, Newton, PPN, R10, clock, orbital, R2/fR, scalaron, WEP, common-matter or public claim is made.",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "needle_found", "needles"]),
                "## CDB/Memory Theorem Attempt",
                md_table(cdb_memory, ["audit_id", "channel", "attempted_zero", "evidence_summary", "status", "blocking_gap"]),
                "## Qnorm First-Fill Synthesis",
                md_table(qnorm, ["qnorm_id", "quantity", "first_fill_expression", "required_units", "current_status", "missing_inputs", "arena_map"]),
                "## Transition Closure Pack",
                md_table(transition, ["input_id", "input_name", "role_or_expression", "required_value_or_gate", "status", "parent_signed"]),
                "## cR2 Bound Row Interface",
                md_table(interface, ["interface_id", "quantity", "formula_or_role", "required_units", "current_status", "missing_inputs", "observable_links"]),
                "## Runner Refusal",
                md_table(runner, ["runner_id", "acceptance_rule", "input_state", "runner_result", "effect"]),
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "reason", "next_action"]),
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
    cdb_memory = cdb_memory_audit_rows()
    qnorm = qnorm_first_fill_rows()
    transition = transition_closure_pack_rows()
    interface = cr2_bound_interface_rows()
    runner = runner_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()
    generated_csvs = [
        SOURCE_REGISTER,
        CDB_MEMORY_AUDIT,
        QNORM_FIRST_FILL,
        TRANSITION_CLOSURE_PACK,
        CR2_BOUND_INTERFACE,
        RUNNER,
        CLAIM_GATE,
        DECISION,
        NEXT_TARGET,
    ]
    write_csv(SOURCE_REGISTER, sources)
    write_csv(CDB_MEMORY_AUDIT, cdb_memory)
    write_csv(QNORM_FIRST_FILL, qnorm)
    write_csv(TRANSITION_CLOSURE_PACK, transition)
    write_csv(CR2_BOUND_INTERFACE, interface)
    write_csv(RUNNER, runner)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, cdb_memory, qnorm, transition, interface, runner, gates, decisions, validation, next_rows)


if __name__ == "__main__":
    main()
