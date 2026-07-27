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
QUARANTINE = MICROSCOPE / "quarantine" / "1847"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1847-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC1847_0_1846_next",
        "source_key": "1846_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_NEXT_TARGET.csv",
        "needles": ["NEXT1846_0_primary", "1847-Y5-R2FR-parent-Xhat"],
        "role": "1846 selects parent Xhat owner and Hessian signs/range as the next target.",
    },
    {
        "source_id": "SRC1847_1_1846_validation",
        "source_key": "1846_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1846_VALIDATION.csv",
        "needles": ["VAL1846_OVERALL", "PASS"],
        "role": "confirms 1846 passed as a nonclaim checkpoint.",
    },
    {
        "source_id": "SRC1847_2_1846_parent_owner",
        "source_key": "1846_parent_owner_audit",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_PARENT_SCALAR_OWNER_AUDIT.csv",
        "needles": ["OWN1846_4_verdict", "PARENT_OWNER_NOT_DERIVED"],
        "role": "1846 shows the dangerous scalar owner is not derived.",
    },
    {
        "source_id": "SRC1847_3_1846_operator_pack",
        "source_key": "1846_positive_operator_pack",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1846_POSITIVE_OPERATOR_PACK.csv",
        "needles": ["OP1846_4_verdict", "OPERATOR_PACK_UNSIGNED"],
        "role": "1846 shows the claim-grade positive operator pack is unsigned.",
    },
    {
        "source_id": "SRC1847_4_1025_second_variation",
        "source_key": "1025_second_variation",
        "source_path": RESIDUALS / "P8_Y5_R10_1025_SECOND_VARIATION_DERIVATION.csv",
        "needles": ["SV1025_6_verdict", "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED"],
        "role": "1025 supplies the scalar second-variation/range contract.",
    },
    {
        "source_id": "SRC1847_5_1025_hessian_audit",
        "source_key": "1025_parent_hessian_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_1025_PARENT_HESSIAN_AUDIT.csv",
        "needles": ["PHA1025_8_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1025 audits the missing parent Hessian signs, units and source terms.",
    },
    {
        "source_id": "SRC1847_6_1025_normalization_locks",
        "source_key": "1025_field_normalization_locks",
        "source_path": RESIDUALS / "P8_Y5_R10_1025_FIELD_NORMALIZATION_LOCKS.csv",
        "needles": ["FNL1025_1_canonical_metric", "CLEAN_CONTRACT_NOT_SIGNED"],
        "role": "1025 identifies the field metric/vacuum lock and beta target.",
    },
    {
        "source_id": "SRC1847_7_1025_alpha_template",
        "source_key": "1025_alpha_source_template",
        "source_path": RESIDUALS / "P8_Y5_R10_1025_ALPHA_SOURCE_ROW_TEMPLATE.csv",
        "needles": ["ASR1025_5_candidate_alpha", "SCHEMA_READY_VALUES_MISSING"],
        "role": "1025 supplies the fallback alpha source-row schema.",
    },
    {
        "source_id": "SRC1847_8_1094_parent_clause",
        "source_key": "1094_parent_Xhat_clause",
        "source_path": RESIDUALS / "P8_Y5_R10_1094_PARENT_XHAT_ACTION_CLAUSE_ATTEMPT.csv",
        "needles": ["PX1094_3_verdict", "PARENT_ACTION_CLAUSE_NOT_DERIVED"],
        "role": "1094 gives the parent Xhat action clause needed for WEP/product scoring.",
    },
    {
        "source_id": "SRC1847_9_1094_direct_product",
        "source_key": "1094_direct_WEP_product",
        "source_path": RESIDUALS / "P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv",
        "needles": ["DWP1094_3_direct_product_bound", "NUMERIC_SCORE_THRESHOLD_NONCLAIM"],
        "role": "1094 records a private direct WEP product threshold but no MTS prediction.",
    },
    {
        "source_id": "SRC1847_10_1026_parent_metric",
        "source_key": "1026_parent_metric_attempt",
        "source_path": RESIDUALS / "P8_Y5_R10_1026_PARENT_METRIC_ATTEMPT.csv",
        "needles": ["PM1026_6_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1026 shows the parent metric/eigenvalue lock remains unowned.",
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_SOURCE_REGISTER.csv",
    "parent_xhat_action": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_PARENT_XHAT_ACTION_CLAUSE.csv",
    "second_variation": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_SECOND_VARIATION_DERIVATION.csv",
    "parent_hessian": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_PARENT_HESSIAN_AUDIT.csv",
    "normalization_locks": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_FIELD_NORMALIZATION_LOCKS.csv",
    "alpha_template": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_ALPHA_SOURCE_ROW_TEMPLATE.csv",
    "direct_product": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_DIRECT_PRODUCT_BRIDGE.csv",
    "branch_verdicts": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_BRANCH_VERDICTS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1847_VALIDATION.csv",
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


def parent_xhat_action_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PX1847_0_field_owner",
            "parent_action_clause": "S_parent contains a normalized scalar/vertical mode Xhat with a declared quotient or physical-residual role",
            "must_satisfy": "Xhat is not chi_X closure notation; it is the field varied in the parent action and used in the Hessian",
            "current_status": "NOT_SIGNED",
            "if_signed": "connects no-hair operator, range, alpha/WEP products and local residual rows to one owner",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PX1847_1_same_variable_lock",
            "parent_action_clause": "visible coefficient response and no-hair equation use the same Xhat",
            "must_satisfy": "d ln(c_visible)=b_X dXhat and delta_X S_parent gives L_X Xhat=J_X with one normalization",
            "current_status": "NOT_DERIVED",
            "if_signed": "prevents separate knobs for clocks, WEP, R10 range and source amplitude",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PX1847_2_matter_response",
            "parent_action_clause": "ordinary matter response gives delta_X S_matter=0 or a finite observable product",
            "must_satisfy": "no hidden split into beta_source, tau, material tensor or readout factors unless each factor is sourced",
            "current_status": "NOT_SIGNED",
            "if_signed": "turns matter branch into theorem-zero or scoreable finite product",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PX1847_3_no_rescale_cheat",
            "parent_action_clause": "measured G/calibration cannot absorb relative source-weight or material-dependent residuals",
            "must_satisfy": "same observed-frame force map is used for GR baseline and MTS residual",
            "current_status": "POLICY_WRITTEN_NOT_PARENT_SIGNED",
            "if_signed": "protects local tests from cancellation/rescaling objections",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "clause_id": "PX1847_4_verdict",
            "parent_action_clause": "parent Xhat action clause sufficient for Hessian and product scoring",
            "must_satisfy": "field owner + same-variable lock + matter response + readout/frame + no-rescale rule",
            "current_status": "PARENT_XHAT_ACTION_CLAUSE_NOT_DERIVED",
            "if_signed": "1847 Hessian and alpha/product rows can become real prediction rows",
            "valid_for_claim": False,
        },
    ]


def second_variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "SV1847_0_local_block",
            "step": "write minimal parent-owned local Xhat block",
            "mathematical_statement": "S_X=int_A sqrt(h)[1/2 Z_X h^{ij} partial_i Xhat partial_j Xhat + 1/2 M_X^2 Xhat^2 - J_X Xhat] + boundary",
            "derived_result": "smallest scalar block whose second variation can define local finite-range channel",
            "status": "CONDITIONAL_ANSATZ_ONLY",
            "missing_for_claim": "same parent action must produce Xhat, h_ij, Z_X, M_X^2, J_X and boundary terms",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "SV1847_1_euler_operator",
            "step": "vary Xhat once",
            "mathematical_statement": "delta_X S_X -> O_X Xhat = J_X with O_X=-nabla_i(Z_X nabla^i)+M_X^2",
            "derived_result": "local operator is fixed once parent block and boundary convention are owned",
            "status": "CONDITIONAL_OPERATOR_DERIVED",
            "missing_for_claim": "parent Euler expression, self-adjoint domain and source split",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "SV1847_2_Hessian_signs",
            "step": "vary Xhat twice",
            "mathematical_statement": "delta_X^2 S_X=int_A sqrt(h)[Z_X |grad delta Xhat|^2+M_X^2(delta Xhat)^2]+boundary Hessian terms",
            "derived_result": "Z_X>0 and M_X^2>0 are exact local stability requirements",
            "status": "EXACT_CONDITION_DERIVED_VALUES_MISSING",
            "missing_for_claim": "parent Hessian signs, mixed-sector Hessian control and units",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "SV1847_3_range_relation",
            "step": "canonicalize static operator",
            "mathematical_statement": "mu_X^2=M_X^2/Z_X and lambda_X=sqrt(Z_X/M_X^2)",
            "derived_result": "lambda_X is exact if Z_X and M_X^2 are positive and come from the same normalized parent branch",
            "status": "EXACT_RELATION_DERIVED_NOT_OWNED",
            "missing_for_claim": "same-branch Z_X/M_X^2 with length units",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "SV1847_4_field_rescaling_guard",
            "step": "block fake normalization wins",
            "mathematical_statement": "Xhat->aXhat rescales Z_X, M_X^2, J_X and b_X in linked ways; invariant rows are lambda_X and coupled products",
            "derived_result": "field rescaling cannot choose beta, lambda or alpha after seeing local data",
            "status": "GUARDRAIL_PASS",
            "missing_for_claim": "parent field-space metric or Ward identity fixing invariant normalization",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "SV1847_5_sourcefree_nohair",
            "step": "connect Hessian to local silence",
            "mathematical_statement": "int_A[Z_X|grad Xhat|^2+M_X^2 Xhat^2]=int_A Xhat J_X+boundary_flux_X",
            "derived_result": "if Z_X>0, M_X^2>0, J_X=0 and boundary_flux_X=0, then Xhat=0 on local exterior",
            "status": "CONDITIONAL_THEOREM_ONLY",
            "missing_for_claim": "J_X=0, boundary flux zero and parent-signed positivity together",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "SV1847_6_verdict",
            "step": "decide whether 1847 owns the Hessian",
            "mathematical_statement": "parent_signed(delta_X^2 S_parent) -> Xhat,Z_X,M_X^2,lambda_X,alpha/source row",
            "derived_result": "1847 derives the exact contract but does not find parent-signed Xhat/Hessian ownership in current corpus",
            "status": "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED",
            "missing_for_claim": "explicit parent second variation, Xhat owner and normalization ledger",
            "valid_for_claim": False,
        },
    ]


