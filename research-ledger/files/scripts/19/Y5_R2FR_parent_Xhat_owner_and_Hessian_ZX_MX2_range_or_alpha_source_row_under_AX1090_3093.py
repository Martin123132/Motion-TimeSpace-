from __future__ import annotations

import csv
import hashlib
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


RUN_UTC = datetime.now(timezone.utc).isoformat()
ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3093"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "3093-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row-under-AX1090.md"

SOURCES: dict[str, dict[str, Any]] = {
    "SRC3093_00_3092_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3092_NEXT_TARGET.csv",
        "needles": ["NEXT3092_0_3093", "lambda_X=sqrt(Z_X/M_X^2)"],
        "role": "3092 selects parent Xhat owner and Hessian/range extraction.",
    },
    "SRC3093_01_3092_doc": {
        "path": ROOT / "3092-Y5-R2FR-scalar-nohair-input-pack-or-residual-alpha-coefficient-runner-under-AX1090.md",
        "needles": ["PARENT_OWNER_AND_HESSIAN_FIRST", "SIA3092_2_Z_X"],
        "role": "3092 blocks no-hair until the owner/Hessian inputs exist.",
    },
    "SRC3093_02_1847_doc": {
        "path": ROOT / "1847-Y5-R2FR-parent-Xhat-owner-and-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "needles": ["anti-knob rule", "exact second-variation/range law is derived"],
        "role": "1847 precedent for the active parent q_loc branch.",
    },
    "SRC3093_03_1847_parent_clause": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_PARENT_XHAT_ACTION_CLAUSE.csv",
        "needles": ["PX1847_4_verdict", "PARENT_XHAT_ACTION_CLAUSE_NOT_DERIVED"],
        "role": "1847 parent Xhat action clause failure.",
    },
    "SRC3093_04_1847_second_variation": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_SECOND_VARIATION_DERIVATION.csv",
        "needles": ["SV1847_6_verdict", "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED"],
        "role": "1847 second variation/range contract.",
    },
    "SRC3093_05_1847_hessian": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_PARENT_HESSIAN_AUDIT.csv",
        "needles": ["PHA1847_8_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1847 missing parent Hessian/sign/source audit.",
    },
    "SRC3093_06_1847_norm": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_FIELD_NORMALIZATION_LOCKS.csv",
        "needles": ["FNL1847_1_canonical_metric", "CLEAN_CONTRACT_NOT_SIGNED"],
        "role": "1847 field normalization locks and beta target.",
    },
    "SRC3093_07_1847_alpha_template": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1847_ALPHA_SOURCE_ROW_TEMPLATE.csv",
        "needles": ["ASR1847_5_candidate_alpha", "SCHEMA_READY_VALUES_MISSING"],
        "role": "1847 fallback alpha source-row schema.",
    },
    "SRC3093_08_1094_parent_clause": {
        "path": RESIDUALS / "P8_Y5_R10_1094_PARENT_XHAT_ACTION_CLAUSE_ATTEMPT.csv",
        "needles": ["PX1094_3_verdict", "PARENT_ACTION_CLAUSE_NOT_DERIVED"],
        "role": "1094 parent Xhat clause needed for direct product scoring.",
    },
    "SRC3093_09_1094_direct_product": {
        "path": RESIDUALS / "P8_Y5_R10_1094_DIRECT_WEP_PRODUCT_CONTRACT.csv",
        "needles": ["DWP1094_3_direct_product_bound", "MISSING_MTS_DIRECT_PRODUCT"],
        "role": "1094 direct product bound exists but prediction side is missing.",
    },
    "SRC3093_10_1026_metric": {
        "path": RESIDUALS / "P8_Y5_R10_1026_PARENT_METRIC_ATTEMPT.csv",
        "needles": ["PM1026_6_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1026 parent metric/eigenvalue lock remains unowned.",
    },
    "SRC3093_11_1026_next": {
        "path": RESIDUALS / "P8_Y5_R10_1026_NEXT_TARGET.csv",
        "needles": ["1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row", "derive qbar_XT=0"],
        "role": "1026 says source-zero/bounded coupling is the cleaner return if metric lock fails.",
    },
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3093_SOURCE_REGISTER.csv",
    "parent_clause": RESIDUALS / "P8_Y5_R2FR_3093_PARENT_XHAT_ACTION_CLAUSE.csv",
    "second_variation": RESIDUALS / "P8_Y5_R2FR_3093_SECOND_VARIATION_DERIVATION.csv",
    "hessian": RESIDUALS / "P8_Y5_R2FR_3093_PARENT_HESSIAN_AUDIT.csv",
    "normalization": RESIDUALS / "P8_Y5_R2FR_3093_FIELD_NORMALIZATION_LOCKS.csv",
    "alpha_template": RESIDUALS / "P8_Y5_R2FR_3093_ALPHA_SOURCE_ROW_TEMPLATE.csv",
    "direct_product": RESIDUALS / "P8_Y5_R2FR_3093_DIRECT_PRODUCT_BRIDGE.csv",
    "verdicts": RESIDUALS / "P8_Y5_R2FR_3093_BRANCH_VERDICTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3093_CLAIM_GATE.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3093_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3093_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3093_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3093_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "parent_clause_copy": LOCAL_BOUNDS / "parent_Xhat_action_clause_3093_NONCLAIM.csv",
    "hessian_copy": LOCAL_BOUNDS / "parent_hessian_audit_3093_NONCLAIM.csv",
    "alpha_template_copy": LOCAL_BOUNDS / "alpha_source_row_template_3093_NONCLAIM.csv",
    "verdicts_copy": LOCAL_BOUNDS / "branch_verdicts_3093_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3093_parent_metric_or_source_zero_NEXT_NONCLAIM.csv",
}


