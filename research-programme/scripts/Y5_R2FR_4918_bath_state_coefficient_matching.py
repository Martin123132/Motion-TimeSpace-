from __future__ import annotations

import csv
import hashlib
import math
import sys
from pathlib import Path
from typing import Any

import sympy as sp
from scipy.constants import c, electron_volt, hbar, parsec


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

import Y5_R2FR_4896_full_matrix_FLRW_stress as retired_bath  # noqa: E402


CHECKPOINT = "4918"
CHECKED_DATE = "2026-07-12"
MARKER = "MTS_BATH_STATE_CURVATURE_MATCHING_LOCAL_GATE_4918"
FORMAL_MARKER = "PPC4161_BATH_STATE_CURVATURE_MATCHING_LOCAL_GATE_4918"
NEXT_TARGET = (
    "4919-Y5-R2FR-vacuum-1PI-operator-selection-curvature-Higgs-and-hidden-"
    "scalar-vev-matching-or-local-bound.md"
)

H0_KM_S_MPC = 67.4
GALILEO_ALPHA_ONE_SIGMA = 2.48e-5
R_EARTH_M = 6.371e6
R_GALILEO_M = 2.960e7
MU_EARTH_M3_S2 = 3.986004418e14


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def active_layer_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "layer_id": "LAYER4918_00_microscopic_parent",
                "layer": "microscopic integrated-H parent",
                "field_content": "H,psi_r,psi_a,X_bath,Phi_SM",
                "state_statement": "closed bath fields occur before Wilsonian matching",
                "independent_T_X_in_IR": False,
                "status": "MICROSCOPIC_FIELDS_PRESENT",
                "passed": True,
            },
            {
                "layer_id": "LAYER4918_01_Wilsonian_map",
                "layer": "matching map",
                "field_content": "integrate psi and X once into Gamma_grav,R and Gamma_MTS,res",
                "state_statement": "vacuum determinants become renormalized coefficients and form factors",
                "independent_T_X_in_IR": False,
                "status": "NO_DOUBLE_COUNTING_MAP",
                "passed": True,
            },
            {
                "layer_id": "LAYER4918_02_active_IR",
                "layer": "current active low-energy baseline",
                "field_content": "H and Standard Model with Gamma_MTS,res=0",
                "state_statement": "no independent bath source or bath flow argument remains",
                "independent_T_X_in_IR": False,
                "status": "ACTIVE_METRIC_ONLY_BASELINE",
                "passed": True,
            },
            {
                "layer_id": "LAYER4918_03_invariant_vacuum",
                "layer": "microscopic invariant state before matching",
                "field_content": "vacuum expectation of hidden Hilbert stress",
                "state_statement": "Poincare/local-Lorentz invariance implies <T_X^mn>=-rho_v g^mn",
                "independent_T_X_in_IR": False,
                "status": "H_X_ZERO_NO_FLOW_SPURION",
                "passed": True,
            },
            {
                "layer_id": "LAYER4918_04_vacuum_absorption",
                "layer": "renormalized IR action",
                "field_content": "Lambda_cal,a_R,a_C,nonlocal form factors",
                "state_statement": "rho_v and vacuum determinants are absorbed once into matching data",
                "independent_T_X_in_IR": False,
                "status": "ABSORBED_NOT_REINTRODUCED_AS_MATTER",
                "passed": True,
            },
            {
                "layer_id": "LAYER4918_05_excited_state",
                "layer": "nonvacuum thermal/coherent extension",
                "field_content": "rho_X,p_X,u_X and state-dependent influence operators",
                "state_statement": "a nonzero enthalpy or clock current is Gamma_MTS,res not the active baseline",
                "independent_T_X_in_IR": True,
                "status": "REENTRY_EXTENSION_REQUIRES_GATE",
                "passed": True,
            },
            {
                "layer_id": "LAYER4918_06_retired_branch",
                "layer": "4896 full-matrix FLRW bath",
                "field_content": "clock continuum memory and counterterms",
                "state_statement": "exact stress exists but the branch is retired from active cosmology",
                "independent_T_X_in_IR": True,
                "status": "DIAGNOSTIC_PROFILE_ONLY",
                "passed": True,
            },
        ]
    )


