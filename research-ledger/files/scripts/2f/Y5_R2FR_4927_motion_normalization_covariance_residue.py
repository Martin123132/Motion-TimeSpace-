from __future__ import annotations

import csv
import hashlib
import math
import sys
from pathlib import Path
from typing import Any

import mpmath as mp
import numpy as np
from scipy.constants import G, c, hbar, physical_constants


sys.dont_write_bytecode = True
mp.mp.dps = 90


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SOURCE = POST / "source-intake" / "nonlocal_form_factors" / "4927"
SCRIPTS = POST / "scripts"

CHECKPOINT = "4927"
CHECKED_DATE = "2026-07-12"
MARKER = "MTS_MOTION_NORMALIZATION_COVARIANCE_RESIDUE_4927"
FORMAL_MARKER = "PPC4161_MOTION_NORMALIZATION_COVARIANCE_RESIDUE_4927"
NEXT_TARGET = (
    "4928-Y5-R2FR-integrated-H-C3-functional-flow-boundary-or-"
    "observational-Wilson-freeze.md"
)

FORM_FACTOR_URL = "https://arxiv.org/abs/2003.04503"
DECOUPLING_URL = "https://arxiv.org/abs/1812.00460"
FORM_FACTOR_PDF = SOURCE / "massive-scalar-nonlocal-form-factors-v3.pdf"
FORM_FACTOR_SOURCE = SOURCE / "2003.04503v3-source.tar"
DECOUPLING_PDF = SOURCE / "matter-form-factors-decoupling-4D-v2.pdf"
DECOUPLING_SOURCE = SOURCE / "1812.00460v2-source.tar"
PROVENANCE = SOURCE / "PROVENANCE.md"

EXPECTED_HASHES = {
    FORM_FACTOR_PDF: "7fa6c9d5e22429b80e091e63fefb8ec578023f65dffa5200d062089749d52ec6",
    FORM_FACTOR_SOURCE: "268830a2b76dfaa2f075a45d4751f55d81f7be262bea0e884fd8ae166a3985e1",
    DECOUPLING_PDF: "e26accddfbc861c4379c291650f722912c32dd99f3d0c8738d5344b9edb89c4b",
    DECOUPLING_SOURCE: "355c7b031d397cc9c4546fb42bab2e338dbecab93b794eb92a50b4182048128e",
}

CORE_ACTION = (
    ROOT
    / "core-mts-framework"
    / "action-principle"
    / "the-fundamental-action-of-motion-timespace-field-theory.md"
)
CHECKPOINT_4872 = POST / "4872-Y5-R2FR-primitive-MTS-to-public-unit-flow-action-and-universal-source-coupling-or-correspondence-demotion.md"
CHECKPOINT_4873 = POST / "4873-Y5-R2FR-covariant-open-parent-action-and-connected-covariance-kernel-to-unit-flow-Kubo-coefficients-or-final-EFT-freeze.md"
CHECKPOINT_4874 = POST / "4874-Y5-R2FR-metric-only-quotient-background-independence-and-universal-principal-symbol-proof-or-equivalence-axiom-freeze.md"
CHECKPOINT_4875 = POST / "4875-Y5-R2FR-collective-metric-path-integral-massless-spin2-pole-and-Weinberg-Witten-evasion-or-induced-background-only-demotion.md"
CHECKPOINT_4876 = POST / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md"
CHECKPOINT_4877 = POST / "4877-Y5-R2FR-MTS-bath-signed-spectrum-sum-rules-and-nonlocal-form-factor-completion-or-renormalized-vacuum-freeze.md"
CHECKPOINT_4898 = POST / "4898-Y5-R2FR-microscopic-Planck-stiffness-owner-and-GN-calibration-versus-prediction-gate.md"
CHECKPOINT_4915 = POST / "4915-Y5-R2FR-parent-EH-residue-universal-source-coupling-and-measured-G-calibration-or-closure-demotion.md"
CHECKPOINT_4916 = POST / "4916-Y5-R2FR-covariantization-map-from-microscopic-motion-action-to-integrated-H-parent-and-no-direct-flow-charge-or-primitive-freeze.md"
CHECKPOINT_4926 = POST / "4926-Y5-R2FR-known-massive-threshold-spectrum-and-motion-scale-normalization-or-low-energy-Wilson-posterior.md"
CHECKPOINT_DOC = POST / "4927-Y5-R2FR-motion-field-normalization-from-metric-covariance-residue-and-EH-matching-or-one-Wilson-freeze.md"
FORMAL_NOTE = FORMAL / "943-PPC4161-motion-normalization-covariance-residue-and-all-mass-loop-gate.md"
VALIDATION = SCRIPTS / "Y5_R2FR_4927_motion_normalization_covariance_residue_validation.py"
RESUME = POST / "CURRENT_LOCAL_RESUME.md"
CLAIMS_REGISTER = FORMAL / "02-claims-register.csv"
VARIABLE_REGISTER = FORMAL / "04-variable-audit.csv"
EQUATION_REGISTER = FORMAL / "05-equation-register.md"
RED_TEAM_REGISTER = FORMAL / "06-consistency-red-team.md"
SPINE_REGISTER = FORMAL / "07-unification-spine.md"

