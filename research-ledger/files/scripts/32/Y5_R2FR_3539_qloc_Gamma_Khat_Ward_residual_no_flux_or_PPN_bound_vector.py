from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
LOCAL_BOUNDS = ROOT / "source-intake" / "local_bounds"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3539-Y5-R2FR-qloc-Gamma-Khat-Ward-residual-no-flux-or-PPN-bound-vector.md"
CANONICAL_STATUS = OUT / "P8_local_GR_qloc_Gamma_Khat_Ward_status.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3539": {"path": Path(__file__).resolve(), "role": "3539 generator"},
    "doc_3538": {
        "path": ROOT / "3538-Y5-R2FR-observed-flow-coframe-stationary-branch-ownership-or-PPN-vector-bounds.md",
        "role": "observed-flow/stationary branch handoff",
    },
    "next_3538": {
        "path": OUT / "P8_Y5_R2FR_3538_NEXT_TARGET.csv",
        "role": "selected qloc/Gamma-Khat next target",
    },
    "ppn_vector_3538": {
        "path": OUT / "P8_Y5_R2FR_3538_PPN_VECTOR_BOUND_ROWS.csv",
        "role": "surviving flow/domain PPN vector rows",
    },
    "symbol_map": {
        "path": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
        "role": "Gamma/Khat/q_loc/P_loc symbol-action map",
    },
    "first_variation_gates": {
        "path": OUT / "P8_MTS_SYMBOL_FIRST_VARIATION_GATES.csv",
        "role": "first-variation claim gate for Gamma/Khat/q_loc",
    },
    "keep_kill": {
        "path": OUT / "P8_MTS_SYMBOL_KEEP_KILL_RULES.csv",
        "role": "q_loc keep/kill rule: Ward residual or explicit bound only",
    },
    "gk_candidates": {
        "path": OUT / "P8_GK_STRESS_ACTION_CANDIDATES.csv",
        "role": "metric-response scalar-density candidate action",
    },
    "gk_decision": {
        "path": OUT / "P8_GK_STRESS_ACTION_DECISION.csv",
        "role": "prior GK action decision",
    },
    "gk_contract": {
        "path": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
        "role": "scalar-density/Khat metric-response/Ward contract",
    },
    "gk_match_audit": {
        "path": OUT / "P8_GK_METRIC_RESPONSE_MATCH_AUDIT.csv",
        "role": "current corpus match failures for Gamma/Khat",
    },
    "gk_source_evidence": {
        "path": OUT / "P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
        "role": "evidence for q_loc source identity and limits",
    },
    "gk_residual_branch": {
        "path": OUT / "P8_GK_RESIDUAL_BOUND_BRANCH.csv",
        "role": "fallback if metric response is unsigned",
    },
    "domain_alpha3": {
        "path": OUT / "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv",
        "role": "domain alpha3 no-leak warning",
    },
    "boundary_alpha3": {
        "path": OUT / "P8_BOUNDARY_ALPHA3_NOFLUX_THEOREM_ATTEMPT.csv",
        "role": "boundary alpha3 no-flux warning",
    },
    "prediction_template": {
        "path": OUT / "MTS_local_residual_predictions_TEMPLATE.csv",
        "role": "local residual prediction rows R0-R11",
    },
    "r11_vector": {
        "path": OUT / "R11_nonEH_operator_vector_executable.csv",
        "role": "R11 non-EH operator executable vector",
    },
    "local_bounds": {
        "path": LOCAL_BOUNDS / "local_bound_claims.csv",
        "role": "empirical WEP/PPN/Gdot/R10/R11 bound ledger",
    },
}


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_escape(value: Any) -> str:
    return str(value).replace("\n", "<br>").replace("|", "\\|")


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    if not rows:
        return "_No rows._"
    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(markdown_escape(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(item["path"]),
            "exists": bool_text(item["path"].exists()),
            "role": item["role"],
            "valid_for_claim": "False",
        }
        for source_id, item in SOURCES.items()
    ]


