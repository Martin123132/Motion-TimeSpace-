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
QUARANTINE = ROOT / "source-intake" / "microscope" / "quarantine" / "1725"
RAB_QUEUE = ROOT / "source-intake" / "rab-sector" / "acquisition-queue"
BRANCH_ID = "MTS_R10_WEP_RAB_FINITE_SOURCE_BRANCH_1428"
TITLE = "1725 - Tau Source Normal Lock Or Explicit Finite Input Row"
UTC = datetime.now(timezone.utc).isoformat()


def no() -> str:
    return "False"


def yesno(value: bool) -> str:
    return "True" if value else "False"


SOURCES = [
    {
        "source_id": "SRC1725_0_1724_doc",
        "source_key": "1724_doc",
        "source_path": ROOT / "1724-Y5-R2FR-compact-annulus-norm-tau-owner-or-first-source-row.md",
        "needles": ["NEXT1724_0_primary", "tau/source-normal lock"],
    },
    {
        "source_id": "SRC1725_1_1724_next",
        "source_key": "1724_next_target",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1724_NEXT_TARGET.csv",
        "needles": ["1725-Y5-R2FR-tau-source-normal-lock-or-explicit-finite-input-row.md", "selected"],
    },
    {
        "source_id": "SRC1725_2_684_doc",
        "source_key": "684_doc",
        "source_path": ROOT / "684-Y5-R10-observed-frame-tau-coframe-lock-for-MH-ref.md",
        "needles": ["tau_source = tau_charge = tau_clock = tau_orbit = tau_obs[e_obs]", "blocked_nonclaim"],
    },
    {
        "source_id": "SRC1725_3_684_frame_lock",
        "source_key": "684_frame_lock",
        "source_path": RESIDUALS / "P8_Y5_R10_684_FRAME_LOCK_CONTRACT.csv",
        "needles": ["FLC684_1_tau_from_observed_frame", "tau_lock_not_parent_signed"],
    },
    {
        "source_id": "SRC1725_4_684_tau_audit",
        "source_key": "684_tau_generator_audit",
        "source_path": RESIDUALS / "P8_Y5_R10_684_TAU_GENERATOR_AUDIT.csv",
        "needles": ["TGA684_6_total", "NO_PARENT_SIGNED_TAU_LOCK"],
    },
    {
        "source_id": "SRC1725_5_685_contract",
        "source_key": "685_tau_generator_contract",
        "source_path": RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv",
        "needles": ["TGC685_6_verdict", "tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit=tau_obs"],
    },
    {
        "source_id": "SRC1725_6_685_killing_clock",
        "source_key": "685_killing_clock_gate",
        "source_path": RESIDUALS / "P8_Y5_R10_685_KILLING_CLOCK_GATE.csv",
        "needles": ["KCG685_7_total", "seven blocking gates remain open"],
    },
    {
        "source_id": "SRC1725_7_683_same_frame",
        "source_key": "683_same_frame_gm",
        "source_path": RESIDUALS / "P8_Y5_R10_683_SAME_FRAME_GM_GATE.csv",
        "needles": ["SFG683_0_tau_lock", "MISSING_SAME_OBSERVED_TIME_GENERATOR"],
    },
    {
        "source_id": "SRC1725_8_663_euler",
        "source_key": "663_euler_ward",
        "source_path": RESIDUALS / "P8_Y5_R10_663_EULER_WARD_CHAIN_RESULT.csv",
        "needles": ["EW663_1_Noether_current", "tau_source_readout_lock_still_open"],
    },
    {
        "source_id": "SRC1725_9_664_integrability",
        "source_key": "664_integrability",
        "source_path": RESIDUALS / "P8_Y5_R10_664_INTEGRABILITY_ATTEMPT.csv",
        "needles": ["HCI664_4_time_generator_lock", "same observed time/coframe branch is not parent-derived"],
    },
    {
        "source_id": "SRC1725_10_hamiltonian_source",
        "source_key": "hamiltonian_source_measure",
        "source_path": RESIDUALS / "P8_Y5_HAMILTONIAN_SOURCE_MEASURE_CONTRACT.csv",
        "needles": ["HSM541_1_integrable_charge", "not_derived_for_current_MTS"],
    },
    {
        "source_id": "SRC1725_11_hamiltonian_charge",
        "source_key": "hamiltonian_boundary_charge",
        "source_path": RESIDUALS / "P8_mass_current_Hamiltonian_boundary_charge_CONTRACT.csv",
        "needles": ["HC1_observed_time_generator", "not_parent_derived"],
    },
    {
        "source_id": "SRC1725_12_457_doc",
        "source_key": "457_doc",
        "source_path": ROOT / "457-mass-current-Hamiltonian-boundary-charge-attempt.md",
        "needles": ["Hamiltonian charge parent-derived", "fail"],
    },
    {
        "source_id": "SRC1725_13_647_tau_clock",
        "source_key": "647_tau_clock_map",
        "source_path": RESIDUALS / "P8_Y5_R10_647_TAU_CLOCK_MAP.csv",
        "needles": ["TAU647_0_time_drift", "defined_product_map"],
    },
    {
        "source_id": "SRC1725_14_648_clock",
        "source_key": "648_clock_product",
        "source_path": ROOT / "648-Y5-R10-clock-product-bound-runner-or-derive-local-chiX-dynamics.md",
        "needles": ["tau_clock", "not derived"],
    },
    {
        "source_id": "SRC1725_15_1608_tau_wep",
        "source_key": "1608_tau_wep",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1608_TAU_WEP_READOUT_CONTRACT.csv",
        "needles": ["TAU1608_4_verdict", "TAU_WEP_NOT_EVALUATED"],
    },
    {
        "source_id": "SRC1725_16_boundary_ref",
        "source_key": "boundary_reference_first_row",
        "source_path": RESIDUALS / "P8_Y5_BOUNDARY_REFERENCE_FIRST_ROW_STATUS.csv",
        "needles": ["M_H_ref", "missing_claim_valid_source_or_zero_theorem"],
    },
    {
        "source_id": "SRC1725_17_1720_jh_row",
        "source_key": "1720_jh_row",
        "source_path": RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv",
        "needles": ["JHN1720_0_observed_Hilbert_current_norm_candidate", "MISSING_PARENT_SIGNED_TAU_OBS"],
    },
]


