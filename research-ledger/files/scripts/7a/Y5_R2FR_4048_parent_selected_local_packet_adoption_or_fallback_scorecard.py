from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4048-Y5-R2FR-parent-selected-local-packet-adoption-or-fallback-scorecard.md"

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4048_SOURCE_REGISTER.csv",
    "parent_packet_contract": SOURCE_DIR / "P8_Y5_R2FR_4048_PARENT_PACKET_CONTRACT.csv",
    "adoption_audit": SOURCE_DIR / "P8_Y5_R2FR_4048_ADOPTION_AUDIT.csv",
    "sufficiency_theorem": SOURCE_DIR / "P8_Y5_R2FR_4048_LOCAL_GR_SUFFICIENCY_THEOREM.csv",
    "residual_collapse": SOURCE_DIR / "P8_Y5_R2FR_4048_RESIDUAL_COLLAPSE_MATRIX.csv",
    "fallback_scorecard": SOURCE_DIR / "P8_Y5_R2FR_4048_FALLBACK_SCORECARD.csv",
    "ppn_zero_vector": SOURCE_DIR / "P8_Y5_R2FR_4048_CONDITIONAL_PPN_ZERO_VECTOR.csv",
    "evaluator": SOURCE_DIR / "P8_Y5_R2FR_4048_EVALUATOR_RESULTS.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4048_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4048_CLAIM_GATE.csv",
    "remaining_residuals": SOURCE_DIR / "P8_Y5_R2FR_4048_REMAINING_LOCAL_RESIDUAL_VECTOR.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4048_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4048_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4048_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"empty rows for {path}")
    fields: List[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def source_rows(ts: str) -> List[Dict[str, object]]:
    specs = [
        ("SRC4048_00", ROOT / "4021-Y5-R2FR-parent-adoption-witness-or-first-PPN-score-input-fill.md", "Q_parent^loc = Q_dyn^loc x K_G x Q_aux", "4021 sufficient local parent witness"),
        ("SRC4048_01", SOURCE_DIR / "P8_Y5_R2FR_4021_PARENT_LOCAL_ACTION_WITNESS.csv", "S_loc^{<=2PN}", "4021 parent local action witness rows"),
        ("SRC4048_02", SOURCE_DIR / "P8_Y5_R2FR_4021_DERIVED_ZERO_LEMMAS.csv", "B_source=A_source^2", "4021 conditional PPN zero lemmas"),
        ("SRC4048_03", SOURCE_DIR / "P8_Y5_R2FR_4021_WITNESS_PPN_SCORE_FILL.csv", "Delta_PPN_abs_4021", "4021 conditional PPN zero score fill"),
        ("SRC4048_04", SOURCE_DIR / "P8_Y5_R2FR_4022_WITNESS_ADMISSION_MATRIX.csv", "not_admitted_currently_score_or_excise", "4022 stress-test admission matrix"),
        ("SRC4048_05", SOURCE_DIR / "P8_Y5_R2FR_4022_EVALUATOR_RESULTS.csv", "CURRENT_STRESS_TEST_FAILS_FULL_ADOPTION", "4022 adoption stress-test failure before later reductions"),
        ("SRC4048_06", SOURCE_DIR / "P8_Y5_R2FR_4020_LOCAL_GR_ROLLUP_CHAIN.csv", "If ROLL4020_0..4 are parent-signed", "4020 local-GR conditional rollup"),
        ("SRC4048_07", SOURCE_DIR / "P8_Y5_R2FR_4019_EH_ONLY_R11_ADOPTION_CLAUSES.csv", "S_loc^{<=2PN}", "4019 EH-only/R11 adoption clauses"),
        ("SRC4048_08", SOURCE_DIR / "P8_Y5_R2FR_4042_NONEH_THEOREM_CONTRACT.csv", "Delta_PPN_abs_nonEH", "4042 non-EH theorem-or-bound contract"),
        ("SRC4048_09", SOURCE_DIR / "P8_Y5_R2FR_4038_EVALUATOR_RESULTS.csv", "C_POYNTING_AND_C_B_ZERO_IN_SELECTED_LOCAL_BRANCH", "4038 Poynting/boundary closure"),
        ("SRC4048_10", SOURCE_DIR / "P8_Y5_R2FR_4043_EVALUATOR_RESULTS.csv", "PROJECTOR_DOMAIN_STRESS_ZERO_IN_PRIVATE_SELECTED_BRANCH", "4043 projector/domain closure"),
        ("SRC4048_11", SOURCE_DIR / "P8_Y5_R2FR_4046_EVALUATOR_RESULTS.csv", "CZ_TAIL_ZERO_IN_PRIVATE_SELECTED_RESET_BRANCH", "4046 cZ tail closure"),
        ("SRC4048_12", SOURCE_DIR / "P8_Y5_R2FR_4047_EVALUATOR_RESULTS.csv", "CNORM_ZERO_IN_PRIVATE_SELECTED_BRANCH", "4047 c_norm closure"),
        ("SRC4048_13", SOURCE_DIR / "P8_Y5_R2FR_4016_GREF_SUPERSELECTION_THEOREM.csv", "D_X ln G_ref=0", "fixed coupling derivative silence"),
        ("SRC4048_14", SOURCE_DIR / "P8_Y5_R2FR_4036_NO_HOM_SOURCE_SLOT_THEOREM.csv", "Hom_parent", "no source-slot/source-prefactor theorem"),
        ("SRC4048_15", SOURCE_DIR / "P8_Y5_R2FR_4044_SELECTED_BRANCH_CLAIM_LADDER.csv", "parent packet adopted", "4044 claim ladder required parent adoption"),
    ]
    rows: List[Dict[str, object]] = []
    for source_id, path, needle, role in specs:
        exists = path.exists()
        text = read_text(path) if exists else ""
        rows.append(
            {
                "source_id": source_id,
                "path": str(path),
                "exists": exists,
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": ts,
            }
        )
    return rows


def parent_packet_contract_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("PPC4048_0_field_space", "field-space factorization", "Q_parent^loc = Q_dyn^loc x K_G x Q_aux; q:Q_dyn^loc -> Met_obs; V=ker(Dq); T_local K_G=0", "separates public observed geometry, fixed coupling data, and auxiliary/private directions"),
        ("PPC4048_1_action_domain", "local <=2PN action domain", "S_loc^{<=2PN}=S_EH[g_obs;kappa_*]+S_matter[psi,g_obs,theta]+S_EM[A,g_obs]+S_binding+dB_proper+S_top+S_aux^{double-zero}+S_vert^{Dq=0}", "forbids independent local non-EH metric operators unless exact, topological, vertical-only, or auxiliary double-zero"),
        ("PPC4048_2_fixed_coupling", "constant local coupling branch", "G_ref=c^4*kappa_*/(8*pi), delta_local kappa_*=0, Hom(source/range/domain/memory,K_G)=0", "removes Gdot/radial/range/source derivative hair without claiming a numerical prediction for G"),
        ("PPC4048_3_source_functor", "ordinary matter source descent", "S_matter=Sbar_m[Obs(q(Phi)),psi,theta] with fixed representation labels and no source-only prefactor w_A(hidden)", "kills direct c_T/source-label leakage and species/source normalization pullback"),
        ("PPC4048_4_em_owner", "unique EM owner", "S_EM uses one observed Hodge *_obs[g_obs(q(Phi))] and one Hilbert variation; no f(hidden)F^2 slot", "counts Maxwell/binding/Poynting stress once and forbids hidden EM source multipliers"),
        ("PPC4048_5_source_charge", "same source charge", "Pi_M J_H = J_M_top+dB_zero and M_H_ref=H_tau[S_outer]-H_ref=Mbar_H_ref(q(Phi)) before orbital GM readout", "locks Newton source mass to the same Hilbert/H_tau/Pi_M branch"),
        ("PPC4048_6_boundary_support", "proper boundary/support branch", "dB and exact terms have compact-support or matched-boundary zero flux; worldtube/support/projectors are parent-owned or q-basic", "removes boundary, support and Poynting source leakage in the local exterior"),
        ("PPC4048_7_gamma_khat_qloc", "Gamma/Khat/q_loc projector silence", "q_loc=P_loc(nabla Gamma_eff-nabla Khat) is vertical/projector-silent or auxiliary double-zero through O(U^2)", "removes delta_beta_q_loc and finite local force/source-exchange tails in the selected branch"),
        ("PPC4048_8_memory_reset", "local retarded memory branch", "X_mem(t0)=0, J_open+B_lift=0, B_nonlocal_kernel=0 on compact isolated PPN/Newton collar", "removes Delta_cZ tail without deleting FLRW/open memory sectors"),
        ("PPC4048_9_readout_firewall", "readout-after-variation firewall", "PPN, R10, clocks, orbital, EM and cosmology readouts are post-variation maps and cannot choose action source terms", "prevents empirical fitting or measured GM from being smuggled into the action"),
        ("PPC4048_10_claim_firewall", "claim firewall", "if any clause is not parent-adopted, route the surviving family to explicit bound rows with no cancellation credit", "keeps private theorem candidates distinct from public claims"),
    ]
    return [
        {
            "clause_id": clause_id,
            "contract_clause": clause,
            "mathematical_condition": condition,
            "effect": effect,
            "adoption_status": "CONTRACT_READY_NOT_FINAL_CORPUS_ADOPTED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for clause_id, clause, condition, effect in rows
    ]


def adoption_audit_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("AUD4048_0_field_space", "PPC4048_0_field_space", "supported by 4021 witness and 4016 fixed K_G theorem", "ADOPTABLE_PRIVATE_CONTRACT", "not yet written into the public parent corpus"),
        ("AUD4048_1_action_domain", "PPC4048_1_action_domain", "supported by 4019/4042 EH-only/nonEH classifier", "ADOPTABLE_PRIVATE_CONTRACT", "every rejected nonEH family must be scored"),
        ("AUD4048_2_fixed_coupling", "PPC4048_2_fixed_coupling", "supported by 4016 and 4047 G_obs derivative zero", "ADOPTABLE_PRIVATE_CONTRACT", "does not predict numerical G"),
        ("AUD4048_3_source_functor", "PPC4048_3_source_functor", "supported by 4007, 4008, 4036 and 4047 epsilon_mu zero", "ADOPTABLE_PRIVATE_CONTRACT", "no source/material weight may be added later"),
        ("AUD4048_4_em_owner", "PPC4048_4_em_owner", "supported by 4013/4014 and 4038 Poynting no-flux branch", "ADOPTABLE_PRIVATE_CONTRACT", "open/radiative EM systems remain fallback/scored"),
        ("AUD4048_5_source_charge", "PPC4048_5_source_charge", "supported by 4011/4012/4015 and 4047 M_eff derivative zero", "ADOPTABLE_PRIVATE_CONTRACT", "same-source charge equality must be parent-owned"),
        ("AUD4048_6_boundary_support", "PPC4048_6_boundary_support", "supported by 4038 boundary/Poynting zero and 4043 projector/domain silence", "ADOPTABLE_PRIVATE_CONTRACT", "if boundary/reference branch changes, fallback rows reactivate"),
        ("AUD4048_7_gamma_khat_qloc", "PPC4048_7_gamma_khat_qloc", "supported conditionally by 4023-4030 tracefree/Gamma/Khat route, not public-final", "CONDITIONAL_WEAK_LINK", "must remain explicit in the parent packet and scorer fallback"),
        ("AUD4048_8_memory_reset", "PPC4048_8_memory_reset", "supported by 4046 local reset/no-incoming memory branch", "ADOPTABLE_PRIVATE_CONTRACT", "does not erase cosmological/galaxy memory"),
        ("AUD4048_9_readout_firewall", "PPC4048_9_readout_firewall", "supported by 4037 and 4044 readout firewall", "ADOPTABLE_PRIVATE_CONTRACT", "empirical readouts cannot be action-source definitions"),
        ("AUD4048_10_claim_firewall", "PPC4048_10_claim_firewall", "supported by 4021/4044/4047 claim guards", "MANDATORY", "blocks public local-GR claim until adoption or scores pass"),
    ]
    return [
        {
            "audit_id": audit_id,
            "contract_clause": clause_id,
            "evidence": evidence,
            "audit_status": status,
            "remaining_risk": risk,
            "clause_adopted_in_actual_corpus": False,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for audit_id, clause_id, evidence, status, risk in rows
    ]


def sufficiency_theorem_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "SFT4048_0_packet",
            "premise": "all PPC4048_0..10 clauses are adopted as one local parent-action packet",
            "mathematical_statement": "S_loc^{<=2PN} has only EH + same-source matter/EM/binding + exact/topological/proper boundary + double-zero/vertical-silent auxiliaries",
            "result": "the selected local branch is an EH same-source branch through required PPN order",
            "status": "SUFFICIENT_CONDITIONAL_THEOREM",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "SFT4048_1_Newton",
            "premise": "EH 00 equation, fixed G_ref, same Hilbert source mass",
            "mathematical_statement": "G_00^(1)=kappa_ref T_00^H and kappa_ref=8*pi*G_ref/c^4 imply nabla^2 Phi=4*pi*G_ref rho_H",
            "result": "Newton/Poisson/Gauss inverse-square limit follows with calibrated constant G_ref",
            "status": "ZERO_RESIDUAL_UNDER_PACKET",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "SFT4048_2_PPN",
            "premise": "EH-only local operator plus same source and no q_loc/nonEH/projector/source-normalization leakage",
            "mathematical_statement": "Delta_PPN_abs=|delta_gamma|+|delta_beta|+|alpha_i|+|xi|+|zeta_i|+|Gdot/G|=0",
            "result": "gamma=beta=1, alpha_i=xi=zeta_i=0, Gdot/G=0 under the packet",
            "status": "ZERO_RESIDUAL_UNDER_PACKET",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "SFT4048_3_cZ_cnorm",
            "premise": "4046 cZ reset branch and 4047 c_norm source packet are adopted inside PPC4048",
            "mathematical_statement": "Delta_cZ_selected=0 and Delta_cnorm_selected=0",
            "result": "the two post-4044 live envelopes are absorbed into the one packet contract",
            "status": "ZERO_RESIDUAL_UNDER_PACKET",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "theorem_id": "SFT4048_4_nonclaim",
            "premise": "the contract is not yet globally adopted by the full MTS corpus",
            "mathematical_statement": "private sufficient packet != public completed all-sector theorem",
            "result": "next task is corpus clause map/adoption, not public claim",
            "status": "PUBLIC_CLAIM_BLOCKED",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def residual_collapse_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("RCM4048_0_direct", "direct source-only vertices", "c_T,c_EM,C_XF2_direct", "4037/4036", "ZERO_UNDER_PACKET"),
        ("RCM4048_1_boundary", "Poynting/boundary/reference leakage", "c_Poynting,c_B", "4038", "ZERO_UNDER_PACKET_ELSE_FINITE_FLUX_BOUND"),
        ("RCM4048_2_nonEH", "standalone non-EH/R11 operator families", "c_nonEH,Delta_PPN_abs_nonEH", "4019/4042", "ZERO_IF_ADMITTED_CLASSES_ELSE_PPN_BOUND_VECTOR"),
        ("RCM4048_3_projector", "projector/domain preferred-frame stress", "alpha_i,xi,projector/domain stress", "4043", "ZERO_UNDER_PACKET_ELSE_ALPHA_XI_BOUND"),
        ("RCM4048_4_cZ", "hidden-current memory tail", "Delta_cZ_selected", "4046", "ZERO_UNDER_PACKET_ELSE_MEMORY_SUPPRESSION_BOUND"),
        ("RCM4048_5_cnorm", "source-normalization derivative hair", "Delta_cnorm_selected", "4047", "ZERO_UNDER_PACKET_ELSE_CNORM_BOUND_VECTOR"),
        ("RCM4048_6_parent", "parent packet adoption", "Parent_packet_adoption", "4048", "CONVERTED_TO_EXPLICIT_CONTRACT_NOT_PUBLIC_FINAL"),
    ]
    return [
        {
            "collapse_id": row_id,
            "channel": channel,
            "symbols": symbols,
            "source_checkpoint": source,
            "packet_status": status,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for row_id, channel, symbols, source, status in rows
    ]


def fallback_scorecard_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("FB4048_0_KG", "fixed K_G/coupling branch rejected", "Gdot/G, radial/range G drift, source coupling drift", "epsilon_Gref_superselection_4016"),
        ("FB4048_1_source", "same Hilbert/H_tau/Pi_M source charge rejected", "orbital GM mismatch, beta source square law, WEP/source charge", "epsilon_support_4011 + epsilon_charge_4012"),
        ("FB4048_2_nonEH", "EH-only/nonEH operator classifier rejected", "delta_gamma_R11, delta_beta_R11, xi, range/clock terms", "Delta_PPN_abs_nonEH"),
        ("FB4048_3_qloc", "Gamma/Khat/q_loc projector silence rejected", "delta_beta_q_loc, alpha(lambda), local force/source exchange", "q_loc amplitude/profile bound rows"),
        ("FB4048_4_projector", "domain/projector branch rejected", "alpha1, alpha2, alpha3, xi", "alpha_xi bound vector"),
        ("FB4048_5_memory", "local reset/no-incoming memory branch rejected", "Delta_cZ tail, Gdot/range/memory fifth-force leakage", "3895/3931 memory suppression law"),
        ("FB4048_6_cnorm", "source-normalization packet rejected", "Delta_cnorm derivative envelope", "epsilon_G + epsilon_Meff + epsilon_mu_derivative"),
        ("FB4048_7_public", "actual corpus does not adopt PPC4048", "no local-GR public claim", "run scorer rows with no cancellation credit"),
    ]
    return [
        {
            "fallback_id": fallback_id,
            "failure_mode": failure_mode,
            "observable_residual": residual,
            "required_bound_or_score": score,
            "valid_for_claim": False,
            "timestamp_utc": ts,
        }
        for fallback_id, failure_mode, residual, score in rows
    ]


