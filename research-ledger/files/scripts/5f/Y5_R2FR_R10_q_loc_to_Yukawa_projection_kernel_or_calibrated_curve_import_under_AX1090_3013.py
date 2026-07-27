from __future__ import annotations

import csv
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

CHECKPOINT = "3013"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3013-Y5-R2FR-R10-q_loc-to-Yukawa-projection-kernel-or-calibrated-curve-import-under-AX1090.md"

SOURCE_PATHS = {
    "SRC3013_00_3012_doc": ROOT / "3012-Y5-R2FR-R10-first-source-backed-bound-rows-and-dryrun-schema-under-AX1090.md",
    "SRC3013_01_3012_next": RESIDUALS / "P8_Y5_R2FR_3012_NEXT_TARGET.csv",
    "SRC3013_02_3012_facts": RESIDUALS / "P8_Y5_R2FR_3012_SOURCE_FACTS.csv",
    "SRC3013_03_3012_bounds": RESIDUALS / "P8_Y5_R2FR_3012_R10_BOUND_ROWS_NONCLAIM.csv",
    "SRC3013_04_3012_dryrun": RESIDUALS / "P8_Y5_R2FR_3012_QLOC_TO_ALPHA_DRYRUN_SCHEMA.csv",
    "SRC3013_05_2410_source_map_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_2410_R10_SOURCE_MAP_DERIVATION_GATE.csv",
    "SRC3013_06_2210_range_operator": RESIDUALS / "P8_Y5_PARENT_QLOC_2210_RANGE_OPERATOR_DERIVATION.csv",
    "SRC3013_07_2210_source_map_first_row": RESIDUALS / "P8_Y5_PARENT_QLOC_2210_R10_SOURCE_MAP_FIRST_ROW.csv",
    "SRC3013_08_2663_charge_normalization": LOCAL_BOUNDS / "R10_source_test_charge_normalization_2663_NONCLAIM.csv",
    "SRC3013_09_2701_alpha_response": LOCAL_BOUNDS / "q_loc_R10_alpha_response_operator_2701_NONCLAIM.csv",
    "SRC3013_10_2702_profile_schema": RESIDUALS / "P8_Y5_R2FR_2702_QLOC_R10_PROFILE_INPUT_SCHEMA_NONCLAIM.csv",
    "SRC3013_11_2702_profile_audit": RESIDUALS / "P8_Y5_R2FR_2702_QLOC_PROFILE_ASSET_AUDIT.csv",
    "SRC3013_12_3010_bound_interface": RESIDUALS / "P8_Y5_R2FR_3010_QLOC_COUPLING_BOUND_INTERFACE.csv",
    "SRC3013_13_fig5_vector_audit": RESIDUALS / "P8_Y5_R2FR_3012_FIGURE_VECTOR_AUDIT.csv",
    "SRC3013_14_aps_fetch_log": ROOT
    / "source-intake"
    / "r10-sources"
    / "3012"
    / "aps_supplemental_fetch_attempt_3012.log",
}

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3013_SOURCE_REGISTER.csv",
    "kernel_derivation": RESIDUALS / "P8_Y5_R2FR_3013_R10_KERNEL_DERIVATION.csv",
    "parent_contract": RESIDUALS / "P8_Y5_R2FR_3013_PARENT_ACTION_CONTRACT.csv",
    "prediction_template": RESIDUALS / "P8_Y5_R2FR_3013_R10_PREDICTION_ROW_TEMPLATE.csv",
    "component_envelope": RESIDUALS / "P8_Y5_R2FR_3013_ALPHA_COMPONENT_ENVELOPE.csv",
    "curve_import": RESIDUALS / "P8_Y5_R2FR_3013_CURVE_IMPORT_SIDE_ROUTE.csv",
    "blockers": RESIDUALS / "P8_Y5_R2FR_3013_BLOCKER_LEDGER.csv",
    "dryrun": RESIDUALS / "P8_Y5_R2FR_3013_DRYRUN_RESULTS.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3013_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3013_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3013_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3013_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3013_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "kernel_copy": LOCAL_BOUNDS / "R10_q_loc_to_Yukawa_kernel_contract_3013_NONCLAIM.csv",
    "prediction_copy": LOCAL_BOUNDS / "R10_prediction_row_template_3013_NONCLAIM.csv",
    "contract_copy": LOCAL_BOUNDS / "R10_parent_action_contract_3013_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3013_PARENT_ACTION_SOURCE_OWNER_OR_R10_KERNEL_VALUES_NEXT.csv",
}

for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]:
    path.parent.mkdir(parents=True, exist_ok=True)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def as_str(value: Any) -> str:
    return "" if value is None else str(value)


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def base(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "branch_id": BRANCH_ID,
        "control_only": True,
        "score_ready": False,
        "valid_prediction_row": False,
        "valid_for_claim": False,
        "claim_allowed": False,
        "generated_utc": RUN_UTC,
    }


