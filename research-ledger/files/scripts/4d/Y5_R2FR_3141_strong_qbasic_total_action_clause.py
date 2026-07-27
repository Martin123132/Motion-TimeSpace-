from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3141_INPUTS.csv"
GLUING = OUT / "P8_Y5_R2FR_3141_QBASIC_GLUING_THEOREM.csv"
CONTRACT = OUT / "P8_Y5_R2FR_3141_TOTAL_ACTION_CONTRACT.csv"
AUDIT = OUT / "P8_Y5_R2FR_3141_SECTOR_QBASIC_AUDIT.csv"
OBSTRUCTIONS = OUT / "P8_Y5_R2FR_3141_OBSTRUCTION_TO_FORK_LEDGER.csv"
DECISION = OUT / "P8_Y5_R2FR_3141_DECISION.csv"
GATE = OUT / "P8_Y5_R2FR_3141_GATE.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3141_VALIDATION.csv"


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def source_path(relative: str) -> str:
    return str((ROOT / relative).resolve())


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
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
        for row in rows:
            writer.writerow(row)


def input_rows() -> list[dict[str, str]]:
    now = stamp()
    rows = [
        {
            "source_id": "SRC3141_0_3140_doc",
            "path": source_path("3140-Y5-R2FR-theta-descent-from-qbasic-action-under-AX1090.md"),
            "role": "strong q-basic total action handoff",
        },
        {
            "source_id": "SRC3141_1_3140_theorem",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R2FR_3140_THETA_DESCENT_THEOREM.csv"
            ),
            "role": "theta descent from strong q-basic action",
        },
        {
            "source_id": "SRC3141_2_3138_construction",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R2FR_3138_TYPED_QOBS_CONSTRUCTION.csv"
            ),
            "role": "typed Q_obs/Obs_e/Rep(Q_obs) construction",
        },
        {
            "source_id": "SRC3141_3_252_projector",
            "path": source_path("252-topological-projector-parent-action-skeleton.md"),
            "role": "topological projector action skeleton",
        },
        {
            "source_id": "SRC3141_4_407_relational",
            "path": source_path("407-primitive-relational-quotient-action-sketch.md"),
            "role": "primitive relational quotient action sketch",
        },
        {
            "source_id": "SRC3141_5_410_matter",
            "path": source_path("410-quotient-matter-functor-theorem-attempt.md"),
            "role": "matter functor factorization attempt",
        },
        {
            "source_id": "SRC3141_6_1057_unique_F2",
            "path": source_path(
                "1057-Y5-R10-unique-Maxwell-subblock-no-independent-F2-ban-or-balpha-retention.md"
            ),
            "role": "unique Maxwell subblock/no independent F2 attempt",
        },
        {
            "source_id": "SRC3141_7_1099_EM_owner",
            "path": source_path(
                "1099-Y5-R10-unique-EM-kinetic-owner-no-extra-F2-theorem-or-alpha-coefficient-source-row.md"
            ),
            "role": "unique EM kinetic owner theorem attempt",
        },
        {
            "source_id": "SRC3141_8_1100_TQ",
            "path": source_path(
                "1100-Y5-R10-parent-TQ-owner-fixed-charge-lattice-and-gauge-norm-signature.md"
            ),
            "role": "T_Q/gauge norm and charge lattice owner attempt",
        },
        {
            "source_id": "SRC3141_9_1889_source",
            "path": source_path(
                "1889-Y5-R2FR-source-current-Ward-owner-or-real-deltaw-component-basis.md"
            ),
            "role": "source-current Ward owner and label-forgetting contract",
        },
        {
            "source_id": "SRC3141_10_1890_no_prefactor",
            "path": source_path(
                "1890-Y5-R2FR-no-source-prefactor-parent-action-clause-or-component-basis-first-source-row.md"
            ),
            "role": "no source-prefactor parent action clause attempt",
        },
        {
            "source_id": "SRC3141_11_890_boundary",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R10_890_BOUNDARY_NO_TAIL_THEOREM_ATTEMPT.csv"
            ),
            "role": "boundary no-tail theorem attempt",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def gluing_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "theorem_id": "QBG3141_0_sector_premise",
            "statement": "For each sector s, L_s(Phi)=q^* Lbar_s(Q_obs,Rep(Q_obs),J_Q) + dB_s.",
            "proof": "definition of strong q-basic local n-form sector",
            "status": "premise_schema",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "QBG3141_1_finite_sum",
            "statement": "A finite sum of q-basic local n-forms is q-basic.",
            "proof": "sum_s L_s = q^*(sum_s Lbar_s) + d(sum_s B_s)",
            "status": "exact_theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "QBG3141_2_total_action",
            "statement": "If every geometry/projector/EM/matter/source/boundary sector satisfies QBG3141_0, then L_parent=q^*Lbar_total+dB_total.",
            "proof": "apply finite-sum theorem and define Lbar_total by the sector sum over Q_obs and Rep(Q_obs)",
            "status": "conditional_total_action_theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "QBG3141_3_theta_kernel_transfer",
            "statement": "QBG3141_2 feeds 3140, so theta descent follows; with boundary silence it feeds 3139 kernel-null.",
            "proof": "3140 proves theta descent from strong q-basic action; 3139 proves kernel-null from theta descent plus boundary/matter/source silence",
            "status": "conditional_chain_closed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "QBG3141_4_no_single_sector_exception",
            "statement": "One non-q-basic sector prevents total q-basicness unless it is moved into an explicit residual row.",
            "proof": "a surviving representative-dependent term cannot be absorbed into q^*Lbar_total without adding it to Q_obs or a residual coefficient",
            "status": "exact_guard",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def contract_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "contract_id": "QBC3141_0_total",
            "sector": "total action",
            "required_form": "L_parent = q^*Lbar_total(Q_obs,Rep(Q_obs),J_Q) + dB_total",
            "owned_objects": "Q_obs; Obs_e; Rep(Q_obs); A_Q/T_Q if EM exists; Hilbert source current; boundary primitive",
            "forbidden_slots": "representative Xhat; species source weights; hidden scalar F2 coefficient; disformal frame; non-Hilbert source mask",
            "effect_if_signed": "3140 theta descent and 3139 kernel-null premises collapse into one total-action theorem plus boundary silence",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "QBC3141_1_geometry",
            "sector": "geometry/EH",
            "required_form": "L_geom=q^*Lbar_EH(e_obs,omega_obs,Lambda,G_ref)+dB_geom",
            "owned_objects": "e_obs from Obs_e; same-frame connection; universal constants",
            "forbidden_slots": "A(X)R; F(sigma)R; disformal matter-frame EH rewrite",
            "effect_if_signed": "left-hand GR operator is q-basic in local exterior",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "QBC3141_2_projector_domain",
            "sector": "projector/domain",
            "required_form": "L_proj=q^*Lbar_proj([C]_PD,[J_rel],boundary_class)+dB_proj",
            "owned_objects": "metric-independent relative/topological projector P_D",
            "forbidden_slots": "Hodge/least-energy metric projector; local scalar class mode; unowned domain clock",
            "effect_if_signed": "projector contributes no bulk local stress and can be part of q-basic action",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "QBC3141_3_EM",
            "sector": "EM/Maxwell",
            "required_form": "L_EM=q^*(-C_P/4 mu_obs <F_Q T_Q,F_Q T_Q>_P) with T_Q,N_Q fixed representation data",
            "owned_objects": "parent T_Q; fixed charge lattice; fixed gauge norm/level; A_Q current owner",
            "forbidden_slots": "lambda_A F_Q^2; f_X(Xhat)F_Q^2; radiative/readout alpha re-entry",
            "effect_if_signed": "b_alpha=0 by chain rule and EM Hilbert stress/Poynting readout is owned",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "QBC3141_4_matter",
            "sector": "ordinary matter/clock constants",
            "required_form": "L_matter=sum_A L_A(Psi_A,Obs_e(Q_obs),A_Q,theta_A) over Rep(Q_obs)",
            "owned_objects": "theta_A as fixed representation/superselection labels; masses/charges/clock constants",
            "forbidden_slots": "theta_A(marker,Xhat); species-only action scales; nonminimal hidden clock coupling",
            "effect_if_signed": "b_clock,b_mass and representation part of b_alpha vanish",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "QBC3141_5_source",
            "sector": "source/current coupling",
            "required_form": "J_source = delta L_matter/delta e_obs and F_src(q_src(T_total))=kappa_univ T_total",
            "owned_objects": "total Hilbert current; label-forgotten source functor; projected measured mass",
            "forbidden_slots": "w_A S_A; kappa_A T_A; post-readout source masks; non-Hilbert current",
            "effect_if_signed": "source coupling is calibrated after one common-mode G/GM normalization, not species-weighted",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "contract_id": "QBC3141_6_boundary",
            "sector": "boundary/no-tail",
            "required_form": "B_total=sum_s B_s with int_boundary Xi_v(delta)=0 for local compact admissible variations",
            "owned_objects": "boundary primitive; admissible local worldtube; no edge/source tail",
            "forbidden_slots": "measured edge charge; source-support shift; boundary exchange current",
            "effect_if_signed": "boundary-exact symplectic current becomes zero charge for local kernel directions",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def audit_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "audit_id": "QBA3141_0_geometry",
            "sector": "geometry/EH",
            "current_evidence": "3138/3140 provide Q_obs/Obs_e target; 711/946 retain frame-transfer/EH-prefactor blockers",
            "current_status": "conditional_not_parent_signed",
            "main_obstruction": "A(X)R or same-frame EH operator not fully owned",
            "residual_if_fail": "c_g/b_g; A_EH(X); PPN gamma/beta residual",
            "next_needed": "same-frame EH operator and no-prefactor theorem",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "QBA3141_1_projector",
            "sector": "projector/domain",
            "current_evidence": "251/252 provide topological route; 272 gives conditional quotient; FLRW/Bmem and boundary no-tail remain open",
            "current_status": "conditional_topological_route_not_total_action_signed",
            "main_obstruction": "metric-independent P_D not fully unified with FLRW and local boundary silence",
            "residual_if_fail": "projector bulk stress; Delta_W_support; q_nonH",
            "next_needed": "P_D parent owner plus boundary primitive zero",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "QBA3141_2_EM",
            "sector": "EM/Maxwell",
            "current_evidence": "1057/1099/1100 give exact conditional theorem but retain no-extra-F2, T_Q norm, current, and readout blockers",
            "current_status": "conditional_exact_balpha_zero_not_parent_signed",
            "main_obstruction": "independent lambda_A/f_X F_Q^2 remains legal; T_Q/gauge norm not fixed",
            "residual_if_fail": "b_alpha; beta_source_alpha; EM stress/Poynting readout uncertainty",
            "next_needed": "parent T_Q/gauge norm plus no-extra-F2 operator-domain exhaustion",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "QBA3141_3_matter",
            "sector": "ordinary matter",
            "current_evidence": "410/3137 give conditional Rep(Q_obs) matter theorem; no-marker and constant-sector ownership remain unsigned",
            "current_status": "conditional_matter_functor_not_parent_signed",
            "main_obstruction": "matter constants can still be marker/Xhat/species indexed",
            "residual_if_fail": "b_clock; b_mass; b_alpha",
            "next_needed": "Rep(Q_obs) parent matter functor and constant superselection owner",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "QBA3141_4_source",
            "sector": "source/current coupling",
            "current_evidence": "1889/1890 give exact conditional label-forgetting/no-prefactor theorem but retain source prefactor countermodel",
            "current_status": "conditional_source_functor_not_parent_signed",
            "main_obstruction": "pre-action w_A and species-labelled kappa_A remain legal unless parent grammar forbids source-only weights",
            "residual_if_fail": "Delta_w_species; Delta_kappa_AB; non-Hilbert current; projected mass flux",
            "next_needed": "no-source-prefactor matter-normalization owner and label-forgotten source functor",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "QBA3141_5_boundary",
            "sector": "boundary/no-tail",
            "current_evidence": "890/946 keep boundary no-tail conditional; 3139 shows boundary exactness must become zero charge",
            "current_status": "conditional_boundary_exact_not_zero_charge",
            "main_obstruction": "measured edge/source tails and support shifts are not parent-forbidden",
            "residual_if_fail": "Delta_W_support; q_nonH; boundary charge",
            "next_needed": "boundary no-tail theorem for total B_total",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "audit_id": "QBA3141_6_total",
            "sector": "total",
            "current_evidence": "gluing theorem is exact, but at least six sector premises remain unsigned",
            "current_status": "not_claim_ready",
            "main_obstruction": "total sector-by-sector q-basic ownership not yet derived",
            "residual_if_fail": "finite residual vector remains active",
            "next_needed": "select smallest sector throat: EM T_Q/no-extra-F2 or source no-prefactor",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def obstruction_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "obstruction_id": "QBO3141_0_no_extra_F2",
            "fork": "EM/Poynting",
            "obstruction": "lambda_A F_Q^2 or f_X(Xhat)F_Q^2 is legal under ordinary covariance/U(1)",
            "why_this_is_nextable": "narrow operator-domain theorem could close b_alpha and EM Hilbert stress/Poynting readout",
            "status": "best_narrow_fork",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "QBO3141_1_TQ_norm",
            "fork": "EM/Poynting",
            "obstruction": "T_Q/gauge norm/level not parent-fixed",
            "why_this_is_nextable": "a level/index/monopole/Ward owner would turn EM coefficient from convention into parent data",
            "status": "best_narrow_fork_pair",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "QBO3141_2_source_prefactor",
            "fork": "source/Newton",
            "obstruction": "w_A S_A or kappa_A T_A relative source weights remain legal",
            "why_this_is_nextable": "no-source-prefactor theorem directly attacks calibrated Newtonian source coupling",
            "status": "best_source_fork",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "QBO3141_3_boundary_tail",
            "fork": "kernel/local-GR",
            "obstruction": "boundary-exact symplectic current may carry nonzero local edge/source charge",
            "why_this_is_nextable": "needed for the broad kernel-null proof but broader than EM/source forks",
            "status": "broad_route_required_later",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "QBO3141_4_projector_unification",
            "fork": "projector/cosmology",
            "obstruction": "topological P_D must be same object in local exterior and FLRW memory projection",
            "why_this_is_nextable": "essential for unification but less immediate for local GR/EM/source coupling",
            "status": "broad_route_required_later",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "QBD3141_0_gluing",
            "decision": "strong_qbasic_total_action_reduced_to_sector_qbasic_gluing",
            "reason": "finite sums of q-basic local n-forms are q-basic, so the broad action theorem is sector-local",
            "effect": "total action burden becomes a clear contract rather than a fog bank",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "QBD3141_1_claim",
            "decision": "do_not_claim_local_GR_Newton_EM",
            "reason": "geometry, projector, EM, matter, source, and boundary sector signatures remain unsigned",
            "effect": "3139/3140 remain conditional; residual vector stays active",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "QBD3141_2_next",
            "decision": "take_EM_Poynting_no_extra_F2_fork_next",
            "reason": "it is narrower than total action, directly attacks b_alpha, EM stress, Poynting readout, and source alpha coupling",
            "effect": "3142 should target parent T_Q/gauge norm plus no-independent-F2 as a q-basic EM sector theorem",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "QBGATE3141_0_gluing",
            "gate": "qbasic_sector_gluing_theorem",
            "status": "pass_exact_theorem",
            "claim_allowed": "false",
            "reason": "mathematical gluing theorem is exact but sector premises are unsigned",
            "generated_utc": now,
        },
        {
            "gate_id": "QBGATE3141_1_sector_ownership",
            "gate": "all_total_action_sectors_qbasic",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "six sector audits remain conditional/not parent-signed",
            "generated_utc": now,
        },
        {
            "gate_id": "QBGATE3141_2_EM",
            "gate": "EM_Maxwell_Poynting_balpha_claim",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": "T_Q norm, no-extra-F2, current owner, and readout/radiative guard remain unsigned",
            "generated_utc": now,
        },
        {
            "gate_id": "QBGATE3141_3_source",
            "gate": "calibrated_source_coupling_Newton_claim",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": "no-source-prefactor and label-forgotten source functor remain unsigned",
            "generated_utc": now,
        },
        {
            "gate_id": "QBGATE3141_4_local_GR",
            "gate": "local_GR_Newton_PPN_total_action_claim",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": "strong q-basic total action contract is written but not parent-owned",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    gluing: list[dict[str, str]],
    contract: list[dict[str, str]],
    audit: list[dict[str, str]],
    obstructions: list[dict[str, str]],
    decisions: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    exact_gluing = any(
        row["theorem_id"] == "QBG3141_1_finite_sum" and row["status"] == "exact_theorem"
        for row in gluing
    )
    contract_covers = {
        "geometry/EH",
        "projector/domain",
        "EM/Maxwell",
        "ordinary matter/clock constants",
        "source/current coupling",
        "boundary/no-tail",
    }.issubset({row["sector"] for row in contract})
    total_not_claim = any(
        row["audit_id"] == "QBA3141_6_total" and row["current_status"] == "not_claim_ready"
        for row in audit
    )
    next_em = any(
        row["decision_id"] == "QBD3141_2_next" and "EM_Poynting" in row["decision"]
        for row in decisions
    )
    obstructions_nonclaim = all(row["valid_for_claim"] == "false" for row in obstructions)
    gates_block = all(row["claim_allowed"] == "false" for row in gates)
    return [
        {
            "check_id": "V3141_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3141_1_gluing_theorem_exact",
            "status": "pass" if exact_gluing else "fail",
            "details": f"gluing_rows={len(gluing)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3141_2_contract_covers_core_sectors",
            "status": "pass" if contract_covers else "fail",
            "details": json.dumps([row["sector"] for row in contract], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3141_3_total_not_claim_ready",
            "status": "pass" if total_not_claim else "fail",
            "details": json.dumps({row["audit_id"]: row["current_status"] for row in audit}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3141_4_next_fork_selected",
            "status": "pass" if next_em else "fail",
            "details": "EM/Poynting no-extra-F2 fork selected",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3141_5_no_claim_leak",
            "status": "pass" if obstructions_nonclaim and gates_block else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    gluing = gluing_rows()
    contract = contract_rows()
    audit = audit_rows()
    obstructions = obstruction_rows()
    decisions = decision_rows()
    gates = gate_rows()
    validations = validation_rows(inputs, gluing, contract, audit, obstructions, decisions, gates)
    write_csv(INPUTS, inputs)
    write_csv(GLUING, gluing)
    write_csv(CONTRACT, contract)
    write_csv(AUDIT, audit)
    write_csv(OBSTRUCTIONS, obstructions)
    write_csv(DECISION, decisions)
    write_csv(GATE, gates)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
