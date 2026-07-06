from __future__ import annotations

import csv
from pathlib import Path
from typing import Dict, Iterable, List


def write_csv(path: Path, rows: Iterable[Dict[str, object]]) -> None:
    row_list = list(rows)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not row_list:
        path.write_text("", encoding="utf-8")
        return
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(row_list[0].keys()))
        writer.writeheader()
        writer.writerows(row_list)


def read_csv(path: Path) -> List[Dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def second_order_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "SOT4469_0_strict_metric_second_order",
            "target": "forbid non-topological curvature-square bulk terms",
            "premise": "4D local diffeo-invariant metric/coframe branch; equations through tested local order are second order; no extra unscreened local modes; boundary terms are fixed/topological/routed",
            "derivation": "Under the strict second-order/no-extra-mode selector, the local bulk normal form is EH plus Lambda plus topological/boundary terms. Non-topological R^2, Ricci^2, Weyl^2, f(R), and nonlocal kernels either introduce higher derivatives or extra scalar/spin modes, so they are not allowed in the exact local branch.",
            "if_signed": "D0=0, D2=0, c_R2_eff=0 for local tests; no metric scalaron/fifth-force branch",
            "current_status": "EXACT_CONDITIONAL_SELECTOR_THEOREM",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SOT4469_1_current_MTS_selector_status",
            "target": "is the strict selector parent-owned by MTS",
            "premise": "MTS parent action itself derives leading two-derivative order and no extra unscreened light modes, rather than adopting them as a local selector",
            "derivation": "The 200/201 trail records the selector and residual ledger, but also records selector assumptions as not parent-derived and curvature-square terms as residual coefficients.",
            "if_signed": "second channel could be forbidden rather than merely bounded",
            "current_status": "SELECTOR_PRESENT_NOT_PARENT_DERIVED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SOT4469_2_palatini_connection_escape",
            "target": "independent connection/torsion cannot sneak in a second mode",
            "premise": "connection is either Levi-Civita by field inventory or algebraically eliminated by positive/invertible equation with no source/projective/boundary leakage",
            "derivation": "If an independent connection survives, torsion/nonmetricity or hypermomentum can carry local residuals even if metric curvature squares are filtered.",
            "if_signed": "connection sector cannot regenerate c_R2/D2-like local force",
            "current_status": "CONDITIONAL_OWNER_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SOT4469_3_refinement_same_channel",
            "target": "same signed-deficit c2",
            "premise": "one physical oriented curvature flux is represented by quotient/projective refinements and a cylindrical first-moment action",
            "derivation": "S_n(delta)=n Phi(delta/n)=Phi(delta) for all n forces the same-channel primitive response to be linear, so Phi''(0)=0.",
            "if_signed": "same-channel c2_visible=0",
            "current_status": "EXACT_CONDITIONAL_FROM_4459_PARENT_PREMISE_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SOT4469_4_no_second_channel_verdict",
            "target": "full no-second-channel local-GR scalar closure",
            "premise": "SOT4469_0 through SOT4469_3 all sign together and hidden scalar/marker/grain/nonlocal channels are absent/topological/heavy",
            "derivation": "The current corpus has a strong conditional theorem shape, but it does not yet parent-sign the strict selector or exclude every separate second channel.",
            "if_signed": "finite scalar pack becomes inactive",
            "current_status": "NOT_SIGNED_FINITE_BRANCH_RETAINED",
            "parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def channel_classification_rows() -> List[Dict[str, object]]:
    return [
        {
            "channel_id": "CH4469_0_Gauss_Bonnet",
            "channel": "4D Gauss-Bonnet combination",
            "operator": "Riemann^2 - 4 Ricci^2 + R^2",
            "safe_route": "topological/boundary-only with constant coefficient and boundary silence",
            "current_status": "HARMLESS_ONLY_IF_BOUNDARY_SAFE",
            "finite_or_blocked_route": "retain boundary/class-hair row if coefficient or boundary varies",
            "valid_for_claim": False,
        },
        {
            "channel_id": "CH4469_1_R2_fR_scalar",
            "channel": "R^2 or f(R) scalar mode",
            "operator": "c_R2 R^2 + f_extra(R)",
            "safe_route": "coefficient zero, infinite mass/decoupled scalar, or strict second-order/no-extra-mode theorem",
            "current_status": "LIVE_SCALAR_COUNTERCHANNEL",
            "finite_or_blocked_route": "c_R2_eff, lambda_R2, C_total, alpha(lambda), PPN gamma",
            "valid_for_claim": False,
        },
        {
            "channel_id": "CH4469_2_Ricci_Weyl_spin2",
            "channel": "Ricci^2/Weyl^2/Riemann^2 non-topological spin/tensor mode",
            "operator": "c_Ric R_mn R^mn + c_W C_mnrs C^mnrs + c_Riem R_mnrs R^mnrs",
            "safe_route": "topological Gauss-Bonnet combination or all non-topological coefficients zero/heavy",
            "current_status": "LIVE_SPIN2_COUNTERCHANNEL",
            "finite_or_blocked_route": "D2 basis guard plus PPN/light/wave projection",
            "valid_for_claim": False,
        },
        {
            "channel_id": "CH4469_3_trace_norm_holonomy",
            "channel": "trace/norm/even holonomy or physical grain response",
            "operator": "trace(Log U)^2, norm(Log U)^2, grain-scale quadratic action",
            "safe_route": "parent proves only oriented signed linear deficit is physical and refinement-gauge invariant",
            "current_status": "LIVE_IF_PARENT_OWNS_TRACE_NORM_OR_GRAIN",
            "finite_or_blocked_route": "map to c2_visible and c_R2_eff with shape/cell normalization",
            "valid_for_claim": False,
        },
        {
            "channel_id": "CH4469_4_hidden_scalar_marker_memory_tower",
            "channel": "hidden scalar, marker prefactor, nonlocal kernel or memory tower",
            "operator": "auxiliary scalar/tower integrated out into f(R), Yukawa or nonlocal terms",
            "safe_route": "typed field inventory forbids it, or source-free positive no-hair/heavy-screening theorem signs",
            "current_status": "LIVE_COUNTERCHANNEL",
            "finite_or_blocked_route": "source-backed mass, stiffness, coupling and projection pack",
            "valid_for_claim": False,
        },
        {
            "channel_id": "CH4469_5_verdict",
            "channel": "complete second curvature/scalar channel",
            "operator": "all CH4469_0 through CH4469_4",
            "safe_route": "only GB/topological boundary harmless; all propagating or sourced channels zero/topological/heavy/screened",
            "current_status": "NOT_FORBIDDEN_BY_CURRENT_PARENT",
            "finite_or_blocked_route": "finite c_R2_eff/C_total coefficient pack remains mandatory",
            "valid_for_claim": False,
        },
    ]


def finite_coefficient_pack_rows() -> List[Dict[str, object]]:
    return [
        {
            "coefficient_id": "FC4469_0_D0_scalar_basis",
            "quantity": "D0",
            "formula": "D0 = 12*c_R2 + c_Ric - 6*c_W - 8*c_Riem",
            "needed_for": "scalar-sector mass/range and pure-R2 guard",
            "current_value": "MISSING_PARENT_BASIS_COEFFICIENTS",
            "units": "m^2_or_action_normalized_length_squared",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "FC4469_1_D2_spin2_basis",
            "quantity": "D2",
            "formula": "D2 = -c_Ric - 2*c_W - 4*c_Riem",
            "needed_for": "spin-2/tensor contamination guard; pure f(R) scalar map requires D2=0",
            "current_value": "MISSING_PARENT_BASIS_COEFFICIENTS",
            "units": "m^2_or_action_normalized_length_squared",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "FC4469_2_cR2_eff",
            "quantity": "c_R2_eff",
            "formula": "c_R2_eff = xi_shape*c2_visible*ell_cell^2/N_EH; pure-R2 lambda_R2=sqrt(6*c_R2_eff)=sqrt(D0/2)",
            "needed_for": "finite scalar range lambda_R2",
            "current_value": "MISSING_c2_VISIBLE_ELL_CELL_SHAPE_FACTOR_N_EH_OR_D0",
            "units": "m^2",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "FC4469_3_C_total",
            "quantity": "C_total",
            "formula": "C_total = C_explicit_Achi + C_metric_pole + C_hidden_source",
            "needed_for": "alpha_eff=C_total^2/3",
            "current_value": "C_explicit_Achi_PRIVATE_ZERO; C_metric_pole_MISSING; C_hidden_source_MISSING",
            "units": "dimensionless",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "FC4469_4_live_alpha_curve",
            "quantity": "alpha_bound(lambda)",
            "formula": "abs(C_total^2/3) <= alpha_bound(lambda_R2)",
            "needed_for": "R10 finite scalar claim gate",
            "current_value": "LIVE_CLAIM_CURVE_PLACEHOLDER_REVIEW_CANDIDATE_NONCLAIM_ONLY",
            "units": "dimensionless_vs_m",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "coefficient_id": "FC4469_5_lightcone_PPN_projection",
            "quantity": "gamma(r)-1",
            "formula": "gamma(r)-1 = -2*alpha_eff*exp(-r/lambda_R2)/(1+alpha_eff*exp(-r/lambda_R2))",
            "needed_for": "PPN/local-light branch if scalar range reaches solar-system scales",
            "current_value": "MISSING_LIGHTCONE_AND_C_TOTAL_PROJECTION",
            "units": "dimensionless",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
        },
    ]


def bound_pressure_rows() -> List[Dict[str, object]]:
    return [
        {
            "pressure_id": "BP4469_0_current_R10_pressure",
            "branch": "universal metric scalar at current private lambda pressure",
            "lambda_R2_m": 7.63929980956e-05,
            "alpha_eff_if_C_total_1": 1.0 / 3.0,
            "alpha_bound_review_candidate": 0.136485683105,
            "ratio_alpha_to_bound": 2.44225859996,
            "C_total_abs_limit": 0.63988831003,
            "status": "UNIVERSAL_METRIC_SCALAR_FAILS_REVIEW_CANDIDATE_PRESSURE",
            "valid_for_claim": False,
        },
        {
            "pressure_id": "BP4469_1_decoupling_target",
            "branch": "source/metric scalar decoupled",
            "lambda_R2_m": "any",
            "alpha_eff_if_C_total_1": 0,
            "alpha_bound_review_candidate": "not_needed_if_C_total_0",
            "ratio_alpha_to_bound": 0,
            "C_total_abs_limit": 0,
            "status": "PASSES_ONLY_IF_PARENT_DECUPLING_OR_NO_POLE_SIGNS",
            "valid_for_claim": False,
        },
        {
            "pressure_id": "BP4469_2_no_pole_target",
            "branch": "c_R2_eff=0 no finite scalar pole",
            "lambda_R2_m": "not_applicable",
            "alpha_eff_if_C_total_1": 0,
            "alpha_bound_review_candidate": "not_needed_if_no_pole",
            "ratio_alpha_to_bound": 0,
            "C_total_abs_limit": "not_needed_if_no_pole",
            "status": "PASSES_ONLY_IF_NO_SECOND_CHANNEL_SIGNS",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4469_0_conditional_theorem",
            "finding": "a strict 4D local second-order/no-extra-mode metric/coframe selector would forbid non-topological curvature-square bulk channels",
            "consequence": "this is the cleanest exact route to c_R2_eff=0 and no metric scalaron",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4469_1_current_parent_status",
            "finding": "current MTS does not parent-derive that strict selector; it keeps curvature-square terms as residual coefficients",
            "consequence": "no public local-GR scalar closure; finite coefficient pack remains live",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4469_2_finite_pack_priority",
            "finding": "if the selector cannot be parent-signed, the first useful finite inputs are D0/D2 or c_R2_eff plus C_total",
            "consequence": "R10/PPN claims remain blocked until those coefficients and a live alpha(lambda) curve exist",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    theorem_rows: List[Dict[str, object]],
    channel_rows: List[Dict[str, object]],
    coefficient_rows: List[Dict[str, object]],
    pressure_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    sources_ok = all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in source_rows)
    conditional_theorem_written = any(row.get("theorem_id") == "SOT4469_0_strict_metric_second_order" for row in theorem_rows)
    no_second_signed = any(
        row.get("theorem_id") == "SOT4469_4_no_second_channel_verdict"
        and row.get("parent_signed") is True
        for row in theorem_rows
    )
    finite_pack_ready = all(
        "MISSING" not in str(row.get("current_value")) and row.get("claim_status") != "BLOCKED"
        for row in coefficient_rows
    )
    pressure_has_guard = any(
        row.get("pressure_id") == "BP4469_0_current_R10_pressure"
        and float(row.get("ratio_alpha_to_bound", 0)) > 1
        for row in pressure_rows
    )
    no_claims = all(
        str(row.get("valid_for_claim")).lower() == "false"
        for group in [source_rows, theorem_rows, channel_rows, coefficient_rows, pressure_rows]
        for row in group
    )
    return [
        {
            "gate_id": "CG4469_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": sources_ok,
            "claim_allowed": False,
            "detail": "source register validates selector, residual, refinement, scalaron and pressure evidence",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4469_1_conditional_second_order_theorem",
            "claim": "conditional theorem forbidding non-topological second curvature channels is written",
            "gate_pass": conditional_theorem_written,
            "claim_allowed": False,
            "detail": "exact route exists only if strict second-order/no-extra-mode selector is parent-signed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4469_2_no_second_channel_parent_signed",
            "claim": "MTS parent actually signs no second curvature/scalar channel",
            "gate_pass": no_second_signed,
            "claim_allowed": False,
            "detail": "current selector assumptions remain not parent-derived",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4469_3_finite_coefficient_pack_ready",
            "claim": "finite c_R2_eff/C_total branch is score-ready",
            "gate_pass": finite_pack_ready,
            "claim_allowed": False,
            "detail": "D0/D2, c_R2_eff, C_total, live curve and PPN projection remain missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4469_4_R10_pressure_guard",
            "claim": "universal metric scalar is safe by default",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "pressure row shows alpha=1/3 exceeds review-candidate bound" if pressure_has_guard else "pressure guard missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4469_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to public/local-GR evidence",
            "gate_pass": no_claims,
            "claim_allowed": False,
            "detail": "4469 is a conditional theorem and finite-pack staging checkpoint",
            "valid_for_claim": False,
        },
    ]