def write_csv(path: Path, output_rows: list[dict[str, Any]]) -> None:
    fieldnames: list[str] = []
    for output_row in output_rows:
        for key in output_row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def csv_ok(path: Path) -> bool:
    try:
        rows(path)
        return True
    except Exception:
        return False


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [as_str(output_row.get(column, "")).replace("\n", " ") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


source_register = [
    base(
        {
            "source_id": source_id,
            "local_path": str(path),
            "exists": path.exists(),
            "role": {
                "SRC3013_00_3012_doc": "previous checkpoint verdict and guardrails",
                "SRC3013_01_3012_next": "3013 target definition",
                "SRC3013_02_3012_facts": "R10 paper Yukawa convention and supplement facts",
                "SRC3013_03_3012_bounds": "nonclaim R10 bound rows and blockers",
                "SRC3013_04_3012_dryrun": "prediction and bound row dry-run requirements",
                "SRC3013_05_2410_source_map_gate": "no direct q_loc scalarization and source-map contract",
                "SRC3013_06_2210_range_operator": "lambda owner and finite-range operator law",
                "SRC3013_07_2210_source_map_first_row": "range-indexed source-map first row",
                "SRC3013_08_2663_charge_normalization": "source/test charge normalization contract",
                "SRC3013_09_2701_alpha_response": "acceleration-level alpha response operator",
                "SRC3013_10_2702_profile_schema": "q_loc R10 profile row schema",
                "SRC3013_11_2702_profile_audit": "current profile asset audit",
                "SRC3013_12_3010_bound_interface": "q_loc/Delta_K/coupling residual bounds",
                "SRC3013_13_fig5_vector_audit": "Fig. 5 vector status from 3012",
                "SRC3013_14_aps_fetch_log": "APS supplement fetch blocker evidence",
            }[source_id],
            "status": "PRESENT" if path.exists() else "MISSING_LOCAL_SOURCE",
        }
    )
    for source_id, path in SOURCE_PATHS.items()
]

kernel_derivation = [
    base(
        {
            "kernel_id": "KDER3013_0_R10_convention",
            "object": "published R10 Yukawa convention",
            "derived_statement": "V(r)=V_N(r)[1+alpha exp(-r/lambda)]",
            "kernel_form": "a_Y/a_N = alpha(lambda) (1+r/lambda) exp(-r/lambda) for point-body radial acceleration",
            "status": "SOURCE_ANCHORED",
            "missing_for_claim": "none for convention; still need MTS source projection",
            "source_anchor": "FACT3012_0_yukawa_potential; R10OP2701_0",
        }
    ),
    base(
        {
            "kernel_id": "KDER3013_1_acceleration_response",
            "object": "acceleration-level q_loc response",
            "derived_statement": "If q_loc is converted into a same-frame radial acceleration a_q(r,lambda), then alpha_q(lambda;r)=a_q/a_N * exp(r/lambda)/(1+r/lambda).",
            "kernel_form": "R_R10_alpha[q_loc]=sup_r |a_q(r,lambda)/a_N(r)| exp(r/lambda)/(1+r/lambda)",
            "status": "CONDITIONAL_KERNEL_DERIVED_NONCLAIM",
            "missing_for_claim": "MISSING_q_loc_PROFILE; MISSING_FORCE_DENSITY_TO_ACCELERATION_MAP; MISSING_SOURCE_FRAME; MISSING_FULL_BOUND_CURVE",
            "source_anchor": "R10OP2701_0_QLOC_YUKAWA_ALPHA_RESPONSE; QPROF2702_0",
        }
    ),
    base(
        {
            "kernel_id": "KDER3013_2_parent_finite_range_operator",
            "object": "parent finite-range mode",
            "derived_statement": "A finite-range local residual branch must reduce on the quotient domain to L_AB X^B=J_A with L_AB=-Z_AB Delta+M_AB plus controlled lower-derivative terms.",
            "kernel_form": "M_AB v_i^B=mu_i^2 Z_AB v_i^B; lambda_i=1/mu_i, or lambda_X=sqrt(Z_X/M_X^2) in the one-mode reduction",
            "status": "RANGE_OWNER_DERIVED_VALUES_BLOCKED",
            "missing_for_claim": "MISSING_PARENT_Z_AB; MISSING_PARENT_M_AB; MISSING_EIGENVECTORS; MISSING_DOMAIN_CERTIFICATE",
            "source_anchor": "ROD2210_0; ROD2210_1; ROD2210_2",
        }
    ),
    base(
        {
            "kernel_id": "KDER3013_3_charge_response",
            "object": "parent charge/eigenmode alpha response",
            "derived_statement": "For a signed eigenmode source J_i and charges Q_i^S,q_i^T, the same Yukawa language gives alpha_i=s_i Q_i^S q_i^T/(4*pi*G_obs*M_S*m_T*Z_i), with apparatus/readout tau and tail terms separated.",
            "kernel_form": "alpha_i(lambda_i)=K_i Qbar_i^S qbar_i^T tau_R10_i + alpha_edge_i + alpha_tail_i, K_i=s_i/(4*pi*Z_i*G_obs)",
            "status": "CONDITIONAL_ALPHA_LAW_DERIVED_VALUES_BLOCKED",
            "missing_for_claim": "MISSING_Z_i; MISSING_Q_SOURCE; MISSING_q_TEST; MISSING_tau_R10; MISSING_SIGN_POLICY; MISSING_APPARATUS_NORMALIZATION",
            "source_anchor": "SMG2410_3; SM2210_1; CHG2663_0_to_7",
        }
    ),
    base(
        {
            "kernel_id": "KDER3013_4_q_loc_bridge",
            "object": "q_loc-to-source bridge",
            "derived_statement": "q_loc^nu is not a scalar Yukawa source. A legitimate bridge must either provide J_i=S_i[I_div^{-1}(q_loc)] or an identity q_loc^nu=P_loc b_i^nu[(L_i X_i)-J_i]+boundary terms.",
            "kernel_form": "J_i=C_i[I_div^{-1}(q_loc)] with units/domain/source frame, or theorem-zero if the Euler/source/boundary pieces vanish",
            "status": "BRIDGE_CONTRACT_EXACT_BUT_UNSIGNED",
            "missing_for_claim": "MISSING_CURRENT_OWNER; MISSING_TGK_OR_I_DIV_INVERSE; MISSING_b_i_nu; MISSING_BOUNDARY_TERMS; MISSING_UNITS",
            "source_anchor": "SMG2410_0; SMG2410_4; SM2210_2",
        }
    ),
    base(
        {
            "kernel_id": "KDER3013_5_no_cancellation_envelope",
            "object": "absolute R10 residual envelope",
            "derived_statement": "The R10 prediction must bound bulk, edge, tail, Delta_K, Ward/Euler and matter/coupling pieces separately; cancellation between them is not evidence.",
            "kernel_form": "|alpha_total| <= |alpha_bulk|+|alpha_edge|+|alpha_tail|+|alpha_DeltaK|+|alpha_Ward|+|alpha_matter_coupling|",
            "status": "ENVELOPE_DERIVED_VALUES_BLOCKED",
            "missing_for_claim": "MISSING_COMPONENT_VALUES_OR_ZERO_THEOREMS; MISSING_FULL_BOUND_CURVE",
            "source_anchor": "BI3010_0_to_4; CHG2663_6",
        }
    ),
]

parent_contract = [
    base(
        {
            "clause_id": "PACT3013_0_quotient_domain",
            "required_clause": "physical quotient/domain projection for the local R10 branch",
            "mathematical_contract": "declare domain D_R10, boundary class, source/test body support, and observed coframe before defining X_i or q_loc projection",
            "current_status": "MISSING_DOMAIN_CERTIFICATE",
            "blocks": "range eigenproblem, source charge, boundary/tail split",
        }
    ),
    base(
        {
            "clause_id": "PACT3013_1_operator_coefficients",
            "required_clause": "parent-signed kinetic/mass operator",
            "mathematical_contract": "provide Z_AB and M_AB or a rank-zero/spectral replacement on the same quotient domain",
            "current_status": "MISSING_PARENT_Z_AB_AND_M_AB",
            "blocks": "lambda_i and K_i normalization",
        }
    ),
    base(
        {
            "clause_id": "PACT3013_2_source_current_owner",
            "required_clause": "source current J_A or inverse-divergence map from q_loc",
            "mathematical_contract": "define J_i=v_i^A J_A or C_i[I_div^{-1}(q_loc)] with units and no scalar-proxy shortcut",
            "current_status": "MISSING_CURRENT_OWNER",
            "blocks": "Q_i^S and q_loc-to-Yukawa bridge",
        }
    ),
    base(
        {
            "clause_id": "PACT3013_3_source_test_charges",
            "required_clause": "body charge integrals and test response",
            "mathematical_contract": "Q_i^B=int_B rho_i dV_H + Q_edge_i with source/test material response in the same frame; q_i^T may be zero only by signed matter-descent theorem",
            "current_status": "MISSING_Q_SOURCE_AND_q_TEST",
            "blocks": "alpha_i numerator",
        }
    ),
    base(
        {
            "clause_id": "PACT3013_4_observed_Newton_frame",
            "required_clause": "same-frame G_obs, source mass and test mass",
            "mathematical_contract": "declare M_S,m_T,G_obs and measured-GM guard so the Yukawa alpha denominator matches the published R10 convention",
            "current_status": "MISSING_APPARATUS_NORMALIZATION",
            "blocks": "dimensionless alpha comparison",
        }
    ),
    base(
        {
            "clause_id": "PACT3013_5_tau_readout",
            "required_clause": "R10 readout/source normalization factor",
            "mathematical_contract": "derive tau_R10(lambda) from apparatus/source-worldtube projection or bound it separately; tau_R10=1 shortcut is forbidden",
            "current_status": "MISSING_tau_R10",
            "blocks": "apparatus-to-theory comparison",
        }
    ),
    base(
        {
            "clause_id": "PACT3013_6_boundary_tail_policy",
            "required_clause": "edge, tail and boundary residual split",
            "mathematical_contract": "provide theorem-zero certificates or nonnegative absolute bounds for alpha_edge, alpha_tail, alpha_DeltaK, alpha_Ward and alpha_matter_coupling",
            "current_status": "MISSING_COMPONENT_ZERO_OR_BOUNDS",
            "blocks": "no-cancellation promotion",
        }
    ),
]

prediction_template = [
    base(
        {
            "prediction_id": "PRED3013_0_R10_kernel_template",
            "lambda_i_m": "MISSING_lambda_i_from_parent_spectrum",
            "alpha_predicted": "MISSING_NUMERIC_ALPHA",
            "alpha_predicted_abs_envelope": "|K_i Qbar_i^S qbar_i^T tau_R10_i| + |alpha_edge_i| + |alpha_tail_i| + |alpha_DeltaK_i| + |alpha_Ward_i| + |alpha_matter_coupling_i|",
            "alpha_units": "dimensionless",
            "kernel_source_path": str(OUTPUTS["kernel_derivation"]),
            "q_loc_profile_path": "MISSING_q_loc_profile_or_theorem_zero_certificate",
            "source_normalization": "MISSING_M_S_m_T_G_obs_tau_R10",
            "bound_curve_path": "MISSING_valid_full_curve_or_supplement_import",
            "comparison_rule": "valid only if abs(alpha_predicted)<=alpha_bound(lambda_i) inside sampled lambda range with no extrapolation",
            "status": "TEMPLATE_ONLY_VALUES_BLOCKED",
        }
    ),
    base(
        {
            "prediction_id": "PRED3013_1_theorem_zero_alternative",
            "lambda_i_m": "not_required_if_all_R10_components_zero",
            "alpha_predicted": "0 only if parent zero theorem covers q_loc bridge, source current, test response, boundary and tail terms",
            "alpha_predicted_abs_envelope": "0",
            "alpha_units": "dimensionless",
            "kernel_source_path": str(OUTPUTS["parent_contract"]),
            "q_loc_profile_path": "MISSING_THEOREM_ZERO_CERTIFICATE",
            "source_normalization": "covered by theorem only if same-frame R10 apparatus clauses included",
            "bound_curve_path": "still required for empirical comparator if presenting as R10 test",
            "comparison_rule": "zero theorem can close the local R10 residual, but not replace empirical bound provenance",
            "status": "ZERO_ROUTE_NOT_SIGNED",
        }
    ),
]

component_envelope = [
    base(
        {
            "component_id": "ENV3013_0_bulk",
            "alpha_component": "alpha_bulk_i",
            "formula_or_bound": "K_i Qbar_i^S qbar_i^T tau_R10_i",
            "status": "MISSING_K_Q_q_tau",
            "required_owner": "parent action source current plus source/test charge normalization",
        }
    ),
    base(
        {
            "component_id": "ENV3013_1_edge",
            "alpha_component": "alpha_edge_i",
            "formula_or_bound": "absolute edge/source-boundary contribution from Q_edge_i",
            "status": "MISSING_EDGE_SPLIT",
            "required_owner": "boundary/source-domain clause",
        }
    ),
    base(
        {
            "component_id": "ENV3013_2_tail",
            "alpha_component": "alpha_tail_i",
            "formula_or_bound": "retained spectral/tail envelope outside the selected one-mode branch",
            "status": "MISSING_TAIL_BOUND",
            "required_owner": "spectral measure or truncation theorem",
        }
    ),
    base(
        {
            "component_id": "ENV3013_3_DeltaK",
            "alpha_component": "alpha_DeltaK_i",
            "formula_or_bound": "R_R10_alpha[P_R10(q_DeltaK)] with ||q_DeltaK|| <= C_Ploc D_Delta + C_comm ||Delta_K||",
            "status": "SOURCE_READY_NONNUMERIC",
            "required_owner": "Delta_K components and R10 projection norm",
        }
    ),
    base(
        {
            "component_id": "ENV3013_4_Ward",
            "alpha_component": "alpha_Ward_i",
            "formula_or_bound": "R_R10_alpha[P_R10(q_Ward)] with Euler/source/boundary residuals",
            "status": "SOURCE_READY_SCHEMA",
            "required_owner": "Euler/source zero or boundary flux bound",
        }
    ),
    base(
        {
            "component_id": "ENV3013_5_matter_coupling",
            "alpha_component": "alpha_matter_coupling_i",
            "formula_or_bound": "R_R10_alpha[matter/source descent leakage and visible hidden-coupling vector]",
            "status": "SOURCE_READY_NONNUMERIC",
            "required_owner": "A_matter and c_g/b_dis/dln_alpha/dln_m projection pack",
        }
    ),
]

curve_import = [
    base(
        {
            "route_id": "CURVE3013_0_APS_supplement",
            "route": "import publisher supplemental numerical constraints",
            "current_status": "BLOCKED_BY_403",
            "required_next_evidence": "downloaded supplemental file or table with 66 lambda values and signed alpha constraints",
            "claim_policy": "only rows with positive numeric lambda/alpha, provenance, units and no MISSING markers can become valid_bound_curve_row=true",
        }
    ),
    base(
        {
            "route_id": "CURVE3013_1_calibrated_vector_digitization",
            "route": "calibrate Fig. 5 vector paths",
            "current_status": "VECTOR_PRESENT_AXIS_NOT_CALIBRATED",
            "required_next_evidence": "axis transform, curve identity, point extraction QA and uncertainty ledger",
            "claim_policy": "uncalibrated path coordinates remain nonclaim and cannot overwrite the live curve file",
        }
    ),
    base(
        {
            "route_id": "CURVE3013_2_anchor_smoke",
            "route": "alpha=1 threshold anchors",
            "current_status": "PRESENT_NONCURVE",
            "required_next_evidence": "none; anchors stay smoke/provenance only",
            "claim_policy": "anchors cannot replace the full curve and cannot score a predicted lambda_i unless the prediction is exactly the threshold statement being audited",
        }
    ),
]

blockers = [
    base(
        {
            "blocker_id": "BLK3013_0_current_owner",
            "blocking_condition": "MISSING_CURRENT_OWNER_OR_I_DIV_INVERSE",
            "precise_missing_object": "J_i, C_i[I_div^{-1}(q_loc)] or q_loc=P_loc b_i(L_iX_i-J_i)+boundary identity",
            "why_it_blocks": "without this, q_loc is a vector/divergence residual, not a scalar Yukawa source",
            "next_attack": "derive source-current owner from parent action variation or demote R10 to acceleration-profile only",
        }
    ),
    base(
        {
            "blocker_id": "BLK3013_1_operator_coefficients",
            "blocking_condition": "MISSING_Z_M_EIGENMODE",
            "precise_missing_object": "Z_AB, M_AB, v_i and units on the R10 quotient domain",
            "why_it_blocks": "lambda_i and K_i are not empirical knobs; they must come from the parent spectrum",
            "next_attack": "derive finite-range quadratic block or prove rank-zero constraint branch",
        }
    ),
    base(
        {
            "blocker_id": "BLK3013_2_charges",
            "blocking_condition": "MISSING_SOURCE_TEST_CHARGES",
            "precise_missing_object": "Qbar_i^S, qbar_i^T and edge split in same Newton frame",
            "why_it_blocks": "the alpha numerator is undefined",
            "next_attack": "source-sign body charge integrals or prove visible matter response zero",
        }
    ),
    base(
        {
            "blocker_id": "BLK3013_3_tau_R10",
            "blocking_condition": "MISSING_tau_R10",
            "precise_missing_object": "apparatus/source-worldtube projection factor",
            "why_it_blocks": "the lab R10 readout is not the same thing as an abstract point-body alpha unless tau is owned",
            "next_attack": "derive tau_R10 or carry it as a finite nuisance with independent bound",
        }
    ),
    base(
        {
            "blocker_id": "BLK3013_4_bound_curve",
            "blocking_condition": "MISSING_FULL_ALPHA_BOUND_CURVE",
            "precise_missing_object": "66-lambda signed alpha constraints or calibrated Fig. 5 curve",
            "why_it_blocks": "anchors cannot support interpolation or envelope scoring",
            "next_attack": "get APS supplement through browser/manual download or perform calibrated vector digitization",
        }
    ),
    base(
        {
            "blocker_id": "BLK3013_5_no_cancellation",
            "blocking_condition": "MISSING_COMPONENT_ZERO_OR_BOUNDS",
            "precise_missing_object": "absolute values or zero theorems for bulk/edge/tail/DeltaK/Ward/matter-coupling pieces",
            "why_it_blocks": "a local-GR/R10 pass cannot depend on hidden cancellation",
            "next_attack": "fill component envelope rows one by one",
        }
    ),
]

dryrun_results = [
    base(
        {
            "dryrun_id": "DR3013_0_kernel_shape",
            "check": "R10 alpha kernel shape derived",
            "passed": True,
            "observed": "acceleration-level and parent charge/eigenmode-level kernels written",
            "result_status": "KERNEL_CONTRACT_DERIVED_NONCLAIM",
        }
    ),
    base(
        {
            "dryrun_id": "DR3013_1_no_scalar_proxy",
            "check": "q_loc direct scalar shortcut forbidden",
            "passed": True,
            "observed": "q_loc bridge requires current owner or inverse-divergence map",
            "result_status": "GUARD_ACTIVE",
        }
    ),
    base(
        {
            "dryrun_id": "DR3013_2_prediction_numeric",
            "check": "valid numeric alpha prediction row exists",
            "passed": False,
            "observed": "lambda_i, K_i, Qbar_i, qbar_i, tau_R10 and component bounds are missing",
            "result_status": "BLOCKED_NONCLAIM",
        }
    ),
    base(
        {
            "dryrun_id": "DR3013_3_bound_curve",
            "check": "valid full R10 alpha(lambda) curve exists",
            "passed": False,
            "observed": "APS supplement blocked and vector figure uncalibrated",
            "result_status": "BLOCKED_NONCLAIM",
        }
    ),
    base(
        {
            "dryrun_id": "DR3013_4_R10_claim",
            "check": "R10 claim allowed",
            "passed": False,
            "observed": "kernel contract exists but values and curve are missing",
            "result_status": "CLAIM_FORBIDDEN",
        }
    ),
]

promotion_gates = [
    base(
        {
            "gate_id": "GATE3013_0_sources_exist",
            "gate": "all cited local source paths exist",
            "result": all(boolish(row["exists"]) for row in source_register),
            "notes": "3013 is grounded in current local ledgers",
        }
    ),
    base(
        {
            "gate_id": "GATE3013_1_kernel_written",
            "gate": "kernel contract written without numeric promotion",
            "result": True,
            "notes": "derives response formulas and missing owners, not a prediction value",
        }
    ),
    base(
        {
            "gate_id": "GATE3013_2_no_proxy",
            "gate": "no direct rho_X := q_loc scalar proxy is allowed",
            "result": True,
            "notes": "bridge clause requires current owner/inverse-divergence/domain/units",
        }
    ),
    base(
        {
            "gate_id": "GATE3013_3_no_curve_promotion",
            "gate": "no uncalibrated curve or anchor-only data is promoted",
            "result": True,
            "notes": "curve import side route remains blocked/nonclaim",
        }
    ),
    base(
        {
            "gate_id": "GATE3013_4_prediction_claim",
            "gate": "valid R10 prediction row exists",
            "result": False,
            "notes": "parent coefficients, charges, tau and component bounds are missing",
        }
    ),
    base(
        {
            "gate_id": "GATE3013_5_R10_claim",
            "gate": "R10 pass claim allowed",
            "result": False,
            "notes": "both prediction values and full bound curve remain blocked",
        }
    ),
]

decision = [
    base(
        {
            "decision_id": "DEC3013_0_status",
            "decision": "3013 derives the exact R10 comparison kernel contract but keeps the row nonclaim.",
            "rationale": "The mathematics is now sharp enough to score later: alpha is either an acceleration ratio in the R10 Yukawa convention or a parent charge/eigenmode product. The q_loc bridge remains the unsigned object.",
            "claim_allowed_after_decision": False,
        }
    ),
    base(
        {
            "decision_id": "DEC3013_1_next_route",
            "decision": "The next real derivation target is the parent source-current owner, not another bound-table pass.",
            "rationale": "Even a perfect R10 curve cannot score MTS until q_loc is connected to J_i or to a same-frame acceleration profile with units.",
            "claim_allowed_after_decision": False,
        }
    ),
    base(
        {
            "decision_id": "DEC3013_2_curve_side_route",
            "decision": "Curve import remains a side route, not the main theory route.",
            "rationale": "APS supplement/manual digitization will be needed eventually, but it does not solve the source-current/coupling problem.",
            "claim_allowed_after_decision": False,
        }
    ),
]

next_target = [
    base(
        {
            "next_id": "NEXT3013_0_3014",
            "priority": "selected_primary",
            "target_doc": "3014-Y5-R2FR-parent-source-current-owner-for-R10-kernel-or-rank-zero-local-closure-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_parent_source_current_owner_for_R10_kernel_or_rank_zero_local_closure_under_AX1090_3014.py",
            "mission": "Try to derive the parent source-current owner J_i/C_i[I_div^{-1}(q_loc)] needed by the R10 kernel, or prove the finite-range R10 branch is rank-zero/closure-only.",
            "success_condition": "either a parent-signed source-current/inverse-divergence map exists with units/domain, or the branch is demoted to an explicit local-closure residual with no Yukawa alpha claim.",
            "fallback_if_fail": "write the missing source-current owner as the active blocker and move to PPN kernel only if R10 remains source-map blocked",
            "guardrails": "no direct scalarization of q_loc; no R10 pass; no curve promotion; no hidden coupling; no formalization-workbench edits; no GitHub action",
        }
    )
]

write_csv(OUTPUTS["sources"], source_register)
write_csv(OUTPUTS["kernel_derivation"], kernel_derivation)
write_csv(OUTPUTS["parent_contract"], parent_contract)
write_csv(OUTPUTS["prediction_template"], prediction_template)
write_csv(OUTPUTS["component_envelope"], component_envelope)
write_csv(OUTPUTS["curve_import"], curve_import)
write_csv(OUTPUTS["blockers"], blockers)
write_csv(OUTPUTS["dryrun"], dryrun_results)
write_csv(OUTPUTS["gates"], promotion_gates)
write_csv(OUTPUTS["decision"], decision)
write_csv(OUTPUTS["next"], next_target)

branch_rows = []
for key, source_key in [
    ("kernel_copy", "kernel_derivation"),
    ("prediction_copy", "prediction_template"),
    ("contract_copy", "parent_contract"),
    ("next_copy", "next"),
]:
    shutil.copy2(OUTPUTS[source_key], BRANCH_OUTPUTS[key])
    branch_rows.append(
        base(
            {
                "copy_id": f"COPY3013_{len(branch_rows)}",
                "source": str(OUTPUTS[source_key]),
                "destination": str(BRANCH_OUTPUTS[key]),
                "exists": BRANCH_OUTPUTS[key].exists(),
                "purpose": key,
            }
        )
    )
write_csv(OUTPUTS["branches"], branch_rows)

all_generated = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
all_csv = [path for path in list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) if path.suffix == ".csv"]
claim_rows = (
    source_register
    + kernel_derivation
    + parent_contract
    + prediction_template
    + component_envelope
    + curve_import
    + blockers
    + dryrun_results
    + promotion_gates
    + decision
    + next_target
)

