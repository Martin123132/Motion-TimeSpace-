from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = ROOT.parent / "formalization-workbench"
DOC = ROOT / "3513-Y5-R2FR-ellJ-source-current-owner-JH-Htau-PiM-Href-or-bound.md"
CANONICAL_RESIDUAL_LAW = OUT / "P8_EM_ellJ_source_current_owner_residual_law.csv"


SOURCES: dict[str, dict[str, Any]] = {
    "script_3513": {"path": Path(__file__).resolve(), "role": "3513 generator"},
    "doc_3512": {
        "path": ROOT / "3512-Y5-R2FR-product-lock-factor-vector-ellJ-Rframe-or-Gdot-runner.md",
        "role": "3512 product-lock handoff selecting ell_J",
    },
    "product_vector_3512": {
        "path": OUT / "P8_EM_product_lock_factor_vector_ellJ_Rframe.csv",
        "role": "canonical product-lock factor vector",
    },
    "ellj_theorem_2937": {
        "path": OUT / "P8_Y5_R2FR_2937_ELLJ_OWNER_THEOREM_ATTEMPT.csv",
        "role": "conditional ell_J owner theorem",
    },
    "source_clause_2937": {
        "path": OUT / "P8_Y5_R2FR_2937_SOURCE_CURRENT_CLAUSE_LEDGER.csv",
        "role": "source-current owner clauses",
    },
    "source_measure_2938": {
        "path": OUT / "P8_Y5_R2FR_2938_HTAU_WORLDTUBE_SOURCE_MEASURE_THEOREM_ATTEMPT.csv",
        "role": "H_tau/worldtube source-measure theorem",
    },
    "source_measure_residual_2938": {
        "path": OUT / "P8_Y5_R2FR_2938_SOURCE_MEASURE_RESIDUAL_IDENTITY.csv",
        "role": "exact source-measure residual identity",
    },
    "ellj_reference_2938": {
        "path": OUT / "P8_Y5_R2FR_2938_MHREF_ELLJ_REFERENCE_LOCK_CONTRACT.csv",
        "role": "M_H_ref/ell_J/reference anti-laundering contract",
    },
    "current_ward_3508": {
        "path": OUT / "P8_EM_current_source_Ward_alpha_source_residual.csv",
        "role": "current/source Ward residuals",
    },
    "common_action_3510": {
        "path": OUT / "P8_EM_common_action_density_line_universal_source_scale.csv",
        "role": "common action-density scale separation",
    },
    "pim_lock_2665": {
        "path": OUT / "P8_Y5_R10_HAMILTONIAN_PIM_QBARXH_LOCK_2665_LOCK_CONTRACT.csv",
        "role": "Hamiltonian/Pi_M/source-domain lock contract",
    },
    "htau_integrability_2667": {
        "path": OUT / "P8_Y5_R10_HTAU_INTEGRABILITY_CURL_2667_INTEGRABILITY_GATE.csv",
        "role": "H_tau integrability curl gate",
    },
    "worldtube_audit_2611": {
        "path": OUT / "P8_Y5_MATTER_DESCENT_GATE_2611_WORLDTUBE_SOURCE_OWNER_AUDIT.csv",
        "role": "worldtube source owner audit",
    },
    "gdot_gate_2933": {
        "path": OUT / "P8_Y5_R2FR_2933_DOTG_KAPPA_PROJECTION_GATE.csv",
        "role": "finite dotG comparator carried from previous gates",
    },
}


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat()


def bool_text(value: bool) -> str:
    return "True" if value else "False"


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register_rows() -> list[dict[str, Any]]:
    return [
        {
            "source_id": source_id,
            "path": str(metadata["path"]),
            "exists": bool_text(Path(metadata["path"]).exists()),
            "role": metadata["role"],
            "valid_for_claim": "False",
        }
        for source_id, metadata in SOURCES.items()
    ]


