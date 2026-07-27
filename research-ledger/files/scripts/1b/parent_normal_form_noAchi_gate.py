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


def parent_normal_form_rows() -> List[Dict[str, object]]:
    return [
        {
            "normal_form_id": "NF4468_0_private_selector_grammar",
            "target": "explicit matter-frame A(chi)",
            "candidate_grammar": "S_parent|loc = S_EH[g_obs;kappa_*] + S_matter[psi,g_obs(q),theta(q)] + S_MH[A,g_obs(q)] + S_binding[psi,A,g_obs(q)] + topological/boundary silent rest",
            "derivation": "inside this typed grammar, ordinary matter has no independent argument A(chi)^2 g_obs and no scalar-dependent theta_j(chi) slot before variation",
            "result": "C_explicit_Achi=0 in the private selector branch",
            "scope": "PRIVATE_PPC4161_SELECTOR_BRANCH_ONLY",
            "signed_in_private_selector": True,
            "global_parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "normal_form_id": "NF4468_1_vertical_chain_rule",
            "target": "delta_chi S_matter",
            "candidate_grammar": "S_matter=Sbar_m[Psi,g_obs(q(Phi)),theta_obs(q(Phi))]",
            "derivation": "for v_chi in ker(Dq) and L_vchi theta_obs=0, delta_vchi S_matter = DSbar_m[Dq[v_chi],L_vchi theta_obs] = 0",
            "result": "ordinary matter is source-silent along a genuinely vertical chi direction",
            "scope": "CONDITIONAL_ON_ACTUAL_VCHI_AND_THETA_SILENCE",
            "signed_in_private_selector": True,
            "global_parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "normal_form_id": "NF4468_2_total_scalar_coupling_split",
            "target": "do not confuse no-Achi with no scalaron",
            "candidate_grammar": "C_total = C_explicit_Achi + C_metric_pole + C_hidden_source",
            "derivation": "no-Achi kills only the explicit matter-frame term; a finite curvature-square scalar can still source the metric trace and carry universal f(R)-like coupling",
            "result": "C_total=0 requires no explicit A(chi), no hidden source tail, and no metric scalar pole or a separate decoupling theorem",
            "scope": "SPLIT_DERIVED_CURRENT_ZERO_NOT_GLOBAL",
            "signed_in_private_selector": True,
            "global_parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "normal_form_id": "NF4468_3_no_second_channel_audit",
            "target": "no curvature-square scalar pole",
            "candidate_grammar": "c_R2_eff=0, D0=0, D2=0, and no trace/norm holonomy, hidden scalar, physical grain, marker, loop/EFT or memory-tower channel",
            "derivation": "4459 kills same-channel visible c2 only under parent-signed refinement equivalence; 200/201 still retain curvature-square residuals as legal EFT coefficients",
            "result": "second curvature channel is not forbidden by the current parent grammar",
            "scope": "UNSIGNED_NO_SECOND_CHANNEL",
            "signed_in_private_selector": False,
            "global_parent_signed": False,
            "valid_for_claim": False,
        },
        {
            "normal_form_id": "NF4468_4_combined_local_GR_gate",
            "target": "local-GR scalar closure",
            "candidate_grammar": "no A(chi) + vertical theta silence + no hidden source tail + no curvature-square metric pole",
            "derivation": "only the product of the source-silence and no-second-channel clauses removes both explicit and metric scalar couplings",
            "result": "private no-Achi progress is real, but local-GR scalar closure remains unsigned because c_R2_eff/no-second-channel is open",
            "scope": "NONCLAIM_FINITE_BRANCH_RETAINED",
            "signed_in_private_selector": False,
            "global_parent_signed": False,
            "valid_for_claim": False,
        },
    ]


