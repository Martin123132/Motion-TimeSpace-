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
QUARANTINE = MICROSCOPE / "quarantine" / "1845"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1845-Y5-R2FR-vertical-quotient-LX-construction-or-scalar-nohair-branch-choice.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1845_0_1844_next",
        "source_key": "1844_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1844_NEXT_TARGET.csv",
        "needles": ["NEXT1844_0_primary", "1845-Y5-R2FR-vertical-quotient"],
        "role": "1844 selects vertical quotient versus scalar no-hair branch choice.",
    },
    {
        "source_id": "SRC1845_1_1844_validation",
        "source_key": "1844_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1844_VALIDATION.csv",
        "needles": ["VAL1844_OVERALL", "PASS"],
        "role": "confirms 1844 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1845_2_1844_BX_gate",
        "source_key": "1844_BX_primitive_gate",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1844_BX_PRIMITIVE_GATES.csv",
        "needles": ["BXG1844_5_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1844 shows the Noether/edge primitive route is still not parent-signed.",
    },
    {
        "source_id": "SRC1845_3_1844_scalar_split",
        "source_key": "1844_scalar_branch_split",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1844_SCALAR_BRANCH_SEPARATION.csv",
        "needles": ["SB1844_3_scalar_verdict", "separates_routes"],
        "role": "1844 requires scalar no-hair to remain separate from edge exactness.",
    },
    {
        "source_id": "SRC1845_4_1022_vertical_quotient",
        "source_key": "1022_vertical_quotient_construction",
        "source_path": RESIDUALS / "P8_Y5_R10_1022_VERTICAL_QUOTIENT_CONSTRUCTION.csv",
        "needles": ["VQC1022_7_verdict", "fail_current_claim_but_best_next_target"],
        "role": "1022 supplies the quotient/vertical construction clauses.",
    },
    {
        "source_id": "SRC1845_5_1022_scalar_nohair",
        "source_key": "1022_scalar_nohair_construction",
        "source_path": RESIDUALS / "P8_Y5_R10_1022_SCALAR_NOHAIR_CONSTRUCTION.csv",
        "needles": ["SNH1022_6_verdict", "fallback_not_next_best"],
        "role": "1022 records scalar no-hair as a fallback route, not an edge primitive.",
    },
    {
        "source_id": "SRC1845_6_1023_qvx_certificate",
        "source_key": "1023_qvx_certificate",
        "source_path": RESIDUALS / "P8_Y5_R10_1023_QVX_CERTIFICATE.csv",
        "needles": ["QVC1023_8_verdict", "fail_current_claim_demote_current_branch"],
        "role": "1023 tested the single q/v_X/action descent certificate and found it unclosed.",
    },
    {
        "source_id": "SRC1845_7_1023_coupling_audit",
        "source_key": "1023_coupling_descent_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1023_COUPLING_DESCENT_AUDIT.csv",
        "needles": ["CDA1023_4_verdict", "coupling_not_theorem_zero"],
        "role": "1023 identifies the matter/boundary/projector coupling that remains live.",
    },
    {
        "source_id": "SRC1845_8_1023_scalar_pack",
        "source_key": "1023_scalar_source_input_pack",
        "source_path": RESIDUALS / "P8_Y5_R10_1023_SCALAR_SOURCE_INPUT_PACK.csv",
        "needles": ["SNH1023_0_Z_X", "MISSING_PARENT_INPUT"],
        "role": "1023 supplies the scalar no-hair/source-coefficient input pack.",
    },
    {
        "source_id": "SRC1845_9_1023_next",
        "source_key": "1023_next_target",
        "source_path": RESIDUALS / "P8_Y5_R10_1023_NEXT_TARGET.csv",
        "needles": ["1024-Y5-R10-scalar-nohair", "fill or reject"],
        "role": "1023 selects scalar no-hair input fill or residual alpha runner after quotient failure.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1845_SOURCE_REGISTER.csv",
    "branch_matrix": RESIDUALS / "P8_Y5_PARENT_QLOC_1845_BRANCH_DECISION_MATRIX.csv",
    "qvx_certificate": RESIDUALS / "P8_Y5_PARENT_QLOC_1845_QVX_CERTIFICATE.csv",
    "coupling_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1845_COUPLING_DESCENT_AUDIT.csv",
    "scalar_input_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1845_SCALAR_NOHAIR_INPUT_PACK.csv",
    "fallback_source_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1845_FALLBACK_SOURCE_ROWS.csv",
    "demotion": RESIDUALS / "P8_Y5_PARENT_QLOC_1845_DEMOTION_LEDGER.csv",
    "gr_bridge": RESIDUALS / "P8_Y5_PARENT_QLOC_1845_GR_BRIDGE_STATUS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1845_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1845_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1845_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1845_VALIDATION.csv",
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


def branch_matrix_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "matrix_id": "BDM1845_0_vertical_quotient",
            "candidate": "quotient/vertical removal before variation",
            "core_test": "q, v_X, action descent, matter descent, boundary silence and degree count close together",
            "scrutiny_level": "least_post_hoc_if_successful",
            "current_status": "TESTED_NOT_CLOSED",
            "missing": "single parent certificate for field-by-field vertical action and descended matter/boundary terms",
            "decision": "demote current local branch; keep quotient route as future parent-action theorem target",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "matrix_id": "BDM1845_1_scalar_nohair",
            "candidate": "positive scalar no-hair/source-free local silence",
            "core_test": "Z_X>0, M_X^2>=0, J_X=0 and boundary_flux_X=0 imply X=0 in compact exterior",
            "scrutiny_level": "honest_fallback_if_coefficients_are_real",
            "current_status": "PROMOTED_TO_NEXT_WORK_TARGET_NOT_CLAIM",
            "missing": "Z_X, M_X2, J_X, boundary flux and lambda_X source rows",
            "decision": "attempt next because it is executable after quotient certificate failure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "matrix_id": "BDM1845_2_finite_residual",
            "candidate": "bounded residual coupling/source branch",
            "core_test": "K_X, Qbar_XH, qbar_XT, EDGEBOUND, FB5540 and R11 rows form no-cancellation envelope",
            "scrutiny_level": "empirical_score_route",
            "current_status": "FALLBACK_IF_NOHAIR_FAILS",
            "missing": "source-backed coefficient rows and local arena projection",
            "decision": "score residual instead of asserting local silence",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def qvx_certificate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "QVC1845_0_parent_q",
            "required_object": "parent quotient map q",
            "pass_condition": "q is canonical parent reduction, not post-readout projection; Dq[v_X]=0 for actual local X direction",
            "current_evidence": "prior quotient pieces are conditional and do not identify actual local MTS X variations with the null generator",
            "current_status": "PARTIAL_CONDITIONAL",
            "missing_for_claim": "prove actual local Xhat variations equal the parent null/relative-exact generator",
            "claim_effect_if_signed": "X is representative data, not a physical local field",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "QVC1845_1_NX_integrability",
            "required_object": "integrable null distribution N_X",
            "pass_condition": "N_X is parent-owned, invariant under parent symmetries, and integrable on compact local domain",
            "current_evidence": "construction is stated conditionally in prior ledgers",
            "current_status": "NOT_PARENT_SIGNED",
            "missing_for_claim": "field-space distribution, Frobenius/integrability proof, and domain admissibility",
            "claim_effect_if_signed": "q fibres are legitimate representative orbits",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "QVC1845_2_action_descent",
            "required_object": "parent action descent",
            "pass_condition": "S_parent[Phi]=S_red[q(Phi)]+fixed boundary/topological terms before variation",
            "current_evidence": "action descent remains a conditional theorem with retained boundary/domain terms",
            "current_status": "CONDITIONAL_ONLY",
            "missing_for_claim": "explicit parent Lagrangian and proof retained boundary/domain terms are silent",
            "claim_effect_if_signed": "no independent X Hessian, Green function, or K_X",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "QVC1845_3_matter_descent",
            "required_object": "ordinary matter quotient functor",
            "pass_condition": "S_matter=Sbar_m[Obs(q(Phi)),psi,theta_A] and L_vX theta_A=0 for constants/material markers",
            "current_evidence": "metric/frame chain rule can pass conditionally, but constants, EM labels and material markers are not parent-owned",
            "current_status": "CONDITIONAL_THEOREM_ONLY",
            "missing_for_claim": "no-marker constants, EM/material labels, hidden conformal/disformal channel exclusion",
            "claim_effect_if_signed": "qbar_XT=0 and no ordinary matter X source",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "QVC1845_4_vertical_action",
            "required_object": "field-by-field v_X",
            "pass_condition": "v_X is specified on metric/coframe, canonical data, memory/projector/domain fields, matter readout, and boundary fields",
            "current_evidence": "candidate maps exist only as partial route language; active PARENT_QLOC branch has no full transformation law",
            "current_status": "MISSING",
            "missing_for_claim": "actual MTS parent transformation law on every field class",
            "claim_effect_if_signed": "DCdagger/Omega-flat map becomes a calculation",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "QVC1845_5_momentum_map",
            "required_object": "differentiable first-class generator",
            "pass_condition": "delta G_X=Omega(delta Phi,v_X), G_X=int epsilon C_X+Q_X, and bracket closes without active K_boundary",
            "current_evidence": "parent theta/Omega/DC_X/Q_X and edge differentiability remain unsigned",
            "current_status": "NOT_DERIVED",
            "missing_for_claim": "parent symplectic potential, DC_X, Q_X differentiability and algebra closure",
            "claim_effect_if_signed": "X is constraint/gauge, not physical source field",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "QVC1845_6_boundary_silence",
            "required_object": "local boundary/edge silence",
            "pass_condition": "Q_X=0/proper/exact and Pi_M^H[Q_X]=0 with no edge cocycle on compact branch",
            "current_evidence": "1843-1844 show B_X primitive, projector orthogonality, and EDGEBOUND terms remain unsigned",
            "current_status": "BLOCKED_BY_1843_1844",
            "missing_for_claim": "B_X primitive, weighted-Stokes zero/bound, projector orthogonality, and cocycle audit",
            "claim_effect_if_signed": "Qbar_XH=0 and no edge alpha branch",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "QVC1845_7_degree_count",
            "required_object": "constraint rank and reduced nondegeneracy",
            "pass_condition": "primary+secondary first-class pair removes X pair; reduced Omega has no proper X stabilizer",
            "current_evidence": "rank and no-stabilizer computation are not in the current parent branch",
            "current_status": "NOT_CHECKED",
            "missing_for_claim": "rank calculation, no-stabilizer theorem, and reduced phase-space proof",
            "claim_effect_if_signed": "zero Hessian becomes gauge evidence rather than under-specified dynamics",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "certificate_id": "QVC1845_8_verdict",
            "required_object": "single q/v_X/action descent certificate",
            "pass_condition": "QVC1845_0 through QVC1845_7 all parent-signed together",
            "current_evidence": "conditional pieces exist, but no single parent certificate closes in active PARENT_QLOC branch",
            "current_status": "FAIL_CURRENT_CLAIM_DEMOTE_CURRENT_BRANCH",
            "missing_for_claim": "q, v_X, action, matter, boundary and degree certificates in one source-backed row",
            "claim_effect_if_signed": "K_X=qbar_XT=Qbar_XH=0 and local X alpha inactive",
            "valid_for_claim": False,
        },
    ]


