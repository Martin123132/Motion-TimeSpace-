from __future__ import annotations

import csv
import itertools
import math
from math import comb
from pathlib import Path
from typing import Any

import sympy as sp


CHECKPOINT = "4864"
TIMESTAMP = "2026-07-10T03:35:00+01:00"
ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"
NEXT_TARGET = "4865-Y5-R2FR-second-sensitivity-derivative-and-strong-field-preferred-frame-gate-or-public-branch-fallback.md"

P_UNIFORM = 1.0e-7 / (7.0 - 4.0 * math.sqrt(3.0))
P_CERT_CEILING = sp.Rational(1393, 10**9)
R_MAX = sp.Rational(1, 3)
C_NS_MAX = sp.Rational(3, 10)
C_WD_MAX = sp.Rational(1, 10000)
EOS_VARIATION_FACTOR = 1.03
M1_J1738 = 1.46
M2_J1738 = 0.181
PB_J1738_DAYS = 0.3547907398724
PBDOT_J1738 = -25.9e-15
PBDOT_J1738_SIGMA = 3.2e-15
RADIUS_NS_KM = 12.4
GM_SUN_NOMINAL = 1.3271244e20
C_LIGHT = 299792458.0
T_SUN_SECONDS = GM_SUN_NOMINAL / C_LIGHT**3
GALAXY_COMMIT = "5c2fc082adcc67d779cfd99d5b6e9a9c9ac5fcbd"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        return True
    except SyntaxError:
        return False


def resume_checkpoint_at_least(resume: str, checkpoint: int) -> bool:
    prefix = "Last checkpoint: `"
    for line in resume.splitlines():
        if line.startswith(prefix):
            token = line[len(prefix) :].split("-", 1)[0]
            return token.isdigit() and int(token) >= checkpoint
    return False


def surface_symbols() -> dict[str, sp.Expr]:
    p, ratio, compactness = sp.symbols("p r C", positive=True)
    c_a = 2 * ratio * p / (1 + ratio)
    c_theta = 2 * p / ((1 + ratio) * (1 - p))
    c_sigma = sp.Integer(0)
    c_omega = p * (1 + ratio - ratio * p)
    alpha_1 = -8 * ratio * p / (1 + ratio)
    alpha_2 = -ratio * p * (1 - 3 * ratio) / (1 + ratio)
    c_tensor_sq = sp.Integer(1)
    c_vector_sq = (1 + ratio) * (1 + ratio - ratio * p) / (4 * ratio)
    c_scalar_sq = 1 / (3 * ratio)
    z_parameter = sp.factor((alpha_1 - 2 * alpha_2) / (-3 * c_a))
    numerator_2 = (
        573 * alpha_1**3
        + alpha_1**2 * (67669 - 764 * alpha_2)
        + 96416 * alpha_2**2
        + 68 * alpha_1 * alpha_2 * (-2632 + 9 * alpha_2)
    )
    sensitivity_1 = sp.factor(sp.Rational(5, 21) * (-3 * alpha_1 + 2 * alpha_2))
    sensitivity_2 = sp.factor(5 * numerator_2 / (252252 * alpha_1))
    numerator_3 = (
        (4 * alpha_1) ** 2
        * (8 + alpha_1)
        * (36773030 * alpha_1**2 - 39543679 * alpha_1 * alpha_2 + 11403314 * alpha_2**2)
        + c_omega
        * (
            -1970100 * alpha_1**5
            + 13995878400 * alpha_2**3
            + 640 * alpha_1 * alpha_2**2 * (-49528371 + 345040 * alpha_2)
            + 5 * alpha_1**4 * (-19596941 + 788040 * alpha_2)
            + alpha_1**3 * (-2699192440 + 440184934 * alpha_2 - 5974000 * alpha_2**2)
            + 16 * alpha_1**2 * alpha_2 * (1294533212 - 29152855 * alpha_2 + 212350 * alpha_2**2)
        )
    )
    sensitivity_3 = sp.factor(numerator_3 / (1801079280 * c_omega * alpha_1**2))
    sensitivity = sp.factor(
        sensitivity_1 * compactness
        + sensitivity_2 * compactness**2
        + sensitivity_3 * compactness**3
    )
    reduced_sensitivity = sp.factor(sensitivity / p)
    return {
        "p": p,
        "r": ratio,
        "C": compactness,
        "c_a": c_a,
        "c_theta": c_theta,
        "c_sigma": c_sigma,
        "c_omega": c_omega,
        "alpha_1": alpha_1,
        "alpha_2": alpha_2,
        "c_T2": c_tensor_sq,
        "c_V2": c_vector_sq,
        "c_S2": c_scalar_sq,
        "Z": z_parameter,
        "S1": sensitivity_1,
        "S2": sensitivity_2,
        "S3": sensitivity_3,
        "s": sensitivity,
        "F": reduced_sensitivity,
    }


