from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4012"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4012-Y5-R2FR-PiM-Htau-source-current-commutator-lock-or-CM-Ccurl-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4012_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4012_CHARGE_LOCK_AUDIT.csv",
    "finite": SRC / "P8_Y5_R2FR_4012_CHARGE_GLUE_FINITE_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4012_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4012_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4012_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4012_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4012_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4012_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4012_VALIDATION.csv",
}

NEXT_DOC = "4013-Y5-R2FR-Maxwell-Poynting-Hilbert-stress-once-only-lock-or-IEM-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4013_Maxwell_Poynting_Hilbert_stress_once_only_lock_or_IEM_row.py"


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
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
        writer.writerows(rows)


def source_specs() -> list[tuple[str, Path, str, str]]:
    return [
        ("SRC4012_00_handoff", SRC / "P8_Y5_R2FR_4011_NEXT_TARGET.csv", "NEXT4011_0", "4011 handoff"),
        ("SRC4012_01_support_measure", SRC / "P8_Y5_R2FR_4011_HILBERT_WORLDTUBE_LOCK_THEOREM.csv", "HWT4011_2_source_measure_descent", "4011 source measure descent"),
        ("SRC4012_02_support_full", SRC / "P8_Y5_R2FR_4011_HILBERT_WORLDTUBE_LOCK_THEOREM.csv", "HWT4011_6_full_lock_condition", "4011 support lock condition"),
        ("SRC4012_03_same_charge_audit", SRC / "P8_Y5_R2FR_4011_SOURCE_MEASURE_DESCENT_AUDIT.csv", "SDA4011_4_same_charge_PiM_Htau", "same-charge audit"),
        ("SRC4012_04_EM_once_audit", SRC / "P8_Y5_R2FR_4011_SOURCE_MEASURE_DESCENT_AUDIT.csv", "SDA4011_6_EM_Poynting_once", "EM/Poynting once-only audit"),
        ("SRC4012_05_same_charge_row", SRC / "P8_Y5_R2FR_4011_SUPPORT_FLUX_FINITE_ROWS.csv", "SFLUX4011_4_same_charge", "same-charge finite row"),
        ("SRC4012_06_reference_row", SRC / "P8_Y5_R2FR_4011_SUPPORT_FLUX_FINITE_ROWS.csv", "SFLUX4011_5_reference_surface", "reference/surface finite row"),
        ("SRC4012_07_EM_once_row", SRC / "P8_Y5_R2FR_4011_SUPPORT_FLUX_FINITE_ROWS.csv", "SFLUX4011_7_EM_once", "EM once finite row"),
        ("SRC4012_08_4011_decision", SRC / "P8_Y5_R2FR_4011_DECISION_GATE.csv", "DEC4011_3_next", "4011 next decision"),
        ("SRC4012_09_PiM_fixed", SRC / "P8_Y5_R2FR_4001_PIM_CONSTANCY_THEOREM.csv", "PCM4001_1_fixed_chainmap_zero", "fixed Pi_M chain-map theorem"),
        ("SRC4012_10_PiM_qbasic", SRC / "P8_Y5_R2FR_4001_PIM_CONSTANCY_THEOREM.csv", "PCM4001_3_quotient_source_connection_zero", "q-basic source-coordinate route"),
        ("SRC4012_11_wrong_current", SRC / "P8_Y5_R2FR_4001_PIM_CONSTANCY_THEOREM.csv", "PCM4001_4_closed_wrong_current_guard", "closed wrong-current guard"),
        ("SRC4012_12_PiM_audit_Htau", SRC / "P8_Y5_R2FR_4001_PIM_ZERO_PROOF_AUDIT.csv", "PZA4001_4_Htau_Href", "H_tau/H_ref Pi_M audit"),
        ("SRC4012_13_PiM_audit_guard", SRC / "P8_Y5_R2FR_4001_PIM_ZERO_PROOF_AUDIT.csv", "PZA4001_5_wrong_current_guard", "wrong current guard audit"),
        ("SRC4012_14_C_M", SRC / "P8_Y5_R2FR_4001_PIM_COMMUTATOR_BOUND_VECTOR.csv", "PMB4001_1_C_M", "C_M bound row"),
        ("SRC4012_15_C_curl", SRC / "P8_Y5_R2FR_4001_PIM_COMMUTATOR_BOUND_VECTOR.csv", "PMB4001_3_C_curl", "C_curl bound row"),
        ("SRC4012_16_I_comm", SRC / "P8_Y5_R2FR_4001_PIM_COMMUTATOR_BOUND_VECTOR.csv", "PMB4001_7_I_commutator", "I_commutator bound row"),
        ("SRC4012_17_R_eq", SRC / "P8_Y5_R2FR_4001_PIM_COMMUTATOR_BOUND_VECTOR.csv", "PMB4001_9_R_eq_guard", "R_eq guard row"),
        ("SRC4012_18_Htau_integrability", SRC / "P8_Y5_R2FR_4002_HTAU_HREF_THEOREM.csv", "HIR4002_1_integrability_criterion", "H_tau integrability criterion"),
        ("SRC4012_19_Htau_zero", SRC / "P8_Y5_R2FR_4002_HTAU_HREF_THEOREM.csv", "HIR4002_5_zero_branch", "H_tau zero branch"),
        ("SRC4012_20_Htau_bound", SRC / "P8_Y5_R2FR_4002_CURL_REFERENCE_BOUND_VECTOR.csv", "HRB4002_0_master", "H_tau/H_ref bound vector"),
        ("SRC4012_21_Noether_current", SRC / "P8_Y5_R2FR_4003_PARENT_CURRENT_CHAIN_THEOREM.csv", "PCC4003_1_noether_current", "parent Noether current"),
        ("SRC4012_22_Noether_descent", SRC / "P8_Y5_R2FR_4003_PARENT_CURRENT_CHAIN_THEOREM.csv", "PCC4003_3_descent_zero_lemma", "descent to reduced/EH charge"),
        ("SRC4012_23_Noether_feedthrough", SRC / "P8_Y5_R2FR_4003_PARENT_CURRENT_CHAIN_THEOREM.csv", "PCC4003_4_integrability_feedthrough", "current-chain H_tau feedthrough"),
        ("SRC4012_24_matter_EM", SRC / "P8_Y5_R2FR_4003_INTEGRABILITY_COMPONENT_BOUND_VECTOR.csv", "PCB4003_5_I_matter_EM", "matter/EM flux row"),
        ("SRC4012_25_3514_derivation", SRC / "P8_Y5_R2FR_3514_PIM_HTAU_COMMUTATOR_DERIVATION.csv", "PHC3514_3_conditional_zero_theorem", "3514 Pi_M/H_tau zero route"),
        ("SRC4012_26_3514_C_M", SRC / "P8_Y5_R2FR_3514_PIM_HTAU_RESIDUAL_COMPONENTS.csv", "PHCR3514_1_C_M", "3514 C_M row"),
        ("SRC4012_27_3514_C_curl", SRC / "P8_Y5_R2FR_3514_PIM_HTAU_RESIDUAL_COMPONENTS.csv", "PHCR3514_3_C_curl", "3514 C_curl row"),
        ("SRC4012_28_3514_zero_gates", SRC / "P8_Y5_R2FR_3514_PIM_HTAU_ZERO_GATES.csv", "PHCG3514_1_integrable_Htau", "3514 integrable H_tau gate"),
        ("SRC4012_29_single_charge", SRC / "P8_Y5_R2FR_3575_SINGLE_CHARGE_THEOREM.csv", "SCT3575_5_Hamiltonian_charge_lock", "single charge/H_tau lock"),
        ("SRC4012_30_qbasic_Htau", SRC / "P8_Y5_R2FR_3577_HTAU_QBASIC_REFERENCE_THEOREM.csv", "HTQ3577_3_MHref_qbasic", "M_H_ref q-basic theorem"),
        ("SRC4012_31_curl_identity", SRC / "P8_Y5_R2FR_3578_HTAU_CURL_IDENTITIES.csv", "CID3578_1_curl", "H_tau curl law"),
        ("SRC4012_32_curl_total", SRC / "P8_Y5_R2FR_3578_HTAU_CURL_COMPONENT_VECTOR.csv", "HCURL3578_8_total", "H_tau curl component total"),
        ("SRC4012_33_charge_identity", SRC / "P8_Y5_R2FR_3592_CHARGE_EQUALITY_RESIDUAL_IDENTITY.csv", "CEI3592_10_total_identity", "charge equality total identity"),
        ("SRC4012_34_subdenom", SRC / "P8_Y5_R2FR_3602_PIM_HTAU_SUBDENOMINATOR_THEOREM.csv", "PHT3602_6_subdenominator_theorem", "Pi_M/H_tau subdenominator theorem"),
        ("SRC4012_35_flux_closure", SRC / "P8_Y5_R2FR_3884_PIM_HILBERT_FLUX_CLOSURE_THEOREM.csv", "PFC3884_1_product_rule", "Pi_M Hilbert flux closure"),
        ("SRC4012_36_flux_EM", SRC / "P8_Y5_R2FR_3884_PIM_HILBERT_FLUX_CLOSURE_THEOREM.csv", "PFC3884_3_em_flux", "EM flux exception"),
        ("SRC4012_37_combined_zero", SRC / "P8_Y5_R2FR_3911_PIM_HTAU_COMBINED_ZERO_OR_BOUND.csv", "COM3911_1_double_zero_branch", "combined double-zero branch"),
        ("SRC4012_38_curl_exact", SRC / "P8_Y5_R2FR_3911_HTAU_CURL_EXACTNESS_GATE.csv", "CURL3911_1_stationary_exact_flux_zero", "stationary exact flux zero"),
        ("SRC4012_39_constraint_map", SRC / "P8_Y5_R2FR_3941_PIM_HTAU_MAP_DERIVATION.csv", "MAP3941_2_constraint_pushforward", "constraint-map Pi_M construction"),
        ("SRC4012_40_constraint_theorem", SRC / "P8_Y5_R2FR_3941_PIM_HTAU_MAP_DERIVATION.csv", "MAP3941_4_conditional_theorem", "conditional PiM/Htau theorem"),
        ("SRC4012_41_PiM_comm_zero", SRC / "P8_Y5_R2FR_3965_PIM_COMMUTATOR_ZERO_THEOREM_OR_BOUND.csv", "PCT3965_2_zero_theorem", "fixed parent chain-map zero"),
        ("SRC4012_42_equality_guard", SRC / "P8_Y5_R2FR_3986_PIM_HILBERT_EQUALITY_REDUCTION_THEOREM.csv", "PH3986_1_not_full_parent_equality", "not full parent equality guard"),
    ]


