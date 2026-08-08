from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "source-intake" / "mts_residuals"
DOC = ROOT / "3433-Y5-R2FR-MHref-tau-source-normalization-lock-or-residual-vector-under-AX1090.md"
FORMALIZATION = ROOT.parent / "formalization-workbench"

SOURCES = {
    "doc_3432": ROOT / "3432-Y5-R2FR-GammaKhat-q_loc-Hilbert-owner-or-residual-bound-under-AX1090.md",
    "next_3432": OUT / "P8_Y5_R2FR_3432_NEXT_TARGET.csv",
    "qloc_bound_3432": OUT / "P8_Y5_R2FR_3432_QLOC_RESIDUAL_BOUND_PACK.csv",
    "qloc_operator_3432": OUT / "P8_Y5_R2FR_3432_QLOC_PPN_R10_OPERATOR_UPDATE.csv",
    "mhref_candidates_3425": OUT / "P8_Y5_R2FR_3425_MHREF_CANDIDATE_ROWS.csv",
    "hpi_bounds_3425": OUT / "P8_Y5_R2FR_3425_HPI_M_RESIDUAL_BOUND_ROWS.csv",
    "pc3400_3_3425": OUT / "P8_Y5_R2FR_3425_PC3400_3_LOCK_AUDIT.csv",
    "promotion_3425": OUT / "P8_Y5_R2FR_3425_PROMOTION_GATES.csv",
    "icomm_3426": OUT / "P8_Y5_R2FR_3426_ICOMM_BOUND_ROWS.csv",
    "bzero_3427": OUT / "P8_Y5_R2FR_3427_BZERO_BOUND_ROWS.csv",
    "hidden_bound_3430": OUT / "P8_Y5_R2FR_3430_HIDDEN_PROJECTOR_BOUND_ROWS.csv",
    "domain_bound_3431": OUT / "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv",
    "source_measure_theorem_509": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_THEOREM.csv",
    "source_measure_residual_509": OUT / "P8_SOURCE_MEASURE_MEFF_FLUX_RESIDUAL_MAP.csv",
    "worldtube_theorem_510": OUT / "P8_WORLDTUBE_SOURCE_MEASURE_THEOREM.csv",
    "worldtube_proof_510": OUT / "P8_WORLDTUBE_SOURCE_MEASURE_PROOF_SKETCH.csv",
    "constant_gm_runner": OUT / "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
    "constant_kappa_decision": OUT / "P8_CONSTANT_KAPPA_DECISION.csv",
    "source_normalized_stack": OUT / "P8_source_normalized_Newton_branch_STACK.csv",
    "source_residual_template": OUT / "P8_source_normalization_residual_vector_TEMPLATE.csv",
}

OUTPUTS = {
    "source_register": OUT / "P8_Y5_R2FR_3433_SOURCE_REGISTER.csv",
    "source_lock_theorem": OUT / "P8_Y5_R2FR_3433_MHREF_TAU_SOURCE_LOCK_THEOREM.csv",
    "same_frame_audit": OUT / "P8_Y5_R2FR_3433_SAME_FRAME_MHREF_TAU_AUDIT.csv",
    "epsilon_mu_vector": OUT / "P8_Y5_R2FR_3433_EPSILON_MU_RESIDUAL_VECTOR.csv",
    "newton_ppn_gates": OUT / "P8_Y5_R2FR_3433_NEWTON_PPN_READOUT_GATES.csv",
    "pc3400_update": OUT / "P8_Y5_R2FR_3433_PC3400_SOURCE_COUPLING_UPDATE.csv",
    "promotion_gates": OUT / "P8_Y5_R2FR_3433_PROMOTION_GATES.csv",
    "decision_ledger": OUT / "P8_Y5_R2FR_3433_DECISION_LEDGER.csv",
    "next_target": OUT / "P8_Y5_R2FR_3433_NEXT_TARGET.csv",
    "runner_nonclaim": OUT / "P8_Y5_R2FR_3433_RUNNER_NONCLAIM.csv",
    "validation": OUT / "P8_Y5_BRR545_3433_VALIDATION.csv",
}


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