OUTPUTS = {
    "source_register": RESIDUALS / "P8_Y5_PARENT_QLOC_1725_SOURCE_REGISTER.csv",
    "theorem_audit": RESIDUALS / "P8_Y5_PARENT_QLOC_1725_TAU_SOURCE_NORMAL_THEOREM_AUDIT.csv",
    "rescaling_guard": RESIDUALS / "P8_Y5_PARENT_QLOC_1725_NO_LAPSE_RESCALING_GUARD.csv",
    "input_rows": RESIDUALS / "P8_Y5_PARENT_QLOC_1725_EXPLICIT_FINITE_INPUT_ROWS.csv",
    "runner_refusal": RESIDUALS / "P8_Y5_PARENT_QLOC_1725_RUNNER_REFUSAL.csv",
    "decision": RESIDUALS / "P8_Y5_PARENT_QLOC_1725_DECISION_LEDGER.csv",
    "next_target": RESIDUALS / "P8_Y5_PARENT_QLOC_1725_NEXT_TARGET.csv",
    "claim_gate": RESIDUALS / "P8_Y5_PARENT_QLOC_1725_CLAIM_GATE.csv",
    "validation": RESIDUALS / "P8_Y5_BRR545_1725_VALIDATION.csv",
}


COPY_MAP = {
    "theorem_audit": "R2FR_1725_TAU_SOURCE_NORMAL_THEOREM_AUDIT.csv",
    "rescaling_guard": "R2FR_1725_NO_LAPSE_RESCALING_GUARD.csv",
    "input_rows": "R2FR_1725_EXPLICIT_FINITE_INPUT_ROWS.csv",
    "runner_refusal": "R2FR_1725_RUNNER_REFUSAL.csv",
    "decision": "R2FR_1725_DECISION_LEDGER.csv",
    "next_target": "R2FR_1725_NEXT_TARGET.csv",
    "claim_gate": "R2FR_1725_CLAIM_GATE.csv",
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


def theorem_audit_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSL1725_0_parent_observed_time_flow",
            "tau_role": "tau_obs definition",
            "candidate_identity": "tau_obs in Gamma(TM_local) is selected by e_obs plus boundary/clock normalization before any source or orbit readout.",
            "mathematical_form": "tau_obs = arg_fixed{N_boundary[e_obs,tau]=1, L_tau B_local=0, orientation future-directed}",
            "current_status": "DEFINITION_TARGET_ONLY",
            "blocking_gap": "no parent clause constructs tau_obs from local branch and boundary clock data",
            "if_signed": "all source, charge, clock, orbit and boundary comparisons can use one generator",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSL1725_1_fixed_variation",
            "tau_role": "fixed variation class",
            "candidate_identity": "delta tau_obs = 0 inside the source-current and Hamiltonian variation once the branch/boundary class is fixed.",
            "mathematical_form": "delta_{Phi,e} tau_obs |_{B_clock,B_ref}=0",
            "current_status": "VARIATION_LOCK_NOT_PARENT_SIGNED",
            "blocking_gap": "fixed-generator variational class is stated in old gates but not derived for the current parent action",
            "if_signed": "J_H[tau_obs] and delta H_tau can be compared without a moving-readout residual",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSL1725_2_source_current_lock",
            "tau_role": "source tau",
            "candidate_identity": "tau_source = tau_obs and J_H[tau_obs] is varied from ordinary matter before measured-GM fitting.",
            "mathematical_form": "J_H[tau_obs] = star(T_obs(tau_obs,.)); T_obs=(2/sqrt|g_obs|) delta S_ord/delta g_obs",
            "current_status": "SOURCE_CURRENT_LOCK_CONDITIONAL",
            "blocking_gap": "ordinary matter functor, source-prefactor exclusion and parent-signed e_obs/tau_obs are still open",
            "if_signed": "source current becomes a parent object rather than a fitted orbital mass label",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSL1725_3_hamiltonian_charge_lock",
            "tau_role": "charge tau",
            "candidate_identity": "tau_charge = tau_obs and H_tau is finite/integrable with H_ref fixed once.",
            "mathematical_form": "delta H_tau = integral_S(delta Q_tau - i_tau theta); M_H_ref=H_tau[S]-H_ref",
            "current_status": "HAMILTONIAN_LOCK_NOT_DERIVED",
            "blocking_gap": "explicit MTS theta, Q_tau, boundary conditions, integrability and reference lock are not parent-derived",
            "if_signed": "M_H_ref can become a stable denominator candidate instead of a convention",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSL1725_4_clock_lock",
            "tau_role": "clock tau",
            "candidate_identity": "tau_clock = tau_obs and clock proper time/readout follows e_obs clocks, not an independent chi_X coordinate.",
            "mathematical_form": "d s_clock^2 = -g_obs(tau_obs,tau_obs) dt^2 with boundary clock normalization fixed before alpha/clock tests",
            "current_status": "CLOCK_LOCK_NOT_DERIVED",
            "blocking_gap": "647/648 quantify product bounds for d chi_X/dt but do not construct the Hamiltonian time generator",
            "if_signed": "clock bounds test the same time generator as the source and charge sectors",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSL1725_5_orbit_lock",
            "tau_role": "orbit tau",
            "candidate_identity": "tau_orbit = tau_obs and the same H_tau source controls Poisson/Gauss and inverse-square orbital readout.",
            "mathematical_form": "nabla^2 Phi[g_obs,tau_obs]=4*pi*G_ref*rho_H; a_orbit=-grad Phi",
            "current_status": "ORBIT_LOCK_NOT_DERIVED",
            "blocking_gap": "683/457 keep Poisson-Gauss-orbit calibration blocked to avoid borrowing Newtonian GM",
            "if_signed": "GM_orbit/G_ref could become a derived readout instead of a circular denominator",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSL1725_6_boundary_reference_lock",
            "tau_role": "boundary/reference tau",
            "candidate_identity": "H_ref and boundary counterterms are fixed using the same tau_obs and carry no source-dependent shift.",
            "mathematical_form": "partial_source H_ref = partial_frame H_ref = partial_r H_ref = partial_t H_ref = 0 within the locked branch",
            "current_status": "BOUNDARY_REFERENCE_LOCK_OPEN",
            "blocking_gap": "boundary-reference status has zero claim-valid data rows and zero claim-valid theorem-zero rows for M_H_ref",
            "if_signed": "reference subtraction cannot masquerade as a source-normalization success",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSL1725_7_wep_readout_lock",
            "tau_role": "WEP/readout tau",
            "candidate_identity": "tau_WEP/source-normal/readout convention is tied to tau_obs rather than set to tau_eff=1.",
            "mathematical_form": "tau_WEP = N_eta^{-1}<K_CMSM,S_Earth x M_TiPt> in the same source-normal/readout basis",
            "current_status": "WEP_READOUT_LOCK_NOT_EVALUATED",
            "blocking_gap": "official K_CMSM/source/material/alignment inputs are absent and tau_WEP can vanish in the null-space countermodel",
            "if_signed": "WEP tau becomes an arena projection of the same parent time/source-normal convention",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSL1725_8_no_lapse_rescaling",
            "tau_role": "rescaling guard",
            "candidate_identity": "tau -> f tau is not evidence unless f is fixed by parent clock/boundary normalization and transforms source/charge/clocks consistently.",
            "mathematical_form": "J_H[f tau]=f J_H[tau]; delta H_{f tau}=f delta H_tau + Delta_f; clock rate rescales unless f=1 on B_clock",
            "current_status": "GUARD_DERIVED_AS_REFUSAL_LEMMA",
            "blocking_gap": "the guard is usable only to reject shortcuts, not to pick f or prove tau_obs exists",
            "if_signed": "prevents denominator laundering by homogeneous lapse or tau_eff=1 choices",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSL1725_9_composite_theorem",
            "tau_role": "one-generator lock",
            "candidate_identity": "If TSL1725_0 through TSL1725_8 are parent-signed, then tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit=tau_WEP=tau_obs and delta tau_obs=0.",
            "mathematical_form": "tau_all = tau_obs; R_tau_frame := {tau_source-tau_obs,...,tau_WEP-tau_obs}=0",
            "current_status": "CONDITIONAL_THEOREM_ONLY",
            "blocking_gap": "all nontrivial parent certificates remain missing or blocked",
            "if_signed": "common annulus/norm owner and M_H_ref denominator can reopen",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "audit_id": "TSL1725_10_verdict",
            "tau_role": "tau-source-normal verdict",
            "candidate_identity": "the exact contract is now written, but current MTS cannot claim a tau/source-normal lock",
            "mathematical_form": "R_tau_frame retained or source-filled; no local-GR promotion",
            "current_status": "TAU_SOURCE_NORMAL_LOCK_NOT_PARENT_SIGNED",
            "blocking_gap": "observed time vector, fixed variation, Hamiltonian charge, clock normalization, orbit bridge, WEP readout and boundary reference are unsigned",
            "if_signed": "would close the hardest normalization ambiguity in the local branch",
            "derivation_ready": no(),
            "valid_for_claim": no(),
        },
    ]


