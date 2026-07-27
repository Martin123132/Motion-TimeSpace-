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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"
PYCACHE = ROOT / "scripts" / "__pycache__"

CHECKPOINT = "3099"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "3099-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg-under-AX1090.md"

ALPHA_PPN_PROXY = 0.005788015401465051

SOURCES: dict[str, dict[str, Any]] = {
    "SRC3099_00_3098_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3098_NEXT_TARGET.csv",
        "needles": ["NEXT3098_0_primary", "canonical-X-normalization-and-range-gate"],
        "role": "3098 selects canonical X normalization and range gate for c_g.",
    },
    "SRC3099_01_3098_doc": {
        "path": ROOT / "3098-Y5-R2FR-PPN-common-frame-cg-translation-gate-under-AX1090.md",
        "needles": ["Current verdict", "N_X"],
        "role": "3098 states the direct c_g bound is blocked by N_X, tau_PPN, range, and contamination.",
    },
    "SRC3099_02_3098_derivation": {
        "path": RESIDUALS / "P8_Y5_R2FR_3098_COMMON_FRAME_DERIVATION.csv",
        "needles": ["DER3098_1_canonical_scalar", "DER3098_4_cg_translation"],
        "role": "3098 supplies the Cassini-to-c_g conditional derivation.",
    },
    "SRC3099_03_3098_bound": {
        "path": RESIDUALS / "P8_Y5_R2FR_3098_CG_CONDITIONAL_BOUND_ROW.csv",
        "needles": ["CGB3098_0_alpha_proxy", "MISSING_NX_TAU_PPN"],
        "role": "3098 supplies the source-backed alpha proxy and nonclaim c_g row.",
    },
    "SRC3099_04_3098_assumptions": {
        "path": RESIDUALS / "P8_Y5_R2FR_3098_SCALAR_TENSOR_ASSUMPTION_GATE.csv",
        "needles": ["AST3098_1_canonical_normalization", "AST3098_2_solar_system_range"],
        "role": "3098 identifies canonical normalization and range as explicit blocking gates.",
    },
    "SRC3099_05_1853_doc": {
        "path": ROOT / "1853-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg.md",
        "needles": ["rescaling-invariant effective coupling", "lambda_X=sqrt"],
        "role": "1853 precedent for invariant c_g/sqrt(Z_X) and range classification.",
    },
    "SRC3099_06_1853_canonical": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1853_CANONICAL_X_NORMALIZATION_DERIVATION.csv",
        "needles": ["CN1853_2_NX_definition", "CN1853_4_verdict"],
        "role": "1853 canonical X normalization derivation precedent.",
    },
    "SRC3099_07_1853_range": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1853_RANGE_TRANSFER_DERIVATION.csv",
        "needles": ["RG1853_1_lambda_relation", "RG1853_5_verdict"],
        "role": "1853 range transfer derivation precedent.",
    },
    "SRC3099_08_3093_hessian": {
        "path": RESIDUALS / "P8_Y5_R2FR_3093_PARENT_HESSIAN_AUDIT.csv",
        "needles": ["PHA3093_1_ZX_positive", "PHA3093_2_MX2_positive"],
        "role": "3093 current AX1090 parent Hessian audit.",
    },
    "SRC3099_09_3093_locks": {
        "path": RESIDUALS / "P8_Y5_R2FR_3093_FIELD_NORMALIZATION_LOCKS.csv",
        "needles": ["FNL3093_1_canonical_metric", "FNL3093_4_CX_tie"],
        "role": "3093 current AX1090 field normalization locks.",
    },
    "SRC3099_10_3094_beta": {
        "path": RESIDUALS / "P8_Y5_R2FR_3094_BETA_EIGENVALUE_ATTEMPT.csv",
        "needles": ["BE3094_4_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "3094 shows the parent eigenvalue/range theorem is still not signed.",
    },
    "SRC3099_11_1030_tau": {
        "path": RESIDUALS / "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv",
        "needles": ["CPG1030_3_tau_PPN", "MISSING_PPN_RESPONSE_MATRIX"],
        "role": "1030 provenance gate keeps tau_PPN source-missing.",
    },
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3099_SOURCE_REGISTER.csv",
    "canonical": RESIDUALS / "P8_Y5_R2FR_3099_CANONICAL_X_NORMALIZATION_DERIVATION.csv",
    "range": RESIDUALS / "P8_Y5_R2FR_3099_RANGE_TRANSFER_DERIVATION.csv",
    "classifier": RESIDUALS / "P8_Y5_R2FR_3099_RANGE_BRANCH_CLASSIFIER.csv",
    "zx_gate": RESIDUALS / "P8_Y5_R2FR_3099_ZX_MX2_TAUPPN_INPUT_GATE.csv",
    "bound": RESIDUALS / "P8_Y5_R2FR_3099_CG_NORMALIZED_BOUND_ROW.csv",
    "rescale": RESIDUALS / "P8_Y5_R2FR_3099_RESCALING_COUNTEREXAMPLE_AUDIT.csv",
    "branch_status": RESIDUALS / "P8_Y5_R2FR_3099_LOCAL_BRANCH_STATUS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_R2FR_3099_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3099_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3099_NEXT_TARGET.csv",
    "copies": RESIDUALS / "P8_Y5_R2FR_3099_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3099_VALIDATION.csv",
}