def ward_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "WRT3539_0_define_SGK",
            "object": "S_GK",
            "mathematical_statement": "S_GK[g,Phi] = - integral_M sqrt(-g) Gamma_eff(g,Phi,nabla Phi,D,...)",
            "derived_consequence": "Gamma_eff is no longer a fitted readout; it is a parent scalar-density contribution to the action.",
            "required_signature": "Gamma_eff formula, units, field arguments, covariance, background subtraction, source path",
            "current_status": "EXACT_CONTRACT_NOT_PARENT_SIGNED",
            "claim_allowed": "False",
        },
        {
            "route_id": "WRT3539_1_metric_response",
            "object": "K_hat^{mu nu}",
            "mathematical_statement": "delta(sqrt(-g) Gamma_eff) = 1/2 sqrt(-g) (Gamma_eff g^{mu nu} - K_metric^{mu nu}) delta g_{mu nu} + sqrt(-g) E_A delta Phi^A + dTheta_GK",
            "derived_consequence": "K_hat must equal K_metric, including derivative and boundary terms, before q_loc can be a Ward residual.",
            "required_signature": "K_hat^{mu nu}=K_metric^{mu nu}[Gamma_eff] with fixed sign/volume convention",
            "current_status": "NOT_MATCHED_TO_CURRENT_MTS_SYMBOLS",
            "claim_allowed": "False",
        },
        {
            "route_id": "WRT3539_2_diffeomorphism_Ward",
            "object": "Ward identity",
            "mathematical_statement": "0 = delta_xi S_GK = integral sqrt(-g)[-nabla_mu T_GK^{mu nu} + E_A R_A^nu + B_GK^nu] xi_nu",
            "derived_consequence": "nabla_mu T_GK^{mu nu} = E_A R_A^nu + B_GK^nu, where B_GK is boundary/nonlocal/domain flux.",
            "required_signature": "diffeomorphism-invariant SGK, field transformation generators R_A^nu, explicit boundary current",
            "current_status": "WARD_THEOREM_FORM_WRITTEN",
            "claim_allowed": "False",
        },
        {
            "route_id": "WRT3539_3_qloc_identity",
            "object": "q_loc^nu",
            "mathematical_statement": "q_loc^nu = P_loc^nu_rho(nabla^rho Gamma_eff - nabla_mu K_hat^{mu rho})",
            "derived_consequence": "If K_hat=K_metric then q_loc^nu = P_loc^nu_rho(E_A R_A^rho + B_GK^rho) up to the chosen stress sign convention.",
            "required_signature": "same P_loc as observed local quotient; no data-chosen projection; convention locked",
            "current_status": "EXACT_IF_METRIC_RESPONSE_MATCHES",
            "claim_allowed": "False",
        },
        {
            "route_id": "WRT3539_4_on_shell_no_flux_zero",
            "object": "compact local vacuum branch",
            "mathematical_statement": "E_A=0, B_GK^nu=0, Delta_K^{mu nu}:=K_hat^{mu nu}-K_metric^{mu nu}=0 => q_loc^nu=0",
            "derived_consequence": "This is the legal plateau replacement: q_loc goes silent because Euler/Ward/no-flux clauses force it, not because it was assumed.",
            "required_signature": "Euler equations, boundary/domain no-flux, Khat response equality, P_loc ownership",
            "current_status": "CONDITIONAL_THEOREM_NOT_CLAIM",
            "claim_allowed": "False",
        },
        {
            "route_id": "WRT3539_5_first_variation_silence",
            "object": "linear local residual",
            "mathematical_statement": "partial_A T_GK^{mu nu}(Phi0)=0 and partial_A B_GK^nu(Phi0)=0 => delta q_loc^nu|Phi0=0",
            "derived_consequence": "Linear PPN/fifth-force/source-normalization leakage is removed only if the double-zero is parent-owned.",
            "required_signature": "Gamma fixed-point expansion, positive Hessian or representation theorem, boundary first-variation zero",
            "current_status": "DOUBLE_ZERO_GATE_OPEN",
            "claim_allowed": "False",
        },
    ]