def meta() -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def remove_pycache() -> None:
    if PYCACHE.exists():
        shutil.rmtree(PYCACHE)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def file_hash(path: Path) -> str:
    if not path.exists():
        return "MISSING"
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def csv_ok(path: Path) -> bool:
    try:
        if not path.exists():
            return False
        with path.open("r", newline="", encoding="utf-8") as handle:
            list(csv.DictReader(handle))
        return True
    except Exception:
        return False


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def source_parse_ok(path: Path) -> bool:
    return csv_ok(path) if path.suffix.lower() == ".csv" else path.exists()


def with_meta(output_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    base = meta()
    return [{**base, **row} for row in output_rows]


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for row in output_rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in output_rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def source_rows() -> list[dict[str, Any]]:
    output_rows = []
    for source_id, source in SOURCES.items():
        path = Path(source["path"])
        text = read_text(path)
        missing = [needle for needle in source["needles"] if needle not in text]
        output_rows.append(
            {
                "source_id": source_id,
                "source_path": str(path),
                "exists": path.exists(),
                "parse_ok": source_parse_ok(path),
                "sha256": file_hash(path),
                "needles_present": not missing,
                "missing_needles": ";".join(missing),
                "role": source["role"],
            }
        )
    return with_meta(output_rows)


def parent_clause_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "clause_id": "PX3093_0_field_owner",
                "parent_action_clause": "S_parent contains a normalized scalar/vertical mode Xhat with a declared quotient or physical-residual role",
                "must_satisfy": "Xhat is not chi_X closure notation; it is the field varied in the parent action and used in the Hessian",
                "current_status": "NOT_SIGNED",
                "if_signed": "connects no-hair operator, range, alpha/WEP/R10 products and local residual rows to one owner",
            },
            {
                "clause_id": "PX3093_1_same_variable_lock",
                "parent_action_clause": "visible coefficient response and no-hair equation use the same Xhat",
                "must_satisfy": "d ln(c_visible)=b_X dXhat and delta_X S_parent gives L_X Xhat=J_X with one normalization",
                "current_status": "NOT_DERIVED",
                "if_signed": "prevents separate knobs for clocks, WEP, R10 range and source amplitude",
            },
            {
                "clause_id": "PX3093_2_matter_response",
                "parent_action_clause": "ordinary matter response gives delta_X S_matter=0 or a finite observable product",
                "must_satisfy": "no hidden split into beta_source, tau, material tensor or readout factors unless each factor is sourced",
                "current_status": "NOT_SIGNED",
                "if_signed": "turns matter branch into theorem-zero or scoreable finite product",
            },
            {
                "clause_id": "PX3093_3_no_rescale_cheat",
                "parent_action_clause": "measured G/calibration cannot absorb relative source-weight or material-dependent residuals",
                "must_satisfy": "same observed-frame force map is used for GR baseline and MTS residual",
                "current_status": "POLICY_WRITTEN_NOT_PARENT_SIGNED",
                "if_signed": "protects local tests from cancellation/rescaling objections",
            },
            {
                "clause_id": "PX3093_4_verdict",
                "parent_action_clause": "parent Xhat action clause sufficient for Hessian and product scoring",
                "must_satisfy": "field owner + same-variable lock + matter response + readout/frame + no-rescale rule",
                "current_status": "PARENT_XHAT_ACTION_CLAUSE_NOT_DERIVED",
                "if_signed": "3093 Hessian and alpha/product rows can become real prediction rows",
            },
        ]
    )


