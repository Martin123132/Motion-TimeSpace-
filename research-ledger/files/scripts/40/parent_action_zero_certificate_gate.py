from __future__ import annotations

import csv
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


def parent_action_certificate_rows() -> List[Dict[str, object]]:
    return [
        {
            "certificate_id": "PAC4467_0_common_mode_normal_form",
            "target": "C_matter=0 source silence",
            "exact_certificate": "S_parent = S_geom[q(Phi),chi] + S_matter[Psi,g_obs(q(Phi)),theta0] with no A(chi), no theta_j(chi), no hidden matter operator and no source-prefactor slot",
            "derivation_if_signed": "delta_chi S_matter=0, hence C_matter=d ln A/dchi=0 and alpha_eff=C_matter^2/3=0",
            "current_evidence": "193/4265/4277 give the quotient chain-rule zero inside the standard branch; 4332 keeps Xi_open outside it",
            "current_status": "CONDITIONAL_STANDARD_BRANCH_ONLY_NOT_GLOBAL_PARENT_SIGNED",
            "signed_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "PAC4467_1_actual_vertical_generator",
            "target": "chi is representative/vertical rather than physical",
            "exact_certificate": "there is a parent q and actual v_chi such that Dq[v_chi]=0, v_chi is field-by-field specified and integrable",
            "derivation_if_signed": "chi has no physical local pole/source row before variation",
            "current_evidence": "637/581/670 provide conditional quotient math; 1023 says the single q/v_X/action certificate fails current claim",
            "current_status": "PARTIAL_CONDITIONAL_Q_KERNEL_ACTUAL_VCHI_UNSIGNED",
            "signed_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "PAC4467_2_matter_descent",
            "target": "matter/source silence",
            "exact_certificate": "S_matter=Sbar_m[Psi,g_obs(q(Phi)),theta_obs(q(Phi))] and L_vchi theta_obs=0 with hidden conformal/disformal channels excluded",
            "derivation_if_signed": "delta_vchi S_matter=0; no qbar_XT and no common matter source charge",
            "current_evidence": "4277 derives delta_v S_matter=0 and g_X=b_dis=0 only in the standard branch; 1023/4332 retain hidden-frame/source-label tails outside it",
            "current_status": "CONDITIONAL_BRANCH_ZERO_HIDDEN_TAILS_OPEN",
            "signed_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "PAC4467_3_boundary_degree_silence",
            "target": "no edge/degree scalar pole",
            "exact_certificate": "Q_chi=0/proper/exact, bracket closure, first-class pair removes chi pair, and reduced symplectic form has no chi stabilizer",
            "derivation_if_signed": "K_X=Qbar_XH=0 and no boundary-hair alpha row",
            "current_evidence": "1023 and 670 both keep boundary, momentum-map and degree-count clauses unsigned",
            "current_status": "BOUNDARY_AND_DEGREE_COUNT_UNSIGNED",
            "signed_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "PAC4467_4_refinement_cR2_zero",
            "target": "c_R2_eff=0 scalar absence",
            "exact_certificate": "quotient/projective refinement groupoid + cylindrical first-moment action + additive signed hinge flux + parent-owned hinge/connection/coframe + no physical grain + no second channel",
            "derivation_if_signed": "S_n(delta)=n Phi(delta/n)=Phi(delta) kills Phi''(0), so c2_visible=0 and c_R2_eff=0 in the same channel",
            "current_evidence": "4459 proves the math; 4460 marks groupoid/cylindrical/geometry/no-second-channel clauses not parent-signed; 4461 maps finite fallback",
            "current_status": "EXACT_CONDITIONAL_THEOREM_FULL_PARENT_CERTIFICATE_UNSIGNED",
            "signed_now": False,
            "valid_for_claim": False,
        },
        {
            "certificate_id": "PAC4467_5_verdict",
            "target": "local-GR scalar/common-mode claim",
            "exact_certificate": "either PAC4467_0-3 source-silence certificate signs, or PAC4467_4 refinement certificate signs",
            "derivation_if_signed": "alpha_eff=0 by source silence or no scalar pole; calibrated G cannot hide a fifth force",
            "current_evidence": "both certificates have exact proof language but missing parent signatures",
            "current_status": "NO_PUBLIC_LOCAL_GR_SCALAR_CLOSURE_FINITE_BRANCH_RETAINED",
            "signed_now": False,
            "valid_for_claim": False,
        },
    ]


