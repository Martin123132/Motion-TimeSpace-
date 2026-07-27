from __future__ import annotations

import csv
import py_compile
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHECKPOINT = "4015"
SCRIPT_PATH = Path(__file__).resolve()
PCW = SCRIPT_PATH.parents[1]
ROOT = PCW.parent
FWB = ROOT / "formalization-workbench"
SRC = PCW / "source-intake" / "mts_residuals"
DOC_PATH = PCW / "4015-Y5-R2FR-Gauss-Poisson-Gref-source-normalization-or-Newton-row.md"
SPINE_PATH = PCW / "LOCAL_GR_COUPLING_SPINE_CURRENT_STATE.md"

OUTPUTS = {
    "sources": SRC / "P8_Y5_R2FR_4015_SOURCE_REGISTER.csv",
    "theorem": SRC / "P8_Y5_R2FR_4015_GAUSS_POISSON_GREF_NEWTON_THEOREM.csv",
    "audit": SRC / "P8_Y5_R2FR_4015_SOURCE_NORMALIZATION_AUDIT.csv",
    "finite": SRC / "P8_Y5_R2FR_4015_NEWTON_BRIDGE_FINITE_ROWS.csv",
    "cases": SRC / "P8_Y5_R2FR_4015_EVALUATOR_CASES.csv",
    "results": SRC / "P8_Y5_R2FR_4015_EVALUATOR_RESULTS.csv",
    "decision": SRC / "P8_Y5_R2FR_4015_DECISION_GATE.csv",
    "claim_gate": SRC / "P8_Y5_R2FR_4015_CLAIM_GATE.csv",
    "next": SRC / "P8_Y5_R2FR_4015_NEXT_TARGET.csv",
    "status": SRC / "P8_Y5_R2FR_4015_STATUS.csv",
    "validation": SRC / "P8_Y5_BRR545_4015_VALIDATION.csv",
}

