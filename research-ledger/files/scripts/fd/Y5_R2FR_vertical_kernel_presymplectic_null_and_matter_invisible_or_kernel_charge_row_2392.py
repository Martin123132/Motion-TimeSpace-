from __future__ import annotations

import csv
from pathlib import Path


BRANCH_ID = "MTS_R2FR_VERTICAL_KERNEL_PRESYMPLECTIC_NULL_AND_MATTER_INVISIBLE_OR_KERNEL_CHARGE_ROW_2392"
PROJECT_ROOT = Path(
    r"D:\Users\ollet\Desktop\Turn an intuitive research programme into a formal field-theoretic framework\Motion-TimeSpace--main"
)
POST_ROOT = PROJECT_ROOT / "post-checkpoint-work"
RESIDUALS = POST_ROOT / "source-intake" / "mts_residuals"
DOC_PATH = POST_ROOT / "2392-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md"
FORMALIZATION_WORKBENCH = PROJECT_ROOT / "formalization-workbench"


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def contains(path: Path, needle: str) -> bool:
    return needle in read_text(path)


def no_claim() -> str:
    return "false"


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fields})


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_register() -> list[dict[str, object]]:
    sources = [
        {
            "row_id": "SRC2392_00_2391_doc",
            "source_key": "2391_kernel_handoff",
            "source_path": POST_ROOT / "2391-Y5-R2FR-parent-q-Obs-e-functor-construction-or-frame-leak-source-pack.md",
            "needles": [
                "2392-Y5-R2FR-vertical-kernel-presymplectic-null-and-matter-invisible-or-kernel-charge-row.md",
                "epsilon_kernel_charge",
                "presymplectic-null",
            ],
            "source_role": "2391 selects vertical kernel nullness as next gate",
        },
        {
            "row_id": "SRC2392_01_2391_certificates",
            "source_key": "2391_qObs_certificates",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2391_Q_OBS_E_CERTIFICATE.csv",
            "needles": ["QOC2391_2_presymplectic_null", "MISSING_PRESYMPLECTIC_NULL_KERNEL", "QOC2391_6_matter_readout_descent"],
            "source_role": "null-kernel and matter/readout descent gaps",
        },
        {
            "row_id": "SRC2392_02_2391_leaks",
            "source_key": "2391_qObs_leaks",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_2391_Q_OBS_E_LEAK_VALUES.csv",
            "needles": ["epsilon_kernel_charge", "epsilon_q_rank_or_integrability", "epsilon_projection_declaration"],
            "source_role": "kernel charge/rank/tautology leak rows",
        },
        {
            "row_id": "SRC2392_03_1736_doc",
            "source_key": "1736_Dq_tau_commutator",
            "source_path": POST_ROOT / "1736-Y5-R2FR-Dq-tau-commutator-zero-or-first-finite-bound-row.md",
            "needles": ["exact commutator-zero route exists", "vertical basis", "E_Dq_tau_commutator_norm"],
            "source_role": "tau/projectability and vertical-basis obstruction",
        },
        {
            "row_id": "SRC2392_04_1737_doc",
            "source_key": "1737_q_Dq_basis",
            "source_path": POST_ROOT / "1737-Y5-R2FR-q-map-Dq-vertical-basis-source-row-or-coframe-functor-zero.md",
            "needles": ["visible quotient candidate `Q_vis`", "DObs_e[v]=0", "finite nonclaim source rows"],
            "source_role": "visible quotient and finite Dq rows",
        },
        {
            "row_id": "SRC2392_05_1756_doc",
            "source_key": "1756_hidden_source",
            "source_path": POST_ROOT / "1756-Y5-R2FR-two-slot-source-free-owner-or-hidden-source-counterexample-ledger.md",
            "needles": ["delta_X S_parent = L_X X + J_hidden + gated coupling terms + boundary", "proof not closed"],
            "source_role": "hidden source and boundary terms obstruct matter-invisible kernel",
        },
        {
            "row_id": "SRC2392_06_1760_doc",
            "source_key": "1760_matter_descent",
            "source_path": POST_ROOT / "1760-Y5-R2FR-matter-worldtube-quotient-descent-or-Amatter-bound.md",
            "needles": ["delta_v S_matter=0", "V_m[X,rho_A,W_source]", "A_matter"],
            "source_role": "conditional matter/worldtube descent and live direct-slot obstruction",
        },
        {
            "row_id": "SRC2392_07_1008_doc",
            "source_key": "1008_theta_Qtau",
            "source_path": POST_ROOT / "1008-Y5-R10-parent-theta-Qtau-extraction-or-charge-decomposition-runner.md",
            "needles": ["theta_MTS", "Q_tau^MTS", "not closed"],
            "source_role": "parent symplectic potential/Noether charge extraction still missing",
        },
        {
            "row_id": "SRC2392_08_1009_doc",
            "source_key": "1009_parent_action_contract",
            "source_path": POST_ROOT / "1009-Y5-R10-parent-current-chain-action-contract-or-sector-variation-runner.md",
            "needles": ["minimum parent-action blocks", "no total parent action is promoted", "local-GR claim"],
            "source_role": "parent action blocks organized but not promoted",
        },
        {
            "row_id": "SRC2392_09_1575_doc",
            "source_key": "1575_vertical_generator",
            "source_path": POST_ROOT / "1575-Y5-RAB-parent-RAB-vertical-generator-and-matter-descent-signature.md",
            "needles": ["`v_R in ker(Dq)`", "NOT_PARENT_SIGNED", "matter descent"],
            "source_role": "example vertical-generator signature still not parent-signed",
        },
        {
            "row_id": "SRC2392_10_1736_commutator_csv",
            "source_key": "1736_commutator_audit",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1736_COMMUTATOR_PROOF_AUDIT.csv",
            "needles": ["DTC1736_1_vertical_basis", "DTC1736_6_source_readout_guard"],
            "source_role": "machine audit for vertical basis and source/readout reopening guard",
        },
        {
            "row_id": "SRC2392_11_1756_owner_csv",
            "source_key": "1756_two_slot_owner",
            "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1756_TWO_SLOT_SOURCE_FREE_OWNER_PROOF_ATTEMPT.csv",
            "needles": ["OP1756_4_quotient_matter", "OP1756_6_boundary_history"],
            "source_role": "machine proof attempt for quotient matter and boundary/history silence",
        },
        {
            "row_id": "SRC2392_12_1008_variation_csv",
            "source_key": "1008_parent_variation",
            "source_path": RESIDUALS / "P8_Y5_R10_1008_PARENT_VARIATION_AUDIT.csv",
            "needles": ["PVA1008_0_parent_action", "PVA1008_1_theta_MTS", "PVA1008_6_verdict"],
            "source_role": "parent action/theta extraction audit",
        },
    ]
    rows: list[dict[str, object]] = []
    for source in sources:
        path = Path(source["source_path"])
        needles = list(source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": source["row_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": str(path.exists()).lower(),
                "required": "true",
                "needles_found": str(all(contains(path, needle) for needle in needles)).lower(),
                "needles": "; ".join(needles),
                "source_role": source["source_role"],
                "valid_for_claim": no_claim(),
            }
        )
    return rows


