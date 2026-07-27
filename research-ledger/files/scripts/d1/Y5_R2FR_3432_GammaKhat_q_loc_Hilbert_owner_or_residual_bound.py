from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3432-Y5-R2FR-GammaKhat-q_loc-Hilbert-owner-or-residual-bound-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3431": ROOT / "3431-Y5-R2FR-domain-projector-no-stress-theorem-or-operator-bound-under-AX1090.md",
    "next_3431": OUT / "P8_Y5_R2FR_3431_NEXT_TARGET.csv",
    "bound_rows_3430": OUT / "P8_Y5_R2FR_3430_HIDDEN_PROJECTOR_BOUND_ROWS.csv",
    "gamma_contract_513": OUT / "P8_GAMMA_KHAT_QLOC_FIRST_VARIATION_CONTRACT.csv",
    "gamma_stress_rewrite_513": OUT / "P8_GAMMA_KHAT_QLOC_STRESS_REWRITE.csv",
    "gamma_integrability_513": OUT / "P8_GAMMA_KHAT_QLOC_INTEGRABILITY_GATES.csv",
    "gamma_gate_tests_513": OUT / "P8_GAMMA_KHAT_QLOC_GATE_TESTS.csv",
    "gamma_residual_513": OUT / "P8_GAMMA_KHAT_QLOC_RESIDUAL_OR_DEMOTION.csv",
    "gamma_decision_513": OUT / "P8_GAMMA_KHAT_QLOC_DECISION.csv",
    "gk_response_contract_514": OUT / "P8_GK_METRIC_RESPONSE_CONTRACT.csv",
    "gk_metric_response_sources_515": OUT / "P8_GK_METRIC_RESPONSE_MATCH_SOURCE_REGISTER.csv",
    "gk_metric_response_evidence_515": OUT / "P8_GK_METRIC_RESPONSE_SOURCE_EVIDENCE.csv",
    "gamma_owner_decision_516": OUT / "P8_GAMMA_OWNER_OR_QLOC_BOUND_DECISION.csv",
    "qloc_bound_runner_spec_516": OUT / "P8_QLOC_BOUND_RUNNER_SPEC.csv",
    "qloc_bound_trigger_517": OUT / "P8_QLOC_BOUND_TRIGGER_LEDGER.csv",
    "q_loc_2409_variation": OUT / "P8_Y5_PARENT_QLOC_2409_GAMMA_EFF_METRIC_VARIATION_MERGE.csv",
    "q_loc_2409_khat_audit": OUT / "P8_Y5_PARENT_QLOC_2409_KHAT_METRIC_RESPONSE_MATCH_AUDIT.csv",
    "q_loc_2409_operator_status": OUT / "P8_Y5_PARENT_QLOC_2409_QLOC_RESPONSE_OPERATOR_STATUS.csv",
    "q_loc_2409_claim_gates": OUT / "P8_Y5_PARENT_QLOC_2409_CLAIM_GATES.csv",
    "fixed_point_511": OUT / "P8_MIN_PARENT_LOCAL_GR_FIXED_POINT_CONDITIONS.csv",
    "symbol_map_512": OUT / "P8_MTS_SYMBOL_TO_LOCAL_GR_ACTION_MAP.csv",
    "source_current_noether": OUT / "P8_YLOC_SOURCE_CURRENT_NOETHER_AUDIT.csv",
    "constant_gm_runner": OUT / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3432_SOURCE_REGISTER.csv",
    "hilbert_owner_theorem": OUT / "P8_Y5_R2FR_3432_QLOC_HILBERT_OWNER_THEOREM.csv",
    "owner_audit": OUT / "P8_Y5_R2FR_3432_GAMMA_KHAT_OWNER_AUDIT.csv",
    "residual_decomposition": OUT / "P8_Y5_R2FR_3432_QLOC_RESIDUAL_DECOMPOSITION.csv",
    "residual_bound_pack": OUT / "P8_Y5_R2FR_3432_QLOC_RESIDUAL_BOUND_PACK.csv",
    "hidden_bound_update": OUT / "P8_Y5_R2FR_3432_HBR3430_2_UPDATE.csv",
    "ppn_r10_operator_update": OUT / "P8_Y5_R2FR_3432_QLOC_PPN_R10_OPERATOR_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3432_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3432_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3432_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3432_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3432_VALIDATION.csv",
}


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def md_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No rows._"
    fields = list(rows[0].keys())

    def clean(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "/")

    return "\n".join(
        [
            "| " + " | ".join(fields) + " |",
            "| " + " | ".join("---" for _ in fields) + " |",
            *["| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |" for row in rows],
        ]
    )


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3431": "domain/projector handoff",
        "next_3431": "3432 target declaration",
        "bound_rows_3430": "HBR3430_2 q_loc hidden bound row",
        "gamma_contract_513": "first-variation q_loc contract",
        "gamma_stress_rewrite_513": "q_loc = projected divergence stress rewrite",
        "gamma_integrability_513": "Hilbert/integrability gate list",
        "gamma_gate_tests_513": "existing q_loc gate tests",
        "gamma_residual_513": "residual/demotion branches",
        "gamma_decision_513": "q_loc decision ledger",
        "gk_response_contract_514": "metric-response owner contract",
        "gk_metric_response_sources_515": "metric-response source register",
        "gk_metric_response_evidence_515": "metric-response evidence",
        "gamma_owner_decision_516": "owner-or-bound decision",
        "qloc_bound_runner_spec_516": "q_loc bound runner specification",
        "qloc_bound_trigger_517": "q_loc bound trigger ledger",
        "q_loc_2409_variation": "response-doublet formal variation candidate",
        "q_loc_2409_khat_audit": "Khat metric-response match audit",
        "q_loc_2409_operator_status": "PPN/R10 operator status",
        "q_loc_2409_claim_gates": "q_loc claim gates",
        "fixed_point_511": "minimal local-GR fixed-point conditions",
        "symbol_map_512": "symbol placement map",
        "source_current_noether": "Noether current audit",
        "constant_gm_runner": "source-normalization residual runner",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def hilbert_owner_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "QH3432_0_rewrite",
            "statement": "The q_loc object is the local projection of the divergence of an effective stress tensor.",
            "formula": "T_GK^{mu nu}:=Gamma_eff g^{mu nu}-K_hat^{mu nu}; q_loc^nu=P_loc nabla_mu T_GK^{mu nu}",
            "status": "ALGEBRAIC_IDENTITY",
            "condition_or_missing": "requires stress units and fixed sign convention, but not a zero proof",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "QH3432_1_hilbert_owner",
            "statement": "If T_GK is the Hilbert stress of a diffeomorphism-invariant parent action, its divergence is Euler-owned.",
            "formula": "T_GK^{mu nu}=(-2/sqrt(-g)) delta S_GK/delta g_{mu nu}; nabla_mu T_GK^{mu nu}=sum_A E_A nabla^nu Phi^A + B_GK^nu",
            "status": "CONDITIONAL_WARD_THEOREM",
            "condition_or_missing": "S_GK action, Helmholtz integrability, K_hat metric response, Euler equations, and boundary convention",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "QH3432_2_zero_branch",
            "statement": "q_loc vanishes in compact local vacuum only if Euler, boundary, and projector defects vanish in the same branch.",
            "formula": "E_A=0, B_GK^nu=0, [P_loc,nabla]T_GK=0, P_loc parent-owned => q_loc^nu=0",
            "status": "CONDITIONAL_ZERO_THEOREM",
            "condition_or_missing": "current MTS lacks a single branch satisfying all clauses",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "QH3432_3_double_zero",
            "statement": "First-order PPN leakage is removed only if T_GK and its first field variation vanish at the local fixed point.",
            "formula": "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0 => F_1^{GK}=0",
            "status": "CONDITIONAL_LINEAR_SILENCE_THEOREM",
            "condition_or_missing": "response-doublet candidate has formal shape, but physical q_loc component map and live K_hat identity are missing",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "QH3432_4_noether_not_enough",
            "statement": "Noether/Bianchi ownership gives conservation accounting, not componentwise q_loc silence.",
            "formula": "nabla_mu(T_EH+T_m+T_GK+T_extra)^{mu nu}=0 does not imply nabla_mu T_GK^{mu nu}=0",
            "status": "NO_GO_LEMMA",
            "condition_or_missing": "component zero or bound is required; no hidden exchange cancellation",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "QH3432_5_bound_branch",
            "statement": "If any owner clause fails, q_loc is an explicit residual source with a norm bound.",
            "formula": "||q_loc||_* <= ||P_loc||[||Delta_K||_*+||E nabla Phi||_*+||B_GK||_*]+||[P_loc,nabla]T_GK||_*",
            "status": "BOUND_THEOREM_READY_VALUES_MISSING",
            "condition_or_missing": "operator norms, defect profiles, boundary flux, source normalization, and M_H_ref",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "QH3432_6_verdict",
            "statement": "Current MTS has a clean Hilbert-owner contract and response-doublet candidate, but no current q_loc zero claim.",
            "formula": "q_loc_zero_current=false; epsilon_q_loc_TGK_mass retained",
            "status": "OWNER_NOT_SIGNED_BOUND_RETAINED",
            "condition_or_missing": "K_hat identity and response/source-normalization map are the immediate blockers",
            "valid_for_claim": False,
        },
    ]


