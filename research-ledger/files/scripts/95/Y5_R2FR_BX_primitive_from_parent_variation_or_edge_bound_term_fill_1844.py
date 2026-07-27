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
QUARANTINE = MICROSCOPE / "quarantine" / "1844"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1844-Y5-R2FR-BX-primitive-from-parent-variation-or-edge-bound-term-fill.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1844_0_1843_next",
        "source_key": "1843_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_NEXT_TARGET.csv",
        "needles": ["NEXT1843_0_primary", "1844-Y5-R2FR-BX-primitive"],
        "role": "1843 selects the B_X primitive or first edge-bound term as the next target.",
    },
    {
        "source_id": "SRC1844_1_1843_validation",
        "source_key": "1843_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1843_VALIDATION.csv",
        "needles": ["VAL1843_OVERALL", "PASS"],
        "role": "confirms 1843 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1844_2_1843_stokes",
        "source_key": "1843_weighted_stokes",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_WEIGHTED_STOKES_THEOREM_AND_BOUND.csv",
        "needles": ["ETB1843_5_verdict", "FAIL_CURRENT_CLAIM_BUT_DERIVATION_PROGRESS"],
        "role": "1843 gives the exact weighted-Stokes zero conditions and finite fallback bound.",
    },
    {
        "source_id": "SRC1844_3_1843_source_pack",
        "source_key": "1843_source_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1843_SOURCE_PACK_SCHEMA.csv",
        "needles": ["SP1843_2_edge_bound_terms", "MISSING_EDGEBOUND_TERMS"],
        "role": "1843 identifies the edge-bound terms missing from a first executable row.",
    },
    {
        "source_id": "SRC1844_4_1021_parent_variation",
        "source_key": "1021_parent_variation_template",
        "source_path": RESIDUALS / "P8_Y5_R10_1021_PARENT_VARIATION_TEMPLATE.csv",
        "needles": ["PVT1021_5_verdict", "map_written_not_closed"],
        "role": "1021 gives the prior B_X parent-variation template and failure mode.",
    },
    {
        "source_id": "SRC1844_5_1021_primitive_gates",
        "source_key": "1021_BX_primitive_gates",
        "source_path": RESIDUALS / "P8_Y5_R10_1021_BX_PRIMITIVE_GATES.csv",
        "needles": ["BXG1021_5_verdict", "fail_current_claim"],
        "role": "1021 lists the primitive closure gates that must all close together.",
    },
    {
        "source_id": "SRC1844_6_1021_scalar_split",
        "source_key": "1021_scalar_branch_separation",
        "source_path": RESIDUALS / "P8_Y5_R10_1021_SCALAR_BRANCH_SEPARATION.csv",
        "needles": ["SB1021_3_scalar_verdict", "separates_routes"],
        "role": "1021 separates scalar no-hair silence from the Noether edge-charge primitive route.",
    },
    {
        "source_id": "SRC1844_7_1021_edge_fill",
        "source_key": "1021_edge_bound_fill_schema",
        "source_path": RESIDUALS / "P8_Y5_R10_1021_EDGE_BOUND_FILL_SCHEMA.csv",
        "needles": ["EBF1021_5_verdict", "not_fillable_currently"],
        "role": "1021 supplies the first edge-bound fill schema.",
    },
    {
        "source_id": "SRC1844_8_1021_next",
        "source_key": "1021_next_target",
        "source_path": RESIDUALS / "P8_Y5_R10_1021_NEXT_TARGET.csv",
        "needles": ["1022-Y5-R10-vertical-quotient", "choose and test"],
        "role": "1021 selects the vertical quotient versus scalar no-hair branch choice.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1844_SOURCE_REGISTER.csv",
    "parent_variation": RESIDUALS / "P8_Y5_PARENT_QLOC_1844_PARENT_VARIATION_TEMPLATE.csv",
    "primitive_gates": RESIDUALS / "P8_Y5_PARENT_QLOC_1844_BX_PRIMITIVE_GATES.csv",
    "scalar_branch": RESIDUALS / "P8_Y5_PARENT_QLOC_1844_SCALAR_BRANCH_SEPARATION.csv",
    "edge_bound_fill": RESIDUALS / "P8_Y5_PARENT_QLOC_1844_EDGE_BOUND_FILL_SCHEMA.csv",
    "route_verdicts": RESIDUALS / "P8_Y5_PARENT_QLOC_1844_ROUTE_VERDICTS.csv",
    "gr_bridge": RESIDUALS / "P8_Y5_PARENT_QLOC_1844_GR_BRIDGE_STATUS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1844_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1844_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1844_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1844_VALIDATION.csv",
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


def parent_variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "template_id": "PVT1844_0_parent_first_variation",
            "object": "parent X-sector first variation",
            "formula": "delta L_X = E_A^X delta X^A + d Theta_X(Phi,delta X)",
            "closure_test": "L_X, field normalization, source coupling, and boundary terms are all parent-signed before local readout",
            "current_status": "FORMULA_TRANSFERRED_NOT_PARENT_SIGNED",
            "implication": "variation algebra is available but not a derivation of the MTS edge primitive",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "template_id": "PVT1844_1_vertical_Noether_route",
            "object": "vertical/gauge branch",
            "formula": "delta_epsilon X^A=R_i^A epsilon^i+R_i^{A mu} nabla_mu epsilon^i; J_epsilon=Theta_X(delta_epsilon X)-mu_epsilon=dQ_epsilon+epsilon C_X",
            "closure_test": "vertical generator is actual parent gauge direction and not a fitted local closure",
            "current_status": "VERTICAL_GENERATOR_UNSIGNED",
            "implication": "Noether edge silence cannot be claimed yet",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "template_id": "PVT1844_2_boundary_covector",
            "object": "boundary adjoint covector",
            "formula": "B_DC[X,deltaY]=-int_S n_mu X_nu delta P^{mu nu}+delta Q_X+density/reference terms",
            "closure_test": "delta Q_X cancels every boundary covector or remaining covectors are explicitly bounded",
            "current_status": "COVECTOR_OWNER_MISSING",
            "implication": "edge source cannot be zeroed by words like exactness without a primitive",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "template_id": "PVT1844_3_BX_definition",
            "object": "edge boundary momentum",
            "formula": "B_X := i_S^*(n_mu P_X^{mu nu} epsilon_nu + B_ct[epsilon]) as a surface top form",
            "closure_test": "P_X and B_ct are fixed by the same parent action and reference principle",
            "current_status": "DEFINITION_WRITTEN_PRIMITIVE_NOT_DERIVED",
            "implication": "B_X is the next derivation bottleneck",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "template_id": "PVT1844_4_hodge_decomposition",
            "object": "surface decomposition",
            "formula": "B_X=d_S b_X+h_X+r_X on S_edge",
            "closure_test": "derive b_X and show h_X=r_X=0, or source-bound all three terms",
            "current_status": "DECOMPOSITION_CONTRACT_READY",
            "implication": "weighted-Stokes bound has a precise algebraic slot but no numeric/source-backed payload",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "template_id": "PVT1844_5_verdict",
            "object": "parent variation to primitive map",
            "formula": "parent L_X/Theta_X/Q_X -> P_X,B_ct -> B_X -> d_S b_X+h_X+r_X -> Q_edge bound",
            "closure_test": "every arrow is parent-signed or theorem-zero, with no missing edge-bound term",
            "current_status": "MAP_WRITTEN_NOT_CLOSED",
            "implication": "B_X primitive is not derived in current MTS",
            "valid_for_claim": False,
        },
    ]