def rescaling_guard_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NLR1725_0_source_scaling",
            "shortcut": "choose tau_eff=1 or rescale tau after source readout",
            "transformation": "tau -> f tau gives J_H[f tau]=f J_H[tau]",
            "failure_mode": "source-current norm and WEP/readout tau can be tuned by f",
            "legal_only_if": "f fixed by source-independent parent clock/boundary normalization before readout",
            "status": "SHORTCUT_REJECTED",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NLR1725_1_charge_scaling",
            "shortcut": "use H_tau as denominator without fixed tau normalization",
            "transformation": "delta H_{f tau}=f delta H_tau plus possible Delta_f if f varies over phase space",
            "failure_mode": "M_H_ref can be rescaled or reference-shifted without changing observations",
            "legal_only_if": "integrable H_tau, fixed H_ref and delta tau=0 are parent-signed",
            "status": "DENOMINATOR_RESCALING_REJECTED",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NLR1725_2_clock_scaling",
            "shortcut": "identify chi_X clock drift with Hamiltonian tau by naming convention",
            "transformation": "clock rate changes under tau -> f tau unless boundary clock normalization fixes f",
            "failure_mode": "clock product bounds test a different time variable than source/charge",
            "legal_only_if": "proper-time clock normalization from e_obs and tau_obs is derived",
            "status": "CLOCK_COORDINATE_SHORTCUT_REJECTED",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NLR1725_3_orbit_scaling",
            "shortcut": "set tau from observed orbital GM",
            "transformation": "GM_orbit/G_ref fixes a readout scale only after Poisson-Gauss-orbit theorem",
            "failure_mode": "borrows Newtonian source normalization to prove the Newtonian limit",
            "legal_only_if": "M_H_ref -> Poisson/Gauss -> orbital GM is derived in that order",
            "status": "ORBITAL_BACKFILL_REJECTED",
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "guard_id": "NLR1725_4_verdict",
            "shortcut": "any single-sector tau normalization",
            "transformation": "sector-specific f_source, f_charge, f_clock, f_orbit or f_wep",
            "failure_mode": "frame residual R_tau_frame is hidden instead of bounded",
            "legal_only_if": "one parent-selected tau_obs owns every sector before comparison",
            "status": "NO_LAPSE_RESCALING_GUARD_ACTIVE",
            "valid_for_claim": no(),
        },
    ]