BRANCH_COPIES = {
    OUTPUTS["bound"]: LOCAL_BOUNDS / "cg_normalized_bound_3099_NONCLAIM.csv",
    OUTPUTS["classifier"]: LOCAL_BOUNDS / "range_branch_classifier_3099_NONCLAIM.csv",
    OUTPUTS["zx_gate"]: PARENT_ACTION / "Xhat_ZX_MX2_tauPPN_input_gate_3099_NOT_SIGNED.csv",
    OUTPUTS["rescale"]: PARENT_ACTION / "Xhat_rescaling_counterexample_3099_NONCLAIM.csv",
    OUTPUTS["next"]: RAB_QUEUE / "JR3099_parent_Hessian_tauPPN_extraction_NEXT_NONCLAIM.csv",
}


def base_row() -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "timestamp_utc": RUN_UTC,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def with_base(row: dict[str, Any]) -> dict[str, Any]:
    merged = base_row()
    merged.update(row)
    return merged


def ensure_dirs() -> None:
    for path in [RESIDUALS, LOCAL_BOUNDS, PARENT_ACTION, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def remove_pycache() -> None:
    if PYCACHE.exists():
        resolved = PYCACHE.resolve()
        if str(resolved).startswith(str(ROOT.resolve())):
            shutil.rmtree(resolved)


def sha256(path: Path) -> str:
    if not path.exists() or not path.is_file():
        return ""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        csv_rows(path)
    except Exception:
        return False
    return True


def write_csv(path: Path, rows: list[dict[str, Any]], field_order: list[str] | None = None) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    if field_order:
        fields.extend(field_order)
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def source_register() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, spec in SOURCES.items():
        path = Path(spec["path"])
        exists = path.exists()
        text = read_text(path) if exists else ""
        parses = csv_parses(path) if exists and path.suffix.lower() == ".csv" else exists
        missing = [needle for needle in spec["needles"] if needle not in text]
        rows.append(
            with_base(
                {
                    "source_id": source_id,
                    "path": str(path),
                    "exists": exists,
                    "parseable": parses,
                    "needles_found": not missing,
                    "missing_needles": ";".join(missing),
                    "sha256": sha256(path),
                    "role": spec["role"],
                }
            )
        )
    return rows


def canonical_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "CN3099_0_parent_quadratic_block",
            "statement": "A raw c_g statement is meaningful only after the same parent Xhat owns the kinetic Hessian, mass Hessian, and matter-frame response.",
            "equation": "S_X^(2)=(M_Pl^2/2) int sqrt(-g_E) [Z_X (partial Xhat)^2 - M_X^2 Xhat^2] + S_matter[A_g(Xhat)^2 g_E,psi]",
            "status": "CONDITIONAL_PARENT_BLOCK",
            "missing_for_claim": "parent-signed single Xhat block with Z_X, M_X^2, c_g, tau_PPN in one normalization",
            "claim_effect": "raw c_g cannot be compared to Cassini or R10",
        },
        {
            "step_id": "CN3099_1_canonical_field",
            "statement": "If Z_X is positive and constant in the local branch, the canonical field is fixed.",
            "equation": "phi = M_Pl sqrt(Z_X) Xhat",
            "status": "EXACT_IF_ZX_POSITIVE",
            "missing_for_claim": "numeric/source-backed Z_X>0",
            "claim_effect": "defines N_X but does not source it",
        },
        {
            "step_id": "CN3099_2_NX_definition",
            "statement": "PPN sees the derivative with respect to the canonical scalar, not the coordinate Xhat.",
            "equation": "N_X := dXhat/d(phi/M_Pl) = 1/sqrt(Z_X)",
            "status": "NORMALIZATION_LAW_DERIVED",
            "missing_for_claim": "Z_X value and units",
            "claim_effect": "replaces the 3098 placeholder N_X",
        },
        {
            "step_id": "CN3099_3_alpha_eff_definition",
            "statement": "The PPN scalar charge inherits arena projection and range/screening transfer.",
            "equation": "alpha_eff_PPN = tau_PPN c_g S_PPN(lambda_X,environment)/sqrt(Z_X)",
            "status": "INVARIANT_EFFECTIVE_COUPLING_FORM",
            "missing_for_claim": "tau_PPN, S_PPN, Z_X, lambda_X",
            "claim_effect": "Cassini can only bind alpha_eff_PPN until all factors are sourced",
        },
        {
            "step_id": "CN3099_4_rescaling_guard",
            "statement": "A field redefinition can change raw c_g without changing the physical coupling.",
            "equation": "Xhat' = a Xhat; c_g' = c_g/a; Z_X' = Z_X/a^2; c_g'/sqrt(Z_X') = sign(a) c_g/sqrt(Z_X)",
            "status": "NO_RESCALING_CHEAT_THEOREM",
            "missing_for_claim": "none for the guard; missing inputs remain for numeric bound",
            "claim_effect": "forbids scoring raw c_g as evidence",
        },
        {
            "step_id": "CN3099_5_verdict",
            "statement": "3099 closes the algebraic normalization law, but not the parent numerical inputs.",
            "equation": "abs(tau_PPN c_g S_PPN/sqrt(Z_X)) <= 0.005788015401465051",
            "status": "LAW_READY_INPUTS_MISSING",
            "missing_for_claim": "Z_X, tau_PPN, S_PPN(lambda_X,environment), same-parent ownership",
            "claim_effect": "direct c_g/local-GR PPN pass remains blocked",
        },
    ]
    return [with_base(row) for row in rows]


