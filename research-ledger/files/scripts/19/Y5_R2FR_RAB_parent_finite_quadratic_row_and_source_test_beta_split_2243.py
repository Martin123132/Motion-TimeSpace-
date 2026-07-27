from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "2243-Y5-R2FR-RAB-parent-finite-quadratic-row-and-source-test-beta-split.md"
BRANCH_ID = "MTS_R2FR_PARENT_QLOC_RAB_FINITE_QUADRATIC_BETA_SPLIT_2243"
START_TS = datetime.now(timezone.utc).timestamp()


SOURCE_FILES = {
    "2242_doc": ROOT / "2242-Y5-R2FR-RAB-first-internal-ZR-or-tauR10-projection-row.md",
    "2242_validation": OUT / "P8_Y5_BRR545_2242_VALIDATION.csv",
    "2242_kernel_contract": OUT / "P8_Y5_PARENT_QLOC_2242_SOURCE_TEST_KERNEL_CONTRACT.csv",
    "2242_join": OUT / "P8_Y5_PARENT_QLOC_2242_INTERNAL_JOIN_READINESS.csv",
    "1036_doc": ROOT / "1036-Y5-R10-parent-X-quadratic-action-and-beta-source-test-split.md",
    "1036_validation": OUT / "P8_Y5_BRR545_1036_VALIDATION.csv",
    "1036_parent_audit": OUT / "P8_Y5_R10_1036_PARENT_X_ACTION_AUDIT.csv",
    "1036_beta": OUT / "P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
    "1036_branch": OUT / "P8_Y5_R10_1036_BRANCH_CLASSIFICATION.csv",
    "1035_charge_split": OUT / "P8_Y5_R10_1035_SOURCE_TEST_CHARGE_SPLIT.csv",
    "1035_kernel": OUT / "P8_Y5_R10_1035_KERNEL_DERIVATION_AUDIT.csv",
    "1025_hessian": ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
    "1026_metric_fail": ROOT / "1026-Y5-R10-parent-metric-ZXfX2-beta-eigenvalue-or-source-zero-return.md",
    "1027_source_zero_fail": ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
    "1028_no_marker_fail": ROOT / "1028-Y5-R10-frame-marker-coupling-bound-input-pack-or-no-marker-theorem.md",
}


SOURCE_REGISTER = OUT / "P8_Y5_PARENT_QLOC_2243_SOURCE_REGISTER.csv"
PARENT_RAB_ACTION_AUDIT = OUT / "P8_Y5_PARENT_QLOC_2243_PARENT_RAB_ACTION_AUDIT.csv"
BETA_SOURCE_TEST_DERIVATION = OUT / "P8_Y5_PARENT_QLOC_2243_BETA_SOURCE_TEST_DERIVATION.csv"
BRANCH_CLASSIFICATION = OUT / "P8_Y5_PARENT_QLOC_2243_BRANCH_CLASSIFICATION.csv"
PARENT_ACTION_ROW_TEMPLATE = OUT / "P8_Y5_PARENT_QLOC_2243_PARENT_ACTION_ROW_TEMPLATE.csv"
R10_ALPHA_TEMPLATE = OUT / "R10_alpha_lambda_curve_MTS_2243_PARENT_RAB_BETA_TEMPLATE_NONCLAIM.csv"
JOIN_GATES = OUT / "P8_Y5_PARENT_QLOC_2243_JOIN_GATES.csv"
RUNNER_SMOKE = OUT / "P8_Y5_PARENT_QLOC_2243_RUNNER_SMOKE_STATUS.csv"
PLACEHOLDER_REFUSAL = OUT / "P8_Y5_PARENT_QLOC_2243_PLACEHOLDER_REFUSAL_RUNNER.csv"
CLAIM_GATES = OUT / "P8_Y5_PARENT_QLOC_2243_CLAIM_GATES.csv"
DECISION = OUT / "P8_Y5_PARENT_QLOC_2243_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_PARENT_QLOC_2243_NEXT_TARGET.csv"
BRANCH_COPIES = OUT / "P8_Y5_PARENT_QLOC_2243_BRANCH_COPIES.csv"
VALIDATION = OUT / "P8_Y5_BRR545_2243_VALIDATION.csv"


