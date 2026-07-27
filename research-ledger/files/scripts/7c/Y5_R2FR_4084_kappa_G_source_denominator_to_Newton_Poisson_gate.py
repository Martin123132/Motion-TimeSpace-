from __future__ import annotations

import csv
import math
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple


ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT.parent
SOURCE_DIR = ROOT / "source-intake" / "mts_residuals"
FORMALIZATION = PROJECT / "formalization-workbench"
SCRIPT_PATH = Path(__file__).resolve()
DOC_PATH = ROOT / "4084-Y5-R2FR-kappa-G-source-denominator-to-Newton-Poisson-gate.md"

DECISION = "NEWTON_POISSON_GATE_DERIVED_CONDITIONAL_WITH_CALIBRATED_G_SOURCE_DENOMINATOR_STILL_PARENT_UNSIGNED"

C_LIGHT = 299_792_458.0
G_CODATA = 6.67430e-11
G_RELATIVE_UNCERTAINTY = 2.2e-5
GDOT_OVER_G_LLR_ENVELOPE = 1.3e-12
KAPPA_REF = 8.0 * math.pi * G_CODATA / (C_LIGHT**4)
POISSON_COEFFICIENT = 4.0 * math.pi * G_CODATA

LOCAL_SOURCES: Dict[str, Tuple[Path, str, str]] = {
    "SRC4084_00_4083_next": (
        SOURCE_DIR / "P8_Y5_R2FR_4083_NEXT_TARGET.csv",
        "4084-Y5-R2FR-kappa-G-source-denominator-to-Newton-Poisson-gate.md",
        "4083 selected kappa/G/source denominator to Newton/Poisson gate.",
    ),
    "SRC4084_01_4083_em_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4083_STANDARD_VISIBLE_EM_IMPORT_CONTRACT.csv",
        "calibrated_standard_visible_EM",
        "4083 removes alpha/charge loop from local GR branch by calibrated visible EM import.",
    ),
    "SRC4084_02_4080_kappa": (
        SOURCE_DIR / "P8_Y5_R2FR_4080_KAPPA_TOPOLOGICAL_THEOREM.csv",
        "EXACT_CONDITIONAL_CONSTANT_KAPPA_THEOREM",
        "4080 supplies constant-kappa theorem and the warning that numerical G is not derived.",
    ),
    "SRC4084_03_4080_bounds": (
        SOURCE_DIR / "P8_Y5_R2FR_4080_GDOT_AND_G_CALIBRATION_BOUNDS.csv",
        "BOUND4080_1_CODATA_G_calibration",
        "4080 supplies Gdot/G and CODATA G calibration residual scales.",
    ),
    "SRC4084_04_4062_contract": (
        SOURCE_DIR / "P8_Y5_R2FR_4062_NEWTON_GR_REDUCTION_CONTRACT.csv",
        "nabla^2 Phi = 4*pi*G_N*rho_H",
        "4062 states the EH/same-source Newton reduction contract.",
    ),
    "SRC4084_05_4062_cnorm": (
        SOURCE_DIR / "P8_Y5_R2FR_4062_CNORM_NEWTON_G_CALIBRATION_LAW.csv",
        "G_N := c^4 kappa_eff/(8*pi)",
        "4062 records the allowed universal G calibration and forbids derivative hair.",
    ),
    "SRC4084_06_4063_poisson": (
        SOURCE_DIR / "P8_Y5_R2FR_4063_NEWTON_POISSON_DERIVATION.csv",
        "NEWTON_POISSON_LIMIT_CONDITIONAL",
        "4063 already derives the weak-field Poisson coefficient conditionally.",
    ),
    "SRC4084_07_4063_ppn": (
        SOURCE_DIR / "P8_Y5_R2FR_4063_PPN_READOUT_VECTOR.csv",
        "Delta_PPN_abs",
        "4063 records that Newton is not yet full PPN/local GR.",
    ),
    "SRC4084_08_4015_theorem": (
        SOURCE_DIR / "P8_Y5_R2FR_4015_GAUSS_POISSON_GREF_NEWTON_THEOREM.csv",
        "OVERCLAIM_GUARD_EXACT",
        "4015 prevents orbital GM laundering and states Gauss/Poisson/Newton theorem.",
    ),
    "SRC4084_09_4015_audit": (
        SOURCE_DIR / "P8_Y5_R2FR_4015_SOURCE_NORMALIZATION_AUDIT.csv",
        "GUARD_LOCKED",
        "4015 source audit locks anti-laundering while keeping parent clauses unsigned.",
    ),
    "SRC4084_10_4015_residuals": (
        SOURCE_DIR / "P8_Y5_R2FR_4015_NEWTON_BRIDGE_FINITE_ROWS.csv",
        "epsilon_Newton_bridge_4015",
        "4015 finite rows provide no-cancellation Newton bridge residual vector.",
    ),
    "SRC4084_11_4072_reduction": (
        SOURCE_DIR / "P8_Y5_R2FR_4072_EH_NEWTON_PPN_REDUCTION_CONTRACT.csv",
        "CONDITIONAL_LINK_TO_4063",
        "4072 links the observed coframe/EH branch to 4063 Newton/PPN readout.",
    ),
    "SRC4084_12_4081_source": (
        SOURCE_DIR / "P8_Y5_R2FR_4081_SOURCE_COUPLING_WEP_THEOREM.csv",
        "EXACT_CONDITIONAL_UNIVERSAL_HILBERT_SOURCE_THEOREM",
        "4081 supplies universal Hilbert source theorem but not parent promotion.",
    ),
}