def source_register() -> list[dict[str, Any]]:
    roles = {
        "doc_3432": "q_loc handoff",
        "next_3432": "3433 target declaration",
        "qloc_bound_3432": "q_loc residual bound pack",
        "qloc_operator_3432": "q_loc source-normalization operator handoff",
        "mhref_candidates_3425": "M_H_ref candidate rows",
        "hpi_bounds_3425": "Hamiltonian/PiM residual bounds",
        "pc3400_3_3425": "PC3400_3 lock audit",
        "promotion_3425": "prior promotion gates",
        "icomm_3426": "PiM commutator bounds",
        "bzero_3427": "boundary/reference bounds",
        "hidden_bound_3430": "hidden/projector residual bounds",
        "domain_bound_3431": "domain/projector operator bounds",
        "source_measure_theorem_509": "source-measure/Meff flux theorem",
        "source_measure_residual_509": "source-measure residual map",
        "worldtube_theorem_510": "worldtube source-measure theorem",
        "worldtube_proof_510": "worldtube proof sketch",
        "constant_gm_runner": "constant GM residual runner input",
        "constant_kappa_decision": "constant kappa decision",
        "source_normalized_stack": "source-normalized Newton branch stack",
        "source_residual_template": "source-normalization residual vector template",
    }
    return [
        {
            "source_id": key,
            "path": str(path),
            "exists": path.exists(),
            "role": roles[key],
            "valid_for_claim": False,
        }
        for key, path in SOURCES.items()
    ]


def source_lock_theorem() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "SL3433_0_definition",
            "statement": "Measured Newtonian source strength must be built from one same-frame Hamiltonian/Hilbert source denominator.",
            "formula": "mu_obs := G0 M_H_ref (1+epsilon_mu), M_H_ref:=c^-2(H_tau[S_outer]-H_ref)",
            "status": "DEFINITION_LOCK_CANDIDATE",
            "condition_or_missing": "tau, surface, reference, units and source path must be fixed in one row",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SL3433_1_same_tau",
            "statement": "The time generator tau must be the same for source charge, clock normalization, orbital readout, and boundary subtraction.",
            "formula": "tau_source=tau_clock=tau_orbit=tau_boundary=tau_obs",
            "status": "NECESSARY_LOCK_THEOREM",
            "condition_or_missing": "parent observed coframe/asymptotic normalization not fully derived",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SL3433_2_flux_closure",
            "statement": "If the projected Hilbert mass current is closed in the compact exterior, M_H_ref has no radial/time leakage.",
            "formula": "d(Pi_M J_H)=0 and boundary flux=0 => partial_r M_H_ref=0 and partial_tau M_H_ref=0",
            "status": "CONDITIONAL_FLUX_THEOREM",
            "condition_or_missing": "PiM chain-map, source-current descent, and boundary silence not all signed",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SL3433_3_constant_kappa",
            "statement": "A universal constant kappa can be absorbed into G0 only if it is source-blind, range-blind, frame-blind, and time/radius independent.",
            "formula": "D_t kappa=D_r kappa=D_A kappa=D_lambda kappa=D_frame kappa=0",
            "status": "CONDITIONAL_GLOBAL_CALIBRATION_RULE",
            "condition_or_missing": "topological kappa route is conditional/not adopted as current parent proof",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SL3433_4_residual_identity",
            "statement": "Any failure of the source lock enters an observable residual vector, not a hidden recalibration.",
            "formula": "delta ln mu_obs = delta ln G_eff + delta ln M_H_ref + delta epsilon_mu + delta_frame + delta_range + delta_species",
            "status": "EXACT_ACCOUNTING_RULE",
            "condition_or_missing": "numeric values and row-specific maps missing",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SL3433_5_newton_limit",
            "statement": "Newtonian recovery follows only after EH/Poisson source coefficient, Gauss surface equality, and inverse-square readout share the same M_H_ref.",
            "formula": "nabla^2 Phi=4 pi G0 rho_H, integral gradPhi.dS=4 pi G0 M_H_ref, a_r=-G0 M_H_ref/r^2",
            "status": "CONDITIONAL_NEWTON_STACK",
            "condition_or_missing": "same-frame source/readout and residual-zero gates still open",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SL3433_6_no_calibration_cheat",
            "statement": "A single fitted GM can hide a universal constant offset, but it cannot hide derivative, range, species, frame, q_loc, boundary, or PPN hair.",
            "formula": "constant epsilon0 may be absorbed; D_i epsilon_mu, alpha(lambda), eta_AB, beta/gamma/alpha_i/xi residuals cannot",
            "status": "NO_CHEAT_RULE",
            "condition_or_missing": "requires row-by-row residual vector before claims",
            "valid_for_claim": False,
        },
        {
            "theorem_id": "SL3433_7_verdict",
            "statement": "Current MTS has a legitimate EH/Hilbert denominator route but not a full source-normalization lock.",
            "formula": "source_lock_current=false; epsilon_mu_residual_vector retained",
            "status": "PARTIAL_EH_ROUTE_RESIDUAL_VECTOR_REQUIRED",
            "condition_or_missing": "tau/reference/PiM/q_loc/domain/boundary/extra/source-frame rows",
            "valid_for_claim": False,
        },
    ]


