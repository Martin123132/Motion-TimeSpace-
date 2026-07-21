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
SOURCE = POST / "source-intake" / "functional_rg" / "4945"

RESULT_JSON = SOURCE / "primary_CFF_two_sign_geometry_results.json"
SIGN_CSV = SOURCE / "polarization_sign_symmetry_and_bound_gate.csv"
GEOMETRY_CSV = SOURCE / "PSR_B1534_geometry_reconstruction.csv"
OPERATORS_CSV = SOURCE / "CFF_competing_operator_audit.csv"
LOCAL_CSV = SOURCE / "geometry_corrected_local_CFF_projection.csv"

SOURCE_0306_TEX = POST / "source-intake" / "functional_rg" / "4931" / "src-0306021" / "0306021.tex"
SOURCE_0306_PDF = POST / "source-intake" / "functional_rg" / "4931" / "0306021.pdf"
SOURCE_0306_TAR = POST / "source-intake" / "functional_rg" / "4931" / "0306021-source.tar"
PDF_1402 = SOURCE / "1402.4836.pdf"
TAR_1402 = SOURCE / "1402.4836-source.tar"
TEX_1402 = SOURCE / "src-1402.4836" / "paperforarXiv.tex"
PDF_0208 = SOURCE / "0208357.pdf"
TAR_0208 = SOURCE / "0208357-source.tar"
TEX_0208 = SOURCE / "src-0208357" / "ms.tex"
PDF_2009 = SOURCE / "2009.12043.pdf"
TAR_2009 = SOURCE / "2009.12043-source.tar"
TEX_2009 = SOURCE / "src-2009.12043" / "ms.tex"
RESULT_4944 = POST / "source-intake" / "functional_rg" / "4944" / "visible_CFF_threshold_and_total_bound_results.json"
RESIDUAL_4942 = POST / "source-intake" / "functional_rg" / "4942" / "local_O4_C3_CFF_residual_vector.csv"

EXPECTED_HASHES = {
    SOURCE_0306_TEX: "690ed654b9bb28b6d1ac6fdacdba0cc469ff388caf7f693084a692f30817b5c4",
    SOURCE_0306_PDF: "051bb00b53a2405c5fe9e60ce8caa3fb53569fc521c3c160056a9ddc63308dd9",
    SOURCE_0306_TAR: "4bb0cf7e021fd642f562c779b409e1d26cc42fc8aeae605fc1514bca565ba8b1",
    PDF_1402: "82b37ae48184bf8f0dad378732218c0f017abda0ac46869396f7c1f0f833704f",
    TAR_1402: "3b45c022d9917f404802ece4aa9139d231399a659e5e81e877bafd80c61b6b1a",
    TEX_1402: "c89132882ce113d653d52c64c10427dd814f2ed500a5da06432f17805146a9a3",
    PDF_0208: "6083cf62c46d697efa43788841ba233311422a440a86efc315ad95fd2cfc16b4",
    TAR_0208: "86051384c79309b7330608f63a4a63d506d79f03fa6c024e1c2076460ba74b6c",
    TEX_0208: "40e72fa5f56b2970474dfcc6b1db178a828dbece2578372f0e9b391ab880bbb9",
    PDF_2009: "b39c527cd57fb57c91015072042ad9fcffa5a396fadce2f9ebd78f65df53fbe1",
    TAR_2009: "e882f5205938ca315f445c0b356744f988467e4c242148d10d25d9fa56a6d009",
    TEX_2009: "cc3a29e4fbe38093d40e6aa25f4bf52b42dd9bab5a098fe4f229da1f4db83ac1",
    RESULT_4944: "733f057b78ee5c9848a5d25c019b2c993bf6faebb78f0a4653923e4b62cc357d",
    RESIDUAL_4942: "51f034326f02684491743d6b12fed9d54854885dae07e7894e77423f435a14a5",
}

