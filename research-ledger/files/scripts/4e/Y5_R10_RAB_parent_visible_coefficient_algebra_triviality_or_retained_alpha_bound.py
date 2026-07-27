from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE = ROOT / "source-intake" / "microscope"
COEFF = MICROSCOPE / "branch_locked_wep" / "coefficients"
QUARANTINE = MICROSCOPE / "quarantine" / "1468"
FORMALIZATION = ROOT.parent / "formalization-workbench"

DOC = ROOT / "1468-Y5-R10-RAB-parent-visible-coefficient-algebra-triviality-or-retained-alpha-bound.md"

BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
START_TS = datetime.now(timezone.utc).timestamp()

PREV_NEXT = OUT / "P8_Y5_R10_1467_NEXT_TARGET.csv"
PREV_VALIDATION = OUT / "P8_Y5_BRR545_1467_VALIDATION.csv"
PREV_VISIBLE = OUT / "P8_Y5_R10_1467_VISIBLE_COEFFICIENT_ALGEBRA_THEOREM_ATTEMPT.csv"
PREV_UNIQUE_EM = OUT / "P8_Y5_R10_1467_UNIQUE_EM_OWNER_NO_HIDDEN_F2_PROOF_ATTEMPT.csv"
PREV_NO_HIDDEN_F2 = OUT / "P8_Y5_R10_1467_NO_HIDDEN_F2_OPERATOR_CLASSIFICATION.csv"
PREV_COUNTERMODELS = OUT / "P8_Y5_R10_1467_COUNTERMODEL_LEDGER.csv"
PREV_GATES = OUT / "P8_Y5_R10_1467_REDUCTION_GATES.csv"
PREV_SIGNING = OUT / "P8_Y5_R10_1467_PARENT_SIGNING_DECISION.csv"

PARENT_990 = OUT / "P8_Y5_R10_990_PARENT_ACTION_CONTRACT.csv"
PARENT_1055 = OUT / "P8_Y5_R10_1055_PARENT_ACTION_CONTRACT_CANDIDATE.csv"
CONSTANT_SECTOR = OUT / "P8_constant_sector_universality_CONTRACT.csv"
GLOBAL_COUPLING = OUT / "P8_global_coupling_superselection_CONTRACT.csv"
NO_SPECIES_SOURCE = OUT / "P8_no_species_source_charge_CONTRACT.csv"
DOMAIN_ALPHA3 = OUT / "P8_DOMAIN_ALPHA3_NOLEAK_THEOREM_ATTEMPT.csv"
DOMAIN_NOVECTOR = OUT / "P8_DOMAIN_SELECTOR_NOVECTOR_THEOREM_ATTEMPT.csv"
DOMAIN_GATE = OUT / "P8_DOMAIN_SELECTOR_VECTOR_COEFFICIENT_GATE.csv"
ALPHA_BOUND_MATRIX = OUT / "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv"
CLOCK_PRODUCT_BOUND = OUT / "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv"
ALPHA_GATE_1396 = OUT / "P8_Y5_R10_1396_ALPHAEM_WEP_CLOCK_R10_GATE.csv"
BETA_SOURCE_ALPHA = OUT / "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_FINITE_BOUND_ROW.csv"
BOUND_1107 = OUT / "P8_Y5_R10_1107_ALPHA_BOUND_THRESHOLD_IMPORT.csv"
BOUND_1099 = OUT / "P8_Y5_R10_1099_ALPHA_PRODUCT_BOUND_IMPORT.csv"
R10_ALPHA_CANDIDATES = OUT / "P8_Y5_R10_1034_ALPHA_BOUND_CANDIDATE_ROWS.csv"
CLOCK_WAITSTATE_1324 = OUT / "P8_Y5_R10_1324_CLOCK_WAITSTATE_LEDGER.csv"

LIVE_OFFICIAL_READOUT = MICROSCOPE / "official_readout" / "P_WEP_K_CMSM_readout.csv"
LIVE_SOURCE_WORLD = MICROSCOPE / "source_worldtube" / "P_WEP_R_source_Earth_worldtube.csv"
LIVE_MATERIAL_TENSOR = MICROSCOPE / "derived" / "P_WEP_R_material_TA6V_minus_PtRh10_full_tensor.csv"
LIVE_CPARENT = COEFF / "C_parent_WEP_slot_import.csv"
LIVE_VISIBLE_ALGEBRA = COEFF / "visible_coefficient_algebra_parent_signed_import.csv"
LIVE_ALPHA_BOUND = COEFF / "alpha_constant_channel_claim_bound_import.csv"

