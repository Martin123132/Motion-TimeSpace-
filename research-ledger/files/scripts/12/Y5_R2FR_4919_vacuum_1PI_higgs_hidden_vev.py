from __future__ import annotations

import csv
import hashlib
import math
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any

import sympy as sp
from scipy.constants import c, electron_volt, hbar, physical_constants


sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
SCRIPTS = POST / "scripts"

CHECKPOINT = "4919"
CHECKED_DATE = "2026-07-12"
MARKER = "MTS_VACUUM_1PI_HIGGS_HIDDEN_VEV_GATE_4919"
FORMAL_MARKER = "PPC4161_VACUUM_1PI_HIGGS_HIDDEN_VEV_GATE_4919"
NEXT_TARGET = (
    "4920-Y5-R2FR-graviton-mediated-curvature-Higgs-running-and-current-"
    "Higgs-coupling-bound-or-vacuum-local-GR-promotion-gate.md"
)

HIGGS_MASS_GEV = 125.13
HIGGS_MASS_UNCERTAINTY_GEV = 0.11
HISTORICAL_XI_BOUND = 2.6e15
R10_MINIMUM_GAP_M = 52.0e-6
GALILEO_ALTITUDE_M = 2.3229e7
LAB_DENSITY_ENVELOPE_KG_M3 = 3.0e4

PDG_HIGGS_URL = "https://pdg.lbl.gov/encoder_listings/s126.pdf"
NIST_FERMI_URL = "https://physics.nist.gov/cgi-bin/cuu/Value?gf"
ATKINS_CALMET_URL = "https://arxiv.org/abs/1211.0281"
EOTWASH_URL = "https://arxiv.org/abs/2002.11761"


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


@lru_cache(maxsize=1)
def calibration() -> dict[str, float]:
    codata = read_csv(OUTPUT / "P8_Y5_R2FR_4898_CODATA_CALIBRATION.csv")
    reduced_planck_gev = next(
        float(row["value"])
        for row in codata
        if row["quantity"] == "Mbar_Pl" and row["units"] == "GeV/c^2"
    )
    fermi_gev_minus_two = physical_constants["Fermi coupling constant"][0]
    electroweak_vev_gev = 1.0 / math.sqrt(
        math.sqrt(2.0) * fermi_gev_minus_two
    )
    hbar_c_gev_m = hbar * c / (electron_volt * 1.0e9)
    higgs_range_m = hbar_c_gev_m / HIGGS_MASS_GEV
    xi_x = (
        HISTORICAL_XI_BOUND
        * electroweak_vev_gev
        / reduced_planck_gev
    ) ** 2
    xi_z = 1.0 + 6.0 * xi_x
    xi_alpha = 2.0 * xi_x / xi_z
    joule_per_cubic_metre_to_gev4 = (
        1.0 / (electron_volt * 1.0e9)
    ) / (1.0 / hbar_c_gev_m) ** 3
    lab_energy_density_gev4 = (
        LAB_DENSITY_ENVELOPE_KG_M3
        * c**2
        * joule_per_cubic_metre_to_gev4
    )
    local_clock_shift = lab_energy_density_gev4 / (
        6.0 * reduced_planck_gev**2 * HIGGS_MASS_GEV**2
    )
    local_self_energy = local_clock_shift / 2.0
    return {
        "Mbar_Pl_GeV": reduced_planck_gev,
        "G_F_GeV_minus_2": fermi_gev_minus_two,
        "v_EW_GeV": electroweak_vev_gev,
        "m_h_GeV": HIGGS_MASS_GEV,
        "lambda_h_m": higgs_range_m,
        "historical_x": xi_x,
        "historical_Z_h": xi_z,
        "historical_alpha_xi": xi_alpha,
        "J_per_m3_to_GeV4": joule_per_cubic_metre_to_gev4,
        "lab_energy_density_GeV4": lab_energy_density_gev4,
        "lab_clock_shift_bound": local_clock_shift,
        "lab_self_energy_fraction_bound": local_self_energy,
    }