def same_frame_audit() -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "SFA3433_0_tau_lock",
            "lock": "tau observed-time generator",
            "current_evidence": "3425 defines epsilon_tau_lock and partial tau naming",
            "pass_now": False,
            "blocker": "tau not parent-selected as one observed source/clock/orbit/boundary generator",
            "residual_symbol": "epsilon_tau_lock",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SFA3433_1_reference",
            "lock": "fixed derivative-silent H_ref",
            "current_evidence": "3427 fixed reference theorem helps under Hilbert-identity branch",
            "pass_now": False,
            "blocker": "reference functional/background class not parent-derived for full MTS branch",
            "residual_symbol": "epsilon_reference",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SFA3433_2_PiM_chain",
            "lock": "PiM Hilbert-current chain map",
            "current_evidence": "3426 identity branch can make I_comm=0 conditionally",
            "pass_now": False,
            "blocker": "identity/inclusion branch not parent-adopted across source readout",
            "residual_symbol": "epsilon_PiM_comm",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SFA3433_3_MHref_positive",
            "lock": "positive same-frame M_H_ref denominator",
            "current_evidence": "3425 EH candidate denominator exists",
            "pass_now": False,
            "blocker": "no source-specific claim-ready row with tau/surface/reference/units/source path",
            "residual_symbol": "epsilon_HPiM_after_EH_lock",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SFA3433_4_q_loc",
            "lock": "q_loc contributes no extra source-normalization hair",
            "current_evidence": "3432 decomposes q_loc residual",
            "pass_now": False,
            "blocker": "Hilbert owner and Khat identity are unsigned; bound values missing",
            "residual_symbol": "epsilon_q_loc_TGK_mass",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SFA3433_5_domain_boundary_extra",
            "lock": "domain/projector/boundary/extra mass are zero or bounded",
            "current_evidence": "3427/3430/3431 provide bound formulas",
            "pass_now": False,
            "blocker": "no numeric or parent-signed zero rows for domain/boundary/hidden totals",
            "residual_symbol": "epsilon_domain_projector_abs + epsilon_boundary_symplectic_abs + epsilon_extra_mass",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SFA3433_6_same_frame",
            "lock": "source frame equals matter/clock/orbital frame",
            "current_evidence": "source-normalized Newton stack has SN0 as first rung",
            "pass_now": False,
            "blocker": "same observed coframe/source variation theorem not parent-derived",
            "residual_symbol": "delta_frame_source",
            "valid_for_claim": False,
        },
        {
            "audit_id": "SFA3433_7_second_order",
            "lock": "second-order PPN source closure",
            "current_evidence": "constant GM runner keeps beta source residue deferred",
            "pass_now": False,
            "blocker": "first-order Newton matching does not clear beta/gamma/PPN",
            "residual_symbol": "delta_beta_source",
            "valid_for_claim": False,
        },
    ]