def parent_hessian_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PHA1847_0_branch_extremum",
            "object": "F_1=E_Xhat|_{Xhat=0}",
            "required_evidence": "parent Euler expression vanishes on local branch before readout",
            "current_evidence": "1846 keeps scalar branch nonclaim; no parent Xhat action clause is signed",
            "status": "MISSING_PARENT_EULER_ZERO",
            "if_missing": "Xhat=0 is not proven stationary local vacuum",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PHA1847_1_ZX_positive",
            "object": "Z_X>0",
            "required_evidence": "positive gradient Hessian residue with field units and sign convention",
            "current_evidence": "1846/1093 operator pack remains unsigned; 1025 says parent sign missing",
            "status": "MISSING_PARENT_HESSIAN_SIGN",
            "if_missing": "ghost, anti-elliptic or indefinite local residual must be retained",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PHA1847_2_MX2_positive",
            "object": "M_X^2>0",
            "required_evidence": "positive local curvature Hessian in same Xhat normalization",
            "current_evidence": "mass gap/range remain formula-only; beta eigenvalue not signed",
            "status": "MISSING_PARENT_MASS_GAP",
            "if_missing": "massless, tachyonic or long-range branch remains possible",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PHA1847_3_lambda_units",
            "object": "lambda_X=sqrt(Z_X/M_X^2)",
            "required_evidence": "same-branch Z_X and M_X^2 with compatible units yielding meters",
            "current_evidence": "range relation exact but values/units missing; alpha runner refuses",
            "status": "RELATION_ONLY_VALUES_MISSING",
            "if_missing": "R10/local interpolation cannot be claim-grade",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PHA1847_4_cross_Hessian",
            "object": "mixed Xhat-sector Hessian terms",
            "required_evidence": "cross terms with metric, trace, projector, boundary and matter variables vanish or form positive block",
            "current_evidence": "no full parent metric/cross-term policy in active branch",
            "status": "MISSING_BLOCK_DIAGONAL_OR_POSITIVE_MATRIX_PROOF",
            "if_missing": "single-scalar Z_X/M_X^2 truncation may be invalid",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PHA1847_5_source_current",
            "object": "J_X=0 or J_X bound",
            "required_evidence": "delta_X S_matter plus hidden/source/domain terms vanish or are numerically bounded",
            "current_evidence": "1846 source silence audit remains unsigned",
            "status": "MISSING_SOURCE_ZERO_OR_BOUND",
            "if_missing": "qbar_XT/source-coupling remains live finite-force channel",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PHA1847_6_boundary_flux",
            "object": "boundary_flux_X=0 or bound",
            "required_evidence": "self-adjoint boundary class, exact/proper gauge edge or explicit flux bound",
            "current_evidence": "1843-1844 keep B_X/EDGEBOUND boundary branch unsigned",
            "status": "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND",
            "if_missing": "positive no-hair identity cannot conclude Xhat=0",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PHA1847_7_prefactor",
            "object": "K_X=s_X/(4*pi*Z_X*G_obs)",
            "required_evidence": "normalization convention, sign s_X, G_obs frame and source/test charges",
            "current_evidence": "alpha source rows remain schema-ready values-missing",
            "status": "MISSING_ALPHA_NORMALIZATION",
            "if_missing": "alpha(lambda) row remains smoke-only",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PHA1847_8_verdict",
            "object": "parent Xhat/Hessian ownership",
            "required_evidence": "PX1847 and PHA1847_0 through PHA1847_7 close from one parent branch",
            "current_evidence": "none of the parent-owned owner/value/sign/source rows close",
            "status": "FAIL_CURRENT_CLAIM",
            "if_missing": "move to parent metric/eigenvalue theorem or source-zero/bounded coupling row",
            "valid_for_claim": False,
        },
    ]


