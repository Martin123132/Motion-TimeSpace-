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

CHECKPOINT = "3098"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "3098-Y5-R2FR-PPN-common-frame-cg-translation-gate-under-AX1090.md"

SOURCES: dict[str, dict[str, Any]] = {
    "SRC3098_00_3097_next": {
        "path": RESIDUALS / "P8_Y5_R2FR_3097_NEXT_TARGET.csv",
        "needles": ["NEXT3097_0_primary", "PPN-common-frame-cg-translation-gate"],
        "role": "3097 selects Cassini/PPN common-frame c_g translation gate.",
    },
    "SRC3098_01_3097_doc": {
        "path": ROOT / "3097-Y5-R2FR-first-real-local-coupling-bound-source-table-under-AX1090.md",
        "needles": ["OBS3097_2_PPN_CASSINI_2003", "MISSING_MTS_TO_PPN_MAP"],
        "role": "3097 supplies real Cassini anchor and blocks c_g-to-PPN translation.",
    },
    "SRC3098_02_1852_doc": {
        "path": ROOT / "1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md",
        "needles": ["scalar-tensor proxy", "not yet a direct MTS `c_g` bound"],
        "role": "1852 precedent for PPN common-frame c_g translation gate.",
    },
    "SRC3098_03_1852_ppn_bound": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_PPN_OBSERVABLE_BOUND.csv",
        "needles": ["PPN1852_0_cassini_gamma", "6.7e-05"],
        "role": "1852 Cassini observable and scalar-tensor proxy bound.",
    },
    "SRC3098_04_1852_derivation": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_COMMON_FRAME_DERIVATION.csv",
        "needles": ["DER1852_4_cg_translation", "MISSING, so c_g remains unbounded"],
        "role": "1852 conditional derivation from Cassini proxy to c_g.",
    },
    "SRC3098_05_1852_assumptions": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_SCALAR_TENSOR_ASSUMPTION_GATE.csv",
        "needles": ["AST1852_5_verdict", "FAIL_CURRENT_CLAIM"],
        "role": "1852 scalar-tensor assumption gate.",
    },
    "SRC3098_06_1852_failures": {
        "path": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_PPN_FAILURE_MODE_AUDIT.csv",
        "needles": ["PFM1852_0_rescaling", "PFM1852_3_multi_component_ppn"],
        "role": "1852 failure modes blocking direct c_g claim.",
    },
    "SRC3098_07_1030_spm_contract": {
        "path": RESIDUALS / "P8_Y5_R10_1030_PUBLIC_METRIC_ACTION_CONTRACT.csv",
        "needles": ["SPM1030_2_no_shadow_frame_slot", "EXACT_CLOSURE_CLAUSE_NOT_DERIVED"],
        "role": "1030 single-public-metric/no-shadow-frame contract.",
    },
    "SRC3098_08_1030_provenance": {
        "path": RESIDUALS / "P8_Y5_R10_1030_CG_PROVENANCE_GATE_BINDING.csv",
        "needles": ["CPG1030_3_tau_PPN", "MISSING_PPN_RESPONSE_MATRIX"],
        "role": "1030 c_g provenance/tau_PPN gate.",
    },
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3098_SOURCE_REGISTER.csv",
    "ppn_bound": RESIDUALS / "P8_Y5_R2FR_3098_PPN_OBSERVABLE_BOUND.csv",
    "derivation": RESIDUALS / "P8_Y5_R2FR_3098_COMMON_FRAME_DERIVATION.csv",
    "assumption_gate": RESIDUALS / "P8_Y5_R2FR_3098_SCALAR_TENSOR_ASSUMPTION_GATE.csv",
    "conditional_bound": RESIDUALS / "P8_Y5_R2FR_3098_CG_CONDITIONAL_BOUND_ROW.csv",
    "failure_audit": RESIDUALS / "P8_Y5_R2FR_3098_PPN_FAILURE_MODE_AUDIT.csv",
    "branch_status": RESIDUALS / "P8_Y5_R2FR_3098_LOCAL_BRANCH_STATUS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_R2FR_3098_CLAIM_GATE.csv",
    "decisions": RESIDUALS / "P8_Y5_R2FR_3098_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3098_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3098_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3098_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "ppn_bound_copy": LOCAL_BOUNDS / "PPN_observable_bound_3098_NONCLAIM.csv",
    "conditional_bound_copy": LOCAL_BOUNDS / "cg_conditional_bound_3098_NONCLAIM.csv",
    "failure_audit_copy": LOCAL_BOUNDS / "PPN_failure_mode_audit_3098_NONCLAIM.csv",
    "branch_status_copy": LOCAL_BOUNDS / "local_branch_status_3098_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3098_canonical_X_normalization_range_gate_NEXT_NONCLAIM.csv",
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


