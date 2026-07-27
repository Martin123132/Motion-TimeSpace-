from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
BRANCH_RESIDUALS = MICROSCOPE / "branch_locked_wep" / "residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
DOC = ROOT / "1530-Y5-lambda-phi-bound-input-source-pass.md"
START_TS = datetime.now(timezone.utc).timestamp()

SOURCE_FILES = {
    "1529_doc": ROOT / "1529-Y5-parent-boundary-no-flux-zero-mode-certificate-or-lambda-phi-bound-inputs.md",
    "1529_validation": OUT / "P8_Y5_BRR545_1529_VALIDATION.csv",
    "1529_inputs": OUT / "P8_Y5_PARENT_QLOC_1529_LAMBDA_PHI_BOUND_INPUT_LEDGER.csv",
    "1529_certificate": OUT / "P8_Y5_PARENT_QLOC_1529_BOUNDARY_CERTIFICATE_AUDIT.csv",
    "1529_runner": OUT / "P8_Y5_PARENT_QLOC_1529_CERTIFICATE_OR_BOUND_RUNNER.csv",
    "1529_claim_gate": OUT / "P8_Y5_PARENT_QLOC_1529_CLAIM_GATE.csv",
    "1529_next": OUT / "P8_Y5_PARENT_QLOC_1529_NEXT_TARGET.csv",
    "1528_stress": OUT / "P8_Y5_PARENT_QLOC_1528_MULTIPLIER_STRESS_BOUND_SCHEMA.csv",
    "1528_theorem": OUT / "P8_Y5_PARENT_QLOC_1528_LAMBDA_PHI_ENERGY_THEOREM.csv",
    "1527_aux": OUT / "P8_Y5_PARENT_QLOC_1527_LOCAL_AUXILIARY_ACTION_CONTRACT.csv",
    "1524_green": OUT / "P8_Y5_PARENT_QLOC_1524_GREEN_NORMALIZATION_CONTRACT.csv",
    "1524_profile": OUT / "P8_Y5_PARENT_QLOC_1524_KHAT_DELTAK_SCALAR_PROFILE.csv",
    "1523_pigamma": OUT / "P8_Y5_PARENT_QLOC_1523_PIGAMMA_PROJECTOR_LEDGER.csv",
    "1523_units": OUT / "P8_Y5_PARENT_QLOC_1523_UNITS_LEDGER.csv",
    "1289_variation": OUT / "P8_Y5_R10_1289_KMETRIC_VARIATION_EXPANSION_NONCLAIM.csv",
    "1289_derivative": OUT / "P8_Y5_R10_1289_FIRST_DERIVATIVE_TERM_ROW_NONCLAIM.csv",
    "1367_kernel": OUT / "P8_Y5_R10_1367_KMETRIC_CHAIN_KERNEL_ATTEMPT.csv",
    "776_kgamma": OUT / "P8_Y5_R10_776_KGAMMA_METRIC_RESPONSE_LEDGER.csv",
    "798_gamma": OUT / "P8_Y5_R10_798_GAMMA_SOURCE_EXPANSION.csv",
    "gk_contract": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
}

SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_1530_SOURCE_REGISTER.csv"
INPUT_AUDIT = OUT / "P8_Y5_PARENT_QLOC_1530_BOUND_INPUT_SOURCE_AUDIT.csv"
ANALYTIC_CONTRACT = OUT / "P8_Y5_PARENT_QLOC_1530_ANALYTIC_BOUND_CONTRACT.csv"
DELTAG_REDUCTION = OUT / "P8_Y5_PARENT_QLOC_1530_DELTA_G_SGAMMA_REDUCTION.csv"
OBS_PROJECTION = OUT / "P8_Y5_PARENT_QLOC_1530_OBSERVABLE_PROJECTION_CONTRACT.csv"
RUNNER = OUT / "P8_Y5_PARENT_QLOC_1530_BOUND_INPUT_RUNNER.csv"
REJECTION_LEDGER = OUT / "P8_Y5_PARENT_QLOC_1530_REJECTION_LEDGER.csv"
CLAIM_GATE = OUT / "P8_Y5_PARENT_QLOC_1530_CLAIM_GATE.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_1530_DECISION.csv"
LOCAL_STATUS = OUT / "P8_Y5_PARENT_QLOC_1530_LOCAL_GR_NEWTON_STATUS.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_1530_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1530_VALIDATION.csv"