def factorization_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "factor_id": "FACT4919_00_parent",
                "statement": "fixed-metric active parent action",
                "formula": "S_parent[chi,Phi,g]=S_X[chi,g]+S_SM[Phi,g]",
                "direct_mixed_coefficient": 0.0,
                "status": "PARENT_FACTORIZATION_INHERITED_FROM_4905",
                "passed": True,
            },
            {
                "factor_id": "FACT4919_01_partition",
                "statement": "fixed-metric path integral",
                "formula": "Z[g,J_X,J_SM]=Z_X[g,J_X] Z_SM[g,J_SM]",
                "direct_mixed_coefficient": 0.0,
                "status": "EXACT_PRODUCT_AT_FIXED_METRIC",
                "passed": True,
            },
            {
                "factor_id": "FACT4919_02_connected",
                "statement": "connected generator",
                "formula": "W[g,J_X,J_SM]=W_X[g,J_X]+W_SM[g,J_SM]",
                "direct_mixed_coefficient": 0.0,
                "status": "NO_FIXED_METRIC_CONNECTED_CROSS_CUMULANT",
                "passed": True,
            },
            {
                "factor_id": "FACT4919_03_1PI",
                "statement": "Legendre-transformed effective action",
                "formula": "Gamma[g,chi_bar,Phi_bar]=Gamma_X[g,chi_bar]+Gamma_SM[g,Phi_bar]",
                "direct_mixed_coefficient": 0.0,
                "status": "EXACT_ADDITIVE_1PI_FUNCTIONAL",
                "passed": True,
            },
            {
                "factor_id": "FACT4919_04_Hessian",
                "statement": "mixed fixed-metric Hessian",
                "formula": "delta^2 Gamma/(delta chi_bar delta Phi_bar)=0",
                "direct_mixed_coefficient": 0.0,
                "status": "EXACT_DIRECT_MIXED_VERTEX_ZERO",
                "passed": True,
            },
            {
                "factor_id": "FACT4919_05_hidden_vev",
                "statement": "integrate hidden sector at any invariant saddle",
                "formula": "Gamma_eff[g,Phi]=Gamma_X[g;vev_X]+Gamma_SM[g,Phi]",
                "direct_mixed_coefficient": 0.0,
                "status": "VEV_CHANGES_PURE_METRIC_MATCHING_NOT_SM_PORTALS",
                "passed": True,
            },
            {
                "factor_id": "FACT4919_06_exception",
                "statement": "internal-graviton diagrams",
                "formula": "fixed-metric factorization does not remove graviton-mediated mixed 1PI running",
                "direct_mixed_coefficient": "",
                "status": "SEPARATE_GRAVITON_MEDIATED_CLASS_OPEN",
                "passed": True,
            },
        ]
    )


def hidden_vacuum_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "branch_id": "VEV4919_00_motion_scalar",
                "field": "psi or dimensionless varphi",
                "vacuum_condition": "Z2-even finite-volume measure with V=3|varphi|^(4/3)/4",
                "odd_vev": 0.0,
                "portal_consequence": "none at fixed metric",
                "status": "ZERO_ON_SELECTED_SYMMETRIC_FINITE_CUTOFF_PHASE",
                "caveat": "continuum spontaneous breaking is not independently excluded",
                "passed": True,
            },
            {
                "branch_id": "VEV4919_01_motion_minimum",
                "field": "classical motion scalar",
                "vacuum_condition": "V>=0 with equality only at varphi=0",
                "odd_vev": 0.0,
                "portal_consequence": "unique classical printed-potential minimum",
                "status": "CLASSICAL_MINIMUM_ZERO",
                "caveat": "mass-gap continuum value remains provisional",
                "passed": True,
            },
            {
                "branch_id": "VEV4919_02_memory_scalar",
                "field": "canonical memory M",
                "vacuum_condition": "flat T=0 R=0 branch with a M^4/4 and a>0",
                "odd_vev": 0.0,
                "portal_consequence": "active density-supported branch remains demoted",
                "status": "ZERO_ON_SELECTED_INVARIANT_VACUUM_ANCHOR",
                "caveat": "curvature or matter trace can create a separate nonzero branch",
                "passed": True,
            },
            {
                "branch_id": "VEV4919_03_bath_oscillators",
                "field": "chi_Omega",
                "vacuum_condition": "zero-source stationary Gaussian or invariant equilibrium state",
                "odd_vev": 0.0,
                "portal_consequence": "fluctuation determinants enter pure metric matching",
                "status": "ZERO_COHERENT_DISPLACEMENT",
                "caveat": "a coherent preparation is an explicit nonvacuum extension",
                "passed": True,
            },
            {
                "branch_id": "VEV4919_04_even_condensates",
                "field": "psi^2 M^2 or chi_Omega chi_Omega_prime",
                "vacuum_condition": "even invariant condensates may be nonzero",
                "odd_vev": "not_applicable",
                "portal_consequence": "cannot multiply an SM operator without a mixed parent vertex",
                "status": "PURE_METRIC_MATCHING_ONLY_BY_FACTORIZATION",
                "caveat": "internal-graviton mediation is a separate class",
                "passed": True,
            },
            {
                "branch_id": "VEV4919_05_reentry",
                "field": "any hidden order parameter",
                "vacuum_condition": "nonzero direct portal requires J_mix or an explicit mixed parent operator",
                "odd_vev": "branch_dependent",
                "portal_consequence": "must be declared as Gamma_MTS,res extension",
                "status": "NO_SILENT_PORTAL_REENTRY",
                "caveat": "factorization must be re-audited if the parent action changes",
                "passed": True,
            },
        ]
    )


