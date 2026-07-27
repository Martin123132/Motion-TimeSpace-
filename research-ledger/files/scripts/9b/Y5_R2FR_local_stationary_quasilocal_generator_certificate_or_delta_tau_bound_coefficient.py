from __future__ import annotations

import csv
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = ROOT.parent
FORMALIZATION = PROJECT_ROOT / "formalization-workbench"
RESIDUALS = ROOT / "source-intake" / "mts_residuals"
MICROSCOPE_RESIDUALS = ROOT / "source-intake" / "microscope" / "branch_locked_wep" / "residuals"
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1728"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1728 - Local Stationary Quasilocal Generator Certificate Or Delta Tau Bound Coefficient"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1728_0_1727_doc",
        "source_key": "1727_doc",
        "source_path": ROOT / "1727-Y5-R2FR-boundary-clock-superselection-or-delta-tau-residual-first-row.md",
        "needles": ["NEXT1727_0_primary", "local stationary/Killing or quasilocal generator certificate"],
    },
    {
        "source_id": "SRC1728_1_1727_next",
        "source_key": "1727_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1727_NEXT_TARGET.csv",
        "needles": ["1728-Y5-R2FR-local-stationary-quasilocal-generator-certificate-or-delta-tau-bound-coefficient.md", "selected"],
    },
    {
        "source_id": "SRC1728_2_1727_delta_tau",
        "source_key": "1727_delta_tau_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1727_DELTA_TAU_FIRST_RESIDUAL_ROW.csv",
        "needles": ["DTAU1727_1_source_current_delta_tau", "MISSING_TOBS_OPERATOR_NORM"],
    },
    {
        "source_id": "SRC1728_3_1727_validation",
        "source_key": "1727_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1727_VALIDATION.csv",
        "needles": ["VAL1727_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1728_4_685_killing_clock",
        "source_key": "685_killing_clock_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_685_KILLING_CLOCK_GATE.csv",
        "needles": ["KCG685_1_stationarity", "MISSING_LOCAL_STATIONARY_KILLING_CERTIFICATE"],
    },
    {
        "source_id": "SRC1728_5_685_tau_contract",
        "source_key": "685_tau_generator_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
        "needles": ["TGC685_1_Killing_stationary_route", "conditional_not_parent_derived"],
    },
    {
        "source_id": "SRC1728_6_457_doc",
        "source_key": "457_hamiltonian_doc",
        "source_path": ROOT / "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "needles": ["observed_time_generator", "not_parent_derived"],
    },
    {
        "source_id": "SRC1728_7_hamiltonian_contract",
        "source_key": "hamiltonian_boundary_charge",
        "source_path": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "needles": ["HC1_observed_time_generator", "not_parent_derived"],
    },
    {
        "source_id": "SRC1728_8_1726_observed_generator",
        "source_key": "1726_observed_generator",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_OBSERVED_TIME_GENERATOR_AUDIT.csv",
        "needles": ["OTG1726_6_verdict", "OBSERVED_TIME_GENERATOR_NOT_PARENT_SELECTED"],
    },
    {
        "source_id": "SRC1728_9_1726_Rtau_schema",
        "source_key": "1726_Rtau_schema",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_RTAU_RESIDUAL_BOUND_SCHEMA.csv",
        "needles": ["RTAU1726_1_source_current_bound", "MISSING_TOBS_OPERATOR_NORM"],
    },
    {
        "source_id": "SRC1728_10_1720_jh_row",
        "source_key": "1720_jh_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv",
        "needles": ["JHN1720_0_observed_Hilbert_current_norm_candidate", "MISSING_PARENT_SIGNED_TAU_OBS"],
    },
    {
        "source_id": "SRC1728_11_1719_ingredients",
        "source_key": "1719_ingredients",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1719_NUMERATOR_INGREDIENT_SOURCE_ROWS.csv",
        "needles": ["ING1719_0_JH_norm_candidate", "MISSING"],
    },
    {
        "source_id": "SRC1728_12_664_integrability",
        "source_key": "664_integrability",
        "source_path": RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
        "needles": ["HCI664_4_time_generator_lock", "same observed time/coframe branch is not parent-derived"],
    },
    {
        "source_id": "SRC1728_13_boundary_ref_status",
        "source_key": "boundary_reference_first_row",
        "source_path": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
        "needles": ["M_H_ref", "missing_claim_valid_source_or_zero_theorem"],
    },
    {
        "source_id": "SRC1728_14_same_coframe",
        "source_key": "same_coframe_parent_clause",
        "source_path": RESIDUALS / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "needles": ["UOC519_2_readout_uses_same_e", "conditional_clause_written_not_current_MTS_derived"],
    },
    {
        "source_id": "SRC1728_15_1725_no_lapse_guard",
        "source_key": "1725_no_lapse_guard",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1725_NO_LAPSE_RESCALING_GUARD.csv",
        "needles": ["NLR1725_4_verdict", "NO_LAPSE_RESCALING_GUARD_ACTIVE"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1728_SOURCE_REGISTER.csv",
    "certificate_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1728_LOCAL_GENERATOR_CERTIFICATE_AUDIT.csv",
    "certificate_attempt": RESIDUALS / "P8_Y5_PARENT_QLOC_1728_STATIONARY_QUASILOCAL_CERTIFICATE_ATTEMPT.csv",
    "coefficient_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1728_DELTA_TAU_BOUND_COEFFICIENT_ROWS.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1728_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1728_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1728_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1728_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1728_VALIDATION.csv",
}


COPY_MAP = {
    "certificate_audit": "R2FR_1728_LOCAL_GENERATOR_CERTIFICATE_AUDIT.csv",
    "certificate_attempt": "R2FR_1728_STATIONARY_QUASILOCAL_CERTIFICATE_ATTEMPT.csv",
    "coefficient_rows": "R2FR_1728_DELTA_TAU_BOUND_COEFFICIENT_ROWS.csv",
    "runner_refusal": "R2FR_1728_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1728_DECISION_LEDGER.csv",
    "next_target": "R2FR_1728_NEXT_TARGET.csv",
    "claim_gate": "R2FR_1728_CLAIM_GATE.csv",
}


def source_rows() -> list[dict[str, Any]]:
    rows = []
    for source in SOURCES:
        path = Path(source["source_path"])
        text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        needles_present = all(needle in text for needle in source["needles"])
        rows.append(
            {
                "branch_id": BRANCH_ID,
                "source_id": source["source_id"],
                "source_key": source["source_key"],
                "source_path": str(path),
                "exists": yesno(path.exists()),
                "needles": ";".join(source["needles"]),
                "needles_present": yesno(needles_present),
                "checked_utc": UTC,
            }
        )
    return rows


def certificate_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "LGC1728_0_stationary_killing",
            "certificate_clause": "stationary Killing generator",
            "candidate_statement": "A future-directed timelike xi exists in the local exterior with L_xi g_obs=0 and boundary-clock normalization.",
            "mathematical_form": "L_xi g_obs=0; g_obs(xi,xi)<0; N_B[e_obs,xi]=1",
            "current_status": "MISSING_LOCAL_STATIONARY_KILLING_CERTIFICATE",
            "blocking_gap": "stationary local domain and same-frame Hilbert conservation are not derived",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "LGC1728_1_quasilocal_flow",
            "certificate_clause": "quasilocal lapse/shift generator",
            "candidate_statement": "A finite-boundary lapse/shift pair defines tau_obs=N n+N^i e_i and is fixed by boundary clocks before readout.",
            "mathematical_form": "tau_obs=N_B n + N_B^i e_i; delta N_B=delta N_B^i=0; N_B from B_clock",
            "current_status": "MISSING_QUASILOCAL_LAPSE_SHIFT_CERTIFICATE",
            "blocking_gap": "no parent boundary phase-space class supplies fixed lapse/shift data for current MTS",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "LGC1728_2_asymptotic_time",
            "certificate_clause": "asymptotic time fallback",
            "candidate_statement": "If an asymptotic region exists, tau_obs approaches the normalized asymptotic time translation.",
            "mathematical_form": "tau_obs -> partial_t at infinity; N_infty=1; shift_infty=0",
            "current_status": "ASYMPTOTIC_ROUTE_NOT_AVAILABLE_FOR_COMPACT_BRANCH",
            "blocking_gap": "the current local compact branch does not have a sourced asymptotic normalization row",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "LGC1728_3_EH_exterior_constraints",
            "certificate_clause": "EH/exterior constraint compatibility",
            "candidate_statement": "The generator is a mass generator only if the local exterior has the EH-like constraint algebra or all non-EH charges are retained.",
            "mathematical_form": "S_ext -> S_EH+boundary; C_xi=0 or C_extra+C_projector+C_boundary retained",
            "current_status": "EH_EXTERIOR_NOT_PARENT_SIGNED",
            "blocking_gap": "Hamiltonian route is conditional downstream of EH exterior and no-extra-charge gates",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "LGC1728_4_boundary_integrability",
            "certificate_clause": "integrable boundary charge",
            "candidate_statement": "The same generator must make delta H_tau finite/integrable with a fixed reference.",
            "mathematical_form": "delta H_tau=int_S(delta Q_tau-i_tau theta); curl_phase_space(delta H_tau)=0; H_ref fixed once",
            "current_status": "INTEGRABILITY_REFERENCE_LOCK_NOT_DERIVED",
            "blocking_gap": "HCI664 and boundary-reference rows keep theta/Q_tau/B_ref/tau lock open",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "LGC1728_5_no_lapse_rescaling",
            "certificate_clause": "no lapse rescaling",
            "candidate_statement": "The certificate must fix the tau -> f tau ambiguity before comparing sectors.",
            "mathematical_form": "f=1 on B_clock and parent extension fixes f in A_ext; no sector-specific f_source/f_charge/f_clock",
            "current_status": "GUARD_ACTIVE_CERTIFICATE_MISSING",
            "blocking_gap": "1725 rejects rescaling shortcuts but does not construct the parent extension",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "LGC1728_6_same_frame_source_clock",
            "certificate_clause": "same-frame source/clock compatibility",
            "candidate_statement": "The generator must live in the same e_obs frame used by matter source, clocks, photons, rods and orbits.",
            "mathematical_form": "e_source=e_clock=e_photon=e_orbit=e_obs; tau_source=tau_clock=tau_obs",
            "current_status": "SAME_FRAME_CERTIFICATE_CONDITIONAL_ONLY",
            "blocking_gap": "same-coframe clauses are written but not current-MTS derived",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "LGC1728_7_verdict",
            "certificate_clause": "local generator certificate verdict",
            "candidate_statement": "Current MTS does not yet have a sourced stationary/Killing/quasilocal generator certificate.",
            "mathematical_form": "tau_obs extension certificate remains missing; delta_tau residual coefficient route activates",
            "current_status": "LOCAL_GENERATOR_CERTIFICATE_NOT_SIGNED",
            "blocking_gap": "stationarity/quasilocal data, boundary clock normalization, EH/exterior compatibility, integrability and same-frame proof are unsigned",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
    ]


def certificate_attempt_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LGA1728_0_exact_symmetry_route",
            "route": "Killing/stationary route",
            "mathematical_form": "L_xi g_obs=0 and nabla_mu T_obs^{mu nu}=0 imply nabla_mu(T_obs^{mu nu} xi_nu)=0",
            "current_result": "CONDITIONAL_REFERENCE_ONLY",
            "why_not_enough": "no parent-signed local stationary domain, no same-frame T_obs conservation, and no boundary-clock normalization",
            "if_closed": "source current conservation can be linked to a mass-current generator",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LGA1728_1_quasilocal_route",
            "route": "finite-boundary quasilocal route",
            "mathematical_form": "tau=N n+N^i e_i with fixed (N,N^i) on B and integrable H_tau",
            "current_result": "BOUNDARY_PHASE_SPACE_NOT_DECLARED",
            "why_not_enough": "fixed lapse/shift, boundary clock, symplectic form, and reference subtraction are not supplied by the current parent action",
            "if_closed": "compact local branch would not need asymptotic infinity to define the time generator",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LGA1728_2_asymptotic_route",
            "route": "asymptotic time route",
            "mathematical_form": "tau -> partial_t at infinity and H_tau -> ADM/Brown-York/Noether charge after matching",
            "current_result": "NOT_CURRENT_LOCAL_BRANCH_SOURCE",
            "why_not_enough": "local branch under audit is compact/exterior-annulus based and lacks asymptotic data rows",
            "if_closed": "could define a comparator for isolated systems, not the present local certificate",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "attempt_id": "LGA1728_3_verdict",
            "route": "certificate verdict",
            "mathematical_form": "certificate := exact symmetry or fixed quasilocal lapse/shift plus clock normalization plus integrable H_tau",
            "current_result": "FAIL_CURRENT_CLAIM",
            "why_not_enough": "all viable routes are conditional templates, not sourced current-MTS certificates",
            "if_closed": "tau_obs selection and delta_tau zero route can reopen",
            "valid_for_claim": no(),
        },
    ]