def epsilon_mu_vector() -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EMU3433_0_constant_Geff",
            "residual": "dln_Geff_dt / D_r G_eff / source/range/frame G_eff",
            "formula": "delta ln G_eff contributes directly to delta ln mu_obs",
            "target_or_bound": "Gdot 9.6e-15 yr^-1; range/source/frame rows require zero or bounds",
            "source_link": "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
            "status": "CONDITIONAL_KAPPA_ROUTE_NOT_CLAIMED",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMU3433_1_MHref_flux",
            "residual": "dln_MHref_dt / radial M_H_ref leakage",
            "formula": "delta ln M_H_ref = epsilon_tau_lock + epsilon_reference + epsilon_PiM_comm + epsilon_boundary_flux",
            "target_or_bound": "mass conservation / beta / Gdot / radial hair locks",
            "source_link": "P8_Y5_R2FR_3425_HPI_M_RESIDUAL_BOUND_ROWS.csv",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMU3433_2_q_loc",
            "residual": "epsilon_q_loc_TGK_mass",
            "formula": "epsilon_q_loc_TGK_mass <= sum(abs(QRB3432_0..QRB3432_5))",
            "target_or_bound": "PPN/R10/source-normalization after M_H_ref map",
            "source_link": "P8_Y5_R2FR_3432_QLOC_RESIDUAL_BOUND_PACK.csv",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMU3433_3_domain_projector",
            "residual": "epsilon_domain_projector_abs",
            "formula": "epsilon_domain_projector_abs <= sum(abs(DPOB3431_0..DPOB3431_3))",
            "target_or_bound": "alpha1/alpha2/alpha3/xi/source-normalization",
            "source_link": "P8_Y5_R2FR_3431_DOMAIN_PROJECTOR_OPERATOR_BOUND_PACK.csv",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMU3433_4_boundary_reference",
            "residual": "epsilon_boundary_symplectic_abs",
            "formula": "(|B_zero|+|Delta_symp|+|Delta_H_ref|+|Phi_boundary|)/M_H_ref",
            "target_or_bound": "orbital GM, clocks/Gdot, alpha3",
            "source_link": "P8_Y5_R2FR_3427_BZERO_BOUND_ROWS.csv",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMU3433_5_hidden_extra",
            "residual": "epsilon_hidden_total_abs / epsilon_extra_mass",
            "formula": "absolute hidden/projector/extra-sector sum, no cancellations",
            "target_or_bound": "local GR/Newton/PPN/R10/clocks/orbital",
            "source_link": "P8_Y5_R2FR_3430_HIDDEN_PROJECTOR_BOUND_ROWS.csv",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMU3433_6_species_frame",
            "residual": "eta_source_AB + delta_frame_source",
            "formula": "Delta_AB ln mu_obs=0 and Delta_frame ln mu_obs=0 only under same-frame universal source theorem",
            "target_or_bound": "eta_source_AB <= 2.8e-15 or derived zero; frame residual below WEP/clock/operator locks",
            "source_link": "P8_source_normalization_residual_vector_TEMPLATE.csv",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMU3433_7_range_radial",
            "residual": "alpha(lambda) + partial_r_ln_mu_obs",
            "formula": "finite-range/radial source hair cannot be absorbed into one local GM calibration",
            "target_or_bound": "verified alpha(lambda) curve or no-finite-range theorem; radial no-hair/PPN bound",
            "source_link": "P8_CONSTANT_GM_LOCAL_RESIDUAL_RUNNER_INPUT.csv",
            "status": "FORMULA_READY_VALUES_MISSING",
            "valid_for_claim": False,
        },
        {
            "row_id": "EMU3433_8_second_order",
            "residual": "delta_beta_source and second-order PPN source residue",
            "formula": "first-order Poisson success does not set beta-1 or nonlinear source terms to zero",
            "target_or_bound": "beta_minus_1 <= 7.8e-5 or derived second-order closure",
            "source_link": "P8_source_normalization_residual_vector_TEMPLATE.csv",
            "status": "DEFERRED_BUT_BLOCKS_LOCAL_GR",
            "valid_for_claim": False,
        },
    ]