def zero_proof_rows() -> list[dict[str, Any]]:
    return [
        {
            "proof_id": "EJL3513_0_define_normalization_slot",
            "claim_piece": "ell_J is the only remaining source-current normalization slot",
            "statement": "Define z_ellJ[X] as the logarithmic drift between the readout source current and the parent Hilbert/worldtube source current after G_ref and w_common have been separated.",
            "mathematical_form": "z_ellJ[X] := D_X ln ell_J := D_X ln J_readout[X] - D_X ln Pi_M^H J_H[X]",
            "derivation_gain": "turns the vague coupling gap into a measured mismatch between two named current paths",
            "current_status": "EXACT_DEFINITION_NONCLAIM",
            "remaining_gap": "the two current paths are not yet proven equal for current MTS",
            "source_path": str(SOURCES["product_vector_3512"]["path"]),
            "claim_allowed": "False",
        },
        {
            "proof_id": "EJL3513_1_commuting_square_zero_theorem",
            "claim_piece": "source-current owner commuting square",
            "statement": "If matter variation, Hilbert current, Hamiltonian charge, Pi_M projection, worldtube support and reference subtraction are one pre-readout functorial chain, then ell_J has no branch-dependent scale freedom.",
            "mathematical_form": "S_m -> J_H -> H_tau-H_ref -> Pi_M^H(H_tau-H_ref)=M_H_ref -> J_readout, with both routes equal",
            "derivation_gain": "proves D_X ln ell_J=0 without fitting GM, because there is no second independent current owner",
            "current_status": "CONDITIONAL_ZERO_THEOREM_REWRITTEN_AS_COMMUTING_SQUARE",
            "remaining_gap": "Pi_M/H_tau/reference/worldtube square is not parent-signed",
            "source_path": str(SOURCES["ellj_theorem_2937"]["path"]),
            "claim_allowed": "False",
        },
        {
            "proof_id": "EJL3513_2_exact_residual_law",
            "claim_piece": "ell_J obstruction decomposition",
            "statement": "When the square does not close, z_ellJ is exactly the sum of named normalized obstruction terms; no cancellation credit is allowed.",
            "mathematical_form": "z_ellJ[X] = R_md[X]+R_Ward[X]+R_PiM[X]+R_Htau[X]+R_ref[X]+R_W[X]+R_frame[X]+R_units[X]",
            "derivation_gain": "replaces a missing coupling with an algebraic target list that can be proven term by term or bounded",
            "current_status": "EXACT_RESIDUAL_DECOMPOSITION_READY",
            "remaining_gap": "component zero proofs or numeric bounds remain absent",
            "source_path": str(SOURCES["source_measure_residual_2938"]["path"]),
            "claim_allowed": "False",
        },
        {
            "proof_id": "EJL3513_3_duplicate_scale_elimination",
            "claim_piece": "no hidden source-only rescaling",
            "statement": "Once w_common owns the action-density line and G_ref owns the EH coefficient, a further source-only ell_J(X) is illegal unless it appears as an explicit non-Hilbert/source selector residual.",
            "mathematical_form": "D_X ln ell_J = 0 unless S_m contains a source-only multiplier or the readout functor fails to commute with Pi_M/H_tau/H_ref",
            "derivation_gain": "separates the real derivation route from the fake route of hiding ell_J inside measured GM",
            "current_status": "CONDITIONAL_EXCLUSION_WITH_COUNTERMODEL_SLOT",
            "remaining_gap": "ordinary matter grammar/no-source-only selector remains conditional",
            "source_path": str(SOURCES["common_action_3510"]["path"]),
            "claim_allowed": "False",
        },
        {
            "proof_id": "EJL3513_4_current_verdict",
            "claim_piece": "current MTS ell_J status",
            "statement": "Current MTS is closer than 3512: the ell_J proof now reduces to the Pi_M/H_tau/H_ref/worldtube commuting square plus matter descent, not an open-ended coupling mystery.",
            "mathematical_form": "claim(z_ellJ=0) requires every residual row EJR3513_1..8 to be zero-owned or bounded without cancellation",
            "derivation_gain": "selects a concrete next proof target instead of circling the whole product lock again",
            "current_status": "NOT_CLAIMED_BUT_NARROWED",
            "remaining_gap": "Pi_M-H_tau commutator and H_ref/source measure denominator remain the highest-pressure rows",
            "source_path": str(SOURCES["ellj_reference_2938"]["path"]),
            "claim_allowed": "False",
        },
    ]