def input_rows() -> list[dict[str, Any]]:
    source_bundle = ";".join(str(source["source_path"]) for source in SOURCES)
    return [
        {
            "branch_id": BRANCH_ID,
            "input_id": "TAU1725_0_common_tau_lock_candidate",
            "quantity": "R_tau_frame",
            "definition": "vector residual stack measuring tau_source, tau_charge, tau_clock, tau_boundary, tau_orbit and tau_WEP against tau_obs",
            "formula": "R_tau_frame={tau_source-tau_obs,tau_charge-tau_obs,tau_clock-tau_obs,tau_boundary-tau_obs,tau_orbit-tau_obs,tau_WEP-tau_obs}",
            "required_inputs": "system_id;e_obs_id;tau_obs_definition;clock_normalization;Hamiltonian_generator;H_ref_rule;source_normal;orbit_readout_rule;WEP_readout_basis;units;source_path",
            "current_status": "EXPLICIT_FINITE_INPUT_ROW_TEMPLATE_ONLY",
            "missing_inputs": "MISSING_PARENT_SELECTED_TAU_OBS;MISSING_CLOCK_NORMALIZATION;MISSING_HAMILTONIAN_GENERATOR;MISSING_REFERENCE_LOCK;MISSING_ORBIT_BRIDGE;MISSING_WEP_READOUT_BASIS;MISSING_UNITS",
            "source_paths": source_bundle,
            "numeric_value": "MISSING_RESIDUAL_VECTOR_OR_THEOREM_ZERO",
            "units": "mixed_until_common_time_normalization_declared",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "TAU1725_1_observed_time_generator_candidate",
            "quantity": "tau_obs",
            "definition": "parent-selected observed time-flow vector normalized by boundary/clock data",
            "formula": "tau_obs in Gamma(TM_local), N_boundary[e_obs,tau_obs]=1, L_tau B_local=0",
            "required_inputs": "stationary_or_quasilocal_domain;boundary_clock;normalization_rule;e_obs_id;delta_tau_rule",
            "current_status": "MISSING_PARENT_SELECTED_TAU_OBS",
            "missing_inputs": "MISSING_LOCAL_STATIONARY_KILLING_CERTIFICATE;MISSING_BOUNDARY_CLOCK_NORMALIZATION;MISSING_DELTA_TAU_ZERO",
            "source_paths": str(RESIDUALS / "P8_Y5_R10_685_KILLING_CLOCK_GATE.csv") + ";" + str(RESIDUALS / "P8_Y5_R10_685_TAU_GENERATOR_CONTRACT.csv"),
            "numeric_value": "MISSING_VECTOR_FIELD_OR_THEOREM",
            "units": "time_generator_normalization_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "TAU1725_2_source_normal_candidate",
            "quantity": "n_source_or_tau",
            "definition": "source-normal convention used by J_H[tau], annulus volume form, WEP readout and boundary charge",
            "formula": "n_source = tau_obs/sqrt(-g_obs(tau_obs,tau_obs)) where timelike and normalized; otherwise explicit quasilocal normal certificate",
            "required_inputs": "e_obs_id;tau_obs_id;signature;orientation;source worldtube;annulus slice;readout basis",
            "current_status": "MISSING_SOURCE_NORMAL_LOCK",
            "missing_inputs": "MISSING_PARENT_SIGNED_EOBS;MISSING_PARENT_SIGNED_TAU_OBS;MISSING_ORIENTATION;MISSING_WORLDTUBE_SOURCE_BASIS",
            "source_paths": str(RESIDUALS / "P8_Y5_PARENT_QLOC_1720_JH_NORM_FIRST_SOURCE_ROW.csv") + ";" + str(RESIDUALS / "P8_Y5_PARENT_QLOC_1608_TAU_WEP_READOUT_CONTRACT.csv"),
            "numeric_value": "MISSING_NORMAL_CERTIFICATE",
            "units": "dimensionless_unit_normal_or_time_normal_MISSING",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "input_id": "TAU1725_3_lapse_rescaling_bound_candidate",
            "quantity": "epsilon_tau_rescale",
            "definition": "finite residual for allowed mismatch between sector tau normalizations if theorem-zero fails",
            "formula": "epsilon_tau_rescale := ||R_tau_frame||_declared / ||tau_obs||_declared",
            "required_inputs": "norm_on_time_generators;sector_tau_values;common_units;source_path;bound_or_theorem_zero",
            "current_status": "RETAINED_RESIDUAL_TEMPLATE_ONLY",
            "missing_inputs": "MISSING_TAU_NORM;MISSING_SECTOR_TAU_VALUES;MISSING_COMMON_UNITS;MISSING_BOUND",
            "source_paths": str(OUTPUTS["rescaling_guard"]),
            "numeric_value": "MISSING_EPSILON_TAU_RESCALE_BOUND",
            "units": "dimensionless_after_norm_declared",
            "score_ready": no(),
            "valid_for_claim": no(),
        },
    ]


