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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1726"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1726 - Observed Time Generator Fixed Variation Or Rtau Residual Bound"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1726_0_1725_doc",
        "source_key": "1725_doc",
        "source_path": ROOT / "1725-Y5-R2FR-tau-source-normal-lock-or-explicit-finite-input-row.md",
        "needles": ["NEXT1725_0_primary", "delta tau_obs=0"],
    },
    {
        "source_id": "SRC1726_1_1725_next",
        "source_key": "1725_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1725_NEXT_TARGET.csv",
        "needles": ["1726-Y5-R2FR-observed-time-generator-fixed-variation-or-Rtau-residual-bound.md", "selected"],
    },
    {
        "source_id": "SRC1726_2_1725_rescaling_guard",
        "source_key": "1725_rescaling_guard",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1725_NO_LAPSE_RESCALING_GUARD.csv",
        "needles": ["NLR1725_4_verdict", "NO_LAPSE_RESCALING_GUARD_ACTIVE"],
    },
    {
        "source_id": "SRC1726_3_1725_validation",
        "source_key": "1725_validation",
        "source_path": RESIDUALS / "P8_Y5_BRR545_1725_VALIDATION.csv",
        "needles": ["VAL1725_OVERALL", "PASS"],
    },
    {
        "source_id": "SRC1726_4_685_killing_clock",
        "source_key": "685_killing_clock_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_685_KILLING_CLOCK_GATE.csv",
        "needles": ["KCG685_0_observed_vector", "MISSING_PARENT_SELECTED_TAU_OBS"],
    },
    {
        "source_id": "SRC1726_5_685_tau_contract",
        "source_key": "685_tau_generator_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
        "needles": ["TGC685_0_define_tau_obs", "definition_target_only"],
    },
    {
        "source_id": "SRC1726_6_684_tau_audit",
        "source_key": "684_tau_generator_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
        "needles": ["TGA684_6_total", "NO_PARENT_SIGNED_TAU_LOCK"],
    },
    {
        "source_id": "SRC1726_7_684_frame_lock",
        "source_key": "684_frame_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv",
        "needles": ["FLC684_1_tau_from_observed_frame", "tau_lock_not_parent_signed"],
    },
    {
        "source_id": "SRC1726_8_664_integrability",
        "source_key": "664_integrability",
        "source_path": RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
        "needles": ["HCI664_4_time_generator_lock", "delta tau=0"],
    },
    {
        "source_id": "SRC1726_9_457_hamiltonian_doc",
        "source_key": "457_hamiltonian_doc",
        "source_path": ROOT / "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "needles": ["observed_time_generator", "not_parent_derived"],
    },
    {
        "source_id": "SRC1726_10_hamiltonian_charge",
        "source_key": "hamiltonian_boundary_charge",
        "source_path": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "needles": ["HC1_observed_time_generator", "not_parent_derived"],
    },
    {
        "source_id": "SRC1726_11_same_coframe",
        "source_key": "same_coframe_parent_clause",
        "source_path": RESIDUALS / "P8_Y5_SAME_COFRAME_PARENT_CLAUSE.csv",
        "needles": ["UOC519_2_readout_uses_same_e", "conditional_clause_written_not_current_MTS_derived"],
    },
    {
        "source_id": "SRC1726_12_parent_clause",
        "source_key": "662_parent_clause_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_662_PARENT_CLAUSE_AUDIT.csv",
        "needles": ["CL662_1_same_observed_source_frame", "not_yet_derived"],
    },
    {
        "source_id": "SRC1726_13_662_doc",
        "source_key": "662_doc",
        "source_path": ROOT / "662-Y5-R10-Hilbert-worldtube-source-measure-glue-or-equality-residual-bound.md",
        "needles": ["P662_1_observed_source_current", "same_frame_measure_unsigned"],
    },
    {
        "source_id": "SRC1726_14_647_tau_clock",
        "source_key": "647_tau_clock_map",
        "source_path": RESIDUALS / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv",
        "needles": ["TAU647_0_time_drift", "defined_product_map"],
    },
    {
        "source_id": "SRC1726_15_648_clock_doc",
        "source_key": "648_clock_doc",
        "source_path": ROOT / "648-Y5-R10-clock-product-bound-runner-or-derive-local-chiX-dynamics.md",
        "needles": ["tau_clock", "not derived"],
    },
    {
        "source_id": "SRC1726_16_boundary_ref",
        "source_key": "boundary_reference_first_row",
        "source_path": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
        "needles": ["M_H_ref", "missing_claim_valid_source_or_zero_theorem"],
    },
    {
        "source_id": "SRC1726_17_1720_jh_row",
        "source_key": "1720_jh_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv",
        "needles": ["JHN1720_0_observed_Hilbert_current_norm_candidate", "MISSING_PARENT_SIGNED_TAU_OBS"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_SOURCE_REGISTER.csv",
    "observed_generator": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_OBSERVED_TIME_GENERATOR_AUDIT.csv",
    "fixed_variation": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_FIXED_VARIATION_AUDIT.csv",
    "residual_schema": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_RTAU_RESIDUAL_BOUND_SCHEMA.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1726_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1726_VALIDATION.csv",
}


COPY_MAP = {
    "observed_generator": "R2FR_1726_OBSERVED_TIME_GENERATOR_AUDIT.csv",
    "fixed_variation": "R2FR_1726_FIXED_VARIATION_AUDIT.csv",
    "residual_schema": "R2FR_1726_RTAU_RESIDUAL_BOUND_SCHEMA.csv",
    "runner_refusal": "R2FR_1726_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1726_DECISION_LEDGER.csv",
    "next_target": "R2FR_1726_NEXT_TARGET.csv",
    "claim_gate": "R2FR_1726_CLAIM_GATE.csv",
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


def observed_generator_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OTG1726_0_parent_data",
            "clause": "parent branch data",
            "candidate_statement": "A parent local branch supplies e_obs, a time orientation, a boundary/clock class, and admissible exterior domain before source or orbit readout.",
            "mathematical_form": "B_local=(M_local,e_obs,B_clock,B_ref,orientation,domain_class)",
            "current_status": "PARENT_BRANCH_DATA_INCOMPLETE",
            "blocking_gap": "boundary clock class and reference class are not parent-signed for current MTS",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OTG1726_1_stationary_or_quasilocal_flow",
            "clause": "stationary/quasilocal generator",
            "candidate_statement": "tau_obs is a stationary Killing field where available, or an admissible quasilocal time-flow fixed by boundary lapse/shift data.",
            "mathematical_form": "L_tau g_obs=0 in stationary exterior, or (N,N^i)|_B fixed with tau_obs=N n + N^i e_i",
            "current_status": "MISSING_LOCAL_STATIONARY_OR_QUASILOCAL_CERTIFICATE",
            "blocking_gap": "KCG685_1 and HC1 record the route but not the current-branch certificate",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OTG1726_2_boundary_clock_normalization",
            "clause": "clock normalization",
            "candidate_statement": "tau_obs is normalized by the same boundary/local clocks used for redshift and clock-comparison readouts.",
            "mathematical_form": "g_obs(tau_obs,tau_obs)|_{B_clock}=-1 or N_B[e_obs,tau_obs]=1",
            "current_status": "MISSING_BOUNDARY_CLOCK_NORMALIZATION_THEOREM",
            "blocking_gap": "647/648 provide clock product maps and bounds but not a Hamiltonian generator normalization theorem",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OTG1726_3_uniqueness_mod_gauge",
            "clause": "uniqueness against lapse rescaling",
            "candidate_statement": "the parent boundary/clock rule fixes the homogeneous rescaling tau -> f tau, so f is not chosen sector-by-sector.",
            "mathematical_form": "if tau' = f tau and N_B[tau']=N_B[tau]=1, then f|_{B_clock}=1 and interior extension is fixed by the parent gauge condition",
            "current_status": "NO_LAPSE_GUARD_ONLY_NO_SELECTION",
            "blocking_gap": "1725 kills rescaling shortcuts but does not construct the unique parent extension of tau_obs",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OTG1726_4_same_frame_compatibility",
            "clause": "same coframe compatibility",
            "candidate_statement": "the same e_obs and tau_obs define clocks, rods, photons, source current, Hamiltonian charge and slow-orbit readout.",
            "mathematical_form": "e_source=e_clock=e_photon=e_orbit=e_obs and J_H[tau_obs]=star(T_obs(tau_obs,.))",
            "current_status": "SAME_FRAME_CONDITIONAL_NOT_CORPUS_PROVED",
            "blocking_gap": "UOC519 and CL662 clauses are written but not current-MTS derived",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OTG1726_5_source_independent_selection",
            "clause": "pre-readout selection",
            "candidate_statement": "tau_obs is selected before source mass, orbital GM, WEP readout or R10 fitting, so it cannot absorb residuals.",
            "mathematical_form": "partial_{GM_orbit,Qbar,WEP,R10} tau_obs = 0",
            "current_status": "PRE_READOUT_SELECTION_NOT_SIGNED",
            "blocking_gap": "no parent proof excludes post-readout tau choices except the 1725 guardrail",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "OTG1726_6_verdict",
            "clause": "observed time generator verdict",
            "candidate_statement": "the current corpus has a clean definition target for tau_obs but not a parent-selected observed time generator.",
            "mathematical_form": "tau_obs remains MISSING_PARENT_SELECTED_TAU_OBS",
            "current_status": "OBSERVED_TIME_GENERATOR_NOT_PARENT_SELECTED",
            "blocking_gap": "stationary/quasilocal certificate, boundary clock normalization, unique gauge extension and same-frame proof are missing",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
    ]


def fixed_variation_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "FVA1726_0_variation_domain",
            "variation_clause": "allowed phase-space variation",
            "candidate_identity": "variations act on interior dynamical fields while boundary clock/reference data and tau_obs are held fixed.",
            "mathematical_form": "delta in T_phi P with delta B_clock=delta B_ref=0 and delta tau_obs=0",
            "current_status": "VARIATION_DOMAIN_NOT_PARENT_DECLARED",
            "open_term_if_missing": "delta B_clock; delta B_ref; delta tau_obs",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "FVA1726_1_source_variation",
            "variation_clause": "source current variation",
            "candidate_identity": "J_H[tau_obs] varies only through T_obs, not through the readout vector.",
            "mathematical_form": "delta J_H[tau]=star(delta T_obs(tau,.)) + star(T_obs(delta tau,.)); require delta tau=0",
            "current_status": "DELTA_TAU_SOURCE_TERM_NOT_ZEROED",
            "open_term_if_missing": "star(T_obs(delta tau,.))",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "FVA1726_2_hamiltonian_variation",
            "variation_clause": "Hamiltonian variation",
            "candidate_identity": "H_tau is varied at fixed generator and fixed reference subtraction.",
            "mathematical_form": "delta H_tau = int_S(delta Q_tau - i_tau theta) with delta tau=0 and delta H_ref=0",
            "current_status": "DELTA_TAU_HAMILTONIAN_TERM_NOT_ZEROED",
            "open_term_if_missing": "H_delta_tau; delta H_ref; Delta_symp",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "FVA1726_3_clock_variation",
            "variation_clause": "clock normalization variation",
            "candidate_identity": "the clock normalization condition remains fixed under allowed source/field variations.",
            "mathematical_form": "delta(g_obs(tau_obs,tau_obs)|_B)=0 with delta tau_obs=0 and fixed boundary clock standard",
            "current_status": "CLOCK_VARIATION_CLASS_NOT_SIGNED",
            "open_term_if_missing": "delta N_B; delta clock standard; delta tau_clock",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "FVA1726_4_reference_variation",
            "variation_clause": "boundary/reference variation",
            "candidate_identity": "H_ref and boundary counterterms are fixed once and cannot absorb source, radius, time, frame or readout changes.",
            "mathematical_form": "partial_source H_ref=partial_r H_ref=partial_t H_ref=partial_frame H_ref=0",
            "current_status": "REFERENCE_VARIATION_LOCK_OPEN",
            "open_term_if_missing": "Delta_ref; B_zero_flux; H_ref_shift",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "FVA1726_5_fixed_variation_verdict",
            "variation_clause": "fixed tau verdict",
            "candidate_identity": "delta tau_obs=0 is an exact requirement, not a convention; current MTS has not signed it.",
            "mathematical_form": "delta tau_obs=0 remains conditional; R_delta_tau retained",
            "current_status": "FIXED_VARIATION_NOT_PARENT_SIGNED",
            "open_term_if_missing": "R_delta_tau",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
    ]