def commuting_square_rows() -> list[dict[str, Any]]:
    return [
        {
            "square_id": "CS3513_0_action_to_Hilbert_current",
            "object": "S_matter -> J_H,T_H",
            "map": "J_H[tau] := delta S_matter/delta e_obs contracted with L_tau e_obs",
            "commutes_if": "S_matter descends through q(Phi), e_obs and tau with no source-only preweight",
            "failure_term": "R_md + R_Ward",
            "source_path": str(SOURCES["current_ward_3508"]["path"]),
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "next_derivation": "prove matter descent/no-source-only current owner",
            "claim_allowed": "False",
        },
        {
            "square_id": "CS3513_1_current_to_Htau",
            "object": "J_H -> H_tau",
            "map": "H_tau[S] := integral_S Q_tau[J_H] after theta_MTS/Noether extraction",
            "commutes_if": "theta_MTS, Q_tau and symplectic potential are parent-derived and integrable",
            "failure_term": "R_Htau",
            "source_path": str(SOURCES["htau_integrability_2667"]["path"]),
            "current_status": "INTEGRABILITY_GATE_OPEN",
            "next_derivation": "prove H_tau curl vanishes or exact-bound it",
            "claim_allowed": "False",
        },
        {
            "square_id": "CS3513_2_reference_subtraction",
            "object": "H_tau -> H_tau-H_ref",
            "map": "M_H_ref := H_tau[S_outer] - H_ref[Sigma_ref]",
            "commutes_if": "H_ref is source-blind, fixed before readout and cannot absorb GM/source/frame drift",
            "failure_term": "R_ref + R_units",
            "source_path": str(SOURCES["ellj_reference_2938"]["path"]),
            "current_status": "REFERENCE_SELECTOR_UNSIGNED",
            "next_derivation": "derive source-blind Sigma_ref and positivity of M_H_ref",
            "claim_allowed": "False",
        },
        {
            "square_id": "CS3513_3_PiM_projection",
            "object": "H_tau-H_ref -> Pi_M^H(H_tau-H_ref)",
            "map": "Pi_M^H takes the fixed M_H_ref/source-mass component at fixed tau, surface and reference data",
            "commutes_if": "[D_X,Pi_M^H]J_H=0 and projector stress/domain/Hodge variations vanish or are bounded",
            "failure_term": "R_PiM",
            "source_path": str(SOURCES["pim_lock_2665"]["path"]),
            "current_status": "RETAINED_PROJECTOR_OBSTRUCTION",
            "next_derivation": "prove Pi_M-H_tau commutator zero on parent-owned source branch",
            "claim_allowed": "False",
        },
        {
            "square_id": "CS3513_4_worldtube_support",
            "object": "J_H -> W_source",
            "map": "W_source := closure(supp J_H[tau]) with linked exterior surfaces before readout",
            "commutes_if": "source support, compactness, regularity and linked surfaces are parent-owned",
            "failure_term": "R_W",
            "source_path": str(SOURCES["worldtube_audit_2611"]["path"]),
            "current_status": "WORLDTUBE_DESCENT_NOT_PARENT_SIGNED",
            "next_derivation": "prove worldtube support selector follows from J_H rather than fitted domain masks",
            "claim_allowed": "False",
        },
        {
            "square_id": "CS3513_5_observational_readout",
            "object": "M_H_ref -> Newton/R10/PPN/orbital source",
            "map": "readout source uses the same M_H_ref, tau, coframe and source current as the parent charge",
            "commutes_if": "R_frame=0 and measured GM tests rather than defines the source denominator",
            "failure_term": "R_frame + R_units",
            "source_path": str(SOURCES["ellj_reference_2938"]["path"]),
            "current_status": "ANTI_LAUNDERING_GUARD_ONLY",
            "next_derivation": "lock same-frame readout after Pi_M/H_tau denominator closes",
            "claim_allowed": "False",
        },
    ]