WEB_SOURCES = [
    {
        "source_id": "WEB4084_0_nist_codata_G",
        "title": "CODATA Value: Newtonian constant of gravitation",
        "authors": "NIST/CODATA",
        "year": 2022,
        "url": "https://physics.nist.gov/cgi-bin/cuu/Value?bg=",
        "supporting_url": "https://physics.nist.gov/constants",
        "extracted_result": "G = 6.67430(15)e-11 m^3 kg^-1 s^-2; relative standard uncertainty 2.2e-5",
        "source_role": "calibrated Newtonian G value and uncertainty",
        "confidence": "official_CODATA_NIST_constant_page_reused_from_4080",
    },
    {
        "source_id": "WEB4084_1_LLR_Gdot",
        "title": "Progress in Lunar Laser Ranging Tests of Relativistic Gravity",
        "authors": "Williams, Turyshev, Boggs",
        "year": 2004,
        "url": "https://doi.org/10.1103/PhysRevLett.93.261101",
        "supporting_url": "https://arxiv.org/abs/gr-qc/0411113",
        "extracted_result": "Gdot/G = (4 +/- 9)e-13 yr^-1",
        "source_role": "finite G/kappa drift residual scale",
        "confidence": "peer_reviewed_PRL_and_arXiv_preprint_reused_from_4080",
    },
]

OUTPUTS = {
    "source_register": SOURCE_DIR / "P8_Y5_R2FR_4084_SOURCE_REGISTER.csv",
    "web_provenance": SOURCE_DIR / "P8_Y5_R2FR_4084_WEB_PROVENANCE.csv",
    "poisson_theorem": SOURCE_DIR / "P8_Y5_R2FR_4084_NEWTON_POISSON_GATE_THEOREM.csv",
    "source_denominator": SOURCE_DIR / "P8_Y5_R2FR_4084_SOURCE_DENOMINATOR_GATE.csv",
    "g_kappa": SOURCE_DIR / "P8_Y5_R2FR_4084_G_KAPPA_CALIBRATION_ROWS.csv",
    "residuals": SOURCE_DIR / "P8_Y5_R2FR_4084_NEWTON_POISSON_RESIDUAL_VECTOR.csv",
    "runner_update": SOURCE_DIR / "P8_Y5_R2FR_4084_EFFECTIVE_RESIDUAL_RUNNER_UPDATE.csv",
    "decision_gate": SOURCE_DIR / "P8_Y5_R2FR_4084_DECISION_GATE.csv",
    "claim_gate": SOURCE_DIR / "P8_Y5_R2FR_4084_CLAIM_GATE.csv",
    "next_target": SOURCE_DIR / "P8_Y5_R2FR_4084_NEXT_TARGET.csv",
    "status": SOURCE_DIR / "P8_Y5_R2FR_4084_STATUS.csv",
    "validation": SOURCE_DIR / "P8_Y5_BRR545_4084_VALIDATION.csv",
}


def timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def write_csv(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows supplied for {path}")
    with path.open("w", newline="", encoding="utf-8") as output_file:
        writer = csv.DictWriter(output_file, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def source_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source_id, (path, needle, role) in LOCAL_SOURCES.items():
        text = read_text(path)
        rows.append(
            {
                "source_id": source_id,
                "source_type": "local_file",
                "path_or_url": str(path),
                "exists_or_recorded": path.exists(),
                "needle": needle,
                "needle_found": needle in text,
                "role": role,
                "timestamp_utc": current_timestamp,
            }
        )
    for source in WEB_SOURCES:
        rows.append(
            {
                "source_id": source["source_id"],
                "source_type": "web_source",
                "path_or_url": source["url"],
                "exists_or_recorded": True,
                "needle": source["extracted_result"],
                "needle_found": True,
                "role": source["source_role"],
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def web_provenance_rows(current_timestamp: str) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    for source in WEB_SOURCES:
        row = dict(source)
        row["timestamp_utc"] = current_timestamp
        row["valid_for_claim"] = False
        rows.append(row)
    return rows


def poisson_theorem_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "theorem_id": "NPG4084_0_EH_same_source",
            "statement": "If the local observed metric action reduces to EH/EC with Levi-Civita connection, calibrated constant kappa_ref, and the same Hilbert stress T_H_total as source, then the leading weak-field equation is G_00^(1)=kappa_ref T_00^H plus explicit residuals.",
            "proof_sketch": "Vary S_EH[g_obs;kappa_ref]+S_matter[e_obs,psi] with kappa_ref fixed before readout. The 00 component of the linearized Einstein equation is sourced by the Hilbert stress in the same observed frame.",
            "formula": "G_00^(1)=kappa_ref*T_00^H + R_EH00 + R_source",
            "result": "EXACT_CONDITIONAL_EH_SAME_SOURCE_GATE",
            "current_MTS_status": "EH_OPERATOR_AND_SAME_SOURCE_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "NPG4084_1_Poisson_coefficient",
            "statement": "With g_00=-(1+2 Phi_N/c^2), T_00^H=rho_H c^2, and kappa_ref=8 pi G_ref/c^4, the EH 00 equation gives nabla^2 Phi_N=4 pi G_ref rho_H.",
            "proof_sketch": "Use G_00^(1)=2 nabla^2 Phi_N/c^2 and T_00^H=rho_H c^2. Then 2 nabla^2 Phi_N/c^2=kappa_ref rho_H c^2, so nabla^2 Phi_N=(kappa_ref c^4/2)rho_H=4 pi G_ref rho_H.",
            "formula": "nabla^2 Phi_N = 4*pi*G_ref*rho_H",
            "result": "EXACT_CONDITIONAL_NEWTON_POISSON_COEFFICIENT",
            "current_MTS_status": "COEFFICIENT_DERIVED_IF_4084_PREMISES_SIGNED",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "NPG4084_2_source_denominator",
            "statement": "The source density rho_H must be defined from the parent Hilbert/Hamiltonian source charge before orbital readout: M_H=int rho_H dV_obs, not M_H=GM_orb/G_ref.",
            "proof_sketch": "If M_H is backfilled from orbital GM, the Poisson test becomes tautological. Parent source charge must be constructed independently through Hilbert stress/Pi_M/H_tau or retained as a residual.",
            "formula": "Delta_orb := GM_orb - G_ref*M_H is output-only",
            "result": "ANTI_ORBITAL_LAUNDERING_SOURCE_DENOMINATOR_RULE",
            "current_MTS_status": "GUARD_LOCKED_SOURCE_CHARGE_PARENT_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "NPG4084_3_Gauss_inverse_square",
            "statement": "If projected source current is closed and exterior boundary/radiative/domain fluxes vanish or are owned, integrating Poisson gives the Gauss law and far-field inverse-square acceleration.",
            "proof_sketch": "Integrate nabla^2 Phi_N over compact support and apply divergence theorem. With no extra monopole or unowned boundary flux, surface integral grad Phi_N.dS=4 pi G_ref M_H and Phi_N=-G_ref M_H/r plus multipoles.",
            "formula": "int_S grad Phi_N.dS = 4*pi*G_ref*M_H; a_r=-G_ref*M_H/r^2",
            "result": "EXACT_CONDITIONAL_GAUSS_NEWTON_READOUT",
            "current_MTS_status": "BOUNDARY_CHARGE_LOCK_AND_MULTIPOLE_GATES_UNSIGNED",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "theorem_id": "NPG4084_4_Newton_not_full_GR",
            "statement": "Passing the Newton/Poisson gate would establish the first-order scalar potential branch only; local GR still requires gamma=1, beta=1, preferred-frame silence, Bianchi/conservation closure, and no extra PPN sources.",
            "proof_sketch": "Newtonian agreement is a weak-field first-order scalar test. PPN order checks spatial curvature, nonlinear self-coupling, preferred frames, conservation anomalies and time-varying coupling.",
            "formula": "Delta_PPN_abs remains active",
            "result": "ANTI_OVERCLAIM_GUARD_NEWTON_NOT_LOCAL_GR",
            "current_MTS_status": "PPN_SECOND_ORDER_GATE_REMAINS_P0",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def source_denominator_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "gate_id": "SDG4084_0_EH_operator",
            "clause": "observed metric operator has EH 00 weak-field coefficient",
            "status": "CONDITIONAL_ON_EH_EC_TORSION_NONMETRICITY_GATE",
            "zero_if": "reduced parent action is EH/EC in e_obs with torsion/nonmetricity zero",
            "if_open": "retain Delta_EH00 and PPN R11/nonEH residual rows",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "SDG4084_1_same_Hilbert_source",
            "clause": "rho_H is the same Hilbert stress source for matter, calibrated visible EM, clocks and orbital probes",
            "status": "IMPROVED_BY_4083_EM_IMPORT_BUT_PARENT_SOURCE_FUNCTOR_UNSIGNED",
            "zero_if": "same-coframe matter functor and visible EM import are parent-owned before readout",
            "if_open": "retain WEP/source-label/source-current residuals",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "SDG4084_2_G_kappa_convention",
            "clause": "kappa_ref=8*pi*G_ref/c^4 fixed before readout",
            "status": "CALIBRATION_ALLOWED_VALUE_NOT_DERIVED",
            "zero_if": "single universal calibrated G_ref/kappa_ref is used and derivative/source/range/frame hair is forbidden",
            "if_open": "retain C_Gref_kappa, Gdot/G, range and source-dependent G residuals",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "SDG4084_3_source_charge_denominator",
            "clause": "M_H=int rho_H dV_obs equals parent Pi_M/H_tau/Hilbert source charge",
            "status": "CONDITIONAL_4012_CHARGE_LOCK_UNSIGNED",
            "zero_if": "constraint/boundary-charge map uniquely identifies Hilbert source charge and exact terms have zero flux",
            "if_open": "retain C_PiM_H and source denominator residual",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "SDG4084_4_Gauss_boundary",
            "clause": "exterior projected source current closed with no unowned boundary/domain/memory/radiative flux",
            "status": "CONDITIONAL_ZERO_FLUX_UNSIGNED",
            "zero_if": "Poynting once-only, boundary nohair and closed exterior source current clauses are signed",
            "if_open": "retain C_Gauss_boundary and mu_extra/(G_ref*M_H)",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "gate_id": "SDG4084_5_orbital_readout",
            "clause": "orbital GM is an output comparison, not the definition of M_H",
            "status": "GUARD_LOCKED",
            "zero_if": "slow-geodesic readout uses same observed metric and no fifth-force/source-frame term",
            "if_open": "retain C_orbital_readout; never backfill M_H from GM_orb/G_ref",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def g_kappa_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "row_id": "GK4084_0_G_ref",
            "quantity": "G_ref",
            "value": G_CODATA,
            "units": "m^3 kg^-1 s^-2",
            "uncertainty_or_bound": G_RELATIVE_UNCERTAINTY,
            "uncertainty_units": "relative_dimensionless",
            "source_id": "WEB4084_0_nist_codata_G",
            "interpretation": "calibrated universal coupling constant, not MTS numerical prediction",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "row_id": "GK4084_1_kappa_ref",
            "quantity": "kappa_ref",
            "value": KAPPA_REF,
            "units": "SI_Einstein_coupling_convention",
            "uncertainty_or_bound": G_RELATIVE_UNCERTAINTY,
            "uncertainty_units": "relative_dimensionless_from_G",
            "source_id": "WEB4084_0_nist_codata_G",
            "interpretation": "kappa_ref=8*pi*G_ref/c^4 in the selected EH convention",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "row_id": "GK4084_2_4piG",
            "quantity": "4*pi*G_ref",
            "value": POISSON_COEFFICIENT,
            "units": "m^3 kg^-1 s^-2",
            "uncertainty_or_bound": G_RELATIVE_UNCERTAINTY,
            "uncertainty_units": "relative_dimensionless_from_G",
            "source_id": "WEB4084_0_nist_codata_G",
            "interpretation": "Poisson coefficient in nabla^2 Phi=4*pi*G_ref*rho_H",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "row_id": "GK4084_3_Gdot",
            "quantity": "Gdot_over_G",
            "value": 0.0,
            "units": "per_year",
            "uncertainty_or_bound": GDOT_OVER_G_LLR_ENVELOPE,
            "uncertainty_units": "absolute_one_sigma_envelope_per_year",
            "source_id": "WEB4084_1_LLR_Gdot",
            "interpretation": "finite drift residual scale if constant-kappa branch is not parent signed",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def residual_rows(current_timestamp: str) -> List[Dict[str, object]]:
    residuals = [
        ("Delta_EH00", "weak-field 00 operator mismatch", "ZERO_IF_EH_OPERATOR_PARENT_SIGNED_ELSE_RETAIN"),
        ("Delta_NR_source", "nonrelativistic source-density mismatch", "ZERO_IF_T00_EQUALS_RHO_C2_IN_OBSERVED_FRAME"),
        ("C_PiM_H", "Hilbert/Hamiltonian/source denominator mismatch", "ZERO_IF_4012_CHARGE_LOCK_PARENT_SIGNED_ELSE_RETAIN"),
        ("C_Gref_kappa", "kappa to calibrated G convention mismatch", "ZERO_IF_KAPPA_REF_CONVENTION_FIXED_ELSE_RETAIN"),
        ("C_frame_units", "frame/unit split between metric operator, source, clocks and orbit readout", "ZERO_IF_SINGLE_OBSERVED_FRAME_SIGNED_ELSE_RETAIN"),
        ("C_Gauss_boundary", "boundary/domain/memory/radiative flux in Gauss law", "ZERO_IF_CLOSED_EXTERIOR_AND_ZERO_FLUX_SIGNED_ELSE_RETAIN"),
        ("C_orbital_readout", "GM_orb output residual after slow-geodesic projection", "OUTPUT_COMPARISON_ONLY_NOT_INPUT"),
        ("mu_extra_over_GM", "hidden extra monopole divided by G_ref M_H", "ZERO_IF_NO_SHADOW_SOURCE_CHANNEL_SIGNED_ELSE_RETAIN"),
        ("epsilon_EM_once", "EM/Poynting/binding energy counted once in rho_H", "IMPROVED_BY_4083_IMPORT_ZERO_IN_BASELINE_DEVIATIONS_BOUNDED"),
        ("epsilon_G_run", "G/kappa time/range/source drift", f"BOUND_BY_GDOT_{GDOT_OVER_G_LLR_ENVELOPE:.3e}_PER_YEAR_AND_G_CALIBRATION"),
        ("epsilon_PPN_2nd", "second-order PPN stability residual", "ACTIVE_NEXT_GATE_NOT_CLOSED_BY_NEWTON"),
    ]
    rows: List[Dict[str, object]] = []
    for index, (coefficient, meaning, status) in enumerate(residuals):
        rows.append(
            {
                "row_id": f"NPR4084_{index}",
                "coefficient": coefficient,
                "meaning": meaning,
                "formula_or_bound": status,
                "units": "dimensionless_or_declared_component_units",
                "observable_links": "Newton;orbital_GM;PPN;WEP;clocks;R10",
                "valid_for_claim": False,
                "timestamp_utc": current_timestamp,
            }
        )
    return rows


def runner_update_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "runner_id": "RUNUP4084_0_Newton_Poisson",
            "quantity": "Newton_Poisson_gate",
            "old_score": "ALPHA_LOOP_REMOVED_FROM_CRITICAL_PATH_RETURN_TO_KAPPA_G_POISSON_PPN_GATE",
            "new_score": "EXACT_CONDITIONAL_POISSON_DERIVATION_WITH_SOURCE_DENOMINATOR_GUARD",
            "numeric_value": POISSON_COEFFICIENT,
            "numeric_units": "4*pi*G_ref",
            "aggregate_effect": "first-order Newton coefficient is derived conditionally from EH plus calibrated G, not fitted orbital GM",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4084_1_source_denominator",
            "quantity": "M_H_source_denominator",
            "old_score": "C_PiM_H_RETAINED",
            "new_score": "ANTI_ORBITAL_LAUNDERING_SOURCE_DENOMINATOR_RULE_LOCKED",
            "numeric_value": "not_numeric",
            "numeric_units": "gate",
            "aggregate_effect": "M_H must be parent Hilbert/Hamiltonian charge; GM_orb is output residual only",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4084_2_G_kappa",
            "quantity": "kappa_ref",
            "old_score": "FINITE_EXTERNAL_CODATA_CALIBRATION_SCALE",
            "new_score": "KAPPA_REF_NUMERICALLY_INSTANTIATED_AS_CALIBRATED_CONSTANT",
            "numeric_value": KAPPA_REF,
            "numeric_units": "8*pi*G/c^4",
            "aggregate_effect": "constant coupling may be calibrated; value is not MTS prediction",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
        {
            "runner_id": "RUNUP4084_3_next_PPN",
            "quantity": "Delta_PPN_abs",
            "old_score": "ACTIVE_NEXT_GATE_NOT_CLOSED_BY_NEWTON",
            "new_score": "NEXT_TARGET_SOURCE_STABLE_PPN_VECTOR",
            "numeric_value": "not_numeric",
            "numeric_units": "gate",
            "aggregate_effect": "after Newton/Poisson gate, next proof must preserve gamma beta preferred-frame conservation rows",
            "valid_for_claim": False,
            "timestamp_utc": current_timestamp,
        },
    ]


def decision_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "decision_id": "DEC4084_0",
            "decision": DECISION,
            "strongest_positive_result": "Newton/Poisson coefficient follows exactly from EH same-source branch with kappa_ref=8*pi*G_ref/c^4 and calibrated visible matter.",
            "blocking_fact": "EH operator, observed coframe/source denominator, Pi_M/H_tau charge equality and PPN second-order stability are not parent-signed together.",
            "allowed_status": "private_nonclaim_checkpoint",
            "claim_allowed": False,
            "next_action": "build source-stable PPN vector: gamma, beta, preferred-frame, conservation and Gdot residuals under the same source denominator.",
            "timestamp_utc": current_timestamp,
        }
    ]


def claim_gate_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "claim_id": "CLAIM4084_0",
            "claim": "Newton/Poisson follows from EH same-source branch with calibrated G",
            "claim_allowed": True,
            "scope": "conditional mathematical theorem",
            "why": "linearized EH 00 equation gives the Poisson coefficient under declared premises",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4084_1",
            "claim": "MTS predicts the numerical value of G",
            "claim_allowed": False,
            "scope": "parent local-GR/Newton derivation",
            "why": "G_ref is calibrated like in GR unless a parent normalization/superselection theorem predicts it",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4084_2",
            "claim": "orbital GM may define the source mass",
            "claim_allowed": False,
            "scope": "methodological guard",
            "why": "that would launder the Newton test; GM_orb must be an output residual",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4084_3",
            "claim": "local GR is now fully derived",
            "claim_allowed": False,
            "scope": "parent local-GR derivation",
            "why": "PPN gamma/beta/preferred-frame/conservation and parent coframe/source gates remain unsigned",
            "timestamp_utc": current_timestamp,
        },
        {
            "claim_id": "CLAIM4084_4",
            "claim": "source denominator anti-laundering gate is locked",
            "claim_allowed": True,
            "scope": "private nonclaim residual target",
            "why": "the branch now explicitly forbids defining M_H from observed orbital GM",
            "timestamp_utc": current_timestamp,
        },
    ]