def second_variation_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "derivation_id": "SV3093_0_local_block",
                "step": "write minimal parent-owned local Xhat block",
                "mathematical_statement": "S_X=int_A sqrt(h)[1/2 Z_X h^{ij} partial_i Xhat partial_j Xhat + 1/2 M_X^2 Xhat^2 - J_X Xhat] + boundary",
                "derived_result": "smallest scalar block whose second variation can define local finite-range channel",
                "status": "CONDITIONAL_ANSATZ_ONLY",
                "missing_for_claim": "same parent action must produce Xhat, h_ij, Z_X, M_X^2, J_X and boundary terms",
            },
            {
                "derivation_id": "SV3093_1_euler_operator",
                "step": "vary Xhat once",
                "mathematical_statement": "delta_X S_X -> O_X Xhat = J_X with O_X=-nabla_i(Z_X nabla^i)+M_X^2",
                "derived_result": "local operator is fixed once parent block and boundary convention are owned",
                "status": "CONDITIONAL_OPERATOR_DERIVED",
                "missing_for_claim": "parent Euler expression, self-adjoint domain and source split",
            },
            {
                "derivation_id": "SV3093_2_Hessian_signs",
                "step": "vary Xhat twice",
                "mathematical_statement": "delta_X^2 S_X=int_A sqrt(h)[Z_X |grad delta Xhat|^2+M_X^2(delta Xhat)^2]+boundary Hessian terms",
                "derived_result": "Z_X>0 and M_X^2>0 are exact local stability requirements",
                "status": "EXACT_CONDITION_DERIVED_VALUES_MISSING",
                "missing_for_claim": "parent Hessian signs, mixed-sector Hessian control and units",
            },
            {
                "derivation_id": "SV3093_3_range_relation",
                "step": "canonicalize static operator",
                "mathematical_statement": "mu_X^2=M_X^2/Z_X and lambda_X=sqrt(Z_X/M_X^2)",
                "derived_result": "lambda_X is exact if Z_X and M_X^2 are positive and come from the same normalized parent branch",
                "status": "EXACT_RELATION_DERIVED_NOT_OWNED",
                "missing_for_claim": "same-branch Z_X/M_X^2 with length units",
            },
            {
                "derivation_id": "SV3093_4_field_rescaling_guard",
                "step": "block fake normalization wins",
                "mathematical_statement": "Xhat->aXhat rescales Z_X, M_X^2, J_X and b_X in linked ways; invariant rows are lambda_X and coupled products",
                "derived_result": "field rescaling cannot choose beta, lambda or alpha after seeing local data",
                "status": "GUARDRAIL_PASS",
                "missing_for_claim": "parent field-space metric or Ward identity fixing invariant normalization",
            },
            {
                "derivation_id": "SV3093_5_sourcefree_nohair",
                "step": "connect Hessian to local silence",
                "mathematical_statement": "int_A[Z_X|grad Xhat|^2+M_X^2 Xhat^2]=int_A Xhat J_X+boundary_flux_X",
                "derived_result": "if Z_X>0, M_X^2>0, J_X=0 and boundary_flux_X=0, then Xhat=0 on local exterior",
                "status": "CONDITIONAL_THEOREM_ONLY",
                "missing_for_claim": "J_X=0, boundary flux zero and parent-signed positivity together",
            },
            {
                "derivation_id": "SV3093_6_verdict",
                "step": "decide whether 3093 owns the Hessian",
                "mathematical_statement": "parent_signed(delta_X^2 S_parent) -> Xhat,Z_X,M_X^2,lambda_X,alpha/source row",
                "derived_result": "3093 derives the exact contract but does not find parent-signed Xhat/Hessian ownership in current corpus",
                "status": "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED",
                "missing_for_claim": "explicit parent second variation, Xhat owner and normalization ledger",
            },
        ]
    )


def hessian_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "audit_id": "PHA3093_0_branch_extremum",
                "object": "F_1=E_Xhat|_{Xhat=0}",
                "required_evidence": "parent Euler expression vanishes on local branch before readout",
                "current_evidence": "3092 keeps scalar branch nonclaim; no parent Xhat action clause is signed",
                "status": "MISSING_PARENT_EULER_ZERO",
                "if_missing": "Xhat=0 is not proven stationary local vacuum",
            },
            {
                "audit_id": "PHA3093_1_ZX_positive",
                "object": "Z_X>0",
                "required_evidence": "positive gradient Hessian residue with field units and sign convention",
                "current_evidence": "3092/1847/1093 operator packs remain unsigned",
                "status": "MISSING_PARENT_HESSIAN_SIGN",
                "if_missing": "ghost, anti-elliptic or indefinite local residual must be retained",
            },
            {
                "audit_id": "PHA3093_2_MX2_positive",
                "object": "M_X^2>0",
                "required_evidence": "positive local curvature Hessian in same Xhat normalization",
                "current_evidence": "mass gap/range remain formula-only; beta eigenvalue not signed",
                "status": "MISSING_PARENT_MASS_GAP",
                "if_missing": "massless, tachyonic or long-range branch remains possible",
            },
            {
                "audit_id": "PHA3093_3_lambda_units",
                "object": "lambda_X=sqrt(Z_X/M_X^2)",
                "required_evidence": "same-branch Z_X and M_X^2 with compatible units yielding meters",
                "current_evidence": "range relation exact but values/units missing; alpha runner refuses",
                "status": "RELATION_ONLY_VALUES_MISSING",
                "if_missing": "R10/local interpolation cannot be claim-grade",
            },
            {
                "audit_id": "PHA3093_4_cross_Hessian",
                "object": "mixed Xhat-sector Hessian terms",
                "required_evidence": "cross terms with metric, trace, projector, boundary and matter variables vanish or form positive block",
                "current_evidence": "1026 says parent metric/eigenvalue/cross-block lock remains unowned",
                "status": "MISSING_BLOCK_DIAGONAL_OR_POSITIVE_MATRIX_PROOF",
                "if_missing": "single-scalar Z_X/M_X^2 truncation may be invalid",
            },
            {
                "audit_id": "PHA3093_5_source_current",
                "object": "J_X=0 or J_X bound",
                "required_evidence": "delta_X S_matter plus hidden/source/domain terms vanish or are numerically bounded",
                "current_evidence": "3092 source silence audit remains unsigned; 1026 next target returns to qbar_XT/J_X",
                "status": "MISSING_SOURCE_ZERO_OR_BOUND",
                "if_missing": "qbar_XT/source-coupling remains live finite-force channel",
            },
            {
                "audit_id": "PHA3093_6_boundary_flux",
                "object": "boundary_flux_X=0 or bound",
                "required_evidence": "self-adjoint boundary class, exact/proper gauge edge or explicit flux bound",
                "current_evidence": "3092 keeps boundary flux unsigned",
                "status": "MISSING_BOUNDARY_FLUX_ZERO_OR_BOUND",
                "if_missing": "positive no-hair identity cannot conclude Xhat=0",
            },
            {
                "audit_id": "PHA3093_7_prefactor",
                "object": "K_X=s_X/(4*pi*Z_X*G_obs)",
                "required_evidence": "normalization convention, sign s_X, G_obs frame and source/test charges",
                "current_evidence": "alpha source rows remain schema-ready values-missing",
                "status": "MISSING_ALPHA_NORMALIZATION",
                "if_missing": "alpha(lambda) row remains smoke-only",
            },
            {
                "audit_id": "PHA3093_8_verdict",
                "object": "parent Xhat/Hessian ownership",
                "required_evidence": "PX3093 and PHA3093_0 through PHA3093_7 close from one parent branch",
                "current_evidence": "none of the parent-owned owner/value/sign/source rows close",
                "status": "FAIL_CURRENT_CLAIM",
                "if_missing": "move to parent metric/eigenvalue theorem or source-zero/bounded coupling row",
            },
        ]
    )


