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
PARENT_ACTION = ROOT / "source-intake" / "parent-action"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
FORMALIZATION = PROJECT / "formalization-workbench"

CHECKPOINT = "3003"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"

DOC = ROOT / "3003-Y5-R2FR-unfixed-reference-Bv-selector-or-Delta-ref-component-bound-under-AX1090.md"

OUTPUTS = {
    "sources": RESIDUALS / "P8_Y5_R2FR_3003_SOURCE_REGISTER.csv",
    "selector": RESIDUALS / "P8_Y5_R2FR_3003_UNFIXED_REFERENCE_SELECTOR_AUDIT.csv",
    "derivatives": RESIDUALS / "P8_Y5_R2FR_3003_DELTA_REF_DERIVATIVE_VECTOR_ROWS.csv",
    "bounds": RESIDUALS / "P8_Y5_R2FR_3003_EPSILON_BV_UNFIXED_REFERENCE_BOUND_ROWS.csv",
    "rebase": RESIDUALS / "P8_Y5_R2FR_3003_BV_REBASE_AFTER_REFERENCE_SELECTOR.csv",
    "gates": RESIDUALS / "P8_Y5_R2FR_3003_PROMOTION_GATES.csv",
    "decision": RESIDUALS / "P8_Y5_R2FR_3003_DECISION_LEDGER.csv",
    "next": RESIDUALS / "P8_Y5_R2FR_3003_NEXT_TARGET.csv",
    "branches": RESIDUALS / "P8_Y5_R2FR_3003_BRANCH_COPIES.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_3003_VALIDATION.csv",
}