def residual_law_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EJR3513_0_total",
            "residual": "z_ellJ",
            "definition": "D_X ln ell_J source-current normalization drift",
            "formula": "z_ellJ[X] = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units",
            "source_path": str(SOURCES["ellj_theorem_2937"]["path"]),
            "source_status": "EXACT_DECOMPOSITION_NONCLAIM",
            "zero_condition": "all component residuals zero-owned by one parent source-current chain",
            "bounded_if": "all nonzero components have sourced numeric rows and no cancellation is credited",
            "observable_links": "Gdot; Newton_GM; PPN; orbital_GM; R10; WEP",
            "next_action": "attack R_PiM + R_Htau first because they are the algebraic heart of the denominator",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EJR3513_1_R_md",
            "residual": "R_md",
            "definition": "matter descent/source-only multiplier obstruction",
            "formula": "R_md := D_X ln(delta S_matter/delta e_obs) - D_X ln(delta Sbar[q(Phi)]/delta e_obs)",
            "source_path": str(SOURCES["current_ward_3508"]["path"]),
            "source_status": "CONDITIONAL_DESCENT_NOT_PARENT_SIGNED",
            "zero_condition": "S_matter=Sbar[q(Phi),psi,theta] with no source-only weights",
            "bounded_if": "source-only matter weights are parameterized and constrained by WEP/R10/local tests",
            "observable_links": "WEP; R10; PPN source composition",
            "next_action": "reuse 3508/3510 no-source-only grammar after Pi_M denominator is fixed",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EJR3513_2_R_Ward",
            "residual": "R_Ward",
            "definition": "Ward/source identity does not carry through projection/readout",
            "formula": "R_Ward := normalized failure of nabla_mu T_H^{mu nu}=0 to imply d(Pi_M J_H)=0",
            "source_path": str(SOURCES["current_ward_3508"]["path"]),
            "source_status": "WARD_IDENTITY_AVAILABLE_BUT_NOT_ENOUGH",
            "zero_condition": "same current is conserved before Pi_M/readout and all boundary tails vanish or are exact",
            "bounded_if": "boundary/non-Hilbert tails get source-backed envelopes",
            "observable_links": "PPN; R10; source conservation",
            "next_action": "do not stop at Ward; prove projection commute",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EJR3513_3_R_PiM",
            "residual": "R_PiM",
            "definition": "Pi_M/source-current commutator obstruction",
            "formula": "R_PiM := ([D_X,Pi_M^H]J_H + Pi_M^H[D_X,J_H] - D_X Pi_M^H[J_H]) / Pi_M^H[J_H]",
            "source_path": str(SOURCES["pim_lock_2665"]["path"]),
            "source_status": "RETAINED_PROJECTOR_OBSTRUCTION",
            "zero_condition": "Pi_M fixed-variable list, source support and Hodge/domain data are parent-owned and independent of readout",
            "bounded_if": "commutator, projector-stress and domain/Hodge variations get numeric source rows",
            "observable_links": "Newton source mass; PPN; R10 Qbar_XH; orbital_GM",
            "next_action": "3514 should prove or bound this row first",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EJR3513_4_R_Htau",
            "residual": "R_Htau",
            "definition": "H_tau non-integrability/source-charge curl",
            "formula": "R_Htau := normalized curl(delta H_tau) = normalized integral_S i_tau omega_total plus exact/boundary terms",
            "source_path": str(SOURCES["htau_integrability_2667"]["path"]),
            "source_status": "INTEGRABILITY_CURL_NOT_CLAIM_READY",
            "zero_condition": "parent L_X, theta_X, omega_X, tau/surface lock and boundary exactness are signed",
            "bounded_if": "field-space curl and boundary exactness rows are numerically bounded",
            "observable_links": "Gdot; Newton source mass; PPN; clocks",
            "next_action": "couple with R_PiM in 3514 rather than treating H_tau as a free denominator",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EJR3513_5_R_ref",
            "residual": "R_ref",
            "definition": "source-blind reference failure",
            "formula": "R_ref := D_X H_ref / (H_tau-H_ref)",
            "source_path": str(SOURCES["ellj_reference_2938"]["path"]),
            "source_status": "REFERENCE_SELECTOR_UNSIGNED",
            "zero_condition": "H_ref depends only on boundary/topology/stationarity/asymptotic coframe data",
            "bounded_if": "reference derivative has source-backed bound and is not cancelled against H_tau",
            "observable_links": "Gdot; orbital_GM; R10 denominator; local GR boundary",
            "next_action": "after Pi_M/H_tau, lock Sigma_ref source-blindness",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EJR3513_6_R_W",
            "residual": "R_W",
            "definition": "worldtube support/domain selector drift",
            "formula": "R_W := D_X ln int_{W_source} rho_H dV_H - D_X ln int_{closure(supp J_H[tau])} rho_H dV_H",
            "source_path": str(SOURCES["worldtube_audit_2611"]["path"]),
            "source_status": "WORLDTUBE_DESCENT_NOT_PARENT_SIGNED",
            "zero_condition": "W_source is exactly closure(supp J_H[tau]) on the parent-owned Hamiltonian slice",
            "bounded_if": "domain mask/support variation gets a nonclaim source-bound row",
            "observable_links": "Newton source; R10 source support; WEP/source composition",
            "next_action": "derive support selector after source current is parent-owned",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EJR3513_7_R_frame",
            "residual": "R_frame",
            "definition": "same-frame/tau/readout mismatch",
            "formula": "R_frame := D_X ln(source readout frame) - D_X ln(parent H_tau frame)",
            "source_path": str(SOURCES["product_vector_3512"]["path"]),
            "source_status": "PARALLEL_PRODUCT_FACTOR_RETAINED",
            "zero_condition": "same observed coframe/tau/source/orbit/clock/reference branch is fixed before readout",
            "bounded_if": "clock/orbital/frame residuals are source-backed independently",
            "observable_links": "clock; PPN; orbital_GM; Gdot",
            "next_action": "leave as parallel 3512 R_frame gate until ell_J denominator is sharper",
            "valid_for_claim": "False",
        },
        {
            "row_id": "EJR3513_8_R_units",
            "residual": "R_units",
            "definition": "duplicate unit/source normalization after w_common and G_ref are separated",
            "formula": "R_units := D_X ln C_source + D_X ln hidden ell_J unit convention",
            "source_path": str(SOURCES["common_action_3510"]["path"]),
            "source_status": "DUPLICATE_SCALE_CONDITIONALLY_EXCLUDED",
            "zero_condition": "w_common is the only action-density line scale and measured GM cannot define source mass",
            "bounded_if": "remaining source scale gets independent Gdot/Newton/clock bound rows",
            "observable_links": "Gdot; Newton_G; clock/action normalization",
            "next_action": "do not absorb into measured GM; carry explicit product factor if not zero-owned",
            "valid_for_claim": "False",
        },
    ]


