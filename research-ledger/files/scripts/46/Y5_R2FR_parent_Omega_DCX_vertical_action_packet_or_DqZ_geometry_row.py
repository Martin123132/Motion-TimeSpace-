from __future__ import annotations

import csv
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1784"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1784_0_1783_handoff",
        "source_key": "1783_handoff_doc",
        "source_path": ROOT / "1783-Y5-R2FR-constraint-first-residual-exclusion-or-DqZ-component-proof.md",
        "needles": ["DEC1783_3_best_next", "NEXT1783_0_primary", "DZE1783_0_geometry"],
    },
    {
        "source_id": "SRC1784_1_1783_validation",
        "source_key": "1783_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1783_VALIDATION.csv",
        "needles": ["VAL1783_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1784_2_1783_gate",
        "source_key": "1783_constraint_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1783_CONSTRAINT_FIRST_EXCLUSION_GATE.csv",
        "needles": ["CFE1783_1_momentum_map_generator", "CFE1783_7_verdict"],
    },
    {
        "source_id": "SRC1784_3_1783_routes",
        "source_key": "1783_route_matrix",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1783_RESIDUAL_EXCLUSION_ROUTE_MATRIX.csv",
        "needles": ["REM1783_0_quotient_no_pole", "REM1783_4_finite_DqZ"],
    },
    {
        "source_id": "SRC1784_4_1783_dqz",
        "source_key": "1783_dqz_rows",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1783_DQZ_EOBS_COMPONENT_ROWS.csv",
        "needles": ["DZE1783_0_geometry", "DZE1783_5_total_abs"],
    },
    {
        "source_id": "SRC1784_5_590_dcdagger",
        "source_key": "590_dcdagger_vertical_map",
        "source_path": RESIDUALS / "P8_Y5_R10_590_DCDAGGER_VERTICAL_MAP.csv",
        "needles": ["DVM590_3_precise_map", "DVM590_4_raise_index"],
    },
    {
        "source_id": "SRC1784_6_590_field_action",
        "source_key": "590_field_by_field_action",
        "source_path": RESIDUALS / "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP.csv",
        "needles": ["metric_or_coframe", "boundary_edge"],
    },
    {
        "source_id": "SRC1784_7_590_closure",
        "source_key": "590_mapping_closure_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_590_MAPPING_CLOSURE_GATE.csv",
        "needles": ["MCG590_0_parent_Omega", "MCG590_6_matter_quotient"],
    },
    {
        "source_id": "SRC1784_8_591_omega",
        "source_key": "591_parent_omega_candidate",
        "source_path": RESIDUALS / "P8_Y5_R10_591_PARENT_OMEGA_CANDIDATE.csv",
        "needles": ["OM591_0_covariant_variation_definition", "OM591_4_reduced_Omega"],
    },
    {
        "source_id": "SRC1784_9_591_dc",
        "source_key": "591_dc_operator_formula",
        "source_path": RESIDUALS / "P8_Y5_R10_591_DC_OPERATOR_FORMULA.csv",
        "needles": ["DC591_0_constraint_definition", "DC591_4_boundary_pairing"],
    },
    {
        "source_id": "SRC1784_10_591_dcadjoint",
        "source_key": "591_dcdagger_formula",
        "source_path": RESIDUALS / "P8_Y5_R10_591_DCDAGGER_FORMULA.csv",
        "needles": ["DCA591_1_PJ_adjoint", "DCA591_4_compare_to_Omega_flat"],
    },
    {
        "source_id": "SRC1784_11_591_compare",
        "source_key": "591_omega_dcdagger_comparison",
        "source_path": RESIDUALS / "P8_Y5_R10_591_OMEGA_DCDAGGER_COMPARISON.csv",
        "needles": ["CMP591_0_GR_like_success_condition", "CMP591_5_verdict"],
    },
    {
        "source_id": "SRC1784_12_582_momentum",
        "source_key": "582_momentum_map_closure",
        "source_path": RESIDUALS / "P8_Y5_R10_582_MOMENTUM_MAP_CLOSURE_THEOREM.csv",
        "needles": ["MMT582_0_constraint_generator", "MMT582_5_failure_result"],
    },
    {
        "source_id": "SRC1784_13_582_boundary",
        "source_key": "582_boundary_differentiability",
        "source_path": RESIDUALS / "P8_Y5_R10_582_BOUNDARY_DIFFERENTIABILITY_AUDIT.csv",
        "needles": ["BD582_0_bulk_variation", "BD582_5_verdict"],
    },
    {
        "source_id": "SRC1784_14_582_dirac",
        "source_key": "582_dirac_bracket_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_582_DIRAC_BRACKET_AUDIT.csv",
        "needles": ["DA582_0_rank", "DA582_5_degree_count"],
    },
    {
        "source_id": "SRC1784_15_583_owner",
        "source_key": "583_momentum_map_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_583_PARENT_MOMENTUM_MAP_OWNER_ATTEMPT.csv",
        "needles": ["OMA583_0_zero_momentum_map", "OMA583_5_verdict"],
    },
    {
        "source_id": "SRC1784_16_583_noether",
        "source_key": "583_noether_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_583_NOETHER_MOMENTUM_MAP_CONTRACT.csv",
        "needles": ["NMC583_0_symplectic_potential", "NMC583_5_boundary_zero"],
    },
    {
        "source_id": "SRC1784_17_583_gate",
        "source_key": "583_owner_gate_status",
        "source_path": RESIDUALS / "P8_Y5_R10_583_OWNER_GATE_STATUS.csv",
        "needles": ["OG583_0_parent_Omega", "OG583_5_owner_claim"],
    },
    {
        "source_id": "SRC1784_18_1038_closure",
        "source_key": "1038_omega_dcx_closure",
        "source_path": RESIDUALS / "P8_Y5_R10_1038_OMEGA_DCX_CLOSURE_AUDIT.csv",
        "needles": ["ODC1038_0_parent_Omega", "ODC1038_8_verdict"],
    },
    {
        "source_id": "SRC1784_19_1038_fieldmap",
        "source_key": "1038_vertical_generator_field_map",
        "source_path": RESIDUALS / "P8_Y5_R10_1038_VERTICAL_GENERATOR_FIELD_MAP.csv",
        "needles": ["metric_or_coframe", "boundary_edge_modes"],
    },
    {
        "source_id": "SRC1784_20_1038_claim",
        "source_key": "1038_no_pole_claim_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_1038_NO_POLE_CLAIM_GATE.csv",
        "needles": ["NPG1038_0_exact_no_pole", "MISSING_PARENT_OMEGA"],
    },
    {
        "source_id": "SRC1784_21_1555_first_class",
        "source_key": "1555_first_class_contract",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1555_FIRST_CLASS_CONSTRAINT_CONTRACT.csv",
        "needles": ["FCC1555_0_parent_phase_space", "FCC1555_7_no_GR_import"],
    },
    {
        "source_id": "SRC1784_22_1665_vertical",
        "source_key": "1665_coupling_vertical",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1665_COUPLING_VERTICAL_GENERATOR_AUDIT.csv",
        "needles": ["CVG1665_0_dcdagger_map", "CVG1665_7_verdict"],
    },
    {
        "source_id": "SRC1784_23_670_no_pole",
        "source_key": "670_no_pole_chain",
        "source_path": RESIDUALS / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
        "needles": ["NQ670_6_constraint_generator", "NQ670_8_no_pole_result"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1784_SOURCE_REGISTER.csv",
    "packet_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1784_OMEGA_DCX_VERTICAL_PACKET_GATE.csv",
    "alignment_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1784_OMEGA_DCX_ALIGNMENT_MATRIX.csv",
    "field_action": RESIDUALS / "P8_Y5_PARENT_QLOC_1784_FIELD_ACTION_PACKET.csv",
    "theorem_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1784_VERTICAL_PACKET_THEOREM_ATTEMPT.csv",
    "dqz_geometry_row": RESIDUALS / "P8_Y5_PARENT_QLOC_1784_DQZ_GEOMETRY_ROW_SCHEMA.csv",
    "countermodel": RESIDUALS / "P8_Y5_PARENT_QLOC_1784_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1784_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1784_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1784_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1784_VALIDATION.csv",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        path = source["source_path"]
        exists = path.exists()
        text = read_text(path) if exists else ""
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": exists,
                "needles": ";".join(needles),
                "needles_present": exists and all(needle in text for needle in needles),
                "role": "1784 parent Omega/DC_X/v_X vertical-action packet evidence",
            }
        )
    return rows


def packet_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ODP1784_0_parent_variable_set",
            "clause": "parent variables and boundary variables are declared before quotient",
            "mathematical_form": "Y=(e/g,pi or covariant data, X/Z/phi/R_AB, Gamma/Khat sector, memory/domain/projector, matter/readout, boundary edge data)",
            "source_basis": "FCC1555_0_parent_phase_space;ODC1038_3_vertical_generator_fields;CFE1783_1_momentum_map_generator",
            "current_status": "PARENT_VARIABLE_SET_INCOMPLETE",
            "blocking_issue": "metric/coframe candidates exist, but MTS extra, matter/readout, projector, and boundary variables are not in one parent field list",
            "exit_condition": "one parent field list with domain, boundary, matter/readout, and residual variables plus allowed gauge degeneracies",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ODP1784_1_theta_omega",
            "clause": "parent symplectic potential and two-form are explicit",
            "mathematical_form": "delta L_parent=E_A delta Y^A+d theta_Y(delta Y), Omega_Y(delta1,delta2)=int_Sigma delta1 theta_Y(delta2)-delta2 theta_Y(delta1)",
            "source_basis": "OM591_0_covariant_variation_definition;NMC583_0_symplectic_potential;ODC1038_0_parent_Omega",
            "current_status": "MISSING_PARENT_OMEGA",
            "blocking_issue": "DCdagger remains an undefined covector up to arbitrary pairing",
            "exit_condition": "theta_Y and Omega_Y for all parent and boundary fields, with reference conditions",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ODP1784_2_DCX_operator",
            "clause": "constraint/source operator C_X and linearization D C_X are parent-owned",
            "mathematical_form": "C_X^nu=-nabla_mu P^{mu nu}[Y]+J_eff^nu[Y], with D C_X[delta Y] and convention-fixed density/connection terms",
            "source_basis": "DC591_0_constraint_definition;DC591_1_linearization_tensor_convention;ODC1038_1_DCX_operator",
            "current_status": "MISSING_DCX_OPERATOR",
            "blocking_issue": "P and J_eff are not derived from one parent variational current",
            "exit_condition": "P,J_eff, density convention, operator domain, and source/current owner are explicit",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ODP1784_3_DCDagger_Omega_flat",
            "clause": "DCdagger is mapped to the actual vertical generator by Omega",
            "mathematical_form": "(D C_X)^dagger epsilon = Omega_Y^flat(v_epsilon), and v_epsilon=Omega_Y^{-1}[(D C_X)^dagger epsilon] only on reduced nondegenerate phase space",
            "source_basis": "DVM590_3_precise_map;DVM590_4_raise_index;DCA591_4_compare_to_Omega_flat",
            "current_status": "FORMAL_MAP_SHAPE_EXISTS_NOT_EXECUTABLE",
            "blocking_issue": "the covector/vector conversion is not computable without Omega_Y and reduced inverse",
            "exit_condition": "Omega-flat equality checked field-by-field and reduced Omega inverse declared",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ODP1784_4_field_action",
            "clause": "vertical generator acts on every parent, matter/readout, and boundary field",
            "mathematical_form": "v_X[Y^A] specified for metric/coframe, momenta, Gamma/Khat/q_loc, domain/memory/projector, matter/readout/constants, and boundary modes",
            "source_basis": "P8_Y5_R10_590_FIELD_BY_FIELD_VERTICAL_ACTION_MAP;P8_Y5_R10_1038_VERTICAL_GENERATOR_FIELD_MAP;CVG1665_2_field_action",
            "current_status": "FIELD_MAP_INCOMPLETE",
            "blocking_issue": "metric/coframe Lie derivative candidate is not enough; extra, readout, and boundary fields are unmapped",
            "exit_condition": "field-by-field vertical action and no-marker/no-readout leakage certificate",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ODP1784_5_boundary_QX",
            "clause": "generator is differentiable and local boundary charge is zero/proper/exact",
            "mathematical_form": "delta Q_X cancels B_DC[X,delta Y] and Q_X=0/proper/exact with K_boundary=0 on compact local branch",
            "source_basis": "BD582_0_bulk_variation;BD582_5_verdict;NMC583_5_boundary_zero;ODC1038_4_boundary_differentiability",
            "current_status": "MISSING_BOUNDARY_CHARGE_ZERO",
            "blocking_issue": "edge charge can carry the local source/fifth-force residual",
            "exit_condition": "boundary primitive, differentiable Q_X, projector orthogonality, and zero cocycle",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ODP1784_6_bracket_degree",
            "clause": "constraint algebra closes and removes the residual pair",
            "mathematical_form": "{G[epsilon],G[eta]}=G[[epsilon,eta]]+K_boundary and K_boundary=0; primary+secondary first-class pair removes X",
            "source_basis": "MMT582_2_equivariance;DA582_4_bracket_closure;DA582_5_degree_count;ODC1038_5_bracket_closure;ODC1038_6_degree_count",
            "current_status": "MISSING_BRACKET_AND_DEGREE_COUNT",
            "blocking_issue": "zero Hessian may be under-specified dynamics, second-class remnant, or edge-charged mode",
            "exit_condition": "bracket closure, no central edge cocycle, rank count, no stabilizer",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ODP1784_7_matter_readout",
            "clause": "matter/readout/constants are quotient-blind to the vertical representative",
            "mathematical_form": "S_matter=Sbar[q(Phi),psi,theta], v_X[theta_A]=0, readouts apply after reduction",
            "source_basis": "ODC1038_7_matter_readout;MCG590_6_matter_quotient;NMC583_1_vertical_generator",
            "current_status": "MISSING_MATTER_QUOTIENT",
            "blocking_issue": "source/test marker, hidden frame, or readout map can reintroduce Dq_Z and qbar_XT",
            "exit_condition": "matter descent, no-marker theorem, and readout functor certificate",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "ODP1784_8_verdict",
            "clause": "parent Omega/DC_X/v_X vertical-action packet is signed",
            "mathematical_form": "ODP1784_0 through ODP1784_7 pass in one parent branch",
            "source_basis": "590/591/582/583/1038/1555/1665/1783/670",
            "current_status": "PARENT_OMEGA_DCX_VERTICAL_PACKET_NOT_SIGNED",
            "blocking_issue": "packet remains formal rather than a parent-owned generator for MTS local residuals",
            "exit_condition": "one parent Lagrangian/theta/Omega plus DC_X, v_X, Q_X, bracket, degree, and matter/readout certificates",
            "parent_signed": False,
            "theorem_closed_for_claim": False,
            "score_ready": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def alignment_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "align_id": "ALN1784_0_DCadjoint_covector",
            "object": "(D C_X)^dagger epsilon",
            "left_status": "FORMAL_ADJOINT_DEFINED",
            "right_target": "field-space covector",
            "equation": "<epsilon,D C_X[delta Y]> = <(D C_X)^dagger epsilon,delta Y> + B_DC",
            "current_result": "FORMAL_ONLY_BOUNDARY_OPEN",
            "source_basis": "DCA591_0_formal_pairing;DCA591_3_boundary_adjoint",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "align_id": "ALN1784_1_Omega_flat",
            "object": "Omega_Y^flat(v_X)",
            "left_status": "MISSING_PARENT_OMEGA",
            "right_target": "same field-space covector",
            "equation": "Omega_Y(delta Y,v_X)=delta G_X[delta Y]",
            "current_result": "NOT_COMPARABLE_WITHOUT_OMEGA_AND_DCX",
            "source_basis": "DVM590_2_momentum_map_identity;ODC1038_2_Omega_flat_map",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "align_id": "ALN1784_2_raise_to_vector",
            "object": "v_X",
            "left_status": "NOT_COMPUTABLE",
            "right_target": "actual vertical generator",
            "equation": "v_X=Omega_Y^{-1}[(D C_X)^dagger epsilon] on reduced nondegenerate phase space",
            "current_result": "REDUCED_OMEGA_INVERSE_MISSING",
            "source_basis": "DVM590_4_raise_index;OM591_4_reduced_Omega",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "align_id": "ALN1784_3_PJ_owner",
            "object": "P^{mu nu},J_eff^nu",
            "left_status": "OPERATOR_SHAPE_DERIVED",
            "right_target": "one parent Noether/momentum-map current",
            "equation": "j_X=theta_Y(v_X)-mu_X = X_nu J_eff^nu + nabla_mu X_nu P^{mu nu}+dB",
            "current_result": "P_AND_J_OWNER_NOT_DERIVED",
            "source_basis": "CMP591_1_current_MTS_P_owner;CMP591_2_current_MTS_J_owner;OMA583_1_noether_current_owner",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "align_id": "ALN1784_4_boundary",
            "object": "B_DC and Q_X",
            "left_status": "BOUNDARY_TERM_EXPLICIT",
            "right_target": "differentiable zero/proper generator",
            "equation": "B_DC + delta Q_X=0 and Q_X=0/proper/exact locally",
            "current_result": "BOUNDARY_NOT_SILENCED",
            "source_basis": "DC591_4_boundary_pairing;BD582_0_bulk_variation;BD582_5_verdict",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "align_id": "ALN1784_5_verdict",
            "object": "Omega/DCdagger alignment",
            "left_status": "FORMULA_PROGRESS",
            "right_target": "parent-owned vertical generator certificate",
            "equation": "ALN1784_0 through ALN1784_4 close together",
            "current_result": "FORMAL_MAP_NOT_PARENT_CERTIFICATE",
            "source_basis": "CMP591_5_verdict;ODC1038_8_verdict",
            "valid_for_claim": False,
        },
    ]