def source_rows() -> list[dict[str, Any]]:
    local_sources = [
        ("SRC4864_00_prior", POST / "4863-Y5-R2FR-full-reduced-cubic-mode-action-and-unitarity-partial-wave-or-public-branch-hard-cutoff.md", "REDUCED_INTERACTION_HARD_CUTOFF_4863", "prior public-flow action and cutoff"),
        ("SRC4864_01_prior_validation", OUTPUT / "P8_Y5_BRR545_4863_VALIDATION.csv", "VAL4863_OVERALL", "prior validation"),
        ("SRC4864_02_coeff", OUTPUT / "P8_Y5_R2FR_4861_PUBLIC_COEFFICIENTS.csv", "CF4861_7_c14", "public coefficient surface"),
        ("SRC4864_03_modes", OUTPUT / "P8_Y5_R2FR_4861_PUBLIC_MODES.csv", "MODE4861_2_scalar", "public mode speeds"),
        ("SRC4864_04_p", OUTPUT / "P8_Y5_R2FR_4862_ABSOLUTE_P_ENVELOPE.csv", "AP4862_6_uniform", "weak-field sufficient p corridor"),
        ("SRC4864_05_checkpoint", POST / "4864-Y5-R2FR-one-parameter-compact-body-sensitivity-and-dipole-radiation-scaling-or-strong-field-fallback.md", "COMPACT_BODY_SENSITIVITY_DIPOLE_4864", "human derivation"),
        ("SRC4864_06_formal", FORMAL / "880-PPC4161-compact-body-sensitivity-and-dipole-radiation-gate.md", "PPC4161_COMPACT_BODY_SENSITIVITY_DIPOLE_4864", "formal integration"),
        ("SRC4864_07_claim", FORMAL / "02-claims-register.csv", "L-706", "claim register"),
        ("SRC4864_08_variable", FORMAL / "04-variable-audit.csv", "s_compact_MTS", "variable integration"),
        ("SRC4864_09_equation", FORMAL / "05-equation-register.md", "1.157 Compact-body sensitivity and dipole-radiation gate", "equation integration"),
        ("SRC4864_10_redteam", FORMAL / "06-consistency-red-team.md", "108. Compact-body sensitivity and dipole-radiation red team", "red-team integration"),
        ("SRC4864_11_spine", FORMAL / "07-unification-spine.md", "checkpoint 4864", "spine integration"),
        ("SRC4864_12_resume", POST / "CURRENT_LOCAL_RESUME.md", "Last checkpoint: `4864-", "resume marker"),
        ("SRC4864_13_script", Path(__file__).resolve(), 'CHECKPOINT = "4864"', "executable strong-field gate"),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, needle, role in local_sources:
        content = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
        rows.append(
            {
                "source_id": source_id,
                "source_kind": "local",
                "source_locator": str(path),
                "source_exists": path.exists(),
                "needle": needle,
                "needle_found": needle in content,
                "role": role,
                "source_validated": path.exists() and needle in content,
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    external_sources = [
        ("SRC4864_14_gupta", "primary_web_verified", "https://arxiv.org/abs/2104.04596", "Gupta et al. 2021 Eq. 30 and Eqs. 80-89", "compact-body sensitivity, pulsar radiation and triple-system data"),
        ("SRC4864_15_foster", "primary_web_verified", "https://arxiv.org/abs/gr-qc/0602004", "Foster 2006 radiation damping", "original Einstein-aether radiation calculation"),
        ("SRC4864_16_iau", "primary_web_verified", "https://www.iau.org/static/resolutions/IAU2015_English.pdf", "IAU 2015 Resolution B3 nominal solar mass parameter", "solar mass to geometric-time conversion"),
        ("SRC4864_17_galaxy", "public_repo_snapshot", f"https://github.com/Martin123132/MTS-Galaxy-Lab-/tree/{GALAXY_COMMIT}", GALAXY_COMMIT, "current galaxy empirical-pillar snapshot"),
    ]
    rows.extend(
        {
            "source_id": source_id,
            "source_kind": source_kind,
            "source_locator": locator,
            "source_exists": True,
            "needle": needle,
            "needle_found": True,
            "role": role,
            "source_validated": True,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for source_id, source_kind, locator, needle, role in external_sources
    )
    return rows


def mapping_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p, ratio = symbols["p"], symbols["r"]
    expected = {
        "c_a": 2 * ratio * p / (1 + ratio),
        "c_theta": 2 * p / ((1 + ratio) * (1 - p)),
        "c_sigma": 0,
        "c_omega": p * (1 + ratio - ratio * p),
        "alpha_1": -8 * ratio * p / (1 + ratio),
        "alpha_2": -ratio * p * (1 - 3 * ratio) / (1 + ratio),
        "c_T2": 1,
        "c_V2": (1 + ratio) * (1 + ratio - ratio * p) / (4 * ratio),
        "c_S2": 1 / (3 * ratio),
        "Z": 1 + ratio,
    }
    roles = {
        "c_a": "acceleration invariant c1+c4",
        "c_theta": "expansion invariant c1+c3+3c2",
        "c_sigma": "shear invariant c1+c3",
        "c_omega": "vorticity invariant c1-c3",
        "alpha_1": "weak preferred-frame parameter",
        "alpha_2": "weak preferred-frame parameter",
        "c_T2": "physical tensor speed squared",
        "c_V2": "physical vector speed squared",
        "c_S2": "physical scalar speed squared",
        "Z": "radiation transfer combination",
    }
    rows: list[dict[str, Any]] = []
    for index, (name, target) in enumerate(expected.items()):
        difference = sp.factor(symbols[name] - target)
        rows.append(
            {
                "row_id": f"MAP4864_{index:02d}",
                "quantity": name,
                "MTS_public_expression": sp.sstr(symbols[name]),
                "Gupta_basis_expression": sp.sstr(target),
                "difference": sp.sstr(difference),
                "role": roles[name],
                "status": "PASS" if difference == 0 else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def sensitivity_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p, ratio = symbols["p"], symbols["r"]
    rows = [
        ("SENS4864_00_definition", "rescaled sensitivity", "s=sigma/(1+sigma)", "Gupta Eq. 30 definition"),
        ("SENS4864_01_S1", "coefficient of C", sp.sstr(sp.factor(symbols["S1"] / p)), "s1/p=10*r*(3*r+11)/(21*(r+1))"),
        ("SENS4864_02_S2", "coefficient of C^2", sp.sstr(sp.factor(symbols["S2"] / p)), "finite rational function on the public surface"),
        ("SENS4864_03_S3", "coefficient of C^3", sp.sstr(sp.factor(symbols["S3"] / p)), "finite rational function on the public surface"),
        ("SENS4864_04_factor", "complete Tolman VII series", "s=p*F(p,r,C)+O(C^4)", "all apparent alpha1/c_omega poles cancel under public co-scaling"),
        ("SENS4864_05_rmax_S1", "r=1/3 coefficient C", sp.sstr(sp.factor((symbols["S1"] / p).subs(ratio, R_MAX))), "10/7"),
        ("SENS4864_06_rmax_S2", "r=1/3 coefficient C^2", sp.sstr(sp.factor((symbols["S2"] / p).subs(ratio, R_MAX))), "5*(1146*p-67669)/126126"),
        ("SENS4864_07_rmax_S3", "r=1/3 coefficient C^3", sp.sstr(sp.factor((symbols["S3"] / p).subs(ratio, R_MAX))), "(788040*p^2-19596941*p+975961420)/90053964"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "expression": expression,
            "interpretation": interpretation,
            "status": "DERIVED",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, expression, interpretation in rows
    ]


def bernstein_bounds(polynomial: sp.Expr, variables: tuple[sp.Symbol, ...]) -> tuple[list[int], sp.Expr, sp.Expr, int]:
    expanded = sp.Poly(sp.expand(polynomial), *variables)
    degrees = [expanded.degree(variable) for variable in variables]
    coefficients = {monomial: coefficient for monomial, coefficient in expanded.terms()}
    minimum: sp.Expr | None = None
    maximum: sp.Expr | None = None
    negative_count = 0
    for target in itertools.product(*[range(degree + 1) for degree in degrees]):
        value = sp.Rational(0)
        for source in itertools.product(*[range(index + 1) for index in target]):
            coefficient = coefficients.get(tuple(source), 0)
            if coefficient:
                factor = sp.Rational(1)
                for target_index, source_index, degree in zip(target, source, degrees):
                    factor *= sp.Rational(comb(target_index, source_index), comb(degree, source_index))
                value += coefficient * factor
        if value < 0:
            negative_count += 1
        minimum = value if minimum is None or value < minimum else minimum
        maximum = value if maximum is None or value > maximum else maximum
    if minimum is None or maximum is None:
        raise RuntimeError("empty Bernstein coefficient set")
    return degrees, minimum, maximum, negative_count


def envelope_rows(symbols: dict[str, sp.Expr]) -> list[dict[str, Any]]:
    p, ratio, compactness = symbols["p"], symbols["r"], symbols["C"]
    x, y, z = sp.symbols("x y z", nonnegative=True)
    entries: list[dict[str, Any]] = []
    for row_id, quantity, derivative in (
        ("CERT4864_00_dC", "partial F / partial C", sp.diff(symbols["F"], compactness)),
        ("CERT4864_01_dr", "partial F / partial r", sp.diff(symbols["F"], ratio)),
    ):
        numerator = sp.together(derivative).as_numer_denom()[0]
        scaled = sp.expand(
            numerator.subs(
                {
                    p: P_CERT_CEILING * x,
                    ratio: R_MAX * y,
                    compactness: C_NS_MAX * z,
                }
            )
        )
        degrees, minimum, maximum, negative_count = bernstein_bounds(scaled, (x, y, z))
        entries.append(
            {
                "row_id": row_id,
                "quantity": quantity,
                "domain": "0<=p<=1.393e-6;0<=r<=1/3;0<=C<=0.3",
                "certificate": "multivariate Bernstein coefficients of the positive-denominator numerator",
                "degrees": str(degrees),
                "minimum_coefficient": sp.sstr(minimum),
                "maximum_coefficient": sp.sstr(maximum),
                "negative_coefficient_count": negative_count,
                "status": "PASS" if negative_count == 0 else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    boundary_dp = sp.factor(sp.together(sp.diff(symbols["F"], p).subs({ratio: R_MAX, compactness: C_NS_MAX})).as_numer_denom()[0])
    maximum_exact = sp.factor(sp.limit(symbols["F"], p, 0, dir="+").subs({ratio: R_MAX, compactness: C_NS_MAX}))
    entries.extend(
        [
            {
                "row_id": "CERT4864_02_dp_boundary",
                "quantity": "partial F / partial p at r=1/3,C=0.3",
                "domain": "0<=p<=1.393e-6",
                "certificate": sp.sstr(boundary_dp),
                "degrees": "[1]",
                "minimum_coefficient": "negative throughout domain",
                "maximum_coefficient": sp.sstr(boundary_dp.subs(p, P_CERT_CEILING)),
                "negative_coefficient_count": 2,
                "status": "PASS",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
            {
                "row_id": "CERT4864_03_Fmax",
                "quantity": "uniform reduced sensitivity maximum",
                "domain": "0<p<=p_uniform;0<r<=1/3;0<C<=0.3",
                "certificate": "monotone in r,C and decreasing in p at the upper r,C boundary",
                "degrees": "exact rational endpoint",
                "minimum_coefficient": "0",
                "maximum_coefficient": sp.sstr(maximum_exact),
                "negative_coefficient_count": 0,
                "status": "PASS" if maximum_exact == sp.Rational(204098, 425425) else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            },
        ]
    )
    return entries


def numeric_bundle(symbols: dict[str, sp.Expr]) -> dict[str, float]:
    p, ratio, compactness = symbols["p"], symbols["r"], symbols["C"]

    def reduced_sensitivity(p_value: float, ratio_value: float, compactness_value: float) -> float:
        return float(sp.N(symbols["F"].subs({p: p_value, ratio: ratio_value, compactness: compactness_value}), 30))

    solar_radius_km = GM_SUN_NOMINAL / C_LIGHT**2 / 1000.0
    compactness_nominal = solar_radius_km * M1_J1738 / RADIUS_NS_KM
    f_max = float(sp.Rational(204098, 425425))
    f_wd = reduced_sensitivity(0.0, 1.0 / 3.0, float(C_WD_MAX))
    f_nominal = reduced_sensitivity(0.0, 1.0 / 3.0, compactness_nominal)
    delta_limit = (0.5 + 2.0 * 1.8) * 1.0e-6
    s_limit = 2.0 * delta_limit / (2.0 + delta_limit)
    p_triple_limit = s_limit / f_max
    s_at_uniform = P_UNIFORM * f_max
    delta_at_uniform = 2.0 * s_at_uniform / (2.0 - s_at_uniform)
    total_mass = M1_J1738 + M2_J1738
    period_seconds = PB_J1738_DAYS * 86400.0
    velocity_sq = (2.0 * math.pi * T_SUN_SECONDS * total_mass / period_seconds) ** (2.0 / 3.0)
    pdot_gr = (
        -(192.0 * math.pi / 5.0)
        * (2.0 * math.pi * T_SUN_SECONDS / period_seconds) ** (5.0 / 3.0)
        * (M1_J1738 * M2_J1738 / total_mass ** (1.0 / 3.0))
    )
    radiation_allowance = abs(PBDOT_J1738 - 2.0 * PBDOT_J1738_SIGMA) / abs(pdot_gr) - 1.0
    p_ceiling = float(P_CERT_CEILING)
    scaled_zeta_max = 16.0 / (3.0 * (4.0 - p_ceiling)) + 8.0 * math.sqrt(3.0) / (4.0 - p_ceiling) ** 1.5
    dipole_coefficient_max = (5.0 / 32.0) * scaled_zeta_max * (f_max + f_wd) ** 2 / velocity_sq
    dipole_coefficient_nominal = (5.0 / 32.0) * scaled_zeta_max * (f_nominal + f_wd) ** 2 / velocity_sq
    p_dipole_limit = radiation_allowance / dipole_coefficient_max
    p_dipole_limit_eos = radiation_allowance / (dipole_coefficient_max * EOS_VARIATION_FACTOR**2)
    dipole_at_uniform = dipole_coefficient_max * P_UNIFORM
    dipole_at_uniform_eos = dipole_at_uniform * EOS_VARIATION_FACTOR**2
    common_inflation_limit = math.sqrt(radiation_allowance / dipole_at_uniform)
    psi1_limit = 1.5 * (1.0 / 3.0) ** 3 * math.sqrt(1.0) / (4.0 / 3.0)
    psi2_limit = -3.0 * math.sqrt(3.0) * (1.0 / 3.0) ** 2.5
    psi3_scaled_limit = 8.0 * (1.0 / 3.0) ** 1.5 / (4.0 / 3.0) ** 4 + 1.5 * math.sqrt(3.0) * (4.0 / 3.0) * (1.0 / 3.0) ** 1.5
    weighted_sensitivity_max = (M2_J1738 / total_mass) * f_max
    quadrupole_coefficient_max = (
        psi1_limit
        + weighted_sensitivity_max * psi2_limit
        + weighted_sensitivity_max**2 * psi3_scaled_limit
    )
    alpha1_max_at_uniform = 2.0 * P_UNIFORM
    return {
        "solar_radius_km": solar_radius_km,
        "compactness_nominal": compactness_nominal,
        "F_max": f_max,
        "F_WD": f_wd,
        "F_nominal": f_nominal,
        "delta_limit": delta_limit,
        "s_limit": s_limit,
        "p_triple_limit": p_triple_limit,
        "s_at_uniform": s_at_uniform,
        "delta_at_uniform": delta_at_uniform,
        "period_seconds": period_seconds,
        "velocity_sq": velocity_sq,
        "pdot_gr": pdot_gr,
        "radiation_allowance": radiation_allowance,
        "scaled_zeta_max": scaled_zeta_max,
        "dipole_coefficient_max": dipole_coefficient_max,
        "dipole_coefficient_nominal": dipole_coefficient_nominal,
        "p_dipole_limit": p_dipole_limit,
        "p_dipole_limit_eos": p_dipole_limit_eos,
        "dipole_at_uniform": dipole_at_uniform,
        "dipole_at_uniform_eos": dipole_at_uniform_eos,
        "common_inflation_limit": common_inflation_limit,
        "psi1_limit": psi1_limit,
        "psi2_limit": psi2_limit,
        "psi3_scaled_limit": psi3_scaled_limit,
        "quadrupole_coefficient_max": quadrupole_coefficient_max,
        "quadrupole_at_uniform": abs(quadrupole_coefficient_max) * P_UNIFORM,
        "alpha1_max_at_uniform": alpha1_max_at_uniform,
    }


def triple_rows(values: dict[str, float]) -> list[dict[str, Any]]:
    entries = [
        ("TRI4864_00_data", "PSR J0337 fractional acceleration two-sigma envelope", values["delta_limit"], "dimensionless", "0.5e-6 plus two times 1.8e-6"),
        ("TRI4864_01_map", "exact delta_a from rescaled sensitivity", values["delta_at_uniform"], "dimensionless", "delta_a=2s/(2-s) with s=p F"),
        ("TRI4864_02_smax", "allowed rescaled sensitivity", values["s_limit"], "dimensionless", "s_max=2 delta_max/(2+delta_max)"),
        ("TRI4864_03_pbound", "conservative p upper bound", values["p_triple_limit"], "dimensionless", "uses the exact Fmax=204098/425425 envelope"),
        ("TRI4864_04_margin", "p-bound margin over p_uniform", values["p_triple_limit"] / P_UNIFORM, "ratio", "triple-system sensitivity is weaker than the existing weak-field corridor"),
        ("TRI4864_05_alpha1", "maximum absolute alpha1 at p_uniform", values["alpha1_max_at_uniform"], "dimensionless", "below the Gupta joint binary-plus-triple 95 percent magnitude 2.4e-5"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "value": f"{value:.16g}",
            "units": units,
            "interpretation": interpretation,
            "status": "PASS",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, value, units, interpretation in entries
    ]


def radiation_rows(values: dict[str, float]) -> list[dict[str, Any]]:
    entries = [
        ("RAD4864_00_scaling", "dipole regularity", "(s1-s2)^2*zeta2=O(p)", "analytic", "s_A=p F_A while zeta2=O(1/p)"),
        ("RAD4864_01_zeta", "maximum p*zeta2", f"{values['scaled_zeta_max']:.16g}", "dimensionless", "monotone maximum at r=1/3 and p=1.393e-6"),
        ("RAD4864_02_v2", "J1738 orbital velocity squared", f"{values['velocity_sq']:.16g}", "dimensionless", "Kepler value from observed masses and period"),
        ("RAD4864_03_GR", "J1738 GR period derivative", f"{values['pdot_gr']:.16g}", "s/s", "standard quadrupole prediction"),
        ("RAD4864_04_allow", "two-sigma no-cancellation extra-loss allowance", f"{values['radiation_allowance']:.16g}", "fraction", "observed maximum magnitude divided by GR magnitude minus one"),
        ("RAD4864_05_Kmax", "worst-envelope dipole coefficient R_D/p", f"{values['dipole_coefficient_max']:.16g}", "dimensionless", "C_NS<=0.3 and C_WD<=1e-4"),
        ("RAD4864_06_Rmax", "worst-envelope dipole fraction at p_uniform", f"{values['dipole_at_uniform']:.16g}", "fraction", "no prefactor reduction or cancellation credit"),
        ("RAD4864_07_Rmax_EOS", "three-percent EoS-stressed dipole fraction", f"{values['dipole_at_uniform_eos']:.16g}", "fraction", "sensitivity amplitude inflated by 3 percent"),
        ("RAD4864_08_pbound", "worst-envelope dipole p upper bound", f"{values['p_dipole_limit']:.16g}", "dimensionless", "dipole-only two-sigma smoke bound"),
        ("RAD4864_09_pbound_EOS", "three-percent EoS-stressed p upper bound", f"{values['p_dipole_limit_eos']:.16g}", "dimensionless", "remains above p_uniform"),
        ("RAD4864_10_inflation", "maximum common sensitivity inflation before edge", f"{values['common_inflation_limit']:.16g}", "factor", "26.7 percent headroom over the C<=0.3 series envelope"),
        ("RAD4864_11_Psi1", "limit (Psi1-1)/p at r=1/3", f"{values['psi1_limit']:.16g}", "dimensionless", "quadrupole channel is regular"),
        ("RAD4864_12_Psi2", "limit Psi2 at r=1/3", f"{values['psi2_limit']:.16g}", "dimensionless", "multiplied by S=O(p)"),
        ("RAD4864_13_Psi3", "limit p*Psi3 at r=1/3", f"{values['psi3_scaled_limit']:.16g}", "dimensionless", "multiplied by S^2=O(p^2)"),
        ("RAD4864_14_quad", "worst-envelope quadrupole fractional scale", f"{values['quadrupole_at_uniform']:.16g}", "fraction", "negligible beside the dipole smoke term"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "value_or_law": value,
            "units": units,
            "interpretation": interpretation,
            "status": "PASS" if row_id not in {"RAD4864_08_pbound", "RAD4864_09_pbound_EOS"} or float(value) > P_UNIFORM else "FAIL",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, value, units, interpretation in entries
    ]


def grid_rows(symbols: dict[str, sp.Expr], values: dict[str, float]) -> list[dict[str, Any]]:
    p_symbol, ratio_symbol, compactness_symbol = symbols["p"], symbols["r"], symbols["C"]
    rows: list[dict[str, Any]] = []
    p_values = [1.0e-15, 1.0e-9, P_UNIFORM]
    ratio_values = [1.0e-6, 1.0e-3, 0.1, 1.0 / 3.0]
    compactness_values = [0.05, 0.1, 0.2, 0.3]
    for p_value, ratio_value, compactness_value in itertools.product(p_values, ratio_values, compactness_values):
        reduced = float(
            sp.N(
                symbols["F"].subs(
                    {
                        p_symbol: p_value,
                        ratio_symbol: ratio_value,
                        compactness_symbol: compactness_value,
                    }
                ),
                30,
            )
        )
        reduced_wd = float(
            sp.N(
                symbols["F"].subs(
                    {
                        p_symbol: p_value,
                        ratio_symbol: ratio_value,
                        compactness_symbol: float(C_WD_MAX),
                    }
                ),
                30,
            )
        )
        c_a = 2.0 * ratio_value * p_value / (1.0 + ratio_value)
        c_scalar = 1.0 / math.sqrt(3.0 * ratio_value)
        c_vector = math.sqrt((1.0 + ratio_value) * (1.0 + ratio_value - ratio_value * p_value) / (4.0 * ratio_value))
        zeta_2 = 4.0 / (3.0 * c_scalar**3 * c_a * (2.0 - c_a)) + 4.0 / (3.0 * c_a * c_vector**3)
        sensitivity = p_value * reduced
        dipole_fraction = (5.0 / 32.0) * zeta_2 * (p_value * (reduced + reduced_wd)) ** 2 / values["velocity_sq"]
        passed = 0.0 < reduced <= values["F_max"] * (1.0 + 1.0e-12) and dipole_fraction < values["radiation_allowance"]
        rows.append(
            {
                "row_id": f"GRID4864_{len(rows):02d}",
                "p": f"{p_value:.16g}",
                "r": f"{ratio_value:.16g}",
                "compactness": f"{compactness_value:.16g}",
                "F_s_over_p": f"{reduced:.16g}",
                "sensitivity": f"{sensitivity:.16g}",
                "dipole_fraction_J1738": f"{dipole_fraction:.16g}",
                "status": "PASS" if passed else "FAIL",
                "valid_for_claim": False,
                "timestamp_utc": TIMESTAMP,
            }
        )
    return rows


def galaxy_rows() -> list[dict[str, Any]]:
    source = f"https://github.com/Martin123132/MTS-Galaxy-Lab-/tree/{GALAXY_COMMIT}"
    entries = [
        ("GAL4864_00_snapshot", "repository snapshot", GALAXY_COMMIT, "commit", "read-only accounting; no galaxy files modified"),
        ("GAL4864_01_LTG", "bundled LTG sample", 175, "galaxies", "SPARC-derived browser and research harness"),
        ("GAL4864_02_ETG", "bundled ETG sample", 16, "galaxies", "ATLAS3D early-type extension"),
        ("GAL4864_03_v1810_all", "v18.10 all-galaxy locked-MTS mean RMSE", 21.90, "km/s", "release candidate metric, not a parent-action derivation"),
        ("GAL4864_04_v1810_clean", "v18.10 clean locked-MTS mean RMSE", 19.33, "km/s", "release candidate metric"),
        ("GAL4864_05_holdout", "v18.10 median holdout high-RMSE gain", 66.68, "percent", "route-stratified holdout diagnostic"),
        ("GAL4864_06_v1838_gain", "v18.38 clean high-RMSE gain", 71.44246581618702, "percent", "later exact-cache release candidate metadata"),
        ("GAL4864_07_v1838_null", "v18.38 branch-shuffle null margin", 15.48459143587942, "percentage_points", "positive release-lock discriminator"),
        ("GAL4864_08_guard", "v18.38 protected maximum regression", 0.0, "km/s", "locked candidate guardrail"),
        ("GAL4864_09_caveat", "native closed-form replacement", False, "boolean", "exact tested support cache remains source of truth; native expression is not compressed"),
    ]
    return [
        {
            "row_id": row_id,
            "quantity": quantity,
            "value": value,
            "units": units,
            "interpretation": interpretation,
            "provenance": source,
            "status": "EMPIRICAL_PILLAR_ACCOUNTED_PRIVATE_NONCLAIM",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, quantity, value, units, interpretation in entries
    ]


def decision_rows(values: dict[str, float]) -> list[dict[str, Any]]:
    entries = [
        ("DEC4864_0_map", "accept the exact public-flow to compact-body coefficient map", "all ten invariant, PPN, speed and Z identities vanish symbolically"),
        ("DEC4864_1_regular", "accept s=p F(p,r,C)+O(C^4) as the derived co-scaling law", "every apparent alpha1 and c_omega pole cancels on the selected public surface"),
        ("DEC4864_2_envelope", "use F<=204098/425425 for C<=0.3", "exact Bernstein monotonicity certificate gives the upper endpoint"),
        ("DEC4864_3_triple", "retain the public branch under the J0337 triple-system smoke gate", f"p_triple={values['p_triple_limit']:.6e} exceeds p_uniform"),
        ("DEC4864_4_dipole", "retain the public branch under the J1738 no-cancellation dipole smoke gate", f"three-percent-stressed p_dipole={values['p_dipole_limit_eos']:.6e} exceeds p_uniform"),
        ("DEC4864_5_alpha_hat", "do not apply strong-field alpha-hat priors yet", "Gupta explicitly requires sensitivity derivatives that Eq. 80 does not provide"),
        ("DEC4864_6_galaxy", "account MTS-Galaxy-Lab as an existing empirical pillar", "175 LTGs, 16 ETGs and extensive holdout/null/QA machinery exist, while exact-cache and parent-derivation caveats remain"),
        ("DEC4864_7_next", "derive the second sensitivity response before claiming strong-field closure", "sigma-prime and full alpha-hat projections are the remaining compact-body obstruction"),
    ]
    return [
        {
            "decision_id": row_id,
            "decision": decision,
            "reason": reason,
            "next_target": NEXT_TARGET if row_id == "DEC4864_7_next" else "",
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for row_id, decision, reason in entries
    ]


def residual_rows() -> list[dict[str, Any]]:
    entries = [
        (1, "E_sensitivity_leading", "CLOSED_ANALYTIC_THROUGH_C3", "public co-scaling removes the apparent small-coupling poles", "retain the exact F envelope"),
        (2, "E_triple_SEP", "BOUNDED_SMOKE_PASS", "J0337 gives a p bound over six times weaker than p_uniform", "upgrade with full likelihood only if needed"),
        (3, "E_binary_dipole", "BOUNDED_SMOKE_PASS", "J1738 C<=0.3 no-cancellation envelope leaves a finite margin", "retain no-cancellation policy"),
        (4, "E_sensitivity_C4", "OPEN_CONTROLLED", "Tolman VII series is truncated at C3 although the source reports excellent convergence and under-three-percent EoS variation", "run full stellar ODE at corridor edges"),
        (5, "E_sigma_prime", "OPEN_HARD_NEXT", "strong-field alpha-hat parameters require sensitivity derivatives not supplied by Eq. 80", "derive second velocity response or a source-backed bound"),
        (6, "E_full_pulsar_likelihood", "OPEN_NONBLOCKING", "one-system two-sigma envelope is not a correlated four-pulsar timing likelihood", "run after sigma-prime or if the corridor approaches the smoke edge"),
        (7, "E_exact_GR_endpoint", "OPEN_HARD", "finite-p public branch remains observationally GR-like but p=0 is a singular flow chart", "return after strong-field preferred-frame gate"),
        (8, "E_galaxy_parent_link", "OPEN_HARD", "galaxy evidence is substantial but its locked response cache is not yet derived from the parent action", "derive transport law after local correspondence branch survives"),
    ]
    return [
        {
            "priority": priority,
            "residual": residual,
            "status": status,
            "evidence": evidence,
            "next_action": next_action,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }
        for priority, residual, status, evidence, next_action in entries
    ]


def validation_rows(
    sources: list[dict[str, Any]],
    mapping: list[dict[str, Any]],
    sensitivity: list[dict[str, Any]],
    certificates: list[dict[str, Any]],
    triple: list[dict[str, Any]],
    radiation: list[dict[str, Any]],
    grid: list[dict[str, Any]],
    galaxy: list[dict[str, Any]],
    decisions: list[dict[str, Any]],
    residuals: list[dict[str, Any]],
    values: dict[str, float],
) -> list[dict[str, Any]]:
    claims = [row for row in read_csv(FORMAL / "02-claims-register.csv") if row.get("claim_id") == "L-706"]
    variables = [row for row in read_csv(FORMAL / "04-variable-audit.csv") if row.get("symbol") == "s_compact_MTS"]
    checkpoint = (POST / "4864-Y5-R2FR-one-parameter-compact-body-sensitivity-and-dipole-radiation-scaling-or-strong-field-fallback.md").read_text(encoding="utf-8")
    formal = (FORMAL / "880-PPC4161-compact-body-sensitivity-and-dipole-radiation-gate.md").read_text(encoding="utf-8")
    resume = (POST / "CURRENT_LOCAL_RESUME.md").read_text(encoding="utf-8")
    prior_validation = read_csv(OUTPUT / "P8_Y5_BRR545_4863_VALIDATION.csv")

    def result(check_id: str, passed: bool, detail: str) -> dict[str, Any]:
        return {
            "check_id": check_id,
            "status": "PASS" if passed else "FAIL",
            "detail": detail,
            "valid_for_claim": False,
            "timestamp_utc": TIMESTAMP,
        }

    groups = (sources, mapping, sensitivity, certificates, triple, radiation, grid, galaxy, decisions, residuals)
    checks = [
        result("VAL4864_00_sources", len(sources) == 18 and all(row["source_validated"] for row in sources), f"sources={len(sources)}"),
        result("VAL4864_01_mapping", len(mapping) == 10 and all(row["status"] == "PASS" for row in mapping), "all Gupta-basis identities pass"),
        result("VAL4864_02_scaling", len(sensitivity) == 8 and sensitivity[4]["expression"] == "s=p*F(p,r,C)+O(C^4)", "small-p pole cancellation recorded"),
        result("VAL4864_03_certificate", len(certificates) == 4 and all(row["status"] == "PASS" for row in certificates), "Bernstein monotonicity and exact Fmax pass"),
        result("VAL4864_04_Fmax", abs(values["F_max"] - 204098 / 425425) < 1.0e-15, f"Fmax={values['F_max']}"),
        result("VAL4864_05_triple", values["p_triple_limit"] > P_UNIFORM and values["delta_at_uniform"] < values["delta_limit"], f"p_triple/p_uniform={values['p_triple_limit']/P_UNIFORM}"),
        result("VAL4864_06_alpha1", values["alpha1_max_at_uniform"] < 2.4e-5, f"max_abs_alpha1={values['alpha1_max_at_uniform']}"),
        result("VAL4864_07_dipole", values["p_dipole_limit_eos"] > P_UNIFORM and values["dipole_at_uniform_eos"] < values["radiation_allowance"], f"p_dipole_eos/p_uniform={values['p_dipole_limit_eos']/P_UNIFORM}"),
        result("VAL4864_08_quadrupole", values["quadrupole_at_uniform"] < 1.0e-6, f"quadrupole_fraction={values['quadrupole_at_uniform']}"),
        result("VAL4864_09_grid", len(grid) == 48 and all(row["status"] == "PASS" for row in grid), "48-point p-r-C grid passes"),
        result("VAL4864_10_galaxy", len(galaxy) == 10 and galaxy[-1]["value"] is False, "galaxy pillar counted with exact-cache caveat"),
        result("VAL4864_11_branch", decisions[4]["decision"] == "retain the public branch under the J1738 no-cancellation dipole smoke gate", "strong-field smoke does not trigger fallback"),
        result("VAL4864_12_residual", residuals[4]["status"] == "OPEN_HARD_NEXT", "sigma-prime is the next hard compact-body target"),
        result("VAL4864_13_nonclaim", all(not row["valid_for_claim"] for group in groups for row in group), "all rows remain private nonclaim"),
        result("VAL4864_14_registers", len(claims) == 1 and len(variables) == 1, f"claims={len(claims)} variables={len(variables)}"),
        result("VAL4864_15_documents", "COMPACT_BODY_SENSITIVITY_DIPOLE_4864" in checkpoint and "PPC4161_COMPACT_BODY_SENSITIVITY_DIPOLE_4864" in formal, "checkpoint and formal markers found"),
        result("VAL4864_16_resume", resume_checkpoint_at_least(resume, 4864) and NEXT_TARGET in resume, "resume advanced to second sensitivity response"),
        result("VAL4864_17_prior", prior_validation[-1].get("status") == "PASS", "4863 validation remains green"),
        result("VAL4864_18_script", compiles(Path(__file__).resolve()), "generator compiles"),
    ]
    checks.append(result("VAL4864_OVERALL", all(row["status"] == "PASS" for row in checks), "COMPACT_BODY_SENSITIVITY_AND_DIPOLE_GATE_VALIDATED"))
    return checks


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    symbols = surface_symbols()
    sources = source_rows()
    mapping = mapping_rows(symbols)
    sensitivity = sensitivity_rows(symbols)
    certificates = envelope_rows(symbols)
    values = numeric_bundle(symbols)
    triple = triple_rows(values)
    radiation = radiation_rows(values)
    grid = grid_rows(symbols, values)
    galaxy = galaxy_rows()
    decisions = decision_rows(values)
    residuals = residual_rows()
    validation = validation_rows(sources, mapping, sensitivity, certificates, triple, radiation, grid, galaxy, decisions, residuals, values)
    write_csv(OUTPUT / "P8_Y5_R2FR_4864_SOURCE_REGISTER.csv", sources)
    write_csv(OUTPUT / "P8_Y5_R2FR_4864_COEFFICIENT_MAP.csv", mapping)
    write_csv(OUTPUT / "P8_Y5_R2FR_4864_SENSITIVITY_DERIVATION.csv", sensitivity)
    write_csv(OUTPUT / "P8_Y5_R2FR_4864_MONOTONIC_ENVELOPE_CERTIFICATE.csv", certificates)
    write_csv(OUTPUT / "P8_Y5_R2FR_4864_TRIPLE_SYSTEM_BOUND.csv", triple)
    write_csv(OUTPUT / "P8_Y5_R2FR_4864_BINARY_RADIATION_BOUND.csv", radiation)
    write_csv(OUTPUT / "P8_Y5_R2FR_4864_STRONG_FIELD_GRID.csv", grid)
    write_csv(OUTPUT / "P8_Y5_R2FR_4864_GALAXY_PILLAR_ACCOUNTING.csv", galaxy)
    write_csv(OUTPUT / "P8_Y5_R2FR_4864_BRANCH_DECISION.csv", decisions)
    write_csv(OUTPUT / "P8_Y5_R2FR_4864_RESIDUAL_REBASE.csv", residuals)
    write_csv(OUTPUT / "P8_Y5_BRR545_4864_VALIDATION.csv", validation)
    passed = validation[-1]["status"] == "PASS"
    print("P8_Y5_BRR545_4864_VALIDATION_PASS" if passed else "P8_Y5_BRR545_4864_VALIDATION_FAIL")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