def normalization_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "lock_id": "FNL3093_0_invariant",
                "target": "identify physical finite-range invariant",
                "condition": "beta_eff=ell_vac^2 M_X^2/Z_X or equivalent parent-normalized Hessian eigenvalue",
                "current_status": "CONDITIONAL_INVARIANT_IDENTIFIED",
                "allowed_use": "theorem target and normalization guard",
                "forbidden_use": "claim that rho_vac alone predicts lambda_X",
            },
            {
                "lock_id": "FNL3093_1_canonical_metric",
                "target": "make vacuum density set the field-space metric",
                "condition": "Z_X f_X^2=rho_vac^(1/2)",
                "current_status": "CLEAN_CONTRACT_NOT_SIGNED",
                "allowed_use": "parent Ward/metric theorem target",
                "forbidden_use": "normalization chosen after R10 pressure",
            },
            {
                "lock_id": "FNL3093_2_beta3",
                "target": "low-scrutiny finite theorem target",
                "condition": "U''(0)=3 from spatial trace/eigenvalue theorem",
                "current_status": "BEST_CONDITIONAL_TARGET_NOT_SIGNED",
                "allowed_use": "private derivation target",
                "forbidden_use": "predicted beta/lambda claim",
            },
            {
                "lock_id": "FNL3093_3_direct_range",
                "target": "direct range backsolve",
                "condition": "choose beta/lambda after seeing local bound pressure",
                "current_status": "CLOSURE_ONLY_FORBIDDEN_AS_DERIVATION",
                "allowed_use": "sanity check only",
                "forbidden_use": "evidence or prediction",
            },
            {
                "lock_id": "FNL3093_4_CX_tie",
                "target": "tie range normalization to source amplitude",
                "condition": "same parent normalization fixes lambda_X and C_X/K_X/qbar_XT/Qbar_XH",
                "current_status": "MISSING_COUPLING_NORMALIZATION_LEDGER",
                "allowed_use": "next source-row schema",
                "forbidden_use": "choose range and amplitude independently",
            },
        ]
    )