BRANCH_OUTPUTS = {
    "selector_copy": PARENT_ACTION / "unfixed_reference_Bv_selector_3003_NOT_SIGNED.csv",
    "bounds_copy": LOCAL_BOUNDS / "epsilon_Bv_unfixed_reference_bound_rows_3003_NONCLAIM.csv",
    "next_copy": RAB_QUEUE / "JR3003_PROJECTOR_BOUNDARY_BV_NEXT_NONCLAIM.csv",
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


def anchors(path: Path, needles: list[str]) -> bool:
    haystack = text(path)
    return path.exists() and all(needle in haystack for needle in needles)


def missing_anchors(path: Path, needles: list[str]) -> str:
    haystack = text(path)
    return "; ".join(needle for needle in needles if needle not in haystack)


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


def under(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def boolish(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass", "passed"}


def md_table(output_rows: list[dict[str, Any]], columns: list[str]) -> str:
    header = "| " + " | ".join(columns) + " |"
    divider = "| " + " | ".join("---" for _ in columns) + " |"
    lines = [header, divider]
    for output_row in output_rows:
        cells = [str(output_row.get(column, "")).replace("\n", " ").replace("|", "/") for column in columns]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SOURCE_SPECS = [
    (
        "SRC3003_00_3002_next",
        RESIDUALS / "P8_Y5_R2FR_3002_NEXT_TARGET.csv",
        ["NEXT3002_0_3003", "epsilon_Bv_unfixed_reference"],
        "3002 selects unfixed-reference Bv as next primary boundary debt.",
    ),
    (
        "SRC3003_01_3002_rebase",
        RESIDUALS / "P8_Y5_R2FR_3002_BV_REBASE_AFTER_CORNER_TOPOLOGICAL_CLASSIFICATION.csv",
        ["REB3002_3_Bv_remainder", "MISSING_UNFIXED_REFERENCE_PROJECTOR_MREF_BOUNDS"],
        "3002 rebase leaves unfixed reference, projector-boundary and denominator open.",
    ),
    (
        "SRC3003_02_2991_epsilon",
        RESIDUALS / "P8_Y5_R2FR_2991_EPSILON_BV_SOURCE_BOUND_ROWS_NONCLAIM.csv",
        ["EBV2991_05_unfixed_reference", "MISSING_PARENT_BREF_RULE"],
        "2991 defines epsilon_Bv_unfixed_reference as abs(D_v B_ref)/M_ref.",
    ),
    (
        "SRC3003_03_2546_classification",
        RESIDUALS / "P8_Y5_NO_SHADOW_2546_BOUNDARY_TERM_CLASSIFICATION.csv",
        ["BTC2546_4_fixed_reference", "PRIMARY_LIVE_REMAINDER"],
        "2546 identifies unfixed reference/counterterm as a primary live boundary remainder.",
    ),
    (
        "SRC3003_04_2546_certificate",
        RESIDUALS / "P8_Y5_NO_SHADOW_2546_BOUNDARY_CERTIFICATE_MATRIX.csv",
        ["BCC2546_4_fixed_reference", "MISSING_FIXED_REFERENCE_SELECTOR"],
        "2546 says the fixed reference selector certificate is missing.",
    ),
    (
        "SRC3003_05_2546_bound_row",
        RESIDUALS / "P8_Y5_NO_SHADOW_2546_BREM_BOUND_ROWS.csv",
        ["BRB2546_1_Delta_ref", "PRIMARY_NEXT_BOUND_IF_SELECTOR_FAILS"],
        "2546 gives Delta_ref_over_MH as the bound row if selector proof fails.",
    ),
    (
        "SRC3003_06_2547_selector_theorem",
        RESIDUALS / "P8_Y5_NO_SHADOW_2547_FIXED_REFERENCE_SELECTOR_THEOREM.csv",
        ["FRS2547_2_chain_rule_to_Bref", "PASS_AS_CONDITIONAL_CONTRACT"],
        "2547 proves the conditional chain-rule zero if all fixed beta_ref clauses are signed.",
    ),
    (
        "SRC3003_07_2547_signature_audit",
        RESIDUALS / "P8_Y5_NO_SHADOW_2547_SIGNATURE_AUDIT.csv",
        ["SIG2547_0_configuration_bundle", "SIG2547_7_denominator"],
        "2547 lists missing signatures: parent bundle through same-frame denominator.",
    ),
    (
        "SRC3003_08_2547_delta_ref",
        RESIDUALS / "P8_Y5_NO_SHADOW_2547_DELTA_REF_BOUND_ROWS.csv",
        ["DRB2547_4_total_absolute", "NOT_COMPUTED_COMPONENTS_MISSING"],
        "2547 stages Delta_ref absolute bound rows but has no component values.",
    ),
    (
        "SRC3003_09_2547_dirichlet",
        RESIDUALS / "P8_Y5_NO_SHADOW_2547_DIRICHLET_ACTION_CONTRACT.csv",
        ["DAC2547_0_parent_bundle", "MISSING_PARENT_CONFIGURATION_BUNDLE"],
        "2547 states the Dirichlet/fixed-beta parent contract but marks it unsigned.",
    ),
    (
        "SRC3003_10_2448_owner",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2448_BREF_RELATIVE_BOUNDARY_OWNER_CONTRACT.csv",
        ["RBO2448_6_Bref_derivative_vector", "NOT_SIGNED"],
        "2448 keeps the B_ref derivative-vector owner unsigned.",
    ),
    (
        "SRC3003_11_2448_derivative_vector",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2448_BREF_QBLIND_DERIVATIVE_VECTOR.csv",
        ["BDV2448_6_verdict", "FAIL_CURRENT_CLAIM"],
        "2448 refuses the current derivative-vector zero claim.",
    ),
    (
        "SRC3003_12_2455_embedding",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2455_BOUNDARY_REFERENCE_EMBEDDING_DERIVATION.csv",
        ["EMB2455_2_zero_condition", "CONDITIONAL_THEOREM"],
        "2455 gives exact zero condition for q/source-blind boundary reference inputs.",
    ),
    (
        "SRC3003_13_2455_delta_template",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2455_DELTA_REF_BOUND_ROW_TEMPLATE.csv",
        ["DBR2455_4_total_Delta_ref_bound", "MISSING_COMPONENT_INPUTS"],
        "2455 gives finite Delta_ref template with component inputs still missing.",
    ),
    (
        "SRC3003_14_2448_source_pack",
        RESIDUALS / "P8_Y5_PARENT_QLOC_2448_S_EQ_BOUNDARY_SOURCE_BOUND_INPUT_PACK.csv",
        ["SBI2448_0_Delta_ref", "MISSING_DELTA_REF_VALUE_AND_BREF_RULE"],
        "2448 source-bound pack requires real Delta_ref value or theorem-zero.",
    ),
]


def source_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "source_id": source_id,
                "source_path": str(path),
                "path_exists": path.exists(),
                "required_anchors": "; ".join(needles),
                "anchors_found": anchors(path, needles),
                "missing_anchors": missing_anchors(path, needles),
                "role": role,
            }
        )
        for source_id, path, needles, role in SOURCE_SPECS
    ]


