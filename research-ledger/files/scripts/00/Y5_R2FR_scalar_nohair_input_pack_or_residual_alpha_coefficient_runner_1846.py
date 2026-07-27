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
QUARANTINE = MICROSCOPE / "quarantine" / "1846"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1846-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1846_0_1845_next",
        "source_key": "1845_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1845_NEXT_TARGET.csv",
        "needles": ["NEXT1845_0_primary", "1846-Y5-R2FR-scalar-nohair"],
        "role": "1845 selects scalar no-hair input pack or residual alpha runner.",
    },
    {
        "source_id": "SRC1846_1_1845_validation",
        "source_key": "1845_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1845_VALIDATION.csv",
        "needles": ["VAL1845_OVERALL", "PASS"],
        "role": "confirms 1845 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1846_2_1845_scalar_pack",
        "source_key": "1845_scalar_input_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1845_SCALAR_NOHAIR_INPUT_PACK.csv",
        "needles": ["SNH1845_0_Z_X", "MISSING_PARENT_INPUT"],
        "role": "1845 lists the missing scalar no-hair inputs in the active parent branch.",
    },
    {
        "source_id": "SRC1846_3_1024_scalar_assessment",
        "source_key": "1024_scalar_input_assessment",
        "source_path": RESIDUALS / "P8_Y5_R10_1024_SCALAR_INPUT_ASSESSMENT.csv",
        "needles": ["SIA1024_6_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1024 establishes the scalar no-hair input failure pattern.",
    },
    {
        "source_id": "SRC1846_4_1024_alpha_refusal",
        "source_key": "1024_alpha_runner_refusal",
        "source_path": RESIDUALS / "P8_Y5_R10_1024_ALPHA_RUNNER_REFUSAL.csv",
        "needles": ["RUN1024_6_verdict", "refused_no_claim"],
        "role": "1024 stages the residual alpha runner but refuses claims.",
    },
    {
        "source_id": "SRC1846_5_1042_nohair_identity",
        "source_key": "1042_positive_nohair_identity",
        "source_path": RESIDUALS / "P8_Y5_R10_1042_POSITIVE_X_NOHAIR_IDENTITY.csv",
        "needles": ["NH1042_5_verdict", "four owner premises"],
        "role": "1042 gives the exact conditional positive no-hair identity.",
    },
    {
        "source_id": "SRC1846_6_1092_nohair_audit",
        "source_key": "1092_scalar_nohair_route_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1092_SCALAR_NOHAIR_ROUTE_AUDIT.csv",
        "needles": ["SNH1092_4_verdict", "NOHAIR_ROUTE_UNSIGNED"],
        "role": "1092 sharpens the no-hair route into owner/sign/source/boundary gates.",
    },
    {
        "source_id": "SRC1846_7_1093_parent_owner",
        "source_key": "1093_parent_scalar_owner",
        "source_path": RESIDUALS / "P8_Y5_R10_1093_PARENT_SCALAR_OWNER_ATTEMPT.csv",
        "needles": ["OWN1093_4_verdict", "PARENT_OWNER_NOT_DERIVED"],
        "role": "1093 shows the dangerous scalar owner is still not derived.",
    },
    {
        "source_id": "SRC1846_8_1093_operator_pack",
        "source_key": "1093_positive_operator_pack",
        "source_path": RESIDUALS / "P8_Y5_R10_1093_POSITIVE_OPERATOR_INPUT_PACK.csv",
        "needles": ["OP1093_4_verdict", "OPERATOR_PACK_UNSIGNED"],
        "role": "1093 shows the positive operator pack remains unsigned.",
    },
    {
        "source_id": "SRC1846_9_1093_source_silence",
        "source_key": "1093_source_silence",
        "source_path": RESIDUALS / "P8_Y5_R10_1093_SOURCE_SILENCE_AUDIT.csv",
        "needles": ["JX1093_4_verdict", "SOURCE_SILENCE_NOT_DERIVED"],
        "role": "1093 shows source-free no-hair premises remain unsigned.",
    },
    {
        "source_id": "SRC1846_10_1093_doc_theorem",
        "source_key": "1093_exact_conditional_theorem",
        "source_path": ROOT / "1093-Y5-R10-scalar-nohair-input-owner-or-balpha-tau-projection-source.md",
        "needles": ["THM1093_2_zero_result", "EXACT_CONDITIONAL_THEOREM"],
        "role": "1093 records the zero result as exact conditional math, not an active MTS claim.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_SOURCE_REGISTER.csv",
    "scalar_input_assessment": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_SCALAR_INPUT_ASSESSMENT.csv",
    "positive_nohair_contract": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_POSITIVE_NOHAIR_CONTRACT.csv",
    "parent_owner_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_PARENT_SCALAR_OWNER_AUDIT.csv",
    "operator_pack": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_POSITIVE_OPERATOR_PACK.csv",
    "source_silence": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_SOURCE_SILENCE_AUDIT.csv",
    "alpha_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_ALPHA_COEFFICIENT_ROWS.csv",
    "alpha_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_ALPHA_RUNNER_REFUSAL.csv",
    "branch_verdicts": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_BRANCH_VERDICTS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1846_VALIDATION.csv",
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


def scalar_input_assessment_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "SIA1846_0_operator_domain",
            "quantity": "O_X self-adjoint positive operator",
            "required_condition": "O_X=-nabla_i(Z_X nabla^i)+M_X^2 on compact source-free exterior with owned local domain",
            "current_evidence": "positive identity exists as mathematics; parent operator/domain not owned",
            "current_status": "TEMPLATE_ONLY",
            "missing_for_claim": "parent operator, field units, self-adjoint domain and boundary class",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SIA1846_1_parent_owner",
            "quantity": "same Xhat owns visible coefficients and no-hair equation",
            "required_condition": "one parent-normalized Xhat controls dangerous coupling and obeys L_X Xhat=J_X",
            "current_evidence": "1093 owner audit finds closure-coordinate and theorem-target candidates only",
            "current_status": "PARENT_OWNER_NOT_DERIVED",
            "missing_for_claim": "identify Xhat as action-owned parent field rather than closure coordinate",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SIA1846_2_Z_X",
            "quantity": "Z_X>0",
            "required_condition": "second variation fixes positive kinetic residue with normalization and units",
            "current_evidence": "operator pack has formula language but no parent-signed Hessian",
            "current_status": "MISSING_PARENT_INPUT",
            "missing_for_claim": "parent Hessian, sign convention, field normalization and units",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SIA1846_3_M_X2_lambda",
            "quantity": "M_X^2>0 and lambda_X",
            "required_condition": "mass gap is positive and lambda_X=sqrt(Z_X/M_X^2) has source-backed length units",
            "current_evidence": "mass gap and range remain formula-only",
            "current_status": "MISSING_PARENT_INPUT",
            "missing_for_claim": "parent Hessian curvature, zero-mode handling and range units",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SIA1846_4_J_X_zero",
            "quantity": "J_X=0",
            "required_condition": "ordinary matter plus hidden/source/domain terms are X-blind channel-by-channel",
            "current_evidence": "source silence audit keeps ordinary matter, alpha, WEP, R10 and readout channels live",
            "current_status": "MISSING_SOURCE_ZERO_PROOF",
            "missing_for_claim": "matter quotient/no-marker theorem or explicit source-current bounds",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SIA1846_5_boundary_flux_zero",
            "quantity": "boundary_flux_X=0",
            "required_condition": "boundary flux is zero/proper/exact or source-backed bounded",
            "current_evidence": "1843-1844 leave B_X/EDGEBOUND/projector terms unsigned",
            "current_status": "MISSING_BOUNDARY_LOCK",
            "missing_for_claim": "boundary class, no-hair/projector silence or flux bound",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SIA1846_6_energy_identity",
            "quantity": "positive energy identity",
            "required_condition": "int_A(Z_X|grad X|^2+M_X^2 X^2+positive_mix)=int_A XJ_X+Phi_boundary",
            "current_evidence": "1042/1093 prove the math conditionally",
            "current_status": "CONDITIONAL_MATH_VALID",
            "missing_for_claim": "SIA1846_0 through SIA1846_5 together",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "SIA1846_7_verdict",
            "quantity": "scalar no-hair theorem",
            "required_condition": "all scalar input rows parent-signed or source-bounded with zero RHS",
            "current_evidence": "the theorem contract is exact, but every physical owner premise is unsigned",
            "current_status": "FAIL_CURRENT_CLAIM",
            "missing_for_claim": "operator, parent owner, Z_X, M_X^2, J_X=0, boundary_flux_X=0 and no zero-mode gate",
            "valid_for_claim": False,
        },
    ]


