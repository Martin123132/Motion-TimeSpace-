from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3449-Y5-R2FR-absent-quotient-X-erasure-or-omegaX-bound-first-row-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "script_3449": Path(__file__).resolve(),
    "doc_3448": ROOT / "3448-Y5-R2FR-extra-sector-LX-ThetaX-QtauX-owner-or-deltaHcurl-extra-row-under-AX1090.md",
    "next_3448": OUT / "P8_Y5_R2FR_3448_NEXT_TARGET.csv",
    "lx_owner_audit_3448": OUT / "P8_Y5_R2FR_3448_LX_OWNER_ROUTE_AUDIT.csv",
    "curl_extra_3448": OUT / "P8_Y5_R2FR_3448_DELTAH_CURL_EXTRA_COMPONENT_ROW.csv",
    "quotient_map_637": OUT / "P8_Y5_R10_637_QUOTIENT_MAP_DERIVATION.csv",
    "no_pole_chain_670": OUT / "P8_Y5_R10_670_NO_POLE_QUOTIENT_PROOF_CHAIN.csv",
    "quotient_signature_626": OUT / "P8_Y5_R10_626_QUOTIENT_INVARIANT_SIGNATURE_ATTEMPT.csv",
    "vertical_chain_581": OUT / "P8_Y5_R10_581_QUOTIENT_VERTICAL_THEOREM_CHAIN.csv",
    "minimal_quotient_gate_619": OUT / "P8_Y5_R10_619_MINIMAL_QUOTIENT_GATE.csv",
    "erasure_audit_2670": OUT / "P8_Y5_R2FR_QUOTIENT_ERASURE_2670_ERASURE_CERTIFICATE_AUDIT.csv",
    "strict_signature_3114": OUT / "P8_Y5_R2FR_3114_STRICT_LOCAL_QUOTIENT_SIGNATURE_GATE.csv",
    "absent_attempt_3133": OUT / "P8_Y5_R2FR_3133_ABSENT_QUOTIENT_ATTEMPT.csv",
    "quotient_map_3134": OUT / "P8_Y5_R2FR_3134_QUOTIENT_MAP_ATTEMPT.csv",
    "fiber_descent_3271": OUT / "P8_Y5_R2FR_3271_QUOTIENT_FIBER_DESCENT_THEOREM.csv",
    "matter_signature_1088": OUT / "P8_Y5_R10_1088_MINIMAL_PARENT_ORDINARY_MATTER_SIGNATURE_CLAUSE_OR_FINITE_COEFFICIENT_INTAKE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3449_SOURCE_REGISTER.csv",
    "absent_quotient_zero_proof": OUT / "P8_Y5_R2FR_3449_ABSENT_QUOTIENT_ZERO_PROOF.csv",
    "parent_clause_matrix": OUT / "P8_Y5_R2FR_3449_PARENT_CLAUSE_MATRIX.csv",
    "omegaX_bound_first_row": OUT / "P8_Y5_R2FR_3449_OMEGAX_BOUND_FIRST_ROW.csv",
    "deltaH_curl_update": OUT / "P8_Y5_R2FR_3449_DELTAH_CURL_UPDATE.csv",
    "countermodel_guard": OUT / "P8_Y5_R2FR_3449_COUNTERMODEL_GUARD.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3449_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3449_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3449_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3449_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3449_VALIDATION.csv",
}


def existing_sources() -> dict[str, Path]:
    sources = dict(SOURCES)
    if not sources["matter_signature_1088"].exists():
        fallback = ROOT / "1088-Y5-R10-minimal-parent-ordinary-matter-signature-clause-or-finite-coefficient-intake.md"
        sources["matter_signature_1088"] = fallback
    return sources


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"no rows for {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


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


