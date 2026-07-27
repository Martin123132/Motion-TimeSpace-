from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
OUT = ROOT / "source-intake" / "mts_residuals"
QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
MICROSCOPE = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
BETA_DOCS = ROOT / "source-intake" / "beta-source" / "docs"

BRANCH_ID = "MTS_R2FR_PARENT_FINITE_Q_QUADRATIC_BETA_SPLIT_2291"
START_TS = datetime.now(timezone.utc).timestamp()
DOC = ROOT / "2291-Y5-R2FR-parent-finite-quadratic-row-and-source-test-beta-split.md"


SOURCES: list[dict[str, Any]] = [
    {
        "source_id": "SRC2291_00_2290_doc",
        "source_key": "2290_handoff",
        "source_path": ROOT / "2290-Y5-R2FR-first-internal-Zq-or-tauR10-projection-row.md",
        "needles": ["NEXT_2291_PARENT_FINITE_QUADRATIC_ROW_AND_SOURCE_TEST_BETA_SPLIT", "source/test product law", "finite quadratic q-row"],
        "role": "current handoff selecting finite q quadratic row and source/test beta split",
    },
    {
        "source_id": "SRC2291_01_2290_validation",
        "source_key": "2290_validation",
        "source_path": OUT / "P8_Y5_BRR545_2290_VALIDATION.csv",
        "needles": ["VAL2290_OVERALL", "PASS"],
        "role": "confirms 2290 passed before 2291",
    },
    {
        "source_id": "SRC2291_02_2290_kernel",
        "source_key": "2290_kernel_contract",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2290_SOURCE_TEST_KERNEL_CONTRACT.csv",
        "needles": ["KERN2290_3_source_test_product", "KERN2290_4_universal_weyl_warning", "CG_SQUARED_WARNING"],
        "role": "current source/test product law and c_g squared warning",
    },
    {
        "source_id": "SRC2291_03_2290_join",
        "source_key": "2290_join_readiness",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2290_INTERNAL_JOIN_READINESS.csv",
        "needles": ["JOIN2290_4_beta_source", "JOIN2290_7_tau_R10", "JOIN2290_8_alpha_predicted"],
        "role": "current blocked join factors",
    },
    {
        "source_id": "SRC2291_04_2243_doc",
        "source_key": "2243_prior_finite_row",
        "source_path": ROOT / "2243-Y5-R2FR-RAB-parent-finite-quadratic-row-and-source-test-beta-split.md",
        "needles": ["parent finite-`R_AB` action row is not owned", "beta_source beta_test", "2244-Y5-R2FR"],
        "role": "prior same-fork finite RAB row/beta split checkpoint",
    },
    {
        "source_id": "SRC2291_05_2243_validation",
        "source_key": "2243_validation",
        "source_path": OUT / "P8_Y5_BRR545_2243_VALIDATION.csv",
        "needles": ["VAL2243_OVERALL", "PASS"],
        "role": "confirms 2243 passed as nonclaim",
    },
    {
        "source_id": "SRC2291_06_2243_parent_audit",
        "source_key": "2243_parent_audit",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2243_PARENT_RAB_ACTION_AUDIT.csv",
        "needles": ["PRAB2243_0_branch_extremum", "PRAB2243_6_verdict", "FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED"],
        "role": "prior parent finite-RAB row audit",
    },
    {
        "source_id": "SRC2291_07_2243_beta",
        "source_key": "2243_beta_split",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2243_BETA_SOURCE_TEST_DERIVATION.csv",
        "needles": ["BETA2243_1_two_body_exchange", "BETA2243_3_common_Weyl_cg", "CG_SQUARED_UNLESS_SOURCE_LEG_PACKED"],
        "role": "prior beta source/test derivation specialized to R_AB",
    },
    {
        "source_id": "SRC2291_08_2243_branch",
        "source_key": "2243_branch_classification",
        "source_path": OUT / "P8_Y5_PARENT_QLOC_2243_BRANCH_CLASSIFICATION.csv",
        "needles": ["BR2243_0_no_physical_RAB_pole", "BR2243_2_sourced_finite_exchange", "SCOREABLE_STRUCTURE_BUT_INPUTS_MISSING"],
        "role": "prior branch classification",
    },
    {
        "source_id": "SRC2291_09_1036_parent",
        "source_key": "1036_parent_X_audit",
        "source_path": OUT / "P8_Y5_R10_1036_PARENT_X_ACTION_AUDIT.csv",
        "needles": ["PX1036_0_branch_extremum", "PX1036_6_verdict", "FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED"],
        "role": "generic finite-X parent action audit",
    },
    {
        "source_id": "SRC2291_10_1036_beta",
        "source_key": "1036_beta_derivation",
        "source_path": OUT / "P8_Y5_R10_1036_BETA_SOURCE_TEST_DERIVATION.csv",
        "needles": ["BETA1036_1_two_body_exchange", "BETA1036_3_common_Weyl_cg", "CG_SQUARED_UNLESS_SOURCE_LEG_PACKED"],
        "role": "generic beta source/test derivation",
    },
    {
        "source_id": "SRC2291_11_1036_branch",
        "source_key": "1036_branch_classification",
        "source_path": OUT / "P8_Y5_R10_1036_BRANCH_CLASSIFICATION.csv",
        "needles": ["BR1036_0_no_physical_X_pole", "BR1036_2_sourced_finite_exchange", "RETAINED_TAIL_BRANCH"],
        "role": "generic finite-X branch classification",
    },
    {
        "source_id": "SRC2291_12_1036_validation",
        "source_key": "1036_validation",
        "source_path": OUT / "P8_Y5_BRR545_1036_VALIDATION.csv",
        "needles": ["V1036_SUMMARY", "pass"],
        "role": "confirms 1036 finite-X/beta checkpoint passed",
    },
    {
        "source_id": "SRC2291_13_1025_hessian",
        "source_key": "1025_hessian",
        "source_path": ROOT / "1025-Y5-R10-parent-Hessian-ZX-MX2-range-or-alpha-source-row.md",
        "needles": ["Z_X", "M_X", "valid_for_claim"],
        "role": "older Hessian/range obstruction evidence",
    },
    {
        "source_id": "SRC2291_14_1027_source_zero",
        "source_key": "1027_source_zero",
        "source_path": ROOT / "1027-Y5-R10-qbarXT-source-zero-or-bounded-coupling-row.md",
        "needles": ["qbar", "source", "valid_for_claim"],
        "role": "older source-zero/bounded-coupling obstruction evidence",
    },
]