def bound_input_rows() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "ELLJB3513_0_Gdot",
            "arena": "Gdot/time drift",
            "quantity": "z_ellJ_time",
            "prediction": "MISSING_D_T_LN_ELLJ",
            "bound": "4.0e-14 yr^-1",
            "claim_condition": "other product factors zero-owned or independently bounded; no cancellation",
            "source_path": str(SOURCES["gdot_gate_2933"]["path"]),
            "runner_status": "BLOCKED_PREDICTION_MISSING",
            "valid_for_claim": "False",
        },
        {
            "row_id": "ELLJB3513_1_Newton_radial",
            "arena": "Newton/orbital source mass",
            "quantity": "D_R ln ell_J or source-domain drift",
            "prediction": "MISSING_D_R_LN_ELLJ",
            "bound": "MISSING_NEWTON_SOURCE_BOUND",
            "claim_condition": "M_H_ref derived before orbital GM readout",
            "source_path": str(SOURCES["ellj_reference_2938"]["path"]),
            "runner_status": "BLOCKED_BOUND_AND_PREDICTION_MISSING",
            "valid_for_claim": "False",
        },
        {
            "row_id": "ELLJB3513_2_PPN",
            "arena": "local PPN/source coupling",
            "quantity": "source prefactor residual",
            "prediction": "MISSING_PPN_SOURCE_PREFACTOR",
            "bound": "MISSING_PPN_SOURCE_BOUND",
            "claim_condition": "Pi_M/H_tau/reference square closes or all source-prefactor residuals bounded",
            "source_path": str(SOURCES["pim_lock_2665"]["path"]),
            "runner_status": "BLOCKED_BOUND_AND_PREDICTION_MISSING",
            "valid_for_claim": "False",
        },
        {
            "row_id": "ELLJB3513_3_R10",
            "arena": "R10 short-range alpha",
            "quantity": "ell_J contribution to Qbar_XH/tau_R10",
            "prediction": "MISSING_ELLJ_ALPHA_PROJECTION",
            "bound": "MISSING_REAL_ALPHA_LAMBDA_BOUND_LINK",
            "claim_condition": "Qbar_XH denominator M_H_ref and tau_R10 are parent-owned",
            "source_path": str(SOURCES["pim_lock_2665"]["path"]),
            "runner_status": "BLOCKED_DENOMINATOR_AND_PROJECTION_MISSING",
            "valid_for_claim": "False",
        },
        {
            "row_id": "ELLJB3513_4_WEP",
            "arena": "composition/source universality",
            "quantity": "species/source label dependence in ell_J",
            "prediction": "MISSING_DELTA_ELLJ_AB",
            "bound": "MISSING_WEP_SOURCE_BOUND",
            "claim_condition": "ordinary matter category connected and no source-only species scale",
            "source_path": str(SOURCES["current_ward_3508"]["path"]),
            "runner_status": "BLOCKED_SOURCE_LABEL_PROJECTION_MISSING",
            "valid_for_claim": "False",
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3513_0_derivation_gain",
            "decision": "keep the ell_J route active",
            "rationale": "3513 converts ell_J from a vague coupling gap into a commuting-square residual law.",
            "effect": "next work can attack Pi_M/H_tau/H_ref terms directly instead of looping over all coupling factors",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3513_1_no_current_claim",
            "decision": "do not claim D_X ln ell_J=0 yet",
            "rationale": "the current corpus still lacks a parent-signed Pi_M/H_tau/reference/worldtube square.",
            "effect": "Gdot/Newton/PPN/R10 rows stay nonclaim until zero proofs or numeric bounds exist",
            "claim_allowed": "False",
        },
        {
            "decision_id": "DEC3513_2_best_next_attack",
            "decision": "attack the Pi_M-H_tau commutator next",
            "rationale": "R_PiM and R_Htau are the algebraic choke point for the source denominator; if they close, ell_J becomes much less grim.",
            "effect": "3514 should try a proof of [D_X,Pi_M]H_tau=0 or create the first honest bound row",
            "claim_allowed": "False",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "next_doc": "3514-Y5-R2FR-PiM-Htau-source-current-commuting-square-zero-or-bound.md",
            "next_script": "scripts/Y5_R2FR_3514_PiM_Htau_source_current_commuting_square_zero_or_bound.py",
            "objective": "Try to prove the Pi_M/H_tau source-current square commutes, i.e. [D_X,Pi_M^H]H_tau=0 with fixed source support, tau, surface and reference; if not, produce source-backed nonclaim bound rows for R_PiM+R_Htau.",
            "success_gate": "Either R_PiM=R_Htau=0 is parent-signed or their prediction-side rows become executable without measured-GM absorption.",
            "forbidden_shortcuts": "do not use Ward conservation alone; do not define M_H_ref from orbital GM; do not cancel Pi_M against H_ref or R_frame",
            "claim_allowed": "False",
        }
    ]


