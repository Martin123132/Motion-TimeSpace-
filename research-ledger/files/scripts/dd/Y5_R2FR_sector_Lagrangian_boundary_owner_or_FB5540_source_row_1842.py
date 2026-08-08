from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1842"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1842-Y5-R2FR-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1842_0_1841_next",
        "source_key": "1841_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_NEXT_TARGET.csv",
        "needles": ["NEXT1841_0_primary", "1842-Y5-R2FR-sector-Lagrangian"],
        "role": "1841 selects sector Lagrangian/boundary owner or FB5540 source row.",
    },
    {
        "source_id": "SRC1842_1_1841_validation",
        "source_key": "1841_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1841_VALIDATION.csv",
        "needles": ["VAL1841_OVERALL", "PASS"],
        "role": "confirms 1841 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1842_2_1841_source_root",
        "source_key": "1841_source_normalization_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1841_OPERATOR_BOUND_INPUT_PACK.csv",
        "needles": ["OBI1841_6_source_normalization", "MISSING_MHREF_AND_FB5540_COMPONENTS"],
        "role": "1841 makes M_H_ref plus FB5540 components the source-normalization root row.",
    },
    {
        "source_id": "SRC1842_3_1017_reference_lock",
        "source_key": "1017_hamiltonian_reference_lock",
        "source_path": ROOT / "1017-Y5-R10-Hamiltonian-PiM-reference-lock-or-MHref-first-row.md",
        "needles": ["HPT1017_5_verdict", "fail_current_claim"],
        "role": "1017 identifies the Hamiltonian reference/integrability lock and first-row schema.",
    },
    {
        "source_id": "SRC1842_4_1018_owner_status",
        "source_key": "1018_sector_owner_status",
        "source_path": ROOT / "1018-Y5-R10-sector-Lagrangian-boundary-owner-or-FB5540-source-row.md",
        "needles": ["LOC1018_8_verdict", "fail_current_claim"],
        "role": "1018 supplies the sector-owner map and current failure.",
    },
    {
        "source_id": "SRC1842_5_1018_source_schema",
        "source_key": "1018_source_row_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_1018_SOURCE_ROW_SCHEMA.csv",
        "needles": ["FSR1018_7_total_guard", "NOT_COMPUTED_COMPONENTS_MISSING"],
        "role": "1018 source schema lists FB5540, bulk, edge and no-cancellation inputs.",
    },
    {
        "source_id": "SRC1842_6_1018_next",
        "source_key": "1018_next_target",
        "source_path": RESIDUALS / "P8_Y5_R10_1018_NEXT_TARGET.csv",
        "needles": ["1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md", "derive boundary exactness"],
        "role": "1018 selects boundary exactness/projector orthogonality or source pack as the next theorem route.",
    },
    {
        "source_id": "SRC1842_7_1019_boundary_status",
        "source_key": "1019_boundary_projector_precedent",
        "source_path": ROOT / "1019-Y5-R10-boundary-exactness-projector-orthogonality-or-source-pack.md",
        "needles": ["BE1019_6_verdict", "fail_current_claim"],
        "role": "1019 shows the boundary/projector route is precise but still parent-unsigned.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1842_SOURCE_REGISTER.csv",
    "owner_clauses": RESIDUALS / "P8_Y5_PARENT_QLOC_1842_OWNER_CLAUSES.csv",
    "route_tests": RESIDUALS / "P8_Y5_PARENT_QLOC_1842_ROUTE_TESTS.csv",
    "source_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1842_FB5540_SOURCE_ROW_SCHEMA.csv",
    "source_runner": RESIDUALS / "P8_Y5_PARENT_QLOC_1842_FB5540_SOURCE_ROW_RUNNER.csv",
    "gr_bridge": RESIDUALS / "P8_Y5_PARENT_QLOC_1842_GR_BRIDGE_STATUS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1842_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1842_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1842_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1842_VALIDATION.csv",
}