def coupling_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CDA1845_0_metric_chain_rule",
            "object": "metric/coframe matter variation",
            "result": "CONDITIONAL_MATH_PASS",
            "reason": "DObs(Dq[v_X])=0 kills metric/frame pullback only if v_X is truly vertical",
            "remaining_coupling": "none from metric/frame channel if q/v_X closes",
            "demotion_effect": "if q/v_X fails, retain qbar_XT rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CDA1845_1_constants_markers",
            "object": "theta_A constants/material labels",
            "result": "NOT_CLOSED",
            "reason": "L_vX theta_A is not parent-owned for EM, clocks, masses or material labels",
            "remaining_coupling": "constant/material marker X-dependence",
            "demotion_effect": "retain clock/EM/WEP source rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CDA1845_2_hidden_frame",
            "object": "hidden conformal/disformal X channel",
            "result": "COUNTEREXAMPLE_FILTER_ONLY",
            "reason": "hidden X-frame dependence is observable unless it factors through q or is finite-coupled",
            "remaining_coupling": "F_X prime or disformal coefficient if present",
            "demotion_effect": "source/coefficient pack required",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CDA1845_3_projector_boundary",
            "object": "projector/boundary coupling",
            "result": "OPEN",
            "reason": "B_X, Pi_M^H[Q_edge], K_boundary and source split remain unsigned",
            "remaining_coupling": "edge/source projection into measured Hamiltonian mass",
            "demotion_effect": "retain EDGEBOUND and Qbar_edge rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "CDA1845_4_verdict",
            "object": "coupling descent verdict",
            "result": "COUPLING_NOT_THEOREM_ZERO",
            "reason": "matter descent and boundary/projector descent are conditional, not parent-signed",
            "remaining_coupling": "qbar_XT;Qbar_XH;edge terms;clock/WEP channels",
            "demotion_effect": "move to scalar no-hair/source coefficient input pack",
            "valid_for_claim": False,
        },
    ]