SOURCE_REGISTER = OUT / "P8_Y5_R10_1468_SOURCE_REGISTER.csv"
ALGEBRA_TRIVIALITY = OUT / "P8_Y5_R10_1468_PARENT_VISIBLE_COEFFICIENT_ALGEBRA_TRIVIALITY_ATTEMPT.csv"
HIDDEN_INVARIANTS = OUT / "P8_Y5_R10_1468_HIDDEN_INVARIANT_ALGEBRA_AUDIT.csv"
VISIBLE_GRAMMAR = OUT / "P8_Y5_R10_1468_VISIBLE_ACTION_GRAMMAR_NO_EXTENSION_AUDIT.csv"
DERIVATION_DECISION = OUT / "P8_Y5_R10_1468_DERIVATION_DECISION.csv"
RETAINED_BOUNDS = OUT / "P8_Y5_R10_1468_RETAINED_ALPHA_CONSTANT_BOUND_ROWS.csv"
WAITSTATE = OUT / "P8_Y5_R10_1468_RETAINED_ALPHA_WAITSTATE_LEDGER.csv"
COUNTERMODELS = OUT / "P8_Y5_R10_1468_COUNTERMODEL_LEDGER.csv"
LIVE_GUARD = OUT / "P8_Y5_R10_1468_LIVE_IMPORT_GUARD.csv"
REDUCTION_GATES = OUT / "P8_Y5_R10_1468_REDUCTION_GATES.csv"
SIGNING_DECISION = OUT / "P8_Y5_R10_1468_PARENT_SIGNING_DECISION.csv"
DECISION_LEDGER = OUT / "P8_Y5_R10_1468_DECISION_LEDGER.csv"
NEXT_TARGET = OUT / "P8_Y5_R10_1468_NEXT_TARGET.csv"
VALIDATION = OUT / "P8_Y5_BRR545_1468_VALIDATION.csv"

QUAR_RETAINED_BOUNDS = QUARANTINE / "RETAINED_ALPHA_CONSTANT_BOUND_ROWS_NONCLAIM.csv"
QUAR_WAITSTATE = QUARANTINE / "RETAINED_ALPHA_WAITSTATE_LEDGER_NONCLAIM.csv"

BRANCH_ALGEBRA = COEFF / "parent_visible_coefficient_algebra_triviality_attempt_1468.csv"
BRANCH_RETAINED_BOUNDS = COEFF / "retained_alpha_constant_bound_rows_nonclaim_1468.csv"
BRANCH_SIGNING = COEFF / "C_parent_WEP_visible_algebra_signing_decision_1468.csv"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def truth(value: Any) -> bool:
    return str(value).strip().lower() in {"true", "1", "yes", "pass"}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def copy_branch(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def formalization_modified_count() -> int:
    if not FORMALIZATION.exists():
        return 0
    count = 0
    for path in FORMALIZATION.rglob("*"):
        if path.is_file() and path.stat().st_mtime >= START_TS:
            count += 1
    return count


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC1468_0_1467_next", PREV_NEXT, "1467 handoff to parent visible coefficient algebra"),
        ("SRC1468_1_1467_validation", PREV_VALIDATION, "1467 validation baseline"),
        ("SRC1468_2_1467_visible", PREV_VISIBLE, "visible coefficient algebra equivalence"),
        ("SRC1468_3_1467_unique_em", PREV_UNIQUE_EM, "unique EM owner reduction"),
        ("SRC1468_4_1467_no_hidden_f2", PREV_NO_HIDDEN_F2, "operator classification for hidden F2"),
        ("SRC1468_5_1467_countermodels", PREV_COUNTERMODELS, "surviving hidden coefficient countermodels"),
        ("SRC1468_6_1467_gates", PREV_GATES, "1467 gate pattern"),
        ("SRC1468_7_1467_signing", PREV_SIGNING, "1467 signing refusal"),
        ("SRC1468_8_parent_990", PARENT_990, "parent action contract"),
        ("SRC1468_9_parent_1055", PARENT_1055, "no mixed coefficients contract candidate"),
        ("SRC1468_10_constant_sector", CONSTANT_SECTOR, "constant-sector universality contract"),
        ("SRC1468_11_global_coupling", GLOBAL_COUPLING, "global coupling superselection contract"),
        ("SRC1468_12_no_species_source", NO_SPECIES_SOURCE, "no species source charge contract"),
        ("SRC1468_13_domain_alpha3", DOMAIN_ALPHA3, "no-leak theorem failure pattern"),
        ("SRC1468_14_domain_novector", DOMAIN_NOVECTOR, "covariance not absence analogy"),
        ("SRC1468_15_domain_gate", DOMAIN_GATE, "retained residual product gate pattern"),
        ("SRC1468_16_alpha_bound_matrix", ALPHA_BOUND_MATRIX, "alpha/mass/clock bound matrix"),
        ("SRC1468_17_clock_product", CLOCK_PRODUCT_BOUND, "clock alpha product bound"),
        ("SRC1468_18_alpha_gate", ALPHA_GATE_1396, "alphaEM/WEP/clock/R10 blocker gate"),
        ("SRC1468_19_beta_source_alpha", BETA_SOURCE_ALPHA, "finite beta_source_alpha target rows"),
        ("SRC1468_20_bound_1107", BOUND_1107, "alpha threshold/product bound imports"),
        ("SRC1468_21_bound_1099", BOUND_1099, "alpha product bound import"),
        ("SRC1468_22_R10_alpha", R10_ALPHA_CANDIDATES, "R10 alpha bound candidate rows"),
        ("SRC1468_23_clock_waitstate", CLOCK_WAITSTATE_1324, "clock waitstate missing-source ledger"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, usage in local_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": str(path.relative_to(ROOT)),
                "exists": path.exists(),
                "usage": usage,
                "valid_for_claim": False,
                "claim_allowed": False,
            }
        )
    return rows