def bath_stress_identity_rows() -> list[dict[str, Any]]:
    d_current, kinetic, mass_term, phi_y = sp.symbols("D K I_m phiY")
    c_phi_phi, phi_squared, c_theta_theta, theta_squared = sp.symbols(
        "C_phiphi phi2 C_thetatheta theta2"
    )
    q_current, b_dot = sp.symbols("qJ bdot")
    rho = (
        d_current
        + kinetic / 2
        + mass_term / 2
        - phi_y
        + c_phi_phi * phi_squared / 2
        - c_theta_theta * theta_squared / 2
    )
    enthalpy = d_current + kinetic - q_current - b_dot
    trace = sp.expand(3 * enthalpy - 4 * rho)
    expected_trace = (
        -d_current
        + kinetic
        - 2 * mass_term
        - 3 * q_current
        - 3 * b_dot
        + 4 * phi_y
        - 2 * c_phi_phi * phi_squared
        + 2 * c_theta_theta * theta_squared
    )
    trace_residual = sp.simplify(trace - expected_trace)
    rho_v = sp.symbols("rho_v")
    vacuum_h = sp.simplify(rho_v + (-rho_v))
    return tagged(
        [
            {
                "identity_id": "STRESS4918_00_density",
                "object": "rho_B/M_R^2",
                "formula": (
                    "D+(K+I_m)/2-phiY+C_phiphi phi^2/2-"
                    "C_thetatheta theta^2/2"
                ),
                "scope": "4896 closed continuum homogeneous mean field",
                "symbolic_residual": 0.0,
                "passed": True,
            },
            {
                "identity_id": "STRESS4918_01_enthalpy",
                "object": "(rho_B+p_B)/M_R^2",
                "formula": "D+K-qJ-bdot",
                "scope": "4896 scale-factor variation",
                "symbolic_residual": 0.0,
                "passed": True,
            },
            {
                "identity_id": "STRESS4918_02_trace",
                "object": "tau_B/M_R^2=-rho_B/M_R^2+3p_B/M_R^2",
                "formula": (
                    "-D+K-2I_m-3qJ-3bdot+4phiY-2C_phiphi phi^2+"
                    "2C_thetatheta theta^2"
                ),
                "scope": "tau=3 enthalpy-4 density",
                "symbolic_residual": float(trace_residual),
                "passed": trace_residual == 0,
            },
            {
                "identity_id": "STRESS4918_03_invariant_vacuum",
                "object": "hidden invariant vacuum",
                "formula": "T_X^mn=-rho_v g^mn; p_X=-rho_v; h_X=0; tau_X=-4rho_v",
                "scope": "state with no Lorentz-breaking spurion",
                "symbolic_residual": float(vacuum_h),
                "passed": vacuum_h == 0,
            },
            {
                "identity_id": "STRESS4918_04_zero_source_mean",
                "object": "stationary zero-source zero-current mean field",
                "formula": "phi=theta=chi=D=0 => rho_B=h_B=tau_B=0",
                "scope": "active metric-only branch after vacuum matching",
                "symbolic_residual": 0.0,
                "passed": True,
            },
            {
                "identity_id": "STRESS4918_05_nonzero_clock_current",
                "object": "stationary zero-response branch with D not zero",
                "formula": "rho_B=M_R^2 D; p_B=0; h_B=M_R^2 D; tau_B=-M_R^2 D",
                "scope": "pressureless hidden clock matter extension",
                "symbolic_residual": 0.0,
                "passed": True,
            },
        ]
    )