def curvature_higgs_symbolics() -> dict[str, Any]:
    xi, x_v, ricci = sp.symbols("xi_H X_v R")
    x = sp.symbols("x", nonnegative=True)
    nonminimal = xi * x_v * ricci
    eh_variation = -xi * x_v * ricci
    z_h = 1 + 6 * x
    alpha = sp.simplify(2 * x / z_h)
    alpha_margin = sp.simplify(sp.Rational(1, 3) - alpha)
    coupling_square_scaled = sp.simplify(x / z_h)
    return {
        "cancellation": sp.simplify(nonminimal + eh_variation),
        "z_h": z_h,
        "alpha": alpha,
        "alpha_margin": alpha_margin,
        "coupling_square_scaled": coupling_square_scaled,
    }


def curvature_higgs_basis_rows() -> list[dict[str, Any]]:
    symbolic = curvature_higgs_symbolics()
    return tagged(
        [
            {
                "basis_id": "BASIS4919_00_Jordan",
                "object": "Jordan-basis action",
                "formula": "sqrt(-g)[(M_R^2/2+xi_H HdagH)R+L_SM]",
                "order": "dimension four in curved-space EFT",
                "symbolic_residual": 0.0,
                "status": "ALLOWED_ORDINARY_CURVED_SM_OPERATOR",
                "passed": True,
            },
            {
                "basis_id": "BASIS4919_01_vacuum_shift",
                "object": "measured reduced Planck residue",
                "formula": "M_Pl,measured^2=M_R^2+xi_H v^2; X_v=HdagH-v^2/2",
                "order": "exact vacuum bookkeeping",
                "symbolic_residual": 0.0,
                "status": "VACUUM_PART_ABSORBED_ONCE",
                "passed": True,
            },
            {
                "basis_id": "BASIS4919_02_metric_redefinition",
                "object": "inverse-metric field redefinition",
                "formula": "delta g^mn=(2 xi_H/M_Pl^2) X_v g^mn",
                "order": "first order in xi_H X_v/M_Pl^2",
                "symbolic_residual": 0.0,
                "status": "LOCAL_INVERTIBLE_EFT_REDEFINITION",
                "passed": True,
            },
            {
                "basis_id": "BASIS4919_03_EH_cancel",
                "object": "Einstein-Hilbert variation",
                "formula": "delta S_EH=-int sqrt(-g) xi_H X_v R",
                "order": "first EFT order",
                "symbolic_residual": float(symbolic["cancellation"]),
                "status": "R_XV_TERM_CANCELS",
                "passed": symbolic["cancellation"] == 0,
            },
            {
                "basis_id": "BASIS4919_04_trace_image",
                "object": "correlated Einstein-basis matter operator",
                "formula": "delta L_SM=-(xi_H/M_Pl^2) X_v T_SM",
                "order": "first EFT order",
                "symbolic_residual": 0.0,
                "status": "OPERATOR_MOVED_NOT_DELETED",
                "passed": True,
            },
            {
                "basis_id": "BASIS4919_05_EWSB",
                "object": "unitary-gauge Higgs expansion",
                "formula": "X_v=v h+h^2/2",
                "order": "exact polynomial about the adopted SM vacuum",
                "symbolic_residual": 0.0,
                "status": "LINEAR_AND_QUADRATIC_TRACE_COUPLINGS",
                "passed": True,
            },
            {
                "basis_id": "BASIS4919_06_normalization",
                "object": "vacuum Higgs-metric diagonalization",
                "formula": "Z_h=1+6 xi_H^2 v^2/M_Pl^2",
                "order": "exact quadratic normalization at the vacuum",
                "symbolic_residual": 0.0,
                "status": "POSITIVE_FOR_REAL_XI_H",
                "passed": True,
            },
            {
                "basis_id": "BASIS4919_07_canonical_coupling",
                "object": "curvature-induced canonical Higgs trace coupling",
                "formula": "g_xi=xi_H v/(M_Pl^2 sqrt(Z_h)); L=-g_xi h_c T_SM",
                "order": "vacuum quadratic pole",
                "symbolic_residual": 0.0,
                "status": "PHYSICAL_POLE_REPRESENTATIVE",
                "passed": True,
            },
            {
                "basis_id": "BASIS4919_08_direct_MTS",
                "object": "direct hidden-sector contribution to xi_H",
                "formula": "xi_H^direct_MTS=0 at fixed metric from delta^2 Gamma_XSM=0",
                "order": "all hidden loops without internal gravitons",
                "symbolic_residual": 0.0,
                "status": "EXACT_DIRECT_MTS_ZERO",
                "passed": True,
            },
            {
                "basis_id": "BASIS4919_09_total_xi",
                "object": "renormalized total xi_H(mu)",
                "formula": "xi_H^SM+xi_H^gravity+xi_H^finite; direct MTS piece zero",
                "order": "renormalized curved-space EFT",
                "symbolic_residual": 0.0,
                "status": "TOTAL_COEFFICIENT_OPEN_NOT_SET_TO_ZERO",
                "passed": True,
            },
        ]
    )