def positive_nohair_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHC1846_0_operator_setup",
            "step": "retained scalar mode equation",
            "mathematical_statement": "Let Xhat be the parent-owned retained local mode on compact exterior A with L_X Xhat=J_X.",
            "status": "CONDITIONAL_CONTRACT",
            "consequence": "only applies if Xhat is the same parent field that controls visible coefficients",
            "math_valid": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHC1846_1_energy_identity",
            "step": "multiply by Xhat and integrate",
            "mathematical_statement": "int_A[Z_X^{mu nu} nabla_mu Xhat nabla_nu Xhat+M_X^2 Xhat^2+positive_mix] = int_A Xhat J_X + Phi_boundary",
            "status": "EXACT_CONDITIONAL_IDENTITY",
            "consequence": "turns local silence into sign/source/boundary premises rather than a plateau axiom",
            "math_valid": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHC1846_2_zero_result",
            "step": "set RHS to zero with positive gap/no zero mode",
            "mathematical_statement": "Z_X>=Z_min>0, M_X^2>=m_min^2>0, J_X=0, Phi_boundary=0 and no zero mode imply Xhat=0 on A.",
            "status": "EXACT_CONDITIONAL_THEOREM",
            "consequence": "would silence the scalar local branch and reopen local-GR route if parent-signed",
            "math_valid": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHC1846_3_failure_branch",
            "step": "any premise fails",
            "mathematical_statement": "alpha_X(lambda_X)=K_X Qbar_XH qbar_XT plus edge and FB5540 absolute guard",
            "status": "FINITE_RESIDUAL_BRANCH",
            "consequence": "local tests score the residual instead of accepting a closure",
            "math_valid": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "theorem_id": "NHC1846_4_verdict",
            "step": "MTS no-hair status",
            "mathematical_statement": "positive no-hair theorem is derived as mathematics but not activated for MTS",
            "status": "CONDITIONAL_THEOREM_NOT_MTS_CLAIM",
            "consequence": "must derive parent owner/operator/source/boundary clauses first",
            "math_valid": True,
            "valid_for_claim": False,
        },
    ]


