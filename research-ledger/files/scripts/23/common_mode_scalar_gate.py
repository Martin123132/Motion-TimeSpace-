from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Tuple


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    rows = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def as_float(value: object) -> Optional[float]:
    try:
        if value is None:
            return None
        text = str(value).strip()
        if not text or text.upper().startswith("MISSING") or text == "alpha(lambda)":
            return None
        return float(text)
    except (TypeError, ValueError):
        return None


def nearest_r10_bound(
    r10_rows: Iterable[Mapping[str, object]],
    target_lambda_m: float,
) -> Optional[Tuple[Mapping[str, object], float, float, float]]:
    candidates: List[Tuple[float, Mapping[str, object], float, float]] = []
    for row in r10_rows:
        lambda_value = as_float(row.get("lambda_value"))
        alpha_bound = as_float(row.get("alpha_bound"))
        if lambda_value is None or alpha_bound is None or lambda_value <= 0 or alpha_bound <= 0:
            continue
        candidates.append((abs(math.log(lambda_value / target_lambda_m)), row, lambda_value, alpha_bound))
    if not candidates:
        return None
    _, row, lambda_value, alpha_bound = sorted(candidates, key=lambda item: item[0])[0]
    return row, lambda_value, alpha_bound, abs(lambda_value - target_lambda_m)


def common_mode_normal_form_rows() -> List[Dict[str, object]]:
    return [
        {
            "normal_form_id": "CM4466_0_parent_action_split",
            "object": "local scalar/common-mode normal form",
            "formula": "S = S_GR[g_obs] + S_chi[g_obs,chi;c_R2_eff] + S_matter[Psi, A(chi)^2 g_obs, theta_j(chi)]",
            "meaning": "after WEP differential closure, only a common conformal/source factor and the finite curvature scalar can remain",
            "zero_condition": "c_R2_eff=0 or d ln A/dchi=0 and d ln theta_j/dchi=0",
            "status": "NORMAL_FORM_WRITTEN_NONCLAIM",
            "valid_for_claim": False,
        },
        {
            "normal_form_id": "CM4466_1_common_charge",
            "object": "common matter charge",
            "formula": "C_matter = d ln A/dchi; C_A=C_common=C_matter when b_j=d ln theta_j/dchi=0",
            "meaning": "MICROSCOPE sees Delta_C_AB=0, but R10/PPN/orbits see a common fifth force if C_matter != 0",
            "zero_condition": "matter action is chi-silent in the metric/constant sector",
            "status": "WEP_SAFE_NOT_R10_SAFE",
            "valid_for_claim": False,
        },
        {
            "normal_form_id": "CM4466_2_scalaron_range",
            "object": "finite R2 scalar range",
            "formula": "lambda_R2 = sqrt(6*c_R2_eff) = sqrt(D0/2)",
            "meaning": "c_R2_eff controls whether a propagating scalar exists and how far it reaches",
            "zero_condition": "c_R2_eff=0 gives no finite local scalar range; c_R2_eff<0 is tachyonic/not a pass",
            "status": "FINITE_BRANCH_IF_POSITIVE",
            "valid_for_claim": False,
        },
        {
            "normal_form_id": "CM4466_3_R10_alpha",
            "object": "composition-blind Yukawa strength",
            "formula": "alpha_eff = C_matter^2/3 in the pure metric f(R)-like scalar normalization",
            "meaning": "universal metric coupling C_matter=1 gives alpha_eff=1/3 even though WEP is zero",
            "zero_condition": "C_matter=0 or no scalar pole",
            "status": "R10_PPN_ORBITAL_PRESSURE_OBJECT",
            "valid_for_claim": False,
        },
    ]