def source_silence_audit_rows() -> List[Dict[str, object]]:
    return [
        {
            "audit_id": "SSA4467_0_chain_rule_theorem",
            "claim_piece": "matter action descends through quotient data",
            "formula": "S_matter=Sbar_m[Psi,g_obs(q(Phi)),theta_obs(q(Phi))], v in ker(Dq) => delta_v S_matter=0",
            "evidence_status": "DERIVED_CONDITIONALLY_IN_193_4265_4277",
            "what_is_signed": "standard branch chain-rule zero",
            "what_is_unsigned": "global parent branch selector and actual v_chi certificate",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SSA4467_1_no_Achi",
            "claim_piece": "no common conformal matter coupling",
            "formula": "A(chi)=constant => C_matter=d ln A/dchi=0",
            "evidence_status": "NOT_GLOBAL_PARENT_SIGNED",
            "what_is_signed": "4277 excludes g_X/b_dis only inside the standard branch",
            "what_is_unsigned": "global absence of A(chi) or hidden conformal/disformal channel",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SSA4467_2_no_theta_chi",
            "claim_piece": "no internal constant/common composition drift",
            "formula": "d ln theta_j/dchi=0 for alpha_EM, mass ratios, source normalization and material markers",
            "evidence_status": "BRANCH_LOCAL_ONLY",
            "what_is_signed": "source-label forgetting kills differential WEP in the private branch",
            "what_is_unsigned": "global constant-sector silence for every local-test arena",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SSA4467_3_no_Xi_open",
            "claim_piece": "no hidden source/readout tail",
            "formula": "Xi_src_hidden=0 only if all hidden weights, source normalization, hidden operators, EM weights, inner charge and environment selectors vanish",
            "evidence_status": "4332_BRANCH_ZERO_OPEN_TAIL_RETAINED",
            "what_is_signed": "Xi zero formula inside source-label-forgetting Hilbert-owner branch",
            "what_is_unsigned": "global no-hidden-slot/source-label-forgetting parent theorem",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SSA4467_4_source_silence_verdict",
            "claim_piece": "C_matter=0",
            "formula": "C_matter=0 follows only if SSA4467_0 through SSA4467_3 all sign together",
            "evidence_status": "CERTIFICATE_NOT_SIGNED",
            "what_is_signed": "conditional theorem scaffold",
            "what_is_unsigned": "actual parent action normal form with no A(chi), no theta_j(chi), no Xi_open",
            "valid_for_claim": False,
        },
    ]


def refinement_certificate_rows() -> List[Dict[str, object]]:
    return [
        {
            "refinement_id": "RC4467_0_linearity_math",
            "clause": "same physical flux subdivision is action-equivalent",
            "test": "S_n(delta)=n Phi(delta/n)=Phi(delta) for all n",
            "current_status": "EXACT_CONDITIONAL_THEOREM_FROM_4459",
            "if_signed": "Phi''(0)=0 in the same deficit channel",
            "blocking_gap": "the theorem premise is not itself a parent action signature",
            "valid_for_claim": False,
        },
        {
            "refinement_id": "RC4467_1_refinement_groupoid",
            "clause": "parent configurations are quotient/projective refinement equivalence classes",
            "test": "q_ref relates refinements before variation and preserves physical observables",
            "current_status": "QUOTIENT_ROUTE_IDENTIFIED_NOT_PARENT_DERIVED",
            "if_signed": "cell subdivision is gauge/readout-silent",
            "blocking_gap": "current corpus does not prove the parent refinement groupoid",
            "valid_for_claim": False,
        },
        {
            "refinement_id": "RC4467_2_cylindrical_action",
            "clause": "parent action is projectively consistent under refinement",
            "test": "S_T'[Phi']=S_T[q_ref(Phi')]",
            "current_status": "NOT_PARENT_SIGNED",
            "if_signed": "activates the 4459 linearity theorem",
            "blocking_gap": "refined/unrefined actions may differ by finite c2 response",
            "valid_for_claim": False,
        },
        {
            "refinement_id": "RC4467_3_geometry_owner",
            "clause": "same parent owns coframe, hinge, orientation, connection and signed deficit",
            "test": "B_h/A_h and Log(U_h) are parent-owned before EH/Regge import",
            "current_status": "FAILED_CURRENT_CORPUS_FROM_4460_4461",
            "if_signed": "refinement theorem would attach to the real local geometry variable",
            "blocking_gap": "cell-to-hinge complex, orientation, connection owner and branch domain remain unsigned",
            "valid_for_claim": False,
        },
        {
            "refinement_id": "RC4467_4_no_second_channel",
            "clause": "no density-squared, trace/norm, hidden scalar, marker prefactor or tower channel survives",
            "test": "all c_R2/c_Ric/c_W/c_Riem owners are zero/topological/vertical or finite-sourced",
            "current_status": "OPEN_COUNTERROUTES_RETAINED",
            "if_signed": "c_R2_eff=0 rather than only c2_visible=0 in one channel",
            "blocking_gap": "R2 density and trace/norm holonomy counterroutes remain legal",
            "valid_for_claim": False,
        },
        {
            "refinement_id": "RC4467_5_refinement_verdict",
            "clause": "c_R2_eff=0",
            "test": "RC4467_0 through RC4467_4 all sign together",
            "current_status": "CERTIFICATE_NOT_SIGNED",
            "if_signed": "no scalar pole; R10 finite alpha row inactive",
            "blocking_gap": "multiple parent signatures remain open simultaneously",
            "valid_for_claim": False,
        },
    ]


