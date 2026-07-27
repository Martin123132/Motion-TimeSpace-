from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"

INPUTS = OUT / "P8_Y5_R2FR_3139_INPUTS.csv"
IDENTITY = OUT / "P8_Y5_R2FR_3139_KERNEL_NULL_VARIATIONAL_IDENTITY.csv"
OWNERSHIP = OUT / "P8_Y5_R2FR_3139_PREMISE_OWNERSHIP_AUDIT.csv"
COUNTERMODELS = OUT / "P8_Y5_R2FR_3139_COUNTERMODEL_STRESS_TEST.csv"
DECISION = OUT / "P8_Y5_R2FR_3139_REDUCTION_DECISION.csv"
GATE = OUT / "P8_Y5_R2FR_3139_GATE.csv"
VALIDATION = OUT / "P8_Y5_R2FR_3139_VALIDATION.csv"


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
            "source_id": "SRC3139_0_3138_doc",
            "path": source_path("3138-Y5-R2FR-qobs-obse-repqobs-construction-under-AX1090.md"),
            "role": "typed Q_obs, Obs_e, Rep(Q_obs) construction and kernel-null next target",
        },
        {
            "source_id": "SRC3139_1_3138_certificate",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R2FR_3138_REP_QOBS_CERTIFICATE_MATRIX.csv"
            ),
            "role": "current certificate matrix for parent ownership failure",
        },
        {
            "source_id": "SRC3139_2_946_doc",
            "path": source_path(
                "946-Y5-R10-q-kernel-presymplectic-null-and-no-marker-certificate-or-cg-ba-bound-row.md"
            ),
            "role": "prior q-kernel presymplectic-null audit",
        },
        {
            "source_id": "SRC3139_3_946_certificate",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R10_946_KERNEL_CERTIFICATE_AUDIT.csv"
            ),
            "role": "prior kernel certificate rows",
        },
        {
            "source_id": "SRC3139_4_272_doc",
            "path": source_path("272-quotient-configuration-principle-from-topological-projector.md"),
            "role": "conditional presymplectic quotient route",
        },
        {
            "source_id": "SRC3139_5_711_doc",
            "path": source_path(
                "711-Y5-R10-derive-descent-clause-from-quotient-geometry-or-demote-scalar-zero-to-closure.md"
            ),
            "role": "quotient descent failure audit",
        },
        {
            "source_id": "SRC3139_6_711_audit",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R10_711_QUOTIENT_DESCENT_DERIVATION_AUDIT.csv"
            ),
            "role": "quotient descent derivation audit rows",
        },
        {
            "source_id": "SRC3139_7_410_doc",
            "path": source_path("410-quotient-matter-functor-theorem-attempt.md"),
            "role": "matter functor factorization theorem attempt and countermodels",
        },
        {
            "source_id": "SRC3139_8_623_coframe",
            "path": source_path(
                "source-intake/mts_residuals/P8_Y5_R10_623_COFRAME_FUNCTOR_THEOREM_ATTEMPT.csv"
            ),
            "role": "observed coframe functor theorem attempt",
        },
    ]
    for row in rows:
        row["exists"] = str(Path(row["path"]).exists()).lower()
        row["valid_for_claim"] = "false"
        row["generated_utc"] = now
    return rows