def normalization_lock_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "lock_id": "FNL1847_0_invariant",
            "target": "identify physical finite-range invariant",
            "condition": "beta_eff=ell_vac^2 M_X^2/Z_X or an equivalent parent-normalized Hessian eigenvalue",
            "current_status": "CONDITIONAL_INVARIANT_IDENTIFIED",
            "allowed_use": "theorem target and normalization guard",
            "forbidden_use": "claim that rho_vac alone predicts lambda_X",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "FNL1847_1_canonical_metric",
            "target": "make vacuum density set the field-space metric",
            "condition": "Z_X f_X^2=rho_vac^(1/2)",
            "current_status": "CLEAN_CONTRACT_NOT_SIGNED",
            "allowed_use": "parent Ward/metric theorem target",
            "forbidden_use": "normalization chosen after R10 pressure",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "FNL1847_2_beta3",
            "target": "low-scrutiny finite theorem target",
            "condition": "U''(0)=3 from spatial trace/eigenvalue theorem",
            "current_status": "BEST_CONDITIONAL_TARGET_NOT_SIGNED",
            "allowed_use": "private derivation target",
            "forbidden_use": "predicted beta/lambda claim",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "FNL1847_3_direct_range",
            "target": "direct range backsolve",
            "condition": "choose beta/lambda after seeing local bound pressure",
            "current_status": "CLOSURE_ONLY_FORBIDDEN_AS_DERIVATION",
            "allowed_use": "sanity check only",
            "forbidden_use": "evidence or prediction",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "lock_id": "FNL1847_4_CX_tie",
            "target": "tie range normalization to source amplitude",
            "condition": "same parent normalization fixes lambda_X and C_X/K_X/qbar_XT/Qbar_XH",
            "current_status": "MISSING_COUPLING_NORMALIZATION_LEDGER",
            "allowed_use": "next source-row schema",
            "forbidden_use": "choose range and amplitude independently",
            "valid_for_claim": False,
        },
    ]