def qloc_zero_test_rows() -> list[dict[str, Any]]:
    return [
        {
            "test_id": "QZT3539_0_scalar_density_owner",
            "clause": "Gamma_eff scalar action-density owner",
            "pass_condition": "Gamma_eff = Gamma_eff(g,Phi,nabla Phi,D,topology) is declared in the parent action with units and no post-fit selector.",
            "current_evidence": "GK contract requires this; match audit did not find it in current MTS symbols.",
            "result": "FAIL_CURRENT_CLAIM",
            "residual_if_failed": "Gamma behaves as a phenomenological/local-load readout; q_loc stays physical.",
            "claim_allowed": "False",
        },
        {
            "test_id": "QZT3539_1_Khat_response",
            "clause": "K_hat is exact metric response of Gamma_eff",
            "pass_condition": "K_hat^{mu nu}=K_metric^{mu nu}[Gamma_eff], including derivative and boundary terms under one sign convention.",
            "current_evidence": "GK candidates define the route; GK match audit did not find the equality.",
            "result": "FAIL_CURRENT_CLAIM",
            "residual_if_failed": "Delta_K^{mu nu}=K_hat^{mu nu}-K_metric^{mu nu} sources q_loc through -P_loc nabla_mu Delta_K.",
            "claim_allowed": "False",
        },
        {
            "test_id": "QZT3539_2_Ward_specificity",
            "clause": "specific Ward identity for S_GK",
            "pass_condition": "Diffeomorphism variation of the same S_GK produces exactly nabla Gamma_eff - div K_hat plus Euler/boundary terms.",
            "current_evidence": "Generic Ward/Bianchi ledgers exist; specific S_GK identity is conditional on QZT3539_0 and QZT3539_1.",
            "result": "CONDITIONAL",
            "residual_if_failed": "Ward ownership only tells where leakage goes; it does not make q_loc zero.",
            "claim_allowed": "False",
        },
        {
            "test_id": "QZT3539_3_Euler_shell",
            "clause": "extra fields are on shell locally",
            "pass_condition": "E_A=0 on the compact local branch, with source terms absent or Hilbert-owned.",
            "current_evidence": "3535/3536/3537 provide conditional local-zero machinery, not a signed Gamma/Khat Euler system.",
            "result": "CONDITIONAL_NOT_SIGNED",
            "residual_if_failed": "E_A R_A^nu is a finite local force/source residual.",
            "claim_allowed": "False",
        },
        {
            "test_id": "QZT3539_4_boundary_domain_no_flux",
            "clause": "boundary/domain projection silence",
            "pass_condition": "B_GK^nu=0 or exact term annihilated by P_loc for the local branch.",
            "current_evidence": "boundary/domain alpha3 files keep no-flux conditional and not parent-owned.",
            "result": "OPEN_HIGH_PRESSURE",
            "residual_if_failed": "R7 alpha3, R8 xi, R11 boundary/domain operators remain active.",
            "claim_allowed": "False",
        },
        {
            "test_id": "QZT3539_5_Ploc_owner",
            "clause": "P_loc is parent-owned",
            "pass_condition": "P_loc descends from the same observed quotient/selector as matter and local rods/clocks.",
            "current_evidence": "symbol map says P_loc is open; 3538 gives same-stack condition but not full parent signature.",
            "result": "CONDITIONAL_NOT_SIGNED",
            "residual_if_failed": "Projection can hide force components; bounds must use full vector envelope.",
            "claim_allowed": "False",
        },
        {
            "test_id": "QZT3539_6_units_weak_field_map",
            "clause": "q_loc has units and weak-field observable map",
            "pass_condition": "q_loc profile maps to WEP/PPN/Gdot/R10/R11 rows with sourced coefficients.",
            "current_evidence": "template and local bounds exist, but q_loc-to-observable coefficients are not live numeric rows.",
            "result": "FAIL_CURRENT_CLAIM",
            "residual_if_failed": "Use nonclaim bound-vector rows, not local-GR pass language.",
            "claim_allowed": "False",
        },
        {
            "test_id": "QZT3539_7_verdict",
            "clause": "q_loc theorem-zero",
            "pass_condition": "all QZT3539_0 through QZT3539_6 are signed.",
            "current_evidence": "The theorem route is exact, but multiple parent signatures are unsigned.",
            "result": "NOT_CLAIMED",
            "residual_if_failed": "q_loc is retained as explicit PPN/local-bound vector.",
            "claim_allowed": "False",
        },
    ]