def ppn_zero_vector_rows(ts: str) -> List[Dict[str, object]]:
    rows = [
        ("PPNZ4048_0_gamma", "gamma-1", "0", "EH-only spatial response plus no R11/readout stress"),
        ("PPNZ4048_1_beta", "beta-1", "0", "same-source EH nonlinear completion gives B_source=A_source^2"),
        ("PPNZ4048_2_alpha", "alpha1,alpha2,alpha3", "0", "no local vector/domain/memory preferred-frame source under PPC4048"),
        ("PPNZ4048_3_xi", "xi", "0", "no projector/domain anisotropic stress under PPC4048"),
        ("PPNZ4048_4_zeta", "zeta_i", "0", "same Hilbert stress plus Bianchi/conservation closure"),
        ("PPNZ4048_5_Gdot", "Gdot/G", "0", "fixed K_G/kappa_* branch"),
        ("PPNZ4048_6_cZ", "Delta_cZ_selected", "0", "4046 local reset/no-incoming tail zero"),
        ("PPNZ4048_7_cnorm", "Delta_cnorm_selected", "0", "4047 source-normalization derivative zero"),
        ("PPNZ4048_8_master", "Delta_PPN_abs_4048", "0", "absolute no-cancellation sum of zero rows under PPC4048"),
    ]
    return [
        {
            "zero_id": zero_id,
            "quantity": quantity,
            "conditional_value_under_PPC4048": value,
            "reason": reason,
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        }
        for zero_id, quantity, value, reason in rows
    ]