def residual_schema_rows() -> list[dict[str, Any]]:
    source_bundle = ";".join(str(source["source_path"]) for source in SOURCES)
    return [
        {
            "branch_id": BRANCH_ID,
            "schema_id": "RTAU1726_0_vector_schema",
            "quantity": "R_tau_frame",
            "bound_form": "R_tau_frame={tau_source-tau_obs,tau_charge-tau_obs,tau_clock-tau_obs,tau_boundary-tau_obs,tau_orbit-tau_obs,tau_WEP-tau_obs,delta tau_obs}",
            "required_inputs": "system_id;sector_tau_values;tau_obs;norm_type;boundary_clock;source_normal;units;source_path",
            "current_status": "SCHEMA_ONLY_NOT_SCORE_READY",
            "missing_inputs": "MISSING_TAU_OBS;MISSING_SECTOR_TAU_VALUES;MISSING_NORM_TYPE;MISSING_UNITS;MISSING_SOURCE_PATHS_FOR_VALUES",
            "source_paths": source_bundle,
            "numeric_value": "MISSING_RESIDUAL_VECTOR",
            "units": "dimensionless_or_time_normalized_after_norm_declared",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "schema_id": "RTAU1726_1_source_current_bound",
            "quantity": "Delta_JH_tau",
            "bound_form": "||J_H[tau_source]-J_H[tau_obs]||_A <= ||T_obs||_{A,op} ||tau_source-tau_obs||_A",
            "required_inputs": "T_obs_operator_norm;A_ext;tau_source;tau_obs;current_norm;units",
            "current_status": "BOUND_FORM_ONLY",
            "missing_inputs": "MISSING_TOBS_OPERATOR_NORM;MISSING_A_EXT;MISSING_TAU_SOURCE;MISSING_TAU_OBS;MISSING_NORM_UNITS",
            "source_paths": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv"),
            "numeric_value": "MISSING_SOURCE_CURRENT_BOUND",
            "units": "current_norm_units_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "schema_id": "RTAU1726_2_hamiltonian_bound",
            "quantity": "Delta_H_tau",
            "bound_form": "|H_{tau_charge}-H_{tau_obs}|/M_H_ref <= C_Htau ||tau_charge-tau_obs|| + |Delta_ref|/M_H_ref + |Delta_symp|/M_H_ref",
            "required_inputs": "C_Htau;tau_charge;tau_obs;M_H_ref;Delta_ref;Delta_symp;units",
            "current_status": "BOUND_FORM_ONLY",
            "missing_inputs": "MISSING_C_HTAU;MISSING_M_H_REF;MISSING_DELTA_REF;MISSING_DELTA_SYMP;MISSING_TAU_VALUES",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv") + ";" + str(RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv"),
            "numeric_value": "MISSING_HAMILTONIAN_TAU_BOUND",
            "units": "dimensionless_after_M_H_ref_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "schema_id": "RTAU1726_3_clock_bound",
            "quantity": "Delta_clock_tau",
            "bound_form": "|Delta ln nu_clock| <= C_clock ||tau_clock-tau_obs|| + |kappa_alpha tau_clock_time| if chi_X drift remains independent",
            "required_inputs": "C_clock;tau_clock;tau_obs;clock_pair;chiX_dynamics;units",
            "current_status": "BOUND_FORM_ONLY",
            "missing_inputs": "MISSING_CLOCK_NORMALIZATION;MISSING_C_CLOCK;MISSING_TAU_CLOCK;MISSING_TAU_OBS;MISSING_CHIX_DYNAMICS",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv") + ";" + str(ROOT / "648-Y5-R10-clock-product-bound-runner-or-derive-local-chiX-dynamics.md"),
            "numeric_value": "MISSING_CLOCK_TAU_BOUND",
            "units": "clock_fractional_or_time_units_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "schema_id": "RTAU1726_4_orbit_bound",
            "quantity": "Delta_orbit_tau",
            "bound_form": "|Delta a/a| <= C_orbit ||tau_orbit-tau_obs|| + epsilon_Poisson_Gauss + epsilon_Gdot",
            "required_inputs": "C_orbit;tau_orbit;tau_obs;Poisson_Gauss_residual;Gdot_residual;units",
            "current_status": "BOUND_FORM_ONLY",
            "missing_inputs": "MISSING_ORBIT_BRIDGE;MISSING_C_ORBIT;MISSING_TAU_ORBIT;MISSING_POISSON_GAUSS_RESIDUAL;MISSING_GDOT_RESIDUAL",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv") + ";" + str(RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv"),
            "numeric_value": "MISSING_ORBIT_TAU_BOUND",
            "units": "dimensionless_fractional_acceleration_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "schema_id": "RTAU1726_5_wep_bound",
            "quantity": "Delta_tau_WEP",
            "bound_form": "|tau_WEP-tau_obs_projection| <= C_WEP ||readout_basis_tau - tau_obs|| + epsilon_CMSM_alignment",
            "required_inputs": "C_WEP;K_CMSM;source_worldtube;material_tensor;tau_obs_projection;units",
            "current_status": "BOUND_FORM_ONLY",
            "missing_inputs": "MISSING_K_CMSM;MISSING_SOURCE_WORLDTUBE;MISSING_MATERIAL_TENSOR;MISSING_ALIGNMENT;MISSING_TAU_OBS_PROJECTION",
            "source_paths": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1608_TAU_WEP_READOUT_CONTRACT.csv"),
            "numeric_value": "MISSING_WEP_TAU_BOUND",
            "units": "arena_projection_units_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "schema_id": "RTAU1726_6_total_bound",
            "quantity": "epsilon_tau_frame_total",
            "bound_form": "epsilon_tau_frame_total <= C_source e_source + C_H e_charge + C_clock e_clock + C_orbit e_orbit + C_WEP e_WEP + e_delta_tau",
            "required_inputs": "all sector constants;all sector residuals;common norm;M_H_ref;source paths;units",
            "current_status": "TOTAL_BOUND_TEMPLATE_ONLY",
            "missing_inputs": "MISSING_ALL_SECTOR_CONSTANTS;MISSING_COMMON_NORM;MISSING_M_H_REF;MISSING_NUMERIC_RESIDUALS",
            "source_paths": str(OUTPUTS["residual_schema"]),
            "numeric_value": "MISSING_TOTAL_RTAU_BOUND",
            "units": "dimensionless_after_common_normalization_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1726_0_observed_generator",
            "quantity": "tau_obs parent selection",
            "runner_decision": "CONDITIONAL_ONLY_REFUSE_CLAIM",
            "refusal_reasons": "MISSING_PARENT_BRANCH_DATA;MISSING_STATIONARY_OR_QUASILOCAL_CERTIFICATE;MISSING_BOUNDARY_CLOCK_NORMALIZATION;MISSING_UNIQUE_GAUGE_EXTENSION",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1726_1_fixed_variation",
            "quantity": "delta tau_obs=0 fixed-variation clause",
            "runner_decision": "CONDITIONAL_ONLY_REFUSE_CLAIM",
            "refusal_reasons": "MISSING_VARIATION_DOMAIN;MISSING_BOUNDARY_CLOCK_SUPERSELECTION;MISSING_REFERENCE_LOCK;MISSING_DELTA_TAU_ZERO_THEOREM",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1726_2_Rtau_bound_schema",
            "quantity": "R_tau_frame residual bound schema",
            "runner_decision": "ACCEPT_SCHEMA_REFUSE_SCORING",
            "refusal_reasons": "BOUND_FORMS_WRITTEN_BUT_ALL_NUMERIC_OR_THEOREM_ZERO_INPUTS_MISSING",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1726_3_MHref_JH_Ndomain",
            "quantity": "M_H_ref/J_H/N_domain reopening",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "NO_TAU_OBS_SELECTION;NO_FIXED_VARIATION;NO_RTAU_BOUND;COMMON_NORM_OWNER_STILL_BLOCKED",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1726_4_Newton_local_GR",
            "quantity": "Newton/local-GR reduction",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "TAU_GENERATOR_NOT_PARENT_SELECTED;M_H_REF_MISSING;JH_TOTAL_MISSING;NDOMAIN_MISSING;PPN_VECTOR_OPEN",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1726_0_observed_generator",
            "decision": "tau_obs remains a target, not a derived object",
            "because": "boundary clock normalization, stationary/quasilocal certificate, unique gauge extension and same-frame proof remain unsigned",
            "next_action": "do not use tau_obs as a theorem-zero object in source or Hamiltonian scoring",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1726_1_fixed_variation",
            "decision": "delta tau_obs=0 remains unsigned",
            "because": "the allowed phase-space variation has not been restricted by a parent boundary-clock/reference superselection class",
            "next_action": "attack boundary-clock superselection and fixed-variation domain first",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1726_2_residual_route",
            "decision": "R_tau_frame becomes the honest fallback",
            "because": "if tau_obs is not derived, source/charge/clock/orbit/WEP mismatches must be finite residuals with explicit constants and units",
            "next_action": "source or theorem-zero R_tau_frame before reopening M_H_ref, J_H_total, N_domain or PPN",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1726_0_primary",
            "next_target": "1727-Y5-R2FR-boundary-clock-superselection-or-delta-tau-residual-first-row.md",
            "script": "scripts/Y5_R2FR_boundary_clock_superselection_or_delta_tau_residual_first_row.py",
            "objective": "derive the boundary-clock/reference superselection class that fixes tau_obs and delta tau_obs=0, or write the first explicit delta-tau residual row",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1726_1_parallel_stationary_certificate",
            "next_target": "1727b-Y5-R2FR-local-stationary-quasilocal-generator-certificate.md",
            "script": "scripts/Y5_R2FR_local_stationary_quasilocal_generator_certificate.py",
            "objective": "try to source a local stationary/Killing or admissible quasilocal time-flow certificate without using orbital GM as input",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1726_2_later_numeric_Rtau",
            "next_target": "1728-Y5-R2FR-Rtau-frame-residual-numeric-bound-intake.md",
            "script": "scripts/Y5_R2FR_Rtau_frame_residual_numeric_bound_intake.py",
            "objective": "fill finite R_tau_frame constants and sector residuals if the theorem route fails",
            "selection_status": "later",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1726_0_tau_obs",
            "claim": "tau_obs is parent-selected",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "observed generator audit ends with OBSERVED_TIME_GENERATOR_NOT_PARENT_SELECTED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1726_1_delta_tau_zero",
            "claim": "delta tau_obs=0 in the allowed variation class",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "fixed-variation audit ends with FIXED_VARIATION_NOT_PARENT_SIGNED",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1726_2_Rtau_bound",
            "claim": "R_tau_frame is bounded or theorem-zero",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "residual schema has bound forms only and no numeric/theorem-zero inputs",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1726_3_MHref_common_norm",
            "claim": "M_H_ref and common norm owner can reopen",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "tau_obs selection, fixed variation and R_tau_frame remain open",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1726_4_Newton_local_GR",
            "claim": "Newton/local-GR reduction is derived",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "tau generator, source normalization, N_domain and PPN residual vector remain unclosed",
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "observed_generator": observed_generator_rows(),
        "fixed_variation": fixed_variation_rows(),
        "residual_schema": residual_schema_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1726_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1726_{key.upper()}.csv")


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
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1726_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1726_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1726*"):
        text = str(path)
        if "\\.venv\\" in text or "\\__pycache__\\" in text:
            continue
        if path.is_file():
            return False
    return True