def scalar_input_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "SNH1845_0_Z_X",
            "quantity": "Z_X",
            "needed_for": "positive kinetic term",
            "required_source": "parent Hessian second variation with field units",
            "current_status": "MISSING_PARENT_INPUT",
            "if_missing": "no scalar no-hair theorem; score residual",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SNH1845_1_M_X2",
            "quantity": "M_X^2",
            "needed_for": "positive mass gap and lambda_X",
            "required_source": "parent Hessian curvature/range derivation with units",
            "current_status": "MISSING_PARENT_INPUT",
            "if_missing": "zero/long-range/tachyonic mode remains possible",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SNH1845_2_J_X_zero",
            "quantity": "J_X=0",
            "needed_for": "source-free exterior equation",
            "required_source": "matter/hidden/source variation proof or sourced current bound",
            "current_status": "MISSING_SOURCE_ZERO_PROOF",
            "if_missing": "qbar_XT/source coupling row required",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SNH1845_3_boundary_flux_zero",
            "quantity": "boundary_flux_X=0",
            "needed_for": "positive energy identity conclusion",
            "required_source": "boundary class/no-hair/projector silence or flux bound",
            "current_status": "MISSING_BOUNDARY_LOCK",
            "if_missing": "EDGEBOUND and Qbar_edge rows remain live",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SNH1845_4_lambda_X",
            "quantity": "lambda_X=sqrt(Z_X/M_X^2)",
            "needed_for": "R10/R11 range projection",
            "required_source": "signed Z_X and M_X2 with consistent units",
            "current_status": "MISSING_RANGE_DERIVATION",
            "if_missing": "no alpha(lambda) local score row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SNH1845_5_alpha_coefficients",
            "quantity": "K_X;Qbar_XH;qbar_XT;lambda_X",
            "needed_for": "R10/R11 residual scoring if no-hair fails",
            "required_source": "source-normalized coefficient rows with units and no-cancellation envelope",
            "current_status": "MISSING_ARENA_PROJECTION",
            "if_missing": "no local empirical pass",
            "valid_for_claim": False,
        },
    ]