COPY_TARGETS = {
    "queue": QUEUE / "JR2243_PARENT_FINITE_RAB_ROW_TEMPLATE_NONCLAIM.csv",
    "branch_wep": MICROSCOPE / "parent_finite_RAB_beta_split_nonclaim_2243.csv",
    "beta_docs": BETA_DOCS / "PARENT_FINITE_RAB_BETA_SPLIT_2243_NONCLAIM.csv",
}


GENERATED = [
    SOURCE_REGISTER,
    PARENT_RAB_ACTION_AUDIT,
    BETA_SOURCE_TEST_DERIVATION,
    BRANCH_CLASSIFICATION,
    PARENT_ACTION_ROW_TEMPLATE,
    R10_ALPHA_TEMPLATE,
    JOIN_GATES,
    RUNNER_SMOKE,
    PLACEHOLDER_REFUSAL,
    CLAIM_GATES,
    DECISION,
    NEXT_TARGET,
    BRANCH_COPIES,
    VALIDATION,
]


def flags() -> dict[str, bool]:
    return {
        "numeric_value_present": False,
        "source_backed": False,
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


def resolve_project_path(path_text: str) -> Path:
    path = Path(path_text.strip())
    if path.is_absolute():
        return path
    return ROOT / path


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


def validation_pass(path: Path) -> bool:
    if not path.exists():
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower() or "summary" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key, "").lower() in {"pass", "PASS".lower()} for row in overall_rows)
    return all(row.get(result_key, "").lower() in {"pass", "PASS".lower()} for row in rows)


def source_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, (key, path) in enumerate(SOURCE_FILES.items()):
        if key.startswith("2242"):
            role = "current R2FR finite-row handoff"
        elif key.startswith("1036") or key.startswith("1035"):
            role = "existing R10 finite-X/beta grammar being specialized to R_AB"
        else:
            role = "older parent/source/marker obstruction evidence"
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": f"SRC2243_{index}_{key}",
                "source_path": rel(path),
                "path_exists": path.exists(),
                "validation_overall_pass": validation_pass(path) if key.endswith("validation") else "",
                "role": role,
                **flags(),
            }
        )
    return rows


def source_register_paths_exist() -> bool:
    return all(resolve_project_path(row["source_path"]).exists() for row in read_csv(SOURCE_REGISTER))


def parent_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PRAB2243_0_branch_extremum",
            "required_parent_object": "E_R|0=0",
            "candidate_formula": "delta S_parent/delta R_AB evaluated on the local GR/Newton branch",
            "result": "MISSING_PARENT_EULER_ZERO",
            "if_missing": "R_AB=0 is not stationary by theorem; finite residual branch remains live",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PRAB2243_1_quadratic_residue",
            "required_parent_object": "Z_R",
            "candidate_formula": "Z_R is the coefficient of the projected local derivative term <D R_AB, D R^AB> in delta^2 S_parent",
            "result": "MISSING_PARENT_KINETIC_RESIDUE",
            "if_missing": "K_R cannot be numeric and ghost/anti-elliptic branches are not excluded by theorem",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PRAB2243_2_mass_gap_range",
            "required_parent_object": "M_R^2 and lambda_R",
            "candidate_formula": "lambda_R=sqrt(Z_R/M_R^2) with M_R^2 from the same parent Hessian normalization",
            "result": "RELATION_DERIVED_VALUES_MISSING",
            "if_missing": "finite-range prediction is closure-only, not a parent prediction",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PRAB2243_3_source_current",
            "required_parent_object": "J_R^{AB}",
            "candidate_formula": "J_R^{AB}=-delta_{R_AB} S_matter plus hidden/source/domain currents, projected into the R_AB slot",
            "result": "MISSING_SOURCE_ZERO_OR_SOURCE_LAW",
            "if_missing": "ordinary matter may source a finite local R_AB mode; R10/PPN/clock/orbital rows stay active",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PRAB2243_4_source_test_betas",
            "required_parent_object": "beta_source and beta_test",
            "candidate_formula": "beta_i is the parent-normalized derivative of each body's effective source/readout mass with respect to the finite R_AB channel",
            "result": "MISSING_BETA_SOURCE_TEST_SPLIT",
            "if_missing": "alpha(lambda) cannot be scored and c_g cannot be treated as a single linear coefficient",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PRAB2243_5_no_pole_alternative",
            "required_parent_object": "physical R_AB pole absent",
            "candidate_formula": "R_AB is quotient/gauge/constraint-only before local inversion; no propagating Green kernel exists",
            "result": "NO_POLE_ROUTE_NOT_SIGNED",
            "if_missing": "retain the finite pole template and bound it",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "PRAB2243_6_verdict",
            "required_parent_object": "single parent finite-R_AB row",
            "candidate_formula": "parent_signed(E_R=0, Z_R>0, M_R^2>0, J_R/beta law, boundary/tails)",
            "result": "FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED",
            "if_missing": "demote finite-R_AB R10/local branch to explicit closure/nonclaim template",
            **flags(),
        },
    ]