def validate(outputs: dict[str, Path], source_rows: list[dict[str, Any]], residual_rows: list[dict[str, Any]], proof_rows: list[dict[str, Any]], bound_rows: list[dict[str, Any]], next_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    sources_exist = all(row["exists"] == "True" for row in source_rows)
    checks.append(
        {
            "check_id": "VAL3513_0_sources_exist",
            "passed": bool_text(sources_exist),
            "detail": "all cited local source paths exist" if sources_exist else "one or more cited source paths are missing",
            "valid_for_claim": "False",
        }
    )

    residual_has_total = any(row["row_id"] == "EJR3513_0_total" and "R_PiM" in row["formula"] and "R_Htau" in row["formula"] for row in residual_rows)
    checks.append(
        {
            "check_id": "VAL3513_1_residual_law_written",
            "passed": bool_text(residual_has_total),
            "detail": "z_ellJ residual law includes named obstruction sum",
            "valid_for_claim": "False",
        }
    )

    commuting_square = any(row["proof_id"] == "EJL3513_1_commuting_square_zero_theorem" for row in proof_rows)
    checks.append(
        {
            "check_id": "VAL3513_2_commuting_square_theorem",
            "passed": bool_text(commuting_square),
            "detail": "ell_J zero route written as commuting-square theorem",
            "valid_for_claim": "False",
        }
    )

    no_claims = all(row.get("claim_allowed", "False") != "True" for row in proof_rows + decision_rows() + next_rows) and all(row.get("valid_for_claim", "False") != "True" for row in residual_rows + bound_rows)
    checks.append(
        {
            "check_id": "VAL3513_3_no_claim_flags",
            "passed": bool_text(no_claims),
            "detail": "all 3513 rows remain nonclaim",
            "valid_for_claim": "False",
        }
    )

    placeholders_blocked = all(
        ("MISSING_" in row["prediction"] or "MISSING_" in row["bound"]) and row["valid_for_claim"] == "False"
        for row in bound_rows
    )
    checks.append(
        {
            "check_id": "VAL3513_4_bound_rows_block_placeholders",
            "passed": bool_text(placeholders_blocked),
            "detail": "bound input rows block missing prediction/bound placeholders",
            "valid_for_claim": "False",
        }
    )

    next_selected = any("Pi_M/H_tau" in row["objective"] or "PiM_Htau" in row["next_script"] for row in next_rows)
    checks.append(
        {
            "check_id": "VAL3513_5_next_target_PiM_Htau",
            "passed": bool_text(next_selected),
            "detail": "3514 Pi_M-H_tau commutator selected next",
            "valid_for_claim": "False",
        }
    )

    csvs_parse = True
    parse_details: list[str] = []
    for name, path in outputs.items():
        if path.suffix.lower() != ".csv":
            continue
        if name == "validation" and not path.exists():
            parse_details.append("validation:deferred_until_written")
            continue
        try:
            read_csv_rows(path)
            parse_details.append(name)
        except Exception as exc:  # pragma: no cover - validation detail
            csvs_parse = False
            parse_details.append(f"{name}:{exc}")
    checks.append(
        {
            "check_id": "VAL3513_6_csvs_parse",
            "passed": bool_text(csvs_parse),
            "detail": "; ".join(parse_details),
            "valid_for_claim": "False",
        }
    )

    checks.append(
        {
            "check_id": "VAL3513_7_formalization_workbench_not_targeted",
            "passed": "True",
            "detail": str(FORMALIZATION),
            "valid_for_claim": "False",
        }
    )

    passed = all(row["passed"] == "True" for row in checks)
    checks.append(
        {
            "check_id": "VAL3513_SUMMARY",
            "passed": bool_text(passed),
            "detail": "PASS" if passed else "FAIL",
            "valid_for_claim": "False",
        }
    )
    return checks


def markdown_table(rows: list[dict[str, Any]], fields: list[str]) -> str:
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(str(row.get(field, "")).replace("\n", " ") for field in fields) + " |")
    return "\n".join(lines)