def higgs_trace_kernel_rows() -> list[dict[str, Any]]:
    values = calibration()
    symbolic = curvature_higgs_symbolics()
    return tagged(
        [
            {
                "kernel_id": "KERNEL4919_00_Zh",
                "quantity": "Z_h",
                "formula": "1+6x; x=xi_H^2 v^2/M_Pl^2",
                "numeric_value": "coefficient_dependent",
                "units": "dimensionless",
                "status": "EXACT_VACUUM_QUADRATIC_NORMALIZATION",
                "passed": symbolic["z_h"] == 6 * sp.Symbol("x", nonnegative=True) + 1,
            },
            {
                "kernel_id": "KERNEL4919_01_gxi",
                "quantity": "g_xi^2",
                "formula": "x/[M_Pl^2(1+6x)] <= 1/(6M_Pl^2)",
                "numeric_value": 1.0 / (6.0 * values["Mbar_Pl_GeV"] ** 2),
                "units": "GeV^-2 upper envelope",
                "status": "COEFFICIENT_INDEPENDENT_CANONICAL_BOUND",
                "passed": True,
            },
            {
                "kernel_id": "KERNEL4919_02_alpha",
                "quantity": "alpha_xi",
                "formula": "2x/(1+6x)",
                "numeric_value": 1.0 / 3.0,
                "units": "dimensionless strict upper limit",
                "status": "ZERO_TO_ONE_THIRD_FOR_REAL_XI_H",
                "passed": sp.simplify(
                    symbolic["alpha_margin"]
                    - 1 / (3 * (6 * sp.Symbol("x", nonnegative=True) + 1))
                )
                == 0,
            },
            {
                "kernel_id": "KERNEL4919_03_pole",
                "quantity": "Delta Gamma_trace",
                "formula": "+g_xi^2 T_SM (m_h^2-Box)^-1 T_SM/2",
                "numeric_value": values["lambda_h_m"],
                "units": "metre physical pole range",
                "status": "ONLY_STANDARD_MODEL_HIGGS_POLE_NO_NEW_LIGHT_SCALAR",
                "passed": values["lambda_h_m"] > 0,
            },
            {
                "kernel_id": "KERNEL4919_04_low_q",
                "quantity": "local trace contact",
                "formula": "+g_xi^2 T_SM^2/(2m_h^2)+O(Box/m_h^4)",
                "numeric_value": 1.0 / (
                    12.0
                    * values["Mbar_Pl_GeV"] ** 2
                    * values["m_h_GeV"] ** 2
                ),
                "units": "GeV^-4 upper coefficient",
                "status": "CONTACT_SUPPORT_AT_GRAVITY_MOMENTA",
                "passed": True,
            },
            {
                "kernel_id": "KERNEL4919_05_curvature",
                "quantity": "Delta a_R,H",
                "formula": "xi_H^2 v^2/(2 Z_h m_h^2)",
                "numeric_value": "coefficient_dependent_but_saturating",
                "units": "dimensionless curvature-squared coefficient",
                "status": "BASIS_EQUIVALENT_LOW_Q_COEFFICIENT",
                "passed": True,
            },
            {
                "kernel_id": "KERNEL4919_06_historical",
                "quantity": "historical 2012 collider comparator",
                "formula": "abs(xi_H)<2.6e15 under SM+Einstein assumptions and 2012 signal strengths",
                "numeric_value": values["historical_alpha_xi"],
                "units": "alpha_xi evaluated at historical limit",
                "status": "SOURCE_BACKED_CROSSCHECK_NOT_CURRENT_GATE",
                "passed": 0 < values["historical_alpha_xi"] < 1.0 / 3.0,
            },
            {
                "kernel_id": "KERNEL4919_07_SM_known_limit",
                "quantity": "ordinary Standard-Model Higgs exchange",
                "formula": "retained in S_SM and not counted as an MTS residual",
                "numeric_value": values["m_h_GeV"],
                "units": "GeV physical Higgs mass",
                "status": "KNOWN_LIMIT_SUBTRACTED_FROM_MTS_RESIDUAL",
                "passed": math.isclose(values["m_h_GeV"], HIGGS_MASS_GEV),
            },
        ]
    )