OUTPUTS = {
    "source_register": OUT / "P8_Y5_PARENT_QLOC_2291_SOURCE_REGISTER.csv",
    "parent_q_audit": OUT / "P8_Y5_PARENT_QLOC_2291_PARENT_Q_ACTION_AUDIT.csv",
    "beta_derivation": OUT / "P8_Y5_PARENT_QLOC_2291_BETA_SOURCE_TEST_DERIVATION.csv",
    "branch_classification": OUT / "P8_Y5_PARENT_QLOC_2291_BRANCH_CLASSIFICATION.csv",
    "parent_action_template": OUT / "P8_Y5_PARENT_QLOC_2291_PARENT_ACTION_ROW_TEMPLATE.csv",
    "r10_alpha_template": OUT / "R10_alpha_lambda_curve_MTS_2291_PARENT_Q_BETA_TEMPLATE_NONCLAIM.csv",
    "join_gates": OUT / "P8_Y5_PARENT_QLOC_2291_JOIN_GATES.csv",
    "runner_smoke": OUT / "P8_Y5_PARENT_QLOC_2291_RUNNER_SMOKE_STATUS.csv",
    "refusal": OUT / "P8_Y5_PARENT_QLOC_2291_PLACEHOLDER_REFUSAL_RUNNER.csv",
    "claim_gates": OUT / "P8_Y5_PARENT_QLOC_2291_CLAIM_GATES.csv",
    "decision": OUT / "P8_Y5_PARENT_QLOC_2291_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_PARENT_QLOC_2291_NEXT_TARGET.csv",
    "branch_copies": OUT / "P8_Y5_PARENT_QLOC_2291_BRANCH_COPIES.csv",
    "validation": OUT / "P8_Y5_BRR545_2291_VALIDATION.csv",
}


COPY_TARGETS = {
    "queue": (OUTPUTS["parent_action_template"], QUEUE / "JR2291_PARENT_FINITE_Q_ROW_TEMPLATE_NONCLAIM.csv"),
    "branch_wep": (OUTPUTS["parent_action_template"], MICROSCOPE / "parent_finite_q_beta_split_nonclaim_2291.csv"),
    "beta_docs": (OUTPUTS["parent_action_template"], BETA_DOCS / "PARENT_FINITE_Q_BETA_SPLIT_2291_NONCLAIM.csv"),
}


def stringify(value: Any) -> str:
    if isinstance(value, bool):
        return "True" if value else "False"
    return str(value)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        for row in rows:
            writer.writerow({key: stringify(value) for key, value in row.items()})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def csv_parses(path: Path) -> bool:
    try:
        read_csv(path)
        return True
    except Exception:
        return False


def validation_pass(path: Path) -> bool:
    if not path.exists() or not csv_parses(path):
        return False
    rows = read_csv(path)
    if not rows:
        return False
    id_key = "check_id" if "check_id" in rows[0] else "validation_id"
    result_key = "result" if "result" in rows[0] else "status"
    overall_rows = [row for row in rows if "overall" in row.get(id_key, "").lower() or "summary" in row.get(id_key, "").lower()]
    if overall_rows:
        return all(row.get(result_key, "").lower() == "pass" for row in overall_rows)
    return all(row.get(result_key, "").lower() == "pass" for row in rows)


def remove_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def ignored_environment_path(path: Path) -> bool:
    ignored_parts = {".venv", ".venv-score", "__pycache__", "site-packages", ".git"}
    return any(part in ignored_parts for part in path.parts)


def formalization_has_2291_artifacts() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*2291*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            return True
    return False


def formalization_touched_since_start() -> bool:
    if not FORMALIZATION.exists():
        return False
    for candidate in FORMALIZATION.rglob("*"):
        if candidate.is_file() and not ignored_environment_path(candidate.relative_to(FORMALIZATION)):
            if candidate.stat().st_mtime >= START_TS:
                return True
    return False