def field_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "field_id": "FAP1784_0_metric_coframe",
            "field_block": "metric_or_coframe",
            "candidate_action": "v_X[g]=L_epsilon g or v_X[e]=L_epsilon e plus local Lorentz compensation",
            "current_status": "STANDARD_CANDIDATE_NOT_PARENT_DECLARED",
            "missing_input": "observed coframe/metric owner and parent symplectic potential",
            "leak_if_missing": "Dq_Z[e_obs,g_obs] geometry row remains live",
            "source_basis": "590 field map metric_or_coframe;1038 field map metric_or_coframe",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "field_id": "FAP1784_1_momenta_boundary_charge",
            "field_block": "canonical_momenta_or_boundary_charge",
            "candidate_action": "v_X[pi]=L_epsilon pi plus density and boundary improvements",
            "current_status": "NOT_WRITTEN_FOR_MTS",
            "missing_input": "canonical variables or covariant phase-space charge split",
            "leak_if_missing": "Q_X or boundary symplectic residual can carry source charge",
            "source_basis": "590 field map canonical_momenta_or_boundary_charge;1038 field map canonical_momenta_or_boundary_charge",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "field_id": "FAP1784_2_Gamma_Khat_qloc",
            "field_block": "Gamma_Khat_qloc_sector",
            "candidate_action": "v_X[T_GK]=L_epsilon T_GK if T_GK is parent stress",
            "current_status": "CONDITIONAL_NOT_INTEGRATED_WITH_DCX",
            "missing_input": "parent S_GK, Helmholtz/integrability, and actual DC_X owner",
            "leak_if_missing": "q_loc and Khat/Gamma residual cannot be declared q-vertical",
            "source_basis": "590 field map Gamma_Khat_qloc_sector;1038 field map Gamma_Khat_qloc_sector",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "field_id": "FAP1784_3_domain_memory_projector",
            "field_block": "domain_memory_projector_fields",
            "candidate_action": "v_X[Phi^A]=L_epsilon Phi^A or quotient-vertical representative shift",
            "current_status": "UNMAPPED",
            "missing_input": "transformation law for chi_D, Q_coh, memory, Pi_M/projector, and boundary variables",
            "leak_if_missing": "source/projector terms can reopen local GR residuals",
            "source_basis": "590 field map domain_memory_projector_fields;1038 field map domain_memory_projector_fields",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "field_id": "FAP1784_4_matter_readout_constants",
            "field_block": "matter_readout_constants",
            "candidate_action": "v_X[psi]=0 and v_X[theta_A]=0 only after matter quotient descent",
            "current_status": "NOT_DERIVED",
            "missing_input": "matter action descent, no-marker theorem, no hidden source/readout frame",
            "leak_if_missing": "qbar_XT, WEP, clock, and EM marker rows remain live",
            "source_basis": "590 field map matter_readout;1038 field map matter_readout_constants",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "field_id": "FAP1784_5_boundary_edge_modes",
            "field_block": "boundary_edge_modes",
            "candidate_action": "proper compact transformation or exact boundary representative shift",
            "current_status": "NOT_DERIVED",
            "missing_input": "boundary differentiability, Q_X, cocycle, and projector calculation",
            "leak_if_missing": "edge hair and source mass projection residuals remain live",
            "source_basis": "590 field map boundary_edge;1038 field map boundary_edge_modes",
            "valid_for_claim": False,
        },
    ]