def newton_ppn_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "NPG3433_0_EH_subcharge",
            "gate": "public EH/Hilbert subcharge exists",
            "result": "PASS_CONDITIONAL_SUBTHEOREM",
            "evidence": "3425 public EH/Hilbert subcharge route",
            "valid_for_claim": False,
        },
        {
            "gate_id": "NPG3433_1_same_MHref",
            "gate": "same M_H_ref controls source, metric 1/r, and orbit",
            "result": "FAIL_CURRENT",
            "evidence": "source-specific M_H_ref row missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "NPG3433_2_constant_universal_G",
            "gate": "G/kappa is universal and derivative-free",
            "result": "CONDITIONAL_NOT_ADOPTED",
            "evidence": "constant kappa route exists only as conditional decision",
            "valid_for_claim": False,
        },
        {
            "gate_id": "NPG3433_3_Poisson",
            "gate": "EH weak-field equation reduces to Poisson with Hilbert source",
            "result": "CONDITIONAL_EH_ONLY",
            "evidence": "source-normalized stack SN5, but residual source purity is not proven",
            "valid_for_claim": False,
        },
        {
            "gate_id": "NPG3433_4_inverse_square",
            "gate": "same charge gives pure inverse-square orbital readout",
            "result": "NOT_DERIVED",
            "evidence": "SN9 and finite-range/radial rows remain open",
            "valid_for_claim": False,
        },
        {
            "gate_id": "NPG3433_5_PPN",
            "gate": "PPN beta/gamma/preferred-frame rows are controlled",
            "result": "BLOCKED",
            "evidence": "domain/q_loc/boundary/source-normalization rows missing values",
            "valid_for_claim": False,
        },
    ]


def pc3400_update() -> list[dict[str, Any]]:
    return [
        {
            "pc_id": "PC3400_3",
            "requirement": "H_tau/PiM/M_H_ref source denominator lock",
            "3433_result": "same-frame theorem and epsilon_mu residual vector written",
            "signed_part": "EH/Hilbert subcharge route remains conditionally valid",
            "open_part": "tau/reference/PiM/source-specific M_H_ref row not parent-signed",
            "status": "PARTIAL_NOT_PROMOTED",
            "valid_for_claim": False,
        },
        {
            "pc_id": "PC3400_4",
            "requirement": "no extra compact-source mass",
            "3433_result": "q_loc/domain/boundary/hidden residuals are now explicitly injected into epsilon_mu",
            "signed_part": "no calibration-cheat rule prevents hiding these channels in fitted GM",
            "open_part": "zero certificates or numeric bounds missing",
            "status": "PARTIAL_NOT_PROMOTED",
            "valid_for_claim": False,
        },
    ]