def table(headers: list[str], rows: list[dict[str, Any]]) -> str:
    def cell(value: Any) -> str:
        return stringify(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in SOURCES:
        source_path = Path(source["source_path"])
        source_text = read_text(source_path)
        needles = source["needles"]
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": source_path,
                "exists": source_path.exists(),
                "needles": "; ".join(needles),
                "needles_present": all(needle in source_text for needle in needles),
                "role": source["role"],
                "valid_for_claim": False,
            }
        )
    return rows


def parent_q_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "PQ2291_0_branch_extremum",
            "required_parent_object": "E_q|0=0",
            "candidate_formula": "delta S_parent/delta q evaluated on the local GR/Newton branch",
            "result": "MISSING_PARENT_EULER_ZERO",
            "if_missing": "q=0 is not stationary by theorem; finite residual branch remains live",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PQ2291_1_quadratic_residue",
            "required_parent_object": "Z_q",
            "candidate_formula": "Z_q is the coefficient of the projected local derivative term <D q,D q> in delta^2 S_parent",
            "result": "MISSING_PARENT_KINETIC_RESIDUE",
            "if_missing": "K_q cannot be numeric and ghost/anti-elliptic branches are not excluded by theorem",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PQ2291_2_mass_gap_range",
            "required_parent_object": "M_q^2 and lambda_q",
            "candidate_formula": "lambda_q=sqrt(Z_q/M_q^2) with M_q^2 from the same parent Hessian normalization",
            "result": "RELATION_DERIVED_VALUES_MISSING",
            "if_missing": "finite-range prediction is closure-only, not a parent prediction",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PQ2291_3_source_current",
            "required_parent_object": "J_q",
            "candidate_formula": "J_q=-delta_q S_matter plus hidden/source/domain currents, projected into the q slot",
            "result": "MISSING_SOURCE_ZERO_OR_SOURCE_LAW",
            "if_missing": "ordinary matter may source a finite local q mode; R10/PPN/clock/orbital rows stay active",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PQ2291_4_source_test_betas",
            "required_parent_object": "beta_source and beta_test",
            "candidate_formula": "beta_i is the parent-normalized derivative of each body's effective source/readout mass with respect to the finite q channel",
            "result": "MISSING_BETA_SOURCE_TEST_SPLIT",
            "if_missing": "alpha(lambda) cannot be scored and c_g cannot be treated as a single linear coefficient",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PQ2291_5_no_pole_alternative",
            "required_parent_object": "physical q pole absent",
            "candidate_formula": "q is quotient/gauge/constraint-only before local inversion; no propagating Green kernel exists",
            "result": "NO_POLE_ROUTE_NOT_SIGNED",
            "if_missing": "retain the finite pole template and bound it",
            "valid_for_claim": False,
        },
        {
            "audit_id": "PQ2291_6_verdict",
            "required_parent_object": "single parent finite-q row",
            "candidate_formula": "parent_signed(E_q=0, Z_q>0, M_q^2>0, J_q/beta law, boundary/tails)",
            "result": "FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED",
            "if_missing": "demote finite-q R10/local branch to explicit closure/nonclaim template",
            "valid_for_claim": False,
        },
    ]


def beta_derivation_rows() -> list[dict[str, Any]]:
    return [
        {
            "derivation_id": "BETA2291_0_point_body_source",
            "premise": "ordinary body i has effective source/readout mass m_i[q]",
            "result": "beta_i := parent-normalized derivative of ln m_i^eff with respect to the finite q channel; J_q contains beta_i m_i times projected source support",
            "status": "CONDITIONAL_STANDARD_VARIATION",
            "missing_for_claim": "parent-owned q normalization and matter/readout mass functional",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "BETA2291_1_two_body_exchange",
            "premise": "finite scalar/tensor-like q mode has a static Yukawa Green kernel",
            "result": "delta V_q(r)=-s_q beta_s beta_t m_s m_t exp(-r/lambda_q)/(4*pi Z_q r) after projection to the measured channel",
            "status": "CONDITIONAL_EXCHANGE_LAW",
            "missing_for_claim": "sign s_q, Z_q, lambda_q, source/test beta rows, tensor projector, and profile projection",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "BETA2291_2_R10_alpha_match",
            "premise": "R10 compares to V=V_N[1+alpha exp(-r/lambda)]",
            "result": "alpha_q=s_q beta_s beta_t/(4*pi G_N Z_q) in nonabsorbed beta units, then multiplied by source/test profile and R10 harmonic projection",
            "status": "CONDITIONAL_NORMALIZATION_SPLIT",
            "missing_for_claim": "which beta convention the parent action uses and whether tensor projection changes scalar Yukawa normalization",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "BETA2291_3_common_Weyl_cg",
            "premise": "m_i^eff=A_g(q)m_i and A_g is universal",
            "result": "alpha_q is proportional to c_g^2 for universal source and test legs unless the source leg is explicitly packed into Qbar",
            "status": "CG_SQUARED_UNLESS_SOURCE_LEG_PACKED",
            "missing_for_claim": "parent-signed A_g branch, q channel normalization, and source/test profile factors",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "BETA2291_4_quotient_zero",
            "premise": "S_matter and constants descend through public quotient and q is vertical/constraint-only",
            "result": "beta_s=beta_t=0 and alpha_q=0 only if descent/no-shadow/no-marker/no-tail clauses are parent-signed together",
            "status": "CONDITIONAL_ZERO_NOT_SIGNED",
            "missing_for_claim": "parent q-kernel, matter functor, no-shadow frame, no-marker constants, and hidden-tail silence",
            "valid_for_claim": False,
        },
        {
            "derivation_id": "BETA2291_5_verdict",
            "premise": "current corpus only",
            "result": "beta law is derived as a contract, but no numeric or zero beta source/test row is claim-ready",
            "status": "BETA_ROWS_UNOWNED",
            "missing_for_claim": "parent action schema or sourced beta bounds",
            "valid_for_claim": False,
        },
    ]