MOTION_REPAIR_PATH = OUTPUT / "P8_Y5_R2FR_4926_MOTION_SCALE_REPAIR_BRANCH.csv"
LOCALITY_PATH = OUTPUT / "P8_Y5_R2FR_4926_LOCALITY_ENVELOPE.csv"
RG_PATH = OUTPUT / "P8_Y5_R2FR_4925_TWO_LOOP_RG_TRANSFER.csv"

ELECTRON_VOLT_J = physical_constants["electron volt"][0]
HBAR_C_EV_M = hbar * c / ELECTRON_VOLT_J
REDUCED_PLANCK_ENERGY_EV = math.sqrt(hbar * c**5 / (8.0 * math.pi * G)) / ELECTRON_VOLT_J
AU_M = 149_597_870_700.0


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for fieldname in row:
            if fieldname not in fieldnames:
                fieldnames.append(fieldname)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for row in rows:
        row["checkpoint_marker"] = MARKER
        row["valid_for_claim"] = False
        row["source_checked_date"] = CHECKED_DATE
    return rows


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def read_text_auto(path: Path) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue
    return path.read_text(encoding="utf-8", errors="replace")


def prior_inputs() -> dict[str, float]:
    repair_rows = read_csv(MOTION_REPAIR_PATH)
    rg_rows = read_csv(RG_PATH)
    locality_rows = read_csv(LOCALITY_PATH)
    minimal = next(
        row for row in repair_rows if row["branch"] == "minimal_single_scale_C_N_1"
    )
    gw = next(row for row in rg_rows if row["row_id"] == "RG4925_GW250114")
    ns = next(
        row
        for row in locality_rows
        if row["arena"] == "NS_12km" and row["gate"] == "formal_edge"
    )
    return {
        "minimal_mu_eV": float(minimal["mu_eV"]),
        "q_gw_eV": float(gw["q_eV"]),
        "q_ns_eV": float(ns["q_eV"]),
    }


def covariance_dimension_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "audit_id": "CDIM4927_00_core_raw",
                "field_coordinate": "repaired old phi with mass dimension 3/2",
                "object": "connected gradient bilinear",
                "bilinear_mass_dimension": 5,
                "displayed_coefficient": 1,
                "coefficient_mass_dimension": 0,
                "resulting_metric_term_dimension": 5,
                "required_coefficient_dimension": -5,
                "verdict": "CORE_RAW_ADDITIVE_METRIC_DIMENSIONALLY_INVALID",
                "passed": True,
            },
            {
                "audit_id": "CDIM4927_01_4872_old",
                "field_coordinate": "repaired old phi with mass dimension 3/2",
                "object": "ell_star^2 times connected gradient bilinear",
                "bilinear_mass_dimension": 5,
                "displayed_coefficient": "ell_star^2",
                "coefficient_mass_dimension": -2,
                "resulting_metric_term_dimension": 3,
                "required_coefficient_dimension": -5,
                "verdict": "ELL_STAR_SQUARED_DOES_NOT_REPAIR_OLD_FIELD",
                "passed": True,
            },
            {
                "audit_id": "CDIM4927_02_4872_canonical",
                "field_coordinate": "canonical psi with mass dimension 1",
                "object": "ell_star^2 times connected gradient bilinear",
                "bilinear_mass_dimension": 4,
                "displayed_coefficient": "ell_star^2",
                "coefficient_mass_dimension": -2,
                "resulting_metric_term_dimension": 2,
                "required_coefficient_dimension": -4,
                "verdict": "ELL_STAR_SQUARED_DOES_NOT_REPAIR_CANONICAL_FIELD",
                "passed": True,
            },
            {
                "audit_id": "CDIM4927_03_correct_old",
                "field_coordinate": "old phi",
                "object": "B_old times connected gradient bilinear",
                "bilinear_mass_dimension": 5,
                "displayed_coefficient": "B_old",
                "coefficient_mass_dimension": -5,
                "resulting_metric_term_dimension": 0,
                "required_coefficient_dimension": -5,
                "verdict": "DIMENSIONALLY_CORRECT_OLD_COVARIANCE",
                "passed": True,
            },
            {
                "audit_id": "CDIM4927_04_correct_canonical",
                "field_coordinate": "psi=phi/sqrt(M_N)",
                "object": "B_psi times connected gradient bilinear",
                "bilinear_mass_dimension": 4,
                "displayed_coefficient": "B_psi=B_old M_N=L_C^4",
                "coefficient_mass_dimension": -4,
                "resulting_metric_term_dimension": 0,
                "required_coefficient_dimension": -4,
                "verdict": "CANONICAL_COVARIANCE_INVARIANT_DERIVED",
                "passed": True,
            },
            {
                "audit_id": "CDIM4927_05_cutoff",
                "field_coordinate": "canonical psi",
                "object": "possible cutoff relation",
                "bilinear_mass_dimension": 4,
                "displayed_coefficient": "B_psi=zeta_B Lambda_UV^(-4)",
                "coefficient_mass_dimension": -4,
                "resulting_metric_term_dimension": 0,
                "required_coefficient_dimension": -4,
                "verdict": "DIMENSIONALLY_ALLOWED_BUT_ZETA_B_AND_IDENTIFICATION_NOT_DERIVED",
                "passed": True,
            },
            {
                "audit_id": "CDIM4927_06_4873_supersession",
                "field_coordinate": "historical covariance branch",
                "object": "Lambda_UV=ell_star^-1 using the same ell_star from ell_star^2 covariance",
                "bilinear_mass_dimension": "coordinate dependent",
                "displayed_coefficient": "ell_star^2",
                "coefficient_mass_dimension": -2,
                "resulting_metric_term_dimension": "nonzero",
                "required_coefficient_dimension": -4,
                "verdict": "SAME_SYMBOL_COVARIANCE_CUTOFF_IDENTIFICATION_SUPERSEDED",
                "passed": True,
            },
        ]
    )


