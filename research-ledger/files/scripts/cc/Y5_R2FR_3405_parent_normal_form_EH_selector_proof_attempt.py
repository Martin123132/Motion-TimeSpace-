from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3405-Y5-R2FR-parent-normal-form-EH-selector-proof-attempt-under-AX1090.md"

SOURCES = {
    "doc_3404": ROOT / "3404-Y5-R2FR-source-calibrated-EH-parent-ownership-audit-under-AX1090.md",
    "doc_3403": ROOT / "3403-Y5-R2FR-PiM-boundary-readout-operator-beta-residual-fill-under-AX1090.md",
    "doc_3402": ROOT / "3402-Y5-R2FR-v-second-order-source-square-theorem-attempt-under-AX1090.md",
    "doc_3400": ROOT / "3400-Y5-R2FR-first-order-source-coupling-parent-signature-pack-under-AX1090.md",
    "doc_3340": ROOT / "3340-Y5-R2FR-parent-Hilbert-source-clause-or-finite-residual-vector-under-AX1090.md",
    "own_3404": OUT / "P8_Y5_R2FR_3404_PARENT_OWNERSHIP_CLAUSES.csv",
    "thm_3404": OUT / "P8_Y5_R2FR_3404_CONDITIONAL_EH_OWNERSHIP_THEOREM.csv",
    "obs_3404": OUT / "P8_Y5_R2FR_3404_EH_IMPORT_OBSTRUCTION_THEOREM.csv",
    "ops_3404": OUT / "P8_Y5_R2FR_3404_NONEH_OPERATOR_SURVIVAL_LAW.csv",
    "next_3404": OUT / "P8_Y5_R2FR_3404_NEXT_TARGET.csv",
    "red_2924": OUT / "P8_Y5_R2FR_2924_MTS_TO_EH_REDUCTION_CONTRACT.csv",
    "dominance_3062": OUT / "P8_Y5_R2FR_3062_EH_OPERATOR_DOMINANCE_ATTEMPT.csv",
    "dominance_3086": OUT / "P8_Y5_R2FR_3086_EH_DOMINANCE_THEOREM_ATTEMPT.csv",
    "sgk_3241": OUT / "P8_Y5_R2FR_3241_EH_SGK_IDENTITY_DERIVATION.csv",
    "induced_3324": OUT / "P8_Y5_R2FR_3324_INDUCED_EH_ATTEMPT.csv",
    "newton_3359": OUT / "P8_Y5_R2FR_3359_EH_NEWTON_RECOVERY_CONDITIONS.csv",
    "noneh_3368": OUT / "P8_Y5_R2FR_3368_NONEH_OPERATOR_CLASSIFICATION.csv",
    "r11_beta": OUT / "P8_Y5_R11_BETA_COMPONENT_VECTOR.csv",
    "local_eh_r11": OUT / "P8_LOCAL_EH_R11_OPERATOR_AUDIT.csv",
    "source_square_3402": OUT / "P8_Y5_R2FR_3402_SOURCE_SQUARE_THEOREM.csv",
    "kappav_3403": OUT / "P8_Y5_R2FR_3403_KAPPAV_REDUCED_ENVELOPE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3405_SOURCE_REGISTER.csv",
    "normal_form_hypotheses": OUT / "P8_Y5_R2FR_3405_PARENT_NORMAL_FORM_HYPOTHESES.csv",
    "eh_selector_proof": OUT / "P8_Y5_R2FR_3405_EH_SELECTOR_PROOF_ATTEMPT.csv",
    "spin2_bootstrap": OUT / "P8_Y5_R2FR_3405_SPIN2_BOOTSTRAP_ROUTE.csv",
    "derivative_order_bound": OUT / "P8_Y5_R2FR_3405_DERIVATIVE_ORDER_BOUND_LAW.csv",
    "operator_triage": OUT / "P8_Y5_R2FR_3405_NONEH_OPERATOR_TRIAGE.csv",
    "selector_result": OUT / "P8_Y5_R2FR_3405_SELECTOR_RESULT.csv",
    "local_gr_impact": OUT / "P8_Y5_R2FR_3405_LOCAL_GR_IMPACT.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3405_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3405_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3405_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3405_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3405_VALIDATION.csv",
}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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
        return ""
    fields = list(rows[0].keys())
    clean = lambda value: str(value).replace("\n", " ").replace("|", "/")
    lines = [
        "| " + " | ".join(fields) + " |",
        "| " + " | ".join("---" for _ in fields) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(clean(row.get(field, "")) for field in fields) + " |")
    return "\n".join(lines)