def branch_classification_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_case_id": "BR2291_0_no_physical_q_pole",
            "branch": "quotient/gauge/constraint q",
            "required_parent_signature": "q absent from physical quotient or first-class/constraint-only with no invertible local Green kernel",
            "R10_alpha_form": "alpha_q=0 or not_applicable",
            "current_status": "BEST_LOCAL_GR_ROUTE_BUT_UNSIGNED",
            "next_action": "try no-physical-q-pole theorem before accepting finite residual branch",
            "valid_for_claim": False,
        },
        {
            "branch_case_id": "BR2291_1_sourcefree_massive_nohair",
            "branch": "massive finite q with no local source",
            "required_parent_signature": "Z_q>0, M_q^2>0, J_q=0, boundary_flux_q=0 from one parent branch",
            "R10_alpha_form": "alpha_q=0 in local exterior by energy identity",
            "current_status": "CONDITIONAL_NOHAIR_UNSIGNED",
            "next_action": "revive only if source-zero and boundary flux close together",
            "valid_for_claim": False,
        },
        {
            "branch_case_id": "BR2291_2_sourced_finite_exchange",
            "branch": "physical finite q exchange",
            "required_parent_signature": "Z_q, lambda_q, beta_source, beta_test, profile, sign, tensor projector, and tail envelope",
            "R10_alpha_form": "alpha_q=K_q^R10(lambda) beta_source beta_test + epsilon_tail",
            "current_status": "SCOREABLE_STRUCTURE_BUT_INPUTS_MISSING",
            "next_action": "if no-pole fails, build bounded beta_source/beta_test rows without cancellation",
            "valid_for_claim": False,
        },
        {
            "branch_case_id": "BR2291_3_shadow_frame_marker",
            "branch": "Weyl/disformal/marker leakage",
            "required_parent_signature": "A_g'(0), B_g'(0), marker coefficients, non-Hilbert source, and support shifts are theorem-zero or bounded",
            "R10_alpha_form": "sum of absolute source/test leakage channels, not a single clean scalar alpha",
            "current_status": "RETAINED_TAIL_BRANCH",
            "next_action": "route into no-cancellation tail envelope and cross-check WEP/clock/PPN",
            "valid_for_claim": False,
        },
    ]


def parent_action_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "PQA2291_0_finite_q_parent_row",
            "branch": "physical_finite_q_exchange",
            "action_density": "sqrt(-g)[-1/2 Z_q <D q,D q> -1/2 M_q^2 q^2 + q J_q] plus declared boundary/tail terms",
            "Z_q": "MISSING_PARENT_KINETIC_RESIDUE",
            "M_q2": "MISSING_PARENT_MASS_GAP",
            "lambda_q": "MISSING_PARENT_RANGE",
            "J_q": "MISSING_SOURCE_CURRENT_OR_ZERO_THEOREM",
            "beta_source": "MISSING_BETA_SOURCE",
            "beta_test": "MISSING_BETA_TEST",
            "current_status": "TEMPLATE_ONLY_PARENT_ROW_NOT_OWNED",
            "valid_for_claim": False,
        },
        {
            "row_id": "PQA2291_1_no_pole_parent_row",
            "branch": "no_physical_q_pole",
            "action_density": "q is absent, pure quotient/gauge, or algebraic constraint with no propagating local pole",
            "Z_q": "not_applicable_if_no_pole_signed",
            "M_q2": "not_applicable_if_no_pole_signed",
            "lambda_q": "not_applicable_if_no_pole_signed",
            "J_q": "zero_or_constraint_current_only_if_parent_signed",
            "beta_source": "0_if_matter_descends_and_no_shadow_signed",
            "beta_test": "0_if_matter_descends_and_no_shadow_signed",
            "current_status": "BEST_THEOREM_ROUTE_UNSIGNED",
            "valid_for_claim": False,
        },
    ]