def beta_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "BETA2243_0_point_body_source",
            "premise": "ordinary body i has effective source/readout mass m_i[R_AB]",
            "result": "beta_i := parent-normalized derivative of ln m_i^eff with respect to the finite R_AB channel; J_R contains beta_i m_i times the projected source support",
            "status": "CONDITIONAL_STANDARD_VARIATION",
            "missing_for_claim": "parent-owned R_AB normalization and matter/readout mass functional",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "BETA2243_1_two_body_exchange",
            "premise": "finite scalar/tensor-like R_AB mode has a static Yukawa Green kernel",
            "result": "delta V_R(r)=-s_R beta_s beta_t m_s m_t exp(-r/lambda_R)/(4*pi Z_R r) after projection to the measured channel",
            "status": "CONDITIONAL_EXCHANGE_LAW",
            "missing_for_claim": "sign s_R, Z_R, lambda_R, source/test beta rows, tensor projector, and profile projection",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "BETA2243_2_R10_alpha_match",
            "premise": "R10 compares to V=V_N[1+alpha exp(-r/lambda)]",
            "result": "alpha_R=s_R beta_s beta_t/(4*pi G_N Z_R) in nonabsorbed beta units, then multiplied by source/test profile and R10 harmonic projection",
            "status": "CONDITIONAL_NORMALIZATION_SPLIT",
            "missing_for_claim": "which beta convention the parent action uses and whether tensor projection changes the scalar Yukawa normalization",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "BETA2243_3_common_Weyl_cg",
            "premise": "m_i^eff=A_g(R_AB)m_i and A_g is universal",
            "result": "alpha_R is proportional to c_g^2 for universal source and test legs unless the source leg is explicitly packed into Qbar",
            "status": "CG_SQUARED_UNLESS_SOURCE_LEG_PACKED",
            "missing_for_claim": "parent-signed A_g branch, R_AB channel normalization, and source/test profile factors",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "BETA2243_4_quotient_zero",
            "premise": "S_matter and constants descend through q and R_AB is vertical/constraint-only",
            "result": "beta_s=beta_t=0 and alpha_R=0 only if descent/no-shadow/no-marker/no-tail clauses are parent-signed together",
            "status": "CONDITIONAL_ZERO_NOT_SIGNED",
            "missing_for_claim": "parent q-kernel, matter functor, no-shadow frame, no-marker constants, and hidden-tail silence",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "derivation_id": "BETA2243_5_verdict",
            "premise": "current corpus only",
            "result": "beta law is derived as a contract, but no numeric or zero beta source/test row is claim-ready",
            "status": "BETA_ROWS_UNOWNED",
            "missing_for_claim": "parent action schema or sourced beta bounds",
            **flags(),
        },
    ]


def branch_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "branch_case_id": "BR2243_0_no_physical_RAB_pole",
            "branch": "quotient/gauge/constraint R_AB",
            "required_parent_signature": "R_AB absent from physical quotient or first-class/constraint-only with no invertible local Green kernel",
            "R10_alpha_form": "alpha_R=0 or not_applicable",
            "current_status": "BEST_LOCAL_GR_ROUTE_BUT_UNSIGNED",
            "next_action": "try no-physical-RAB-pole theorem before accepting finite residual branch",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "branch_case_id": "BR2243_1_sourcefree_massive_nohair",
            "branch": "massive finite R_AB with no local source",
            "required_parent_signature": "Z_R>0, M_R^2>0, J_R=0, boundary_flux_R=0 from one parent branch",
            "R10_alpha_form": "alpha_R=0 in local exterior by energy identity",
            "current_status": "CONDITIONAL_NOHAIR_UNSIGNED",
            "next_action": "revive only if source-zero and boundary flux close together",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "branch_case_id": "BR2243_2_sourced_finite_exchange",
            "branch": "physical finite R_AB exchange",
            "required_parent_signature": "Z_R, lambda_R, beta_source, beta_test, profile, sign, tensor projector, and tail envelope",
            "R10_alpha_form": "alpha_R=K_R^R10(lambda) beta_source beta_test + epsilon_tail",
            "current_status": "SCOREABLE_STRUCTURE_BUT_INPUTS_MISSING",
            "next_action": "if no-pole fails, build bounded beta_source/beta_test rows without cancellation",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "branch_case_id": "BR2243_3_shadow_frame_marker",
            "branch": "Weyl/disformal/marker leakage",
            "required_parent_signature": "A_g'(0), B_g'(0), marker coefficients, non-Hilbert source, and support shifts are theorem-zero or bounded",
            "R10_alpha_form": "sum of absolute source/test leakage channels, not a single clean scalar alpha",
            "current_status": "RETAINED_TAIL_BRANCH",
            "next_action": "route into no-cancellation tail envelope and cross-check WEP/clock/PPN",
            **flags(),
        },
    ]