def range_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "step_id": "RG3099_0_hessian_ratio",
            "statement": "The same Hessian that canonically normalizes Xhat fixes the local range.",
            "equation": "mu_X^2 = M_X^2/Z_X",
            "status": "EXACT_IF_PARENT_HESSIAN_SIGNED",
            "missing_for_claim": "same-branch Z_X and M_X^2",
        },
        {
            "step_id": "RG3099_1_lambda_relation",
            "statement": "The static range is invariant under Xhat rescalings.",
            "equation": "lambda_X = 1/mu_X = sqrt(Z_X/M_X^2) in hbar=c=1 units; lambda_X=infinity if M_X^2=0",
            "status": "RANGE_LAW_DERIVED",
            "missing_for_claim": "numeric/source-backed M_X^2/Z_X",
        },
        {
            "step_id": "RG3099_2_ppn_transfer",
            "statement": "Cassini constrains only the long-range unscreened effective charge.",
            "equation": "alpha_eff_PPN(lambda_X)=tau_PPN c_g S_PPN(lambda_X,environment)/sqrt(Z_X)",
            "status": "TRANSFER_FORM_READY",
            "missing_for_claim": "S_PPN and tau_PPN response matrix",
        },
        {
            "step_id": "RG3099_3_r10_transfer",
            "statement": "If lambda_X is laboratory-short, the relevant arena becomes the R10/Yukawa alpha(lambda) curve, not Cassini.",
            "equation": "alpha_eff_R10(lambda_X)=tau_R10 c_g S_R10(lambda_X,apparatus)/sqrt(Z_X)",
            "status": "ARENA_SPLIT_FORM_READY",
            "missing_for_claim": "tau_R10, S_R10, real alpha(lambda_X) curve, Z_X",
        },
        {
            "step_id": "RG3099_4_instability_guard",
            "statement": "A negative M_X^2 is not a local-GR pass; it is a branch instability unless stabilized by a parent nonlinear theorem.",
            "equation": "M_X^2 < 0 -> tachyonic/local instability gate, not a fifth-force bound row",
            "status": "INSTABILITY_GATE",
            "missing_for_claim": "stabilizing parent theorem if M_X^2<0",
        },
        {
            "step_id": "RG3099_5_no_backsolve_policy",
            "statement": "The branch may not choose lambda_X after seeing Cassini/R10 pressure.",
            "equation": "lambda_X must come from parent Hessian inputs before empirical scoring",
            "status": "NO_POST_HOC_RANGE_FIT",
            "missing_for_claim": "parent-owned lambda_X",
        },
        {
            "step_id": "RG3099_6_verdict",
            "statement": "The range law is derived, but the current AX1090 branch remains unclassified.",
            "equation": "range_class = unknown because Z_X and M_X^2 are missing",
            "status": "RANGE_UNCLASSIFIED_CURRENT_BRANCH",
            "missing_for_claim": "Z_X and M_X^2 source rows",
        },
    ]
    return [with_base(row) for row in rows]


def classifier_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "class_id": "RBC3099_0_massless_or_solar_long",
            "condition": "M_X^2=0 or lambda_X much larger than the solar-system PPN impact scale with S_PPN near 1",
            "dominant_test": "Cassini/PPN plus orbital checks",
            "allowed_bound_use": "alpha_eff_PPN proxy can constrain tau_PPN c_g/sqrt(Z_X)",
            "current_status": "NOT_CLASSIFIED",
            "selected_current_branch": False,
        },
        {
            "class_id": "RBC3099_1_lab_short",
            "condition": "lambda_X in micrometer-to-millimeter laboratory range",
            "dominant_test": "Eot-Wash/R10 Yukawa alpha(lambda) curve",
            "allowed_bound_use": "R10 bound curve, not unsuppressed Cassini proxy",
            "current_status": "NOT_CLASSIFIED",
            "selected_current_branch": False,
        },
        {
            "class_id": "RBC3099_2_earth_or_orbital",
            "condition": "lambda_X comparable to Earth radius, Earth-Moon, AU, or source-support scales",
            "dominant_test": "WEP/orbital/LLR/finite-range PPN kernels",
            "allowed_bound_use": "finite-source geometry and no-cancellation vector envelope",
            "current_status": "NOT_CLASSIFIED",
            "selected_current_branch": False,
        },
        {
            "class_id": "RBC3099_3_screened_or_plateau",
            "condition": "local nonlinear screening or plateau suppresses effective scalar charge",
            "dominant_test": "screening-profile theorem plus lab/solar-system split",
            "allowed_bound_use": "only screened effective coupling is bounded until parent-to-local map closes",
            "current_status": "NOT_DERIVED",
            "selected_current_branch": False,
        },
        {
            "class_id": "RBC3099_4_tachyonic_or_unstable",
            "condition": "M_X^2<0 without a stabilizing parent nonlinear theorem",
            "dominant_test": "stability/regularity, not empirical local-GR pass",
            "allowed_bound_use": "none until stable vacuum branch is proven",
            "current_status": "NOT_CLASSIFIED",
            "selected_current_branch": False,
        },
        {
            "class_id": "RBC3099_5_current_AX1090",
            "condition": "Z_X, M_X^2, tau_PPN, and S_PPN are not source-backed in the active branch",
            "dominant_test": "none claim-grade",
            "allowed_bound_use": "record invariant formula and source-backed proxy only",
            "current_status": "SELECTED_CURRENT_STATUS",
            "selected_current_branch": True,
        },
    ]
    return [with_base(row) for row in rows]