def runner_refusal_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1725_0_tau_lock_theorem",
            "quantity": "one-generator tau/source-normal lock",
            "runner_decision": "CONDITIONAL_ONLY_REFUSE_CLAIM",
            "refusal_reasons": "MISSING_PARENT_SELECTED_TAU_OBS;MISSING_FIXED_VARIATION;MISSING_HAMILTONIAN_GENERATOR;MISSING_CLOCK_NORMALIZATION;MISSING_ORBIT_BRIDGE;MISSING_WEP_READOUT_BASIS;MISSING_REFERENCE_LOCK",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1725_1_lapse_guard",
            "quantity": "no-lapse-rescaling guard",
            "runner_decision": "ACCEPT_REFUSAL_LEMMA_ONLY",
            "refusal_reasons": "guard rejects tau_eff=1 and rescaled denominators but does not construct tau_obs",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1725_2_explicit_input_rows",
            "quantity": "R_tau_frame finite input rows",
            "runner_decision": "ACCEPT_SCHEMA_REFUSE_SCORING",
            "refusal_reasons": "all rows carry MISSING markers and valid_for_claim=false",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1725_3_common_norm_owner",
            "quantity": "1724 common annulus/norm owner reopening",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "TAU_SOURCE_NORMAL_LOCK_NOT_PARENT_SIGNED",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "run_id": "RUN1725_4_Newton_local_GR",
            "quantity": "Newton/local-GR source-normalization",
            "runner_decision": "BLOCKED_NO_CLAIM",
            "refusal_reasons": "NO_TAU_LOCK;NO_M_H_REF_DENOMINATOR;NO_JH_TOTAL_NORM;NO_NDOMAIN;PPN_VECTOR_OPEN",
            "accepted_for_scoring": no(),
            "claim_allowed": no(),
        },
    ]