def nullness_theorem_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKN2392_0_kernel_target",
            "step": "kernel target",
            "statement": "For V=ker(Dq) to be a true quotient fibre, each vertical v must be a parent variation whose flow preserves q, e_obs, tau projection, source/readout maps, and boundary class before fitting.",
            "derivation_status": "CONDITIONAL_TARGET",
            "current_gain": "turns verticality into a checkable parent signature rather than a label",
            "remaining_gap": "V, Dq, tau pushforward, and readout guard are not jointly parent-signed",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKN2392_1_presymplectic_null",
            "step": "presymplectic-null charge test",
            "statement": "The kernel is physically null only if i_v Theta_parent = dB_v plus constraints and the compact local flux integral_S(delta Q_v - i_v Theta_parent) vanishes or is bounded.",
            "derivation_status": "CONDITIONAL_COVARIANT_PHASE_SPACE_TEST",
            "current_gain": "makes projection-by-declaration impossible unless the vertical direction carries no Hamiltonian charge",
            "remaining_gap": "Theta_parent, Q_v, B_v, constraints, and zero compact flux are not extracted",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKN2392_2_matter_invisible",
            "step": "matter invisibility test",
            "statement": "For ordinary matter, delta_v S_matter=0 follows if S_matter descends through q/e_obs, matter lifts are fixed over q, and no direct V_m[v,rho_A,W_source,C_top] or source-prefactor slot exists.",
            "derivation_status": "CONDITIONAL_CHAIN_RULE_TEST",
            "current_gain": "separates quotient matter descent from hidden source couplings",
            "remaining_gap": "direct-slot exclusion, matter lift, worldtube/support descent, and source-prefactor silence remain unsigned",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKN2392_3_boundary_history_silence",
            "step": "boundary/history silence",
            "statement": "Even if bulk matter is invisible, the kernel is not null if boundary, history, reference, domain, or source-support tails have Pi_local dB_v or J_history[v] flux.",
            "derivation_status": "OBSTRUCTION_RETAINED",
            "current_gain": "prevents boundary terms from being hidden under the word gauge",
            "remaining_gap": "zero compact boundary flux and history-tail theorem are missing",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKN2392_4_rank_integrability",
            "step": "rank and involutivity test",
            "statement": "V must be a regular involutive distribution: [v_i,v_j] must lie in V and rank(Dq) must be constant on the local branch, or q is not a stable quotient chart.",
            "derivation_status": "CONDITIONAL_GEOMETRY_TEST",
            "current_gain": "adds the missing quotient-geometry gate before any q/Obs_e claim",
            "remaining_gap": "vertical basis, bracket table, rank audit, and units/norms remain missing",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKN2392_5_verdict",
            "step": "current verdict",
            "statement": "2392 does not close the kernel. It proves the exact contract: V must be regular, parent-presymplectic-null, matter/readout-invisible, and boundary/history silent. Current MTS has not yet supplied the parent action objects needed to claim that.",
            "derivation_status": "ROUTE_EXACT_NOT_CLAIMED",
            "current_gain": "the next bottleneck is parent Theta/Q_v extraction for vertical variations",
            "remaining_gap": "kernel-charge rows remain nonclaim",
            "valid_for_claim": no_claim(),
        },
    ]