def selector_rows() -> list[dict[str, Any]]:
    data = [
        (
            "URS3003_0_parent_bundle",
            "parent configuration bundle beta_ref is declared before q/source/readout",
            "MISSING_PARENT_CONFIGURATION_BUNDLE",
            "without a parent-owned beta_ref bundle, B_ref can become a tuning knob",
            "SIG2547_0_configuration_bundle;DAC2547_0_parent_bundle",
        ),
        (
            "URS3003_1_surface_domain",
            "surface/domain pair is fixed before source/readout variation",
            "MISSING_SOURCE_BLIND_SURFACE_DOMAIN_RULE",
            "a moving domain leaks into D_v B_ref",
            "SIG2547_1_surface_domain;BTC2546_4_fixed_reference",
        ),
        (
            "URS3003_2_metric_boundary",
            "boundary metric or induced data obey D_a sigma_AB=0",
            "MISSING_BOUNDARY_METRIC_ZERO_CERTIFICATE",
            "metric leak contributes C_sigma*D_a sigma_AB",
            "SIG2547_2_metric;EMB2455_2_zero_condition",
        ),
        (
            "URS3003_3_tau_coframe",
            "tau/coframe lock obeys D_a tau=0 in the same boundary frame",
            "MISSING_TAU_COFRAME_LOCK",
            "tau/coframe leak contributes C_tau*D_a tau",
            "SIG2547_3_tau;EMB2455_2_zero_condition",
        ),
        (
            "URS3003_4_topology",
            "C_top is superselected or silent under the relevant vertical variation",
            "MISSING_CTOP_SUPERSELECTION_CERTIFICATE",
            "topological leak contributes C_top*D_a C_top",
            "SIG2547_4_topology;RBO2448_1_Ctop_superselection",
        ),
        (
            "URS3003_5_counterterm",
            "counterterm B_ct is fixed by parent action, not fitted after readout",
            "MISSING_COUNTERTERM_ZERO_CERTIFICATE",
            "counterterm leak contributes D_a B_ct",
            "SIG2547_5_counterterm;DAC2547_3_reference_functional",
        ),
        (
            "URS3003_6_embedding_operator",
            "embedding/regularity operator norm exists for the boundary reference functional",
            "MISSING_EMBEDDING_HESSIAN_OR_OPERATOR_NORM",
            "finite bound cannot be computed without C_sigma/C_tau/C_top response norms",
            "SIG2547_6_embedding;DBR2455_2_embedding_operator_norm",
        ),
        (
            "URS3003_7_denominator",
            "same-frame positive M_ref or M_H_ref is available without observed-GM import",
            "MISSING_SAME_FRAME_N_E_OR_MHREF",
            "dimensionless residual cannot be normalized claim-safely",
            "SIG2547_7_denominator;BRB2546_1_Delta_ref",
        ),
        (
            "URS3003_8_conditional_chain_rule",
            "if URS3003_0 through URS3003_7 are parent-signed, D_a B_ref=0",
            "CONDITIONAL_THEOREM_PRESENT_NOT_SIGNED",
            "FRS2547_2 and EMB2455_2 supply the route, but current MTS lacks the signatures",
            "FRS2547_2_chain_rule_to_Bref;EMB2455_2_zero_condition",
        ),
        (
            "URS3003_9_verdict",
            "epsilon_Bv_unfixed_reference zero selector",
            "ZERO_NOT_PROMOTED_BOUND_ROWS_STAGED",
            "selector proof remains conditional and no finite Delta_ref value exists",
            "all rows above",
        ),
    ]
    return [
        base(
            {
                "audit_id": audit_id,
                "selector_clause": selector_clause,
                "current_status": current_status,
                "failure_mode": failure_mode,
                "source_anchors": source_anchors,
                "parent_signed_now": False,
                "theorem_zero_now": False,
            }
        )
        for audit_id, selector_clause, current_status, failure_mode, source_anchors in data
    ]