def parent_owner_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN1846_0_target",
            "candidate_owner": "parent scalar Xhat/I controlling visible coefficients",
            "needed_identity": "d ln(c_visible)=b_X dXhat and the same Xhat enters L_X Xhat=J_X",
            "current_status": "TARGET_SHARP",
            "why_not_closed": "not yet identified as a parent field rather than a closure coordinate",
            "if_closed": "clock, WEP, R10 and local-GR residuals can share one normalization",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN1846_1_chiX",
            "candidate_owner": "chi_X finite alpha-pressure coordinate",
            "needed_identity": "chi_X is a parent-owned local field with units and action normalization",
            "current_status": "CLOSURE_COORDINATE_ONLY",
            "why_not_closed": "visible coefficient response is defined but not tied to parent state variation",
            "if_closed": "could feed no-hair operator and alpha/WEP projection",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN1846_2_vertical_norm",
            "candidate_owner": "parent vertical norm or quotient-fixed scalar",
            "needed_identity": "visible scalar pressure equals a vertical-norm response or quotient-fixed observable",
            "current_status": "NOT_DERIVED",
            "why_not_closed": "vertical quotient certificate failed in 1845",
            "if_closed": "could reopen quotient no-pole route rather than scalar no-hair",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN1846_3_clock_coframe",
            "candidate_owner": "clock/coframe scalar",
            "needed_identity": "same signed scalar controls observed clock/redshift maps and local source equation",
            "current_status": "THEOREM_TARGET_NOT_DERIVED",
            "why_not_closed": "clock scalar is not parent-derived and may be gauge/closure if not action-owned",
            "if_closed": "could connect clock and local no-hair routes",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "owner_id": "OWN1846_4_verdict",
            "candidate_owner": "unique parent owner for dangerous scalar coefficient",
            "needed_identity": "one parent-normalized Xhat controls visible coefficients and obeys the no-hair operator",
            "current_status": "PARENT_OWNER_NOT_DERIVED",
            "why_not_closed": "all candidates are closure coordinates, conditional quotient targets, or unsigned theorem targets",
            "if_closed": "would unlock the positive no-hair identity as a local-GR route",
            "valid_for_claim": False,
        },
    ]