def owner_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "GOA3432_0_action_existence",
            "owner_clause": "local diffeomorphism-invariant S_GK exists",
            "best_evidence": "response-doublet candidate Gamma_eff=Gamma0+1/2 M_AB Z^A Z^B+O(Z^4)",
            "pass_now": False,
            "blocker": "candidate is not adopted as live MTS parent density with field content, units, and boundary convention",
            "fallback_residual": "q_action_owner_defect",
            "valid_for_claim": False,
        },
        {
            "audit_id": "GOA3432_1_metric_response",
            "owner_clause": "K_hat equals the metric response of Gamma_eff",
            "best_evidence": "formal K_metric variation exists in 2409",
            "pass_now": False,
            "blocker": "no source path proves live K_hat is delta[sqrt(-g)Gamma_eff]/delta g under one convention",
            "fallback_residual": "q_metric_response_defect",
            "valid_for_claim": False,
        },
        {
            "audit_id": "GOA3432_2_integrability",
            "owner_clause": "Helmholtz/integrability conditions for T_GK",
            "best_evidence": "513/514 gate list",
            "pass_now": False,
            "blocker": "second-variation symmetry and boundary improvement not checked for live tensor",
            "fallback_residual": "q_integrability_defect",
            "valid_for_claim": False,
        },
        {
            "audit_id": "GOA3432_3_euler_closure",
            "owner_clause": "fields building Gamma/Khat obey source-free local Euler equations",
            "best_evidence": "positive-operator/no-hair machinery from 3429 can apply if field-specific source/gap data exist",
            "pass_now": False,
            "blocker": "field-specific lambda, J, B, R and source-free collar are missing",
            "fallback_residual": "q_euler_source_defect",
            "valid_for_claim": False,
        },
        {
            "audit_id": "GOA3432_4_double_zero",
            "owner_clause": "T_GK(Phi0)=0 and partial_A T_GK(Phi0)=0",
            "best_evidence": "response-doublet density has formal double-zero after Gamma0 subtraction",
            "pass_now": False,
            "blocker": "physical q_loc component map and live Khat identity are not matched",
            "fallback_residual": "q_F1_defect",
            "valid_for_claim": False,
        },
        {
            "audit_id": "GOA3432_5_projector",
            "owner_clause": "P_loc is parent-owned and commutes with local readout/fixed-point limit",
            "best_evidence": "3431 supplies projector no-stress or operator-bound discipline",
            "pass_now": False,
            "blocker": "active dynamic/domain projector branch is not zero; P_loc commutator can survive",
            "fallback_residual": "q_projection_defect",
            "valid_for_claim": False,
        },
        {
            "audit_id": "GOA3432_6_boundary",
            "owner_clause": "S_GK boundary/symplectic flux is zero or fixed reference",
            "best_evidence": "3427 boundary/reference theorem helps identity-Hilbert branch",
            "pass_now": False,
            "blocker": "GK-specific theta/Q/boundary flux not extracted",
            "fallback_residual": "q_boundary_flux_defect",
            "valid_for_claim": False,
        },
    ]