def ensure_dirs() -> None:
    for directory in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": path.exists(),
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def owner_clause_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "owner_id": "LOC1842_0_LX_owner",
            "required_owner": "parent-owned extra-sector Lagrangian",
            "mathematical_form": "L_X[g,X,nabla X] with explicit operator, source term, normalization and boundary conditions",
            "current_status": "NOT_SIGNED",
            "failure_if_missing": "Theta_X,Q_X,omega_X,C_X,R10/R11 and local scaling cannot be computed",
            "feeds": "delta_H_tau_nonintegrable_over_MH;C_extra;R10;R11",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "LOC1842_1_Theta_QX_owner",
            "required_owner": "sector symplectic potential and Hamiltonian charge",
            "mathematical_form": "delta L_X=E_X delta X+dTheta_X; J_tau^X=Theta_X(L_tau X)-i_tau L_X=dQ_tau^X+C_tau^X",
            "current_status": "FORMULA_WRITTEN_NOT_OWNED",
            "failure_if_missing": "Hamiltonian integrability remains schematic",
            "feeds": "delta_H_tau_nonintegrable_over_MH;symplectic_boundary_flux_over_MH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "LOC1842_2_no_pole_quotient",
            "required_owner": "X is absent from physical quotient or first-class vertical",
            "mathematical_form": "Dq[v_X]=0 and delta G_X=Omega(delta Phi,v_X) is differentiable with zero boundary charge",
            "current_status": "CONDITIONAL_ROUTE_UNSIGNED",
            "failure_if_missing": "parent Omega/DC_X and boundary charge owner do not close",
            "feeds": "K_X;qbar_XT;Qbar_XH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "LOC1842_3_positive_sourcefree",
            "required_owner": "positive source-free local X operator",
            "mathematical_form": "O_X X=-nabla_i(Z_X nabla^i X)+M_X^2 X, with Z_X>0, M_X^2>0, J_X=0, boundary_flux_X=0",
            "current_status": "CONDITIONAL_THEOREM_UNSIGNED",
            "failure_if_missing": "Z_X,M_X^2,J_X=0 and boundary_flux_X=0 are not parent-signed together",
            "feeds": "lambda_X;alpha_X;R10;R11",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "LOC1842_4_Bref_owner",
            "required_owner": "reference boundary functional selected before readout",
            "mathematical_form": "B_ref[gamma_ref,tau_ref,C_top] with partial_{source,r,t,frame,lambda}Delta_ref=0",
            "current_status": "NOT_SIGNED",
            "failure_if_missing": "reference can absorb source calibration",
            "feeds": "Delta_ref_over_MH;Delta_symp_over_MH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "LOC1842_5_Bclass_owner",
            "required_owner": "boundary class/no-hair/projector silence",
            "mathematical_form": "B_class[chi_B,C_top] plus exact/proper-gauge/no-vector-tensor-hair conditions",
            "current_status": "NOT_SIGNED",
            "failure_if_missing": "symplectic boundary flux and edge charge remain live",
            "feeds": "B_zero_flux;symplectic_boundary_flux;Qbar_edge_XH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "LOC1842_6_tau_owner",
            "required_owner": "same generator for source, charge, clocks and readout",
            "mathematical_form": "tau_source=tau_charge=tau_clock=tau_readout up to source-backed mismatch bound",
            "current_status": "NOT_SIGNED",
            "failure_if_missing": "Hamiltonian source charge and clock/PPN readout can drift apart",
            "feeds": "tau_lock_mismatch;clock;PPN;M_H_ref",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "LOC1842_7_MHref_owner",
            "required_owner": "same-frame Hamiltonian/Hilbert source denominator",
            "mathematical_form": "M_H_ref=H_tau[S_outer]-H_ref=int_S Q_tau - H_ref, positive and fixed before orbital readout",
            "current_status": "MISSING_STABLE_MH_REF",
            "failure_if_missing": "R_eq/FB5540/source-normalization rows are unnormalized",
            "feeds": "FB5540;R_eq;I_commutator;Newton;local_GR",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "LOC1842_8_verdict",
            "required_owner": "all owners needed for FB5540 and local-GR source charge",
            "mathematical_form": "LOC1842_0 through LOC1842_7 parent-signed together",
            "current_status": "FAIL_CURRENT_CLAIM",
            "failure_if_missing": "current MTS has a precise owner map but no owner closure",
            "feeds": "FB5540;R10;R11;local_GR",
            "valid_for_claim": False,
        },
    ]