def r10_alpha_template_rows() -> list[dict[str, Any]]:
    return [
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "template_branch": "parent_q_beta_product_template",
            "lambda_value": "MISSING_PARENT_LAMBDA_Q",
            "alpha_predicted": "MISSING_KQ_BETA_SOURCE_BETA_TEST_TAIL_ENVELOPE",
            "force_law_form": "alpha_q(lambda)=K_q^R10(lambda) beta_source(lambda) beta_test(lambda)+epsilon_tail(lambda)",
            "derivation_status": "template_invalid_missing_parent_action_row_and_beta_split",
            "valid_for_claim": False,
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "template_branch": "universal_weyl_cg_squared_template",
            "lambda_value": "MISSING_PARENT_LAMBDA_Q",
            "alpha_predicted": "MISSING_NUMERIC_KQ_TIMES_CG_SQUARED_AND_PROFILE",
            "force_law_form": "universal Weyl finite exchange: alpha_q proportional to K_q^R10 c_g^2",
            "derivation_status": "template_invalid_missing_parent_cg_Zq_lambda_and_profile",
            "valid_for_claim": False,
        },
        {
            "model_id": "MTS_source_normalized_Newton_branch",
            "template_branch": "no_physical_q_pole_template",
            "lambda_value": "ALL_LOCAL_R10_RANGE",
            "alpha_predicted": "MISSING_NO_PHYSICAL_Q_POLE_THEOREM",
            "force_law_form": "no finite Yukawa alpha if q has no physical pole and hidden tails are zero/bounded",
            "derivation_status": "template_invalid_missing_no_pole_parent_action_signature",
            "valid_for_claim": False,
        },
    ]


def join_gate_rows() -> list[dict[str, Any]]:
    entries = [
        ("JOIN2291_0_parent_row", "parent finite-q row", "E_q=0, Z_q, M_q^2, lambda_q, J_q/beta law, sign, boundary/tails from one parent branch", "MISSING_PARENT_ROW"),
        ("JOIN2291_1_beta_product", "beta_source beta_test", "numeric/source-backed or zero-theorem beta_source and beta_test rows", "MISSING_BETA_SOURCE_TEST_SPLIT"),
        ("JOIN2291_2_cg_law", "c_g versus c_g^2 policy", "explicit declaration whether Qbar already contains the source leg", "LAW_CORRECTED_NO_NUMERIC_INPUTS"),
        ("JOIN2291_3_external_bound", "R10 alpha_bound(lambda)", "promoted digitized/official bound curve", "REVIEW_CANDIDATE_NONCLAIM"),
        ("JOIN2291_4_no_cancellation", "absolute tail envelope", "all hidden/marker/disformal/non-Hilbert/support terms zero or bounded in absolute sum", "MISSING_ABSOLUTE_TAIL_ENVELOPE"),
    ]
    return [
        {
            "gate_id": gate_id,
            "object": obj,
            "required_for_claim": required,
            "current_status": status,
            "ready": False,
            "valid_for_claim": False,
        }
        for gate_id, obj, required, status in entries
    ]


def runner_smoke_rows() -> list[dict[str, Any]]:
    return [
        {
            "smoke_id": "SMOKE2291_0_runner_status",
            "valid_mts_rows": 0,
            "valid_bound_rows": 0,
            "comparison_rows": 1,
            "R10_pass_for_claim": False,
            "claim_allowed": False,
            "expected_result": "blocked_nonclaim",
            "valid_for_claim": False,
        }
    ]