QUARANTINE = MICROSCOPE / "quarantine" / "1530"
QUAR_INPUTS = QUARANTINE / "BOUND_INPUT_SOURCE_AUDIT_NONCLAIM.csv"
QUAR_ANALYTIC = QUARANTINE / "ANALYTIC_BOUND_CONTRACT_NONCLAIM.csv"
QUAR_DELTAG = QUARANTINE / "DELTA_G_SGAMMA_REDUCTION_NONCLAIM.csv"
QUAR_DECISION = QUARANTINE / "DECISION_NONCLAIM.csv"
BRANCH_INPUTS = BRANCH_RESIDUALS / "lambda_phi_bound_input_source_audit_nonclaim_1530.csv"
BRANCH_ANALYTIC = BRANCH_RESIDUALS / "lambda_phi_analytic_bound_contract_nonclaim_1530.csv"
BRANCH_DELTAG = BRANCH_RESIDUALS / "delta_g_sgamma_reduction_nonclaim_1530.csv"
BRANCH_DECISION = BRANCH_RESIDUALS / "lambda_phi_bound_input_decision_nonclaim_1530.csv"


def flags() -> dict[str, bool]:
    return {
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
    }


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT)).replace("\\", "/")
    except ValueError:
        return str(path)


def source_list(*keys: str) -> str:
    return "; ".join(rel(SOURCE_FILES[key]) for key in keys)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def parse_csv(path: Path) -> bool:
    read_csv(path)
    return True


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    claim_keys = [
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "accepted_for_scoring",
        "passes_for_claim",
    ]
    for path in paths:
        for row in read_csv(path):
            for key in claim_keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "source_id": f"SRC1530_{index}_{key}",
            "source_path": rel(path),
            "exists": path.exists(),
            "purpose": "input evidence for lambda_phi multiplier-stress bound input source pass",
            **flags(),
        }
        for index, (key, path) in enumerate(SOURCE_FILES.items())
    ]