def theorem_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OVT1784_0_DCadjoint_map",
            "claim": "DCdagger is the Omega-flat covector of the vertical generator",
            "mathematical_form": "if delta G_X[epsilon]=<epsilon,D C_X[delta Y]>+delta Q_X=Omega_Y(delta Y,v_epsilon), then (D C_X)^dagger epsilon=Omega_Y^flat(v_epsilon)",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "parent theta/Omega, D C_X, boundary differentiability, and v_X field action",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OVT1784_1_vector_warning",
            "claim": "DCdagger is not the vertical generator until Omega is inverted",
            "mathematical_form": "v_epsilon=Omega_Y^{-1}[(D C_X)^dagger epsilon] only after reduced nondegenerate Omega is built",
            "proof_status": "EXACT_MAP_GUARD",
            "missing_for_current_claim": "reduced Omega inverse, no-stabilizer theorem, and boundary domain",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OVT1784_2_no_pole_packet",
            "claim": "Omega/DC_X/v_X packet can promote constraint-first no-pole exclusion",
            "mathematical_form": "ODP1784_0..7 plus first-class bracket and degree count imply X is representative data and Dq_X/K_X/qbar/Qbar rows vanish",
            "proof_status": "EXACT_CONDITIONAL_THEOREM",
            "missing_for_current_claim": "ODP1784 packet not signed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "OVT1784_3_current_verdict",
            "claim": "current MTS supplies parent Omega/DC_X/v_X packet",
            "mathematical_form": "ODP1784_0 through ODP1784_7 pass and ALN1784_5 closes",
            "proof_status": "FAIL_CURRENT_PARENT_PROOF",
            "missing_for_current_claim": "parent Lagrangian/theta, DC_X owner, field action, boundary Q_X, bracket, degree count, matter descent",
            "valid_for_claim": False,
        },
    ]