def residual_decomposition() -> list[dict[str, Any]]:
    return [
        {
            "residual_id": "QRD3432_0_action_owner",
            "defect": "q_action_owner_defect",
            "meaning": "Gamma/Khat are not proven to come from one scalar parent density",
            "bound_route": "treat T_GK as retained effective stress and bound its divergence",
            "test_arenas": "PPN/source-normalization/R10",
            "valid_for_claim": False,
        },
        {
            "residual_id": "QRD3432_1_metric_response",
            "defect": "q_metric_response_defect",
            "meaning": "live K_hat may not equal K_metric from Gamma_eff variation",
            "bound_route": "Delta_K^{mu nu}:=K_hat^{mu nu}-K_metric^{mu nu}; bound P_loc nabla_mu Delta_K^{mu nu}",
            "test_arenas": "PPN beta/gamma/alpha; fifth-force",
            "valid_for_claim": False,
        },
        {
            "residual_id": "QRD3432_2_euler_source",
            "defect": "q_euler_source_defect",
            "meaning": "fields in T_GK are not source-free/on-shell in local compact vacuum",
            "bound_route": "sum_A ||E_A nabla Phi^A||_* or positive-operator no-hair input",
            "test_arenas": "Newtonian source exchange; R10/Yukawa; clocks",
            "valid_for_claim": False,
        },
        {
            "residual_id": "QRD3432_3_first_order",
            "defect": "q_F1_defect",
            "meaning": "T_GK or first variation is nonzero at fixed point",
            "bound_route": "linear response coefficient beta_qloc or F1_GK residual",
            "test_arenas": "PPN first-order and preferred-frame rows",
            "valid_for_claim": False,
        },
        {
            "residual_id": "QRD3432_4_projector",
            "defect": "q_projection_defect",
            "meaning": "P_loc can hide or create residual components if not parent-owned",
            "bound_route": "||[P_loc,nabla]T_GK||_* plus 3431 domain/projector operator-bound rows",
            "test_arenas": "PPN alpha/xi; source calibration",
            "valid_for_claim": False,
        },
        {
            "residual_id": "QRD3432_5_boundary",
            "defect": "q_boundary_flux_defect",
            "meaning": "bulk q_loc silence does not imply boundary/symplectic silence",
            "bound_route": "|Phi_GK|/M_H_ref plus boundary/reference flux rows",
            "test_arenas": "orbital GM; clocks/Gdot; alpha3",
            "valid_for_claim": False,
        },
        {
            "residual_id": "QRD3432_6_total",
            "defect": "epsilon_q_loc_TGK_mass",
            "meaning": "absolute total q_loc hidden residual",
            "bound_route": "absolute sum of QRD3432_0..5, no cancellation unless parent Ward identity is signed",
            "test_arenas": "local GR/Newton/PPN/R10/clocks/orbital",
            "valid_for_claim": False,
        },
    ]