def input_audit_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "BIA1530_0_C_P",
            "C_P",
            "Poincare/zero-mode constant",
            "ANALYTIC_FORM_ONLY",
            "C_P can be expressed once domain diameter/spectral gap and zero-mode condition are parent-owned",
            "missing domain geometry, spectral gap, boundary class",
            source_list("1529_inputs", "1528_theorem"),
        ),
        (
            "BIA1530_1_C_E",
            "C_E",
            "elliptic gradient estimate constant",
            "ANALYTIC_FORM_ONLY",
            "C_E is an elliptic regularity constant for the chosen collar/domain/operator",
            "missing elliptic branch, regularity class, domain metric bounds",
            source_list("1529_inputs", "1528_theorem"),
        ),
        (
            "BIA1530_2_C_T",
            "C_T",
            "stress conversion constant",
            "ALGEBRAIC_FORM_ONLY",
            "T_lambda bound reduces to quadratic gradient term plus lambda_phi times delta_g S_Gamma",
            "missing metric norm convention and stress projection norm",
            source_list("1528_stress", "1527_aux"),
        ),
        (
            "BIA1530_3_R_norm",
            "||R||",
            "Ricci scalar norm on local collar",
            "MISSING_SOURCE_NORM",
            "R=0 would close only if same parent local vacuum branch is signed; otherwise need finite same-frame norm",
            "missing local-vacuum branch certificate or source-backed curvature norm",
            source_list("1528_theorem", "1529_certificate"),
        ),
        (
            "BIA1530_4_boundary_source_norm",
            "boundary_source_norm",
            "boundary/no-flux violation norm",
            "MISSING_BOUNDARY_NORM",
            "no parent boundary certificate found in 1529; finite violation norm is fallback",
            "missing boundary source model or no-flux theorem",
            source_list("1529_certificate", "1529_inputs"),
        ),
        (
            "BIA1530_5_initial_data_norm",
            "initial_data_norm",
            "hyperbolic branch initial data norm",
            "MISSING_OR_BRANCH_CAN_BE_EXCLUDED",
            "if static elliptic branch is signed, this term drops; otherwise it must be sourced",
            "missing static-branch certificate or initial data norm",
            source_list("1528_theorem", "1529_certificate"),
        ),
        (
            "BIA1530_6_delta_g_SGamma_norm",
            "||delta_g S_Gamma||",
            "metric-response norm of S_Gamma=(2/3)(Gamma_eff+C)",
            "REDUCED_TO_KMETRIC_KERNEL_NORMS",
            "delta_g S_Gamma = (2/3) delta_g Gamma_eff if C is metric-silent; Gamma_eff metric response is exactly the Kmetric kernel problem",
            "missing M_m, M_L, K_conn, K_domain, K_boundary, sign/volume convention",
            source_list("1289_variation", "1289_derivative", "1367_kernel", "776_kgamma", "798_gamma"),
        ),
        (
            "BIA1530_7_observable_projection",
            "Pi_gamma/P_loc/C_op projection",
            "projection of multiplier stress into S_total, Q_loc, and q_loc_hat",
            "SCHEMA_EXISTS_VALUES_MISSING",
            "1523/1524 supply the scalar projection/Green schema, but Pi_gamma, C_op, and Q_loc normalization are not live",
            "missing live projector, C_op, source integral, GM normalization",
            source_list("1523_pigamma", "1524_green", "1523_units"),
        ),
        (
            "BIA1530_8_no_cancellation",
            "absolute envelope",
            "abs-sum guard",
            "GUARD_RETAINED",
            "multiplier terms must be added in absolute value with no cancellation against K_L/Gamma terms",
            "none for guard; values still missing",
            source_list("1529_inputs", "1528_stress"),
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": audit_id,
            "quantity": quantity,
            "target": target,
            "status": status,
            "finding": finding,
            "missing_to_promote": missing,
            "source_paths": sources,
            **flags(),
        }
        for audit_id, quantity, target, status, finding, missing, sources in rows
    ]


def analytic_contract_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "ABC1530_0_Poincare_form",
            "C_P",
            "for a parent-owned connected compact domain with Dirichlet or zero-mean Neumann data, ||lambda_phi|| <= C_P ||grad lambda_phi||",
            "CONDITIONAL_ANALYTIC_FORM",
            "requires domain, boundary class, and zero-mode owner",
        ),
        (
            "ABC1530_1_gradient_form",
            "C_E",
            "||grad lambda_phi|| <= C_E(|c_I| ||R|| + boundary_source_norm + initial_data_norm)",
            "CONDITIONAL_ANALYTIC_FORM",
            "requires elliptic operator, regularity class, and domain constants",
        ),
        (
            "ABC1530_2_stress_form",
            "C_T",
            "||T_lambda_phi|| <= C_T(||grad lambda_phi||^2 + ||lambda_phi|| ||delta_g S_Gamma||)",
            "CONDITIONAL_ALGEBRAIC_FORM",
            "requires metric/stress norm convention and delta_g S_Gamma norm",
        ),
        (
            "ABC1530_3_abs_envelope",
            "epsilon_lambda_phi",
            "epsilon_lambda_phi <= abs(C_T)*(C_E A)^2 + abs(C_T)*C_P*C_E*A*||delta_g S_Gamma||, with A=|c_I|||R||+boundary_source_norm+initial_data_norm",
            "COMPOSITE_BOUND_FORM_WRITTEN",
            "all constants and norms remain missing or conditional",
        ),
        (
            "ABC1530_4_verdict",
            "analytic contract",
            "bound algebra is now organized, but no numeric/source-backed bound exists",
            "NOT_SCORE_READY",
            "missing values block lambda_phi decision",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "contract_id": contract_id,
            "quantity": quantity,
            "formula_or_contract": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1528_stress", "1529_inputs", "1528_theorem"),
            **flags(),
        }
        for contract_id, quantity, formula, status, missing in rows
    ]