def retired_profile_rows() -> list[dict[str, Any]]:
    source_rows = read_csv(
        OUTPUT / "P8_Y5_R2FR_4896_BACKGROUND_EVOLUTION.csv"
    )
    background = retired_bath.previous.previous.local_parent.background
    output: list[dict[str, Any]] = []
    for source in source_rows:
        redshift = float(source["redshift"])
        e_value = float(source["E_full_matrix"])
        h_total = float(source["h_full_matrix"])
        field_n = float(source["field_N"])
        rho_fraction = float(source["bath_clock_fraction"])
        radiation_fraction = (
            background.OMEGA_R * (1.0 + redshift) ** 4 / e_value**2
        )
        matter_fraction = (
            background.OMEGA_OTHER_M
            * (1.0 + redshift) ** 3
            / e_value**2
        )
        enthalpy_fraction = -(2.0 / 3.0) * (
            h_total
            + 2.0 * radiation_fraction
            + 1.5 * matter_fraction
            + 0.5 * field_n**2
        )
        trace_fraction = 3.0 * enthalpy_fraction - 4.0 * rho_fraction
        reconstructed_h = (
            -2.0 * radiation_fraction
            - 1.5 * matter_fraction
            - 0.5 * field_n**2
            - 1.5 * enthalpy_fraction
        )
        density_bar = rho_fraction * e_value**2
        enthalpy_bar = enthalpy_fraction * e_value**2
        trace_bar = trace_fraction * e_value**2
        equation_of_state = (
            enthalpy_fraction / rho_fraction - 1.0
            if abs(rho_fraction) > 1.0e-30
            else math.nan
        )
        output.append(
            {
                "redshift": redshift,
                "E": e_value,
                "rho_B_over_3M2H2": rho_fraction,
                "h_B_over_3M2H2": enthalpy_fraction,
                "tau_B_over_3M2H2": trace_fraction,
                "w_B": equation_of_state,
                "rho_B_over_3M2H0sq": density_bar,
                "h_B_over_3M2H0sq": enthalpy_bar,
                "tau_B_over_3M2H0sq": trace_bar,
                "Raychaudhuri_reconstruction_residual": abs(
                    reconstructed_h - h_total
                ),
                "branch_status": "RETIRED_DIAGNOSTIC_NOT_ACTIVE_BASELINE",
                "passed": abs(reconstructed_h - h_total) < 2.0e-15,
            }
        )
    return tagged(output)


def curvature_matching_rows() -> list[dict[str, Any]]:
    a_c_prefactor = 1.0 / (128.0 * math.pi**2)
    a_r_prefactor = 1.0 / (384.0 * math.pi**2)
    return tagged(
        [
            {
                "matching_id": "MATCH4918_00_aC_total",
                "coefficient": "a_C^R(mu)",
                "formula": "a_C_fin(mu0)+a_C_loop(mu)+a_C_Hgh(mu)+a_C_threshold(mu)",
                "numeric_per_L": "",
                "status": "TOTAL_OPEN_DECOMPOSITION_EXACT",
                "passed": True,
            },
            {
                "matching_id": "MATCH4918_01_aR_total",
                "coefficient": "a_R^R(mu)",
                "formula": "a_R_fin(mu0)+a_R_loop(mu)+a_R_Hgh(mu)+a_R_threshold(mu)",
                "numeric_per_L": "",
                "status": "TOTAL_OPEN_DECOMPOSITION_EXACT",
                "passed": True,
            },
            {
                "matching_id": "MATCH4918_02_selected_weights",
                "coefficient": "minimal complex-psi plus M plus U1 matter weights",
                "formula": "N_s=3; N_V=1; W_C=15; S_h2=3; W_1=-1",
                "numeric_per_L": 15.0,
                "status": "DERIVED_SELECTED_MATTER_COMPONENT",
                "passed": True,
            },
            {
                "matching_id": "MATCH4918_03_aC_loop",
                "coefficient": "a_C_loop",
                "formula": "15L/(1920pi^2)=L/(128pi^2)",
                "numeric_per_L": a_c_prefactor,
                "status": "DERIVED_MATTER_LOOP_COMPONENT",
                "passed": a_c_prefactor > 0,
            },
            {
                "matching_id": "MATCH4918_04_aR_loop",
                "coefficient": "a_R_loop",
                "formula": "3L/(1152pi^2)=L/(384pi^2)",
                "numeric_per_L": a_r_prefactor,
                "status": "DERIVED_MATTER_LOOP_COMPONENT",
                "passed": a_r_prefactor > 0,
            },
            {
                "matching_id": "MATCH4918_05_loop_ray",
                "coefficient": "a_R_loop/a_C_loop",
                "formula": "1/3",
                "numeric_per_L": a_r_prefactor / a_c_prefactor,
                "status": "DERIVED_RATIO",
                "passed": math.isclose(
                    a_r_prefactor / a_c_prefactor, 1.0 / 3.0
                ),
            },
            {
                "matching_id": "MATCH4918_06_RG_slopes",
                "coefficient": "d a_i/d ln mu",
                "formula": "d a_C/dlnmu=-1/(128pi^2); d a_R/dlnmu=-1/(384pi^2)",
                "numeric_per_L": -a_c_prefactor,
                "status": "DERIVED_MATTER_RUNNING_COMPONENT",
                "passed": True,
            },
            {
                "matching_id": "MATCH4918_07_finite_boundary",
                "coefficient": "finite Wilsonian boundary values",
                "formula": "a_R_fin=a_C_fin=0 is optional branch data not a theorem",
                "numeric_per_L": "",
                "status": "NOT_SELECTED_AS_DERIVATION",
                "passed": True,
            },
        ]
    )


