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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1785"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1785_0_1784_handoff",
        "source_key": "1784_handoff_doc",
        "source_path": ROOT / "1784-Y5-R2FR-parent-Omega-DCX-vertical-action-packet-or-DqZ-geometry-row.md",
        "needles": ["ODP1784_8_verdict", "OVT1784_0_DCadjoint_map", "NEXT1784_0_primary"],
    },
    {
        "source_id": "SRC1785_1_1784_validation",
        "source_key": "1784_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1784_VALIDATION.csv",
        "needles": ["VAL1784_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1785_2_1784_packet_gate",
        "source_key": "1784_omega_dcx_vertical_packet_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1784_OMEGA_DCX_VERTICAL_PACKET_GATE.csv",
        "needles": ["ODP1784_1_theta_omega", "ODP1784_8_verdict"],
    },
    {
        "source_id": "SRC1785_3_1784_theorem",
        "source_key": "1784_vertical_packet_theorem_attempt",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1784_VERTICAL_PACKET_THEOREM_ATTEMPT.csv",
        "needles": ["OVT1784_0_DCadjoint_map", "OVT1784_3_current_verdict"],
    },
    {
        "source_id": "SRC1785_4_1784_dqz_geometry",
        "source_key": "1784_dqz_geometry_row_schema",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1784_DQZ_GEOMETRY_ROW_SCHEMA.csv",
        "needles": ["DZG1784_0_eobs_metric", "DZG1784_3_total_abs"],
    },
    {
        "source_id": "SRC1785_5_592_noether_formula",
        "source_key": "592_noether_pj_origin_formula",
        "source_path": RESIDUALS / "P8_Y5_R10_592_NOETHER_PJ_ORIGIN_FORMULA.csv",
        "needles": [
            "NPJ592_0_parent_variation",
            "NPJ592_1_vertical_quasi_symmetry",
            "NPJ592_2_Noether_current",
            "NPJ592_3_PJ_split",
            "NPJ592_4_constraint_density",
            "NPJ592_5_momentum_map_condition",
        ],
    },
    {
        "source_id": "SRC1785_6_592_parent_origin",
        "source_key": "592_pj_parent_origin_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_592_PJ_PARENT_ORIGIN_ATTEMPT.csv",
        "needles": ["PJA592_0_GR_EH_template", "PJA592_1_affine_Vdef_block", "PJA592_5_current_verdict"],
    },
    {
        "source_id": "SRC1785_7_592_improvement",
        "source_key": "592_improvement_ambiguity_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_592_IMPROVEMENT_AMBIGUITY_GATE.csv",
        "needles": ["IAG592_0_superpotential_improvement", "IAG592_4_matter_improper_charge"],
    },
    {
        "source_id": "SRC1785_8_592_edge_plan",
        "source_key": "592_edge_coefficient_source_plan",
        "source_path": RESIDUALS / "P8_Y5_R10_592_EDGE_COEFFICIENT_SOURCE_PLAN.csv",
        "needles": ["ESP592_0", "ESP592_2"],
    },
    {
        "source_id": "SRC1785_9_593_parent_candidates",
        "source_key": "593_minimal_parent_fill_candidates",
        "source_path": RESIDUALS / "P8_Y5_R10_593_MINIMAL_PARENT_FILL_CANDIDATES.csv",
        "needles": [
            "MPF593_A_diffeomorphism_parent",
            "MPF593_B_strict_quotient_zero",
            "MPF593_C_affine_topological_block",
            "MPF593_D_EH_plus_quotient_extra",
        ],
    },
    {
        "source_id": "SRC1785_10_593_theta_mu_vx",
        "source_key": "593_theta_mu_vx_filled_forms",
        "source_path": RESIDUALS / "P8_Y5_R10_593_THETA_MU_VX_FILLED_FORMS.csv",
        "needles": ["TMV593_0_EH_theta", "TMV593_1_extra_theta", "TMV593_2_matter_theta", "TMV593_3_muX"],
    },
    {
        "source_id": "SRC1785_11_593_extraction",
        "source_key": "593_pj_extraction_test",
        "source_path": RESIDUALS / "P8_Y5_R10_593_PJ_EXTRACTION_TEST.csv",
        "needles": [
            "PJE593_0_diffeo_extracts_PJ",
            "PJE593_1_quotient_zero_extracts_zero",
            "PJE593_2_affine_block_not_origin",
            "PJE593_3_hybrid_needs_split",
        ],
    },
    {
        "source_id": "SRC1785_12_593_edge_inputs",
        "source_key": "593_edge_coefficient_input_rows",
        "source_path": RESIDUALS / "P8_Y5_R10_593_EDGE_COEFFICIENT_INPUT_ROWS.csv",
        "needles": ["ECI593_0", "ECI593_2"],
    },
    {
        "source_id": "SRC1785_13_728_omega",
        "source_key": "728_parent_omega_candidate",
        "source_path": RESIDUALS / "P8_Y5_R10_728_PARENT_OMEGA_CANDIDATE.csv",
        "needles": ["OM728_0_covariant_variation_definition", "OM728_4_reduced_Omega"],
    },
    {
        "source_id": "SRC1785_14_728_dcdagger",
        "source_key": "728_dcdagger_formula",
        "source_path": RESIDUALS / "P8_Y5_R10_728_DCDAGGER_FORMULA.csv",
        "needles": ["DCA728_0_formal_pairing", "DCA728_4_compare_to_Omega_flat"],
    },
    {
        "source_id": "SRC1785_15_728_blocker",
        "source_key": "728_parent_ownership_blocker",
        "source_path": RESIDUALS / "P8_Y5_R10_728_PARENT_OWNERSHIP_BLOCKER.csv",
        "needles": ["POB728_0_L_parent", "POB728_1_theta_mu_vX", "POB728_2_PJ_from_one_current"],
    },
    {
        "source_id": "SRC1785_16_729_noether",
        "source_key": "729_noether_pj_origin_formula",
        "source_path": RESIDUALS / "P8_Y5_R10_729_NOETHER_PJ_ORIGIN_FORMULA.csv",
        "needles": [
            "NPJ729_0_parent_variation",
            "NPJ729_1_vertical_quasi_symmetry",
            "NPJ729_2_Noether_current",
            "NPJ729_3_PJ_split",
            "NPJ729_4_constraint_density",
            "NPJ729_5_symplectic_flat_closure",
            "NPJ729_6_current_verdict",
        ],
    },
    {
        "source_id": "SRC1785_17_729_blocker",
        "source_key": "729_parent_origin_blocker",
        "source_path": RESIDUALS / "P8_Y5_R10_729_PARENT_ORIGIN_BLOCKER.csv",
        "needles": [
            "POB729_0_L_parent",
            "POB729_1_theta_mu_vX",
            "POB729_2_one_current_PJ_split",
            "POB729_3_boundary_representative",
            "POB729_4_matter_projector_silence",
            "POB729_5_edge_coefficients",
        ],
    },
    {
        "source_id": "SRC1785_18_729_origin_attempt",
        "source_key": "729_pj_parent_origin_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_729_PJ_PARENT_ORIGIN_ATTEMPT.csv",
        "needles": [
            "PJA729_0_GR_EH_template",
            "PJA729_1_strict_quotient_zero",
            "PJA729_2_affine_Vdef_block",
            "PJA729_3_GK_stress_Ward_route",
            "PJA729_4_memory_domain_relative_current",
            "PJA729_5_independent_PJ",
            "PJA729_6_current_verdict",
        ],
    },
    {
        "source_id": "SRC1785_19_729_decision",
        "source_key": "729_decision_matrix",
        "source_path": RESIDUALS / "P8_Y5_R10_729_DECISION_MATRIX.csv",
        "needles": ["D729_0_Noether_PJ_contract_current_chain", "D729_2_next_best_route_is_minimal_parent_fill"],
    },
    {
        "source_id": "SRC1785_20_730_decision",
        "source_key": "730_decision_matrix",
        "source_path": RESIDUALS / "P8_Y5_R10_730_DECISION_MATRIX.csv",
        "needles": [
            "D730_0_minimal_parent_fill_written",
            "D730_1_affine_origin_rejected",
            "D730_2_best_routes_are_quotient_or_hybrid",
            "D730_3_fixed_point_is_residual_backup",
            "D730_4_edge_coefficients_still_missing",
        ],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1785_SOURCE_REGISTER.csv",
    "lagrangian_theta_vx_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1785_PARENT_LAGRANGIAN_THETA_VX_GATE.csv",
    "minimal_fill_route_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1785_MINIMAL_FILL_ROUTE_MATRIX.csv",
    "noether_pj_contract_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1785_NOETHER_PJ_CONTRACT_GATE.csv",
    "dqz_geometry_source_row_plan": RESIDUALS / "P8_Y5_PARENT_QLOC_1785_DQZ_GEOMETRY_SOURCE_ROW_PLAN.csv",
    "countermodel_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1785_COUNTERMODEL_LEDGER.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1785_CLAIM_GATE.csv",
    "decision_ledger": RESIDUALS / "P8_Y5_PARENT_QLOC_1785_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1785_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1785_VALIDATION.csv",
}

DOC_PATH = ROOT / "1785-Y5-R2FR-parent-Lagrangian-theta-vX-minimal-fill-or-DqZ-geometry-source-row.md"


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
                "role": "1785 parent Lagrangian/theta/vX minimal-fill and Dq_Z fallback evidence",
            }
        )
    return rows