def deltag_reduction_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DGS1530_0_definition",
            "S_Gamma",
            "S_Gamma=(2/3)(Gamma_eff+C)",
            "SOURCE_RELATION_IMPORTED",
            "C metric-silence must be specified",
        ),
        (
            "DGS1530_1_metric_response",
            "delta_g S_Gamma",
            "delta_g S_Gamma=(2/3)delta_g Gamma_eff if delta_g C=0",
            "REDUCTION_WRITTEN",
            "constant/background term metric dependence not signed",
        ),
        (
            "DGS1530_2_Gamma_kernel",
            "delta_g Gamma_eff",
            "Gamma_eff=L_cg^-2 F(m), so delta_g Gamma_eff=L_cg^-2 F'(m)delta_g m - 2L_cg^-3 F(m)delta_g L_cg plus hidden connection/domain/boundary terms",
            "KERNEL_ROUTE_SOURCE_BACKED_SYMBOLIC",
            "M_m, M_L, K_conn, K_domain, K_boundary are still missing",
        ),
        (
            "DGS1530_3_norm_envelope",
            "||delta_g S_Gamma||",
            "||delta_g S_Gamma|| <= (2/3)(L_cg^-2|F'| ||M_m|| + 2L_cg^-3|F| ||M_L|| + ||K_conn|| + ||K_domain|| + ||K_boundary||)",
            "SYMBOLIC_NORM_ENVELOPE",
            "requires live norms/units for every kernel",
        ),
        (
            "DGS1530_4_fixed_point_shortcut",
            "F'(m_*)=0 route",
            "even if F'(m_*)=0, L_cg response and hidden connection/domain/boundary kernels remain unless separately zeroed",
            "SHORTCUT_BLOCKED",
            "do not claim delta_g S_Gamma=0 from fixed point alone",
        ),
        (
            "DGS1530_5_verdict",
            "delta_g S_Gamma source pass",
            "the input is reduced to the same Kmetric kernel norms that block DeltaK; this is the sharpest next source target",
            "NOT_NUMERIC_REDUCED_TO_KERNELS",
            "no scoreable operator norm yet",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "reduction_id": reduction_id,
            "quantity": quantity,
            "formula_or_statement": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1289_variation", "1289_derivative", "1367_kernel", "776_kgamma", "798_gamma"),
            **flags(),
        }
        for reduction_id, quantity, formula, status, missing in rows
    ]


def observable_projection_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "OBS1530_0_multiplier_source",
            "S_lambda",
            "S_total gains S_lambda from T_lambda_phi unless lambda_phi=0",
            "RETAINED_CHANNEL",
            "requires Pi_gamma/P_loc projection of multiplier stress",
        ),
        (
            "OBS1530_1_projected_scalar",
            "Pi_gamma[S_lambda]",
            "S_lambda_scalar := Pi_gamma[P_loc div T_lambda_phi] or equivalent scalar-channel projection",
            "SCHEMA_ONLY",
            "Pi_gamma/P_loc not live",
        ),
        (
            "OBS1530_2_green_charge",
            "Q_lambda",
            "if nabla^2 R_AB=C_op S_total, Q_lambda=(C_op/4*pi) int S_lambda_scalar d^3x",
            "CONDITIONAL_GREEN_FORM",
            "C_op and source integral missing",
        ),
        (
            "OBS1530_3_dimensionless",
            "q_lambda_hat",
            "q_lambda_hat=Q_lambda c^2/(G M_source)",
            "CONDITIONAL_DIMENSIONLESS_FORM",
            "GM/source normalization missing",
        ),
        (
            "OBS1530_4_verdict",
            "observable projection",
            "projection path exists as a schema, but no local observable value can be computed",
            "NOT_SCORE_READY",
            "Pi_gamma, C_op, Q_lambda, GM missing",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "projection_id": projection_id,
            "quantity": quantity,
            "formula_or_statement": formula,
            "status": status,
            "missing_to_promote": missing,
            "source_paths": source_list("1523_pigamma", "1524_green", "1524_profile", "1523_units"),
            **flags(),
        }
        for projection_id, quantity, formula, status, missing in rows
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1530_0_full_multiplier_bound",
            "route": "score epsilon_lambda_phi",
            "required_inputs": "C_P; C_E; C_T; R_norm; boundary_source_norm; initial_data_norm/static exclusion; delta_g_SGamma_norm; observable projection",
            "current_inputs": "analytic formulas only; delta_g_SGamma reduced to missing Kmetric kernels; projection schema only",
            "result": "BLOCKED_INPUT_VALUES_MISSING",
            "next_required_object": "delta_g_SGamma/Kmetric kernel norms or source-backed domain constants",
            "source_paths": source_list("1529_inputs", "1528_stress", "1524_green"),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1530_1_delta_g_SGamma_norm",
            "route": "fill ||delta_g S_Gamma||",
            "required_inputs": "M_m; M_L; K_conn; K_domain; K_boundary; L_cg; F; F_prime; sign/units",
            "current_inputs": "symbolic Kmetric/Gamma kernels only",
            "result": "BLOCKED_KMETRIC_KERNEL_NORMS_MISSING",
            "next_required_object": "Kmetric kernel norm source pass",
            "source_paths": source_list("1289_variation", "1367_kernel", "776_kgamma"),
            **flags(),
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "runner_id": "RUN1530_2_Khat_promotion",
            "route": "promote staged Khat adoption",
            "required_inputs": "lambda_phi zero theorem or accepted finite multiplier bound",
            "current_inputs": "neither zero nor bound accepted",
            "result": "BLOCKED_NO_KHAT_PROMOTION",
            "next_required_object": "lambda_phi decision",
            "source_paths": source_list("1529_claim_gate", "1527_aux"),
            **flags(),
        },
    ]