def algebra_triviality_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "VAT1468_0_target",
            "claim": "parent visible coefficient algebra has no hidden maps",
            "mathematical_form": "C_vis := Coeff(O_vis) = q_loc^*C^\u221e(Q_obs) \u2297 pi_const^*C^\u221e(K_const), so Hom(C_hid,C_vis)=0",
            "result": "TARGET_RESTATED_AS_PARENT_GRAMMAR_THEOREM",
            "proof_status": "not_closed",
            "would_close_if": "parent proves visible action is a functor only of quotient observables and fixed constant sectors",
            "blocker": "MISSING_PARENT_VISIBLE_ACTION_GRAMMAR",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "VAT1468_1_descent_subtheorem",
            "claim": "descent implies vertical silence",
            "mathematical_form": "c in q^*C^\u221e(Q_obs)\u2297pi^*C^\u221e(K_const), v in ker(Dq)cap ker(Dpi) => L_v c=0",
            "result": "EXACT_SUBTHEOREM",
            "proof_status": "proved_conditional",
            "would_close_if": "every visible coefficient is known to live in this descended algebra",
            "blocker": "INCLUSION_OF_VISIBLE_COEFFICIENTS_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "VAT1468_2_invariant_algebra_route",
            "claim": "vertical invariance plus orbit transitivity can force descent",
            "mathematical_form": "if vertical automorphism orbits equal fibres of (q_loc,pi_const), then C^\u221e(C_parent)^V = q_loc^*C^\u221e(Q_obs)\u2297pi_const^*C^\u221e(K_const)",
            "result": "EXACT_CONDITIONAL_ROUTE",
            "proof_status": "route_identified_not_parent_signed",
            "would_close_if": "parent derives the vertical group action and proves no extra hidden invariants survive on fibres",
            "blocker": "MISSING_VERTICAL_ORBIT_TRANSITIVITY_AND_NO_EXTRA_INVARIANTS",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "VAT1468_3_no_extension_route",
            "claim": "visible action grammar can forbid hidden coefficient slots by construction",
            "mathematical_form": "S_parent = S_hidden[Phi_hid] + S_vis[q(Phi), pi_const(Phi), fields_vis], with Arg(S_vis) excluding Xhat",
            "result": "SUFFICIENT_CONTRACT_NOT_DERIVED",
            "proof_status": "contract_sufficient_not_parent_derived",
            "would_close_if": "MTS primitives derive this split rather than adopting it as hygiene",
            "blocker": "MISSING_NO_EXTENSION_THEOREM",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "step_id": "VAT1468_4_verdict",
            "claim": "current corpus parent-derives visible coefficient algebra triviality",
            "mathematical_form": "VAT1468_1 + VAT1468_2 or VAT1468_3 would close PAC1055_3",
            "result": "NOT_PARENT_DERIVED_KEEP_RETAINED_ALPHA_BOUND_ROWS",
            "proof_status": "failed_to_promote",
            "would_close_if": "hidden invariant algebra triviality or no-extension visible action grammar is derived from the parent action",
            "blocker": "VISIBLE_COEFFICIENT_ALGEBRA_UNSIGNED",
            "parent_signed": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def hidden_invariant_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "HIA1468_0_orbit_condition",
            "condition": "vertical orbits equal hidden fibres over (q_loc,pi_const)",
            "status": "UNSIGNED",
            "if_true": "all vertical-invariant coefficient functions descend to quotient/constants",
            "if_false": "extra fibre labels can feed visible coefficients",
            "counterexample": "C_parent=Q_obs x K_const x R_X with vertical action not transitive in X",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "HIA1468_1_extra_invariant",
            "condition": "no hidden scalar invariant Xhat independent of q_loc and pi_const",
            "status": "UNSIGNED",
            "if_true": "f(Xhat)F_Q^2 is not an available invariant coefficient",
            "if_false": "gauge/diffeo-invariant hidden alpha channel survives",
            "counterexample": "Xhat is a parent scalar singlet with L_v Xhat=0 but not q/pi data",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "HIA1468_2_covariance_not_enough",
            "condition": "diffeomorphism/gauge covariance alone excludes hidden coefficients",
            "status": "REJECTED_SHORTCUT",
            "if_true": "no extra parent grammar theorem would be needed",
            "if_false": "must use orbit/invariant algebra or no-extension theorem",
            "counterexample": "[g_*^-2 + epsilon f(Xhat)]F_Q^2 is gauge and diffeo covariant",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "audit_id": "HIA1468_3_connected_fibre",
            "condition": "fibres are connected and generated by allowed local vertical variations",
            "status": "UNSIGNED",
            "if_true": "local derivative silence can globalize to fibre-constant coefficients",
            "if_false": "discrete hidden sectors or topological labels can remain as constants in visible coefficients",
            "counterexample": "two disconnected hidden sectors with distinct Z_EM constants",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def visible_grammar_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "grammar_id": "VAG1468_0_visible_action_split",
            "required_clause": "visible action factors through q_loc and pi_const only",
            "current_status": "CONTRACT_CANDIDATE_NOT_DERIVED",
            "source_anchor": "PAC1055_6_single_parent_action; PAC1055_3_no_mixed_coefficients",
            "would_forbid": "f(Xhat)F_Q^2; m_A(Xhat); y_A(Xhat); clock_i(Xhat)",
            "fallback_if_missing": "retain alpha/mass/clock product-bound rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "grammar_id": "VAG1468_1_constant_sector_superselection",
            "required_clause": "K_const is superselected/global/topological, not a local hidden scalar bundle",
            "current_status": "NOT_PARENT_DERIVED",
            "source_anchor": "C1_superselection_independence; GS0_configuration_factorization",
            "would_forbid": "local running of alpha_EM, masses, clock constants, and kappa_eff from MTS invariants",
            "fallback_if_missing": "retain clock/fine-structure/Gdot/WEP residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "grammar_id": "VAG1468_2_no_spurion_extension",
            "required_clause": "hidden/projector/material variables cannot be promoted to spurion coefficients in S_vis",
            "current_status": "POLICY_ONLY_NOT_THEOREM",
            "source_anchor": "C2_no_direct_constant_vertices; S3_no_material_marker_extension",
            "would_forbid": "direct WEP/clock/fifth-force constant vertices",
            "fallback_if_missing": "create executable residual coefficients with source paths and units",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "grammar_id": "VAG1468_3_radiative_stability",
            "required_clause": "effective/readout maps preserve the same quotient-plus-constant coefficient algebra",
            "current_status": "REQUIRED_CLOSURE_NOT_DERIVED",
            "source_anchor": "PAC1055_5_radiative_readout_closure",
            "would_forbid": "Z_EM^eff(q,K,Xhat;mu), clock_i^eff(Xhat), mass_i^eff(Xhat)",
            "fallback_if_missing": "retain radiative/readout reentry residuals",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def derivation_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DER1468_0_exact_piece",
            "decision": "accept the exact descent subtheorem",
            "reason": "if coefficients already live in the quotient-plus-constant algebra, all hidden vertical derivatives vanish",
            "promotion_effect": "none by itself",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DER1468_1_failed_piece",
            "decision": "do not claim parent algebra triviality",
            "reason": "hidden invariant algebra triviality, vertical orbit transitivity, and no-extension visible grammar remain unsigned",
            "promotion_effect": "PAC1055_3 remains private contract/theorem target",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "DER1468_2_fallback",
            "decision": "retain alpha/constant channels as bound rows",
            "reason": "failed theorem-zero must become explicit residual products rather than hidden assumptions",
            "promotion_effect": "no score-ready row until MTS prediction values/provenance exist",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def retained_bound_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_row_id": "RAB1468_0_alphaEM_hidden_F2",
            "arena": "fine_structure_EM",
            "retained_quantity": "b_alpha_EM := L_v ln Z_EM or equivalent hidden EM kinetic coefficient response",
            "product_to_bound": "b_alpha_EM * tau_clock_or_local_hidden_flow",
            "comparison_source": "P8_Y5_R10_1052_ALPHA_CLOCK_PRODUCT_BOUND_LEDGER.csv:ACB1052_2",
            "available_bound_value": "2.1e-18",
            "bound_units": "yr^-1 product bound",
            "missing_mts_inputs": "standalone b_alpha_EM; tau_clock/local hidden flow; readout model; source path",
            "current_status": "RETAINED_BOUND_ROW_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_row_id": "RAB1468_1_WEP_alpha_product",
            "arena": "MICROSCOPE_WEP",
            "retained_quantity": "P_WEP_alpha or beta_source_alpha*b_alpha*tau_WEP",
            "product_to_bound": "DeltaQ_alpha_AB * beta_source_alpha * b_alpha * tau_WEP",
            "comparison_source": "P8_Y5_R10_1414_BETA_SOURCE_ALPHA_FINITE_BOUND_ROW.csv:BSB1414_1_alpha_only_target",
            "available_bound_value": "4.797780522732e-05",
            "bound_units": "dimensionless target only",
            "missing_mts_inputs": "parent basis map; beta_source_alpha; tau_WEP; material/readout composition matrix",
            "current_status": "TARGET_ONLY_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_row_id": "RAB1468_2_R10_alpha_lambda",
            "arena": "R10_short_range_fifth_force",
            "retained_quantity": "alpha_X(lambda_X) from hidden EM/mass coefficient channel",
            "product_to_bound": "K_X Qbar_source Qbar_test /(4*pi*Z_X*G_obs)",
            "comparison_source": "P8_Y5_R10_1034_ALPHA_BOUND_CANDIDATE_ROWS.csv:R10B1034_3_vector_review_candidate_summary",
            "available_bound_value": "review_candidate_curve_nonclaim",
            "bound_units": "dimensionless alpha(lambda)",
            "missing_mts_inputs": "lambda_X; Z_X; K_X; Qbar_source/test; official curve or QA-approved digitization",
            "current_status": "RETAINED_R10_BOUND_ROW_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_row_id": "RAB1468_3_mass_clock_coefficients",
            "arena": "mass_clock_constants",
            "retained_quantity": "m_A(Xhat), y_A(Xhat), clock_i(Xhat) coefficient leakage",
            "product_to_bound": "b_mu/b_nuc/b_clock_i times clock/local hidden flow",
            "comparison_source": "P8_Y5_R10_1048_ALPHA_MASS_CLOCK_BOUND_MATRIX.csv:BM1048_0_alpha_clock",
            "available_bound_value": "matrix_only_no_single_bound",
            "bound_units": "mixed; product-specific",
            "missing_mts_inputs": "coefficient definitions; sensitivity matrix; tau_clock; units; source paths",
            "current_status": "RETAINED_MATRIX_ROW_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "bound_row_id": "RAB1468_4_global_kappa_constant",
            "arena": "Newton_PPN_Gdot",
            "retained_quantity": "kappa_eff hidden/local dependence if constant-sector superselection fails",
            "product_to_bound": "dln_Geff_dt, partial_A ln G_eff, partial_r ln G_eff, alpha(lambda)",
            "comparison_source": "P8_global_coupling_superselection_CONTRACT.csv:GS7_scalar_branch_fallback",
            "available_bound_value": "fallback_policy_only",
            "bound_units": "arena-dependent",
            "missing_mts_inputs": "numeric residual coefficients; source-normalized Newtonian map; local/orbital projections",
            "current_status": "RETAINED_SCALAR_KAPPA_BRANCH_NONCLAIM",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def waitstate_rows() -> list[dict[str, Any]]:
    blockers = [
        ("WAIT1468_0_visible_algebra", "parent_visible_coefficient_algebra", "MISSING_PARENT_THEOREM", "derive hidden invariant algebra triviality or no-extension visible action grammar"),
        ("WAIT1468_1_balpha", "b_alpha_EM", "MISSING_MTS_VALUE", "derive or source standalone hidden EM coefficient response"),
        ("WAIT1468_2_tau_clock", "tau_clock_or_hidden_flow", "MISSING_DYNAMICS", "derive clock/local hidden flow normalization and units"),
        ("WAIT1468_3_tau_WEP", "tau_WEP", "MISSING_WEP_PROJECTION", "derive or source WEP projection/readout kernel"),
        ("WAIT1468_4_R10_curve", "R10_alpha_bound_curve", "REVIEW_CANDIDATE_NOT_CLAIM_READY", "obtain official curve or QA-approved digitization"),
        ("WAIT1468_5_parent_basis", "parent_basis_map", "MISSING_PARENT_BASIS", "fix source/current conventions before comparing beta_source_alpha"),
        ("WAIT1468_6_radiative", "radiative_readout_closure", "MISSING_CLOSURE", "prove EFT/readout maps preserve visible coefficient algebra or retain bounds"),
    ]
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "waitstate_id": wait_id,
            "blocked_field": field,
            "current_value": marker,
            "required_resolution": resolution,
            "claim_effect": "no score-ready alpha/constant row until resolved",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for wait_id, field, marker, resolution in blockers
    ]