def dqz_geometry_row_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZG1784_0_eobs_metric",
            "component": "Dq_Z[e_obs,g_obs]",
            "why_needed": "if Omega/DC_X/v_X packet fails, Z is not a proved representative direction",
            "finite_formula": "epsilon_Z_geom := ||D_Z e_obs|| + ||D_Z g_obs||",
            "required_inputs": "Z basis;coframe/metric norm;arena projection;source path;normalizer",
            "current_value": "MISSING_NUMERIC_OR_THEOREM_ZERO",
            "units": "coframe_metric_component_norm_MISSING",
            "source_anchor": "DZE1783_0_geometry;DQM1674_0_coframe_metric",
            "current_status": "RETAINED_NONCLAIM_GEOMETRY_ROW",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZG1784_1_pairing_norm",
            "component": "Omega_to_coframe_norm_bridge",
            "why_needed": "DCdagger/Omega norms must be translated into observable coframe/metric leakage before scoring",
            "finite_formula": "||D_Z e_obs|| <= N_Omega_to_e ||Omega_flat(v_Z)|| + frame_shadow_term",
            "required_inputs": "Omega norm;coframe norm;shadow-frame coefficient;source path",
            "current_value": "MISSING_NORM_BRIDGE",
            "units": "dimensionless_or_declared_operator_norm_MISSING",
            "source_anchor": "OM591_4_reduced_Omega;DCA591_4_compare_to_Omega_flat",
            "current_status": "RETAINED_NONCLAIM_NORM_BRIDGE",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZG1784_2_boundary_edge_projection",
            "component": "Q_X_to_mass_source_projection",
            "why_needed": "boundary charge can mimic a local source even if bulk Dq_Z geometry is small",
            "finite_formula": "epsilon_QX_mass := ||Pi_M^H Q_X|| + ||K_boundary||",
            "required_inputs": "Q_X;K_boundary;Pi_M^H projection;source path;units",
            "current_value": "MISSING_BOUNDARY_CHARGE_ZERO_OR_VALUE",
            "units": "mass_charge_or_dimensionless_projection_MISSING",
            "source_anchor": "BD582_1_charge_value;BD582_2_central_term;ZE670_2_Qbar_XH",
            "current_status": "RETAINED_NONCLAIM_EDGE_ROW",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DZG1784_3_total_abs",
            "component": "epsilon_DqZ_geometry_packet_abs",
            "why_needed": "no-cancellation envelope if parent packet does not close",
            "finite_formula": "abs(DZG1784_0)+abs(DZG1784_1)+abs(DZG1784_2)",
            "required_inputs": "component values;common normalizer;source paths;no-cancellation flag",
            "current_value": "MISSING_COMPONENT_VALUES_AND_COMMON_NORM",
            "units": "common_dimensionless_or_declared_norm_MISSING",
            "source_anchor": "DZE1783_5_total_abs",
            "current_status": "RETAINED_NONCLAIM_ENVELOPE",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1784_0_arbitrary_pairing",
            "countermodel": "choose a field-space pairing where DCdagger looks small without owning parent Omega",
            "survives_current_constraints": True,
            "why_survives": "Omega_Y is missing, so DCdagger is pairing-dependent bookkeeping",
            "what_kills_it": "parent theta/Omega and reduced norm bridge",
        },
        {
            "branch_id": "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428",
            "countermodel_id": "CM1784_1_metric_only_generator",
            "countermodel": "v_X is specified on metric/coframe only while memory/projector/readout/boundary fields carry the charge",
            "survives_current_constraints": True,
            "why_survives": "field map is incomplete outside metric/coframe block",
            "what_kills_it": "field-by-field vertical action on all parent and boundary variables",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1784_2_boundary_generator",
            "countermodel": "bulk constraint is differentiable only after adding a nonzero boundary charge Q_X",
            "survives_current_constraints": True,
            "why_survives": "Q_X=0/proper/exact and K_boundary=0 are not derived",
            "what_kills_it": "boundary differentiability plus zero/proper charge and no cocycle",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1784_3_second_class_remnant",
            "countermodel": "rank-zero or constraint-looking sector is second-class or under-specified rather than gauge",
            "survives_current_constraints": True,
            "why_survives": "bracket closure and degree count are not computed",
            "what_kills_it": "Dirac bracket closure, rank, and reduced nondegeneracy proof",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1784_4_matter_marker_leak",
            "countermodel": "matter constants/readout markers transform under v_X even if bulk geometry is quotient-like",
            "survives_current_constraints": True,
            "why_survives": "matter quotient and no-marker theorem remain missing",
            "what_kills_it": "matter descent, no-marker theorem, and readout functor certificate",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1784_0_packet",
            "claim": "parent Omega/DC_X/v_X packet is signed",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "ODP1784_8 remains PARENT_OMEGA_DCX_VERTICAL_PACKET_NOT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1784_1_DCadjoint_generator",
            "claim": "DCdagger has been mapped to actual vertical generator",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "Omega inverse, reduced nondegeneracy, and field action are missing",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1784_2_no_pole",
            "claim": "no-pole/local residual exclusion follows",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "boundary Q_X, bracket closure, degree count, and matter/readout descent are unsigned",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1784_3_local_gr",
            "claim": "local GR/Newton/PPN/R10 branch follows",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "Dq_Z geometry and edge/source rows remain nonclaim fallbacks",
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1784_0_exact_result",
            "decision": "DCDAGGER_TO_VERTICAL_GENERATOR_MAP_IS_EXACT_CONDITIONAL",
            "reason": "DCdagger equals Omega-flat(v_X) only when delta G_X is the same functional as the parent symplectic pairing",
            "next_action": "keep formula as contract, not generator proof",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1784_1_current_status",
            "decision": "PARENT_OMEGA_DCX_VERTICAL_PACKET_NOT_SIGNED",
            "reason": "theta/Omega, DC_X owner, field action, boundary charge, bracket closure, degree count, and matter/readout descent are missing",
            "next_action": "do not claim no-pole or local-GR recovery",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1784_2_fallback",
            "decision": "DQZ_GEOMETRY_ROW_STAGED_NONCLAIM",
            "reason": "if the packet fails, the first honest observable row is finite Dq_Z[e_obs,g_obs] plus norm/edge projections",
            "next_action": "fill no geometry component without units, norm, arena projection, and source path",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1784_3_best_next",
            "decision": "PARENT_LAGRANGIAN_THETA_VX_MINIMAL_FILL_IS_NEXT",
            "reason": "the highest leverage missing object is theta_Y/Omega_Y from one parent Lagrangian plus v_X on all fields",
            "next_action": "build 1785 parent Lagrangian/theta/v_X minimal-fill gate or demote to Dq_Z geometry source acquisition",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1784_0_primary",
            "next_target": "1785-Y5-R2FR-parent-Lagrangian-theta-vX-minimal-fill-or-DqZ-geometry-source-row.md",
            "script": "scripts/Y5_R2FR_parent_Lagrangian_theta_vX_minimal_fill_or_DqZ_geometry_source_row.py",
            "objective": "try to fill a minimal parent Lagrangian/theta_Y/v_X packet for the vertical generator; if not, start source acquisition for finite Dq_Z geometry row",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1784_1_parallel",
            "next_target": "1785b-Y5-R2FR-boundary-QX-zero-proper-cocycle-or-edge-row.md",
            "script": "scripts/Y5_R2FR_boundary_QX_zero_proper_cocycle_or_edge_row.py",
            "objective": "attack boundary differentiability, Q_X zero/proper status, and K_boundary cocycle after the vertical packet is sharpened",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1784_2_later",
            "next_target": "1786-Y5-R2FR-matter-readout-no-marker-descent-or-qbarXT-row.md",
            "script": "scripts/Y5_R2FR_matter_readout_no_marker_descent_or_qbarXT_row.py",
            "objective": "attack matter constants/readout leakage after parent v_X field action is less ambiguous",
            "selection_status": "later",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "packet_gate": packet_gate_rows(),
        "alignment_matrix": alignment_matrix_rows(),
        "field_action": field_action_rows(),
        "theorem_attempt": theorem_attempt_rows(),
        "dqz_geometry_row": dqz_geometry_row_rows(),
        "countermodel": countermodel_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        shutil.copy2(path, MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(path, QUARANTINE / filename)
        shutil.copy2(path, RAB_QUEUE / f"JR1784_{key.upper()}.csv")


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return all(boolish(row["exists"]) for row in rows), all(boolish(row["needles_present"]) for row in rows)


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for flag in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "accepted_for_scoring",
                "theorem_closed_for_claim",
                "parent_signed",
                "valid_prediction_row",
            ):
                if flag in row and boolish(row[flag]):
                    return False
    return True


def missing_rows_not_ready(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            text = " ".join(str(value) for value in row.values()).upper()
            if "MISSING" in text:
                for flag in (
                    "valid_for_claim",
                    "claim_allowed",
                    "score_ready",
                    "accepted_for_scoring",
                    "theorem_closed_for_claim",
                    "valid_prediction_row",
                ):
                    if boolish(row.get(flag, False)):
                        return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        filename = path.name
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1784_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add("1784-Y5-R2FR-parent-Omega-DCX-vertical-action-packet-or-DqZ-geometry-row.md")
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1784_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1784_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1784_2_packet_gate_complete",
            any(row["gate_id"] == "ODP1784_8_verdict" for row in rows_map["packet_gate"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["packet_gate"]),
            "Omega/DC_X/v_X packet gate is complete and nonclaim",
        ),
        (
            "VAL1784_3_alignment_matrix_complete",
            any(row["align_id"] == "ALN1784_5_verdict" for row in rows_map["alignment_matrix"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["alignment_matrix"]),
            "Omega/DCdagger alignment matrix is complete and nonclaim",
        ),
        (
            "VAL1784_4_field_action_nonclaim",
            all(not boolish(row["valid_for_claim"]) for row in rows_map["field_action"]),
            "field action packet remains nonclaim",
        ),
        (
            "VAL1784_5_conditional_theorem_written",
            any(row["theorem_id"] == "OVT1784_0_DCadjoint_map" and row["proof_status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["theorem_attempt"])
            and any(row["theorem_id"] == "OVT1784_1_vector_warning" and row["proof_status"] == "EXACT_MAP_GUARD" for row in rows_map["theorem_attempt"]),
            "DCdagger/Omega-flat theorem and vector warning are written",
        ),
        (
            "VAL1784_6_current_proof_not_promoted",
            any(row["theorem_id"] == "OVT1784_3_current_verdict" and row["proof_status"] == "FAIL_CURRENT_PARENT_PROOF" for row in rows_map["theorem_attempt"]),
            "current Omega/DC_X/v_X proof remains unpromoted",
        ),
        (
            "VAL1784_7_dqz_geometry_rows_nonclaim",
            all(
                not boolish(row["valid_for_claim"])
                and not boolish(row["score_ready"])
                and not boolish(row["valid_prediction_row"])
                for row in rows_map["dqz_geometry_row"]
            ),
            "Dq_Z geometry fallback rows remain nonclaim and not score-ready",
        ),
        (
            "VAL1784_8_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel"]),
            "countermodels remain live until theorem or bound rows close them",
        ),
        (
            "VAL1784_9_claim_gates_blocked",
            all(not boolish(row["valid_for_claim"]) and row["status"] in {"BLOCKED", "REFUSED"} for row in rows_map["claim_gate"]),
            "claim gates are blocked or refused",
        ),
        ("VAL1784_10_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1784_11_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1784_12_decision_next",
            any(row["decision_id"] == "DEC1784_3_best_next" and "PARENT_LAGRANGIAN_THETA" in row["decision"] for row in rows_map["decision"]),
            "decision selects parent Lagrangian/theta/v_X minimal fill next",
        ),
        (
            "VAL1784_13_next_selected",
            any(row["route_id"] == "NEXT1784_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1784_14_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1784 CSVs parse"),
        ("VAL1784_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1784_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1784_17_formalization_untouched", formalization_untouched(), "no 1784 outputs found under formalization-workbench"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1784_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1784 parent Omega/DC_X/v_X vertical-action packet or Dq_Z geometry row checkpoint",
        }
    )
    return rows


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(str(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1784 - Y5/R2FR Parent Omega-DCX Vertical-Action Packet or DqZ Geometry Row",
            "",
            "## Verdict",
            "",
            "1784 locks down the exact status of the `DCdagger` idea. The clean statement is true but conditional: `(D C_X)^dagger epsilon` is the `Omega`-flat covector of the vertical generator, not the vertical generator itself. To get the actual vector, the theory must own `Omega_Y` and its reduced inverse.",
            "",
            "Current MTS still does not supply the parent `theta_Y/Omega_Y`, the parent-owned `D C_X`, the field-by-field `v_X`, the differentiable/zero boundary charge, bracket closure, degree count, or matter/readout descent. So the no-pole/constraint-first route remains a contract, not a claim. The fallback is explicit finite `Dq_Z[e_obs,g_obs]` geometry rows.",
            "",
            "**Claim ceiling:** no parent `Omega/DC_X/v_X` packet claim, no `DCdagger` actual-generator claim, no no-pole/local-GR/Newton/PPN/R10 pass, no GitHub action, and no `formalization-workbench` edit is allowed from 1784.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Omega-DCX Vertical Packet Gate",
            markdown_table(rows_map["packet_gate"], ["gate_id", "clause", "mathematical_form", "current_status", "blocking_issue", "exit_condition", "valid_for_claim"]),
            "",
            "## Omega-DCdagger Alignment Matrix",
            markdown_table(rows_map["alignment_matrix"], ["align_id", "object", "left_status", "right_target", "equation", "current_result", "valid_for_claim"]),
            "",
            "## Field-Action Packet",
            markdown_table(rows_map["field_action"], ["field_id", "field_block", "candidate_action", "current_status", "missing_input", "leak_if_missing", "valid_for_claim"]),
            "",
            "## Vertical Packet Theorem Attempt",
            markdown_table(rows_map["theorem_attempt"], ["theorem_id", "claim", "mathematical_form", "proof_status", "missing_for_current_claim", "valid_for_claim"]),
            "",
            "## DqZ Geometry Row Schema",
            markdown_table(rows_map["dqz_geometry_row"], ["row_id", "component", "why_needed", "finite_formula", "current_value", "current_status", "score_ready", "valid_for_claim"]),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is the right kind of failure. We are no longer saying 'the coupling is missing' in the vague sense. We can now name the missing machine: one parent Lagrangian must produce `theta_Y`, `Omega_Y`, `C_X`, `D C_X`, `v_X`, and `Q_X` consistently. If that machine cannot be built, the local branch becomes finite-residual physics rather than derived GR.",
            "",
        ]
    )


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1784-Y5-R2FR-parent-Omega-DCX-vertical-action-packet-or-DqZ-geometry-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1784 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