def profile_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "law_id": "QPL3539_0_exact_profile",
            "quantity": "physical q_loc profile",
            "formula": "q_loc^nu(x)=P_loc^nu_rho[E_A(x) R_A^rho(x)+B_GK^rho(x)-nabla_mu Delta_K^{mu rho}(x)]",
            "interpretation": "The local force is the sum of Euler leakage, boundary/domain flux, and metric-response mismatch.",
            "current_status": "DERIVED_CONDITIONAL_FORM",
            "valid_for_claim": "False",
        },
        {
            "law_id": "QPL3539_1_norm_bound",
            "quantity": "local amplitude envelope",
            "formula": "||q_loc|| <= ||P_loc|| [sum_A ||E_A|| ||R_A|| + ||B_GK|| + ||nabla Delta_K||]",
            "interpretation": "This is the clean bound target: zero every term by theorem, or source each term numerically.",
            "current_status": "BOUND_FORM_READY_COEFFICIENTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "law_id": "QPL3539_2_mass_gap_tail",
            "quantity": "finite-range exterior tail",
            "formula": "If L2 = 1/2 Z_A (partial Y_A)^2 + 1/2 M_A^2 Y_A^2 then Y_A(r)~C_A exp(-r/lambda_A)/r, lambda_A=sqrt(Z_A/M_A^2).",
            "interpretation": "R10 fifth-force rows require Z_A, M_A^2, source charge C_A, and q_loc-to-alpha(lambda) normalization.",
            "current_status": "ROUTE_TO_R10_NOT_NUMERIC_CLAIM",
            "valid_for_claim": "False",
        },
        {
            "law_id": "QPL3539_3_double_zero_linear_silence",
            "quantity": "linear PPN residual",
            "formula": "If Gamma_eff=Gamma0+1/2 H_AB Y^A Y^B+O(Y^3), K_hat=K_metric, and B_GK=O(Y^2), then q_loc=O(Y nabla Y)+O(Y^2).",
            "interpretation": "This is the serious route to first-order silence; it needs the Gamma fixed-point expansion and boundary first-variation zero.",
            "current_status": "PROMISING_BUT_UNSIGNED",
            "valid_for_claim": "False",
        },
        {
            "law_id": "QPL3539_4_PPN_vector_map",
            "quantity": "PPN residual vector",
            "formula": "p_qloc = M_PPN[q_loc] = (eta_source, alpha1, alpha2, alpha3, xi, Gdot/G, alpha(lambda), c_R11)",
            "interpretation": "The next computational gate is to fill or theorem-zero the linear map M_PPN component by component.",
            "current_status": "MAP_DECLARED_NOT_FILLED",
            "valid_for_claim": "False",
        },
    ]


def ppn_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "QBV3539_0_R0_direct_geometry",
            "observable_row": "R0_identity_coframe_direct",
            "residual_component": "direct geometry/coframe slip from q_loc",
            "required_input": "q_loc-induced differential acceleration in observed coframe; compare to MICROSCOPE eta <= 2.8e-15",
            "available_bound": "2.8e-15 dimensionless",
            "current_status": "NO_QLOC_TO_ETA_GEOM_COEFFICIENT",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QBV3539_1_R1_source_charge",
            "observable_row": "R1_WEP_source_charge",
            "residual_component": "source-normalization force charge",
            "required_input": "species/material derivative of active source charge induced by q_loc or Gamma/Khat mismatch",
            "available_bound": "2.8e-15 dimensionless proxy",
            "current_status": "SOURCE_CHARGE_MAP_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QBV3539_2_R3_R4_metric",
            "observable_row": "R3_gamma;R4_beta",
            "residual_component": "weak-field metric tail",
            "required_input": "solve metric perturbation sourced by q_loc stress/residual and extract gamma-1, beta-1",
            "available_bound": "gamma:2.3e-5; beta:7.8e-5",
            "current_status": "WEAK_FIELD_SOLVER_MAP_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QBV3539_3_R5_alpha1",
            "observable_row": "R5_alpha1",
            "residual_component": "preferred-frame vector from projected q_loc",
            "required_input": "alpha1 = C_alpha1^nu q_loc_nu or theorem-zero vector component",
            "available_bound": "abs(alpha1)<=1e-4",
            "current_status": "VECTOR_COEFFICIENT_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QBV3539_4_R6_alpha2",
            "observable_row": "R6_alpha2",
            "residual_component": "preferred-frame/vector quadrupole from q_loc",
            "required_input": "alpha2 = C_alpha2[q_loc,Q_STF,domain vector] or theorem-zero",
            "available_bound": "abs(alpha2)<=2e-9",
            "current_status": "VECTOR_QUADRUPOLE_COEFFICIENT_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QBV3539_5_R7_alpha3",
            "observable_row": "R7_alpha3",
            "residual_component": "momentum-nonconservation/self-acceleration flux",
            "required_input": "alpha3 = C_alpha3^nu q_loc_nu + C_boundary B_GK + C_domain F_D or theorem-zero no-flux",
            "available_bound": "abs(alpha3)<=4e-20",
            "current_status": "HIGHEST_PRESSURE_NOT_SCOREABLE",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QBV3539_6_R8_xi",
            "observable_row": "R8_xi",
            "residual_component": "preferred-location/anisotropic q_loc coupling",
            "required_input": "xi coefficient for anisotropic exterior environment or proof q_loc has no STF/preferred-location piece",
            "available_bound": "abs(xi)<=4e-9",
            "current_status": "ANISOTROPY_COEFFICIENT_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QBV3539_7_R9_Gdot",
            "observable_row": "R9_Gdot",
            "residual_component": "time drift of source normalization or Gamma/Khat background",
            "required_input": "d ln(G_eff M_eff)/dt induced by q_loc branch",
            "available_bound": "9.6e-15 yr^-1",
            "current_status": "DRIFT_COEFFICIENT_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QBV3539_8_R10_fifth_force",
            "observable_row": "R10_fifth_force",
            "residual_component": "finite-range q_loc/Y_A tail",
            "required_input": "Z_A, M_A^2, lambda_A, source charge C_A, alpha(lambda) curve comparison",
            "available_bound": "alpha(lambda) curve required",
            "current_status": "R10_NUMERIC_PARENT_INPUTS_MISSING",
            "valid_for_claim": "False",
        },
        {
            "bound_id": "QBV3539_9_R11_operator_vector",
            "observable_row": "R11_EH_operator_ledger",
            "residual_component": "unfactored non-EH operators generated by Gamma/Khat mismatch or boundary current",
            "required_input": "operator coefficient vector with units, normalization, and weak-field projection",
            "available_bound": "symbolic operator ledger only",
            "current_status": "R11_VECTOR_HAS_MISSING_ROWS",
            "valid_for_claim": "False",
        },
    ]


def gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3539_0_derivation_first",
            "gate": "q_loc zero must be derived from S_GK metric response and Ward/Euler/no-flux identity",
            "current_result": "conditional theorem written",
            "blocks": "plateau axiom, fitted cancellation, bookkeeping stress",
            "claim_allowed": "False",
        },
        {
            "gate_id": "G3539_1_metric_response_gap",
            "gate": "Delta_K=0 must be proved",
            "current_result": "not matched in current corpus",
            "blocks": "Gamma/Khat independent-knob local-GR pass",
            "claim_allowed": "False",
        },
        {
            "gate_id": "G3539_2_boundary_flux_gap",
            "gate": "B_GK=0 or P_loc B_GK=0 must be proved",
            "current_result": "open; alpha3 pressure remains",
            "blocks": "R7 alpha3 and domain/boundary no-flux claim",
            "claim_allowed": "False",
        },
        {
            "gate_id": "G3539_3_PPN_bound_vector",
            "gate": "surviving q_loc components must map to R0/R1/R3/R4/R5/R6/R7/R8/R9/R10/R11",
            "current_result": "nonclaim rows emitted",
            "blocks": "unscored local-GR/PPN pass",
            "claim_allowed": "False",
        },
        {
            "gate_id": "G3539_4_local_GR_status",
            "gate": "local GR/Newton reduction can reopen only after q_loc theorem-zero or scored bound vector",
            "current_result": "blocked but sharper",
            "blocks": "local-GR claim",
            "claim_allowed": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3539_0_actual_derivation_obtained",
            "decision": "Use the metric-response Ward identity as the exact q_loc route.",
            "rationale": "It directly rewrites q_loc as Euler leakage plus boundary/domain flux plus Khat-response mismatch.",
            "effect": "The local force problem is no longer vague: prove E_A=0, B_GK=0, Delta_K=0 or bound those three terms.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3539_1_no_plateau",
            "decision": "Do not set q_loc=0 by a local-vacuum plateau axiom.",
            "rationale": "The Ward identity gives a real mechanism; if any clause fails, q_loc is a physical residual.",
            "effect": "The framework stays engineering-honest and testable.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3539_2_bound_vector_now_explicit",
            "decision": "Retain q_loc as explicit PPN/local-bound vector until the parent action signs the theorem.",
            "rationale": "R7 alpha3, R10 fifth force, and R11 operator rows are too tight to handwave.",
            "effect": "Next work can fill coefficients instead of repeating missing-premise audits.",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3539_3_next",
            "decision": "Attack the Gamma_eff scalar-density owner and Khat response equality next.",
            "rationale": "Delta_K=0 is the shortest leap from contract to actual local-force silence.",
            "effect": "3540 should either construct the parent-owned Gamma/Khat pair or create the q_loc bound runner inputs.",
            "claim_allowed": "False",
        },
    ]