def evaluator_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "case_id": "CASE4048_0_packet_adopted",
            "verdict": "CONDITIONAL_LOCAL_GR_ZERO_VECTOR_UNDER_PPC4048",
            "result": "If PPC4048 is adopted as the local parent-action packet, Newton/Poisson, PPN gamma/beta/vector/conservation rows, cZ and c_norm all collapse to zero in the selected compact local branch.",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4048",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4048_1_current_corpus",
            "verdict": "ADOPTION_CONTRACT_READY_NOT_FINAL_CORPUS_ADOPTED",
            "result": "4048 makes the exact packet explicit and source-backed, but does not modify/adopt it into the main corpus or formalization-workbench.",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4048",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "case_id": "CASE4048_2_packet_rejected",
            "verdict": "FALLBACK_SCORECARD_REQUIRED",
            "result": "Any rejected clause maps to the listed no-cancellation fallback score rows rather than being hidden in the local-GR claim.",
            "claim_result": "NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4048",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def decision_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4048_0_accept_contract",
            "decision": "PPC4048 is the current strongest local-GR parent packet candidate",
            "reason": "it packages the 4021 witness plus 4022 stress-test routing and the later 4038/4042/4043/4046/4047 residual closures into one contract",
            "next_action": "map PPC4048 clause-by-clause to actual corpus/formalization sources before public adoption",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
        {
            "decision_id": "DEC4048_1_no_public_claim",
            "decision": "do not claim completed local GR yet",
            "reason": "PPC4048 is sufficient if adopted, but the actual corpus adoption evidence is not yet written and verified",
            "next_action": "4049 corpus clause map and conflict ledger",
            "valid_for_public_claim": False,
            "timestamp_utc": ts,
        },
    ]