def parent_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRA2243_0_finite_RAB_parent_row",
            "branch": "physical_finite_RAB_exchange",
            "action_density": "sqrt(-g)[-1/2 Z_R <D R_AB,D R^AB> -1/2 M_R^2 <R_AB,R^AB> + R_AB J_R^AB] plus declared boundary/tail terms",
            "Z_R": "MISSING_PARENT_KINETIC_RESIDUE",
            "M_R2": "MISSING_PARENT_MASS_GAP",
            "lambda_R": "MISSING_PARENT_RANGE",
            "J_R": "MISSING_SOURCE_CURRENT_OR_ZERO_THEOREM",
            "beta_source": "MISSING_BETA_SOURCE",
            "beta_test": "MISSING_BETA_TEST",
            "current_status": "TEMPLATE_ONLY_PARENT_ROW_NOT_OWNED",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "PRA2243_1_no_pole_parent_row",
            "branch": "no_physical_RAB_pole",
            "action_density": "R_AB is absent, pure quotient/gauge, or algebraic constraint with no propagating local pole",
            "Z_R": "not_applicable_if_no_pole_signed",
            "M_R2": "not_applicable_if_no_pole_signed",
            "lambda_R": "not_applicable_if_no_pole_signed",
            "J_R": "zero_or_constraint_current_only_if_parent_signed",
            "beta_source": "0_if_matter_descends_and_no_shadow_signed",
            "beta_test": "0_if_matter_descends_and_no_shadow_signed",
            "current_status": "BEST_THEOREM_ROUTE_UNSIGNED",
            **flags(),
        },
    ]


def r10_alpha_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "model_id": "MTS_source_normalized_Newton_branch",
            "template_branch": "parent_RAB_beta_product_template",
            "lambda_value": "MISSING_PARENT_LAMBDA_R",
            "alpha_predicted": "MISSING_KR_BETA_SOURCE_BETA_TEST_TAIL_ENVELOPE",
            "force_law_form": "alpha_R(lambda)=K_R^R10(lambda) beta_source(lambda) beta_test(lambda)+epsilon_tail(lambda)",
            "derivation_status": "template_invalid_missing_parent_action_row_and_beta_split",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "model_id": "MTS_source_normalized_Newton_branch",
            "template_branch": "universal_weyl_cg_squared_template",
            "lambda_value": "MISSING_PARENT_LAMBDA_R",
            "alpha_predicted": "MISSING_NUMERIC_KR_TIMES_CG_SQUARED_AND_PROFILE",
            "force_law_form": "universal Weyl finite exchange: alpha_R proportional to K_R^R10 c_g^2",
            "derivation_status": "template_invalid_missing_parent_cg_ZR_lambda_and_profile",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "model_id": "MTS_source_normalized_Newton_branch",
            "template_branch": "no_physical_RAB_pole_template",
            "lambda_value": "ALL_LOCAL_R10_RANGE",
            "alpha_predicted": "MISSING_NO_PHYSICAL_RAB_POLE_THEOREM",
            "force_law_form": "no finite Yukawa alpha if R_AB has no physical pole and hidden tails are zero/bounded",
            "derivation_status": "template_invalid_missing_no_pole_parent_action_signature",
            **flags(),
        },
    ]