def zx_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "gate_id": "ZMG3099_0_same_parent_owner",
            "needed_input": "same parent Xhat owns c_g, Z_X, M_X^2, source current, and local projection",
            "current_status": "NOT_PARENT_SIGNED",
            "blocks": "prevents comparing raw c_g to Cassini/R10",
            "next_evidence": "single parent action clause with all coefficients in one normalization",
            "gate_pass": False,
        },
        {
            "gate_id": "ZMG3099_1_ZX_positive",
            "needed_input": "Z_X>0 with units and field normalization",
            "current_status": "MISSING_ZX",
            "blocks": "prevents N_X=1/sqrt(Z_X) numeric bound",
            "next_evidence": "parent Hessian kinetic coefficient source row",
            "gate_pass": False,
        },
        {
            "gate_id": "ZMG3099_2_MX2_signed",
            "needed_input": "M_X^2>=0 or signed massless/stabilized theorem",
            "current_status": "MISSING_MX2",
            "blocks": "prevents lambda_X and arena classification",
            "next_evidence": "parent Hessian mass/eigenvalue coefficient source row",
            "gate_pass": False,
        },
        {
            "gate_id": "ZMG3099_3_tau_PPN",
            "needed_input": "tau_PPN response matrix from MTS variable to measured PPN gamma",
            "current_status": "MISSING_PPN_RESPONSE_MATRIX",
            "blocks": "prevents turning alpha_eff_PPN into a c_g component bound",
            "next_evidence": "linearized weak-field response matrix including gauge/readout conventions",
            "gate_pass": False,
        },
        {
            "gate_id": "ZMG3099_4_range_screening_transfer",
            "needed_input": "S_PPN(lambda_X, environment) or long-range unscreened certificate",
            "current_status": "MISSING_RANGE_SCREENING_TRANSFER",
            "blocks": "prevents deciding Cassini vs R10 vs orbital arena",
            "next_evidence": "lambda_X in metres and screening/profile theorem",
            "gate_pass": False,
        },
        {
            "gate_id": "ZMG3099_5_cross_sector_silence",
            "needed_input": "cross-Hessian, disformal, non-Hilbert, boundary, and support terms zero or included in residual vector",
            "current_status": "MISSING_CROSS_SECTOR_SILENCE",
            "blocks": "prevents one-parameter c_g PPN claim",
            "next_evidence": "block diagonalization theorem or PPN no-cancellation vector",
            "gate_pass": False,
        },
        {
            "gate_id": "ZMG3099_6_no_backsolve_lock",
            "needed_input": "lambda_X and Z_X sourced before empirical scoring",
            "current_status": "POLICY_LOCK_PASSED",
            "blocks": "forbids post-hoc range fitting but does not supply inputs",
            "next_evidence": "keep source rows nonclaim until parent inputs exist",
            "gate_pass": True,
        },
        {
            "gate_id": "ZMG3099_7_verdict",
            "needed_input": "all normalization/range/tau gates pass simultaneously",
            "current_status": "FAIL_CURRENT_CLAIM_NORMALIZATION_RANGE_MISSING",
            "blocks": "no direct c_g component bound, PPN pass, or local-GR/Newton reduction",
            "next_evidence": "3100 parent Hessian and tau_PPN extraction attempt",
            "gate_pass": False,
        },
    ]
    return [with_base(row) for row in rows]


def bound_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "bound_id": "NGB3099_0_alpha_proxy_input",
            "quantity": "alpha_PPN_proxy",
            "formula": "sqrt(delta_gamma/(2-delta_gamma)) from Cassini conservative envelope",
            "numeric_bound": f"{ALPHA_PPN_PROXY:.18g}",
            "units": "dimensionless",
            "source": "P8_Y5_R2FR_3098_CG_CONDITIONAL_BOUND_ROW.csv:CGB3098_0_alpha_proxy",
            "status": "SOURCE_BACKED_PROXY_NONCLAIM",
        },
        {
            "bound_id": "NGB3099_1_invariant_effective_ppn",
            "quantity": "alpha_eff_PPN",
            "formula": "alpha_eff_PPN=tau_PPN c_g S_PPN(lambda_X,env)/sqrt(Z_X)",
            "numeric_bound": f"abs(alpha_eff_PPN)<={ALPHA_PPN_PROXY:.18g}",
            "units": "dimensionless",
            "source": "CN3099_3_alpha_eff_definition",
            "status": "CONDITIONAL_INVARIANT_BOUND_FORMULA",
        },
        {
            "bound_id": "NGB3099_2_raw_cg_formula",
            "quantity": "c_g",
            "formula": "abs(c_g)<=alpha_PPN_proxy*sqrt(Z_X)/(abs(tau_PPN)*abs(S_PPN))",
            "numeric_bound": "MISSING_ZX_TAUPPN_SPPN",
            "units": "dimensionless_per_Xhat",
            "source": "CN3099_5_verdict",
            "status": "FORMULA_READY_COMPONENT_BOUND_MISSING",
        },
        {
            "bound_id": "NGB3099_3_rescaling_invariant_cg_over_sqrtZX",
            "quantity": "c_g/sqrt(Z_X)",
            "formula": "abs(tau_PPN*S_PPN*c_g/sqrt(Z_X))<=alpha_PPN_proxy",
            "numeric_bound": "MISSING_TAUPPN_SPPN",
            "units": "dimensionless",
            "source": "CN3099_4_rescaling_guard",
            "status": "INVARIANT_IDENTIFIED_TRANSFER_MISSING",
        },
        {
            "bound_id": "NGB3099_4_lab_short_range",
            "quantity": "alpha_eff_R10(lambda_X)",
            "formula": "alpha_eff_R10=tau_R10 c_g S_R10(lambda_X,apparatus)/sqrt(Z_X)",
            "numeric_bound": "MISSING_LAMBDAX_TAUR10_R10_CURVE",
            "units": "dimensionless",
            "source": "RG3099_3_r10_transfer",
            "status": "ARENA_TRANSFER_FORMULA_ONLY",
        },
        {
            "bound_id": "NGB3099_5_zero_route",
            "quantity": "c_g or tau_PPN",
            "formula": "parent theorem c_g=0 or tau_PPN=0 would silence the PPN scalar charge",
            "numeric_bound": "MISSING_ZERO_THEOREM",
            "units": "dimensionless",
            "source": "1030 and 3098 zero/translation gates",
            "status": "ZERO_ROUTE_NOT_PARENT_SIGNED",
        },
    ]
    return [with_base(row) for row in rows]


