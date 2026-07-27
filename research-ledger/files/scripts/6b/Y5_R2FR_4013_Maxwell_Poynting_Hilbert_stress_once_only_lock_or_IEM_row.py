from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4013"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4013-Y5-R2FR-Maxwell-Poynting-Hilbert-stress-once-only-lock-or-IEM-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4013_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4013_MAXWELL_POYNTING_ONCE_ONLY_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4013_EM_STRESS_SOURCE_AUDIT.csv",
    "finite": SRC / "P8_Y5_R2FR_4013_EM_ONCE_ONLY_FINITE_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4013_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4013_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4013_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4013_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4013_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4013_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4013_VALIDATION.csv",
}

NEXT_DOC = "4014-Y5-R2FR-observed-Hodge-Maxwell-normalization-owner-or-CXF2-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4014_observed_Hodge_Maxwell_normalization_owner_or_CXF2_row.py"


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
        ("SRC4013_00_handoff", SRC / "P8_Y5_R2FR_4012_NEXT_TARGET.csv", "NEXT4012_0", "4012 handoff"),
        ("SRC4013_01_charge_theorem", SRC / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv", "CHG4012_4_same_charge_equality", "4012 charge equality theorem"),
        ("SRC4013_02_charge_vector", SRC / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv", "CHG4012_6_charge_glue_finite_vector", "4012 charge finite vector"),
        ("SRC4013_03_EM_audit", SRC / "P8_Y5_R2FR_4012_CHARGE_LOCK_AUDIT.csv", "CGA4012_5_EM_Poynting_source", "4012 EM/Poynting audit"),
        ("SRC4013_04_EM_row", SRC / "P8_Y5_R2FR_4012_CHARGE_GLUE_FINITE_ROWS.csv", "CGLUE4012_8_EM_flux", "4012 EM flux row"),
        ("SRC4013_05_4012_decision", SRC / "P8_Y5_R2FR_4012_DECISION_GATE.csv", "DEC4012_3_next", "4012 next decision"),
        ("SRC4013_06_EMF_bound", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_0_minimal_bound_field_stress", "minimal bound EM stress"),
        ("SRC4013_07_EMF_flux", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_1_radiative_poynting_flux", "radiative Poynting flux"),
        ("SRC4013_08_EMF_XF2", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_2_nonminimal_XF2", "nonminimal hidden F2"),
        ("SRC4013_09_EMF_wEM", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_3_EM_normalization_multiplier", "EM normalization multiplier"),
        ("SRC4013_10_EMF_hodge", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_4_observed_Hodge_flow_rule", "observed Hodge flow rule"),
        ("SRC4013_11_EMF_exchange", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_5_matter_EM_internal_exchange", "matter-EM exchange"),
        ("SRC4013_12_EMF_readout", SRC / "P8_EM_Poynting_source_flux_or_cross_term_vector.csv", "EMF3502_6_readout_radiative_regeneration", "readout radiative regeneration"),
        ("SRC4013_13_EMB_hodge", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_0_Delta_Hodge_EM", "Hodge bound vector"),
        ("SRC4013_14_EMB_wEM", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_1_w_EM", "w_EM bound vector"),
        ("SRC4013_15_EMB_CXF2", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_2_C_XF2", "C_XF2 bound vector"),
        ("SRC4013_16_EMB_flux", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_4_Phi_EM_rad", "Phi_EM_rad bound vector"),
        ("SRC4013_17_EMB_Jtotal", SRC / "P8_EM_Hodge_Maxwell_current_owner_bound_vector.csv", "EMB3503_6_Delta_J_total", "total current closure"),
        ("SRC4013_18_status_hodge", SRC / "P8_EM_source_label_forgetting_EM_Hodge_status.csv", "STAT3523_1_EM_Poynting_route", "Poynting as Maxwell stress status"),
        ("SRC4013_19_status_alpha", SRC / "P8_local_GR_calibrated_alpha_source_interface_status.csv", "STAT3529_1_EM_stress", "calibrated Maxwell stress status"),
        ("SRC4013_20_3883_stress", SRC / "P8_Y5_R2FR_3883_MAXWELL_STRESS_POYNTING_DERIVATION.csv", "MX3883_1_stress", "Maxwell Hilbert stress derivation"),
        ("SRC4013_21_3883_exchange", SRC / "P8_Y5_R2FR_3883_MAXWELL_STRESS_POYNTING_DERIVATION.csv", "MX3883_3_exchange", "matter-EM exchange cancellation"),
        ("SRC4013_22_3883_poynting", SRC / "P8_Y5_R2FR_3883_MAXWELL_STRESS_POYNTING_DERIVATION.csv", "MX3883_4_poynting", "Poynting accounting"),
        ("SRC4013_23_3883_guard", SRC / "P8_Y5_R2FR_3883_MAXWELL_STRESS_POYNTING_DERIVATION.csv", "MX3883_5_nonminimal_guard", "nonminimal EM guard"),
        ("SRC4013_24_HSL_source", SRC / "P8_Y5_R2FR_3883_SAME_HILBERT_SOURCE_LOCK.csv", "HSL3883_1_Hilbert_definition", "same Hilbert stress definition"),
        ("SRC4013_25_HSL_conservation", SRC / "P8_Y5_R2FR_3883_SAME_HILBERT_SOURCE_LOCK.csv", "HSL3883_4_conservation", "total stress conservation"),
        ("SRC4013_26_MER_hodge", SRC / "P8_Y5_R2FR_3883_MATTER_EM_RESIDUAL_VECTOR.csv", "MER3883_2_Delta_Hodge_EM", "3883 Hodge residual"),
        ("SRC4013_27_MER_flux", SRC / "P8_Y5_R2FR_3883_MATTER_EM_RESIDUAL_VECTOR.csv", "MER3883_6_Phi_EM_rad", "3883 Poynting residual"),
        ("SRC4013_28_MER_Jtotal", SRC / "P8_Y5_R2FR_3883_MATTER_EM_RESIDUAL_VECTOR.csv", "MER3883_7_Delta_J_total", "3883 J_total residual"),
        ("SRC4013_29_3900_minimal", SRC / "P8_Y5_R2FR_3900_MAXWELL_EM_STRESS_CALIBRATION_GATE.csv", "EM3900_0_minimal_Maxwell", "3900 minimal Maxwell"),
        ("SRC4013_30_3900_poynting", SRC / "P8_Y5_R2FR_3900_MAXWELL_EM_STRESS_CALIBRATION_GATE.csv", "EM3900_1_Poynting", "3900 Poynting flux"),
        ("SRC4013_31_3930_total", SRC / "P8_Y5_R2FR_3930_POYNTING_BOUNDARY_GUARD.csv", "PYG3930_0_total_system", "total system Poynting guard"),
        ("SRC4013_32_3930_internal", SRC / "P8_Y5_R2FR_3930_POYNTING_BOUNDARY_GUARD.csv", "PYG3930_1_internal_flow_allowed", "internal flow allowed"),
        ("SRC4013_33_3941_bound", SRC / "P8_Y5_R2FR_3941_MAXWELL_STRESS_INCLUSION_ROWS.csv", "EM3941_0_bound_field", "bound field inside source"),
        ("SRC4013_34_3941_flux", SRC / "P8_Y5_R2FR_3941_MAXWELL_STRESS_INCLUSION_ROWS.csv", "EM3941_1_radiative_flux", "radiative flux retained"),
        ("SRC4013_35_3946_current", SRC / "P8_Y5_R2FR_3946_CONSERVATION_CURRENT_THEOREM.csv", "CCT3946_1_divergence_identity", "source current divergence identity"),
        ("SRC4013_36_3946_balance", SRC / "P8_Y5_R2FR_3946_CONSERVATION_CURRENT_THEOREM.csv", "CCT3946_2_worldtube_balance", "worldtube energy balance"),
        ("SRC4013_37_3946_flux", SRC / "P8_Y5_R2FR_3946_POYNTING_AND_WALL_FLUX_BOUND_LAW.csv", "FLX3946_1_Poynting", "Poynting flux bound"),
        ("SRC4013_38_3947_placement", SRC / "P8_Y5_R2FR_3947_TOTAL_HILBERT_POSITIVE_ENERGY_THEOREM.csv", "PET3947_4_EM_and_Poynting_placement", "EM/Poynting placement"),
        ("SRC4013_39_3960_visible", SRC / "P8_Y5_R2FR_3960_EM_POYNTING_F2_GATE.csv", "EMG3960_0_visible_Maxwell", "visible Maxwell stress"),
        ("SRC4013_40_3960_exchange", SRC / "P8_Y5_R2FR_3960_EM_POYNTING_F2_GATE.csv", "EMG3960_1_internal_exchange", "internal exchange zero"),
        ("SRC4013_41_3960_flux", SRC / "P8_Y5_R2FR_3960_EM_POYNTING_F2_GATE.csv", "EMG3960_3_Poynting_flux", "Poynting flux gate"),
        ("SRC4013_42_3961_identity", SRC / "P8_Y5_R2FR_3961_POYNTING_NO_FLUX_THEOREM_OR_BOUND.csv", "PNF3961_0_identity", "Poynting identity"),
        ("SRC4013_43_3961_zero", SRC / "P8_Y5_R2FR_3961_POYNTING_NO_FLUX_THEOREM_OR_BOUND.csv", "PNF3961_1_stationary_zero", "stationary Poynting zero"),
        ("SRC4013_44_3978_total", SRC / "P8_Y5_R2FR_3978_POYNTING_INCLUSION_CONTRACT.csv", "PIC3978_0_total_source", "total source contract"),
        ("SRC4013_45_3978_noclaim", SRC / "P8_Y5_R2FR_3978_POYNTING_INCLUSION_CONTRACT.csv", "PIC3978_4_no_charge_claim", "not EM unification proof"),
        ("SRC4013_46_3981_branch", SRC / "P8_Y5_R2FR_3981_CONTROLLED_POYNTING_SILENCE_THEOREM.csv", "CPS3981_0_branch", "controlled Poynting silence"),
        ("SRC4013_47_3993_map", SRC / "P8_Y5_R2FR_3993_EM_POYNTING_MAP_LEDGER.csv", "EMDD3993_2_radiative_poynting", "Poynting map ledger"),
        ("SRC4013_48_3994_bound", SRC / "P8_Y5_R2FR_3994_POYNTING_FLUX_ZERO_OR_BOUND_ROWS.csv", "PY3994_2_flux_bound", "Poynting flux bound rows"),
        ("SRC4013_49_4000_action", SRC / "P8_Y5_R2FR_4000_EM_STRESS_POYNTING_THEOREM.csv", "EMP4000_0_Maxwell_action_branch", "4000 Maxwell action branch"),
        ("SRC4013_50_4000_stress", SRC / "P8_Y5_R2FR_4000_EM_STRESS_POYNTING_THEOREM.csv", "EMP4000_1_Hilbert_stress_inclusion", "4000 stress inclusion"),
        ("SRC4013_51_4000_poynting", SRC / "P8_Y5_R2FR_4000_EM_STRESS_POYNTING_THEOREM.csv", "EMP4000_2_Poynting_as_stress_flux", "4000 Poynting stress flux"),
        ("SRC4013_52_4000_exchange", SRC / "P8_Y5_R2FR_4000_EM_STRESS_POYNTING_THEOREM.csv", "EMP4000_3_internal_exchange_cancellation", "4000 exchange cancellation"),
        ("SRC4013_53_4000_bound", SRC / "P8_Y5_R2FR_4000_EM_STRESS_POYNTING_THEOREM.csv", "EMP4000_5_radiative_bound", "4000 radiative bound"),
        ("SRC4013_54_4003_EM", SRC / "P8_Y5_R2FR_4003_INTEGRABILITY_COMPONENT_BOUND_VECTOR.csv", "PCB4003_5_I_matter_EM", "4003 matter/EM integrability component"),
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
            "theorem_id": "MPE4013_0_total_visible_action",
            "claim_piece": "same-action matter plus Maxwell source",
            "mathematical_form": "S_source = S_ord[psi,e_obs] - (1/(4 mu0)) int F wedge *_obs F + int A.J[psi,e_obs] + S_binding + dB",
            "derived_result": "ordinary matter, Maxwell fields and binding terms must be varied together against the same observed coframe before source support, Pi_M, orbital GM or readout are applied",
            "status": "CONDITIONAL_PARENT_ACTION_PACKET",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MPE4013_1_Maxwell_Hilbert_stress",
            "claim_piece": "EM stress inside J_H_total",
            "mathematical_form": "T_EM^{ab}=(1/mu0)(F^{a c}F^b_c - (1/4)g_obs^{ab}F_cd F^cd); J_H_total[tau]=-T_total^a_b tau^b epsilon_a",
            "derived_result": "bound/local Maxwell field energy, pressure, momentum density and stress contribute to the Hilbert source once; they are not a separate fitted mass channel",
            "status": "EXACT_IF_OBSERVED_HODGE_AND_NORMALIZATION_OWNED",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MPE4013_2_internal_exchange_cancellation",
            "claim_piece": "matter-EM Lorentz exchange is internal",
            "mathematical_form": "nabla_a T_EM^{ab}=-F^{bc}J_c and nabla_a T_matter^{ab}=+F^{bc}J_c, hence nabla_a(T_matter+T_EM)^{ab}=0 up to parent extra/boundary/radiative channels",
            "derived_result": "matter-only source tubes are the wrong object; total matter+EM Hilbert stress is the conserved source current",
            "status": "EXACT_BOOKKEEPING_IF_SAME_CURRENT_OWNER",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MPE4013_3_Poynting_flux_placement",
            "claim_piece": "Poynting is source-current flux, not an added force",
            "mathematical_form": "dU_EM/dt + int_boundary S_Poynting.n dA = -int_W J.E dV; internal S_Poynting may circulate, but only boundary/radiative flux changes M_H",
            "derived_result": "the Poynting-vector intuition is legitimate when treated as Hilbert source-current flow; stationary closed branches can zero net leakage, open/radiative branches require a flux row",
            "status": "EXACT_IDENTITY_WITH_BRANCH_CONDITION",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MPE4013_4_once_only_rule",
            "claim_piece": "no double counting and no deletion",
            "mathematical_form": "J_H_total = J_matter + J_EM + J_binding + J_apparatus + dB_zero, with bound EM stress inside J_EM and Phi_EM_rad only if flux crosses the chosen worldtube boundary",
            "derived_result": "EM is counted once: not zero times by using matter-only mass, not twice by adding Poynting as extra after already varying Maxwell stress",
            "status": "CONDITIONAL_ONCE_ONLY_SOURCE_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MPE4013_5_no_flux_branch",
            "claim_piece": "stationary isolated local branch",
            "mathematical_form": "time_avg(dU_EM/dt)=0 and time_avg(int_W J.E dV)=0 imply time_avg(Phi_EM_rad)=0; controlled neutral/nonradiating exterior also has T_EM|Omega_ext=0",
            "derived_result": "Poynting leakage can be theorem-zero only on a stated stationary/controlled branch, never universally",
            "status": "BRANCH_SPECIFIC_ZERO_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "MPE4013_6_finite_EM_vector",
            "claim_piece": "finite fallback if once-only lock fails",
            "mathematical_form": "epsilon_EM_once_4013 <= |Delta_Hodge_EM|+|w_EM-1|+|C_XF2|+|C_JQ|+|Phi_EM_rad|/(G_ref M_H)+|C_EM_readout|+|Delta_J_total|+|epsilon_binding_once|+|C_Poynting_units|",
            "derived_result": "open EM/Poynting terms are now one finite residual vector with no hidden deletion, no double counting and no claim promotion",
            "status": "FINITE_EM_ONCE_ONLY_VECTOR_DERIVED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "ESA4013_0_same_observed_coframe",
            "clause": "Maxwell Hodge, matter stress, clocks/source support and local readout use the same e_obs/q branch",
            "current_status": "OBSERVED_HODGE_PARENT_SIGNATURE_UNSIGNED",
            "risk_if_open": "EM stress may source a different geometry than the local GR/Newton branch",
            "next_action": "derive observed Hodge/Maxwell normalization owner in 4014 or keep Delta_Hodge_EM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ESA4013_1_unique_Maxwell_normalization",
            "clause": "Maxwell kinetic coefficient and charge/current normalization are parent-owned",
            "current_status": "W_EM_CJQ_CXF2_OPEN",
            "risk_if_open": "EM field energy rescales source mass, alpha, clocks and WEP response",
            "next_action": "exclude independent F2/dual-F2/source-current normalization or retain w_EM/C_XF2/C_JQ",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ESA4013_2_total_Hilbert_variation",
            "clause": "matter, EM, binding and apparatus terms are varied once in J_H_total before readout",
            "current_status": "CONDITIONAL_PACKET_EXISTS_NOT_FINAL_PARENT_ADOPTED",
            "risk_if_open": "bound EM energy is either omitted from source mass or added twice after variation",
            "next_action": "adopt total-source action grammar or retain epsilon_binding_once/Delta_J_total",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ESA4013_3_internal_exchange",
            "clause": "Lorentz force exchange is internal to total matter+EM stress",
            "current_status": "EXACT_IF_SAME_CURRENT_OWNER",
            "risk_if_open": "matter-only Ward failure is mistaken for a new force",
            "next_action": "bind J_current owner to Maxwell action or keep C_JQ/internal-exchange row",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ESA4013_4_Poynting_boundary_flux",
            "clause": "only net boundary/radiative Poynting flux changes source Hamiltonian mass",
            "current_status": "STATIONARY_ZERO_OR_FLUX_BOUND_REQUIRED",
            "risk_if_open": "internal Poynting is incorrectly set to zero or crossing flux is hidden",
            "next_action": "state stationary/no-flux branch or fill Phi_EM_rad bound",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ESA4013_5_Poynting_units_convention",
            "clause": "relation between T_EM^{0i} and S_Poynting has a declared c-convention",
            "current_status": "CONVENTION_GUARD_ADDED",
            "risk_if_open": "source-flux rows can be off by powers of c",
            "next_action": "declare c_T convention before numeric Poynting flux scoring",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "ESA4013_6_not_EM_unification_claim",
            "clause": "Poynting inclusion does not derive charge, alpha, Coulomb law or Maxwell emergence",
            "current_status": "OVERCLAIM_GUARD_ACTIVE",
            "risk_if_open": "source-stress bookkeeping is oversold as EM unification",
            "next_action": "keep EM-origin claims separate from source-current accounting",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def finite_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "EMO4013_0_master",
            "coefficient": "epsilon_EM_once_4013",
            "formula": "|Delta_Hodge_EM|+|w_EM-1|+|C_XF2|+|C_JQ|+|Phi_EM_rad|/(G_ref M_H)+|C_EM_readout|+|Delta_J_total|+|epsilon_binding_once|+|C_Poynting_units|",
            "value": "MISSING_PARENT_SIGNED_OR_NUMERIC_COMPONENTS",
            "units": "dimensionless_fractional_EM_source_mismatch",
            "source_status": "FINITE_VECTOR_NONCLAIM",
            "observable_links": "Maxwell stress; Newton source; clocks; WEP; R10; PPN; source energy conservation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMO4013_1_bound_EM_inside_MH",
            "coefficient": "epsilon_EM_bound",
            "formula": "mu_EM_bound_fields/(G_ref M_H)",
            "value": "ZERO_RELATIVE_EXTRA_CHANNEL_IF_INCLUDED_ONCE_IN_J_H_TOTAL",
            "units": "dimensionless_bound_field_source_fraction",
            "source_status": "CONDITIONAL_INSIDE_MH_NOT_EXTRA",
            "observable_links": "Newton source mass; WEP; material binding; local energy",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMO4013_2_Phi_EM_rad",
            "coefficient": "Phi_EM_rad_over_GM",
            "formula": "Phi_EM_rad/(G_ref M_H), Phi_EM_rad=int_boundary S_Poynting.n dA",
            "value": "ZERO_IF_STATIONARY_ISOLATED_ELSE_MISSING_FLUX_BOUND",
            "units": "time^-1_or_dimensionless_over_window",
            "source_status": "RETAINED_FLUX_COEFFICIENT_REQUIRED",
            "observable_links": "Gdot/G; clock drift; source time hair; radiating systems",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMO4013_3_Delta_Hodge_EM",
            "coefficient": "Delta_Hodge_EM",
            "formula": "*_EM - *_obs[e_obs(q)] or chi_EM - chi_obs",
            "value": "MISSING_OBSERVED_HODGE_PARENT_SIGNATURE",
            "units": "dimensionless_or_tensor",
            "source_status": "HODGE_OWNER_OPEN",
            "observable_links": "Maxwell light cone; Poynting flow; clocks; PPN",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMO4013_4_wEM_CJQ",
            "coefficient": "w_EM_plus_C_JQ",
            "formula": "|w_EM-1| + |charge/current normalization ambiguity|",
            "value": "MISSING_MAXWELL_KINETIC_AND_CURRENT_OWNER",
            "units": "dimensionless_normalization",
            "source_status": "MAXWELL_NORMALIZATION_OPEN",
            "observable_links": "alpha_EM; binding energy; WEP; clocks; source normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMO4013_5_CXF2",
            "coefficient": "C_XF2",
            "formula": "hidden/motion/time field coefficient multiplying F^2 or F*F",
            "value": "MISSING_OPERATOR_DOMAIN_EXCLUSION_OR_BOUND",
            "units": "model_dependent",
            "source_status": "NONMINIMAL_EM_SOURCE_OPEN",
            "observable_links": "alpha_EM drift; fifth force; clocks; R10; WEP",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMO4013_6_C_EM_readout",
            "coefficient": "C_EM_readout",
            "formula": "effective readout/loop-induced f_X F^2, alpha_X, or EM binding response after reduction",
            "value": "MISSING_READOUT_CLOSURE_OR_BOUND",
            "units": "model_dependent",
            "source_status": "READOUT_RADIATIVE_REGENERATION_OPEN",
            "observable_links": "clock; WEP; spectroscopy; alpha_EM; source normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMO4013_7_Delta_J_total",
            "coefficient": "Delta_J_total",
            "formula": "dJ_H_total - (Delta_nonEH + Delta_frame + Delta_extra + Delta_boundary + Delta_radiative)",
            "value": "ZERO_IF_TOTAL_PARENT_VARIATION_AND_STATIONARY_SOURCE_FREE_EXTERIOR_CLOSE",
            "units": "current_divergence",
            "source_status": "TOTAL_CURRENT_CLOSURE_UNSIGNED",
            "observable_links": "D_r M_H; D_t M_H; Newton source; PPN conservation",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMO4013_8_binding_once",
            "coefficient": "epsilon_binding_once",
            "formula": "binding/apparatus/internal energy omitted from or double-counted in J_H_total, normalized by M_H",
            "value": "MISSING_BINDING_AND_APPARATUS_ONCE_ONLY_LEDGER",
            "units": "dimensionless_binding_source_fraction",
            "source_status": "BINDING_ONCE_ONLY_OPEN",
            "observable_links": "WEP; material source; Newton mass; clocks",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "row_id": "EMO4013_9_Poynting_units",
            "coefficient": "C_Poynting_units",
            "formula": "declared conversion between T_EM^{0i} and S_Poynting under x^0=t or x^0=ct conventions",
            "value": "MISSING_DECLARED_C_CONVENTION_FOR_NUMERIC_FLUX_ROWS",
            "units": "power_of_c_convention_guard",
            "source_status": "UNITS_GUARD_REQUIRED",
            "observable_links": "Poynting flux bounds; clock/Gdot source drift; EM stress normalization",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    base = {
        "same_hodge": True,
        "maxwell_norm": True,
        "same_current": True,
        "total_variation": True,
        "stationary_no_flux": True,
        "no_hidden_F2": True,
        "readout_closed": True,
        "binding_once": True,
        "units_declared": True,
        "numeric_pack": False,
    }
    cases: list[dict[str, Any]] = []

    def add(case_id: str, **overrides: bool) -> None:
        row = dict(base)
        row.update(overrides)
        row.update({"case_id": case_id, "valid_for_claim": False, "timestamp_utc": timestamp})
        cases.append(row)

    add("CASE4013_0_full_once_only_signed")
    add("CASE4013_1_Hodge_open", same_hodge=False)
    add("CASE4013_2_Maxwell_norm_open", maxwell_norm=False)
    add("CASE4013_3_current_owner_open", same_current=False)
    add("CASE4013_4_total_variation_open", total_variation=False)
    add("CASE4013_5_Poynting_flux_open", stationary_no_flux=False)
    add("CASE4013_6_hidden_F2_open", no_hidden_F2=False)
    add("CASE4013_7_readout_binding_units_open", readout_closed=False, binding_once=False, units_declared=False)
    add(
        "CASE4013_8_numeric_pack",
        same_hodge=False,
        maxwell_norm=False,
        same_current=False,
        total_variation=False,
        stationary_no_flux=False,
        no_hidden_F2=False,
        readout_closed=False,
        binding_once=False,
        units_declared=False,
        numeric_pack=True,
    )
    return cases


def result_for_case(row: dict[str, Any], timestamp: str) -> dict[str, Any]:
    if bool(row["numeric_pack"]):
        return {
            "case_id": row["case_id"],
            "em_source_status": "FINITE_EM_ONCE_ONLY_PACK_NONCLAIM",
            "source_result": "DELTA_HODGE+wEM+CJQ+CXF2+PHI_EM+CEM_READOUT+BINDING+UNITS_VECTOR_REQUIRED",
            "claim_result": "NO_NEWTON_LOCAL_GR_MAXWELL_PROMOTION",
            "next_action": "fill source-backed EM/Hodge/normalization/Poynting/binding rows or prove them zero",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    blockers: list[str] = []
    if not bool(row["same_hodge"]):
        blockers.append("Delta_Hodge_EM")
    if not bool(row["maxwell_norm"]):
        blockers.append("w_EM+C_JQ")
    if not bool(row["same_current"]):
        blockers.append("epsilon_internal_exchange")
    if not bool(row["total_variation"]):
        blockers.append("Delta_J_total")
    if not bool(row["stationary_no_flux"]):
        blockers.append("Phi_EM_rad")
    if not bool(row["no_hidden_F2"]):
        blockers.append("C_XF2")
    if not bool(row["readout_closed"]):
        blockers.append("C_EM_readout")
    if not bool(row["binding_once"]):
        blockers.append("epsilon_binding_once")
    if not bool(row["units_declared"]):
        blockers.append("C_Poynting_units")

    if not blockers:
        return {
            "case_id": row["case_id"],
            "em_source_status": "CONDITIONAL_MAXWELL_POYNTING_ONCE_ONLY_LOCK",
            "source_result": "BOUND_EM_INSIDE_JH_TOTAL_AND_PHI_EM_ZERO_ON_STATIONARY_BRANCH",
            "claim_result": "SOURCE_ACCOUNTING_LOCK_NOT_EM_UNIFICATION_OR_FULL_LOCAL_GR",
            "next_action": "move to observed Hodge/Maxwell normalization owner or Newton/Gauss bridge",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }

    return {
        "case_id": row["case_id"],
        "em_source_status": "EM_ONCE_ONLY_LOCK_BLOCKED",
        "source_result": "+".join(blockers),
        "claim_result": "NO_NEWTON_LOCAL_GR_MAXWELL_PROMOTION",
        "next_action": "retain " + "+".join(blockers) + " as finite nonclaim rows",
        "valid_for_claim": False,
        "timestamp_utc": timestamp,
    }


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    return [result_for_case(row, timestamp) for row in cases]


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4013_0_conditional_derivation",
            "decision": "Maxwell/Poynting once-only source accounting has a real derivation route",
            "reason": "minimal Maxwell variation gives Hilbert stress; matter-EM Lorentz exchange cancels in total stress; Poynting is boundary flux, not a separate post-hoc source term",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4013_1_no_promotion",
            "decision": "do not promote Newton/local-GR/Maxwell-source claim",
            "reason": "observed Hodge ownership, Maxwell normalization, hidden F2 exclusion, charge-current owner, readout closure and binding once-only remain unsigned",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4013_2_finite_policy",
            "decision": "if once-only lock fails, retain explicit EM source vector",
            "reason": "bound EM, radiative Poynting, Hodge, w_EM, hidden F2, current normalization, readout and binding terms have distinct observable projections",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4013_3_next",
            "decision": "next target is observed Hodge/Maxwell normalization owner",
            "reason": "the source-stress accounting route is now clear; the live EM bottleneck is whether the observed Hodge, Maxwell kinetic normalization and no-extra-F2 domain are parent-owned",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "gate_id": "CLAIM4013_0_Newton_source",
            "arena": "Newtonian_source_mass",
            "allowed": False,
            "reason": "EM source accounting is conditional and Hodge/normalization/binding rows remain unsigned",
            "blocking_rows": "EMO4013_3_Delta_Hodge_EM;EMO4013_4_wEM_CJQ;EMO4013_8_binding_once",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4013_1_Maxwell",
            "arena": "Maxwell_EM_stress",
            "allowed": False,
            "reason": "minimal Maxwell stress is conditionally included, but Maxwell emergence/charge normalization/alpha are not derived",
            "blocking_rows": "EMO4013_4_wEM_CJQ;EMO4013_5_CXF2",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4013_2_clocks_WEP_R10",
            "arena": "clocks_WEP_R10",
            "allowed": False,
            "reason": "readout, binding, radiative flux and hidden F2 rows remain nonclaim",
            "blocking_rows": "EMO4013_2_Phi_EM_rad;EMO4013_5_CXF2;EMO4013_6_C_EM_readout;EMO4013_8_binding_once",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "gate_id": "CLAIM4013_3_PPN",
            "arena": "local_GR_PPN",
            "allowed": False,
            "reason": "source accounting is not a second-order PPN stability theorem",
            "blocking_rows": "EMO4013_7_Delta_J_total;EMO4013_9_Poynting_units",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4013_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "target": "derive the observed Hodge/Maxwell kinetic normalization/no-extra-F2 owner that makes EM Hilbert stress parent-owned, or retain Delta_Hodge_EM, w_EM, C_JQ and C_XF2 rows",
            "success_condition": "the same observed coframe fixes *_obs, Maxwell kinetic normalization, current/charge normalization and excludes hidden F^2/F*F source slots before clocks/WEP/R10/Newton scoring; otherwise all EM coupling rows stay valid_for_claim=false",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "Maxwell/Poynting stress accounting derived as a conditional once-only Hilbert source theorem; bound EM stress belongs in J_H_total while crossing Poynting flux is a retained leakage row",
            "current_best_next": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["exists"] and row["needle_found"])
    lines = [
        "# 4013 - Maxwell/Poynting Hilbert Stress Once-Only Lock Or I_EM Row",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "The Poynting route is now disciplined instead of mystical:",
        "",
        "`J_H_total = J_matter + J_EM + J_binding + J_apparatus + dB_zero`.",
        "",
        "Minimal Maxwell variation gives the EM Hilbert stress, and the Lorentz force exchange cancels only in the total matter+EM stress. Bound/local EM field energy belongs inside `J_H_total` once. Net radiative/background Poynting flux crossing the worldtube boundary is not deleted; it becomes `Phi_EM_rad`.",
        "",
        "So the rule is: count EM stress once, not zero times and not twice.",
        "",
        "## Branch Law",
        "",
        "Stationary isolated branches may set the time-averaged boundary Poynting flux to zero using",
        "",
        "`dU_EM/dt + int_boundary S_Poynting.n dA = -int_W J.E dV`.",
        "",
        "Radiating or externally driven branches must retain the flux row. Internal Poynting circulation is allowed; only net boundary flux matters for source-mass drift.",
        "",
        "## Finite EM Vector",
        "",
        "`epsilon_EM_once_4013 <= |Delta_Hodge_EM|+|w_EM-1|+|C_XF2|+|C_JQ|+|Phi_EM_rad|/(G_ref M_H)+|C_EM_readout|+|Delta_J_total|+|epsilon_binding_once|+|C_Poynting_units|`.",
        "",
        "This is still not an EM unification claim: it does not derive charge, alpha, Coulomb law or Maxwell emergence.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: EM=`{row['em_source_status']}`, source=`{row['source_result']}`, claim=`{row['claim_result']}`, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "This is a real forward step: Poynting is no longer a loose intuition. It is either already inside total Hilbert stress or it is a boundary-flux residual. The next mathematical throat is observed Hodge/Maxwell normalization ownership.",
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
    marker = "## 4013 - Maxwell/Poynting Once-Only Hilbert Source"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: minimal Maxwell variation gives `T_EM`, so bound EM energy/stress belongs inside `J_H_total` once when the observed Hodge/coframe and normalization are parent-owned.
- Poynting placement: internal `S_Poynting` may circulate; only net boundary/radiative flux `Phi_EM_rad=int_boundary S_Poynting.n dA` changes the source Hamiltonian mass.
- Branch law: stationary isolated branches can zero time-averaged `Phi_EM_rad`; radiating/driven branches require a finite flux row.
- Finite fallback: `epsilon_EM_once_4013 <= |Delta_Hodge_EM|+|w_EM-1|+|C_XF2|+|C_JQ|+|Phi_EM_rad|/(G_ref M_H)+|C_EM_readout|+|Delta_J_total|+|epsilon_binding_once|+|C_Poynting_units|`.
- No claim: this is source-stress bookkeeping, not charge/alpha/Coulomb/Maxwell-emergence proof.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4013 - Maxwell/Poynting Once-Only Hilbert Source" in read_text(SPINE_PATH)


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

    add("VAL4013_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4013_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, theorem_id in enumerate(
        [
            "MPE4013_0_total_visible_action",
            "MPE4013_1_Maxwell_Hilbert_stress",
            "MPE4013_2_internal_exchange_cancellation",
            "MPE4013_3_Poynting_flux_placement",
            "MPE4013_4_once_only_rule",
            "MPE4013_5_no_flux_branch",
            "MPE4013_6_finite_EM_vector",
        ],
        start=2,
    ):
        add(f"VAL4013_{idx:02d}_theorem", any(row["theorem_id"] == theorem_id for row in theorem), f"{theorem_id} present")
    add("VAL4013_09_audit_hodge", any(row["audit_id"] == "ESA4013_0_same_observed_coframe" for row in audit), "Hodge audit present")
    add("VAL4013_10_audit_norm", any(row["audit_id"] == "ESA4013_1_unique_Maxwell_normalization" for row in audit), "Maxwell normalization audit present")
    add("VAL4013_11_audit_total", any(row["audit_id"] == "ESA4013_2_total_Hilbert_variation" for row in audit), "total Hilbert variation audit present")
    add("VAL4013_12_audit_flux", any(row["audit_id"] == "ESA4013_4_Poynting_boundary_flux" for row in audit), "Poynting flux audit present")
    add("VAL4013_13_audit_units", any(row["audit_id"] == "ESA4013_5_Poynting_units_convention" for row in audit), "Poynting units audit present")
    add("VAL4013_14_audit_overclaim", any(row["audit_id"] == "ESA4013_6_not_EM_unification_claim" for row in audit), "overclaim guard present")
    master = next(row for row in finite if row["row_id"] == "EMO4013_0_master")
    add("VAL4013_15_master_vector", "C_Poynting_units" in master["formula"] and "Phi_EM_rad" in master["formula"], "master vector contains flux and units guard")
    for idx, row_id in enumerate(
        [
            "EMO4013_1_bound_EM_inside_MH",
            "EMO4013_2_Phi_EM_rad",
            "EMO4013_3_Delta_Hodge_EM",
            "EMO4013_4_wEM_CJQ",
            "EMO4013_5_CXF2",
            "EMO4013_6_C_EM_readout",
            "EMO4013_7_Delta_J_total",
            "EMO4013_8_binding_once",
            "EMO4013_9_Poynting_units",
        ],
        start=16,
    ):
        add(f"VAL4013_{idx:02d}_{row_id}", any(row["row_id"] == row_id for row in finite), f"{row_id} present")
    full = next(row for row in results if row["case_id"] == "CASE4013_0_full_once_only_signed")
    hodge = next(row for row in results if row["case_id"] == "CASE4013_1_Hodge_open")
    norm = next(row for row in results if row["case_id"] == "CASE4013_2_Maxwell_norm_open")
    current = next(row for row in results if row["case_id"] == "CASE4013_3_current_owner_open")
    total = next(row for row in results if row["case_id"] == "CASE4013_4_total_variation_open")
    flux = next(row for row in results if row["case_id"] == "CASE4013_5_Poynting_flux_open")
    hidden = next(row for row in results if row["case_id"] == "CASE4013_6_hidden_F2_open")
    readout = next(row for row in results if row["case_id"] == "CASE4013_7_readout_binding_units_open")
    numeric = next(row for row in results if row["case_id"] == "CASE4013_8_numeric_pack")
    add("VAL4013_25_full_case", full["source_result"] == "BOUND_EM_INSIDE_JH_TOTAL_AND_PHI_EM_ZERO_ON_STATIONARY_BRANCH", "full signed case conditionally locks once-only source")
    add("VAL4013_26_hodge_case", hodge["source_result"] == "Delta_Hodge_EM", "Hodge open routes to Delta_Hodge_EM")
    add("VAL4013_27_norm_case", norm["source_result"] == "w_EM+C_JQ", "normalization open routes to w_EM+C_JQ")
    add("VAL4013_28_current_case", current["source_result"] == "epsilon_internal_exchange", "current owner open routes to exchange row")
    add("VAL4013_29_total_case", total["source_result"] == "Delta_J_total", "total variation open routes to Delta_J_total")
    add("VAL4013_30_flux_case", flux["source_result"] == "Phi_EM_rad", "Poynting flux open routes to Phi_EM_rad")
    add("VAL4013_31_hidden_case", hidden["source_result"] == "C_XF2", "hidden F2 open routes to C_XF2")
    add("VAL4013_32_readout_case", "C_EM_readout" in readout["source_result"] and "C_Poynting_units" in readout["source_result"], "readout/binding/units open routed")
    add("VAL4013_33_numeric_case", numeric["em_source_status"] == "FINITE_EM_ONCE_ONLY_PACK_NONCLAIM", "numeric pack remains nonclaim")
    add("VAL4013_34_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4013_35_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4013_36_doc_exists", DOC_PATH.exists() and "count EM stress once" in read_text(DOC_PATH), "document written with once-only rule")
    add("VAL4013_37_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4013_38_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4013_39_compile", compile_ok, "script compiles")
    add("VAL4013_40_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
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
    add("VAL4013_41_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4013_42_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4013_43_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4013_44_forward_target", "Hodge" in read_text(OUTPUTS["next"]) and "C_XF2" in read_text(OUTPUTS["next"]), "forward target is Hodge/Maxwell normalization owner")
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
    print(f"4013 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