def certificate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKC2392_0_vertical_basis",
            "certificate": "parent vertical basis",
            "required_test": "list v_i as parent variations and prove v_i in ker(Dq), not just gauge by analogy",
            "status": "MISSING_PARENT_VERTICAL_BASIS",
            "residual_if_missing": "epsilon_q_rank_or_integrability",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKC2392_1_rank_involutive",
            "certificate": "regular involutive quotient distribution",
            "required_test": "rank(Dq) constant and [v_i,v_j] in span(V) with sourced bracket table/norm",
            "status": "MISSING_RANK_AND_BRACKET_AUDIT",
            "residual_if_missing": "epsilon_q_rank_or_integrability",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKC2392_2_theta_Qv",
            "certificate": "parent Theta/Q_v extraction",
            "required_test": "derive delta L_parent = E delta Phi + dTheta_parent and J_v = Theta_parent(v)-i_v L = dQ_v + constraints",
            "status": "MISSING_THETA_PARENT_AND_QV",
            "residual_if_missing": "epsilon_kernel_charge",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKC2392_3_zero_compact_flux",
            "certificate": "zero compact local flux",
            "required_test": "integral_S(delta Q_v - i_v Theta_parent) plus boundary/reference improvements vanishes on linked local surfaces",
            "status": "MISSING_ZERO_COMPACT_FLUX_CERTIFICATE",
            "residual_if_missing": "epsilon_kernel_charge",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKC2392_4_matter_descent",
            "certificate": "matter-invisible kernel",
            "required_test": "S_matter descends through q/e_obs and matter lifts/constants are fixed over q for every v_i",
            "status": "MISSING_MATTER_DESCENT_SIGNATURE",
            "residual_if_missing": "epsilon_matter_kernel",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKC2392_5_no_direct_source_slot",
            "certificate": "no direct source/worldtube/material slots",
            "required_test": "exclude V_m[v,rho_A,W_source,C_top], source prefactors, material markers, and support terms outside q",
            "status": "MISSING_NO_DIRECT_SOURCE_SLOT_PROOF",
            "residual_if_missing": "epsilon_hidden_source_slot",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKC2392_6_boundary_history",
            "certificate": "boundary/history/reference silence",
            "required_test": "Pi_local dB_v=0 and J_history[v]=0 or bounded for compact local domains",
            "status": "MISSING_BOUNDARY_HISTORY_SILENCE",
            "residual_if_missing": "epsilon_boundary_history",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKC2392_7_MHref",
            "certificate": "positive same-frame M_H_ref",
            "required_test": "derive H_tau-H_ref in the same q/Obs_e/tau branch before normalizing kernel leakage",
            "status": "MISSING_POSITIVE_SAME_FRAME_MHREF",
            "residual_if_missing": "all normalized rows remain non-score-ready",
            "valid_for_claim": no_claim(),
        },
    ]