def primitive_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "BXG1844_0_same_parent_origin",
            "primitive_requirement": "P_X, J_X, Theta_X, Q_X, Omega_X, and B_ct all come from one parent L_X",
            "test": "compare adjoint operator, Noether current, symplectic form, and counterterm from the same action",
            "current_result": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "single signed parent sector action with source normalization and boundary reference",
            "if_missing": "B_X can be an assembled closure rather than a derived primitive",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "BXG1844_1_counterterm_owner",
            "primitive_requirement": "B_ct is fixed before readout",
            "test": "delta(Q_X+B_ct)-i_epsilon Theta_X has no uncancelled boundary covector",
            "current_result": "NOT_DERIVED",
            "missing_for_claim": "differentiability/reference principle for the X-sector boundary class",
            "if_missing": "reference/counterterm can accidentally absorb source calibration",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "BXG1844_2_exact_surface_pullback",
            "primitive_requirement": "i_S^*B_X-h_X is exact on S_edge",
            "test": "construct b_X with B_X-h_X=d_S b_X and verify patch overlap compatibility",
            "current_result": "NOT_DERIVED",
            "missing_for_claim": "explicit b_X primitive or theorem bounding norm_bX",
            "if_missing": "weighted-Stokes exact route remains conditional",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "BXG1844_3_harmonic_zero",
            "primitive_requirement": "harmonic/cohomology edge class vanishes or is bounded",
            "test": "Pi_Hedge[B_X]=0, or h_X coefficient bound is source-backed",
            "current_result": "MISSING_COHOMOLOGY_PROOF_OR_BOUND",
            "missing_for_claim": "boundary cohomology certificate plus source-backed harmonic bound",
            "if_missing": "closed edge classes can feed R10/R11",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "BXG1844_4_kernel_norm",
            "primitive_requirement": "d_S(F_lambda epsilon_X) is zero or bounded",
            "test": "closed weight on S_edge, or source-backed norm_dS_Feps",
            "current_result": "MISSING_KERNEL_DERIVATIVE_BOUND",
            "missing_for_claim": "edge geometry, lambda support, allowed epsilon_X domain",
            "if_missing": "even exact B_X leaves a weighted derivative residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "BXG1844_5_verdict",
            "primitive_requirement": "B_X primitive closure",
            "test": "BXG1844_0 through BXG1844_4 close together",
            "current_result": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "parent-signed primitive or source-backed edge-bound pack",
            "if_missing": "move to vertical quotient construction or scalar/source coefficient fallback",
            "valid_for_claim": False,
        },
    ]