NEXT_DOC = "4016-Y5-R2FR-Gref-superselection-universal-calibration-or-Gdot-range-row.md"
NEXT_SCRIPT = "scripts/Y5_R2FR_4016_Gref_superselection_universal_calibration_or_Gdot_range_row.py"


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
        ("SRC4015_00_handoff", SRC / "P8_Y5_R2FR_4014_NEXT_TARGET.csv", "NEXT4014_0", "4014 handoff to Newton bridge"),
        ("SRC4015_01_4001_projector", PCW / "4001-Y5-R2FR-parent-projector-constancy-or-PiM-commutator-bound.md", "Pi_M:C_H(A_ext)->C_M(A_ext)", "Pi_M fixed chain-map contract"),
        ("SRC4015_02_4002_Htau", PCW / "4002-Y5-R2FR-Htau-Href-integrability-reference-lock-or-curl-bound.md", "M_H_ref := H_tau", "same-frame positive Hamiltonian mass denominator"),
        ("SRC4015_03_4003_current", PCW / "4003-Y5-R2FR-parent-theta-Qtau-current-chain-or-integrability-source-row.md", "J_tau = d Q_tau^MTS + C_tau", "parent Noether current chain"),
        ("SRC4015_04_4012_charge_eq", SRC / "P8_Y5_R2FR_4012_PIM_HTAU_CHARGE_LOCK_THEOREM.csv", "CHG4012_4_same_charge_equality", "Pi_M/H_tau/Hilbert source equality"),
        ("SRC4015_05_4012_charge_vector", SRC / "P8_Y5_R2FR_4012_CHARGE_GLUE_FINITE_ROWS.csv", "CGLUE4012_9_G_PPN", "G and PPN source finite row"),
        ("SRC4015_06_4013_EM_stress", SRC / "P8_Y5_R2FR_4013_MAXWELL_POYNTING_ONCE_ONLY_THEOREM.csv", "MPE4013_1_Maxwell_Hilbert_stress", "EM stress belongs inside Hilbert source once"),
        ("SRC4015_07_4013_flux", SRC / "P8_Y5_R2FR_4013_MAXWELL_POYNTING_ONCE_ONLY_THEOREM.csv", "MPE4013_3_Poynting_flux_placement", "Poynting flux placement"),
        ("SRC4015_08_4014_norm", SRC / "P8_Y5_R2FR_4014_OBSERVED_HODGE_MAXWELL_OWNER_THEOREM.csv", "OHN4014_2_parent_Maxwell_normalization", "EM normalization owner"),
        ("SRC4015_09_4014_owner_vector", SRC / "P8_Y5_R2FR_4014_HODGE_F2_CURRENT_FINITE_ROWS.csv", "EMOWN4014_0_master", "EM owner finite vector"),
        ("SRC4015_10_PG0_charge", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG0_Hamiltonian_charge_input", "Hamiltonian charge input"),
        ("SRC4015_11_PG1_Hilbert", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG1_charge_equals_projected_Hilbert_source", "charge equals projected Hilbert source"),
        ("SRC4015_12_PG2_frame", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG2_same_frame_weak_field_potential", "same-frame weak-field potential"),
        ("SRC4015_13_PG3_Poisson", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG3_EH_to_Poisson_coefficient", "EH to Poisson coefficient"),
        ("SRC4015_14_PG4_Gauss", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG4_Gauss_surface_integral", "Gauss surface integral"),
        ("SRC4015_15_PG5_orbits", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG5_orbital_inverse_square_readout", "orbital inverse-square readout"),
        ("SRC4015_16_PG6_mu", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG6_zero_mu_extra_and_source_residuals", "extra measured-GM residuals"),
        ("SRC4015_17_PG7_constG", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG7_constant_universal_Geff", "constant universal Geff"),
        ("SRC4015_18_PG8_hair", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG8_no_derivative_hair", "no derivative hair"),
        ("SRC4015_19_PG9_PPN", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG9_second_order_source_stability", "second-order source stability"),
        ("SRC4015_20_PG10_fallback", SRC / "P8_Hamiltonian_charge_Poisson_Gauss_calibration_CONTRACT.csv", "PG10_retained_residual_fallback", "retained residual fallback"),
        ("SRC4015_21_KGL_delta_kappa", SRC / "P8_EM_fixed_kappa_Gref_action_line_lock.csv", "KGLR3511_0_delta_kappa", "delta kappa residual"),
        ("SRC4015_22_KGL_source_current", SRC / "P8_EM_fixed_kappa_Gref_action_line_lock.csv", "KGLR3511_2_delta_ellJ", "source-current normalization"),
        ("SRC4015_23_KGL_Gproduct", SRC / "P8_EM_fixed_kappa_Gref_action_line_lock.csv", "KGLR3511_4_Geff_product", "G product gate"),
        ("SRC4015_24_KGL_Gmatch", SRC / "P8_EM_fixed_kappa_Gref_action_line_lock.csv", "KGLR3511_5_epsilon_Gref_match", "Gref match guard"),
        ("SRC4015_25_CU0_same_frame", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU0_same_frame_EH_source", "same-frame EH source"),
        ("SRC4015_26_CU1_global", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU1_global_coupling_status", "global coupling status"),
        ("SRC4015_27_CU4_range", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU4_no_range_radial_running", "range/radial running"),
        ("SRC4015_28_CU6_policy", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU6_constant_only_calibration_policy", "constant-only calibration policy"),
        ("SRC4015_29_CU7_GM", SRC / "P8_constant_universal_Geff_kappa_CONTRACT.csv", "CU7_measured_GM_product_silence", "measured GM product silence"),
        ("SRC4015_30_GS0_factor", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS0_configuration_factorization", "global coupling factorization"),
        ("SRC4015_31_GS5_Bianchi", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS5_Bianchi_arbitrary_source_consistency", "Bianchi coupling consistency"),
        ("SRC4015_32_GS6_offset", SRC / "P8_global_coupling_superselection_CONTRACT.csv", "GS6_constant_offset_policy", "global constant offset policy"),
        ("SRC4015_33_Z0_decomp", SRC / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv", "Z0_decomposition_identity", "measured source decomposition"),
        ("SRC4015_34_Z1_global", SRC / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv", "Z1_global_coupling_superselection", "global coupling zero premise"),
        ("SRC4015_35_Z2_flux", SRC / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv", "Z2_calibrated_PiM_flux_conservation", "Pi_M flux conservation"),
        ("SRC4015_36_Z3_mu", SRC / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv", "Z3_mu_extra_zero_or_universal_constant", "mu_extra zero/universal premise"),
        ("SRC4015_37_Z5_radial", SRC / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv", "Z5_no_radial_or_range_hair", "radial/range hair premise"),
        ("SRC4015_38_Z8_PPN", SRC / "P8_CONSTANT_GM_ZERO_THEOREM_ATTEMPT.csv", "Z8_second_order_source_stability", "PPN stability premise"),
        ("SRC4015_39_decision", SRC / "P8_CONSTANT_GM_ZERO_OR_RESIDUAL_DECISION.csv", "constant_GM_promoted", "constant GM decision"),
        ("SRC4015_40_bound_Gdot", SRC / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv", "P8_Geff_time_drift", "Gdot residual target"),
        ("SRC4015_41_bound_range", SRC / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv", "P8_range_dependence", "range residual target"),
        ("SRC4015_42_bound_beta", SRC / "P8_CONSTANT_GM_RESIDUAL_BOUND_MATRIX.csv", "P8_nonlinear_beta_source_residue", "second-order beta residual target"),
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
            "theorem_id": "GPN4015_0_definitions",
            "claim_piece": "Newton bridge variables fixed before readout",
            "mathematical_form": "kappa_ref := 8*pi*G_ref/c^4; g_00=-(1+2*Phi/c^2)+O(c^-4); T_00^H=rho_H*c^2+O(v^2/c^2); M_H_ref=int rho_H dV_obs",
            "derived_result": "G_ref is a calibrated action/source coupling constant; M_H_ref is the parent Hamiltonian/Hilbert charge, not orbital GM divided by G_ref",
            "status": "EXACT_DEFINITION_LOCK_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GPN4015_1_EH00_to_Poisson",
            "claim_piece": "weak-field operator coefficient",
            "mathematical_form": "G_00^(1)=2*nabla^2 Phi/c^2 + Delta_EH00 and G_00=kappa_ref*T_00^H imply nabla^2 Phi=(kappa_ref*c^4/2)*rho_H + R_EH00",
            "derived_result": "if the reduced metric operator is EH in the observed frame and the source limit is nonrelativistic, the coefficient is 4*pi*G_ref",
            "status": "EXACT_CONDITIONAL_LINEARIZED_EH_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GPN4015_2_Poisson_to_Gauss",
            "claim_piece": "Gauss surface law",
            "mathematical_form": "int_S grad(Phi).dS = 4*pi*G_ref*M_H_ref + R_Gauss when d(Pi_M J_H)=0 and boundary/source fluxes vanish on the exterior annulus",
            "derived_result": "the same parent source charge controls the Poisson volume integral and the enclosing surface integral if the 4012 charge lock and boundary/nohair rows are signed",
            "status": "EXACT_CONDITIONAL_GAUSS_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GPN4015_3_Gauss_to_inverse_square",
            "claim_piece": "Newton inverse-square readout",
            "mathematical_form": "Phi=-G_ref*M_H_ref/r + Phi_multipole + Phi_res; a=-grad(Phi); for circular slow test motion v^2*r=G_ref*M_H_ref + R_orb",
            "derived_result": "orbital GM becomes a readout test of G_ref*M_H_ref, not the definition of M_H_ref",
            "status": "EXACT_CONDITIONAL_NEWTON_READOUT_THEOREM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GPN4015_4_no_orbital_laundering",
            "claim_piece": "anti-backfill rule",
            "mathematical_form": "M_H_ref cannot be set equal to GM_orb/G_ref; only Delta_orb := GM_orb-G_ref*M_H_ref may be scored after parent source ownership",
            "derived_result": "this prevents the theory from silently importing Newton's constant and mass from the data it is meant to explain",
            "status": "OVERCLAIM_GUARD_EXACT",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GPN4015_5_G_constant_policy",
            "claim_piece": "what is and is not derived about Newton's constant",
            "mathematical_form": "GR fixes kappa=8*pi*G/c^4 as a universal coupling but does not derive its numerical value; MTS may likewise calibrate G_ref unless a parent superselection/normalization theorem predicts it",
            "derived_result": "4015 can derive one shared coupling channel; it does not pretend to derive the absolute numerical value of G_ref",
            "status": "CALIBRATED_CONSTANT_POLICY",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GPN4015_6_Newton_bridge_vector",
            "claim_piece": "finite fallback if Newton bridge is not fully signed",
            "mathematical_form": "epsilon_Newton_bridge_4015 <= |Delta_EH00|+|Delta_NR_source|+|C_PiM_H|+|C_Gref_kappa|+|C_frame|+|C_units|+|C_Gauss_boundary|+|C_multipole|+|C_orbital_readout|+|mu_extra|/(G_ref*M_H_ref)+|epsilon_EM_once|+|epsilon_G_run|+|epsilon_range|+|epsilon_PPN_2nd|",
            "derived_result": "every possible failure of the Newton bridge is now a named residual, not a hidden fitted-GM manoeuvre",
            "status": "FINITE_NEWTON_BRIDGE_VECTOR_DERIVED_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "theorem_id": "GPN4015_7_Newton_not_local_GR",
            "claim_piece": "Newton bridge is not yet full local GR",
            "mathematical_form": "Poisson/Gauss/slow-geodesic agreement fixes the first-order scalar potential only; local GR also requires gamma=1, beta=1, conservation/Bianchi closure, and no extra sector PPN source terms",
            "derived_result": "a successful 4015 branch would be serious progress, but PPN second-order stability remains the next gate before local-GR promotion",
            "status": "ANTI_OVERCLAIM_GUARD",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def audit_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "audit_id": "SNA4015_0_same_action_EH_operator",
            "clause": "the reduced parent metric action has the EH weak-field 00 operator in the same observed frame",
            "current_status": "CONDITIONAL_NOT_PARENT_SIGNED",
            "risk_if_open": "Poisson coefficient can be shifted by extra scalar/vector/operator terms",
            "next_action": "prove EH operator reduction or retain Delta_EH00",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SNA4015_1_parent_source_charge",
            "clause": "rho_H integrates to the same M_H_ref owned by Pi_M/H_tau/Hilbert source equality",
            "current_status": "CONDITIONAL_4012_LOCK_UNSIGNED",
            "risk_if_open": "the source in Poisson is not the Hamiltonian charge used in tests",
            "next_action": "sign 4012 charge equality or retain C_PiM_H",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SNA4015_2_Gref_kappa_relation",
            "clause": "kappa_ref and G_ref are fixed before readout by kappa_ref=8*pi*G_ref/c^4",
            "current_status": "CALIBRATION_ALLOWED_SUPERSELECTION_UNSIGNED",
            "risk_if_open": "G may vary by time, radius, source, range, frame or domain",
            "next_action": "derive global coupling superselection or retain Gdot/range/source residuals",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SNA4015_3_boundary_Gauss",
            "clause": "exterior annulus has closed projected source current and no unowned boundary/radiative flux",
            "current_status": "CONDITIONAL_4010_4013_UNSIGNED",
            "risk_if_open": "surface integral differs from volume source charge",
            "next_action": "bind boundary nohair and Poynting once-only rows or retain C_Gauss_boundary",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SNA4015_4_slow_particle_readout",
            "clause": "ordinary matter test bodies follow the same observed metric potential with no fifth-force readout term",
            "current_status": "CONDITIONAL_NOT_PPN_SIGNED",
            "risk_if_open": "orbital GM is contaminated by readout/fifth-force terms",
            "next_action": "derive slow-geodesic matter limit or retain C_orbital_readout",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SNA4015_5_EM_once_inside_source",
            "clause": "bound EM energy/stress contributes to rho_H once and only once",
            "current_status": "CONDITIONAL_4013_4014_UNSIGNED",
            "risk_if_open": "source mass can double-count or delete EM/Poynting energy",
            "next_action": "adopt 4013/4014 EM owner package or retain epsilon_EM_once",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SNA4015_6_orbital_laundering_guard",
            "clause": "observed orbital GM is an output comparison, never an input definition of M_H_ref",
            "current_status": "GUARD_LOCKED",
            "risk_if_open": "Newton pass becomes circular",
            "next_action": "reject any row importing M_H_ref from GM_orb/G_ref",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "audit_id": "SNA4015_7_PPN_second_order",
            "clause": "first-order Newton bridge survives gamma/beta/source-normalized PPN order",
            "current_status": "DEFERRED_NOT_DERIVED",
            "risk_if_open": "Newtonian success is falsely promoted to local GR",
            "next_action": "after G_ref superselection, build PPN source-stability vector",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def finite_rows(timestamp: str) -> list[dict[str, Any]]:
    rows = [
        ("NBR4015_0_master", "epsilon_Newton_bridge_4015", "|Delta_EH00|+|Delta_NR_source|+|C_PiM_H|+|C_Gref_kappa|+|C_frame|+|C_units|+|C_Gauss_boundary|+|C_multipole|+|C_orbital_readout|+|mu_extra|/(G_ref*M_H_ref)+|epsilon_EM_once|+|epsilon_G_run|+|epsilon_range|+|epsilon_PPN_2nd|", "MISSING_COMPONENT_VALUES_OR_PARENT_SIGNATURES", "dimensionless envelope", "Newton bridge residual master", "Newton; orbital_GM; PPN; R10; clocks"),
        ("NBR4015_1_Delta_EH00", "Delta_EH00", "G_00^(1)-2*nabla^2(Phi)/c^2 plus non-EH 00 operator pieces", "ZERO_IF_REDUCED_EH_OPERATOR_SIGNED_ELSE_MISSING_BOUND", "1/length^2", "weak-field operator mismatch", "PPN; local_GR"),
        ("NBR4015_2_Delta_NR_source", "Delta_NR_source", "T_00^H/(rho_H*c^2)-1 plus pressure/relativistic/source-frame corrections", "ZERO_IF_NONRELATIVISTIC_SOURCE_LIMIT_SIGNED_ELSE_MISSING_BOUND", "dimensionless", "source density limit", "Newton; clocks"),
        ("NBR4015_3_C_PiM_H", "C_PiM_H", "M_H[Pi_M J_H]-(H_tau-H_ref) on the same exterior annulus and frame", "ZERO_IF_4012_CHARGE_LOCK_SIGNED_ELSE_RETAIN", "mass or dimensionless ratio", "Hamiltonian/Hilbert charge mismatch", "Newton; WEP; orbital_GM"),
        ("NBR4015_4_C_Gref_kappa", "C_Gref_kappa", "kappa_eff*c^4/(8*pi*G_ref)-1", "ZERO_IF_GREF_KAPPA_CALIBRATION_FIXED_ELSE_RETAIN", "dimensionless", "coupling normalization mismatch", "Gdot; Newton; PPN"),
        ("NBR4015_5_C_frame_units", "C_frame_plus_C_units", "same observed tau/coframe/units mismatch between EH operator, source charge, and orbital readout", "ZERO_IF_SINGLE_OBSERVED_FRAME_SIGNED_ELSE_RETAIN", "dimensionless", "frame/unit calibration split", "clocks; PPN; orbital_GM"),
        ("NBR4015_6_C_Gauss_boundary", "C_Gauss_boundary", "surface integral residual from unclosed source current, boundary, domain, memory, or radiative flux", "ZERO_IF_CLOSED_EXTERIOR_AND_ZERO_FLUX_SIGNED_ELSE_RETAIN", "potential flux", "Gauss law boundary residual", "R10; orbital_GM"),
        ("NBR4015_7_C_multipole", "C_multipole", "non-monopole exterior potential terms retained when pure 1/r readout is assumed", "ZERO_FOR_MONOPOLE_OR_FAR_FIELD_PROJECTION_SIGNED_ELSE_RETAIN", "dimensionless or potential", "inverse-square shape residual", "orbital systems"),
        ("NBR4015_8_C_orbital_readout", "C_orbital_readout", "GM_orb-G_ref*M_H_ref after slow-geodesic and no-fifth-force projection", "OUTPUT_COMPARISON_ONLY_NOT_INPUT", "m^3/s^2 or dimensionless ratio", "orbital readout residual", "orbital_GM; PPN"),
        ("NBR4015_9_mu_extra", "mu_extra_over_GM", "mu_extra/(G_ref*M_H_ref) from boundary, bulk, domain, memory, non-Hilbert, or apparatus source terms", "ZERO_IF_MU_EXTRA_OWNER_SIGNED_ELSE_RETAIN", "dimensionless", "measured-GM hidden source correction", "Gdot; WEP; R10"),
        ("NBR4015_10_epsilon_EM_once", "epsilon_EM_once", "Delta_Hodge_EM+w_EM+C_XF2+C_JQ+Phi_EM_rad/(G_ref*M_H_ref)+C_EM_readout+binding once-only terms", "ZERO_IF_4013_4014_EM_OWNER_SIGNED_ELSE_RETAIN", "dimensionless", "EM stress/Poynting once-only source residual", "EM; Newton; WEP"),
        ("NBR4015_11_epsilon_G_run", "epsilon_G_run", "D_X ln G_ref over time, radius, source label, range, frame, or domain", "ZERO_IF_GLOBAL_COUPLING_SUPERSELECTION_SIGNED_ELSE_RETAIN", "dimensionless or rate", "running coupling residual", "Gdot; R10; PPN"),
        ("NBR4015_12_epsilon_range", "epsilon_range", "alpha(lambda) or finite-range/radial source-hair projection", "ZERO_IF_NO_RANGE_RADIAL_HAIR_SIGNED_ELSE_CURVE_REQUIRED", "dimensionless", "finite-range Newton residual", "R10; orbital systems"),
        ("NBR4015_13_epsilon_PPN_2nd", "epsilon_PPN_2nd", "|gamma-1|+|beta-1|+|delta_beta_source| after measured-GM normalization", "DEFERRED_REQUIRED_FOR_LOCAL_GR", "dimensionless", "second-order local-GR source stability", "PPN; local_GR"),
    ]
    return [
        {
            "row_id": row_id,
            "coefficient": coefficient,
            "formula": formula,
            "value": value,
            "units": units,
            "role": role,
            "observable_links": observable_links,
            "status": "FINITE_NONCLAIM_ROW",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for row_id, coefficient, formula, value, units, role, observable_links in rows
    ]


def case_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "case_id": "CASE4015_0_full_Newton_bridge_signed",
            "EH_operator": True,
            "charge_lock": True,
            "Gref_kappa_fixed": True,
            "Gauss_boundary_closed": True,
            "slow_geodesic_readout": True,
            "EM_once_owned": True,
            "G_universal": True,
            "PPN_second_order": False,
            "orbital_import": False,
            "description": "all first-order Newton bridge clauses signed; PPN still deferred",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4015_1_EH_operator_open",
            "EH_operator": False,
            "charge_lock": True,
            "Gref_kappa_fixed": True,
            "Gauss_boundary_closed": True,
            "slow_geodesic_readout": True,
            "EM_once_owned": True,
            "G_universal": True,
            "PPN_second_order": False,
            "orbital_import": False,
            "description": "Poisson coefficient not owned by reduced EH operator",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4015_2_charge_lock_open",
            "EH_operator": True,
            "charge_lock": False,
            "Gref_kappa_fixed": True,
            "Gauss_boundary_closed": True,
            "slow_geodesic_readout": True,
            "EM_once_owned": True,
            "G_universal": True,
            "PPN_second_order": False,
            "orbital_import": False,
            "description": "Poisson source not identical to Hamiltonian/Hilbert charge",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4015_3_Gref_kappa_open",
            "EH_operator": True,
            "charge_lock": True,
            "Gref_kappa_fixed": False,
            "Gauss_boundary_closed": True,
            "slow_geodesic_readout": True,
            "EM_once_owned": True,
            "G_universal": False,
            "PPN_second_order": False,
            "orbital_import": False,
            "description": "G_ref/kappa calibration or universality not signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4015_4_Gauss_boundary_open",
            "EH_operator": True,
            "charge_lock": True,
            "Gref_kappa_fixed": True,
            "Gauss_boundary_closed": False,
            "slow_geodesic_readout": True,
            "EM_once_owned": True,
            "G_universal": True,
            "PPN_second_order": False,
            "orbital_import": False,
            "description": "surface integral has boundary/multipole/mu_extra leakage",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4015_5_geodesic_readout_open",
            "EH_operator": True,
            "charge_lock": True,
            "Gref_kappa_fixed": True,
            "Gauss_boundary_closed": True,
            "slow_geodesic_readout": False,
            "EM_once_owned": True,
            "G_universal": True,
            "PPN_second_order": False,
            "orbital_import": False,
            "description": "test bodies do not yet read the same potential cleanly",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4015_6_EM_once_open",
            "EH_operator": True,
            "charge_lock": True,
            "Gref_kappa_fixed": True,
            "Gauss_boundary_closed": True,
            "slow_geodesic_readout": True,
            "EM_once_owned": False,
            "G_universal": True,
            "PPN_second_order": False,
            "orbital_import": False,
            "description": "EM/Poynting stress source bookkeeping is not fully signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4015_7_PPN_overclaim",
            "EH_operator": True,
            "charge_lock": True,
            "Gref_kappa_fixed": True,
            "Gauss_boundary_closed": True,
            "slow_geodesic_readout": True,
            "EM_once_owned": True,
            "G_universal": True,
            "PPN_second_order": False,
            "orbital_import": False,
            "description": "Newtonian bridge is incorrectly promoted to local GR",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4015_8_orbital_laundering_attempt",
            "EH_operator": True,
            "charge_lock": False,
            "Gref_kappa_fixed": True,
            "Gauss_boundary_closed": True,
            "slow_geodesic_readout": True,
            "EM_once_owned": True,
            "G_universal": True,
            "PPN_second_order": False,
            "orbital_import": True,
            "description": "tries to define M_H_ref from observed orbital GM",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "case_id": "CASE4015_9_numeric_nonclaim_pack",
            "EH_operator": False,
            "charge_lock": False,
            "Gref_kappa_fixed": False,
            "Gauss_boundary_closed": False,
            "slow_geodesic_readout": False,
            "EM_once_owned": False,
            "G_universal": False,
            "PPN_second_order": False,
            "orbital_import": False,
            "description": "component rows exist but are not numerically sourced or parent signed",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def truthy(row: dict[str, Any], key: str) -> bool:
    return str(row[key]).lower() == "true" if isinstance(row[key], str) else bool(row[key])


def result_rows(cases: list[dict[str, Any]], timestamp: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for row in cases:
        case_id = row["case_id"]
        if truthy(row, "orbital_import"):
            owner_status = "ORBITAL_GM_LAUNDERING_REJECTED"
            residual_result = "C_PiM_H_UNOWNED_AND_IMPORT_FORBIDDEN"
            claim_result = "NO_NEWTON_SOURCE_CLAIM"
            next_action = "derive M_H_ref from parent charge or keep orbital GM as output-only comparison"
        elif case_id == "CASE4015_0_full_Newton_bridge_signed":
            owner_status = "CONDITIONAL_NEWTON_GAUSS_POISSON_LOCK"
            residual_result = "DELTA_EH00_CPiMH_GAUSS_ORBITAL_ZERO_IF_PARENT_SIGNED"
            claim_result = "NEWTON_LIMIT_CONDITIONAL_ONLY_LOCAL_GR_NOT_CLAIMED"
            next_action = "move to G_ref superselection and then PPN second-order source stability"
        elif not truthy(row, "EH_operator"):
            owner_status = "NEWTON_BRIDGE_BLOCKED"
            residual_result = "Delta_EH00+Delta_NR_source"
            claim_result = "NO_POISSON_COEFFICIENT_CLAIM"
            next_action = "prove reduced EH 00 operator or keep operator residual rows"
        elif not truthy(row, "charge_lock"):
            owner_status = "NEWTON_BRIDGE_BLOCKED"
            residual_result = "C_PiM_H"
            claim_result = "NO_SOURCE_MASS_CLAIM"
            next_action = "close Pi_M/H_tau/Hilbert charge equality before using Newton mass"
        elif not truthy(row, "Gref_kappa_fixed") or not truthy(row, "G_universal"):
            owner_status = "GREF_CALIBRATION_BLOCKED"
            residual_result = "C_Gref_kappa+epsilon_G_run+epsilon_range"
            claim_result = "NO_CONSTANT_UNIVERSAL_G_CLAIM"
            next_action = "derive global coupling superselection or source Gdot/range/source residual rows"
        elif not truthy(row, "Gauss_boundary_closed"):
            owner_status = "GAUSS_SURFACE_BLOCKED"
            residual_result = "C_Gauss_boundary+C_multipole+mu_extra_over_GM"
            claim_result = "NO_INVERSE_SQUARE_SURFACE_CLAIM"
            next_action = "close boundary/worldtube/nohair and mu_extra rows"
        elif not truthy(row, "slow_geodesic_readout"):
            owner_status = "ORBITAL_READOUT_BLOCKED"
            residual_result = "C_orbital_readout+fifth_force_readout"
            claim_result = "NO_ORBITAL_GM_CLAIM"
            next_action = "derive slow-particle same-frame geodesic limit"
        elif not truthy(row, "EM_once_owned"):
            owner_status = "SOURCE_STRESS_BOOKKEEPING_BLOCKED"
            residual_result = "epsilon_EM_once"
            claim_result = "NO_ACTIVE_SOURCE_CLAIM"
            next_action = "close Maxwell/Poynting once-only owner"
        elif case_id == "CASE4015_7_PPN_overclaim" or not truthy(row, "PPN_second_order"):
            owner_status = "NEWTON_ONLY_NOT_LOCAL_GR"
            residual_result = "epsilon_PPN_2nd"
            claim_result = "NO_LOCAL_GR_PROMOTION"
            next_action = "run second-order PPN source-stability after first-order coupling is locked"
        else:
            owner_status = "FINITE_NEWTON_BRIDGE_PACK_NONCLAIM"
            residual_result = "FULL_RESIDUAL_VECTOR_REQUIRED"
            claim_result = "NO_CLAIM"
            next_action = "fill numeric/source-backed residual rows"
        rows.append(
            {
                "case_id": case_id,
                "owner_status": owner_status,
                "residual_result": residual_result,
                "claim_result": claim_result,
                "next_action": next_action,
                "valid_for_claim": False,
                "timestamp_utc": timestamp,
            }
        )
    return rows


def decision_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "decision_id": "DEC4015_0_bridge_derived",
            "decision": "keep Gauss/Poisson/Newton bridge as exact conditional theorem",
            "rationale": "the same chain can connect EH weak-field operator, Hilbert/Hamiltonian source charge, Gauss surface law, and orbital readout",
            "effect": "Newton route is sharper and no longer just missing-G vibes",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4015_1_G_not_predicted",
            "decision": "do not claim numerical prediction of Newton's constant",
            "rationale": "GR calibrates G; MTS can be competitive if it derives one universal coupling channel rather than source-by-source fitted GM",
            "effect": "absolute G value remains calibration unless a deeper parent normalization theorem is found",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4015_2_no_orbital_laundering",
            "decision": "orbital GM is output-only",
            "rationale": "using GM_orb to define M_H_ref would make the Newton pass circular",
            "effect": "M_H_ref must come from 4012 parent charge lock",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
        {
            "decision_id": "DEC4015_3_next_best_target",
            "decision": f"move to {NEXT_DOC}",
            "rationale": "the most immediate remaining throat is whether G_ref/kappa is a global superselected constant or a live residual field",
            "effect": "PPN source stability waits until first-order coupling is not drifting",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        },
    ]


def claim_gate_rows(timestamp: str) -> list[dict[str, Any]]:
    gates = [
        ("CLAIM4015_0_Newton_limit", "conditional Newton bridge", False, "parent signatures not all adopted; output remains private nonclaim"),
        ("CLAIM4015_1_constant_G", "constant universal G_ref", False, "superselection/global coupling theorem unsigned"),
        ("CLAIM4015_2_orbital_GM", "orbital GM prediction", False, "orbital GM is only an output comparison until M_H_ref and G_ref are independently owned"),
        ("CLAIM4015_3_local_GR", "local GR recovery", False, "PPN gamma/beta/source stability not derived"),
        ("CLAIM4015_4_R10_PPN_clock", "R10/PPN/clock empirical pass", False, "finite residual vector lacks numeric sourced rows"),
    ]
    return [
        {
            "claim_id": claim_id,
            "claim": claim,
            "allowed": allowed,
            "reason": reason,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
        for claim_id, claim, allowed, reason in gates
    ]


def next_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "row_id": "NEXT4015_0",
            "next_doc": NEXT_DOC,
            "next_script": NEXT_SCRIPT,
            "objective": "derive whether G_ref/kappa is a global superselected calibration constant, or convert Gdot, source-label, radial and range dependence into explicit residual rows",
            "success_condition": "G_ref is fixed before readout and has no time, radius, source, range, frame or domain derivative; otherwise every live derivative is retained as a nonclaim bound input",
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def status_rows(timestamp: str) -> list[dict[str, Any]]:
    return [
        {
            "checkpoint": CHECKPOINT,
            "status": "COMPLETE_NONCLAIM",
            "summary": "Gauss/Poisson/G_ref/Newton bridge derived as an exact conditional route from parent Hilbert/Hamiltonian source charge to Newtonian readout, with orbital-GM laundering blocked and finite residual vector retained.",
            "claim_allowed": False,
            "next_doc": NEXT_DOC,
            "valid_for_claim": False,
            "timestamp_utc": timestamp,
        }
    ]


def write_doc(timestamp: str, sources: list[dict[str, Any]], results: list[dict[str, Any]]) -> None:
    found = sum(1 for row in sources if row["needle_found"])
    lines = [
        "# 4015 - Gauss/Poisson/G_ref Source Normalization Or Newton Row",
        "",
        f"- Timestamp: `{timestamp}`",
        "- Status: `private_nonclaim_checkpoint`",
        "- Scope: `post-checkpoint-work` only; no `formalization-workbench` edits.",
        "",
        "## Result",
        "",
        "This checkpoint turns the Newton side into an actual bridge rather than another missing-coupling fog bank.",
        "",
        "Definitions are now fixed before orbital readout:",
        "",
        "`kappa_ref := 8*pi*G_ref/c^4`",
        "",
        "`g_00=-(1+2*Phi/c^2)+O(c^-4)`",
        "",
        "`T_00^H=rho_H*c^2+O(v^2/c^2)`",
        "",
        "`M_H_ref=int rho_H dV_obs`",
        "",
        "If the reduced EH 00 operator, same-frame nonrelativistic source limit, 4012 charge lock, Gauss boundary closure, and slow-geodesic matter readout are all signed, then",
        "",
        "`nabla^2 Phi=4*pi*G_ref*rho_H`",
        "",
        "`int_S grad(Phi).dS=4*pi*G_ref*M_H_ref`",
        "",
        "`Phi=-G_ref*M_H_ref/r` and `v^2*r=G_ref*M_H_ref` in the clean monopole slow-orbit branch.",
        "",
        "That is the right reduction target: `GM_orb` tests `G_ref*M_H_ref`; it does not define either side.",
        "",
        "## Newton Constant Policy",
        "",
        "This does not claim the numerical value of Newton's constant is derived. GR itself fixes how one universal `G` couples geometry to stress; it does not derive the number from Newtonian mechanics. The MTS target is therefore: one parent-owned, source-blind `G_ref` used by the EH operator, Hamiltonian charge, Poisson law, Gauss law, and orbital readout. A deeper derivation of `G_ref` is a later superselection/normalization target, not something to smuggle in here.",
        "",
        "## Finite Bridge Vector",
        "",
        "`epsilon_Newton_bridge_4015 <= |Delta_EH00|+|Delta_NR_source|+|C_PiM_H|+|C_Gref_kappa|+|C_frame|+|C_units|+|C_Gauss_boundary|+|C_multipole|+|C_orbital_readout|+|mu_extra|/(G_ref*M_H_ref)+|epsilon_EM_once|+|epsilon_G_run|+|epsilon_range|+|epsilon_PPN_2nd|`.",
        "",
        "## Evaluator Results",
        "",
    ]
    for row in results:
        lines.append(
            f"- `{row['case_id']}`: owner=`{row['owner_status']}`, residual=`{row['residual_result']}`, claim=`{row['claim_result']}`, next=`{row['next_action']}`"
        )
    lines.extend(
        [
            "",
            "## Verdict",
            "",
            "This is a real forward step. The Newton limit is now expressed as a conditional derivation chain with an anti-circularity guard. The grim bit is still honest: without G_ref superselection and second-order PPN stability, this is not local GR yet. The good bit is that the target is now narrow enough to attack.",
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
    marker = "## 4015 - Gauss/Poisson/Gref Newton Bridge"
    block = f"""

{marker}

- Timestamp: `{timestamp}`
- Result: the Newton bridge is now an exact conditional chain: `kappa_ref=8*pi*G_ref/c^4`, `G_00^(1)=2 nabla^2 Phi/c^2`, `T_00^H=rho_H c^2`, hence `nabla^2 Phi=4*pi*G_ref rho_H` when the reduced EH operator and same-frame source limit are signed.
- Source lock: the Gauss mass is `M_H_ref=int rho_H dV_obs`, tied to the 4012 `Pi_M/H_tau/Hilbert` charge route; orbital `GM` is output-only and cannot define `M_H_ref`.
- Surface/readout lock: `int_S grad(Phi).dS=4*pi*G_ref M_H_ref` and `v^2 r=G_ref M_H_ref` follow only after boundary/nohair, EM/Poynting once-only and slow-geodesic readout clauses close.
- G policy: numerical `G_ref` is not claimed as predicted; the derivation target is one universal source-blind coupling, with deeper absolute normalization left to superselection/normalization work.
- Finite fallback: `epsilon_Newton_bridge_4015 <= |Delta_EH00|+|Delta_NR_source|+|C_PiM_H|+|C_Gref_kappa|+|C_frame|+|C_units|+|C_Gauss_boundary|+|C_multipole|+|C_orbital_readout|+|mu_extra|/(G_ref*M_H_ref)+|epsilon_EM_once|+|epsilon_G_run|+|epsilon_range|+|epsilon_PPN_2nd|`.
- No claim: Newton bridge is conditional and not yet local GR; PPN gamma/beta and G_ref superselection remain open.
- Next: `{NEXT_DOC}`.
"""
    current = read_text(SPINE_PATH)
    if marker not in current:
        SPINE_PATH.write_text(current.rstrip() + block + "\n", encoding="utf-8")


def marker_in_spine() -> bool:
    return "## 4015 - Gauss/Poisson/Gref Newton Bridge" in read_text(SPINE_PATH)


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

    add("VAL4015_00_sources_exist", all(bool(row["exists"]) for row in sources), "every cited source path exists")
    add("VAL4015_01_needles_found", all(bool(row["needle_found"]) for row in sources), "every cited source needle found")
    for idx, theorem_id in enumerate(
        [
            "GPN4015_0_definitions",
            "GPN4015_1_EH00_to_Poisson",
            "GPN4015_2_Poisson_to_Gauss",
            "GPN4015_3_Gauss_to_inverse_square",
            "GPN4015_4_no_orbital_laundering",
            "GPN4015_5_G_constant_policy",
            "GPN4015_6_Newton_bridge_vector",
            "GPN4015_7_Newton_not_local_GR",
        ],
        start=2,
    ):
        add(f"VAL4015_{idx:02d}_theorem", any(row["theorem_id"] == theorem_id for row in theorem), f"{theorem_id} present")
    for idx, audit_id in enumerate(
        [
            "SNA4015_0_same_action_EH_operator",
            "SNA4015_1_parent_source_charge",
            "SNA4015_2_Gref_kappa_relation",
            "SNA4015_3_boundary_Gauss",
            "SNA4015_4_slow_particle_readout",
            "SNA4015_5_EM_once_inside_source",
            "SNA4015_6_orbital_laundering_guard",
            "SNA4015_7_PPN_second_order",
        ],
        start=10,
    ):
        add(f"VAL4015_{idx:02d}_audit", any(row["audit_id"] == audit_id for row in audit), f"{audit_id} present")
    master = next(row for row in finite if row["row_id"] == "NBR4015_0_master")
    add("VAL4015_18_master_vector", "C_Gref_kappa" in master["formula"] and "epsilon_PPN_2nd" in master["formula"], "master vector contains Gref and PPN guards")
    for idx, row_id in enumerate(
        [
            "NBR4015_1_Delta_EH00",
            "NBR4015_2_Delta_NR_source",
            "NBR4015_3_C_PiM_H",
            "NBR4015_4_C_Gref_kappa",
            "NBR4015_5_C_frame_units",
            "NBR4015_6_C_Gauss_boundary",
            "NBR4015_7_C_multipole",
            "NBR4015_8_C_orbital_readout",
            "NBR4015_9_mu_extra",
            "NBR4015_10_epsilon_EM_once",
            "NBR4015_11_epsilon_G_run",
            "NBR4015_12_epsilon_range",
            "NBR4015_13_epsilon_PPN_2nd",
        ],
        start=19,
    ):
        add(f"VAL4015_{idx:02d}_{row_id}", any(row["row_id"] == row_id for row in finite), f"{row_id} present")
    full = next(row for row in results if row["case_id"] == "CASE4015_0_full_Newton_bridge_signed")
    eh_open = next(row for row in results if row["case_id"] == "CASE4015_1_EH_operator_open")
    charge_open = next(row for row in results if row["case_id"] == "CASE4015_2_charge_lock_open")
    g_open = next(row for row in results if row["case_id"] == "CASE4015_3_Gref_kappa_open")
    gauss_open = next(row for row in results if row["case_id"] == "CASE4015_4_Gauss_boundary_open")
    geo_open = next(row for row in results if row["case_id"] == "CASE4015_5_geodesic_readout_open")
    em_open = next(row for row in results if row["case_id"] == "CASE4015_6_EM_once_open")
    ppn = next(row for row in results if row["case_id"] == "CASE4015_7_PPN_overclaim")
    laundering = next(row for row in results if row["case_id"] == "CASE4015_8_orbital_laundering_attempt")
    add("VAL4015_32_full_case", full["owner_status"] == "CONDITIONAL_NEWTON_GAUSS_POISSON_LOCK", "full first-order bridge locks conditionally")
    add("VAL4015_33_EH_case", eh_open["residual_result"] == "Delta_EH00+Delta_NR_source", "EH operator failure routed")
    add("VAL4015_34_charge_case", charge_open["residual_result"] == "C_PiM_H", "charge lock failure routed")
    add("VAL4015_35_G_case", "epsilon_G_run" in g_open["residual_result"], "Gref/g-running failure routed")
    add("VAL4015_36_Gauss_case", "C_Gauss_boundary" in gauss_open["residual_result"], "Gauss boundary failure routed")
    add("VAL4015_37_geodesic_case", "C_orbital_readout" in geo_open["residual_result"], "orbital readout failure routed")
    add("VAL4015_38_EM_case", em_open["residual_result"] == "epsilon_EM_once", "EM once-only failure routed")
    add("VAL4015_39_PPN_guard", ppn["owner_status"] == "NEWTON_ONLY_NOT_LOCAL_GR", "PPN overclaim blocked")
    add("VAL4015_40_laundering_guard", laundering["owner_status"] == "ORBITAL_GM_LAUNDERING_REJECTED", "orbital GM laundering rejected")
    add("VAL4015_41_claim_gate_false", all(str(row.get("allowed", "")).lower() == "false" for row in read_csv(OUTPUTS["claim_gate"])), "all claim gates false")
    add("VAL4015_42_next_target", OUTPUTS["next"].exists() and NEXT_DOC in read_text(OUTPUTS["next"]), "next target written")
    add("VAL4015_43_doc_exists", DOC_PATH.exists() and "kappa_ref := 8*pi*G_ref/c^4" in read_text(DOC_PATH), "document written with Gref policy")
    add("VAL4015_44_spine_updated", SPINE_PATH.exists() and marker_in_spine(), "spine updated")
    add("VAL4015_45_no_fwb_outputs", not any(str(path).startswith(str(FWB)) for path in OUTPUTS.values()), "no outputs target formalization-workbench")
    add("VAL4015_46_compile", compile_ok, "script compiles")
    add("VAL4015_47_no_pycache", not (SCRIPT_PATH.parent / "__pycache__").exists(), "script __pycache__ removed")
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
    add("VAL4015_48_all_nonclaim", all(str(row.get("valid_for_claim", "")).lower() == "false" for table in output_tables for row in table), "all emitted rows remain nonclaim")
    add("VAL4015_49_no_nan", not any("nan" in str(row).lower() or "inf" in str(row).lower() for row in results), "no nan/inf evaluator outputs")
    add("VAL4015_50_private_scope", DOC_PATH.exists() and "private_nonclaim_checkpoint" in read_text(DOC_PATH), "private scope recorded")
    add("VAL4015_51_no_absolute_G_claim", "does not claim the numerical value" in read_text(DOC_PATH), "absolute G value not claimed")
    add("VAL4015_52_output_only_GM", "GM_orb` tests `G_ref*M_H_ref`" in read_text(DOC_PATH), "orbital GM output-only policy recorded")
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
    print(f"4015 validation: {passed}/{total} passed")
    if passed != total:
        for row in validation:
            if not row["passed"]:
                print(f"FAIL {row['check_id']}: {row['detail']}")
        raise SystemExit(1)
    print(f"Wrote {DOC_PATH}")


if __name__ == "__main__":
    main()