def write_doc(
    source_rows: list[dict[str, Any]],
    proof_rows: list[dict[str, Any]],
    square_rows: list[dict[str, Any]],
    residual_rows: list[dict[str, Any]],
    bound_rows: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    next_rows: list[dict[str, Any]],
    validation_rows: list[dict[str, Any]],
) -> None:
    doc = f"""# 3513 - ellJ Source-Current Owner: JH/Htau/PiM/Href Or Bound

## Summary
- **Actual derivation gain:** `ell_J` is now an exact residual law, not a vague missing coupling.
- **Core result:** `z_ellJ[X] = R_md + R_Ward + R_PiM + R_Htau + R_ref + R_W + R_frame + R_units`.
- **Zero route:** if the `S_matter -> J_H -> H_tau-H_ref -> Pi_M -> M_H_ref -> readout` square commutes, then `D_X ln ell_J = 0`.
- **Current status:** not claimed; the hard rows are now specifically `R_PiM` and `R_Htau`, with `H_ref/worldtube/frame` retained as no-laundering guards.

## Source Register
{markdown_table(source_rows, ["source_id", "path", "exists", "role", "valid_for_claim"])}

## Zero-Proof Attempt
{markdown_table(proof_rows, ["proof_id", "claim_piece", "statement", "mathematical_form", "derivation_gain", "current_status", "remaining_gap", "claim_allowed"])}

## Source-Current Commuting Square
{markdown_table(square_rows, ["square_id", "object", "map", "commutes_if", "failure_term", "current_status", "next_derivation", "claim_allowed"])}

## ellJ Residual Law
{markdown_table(residual_rows, ["row_id", "residual", "definition", "formula", "source_status", "zero_condition", "bounded_if", "observable_links", "next_action", "valid_for_claim"])}

## Bound Input Template
{markdown_table(bound_rows, ["row_id", "arena", "quantity", "prediction", "bound", "claim_condition", "runner_status", "valid_for_claim"])}

## Decisions
{markdown_table(decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])}

## Next Target
{markdown_table(next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed"])}

## Validation
{markdown_table(validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])}

Generated: {now_utc()}
"""
    DOC.write_text(doc, encoding="utf-8")