def scalar_branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "branch": "SB1844_0_scalar_like_LX",
            "formula": "L_X=1/2 sqrt(h)(Z_X |grad X|^2+M_X^2 X^2)-sqrt(h) X J_X",
            "boundary_result": "positive operator plus J_X=0 can silence X under selected boundary conditions",
            "warning": "this is not a Noether edge-charge primitive unless X is also a gauge/vertical direction",
            "status": "CONDITIONAL_ROUTE_ONLY",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "branch": "SB1844_1_scalar_boundary_condition",
            "formula": "delta X|_S=0 or n.grad X|_S=0 plus positive operator and J_X=0",
            "boundary_result": "boundary flux can vanish for a specified boundary-value problem",
            "warning": "the parent theory must select these conditions; they cannot be imposed after local data are seen",
            "status": "NOT_PROMOTED",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "branch": "SB1844_2_scalar_source_route",
            "formula": "(-Z_X Delta+M_X^2)X=J_X with Z_X>0 and M_X^2>=0",
            "boundary_result": "if J_X=0 and boundary data vanish, X=0 by positive-energy/no-hair argument",
            "warning": "requires actual Z_X, M_X^2, J_X and boundary condition from the parent action",
            "status": "MISSING_SOURCE_COEFFICIENTS",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "branch": "SB1844_3_scalar_verdict",
            "formula": "scalar no-hair can be a fallback theorem, not the B_X primitive theorem",
            "boundary_result": "separates_routes",
            "warning": "do not mix scalar silence with Noether edge-charge exactness",
            "status": "ROUTE_SPLIT_RETAINED",
            "valid_for_claim": False,
        },
    ]