def promotion_gates() -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "PG3433_0_source_lock_theorem",
            "gate": "M_H_ref/tau source lock theorem exists",
            "result": "PASS_CONDITIONAL_THEOREM",
            "evidence": "SL3433 rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3433_1_epsilon_mu_vector",
            "gate": "source-normalization residual vector is assembled",
            "result": "PASS_SYMBOLIC_VALUES_MISSING",
            "evidence": "EMU3433 rows",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3433_2_Newton",
            "gate": "Newtonian source coupling is derived for current MTS",
            "result": "BLOCKED",
            "evidence": "same-frame M_H_ref/tau and residual-zero rows missing",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3433_3_PPN",
            "gate": "local GR/PPN is derived",
            "result": "BLOCKED",
            "evidence": "second-order PPN, q_loc, domain, boundary, source-normalization rows remain open",
            "valid_for_claim": False,
        },
        {
            "gate_id": "PG3433_4_score_ready",
            "gate": "residual vector can be scored numerically",
            "result": "FAIL_VALUES_MISSING",
            "evidence": "no numeric M_H_ref/q_loc/domain/boundary/source maps",
            "valid_for_claim": False,
        },
    ]


def decision_ledger() -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC3433_0_G_constant",
            "decision": "Treat G0 as an allowed universal calibration only after derivative/source/range/frame hair is zero or bounded.",
            "reason": "GR also uses a measured Newton constant, but it cannot hide local non-universal residuals.",
            "next_action": "separate constant offset from derivative/residual vector",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3433_1_MHref",
            "decision": "Do not use bare rest mass as the source denominator.",
            "reason": "the exterior charge must include Hilbert/Hamiltonian dressing and binding energy in the same frame.",
            "next_action": "fill source-specific M_H_ref row or keep epsilon_HPiM residual",
            "valid_for_claim": False,
        },
        {
            "decision_id": "DEC3433_2_next",
            "decision": "Next route should derive the source-normalized Poisson limit with residual terms visible.",
            "reason": "this connects field-theory source coupling to actual Newtonian mechanics without importing GR by assumption.",
            "next_action": "derive Poisson/Kepler stack or produce first score-ready residual runner",
            "valid_for_claim": False,
        },
    ]


def next_target() -> list[dict[str, Any]]:
    return [
        {
            "target_doc": "3434-Y5-R2FR-source-normalized-Poisson-limit-and-first-PPN-residual-stack-under-AX1090.md",
            "target_script": "scripts/Y5_R2FR_3434_source_normalized_Poisson_limit_and_first_PPN_residual_stack.py",
            "objective": "derive the source-normalized Poisson/Newton limit from the EH/Hilbert branch while carrying epsilon_mu/q_loc/domain/boundary residuals into the first PPN residual stack",
            "success_condition": "Poisson coefficient and Kepler readout are derived conditionally, with every non-EH/source-normalization residual visible as a score-ready or blocked row",
            "valid_for_claim": False,
        }
    ]


def runner_nonclaim() -> list[dict[str, Any]]:
    return [
        {
            "runner_id": "RUN3433_0",
            "purpose": "prevent GM calibration cheat",
            "rule": "only a universal constant offset may be absorbed into G0; derivative/source/range/frame/q_loc/domain/boundary terms must remain explicit",
            "current_value": "claim_allowed=false",
            "valid_for_claim": False,
        },
        {
            "runner_id": "RUN3433_1",
            "purpose": "force same-frame denominator",
            "rule": "Newton/PPN claims require one tau-normalized M_H_ref source denominator or an explicit epsilon_mu residual vector",
            "current_value": "epsilon_mu_vector_required=true",
            "valid_for_claim": False,
        },
    ]


def all_outputs_scoped() -> bool:
    root_resolved = ROOT.resolve()
    return all(root_resolved in path.resolve().parents or path.resolve() == root_resolved for path in [DOC, *OUTPUTS.values()])


def all_generated_nonclaim(rows_by_name: dict[str, list[dict[str, Any]]]) -> bool:
    for name, rows in rows_by_name.items():
        if name == "validation":
            continue
        for row in rows:
            if "valid_for_claim" in row and str(row["valid_for_claim"]).lower() != "false":
                return False
            if "claim_allowed" in row and str(row["claim_allowed"]).lower() != "false":
                return False
    return True