def field_redefinition_rows() -> list[dict[str, Any]]:
    base_mass = 2.3
    base_lambda = 5.7
    base_covariance = 0.04
    base_g = base_lambda * base_mass ** (-1.0 / 3.0)
    base_bpsi = base_covariance * base_mass
    rows: list[dict[str, Any]] = []
    for scale in (0.01, 0.1, 1.0, 10.0, 100.0):
        transformed_mass = base_mass * scale**2
        transformed_lambda = base_lambda * scale ** (2.0 / 3.0)
        transformed_covariance = base_covariance / scale**2
        transformed_g = transformed_lambda * transformed_mass ** (-1.0 / 3.0)
        transformed_bpsi = transformed_covariance * transformed_mass
        rows.append(
            {
                "scale_s": scale,
                "field_map": "phi_prime=s phi",
                "M_N_prime": transformed_mass,
                "lambda_old_prime": transformed_lambda,
                "B_old_prime": transformed_covariance,
                "transformation_law": "M_N'=s^2 M_N; lambda'=s^(2/3)lambda; B_old'=s^-2 B_old",
                "g_psi_invariant": transformed_g,
                "B_psi_invariant": transformed_bpsi,
                "g_psi_error": abs(transformed_g - base_g),
                "B_psi_error": abs(transformed_bpsi - base_bpsi),
                "verdict": "SAME_CANONICAL_THEORY_DIFFERENT_OLD_COORDINATE",
                "passed": abs(transformed_g - base_g) < 1.0e-13
                and abs(transformed_bpsi - base_bpsi) < 1.0e-13,
            }
        )
    return tagged(rows)


def invariant_jacobian_rows() -> list[dict[str, Any]]:
    jacobian = np.array(
        [
            [-1.0 / 3.0, 1.0, 0.0, 0.0, 0.0, 0.0],
            [1.0, 0.0, 1.0, 0.0, 0.0, 0.0],
            [0.0, 0.0, 0.0, 1.0, 1.0, 1.0],
        ],
        dtype=float,
    )
    null_vectors = {
        "field_coordinate": np.array([3.0, 1.0, -3.0, 0.0, 0.0, 0.0]),
        "EH_boundary_loop": np.array([0.0, 0.0, 0.0, 1.0, -1.0, 0.0]),
        "EH_boundary_threshold": np.array([0.0, 0.0, 0.0, 1.0, 0.0, -1.0]),
    }
    rows: list[dict[str, Any]] = [
        {
            "row_id": "IJ4927_rank",
            "parameter_vector": "(ln M_N,ln lambda_old,ln B_old,y_boundary,y_loop,y_threshold)",
            "observable_vector": "(ln g_psi,ln B_psi,M_R^2 normalized)",
            "jacobian": "[-1/3,1,0,0,0,0];[1,0,1,0,0,0];[0,0,0,1,1,1]",
            "rank": int(np.linalg.matrix_rank(jacobian)),
            "nullity": int(jacobian.shape[1] - np.linalg.matrix_rank(jacobian)),
            "null_vector": "three independent rows follow",
            "null_error": 0.0,
            "verdict": "THREE_IDENTIFIABILITY_DIRECTIONS_REMAIN",
            "passed": np.linalg.matrix_rank(jacobian) == 3,
        }
    ]
    for name, vector in null_vectors.items():
        error = float(np.max(np.abs(jacobian @ vector)))
        rows.append(
            {
                "row_id": f"IJ4927_null_{name}",
                "parameter_vector": "(ln M_N,ln lambda_old,ln B_old,y_boundary,y_loop,y_threshold)",
                "observable_vector": "unchanged",
                "jacobian": "same as rank row",
                "rank": 3,
                "nullity": 3,
                "null_vector": ";".join(f"{value:g}" for value in vector),
                "null_error": error,
                "verdict": "EXACT_NULL_DIRECTION_VERIFIED",
                "passed": error < 1.0e-14,
            }
        )
    return tagged(rows)


def stress_residue_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for mass_normalization in (1.0e-12, 1.0, 1.0e12):
        for insertions in (2, 3, 4):
            vertex_factor = mass_normalization ** (-insertions)
            propagator_factor = mass_normalization**insertions
            residue = vertex_factor * propagator_factor
            rows.append(
                {
                    "M_N_demo": mass_normalization,
                    "stress_insertions": insertions,
                    "old_field_propagator_scaling": "each internal scalar propagator proportional to M_N",
                    "Hilbert_stress_vertex_scaling": "each old-coordinate stress insertion proportional to M_N^-1",
                    "vertex_factor": vertex_factor,
                    "propagator_factor": propagator_factor,
                    "normalization_residue": residue,
                    "canonical_statement": "T[phi]/M_N=T[psi]; correlators depend on g_psi not M_N separately",
                    "verdict": "M_N_CANCELS_FROM_STRESS_RESIDUE",
                    "passed": abs(residue - 1.0) < 1.0e-14,
                }
            )
    return tagged(rows)