def alpha_template_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "row_id": "ASR3093_0_bulk_Hessian",
                "quantity": "Xhat;Z_X;M_X2;lambda_X",
                "formula": "lambda_X=sqrt(Z_X/M_X2)",
                "required_columns": "system_id;field_id;branch_id;Xhat_owner;Z_X;M_X2;lambda_X;Z_units;M_units;lambda_units;source_path;valid_for_claim",
                "current_status": "MISSING_PARENT_INPUT",
                "source_path": str(OUTPUTS["hessian"]),
            },
            {
                "row_id": "ASR3093_1_field_metric_beta",
                "quantity": "Z_X f_X^2;Upp0;beta_eff",
                "formula": "beta_eff=Upp0*rho_vac^(1/2)/(Z_X*f_X^2)",
                "required_columns": "system_id;branch_id;ZX_fX2;Upp0;beta_eff;metric_units;source_path;valid_for_claim",
                "current_status": "MISSING_PARENT_METRIC_AND_EIGENVALUE",
                "source_path": str(RESIDUALS / "P8_Y5_R10_1026_PARENT_METRIC_ATTEMPT.csv"),
            },
            {
                "row_id": "ASR3093_2_source_current",
                "quantity": "J_X or qbar_XT",
                "formula": "J_X=delta_X S_matter + hidden/source/domain terms",
                "required_columns": "system_id;matter_sector;qbar_XT;J_X;J_X_bound;units;source_path;valid_for_claim",
                "current_status": "MISSING_SOURCE_ZERO_OR_BOUND",
                "source_path": str(OUTPUTS["hessian"]),
            },
            {
                "row_id": "ASR3093_3_Hamiltonian_projection",
                "quantity": "Qbar_XH",
                "formula": "Qbar_XH(lambda)=Pi_M^H[Q_X^H(lambda)]/M_H",
                "required_columns": "system_id;source_body;Q_XH;Qbar_XH;projector;units;source_path;valid_for_claim",
                "current_status": "MISSING_ARENA_PROJECTION",
                "source_path": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1847_ALPHA_SOURCE_ROW_TEMPLATE.csv"),
            },
            {
                "row_id": "ASR3093_4_green_prefactor",
                "quantity": "K_X",
                "formula": "K_X=s_X/(4*pi*Z_X*G_obs)",
                "required_columns": "system_id;K_X;s_X;Z_X;G_obs;normalization;units;source_path;valid_for_claim",
                "current_status": "MISSING_ALPHA_NORMALIZATION",
                "source_path": str(OUTPUTS["normalization"]),
            },
            {
                "row_id": "ASR3093_5_candidate_alpha",
                "quantity": "alpha_bulk(lambda_X)",
                "formula": "alpha_bulk(lambda_X)=K_X*Qbar_XH(lambda_X)*qbar_XT",
                "required_columns": "system_id;lambda_X;K_X;Qbar_XH;qbar_XT;alpha_bulk;alpha_bound;source_paths;valid_for_claim",
                "current_status": "SCHEMA_READY_VALUES_MISSING",
                "source_path": str(OUTPUTS["alpha_template"]),
            },
        ]
    )


def direct_product_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "bridge_id": "DPB3093_0_WEP_threshold",
                "object": "P_WEP_alpha_direct bound",
                "status": "NUMERIC_THRESHOLD_NONCLAIM_EXISTS",
                "value": "4.797780522732e-05",
                "units": "dimensionless",
                "meaning": "private WEP product threshold can score a future direct MTS product row",
            },
            {
                "bridge_id": "DPB3093_1_MTS_prediction",
                "object": "MTS direct WEP/R10 product prediction",
                "status": "MISSING_MTS_DIRECT_PRODUCT",
                "value": "MISSING",
                "units": "dimensionless",
                "meaning": "requires parent Xhat action/matter response or explicit source-backed product",
            },
            {
                "bridge_id": "DPB3093_2_verdict",
                "object": "direct product bridge",
                "status": "BOUND_SIDE_READY_PREDICTION_SIDE_MISSING",
                "value": "not_run",
                "units": "dimensionless",
                "meaning": "do not scrape more bound data until MTS prediction owner exists",
            },
        ]
    )


def verdict_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "verdict_id": "BV3093_0_Xhat_owner",
                "branch": "parent Xhat owner",
                "status": "PARENT_ACTION_CLAUSE_NOT_DERIVED",
                "because": "no source makes Xhat the field varied in the parent action and the same variable controlling visible coefficients",
                "allowed_statement": "MTS has an exact parent-owner contract",
                "forbidden_statement": "chi_X/Xhat is already the physical scalar",
                "next_action": "try parent metric/eigenvalue theorem or direct source product row",
            },
            {
                "verdict_id": "BV3093_1_Hessian_formula",
                "branch": "parent Hessian route",
                "status": "CONTRACT_DERIVED_NOT_OWNED",
                "because": "second variation/range law is exact, but current files do not supply parent-signed Xhat, Z_X, M_X^2 or units",
                "allowed_statement": "MTS has a precise Hessian contract for local scalar route",
                "forbidden_statement": "MTS predicts lambda_X or passes local tests from this route",
                "next_action": "derive parent field-space metric and Hessian eigenvalue",
            },
            {
                "verdict_id": "BV3093_2_alpha_source_row",
                "branch": "residual alpha/source fallback",
                "status": "SCHEMA_READY_VALUES_MISSING",
                "because": "K_X, Qbar_XH, qbar_XT, Z_X, Xhat owner and lambda_X remain missing or unsigned",
                "allowed_statement": "fallback alpha rows are ready to receive sourced values",
                "forbidden_statement": "fallback alpha row is evidence",
                "next_action": "fill only after parent metric/eigenvalue or source-current coefficients exist",
            },
            {
                "verdict_id": "BV3093_3_direct_product",
                "branch": "direct WEP/R10 product",
                "status": "BOUND_SIDE_READY_PREDICTION_SIDE_MISSING",
                "because": "WEP product threshold exists but MTS has no parent-projected product prediction",
                "allowed_statement": "direct product scoring avoids fake factor splitting if prediction row is sourced",
                "forbidden_statement": "threshold alone supports MTS",
                "next_action": "use only after parent Xhat matter-response clause or numeric product row exists",
            },
            {
                "verdict_id": "BV3093_4_next_target",
                "branch": "next target",
                "status": "PARENT_METRIC_OR_SOURCE_ZERO_RETURN",
                "because": "Xhat owner/Hessian row failed; least fake next options are parent metric/eigenvalue or qbar_XT/J_X source-zero",
                "allowed_statement": "finite route is a private theorem target; source-zero remains cleaner for local GR",
                "forbidden_statement": "finite lambda or local-GR claim",
                "next_action": "3094-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return-under-AX1090.md",
            },
        ]
    )


def gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG3093_0_sources_registered", "3093 source chain exists", "source chain supports audit continuity only"),
        ("CG3093_1_parent_Xhat_owner", "same Xhat is parent-owned scalar/operator field", "PX3093_4_verdict=PARENT_XHAT_ACTION_CLAUSE_NOT_DERIVED"),
        ("CG3093_2_parent_block_owned", "single parent action owns Xhat block", "local block is conditional ansatz only"),
        ("CG3093_3_ZX_positive", "Z_X>0 is parent-signed", "kinetic Hessian sign and units are missing"),
        ("CG3093_4_MX2_positive", "M_X^2>0 is parent-signed", "mass-gap/eigenvalue theorem is missing"),
        ("CG3093_5_lambda_claim", "lambda_X is claim-grade", "same-branch values and length units are missing"),
        ("CG3093_6_alpha_source_claim", "alpha(lambda) row is claim-grade", "K_X, Qbar_XH, qbar_XT and bound comparison inputs are missing"),
        ("CG3093_7_local_GR_claim", "local GR/Newton reduction is derived", "Xhat/Hessian/source/boundary/no-pole routes remain unsigned"),
    ]
    return with_meta(
        [
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": False,
                "reason": reason,
                "claim_allowed": False,
                "claim_allowed_for_physics": False,
            }
            for gate_id, claim, reason in gates
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "decision_id": "DEC3093_0_exact_contract",
                "decision": "The exact parent Xhat/Hessian/range contract is now written in the current AX1090 branch.",
                "because": "second variation gives O_X, positivity conditions and lambda_X=sqrt(Z_X/M_X^2), while the parent Xhat clause states the owner requirement",
                "next_action": "do not re-derive the same formula; hunt parent metric/eigenvalue or source-zero owner",
            },
            {
                "decision_id": "DEC3093_1_no_claim",
                "decision": "Current MTS still does not own Xhat, Z_X, M_X^2, lambda_X or alpha.",
                "because": "required values, signs, units, cross-term controls, matter response and source coefficients are missing or conditional",
                "next_action": "keep local R10/PPN/local-GR claims blocked",
            },
            {
                "decision_id": "DEC3093_2_product_bridge",
                "decision": "Direct WEP product scoring is useful but prediction-side empty.",
                "because": "the bound-side product threshold exists, but no parent Xhat matter response yields an MTS product row",
                "next_action": "derive parent matter-response clause or source a direct product row later",
            },
            {
                "decision_id": "DEC3093_3_next_target",
                "decision": "Next target is parent metric/eigenvalue or source-zero return.",
                "because": "without parent field-space metric/eigenvalue, the finite Hessian route cannot be promoted; source-zero is cleaner for local GR if it can be signed",
                "next_action": "3094-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return-under-AX1090.md",
            },
        ]
    )