def countermodel_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1468_0_hidden_scalar_coefficient",
            "countermodel": "C_parent=Q_obs x K_const x R_X and S_vis contains [g_*^-2+epsilon f(X)]F_Q^2",
            "survives_why": "gauge/diffeo covariance and a single A_Q can still hold",
            "killed_by_1468": False,
            "needed_to_kill": "no-extension grammar or hidden invariant algebra triviality",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1468_1_discrete_hidden_sector",
            "countermodel": "two hidden fibre components carry different constant Z_EM values but same q_loc and pi_const readout",
            "survives_why": "local vertical derivative tests can miss disconnected fibre labels",
            "killed_by_1468": False,
            "needed_to_kill": "connected fibre/orbit theorem or discrete-sector exclusion",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1468_2_spurion_marker",
            "countermodel": "material/domain marker is treated as a fixed spurion coefficient in S_vis",
            "survives_why": "contract forbids it as policy, but parent no-spurion theorem is not derived",
            "killed_by_1468": False,
            "needed_to_kill": "parent no-spurion/no-extension theorem",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
        {
            "same_parent_branch_id": BRANCH_ID,
            "countermodel_id": "CM1468_3_radiative_reentry",
            "countermodel": "bare S_vis has quotient coefficients but readout/EFT produces Z_EM^eff(Xhat)",
            "survives_why": "tree-level grammar does not prove radiative/readout stability",
            "killed_by_1468": False,
            "needed_to_kill": "radiative/readout closure theorem or executable bound rows",
            "valid_for_claim": False,
            "claim_allowed": False,
        },
    ]