def join_rows() -> list[dict[str, Any]]:
    return [
        ("JOIN2243_0_parent_row", "parent finite-R_AB row", "E_R=0, Z_R, M_R2, lambda_R, J_R/beta law, sign, boundary/tails from one parent branch", "MISSING_PARENT_ROW"),
        ("JOIN2243_1_beta_product", "beta_source beta_test", "numeric/source-backed or zero-theorem beta_source and beta_test rows", "MISSING_BETA_SOURCE_TEST_SPLIT"),
        ("JOIN2243_2_cg_law", "c_g versus c_g^2 policy", "explicit declaration whether Qbar already contains the source leg", "LAW_CORRECTED_NO_NUMERIC_INPUTS"),
        ("JOIN2243_3_external_bound", "R10 alpha_bound(lambda)", "promoted digitized/official bound curve", "REVIEW_CANDIDATE_NONCLAIM"),
        ("JOIN2243_4_no_cancellation", "absolute tail envelope", "all hidden/marker/disformal/non-Hilbert/support terms zero or bounded in absolute sum", "MISSING_ABSOLUTE_TAIL_ENVELOPE"),
    ]


def join_dicts() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "object": obj,
            "required_for_claim": required,
            "current_status": status,
            "ready": False,
            **flags(),
        }
        for gate_id, obj, required, status in join_rows()
    ]


def runner_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "smoke_id": "SMOKE2243_0_runner_status",
            "valid_mts_rows": 0,
            "valid_bound_rows": 0,
            "comparison_rows": 1,
            "R10_pass_for_claim": False,
            "expected_result": "blocked_nonclaim",
            **flags(),
        }
    ]


def refusal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, obj, status in [
        ("REF2243_TEMPLATE_0", "PRA2243_0_finite_RAB_parent_row", "TEMPLATE_ONLY_PARENT_ROW_NOT_OWNED"),
        ("REF2243_TEMPLATE_1", "PRA2243_1_no_pole_parent_row", "BEST_THEOREM_ROUTE_UNSIGNED"),
    ]:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": source_id,
                "object": obj,
                "current_status": status,
                "refusal_status": "rejected_parent_action_template_only",
                "failure_reasons": "MISSING_PARENT_INPUTS;NOT_SCORE_READY;CLAIM_POLICY_FALSE",
                "score_eligible": False,
                **flags(),
            }
        )
    for row in join_dicts():
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "refusal_id": row["gate_id"].replace("JOIN2243", "REF2243_JOIN"),
                "object": row["object"],
                "current_status": row["current_status"],
                "refusal_status": "rejected_join_gate_not_ready",
                "failure_reasons": f"{row['current_status']};READY_FALSE;CLAIM_POLICY_FALSE",
                "score_eligible": False,
                **flags(),
            }
        )
    return rows


def claim_rows() -> list[dict[str, Any]]:
    return [
        ("CGATE2243_0_parent_action_row", "single parent action supplies the finite R_AB row", "E_R, Z_R, M_R2/lambda_R, J_R, beta split, projector, and tails are not parent-signed together"),
        ("CGATE2243_1_numeric_alpha", "MTS has numeric alpha_predicted(lambda)", "K_R, beta_source, beta_test, lambda_R, profile, and promoted bound curve are missing"),
        ("CGATE2243_2_linear_cg", "R10 alpha may be scored as linear in c_g", "source-test exchange gives c_g squared for universal Weyl legs unless source leg is explicitly included elsewhere"),
        ("CGATE2243_3_no_pole", "no physical R_AB pole is derived", "no-pole/quotient route remains conditional in current parent evidence"),
        ("CGATE2243_4_local_GR_R10", "local GR/R10 pass is established", "parent-action row and empirical score inputs remain nonclaim"),
    ]