def alpha_proxy(delta_gamma: float) -> float:
    return (delta_gamma / (2.0 - delta_gamma)) ** 0.5


def ppn_bound_rows() -> list[dict[str, Any]]:
    delta_gamma = 6.7e-05
    return with_meta(
        [
            {
                "row_id": "PPN3098_0_cassini_gamma",
                "observable": "gamma_minus_1",
                "central_value": 2.1e-05,
                "one_sigma": 2.3e-05,
                "conservative_bound_value": delta_gamma,
                "bound_rule": "|central| + 2*sigma",
                "units": "dimensionless",
                "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
                "source_backed_observable": True,
            },
            {
                "row_id": "PPN3098_1_scalar_tensor_alpha0_proxy",
                "observable": "alpha0_abs_proxy",
                "central_value": "",
                "one_sigma": "",
                "conservative_bound_value": alpha_proxy(delta_gamma),
                "bound_rule": "from |gamma-1|=2 alpha0^2/(1+alpha0^2), alpha0^2 <= delta_gamma/(2-delta_gamma)",
                "units": "dimensionless",
                "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
                "source_backed_observable": True,
            },
        ]
    )


def derivation_rows() -> list[dict[str, Any]]:
    alpha_bound = alpha_proxy(6.7e-05)
    return with_meta(
        [
            {
                "step_id": "DER3098_0_common_frame_ansatz",
                "statement": "Assume ordinary matter sees a universal conformal frame g_matter=A_g(Xhat)^2 g_E.",
                "equation": "A_g(Xhat)=exp(c_g Xhat + O(Xhat^2))",
                "status": "CONDITIONAL_ANSATZ",
                "missing_for_MTS": "parent action has not signed universal common frame as the only local matter coupling",
            },
            {
                "step_id": "DER3098_1_canonical_scalar",
                "statement": "Introduce canonical scalar varphi with alpha_PPN=d ln A_g/d(varphi/M_Pl).",
                "equation": "alpha_PPN = N_X c_g, where N_X=dXhat/d(varphi/M_Pl)",
                "status": "NORMALIZATION_GATE",
                "missing_for_MTS": "N_X from Z_X and parent Hessian/range is not owned",
            },
            {
                "step_id": "DER3098_2_ppn_gamma_law",
                "statement": "For an unscreened massless single scalar-tensor limit, gamma-1=-2 alpha_PPN^2/(1+alpha_PPN^2).",
                "equation": "|alpha_PPN| <= sqrt(delta_gamma/(2-delta_gamma))",
                "status": "STANDARD_CONDITIONAL_RELATION",
                "missing_for_MTS": "MTS has not proven it reduces to this scalar-tensor PPN limit",
            },
            {
                "step_id": "DER3098_3_cassini_proxy_bound",
                "statement": "Using the conservative Cassini envelope gives a scalar-tensor proxy bound.",
                "equation": f"delta_gamma=6.7e-05; |alpha_PPN|<={alpha_bound:.12g}",
                "status": "NUMERIC_PROXY_DERIVED",
                "missing_for_MTS": "proxy is not a direct c_g bound until N_X, range and contamination gates pass",
            },
            {
                "step_id": "DER3098_4_cg_translation",
                "statement": "If N_X and tau_PPN are signed, c_g inherits the proxy through |N_X tau_PPN c_g| <= alpha0_abs_bound.",
                "equation": f"|c_g| <= {alpha_bound:.12g}/|N_X tau_PPN|",
                "status": "CONDITIONAL_BOUND_FORMULA_READY",
                "missing_for_MTS": "N_X and tau_PPN are MISSING, so c_g remains unbounded as an MTS component",
            },
        ]
    )