def rejection_rows() -> list[dict[str, Any]]:
    rows = [
        ("REJ1530_0_formula_as_value", "treat analytic inequality as numeric bound", "REJECTED", "domain constants and norms are not values"),
        ("REJ1530_1_fixed_point_zero", "set delta_g S_Gamma=0 from F'(m_*)=0", "REJECTED", "L_cg and hidden connection/domain/boundary kernels remain"),
        ("REJ1530_2_R_zero_import", "set R_norm=0 from desired local GR", "REJECTED", "would be circular without same parent branch certificate"),
        ("REJ1530_3_projection_as_score", "use Pi_gamma/C_op schema as observable value", "REJECTED", "projection/normalization constants are not live"),
        ("REJ1530_4_cancel_multiplier", "cancel multiplier stress against K_L or Gamma terms", "REJECTED", "absolute envelope/no-cancellation guard retained"),
        ("REJ1530_5_promote_Khat", "promote Khat adoption before lambda_phi bound", "REJECTED", "multiplier stress unresolved"),
        ("REJ1530_6_score_local_GR", "score local GR/PPN now", "REJECTED", "q_loc local branch remains nonclaim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "rejection_id": rejection_id,
            "shortcut": shortcut,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for rejection_id, shortcut, status, reason in rows
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    rows = [
        ("GATE1530_0_input_audit", "bound input source pass completed", "PASS_NONCLAIM", "all requested input slots audited"),
        ("GATE1530_1_analytic_contract", "multiplier bound formula organized", "PASS_NONCLAIM", "composite epsilon_lambda_phi bound written"),
        ("GATE1530_2_delta_g_SGamma", "delta_g S_Gamma norm is source-backed", "BLOCKED", "reduced to missing Kmetric kernel norms"),
        ("GATE1530_3_domain_constants", "domain constants are source-backed", "BLOCKED", "domain/spectral/elliptic data missing"),
        ("GATE1530_4_observable_projection", "lambda_phi stress maps to q_loc observable", "BLOCKED", "Pi_gamma/C_op/GM missing"),
        ("GATE1530_5_lambda_decision", "lambda_phi is zero or bounded", "BLOCKED", "input values missing"),
        ("GATE1530_6_local_GR", "local GR/Newton/PPN recovery is claimable", "BLOCKED_NO_CLAIM", "q_loc branch remains nonclaim"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "status": status,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, status, reason in rows
    ]


def decision_rows() -> list[dict[str, Any]]:
    rows = [
        (
            "DEC1530_0_progress",
            "Keep the multiplier-stress bound algebra.",
            "BOUND_FORM_ORGANIZED",
            "the obstruction is now a finite list of constants/norms rather than a vague local residual.",
        ),
        (
            "DEC1530_1_key_blocker",
            "Treat delta_g S_Gamma as the sharpest next input.",
            "DELTAG_SGAMMA_REDUCED_TO_KMETRIC_KERNELS",
            "this couples the lambda_phi problem back to the same Kmetric kernels blocking DeltaK.",
        ),
        (
            "DEC1530_2_no_claim",
            "Do not promote lambda_phi, Khat, or local GR.",
            "CLAIM_BLOCKED",
            "every score route still depends on missing norms/projections.",
        ),
        (
            "DEC1530_3_next",
            "Next target is Kmetric kernel norm source pass for delta_g S_Gamma.",
            "NEXT_1531_KMETRIC_KERNEL_NORMS",
            "it is the shared bottleneck for multiplier bounds and DeltaK.",
        ),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": decision_id,
            "decision": decision,
            "result": result,
            "rationale": rationale,
            **flags(),
        }
        for decision_id, decision, result, rationale in rows
    ]


def local_status_rows() -> list[dict[str, Any]]:
    rows = [
        ("LOCAL1530_0_lambda_bound", "lambda_phi multiplier bound", "FORMULA_ONLY", "constants/norms missing"),
        ("LOCAL1530_1_delta_g_SGamma", "delta_g S_Gamma", "REDUCED_TO_KMETRIC_KERNELS", "operator norm not sourced"),
        ("LOCAL1530_2_projection", "observable projection", "SCHEMA_ONLY", "Pi_gamma/C_op/GM missing"),
        ("LOCAL1530_3_Khat", "current Khat adoption", "NOT_PROMOTED", "lambda_phi bound unresolved"),
        ("LOCAL1530_4_GR", "derived local GR/Newton", "NOT_CLAIMED", "q_loc/DeltaK/C_op downstream"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "status_id": status_id,
            "claim": claim,
            "current_status": status,
            "reason": reason,
            **flags(),
        }
        for status_id, claim, status, reason in rows
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "next_id": "NEXT1530_0_1531",
            "next_target": "1531-Y5-delta-g-SGamma-Kmetric-kernel-norm-source-pass.md",
            "script": "scripts/Y5_delta_g_SGamma_Kmetric_kernel_norm_source_pass.py",
            "objective": "source or bound the Kmetric kernel norms controlling delta_g S_Gamma: M_m, M_L, K_conn, K_domain, K_boundary, sign/units, L_cg, F, and F_prime; decide whether the multiplier-stress bound can progress",
            "do_not": "do not set delta_g S_Gamma to zero from fixed-point language; do not promote Khat/local GR; do not edit formalization-workbench",
            **flags(),
        }
    ]


def copy_outputs() -> None:
    copies = [
        (INPUT_AUDIT, QUAR_INPUTS),
        (ANALYTIC_CONTRACT, QUAR_ANALYTIC),
        (DELTAG_REDUCTION, QUAR_DELTAG),
        (DECISION, QUAR_DECISION),
        (INPUT_AUDIT, BRANCH_INPUTS),
        (ANALYTIC_CONTRACT, BRANCH_ANALYTIC),
        (DELTAG_REDUCTION, BRANCH_DELTAG),
        (DECISION, BRANCH_DECISION),
    ]
    for source, destination in copies:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_modified_count_since_start() -> int:
    if not FORMALIZATION.exists():
        return 0
    return sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= START_TS)