def edge_bound_fill_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "fill_id": "EBF1844_0_norm_bX",
            "quantity": "norm_bX",
            "definition": "dual norm of the primitive b_X entering |int_S d_S(F epsilon) wedge b_X|",
            "required_source": "explicit b_X from P_X/B_ct or a theorem-bound on b_X",
            "current_status": "MISSING_BX_PRIMITIVE_OR_BOUND",
            "units": "edge_charge_units",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "EBF1844_1_harmonic_edge_abs",
            "quantity": "harmonic_edge_abs",
            "definition": "absolute harmonic/cohomology contribution |int_S F epsilon h_X|",
            "required_source": "H_edge projection of B_X or no-hair/cohomology theorem",
            "current_status": "MISSING_H_EDGE_ZERO_OR_BOUND",
            "units": "edge_charge_units",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "EBF1844_2_residual_edge_abs",
            "quantity": "residual_edge_abs",
            "definition": "absolute non-exact/non-harmonic residual contribution |int_S F epsilon r_X|",
            "required_source": "proof r_X=0 or a source-backed residual bound",
            "current_status": "MISSING_PARENT_RESIDUAL_BOUND",
            "units": "edge_charge_units",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "EBF1844_3_norm_dS_Feps",
            "quantity": "norm_dS_Feps",
            "definition": "surface derivative norm of F_lambda epsilon_X over the selected edge geometry",
            "required_source": "edge geometry, lambda support, and allowed epsilon_X domain",
            "current_status": "MISSING_KERNEL_DERIVATIVE_BOUND",
            "units": "inverse_length_or_surface_weight_units",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "EBF1844_4_corner",
            "quantity": "C_corner",
            "definition": "absolute corner contribution if the edge surface has a boundary or joints",
            "required_source": "corner-free certificate or corner charge bound",
            "current_status": "MISSING_CORNER_AUDIT",
            "units": "edge_charge_units",
            "source_path": "MISSING_SOURCE_PATH",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "fill_id": "EBF1844_5_verdict",
            "quantity": "EDGEBOUND fillability",
            "definition": "first executable edge-bound row requires all EBF1844_0 through EBF1844_4",
            "required_source": "primitive or numeric/source-backed bound for every term",
            "current_status": "NOT_FILLABLE_CURRENTLY",
            "units": "mixed_missing_units",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1844_EDGE_BOUND_FILL_SCHEMA.csv",
            "valid_for_claim": False,
        },
    ]