def operator_pack_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "OP1846_0_LX_owner",
            "required_input": "parent L_X selected from second variation",
            "mathematical_role": "defines the self-adjoint operator acting on the same Xhat that controls visible coefficients",
            "current_status": "MISSING_PARENT_LX",
            "source_basis": "NHC1846_0_operator_setup;SIA1846_0_operator_domain",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "OP1846_1_Z_positive",
            "required_input": "Z_X positive kinetic matrix",
            "mathematical_role": "makes int Z_X |grad X|^2 nonnegative",
            "current_status": "FORMULA_ONLY_NOT_PARENT_SIGNED",
            "source_basis": "SIA1846_2_Z_X",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "OP1846_2_mass_gap",
            "required_input": "M_X^2 positive gap or justified zero-mode handling",
            "mathematical_role": "removes long-range scalar zero mode from local exterior",
            "current_status": "FORMULA_ONLY_NOT_PARENT_SIGNED",
            "source_basis": "SIA1846_3_M_X2_lambda",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "OP1846_3_self_adjoint_domain",
            "required_input": "self-adjoint local domain and boundary class",
            "mathematical_role": "permits integration by parts without hidden leakage",
            "current_status": "MISSING_DOMAIN_SIGNATURE",
            "source_basis": "SIA1846_0_operator_domain;SIA1846_5_boundary_flux_zero",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "OP1846_4_verdict",
            "required_input": "claim-grade positive operator pack",
            "mathematical_role": "supports positive no-hair identity for MTS rather than generic math",
            "current_status": "OPERATOR_PACK_UNSIGNED",
            "source_basis": "NHC1846_4_verdict",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
    ]


def source_silence_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "silence_id": "JX1846_0_matter",
            "channel": "ordinary matter/source current",
            "needed_zero": "J_X^matter=0",
            "current_status": "CONDITIONAL_ON_PARENT_MATTER_SIGNATURE",
            "obstruction": "ordinary matter signature/descent is not parent-signed in active branch",
            "finite_fallback": "J_X_bound source row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "silence_id": "JX1846_1_visible_coefficients",
            "channel": "alpha/EM/clock visible coefficient",
            "needed_zero": "partial_X ln(c_visible)=0 or parent-owned coefficient with no local source",
            "current_status": "NOT_DERIVED",
            "obstruction": "dangerous scalar owner and no-extra-coupling theorem remain unsigned",
            "finite_fallback": "b_visible or product source row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "silence_id": "JX1846_2_WEP_source",
            "channel": "WEP/source/test material projection",
            "needed_zero": "material response product is zero or bounded",
            "current_status": "PROJECTION_NOT_DERIVED",
            "obstruction": "source worldtube, material tensor and Xhat normalization are not jointly owned",
            "finite_fallback": "direct WEP product row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "silence_id": "JX1846_3_R10_source",
            "channel": "R10/Yukawa projection",
            "needed_zero": "beta_s beta_t K_X/Z_X tau_R10=0 or bounded alpha(lambda)",
            "current_status": "PROJECTION_NOT_DERIVED",
            "obstruction": "tau_R10, K_X/Z_X and lambda_X remain template rows",
            "finite_fallback": "alpha_X(lambda) source row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "silence_id": "JX1846_4_verdict",
            "channel": "source-free no-hair premise",
            "needed_zero": "J_X=0 channelwise",
            "current_status": "SOURCE_SILENCE_NOT_DERIVED",
            "obstruction": "ordinary matter, visible coefficients, WEP, R10, boundary and readout channels are not all parent-silenced",
            "finite_fallback": "residual coefficient/product runner",
            "valid_for_claim": False,
        },
    ]