def validation_rows(generated_csvs: list[Path]) -> list[dict[str, Any]]:
    sources = read_csv(SOURCE_REGISTER)
    audit = read_csv(INPUT_AUDIT)
    analytic = read_csv(ANALYTIC_CONTRACT)
    deltag = read_csv(DELTAG_REDUCTION)
    projection = read_csv(OBS_PROJECTION)
    runners = read_csv(RUNNER)
    rejections = read_csv(REJECTION_LEDGER)
    gates = read_csv(CLAIM_GATE)
    decisions = read_csv(DECISION)
    next_rows = read_csv(NEXT_TARGET)

    checks = [
        ("VAL1530_0_sources_exist", all(row["exists"] == "True" for row in sources), "all cited 1530 input source paths exist"),
        ("VAL1530_1_all_inputs_audited", len(audit) >= 9 and any(row["audit_id"] == "BIA1530_6_delta_g_SGamma_norm" for row in audit), "all requested bound inputs audited"),
        ("VAL1530_2_analytic_contract", any(row["contract_id"] == "ABC1530_3_abs_envelope" and row["status"] == "COMPOSITE_BOUND_FORM_WRITTEN" for row in analytic), "composite lambda_phi bound form written"),
        ("VAL1530_3_delta_g_reduced", any(row["reduction_id"] == "DGS1530_5_verdict" and row["status"] == "NOT_NUMERIC_REDUCED_TO_KERNELS" for row in deltag), "delta_g S_Gamma reduced to Kmetric kernel norms"),
        ("VAL1530_4_projection_schema", any(row["projection_id"] == "OBS1530_4_verdict" and row["status"] == "NOT_SCORE_READY" for row in projection), "observable projection remains schema-only"),
        ("VAL1530_5_runners_blocked", all(row["result"].startswith("BLOCKED") for row in runners), "bound/Khat runners remain blocked"),
        ("VAL1530_6_rejections_guardrails", len(rejections) >= 7 and all(row["status"] == "REJECTED" for row in rejections), "unsafe shortcuts rejected"),
        ("VAL1530_7_claim_gates_block", any(row["gate_id"] == "GATE1530_6_local_GR" and row["status"] == "BLOCKED_NO_CLAIM" for row in gates), "local GR claim remains blocked"),
        ("VAL1530_8_decision_next", any(row["result"] == "NEXT_1531_KMETRIC_KERNEL_NORMS" for row in decisions), "decision selects Kmetric kernel norm source pass next"),
        ("VAL1530_9_next_target", any("1531-Y5-delta-g-SGamma" in row["next_target"] for row in next_rows), "next target is delta_g S_Gamma Kmetric kernel norm source pass"),
        ("VAL1530_10_csv_parse", all(parse_csv(path) for path in generated_csvs), "all generated 1530 CSVs parse cleanly"),
        ("VAL1530_11_claim_flags_false", generated_flags_false(generated_csvs), "all generated prediction/claim flags remain false"),
        ("VAL1530_12_branch_copies", all(path.exists() for path in [QUAR_INPUTS, QUAR_ANALYTIC, QUAR_DELTAG, QUAR_DECISION, BRANCH_INPUTS, BRANCH_ANALYTIC, BRANCH_DELTAG, BRANCH_DECISION]), "branch/quarantine nonclaim copies written"),
        ("VAL1530_13_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL1530_14_formalization_untouched", formalization_modified_count_since_start() == 0, "formalization modified-file count since start=0"),
    ]
    overall = all(result for _, result, _ in checks)
    rows = [
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
        }
        for check_id, result, detail in checks
    ]
    rows.append(
        {
            "same_parent_branch_id": BRANCH_ID,
            "check_id": "VAL1530_15_overall",
            "result": "PASS" if overall else "FAIL",
            "detail": "1530 organizes lambda_phi bound algebra, reduces delta_g S_Gamma to Kmetric kernel norms, keeps claims blocked, and selects Kmetric kernel norm sourcing next"
            if overall
            else "1530 validation failed; inspect failed rows before continuing",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    output = ["| " + " | ".join(columns) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    for row in rows:
        output.append(
            "| "
            + " | ".join(str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns)
            + " |"
        )
    return "\n".join(output)


def write_doc(
    sources: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    analytic: list[dict[str, Any]],
    deltag: list[dict[str, Any]],
    projection: list[dict[str, Any]],
    runners: list[dict[str, Any]],
    rejections: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    local_rows: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> None:
    DOC.write_text(
        "\n".join(
            [
                "# 1530 - Lambda Phi Bound Input Source Pass",
                "",
                "## Verdict",
                "- The multiplier-stress bound is now organized as a composite absolute envelope, but it is not numeric or score-ready.",
                "- `C_P`, `C_E`, and `C_T` have conditional analytic forms only; domain geometry, zero-mode ownership, elliptic branch, and metric norm conventions are missing.",
                "- The sharpest sourced reduction is `delta_g S_Gamma=(2/3)delta_g Gamma_eff`, which reduces the operator norm to the same `Kmetric` kernels blocking `DeltaK`.",
                "- Observable projection into `S_total`, `Q_loc`, and `q_loc_hat` is schema-only because `Pi_gamma`, `C_op`, and measured-GM normalization are not live.",
                "- No `lambda_phi`, `K_hat`, `DeltaK`, local-GR/Newton, or PPN claim is promoted from 1530.",
                "",
                "## Source Register",
                md_table(sources, ["source_id", "source_path", "exists", "purpose"]),
                "",
                "## Bound Input Source Audit",
                md_table(audit, ["audit_id", "quantity", "target", "status", "finding", "missing_to_promote"]),
                "",
                "## Analytic Bound Contract",
                md_table(analytic, ["contract_id", "quantity", "formula_or_contract", "status", "missing_to_promote"]),
                "",
                "## Delta g S_Gamma Reduction",
                md_table(deltag, ["reduction_id", "quantity", "formula_or_statement", "status", "missing_to_promote"]),
                "",
                "## Observable Projection Contract",
                md_table(projection, ["projection_id", "quantity", "formula_or_statement", "status", "missing_to_promote"]),
                "",
                "## Bound Input Runner",
                md_table(runners, ["runner_id", "route", "required_inputs", "current_inputs", "result", "next_required_object"]),
                "",
                "## Rejection Ledger",
                md_table(rejections, ["rejection_id", "shortcut", "status", "reason"]),
                "",
                "## Claim Gates",
                md_table(gates, ["gate_id", "claim", "status", "reason"]),
                "",
                "## Decision",
                md_table(decisions, ["decision_id", "decision", "result", "rationale"]),
                "",
                "## Local GR / Newton Status",
                md_table(local_rows, ["status_id", "claim", "current_status", "reason"]),
                "",
                "## Validation",
                md_table(validation, ["check_id", "result", "detail"]),
                "",
                "## Next Target",
                md_table(next_rows, ["next_id", "next_target", "script", "objective", "do_not"]),
                "",
            ]
        ),
        encoding="utf-8",
    )


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_register_rows()
    audit = input_audit_rows()
    analytic = analytic_contract_rows()
    deltag = deltag_reduction_rows()
    projection = observable_projection_rows()
    runners = runner_rows()
    rejections = rejection_rows()
    gates = claim_gate_rows()
    decisions = decision_rows()
    local_rows = local_status_rows()
    next_rows = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(INPUT_AUDIT, audit)
    write_csv(ANALYTIC_CONTRACT, analytic)
    write_csv(DELTAG_REDUCTION, deltag)
    write_csv(OBS_PROJECTION, projection)
    write_csv(RUNNER, runners)
    write_csv(REJECTION_LEDGER, rejections)
    write_csv(CLAIM_GATE, gates)
    write_csv(DECISION, decisions)
    write_csv(LOCAL_STATUS, local_rows)
    write_csv(NEXT_TARGET, next_rows)
    copy_outputs()
    remove_pycache()

    generated_csvs = [
        SOURCE_REGISTER,
        INPUT_AUDIT,
        ANALYTIC_CONTRACT,
        DELTAG_REDUCTION,
        OBS_PROJECTION,
        RUNNER,
        REJECTION_LEDGER,
        CLAIM_GATE,
        DECISION,
        LOCAL_STATUS,
        NEXT_TARGET,
    ]
    validation = validation_rows(generated_csvs)
    write_csv(VALIDATION, validation)
    write_doc(sources, audit, analytic, deltag, projection, runners, rejections, gates, decisions, local_rows, validation, next_rows)


if __name__ == "__main__":
    main()