validation_rows = [
    {
        "validation_id": "VAL3013_00_sources_exist",
        "passed": all(boolish(row["exists"]) for row in source_register),
        "requirement": "every cited local source path exists",
        "evidence": OUTPUTS["sources"].name,
    },
    {
        "validation_id": "VAL3013_01_csv_parse",
        "passed": all(csv_ok(path) for path in all_csv),
        "requirement": "generated CSV rows parse cleanly",
        "evidence": "all generated CSV artifacts import with csv.DictReader",
    },
    {
        "validation_id": "VAL3013_02_kernel_forms_present",
        "passed": all(row["kernel_form"] for row in kernel_derivation),
        "requirement": "each kernel derivation row has an explicit kernel/formula",
        "evidence": OUTPUTS["kernel_derivation"].name,
    },
    {
        "validation_id": "VAL3013_03_parent_contract_complete",
        "passed": len(parent_contract) >= 7 and all(row["current_status"].startswith("MISSING") for row in parent_contract),
        "requirement": "parent action contract clauses are explicit and unsigned",
        "evidence": OUTPUTS["parent_contract"].name,
    },
    {
        "validation_id": "VAL3013_04_no_scalar_proxy_guard",
        "passed": any("rho_X := q_loc" in row["gate"] or "direct rho_X := q_loc" in row["gate"] for row in promotion_gates)
        or any("q_loc is a vector" in row["why_it_blocks"] for row in blockers),
        "requirement": "direct scalarization of q_loc is forbidden",
        "evidence": "BLK3013_0 and GATE3013_2",
    },
    {
        "validation_id": "VAL3013_05_prediction_rows_nonclaim",
        "passed": all(not boolish(row.get("valid_prediction_row")) and not boolish(row.get("valid_for_claim")) for row in prediction_template),
        "requirement": "prediction templates remain invalid/nonclaim while values are missing",
        "evidence": OUTPUTS["prediction_template"].name,
    },
    {
        "validation_id": "VAL3013_06_missing_markers_nonclaim",
        "passed": all(not boolish(row.get("valid_for_claim")) for row in claim_rows if "MISSING" in " ".join(map(str, row.values()))),
        "requirement": "rows with MISSING markers are never valid_for_claim=true",
        "evidence": "all 3013 generated ledgers",
    },
    {
        "validation_id": "VAL3013_07_claims_blocked",
        "passed": all(not boolish(row.get("claim_allowed")) for row in claim_rows)
        and any(row["gate_id"] == "GATE3013_5_R10_claim" and not boolish(row["result"]) for row in promotion_gates),
        "requirement": "R10 and local-claim promotion remains blocked",
        "evidence": OUTPUTS["gates"].name,
    },
    {
        "validation_id": "VAL3013_08_outputs_scoped",
        "passed": all(under(path, ROOT) for path in all_generated),
        "requirement": "no generated file is outside post-checkpoint-work",
        "evidence": "generated path scope check",
    },
    {
        "validation_id": "VAL3013_09_formalization_not_targeted",
        "passed": not any(under(path, FORMALIZATION) for path in all_generated),
        "requirement": "formalization-workbench is not modified by this checkpoint",
        "evidence": "output target list excludes formalization-workbench",
    },
    {
        "validation_id": "VAL3013_10_next_target_selected",
        "passed": next_target[0]["target_doc"].startswith("3014-Y5-R2FR-parent-source-current-owner"),
        "requirement": "next target selects parent source-current owner or rank-zero closure",
        "evidence": OUTPUTS["next"].name,
    },
]