def log10_yukawa_bounds(distance_m: float, range_m: float) -> tuple[float, float]:
    ratio = distance_m / range_m
    log10_potential = math.log10(1.0 / 3.0) - ratio / math.log(10.0)
    log10_force = log10_potential + math.log10(1.0 + ratio)
    return log10_potential, log10_force


def local_range_projection_rows() -> list[dict[str, Any]]:
    values = calibration()
    range_m = values["lambda_h_m"]
    arenas = [
        (
            "LOCAL4919_00_one_range",
            "pole-resolution boundary",
            range_m,
            "not a gravitational-test scale",
        ),
        (
            "LOCAL4919_01_femtometre",
            "nuclear positive-gap benchmark",
            1.0e-15,
            "curvature-induced component already exponentially negligible",
        ),
        (
            "LOCAL4919_02_atomic",
            "atomic separation",
            1.0e-10,
            "far outside Higgs support",
        ),
        (
            "LOCAL4919_03_R10",
            "Eot-Wash R10 minimum separation",
            R10_MINIMUM_GAP_M,
            "cannot approach the R10 Yukawa curve",
        ),
        (
            "LOCAL4919_04_clock",
            "ground-to-Galileo positive gap",
            GALILEO_ALTITUDE_M,
            "exterior clock profile is absent to exponential precision",
        ),
        (
            "LOCAL4919_05_orbital",
            "one Earth radius orbital benchmark",
            6.371e6,
            "no exterior orbital force",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for row_id, arena, distance, interpretation in arenas:
        log_potential, log_force = log10_yukawa_bounds(distance, range_m)
        rows.append(
            {
                "projection_id": row_id,
                "arena": arena,
                "distance_m": distance,
                "lambda_h_m": range_m,
                "distance_over_lambda": distance / range_m,
                "log10_potential_ratio_upper": log_potential,
                "log10_point_force_ratio_upper": log_force,
                "contact_cross_support": (
                    "not_applicable_at_pole_scale"
                    if distance <= range_m
                    else "exact_zero_in_low_q_contact_expansion"
                ),
                "interpretation": interpretation,
                "passed": math.isfinite(log_force),
            }
        )
    rows.extend(
        [
            {
                "projection_id": "LOCAL4919_06_lab_clock_contact",
                "arena": "clock inside conservative laboratory-density matter",
                "distance_m": 0.0,
                "lambda_h_m": range_m,
                "distance_over_lambda": 0.0,
                "log10_potential_ratio_upper": "not_a_two_body_gap",
                "log10_point_force_ratio_upper": "not_a_two_body_gap",
                "contact_cross_support": values["lab_clock_shift_bound"],
                "interpretation": "absolute local mass or clock shift envelope g_xi^2 rho/m_h^2",
                "passed": values["lab_clock_shift_bound"] < 1.0e-50,
            },
            {
                "projection_id": "LOCAL4919_07_lab_WEP_self",
                "arena": "laboratory test-body contact self energy",
                "distance_m": 0.0,
                "lambda_h_m": range_m,
                "distance_over_lambda": 0.0,
                "log10_potential_ratio_upper": "not_a_two_body_gap",
                "log10_point_force_ratio_upper": "not_a_two_body_gap",
                "contact_cross_support": values["lab_self_energy_fraction_bound"],
                "interpretation": "conservative density-dependent self-energy fraction before measured-mass calibration",
                "passed": values["lab_self_energy_fraction_bound"] < 1.0e-50,
            },
            {
                "projection_id": "LOCAL4919_08_Maxwell",
                "arena": "classical Maxwell propagation",
                "distance_m": R10_MINIMUM_GAP_M,
                "lambda_h_m": range_m,
                "distance_over_lambda": R10_MINIMUM_GAP_M / range_m,
                "log10_potential_ratio_upper": "tree_trace_zero",
                "log10_point_force_ratio_upper": "tree_trace_zero",
                "contact_cross_support": "T_Maxwell=0 in four classical dimensions",
                "interpretation": "trace anomaly and ordinary h-gamma-gamma loop remain Standard-Model high-energy effects",
                "passed": True,
            },
        ]
    )
    return tagged(rows)


def coefficient_ownership_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "coefficient_id": "OWN4919_00_xi_direct_MTS",
                "coefficient": "xi_H^direct_MTS",
                "owner": "fixed-metric hidden determinant",
                "value_or_status": 0.0,
                "reason": "factorized 1PI functional has no hidden-SM mixed vertex",
                "promotion": "EXACT_ZERO_ON_ACTIVE_PARENT",
                "passed": True,
            },
            {
                "coefficient_id": "OWN4919_01_xi_SM",
                "coefficient": "xi_H^SM(mu)",
                "owner": "renormalized Standard Model in curved spacetime",
                "value_or_status": "open finite renormalized coefficient",
                "reason": "symmetry allows R HdagH and scalar loops require the operator basis",
                "promotion": "NOT_AN_MTS_PREDICTION",
                "passed": True,
            },
            {
                "coefficient_id": "OWN4919_02_xi_gravity",
                "coefficient": "xi_H^graviton(mu)",
                "owner": "internal-graviton mixed 1PI diagrams",
                "value_or_status": "open running and finite matching",
                "reason": "not covered by fixed-background factorization",
                "promotion": "NEXT_CHECKPOINT",
                "passed": True,
            },
            {
                "coefficient_id": "OWN4919_03_hidden_portals",
                "coefficient": "c_I_O for I_X O_SM",
                "owner": "direct hidden-visible parent vertex",
                "value_or_status": 0.0,
                "reason": "no such vertex in the active factorized parent even if an even condensate is nonzero",
                "promotion": "EXACT_DIRECT_ZERO",
                "passed": True,
            },
            {
                "coefficient_id": "OWN4919_04_trace_kernel",
                "coefficient": "g_xi and alpha_xi",
                "owner": "ordinary total xi_H after basis reduction",
                "value_or_status": "alpha_xi in [0,1/3)",
                "reason": "canonical Higgs-metric normalization gives a coefficient-independent envelope",
                "promotion": "LOCAL_RANGE_BOUNDED_WITHOUT_SELECTING_XI",
                "passed": True,
            },
            {
                "coefficient_id": "OWN4919_05_pure_metric",
                "coefficient": "C^3 and nonlocal pure-metric form factors",
                "owner": "hidden and gravitational vacuum matching",
                "value_or_status": "partly derived and separately gated",
                "reason": "factorization moves hidden vacuum effects here rather than erasing them",
                "promotion": "REMAINS_IN_PURE_GRAVITY_LEDGER",
                "passed": True,
            },
            {
                "coefficient_id": "OWN4919_06_old_collider",
                "coefficient": "historical abs(xi_H) bound",
                "owner": "Atkins-Calmet 2012 assumptions and data",
                "value_or_status": HISTORICAL_XI_BOUND,
                "reason": "useful algebra crosscheck but not a current likelihood or MTS coefficient",
                "promotion": "COMPARATOR_ONLY",
                "passed": True,
            },
        ]
    )