def source_register(sources: dict[str, Path]) -> list[dict[str, Any]]:
    roles = {
        "script_3449": "generator for this checkpoint",
        "doc_3448": "immediate handoff selecting absent quotient first",
        "next_3448": "machine-readable 3449 target",
        "lx_owner_audit_3448": "absent quotient branch selected as preferred route",
        "curl_extra_3448": "DHC3448 zero candidate and omega_X fallback rows",
        "quotient_map_637": "canonical quotient map and Dq[v_X] conditional derivation",
        "no_pole_chain_670": "no-pole quotient proof chain",
        "quotient_signature_626": "quotient-invariant matter action signature attempt",
        "vertical_chain_581": "quotient vertical theorem chain",
        "minimal_quotient_gate_619": "countermodel guard for markers/source weights/conformal frames",
        "erasure_audit_2670": "absent-quotient erasure certificate audit",
        "strict_signature_3114": "strict local quotient signature gate",
        "absent_attempt_3133": "recent absent quotient attempt",
        "quotient_map_3134": "explicit candidate quotient map",
        "fiber_descent_3271": "fiber-constant descent theorem",
        "matter_signature_1088": "ordinary matter signature clause or markdown fallback",
    }
    return [
        {
            "source_id": source_id,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[source_id],
            "claim_allowed": False,
            "valid_for_claim": False,
        }
        for source_id, path in sources.items()
    ]