def next_target_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "target_id": "NEXT4084_0",
            "next_target": "4085-Y5-R2FR-source-stable-PPN-vector-gamma-beta-preferred-frame-gate.md",
            "script": "scripts/Y5_R2FR_4085_source_stable_PPN_vector_gamma_beta_preferred_frame_gate.py",
            "why": "Newton/Poisson is only first-order; the serious local-GR gate is whether the same source denominator survives gamma, beta, preferred-frame and conservation PPN projections.",
            "priority": "P0",
            "timestamp_utc": current_timestamp,
        },
        {
            "target_id": "NEXT4084_1",
            "next_target": "parent_source_denominator_signature_later",
            "script": "fold_into_parent_action_work",
            "why": "source denominator equality still needs parent Pi_M/H_tau/Hilbert charge adoption.",
            "priority": "P1",
            "timestamp_utc": current_timestamp,
        },
    ]


def status_rows(current_timestamp: str) -> List[Dict[str, object]]:
    return [
        {
            "timestamp_utc": current_timestamp,
            "branch_id": "MTS_R2FR_Y5_4084_KAPPA_G_SOURCE_DENOMINATOR_TO_NEWTON_POISSON_GATE",
            "status": DECISION,
            "public_claim_allowed": False,
            "github_action": False,
            "formalization_workbench_modified": False,
            "summary": "4084 derives the Newton/Poisson coefficient conditionally from EH same-source branch, instantiates calibrated G/kappa rows, locks the no-orbital-GM-laundering source denominator rule, and points next to source-stable PPN.",
            "valid_for_claim": False,
        }
    ]