def source_register_rows(timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in source_specs():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "role": role,
                "path": str(path),
                "needle": needle,
                "exists": path.exists(),
                "needle_found": needle in text,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def theorem_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "CHG4012_0_parent_constraint_map",
            "claim_piece": "non-circular Pi_M construction",
            "mathematical_form": "Pi_M^C := D_N[C_tau]|_{J_H[tau]} on the compact exterior annulus; Delta_charge := M_H[Pi_M^C J_H] - (H_tau[S_outer]-H_ref)",
            "derived_result": "Pi_M is not a fitted mass mask; it is the parent constraint/boundary-charge pushforward from Hilbert source current to exterior Hamiltonian charge",
            "status": "CONDITIONAL_CONSTRUCTION_NOT_PARENT_ADOPTED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CHG4012_1_chainmap_commutator_zero",
            "claim_piece": "projected current commutator zero",
            "mathematical_form": "d(Pi_M^C J_H)=Pi_M^C dJ_H + [d,Pi_M^C]J_H; if Pi_M^C is parent-selected, fixed on A_ext, and d Pi_M^C=Pi_M^C d on C_H(A_ext), then [d,Pi_M^C]J_H=0",
            "derived_result": "the Pi_M commutator is killed by parent chain-map fixedness, not by assuming the source current is already closed",
            "status": "EXACT_CONDITIONAL_CHAINMAP_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CHG4012_2_Htau_curl_zero",
            "claim_piece": "Hamiltonian charge exactness",
            "mathematical_form": "alpha_tau[delta Phi]=int_S(delta Q_tau^MTS-i_tau Theta_total)-delta H_ref; d_field alpha_tau=0 iff int_S i_tau omega_MTS plus corner/reference terms vanish or are exact/proper",
            "derived_result": "C_curl=0 is a covariant-phase-space exactness condition; otherwise it is a real curl row, not a notation issue",
            "status": "EXACT_CONDITIONAL_HTAU_INTEGRABILITY_GATE",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CHG4012_3_MHref_qbasic_CM_zero",
            "claim_piece": "mass-coordinate connection zero",
            "mathematical_form": "If M_H_ref=H_tau-H_ref=Mbar_H_ref(q(Phi)) and v_X in ker(Dq), then A_X^M=D_X M_H_ref=0 and C_M=0",
            "derived_result": "the mass-coordinate leakage C_M is zero only when the Hamiltonian denominator descends through the same quotient as the source branch",
            "status": "EXACT_IF_MHREF_Q_BASIC",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CHG4012_4_same_charge_equality",
            "claim_piece": "Pi_M/H_tau/Hilbert source equality",
            "mathematical_form": "Pi_M^C J_H = J_M_top + dB_zero and M_H[Pi_M^C J_H]=H_tau[S_outer]-H_ref if the parent constraint map is unique, no homogeneous mass kernel survives, exact terms have zero linked-surface flux, and all extra/EM/boundary fluxes are owned",
            "derived_result": "the Newton source mass can be the same object as the Hamiltonian charge, but only on a strict parent constraint-map branch",
            "status": "CONDITIONAL_SAME_CHARGE_THEOREM_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CHG4012_5_double_zero_branch",
            "claim_piece": "R_PiM plus R_Htau collapse",
            "mathematical_form": "R_PiM+R_Htau=C_M+C_shape+C_curl+C_domain+C_ref+C_frame+C_units; 4001+4002+4011 give zero if Pi_M fixed, M_H_ref q-basic, H_tau exact, support/domain fixed, reference/frame/units locked",
            "derived_result": "the double zero is derivable as a branch theorem assembled from prior gates; it is not currently a global MTS claim",
            "status": "EXACT_CONDITIONAL_ASSEMBLY_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "CHG4012_6_charge_glue_finite_vector",
            "claim_piece": "finite fallback if charge lock fails",
            "mathematical_form": "epsilon_charge_4012 <= |C_M|+|C_curl|+|I_commutator|+|R_eq|+|C_ref|+|C_frame|+|C_units|+|R_kernel|+|R_extra|+|R_symp|+|R_boundary|+|R_EM_flux|+|epsilon_G_norm|+|epsilon_PPN_source|",
            "derived_result": "the surviving coupling obstruction is now an explicit finite vector with no fitted-GM laundering and no cancellation credit",
            "status": "FINITE_CHARGE_GLUE_VECTOR_DERIVED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "CGA4012_0_parent_constraint_map",
            "clause": "Pi_M is constructed as a parent constraint/boundary-charge map before readout",
            "current_status": "CONDITIONAL_CONSTRUCTION_EXISTS_NOT_FINAL_PARENT_ADOPTED",
            "risk_if_open": "Pi_M remains a selector and the mass charge can be tuned after seeing local data",
            "next_action": "adopt Pi_M^C in the parent branch or retain I_commutator and R_eq",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CGA4012_1_chainmap_fixedness",
            "clause": "d Pi_M=Pi_M d and D_X Pi_M=0 on the Hilbert current complex in the compact exterior",
            "current_status": "EXACT_MATH_LEMMA_PHYSICAL_DOMAIN_UNSIGNED",
            "risk_if_open": "projector current is not conserved even if Hilbert current is",
            "next_action": "prove current-domain compatibility or source I_commutator",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CGA4012_2_Htau_integrability",
            "clause": "alpha_tau is closed on the allowed local branch",
            "current_status": "CURL_GATE_OPEN",
            "risk_if_open": "H_tau is path-dependent and C_curl remains a physical residual",
            "next_action": "derive exact/zero symplectic flux or keep C_curl",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CGA4012_3_MHref_qbasic",
            "clause": "M_H_ref=H_tau-H_ref descends through q and is positive/same-frame/unit-declared",
            "current_status": "CONDITIONAL_DENOMINATOR_LOCK",
            "risk_if_open": "C_M and C_units can hide source normalization drift",
            "next_action": "bind H_tau/H_ref/tau/e_obs/surfaces to the same branch or retain C_M/C_units",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CGA4012_4_same_charge",
            "clause": "Pi_M J_H equals exterior Hamiltonian/topological source charge with zero-flux exact terms",
            "current_status": "NOT_DERIVED_KEY_BLOCKER_REDUCED_TO_CONSTRAINT_KERNEL",
            "risk_if_open": "support can be correct while measured Newtonian GM is a different charge",
            "next_action": "prove constraint-map uniqueness/no homogeneous mass kernel or keep R_eq/R_kernel",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CGA4012_5_EM_Poynting_source",
            "clause": "EM stress, Poynting flux and binding energy enter J_H_total exactly once",
            "current_status": "OPEN_CRITICAL_GUARD",
            "risk_if_open": "local source coupling double-counts or omits field energy",
            "next_action": "make Maxwell/Poynting Hilbert stress the next parent-owned source-current target",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CGA4012_6_G_normalization",
            "clause": "universal G_ref normalization is fixed independently of orbital GM fit",
            "current_status": "CALIBRATION_GUARD_OPEN",
            "risk_if_open": "first-order Newton success becomes a calibration tautology",
            "next_action": "separate source charge equality from empirical G_ref calibration",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "CGA4012_7_PPN_stability",
            "clause": "the same charge remains stable through beta/gamma/preferred-frame/source-profile order",
            "current_status": "NOT_TESTED_BY_CHARGE_EQUALITY",
            "risk_if_open": "Newton-looking first order does not imply local GR",
            "next_action": "keep PPN source-stability gate closed until second-order residuals are derived or bounded",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def finite_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "CGLUE4012_0_master",
            "coefficient": "epsilon_charge_4012",
            "formula": "|C_M|+|C_curl|+|I_commutator|+|R_eq|+|C_ref|+|C_frame|+|C_units|+|R_kernel|+|R_extra|+|R_symp|+|R_boundary|+|R_EM_flux|+|epsilon_G_norm|+|epsilon_PPN_source|",
            "value": "MISSING_PARENT_SIGNED_OR_NUMERIC_COMPONENTS",
            "units": "dimensionless_fractional_charge_mismatch",
            "source_status": "FINITE_VECTOR_NONCLAIM",
            "observable_links": "Newton GM; PPN; R10 normalization; clocks; orbital systems",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CGLUE4012_1_C_M",
            "coefficient": "C_M",
            "formula": "-(partial_M A_X^M) partial_M(H_tau-H_ref)/(Pi_M H_tau)",
            "value": "ZERO_IF_MHREF_Q_BASIC_ELSE_MISSING_MASS_CONNECTION_BOUND",
            "units": "dimensionless_mass_connection",
            "source_status": "NEW_PARENT_CONNECTION_REQUIRED",
            "observable_links": "Newton source normalization; R10 source charge; PPN source profile",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CGLUE4012_2_C_curl",
            "coefficient": "C_curl",
            "formula": "Pi_M^H(curl(delta H_tau))/(Pi_M H_tau)",
            "value": "ZERO_IF_HTAU_EXACT_ELSE_MISSING_SYMPLECTIC_CURL_BOUND",
            "units": "dimensionless_Hamiltonian_curl",
            "source_status": "HTAU_INTEGRABILITY_CURL_OPEN",
            "observable_links": "clocks; orbital timing; Newton source stability; PPN conservation channels",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CGLUE4012_3_I_commutator",
            "coefficient": "I_commutator",
            "formula": "M_H_ref^-1 |int_A [d,Pi_M^C]J_H|",
            "value": "ZERO_IF_PARENT_CHAINMAP_FIXED_ELSE_MISSING_OPERATOR_BOUND",
            "units": "dimensionless_projector_current_commutator",
            "source_status": "CHAINMAP_DOMAIN_UNSIGNED",
            "observable_links": "Newton source; R10; WEP/source composition; PPN conservation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CGLUE4012_4_R_eq",
            "coefficient": "R_eq",
            "formula": "Pi_M^C J_H - J_M_top - dB_zero on the same M_H_ref denominator",
            "value": "ZERO_IF_SAME_CHARGE_CONSTRAINT_MAP_SIGNED_ELSE_MISSING_EQUALITY_BOUND",
            "units": "dimensionless_charge_equality_residual",
            "source_status": "HILBERT_TOPOLOGICAL_EQUALITY_UNSIGNED",
            "observable_links": "Newton GM; orbital mass; R10 alpha normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CGLUE4012_5_constraint_kernel",
            "coefficient": "R_kernel_plus_R_extra",
            "formula": "|R_kernel|+|R_extra| from non-unique constraint Green map, homogeneous mass mode, extra sector source shadow",
            "value": "MISSING_CONSTRAINT_UNIQUENESS_AND_EXTRA_SECTOR_SILENCE",
            "units": "dimensionless_extra_charge_fraction",
            "source_status": "CONSTRAINT_KERNEL_OPEN",
            "observable_links": "Newton source; galaxy/cosmology separation; local fifth-force tests",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CGLUE4012_6_reference_frame_units",
            "coefficient": "C_ref_plus_C_frame_plus_C_units",
            "formula": "|C_ref|+|D_X ln(tau,e_obs,Sigma,frame)|+|D_X ln(Pi_M H_tau units)|",
            "value": "MISSING_REFERENCE_FRAME_DENOMINATOR_LOCK",
            "units": "dimensionless_reference_frame_units",
            "source_status": "REFERENCE_FRAME_UNITS_OPEN",
            "observable_links": "clocks; orbital timing; PPN preferred-frame; source normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CGLUE4012_7_boundary_symplectic",
            "coefficient": "R_symp_plus_R_boundary",
            "formula": "|int_S i_tau omega_extra|/|Pi_M H_tau| + |corner_tau|/|Pi_M H_tau| + |boundary/reference flux|",
            "value": "MISSING_EXACT_OR_ZERO_BOUNDARY_SYMPLECTIC_FLUX",
            "units": "dimensionless_boundary_symplectic_flux",
            "source_status": "BOUNDARY_SYMPLECTIC_GATE_OPEN",
            "observable_links": "local conservation; clocks; PPN alpha/zeta channels",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CGLUE4012_8_EM_flux",
            "coefficient": "R_EM_flux",
            "formula": "net radiative/background Poynting plus EM Hilbert stress accounting mismatch divided by M_H_ref",
            "value": "MISSING_MAXWELL_POYNTING_HILBERT_STRESS_ONCE_ONLY_THEOREM",
            "units": "dimensionless_EM_source_flux",
            "source_status": "OPEN_CRITICAL_GUARD",
            "observable_links": "EM; clocks; source mass; energy conservation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "CGLUE4012_9_G_PPN",
            "coefficient": "epsilon_G_norm_plus_epsilon_PPN_source",
            "formula": "|lambda_PiM_EH-1| + epsilon_universal_G_normalization + epsilon_PPN_source_stability",
            "value": "MISSING_UNIVERSAL_G_AND_SECOND_ORDER_SOURCE_STABILITY",
            "units": "dimensionless_calibration_and_PPN_fraction",
            "source_status": "NOT_LOCAL_GR_CLAIM_READY",
            "observable_links": "Newton G; PPN beta/gamma/preferred-frame; orbital systems",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "constraint_map": True,
        "chainmap_fixed": True,
        "Htau_exact": True,
        "MHref_qbasic": True,
        "same_charge": True,
        "EM_once": True,
        "G_norm": True,
        "PPN_stable": True,
        "numeric_pack": False,
    }
    cases = []

    def add(case_id: str, **overrides: bool) -> None:
        row = dict(base)
        row.update(overrides)
        row.update({"case_id": case_id, "valid_for_claim": False, "timestamp_utc": timestamp})
        cases.append(row)

    add("CASE4012_0_full_charge_lock_signed")
    add("CASE4012_1_constraint_map_open", constraint_map=False)
    add("CASE4012_2_chainmap_open", chainmap_fixed=False)
    add("CASE4012_3_Htau_curl_open", Htau_exact=False)
    add("CASE4012_4_MHref_qbasic_open", MHref_qbasic=False)
    add("CASE4012_5_same_charge_open", same_charge=False)
    add("CASE4012_6_EM_once_open", EM_once=False)
    add("CASE4012_7_G_PPN_open", G_norm=False, PPN_stable=False)
    add(
        "CASE4012_8_numeric_pack",
        constraint_map=False,
        chainmap_fixed=False,
        Htau_exact=False,
        MHref_qbasic=False,
        same_charge=False,
        EM_once=False,
        G_norm=False,
        PPN_stable=False,
        numeric_pack=True,
    )
    return cases