def leak_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKL2392_0_rank_integrability",
            "quantity": "epsilon_q_rank_or_integrability",
            "formula": "||[v_i,v_j] mod V|| + ||rank(Dq)-rank_expected||",
            "units": "field-space quotient defect",
            "current_value": "MISSING_VERTICAL_BASIS;MISSING_BRACKET_TABLE;MISSING_RANK_AUDIT",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKL2392_1_kernel_charge",
            "quantity": "epsilon_kernel_charge",
            "formula": "abs(integral_S (delta Q_v - i_v Theta_parent + boundary_improvements))/M_H_ref",
            "units": "dimensionless Hamiltonian charge leakage",
            "current_value": "MISSING_THETA_PARENT;MISSING_Q_V;MISSING_BOUNDARY_IMPROVEMENTS;MISSING_ZERO_FLUX_CERTIFICATE;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKL2392_2_matter_kernel",
            "quantity": "epsilon_matter_kernel",
            "formula": "abs(delta_v S_matter_on_shell)/M_H_ref",
            "units": "dimensionless matter-source leakage after normalization",
            "current_value": "MISSING_MATTER_DESCENT;MISSING_MATTER_LIFT;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKL2392_3_hidden_source_slot",
            "quantity": "epsilon_hidden_source_slot",
            "formula": "abs(partial_v V_m[v,rho_A,W_source,C_top]) / M_H_ref",
            "units": "dimensionless hidden-source leakage",
            "current_value": "MISSING_NO_DIRECT_SLOT_PROOF;MISSING_VM_DENSITY;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKL2392_4_boundary_history",
            "quantity": "epsilon_boundary_history",
            "formula": "abs(integral_S Pi_local dB_v + integral_history J_history[v]) / M_H_ref",
            "units": "dimensionless boundary/history leakage",
            "current_value": "MISSING_BOUNDARY_FLUX;MISSING_HISTORY_TAIL;MISSING_M_H_REF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKL2392_5_projection_declaration",
            "quantity": "epsilon_projection_declaration",
            "formula": "1 if q/Obs_e relies on q_candidate containing e_obs before null-kernel proof else 0",
            "units": "boolean guard",
            "current_value": "MISSING_NULL_KERNEL_PROOF",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "VKL2392_6_total",
            "quantity": "Delta_vertical_kernel_total_over_MH",
            "formula": "epsilon_q_rank_or_integrability + epsilon_kernel_charge + epsilon_matter_kernel + epsilon_hidden_source_slot + epsilon_boundary_history + epsilon_projection_declaration",
            "units": "dimensionless",
            "current_value": "COMPONENTS_MISSING",
            "score_ready": "false",
            "valid_for_claim": no_claim(),
        },
    ]


def decision_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2392_0_accept_kernel_contract",
            "decision": "accept vertical kernel nullness as the required q/Obs_e promotion gate",
            "reason": "q/Obs_e descent is only physical if the quotient kernel carries no charge and no matter/readout source",
            "consequence": "projection-by-declaration is blocked until nullness certificates exist",
            "status": "CONDITIONAL_KERNEL_CONTRACT_ACCEPTED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2392_1_no_promotion",
            "decision": "do not promote vertical kernel nullness for current MTS",
            "reason": "parent Theta/Q_v, vertical basis, rank/bracket audit, matter descent, direct-slot exclusion, boundary/history silence, and M_H_ref remain missing",
            "consequence": "parent q/Obs_e, same-frame, J_H, W_source, local-GR and Newton claims remain blocked",
            "status": "VERTICAL_KERNEL_NULLNESS_NOT_PARENT_SIGNED",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "DEC2392_2_charge_first",
            "decision": "attack parent Theta/Q_v extraction next",
            "reason": "without the covariant phase-space charge test there is no way to tell gauge fibre from hidden physical charge",
            "consequence": "2393 should derive vertical Noether charge Q_v or fill epsilon_kernel_charge with sourced finite rows",
            "status": "SELECT_2393_VERTICAL_NOETHER_CHARGE",
            "valid_for_claim": no_claim(),
        },
    ]