def validate_sources(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    failures = [
        row["source_id"]
        for row in rows
        if row["exists_or_recorded"] is not True or row["needle_found"] is not True
    ]
    return not failures, f"missing_or_unmatched_sources={failures}"


def validate_csv_parse(paths: List[Path]) -> Tuple[bool, str]:
    failures: List[str] = []
    for path in paths:
        try:
            with path.open(newline="", encoding="utf-8") as input_file:
                rows = list(csv.DictReader(input_file))
            if not rows:
                failures.append(f"{path}:empty")
        except Exception as exc:
            failures.append(f"{path}:{exc}")
    return not failures, f"csv_failures={failures}"


def validate_g_kappa(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    failures: List[str] = []
    for row in rows:
        try:
            value = float(row["value"])
            bound = float(row["uncertainty_or_bound"])
            if not math.isfinite(value):
                failures.append(f"{row['row_id']}:value not finite")
            if row["row_id"] != "GK4084_3_Gdot" and value <= 0:
                failures.append(f"{row['row_id']}:positive value required")
            if bound < 0:
                failures.append(f"{row['row_id']}:negative uncertainty")
        except Exception:
            failures.append(f"{row['row_id']}:non-numeric")
        if row["valid_for_claim"] is not False:
            failures.append(f"{row['row_id']}:overclaim")
    return not failures, "; ".join(failures) if failures else "G/kappa rows numeric and nonclaim"


def validate_source_denominator(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    joined = str(rows)
    required = ["M_H=int rho_H dV_obs", "GUARD_LOCKED", "CALIBRATION_ALLOWED_VALUE_NOT_DERIVED"]
    missing = [token for token in required if token not in joined]
    overclaims = [row["gate_id"] for row in rows if row["valid_for_claim"] is not False]
    return not missing and not overclaims, f"missing={missing}; overclaims={overclaims}"


def validate_claim_scopes(rows: List[Dict[str, object]]) -> Tuple[bool, str]:
    allowed_scopes = {"conditional mathematical theorem", "private nonclaim residual target"}
    bad_rows = [
        row["claim_id"]
        for row in rows
        if row["claim_allowed"] is True and row["scope"] not in allowed_scopes
    ]
    return not bad_rows, f"bad_allowed_claim_scopes={bad_rows}"


def validate_no_public_claim(row_groups: List[List[Dict[str, object]]]) -> Tuple[bool, str]:
    text = str(row_groups)
    forbidden = [
        "public_claim': True",
        '"public_claim": True',
        "github_action': True",
        '"github_action": True',
        "MTS predicts the numerical value of G', 'claim_allowed': True",
        "orbital GM may define the source mass', 'claim_allowed': True",
        "local GR is now fully derived', 'claim_allowed': True",
    ]
    hits = [token for token in forbidden if token in text]
    return not hits, f"forbidden_public_claim_tokens={hits}"


def validate_output_scope(paths: List[Path]) -> Tuple[bool, str]:
    outside = [str(path) for path in paths + [DOC_PATH] if ROOT not in path.parents and path != ROOT]
    formalization_hits = [str(path) for path in paths + [DOC_PATH] if FORMALIZATION in path.parents]
    return not outside and not formalization_hits, f"outside_post_checkpoint={outside}; formalization_hits={formalization_hits}"


def validate_script_compile() -> Tuple[bool, str]:
    try:
        py_compile.compile(str(SCRIPT_PATH), doraise=True)
    except py_compile.PyCompileError as exc:
        return False, str(exc)
    return True, "script compiles"


def validation_rows(
    source_table: List[Dict[str, object]],
    generated_csvs: List[Path],
    row_groups: List[List[Dict[str, object]]],
    g_kappa: List[Dict[str, object]],
    source_denominator: List[Dict[str, object]],
    claims: List[Dict[str, object]],
) -> List[Dict[str, object]]:
    source_ok, source_detail = validate_sources(source_table)
    csv_ok, csv_detail = validate_csv_parse(generated_csvs)
    g_ok, g_detail = validate_g_kappa(g_kappa)
    source_den_ok, source_den_detail = validate_source_denominator(source_denominator)
    no_public_ok, no_public_detail = validate_no_public_claim(row_groups)
    claim_scope_ok, claim_scope_detail = validate_claim_scopes(claims)
    output_scope_ok, output_scope_detail = validate_output_scope(generated_csvs)
    compile_ok, compile_detail = validate_script_compile()
    joined = str(row_groups)
    return [
        {"check_id": "VAL4084_00_sources", "passed": source_ok, "detail": source_detail},
        {"check_id": "VAL4084_01_csv_parse", "passed": csv_ok, "detail": csv_detail},
        {"check_id": "VAL4084_02_g_kappa_numeric", "passed": g_ok, "detail": g_detail},
        {"check_id": "VAL4084_03_source_denominator", "passed": source_den_ok, "detail": source_den_detail},
        {"check_id": "VAL4084_04_no_public_or_github_claim", "passed": no_public_ok, "detail": no_public_detail},
        {"check_id": "VAL4084_05_claim_scope", "passed": claim_scope_ok, "detail": claim_scope_detail},
        {"check_id": "VAL4084_06_output_scope", "passed": output_scope_ok, "detail": output_scope_detail},
        {
            "check_id": "VAL4084_07_poisson_derivation",
            "passed": "EXACT_CONDITIONAL_NEWTON_POISSON_COEFFICIENT" in joined
            and "ANTI_ORBITAL_LAUNDERING_SOURCE_DENOMINATOR_RULE" in joined,
            "detail": "Poisson coefficient and anti-laundering denominator rule are present",
        },
        {
            "check_id": "VAL4084_08_next_target",
            "passed": "4085-Y5-R2FR-source-stable-PPN-vector-gamma-beta-preferred-frame-gate.md" in joined,
            "detail": "next target moves to source-stable PPN vector",
        },
        {"check_id": "VAL4084_09_script_compiles", "passed": compile_ok, "detail": compile_detail},
    ]


def doc_text(current_timestamp: str) -> str:
    return f"""# 4084 - Kappa/G Source Denominator To Newton Poisson Gate

- Timestamp: `{current_timestamp}`
- Status: `private_nonclaim_checkpoint`
- Decision: `{DECISION}`
- Public local-GR/Newton claim: `false`
- GitHub action: `false`

## Result

This checkpoint locks the first-order Newton bridge in the clean form:

```text
S_EH[g_obs; kappa_ref] + S_matter[e_obs, visible matter]
kappa_ref = 8 pi G_ref / c^4
g_00 = -(1 + 2 Phi_N/c^2)
T_00^H = rho_H c^2
```

Then:

```text
G_00^(1) = 2 nabla^2 Phi_N/c^2
G_00^(1) = kappa_ref T_00^H
nabla^2 Phi_N = 4 pi G_ref rho_H
```

So the Poisson coefficient is derived conditionally from EH plus a calibrated universal `G_ref`.

## No Fitted-GM Laundering

The source denominator is now explicitly:

```text
M_H = int rho_H dV_obs
```

from the parent Hilbert/Hamiltonian source branch. It is not:

```text
M_H := GM_orb / G_ref
```

Orbital `GM` is an output comparison:

```text
Delta_orb = GM_orb - G_ref M_H
```

That matters. It stops the Newtonian limit from being won by definition.

## Calibrated G/Kappa Rows

```text
G_ref = {G_CODATA:.8e} m^3 kg^-1 s^-2
relative G calibration scale = {G_RELATIVE_UNCERTAINTY:.3e}
kappa_ref = {KAPPA_REF:.12e}
4 pi G_ref = {POISSON_COEFFICIENT:.12e}
Gdot/G residual scale = {GDOT_OVER_G_LLR_ENVELOPE:.3e} yr^-1
```

This is exactly like GR in one important sense: the local reduction may use a calibrated `G`, but it must not pretend to derive the numerical value of `G`.

## What Improved

4083 lets calibrated visible EM sit inside the Hilbert stress. That means the Newton source can include ordinary matter plus bound EM/Poynting stress once, without the alpha loop blocking the branch.

## What Remains Unsigned

```text
EH/EC parent reduction to observed metric operator
q/e_obs same-frame source functor
Pi_M/H_tau/Hilbert source denominator equality
closed exterior Gauss boundary
slow-geodesic orbital readout with no fifth force
PPN gamma/beta/preferred-frame/conservation stability
```

## Decision

```text
Newton/Poisson coefficient = exact conditional
G numerical value = calibrated, not predicted
source denominator anti-laundering = locked
local GR claim = still false
next gate = source-stable PPN vector
```

## Sources

- NIST/CODATA, Newtonian constant of gravitation, 2022 value.
- Williams, Turyshev and Boggs, lunar laser ranging `Gdot/G` bound.

## Next

```text
4085-Y5-R2FR-source-stable-PPN-vector-gamma-beta-preferred-frame-gate.md
```

If 4085 works, that is where this starts to look genuinely dangerous in the good way: not just Newton, but GR-shaped local tests.
"""


def main() -> None:
    current_timestamp = timestamp()
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    sources = source_rows(current_timestamp)
    web_provenance = web_provenance_rows(current_timestamp)
    poisson = poisson_theorem_rows(current_timestamp)
    source_denominator = source_denominator_rows(current_timestamp)
    g_kappa = g_kappa_rows(current_timestamp)
    residuals = residual_rows(current_timestamp)
    runner = runner_update_rows(current_timestamp)
    decisions = decision_gate_rows(current_timestamp)
    claims = claim_gate_rows(current_timestamp)
    next_targets = next_target_rows(current_timestamp)
    statuses = status_rows(current_timestamp)

    DOC_PATH.write_text(doc_text(current_timestamp), encoding="utf-8")
    write_csv(OUTPUTS["source_register"], sources)
    write_csv(OUTPUTS["web_provenance"], web_provenance)
    write_csv(OUTPUTS["poisson_theorem"], poisson)
    write_csv(OUTPUTS["source_denominator"], source_denominator)
    write_csv(OUTPUTS["g_kappa"], g_kappa)
    write_csv(OUTPUTS["residuals"], residuals)
    write_csv(OUTPUTS["runner_update"], runner)
    write_csv(OUTPUTS["decision_gate"], decisions)
    write_csv(OUTPUTS["claim_gate"], claims)
    write_csv(OUTPUTS["next_target"], next_targets)
    write_csv(OUTPUTS["status"], statuses)

    generated_csvs = [
        OUTPUTS["source_register"],
        OUTPUTS["web_provenance"],
        OUTPUTS["poisson_theorem"],
        OUTPUTS["source_denominator"],
        OUTPUTS["g_kappa"],
        OUTPUTS["residuals"],
        OUTPUTS["runner_update"],
        OUTPUTS["decision_gate"],
        OUTPUTS["claim_gate"],
        OUTPUTS["next_target"],
        OUTPUTS["status"],
    ]
    row_groups = [
        sources,
        web_provenance,
        poisson,
        source_denominator,
        g_kappa,
        residuals,
        runner,
        decisions,
        claims,
        next_targets,
        statuses,
    ]
    validation = validation_rows(sources, generated_csvs, row_groups, g_kappa, source_denominator, claims)
    write_csv(OUTPUTS["validation"], validation)

    cache_dir = SCRIPT_PATH.parent / "__pycache__"
    if cache_dir.exists():
        shutil.rmtree(cache_dir)

    failures = [row for row in validation if not row["passed"]]
    print(f"wrote {DOC_PATH}")
    print(f"decision: {DECISION}")
    print(f"validation rows: {len(validation)}")
    print(f"validation failures: {len(failures)}")
    for failure in failures:
        print(f"FAIL {failure['check_id']}: {failure['detail']}")


if __name__ == "__main__":
    main()