def fallback_source_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "FBR1845_0_quotient_certificate",
            "quantity": "q_vX_action_matter_boundary_certificate",
            "required_columns": "q_id;vX_id;action_descent;matter_descent;boundary_silence;degree_count;source_path;valid_for_claim",
            "current_status": "MISSING_CERTIFICATE",
            "used_if": "quotient/vertical route is reopened",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FBR1845_1_scalar_operator_pack",
            "quantity": "Z_X;M_X2;J_X;boundary_flux_X;lambda_X",
            "required_columns": "system_id;Z_X;M_X2;J_X;boundary_flux_X;lambda_X;units;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_INPUT",
            "used_if": "scalar no-hair route selected next",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FBR1845_2_sourced_alpha_pack",
            "quantity": "K_X;Qbar_XH;qbar_XT;alpha_X(lambda)",
            "required_columns": "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_X;units;source_path;valid_for_claim",
            "current_status": "MISSING_ARENA_PROJECTION",
            "used_if": "scalar/source route remains nonzero",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FBR1845_3_edge_bound_pack",
            "quantity": "EDGEBOUND terms",
            "required_columns": "C_corner;norm_dS_Feps;norm_bX;harmonic_edge_abs;residual_edge_abs;units;source_path;valid_for_claim",
            "current_status": "MISSING_EDGE_BOUND_TERMS",
            "used_if": "boundary/edge charge route remains live",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "FBR1845_4_total_guard",
            "quantity": "absolute no-cancellation local residual envelope",
            "required_columns": "abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_R11;component_sum_abs;bound_curve;valid_for_claim",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "used_if": "any theorem-zero branch fails",
            "valid_for_claim": False,
        },
    ]