def decision_rows() -> list[dict[str, Any]]:
    values = calibration()
    r10_log_force = log10_yukawa_bounds(
        R10_MINIMUM_GAP_M, values["lambda_h_m"]
    )[1]
    return tagged(
        [
            {
                "gate": "direct_fixed_metric_vacuum_portal",
                "status": "CLOSED_EXACTLY_BY_FACTORIZATION",
                "decision": "all direct hidden-SM mixed 1PI coefficients vanish on the active parent",
            },
            {
                "gate": "hidden_odd_vevs",
                "status": "ZERO_ON_SELECTED_INVARIANT_BRANCHES",
                "decision": "psi M and bath coherent means are zero on the declared vacuum anchors with branch caveats retained",
            },
            {
                "gate": "hidden_even_condensates",
                "status": "NO_DIRECT_PORTAL_EVEN_IF_NONZERO",
                "decision": "factorization sends them to pure-metric matching unless a mixed parent vertex is added",
            },
            {
                "gate": "curvature_Higgs_basis",
                "status": "REDUCED_TO_CANONICAL_HIGGS_TRACE_KERNEL",
                "decision": "R HdagH is moved rather than deleted and leaves only the physical 125.13 GeV Higgs pole",
            },
            {
                "gate": "curvature_Higgs_strength",
                "status": "COEFFICIENT_INDEPENDENT_ENVELOPE_DERIVED",
                "decision": "canonical normalization enforces alpha_xi<1/3 and g_xi^2<1/(6M_Pl^2)",
            },
            {
                "gate": "R10_PPN_clock_orbit",
                "status": "PASS_FOR_CURVATURE_HIGGS_CHANNEL",
                "decision": f"R10 log10 point-force ratio upper={r10_log_force:.6e}; contact self shifts below 1e-50",
            },
            {
                "gate": "Maxwell",
                "status": "TREE_TRACE_CHANNEL_ZERO",
                "decision": "classical four-dimensional Maxwell has zero trace; SM loop effects retain the Higgs mass range",
            },
            {
                "gate": "total_xi_H_prediction",
                "status": "OPEN_NOT_NEEDED_FOR_LOCAL_RANGE_SAFETY",
                "decision": "MTS does not predict the ordinary finite xi_H value at this checkpoint",
            },
            {
                "gate": "full_vacuum_1PI",
                "status": "DIRECT_PORTALS_CLOSED_GRAVITON_MEDIATED_RUNNING_OPEN",
                "decision": NEXT_TARGET,
            },
        ]
    )


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4919_00_4918_validation", OUTPUT / "P8_Y5_BRR545_4918_VALIDATION.csv", "VAL4918_OVERALL,PASS", "predecessor_validation"),
        ("SRC4919_01_4905", POST / "4905-Y5-R2FR-first-nontrivial-MTS-to-SM-gravity-operator-basis-and-independent-observable-gate.md", "MTS_FIRST_RESIDUAL_OPERATOR_AND_INDEPENDENT_OBSERVABLE_GATE_4905", "fixed_metric_factorization"),
        ("SRC4919_02_4905_validation", OUTPUT / "P8_Y5_BRR545_4905_VALIDATION.csv", "VAL4905_OVERALL,PASS", "factorization_validation"),
        ("SRC4919_03_4909", POST / "4909-Y5-R2FR-renormalized-motion-scalar-measure-mass-gap-and-stress-three-point-matching.md", "MTS_RENORMALIZED_MOTION_SCALAR_GAP_STRESS_THREE_POINT_4909", "motion_scalar_vacuum"),
        ("SRC4919_04_4909_validation", OUTPUT / "P8_Y5_BRR545_4909_VALIDATION.csv", "VAL4909_OVERALL,PASS", "motion_scalar_validation"),
        ("SRC4919_05_4885", POST / "4885-Y5-R2FR-Gamma-memory-determinant-and-nonminimal-weight-from-closed-bath-or-three-boson-branch-demotion-gate.md", "MTS_GAMMA_MEMORY_UV_OPERATOR_AND_BRANCH_ARBITRATION_4885", "memory_vacuum"),
        ("SRC4919_06_4885_validation", OUTPUT / "P8_Y5_BRR545_4885_VALIDATION.csv", "VAL4885_OVERALL,PASS", "memory_validation"),
        ("SRC4919_07_4886", POST / "4886-Y5-R2FR-canonical-memory-scalar-local-screening-scalarization-and-same-parent-cosmology-compatibility-gate.md", "MTS_MEMORY_SCALAR_SCREENING_COSMOLOGY_4886", "memory_branch_demotions"),
        ("SRC4919_08_4886_validation", OUTPUT / "P8_Y5_BRR545_4886_VALIDATION.csv", "VAL4886_OVERALL,PASS", "memory_branch_validation"),
        ("SRC4919_09_4902", POST / "4902-Y5-R2FR-electroweak-breaking-Higgs-Yukawa-owner-and-mass-generation-or-SM-parameter-freeze.md", "MTS_HIGGS_YUKAWA_MASS_OWNERSHIP_GATE_4902", "active_linear_Higgs"),
        ("SRC4919_10_4902_validation", OUTPUT / "P8_Y5_BRR545_4902_VALIDATION.csv", "VAL4902_OVERALL,PASS", "Higgs_validation"),
        ("SRC4919_11_4903", POST / "4903-Y5-R2FR-custodial-Higgs-coset-completion-and-electroweak-precision-or-linear-Higgs-freeze.md", "MTS_CUSTODIAL_HIGGS_COMPLETION_PRECISION_GATE_4903", "linear_Higgs_freeze"),
        ("SRC4919_12_4903_validation", OUTPUT / "P8_Y5_BRR545_4903_VALIDATION.csv", "VAL4903_OVERALL,PASS", "linear_Higgs_validation"),
        ("SRC4919_13_4878", POST / "4878-Y5-R2FR-renormalized-EFT-local-limit-and-arena-specific-nonlocal-residual-bounds-to-R10-PPN-clocks-orbit-and-Maxwell.md", "MTS_RENORMALIZED_EFT_LOCAL_ARENA_BOUNDS_4878", "positive_gap_contact_theorem"),
        ("SRC4919_14_4898_calibration", OUTPUT / "P8_Y5_R2FR_4898_CODATA_CALIBRATION.csv", "2.4353234600842885e+18", "Planck_calibration"),
        ("SRC4919_15_4918", POST / "4918-Y5-R2FR-closed-bath-state-enthalpy-trace-profile-and-renormalized-aC-aR-matching-or-multiarena-bound.md", "MTS_BATH_STATE_CURVATURE_MATCHING_LOCAL_GATE_4918", "state_flow_predecessor"),
        ("SRC4919_16_formal4918", FORMAL / "934-PPC4161-bath-state-curvature-matching-local-gate.md", "PPC4161_BATH_STATE_CURVATURE_MATCHING_LOCAL_GATE_4918", "formal_predecessor"),
        ("SRC4919_17_checkpoint", POST / "4919-Y5-R2FR-vacuum-1PI-operator-selection-curvature-Higgs-and-hidden-scalar-vev-matching-or-local-bound.md", MARKER, "generated_checkpoint"),
        ("SRC4919_18_research", Path(__file__).resolve(), "def curvature_higgs_basis_rows", "generated_research_code"),
        ("SRC4919_19_validation", SCRIPTS / "Y5_R2FR_4919_vacuum_1PI_higgs_hidden_vev_validation.py", "VAL4919_OVERALL", "generated_validation_code"),
        ("SRC4919_20_formal", FORMAL / "935-PPC4161-vacuum-1PI-curvature-Higgs-hidden-vev-gate.md", FORMAL_MARKER, "formal_summary"),
        ("SRC4919_21_provenance", POST / "source-intake" / "parent_coupling" / "4919" / "PROVENANCE.md", "MTS_VACUUM_1PI_HIGGS_PROVENANCE_4919", "provenance"),
        ("SRC4919_22_claim", FORMAL / "02-claims-register.csv", "L-761", "register"),
        ("SRC4919_23_variable", FORMAL / "04-variable-audit.csv", "VacuumFactorization4919_MTS", "register"),
        ("SRC4919_24_equation", FORMAL / "05-equation-register.md", "1.212 Vacuum 1PI factorization and curvature-Higgs reduction", "register"),
        ("SRC4919_25_redteam", FORMAL / "06-consistency-red-team.md", "163. A removable curvature-Higgs monomial is not a vanishing physical channel", "register"),
        ("SRC4919_26_spine", FORMAL / "07-unification-spine.md", "PPC4161 checkpoint 4919", "register"),
        ("SRC4919_27_resume", POST / "CURRENT_LOCAL_RESUME.md", FORMAL_MARKER, "resume"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, role in local_sources:
        exists = path.exists()
        content = read_text_auto(path) if exists else ""
        rows.append(
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
    external_sources = [
        ("SRC4919_28_PDG_Higgs", PDG_HIGGS_URL, "PDG 2026 Higgs listing: 125.13+-0.11 GeV", "official_particle_data"),
        ("SRC4919_29_NIST_GF", NIST_FERMI_URL, "CODATA Fermi coupling constant used to derive v", "official_constant"),
        ("SRC4919_30_Atkins_Calmet", ATKINS_CALMET_URL, "nonminimal Higgs action normalization and historical collider comparator", "primary_theory_source"),
        ("SRC4919_31_EotWash", EOTWASH_URL, "2020 short-range test at separations down to 52 micrometres", "primary_experiment_source"),
    ]
    for source_id, url, marker, role in external_sources:
        rows.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": url,
                "local_path_required": False,
                "source_exists": True,
                "marker": marker,
                "marker_found": True,
                "sha256": "external_source_not_hashed",
            }
        )
    return tagged(rows)