def claim_gate_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2392_0_contract_shape",
            "gate": "vertical kernel nullness contract shape",
            "gate_status": "PASS_CONDITIONAL_THEOREM_ONLY",
            "claim_effect": "use as gate; not evidence of current-MTS closure",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2392_1_vertical_basis",
            "gate": "parent vertical basis and rank/involutivity",
            "gate_status": "FAIL",
            "claim_effect": "quotient geometry not promoted",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2392_2_presymplectic_charge",
            "gate": "Theta/Q_v compact-flux zero",
            "gate_status": "FAIL",
            "claim_effect": "kernel may carry hidden Hamiltonian charge",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2392_3_matter_invisible",
            "gate": "matter/readout invisibility",
            "gate_status": "FAIL",
            "claim_effect": "kernel may source matter/readout",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2392_4_MHref",
            "gate": "positive same-frame M_H_ref",
            "gate_status": "FAIL",
            "claim_effect": "normalized kernel rows remain non-score-ready",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "CG2392_5_GR_Newton",
            "gate": "local GR/Newton from null kernel",
            "gate_status": "BLOCKED",
            "claim_effect": "no GR/Newton reduction claim from 2392",
            "valid_for_claim": no_claim(),
        },
    ]


def refusal_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2392_0_claim_null_kernel",
            "claim": "V=ker(Dq) is parent-null and matter-invisible for current MTS",
            "allowed": "false",
            "reason": "vertical basis, rank/involutivity, Theta/Q_v, zero flux, matter descent, direct-slot exclusion, boundary silence, and M_H_ref are unsigned",
            "blocking_rows": "VKC2392_0_vertical_basis;VKC2392_2_theta_Qv;VKC2392_4_matter_descent;VKC2392_7_MHref",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2392_1_call_kernel_gauge",
            "claim": "vertical directions are harmless gauge by definition",
            "allowed": "false",
            "reason": "gauge status requires presymplectic-null charge and matter/readout invisibility, not naming",
            "blocking_rows": "VKC2392_2_theta_Qv;VKC2392_3_zero_compact_flux;VKC2392_4_matter_descent",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2392_2_ignore_boundary",
            "claim": "bulk matter invisibility is enough",
            "allowed": "false",
            "reason": "boundary/history/source-support flux can reopen the kernel as a physical charge channel",
            "blocking_rows": "VKC2392_6_boundary_history;VKL2392_4_boundary_history",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "REF2392_3_claim_GR_Newton",
            "claim": "local GR/Newton follows from a conditional null-kernel contract",
            "allowed": "false",
            "reason": "the kernel contract is necessary but not sufficient; q/Obs_e, EH exterior, source charge, M_H_ref, Poisson/Gauss, PPN, and boundary locks remain required",
            "blocking_rows": "CG2392_5_GR_Newton;VKC2392_7_MHref",
            "valid_for_claim": no_claim(),
        },
    ]


def next_target_rows() -> list[dict[str, object]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2392_0_selected",
            "next_file": "2393-Y5-R2FR-vertical-Noether-charge-Qv-extraction-or-kernel-charge-source-row.md",
            "success_condition": "derive Theta_parent and Q_v for vertical variations and prove integral_S(delta Q_v - i_v Theta_parent)=0 on compact local surfaces",
            "fallback_condition": "fill epsilon_kernel_charge with source paths, units, boundary-improvement terms, denominator status, and valid_for_claim=false",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2392_1_parallel",
            "next_file": "2393b-Y5-R2FR-vertical-basis-rank-bracket-audit-or-epsilon-q-integrability-row.md",
            "success_condition": "list v_i, prove v_i in ker(Dq), constant rank, and [v_i,v_j] in V",
            "fallback_condition": "fill epsilon_q_rank_or_integrability with bracket/rank source rows",
            "valid_for_claim": no_claim(),
        },
        {
            "branch_id": BRANCH_ID,
            "row_id": "NEXT2392_2_parallel",
            "next_file": "2393c-Y5-R2FR-matter-boundary-invisibility-or-hidden-source-kernel-bound.md",
            "success_condition": "prove delta_v S_matter=0 plus boundary/history/source-support silence for each v_i",
            "fallback_condition": "fill epsilon_matter_kernel, epsilon_hidden_source_slot, and epsilon_boundary_history",
            "valid_for_claim": no_claim(),
        },
    ]