def source_register() -> list[dict[str, Any]]:
    roles = {
        "own_3404": "parent ownership contract that 3405 tries to compress into a selector theorem",
        "thm_3404": "conditional EH ownership chain feeding the selector proof",
        "obs_3404": "countermodels that prove generic covariance is insufficient",
        "red_2924": "older MTS-to-EH reduction clauses and blockers",
        "dominance_3062": "EH operator dominance attempt and unresolved operator/source gates",
        "dominance_3086": "residual-sector zero theorem shape",
        "sgk_3241": "q_loc/EH residual identity bridge",
        "induced_3324": "induced EH route and G-circularity warning",
        "newton_3359": "EH Newton recovery conditions",
        "noneh_3368": "non-EH operator classification",
        "r11_beta": "R11 beta operator family vector",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles.get(key, "supporting checkpoint/source evidence"),
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def normal_form_hypotheses() -> list[dict[str, Any]]:
    return [
        {
            "hypothesis_id": "PNF3405_0_q_basic_observable",
            "statement": "The local observable geometry is one q-basic metric/coframe, not a representative-dependent mixture.",
            "math_form": "Lie_v g_obs=0 for v in ker(Dq); S_matter and PPN readout use g_obs through O(U^2).",
            "why_less_smuggly": "This is an MTS quotient statement, not a GR premise.",
            "current_status": "PARTIAL_NOT_SIGNED_THROUGH_OU2",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "PNF3405_1_mode_rank",
            "statement": "The compact local vacuum quotient has only the massless spin-2 observed metric as a long-range propagating mode.",
            "math_form": "rank phase space = 2 transverse-traceless modes; no scalar, vector, torsion, nonmetricity, memory, domain or bulk-X long-range charge.",
            "why_less_smuggly": "This replaces 'assume EH' with a measurable/derivable mode-count target.",
            "current_status": "NOT_PARENT_SIGNED_R11_FAMILIES_RETAINED",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "PNF3405_2_two_derivative_normal_form",
            "statement": "The leading local quotient action at the tested weak-field order is a two-derivative normal form.",
            "math_form": "L_eff=L_0+L_2+dB+L_{>=4}; L_{>=4} either zero or bounded by (ell_*/L)^2.",
            "why_less_smuggly": "This gives an exact EH route if true and a quantitative residual route if false.",
            "current_status": "NEW_3405_SELECTOR_FORMULATION_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "PNF3405_3_universal_Hilbert_source",
            "statement": "The spin-2 mode couples to one descended Hilbert stress tensor before calibration.",
            "math_form": "delta S_matter/delta g_obs -> T_total; h_mn T_total^mn is the universal linear coupling.",
            "why_less_smuggly": "This imports the self-coupling consistency theorem only after MTS owns the source.",
            "current_status": "STRONG_CONDITIONAL_FROM_3340_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "PNF3405_4_vertical_kernel_silence",
            "statement": "Vertical variables either are gauge/constraints or have a double-zero/gapped coupling to the local source/readout.",
            "math_form": "C_X(Phi0)=0, DC_X(Phi0)=0, M_X^2>0, and no source charge; otherwise keep residual R_X.",
            "why_less_smuggly": "It blocks hidden scalar/vector/domain hair without pretending those sectors do not exist.",
            "current_status": "OPEN_FOR_ACTUAL_R11_ROWS",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "PNF3405_5_connection_normal_form",
            "statement": "Independent connection variables are algebraic/gauge in the local branch or reduce to Levi-Civita.",
            "math_form": "delta_Gamma S gives nabla^Gamma g_obs=0 plus projective gauge; torsion/nonmetricity source/readout residuals vanish or are bounded.",
            "why_less_smuggly": "It targets the connection leak directly instead of hiding it inside EH notation.",
            "current_status": "NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "PNF3405_6_fixed_boundary_topology",
            "statement": "Boundary/reference/projector terms are fixed before readout and are exact, topological, or source-blind.",
            "math_form": "delta_g B_ref=0; B_zero_flux=0; Delta_symp=0; no post-readout subtraction.",
            "why_less_smuggly": "It prevents boundary bookkeeping from acting as a hidden mass/PPN fit.",
            "current_status": "CONDITIONAL_STOKES_ROUTE_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "hypothesis_id": "PNF3405_7_common_branch_Gref",
            "statement": "The same branch constant G_ref normalizes field equation, Hilbert/Pi_M source, and readout.",
            "math_form": "kappa_MTS=8*pi*G_ref/c^4; mu=G_ref M_H[Pi_M J_H]; U=mu/r.",
            "why_less_smuggly": "It allows GR-style calibration of G while forbidding split-G closure tricks.",
            "current_status": "FIRST_ORDER_STAGED_SECOND_ORDER_OPEN",
            "valid_for_claim": False,
        },
    ]


def eh_selector_proof() -> list[dict[str, Any]]:
    return [
        {
            "step_id": "SEL3405_0_project_parent_to_quotient",
            "claim": "Parent variation descends to an observed quotient action plus vertical residuals.",
            "derivation": "For q-basic variations delta g_obs=Dq delta Phi, delta S_parent=<E_obs,delta g_obs>+<E_vert,delta Phi_vert>. PNF3405_0 and PNF3405_4 set E_vert=0 or put it into R_vert.",
            "result": "selection can be done on S_eff[g_obs] with explicit residuals instead of on the full uncontrolled parent",
            "status": "DERIVED_CONDITIONAL",
            "valid_for_claim": False,
        },
        {
            "step_id": "SEL3405_1_two_derivative_basis",
            "claim": "The only local diffeomorphism-invariant scalar-density basis at derivative order <=2 is sqrt(-g)(C0+C1 R) plus a boundary term.",
            "derivation": "At zero derivatives the scalar is constant. At two derivatives, contractions of second derivatives of g reduce, up to a divergence, to the Ricci scalar; connection-first form gives the same normal form after imposing metric compatibility.",
            "result": "S_eff^{<=2}=int sqrt(-g)(C0+C1 R)+dB",
            "status": "DERIVED_MATH_NORMAL_FORM",
            "valid_for_claim": False,
        },
        {
            "step_id": "SEL3405_2_field_equation",
            "claim": "Variation of the two-derivative normal form gives EH field equations.",
            "derivation": "delta int sqrt(-g)R gives G_mn plus boundary; delta int sqrt(-g)C0 gives Lambda g_mn; fixed boundary/reference terms do not alter local equations.",
            "result": "E_mn=C1 G_mn - (C0/2) g_mn",
            "status": "DERIVED_MATH_NORMAL_FORM",
            "valid_for_claim": False,
        },
        {
            "step_id": "SEL3405_3_source_coupling",
            "claim": "Universal Hilbert coupling fixes the right-hand source without source-only weights.",
            "derivation": "PNF3405_3 makes h_mn couple to T_total^mn from the same descended action; Ward identity enforces common conservation with the left-hand tensor.",
            "result": "G_mn+Lambda g_mn=kappa_* T_total_mn plus explicit residuals",
            "status": "EXACT_IF_HILBERT_SOURCE_SIGNED",
            "valid_for_claim": False,
        },
        {
            "step_id": "SEL3405_4_spin2_bootstrap_equivalence",
            "claim": "The same result follows from massless spin-2 consistency: a two-derivative spin-2 field universally coupled to its Hilbert stress bootstraps to EH.",
            "derivation": "Linear gauge invariance requires conserved source coupling; iterating the spin-2 field's own stress-energy self-coupling gives the nonlinear Einstein tensor completion.",
            "result": "EH is selected by mode-count plus universal source, not by aesthetic preference",
            "status": "DERIVED_STANDARD_SELECTOR_IF_MODE_RANK_SIGNED",
            "valid_for_claim": False,
        },
        {
            "step_id": "SEL3405_5_nonEH_survival",
            "claim": "Every non-EH operator survives unless it is outside the two-derivative normal form, topological/boundary, vertical-silent, or quantitatively suppressed.",
            "derivation": "R^2, f(R), Weyl^2, scalar/vector, torsion/nonmetricity, nonlocal memory, domain/projector and bulk-X terms are not eliminated by covariance alone.",
            "result": "3405 gives an exact selector only if PNF3405_1..6 are parent-signed; otherwise use residual bound law",
            "status": "OBSTRUCTION_DERIVED",
            "valid_for_claim": False,
        },
    ]


def spin2_bootstrap() -> list[dict[str, Any]]:
    return [
        {
            "route_id": "SPIN3405_0_linear_mode",
            "requirement": "linearized observed geometry has only a massless spin-2 mode",
            "test_or_derivation": "show the parent Hessian around the local vacuum has TT metric kernel only; scalar/vector/connection/domain kernels are constrained or gapped",
            "if_passes": "linear kinetic term is Fierz-Pauli up to normalization",
            "current_status": "NOT_YET_EXTRACTED_FROM_PARENT_HESSIAN",
            "valid_for_claim": False,
        },
        {
            "route_id": "SPIN3405_1_gauge_identity",
            "requirement": "linearized gauge symmetry is the q-basic diffeomorphism symmetry",
            "test_or_derivation": "derive delta h_mn=partial_m xi_n+partial_n xi_m from quotient redundancy rather than assuming GR diffeomorphism",
            "if_passes": "source must be conserved and coupled universally",
            "current_status": "PLAUSIBLE_FROM_Q_BASIC_BRANCH_NOT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "route_id": "SPIN3405_2_self_coupling",
            "requirement": "the spin-2 field couples to the total Hilbert stress including its own stress",
            "test_or_derivation": "use the 3340 Hilbert source clause and parent Noether identity to forbid separate source weights",
            "if_passes": "nonlinear completion is EH at two derivatives",
            "current_status": "CONDITIONAL_FROM_3340",
            "valid_for_claim": False,
        },
        {
            "route_id": "SPIN3405_3_MTS_gain",
            "requirement": "MTS owns the mode-rank and source-universality premises",
            "test_or_derivation": "prove vertical kernel silence and common Hilbert source from parent action",
            "if_passes": "EH selector becomes an MTS theorem, not an imported GR axiom",
            "current_status": "THIS_IS_NOW_THE_CENTRAL_TARGET",
            "valid_for_claim": False,
        },
    ]


def derivative_order_bound() -> list[dict[str, Any]]:
    return [
        {
            "bound_id": "DOB3405_0_four_derivative_metric",
            "operator_class": "R2/fR/Ricci2/Weyl2",
            "normal_form_status": "outside exact two-derivative selector",
            "residual_law": "|E_4|/|E_EH| <= C_4*(ell_4/L_local)^2 after source/readout projection",
            "needed_inputs": "C_4 sign/norm; ell_4 or mass scale; weak-field projection to beta/gamma/R10; boundary status",
            "claim_status": "BOUND_ROUTE_IF_NOT_ZERO",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DOB3405_1_extra_fields",
            "operator_class": "scalar/vector/bulk-X/memory/domain",
            "normal_form_status": "outside metric-only spin-2 selector unless constrained/gapped",
            "residual_law": "|E_X|/|E_EH| <= |Q_X|*|K_X|/(M_X^2 L_local^2) + contact/readout terms",
            "needed_inputs": "Q_X,K_X,M_X^2, source charge, local profile, PPN/fifth-force projection",
            "claim_status": "BOUND_ROUTE_IF_DOUBLE_ZERO_FAILS",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DOB3405_2_connection",
            "operator_class": "torsion/nonmetricity/metric-affine",
            "normal_form_status": "outside Levi-Civita normal form unless algebraic/gauge",
            "residual_law": "|E_conn|/|E_EH| <= C_T|T|/L_local + C_Q|Q|/L_local plus clock/light/source maps",
            "needed_inputs": "connection field equations, hypermomentum/source coupling, clock/light/PPN projection",
            "claim_status": "BOUND_ROUTE_IF_LC_PROOF_FAILS",
            "valid_for_claim": False,
        },
        {
            "bound_id": "DOB3405_3_boundary_projector",
            "operator_class": "boundary/reference/projector/domain stress",
            "normal_form_status": "silent only if exact/topological/fixed before readout",
            "residual_law": "|E_boundary|/|E_EH| <= |B_zero_flux|+|Delta_symp|+|projector_stress_beta_equiv|",
            "needed_inputs": "fixed annulus, reference variation, projector stress, source-worldtube matching",
            "claim_status": "BOUND_ROUTE_IF_STOKES_ZERO_FAILS",
            "valid_for_claim": False,
        },
    ]


def operator_triage() -> list[dict[str, Any]]:
    r11_rows = read_csv(SOURCES["r11_beta"])
    triage = []
    for row in r11_rows:
        family = row["operator_family"]
        if family in {"R2_fR_scalar_mode", "Ricci_Weyl_squared"}:
            selector_bucket = "killed by exact two-derivative normal form; otherwise four-derivative bound"
        elif family in {"torsion_nonmetricity"}:
            selector_bucket = "killed by Levi-Civita connection normal form; otherwise connection residual bound"
        elif family in {"scalar_tensor_class_metric", "vector_preferred_frame", "bulk_X_force_law", "nonlocal_memory_kernel"}:
            selector_bucket = "killed by mode-rank/vertical-kernel silence; otherwise extra-field residual bound"
        elif family in {"boundary_topological_terms", "projector_domain_stress"}:
            selector_bucket = "killed by fixed topological/boundary/projector silence; otherwise boundary/projector bound"
        else:
            selector_bucket = "requires same-source/readout ownership or q_loc vector split"
        triage.append({
            "operator_id": row["component_id"],
            "operator_family": family,
            "selector_bucket": selector_bucket,
            "current_evidence": row["current_evidence"],
            "current_status": row["status"],
            "score_ready": False,
            "valid_for_claim": False,
        })
    return triage


def selector_result() -> list[dict[str, Any]]:
    return [
        {
            "result_id": "RES3405_0_exact_selector",
            "statement": "PNF3405_0 through PNF3405_7 imply the local two-derivative quotient field equation is EH with one Hilbert source and one G_ref.",
            "mathematical_result": "S_eff=int sqrt(-g_obs)(C0+C1 R[g_obs])+S_matter[g_obs]+dB+R_silent; variation gives G_mn+Lambda g_mn=kappa_*T_mn",
            "what_is_new": "3405 replaces the loose 'assume EH/Lovelock' gap with a parent normal-form + spin-2 mode-count contract.",
            "claim_status": "EXACT_CONDITIONAL_SELECTOR_NOT_PARENT_SIGNED",
            "valid_for_claim": False,
        },
        {
            "result_id": "RES3405_1_partial_derivation",
            "statement": "The two-derivative basis calculation itself is closed: if the parent has reduced to a two-derivative metric action, EH follows.",
            "mathematical_result": "L_0+L_2+dB = sqrt(-g)(C0+C1 R)+dB",
            "what_is_new": "The remaining derivation target is no longer 'derive all of GR'; it is 'derive two-derivative massless spin-2 quotient normal form'.",
            "claim_status": "DERIVED_MATH_NOT_MTS_SIGNATURE",
            "valid_for_claim": False,
        },
        {
            "result_id": "RES3405_2_fallback_bound",
            "statement": "If PNF3405_1 or PNF3405_2 fails, MTS must carry non-EH residual bounds, not claim local GR.",
            "mathematical_result": "Delta_PPN <= Delta_EH_selector_abs + sum_i |E_i/E_EH|_projection with no cancellation credit",
            "what_is_new": "Non-EH rows now have a single normal-form residual law instead of scattered placeholders.",
            "claim_status": "BOUND_CONTRACT_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
    ]


def local_gr_impact() -> list[dict[str, Any]]:
    return [
        {
            "impact_id": "IM3405_0_Newton",
            "quantity": "Delta_Newton_v_coupled",
            "if_selector_signed": "zero after common G_ref and Hilbert/PiM source lock",
            "remaining_if_not_signed": "source kappa/readout/PiM mass residual remains",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IM3405_1_beta",
            "quantity": "kappa_v",
            "if_selector_signed": "eta/source/operator lanes collapse; PiM/boundary/readout/coupling/q_loc still require their matching silence clauses",
            "remaining_if_not_signed": "use 3403 reduced envelope plus derivative-order residual law",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IM3405_2_gamma",
            "quantity": "gamma-1",
            "if_selector_signed": "EH metric core gives gamma=1 before residuals",
            "remaining_if_not_signed": "R2/scalar/vector/connection/readout maps must be bounded",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IM3405_3_preferred_frame",
            "quantity": "alpha_i, alpha3, xi",
            "if_selector_signed": "mode-rank and q_loc vector silence can kill preferred-frame/domain leakage",
            "remaining_if_not_signed": "q_loc/vector/domain/projector projections remain high-risk",
            "valid_for_claim": False,
        },
        {
            "impact_id": "IM3405_4_Maxwell_EM_stress",
            "quantity": "EM/Poynting stress ownership",
            "if_selector_signed": "same Hilbert source puts Maxwell/Poynting stress on the source side before boundary bookkeeping",
            "remaining_if_not_signed": "hidden Hodge/current normalization and boundary-flux shadow rows remain",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "GATE3405_0_two_derivative_math",
            "claim": "two-derivative metric normal form selects EH",
            "gate_pass": True,
            "reason": "the scalar-density basis at <=2 derivatives is sqrt(-g)(C0+C1R)+dB",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3405_1_parent_mode_rank",
            "claim": "MTS parent local vacuum has only massless spin-2 q-basic metric modes",
            "gate_pass": False,
            "reason": "parent Hessian/mode-rank extraction has not been performed and R11 families remain live",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3405_2_vertical_silence",
            "claim": "vertical/extra sectors are gauge, gapped double-zero, or source/readout silent",
            "gate_pass": False,
            "reason": "actual scalar/vector/torsion/memory/domain/bulk-X rows lack parent-owned zero coefficients",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3405_3_EH_selector",
            "claim": "MTS derives the EH selector rather than importing it",
            "gate_pass": False,
            "reason": "the selector theorem is exact conditional but parent normal-form hypotheses are unsigned",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
        {
            "gate_id": "GATE3405_4_local_GR",
            "claim": "local GR/PPN is derived",
            "gate_pass": False,
            "reason": "beta/gamma/source/readout/q_loc vector gates remain downstream of the selector",
            "claim_allowed": False,
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3405_0_real_progress",
            "finding": "3405 derives the EH selector from a smaller target: two-derivative massless spin-2 quotient normal form plus universal Hilbert source",
            "reason": "the EH problem is no longer a foggy GR-import issue; it is a parent Hessian/mode-rank and vertical-silence problem",
            "next_action": "extract or bound the parent Hessian/mode-rank normal form",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3405_1_not_done",
            "finding": "MTS still does not own EH at claim level",
            "reason": "R11 non-EH families survive generic covariance and require either signed zero coefficients or derivative-order bounds",
            "next_action": "do not publish local-GR claim; continue proof attempt or populate non-EH residual bounds",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3405_2_best_next",
            "finding": "the best next target is parent Hessian/mode-rank extraction",
            "reason": "if only TT spin-2 is long-range, the spin-2 bootstrap plus Hilbert source gives the cleanest EH derivation route",
            "next_action": "build 3406 parent Hessian mode-rank extractor; q_loc vector split remains second target",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_id": "3406-Y5-R2FR-parent-Hessian-mode-rank-extractor-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3406_parent_Hessian_mode_rank_extractor.py",
            "objective": "extract the local vacuum Hessian/mode-rank signature needed for the spin-2 EH bootstrap route",
            "why_next": "this is the constructive way to prove or reject the central PNF3405_1 premise rather than circling the EH selector",
            "valid_for_claim": False,
        },
        {
            "target_id": "3407-Y5-R2FR-derivative-order-residual-bound-pack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3407_derivative_order_residual_bound_pack.py",
            "objective": "if mode-rank extraction cannot zero non-EH rows, turn the four-derivative/extra-field residual laws into scored bound inputs",
            "why_next": "this is the fallback route that prevents a failed EH proof from wasting the local-GR program",
            "valid_for_claim": False,
        },
        {
            "target_id": "3408-Y5-R2FR-q_loc-U2-alpha-vector-projection-split-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3408_q_loc_U2_alpha_vector_projection_split.py",
            "objective": "separate q_loc beta, alpha_i/alpha3 and xi projections after the selector/mode-rank fork",
            "why_next": "q_loc remains the highest-danger preferred-frame guard after EH-selector progress",
            "valid_for_claim": False,
        },
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3405_0_scope",
            "check": "writes only 3405 files under post-checkpoint-work",
            "status": "PASS_IF_VALIDATION_TRUE",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3405_1_no_claim",
            "check": "two-derivative math is allowed but MTS parent EH claim remains blocked",
            "status": "NONCLAIM_SELECTOR_ATTEMPT",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3405_2_next",
            "check": "next step is Hessian/mode-rank extraction, not another generic missing ledger",
            "status": "FORWARD_DERIVATION_ROUTE",
            "valid_for_claim": False,
        },
    ]


def validation(outputs: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(check_id: str, check: str, passed: bool, detail: str = "") -> None:
        rows.append({"check_id": check_id, "check": check, "passed": bool(passed), "detail": detail})

    generated_paths = [str(path) for path in OUTPUTS.values()] + [str(DOC)]
    all_nonclaim = all(
        str(row.get("valid_for_claim", False)).lower() == "false"
        for name, table in outputs.items()
        if name != "validation"
        for row in table
    )

    add("VAL3405_0_sources", "all registered sources exist", all(row["exists"] for row in outputs["source_register"]), f"sources={len(outputs['source_register'])}")
    add("VAL3405_1_hypotheses", "parent normal-form hypotheses written", len(outputs["normal_form_hypotheses"]) >= 8, "")
    add("VAL3405_2_selector_math", "EH selector proof includes two-derivative basis", any("two-derivative" in row["claim"] for row in outputs["eh_selector_proof"]), "")
    add("VAL3405_3_spin2", "spin-2 bootstrap route written", len(outputs["spin2_bootstrap"]) >= 4 and any("Fierz-Pauli" in row["if_passes"] for row in outputs["spin2_bootstrap"]), "")
    add("VAL3405_4_bound_law", "fallback derivative-order residual law written", len(outputs["derivative_order_bound"]) >= 4, "")
    add("VAL3405_5_operator_triage", "R11 beta families triaged", len(outputs["operator_triage"]) >= 12, "")
    add("VAL3405_6_result", "selector result distinguishes math from MTS claim", any(row["claim_status"] == "DERIVED_MATH_NOT_MTS_SIGNATURE" for row in outputs["selector_result"]), "")
    add("VAL3405_7_gates", "EH/local-GR claim gates remain blocked", not any(row["gate_pass"] for row in outputs["promotion_gates"] if row["gate_id"] in {"GATE3405_1_parent_mode_rank", "GATE3405_2_vertical_silence", "GATE3405_3_EH_selector", "GATE3405_4_local_GR"}), "")
    add("VAL3405_8_no_overclaim", "all generated rows are nonclaim", all_nonclaim, "")
    add("VAL3405_9_scope", "no 3405 output path targets formalization-workbench", "formalization-workbench" not in "\n".join(generated_paths), "")
    add("VAL3405_10_next", "next target is Hessian/mode-rank extraction", any("Hessian-mode-rank" in row["target_id"] for row in outputs["next_target"]), "")
    overall = all(row["passed"] for row in rows)
    add("VAL3405_11_overall", "3405 validation overall", overall, "all required checks passed" if overall else "one or more checks failed")
    return rows


def write_doc(outputs: dict[str, list[dict[str, Any]]]) -> None:
    parts = [
        "# 3405 - Y5/R2FR parent normal-form EH selector proof attempt under AX1090",
        "",
        "## Verdict",
        "",
        "- 3405 makes a real derivation move: EH is selected from a two-derivative q-basic metric normal form, or equivalently from a massless spin-2 bootstrap with universal Hilbert source.",
        "- This does not yet prove MTS owns EH. It reduces the hard target to parent Hessian/mode-rank extraction plus vertical-kernel silence.",
        "- If the parent has only the long-range q-basic spin-2 metric and the leading local action is two-derivative, the local quotient action is `sqrt(-g)(C0+C1 R)+dB`, so EH follows.",
        "- If that premise fails, the theory must carry a derivative-order/non-EH residual bound instead of claiming local GR.",
        "",
        "## Parent Normal-Form Hypotheses",
        md_table(outputs["normal_form_hypotheses"]),
        "",
        "## EH Selector Proof Attempt",
        md_table(outputs["eh_selector_proof"]),
        "",
        "## Spin-2 Bootstrap Route",
        md_table(outputs["spin2_bootstrap"]),
        "",
        "## Derivative-Order Residual Bound",
        md_table(outputs["derivative_order_bound"]),
        "",
        "## Non-EH Operator Triage",
        md_table(outputs["operator_triage"]),
        "",
        "## Selector Result",
        md_table(outputs["selector_result"]),
        "",
        "## Local-GR Impact",
        md_table(outputs["local_gr_impact"]),
        "",
        "## Promotion Gates",
        md_table(outputs["promotion_gates"]),
        "",
        "## Decision Ledger",
        md_table(outputs["decision_ledger"]),
        "",
        "## Next Target",
        md_table(outputs["next_target"]),
        "",
        "## Validation",
        md_table(outputs["validation"]),
        "",
    ]
    DOC.write_text("\n".join(parts), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    outputs: dict[str, list[dict[str, Any]]] = {
        "source_register": source_register(),
        "normal_form_hypotheses": normal_form_hypotheses(),
        "eh_selector_proof": eh_selector_proof(),
        "spin2_bootstrap": spin2_bootstrap(),
        "derivative_order_bound": derivative_order_bound(),
        "operator_triage": operator_triage(),
        "selector_result": selector_result(),
        "local_gr_impact": local_gr_impact(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    outputs["validation"] = validation(outputs)
    for key, path in OUTPUTS.items():
        write_csv(path, outputs[key])
    write_doc(outputs)

    if not all(row["passed"] for row in outputs["validation"]):
        raise RuntimeError("3405 validation failed")

    print(f"Wrote {DOC}")
    print(f"Wrote {len(OUTPUTS)} CSV outputs under {OUT}")
    print("; ".join(f"{path.name}={len(outputs[key])}" for key, path in OUTPUTS.items()))


if __name__ == "__main__":
    main()