def validation_rows(rows_by_name: dict[str, list[dict[str, Any]]], start_utc: datetime) -> list[dict[str, Any]]:
    source_rows = rows_by_name["source_register"]
    theorem_rows = rows_by_name["source_lock_theorem"]
    audit_rows = rows_by_name["same_frame_audit"]
    epsilon_rows = rows_by_name["epsilon_mu_vector"]
    newton_rows = rows_by_name["newton_ppn_gates"]
    pc_rows = rows_by_name["pc3400_update"]
    promotion_rows = rows_by_name["promotion_gates"]
    next_rows = rows_by_name["next_target"]
    modified_count = 0
    if FORMALIZATION.exists():
        start_ts = start_utc.timestamp()
        modified_count = sum(1 for path in FORMALIZATION.rglob("*") if path.is_file() and path.stat().st_mtime >= start_ts)
    validations = [
        {
            "check_id": "VAL3433_0_sources_exist",
            "condition": "all cited source paths exist",
            "passed": all(row["exists"] for row in source_rows),
            "detail": f"{sum(1 for row in source_rows if row['exists'])}/{len(source_rows)} source paths exist",
        },
        {
            "check_id": "VAL3433_1_outputs_scoped",
            "condition": "all outputs are in post-checkpoint-work",
            "passed": all_outputs_scoped(),
            "detail": str(ROOT),
        },
        {
            "check_id": "VAL3433_2_nonclaim",
            "condition": "all generated rows remain nonclaim",
            "passed": all_generated_nonclaim(rows_by_name),
            "detail": "valid_for_claim=false throughout generated rows",
        },
        {
            "check_id": "VAL3433_3_source_lock_theorem",
            "condition": "M_H_ref/tau source lock theorem exists",
            "passed": any(row["theorem_id"] == "SL3433_5_newton_limit" for row in theorem_rows),
            "detail": "source-normalized Newton theorem present as conditional stack",
        },
        {
            "check_id": "VAL3433_4_no_calibration_cheat",
            "condition": "GM calibration cheat is explicitly forbidden",
            "passed": any(row["theorem_id"] == "SL3433_6_no_calibration_cheat" for row in theorem_rows),
            "detail": "constant offset separated from derivative/range/source hair",
        },
        {
            "check_id": "VAL3433_5_locks_not_promoted",
            "condition": "same-frame locks are not falsely promoted",
            "passed": all(str(row["pass_now"]).lower() == "false" for row in audit_rows),
            "detail": "all same-frame locks remain unsigned",
        },
        {
            "check_id": "VAL3433_6_epsilon_mu_vector",
            "condition": "epsilon_mu residual vector covers major source-normalization channels",
            "passed": len(epsilon_rows) >= 9 and any(row["row_id"] == "EMU3433_2_q_loc" for row in epsilon_rows),
            "detail": f"{len(epsilon_rows)} epsilon_mu rows",
        },
        {
            "check_id": "VAL3433_7_newton_ppn_gates",
            "condition": "Newton and PPN gates are separated",
            "passed": any(row["gate_id"] == "NPG3433_3_Poisson" for row in newton_rows)
            and any(row["gate_id"] == "NPG3433_5_PPN" and row["result"] == "BLOCKED" for row in newton_rows),
            "detail": "Poisson conditional and PPN blocked rows present",
        },
        {
            "check_id": "VAL3433_8_pc3400_updates",
            "condition": "PC3400 source-coupling updates exist",
            "passed": len(pc_rows) == 2 and all(row["status"] == "PARTIAL_NOT_PROMOTED" for row in pc_rows),
            "detail": "PC3400_3 and PC3400_4 updated as partial",
        },
        {
            "check_id": "VAL3433_9_local_GR_blocked",
            "condition": "local GR remains blocked until residual rows close",
            "passed": any(row["gate_id"] == "PG3433_3_PPN" and row["result"] == "BLOCKED" for row in promotion_rows),
            "detail": "no local-GR claim promoted",
        },
        {
            "check_id": "VAL3433_10_next_target",
            "condition": "next target attacks Poisson/PPN source-normalized readout",
            "passed": next_rows[0]["target_doc"].startswith("3434-Y5-R2FR-source-normalized-Poisson"),
            "detail": next_rows[0]["target_doc"],
        },
        {
            "check_id": "VAL3433_11_formalization_untouched",
            "condition": "formalization-workbench modified-file count remains 0 during this run",
            "passed": modified_count == 0,
            "detail": f"modified_count_since_start={modified_count}",
        },
    ]
    validations.append(
        {
            "check_id": "VAL3433_12_overall",
            "condition": "3433 M_H_ref/tau source-normalization checkpoint is internally valid",
            "passed": all(row["passed"] for row in validations),
            "detail": "PASS" if all(row["passed"] for row in validations) else "FAIL",
        }
    )
    return validations