def refusal_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in parent_action_template_rows():
        rows.append(
            {
                "refusal_id": f"REF2291_TEMPLATE_{len(rows)}",
                "object": row["row_id"],
                "current_status": row["current_status"],
                "refusal_status": "rejected_parent_action_template_only",
                "failure_reasons": "MISSING_PARENT_INPUTS;NOT_SCORE_READY;CLAIM_POLICY_FALSE",
                "score_eligible": False,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    for row in join_gate_rows():
        rows.append(
            {
                "refusal_id": f"REF2291_{row['gate_id']}",
                "object": row["object"],
                "current_status": row["current_status"],
                "refusal_status": "rejected_join_gate_not_ready",
                "failure_reasons": f"{row['current_status']};READY_FALSE;CLAIM_POLICY_FALSE",
                "score_eligible": False,
                "claim_allowed": False,
                "valid_for_claim": False,
            }
        )
    return rows


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {"gate_id": "CGATE2291_0_parent_action_row", "claim": "single parent action supplies the finite q row", "gate_pass": False, "reason": "E_q, Z_q, M_q^2/lambda_q, J_q, beta split, projector, and tails are not parent-signed together", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CGATE2291_1_numeric_alpha", "claim": "MTS has numeric alpha_predicted(lambda)", "gate_pass": False, "reason": "K_q, beta_source, beta_test, lambda_q, profile, and promoted bound curve are missing", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CGATE2291_2_linear_cg", "claim": "R10 alpha may be scored as linear in c_g", "gate_pass": False, "reason": "source-test exchange gives c_g squared for universal Weyl legs unless source leg is explicitly included elsewhere", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CGATE2291_3_no_pole", "claim": "no physical q pole is derived", "gate_pass": False, "reason": "no-pole/quotient route remains conditional in current parent evidence", "claim_allowed": False, "valid_for_claim": False},
        {"gate_id": "CGATE2291_4_local_GR_R10", "claim": "local GR/R10 pass is established", "gate_pass": False, "reason": "parent-action row and empirical score inputs remain nonclaim", "claim_allowed": False, "valid_for_claim": False},
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC2291_0_parent_row_status",
            "decision": "The parent finite-q quadratic row is not owned by the current corpus.",
            "because": "the necessary pieces exist only as conditional contracts spread across Hessian/source/marker gates and the 2290 kernel contract",
            "next_action": "keep the finite-q branch as a closure/nonclaim template unless a parent action signs all pieces",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2291_1_coupling_law_status",
            "decision": "The corrected coupling law is beta_source times beta_test.",
            "because": "two-body exchange forbids a single naked coupling coefficient; universal c_g enters twice",
            "next_action": "future R10/PPN templates must require beta_source, beta_test, and a declaration of whether Qbar contains a source leg",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2291_2_best_route",
            "decision": "The least-scrutiny route is still no physical q pole; the fallback is bounded beta rows.",
            "because": "a derived no-pole/constraint branch gives GR reduction cleaner than tuning a short-range finite residual",
            "next_action": "try no-physical-q-pole theorem first, then bounded beta_source/beta_test acquisition",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC2291_3_next_target",
            "decision": "Next target is no physical q pole or bounded beta runner.",
            "because": "this is the fork that decides whether local GR is derived structurally or tested as a finite residual",
            "next_action": "2292-Y5-R2FR-no-physical-q-pole-theorem-or-bounded-beta-runner.md",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_target": "2292-Y5-R2FR-no-physical-q-pole-theorem-or-bounded-beta-runner.md",
            "script": "scripts/Y5_R2FR_no_physical_q_pole_theorem_or_bounded_beta_runner_2292.py",
            "objective": "try to prove the finite local q/R_AB mode has no physical pole in the GR/Newton branch; if not, build bounded beta_source/beta_test acquisition rows with no-cancellation tails",
            "include": "quotient/gauge/constraint pole audit, Hessian degeneracy or first-class certificate, algebraic constraint alternative, beta_source/beta_test row schema, c_g^2 convention, R10/PPN/clock/WEP routing",
            "exclude": "asserted alpha=0, invented beta/c_g values, linear-c_g R10 score, cancellation between unknown tails, R10 pass claim, formalization-workbench edits, GitHub action",
            "valid_for_claim": False,
        }
    ]


def generated_claim_flags_false(paths: list[Path]) -> bool:
    false_values = {"", "false", "0", "no", "none", "null"}
    guarded_keys = {
        "score_ready",
        "valid_prediction_row",
        "valid_for_claim",
        "claim_allowed",
        "ready",
        "R10_pass_for_claim",
        "score_eligible",
    }
    for path in paths:
        for row in read_csv(path):
            for key, value in row.items():
                if key in guarded_keys and value.strip().lower() not in false_values:
                    return False
    return True


def templates_have_missing(rows: list[dict[str, Any]]) -> bool:
    return all("MISSING" in " ".join(str(value) for value in row.values()) or "not_applicable_if_no_pole_signed" in " ".join(str(value) for value in row.values()) for row in rows)


def copy_branch_files() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for copy_id, (source_path, target_path) in COPY_TARGETS.items():
        target_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source_path, target_path)
        rows.append(
            {
                "copy_id": copy_id,
                "source_path": source_path,
                "target_path": target_path,
                "target_exists": target_path.exists(),
                "target_parses": csv_parses(target_path),
                "reason": "branch copy for 2291 parent finite-q beta split checkpoint",
            }
        )
    return rows


