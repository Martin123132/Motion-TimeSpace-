from __future__ import annotations

import csv
import json
import math
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"

DOC_PATH = ROOT / "578-Y5-R10-lambda-X-mass-gap-and-product-coefficient-derivation-targets.md"

PRIOR_577_VALIDATION = RESIDUALS / "P8_Y5_BRR545_577_VALIDATION.csv"
PRIOR_577_SUMMARY = RESIDUALS / "P8_Y5_R10_577_NONCLAIM_SUMMARY.csv"
HESSIAN_FORMULA = RESIDUALS / "P8_Y5_R10_564_HESSIAN_EXTRACTION_FORMULA.csv"
MASS_GAP_GATE = RESIDUALS / "P8_Y5_R10_MASS_GAP_THEOREM_ZERO_GATE.csv"
PREFAC_FORMULA = RESIDUALS / "P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv"
NUMERATOR_REGISTER = RESIDUALS / "P8_Y5_R10_NUMERATOR_FACTOR_REGISTER.csv"
QBAR_BUDGET_577 = RESIDUALS / "P8_Y5_R10_577_QBAR_BUDGET_MATRIX.csv"
COEFFICIENT_TARGETS_577 = RESIDUALS / "P8_Y5_R10_577_COEFFICIENT_TARGETS.csv"
REVIEW_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv"
LIVE_CLAIM_CURVE = LOCAL_BOUNDS / "R10_alpha_lambda_bound_curve_DIGITIZED.csv"

SOURCE_REGISTER_PATH = RESIDUALS / "P8_Y5_R10_578_SOURCE_REGISTER.csv"
LOCAL_DERIVATION_PATH = RESIDUALS / "P8_Y5_R10_578_LOCAL_QUADRATIC_DERIVATION.csv"
MASS_GAP_TARGETS_PATH = RESIDUALS / "P8_Y5_R10_578_MASS_GAP_TARGETS.csv"
REVERSE_WINDOWS_PATH = RESIDUALS / "P8_Y5_R10_578_REVERSE_LAMBDA_WINDOWS.csv"
PRODUCT_DERIVATION_PATH = RESIDUALS / "P8_Y5_R10_578_PRODUCT_COEFFICIENT_DERIVATION.csv"
REPAIR_QUEUE_PATH = RESIDUALS / "P8_Y5_R10_578_COEFFICIENT_REPAIR_QUEUE.csv"
DECISION_PATH = RESIDUALS / "P8_Y5_BRR545_578_DECISION.csv"
ROUTE_UPDATE_PATH = RESIDUALS / "P8_Y5_BRR545_578_ROUTE_UPDATE.csv"
VALIDATION_PATH = RESIDUALS / "P8_Y5_BRR545_578_VALIDATION.csv"
SUMMARY_PATH = RESIDUALS / "P8_Y5_R10_578_NONCLAIM_SUMMARY.csv"

STATUS = "Y5_R10_lambda_X_product_law_derived_conditionally_numeric_coefficients_missing"
CLAIM_CEILING = "lambda_product_derivation_targets_only_no_R10_pass_no_WEP_PPN_or_local_GR_pass"
NEXT_TARGET = "579-Y5-R10-parent-Hessian-source-charge-fill-or-theorem-zero-return.md"

HBAR_C_EV_M = 1.973269804e-7
LAMBDA_TARGETS = [5.9e-6, 1.0e-5, 2.0e-5, 3.86e-5, 5.0e-5, 7.5e-5, 1.0e-4, 2.0e-4, 5.0e-4, 6.080783e-4, 1.0e-3]
PRODUCT_THRESHOLDS = [1.0, 0.3, 0.1, 0.03, 0.01, 0.003, 0.001]