def route_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "RT1842_0_direct_owner",
            "route": "derive full L_X/Theta_X/Q_X/B/tau owner",
            "mathematical_form": "one parent action gives E_X,Theta_X,Q_X,B_ref,B_class,tau,M_H_ref without post-readout fitting",
            "current_status": "BEST_BUT_UNSIGNED",
            "blocker": "sector Lagrangian and boundary/tau owners are incomplete",
            "fallback": "FB5540 source row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RT1842_1_vertical_constraint",
            "route": "X is vertical first-class constraint direction",
            "mathematical_form": "delta G_X=Omega(delta Phi,v_X); Q_X differentiable; K_boundary=0",
            "current_status": "BEST_ZERO_ROUTE_NOT_SIGNED",
            "blocker": "single parent owner and boundary differentiability do not close",
            "fallback": "edge residual vector retained",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RT1842_2_positive_sourcefree",
            "route": "positive source-free local operator kills X profile",
            "mathematical_form": "int_A(Z_X|grad X|^2+M_X^2X^2)=int_A XJ_X+boundary_flux_X",
            "current_status": "CONDITIONAL_THEOREM_ONLY",
            "blocker": "Z_X,M_X^2,J_X=0,boundary_flux_X=0 missing",
            "fallback": "alpha/lambda residual vector retained",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RT1842_3_massive_sourced",
            "route": "finite physical X residual",
            "mathematical_form": "lambda_X=sqrt(Z_X/M_X^2), alpha_X=K_X Qbar_XH qbar_XT",
            "current_status": "SCHEMA_READY_NO_VALUES",
            "blocker": "all coefficients/units/source paths missing or nonclaim",
            "fallback": "R10/R11 source acquisition required",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RT1842_4_edge_branch",
            "route": "edge/boundary charge residual",
            "mathematical_form": "alpha_edge(lambda)=K_edge(lambda)Qbar_edge_XH(lambda)qbar_XT",
            "current_status": "SCHEMA_READY_NO_VALUES",
            "blocker": "boundary exactness/projector orthogonality and edge coefficients missing",
            "fallback": "edge residual vector retained",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "RT1842_5_verdict",
            "route": "sector Lagrangian/boundary owner closed",
            "mathematical_form": "one zero-theorem route closes or source-backed RT1842_3/4 rows exist with no-cancellation guard",
            "current_status": "FAIL_CURRENT_CLAIM",
            "blocker": "no route signs enough clauses or supplies source-backed values",
            "fallback": "move to boundary exactness/projector orthogonality or source pack",
            "valid_for_claim": False,
        },
    ]


def source_schema_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FSR1842_0_M_H_ref",
            "quantity": "M_H_ref",
            "definition": "same-frame Hamiltonian source denominator",
            "required_columns": "system_id;surface;Q_tau_integral;G_ref;H_ref;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_STABLE_MH_REF",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FSR1842_1_delta_H_tau",
            "quantity": "delta_H_tau_nonintegrable_over_MH",
            "definition": "field-space curl of Hamiltonian variation normalized by M_H_ref",
            "required_columns": "system_id;surface_pair;omega_X_integral;reference_curl;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_INTEGRABILITY_NUMERIC_OR_THEOREM_ZERO",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FSR1842_2_Delta_ref",
            "quantity": "Delta_ref_over_MH",
            "definition": "reference shift/derivative profile normalized by M_H_ref",
            "required_columns": "system_id;reference_branch;Delta_ref;derivative_profile;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_REFERENCE_NUMERIC_OR_THEOREM_ZERO",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FSR1842_3_boundary_flux",
            "quantity": "symplectic_boundary_flux_over_MH;B_zero_flux;Delta_symp",
            "definition": "boundary/projector/non-EH linked flux normalized by M_H_ref",
            "required_columns": "system_id;surface_pair;symplectic_boundary_flux;B_zero_flux;Delta_symp;M_H_ref;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_SYMPLECTIC_BOUNDARY_NUMERIC_OR_THEOREM_ZERO",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FSR1842_4_LX_bulk_coefficients",
            "quantity": "Z_X;M_X2;J_X;lambda_X",
            "definition": "bulk X-sector coefficients if no theorem-zero route closes",
            "required_columns": "system_id;field_id;Z_X;M_X2;J_X;lambda_X;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_PARENT_INPUT",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FSR1842_5_R10_source_projection",
            "quantity": "K_X;Qbar_XH;qbar_XT",
            "definition": "R10 residual amplitude factors for active X exchange",
            "required_columns": "system_id;K_X;Qbar_XH;qbar_XT;normalization;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FSR1842_6_edge_projection",
            "quantity": "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT",
            "definition": "edge/boundary residual amplitude factors if boundary theorem fails",
            "required_columns": "system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;units;source_path;assumptions;valid_for_claim",
            "current_status": "MISSING_EDGE_COEFFICIENTS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FSR1842_7_total_guard",
            "quantity": "FB5540_alpha_R11_total_guard",
            "definition": "no-cancellation envelope across FB5540, bulk X, edge X and R11 coefficients",
            "required_columns": "system_id;component_sum_abs;M_H_ref;normalization;source_path;assumptions;valid_for_claim",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "valid_for_claim": False,
        },
    ]