CSV_BUILDERS = {
    "P8_Y5_PARENT_QLOC_2392_SOURCE_REGISTER.csv": source_register,
    "P8_Y5_PARENT_QLOC_2392_VERTICAL_KERNEL_NULLNESS_THEOREM.csv": nullness_theorem_rows,
    "P8_Y5_PARENT_QLOC_2392_VERTICAL_KERNEL_CERTIFICATE.csv": certificate_rows,
    "P8_Y5_PARENT_QLOC_2392_KERNEL_CHARGE_LEAK_VALUES.csv": leak_rows,
    "P8_Y5_PARENT_QLOC_2392_DECISION_LEDGER.csv": decision_rows,
    "P8_Y5_PARENT_QLOC_2392_CLAIM_GATES.csv": claim_gate_rows,
    "P8_Y5_PARENT_QLOC_2392_REFUSAL_RUNNER.csv": refusal_rows,
    "P8_Y5_PARENT_QLOC_2392_NEXT_TARGET.csv": next_target_rows,
}


def check_no_positive_claim_flags(paths: list[Path]) -> bool:
    for path in paths:
        if not path.exists():
            continue
        for row in read_csv(path):
            if str(row.get("valid_for_claim", "")).strip().lower() == "true":
                return False
    return True


def validation_rows() -> list[dict[str, object]]:
    csv_paths = [RESIDUALS / name for name in CSV_BUILDERS]
    rows: list[dict[str, object]] = []

    def add(row_id: str, passed: bool, detail: str) -> None:
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "row_id": row_id,
                "status": "PASS" if passed else "FAIL",
                "detail": detail,
                "valid_for_claim": no_claim(),
            }
        )

    sources = source_register()
    add("VAL2392_00_sources_exist", all(row["exists"] == "true" for row in sources), "all required source paths exist")
    add("VAL2392_01_needles_found", all(row["needles_found"] == "true" for row in sources), "all source needles found")
    theorem = nullness_theorem_rows()
    add(
        "VAL2392_02_presymplectic_test_present",
        any("i_v Theta_parent = dB_v" in row["statement"] for row in theorem),
        "presymplectic-null charge test is present",
    )
    add(
        "VAL2392_03_matter_invisible_present",
        any("delta_v S_matter=0" in row["statement"] for row in theorem),
        "matter-invisibility chain-rule test is present",
    )
    add(
        "VAL2392_04_boundary_guard_present",
        any("boundary" in row["statement"] and "history" in row["statement"] for row in theorem),
        "boundary/history silence guard is present",
    )
    certs = certificate_rows()
    add(
        "VAL2392_05_required_gaps_explicit",
        all("MISSING" in row["status"] for row in certs),
        "vertical/theta/Qv/flux/matter/direct-slot/boundary/MHref gaps explicit",
    )
    values = leak_rows()
    add(
        "VAL2392_06_value_rows_nonready",
        all(
            row["score_ready"] == "false"
            and (("MISSING" in row["current_value"]) or row["current_value"] == "COMPONENTS_MISSING")
            for row in values
        ),
        "kernel charge/source leak rows remain non-score-ready",
    )
    gates = claim_gate_rows()
    add(
        "VAL2392_07_global_claims_blocked",
        all(row["gate_status"] != "PASS" for row in gates if row["row_id"] != "CG2392_0_contract_shape"),
        "global/local gates remain blocked",
    )
    add(
        "VAL2392_08_csv_parse",
        all(path.exists() and len(read_csv(path)) > 0 for path in csv_paths),
        "generated CSVs parse and have rows",
    )
    add("VAL2392_09_no_claim_flags", check_no_positive_claim_flags(csv_paths), "no generated row has valid_for_claim=true")
    add(
        "VAL2392_10_formalization_untouched_by_script",
        FORMALIZATION_WORKBENCH not in DOC_PATH.parents and all(FORMALIZATION_WORKBENCH not in path.parents for path in csv_paths),
        "script writes only post-checkpoint-work outputs",
    )
    add(
        "VAL2392_11_next_selected",
        any(row["row_id"] == "NEXT2392_0_selected" for row in next_target_rows()),
        "vertical Noether charge extraction selected next",
    )
    overall = all(row["status"] == "PASS" for row in rows)
    add(
        "VAL2392_OVERALL",
        overall,
        "2392 states the exact vertical-kernel nullness contract, refuses gauge-by-name without Theta/Qv/matter/boundary certificates, and selects vertical Noether charge extraction next",
    )
    return rows


def md_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ")