def coefficient_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "DTC1728_0_C_Tobs_tau_primary",
            "quantity": "C_Tobs_tau",
            "definition": "operator coefficient converting moving tau into a source-current residual",
            "bound_form": "Delta_JH_delta_tau <= C_Tobs_tau * ||delta tau_obs||_B",
            "required_inputs": "system_id;A_ext;B_clock;tau_obs;T_obs_operator_norm;current_norm;delta_tau_norm;units;source_path",
            "current_status": "FIRST_COEFFICIENT_ROW_TEMPLATE",
            "missing_inputs": "MISSING_SYSTEM_ID;MISSING_A_EXT;MISSING_B_CLOCK;MISSING_TAU_OBS;MISSING_TOBS_OPERATOR_NORM;MISSING_CURRENT_NORM;MISSING_DELTA_TAU_NORM;MISSING_UNITS",
            "source_paths": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1727_DELTA_TAU_FIRST_RESIDUAL_ROW.csv") + ";" + str(RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv"),
            "numeric_value": "MISSING_C_TOBS_TAU",
            "units": "current_norm_per_tau_norm_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "DTC1728_1_C_Htau",
            "quantity": "C_Htau",
            "definition": "operator coefficient converting moving tau into a Hamiltonian-charge residual",
            "bound_form": "Delta_H_delta_tau/M_H_ref <= C_Htau * ||delta tau_obs||_B + Delta_ref/M_H_ref + Delta_symp/M_H_ref",
            "required_inputs": "system_id;Q_tau;theta;H_ref;M_H_ref;delta_tau_norm;units;source_path",
            "current_status": "COEFFICIENT_ROW_TEMPLATE",
            "missing_inputs": "MISSING_Q_TAU;MISSING_THETA;MISSING_H_REF;MISSING_M_H_REF;MISSING_DELTA_REF;MISSING_DELTA_SYMP;MISSING_UNITS",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv") + ";" + str(RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv"),
            "numeric_value": "MISSING_C_HTAU",
            "units": "dimensionless_per_tau_norm_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "DTC1728_2_C_clock_tau",
            "quantity": "C_clock_tau",
            "definition": "coefficient converting moving tau into a clock-boundary normalization residual",
            "bound_form": "Delta_clock_boundary_tau <= C_clock_tau * ||delta tau_obs||_B + |kappa_alpha tau_clock_time|",
            "required_inputs": "clock_pair;B_clock;tau_obs;clock_sensitivity;chiX_dynamics;units;source_path",
            "current_status": "COEFFICIENT_ROW_TEMPLATE",
            "missing_inputs": "MISSING_CLOCK_NORMALIZATION;MISSING_CLOCK_SENSITIVITY;MISSING_CHIX_DYNAMICS;MISSING_DELTA_TAU_NORM;MISSING_UNITS",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv") + ";" + str(ROOT / "648-Y5-R10-clock-product-bound-runner-or-derive-local-chiX-dynamics.md"),
            "numeric_value": "MISSING_C_CLOCK_TAU",
            "units": "fractional_clock_shift_per_tau_norm_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "coefficient_id": "DTC1728_3_total_coefficient_stack",
            "quantity": "C_delta_tau_total",
            "definition": "total conservative coefficient stack for epsilon_delta_tau propagation",
            "bound_form": "epsilon_delta_tau_effect <= (C_Tobs_tau+C_Htau+C_clock_tau+C_orbit_tau+C_WEP_tau) * ||delta tau_obs||",
            "required_inputs": "all sector coefficients;common tau norm;common units;source paths",
            "current_status": "TOTAL_COEFFICIENT_STACK_TEMPLATE",
            "missing_inputs": "MISSING_SECTOR_COEFFICIENTS;MISSING_COMMON_NORM;MISSING_COMMON_UNITS;MISSING_NUMERIC_VALUES",
            "source_paths": str(OUTPUTS["coefficient_rows"]),
            "numeric_value": "MISSING_C_DELTA_TAU_TOTAL",
            "units": "dimensionless_after_common_normalization_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
            "claim_allowed": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1728_0_generator_certificate",
            "quantity": "local stationary/Killing/quasilocal generator certificate",
            "runner_decision": "CONDITIONAL_ONLY_REFUSE_CLAIM",
            "refusal_reasons": "MISSING_STATIONARY_CERTIFICATE;MISSING_QUASILOCAL_LAPSE_SHIFT;MISSING_BOUNDARY_CLOCK_NORMALIZATION;MISSING_EH_EXTERIOR_COMPATIBILITY;MISSING_INTEGRABILITY_REFERENCE_LOCK",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1728_1_delta_tau_coefficients",
            "quantity": "delta_tau bound coefficient rows",
            "runner_decision": "ACCEPT_SCHEMA_REFUSE_SCORING",
            "refusal_reasons": "COEFFICIENT_ROWS_HAVE_MISSING_INPUTS_AND_VALID_FOR_CLAIM_FALSE",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1728_2_delta_tau_bound",
            "quantity": "epsilon_delta_tau bound",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "NO_DELTA_TAU_VALUE;NO_C_TOBS_TAU;NO_C_HTAU;NO_COMMON_NORM;NO_UNITS",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1728_3_MHref_JH_Ndomain",
            "quantity": "M_H_ref/J_H/N_domain reopening",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "NO_GENERATOR_CERTIFICATE;NO_DELTA_TAU_BOUND;NO_M_H_REF;NO_COMMON_NORM_OWNER",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1728_4_Newton_local_GR",
            "quantity": "Newton/local-GR reduction",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "TAU_GENERATOR_NOT_CERTIFIED;SOURCE_NORMALIZATION_DENOMINATOR_MISSING;NDOMAIN_MISSING;PPN_VECTOR_OPEN",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1728_0_certificate_verdict",
            "decision": "generator certificate not claimed",
            "because": "stationary, quasilocal, and asymptotic routes are all conditional templates without current-MTS source certificates",
            "next_action": "do not promote tau_obs or delta_tau zero from the generator route",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1728_1_first_coefficient",
            "decision": "open C_Tobs_tau first",
            "because": "the immediate mathematical leak from moving tau is star(T_obs(delta tau,.)) in the source-current norm",
            "next_action": "source or bound T_obs_operator_norm on the same A_ext/tau/norm owner before C_Htau",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1728_2_best_next",
            "decision": "target T_obs operator norm before Hamiltonian coefficient",
            "because": "C_Htau still needs theta/Q_tau/H_ref/M_H_ref, while C_Tobs_tau can be tied to the existing J_H norm row if the common norm owner is filled",
            "next_action": "1729 should fill or bound C_Tobs_tau, or prove T_obs(delta tau) is silent",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1728_0_primary",
            "next_target": "1729-Y5-R2FR-Tobs-delta-tau-operator-norm-or-source-current-silence.md",
            "script": "scripts/Y5_R2FR_Tobs_delta_tau_operator_norm_or_source_current_silence.py",
            "objective": "fill/source C_Tobs_tau for Delta_JH_delta_tau, or prove the source-current moving-tau term is zero in the parent variation class",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1728_1_parallel_Htau_coefficient",
            "next_target": "1729b-Y5-R2FR-Htau-delta-tau-coefficient-or-integrability-lock.md",
            "script": "scripts/Y5_R2FR_Htau_delta_tau_coefficient_or_integrability_lock.py",
            "objective": "source C_Htau or derive the Hamiltonian fixed-generator/integrability lock",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1728_2_later_stationary_data",
            "next_target": "1730-Y5-R2FR-stationary-quasilocal-data-intake.md",
            "script": "scripts/Y5_R2FR_stationary_quasilocal_data_intake.py",
            "objective": "if external/local system data exist, add stationary/quasilocal certificate rows without using orbital GM as proof",
            "selection_status": "later",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1728_0_generator_certificate",
            "claim": "local stationary/Killing/quasilocal generator is certified",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "LGC1728_7 verdict says certificate is not signed",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1728_1_delta_tau_coefficients",
            "claim": "delta_tau coefficients are source-backed",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "coefficient rows are templates with missing norms, values and units",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1728_2_epsilon_delta_tau",
            "claim": "epsilon_delta_tau is bounded or theorem-zero",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "delta_tau value and propagation coefficients are missing",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1728_3_MHref_JH_Ndomain",
            "claim": "M_H_ref/J_H/N_domain can reopen",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "generator certificate and delta_tau bound remain open",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1728_4_Newton_local_GR",
            "claim": "Newton/local-GR reduction is derived",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "fixed tau, source-normalization denominator, N_domain and PPN residual vector remain open",
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "certificate_audit": certificate_audit_rows(),
        "certificate_attempt": certificate_attempt_rows(),
        "coefficient_rows": coefficient_rows(),
        "runner_refusal": runner_refusal_rows(),
        "decision": decision_rows(),
        "next_target": next_target_rows(),
        "claim_gate": claim_gate_rows(),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames = list(rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def markdown_table(rows: list[dict[str, Any]], columns: list[str]) -> str:
    def cell(value: Any) -> str:
        return str(value).replace("\n", " ").replace("|", "\\|")

    lines = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(cell(row.get(column, "")) for column in columns) + " |")
    return "\n".join(lines)