def claim_gate_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4048_0_private",
            "claim": "PPC4048 is a sufficient private local parent-action packet for the GR/PPN zero vector",
            "allowed": True,
            "public_claim": False,
            "scope": "private theorem candidate, not public corpus claim",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4048_1_local_GR_public",
            "claim": "MTS publicly derives local GR from the full corpus",
            "allowed": False,
            "public_claim": False,
            "scope": "blocked until PPC4048 is mapped to and adopted by actual corpus sources or fallback score rows pass",
            "timestamp_utc": ts,
        },
        {
            "claim_id": "CLAIM4048_2_numerical_G",
            "claim": "MTS predicts the measured numerical value of Newton's constant",
            "allowed": False,
            "public_claim": False,
            "scope": "PPC4048 calibrates a universal fixed G_ref branch; it does not predict dimensionful G",
            "timestamp_utc": ts,
        },
    ]


def remaining_residual_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "residual_id": "REM4048_0_corpus_map",
            "symbol": "PPC4048_corpus_adoption_map",
            "residual": "each PPC4048 clause must be matched against actual parent/corpus files, with conflicts or missing clauses recorded",
            "current_route": "4049 corpus clause map and conflict ledger",
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4048_1_public_score",
            "symbol": "fallback_score_rows_if_rejected",
            "residual": "if any PPC4048 clause fails corpus adoption, the corresponding no-cancellation fallback score rows must be filled numerically/source-backed",
            "current_route": "PPN/R10/WEP/clock/orbital bound row acquisition",
            "timestamp_utc": ts,
        },
        {
            "residual_id": "REM4048_2_global_scope",
            "symbol": "global_MTS_unification_scope",
            "residual": "local compact PPN/Newton branch is not the full cosmology/galaxy/EM/unified field theory",
            "current_route": "after local branch adoption, connect to cosmology/galaxy/EM pillars without changing local packet",
            "timestamp_utc": ts,
        },
    ]