def decision_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1725_0_partial_derivation",
            "decision": "rescaling shortcut is killed",
            "because": "tau -> f tau rescales source current, Hamiltonian charge and clock readout unless one parent clock/boundary normalization fixes f before comparison",
            "next_action": "keep no-lapse guard active in every local source-normalization runner",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1725_1_tau_lock_verdict",
            "decision": "one-generator tau lock remains unsigned",
            "because": "observed vector, fixed variation, Hamiltonian integrability, clock normalization, orbit bridge, boundary reference and WEP readout all remain missing",
            "next_action": "split the hard theorem and attack the observed time-generator/fixed-variation clause first",
        },
        {
            "branch_id": BRANCH_ID,
            "decision_id": "DEC1725_2_finite_branch",
            "decision": "retain explicit R_tau_frame input row",
            "because": "if the theorem fails, the local branch can still be tested as a finite frame-residual branch rather than pretending to reduce to GR",
            "next_action": "bound or source epsilon_tau_rescale before any M_H_ref, J_H or N_domain scoring",
        },
    ]


def next_target_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1725_0_primary",
            "next_target": "1726-Y5-R2FR-observed-time-generator-fixed-variation-or-Rtau-residual-bound.md",
            "script": "scripts/Y5_R2FR_observed_time_generator_fixed_variation_or_Rtau_residual_bound.py",
            "objective": "derive parent selection of tau_obs plus delta tau_obs=0 from boundary/clock/stationary data, or bound the R_tau_frame residual explicitly",
            "selection_status": "selected",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1725_1_parallel_surface_annulus",
            "next_target": "1726b-Y5-R2FR-surface-pair-annulus-source-row-fill.md",
            "script": "scripts/Y5_R2FR_surface_pair_annulus_source_row_fill.py",
            "objective": "fill S1/S2/A_ext/homology/source-free certificate as geometry inputs after the tau guard is written",
            "selection_status": "held_parallel",
        },
        {
            "branch_id": BRANCH_ID,
            "route_id": "NEXT1725_2_later_nonHilbert",
            "next_target": "1727-Y5-R2FR-nonHilbert-current-silence-or-qnonH-source-row.md",
            "script": "scripts/Y5_R2FR_nonHilbert_current_silence_or_qnonH_source_row.py",
            "objective": "derive non-Hilbert/current/readout source silence or source a finite q_nonH correction once the frame/time guard is less ambiguous",
            "selection_status": "later",
        },
    ]


def claim_gate_rows() -> list[dict[str, Any]]:
    return [
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1725_0_tau_source_normal_lock",
            "claim": "tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit=tau_WEP=tau_obs",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "composite tau theorem remains conditional and all nontrivial parent certificates are missing",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1725_1_tau_rescaling_solved",
            "claim": "tau normalization ambiguity is solved",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "rescaling guard rejects shortcuts but does not choose a parent-normalized tau_obs",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1725_2_M_H_ref_denominator",
            "claim": "M_H_ref is a safe local denominator",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "Hamiltonian integrability, fixed reference and tau lock are unsigned",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1725_3_common_norm_owner",
            "claim": "1724 common annulus/norm owner can reopen",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "tau/source-normal lock is still not parent-signed",
            "claim_allowed": no(),
        },
        {
            "branch_id": BRANCH_ID,
            "claim_id": "CG1725_4_Newton_local_GR",
            "claim": "Newton/local-GR reduction is derived",
            "status": "BLOCKED_NO_CLAIM",
            "reason": "tau lock, M_H_ref, J_H_total, N_domain and PPN vector remain open",
            "claim_allowed": no(),
        },
    ]