def alpha_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ALPHA1846_0_bulk_operator",
            "quantity": "Z_X;M_X2;lambda_X",
            "formula": "lambda_X=sqrt(Z_X/M_X2)",
            "required_columns": "system_id;field_id;Z_X;M_X2;lambda_X;Z_units;M_units;lambda_units;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_INPUT",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ALPHA1846_1_source_current",
            "quantity": "J_X or J_X_bound",
            "formula": "O_X X=J_X",
            "required_columns": "system_id;J_X;J_X_bound;source_channel;units;source_path;valid_for_claim",
            "current_status": "MISSING_SOURCE_ZERO_PROOF",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ALPHA1846_2_boundary_flux",
            "quantity": "boundary_flux_X or boundary_flux_bound",
            "formula": "Phi_boundary=int_boundary X Z_X n.grad X plus edge/projector terms",
            "required_columns": "system_id;boundary_flux_X;boundary_flux_bound;boundary_rule;units;source_path;valid_for_claim",
            "current_status": "MISSING_BOUNDARY_LOCK",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ALPHA1846_3_bulk_R10_projection",
            "quantity": "K_X;Qbar_XH;qbar_XT",
            "formula": "alpha_bulk(lambda_X)=K_X Qbar_XH qbar_XT",
            "required_columns": "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_bulk;normalization;units;source_path;valid_for_claim",
            "current_status": "MISSING_ARENA_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ALPHA1846_4_edge_projection",
            "quantity": "lambda_edge;K_edge;Qbar_edge_XH;qbar_XT",
            "formula": "alpha_edge(lambda_edge)=K_edge Qbar_edge_XH qbar_XT",
            "required_columns": "system_id;lambda_edge;K_edge;Qbar_edge_XH;qbar_XT;alpha_edge;units;source_path;valid_for_claim",
            "current_status": "MISSING_EDGE_PROJECTION",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ALPHA1846_5_no_cancellation_guard",
            "quantity": "alpha_total_guard",
            "formula": "abs_alpha_total=|alpha_bulk|+|alpha_edge|+|epsilon_FB5540|+|alpha_R11|",
            "required_columns": "system_id;lambda;abs_alpha_bulk;abs_alpha_edge;abs_FB5540;abs_alpha_R11;component_sum_abs;bound;source_path;valid_for_claim",
            "current_status": "NOT_COMPUTED_COMPONENTS_MISSING",
            "valid_for_claim": False,
        },
    ]


def alpha_refusal_rows() -> list[dict[str, Any]]:
    reasons = {
        "RUN1846_0_bulk_operator": ("ALPHA1846_0_bulk_operator", "blocked_missing_operator_inputs", "MISSING_PARENT_INPUT;VALID_FOR_CLAIM_FALSE"),
        "RUN1846_1_source_current": ("ALPHA1846_1_source_current", "blocked_missing_source_zero_or_bound", "MISSING_SOURCE_ZERO_PROOF;VALID_FOR_CLAIM_FALSE"),
        "RUN1846_2_boundary_flux": ("ALPHA1846_2_boundary_flux", "blocked_missing_boundary_flux_zero_or_bound", "MISSING_BOUNDARY_LOCK;VALID_FOR_CLAIM_FALSE"),
        "RUN1846_3_bulk_R10_projection": ("ALPHA1846_3_bulk_R10_projection", "blocked_missing_alpha_projection_inputs", "MISSING_ARENA_PROJECTION;VALID_FOR_CLAIM_FALSE"),
        "RUN1846_4_edge_projection": ("ALPHA1846_4_edge_projection", "blocked_missing_edge_projection_inputs", "MISSING_EDGE_PROJECTION;VALID_FOR_CLAIM_FALSE"),
        "RUN1846_5_no_cancellation_guard": ("ALPHA1846_5_no_cancellation_guard", "blocked_missing_no_cancellation_components", "NOT_COMPUTED_COMPONENTS_MISSING;VALID_FOR_CLAIM_FALSE"),
        "RUN1846_6_verdict": ("ALPHA1846_VERDICT", "REFUSED_NO_CLAIM", "SCALAR_NOHAIR_INPUTS_MISSING;ALPHA_COMPONENTS_MISSING;VALID_FOR_CLAIM_FALSE"),
    }
    rows: list[dict[str, Any]] = []
    for runner_id, (row_id, status, failure_reasons) in reasons.items():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "runner_id": runner_id,
                "row_id": row_id,
                "computed_status": status,
                "claim_allowed": False,
                "failure_reasons": failure_reasons,
                "valid_for_claim": False,
            }
        )
    return rows