def derivative_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DRV3003_0_partial_q",
            "partial_q Delta_ref",
            "D_q B_ref / M_ref",
            "MISSING_PARENT_BREF_RULE",
            "needs parent-owned beta_ref plus q-blind boundary data or finite C_sigma,C_tau,C_top,B_ct inputs",
        ),
        (
            "DRV3003_1_partial_source",
            "partial_source Delta_ref",
            "D_source B_ref / M_ref",
            "MISSING_PARENT_BREF_RULE",
            "needs source-blind selector and no post-readout counterterm selection",
        ),
        (
            "DRV3003_2_partial_r",
            "partial_r Delta_ref",
            "D_r B_ref / M_ref",
            "MISSING_PARENT_BREF_RULE",
            "needs radial reference branch fixed before local readout",
        ),
        (
            "DRV3003_3_partial_t",
            "partial_t Delta_ref",
            "D_t B_ref / M_ref",
            "MISSING_PARENT_BREF_RULE",
            "needs time/reference synchronization rule and coframe lock",
        ),
        (
            "DRV3003_4_partial_frame",
            "partial_frame Delta_ref",
            "D_frame B_ref / M_ref",
            "MISSING_FRAME_SELECTOR",
            "needs frame-invariant boundary reference or explicit frame-response norm",
        ),
        (
            "DRV3003_5_partial_lambda",
            "partial_lambda Delta_ref",
            "D_lambda B_ref / M_ref",
            "MISSING_SCALE_SELECTOR",
            "needs scale/regularization branch fixed before comparing arenas",
        ),
        (
            "DRV3003_6_total_absolute",
            "Delta_ref derivative-vector absolute sum",
            "sum_abs(DRV3003_0..5)",
            "NOT_COMPUTED_COMPONENTS_MISSING",
            "no cancellation allowed; finite value requires every component and denominator sourced",
        ),
    ]
    return [
        base(
            {
                "derivative_id": derivative_id,
                "quantity": quantity,
                "bound_interface": bound_interface,
                "current_value": "MISSING_VALUE",
                "status": status,
                "required_inputs": required_inputs,
                "units": "dimensionless_after_same_frame_M_ref",
                "source_anchors": "RBO2448_6_Bref_derivative_vector;BDV2448_6_verdict;DBR2455_4_total_Delta_ref_bound",
                "finite_numeric_value_present": False,
                "theorem_zero_now": False,
            }
        )
        for derivative_id, quantity, bound_interface, status, required_inputs in data
    ]


def bound_rows() -> list[dict[str, Any]]:
    data = [
        (
            "BUR3003_0_zero_switch",
            "epsilon_Bv_unfixed_reference_zero_if_fixed_selector",
            "0 if beta_ref=(surface, sigma_AB, tau, C_top, B_ct) is parent-fixed before q/source/readout and D_a beta_ref=0",
            "CONDITIONAL_ZERO_NOT_PROMOTED",
            "FRS2547_2_chain_rule_to_Bref;EMB2455_2_zero_condition",
        ),
        (
            "BUR3003_1_metric_leak",
            "Delta_ref_metric_leak",
            "C_sigma*max(||D_q sigma||,||D_source sigma||,||D_r sigma||,||D_t sigma||)/M_ref",
            "MISSING_BOUND_VALUE",
            "DRB2547_1_metric_leak;DBR2455_0_partial_q_Bref_bound",
        ),
        (
            "BUR3003_2_tau_leak",
            "Delta_ref_tau_leak",
            "C_tau*max(||D_q tau||,||D_source tau||,||D_r tau||,||D_t tau||)/M_ref",
            "MISSING_BOUND_VALUE",
            "DRB2547_2_tau_leak;DBR2455_1_partial_source_Bref_bound",
        ),
        (
            "BUR3003_3_topology_counterterm_leak",
            "Delta_ref_topology_counterterm_leak",
            "max(C_top|D_a C_top|+|D_a B_ct|)/M_ref over a in {q,source,r,t,frame,lambda}",
            "MISSING_BOUND_VALUE",
            "DRB2547_3_topology_counterterm_leak;SIG2547_4_topology;SIG2547_5_counterterm",
        ),
        (
            "BUR3003_4_total_absolute",
            "Delta_ref_total_absolute",
            "sum_abs(BUR3003_1,BUR3003_2,BUR3003_3,branch_drift)/M_ref",
            "NOT_COMPUTED_COMPONENTS_MISSING",
            "DRB2547_4_total_absolute;BRB2546_1_Delta_ref",
        ),
        (
            "BUR3003_5_epsilon_unfixed_reference",
            "epsilon_Bv_unfixed_reference",
            "abs(D_v B_ref)/M_ref <= Delta_ref_total_absolute with no cancellation import",
            "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "EBV2991_05_unfixed_reference;SBI2448_0_Delta_ref",
        ),
    ]
    return [
        base(
            {
                "bound_id": bound_id,
                "symbol": symbol,
                "bound_interface": bound_interface,
                "current_value": "MISSING_VALUE" if "ZERO" not in status else "NOT_ALLOWED_AS_VALUE",
                "status": status,
                "source_anchors": source_anchors,
                "units": "dimensionless_after_same_frame_M_ref",
                "finite_numeric_value_present": False,
                "theorem_zero_now": False,
            }
        )
        for bound_id, symbol, bound_interface, status, source_anchors in data
    ]