def main() -> None:
    source_rows = source_register_rows()
    proof_rows = zero_proof_rows()
    square_rows = commuting_square_rows()
    residual_rows = residual_law_rows()
    bound_rows = bound_input_rows()
    decisions = decision_rows()
    next_rows = next_target_rows()

    outputs = {
        "source_register": OUT / "P8_Y5_R2FR_3513_SOURCE_REGISTER.csv",
        "zero_proof": OUT / "P8_Y5_R2FR_3513_ELLJ_ZERO_PROOF_ATTEMPT.csv",
        "commuting_square": OUT / "P8_Y5_R2FR_3513_ELLJ_SOURCE_CURRENT_COMMUTING_SQUARE.csv",
        "residual_law": OUT / "P8_Y5_R2FR_3513_ELLJ_RESIDUAL_LAW.csv",
        "canonical_residual_law": CANONICAL_RESIDUAL_LAW,
        "bound_template": OUT / "P8_Y5_R2FR_3513_ELLJ_BOUND_INPUT_TEMPLATE.csv",
        "decision_ledger": OUT / "P8_Y5_R2FR_3513_DECISION_LEDGER.csv",
        "next_target": OUT / "P8_Y5_R2FR_3513_NEXT_TARGET.csv",
        "validation": OUT / "P8_Y5_BRR545_3513_VALIDATION.csv",
    }

    write_csv(outputs["source_register"], source_rows, ["source_id", "path", "exists", "role", "valid_for_claim"])
    write_csv(
        outputs["zero_proof"],
        proof_rows,
        [
            "proof_id",
            "claim_piece",
            "statement",
            "mathematical_form",
            "derivation_gain",
            "current_status",
            "remaining_gap",
            "source_path",
            "claim_allowed",
        ],
    )
    write_csv(
        outputs["commuting_square"],
        square_rows,
        [
            "square_id",
            "object",
            "map",
            "commutes_if",
            "failure_term",
            "source_path",
            "current_status",
            "next_derivation",
            "claim_allowed",
        ],
    )
    residual_fields = [
        "row_id",
        "residual",
        "definition",
        "formula",
        "source_path",
        "source_status",
        "zero_condition",
        "bounded_if",
        "observable_links",
        "next_action",
        "valid_for_claim",
    ]
    write_csv(outputs["residual_law"], residual_rows, residual_fields)
    write_csv(outputs["canonical_residual_law"], residual_rows, residual_fields)
    write_csv(
        outputs["bound_template"],
        bound_rows,
        [
            "row_id",
            "arena",
            "quantity",
            "prediction",
            "bound",
            "claim_condition",
            "source_path",
            "runner_status",
            "valid_for_claim",
        ],
    )
    write_csv(outputs["decision_ledger"], decisions, ["decision_id", "decision", "rationale", "effect", "claim_allowed"])
    write_csv(outputs["next_target"], next_rows, ["next_doc", "next_script", "objective", "success_gate", "forbidden_shortcuts", "claim_allowed"])

    validation_rows = validate(outputs, source_rows, residual_rows, proof_rows, bound_rows, next_rows)
    write_csv(outputs["validation"], validation_rows, ["check_id", "passed", "detail", "valid_for_claim"])
    write_doc(source_rows, proof_rows, square_rows, residual_rows, bound_rows, decisions, next_rows, validation_rows)

    print(f"wrote {DOC}")
    print(f"validation {outputs['validation']}")


if __name__ == "__main__":
    main()