def rescale_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "case_id": "RCE3099_0_field_rescale",
            "operation": "Xhat_prime=a Xhat",
            "raw_effect": "c_g_prime=c_g/a and Z_X_prime=Z_X/a^2",
            "invariant_effect": "c_g_prime/sqrt(Z_X_prime)=sign(a)c_g/sqrt(Z_X)",
            "lesson": "raw c_g can be changed by notation",
            "blocks_raw_cg_claim": True,
        },
        {
            "case_id": "RCE3099_1_fake_small_cg",
            "operation": "choose large a after seeing a bound",
            "raw_effect": "raw c_g_prime becomes arbitrarily small",
            "invariant_effect": "alpha_eff_PPN unchanged when Z_X transforms with the same parent block",
            "lesson": "small raw c_g alone is not evidence",
            "blocks_raw_cg_claim": True,
        },
        {
            "case_id": "RCE3099_2_fake_large_cg",
            "operation": "choose small a after seeing a bound",
            "raw_effect": "raw c_g_prime becomes arbitrarily large",
            "invariant_effect": "alpha_eff_PPN unchanged when Z_X transforms with the same parent block",
            "lesson": "large raw c_g alone is not failure",
            "blocks_raw_cg_claim": True,
        },
        {
            "case_id": "RCE3099_3_range_invariant",
            "operation": "same Xhat rescaling in mass term",
            "raw_effect": "M_X2_prime=M_X2/a^2 and Z_X_prime=Z_X/a^2",
            "invariant_effect": "M_X2_prime/Z_X_prime=M_X2/Z_X, so lambda_X is unchanged",
            "lesson": "range must be parent-owned, not chosen by field coordinates",
            "blocks_raw_cg_claim": True,
        },
        {
            "case_id": "RCE3099_4_verdict",
            "operation": "attempt to score raw c_g",
            "raw_effect": "coordinate-dependent",
            "invariant_effect": "only tau_PPN c_g S_PPN/sqrt(Z_X) is PPN-facing",
            "lesson": "direct raw c_g claim is rejected until normalization is signed",
            "blocks_raw_cg_claim": True,
        },
    ]
    return [with_base(row) for row in rows]