def rows_by_key() -> dict[str, list[dict[str, Any]]]:
    return {
        "source_register": source_rows(),
        "theorem_audit": theorem_audit_rows(),
        "rescaling_guard": rescaling_guard_rows(),
        "input_rows": input_rows(),
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
    shutil.copy2(OUTPUTS["source_register"], QUARANTINE / "P8_Y5_PARENT_QLOC_1725_SOURCE_REGISTER.csv")
    for key, filename in COPY_MAP.items():
        shutil.copy2(OUTPUTS[key], MICROSCOPE_RESIDUALS / filename)
        shutil.copy2(OUTPUTS[key], QUARANTINE / filename)
        shutil.copy2(OUTPUTS[key], RAB_QUEUE / f"JR1725_{key.upper()}.csv")


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
    if not (QUARANTINE / "P8_Y5_PARENT_QLOC_1725_SOURCE_REGISTER.csv").exists():
        return False
    for key, filename in COPY_MAP.items():
        if not (MICROSCOPE_RESIDUALS / filename).exists():
            return False
        if not (QUARANTINE / filename).exists():
            return False
        if not (RAB_QUEUE / f"JR1725_{key.upper()}.csv").exists():
            return False
    return True


def formalization_untouched() -> bool:
    if not FORMALIZATION.exists():
        return True
    for path in FORMALIZATION.rglob("*1725*"):
        text = str(path)
        if "\\.venv\\" in text or "\\__pycache__\\" in text:
            continue
        if path.is_file():
            return False
    return True


def input_rows_have_missing(rows: list[dict[str, Any]]) -> bool:
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
    theorem = rows_map["theorem_audit"]
    guard = rows_map["rescaling_guard"]
    input_candidates = rows_map["input_rows"]
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
        check("VAL1725_0_sources_exist", all(row["exists"] == "True" for row in source_register), "all cited source paths exist", "one or more cited source paths missing"),
        check("VAL1725_1_needles_present", all(row["needles_present"] == "True" for row in source_register), "required source needles are present", "one or more required source needles missing"),
        check(
            "VAL1725_2_1724_handoff_preserved",
            any(row["source_key"] == "1724_next_target" and row["needles_present"] == "True" for row in source_register),
            "1724 selected tau/source-normal lock route",
            "1724 handoff missing",
        ),
        check(
            "VAL1725_3_theorem_roles_complete",
            {row["tau_role"] for row in theorem} >= {"tau_obs definition", "fixed variation class", "source tau", "charge tau", "clock tau", "orbit tau", "boundary/reference tau", "WEP/readout tau", "rescaling guard", "one-generator lock"},
            "theorem audit covers tau definition, variation, source, charge, clock, orbit, boundary, WEP and rescaling roles",
            "theorem audit missing required tau role",
        ),
        check(
            "VAL1725_4_verdict_blocked",
            any(row["audit_id"] == "TSL1725_10_verdict" and row["current_status"] == "TAU_SOURCE_NORMAL_LOCK_NOT_PARENT_SIGNED" for row in theorem),
            "tau/source-normal lock verdict remains blocked",
            "tau/source-normal lock verdict missing or opened",
        ),
        check(
            "VAL1725_5_rescaling_guard_active",
            any(row["guard_id"] == "NLR1725_4_verdict" and row["status"] == "NO_LAPSE_RESCALING_GUARD_ACTIVE" for row in guard),
            "no-lapse-rescaling guard is active",
            "no-lapse-rescaling guard missing",
        ),
        check(
            "VAL1725_6_input_rows_nonclaim",
            len(input_candidates) == 4 and input_rows_have_missing(input_candidates),
            "explicit finite input rows remain nonclaim and contain missing markers",
            "input rows are incomplete or claim-enabled",
        ),
        check(
            "VAL1725_7_runner_refusals_cover_chain",
            {row["quantity"] for row in refusals} >= {"one-generator tau/source-normal lock", "no-lapse-rescaling guard", "R_tau_frame finite input rows", "Newton/local-GR source-normalization"},
            "runner refusals cover tau lock, rescaling guard, finite input rows and Newton/local-GR",
            "runner refusals do not cover the full chain",
        ),
        check(
            "VAL1725_8_decision_next",
            any(row["decision_id"] == "DEC1725_1_tau_lock_verdict" and "observed time-generator" in row["next_action"] for row in decisions),
            "decision selects observed time-generator/fixed-variation clause next",
            "decision does not select the time-generator/fixed-variation split",
        ),
        check(
            "VAL1725_9_next_selected",
            any(row["route_id"] == "NEXT1725_0_primary" and row["selection_status"] == "selected" for row in next_rows),
            "next target row selects 1726 primary route",
            "next target missing selected primary route",
        ),
        check(
            "VAL1725_10_claim_gates_blocked",
            all(row["status"] == "BLOCKED_NO_CLAIM" and row["claim_allowed"] == "False" for row in claim_rows),
            "claim gates remain blocked",
            "one or more claim gates opened",
        ),
        check("VAL1725_11_csv_parse", parsed_ok, "all generated 1725 CSVs parse", "one or more generated 1725 CSVs failed to parse"),
        check("VAL1725_12_no_claim_flags", no_claim_flags(rows_map), "all generated scoring and claim flags remain false", "one or more generated flags enabled a claim"),
        check("VAL1725_13_branch_copies", branch_copies_exist(), "branch/quarantine/queue copies exist", "one or more branch/quarantine/queue copies missing"),
        check("VAL1725_14_pycache_absent", not (ROOT / "scripts" / "__pycache__").exists(), "scripts __pycache__ absent", "scripts __pycache__ still exists"),
        check("VAL1725_15_formalization_untouched", formalization_untouched(), "no 1725 outputs found under formalization-workbench", "1725 output leaked into formalization-workbench"),
    ]
    overall = all(row["result"] == "PASS" for row in validation)
    validation.append(
        {
            "branch_id": BRANCH_ID,
            "check_id": "VAL1725_OVERALL",
            "result": "PASS" if overall else "FAIL",
            "detail": "1725 tau/source-normal lock validation" if overall else "one or more 1725 validation checks failed",
        }
    )
    return validation