def result_for_case(row: dict[str, Any], timestamp: str) -> dict[str, Any]:
    if bool(row["numeric_pack"]):
        return {
            "case_id": row["case_id"],
            "charge_status": "FINITE_CHARGE_GLUE_PACK_NONCLAIM",
            "commutator_result": "C_M+C_curl+I_commutator+R_eq+EM_G_PPN_VECTOR_REQUIRED",
            "local_GR_result": "NO_LOCAL_GR_PROMOTION",
            "next_action": "fill source-backed charge, curl, commutator, EM-flux, G-normalization and PPN-stability rows",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    blockers: list[str] = []
    if not bool(row["constraint_map"]):
        blockers.extend(["R_kernel", "R_extra"])
    if not bool(row["chainmap_fixed"]):
        blockers.append("I_commutator")
    if not bool(row["Htau_exact"]):
        blockers.append("C_curl")
    if not bool(row["MHref_qbasic"]):
        blockers.extend(["C_M", "C_units"])
    if not bool(row["same_charge"]):
        blockers.append("R_eq")
    if not bool(row["EM_once"]):
        blockers.append("R_EM_flux")
    if not bool(row["G_norm"]):
        blockers.append("epsilon_G_norm")
    if not bool(row["PPN_stable"]):
        blockers.append("epsilon_PPN_source")

    if not blockers:
        return {
            "case_id": row["case_id"],
            "charge_status": "CONDITIONAL_PIM_HTAU_SOURCE_CHARGE_LOCK",
            "commutator_result": "C_M_C_curl_I_commutator_R_eq_ZERO_IF_PARENT_BRANCH_SIGNED",
            "local_GR_result": "NEWTON_SOURCE_CHARGE_CONDITIONAL_NOT_FULL_PPN_CLAIM",
            "next_action": "move to Maxwell/Poynting once-only Hilbert stress and then second-order PPN source stability",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    return {
        "case_id": row["case_id"],
        "charge_status": "CHARGE_LOCK_BLOCKED",
        "commutator_result": "+".join(blockers),
        "local_GR_result": "NO_LOCAL_GR_PROMOTION",
        "next_action": "retain " + "+".join(blockers) + " as finite nonclaim rows",
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    return [result_for_case(row, timestamp) for row in cases]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4012_0_conditional_derivation",
            "decision": "Pi_M/H_tau charge lock has a real conditional route",
            "reason": "construct Pi_M from the parent constraint/boundary-charge map, prove chain-map fixedness, H_tau exactness, M_H_ref q-basicity and same-charge equality",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4012_1_no_promotion",
            "decision": "do not promote Newton/local-GR/R10/PPN claim",
            "reason": "constraint-map uniqueness, H_tau curl, same-charge equality, EM/Poynting once-only accounting, G normalization and PPN stability are not all parent-signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4012_2_finite_policy",
            "decision": "if charge lock fails, retain explicit charge-glue vector",
            "reason": "C_M, C_curl, I_commutator, R_eq, reference/frame/unit, EM flux, G normalization and PPN source terms have distinct observable projections",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4012_3_next",
            "decision": "next target is Maxwell/Poynting Hilbert stress once-only lock",
            "reason": "4012 reduces source coupling to a parent-owned charge theorem, and the most concrete live physics input is whether EM stress/Poynting/binding energy enters J_H_total once and only once",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM4012_0_Newton",
            "arena": "Newtonian_source_coupling",
            "allowed": False,
            "reason": "charge equality is conditional and universal G_ref normalization remains open",
            "blocking_rows": "CGLUE4012_4_R_eq;CGLUE4012_9_G_PPN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4012_1_local_GR_PPN",
            "arena": "local_GR_PPN",
            "allowed": False,
            "reason": "first-order charge lock is not second-order PPN stability",
            "blocking_rows": "CGLUE4012_7_boundary_symplectic;CGLUE4012_9_G_PPN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4012_2_R10_WEP",
            "arena": "R10_WEP_source_charge",
            "allowed": False,
            "reason": "source charge residual rows lack numeric arena projection and same-charge proof",
            "blocking_rows": "CGLUE4012_1_C_M;CGLUE4012_3_I_commutator;CGLUE4012_4_R_eq",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4012_3_EM",
            "arena": "EM_Maxwell_stress",
            "allowed": False,
            "reason": "Maxwell/Poynting Hilbert stress once-only accounting is still a live guard",
            "blocking_rows": "CGLUE4012_8_EM_flux",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4012_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive Maxwell/Poynting/binding energy as a once-only contribution to the parent Hilbert source current J_H_total, or retain I_matter_EM/R_EM_flux rows",
            "success_condition": "J_H_total=J_matter+J_EM+J_Poynting+J_binding+dB_zero is parent-derived from the same observed coframe, has no double counting, and its stationary/radiative flux split is explicit before Newton/PPN/R10 scoring",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "Pi_M/H_tau source charge lock derived as a strict conditional parent constraint-map theorem; surviving coupling obstruction is an explicit charge-glue vector, with EM/Poynting once-only as next concrete physics target",
            "current_best_next": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    lines = [
        "# 4012 - Pi_M/H_tau Source-Current Commutator Lock Or C_M/C_curl Row",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "The clean route is now a parent constraint-map theorem, not an empirical `GM` definition:",
        "",
        "`Pi_M^C := D_N[C_tau]|_{J_H[tau]}`",
        "",
        "`Delta_charge := M_H[Pi_M^C J_H] - (H_tau[S_outer]-H_ref)`.",
        "",
        "If `Pi_M^C` is parent-selected, fixed as a chain map, `H_tau` is exact, `M_H_ref` is q-basic, the constraint map has no homogeneous mass kernel, and exact/boundary/EM terms have owned zero-flux accounting, then `C_M=0`, `C_curl=0`, `[d,Pi_M]J_H=0`, and `R_eq=0`.",
        "",
        "This is a genuine derivation path to calibrated source coupling. It is still not a public Newton/local-GR claim, because the parent signatures are not all adopted and the EM/Poynting source term remains live.",
        "",
        "## Charge-Glue Vector",
        "",
        "If the theorem branch is not adopted, the retained vector is",
        "",
        "`epsilon_charge_4012 <= |C_M|+|C_curl|+|I_commutator|+|R_eq|+|C_ref|+|C_frame|+|C_units|+|R_kernel|+|R_extra|+|R_symp|+|R_boundary|+|R_EM_flux|+|epsilon_G_norm|+|epsilon_PPN_source|`.",
        "",
        "No fitted orbital `GM` is allowed to define the charge it is supposed to test.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: charge=`{row['charge_status']}`, commutator=`{row['commutator_result']}`, local_GR=`{row['local_GR_result']}`, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "4012 moves the coupling problem forward: the source mass can be made the same object as the Hamiltonian charge only through a parent constraint-map lock. The live physics bottleneck is now concrete: EM/Poynting/binding energy must enter the Hilbert source exactly once.",
            "",
            "## Next Target",
            "",
            f"- `{NEXT_DOC}`",
            f"- `{NEXT_SCRIPT}`",
            "",
            "## Source Count",
            "",
            f"- source needles found: `{found}/{len(sources)}`",
            "",
        ]
    )
    DOC_PATH.write_text("\n".join(lines), encoding="utf-8")


def append_spine(timestamp: str) -> None:
    marker = "## 4012 - Pi_M/H_tau Charge Lock"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: `Pi_M^C := D_N[C_tau]|_{{J_H[tau]}}` gives a non-circular parent constraint-map route to `M_H[Pi_M^C J_H]=H_tau[S_outer]-H_ref`.
- Conditional zero: fixed chain-map `Pi_M`, exact `H_tau`, q-basic positive `M_H_ref`, parent-owned support/domain, fixed reference/frame/units, no constraint kernel and zero-flux exact terms give `C_M=C_curl=I_commutator=R_eq=0`.
- No fitted-GM laundering: orbital `GM` may test `G_ref M_H_ref`; it cannot define `M_H_ref`.
- Finite fallback: `epsilon_charge_4012 <= |C_M|+|C_curl|+|I_commutator|+|R_eq|+|C_ref|+|C_frame|+|C_units|+|R_kernel|+|R_extra|+|R_symp|+|R_boundary|+|R_EM_flux|+|epsilon_G_norm|+|epsilon_PPN_source|`.
- No claim: Newton/local-GR/R10/PPN promotion remains blocked until parent signatures, EM/Poynting once-only accounting, G normalization and PPN stability close.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4012 - Pi_M/H_tau Charge Lock" in read_text(SPINE_PATH)


def build_validation_rows(
    timestamp: str,
    sources: list[dict[str, Any]],
    theorem: list[dict[str, Any]],
    audit: list[dict[str, Any]],
    finite: list[dict[str, Any]],
    results: list[dict[str, Any]],
    compile_ok: bool,
) -> list[dict[str, Any]]:
    checks: list[dict[str, Any]] = []

    def add(check_id: str, passed: bool, detail: str) -> None:
        checks.append({"check_id": check_id, "passed": bool(passed), "detail": detail, "timestamp_utc": timestamp})

    add("VAL4012_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4012_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, theorem_id in enumerate(
        [
            "CHG4012_0_parent_constraint_map",
            "CHG4012_1_chainmap_commutator_zero",
            "CHG4012_2_Htau_curl_zero",
            "CHG4012_3_MHref_qbasic_CM_zero",
            "CHG4012_4_same_charge_equality",
            "CHG4012_5_double_zero_branch",
            "CHG4012_6_charge_glue_finite_vector",
        ],
        start=2,
    ):
        add(f"VAL4012_{idx:02d}_theorem_{idx}", any(row["theorem_id"] == theorem_id for row in theorem), f"{theorem_id} present")
    add("VAL4012_09_audit_constraint", any(row["audit_id"] == "CGA4012_0_parent_constraint_map" for row in audit), "constraint-map audit present")
    add("VAL4012_10_audit_Htau", any(row["audit_id"] == "CGA4012_2_Htau_integrability" for row in audit), "H_tau audit present")
    add("VAL4012_11_audit_same_charge", any(row["audit_id"] == "CGA4012_4_same_charge" for row in audit), "same-charge audit present")
    add("VAL4012_12_audit_EM", any(row["audit_id"] == "CGA4012_5_EM_Poynting_source" for row in audit), "EM/Poynting audit present")
    add("VAL4012_13_audit_GPPN", any(row["audit_id"] == "CGA4012_7_PPN_stability" for row in audit), "PPN audit present")
    master = next(row for row in finite if row["row_id"] == "CGLUE4012_0_master")
    add("VAL4012_14_master_vector", "R_EM_flux" in master["formula"] and "epsilon_PPN_source" in master["formula"], "master vector contains EM and PPN guards")
    for idx, row_id in enumerate(
        [
            "CGLUE4012_1_C_M",
            "CGLUE4012_2_C_curl",
            "CGLUE4012_3_I_commutator",
            "CGLUE4012_4_R_eq",
            "CGLUE4012_5_constraint_kernel",
            "CGLUE4012_6_reference_frame_units",
            "CGLUE4012_7_boundary_symplectic",
            "CGLUE4012_8_EM_flux",
            "CGLUE4012_9_G_PPN",
        ],
        start=15,
    ):
        add(f"VAL4012_{idx:02d}_{row_id}", any(row["row_id"] == row_id for row in finite), f"{row_id} present")
    full = next(row for row in results if row["case_id"] == "CASE4012_0_full_charge_lock_signed")
    constraint_open = next(row for row in results if row["case_id"] == "CASE4012_1_constraint_map_open")
    chainmap_open = next(row for row in results if row["case_id"] == "CASE4012_2_chainmap_open")
    curl_open = next(row for row in results if row["case_id"] == "CASE4012_3_Htau_curl_open")
    mhref_open = next(row for row in results if row["case_id"] == "CASE4012_4_MHref_qbasic_open")
    same_open = next(row for row in results if row["case_id"] == "CASE4012_5_same_charge_open")
    em_open = next(row for row in results if row["case_id"] == "CASE4012_6_EM_once_open")
    gppn_open = next(row for row in results if row["case_id"] == "CASE4012_7_G_PPN_open")
    numeric_case = next(row for row in results if row["case_id"] == "CASE4012_8_numeric_pack")
    add("VAL4012_24_full_case", full["commutator_result"] == "C_M_C_curl_I_commutator_R_eq_ZERO_IF_PARENT_BRANCH_SIGNED", "full signed case conditionally zeros charge rows")
    add("VAL4012_25_constraint_case", "R_kernel" in constraint_open["commutator_result"], "constraint-map open routes to kernel rows")
    add("VAL4012_26_chainmap_case", chainmap_open["commutator_result"] == "I_commutator", "chainmap open routes to I_commutator")
    add("VAL4012_27_curl_case", curl_open["commutator_result"] == "C_curl", "H_tau curl open routes to C_curl")
    add("VAL4012_28_mhref_case", "C_M" in mhref_open["commutator_result"], "M_H_ref q-basic open routes to C_M")
    add("VAL4012_29_same_case", same_open["commutator_result"] == "R_eq", "same-charge open routes to R_eq")
    add("VAL4012_30_em_case", em_open["commutator_result"] == "R_EM_flux", "EM open routes to R_EM_flux")
    add("VAL4012_31_gppn_case", "epsilon_G_norm" in gppn_open["commutator_result"] and "epsilon_PPN_source" in gppn_open["commutator_result"], "G/PPN open routed")
    add("VAL4012_32_numeric_case", numeric_case["charge_status"] == "FINITE_CHARGE_GLUE_PACK_NONCLAIM", "numeric pack remains nonclaim")
    add("VAL4012_33_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4012_34_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4012_35_doc_exists", DOC_PATH.exists() and "No fitted orbital `GM`" in read_text(DOC_PATH), "document written with anti-laundering guard")
    add("VAL4012_36_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4012_37_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4012_38_compile", compile_ok, "script compiles")
    add("VAL4012_39_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
    output_tables = [
        sources,
        theorem,
        audit,
        finite,
        results,
        read_csv(OUTPUTS["decision"]),
        read_csv(OUTPUTS["claim_gate"]),
        read_csv(OUTPUTS["next"]),
        read_csv(OUTPUTS["status"]),
    ]
    add("VAL4012_40_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4012_41_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4012_42_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4012_43_forward_target", "Maxwell" in read_text(OUTPUTS["next"]) and "Poynting" in read_text(OUTPUTS["next"]), "forward target is Maxwell/Poynting once-only lock")
    return checks


def main() -> None:
    timestamp = now_utc()
    sources = source_register_rows(timestamp)
    theorem = theorem_rows(timestamp)
    audit = audit_rows(timestamp)
    finite = finite_rows(timestamp)
    cases = case_rows(timestamp)
    results = result_rows(cases, timestamp)
    decisions = decision_rows(timestamp)
    claims = claim_gate_rows(timestamp)
    next_target = next_rows(timestamp)
    status = status_rows(timestamp)

    write_csv(OUTPUTS["sources"], sources)
    write_csv(OUTPUTS["theorem"], theorem)
    write_csv(OUTPUTS["audit"], audit)
    write_csv(OUTPUTS["finite"], finite)
    write_csv(OUTPUTS["cases"], cases)
    write_csv(OUTPUTS["results"], results)
    write_csv(OUTPUTS["decision"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next"], next_target)
    write_csv(OUTPUTS["status"], status)
    write_doc(timestamp, sources, results)
    append_spine(timestamp)

    compile_ok = True
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError:
        compile_ok = False
    cache = SCRIPT_PATH.parent / "__pycache__"
    if cache.exists():
        shutil.rmtree(cache)

    validation = build_validation_rows(timestamp, sources, theorem, audit, finite, results, compile_ok)
    write_csv(OUTPUTS["validation"], validation)
    passed = sum(1 for row in validation if row["passed"])
    total = len(validation)
    print(f"4012 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