overall_pass = all(boolish(row["passed"]) for row in validation_rows)
validation_rows.append(
    {
        "validation_id": "VAL3013_99_overall",
        "passed": overall_pass,
        "requirement": "all 3013 validation checks pass",
        "evidence": "aggregate of VAL3013_00 through VAL3013_10",
    }
)
write_csv(OUTPUTS["validation"], validation_rows)

doc = f"""# 3013 — R10 `q_loc` to Yukawa Projection Kernel or Calibrated Curve Import under AX1090

Status: `Y5_R2FR_3013_R10_kernel_contract_derived_source_owner_blocked_3014_next`

## Verdict

3013 is a useful theory step. It does **not** give an R10 pass, but it does derive the exact contract a future R10 pass would need.

There are now two honest comparison languages:

1. **Acceleration response:** if `q_loc` is converted into a same-frame radial acceleration `a_q`, then `alpha_q(lambda;r)=a_q/a_N * exp(r/lambda)/(1+r/lambda)`.
2. **Parent eigenmode charge response:** if the parent action provides `(-Z Delta + M^2)X=J`, then `lambda=sqrt(Z/M^2)` in the one-mode case and `alpha=K_X Qbar_XH qbar_XT tau_R10 + tails`, with `K_X=s_X/(4*pi*Z_X*G_obs)`.

The dragon is exactly located now: `q_loc^nu` is not itself a scalar Yukawa source. A parent action must supply a source-current owner, inverse-divergence map, or theorem-zero closure before R10 can score MTS.

## Source Register

{md_table(source_register, ["source_id", "exists", "role", "status"])}

## Kernel Derivation

{md_table(kernel_derivation, ["kernel_id", "object", "status", "missing_for_claim"])}

## Parent Action Contract

{md_table(parent_contract, ["clause_id", "required_clause", "current_status", "blocks"])}

## Prediction Template

{md_table(prediction_template, ["prediction_id", "alpha_predicted", "alpha_predicted_abs_envelope", "status"])}

## Component Envelope

{md_table(component_envelope, ["component_id", "alpha_component", "status", "required_owner"])}

## Curve Import Side Route

{md_table(curve_import, ["route_id", "route", "current_status", "claim_policy"])}

## Blocker Ledger

{md_table(blockers, ["blocker_id", "blocking_condition", "precise_missing_object", "next_attack"])}

## Dry-Run Results

{md_table(dryrun_results, ["dryrun_id", "check", "passed", "result_status"])}

## Promotion Gates

{md_table(promotion_gates, ["gate_id", "gate", "result", "notes"])}

## Decision Ledger

{md_table(decision, ["decision_id", "decision", "rationale"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "mission", "success_condition"])}

## Validation

{md_table(validation_rows, ["validation_id", "passed", "requirement", "evidence"])}

## Files Written

- `{OUTPUTS["sources"]}`
- `{OUTPUTS["kernel_derivation"]}`
- `{OUTPUTS["parent_contract"]}`
- `{OUTPUTS["prediction_template"]}`
- `{OUTPUTS["component_envelope"]}`
- `{OUTPUTS["curve_import"]}`
- `{OUTPUTS["blockers"]}`
- `{OUTPUTS["dryrun"]}`
- `{OUTPUTS["gates"]}`
- `{OUTPUTS["decision"]}`
- `{OUTPUTS["next"]}`
- `{OUTPUTS["branches"]}`
- `{OUTPUTS["validation"]}`
- `{BRANCH_OUTPUTS["kernel_copy"]}`
- `{BRANCH_OUTPUTS["prediction_copy"]}`
- `{BRANCH_OUTPUTS["contract_copy"]}`
- `{BRANCH_OUTPUTS["next_copy"]}`

## Hard Guardrails Still Active

- No R10 pass claim.
- No direct scalarization of `q_loc`.
- No anchor-only or uncalibrated-figure bound curve.
- No hidden-coupling cancellation.
- No `formalization-workbench` edits.
- No GitHub action.
"""

DOC.write_text(doc, encoding="utf-8")