def live_guard_rows() -> list[dict[str, Any]]:
    guarded = [
        ("LG1468_0_official_readout", LIVE_OFFICIAL_READOUT, "official MICROSCOPE readout kernel"),
        ("LG1468_1_source_worldtube", LIVE_SOURCE_WORLD, "source worldtube/projection table"),
        ("LG1468_2_material_tensor", LIVE_MATERIAL_TENSOR, "material tensor from official data"),
        ("LG1468_3_Cparent", LIVE_CPARENT, "live C_parent WEP coefficient import"),
        ("LG1468_4_visible_algebra", LIVE_VISIBLE_ALGEBRA, "live parent-signed visible algebra import"),
        ("LG1468_5_alpha_bound", LIVE_ALPHA_BOUND, "live claim alpha/constant bound import"),
    ]
    return [
        {
            "guard_id": guard_id,
            "path": str(path.relative_to(ROOT)),
            "meaning": meaning,
            "exists_now": path.exists(),
            "would_write_in_1468": False,
            "status": "ABSENT_EXPECTED" if not path.exists() else "PRESENT_PREEXISTING_REVIEW_REQUIRED",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
        for guard_id, path, meaning in guarded
    ]


def reduction_gate_rows(algebra: list[dict[str, Any]], retained: list[dict[str, Any]]) -> list[dict[str, Any]]:
    exact_descent = any(row["result"] == "EXACT_SUBTHEOREM" for row in algebra)
    failed_verdict = any(row["result"] == "NOT_PARENT_DERIVED_KEEP_RETAINED_ALPHA_BOUND_ROWS" for row in algebra)
    retained_written = len(retained) >= 5
    return [
        {
            "gate_id": "GATE1468_0_exact_descent_subtheorem",
            "gate": "descent-to-vertical-silence subtheorem is exact",
            "gate_pass": exact_descent,
            "claim_effect": "math piece proven conditional only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1468_1_hidden_invariant_triviality",
            "gate": "hidden invariant algebra is exactly quotient-plus-constant",
            "gate_pass": False,
            "claim_effect": "visible coefficient algebra cannot be parent-promoted",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1468_2_no_extension_grammar",
            "gate": "visible action grammar forbids hidden coefficient slots by parent derivation",
            "gate_pass": False,
            "claim_effect": "f(Xhat)F_Q^2 countermodel survives",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1468_3_radiative_readout_closure",
            "gate": "EFT/readout maps preserve coefficient algebra",
            "gate_pass": False,
            "claim_effect": "radiative reentry remains retained",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1468_4_failed_theorem_recorded",
            "gate": "failed parent-algebra promotion is explicitly recorded",
            "gate_pass": failed_verdict,
            "claim_effect": "prevents hidden closure",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1468_5_retained_bound_rows_written",
            "gate": "alpha/constant retained bound rows are written",
            "gate_pass": retained_written,
            "claim_effect": "fallback is executable scaffold only",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1468_6_score_ready_alpha_rows",
            "gate": "retained alpha/constant rows are score-ready",
            "gate_pass": False,
            "claim_effect": "MTS values/projections/source paths missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE1468_7_local_claim",
            "gate": "local GR/WEP/R10/Newton claim allowed",
            "gate_pass": False,
            "claim_effect": "explicitly forbidden in 1468",
            "valid_for_claim": False,
        },
    ]


def signing_decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "same_parent_branch_id": BRANCH_ID,
            "decision_id": "SIGN1468_0_visible_algebra",
            "target": "parent visible coefficient algebra triviality",
            "exact_descent_subtheorem": True,
            "hidden_invariant_triviality_signed": False,
            "no_extension_grammar_signed": False,
            "constant_superselection_signed": False,
            "radiative_readout_closure_signed": False,
            "retained_bound_rows_written": True,
            "retained_rows_score_ready": False,
            "visible_algebra_import_allowed": False,
            "no_hidden_F2_import_allowed": False,
            "C_parent_WEP_import_allowed": False,
            "local_claim_allowed": False,
            "decision": "REFUSE_VISIBLE_ALGEBRA_PROMOTION_KEEP_RETAINED_ALPHA_BOUND_ROWS",
            "reason": "the exact descent lemma is useful, but the parent has not derived hidden invariant algebra triviality or a no-extension visible action grammar",
            "valid_prediction_row": False,
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC1468_0",
            "decision": "keep the exact descent lemma",
            "why": "it gives the right mathematical shape for future closure",
            "consequence": "the next proof target is hidden invariant algebra/no-extension, not EM algebra",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1468_1",
            "decision": "reject covariance-only proof",
            "why": "hidden scalar coefficients are gauge and diffeo covariant",
            "consequence": "do not use covariance/Ward language to smuggle no-hidden-F2",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC1468_2",
            "decision": "write retained alpha/constant bound rows",
            "why": "failed theorem-zero must become explicit products with units, sources, and waitstates",
            "consequence": "future empirical route has a scaffold but remains nonclaim",
            "valid_for_claim": False,
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_id": "NEXT1468_0_1469",
            "next_target": "1469-Y5-R10-RAB-hidden-invariant-algebra-or-alpha-residual-product-runner.md",
            "script": "scripts/Y5_R10_RAB_hidden_invariant_algebra_or_alpha_residual_product_runner.py",
            "objective": "try to derive hidden invariant algebra triviality/orbit transitivity; if it fails, turn 1468 retained alpha rows into a stricter nonclaim product runner",
            "include": "vertical orbit transitivity; no extra hidden invariants; connected fibre/discrete-sector audit; alpha/clock/WEP/R10 product schema",
            "exclude": "local-GR pass; WEP/R10 claim; C_parent promotion; formalization-workbench edits; GitHub action",
            "valid_for_claim": False,
            "claim_allowed": False,
        }
    ]