def rebase_rows() -> list[dict[str, Any]]:
    data = [
        (
            "REB3003_0_exact_fixed",
            "epsilon_Bv_exact_fixed_primitive",
            "0",
            "closed only as exact/fixed component by 2999",
        ),
        (
            "REB3003_1_tau_surface",
            "epsilon_Bv_tau_surface_commutator_total_abs",
            "COMPONENTS_MISSING_NO_FINITE_VALUE",
            "demoted to explicit residual closure by 3001",
        ),
        (
            "REB3003_2_corner_topological",
            "epsilon_Bv_corner_topological_total_abs",
            "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "classified and staged by 3002",
        ),
        (
            "REB3003_3_unfixed_reference",
            "epsilon_Bv_unfixed_reference",
            "MISSING_SOURCE_BACKED_UPPER_BOUND",
            "3003 finds conditional selector only; no theorem-zero or finite Delta_ref value",
        ),
        (
            "REB3003_4_Bv_remainder",
            "epsilon_Bv_remainder_after_3003",
            "MISSING_PROJECTOR_BOUNDARY_MREF_BOUNDS",
            "next Bv debts are projector-boundary silence/commutator and denominator",
        ),
        (
            "REB3003_5_kernel",
            "epsilon_kernel_charge_public_SRNG_rebased_3003",
            "MISSING_THETA_PARENT_QV_BV_REMAINDER_CV_ZERO_FLUX_MREF",
            "Bv is narrower but full kernel charge remains open",
        ),
    ]
    return [
        base(
            {
                "rebase_id": rebase_id,
                "symbol": symbol,
                "current_value": current_value,
                "status": status,
            }
        )
        for rebase_id, symbol, current_value, status in data
    ]


def gate_rows() -> list[dict[str, Any]]:
    data = [
        (
            "GATE3003_0_sources",
            "3003 source anchors exist",
            "PASS",
            True,
            False,
            "all required prior checkpoint anchors are present",
        ),
        (
            "GATE3003_1_selector_zero",
            "epsilon_Bv_unfixed_reference=0 can be promoted",
            "CONDITIONAL_ONLY_FAIL_CLOSED",
            False,
            False,
            "parent beta_ref bundle, surface/domain, metric, tau, C_top, counterterm, embedding and denominator signatures are missing",
        ),
        (
            "GATE3003_2_finite_delta_ref",
            "finite Delta_ref value exists",
            "BLOCKED_NONCLAIM",
            False,
            False,
            "component values and same-frame M_ref/M_H_ref are missing",
        ),
        (
            "GATE3003_3_no_cancellation",
            "unfixed reference is not used as a cancellation knob",
            "PASS_AS_GUARDRAIL",
            True,
            False,
            "3003 refuses observed-GM import and keeps all rows nonclaim",
        ),
        (
            "GATE3003_4_full_Bv_zero",
            "epsilon_Bv_ambiguity=0",
            "FAIL_CLOSED",
            False,
            False,
            "projector-boundary and M_ref debts remain even after reference selector audit",
        ),
        (
            "GATE3003_5_local_claims",
            "local GR/Newton/PPN/WEP/R10 claim allowed",
            "FAIL_CLOSED",
            False,
            False,
            "kernel charge and Bv remainder still open",
        ),
    ]
    return [
        base(
            {
                "gate_id": gate_id,
                "gate": gate,
                "gate_status": gate_status,
                "condition_passed": condition_passed,
                "promotion_allowed_now": promotion_allowed_now,
                "reason": reason,
            }
        )
        for gate_id, gate, gate_status, condition_passed, promotion_allowed_now, reason in data
    ]