def lagrangian_theta_vx_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "PLT1785_0_L_parent",
            "clause": "one parent Lagrangian must own the local residual branch",
            "mathematical_form": "L_parent[Y,dY;boundary] -> E_A delta Y^A + d theta_Y(delta Y)",
            "source_basis": "POB728_0_L_parent;POB729_0_L_parent;D730_0_minimal_parent_fill_written",
            "current_status": "MISSING_EXPLICIT_L_PARENT",
            "blocking_issue": "no single signed L_parent currently produces theta_Y, Omega_Y, C_X, D C_X, v_X, Q_X, matter descent, and boundary representative together",
            "exit_condition": "write the parent action with field list, gauge/quotient map, boundary terms, and variation showing all objects in one branch",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "PLT1785_1_theta_Y",
            "clause": "theta_Y must be the actual symplectic potential from variation",
            "mathematical_form": "delta L_parent = E_A delta Y^A + d theta_Y(delta Y)",
            "source_basis": "NPJ592_0_parent_variation;TMV593_0_EH_theta;TMV593_1_extra_theta;OM728_0_covariant_variation_definition",
            "current_status": "THETA_FORMAL_NOT_PARENT_FILLED",
            "blocking_issue": "EH theta template exists, but MTS extra-sector theta and matter/readout theta are not derived from one L_parent",
            "exit_condition": "derive theta_Y component-by-component from L_parent with exact boundary convention",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "PLT1785_2_vX",
            "clause": "vertical generator must be a field-by-field action, not a named covector",
            "mathematical_form": "v_X: Y^A -> delta_X Y^A with v_X in ker(Dq) or controlled quotient-horizontal split",
            "source_basis": "ODP1784_3_vertical_generator;OVT1784_1_vector_warning;POB729_1_theta_mu_vX",
            "current_status": "VX_FIELD_ACTION_NOT_FILLED",
            "blocking_issue": "DCdagger has only reached Omega-flat covector status; the actual vector requires parent Omega inverse plus a field action",
            "exit_condition": "field-by-field v_X on coframe/metric, extra sector, projector, matter/readout, and boundary variables",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "PLT1785_3_mu_X",
            "clause": "quasi-symmetry term must be fixed",
            "mathematical_form": "delta_X L_parent = d mu_X",
            "source_basis": "NPJ592_1_vertical_quasi_symmetry;TMV593_3_muX;NPJ729_1_vertical_quasi_symmetry",
            "current_status": "MU_X_ROUTE_NOT_CHOSEN",
            "blocking_issue": "strict symmetry, boundary quasi-symmetry, and hybrid EH-plus-extra options are still separate routes",
            "exit_condition": "choose strict quotient-zero or hybrid representative and derive mu_X with boundary conventions",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "PLT1785_4_jX_current",
            "clause": "the current must be produced before P/J can be owned",
            "mathematical_form": "j_X = theta_Y(v_X) - mu_X",
            "source_basis": "NPJ592_2_Noether_current;NPJ729_2_Noether_current;PJE593_3_hybrid_needs_split",
            "current_status": "NOETHER_CURRENT_CONTRACT_ONLY",
            "blocking_issue": "the exact formula exists, but theta_Y, v_X, and mu_X are not jointly filled from a signed parent",
            "exit_condition": "compute j_X from the signed parent branch and only then identify P and J pieces",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "PLT1785_5_PJ_split",
            "clause": "P and J must be extracted as coefficients of one current",
            "mathematical_form": "j_X = P_X[epsilon] + J_X[epsilon] + d B_X[epsilon] with no independently inserted P/J",
            "source_basis": "NPJ592_3_PJ_split;POB729_2_one_current_PJ_split;PJA729_5_independent_PJ",
            "current_status": "FORMULA_DERIVED_NOT_FILLED",
            "blocking_issue": "coefficient extraction is a correct contract, but P/J are not yet obtained from one explicit current",
            "exit_condition": "derive P and J by coefficient matching from the same j_X and record residual/improvement ambiguity",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "PLT1785_6_boundary_representative",
            "clause": "boundary and superpotential representative must be fixed",
            "mathematical_form": "j_X -> j_X + d U_X and Q_X fixed by differentiability or quotient descent",
            "source_basis": "IAG592_0_superpotential_improvement;POB729_3_boundary_representative;ODP1784_4_boundary_charge",
            "current_status": "BOUNDARY_REPRESENTATIVE_OPEN",
            "blocking_issue": "improvements can move edge coefficients unless the representative is owned by the parent variational problem",
            "exit_condition": "parent boundary condition selects Q_X and kills or quantifies improvement freedom",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "PLT1785_7_matter_projector_silence",
            "clause": "ordinary matter/readout must be blind to the vertical quotient direction",
            "mathematical_form": "delta_{v_X} S_matter = 0 or controlled finite leakage term sourced by Dq_Z",
            "source_basis": "IAG592_4_matter_improper_charge;POB729_4_matter_projector_silence;ODP1784_7_matter_readout",
            "current_status": "NOT_PROVED",
            "blocking_issue": "matter/projector silence is the hinge between derived local GR and finite residual physics",
            "exit_condition": "prove descent of matter measure/coframe/connection/readout through q or write finite leakage rows",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "PLT1785_8_verdict",
            "clause": "parent Lagrangian/theta/v_X minimal fill is signed",
            "mathematical_form": "PLT1785_0 through PLT1785_7 all pass in one branch",
            "source_basis": "1784 verdict plus 592/593/728/729/730 chain",
            "current_status": "PARENT_LAGRANGIAN_THETA_VX_MINIMAL_FILL_NOT_SIGNED",
            "blocking_issue": "the derivation contract is exact, but the parent fill is still missing the selected branch and boundary/matter certificates",
            "exit_condition": "one signed strict quotient-zero or hybrid branch closes L_parent, theta_Y, v_X, mu_X, j_X, P/J, Q_X, and matter silence",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def minimal_fill_route_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "MRM1785_0_strict_quotient_zero",
            "route": "strict quotient-zero parent",
            "mathematical_strategy": "construct q so v_X is vertical, S_parent descends through q, and j_X has zero ordinary/readout charge",
            "source_basis": "MPF593_B_strict_quotient_zero;PJA729_1_strict_quotient_zero;D730_2_best_routes_are_quotient_or_hybrid",
            "strength": "lowest scrutiny if it closes, because local GR emerges by quotient blindness rather than tuned cancellation",
            "failure_mode": "needs explicit q, Dq, ker(Dq), matter/coframe/connection descent, and boundary silence",
            "current_status": "BEST_ROUTE_CONDITIONAL_NOT_CONSTRUCTED",
            "next_action": "attempt exact q/descent/boundary proof before finite residual rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "MRM1785_1_hybrid_EH_plus_quotient_extra",
            "route": "EH core plus quotient-owned MTS extra sector",
            "mathematical_strategy": "keep Einstein-Hilbert local core and attach an extra sector that is quotient-vertical or boundary-only locally",
            "source_basis": "MPF593_D_EH_plus_quotient_extra;PJE593_3_hybrid_needs_split;PJA729_0_GR_EH_template",
            "strength": "most realistic bridge to GR if pure quotient-zero is too strong",
            "failure_mode": "must prevent double counting, fix boundary representative, and split ADM/extra-sector charges cleanly",
            "current_status": "PROMISING_BUT_UNSIGNED",
            "next_action": "derive split current and prove extra-sector local silence or quantify leakage",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "MRM1785_2_diffeomorphism_parent",
            "route": "standard diffeomorphism Noether parent",
            "mathematical_strategy": "use GR covariant phase-space current as template for theta, constraints, and boundary charge",
            "source_basis": "MPF593_A_diffeomorphism_parent;PJA592_0_GR_EH_template;PJE593_0_diffeo_extracts_PJ",
            "strength": "known mathematical machinery and good local-GR benchmark",
            "failure_mode": "does not by itself prove MTS C_X/P/J are vertical quotient currents rather than ordinary diffeomorphism charges",
            "current_status": "TEMPLATE_ONLY_NOT_MTS_ORIGIN",
            "next_action": "use as EH baseline inside hybrid branch, not as proof of MTS coupling origin",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "MRM1785_3_GK_stress_Ward",
            "route": "GK stress/Ward origin",
            "mathematical_strategy": "try to derive J-like stress response from a Ward identity and then connect it to the local residual projection",
            "source_basis": "PJA729_3_GK_stress_Ward_route;D729_0_Noether_PJ_contract_current_chain",
            "strength": "promising for current/J ownership and conservation accounting",
            "failure_mode": "weak on P/edge coefficients unless S_GK, Helmholtz conditions, and projector map are supplied",
            "current_status": "PARTIAL_ROUTE_FOR_J_NOT_FULL_PJ",
            "next_action": "keep as supporting route after q/hybrid branch choice",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "MRM1785_4_affine_Vdef",
            "route": "affine topological Vdef block",
            "mathematical_strategy": "insert affine/topological block to reproduce P/J-like terms",
            "source_basis": "MPF593_C_affine_topological_block;PJA592_1_affine_Vdef_block;PJE593_2_affine_block_not_origin;D730_1_affine_origin_rejected",
            "strength": "can mimic forms",
            "failure_mode": "independent insertion of P/J is not a parent-origin derivation",
            "current_status": "REJECTED_AS_PARENT_ORIGIN",
            "next_action": "do not promote; use only as countermodel guard",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "MRM1785_5_edge_source_acquisition",
            "route": "finite Dq_Z and edge coefficient acquisition",
            "mathematical_strategy": "if derivation stalls, source K_edge, Qbar_XH, qbar_XT, Dq_Z geometry, and arena projections as finite residual inputs",
            "source_basis": "ESP592_0;ESP592_2;ECI593_0;ECI593_2;DZG1784_0_eobs_metric",
            "strength": "turns failure into testable nonclaim residual rows",
            "failure_mode": "becomes phenomenological unless parent coefficients are later derived",
            "current_status": "FALLBACK_SOURCE_ROUTE_NOT_CLAIM",
            "next_action": "stage source-ready rows only after q/hybrid proof attempt fails",
            "valid_for_claim": False,
        },
    ]