def residual_rows_have_missing(rows: list[dict[str, Any]]) -> bool:
    for row in rows:
        combined = ";".join(str(value) for value in row.values())
        if "MISSING_" not in combined:
            return False
        if row.get("valid_for_claim") != "False":
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
    observed = rows_map["observed_generator"]
    fixed = rows_map["fixed_variation"]
    residual = rows_map["residual_schema"]
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
        check("VAL1726_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1726_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1726_2_1725_handoff_preserved",
            any(row["source_key"] == "1725_next_target" and row["needles_present"] == "True" for row in source_register),
            "1725 selected observed time-generator/fixed-variation route",
            "1725 handoff missing",
        ),
        check(
            "VAL1726_3_observed_generator_audit_complete",
            {row["clause"] for row in observed} >= {"parent branch data", "stationary/quasilocal generator", "clock normalization", "uniqueness against lapse rescaling", "same coframe compatibility", "pre-readout selection"},
            "observed generator audit covers parent data, stationarity, clock normalization, gauge uniqueness, same-frame and pre-readout clauses",
            "observed generator audit missing required clause",
        ),
        check(
            "VAL1726_4_observed_verdict_blocked",
            any(row["audit_id"] == "OTG1726_6_verdict" and row["current_status"] == "OBSERVED_TIME_GENERATOR_NOT_PARENT_SELECTED" for row in observed),
            "observed time generator remains not parent-selected",
            "observed generator verdict missing or opened",
        ),
        check(
            "VAL1726_5_fixed_variation_complete",
            {row["variation_clause"] for row in fixed} >= {"allowed phase-space variation", "source current variation", "Hamiltonian variation", "clock normalization variation", "boundary/reference variation", "fixed tau verdict"},
            "fixed-variation audit covers phase space, source, Hamiltonian, clock, reference and verdict clauses",
            "fixed-variation audit missing required clause",
        ),
        check(
            "VAL1726_6_fixed_variation_blocked",
            any(row["audit_id"] == "FVA1726_5_fixed_variation_verdict" and row["current_status"] == "FIXED_VARIATION_NOT_PARENT_SIGNED" for row in fixed),
            "delta tau_obs=0 remains unsigned",
            "fixed-variation verdict missing or opened",
        ),
        check(
            "VAL1726_7_residual_schema_nonclaim",
            len(residual) == 7 and residual_rows_have_missing(residual),
            "R_tau residual schema rows remain nonclaim and carry missing markers",
            "residual schema rows are incomplete or claim-enabled",
        ),
        check(
            "VAL1726_8_runner_refusals_cover_chain",
            {row["quantity"] for row in refusals} >= {"tau_obs parent selection", "delta tau_obs=0 fixed-variation clause", "R_tau_frame residual bound schema", "Newton/local-GR reduction"},
            "runner refusals cover tau selection, fixed variation, R_tau schema and Newton/local-GR",
            "runner refusals do not cover the full chain",
        ),
        check(
            "VAL1726_9_decision_next",
            any(row["decision_id"] == "DEC1726_1_fixed_variation" and "boundary-clock" in row["next_action"] for row in decisions),
            "decision selects boundary-clock superselection next",
            "decision does not select boundary-clock superselection",
        ),
        check(
            "VAL1726_10_next_selected",
            any(row["route_id"] == "NEXT1726_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target row selects 1727 primary route",
            "next target missing selected primary route",
        ),
        check(
            "VAL1726_11_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1726_12_csv_parse", parsed_ok, "all generated 1726 CSVs parse", "one or more generated 1726 CSVs failed to parse"),
        check("VAL1726_13_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1726_14_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1726_15_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1726_16_formalization_untouched", formalization_untouched(), "no 1726 outputs found under formalization-workbench", "1726 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1726_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1726 observed time generator/fixed variation validation" if overall else "one or more 1726 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1726 splits the tau problem into the two things that must be earned before the local branch can claim GR-like source normalization: parent selection of `tau_obs`, and the fixed-variation clause `delta tau_obs=0`.",
        "- Current result: neither is derived for current MTS. `tau_obs` remains a clean target object, not a parent-signed object.",
        "- The useful mathematical progress is that the fallback is now bound-shaped: if `tau_obs` is not derived, `R_tau_frame` must carry explicit source, charge, clock, boundary, orbit, WEP, and `delta tau` residuals.",
        "- This closes another loophole: a moving time generator cannot be quietly ignored inside `J_H`, `H_tau`, clocks, or orbital readout.",
        "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, `M_H_ref`, `J_H_total`, `N_domain`, or source-normalization claim is made.",
        "",
        "## Conditional Generator Theorem",
        "If a parent local branch supplies `e_obs`, a time orientation, a boundary/clock class, a reference class, a stationary or admissible quasilocal time-flow certificate, a clock normalization rule that fixes lapse rescaling, and a variation domain with fixed boundary data, then `tau_obs` is selected before readout and `delta tau_obs=0` in source and Hamiltonian variations. The present corpus has the theorem as a route, but not the certificates needed to use it as evidence.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Observed Time Generator Audit",
        markdown_table(rows_map["observed_generator"], ["audit_id", "clause", "current_status", "blocking_gap", "derivation_ready", "valid_for_claim"]),
        "",
        "## Fixed Variation Audit",
        markdown_table(rows_map["fixed_variation"], ["audit_id", "variation_clause", "current_status", "open_term_if_missing", "derivation_ready", "valid_for_claim"]),
        "",
        "## R Tau Residual Bound Schema",
        markdown_table(rows_map["residual_schema"], ["schema_id", "quantity", "current_status", "missing_inputs", "numeric_value", "units", "score_ready", "valid_for_claim"]),
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
        "1726 is another boring-looking but important lockpick. It says: no fixed observed time, no clean source current; no fixed variation, no clean Hamiltonian charge. The best next target is the boundary-clock/reference superselection class, because that is the smallest parent clause that could make `tau_obs` and `delta tau_obs=0` real rather than conventional. If that clause fails, we stop pretending and turn `R_tau_frame` into a finite empirical residual branch.",
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
    doc_path = ROOT / "1726-Y5-R2FR-observed-time-generator-fixed-variation-or-Rtau-residual-bound.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1726_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1726 validation FAIL")
    print("1726 validation PASS")


if __name__ == "__main__":
    main()