def decision_rows() -> list[dict[str, Any]]:
    data = [
        (
            "DEC3003_0_contract",
            "Keep the fixed-reference selector as an exact conditional contract.",
            "FRS2547_2 and EMB2455_2 show the chain-rule zero if parent beta_ref is fixed before q/source/readout.",
            "retain as parent-action requirement, not current theorem-zero",
        ),
        (
            "DEC3003_1_no_zero",
            "Do not promote epsilon_Bv_unfixed_reference=0.",
            "Current MTS lacks parent signatures for beta_ref ownership, surface/domain, metric, tau, C_top, counterterm, embedding and denominator.",
            "stage Delta_ref derivative-vector rows instead",
        ),
        (
            "DEC3003_2_no_value",
            "Do not assign a finite Delta_ref value.",
            "No source-backed derivative-vector components or same-frame M_ref/M_H_ref exist; importing observed GM would be circular.",
            "all finite-value rows stay valid_for_claim=false",
        ),
        (
            "DEC3003_3_demote_route",
            "Demote unfixed-reference closure to explicit residual unless the parent action signs it later.",
            "This prevents the reference/counterterm route becoming a hidden cancellation knob.",
            "move to projector-boundary Bv silence next",
        ),
    ]
    return [
        base(
            {
                "decision_id": decision_id,
                "decision": decision,
                "rationale": rationale,
                "next_effect": next_effect,
            }
        )
        for decision_id, decision, rationale, next_effect in data
    ]