def route_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "R1844_0_vertical_gauge_primitive",
            "route": "derive B_X as a Noether/vertical primitive",
            "status": "BEST_CLEAN_ROUTE_NOT_CLOSED",
            "because": "if X is a genuine vertical redundancy, local source poles can disappear before fitting",
            "next_step": "construct q, v_X, action descent, matter descent, boundary silence and degree count",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "R1844_1_scalar_nohair_route",
            "route": "positive scalar/source-free no-hair",
            "status": "FALLBACK_SEPARATE_ROUTE",
            "because": "can yield X=0 under signed positivity and source-free boundary data, but it is not an edge primitive",
            "next_step": "source Z_X, M_X^2, J_X, boundary conditions and no-hair theorem if quotient route fails",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "R1844_2_edge_bound_fill",
            "route": "finite edge-bound residual",
            "status": "FALLBACK_SCHEMA_READY",
            "because": "weighted-Stokes gives a finite bound once b_X, harmonic, residual, kernel and corner terms are sourced",
            "next_step": "fill EDGEBOUND rows as nonclaim source-backed inputs",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "R1844_3_verdict",
            "route": "B_X primitive checkpoint",
            "status": "FAIL_CURRENT_CLAIM_BUT_SPLITS_ROUTES",
            "because": "the primitive map is exact enough to audit but not parent-signed enough to claim",
            "next_step": "move to vertical quotient construction or scalar no-hair branch choice",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def gr_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1844_0_BX_primitive",
            "bridge_piece": "edge primitive needed for local GR silence",
            "current_status": "BLOCKED_NOT_PARENT_SIGNED",
            "evidence": "PVT1844_5_verdict;BXG1844_5_verdict",
            "remaining_gap": "derive b_X from parent L_X/Theta_X/Q_X/B_ct or source-bound the edge terms",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1844_1_scalar_branch",
            "bridge_piece": "positive scalar no-hair local silence",
            "current_status": "SEPARATE_FALLBACK_NOT_EDGE_PROOF",
            "evidence": "SB1844_3_scalar_verdict",
            "remaining_gap": "source Z_X/M_X2/J_X and parent-selected boundary conditions",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1844_2_edge_bound",
            "bridge_piece": "finite weighted-Stokes edge residual",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "evidence": "EBF1844_0 through EBF1844_5",
            "remaining_gap": "fill norm_bX, harmonic/residual terms, kernel derivative and corner audit",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1844_3_local_GR_Newton",
            "bridge_piece": "derived local GR/Newton reduction",
            "current_status": "BLOCKED",
            "evidence": "nonzero or unbounded edge/local source branch still possible",
            "remaining_gap": "quotient no-pole theorem or bounded residual small enough for local tests",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1844_4_next",
            "bridge_piece": "next derivation owner",
            "current_status": "VERTICAL_QUOTIENT_OR_SCALAR_NOHAIR_BRANCH_CHOICE_IS_NEXT",
            "evidence": "DEC1844_2_best_next;NEXT1844_0_primary",
            "remaining_gap": "choose/test least-scrutiny local branch without mixing routes",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1844_0_sources_registered",
            "claim": "1844 source chain exists",
            "gate_pass": False,
            "reason": "sources exist for audit only; they do not make parent primitive signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1844_1_BX_primitive_derived",
            "claim": "B_X=d_S b_X is derived",
            "gate_pass": False,
            "reason": "PVT1844_5 and BXG1844_5 remain fail-current-claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1844_2_Qedge_zero",
            "claim": "Q_edge(lambda)=0",
            "gate_pass": False,
            "reason": "exactness, harmonic zero, kernel closure and corner silence are not parent-signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1844_3_scalar_nohair",
            "claim": "scalar no-hair gives local silence",
            "gate_pass": False,
            "reason": "scalar branch requires real Z_X, M_X2, J_X and parent-selected boundary data",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1844_4_edge_bound_executable",
            "claim": "first edge-bound row is executable",
            "gate_pass": False,
            "reason": "EDGEBOUND terms have missing source paths and units",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1844_5_local_GR_Newton",
            "claim": "local GR/Newton reduction passes",
            "gate_pass": False,
            "reason": "local source branch remains theorem-unclosed and unbounded",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1844_0_primitive_result",
            "decision": "The explicit B_X primitive is still not derivable from current files.",
            "reason": "The parent L_X/Theta_X/Q_X/P_X/B_ct chain is an audit contract, not a signed parent variation.",
            "next_action": "do not claim Q_edge zero; attack the branch-choice theorem directly",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1844_1_route_split",
            "decision": "Keep gauge-edge and scalar no-hair routes separate.",
            "reason": "Scalar positivity can silence an X field under source-free conditions, but it does not automatically supply a Noether edge primitive.",
            "next_action": "test the quotient/vertical construction first, scalar no-hair second",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1844_2_best_next",
            "decision": "The least-scrutiny route is the vertical quotient construction if it can be built.",
            "reason": "Removing X before variation is cleaner than bounding a leftover local coupling after the fact.",
            "next_action": "1845-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1844_3_fallback",
            "decision": "If no quotient/vertical construction closes, fill EDGEBOUND and scalar source coefficients.",
            "reason": "Then MTS survives or fails as a bounded residual theory rather than a theorem-zero local-GR branch.",
            "next_action": "fill EBF1844 terms plus Z_X/M_X2/J_X/K_X/Qbar/qbar rows",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1844_0_primary",
            "next_target": "1845-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md",
            "script": "scripts/Y5_R2FR_vertical_quotient_LX_construction_or_scalar_nohair_branch_choice_1845.py",
            "objective": "choose and test the least-scrutiny local branch: construct X as absent/vertical quotient before variation, or demote to scalar positive no-hair/source-coefficient route",
            "selection_status": "selected",
            "success_condition": "q, v_X, action descent, matter descent, boundary silence and degree count close together, or scalar/source branch is explicitly demoted to nonclaim coefficients",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1844_1_parallel",
            "next_target": "1845b-Y5-R2FR-EDGEBOUND-source-term-fill.md",
            "script": "scripts/Y5_R2FR_EDGEBOUND_source_term_fill_1845b.py",
            "objective": "fill norm_bX, harmonic_edge_abs, residual_edge_abs, norm_dS_Feps and C_corner with source-backed nonclaim rows",
            "selection_status": "parallel_held",
            "success_condition": "first edge-bound row parses with real units and source paths but remains valid_for_claim=false until all gates close",
        },
    ]


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "parent_variation": parent_variation_rows(),
        "primitive_gates": primitive_gate_rows(),
        "scalar_branch": scalar_branch_rows(),
        "edge_bound_fill": edge_bound_fill_rows(),
        "route_verdicts": route_verdict_rows(),
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
            RAB_QUEUE / f"JR1844_{key.upper()}.csv",
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
        if not (RAB_QUEUE / f"JR1844_{key.upper()}.csv").exists():
            return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = [
        "1844-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1844",
        "P8_Y5_BRR545_1844",
        "Y5_R2FR_BX_primitive_from_parent_variation_or_edge_bound_term_fill_1844",
    ]
    return not any(any(marker in path.name for marker in markers) for path in FORMALIZATION.rglob("*"))


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
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
        ("VAL1844_0_sources_exist", all(row["exists"] is True for row in source_rows), "all cited source paths exist"),
        ("VAL1844_1_needles_present", all(row["needles_present"] is True for row in source_rows), "all cited source needles are present"),
        (
            "VAL1844_2_parent_map_blocks_claim",
            any(row["template_id"] == "PVT1844_5_verdict" and row["current_status"] == "MAP_WRITTEN_NOT_CLOSED" for row in rows_map["parent_variation"]),
            "parent variation to primitive map remains nonclaim",
        ),
        (
            "VAL1844_3_primitive_gates_block_claim",
            any(row["gate_id"] == "BXG1844_5_verdict" and row["current_result"] == "FAIL_CURRENT_CLAIM" for row in rows_map["primitive_gates"]),
            "B_X primitive closure gates remain nonclaim",
        ),
        (
            "VAL1844_4_scalar_branch_separated",
            any(row["branch"] == "SB1844_3_scalar_verdict" and row["boundary_result"] == "separates_routes" for row in rows_map["scalar_branch"]),
            "scalar no-hair route is separated from Noether primitive route",
        ),
        (
            "VAL1844_5_edge_bound_not_fillable",
            any(row["fill_id"] == "EBF1844_5_verdict" and row["current_status"] == "NOT_FILLABLE_CURRENTLY" for row in rows_map["edge_bound_fill"]),
            "edge-bound first row remains not fillable",
        ),
        (
            "VAL1844_6_route_verdict_nonclaim",
            any(row["route_id"] == "R1844_3_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_BUT_SPLITS_ROUTES" for row in rows_map["route_verdicts"]),
            "route verdict splits the theorem routes without claim promotion",
        ),
        (
            "VAL1844_7_bridge_next_selected",
            any(row["status_id"] == "GB1844_4_next" and row["current_status"] == "VERTICAL_QUOTIENT_OR_SCALAR_NOHAIR_BRANCH_CHOICE_IS_NEXT" for row in rows_map["gr_bridge"]),
            "bridge status selects vertical quotient/scalar branch choice next",
        ),
        (
            "VAL1844_8_claim_gates_blocked",
            all(row["gate_pass"] is False and row["claim_allowed"] is False for row in rows_map["claim_gate"]),
            "all claim gates remain blocked",
        ),
        (
            "VAL1844_9_decision_best_next",
            any(row["decision_id"] == "DEC1844_2_best_next" and "vertical quotient" in row["decision"] for row in rows_map["decision"]),
            "decision ledger selects least-scrutiny vertical quotient route first",
        ),
        (
            "VAL1844_10_next_target_selected",
            any(row["route_id"] == "NEXT1844_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1844_11_no_claim_flags", no_claim_flags(rows_map), "no claim flags are true"),
        ("VAL1844_12_missing_rows_nonclaim", missing_rows_not_ready(rows_map), "MISSING_* rows stay nonclaim"),
        ("VAL1844_13_csv_parse", csv_parse_all(), "all generated 1844 CSVs parse"),
        ("VAL1844_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1844_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1844_16_formalization_untouched", no_formalization_outputs(), "no 1844 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1844_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1844 B_X primitive from parent variation or edge-bound term fill",
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
            "# 1844 Y5 R2FR B_X primitive from parent variation or edge-bound term fill",
            "",
            "**Progress:** 1844 ports the earlier R10 primitive audit into the active parent-q_loc branch and makes the fork explicit: either derive `B_X=d_S b_X+h_X+r_X` from one parent variation, or stop trying to call the edge term zero and fill a finite edge-bound row.",
            "",
            "**Current verdict:** `B_X` is still not derivable from current files. The checkpoint does not close local GR; it turns the local source leakage into a clean branch choice between vertical quotient removal, scalar no-hair fallback, or sourced edge-bound residuals.",
            "",
            "**Claim ceiling:** no `B_X=d_S b_X`, no `Q_edge=0`, no scalar no-hair local silence, no R10/R11 pass, no PPN pass, no local-GR/Newton reduction, no GitHub action, and no `formalization-workbench` edit is allowed from 1844.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Parent Variation Template",
            markdown_table(rows_map["parent_variation"], ["template_id", "object", "formula", "closure_test", "current_status", "implication", "valid_for_claim"]),
            "",
            "## B_X Primitive Gates",
            markdown_table(rows_map["primitive_gates"], ["gate_id", "primitive_requirement", "test", "current_result", "missing_for_claim", "if_missing", "valid_for_claim"]),
            "",
            "## Scalar Branch Separation",
            markdown_table(rows_map["scalar_branch"], ["branch", "formula", "boundary_result", "warning", "status", "valid_for_claim"]),
            "",
            "## Edge Bound Fill Schema",
            markdown_table(rows_map["edge_bound_fill"], ["fill_id", "quantity", "definition", "required_source", "current_status", "units", "source_path", "valid_for_claim"]),
            "",
            "## Route Verdicts",
            markdown_table(rows_map["route_verdicts"], ["route_id", "route", "status", "because", "next_step", "claim_allowed", "valid_for_claim"]),
            "",
            "## GR Bridge Status",
            markdown_table(rows_map["gr_bridge"], ["status_id", "bridge_piece", "current_status", "evidence", "remaining_gap", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "reason", "next_action", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is not a defeat; it is a useful narrowing of the battlefield. The cleanest way to reduce to GR remains: remove the extra local branch before variation by showing it is quotient/vertical. If that cannot be built, the honest route is scalar no-hair with real coefficients or a finite residual bound. No more ghost-coupling sneaking through the side door.",
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
    print(f"1844 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