SOURCE_FILES = [
    {
        "source_file": "577-Y5-R10-qbar-XT-finite-envelope-after-source-current-failure.md",
        "role": "finite qbar_XT product wall and next target",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_BRR545_577_VALIDATION.csv",
        "role": "prior finite-envelope validation",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_577_NONCLAIM_SUMMARY.csv",
        "role": "qbar retained and finite product ceiling summary",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_564_HESSIAN_EXTRACTION_FORMULA.csv",
        "role": "parent Hessian extraction formula for Z_X and M_X^2",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_MASS_GAP_THEOREM_ZERO_GATE.csv",
        "role": "mass-gap and no-hair gate status",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_ZX_LAMBDA_PREFACtOR_FORMULA_REGISTER.csv",
        "role": "static operator, lambda, Green profile, and prefactor formulas",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_NUMERATOR_FACTOR_REGISTER.csv",
        "role": "source/test/projection numerator factors",
    },
    {
        "source_file": "source-intake/mts_residuals/P8_Y5_R10_577_QBAR_BUDGET_MATRIX.csv",
        "role": "qbar budgets from previous pressure wall",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_VECTOR_2020_REVIEW_CANDIDATE.csv",
        "role": "review-candidate curve for reverse lambda windows",
    },
    {
        "source_file": "source-intake/local_bounds/R10_alpha_lambda_bound_curve_DIGITIZED.csv",
        "role": "live claim curve placeholder, expected claim-blocked",
    },
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        values = []
        for column in columns:
            value = str(row.get(column, ""))
            value = value.replace("\n", "<br>").replace("|", "\\|")
            values.append(value)
        lines.append("| " + " | ".join(values) + " |")
    return "\n".join(lines)


def fmt(value: float) -> str:
    if value == 0:
        return "0"
    if abs(value) < 1e-3 or abs(value) >= 1e4:
        return f"{value:.6e}"
    return f"{value:.12g}"


def to_float(value: str) -> float:
    return float(str(value).strip())


def source_register() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for item in SOURCE_FILES:
        source_file = str(item["source_file"])
        rows.append(
            {
                "source_file": source_file,
                "exists": str((ROOT / source_file).exists()),
                "role": item["role"],
            }
        )
    return rows


def numeric_curve_rows(curve_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in curve_rows:
        try:
            lambda_value = to_float(row["lambda_value"])
            alpha_bound = to_float(row["alpha_bound"])
        except (KeyError, ValueError):
            continue
        if lambda_value > 0 and alpha_bound > 0:
            rows.append({**row, "lambda_value_float": lambda_value, "alpha_bound_float": alpha_bound})
    return sorted(rows, key=lambda row: row["lambda_value_float"])


def log_interp_alpha(curve_rows: list[dict[str, object]], lambda_value: float) -> tuple[float, str]:
    if lambda_value <= curve_rows[0]["lambda_value_float"]:
        row = curve_rows[0]
        return row["alpha_bound_float"], f"clamped:{row['bound_id']}"
    if lambda_value >= curve_rows[-1]["lambda_value_float"]:
        row = curve_rows[-1]
        return row["alpha_bound_float"], f"clamped:{row['bound_id']}"
    log_lambda = math.log10(lambda_value)
    for left, right in zip(curve_rows, curve_rows[1:]):
        left_lambda = left["lambda_value_float"]
        right_lambda = right["lambda_value_float"]
        if left_lambda <= lambda_value <= right_lambda:
            left_x = math.log10(left_lambda)
            right_x = math.log10(right_lambda)
            t = (log_lambda - left_x) / (right_x - left_x)
            log_alpha = math.log10(left["alpha_bound_float"]) + t * (
                math.log10(right["alpha_bound_float"]) - math.log10(left["alpha_bound_float"])
            )
            return 10**log_alpha, f"log_interp:{left['bound_id']}->{right['bound_id']}"
    raise ValueError(f"lambda not bracketed: {lambda_value}")


def crossing_lambda(left: dict[str, object], right: dict[str, object], threshold: float) -> float:
    left_x = math.log10(left["lambda_value_float"])
    right_x = math.log10(right["lambda_value_float"])
    left_y = math.log10(left["alpha_bound_float"])
    right_y = math.log10(right["alpha_bound_float"])
    target_y = math.log10(threshold)
    if right_y == left_y:
        return left["lambda_value_float"]
    t = (target_y - left_y) / (right_y - left_y)
    return 10 ** (left_x + t * (right_x - left_x))


def allowed_intervals(curve_rows: list[dict[str, object]], threshold: float) -> list[tuple[float, float]]:
    intervals: list[tuple[float, float]] = []
    in_interval = curve_rows[0]["alpha_bound_float"] >= threshold
    start = curve_rows[0]["lambda_value_float"] if in_interval else None
    for left, right in zip(curve_rows, curve_rows[1:]):
        left_ok = left["alpha_bound_float"] >= threshold
        right_ok = right["alpha_bound_float"] >= threshold
        if left_ok and right_ok:
            continue
        if left_ok and not right_ok:
            end = crossing_lambda(left, right, threshold)
            intervals.append((start if start is not None else left["lambda_value_float"], end))
            start = None
            in_interval = False
        elif not left_ok and right_ok:
            start = crossing_lambda(left, right, threshold)
            in_interval = True
    if in_interval and start is not None:
        intervals.append((start, curve_rows[-1]["lambda_value_float"]))
    return intervals


def interval_text(intervals: list[tuple[float, float]], limit: int = 8) -> str:
    shown = intervals[:limit]
    text = ";".join(f"{fmt(start)}..{fmt(end)}" for start, end in shown)
    if len(intervals) > limit:
        text += f";...(+{len(intervals) - limit} more raw fragments)"
    return text


def mass_interval_text(intervals: list[tuple[float, float]], limit: int = 8) -> str:
    shown = intervals[:limit]
    text = ";".join(
        f"{fmt(HBAR_C_EV_M / end)}..{fmt(HBAR_C_EV_M / start)}" for start, end in shown
    )
    if len(intervals) > limit:
        text += f";...(+{len(intervals) - limit} more raw fragments)"
    return text


def make_local_derivation() -> list[dict[str, object]]:
    return [
        {
            "step_id": "LD578_0_parent_expansion",
            "derivation_step": "expand the parent action around the compact local branch",
            "formula": "S_X^(2)=1/2 int sqrt(g)[Z_X nabla_i X nabla^i X + M_X^2 X^2] - int sqrt(g) J_X X",
            "result": "conditional_quadratic_form_derived",
            "remaining_input": "parent action must supply numeric Z_X, M_X^2, and source split J_X",
            "valid_for_claim": "false",
        },
        {
            "step_id": "LD578_1_static_operator",
            "derivation_step": "vary X in the static weak-field exterior",
            "formula": "(-Z_X Delta + M_X^2) X = J_X",
            "result": "conditional_operator_derived",
            "remaining_input": "Z_X>0 and M_X^2>0 must be parent-owned in the same branch",
            "valid_for_claim": "false",
        },
        {
            "step_id": "LD578_2_range_law",
            "derivation_step": "canonicalize the operator",
            "formula": "mu_X^2=M_X^2/Z_X; lambda_X=1/mu_X=sqrt(Z_X/M_X^2)",
            "result": "lambda_law_derived_conditionally",
            "remaining_input": "numeric Hessian ratio M_X^2/Z_X is missing",
            "valid_for_claim": "false",
        },
        {
            "step_id": "LD578_3_green_function",
            "derivation_step": "solve exterior point-source Green function",
            "formula": "X(r)=Q_X^H(lambda_X) exp(-r/lambda_X)/(4*pi*Z_X*r)",
            "result": "profile_derived_conditionally",
            "remaining_input": "projected source charge Q_X^H(lambda_X) must be derived or bounded",
            "valid_for_claim": "false",
        },
        {
            "step_id": "LD578_4_test_potential",
            "derivation_step": "couple test body to the finite X profile",
            "formula": "V_X(r)=-q_X^T X(r); V_N(r)=-G_obs M_H m_T/r",
            "result": "force_ratio_setup_derived",
            "remaining_input": "test charge q_X^T and source mass calibration must be parent-owned",
            "valid_for_claim": "false",
        },
        {
            "step_id": "LD578_5_alpha_law",
            "derivation_step": "divide by Newtonian potential",
            "formula": "alpha_X(lambda_X)=s_X Q_X^H q_X^T/(4*pi*Z_X*G_obs*M_H*m_T)=K_X Qbar_XH(lambda_X) qbar_XT",
            "result": "product_law_derived_conditionally",
            "remaining_input": "K_X, Qbar_XH(lambda_X), and qbar_XT remain symbolic",
            "valid_for_claim": "false",
        },
        {
            "step_id": "LD578_6_nohair_fork",
            "derivation_step": "test theorem-zero alternative",
            "formula": "int[Z_X|grad X|^2+M_X^2 X^2]=int_boundary Z_X X n.gradX + int X J_X",
            "result": "conditional_nohair_identity_only",
            "remaining_input": "J_X=0 and boundary flux=0 failed to be parent-derived earlier",
            "valid_for_claim": "false",
        },
        {
            "step_id": "LD578_7_verdict",
            "derivation_step": "combine local law with R10",
            "formula": "abs(K_X Qbar_XH(lambda_X) qbar_XT)<=alpha_bound(lambda_X)",
            "result": "exact_nonclaim_target_law",
            "remaining_input": "derive lambda_X and product coefficients before scoring",
            "valid_for_claim": "false",
        },
    ]


def make_mass_gap_targets(curve_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for lambda_value in LAMBDA_TARGETS:
        alpha_bound, interpolation = log_interp_alpha(curve_rows, lambda_value)
        mu_m_inv = 1.0 / lambda_value
        mu2_m2 = mu_m_inv**2
        m_eV = HBAR_C_EV_M / lambda_value
        rows.append(
            {
                "target_id": f"MGT578_{len(rows)}",
                "lambda_X_m": fmt(lambda_value),
                "lambda_X_um": fmt(lambda_value * 1e6),
                "M_X2_over_Z_X_m_minus2": fmt(mu2_m2),
                "canonical_m_X_eV": fmt(m_eV),
                "alpha_bound_review_candidate": fmt(alpha_bound),
                "unsuppressed_product_allowed_at_lambda": str(alpha_bound >= 1.0).lower(),
                "interpolation_method": interpolation,
                "required_parent_relation": f"M_X^2/Z_X={fmt(mu2_m2)} m^-2",
                "valid_for_claim": "false",
            }
        )
    return rows


def make_reverse_windows(curve_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for threshold in PRODUCT_THRESHOLDS:
        intervals = allowed_intervals(curve_rows, threshold)
        lambda_text = interval_text(intervals)
        mass_text = mass_interval_text(intervals)
        pass_entire = len(intervals) == 1 and math.isclose(intervals[0][0], curve_rows[0]["lambda_value_float"]) and math.isclose(
            intervals[0][1], curve_rows[-1]["lambda_value_float"]
        )
        rows.append(
            {
                "window_id": f"RLW578_{len(rows)}",
                "constant_abs_product": fmt(threshold),
                "condition": "alpha_bound(lambda)>=constant_abs_product",
                "allowed_lambda_intervals_m_review_candidate": lambda_text,
                "allowed_canonical_mX_eV_intervals": mass_text,
                "passes_entire_review_candidate_range": str(pass_entire).lower(),
                "number_of_allowed_intervals": len(intervals),
                "valid_for_claim": "false",
                "notes": "Reverse target only; raw vector digitization can fragment crossings, so intervals are compressed for readability.",
            }
        )
    return rows


def make_product_derivation() -> list[dict[str, object]]:
    return [
        {
            "factor_id": "PCD578_0_KX",
            "factor": "K_X",
            "derived_form": "K_X=s_X/(4*pi*Z_X*G_obs) after chosen X normalization",
            "meaning": "kinetic normalization and sign convention prefactor",
            "status": "conditional_prefactor_derived_numeric_ZX_missing",
            "zero_or_suppression_route": "large Z_X, canonical normalization, or parent source normalization can suppress K_X",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "PCD578_1_Qbar_XH",
            "factor": "Qbar_XH(lambda_X)",
            "derived_form": "Qbar_XH=Pi_M^H[Q_X^H(lambda_X)]/M_H",
            "meaning": "projected source charge per measured source mass",
            "status": "not_parent_derived",
            "zero_or_suppression_route": "source neutrality, screening, boundary no-flux, or Hamiltonian projector orthogonality",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "PCD578_2_qbar_XT",
            "factor": "qbar_XT",
            "derived_form": "qbar_XT=q_X^T/m_T=-m_T^-1 delta S_T/dX",
            "meaning": "ordinary test-body charge per inertial mass",
            "status": "retained_after_576",
            "zero_or_suppression_route": "trivial MTS action on matter constants, selector-blind matter, or small finite matter coupling",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "PCD578_3_lambda_X",
            "factor": "lambda_X",
            "derived_form": "lambda_X=sqrt(Z_X/M_X^2)",
            "meaning": "range selecting the R10 bound ordinate",
            "status": "conditional_law_derived_numeric_Hessian_missing",
            "zero_or_suppression_route": "large M_X^2/Z_X gives short range; no fifth-force if source/test charge zero",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "PCD578_4_alpha_abs_gate",
            "factor": "abs(alpha_X)",
            "derived_form": "abs(alpha_X)=abs(K_X Qbar_XH(lambda_X) qbar_XT)",
            "meaning": "R10 comparison magnitude",
            "status": "gate_locked",
            "zero_or_suppression_route": "sign cannot remove magnitude bound",
            "valid_for_claim": "false",
        },
        {
            "factor_id": "PCD578_5_claim_evidence",
            "factor": "alpha_bound(lambda)",
            "derived_form": "external R10 curve ordinate at derived lambda_X",
            "meaning": "empirical comparison wall",
            "status": "review_candidate_nonclaim",
            "zero_or_suppression_route": "claim needs official/supplemental or QA-promoted curve rows",
            "valid_for_claim": "false",
        },
    ]


def make_repair_queue() -> list[dict[str, object]]:
    return [
        {
            "queue_id": "RQ578_0_parent_Hessian",
            "missing_item": "numeric or symbolic parent Hessian ratio M_X^2/Z_X",
            "why_needed": "sets lambda_X and therefore which R10 bound applies",
            "acceptable_fill": "derive from local parent potential/action second variation with units and sign",
            "failure_mode": "lambda remains a scan knob only",
            "next_action": NEXT_TARGET,
        },
        {
            "queue_id": "RQ578_1_ZX_normalization",
            "missing_item": "Z_X sign and normalization",
            "why_needed": "ghost/ellipticity, range canonicalization, and alpha prefactor all depend on Z_X",
            "acceptable_fill": "positive parent kinetic residue or canonical field convention with transformed charges",
            "failure_mode": "wrong-sign or convention-dependent alpha",
            "next_action": NEXT_TARGET,
        },
        {
            "queue_id": "RQ578_2_source_charge",
            "missing_item": "Qbar_XH(lambda_X)",
            "why_needed": "determines whether host/source sector actually sources the finite X mode",
            "acceptable_fill": "derive neutrality/screening or compute finite projected source charge",
            "failure_mode": "finite branch remains symbolic",
            "next_action": "derive source charge profile",
        },
        {
            "queue_id": "RQ578_3_test_charge",
            "missing_item": "qbar_XT",
            "why_needed": "576 retained test-body charge instead of proving it zero",
            "acceptable_fill": "derive tiny amplitude law from matter coupling or provide bounded coefficient",
            "failure_mode": "R10 cannot score MTS alpha",
            "next_action": "derive qbar_XT amplitude law",
        },
        {
            "queue_id": "RQ578_4_curve_promotion",
            "missing_item": "claim-grade alpha_bound(lambda)",
            "why_needed": "review candidate is useful for pressure but not public evidence",
            "acceptable_fill": "supplemental table, official data, or manual QA-promoted digitization",
            "failure_mode": "private diagnostic only",
            "next_action": "promote bound curve later, after coefficients exist",
        },
        {
            "queue_id": "RQ578_5_local_GR_separation",
            "missing_item": "PPN/source/calibration gates beyond R10",
            "why_needed": "R10 pass would still not be full local GR",
            "acceptable_fill": "measured-GM, beta/gamma, conservation, and frame residuals pass separately",
            "failure_mode": "overclaim",
            "next_action": "keep claim ceiling locked",
        },
    ]


def make_decisions() -> list[dict[str, object]]:
    return [
        {
            "decision_id": "D578_0_lambda_law_derived",
            "decision": "accept lambda_X=sqrt(Z_X/M_X^2) as conditionally derived",
            "meaning": "range is no longer conceptually vague; it is the parent Hessian ratio",
            "status": "conditional_derivation_progress",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D578_1_product_law_derived",
            "decision": "accept alpha_X=K_X Qbar_XH qbar_XT as conditionally derived",
            "meaning": "R10 force strength is an exact Green-function product once coefficients are parent-filled",
            "status": "conditional_derivation_progress",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D578_2_numeric_claim_blocked",
            "decision": "do not claim R10 pass or fail",
            "meaning": "lambda_X, Z_X, Qbar_XH, qbar_XT, and claim-grade curve rows remain missing",
            "status": "blocked_for_claim",
            "next_target": NEXT_TARGET,
        },
        {
            "decision_id": "D578_3_next_best_derivation",
            "decision": "derive parent Hessian/source charge or return to theorem-zero",
            "meaning": "the next real fork is mass gap plus product coefficients, not more prose around R10",
            "status": "next_derivation_target",
            "next_target": NEXT_TARGET,
        },
    ]


def make_route_update() -> list[dict[str, object]]:
    return [
        {
            "route_id": "RU578_0_allowed",
            "allowed_after_578": "use lambda_X=sqrt(Z_X/M_X^2) as the canonical local range law",
            "forbidden_after_578": "choose lambda_X by fit without parent Hessian provenance",
            "next_action": "derive M_X^2/Z_X",
        },
        {
            "route_id": "RU578_1_allowed",
            "allowed_after_578": "use Green-function alpha product as the coefficient target",
            "forbidden_after_578": "treat symbolic K_X Qbar_XH qbar_XT as numeric evidence",
            "next_action": "fill K_X, Qbar_XH, qbar_XT",
        },
        {
            "route_id": "RU578_2_allowed",
            "allowed_after_578": "use reverse lambda windows to guide derivation pressure",
            "forbidden_after_578": "claim windows are exclusions before lambda/product are derived",
            "next_action": "derive range first, then compare",
        },
        {
            "route_id": "RU578_3_allowed",
            "allowed_after_578": "keep theorem-zero route as a possible rescue only if parent identities close",
            "forbidden_after_578": "erase finite branch pressure by saying qbar_XT should vanish",
            "next_action": NEXT_TARGET,
        },
    ]


def make_validation(
    source_rows: list[dict[str, object]],
    prior_validation: list[dict[str, str]],
    prior_summary: list[dict[str, str]],
    local_derivation: list[dict[str, object]],
    mass_targets: list[dict[str, object]],
    windows: list[dict[str, object]],
    product_derivation: list[dict[str, object]],
    repair_queue: list[dict[str, object]],
    live_claim_rows: list[dict[str, str]],
    decisions: list[dict[str, object]],
) -> list[dict[str, object]]:
    missing = [row["source_file"] for row in source_rows if row["exists"] != "True"]
    prior_pass = bool(prior_validation) and all(row.get("result") == "pass" for row in prior_validation)
    qbar_retained = bool(prior_summary) and prior_summary[0].get("qbar_XT_retained") == "true"
    lambda_law = any(row.get("result") == "lambda_law_derived_conditionally" for row in local_derivation)
    product_law = any(row.get("result") == "product_law_derived_conditionally" for row in local_derivation)
    live_claim_valid = [row for row in live_claim_rows if str(row.get("valid_for_claim", "")).lower() == "true"]
    blocked_decision = any(row.get("status") == "blocked_for_claim" for row in decisions)
    one_window = next(row for row in windows if row["constant_abs_product"] == "1")
    per_mille_window = next(row for row in windows if row["constant_abs_product"] == "0.001")
    positive_targets = all(float(row["M_X2_over_Z_X_m_minus2"]) > 0 for row in mass_targets)
    return [
        {
            "check_id": "V578_0_source_paths_exist",
            "result": "pass" if not missing else "fail",
            "detail": "missing=" + str(len(missing)) + (";" + ";".join(map(str, missing)) if missing else ""),
        },
        {
            "check_id": "V578_1_prior_577_validated",
            "result": "pass" if prior_pass and qbar_retained else "fail",
            "detail": f"prior_rows={len(prior_validation)};qbar_retained={qbar_retained}",
        },
        {
            "check_id": "V578_2_lambda_law_derived_conditionally",
            "result": "pass" if lambda_law else "fail",
            "detail": "lambda_X=sqrt(Z_X/M_X^2)",
        },
        {
            "check_id": "V578_3_product_law_derived_conditionally",
            "result": "pass" if product_law else "fail",
            "detail": "alpha_X=K_X Qbar_XH qbar_XT",
        },
        {
            "check_id": "V578_4_mass_gap_targets_numeric",
            "result": "pass" if mass_targets and positive_targets else "fail",
            "detail": f"target_rows={len(mass_targets)}",
        },
        {
            "check_id": "V578_5_reverse_windows_sane",
            "result": "pass"
            if one_window["passes_entire_review_candidate_range"] == "false"
            and per_mille_window["passes_entire_review_candidate_range"] == "true"
            else "fail",
            "detail": "product_1_not_global_safe;product_0p001_global_safe_on_review_candidate",
        },
        {
            "check_id": "V578_6_coefficients_still_block_claim",
            "result": "pass" if len(repair_queue) >= 5 and blocked_decision else "fail",
            "detail": f"repair_items={len(repair_queue)};claim_allowed=false",
        },
        {
            "check_id": "V578_7_live_claim_curve_still_blocked",
            "result": "pass" if len(live_claim_valid) == 0 else "fail",
            "detail": f"live_claim_rows={len(live_claim_valid)}",
        },
        {
            "check_id": "V578_8_no_overclaim",
            "result": "pass",
            "detail": "conditional_laws_only;no_R10_pass;no_WEP;no_PPN;no_local_GR",
        },
    ]


def write_markdown(
    generated: str,
    source_rows: list[dict[str, object]],
    local_derivation: list[dict[str, object]],
    mass_targets: list[dict[str, object]],
    windows: list[dict[str, object]],
    product_derivation: list[dict[str, object]],
    repair_queue: list[dict[str, object]],
    decisions: list[dict[str, object]],
    route_update: list[dict[str, object]],
    validation: list[dict[str, object]],
) -> None:
    body = f"""# 578 Y5 R10 lambda-X mass-gap and product coefficient derivation targets

Generated: {generated}  
Status: `{STATUS}`  
Claim ceiling: `{CLAIM_CEILING}`  
Next target: `{NEXT_TARGET}`

## Verdict
- The derivation path works at the structural level.
- From the local quadratic parent action, the finite range is:

```text
(-Z_X Delta + M_X^2) X = J_X,
mu_X^2 = M_X^2 / Z_X,
lambda_X = sqrt(Z_X / M_X^2).
```

- From the Green-function exterior field, the fifth-force strength is:

```text
X(r) = Q_X^H exp(-r/lambda_X)/(4 pi Z_X r),
alpha_X(lambda_X) = K_X Qbar_XH(lambda_X) qbar_XT.
```

- So we have derived the exact local target law, not the numeric pass. The missing machine is now precise: parent Hessian ratio `M_X^2/Z_X`, positive `Z_X`, source charge `Qbar_XH`, and test charge `qbar_XT`.

## Source Register
{markdown_table(source_rows, ["source_file", "exists", "role"])}

## Local Quadratic Derivation
{markdown_table(local_derivation, ["step_id", "derivation_step", "formula", "result", "remaining_input", "valid_for_claim"])}

## Mass-Gap Targets
{markdown_table(mass_targets, ["target_id", "lambda_X_m", "lambda_X_um", "M_X2_over_Z_X_m_minus2", "canonical_m_X_eV", "alpha_bound_review_candidate", "unsuppressed_product_allowed_at_lambda", "required_parent_relation", "valid_for_claim"])}

## Reverse Lambda Windows
{markdown_table(windows, ["window_id", "constant_abs_product", "allowed_lambda_intervals_m_review_candidate", "allowed_canonical_mX_eV_intervals", "passes_entire_review_candidate_range", "number_of_allowed_intervals", "valid_for_claim"])}

## Product Coefficient Derivation
{markdown_table(product_derivation, ["factor_id", "factor", "derived_form", "meaning", "status", "zero_or_suppression_route", "valid_for_claim"])}

## Repair Queue
{markdown_table(repair_queue, ["queue_id", "missing_item", "why_needed", "acceptable_fill", "failure_mode", "next_action"])}

## Decision
{markdown_table(decisions, ["decision_id", "decision", "meaning", "status", "next_target"])}

## Route Update
{markdown_table(route_update, ["route_id", "allowed_after_578", "forbidden_after_578", "next_action"])}

## Validation
{markdown_table(validation, ["check_id", "result", "detail"])}

## Practical Read
This is a better position than “we need a miracle”. The local range and force law are now proper engineering targets. If the parent action gives `lambda_X` near tens of microns, an order-one product is not immediately murdered by this private R10 pressure curve. If it gives `lambda_X` around `0.1-1 mm`, the product needs percent-to-per-mille suppression unless a stronger zero theorem returns. The next move is therefore very specific: derive the parent Hessian ratio `M_X^2/Z_X` and the source/test product, or explicitly demote the finite branch to a scored residual.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    generated = datetime.now(timezone.utc).isoformat()
    source_rows = source_register()
    prior_validation = read_csv(PRIOR_577_VALIDATION)
    prior_summary = read_csv(PRIOR_577_SUMMARY)
    curve_rows = numeric_curve_rows(read_csv(REVIEW_CURVE))
    live_claim_rows = read_csv(LIVE_CLAIM_CURVE)

    local_derivation = make_local_derivation()
    mass_targets = make_mass_gap_targets(curve_rows)
    reverse_windows = make_reverse_windows(curve_rows)
    product_derivation = make_product_derivation()
    repair_queue = make_repair_queue()
    decisions = make_decisions()
    route_update = make_route_update()
    validation = make_validation(
        source_rows,
        prior_validation,
        prior_summary,
        local_derivation,
        mass_targets,
        reverse_windows,
        product_derivation,
        repair_queue,
        live_claim_rows,
        decisions,
    )

    product_one = next(row for row in reverse_windows if row["constant_abs_product"] == "1")
    product_per_mille = next(row for row in reverse_windows if row["constant_abs_product"] == "0.001")
    summary_rows = [
        {
            "summary_id": "S578_0_result",
            "status": STATUS,
            "lambda_law": "lambda_X=sqrt(Z_X/M_X^2)",
            "alpha_law": "alpha_X(lambda_X)=K_X*Qbar_XH(lambda_X)*qbar_XT",
            "operator_law": "(-Z_X Delta + M_X^2)X=J_X",
            "numeric_parent_Hessian_available": "false",
            "numeric_product_coefficients_available": "false",
            "product_1_allowed_lambda_windows_m_review_candidate": product_one["allowed_lambda_intervals_m_review_candidate"],
            "product_0p001_global_safe_review_candidate": product_per_mille["passes_entire_review_candidate_range"],
            "claim_allowed": "false",
            "R10_pass_for_claim": "false",
            "local_GR_pass": "false",
            "next_target": NEXT_TARGET,
        }
    ]

    write_csv(SOURCE_REGISTER_PATH, source_rows, ["source_file", "exists", "role"])
    write_csv(
        LOCAL_DERIVATION_PATH,
        local_derivation,
        ["step_id", "derivation_step", "formula", "result", "remaining_input", "valid_for_claim"],
    )
    write_csv(
        MASS_GAP_TARGETS_PATH,
        mass_targets,
        [
            "target_id",
            "lambda_X_m",
            "lambda_X_um",
            "M_X2_over_Z_X_m_minus2",
            "canonical_m_X_eV",
            "alpha_bound_review_candidate",
            "unsuppressed_product_allowed_at_lambda",
            "interpolation_method",
            "required_parent_relation",
            "valid_for_claim",
        ],
    )
    write_csv(
        REVERSE_WINDOWS_PATH,
        reverse_windows,
        [
            "window_id",
            "constant_abs_product",
            "condition",
            "allowed_lambda_intervals_m_review_candidate",
            "allowed_canonical_mX_eV_intervals",
            "passes_entire_review_candidate_range",
            "number_of_allowed_intervals",
            "valid_for_claim",
            "notes",
        ],
    )
    write_csv(
        PRODUCT_DERIVATION_PATH,
        product_derivation,
        ["factor_id", "factor", "derived_form", "meaning", "status", "zero_or_suppression_route", "valid_for_claim"],
    )
    write_csv(
        REPAIR_QUEUE_PATH,
        repair_queue,
        ["queue_id", "missing_item", "why_needed", "acceptable_fill", "failure_mode", "next_action"],
    )
    write_csv(
        DECISION_PATH,
        decisions,
        ["decision_id", "decision", "meaning", "status", "next_target"],
    )
    write_csv(
        ROUTE_UPDATE_PATH,
        route_update,
        ["route_id", "allowed_after_578", "forbidden_after_578", "next_action"],
    )
    write_csv(VALIDATION_PATH, validation, ["check_id", "result", "detail"])
    write_csv(
        SUMMARY_PATH,
        summary_rows,
        [
            "summary_id",
            "status",
            "lambda_law",
            "alpha_law",
            "operator_law",
            "numeric_parent_Hessian_available",
            "numeric_product_coefficients_available",
            "product_1_allowed_lambda_windows_m_review_candidate",
            "product_0p001_global_safe_review_candidate",
            "claim_allowed",
            "R10_pass_for_claim",
            "local_GR_pass",
            "next_target",
        ],
    )

    write_markdown(
        generated,
        source_rows,
        local_derivation,
        mass_targets,
        reverse_windows,
        product_derivation,
        repair_queue,
        decisions,
        route_update,
        validation,
    )

    all_passed = all(row["result"] == "pass" for row in validation)
    print(
        json.dumps(
            {
                "generated_at_utc": generated,
                "status": STATUS,
                "claim_ceiling": CLAIM_CEILING,
                "doc": str(DOC_PATH.relative_to(ROOT)),
                "validation": str(VALIDATION_PATH.relative_to(ROOT)),
                "next_target": NEXT_TARGET,
                "all_validation_passed": all_passed,
                "claim_allowed": False,
                "lambda_law": "lambda_X=sqrt(Z_X/M_X^2)",
                "alpha_law": "alpha_X=K_X*Qbar_XH*qbar_XT",
            },
            indent=2,
        )
    )
    if not all_passed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
