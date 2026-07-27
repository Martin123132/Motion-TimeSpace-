from __future__ import annotations

import csv
import math
from pathlib import Path
from typing import Dict, Iterable, List


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


def as_float(value: object) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return parsed if math.isfinite(parsed) else None


def owner_theorem_rows() -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "OCT4461_0_connection_owner",
            "object": "Gamma_eff/omega_obs",
            "exact_statement": "If the parent local field inventory contains only the observed coframe/metric branch e_obs,g_obs and the transport connection is defined functorially as the spin/Levi-Civita connection omega[e_obs], then Gamma_eff = Gamma_LC[g_obs] and T=Q=0 are kinematic identities, not extra field equations.",
            "proof_move": "No independent connection variation exists; under a frame change e -> Lambda e the induced omega[e] transforms as a connection, and under refinement the pullback of e fixes the pullback of omega[e].",
            "must_be_parent_signed": "field inventory has no independent connection slot; no hypermomentum/current couples to an independent Gamma; all matter/readout branches use e_obs/g_obs",
            "if_not_signed": "retain C = Gamma_eff - Gamma_LC[g_obs] and the DeltaGamma source-current vector",
            "current_status": "CONDITIONAL_THEOREM_PARENT_INVENTORY_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "OCT4461_1_distortion_equation",
            "object": "independent connection residual C",
            "exact_statement": "If an independent connection is allowed, local GR follows only when the connection equation has the algebraic form M_C C = Delta_Gamma - B_C - P_projective with invertible positive M_C and all source/boundary/projective terms zero or gauge-silent.",
            "proof_move": "Decompose Gamma_eff = Gamma_LC[g_obs] + C; torsion and nonmetricity are linear projections of C, so C=0 forces the local Levi-Civita branch.",
            "must_be_parent_signed": "positive/invertible M_C; Delta_Gamma=0 or bounded; B_C=0 or boundary-silent; projective trace fixed or all-sector silent",
            "if_not_signed": "score the seven DeltaGamma components against WEP/clock/lightcone/R10/PPN/orbital arenas",
            "current_status": "RESIDUAL_VECTOR_BRANCH_RETAINED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "OCT4461_2_hinge_owner",
            "object": "B_h/A_h",
            "exact_statement": "If MTS owns an oriented local two-chain h and a descended coframe e_obs, then B_h^{IJ}=integral_h e_obs^I wedge e_obs^J and A_h=sqrt(|B_h.B_h|/2) are parent geometric objects.",
            "proof_move": "The coframe supplies the area bivector; the parent cell/refinement map must supply the face h, orientation, and shape/scale normalization.",
            "must_be_parent_signed": "cell-to-hinge complex; orientation/relative-chain rule; refinement law; ell_cell and shape factor or a proof they are gauge",
            "if_not_signed": "carry ell_cell and shape_factor as finite source inputs for c_R2_eff",
            "current_status": "CONDITIONAL_GEOMETRY_PARENT_CELL_LAW_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "OCT4461_3_log_holonomy_scalar",
            "object": "delta_h = <sigma_h,Log U_h>",
            "exact_statement": "On a small-curvature branch U_h=Pexp integral_{partial h} omega, Log U_h = F[omega](Sigma_h)+O(ell^3 nabla F + ell^4 F^2); contracting it with the parent-owned oriented hinge bivector gives a gauge-scalar signed deficit delta_h.",
            "proof_move": "Log U_h is adjoint-covariant and B_h is adjoint-covariant, so the invariant contraction is gauge-scalar; orientation reversal flips the sign of B_h and hence delta_h.",
            "must_be_parent_signed": "same parent owns omega, B_h, orientation, branch domain and boundary residual policy",
            "if_not_signed": "trace/norm holonomy costs remain legal and visible c2 is finite",
            "current_status": "MATH_OK_OWNER_UNSIGNED",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "theorem_id": "OCT4461_4_refinement_linearity",
            "object": "linear area-deficit action",
            "exact_statement": "If S_h = kappa A_h delta_h and refinement is cylindrical, then splitting one physical flux into n equal subhinges leaves the action invariant while any same-channel delta_h^2 term scales by 1/n and is not refinement-gauge invariant.",
            "proof_move": "Additivity gives sum_i delta_i=delta and sum_i A_i delta_i -> A delta on the same physical flux branch; sum_i delta_i^2=delta^2/n for equal subdivision.",
            "must_be_parent_signed": "quotient/projective refinement equivalence plus linear signed deficit owner",
            "if_not_signed": "finite c2 branch must be mapped to local scalar/spin residuals",
            "current_status": "EXACT_CONDITIONAL_ZERO_SELECTOR",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def scalaron_map_rows(d0_bound_m2: float | None, c_r2_bound_m2: float | None) -> List[Dict[str, object]]:
    lambda_from_d0_m = math.sqrt(d0_bound_m2 / 2.0) if d0_bound_m2 and d0_bound_m2 > 0 else ""
    lambda_from_cr2_m = math.sqrt(6.0 * c_r2_bound_m2) if c_r2_bound_m2 and c_r2_bound_m2 > 0 else ""
    return [
        {
            "map_id": "SM4461_0_basis_guard",
            "quantity": "D0,D2",
            "formula": "D0 = 12*c_R2 + c_Ric - 6*c_W - 8*c_Riem; D2 = -c_Ric - 2*c_W - 4*c_Riem",
            "condition": "pure f(R) scalaron map is valid only when D2=0 and non-R2 quadratic channels are parent-zero/topological/boundary-silent",
            "derived_value": "MISSING_PARENT_BASIS_COEFFICIENTS",
            "units": "m^2",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "map_id": "SM4461_1_c2_to_cR2",
            "quantity": "c_R2_eff",
            "formula": "c_R2_eff = xi_shape * c2_visible * ell_cell^2 / N_EH",
            "condition": "requires parent Phi''(0), cell scale, shape factor, continuum normalization and sign",
            "derived_value": "MISSING_c2_VISIBLE_ELL_CELL_SHAPE_FACTOR_N_EH",
            "units": "m^2",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "map_id": "SM4461_2_scalaron_range",
            "quantity": "lambda_R2",
            "formula": "lambda_R2 = sqrt(6*c_R2_eff) = sqrt(D0/2) in pure-R2 normalization",
            "condition": "requires c_R2_eff > 0; c_R2_eff < 0 is tachyonic for the scalar branch",
            "derived_value": lambda_from_d0_m,
            "units": "m_from_current_D0_bound_pressure_not_prediction",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "map_id": "SM4461_3_scalar_coupling",
            "quantity": "alpha_eff",
            "formula": "alpha_eff = C_matter^2/3 for a universal metric f(R)-like scalar; alpha_eff=0 only if the parent proves scalar/source decoupling",
            "condition": "requires universal matter coupling normalization C_matter and no screening/readout loophole",
            "derived_value": "MISSING_C_MATTER",
            "units": "dimensionless",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "map_id": "SM4461_4_yukawa_potential",
            "quantity": "Phi_Newton_residual",
            "formula": "V(r) = -G_eff*m1*m2/r * [1 + alpha_eff*exp(-r/lambda_R2)]",
            "condition": "valid for weak-field scalar branch with universal source coupling and no D2/spin-2 contamination",
            "derived_value": "SYMBOLIC_NONCLAIM",
            "units": "potential_energy",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "map_id": "SM4461_5_ppn_gamma",
            "quantity": "gamma(r)-1",
            "formula": "gamma(r)-1 = -2*alpha_eff*exp(-r/lambda_R2)/(1 + alpha_eff*exp(-r/lambda_R2))",
            "condition": "requires photon/lightcone branch to use the same observed metric and scalar coupling",
            "derived_value": "MISSING_LIGHTCONE_AND_C_MATTER",
            "units": "dimensionless",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "map_id": "SM4461_6_R10_check",
            "quantity": "R10_alpha_lambda_gate",
            "formula": "pass only if abs(alpha_eff) <= alpha_bound(lambda_R2) using a source-backed full bound curve",
            "condition": "requires real alpha_bound(lambda), C_matter, c_R2_eff and no fitted-G absorption",
            "derived_value": "CLAIM_BLOCKED_BY_MISSING_ALPHA_CURVE_AND_PARENT_COEFFICIENTS",
            "units": "dimensionless_vs_m",
            "score_ready": False,
            "valid_for_claim": False,
        },
        {
            "map_id": "SM4461_7_bound_pressure",
            "quantity": "current_bound_pressure",
            "formula": "from current private D0 bound: lambda_R2 <= sqrt(D0_bound/2); from pure R2: c_R2 <= D0_bound/12",
            "condition": "pressure only, because MTS has not sourced c_R2_eff",
            "derived_value": f"D0_bound_m2={d0_bound_m2}; c_R2_bound_m2={c_r2_bound_m2}; lambda_bound_m={lambda_from_d0_m}; lambda_bound_um={lambda_from_d0_m * 1e6 if isinstance(lambda_from_d0_m, float) else ''}",
            "units": "m^2_and_m",
            "score_ready": False,
            "valid_for_claim": False,
        },
    ]