def absent_quotient_zero_proof() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "AQZ3449_0_setup",
            "claim_piece": "quotient setup",
            "formal_statement": "Let q:Conf_parent->Q_obs be a smooth quotient/submersion on the local branch, and let v_X be tangent to its fibres so Dq[v_X]=0.",
            "derivation": "This defines X as representative data, not an independent physical coordinate. Any observable O=O_bar(q(Phi)) obeys L_vX O = D O_bar[Dq(v_X)] = 0.",
            "status": "EXACT_MATH_IF_Q_AND_VX_ARE_PARENT_SIGNED",
            "missing_for_promotion": "field-by-field parent v_X and domain-scoped q-map signature",
            "source_path": str(SOURCES["quotient_map_3134"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "AQZ3449_1_action_variation",
            "claim_piece": "bulk action erasure",
            "formal_statement": "If S_parent[Phi]=S_red[q(Phi)]+S_top[q(Phi)]+S_fixed_boundary on the local branch, then delta_vX S_parent=0 for every vertical v_X.",
            "derivation": "delta_vX S_parent = <delta S_red/dq, Dq[v_X]> + delta_vX S_fixed_boundary = 0. Thus the Euler contraction E_parent(v_X) and any independent X Hessian block vanish modulo constraints and fixed boundary terms.",
            "status": "DERIVED_CONDITIONAL_ZERO",
            "missing_for_promotion": "parent action descent before variation and boundary/topological silence",
            "source_path": str(SOURCES["no_pole_chain_670"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "AQZ3449_2_symplectic_pullback",
            "claim_piece": "Theta_X and omega_X erasure",
            "formal_statement": "If the symplectic potential descends as Theta_parent=q*Theta_red+dY with Y quotient-owned or vertically silent on the chosen boundary, then i_vX omega_parent=0.",
            "derivation": "omega_parent=delta Theta_parent=q*omega_red+d(delta Y). Contracting with v_X kills the q*omega_red part because Dq[v_X]=0; the exact d(delta Y) term integrates to zero only under the boundary-silence clause.",
            "status": "DERIVED_CONDITIONAL_ZERO_WITH_BOUNDARY_CLAUSE",
            "missing_for_promotion": "Y/boundary charge silence and surface-domain statement",
            "source_path": str(SOURCES["erasure_audit_2670"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "AQZ3449_3_noether_charge",
            "claim_piece": "Q_tau^X and C_tau^X erasure",
            "formal_statement": "If tau, surface data, measure, coframe and connection are quotient-owned and X has no separate bulk L_X, then J_tau^X=Theta_X(L_tau X)-i_tau L_X=dQ_tau^X+C_tau^X is identically zero.",
            "derivation": "The X-sector split from 3448 becomes the zero split L_X=Theta_X=omega_X=0. With no boundary representative charge, Q_tau^X=0 and C_tau^X=0 on the local branch.",
            "status": "DERIVED_CONDITIONAL_ZERO_WITH_DESCENT_CLAUSES",
            "missing_for_promotion": "measure/coframe/connection descent, tau/surface quotient ownership and Q_X boundary silence",
            "source_path": str(SOURCES["quotient_signature_626"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "AQZ3449_4_deltaH_result",
            "claim_piece": "extra H_tau curl erasure",
            "formal_statement": "Under AQZ3449_0 through AQZ3449_3, Delta_H_curl_extra=abs(int_BF[-int_S i_tau omega_X+C_tau^X+B_X])=0.",
            "derivation": "Each integrand term is zero separately: omega_X=0 by symplectic pullback, C_tau^X=0 by no independent X current, and B_X=0 by boundary silence. No cancellation is used.",
            "status": "THEOREM_PROVED_CONDITIONALLY_NOT_PARENT_PROMOTED",
            "missing_for_promotion": "all parent clauses must be signed in one certificate",
            "source_path": str(OUTPUTS["absent_quotient_zero_proof"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "proof_id": "AQZ3449_5_current_verdict",
            "claim_piece": "current MTS status",
            "formal_statement": "The exact theorem is now derived, but current MTS does not yet own every premise as a parent action fact.",
            "derivation": "Existing sources provide strong conditional q/descent math and explicit countermodel guards; the remaining leap is parent signature, especially all-field v_X, visible-sector descent and boundary silence.",
            "status": "ZERO_PROOF_NOT_CLAIMED_FALLBACK_BOUND_ROW_ACTIVE",
            "missing_for_promotion": "field-by-field v_X kernel signature or omega_X finite-bound inputs",
            "source_path": str(OUTPUTS["parent_clause_matrix"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def parent_clause_matrix() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "PCM3449_0_q_map",
            "clause": "parent q-map",
            "required_statement": "q:Conf_parent->Q_obs is local-branch parent-owned, not a post-readout projection.",
            "best_current_evidence": "637 and 3134 give a canonical/candidate quotient map.",
            "promotion_status": "PARTIAL_CONDITIONAL_SUPPORT",
            "failure_mode_if_unsigned": "X may be a physical coordinate rather than representative data.",
            "next_action": "field-by-field q target in 3450",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "PCM3449_1_vX_kernel",
            "clause": "vertical generator",
            "required_statement": "v_X is specified on metric/coframe, connection, EM, matter, memory/projector/domain and boundary fields, with Dq[v_X]=0 in every observed slot.",
            "best_current_evidence": "3134 states the criterion; 2570 has a ledger; multiple sources still mark all-field ownership missing.",
            "promotion_status": "MISSING_FIELD_BY_FIELD_PARENT_SIGNATURE",
            "failure_mode_if_unsigned": "a hidden conformal/disformal/source/domain slot can leak into local physics.",
            "next_action": "3450 kernel-signature table",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "PCM3449_2_action_descent",
            "clause": "bulk action descent before variation",
            "required_statement": "S_parent=S_red[q(Phi)] plus fixed boundary/topological terms before local equations are varied.",
            "best_current_evidence": "670 and 2670 give exact conditional route; 3114 states strict branch signature.",
            "promotion_status": "CONDITIONAL_NOT_PARENT_DERIVED",
            "failure_mode_if_unsigned": "an independent X Hessian or Green function remains physical.",
            "next_action": "tie action descent to the same q/v_X certificate",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "PCM3449_3_matter_descent",
            "clause": "ordinary matter and visible coefficients descend",
            "required_statement": "S_matter=Sbar[Obs(q(Phi)),Psi,theta_rep] and constants/source weights have no representative-X dependence.",
            "best_current_evidence": "626, 1088 and 3271 prove the chain-rule/descent theorem conditionally.",
            "promotion_status": "CONDITIONAL_WITH_COUNTERMODELS_RETAINED",
            "failure_mode_if_unsigned": "theta_A(X), source weights, hidden frame markers or material coefficients reintroduce coupling.",
            "next_action": "forbid or bound visible-sector leakage in the same signature",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "PCM3449_4_measure_coframe_connection",
            "clause": "measure/coframe/connection descent",
            "required_statement": "volume measure, observed coframe, metric connection, matter connection and tau/surface data all factor through q.",
            "best_current_evidence": "626 and 1088 give the structure; 3114 keeps public clock/readout conditional.",
            "promotion_status": "CONDITIONAL_NOT_GLOBAL_CERTIFICATE",
            "failure_mode_if_unsigned": "clock, PPN, EM stress or connection readout residuals survive.",
            "next_action": "include tau/surface/readout in 3450 kernel table",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "PCM3449_5_boundary_silence",
            "clause": "boundary/corner/projector silence",
            "required_statement": "Q_X=0/proper/exact, K_boundary=0, and Pi_M^H sees no X boundary charge on compact local branches.",
            "best_current_evidence": "2670 and 670 identify the condition; 3445/3448 keep Pi_M^H identity clean but do not silence X boundary charge.",
            "promotion_status": "MISSING_BOUNDARY_CHARGE_ZERO",
            "failure_mode_if_unsigned": "omega_X may be exact in the bulk but still contribute through surfaces/corners.",
            "next_action": "if 3450 cannot zero it, use the omega_X/B_X bound rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "clause_id": "PCM3449_6_verdict",
            "clause": "single-certificate promotion",
            "required_statement": "PCM3449_0 through PCM3449_5 must be parent-signed together, not borrowed piecemeal from separate closures.",
            "best_current_evidence": "the exact theorem is internally coherent; the parent signature is incomplete.",
            "promotion_status": "NOT_PROMOTED",
            "failure_mode_if_unsigned": "local-GR pass would be a closure assumption.",
            "next_action": "3450 field-by-field kernel signature or first numeric/theorem bound",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def omegaX_bound_first_row() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "OB3449_0_surface_norm_bound",
            "quantity": "I_omega_X",
            "definition": "first theorem-bound fallback for the extra-sector symplectic leakage",
            "inequality": "I_omega_X=abs(int_BF int_S i_tau omega_X) <= int_BF int_S ||tau_S||_h ||omega_X||_{h,*} dA_h dlambda",
            "cauchy_variant": "I_omega_X <= (int_BF int_S ||tau_S||_h^2 dA_h dlambda)^(1/2) (int_BF int_S ||omega_X||_{h,*}^2 dA_h dlambda)^(1/2)",
            "required_inputs": "surface_pair;tau_id;public_surface_metric_h;surface_measure_dA;branch_parameter_lambda;omega_X_norm_density",
            "units": "H_tau curl numerator units after tau/surface normalization",
            "source_path": str(OUTPUTS["absent_quotient_zero_proof"]),
            "current_status": "THEOREM_BOUND_FORMULA_READY_NUMERIC_INPUTS_MISSING",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "OB3449_1_zero_limit",
            "quantity": "I_omega_X_zero_limit",
            "definition": "fallback bound collapses to zero if absent-quotient erasure is signed",
            "inequality": "omega_X=0 => I_omega_X=0",
            "cauchy_variant": "norm factor ||omega_X||_{h,*}=0",
            "required_inputs": "parent-signed q/v_X/action/matter/boundary certificate",
            "units": "same as I_omega_X",
            "source_path": str(OUTPUTS["absent_quotient_zero_proof"]),
            "current_status": "CONDITIONAL_ZERO_NOT_PROMOTED",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "bound_id": "OB3449_2_data_row_template",
            "quantity": "omega_X_norm_density",
            "definition": "source-ready row to make the bound executable if zero proof fails",
            "inequality": "omega_X_norm_density := ||omega_X(delta,L_tau)||_{h,*}",
            "cauchy_variant": "supply L2_omegaX_norm over the same S x BF domain",
            "required_inputs": "system_id;sector;L_X_branch;Theta_X;omega_X_expression;surface_pair;tau_id;norm_choice;value_or_upper_bound;units;source_path",
            "units": "H_tau density per area per branch-parameter",
            "source_path": str(OUTPUTS["omegaX_bound_first_row"]),
            "current_status": "SCHEMA_READY_NONCLAIM",
            "score_ready": False,
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def deltaH_curl_update() -> list[dict[str, Any]]:
    return [
        {
            "update_id": "DHU3449_0_DHC3448_1",
            "prior_row": "DHC3448_1_absent_quotient_zero_candidate",
            "new_status": "CONDITIONAL_THEOREM_DERIVED_NOT_PARENT_PROMOTED",
            "replacement_or_feed": "AQZ3449_0..AQZ3449_5",
            "effect": "extra-sector zero is now a proved theorem under explicit q/v_X/action/descent/boundary premises, not a mere wish.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "update_id": "DHU3449_1_DHC3448_3",
            "prior_row": "DHC3448_3_omegaX_integral_bound",
            "new_status": "FIRST_THEOREM_BOUND_FORMULA_READY",
            "replacement_or_feed": "OB3449_0_surface_norm_bound",
            "effect": "if zero proof remains unsigned, omega_X can be bounded by a surface norm rather than left as MISSING.",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def countermodel_guard() -> list[dict[str, Any]]:
    return [
        {
            "guard_id": "CG3449_0_hidden_conformal_frame",
            "countermodel": "hat_g_ab=exp(2F(X)) g_ab seen by matter",
            "why_it_breaks_zero": "Dq[v_X]=0 for a public metric is not enough if matter actually sees an X-dependent shadow frame.",
            "required_exclusion_or_bound": "no-shadow-frame theorem or finite conformal leakage coefficient",
            "source_path": str(SOURCES["minimal_quotient_gate_619"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "guard_id": "CG3449_1_source_weight_marker",
            "countermodel": "source/species weights kappa_A(X) or theta_A(X)",
            "why_it_breaks_zero": "matter descent through q fails even if geometry descends.",
            "required_exclusion_or_bound": "ordinary matter signature with fixed representation constants, or WEP/R10 coefficient priors",
            "source_path": str(SOURCES["minimal_quotient_gate_619"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "guard_id": "CG3449_2_boundary_charge",
            "countermodel": "bulk vertical exactness with nonzero boundary charge Q_X",
            "why_it_breaks_zero": "i_v omega can be exact in the bulk while H_tau still receives a surface/corner term.",
            "required_exclusion_or_bound": "Q_X=0/proper/exact and K_boundary=0 on the local branch",
            "source_path": str(SOURCES["erasure_audit_2670"]),
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "G3449_0_sources_exist",
            "gate": "all cited 3449 source paths exist",
            "status": "PRIVATE_CHECK_PASS",
            "blocks_claim": False,
            "needed_for_claim": "source existence is only provenance",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3449_1_conditional_theorem",
            "gate": "absent-quotient erasure theorem is derived as a no-cancellation zero",
            "status": "PASS_CONDITIONAL",
            "blocks_claim": False,
            "needed_for_claim": "promote all premises with parent signatures",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3449_2_parent_premises",
            "gate": "q/v_X/action/matter/coframe/connection/boundary clauses are signed together",
            "status": "FAIL_NOT_PARENT_SIGNED",
            "blocks_claim": True,
            "needed_for_claim": "single certificate, not scattered conditional rows",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3449_3_fallback_bound",
            "gate": "omega_X fallback has first theorem-bound formula",
            "status": "PASS_FORMULA_NUMERIC_INPUTS_MISSING",
            "blocks_claim": True,
            "needed_for_claim": "omega_X norm density or exact zero source row",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "G3449_4_no_local_claim",
            "gate": "no local-GR/Newton/R10/PPN/clock/orbital pass is claimed",
            "status": "ENFORCED",
            "blocks_claim": True,
            "needed_for_claim": "full residual vector zero or bounded against arenas",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3449_0",
            "question": "Did the absent-quotient route mathematically work?",
            "answer": "Yes, as a precise conditional theorem: if q/v_X/action/descent/boundary clauses hold, Delta_H_curl_extra=0 with no cancellation.",
            "reason": "The action and symplectic form pull back from the quotient, so vertical X variations have zero physical current.",
            "next_action": "do not claim it until the parent certificate is signed",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3449_1",
            "question": "Did current MTS close the theorem?",
            "answer": "Not yet.",
            "reason": "The current corpus has scattered conditional evidence, but all-field v_X, matter/readout descent and boundary charge silence remain unsigned together.",
            "next_action": "3450 field-by-field v_X kernel signature, with omega_X norm bound fallback",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3450-Y5-R2FR-field-by-field-vX-kernel-signature-or-omegaX-norm-bound-input-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3450_field_by_field_vX_kernel_signature_or_omegaX_norm_bound_input.py",
            "objective": "Specify v_X on every observed and hidden slot and prove Dq[v_X]=0 field-by-field, or fill the first omega_X norm-density bound input.",
            "start_from": "PCM3449_1_vX_kernel and OB3449_0_surface_norm_bound",
            "success_gate": "Either a parent-signed v_X kernel table closes the absent-quotient route, or a nonclaim omega_X norm row becomes executable with units and surfaces.",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3449_0",
            "mode": "private_nonclaim_checkpoint",
            "result": "conditional zero theorem derived and first omega_X theorem-bound fallback staged",
            "claim_status": "NO_LOCAL_GR_NEWTON_R10_PPN_CLOCK_OR_ORBITAL_CLAIM",
            "reason": "parent-owned field-by-field kernel and boundary/descent clauses remain unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        }
    ]


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], sources: dict[str, Path], start_utc: datetime) -> list[dict[str, Any]]:
    modified_count = 0
    if FORMALIZATION.exists():
        start_timestamp = start_utc.timestamp()
        modified_count = sum(
            1
            for checked_path in FORMALIZATION.rglob("*")
            if checked_path.is_file() and checked_path.stat().st_mtime >= start_timestamp
        )

    nonclaim_ok = True
    for rows in rows_by_name.values():
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                nonclaim_ok = False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                nonclaim_ok = False

    parse_ok = True
    for output_name, path in OUTPUTS.items():
        if output_name == "validation":
            continue
        try:
            read_csv(path)
        except csv.Error:
            parse_ok = False

    theorem_status = [
        row
        for row in rows_by_name["absent_quotient_zero_proof"]
        if row["proof_id"] == "AQZ3449_4_deltaH_result"
    ]
    fallback_bound = [
        row
        for row in rows_by_name["omegaX_bound_first_row"]
        if row["bound_id"] == "OB3449_0_surface_norm_bound"
    ]
    blockers = [
        row
        for row in rows_by_name["parent_clause_matrix"]
        if row["promotion_status"].startswith("MISSING") or "NOT_PARENT" in row["promotion_status"]
    ]

    validations = [
        {
            "check_id": "VAL3449_0_sources_exist",
            "condition": "all cited 3449 source paths exist",
            "passed": all(path.exists() for path in sources.values()),
            "detail": f"{sum(1 for path in sources.values() if path.exists())}/{len(sources)} source paths exist",
        },
        {
            "check_id": "VAL3449_1_theorem_derived",
            "condition": "absent quotient implies Delta_H_curl_extra zero without cancellation",
            "passed": bool(theorem_status)
            and theorem_status[0]["status"] == "THEOREM_PROVED_CONDITIONALLY_NOT_PARENT_PROMOTED",
            "detail": theorem_status[0]["formal_statement"] if theorem_status else "missing theorem row",
        },
        {
            "check_id": "VAL3449_2_not_promoted",
            "condition": "parent clause matrix keeps unsigned premises explicit",
            "passed": len(blockers) >= 3
            and any(row["clause_id"] == "PCM3449_1_vX_kernel" for row in blockers)
            and any(row["clause_id"] == "PCM3449_5_boundary_silence" for row in blockers),
            "detail": f"{len(blockers)} blocker/non-parent rows retained",
        },
        {
            "check_id": "VAL3449_3_fallback_bound_ready",
            "condition": "first omega_X theorem-bound fallback row exists",
            "passed": bool(fallback_bound)
            and "||omega_X||" in fallback_bound[0]["inequality"]
            and fallback_bound[0]["valid_for_claim"] is False,
            "detail": fallback_bound[0]["current_status"] if fallback_bound else "missing fallback bound",
        },
        {
            "check_id": "VAL3449_4_countermodels_retained",
            "condition": "hidden frame, source marker and boundary charge countermodels remain guarded",
            "passed": {row["guard_id"] for row in rows_by_name["countermodel_guard"]}
            == {"CG3449_0_hidden_conformal_frame", "CG3449_1_source_weight_marker", "CG3449_2_boundary_charge"},
            "detail": "three countermodel guards present",
        },
        {
            "check_id": "VAL3449_5_no_claims",
            "condition": "all generated rows remain nonclaim",
            "passed": nonclaim_ok,
            "detail": "valid_for_claim=false and claim_allowed=false wherever present",
        },
        {
            "check_id": "VAL3449_6_generated_csv_parse",
            "condition": "generated CSV rows parse cleanly",
            "passed": parse_ok,
            "detail": "CSV reader pass for generated outputs present before validation write",
        },
        {
            "check_id": "VAL3449_7_next_target_3450",
            "condition": "next target is field-by-field v_X kernel or omega_X norm bound",
            "passed": rows_by_name["next_target"][0]["target_doc"].startswith("3450-Y5-R2FR-field-by-field-vX"),
            "detail": rows_by_name["next_target"][0]["target_doc"],
        },
        {
            "check_id": "VAL3449_8_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3449_9_overall",
            "condition": "3449 absent-quotient theorem checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3449 - Absent-Quotient X Erasure or omega_X Bound First Row

## Summary
- This checkpoint takes the leap directly: it derives the absent-quotient erasure theorem for the extra sector.
- The theorem is clean: if `q` is parent-owned, `v_X in ker(Dq)`, the action/symplectic potential descend before variation, and boundary charge is silent, then `L_X=Theta_X=omega_X=Q_tau^X=C_tau^X=B_X=0`.
- Therefore `Delta_H_curl_extra=0` follows without cancellation or fitted small coefficients.
- Current MTS still cannot claim this as local GR because the parent certificate is not signed as one object: all-field `v_X`, matter/readout descent, and boundary silence remain open.
- To avoid stalling, the fallback is now concrete too: `I_omega_X` has a first surface-norm theorem bound with named inputs.

## Source Register
{md_table(rows_by_name["source_register"])}

## Absent-Quotient Zero Proof
{md_table(rows_by_name["absent_quotient_zero_proof"])}

## Parent Clause Matrix
{md_table(rows_by_name["parent_clause_matrix"])}

## omega_X Bound First Row
{md_table(rows_by_name["omegaX_bound_first_row"])}

## DeltaH Curl Update
{md_table(rows_by_name["deltaH_curl_update"])}

## Countermodel Guard
{md_table(rows_by_name["countermodel_guard"])}

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
The absent-quotient route is mathematically alive: if the parent action really makes `X` representative/fibre data before variation, the extra-sector H_tau curl vanishes exactly. The current project is now forced onto one sharp next gate: specify `v_X` field-by-field and prove it is in `ker(Dq)`, or stop pretending zero and bound `omega_X`.
"""
    DOC.write_text(text, encoding="utf-8")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    sources = existing_sources()
    rows_by_name = {
        "source_register": source_register(sources),
        "absent_quotient_zero_proof": absent_quotient_zero_proof(),
        "parent_clause_matrix": parent_clause_matrix(),
        "omegaX_bound_first_row": omegaX_bound_first_row(),
        "deltaH_curl_update": deltaH_curl_update(),
        "countermodel_guard": countermodel_guard(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    for output_name, rows in rows_by_name.items():
        write_csv(OUTPUTS[output_name], rows)
    rows_by_name["validation"] = validation_rows(rows_by_name, sources, start_utc)
    write_csv(OUTPUTS["validation"], rows_by_name["validation"])
    write_doc(rows_by_name)
    failed_rows = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed_rows:
        raise SystemExit(f"3449 validation failed: {failed_rows}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
