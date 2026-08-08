from __future__ import annotations

import csv
import math
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
MICROSCOPE_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
QUARANTINE = MICROSCOPE / "quarantine" / "1852"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC_PATH = ROOT / "1852-Y5-R2FR-PPN-common-frame-cg-translation-gate.md"

GAMMA_MINUS_ONE_CENTRAL = 2.1e-5
GAMMA_MINUS_ONE_SIGMA = 2.3e-5
GAMMA_BOUND_2SIGMA = abs(GAMMA_MINUS_ONE_CENTRAL) + 2.0 * GAMMA_MINUS_ONE_SIGMA
ALPHA0_SQUARED_BOUND = GAMMA_BOUND_2SIGMA / (2.0 - GAMMA_BOUND_2SIGMA)
ALPHA0_ABS_BOUND = math.sqrt(ALPHA0_SQUARED_BOUND)


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_SOURCE_REGISTER.csv",
    "ppn_observable": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_PPN_OBSERVABLE_BOUND.csv",
    "derivation": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_COMMON_FRAME_DERIVATION.csv",
    "assumption_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_SCALAR_TENSOR_ASSUMPTION_GATE.csv",
    "cg_bound": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_CG_CONDITIONAL_BOUND_ROW.csv",
    "failure_modes": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_PPN_FAILURE_MODE_AUDIT.csv",
    "local_branch": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_LOCAL_BRANCH_STATUS.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_CLAIM_GATE.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1852_NEXT_TARGET.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1852_VALIDATION.csv",
}


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def source_path(relative_path: str) -> str:
    return rel(ROOT / relative_path)