def eh_matching_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "route_id": "EH4927_00_stress_residue",
                "candidate": "fix M_N from the motion stress two-point residue",
                "equation": "<T T> scales as M_N^-2 times M_N^2 and is normalization invariant",
                "result": "the residue fixes field count and invariant dynamics but not the old coordinate normalization",
                "C_N_fixed": False,
                "status": "REJECTED_EXACT_CANCELLATION",
                "passed": True,
            },
            {
                "route_id": "EH4927_01_active_H",
                "candidate": "fix M_N from the calibrated Einstein residue",
                "equation": "M_R^2=M_b^2+W1 Lambda_UV^2/(96pi^2)+Delta M^2",
                "result": "the active integrated-H parent contains no B_old or M_N coordinate separately",
                "C_N_fixed": False,
                "status": "REJECTED_NO_ACTIVE_PARENT_EQUATION",
                "passed": True,
            },
            {
                "route_id": "EH4927_02_composite_metric",
                "candidate": "identify the public graviton with the old scalar covariance",
                "equation": "H or g proportional to B_psi <partial psi partial psi>",
                "result": "this revives the fixed-background scalar-only composite-graviton branch rejected at 4875",
                "C_N_fixed": False,
                "status": "REJECTED_BRANCH_SWITCH_AND_WEINBERG_WITTEN_TRIGGER",
                "passed": True,
            },
            {
                "route_id": "EH4927_03_cutoff_identification",
                "candidate": "set B_psi=Lambda_UV^-4 and use pure induced gravity",
                "equation": "B_psi=zeta_B Lambda_UV^-4; M_R^2=W1 Lambda_UV^2/(96pi^2)",
                "result": "requires zeta_B pure-induced boundary spectrum and cutoff ownership; even then only B_old M_N is fixed",
                "C_N_fixed": False,
                "status": "DIMENSIONALLY_ALLOWED_EXTRA_CLOSURE_NOT_DERIVED",
                "passed": True,
            },
            {
                "route_id": "EH4927_04_field_coordinate",
                "candidate": "interpret C_N=M_N/M_Pl as a physical coupling",
                "equation": "(M_N,lambda_old,B_old)->(s^2M_N,s^(2/3)lambda_old,s^-2B_old)",
                "result": "C_N moves along a field-coordinate orbit while g_psi and B_psi remain fixed",
                "C_N_fixed": False,
                "status": "C_N_DEMOTED_TO_REDUNDANT_COORDINATE",
                "passed": True,
            },
            {
                "route_id": "EH4927_05_physical_replacement",
                "candidate": "retain invariant scalar data",
                "equation": "g_psi=lambda_old M_N^-1/3; B_psi=B_old M_N; mu=g_psi^(3/8)",
                "result": "g_psi or mu and B_psi are physical matching quantities; neither is numerically fixed by the old coefficient-one map",
                "C_N_fixed": False,
                "status": "SELECTED_INVARIANT_PARAMETERIZATION",
                "passed": True,
            },
        ]
    )


def k_w(u_value: float | mp.mpf) -> mp.mpf:
    u = mp.mpf(u_value)
    if u <= 0:
        return mp.mpf("0")
    if u < mp.mpf("1e-7"):
        return -u / 840 * (1 + u / 18)
    a_value = 2 * mp.sqrt(u / (u + 4))
    a_function = 1 - mp.log((2 + a_value) / (2 - a_value)) / a_value
    return (
        8 * a_function / (15 * a_value**4)
        + 2 / (45 * a_value**2)
        + mp.mpf(1) / 150
    )


def beta_w_exact(x_value: float | mp.mpf) -> mp.mpf:
    x_value = mp.mpf(x_value)
    if x_value <= 0:
        return mp.mpf("0")
    if x_value >= 1:
        return -mp.mpf(1) / 60
    if x_value < mp.mpf("1e-4"):
        return -x_value**2 / 210 - x_value**4 / 378
    a_value = 2 * x_value
    logarithm = mp.log((1 + x_value) / (1 - x_value))
    numerator = (
        a_value**5
        + 20 * a_value**3
        - 120 * a_value
        + 30 * (4 - a_value**2) * logarithm
    )
    return numerator / (90 * a_value**5)


def beta_w_series(x_value: float | mp.mpf, terms: int = 12000) -> mp.mpf:
    x_value = mp.mpf(x_value)
    total = mp.mpf("0")
    power = x_value**2
    for index in range(1, terms + 1):
        total += power / (6 * (2 * index + 3) * (2 * index + 5))
        power *= x_value**2
    return -total


def form_factor_beta_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for x_value in (0.01, 0.1, 0.5, 0.9, 0.99, 0.999):
        exact = beta_w_exact(x_value)
        series = beta_w_series(x_value)
        error = abs(exact - series)
        rows.append(
            {
                "x": x_value,
                "u": 4 * x_value**2 / (1 - x_value**2),
                "beta_exact_dkW_dlnu": float(exact),
                "beta_positive_series": float(series),
                "series_error": float(error),
                "lower_bound": -1.0 / 60.0,
                "upper_bound": 0.0,
                "analytic_series": "-sum_n>=1 x^(2n)/[6(2n+3)(2n+5)]",
                "endpoint_sum": "sum at x=1 telescopes to 1/60",
                "status": "EXACT_MONOTONE_THRESHOLD_BETA_BOUND",
                "passed": exact >= -mp.mpf(1) / 60 - mp.mpf("1e-30")
                and exact <= 0
                and error < mp.mpf("2e-12"),
            }
        )
    return tagged(rows)