def assumption_gate_rows() -> list[dict[str, Any]]:
    rows_data = [
        ("AST3098_0_universal_conformal", "all ordinary matter sees one universal conformal frame A_g(Xhat)^2 g_E", "map c_g to PPN gamma", "NOT_PARENT_SIGNED", "species/frame/readout terms move PPN and WEP independently"),
        ("AST3098_1_canonical_normalization", "Xhat normalization is tied to the canonical scalar varphi/M_Pl", "turn alpha_PPN proxy into c_g bound", "MISSING_NX_FROM_ZX_HESSIAN", "c_g can be rescaled by field normalization"),
        ("AST3098_2_solar_system_range", "the X mode is effectively long-range across the Cassini solar-system impact scale", "use Cassini gamma without Yukawa/range suppression", "MISSING_MX2_OR_LAMBDA_SOLAR_SYSTEM_GATE", "finite range or screening suppresses Cassini and sends c_g to R10/orbital gates"),
        ("AST3098_3_no_screening", "no local screening, environmental plateau or nonlinear suppression changes the scalar charge", "apply weak-field scalar-tensor gamma law", "NOT_DERIVED", "Cassini bound constrains screened effective coupling, not parent c_g"),
        ("AST3098_4_no_disformal_nonhilbert_contamination", "b_dis, q_nonH, support and boundary terms do not contribute at the same PPN order", "isolate c_g as the gamma source", "MISSING_CONTAMINATION_ZERO_OR_BOUND", "PPN residual vector is multi-component, not a one-parameter c_g bound"),
        ("AST3098_5_verdict", "all scalar-tensor translation assumptions pass simultaneously", "promote alpha0 proxy to c_g component bound", "FAIL_CURRENT_CLAIM", "keep PPN result as source-backed conditional proxy only"),
    ]
    return with_meta(
        [
            {
                "assumption_id": assumption_id,
                "assumption": assumption,
                "needed_for": needed_for,
                "current_status": status,
                "failure_if_missing": failure,
                "gate_pass": False,
            }
            for assumption_id, assumption, needed_for, status, failure in rows_data
        ]
    )


def conditional_bound_rows() -> list[dict[str, Any]]:
    alpha_bound = alpha_proxy(6.7e-05)
    return with_meta(
        [
            {
                "bound_id": "CGB3098_0_alpha_proxy",
                "quantity": "alpha_PPN_proxy",
                "formula": "sqrt(delta_gamma/(2-delta_gamma))",
                "numeric_bound": alpha_bound,
                "units": "dimensionless",
                "source": "Cassini gamma_minus_1 conservative 2sigma envelope",
                "status": "SOURCE_BACKED_PROXY",
                "claim_allowed": False,
            },
            {
                "bound_id": "CGB3098_1_cg_conditional",
                "quantity": "c_g",
                "formula": "abs(c_g) <= alpha_PPN_proxy / abs(N_X tau_PPN)",
                "numeric_bound": "MISSING_NX_TAU_PPN",
                "units": "dimensionless_per_normalized_Xhat",
                "source": "DER3098_4_cg_translation",
                "status": "CONDITIONAL_FORMULA_READY_COMPONENT_BOUND_MISSING",
                "claim_allowed": False,
            },
            {
                "bound_id": "CGB3098_2_long_range_branch",
                "quantity": "c_g_long_range",
                "formula": "if lambda_X >> solar impact scale and N_X=tau_PPN=1, abs(c_g)<=alpha_PPN_proxy",
                "numeric_bound": alpha_bound,
                "units": "dimensionless",
                "source": "conditional scalar-tensor limit only",
                "status": "ILLUSTRATIVE_NOT_MTS_CLAIM",
                "claim_allowed": False,
            },
            {
                "bound_id": "CGB3098_3_finite_range_branch",
                "quantity": "c_g_finite_range",
                "formula": "Cassini response multiplied by range/screening transfer S_PPN(lambda_X, environment)",
                "numeric_bound": "MISSING_RANGE_TRANSFER",
                "units": "dimensionless",
                "source": "range gate required",
                "status": "BLOCKED_BY_RANGE_SCREENING",
                "claim_allowed": False,
            },
        ]
    )