def zero_route_rows() -> List[Dict[str, object]]:
    return [
        {
            "route_id": "ZR4466_0_source_silence",
            "route": "C_matter=0",
            "required_parent_clause": "matter action and all local matter constants are independent of chi after quotienting",
            "mathematical_test": "delta S_matter/dchi = 0 and d ln theta_j/dchi=0 before using field equations",
            "if_passes": "WEP, R10 scalar source, PPN scalar gamma tail and orbital fifth force vanish together",
            "current_status": "STRONG_ROUTE_EXACT_BUT_PARENT_SIGNATURE_UNSIGNED",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "route_id": "ZR4466_1_refinement_cR2_zero",
            "route": "c_R2_eff=0",
            "required_parent_clause": "quotient/projective refinement equivalence, cylindrical first-moment action, owned hinge/connection/coframe and no second curvature-square channel",
            "mathematical_test": "S_n(delta)=n Phi(delta/n)=Phi(delta) for same physical flux, forcing Phi''(0)=0",
            "if_passes": "the scalar pole is absent; lambda_R2 is not a physical finite range",
            "current_status": "EXACT_CONDITIONAL_ZERO_SELECTOR_PARENT_SIGNATURE_OPEN",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "route_id": "ZR4466_2_universal_metric_scalar",
            "route": "C_matter=1 with finite c_R2_eff>0",
            "required_parent_clause": "pure metric f(R)-like scalar with same Hilbert trace source and no screening/readout loophole",
            "mathematical_test": "alpha_eff=1/3 and lambda_R2=sqrt(6*c_R2_eff)",
            "if_passes": "not a zero route; must pass R10/PPN/orbital bounds",
            "current_status": "FINITE_BRANCH_PRESSURED_BY_R10",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
        {
            "route_id": "ZR4466_3_short_range_or_weak_common",
            "route": "finite but small/short common mode",
            "required_parent_clause": "source-backed C_matter and c_R2_eff values in the same branch",
            "mathematical_test": "C_matter^2/3 <= alpha_bound(lambda_R2)",
            "if_passes": "empirical local scalar bound can be satisfied without exact zero",
            "current_status": "FORMULA_READY_VALUES_AND_LIVE_CURVE_MISSING",
            "blocks_claim": True,
            "valid_for_claim": False,
        },
    ]


def r10_pressure_rows(
    r10_review_rows: List[Dict[str, str]],
    lambda_pressure_m: float = 7.639299809562832e-05,
    live_numeric_rows: int = 0,
) -> List[Dict[str, object]]:
    nearest = nearest_r10_bound(r10_review_rows, lambda_pressure_m)
    if nearest is None:
        return [
            {
                "pressure_id": "R10P4466_0_missing",
                "branch": "finite common-mode scalar",
                "lambda_m": lambda_pressure_m,
                "alpha_bound": "MISSING_REVIEW_BOUND",
                "alpha_eff_universal": 1.0 / 3.0,
                "ratio_alpha_to_bound": "MISSING",
                "C_matter_abs_limit": "MISSING",
                "status": "NO_R10_PRESSURE_AVAILABLE",
                "valid_for_claim": False,
            }
        ]
    row, nearest_lambda, alpha_bound, delta_lambda = nearest
    alpha_universal = 1.0 / 3.0
    ratio = alpha_universal / alpha_bound
    cmatter_limit = math.sqrt(3.0 * alpha_bound)
    return [
        {
            "pressure_id": "R10P4466_0_current_lambda_pressure",
            "branch": "universal metric scalar at current lambda_R2 pressure",
            "lambda_m": f"{lambda_pressure_m:.12g}",
            "nearest_review_lambda_m": f"{nearest_lambda:.12g}",
            "delta_lambda_m": f"{delta_lambda:.12g}",
            "alpha_bound": f"{alpha_bound:.12g}",
            "alpha_eff_universal": f"{alpha_universal:.12g}",
            "ratio_alpha_to_bound": f"{ratio:.12g}",
            "C_matter_abs_limit": f"{cmatter_limit:.12g}",
            "source_ref": row.get("alpha_bound_source", "MISSING_SOURCE"),
            "curve_status": "REVIEW_CANDIDATE_NONCLAIM_LIVE_NUMERIC_ROWS_%s" % live_numeric_rows,
            "status": "UNIVERSAL_CMATTER_FAILS_REVIEW_PRESSURE" if alpha_universal > alpha_bound else "UNIVERSAL_CMATTER_PASSES_REVIEW_PRESSURE",
            "valid_for_claim": False,
        },
        {
            "pressure_id": "R10P4466_1_decoupled_common_mode",
            "branch": "C_matter=0 source-silent scalar/common mode",
            "lambda_m": f"{lambda_pressure_m:.12g}",
            "nearest_review_lambda_m": f"{nearest_lambda:.12g}",
            "delta_lambda_m": f"{delta_lambda:.12g}",
            "alpha_bound": f"{alpha_bound:.12g}",
            "alpha_eff_universal": "0",
            "ratio_alpha_to_bound": "0",
            "C_matter_abs_limit": f"{cmatter_limit:.12g}",
            "source_ref": row.get("alpha_bound_source", "MISSING_SOURCE"),
            "curve_status": "R10_IRRELEVANT_IF_PARENT_SOURCE_SILENCE_SIGNED",
            "status": "PASSES_IF_ZERO_THEOREM_SIGNED",
            "valid_for_claim": False,
        },
        {
            "pressure_id": "R10P4466_2_cR2_zero",
            "branch": "c_R2_eff=0 refinement/hinge zero",
            "lambda_m": "no finite scalar pole",
            "nearest_review_lambda_m": f"{nearest_lambda:.12g}",
            "delta_lambda_m": "not_applicable_if_no_pole",
            "alpha_bound": f"{alpha_bound:.12g}",
            "alpha_eff_universal": "0",
            "ratio_alpha_to_bound": "0",
            "C_matter_abs_limit": "not_needed_if_no_pole",
            "source_ref": row.get("alpha_bound_source", "MISSING_SOURCE"),
            "curve_status": "R10_IRRELEVANT_IF_PARENT_REFINEMENT_ZERO_SIGNED",
            "status": "PASSES_IF_ZERO_SELECTOR_SIGNED",
            "valid_for_claim": False,
        },
    ]


def finite_branch_contract_rows() -> List[Dict[str, object]]:
    return [
        {
            "contract_id": "FB4466_0_live_curve",
            "needed_input": "source-backed live alpha_bound(lambda) curve",
            "current_status": "LIVE_FILE_PLACEHOLDER_REVIEW_CANDIDATE_ONLY",
            "why_needed": "review-candidate vector extraction is useful pressure but not claim-grade",
            "valid_for_claim": False,
        },
        {
            "contract_id": "FB4466_1_parent_cR2_value",
            "needed_input": "c_R2_eff or D0 value with sign/units from parent coefficient owner",
            "current_status": "MISSING_PARENT_COEFFICIENT_VALUE",
            "why_needed": "lambda_R2 cannot be predicted from a bound pressure alone",
            "valid_for_claim": False,
        },
        {
            "contract_id": "FB4466_2_parent_Cmatter_value",
            "needed_input": "C_matter from matter action normal form or scalar/source decoupling theorem",
            "current_status": "MISSING_PARENT_SOURCE_SILENCE_OR_COUPLING_VALUE",
            "why_needed": "alpha_eff cannot be treated as fitted after R10/PPN tests",
            "valid_for_claim": False,
        },
        {
            "contract_id": "FB4466_3_no_screening_shortcut",
            "needed_input": "screening/readout mechanism with parent equations if invoked",
            "current_status": "NO_SCREENING_MECHANISM_SIGNED",
            "why_needed": "screening cannot be used as an unmodelled escape hatch",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4466_0_normal_form",
            "finding": "after WEP differential closure, common-mode scalar coupling has only three honest exits: C_matter=0, c_R2_eff=0, or finite alpha(lambda) bound pass",
            "consequence": "calibrated G and WEP cannot hide the universal scalar",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4466_1_R10_pressure",
            "finding": "at the current lambda_R2 pressure the universal C_matter=1 branch fails the review-candidate R10 smoke pressure",
            "consequence": "the natural metric f(R)-like scalar is not the safe local-GR route unless the parent shortens/decouples/zeros it",
            "next_action": "prioritize zero/decoupling over finite tuning",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4466_2_best_route",
            "finding": "the cleanest derivation target is now a parent action signature that either makes chi matter-silent or activates the refinement c_R2 zero selector",
            "consequence": "next checkpoint should inspect the parent action normal form, not run another broad empirical loop",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    normal_rows: List[Dict[str, object]],
    zero_rows: List[Dict[str, object]],
    r10_rows: List[Dict[str, object]],
    finite_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    source_ok = all(bool(row.get("local_path_exists")) and bool(row.get("needle_found")) for row in source_rows)
    normal_ok = any(row.get("normal_form_id") == "CM4466_0_parent_action_split" for row in normal_rows)
    zero_ok = any(row.get("route_id") == "ZR4466_0_source_silence" for row in zero_rows) and any(row.get("route_id") == "ZR4466_1_refinement_cR2_zero" for row in zero_rows)
    r10_pressure = any(row.get("status") == "UNIVERSAL_CMATTER_FAILS_REVIEW_PRESSURE" for row in r10_rows)
    finite_blocked = all(str(row.get("current_status", "")).startswith(("MISSING", "LIVE_FILE_PLACEHOLDER", "NO_SCREENING")) for row in finite_rows)
    no_claims = not any(
        str(row.get("valid_for_claim")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true"
        for row in normal_rows + zero_rows + r10_rows + finite_rows
    )
    return [
        {
            "gate_id": "CG4466_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": source_ok,
            "claim_allowed": False,
            "detail": "source register validates 4465/4464/4461/refinement/R10 handoff",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4466_1_normal_form",
            "claim": "common-mode scalar normal form is written",
            "gate_pass": normal_ok,
            "claim_allowed": False,
            "detail": "S_matter[A(chi)^2 g_obs, theta_j(chi)] separates C_matter from c_R2_eff",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4466_2_zero_routes",
            "claim": "source silence and c_R2 zero routes are explicit",
            "gate_pass": zero_ok,
            "claim_allowed": False,
            "detail": "both routes remain parent-signature conditional",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4466_3_R10_pressure",
            "claim": "universal C_matter=1 branch is pressure-tested",
            "gate_pass": r10_pressure,
            "claim_allowed": False,
            "detail": "review candidate says alpha=1/3 fails at current lambda pressure",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4466_4_finite_branch_blocked",
            "claim": "finite common-mode branch is claim-ready",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "blocked until live curve, parent c_R2 value and parent C_matter value exist" if finite_blocked else "unexpected finite inputs present",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4466_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to public/local-GR claim evidence",
            "gate_pass": no_claims,
            "claim_allowed": False,
            "detail": "4466 is private theorem/pressure discipline",
            "valid_for_claim": False,
        },
    ]