def alpha_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "ASR1847_0_bulk_Hessian",
            "quantity": "Xhat;Z_X;M_X2;lambda_X",
            "formula": "lambda_X=sqrt(Z_X/M_X2)",
            "required_columns": "system_id;field_id;branch_id;Xhat_owner;Z_X;M_X2;lambda_X;Z_units;M_units;lambda_units;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_INPUT",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1847_PARENT_HESSIAN_AUDIT.csv",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ASR1847_1_field_metric_beta",
            "quantity": "Z_X f_X^2;Upp0;beta_eff",
            "formula": "beta_eff=Upp0*rho_vac^(1/2)/(Z_X*f_X^2)",
            "required_columns": "system_id;branch_id;ZX_fX2;Upp0;beta_eff;metric_units;source_path;valid_for_claim",
            "current_status": "MISSING_PARENT_METRIC_AND_EIGENVALUE",
            "source_path": "source-intake/mts_residuals/P8_Y5_R10_1026_PARENT_METRIC_ATTEMPT.csv",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ASR1847_2_source_current",
            "quantity": "J_X or qbar_XT",
            "formula": "J_X=delta_X S_matter + hidden/source/domain terms",
            "required_columns": "system_id;matter_sector;qbar_XT;J_X;J_X_bound;units;source_path;valid_for_claim",
            "current_status": "MISSING_SOURCE_ZERO_OR_BOUND",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1846_SOURCE_SILENCE_AUDIT.csv",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ASR1847_3_Hamiltonian_projection",
            "quantity": "Qbar_XH",
            "formula": "Qbar_XH(lambda)=Pi_M^H[Q_X^H(lambda)]/M_H",
            "required_columns": "system_id;source_body;Q_XH;Qbar_XH;projector;units;source_path;valid_for_claim",
            "current_status": "MISSING_ARENA_PROJECTION",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1843_SOURCE_PACK_SCHEMA.csv",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ASR1847_4_green_prefactor",
            "quantity": "K_X",
            "formula": "K_X=s_X/(4*pi*Z_X*G_obs)",
            "required_columns": "system_id;K_X;s_X;Z_X;G_obs;normalization;units;source_path;valid_for_claim",
            "current_status": "MISSING_ALPHA_NORMALIZATION",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1847_FIELD_NORMALIZATION_LOCKS.csv",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "ASR1847_5_candidate_alpha",
            "quantity": "alpha_bulk(lambda_X)",
            "formula": "alpha_bulk(lambda_X)=K_X*Qbar_XH(lambda_X)*qbar_XT",
            "required_columns": "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_bulk;alpha_bound;source_paths;valid_for_claim",
            "current_status": "SCHEMA_READY_VALUES_MISSING",
            "source_path": "source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1847_ALPHA_SOURCE_ROW_TEMPLATE.csv",
            "valid_for_claim": False,
        },
    ]