def fork_decision_rows() -> List[Dict[str, object]]:
    return [
        {
            "fork_id": "FD4461_0_clean_GR_route",
            "route": "parent owns coframe-only or Palatini/Regge linear geometry",
            "requirement": "OCT4461_0/2/3/4 plus matter/source descent all parent-signed",
            "payoff": "Gamma becomes Levi-Civita, signed area-deficit action is linear, visible same-channel c2 is zero by refinement",
            "current_status": "NOT_PARENT_SIGNED",
            "next_action": "try to derive universal source coupling and Newton G normalization from the same parent action",
            "valid_for_claim": False,
        },
        {
            "fork_id": "FD4461_1_connection_residual_route",
            "route": "independent connection survives",
            "requirement": "DeltaGamma components, common units and P_WEP/P_clock/P_lightcone/P_R10/P_PPN/P_orbital projections",
            "payoff": "local branch becomes an empirical residual-vector test rather than an assumed GR limit",
            "current_status": "RETAINED",
            "next_action": "derive P_WEP/source-frame response before inserting coefficients",
            "valid_for_claim": False,
        },
        {
            "fork_id": "FD4461_2_finite_c2_scalaron_route",
            "route": "trace/norm/even holonomy or physical grain gives finite c2",
            "requirement": "c2_visible, ell_cell, shape factor, N_EH, C_matter and real alpha(lambda) bounds",
            "payoff": "finite curvature-square residual becomes testable through lambda_R2 and alpha_eff",
            "current_status": "FORMULA_MAP_FILLED_NONCLAIM",
            "next_action": "source c2/ell_cell/C_matter or prove one of them zero from parent theory",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows() -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "CG4461_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "source validation is performed by the generator",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4461_1_connection_owner_theorem",
            "claim": "exact connection-owner criterion written",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "criterion is conditional on parent field inventory/matter silence",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4461_2_hinge_log_derivation",
            "claim": "hinge/log scalar contraction and refinement linearity derived",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "math is written but parent ownership of cell/orientation/branch is unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4461_3_scalaron_map",
            "claim": "finite c2 branch has scalaron/Yukawa/PPN/R10 formulas",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "formula map is filled, but coefficients and coupling are missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4461_4_local_GR",
            "claim": "MTS reduces to local GR/Newton",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "parent ownership, source coupling, PPN/WEP and Newton normalization are not closed",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4461_5_next_target",
            "claim": "next source-coupling target is selected",
            "gate_pass": True,
            "claim_allowed": False,
            "detail": "4462-Y5-R2FR-universal-source-coupling-and-Newton-G-normalization-or-residual-bound-row.md",
            "valid_for_claim": False,
        },
    ]