def markdown_table(rows: list[dict[str, object]], columns: list[str]) -> str:
    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(md_escape(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def write_doc() -> None:
    source_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2392_SOURCE_REGISTER.csv")
    theorem = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2392_VERTICAL_KERNEL_NULLNESS_THEOREM.csv")
    certs = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2392_VERTICAL_KERNEL_CERTIFICATE.csv")
    values = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2392_KERNEL_CHARGE_LEAK_VALUES.csv")
    decisions = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2392_DECISION_LEDGER.csv")
    gates = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2392_CLAIM_GATES.csv")
    refusals = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2392_REFUSAL_RUNNER.csv")
    next_rows = read_csv(RESIDUALS / "P8_Y5_PARENT_QLOC_2392_NEXT_TARGET.csv")
    validation = read_csv(RESIDUALS / "P8_Y5_BRR545_2392_VALIDATION.csv")

    body = f"""# 2392 - vertical kernel presymplectic-null and matter-invisible or kernel-charge row

## Result

2392 tests whether the quotient kernel is a real gauge/null fibre or merely a renamed physical sector.

The required contract is:

1. `V=ker(Dq)` is a parent-defined vertical distribution with explicit basis vectors `v_i`.
2. `V` is regular and involutive, so the quotient is a stable local chart.
3. Each vertical vector is presymplectic-null:
   `i_v Theta_parent = dB_v + constraints`,
   and the compact local charge
   `integral_S(delta Q_v - i_v Theta_parent + boundary_improvements)` vanishes or is bounded.
4. Matter and readout are invisible along the kernel:
   `delta_v S_matter=0`,
   no direct `V_m[v,rho_A,W_source,C_top]` slot,
   no material marker/source prefactor,
   and no boundary/history/source-support tail.

This is the exact gate that stops `q/Obs_e` from becoming projection-by-declaration.

Current MTS does not yet sign the vertical basis, rank/bracket audit, parent `Theta_parent`, vertical charge `Q_v`,
zero compact flux, matter descent, no-direct-source-slot rule, boundary/history silence, or positive same-frame
`M_H_ref`.

So 2392 is not a kernel-nullness proof.  It is a sharpened theorem-or-bound contract.  No parent `q/Obs_e` pass,
same-frame pass, `J_H` pass, `W_source` pass, local-GR pass, Newton pass, PPN, clock, orbital, R10, or public/GitHub
claim is made.

## Source Register

{markdown_table(source_rows, ["row_id", "source_key", "source_path", "exists", "needles_found", "source_role", "valid_for_claim"])}

## Vertical Kernel Nullness Theorem

{markdown_table(theorem, ["row_id", "step", "statement", "derivation_status", "current_gain", "remaining_gap", "valid_for_claim"])}

## Vertical Kernel Certificate

{markdown_table(certs, ["row_id", "certificate", "required_test", "status", "residual_if_missing", "valid_for_claim"])}

## Kernel Charge Leak Values

{markdown_table(values, ["row_id", "quantity", "formula", "units", "current_value", "score_ready", "valid_for_claim"])}

## Decision Ledger

{markdown_table(decisions, ["row_id", "decision", "reason", "consequence", "status", "valid_for_claim"])}

## Claim Gates

{markdown_table(gates, ["row_id", "gate", "gate_status", "claim_effect", "valid_for_claim"])}

## Refusal Runner

{markdown_table(refusals, ["row_id", "claim", "allowed", "reason", "blocking_rows", "valid_for_claim"])}

## Next Target

{markdown_table(next_rows, ["row_id", "next_file", "success_condition", "fallback_condition", "valid_for_claim"])}

## Validation

{markdown_table(validation, ["row_id", "status", "detail", "valid_for_claim"])}

## Practical Status

This is a hard but useful narrowing.  If the vertical charge test closes, the q/Obs_e route gets much more serious.
If it does not, we have found a real physical residual rather than a philosophical objection.  The next best target is
therefore `Q_v`: extract the vertical Noether charge or write the kernel-charge row honestly.
"""
    DOC_PATH.write_text(body, encoding="utf-8")


def main() -> None:
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for name, builder in CSV_BUILDERS.items():
        write_csv(RESIDUALS / name, builder())
    write_csv(RESIDUALS / "P8_Y5_BRR545_2392_VALIDATION.csv", validation_rows())
    write_doc()
    print(f"wrote {DOC_PATH}")
    print(f"wrote {RESIDUALS / 'P8_Y5_BRR545_2392_VALIDATION.csv'}")


if __name__ == "__main__":
    main()