def build_markdown(rows_map: dict[str, list[dict[str, Any]]], validation_rows: list[dict[str, Any]]) -> str:
    lines = [
        f"# {TITLE}",
        "",
        "## Verdict",
        "- 1725 tries the derivation-first route for the one-generator `tau_obs`/source-normal lock.",
        "- The useful progress is real but negative: a lapse/time-rescaling shortcut is now explicitly killed. Setting `tau_eff=1`, choosing `tau` from orbital `GM`, or using a clock coordinate as the Hamiltonian generator is not evidence.",
        "- The full lock is still not parent-signed: observed time vector, fixed variation, Hamiltonian integrability, clock normalization, orbit bridge, boundary reference, and WEP readout remain open.",
        "- The fallback is no longer vague. It is the explicit residual vector `R_tau_frame`, which must be theorem-zero or finite/source-backed before any local-GR/Newton claim can reopen.",
        "- No WEP, R10, PPN, clock, orbital, Newton, local-GR, `M_H_ref`, `J_H_total`, `N_domain`, or source-normalization claim is made.",
        "",
        "## Conditional Tau-Lock Theorem",
        "If the parent action selects a future-directed observed time vector `tau_obs` from `e_obs` plus boundary/clock data, fixes `delta tau_obs=0` in the allowed variation class, makes `H_tau` integrable with a fixed reference, uses the same `tau_obs` in source variation, clock readout, orbit readout, boundary subtraction, and WEP/source-normal conventions, and forbids lapse rescaling by a parent normalization rule, then `tau_source=tau_charge=tau_clock=tau_boundary=tau_orbit=tau_WEP=tau_obs`. The present corpus has this theorem as a contract, not as a completed derivation.",
        "",
        "## Source Register",
        markdown_table(rows_map["source_register"], ["source_id", "source_key", "source_path", "exists", "needles_present"]),
        "",
        "## Tau Source-Normal Theorem Audit",
        markdown_table(rows_map["theorem_audit"], ["audit_id", "tau_role", "current_status", "blocking_gap", "derivation_ready", "valid_for_claim"]),
        "",
        "## No-Lapse Rescaling Guard",
        markdown_table(rows_map["rescaling_guard"], ["guard_id", "shortcut", "failure_mode", "legal_only_if", "status", "valid_for_claim"]),
        "",
        "## Explicit Finite Input Rows",
        markdown_table(rows_map["input_rows"], ["input_id", "quantity", "current_status", "missing_inputs", "numeric_value", "units", "score_ready", "valid_for_claim"]),
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
        "This is a good hardening step. It does not get us local GR, but it cuts off one of the biggest ways a local branch can accidentally cheat: hiding a source/clock/charge mismatch inside a normalization choice. The next move should split the monster: first try to derive the observed time generator and `delta tau_obs=0` fixed-variation clause. If that fails, `R_tau_frame` becomes a finite empirical residual branch rather than an implicit GR reduction.",
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
    doc_path = ROOT / "1725-Y5-R2FR-tau-source-normal-lock-or-explicit-finite-input-row.md"
    doc_path.write_text(build_markdown(rows_map, validation_rows), encoding="utf-8")
    print(f"wrote {doc_path}")
    print(f"wrote {OUTPUTS['validation']}")
    overall = next(row for row in validation_rows if row["check_id"] == "VAL1725_OVERALL")
    if overall["result"] != "PASS":
        raise SystemExit("1725 validation FAIL")
    print("1725 validation PASS")


if __name__ == "__main__":
    main()