def rollup_rows() -> List[Dict[str, object]]:
    return [
        {
            "rollup_id": "RU4467_0_signed_math",
            "category": "derived/usable now",
            "items": "quotient chain-rule zero in the standard branch; g_X=b_dis zero conditionally; refinement linearity theorem; R10 pressure gate",
            "effect": "strong private scaffold for local-GR reduction",
            "claim_effect": "nonclaim only",
            "valid_for_claim": False,
        },
        {
            "rollup_id": "RU4467_1_unsigned_source_silence",
            "category": "source-silence blockers",
            "items": "actual v_chi, global no A(chi), global theta_j silence, no Xi_open, boundary/degree silence",
            "effect": "C_matter=0 cannot be promoted",
            "claim_effect": "finite common-mode branch retained",
            "valid_for_claim": False,
        },
        {
            "rollup_id": "RU4467_2_unsigned_refinement",
            "category": "c_R2 zero blockers",
            "items": "refinement groupoid, cylindrical parent action, parent-owned hinge/connection/coframe, no grain, no second channel",
            "effect": "c_R2_eff=0 cannot be promoted",
            "claim_effect": "scalaron/R10 branch retained",
            "valid_for_claim": False,
        },
        {
            "rollup_id": "RU4467_3_next_exact_target",
            "category": "next proof focus",
            "items": "parent action normal form with no A(chi) and no second curvature-square channel",
            "effect": "the next move should try to sign the two most valuable missing clauses rather than recircle all local tests",
            "claim_effect": "selects 4468",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4467_0_source_silence",
            "finding": "C_matter=0 is exactly derivable from quotient matter descent only if no A(chi), no theta_j(chi) and no Xi_open are parent-signed",
            "consequence": "current evidence gives a conditional standard-branch theorem, not a global parent certificate",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4467_1_refinement_zero",
            "finding": "c_R2_eff=0 is exactly derivable if refinement linearity is attached to a parent-owned hinge/connection/coframe and no second channel",
            "consequence": "current evidence proves the math but not the full parent signature",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4467_2_claim_ceiling",
            "finding": "neither zero certificate signs today",
            "consequence": "finite common-mode scalar remains bound-only under R10/PPN/orbital pressure",
            "next_action": "do not claim local GR from WEP closure or calibrated G",
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    parent_rows: List[Dict[str, object]],
    source_rows_audit: List[Dict[str, object]],
    refinement_rows: List[Dict[str, object]],
    rollup: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    source_ok = all(bool(row.get("local_path_exists")) and bool(row.get("needle_found")) for row in source_rows)
    parent_verdict = any(row.get("certificate_id") == "PAC4467_5_verdict" and row.get("signed_now") is False for row in parent_rows)
    source_verdict = any(row.get("audit_id") == "SSA4467_4_source_silence_verdict" and row.get("evidence_status") == "CERTIFICATE_NOT_SIGNED" for row in source_rows_audit)
    refinement_verdict = any(row.get("refinement_id") == "RC4467_5_refinement_verdict" and row.get("current_status") == "CERTIFICATE_NOT_SIGNED" for row in refinement_rows)
    next_focus = any(row.get("rollup_id") == "RU4467_3_next_exact_target" for row in rollup)
    no_claims = not any(
        str(row.get("valid_for_claim")).lower() == "true" or str(row.get("claim_allowed", "False")).lower() == "true"
        for row in parent_rows + source_rows_audit + refinement_rows + rollup
    )
    return [
        {
            "gate_id": "CG4467_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": source_ok,
            "claim_allowed": False,
            "detail": "source register validates quotient, source-silence, refinement and common-mode handoff",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4467_1_parent_certificate",
            "claim": "parent action zero certificate signs",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "source-silence and refinement zero certificates both retain unsigned parent clauses" if parent_verdict else "verdict row missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4467_2_source_silence",
            "claim": "C_matter=0 source silence is parent-signed",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "standard-branch chain-rule exists, but no global no-Achi/no-Xi-open certificate" if source_verdict else "source verdict row missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4467_3_refinement_cR2_zero",
            "claim": "c_R2_eff=0 refinement certificate is parent-signed",
            "gate_pass": False,
            "claim_allowed": False,
            "detail": "4459 math is exact, but 4460/4461 parent signatures remain open" if refinement_verdict else "refinement verdict row missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4467_4_next_focus",
            "claim": "next exact target is selected",
            "gate_pass": next_focus,
            "claim_allowed": False,
            "detail": "focus no-Achi/no-second-channel normal form rather than broad recircling",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4467_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to public/local-GR claim evidence",
            "gate_pass": no_claims,
            "claim_allowed": False,
            "detail": "4467 is a certificate audit, not a pass",
            "valid_for_claim": False,
        },
    ]
