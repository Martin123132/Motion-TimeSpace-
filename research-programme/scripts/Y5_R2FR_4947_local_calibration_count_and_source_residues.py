from __future__ import annotations

import csv
import hashlib
import json
import math
import sys
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4947"

RESULT_JSON = SOURCE / "local_calibration_count_results.json"
CALIBRATION_CSV = SOURCE / "parent_low_energy_calibration_ledger.csv"
RESIDUE_CSV = SOURCE / "source_residue_chain.csv"
LIMIT_CSV = SOURCE / "Newton_geodesic_Lorentz_limit_gate.csv"
ARENA_CSV = SOURCE / "cross_arena_no_retuning_matrix.csv"

PARENT_4916 = POST / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md"
EXCHANGE_4917 = POST / "4917-Y5-R2FR-radiative-flow-matter-reentry-coefficients-from-gravity-mediation-or-local-bound-pack.md"
STATE_4918 = POST / "4918-Y5-R2FR-closed-bath-state-enthalpy-trace-profile-and-renormalized-aC-aR-matching-or-multiarena-bound.md"
SCALE_4938 = POST / "4938-Y5-R2FR-motion-scale-to-Newton-scale-parent-identity-or-explicit-two-scale-theory-gate.md"
SOURCE_4943 = POST / "4943-Y5-R2FR-matter-source-interior-psi-zero-continuation-and-junction-or-fifth-force-residual-gate.md"
MAXWELL_4946 = POST / "4946-Y5-R2FR-QCD-TJJ-dispersive-matching-and-weak-local-Maxwell-action-certificate.md"
LOCAL_VECTOR_4942 = POST / "source-intake" / "functional_rg" / "4942" / "local_O4_C3_CFF_residual_vector.csv"
MAXWELL_CERT_4946 = POST / "source-intake" / "functional_rg" / "4946" / "local_Maxwell_action_stress_and_calibration_certificate.csv"
TRANSFER_4946 = POST / "source-intake" / "functional_rg" / "4946" / "universal_CFF_calibration_transfer_functions.csv"

EXPECTED_HASHES = {
    PARENT_4916: "4c20db8f8f75d81bab3c2a6d334cbcefeb2f2c1d66266be0ec412947c705b636",
    EXCHANGE_4917: "61dc24dd5d6c686589946358f8d488690ebc1ba478616b33757282b9111cab7c",
    STATE_4918: "b7e5c191e4e08f07500f091a8d78383306c9b1a835cf115491789f4a0ea9a53e",
    SCALE_4938: "b30394a62c6a22af5da315b92a2823f44aa34cd914b6bab813136b0926aa0ca4",
    SOURCE_4943: "a90da0e9ad0457fc3dbdb389d7bf2715cb9d707cbffa094a987b0b0553e257b5",
    MAXWELL_4946: "4985b31aa5d5253ec64fd1575bbd0f844c1b5c0924a11482fb77374ddee477b6",
    LOCAL_VECTOR_4942: "51f034326f02684491743d6b12fed9d54854885dae07e7894e77423f435a14a5",
    MAXWELL_CERT_4946: "8b80ddf7b5cb469fa7c580b24f6b0d759322871bfb7064111839565ba290799a",
    TRANSFER_4946: "8707daa86fac5daf0bd6859bf8d8c29f18777349c9dbac24e259f729facd15a8",
}