def ensure_dirs() -> None:
    for path in [RESIDUALS, MICROSCOPE_RESIDUALS, QUARANTINE, RAB_QUEUE]:
        path.mkdir(parents=True, exist_ok=True)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def build_rows_map() -> dict[str, list[dict[str, Any]]]:
    source_rows = [
        {
            "source_id": "SRC1852_0_1851_handoff",
            "source_type": "local_checkpoint",
            "source_path": source_path("1851-Y5-R2FR-first-real-local-coupling-bound-source-table.md"),
            "source_url": "",
            "needle": "NEXT1851_0_primary",
            "use": "selected PPN/common-frame c_g translation target",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1852_1_1851_observable_table",
            "source_type": "local_csv",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1851_OBSERVABLE_BOUND_SOURCE_TABLE.csv"),
            "source_url": "",
            "needle": "OBS1851_2_PPN_CASSINI_2003",
            "use": "Cassini PPN observable bound row",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1852_2_1851_translation_gate",
            "source_type": "local_csv",
            "source_path": source_path("source-intake/mts_residuals/P8_Y5_PARENT_QLOC_1851_MTS_TRANSLATION_GATES.csv"),
            "source_url": "",
            "needle": "TRG1851_0_cg_to_PPN",
            "use": "missing c_g to PPN translation handoff",
            "status": "FOUND",
            "valid_for_claim": False,
        },
        {
            "source_id": "SRC1852_3_cassini_2003",
            "source_type": "primary_paper",
            "source_path": "",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "needle": "gamma = 1 + (2.1 +/- 2.3) x 10^-5",
            "use": "PPN gamma-minus-one source for conservative bound",
            "status": "WEB_SOURCE_RECORDED",
            "valid_for_claim": False,
        },
    ]

    ppn_observable_rows = [
        {
            "row_id": "PPN1852_0_cassini_gamma",
            "observable": "gamma_minus_1",
            "central_value": GAMMA_MINUS_ONE_CENTRAL,
            "one_sigma": GAMMA_MINUS_ONE_SIGMA,
            "conservative_bound_value": GAMMA_BOUND_2SIGMA,
            "bound_rule": "|central| + 2*sigma",
            "units": "dimensionless",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "source_backed_observable": True,
            "valid_for_claim": False,
        },
        {
            "row_id": "PPN1852_1_scalar_tensor_alpha0_proxy",
            "observable": "alpha0_abs_proxy",
            "central_value": "",
            "one_sigma": "",
            "conservative_bound_value": ALPHA0_ABS_BOUND,
            "bound_rule": "from |gamma-1|=2 alpha0^2/(1+alpha0^2), alpha0^2 <= delta_gamma/(2-delta_gamma)",
            "units": "dimensionless",
            "source_url": "https://pubmed.ncbi.nlm.nih.gov/14508481/",
            "source_backed_observable": True,
            "valid_for_claim": False,
        },
    ]

    derivation_rows = [
        {
            "step_id": "DER1852_0_common_frame_ansatz",
            "statement": "Assume ordinary matter sees a universal conformal frame g_matter=A_g(Xhat)^2 g_E.",
            "equation": "A_g(Xhat)=exp(c_g Xhat + O(Xhat^2))",
            "status": "CONDITIONAL_ANSATZ",
            "missing_for_MTS": "parent action has not signed universal common frame as the only local matter coupling",
            "valid_for_claim": False,
        },
        {
            "step_id": "DER1852_1_canonical_scalar",
            "statement": "Introduce canonical scalar varphi with alpha_PPN=d ln A_g/d(varphi/M_Pl).",
            "equation": "alpha_PPN = N_X c_g, where N_X=dXhat/d(varphi/M_Pl)",
            "status": "NORMALIZATION_GATE",
            "missing_for_MTS": "N_X from Z_X and parent Hessian/range is not owned",
            "valid_for_claim": False,
        },
        {
            "step_id": "DER1852_2_ppn_gamma_law",
            "statement": "For an unscreened massless single scalar-tensor limit, gamma-1=-2 alpha_PPN^2/(1+alpha_PPN^2).",
            "equation": "|alpha_PPN| <= sqrt(delta_gamma/(2-delta_gamma))",
            "status": "STANDARD_CONDITIONAL_RELATION",
            "missing_for_MTS": "MTS has not proven it reduces to this scalar-tensor PPN limit",
            "valid_for_claim": False,
        },
        {
            "step_id": "DER1852_3_cassini_proxy_bound",
            "statement": "Using the conservative Cassini envelope gives a scalar-tensor proxy bound.",
            "equation": f"delta_gamma={GAMMA_BOUND_2SIGMA:.8g}; |alpha_PPN|<={ALPHA0_ABS_BOUND:.8g}",
            "status": "NUMERIC_PROXY_DERIVED",
            "missing_for_MTS": "proxy is not a direct c_g bound until N_X, range and contamination gates pass",
            "valid_for_claim": False,
        },
        {
            "step_id": "DER1852_4_cg_translation",
            "statement": "If N_X and tau_PPN are signed, c_g inherits the proxy through |N_X tau_PPN c_g| <= alpha0_abs_bound.",
            "equation": f"|c_g| <= {ALPHA0_ABS_BOUND:.8g}/|N_X tau_PPN|",
            "status": "CONDITIONAL_BOUND_FORMULA_READY",
            "missing_for_MTS": "N_X and tau_PPN are MISSING, so c_g remains unbounded as an MTS component",
            "valid_for_claim": False,
        },
    ]

    assumption_rows = [
        {
            "assumption_id": "AST1852_0_universal_conformal",
            "assumption": "all ordinary matter sees one universal conformal frame A_g(Xhat)^2 g_E",
            "needed_for": "map c_g to PPN gamma",
            "current_status": "NOT_PARENT_SIGNED",
            "failure_if_missing": "species/frame/readout terms move PPN and WEP independently",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "assumption_id": "AST1852_1_canonical_normalization",
            "assumption": "Xhat normalization is tied to the canonical scalar varphi/M_Pl",
            "needed_for": "turn alpha_PPN proxy into c_g bound",
            "current_status": "MISSING_NX_FROM_ZX_HESSIAN",
            "failure_if_missing": "c_g can be rescaled by field normalization",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "assumption_id": "AST1852_2_solar_system_range",
            "assumption": "the X mode is effectively long-range across the Cassini solar-system impact scale",
            "needed_for": "use Cassini gamma without Yukawa/range suppression",
            "current_status": "MISSING_MX2_OR_LAMBDA_SOLAR_SYSTEM_GATE",
            "failure_if_missing": "finite range or screening suppresses Cassini and sends c_g to R10/orbital gates",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "assumption_id": "AST1852_3_no_screening",
            "assumption": "no local screening, environmental plateau or nonlinear suppression changes the scalar charge",
            "needed_for": "apply weak-field scalar-tensor gamma law",
            "current_status": "NOT_DERIVED",
            "failure_if_missing": "Cassini bound constrains screened effective coupling, not parent c_g",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "assumption_id": "AST1852_4_no_disformal_nonhilbert_contamination",
            "assumption": "b_dis, q_nonH, support and boundary terms do not contribute at the same PPN order",
            "needed_for": "isolate c_g as the gamma source",
            "current_status": "MISSING_CONTAMINATION_ZERO_OR_BOUND",
            "failure_if_missing": "PPN residual vector is multi-component, not a one-parameter c_g bound",
            "gate_pass": False,
            "valid_for_claim": False,
        },
        {
            "assumption_id": "AST1852_5_verdict",
            "assumption": "all scalar-tensor translation assumptions pass simultaneously",
            "needed_for": "promote alpha0 proxy to c_g component bound",
            "current_status": "FAIL_CURRENT_CLAIM",
            "failure_if_missing": "keep PPN result as source-backed conditional proxy only",
            "gate_pass": False,
            "valid_for_claim": False,
        },
    ]

    cg_bound_rows = [
        {
            "bound_id": "CGB1852_0_alpha_proxy",
            "quantity": "alpha_PPN_proxy",
            "formula": "sqrt(delta_gamma/(2-delta_gamma))",
            "numeric_bound": ALPHA0_ABS_BOUND,
            "units": "dimensionless",
            "source": "Cassini gamma_minus_1 conservative 2sigma envelope",
            "status": "SOURCE_BACKED_PROXY",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "CGB1852_1_cg_conditional",
            "quantity": "c_g",
            "formula": "abs(c_g) <= alpha_PPN_proxy / abs(N_X tau_PPN)",
            "numeric_bound": "MISSING_NX_TAU_PPN",
            "units": "dimensionless_per_normalized_Xhat",
            "source": "DER1852_4_cg_translation",
            "status": "CONDITIONAL_FORMULA_READY_COMPONENT_BOUND_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "CGB1852_2_long_range_branch",
            "quantity": "c_g_long_range",
            "formula": "if lambda_X >> solar impact scale and N_X=tau_PPN=1, abs(c_g)<=alpha_PPN_proxy",
            "numeric_bound": ALPHA0_ABS_BOUND,
            "units": "dimensionless",
            "source": "conditional scalar-tensor limit only",
            "status": "ILLUSTRATIVE_NOT_MTS_CLAIM",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "CGB1852_3_finite_range_branch",
            "quantity": "c_g_finite_range",
            "formula": "Cassini response multiplied by range/screening transfer S_PPN(lambda_X, environment)",
            "numeric_bound": "MISSING_RANGE_TRANSFER",
            "units": "dimensionless",
            "source": "range gate required",
            "status": "BLOCKED_BY_RANGE_SCREENING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    failure_rows = [
        {
            "failure_id": "PFM1852_0_rescaling",
            "failure_mode": "field normalization rescaling",
            "why_it_matters": "c_g is derivative with respect to Xhat; PPN sees canonical alpha_PPN",
            "required_fix": "derive N_X from Z_X/Hessian parent action",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "failure_id": "PFM1852_1_range",
            "failure_mode": "finite range or heavy local mode",
            "why_it_matters": "Cassini constrains long-range solar-system fields; short-range modes need R10/lab bounds",
            "required_fix": "derive M_X^2/lambda_X and solar-system transfer function",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "failure_id": "PFM1852_2_screening",
            "failure_mode": "environmental screening or plateau suppression",
            "why_it_matters": "Cassini would bound screened effective coupling, not parent coupling",
            "required_fix": "derive local screening map without smuggling plateau axiom",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "failure_id": "PFM1852_3_multi_component_ppn",
            "failure_mode": "b_dis/q_nonH/support/boundary terms contribute to gamma",
            "why_it_matters": "a single c_g bound would be fake if other residuals share the PPN channel",
            "required_fix": "derive PPN residual vector and absolute no-cancellation envelope",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "failure_id": "PFM1852_4_matter_frame_nonuniversality",
            "failure_mode": "source/test matter frames are not universal",
            "why_it_matters": "PPN and WEP constraints split into species-dependent charges",
            "required_fix": "parent matter functor/no-marker theorem or material sensitivity map",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
    ]

    local_branch_rows = [
        {
            "branch_id": "LBS1852_0_if_all_gates_pass",
            "branch": "long-range scalar-tensor common-frame MTS",
            "result": f"|N_X tau_PPN c_g| <= {ALPHA0_ABS_BOUND:.8g}",
            "status": "CONDITIONAL_COMPETITIVE_GATE",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "LBS1852_1_current_MTS",
            "branch": "current parent/local branch",
            "result": "Cassini source bound exists, but c_g is not directly bounded",
            "status": "FAIL_CURRENT_CLAIM_TRANSLATION_MISSING",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "branch_id": "LBS1852_2_best_next",
            "branch": "normalization/range repair",
            "result": "derive N_X and lambda_X transfer before claiming PPN/local GR",
            "status": "NEXT_TARGET",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    claim_gate_rows = [
        {
            "gate_id": "CG1852_0_cassini_source",
            "claim": "Cassini PPN source bound is recorded",
            "gate_pass": True,
            "reason": "gamma_minus_one conservative bound and alpha0 proxy are computed",
            "claim_allowed": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1852_1_alpha_proxy",
            "claim": "scalar-tensor alpha0 proxy is computed",
            "gate_pass": True,
            "reason": "standard conditional formula yields numeric proxy",
            "claim_allowed": True,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1852_2_cg_component_bound",
            "claim": "MTS c_g is bounded by Cassini",
            "gate_pass": False,
            "reason": "N_X, tau_PPN, range/screening and contamination gates fail current claim",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG1852_3_local_GR",
            "claim": "local GR branch passes PPN",
            "gate_pass": False,
            "reason": "PPN residual vector and component bounds are not derived",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]

    decision_rows = [
        {
            "decision_id": "DEC1852_0_derivation_status",
            "decision": "The Cassini-to-alpha0 derivation is exact for the scalar-tensor proxy.",
            "because": "gamma law can be inverted cleanly and gives a numeric common-frame proxy.",
            "next_action": "keep it as a benchmark bound, not a direct MTS claim",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1852_1_current_block",
            "decision": "The direct c_g claim remains blocked.",
            "because": "field normalization, range/screening and residual-vector isolation are unsigned.",
            "next_action": "derive N_X/lambda_X transfer from the parent Hessian and local range branch",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1852_2_best_next",
            "decision": "Next target should be canonical X normalization and range gate.",
            "because": "without N_X and lambda_X, every c_g bound can be rescaled or range-suppressed.",
            "next_action": "1853-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg.md",
            "valid_for_claim": False,
        },
    ]

    next_target_rows = [
        {
            "route_id": "NEXT1852_0_primary",
            "next_target": "1853-Y5-R2FR-canonical-X-normalization-and-range-gate-for-cg.md",
            "script": "scripts/Y5_R2FR_canonical_X_normalization_and_range_gate_for_cg_1853.py",
            "objective": "derive N_X from Z_X/Hessian ownership and decide whether lambda_X is solar-system long-range, R10 short-range, screened, or still missing",
            "selection_status": "selected",
            "success_condition": "PPN c_g bound becomes normalized/range-qualified, or c_g remains source-only with explicit N_X/lambda_X blockers",
        },
        {
            "route_id": "NEXT1852_1_parallel",
            "next_target": "1853b-Y5-R2FR-PPN-residual-vector-no-cancellation-envelope.md",
            "script": "scripts/Y5_R2FR_PPN_residual_vector_no_cancellation_envelope_1853b.py",
            "objective": "derive the PPN residual vector over c_g, b_dis, q_nonH, support and boundary components",
            "selection_status": "held",
            "success_condition": "PPN no-cancellation vector is explicit enough for multi-component bounds",
        },
    ]

    return {
        "source_register": source_rows,
        "ppn_observable": ppn_observable_rows,
        "derivation": derivation_rows,
        "assumption_gate": assumption_rows,
        "cg_bound": cg_bound_rows,
        "failure_modes": failure_rows,
        "local_branch": local_branch_rows,
        "claim_gate": claim_gate_rows,
        "decision": decision_rows,
        "next_target": next_target_rows,
    }


def copy_outputs(include_validation: bool = False) -> None:
    keys = list(OUTPUTS)
    if not include_validation:
        keys = [key for key in keys if key != "validation"]
    for key in keys:
        src = OUTPUTS[key]
        if not src.exists():
            continue
        for dst_dir in [MICROSCOPE_RESIDUALS, QUARANTINE]:
            shutil.copy2(src, dst_dir / src.name)
        shutil.copy2(src, RAB_QUEUE / f"JR1852_{src.name}")


def check_sources(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        if str(row["source_type"]).startswith("local"):
            path = ROOT / str(row["source_path"])
            if not path.exists():
                missing.append(str(row["source_path"]))
        elif not str(row["source_url"]).startswith("http"):
            missing.append(str(row["source_id"]))
    return not missing, "missing: " + "; ".join(missing) if missing else "all local paths exist and web source URLs are recorded"


def check_needles(source_rows: list[dict[str, Any]]) -> tuple[bool, str]:
    missing: list[str] = []
    for row in source_rows:
        if not str(row["source_type"]).startswith("local"):
            continue
        path = ROOT / str(row["source_path"])
        needle = str(row["needle"])
        if path.exists() and needle not in path.read_text(encoding="utf-8", errors="ignore"):
            missing.append(f"{row['source_path']}::{needle}")
    return not missing, "missing: " + "; ".join(missing) if missing else "all local source needles are present"


def check_csv_parse() -> tuple[bool, str]:
    malformed: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        try:
            read_csv(path)
        except Exception as exc:  # pragma: no cover
            malformed.append(f"{path.name}: {exc}")
    return not malformed, "malformed: " + "; ".join(malformed) if malformed else "all generated 1852 CSVs parse"


def check_branch_copies() -> tuple[bool, str]:
    missing: list[str] = []
    for key, path in OUTPUTS.items():
        if key == "validation":
            continue
        expected = [
            MICROSCOPE_RESIDUALS / path.name,
            QUARANTINE / path.name,
            RAB_QUEUE / f"JR1852_{path.name}",
        ]
        for item in expected:
            if not item.exists():
                missing.append(str(item))
    return not missing, "missing copies: " + "; ".join(missing) if missing else "branch/quarantine/queue copies exist"


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    ok, detail = check_sources(rows_map["source_register"])
    checks.append(("VAL1852_0_sources_recorded", ok, detail))
    ok, detail = check_needles(rows_map["source_register"])
    checks.append(("VAL1852_1_local_needles_present", ok, detail))
    checks.append(
        (
            "VAL1852_2_gamma_bound_numeric",
            any(
                row["row_id"] == "PPN1852_0_cassini_gamma"
                and abs(float(row["conservative_bound_value"]) - GAMMA_BOUND_2SIGMA) < 1e-15
                for row in rows_map["ppn_observable"]
            ),
            "Cassini gamma bound is numeric",
        )
    )
    checks.append(
        (
            "VAL1852_3_alpha_proxy_numeric",
            any(
                row["row_id"] == "PPN1852_1_scalar_tensor_alpha0_proxy"
                and 0.0 < float(row["conservative_bound_value"]) < 0.01
                for row in rows_map["ppn_observable"]
            ),
            "scalar-tensor alpha0 proxy is numeric and small",
        )
    )
    checks.append(
        (
            "VAL1852_4_derivation_conditional",
            any(row["step_id"] == "DER1852_4_cg_translation" and row["status"] == "CONDITIONAL_BOUND_FORMULA_READY" for row in rows_map["derivation"]),
            "c_g conditional bound formula is present",
        )
    )
    checks.append(
        (
            "VAL1852_5_assumption_gate_blocks",
            any(row["assumption_id"] == "AST1852_5_verdict" and row["current_status"] == "FAIL_CURRENT_CLAIM" for row in rows_map["assumption_gate"])
            and all(not boolish(row["gate_pass"]) for row in rows_map["assumption_gate"]),
            "scalar-tensor assumptions block current MTS c_g claim",
        )
    )
    checks.append(
        (
            "VAL1852_6_cg_bound_nonclaim",
            any(row["bound_id"] == "CGB1852_1_cg_conditional" and row["numeric_bound"] == "MISSING_NX_TAU_PPN" for row in rows_map["cg_bound"])
            and all(not boolish(row["claim_allowed"]) for row in rows_map["cg_bound"]),
            "c_g component bound remains nonclaim",
        )
    )
    checks.append(
        (
            "VAL1852_7_failure_modes_block",
            all(boolish(row["blocks_claim"]) and not boolish(row["valid_for_claim"]) for row in rows_map["failure_modes"]),
            "all listed PPN failure modes block direct claim",
        )
    )
    checks.append(
        (
            "VAL1852_8_local_branch_status",
            any(row["branch_id"] == "LBS1852_1_current_MTS" and row["status"] == "FAIL_CURRENT_CLAIM_TRANSLATION_MISSING" for row in rows_map["local_branch"]),
            "current local branch remains blocked",
        )
    )
    checks.append(
        (
            "VAL1852_9_claim_gates_safe",
            any(row["gate_id"] == "CG1852_0_cassini_source" and boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and any(row["gate_id"] == "CG1852_2_cg_component_bound" and not boolish(row["gate_pass"]) for row in rows_map["claim_gate"])
            and all(not boolish(row["valid_for_claim"]) for row in rows_map["claim_gate"]),
            "source/proxy gates pass but MTS component/local claims do not",
        )
    )
    checks.append(
        (
            "VAL1852_10_next_target_selected",
            any(row["route_id"] == "NEXT1852_0_primary" and row["selection_status"] == "selected" for row in rows_map["next_target"]),
            "next target selected",
        )
    )
    checks.append(
        (
            "VAL1852_11_no_claim_flags",
            all(not boolish(row.get("valid_for_claim", False)) for rows in rows_map.values() for row in rows),
            "no valid_for_claim flags are true",
        )
    )
    checks.append(
        (
            "VAL1852_12_missing_rows_nonclaim",
            all(
                not boolish(row.get("valid_for_claim", False))
                for rows in rows_map.values()
                for row in rows
                if "MISSING_" in " ".join(str(value) for value in row.values())
            ),
            "MISSING_* rows stay nonclaim",
        )
    )
    ok, detail = check_csv_parse()
    checks.append(("VAL1852_13_csv_parse", ok, detail))
    ok, detail = check_branch_copies()
    checks.append(("VAL1852_14_branch_copies", ok, detail))
    pycache_path = ROOT / "scripts" / "__pycache__"
    checks.append(("VAL1852_15_pycache_absent", not pycache_path.exists(), "scripts __pycache__ absent"))
    formalization_outputs = list(FORMALIZATION.rglob("*1852*")) if FORMALIZATION.exists() else []
    checks.append(
        (
            "VAL1852_16_formalization_untouched",
            not formalization_outputs,
            "no 1852 outputs found under formalization-workbench",
        )
    )
    overall = all(result for _, result, _ in checks)
    validation_rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    validation_rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1852_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1852 PPN common-frame c_g translation gate",
        }
    )
    return validation_rows


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    header = "| " + " | ".join(fields) + " |"
    sep = "| " + " | ".join("---" for _ in fields) + " |"
    lines = [header, sep]
    for row in rows:
        values = [str(row.get(field, "")).replace("\n", " ") for field in fields]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    return "\n".join(
        [
            "# 1852: PPN Common-Frame c_g Translation Gate",
            "",
            f"**Current verdict:** Cassini gives a real source-backed PPN anchor and a clean scalar-tensor proxy `|alpha_PPN| <= {ALPHA0_ABS_BOUND:.6g}` from the conservative `|gamma-1| <= {GAMMA_BOUND_2SIGMA:.6g}` envelope. But this is not yet a direct MTS `c_g` bound: the parent branch still lacks `N_X`, `tau_PPN`, solar-system range/screening, and proof that disformal/non-Hilbert/support terms are silent.",
            "",
            "## Source Register",
            markdown_table(rows_map["source_register"], ["source_id", "source_type", "source_path", "source_url", "needle", "use", "status", "valid_for_claim"]),
            "",
            "## PPN Observable Bound",
            markdown_table(rows_map["ppn_observable"], ["row_id", "observable", "central_value", "one_sigma", "conservative_bound_value", "bound_rule", "units", "source_url", "source_backed_observable", "valid_for_claim"]),
            "",
            "## Common-Frame Derivation",
            markdown_table(rows_map["derivation"], ["step_id", "statement", "equation", "status", "missing_for_MTS", "valid_for_claim"]),
            "",
            "## Scalar-Tensor Assumption Gate",
            markdown_table(rows_map["assumption_gate"], ["assumption_id", "assumption", "needed_for", "current_status", "failure_if_missing", "gate_pass", "valid_for_claim"]),
            "",
            "## c_g Conditional Bound Row",
            markdown_table(rows_map["cg_bound"], ["bound_id", "quantity", "formula", "numeric_bound", "units", "source", "status", "claim_allowed", "valid_for_claim"]),
            "",
            "## PPN Failure Mode Audit",
            markdown_table(rows_map["failure_modes"], ["failure_id", "failure_mode", "why_it_matters", "required_fix", "blocks_claim", "valid_for_claim"]),
            "",
            "## Local Branch Status",
            markdown_table(rows_map["local_branch"], ["branch_id", "branch", "result", "status", "claim_allowed", "valid_for_claim"]),
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
            "This is a useful tightening. If MTS really has a long-range, unscreened, universal common scalar frame, Cassini is a harsh judge. If it is finite-range, screened, or not canonically normalized the same way, Cassini is still useful but it cannot be used honestly until the transfer map is derived.",
            "",
        ]
    )


def main() -> None:
    ensure_dirs()
    rows_map = build_rows_map()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs(include_validation=False)
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    DOC_PATH.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    copy_outputs(include_validation=True)
    print(f"wrote {DOC_PATH}")
    print(f"wrote {OUTPUTS['validation']}")
    print(f"1852 validation {validation_rows[-1]['result']}")


if __name__ == "__main__":
    main()