def direct_product_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "DPB1847_0_WEP_threshold",
            "object": "P_WEP_alpha_direct bound",
            "status": "NUMERIC_THRESHOLD_NONCLAIM_EXISTS",
            "value": "4.797780522732e-05",
            "units": "dimensionless",
            "meaning": "private WEP product threshold can score a future direct MTS product row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "DPB1847_1_MTS_prediction",
            "object": "MTS direct WEP/R10 product prediction",
            "status": "MISSING_MTS_DIRECT_PRODUCT",
            "value": "MISSING",
            "units": "dimensionless",
            "meaning": "requires parent Xhat action/matter response or explicit source-backed product",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "bridge_id": "DPB1847_2_verdict",
            "object": "direct product bridge",
            "status": "BOUND_SIDE_READY_PREDICTION_SIDE_MISSING",
            "value": "not_run",
            "units": "dimensionless",
            "meaning": "do not scrape more bound data until MTS prediction owner exists",
            "valid_for_claim": False,
        },
    ]


def branch_verdict_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1847_0_Xhat_owner",
            "branch": "parent Xhat owner",
            "status": "PARENT_ACTION_CLAUSE_NOT_DERIVED",
            "because": "no source makes Xhat the field varied in the parent action and the same variable controlling visible coefficients",
            "allowed_statement": "MTS has an exact parent-owner contract",
            "forbidden_statement": "chi_X/Xhat is already the physical scalar",
            "next_action": "try parent metric/eigenvalue theorem or direct source product row",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1847_1_Hessian_formula",
            "branch": "parent Hessian route",
            "status": "CONTRACT_DERIVED_NOT_OWNED",
            "because": "second variation/range law is exact, but current files do not supply parent-signed Xhat, Z_X, M_X^2 or units",
            "allowed_statement": "MTS has a precise Hessian contract for local scalar route",
            "forbidden_statement": "MTS predicts lambda_X or passes local tests from this route",
            "next_action": "derive parent field-space metric and Hessian eigenvalue",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1847_2_alpha_source_row",
            "branch": "residual alpha/source fallback",
            "status": "SCHEMA_READY_VALUES_MISSING",
            "because": "K_X, Qbar_XH, qbar_XT, Z_X, Xhat owner and lambda_X remain missing or unsigned",
            "allowed_statement": "fallback alpha rows are ready to receive sourced values",
            "forbidden_statement": "fallback alpha row is evidence",
            "next_action": "fill only after parent metric/eigenvalue or source-current coefficients exist",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1847_3_direct_product",
            "branch": "direct WEP/R10 product",
            "status": "BOUND_SIDE_READY_PREDICTION_SIDE_MISSING",
            "because": "WEP product threshold exists but MTS has no parent-projected product prediction",
            "allowed_statement": "direct product scoring avoids fake factor splitting if prediction row is sourced",
            "forbidden_statement": "threshold alone supports MTS",
            "next_action": "use only after parent Xhat matter-response clause or numeric product row exists",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "verdict_id": "BV1847_4_next_target",
            "branch": "next target",
            "status": "PARENT_METRIC_OR_SOURCE_ZERO_RETURN",
            "because": "Xhat owner/Hessian row failed; the least fake next options are parent metric/eigenvalue or qbar_XT/J_X source-zero",
            "allowed_statement": "finite route is a private theorem target; source-zero remains cleaner for local GR",
            "forbidden_statement": "finite lambda or local-GR claim",
            "next_action": "1848-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1847_0_sources_registered",
            "claim": "1847 source chain exists",
            "gate_pass": False,
            "reason": "source chain supports audit continuity only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1847_1_parent_Xhat_owner",
            "claim": "same Xhat is parent-owned scalar/operator field",
            "gate_pass": False,
            "reason": "PX1847_4_verdict=PARENT_XHAT_ACTION_CLAUSE_NOT_DERIVED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1847_2_parent_block_owned",
            "claim": "single parent action owns Xhat block",
            "gate_pass": False,
            "reason": "local block is conditional ansatz only",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1847_3_ZX_positive",
            "claim": "Z_X>0 is parent-signed",
            "gate_pass": False,
            "reason": "kinetic Hessian sign and units are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1847_4_MX2_positive",
            "claim": "M_X^2>0 is parent-signed",
            "gate_pass": False,
            "reason": "mass-gap/eigenvalue theorem is missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1847_5_alpha_source_claim",
            "claim": "alpha(lambda) row is claim-grade",
            "gate_pass": False,
            "reason": "K_X, Qbar_XH, qbar_XT and bound comparison inputs are missing",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "gate_id": "CG1847_6_local_GR_claim",
            "claim": "local GR/Newton reduction is derived",
            "gate_pass": False,
            "reason": "Xhat/Hessian/source/boundary/no-pole routes remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1847_0_exact_contract",
            "decision": "The exact parent Xhat/Hessian/range contract is now written in the active branch.",
            "because": "second variation gives O_X, positivity conditions and lambda_X=sqrt(Z_X/M_X^2), while the parent Xhat clause states the owner requirement.",
            "next_action": "do not re-derive the same formula; hunt parent metric/eigenvalue or source-zero owner",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1847_1_no_claim",
            "decision": "Current MTS still does not own Xhat, Z_X, M_X^2, lambda_X or alpha.",
            "because": "required values, signs, units, cross-term controls, matter response and source coefficients are missing or conditional.",
            "next_action": "keep local R10/PPN/local-GR claims blocked",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1847_2_product_bridge",
            "decision": "Direct WEP product scoring is useful but prediction-side empty.",
            "because": "the bound-side product threshold exists, but no parent Xhat matter response yields an MTS product row.",
            "next_action": "derive parent matter-response clause or source a direct product row later",
            "valid_for_claim": False,
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1847_3_next_target",
            "decision": "Next target is parent metric/eigenvalue or source-zero return.",
            "because": "without parent field-space metric/eigenvalue, the finite Hessian route cannot be promoted; source-zero is cleaner for local GR if it can be signed.",
            "next_action": "1848-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1847_0_primary",
            "next_target": "1848-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
            "script": "scripts/Y5_R2FR_parent_metric_ZXfX2_beta_eigenvalue_or_source_zero_return_1848.py",
            "objective": "try to derive parent field-space metric lock Z_X f_X^2=rho_vac^(1/2) and beta eigenvalue; if unsigned, return to J_X/qbar_XT source-zero or bounded coupling rows",
            "selection_status": "selected",
            "success_condition": "parent M_AB/e_X/H_X spectrum signs the finite route, or finite route is frozen and source-zero/bounded coupling becomes primary",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1847_1_parallel",
            "next_target": "1848b-Y5-R2FR-direct-WEP-R10-product-prediction-row.md",
            "script": "scripts/Y5_R2FR_direct_WEP_R10_product_prediction_row_1848b.py",
            "objective": "stage direct product prediction rows only if parent Xhat matter-response or numeric source kernels are available",
            "selection_status": "held",
            "success_condition": "no standalone beta/tau division, no tau=1 shortcut, no threshold-only claim",
        },
    ]


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_register_rows(),
        "parent_xhat_action": parent_xhat_action_rows(),
        "second_variation": second_variation_rows(),
        "parent_hessian": parent_hessian_rows(),
        "normalization_locks": normalization_lock_rows(),
        "alpha_template": alpha_template_rows(),
        "direct_product": direct_product_rows(),
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
            RAB_QUEUE / f"JR1847_{key.upper()}.csv",
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
        if not (RAB_QUEUE / f"JR1847_{key.upper()}.csv").exists():
            return False
    return True