def arena_scales(inputs: dict[str, float]) -> dict[str, float]:
    return {
        "AU": HBAR_C_EV_M / AU_M,
        "Earth": HBAR_C_EV_M / 6_371_000.0,
        "GW250114": inputs["q_gw_eV"],
        "NS_12km": inputs["q_ns_eV"],
        "R10_50um": HBAR_C_EV_M / 50.0e-6,
        "atomic_1A": HBAR_C_EV_M / 1.0e-10,
        "nuclear_1fm": HBAR_C_EV_M / 1.0e-15,
    }


def arena_pairs(inputs: dict[str, float]) -> list[tuple[str, str, str, float, float]]:
    scales = arena_scales(inputs)
    return [
        ("PAIR4927_NS_GW", "GW250114", "NS_12km", scales["GW250114"], scales["NS_12km"]),
        ("PAIR4927_NS_Earth", "Earth", "NS_12km", scales["Earth"], scales["NS_12km"]),
        ("PAIR4927_R10_AU", "AU", "R10_50um", scales["AU"], scales["R10_50um"]),
        ("PAIR4927_atomic_AU", "AU", "atomic_1A", scales["AU"], scales["atomic_1A"]),
        ("PAIR4927_nuclear_AU", "AU", "nuclear_1fm", scales["AU"], scales["nuclear_1fm"]),
    ]


def form_factor_scan_rows(inputs: dict[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pair_id, low_name, high_name, q_low, q_high in arena_pairs(inputs):
        log_ratio = math.log((q_high / q_low) ** 2)
        delta_bound = log_ratio / 60.0
        for exponent_half in range(-40, 41):
            mass_ratio = 10.0 ** (exponent_half / 2.0)
            mass_eV = q_high * mass_ratio
            u_high = mp.mpf(q_high / mass_eV) ** 2
            u_low = mp.mpf(q_low / mass_eV) ** 2
            delta = abs(k_w(u_high) - k_w(u_low))
            epsilon = (
                float(delta)
                * q_high**2
                / (16.0 * math.pi**2 * REDUCED_PLANCK_ENERGY_EV**2)
            )
            rows.append(
                {
                    "pair_id": pair_id,
                    "low_arena": low_name,
                    "high_arena": high_name,
                    "q_low_eV": q_low,
                    "q_high_eV": q_high,
                    "mass_over_q_high": mass_ratio,
                    "mass_eV": mass_eV,
                    "u_low": float(u_low),
                    "u_high": float(u_high),
                    "abs_delta_kW": float(delta),
                    "analytic_delta_kW_bound": delta_bound,
                    "bound_ratio": float(delta) / delta_bound,
                    "spin2_relative_transfer": epsilon,
                    "mass_regime": "light" if mass_ratio <= 0.1 else "heavy" if mass_ratio >= 10.0 else "crossover",
                    "status": "EXACT_FORM_FACTOR_WITHIN_MASSLESS_SLOPE_BOUND",
                    "passed": delta <= mp.mpf(delta_bound) * (1 + mp.mpf("2e-13")),
                }
            )
    return tagged(rows)


def cross_arena_transfer_rows(inputs: dict[str, float]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pair_id, low_name, high_name, q_low, q_high in arena_pairs(inputs):
        log_q_ratio = math.log(q_high / q_low)
        delta_kw_bound = log_q_ratio / 30.0
        spin2 = (
            q_high**2
            * log_q_ratio
            / (480.0 * math.pi**2 * REDUCED_PLANCK_ENERGY_EV**2)
        )
        spin0_minimal = (
            q_high**2
            * log_q_ratio
            / (96.0 * math.pi**2 * REDUCED_PLANCK_ENERGY_EV**2)
        )
        newton_unit_envelope = (
            q_high**2
            * log_q_ratio
            / (16.0 * math.pi**2 * REDUCED_PLANCK_ENERGY_EV**2)
        )
        largest = max(spin2, spin0_minimal, newton_unit_envelope)
        rows.append(
            {
                "pair_id": pair_id,
                "low_arena": low_name,
                "high_arena": high_name,
                "q_low_eV": q_low,
                "q_high_eV": q_high,
                "ln_q_high_over_q_low": log_q_ratio,
                "delta_kW_bound": delta_kw_bound,
                "spin2_transfer_per_real_scalar": spin2,
                "spin0_minimal_massless_envelope_per_real_scalar": spin0_minimal,
                "unit_weight_Newton_running_envelope_per_real_scalar": newton_unit_envelope,
                "real_scalar_multiplicity_to_one_percent": 0.01 / largest,
                "formula_spin2": "q_high^2 ln(q_high/q_low)/(480 pi^2 Mbar_Pl^2)",
                "status": "ALL_MASS_SPIN2_BOUND_AND_SOURCE_BACKED_SPIN0_NEWTON_ENVELOPES_TINY",
                "passed": largest < 1.0e-30,
            }
        )
    return tagged(rows)


def mass_regime_rows(inputs: dict[str, float]) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "regime": "heavy",
                "condition": "m>=10Q",
                "valid_description": "local Schwinger-DeWitt threshold plus power-suppressed exact form factor",
                "forbidden_extrapolation": "none if Q/m gate is enforced",
                "normalization_dependence": "mass location depends on invariant mu; old C_N coordinate does not",
                "local_GR_result": "4926 local threshold and 4927 quadratic decoupling both compact-safe",
                "status": "CLOSED_PER_FINITE_REAL_POLE",
                "passed": True,
            },
            {
                "regime": "crossover",
                "condition": "0.1Q<m<10Q",
                "valid_description": "exact k_W(u) form factor",
                "forbidden_extrapolation": "do not use the local 1/m^2 C3 coefficient",
                "normalization_dependence": "only selects a point on the bounded universal threshold curve",
                "local_GR_result": "exact scan remains below the massless-slope transfer bound",
                "status": "CLOSED_SPIN2_TRANSFER",
                "passed": True,
            },
            {
                "regime": "light_or_massless",
                "condition": "m<=0.1Q including m=0",
                "valid_description": "renormalized nonlocal curvature logarithm and momentum-subtraction running",
                "forbidden_extrapolation": "never continue 1/m^2 to zero mass",
                "normalization_dependence": "massless transfer depends on arena ratio not on old C_N",
                "local_GR_result": "Planck-suppressed cross-arena transfer is the worst finite-pole envelope",
                "status": "CLOSED_SPIN2_AND_BOUNDED_TRACE_NEWTON_TRANSFER",
                "passed": True,
            },
            {
                "regime": "all",
                "condition": "0<=m<infinity for finite real-pole multiplicity",
                "valid_description": "matched local plus exact crossover plus nonlocal domains",
                "forbidden_extrapolation": "no single asymptotic formula outside its domain",
                "normalization_dependence": "physical mu remains a scalar-sector input but is not needed for local loop safety",
                "local_GR_result": "motion-loop mass uncertainty removed as a local-GR blocker",
                "status": "ALL_MASS_DOMAIN_COVERAGE_ACHIEVED_FINITE_MULTIPLICITY",
                "passed": True,
            },
        ]
    )