def branch_status_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "status_id": "LBS3099_0_math_progress",
            "branch": "canonical normalization and range algebra",
            "status": "DERIVED_CONDITIONAL_LAWS",
            "meaning": "N_X=1/sqrt(Z_X), lambda_X=sqrt(Z_X/M_X^2), and alpha_eff_PPN=tau_PPN c_g S_PPN/sqrt(Z_X)",
            "claim_allowed_now": False,
        },
        {
            "status_id": "LBS3099_1_current_AX1090",
            "branch": "current parent/local branch",
            "status": "FAIL_CURRENT_CLAIM_INPUTS_MISSING",
            "meaning": "Z_X, M_X^2, tau_PPN, S_PPN, and cross-sector silence are not signed",
            "claim_allowed_now": False,
        },
        {
            "status_id": "LBS3099_2_best_next_route",
            "branch": "derivation-first route",
            "status": "MOVE_TO_PARENT_HESSIAN_AND_TAUPPN_EXTRACTION",
            "meaning": "try to source Z_X/M_X^2/tau_PPN from parent action before any local-GR/PPN claim",
            "claim_allowed_now": False,
        },
    ]
    return [with_base(row) for row in rows]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "claim_id": "CG3099_0_alpha_proxy",
            "claim": "Cassini alpha_PPN proxy exists as a source-backed benchmark",
            "evidence": "3098 Cassini row and 3099 invariant formula",
            "allowed": True,
            "claim_allowed_for_physics": False,
            "reason": "benchmark only; not an MTS prediction row",
        },
        {
            "claim_id": "CG3099_1_invariant_formula",
            "claim": "PPN-facing invariant is tau_PPN c_g S_PPN/sqrt(Z_X)",
            "evidence": "canonical normalization and range derivation",
            "allowed": True,
            "claim_allowed_for_physics": False,
            "reason": "conditional theorem; numeric inputs missing",
        },
        {
            "claim_id": "CG3099_2_direct_cg_bound",
            "claim": "raw c_g is directly bounded by Cassini",
            "evidence": "blocked by ZMG3099 and RCE3099",
            "allowed": False,
            "claim_allowed_for_physics": False,
            "reason": "coordinate-dependent without Z_X/tau/range transfer",
        },
        {
            "claim_id": "CG3099_3_ppn_pass",
            "claim": "MTS passes PPN/local-GR reduction",
            "evidence": "blocked by missing response matrix and contamination silence",
            "allowed": False,
            "claim_allowed_for_physics": False,
            "reason": "PPN residual vector not closed",
        },
        {
            "claim_id": "CG3099_4_local_GR_Newton",
            "claim": "local GR/Newton limit is derived",
            "evidence": "normalization/range gate is necessary but insufficient",
            "allowed": False,
            "claim_allowed_for_physics": False,
            "reason": "needs parent Hessian, matter frame, conservation, and PPN vector closure",
        },
    ]
    return [with_base(row) for row in rows]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "decision_id": "DEC3099_0_use_invariant_not_raw_cg",
            "decision": "score only the PPN-facing invariant alpha_eff_PPN",
            "rationale": "raw c_g is field-coordinate dependent; c_g/sqrt(Z_X) is the normalization-invariant object",
            "status": "adopted",
        },
        {
            "decision_id": "DEC3099_1_no_claim_from_current_inputs",
            "decision": "keep c_g rows nonclaim",
            "rationale": "Z_X, M_X^2, tau_PPN, S_PPN, and cross-sector silence are missing",
            "status": "adopted",
        },
        {
            "decision_id": "DEC3099_2_next_target",
            "decision": "try parent Hessian/tau_PPN extraction next",
            "rationale": "this is the shortest route to either a real local bound or a clean demotion to closure-only",
            "status": "selected",
        },
    ]
    return [with_base(row) for row in rows]


def next_rows() -> list[dict[str, Any]]:
    rows = [
        {
            "route_id": "NEXT3099_0_primary",
            "next_checkpoint": "3100-Y5-R2FR-parent-Hessian-and-tauPPN-extraction-for-cg-under-AX1090.md",
            "script": "scripts/Y5_R2FR_parent_Hessian_and_tauPPN_extraction_for_cg_under_AX1090_3100.py",
            "objective": "try to extract parent-owned Z_X, M_X^2, tau_PPN, and S_PPN inputs; if absent, state the exact parent-action clause required",
            "selection_status": "selected",
            "success_condition": "c_g gets a normalized/range-qualified source row, or the local PPN branch is explicitly closure-only until the parent action is extended",
        },
        {
            "route_id": "NEXT3099_1_parallel",
            "next_checkpoint": "3099b-Y5-R2FR-PPN-residual-vector-no-cancellation-envelope-under-AX1090.md",
            "script": "scripts/Y5_R2FR_PPN_residual_vector_no_cancellation_envelope_under_AX1090_3099b.py",
            "objective": "derive the multi-component PPN residual vector over c_g, disformal, non-Hilbert, support, and boundary terms",
            "selection_status": "held",
            "success_condition": "PPN constraints become an absolute vector envelope rather than a one-parameter proxy",
        },
    ]
    return [with_base(row) for row in rows]


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source, target in BRANCH_COPIES.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        rows.append(
            with_base(
                {
                    "copy_id": f"COPY3099_{len(rows)}",
                    "source": str(source),
                    "target": str(target),
                    "target_exists": target.exists(),
                    "target_sha256": sha256(target),
                    "purpose": "nonclaim branch handoff copy",
                }
            )
        )
    return rows


def md_escape(value: Any) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> list[str]:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return lines