def next_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "next_id": "NEXT3003_0_3004",
                "priority": "selected_primary",
                "target_doc": "3004-Y5-R2FR-projector-boundary-Bv-silence-or-PiM-boundary-commutator-bound-under-AX1090.md",
                "target_script": "scripts/Y5_R2FR_projector_boundary_Bv_silence_or_PiM_boundary_commutator_bound_under_AX1090_3004.py",
                "mission": "Attack epsilon_Bv_projector_boundary: prove projector/source-measure boundary contribution is silent in the same domain for q, Pi_M, Q_tau and readout, or stage finite projector-boundary commutator rows.",
                "success_condition": "projector-boundary Bv component becomes theorem-zero by parent silence/domain signatures or gains a finite source-backed Pi_M boundary commutator bound row",
                "fallback_if_fail": "demote projector-boundary route to explicit residual closure and move to M_ref/denominator ownership",
                "guardrails": "no full Bv zero claim; no epsilon_kernel_charge claim; no local-GR/Newton/PPN/WEP/R10 claim; no GitHub; no formalization-workbench edits",
            }
        )
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        base(
            {
                "copy_id": copy_id,
                "path": str(path),
                "path_exists": path.exists(),
                "row_count": len(rows(path)),
                "csv_parse_ok": csv_ok(path),
                "claim_flags_present": any(boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) for row in rows(path)),
            }
        )
        for copy_id, path in BRANCH_OUTPUTS.items()
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    selector: list[dict[str, Any]],
    derivatives: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    rebase: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output_paths = list(OUTPUTS.values()) + list(BRANCH_OUTPUTS.values()) + [DOC]
    generated_rows = sources + selector + derivatives + bounds + rebase + gates + decisions + next_target + branches
    targeted_formalization_hits = []
    if FORMALIZATION.exists():
        patterns = [
            "*Y5_R2FR_3003*",
            "*3003-Y5-R2FR*",
            "*unfixed_reference_Bv_selector_3003*",
            "*epsilon_Bv_unfixed_reference_bound_rows_3003*",
            "*JR3003_PROJECTOR_BOUNDARY*",
        ]
        for pattern in patterns:
            targeted_formalization_hits.extend(FORMALIZATION.rglob(pattern))

    checks = [
        (
            "VAL3003_00_sources_exist",
            all(boolish(row["path_exists"]) for row in sources),
            "every cited source path exists",
            True,
        ),
        (
            "VAL3003_01_source_anchors",
            all(boolish(row["anchors_found"]) for row in sources),
            "every source has required anchors",
            True,
        ),
        (
            "VAL3003_02_selector_not_promoted",
            any(row["audit_id"] == "URS3003_9_verdict" for row in selector)
            and not any(boolish(row["theorem_zero_now"]) for row in selector),
            "selector proof remains conditional, not current theorem-zero",
            True,
        ),
        (
            "VAL3003_03_missing_signature_clauses",
            all(
                expected in {row["current_status"] for row in selector}
                for expected in {
                    "MISSING_PARENT_CONFIGURATION_BUNDLE",
                    "MISSING_SOURCE_BLIND_SURFACE_DOMAIN_RULE",
                    "MISSING_BOUNDARY_METRIC_ZERO_CERTIFICATE",
                    "MISSING_TAU_COFRAME_LOCK",
                    "MISSING_CTOP_SUPERSELECTION_CERTIFICATE",
                    "MISSING_COUNTERTERM_ZERO_CERTIFICATE",
                    "MISSING_EMBEDDING_HESSIAN_OR_OPERATOR_NORM",
                    "MISSING_SAME_FRAME_N_E_OR_MHREF",
                }
            ),
            "selector audit preserves all missing parent clauses",
            True,
        ),
        (
            "VAL3003_04_derivative_rows_nonclaim",
            len(derivatives) == 7
            and all(not boolish(row["valid_for_claim"]) and not boolish(row["claim_allowed"]) for row in derivatives),
            "Delta_ref derivative-vector rows are staged and nonclaim",
            True,
        ),
        (
            "VAL3003_05_bounds_nonclaim",
            len(bounds) == 6
            and all(not boolish(row["valid_for_claim"]) and not boolish(row["claim_allowed"]) for row in bounds),
            "epsilon_Bv_unfixed_reference bound rows are nonclaim",
            True,
        ),
        (
            "VAL3003_06_no_finite_values_fabricated",
            all(
                "MISSING" in str(row.get("current_value", "")) or str(row.get("current_value")) == "NOT_ALLOWED_AS_VALUE"
                for row in bounds
            ),
            "no finite Delta_ref or epsilon_Bv value fabricated",
            True,
        ),
        (
            "VAL3003_07_local_claims_blocked",
            all(row["promotion_allowed_now"] is False for row in gates),
            "no local GR/Newton/PPN/WEP/R10 promotion allowed",
            True,
        ),
        (
            "VAL3003_08_next_target_projector",
            len(next_target) == 1 and "projector-boundary" in next_target[0]["mission"],
            "3004 selects projector-boundary Bv next",
            True,
        ),
        (
            "VAL3003_09_branch_copies",
            len(branches) == 3
            and all(boolish(row["path_exists"]) and boolish(row["csv_parse_ok"]) for row in branches)
            and not any(boolish(row["claim_flags_present"]) for row in branches),
            "branch copies exist, parse, and carry no claim flags",
            True,
        ),
        (
            "VAL3003_10_csv_parse",
            all(csv_ok(path) for path in OUTPUTS.values() if path.suffix == ".csv"),
            "all 3003 CSV outputs parse cleanly",
            True,
        ),
        (
            "VAL3003_11_paths_under_post_checkpoint",
            all(under(path, ROOT) for path in output_paths),
            "all generated outputs are under post-checkpoint-work",
            True,
        ),
        (
            "VAL3003_12_formalization_untouched",
            len(targeted_formalization_hits) == 0,
            "no targeted 3003 files exist under formalization-workbench",
            True,
        ),
        (
            "VAL3003_13_no_claim_flags",
            not any(boolish(row.get("valid_for_claim")) or boolish(row.get("claim_allowed")) for row in generated_rows),
            "all generated rows remain valid_for_claim=false and claim_allowed=false",
            True,
        ),
    ]
    preliminary = [
        base(
            {
                "validation_id": validation_id,
                "passed": passed,
                "detail": detail,
                "required": required,
            }
        )
        for validation_id, passed, detail, required in checks
    ]
    overall = all(boolish(row["passed"]) for row in preliminary if boolish(row["required"]))
    preliminary.append(
        base(
            {
                "validation_id": "VAL3003_OVERALL",
                "passed": overall,
                "detail": "3003 refuses unfixed-reference zero/value promotion, stages Delta_ref derivative/bound rows, and selects projector-boundary Bv next",
                "required": True,
            }
        )
    )
    return preliminary