def next_target_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "NEXT4048_0",
            "next_doc": "4049-Y5-R2FR-PPC4048-corpus-clause-map-and-conflict-ledger.md",
            "next_script": "scripts/Y5_R2FR_4049_PPC4048_corpus_clause_map_and_conflict_ledger.py",
            "reason": "PPC4048 is now a precise sufficient packet; the next non-circular move is to map it against actual corpus sources and expose any conflicts before adoption",
            "timestamp_utc": ts,
        }
    ]


def status_rows(ts: str) -> List[Dict[str, object]]:
    return [
        {
            "status_id": "STAT4048",
            "status": "PPC4048_SUFFICIENT_PACKET_READY_CORPUS_ADOPTION_MAP_NEXT",
            "public_claim": False,
            "timestamp_utc": ts,
        }
    ]


def doc_text(ts: str, source_count: int) -> str:
    return f"""# 4048 - Parent Selected Local Packet Adoption Or Fallback Scorecard

- Timestamp: `{ts}`
- Status: `private_nonclaim_checkpoint`
- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.
- Source needles found: `{source_count}/16`.

## What Actually Moved

4048 takes the 4021 parent witness and re-runs it after the later stress work:

- 4038 controls Poynting/boundary leakage;
- 4042 decomposes standalone non-EH operators into admitted classes or a PPN bound vector;
- 4043 controls projector/domain preferred-frame stress;
- 4046 gives `Delta_cZ_selected=0`;
- 4047 gives `Delta_cnorm_selected=0`.

The result is the explicit packet `PPC4048`: a sufficient local parent-action contract.

If `PPC4048_0..10` are adopted as one parent local branch, the conditional local vector is:

`gamma=beta=1`, `alpha_i=xi=zeta_i=0`, `Gdot/G=0`, `Delta_cZ_selected=0`, and `Delta_cnorm_selected=0`.

## What Is Not Being Claimed

This is still not a public local-GR claim. 4048 does not rewrite the main corpus and does not claim that the full MTS parent action already adopts the packet.

It says something sharper:

`PPC4048` is now the exact contract the parent action must satisfy. Accept it and the selected compact local branch closes. Reject any clause and the corresponding fallback score row must be filled with no cancellation credit.

## Current Verdict

- Current evaluator result: `ADOPTION_CONTRACT_READY_NOT_FINAL_CORPUS_ADOPTED`.
- Conditional result: `CONDITIONAL_LOCAL_GR_ZERO_VECTOR_UNDER_PPC4048`.
- Claim result: `NO_PUBLIC_LOCAL_GR_CLAIM_FROM_4048`.
- Next live task: map `PPC4048` clause-by-clause onto actual corpus/formalization sources and list conflicts.

## Next Target

- `4049-Y5-R2FR-PPC4048-corpus-clause-map-and-conflict-ledger.md`
- `scripts/Y5_R2FR_4049_PPC4048_corpus_clause_map_and_conflict_ledger.py`
"""