def demotion_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "demotion_id": "DEM1845_0_scope",
            "demoted_object": "current quotient/vertical no-pole route",
            "demotion": "DEMOTED_TO_CONDITIONAL_ONLY_FOR_CURRENT_MTS",
            "reason": "the single certificate fails at field-by-field v_X, action descent, matter/no-marker descent, boundary silence and degree count",
            "what_survives": "conditional theorem target for a future parent action",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "demotion_id": "DEM1845_1_scalar_operator",
            "demoted_object": "scalar no-hair fallback",
            "demotion": "PROMOTED_TO_NEXT_WORK_TARGET_NOT_CLAIM",
            "reason": "it is now the honest executable branch after quotient certificate failure",
            "what_survives": "positive energy identity if Z_X, M_X2, J_X and boundary flux are sourced",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "demotion_id": "DEM1845_2_sourced_residual",
            "demoted_object": "finite coupling/source branch",
            "demotion": "RETAINED_AS_SCOREABLE_IF_SCALAR_NOHAIR_FAILS",
            "reason": "nonzero J_X or matter coupling must be tested rather than hidden",
            "what_survives": "R10/R11 alpha/source-bound runner",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "demotion_id": "DEM1845_3_claim_ceiling",
            "demoted_object": "local-GR/R10/R11 local silence",
            "demotion": "BLOCKED",
            "reason": "no theorem-zero branch or valid source-bound branch closes",
            "what_survives": "discipline: no public/local claim from this branch yet",
            "valid_for_claim": False,
        },
    ]