def validation_rows() -> list[dict[str, Any]]:
    validations: list[dict[str, Any]] = []

    def add(validation_id: str, check_pass: bool, detail: str, artifact: Path | str) -> None:
        validations.append(
            with_base(
                {
                    "validation_id": validation_id,
                    "check_pass": bool(check_pass),
                    "detail": detail,
                    "artifact": str(artifact),
                }
            )
        )

    sources = csv_rows(OUTPUTS["sources"])
    canonical = csv_rows(OUTPUTS["canonical"])
    range_transfer = csv_rows(OUTPUTS["range"])
    classifier = csv_rows(OUTPUTS["classifier"])
    zx_gate = csv_rows(OUTPUTS["zx_gate"])
    bounds = csv_rows(OUTPUTS["bound"])
    rescale = csv_rows(OUTPUTS["rescale"])
    branch_status = csv_rows(OUTPUTS["branch_status"])
    claim_gate = csv_rows(OUTPUTS["claim_gate"])
    decisions = csv_rows(OUTPUTS["decision"])
    next_targets = csv_rows(OUTPUTS["next"])

    add("VAL3099_00_sources_csv", OUTPUTS["sources"].exists(), "source register exists", OUTPUTS["sources"])
    add("VAL3099_01_sources_exist", all(row["exists"] == "True" for row in sources), "every cited source path exists", OUTPUTS["sources"])
    add("VAL3099_02_sources_parse", all(row["parseable"] == "True" for row in sources), "every cited csv source parses", OUTPUTS["sources"])
    add("VAL3099_03_sources_needles", all(row["needles_found"] == "True" for row in sources), "all source needles found", OUTPUTS["sources"])
    add("VAL3099_04_doc_exists", DOC.exists(), "checkpoint doc exists", DOC)
    add("VAL3099_05_canonical_parses", csv_parses(OUTPUTS["canonical"]), "canonical derivation csv parses", OUTPUTS["canonical"])
    add("VAL3099_06_NX_law", any(row.get("step_id") == "CN3099_2_NX_definition" and "1/sqrt(Z_X)" in row.get("equation", "") for row in canonical), "N_X law recorded", OUTPUTS["canonical"])
    add("VAL3099_07_invariant_formula", any(row.get("step_id") == "CN3099_3_alpha_eff_definition" and "S_PPN" in row.get("equation", "") for row in canonical), "PPN-facing invariant formula recorded", OUTPUTS["canonical"])
    add("VAL3099_08_rescaling_guard", any(row.get("step_id") == "CN3099_4_rescaling_guard" and "c_g/sqrt(Z_X)" in row.get("equation", "") for row in canonical), "rescaling guard recorded", OUTPUTS["canonical"])
    add("VAL3099_09_range_parses", csv_parses(OUTPUTS["range"]), "range derivation csv parses", OUTPUTS["range"])
    add("VAL3099_10_lambda_law", any(row.get("step_id") == "RG3099_1_lambda_relation" and "sqrt(Z_X/M_X^2)" in row.get("equation", "") for row in range_transfer), "lambda law recorded", OUTPUTS["range"])
    add("VAL3099_11_no_backsolve", any(row.get("step_id") == "RG3099_5_no_backsolve_policy" for row in range_transfer), "no post-hoc range fitting policy recorded", OUTPUTS["range"])
    add("VAL3099_12_classifier_current", any(row.get("class_id") == "RBC3099_5_current_AX1090" and row.get("selected_current_branch") == "True" for row in classifier), "current branch selected as unclassified/input-missing", OUTPUTS["classifier"])
    add("VAL3099_13_zx_gate_parses", csv_parses(OUTPUTS["zx_gate"]), "Z_X/M_X2/tau gate csv parses", OUTPUTS["zx_gate"])
    add("VAL3099_14_zx_gate_verdict_fail", any(row.get("gate_id") == "ZMG3099_7_verdict" and row.get("current_status") == "FAIL_CURRENT_CLAIM_NORMALIZATION_RANGE_MISSING" for row in zx_gate), "gate verdict blocks claim", OUTPUTS["zx_gate"])
    add("VAL3099_15_required_inputs_block", all(row.get("gate_pass") == "False" for row in zx_gate if row.get("gate_id") != "ZMG3099_6_no_backsolve_lock"), "all physical input gates except policy lock remain blocked", OUTPUTS["zx_gate"])
    add("VAL3099_16_bound_parses", csv_parses(OUTPUTS["bound"]), "normalized bound csv parses", OUTPUTS["bound"])
    add("VAL3099_17_alpha_numeric", any(row.get("bound_id") == "NGB3099_0_alpha_proxy_input" and float(row.get("numeric_bound", "nan")) > 0 for row in bounds), "alpha proxy numeric positive", OUTPUTS["bound"])
    add("VAL3099_18_raw_cg_nonclaim", any(row.get("bound_id") == "NGB3099_2_raw_cg_formula" and row.get("numeric_bound") == "MISSING_ZX_TAUPPN_SPPN" for row in bounds), "raw c_g remains nonclaim", OUTPUTS["bound"])
    add("VAL3099_19_all_bounds_nonclaim", all(row.get("valid_for_claim") == "False" and row.get("claim_allowed") == "False" for row in bounds), "all bound rows are nonclaim", OUTPUTS["bound"])
    add("VAL3099_20_rescale_parses", csv_parses(OUTPUTS["rescale"]), "rescaling audit csv parses", OUTPUTS["rescale"])
    add("VAL3099_21_rescale_blocks_raw", all(row.get("blocks_raw_cg_claim") == "True" for row in rescale), "rescaling audit blocks raw c_g scoring", OUTPUTS["rescale"])
    add("VAL3099_22_branch_status_fail", any(row.get("status_id") == "LBS3099_1_current_AX1090" and row.get("status") == "FAIL_CURRENT_CLAIM_INPUTS_MISSING" for row in branch_status), "branch status records current failure to claim", OUTPUTS["branch_status"])
    add("VAL3099_23_claim_gate_blocks_direct", any(row.get("claim_id") == "CG3099_2_direct_cg_bound" and row.get("allowed") == "False" for row in claim_gate), "claim gate blocks direct c_g bound", OUTPUTS["claim_gate"])
    add("VAL3099_24_decision_selected", any(row.get("decision_id") == "DEC3099_2_next_target" and row.get("status") == "selected" for row in decisions), "next decision selected", OUTPUTS["decision"])
    add("VAL3099_25_next_primary", any(row.get("route_id") == "NEXT3099_0_primary" and row.get("selection_status") == "selected" for row in next_targets), "primary next target selected", OUTPUTS["next"])
    add("VAL3099_26_branch_copies_exist", all(target.exists() for target in BRANCH_COPIES.values()), "all branch handoff copies exist", OUTPUTS["copies"])
    add("VAL3099_27_branch_copies_parse", all(csv_parses(target) for target in BRANCH_COPIES.values()), "all branch handoff copies parse", OUTPUTS["copies"])
    fw_hits = list(FORMALIZATION.rglob("*3099*")) if FORMALIZATION.exists() else []
    add("VAL3099_28_formalization_untouched", len(fw_hits) == 0, "no formalization-workbench 3099 artifacts exist", FORMALIZATION)
    add("VAL3099_29_pycache_removed", not PYCACHE.exists(), "scripts __pycache__ absent after run", PYCACHE)
    return validations