def claim_dicts() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "gate_id": gate_id,
            "claim": claim,
            "gate_pass": False,
            "reason": reason,
            **flags(),
        }
        for gate_id, claim, reason in claim_rows()
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2243_0_parent_row_status",
            "decision": "The parent finite-R_AB quadratic row is not owned by the current corpus.",
            "because": "the necessary pieces exist only as conditional contracts spread across older Hessian/source/marker gates and the 2242 kernel contract",
            "next_action": "keep the finite-R_AB branch as a closure/nonclaim template unless a parent action signs all pieces",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2243_1_coupling_law_status",
            "decision": "The corrected coupling law is beta_source times beta_test.",
            "because": "two-body exchange forbids a single naked coupling coefficient; universal c_g enters twice",
            "next_action": "future R10/PPN templates must require beta_source, beta_test, and a declaration of whether Qbar contains a source leg",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2243_2_best_route",
            "decision": "The least-scrutiny route is still no physical R_AB pole; the fallback is bounded beta rows.",
            "because": "a derived no-pole/constraint branch gives GR reduction cleaner than tuning a short-range finite residual",
            "next_action": "try no-physical-RAB-pole theorem first, then bounded beta_source/beta_test acquisition",
            **flags(),
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC2243_3_next_target",
            "decision": "Next target is no physical R_AB pole or bounded beta runner.",
            "because": "this is the fork that decides whether local GR is derived structurally or tested as a finite residual",
            "next_action": "2244-Y5-R2FR-RAB-no-physical-pole-theorem-or-bounded-beta-runner.md",
            **flags(),
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "next_target": "2244-Y5-R2FR-RAB-no-physical-pole-theorem-or-bounded-beta-runner.md",
            "script": "scripts/Y5_R2FR_RAB_no_physical_pole_theorem_or_bounded_beta_runner_2244.py",
            "objective": "try to prove the finite local R_AB mode has no physical pole in the GR/Newton branch; if not, build bounded beta_source/beta_test acquisition rows with no-cancellation tails",
            "include": "quotient/gauge/constraint pole audit, Hessian degeneracy or first-class certificate, algebraic constraint alternative, beta_source/beta_test row schema, c_g^2 convention, R10/PPN/clock/WEP routing",
            "exclude": "asserted alpha=0, invented beta/c_g values, linear-c_g R10 score, cancellation between unknown tails, R10 pass claim, formalization-workbench edits, GitHub action",
            **flags(),
        }
    ]


def copy_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, target in COPY_TARGETS.items():
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(PARENT_ACTION_ROW_TEMPLATE, target)
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "copy_id": copy_id,
                "source_path": rel(PARENT_ACTION_ROW_TEMPLATE),
                "target_path": rel(target),
                "copied": target.exists(),
                "parse_ok": parse_csv(target),
                **flags(),
            }
        )
    return rows


def generated_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    keys = ["numeric_value_present", "source_backed", "score_ready", "valid_prediction_row", "valid_for_claim", "claim_allowed"]
    for path in paths:
        for row in read_csv(path):
            for key in keys:
                if key in row and str(row[key]).strip().lower() not in false_values:
                    return False
    return True


def all_claims_blocked() -> bool:
    return all(row.get("gate_pass", "").lower() == "false" and row.get("claim_allowed", "").lower() == "false" for row in read_csv(CLAIM_GATES))


def join_gates_blocked() -> bool:
    return all(row.get("ready", "").lower() == "false" for row in read_csv(JOIN_GATES))


def parent_template_nonclaim() -> bool:
    text = " ".join(" ".join(row.values()) for row in read_csv(PARENT_ACTION_ROW_TEMPLATE))
    return "MISSING_PARENT" in text and "TEMPLATE_ONLY" in text


def beta_product_law_present() -> bool:
    text = " ".join(" ".join(row.values()) for row in read_csv(BETA_SOURCE_TEST_DERIVATION))
    return "beta_s beta_t" in text and "c_g^2" in text


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def formalization_2243_artifacts_absent() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(
        path.is_file()
        and "2243" in path.name
        and ".venv" not in path.relative_to(FORMALIZATION).parts
        for path in FORMALIZATION.rglob("*")
    )


def formalization_untouched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return True
    return not any(path.is_file() and path.stat().st_mtime >= START_TS for path in FORMALIZATION.rglob("*"))