def gr_bridge_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1845_0_quotient_no_pole",
            "bridge_piece": "remove local X before variation",
            "current_status": "CERTIFICATE_FAILS_CURRENT_BRANCH",
            "evidence": "QVC1845_8_verdict",
            "remaining_gap": "single parent q/v_X/action/matter/boundary/degree certificate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1845_1_coupling_zero",
            "bridge_piece": "matter and boundary coupling zero",
            "current_status": "NOT_THEOREM_ZERO",
            "evidence": "CDA1845_4_verdict",
            "remaining_gap": "constants/material markers, hidden frames, projector and boundary silence",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1845_2_scalar_nohair",
            "bridge_piece": "positive scalar no-hair fallback",
            "current_status": "NEXT_INPUT_TARGET_NOT_CLAIM",
            "evidence": "SNH1845_0_Z_X through SNH1845_5_alpha_coefficients",
            "remaining_gap": "Z_X, M_X2, J_X, boundary_flux_X, lambda_X and alpha rows",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1845_3_local_GR_Newton",
            "bridge_piece": "derived local GR/Newton reduction",
            "current_status": "BLOCKED",
            "evidence": "no quotient no-pole theorem and no scalar no-hair theorem",
            "remaining_gap": "derive theorem-zero branch or score bounded residual against local tests",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "status_id": "GB1845_4_next",
            "bridge_piece": "next derivation owner",
            "current_status": "SCALAR_NOHAIR_INPUT_PACK_OR_RESIDUAL_ALPHA_RUNNER_IS_NEXT",
            "evidence": "DEC1845_3_next_target;NEXT1845_0_primary",
            "remaining_gap": "try positive energy/no-hair route with real inputs; otherwise score residual",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1845_0_sources_registered",
            "claim": "1845 source chain exists",
            "gate_pass": False,
            "reason": "sources prove audit continuity only, not quotient closure",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1845_1_quotient_no_pole",
            "claim": "X is quotient/vertical and absent before variation",
            "gate_pass": False,
            "reason": "QVC1845_8 fails because action, matter, boundary and degree clauses are unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1845_2_coupling_zero",
            "claim": "qbar_XT=Qbar_XH=0 by descent",
            "gate_pass": False,
            "reason": "coupling descent is conditional and projector/boundary channel remains open",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1845_3_scalar_nohair",
            "claim": "scalar no-hair local silence",
            "gate_pass": False,
            "reason": "scalar input pack lacks Z_X, M_X2, J_X and boundary flux proof",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1845_4_residual_score",
            "claim": "bounded residual passes local tests",
            "gate_pass": False,
            "reason": "fallback source rows and arena projections are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1845_5_local_GR_Newton",
            "claim": "derived local GR/Newton reduction",
            "gate_pass": False,
            "reason": "neither theorem-zero nor bounded residual branch is closed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1845_0_certificate_result",
            "decision": "The q/v_X/action descent certificate does not close for the active PARENT_QLOC branch.",
            "reason": "conditional quotient pieces exist, but no field-by-field vertical action, parent action descent, matter/no-marker descent, boundary silence or degree count is signed.",
            "next_action": "do not spend no-pole credit from quotient route",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1845_1_demotion",
            "decision": "Demote the current local branch to scalar no-hair/source-coefficient work.",
            "reason": "this is the honest executable route after the quotient certificate fails in current files.",
            "next_action": "try to fill or reject Z_X, M_X2, J_X=0, boundary_flux_X=0 and alpha coefficients",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1845_2_future_reopen",
            "decision": "The quotient route can be reopened only by a real parent action certificate.",
            "reason": "future q/v_X proof would still be the cleanest local-GR route if it supplies all missing clauses together.",
            "next_action": "require q, v_X, action descent, matter descent, boundary silence and degree count in one source-backed row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1845_3_next_target",
            "decision": "Next target is scalar no-hair input pack or residual alpha coefficient runner.",
            "reason": "Z_X, M_X2, J_X=0, boundary_flux_X=0, lambda_X and alpha coefficients are now the executable local branch inputs.",
            "next_action": "1846-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1845_0_primary",
            "next_target": "1846-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md",
            "script": "scripts/Y5_R2FR_scalar_nohair_input_pack_or_residual_alpha_coefficient_runner_1846.py",
            "objective": "fill or reject the scalar no-hair input pack: Z_X, M_X^2, J_X=0, boundary_flux_X=0, lambda_X and fallback alpha coefficients with units and source paths",
            "selection_status": "selected",
            "success_condition": "positive no-hair theorem is sourced without post-hoc boundary choices, or scalar branch is demoted to explicit residual alpha rows",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1845_1_future_reopen",
            "next_target": "1846b-Y5-R2FR-parent-action-q-vX-certificate-reopen.md",
            "script": "scripts/Y5_R2FR_parent_action_q_vX_certificate_reopen_1846b.py",
            "objective": "reopen quotient route only if a single parent action supplies q, v_X, action descent, matter descent, boundary silence and degree count",
            "selection_status": "held",
            "success_condition": "one parent certificate replaces the conditional quotient ledger",
        },
    ]


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "branch_matrix": branch_matrix_rows(),
        "qvx_certificate": qvx_certificate_rows(),
        "coupling_audit": coupling_audit_rows(),
        "scalar_input_pack": scalar_input_pack_rows(),
        "fallback_source_rows": fallback_source_rows(),
        "demotion": demotion_rows(),
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
            RAB_QUEUE / f"JR1845_{key.upper()}.csv",
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
        if not (RAB_QUEUE / f"JR1845_{key.upper()}.csv").exists():
            return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = [
        "1845-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1845",
        "P8_Y5_BRR545_1845",
        "Y5_R2FR_vertical_quotient_LX_construction_or_scalar_nohair_branch_choice_1845",
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
        ("VAL1845_0_sources_exist", all(row["exists"] is True for row in source_rows), "all cited source paths exist"),
        ("VAL1845_1_needles_present", all(row["needles_present"] is True for row in source_rows), "all cited source needles are present"),
        (
            "VAL1845_2_branch_matrix_demotes",
            any(row["matrix_id"] == "BDM1845_0_vertical_quotient" and row["current_status"] == "TESTED_NOT_CLOSED" for row in rows_map["branch_matrix"]),
            "branch matrix tests quotient first but does not claim it",
        ),
        (
            "VAL1845_3_qvx_certificate_blocks_claim",
            any(row["certificate_id"] == "QVC1845_8_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM_DEMOTE_CURRENT_BRANCH" for row in rows_map["qvx_certificate"]),
            "q/v_X/action certificate fails current claim",
        ),
        (
            "VAL1845_4_coupling_not_theorem_zero",
            any(row["audit_id"] == "CDA1845_4_verdict" and row["result"] == "COUPLING_NOT_THEOREM_ZERO" for row in rows_map["coupling_audit"]),
            "coupling descent remains nonzero/nonclaim",
        ),
        (
            "VAL1845_5_scalar_pack_nonclaim",
            {"SNH1845_0_Z_X", "SNH1845_1_M_X2", "SNH1845_2_J_X_zero", "SNH1845_3_boundary_flux_zero"}.issubset({row["input_id"] for row in rows_map["scalar_input_pack"]})
            and all(row["valid_for_claim"] is False for row in rows_map["scalar_input_pack"]),
            "scalar no-hair input pack exists and remains nonclaim",
        ),
        (
            "VAL1845_6_fallback_rows_nonclaim",
            {"FBR1845_0_quotient_certificate", "FBR1845_1_scalar_operator_pack", "FBR1845_4_total_guard"}.issubset({row["row_id"] for row in rows_map["fallback_source_rows"]})
            and all(row["valid_for_claim"] is False for row in rows_map["fallback_source_rows"]),
            "fallback source rows are explicit and nonclaim",
        ),
        (
            "VAL1845_7_demotion_complete",
            any(row["demotion_id"] == "DEM1845_0_scope" and row["demotion"] == "DEMOTED_TO_CONDITIONAL_ONLY_FOR_CURRENT_MTS" for row in rows_map["demotion"])
            and any(row["demotion_id"] == "DEM1845_1_scalar_operator" and row["demotion"] == "PROMOTED_TO_NEXT_WORK_TARGET_NOT_CLAIM" for row in rows_map["demotion"]),
            "demotion ledger covers quotient and scalar fallback",
        ),
        (
            "VAL1845_8_bridge_next_selected",
            any(row["status_id"] == "GB1845_4_next" and row["current_status"] == "SCALAR_NOHAIR_INPUT_PACK_OR_RESIDUAL_ALPHA_RUNNER_IS_NEXT" for row in rows_map["gr_bridge"]),
            "bridge status selects scalar no-hair/residual runner next",
        ),
        (
            "VAL1845_9_claim_gates_blocked",
            all(row["gate_pass"] is False and row["claim_allowed"] is False for row in rows_map["claim_gate"]),
            "all claim gates remain blocked",
        ),
        (
            "VAL1845_10_decision_next",
            any(row["decision_id"] == "DEC1845_3_next_target" and "scalar no-hair" in row["decision"] for row in rows_map["decision"]),
            "decision ledger selects scalar no-hair input pack next",
        ),
        (
            "VAL1845_11_next_target_selected",
            any(row["route_id"] == "NEXT1845_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1845_12_no_claim_flags", no_claim_flags(rows_map), "no claim flags are true"),
        ("VAL1845_13_missing_rows_nonclaim", missing_rows_not_ready(rows_map), "MISSING_* rows stay nonclaim"),
        ("VAL1845_14_csv_parse", csv_parse_all(), "all generated 1845 CSVs parse"),
        ("VAL1845_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1845_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1845_17_formalization_untouched", no_formalization_outputs(), "no 1845 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1845_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1845 vertical quotient L_X construction or scalar no-hair branch choice",
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
            "# 1845 Y5 R2FR vertical quotient L_X construction or scalar no-hair branch choice",
            "",
            "**Progress:** 1845 takes the clean route seriously: try to make the local `X` branch disappear before variation by quotient/vertical descent. The attempt is now explicit in the active parent-q_loc branch, not just inherited from the old R10 trail.",
            "",
            "**Current verdict:** the single `q/v_X/action` certificate still does not close. Metric/frame chain-rule pieces are promising conditionally, but field-by-field vertical action, parent action descent, matter/no-marker descent, boundary silence, and degree count are not signed together.",
            "",
            "**Claim ceiling:** no quotient no-pole theorem, no coupling-zero theorem, no scalar no-hair theorem, no R10/R11 pass, no PPN pass, no local-GR/Newton reduction, no GitHub action, and no `formalization-workbench` edit is allowed from 1845.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Branch Decision Matrix",
            markdown_table(rows_map["branch_matrix"], ["matrix_id", "candidate", "core_test", "scrutiny_level", "current_status", "missing", "decision", "claim_allowed", "valid_for_claim"]),
            "",
            "## q/v_X Action Descent Certificate",
            markdown_table(rows_map["qvx_certificate"], ["certificate_id", "required_object", "pass_condition", "current_evidence", "current_status", "missing_for_claim", "claim_effect_if_signed", "valid_for_claim"]),
            "",
            "## Coupling Descent Audit",
            markdown_table(rows_map["coupling_audit"], ["audit_id", "object", "result", "reason", "remaining_coupling", "demotion_effect", "valid_for_claim"]),
            "",
            "## Scalar No-Hair Input Pack",
            markdown_table(rows_map["scalar_input_pack"], ["input_id", "quantity", "needed_for", "required_source", "current_status", "if_missing", "valid_for_claim"]),
            "",
            "## Fallback Source Rows",
            markdown_table(rows_map["fallback_source_rows"], ["row_id", "quantity", "required_columns", "current_status", "used_if", "valid_for_claim"]),
            "",
            "## Demotion Ledger",
            markdown_table(rows_map["demotion"], ["demotion_id", "demoted_object", "demotion", "reason", "what_survives", "valid_for_claim"]),
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
            "This is the least flattering but most useful answer: the clean quotient move is still the best theoretical route, but current MTS cannot spend that credit yet. So the next honest derivation is the positive-energy/no-hair branch: prove the scalar operator is positive and source-free, or admit a residual coupling and score it. That is how we avoid smuggling GR in through a hidden closure axiom.",
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
    print(f"1845 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