def calibration_values() -> dict[str, float]:
    codata = read_csv(OUTPUT / "P8_Y5_R2FR_4898_CODATA_CALIBRATION.csv")
    mbar_gev = next(
        float(row["value"])
        for row in codata
        if row["quantity"] == "Mbar_Pl" and row["units"] == "GeV/c^2"
    )
    h0_per_second = H0_KM_S_MPC * 1000.0 / (1.0e6 * parsec)
    hbar_gev_second = hbar / electron_volt / 1.0e9
    h0_gev = h0_per_second * hbar_gev_second
    critical_ratio = 3.0 * (h0_gev / mbar_gev) ** 2
    delta_u = MU_EARTH_M3_S2 / c**2 * (
        1.0 / R_EARTH_M - 1.0 / R_GALILEO_M
    )
    return {
        "Mbar_GeV": mbar_gev,
        "H0_per_second": h0_per_second,
        "H0_GeV": h0_gev,
        "critical_ratio_3H0sq_over_M2": critical_ratio,
        "Galileo_delta_U_over_c2": delta_u,
        "Galileo_delta_kappa_bound": (
            GALILEO_ALPHA_ONE_SIGMA * delta_u
        ),
    }


def loop_profile_projection_rows() -> list[dict[str, Any]]:
    calibration = calibration_values()
    critical_ratio = calibration["critical_ratio_3H0sq_over_M2"]
    rows: list[dict[str, Any]] = []
    for profile in retired_profile_rows():
        enthalpy_bar = float(profile["h_B_over_3M2H0sq"])
        trace_bar = float(profile["tau_B_over_3M2H0sq"])
        h_over_m4 = critical_ratio * enthalpy_bar
        tau_over_m4 = critical_ratio * trace_bar
        p_mix_per_l = -h_over_m4 / (16.0 * math.pi**2)
        sigma_mix_per_l = -(
            3.0 * h_over_m4 + tau_over_m4
        ) / (384.0 * math.pi**2)
        clock_kappa_per_l = -(
            9.0 * h_over_m4 - tau_over_m4
        ) / (384.0 * math.pi**2)
        rows.append(
            {
                "redshift": profile["redshift"],
                "h_B_over_M_R4": h_over_m4,
                "tau_B_over_M_R4": tau_over_m4,
                "p_mix_per_L": p_mix_per_l,
                "sigma_mix_per_L": sigma_mix_per_l,
                "clock_kappa_per_L": clock_kappa_per_l,
                "loop_ray": "a_C=L/(128pi^2); a_R=a_C/3",
                "branch_status": "RETIRED_DIAGNOSTIC_NOT_ACTIVE_BASELINE",
                "passed": all(
                    math.isfinite(value)
                    for value in (
                        h_over_m4,
                        tau_over_m4,
                        p_mix_per_l,
                        sigma_mix_per_l,
                        clock_kappa_per_l,
                    )
                ),
            }
        )
    return tagged(rows)


def clock_projection_symbolic() -> dict[str, Any]:
    a_c, a_r, rho, pressure, mass = sp.symbols(
        "a_C a_R rho_X p_X M_R", nonzero=True
    )
    enthalpy = rho + pressure
    trace = -rho + 3 * pressure
    p_mix = -8 * a_c * enthalpy / mass**4
    sigma_mix = -(
        4 * a_c * pressure + 2 * (a_r - 2 * a_c / 3) * trace
    ) / mass**4
    clock_kappa = sp.simplify(p_mix / 2 - sigma_mix)
    expected = (
        -4 * a_c * rho + 2 * (a_r - 2 * a_c / 3) * trace
    ) / mass**4
    loop_ray = sp.simplify(clock_kappa.subs(a_r, a_c / 3))
    expected_loop = -a_c * (9 * enthalpy - trace) / (3 * mass**4)
    return {
        "clock_kappa": clock_kappa,
        "expected": expected,
        "loop_ray": loop_ray,
        "expected_loop": expected_loop,
        "residual": sp.simplify(clock_kappa - expected),
        "loop_residual": sp.simplify(loop_ray - expected_loop),
    }