def branch_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1846_0_scalar_zero",
            "branch": "scalar no-hair theorem",
            "status": "FAIL_CURRENT_CLAIM",
            "because": "parent owner, Z_X, M_X2, J_X=0, boundary_flux_X=0, zero-mode and units are not parent-signed",
            "allowed_statement": "positive energy identity is an exact conditional theorem target only",
            "next_action": "try parent Xhat owner and Hessian/range extraction",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1846_1_residual_alpha",
            "branch": "residual alpha scorer",
            "status": "SCHEMA_READY_RUNNER_REFUSES",
            "because": "K_X, Qbar_XH, qbar_XT, lambda_X, edge terms and total guard are missing",
            "allowed_statement": "alpha rows are ready as nonclaim placeholders only",
            "next_action": "fill first parent owner/Hessian/range row before alpha scoring",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1846_2_coupling_status",
            "branch": "coupling suspicion",
            "status": "CONFIRMED_AS_LIVE_GAP",
            "because": "J_X, qbar_XT, Qbar_XH and edge projection are exact coupling/source places where local tests bite",
            "allowed_statement": "coupling is now a concrete input class, not a vague objection",
            "next_action": "after owner/Z/M, attack J_X=0 or source product with paths",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1846_3_next_target",
            "branch": "next target",
            "status": "PARENT_OWNER_AND_HESSIAN_FIRST",
            "because": "without a parent Xhat and Z_X/M_X2, neither no-hair nor alpha(lambda) can be normalized",
            "allowed_statement": "operator/range owner is the next least-fake derivation target",
            "next_action": "1847-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1846_0_sources_registered",
            "claim": "1846 source chain exists",
            "gate_pass": False,
            "reason": "sources prove audit continuity only, not no-hair activation",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1846_1_parent_owner",
            "claim": "dangerous scalar is parent-owned",
            "gate_pass": False,
            "reason": "OWN1846_4_verdict=PARENT_OWNER_NOT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1846_2_positive_operator",
            "claim": "positive self-adjoint operator applies to MTS",
            "gate_pass": False,
            "reason": "OP1846_4_verdict=OPERATOR_PACK_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1846_3_source_silence",
            "claim": "J_X=0 channelwise",
            "gate_pass": False,
            "reason": "JX1846_4_verdict=SOURCE_SILENCE_NOT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1846_4_boundary_flux_zero",
            "claim": "boundary_flux_X=0",
            "gate_pass": False,
            "reason": "boundary class/no-hair/projector silence remains unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1846_5_scalar_nohair_claim",
            "claim": "scalar no-hair theorem closes local branch",
            "gate_pass": False,
            "reason": "exact conditional theorem lacks parent owner/operator/source/boundary premises",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1846_6_alpha_runner_claim",
            "claim": "residual alpha row can be scored",
            "gate_pass": False,
            "reason": "alpha runner refusal blocks all rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1846_0_scalar_result",
            "decision": "Scalar no-hair cannot be claimed from current inputs.",
            "because": "the energy identity is exact conditional math, but all physical owner/sign/source/boundary inputs are missing or unsigned.",
            "next_action": "keep no-hair as theorem contract, not evidence",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1846_1_runner_result",
            "decision": "Residual alpha runner is staged but refuses all claims.",
            "because": "operator/range, source, projection, edge and total guard rows are missing.",
            "next_action": "fill first parent owner/Hessian/range row before alpha scoring",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1846_2_coupling",
            "decision": "The coupling gap is now concrete.",
            "because": "J_X, qbar_XT, Qbar_XH and edge projection are the exact coupling/source places where local tests bite.",
            "next_action": "after parent owner/Z_X/M_X2, attack J_X=0 or qbar_XT/product row with source paths",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1846_3_next_target",
            "decision": "Next target is parent Xhat owner plus Hessian signs and range.",
            "because": "without the same parent Xhat and Z_X/M_X2, neither no-hair nor alpha(lambda) can be normalized.",
            "next_action": "1847-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1846_0_primary",
            "next_target": "1847-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md",
            "script": "scripts/Y5_R2FR_parent_Xhat_owner_and_Hessian_ZX_MX2_range_or_alpha_source_row_1847.py",
            "objective": "derive or source the parent Xhat owner, Hessian signs, field units, M_X^2, lambda_X and first fallback alpha/source row if the Hessian cannot be owned",
            "selection_status": "selected",
            "success_condition": "one parent-owned scalar/operator row supplies Xhat, Z_X, M_X2 and lambda_X, or the branch is explicitly demoted to sourced residual coefficients",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1846_1_parallel",
            "next_target": "1847b-Y5-R2FR-direct-WEP-or-R10-product-source-pack.md",
            "script": "scripts/Y5_R2FR_direct_WEP_or_R10_product_source_pack_1847b.py",
            "objective": "construct a direct finite product source pack if parent owner/Hessian extraction fails",
            "selection_status": "held",
            "success_condition": "direct product rows avoid tau=1 shortcuts, clock-to-WEP transfers and factor division without sources",
        },
    ]


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "scalar_input_assessment": scalar_input_assessment_rows(),
        "positive_nohair_contract": positive_nohair_contract_rows(),
        "parent_owner_audit": parent_owner_audit_rows(),
        "operator_pack": operator_pack_rows(),
        "source_silence": source_silence_rows(),
        "alpha_rows": alpha_rows(),
        "alpha_refusal": alpha_refusal_rows(),
        "branch_verdicts": branch_verdict_rows(),
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
            RAB_QUEUE / f"JR1846_{key.upper()}.csv",
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
        if not (RAB_QUEUE / f"JR1846_{key.upper()}.csv").exists():
            return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = [
        "1846-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1846",
        "P8_Y5_BRR545_1846",
        "Y5_R2FR_scalar_nohair_input_pack_or_residual_alpha_coefficient_runner_1846",
    ]
    return not any(any(marker in path.name for marker in markers) for path in FORMALIZATION.rglob("*"))


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    for key, rows in rows_map.items():
        if key == "source_register":
            continue
        for row in rows:
            for field in ["valid_for_claim", "claim_allowed", "gate_pass", "score_ready", "pass_for_claim"]:
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
            for field in ["valid_for_claim", "claim_allowed", "score_ready", "pass_for_claim"]:
                if row.get(field) is True:
                    return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    source_rows = rows_map["source_register"]
    checks = [
        ("VAL1846_0_sources_exist", all(row["exists"] is True for row in source_rows), "all cited source paths exist"),
        ("VAL1846_1_needles_present", all(row["needles_present"] is True for row in source_rows), "all cited source needles are present"),
        (
            "VAL1846_2_scalar_verdict_blocks_claim",
            any(row["input_id"] == "SIA1846_7_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in rows_map["scalar_input_assessment"]),
            "scalar no-hair theorem remains nonclaim",
        ),
        (
            "VAL1846_3_conditional_theorem_written",
            any(row["theorem_id"] == "NHC1846_2_zero_result" and row["status"] == "EXACT_CONDITIONAL_THEOREM" for row in rows_map["positive_nohair_contract"]),
            "exact conditional no-hair theorem is written",
        ),
        (
            "VAL1846_4_parent_owner_blocks",
            any(row["owner_id"] == "OWN1846_4_verdict" and row["current_status"] == "PARENT_OWNER_NOT_DERIVED" for row in rows_map["parent_owner_audit"]),
            "parent scalar owner remains unsigned",
        ),
        (
            "VAL1846_5_operator_pack_blocks",
            any(row["input_id"] == "OP1846_4_verdict" and row["current_status"] == "OPERATOR_PACK_UNSIGNED" for row in rows_map["operator_pack"]),
            "positive operator pack remains unsigned",
        ),
        (
            "VAL1846_6_source_silence_blocks",
            any(row["silence_id"] == "JX1846_4_verdict" and row["current_status"] == "SOURCE_SILENCE_NOT_DERIVED" for row in rows_map["source_silence"]),
            "source silence remains unsigned",
        ),
        (
            "VAL1846_7_alpha_runner_refuses",
            any(row["runner_id"] == "RUN1846_6_verdict" and row["computed_status"] == "REFUSED_NO_CLAIM" for row in rows_map["alpha_refusal"]),
            "residual alpha runner refuses all claims",
        ),
        (
            "VAL1846_8_branch_next_selected",
            any(row["verdict_id"] == "BV1846_3_next_target" and row["status"] == "PARENT_OWNER_AND_HESSIAN_FIRST" for row in rows_map["branch_verdicts"]),
            "branch verdict selects parent owner/Hessian first",
        ),
        (
            "VAL1846_9_claim_gates_blocked",
            all(row["gate_pass"] is False and row["claim_allowed"] is False for row in rows_map["claim_gate"]),
            "all claim gates remain blocked",
        ),
        (
            "VAL1846_10_decision_next",
            any(row["decision_id"] == "DEC1846_3_next_target" and "parent Xhat" in row["decision"] for row in rows_map["decision"]),
            "decision ledger selects parent Xhat/Hessian target",
        ),
        (
            "VAL1846_11_next_target_selected",
            any(row["route_id"] == "NEXT1846_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1846_12_no_claim_flags", no_claim_flags(rows_map), "no claim flags are true"),
        ("VAL1846_13_missing_rows_nonclaim", missing_rows_not_ready(rows_map), "MISSING_* rows stay nonclaim"),
        ("VAL1846_14_csv_parse", csv_parse_all(), "all generated 1846 CSVs parse"),
        ("VAL1846_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1846_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1846_17_formalization_untouched", no_formalization_outputs(), "no 1846 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1846_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1846 scalar no-hair input pack or residual alpha coefficient runner",
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
            "# 1846 Y5 R2FR scalar no-hair input pack or residual alpha coefficient runner",
            "",
            "**Progress:** 1846 proves the no-hair route as an exact conditional contract: a parent-owned scalar with positive self-adjoint operator, source silence, boundary silence, and no zero mode would vanish in the local exterior. That is the derivable version of the local plateau idea.",
            "",
            "**Current verdict:** the theorem is not an active MTS claim. Current files do not yet own the parent scalar `Xhat`, `Z_X`, `M_X^2`, `J_X=0`, `boundary_flux_X=0`, `lambda_X`, or the residual alpha coefficients. The alpha runner is staged and refuses all claims.",
            "",
            "**Claim ceiling:** no scalar no-hair theorem, no residual alpha pass, no R10/R11 pass, no PPN pass, no local-GR/Newton reduction, no GitHub action, and no `formalization-workbench` edit is allowed from 1846.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Scalar Input Assessment",
            markdown_table(rows_map["scalar_input_assessment"], ["input_id", "quantity", "required_condition", "current_evidence", "current_status", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Positive No-Hair Contract",
            markdown_table(rows_map["positive_nohair_contract"], ["theorem_id", "step", "mathematical_statement", "status", "consequence", "math_valid", "valid_for_claim"]),
            "",
            "## Parent Scalar Owner Audit",
            markdown_table(rows_map["parent_owner_audit"], ["owner_id", "candidate_owner", "needed_identity", "current_status", "why_not_closed", "if_closed", "valid_for_claim"]),
            "",
            "## Positive Operator Pack",
            markdown_table(rows_map["operator_pack"], ["input_id", "required_input", "mathematical_role", "current_status", "source_basis", "blocks_claim", "valid_for_claim"]),
            "",
            "## Source Silence Audit",
            markdown_table(rows_map["source_silence"], ["silence_id", "channel", "needed_zero", "current_status", "obstruction", "finite_fallback", "valid_for_claim"]),
            "",
            "## Alpha Coefficient Rows",
            markdown_table(rows_map["alpha_rows"], ["row_id", "quantity", "formula", "required_columns", "current_status", "valid_for_claim"]),
            "",
            "## Alpha Runner Refusal",
            markdown_table(rows_map["alpha_refusal"], ["runner_id", "row_id", "computed_status", "claim_allowed", "failure_reasons", "valid_for_claim"]),
            "",
            "## Branch Verdicts",
            markdown_table(rows_map["branch_verdicts"], ["verdict_id", "branch", "status", "because", "allowed_statement", "next_action", "valid_for_claim"]),
            "",
            "## Claim Gates",
            markdown_table(rows_map["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"]),
            "",
            "## Decisions",
            markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
            "",
            "## Next Target",
            markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status", "success_condition"]),
            "",
            "## Validation",
            markdown_table(validation_rows, ["check_id", "result", "detail"]),
            "",
            "## Working Interpretation",
            "This is a good kind of hard failure. The local-GR bridge now has an exact mathematical contract rather than a wish: identify the parent scalar, prove the operator is positive, prove source and boundary silence, and the local profile dies. If any one of those fails, the theory must wear the residual coupling honestly and score it against local tests.",
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
    print(f"1846 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