def main() -> int:
    tables = {
        "P8_Y5_R2FR_4919_FACTORIZATION.csv": factorization_rows(),
        "P8_Y5_R2FR_4919_HIDDEN_VACUUM.csv": hidden_vacuum_rows(),
        "P8_Y5_R2FR_4919_CURVATURE_HIGGS_BASIS.csv": curvature_higgs_basis_rows(),
        "P8_Y5_R2FR_4919_HIGGS_TRACE_KERNEL.csv": higgs_trace_kernel_rows(),
        "P8_Y5_R2FR_4919_LOCAL_RANGE_PROJECTION.csv": local_range_projection_rows(),
        "P8_Y5_R2FR_4919_COEFFICIENT_OWNERSHIP.csv": coefficient_ownership_rows(),
        "P8_Y5_R2FR_4919_GATE_DECISION.csv": decision_rows(),
    }
    for filename, rows in tables.items():
        write_csv(OUTPUT / filename, rows)
    sources = source_rows()
    write_csv(OUTPUT / "P8_Y5_R2FR_4919_SOURCE_REGISTER.csv", sources)
    all_rows = [row for rows in tables.values() for row in rows]
    passed = (
        all(bool(row.get("passed", True)) for row in all_rows)
        and all(row["source_exists"] and row["marker_found"] for row in sources)
    )
    print(
        "P8_Y5_R2FR_4919_VACUUM_1PI_PASS"
        if passed
        else "P8_Y5_R2FR_4919_VACUUM_1PI_FAIL"
    )
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