def no_formalization_outputs() -> bool:
    if not FORMALIZATION.exists():
        return True
    markers = [
        "1847-Y5-R2FR",
        "P8_Y5_PARENT_QLOC_1847",
        "P8_Y5_BRR545_1847",
        "Y5_R2FR_parent_Xhat_owner_and_Hessian_ZX_MX2_range_or_alpha_source_row_1847",
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
        ("VAL1847_0_sources_exist", all(row["exists"] is True for row in source_rows), "all cited source paths exist"),
        ("VAL1847_1_needles_present", all(row["needles_present"] is True for row in source_rows), "all cited source needles are present"),
        (
            "VAL1847_2_parent_xhat_blocks",
            any(row["clause_id"] == "PX1847_4_verdict" and row["current_status"] == "PARENT_XHAT_ACTION_CLAUSE_NOT_DERIVED" for row in rows_map["parent_xhat_action"]),
            "parent Xhat action clause remains unsigned",
        ),
        (
            "VAL1847_3_second_variation_written",
            any(row["derivation_id"] == "SV1847_6_verdict" and row["status"] == "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED" for row in rows_map["second_variation"]),
            "second variation/range contract written but nonclaim",
        ),
        (
            "VAL1847_4_hessian_audit_blocks",
            any(row["audit_id"] == "PHA1847_8_verdict" and row["status"] == "FAIL_CURRENT_CLAIM" for row in rows_map["parent_hessian"]),
            "parent Hessian ownership remains blocked",
        ),
        (
            "VAL1847_5_normalization_locks_nonclaim",
            any(row["lock_id"] == "FNL1847_1_canonical_metric" and row["current_status"] == "CLEAN_CONTRACT_NOT_SIGNED" for row in rows_map["normalization_locks"])
            and all(row["valid_for_claim"] is False for row in rows_map["normalization_locks"]),
            "normalization locks are explicit and nonclaim",
        ),
        (
            "VAL1847_6_alpha_schema_nonclaim",
            any(row["row_id"] == "ASR1847_5_candidate_alpha" and row["current_status"] == "SCHEMA_READY_VALUES_MISSING" for row in rows_map["alpha_template"])
            and all(row["valid_for_claim"] is False for row in rows_map["alpha_template"]),
            "alpha source row schema is complete and nonclaim",
        ),
        (
            "VAL1847_7_direct_product_nonclaim",
            any(row["bridge_id"] == "DPB1847_2_verdict" and row["status"] == "BOUND_SIDE_READY_PREDICTION_SIDE_MISSING" for row in rows_map["direct_product"]),
            "direct product bridge remains prediction-side missing",
        ),
        (
            "VAL1847_8_branch_next_selected",
            any(row["verdict_id"] == "BV1847_4_next_target" and row["status"] == "PARENT_METRIC_OR_SOURCE_ZERO_RETURN" for row in rows_map["branch_verdicts"]),
            "branch verdict selects parent metric/source-zero next",
        ),
        (
            "VAL1847_9_claim_gates_blocked",
            all(row["gate_pass"] is False and row["claim_allowed"] is False for row in rows_map["claim_gate"]),
            "all claim gates remain blocked",
        ),
        (
            "VAL1847_10_decision_next",
            any(row["decision_id"] == "DEC1847_3_next_target" and "parent metric" in row["decision"] for row in rows_map["decision"]),
            "decision ledger selects parent metric/source-zero target",
        ),
        (
            "VAL1847_11_next_target_selected",
            any(row["route_id"] == "NEXT1847_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        ),
        ("VAL1847_12_no_claim_flags", no_claim_flags(rows_map), "no claim flags are true"),
        ("VAL1847_13_missing_rows_nonclaim", missing_rows_not_ready(rows_map), "MISSING_* rows stay nonclaim"),
        ("VAL1847_14_csv_parse", csv_parse_all(), "all generated 1847 CSVs parse"),
        ("VAL1847_15_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist"),
        ("VAL1847_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent"),
        ("VAL1847_17_formalization_untouched", no_formalization_outputs(), "no 1847 outputs found under formalization-workbench"),
    ]
    rows = [{"branch_id": BRANCH_ID, "check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1847_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "1847 parent Xhat owner and Hessian ZX MX2 range or alpha source row",
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
            "# 1847 Y5 R2FR parent Xhat owner and Hessian ZX MX2 range or alpha source row",
            "",
            "**Progress:** 1847 writes the active-branch contract for the dangerous scalar: one parent `Xhat` must own the visible coefficient, the no-hair operator, the Hessian signs, the range, and any finite alpha/WEP/R10 product. That is the anti-knob rule.",
            "",
            "**Current verdict:** the exact second-variation/range law is derived, but current MTS does not yet own the parent `Xhat` action clause, `Z_X`, `M_X^2`, units, cross-Hessian block, source current, boundary flux, or alpha/product normalization. The fallback rows are schema-ready only.",
            "",
            "**Claim ceiling:** no parent-Xhat claim, no finite-range prediction, no alpha/product pass, no R10/R11 pass, no PPN pass, no local-GR/Newton reduction, no GitHub action, and no `formalization-workbench` edit is allowed from 1847.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present", "missing_needles", "role"]),
            "",
            "## Parent Xhat Action Clause",
            markdown_table(rows_map["parent_xhat_action"], ["clause_id", "parent_action_clause", "must_satisfy", "current_status", "if_signed", "valid_for_claim"]),
            "",
            "## Second Variation Derivation",
            markdown_table(rows_map["second_variation"], ["derivation_id", "step", "mathematical_statement", "derived_result", "status", "missing_for_claim", "valid_for_claim"]),
            "",
            "## Parent Hessian Audit",
            markdown_table(rows_map["parent_hessian"], ["audit_id", "object", "required_evidence", "current_evidence", "status", "if_missing", "valid_for_claim"]),
            "",
            "## Field Normalization Locks",
            markdown_table(rows_map["normalization_locks"], ["lock_id", "target", "condition", "current_status", "allowed_use", "forbidden_use", "valid_for_claim"]),
            "",
            "## Alpha Source Row Template",
            markdown_table(rows_map["alpha_template"], ["row_id", "quantity", "formula", "required_columns", "current_status", "source_path", "valid_for_claim"]),
            "",
            "## Direct Product Bridge",
            markdown_table(rows_map["direct_product"], ["bridge_id", "object", "status", "value", "units", "meaning", "valid_for_claim"]),
            "",
            "## Branch Verdicts",
            markdown_table(rows_map["branch_verdicts"], ["verdict_id", "branch", "status", "because", "allowed_statement", "forbidden_statement", "next_action", "valid_for_claim"]),
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
            "The finite scalar path is now disciplined: same parent field, same Hessian, same source normalization, same observed-frame readout. No more choosing range here and amplitude there. Since the owner row still fails, the next fair attack is either parent metric/eigenvalue ownership or source-zero/bounded coupling.",
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
    print(f"1847 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