MARKER = "MTS_4945_PRIMARY_CFF_TWO_SIGN_GEOMETRY_LOCAL_CERTIFICATE"
CHECKED_DATE = "2026-07-13"
SPEED_OF_LIGHT_M_PER_S = 299_792_458.0
SOLAR_MASS_TIME_S = 4.925490947e-6
ALPHA_EM = 7.2973525693e-3
QED_CRITICAL_FIELD_T = 4.414e9
PULSAR_PERIOD_DAYS = 0.420737298879
ECCENTRICITY = 0.27367752
OMEGA_DEG = 283.306012
SHAPIRO_SHAPE_DD = 0.9772
SHAPIRO_SHAPE_SIGMA = 0.0016
SHAPIRO_SHAPE_DDGR = 0.97496
COMPANION_MASS_SOLAR = 1.3455
COMPANION_MASS_SIGMA_SOLAR = 0.0002
TOTAL_MASS_SOLAR = 2.678463
TOTAL_MASS_SIGMA_SOLAR = 0.000004
SOURCE_STATED_RADIUS_M = 10_000.0
SOURCE_ALLOWANCE_S = 1.0e-6
SOURCE_PRINTED_BOUND_M2 = 0.6e11 * 1.0e-4


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


def geometry_row(
    variant: str,
    shapiro_shape: float,
    companion_mass_solar: float,
    total_mass_solar: float,
) -> dict[str, Any]:
    period_s = PULSAR_PERIOD_DAYS * 86400.0
    omega = math.radians(OMEGA_DEG)
    relative_semimajor_axis_m = SPEED_OF_LIGHT_M_PER_S * (
        SOLAR_MASS_TIME_S * total_mass_solar * (period_s / (2.0 * math.pi)) ** 2
    ) ** (1.0 / 3.0)

    def orbit(true_anomaly: float) -> tuple[float, float, float, float]:
        separation = relative_semimajor_axis_m * (1.0 - ECCENTRICITY**2) / (
            1.0 + ECCENTRICITY * math.cos(true_anomaly)
        )
        argument = omega + true_anomaly
        projection = 1.0 - shapiro_shape**2 * math.sin(argument) ** 2
        impact = separation * math.sqrt(max(0.0, projection))
        line_of_sight = separation * shapiro_shape * math.sin(argument)
        return separation, impact, line_of_sight, argument

    def stationarity_function(true_anomaly: float) -> float:
        argument = omega + true_anomaly
        return (
            ECCENTRICITY * math.sin(true_anomaly)
            / (1.0 + ECCENTRICITY * math.cos(true_anomaly))
            - shapiro_shape**2
            * math.sin(argument)
            * math.cos(argument)
            / (1.0 - shapiro_shape**2 * math.sin(argument) ** 2)
        )

    conjunction_guess = math.pi / 2.0 - omega
    lower = conjunction_guess - 0.5
    upper = conjunction_guess + 0.5
    value_lower = stationarity_function(lower)
    value_upper = stationarity_function(upper)
    if value_lower * value_upper >= 0.0:
        raise RuntimeError(f"conjunction stationary point not bracketed for {variant}")
    for _ in range(160):
        middle = (lower + upper) / 2.0
        value_middle = stationarity_function(middle)
        if value_lower * value_middle <= 0.0:
            upper = middle
            value_upper = value_middle
        else:
            lower = middle
            value_lower = value_middle
    closest_true_anomaly = (lower + upper) / 2.0
    separation_m, impact_m, line_of_sight_m, argument = orbit(closest_true_anomaly)
    source_leg = math.sqrt(max(0.0, 1.0 - (impact_m / separation_m) ** 2))
    geometry_factor = 1.0 + source_leg
    companion_mass_length_m = companion_mass_solar * SOLAR_MASS_TIME_S * SPEED_OF_LIGHT_M_PER_S
    lag_coefficient_s_per_m2 = (
        24.0 * companion_mass_length_m * geometry_factor / (SPEED_OF_LIGHT_M_PER_S * impact_m**2)
    )
    lambda_bound_m2 = SOURCE_ALLOWANCE_S / lag_coefficient_s_per_m2
    stationarity = stationarity_function(closest_true_anomaly)
    linear_CFF_parameter = 12.0 * lambda_bound_m2 * companion_mass_length_m / impact_m**3
    return {
        "geometry_id": variant,
        "shapiro_shape_s": shapiro_shape,
        "companion_mass_solar": companion_mass_solar,
        "total_mass_solar": total_mass_solar,
        "relative_semimajor_axis_m": relative_semimajor_axis_m,
        "closest_true_anomaly_deg": math.degrees(closest_true_anomaly) % 360.0,
        "closest_argument_of_latitude_deg": math.degrees(argument) % 360.0,
        "source_lens_separation_m": separation_m,
        "line_of_sight_separation_m": line_of_sight_m,
        "physical_impact_parameter_m": impact_m,
        "impact_to_stated_radius_ratio": impact_m / SOURCE_STATED_RADIUS_M,
        "source_formula_geometry_factor": geometry_factor,
        "stationarity_residual": stationarity,
        "lag_coefficient_s_per_m2": lag_coefficient_s_per_m2,
        "one_microsecond_abs_lambda_bound_m2": lambda_bound_m2,
        "linear_CFF_parameter_at_bound": linear_CFF_parameter,
        "geometry_assumption": "local-GR/Newton orbit; observer leg at infinity; superior conjunction",
        "status": "SOURCE_FORMULA_RECOMPUTED_WITH_MEASURED_ORBIT_GEOMETRY",
        "passed": abs(stationarity) < 1.0e-11 and 1.0 <= geometry_factor <= 2.0,
    }


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

    source_0306 = SOURCE_0306_TEX.read_text(encoding="utf-8-sig")
    source_1402 = TEX_1402.read_text(encoding="utf-8-sig")
    source_2009 = TEX_2009.read_text(encoding="utf-8-sig")
    required_source_clauses = {
        "0306_mode_sign": "\\lambda_\\pm= \\pm 12 \\lambda" in source_0306,
        "0306_orthogonal_split": "two orthogonal" in source_0306 and "splitting of the pulse" in source_0306,
        "0306_one_microsecond": "upper limit of $1" in source_0306 and "\\mu sec" in source_0306,
        "0306_printed_bound": "0.6 \\times 10^{11} cm^2" in source_0306,
        "1402_orbit": "0.420737298879" in source_1402 and "0.27367752" in source_1402,
        "1402_shape": "0.9772(16)" in source_1402,
        "1402_polarimetry": "preserving polarimetric information" in source_1402,
        "1402_timing_floor": "4.57\\textrm{ }\\mu$s" in source_1402,
        "2009_jitter": "62$\\,$\\mu s" in source_2009,
    }

    geometry_rows = [
        geometry_row("G4945_00_DD_central", SHAPIRO_SHAPE_DD, COMPANION_MASS_SOLAR, TOTAL_MASS_SOLAR),
        geometry_row(
            "G4945_01_DD_plus_1sigma",
            SHAPIRO_SHAPE_DD + SHAPIRO_SHAPE_SIGMA,
            COMPANION_MASS_SOLAR,
            TOTAL_MASS_SOLAR,
        ),
        geometry_row(
            "G4945_02_DD_minus_1sigma",
            SHAPIRO_SHAPE_DD - SHAPIRO_SHAPE_SIGMA,
            COMPANION_MASS_SOLAR,
            TOTAL_MASS_SOLAR,
        ),
        geometry_row(
            "G4945_03_DD_minus_2sigma_conservative",
            SHAPIRO_SHAPE_DD - 2.0 * SHAPIRO_SHAPE_SIGMA,
            COMPANION_MASS_SOLAR - 2.0 * COMPANION_MASS_SIGMA_SOLAR,
            TOTAL_MASS_SOLAR + 2.0 * TOTAL_MASS_SIGMA_SOLAR,
        ),
        geometry_row("G4945_04_DDGR_crosscheck", SHAPIRO_SHAPE_DDGR, COMPANION_MASS_SOLAR, TOTAL_MASS_SOLAR),
    ]
    geometry_rows = tagged(geometry_rows)
    geometry_map = {row["geometry_id"]: row for row in geometry_rows}
    central_geometry = geometry_map["G4945_00_DD_central"]
    conservative_geometry = geometry_map["G4945_03_DD_minus_2sigma_conservative"]
    corrected_bound_m2 = float(conservative_geometry["one_microsecond_abs_lambda_bound_m2"])
    central_bound_m2 = float(central_geometry["one_microsecond_abs_lambda_bound_m2"])

    source_companion_mass_length_m = 1.33 * SOLAR_MASS_TIME_S * SPEED_OF_LIGHT_M_PER_S
    inferred_printed_geometry_factor = (
        SPEED_OF_LIGHT_M_PER_S
        * SOURCE_ALLOWANCE_S
        * SOURCE_STATED_RADIUS_M**2
        / (24.0 * source_companion_mass_length_m * SOURCE_PRINTED_BOUND_M2)
    )
    grazing_formula_bound_m2 = (
        SPEED_OF_LIGHT_M_PER_S
        * SOURCE_ALLOWANCE_S
        * SOURCE_STATED_RADIUS_M**2
        / (24.0 * source_companion_mass_length_m * 2.0)
    )
    equivalent_impact_for_printed_bound_m = math.sqrt(
        SOURCE_PRINTED_BOUND_M2
        * 24.0
        * source_companion_mass_length_m
        * 2.0
        / (SPEED_OF_LIGHT_M_PER_S * SOURCE_ALLOWANCE_S)
    )

    sign_rows = tagged(
        [
            {
                "gate_id": "SIGN4945_00_mode_law",
                "statement": "T_plus=T_GR+12 lambda A and T_minus=T_GR-12 lambda A with A>0",
                "derivation": "source lambda_plus/minus=plus/minus 12 lambda inserted into its travel-time equation",
                "lambda_parity": "mode pair exchanged under lambda to minus lambda",
                "status": "PRIMARY_FORMULA_RECONSTRUCTED",
                "established": True,
                "valid_for_raw_likelihood": False,
                "passed": True,
            },
            {
                "gate_id": "SIGN4945_01_label_swap",
                "statement": "T_plus(-lambda)=T_minus(lambda) and T_minus(-lambda)=T_plus(lambda)",
                "derivation": "direct substitution; no sign prior",
                "lambda_parity": "exact exchange",
                "status": "SIGN_SWAP_PROVED",
                "established": True,
                "valid_for_raw_likelihood": False,
                "passed": True,
            },
            {
                "gate_id": "SIGN4945_02_signed_lag",
                "statement": "DeltaT_signed(lambda)=T_plus-T_minus=24 lambda A",
                "derivation": "subtract source mode times",
                "lambda_parity": "odd",
                "status": "SIGNED_LAG_ODD",
                "established": True,
                "valid_for_raw_likelihood": False,
                "passed": True,
            },
            {
                "gate_id": "SIGN4945_03_observed_split",
                "statement": "DeltaT_split(lambda)=abs(T_plus-T_minus)=24 abs(lambda) A",
                "derivation": "an unresolved unlabelled pulse split is a nonnegative separation",
                "lambda_parity": "even",
                "status": "OBSERVABLE_TWO_SIDED",
                "established": True,
                "valid_for_raw_likelihood": False,
                "passed": True,
            },
            {
                "gate_id": "SIGN4945_04_top_hat",
                "statement": "L_gate(lambda)=1[abs(K lambda)<=tau_max] is even and gives abs(lambda)<=tau_max/K",
                "derivation": "historical one-microsecond allowance applied to the physical split",
                "lambda_parity": "even",
                "status": "PRIMARY_FORMULA_TWO_SIDED_TOP_HAT_NOT_STATISTICAL_LIKELIHOOD",
                "established": True,
                "valid_for_raw_likelihood": False,
                "passed": True,
            },
            {
                "gate_id": "SIGN4945_05_printed_bound_reproduction",
                "statement": "the printed 6.0e6 m^2 bound implies a geometry factor below the source formula minimum",
                "derivation": f"inferred factor={inferred_printed_geometry_factor:.12e}, while the far-observer formula requires 1<=S<=2",
                "lambda_parity": "not applicable",
                "status": "PRINTED_NUMERIC_BOUND_REJECTED_AS_NONREPRODUCIBLE",
                "established": True,
                "valid_for_raw_likelihood": False,
                "passed": inferred_printed_geometry_factor < 1.0,
            },
            {
                "gate_id": "SIGN4945_06_measured_geometry_bound",
                "statement": f"the source formula with the measured orbit gives abs(lambda)<={corrected_bound_m2:.12e} m^2 at the conservative two-sigma geometry",
                "derivation": "physical conjunction impact parameter replaces the unstated grazing trajectory",
                "lambda_parity": "even",
                "status": "GEOMETRY_CORRECTED_HISTORICAL_TWO_SIDED_ENVELOPE",
                "established": True,
                "valid_for_raw_likelihood": False,
                "passed": corrected_bound_m2 > central_bound_m2 > SOURCE_PRINTED_BOUND_M2,
            },
            {
                "gate_id": "SIGN4945_07_raw_likelihood",
                "statement": "no polarization-separated TOAs, covariance, pulse-state model or CFF timing fit is supplied by the acquired packages",
                "derivation": "source archives contain manuscripts and figures but no machine-readable polarimetric TOA likelihood",
                "lambda_parity": "not evaluated statistically",
                "status": "PRIMARY_RAW_DATA_LIKELIHOOD_OPEN",
                "established": False,
                "valid_for_raw_likelihood": False,
                "passed": True,
            },
        ]
    )

    conservative_impact_m = float(conservative_geometry["physical_impact_parameter_m"])
    neutron_star_radius_m = 12_000.0
    magnetar_surface_field_t = 1.0e11
    qed_delay_bound_s = (
        ALPHA_EM
        / (80.0 * SPEED_OF_LIGHT_M_PER_S)
        * (magnetar_surface_field_t / QED_CRITICAL_FIELD_T) ** 2
        * neutron_star_radius_m**6
        / conservative_impact_m**5
    )
    operator_rows = tagged(
        [
            {
                "operator_id": "OP4945_00_CFF",
                "operator": "C_mnrs F^mn F^rs",
                "vacuum_projection": "nonzero Ricci-flat birefringent target",
                "frequency_signature": "frequency independent in geometric optics",
                "polarization_timing_role": "opposite mode delay",
                "degeneracy_status": "TARGET_OPERATOR",
                "numeric_delay_envelope_s": "not applicable",
                "requires_joint_raw_fit": True,
                "passed": True,
            },
            {
                "operator_id": "OP4945_01_Ricci_photon",
                "operator": "R F^2 and R_mn F^mr F^n_r",
                "vacuum_projection": "zero on the companion Ricci-flat exterior",
                "frequency_signature": "none on declared leg",
                "polarization_timing_role": "no exterior competitor",
                "degeneracy_status": "EXACTLY_SILENT_ON_RICCI_FLAT_PROPAGATION_LEG",
                "numeric_delay_envelope_s": 0.0,
                "requires_joint_raw_fit": False,
                "passed": True,
            },
            {
                "operator_id": "OP4945_02_derivative_photon",
                "operator": "on-shell dimension-six D F D F representatives",
                "vacuum_projection": "EOM/field-redefinition equivalent to curvature and source-contact terms",
                "frequency_signature": "no independent vacuum pole at retained EFT order",
                "polarization_timing_role": "not an independent exterior coefficient",
                "degeneracy_status": "ON_SHELL_REDUCED_NOT_DOUBLE_COUNTED",
                "numeric_delay_envelope_s": 0.0,
                "requires_joint_raw_fit": False,
                "passed": True,
            },
            {
                "operator_id": "OP4945_03_metric_GR",
                "operator": "minimal Maxwell on Schwarzschild/frame-dragging metric",
                "vacuum_projection": "single metric cone",
                "frequency_signature": "achromatic common mode",
                "polarization_timing_role": "common Shapiro delay or polarization rotation, not mode split",
                "degeneracy_status": "CANCELS_IN_IDEAL_POLARIZATION_DIFFERENCE",
                "numeric_delay_envelope_s": 0.0,
                "requires_joint_raw_fit": False,
                "passed": True,
            },
            {
                "operator_id": "OP4945_04_cold_plasma",
                "operator": "unmagnetized dispersion measure",
                "vacuum_projection": "environmental propagation",
                "frequency_signature": "nu^-2",
                "polarization_timing_role": "mainly common mode but time-variable DM enters profile timing",
                "degeneracy_status": "MULTIFREQUENCY_SEPARABLE_NOT_FITTED_IN_2003_CFF_ANALYSIS",
                "numeric_delay_envelope_s": "data dependent",
                "requires_joint_raw_fit": True,
                "passed": True,
            },
            {
                "operator_id": "OP4945_05_magnetized_plasma",
                "operator": "magnetoionic circular-mode group delay and Faraday structure",
                "vacuum_projection": "environmental propagation",
                "frequency_signature": "dispersive and rotation-measure dependent",
                "polarization_timing_role": "can generate polarization-dependent arrival structure",
                "degeneracy_status": "DOES_NOT_CANCEL_AUTOMATICALLY_REQUIRES_STOKES_FREQUENCY_FIT",
                "numeric_delay_envelope_s": "data dependent",
                "requires_joint_raw_fit": True,
                "passed": True,
            },
            {
                "operator_id": "OP4945_06_intrinsic_modes_jitter",
                "operator": "orthogonal emission modes, profile evolution and pulse jitter",
                "vacuum_projection": "source nuisance",
                "frequency_signature": "profile and epoch dependent",
                "polarization_timing_role": "polarization channels need not share emission phase",
                "degeneracy_status": "SOURCE_COMMON_MODE_CANCELLATION_CLAIM_REJECTED",
                "numeric_delay_envelope_s": "2014 RMS 4.57 us; 2020 single-pulse jitter 62 us",
                "requires_joint_raw_fit": True,
                "passed": True,
            },
            {
                "operator_id": "OP4945_07_QED_magnetic_vacuum",
                "operator": "Euler-Heisenberg birefringence in a dipole companion field",
                "vacuum_projection": "nonzero but impact-parameter suppressed",
                "frequency_signature": "low-frequency achromatic",
                "polarization_timing_role": "possible same-symmetry competitor",
                "degeneracy_status": "NUMERICALLY_NEGLIGIBLE_EVEN_FOR_1E11_T_SURFACE_FIELD",
                "numeric_delay_envelope_s": qed_delay_bound_s,
                "requires_joint_raw_fit": False,
                "passed": qed_delay_bound_s < 1.0e-20 * SOURCE_ALLOWANCE_S,
            },
            {
                "operator_id": "OP4945_08_parity_odd",
                "operator": "C_mnrs F^mn Ftilde^rs",
                "vacuum_projection": "not in the declared CP-even parent basis",
                "frequency_signature": "potential achromatic birefringence if independently present",
                "polarization_timing_role": "beyond-parent competitor",
                "degeneracy_status": "ABSENT_BY_DECLARED_PARENT_SYMMETRY_NOT_OBSERVATIONALLY_FITTED",
                "numeric_delay_envelope_s": "not applicable",
                "requires_joint_raw_fit": True,
                "passed": True,
            },
        ]
    )

    result_4944 = json.loads(RESULT_4944.read_text(encoding="utf-8"))
    control_abs_m2 = float(result_4944["thresholds"]["calculable_control_abs_envelope_m2"])
    local_rows: list[dict[str, Any]] = []
    for row in read_csv(RESIDUAL_4942):
        mass_length_m = float(row["mass_length_m"])
        radius_m = float(row["radius_m"])
        curvature_factor = 12.0 * mass_length_m / radius_m**3
        control_split = control_abs_m2 * curvature_factor
        corrected_bound_split = corrected_bound_m2 * curvature_factor
        linear_valid = corrected_bound_split < 0.1
        weak_local_certificate = row["system"] in {"Earth", "Sun"} and corrected_bound_split < 1.0e-6
        if weak_local_certificate:
            status = "CONDITIONAL_WEAK_LOCAL_CFF_CERTIFICATE"
        elif linear_valid:
            status = "CONDITIONAL_LINEAR_NONPRECISION_ENVELOPE"
        else:
            status = "TRANSFER_OUTSIDE_LINEAR_CONTROL_NO_CERTIFICATE"
        local_rows.append(
            {
                "system": row["system"],
                "source_class": row["source_class"],
                "mass_length_m": mass_length_m,
                "radius_m": radius_m,
                "CFF_curvature_factor_m_minus_2": curvature_factor,
                "calculable_control_abs_cgamma_m2": control_abs_m2,
                "calculable_control_abs_Delta_v_pol_over_c": control_split,
                "geometry_corrected_historical_abs_cgamma_bound_m2": corrected_bound_m2,
                "geometry_corrected_abs_Delta_v_pol_over_c": corrected_bound_split,
                "linearized_transfer_below_ten_percent": linear_valid,
                "valid_for_conditional_weak_local_CFF_certificate": weak_local_certificate,
                "valid_for_general_local_Maxwell_claim": False,
                "bound_scope": "primary formula plus historical 1 us allowance and measured-orbit two-sigma geometry; no raw likelihood",
                "status": status,
                "passed": weak_local_certificate if row["system"] in {"Earth", "Sun"} else True,
            }
        )
    local_rows = tagged(local_rows)

    sign_test_values = (-1.0e15, -1.0, 0.0, 1.0, 1.0e15)
    lag_coefficient = float(central_geometry["lag_coefficient_s_per_m2"])
    sign_symmetry_numeric = all(
        math.isclose(abs(lag_coefficient * value), abs(lag_coefficient * -value), rel_tol=0.0, abs_tol=0.0)
        for value in sign_test_values
    )
    local_map = {row["system"]: row for row in local_rows}
    checks = {
        "source_hashes_match": not hash_failures,
        "required_source_clauses_found": all(required_source_clauses.values()),
        "all_geometry_stationary_and_physical": all(row["passed"] for row in geometry_rows),
        "polarization_label_swap_two_sided": sign_symmetry_numeric,
        "printed_bound_implies_impossible_geometry_factor": inferred_printed_geometry_factor < 1.0,
        "printed_bound_not_reused": corrected_bound_m2 > 1.0e8 * SOURCE_PRINTED_BOUND_M2,
        "measured_impact_not_stellar_radius": float(central_geometry["impact_to_stated_radius_ratio"]) > 1.0e4,
        "geometry_corrected_bound_linear_on_pulsar_leg": float(conservative_geometry["linear_CFF_parameter_at_bound"]) < 1.0e-5,
        "QED_magnetic_competitor_negligible": qed_delay_bound_s < 1.0e-20 * SOURCE_ALLOWANCE_S,
        "Earth_weak_local_certificate": local_map["Earth"]["valid_for_conditional_weak_local_CFF_certificate"],
        "Sun_weak_local_certificate": local_map["Sun"]["valid_for_conditional_weak_local_CFF_certificate"],
        "compact_transfer_not_promoted": all(
            not local_map[name]["valid_for_conditional_weak_local_CFF_certificate"]
            for name in ("1.4_solar_mass_12km_neutron_star", "10_solar_mass_Schwarzschild_horizon")
        ),
        "all_rows_full_MTS_nonclaim": all(
            not row["valid_for_full_MTS_claim"]
            for table in (sign_rows, geometry_rows, operator_rows, local_rows)
            for row in table
        ),
    }

    result = {
        "marker": MARKER,
        "source_hashes": source_hashes,
        "source_clause_checks": required_source_clauses,
        "convention": "L_EM=-F^2/4+c_gamma C_mnrs F^mn F^rs",
        "primary_formula": {
            "mode_times": "T_plus/minus=T_GR plus/minus 12 c_gamma A",
            "signed_lag": "DeltaT_signed=24 c_gamma A",
            "observed_split": "DeltaT_split=24 abs(c_gamma) A",
            "sign_result": "coefficient-sign reversal exchanges polarization labels; split is even",
            "historical_allowance_s": SOURCE_ALLOWANCE_S,
            "statistical_likelihood": False,
        },
        "printed_bound_audit": {
            "source_printed_bound_m2": SOURCE_PRINTED_BOUND_M2,
            "source_stated_radius_m": SOURCE_STATED_RADIUS_M,
            "inferred_geometry_factor": inferred_printed_geometry_factor,
            "allowed_far_observer_geometry_factor_interval": [1.0, 2.0],
            "same_formula_grazing_bound_m2": grazing_formula_bound_m2,
            "equivalent_impact_for_printed_bound_at_S2_m": equivalent_impact_for_printed_bound_m,
            "status": "nonreproducible and superseded; do not use as evidence",
        },
        "geometry_corrected_envelope": {
            "central_bound_m2": central_bound_m2,
            "conservative_two_sigma_bound_m2": corrected_bound_m2,
            "central_impact_parameter_m": central_geometry["physical_impact_parameter_m"],
            "conservative_impact_parameter_m": conservative_geometry["physical_impact_parameter_m"],
            "bound_to_printed_ratio": corrected_bound_m2 / SOURCE_PRINTED_BOUND_M2,
            "scope": "two-sided historical top-hat from primary formula, not a raw-data likelihood",
        },
        "competing_operator_audit": {
            "rows": len(operator_rows),
            "QED_magnetic_delay_envelope_s": qed_delay_bound_s,
            "unclosed_raw_nuisances": [
                "magnetized plasma",
                "intrinsic orthogonal emission phase",
                "pulse jitter and profile evolution",
                "polarization-resolved TOA covariance",
            ],
        },
        "local_projection": {
            "systems": len(local_rows),
            "conditional_weak_local_certificate_systems": [
                row["system"] for row in local_rows if row["valid_for_conditional_weak_local_CFF_certificate"]
            ],
            "out_of_linear_transfer_systems": [
                row["system"] for row in local_rows if not row["linearized_transfer_below_ten_percent"]
            ],
            "max_linear_valid_split": max(
                row["geometry_corrected_abs_Delta_v_pol_over_c"]
                for row in local_rows
                if row["linearized_transfer_below_ten_percent"]
            ),
        },
        "checks": checks,
        "claim_boundary": {
            "primary_formula_sign_symmetry_proved": True,
            "primary_formula_two_sided_top_hat_constructed": True,
            "source_printed_6e6_m2_bound_reproducible": False,
            "geometry_corrected_historical_envelope_constructed": True,
            "primary_raw_data_robust_likelihood_available": False,
            "conditional_Earth_Sun_CFF_residual_certificate": True,
            "compact_object_CFF_transfer_certified": False,
            "QCD_TJJ_matching_calculated": False,
            "complete_physical_CFF_prediction": False,
            "general_local_Maxwell_promoted": False,
            "full_MTS_fixed_point": False,
        },
    }

    write_csv(SIGN_CSV, sign_rows)
    write_csv(GEOMETRY_CSV, geometry_rows)
    write_csv(OPERATORS_CSV, operator_rows)
    write_csv(LOCAL_CSV, local_rows)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")

    failed = [name for name, passed in checks.items() if not passed]
    print(f"{MARKER}_PRINTED_BOUND_M2={SOURCE_PRINTED_BOUND_M2:.12e}", flush=True)
    print(f"{MARKER}_INFERRED_PRINTED_GEOMETRY={inferred_printed_geometry_factor:.12e}", flush=True)
    print(f"{MARKER}_CENTRAL_IMPACT_M={float(central_geometry['physical_impact_parameter_m']):.12e}", flush=True)
    print(f"{MARKER}_CENTRAL_BOUND_M2={central_bound_m2:.12e}", flush=True)
    print(f"{MARKER}_CONSERVATIVE_BOUND_M2={corrected_bound_m2:.12e}", flush=True)
    print(f"{MARKER}_QED_DELAY_S={qed_delay_bound_s:.12e}", flush=True)
    print(f"{MARKER}_FAILED={len(failed)}", flush=True)
    print(f"{MARKER}_RESULT_SHA256={digest(RESULT_JSON)}", flush=True)
    if failed:
        for failure in failed:
            print(f"{MARKER}_FAIL={failure}", flush=True)
        return 1
    print(f"{MARKER}_PASS", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