def failure_rows() -> list[dict[str, Any]]:
    failures = [
        ("PFM3098_0_rescaling", "field normalization rescaling", "c_g is derivative with respect to Xhat; PPN sees canonical alpha_PPN", "derive N_X from Z_X/Hessian parent action"),
        ("PFM3098_1_range", "finite range or heavy local mode", "Cassini constrains long-range solar-system fields; short-range modes need R10/lab bounds", "derive M_X^2/lambda_X and solar-system transfer function"),
        ("PFM3098_2_screening", "environmental screening or plateau suppression", "Cassini would bound screened effective coupling, not parent coupling", "derive local screening map without smuggling plateau axiom"),
        ("PFM3098_3_multi_component_ppn", "b_dis/q_nonH/support/boundary terms contribute to gamma", "a single c_g bound would be fake if other residuals share the PPN channel", "derive PPN residual vector and absolute no-cancellation envelope"),
        ("PFM3098_4_matter_frame_nonuniversality", "source/test matter frames are not universal", "PPN and WEP constraints split into species-dependent charges", "parent matter functor/no-marker theorem or material sensitivity map"),
    ]
    return with_meta(
        [
            {
                "failure_id": failure_id,
                "failure_mode": mode,
                "why_it_matters": why,
                "required_fix": fix,
                "blocks_claim": True,
            }
            for failure_id, mode, why, fix in failures
        ]
    )


def branch_status_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "status_id": "LBS3098_0_if_all_gates_pass",
                "branch": "long-range scalar-tensor common-frame MTS",
                "result": "|N_X tau_PPN c_g| <= 0.0057880154",
                "status": "CONDITIONAL_COMPETITIVE_GATE",
                "claim_allowed": False,
            },
            {
                "status_id": "LBS3098_1_current_MTS",
                "branch": "current parent/local branch",
                "result": "Cassini source bound exists, but c_g is not directly bounded",
                "status": "FAIL_CURRENT_CLAIM_TRANSLATION_MISSING",
                "claim_allowed": False,
            },
            {
                "status_id": "LBS3098_2_best_next",
                "branch": "normalization/range repair",
                "result": "derive N_X and lambda_X transfer before claiming PPN/local GR",
                "status": "NEXT_TARGET",
                "claim_allowed": False,
            },
        ]
    )


def claim_gate_rows() -> list[dict[str, Any]]:
    gates = [
        ("CG3098_0_cassini_source", "Cassini PPN source bound is recorded", True, "gamma_minus_one conservative bound and alpha0 proxy are computed", True),
        ("CG3098_1_alpha_proxy", "scalar-tensor alpha0 proxy is computed", True, "standard conditional formula yields numeric proxy", True),
        ("CG3098_2_cg_component_bound", "MTS c_g is bounded by Cassini", False, "N_X, tau_PPN, range/screening and contamination gates fail current claim", False),
        ("CG3098_3_local_GR", "local GR branch passes PPN", False, "PPN residual vector and component bounds are not derived", False),
    ]
    return with_meta(
        [
            {
                "gate_id": gate_id,
                "claim": claim,
                "gate_pass": gate_pass,
                "reason": reason,
                "source_backed_proxy": source_proxy,
                "claim_allowed_for_physics": False,
            }
            for gate_id, claim, gate_pass, reason, source_proxy in gates
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "decision_id": "DEC3098_0_derivation_status",
                "decision": "The Cassini-to-alpha0 derivation is exact for the scalar-tensor proxy.",
                "because": "gamma law can be inverted cleanly and gives a numeric common-frame proxy",
                "next_action": "keep it as a benchmark bound, not a direct MTS claim",
            },
            {
                "decision_id": "DEC3098_1_current_block",
                "decision": "The direct c_g claim remains blocked.",
                "because": "field normalization, range/screening and residual-vector isolation are unsigned",
                "next_action": "derive N_X/lambda_X transfer from the parent Hessian and local range branch",
            },
            {
                "decision_id": "DEC3098_2_best_next",
                "decision": "Next target should be canonical X normalization and range gate.",
                "because": "without N_X and lambda_X, every c_g bound can be rescaled or range-suppressed",
                "next_action": "3099-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg-under-AX1090.md",
            },
        ]
    )