def noether_pj_contract_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "contract_id": "NPJ1785_0_parent_variation",
            "claim": "parent variation produces field equations and symplectic potential",
            "mathematical_form": "delta L_parent = E_A delta Y^A + d theta_Y(delta Y)",
            "proof_status": "EXACT_CONDITIONAL_FORMULA",
            "source_basis": "NPJ592_0_parent_variation;NPJ729_0_parent_variation",
            "missing_for_current_claim": "explicit L_parent and theta_Y for MTS branch",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "NPJ1785_1_vertical_quasi_symmetry",
            "claim": "vertical generator is a parent quasi-symmetry",
            "mathematical_form": "delta_X L_parent = d mu_X",
            "proof_status": "EXACT_CONDITIONAL_FORMULA",
            "source_basis": "NPJ592_1_vertical_quasi_symmetry;NPJ729_1_vertical_quasi_symmetry",
            "missing_for_current_claim": "field-by-field v_X and selected mu_X",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "NPJ1785_2_noether_current",
            "claim": "Noether current follows from theta and quasi-symmetry term",
            "mathematical_form": "j_X = theta_Y(v_X) - mu_X",
            "proof_status": "EXACT_CONDITIONAL_FORMULA",
            "source_basis": "NPJ592_2_Noether_current;NPJ729_2_Noether_current",
            "missing_for_current_claim": "theta_Y(v_X) cannot be evaluated until theta_Y and v_X are parent-filled",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "NPJ1785_3_PJ_split",
            "claim": "P and J are coefficients of one parent current",
            "mathematical_form": "j_X = P_X + J_X + d B_X after fixing representative and integrations by parts",
            "proof_status": "EXACT_CONDITIONAL_CONTRACT",
            "source_basis": "NPJ592_3_PJ_split;NPJ729_3_PJ_split;POB729_2_one_current_PJ_split",
            "missing_for_current_claim": "one computed j_X and fixed boundary representative",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "NPJ1785_4_constraint_density",
            "claim": "constraint density belongs to parent current rather than external closure",
            "mathematical_form": "C_X[epsilon] appears as bulk coefficient of j_X or Hamiltonian generator variation",
            "proof_status": "EXACT_CONDITIONAL_CONTRACT",
            "source_basis": "NPJ592_4_constraint_density;NPJ729_4_constraint_density",
            "missing_for_current_claim": "parent constraint operator and differentiable boundary charge",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "NPJ1785_5_symplectic_flat_closure",
            "claim": "DCdagger becomes a vector only after Omega inverse is owned",
            "mathematical_form": "(D C_X)^dagger epsilon = Omega_Y^flat(v_epsilon), with v_epsilon = Omega_Y^{-1}(D C_X)^dagger epsilon only if inversion is defined",
            "proof_status": "EXACT_MAP_GUARD",
            "source_basis": "OVT1784_0_DCadjoint_map;OVT1784_1_vector_warning;DCA728_4_compare_to_Omega_flat",
            "missing_for_current_claim": "parent Omega_Y inverse or presymplectic reduction certificate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "contract_id": "NPJ1785_6_verdict",
            "claim": "Noether P/J origin is derived for current MTS local branch",
            "mathematical_form": "NPJ1785_0 through NPJ1785_5 plus PLT1785 close in one branch",
            "proof_status": "CONTRACT_EXACT_CURRENT_UNFILLED",
            "source_basis": "592/729 exact formula chain plus 1784 Omega-flat warning",
            "missing_for_current_claim": "signed branch choice, L_parent, theta_Y, v_X, mu_X, Q_X, matter silence, and boundary representative",
            "valid_for_claim": False,
        },
    ]