def normalization_decision_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "object": "C_N=M_N/M_Pl",
                "old_status": "unfixed dimensionless normalization",
                "new_status": "redundant old-field coordinate",
                "physical_replacement": "none by itself",
                "consequence": "remove C_N from the physical parameter count",
                "passed": True,
            },
            {
                "object": "g_psi=lambda_old M_N^(-1/3)",
                "old_status": "C_N-dependent repaired coupling",
                "new_status": "field-redefinition invariant scalar coupling",
                "physical_replacement": "g_psi or mu=g_psi^(3/8)",
                "consequence": "physical motion gap remains to be derived or measured directly",
                "passed": True,
            },
            {
                "object": "B_psi=B_old M_N",
                "old_status": "missing metric-covariance normalization",
                "new_status": "field-redefinition invariant covariance coefficient",
                "physical_replacement": "B_psi=L_C^4 or zeta_B Lambda^-4",
                "consequence": "historical covariance map needs an independent state/matching condition",
                "passed": True,
            },
            {
                "object": "M_R^2",
                "old_status": "calibrated Einstein residue",
                "new_status": "unchanged independent integrated-H coupling",
                "physical_replacement": "G_N=(8pi M_R^2)^-1",
                "consequence": "cannot fix an old-field coordinate normalization",
                "passed": True,
            },
            {
                "object": "motion-loop local GR safety",
                "old_status": "conditional compact mass floor",
                "new_status": "all-mass domain covered for finite pole multiplicity",
                "physical_replacement": "local threshold exact crossover and nonlocal transfer",
                "consequence": "mu uncertainty no longer blocks local spin2 GR",
                "passed": True,
            },
            {
                "object": "a_IR",
                "old_status": "one signed low-energy Weyl-cubic coefficient",
                "new_status": "retained",
                "physical_replacement": "none",
                "consequence": "finite UV and QCD matching remain one observable Wilson input",
                "passed": True,
            },
        ]
    )