def no_Achi_proof_rows() -> List[Dict[str, object]]:
    return [
        {
            "proof_id": "NA4468_0_object_language",
            "premise": "ordinary matter functor has only observed quotient-owned geometry arguments",
            "formula": "S_matter[psi,g_obs(q),theta(q)]",
            "proof_move": "an independent conformal factor A(chi) would be an extra parent argument not present in the selector grammar",
            "status": "PRIVATE_SELECTOR_PROOF",
            "remaining_gap": "global MTS parent adoption of the selector is not proved",
            "valid_for_claim": False,
        },
        {
            "proof_id": "NA4468_1_variation",
            "premise": "v_chi is truly vertical and constants/material labels are q-basic",
            "formula": "delta_vchi S_matter = (delta S/delta g_obs)Dq[v_chi] + (delta S/delta theta)L_vchi theta = 0",
            "proof_move": "chain-rule descent kills direct matter source charge",
            "status": "CONDITIONAL_THEOREM",
            "remaining_gap": "actual v_chi and global theta/source-label silence remain parent-unsigned",
            "valid_for_claim": False,
        },
        {
            "proof_id": "NA4468_2_hidden_tail_guard",
            "premise": "no source weights, source normalization, hidden matter operators, hidden Hodge/current weights or environment selectors",
            "formula": "Xi_open=0",
            "proof_move": "if the hidden-slot theorem signs, source tails cannot reintroduce A(chi)-like dependence",
            "status": "NOT_GLOBAL_PARENT_SIGNED",
            "remaining_gap": "4332 retains Xi_open outside the branch",
            "valid_for_claim": False,
        },
        {
            "proof_id": "NA4468_3_coupling_split",
            "premise": "explicit matter-frame coupling and metric-pole coupling are distinct",
            "formula": "alpha_eff = C_total^2/3, with C_total not determined by no-Achi alone if c_R2_eff is finite",
            "proof_move": "prevents a false local-GR pass from the private no-Achi theorem",
            "status": "DERIVED_GUARD",
            "remaining_gap": "need no-pole/no-second-channel or source-backed finite C_total",
            "valid_for_claim": False,
        },
    ]


def no_second_channel_rows() -> List[Dict[str, object]]:
    return [
        {
            "channel_id": "SC4468_0_same_channel_refinement",
            "channel": "same signed-deficit quadratic c2_visible",
            "zero_route": "S_n(delta)=n Phi(delta/n)=Phi(delta) for all n forces Phi''(0)=0",
            "current_status": "EXACT_CONDITIONAL_FROM_4459",
            "why_not_closed": "parent refinement equivalence, cylindrical action and owner clauses remain unsigned",
            "finite_fallback": "retain c2_visible and map to c_R2_eff if refinement signature fails",
            "valid_for_claim": False,
        },
        {
            "channel_id": "SC4468_1_metric_curvature_square_basis",
            "channel": "R^2/Ricci^2/Weyl^2/Riemann^2 EFT basis",
            "zero_route": "all quadratic coefficients topological, boundary-routed, heavy/screened or parent-zero",
            "current_status": "OPEN_FROM_200_201_4461",
            "why_not_closed": "Palatini/IR selector classifies curvature squares as residual coefficients rather than forbidding them",
            "finite_fallback": "D0/D2 basis guard and Yukawa/PPN/R10 map",
            "valid_for_claim": False,
        },
        {
            "channel_id": "SC4468_2_trace_norm_holonomy",
            "channel": "trace/norm/even holonomy cost",
            "zero_route": "parent proves only oriented signed linear deficit is physical and norm/trace costs are gauge/readout artifacts",
            "current_status": "LIVE_COUNTERCHANNEL",
            "why_not_closed": "4461 explicitly leaves trace/norm holonomy costs legal if parent owns them",
            "finite_fallback": "finite scalaron/spin residual pack",
            "valid_for_claim": False,
        },
        {
            "channel_id": "SC4468_3_hidden_scalar_marker_tower",
            "channel": "hidden scalar, marker prefactor, physical grain or memory tower",
            "zero_route": "typed parent action has no such field/marker/tower before variation",
            "current_status": "LIVE_COUNTERCHANNEL",
            "why_not_closed": "no global field-inventory theorem forbids every auxiliary or coarse-grained second channel",
            "finite_fallback": "source-backed coefficient and projection rows",
            "valid_for_claim": False,
        },
        {
            "channel_id": "SC4468_4_verdict",
            "channel": "no-second-channel certificate",
            "zero_route": "SC4468_0 through SC4468_3 all close together",
            "current_status": "NOT_SIGNED",
            "why_not_closed": "only same-channel linearity theorem is exact; the full basis/channel exclusion is not parent-owned",
            "finite_fallback": "finite c_R2/C_total score pack remains mandatory",
            "valid_for_claim": False,
        },
    ]