def dqz_geometry_source_row_plan_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DGS1785_0_geometry_component",
            "component": "epsilon_Z_geom",
            "why_needed": "fallback finite residual if quotient-zero or hybrid local silence does not close",
            "required_formula": "epsilon_Z_geom = norm(Dq_Z[e_obs,g_obs] acting on local observable geometry)",
            "source_basis": "DZG1784_0_eobs_metric;DGS fallback from 1784",
            "current_value": "MISSING_DQZ_GEOMETRY_VALUE",
            "units": "dimensionless or arena-normalized after norm bridge",
            "current_status": "MISSING_PARENT_GEOMETRY_PROJECTION",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DGS1785_1_norm_bridge",
            "component": "Omega_or_coframe_norm_bridge",
            "why_needed": "Dq_Z needs a declared norm before it can bound PPN/R10/clock/orbit leakage",
            "required_formula": "||Dq_Z||_{obs} from parent Omega, coframe metric, or arena covariance norm",
            "source_basis": "OM728_4_reduced_Omega;ODP1784_1_theta_omega",
            "current_value": "MISSING_NORM_BRIDGE",
            "units": "arena dependent",
            "current_status": "MISSING_PARENT_NORM",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DGS1785_2_arena_projection",
            "component": "local arena projection",
            "why_needed": "finite local leakage has to be connected to actual R10, PPN, clock, WEP, or orbital observables",
            "required_formula": "tau_arena * epsilon_Z_geom with source-owned kernel/projection",
            "source_basis": "ESP592_0;ESP592_2;ECI593_0;ECI593_2",
            "current_value": "MISSING_ARENA_PROJECTION",
            "units": "observable dependent",
            "current_status": "MISSING_ARENA_PROJECTION",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DGS1785_3_edge_coefficients",
            "component": "K_edge_Qbar_qbar",
            "why_needed": "edge/current coefficients decide whether residual is zero, bounded, or excluded",
            "required_formula": "alpha_like ~ K_edge * Qbar_XH * qbar_XT * epsilon_Z_geom",
            "source_basis": "ESP592_0;ESP592_2;ECI593_0;ECI593_2;D730_4_edge_coefficients_still_missing",
            "current_value": "MISSING_EDGE_COEFFICIENTS",
            "units": "coefficient dependent",
            "current_status": "MISSING_PARENT_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DGS1785_4_total_abs",
            "component": "total absolute local residual envelope",
            "why_needed": "claim gate requires a numerical residual bound against local tests",
            "required_formula": "|alpha_pred| <= alpha_bound or arena residual <= experimental envelope",
            "source_basis": "DZG1784_3_total_abs;R10/PPN/clock/orbital future source rows",
            "current_value": "MISSING_TOTAL_ABS_RESIDUAL",
            "units": "observable dependent",
            "current_status": "MISSING_PARENT_INPUT",
            "score_ready": False,
            "valid_prediction_row": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1785_0_independent_PJ_insert",
            "countermodel": "P and J are inserted as independent fields or phenomenological terms after the action",
            "survives_current_constraints": True,
            "why_survives": "no signed parent current currently forces P/J to be coefficients of one j_X",
            "what_kills_it": "compute j_X from L_parent and extract P/J uniquely after boundary representative is fixed",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1785_1_diffeo_not_MTS_vertical",
            "countermodel": "the GR diffeomorphism current is mistaken for the MTS vertical quotient current",
            "survives_current_constraints": True,
            "why_survives": "diffeomorphism machinery is a template but does not identify q, ker(Dq), or MTS vertical action",
            "what_kills_it": "construct q and prove v_X is the local vertical generator for the MTS quotient sector",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1785_2_quotient_zero_axiom",
            "countermodel": "strict quotient-zero is asserted as an axiom without pi/matter/readout descent",
            "survives_current_constraints": True,
            "why_survives": "matter measure, coframe, connection, and readout blindness remain unsigned",
            "what_kills_it": "prove S_matter = Sbar[q(Phi),Psi,theta] plus coframe/connection descent and boundary silence",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1785_3_boundary_improvement_leak",
            "countermodel": "superpotential improvement changes the edge coefficient and creates local leakage",
            "survives_current_constraints": True,
            "why_survives": "Q_X and the boundary representative are not fixed by a differentiable variational problem",
            "what_kills_it": "parent boundary conditions fix Q_X or prove improvement terms are quotient-trivial",
        },
        {
            "branch_id": BRANCH_ID,
            "countermodel_id": "CM1785_4_matter_projector_leak",
            "countermodel": "matter/projector sector couples to the vertical direction and produces finite local residuals",
            "survives_current_constraints": True,
            "why_survives": "matter/projector silence is not proven; finite Dq_Z row remains live",
            "what_kills_it": "prove vertical blindness or source finite leakage coefficients and pass local bounds",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1785_0_parent_fill_claim",
            "claim": "MTS has a signed parent Lagrangian/theta/v_X minimal fill",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "MISSING_EXPLICIT_L_PARENT and VX_FIELD_ACTION_NOT_FILLED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1785_1_noether_pj_origin_claim",
            "claim": "P/J are derived from one Noether current",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "NOETHER_CURRENT_CONTRACT_ONLY and BOUNDARY_REPRESENTATIVE_OPEN",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1785_2_local_gr_claim",
            "claim": "local GR/Newton/PPN/R10 pass follows from this checkpoint",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "matter/projector silence and finite Dq_Z rows are not closed",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1785_3_affine_origin_claim",
            "claim": "affine Vdef block is the parent origin of coupling",
            "gate_pass": False,
            "status": "REFUSED",
            "blocker": "affine route can mimic forms but is rejected as parent-origin derivation",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1785_4_finite_residual_score_claim",
            "claim": "Dq_Z finite local residual rows are score-ready",
            "gate_pass": False,
            "status": "BLOCKED",
            "blocker": "MISSING_DQZ_GEOMETRY_VALUE, MISSING_NORM_BRIDGE, MISSING_ARENA_PROJECTION, MISSING_EDGE_COEFFICIENTS",
            "valid_for_claim": False,
        },
    ]