def residual_bound_pack() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "QRB3432_0_metric_response",
            "object": "Khat metric-response defect",
            "symbolic_bound": "epsilon_DeltaK <= C_K ||P_loc nabla_mu Delta_K^{mu nu}||*/M_H_ref",
            "needed_inputs": "Delta_K tensor profile or theorem-zero identity; projection norm; M_H_ref",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "QRB3432_1_euler_source",
            "object": "on-shell Euler source defect",
            "symbolic_bound": "epsilon_E <= C_E sum_A ||E_A nabla Phi^A||*/M_H_ref",
            "needed_inputs": "field equations, source-free collar, gradients, dual norm, M_H_ref",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "QRB3432_2_double_zero_linear",
            "object": "first-order fixed-point leakage",
            "symbolic_bound": "epsilon_F1 <= C_F1 ||partial_A T_GK(Phi0) delta Phi^A||*/M_H_ref",
            "needed_inputs": "fixed-point variables, physical q_loc component map, deltaPhi amplitude/range",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "QRB3432_3_projection",
            "object": "P_loc projection/commutator defect",
            "symbolic_bound": "epsilon_Ploc <= C_P ||[P_loc,nabla]T_GK||*/M_H_ref + epsilon_domain_projector_abs",
            "needed_inputs": "parent-owned P_loc or commutator norm; 3431 domain/projector bound values",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "QRB3432_4_boundary",
            "object": "GK boundary/symplectic flux",
            "symbolic_bound": "epsilon_GK_boundary <= C_B |Phi_GK|/M_H_ref",
            "needed_inputs": "theta_GK/Q_GK boundary flux, fixed reference, linking surface, M_H_ref",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "bound_id": "QRB3432_5_compact_shell_proxy",
            "object": "older compact-shell leakage proxy",
            "symbolic_bound": "epsilon_q_proxy <= 7.432631961576971e-06 only after mapping proxy units to PPN/source units",
            "needed_inputs": "unit map from J_rel/q_loc proxy to observable residual vector",
            "status": "NUMERIC_PROXY_NOT_CLAIM_VALUE",
            "valid_for_claim": False,
        },
        {
            "bound_id": "QRB3432_6_total_q_loc",
            "object": "total q_loc residual",
            "symbolic_bound": "epsilon_q_loc_TGK_mass <= sum(abs(QRB3432_0..QRB3432_5))",
            "needed_inputs": "all sub-bounds or zero certificates",
            "status": "ABSOLUTE_SUM_GUARD",
            "valid_for_claim": False,
        },
    ]