def status_rows() -> list[dict[str, Any]]:
    return [
        {
            "status_id": "STAT3539_0_ward_route",
            "quantity": "q_loc_Ward_identity",
            "value": "exact_conditional_theorem",
            "meaning": "q_loc can be derived as a projected Ward/Euler/boundary residual if Gamma/Khat are one variational object",
            "claim_effect": "route is real, but not parent-signed",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3539_1_profile",
            "quantity": "physical_q_loc_profile",
            "value": "P_loc(E_A R_A + B_GK - div Delta_K)",
            "meaning": "the surviving local force has three explicit sources: Euler leakage, boundary/domain flux, metric-response mismatch",
            "claim_effect": "bound or theorem-zero each source",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3539_2_claim",
            "quantity": "local_GR_PPN_claim",
            "value": "blocked",
            "meaning": "q_loc theorem-zero and bound-vector scoring are not claim-ready",
            "claim_effect": "no local-GR/Newton/PPN pass from 3539",
            "valid_for_claim": "False",
        },
        {
            "status_id": "STAT3539_3_best_next",
            "quantity": "next_best_target",
            "value": "Gamma_eff_scalar_density_owner_or_qloc_bound_runner",
            "meaning": "derive Gamma/Khat as a parent response pair, or start filling the coefficient vector",
            "claim_effect": "pushes forward rather than re-auditing",
            "valid_for_claim": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3540-Y5-R2FR-Gamma-eff-scalar-density-owner-or-qloc-bound-runner.md",
            "next_script": "scripts/Y5_R2FR_3540_Gamma_eff_scalar_density_owner_or_qloc_bound_runner.py",
            "objective": "Try to construct a parent-owned Gamma_eff scalar density whose metric response is K_hat; if Delta_K cannot be killed, instantiate the q_loc bound runner with Euler, boundary, Delta_K, PPN, R10 and R11 coefficient rows.",
            "success_gate": "Either Delta_K=0 and q_loc reduces to on-shell no-flux Ward silence, or q_loc coefficients are ready for local WEP/PPN/Gdot/R10/R11 scoring.",
            "why_next": "3539 turned the local-force problem into three explicit terms; Delta_K is the shortest unsolved structural term.",
            "claim_allowed": "False",
        }
    ]