def next_rows() -> list[dict[str, Any]]:
    return with_meta(
        [
            {
                "route_id": "NEXT3098_0_primary",
                "next_checkpoint": "3099-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg-under-AX1090.md",
                "script": "scripts/Y5_R2FR_canonical_X_normalization_and_range_gate_for_cg_under_AX1090_3099.py",
                "objective": "derive N_X from Z_X/Hessian ownership and decide whether lambda_X is solar-system long-range, R10 short-range, screened, or still missing",
                "selection_status": "selected",
                "success_condition": "PPN c_g bound becomes normalized/range-qualified, or c_g remains source-only with explicit N_X/lambda_X blockers",
            },
            {
                "route_id": "NEXT3098_1_parallel",
                "next_checkpoint": "3099b-Y5-R2FR-PPN-residual-vector-no-cancellation-envelope-under-AX1090.md",
                "script": "scripts/Y5_R2FR_PPN_residual_vector_no_cancellation_envelope_under_AX1090_3099b.py",
                "objective": "derive the PPN residual vector over c_g, b_dis, q_nonH, support and boundary components",
                "selection_status": "held",
                "success_condition": "PPN no-cancellation vector is explicit enough for multi-component bounds",
            },
        ]
    )


def copy_branch_outputs() -> list[dict[str, Any]]:
    copies = {
        "ppn_bound_copy": OUTPUTS["ppn_bound"],
        "conditional_bound_copy": OUTPUTS["conditional_bound"],
        "failure_audit_copy": OUTPUTS["failure_audit"],
        "branch_status_copy": OUTPUTS["branch_status"],
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
                "copy_id": f"COPY3098_{key}",
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
        "# 3098 Y5 R2FR PPN common-frame c_g translation gate under AX1090",
        "",
        "**Progress:** 3098 derives the Cassini-to-scalar-tensor proxy in the current AX1090 branch. The conservative Cassini envelope `|gamma-1| <= 6.7e-05` gives `|alpha_PPN| <= 0.0057880154` under the standard unscreened massless scalar-tensor assumptions.",
        "",
        "**Current verdict:** this is not yet a direct MTS `c_g` bound. The parent branch still lacks `N_X`, `tau_PPN`, solar-system range/screening transfer, and proof that disformal/non-Hilbert/support terms are silent.",
        "",
        "**Claim ceiling:** no `c_g` component bound, PPN pass, local-GR/Newton reduction, R10 pass, GitHub action, or `formalization-workbench` edit is allowed from 3098.",
        "",
        "## Source Register",
        markdown_table(data["sources"], ["source_id", "source_path", "exists", "parse_ok", "needles_present", "missing_needles", "role"]),
        "",
        "## PPN Observable Bound",
        markdown_table(data["ppn_bound"], ["row_id", "observable", "central_value", "one_sigma", "conservative_bound_value", "bound_rule", "units", "source_url", "source_backed_observable", "valid_for_claim"]),
        "",
        "## Common-Frame Derivation",
        markdown_table(data["derivation"], ["step_id", "statement", "equation", "status", "missing_for_MTS", "valid_for_claim"]),
        "",
        "## Scalar-Tensor Assumption Gate",
        markdown_table(data["assumption_gate"], ["assumption_id", "assumption", "needed_for", "current_status", "failure_if_missing", "gate_pass", "valid_for_claim"]),
        "",
        "## c_g Conditional Bound Row",
        markdown_table(data["conditional_bound"], ["bound_id", "quantity", "formula", "numeric_bound", "units", "source", "status", "claim_allowed", "valid_for_claim"]),
        "",
        "## PPN Failure Mode Audit",
        markdown_table(data["failure_audit"], ["failure_id", "failure_mode", "why_it_matters", "required_fix", "blocks_claim", "valid_for_claim"]),
        "",
        "## Local Branch Status",
        markdown_table(data["branch_status"], ["status_id", "branch", "result", "status", "claim_allowed", "valid_for_claim"]),
        "",
        "## Claim Gate",
        markdown_table(data["claim_gate"], ["gate_id", "claim", "gate_pass", "reason", "source_backed_proxy", "claim_allowed_for_physics", "valid_for_claim"]),
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
        "Cassini is a harsh judge only after the MTS-to-PPN transfer exists. Right now it is a clean benchmark: strong enough to punish a long-range unscreened scalar-frame branch, but not honest as a direct `c_g` bound until normalization, range and multi-component PPN gates are derived.",
        "",
    ]
    DOC.write_text("\n".join(sections), encoding="utf-8")