def cleanup_pycache() -> None:
    pycache = ROOT / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)


def copy_outputs() -> None:
    MICROSCOPE_RESIDUALS.mkdir(parents=True, exist_ok=True)
    QUARANTINE.mkdir(parents=True, exist_ok=True)
    RAB_QUEUE.mkdir(parents=True, exist_ok=True)
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1728_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1728_{key.upper()}.csv")


def generated_csv_paths() -> list[Path]:
    return [path for key, path in OUTPUTS.items() if key != "validation"]


def no_claim_flags(rows_map: dict[str, list[dict[str, Any]]]) -> bool:
    flag_fields = {"valid_for_claim", "claim_allowed", "score_ready", "accepted_for_scoring"}
    for rows in rows_map.values():
        for row in rows:
            for key, value in row.items():
                if key in flag_fields and str(value).lower() != "false":
                    return False
    return True


def branch_copies_exist() -> bool:
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1728_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1728_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1728*"):
        text = str(path)
        if "\\.venv\\" in text or "\\__pycache__\\" in text:
            continue
        if path.is_file():
            return False
    return True


def coefficient_rows_have_missing(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        combined = ";".join(str(value) for value in row.values())
        if "MISSING_" not in combined:
            return False
        if row.get("valid_for_claim") != "False" or row.get("claim_allowed") != "False":
            return False
    return True


def build_validation(rows_map: dict[str, list[dict[str, Any]]]) -> list[dict[str, Any]]:
    def check(check_id: str, result: bool, detail_pass: str, detail_fail: str) -> dict[str, Any]:
        return {
            "branch_id": BRANCH_ID,
            "check_id": check_id,
            "result": "PASS" if result else "FAIL",
            "detail": detail_pass if result else detail_fail,
        }

    source_register = rows_map["source_register"]
    audit = rows_map["certificate_audit"]
    attempt = rows_map["certificate_attempt"]
    coefficients = rows_map["coefficient_rows"]
    refusals = rows_map["runner_refusal"]
    decisions = rows_map["decision"]
    next_rows = rows_map["next_target"]
    claim_rows = rows_map["claim_gate"]

    parsed_ok = True
    try:
        for path in generated_csv_paths():
            read_csv(path)
    except Exception:
        parsed_ok = False

    validation = [
        check("VAL1728_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1728_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1728_2_1727_handoff_preserved",
            any(row["source_key"] == "1727_next_target" and row["needles_present"] == "True" for row in source_register),
            "1727 selected local generator certificate route",
            "1727 handoff missing",
        ),
        check(
            "VAL1728_3_certificate_audit_complete",
            {row["certificate_clause"] for row in audit} >= {"stationary Killing generator", "quasilocal lapse/shift generator", "asymptotic time fallback", "EH/exterior constraint compatibility", "integrable boundary charge", "no lapse rescaling", "same-frame source/clock compatibility"},
            "certificate audit covers stationary, quasilocal, asymptotic, EH, integrability, rescaling and same-frame clauses",
            "certificate audit missing required clause",
        ),
        check(
            "VAL1728_4_certificate_verdict_blocked",
            any(row["audit_id"] == "LGC1728_7_verdict" and row["current_status"] == "LOCAL_GENERATOR_CERTIFICATE_NOT_SIGNED" for row in audit),
            "local generator certificate remains unsigned",
            "certificate verdict missing or opened",
        ),
        check(
            "VAL1728_5_attempt_fails_current_claim",
            any(row["attempt_id"] == "LGA1728_3_verdict" and row["current_result"] == "FAIL_CURRENT_CLAIM" for row in attempt),
            "certificate attempt explicitly fails current claim",
            "certificate attempt did not retain fail-current-claim verdict",
        ),
        check(
            "VAL1728_6_coefficients_nonclaim",
            len(coefficients) == 4 and coefficient_rows_have_missing(coefficients),
            "delta_tau coefficient rows remain nonclaim and carry missing markers",
            "coefficient rows are incomplete or claim-enabled",
        ),
        check(
            "VAL1728_7_primary_coefficient_C_Tobs",
            any(row["coefficient_id"] == "DTC1728_0_C_Tobs_tau_primary" and row["quantity"] == "C_Tobs_tau" for row in coefficients),
            "primary C_Tobs_tau coefficient row is present",
            "primary C_Tobs_tau coefficient row missing",
        ),
        check(
            "VAL1728_8_runner_refusals_cover_chain",
            {row["quantity"] for row in refusals} >= {"local stationary/Killing/quasilocal generator certificate", "delta_tau bound coefficient rows", "epsilon_delta_tau bound", "Newton/local-GR reduction"},
            "runner refusals cover certificate, coefficients, epsilon_delta_tau and Newton/local-GR",
            "runner refusals do not cover the full chain",
        ),
        check(
            "VAL1728_9_decision_next",
            any(row["decision_id"] == "DEC1728_2_best_next" and "T_obs operator norm" in row["decision"] for row in decisions),
            "decision selects T_obs operator norm next",
            "decision does not select T_obs operator norm",
        ),
        check(
            "VAL1728_10_next_selected",
            any(row["route_id"] == "NEXT1728_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target row selects 1729 primary route",
            "next target missing selected primary route",
        ),
        check(
            "VAL1728_11_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1728_12_csv_parse", parsed_ok, "all generated 1728 CSVs parse", "one or more generated 1728 CSVs failed to parse"),
        check("VAL1728_13_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1728_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1728_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1728_16_formalization_untouched", formalization_untouched(), "no 1728 outputs found under formalization-workbench", "1728 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1728_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1728 local generator certificate validation" if overall else "one or more 1728 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1728 tries the selected local stationary/Killing/quasilocal generator certificate route.",
        "- Current result: the certificate is **not signed**. The corpus has the right GR-like routes, but no current-MTS stationary domain, quasilocal lapse/shift, boundary clock normalization, EH/exterior compatibility, integrability, or same-frame certificate.",
        "- The fallback is now more useful: the first concrete coefficient row is `C_Tobs_tau`, the operator norm converting a moving `tau` into a source-current residual.",
        "- This is the cleanest next finite branch because `star(T_obs(delta tau,.))` is the immediate leakage term in `J_H[tau]`.",
        "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, fixed-`tau`, `M_H_ref`, `J_H_total`, `N_domain`, or source-normalization claim is made.",
        "",
        "## Conditional Generator Certificate",
        "If the local exterior admits a future-directed stationary Killing field, or a parent-fixed quasilocal lapse/shift generator, normalized by boundary clocks and compatible with the same observed coframe, EH/exterior constraints, and an integrable boundary charge, then `tau_obs` can be more than a label. Current MTS has this as a conditional route only, so `delta_tau` remains a retained residual.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Certificate Audit",
        markdown_table(rows_map["certificate_audit"], ["audit_id", "certificate_clause", "current_status", "blocking_gap", "derivation_ready", "valid_for_claim"]),
        "",
        "## Certificate Attempt",
        markdown_table(rows_map["certificate_attempt"], ["attempt_id", "route", "current_result", "why_not_enough", "if_closed", "valid_for_claim"]),
        "",
        "## Delta Tau Coefficient Rows",
        markdown_table(rows_map["coefficient_rows"], ["coefficient_id", "quantity", "current_status", "missing_inputs", "numeric_value", "units", "score_ready", "valid_for_claim"]),
        "",
        "## Runner Refusal",
        markdown_table(rows_map["runner_refusal"], ["run_id", "quantity", "runner_decision", "refusal_reasons", "accepted_for_scoring", "claim_allowed"]),
        "",
        "## Decision Ledger",
        markdown_table(rows_map["decision"], ["decision_id", "decision", "because", "next_action"]),
        "",
        "## Next Target",
        markdown_table(rows_map["next_target"], ["route_id", "next_target", "script", "objective", "selection_status"]),
        "",
        "## Claim Gates",
        markdown_table(rows_map["claim_gate"], ["claim_id", "claim", "status", "reason"]),
        "",
        "## Validation",
        markdown_table(validation_rows, ["check_id", "result", "detail"]),
        "",
        "## Working Interpretation",
        "1728 is a useful fork. The elegant route would be a real stationary/quasilocal certificate for `tau_obs`; we do not have it. The practical route is therefore to start pricing the damage from `delta_tau`. The first bill is `C_Tobs_tau`, because a moving time generator contaminates the source current before it ever reaches `M_H_ref`, `N_domain`, or PPN. That is the best next small target: either source/bound the operator norm, or prove the moving-tau source-current term is silent.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    rows_map = rows_by_key()
    for key, rows in rows_map.items():
        write_csv(OUTPUTS[key], rows)
    copy_outputs()
    cleanup_pycache()
    validation_rows = build_validation(rows_map)
    write_csv(OUTPUTS["validation"], validation_rows)
    doc_path = ROOT / "1728-Y5-R2FR-local-stationary-quasilocal-generator-certificate-or-delta-tau-bound-coefficient.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1728_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1728 validation FAIL")
    print("1728 validation PASS")


if __name__ == "__main__":
    main()