def validate(
    outputs: dict[str, Path],
    sources: list[dict[str, Any]],
    ward_routes: list[dict[str, Any]],
    zero_tests: list[dict[str, Any]],
    profile_laws: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []
    route_ids = {row["route_id"] for row in ward_routes}
    test_ids = {row["test_id"] for row in zero_tests}
    bound_rows = {row["observable_row"] for row in bounds}
    checks.append({"check_id": "VAL3539_0_sources_exist", "passed": bool_text(all(row["exists"] == "True" for row in sources)), "detail": "all cited source paths exist", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3539_1_metric_response_route_present", "passed": bool_text({"WRT3539_0_define_SGK", "WRT3539_1_metric_response", "WRT3539_2_diffeomorphism_Ward", "WRT3539_3_qloc_identity"} <= route_ids), "detail": "SGK, Khat response, Ward identity and q_loc identity rows present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3539_2_zero_tests_cover_hard_clauses", "passed": bool_text({"QZT3539_0_scalar_density_owner", "QZT3539_1_Khat_response", "QZT3539_4_boundary_domain_no_flux", "QZT3539_5_Ploc_owner", "QZT3539_6_units_weak_field_map"} <= test_ids), "detail": "Gamma, Khat, boundary, P_loc and units tests present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3539_3_profile_has_three_source_terms", "passed": bool_text(any(row["law_id"] == "QPL3539_0_exact_profile" and "E_A" in row["formula"] and "B_GK" in row["formula"] and "Delta_K" in row["formula"] for row in profile_laws)), "detail": "q_loc profile includes Euler, boundary and Khat-mismatch terms", "valid_for_claim": "False"})
    required_bounds = {"R0_identity_coframe_direct", "R1_WEP_source_charge", "R3_gamma;R4_beta", "R5_alpha1", "R6_alpha2", "R7_alpha3", "R8_xi", "R9_Gdot", "R10_fifth_force", "R11_EH_operator_ledger"}
    checks.append({"check_id": "VAL3539_4_bound_vector_covers_local_rows", "passed": bool_text(required_bounds <= bound_rows), "detail": "R0/R1/R3/R4/R5/R6/R7/R8/R9/R10/R11 rows present", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3539_5_alpha3_pressure_retained", "passed": bool_text(any(row["observable_row"] == "R7_alpha3" and "4e-20" in row["available_bound"] and row["valid_for_claim"] == "False" for row in bounds)), "detail": "alpha3 4e-20 row retained as nonclaim", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3539_6_no_claims_promoted", "passed": bool_text(all(row.get("valid_for_claim", "False") == "False" for row in sources + profile_laws + bounds + status) and all(row.get("claim_allowed", "False") == "False" for row in ward_routes + zero_tests + gates + decisions + next_rows)), "detail": "no local-GR/PPN/q_loc-zero claim promoted", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3539_7_next_target_selected", "passed": bool_text(next_rows[0]["next_doc"].startswith("3540-Y5-R2FR-Gamma-eff")), "detail": "3540 Gamma_eff scalar-density/Khat response target selected", "valid_for_claim": "False"})
    parse_ok = True
    parsed: list[str] = []
    for name, path in outputs.items():
        if name in {"doc", "validation"}:
            continue
        try:
            read_csv_rows(path)
            parsed.append(name)
        except Exception:
            parse_ok = False
            parsed.append(f"{name}:PARSE_FAIL")
    checks.append({"check_id": "VAL3539_8_csvs_parse", "passed": bool_text(parse_ok), "detail": "; ".join(parsed), "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3539_9_outputs_stay_in_post_checkpoint_work", "passed": bool_text(all(ROOT in path.parents or path == DOC for path in outputs.values())), "detail": f"root={ROOT}", "valid_for_claim": "False"})
    checks.append({"check_id": "VAL3539_10_formalization_workbench_not_targeted", "passed": bool_text(all(FORMALIZATION not in path.parents for path in outputs.values())), "detail": str(FORMALIZATION), "valid_for_claim": "False"})
    passed = all(row["passed"] == "True" for row in checks)
    checks.append({"check_id": "VAL3539_SUMMARY", "passed": bool_text(passed), "detail": "PASS" if passed else "FAIL", "valid_for_claim": "False"})
    return checks


def write_doc(
    sources: list[dict[str, Any]],
    ward_routes: list[dict[str, Any]],
    zero_tests: list[dict[str, Any]],
    profile_laws: list[dict[str, Any]],
    bounds: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    status: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3539 - q_loc/Gamma-Khat Ward Residual, No-Flux, Or PPN Bound Vector

## Summary
- **Real derivation step:** `q_loc^nu` has an exact conditional identity if `Gamma_eff` is a scalar action density and `K_hat` is its metric response.
- **Core law:** `q_loc = P_loc(E_A R_A + B_GK - div Delta_K)`, where `Delta_K = K_hat - K_metric[Gamma_eff]`.
- **Legal zero route:** `q_loc -> 0` follows only from `E_A=0`, `B_GK=0`, `Delta_K=0`, and parent-owned `P_loc`.
- **No plateau axiom:** local silence is not assumed; unsigned terms become physical WEP/PPN/Gdot/R10/R11 residuals.
- **Next hinge:** either construct the parent-owned `Gamma_eff/K_hat` response pair, or start filling the coefficient vector.

## Derivation
Start with a candidate local extra-sector action

`S_GK[g,Phi] = - integral sqrt(-g) Gamma_eff(g,Phi,nabla Phi,D,...)`.

Define the metric response by

`delta(sqrt(-g) Gamma_eff) = 1/2 sqrt(-g) (Gamma_eff g^{{mu nu}} - K_metric^{{mu nu}}) delta g_{{mu nu}} + sqrt(-g) E_A delta Phi^A + dTheta_GK`.

If `K_hat = K_metric`, then `T_GK^{{mu nu}} = Gamma_eff g^{{mu nu}} - K_hat^{{mu nu}}` is one variational object. Diffeomorphism invariance gives

`nabla_mu T_GK^{{mu nu}} = E_A R_A^nu + B_GK^nu`.

Since `nabla_mu(Gamma_eff g^{{mu nu}})=nabla^nu Gamma_eff`,

`nabla^nu Gamma_eff - nabla_mu K_hat^{{mu nu}} = E_A R_A^nu + B_GK^nu - nabla_mu Delta_K^{{mu nu}}`,

with `Delta_K = K_hat - K_metric`. Therefore

`q_loc^nu = P_loc^nu_rho(E_A R_A^rho + B_GK^rho - nabla_mu Delta_K^{{mu rho}})`.

That is the exact mechanism we wanted. It is not yet a live local-GR claim because the current corpus does not parent-sign `Gamma_eff`, `K_hat=K_metric`, boundary/domain no-flux, or the weak-field coefficient map.

## Source Register
{markdown_table(sources, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Ward Route
{markdown_table(ward_routes, ["route_id", "object", "mathematical_statement", "derived_consequence", "required_signature", "current_status", "claim_allowed"])}

## q_loc Zero Tests
{markdown_table(zero_tests, ["test_id", "clause", "pass_condition", "current_evidence", "result", "residual_if_failed", "claim_allowed"])}

## Physical Profile Laws
{markdown_table(profile_laws, ["law_id", "quantity", "formula", "interpretation", "current_status", "valid_for_claim"])}

## PPN/Local Bound Vector
{markdown_table(bounds, ["bound_id", "observable_row", "residual_component", "required_input", "available_bound", "current_status", "valid_for_claim"])}

## Gates
{markdown_table(gates, ["gate_id", "gate", "current_result", "blocks", "claim_allowed"])}

## Decision Ledger
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Canonical Status
{markdown_table(status, ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sources = source_rows()
    ward_routes = ward_route_rows()
    zero_tests = qloc_zero_test_rows()
    profile_laws = profile_law_rows()
    bounds = ppn_bound_rows()
    gates = gate_rows()
    decisions = decision_rows()
    status = status_rows()
    next_rows = next_target_rows()
    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3539_SOURCE_REGISTER.csv",
        "ward_route": OUT / "P8_Y5_R2FR_3539_METRIC_RESPONSE_WARD_ROUTE.csv",
        "zero_tests": OUT / "P8_Y5_R2FR_3539_QLOC_ZERO_TESTS.csv",
        "profile_laws": OUT / "P8_Y5_R2FR_3539_QLOC_PROFILE_LAWS.csv",
        "ppn_bound_vector": OUT / "P8_Y5_R2FR_3539_PPN_BOUND_VECTOR.csv",
        "gates": OUT / "P8_Y5_R2FR_3539_GATES.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3539_DECISION_LEDGER.csv",
        "status": OUT / "P8_Y5_R2FR_3539_STATUS.csv",
        "canonical_status": CANONICAL_STATUS,
        "next_target": OUT / "P8_Y5_R2FR_3539_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3539_VALIDATION.csv",
        "doc": DOC,
    }
    write_csv(outputs["source_register"], sources, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(outputs["ward_route"], ward_routes, ["route_id", "object", "mathematical_statement", "derived_consequence", "required_signature", "current_status", "claim_allowed"])
    write_csv(outputs["zero_tests"], zero_tests, ["test_id", "clause", "pass_condition", "current_evidence", "result", "residual_if_failed", "claim_allowed"])
    write_csv(outputs["profile_laws"], profile_laws, ["law_id", "quantity", "formula", "interpretation", "current_status", "valid_for_claim"])
    write_csv(outputs["ppn_bound_vector"], bounds, ["bound_id", "observable_row", "residual_component", "required_input", "available_bound", "current_status", "valid_for_claim"])
    write_csv(outputs["gates"], gates, ["gate_id", "gate", "current_result", "blocks", "claim_allowed"])
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    status_fields = ["status_id", "quantity", "value", "meaning", "claim_effect", "valid_for_claim"]
    write_csv(outputs["status"], status, status_fields)
    write_csv(outputs["canonical_status"], status, status_fields)
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "why_next", "claim_allowed"])
    validation_rows = validate(outputs, sources, ward_routes, zero_tests, profile_laws, bounds, gates, decisions, status, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(sources, ward_routes, zero_tests, profile_laws, bounds, gates, decisions, status, next_rows, validation_rows)
    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