def finite_scalar_pack_rows() -> List[Dict[str, object]]:
    return [
        {
            "pack_id": "FSP4468_0_required_scalar_pack",
            "quantity": "c_R2_eff",
            "formula": "c_R2_eff = xi_shape*c2_visible*ell_cell^2/N_EH or D0/12 in pure R2 normalization",
            "current_value": "MISSING_PARENT_COEFFICIENT",
            "role": "sets lambda_R2 and decides whether a finite scalar pole exists",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "pack_id": "FSP4468_1_required_coupling_pack",
            "quantity": "C_total",
            "formula": "C_total = C_explicit_Achi + C_metric_pole + C_hidden_source",
            "current_value": "C_explicit_Achi=0 only inside private selector; C_metric_pole/C_hidden_source not globally zero",
            "role": "sets alpha_eff=C_total^2/3",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "pack_id": "FSP4468_2_current_universal_pressure",
            "quantity": "R10 pressure at lambda_R2",
            "formula": "alpha_eff=1/3 for universal metric scalar; alpha_bound=0.136485683105; ratio=2.44225859996",
            "current_value": "universal branch fails review-candidate pressure at lambda_R2=7.63929980956e-05 m",
            "role": "shows finite scalar is not safe by default",
            "claim_status": "NONCLAIM_PRESSURE",
            "valid_for_claim": False,
        },
        {
            "pack_id": "FSP4468_3_live_curve_requirement",
            "quantity": "alpha_bound(lambda)",
            "formula": "abs(alpha_eff)<=alpha_bound(lambda_R2)",
            "current_value": "live claim curve still placeholder; review-candidate rows are nonclaim",
            "role": "needed before any R10 pass/fail claim",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
        },
        {
            "pack_id": "FSP4468_4_ppn_requirement",
            "quantity": "gamma(r)-1",
            "formula": "gamma(r)-1=-2*alpha_eff*exp(-r/lambda_R2)/(1+alpha_eff*exp(-r/lambda_R2))",
            "current_value": "projection/lightcone branch not source-complete",
            "role": "finite scalar must also pass PPN/orbital/clock gates if range is relevant",
            "claim_status": "BLOCKED",
            "valid_for_claim": False,
        },
    ]


def decision_rows(next_target: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4468_0_no_Achi_progress",
            "finding": "the private PPC4161 selector grammar does make an explicit independent matter-frame A(chi) untypeable",
            "consequence": "this kills C_explicit_Achi inside the adopted local selector branch only",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4468_1_scalaron_guard",
            "finding": "no-Achi does not by itself kill a metric curvature-square scalaron",
            "consequence": "C_total can remain nonzero through C_metric_pole unless c_R2_eff=0 or a separate decoupling theorem signs",
            "next_action": next_target,
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC4468_2_no_second_channel_result",
            "finding": "the second curvature channel is still legal in the current parent grammar",
            "consequence": "finite scalar pack remains mandatory unless the no-second-channel theorem is derived",
            "next_action": next_target,
            "valid_for_claim": False,
        },
    ]


def claim_gate_rows(
    source_rows: List[Dict[str, object]],
    normal_rows: List[Dict[str, object]],
    no_Achi_rows: List[Dict[str, object]],
    second_rows: List[Dict[str, object]],
    finite_rows: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    sources_ok = all(row.get("local_path_exists") is True and row.get("needle_found") is True for row in source_rows)
    private_no_Achi = any(
        row.get("normal_form_id") == "NF4468_0_private_selector_grammar"
        and row.get("signed_in_private_selector") is True
        for row in normal_rows
    )
    second_closed = any(
        row.get("channel_id") == "SC4468_4_verdict"
        and "SIGNED" == str(row.get("current_status"))
        for row in second_rows
    )
    finite_ready = all("MISSING" not in str(row.get("current_value")) and "BLOCKED" not in str(row.get("claim_status")) for row in finite_rows)
    no_claims = all(
        str(row.get("valid_for_claim")).lower() == "false"
        for group in [source_rows, normal_rows, no_Achi_rows, second_rows, finite_rows]
        for row in group
    )
    return [
        {
            "gate_id": "CG4468_0_sources",
            "claim": "all cited local sources exist and needles are found",
            "gate_pass": sources_ok,
            "claim_allowed": False,
            "detail": "source trail covers selector grammar, matter descent, second-channel map and R10 pressure",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4468_1_private_no_Achi",
            "claim": "explicit A(chi) matter-frame factor is forbidden in the private selector",
            "gate_pass": private_no_Achi,
            "claim_allowed": False,
            "detail": "real branch-local progress, but not global parent adoption",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4468_2_no_second_channel",
            "claim": "all curvature-square/second scalar channels are parent-forbidden",
            "gate_pass": second_closed,
            "claim_allowed": False,
            "detail": "second channel remains legal; same-channel linearity alone is insufficient",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4468_3_local_GR_scalar_closure",
            "claim": "local-GR scalar/common-mode closure follows",
            "gate_pass": private_no_Achi and second_closed,
            "claim_allowed": False,
            "detail": "no-Achi without no-pole still leaves metric scalaron branch",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4468_4_finite_scalar_pack_ready",
            "claim": "finite scalar branch can be scored as evidence",
            "gate_pass": finite_ready,
            "claim_allowed": False,
            "detail": "parent c_R2_eff/C_total and live bound curve are still missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "CG4468_5_no_generated_claim_rows",
            "claim": "no generated row is promoted to public/local-GR evidence",
            "gate_pass": no_claims,
            "claim_allowed": False,
            "detail": "4468 is a derivation split and finite-pack staging checkpoint",
            "valid_for_claim": False,
        },
    ]