def generated_csvs() -> list[Path]:
    return [
        SOURCE_REGISTER,
        ALGEBRA_TRIVIALITY,
        HIDDEN_INVARIANTS,
        VISIBLE_GRAMMAR,
        DERIVATION_DECISION,
        RETAINED_BOUNDS,
        WAITSTATE,
        COUNTERMODELS,
        QUAR_RETAINED_BOUNDS,
        QUAR_WAITSTATE,
        LIVE_GUARD,
        REDUCTION_GATES,
        SIGNING_DECISION,
        DECISION_LEDGER,
        NEXT_TARGET,
    ]


def csv_parse_clean(paths: list[Path]) -> bool:
    try:
        for path in paths:
            rows = read_csv_rows(path)
            if not rows:
                return False
        return True
    except Exception:
        return False


def branch_copies_exist() -> bool:
    return BRANCH_ALGEBRA.exists() and BRANCH_RETAINED_BOUNDS.exists() and BRANCH_SIGNING.exists()


def validation_rows(
    sources: list[dict[str, Any]],
    algebra: list[dict[str, Any]],
    invariants: list[dict[str, Any]],
    grammar: list[dict[str, Any]],
    retained: list[dict[str, Any]],
    waitstates: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    live_guard: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    local_sources_exist = all(row["source_type"] != "local_file" or truth(row["exists"]) for row in sources)
    exact_subtheorem = any(row["result"] == "EXACT_SUBTHEOREM" for row in algebra)
    refusal_written = any(row["result"] == "NOT_PARENT_DERIVED_KEEP_RETAINED_ALPHA_BOUND_ROWS" for row in algebra)
    invariants_unsigned = all(row["status"] in {"UNSIGNED", "REJECTED_SHORTCUT"} for row in invariants)
    grammar_unsigned = all("DERIVED" not in row["current_status"] or row["current_status"] in {"CONTRACT_CANDIDATE_NOT_DERIVED", "NOT_PARENT_DERIVED", "REQUIRED_CLOSURE_NOT_DERIVED"} for row in grammar)
    retained_nonclaim = len(retained) >= 5 and all(not truth(row["valid_for_claim"]) and not truth(row["claim_allowed"]) for row in retained)
    waitstates_nonclaim = len(waitstates) >= 7 and all(not truth(row["claim_allowed"]) for row in waitstates)
    countermodels_retained = all(not truth(row["killed_by_1468"]) for row in countermodels)
    live_paths_untouched = all(not truth(row["exists_now"]) and not truth(row["would_write_in_1468"]) for row in live_guard)
    safe_gate_pattern = truth(gates[0]["gate_pass"]) and truth(gates[4]["gate_pass"]) and truth(gates[5]["gate_pass"]) and all(
        not truth(row["gate_pass"]) for row in gates[1:4] + gates[6:]
    )
    signing_refuses = all(
        truth(row["exact_descent_subtheorem"])
        and not truth(row["hidden_invariant_triviality_signed"])
        and not truth(row["no_extension_grammar_signed"])
        and not truth(row["visible_algebra_import_allowed"])
        and not truth(row["no_hidden_F2_import_allowed"])
        and not truth(row["C_parent_WEP_import_allowed"])
        and not truth(row["local_claim_allowed"])
        for row in signing
    )
    generated_parse = csv_parse_clean(generated_csvs())
    pycache_absent = not (ROOT / "scripts" / "__pycache__").exists()
    formalization_untouched = formalization_modified_count() == 0
    checks = [
        ("VAL1468_0_sources", local_sources_exist, "all cited local source paths exist"),
        ("VAL1468_1_exact_subtheorem", exact_subtheorem, "descent-to-vertical-silence subtheorem written"),
        ("VAL1468_2_refusal", refusal_written, "parent visible algebra promotion refused"),
        ("VAL1468_3_invariants_unsigned", invariants_unsigned, "hidden invariant/orbit clauses remain unsigned or rejected shortcut"),
        ("VAL1468_4_grammar_unsigned", grammar_unsigned, "visible action grammar clauses remain unsigned"),
        ("VAL1468_5_retained_bounds", retained_nonclaim, "retained alpha/constant bound rows written nonclaim"),
        ("VAL1468_6_waitstates", waitstates_nonclaim, "waitstates block score-ready retained rows"),
        ("VAL1468_7_countermodels", countermodels_retained, "all countermodels retained"),
        ("VAL1468_8_live_paths", live_paths_untouched, "critical live official/source/material/Cparent/algebra/alpha files remain absent"),
        ("VAL1468_9_gate_pattern", safe_gate_pattern, "only exact-subtheorem/refusal/retained-bound gates pass; claim gates false"),
        ("VAL1468_10_signing_refuses", signing_refuses, "parent signing refuses visible algebra/no-hidden-F2/local claims"),
        ("VAL1468_11_generated_csv_parse", generated_parse, "all generated 1468 CSVs parse cleanly"),
        ("VAL1468_12_branch_copies", branch_copies_exist(), "nonclaim branch copies written"),
        ("VAL1468_13_pycache_absent", pycache_absent, "scripts __pycache__ absent after run"),
        ("VAL1468_14_formalization_untouched", formalization_untouched, f"formalization modified-file count since start={formalization_modified_count()}"),
    ]
    overall = all(result for _, result, _ in checks)
    checks.append(
        (
            "VAL1468_15_overall",
            overall,
            "1468 preserves exact algebra lemma, refuses parent promotion, and writes retained alpha bound scaffold",
        )
    )
    generated = now()
    return [
        {
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail,
            "generated_utc": generated,
        }
        for check_id, result, detail in checks
    ]


def write_doc(
    sources: list[dict[str, Any]],
    algebra: list[dict[str, Any]],
    invariants: list[dict[str, Any]],
    grammar: list[dict[str, Any]],
    retained: list[dict[str, Any]],
    waitstates: list[dict[str, Any]],
    countermodels: list[dict[str, Any]],
    gates: list[dict[str, Any]],
    signing: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    validation: list[dict[str, Any]],
    next_target: list[dict[str, Any]],
) -> None:
    lines: list[str] = []
    lines.append("# 1468 - Y5 R10 RAB Parent Visible Coefficient Algebra Triviality Or Retained Alpha Bound")
    lines.append("")
    lines.append("## Verdict")
    lines.append("- The exact descent lemma is good: if visible coefficients live only in quotient-plus-constant algebra, hidden vertical derivatives vanish.")
    lines.append("- The parent promotion fails: hidden invariant algebra triviality, vertical orbit transitivity, no-extension visible grammar, and radiative/readout closure are still unsigned.")
    lines.append("- Therefore no-hidden-`F_Q^2`, alpha silence, WEP/R10/clock/local-GR, and `C_parent` promotion remain forbidden.")
    lines.append("- The honest fallback is written: retained alpha/constant bound rows with explicit waitstates, not a hidden closure.")
    lines.append("")
    lines.append("## Core Lemma")
    lines.append("If `c in q_loc^*C^\u221e(Q_obs) tensor pi_const^*C^\u221e(K_const)` and `v in ker(Dq_loc) cap ker(Dpi_const)`, then `L_v c = 0`.")
    lines.append("")
    lines.append("This is exact but conditional. The missing parent theorem is the inclusion statement: every visible coefficient must actually live in that descended algebra.")
    lines.append("")
    lines.append("## Source Register")
    lines.append("| source_id | exists | path_or_url | usage |")
    lines.append("|---|---:|---|---|")
    for row in sources:
        lines.append(f"| {row['source_id']} | {row['exists']} | `{row['path_or_url']}` | {row['usage']} |")
    lines.append("")
    lines.append("## Algebra Triviality Attempt")
    lines.append("| step_id | result | blocker | parent_signed |")
    lines.append("|---|---|---|---:|")
    for row in algebra:
        lines.append(f"| {row['step_id']} | {row['result']} | {row['blocker']} | {row['parent_signed']} |")
    lines.append("")
    lines.append("## Hidden Invariant Audit")
    lines.append("| audit_id | status | counterexample |")
    lines.append("|---|---|---|")
    for row in invariants:
        lines.append(f"| {row['audit_id']} | {row['status']} | {row['counterexample']} |")
    lines.append("")
    lines.append("## Visible Action Grammar Audit")
    lines.append("| grammar_id | current_status | would_forbid | fallback_if_missing |")
    lines.append("|---|---|---|---|")
    for row in grammar:
        lines.append(f"| {row['grammar_id']} | {row['current_status']} | {row['would_forbid']} | {row['fallback_if_missing']} |")
    lines.append("")
    lines.append("## Retained Alpha/Constant Bound Rows")
    lines.append("| bound_row_id | arena | available_bound_value | current_status |")
    lines.append("|---|---|---:|---|")
    for row in retained:
        lines.append(f"| {row['bound_row_id']} | {row['arena']} | {row['available_bound_value']} | {row['current_status']} |")
    lines.append("")
    lines.append("## Waitstates")
    lines.append("| waitstate_id | blocked_field | current_value |")
    lines.append("|---|---|---|")
    for row in waitstates:
        lines.append(f"| {row['waitstate_id']} | {row['blocked_field']} | {row['current_value']} |")
    lines.append("")
    lines.append("## Countermodels Retained")
    lines.append("| countermodel_id | killed_by_1468 | needed_to_kill |")
    lines.append("|---|---:|---|")
    for row in countermodels:
        lines.append(f"| {row['countermodel_id']} | {row['killed_by_1468']} | {row['needed_to_kill']} |")
    lines.append("")
    lines.append("## Gates")
    lines.append("| gate_id | gate_pass | claim_effect |")
    lines.append("|---|---:|---|")
    for row in gates:
        lines.append(f"| {row['gate_id']} | {row['gate_pass']} | {row['claim_effect']} |")
    lines.append("")
    lines.append("## Parent Signing Decision")
    for row in signing:
        lines.append(f"- `{row['decision_id']}`: `{row['decision']}` because {row['reason']}.")
    lines.append("")
    lines.append("## Decision Ledger")
    for row in decisions:
        lines.append(f"- `{row['decision_id']}`: {row['decision']} - {row['consequence']}.")
    lines.append("")
    lines.append("## Validation")
    lines.append("| check_id | result | detail |")
    lines.append("|---|---|---|")
    for row in validation:
        lines.append(f"| {row['check_id']} | {row['result']} | {row['detail']} |")
    lines.append("")
    lines.append("## Next Target")
    for row in next_target:
        lines.append(f"- `{row['next_target']}` via `{row['script']}`: {row['objective']}")
    lines.append("")
    DOC.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    sources = source_rows()
    algebra = algebra_triviality_rows()
    invariants = hidden_invariant_rows()
    grammar = visible_grammar_rows()
    derivation = derivation_decision_rows()
    retained = retained_bound_rows()
    waitstates = waitstate_rows()
    countermodels = countermodel_rows()
    live_guard = live_guard_rows()
    gates = reduction_gate_rows(algebra, retained)
    signing = signing_decision_rows()
    decisions = decision_rows()
    next_target = next_target_rows()

    write_csv(SOURCE_REGISTER, sources)
    write_csv(ALGEBRA_TRIVIALITY, algebra)
    write_csv(HIDDEN_INVARIANTS, invariants)
    write_csv(VISIBLE_GRAMMAR, grammar)
    write_csv(DERIVATION_DECISION, derivation)
    write_csv(RETAINED_BOUNDS, retained)
    write_csv(WAITSTATE, waitstates)
    write_csv(COUNTERMODELS, countermodels)
    write_csv(QUAR_RETAINED_BOUNDS, retained)
    write_csv(QUAR_WAITSTATE, waitstates)
    write_csv(LIVE_GUARD, live_guard)
    write_csv(REDUCTION_GATES, gates)
    write_csv(SIGNING_DECISION, signing)
    write_csv(DECISION_LEDGER, decisions)
    write_csv(NEXT_TARGET, next_target)

    copy_branch(ALGEBRA_TRIVIALITY, BRANCH_ALGEBRA)
    copy_branch(RETAINED_BOUNDS, BRANCH_RETAINED_BOUNDS)
    copy_branch(SIGNING_DECISION, BRANCH_SIGNING)

    validation = validation_rows(sources, algebra, invariants, grammar, retained, waitstates, countermodels, live_guard, gates, signing)
    write_csv(VALIDATION, validation)
    write_doc(sources, algebra, invariants, grammar, retained, waitstates, countermodels, gates, signing, decisions, validation, next_target)
    print("Y5_R10_1468_visible_algebra_not_parent_signed_retained_alpha_bounds_nonclaim")


if __name__ == "__main__":
    main()