def validation_rows(all_generated_before_validation: list[Path], branch_copy_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source_rows = read_csv(OUTPUTS["source_register"])
    parent_rows = read_csv(OUTPUTS["parent_q_audit"])
    beta_rows = read_csv(OUTPUTS["beta_derivation"])
    branch_rows = read_csv(OUTPUTS["branch_classification"])
    template_rows = read_csv(OUTPUTS["parent_action_template"])
    alpha_rows = read_csv(OUTPUTS["r10_alpha_template"])
    join_rows = read_csv(OUTPUTS["join_gates"])
    runner_rows = read_csv(OUTPUTS["runner_smoke"])
    refusal_rows_local = read_csv(OUTPUTS["refusal"])
    claim_rows = read_csv(OUTPUTS["claim_gates"])
    decision_rows_local = read_csv(OUTPUTS["decision"])
    next_rows = read_csv(OUTPUTS["next_target"])

    checks = [
        ("VAL2291_0_sources_exist", all(row["exists"] == "True" for row in source_rows), "all cited source paths exist"),
        ("VAL2291_1_needles_present", all(row["needles_present"] == "True" for row in source_rows), "all cited source needles are present"),
        (
            "VAL2291_2_prior_validations",
            validation_pass(OUT / "P8_Y5_BRR545_2290_VALIDATION.csv")
            and validation_pass(OUT / "P8_Y5_BRR545_2243_VALIDATION.csv")
            and validation_pass(OUT / "P8_Y5_BRR545_1036_VALIDATION.csv"),
            "2290, 2243, and 1036 validations pass overall",
        ),
        (
            "VAL2291_3_parent_action_audit_complete",
            any(row["audit_id"] == "PQ2291_6_verdict" and row["result"] == "FAIL_CURRENT_CLAIM_PARENT_ROW_NOT_OWNED" for row in parent_rows),
            "parent finite q row audit reaches non-owned verdict",
        ),
        (
            "VAL2291_4_beta_product_law",
            any(row["status"] == "CG_SQUARED_UNLESS_SOURCE_LEG_PACKED" for row in beta_rows)
            and any(row["status"] == "CONDITIONAL_EXCHANGE_LAW" for row in beta_rows),
            "beta source/test product and c_g-squared law are explicit",
        ),
        (
            "VAL2291_5_branch_fork_complete",
            {"BR2291_0_no_physical_q_pole", "BR2291_1_sourcefree_massive_nohair", "BR2291_2_sourced_finite_exchange", "BR2291_3_shadow_frame_marker"}.issubset(
                {row["branch_case_id"] for row in branch_rows}
            ),
            "branch classification covers no-pole, nohair, finite exchange, and tail branches",
        ),
        (
            "VAL2291_6_parent_templates_nonclaim",
            templates_have_missing(template_rows) and all(row["valid_for_claim"] == "False" for row in template_rows),
            "parent action templates are nonclaim and unscoreable",
        ),
        (
            "VAL2291_7_mts_template_nonclaim",
            templates_have_missing(alpha_rows) and all(row["valid_for_claim"] == "False" for row in alpha_rows),
            "MTS R10 alpha rows remain nonclaim",
        ),
        (
            "VAL2291_8_join_gates_blocked",
            all(row["ready"] == "False" and row["valid_for_claim"] == "False" for row in join_rows),
            "all join gates remain blocked",
        ),
        (
            "VAL2291_9_runner_smoke_refuses_claim",
            any(row["expected_result"] == "blocked_nonclaim" and row["claim_allowed"] == "False" for row in runner_rows),
            "runner smoke status refuses a claim",
        ),
        (
            "VAL2291_10_refusal_runner",
            len(refusal_rows_local) >= 7 and all(row["claim_allowed"] == "False" and row["valid_for_claim"] == "False" for row in refusal_rows_local),
            "placeholder refusal runner blocks templates and join gates",
        ),
        (
            "VAL2291_11_claim_gates_blocked",
            all(row["gate_pass"] == "False" and row["claim_allowed"] == "False" for row in claim_rows),
            "all claim gates refuse promotion",
        ),
        (
            "VAL2291_12_decision_next",
            any(row["decision_id"] == "DEC2291_3_next_target" for row in decision_rows_local)
            and any(row["next_target"] == "2292-Y5-R2FR-no-physical-q-pole-theorem-or-bounded-beta-runner.md" for row in next_rows),
            "decision selects no physical q pole or bounded beta runner next",
        ),
        ("VAL2291_13_csv_parse", all(csv_parses(path) for path in all_generated_before_validation), "all generated 2291 CSVs parse cleanly"),
        ("VAL2291_14_no_claim_flags", generated_claim_flags_false(all_generated_before_validation), "all generated prediction/claim flags remain false"),
        ("VAL2291_15_branch_copies", all(row["target_exists"] and row["target_parses"] for row in branch_copy_rows), "branch/queue copies exist and parse"),
        ("VAL2291_16_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent after run"),
        ("VAL2291_17_formalization_no_2291", not formalization_has_2291_artifacts(), "formalization-workbench has no non-venv 2291 artifacts"),
        ("VAL2291_18_formalization_untouched", not formalization_touched_since_start(), "formalization-workbench untouched during 2291 run"),
    ]
    rows = [{"check_id": check_id, "result": "PASS" if passed else "FAIL", "detail": detail} for check_id, passed, detail in checks]
    overall_pass = all(row["result"] == "PASS" for row in rows)
    rows.append(
        {
            "check_id": "VAL2291_OVERALL",
            "result": "PASS" if overall_pass else "FAIL",
            "detail": "2291 specializes the finite-X/beta contract to q, refuses finite parent row claim, preserves c_g-squared/product law, and selects no-physical-pole vs bounded-beta next",
        }
    )
    return rows


def write_markdown(
    sources: list[dict[str, Any]],
    parent_audit: list[dict[str, Any]],
    beta_derivation: list[dict[str, Any]],
    branch_classification: list[dict[str, Any]],
    parent_template: list[dict[str, Any]],
    alpha_template: list[dict[str, Any]],
    join_gates: list[dict[str, Any]],
    runner_smoke: list[dict[str, Any]],
    refusal: list[dict[str, Any]],
    claim_gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
    branch_copies: list[dict[str, Any]],
    validation: list[dict[str, Any]],
) -> None:
    content = f"""# 2291 - Y5/R2FR Parent Finite Quadratic Row and Source/Test Beta Split

## Verdict

2291 specializes the finite-`X` source/test grammar to the current local `q=R_AB` residual channel.

The parent finite-`q` action row is still not owned by the current corpus: `E_q|0=0`, `Z_q`, `M_q^2/lambda_q`, `J_q`, `beta_source`, `beta_test`, sign, projector, profile, and tail envelope are not supplied together by one parent branch.

But the coupling law is now disciplined. A finite two-body exchange needs `beta_source beta_test`; a universal Weyl leg gives a `c_g^2` law unless the source leg is explicitly inside `Qbar`. The least-scrutiny route remains structural: prove no physical local `q/R_AB` pole in the GR/Newton branch. If that fails, the fallback is bounded beta rows, not a claimed GR pass.

## Source Register
{table(["source_id", "source_key", "source_path", "exists", "needles_present", "role", "valid_for_claim"], sources)}

## Parent q Action Audit
{table(["audit_id", "required_parent_object", "candidate_formula", "result", "if_missing", "valid_for_claim"], parent_audit)}

## Beta Source/Test Derivation
{table(["derivation_id", "premise", "result", "status", "missing_for_claim", "valid_for_claim"], beta_derivation)}

## Branch Classification
{table(["branch_case_id", "branch", "required_parent_signature", "R10_alpha_form", "current_status", "next_action", "valid_for_claim"], branch_classification)}

## Parent Action Row Template
{table(["row_id", "branch", "action_density", "Z_q", "M_q2", "lambda_q", "J_q", "beta_source", "beta_test", "current_status", "valid_for_claim"], parent_template)}

## R10 Alpha Template Update
{table(["model_id", "template_branch", "lambda_value", "alpha_predicted", "force_law_form", "derivation_status", "valid_for_claim"], alpha_template)}

## Join Gates
{table(["gate_id", "object", "required_for_claim", "current_status", "ready", "valid_for_claim"], join_gates)}

## Runner Smoke Status
{table(["smoke_id", "valid_mts_rows", "valid_bound_rows", "comparison_rows", "R10_pass_for_claim", "claim_allowed", "expected_result", "valid_for_claim"], runner_smoke)}

## Placeholder Refusal Runner
{table(["refusal_id", "object", "current_status", "refusal_status", "failure_reasons", "score_eligible", "claim_allowed", "valid_for_claim"], refusal)}

## Claim Gates
{table(["gate_id", "claim", "gate_pass", "reason", "claim_allowed", "valid_for_claim"], claim_gates)}

## Decision Ledger
{table(["decision_id", "decision", "because", "next_action", "valid_for_claim"], decisions)}

## Next Target
{table(["next_target", "script", "objective", "include", "exclude", "valid_for_claim"], next_target)}

## Branch Copies
{table(["copy_id", "source_path", "target_path", "target_exists", "target_parses", "reason"], branch_copies)}

## Validation
{table(["check_id", "result", "detail"], validation)}

## Working Interpretation

This is the right fork. The finite branch now has to either disappear as a physical pole, or put real parent objects on the table. No more misty coupling talk. Either local GR comes from a structural no-pole theorem, or MTS becomes a finite-residual theory with bounded source/test beta rows and no-cancellation tails.
"""
    DOC.write_text(content, encoding="utf-8")


def main() -> None:
    remove_pycache()
    sources = source_register_rows()
    parent_audit = parent_q_audit_rows()
    beta_derivation = beta_derivation_rows()
    branch_classification = branch_classification_rows()
    parent_template = parent_action_template_rows()
    alpha_template = r10_alpha_template_rows()
    join_gates = join_gate_rows()
    runner_smoke = runner_smoke_rows()
    refusal = refusal_rows()
    claim_gates = claim_gate_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["parent_q_audit"], parent_audit)
    write_csv(OUTPUTS["beta_derivation"], beta_derivation)
    write_csv(OUTPUTS["branch_classification"], branch_classification)
    write_csv(OUTPUTS["parent_action_template"], parent_template)
    write_csv(OUTPUTS["r10_alpha_template"], alpha_template)
    write_csv(OUTPUTS["join_gates"], join_gates)
    write_csv(OUTPUTS["runner_smoke"], runner_smoke)
    write_csv(OUTPUTS["refusal"], refusal)
    write_csv(OUTPUTS["claim_gates"], claim_gates)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["next_target"], next_target)

    branch_copies = copy_branch_files()
    write_csv(OUTPUTS["branch_copies"], branch_copies)

    generated_before_validation = [
        OUTPUTS["source_register"],
        OUTPUTS["parent_q_audit"],
        OUTPUTS["beta_derivation"],
        OUTPUTS["branch_classification"],
        OUTPUTS["parent_action_template"],
        OUTPUTS["r10_alpha_template"],
        OUTPUTS["join_gates"],
        OUTPUTS["runner_smoke"],
        OUTPUTS["refusal"],
        OUTPUTS["claim_gates"],
        OUTPUTS["decision"],
        OUTPUTS["next_target"],
        OUTPUTS["branch_copies"],
    ]
    remove_pycache()
    validation = validation_rows(generated_before_validation, branch_copies)
    write_csv(OUTPUTS["validation"], validation)
    write_markdown(
        sources,
        parent_audit,
        beta_derivation,
        branch_classification,
        parent_template,
        alpha_template,
        join_gates,
        runner_smoke,
        refusal,
        claim_gates,
        decisions,
        next_target,
        branch_copies,
        validation,
    )
    remove_pycache()

    failed = [row for row in validation if row["result"] != "PASS"]
    if failed:
        failed_ids = ", ".join(row["check_id"] for row in failed)
        raise SystemExit(f"2291 validation failed: {failed_ids}")
    print(f"Wrote {DOC}")
    print(f"Wrote {OUTPUTS['validation']}")


if __name__ == "__main__":
    main()