def contains_status(path: Path, field: str, expected: str) -> bool:
    return any(str(row.get(field, "")) == expected for row in rows(path))


def all_false(path: Path, field: str) -> bool:
    table = rows(path)
    return bool(table) and all(not boolish(row.get(field, "")) for row in table)


def numeric_alpha_proxy_ok() -> bool:
    table = rows(OUTPUTS["ppn_bound"])
    alpha_rows = [row for row in table if row.get("observable") == "alpha0_abs_proxy"]
    if len(alpha_rows) != 1:
        return False
    try:
        value = float(alpha_rows[0]["conservative_bound_value"])
    except (KeyError, TypeError, ValueError):
        return False
    return 0.0057 < value < 0.0059


def validation_rows() -> list[dict[str, Any]]:
    formalization_3098 = list(FORMALIZATION.rglob("*3098*")) if FORMALIZATION.exists() else []
    checks = [
        ("VAL3098_00_sources_csv", csv_ok(OUTPUTS["sources"]), "source register parses", OUTPUTS["sources"]),
        ("VAL3098_01_sources_exist", all(boolish(row["exists"]) for row in rows(OUTPUTS["sources"])), "every cited local source path exists", OUTPUTS["sources"]),
        ("VAL3098_02_sources_parse", all(boolish(row["parse_ok"]) for row in rows(OUTPUTS["sources"])), "every cited csv source parses", OUTPUTS["sources"]),
        ("VAL3098_03_needles_present", all(boolish(row["needles_present"]) for row in rows(OUTPUTS["sources"])), "all source needles found", OUTPUTS["sources"]),
        ("VAL3098_04_doc_created", DOC.exists(), "checkpoint markdown created", DOC),
        ("VAL3098_05_ppn_bound_parse", csv_ok(OUTPUTS["ppn_bound"]), "PPN bound table parses", OUTPUTS["ppn_bound"]),
        ("VAL3098_06_gamma_bound_numeric", contains_status(OUTPUTS["ppn_bound"], "observable", "gamma_minus_1"), "Cassini gamma bound row exists", OUTPUTS["ppn_bound"]),
        ("VAL3098_07_alpha_proxy_numeric", numeric_alpha_proxy_ok(), "scalar-tensor alpha0 proxy is numeric and small", OUTPUTS["ppn_bound"]),
        ("VAL3098_08_derivation_parse", csv_ok(OUTPUTS["derivation"]), "common-frame derivation parses", OUTPUTS["derivation"]),
        ("VAL3098_09_derivation_conditional", contains_status(OUTPUTS["derivation"], "status", "CONDITIONAL_BOUND_FORMULA_READY"), "c_g conditional bound formula is present", OUTPUTS["derivation"]),
        ("VAL3098_10_assumption_parse", csv_ok(OUTPUTS["assumption_gate"]), "scalar-tensor assumption gate parses", OUTPUTS["assumption_gate"]),
        ("VAL3098_11_assumption_blocks", contains_status(OUTPUTS["assumption_gate"], "current_status", "FAIL_CURRENT_CLAIM"), "assumption gates block current MTS c_g claim", OUTPUTS["assumption_gate"]),
        ("VAL3098_12_conditional_bound_parse", csv_ok(OUTPUTS["conditional_bound"]), "conditional c_g bound table parses", OUTPUTS["conditional_bound"]),
        ("VAL3098_13_cg_bound_nonclaim", contains_status(OUTPUTS["conditional_bound"], "status", "CONDITIONAL_FORMULA_READY_COMPONENT_BOUND_MISSING") and all_false(OUTPUTS["conditional_bound"], "claim_allowed"), "c_g component bound remains nonclaim", OUTPUTS["conditional_bound"]),
        ("VAL3098_14_failure_parse", csv_ok(OUTPUTS["failure_audit"]), "failure audit parses", OUTPUTS["failure_audit"]),
        ("VAL3098_15_failures_block", all(boolish(row["blocks_claim"]) for row in rows(OUTPUTS["failure_audit"])), "all listed PPN failure modes block direct claim", OUTPUTS["failure_audit"]),
        ("VAL3098_16_branch_status_parse", csv_ok(OUTPUTS["branch_status"]), "branch status parses", OUTPUTS["branch_status"]),
        ("VAL3098_17_current_status_blocks", contains_status(OUTPUTS["branch_status"], "status", "FAIL_CURRENT_CLAIM_TRANSLATION_MISSING"), "current branch status blocks direct c_g bound", OUTPUTS["branch_status"]),
        ("VAL3098_18_claim_gate_parse", csv_ok(OUTPUTS["claim_gate"]), "claim gate parses", OUTPUTS["claim_gate"]),
        ("VAL3098_19_claims_blocked", all_false(OUTPUTS["claim_gate"], "claim_allowed_for_physics"), "all physics claims remain blocked", OUTPUTS["claim_gate"]),
        ("VAL3098_20_decisions_parse", csv_ok(OUTPUTS["decisions"]), "decision ledger parses", OUTPUTS["decisions"]),
        ("VAL3098_21_next_parse", csv_ok(OUTPUTS["next"]), "next target parses", OUTPUTS["next"]),
        ("VAL3098_22_next_selected", contains_status(OUTPUTS["next"], "selection_status", "selected"), "primary next target selected", OUTPUTS["next"]),
        ("VAL3098_23_branch_copies_parse", csv_ok(OUTPUTS["branches"]), "branch copy ledger parses", OUTPUTS["branches"]),
        ("VAL3098_24_branch_copies_exist", all(boolish(row["target_exists"]) for row in rows(OUTPUTS["branches"])), "all branch copies exist", OUTPUTS["branches"]),
        ("VAL3098_25_no_formalization_edit", len(formalization_3098) == 0, "no 3098 files created under formalization-workbench", FORMALIZATION),
        ("VAL3098_26_pycache_removed", not PYCACHE.exists(), "scripts __pycache__ absent after run", PYCACHE),
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
        "ppn_bound": ppn_bound_rows(),
        "derivation": derivation_rows(),
        "assumption_gate": assumption_gate_rows(),
        "conditional_bound": conditional_bound_rows(),
        "failure_audit": failure_rows(),
        "branch_status": branch_status_rows(),
        "claim_gate": claim_gate_rows(),
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
    print(f"3098 PPN common-frame c_g translation checkpoint written: {passed}/{len(data['validation'])} validation checks passed")
    print(DOC)
    print(OUTPUTS["validation"])


if __name__ == "__main__":
    main()