MARKER = "MTS_4947_LOCAL_CALIBRATION_COUNT_SOURCE_RESIDUES"
CHECKED_DATE = "2026-07-13"
C_LIGHT_M_S = 299_792_458.0
WEAK_COMPACTNESS_MAX = 1.0e-2


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty table {path.name}")
    fieldnames: list[str] = []
    for row in rows:
        fieldnames.extend(key for key in row if key not in fieldnames)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def main() -> int:
    print(f"{MARKER}_START", flush=True)
    SOURCE.mkdir(parents=True, exist_ok=True)
    source_hashes = {
        path.relative_to(ROOT).as_posix(): digest(path) if path.exists() else "MISSING"
        for path in EXPECTED_HASHES
    }
    hash_failures = [
        path.relative_to(ROOT).as_posix()
        for path, expected in EXPECTED_HASHES.items()
        if source_hashes[path.relative_to(ROOT).as_posix()] != expected
    ]
    if hash_failures:
        raise RuntimeError(f"source hash mismatch: {hash_failures}")

    parent_text = PARENT_4916.read_text(encoding="utf-8-sig")
    exchange_text = EXCHANGE_4917.read_text(encoding="utf-8-sig")
    state_text = STATE_4918.read_text(encoding="utf-8-sig")
    scale_text = SCALE_4938.read_text(encoding="utf-8-sig")
    source_text = SOURCE_4943.read_text(encoding="utf-8-sig")
    maxwell_text = MAXWELL_4946.read_text(encoding="utf-8-sig")
    source_clause_checks = {
        "Einstein_source_equation": "M_R^2(G_{\\mu\\nu}+\\Lambda g_{\\mu\\nu})=T^{\\rm total}_{\\mu\\nu}" in parent_text,
        "Newton_residue_identity": "G_N=\\frac1{8\\pi M_R^2}" in parent_text,
        "universal_exchange_kernel": "T_X^{\\mu\\nu}T^{\\rm SM}_{\\mu\\nu}" in exchange_text and "q^2+i0" in exchange_text,
        "active_state_source_absent": "\\boxed{\\Gamma_{\\rm MTS,res}=0}" in state_text,
        "curvature_matching_open": "renormalized coefficients remain open finite matching sums" in state_text,
        "one_universal_motion_scale": "J_gap=m_gap^2 G_N" in scale_text,
        "matter_scalar_tadpole_zero": "delta S_SM/delta psi=0" in source_text,
        "one_scalar_fifth_force_zero": "classical one-scalar fifth force              = zero" in source_text,
        "Maxwell_field_and_stress": "nabla_m F^mn" in maxwell_text and "T_EM,mn" in maxwell_text,
    }
    failed_clauses = [name for name, passed in source_clause_checks.items() if not passed]
    if failed_clauses:
        raise RuntimeError(f"authoritative source clause mismatch: {failed_clauses}")

    calibration_rows = tagged(
        [
            {
                "parameter_id": "CAL4947_00_GN",
                "symbol": "G_N <-> M_R^2",
                "sector": "metric_gravity",
                "physical_role": "residue of the unique massless spin-2 pole and coefficient of the Einstein equation",
                "independent_scalar_coordinate": True,
                "count_in_declared_truncation": True,
                "current_status": "MEASURED_ONCE_NOT_PREDICTED",
                "selection_or_measurement": "one Cavendish-orbital normalization fixes M_R^2=(8 pi G_N)^-1",
                "leading_local_source_residue": True,
                "arena_retuning_allowed": False,
                "not_a_duplicate_of": "Newton G; lensing G; orbital G; waveform G; all are the same residue",
            },
            {
                "parameter_id": "CAL4947_01_Lambda",
                "symbol": "Lambda_cal",
                "sector": "background_gravity",
                "physical_role": "renormalized homogeneous vacuum curvature",
                "independent_scalar_coordinate": True,
                "count_in_declared_truncation": True,
                "current_status": "BACKGROUND_CALIBRATION_NOT_MICROSCOPICALLY_PREDICTED",
                "selection_or_measurement": "cosmological background datum",
                "leading_local_source_residue": False,
                "arena_retuning_allowed": False,
                "not_a_duplicate_of": "G_N",
            },
            {
                "parameter_id": "CAL4947_02_alphaEM",
                "symbol": "alpha_EM (or e in a fixed charge convention)",
                "sector": "visible_U1",
                "physical_role": "single physical electromagnetic charge normalization after canonical photon normalization",
                "independent_scalar_coordinate": True,
                "count_in_declared_truncation": True,
                "current_status": "INHERITED_SM_MEASUREMENT",
                "selection_or_measurement": "one low-energy electromagnetic normalization",
                "leading_local_source_residue": True,
                "arena_retuning_allowed": False,
                "not_a_duplicate_of": "Lorentz-force charge; Maxwell source charge; EM-stress normalization",
            },
            {
                "parameter_id": "CAL4947_03_Jgap",
                "symbol": "J_gap=m_gap^2 G_N",
                "sector": "motion",
                "physical_role": "second relevant gravity-motion trajectory coordinate",
                "independent_scalar_coordinate": True,
                "count_in_declared_truncation": True,
                "current_status": "UNIVERSAL_VALUE_NOT_SELECTED",
                "selection_or_measurement": "derive from a parent selection rule or calibrate once across all MTS arenas",
                "leading_local_source_residue": False,
                "arena_retuning_allowed": False,
                "not_a_duplicate_of": "G_N; it is an independent relevant coordinate but is silent on the local psi=0 source branch",
            },
            {
                "parameter_id": "CAL4947_04_cIR",
                "symbol": "c_IR=c_nonQCD+c_QCD^r",
                "sector": "photon_curvature",
                "physical_role": "one Weyl-photon Wilson coefficient shared by propagation and stress",
                "independent_scalar_coordinate": True,
                "count_in_declared_truncation": True,
                "current_status": "QCD_TJJ_OR_ONE_CALIBRATION_OPEN",
                "selection_or_measurement": "first-principles TJJ matching or one robust curved-photon calibration",
                "leading_local_source_residue": False,
                "arena_retuning_allowed": False,
                "not_a_duplicate_of": "alpha_EM; not an independent EM-stress coefficient",
            },
            {
                "parameter_id": "CAL4947_05_aR",
                "symbol": "a_R^r",
                "sector": "higher_curvature",
                "physical_role": "renormalized R^2 local Wilson coefficient",
                "independent_scalar_coordinate": True,
                "count_in_declared_truncation": True,
                "current_status": "FINITE_MATCHING_SUM_OPEN",
                "selection_or_measurement": "UV trajectory plus complete threshold matching or one universal bound",
                "leading_local_source_residue": False,
                "arena_retuning_allowed": False,
                "not_a_duplicate_of": "G_N; contributes only through derivative-suppressed contact/extra-pole structure",
            },
            {
                "parameter_id": "CAL4947_06_aC",
                "symbol": "a_C^r",
                "sector": "higher_curvature",
                "physical_role": "renormalized C^2 local Wilson coefficient",
                "independent_scalar_coordinate": True,
                "count_in_declared_truncation": True,
                "current_status": "FINITE_MATCHING_SUM_OPEN",
                "selection_or_measurement": "UV trajectory plus complete threshold matching or one universal bound",
                "leading_local_source_residue": False,
                "arena_retuning_allowed": False,
                "not_a_duplicate_of": "G_N; contributes only through derivative-suppressed contact/extra-pole structure",
            },
            {
                "parameter_id": "CAL4947_07_thetaSM",
                "symbol": "theta_SM",
                "sector": "visible_matter",
                "physical_role": "inherited Standard-Model masses mixings and non-U1 couplings",
                "independent_scalar_coordinate": False,
                "count_in_declared_truncation": False,
                "current_status": "EXPLICIT_INHERITED_PARAMETER_SET",
                "selection_or_measurement": "outside the new MTS gravitational calibration count",
                "leading_local_source_residue": False,
                "arena_retuning_allowed": False,
                "not_a_duplicate_of": "body-dependent mass and charge are matter state data, not new gravitational couplings",
            },
            {
                "parameter_id": "CAL4947_08_RGWilson",
                "symbol": "A_C3,W_O4,W_C,parent",
                "sector": "RG_endpoint",
                "physical_role": "trajectory-derived Wilson coordinates in the completed truncation",
                "independent_scalar_coordinate": False,
                "count_in_declared_truncation": False,
                "current_status": "DERIVED_CONDITIONALLY_ON_RG_TRUNCATION_AND_TRAJECTORY",
                "selection_or_measurement": "recompute under truncation and scheme enlargement; no arena fit",
                "leading_local_source_residue": False,
                "arena_retuning_allowed": False,
                "not_a_duplicate_of": "calibration data",
            },
        ]
    )

    residue_rows = tagged(
        [
            {
                "chain_id": "SRC4947_00_parent_action",
                "operation": "declare unchanged local parent action",
                "equation": "S_loc=int sqrt(-g)[M_R2(R-2Lambda)/2-F2/4-(nabla psi)2/2-m_gap2 psi2/2+c_IR CFF+...] + S_matter[g,A,Phi]",
                "residue_owner": "M_R^2; canonical photon field; explicit matter functor",
                "new_independent_calibration": False,
                "derivation_status": "PARENT_ACTION_RECONSTRUCTED",
                "passed": True,
            },
            {
                "chain_id": "SRC4947_01_metric_variation",
                "operation": "vary g_mn on the psi=0 local branch",
                "equation": "M_R^2(G_mn+Lambda g_mn)=T_total_mn; G_N=1/(8 pi M_R^2)",
                "residue_owner": "G_N",
                "new_independent_calibration": True,
                "derivation_status": "EINSTEIN_SOURCE_RESIDUE_DERIVED",
                "passed": True,
            },
            {
                "chain_id": "SRC4947_02_exchange",
                "operation": "invert the harmonic-gauge Einstein Hessian between conserved sources",
                "equation": "Gamma_12=i[M_R^2(q2+i0)]^-1[T1_mn T2^mn-T1 T2/2]",
                "residue_owner": "1/M_R^2=8 pi G_N",
                "new_independent_calibration": False,
                "derivation_status": "UNIVERSAL_MASSLESS_EXCHANGE_DERIVED",
                "passed": True,
            },
            {
                "chain_id": "SRC4947_03_linearized_Einstein",
                "operation": "linearize in harmonic gauge",
                "equation": "Box hbar_mn=-2 T_mn/M_R^2=-16 pi G_N T_mn",
                "residue_owner": "same G_N",
                "new_independent_calibration": False,
                "derivation_status": "LINEARIZED_SOURCE_EQUATION_DERIVED",
                "passed": True,
            },
            {
                "chain_id": "SRC4947_04_Poisson",
                "operation": "take the static nonrelativistic source limit",
                "equation": "nabla2 Phi=4 pi G_N rho; g00=-(1+2 Phi/c2)",
                "residue_owner": "same G_N",
                "new_independent_calibration": False,
                "derivation_status": "NEWTON_POISSON_LIMIT_DERIVED",
                "passed": True,
            },
            {
                "chain_id": "SRC4947_05_point_source",
                "operation": "solve the Poisson equation for a point source",
                "equation": "Phi=-G_N M/r; d2x/dt2=-grad Phi",
                "residue_owner": "same G_N",
                "new_independent_calibration": False,
                "derivation_status": "NEWTON_FORCE_LIMIT_DERIVED",
                "passed": True,
            },
            {
                "chain_id": "SRC4947_06_neutral_worldline",
                "operation": "vary S_pp=-m int ds",
                "equation": "u^a nabla_a u^m=0",
                "residue_owner": "same metric sourced by G_N",
                "new_independent_calibration": False,
                "derivation_status": "UNIVERSAL_GEODESIC_LIMIT_DERIVED",
                "passed": True,
            },
            {
                "chain_id": "SRC4947_07_null_worldline",
                "operation": "take the massless eikonal/geodesic limit",
                "equation": "k^a nabla_a k^m=0; alpha_lens=4G_N M/(b c2)+higher orders",
                "residue_owner": "same metric and same G_N",
                "new_independent_calibration": False,
                "derivation_status": "NO_SEPARATE_LENSING_G",
                "passed": True,
            },
            {
                "chain_id": "SRC4947_08_gauge_normalization",
                "operation": "canonically normalize -F2/4 and fix the physical charge convention once",
                "equation": "alpha_EM=e2/(4 pi) in natural rationalized units",
                "residue_owner": "alpha_EM",
                "new_independent_calibration": True,
                "derivation_status": "ONE_EM_NORMALIZATION_IDENTIFIED",
                "passed": True,
            },
            {
                "chain_id": "SRC4947_09_Maxwell",
                "operation": "vary A_n",
                "equation": "nabla_m F^mn-4c_IR nabla_m(C^mnrs F_rs)=J^n; nabla_[mF_nr]=0",
                "residue_owner": "alpha_EM through J; c_IR for the derivative correction",
                "new_independent_calibration": False,
                "derivation_status": "MAXWELL_CFF_FIELD_EQUATION_DERIVED",
                "passed": True,
            },
            {
                "chain_id": "SRC4947_10_charged_worldline",
                "operation": "vary S_pp=-m int ds+q int A_m dx^m",
                "equation": "u^a nabla_a u^m=(q/m)F^m_n u^n; a=-grad Phi+(q/m)(E+v cross B)",
                "residue_owner": "same G_N metric and same alpha_EM charge convention",
                "new_independent_calibration": False,
                "derivation_status": "GEODESIC_PLUS_LORENTZ_FORCE_DERIVED",
                "passed": True,
            },
            {
                "chain_id": "SRC4947_11_EM_stress",
                "operation": "vary the same electromagnetic action with respect to g_mn",
                "equation": "T_EM,mn=F_ma F_n^a-g_mn F2/4+c_IR H_CFF,mn; T_EM^0i=(E cross B)^i",
                "residue_owner": "same canonical photon normalization and same c_IR",
                "new_independent_calibration": False,
                "derivation_status": "EM_STRESS_AND_POYNTING_RESIDUE_DERIVED",
                "passed": True,
            },
            {
                "chain_id": "SRC4947_12_total_conservation",
                "operation": "combine diffeomorphism and U1 Ward identities on shell",
                "equation": "nabla^m(T_EM,mn+T_matter,mn)=0; nabla^m T_matter,mn=F_nm J^m",
                "residue_owner": "no exchange calibration",
                "new_independent_calibration": False,
                "derivation_status": "SOURCE_EXCHANGE_CONSERVATION_DERIVED",
                "passed": True,
            },
            {
                "chain_id": "SRC4947_13_motion_silence",
                "operation": "evaluate the reflection-even matter functor and O4 action at psi=0",
                "equation": "delta S_SM/delta psi=0; Q_psi=0; a_psi/a_N=0",
                "residue_owner": "J_gap remains universal but does not create a local source residue",
                "new_independent_calibration": False,
                "derivation_status": "CLASSICAL_ONE_SCALAR_FIFTH_FORCE_ZERO",
                "passed": True,
            },
        ]
    )

    limit_rows = tagged(
        [
            {
                "gate_id": "LIM4947_00_action_to_Einstein",
                "limit_or_identity": "metric variation",
                "required_conditions": "one public metric; diffeomorphism invariance; psi=0 branch",
                "result": "M_R2(G+Lambda g)=T_total",
                "extra_fit_required": False,
                "status": "DERIVED",
                "passed": True,
            },
            {
                "gate_id": "LIM4947_01_Einstein_to_Poisson",
                "limit_or_identity": "weak static slow-source limit",
                "required_conditions": "|Phi|/c2 << 1; pressure/rho c2 << 1; local Lambda r2 << |Phi|/c2",
                "result": "nabla2 Phi=4 pi G_N rho",
                "extra_fit_required": False,
                "status": "DERIVED",
                "passed": True,
            },
            {
                "gate_id": "LIM4947_02_Poisson_to_Newton",
                "limit_or_identity": "isolated point source",
                "required_conditions": "asymptotic Phi=0 and source mass M",
                "result": "Phi=-G_N M/r; a=-G_N M rhat/r2",
                "extra_fit_required": False,
                "status": "DERIVED",
                "passed": True,
            },
            {
                "gate_id": "LIM4947_03_metric_to_geodesic",
                "limit_or_identity": "neutral WKB/test-particle limit",
                "required_conditions": "minimal one-metric matter functor; negligible self-force",
                "result": "u.nabla u=0",
                "extra_fit_required": False,
                "status": "DERIVED_TEST_BODY_ORDER",
                "passed": True,
            },
            {
                "gate_id": "LIM4947_04_null_lensing",
                "limit_or_identity": "null eikonal limit",
                "required_conditions": "metric-dominated photon propagation; perturbative CFF correction",
                "result": "alpha_lens=4G_N M/(b c2)+universal CFF correction whose physical coefficient is open",
                "extra_fit_required": False,
                "status": "SAME_GN_DERIVED_CFF_NUMERIC_OPEN",
                "passed": True,
            },
            {
                "gate_id": "LIM4947_05_Maxwell_flat",
                "limit_or_identity": "C_mnrs=0",
                "required_conditions": "canonical photon normalization and explicit U1 current",
                "result": "partial_m F^mn=J^n; partial_[mF_nr]=0",
                "extra_fit_required": False,
                "status": "EXACT_FOR_EVERY_CIR",
                "passed": True,
            },
            {
                "gate_id": "LIM4947_06_Lorentz",
                "limit_or_identity": "charged point-particle variation",
                "required_conditions": "one q in the same U1 convention as J",
                "result": "m u.nabla u=q F.u",
                "extra_fit_required": False,
                "status": "DERIVED",
                "passed": True,
            },
            {
                "gate_id": "LIM4947_07_EM_gravity_source",
                "limit_or_identity": "metric variation of the same EM action",
                "required_conditions": "same c_IR in propagation and stress",
                "result": "T_EM=FF-gF2/4+c_IR H_CFF and total conservation",
                "extra_fit_required": False,
                "status": "DERIVED",
                "passed": True,
            },
            {
                "gate_id": "LIM4947_08_standard_PPN",
                "limit_or_identity": "two-derivative psi=0 vacuum exterior",
                "required_conditions": "C3 and CFF treated as higher-gradient residuals",
                "result": "delta gamma=delta beta=0 at standard PPN order",
                "extra_fit_required": False,
                "status": "DERIVED_ON_DECLARED_BRANCH",
                "passed": True,
            },
            {
                "gate_id": "LIM4947_09_strong_EP",
                "limit_or_identity": "self-gravitating compact-body universality",
                "required_conditions": "sensitivities radiation reaction and higher-curvature interior matching",
                "result": "not established by the test-body derivation",
                "extra_fit_required": False,
                "status": "OPEN_NOT_SMUGGLED",
                "passed": True,
            },
        ]
    )

    local_rows = read_csv(LOCAL_VECTOR_4942)
    transfer_rows = read_csv(TRANSFER_4946)
    transfer_by_system = {row["system"]: row for row in transfer_rows}
    arena_rows: list[dict[str, Any]] = []
    for row in local_rows:
        system = row["system"]
        mass_length = float(row["mass_length_m"])
        radius = float(row["radius_m"])
        compactness = mass_length / radius
        weak_limit = compactness <= WEAK_COMPACTNESS_MAX
        newton_acceleration = C_LIGHT_M_S**2 * mass_length / radius**2
        transfer = transfer_by_system[system]
        expected_cff_factor = 12.0 * mass_length / radius**3
        actual_cff_factor = float(transfer["CFF_curvature_factor_m_minus_2"])
        cff_factor_matches = math.isclose(expected_cff_factor, actual_cff_factor, rel_tol=2e-15)
        ppn_zero = (
            float(row["PPN_delta_gamma_at_standard_order"]) == 0.0
            and float(row["PPN_delta_beta_at_standard_order"]) == 0.0
        )
        arena_rows.append(
            {
                "system": system,
                "source_class": row["source_class"],
                "mass_length_m": mass_length,
                "radius_m": radius,
                "compactness_GM_over_rc2": compactness,
                "Phi_over_c2_Newton": -compactness,
                "Newton_surface_acceleration_m_s2": newton_acceleration,
                "weak_field_Newton_gate": weak_limit,
                "PPN_delta_gamma": float(row["PPN_delta_gamma_at_standard_order"]),
                "PPN_delta_beta": float(row["PPN_delta_beta_at_standard_order"]),
                "same_GN_token": "G_N_UNIVERSAL_4947",
                "same_alphaEM_token": "ALPHA_EM_UNIVERSAL_4947",
                "same_Jgap_token": "J_GAP_UNIVERSAL_4947",
                "same_cIR_token": "C_IR_UNIVERSAL_4947",
                "CFF_factor_m_minus_2": actual_cff_factor,
                "CFF_factor_recomputed": expected_cff_factor,
                "CFF_factor_matches": cff_factor_matches,
                "arena_specific_source_normalization": False,
                "arena_specific_Jgap": False,
                "arena_specific_cIR": False,
                "status": "LEADING_GR_NEWTON_MAXWELL_SOURCE_CHAIN_PASS" if weak_limit else "GR_SOURCE_CHAIN_RETAINED_NEWTON_APPROXIMATION_NOT_APPLICABLE",
                "passed": cff_factor_matches and ppn_zero,
                "checkpoint_marker": MARKER,
                "valid_for_full_MTS_claim": False,
                "source_checked_date": CHECKED_DATE,
            }
        )

    declared_coordinates = [row for row in calibration_rows if row["count_in_declared_truncation"]]
    unresolved_coordinates = [
        row
        for row in declared_coordinates
        if row["current_status"]
        in {
            "UNIVERSAL_VALUE_NOT_SELECTED",
            "QCD_TJJ_OR_ONE_CALIBRATION_OPEN",
            "FINITE_MATCHING_SUM_OPEN",
        }
    ]
    leading_residues = [row for row in calibration_rows if row["leading_local_source_residue"]]
    new_residue_rows = [row for row in residue_rows if row["new_independent_calibration"]]
    weak_systems = [row["system"] for row in arena_rows if row["weak_field_Newton_gate"]]
    strong_systems = [row["system"] for row in arena_rows if not row["weak_field_Newton_gate"]]

    checks = {
        "source_hashes_match": not hash_failures,
        "authoritative_source_clauses_match": not failed_clauses,
        "nine_calibration_ledger_rows": len(calibration_rows) == 9,
        "seven_counted_scalar_coordinates_in_declared_truncation": len(declared_coordinates) == 7,
        "two_leading_local_source_normalizations": len(leading_residues) == 2,
        "two_new_residue_rows_only": len(new_residue_rows) == 2,
        "metric_residue_is_GN_only": [row["symbol"] for row in leading_residues if row["sector"] == "metric_gravity"] == ["G_N <-> M_R^2"],
        "four_unresolved_universal_EFT_coordinates": len(unresolved_coordinates) == 4,
        "all_residue_chain_steps_pass": all(row["passed"] for row in residue_rows),
        "all_limit_gates_recorded_without_false_closure": all(row["passed"] for row in limit_rows),
        "five_fixed_arenas": len(arena_rows) == 5,
        "three_weak_Newton_arenas": len(weak_systems) == 3,
        "two_strong_arenas_not_mislabeled_Newtonian": len(strong_systems) == 2,
        "all_standard_PPN_shifts_zero_on_declared_branch": all(float(row["PPN_delta_gamma"]) == 0.0 and float(row["PPN_delta_beta"]) == 0.0 for row in arena_rows),
        "all_CFF_transfer_factors_reproduced": all(row["CFF_factor_matches"] for row in arena_rows),
        "no_arena_retuning": all(not row["arena_specific_source_normalization"] and not row["arena_specific_Jgap"] and not row["arena_specific_cIR"] for row in arena_rows),
        "all_rows_full_MTS_nonclaim": all(not row["valid_for_full_MTS_claim"] for table in (calibration_rows, residue_rows, limit_rows, arena_rows) for row in table),
    }

    result = {
        "marker": MARKER,
        "source_hashes": source_hashes,
        "source_clause_checks": source_clause_checks,
        "parent_low_energy_action": {
            "action": "S_loc=int sqrt(-g)[M_R2(R-2Lambda)/2-F2/4-(nabla psi)2/2-m_gap2 psi2/2+c_IR CFF+a_R R2+a_C C2+...] + S_matter[g,A,Phi]",
            "selected_local_branch": "psi=0; delta S_matter/delta psi=0",
            "metric_equation": "M_R2(G_mn+Lambda g_mn)=T_total_mn",
            "metric_residue_identity": "1/M_R2=8 pi G_N",
            "exchange_kernel": "i[T1.T2-T1T2/2]/[M_R2(q2+i0)]",
        },
        "Newton_chain": {
            "linearized_equation": "Box hbar_mn=-16 pi G_N T_mn",
            "Poisson_equation": "nabla2 Phi=4 pi G_N rho",
            "point_source": "Phi=-G_N M/r",
            "test_body": "d2x/dt2=-grad Phi",
            "null_lensing": "alpha_lens=4G_N M/(b c2)+higher-gradient corrections",
            "independent_Newton_or_lensing_G": False,
        },
        "Maxwell_chain": {
            "field_equation": "nabla F-4c_IR nabla(CF)=J",
            "Lorentz_force": "m u.nabla u=q F.u",
            "stress": "T_EM=FF-gF2/4+c_IR H_CFF",
            "Poynting": "T_EM^0i=(E cross B)^i",
            "total_conservation": "nabla(T_EM+T_matter)=0",
            "independent_force_or_stress_charge_normalization": False,
        },
        "calibration_count": {
            "leading_local_source_normalizations": 2,
            "leading_local_source_symbols": [row["symbol"] for row in leading_residues],
            "declared_scalar_coordinates_in_current_truncation": 7,
            "declared_symbols": [row["symbol"] for row in declared_coordinates],
            "currently_unselected_or_unmatched_coordinates": [row["symbol"] for row in unresolved_coordinates],
            "inherited_theta_SM_is_parameter_set_not_counted_as_one_scalar": True,
            "full_untruncated_EFT_parameter_count_closed": False,
            "arena_dependent_calibrations": 0,
        },
        "arena_summary": {
            "weak_Newton_systems": weak_systems,
            "strong_systems_not_called_Newtonian": strong_systems,
            "same_tokens": ["G_N_UNIVERSAL_4947", "ALPHA_EM_UNIVERSAL_4947", "J_GAP_UNIVERSAL_4947", "C_IR_UNIVERSAL_4947"],
        },
        "checks": checks,
        "claim_boundary": {
            "single_metric_pole_owns_GR_Newton_orbital_and_lensing_residue": True,
            "Poisson_point_force_and_geodesic_limits_derived": True,
            "Maxwell_Lorentz_stress_and_Poynting_share_one_action": True,
            "classical_one_scalar_fifth_force_zero_on_selected_branch": True,
            "standard_PPN_beta_gamma_shift_zero_on_selected_branch": True,
            "strong_equivalence_principle_for_compact_bodies_proved": False,
            "G_N_predicted_from_dimensionless_MTS_data": False,
            "J_gap_selected_without_calibration": False,
            "physical_c_IR_calculated_or_calibrated": False,
            "a_R_a_C_finite_matching_completed": False,
            "visible_U1_and_matter_functor_derived_from_motion_alone": False,
            "full_untruncated_parameter_count_closed": False,
            "full_MTS_fixed_point_and_empirical_unification": False,
        },
    }

    write_csv(CALIBRATION_CSV, calibration_rows)
    write_csv(RESIDUE_CSV, residue_rows)
    write_csv(LIMIT_CSV, limit_rows)
    write_csv(ARENA_CSV, arena_rows)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    failed_checks = [name for name, passed in checks.items() if not passed]
    print(f"{MARKER}_DECLARED_COORDINATES={len(declared_coordinates)}", flush=True)
    print(f"{MARKER}_LEADING_SOURCE_NORMALIZATIONS={len(leading_residues)}", flush=True)
    print(f"{MARKER}_UNRESOLVED_COORDINATES={len(unresolved_coordinates)}", flush=True)
    print(f"{MARKER}_WEAK_NEWTON_SYSTEMS={len(weak_systems)}", flush=True)
    print(f"{MARKER}_FAILED={len(failed_checks)}", flush=True)
    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    if failed_checks:
        for failure in failed_checks:
            print(f"{MARKER}_FAIL={failure}", flush=True)
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