def source_runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "runner_id": f"FRR1842_{index}_{row['row_id'].split('_', 2)[-1]}",
            "row_id": row["row_id"],
            "quantity": row["quantity"],
            "computed_status": "BLOCKED_MISSING_INPUTS",
            "claim_allowed": False,
            "failure_reasons": "MISSING_THEOREM_OR_SOURCE_INPUT;VALID_FOR_CLAIM_FALSE",
        }
        for index, row in enumerate(source_schema_rows())
    ]


def gr_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1842_0_owner_map",
            "bridge_piece": "sector owner map",
            "current_status": "EXPLICIT_BUT_UNSIGNED",
            "evidence": "LOC1842 rows",
            "remaining_gap": "no owner route closes current MTS",
            "valid_for_claim": False,
        },
        {
            "branch_id": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428",
            "status_id": "GB1842_1_source_row",
            "bridge_piece": "FB5540/source-normalization first row",
            "current_status": "SCHEMA_READY_NO_VALUES",
            "evidence": "FSR1842 rows",
            "remaining_gap": "M_H_ref and numerator components missing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1842_2_zero_route",
            "bridge_piece": "no-pole/source-free theorem route",
            "current_status": "CONDITIONAL_NOT_PROMOTED",
            "evidence": "RT1842_1;RT1842_2",
            "remaining_gap": "boundary exactness, projector orthogonality, positive operator and source-free conditions are unsigned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1842_3_Newton_GR",
            "bridge_piece": "Newton/local-GR route",
            "current_status": "BLOCKED",
            "evidence": "LOC1842_8;FRR1842 rows",
            "remaining_gap": "local GR cannot reopen until owner map or source pack closes",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1842_4_next",
            "bridge_piece": "next derivation owner",
            "current_status": "BOUNDARY_EXACTNESS_PROJECTOR_ORTHOGONALITY_OR_SOURCE_PACK_IS_NEXT",
            "evidence": "1018/1019 route split",
            "remaining_gap": "derive boundary exactness/projector orthogonality or build complete no-cancellation source pack",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1842_0_owner_map_written",
            "claim": "sector Lagrangian/boundary owner map is explicit",
            "gate_pass": True,
            "reason": "owner clauses cover L_X,Theta/Q,quotient,sourcefree,B_ref,boundary,tau and M_H_ref",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1842_1_LX_owned",
            "claim": "L_X,Theta_X,Q_X,omega_X are parent-owned",
            "gate_pass": False,
            "reason": "minimal candidates are routes, not signed current-MTS derivations",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1842_2_no_pole_zero",
            "claim": "X has no physical pole and no R10/R11 residual",
            "gate_pass": False,
            "reason": "parent Omega/DC_X plus boundary charge silence are unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1842_3_positive_sourcefree_zero",
            "claim": "X=0 in compact local exterior by positive source-free theorem",
            "gate_pass": False,
            "reason": "Z_X,M_X2,J_X=0 and boundary_flux_X=0 are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1842_4_FB5540_first_row_ready",
            "claim": "FB5540 source row is claim-ready",
            "gate_pass": False,
            "reason": "M_H_ref and numerator components remain missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1842_5_R10_R11_ready",
            "claim": "R10/R11 residual vectors are source-backed",
            "gate_pass": False,
            "reason": "bulk and edge coefficients are missing/nonclaim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1842_6_Newton_local_GR",
            "claim": "Newton/local-GR gates can reopen",
            "gate_pass": False,
            "reason": "source charge, FB5540, R10/R11 and PPN owners remain blocked",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1842_0_owner_result",
            "decision": "OWNER_MAP_SHARP_BUT_NOT_CLOSED",
            "reason": "L_X/Theta_X/Q_X,B_ref,B_class/C_top/chi_B,tau,M_H_ref and boundary charge are all explicit but unsigned",
            "next_action": "do not promote FB5540,R10,R11,Newton or local GR from symbolic sector machinery",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1842_1_best_derivation_route",
            "decision": "NO_POLE_ROUTE_STRONGEST_IF_BOUNDARY_PROJECTOR_CLOSE",
            "reason": "it removes the physical X pole structurally instead of fitting a small coefficient",
            "next_action": "try boundary exactness/projector orthogonality before coefficient sourcing",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1842_2_source_row_fallback",
            "decision": "FULL_NO_CANCELLATION_SOURCE_ROW_REQUIRED_IF_THEOREM_FAILS",
            "reason": "FB5540,bulk X,edge X and R11 components cannot cancel as unknowns or borrow orbital GM as denominator",
            "next_action": "source M_H_ref and all numerator/edge/bulk factors together or keep row blocked",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1842_3_best_next",
            "decision": "BOUNDARY_EXACTNESS_PROJECTOR_ORTHOGONALITY_OR_SOURCE_PACK_IS_NEXT",
            "reason": "edge/source leakage is the first place a structural theorem could kill the residual branch without data fitting",
            "next_action": "1843-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1842_0_primary",
            "next_target": "1843-Y5-R2FR-boundary-exactness-projector-orthogonality-or-source-pack.md",
            "script": "scripts/Y5_R2FR_boundary_exactness_projector_orthogonality_or_source_pack_1843.py",
            "objective": "derive boundary exactness, projector orthogonality and no edge/source double-count for the X/Hamiltonian branch, or build a complete source pack for FB5540 plus bulk/edge R10/R11 coefficients",
            "selection_status": "selected",
            "success_condition": "Q_edge and Qbar_edge_XH are theorem-zero, or FB5540/bulk/edge/R11 source rows are complete, source-backed and no-cancellation guarded",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1842_1_parallel",
            "next_target": "1843b-Y5-R2FR-MHref-first-source-row-acquisition.md",
            "script": "scripts/Y5_R2FR_MHref_first_source_row_acquisition_1843b.py",
            "objective": "if derivation stalls, stage a complete nonclaim M_H_ref and numerator source row acquisition checklist",
            "selection_status": "parallel_held",
            "success_condition": "no numeric score is possible unless denominator and all numerator components are real and sourced",
        },
    ]


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "owner_clauses": owner_clause_rows(),
        "route_tests": route_test_rows(),
        "source_schema": source_schema_rows(),
        "source_runner": source_runner_rows(),
        "gr_bridge": gr_bridge_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames(rows: list[dict[str, Any]]) -> list[str]:
    names: list[str] = []
    for row in rows:
        for key in row:
            if key not in names:
                names.append(key)
    return names


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames(rows))
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        for target in [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1842_{key.upper()}.csv",
        ]:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)