def write_doc(data: dict[str, list[dict[str, Any]]]) -> None:
    lines: list[str] = [
        "# 3099 - Y5 R2FR canonical X normalization and range gate for c_g under AX1090",
        "",
        f"**Progress:** 3099 derives the normalization/range law that 3098 left as `N_X` and `lambda_X` placeholders. The PPN-facing quantity is not raw `c_g`; it is `alpha_eff_PPN = tau_PPN c_g S_PPN(lambda_X,environment)/sqrt(Z_X)`.",
        "",
        "**Current verdict:** this is real progress but not a local-GR/PPN pass. The algebra is closed conditionally, while the active AX1090 branch still lacks parent-signed `Z_X`, `M_X^2`, `tau_PPN`, `S_PPN`, and cross-sector silence.",
        "",
        "**Claim ceiling:** no direct `c_g` component bound, PPN pass, local-GR/Newton reduction, R10 pass, GitHub action, or `formalization-workbench` edit is allowed from 3099.",
        "",
        "## Source Register",
        *md_table(data["sources"], ["source_id", "path", "exists", "parseable", "needles_found", "missing_needles", "role"]),
        "",
        "## Canonical X Normalization",
        *md_table(data["canonical"], ["step_id", "statement", "equation", "status", "missing_for_claim", "claim_effect"]),
        "",
        "## Range Transfer",
        *md_table(data["range"], ["step_id", "statement", "equation", "status", "missing_for_claim"]),
        "",
        "## Range Branch Classifier",
        *md_table(data["classifier"], ["class_id", "condition", "dominant_test", "allowed_bound_use", "current_status", "selected_current_branch"]),
        "",
        "## Z_X / M_X^2 / tau_PPN Input Gate",
        *md_table(data["zx_gate"], ["gate_id", "needed_input", "current_status", "blocks", "next_evidence", "gate_pass"]),
        "",
        "## Normalized Bound Rows",
        *md_table(data["bound"], ["bound_id", "quantity", "formula", "numeric_bound", "units", "source", "status"]),
        "",
        "## Rescaling Counterexample Audit",
        *md_table(data["rescale"], ["case_id", "operation", "raw_effect", "invariant_effect", "lesson", "blocks_raw_cg_claim"]),
        "",
        "## Local Branch Status",
        *md_table(data["branch_status"], ["status_id", "branch", "status", "meaning", "claim_allowed_now"]),
        "",
        "## Claim Gate",
        *md_table(data["claim_gate"], ["claim_id", "claim", "evidence", "allowed", "claim_allowed_for_physics", "reason"]),
        "",
        "## Decision Ledger",
        *md_table(data["decision"], ["decision_id", "decision", "rationale", "status"]),
        "",
        "## Next Target",
        *md_table(data["next"], ["route_id", "next_checkpoint", "script", "objective", "selection_status", "success_condition"]),
        "",
        "## Branch Copies",
        *md_table(data["copies"], ["copy_id", "source", "target", "target_exists", "purpose"]),
        "",
        "## Validation",
        *md_table(data["validation"], ["validation_id", "check_pass", "detail", "artifact"]),
        "",
    ]
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    ensure_dirs()
    remove_pycache()

    data = {
        "sources": source_register(),
        "canonical": canonical_rows(),
        "range": range_rows(),
        "classifier": classifier_rows(),
        "zx_gate": zx_gate_rows(),
        "bound": bound_rows(),
        "rescale": rescale_rows(),
        "branch_status": branch_status_rows(),
        "claim_gate": claim_gate_rows(),
        "decision": decision_rows(),
        "next": next_rows(),
    }

    write_csv(OUTPUTS["sources"], data["sources"])
    write_csv(OUTPUTS["canonical"], data["canonical"])
    write_csv(OUTPUTS["range"], data["range"])
    write_csv(OUTPUTS["classifier"], data["classifier"])
    write_csv(OUTPUTS["zx_gate"], data["zx_gate"])
    write_csv(OUTPUTS["bound"], data["bound"])
    write_csv(OUTPUTS["rescale"], data["rescale"])
    write_csv(OUTPUTS["branch_status"], data["branch_status"])
    write_csv(OUTPUTS["claim_gate"], data["claim_gate"])
    write_csv(OUTPUTS["decision"], data["decision"])
    write_csv(OUTPUTS["next"], data["next"])

    data["copies"] = copy_rows()
    write_csv(OUTPUTS["copies"], data["copies"])

    remove_pycache()
    data["validation"] = []
    write_doc(data)
    data["validation"] = validation_rows()
    write_csv(OUTPUTS["validation"], data["validation"])
    write_doc(data)
    remove_pycache()

    passed = sum(1 for row in data["validation"] if row["check_pass"])
    total = len(data["validation"])
    print(f"3099 canonical X/range gate written: {passed}/{total} validation checks passed")
    print(DOC)
    print(OUTPUTS["validation"])


if __name__ == "__main__":
    main()