def identity_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "identity_id": "KNI3139_0_covariant_variation",
            "statement": "For a local parent Lagrangian n-form L, delta L = E_i delta Phi^i + d Theta(delta Phi).",
            "derivation": "standard covariant phase-space decomposition; defines Euler form E and presymplectic potential Theta",
            "status": "formal_identity_available",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "KNI3139_1_basic_action",
            "statement": "If L_parent = q^* Lbar(Q) + dB and v in ker(Dq), then i_v delta(q^* Lbar)=0.",
            "derivation": "chain rule gives delta(q^*Lbar)[v]=<Dq[v], delta Lbar/dQ>=0",
            "status": "proved_conditional_on_basic_action",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "KNI3139_2_theta_descent",
            "statement": "If Theta_parent(delta Phi)=q^* Thetabar(Dq delta Phi)+d beta(delta Phi), then Theta_parent(v)=d beta(v).",
            "derivation": "Dq[v]=0 removes the quotient potential term",
            "status": "proved_conditional_on_presymplectic_potential_descent",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "KNI3139_3_omega_boundary",
            "statement": "Under theta descent, omega_parent(v,delta)=d Xi_v(delta) up to equations of motion and commutator terms.",
            "derivation": "omega=delta Theta(v)-L_v Theta(delta)-Theta([delta,v]); substitute Theta(v)=d beta(v)",
            "status": "proved_conditional_boundary_exact",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "KNI3139_4_compact_zero",
            "statement": "If the local boundary pullback of Xi_v(delta) is zero, then Omega_Sigma(v,delta)=0.",
            "derivation": "Omega_Sigma=int_Sigma omega=int_boundarySigma Xi_v; compact/proper boundary silence kills the charge",
            "status": "proved_conditional_on_boundary_silence",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "KNI3139_5_matter_source_pairing",
            "statement": "If S_matter and J_source descend through q, then Lie_v S_matter=0 and <J_source,v>=0.",
            "derivation": "matter/source chain rule: Dq[v]=0 annihilates all quotient-owned readouts",
            "status": "proved_conditional_on_matter_and_source_descent",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "KNI3139_6_kernel_null_theorem",
            "statement": "If KNI3139_1 through KNI3139_5 are parent-owned, ker(Dq) is a gauge/null kernel for local readouts.",
            "derivation": "bulk action, presymplectic form, matter action, source pairing, and compact boundary charges all vanish on v",
            "status": "theorem_shape_proved_parent_premises_unsigned",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "identity_id": "KNI3139_7_obstruction_identity",
            "statement": "If any nonbasic term A(X)R, B_A(X)S_A, disformal frame, marker constant, or edge charge survives, omega(v,delta) need not vanish.",
            "derivation": "nonbasic terms contribute delta_X L or boundary charge outside Range(Dq)^*",
            "status": "counterterm_obstruction_retained",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def ownership_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "premise_id": "KNO3139_0_q_object",
            "premise": "q: Phi_parent -> Q_obs is a parent-owned quotient map",
            "needed_for": "defines vertical directions v in ker(Dq)",
            "current_evidence": "3138 writes typed q candidate; 711/946 keep parent ownership unsigned",
            "current_status": "candidate_written_not_parent_signed",
            "if_signed_effect": "vertical directions become mathematically meaningful",
            "residual_if_unsigned": "q_nonH; c_g/b_g",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "premise_id": "KNO3139_1_basic_action",
            "premise": "L_parent is basic over Q_obs up to an exact boundary primitive",
            "needed_for": "bulk Euler contraction i_v delta S=0",
            "current_evidence": "272 gives conditional topological route; 711 says action basicness not derived",
            "current_status": "conditional_identity_not_parent_signed",
            "if_signed_effect": "bulk fifth-force/source leakage from hidden representative directions is removed",
            "residual_if_unsigned": "A_EH(X); c_g/b_g; scalar/class residual",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "premise_id": "KNO3139_2_theta_descent",
            "premise": "presymplectic potential descends: Theta=q^*Thetabar+d beta",
            "needed_for": "Omega(v,delta) becomes a boundary integral",
            "current_evidence": "946 requested i_v Theta=dB_v; not parent signed",
            "current_status": "not_parent_signed",
            "if_signed_effect": "kernel-null becomes a boundary/no-edge problem instead of a bulk problem",
            "residual_if_unsigned": "hidden representative mode remains physical",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "premise_id": "KNO3139_3_boundary_silence",
            "premise": "local boundary pullback of Xi_v(delta) is zero or pure gauge",
            "needed_for": "int_boundary Xi_v=0",
            "current_evidence": "946 records proper compact support as conditional only; edge/source tails open",
            "current_status": "conditional_for_proper_variations_not_measured_edges",
            "if_signed_effect": "local compact systems have zero representative charge",
            "residual_if_unsigned": "Delta_W_support; q_nonH; boundary tail",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "premise_id": "KNO3139_4_matter_descent",
            "premise": "ordinary matter action is a functor over Rep(Q_obs)",
            "needed_for": "Lie_v S_matter=0 for clocks, masses, alpha, and rods",
            "current_evidence": "3136/3137 prove conditional chain; 410/711 keep parent derivation failed",
            "current_status": "conditional_theorem_not_parent_signed",
            "if_signed_effect": "b_clock, b_mass, and part of b_alpha vanish",
            "residual_if_unsigned": "b_clock; b_mass; b_alpha",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "premise_id": "KNO3139_5_source_descent",
            "premise": "source current lies in Range(Dq)^* and forgets species/marker labels",
            "needed_for": "<J_source,v>=0 and universal source coupling",
            "current_evidence": "946 source-cokernel theorem is exact conditional; source-label forgetting not signed",
            "current_status": "conditional_countermodel_retained",
            "if_signed_effect": "Delta_kappa_AB and source-normalization leakage vanish",
            "residual_if_unsigned": "Delta_kappa_AB; beta_source_alpha",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "premise_id": "KNO3139_6_no_frame_transfer",
            "premise": "no Weyl/disformal/readout transfer term survives outside Q_obs",
            "needed_for": "prevents Einstein-frame-style hiding of representative couplings",
            "current_evidence": "711/946 frame-transfer guards remain unowned; 3138 fallback rows retain c_g/b_g and b_dis",
            "current_status": "not_parent_signed",
            "if_signed_effect": "observed coframe is unique matter-visible frame",
            "residual_if_unsigned": "c_g/b_g; b_dis",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "premise_id": "KNO3139_7_total",
            "premise": "all ownership premises KNO3139_0 through KNO3139_6 are signed",
            "needed_for": "local GR/Newton readout kernel claim",
            "current_evidence": "formal identity proved, parent premises unsigned",
            "current_status": "not_claim_ready",
            "if_signed_effect": "hidden representative branch becomes quotient/gauge for local readouts",
            "residual_if_unsigned": "fallback residual vector remains active",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def countermodel_rows() -> list[dict[str, str]]:
    now = stamp()
    return [
        {
            "countermodel_id": "KNC3139_0_EH_prefactor",
            "surviving_term": "A(X) R[e_obs]",
            "why_it_breaks_kernel_null": "delta_X A contributes R delta X and creates a scalar/class force unless A is Q_obs-only or constant",
            "blocked_by": "basic action proof plus no-frame-transfer proof",
            "current_status": "legal_countermodel_retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "countermodel_id": "KNC3139_1_boundary_charge",
            "surviving_term": "int_boundary Q_v or Xi_v(delta)",
            "why_it_breaks_kernel_null": "Omega(v,delta) becomes a measured edge/source charge",
            "blocked_by": "boundary silence/no-tail theorem",
            "current_status": "legal_countermodel_retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "countermodel_id": "KNC3139_2_marker_matter",
            "surviving_term": "theta_A=theta_A(marker,X)",
            "why_it_breaks_kernel_null": "clock/mass/alpha constants vary along v even if e_obs is fixed",
            "blocked_by": "Rep(Q_obs) superselection ownership",
            "current_status": "legal_countermodel_retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "countermodel_id": "KNC3139_3_disformal_frame",
            "surviving_term": "g_matter = A(X)^2 g_obs + B(X) u_mu u_nu",
            "why_it_breaks_kernel_null": "matter readout changes while Q_obs coframe appears fixed",
            "blocked_by": "unique observed coframe matter functor",
            "current_status": "legal_countermodel_retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "countermodel_id": "KNC3139_4_species_source_label",
            "surviving_term": "F_src({T_A,A})=sum_A kappa_A T_A",
            "why_it_breaks_kernel_null": "source coupling keeps labels not erased by q",
            "blocked_by": "source functor label-forgetting theorem",
            "current_status": "legal_countermodel_retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "countermodel_id": "KNC3139_5_nonHilbert_current",
            "surviving_term": "J_nonH paired directly with representative direction",
            "why_it_breaks_kernel_null": "source current is outside Range(Dq)^*",
            "blocked_by": "source-cokernel ownership plus boundary no-tail",
            "current_status": "legal_countermodel_retained",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def decision_rows(ownership: list[dict[str, str]]) -> list[dict[str, str]]:
    now = stamp()
    all_signed = all(row["current_status"] == "parent_signed" for row in ownership if row["premise_id"] != "KNO3139_7_total")
    return [
        {
            "decision_id": "KND3139_0_formal_identity",
            "decision": "kernel_null_identity_reduced_to_basic_action_theta_descent_boundary_silence_matter_source_descent",
            "reason": "covariant phase-space chain rule turns v in ker(Dq) into a null direction if the listed premises are parent-owned",
            "effect": "this is a real derivation route, not a closure axiom",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "KND3139_1_claim_state",
            "decision": "do_not_claim_kernel_null",
            "reason": "parent ownership premises remain unsigned in current corpus",
            "effect": "local GR/Newton/PPN remains conditional; fallback residual vector remains active",
            "claim_allowed": str(all_signed).lower(),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "decision_id": "KND3139_2_next_target",
            "decision": "attack_presymplectic_potential_descent_or_unique_EM_stress_branch",
            "reason": "theta descent is the shortest route to kernel-null; EM branch is narrower and data-facing for Poynting/alpha",
            "effect": "3139 selects a fork rather than another broad missing ledger",
            "claim_allowed": "false",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def gate_rows(ownership: list[dict[str, str]]) -> list[dict[str, str]]:
    now = stamp()
    unsigned = [row["premise_id"] for row in ownership if row["current_status"] != "parent_signed"]
    return [
        {
            "gate_id": "KNG3139_0_identity",
            "gate": "formal_variational_identity",
            "status": "pass_conditional_theorem_shape",
            "claim_allowed": "false",
            "reason": "the identity is mathematical but does not sign its parent premises",
            "generated_utc": now,
        },
        {
            "gate_id": "KNG3139_1_parent_ownership",
            "gate": "all_kernel_null_premises_parent_signed",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": json.dumps(unsigned, ensure_ascii=False),
            "generated_utc": now,
        },
        {
            "gate_id": "KNG3139_2_countermodels",
            "gate": "all_kernel_countermodels_closed",
            "status": "fail_for_claim",
            "claim_allowed": "false",
            "reason": "EH prefactor, boundary charge, marker matter, disformal frame, species source label, and non-Hilbert current remain legal",
            "generated_utc": now,
        },
        {
            "gate_id": "KNG3139_3_local_GR",
            "gate": "local_GR_Newton_PPN_kernel_claim",
            "status": "not_claim_ready",
            "claim_allowed": "false",
            "reason": "kernel-null route reduced but not parent-owned",
            "generated_utc": now,
        },
    ]


def validation_rows(
    inputs: list[dict[str, str]],
    identities: list[dict[str, str]],
    ownership: list[dict[str, str]],
    countermodels: list[dict[str, str]],
    decisions: list[dict[str, str]],
    gates: list[dict[str, str]],
) -> list[dict[str, str]]:
    now = stamp()
    sources_exist = all(row["exists"] == "true" for row in inputs)
    identity_shape = {
        "KNI3139_0_covariant_variation",
        "KNI3139_1_basic_action",
        "KNI3139_2_theta_descent",
        "KNI3139_3_omega_boundary",
        "KNI3139_4_compact_zero",
        "KNI3139_5_matter_source_pairing",
        "KNI3139_6_kernel_null_theorem",
    }.issubset({row["identity_id"] for row in identities})
    total_not_claim = any(
        row["premise_id"] == "KNO3139_7_total" and row["current_status"] == "not_claim_ready"
        for row in ownership
    )
    countermodels_retained = len(countermodels) >= 6 and all(
        row["current_status"] == "legal_countermodel_retained" for row in countermodels
    )
    decisions_nonclaim = all(row["valid_for_claim"] == "false" for row in decisions)
    gates_block = all(row["claim_allowed"] == "false" for row in gates)
    return [
        {
            "check_id": "V3139_0_sources_exist",
            "status": "pass" if sources_exist else "fail",
            "details": json.dumps({row["source_id"]: row["exists"] for row in inputs}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3139_1_identity_shape_written",
            "status": "pass" if identity_shape else "fail",
            "details": f"identity_rows={len(identities)}",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3139_2_parent_premises_unsigned",
            "status": "pass" if total_not_claim else "fail",
            "details": json.dumps({row["premise_id"]: row["current_status"] for row in ownership}, ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3139_3_countermodels_retained",
            "status": "pass" if countermodels_retained else "fail",
            "details": json.dumps([row["countermodel_id"] for row in countermodels], ensure_ascii=False),
            "valid_for_claim": "false",
            "generated_utc": now,
        },
        {
            "check_id": "V3139_4_no_claim_leak",
            "status": "pass" if decisions_nonclaim and gates_block else "fail",
            "details": "",
            "valid_for_claim": "false",
            "generated_utc": now,
        },
    ]


def main() -> None:
    inputs = input_rows()
    identities = identity_rows()
    ownership = ownership_rows()
    countermodels = countermodel_rows()
    decisions = decision_rows(ownership)
    gates = gate_rows(ownership)
    validations = validation_rows(inputs, identities, ownership, countermodels, decisions, gates)
    write_csv(INPUTS, inputs)
    write_csv(IDENTITY, identities)
    write_csv(OWNERSHIP, ownership)
    write_csv(COUNTERMODELS, countermodels)
    write_csv(DECISION, decisions)
    write_csv(GATE, gates)
    write_csv(VALIDATION, validations)


if __name__ == "__main__":
    main()