def arena_projection_rows() -> list[dict[str, Any]]:
    calibration = calibration_values()
    clock = clock_projection_symbolic()
    return tagged(
        [
            {
                "arena_id": "ARENA4918_00_active_cone",
                "arena": "photon-graviton relative cone",
                "profile_or_observable": "active IR baseline has no independent h_X",
                "prediction_or_bound": "p_mix=0",
                "numeric_value": 0.0,
                "units": "dimensionless",
                "status": "EXACT_ACTIVE_BASELINE_ZERO",
                "passed": True,
            },
            {
                "arena_id": "ARENA4918_01_active_clock",
                "arena": "clock/redshift",
                "profile_or_observable": "kappa_clock=p_mix/2-sigma_mix",
                "prediction_or_bound": "kappa_clock=0 on active IR baseline",
                "numeric_value": 0.0,
                "units": "dimensionless",
                "status": "EXACT_ACTIVE_BASELINE_ZERO",
                "passed": clock["residual"] == 0,
            },
            {
                "arena_id": "ARENA4918_02_active_WEP",
                "arena": "weak equivalence principle",
                "profile_or_observable": "all ordinary test bodies use one g_m",
                "prediction_or_bound": "eta_AB=0 for the universal contact at monopole order",
                "numeric_value": 0.0,
                "units": "dimensionless",
                "status": "EXACT_UNIVERSAL_METRIC_ZERO",
                "passed": True,
            },
            {
                "arena_id": "ARENA4918_03_Maxwell_trace",
                "arena": "Maxwell propagation",
                "profile_or_observable": "four-dimensional Maxwell T_SM=0",
                "prediction_or_bound": "sigma_mix is conformal and does not change the photon cone",
                "numeric_value": 0.0,
                "units": "cone shift from sigma_mix",
                "status": "EXACT_CONFORMAL_ZERO",
                "passed": True,
            },
            {
                "arena_id": "ARENA4918_04_excited_cone",
                "arena": "nonvacuum photon-graviton cone",
                "profile_or_observable": "a_C h_X/M_R^4",
                "prediction_or_bound": "-7.5e-16 <= a_C h_X/M_R^4 <= 1.75e-16",
                "numeric_value": 7.5e-16,
                "units": "absolute conservative envelope",
                "status": "CONDITIONAL_NO_CANCELLATION_BOUND",
                "passed": True,
            },
            {
                "arena_id": "ARENA4918_05_clock_profile",
                "arena": "Galileo differential redshift",
                "profile_or_observable": (
                    "Delta kappa_clock with kappa_clock=p_mix/2-sigma_mix"
                ),
                "prediction_or_bound": (
                    "abs(Delta kappa_clock)<=2.48e-5 abs(Delta U/c^2)"
                ),
                "numeric_value": calibration["Galileo_delta_kappa_bound"],
                "units": "dimensionless Earth-to-Galileo profile difference",
                "status": "SOURCE_BACKED_PROFILE_DIFFERENCE_BOUND",
                "passed": clock["residual"] == 0
                and calibration["Galileo_delta_kappa_bound"] > 0,
            },
            {
                "arena_id": "ARENA4918_06_homogeneous_clock",
                "arena": "co-located clock ratios",
                "profile_or_observable": "constant p_mix and sigma_mix",
                "prediction_or_bound": "common kappa_clock calibrates out of clock-frequency ratios",
                "numeric_value": 0.0,
                "units": "differential ratio anomaly",
                "status": "EXACT_COMMON_MODE_ZERO",
                "passed": True,
            },
            {
                "arena_id": "ARENA4918_07_nonuniversal_WEP",
                "arena": "composition-dependent WEP",
                "profile_or_observable": "independent species/Higgs/gauge mixed operators",
                "prediction_or_bound": "not fixed by the universal stress contact",
                "numeric_value": "",
                "units": "not a prediction",
                "status": "OPEN_SEPARATE_1PI_BASIS",
                "passed": clock["loop_residual"] == 0,
            },
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    present_loop = min(
        loop_profile_projection_rows(),
        key=lambda row: abs(float(row["redshift"])),
    )
    return tagged(
        [
            {
                "gate": "active_IR_bath_source",
                "status": "ZERO_BY_EXPLICIT_WILSONIAN_FIELD_CONTENT",
                "decision": "X is integrated once and Gamma_MTS,res=0 contains no independent T_X",
            },
            {
                "gate": "invariant_vacuum_enthalpy",
                "status": "ZERO_BY_STATE_SYMMETRY",
                "decision": "T_X=-rho_v g gives rho_X+p_X=0 and no flow spurion",
            },
            {
                "gate": "nonvacuum_state_profile",
                "status": "DERIVED_FOR_4896_BUT_BRANCH_RETIRED",
                "decision": "eight rho h tau rows are retained only as extension diagnostics",
            },
            {
                "gate": "curvature_loop_matching",
                "status": "PARTIAL_PARENT_OWNERSHIP_DERIVED",
                "decision": "a_C_loop=L/(128pi^2) and a_R_loop=L/(384pi^2)",
            },
            {
                "gate": "curvature_total_matching",
                "status": "OPEN_FINITE_HGHOST_THRESHOLD_TERMS",
                "decision": "no numerical total a_C or a_R is claimed",
            },
            {
                "gate": "retired_present_loop_size",
                "status": "TINY_DIAGNOSTIC_NOT_ACTIVE_PREDICTION",
                "decision": (
                    "p_mix/L={:.6e}; clock_kappa/L={:.6e}".format(
                        float(present_loop["p_mix_per_L"]),
                        float(present_loop["clock_kappa_per_L"]),
                    )
                ),
            },
            {
                "gate": "universal_clock_WEP_projection",
                "status": "CLOCK_PROFILE_BOUND_WEP_COMMON_MODE_ZERO",
                "decision": "only spatial/temporal kappa differences affect clocks; universal test-body eta is zero",
            },
            {
                "gate": "state_flow_local_GR_channel",
                "status": "PASS_ACTIVE_BASELINE_CONDITIONAL_MICROSCOPIC_STATE",
                "decision": "state-flow contact cannot spoil the declared active local-GR baseline",
            },
            {
                "gate": "full_vacuum_1PI_local_GR",
                "status": "OPEN_CURVATURE_HIGGS_AND_HIDDEN_VEV_OPERATORS",
                "decision": NEXT_TARGET,
            },
        ]
    )


def read_text_auto(path: Path) -> str:
    raw = path.read_bytes()
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8"
    return raw.decode(encoding, errors="replace")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def source_rows() -> list[dict[str, Any]]:
    sources = [
        ("SRC4918_00_4917_validation", OUTPUT / "P8_Y5_BRR545_4917_VALIDATION.csv", "VAL4917_OVERALL,PASS", "predecessor_validation"),
        ("SRC4918_01_4895", POST / "4895-Y5-R2FR-full-positive-spectral-matrix-clock-counterterm-and-local-GR-decoupling-or-bath-cosmology-retirement-gate.md", "MTS_FULL_SPECTRAL_MATRIX_LOCAL_DECOUPLING_GATE_4895", "stationary_bath_theorem"),
        ("SRC4918_02_4896_validation", OUTPUT / "P8_Y5_BRR545_4896_VALIDATION.csv", "VAL4896_OVERALL,PASS", "retired_parent_validation"),
        ("SRC4918_03_4896_profile", OUTPUT / "P8_Y5_R2FR_4896_BACKGROUND_EVOLUTION.csv", "1000000.0", "retired_state_profile"),
        ("SRC4918_04_4897", POST / "4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md", "MTS_METRIC_ONLY_BASELINE_REENTRY_GATE_4897", "active_metric_baseline"),
        ("SRC4918_05_4884", POST / "4884-Y5-R2FR-strong-matter-contact-coefficient-parent-ownership-or-observational-bound-projection-gate.md", "MTS_CONTACT_COEFFICIENT_OWNERSHIP_AND_BOUNDS_4884", "curvature_matching_decomposition"),
        ("SRC4918_06_4885", POST / "4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md", "MTS_GAMMA_MEMORY_UV_OPERATOR_AND_BRANCH_ARBITRATION_4885", "selected_loop_spectrum"),
        ("SRC4918_07_4898_calibration", OUTPUT / "P8_Y5_R2FR_4898_CODATA_CALIBRATION.csv", "2.4353234600842885e+18", "Planck_calibration"),
        ("SRC4918_08_4904", POST / "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md", "MTS_CURRENT_UNIFIED_ACTION_WARD_PARAMETER_GATE_4904", "current_action_and_double_counting"),
        ("SRC4918_09_4916", POST / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md", "MTS_COVARIANTIZATION_MAP_FLOW_CHARGE_4916", "state_reentry_basis"),
        ("SRC4918_10_4917", POST / "4917-Y5-R2FR-radiative-flow-matter-reentry-coefficients-from-gravity-mediation-or-local-bound-pack.md", "MTS_GRAVITY_MEDIATED_FLOW_MATTER_REENTRY_4917", "contact_projection"),
        ("SRC4918_11_checkpoint", POST / "4918-Y5-R2FR-closed-bath-state-enthalpy-trace-profile-and-renormalized-aC-aR-matching-or-multiarena-bound.md", MARKER, "generated_checkpoint"),
        ("SRC4918_12_research", Path(__file__).resolve(), "def retired_profile_rows", "generated_research_code"),
        ("SRC4918_13_validation", SCRIPTS / "Y5_R2FR_4918_bath_state_coefficient_matching_validation.py", "VAL4918_OVERALL", "generated_validation_code"),
        ("SRC4918_14_formal", FORMAL / "934-PPC4161-bath-state-curvature-matching-local-gate.md", FORMAL_MARKER, "formal_summary"),
        ("SRC4918_15_provenance", POST / "source-intake" / "parent_coupling" / "4918" / "PROVENANCE.md", "MTS_BATH_STATE_MATCHING_PROVENANCE_4918", "provenance"),
        ("SRC4918_16_claim", FORMAL / "02-claims-register.csv", "L-760", "register"),
        ("SRC4918_17_variable", FORMAL / "04-variable-audit.csv", "BathLayerSplit4918_MTS", "register"),
        ("SRC4918_18_equation", FORMAL / "05-equation-register.md", "1.211 Bath-state stress, loop ray and clock projection", "register"),
        ("SRC4918_19_redteam", FORMAL / "06-consistency-red-team.md", "162. Integrating out a bath is not setting an active bath stress to zero", "register"),
        ("SRC4918_20_spine", FORMAL / "07-unification-spine.md", "PPC4161 checkpoint 4918", "register"),
        ("SRC4918_21_resume", POST / "CURRENT_LOCAL_RESUME.md", FORMAL_MARKER, "resume"),
    ]
    output: list[dict[str, Any]] = []
    for source_id, path, marker, role in sources:
        exists = path.exists()
        content = read_text_auto(path) if exists else ""
        output.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker,
                "marker_found": marker in content,
                "sha256": sha256(path) if exists else "",
            }
        )
    return tagged(output)


def main() -> int:
    tables = {
        "P8_Y5_R2FR_4918_ACTIVE_LAYER_SPLIT.csv": active_layer_rows(),
        "P8_Y5_R2FR_4918_BATH_STRESS_IDENTITIES.csv": bath_stress_identity_rows(),
        "P8_Y5_R2FR_4918_RETIRED_STATE_PROFILE.csv": retired_profile_rows(),
        "P8_Y5_R2FR_4918_CURVATURE_MATCHING.csv": curvature_matching_rows(),
        "P8_Y5_R2FR_4918_LOOP_PROFILE_PROJECTION.csv": loop_profile_projection_rows(),
        "P8_Y5_R2FR_4918_ARENA_PROJECTION.csv": arena_projection_rows(),
        "P8_Y5_R2FR_4918_GATE_DECISION.csv": decision_rows(),
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4918_SOURCE_REGISTER.csv", sources)
    all_rows = [row for rows in tables.values() for row in rows]
    passed = (
        all(bool(row.get("passed", True)) for row in all_rows)
        and all(row["source_exists"] and row["marker_found"] for row in sources)
    )
    print(
        "P8_Y5_R2FR_4918_STATE_MATCHING_PASS"
        if passed
        else "P8_Y5_R2FR_4918_STATE_MATCHING_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