def validation_rows(generated_paths: list[Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_00_sources_exist",
            "result": "PASS" if all(path.exists() for path in SOURCE_FILES.values()) and source_register_paths_exist() else "FAIL",
            "detail": "all direct and registered 2243 source paths exist",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_01_prior_validations",
            "result": "PASS" if validation_pass(SOURCE_FILES["2242_validation"]) and validation_pass(SOURCE_FILES["1036_validation"]) else "FAIL",
            "detail": "2242 and 1036 validations pass overall",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_02_parent_action_audit_complete",
            "result": "PASS" if any(row.get("result") == "FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED" for row in read_csv(PARENT_RAB_ACTION_AUDIT)) else "FAIL",
            "detail": "parent finite R_AB row audit reaches non-owned verdict",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_03_beta_product_law",
            "result": "PASS" if beta_product_law_present() else "FAIL",
            "detail": "beta source/test product and c_g-squared law are explicit",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_04_branch_fork_complete",
            "result": "PASS" if len(read_csv(BRANCH_CLASSIFICATION)) == 4 else "FAIL",
            "detail": "branch classification covers no-pole, nohair, finite exchange, and tail branches",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_05_parent_templates_nonclaim",
            "result": "PASS" if parent_template_nonclaim() else "FAIL",
            "detail": "parent action templates are nonclaim and unscoreable",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_06_mts_template_nonclaim",
            "result": "PASS" if all(row.get("valid_for_claim", "").lower() == "false" for row in read_csv(R10_ALPHA_TEMPLATE)) else "FAIL",
            "detail": "MTS R10 alpha rows remain nonclaim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_07_join_gates_blocked",
            "result": "PASS" if join_gates_blocked() else "FAIL",
            "detail": "all join gates remain blocked",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_08_runner_smoke_refuses_claim",
            "result": "PASS" if read_csv(RUNNER_SMOKE)[0].get("expected_result") == "blocked_nonclaim" else "FAIL",
            "detail": "runner smoke status refuses a claim",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_09_claim_gates_blocked",
            "result": "PASS" if all_claims_blocked() else "FAIL",
            "detail": "all claim gates refuse promotion",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_10_next_target_written",
            "result": "PASS" if read_csv(NEXT_TARGET)[0]["next_target"].startswith("2244-Y5-R2FR-RAB-no-physical-pole") else "FAIL",
            "detail": "next target row is present",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_11_csv_parse",
            "result": "PASS" if all(parse_csv(path) for path in generated_paths) else "FAIL",
            "detail": "all generated 2243 CSVs parse cleanly",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_12_claim_flags_false",
            "result": "PASS" if generated_flags_false(generated_paths) else "FAIL",
            "detail": "all generated prediction/claim flags remain false",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_13_branch_copies",
            "result": "PASS" if all(row["copied"] == "True" and row["parse_ok"] == "True" for row in read_csv(BRANCH_COPIES)) else "FAIL",
            "detail": "branch/quarantine nonclaim copies written",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_14_pycache_absent",
            "result": "PASS" if not (ROOT / "scripts" / "__pycache__").exists() else "FAIL",
            "detail": "scripts __pycache__ absent after run",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_15_formalization_no_2243",
            "result": "PASS" if formalization_2243_artifacts_absent() else "FAIL",
            "detail": "formalization-workbench has no non-venv 2243 artifacts",
        },
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_16_formalization_untouched",
            "result": "PASS" if formalization_untouched_since_start() else "FAIL",
            "detail": "formalization-workbench untouched during 2243 run",
        },
    ]
    rows.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL2243_OVERALL",
            "result": "PASS" if all(row["result"] == "PASS" for row in rows) else "FAIL",
            "detail": "2243 specializes the parent finite-X/beta contract to R_AB, refuses a finite parent row claim, keeps the c_g-squared/product law, and selects no-physical-pole vs bounded-beta next",
        }
    )
    return rows