def write_doc(rows_by_name: dict[str, list[dict[str, Any]]]) -> None:
    text = f"""# 3433 - MHref/Tau Source-Normalization Lock or Residual Vector

## Summary
- This checkpoint connects the previous `q_loc`, domain, boundary, PiM, and extra-sector residuals to the actual measured Newtonian source strength.
- The central rule is simple: MTS may use a measured constant `G0` only as a universal calibration, not as a bin for hidden derivative/source/range/frame/projector hair.
- The clean theorem is conditional: one observed `tau`, one fixed reference, one positive same-frame `M_H_ref`, closed projected Hilbert mass flux, constant kappa, and zero/bounded residuals imply protected Newtonian `GM`.
- Current MTS does not yet pass that lock; therefore `epsilon_mu` becomes the explicit residual vector for Newton/PPN/R10/clocks.
- This is the bridge from formal local-GR derivation to empirical scoring: no residual can disappear into a fitted `GM` unless it is universal and derivative-free.

## Source Register
{md_table(rows_by_name["source_register"])}

## MHref/Tau Source Lock Theorem
{md_table(rows_by_name["source_lock_theorem"])}

## Same-Frame MHref/Tau Audit
{md_table(rows_by_name["same_frame_audit"])}

## Epsilon Mu Residual Vector
{md_table(rows_by_name["epsilon_mu_vector"])}

## Newton/PPN Readout Gates
{md_table(rows_by_name["newton_ppn_gates"])}

## PC3400 Source-Coupling Update
{md_table(rows_by_name["pc3400_update"])}

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
This is a proper engineering lock: `G` can be measured, but it cannot be used as a carpet. If q_loc/domain/boundary/hidden/source-frame residuals exist, they must show up in `epsilon_mu`, PPN, R10, clocks, or orbital rows. That keeps the route to Newton/GR honest.
"""
    DOC.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    start_utc = datetime.now(timezone.utc)
    rows_by_name = {
        "source_register": source_register(),
        "source_lock_theorem": source_lock_theorem(),
        "same_frame_audit": same_frame_audit(),
        "epsilon_mu_vector": epsilon_mu_vector(),
        "newton_ppn_gates": newton_ppn_gates(),
        "pc3400_update": pc3400_update(),
        "promotion_gates": promotion_gates(),
        "decision_ledger": decision_ledger(),
        "next_target": next_target(),
        "runner_nonclaim": runner_nonclaim(),
    }
    rows_by_name["validation"] = validation_rows(rows_by_name, start_utc)
    for name, rows in rows_by_name.items():
        write_csv(OUTPUTS[name], rows)
    write_doc(rows_by_name)
    failed = [row for row in rows_by_name["validation"] if not row["passed"]]
    if failed:
        raise SystemExit(f"3433 validation failed: {failed}")
    print(f"wrote {DOC}")
    print(f"wrote {len(OUTPUTS)} csv outputs")


if __name__ == "__main__":
    main()