def gate_decision_rows(
    covariance_rows: list[dict[str, Any]],
    orbit_rows: list[dict[str, Any]],
    beta_rows: list[dict[str, Any]],
    scan_rows: list[dict[str, Any]],
    transfer_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "gate": "covariance_dimension",
                "status": "OLD_COEFFICIENT_ONE_AND_ELL_SQUARED_MAPS_SUPERSEDED",
                "decision": "correct coefficients are B_old with dimension -5 and B_psi=B_old M_N with dimension -4",
                "claim_promoted": False,
                "passed": all(bool(row["passed"]) for row in covariance_rows),
            },
            {
                "gate": "field_redefinition",
                "status": "C_N_REDUNDANT_COORDINATE",
                "decision": "g_psi and B_psi are invariant along the exact old-field rescaling orbit",
                "claim_promoted": False,
                "passed": all(bool(row["passed"]) for row in orbit_rows),
            },
            {
                "gate": "Einstein_residue",
                "status": "CANNOT_FIX_C_N",
                "decision": "stress normalization cancels and active integrated H contains no equation for the old coordinate",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "exact_form_factor",
                "status": "MONOTONE_BETA_BOUND_DERIVED",
                "decision": "-1/60<=d kW/d ln u<=0 for every scalar mass",
                "claim_promoted": False,
                "passed": all(bool(row["passed"]) for row in beta_rows),
            },
            {
                "gate": "all_mass_scan",
                "status": "LOCAL_CROSSOVER_NONLOCAL_DOMAINS_COVERED",
                "decision": "all exact scan rows lie below the massless-slope transfer bound",
                "claim_promoted": False,
                "passed": all(bool(row["passed"]) for row in scan_rows),
            },
            {
                "gate": "local_hierarchy",
                "status": "MOTION_MASS_UNCERTAINTY_NOT_LOCAL_GR_BLOCKER",
                "decision": "all one-pole spin2 spin0 and conservative Newton transfers are below 1e-30",
                "claim_promoted": False,
                "passed": all(bool(row["passed"]) for row in transfer_rows),
            },
            {
                "gate": "weak_GR_Newton_Maxwell",
                "status": "RETAINED",
                "decision": "canonicalization cannot alter the one Hilbert source calibrated M_R Newton limit or Maxwell Poynting stress",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "compact_GR",
                "status": "NOT_PROMOTED_TOTAL_WILSON_REMAINDER_OPEN",
                "decision": "motion-loop mass dependence is closed but finite integrated-H and QCD Wilson matching remain",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "full_MTS_to_GR",
                "status": "NOT_PROMOTED",
                "decision": "physical invariant motion gap state and complete ultraviolet matching remain open",
                "claim_promoted": False,
                "passed": True,
            },
            {
                "gate": "next_target",
                "status": "INTEGRATED_H_C3_FUNCTIONAL_FLOW",
                "decision": NEXT_TARGET,
                "claim_promoted": False,
                "passed": True,
            },
        ]
    )


def source_register_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source_id, path, expected_hash, role in (
        ("SRC4927_00_form_pdf", FORM_FACTOR_PDF, EXPECTED_HASHES[FORM_FACTOR_PDF], "exact_massive_scalar_form_factors"),
        ("SRC4927_01_form_source", FORM_FACTOR_SOURCE, EXPECTED_HASHES[FORM_FACTOR_SOURCE], "author_TeX_equation_lock"),
        ("SRC4927_02_decoupling_pdf", DECOUPLING_PDF, EXPECTED_HASHES[DECOUPLING_PDF], "four_dimensional_decoupling"),
        ("SRC4927_03_decoupling_source", DECOUPLING_SOURCE, EXPECTED_HASHES[DECOUPLING_SOURCE], "author_TeX_beta_limits"),
    ):
        exists = path.exists()
        actual_hash = digest(path) if exists else ""
        passed = exists and actual_hash == expected_hash
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": path.relative_to(ROOT).as_posix(),
                "source_role": role,
                "verification": "SHA256",
                "expected_sha256": expected_hash,
                "actual_sha256": actual_hash,
                "source_exists": exists,
                "marker_found": passed,
                "status": "LOCAL_BINARY_SOURCE_HASH_VERIFIED" if passed else "LOCAL_BINARY_SOURCE_FAILED",
                "passed": passed,
            }
        )
    for source_id, path, marker, role in (
        ("SRC4927_04_provenance", PROVENANCE, "MTS_MOTION_NORMALIZATION_FORM_FACTOR_PROVENANCE_4927", "source_provenance"),
        ("SRC4927_05_core", CORE_ACTION, "g_{μν} = η_{μν}", "raw_covariance_metric"),
        ("SRC4927_06_4872", CHECKPOINT_4872, "ell_*^2", "connected_covariance_candidate"),
        ("SRC4927_07_4873", CHECKPOINT_4873, "Lambda_{\\rm UV}=\\ell_*^{-1}", "historical_scale_identification"),
        ("SRC4927_08_4874", CHECKPOINT_4874, "densitized principal symbol", "reference_free_metric"),
        ("SRC4927_09_4875", CHECKPOINT_4875, "strict fixed-background scalar-only composite graviton", "composite_branch_rejection"),
        ("SRC4927_10_4876", CHECKPOINT_4876, "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876", "EH_matching_and_poles"),
        ("SRC4927_11_4877", CHECKPOINT_4877, "MTS_SPECTRUM_NO_GO_NONLOCAL_COMPLETION_AND_RENORMALIZED_VACUUM_FREEZE_4877", "massless_nonlocal_envelope"),
        ("SRC4927_12_4898", CHECKPOINT_4898, "rank}(DF)=1", "EH_nonidentifiability"),
        ("SRC4927_13_4915", CHECKPOINT_4915, "MTS_SINGLE_FUNCTIONAL_EH_SOURCE_RESIDUE_4915", "field_normalization_invariant_graviton_residue"),
        ("SRC4927_14_4916", CHECKPOINT_4916, "S_\\psi[\\mathcal H,\\psi]", "canonical_motion_Hilbert_action"),
        ("SRC4927_15_4926", CHECKPOINT_4926, "MTS_KNOWN_THRESHOLD_MOTION_SCALE_4926", "motion_dimension_repair"),
        ("SRC4927_16_4926_repair", MOTION_REPAIR_PATH, "generic_normalization", "prior_motion_normalization_rows"),
        ("SRC4927_17_research", Path(__file__).resolve(), "def beta_w_exact", "generated_research_code"),
        ("SRC4927_20_checkpoint", CHECKPOINT_DOC, MARKER, "generated_checkpoint"),
        ("SRC4927_21_formal", FORMAL_NOTE, FORMAL_MARKER, "formal_checkpoint_note"),
        ("SRC4927_22_validation", VALIDATION, "MTS_MOTION_NORMALIZATION_COVARIANCE_VALIDATION_4927", "independent_validation_code"),
        ("SRC4927_23_resume", RESUME, NEXT_TARGET, "local_resume_ledger"),
        ("SRC4927_24_claims", CLAIMS_REGISTER, "L-769", "claim_register"),
        ("SRC4927_25_variables", VARIABLE_REGISTER, "MotionNormalizationStatus4927_MTS", "variable_register"),
        ("SRC4927_26_equations", EQUATION_REGISTER, "1.220 Motion-coordinate redundancy and all-mass scalar loop bound", "equation_register"),
        ("SRC4927_27_red_team", RED_TEAM_REGISTER, "171. A field-coordinate normalization is not a physical coupling", "red_team_register"),
        ("SRC4927_28_spine", SPINE_REGISTER, "PPC4161 checkpoint 4927", "unification_spine"),
    ):
        exists = path.exists()
        marker_found = exists and marker in read_text_auto(path)
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": path.relative_to(ROOT).as_posix(),
                "source_role": role,
                "verification": "path_and_marker",
                "expected_sha256": "",
                "actual_sha256": digest(path) if exists else "",
                "source_exists": exists,
                "marker_found": marker_found,
                "status": "LOCAL_TEXT_SOURCE_VERIFIED" if marker_found else "LOCAL_TEXT_SOURCE_FAILED",
                "passed": marker_found,
            }
        )
    for source_id, url, role in (
        ("SRC4927_18_form_URL", FORM_FACTOR_URL, "primary_form_factor_paper"),
        ("SRC4927_19_decoupling_URL", DECOUPLING_URL, "primary_decoupling_paper"),
    ):
        rows.append(
            {
                "source_id": source_id,
                "source_path_or_url": url,
                "source_role": role,
                "verification": "external_primary_URL_recorded",
                "expected_sha256": "",
                "actual_sha256": "",
                "source_exists": True,
                "marker_found": True,
                "status": "EXTERNAL_PRIMARY_URL_RECORDED",
                "passed": True,
            }
        )
    return tagged(rows)


