from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3140_INPUTS.csv"
THEOREM = OUT / "P8_Y5_R2FR_3140_THETA_DESCENT_THEOREM.csv"
PREMISE_COLLAPSE = OUT / "P8_Y5_R2FR_3140_PREMISE_COLLAPSE_MATRIX.csv"
OBSTRUCTIONS = OUT / "P8_Y5_R2FR_3140_THETA_OBSTRUCTION_LEDGER.csv"
DECISION = OUT / "P8_Y5_R2FR_3140_DECISION.csv"
GATE = OUT / "P8_Y5_R2FR_3140_GATE.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3140_VALIDATION.csv"


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
            "source_id": "SRC3140_0_3139_doc",
            "path": source_path("3139-Y5-R2FR-kernel-null-variational-identity-under-AX1090.md"),
            "role": "sets theta-descent as next kernel-null target",
        },
        {
            "source_id": "SRC3140_1_3139_theorem",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R2FR_3139_KERNEL_NULL_VARIATIONAL_IDENTITY.csv"
            ),
            "role": "kernel-null variational identity",
        },
        {
            "source_id": "SRC3140_2_3139_premises",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R2FR_3139_PREMISE_OWNERSHIP_AUDIT.csv"
            ),
            "role": "basic action and theta descent listed as separate unsigned premises",
        },
        {
            "source_id": "SRC3140_3_252_doc",
            "path": source_path("252-topological-projector-parent-action-skeleton.md"),
            "role": "topological parent action skeleton with exact/boundary projector sector",
        },
        {
            "source_id": "SRC3140_4_272_doc",
            "path": source_path("272-quotient-configuration-principle-from-topological-projector.md"),
            "role": "conditional q-quotient from presymplectic null/topological exactness",
        },
        {
            "source_id": "SRC3140_5_407_doc",
            "path": source_path("407-primitive-relational-quotient-action-sketch.md"),
            "role": "primitive relational quotient action sketch",
        },
        {
            "source_id": "SRC3140_6_711_doc",
            "path": source_path(
                "711-Y5-R10-derive-descent-clause-from-quotient-geometry-or-demote-scalar-zero-to-closure.md"
            ),
            "role": "prior quotient descent derivation failure",
        },
        {
            "source_id": "SRC3140_7_946_certificate",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R10_946_KERNEL_CERTIFICATE_AUDIT.csv"
            ),
            "role": "prior theta/boundary certificate failure",
        },
        {
            "source_id": "SRC3140_8_890_boundary",
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


def theorem_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "theorem_id": "TDT3140_0_strong_qbasic_lagrangian",
            "statement": "Assume L_parent(Phi)=q^*Lbar(Q_obs)+dB(Phi) as local n-forms.",
            "derivation": "this is the strong q-basic Lagrangian premise, stronger than Euler-level action equality",
            "status": "premise_required_not_parent_signed",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "TDT3140_1_variation_chain_rule",
            "statement": "delta L_parent=q^*(Ebar_A Dq^A[delta Phi]+d Thetabar(Dq delta Phi))+d delta B.",
            "derivation": "field-space variation commutes with quotient pullback and horizontal d",
            "status": "formal_pass_if_TDT3140_0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "TDT3140_2_potential_choice",
            "statement": "One may choose Theta_parent=q^*Thetabar(Dq delta Phi)+delta B+dY.",
            "derivation": "presymplectic potential is defined up to horizontal exact dY; compare delta L decompositions",
            "status": "derived_modulo_potential_ambiguity_if_TDT3140_0",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "TDT3140_3_theta_descent",
            "statement": "Theta_parent-q^*Thetabar(Dq delta Phi)=delta B+dY, so theta descent follows from strong q-basic action.",
            "derivation": "the difference is vertical variation of the boundary primitive plus a potential ambiguity",
            "status": "conditional_theorem_proved",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "TDT3140_4_vertical_kernel",
            "statement": "For v in ker(Dq), Theta_parent(v)=delta_v B+dY(v).",
            "derivation": "the q^*Thetabar term vanishes because Dq[v]=0",
            "status": "conditional_theorem_proved",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "TDT3140_5_symplectic_current",
            "statement": "omega_parent(v,delta)=d Xi_v(delta) plus boundary-primitive variation terms.",
            "derivation": "delta Theta_parent(v)-delta_v Theta_parent(delta) is horizontal exact after quotient term vanishes",
            "status": "conditional_boundary_exact",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "TDT3140_6_kernel_reduction",
            "statement": "Therefore KNO3139_2 theta descent is not independent if KNO3139_1 is upgraded to strong q-basic Lagrangian descent with owned B.",
            "derivation": "theta descent is a consequence of local-form Lagrangian descent, not a separate axiom",
            "status": "premise_collapsed_conditionally",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "theorem_id": "TDT3140_7_no_claim",
            "statement": "The current corpus has not parent-signed strong q-basic Lagrangian descent for the full Q_obs object.",
            "derivation": "252/272/407 provide skeletons and conditional routes; 711/946 retain failures",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def premise_collapse_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "collapse_id": "TDC3140_0_basic_action",
            "old_premise": "KNO3139_1_basic_action",
            "new_form": "strong q-basic local n-form: L_parent=q^*Lbar+dB",
            "relation": "strengthened",
            "effect": "bulk Euler contraction and theta descent become linked",
            "current_status": "not_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "collapse_id": "TDC3140_1_theta_descent",
            "old_premise": "KNO3139_2_theta_descent",
            "new_form": "derived from TDC3140_0 up to delta B+dY",
            "relation": "collapsed_if_strong_qbasic_signed",
            "effect": "removes one independent miracle from the local-GR route",
            "current_status": "conditional_theorem_not_parent_signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "collapse_id": "TDC3140_2_boundary_silence",
            "old_premise": "KNO3139_3_boundary_silence",
            "new_form": "int_boundarySigma Xi_v(delta)=0, including delta_v B and dY ambiguity",
            "relation": "not_collapsed",
            "effect": "still required to turn boundary-exactness into zero charge",
            "current_status": "still_open",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "collapse_id": "TDC3140_3_matter_source",
            "old_premise": "KNO3139_4_to_5_matter_source_descent",
            "new_form": "still independent unless total parent action includes ordinary matter and source functors over Q_obs",
            "relation": "not_collapsed",
            "effect": "clocks, masses, alpha, and source coupling still need Rep(Q_obs)/Range(Dq)^* ownership",
            "current_status": "still_open",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "collapse_id": "TDC3140_4_no_frame_transfer",
            "old_premise": "KNO3139_6_no_frame_transfer",
            "new_form": "forbidden nonbasic frame terms A(X)R or disformal matter frame",
            "relation": "guard_required_for_TDC3140_0",
            "effect": "frame leaks are now obstructions to strong q-basicness",
            "current_status": "still_open",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "collapse_id": "TDC3140_5_total",
            "old_premise": "KNO3139_7_total",
            "new_form": "q_object + strong_qbasic_action + boundary_silence + matter/source descent + no-frame-transfer",
            "relation": "reduced_premise_count",
            "effect": "kernel-null proof is simpler but still not claim-ready",
            "current_status": "not_claim_ready",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def obstruction_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "obstruction_id": "TDO3140_0_euler_only_descent",
            "obstruction": "Euler equations descend but L_parent is not equal to q^*Lbar+dB as a local n-form.",
            "damage": "bulk equations may look quotient-owned while theta and charges retain hidden representative dependence",
            "required_fix": "prove local-form q-basicness, not just on-shell equation matching",
            "current_status": "legal_obstruction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "TDO3140_1_nonbasic_EH_prefactor",
            "obstruction": "A(X) R[e_obs] or F(sigma)R survives.",
            "damage": "delta_X L_parent is not a boundary term; theta descent fails before boundary silence",
            "required_fix": "show A,F are Q_obs-only constants or forbidden by parent action",
            "current_status": "legal_obstruction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "TDO3140_2_boundary_primitive_charge",
            "obstruction": "B or Y carries a nonzero compact boundary charge.",
            "damage": "theta descent is boundary-exact but not charge-zero, so Omega(v,delta) need not vanish",
            "required_fix": "boundary no-tail theorem for Xi_v(delta)",
            "current_status": "legal_obstruction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "TDO3140_3_Hodge_projector",
            "obstruction": "projector is metric/Hodge/least-energy rather than topological.",
            "damage": "delta_g P_D contributes bulk stress and nonbasic theta terms",
            "required_fix": "metric-independent relative-chain projector",
            "current_status": "legal_obstruction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "TDO3140_4_matter_not_in_Lbar",
            "obstruction": "ordinary matter is appended after quotient reduction instead of included in Lbar(Q_obs,Rep(Q_obs)).",
            "damage": "theta descent for geometry does not imply clock/mass/source descent",
            "required_fix": "total action q-basicness including matter and source readouts",
            "current_status": "legal_obstruction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "obstruction_id": "TDO3140_5_readout_EFT",
            "obstruction": "Q_obs is only a readout map, not the variational parent quotient.",
            "damage": "observables can be postprocessed while hidden variables remain dynamical",
            "required_fix": "derive q as reduced variational configuration space",
            "current_status": "legal_obstruction",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "decision_id": "TDD3140_0_theta_descent",
            "decision": "theta_descent_derived_conditionally_from_strong_qbasic_lagrangian",
            "reason": "variation of L_parent=q^*Lbar+dB gives Theta_parent=q^*Thetabar+delta B+dY",
            "effect": "KNO3139_2 is no longer an independent closure axiom if KNO3139_1 is strengthened and signed",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "TDD3140_1_parent_claim",
            "decision": "do_not_claim_kernel_null_or_local_GR",
            "reason": "strong q-basic total action and boundary silence are not parent-owned in current corpus",
            "effect": "local GR/Newton/PPN remains conditional, but the proof burden is narrower",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "TDD3140_2_next",
            "decision": "attack_strong_qbasic_total_action_or_switch_to_EM_F2",
            "reason": "the broad route now needs L_parent=q^*Lbar+dB for total action; the narrow route attacks EM stress/source directly",
            "effect": "next step should either prove total action basicness or take the EM/Poynting fork",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "gate_id": "TDG3140_0_theta_derivation",
            "gate": "theta_descent_from_strong_qbasic_action",
            "status": "pass_conditional_theorem",
            "claim_allowed": "false",
            "reason": "formal variational chain rule closes theta descent if strong q-basic Lagrangian descent is owned",
            "generated_utc": now,
        },
        {
            "gate_id": "TDG3140_1_parent_basic_action",
            "gate": "strong_qbasic_total_action_parent_signed",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "current action/projector sources are skeleton or conditional, not full Q_obs parent ownership",
            "generated_utc": now,
        },
        {
            "gate_id": "TDG3140_2_boundary_charge",
            "gate": "boundary_exact_to_zero_charge",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "theta descent gives boundary-exactness, not zero charge; no-tail remains required",
            "generated_utc": now,
        },
        {
            "gate_id": "TDG3140_3_local_GR",
            "gate": "local_GR_Newton_PPN_kernel_claim",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": "premise count reduced but parent action/matter/source ownership remains unsigned",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    theorem: list[dict[str, str]],
    collapse: list[dict[str, str]],
    obstructions: list[dict[str, str]],
    decisions: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    theta_closed = any(
        row["theorem_id"] == "TDT3140_3_theta_descent" and row["status"] == "conditional_theorem_proved"
        for row in theorem
    )
    premise_collapsed = any(
        row["collapse_id"] == "TDC3140_1_theta_descent"
        and row["relation"] == "collapsed_if_strong_qbasic_signed"
        for row in collapse
    )
    obstructions_retained = len(obstructions) >= 6 and all(
        row["current_status"] == "legal_obstruction" for row in obstructions
    )
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decisions)
    gates_block_claim = all(row["claim_allowed"] == "false" for row in gates)
    return [
        {
            "check_id": "V3140_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3140_1_theta_descent_conditional_theorem",
            "status": "pass" if theta_closed else "fail",
            "details": f"theorem_rows={len(theorem)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3140_2_premise_collapse_recorded",
            "status": "pass" if premise_collapsed else "fail",
            "details": json.dumps({row["collapse_id"]: row["relation"] for row in collapse}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3140_3_obstructions_retained",
            "status": "pass" if obstructions_retained else "fail",
            "details": json.dumps([row["obstruction_id"] for row in obstructions], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3140_4_no_claim_leak",
            "status": "pass" if decisions_nonclaim and gates_block_claim else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    theorem = theorem_rows()
    collapse = premise_collapse_rows()
    obstructions = obstruction_rows()
    decisions = decision_rows()
    gates = gate_rows()
    validations = validation_rows(inputs, theorem, collapse, obstructions, decisions, gates)
    write_csv(INPUTS, inputs)
    write_csv(THEOREM, theorem)
    write_csv(PREMISE_COLLAPSE, collapse)
    write_csv(OBSTRUCTIONS, obstructions)
    write_csv(DECISION, decisions)
    write_csv(GATE, gates)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