def parse_csv_ok(path: Path) -> bool:
    try:
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def csv_parse_all() -> bool:
    return all(parse_csv_ok(path) for key, path in OUTPUTS.items() if key != "validation")


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1842_{key.upper()}.csv").exists():
            return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = [
        "1842-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1842",
        "P8_Y5_BRR545_1842",
        "Y5_R2FR_sector_Lagrangian_boundary_owner_or_FB5540_source_row_1842",
    ]
    return not any(any(marker in path.name for marker in markers) for path in FORMALIZATION.rglob("*"))


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    allowed_true = {"CG1842_0_owner_map_written"}
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            if row.get("gate_id") in allowed_true and row.get("gate_pass") is True:
                continue
            for field in ["valid_for_claim", "claim_allowed", "gate_pass", "score_ready"]:
                if row.get(field) is True:
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            has_missing = any("MISSING_" in str(value) for value in row.values())
            if not has_missing:
                continue
            for field in ["valid_for_claim", "claim_allowed", "score_ready"]:
                if row.get(field) is True:
                    return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    checks = [
        ("VAL1842_0_sources_exist", all(row["exists"] is True for row in source_rows), "all cited source paths exist"),
        ("VAL1842_1_needles_present", all(row["needles_present"] is True for row in source_rows), "all cited source needles are present"),
        (
            "VAL1842_2_owner_map_complete",
            {"LOC1842_0_LX_owner", "LOC1842_1_Theta_QX_owner", "LOC1842_4_Bref_owner", "LOC1842_7_MHref_owner", "LOC1842_8_verdict"}.issubset({row["owner_id"] for row in rows_map["owner_clauses"]}),
            "owner map covers L_X, Theta/Q, boundary, tau/MHref and verdict",
        ),
        (
            "VAL1842_3_owner_map_blocks_claim",
            any(row["owner_id"] == "LOC1842_8_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in rows_map["owner_clauses"]),
            "owner map remains nonclaim and blocks current promotion",
        ),
        (
            "VAL1842_4_route_split_written",
            {"RT1842_1_vertical_constraint", "RT1842_2_positive_sourcefree", "RT1842_3_massive_sourced", "RT1842_4_edge_branch", "RT1842_5_verdict"}.issubset({row["route_id"] for row in rows_map["route_tests"]}),
            "route split covers zero routes and source fallback",
        ),
        (
            "VAL1842_5_source_schema_complete",
            {"FSR1842_0_M_H_ref", "FSR1842_1_delta_H_tau", "FSR1842_3_boundary_flux", "FSR1842_4_LX_bulk_coefficients", "FSR1842_6_edge_projection", "FSR1842_7_total_guard"}.issubset({row["row_id"] for row in rows_map["source_schema"]}),
            "source schema covers FB5540, bulk X, edge X and total guard rows",
        ),
        (
            "VAL1842_6_source_schema_nonclaim",
            all(row["valid_for_claim"] is False for row in rows_map["source_schema"]) and all(row["claim_allowed"] is False for row in rows_map["source_runner"]),
            "all source schema/runner rows remain missing and nonclaim",
        ),
        (
            "VAL1842_7_GR_bridge_next",
            any(row["status_id"] == "GB1842_4_next" and row["current_status"] == "BOUNDARY_EXACTNESS_PROJECTOR_ORTHOGONALITY_OR_SOURCE_PACK_IS_NEXT" for row in rows_map["gr_bridge"]),
            "GR bridge selects boundary/projector/source-pack next",
        ),
        (
            "VAL1842_8_claim_gates_blocked",
            all((row["gate_pass"] is False or row["gate_id"] == "CG1842_0_owner_map_written") and row["claim_allowed"] is False for row in rows_map["claim_gate"]),
            "owner, R10/R11, Newton and local-GR claims remain blocked",
        ),
        ("VAL1842_9_no_claim_flags", no_claim_flags(rows_map), "no generated claim flags are true"),
        ("VAL1842_10_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1842_11_decision_next",
            any(row["decision_id"] == "DEC1842_3_best_next" and row["decision"] == "BOUNDARY_EXACTNESS_PROJECTOR_ORTHOGONALITY_OR_SOURCE_PACK_IS_NEXT" for row in rows_map["decision"]),
            "decision selects boundary/projector/source-pack route",
        ),
        (
            "VAL1842_12_next_selected",
            any(row["route_id"] == "NEXT1842_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1842_13_csv_parse", csv_parse_all(), "all generated 1842 CSVs parse"),
        ("VAL1842_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1842_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1842_16_formalization_untouched", no_formalization_outputs(), "no 1842 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1842_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1842 sector Lagrangian boundary owner or FB5540 source row",
        }
    )
    return rows


def markdown_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(markdown_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1842 Y5 R2FR sector Lagrangian boundary owner or FB5540 source row",
            "",
            "**Progress:** 1842 ties the local GR/Newton source-charge problem to concrete owner clauses: `L_X`, `Theta_X`, `Q_X`, `B_ref`, boundary class/no-hair, tau lock, and a same-frame `M_H_ref`.",
            "",
            "**Current verdict:** the owner map is sharp, but it does not close current MTS. There is no theorem-zero route for `FB5540`, no stable `M_H_ref`, and no source-backed bulk/edge coefficient pack.",
            "",
            "**Claim ceiling:** no `L_X` owner, `FB5540=0`, source-free X theorem, R10/R11 pass, measured-GM closure, Newton/GR reduction, PPN pass, local-GR claim, GitHub action, or `formalization-workbench` edit is allowed from 1842.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Owner Clauses",
            markdown_table(rows_map["owner_clauses"], ["owner_id", "required_owner", "mathematical_form", "current_status", "failure_if_missing", "feeds", "valid_for_claim"]),
            "",
            "## Route Tests",
            markdown_table(rows_map["route_tests"], ["route_id", "route", "mathematical_form", "current_status", "blocker", "fallback", "valid_for_claim"]),
            "",
            "## FB5540 Source Row Schema",
            markdown_table(rows_map["source_schema"], ["row_id", "quantity", "definition", "required_columns", "current_status", "valid_for_claim"]),
            "",
            "## FB5540 Source Row Runner",
            markdown_table(rows_map["source_runner"], ["runner_id", "row_id", "quantity", "computed_status", "claim_allowed", "failure_reasons"]),
            "",
            "## GR Bridge Status",
            markdown_table(rows_map["gr_bridge"], ["status_id", "bridge_piece", "current_status", "evidence", "remaining_gap", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is the cleanest place to keep pushing. If boundary exactness and projector orthogonality can be parent-signed, a big chunk of local residual hair dies structurally. If they cannot, the theory must carry a complete source pack instead of claiming GR by notation.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1842 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