def write_doc(
    sources: list[dict[str, Any]],
    selector: list[dict[str, Any]],
    derivatives: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    rebase: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# 3003 - Y5/R2FR Unfixed-Reference Bv Selector Or Delta-ref Component Bound Under AX1090

Status: `Y5_R2FR_3003_unfixed_reference_selector_conditional_zero_not_promoted_Delta_ref_rows_staged_3004_next`

Generated: `{RUN_UTC}`

## Current Verdict

3003 attacks `epsilon_Bv_unfixed_reference`, the boundary/reference/counterterm channel where a theory can accidentally smuggle in a cancellation knob.

There is a clean conditional route: if the parent action fixes the reference bundle `beta_ref=(surface, sigma_AB, tau, C_top, B_ct)` before `q`, source, frame, radius, time, scale and readout variations, then the chain rule gives `D_a B_ref=0`, hence the unfixed-reference component vanishes.

Current MTS does not yet sign the required parent clauses. The fixed-reference selector is therefore not promoted, and no finite `Delta_ref` value is fabricated. The win is narrower but real: the reference/counterterm danger is now an explicit residual with derivative-vector rows and guardrails, not a hidden free choice.

## Source Register

{md_table(sources, ["source_id", "path_exists", "anchors_found", "missing_anchors", "role"])}

## Unfixed-Reference Selector Audit

{md_table(selector, ["audit_id", "selector_clause", "current_status", "failure_mode", "source_anchors"])}

## Delta_ref Derivative-Vector Rows

{md_table(derivatives, ["derivative_id", "quantity", "bound_interface", "current_value", "status", "required_inputs"])}

## epsilon_Bv Unfixed-Reference Bound Rows

{md_table(bounds, ["bound_id", "symbol", "bound_interface", "current_value", "status", "source_anchors"])}

## Bv Rebase After 3003

{md_table(rebase, ["rebase_id", "symbol", "current_value", "status"])}

## Promotion Gates

{md_table(gates, ["gate_id", "gate", "gate_status", "condition_passed", "promotion_allowed_now", "reason"])}

## Decision Ledger

{md_table(decisions, ["decision_id", "decision", "rationale", "next_effect"])}

## Next Target

{md_table(next_target, ["next_id", "target_doc", "mission", "success_condition", "guardrails"])}

## Branch Copies

{md_table(branches, ["copy_id", "path", "path_exists", "row_count", "csv_parse_ok", "claim_flags_present"])}

## Validation

{md_table(validation, ["validation_id", "passed", "detail", "required"])}

## Plain-English Takeaway

This is not a shiny knockout, but it is a good defensive round. The reference/counterterm piece was one of the places critics could say, "you tuned the boundary term after seeing the answer." 3003 says: no, we either prove the parent action fixes it first, or we pay a named `Delta_ref` bill. Right now we have the conditional proof path, but not the parent signatures, so the route stays closure-only.

## Forbidden Claims From 3003

- `epsilon_Bv_unfixed_reference=0`.
- `Delta_ref_total_absolute` has a finite sourced value.
- `epsilon_Bv_ambiguity=0`.
- `epsilon_kernel_charge_public_SRNG=0`.
- Local GR/Newton/PPN/WEP/R10 pass.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    sources = source_rows()
    selector = selector_rows()
    derivatives = derivative_rows()
    bounds = bound_rows()
    rebase = rebase_rows()
    gates = gate_rows()
    decisions = decision_rows()
    next_target = next_rows()

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["selector"], selector)
    write_csv(OUTPUTS["derivatives"], derivatives)
    write_csv(OUTPUTS["bounds"], bounds)
    write_csv(OUTPUTS["rebase"], rebase)
    write_csv(OUTPUTS["gates"], gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next"], next_target)

    shutil.copyfile(OUTPUTS["selector"], BRANCH_OUTPUTS["selector_copy"])
    shutil.copyfile(OUTPUTS["bounds"], BRANCH_OUTPUTS["bounds_copy"])
    shutil.copyfile(OUTPUTS["next"], BRANCH_OUTPUTS["next_copy"])

    branches = branch_rows()
    write_csv(OUTPUTS["branches"], branches)
    validation = validation_rows(sources, selector, derivatives, bounds, rebase, gates, decisions, next_target, branches)
    write_csv(OUTPUTS["validation"], validation)
    write_doc(sources, selector, derivatives, bounds, rebase, gates, decisions, next_target, branches, validation)

    overall = next(row for row in validation if row["validation_id"] == "VAL3003_OVERALL")
    if not boolish(overall["passed"]):
        raise SystemExit("3003 validation failed; see P8_Y5_BRR545_3003_VALIDATION.csv")

    print(f"wrote {DOC}")
    print(f"validation {overall['passed']}: {overall['detail']}")


if __name__ == "__main__":
    main()