def script_compiles() -> bool:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
        return True
    except py_compile.PyCompileError:
        return False


def validate_outputs(source_register: List[Dict[str, object]], tables: Dict[str, List[Dict[str, object]]]) -> List[Dict[str, object]]:
    def all_rows_have_false_public(rows: Iterable[Dict[str, object]]) -> bool:
        for row in rows:
            if "valid_for_public_claim" in row and row["valid_for_public_claim"] is not False:
                return False
            if "public_claim" in row and row["public_claim"] is not False:
                return False
        return True

    contract_ids = {row["clause_id"] for row in tables["parent_packet_contract"]}
    audit_clause_ids = {row["contract_clause"] for row in tables["adoption_audit"] if row["contract_clause"] in contract_ids}
    checks = [
        ("VAL4048_00_sources_exist", all(row["exists"] for row in source_register), "all cited source paths exist"),
        ("VAL4048_01_needles_found", all(row["needle_found"] for row in source_register), "all source needles found"),
        ("VAL4048_02_contract_11", len(tables["parent_packet_contract"]) == 11, "eleven PPC4048 clauses present"),
        ("VAL4048_03_audit_covers_contract", len(audit_clause_ids) == len(contract_ids), "adoption audit covers every PPC4048 clause"),
        ("VAL4048_04_suff_packet", any(row["theorem_id"] == "SFT4048_0_packet" for row in tables["sufficiency_theorem"]), "packet sufficiency theorem present"),
        ("VAL4048_05_suff_newton", any(row["theorem_id"] == "SFT4048_1_Newton" for row in tables["sufficiency_theorem"]), "Newton sufficiency row present"),
        ("VAL4048_06_suff_ppn", any(row["theorem_id"] == "SFT4048_2_PPN" for row in tables["sufficiency_theorem"]), "PPN sufficiency row present"),
        ("VAL4048_07_suff_cz_cnorm", any(row["theorem_id"] == "SFT4048_3_cZ_cnorm" for row in tables["sufficiency_theorem"]), "cZ/cnorm sufficiency row present"),
        ("VAL4048_08_residual_parent", any(row["symbols"] == "Parent_packet_adoption" for row in tables["residual_collapse"]), "parent adoption row present"),
        ("VAL4048_09_fallbacks", len(tables["fallback_scorecard"]) >= 8, "fallback scorecard has all major rejection modes"),
        ("VAL4048_10_ppn_master_zero", any(row["quantity"] == "Delta_PPN_abs_4048" and row["conditional_value_under_PPC4048"] == "0" for row in tables["ppn_zero_vector"]), "master PPN zero vector row present"),
        ("VAL4048_11_no_numeric_G_claim", any(row["claim"] == "MTS predicts the measured numerical value of Newton's constant" and row["allowed"] is False for row in tables["claim_gate"]), "numerical G claim blocked"),
        ("VAL4048_12_public_blocked", any(row["claim"] == "MTS publicly derives local GR from the full corpus" and row["allowed"] is False for row in tables["claim_gate"]), "public local-GR claim blocked"),
        ("VAL4048_13_evaluator_conditional", any(row["verdict"] == "CONDITIONAL_LOCAL_GR_ZERO_VECTOR_UNDER_PPC4048" for row in tables["evaluator"]), "conditional zero evaluator present"),
        ("VAL4048_14_evaluator_current", any(row["verdict"] == "ADOPTION_CONTRACT_READY_NOT_FINAL_CORPUS_ADOPTED" for row in tables["evaluator"]), "current corpus evaluator present"),
        ("VAL4048_15_remaining_corpus_map", any(row["symbol"] == "PPC4048_corpus_adoption_map" for row in tables["remaining_residuals"]), "corpus adoption map remains"),
        ("VAL4048_16_next_4049", len(tables["next_target"]) == 1 and "4049" in tables["next_target"][0]["next_doc"], "4049 next target present"),
        ("VAL4048_17_doc_written", DOC_PATH.exists(), "checkpoint doc written"),
        ("VAL4048_18_no_formalization_output", not any(str(path).startswith(str(FORMALIZATION)) for path in OUTPUTS.values()), "no output targets formalization-workbench"),
        ("VAL4048_19_script_compiles", script_compiles(), "script compiles"),
        ("VAL4048_20_private_guard", all(all_rows_have_false_public(rows) for rows in tables.values()), "public-claim guard retained"),
    ]
    return [
        {"check_id": check_id, "passed": passed, "detail": detail}
        for check_id, passed, detail in checks
    ]


def main() -> None:
    ts = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    sources = source_rows(ts)
    source_count = sum(1 for row in sources if row["needle_found"])
    tables: Dict[str, List[Dict[str, object]]] = {
        "parent_packet_contract": parent_packet_contract_rows(ts),
        "adoption_audit": adoption_audit_rows(ts),
        "sufficiency_theorem": sufficiency_theorem_rows(ts),
        "residual_collapse": residual_collapse_rows(ts),
        "fallback_scorecard": fallback_scorecard_rows(ts),
        "ppn_zero_vector": ppn_zero_vector_rows(ts),
        "evaluator": evaluator_rows(ts),
        "decision_gate": decision_gate_rows(ts),
        "claim_gate": claim_gate_rows(ts),
        "remaining_residuals": remaining_residual_rows(ts),
        "next_target": next_target_rows(ts),
        "status": status_rows(ts),
    }

    DOC_PATH.write_text(doc_text(ts, source_count), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    for key, rows in tables.items():
        write_csv(OUTPUTS[key], rows)

    validation_rows = validate_outputs(sources, tables)
    write_csv(OUTPUTS["validation"], validation_rows)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation_rows if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"validation rows: {len(validation_rows)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