def decision_ledger_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1785_0_exact_contract",
            "decision": "NOETHER_PJ_CONTRACT_IS_EXACT_CONDITIONAL",
            "reason": "delta L, theta, mu_X, j_X, and P/J coefficient extraction are mathematically clean as a contract",
            "next_action": "do not treat contract as proof until L_parent/theta/v_X/mu_X are filled",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1785_1_current_status",
            "decision": "PARENT_LAGRANGIAN_THETA_VX_MINIMAL_FILL_NOT_SIGNED",
            "reason": "the current project state has formulas and candidate routes, not one signed parent branch",
            "next_action": "choose one route and close its boundary/matter clauses",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1785_2_affine_rejected",
            "decision": "AFFINE_VDEF_ROUTE_REJECTED_AS_PARENT_ORIGIN",
            "reason": "affine block would insert the desired pieces rather than derive them from one current",
            "next_action": "retain as countermodel guard only",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1785_3_best_next",
            "decision": "CHOOSE_QUOTIENT_ZERO_OR_HYBRID_AND_CLOSE_BOUNDARY_IS_NEXT",
            "reason": "strict quotient-zero is the cleanest win if derivable; hybrid EH-plus-quotient-extra is the realistic backup; both require boundary and matter/projector silence",
            "next_action": "run 1786 branch-choice gate, then either close q/descent/boundary or stage Dq_Z source rows",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1785_0_primary",
            "next_target": "1786-Y5-R2FR-choose-quotient-zero-or-hybrid-and-close-boundary-or-DqZ-source-row.md",
            "script": "scripts/Y5_R2FR_choose_quotient_zero_or_hybrid_and_close_boundary_or_DqZ_source_row.py",
            "objective": "choose between strict quotient-zero and hybrid EH-plus-quotient-extra, then close boundary/matter descent conditions or move to Dq_Z/edge source acquisition",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1785_1_parallel_fallback",
            "next_target": "1786b-Y5-R2FR-DqZ-geometry-source-row-acquisition.md",
            "script": "scripts/Y5_R2FR_DqZ_geometry_source_row_acquisition.py",
            "objective": "prepare source-ready finite Dq_Z geometry/norm/arena/edge rows without claiming local-GR pass",
            "selection_status": "deferred_until_1786_branch_choice",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1785_2_later",
            "next_target": "1787-Y5-R2FR-matter-projector-descent-silence-or-leakage-bound.md",
            "script": "scripts/Y5_R2FR_matter_projector_descent_silence_or_leakage_bound.py",
            "objective": "prove ordinary matter/readout blindness to the vertical quotient direction or retain finite local leakage",
            "selection_status": "queued_after_branch_choice",
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "lagrangian_theta_vx_gate": lagrangian_theta_vx_gate_rows(),
        "minimal_fill_route_matrix": minimal_fill_route_matrix_rows(),
        "noether_pj_contract_gate": noether_pj_contract_gate_rows(),
        "dqz_geometry_source_row_plan": dqz_geometry_source_row_plan_rows(),
        "countermodel_ledger": countermodel_ledger_rows(),
        "claim_gate": claim_gate_rows(),
        "decision_ledger": decision_ledger_rows(),
        "next_target": next_target_rows(),
    }