def hidden_bound_update() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "HBR3430_2_update_from_3432",
            "old_row": "HBR3430_2_GammaKhat_q_loc",
            "updated_residual_symbol": "epsilon_q_loc_TGK_mass",
            "updated_symbolic_bound": "C_K||P_loc div Delta_K||*/M_H_ref + C_E sum||E_A nabla Phi^A||*/M_H_ref + C_F1||F1_GK deltaPhi||*/M_H_ref + C_P||[P_loc,nabla]T_GK||*/M_H_ref + C_B|Phi_GK|/M_H_ref",
            "status": "DECOMPOSED_FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        }
    ]


def ppn_r10_operator_update() -> list[dict[str, Any]]:
    return [
        {
            "operator_id": "QOP3432_0_PPN_inverse_divergence",
            "arena": "PPN",
            "operator_form": "Delta_PPN_A = Pi_A G_Einstein^lin I_div^{-1}[q_loc] + boundary/support terms",
            "3432_status": "SCHEMA_RETAINED_NOT_SCORE_READY",
            "missing": "I_div convention, q_loc profile, source normalization, PPN gauge",
            "valid_for_claim": False,
        },
        {
            "operator_id": "QOP3432_1_R10_yukawa",
            "arena": "R10/fifth-force",
            "operator_form": "alpha_q(lambda)=K_lambda * Qbar_source[q_loc] * qbar_test[q_loc]",
            "3432_status": "SCHEMA_RETAINED_NOT_SCORE_READY",
            "missing": "q_loc-to-Yukawa source map, lambda, charges, real bound curve",
            "valid_for_claim": False,
        },
        {
            "operator_id": "QOP3432_2_source_normalization",
            "arena": "Newton/source calibration",
            "operator_form": "delta ln mu_obs includes epsilon_q_loc_TGK_mass and derivative/radial pieces",
            "3432_status": "RETAINED_AS_CONSTANT_GM_RUNNER_INPUT",
            "missing": "M_H_ref, tau, same-frame source denominator, radial/time derivatives",
            "valid_for_claim": False,
        },
        {
            "operator_id": "QOP3432_3_clocks_Gdot",
            "arena": "clocks/Gdot",
            "operator_form": "time component q_loc^tau maps to dln_Meff_dt or dln_mu_obs_dt after source/readout lock",
            "3432_status": "SYMBOLIC_ONLY",
            "missing": "time component units and clock/source readout map",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3432_0_rewrite",
            "gate": "q_loc stress-divergence rewrite exists",
            "result": "PASS",
            "evidence": "QH3432_0",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3432_1_hilbert_owner",
            "gate": "T_GK is Hilbert-owned by current MTS parent action",
            "result": "FAIL_CURRENT",
            "evidence": "GOA3432_0 through GOA3432_2",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3432_2_khat_identity",
            "gate": "K_hat equals metric response of Gamma_eff",
            "result": "FAIL_CURRENT",
            "evidence": "GOA3432_1",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3432_3_q_loc_zero",
            "gate": "q_loc vanishes in local compact vacuum",
            "result": "BLOCKED",
            "evidence": "Euler, projector, boundary and double-zero clauses unsigned",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3432_4_bound_contract",
            "gate": "q_loc residual bound decomposition exists",
            "result": "PASS_SYMBOLIC_VALUES_MISSING",
            "evidence": "QRB3432_0 through QRB3432_6",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3432_5_score_ready",
            "gate": "q_loc can be scored against PPN/R10/local tests",
            "result": "FAIL_VALUES_AND_MAPS_MISSING",
            "evidence": "QOP3432 rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3432_6_local_GR",
            "gate": "local GR/Newton route is derived",
            "result": "BLOCKED",
            "evidence": "q_loc, source normalization, M_H_ref/tau, and second-order PPN remain open",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3432_0_owner_route",
            "decision": "Keep the Hilbert-owner route as the clean derivation route.",
            "reason": "it would make q_loc an on-shell Ward residual rather than an inserted plateau.",
            "next_action": "source or construct the live K_hat metric-response identity",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3432_1_response_doublet",
            "decision": "Treat the response-doublet density as promising candidate infrastructure, not proof.",
            "reason": "formal double-zero is not enough without live K_hat/source/readout matching.",
            "next_action": "do not promote q_loc zero from response-doublet shape alone",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3432_2_bound_route",
            "decision": "If owner matching fails, q_loc must enter the residual vector explicitly.",
            "reason": "Noether/Bianchi ownership does not prove componentwise zero.",
            "next_action": "connect epsilon_q_loc_TGK_mass to M_H_ref/tau source normalization next",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3433-Y5-R2FR-MHref-tau-source-normalization-lock-or-residual-vector-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3433_MHref_tau_source_normalization_lock_or_residual_vector.py",
            "objective": "connect q_loc/domain/boundary residuals to the calibrated source denominator M_H_ref and tau, deciding whether Newtonian GM is protected or becomes an explicit residual vector",
            "success_condition": "same-frame M_H_ref/tau source denominator is locked, or epsilon_mu/q_loc/domain residual rows become score-ready inputs for Newton/PPN/R10",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3432_0",
            "purpose": "prevent plateau axiom",
            "rule": "q_loc=0 is allowed only if S_GK, K_hat metric response, Euler closure, P_loc ownership, double-zero and boundary silence all pass",
            "current_value": "claim_allowed=false",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3432_1",
            "purpose": "force residual scoring if owner route fails",
            "rule": "epsilon_q_loc_TGK_mass must be carried into Newton/PPN/R10/clocks as an absolute residual",
            "current_value": "bound_required=true",
            "valid_for_claim": False,
        },
    ]