def next_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "route_id": "NEXT3093_0_primary",
                "next_checkpoint": "3094-Y5-R2FR-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return-under-AX1090.md",
                "script": "scripts/Y5_R2FR_parent_metric_ZXfX2_beta_eigenvalue_or_source_zero_return_under_AX1090_3094.py",
                "objective": "try to derive parent field-space metric lock Z_X f_X^2=rho_vac^(1/2) and beta eigenvalue; if unsigned, return to J_X/qbar_XT source-zero or bounded coupling rows",
                "selection_status": "selected",
                "success_condition": "parent M_AB/e_X/H_X spectrum signs the finite route, or finite route is frozen and source-zero/bounded coupling becomes primary",
            },
            {
                "route_id": "NEXT3093_1_parallel",
                "next_checkpoint": "3094b-Y5-R2FR-direct-WEP-R10-product-prediction-row-under-AX1090.md",
                "script": "scripts/Y5_R2FR_direct_WEP_R10_product_prediction_row_under_AX1090_3094b.py",
                "objective": "stage direct product prediction rows only if parent Xhat matter-response or numeric source kernels are available",
                "selection_status": "held",
                "success_condition": "no standalone beta/tau division, no tau=1 shortcut, no threshold-only claim",
            },
        ]
    )


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = {
        "parent_clause_copy": OUTPUTS["parent_clause"],
        "hessian_copy": OUTPUTS["hessian"],
        "alpha_template_copy": OUTPUTS["alpha_template"],
        "verdicts_copy": OUTPUTS["verdicts"],
        "next_copy": OUTPUTS["next"],
    }
    output_rows = []
    for key, source_path in copies.items():
        target_path = BRANCH_OUTPUTS[key]
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_path, target_path)
        output_rows.append(
            {
                **meta(),
                "copy_id": f"COPY3093_{key}",
                "source_path": str(source_path),
                "target_path": str(target_path),
                "target_exists": target_path.exists(),
            }
        )
    write_csv(OUTPUTS["branches"], output_rows)
    return output_rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join(["---"] * len(columns)) + " |",
    ]
    for row in output_rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    sections = [
        "# 3093 Y5 R2FR parent Xhat owner and Hessian ZX MX2 range or alpha source row under AX1090",
        "",
        "**Progress:** 3093 ports the parent-owner/Hessian contract into the current AX1090 branch. One parent `Xhat` must own the visible coefficient, no-hair operator, Hessian signs, range, and finite alpha/WEP/R10 product. This is the anti-knob rule.",
        "",
        "**Current verdict:** the exact second-variation/range law is derived, but current MTS does not yet own the parent `Xhat` action clause, `Z_X`, `M_X^2`, units, cross-Hessian block, source current, boundary flux, or alpha/product normalization. The fallback rows are schema-ready only.",
        "",
        "**Claim ceiling:** no parent-Xhat claim, finite-range prediction, alpha/product pass, R10/R11 pass, WEP/PPN/clock/orbital pass, local-GR/Newton reduction, GitHub action, or `formalization-workbench` edit is allowed from 3093.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "parse_ok", "needles_present", "missing_needles", "role"]),
        "",
        "## Parent Xhat Action Clause",
        markdown_table(data["parent_clause"], ["clause_id", "parent_action_clause", "must_satisfy", "current_status", "if_signed", "valid_for_claim"]),
        "",
        "## Second Variation Derivation",
        markdown_table(data["second_variation"], ["derivation_id", "step", "mathematical_statement", "derived_result", "status", "missing_for_claim", "valid_for_claim"]),
        "",
        "## Parent Hessian Audit",
        markdown_table(data["hessian"], ["audit_id", "object", "required_evidence", "current_evidence", "status", "if_missing", "valid_for_claim"]),
        "",
        "## Field Normalization Locks",
        markdown_table(data["normalization"], ["lock_id", "target", "condition", "current_status", "allowed_use", "forbidden_use", "valid_for_claim"]),
        "",
        "## Alpha Source Row Template",
        markdown_table(data["alpha_template"], ["row_id", "quantity", "formula", "required_columns", "current_status", "source_path", "valid_for_claim"]),
        "",
        "## Direct Product Bridge",
        markdown_table(data["direct_product"], ["bridge_id", "object", "status", "value", "units", "meaning", "valid_for_claim"]),
        "",
        "## Branch Verdicts",
        markdown_table(data["verdicts"], ["verdict_id", "branch", "status", "because", "allowed_statement", "forbidden_statement", "next_action", "valid_for_claim"]),
        "",
        "## Claim Gate",
        markdown_table(data["gates"], ["gate_id", "claim", "gate_pass", "reason", "claim_allowed_for_physics", "valid_for_claim"]),
        "",
        "## Decision Ledger",
        markdown_table(data["decisions"], ["decision_id", "decision", "because", "next_action", "valid_for_claim"]),
        "",
        "## Next Target",
        markdown_table(data["next"], ["route_id", "next_checkpoint", "script", "objective", "selection_status", "success_condition"]),
        "",
        "## Validation",
        markdown_table(data["validation"], ["validation_id", "check_pass", "detail", "artifact"]),
        "",
        "## Working Interpretation",
        "The finite scalar path is disciplined but not promoted: same parent field, same Hessian, same source normalization, same observed-frame readout. Since the owner row still fails, the next fair attack is either parent metric/eigenvalue ownership or source-zero/bounded coupling.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def contains_status(path: Path, field: str, expected: str) -> bool:
    return any(str(row.get(field, "")) == expected for row in rows(path))


def all_false(path: Path, field: str) -> bool:
    table = rows(path)
    return bool(table) and all(not boolish(row.get(field, "")) for row in table)


def validation_rows() -> list[dict[str, Any]]:
    formalization_3093 = list(FORMALIZATION.rglob("*3093*")) if FORMALIZATION.exists() else []
    checks = [
        ("VAL3093_00_sources_csv", csv_ok(OUTPUTS["sources"]), "source register parses", OUTPUTS["sources"]),
        ("VAL3093_01_sources_exist", all(boolish(row["exists"]) for row in rows(OUTPUTS["sources"])), "every cited local source path exists", OUTPUTS["sources"]),
        ("VAL3093_02_sources_parse", all(boolish(row["parse_ok"]) for row in rows(OUTPUTS["sources"])), "every cited csv source parses", OUTPUTS["sources"]),
        ("VAL3093_03_needles_present", all(boolish(row["needles_present"]) for row in rows(OUTPUTS["sources"])), "all source needles found", OUTPUTS["sources"]),
        ("VAL3093_04_doc_created", DOC.exists(), "checkpoint markdown created", DOC),
        ("VAL3093_05_parent_clause_parse", csv_ok(OUTPUTS["parent_clause"]), "parent Xhat action clause parses", OUTPUTS["parent_clause"]),
        ("VAL3093_06_parent_clause_blocks", contains_status(OUTPUTS["parent_clause"], "current_status", "PARENT_XHAT_ACTION_CLAUSE_NOT_DERIVED"), "parent Xhat clause remains unsigned", OUTPUTS["parent_clause"]),
        ("VAL3093_07_second_variation_parse", csv_ok(OUTPUTS["second_variation"]), "second variation derivation parses", OUTPUTS["second_variation"]),
        ("VAL3093_08_contract_written", contains_status(OUTPUTS["second_variation"], "status", "FAIL_CURRENT_CLAIM_CONTRACT_SHARPENED"), "second variation/range contract written but nonclaim", OUTPUTS["second_variation"]),
        ("VAL3093_09_hessian_parse", csv_ok(OUTPUTS["hessian"]), "parent Hessian audit parses", OUTPUTS["hessian"]),
        ("VAL3093_10_hessian_blocks", contains_status(OUTPUTS["hessian"], "status", "FAIL_CURRENT_CLAIM"), "parent Hessian ownership remains blocked", OUTPUTS["hessian"]),
        ("VAL3093_11_norm_parse", csv_ok(OUTPUTS["normalization"]), "field normalization locks parse", OUTPUTS["normalization"]),
        ("VAL3093_12_norm_contract_nonclaim", contains_status(OUTPUTS["normalization"], "current_status", "CLEAN_CONTRACT_NOT_SIGNED"), "canonical metric lock remains unsigned", OUTPUTS["normalization"]),
        ("VAL3093_13_alpha_template_parse", csv_ok(OUTPUTS["alpha_template"]), "alpha source template parses", OUTPUTS["alpha_template"]),
        ("VAL3093_14_alpha_schema_nonclaim", contains_status(OUTPUTS["alpha_template"], "current_status", "SCHEMA_READY_VALUES_MISSING") and all_false(OUTPUTS["alpha_template"], "valid_for_claim"), "alpha source row schema is complete and nonclaim", OUTPUTS["alpha_template"]),
        ("VAL3093_15_direct_product_parse", csv_ok(OUTPUTS["direct_product"]), "direct product bridge parses", OUTPUTS["direct_product"]),
        ("VAL3093_16_direct_product_missing", contains_status(OUTPUTS["direct_product"], "status", "BOUND_SIDE_READY_PREDICTION_SIDE_MISSING"), "direct product prediction side missing", OUTPUTS["direct_product"]),
        ("VAL3093_17_verdicts_parse", csv_ok(OUTPUTS["verdicts"]), "branch verdicts parse", OUTPUTS["verdicts"]),
        ("VAL3093_18_next_verdict", contains_status(OUTPUTS["verdicts"], "status", "PARENT_METRIC_OR_SOURCE_ZERO_RETURN"), "branch verdict selects parent metric/source-zero next", OUTPUTS["verdicts"]),
        ("VAL3093_19_gates_parse", csv_ok(OUTPUTS["gates"]), "claim gates parse", OUTPUTS["gates"]),
        ("VAL3093_20_gates_blocked", all_false(OUTPUTS["gates"], "claim_allowed_for_physics"), "all claim gates remain blocked", OUTPUTS["gates"]),
        ("VAL3093_21_decisions_parse", csv_ok(OUTPUTS["decisions"]), "decision ledger parses", OUTPUTS["decisions"]),
        ("VAL3093_22_next_parse", csv_ok(OUTPUTS["next"]), "next target parses", OUTPUTS["next"]),
        ("VAL3093_23_next_selected", contains_status(OUTPUTS["next"], "selection_status", "selected"), "primary next target selected", OUTPUTS["next"]),
        ("VAL3093_24_branch_copies_parse", csv_ok(OUTPUTS["branches"]), "branch copy ledger parses", OUTPUTS["branches"]),
        ("VAL3093_25_branch_copies_exist", all(boolish(row["target_exists"]) for row in rows(OUTPUTS["branches"])), "all branch copies exist", OUTPUTS["branches"]),
        ("VAL3093_26_no_formalization_edit", len(formalization_3093) == 0, "no 3093 files created under formalization-workbench", FORMALIZATION),
        ("VAL3093_27_pycache_removed", not PYCACHE.exists(), "scripts __pycache__ absent after run", PYCACHE),
    ]
    return [
        {
            **meta(),
            "validation_id": validation_id,
            "check_pass": bool(check_pass),
            "detail": detail,
            "artifact": str(artifact),
        }
        for validation_id, check_pass, detail, artifact in checks
    ]


def main() -> None:
    remove_pycache()
    for directory in [RESIDUALS, LOCAL_BOUNDS, RAB_QUEUE]:
        directory.mkdir(parents=True, exist_ok=True)

    data = {
        "sources": source_rows(),
        "parent_clause": parent_clause_rows(),
        "second_variation": second_variation_rows(),
        "hessian": hessian_rows(),
        "normalization": normalization_rows(),
        "alpha_template": alpha_template_rows(),
        "direct_product": direct_product_rows(),
        "verdicts": verdict_rows(),
        "gates": gate_rows(),
        "decisions": decision_rows(),
        "next": next_rows(),
    }

    for key, output_rows in data.items():
        write_csv(OUTPUTS[key], output_rows)

    data["branches"] = copy_branch_outputs()
    data["validation"] = []
    write_doc(data)
    data["validation"] = validation_rows()
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    passed = sum(1 for row in data["validation"] if boolish(row["check_pass"]))
    print(f"3093 parent Xhat/Hessian checkpoint written: {passed}/{len(data['validation'])} validation checks passed")
    print(DOC)
    print(OUTPUTS["validation"])


if __name__ == "__main__":
    main()