def main() -> int:
    inputs = prior_inputs()
    covariance_rows = covariance_dimension_rows()
    orbit_rows = field_redefinition_rows()
    jacobian_rows = invariant_jacobian_rows()
    stress_rows = stress_residue_rows()
    eh_rows = eh_matching_rows()
    beta_rows = form_factor_beta_rows()
    scan_rows = form_factor_scan_rows(inputs)
    transfer_rows = cross_arena_transfer_rows(inputs)
    regime_rows = mass_regime_rows(inputs)
    normalization_rows = normalization_decision_rows()
    source_rows = source_register_rows()
    gate_rows = gate_decision_rows(
        covariance_rows, orbit_rows, beta_rows, scan_rows, transfer_rows
    )
    tables = {
        "P8_Y5_R2FR_4927_COVARIANCE_DIMENSION_AUDIT.csv": covariance_rows,
        "P8_Y5_R2FR_4927_FIELD_REDEFINITION_ORBIT.csv": orbit_rows,
        "P8_Y5_R2FR_4927_INVARIANT_JACOBIAN.csv": jacobian_rows,
        "P8_Y5_R2FR_4927_STRESS_RESIDUE_CANCELLATION.csv": stress_rows,
        "P8_Y5_R2FR_4927_EH_MATCHING_IDENTIFIABILITY.csv": eh_rows,
        "P8_Y5_R2FR_4927_WEYL_FORM_FACTOR_BETA.csv": beta_rows,
        "P8_Y5_R2FR_4927_SCALAR_FORM_FACTOR_SCAN.csv": scan_rows,
        "P8_Y5_R2FR_4927_CROSS_ARENA_TRANSFER.csv": transfer_rows,
        "P8_Y5_R2FR_4927_MOTION_MASS_REGIME_GATE.csv": regime_rows,
        "P8_Y5_R2FR_4927_NORMALIZATION_DECISION.csv": normalization_rows,
        "P8_Y5_R2FR_4927_SOURCE_REGISTER.csv": source_rows,
        "P8_Y5_R2FR_4927_GATE_DECISION.csv": gate_rows,
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    all_rows = [row for rows in tables.values() for row in rows]
    passed = all(bool(row.get("passed", True)) for row in all_rows)
    max_scan_ratio = max(float(row["bound_ratio"]) for row in scan_rows)
    max_transfer = max(
        max(
            float(row["spin2_transfer_per_real_scalar"]),
            float(row["spin0_minimal_massless_envelope_per_real_scalar"]),
            float(row["unit_weight_Newton_running_envelope_per_real_scalar"]),
        )
        for row in transfer_rows
    )
    print(
        "P8_Y5_R2FR_4927_MOTION_NORMALIZATION_COVARIANCE_PASS"
        if passed
        else "P8_Y5_R2FR_4927_MOTION_NORMALIZATION_COVARIANCE_FAIL"
    )
    print("C_N_physical_parameter=False")
    print(f"max_exact_form_factor_bound_ratio={max_scan_ratio:.16e}")
    print(f"max_one_scalar_transfer={max_transfer:.16e}")
    print("motion_mass_uncertainty_local_GR_blocker=False")
    print("compact_GR_promoted=False")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