def all_outputs_scoped() -> bool:
    root_resolved = ROOT.resolve()
    return all(root_resolved in path.resolve().parents or path.resolve() == root_resolved for path in [DOC, *OUTPUTS.values()])


def all_generated_nonclaim(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    theorem_rows = rows_by_name["hilbert_owner_theorem"]
    audit_rows = rows_by_name["owner_audit"]
    residual_rows = rows_by_name["residual_decomposition"]
    bound_rows = rows_by_name["residual_bound_pack"]
    operator_rows = rows_by_name["ppn_r10_operator_update"]
    promotion_rows = rows_by_name["promotion_gates"]
    next_rows = rows_by_name["next_target"]
    modified_count = 0
    if FORMALIZATION.exists():
        start_ts = start_utc.timestamp()
        modified_count = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start_ts)
    validations = [
        {
            "check_id": "VAL3432_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3432_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": all_outputs_scoped(),
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3432_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": all_generated_nonclaim(rows_by_name),
            "detail": "valid_for_claim=false throughout generated rows",
        },
        {
            "check_id": "VAL3432_3_hilbert_theorem",
            "condition": "Hilbert-owner zero theorem is explicit",
            "passed": any(row["theorem_id"] == "QH3432_2_zero_branch" for row in theorem_rows),
            "detail": "conditional q_loc zero theorem present",
        },
        {
            "check_id": "VAL3432_4_noether_no_go",
            "condition": "Noether/Bianchi alone is rejected as q_loc zero",
            "passed": any(row["theorem_id"] == "QH3432_4_noether_not_enough" for row in theorem_rows),
            "detail": "componentwise zero or bound required",
        },
        {
            "check_id": "VAL3432_5_owner_not_promoted",
            "condition": "owner audit does not promote current q_loc zero",
            "passed": all(str(row["pass_now"]).lower() == "false" for row in audit_rows),
            "detail": "all owner clauses remain unsigned",
        },
        {
            "check_id": "VAL3432_6_residual_decomposed",
            "condition": "q_loc residual is decomposed into actionable defects",
            "passed": len(residual_rows) >= 7 and any(row["residual_id"] == "QRD3432_6_total" for row in residual_rows),
            "detail": f"{len(residual_rows)} residual rows",
        },
        {
            "check_id": "VAL3432_7_bound_pack",
            "condition": "q_loc bound pack exists",
            "passed": len(bound_rows) >= 7 and any(row["bound_id"] == "QRB3432_6_total_q_loc" for row in bound_rows),
            "detail": f"{len(bound_rows)} bound rows",
        },
        {
            "check_id": "VAL3432_8_operator_update",
            "condition": "PPN/R10/source-normalization operator rows are retained",
            "passed": len(operator_rows) >= 4 and any(row["operator_id"] == "QOP3432_2_source_normalization" for row in operator_rows),
            "detail": f"{len(operator_rows)} operator rows",
        },
        {
            "check_id": "VAL3432_9_local_GR_blocked",
            "condition": "local GR remains blocked until q_loc/source rows close",
            "passed": any(row["gate_id"] == "PG3432_6_local_GR" and row["result"] == "BLOCKED" for row in promotion_rows),
            "detail": "no local-GR claim promoted",
        },
        {
            "check_id": "VAL3432_10_next_target",
            "condition": "next target connects residuals to M_H_ref/tau source normalization",
            "passed": next_rows[0]["target_doc"].startswith("3433-Y5-R2FR-MHref-tau"),
            "detail": next_rows[0]["target_doc"],
        },
        {
            "check_id": "VAL3432_11_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3432_12_overall",
            "condition": "3432 Gamma/Khat/q_loc checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3432 - Gamma/Khat/q_loc Hilbert Owner or Residual Bound

## Summary
- This checkpoint attacks `Gamma_eff/K_hat/q_loc` as a derivation problem, not as a plateau assumption.
- The clean route is exact: define `T_GK = Gamma_eff g - K_hat`; if `T_GK` is the Hilbert stress of a diffeomorphism-invariant parent action, then its divergence is Euler-owned.
- The zero claim still fails for current MTS because the live `K_hat` metric-response identity, action owner, Euler closure, projector ownership, boundary silence, and fixed-point double-zero are not all signed.
- The progress is that `q_loc` is now forced into a precise residual decomposition: metric-response defect, Euler-source defect, first-order defect, projection defect, and boundary flux.
- Next best target is source normalization: connect these residuals to `M_H_ref`, `tau`, and measured Newtonian `GM` instead of leaving them as abstract symbols.

## Source Register
{md_table(rows_by_name["source_register"])}

## q_loc Hilbert Owner Theorem
{md_table(rows_by_name["hilbert_owner_theorem"])}

## Gamma/Khat Owner Audit
{md_table(rows_by_name["owner_audit"])}

## q_loc Residual Decomposition
{md_table(rows_by_name["residual_decomposition"])}

## q_loc Residual Bound Pack
{md_table(rows_by_name["residual_bound_pack"])}

## HBR3430_2 Update
{md_table(rows_by_name["hidden_bound_update"])}

## q_loc PPN/R10 Operator Update
{md_table(rows_by_name["ppn_r10_operator_update"])}

## Promotion Gates
{md_table(rows_by_name["promotion_gates"])}

## Decision Ledger
{md_table(rows_by_name["decision_ledger"])}

## Next Target
{md_table(rows_by_name["next_target"])}

## Runner Nonclaim
{md_table(rows_by_name["runner_nonclaim"])}

## Validation
{md_table(rows_by_name["validation"])}

## Bottom Line
This is the non-smuggled route: `q_loc` can disappear only as an on-shell Hilbert/Ward residual from a real parent action. Current MTS does not yet prove that. But it now has a concrete residual vector that can be carried into Newton, PPN, R10, clocks, and source normalization without hiding the problem.
"""
    DOC.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "hilbert_owner_theorem": hilbert_owner_theorem(),
        "owner_audit": owner_audit(),
        "residual_decomposition": residual_decomposition(),
        "residual_bound_pack": residual_bound_pack(),
        "hidden_bound_update": hidden_bound_update(),
        "ppn_r10_operator_update": ppn_r10_operator_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    write_doc(rows_by_name)
    failed = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed:
        raise SystemExit(f"3432 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