def md_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = [str(row.get(column, "")).replace("\n", " ").replace("|", "\\|") for column in columns]
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def build_doc(
    source: list[dict[str, Any]],
    parent_audit: list[dict[str, Any]],
    beta: list[dict[str, Any]],
    branches: list[dict[str, Any]],
    parent_template: list[dict[str, Any]],
    r10_template: list[dict[str, Any]],
    join: list[dict[str, Any]],
    runner: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    claim: list[dict[str, Any]],
    decision: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> str:
    return "\n\n".join(
        [
            "# 2243 - Y5/R2FR R_AB Parent Finite Quadratic Row and Source/Test Beta Split",
            "## Verdict\n"
            "- 2243 specializes the existing finite-`X` source/test grammar to the local `R_AB` residual channel selected by 2242.\n"
            "- The parent finite-`R_AB` action row is not owned by the current corpus: `E_R|0=0`, `Z_R`, `M_R^2/lambda_R`, `J_R`, `beta_source`, `beta_test`, sign, projector, profile, and tail envelope are not supplied together by one parent branch.\n"
            "- The coupling law is now disciplined: a finite two-body exchange needs `beta_source beta_test`; a universal Weyl leg gives a `c_g^2` law unless the source leg is explicitly inside `Qbar`.\n"
            "- The least-scrutiny path remains structural: prove no physical local `R_AB` pole in the GR/Newton branch. If that fails, the fallback is bounded beta rows, not a claimed GR pass.\n"
            "- No finite R10/PPN/local-GR/Newton claim is made, and no `formalization-workbench` or GitHub action is taken.",
            "## Source Register\n"
            + md_table(source, ["source_id", "source_path", "path_exists", "validation_overall_pass", "role"]),
            "## Parent R_AB Action Audit\n"
            + md_table(parent_audit, ["audit_id", "required_parent_object", "candidate_formula", "result", "if_missing"]),
            "## Beta Source/Test Derivation\n"
            + md_table(beta, ["derivation_id", "premise", "result", "status", "missing_for_claim"]),
            "## Branch Classification\n"
            + md_table(branches, ["branch_case_id", "branch", "required_parent_signature", "R10_alpha_form", "current_status", "next_action"]),
            "## Parent Action Row Template\n"
            + md_table(parent_template, ["row_id", "branch", "action_density", "Z_R", "M_R2", "lambda_R", "J_R", "beta_source", "beta_test", "current_status"]),
            "## R10 Alpha Template Update\n"
            + md_table(r10_template, ["model_id", "template_branch", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status"]),
            "## Join Gates\n"
            + md_table(join, ["gate_id", "object", "required_for_claim", "current_status", "ready"]),
            "## Runner Smoke Status\n"
            + md_table(runner, ["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result"]),
            "## Placeholder Refusal Runner\n"
            + md_table(refusal, ["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed"]),
            "## Claim Gates\n"
            + md_table(claim, ["gate_id", "claim", "gate_pass", "reason", "claim_allowed"]),
            "## Decision Ledger\n"
            + md_table(decision, ["decision_id", "decision", "because", "next_action"]),
            "## Next Target\n"
            + md_table(next_target, ["next_target", "script", "objective", "include", "exclude"]),
            "## Branch Copies\n"
            + md_table(copies, ["copy_id", "source_path", "target_path", "copied", "parse_ok"]),
            "## Validation\n"
            + md_table(validation, ["check_id", "result", "detail"]),
            "## Working Interpretation\n\n"
            "This is one of those boring-but-decisive theory moments. The finite branch is not dead, but it has now been forced to wear an ID badge: either it is not a physical pole, or it must provide a real parent quadratic row and source/test charges. "
            "That is exactly the fork we wanted, because it turns the coupling problem from vibes into a theorem-or-bounds problem.",
            "",
        ]
    )


def main() -> None:
    source = source_rows()
    parent_audit = parent_audit_rows()
    beta = beta_rows()
    branches = branch_rows()
    parent_template = parent_template_rows()
    r10_template = r10_alpha_rows()
    join = join_dicts()
    runner = runner_rows()
    refusal = refusal_rows()
    claim = claim_dicts()
    decision = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, source)
    write_csv(PARENT_RAB_ACTION_AUDIT, parent_audit)
    write_csv(BETA_SOURCE_TEST_DERIVATION, beta)
    write_csv(BRANCH_CLASSIFICATION, branches)
    write_csv(PARENT_ACTION_ROW_TEMPLATE, parent_template)
    write_csv(R10_ALPHA_TEMPLATE, r10_template)
    write_csv(JOIN_GATES, join)
    write_csv(RUNNER_SMOKE, runner)
    write_csv(PLACEHOLDER_REFUSAL, refusal)
    write_csv(CLAIM_GATES, claim)
    write_csv(DECISION, decision)
    write_csv(NEXT_TARGET, next_target)
    copies = copy_rows()
    write_csv(BRANCH_COPIES, copies)

    remove_pycache()
    generated_before_validation = [path for path in GENERATED if path != VALIDATION]
    validation = validation_rows(generated_before_validation)
    write_csv(VALIDATION, validation)
    remove_pycache()

    DOC.write_text(
        build_doc(
            source,
            parent_audit,
            beta,
            branches,
            parent_template,
            r10_template,
            join,
            runner,
            refusal,
            claim,
            decision,
            next_target,
            copies,
            validation,
        ),
        encoding="utf-8",
    )

    if not validation_pass(VALIDATION):
        raise SystemExit(f"2243 validation failed: {VALIDATION}")


if __name__ == "__main__":
    main()