def fieldnames_for(rows: list[dict[str, Any]]) -> list[str]:
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    return fieldnames


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = fieldnames_for(rows)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        shutil.copy2(path, MICROSCOPE_RESIDUALS / path.name)
        shutil.copy2(path, QUARANTINE / path.name)
        shutil.copy2(path, RAB_QUEUE / f"JR1785_{key.upper()}.csv")


def boolish(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    return str(value).strip().lower() in {"1", "true", "yes", "y", "pass", "passed"}


def sources_ok(rows_map: dict[str, list[dict[str, Any]]]) -> tuple[bool, bool]:
    rows = rows_map["source_register"]
    return (
        all(boolish(row["exists"]) for row in rows),
        all(boolish(row["needles_present"]) for row in rows),
    )


def parse_csv(path: Path) -> bool:
    try:
        with path.open(newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except csv.Error:
        return False


def generated_csvs() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for rows in rows_map.values():
        for row in rows:
            for flag in (
                "valid_for_claim",
                "claim_allowed",
                "score_ready",
                "accepted_for_scoring",
                "theorem_closed_for_claim",
                "parent_signed",
                "valid_prediction_row",
                "gate_pass",
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
                    "gate_pass",
                ):
                    if boolish(row.get(flag, False)):
                        return False
    return True


def branch_copies_exist() -> bool:
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        if not (MICROSCOPE_RESIDUALS / path.name).exists():
            return False
        if not (QUARANTINE / path.name).exists():
            return False
        if not (RAB_QUEUE / f"JR1785_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    generated_names = {path.name for path in OUTPUTS.values()}
    generated_names.add(DOC_PATH.name)
    return not any(path.name in generated_names for path in FORMALIZATION.rglob("*"))


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, str]]:
    exists_ok, needles_ok = sources_ok(rows_map)
    checks: list[tuple[str, bool, str]] = [
        ("VAL1785_0_sources_exist", exists_ok, "all cited source paths exist"),
        ("VAL1785_1_needles_present", needles_ok, "required source needles are present"),
        (
            "VAL1785_2_lagrangian_gate_complete",
            any(row["gate_id"] == "PLT1785_8_verdict" for row in rows_map["lagrangian_theta_vx_gate"])
            and all(not boolish(row["valid_for_claim"]) and not boolish(row["parent_signed"]) for row in rows_map["lagrangian_theta_vx_gate"]),
            "parent Lagrangian/theta/v_X gate is complete and nonclaim",
        ),
        (
            "VAL1785_3_route_matrix_nonclaim",
            any(row["route_id"] == "MRM1785_0_strict_quotient_zero" for row in rows_map["minimal_fill_route_matrix"])
            and any(row["route_id"] == "MRM1785_1_hybrid_EH_plus_quotient_extra" for row in rows_map["minimal_fill_route_matrix"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["minimal_fill_route_matrix"]),
            "route matrix keeps strict quotient-zero and hybrid routes live without claim",
        ),
        (
            "VAL1785_4_noether_contract_complete",
            any(
                row["contract_id"] == "NPJ1785_0_parent_variation"
                and row["proof_status"] == "EXACT_CONDITIONAL_FORMULA"
                for row in rows_map["noether_pj_contract_gate"]
            )
            and any(
                row["contract_id"] == "NPJ1785_6_verdict"
                and row["proof_status"] == "CONTRACT_EXACT_CURRENT_UNFILLED"
                for row in rows_map["noether_pj_contract_gate"]
            ),
            "Noether P/J contract is exact conditional but unfilled",
        ),
        (
            "VAL1785_5_dqz_source_plan_nonclaim",
            any(row["row_id"] == "DGS1785_0_geometry_component" for row in rows_map["dqz_geometry_source_row_plan"])
            and all(
                not boolish(row["valid_for_claim"])
                and not boolish(row["score_ready"])
                and not boolish(row["valid_prediction_row"])
                for row in rows_map["dqz_geometry_source_row_plan"]
            ),
            "Dq_Z geometry/source rows remain nonclaim and not score-ready",
        ),
        (
            "VAL1785_6_countermodels_retained",
            all(boolish(row["survives_current_constraints"]) for row in rows_map["countermodel_ledger"]),
            "countermodels remain live until theorem or bound rows close them",
        ),
        (
            "VAL1785_7_claim_gates_blocked",
            all(
                not boolish(row["valid_for_claim"])
                and not boolish(row["gate_pass"])
                and row["status"] in {"BLOCKED", "REFUSED"}
                for row in rows_map["claim_gate"]
            ),
            "claim gates are blocked or refused",
        ),
        ("VAL1785_8_no_claim_flags", no_claim_flags(rows_map), "no generated score/claim flags are true"),
        ("VAL1785_9_missing_not_ready", missing_rows_not_ready(rows_map), "no MISSING_* row is marked ready"),
        (
            "VAL1785_10_decision_next",
            any(
                row["decision_id"] == "DEC1785_3_best_next"
                and "QUOTIENT_ZERO_OR_HYBRID" in row["decision"]
                for row in rows_map["decision_ledger"]
            ),
            "decision selects quotient-zero or hybrid boundary closure next",
        ),
        (
            "VAL1785_11_next_selected",
            any(row["route_id"] == "NEXT1785_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1785_12_csv_parse", all(parse_csv(path) for path in generated_csvs()), "all generated 1785 CSVs parse"),
        ("VAL1785_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1785_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1785_15_formalization_untouched", formalization_untouched(), "no 1785 outputs found under formalization-workbench"),
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
            "check_id": "VAL1785_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1785 parent Lagrangian/theta/v_X minimal-fill or Dq_Z geometry source-row checkpoint",
        }
    )
    return rows


def clean_cell(value: Any) -> str:
    return str(value).replace("\n", " ").replace("|", "/")


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = ["| " + " | ".join(clean_cell(row.get(column, "")) for column in columns) + " |" for row in rows]
    return "\n".join([header, sep, *body])


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        [
            "# 1785 - Y5/R2FR Parent Lagrangian-Theta-vX Minimal Fill or DqZ Geometry Source Row",
            "",
            "## Verdict",
            "",
            "1785 tries the derivation-first move after the 1784 `Omega/DC_X/v_X` handoff. The result is useful but still non-claim: the Noether/P-J contract is exact as a conditional theorem, but the actual parent `L_parent`, `theta_Y`, `v_X`, `mu_X`, boundary representative, and matter/projector silence are not signed in one branch.",
            "",
            "The cleanest route remains strict quotient-zero if it can be built: make the local residual direction vertical, prove descent through the quotient, and show ordinary matter/readout is blind to it. The more realistic backup is a hybrid `EH core + quotient-owned MTS extra sector`. The affine route is retained only as a countermodel guard because it can insert the shape without proving parent origin.",
            "",
            "**Claim ceiling:** no parent-fill claim, no derived local-GR/Newton/PPN/R10 claim, no finite residual score, no GitHub action, and no `formalization-workbench` edit is allowed from 1785.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "role"]),
            "",
            "## Parent Lagrangian-Theta-vX Gate",
            markdown_table(
                rows_map["lagrangian_theta_vx_gate"],
                ["gate_id", "clause", "mathematical_form", "current_status", "blocking_issue", "exit_condition", "valid_for_claim"],
            ),
            "",
            "## Minimal Fill Route Matrix",
            markdown_table(
                rows_map["minimal_fill_route_matrix"],
                ["route_id", "route", "mathematical_strategy", "strength", "failure_mode", "current_status", "next_action", "valid_for_claim"],
            ),
            "",
            "## Noether P/J Contract Gate",
            markdown_table(
                rows_map["noether_pj_contract_gate"],
                ["contract_id", "claim", "mathematical_form", "proof_status", "missing_for_current_claim", "valid_for_claim"],
            ),
            "",
            "## DqZ Geometry Source Row Plan",
            markdown_table(
                rows_map["dqz_geometry_source_row_plan"],
                ["row_id", "component", "why_needed", "required_formula", "current_value", "current_status", "score_ready", "valid_for_claim"],
            ),
            "",
            "## Countermodel Ledger",
            markdown_table(rows_map["countermodel_ledger"], ["countermodel_id", "countermodel", "survives_current_constraints", "why_survives", "what_kills_it"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "status", "blocker", "valid_for_claim"]),
            "",
            "## Decision Ledger",
            markdown_table(rows_map["decision_ledger"], ["decision_id", "decision", "reason", "next_action"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This checkpoint narrows the coupling problem to a concrete branch choice. We either prove the local residual is quotient-vertical and invisible to ordinary matter/readout, or we honestly demote it to finite `Dq_Z` leakage with source-backed local bounds. That is a good pressure point: it is no longer vague coupling fog, it is a named proof gate.",
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
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1785 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
